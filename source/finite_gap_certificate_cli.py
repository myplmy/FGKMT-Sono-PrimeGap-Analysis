"""Approval-gated CLI for P007 finite-range residue-state certificates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import mpmath
import numpy
import scipy

from source.finite_gap_certificate import (
    DEFAULT_H,
    DEFAULT_SOLVE_CONSTRAINT_CAP,
    SUPPLIED_CERTIFICATE_SHA256,
    read_certificate,
    run_discovery_comparison,
    run_supplied_certificate_audit,
    transition_resource_estimate,
    verify_saved_result,
)
from source.provenance import APPROVAL_TOKEN, sha256_file


EXPECTED_PYTHON = Path(r"W:\miniforge3\envs\FGKMT\python.exe")
DEFAULT_CERTIFICATE_PATH = Path(
    "ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt"
)
FULL_MODULI = (30, 210, 2310)


def _print(payload: object, *, stream: object = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=stream)


def _preflight(args: argparse.Namespace) -> int:
    certificate_path = Path(args.certificate_path)
    python_matches = (
        EXPECTED_PYTHON.is_file()
        and Path(sys.executable).resolve() == EXPECTED_PYTHON.resolve()
    )
    certificate_exists = certificate_path.is_file()
    certificate_hash = sha256_file(certificate_path) if certificate_exists else None
    certificate_parses = False
    supplied_certificate_verifies_shape = False
    if certificate_exists:
        try:
            certificate = read_certificate(certificate_path)
            certificate_parses = True
            supplied_certificate_verifies_shape = (
                certificate.modulus == 2310
                and certificate.threshold == DEFAULT_H
                and len(certificate.phi_num) == 480
            )
        except Exception:
            pass

    estimates = {
        str(modulus): transition_resource_estimate(
            modulus,
            DEFAULT_H,
            solve_constraint_cap=args.solve_constraint_cap,
        )
        for modulus in (*FULL_MODULI, 30030)
    }
    checks = {
        "python_executable_matches": python_matches,
        "certificate_exists": certificate_exists,
        "certificate_sha256_matches": certificate_hash
        == SUPPLIED_CERTIFICATE_SHA256,
        "certificate_parses": certificate_parses,
        "certificate_shape_matches_mod2310_H1856": supplied_certificate_verifies_shape,
        "numpy_available": bool(numpy.__version__),
        "scipy_available": bool(scipy.__version__),
        "mpmath_available": bool(mpmath.__version__),
        "full_small_moduli_within_constraint_guard": all(
            bool(estimates[str(modulus)]["solve_allowed_by_guard"])
            for modulus in FULL_MODULI
        ),
        "mod30030_blocked_by_constraint_guard": not bool(
            estimates["30030"]["solve_allowed_by_guard"]
        ),
        "gpu_disabled": True,
        "network_not_required": True,
    }
    payload = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "mode": args.mode,
        "checks": checks,
        "python_executable": sys.executable,
        "expected_python_executable": str(EXPECTED_PYTHON),
        "numpy_version": numpy.__version__,
        "scipy_version": scipy.__version__,
        "mpmath_version": mpmath.__version__,
        "certificate_path": str(certificate_path.resolve()),
        "certificate_sha256": certificate_hash,
        "expected_certificate_sha256": SUPPLIED_CERTIFICATE_SHA256,
        "resource_estimates": estimates,
        "actual_experiment_executed": False,
        "actual_prime_search_executed": False,
    }
    _print(payload)
    return 0 if payload["status"] == "PASS" else 1


def _audit(args: argparse.Namespace) -> int:
    token = APPROVAL_TOKEN if args.approved_by_user else None
    report = run_supplied_certificate_audit(
        Path(args.certificate_path),
        Path(args.output_directory),
        approval_token=token,
    )
    _print(report)
    return 0


def _compare(args: argparse.Namespace) -> int:
    token = APPROVAL_TOKEN if args.approved_by_user else None
    moduli = tuple(int(item) for item in args.moduli.split(","))
    report = run_discovery_comparison(
        moduli,
        Path(args.output_directory),
        approval_token=token,
        solve_constraint_cap=args.solve_constraint_cap,
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

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument(
        "--certificate-path", default=str(DEFAULT_CERTIFICATE_PATH)
    )
    preflight.add_argument("--mode", choices=("pilot", "full"), required=True)
    preflight.add_argument(
        "--solve-constraint-cap", type=int, default=DEFAULT_SOLVE_CONSTRAINT_CAP
    )
    preflight.set_defaults(handler=_preflight)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--certificate-path", required=True)
    audit.add_argument("--output-directory", required=True)
    audit.add_argument("--approved-by-user", action="store_true")
    audit.set_defaults(handler=_audit)

    compare = subparsers.add_parser("compare")
    compare.add_argument("--moduli", default=",".join(map(str, FULL_MODULI)))
    compare.add_argument("--output-directory", required=True)
    compare.add_argument(
        "--solve-constraint-cap", type=int, default=DEFAULT_SOLVE_CONSTRAINT_CAP
    )
    compare.add_argument("--approved-by-user", action="store_true")
    compare.set_defaults(handler=_compare)

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
            {
                "status": "FAIL",
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
            stream=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
