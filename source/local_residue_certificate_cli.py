"""Approval-gated CLI for P008 local residue-state feasibility experiments."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source.finite_gap_certificate import (
    SUPPLIED_CERTIFICATE_SHA256,
    read_certificate,
    verify_certificate,
)
from source.local_residue_certificate import (
    run_local_experiment,
    validate_prime_count_metadata,
    verify_saved_result,
)
from source.provenance import APPROVAL_TOKEN, sha256_file


EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")
DEFAULT_CERTIFICATE = Path(
    "ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt"
)


def _print(payload: object, *, stream: object = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=stream)


def _preflight(args: argparse.Namespace) -> int:
    path = Path(args.certificate_path)
    checks: dict[str, bool] = {
        "fixed_python": EXPECTED_PYTHON.is_file()
        and Path(sys.executable).resolve() == EXPECTED_PYTHON.resolve(),
        "certificate_exists": path.is_file(),
        "certificate_hash_pinned": path.is_file()
        and sha256_file(path) == SUPPLIED_CERTIFICATE_SHA256,
        "gpu_disabled": True,
        "candidate_cover_not_claimed": True,
        "representative_sweep_not_coverage_ledger": True,
    }
    if path.is_file():
        certificate = read_certificate(path)
        checks["certificate_exact_global_audit"] = (
            verify_certificate(certificate)["status"] == "PASS"
        )
    if args.mode == "full":
        counts_path = Path(args.counts_path) if args.counts_path else None
        metadata_path = (
            Path(args.count_metadata_path) if args.count_metadata_path else None
        )
        checks["counts_file_exists"] = bool(counts_path and counts_path.is_file())
        checks["count_metadata_exists"] = bool(
            metadata_path and metadata_path.is_file()
        )
        checks["count_metadata_contract"] = False
        if checks["counts_file_exists"] and checks["count_metadata_exists"]:
            try:
                validate_prime_count_metadata(metadata_path, counts_path)
            except (OSError, ValueError):
                pass
            else:
                checks["count_metadata_contract"] = True
    payload = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "mode": args.mode,
        "checks": checks,
        "python": sys.executable,
        "actual_experiment_executed": False,
    }
    _print(payload)
    return 0 if payload["status"] == "PASS" else 1


def _run(args: argparse.Namespace) -> int:
    token = APPROVAL_TOKEN if args.approved_by_user else None
    report = run_local_experiment(
        Path(args.certificate_path),
        Path(args.output_directory),
        mode=args.mode,
        approval_token=token,
        counts_path=Path(args.counts_path) if args.counts_path else None,
        count_metadata_path=(
            Path(args.count_metadata_path) if args.count_metadata_path else None
        ),
    )
    _print(report)
    return 0


def _verify(args: argparse.Namespace) -> int:
    report = verify_saved_result(Path(args.result_directory))
    _print(report)
    return 0 if report["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("preflight", "run"):
        child = subparsers.add_parser(command)
        child.add_argument("--mode", choices=("pilot", "full"), required=True)
        child.add_argument("--certificate-path", default=str(DEFAULT_CERTIFICATE))
        child.add_argument("--counts-path")
        child.add_argument("--count-metadata-path")
        if command == "run":
            child.add_argument("--output-directory", required=True)
            child.add_argument("--approved-by-user", action="store_true")
            child.set_defaults(handler=_run)
        else:
            child.set_defaults(handler=_preflight)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--result-directory", required=True)
    verify.set_defaults(handler=_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except Exception as exc:
        _print(
            {"status": "FAIL", "error_type": type(exc).__name__, "message": str(exc)},
            stream=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
