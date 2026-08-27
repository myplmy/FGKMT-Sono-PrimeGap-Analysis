"""CLI for the approval-gated P015 48-hour independent research queue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.independent_research_queue import GB, run_queue, verify_saved_queue
from source.provenance import APPROVAL_TOKEN


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--approved-by-user", action="store_true")
    run.add_argument("--project-root", type=Path, required=True)
    run.add_argument("--output-directory", type=Path, required=True)
    run.add_argument("--max-wall-seconds", type=int, default=169_200)
    run.add_argument("--max-disk-gb", type=int, default=50)
    verify = sub.add_parser("verify")
    verify.add_argument("--result-directory", type=Path, required=True)
    verify.add_argument("--report", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "run":
        report = run_queue(
            args.project_root,
            args.output_directory,
            approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
            max_wall_seconds=args.max_wall_seconds,
            max_disk_bytes=args.max_disk_gb * GB,
        )
    else:
        report = verify_saved_queue(args.result_directory)
        if args.report is not None:
            if args.report.exists():
                raise FileExistsError(f"refusing to overwrite report: {args.report}")
            args.report.write_text(
                json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
