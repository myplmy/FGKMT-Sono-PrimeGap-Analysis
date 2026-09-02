"""Command-line entrypoint for P020 recurrence artifact synthesis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.recurrence_artifact_synthesis import (
    run_synthesis,
    verify_inputs,
    verify_saved_synthesis,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--project-root", type=Path, required=True)
    preflight.add_argument("--contract", type=Path, required=True)

    run = subparsers.add_parser("run")
    run.add_argument("--project-root", type=Path, required=True)
    run.add_argument("--contract", type=Path, required=True)
    run.add_argument("--result-directory", type=Path, required=True)

    verify = subparsers.add_parser("verify-saved")
    verify.add_argument("--result-directory", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "preflight":
        contract = args.contract
        if not contract.is_absolute():
            contract = args.project_root / contract
        report = verify_inputs(args.project_root, contract)
    elif args.command == "run":
        contract = args.contract
        if not contract.is_absolute():
            contract = args.project_root / contract
        result = args.result_directory
        if not result.is_absolute():
            result = args.project_root / result
        report = run_synthesis(args.project_root, contract, result)
    else:
        report = verify_saved_synthesis(args.result_directory)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), flush=True)
    return 0 if report.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
