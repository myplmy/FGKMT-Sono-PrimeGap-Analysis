"""CLI for P009 boundary-witness toy generation and verification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source.boundary_witness import run_toy_witness, verify_saved_toy_result


EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")


def _emit(payload: object, *, stream: object = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def _preflight(_: argparse.Namespace) -> int:
    matches = EXPECTED_PYTHON.is_file() and Path(sys.executable).resolve() == EXPECTED_PYTHON.resolve()
    payload = {
        "status": "PASS" if matches else "FAIL",
        "python_executable": sys.executable,
        "expected_python_executable": str(EXPECTED_PYTHON),
        "python_executable_matches": matches,
        "mode": "toy-only",
        "actual_1e20_experiment_executed": False,
        "pari_required_for_toy": False,
        "gpu_used": False,
    }
    _emit(payload)
    return 0 if matches else 1


def _toy(args: argparse.Namespace) -> int:
    _emit(run_toy_witness(Path(args.output_directory)))
    return 0


def _verify(args: argparse.Namespace) -> int:
    report = verify_saved_toy_result(Path(args.result_directory))
    _emit(report)
    return 0 if report["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("preflight")
    preflight.set_defaults(handler=_preflight)
    toy = subparsers.add_parser("toy")
    toy.add_argument("--output-directory", required=True)
    toy.set_defaults(handler=_toy)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", required=True)
    verify.set_defaults(handler=_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except Exception as exc:
        _emit(
            {"status": "FAIL", "error_type": type(exc).__name__, "message": str(exc)},
            stream=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
