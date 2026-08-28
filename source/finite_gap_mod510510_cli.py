"""CLI for the approval-gated P014 modulus-510510 staged experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.finite_gap_mod510510 import preflight, run_staged_experiment, verify_saved_experiment
from source.live_progress import LiveProgressReporter
from source.provenance import APPROVAL_TOKEN, require_experiment_approval
from source.runtime_resources import configure_cpu_resources, plan_cpu_resources


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("preflight")
    check.add_argument("--g4-result-directory", type=Path, required=True)
    check.add_argument("--chunk-rows", type=int, default=64)
    check.add_argument("--physical-cores", type=int, default=4)
    check.add_argument("--logical-processors", type=int, default=8)
    run = sub.add_parser("run")
    run.add_argument("--approved-by-user", action="store_true")
    run.add_argument("--g4-result-directory", type=Path, required=True)
    run.add_argument("--output-directory", type=Path, required=True)
    run.add_argument("--max-wall-seconds", type=int, default=54_000)
    run.add_argument("--stage-a-gate-seconds", type=int, default=14_400)
    run.add_argument("--per-solve-time-limit-seconds", type=int, default=1_800)
    run.add_argument("--max-iterations", type=int, default=12)
    run.add_argument("--seed-constraint-count", type=int, default=5_000)
    run.add_argument("--add-per-iteration", type=int, default=5_000)
    run.add_argument("--max-working-constraints", type=int, default=100_000)
    run.add_argument("--max-disk-bytes", type=int, default=10_000_000_000)
    run.add_argument("--chunk-rows", type=int, default=64)
    run.add_argument("--physical-cores", type=int, default=4)
    run.add_argument("--logical-processors", type=int, default=8)
    run.add_argument("--progress-log", type=Path)
    run.add_argument("--heartbeat-seconds", type=float, default=300.0)
    run.add_argument("--live-console", action="store_true")
    verify = sub.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    verify.add_argument("--chunk-rows", type=int, default=64)
    verify.add_argument("--physical-cores", type=int, default=4)
    verify.add_argument("--logical-processors", type=int, default=8)
    verify.add_argument("--progress-log", type=Path)
    verify.add_argument("--heartbeat-seconds", type=float, default=300.0)
    verify.add_argument("--live-console", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "preflight":
        report = preflight(args.g4_result_directory, chunk_rows=args.chunk_rows)
        report["runtime_resource_plan"] = plan_cpu_resources(
            physical_cores=args.physical_cores,
            logical_processors=args.logical_processors,
        ).as_dict()
        _emit(report)
        return 0
    if args.command == "run":
        # Refuse before resource changes or progress-log creation.
        require_experiment_approval(
            APPROVAL_TOKEN if args.approved_by_user else None
        )
    resource_policy = configure_cpu_resources(
        physical_cores=args.physical_cores,
        logical_processors=args.logical_processors,
    )
    print(
        "[RESOURCE] "
        + json.dumps(resource_policy, ensure_ascii=False, sort_keys=True),
        flush=True,
    )
    if args.command == "run":
        def execute_run(progress_callback):
            return run_staged_experiment(
                args.g4_result_directory,
                args.output_directory,
                approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
                max_wall_seconds=args.max_wall_seconds,
                stage_a_gate_seconds=args.stage_a_gate_seconds,
                per_solve_time_limit_seconds=args.per_solve_time_limit_seconds,
                max_iterations=args.max_iterations,
                seed_constraint_count=args.seed_constraint_count,
                add_per_iteration=args.add_per_iteration,
                max_working_constraints=args.max_working_constraints,
                max_disk_bytes=args.max_disk_bytes,
                chunk_rows=args.chunk_rows,
                runtime_resource_policy=resource_policy,
                progress_callback=progress_callback,
            )

        if args.progress_log is None:
            progress_callback = lambda payload: print(
                "[P014] " + json.dumps(payload, ensure_ascii=False, sort_keys=True),
                flush=True,
            )
            summary = execute_run(progress_callback)
        else:
            with LiveProgressReporter(
                args.progress_log,
                experiment="P014_MOD510510_STAGED_CERTIFICATE",
                stage="analysis",
                heartbeat_seconds=args.heartbeat_seconds,
                live_console=args.live_console,
            ) as progress_context:
                progress_context.emit(
                    {"stage": "resource_policy", "policy": resource_policy}
                )
                summary = execute_run(progress_context.emit)
                progress_context.emit({"stage": "analysis", "status": "PASS"})
        _emit(summary)
        return 0
    if args.progress_log is None:
        verify_progress = None
        report = verify_saved_experiment(args.result_directory, chunk_rows=args.chunk_rows)
    else:
        with LiveProgressReporter(
            args.progress_log,
            experiment="P014_MOD510510_STAGED_CERTIFICATE",
            stage="saved_full_exact_recomputation",
            heartbeat_seconds=args.heartbeat_seconds,
            live_console=args.live_console,
        ) as verify_progress:
            verify_progress.emit({"stage": "verification", "status": "STARTED"})
            report = verify_saved_experiment(
                args.result_directory,
                chunk_rows=args.chunk_rows,
                progress_callback=verify_progress.emit,
            )
            verify_progress.emit(
                {"stage": "verification", "status": str(report["status"])}
            )
    if args.report is not None:
        if args.report.exists():
            raise FileExistsError(f"refusing to overwrite report: {args.report}")
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    _emit(report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
