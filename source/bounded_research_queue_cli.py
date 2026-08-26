"""CLI for the user-authorized 50-GB/16-hour research queue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.bounded_research_queue import GB, run_bounded_queue
from source.provenance import APPROVAL_TOKEN


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-by-user", action="store_true")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--replay-manifest", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--max-wall-seconds", type=int, default=55_800)
    parser.add_argument("--max-disk-gb", type=int, default=50)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = run_bounded_queue(
        args.project_root,
        args.replay_manifest,
        args.output_directory,
        approval_token=APPROVAL_TOKEN if args.approved_by_user else None,
        max_wall_seconds=args.max_wall_seconds,
        max_disk_bytes=args.max_disk_gb * GB,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
