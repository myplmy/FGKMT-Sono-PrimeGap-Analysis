"""Prospective P013 extensions of the frozen P012 recurrence diagnostic.

Each stage analyzes one half-open prime-gap-start range.  The statistical
rules are inherited unchanged from P012, while the ranges, seeds, exact prime
counts, and two-stage Bonferroni threshold were frozen before either P013
range was read.  This is an empirical diagnostic, not a prime-gap theorem.
"""

from __future__ import annotations

import csv
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np

from source.plateau_recurrence import RecordReference, load_record_references
from source.provenance import require_experiment_approval, sha256_file
from source.recurrence_stratified_holdout import iter_prime_chunks_range
from source.recurrence_stratified_null import (
    BIN_SCHEMES,
    _serializable_rows,
    accumulate_bin_counts,
    analyze_components,
    build_components,
)


EXPERIMENT = "P013_PROSPECTIVE_STRATIFIED_RECURRENCE_EXTENSION"
SCHEMA_VERSION = "p013-prospective-stratified-recurrence-extension-v1"
VALIDATED_RECORDS_SHA256 = (
    "62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297"
)
P012_CONTRACT_SHA256 = (
    "1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d"
)
P013_CONTRACT_SHA256 = (
    "153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf"
)
P012B_MANIFEST_SHA256 = (
    "299e0bbd3e754c0f5f716ddfaea4b09bb4e0cd6adcb6f98e94e6f0a71abc89e5"
)
P012B_SAVED_REPORT_SHA256 = (
    "da3da7439f81f6ec40a8a28c4349984c59790f411ffdfca24c1999b0505b6bf9"
)
DEFAULT_SEGMENT_SPAN = 50_000_000
DEFAULT_REPLICATIONS = 100_000


class SequentialExtensionError(RuntimeError):
    """Raised when a frozen P013 contract or result invariant fails."""


@dataclass(frozen=True)
class StageConfig:
    name: str
    lower_inclusive: int
    upper_exclusive: int
    expected_gap_start_count: int
    expected_record_indices: tuple[int, ...]
    seed: int


STAGES = {
    "A": StageConfig(
        "A", 10**10, 10**11, 3_663_002_302, (36, 37, 38, 39), 20260828
    ),
    "B": StageConfig(
        "B",
        10**11,
        10**12,
        33_489_857_205,
        (41, 42, 43, 44, 45, 46, 47, 48, 49),
        20260829,
    ),
}


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _write_csv_exclusive(path: Path, rows: Sequence[dict[str, object]]) -> None:
    if not rows:
        raise SequentialExtensionError(f"cannot write empty table: {path.name}")
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _stage(stage: str) -> StageConfig:
    try:
        return STAGES[stage.upper()]
    except KeyError as exc:
        raise SequentialExtensionError("P013 stage must be A or B") from exc


def _load_contract(path: Path) -> dict[str, object]:
    if sha256_file(path) != P013_CONTRACT_SHA256:
        raise SequentialExtensionError("P013 frozen contract hash mismatch")
    payload = json.loads(path.read_text(encoding="utf-8"))
    checks = (
        payload.get("contract_id")
        == "P013_PROSPECTIVE_STRATIFIED_RECURRENCE_EXTENSION_V1",
        payload.get("status") == "FROZEN_BEFORE_P013_EXECUTION",
        payload.get("parent_p012_contract_sha256") == P012_CONTRACT_SHA256,
        payload.get("validated_records_sha256") == VALIDATED_RECORDS_SHA256,
        int(payload.get("replications_per_stage", -1)) == DEFAULT_REPLICATIONS,
        payload.get("forced_first_record_removed") is True,
        payload.get("pooling_after_results_prohibited") is True,
        payload.get("theorem_claimed") is False,
        payload.get("zero_variance_rule")
        == "retain row with z=null and exclude only from z-based family calculation",
    )
    prerequisite = payload.get("p012b_prerequisite")
    primary = payload.get("primary")
    if not isinstance(prerequisite, dict) or not isinstance(primary, dict):
        raise SequentialExtensionError("P013 contract prerequisite/primary missing")
    checks += (
        prerequisite.get("manifest_sha256") == P012B_MANIFEST_SHA256,
        prerequisite.get("saved_verification_report_sha256")
        == P012B_SAVED_REPORT_SHA256,
        prerequisite.get("figure_visual_qa") == "PASS",
        primary.get("scheme") == BIN_SCHEMES[0].name,
        primary.get("cohort") == "primary_start_ge_1000",
        float(primary.get("two_stage_bonferroni_alpha_each", -1)) == 0.025,
    )
    schemes = payload.get("bin_schemes")
    expected_schemes = [
        {"name": item.name, "width": item.width, "shift": item.shift}
        for item in BIN_SCHEMES
    ]
    checks += (schemes == expected_schemes,)
    stages = payload.get("stages")
    if not isinstance(stages, dict):
        raise SequentialExtensionError("P013 contract stage map missing")
    for name, config in STAGES.items():
        item = stages.get(name)
        if not isinstance(item, dict):
            raise SequentialExtensionError(f"P013 contract stage {name} missing")
        checks += (
            int(item.get("lower_inclusive", -1)) == config.lower_inclusive,
            int(item.get("upper_exclusive", -1)) == config.upper_exclusive,
            int(item.get("expected_gap_start_count", -1))
            == config.expected_gap_start_count,
            tuple(item.get("expected_complete_record_indices", ()))
            == config.expected_record_indices,
            int(item.get("seed", -1)) == config.seed,
            item.get("left_censored_continuation_excluded") is True,
            item.get("right_censored_plateau_excluded") is True,
        )
    if not all(checks):
        raise SequentialExtensionError("P013 frozen contract content changed")
    return payload


def _validate_prerequisites(
    records_path: Path,
    p012_contract_path: Path,
    p013_contract_path: Path,
    p012b_manifest_path: Path,
    p012b_saved_report_path: Path,
) -> dict[str, object]:
    if sha256_file(records_path) != VALIDATED_RECORDS_SHA256:
        raise SequentialExtensionError("validated maximal-gap record hash mismatch")
    if sha256_file(p012_contract_path) != P012_CONTRACT_SHA256:
        raise SequentialExtensionError("parent P012 contract hash mismatch")
    contract = _load_contract(p013_contract_path)
    if sha256_file(p012b_manifest_path) != P012B_MANIFEST_SHA256:
        raise SequentialExtensionError("P012-B prerequisite manifest hash mismatch")
    if sha256_file(p012b_saved_report_path) != P012B_SAVED_REPORT_SHA256:
        raise SequentialExtensionError("P012-B saved report hash mismatch")
    manifest = json.loads(p012b_manifest_path.read_text(encoding="utf-8"))
    report = json.loads(p012b_saved_report_path.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "PASS"
        or manifest.get("experiment")
        != "P012B_LOGX_STRATIFIED_CONDITIONAL_NULL_HOLDOUT"
        or report.get("status") != "PASS"
        or report.get("deterministic_full_recomputation") != "PASS"
        or report.get("manifest_sha256") != P012B_MANIFEST_SHA256
    ):
        raise SequentialExtensionError("P012-B prerequisite is not a bound PASS")
    return contract


def select_complete_plateaus(
    references: Sequence[RecordReference], config: StageConfig
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
            raise SequentialExtensionError("record coverage is below stage endpoint")
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
    indices = tuple(row["record_index"] for row in selected)
    if indices != config.expected_record_indices:
        raise SequentialExtensionError(
            f"P013-{config.name} complete record indices changed: {indices!r}"
        )
    return selected


def _derive_plateau_counts(
    provisional: Sequence[dict[str, int]], accumulated: dict[str, object]
) -> list[dict[str, int]]:
    exposures = accumulated["exposure_counts"]
    equal = accumulated["exposure_equal_counts"]
    if not isinstance(exposures, dict) or not isinstance(equal, dict):
        raise SequentialExtensionError("accumulated exposure maps missing")
    reference: list[tuple[int, int]] | None = None
    for scheme in BIN_SCHEMES:
        scheme_exp = exposures.get(scheme.name)
        scheme_equal = equal.get(scheme.name)
        if not isinstance(scheme_exp, dict) or not isinstance(scheme_equal, dict):
            raise SequentialExtensionError(f"missing scheme counts: {scheme.name}")
        totals = [
            (
                sum(int(v) for (candidate, _), v in scheme_exp.items() if candidate == i),
                sum(int(v) for (candidate, _), v in scheme_equal.items() if candidate == i),
            )
            for i in range(len(provisional))
        ]
        if reference is None:
            reference = totals
        elif totals != reference:
            raise SequentialExtensionError("plateau totals differ across bin schemes")
    assert reference is not None
    completed: list[dict[str, int]] = []
    for row, (n_value, m_value) in zip(provisional, reference, strict=True):
        if not n_value >= m_value >= 1:
            raise SequentialExtensionError("P013 plateau violates N>=M>=1")
        completed.append({**row, "N": n_value, "M": m_value, "C": m_value - 1})
    return completed


def validate_inputs(
    records_path: Path,
    p012_contract_path: Path,
    p013_contract_path: Path,
    p012b_manifest_path: Path,
    p012b_saved_report_path: Path,
    *,
    stage: str,
    segment_span: int = DEFAULT_SEGMENT_SPAN,
) -> dict[str, object]:
    config = _stage(stage)
    _validate_prerequisites(
        records_path,
        p012_contract_path,
        p013_contract_path,
        p012b_manifest_path,
        p012b_saved_report_path,
    )
    if not 1_000_000 <= segment_span <= 200_000_000:
        raise SequentialExtensionError("segment span is outside reviewed range")
    selected = select_complete_plateaus(load_record_references(records_path), config)
    return {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "stage": config.name,
        "range": f"[{config.lower_inclusive},{config.upper_exclusive})",
        "expected_gap_start_count": config.expected_gap_start_count,
        "selected_record_indices": [row["record_index"] for row in selected],
        "replications": DEFAULT_REPLICATIONS,
        "seed": config.seed,
        "bonferroni_alpha": 0.025,
        "p013_contract_sha256": P013_CONTRACT_SHA256,
        "extension_prime_stream_read": False,
        "actual_experiment_executed": False,
    }


def compute_extension_analysis(
    records_path: Path,
    p012_contract_path: Path,
    p013_contract_path: Path,
    p012b_manifest_path: Path,
    p012b_saved_report_path: Path,
    *,
    stage: str,
    segment_span: int = DEFAULT_SEGMENT_SPAN,
    replications: int = DEFAULT_REPLICATIONS,
    seed: int | None = None,
    prime_chunks: Iterable[Sequence[int] | np.ndarray] | None = None,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    config = _stage(stage)
    contract = _validate_prerequisites(
        records_path,
        p012_contract_path,
        p013_contract_path,
        p012b_manifest_path,
        p012b_saved_report_path,
    )
    selected_seed = config.seed if seed is None else seed
    if replications != DEFAULT_REPLICATIONS or selected_seed != config.seed:
        raise SequentialExtensionError("P013 replications/seed differ from contract")
    provisional = select_complete_plateaus(load_record_references(records_path), config)
    chunks = (
        prime_chunks
        if prime_chunks is not None
        else iter_prime_chunks_range(
            config.lower_inclusive,
            config.upper_exclusive,
            segment_span=segment_span,
        )
    )

    def monitored_chunks() -> Iterable[Sequence[int] | np.ndarray]:
        emitted = 0
        for index, chunk in enumerate(chunks, start=1):
            values = np.asarray(chunk, dtype=np.int64)
            emitted += int(values.size)
            if progress_callback is not None and (index == 1 or index % 100 == 0):
                progress_callback(
                    {
                        "stage": config.name,
                        "sieve_chunks_completed": index,
                        "primes_emitted_including_possible_boundary": emitted,
                        "last_prime": str(int(values[-1])),
                    }
                )
            yield values

    accumulated = accumulate_bin_counts(monitored_chunks(), provisional)
    if int(accumulated["gap_count"]) != config.expected_gap_start_count:
        raise SequentialExtensionError("gap-start count differs from exact pi difference")
    if int(accumulated["prime_count"]) != config.expected_gap_start_count + 1:
        raise SequentialExtensionError("prime stream lacks one right-boundary prime")
    populations = accumulated["populations"]
    if not isinstance(populations, dict):
        raise SequentialExtensionError("population counts missing")
    for scheme in BIN_SCHEMES:
        values = populations.get(scheme.name)
        if not isinstance(values, dict) or sum(map(int, values.values())) != config.expected_gap_start_count:
            raise SequentialExtensionError(f"population mismatch: {scheme.name}")
    plateaus = _derive_plateau_counts(provisional, accumulated)
    components = build_components(plateaus, accumulated)
    inference = analyze_components(
        plateaus, components, {}, replications=replications, seed=selected_seed
    )
    return {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "experiment": EXPERIMENT,
        "stage": config.name,
        "gap_start_range": {
            "lower_inclusive": str(config.lower_inclusive),
            "upper_exclusive": str(config.upper_exclusive),
        },
        "gap_start_count": config.expected_gap_start_count,
        "prime_stream_count_including_boundary_prime": accumulated["prime_count"],
        "segment_span": segment_span,
        "replications": replications,
        "base_seed": selected_seed,
        "selected_record_indices": [row["record_index"] for row in plateaus],
        "left_censored_continuation_excluded": True,
        "right_censored_plateau_excluded": True,
        "plateaus": plateaus,
        "components": components,
        "rows": inference["rows"],
        "cohorts": inference["cohorts"],
        "primary_contract": contract["primary"],
        "secondary_contract": contract["secondary"],
        "low_information_rule": contract["low_information_rule"],
        "two_stage_bonferroni_alpha": 0.025,
        "forced_first_record_removed": True,
        "p012b_statistics_used_for_inference": False,
        "pooling_after_results_prohibited": True,
        "post_selection_acknowledged": True,
        "theorem_claimed": False,
        "limitations": [
            "within-bin exchangeability is a diagnostic assumption, not a theorem",
            "record-gap selection remains post-selection",
            "separate gap categories are simulated independently despite shared positions",
            "LOW_INFORMATION does not alter family membership",
            "P013 stages are separately reported and are not pooled after inspection",
        ],
    }


def _plot_extension(
    rows: Sequence[dict[str, object]], directory: Path, stage: str
) -> list[Path]:
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
        raise SequentialExtensionError("P013 primary figure cohort is empty")
    gaps = [int(row["gap"]) for row in primary]
    observed = [int(row["observed_recurrences"]) for row in primary]
    expected = [float(row["expected_recurrences"]) for row in primary]
    paths: list[Path] = []
    prefix = f"p013{stage.lower()}"

    figure, axis = plt.subplots(figsize=(9, 5.5))
    axis.plot(gaps, observed, "o-", label="observed recurrence")
    axis.plot(gaps, expected, "^--", label="frozen stratified expected")
    axis.set_xlabel("record gap")
    axis.set_ylabel("recurrence count")
    axis.set_title(f"P013-{stage}: prospective observed versus expected")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    for suffix in ("png", "pdf"):
        path = directory / f"{prefix}_expected.{suffix}"
        figure.savefig(path, dpi=180 if suffix == "png" else None)
        paths.append(path)
    plt.close(figure)

    x = np.arange(len(gaps))
    defined = [i for i, row in enumerate(primary) if row["standardized_residual_z"] is not None]
    undefined = [i for i, row in enumerate(primary) if row["standardized_residual_z"] is None]
    z_values = [float(primary[i]["standardized_residual_z"]) for i in defined]
    figure, axis = plt.subplots(figsize=(9, 5.5))
    axis.axhline(0.0, color="black", linewidth=0.8)
    axis.bar(x[defined], z_values, width=0.6, color="tab:orange", label="stratified z")
    if undefined:
        axis.scatter(
            x[undefined], np.zeros(len(undefined)), marker="x", s=58,
            linewidths=1.7, color="tab:orange",
            label="z undefined (variance=0; not z=0)", zorder=3,
        )
    axis.set_xticks(x, [str(gap) for gap in gaps], rotation=45)
    axis.set_xlabel("record gap")
    axis.set_ylabel("standardized residual z")
    axis.set_title(f"P013-{stage}: prospective stratified residuals")
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    for suffix in ("png", "pdf"):
        path = directory / f"{prefix}_residuals.{suffix}"
        figure.savefig(path, dpi=180 if suffix == "png" else None)
        paths.append(path)
    plt.close(figure)
    return paths


def run_extension(
    records_path: Path,
    p012_contract_path: Path,
    p013_contract_path: Path,
    p012b_manifest_path: Path,
    p012b_saved_report_path: Path,
    output_directory: Path,
    *,
    stage: str,
    approval_token: str | None,
    segment_span: int = DEFAULT_SEGMENT_SPAN,
    make_plots: bool = True,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    config = _stage(stage)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P013 result: {output_directory}")
    started = time.perf_counter()
    analysis = compute_extension_analysis(
        records_path,
        p012_contract_path,
        p013_contract_path,
        p012b_manifest_path,
        p012b_saved_report_path,
        stage=config.name,
        segment_span=segment_span,
        progress_callback=progress_callback,
    )
    output_directory.mkdir(parents=True)
    inputs = {
        "input_validated_records.csv": records_path,
        "input_p012_contract.json": p012_contract_path,
        "input_p013_contract.json": p013_contract_path,
        "input_p012b_manifest.json": p012b_manifest_path,
        "input_p012b_saved_verification_report.json": p012b_saved_report_path,
    }
    for name, source in inputs.items():
        with (output_directory / name).open("xb") as handle:
            handle.write(source.read_bytes())
    _write_json_exclusive(output_directory / "analysis.json", analysis)
    _write_csv_exclusive(output_directory / "plateaus.csv", _serializable_rows(analysis["plateaus"]))
    _write_csv_exclusive(output_directory / "bin_components.csv", _serializable_rows(analysis["components"]))
    _write_csv_exclusive(output_directory / "plateau_statistics.csv", _serializable_rows(analysis["rows"]))
    _write_json_exclusive(output_directory / "cohort_summary.json", {"cohorts": analysis["cohorts"]})
    figures = _plot_extension(analysis["rows"], output_directory / "figures", config.name) if make_plots else []
    summary = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "stage": config.name,
        "gap_start_range": analysis["gap_start_range"],
        "gap_start_count": config.expected_gap_start_count,
        "selected_record_indices": analysis["selected_record_indices"],
        "modeled_rows": len(analysis["rows"]),
        "component_rows": len(analysis["components"]),
        "low_information_rows": sum(row["information_flag"] == "LOW_INFORMATION" for row in analysis["rows"]),
        "replications": DEFAULT_REPLICATIONS,
        "base_seed": config.seed,
        "two_stage_bonferroni_alpha": 0.025,
        "elapsed_seconds": time.perf_counter() - started,
        "figure_count": len(figures),
        "p012b_statistics_used_for_inference": False,
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifacts = sorted(path for path in output_directory.rglob("*") if path.is_file())
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "stage": config.name,
        "input_sha256": {
            "validated_records": VALIDATED_RECORDS_SHA256,
            "p012_contract": P012_CONTRACT_SHA256,
            "p013_contract": P013_CONTRACT_SHA256,
            "p012b_manifest": P012B_MANIFEST_SHA256,
            "p012b_saved_report": P012B_SAVED_REPORT_SHA256,
        },
        "analysis_source_sha256": sha256_file(Path(__file__)),
        "artifacts_sha256": {
            path.relative_to(output_directory).as_posix(): sha256_file(path)
            for path in artifacts
        },
        "segment_span": segment_span,
        "replications": DEFAULT_REPLICATIONS,
        "base_seed": config.seed,
        "two_stage_bonferroni_alpha": 0.025,
        "pooling_after_results_prohibited": True,
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_extension(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest_path = output_directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        saved = json.loads((output_directory / "analysis.json").read_text(encoding="utf-8"))
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            raise SequentialExtensionError("manifest artifact hashes missing")
        for relative, expected in artifacts.items():
            path = output_directory / str(relative)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {relative}")
        if manifest.get("analysis_source_sha256") != sha256_file(Path(__file__)):
            issues.append("current P013 source hash differs from manifest")
        recomputed = compute_extension_analysis(
            output_directory / "input_validated_records.csv",
            output_directory / "input_p012_contract.json",
            output_directory / "input_p013_contract.json",
            output_directory / "input_p012b_manifest.json",
            output_directory / "input_p012b_saved_verification_report.json",
            stage=str(manifest["stage"]),
            segment_span=int(manifest["segment_span"]),
            replications=int(manifest["replications"]),
            seed=int(manifest["base_seed"]),
        )
        if recomputed != saved:
            issues.append("saved P013 analysis differs from full recomputation")
    except Exception as exc:
        issues.append(f"saved P013 verification failed: {type(exc).__name__}: {exc}")
    manifest_path = output_directory / "manifest.json"
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "deterministic_full_recomputation": "PASS" if not issues else "FAIL",
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        if manifest_path.is_file()
        else None,
        "theorem_claimed": False,
    }


__all__ = [
    "DEFAULT_SEGMENT_SPAN",
    "EXPERIMENT",
    "P013_CONTRACT_SHA256",
    "STAGES",
    "SequentialExtensionError",
    "StageConfig",
    "compute_extension_analysis",
    "run_extension",
    "select_complete_plateaus",
    "validate_inputs",
    "verify_saved_extension",
]
