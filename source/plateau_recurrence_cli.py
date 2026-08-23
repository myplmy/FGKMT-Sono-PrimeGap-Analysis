"""Approval-gated command line interface for P006 plateau recurrence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np

from source.plateau_recurrence import (
    KNOWN_PRIME_COUNTS,
    run_plateau_recurrence_analysis,
    verify_saved_result,
)
from source.provenance import APPROVAL_TOKEN, sha256_file


EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")
PINNED_RECORDS_SHA256 = "62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297"
PINNED_SOURCE_COMMIT = "1a112a1387052d9ad360686313f501c01fe46b68"
SUPPORTED_PRODUCTION_LIMITS = (100_000_000, 1_000_000_000, 10_000_000_000)
MIN_SEGMENT_SPAN = 1_000_000
MAX_SEGMENT_SPAN = 200_000_000


def _preflight(args: argparse.Namespace) -> int:
    records_path = Path(args.records_path)
    executable_matches = (
        EXPECTED_PYTHON.is_file()
        and Path(sys.executable).resolve() == EXPECTED_PYTHON.resolve()
    )
    records_exists = records_path.is_file()
    records_hash = sha256_file(records_path) if records_exists else None
    checks = {
        "python_executable_matches": executable_matches,
        "records_file_exists": records_exists,
        "records_sha256_matches": records_hash == PINNED_RECORDS_SHA256,
        "analysis_limit_supported": args.analysis_limit in SUPPORTED_PRODUCTION_LIMITS,
        "pi_value_pinned": args.analysis_limit in KNOWN_PRIME_COUNTS,
        "segment_span_in_range": MIN_SEGMENT_SPAN
        <= args.segment_span
        <= MAX_SEGMENT_SPAN,
        "numpy_available": True,
        "matplotlib_available": True,
        "gpu_required": False,
        "network_required": False,
    }
    payload = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "python_executable": sys.executable,
        "expected_python_executable": str(EXPECTED_PYTHON),
        "numpy_version": np.__version__,
        "matplotlib_version": matplotlib.__version__,
        "records_path": str(records_path),
        "records_sha256": records_hash,
        "expected_records_sha256": PINNED_RECORDS_SHA256,
        "source_commit": PINNED_SOURCE_COMMIT,
        "analysis_limit": args.analysis_limit,
        "segment_span": args.segment_span,
        "actual_experiment_executed": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "PASS" else 1


def _analyze(args: argparse.Namespace) -> int:
    token = APPROVAL_TOKEN if args.approved_by_user else None
    summary = run_plateau_recurrence_analysis(
        Path(args.records_path),
        Path(args.output_directory),
        approval_token=token,
        analysis_limit=args.analysis_limit,
        segment_span=args.segment_span,
        make_plots=not args.no_plots,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _verify(args: argparse.Namespace) -> int:
    report = verify_saved_result(Path(args.result_directory))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--records-path", required=True)
    preflight.add_argument("--analysis-limit", type=int, required=True)
    preflight.add_argument("--segment-span", type=int, required=True)
    preflight.set_defaults(handler=_preflight)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--records-path", required=True)
    analyze.add_argument("--output-directory", required=True)
    analyze.add_argument("--analysis-limit", type=int, required=True)
    analyze.add_argument("--segment-span", type=int, required=True)
    analyze.add_argument("--approved-by-user", action="store_true")
    analyze.add_argument("--no-plots", action="store_true")
    analyze.set_defaults(handler=_analyze)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", required=True)
    verify.set_defaults(handler=_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
