"""Independent high-precision verification of persisted experiment artifacts."""

from __future__ import annotations

import csv
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import mpmath as mp

from source.provenance import require_experiment_approval, sha256_file


VERIFY_DPS = 100
STORED_RELATIVE_TOLERANCE = mp.mpf("1e-38")
X_SCALE_POSITIVE_MIN = 3_814_280
SONO_CONSTANT = mp.mpf("2.0e-17")
ROLLING_WINDOWS = (5, 10, 20)


def _direct_f(x: int) -> mp.mpf:
    """Evaluate the fully expanded FGKMT scale without project helpers."""

    log_1 = mp.log(mp.mpf(x))
    log_2 = mp.log(log_1)
    log_3 = mp.log(log_2)
    log_4 = mp.log(log_3)
    return log_1 * log_2 * log_4 / log_3


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_json_exclusive(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def _relative_error(actual: mp.mpf, expected: mp.mpf) -> mp.mpf:
    if expected == 0:
        return abs(actual - expected)
    return abs((actual - expected) / expected)


def _check_numeric(
    stored_text: str,
    expected: mp.mpf,
    *,
    label: str,
    issues: list[dict[str, str]],
    maxima: dict[str, mp.mpf],
) -> None:
    try:
        stored = mp.mpf(stored_text)
    except (TypeError, ValueError):
        issues.append({"code": "invalid_numeric", "label": label, "stored": stored_text})
        return
    error = _relative_error(stored, expected)
    field = label.rsplit(".", 1)[-1]
    maxima[field] = max(maxima.get(field, mp.mpf("0")), error)
    if error > STORED_RELATIVE_TOLERANCE:
        issues.append(
            {
                "code": "numeric_mismatch",
                "label": label,
                "stored": stored_text,
                "expected": mp.nstr(expected, 70),
                "relative_error": mp.nstr(error, 20),
            }
        )


def _check_equal(
    actual: Any,
    expected: Any,
    *,
    label: str,
    issues: list[dict[str, str]],
) -> None:
    if actual != expected:
        issues.append(
            {
                "code": "exact_mismatch",
                "label": label,
                "stored": str(actual),
                "expected": str(expected),
            }
        )


def _closed_right_decade_exponent(x: int) -> int:
    exponent = len(str(x)) - 1
    if x == 10**exponent:
        exponent -= 1
    return exponent


def _expected_intervals(
    records: list[dict[str, str]],
    analysis_limit: int,
) -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    running_min = mp.inf
    for position, record in enumerate(records):
        end_prime = int(record["end_prime"])
        if end_prime > analysis_limit:
            break
        next_end = (
            int(records[position + 1]["end_prime"])
            if position + 1 < len(records)
            else None
        )
        x_left = max(end_prime, X_SCALE_POSITIVE_MIN)
        x_right = analysis_limit if next_end is None else min(next_end - 1, analysis_limit)
        if x_left > x_right:
            continue
        gap = int(record["gap"])
        f_left = _direct_f(x_left)
        f_right = _direct_f(x_right)
        h_left = mp.mpf(gap) / f_left
        h_minimum = mp.mpf(gap) / f_right
        running_min = min(running_min, h_minimum)
        expected.append(
            {
                "record_index": int(record["record_index"]),
                "start_prime": int(record["start_prime"]),
                "end_prime": end_prime,
                "gap": gap,
                "x_left": x_left,
                "x_right": x_right,
                "f_left": f_left,
                "f_right": f_right,
                "h_left": h_left,
                "h_interval_min": h_minimum,
                "running_min": running_min,
                "sono_ratio_min": h_minimum / SONO_CONSTANT,
                "cramer_ratio_min": mp.mpf(gap) / mp.log(mp.mpf(x_right)) ** 2,
            }
        )
        if x_right == analysis_limit:
            break
    return expected


def _expected_log_bins(intervals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    analysis_min = int(intervals[0]["x_left"])
    analysis_limit = int(intervals[-1]["x_right"])
    result: list[dict[str, Any]] = []
    for exponent in range(
        _closed_right_decade_exponent(analysis_min),
        _closed_right_decade_exponent(analysis_limit) + 1,
    ):
        nominal_left = 10**exponent
        nominal_right = 10 ** (exponent + 1)
        analyzed_left = max(analysis_min, nominal_left + 1)
        analyzed_right = min(analysis_limit, nominal_right)
        candidates: list[tuple[mp.mpf, int, dict[str, Any], mp.mpf]] = []
        for interval in intervals:
            overlap_left = max(analyzed_left, int(interval["x_left"]))
            overlap_right = min(analyzed_right, int(interval["x_right"]))
            if overlap_left > overlap_right:
                continue
            f_value = _direct_f(overlap_right)
            h_value = mp.mpf(interval["gap"]) / f_value
            candidates.append((h_value, overlap_right, interval, f_value))
        h_value, minimum_x, minimizing, f_value = min(
            candidates,
            key=lambda item: (item[0], item[1], item[2]["record_index"]),
        )
        result.append(
            {
                "decade_exponent": exponent,
                "bin_left_exclusive": nominal_left,
                "bin_right_inclusive": nominal_right,
                "analyzed_x_left": analyzed_left,
                "analyzed_x_right": analyzed_right,
                "minimizing_record_index": minimizing["record_index"],
                "gap_start_prime": minimizing["start_prime"],
                "gap_end_prime": minimizing["end_prime"],
                "gap": minimizing["gap"],
                "minimum_x": minimum_x,
                "f_at_minimum": f_value,
                "h_bin_min": h_value,
                "sono_ratio_min": h_value / SONO_CONSTANT,
            }
        )
    return result


def _expected_rolling(
    intervals: list[dict[str, Any]],
    window_size: int,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for end_position in range(window_size - 1, len(intervals)):
        window = intervals[end_position - window_size + 1 : end_position + 1]
        minimizing = min(
            window,
            key=lambda item: (
                item["h_interval_min"],
                item["x_right"],
                item["record_index"],
            ),
        )
        result.append(
            {
                "window_size": window_size,
                "window_start_record_index": window[0]["record_index"],
                "window_end_record_index": window[-1]["record_index"],
                "window_x_left": window[0]["x_left"],
                "window_x_right": window[-1]["x_right"],
                "minimizing_record_index": minimizing["record_index"],
                "gap_start_prime": minimizing["start_prime"],
                "gap_end_prime": minimizing["end_prime"],
                "gap": minimizing["gap"],
                "minimum_x": minimizing["x_right"],
                "f_at_minimum": minimizing["f_right"],
                "h_rolling_min": minimizing["h_interval_min"],
                "sono_ratio_min": minimizing["sono_ratio_min"],
            }
        )
    return result


def _compare_rows(
    stored_rows: list[dict[str, str]],
    expected_rows: list[dict[str, Any]],
    *,
    table_name: str,
    numeric_fields: Iterable[str],
    issues: list[dict[str, str]],
    maxima: dict[str, mp.mpf],
) -> None:
    _check_equal(
        len(stored_rows),
        len(expected_rows),
        label=f"{table_name}.row_count",
        issues=issues,
    )
    exact_fields = set(expected_rows[0]) - set(numeric_fields) if expected_rows else set()
    for position, (stored, expected) in enumerate(
        zip(stored_rows, expected_rows, strict=False),
        start=1,
    ):
        for field in exact_fields:
            _check_equal(
                stored.get(field),
                str(expected[field]),
                label=f"{table_name}[{position}].{field}",
                issues=issues,
            )
        for field in numeric_fields:
            _check_numeric(
                stored.get(field, ""),
                mp.mpf(expected[field]),
                label=f"{table_name}[{position}].{field}",
                issues=issues,
                maxima=maxima,
            )


def verify_result_artifacts(
    records_path: Path,
    result_directory: Path,
    *,
    approval_token: str | None,
) -> tuple[Path, dict[str, object]]:
    """Verify every persisted numeric row and end-bounded boundary independently."""

    require_experiment_approval(approval_token)
    report_path = result_directory / "verification_report.json"
    if report_path.exists():
        raise FileExistsError(f"refusing to overwrite verification report: {report_path}")

    summary_path = result_directory / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    analysis_limit = int(summary["analysis_max_x"])
    issues: list[dict[str, str]] = []
    maxima: dict[str, mp.mpf] = {}

    with mp.workdps(VERIFY_DPS):
        records = _read_csv(records_path)
        expected_intervals = _expected_intervals(records, analysis_limit)
        stored_intervals = _read_csv(
            result_directory / "tables" / "end_bounded_intervals.csv"
        )
        interval_numeric_fields = {
            "f_left",
            "f_right",
            "h_left",
            "h_interval_min",
            "running_min",
            "sono_ratio_min",
            "cramer_ratio_min",
        }
        _compare_rows(
            stored_intervals,
            expected_intervals,
            table_name="end_bounded_intervals",
            numeric_fields=interval_numeric_fields,
            issues=issues,
            maxima=maxima,
        )

        expected_jumps: list[dict[str, Any]] = []
        for previous, current in zip(records, records[1:], strict=False):
            jump_x = int(current["end_prime"])
            if jump_x < X_SCALE_POSITIVE_MIN or jump_x > analysis_limit:
                continue
            previous_gap = int(previous["gap"])
            new_gap = int(current["gap"])
            h_before = mp.mpf(previous_gap) / _direct_f(jump_x - 1)
            h_after = mp.mpf(new_gap) / _direct_f(jump_x)
            expected_jumps.append(
                {
                    "record_index": int(current["record_index"]),
                    "jump_x": jump_x,
                    "previous_gap": previous_gap,
                    "new_gap": new_gap,
                    "h_before_jump": h_before,
                    "h_after_jump": h_after,
                    "recovery_factor": h_after / h_before,
                }
            )
        stored_jumps = _read_csv(result_directory / "tables" / "end_bounded_jumps.csv")
        _compare_rows(
            stored_jumps,
            expected_jumps,
            table_name="end_bounded_jumps",
            numeric_fields={"h_before_jump", "h_after_jump", "recovery_factor"},
            issues=issues,
            maxima=maxima,
        )

        expected_bins = _expected_log_bins(expected_intervals)
        stored_bins = _read_csv(result_directory / "tables" / "log10_bin_minima.csv")
        _compare_rows(
            stored_bins,
            expected_bins,
            table_name="log10_bin_minima",
            numeric_fields={"f_at_minimum", "h_bin_min", "sono_ratio_min"},
            issues=issues,
            maxima=maxima,
        )

        rolling_counts: dict[str, int] = {}
        for window in ROLLING_WINDOWS:
            expected_rolling = _expected_rolling(expected_intervals, window)
            rolling_path = (
                result_directory
                / "tables"
                / f"rolling_local_envelope_w{window}.csv"
            )
            stored_rolling = _read_csv(rolling_path) if rolling_path.exists() else []
            _compare_rows(
                stored_rolling,
                expected_rolling,
                table_name=f"rolling_local_envelope_w{window}",
                numeric_fields={"f_at_minimum", "h_rolling_min", "sono_ratio_min"},
                issues=issues,
                maxima=maxima,
            )
            rolling_counts[str(window)] = len(expected_rolling)

        regression = next(
            (
                item
                for item in expected_intervals
                if item["start_prime"] == 4_652_353 and item["gap"] == 154
            ),
            None,
        )
        if regression is None:
            issues.append(
                {
                    "code": "missing_boundary_regression_record",
                    "label": "gap_154_start_4652353",
                }
            )
        else:
            _check_equal(
                regression["end_prime"],
                4_652_507,
                label="boundary_regression.end_prime",
                issues=issues,
            )
            _check_equal(
                regression["x_left"],
                4_652_507,
                label="boundary_regression.interval_start",
                issues=issues,
            )
            _check_equal(
                regression["x_right"],
                17_051_886,
                label="boundary_regression.interval_end",
                issues=issues,
            )

        minimum = min(expected_intervals, key=lambda item: item["h_interval_min"])
        _check_numeric(
            str(summary["minimum_h"]),
            minimum["h_interval_min"],
            label="summary.minimum_h",
            issues=issues,
            maxima=maxima,
        )
        _check_equal(
            str(summary["minimum_h_x"]),
            str(minimum["x_right"]),
            label="summary.minimum_h_x",
            issues=issues,
        )
        _check_equal(
            str(summary["minimum_h_gap"]),
            str(minimum["gap"]),
            label="summary.minimum_h_gap",
            issues=issues,
        )

    figure_paths = [Path(value) for value in summary.get("figure_files", [])]
    missing_figures = [str(path) for path in figure_paths if not path.is_file()]
    for path in missing_figures:
        issues.append({"code": "missing_figure", "label": path})

    artifact_paths = [
        summary_path,
        result_directory / "tables" / "end_bounded_intervals.csv",
        result_directory / "tables" / "end_bounded_jumps.csv",
        result_directory / "tables" / "log10_bin_minima.csv",
    ]
    artifact_paths.extend(
        result_directory / "tables" / f"rolling_local_envelope_w{window}.csv"
        for window in ROLLING_WINDOWS
        if (result_directory / "tables" / f"rolling_local_envelope_w{window}.csv").exists()
    )
    cross_validation_reports: dict[str, dict[str, str]] = {}
    for report_name in ("oeis_cross_validation.json", "oliveira_cross_validation.json"):
        cross_report_path = result_directory / "cross_validation" / report_name
        if not cross_report_path.exists():
            continue
        cross_report = json.loads(cross_report_path.read_text(encoding="utf-8"))
        cross_status = str(cross_report.get("status", "MISSING"))
        cross_validation_reports[report_name] = {
            "status": cross_status,
            "sha256": sha256_file(cross_report_path),
        }
        artifact_paths.append(cross_report_path)
        if cross_status != "PASS":
            issues.append(
                {
                    "code": "cross_validation_not_passed",
                    "label": report_name,
                    "status": cross_status,
                }
            )
    report: dict[str, object] = {
        "status": "PASS" if not issues else "FAIL",
        "verified_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "verification_dps": VERIFY_DPS,
        "stored_relative_tolerance": mp.nstr(STORED_RELATIVE_TOLERANCE, 5),
        "independent_formula": (
            "ln(x)*ln(ln(x))*ln(ln(ln(ln(x))))/ln(ln(ln(x))); "
            "source.definitions.F/H not called"
        ),
        "boundary_mode": "end",
        "interval_rule": "[end_i, end_(i+1)-1], clipped to analysis range",
        "records_path": str(records_path),
        "records_sha256": sha256_file(records_path),
        "result_directory": str(result_directory),
        "analysis_limit": str(analysis_limit),
        "verified_interval_count": len(expected_intervals),
        "verified_jump_count": len(expected_jumps),
        "verified_log_bin_count": len(expected_bins),
        "verified_rolling_counts": rolling_counts,
        "verified_numeric_value_count": (
            len(expected_intervals) * 7
            + len(expected_jumps) * 3
            + len(expected_bins) * 3
            + sum(rolling_counts.values()) * 3
            + 1
        ),
        "maximum_relative_error_by_field": {
            key: mp.nstr(value, 20) for key, value in sorted(maxima.items())
        },
        "boundary_regression_154": {
            "start_prime": "4652353",
            "gap": "154",
            "end_prime": "4652507",
            "interval": "[4652507,17051886]",
            "status": "PASS" if regression is not None else "FAIL",
        },
        "figure_file_count": len(figure_paths),
        "missing_figure_count": len(missing_figures),
        "cross_validation_reports": cross_validation_reports,
        "artifact_sha256": {
            str(path.relative_to(result_directory)): sha256_file(path)
            for path in artifact_paths
        },
        "execution": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "mpmath_version": mp.__version__,
        },
        "issue_count": len(issues),
        "issues": issues,
    }
    _write_json_exclusive(report_path, report)
    if issues:
        raise RuntimeError(
            f"result verification failed with {len(issues)} issue(s); report: {report_path}"
        )
    return report_path, report


__all__ = ["verify_result_artifacts"]
