"""Command-line entry points for the P009 PARI/GP adapter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.pari_certificate import (
    DEFAULT_TIMEOUT_SECONDS,
    generate_certificate_bundle,
    probe_gp_version,
    run_adapter_validation,
    verify_certificate_file,
    verify_saved_adapter_validation,
)
from source.provenance import APPROVAL_TOKEN, require_experiment_approval


def _print(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("preflight")

    validation = subparsers.add_parser("validate-adapter")
    validation.add_argument("--approved-by-user", action="store_true")
    validation.add_argument("--output-directory", type=Path, required=True)
    validation.add_argument(
        "--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS
    )

    saved_validation = subparsers.add_parser("verify-adapter")
    saved_validation.add_argument("--result-directory", type=Path, required=True)
    saved_validation.add_argument("--report", type=Path)
    saved_validation.add_argument(
        "--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS
    )

    generation = subparsers.add_parser("generate")
    generation.add_argument("--approved-by-user", action="store_true")
    generation.add_argument("--subject", type=int, required=True)
    generation.add_argument("--output-directory", type=Path, required=True)
    generation.add_argument(
        "--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS
    )

    verification = subparsers.add_parser("verify")
    verification.add_argument("--certificate", type=Path, required=True)
    verification.add_argument("--subject", type=int, required=True)
    verification.add_argument("--expected-sha256")
    verification.add_argument(
        "--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "preflight":
        _print(
            {
                "status": "PASS",
                "scope": "P009 PARI adapter static preflight",
                "gp_version": probe_gp_version(),
                "actual_1e20_experiment_executed": False,
            }
        )
        return 0
    if args.command == "validate-adapter":
        require_experiment_approval(
            APPROVAL_TOKEN if args.approved_by_user else None
        )
        _print(
            run_adapter_validation(
                args.output_directory, timeout_seconds=args.timeout_seconds
            )
        )
        return 0
    if args.command == "generate":
        require_experiment_approval(
            APPROVAL_TOKEN if args.approved_by_user else None
        )
        _print(
            generate_certificate_bundle(
                args.subject,
                args.output_directory,
                timeout_seconds=args.timeout_seconds,
            )
        )
        return 0
    if args.command == "verify-adapter":
        report = verify_saved_adapter_validation(
            args.result_directory, timeout_seconds=args.timeout_seconds
        )
        if args.report is not None:
            if args.report.exists():
                raise FileExistsError(f"refusing to overwrite report: {args.report}")
            with args.report.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
        _print(report)
        return 0 if report["status"] == "PASS" else 1
    report = verify_certificate_file(
        args.certificate,
        args.subject,
        expected_sha256=args.expected_sha256,
        timeout_seconds=args.timeout_seconds,
        gp_version=probe_gp_version(),
    )
    _print(report.__dict__)
    return 0 if report.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
