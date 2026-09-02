"""P020 synthesis of persisted recurrence artifacts without a new prime sweep."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


SCHEMA_VERSION = "p020-recurrence-artifact-synthesis-v1"
EXPERIMENT = "P020_RECURRENCE_ARTIFACT_SYNTHESIS"
RUNNER_REVISION = "R2_VISUAL_LAYOUT"
PRIMARY_SCHEME = "primary_width_0p5_shift_0"
PRIMARY_COHORT = "primary_start_ge_1000"
EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")

TABLE_FIELDS: dict[str, tuple[str, ...]] = {
    "coverage_ranges": (
        "stage",
        "role",
        "lower_inclusive",
        "upper_exclusive",
        "log10_lower",
        "log10_upper",
        "reported_gap_start_count",
        "unique_accounting_count",
        "plateau_rows",
        "coverage_note",
    ),
    "p006_descriptive_recurrence": (
        "record_index",
        "start_prime",
        "gap",
        "N",
        "M",
        "C",
        "Q_M_over_N",
        "R_C_over_N_minus_1",
    ),
    "null_model_correction": (
        "record_index",
        "start_prime",
        "gap",
        "observed_recurrences",
        "p011_stationary_expected",
        "p012_stratified_expected",
        "relative_expected_reduction",
    ),
    "prospective_stage_summary": (
        "stage",
        "role",
        "lower_inclusive",
        "upper_exclusive",
        "gap_start_count",
        "primary_plateau_rows",
        "primary_positive_variance_rows",
        "primary_observed_recurrences",
        "primary_expected_recurrences",
        "expected_per_billion_gap_starts",
    ),
    "information_collapse": (
        "stage",
        "role",
        "gap_start_count",
        "primary_plateau_rows",
        "positive_variance_rows",
        "positive_variance_fraction",
        "low_information_rows",
        "low_information_fraction",
        "primary_expected_recurrences",
        "expected_per_billion_gap_starts",
        "hypothesis_test_performed",
    ),
    "p018_forced_record_funnel": (
        "record_index",
        "gap",
        "population_before_removal",
        "plateau_exposure_after_removal",
        "control_exposure",
        "target_gap_count_before_removal",
        "forced_record_removed",
        "conditioned_gap_count_after_removal",
        "expected_component",
        "variance_component",
        "information_flag",
        "gate_recommendation",
    ),
}


class SynthesisError(RuntimeError):
    """Raised when the frozen P020 contract or a persisted input is violated."""


@dataclass(frozen=True)
class SynthesisData:
    tables: dict[str, list[dict[str, object]]]
    summary: dict[str, object]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_object(path: Path) -> dict[str, object]:
    value = _read_json(path)
    if not isinstance(value, dict):
        raise SynthesisError(f"expected JSON object: {path}")
    return value


def _read_json_list(path: Path) -> list[dict[str, object]]:
    value = _read_json(path)
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise SynthesisError(f"expected JSON object list: {path}")
    return [dict(row) for row in value]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _json_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _csv_text(rows: Sequence[Mapping[str, object]], fields: Sequence[str]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(fields), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buffer.getvalue()


def _write_text_exclusive(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _write_json_exclusive(path: Path, payload: object) -> None:
    _write_text_exclusive(path, _json_text(payload))


def _as_int(value: object, label: str) -> int:
    if isinstance(value, bool):
        raise SynthesisError(f"boolean is not an integer for {label}")
    try:
        return int(str(value))
    except (TypeError, ValueError) as exc:
        raise SynthesisError(f"invalid integer for {label}: {value!r}") from exc


def _as_float(value: object, label: str) -> float:
    try:
        result = float(str(value))
    except (TypeError, ValueError) as exc:
        raise SynthesisError(f"invalid float for {label}: {value!r}") from exc
    if not math.isfinite(result):
        raise SynthesisError(f"non-finite float for {label}: {value!r}")
    return result


def _contains_cohort(row: Mapping[str, object], cohort: str) -> bool:
    return cohort in str(row.get("cohorts", "")).split(";")


def load_contract(path: Path) -> dict[str, object]:
    contract = _read_json_object(path)
    if contract.get("contract_version") != "p020-recurrence-artifact-synthesis-contract-v1":
        raise SynthesisError("unexpected P020 contract version")
    if contract.get("primary_scheme") != PRIMARY_SCHEME:
        raise SynthesisError("primary scheme differs from frozen P020 contract")
    if contract.get("primary_cohort") != PRIMARY_COHORT:
        raise SynthesisError("primary cohort differs from frozen P020 contract")
    input_runs = contract.get("input_runs")
    if not isinstance(input_runs, dict) or len(input_runs) != 8:
        raise SynthesisError("P020 contract must pin exactly eight input runs")
    return contract


def _input_roots(project_root: Path, contract: Mapping[str, object]) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    runs = contract["input_runs"]
    assert isinstance(runs, dict)
    for key, raw in runs.items():
        if not isinstance(raw, dict):
            raise SynthesisError(f"invalid input spec: {key}")
        relative = Path(str(raw.get("path", "")))
        root = (project_root / relative).resolve()
        try:
            root.relative_to(project_root.resolve())
        except ValueError as exc:
            raise SynthesisError(f"input path escapes project root: {relative}") from exc
        roots[str(key)] = root
    return roots


def _lightweight_saved_evidence_check(key: str, root: Path) -> dict[str, object]:
    """Hash persisted artifacts and inspect prior verification evidence.

    P012/P013 ``verify_saved_*`` functions intentionally repeat their prime-range
    analysis.  P020 is an artifact-only synthesis, so calling them would violate
    the no-new-prime-sweep contract.  This checker instead verifies every hash
    already committed by the input manifest and the saved verifier report emitted
    by the original authorized run.
    """

    issues: list[str] = []
    manifest_path = root / "manifest.json"
    manifest = _read_json_object(manifest_path)
    artifacts = manifest.get("artifacts_sha256", manifest.get("artifacts"))
    if not isinstance(artifacts, dict):
        issues.append("manifest artifact hash table missing")
        artifacts = {}
    for relative, expected in artifacts.items():
        path = root / str(relative)
        if not path.is_file():
            issues.append(f"missing artifact: {relative}")
        elif sha256_file(path) != str(expected):
            issues.append(f"artifact SHA-256 mismatch: {relative}")

    evidence_kind = "manifest_hashes"
    if key == "p006_full":
        report = _read_json_object(root / "verification_report.json")
        if report.get("status") != "PASS" or report.get("issues") not in ([], None):
            issues.append("P006 saved verification report is not clean PASS")
        evidence_kind = "manifest_hashes_and_saved_verification_report"
    elif key == "p011":
        analysis = _read_json_object(root / "analysis.json")
        if analysis.get("status") != "PASS":
            issues.append("P011 saved analysis status is not PASS")
        evidence_kind = "manifest_hashes_and_saved_analysis_status"
    else:
        report_path = root / "saved_verification_report.json"
        report = _read_json_object(report_path)
        if report.get("status") != "PASS" or report.get("issues") not in ([], None):
            issues.append(f"{key} saved verification evidence is not clean PASS")
        reported_manifest = report.get("manifest_sha256")
        actual_manifest = sha256_file(manifest_path)
        if reported_manifest is not None and reported_manifest != actual_manifest:
            issues.append(f"{key} saved verifier references a different manifest")
        if key.startswith("p018"):
            if report.get("full_prime_range_recomputed") is not False:
                issues.append(f"{key} saved verifier evidence has unexpected prime-sweep flag")
            if report.get("hypothesis_test_performed") is not False:
                issues.append(f"{key} saved verifier evidence has unexpected hypothesis-test flag")
        evidence_kind = "manifest_hashes_and_prior_saved_verifier_evidence"
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "artifact_hash_count": len(artifacts),
        "verification_mode": evidence_kind,
        "new_prime_sweep_performed": False,
    }


def verify_inputs(project_root: Path, contract_path: Path) -> dict[str, object]:
    project_root = project_root.resolve()
    contract_path = contract_path.resolve()
    contract = load_contract(contract_path)
    roots = _input_roots(project_root, contract)
    issues: list[str] = []
    rows: list[dict[str, object]] = []
    runs = contract["input_runs"]
    assert isinstance(runs, dict)
    for key in sorted(roots):
        root = roots[key]
        spec = runs[key]
        assert isinstance(spec, dict)
        manifest = root / "manifest.json"
        expected_hash = str(spec.get("manifest_sha256", ""))
        actual_hash = sha256_file(manifest) if manifest.is_file() else "MISSING"
        if actual_hash != expected_hash:
            issues.append(f"{key}: manifest SHA-256 mismatch")
        verifier_status = "NOT_RUN"
        verifier_issues: object = []
        if root.is_dir() and actual_hash == expected_hash:
            try:
                report = _lightweight_saved_evidence_check(key, root)
                verifier_status = str(report.get("status", "MISSING"))
                verifier_issues = report.get("issues", [])
                if verifier_status != "PASS":
                    issues.append(f"{key}: saved verifier status {verifier_status}")
            except Exception as exc:  # audit boundary: preserve exact exception text
                verifier_status = "ERROR"
                verifier_issues = [f"{type(exc).__name__}: {exc}"]
                issues.append(f"{key}: saved verifier raised {type(exc).__name__}")
        rows.append(
            {
                "input_key": key,
                "project_relative_path": str(root.relative_to(project_root)).replace("\\", "/"),
                "role": str(spec.get("role", "")),
                "expected_manifest_sha256": expected_hash,
                "actual_manifest_sha256": actual_hash,
                "saved_verifier_status": verifier_status,
                "saved_verifier_issues": verifier_issues,
                "verification_mode": report.get("verification_mode", "NOT_RUN")
                if root.is_dir() and actual_hash == expected_hash
                else "NOT_RUN",
                "new_prime_sweep_performed": False,
            }
        )
    expected_executable = EXPECTED_PYTHON.resolve()
    actual_executable = Path(sys.executable).resolve()
    if actual_executable != expected_executable:
        issues.append(
            f"wrong Python executable: {actual_executable}; expected {expected_executable}"
        )
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "contract_sha256": sha256_file(contract_path),
        "python_executable": str(actual_executable),
        "new_prime_sweep_performed": False,
        "inputs": rows,
    }


def load_payloads(project_root: Path, contract: Mapping[str, object]) -> dict[str, dict[str, object]]:
    roots = _input_roots(project_root.resolve(), contract)
    p: dict[str, dict[str, object]] = {}
    p["p006_full"] = {
        "summary": _read_json_object(roots["p006_full"] / "summary.json"),
        "plateaus": _read_csv(roots["p006_full"] / "tables" / "complete_plateaus.csv"),
    }
    p["p011"] = {
        "analysis": _read_json_object(roots["p011"] / "analysis.json"),
        "statistics": _read_csv(roots["p011"] / "plateau_null_statistics.csv"),
    }
    for key in ("p012a_r2", "p012b", "p013a_r2", "p013b"):
        p[key] = {
            "summary": _read_json_object(roots[key] / "summary.json"),
            "cohorts": _read_json_object(roots[key] / "cohort_summary.json"),
            "statistics": _read_csv(roots[key] / "plateau_statistics.csv"),
        }
    for key in ("p018p0", "p018a"):
        p[key] = {
            "summary": _read_json_object(roots[key] / "summary.json"),
            "plateaus": _read_json_list(roots[key] / "plateaus.json"),
            "margin": _read_json_object(roots[key] / "blinded_margin_statistics.json"),
            "components": _read_json_list(
                roots[key] / "blinded_information_components.json"
            ),
            "gate": _read_json_object(roots[key] / "prefix_gate_report.json"),
        }
    return p


def _primary_rows(payload: Mapping[str, object]) -> list[dict[str, object]]:
    rows = payload.get("statistics")
    if not isinstance(rows, list):
        raise SynthesisError("statistics rows missing")
    selected = [
        dict(row)
        for row in rows
        if isinstance(row, dict)
        and row.get("scheme") == PRIMARY_SCHEME
        and _contains_cohort(row, PRIMARY_COHORT)
    ]
    return selected


def _primary_cohort(payload: Mapping[str, object]) -> dict[str, object]:
    root = payload.get("cohorts")
    if not isinstance(root, dict) or not isinstance(root.get("cohorts"), list):
        raise SynthesisError("cohort summary missing")
    matches = [
        dict(row)
        for row in root["cohorts"]
        if isinstance(row, dict)
        and row.get("scheme") == PRIMARY_SCHEME
        and row.get("cohort") == PRIMARY_COHORT
    ]
    if len(matches) != 1:
        raise SynthesisError(f"expected one primary cohort row, found {len(matches)}")
    return matches[0]


def _range_from_summary(summary: Mapping[str, object], key: str) -> tuple[int, int]:
    raw = summary.get(key)
    if not isinstance(raw, dict):
        raise SynthesisError(f"missing range object {key}")
    return _as_int(raw.get("lower_inclusive"), f"{key}.lower"), _as_int(
        raw.get("upper_exclusive"), f"{key}.upper"
    )


def _coverage_row(
    stage: str,
    role: str,
    lower: int,
    upper: int,
    reported_count: int,
    unique_count: int,
    plateau_rows: int,
    note: str,
) -> dict[str, object]:
    if not (0 < lower < upper):
        raise SynthesisError(f"invalid coverage range for {stage}")
    return {
        "stage": stage,
        "role": role,
        "lower_inclusive": lower,
        "upper_exclusive": upper,
        "log10_lower": math.log10(lower),
        "log10_upper": math.log10(upper),
        "reported_gap_start_count": reported_count,
        "unique_accounting_count": unique_count,
        "plateau_rows": plateau_rows,
        "coverage_note": note,
    }


def build_synthesis_data(
    payloads: Mapping[str, Mapping[str, object]], contract: Mapping[str, object]
) -> SynthesisData:
    p006_summary = payloads["p006_full"]["summary"]
    p006_plateaus = payloads["p006_full"]["plateaus"]
    assert isinstance(p006_summary, dict) and isinstance(p006_plateaus, list)
    p006_count = _as_int(p006_summary.get("gap_count"), "P006 gap_count")
    p006_limit = _as_int(p006_summary.get("analysis_limit"), "P006 analysis_limit")

    p012b_summary = payloads["p012b"]["summary"]
    p013a_summary = payloads["p013a_r2"]["summary"]
    p013b_summary = payloads["p013b"]["summary"]
    p018p0_summary = payloads["p018p0"]["summary"]
    p018a_summary = payloads["p018a"]["summary"]
    assert all(
        isinstance(item, dict)
        for item in (
            p012b_summary,
            p013a_summary,
            p013b_summary,
            p018p0_summary,
            p018a_summary,
        )
    )

    p012b_lower, p012b_upper = _range_from_summary(p012b_summary, "holdout_range")
    p013a_lower, p013a_upper = _range_from_summary(p013a_summary, "gap_start_range")
    p013b_lower, p013b_upper = _range_from_summary(p013b_summary, "gap_start_range")
    p018p0_lower, p018p0_upper = _range_from_summary(p018p0_summary, "range")
    p018a_lower, p018a_upper = _range_from_summary(p018a_summary, "range")
    p012b_count = _as_int(p012b_summary.get("holdout_gap_start_count"), "P012B count")
    p013a_count = _as_int(p013a_summary.get("gap_start_count"), "P013A count")
    p013b_count = _as_int(p013b_summary.get("gap_start_count"), "P013B count")
    p018p0_count = _as_int(p018p0_summary.get("exact_gap_start_count"), "P018P0 count")
    p018a_count = _as_int(p018a_summary.get("exact_gap_start_count"), "P018A count")

    coverage = [
        _coverage_row(
            "P006 full",
            "descriptive development",
            2,
            p006_limit,
            p006_count,
            p006_count,
            len(p006_plateaus),
            "unique sweep; one right-censored plateau excluded",
        ),
        _coverage_row(
            "P011",
            "stationary-null diagnostic",
            2,
            p006_limit,
            p006_count,
            0,
            len(payloads["p011"]["statistics"]),
            "reuses P006 aggregates",
        ),
        _coverage_row(
            "P012-A r2",
            "stratified development",
            2,
            p006_limit,
            p006_count,
            0,
            len(_primary_rows(payloads["p012a_r2"])),
            "reuses P006 gap stream; primary cohort rows shown",
        ),
        _coverage_row(
            "P012-B",
            "independent holdout",
            p012b_lower,
            p012b_upper,
            p012b_count,
            p012b_count,
            len(_primary_rows(payloads["p012b"])),
            "unique sweep",
        ),
        _coverage_row(
            "P013-A r2",
            "prospective",
            p013a_lower,
            p013a_upper,
            p013a_count,
            p013a_count,
            len(_primary_rows(payloads["p013a_r2"])),
            "unique sweep",
        ),
        _coverage_row(
            "P013-B",
            "prospective",
            p013b_lower,
            p013b_upper,
            p013b_count,
            p013b_count,
            len(_primary_rows(payloads["p013b"])),
            "unique sweep",
        ),
        _coverage_row(
            "P018-P0",
            "calibration margin-only",
            p018p0_lower,
            p018p0_upper,
            p018p0_count,
            0,
            len(payloads["p018p0"]["plateaus"]),
            "nested subset of P018-A; excluded from unique sum",
        ),
        _coverage_row(
            "P018-A",
            "prefix information margin-only",
            p018a_lower,
            p018a_upper,
            p018a_count,
            p018a_count,
            len(payloads["p018a"]["plateaus"]),
            "unique sweep; no hypothesis test",
        ),
    ]

    unique_total = sum(_as_int(row["unique_accounting_count"], "unique count") for row in coverage)
    accounting = contract.get("unique_processing_accounting")
    if not isinstance(accounting, dict):
        raise SynthesisError("missing unique processing contract")
    expected_total = _as_int(accounting.get("expected_gap_start_total"), "expected total")
    if unique_total != expected_total:
        raise SynthesisError(
            f"unique processing total mismatch: {unique_total} != {expected_total}"
        )

    p006_table: list[dict[str, object]] = []
    for row in p006_plateaus:
        if not isinstance(row, dict):
            raise SynthesisError("invalid P006 plateau row")
        p006_table.append({field: row.get(field, "") for field in TABLE_FIELDS["p006_descriptive_recurrence"]})

    p011_rows = payloads["p011"]["statistics"]
    assert isinstance(p011_rows, list)
    p011_by_index = {str(row["record_index"]): row for row in p011_rows if isinstance(row, dict)}
    correction: list[dict[str, object]] = []
    for row in _primary_rows(payloads["p012a_r2"]):
        key = str(row["record_index"])
        if key not in p011_by_index:
            raise SynthesisError(f"P011/P012 record mismatch: {key}")
        old = p011_by_index[key]
        observed = _as_int(row["observed_recurrences"], f"P012 observed {key}")
        if observed != _as_int(old["observed_recurrences"], f"P011 observed {key}"):
            raise SynthesisError(f"P011/P012 observed mismatch: {key}")
        p011_expected = _as_float(old["expected_recurrences"], f"P011 expected {key}")
        p012_expected = _as_float(row["expected_recurrences"], f"P012 expected {key}")
        correction.append(
            {
                "record_index": _as_int(row["record_index"], "record_index"),
                "start_prime": _as_int(row["start_prime"], "start_prime"),
                "gap": _as_int(row["gap"], "gap"),
                "observed_recurrences": observed,
                "p011_stationary_expected": p011_expected,
                "p012_stratified_expected": p012_expected,
                "relative_expected_reduction": (
                    1.0 - p012_expected / p011_expected if p011_expected else 0.0
                ),
            }
        )

    stage_specs = [
        ("P012-B", "holdout", "p012b", p012b_lower, p012b_upper, p012b_count),
        ("P013-A r2", "prospective", "p013a_r2", p013a_lower, p013a_upper, p013a_count),
        ("P013-B", "prospective", "p013b", p013b_lower, p013b_upper, p013b_count),
    ]
    prospective: list[dict[str, object]] = []
    for stage, role, key, lower, upper, count in stage_specs:
        rows = _primary_rows(payloads[key])
        cohort = _primary_cohort(payloads[key])
        expected = _as_float(cohort["expected_total_recurrences"], f"{stage} expected")
        observed = _as_int(cohort["observed_total_recurrences"], f"{stage} observed")
        prospective.append(
            {
                "stage": stage,
                "role": role,
                "lower_inclusive": lower,
                "upper_exclusive": upper,
                "gap_start_count": count,
                "primary_plateau_rows": len(rows),
                "primary_positive_variance_rows": sum(
                    _as_float(row["variance"], f"{stage} variance") > 0 for row in rows
                ),
                "primary_observed_recurrences": observed,
                "primary_expected_recurrences": expected,
                "expected_per_billion_gap_starts": expected * 1_000_000_000 / count,
            }
        )

    information: list[dict[str, object]] = []
    information_specs = [
        ("P012-A r2", "development", "p012a_r2", p006_count),
        ("P012-B", "holdout", "p012b", p012b_count),
        ("P013-A r2", "prospective", "p013a_r2", p013a_count),
        ("P013-B", "prospective", "p013b", p013b_count),
    ]
    for stage, role, key, count in information_specs:
        rows = _primary_rows(payloads[key])
        cohort = _primary_cohort(payloads[key])
        expected = _as_float(cohort["expected_total_recurrences"], f"{stage} expected")
        positive = sum(_as_float(row["variance"], f"{stage} variance") > 0 for row in rows)
        low = sum(str(row.get("information_flag")) == "LOW_INFORMATION" for row in rows)
        information.append(
            {
                "stage": stage,
                "role": role,
                "gap_start_count": count,
                "primary_plateau_rows": len(rows),
                "positive_variance_rows": positive,
                "positive_variance_fraction": positive / len(rows),
                "low_information_rows": low,
                "low_information_fraction": low / len(rows),
                "primary_expected_recurrences": expected,
                "expected_per_billion_gap_starts": expected * 1_000_000_000 / count,
                "hypothesis_test_performed": True,
            }
        )
    for stage, role, key, count in (
        ("P018-P0", "calibration margin-only", "p018p0", p018p0_count),
        ("P018-A", "prefix information margin-only", "p018a", p018a_count),
    ):
        gate = payloads[key]["gate"]
        assert isinstance(gate, dict)
        rows = _as_int(gate["primary_plateau_rows"], f"{stage} rows")
        expected = _as_float(gate["primary_expected_recurrences_total"], f"{stage} expected")
        information.append(
            {
                "stage": stage,
                "role": role,
                "gap_start_count": count,
                "primary_plateau_rows": rows,
                "positive_variance_rows": _as_int(
                    gate["primary_positive_variance_rows"], f"{stage} positive"
                ),
                "positive_variance_fraction": _as_int(
                    gate["primary_positive_variance_rows"], f"{stage} positive"
                )
                / rows,
                "low_information_rows": _as_int(
                    gate["primary_low_information_rows"], f"{stage} low"
                ),
                "low_information_fraction": _as_float(
                    gate["primary_low_information_fraction"], f"{stage} low fraction"
                ),
                "primary_expected_recurrences": expected,
                "expected_per_billion_gap_starts": expected * 1_000_000_000 / count,
                "hypothesis_test_performed": bool(gate["hypothesis_test_performed"]),
            }
        )

    p018_gate = payloads["p018a"]["gate"]
    p018_components = payloads["p018a"]["components"]
    assert isinstance(p018_gate, dict) and isinstance(p018_components, list)
    primary_components = [
        row
        for row in p018_components
        if isinstance(row, dict) and row.get("scheme") == PRIMARY_SCHEME
    ]
    funnel: list[dict[str, object]] = []
    for row in primary_components:
        forced = _as_int(row["forced_record_removed"], "forced record")
        conditioned = _as_int(row["conditioned_gap_count_after_removal"], "conditioned")
        funnel.append(
            {
                "record_index": _as_int(row["record_index"], "record index"),
                "gap": _as_int(row["gap"], "gap"),
                "population_before_removal": _as_int(
                    row["population_after_removal"], "population"
                )
                + forced,
                "plateau_exposure_after_removal": _as_int(
                    row["plateau_exposure_after_removal"], "exposure"
                ),
                "control_exposure": _as_int(row["control_exposure"], "control"),
                "target_gap_count_before_removal": conditioned + forced,
                "forced_record_removed": forced,
                "conditioned_gap_count_after_removal": conditioned,
                "expected_component": _as_float(row["expected_component"], "expected component"),
                "variance_component": _as_float(row["variance_component"], "variance component"),
                "information_flag": str(row["information_flag"]),
                "gate_recommendation": str(p018_gate["recommendation"]),
            }
        )
    if len(funnel) != 2 or sorted(_as_int(row["gap"], "gap") for row in funnel) != [582, 588]:
        raise SynthesisError("P018-A primary funnel must contain gaps 582 and 588")

    p011_total = sum(_as_float(row["p011_stationary_expected"], "P011 total") for row in correction)
    p012_total = sum(_as_float(row["p012_stratified_expected"], "P012 total") for row in correction)
    observed_total = sum(_as_int(row["observed_recurrences"], "observed total") for row in correction)
    reduction = 1.0 - p012_total / p011_total
    p006_recurrent_rows = sum(_as_int(row["C"], "P006 C") > 0 for row in p006_table)
    p006_recurrence_total = sum(_as_int(row["C"], "P006 C") for row in p006_table)
    p006_large_rows = [row for row in p006_table if _as_int(row["gap"], "P006 gap") >= 100]
    p006_large_recurrences = sum(_as_int(row["C"], "P006 C") for row in p006_large_rows)

    tables = {
        "coverage_ranges": coverage,
        "p006_descriptive_recurrence": p006_table,
        "null_model_correction": correction,
        "prospective_stage_summary": prospective,
        "information_collapse": information,
        "p018_forced_record_funnel": funnel,
    }
    summary: dict[str, object] = {
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "runner_revision": RUNNER_REVISION,
        "status": "PASS",
        "scientific_status": "SYNTHESIS_ONLY",
        "new_prime_computation": False,
        "theorem_claimed": False,
        "visual_qa": "PENDING_USER",
        "input_run_count": 8,
        "figure_family_count": 6,
        "figure_file_count": 12,
        "unique_reported_gap_start_accounting": unique_total,
        "raw_point_rows_saved": False,
        "boundary_discontinuity": {
            "x": 1_000_000_000,
            "gap_start": 999_999_937,
            "gap_end": 1_000_000_007,
            "gap": 70,
            "seamless_raw_union_missing_crossing_gap_count": 1,
        },
        "p006_descriptive": {
            "complete_plateau_rows": len(p006_table),
            "rows_with_recurrence": p006_recurrent_rows,
            "recurrence_total": p006_recurrence_total,
            "gap_ge_100_rows": len(p006_large_rows),
            "gap_ge_100_recurrence_total": p006_large_recurrences,
        },
        "development_null_correction": {
            "primary_rows": len(correction),
            "observed_total": observed_total,
            "p011_stationary_expected_total": p011_total,
            "p012_stratified_expected_total": p012_total,
            "relative_expected_reduction": reduction,
        },
        "prospective_primary": [
            {
                "stage": row["stage"],
                "observed": row["primary_observed_recurrences"],
                "expected": row["primary_expected_recurrences"],
                "positive_variance_rows": row["primary_positive_variance_rows"],
                "plateau_rows": row["primary_plateau_rows"],
            }
            for row in prospective
        ],
        "p018_margin_only": {
            "primary_gaps": [582, 588],
            "target_count_before_forced_removal_each": [
                row["target_gap_count_before_removal"] for row in funnel
            ],
            "conditioned_count_after_removal_each": [
                row["conditioned_gap_count_after_removal"] for row in funnel
            ],
            "positive_variance_rows": _as_int(
                p018_gate["primary_positive_variance_rows"], "P018 positive rows"
            ),
            "recommendation": str(p018_gate["recommendation"]),
            "hypothesis_test_performed": False,
        },
    }
    return SynthesisData(tables=tables, summary=summary)


def _save_figure_pair(fig: plt.Figure, figure_directory: Path, stem: str) -> list[Path]:
    paths = [figure_directory / f"{stem}.png", figure_directory / f"{stem}.pdf"]
    for path in paths:
        if path.exists():
            raise FileExistsError(path)
    figure_directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(paths[0], dpi=190, bbox_inches="tight", facecolor="white")
    fig.savefig(paths[1], bbox_inches="tight", facecolor="white", metadata={"Creator": "P020"})
    plt.close(fig)
    return paths


def _set_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.titlesize": 15,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def create_figures(tables: Mapping[str, Sequence[Mapping[str, object]]], output: Path) -> list[Path]:
    _set_style()
    created: list[Path] = []

    coverage = list(tables["coverage_ranges"])
    role_colors = {
        "descriptive development": "#4C78A8",
        "stationary-null diagnostic": "#9C755F",
        "stratified development": "#F58518",
        "independent holdout": "#54A24B",
        "prospective": "#59A14F",
        "calibration margin-only": "#B279A2",
        "prefix information margin-only": "#E45756",
    }
    fig, ax = plt.subplots(figsize=(12, 6.4))
    for y, row in enumerate(coverage):
        left = _as_float(row["log10_lower"], "coverage lower")
        right = _as_float(row["log10_upper"], "coverage upper")
        unique = _as_int(row["unique_accounting_count"], "coverage unique") > 0
        ax.barh(
            y,
            right - left,
            left=left,
            height=0.62,
            color=role_colors.get(str(row["role"]), "#888888"),
            alpha=0.88 if unique else 0.48,
            hatch=None if unique else "///",
            edgecolor="white",
        )
        row_count = _as_int(row["plateau_rows"], "plateau rows")
        label = f"{row_count} {'row' if row_count == 1 else 'rows'}"
        if right - left < 0.42:
            ax.text(
                left - 0.06,
                y,
                label,
                ha="right",
                va="center",
                color="black",
                fontsize=8,
                fontweight="bold",
            )
        else:
            ax.text(
                (left + right) / 2,
                y,
                label,
                ha="center",
                va="center",
                color="white" if unique else "black",
                fontsize=8,
                fontweight="bold",
            )
    ax.axvline(9.0, color="#D62728", linestyle="--", linewidth=1.3)
    ax.annotate(
        "one raw-stream seam gap\n999,999,937 -> 1,000,000,007 (gap 70)",
        xy=(9.0, 3.0),
        xytext=(9.18, 2.28),
        arrowprops={"arrowstyle": "->", "color": "#D62728"},
        color="#8B1A1A",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "#D62728", "alpha": 0.9},
    )
    ax.set_yticks(range(len(coverage)), [str(row["stage"]) for row in coverage])
    ax.invert_yaxis()
    ticks = list(range(0, 13))
    ax.set_xticks(ticks, [rf"$10^{{{tick}}}$" for tick in ticks])
    ax.set_xlim(0.0, 12.6)
    ax.set_xlabel("gap-start range (log10 x)")
    ax.set_title("Recurrence evidence coverage and experiment roles")
    ax.text(
        0.01,
        -0.17,
        "Solid = unique sweep in the 72,178,455,399 accounting; hatched = reused or nested evidence.",
        transform=ax.transAxes,
        fontsize=9,
    )
    created.extend(_save_figure_pair(fig, output, "01_recurrence_coverage_map"))

    p006 = list(tables["p006_descriptive_recurrence"])
    gaps = np.array([_as_int(row["gap"], "gap") for row in p006])
    m_values = np.array([_as_int(row["M"], "M") for row in p006])
    c_values = np.array([_as_int(row["C"], "C") for row in p006])
    r_values = np.array(
        [
            np.nan
            if str(row["R_C_over_N_minus_1"]).strip() == ""
            else _as_float(row["R_C_over_N_minus_1"], "R")
            for row in p006
        ]
    )
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    width = 3.1
    ax1.bar(gaps - width / 2, m_values, width=width, color="#4C78A8", label="M: all occurrences")
    ax1.bar(gaps + width / 2, c_values, width=width, color="#F58518", label="C: recurrences after record")
    ax1.set_ylabel("count inside plateau exposure")
    ax1.set_title("P006 complete plateaus: occurrence and recurrence counts")
    ax1.legend(loc="upper right")
    positive = r_values > 0
    zero = r_values == 0
    ax2.scatter(gaps[positive], r_values[positive], color="#54A24B", s=42, label="R > 0")
    zero_floor = 3e-8
    ax2.scatter(gaps[zero], np.full(zero.sum(), zero_floor), marker="v", color="#E45756", s=36, label="R = 0 (floor marker)")
    ax2.set_yscale("log")
    ax2.set_ylim(1e-8, 2)
    ax2.set_xlabel("record gap")
    ax2.set_ylabel("R = C/(N-1), log scale")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    created.extend(_save_figure_pair(fig, output, "02_p006_descriptive_recurrence"))

    correction = list(tables["null_model_correction"])
    cgaps = np.array([_as_int(row["gap"], "gap") for row in correction])
    observed = np.array([_as_int(row["observed_recurrences"], "observed") for row in correction])
    p011_expected = np.array([_as_float(row["p011_stationary_expected"], "P011") for row in correction])
    p012_expected = np.array([_as_float(row["p012_stratified_expected"], "P012") for row in correction])
    fig, ax = plt.subplots(figsize=(12, 6.7))
    ax.plot(cgaps, p011_expected, "o-", color="#9C755F", label="P011 stationary expected", alpha=0.85)
    ax.plot(cgaps, p012_expected, "s-", color="#F58518", label="P012 stratified expected", alpha=0.9)
    ax.scatter(cgaps, observed, marker="x", s=62, linewidths=2, color="#1F4E79", label="observed recurrence")
    ax.set_xlabel("record gap (primary cohort: start >= 1,000)")
    ax.set_ylabel("recurrence count")
    ax.set_title(
        "Same development evidence, different null: stationary expectation was too large",
        pad=38,
    )
    ax.legend(loc="upper right")
    ax.text(
        0.5,
        1.01,
        f"Totals: observed={observed.sum():.0f}, P011={p011_expected.sum():.3f}, P012={p012_expected.sum():.3f}\n"
        f"Expected-total reduction={(1 - p012_expected.sum()/p011_expected.sum())*100:.2f}%",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=9,
    )
    created.extend(_save_figure_pair(fig, output, "03_null_model_correction"))

    prospective = list(tables["prospective_stage_summary"])
    labels = [str(row["stage"]) for row in prospective]
    exp_values = np.array([_as_float(row["primary_expected_recurrences"], "expected") for row in prospective])
    obs_values = np.array([_as_int(row["primary_observed_recurrences"], "observed") for row in prospective])
    xpos = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    ax.bar(xpos - 0.18, obs_values, width=0.36, color="#4C78A8", label="observed")
    ax.bar(xpos + 0.18, exp_values, width=0.36, color="#F58518", label="primary expected")
    for i, row in enumerate(prospective):
        ax.text(
            i,
            max(obs_values[i], exp_values[i]) + 0.035,
            f"+var {row['primary_positive_variance_rows']}/{row['primary_plateau_rows']}",
            ha="center",
            fontsize=9,
        )
    ax.set_xticks(xpos, labels)
    ax.set_ylim(0, max(1.25, float(max(obs_values.max(), exp_values.max())) + 0.28))
    ax.set_ylabel("primary-cohort recurrence total")
    ax.set_title("Holdout and prospective stages: observed versus conditional-null expectation")
    ax.legend()
    ax.text(
        0.01,
        -0.14,
        "Stages are not pooled into one p-value or trend test; annotations show positive-variance rows.",
        transform=ax.transAxes,
        fontsize=9,
    )
    created.extend(_save_figure_pair(fig, output, "04_prospective_stage_summary"))

    information = list(tables["information_collapse"])
    raw_columns = [
        np.array([_as_float(row["primary_expected_recurrences"], "expected") for row in information]),
        np.array([_as_float(row["positive_variance_fraction"], "positive fraction") for row in information]),
        np.array([_as_float(row["low_information_fraction"], "low fraction") for row in information]),
    ]
    normalized: list[np.ndarray] = []
    for values in raw_columns:
        lo, hi = float(values.min()), float(values.max())
        if hi == lo:
            normalized.append(np.full_like(values, min(max(hi, 0.0), 1.0)))
        else:
            normalized.append((values - lo) / (hi - lo))
    matrix = np.column_stack(normalized)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    image = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)
    ax.grid(False)
    ax.set_xticks(
        range(3),
        ["primary expected", "positive-variance fraction", "LOW_INFORMATION fraction"],
    )
    ax.set_yticks(range(len(information)), [str(row["stage"]) for row in information])
    for i, row in enumerate(information):
        annotations = [
            f"{_as_float(row['primary_expected_recurrences'], 'expected'):.4g}",
            f"{row['positive_variance_rows']}/{row['primary_plateau_rows']}",
            f"{row['low_information_rows']}/{row['primary_plateau_rows']}",
        ]
        for j, label in enumerate(annotations):
            ax.text(j, i, label, ha="center", va="center", fontweight="bold", color="black")
    ax.set_title("Information collapse across recurrence stages")
    ax.text(
        0.0,
        -0.12,
        "Color is normalized within each column; cell labels are the exact saved values.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03, label="within-column relative intensity")
    created.extend(_save_figure_pair(fig, output, "05_information_collapse"))

    funnel = list(tables["p018_forced_record_funnel"])
    fgaps = [str(row["gap"]) for row in funnel]
    exposure_b = np.array([_as_int(row["plateau_exposure_after_removal"], "exposure") / 1e9 for row in funnel])
    control_b = np.array([_as_int(row["control_exposure"], "control") / 1e9 for row in funnel])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.8))
    fx = np.arange(len(fgaps))
    ax1.bar(fx, exposure_b, color="#4C78A8", label="plateau exposure")
    ax1.bar(fx, control_b, bottom=exposure_b, color="#BAB0AC", label="control exposure")
    ax1.set_xticks(fx, [f"gap {gap}" for gap in fgaps])
    ax1.set_ylabel("gap starts after forced-record removal (billions)")
    ax1.set_title("P018-A margin allocation")
    ax1.legend()
    steps = ["target in bin", "forced record", "conditioned target", "positive variance"]
    for offset, row in zip((-0.06, 0.06), funnel):
        values = [
            _as_int(row["target_gap_count_before_removal"], "target"),
            _as_int(row["forced_record_removed"], "forced"),
            _as_int(row["conditioned_gap_count_after_removal"], "conditioned"),
            1 if _as_float(row["variance_component"], "variance") > 0 else 0,
        ]
        ax2.plot(
            np.arange(4) + offset,
            values,
            marker="o",
            linewidth=2.2,
            label=f"gap {row['gap']}",
        )
        for x, value in enumerate(values):
            ax2.text(x + offset, value + 0.045, str(value), ha="center", fontsize=9)
    ax2.set_xticks(range(4), steps, rotation=18, ha="right")
    ax2.set_ylim(-0.05, 1.35)
    ax2.set_ylabel("count / indicator")
    ax2.set_title("Forced-record removal leaves no alternative target gap")
    ax2.legend()
    fig.suptitle("P018-A: large exposure did not create conditional information")
    fig.tight_layout()
    created.extend(_save_figure_pair(fig, output, "06_p018_forced_record_funnel"))
    return created


def figure_artifact_qa(figure_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    rows: list[dict[str, object]] = []
    pngs = sorted(figure_directory.glob("*.png"))
    pdfs = sorted(figure_directory.glob("*.pdf"))
    if len(pngs) != 6 or len(pdfs) != 6:
        issues.append(f"expected 6 PNG and 6 PDF, found {len(pngs)} and {len(pdfs)}")
    for path in pngs:
        try:
            with Image.open(path) as image:
                image.load()
                grayscale = image.convert("L")
                extrema = grayscale.getextrema()
                width, height = image.size
                if width < 900 or height < 500:
                    issues.append(f"PNG dimensions too small: {path.name} {width}x{height}")
                if extrema[0] == extrema[1]:
                    issues.append(f"PNG is visually constant: {path.name}")
                rows.append(
                    {
                        "file": path.name,
                        "kind": "png",
                        "width": width,
                        "height": height,
                        "grayscale_min": extrema[0],
                        "grayscale_max": extrema[1],
                        "sha256": sha256_file(path),
                    }
                )
        except Exception as exc:
            issues.append(f"PNG decode failed {path.name}: {type(exc).__name__}: {exc}")
    for path in pdfs:
        payload = path.read_bytes()
        if not payload.startswith(b"%PDF-"):
            issues.append(f"PDF header missing: {path.name}")
        if b"%%EOF" not in payload[-1024:]:
            issues.append(f"PDF EOF marker missing: {path.name}")
        rows.append(
            {
                "file": path.name,
                "kind": "pdf",
                "bytes": len(payload),
                "sha256": sha256_file(path),
            }
        )
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "figure_family_count": 6,
        "figure_file_count": len(pngs) + len(pdfs),
        "files": rows,
        "user_visual_qa": "PENDING_USER",
    }


def _relative(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def run_synthesis(project_root: Path, contract_path: Path, result_directory: Path) -> dict[str, object]:
    project_root = project_root.resolve()
    contract_path = contract_path.resolve()
    result_directory = result_directory.resolve()
    try:
        result_directory.relative_to(project_root)
    except ValueError as exc:
        raise SynthesisError("result directory must be inside project root") from exc
    if result_directory.exists():
        raise FileExistsError(result_directory)

    preflight = verify_inputs(project_root, contract_path)
    if preflight["status"] != "PASS":
        raise SynthesisError(f"input preflight failed: {preflight['issues']}")
    contract = load_contract(contract_path)
    payloads = load_payloads(project_root, contract)
    data = build_synthesis_data(payloads, contract)
    result_directory.mkdir(parents=True, exist_ok=False)
    table_directory = result_directory / "tables"
    figure_directory = result_directory / "figures"

    _write_json_exclusive(result_directory / "input_inventory.json", preflight)
    for name, rows in data.tables.items():
        _write_text_exclusive(
            table_directory / f"{name}.csv", _csv_text(rows, TABLE_FIELDS[name])
        )
    created_figures = create_figures(data.tables, figure_directory)
    _write_json_exclusive(result_directory / "summary.json", data.summary)
    qa = figure_artifact_qa(figure_directory)
    if qa["status"] != "PASS":
        raise SynthesisError(f"figure artifact QA failed: {qa['issues']}")
    _write_json_exclusive(result_directory / "artifact_qa.json", qa)

    artifacts = sorted(
        path for path in result_directory.rglob("*") if path.is_file() and path.name != "manifest.json"
    )
    manifest = {
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "runner_revision": RUNNER_REVISION,
        "status": "PASS",
        "scientific_status": "SYNTHESIS_ONLY",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "project_root": str(project_root),
        "contract": _relative(contract_path, project_root),
        "contract_sha256": sha256_file(contract_path),
        "source_files_sha256": {
            "source/recurrence_artifact_synthesis.py": sha256_file(Path(__file__)),
            "source/recurrence_artifact_synthesis_cli.py": sha256_file(
                Path(__file__).with_name("recurrence_artifact_synthesis_cli.py")
            ),
        },
        "input_manifest_sha256": {
            row["input_key"]: row["actual_manifest_sha256"] for row in preflight["inputs"]
        },
        "artifacts_sha256": {
            _relative(path, result_directory): sha256_file(path) for path in artifacts
        },
        "figure_files": [_relative(path, result_directory) for path in created_figures],
        "new_prime_computation": False,
        "theorem_claimed": False,
        "visual_qa": "PENDING_USER",
    }
    _write_json_exclusive(result_directory / "manifest.json", manifest)
    verification = verify_saved_synthesis(result_directory)
    if verification["status"] != "PASS":
        raise SynthesisError(f"saved synthesis verification failed: {verification['issues']}")
    _write_json_exclusive(result_directory / "saved_verification_report.json", verification)
    return {
        "status": "PASS",
        "result_directory": str(result_directory),
        "manifest_sha256": sha256_file(result_directory / "manifest.json"),
        "saved_verification": verification,
        "summary": data.summary,
    }


def verify_saved_synthesis(result_directory: Path) -> dict[str, object]:
    result_directory = result_directory.resolve()
    issues: list[str] = []
    try:
        manifest = _read_json_object(result_directory / "manifest.json")
        project_root = Path(str(manifest["project_root"])).resolve()
        contract_path = (project_root / str(manifest["contract"])).resolve()
        contract = load_contract(contract_path)
        if sha256_file(contract_path) != manifest.get("contract_sha256"):
            issues.append("contract SHA-256 mismatch")
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            issues.append("manifest artifacts_sha256 missing")
            artifacts = {}
        for relative, expected in artifacts.items():
            path = result_directory / str(relative)
            if not path.is_file():
                issues.append(f"missing artifact: {relative}")
            elif sha256_file(path) != expected:
                issues.append(f"artifact SHA-256 mismatch: {relative}")

        input_report = verify_inputs(project_root, contract_path)
        if input_report["status"] != "PASS":
            issues.extend(f"input recheck: {item}" for item in input_report["issues"])
        payloads = load_payloads(project_root, contract)
        recomputed = build_synthesis_data(payloads, contract)
        for name, rows in recomputed.tables.items():
            actual = (result_directory / "tables" / f"{name}.csv").read_text(
                encoding="utf-8"
            ).replace("\r\n", "\n")
            expected = _csv_text(rows, TABLE_FIELDS[name])
            if actual != expected:
                issues.append(f"table full recomputation mismatch: {name}")
        saved_summary = _read_json_object(result_directory / "summary.json")
        if saved_summary != recomputed.summary:
            issues.append("summary full recomputation mismatch")
        qa = figure_artifact_qa(result_directory / "figures")
        if qa["status"] != "PASS":
            issues.extend(f"figure QA: {item}" for item in qa["issues"])
        p018_fields = set(TABLE_FIELDS["p018_forced_record_funnel"])
        forbidden = {
            "observed_recurrence",
            "standardized_residual_z",
            "hypothesis_test_p_value",
            "multiple_testing_q_value",
        }
        overlap = sorted(p018_fields & forbidden)
        if overlap:
            issues.append(f"P018 forbidden output fields present: {overlap}")
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "artifact_hash_verification": "PASS" if not any("SHA-256" in item for item in issues) else "FAIL",
            "input_saved_verifiers": input_report["status"],
            "tables_full_recomputation": "PASS" if not any("table full" in item for item in issues) else "FAIL",
            "summary_full_recomputation": "PASS" if "summary full recomputation mismatch" not in issues else "FAIL",
            "figure_artifact_qa": qa["status"],
            "p018_margin_only_output_contract": "PASS" if not overlap else "FAIL",
            "theorem_claimed": False,
            "visual_qa": "PENDING_USER",
            "manifest_sha256": sha256_file(result_directory / "manifest.json"),
        }
    except Exception as exc:
        issues.append(f"{type(exc).__name__}: {exc}")
        return {
            "status": "FAIL",
            "issues": issues,
            "theorem_claimed": False,
            "visual_qa": "PENDING_USER",
        }


__all__ = [
    "EXPERIMENT",
    "EXPECTED_PYTHON",
    "PRIMARY_COHORT",
    "PRIMARY_SCHEME",
    "RUNNER_REVISION",
    "SCHEMA_VERSION",
    "SynthesisData",
    "SynthesisError",
    "TABLE_FIELDS",
    "build_synthesis_data",
    "create_figures",
    "figure_artifact_qa",
    "load_contract",
    "load_payloads",
    "run_synthesis",
    "sha256_file",
    "verify_inputs",
    "verify_saved_synthesis",
]
