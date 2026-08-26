"""P011 diagnostic null model for P006 maximal-gap recurrence counts.

This is deliberately an empirical diagnostic, not a theorem about prime gaps.
For each completed record plateau, the post-record recurrence count is compared
with a binomial reference whose gap probability is estimated outside that same
plateau.  Selection, nonstationarity, and dependence remain explicit limits.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

from source.provenance import require_experiment_approval, sha256_file


COMPLETE_PLATEAUS_SHA256 = (
    "4675e8b6e7284b31c61ad66f3f98ffa34114553d49ab32878c609608530daca6"
)
GAP_HISTOGRAM_SHA256 = (
    "ef68d47588b492a5747ff54a58634be5d5c4a339a0599bf5273dd43949ed9ecb"
)
SCHEMA_VERSION = "p011-recurrence-null-v1"
EXPERIMENT = "P011_P006_RECURRENCE_NULL_MODEL"
DEFAULT_SEED = 20260826
DEFAULT_REPLICATIONS = 20_000


class RecurrenceNullError(ValueError):
    """Raised when the saved P006 inputs do not satisfy the null contract."""


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _load_inputs(
    complete_plateaus_path: Path,
    gap_histogram_path: Path,
) -> tuple[list[dict[str, int]], dict[int, int], int]:
    if sha256_file(complete_plateaus_path) != COMPLETE_PLATEAUS_SHA256:
        raise RecurrenceNullError("P006 complete-plateau input hash mismatch")
    if sha256_file(gap_histogram_path) != GAP_HISTOGRAM_SHA256:
        raise RecurrenceNullError("P006 gap-histogram input hash mismatch")
    with complete_plateaus_path.open("r", encoding="utf-8", newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    with gap_histogram_path.open("r", encoding="utf-8", newline="") as handle:
        histogram = {int(row["gap"]): int(row["count"]) for row in csv.DictReader(handle)}
    rows: list[dict[str, int]] = []
    for raw in raw_rows:
        row = {
            "record_index": int(raw["record_index"]),
            "start_prime": int(raw["start_prime"]),
            "gap": int(raw["gap"]),
            "N": int(raw["N"]),
            "M": int(raw["M"]),
            "C": int(raw["C"]),
        }
        if not (row["N"] >= row["M"] >= 1 and row["C"] == row["M"] - 1):
            raise RecurrenceNullError("P006 N/M/C invariant failed")
        if histogram.get(row["gap"], 0) < row["M"]:
            raise RecurrenceNullError("global histogram count is smaller than plateau count")
        rows.append(row)
    if not rows:
        raise RecurrenceNullError("P006 complete-plateau table is empty")
    total_gaps = sum(histogram.values())
    return rows, histogram, total_gaps


def validate_inputs(
    complete_plateaus_path: Path,
    gap_histogram_path: Path,
) -> dict[str, object]:
    rows, histogram, total_gaps = _load_inputs(
        complete_plateaus_path, gap_histogram_path
    )
    return {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "complete_plateau_count": len(rows),
        "distinct_gap_count": len(histogram),
        "total_gap_count": total_gaps,
        "gap_one_excluded_from_model": True,
        "experiment_executed": False,
    }


def _bh_adjust(p_values: list[float]) -> list[float]:
    count = len(p_values)
    order = sorted(range(count), key=lambda index: (p_values[index], index))
    adjusted = [1.0] * count
    running = 1.0
    for rank_position in range(count - 1, -1, -1):
        index = order[rank_position]
        rank = rank_position + 1
        running = min(running, p_values[index] * count / rank)
        adjusted[index] = min(1.0, running)
    return adjusted


def _cohort_summary(
    rows: list[dict[str, object]],
    *,
    name: str,
    replications: int,
    seed: int,
) -> dict[str, object]:
    selected = [row for row in rows if name in row["cohorts"]]
    if not selected:
        return {"cohort": name, "row_count": 0, "status": "EMPTY"}
    trials = np.asarray([int(row["post_record_trials"]) for row in selected], dtype=np.int64)
    probabilities = np.asarray([float(row["p_leave_plateau_out"]) for row in selected])
    observed = np.asarray([int(row["observed_recurrences"]) for row in selected], dtype=np.int64)
    expected = trials * probabilities
    variances = trials * probabilities * (1.0 - probabilities)
    positive = variances > 0.0
    observed_z = np.zeros(len(selected), dtype=np.float64)
    observed_z[positive] = (observed[positive] - expected[positive]) / np.sqrt(variances[positive])

    rng = np.random.default_rng(seed)
    simulated = rng.binomial(trials, probabilities, size=(replications, len(selected)))
    total_observed = int(np.sum(observed))
    simulated_totals = np.sum(simulated, axis=1)
    p_total_upper = (int(np.count_nonzero(simulated_totals >= total_observed)) + 1) / (
        replications + 1
    )
    simulated_z = np.zeros_like(simulated, dtype=np.float64)
    simulated_z[:, positive] = (
        simulated[:, positive] - expected[positive]
    ) / np.sqrt(variances[positive])
    observed_max_abs_z = float(np.max(np.abs(observed_z)))
    simulated_max_abs_z = np.max(np.abs(simulated_z), axis=1)
    p_max_abs_z = (int(np.count_nonzero(simulated_max_abs_z >= observed_max_abs_z)) + 1) / (
        replications + 1
    )
    return {
        "status": "PASS",
        "cohort": name,
        "row_count": len(selected),
        "observed_total_recurrences": total_observed,
        "expected_total_recurrences": float(np.sum(expected)),
        "observed_max_absolute_z": observed_max_abs_z,
        "monte_carlo_total_upper_p": p_total_upper,
        "monte_carlo_max_absolute_z_p": p_max_abs_z,
        "replications": replications,
        "seed": seed,
        "independent_binomial_simulation_is_diagnostic_only": True,
    }


def compute_null_analysis(
    complete_plateaus_path: Path,
    gap_histogram_path: Path,
    *,
    replications: int = DEFAULT_REPLICATIONS,
    seed: int = DEFAULT_SEED,
) -> dict[str, object]:
    if replications < 1_000:
        raise RecurrenceNullError("at least 1,000 Monte Carlo replications are required")
    rows, histogram, total_gaps = _load_inputs(
        complete_plateaus_path, gap_histogram_path
    )
    modeled: list[dict[str, object]] = []
    for row in rows:
        gap = row["gap"]
        trials = row["N"] - 1
        if gap == 1 or trials < 1:
            continue
        outside_trials = total_gaps - row["N"]
        outside_equal = histogram[gap] - row["M"]
        if outside_trials <= 0 or not (0 <= outside_equal <= outside_trials):
            raise RecurrenceNullError("leave-plateau-out probability is invalid")
        probability = outside_equal / outside_trials
        observed = row["C"]
        expected = trials * probability
        variance = trials * probability * (1.0 - probability)
        z_score = None if variance == 0.0 else (observed - expected) / math.sqrt(variance)
        greater_p = float(binomtest(observed, trials, probability, alternative="greater").pvalue)
        two_sided_p = float(binomtest(observed, trials, probability).pvalue)
        cohorts = ["all_eligible"]
        if row["start_prime"] >= 1_000:
            cohorts.append("primary_start_ge_1000")
        if row["start_prime"] >= 100_000:
            cohorts.append("sensitivity_start_ge_100000")
        modeled.append(
            {
                **row,
                "post_record_trials": trials,
                "observed_recurrences": observed,
                "global_equal_gap_count": histogram[gap],
                "outside_gap_count": outside_trials,
                "outside_equal_gap_count": outside_equal,
                "p_leave_plateau_out": probability,
                "expected_recurrences": expected,
                "variance": variance,
                "standardized_residual_z": z_score,
                "exact_binomial_greater_p": greater_p,
                "exact_binomial_two_sided_p": two_sided_p,
                "cohorts": cohorts,
            }
        )
    q_values = _bh_adjust([float(row["exact_binomial_greater_p"]) for row in modeled])
    for row, q_value in zip(modeled, q_values):
        row["bh_q_greater_all_eligible"] = q_value

    cohort_names = (
        "primary_start_ge_1000",
        "all_eligible",
        "sensitivity_start_ge_100000",
    )
    cohorts = [
        _cohort_summary(
            modeled,
            name=name,
            replications=replications,
            seed=seed + index,
        )
        for index, name in enumerate(cohort_names)
    ]
    return {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "experiment": EXPERIMENT,
        "null_model": "leave-plateau-out stationary independent binomial diagnostic",
        "total_gap_count": total_gaps,
        "modeled_plateau_count": len(modeled),
        "replications": replications,
        "base_seed": seed,
        "rows": modeled,
        "cohorts": cohorts,
        "limitations": [
            "record-gap selection is post-selection and is not modeled",
            "prime gaps are neither independent nor stationary",
            "the outside-frequency estimate reuses the same finite dataset",
            "plateau-specific x dependence is not captured by one global frequency",
            "p-values are exploratory diagnostics and not theorem evidence",
        ],
    }


def _write_rows_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [name for name in rows[0].keys() if name != "cohorts"]
    fieldnames.append("cohorts")
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            payload = dict(row)
            payload["cohorts"] = ";".join(str(item) for item in row["cohorts"])
            writer.writerow(payload)


def _plot_diagnostics(rows: list[dict[str, object]], figure_directory: Path) -> list[Path]:
    import matplotlib.pyplot as plt

    figure_directory.mkdir(parents=True)
    gaps = [int(row["gap"]) for row in rows]
    observed = [int(row["observed_recurrences"]) for row in rows]
    expected = [float(row["expected_recurrences"]) for row in rows]
    z_values = [
        0.0 if row["standardized_residual_z"] is None else float(row["standardized_residual_z"])
        for row in rows
    ]
    paths: list[Path] = []

    figure, axis = plt.subplots(figsize=(10, 5.5))
    axis.plot(gaps, observed, "o-", label="observed recurrence C")
    axis.plot(gaps, expected, "s--", label="null expected (N-1)p")
    axis.set_xlabel("record gap")
    axis.set_ylabel("recurrence count")
    axis.set_title("P011 observed recurrence versus leave-plateau-out null")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    for suffix in ("png", "pdf"):
        path = figure_directory / f"p011_observed_vs_expected.{suffix}"
        figure.savefig(path, dpi=180 if suffix == "png" else None)
        paths.append(path)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(10, 5.5))
    axis.axhline(0.0, color="black", linewidth=0.8)
    axis.bar([str(gap) for gap in gaps], z_values)
    axis.set_xlabel("record gap")
    axis.set_ylabel("standardized residual z")
    axis.set_title("P011 recurrence residuals (diagnostic null)")
    axis.tick_params(axis="x", rotation=90)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    for suffix in ("png", "pdf"):
        path = figure_directory / f"p011_standardized_residuals.{suffix}"
        figure.savefig(path, dpi=180 if suffix == "png" else None)
        paths.append(path)
    plt.close(figure)
    return paths


def run_null_model(
    complete_plateaus_path: Path,
    gap_histogram_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    replications: int = DEFAULT_REPLICATIONS,
    seed: int = DEFAULT_SEED,
    make_plots: bool = True,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P011 result: {output_directory}")
    analysis = compute_null_analysis(
        complete_plateaus_path,
        gap_histogram_path,
        replications=replications,
        seed=seed,
    )
    output_directory.mkdir(parents=True)
    with (output_directory / "input_complete_plateaus.csv").open("xb") as handle:
        handle.write(complete_plateaus_path.read_bytes())
    with (output_directory / "input_gap_histogram.csv").open("xb") as handle:
        handle.write(gap_histogram_path.read_bytes())
    _write_json_exclusive(output_directory / "analysis.json", analysis)
    _write_rows_csv(output_directory / "plateau_null_statistics.csv", analysis["rows"])
    _write_json_exclusive(
        output_directory / "cohort_summary.json", {"cohorts": analysis["cohorts"]}
    )
    figure_paths = (
        _plot_diagnostics(analysis["rows"], output_directory / "figures")
        if make_plots
        else []
    )
    artifact_paths = [
        output_directory / "input_complete_plateaus.csv",
        output_directory / "input_gap_histogram.csv",
        output_directory / "analysis.json",
        output_directory / "plateau_null_statistics.csv",
        output_directory / "cohort_summary.json",
        *figure_paths,
    ]
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "input_sha256": {
            "complete_plateaus": COMPLETE_PLATEAUS_SHA256,
            "gap_histogram": GAP_HISTOGRAM_SHA256,
        },
        "artifacts_sha256": {
            path.relative_to(output_directory).as_posix(): sha256_file(path)
            for path in artifact_paths
        },
        "replications": replications,
        "base_seed": seed,
        "figure_count": len(figure_paths),
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "modeled_plateau_count": analysis["modeled_plateau_count"],
        "cohorts": analysis["cohorts"],
        "figure_count": len(figure_paths),
        "theorem_claimed": False,
    }


def verify_saved_null_model(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest = json.loads((output_directory / "manifest.json").read_text("utf-8"))
        saved_analysis = json.loads((output_directory / "analysis.json").read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "issues": [f"saved result read failed: {exc}"]}
    if manifest.get("experiment") != EXPERIMENT:
        issues.append("unexpected experiment label")
    artifacts = manifest.get("artifacts_sha256")
    if not isinstance(artifacts, dict):
        issues.append("manifest lacks artifact hashes")
        artifacts = {}
    for relative, expected in artifacts.items():
        path = output_directory / str(relative)
        if not path.is_file() or sha256_file(path) != str(expected):
            issues.append(f"artifact missing/hash mismatch: {relative}")
    try:
        recomputed = compute_null_analysis(
            output_directory / "input_complete_plateaus.csv",
            output_directory / "input_gap_histogram.csv",
            replications=int(manifest["replications"]),
            seed=int(manifest["base_seed"]),
        )
        if recomputed != saved_analysis:
            issues.append("saved analysis differs from deterministic recomputation")
    except (KeyError, OSError, ValueError, RecurrenceNullError) as exc:
        issues.append(f"deterministic recomputation failed: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "deterministic_recomputation": "PASS" if not issues else "FAIL",
        "theorem_claimed": False,
    }


__all__ = [
    "COMPLETE_PLATEAUS_SHA256",
    "DEFAULT_REPLICATIONS",
    "DEFAULT_SEED",
    "EXPERIMENT",
    "GAP_HISTOGRAM_SHA256",
    "RecurrenceNullError",
    "compute_null_analysis",
    "run_null_model",
    "validate_inputs",
    "verify_saved_null_model",
]
