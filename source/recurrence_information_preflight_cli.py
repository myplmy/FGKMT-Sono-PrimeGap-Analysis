"""CLI for the read-only P013 expected-information/power preflight."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.recurrence_information_preflight import (
    build_preflight_report,
    load_stage_information,
)


def _stage_argument(value: str) -> tuple[str, Path]:
    label, separator, raw_path = value.partition("=")
    if not separator or not label or not raw_path:
        raise argparse.ArgumentTypeError("stage must use LABEL=RESULT_DIRECTORY")
    return label, Path(raw_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="append", type=_stage_argument, required=True)
    parser.add_argument("--decision-stage-label", required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    stages = [
        load_stage_information(path, label=label) for label, path in args.stage
    ]
    report = build_preflight_report(
        stages, decision_stage_label=args.decision_stage_label
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite preflight report: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
