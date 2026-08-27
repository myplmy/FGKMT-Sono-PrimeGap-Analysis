"""CLI for the P010B exact candidate-cover toy and saved verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.candidate_cover import run_toy, verify_saved_toy


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    toy = subparsers.add_parser("toy")
    toy.add_argument("--output-directory", type=Path, required=True)
    toy.add_argument("--a", type=int, default=1_000)
    toy.add_argument("--b", type=int, default=10_000)
    toy.add_argument("--threshold", type=int, default=20)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "toy":
        _emit(
            run_toy(
                args.output_directory,
                a=args.a,
                b=args.b,
                threshold=args.threshold,
            )
        )
        return 0
    report = verify_saved_toy(args.result_directory)
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
