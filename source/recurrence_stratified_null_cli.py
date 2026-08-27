"""Command line interface for the approval-gated P012-A experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.recurrence_stratified_null import (
    ANALYSIS_LIMIT,
    DEFAULT_REPLICATIONS,
    DEFAULT_SEED,
    DEFAULT_SEGMENT_SPAN,
    run_stratified_null,
    validate_inputs,
    verify_saved_stratified_null,
)
from source.provenance import APPROVAL_TOKEN


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--complete-plateaus", type=Path, required=True)
    preflight.add_argument("--p011-statistics", type=Path, required=True)
    preflight.add_argument("--analysis-limit", type=int, default=ANALYSIS_LIMIT)
    preflight.add_argument("--segment-span", type=int, default=DEFAULT_SEGMENT_SPAN)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--approved-by-user", action="store_true")
    analyze.add_argument("--complete-plateaus", type=Path, required=True)
    analyze.add_argument("--p011-statistics", type=Path, required=True)
    analyze.add_argument("--output-directory", type=Path, required=True)
    analyze.add_argument("--analysis-limit", type=int, default=ANALYSIS_LIMIT)
    analyze.add_argument("--segment-span", type=int, default=DEFAULT_SEGMENT_SPAN)
    analyze.add_argument("--replications", type=int, default=DEFAULT_REPLICATIONS)
    analyze.add_argument("--seed", type=int, default=DEFAULT_SEED)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "preflight":
        _emit(
            validate_inputs(
                args.complete_plateaus,
                args.p011_statistics,
                analysis_limit=args.analysis_limit,
                segment_span=args.segment_span,
            )
        )
        return 0
    if args.command == "analyze":
        _emit(
            run_stratified_null(
                args.complete_plateaus,
                args.p011_statistics,
                args.output_directory,
                approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
                analysis_limit=args.analysis_limit,
                segment_span=args.segment_span,
                replications=args.replications,
                seed=args.seed,
            )
        )
        return 0
    report = verify_saved_stratified_null(args.result_directory)
    if args.report is not None:
        if args.report.exists():
            raise FileExistsError(f"refusing to overwrite verification report: {args.report}")
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    _emit(report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
