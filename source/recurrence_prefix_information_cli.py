"""CLI for approval-gated P018 blinded prefix information probes."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from importlib.metadata import version
from pathlib import Path

from source.live_progress import LiveProgressReporter
from source.provenance import APPROVAL_TOKEN, require_experiment_approval
from source.recurrence_prefix_information import (
    PROCESS_TREE_MEMORY_LIMIT_BYTES,
    run_prefix_probe,
    validate_prefix_inputs,
    verify_saved_prefix,
)
from source.runtime_resources import (
    configure_cpu_resources,
    configure_process_tree_memory_limit,
    plan_cpu_resources,
)


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), flush=True)


def _runtime_environment() -> dict[str, object]:
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "package_versions": {
            name: version(name)
            for name in ("numpy", "scipy", "mpmath", "gmpy2")
        },
    }


def _inputs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--mode", choices=("P0", "A"), required=True)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--ready-file", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--physical-cores", type=int, default=4)
    parser.add_argument("--logical-processors", type=int, default=8)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    preflight = sub.add_parser("preflight")
    _inputs(preflight)
    run = sub.add_parser("run")
    _inputs(run)
    run.add_argument("--approved-by-user", action="store_true")
    run.add_argument("--output-directory", type=Path, required=True)
    run.add_argument("--progress-log", type=Path, required=True)
    run.add_argument("--heartbeat-seconds", type=float, default=300.0)
    run.add_argument("--live-console", action="store_true")
    verify = sub.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "preflight":
        report = validate_prefix_inputs(
            args.records,
            args.contract,
            args.ready_file,
            args.project_root,
            mode=args.mode,
        )
        report["runtime_resource_plan"] = plan_cpu_resources(
            physical_cores=args.physical_cores,
            logical_processors=args.logical_processors,
        ).as_dict()
        report["runtime_environment"] = _runtime_environment()
        _emit(report)
        return 0
    if args.command == "verify":
        report = verify_saved_prefix(args.result_directory)
        if args.report is not None:
            if args.report.exists():
                raise FileExistsError(f"refusing to overwrite report: {args.report}")
            args.report.write_text(
                json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        _emit(report)
        return 0 if report["status"] == "PASS" else 1

    require_experiment_approval(APPROVAL_TOKEN if args.approved_by_user else None)
    resources = configure_cpu_resources(
        physical_cores=args.physical_cores,
        logical_processors=args.logical_processors,
    )
    resources["process_tree_memory_limit"] = configure_process_tree_memory_limit(
        limit_bytes=PROCESS_TREE_MEMORY_LIMIT_BYTES
    )
    resources["runtime_environment"] = _runtime_environment()
    print(
        "[RESOURCE] " + json.dumps(resources, ensure_ascii=False, sort_keys=True),
        flush=True,
    )
    with LiveProgressReporter(
        args.progress_log,
        experiment="P018_PREFIX_INFORMATION_PROBE",
        stage=args.mode,
        heartbeat_seconds=args.heartbeat_seconds,
        live_console=args.live_console,
    ) as progress:
        summary = run_prefix_probe(
            args.records,
            args.contract,
            args.ready_file,
            args.project_root,
            args.output_directory,
            mode=args.mode,
            approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
            worker_count=8,
            runtime_resource_policy=resources,
            progress_callback=progress.emit,
        )
    _emit(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
