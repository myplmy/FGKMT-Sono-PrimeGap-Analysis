"""CLI for gated P009 single-block PARI boundary certification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source.boundary_witness_pari import run_single_block_actual, validate_prerequisites
from source.provenance import APPROVAL_TOKEN


def _emit(payload: object, *, stream: object = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "run"):
        command = subparsers.add_parser(name)
        command.add_argument("--local-bounds", type=Path, required=True)
        command.add_argument("--adapter-manifest", type=Path, required=True)
        command.add_argument("--replay-manifest", type=Path, required=True)
        if name == "run":
            command.add_argument("--approved-by-user", action="store_true")
            command.add_argument("--output-directory", type=Path, required=True)
            command.add_argument("--timeout-seconds", type=int, default=900)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "preflight":
            _emit(
                validate_prerequisites(
                    args.adapter_manifest, args.replay_manifest, args.local_bounds
                )
            )
            return 0
        _emit(
            run_single_block_actual(
                args.local_bounds,
                args.adapter_manifest,
                args.replay_manifest,
                args.output_directory,
                approval_token=(APPROVAL_TOKEN if args.approved_by_user else None),
                timeout_seconds=args.timeout_seconds,
            )
        )
        return 0
    except Exception as exc:
        _emit(
            {"status": "FAIL", "error_type": type(exc).__name__, "message": str(exc)},
            stream=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
