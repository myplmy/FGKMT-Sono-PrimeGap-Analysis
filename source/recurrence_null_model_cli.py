"""CLI for the user-run P011 recurrence null-model pilot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source.provenance import APPROVAL_TOKEN
from source.recurrence_null_model import (
    DEFAULT_REPLICATIONS,
    DEFAULT_SEED,
    run_null_model,
    validate_inputs,
    verify_saved_null_model,
)


def _emit(payload: object, *, stream: object = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--complete-plateaus", type=Path, required=True)
    preflight.add_argument("--gap-histogram", type=Path, required=True)
    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--approved-by-user", action="store_true")
    analyze.add_argument("--complete-plateaus", type=Path, required=True)
    analyze.add_argument("--gap-histogram", type=Path, required=True)
    analyze.add_argument("--output-directory", type=Path, required=True)
    analyze.add_argument("--replications", type=int, default=DEFAULT_REPLICATIONS)
    analyze.add_argument("--seed", type=int, default=DEFAULT_SEED)
    analyze.add_argument("--no-plots", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "preflight":
            _emit(validate_inputs(args.complete_plateaus, args.gap_histogram))
            return 0
        if args.command == "analyze":
            _emit(
                run_null_model(
                    args.complete_plateaus,
                    args.gap_histogram,
                    args.output_directory,
                    approval_token=(APPROVAL_TOKEN if args.approved_by_user else None),
                    replications=args.replications,
                    seed=args.seed,
                    make_plots=not args.no_plots,
                )
            )
            return 0
        report = verify_saved_null_model(args.result_directory)
        _emit(report)
        return 0 if report["status"] == "PASS" else 1
    except Exception as exc:
        _emit(
            {"status": "FAIL", "error_type": type(exc).__name__, "message": str(exc)},
            stream=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
