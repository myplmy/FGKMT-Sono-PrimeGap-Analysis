"""CLI for the approval-gated P017 P013 parallel calibration."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from source.provenance import APPROVAL_TOKEN
from source.recurrence_parallel_calibration import (
    MODES,
    run_calibration,
    validate_calibration_inputs,
    verify_saved_calibration,
)
from source.runtime_resources import (
    THREAD_ENVIRONMENT_VARIABLES,
    configure_cpu_resources,
    plan_cpu_resources,
)


def _inputs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--p012-contract", type=Path, required=True)
    parser.add_argument("--p013-contract", type=Path, required=True)
    parser.add_argument("--p012b-manifest", type=Path, required=True)
    parser.add_argument("--p012b-saved-report", type=Path, required=True)
    parser.add_argument("--calibration-contract", type=Path, required=True)
    parser.add_argument("--oracle-root", type=Path, required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    preflight = sub.add_parser("preflight")
    _inputs(preflight)
    preflight.add_argument("--physical-cores", type=int, default=4)
    preflight.add_argument("--logical-processors", type=int, default=8)
    run = sub.add_parser("run")
    _inputs(run)
    run.add_argument("--approved-by-user", action="store_true")
    run.add_argument("--output-directory", type=Path, required=True)
    run.add_argument("--physical-cores", type=int, default=4)
    run.add_argument("--logical-processors", type=int, default=8)
    verify = sub.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    return parser


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), flush=True)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "verify":
        report = verify_saved_calibration(args.result_directory)
        if args.report is not None:
            if args.report.exists():
                raise FileExistsError(f"refusing to overwrite report: {args.report}")
            args.report.write_text(
                json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        _emit(report)
        return 0 if report["status"] == "PASS" else 1
    if args.command == "preflight":
        report = validate_calibration_inputs(
            args.records,
            args.p012_contract,
            args.p013_contract,
            args.p012b_manifest,
            args.p012b_saved_report,
            args.calibration_contract,
            args.oracle_root,
            mode=args.mode,
        )
        report["runtime_resource_plan"] = plan_cpu_resources(
            physical_cores=args.physical_cores,
            logical_processors=args.logical_processors,
        ).as_dict()
        _emit(report)
        return 0
    resource_policy = configure_cpu_resources(
        physical_cores=args.physical_cores,
        logical_processors=args.logical_processors,
    )
    coordinator_limits = dict(resource_policy["thread_pool_limits"])
    for name in THREAD_ENVIRONMENT_VARIABLES:
        os.environ[name] = "1"
    resource_policy["coordinator_initial_thread_pool_limits"] = coordinator_limits
    resource_policy["spawned_worker_thread_pool_limits"] = {
        name: os.environ[name] for name in THREAD_ENVIRONMENT_VARIABLES
    }
    print(
        "[RESOURCE] " + json.dumps(resource_policy, ensure_ascii=False, sort_keys=True),
        flush=True,
    )
    report = run_calibration(
        args.records,
        args.p012_contract,
        args.p013_contract,
        args.p012b_manifest,
        args.p012b_saved_report,
        args.calibration_contract,
        args.oracle_root,
        args.output_directory,
        mode=args.mode,
        approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
        runtime_resource_policy=resource_policy,
    )
    _emit(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
