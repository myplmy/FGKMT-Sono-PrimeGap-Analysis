"""CLI for approval-gated P013 prospective recurrence extensions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.provenance import APPROVAL_TOKEN
from source.recurrence_sequential_extension import (
    DEFAULT_SEGMENT_SPAN,
    run_extension,
    validate_inputs,
    verify_saved_extension,
)
from source.runtime_resources import configure_cpu_resources, plan_cpu_resources


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--stage", choices=("A", "B"), required=True)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--p012-contract", type=Path, required=True)
    parser.add_argument("--p013-contract", type=Path, required=True)
    parser.add_argument("--p012b-manifest", type=Path, required=True)
    parser.add_argument("--p012b-saved-report", type=Path, required=True)
    parser.add_argument("--segment-span", type=int, default=DEFAULT_SEGMENT_SPAN)
    parser.add_argument("--physical-cores", type=int, default=4)
    parser.add_argument("--logical-processors", type=int, default=8)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    preflight = sub.add_parser("preflight")
    _common(preflight)
    analyze = sub.add_parser("analyze")
    _common(analyze)
    analyze.add_argument("--approved-by-user", action="store_true")
    analyze.add_argument("--output-directory", type=Path, required=True)
    analyze.add_argument("--checkpoint-path", type=Path)
    verify = sub.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    verify.add_argument("--physical-cores", type=int, default=4)
    verify.add_argument("--logical-processors", type=int, default=8)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "preflight":
        report = validate_inputs(
            args.records,
            args.p012_contract,
            args.p013_contract,
            args.p012b_manifest,
            args.p012b_saved_report,
            stage=args.stage,
            segment_span=args.segment_span,
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
    print(
        "[RESOURCE] "
        + json.dumps(resource_policy, ensure_ascii=False, sort_keys=True),
        flush=True,
    )
    if args.command == "analyze":
        _emit(
            run_extension(
                args.records,
                args.p012_contract,
                args.p013_contract,
                args.p012b_manifest,
                args.p012b_saved_report,
                args.output_directory,
                stage=args.stage,
                approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
                segment_span=args.segment_span,
                checkpoint_path=args.checkpoint_path,
                runtime_resource_policy=resource_policy,
                progress_callback=lambda payload: print(
                    "[P013] "
                    + json.dumps(payload, ensure_ascii=False, sort_keys=True),
                    flush=True,
                ),
            )
        )
        return 0
    report = verify_saved_extension(args.result_directory)
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
