"""Read-only expected-information and screening-power diagnostics for P013.

The Poisson calculations in this module are planning proxies.  They do not
replace the frozen stratified-hypergeometric family test used by P012/P013 and
must never be reported as achieved statistical power for a future range.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable

from scipy.stats import poisson
from scipy.optimize import brentq

from source.provenance import sha256_file


PRIMARY_SCHEME = "primary_width_0p5_shift_0"
PRIMARY_COHORT = "primary_start_ge_1000"
DEFAULT_ALPHA = 0.025
DEFAULT_INFORMATION_EVENT_PROBABILITY = 0.5
DEFAULT_MIN_POSITIVE_VARIANCE_ROWS = 3
DEFAULT_MAX_LOW_INFORMATION_FRACTION = 0.5
DEFAULT_SCREENING_EFFECT_MULTIPLIER = 2.0
DEFAULT_SCREENING_POWER = 0.8


class RecurrenceInformationError(RuntimeError):
    """Raised when a saved recurrence result does not satisfy its provenance contract."""


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RecurrenceInformationError(f"JSON object required: {path}")
    return payload


def _require_saved_result(result_directory: Path) -> tuple[dict[str, object], dict[str, object]]:
    manifest_path = result_directory / "manifest.json"
    saved_path = result_directory / "saved_verification_report.json"
    manifest = _read_json(manifest_path)
    saved = _read_json(saved_path)
    if manifest.get("status") != "PASS" or saved.get("status") != "PASS":
        raise RecurrenceInformationError("input terminal/saved verification is not PASS")
    issues = saved.get("issues", [])
    if issues not in ([], None):
        raise RecurrenceInformationError("input saved verification contains issues")
    saved_manifest_hash = saved.get("manifest_sha256")
    if saved_manifest_hash is not None and saved_manifest_hash != sha256_file(manifest_path):
        raise RecurrenceInformationError("saved verification manifest hash mismatch")
    artifacts = manifest.get("artifacts_sha256")
    if not isinstance(artifacts, dict):
        raise RecurrenceInformationError("input manifest artifact hashes are missing")
    for name in ("summary.json", "cohort_summary.json", "plateau_statistics.csv"):
        expected = artifacts.get(name)
        path = result_directory / name
        if not isinstance(expected, str) or not path.is_file() or sha256_file(path) != expected:
            raise RecurrenceInformationError(f"input artifact hash mismatch: {name}")
    return manifest, saved


def load_stage_information(result_directory: Path, *, label: str) -> dict[str, object]:
    """Load one immutable P012/P013 result and extract primary information metrics."""

    manifest, _ = _require_saved_result(result_directory)
    summary = _read_json(result_directory / "summary.json")
    cohorts = _read_json(result_directory / "cohort_summary.json").get("cohorts")
    if not isinstance(cohorts, list):
        raise RecurrenceInformationError("cohort summary rows are missing")
    matching = [
        row
        for row in cohorts
        if isinstance(row, dict)
        and row.get("scheme") == PRIMARY_SCHEME
        and row.get("cohort") == PRIMARY_COHORT
    ]
    if len(matching) != 1:
        raise RecurrenceInformationError("exactly one primary cohort row is required")
    primary = matching[0]
    expected = float(primary["expected_total_recurrences"])
    observed = int(primary["observed_total_recurrences"])
    if not math.isfinite(expected) or expected < 0 or observed < 0:
        raise RecurrenceInformationError("invalid recurrence expectation or observation")

    primary_rows = 0
    positive_variance_rows = 0
    low_information_rows = 0
    total_variance = 0.0
    with (result_directory / "plateau_statistics.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        for row in csv.DictReader(handle):
            if row.get("scheme") != PRIMARY_SCHEME:
                continue
            cohorts_field = set(filter(None, str(row.get("cohorts", "")).split(";")))
            if PRIMARY_COHORT not in cohorts_field:
                continue
            primary_rows += 1
            variance = float(row["variance"])
            if not math.isfinite(variance) or variance < 0:
                raise RecurrenceInformationError("invalid primary-row variance")
            total_variance += variance
            if variance > 0:
                positive_variance_rows += 1
            if row.get("information_flag") == "LOW_INFORMATION":
                low_information_rows += 1
    if primary_rows < 1:
        raise RecurrenceInformationError("primary plateau statistics are empty")

    return {
        "label": label,
        "result_directory": str(result_directory),
        "manifest_sha256": sha256_file(result_directory / "manifest.json"),
        "experiment": manifest.get("experiment"),
        "stage": manifest.get("stage"),
        "range": summary.get("gap_start_range", summary.get("holdout_range")),
        "gap_start_count": summary.get("gap_start_count", summary.get("holdout_gap_start_count")),
        "primary_expected_recurrences": expected,
        "primary_observed_recurrences": observed,
        "primary_cohort_modeled_rows": int(primary["row_count"]),
        "primary_plateau_rows": primary_rows,
        "primary_positive_variance_rows": positive_variance_rows,
        "primary_low_information_rows": low_information_rows,
        "primary_low_information_fraction": low_information_rows / primary_rows,
        "primary_total_variance": total_variance,
    }


def poisson_screening_metrics(
    expected_recurrences: float,
    *,
    alpha: float = DEFAULT_ALPHA,
    effect_multipliers: Iterable[float] = (1.5, 2.0, 3.0, 5.0, 10.0),
) -> dict[str, object]:
    """Return a count-only Poisson screen, explicitly not the project family test."""

    if not math.isfinite(expected_recurrences) or expected_recurrences <= 0:
        raise ValueError("expected_recurrences must be finite and positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0,1)")
    critical_count = 0
    while float(poisson.sf(critical_count - 1, expected_recurrences)) > alpha:
        critical_count += 1
    powers: dict[str, float] = {}
    for multiplier in effect_multipliers:
        multiplier = float(multiplier)
        if not math.isfinite(multiplier) or multiplier <= 1:
            raise ValueError("effect multipliers must be finite and greater than one")
        powers[f"{multiplier:g}x"] = float(
            poisson.sf(critical_count - 1, multiplier * expected_recurrences)
        )
    return {
        "model": "poisson_count_screening_proxy",
        "alpha": alpha,
        "null_expected_recurrences": expected_recurrences,
        "null_probability_at_least_one": -math.expm1(-expected_recurrences),
        "critical_count": critical_count,
        "screening_power_by_effect_multiplier": powers,
        "is_actual_stratified_hypergeometric_family_power": False,
    }


def _poisson_mean_for_tail(
    critical_count: int,
    tail_probability: float,
    *,
    mean_multiplier: float,
) -> float:
    if critical_count < 1:
        raise ValueError("critical_count must be positive")
    if not 0 < tail_probability < 1:
        raise ValueError("tail_probability must be in (0,1)")
    if not math.isfinite(mean_multiplier) or mean_multiplier <= 0:
        raise ValueError("mean_multiplier must be finite and positive")
    upper = 1.0
    while float(
        poisson.sf(critical_count - 1, mean_multiplier * upper)
    ) < tail_probability:
        upper *= 2.0
        if upper > 1e12:
            raise ValueError("Poisson planning root exceeded reviewed range")
    return float(
        brentq(
            lambda mean: float(
                poisson.sf(critical_count - 1, mean_multiplier * mean)
            )
            - tail_probability,
            0.0,
            upper,
        )
    )


def minimum_poisson_null_expectation_for_power(
    *,
    alpha: float,
    effect_multiplier: float,
    power_target: float,
    maximum_critical_count: int = 10_000,
) -> dict[str, object]:
    """Find the first exact Poisson rejection interval reaching target power."""

    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0,1)")
    if not math.isfinite(effect_multiplier) or effect_multiplier <= 1:
        raise ValueError("effect_multiplier must be finite and greater than one")
    if not 0 < power_target < 1:
        raise ValueError("power_target must be in (0,1)")
    if maximum_critical_count < 1:
        raise ValueError("maximum_critical_count must be positive")

    previous_null_upper = 0.0
    for critical_count in range(1, maximum_critical_count + 1):
        null_upper = _poisson_mean_for_tail(
            critical_count,
            alpha,
            mean_multiplier=1.0,
        )
        power_lower = _poisson_mean_for_tail(
            critical_count,
            power_target,
            mean_multiplier=effect_multiplier,
        )
        candidate = max(
            power_lower,
            math.nextafter(previous_null_upper, math.inf),
        )
        if candidate <= null_upper:
            achieved = float(
                poisson.sf(
                    critical_count - 1,
                    effect_multiplier * candidate,
                )
            )
            return {
                "minimum_null_expected_recurrences": candidate,
                "critical_count": critical_count,
                "achieved_power": achieved,
                "alpha": alpha,
                "effect_multiplier": effect_multiplier,
                "power_target": power_target,
                "is_formal_stratified_hypergeometric_power": False,
            }
        previous_null_upper = null_upper
    raise ValueError("power target was not reached within critical-count limit")


def evaluate_stage(
    stage: dict[str, object],
    *,
    alpha: float = DEFAULT_ALPHA,
    information_event_probability: float = DEFAULT_INFORMATION_EVENT_PROBABILITY,
    minimum_positive_variance_rows: int = DEFAULT_MIN_POSITIVE_VARIANCE_ROWS,
    maximum_low_information_fraction: float = DEFAULT_MAX_LOW_INFORMATION_FRACTION,
    screening_effect_multiplier: float = DEFAULT_SCREENING_EFFECT_MULTIPLIER,
    screening_power_target: float = DEFAULT_SCREENING_POWER,
) -> dict[str, object]:
    expected = float(stage["primary_expected_recurrences"])
    if expected <= 0:
        raise RecurrenceInformationError("positive primary expectation is required for planning")
    if not 0 < information_event_probability < 1:
        raise ValueError("information_event_probability must be in (0,1)")
    proxy_effects = tuple(
        sorted({1.5, 2.0, 3.0, 5.0, 10.0, float(screening_effect_multiplier)})
    )
    proxy = poisson_screening_metrics(
        expected,
        alpha=alpha,
        effect_multipliers=proxy_effects,
    )
    target_expected = -math.log1p(-information_event_probability)
    information_multiplier = target_expected / expected
    power_key = f"{float(screening_effect_multiplier):g}x"
    proxy_power = float(proxy["screening_power_by_effect_multiplier"][power_key])
    power_requirement = minimum_poisson_null_expectation_for_power(
        alpha=alpha,
        effect_multiplier=screening_effect_multiplier,
        power_target=screening_power_target,
    )
    required_power_expectation = float(
        power_requirement["minimum_null_expected_recurrences"]
    )
    information_gate = (
        expected >= target_expected
        and int(stage["primary_positive_variance_rows"]) >= minimum_positive_variance_rows
        and float(stage["primary_low_information_fraction"])
        <= maximum_low_information_fraction
    )
    proxy_power_gate = proxy_power >= screening_power_target
    return {
        **stage,
        "planning_thresholds": {
            "information_event_probability": information_event_probability,
            "target_expected_recurrences": target_expected,
            "minimum_positive_variance_rows": minimum_positive_variance_rows,
            "maximum_low_information_fraction": maximum_low_information_fraction,
            "screening_effect_multiplier": screening_effect_multiplier,
            "screening_power_target": screening_power_target,
        },
        "expected_information_multipliers": {
            "to_event_probability_target": information_multiplier,
            "to_expected_1": 1.0 / expected,
            "to_expected_3": 3.0 / expected,
            "to_expected_5": 5.0 / expected,
            "to_poisson_screening_power_target": required_power_expectation
            / expected,
        },
        "poisson_screening_power_requirement": power_requirement,
        "poisson_screen": proxy,
        "information_gate_pass": information_gate,
        "poisson_screening_power_gate_pass": proxy_power_gate,
        "automatic_next_range_promotion": information_gate and proxy_power_gate,
        "formal_power_certified": False,
    }


def build_preflight_report(
    stages: Iterable[dict[str, object]],
    *,
    decision_stage_label: str,
) -> dict[str, object]:
    evaluated = [evaluate_stage(stage) for stage in stages]
    decision_rows = [row for row in evaluated if row["label"] == decision_stage_label]
    if len(decision_rows) != 1:
        raise RecurrenceInformationError("exactly one decision stage is required")
    decision = decision_rows[0]
    promote = bool(decision["automatic_next_range_promotion"])
    return {
        "status": "PASS",
        "experiment": "P018_P013_EXPECTED_INFORMATION_POWER_PREFLIGHT",
        "stages": evaluated,
        "decision_stage_label": decision_stage_label,
        "recommendation": "PROMOTE_NEXT_RANGE" if promote else "HOLD_NEXT_RANGE",
        "formal_power_certified": False,
        "poisson_screen_is_planning_proxy_only": True,
        "exact_future_hypergeometric_power_requires_preregistered_future_design": True,
        "theorem_claimed": False,
    }


__all__ = [
    "RecurrenceInformationError",
    "build_preflight_report",
    "evaluate_stage",
    "load_stage_information",
    "minimum_poisson_null_expectation_for_power",
    "poisson_screening_metrics",
]
