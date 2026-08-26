"""CLI for the approval-gated P010A G4 cutting-plane experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.finite_gap_cutting_plane import (
    cutting_plane_preflight,
    run_cutting_plane_experiment,
    verify_saved_cutting_plane,
)
from source.provenance import APPROVAL_TOKEN


def _print(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _preflight(args: argparse.Namespace) -> int:
    _print(cutting_plane_preflight(Path(args.exact_lift_manifest)))
    return 0


def _run(args: argparse.Namespace) -> int:
    summary = run_cutting_plane_experiment(
        Path(args.exact_lift_manifest),
        Path(args.output_directory),
        approval_token=(APPROVAL_TOKEN if args.approved_by_user else None),
        max_wall_seconds=args.max_wall_seconds,
        per_solve_time_limit_seconds=args.per_solve_time_limit_seconds,
        max_iterations=args.max_iterations,
        seed_constraint_count=args.seed_constraint_count,
        add_per_iteration=args.add_per_iteration,
        max_working_constraints=args.max_working_constraints,
        max_disk_bytes=args.max_disk_bytes,
        chunk_rows=args.chunk_rows,
        progress_callback=lambda payload: print(
            "[CUT] " + json.dumps(payload, ensure_ascii=False, sort_keys=True),
            flush=True,
        ),
    )
    _print(summary)
    return 0


def _verify(args: argparse.Namespace) -> int:
    report = verify_saved_cutting_plane(Path(args.result_directory))
    if args.report:
        path = Path(args.report)
        if path.exists():
            raise FileExistsError(f"refusing to overwrite verification report: {path}")
        path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    _print(report)
    return 0 if report["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P010A modulus-30030 memory-bounded cutting-plane CLI."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--exact-lift-manifest", required=True)
    preflight.set_defaults(handler=_preflight)

    run = subparsers.add_parser("run")
    run.add_argument("--approved-by-user", action="store_true")
    run.add_argument("--exact-lift-manifest", required=True)
    run.add_argument("--output-directory", required=True)
    run.add_argument("--max-wall-seconds", type=int, default=39_600)
    run.add_argument("--per-solve-time-limit-seconds", type=int, default=3_600)
    run.add_argument("--max-iterations", type=int, default=100)
    run.add_argument("--seed-constraint-count", type=int, default=20_000)
    run.add_argument("--add-per-iteration", type=int, default=10_000)
    run.add_argument("--max-working-constraints", type=int, default=250_000)
    run.add_argument("--max-disk-bytes", type=int, default=50_000_000_000)
    run.add_argument("--chunk-rows", type=int, default=64)
    run.set_defaults(handler=_run)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", required=True)
    verify.add_argument("--report")
    verify.set_defaults(handler=_verify)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
