"""CLI for the approval-gated P012-B independent holdout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.provenance import APPROVAL_TOKEN
from source.recurrence_stratified_holdout import (
    DEFAULT_SEGMENT_SPAN,
    run_holdout,
    validate_inputs,
    verify_saved_holdout,
)
from source.recurrence_stratified_null import DEFAULT_REPLICATIONS, DEFAULT_SEED


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--records", type=Path, required=True)
    preflight.add_argument("--frozen-contract", type=Path, required=True)
    preflight.add_argument("--segment-span", type=int, default=DEFAULT_SEGMENT_SPAN)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--approved-by-user", action="store_true")
    analyze.add_argument("--records", type=Path, required=True)
    analyze.add_argument("--frozen-contract", type=Path, required=True)
    analyze.add_argument("--output-directory", type=Path, required=True)
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
                args.records,
                args.frozen_contract,
                segment_span=args.segment_span,
            )
        )
        return 0
    if args.command == "analyze":
        _emit(
            run_holdout(
                args.records,
                args.frozen_contract,
                args.output_directory,
                approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
                segment_span=args.segment_span,
                replications=args.replications,
                seed=args.seed,
            )
        )
        return 0
    report = verify_saved_holdout(args.result_directory)
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
