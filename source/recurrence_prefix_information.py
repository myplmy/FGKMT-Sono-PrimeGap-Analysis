"""Blinded P018 prefix information probe for future P013-style ranges.

The prefix gate deliberately uses only finite-population margins.  Observed
equal-gap recurrences, p/q values, z scores, and enrichment conclusions are
outside this module's decision surface.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

import numpy as np

from source.parallel_dual_partition import dual_partition_accumulate_bin_counts
from source.plateau_recurrence import RecordReference, load_record_references
from source.provenance import require_experiment_approval, sha256_file
from source.recurrence_information_preflight import (
    minimum_poisson_null_expectation_for_power,
    poisson_screening_metrics,
)
from source.recurrence_stratified_null import (
    BIN_SCHEMES,
    LOW_INFORMATION_MIN_CONDITIONED_GAPS,
    LOW_INFORMATION_MIN_CONTROL_EXPOSURE,
    _bin_bounds,
    _bin_indices,
)


EXPERIMENT = "P018_PREFIX_INFORMATION_PROBE"
SCHEMA_VERSION = "p018-prefix-information-v1"
CONTRACT_SHA256 = (
    "7171efef2659340e240993a384f5dfdfb1b5d60c1b1ab20880aa2129317b0f92"
)
VALIDATED_RECORDS_SHA256 = (
    "62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297"
)
COUNT_PROVENANCE = "primecount_gourdon_deleglise_rivat_match"
PROCESS_TREE_MEMORY_LIMIT_BYTES = 31_500_000_000
PRIMARY_SCHEME = BIN_SCHEMES[0].name
EXPECTED_COUNT_RANGES = {
    "P0": (1_346_294_310_749, 1_408_695_493_610),
    "A": (1_000_000_000_000, 1_968_188_556_462),
}
PROHIBITED_GATE_KEYS = {
    "C",
    "exposure_equal_counts",
    "observed_recurrences",
    "p_value",
    "q_value",
    "z_score",
}


class PrefixInformationError(RuntimeError):
    """Raised when a frozen prefix, count handoff, or blind gate is invalid."""


@dataclass(frozen=True, slots=True)
class PrefixMode:
    name: str
    lower_inclusive: int
    upper_exclusive: int
    expected_record_indices: tuple[int, ...]
    primary_segment_count: int
    verifier_segment_count: int
    hard_wall_seconds: int
    gate_evaluation_allowed: bool


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _load_json_object(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PrefixInformationError(f"cannot read JSON object {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PrefixInformationError(f"JSON root is not an object: {path}")
    return payload


def load_frozen_contract(path: Path) -> dict[str, object]:
    if sha256_file(path) != CONTRACT_SHA256:
        raise PrefixInformationError("P018 prefix contract hash mismatch")
    contract = _load_json_object(path)
    checks = (
        contract.get("contract_id") == "P018_PREFIX_INFORMATION_PROBE_V1",
        contract.get("status") == "FROZEN_BEFORE_PREFIX_EXECUTION",
        contract.get("validated_records_sha256") == VALIDATED_RECORDS_SHA256,
        contract.get("verified_exhaustive_limit") == "100000000000000000000",
        contract.get("interpretation", {}).get("theorem_claimed") is False,
        contract.get("blinding", {}).get("hypothesis_test_performed") is False,
    )
    if not all(checks):
        raise PrefixInformationError("P018 prefix contract content is invalid")
    return contract


def prefix_mode(contract: Mapping[str, object], mode: str) -> PrefixMode:
    selected = mode.upper()
    if selected not in {"P0", "A"}:
        raise PrefixInformationError("P018 prefix mode must be P0 or A")
    modes = contract.get("modes")
    if not isinstance(modes, dict) or not isinstance(modes.get(selected), dict):
        raise PrefixInformationError(f"P018 prefix mode is missing: {selected}")
    item = modes[selected]
    assert isinstance(item, dict)
    result = PrefixMode(
        name=selected,
        lower_inclusive=int(item["lower_inclusive"]),
        upper_exclusive=int(item["upper_exclusive"]),
        expected_record_indices=tuple(
            int(value) for value in item["expected_complete_record_indices"]
        ),
        primary_segment_count=int(item["primary_segment_count"]),
        verifier_segment_count=int(item["verifier_segment_count"]),
        hard_wall_seconds=int(item["hard_wall_seconds"]),
        gate_evaluation_allowed=bool(item["gate_evaluation_allowed"]),
    )
    if not result.lower_inclusive < result.upper_exclusive:
        raise PrefixInformationError("P018 prefix endpoints are not increasing")
    if math.gcd(result.primary_segment_count, result.verifier_segment_count) != 1:
        raise PrefixInformationError("P018 prefix segment counts are not coprime")
    if selected == "P0" and result.gate_evaluation_allowed:
        raise PrefixInformationError("P0 must remain calibration-only")
    if selected == "A" and not result.gate_evaluation_allowed:
        raise PrefixInformationError("A must retain its prefix gate")
    return result


def select_complete_prefix_plateaus(
    references: Sequence[RecordReference], config: PrefixMode
) -> list[dict[str, int]]:
    selected: list[dict[str, int]] = []
    for current, following in zip(references, references[1:], strict=False):
        if current.start_prime < config.lower_inclusive:
            continue
        if current.start_prime >= config.upper_exclusive:
            break
        if following.start_prime >= config.upper_exclusive:
            continue
        if current.verified_exhaustive_limit < config.upper_exclusive:
            raise PrefixInformationError("record coverage is below prefix endpoint")
        selected.append(
            {
                "record_index": current.record_index,
                "start_prime": current.start_prime,
                "end_prime": current.end_prime,
                "gap": current.gap,
                "right_exclusive": following.start_prime,
                "next_record_start_prime": following.start_prime,
                "next_record_gap": following.gap,
                "next_record_end_prime": following.end_prime,
            }
        )
    indices = tuple(row["record_index"] for row in selected)
    if indices != config.expected_record_indices:
        raise PrefixInformationError(
            f"P018-{config.name} complete record indices changed: {indices!r}"
        )
    return selected


def _parse_key_value(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw or raw.lstrip().startswith("#"):
            continue
        key, separator, value = raw.partition("=")
        if not separator or not key:
            raise PrefixInformationError(f"invalid key=value line in {path.name}")
        if key in values:
            raise PrefixInformationError(f"duplicate key in {path.name}: {key}")
        values[key] = value
    return values


def _resolve_within(project_root: Path, relative: str) -> Path:
    root = project_root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise PrefixInformationError("primecount handoff path escaped project root") from exc
    return candidate


def load_primecount_handoff(
    ready_path: Path,
    *,
    project_root: Path,
    config: PrefixMode,
) -> dict[str, object]:
    ready = _parse_key_value(ready_path)
    required_ready = {
        "counts_relative",
        "metadata_relative",
        "preparation_log_relative",
        "evidence_manifest_relative",
    }
    if set(ready) != required_ready:
        raise PrefixInformationError("P018 primecount READY keys changed")
    counts_path = _resolve_within(project_root, ready["counts_relative"])
    metadata_path = _resolve_within(project_root, ready["metadata_relative"])
    preparation_log_path = _resolve_within(
        project_root, ready["preparation_log_relative"]
    )
    evidence_manifest_path = _resolve_within(
        project_root, ready["evidence_manifest_relative"]
    )
    for path in (
        counts_path,
        metadata_path,
        preparation_log_path,
        evidence_manifest_path,
    ):
        if not path.is_file():
            raise PrefixInformationError(f"P018 primecount handoff file missing: {path}")
    validated = _validate_primecount_files(
        counts_path,
        metadata_path,
        evidence_manifest_path,
        evidence_directory=evidence_manifest_path.parent,
        config=config,
    )
    return {
        "ready_path": ready_path,
        "counts_path": counts_path,
        "metadata_path": metadata_path,
        "preparation_log_path": preparation_log_path,
        "evidence_manifest_path": evidence_manifest_path,
        **validated,
    }


def _last_decimal_line(path: Path) -> int:
    values = [line for line in path.read_text(encoding="utf-8").splitlines() if line.isdecimal()]
    if not values:
        raise PrefixInformationError(f"primecount evidence has no decimal result: {path}")
    return int(values[-1])


def _validate_primecount_files(
    counts_path: Path,
    metadata_path: Path,
    evidence_manifest_path: Path,
    *,
    evidence_directory: Path,
    config: PrefixMode,
) -> dict[str, object]:
    metadata = _parse_key_value(metadata_path)
    expected_metadata = {
        "status": "P018_PREFIX_PRIMECOUNTS_READY",
        "algorithms": "gourdon,deleglise-rivat",
        "algorithms_match": "true",
        "contract_sha256": CONTRACT_SHA256,
        "count_provenance": COUNT_PROVENANCE,
        "gpu_used": "false",
        "actual_recurrence_analysis": "false",
        "threads": "8",
        "physical_cores": "4",
    }
    for key, value in expected_metadata.items():
        if metadata.get(key) != value:
            raise PrefixInformationError(f"P018 primecount metadata mismatch: {key}")
    if metadata.get("counts_sha256") != sha256_file(counts_path):
        raise PrefixInformationError("P018 primecount CSV hash mismatch")
    cpu_list = str(metadata.get("cpu_list", "")).split(",")
    if (
        len(cpu_list) != 8
        or len(set(cpu_list)) != 8
        or any(not value.isdecimal() for value in cpu_list)
        or not 0 < int(metadata.get("virtual_memory_limit_kib", "0")) <= 31_250_000
    ):
        raise PrefixInformationError("P018 primecount CPU/memory contract mismatch")
    if metadata.get("evidence_manifest_sha256") != sha256_file(
        evidence_manifest_path
    ):
        raise PrefixInformationError("P018 primecount evidence-manifest hash mismatch")
    with counts_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if {row.get("mode") for row in rows} != {"P0", "A"} or len(rows) != 2:
        raise PrefixInformationError("P018 primecount CSV must contain P0 and A once")
    expected_evidence_values: dict[str, int] = {}
    for candidate in rows:
        candidate_mode = str(candidate["mode"]).lower()
        lower = int(candidate["lower_inclusive"])
        upper = int(candidate["upper_exclusive"])
        pi_lower = int(candidate["pi_lower_minus_1"])
        pi_upper = int(candidate["pi_upper_minus_1"])
        exact_count = int(candidate["exact_gap_start_count"])
        if (
            (lower, upper) != EXPECTED_COUNT_RANGES[str(candidate["mode"])]
            or
            int(candidate["lower_minus_1"]) != lower - 1
            or int(candidate["upper_minus_1"]) != upper - 1
            or exact_count != pi_upper - pi_lower
            or exact_count <= 0
            or candidate.get("count_provenance") != COUNT_PROVENANCE
        ):
            raise PrefixInformationError("P018 primecount CSV row is inconsistent")
        for algorithm in ("gourdon", "deleglise_rivat"):
            expected_evidence_values[
                f"{candidate_mode}_lower_minus_1_{algorithm}.txt"
            ] = pi_lower
            expected_evidence_values[
                f"{candidate_mode}_upper_minus_1_{algorithm}.txt"
            ] = pi_upper

    evidence_hashes: dict[str, str] = {}
    for raw in evidence_manifest_path.read_text(encoding="utf-8").splitlines():
        digest, separator, name = raw.partition("  ")
        if (
            separator != "  "
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
            or Path(name).name != name
            or name in evidence_hashes
        ):
            raise PrefixInformationError("invalid P018 primecount evidence manifest")
        evidence_hashes[name] = digest
    if set(evidence_hashes) != set(expected_evidence_values):
        raise PrefixInformationError("P018 primecount evidence file set changed")
    evidence_paths: list[Path] = []
    for name, expected_value in sorted(expected_evidence_values.items()):
        path = evidence_directory / name
        if not path.is_file() or sha256_file(path) != evidence_hashes[name]:
            raise PrefixInformationError(f"P018 primecount evidence mismatch: {name}")
        if _last_decimal_line(path) != expected_value:
            raise PrefixInformationError(f"P018 primecount evidence value mismatch: {name}")
        evidence_paths.append(path)

    matches = [row for row in rows if row.get("mode") == config.name]
    if len(matches) != 1:
        raise PrefixInformationError("exactly one primecount row is required for mode")
    row = matches[0]
    lower = int(row["lower_inclusive"])
    upper = int(row["upper_exclusive"])
    pi_lower = int(row["pi_lower_minus_1"])
    pi_upper = int(row["pi_upper_minus_1"])
    exact_gap_count = int(row["exact_gap_start_count"])
    if (
        lower != config.lower_inclusive
        or upper != config.upper_exclusive
        or int(row["lower_minus_1"]) != lower - 1
        or int(row["upper_minus_1"]) != upper - 1
        or exact_gap_count != pi_upper - pi_lower
        or exact_gap_count <= 0
        or row.get("count_provenance") != COUNT_PROVENANCE
    ):
        raise PrefixInformationError("P018 primecount row violates endpoint/count rules")
    return {
        "metadata": metadata,
        "row": row,
        "exact_gap_start_count": exact_gap_count,
        "evidence_paths": evidence_paths,
    }


def validate_prefix_inputs(
    records_path: Path,
    contract_path: Path,
    ready_path: Path,
    project_root: Path,
    *,
    mode: str,
) -> dict[str, object]:
    if sha256_file(records_path) != VALIDATED_RECORDS_SHA256:
        raise PrefixInformationError("validated maximal-gap record hash mismatch")
    contract = load_frozen_contract(contract_path)
    config = prefix_mode(contract, mode)
    if PROCESS_TREE_MEMORY_LIMIT_BYTES >= int(
        contract["computation"]["ram_bytes_less_than"]
    ):
        raise PrefixInformationError("P018 Windows memory limit violates contract")
    plateaus = select_complete_prefix_plateaus(
        load_record_references(records_path), config
    )
    counts = load_primecount_handoff(
        ready_path, project_root=project_root, config=config
    )
    disk_limit = int(contract["computation"]["disk_bytes_maximum"])
    disk_free = shutil.disk_usage(project_root).free
    if disk_free < disk_limit:
        raise PrefixInformationError("P018 prefix disk-free preflight failed")
    return {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "mode": config.name,
        "range": {
            "lower_inclusive": str(config.lower_inclusive),
            "upper_exclusive": str(config.upper_exclusive),
        },
        "selected_record_indices": [row["record_index"] for row in plateaus],
        "expected_gap_start_count": counts["exact_gap_start_count"],
        "primary_segment_count": config.primary_segment_count,
        "verifier_segment_count": config.verifier_segment_count,
        "hard_wall_seconds": config.hard_wall_seconds,
        "process_tree_memory_limit_bytes": PROCESS_TREE_MEMORY_LIMIT_BYTES,
        "contract_ram_bytes_less_than": int(
            contract["computation"]["ram_bytes_less_than"]
        ),
        "disk_free_bytes": disk_free,
        "disk_required_bytes": disk_limit,
        "gate_evaluation_allowed": config.gate_evaluation_allowed,
        "contract_sha256": CONTRACT_SHA256,
        "records_sha256": VALIDATED_RECORDS_SHA256,
        "counts_sha256": sha256_file(counts["counts_path"]),
        "prime_stream_read": False,
        "actual_experiment_executed": False,
    }


def build_blinded_information_components(
    plateaus: Sequence[Mapping[str, int]],
    statistics: Mapping[str, object],
) -> list[dict[str, object]]:
    """Build information margins without reading observed equal-gap counts."""

    populations = statistics.get("populations")
    gap_counts = statistics.get("gap_counts")
    exposures = statistics.get("exposure_counts")
    if not all(isinstance(value, dict) for value in (populations, gap_counts, exposures)):
        raise PrefixInformationError("blinded sufficient-statistic margins are missing")
    rows: list[dict[str, object]] = []
    for scheme in BIN_SCHEMES:
        scheme_pop = populations.get(scheme.name)
        scheme_gap = gap_counts.get(scheme.name)
        scheme_exp = exposures.get(scheme.name)
        if not all(isinstance(value, dict) for value in (scheme_pop, scheme_gap, scheme_exp)):
            raise PrefixInformationError(f"blinded scheme margins missing: {scheme.name}")
        assert isinstance(scheme_pop, dict)
        assert isinstance(scheme_gap, dict)
        assert isinstance(scheme_exp, dict)
        for plateau_id, plateau in enumerate(plateaus):
            bins = sorted(
                int(bin_index)
                for candidate, bin_index in scheme_exp
                if int(candidate) == plateau_id
            )
            if not bins:
                raise PrefixInformationError("prefix plateau has no log-bin exposure")
            forced_bin = int(
                _bin_indices(
                    np.asarray([int(plateau["start_prime"])], dtype=np.int64),
                    scheme,
                )[0]
            )
            for bin_index in bins:
                forced = 1 if bin_index == forced_bin else 0
                population = int(scheme_pop.get(bin_index, 0)) - forced
                conditioned = int(
                    scheme_gap.get((bin_index, int(plateau["gap"])), 0)
                ) - forced
                exposure = int(scheme_exp.get((plateau_id, bin_index), 0)) - forced
                if not (
                    population >= exposure >= 0
                    and population >= conditioned >= 0
                ):
                    raise PrefixInformationError("forced-record margin removal is invalid")
                control = population - exposure
                expected = exposure * conditioned / population if population else 0.0
                if population > 1:
                    probability = conditioned / population
                    variance = (
                        exposure
                        * probability
                        * (1.0 - probability)
                        * (population - exposure)
                        / (population - 1)
                    )
                else:
                    variance = 0.0
                left, right = _bin_bounds(bin_index, scheme)
                low = (
                    conditioned < LOW_INFORMATION_MIN_CONDITIONED_GAPS
                    or control < LOW_INFORMATION_MIN_CONTROL_EXPOSURE
                )
                rows.append(
                    {
                        "scheme": scheme.name,
                        "record_index": int(plateau["record_index"]),
                        "start_prime": str(plateau["start_prime"]),
                        "gap": int(plateau["gap"]),
                        "bin_index": bin_index,
                        "bin_left": left,
                        "bin_right_exclusive": right,
                        "forced_record_removed": forced,
                        "population_after_removal": population,
                        "conditioned_gap_count_after_removal": conditioned,
                        "plateau_exposure_after_removal": exposure,
                        "control_exposure": control,
                        "expected_component": expected,
                        "variance_component": variance,
                        "information_flag": "LOW_INFORMATION" if low else "OK",
                    }
                )
    _assert_no_prohibited_gate_keys(rows)
    return rows


def _assert_no_prohibited_gate_keys(payload: object) -> None:
    if isinstance(payload, dict):
        overlap = PROHIBITED_GATE_KEYS & set(map(str, payload))
        if overlap:
            raise PrefixInformationError(
                f"blinded gate contains prohibited keys: {sorted(overlap)!r}"
            )
        for value in payload.values():
            _assert_no_prohibited_gate_keys(value)
    elif isinstance(payload, list):
        for value in payload:
            _assert_no_prohibited_gate_keys(value)


def _plateau_information_rows(
    plateaus: Sequence[Mapping[str, int]],
    components: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scheme in BIN_SCHEMES:
        for plateau in plateaus:
            selected = [
                row
                for row in components
                if row["scheme"] == scheme.name
                and int(row["record_index"]) == int(plateau["record_index"])
            ]
            if not selected:
                raise PrefixInformationError("missing blinded plateau components")
            rows.append(
                {
                    "scheme": scheme.name,
                    "record_index": int(plateau["record_index"]),
                    "start_prime": str(plateau["start_prime"]),
                    "gap": int(plateau["gap"]),
                    "post_record_trials": sum(
                        int(row["plateau_exposure_after_removal"])
                        for row in selected
                    ),
                    "expected_recurrences": sum(
                        float(row["expected_component"]) for row in selected
                    ),
                    "variance": sum(
                        float(row["variance_component"]) for row in selected
                    ),
                    "component_count": len(selected),
                    "low_information_component_count": sum(
                        row["information_flag"] == "LOW_INFORMATION"
                        for row in selected
                    ),
                    "information_flag": "LOW_INFORMATION"
                    if any(
                        row["information_flag"] == "LOW_INFORMATION"
                        for row in selected
                    )
                    else "OK",
                }
            )
    _assert_no_prohibited_gate_keys(rows)
    return rows


def build_prefix_gate_report(
    contract: Mapping[str, object],
    config: PrefixMode,
    plateaus: Sequence[Mapping[str, int]],
    components: Sequence[Mapping[str, object]],
    *,
    exact_gap_start_count: int,
) -> dict[str, object]:
    rows = _plateau_information_rows(plateaus, components)
    primary = [row for row in rows if row["scheme"] == PRIMARY_SCHEME]
    positive = [row for row in primary if float(row["variance"]) > 0.0]
    total_expected = sum(float(row["expected_recurrences"]) for row in primary)
    informative_expected = sum(
        float(row["expected_recurrences"]) for row in positive
    )
    low_count = sum(row["information_flag"] == "LOW_INFORMATION" for row in primary)
    low_fraction = low_count / len(primary) if primary else 1.0
    event_probability = -math.expm1(-informative_expected)
    gate_contract = contract["gates"]["A_EXPLORATORY_PREFIX_ONLY"]
    assert isinstance(gate_contract, dict)
    thresholds = {
        "alpha": float(gate_contract["alpha"]),
        "event_probability_target": float(
            gate_contract["event_probability_target"]
        ),
        "minimum_positive_variance_rows": int(
            gate_contract["minimum_positive_variance_rows"]
        ),
        "maximum_low_information_fraction": float(
            gate_contract["maximum_low_information_fraction"]
        ),
        "effect_multiplier": float(gate_contract["effect_multiplier"]),
        "power_target": float(gate_contract["power_target"]),
    }
    if informative_expected > 0:
        screen = poisson_screening_metrics(
            informative_expected,
            alpha=thresholds["alpha"],
            effect_multipliers=(thresholds["effect_multiplier"],),
        )
        power = float(
            screen["screening_power_by_effect_multiplier"][
                f"{thresholds['effect_multiplier']:g}x"
            ]
        )
    else:
        screen = {
            "model": "poisson_count_screening_proxy",
            "alpha": thresholds["alpha"],
            "null_expected_recurrences": 0.0,
            "null_probability_at_least_one": 0.0,
            "critical_count": 1,
            "screening_power_by_effect_multiplier": {
                f"{thresholds['effect_multiplier']:g}x": 0.0
            },
            "is_actual_stratified_hypergeometric_family_power": False,
        }
        power = 0.0
    power_requirement = minimum_poisson_null_expectation_for_power(
        alpha=thresholds["alpha"],
        effect_multiplier=thresholds["effect_multiplier"],
        power_target=thresholds["power_target"],
    )
    structural_pass = (
        event_probability >= thresholds["event_probability_target"]
        and len(positive) >= thresholds["minimum_positive_variance_rows"]
        and low_fraction <= thresholds["maximum_low_information_fraction"]
    )
    power_pass = power >= thresholds["power_target"]
    gate_pass = config.gate_evaluation_allowed and structural_pass and power_pass
    recommendation = (
        "CALIBRATION_ONLY_NO_GATE"
        if not config.gate_evaluation_allowed
        else "REVIEW_BALANCED_B_DESIGN"
        if gate_pass
        else "HOLD_PREFIX_INFORMATION"
    )
    report = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "mode": config.name,
        "gate_role": "CALIBRATION_ONLY"
        if not config.gate_evaluation_allowed
        else "A_EXPLORATORY_PREFIX_ONLY",
        "primary_scheme": PRIMARY_SCHEME,
        "primary_plateau_rows": len(primary),
        "primary_positive_variance_rows": len(positive),
        "primary_low_information_rows": low_count,
        "primary_low_information_fraction": low_fraction,
        "primary_expected_recurrences_total": total_expected,
        "primary_informative_expected_recurrences": informative_expected,
        "poisson_proxy_probability_at_least_one": event_probability,
        "poisson_screening_power": power,
        "poisson_screen": screen,
        "poisson_power_requirement": power_requirement,
        "planning_thresholds": thresholds,
        "structural_information_gate_pass": structural_pass,
        "poisson_screening_power_gate_pass": power_pass,
        "prefix_A_gate_pass": gate_pass,
        "recommendation": recommendation,
        "automatic_full_range_promotion": False,
        "formal_power_certified": False,
        "hypothesis_test_performed": False,
        "enrichment_claimed": False,
        "exact_gap_start_count": exact_gap_start_count,
        "informative_expected_recurrences_per_billion_gap_starts": informative_expected
        * 1_000_000_000
        / exact_gap_start_count,
        "linear_extrapolation_allowed": False,
        "theorem_claimed": False,
    }
    _assert_no_prohibited_gate_keys(report)
    return report


def _mapping_rows(mapping: Mapping[object, object]) -> list[list[object]]:
    rows: list[list[object]] = []
    for key, value in mapping.items():
        encoded_key: object = list(key) if isinstance(key, tuple) else key
        rows.append([encoded_key, int(value)])
    rows.sort(key=lambda row: json.dumps(row[0], separators=(",", ":")))
    return rows


def _canonical_statistics(
    statistics: Mapping[str, object], *, include_observed_equal: bool
) -> dict[str, object]:
    fields = ["populations", "gap_counts", "exposure_counts"]
    if include_observed_equal:
        fields.append("exposure_equal_counts")
    payload: dict[str, object] = {
        "prime_count": int(statistics["prime_count"]),
        "gap_count": int(statistics["gap_count"]),
    }
    for field in fields:
        schemes = statistics[field]
        if not isinstance(schemes, dict):
            raise PrefixInformationError(f"statistics field is invalid: {field}")
        payload[field] = {
            str(scheme): _mapping_rows(counts)
            for scheme, counts in sorted(schemes.items())
        }
    return payload


def _decode_canonical_margin_statistics(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise PrefixInformationError("canonical margin statistics are not an object")
    expected_fields = {
        "prime_count",
        "gap_count",
        "populations",
        "gap_counts",
        "exposure_counts",
    }
    if set(payload) != expected_fields:
        raise PrefixInformationError("canonical margin-statistic fields changed")
    prime_count = int(payload["prime_count"])
    gap_count = int(payload["gap_count"])
    if gap_count < 0 or prime_count != gap_count + 1:
        raise PrefixInformationError("canonical prime/gap count invariant failed")
    decoded: dict[str, object] = {
        "prime_count": prime_count,
        "gap_count": gap_count,
    }
    expected_schemes = {scheme.name for scheme in BIN_SCHEMES}
    for field in ("populations", "gap_counts", "exposure_counts"):
        schemes = payload[field]
        if not isinstance(schemes, dict) or set(schemes) != expected_schemes:
            raise PrefixInformationError(f"canonical margin schemes changed: {field}")
        decoded_schemes: dict[str, dict[object, int]] = {}
        for scheme, rows in schemes.items():
            if not isinstance(rows, list):
                raise PrefixInformationError("canonical margin rows are not a list")
            mapping: dict[object, int] = {}
            for item in rows:
                if not isinstance(item, list) or len(item) != 2:
                    raise PrefixInformationError("canonical margin row is malformed")
                encoded_key, raw_value = item
                if isinstance(encoded_key, list):
                    key: object = tuple(int(value) for value in encoded_key)
                else:
                    key = int(encoded_key)
                value = int(raw_value)
                if value < 0 or key in mapping:
                    raise PrefixInformationError("canonical margin count/key is invalid")
                mapping[key] = value
            decoded_schemes[str(scheme)] = mapping
        decoded[field] = decoded_schemes
    _assert_no_prohibited_gate_keys(decoded)
    return decoded


def _payload_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _scientific_source_paths() -> dict[str, Path]:
    source_directory = Path(__file__).resolve().parent
    return {
        "recurrence_prefix_information": Path(__file__).resolve(),
        "recurrence_prefix_information_cli": source_directory
        / "recurrence_prefix_information_cli.py",
        "parallel_dual_partition": source_directory / "parallel_dual_partition.py",
        "parallel_segment_statistics": source_directory / "parallel_segment_statistics.py",
        "recurrence_stratified_holdout": source_directory
        / "recurrence_stratified_holdout.py",
        "recurrence_stratified_null": source_directory / "recurrence_stratified_null.py",
        "recurrence_information_preflight": source_directory
        / "recurrence_information_preflight.py",
        "plateau_recurrence": source_directory / "plateau_recurrence.py",
        "runtime_resources": source_directory / "runtime_resources.py",
        "live_progress": source_directory / "live_progress.py",
    }


def run_prefix_probe(
    records_path: Path,
    contract_path: Path,
    ready_path: Path,
    project_root: Path,
    output_directory: Path,
    *,
    mode: str,
    approval_token: str | None,
    worker_count: int = 8,
    runtime_resource_policy: dict[str, object] | None = None,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P018 prefix result: {output_directory}")
    started = time.monotonic()
    if sha256_file(records_path) != VALIDATED_RECORDS_SHA256:
        raise PrefixInformationError("validated maximal-gap record hash mismatch")
    contract = load_frozen_contract(contract_path)
    config = prefix_mode(contract, mode)
    if PROCESS_TREE_MEMORY_LIMIT_BYTES >= int(
        contract["computation"]["ram_bytes_less_than"]
    ):
        raise PrefixInformationError("P018 Windows memory limit violates contract")
    if worker_count != int(contract["computation"]["worker_processes"]):
        raise PrefixInformationError("P018 prefix worker count differs from contract")
    plateaus = select_complete_prefix_plateaus(
        load_record_references(records_path), config
    )
    counts = load_primecount_handoff(
        ready_path, project_root=project_root, config=config
    )
    exact_gap_count = int(counts["exact_gap_start_count"])
    disk_limit = int(contract["computation"]["disk_bytes_maximum"])
    disk_free = shutil.disk_usage(project_root).free
    if disk_free < disk_limit:
        raise PrefixInformationError("P018 prefix disk-free preflight failed")
    input_paths = {
        "input_validated_records.csv": records_path,
        "input_prefix_contract.json": contract_path,
        "input_prime_counts.csv": counts["counts_path"],
        "input_primecount_metadata.txt": counts["metadata_path"],
        "input_primecount_ready.txt": counts["ready_path"],
        "input_primecount_preparation.log": counts["preparation_log_path"],
        "input_primecount_evidence.sha256": counts["evidence_manifest_path"],
    }
    input_hashes = {
        name: sha256_file(Path(path)) for name, path in input_paths.items()
    }
    evidence_hashes = {
        Path(path).name: sha256_file(Path(path))
        for path in counts["evidence_paths"]
    }
    source_paths = _scientific_source_paths()
    source_hashes = {name: sha256_file(path) for name, path in source_paths.items()}

    def progress(payload: dict[str, object]) -> None:
        elapsed = time.monotonic() - started
        if elapsed > config.hard_wall_seconds:
            raise PrefixInformationError(
                f"P018-{config.name} exceeded frozen wall limit"
            )
        if progress_callback is not None:
            progress_callback({"mode": config.name, **payload})

    dual = dual_partition_accumulate_bin_counts(
        config.lower_inclusive,
        config.upper_exclusive,
        plateaus,
        expected_gap_start_count=exact_gap_count,
        worker_count=worker_count,
        primary_segment_count=config.primary_segment_count,
        verifier_segment_count=config.verifier_segment_count,
        primary_sieve_segment_span=int(
            contract["computation"]["primary_sieve_segment_span"]
        ),
        verifier_sieve_segment_span=int(
            contract["computation"]["verifier_sieve_segment_span"]
        ),
        progress_callback=progress,
        deadline_monotonic=started + config.hard_wall_seconds,
    )
    elapsed = time.monotonic() - started
    if elapsed > config.hard_wall_seconds:
        raise PrefixInformationError(f"P018-{config.name} exceeded frozen wall limit")
    statistics = dual["statistics"]
    if not isinstance(statistics, dict):
        raise PrefixInformationError("dual-partition statistics are missing")
    components = build_blinded_information_components(plateaus, statistics)
    gate_report = build_prefix_gate_report(
        contract,
        config,
        plateaus,
        components,
        exact_gap_start_count=exact_gap_count,
    )
    gate_report["informative_expected_recurrences_per_wall_hour"] = (
        float(gate_report["primary_informative_expected_recurrences"])
        * 3600.0
        / elapsed
        if elapsed > 0
        else None
    )
    margin_payload = _canonical_statistics(
        statistics, include_observed_equal=False
    )
    margin_digest = _payload_sha256(margin_payload)
    dual_summary = {
        key: value for key, value in dual.items() if key != "statistics"
    }
    dual_summary.update(
        {
            "blinded_margin_statistics_sha256": margin_digest,
            "observed_equal_counts_saved": False,
        }
    )
    summary = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "mode": config.name,
        "range": {
            "lower_inclusive": str(config.lower_inclusive),
            "upper_exclusive": str(config.upper_exclusive),
        },
        "selected_record_indices": [row["record_index"] for row in plateaus],
        "exact_gap_start_count": exact_gap_count,
        "elapsed_seconds": elapsed,
        "gate_recommendation": gate_report["recommendation"],
        "prefix_A_gate_pass": gate_report["prefix_A_gate_pass"],
        "hypothesis_test_performed": False,
        "observed_recurrence_saved": False,
        "automatic_full_range_promotion": False,
        "gpu_used": False,
        "runtime_resource_policy": runtime_resource_policy,
        "theorem_claimed": False,
    }
    current_input_hashes = {
        name: sha256_file(Path(path)) for name, path in input_paths.items()
    }
    current_evidence_hashes = {
        Path(path).name: sha256_file(Path(path))
        for path in counts["evidence_paths"]
    }
    current_source_hashes = {
        name: sha256_file(path) for name, path in source_paths.items()
    }
    if current_input_hashes != input_hashes:
        raise PrefixInformationError("P018 prefix input changed during computation")
    if current_evidence_hashes != evidence_hashes:
        raise PrefixInformationError("P018 primecount evidence changed during computation")
    if current_source_hashes != source_hashes:
        raise PrefixInformationError("P018 scientific source changed during computation")

    output_directory.mkdir(parents=True)
    for name, source in input_paths.items():
        with (output_directory / name).open("xb") as target:
            target.write(Path(source).read_bytes())
    evidence_output = output_directory / "input_primecount_evidence"
    evidence_output.mkdir()
    for source in counts["evidence_paths"]:
        source_path = Path(source)
        with (evidence_output / source_path.name).open("xb") as target:
            target.write(source_path.read_bytes())
    _write_json_exclusive(output_directory / "plateaus.json", plateaus)
    _write_json_exclusive(
        output_directory / "blinded_margin_statistics.json", margin_payload
    )
    _write_json_exclusive(
        output_directory / "blinded_information_components.json", components
    )
    _write_json_exclusive(output_directory / "prefix_gate_report.json", gate_report)
    _write_json_exclusive(
        output_directory / "dual_partition_verification.json", dual_summary
    )
    _write_json_exclusive(output_directory / "summary.json", summary)
    disk_bytes = sum(
        path.stat().st_size for path in output_directory.rglob("*") if path.is_file()
    )
    if disk_bytes > disk_limit:
        raise PrefixInformationError("P018 prefix result exceeded disk contract")
    artifacts = sorted(path for path in output_directory.rglob("*") if path.is_file())
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "mode": config.name,
        "input_sha256": {
            **input_hashes,
            **{
                f"input_primecount_evidence/{name}": digest
                for name, digest in evidence_hashes.items()
            },
        },
        "source_sha256": source_hashes,
        "artifacts_sha256": {
            path.relative_to(output_directory).as_posix(): sha256_file(path)
            for path in artifacts
        },
        "blinded_margin_statistics_sha256": margin_digest,
        "dual_parallel_passes": 2,
        "serial_oracle_used": False,
        "observed_equal_counts_saved": False,
        "hypothesis_test_performed": False,
        "automatic_full_range_promotion": False,
        "disk_bytes_before_manifest": disk_bytes,
        "gpu_used": False,
        "theorem_claimed": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_prefix(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest_path = output_directory / "manifest.json"
        manifest = _load_json_object(manifest_path)
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            raise PrefixInformationError("saved artifact hash table is missing")
        for relative, expected in artifacts.items():
            path = output_directory / str(relative)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {relative}")
        source_hashes = manifest.get("source_sha256")
        if not isinstance(source_hashes, dict):
            raise PrefixInformationError("saved source hashes are missing")
        current_sources = {
            name: sha256_file(path)
            for name, path in _scientific_source_paths().items()
        }
        if source_hashes != current_sources:
            issues.append("current P018 prefix sources differ from manifest")

        saved_input_paths = {
            "input_validated_records.csv": output_directory
            / "input_validated_records.csv",
            "input_prefix_contract.json": output_directory
            / "input_prefix_contract.json",
            "input_prime_counts.csv": output_directory / "input_prime_counts.csv",
            "input_primecount_metadata.txt": output_directory
            / "input_primecount_metadata.txt",
            "input_primecount_ready.txt": output_directory
            / "input_primecount_ready.txt",
            "input_primecount_preparation.log": output_directory
            / "input_primecount_preparation.log",
            "input_primecount_evidence.sha256": output_directory
            / "input_primecount_evidence.sha256",
        }
        saved_input_hashes = {
            name: sha256_file(path) for name, path in saved_input_paths.items()
        }
        evidence_directory = output_directory / "input_primecount_evidence"
        for path in sorted(evidence_directory.glob("*.txt")):
            saved_input_hashes[f"input_primecount_evidence/{path.name}"] = sha256_file(
                path
            )
        if manifest.get("input_sha256") != saved_input_hashes:
            issues.append("saved input/evidence hashes differ from manifest")
        if (
            saved_input_hashes["input_validated_records.csv"]
            != VALIDATED_RECORDS_SHA256
        ):
            issues.append("saved validated-record hash changed")

        contract = load_frozen_contract(saved_input_paths["input_prefix_contract.json"])
        config = prefix_mode(contract, str(manifest["mode"]))
        primecount = _validate_primecount_files(
            saved_input_paths["input_prime_counts.csv"],
            saved_input_paths["input_primecount_metadata.txt"],
            saved_input_paths["input_primecount_evidence.sha256"],
            evidence_directory=evidence_directory,
            config=config,
        )
        exact_gap_count = int(primecount["exact_gap_start_count"])
        recomputed_plateaus = select_complete_prefix_plateaus(
            load_record_references(saved_input_paths["input_validated_records.csv"]),
            config,
        )
        plateaus = json.loads(
            (output_directory / "plateaus.json").read_text(encoding="utf-8")
        )
        if plateaus != recomputed_plateaus:
            issues.append("saved plateau selection differs from frozen records/range")

        margin_payload = _load_json_object(
            output_directory / "blinded_margin_statistics.json"
        )
        margin_digest = _payload_sha256(margin_payload)
        if manifest.get("blinded_margin_statistics_sha256") != margin_digest:
            issues.append("saved blinded-margin digest differs from manifest")
        margin_statistics = _decode_canonical_margin_statistics(margin_payload)
        recomputed_components = build_blinded_information_components(
            recomputed_plateaus, margin_statistics
        )
        components = json.loads(
            (output_directory / "blinded_information_components.json").read_text(
                encoding="utf-8"
            )
        )
        if components != recomputed_components:
            issues.append("saved components differ from blinded-margin recomputation")
        saved_gate = _load_json_object(output_directory / "prefix_gate_report.json")
        recomputed = build_prefix_gate_report(
            contract,
            config,
            recomputed_plateaus,
            recomputed_components,
            exact_gap_start_count=exact_gap_count,
        )
        saved_without_runtime = dict(saved_gate)
        saved_without_runtime.pop(
            "informative_expected_recurrences_per_wall_hour", None
        )
        if recomputed != saved_without_runtime:
            issues.append("saved blinded gate differs from margin-only recomputation")
        _assert_no_prohibited_gate_keys(margin_payload)
        _assert_no_prohibited_gate_keys(recomputed_components)
        _assert_no_prohibited_gate_keys(saved_gate)
        dual = _load_json_object(output_directory / "dual_partition_verification.json")
        if (
            dual.get("status") != "PASS"
            or dual.get("exact_statistics_equal") is not True
            or dual.get("observed_equal_counts_saved") is not False
            or dual.get("expected_gap_start_count") != exact_gap_count
            or dual.get("blinded_margin_statistics_sha256") != margin_digest
        ):
            issues.append("saved dual-partition verification is not PASS/blinded")
        summary = _load_json_object(output_directory / "summary.json")
        if (
            summary.get("exact_gap_start_count") != exact_gap_count
            or summary.get("gate_recommendation") != saved_gate.get("recommendation")
            or summary.get("prefix_A_gate_pass")
            != saved_gate.get("prefix_A_gate_pass")
            or summary.get("observed_recurrence_saved") is not False
        ):
            issues.append("saved summary differs from counts/blinded gate")
    except Exception as exc:
        issues.append(
            f"saved P018 prefix verification failed: {type(exc).__name__}: {exc}"
        )
    manifest_path = output_directory / "manifest.json"
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "saved_blinded_margin_recomputation": "PASS" if not issues else "FAIL",
        "manifest_sha256": sha256_file(manifest_path)
        if manifest_path.is_file()
        else None,
        "full_prime_range_recomputed": False,
        "dual_parallel_passes_already_required": True,
        "hypothesis_test_performed": False,
        "theorem_claimed": False,
    }


__all__ = [
    "CONTRACT_SHA256",
    "EXPERIMENT",
    "PrefixInformationError",
    "PrefixMode",
    "PROCESS_TREE_MEMORY_LIMIT_BYTES",
    "build_blinded_information_components",
    "build_prefix_gate_report",
    "load_frozen_contract",
    "load_primecount_handoff",
    "prefix_mode",
    "run_prefix_probe",
    "select_complete_prefix_plateaus",
    "validate_prefix_inputs",
    "verify_saved_prefix",
]
