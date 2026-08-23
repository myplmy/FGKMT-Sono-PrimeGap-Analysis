"""Approved P004 sensitivity artifact writer and independent verifier."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import mpmath as mp

from source.analysis import build_end_bounded_intervals, interval_to_dict
from source.definitions import SONO_CONSTANT, WORKING_DPS, X_SCALE_POSITIVE_MIN
from source.local_envelopes import build_rolling_local_envelope, local_metric_to_dict
from source.models import MaximalGapRecord
from source.pipeline import load_validated_records
from source.provenance import require_experiment_approval, sha256_file
from source.sensitivity import (
    ADDITIONAL_ROLLING_WINDOWS,
    SHIFTED_LOG10_OFFSETS,
    X_WIDTH_DECADES,
    build_boundary_difference_windows,
    build_boundary_pairs,
    build_shifted_log10_bin_minima,
    build_start_bounded_intervals,
    build_x_width_local_envelope,
    sensitivity_metric_to_dict,
)
from source.sensitivity_plots import plot_sensitivity_all


EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")
STORED_RELATIVE_TOLERANCE = mp.mpf("1e-38")
VERIFICATION_DPS = 100


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "NOT_INSTALLED"


def _code_snapshot() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    paths = sorted((root / "source").glob("*.py"))
    for relative in ("run_sensitivity_analysis.ps1", "requirements.txt", "environment.yml"):
        candidate = root / relative
        if candidate.exists():
            paths.append(candidate)
    paths = sorted(set(paths), key=lambda item: item.relative_to(root).as_posix())
    digest = hashlib.sha256()
    names: list[str] = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        names.append(relative)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return {"code_sha256": digest.hexdigest(), "code_files": names}


def _execution_metadata() -> dict[str, object]:
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "mpmath_version": _package_version("mpmath"),
        "matplotlib_version": _package_version("matplotlib"),
        "mpmath_dps": mp.mp.dps,
        "minimum_working_dps": WORKING_DPS,
    } | _code_snapshot()


def _write_csv_exclusive(
    path: Path,
    rows: Sequence[Mapping[str, object]],
) -> None:
    if not rows:
        raise ValueError(f"refusing to write an empty CSV: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_json_exclusive(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _key(value: mp.mpf) -> str:
    return mp.nstr(value, 10).replace(".", "p")


def analyze_sensitivity(
    records_path: Path,
    output_directory: Path,
    *,
    analysis_limit: int,
    expected_records_sha256: str,
    expected_source_commit: str,
    approval_token: str | None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if Path(sys.executable).resolve() != EXPECTED_PYTHON.resolve():
        raise RuntimeError(f"wrong Python executable: {sys.executable}")
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite result directory: {output_directory}")
    actual_records_hash = sha256_file(records_path)
    if actual_records_hash != expected_records_sha256:
        raise RuntimeError("validated record SHA-256 does not match the approved P004 plan")

    records = load_validated_records(records_path)
    if not records or records[0].source_commit != expected_source_commit:
        raise RuntimeError("validated records do not match the approved source commit")
    if analysis_limit > records[0].verified_exhaustive_limit:
        raise RuntimeError("analysis limit exceeds verified exhaustive coverage")

    output_directory.mkdir(parents=True, exist_ok=False)
    end_intervals = build_end_bounded_intervals(records, analysis_limit=analysis_limit)
    start_intervals = build_start_bounded_intervals(records, analysis_limit=analysis_limit)
    pairs = build_boundary_pairs(start_intervals, end_intervals)
    difference_windows = build_boundary_difference_windows(
        records, analysis_limit=analysis_limit
    )
    shifted = {
        mp.nstr(offset, 10): build_shifted_log10_bin_minima(
            end_intervals, shift_decades=offset
        )
        for offset in SHIFTED_LOG10_OFFSETS
    }
    rolling = {
        window: build_rolling_local_envelope(end_intervals, window_size=window)
        for window in ADDITIONAL_ROLLING_WINDOWS
    }
    x_width = {
        mp.nstr(width, 10): build_x_width_local_envelope(
            end_intervals, width_decades=width
        )
        for width in X_WIDTH_DECADES
    }

    table_directory = output_directory / "tables"
    _write_csv_exclusive(
        table_directory / "end_bounded_intervals.csv",
        [interval_to_dict(item) for item in end_intervals],
    )
    _write_csv_exclusive(
        table_directory / "start_bounded_intervals.csv",
        [interval_to_dict(item) for item in start_intervals],
    )
    _write_csv_exclusive(
        table_directory / "start_end_paired_intervals.csv",
        [sensitivity_metric_to_dict(item) for item in pairs],
    )
    _write_csv_exclusive(
        table_directory / "start_end_difference_windows.csv",
        [sensitivity_metric_to_dict(item) for item in difference_windows],
    )
    for shift_text, series in shifted.items():
        _write_csv_exclusive(
            table_directory / f"shifted_log10_bin_minima_s{shift_text.replace('.', 'p')}.csv",
            [sensitivity_metric_to_dict(item) for item in series],
        )
    for window, series in rolling.items():
        _write_csv_exclusive(
            table_directory / f"rolling_local_envelope_w{window}.csv",
            [local_metric_to_dict(item) for item in series],
        )
    for width_text, series in x_width.items():
        _write_csv_exclusive(
            table_directory / f"x_width_local_envelope_d{width_text.replace('.', 'p')}.csv",
            [sensitivity_metric_to_dict(item) for item in series],
        )

    minimum_end = min(end_intervals, key=lambda item: item.h_interval_min)
    minimum_start = min(start_intervals, key=lambda item: item.h_interval_min)
    largest_pair_effect = max(pairs, key=lambda item: abs(item.start_over_end_minus_one))
    largest_window_ratio = max(
        difference_windows, key=lambda item: item.start_over_end_ratio
    )
    shifted_summary = {}
    for shift_text, series in shifted.items():
        minimum = min(series, key=lambda item: item.h_bin_min)
        shifted_summary[shift_text] = {
            "bin_count": len(series),
            "minimum_h": mp.nstr(minimum.h_bin_min, 40),
            "minimum_x": str(minimum.minimum_x),
            "minimum_gap_start_prime": str(minimum.gap_start_prime),
            "minimum_gap_end_prime": str(minimum.gap_end_prime),
            "minimum_gap": str(minimum.gap),
        }
    rolling_summary = {
        str(window): {
            "count": len(series),
            "final_h": mp.nstr(series[-1].h_rolling_min, 40),
            "minimum_h": mp.nstr(min(item.h_rolling_min for item in series), 40),
        }
        for window, series in rolling.items()
    }
    x_width_summary = {}
    for width_text, series in x_width.items():
        full = [item for item in series if item.full_window]
        x_width_summary[width_text] = {
            "count": len(series),
            "full_window_count": len(full),
            "final_h": mp.nstr(series[-1].h_x_width_min, 40),
            "minimum_full_window_h": mp.nstr(
                min(item.h_x_width_min for item in full), 40
            )
            if full
            else None,
        }

    provenance_label = (
        f"source commit {expected_source_commit}; integer x; "
        f"analysis through {analysis_limit}; P004 sensitivity"
    )
    figure_paths = plot_sensitivity_all(
        end_intervals,
        start_intervals,
        pairs,
        shifted,
        rolling,
        x_width,
        output_directory / "figures",
        provenance_label=provenance_label,
    )
    summary: dict[str, object] = {
        "status": "COMPUTED_NOT_INTERPRETED",
        "computed_at_utc": _utc_now(),
        "analysis_min_x": str(X_SCALE_POSITIVE_MIN),
        "analysis_limit": str(analysis_limit),
        "verified_exhaustive_limit": str(records[0].verified_exhaustive_limit),
        "source_commit": expected_source_commit,
        "records_path": str(records_path),
        "records_sha256": actual_records_hash,
        "integer_domain": True,
        "end_boundary_definition": "max gap with end_prime <= x",
        "start_boundary_definition": "max gap with start_prime <= x",
        "real_domain_note": "half-open real intervals have an infimum at the next jump, not an attained minimum",
        "end_interval_count": len(end_intervals),
        "start_interval_count": len(start_intervals),
        "paired_record_count": len(pairs),
        "end_global_minimum": {
            "h": mp.nstr(minimum_end.h_interval_min, 40),
            "x": str(minimum_end.x_right),
            "record_index": minimum_end.record_index,
            "gap_start_prime": str(minimum_end.start_prime),
            "gap_end_prime": str(minimum_end.end_prime),
            "gap": str(minimum_end.gap),
        },
        "start_global_minimum": {
            "h": mp.nstr(minimum_start.h_interval_min, 40),
            "x": str(minimum_start.x_right),
            "record_index": minimum_start.record_index,
            "gap_start_prime": str(minimum_start.start_prime),
            "gap_end_prime": str(minimum_start.end_prime),
            "gap": str(minimum_start.gap),
        },
        "largest_paired_interval_minimum_relative_effect": {
            "record_index": largest_pair_effect.record_index,
            "start_over_end_minus_one": mp.nstr(
                largest_pair_effect.start_over_end_minus_one, 40
            ),
        },
        "finite_functions_differ_only_on_start_to_end_minus_one_windows": True,
        "difference_window_count": len(difference_windows),
        "difference_window_total_integer_width": str(
            sum(item.integer_width for item in difference_windows)
        ),
        "largest_pointwise_start_over_end_ratio": {
            "record_index": largest_window_ratio.record_index,
            "ratio": mp.nstr(largest_window_ratio.start_over_end_ratio, 40),
            "x_left": str(largest_window_ratio.x_left),
            "x_right": str(largest_window_ratio.x_right),
        },
        "shifted_log10_bins": shifted_summary,
        "additional_rolling_record_windows": rolling_summary,
        "x_width_trailing_envelopes": x_width_summary,
        "figure_files": [str(path) for path in figure_paths],
        "execution": _execution_metadata(),
        "interpretation_limits": [
            "Sono's finite G1 comparison applies to the end-bounded series only",
            "overlapping local windows are not independent samples",
            "finite robustness does not establish asymptotic behavior",
            "graph visual QA remains a user task",
        ],
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    return summary


def _direct_f(x: int | mp.mpf) -> mp.mpf:
    value = mp.mpf(x)
    log1 = mp.log(value)
    log2 = mp.log(log1)
    log3 = mp.log(log2)
    log4 = mp.log(log3)
    return log1 * log2 * log4 / log3


def _direct_intervals(
    records: Sequence[MaximalGapRecord],
    *,
    analysis_limit: int,
    mode: str,
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    running = mp.inf
    for position, record in enumerate(records):
        jump = record.start_prime if mode == "start" else record.end_prime
        if jump > analysis_limit:
            break
        if position + 1 < len(records):
            following = records[position + 1]
            next_jump = following.start_prime if mode == "start" else following.end_prime
        else:
            next_jump = None
        left = max(jump, X_SCALE_POSITIVE_MIN)
        right = analysis_limit if next_jump is None else min(next_jump - 1, analysis_limit)
        if left > right:
            continue
        f_left = _direct_f(left)
        f_right = _direct_f(right)
        h_left = mp.mpf(record.gap) / f_left
        h_min = mp.mpf(record.gap) / f_right
        running = min(running, h_min)
        result.append(
            {
                "record_index": record.record_index,
                "start_prime": record.start_prime,
                "end_prime": record.end_prime,
                "gap": record.gap,
                "x_left": left,
                "x_right": right,
                "f_left": f_left,
                "f_right": f_right,
                "h_left": h_left,
                "h_interval_min": h_min,
                "running_min": running,
                "sono_ratio_min": h_min / mp.mpf("2e-17"),
                "cramer_ratio_min": mp.mpf(record.gap) / mp.log(right) ** 2,
            }
        )
        if right == analysis_limit:
            break
    return result


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _relative_error(actual: mp.mpf, expected: mp.mpf) -> mp.mpf:
    if expected == 0:
        return abs(actual - expected)
    return abs((actual - expected) / expected)


def verify_sensitivity(
    records_path: Path,
    result_directory: Path,
    *,
    approval_token: str | None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    report_path = result_directory / "verification_report.json"
    if report_path.exists():
        raise FileExistsError(f"refusing to overwrite verification report: {report_path}")
    summary = json.loads((result_directory / "summary.json").read_text(encoding="utf-8"))
    records = load_validated_records(records_path)
    analysis_limit = int(summary["analysis_limit"])
    issues: list[str] = []
    checked = 0
    maximum_relative_error = mp.mpf("0")

    def check_int(actual: object, expected: int, label: str) -> None:
        nonlocal checked
        checked += 1
        if int(actual) != expected:
            issues.append(f"{label}: actual={actual} expected={expected}")

    def check_mpf(actual: object, expected: mp.mpf, label: str) -> None:
        nonlocal checked, maximum_relative_error
        checked += 1
        error = _relative_error(mp.mpf(actual), expected)
        maximum_relative_error = max(maximum_relative_error, error)
        if error > STORED_RELATIVE_TOLERANCE:
            issues.append(
                f"{label}: relative_error={mp.nstr(error, 12)} actual={actual} expected={mp.nstr(expected, 50)}"
            )

    with mp.workdps(VERIFICATION_DPS):
        direct_by_mode = {
            mode: _direct_intervals(records, analysis_limit=analysis_limit, mode=mode)
            for mode in ("end", "start")
        }
        for mode in ("end", "start"):
            rows = _read_csv(result_directory / "tables" / f"{mode}_bounded_intervals.csv")
            expected_rows = direct_by_mode[mode]
            if len(rows) != len(expected_rows):
                issues.append(f"{mode} interval count mismatch")
                continue
            for position, (row, expected) in enumerate(
                zip(rows, expected_rows, strict=True)
            ):
                prefix = f"{mode}[{position}]"
                for key in (
                    "record_index",
                    "start_prime",
                    "end_prime",
                    "gap",
                    "x_left",
                    "x_right",
                ):
                    check_int(row[key], int(expected[key]), f"{prefix}.{key}")
                for key in (
                    "f_left",
                    "f_right",
                    "h_left",
                    "h_interval_min",
                    "running_min",
                    "sono_ratio_min",
                    "cramer_ratio_min",
                ):
                    check_mpf(row[key], mp.mpf(expected[key]), f"{prefix}.{key}")

        end_direct = direct_by_mode["end"]
        start_direct = direct_by_mode["start"]
        end_map = {int(item["record_index"]): item for item in end_direct}
        start_map = {int(item["record_index"]): item for item in start_direct}
        pair_rows = _read_csv(
            result_directory / "tables" / "start_end_paired_intervals.csv"
        )
        for position, row in enumerate(pair_rows):
            record_index = int(row["record_index"])
            start = start_map[record_index]
            end = end_map[record_index]
            prefix = f"pair[{position}]"
            check_mpf(
                row["h_start_interval_min"],
                mp.mpf(start["h_interval_min"]),
                f"{prefix}.h_start",
            )
            check_mpf(
                row["h_end_interval_min"],
                mp.mpf(end["h_interval_min"]),
                f"{prefix}.h_end",
            )
            check_mpf(
                row["start_minus_end"],
                mp.mpf(start["h_interval_min"]) - mp.mpf(end["h_interval_min"]),
                f"{prefix}.delta",
            )
            check_mpf(
                row["start_over_end_minus_one"],
                mp.mpf(start["h_interval_min"]) / mp.mpf(end["h_interval_min"]) - 1,
                f"{prefix}.relative",
            )

        window_rows = _read_csv(
            result_directory / "tables" / "start_end_difference_windows.csv"
        )
        record_map = {record.record_index: record for record in records}
        positions = {record.record_index: i for i, record in enumerate(records)}
        for position, row in enumerate(window_rows):
            record = record_map[int(row["record_index"])]
            previous = records[positions[record.record_index] - 1]
            prefix = f"difference_window[{position}]"
            check_int(row["x_left"], max(record.start_prime, X_SCALE_POSITIVE_MIN), f"{prefix}.left")
            check_int(row["x_right"], min(record.end_prime - 1, analysis_limit), f"{prefix}.right")
            check_mpf(
                row["start_over_end_ratio"],
                mp.mpf(record.gap) / previous.gap,
                f"{prefix}.ratio",
            )

        for shift in SHIFTED_LOG10_OFFSETS:
            shift_text = mp.nstr(shift, 10)
            rows = _read_csv(
                result_directory
                / "tables"
                / f"shifted_log10_bin_minima_s{shift_text.replace('.', 'p')}.csv"
            )
            for position, row in enumerate(rows):
                k = int(row["bin_index"])
                left = max(
                    X_SCALE_POSITIVE_MIN,
                    int(mp.floor(mp.power(10, mp.mpf(k) + shift))) + 1,
                )
                right = min(
                    analysis_limit,
                    int(mp.floor(mp.power(10, mp.mpf(k + 1) + shift))),
                )
                candidates = []
                for interval in end_direct:
                    overlap_left = max(left, int(interval["x_left"]))
                    overlap_right = min(right, int(interval["x_right"]))
                    if overlap_left <= overlap_right:
                        value = mp.mpf(interval["gap"]) / _direct_f(overlap_right)
                        candidates.append((value, overlap_right, interval))
                expected_h, expected_x, expected_interval = min(
                    candidates,
                    key=lambda item: (item[0], item[1], int(item[2]["record_index"])),
                )
                prefix = f"shift[{shift_text}][{position}]"
                check_int(row["analyzed_x_left"], left, f"{prefix}.left")
                check_int(row["analyzed_x_right"], right, f"{prefix}.right")
                check_int(row["minimum_x"], expected_x, f"{prefix}.minimum_x")
                check_int(
                    row["minimizing_record_index"],
                    int(expected_interval["record_index"]),
                    f"{prefix}.record",
                )
                check_mpf(row["h_bin_min"], expected_h, f"{prefix}.h")
                check_mpf(row["f_at_minimum"], _direct_f(expected_x), f"{prefix}.f")

        for window in ADDITIONAL_ROLLING_WINDOWS:
            rows = _read_csv(
                result_directory / "tables" / f"rolling_local_envelope_w{window}.csv"
            )
            expected_count = len(end_direct) - window + 1
            if len(rows) != expected_count:
                issues.append(f"rolling w={window} count mismatch")
                continue
            for row_position, row in enumerate(rows, start=window - 1):
                selected = end_direct[row_position - window + 1 : row_position + 1]
                minimizing = min(
                    selected,
                    key=lambda item: (
                        mp.mpf(item["h_interval_min"]),
                        int(item["x_right"]),
                        int(item["record_index"]),
                    ),
                )
                prefix = f"rolling[{window}][{row_position}]"
                check_int(row["minimum_x"], int(minimizing["x_right"]), f"{prefix}.x")
                check_int(
                    row["minimizing_record_index"],
                    int(minimizing["record_index"]),
                    f"{prefix}.record",
                )
                check_mpf(
                    row["h_rolling_min"],
                    mp.mpf(minimizing["h_interval_min"]),
                    f"{prefix}.h",
                )

        for width in X_WIDTH_DECADES:
            width_text = mp.nstr(width, 10)
            rows = _read_csv(
                result_directory
                / "tables"
                / f"x_width_local_envelope_d{width_text.replace('.', 'p')}.csv"
            )
            factor = mp.power(10, width)
            if len(rows) != len(end_direct):
                issues.append(f"x-width d={width_text} count mismatch")
                continue
            for position, (row, endpoint) in enumerate(zip(rows, end_direct, strict=True)):
                right = int(endpoint["x_right"])
                nominal_left = mp.mpf(right) / factor
                left = max(X_SCALE_POSITIVE_MIN, int(mp.ceil(nominal_left)))
                candidates = []
                for interval in end_direct:
                    overlap_left = max(left, int(interval["x_left"]))
                    overlap_right = min(right, int(interval["x_right"]))
                    if overlap_left <= overlap_right:
                        value = mp.mpf(interval["gap"]) / _direct_f(overlap_right)
                        candidates.append((value, overlap_right, interval))
                expected_h, expected_x, expected_interval = min(
                    candidates,
                    key=lambda item: (item[0], item[1], int(item[2]["record_index"])),
                )
                prefix = f"xwidth[{width_text}][{position}]"
                check_int(row["window_x_left"], left, f"{prefix}.left")
                check_int(row["minimum_x"], expected_x, f"{prefix}.x")
                check_int(
                    row["minimizing_record_index"],
                    int(expected_interval["record_index"]),
                    f"{prefix}.record",
                )
                check_mpf(row["h_x_width_min"], expected_h, f"{prefix}.h")

    figure_files = list((result_directory / "figures").glob("*"))
    if len(figure_files) != 12 or any(path.stat().st_size <= 0 for path in figure_files):
        issues.append("expected 12 non-empty sensitivity figure files")
    artifacts = {
        str(path.relative_to(result_directory)): sha256_file(path)
        for path in sorted(result_directory.rglob("*"))
        if path.is_file() and path != report_path
    }
    report = {
        "status": "PASS" if not issues else "FAIL",
        "verified_at_utc": _utc_now(),
        "verification_dps": VERIFICATION_DPS,
        "stored_relative_tolerance": mp.nstr(STORED_RELATIVE_TOLERANCE, 10),
        "verified_numeric_or_integer_count": checked,
        "maximum_relative_error": mp.nstr(maximum_relative_error, 30),
        "issue_count": len(issues),
        "issues": issues,
        "figure_file_count": len(figure_files),
        "artifact_sha256": artifacts,
        "independent_formula": "ln(x)*ln(ln(x))*ln(ln(ln(ln(x))))/ln(ln(ln(x)))",
        "execution": _execution_metadata(),
    }
    _write_json_exclusive(report_path, report)
    return report


def _add_approval(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--approved-by-user", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--records-path", required=True)
    analyze.add_argument("--result-directory", required=True)
    analyze.add_argument("--analysis-limit", type=int, required=True)
    analyze.add_argument("--expected-records-sha256", required=True)
    analyze.add_argument("--expected-source-commit", required=True)
    _add_approval(analyze)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--records-path", required=True)
    verify.add_argument("--result-directory", required=True)
    _add_approval(verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    token = "USER_APPROVED_EXPERIMENT" if args.approved_by_user else None
    if args.command == "analyze":
        payload = analyze_sensitivity(
            Path(args.records_path),
            Path(args.result_directory),
            analysis_limit=args.analysis_limit,
            expected_records_sha256=args.expected_records_sha256,
            expected_source_commit=args.expected_source_commit,
            approval_token=token,
        )
    else:
        payload = verify_sensitivity(
            Path(args.records_path),
            Path(args.result_directory),
            approval_token=token,
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("status") not in {"FAIL", "BLOCKED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

