"""CLI for P010A replay and gated P010B one-candidate scan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source.finite_gap_replay import (
    run_mod2310_replay,
    run_mod30030_exact_lift,
    run_mod30030_one_candidate_scan,
    verify_saved_mod2310_replay,
    verify_saved_mod30030_scan,
    verify_saved_mod30030_exact_lift,
)
from source.provenance import APPROVAL_TOKEN


def _print(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--certificate", type=Path, required=True)

    replay = subparsers.add_parser("replay-2310")
    replay.add_argument("--approved-by-user", action="store_true")
    replay.add_argument("--certificate", type=Path, required=True)
    replay.add_argument("--output-directory", type=Path, required=True)
    replay.add_argument("--chunk-rows", type=int, default=64)
    replay.add_argument("--top-k", type=int, default=100)

    replay_verify = subparsers.add_parser("verify-replay")
    replay_verify.add_argument("--result-directory", type=Path, required=True)
    replay_verify.add_argument("--report", type=Path)

    scan = subparsers.add_parser("scan-30030")
    scan.add_argument("--approved-by-user", action="store_true")
    scan.add_argument("--certificate", type=Path, required=True)
    scan.add_argument("--replay-manifest", type=Path, required=True)
    scan.add_argument("--output-directory", type=Path, required=True)
    scan.add_argument("--chunk-rows", type=int, default=64)
    scan.add_argument("--top-k", type=int, default=1000)

    scan_verify = subparsers.add_parser("verify-scan")
    scan_verify.add_argument("--result-directory", type=Path, required=True)
    scan_verify.add_argument("--report", type=Path)

    exact_lift = subparsers.add_parser("lift-30030-exact")
    exact_lift.add_argument("--approved-by-user", action="store_true")
    exact_lift.add_argument("--certificate", type=Path, required=True)
    exact_lift.add_argument("--replay-manifest", type=Path, required=True)
    exact_lift.add_argument("--scan-manifest", type=Path, required=True)
    exact_lift.add_argument("--output-directory", type=Path, required=True)
    exact_lift.add_argument("--chunk-rows", type=int, default=64)

    exact_lift_verify = subparsers.add_parser("verify-lift")
    exact_lift_verify.add_argument("--result-directory", type=Path, required=True)
    exact_lift_verify.add_argument("--report", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "preflight":
        from source.finite_gap_certificate import read_certificate
        from source.finite_gap_replay import P007_MOD2310_CERTIFICATE_SHA256
        from source.provenance import sha256_file

        certificate = read_certificate(args.certificate)
        certificate_hash = sha256_file(args.certificate)
        payload = {
            "status": "PASS"
            if certificate.modulus == 2310
            and certificate_hash == P007_MOD2310_CERTIFICATE_SHA256
            else "FAIL",
            "modulus": certificate.modulus,
            "certificate_sha256": certificate_hash,
            "expected_sha256": P007_MOD2310_CERTIFICATE_SHA256,
            "actual_replay_executed": False,
            "mod30030_scan_executed": False,
        }
        _print(payload)
        return 0 if payload["status"] == "PASS" else 1
    if args.command == "replay-2310":
        _print(
            run_mod2310_replay(
                args.certificate,
                args.output_directory,
                approval_token=(
                    APPROVAL_TOKEN if args.approved_by_user else None
                ),
                chunk_rows=args.chunk_rows,
                top_k=args.top_k,
            )
        )
        return 0
    if args.command == "verify-replay":
        report = verify_saved_mod2310_replay(args.result_directory)
        if args.report is not None:
            if args.report.exists():
                raise FileExistsError(f"refusing to overwrite report: {args.report}")
            with args.report.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
        _print(report)
        return 0 if report["status"] == "PASS" else 1
    if args.command == "scan-30030":
        _print(
            run_mod30030_one_candidate_scan(
                args.certificate,
                args.replay_manifest,
                args.output_directory,
                approval_token=(
                    APPROVAL_TOKEN if args.approved_by_user else None
                ),
                chunk_rows=args.chunk_rows,
                top_k=args.top_k,
            )
        )
        return 0
    if args.command == "lift-30030-exact":
        _print(
            run_mod30030_exact_lift(
                args.certificate,
                args.replay_manifest,
                args.scan_manifest,
                args.output_directory,
                approval_token=(APPROVAL_TOKEN if args.approved_by_user else None),
                chunk_rows=args.chunk_rows,
            )
        )
        return 0
    if args.command == "verify-lift":
        report = verify_saved_mod30030_exact_lift(args.result_directory)
    else:
        report = verify_saved_mod30030_scan(args.result_directory)
    if args.report is not None:
        if args.report.exists():
            raise FileExistsError(f"refusing to overwrite report: {args.report}")
        with args.report.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    _print(report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
