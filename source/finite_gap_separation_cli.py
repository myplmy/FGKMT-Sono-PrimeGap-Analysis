"""Preflight and toy CLI for P007 modulus-30030 separation design."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source.finite_gap_certificate import DEFAULT_H, state_count
from source.finite_gap_separation import (
    SeparationCandidate,
    scan_transition_violations,
    separation_memory_estimate,
)


EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")


def _emit(payload: object, *, stream: object = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def _preflight(args: argparse.Namespace) -> int:
    python_matches = EXPECTED_PYTHON.is_file() and Path(sys.executable).resolve() == EXPECTED_PYTHON.resolve()
    estimate = separation_memory_estimate(30030, chunk_rows=args.chunk_rows, top_k=args.top_k)
    checks = {
        "python_executable_matches": python_matches,
        "mod30030_states_is_5760": estimate["states"] == 5760,
        "chunk_estimate_under_1_gib": estimate["under_1_gib"],
        "full_matrix_not_materialized": not estimate["full_constraint_matrix_materialized"],
    }
    payload = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "memory_estimate": estimate,
        "mod30030_scan_executed": False,
        "mod30030_lp_solved": False,
        "exact_mod30030_certificate_produced": False,
    }
    _emit(payload)
    return 0 if payload["status"] == "PASS" else 1


def _toy(args: argparse.Namespace) -> int:
    states = state_count(args.modulus)
    candidate = SeparationCandidate(
        lambda_value=args.lambda_value,
        mu_value=args.mu_value,
        potentials=tuple(0.0 for _ in range(states)),
    )
    report = scan_transition_violations(
        args.modulus,
        args.threshold,
        candidate,
        chunk_rows=args.chunk_rows,
        top_k=args.top_k,
    )
    _emit(report)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--chunk-rows", type=int, default=64)
    preflight.add_argument("--top-k", type=int, default=1000)
    preflight.set_defaults(handler=_preflight)
    toy = subparsers.add_parser("toy")
    toy.add_argument("--modulus", type=int, choices=(30, 210), default=30)
    toy.add_argument("--threshold", type=int, default=12)
    toy.add_argument("--lambda-value", type=float, default=0.0)
    toy.add_argument("--mu-value", type=float, default=0.0)
    toy.add_argument("--chunk-rows", type=int, default=3)
    toy.add_argument("--top-k", type=int, default=20)
    toy.set_defaults(handler=_toy)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except Exception as exc:
        _emit({"status": "FAIL", "error_type": type(exc).__name__, "message": str(exc)}, stream=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
