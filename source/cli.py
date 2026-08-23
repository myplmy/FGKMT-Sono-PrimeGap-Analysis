"""Command-line entry point for the gated FGKMT/Sono experiment."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp

from source.analysis import analysis_limit_for_interval_count, record_at_x
from source.cross_validation import (
    cross_validate_oeis,
    cross_validate_oliveira,
)
from source.definitions import (
    F,
    H,
    SONO_CONSTANT,
    WORKING_DPS,
    X_SCALE_POSITIVE_MIN,
    iter_log,
)
from source.pipeline import (
    analyze_validated_records,
    load_validated_records,
    validate_raw_dataset,
)
from source.prime_gap_list import DEFAULT_EXHAUSTIVE_LIMIT
from source.provenance import (
    APPROVAL_TOKEN,
    DEFAULT_BRANCH,
    RAW_FILE_NAME,
    SCHEMA_FILE_NAME,
    acquire_dataset,
    pinned_raw_url,
    require_experiment_approval,
    resolve_remote_head,
)
from source.result_verification import verify_result_artifacts

EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")


def workspace_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _approval_value(args: argparse.Namespace) -> str | None:
    return APPROVAL_TOKEN if getattr(args, "approved_by_user", False) else None


def _preflight() -> int:
    mp.mp.dps = max(mp.mp.dps, WORKING_DPS)
    x = mp.mpf("1e100")
    nested = mp.log(mp.log(mp.log(mp.log(x))))
    executable_matches = (
        Path(sys.executable).resolve() == EXPECTED_PYTHON.resolve()
        if EXPECTED_PYTHON.is_file()
        else False
    )
    iterated_match = bool(mp.almosteq(iter_log(x, 4), nested))
    checks_passed = (
        executable_matches
        and mp.mp.dps >= WORKING_DPS
        and iterated_match
        and F(X_SCALE_POSITIVE_MIN) > 0
    )
    payload = {
        "status": "PASS" if checks_passed else "FAIL",
        "python_executable": sys.executable,
        "expected_python_executable": str(EXPECTED_PYTHON),
        "python_executable_matches": executable_matches,
        "mpmath_dps": mp.mp.dps,
        "x_scale_positive_min": X_SCALE_POSITIVE_MIN,
        "iter_log_4_matches_nested": iterated_match,
        "base_log_negative_control": "covered by tests/test_iterated_logs.py",
        "F_1e100": mp.nstr(F(x), 40),
        "actual_experiment_executed": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if checks_passed else 1


def _status() -> int:
    root = workspace_root()
    raw_files = list((root / "datas" / "raw").glob("**/allgaps.sql"))
    validated_files = list((root / "datas" / "validated").glob("**/maximal_gap_records.csv"))
    run_summaries = list((root / "test_result").glob("run_*/summary.json"))
    print(
        json.dumps(
            {
                "workspace_root": str(root),
                "raw_dataset_count": len(raw_files),
                "validated_dataset_count": len(validated_files),
                "completed_analysis_count": len(run_summaries),
                "approval_required_for_mutating_stages": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _fetch(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    if args.dry_run:
        commit = args.commit or "<resolve master at execution time>"
        source_urls = (
            {
                RAW_FILE_NAME: pinned_raw_url(commit, RAW_FILE_NAME),
                SCHEMA_FILE_NAME: pinned_raw_url(commit, SCHEMA_FILE_NAME),
            }
            if args.commit
            else {
                RAW_FILE_NAME: "<commit-pinned allgaps.sql URL>",
                SCHEMA_FILE_NAME: "<commit-pinned schema.sql URL>",
            }
        )
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "branch": args.branch,
                    "commit": commit,
                    "source_urls": source_urls,
                    "network_used": False,
                    "files_written": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    raw_path, metadata_path, metadata = acquire_dataset(
        workspace_root(),
        approval_token=token,
        commit=args.commit,
        branch=args.branch,
    )
    print(
        json.dumps(
            {
                "status": "FETCHED",
                "raw_path": str(raw_path),
                "metadata_path": str(metadata_path),
                "commit": metadata["commit"],
                "sha256": metadata["sha256"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _validate(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    metadata = json.loads(Path(args.metadata_path).read_text(encoding="utf-8"))
    commit = str(metadata.get("commit", ""))
    output_directory = (
        workspace_root()
        / "datas"
        / "validated"
        / "prime-gap-list-project"
        / commit
    )
    records_path, report_path, records, report = validate_raw_dataset(
        Path(args.raw_path),
        Path(args.metadata_path),
        output_directory,
        approval_token=token,
        exhaustive_limit=args.exhaustive_limit,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "records_path": str(records_path),
                "report_path": str(report_path),
                "record_count": len(records),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _analyze(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    records = load_validated_records(Path(args.records_path))
    if not records:
        raise ValueError("validated records file is empty")
    commit = records[0].source_commit
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"{timestamp}_{commit[:12]}"
    output_directory = workspace_root() / "test_result" / f"run_{run_id}"
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite an existing run: {output_directory}")
    summary = analyze_validated_records(
        Path(args.records_path),
        output_directory,
        approval_token=token,
        analysis_limit=args.analysis_limit,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _cross_validate_oeis(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    result_directory = Path(args.result_directory)
    if not result_directory.is_dir():
        raise FileNotFoundError(f"result directory does not exist: {result_directory}")
    raw_directory = (
        workspace_root()
        / "datas"
        / "raw"
        / "independent"
        / "oeis"
        / args.source_run_id
    )
    report_path, report = cross_validate_oeis(
        Path(args.records_path),
        raw_directory,
        result_directory,
        approval_token=token,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "source": "OEIS A002386 + A005250",
                "report_path": str(report_path),
                "overlap_record_count": report["overlap_record_count"],
                "mismatch_count": report["mismatch_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _cross_validate_oliveira(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    result_directory = Path(args.result_directory)
    if not result_directory.is_dir():
        raise FileNotFoundError(f"result directory does not exist: {result_directory}")
    raw_directory = (
        workspace_root()
        / "datas"
        / "raw"
        / "independent"
        / "oliveira"
        / args.source_run_id
    )
    report_path, report = cross_validate_oliveira(
        Path(args.records_path),
        raw_directory,
        result_directory,
        approval_token=token,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "source": "Oliveira e Silva official t0.txt.gz",
                "report_path": str(report_path),
                "overlap_record_count": report["overlap_record_count"],
                "mismatch_count": report["mismatch_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _verify_results(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    report_path, report = verify_result_artifacts(
        Path(args.records_path),
        Path(args.result_directory),
        approval_token=token,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "report_path": str(report_path),
                "verified_numeric_value_count": report["verified_numeric_value_count"],
                "issue_count": report["issue_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _run(args: argparse.Namespace) -> int:
    token = _approval_value(args)
    require_experiment_approval(token)
    commit = args.commit or resolve_remote_head(branch=args.branch)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"{timestamp}_{commit[:12]}"
    output_directory = workspace_root() / "test_result" / f"run_{run_id}"
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite an existing run: {output_directory}")

    raw_path, metadata_path, _ = acquire_dataset(
        workspace_root(),
        approval_token=token,
        commit=commit,
        branch=args.branch,
    )
    validated_directory = (
        workspace_root()
        / "datas"
        / "validated"
        / "prime-gap-list-project"
        / commit
    )
    records_path, _, _, report = validate_raw_dataset(
        raw_path,
        metadata_path,
        validated_directory,
        approval_token=token,
        exhaustive_limit=DEFAULT_EXHAUSTIVE_LIMIT,
    )
    summary = analyze_validated_records(
        records_path,
        output_directory,
        approval_token=token,
        analysis_limit=args.analysis_limit,
    )
    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "validation": report["status"],
                "run_directory": str(output_directory),
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _pilot(args: argparse.Namespace) -> int:
    """Run the approved x=16/x_min and fixed-interval smoke experiment."""

    token = _approval_value(args)
    require_experiment_approval(token)
    if args.interval_count < 1:
        raise ValueError("interval_count must be positive")
    commit = args.commit or resolve_remote_head(branch=args.branch)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"{timestamp}_{commit[:12]}_pilot{args.interval_count}"
    output_directory = workspace_root() / "test_result" / f"run_{run_id}"
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite an existing run: {output_directory}")

    raw_path, metadata_path, _ = acquire_dataset(
        workspace_root(),
        approval_token=token,
        commit=commit,
        branch=args.branch,
    )
    validated_directory = (
        workspace_root()
        / "datas"
        / "validated"
        / "prime-gap-list-project"
        / commit
    )
    records_path, report_path, records, report = validate_raw_dataset(
        raw_path,
        metadata_path,
        validated_directory,
        approval_token=token,
        exhaustive_limit=DEFAULT_EXHAUSTIVE_LIMIT,
    )

    probe_x = 16
    probe_record = record_at_x(records, probe_x)
    f_probe = F(probe_x)
    if f_probe >= 0:
        raise RuntimeError("x=16 diagnostic expected F(x) < 0")

    scale_record = record_at_x(records, X_SCALE_POSITIVE_MIN)
    f_scale = F(X_SCALE_POSITIVE_MIN)
    if f_scale <= 0:
        raise RuntimeError("positive FGKMT scale did not begin at configured x_min")

    analysis_limit = analysis_limit_for_interval_count(
        records,
        interval_count=args.interval_count,
    )
    scope = {
        "execution_scope": "LIMITED_PILOT",
        "pilot_interval_count_requested": args.interval_count,
        "pilot_interval_selection": (
            "the plateau active at x=3814280 followed through the requested "
            "number of consecutive end-bounded record intervals"
        ),
        "pilot_derived_analysis_limit": str(analysis_limit),
        "point_diagnostics": {
            "x_16": {
                "x": str(probe_x),
                "g_end_bounded": str(probe_record.gap),
                "active_record_end_prime": str(probe_record.end_prime),
                "f": mp.nstr(f_probe, 40),
                "f_sign": "negative",
                "theorem_scale_h_included": False,
                "sono_ratio_included": False,
                "reason": "domain diagnostic only because F(x) is non-positive",
            },
            "x_scale_positive_min": {
                "x": str(X_SCALE_POSITIVE_MIN),
                "g_end_bounded": str(scale_record.gap),
                "active_record_end_prime": str(scale_record.end_prime),
                "f": mp.nstr(f_scale, 40),
                "h": mp.nstr(H(X_SCALE_POSITIVE_MIN, scale_record.gap), 40),
                "sono_ratio": mp.nstr(
                    H(X_SCALE_POSITIVE_MIN, scale_record.gap) / SONO_CONSTANT,
                    40,
                ),
                "theorem_scale_h_included": True,
            },
        },
    }
    summary = analyze_validated_records(
        records_path,
        output_directory,
        approval_token=token,
        analysis_limit=analysis_limit,
        summary_additions=scope,
    )
    if summary["analyzed_interval_count"] != args.interval_count:
        raise RuntimeError("pilot did not produce the requested number of intervals")

    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "execution_scope": "LIMITED_PILOT",
                "validation": report["status"],
                "validation_report": str(report_path),
                "run_directory": str(output_directory),
                "summary": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _add_approval_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--approved-by-user",
        action="store_true",
        help="assert that the user explicitly authorized actual experiment execution",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight_parser = subparsers.add_parser("preflight", help="run data-independent checks")
    preflight_parser.set_defaults(handler=lambda _args: _preflight())

    status_parser = subparsers.add_parser("status", help="report local artifact counts only")
    status_parser.set_defaults(handler=lambda _args: _status())

    fetch_parser = subparsers.add_parser("fetch", help="fetch a commit-pinned upstream dataset")
    fetch_parser.add_argument("--branch", default=DEFAULT_BRANCH)
    fetch_parser.add_argument("--commit")
    fetch_parser.add_argument("--dry-run", action="store_true")
    _add_approval_flag(fetch_parser)
    fetch_parser.set_defaults(handler=_fetch)

    validate_parser = subparsers.add_parser("validate", help="validate and normalize raw input")
    validate_parser.add_argument("--raw-path", required=True)
    validate_parser.add_argument("--metadata-path", required=True)
    validate_parser.add_argument("--exhaustive-limit", type=int, default=DEFAULT_EXHAUSTIVE_LIMIT)
    _add_approval_flag(validate_parser)
    validate_parser.set_defaults(handler=_validate)

    analyze_parser = subparsers.add_parser("analyze", help="compute tables, summary, and figures")
    analyze_parser.add_argument("--records-path", required=True)
    analyze_parser.add_argument("--analysis-limit", type=int, default=DEFAULT_EXHAUSTIVE_LIMIT)
    analyze_parser.add_argument("--run-id")
    _add_approval_flag(analyze_parser)
    analyze_parser.set_defaults(handler=_analyze)

    oeis_parser = subparsers.add_parser(
        "cross-validate-oeis",
        help="download immutable OEIS b-files and cross-check canonical records",
    )
    oeis_parser.add_argument("--records-path", required=True)
    oeis_parser.add_argument("--result-directory", required=True)
    oeis_parser.add_argument("--source-run-id", required=True)
    _add_approval_flag(oeis_parser)
    oeis_parser.set_defaults(handler=_cross_validate_oeis)

    oliveira_parser = subparsers.add_parser(
        "cross-validate-oliveira",
        help="cross-check canonical records against Oliveira's official table",
    )
    oliveira_parser.add_argument("--records-path", required=True)
    oliveira_parser.add_argument("--result-directory", required=True)
    oliveira_parser.add_argument("--source-run-id", required=True)
    _add_approval_flag(oliveira_parser)
    oliveira_parser.set_defaults(handler=_cross_validate_oliveira)

    verify_parser = subparsers.add_parser(
        "verify-results",
        help="independently verify all persisted F/H and envelope values",
    )
    verify_parser.add_argument("--records-path", required=True)
    verify_parser.add_argument("--result-directory", required=True)
    _add_approval_flag(verify_parser)
    verify_parser.set_defaults(handler=_verify_results)

    run_parser = subparsers.add_parser("run", help="fetch, validate, and analyze in one gated run")
    run_parser.add_argument("--branch", default=DEFAULT_BRANCH)
    run_parser.add_argument("--commit")
    run_parser.add_argument("--analysis-limit", type=int, default=DEFAULT_EXHAUSTIVE_LIMIT)
    run_parser.add_argument("--run-id")
    _add_approval_flag(run_parser)
    run_parser.set_defaults(handler=_run)

    pilot_parser = subparsers.add_parser(
        "pilot",
        help="run the approved x=16/x_min and fixed-interval pilot",
    )
    pilot_parser.add_argument("--branch", default=DEFAULT_BRANCH)
    pilot_parser.add_argument("--commit")
    pilot_parser.add_argument("--interval-count", type=int, default=5)
    pilot_parser.add_argument("--run-id")
    _add_approval_flag(pilot_parser)
    pilot_parser.set_defaults(handler=_pilot)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
