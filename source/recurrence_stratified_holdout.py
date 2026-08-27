"""P012-B independent holdout for the frozen stratified recurrence null.

The holdout is the half-open gap-start range ``[10^9, 10^10)``.  Only
maximal-gap plateaus whose record start and next record start are both inside
that range are analyzed.  The left continuation and the final right-censored
plateau are excluded by the frozen pre-holdout contract.

This remains an empirical diagnostic.  It does not prove a prime-gap law, the
truth of the conditional null, or independence of prime gaps.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import numpy as np

from source.plateau_recurrence import RecordReference, load_record_references
from source.provenance import require_experiment_approval, sha256_file
from source.recurrence_stratified_null import (
    BIN_SCHEMES,
    DEFAULT_REPLICATIONS,
    DEFAULT_SEED,
    StratifiedNullError,
    _serializable_rows,
    accumulate_bin_counts,
    analyze_components,
    build_components,
)


EXPERIMENT = "P012B_LOGX_STRATIFIED_CONDITIONAL_NULL_HOLDOUT"
SCHEMA_VERSION = "p012b-stratified-hypergeometric-holdout-v1"
HOLDOUT_START = 1_000_000_000
HOLDOUT_END = 10_000_000_000
HOLDOUT_GAP_START_COUNT = 404_204_977
DEFAULT_SEGMENT_SPAN = 50_000_000
VALIDATED_RECORDS_SHA256 = (
    "62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297"
)
FROZEN_CONTRACT_SHA256 = (
    "1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d"
)
EXPECTED_COMPLETE_RECORD_INDICES = (31, 32, 33, 34)


class HoldoutError(StratifiedNullError):
    """Raised when the frozen P012-B holdout contract is violated."""


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _write_csv_exclusive(path: Path, rows: Sequence[dict[str, object]]) -> None:
    if not rows:
        raise HoldoutError(f"cannot write an empty table: {path.name}")
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _simple_primes(limit: int) -> np.ndarray:
    if limit < 2:
        return np.empty(0, dtype=np.int64)
    flags = np.ones(limit + 1, dtype=np.bool_)
    flags[:2] = False
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime :: prime] = False
    return np.flatnonzero(flags).astype(np.int64, copy=False)


def iter_prime_chunks_range(
    lower_inclusive: int,
    upper_exclusive: int,
    *,
    segment_span: int,
) -> Iterator[np.ndarray]:
    """Yield primes in the holdout plus the first prime at or above its end.

    The extra boundary prime closes the gap starting at the last prime below
    ``upper_exclusive``.  Bertrand's postulate bounds the search below twice
    the upper endpoint; the function still fails closed if that invariant is
    violated by an implementation error.
    """

    if not (2 < lower_inclusive < upper_exclusive):
        raise ValueError("range must satisfy 2 < lower < upper")
    if upper_exclusive > np.iinfo(np.int64).max // 2:
        raise ValueError("range is too large for the signed-int64 sieve guard")
    if segment_span < 10:
        raise ValueError("segment_span must be at least 10 integers")

    search_ceiling = 2 * upper_exclusive
    base_primes = _simple_primes(math.isqrt(search_ceiling - 1))
    low = lower_inclusive if lower_inclusive % 2 else lower_inclusive + 1
    emitted_any = False

    while low < search_ceiling:
        high = min(search_ceiling - 1, low + segment_span - 1)
        if high % 2 == 0:
            high -= 1
        if high < low:
            break
        flags = np.ones(((high - low) // 2) + 1, dtype=np.bool_)
        for prime_value in base_primes[1:]:
            prime = int(prime_value)
            if prime * prime > high:
                break
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if start % 2 == 0:
                start += prime
            flags[(start - low) // 2 :: prime] = False
        offsets = np.flatnonzero(flags).astype(np.int64, copy=False)
        chunk = low + 2 * offsets
        before = chunk[chunk < upper_exclusive]
        boundary = chunk[chunk >= upper_exclusive]
        if boundary.size:
            closed = np.concatenate((before, boundary[:1]))
            if closed.size:
                yield closed
                emitted_any = True
            if not emitted_any:
                raise HoldoutError("holdout range did not yield any prime")
            return
        if before.size:
            yield before
            emitted_any = True
        low = high + 2

    raise HoldoutError("failed to find the right-boundary prime below 2*upper")


def _load_frozen_contract(path: Path) -> dict[str, object]:
    if sha256_file(path) != FROZEN_CONTRACT_SHA256:
        raise HoldoutError("P012 frozen statistical-contract hash mismatch")
    payload = json.loads(path.read_text(encoding="utf-8"))
    holdout = payload.get("holdout")
    primary = payload.get("primary")
    if not isinstance(holdout, dict) or not isinstance(primary, dict):
        raise HoldoutError("P012 frozen contract lacks holdout or primary fields")
    checks = (
        payload.get("contract_id") == "P012_STRATIFIED_CONDITIONAL_NULL_V1",
        payload.get("status") == "FROZEN_BEFORE_HOLDOUT",
        int(payload.get("replications", -1)) == DEFAULT_REPLICATIONS,
        int(payload.get("seed", -1)) == DEFAULT_SEED,
        payload.get("forced_first_record_removed") is True,
        payload.get("theorem_claimed") is False,
        int(holdout.get("lower_inclusive", -1)) == HOLDOUT_START,
        int(holdout.get("upper_exclusive", -1)) == HOLDOUT_END,
        holdout.get("left_censored_continuation_excluded") is True,
        holdout.get("right_censored_plateau_excluded") is True,
        tuple(holdout.get("expected_complete_record_indices", ()))
        == EXPECTED_COMPLETE_RECORD_INDICES,
        primary.get("scheme") == BIN_SCHEMES[0].name,
        primary.get("cohort") == "primary_start_ge_1000",
    )
    development = payload.get("development")
    if not isinstance(development, dict) or development.get("figure_visual_qa") != "PASS":
        raise HoldoutError("P012-A figure visual QA is not frozen as PASS")
    if not all(checks):
        raise HoldoutError("P012 frozen statistical contract changed")
    return payload


def select_complete_holdout_plateaus(
    references: Sequence[RecordReference],
    *,
    lower_inclusive: int = HOLDOUT_START,
    upper_exclusive: int = HOLDOUT_END,
) -> list[dict[str, int]]:
    """Select only complete record-start exposures wholly inside holdout."""

    selected: list[dict[str, int]] = []
    for current, following in zip(references, references[1:], strict=False):
        if current.start_prime < lower_inclusive:
            continue
        if current.start_prime >= upper_exclusive:
            break
        if following.start_prime >= upper_exclusive:
            continue
        if current.verified_exhaustive_limit < upper_exclusive:
            raise HoldoutError("record source coverage is below the holdout endpoint")
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
                "N": 0,
                "M": 0,
                "C": 0,
            }
        )
    if not selected:
        raise HoldoutError("no complete holdout plateaus were selected")
    return selected


def _load_holdout_plateaus(records_path: Path) -> list[dict[str, int]]:
    if sha256_file(records_path) != VALIDATED_RECORDS_SHA256:
        raise HoldoutError("validated maximal-gap record hash mismatch")
    references = load_record_references(records_path)
    selected = select_complete_holdout_plateaus(references)
    indices = tuple(row["record_index"] for row in selected)
    if indices != EXPECTED_COMPLETE_RECORD_INDICES:
        raise HoldoutError(
            f"complete holdout record indices changed: {indices!r}"
        )
    return selected


def _derive_plateau_counts(
    provisional: Sequence[dict[str, int]],
    accumulated: dict[str, object],
) -> list[dict[str, int]]:
    exposures = accumulated["exposure_counts"]
    equal = accumulated["exposure_equal_counts"]
    if not isinstance(exposures, dict) or not isinstance(equal, dict):
        raise HoldoutError("accumulated exposure dictionaries are missing")
    completed: list[dict[str, int]] = []
    reference_totals: list[tuple[int, int]] | None = None
    for scheme in BIN_SCHEMES:
        scheme_exp = exposures.get(scheme.name)
        scheme_equal = equal.get(scheme.name)
        if not isinstance(scheme_exp, dict) or not isinstance(scheme_equal, dict):
            raise HoldoutError(f"missing accumulated scheme {scheme.name}")
        totals = []
        for plateau_id in range(len(provisional)):
            n_value = sum(
                int(count)
                for (candidate, _), count in scheme_exp.items()
                if int(candidate) == plateau_id
            )
            m_value = sum(
                int(count)
                for (candidate, _), count in scheme_equal.items()
                if int(candidate) == plateau_id
            )
            totals.append((n_value, m_value))
        if reference_totals is None:
            reference_totals = totals
        elif totals != reference_totals:
            raise HoldoutError("plateau totals change across fixed bin schemes")
    assert reference_totals is not None
    for row, (n_value, m_value) in zip(provisional, reference_totals, strict=True):
        if not n_value >= m_value >= 1:
            raise HoldoutError("holdout plateau violates N>=M>=1")
        completed.append({**row, "N": n_value, "M": m_value, "C": m_value - 1})
    return completed


def compute_holdout_analysis(
    records_path: Path,
    frozen_contract_path: Path,
    *,
    segment_span: int = DEFAULT_SEGMENT_SPAN,
    replications: int = DEFAULT_REPLICATIONS,
    seed: int = DEFAULT_SEED,
    prime_chunks: Iterable[Sequence[int] | np.ndarray] | None = None,
) -> dict[str, object]:
    contract = _load_frozen_contract(frozen_contract_path)
    if replications != DEFAULT_REPLICATIONS or seed != DEFAULT_SEED:
        raise HoldoutError("P012-B must use the frozen replications and seed")
    provisional = _load_holdout_plateaus(records_path)
    chunks = (
        prime_chunks
        if prime_chunks is not None
        else iter_prime_chunks_range(
            HOLDOUT_START,
            HOLDOUT_END,
            segment_span=segment_span,
        )
    )
    accumulated = accumulate_bin_counts(chunks, provisional)
    if int(accumulated["gap_count"]) != HOLDOUT_GAP_START_COUNT:
        raise HoldoutError(
            "holdout gap-start count disagrees with pi(10^10)-pi(10^9)"
        )
    if int(accumulated["prime_count"]) != HOLDOUT_GAP_START_COUNT + 1:
        raise HoldoutError("holdout prime stream lacks exactly one right-boundary prime")
    populations = accumulated["populations"]
    if not isinstance(populations, dict):
        raise HoldoutError("holdout population counts are missing")
    for scheme in BIN_SCHEMES:
        scheme_population = populations.get(scheme.name)
        if not isinstance(scheme_population, dict) or sum(
            int(value) for value in scheme_population.values()
        ) != HOLDOUT_GAP_START_COUNT:
            raise HoldoutError(f"holdout population total mismatch for {scheme.name}")

    plateaus = _derive_plateau_counts(provisional, accumulated)
    components = build_components(plateaus, accumulated)
    inference = analyze_components(
        plateaus,
        components,
        {},
        replications=replications,
        seed=seed,
    )
    return {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "experiment": EXPERIMENT,
        "holdout_range": {
            "lower_inclusive": str(HOLDOUT_START),
            "upper_exclusive": str(HOLDOUT_END),
        },
        "holdout_gap_start_count": HOLDOUT_GAP_START_COUNT,
        "prime_stream_count_including_boundary_prime": accumulated["prime_count"],
        "segment_span": segment_span,
        "replications": replications,
        "base_seed": seed,
        "selected_record_indices": [row["record_index"] for row in plateaus],
        "left_censored_continuation_excluded": True,
        "right_censored_plateau_excluded": True,
        "bin_schemes": [
            {"name": scheme.name, "width": scheme.width, "shift": scheme.shift}
            for scheme in BIN_SCHEMES
        ],
        "cohorts": inference["cohorts"],
        "plateaus": plateaus,
        "components": components,
        "rows": inference["rows"],
        "primary_contract": contract["primary"],
        "secondary_contract": contract["secondary"],
        "low_information_rule": contract["low_information_rule"],
        "forced_first_record_removed": True,
        "development_data_used_for_holdout_inference": False,
        "holdout_touched": True,
        "post_selection_acknowledged": True,
        "theorem_claimed": False,
        "limitations": [
            "only complete record-start plateaus wholly inside the holdout are tested",
            "the left continuation and final right-censored plateau are excluded",
            "within-bin exchangeability is a diagnostic assumption, not a theorem",
            "record-gap selection remains post-selection",
            "separate gap categories are simulated independently despite shared positions",
            "the three fixed cohorts coincide because every selected start exceeds 10^9",
            "LOW_INFORMATION is descriptive and does not alter family membership",
        ],
    }


def validate_inputs(
    records_path: Path,
    frozen_contract_path: Path,
    *,
    segment_span: int = DEFAULT_SEGMENT_SPAN,
) -> dict[str, object]:
    contract = _load_frozen_contract(frozen_contract_path)
    plateaus = _load_holdout_plateaus(records_path)
    if not 1_000_000 <= segment_span <= 200_000_000:
        raise HoldoutError("segment span is outside the reviewed P012-B range")
    return {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "holdout_range": f"[{HOLDOUT_START},{HOLDOUT_END})",
        "selected_record_indices": [row["record_index"] for row in plateaus],
        "frozen_contract_id": contract["contract_id"],
        "frozen_contract_sha256": FROZEN_CONTRACT_SHA256,
        "validated_records_sha256": VALIDATED_RECORDS_SHA256,
        "expected_gap_start_count": HOLDOUT_GAP_START_COUNT,
        "segment_span": segment_span,
        "replications": DEFAULT_REPLICATIONS,
        "seed": DEFAULT_SEED,
        "holdout_prime_stream_read": False,
        "actual_experiment_executed": False,
    }


def _plot_holdout(rows: Sequence[dict[str, object]], directory: Path) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    directory.mkdir()
    primary = [
        row
        for row in rows
        if row["scheme"] == BIN_SCHEMES[0].name
        and "primary_start_ge_1000" in row["cohorts"]
    ]
    if not primary:
        raise HoldoutError("P012-B primary figure cohort is empty")
    gaps = [int(row["gap"]) for row in primary]
    observed = [int(row["observed_recurrences"]) for row in primary]
    expected = [float(row["expected_recurrences"]) for row in primary]
    paths: list[Path] = []

    figure, axis = plt.subplots(figsize=(8, 5.5))
    axis.plot(gaps, observed, "o-", label="observed holdout recurrence")
    axis.plot(gaps, expected, "^--", label="frozen P012 expected")
    axis.set_xlabel("record gap")
    axis.set_ylabel("recurrence count")
    axis.set_title("P012-B independent holdout: observed versus expected")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    for suffix in ("png", "pdf"):
        path = directory / f"p012b_holdout_expected.{suffix}"
        figure.savefig(path, dpi=180 if suffix == "png" else None)
        paths.append(path)
    plt.close(figure)

    x = np.arange(len(gaps))
    defined_indices: list[int] = []
    defined_z: list[float] = []
    undefined_indices: list[int] = []
    for index, row in enumerate(primary):
        value = row["standardized_residual_z"]
        if value is None:
            undefined_indices.append(index)
        else:
            defined_indices.append(index)
            defined_z.append(float(value))
    figure, axis = plt.subplots(figsize=(8, 5.5))
    axis.axhline(0.0, color="black", linewidth=0.8)
    axis.bar(
        x[defined_indices],
        defined_z,
        width=0.6,
        color="tab:orange",
        label="P012-B stratified z",
    )
    if undefined_indices:
        axis.scatter(
            x[undefined_indices],
            np.zeros(len(undefined_indices)),
            marker="x",
            s=58,
            linewidths=1.7,
            color="tab:orange",
            label="z undefined (variance=0; not z=0)",
            zorder=3,
        )
    axis.set_xticks(x, [str(gap) for gap in gaps])
    axis.set_xlabel("record gap")
    axis.set_ylabel("standardized residual z")
    axis.set_title("P012-B independent holdout residuals")
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    for suffix in ("png", "pdf"):
        path = directory / f"p012b_holdout_residuals.{suffix}"
        figure.savefig(path, dpi=180 if suffix == "png" else None)
        paths.append(path)
    plt.close(figure)
    return paths


def run_holdout(
    records_path: Path,
    frozen_contract_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    segment_span: int = DEFAULT_SEGMENT_SPAN,
    replications: int = DEFAULT_REPLICATIONS,
    seed: int = DEFAULT_SEED,
    make_plots: bool = True,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P012-B result: {output_directory}")
    started = time.perf_counter()
    analysis = compute_holdout_analysis(
        records_path,
        frozen_contract_path,
        segment_span=segment_span,
        replications=replications,
        seed=seed,
    )
    output_directory.mkdir(parents=True)
    with (output_directory / "input_validated_records.csv").open("xb") as handle:
        handle.write(records_path.read_bytes())
    with (output_directory / "input_frozen_contract.json").open("xb") as handle:
        handle.write(frozen_contract_path.read_bytes())
    _write_json_exclusive(output_directory / "analysis.json", analysis)
    _write_csv_exclusive(
        output_directory / "holdout_plateaus.csv",
        _serializable_rows(analysis["plateaus"]),
    )
    _write_csv_exclusive(
        output_directory / "bin_components.csv",
        _serializable_rows(analysis["components"]),
    )
    _write_csv_exclusive(
        output_directory / "plateau_statistics.csv",
        _serializable_rows(analysis["rows"]),
    )
    _write_json_exclusive(
        output_directory / "cohort_summary.json",
        {"cohorts": analysis["cohorts"]},
    )
    figure_paths = (
        _plot_holdout(analysis["rows"], output_directory / "figures")
        if make_plots
        else []
    )
    summary = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "holdout_range": analysis["holdout_range"],
        "selected_record_indices": analysis["selected_record_indices"],
        "modeled_rows": len(analysis["rows"]),
        "component_rows": len(analysis["components"]),
        "holdout_gap_start_count": HOLDOUT_GAP_START_COUNT,
        "replications": replications,
        "base_seed": seed,
        "elapsed_seconds": time.perf_counter() - started,
        "figure_count": len(figure_paths),
        "development_data_used_for_holdout_inference": False,
        "holdout_touched": True,
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifacts = sorted(path for path in output_directory.rglob("*") if path.is_file())
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "input_sha256": {
            "validated_records": VALIDATED_RECORDS_SHA256,
            "frozen_contract": FROZEN_CONTRACT_SHA256,
        },
        "analysis_source_sha256": sha256_file(Path(__file__)),
        "artifacts_sha256": {
            path.relative_to(output_directory).as_posix(): sha256_file(path)
            for path in artifacts
        },
        "holdout_range": analysis["holdout_range"],
        "replications": replications,
        "base_seed": seed,
        "segment_span": segment_span,
        "development_data_used_for_holdout_inference": False,
        "holdout_touched": True,
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_holdout(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest_path = output_directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        saved_analysis = json.loads(
            (output_directory / "analysis.json").read_text(encoding="utf-8")
        )
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            raise HoldoutError("manifest artifact hashes are missing")
        for relative, expected in artifacts.items():
            path = output_directory / str(relative)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {relative}")
        if manifest.get("experiment") != EXPERIMENT:
            issues.append("manifest experiment identifier mismatch")
        if manifest.get("analysis_source_sha256") != sha256_file(Path(__file__)):
            issues.append("current P012-B analysis source hash differs from manifest")
        if manifest.get("holdout_touched") is not True:
            issues.append("P012-B manifest does not mark holdout access")
        if manifest.get("development_data_used_for_holdout_inference") is not False:
            issues.append("P012-B manifest claims development-data reuse")
        recomputed = compute_holdout_analysis(
            output_directory / "input_validated_records.csv",
            output_directory / "input_frozen_contract.json",
            segment_span=int(manifest["segment_span"]),
            replications=int(manifest["replications"]),
            seed=int(manifest["base_seed"]),
        )
        if recomputed != saved_analysis:
            issues.append("saved holdout analysis differs from deterministic recomputation")
    except Exception as exc:
        issues.append(f"saved P012-B verification failed: {type(exc).__name__}: {exc}")
    manifest_path = output_directory / "manifest.json"
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "deterministic_full_recomputation": "PASS" if not issues else "FAIL",
        "manifest_sha256": (
            hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            if manifest_path.is_file()
            else None
        ),
        "development_data_used_for_holdout_inference": False,
        "holdout_touched": True,
        "theorem_claimed": False,
    }


__all__ = [
    "DEFAULT_SEGMENT_SPAN",
    "EXPECTED_COMPLETE_RECORD_INDICES",
    "EXPERIMENT",
    "FROZEN_CONTRACT_SHA256",
    "HOLDOUT_END",
    "HOLDOUT_GAP_START_COUNT",
    "HOLDOUT_START",
    "HoldoutError",
    "compute_holdout_analysis",
    "iter_prime_chunks_range",
    "run_holdout",
    "select_complete_holdout_plateaus",
    "validate_inputs",
    "verify_saved_holdout",
]
