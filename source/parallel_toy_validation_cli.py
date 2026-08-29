"""Run the P013/P014 process-parallel exactness toys without actual data."""

from __future__ import annotations

import argparse
import json

from source.runtime_resources import configure_cpu_resources


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("--workers must be in [1, 8] for this reviewed toy")
    resource = configure_cpu_resources(physical_cores=4, logical_processors=8)

    from source.finite_gap_certificate import RationalCertificate, state_count
    from source.finite_gap_parallel_exact_scan import (
        exact_scan_core,
        parallel_scan_exact_certificate_constraints,
    )
    from source.finite_gap_separation import scan_exact_certificate_constraints
    from source.parallel_segment_statistics import (
        exact_statistics_core,
        parallel_accumulate_bin_counts,
    )
    from source.recurrence_stratified_holdout import iter_prime_chunks_range
    from source.recurrence_stratified_null import accumulate_bin_counts

    plateaus = [
        {
            "record_index": 1,
            "start_prime": 100_003,
            "right_exclusive": 500_009,
            "gap": 6,
        },
        {
            "record_index": 2,
            "start_prime": 500_009,
            "right_exclusive": 999_983,
            "gap": 8,
        },
    ]
    serial_counts = accumulate_bin_counts(
        iter_prime_chunks_range(100_000, 1_000_003, segment_span=50_003),
        plateaus,
    )
    parallel_counts = parallel_accumulate_bin_counts(
        100_000,
        1_000_003,
        plateaus,
        worker_count=args.workers,
        segment_count=32,
        sieve_segment_span=25_003,
    )
    p013_equal = exact_statistics_core(parallel_counts) == exact_statistics_core(
        serial_counts
    )

    # A synthetic modulus-30030 certificate keeps all eight workers busy long
    # enough to observe real process participation.  It is not the pinned P014
    # research certificate and cannot change the count bound.
    modulus = 30_030
    certificate = RationalCertificate(
        modulus=modulus,
        threshold=1_856,
        denominator=100,
        lambda_num=2,
        mu_num=100,
        t_num=5,
        phi_num=tuple(
            (index % 11) - 5 for index in range(state_count(modulus))
        ),
        internal_bound=0,
        total_bound=0,
    )
    serial_scan = scan_exact_certificate_constraints(
        certificate,
        chunk_rows=256,
        top_k=25,
        allow_large_state_scan=True,
    )
    parallel_scan = parallel_scan_exact_certificate_constraints(
        certificate,
        worker_count=args.workers,
        row_block_rows=256,
        top_k=25,
        allow_large_state_scan=True,
    )
    p014_equal = exact_scan_core(parallel_scan) == exact_scan_core(serial_scan)

    payload = {
        "status": "PASS" if p013_equal and p014_equal else "FAIL",
        "actual_experiment_executed": False,
        "resource_policy": resource,
        "p013": {
            "serial_parallel_exact_equal": p013_equal,
            "gap_count": int(parallel_counts["gap_count"]),
            "segment_count": int(
                parallel_counts["parallel_execution"]["segment_count"]
            ),
            "worker_processes_observed": len(
                parallel_counts["parallel_execution"]["worker_pids"]
            ),
            "all_worker_native_thread_limits_one": parallel_counts[
                "parallel_execution"
            ]["all_worker_native_thread_limits_one"],
        },
        "p014": {
            "serial_parallel_exact_equal": p014_equal,
            "scanned_constraints": int(parallel_scan["scanned_constraints"]),
            "worker_processes_observed": len(
                parallel_scan["parallel_execution"]["worker_pids"]
            ),
            "all_worker_native_thread_limits_one": parallel_scan[
                "parallel_execution"
            ]["all_worker_native_thread_limits_one"],
        },
        "precision_reduced": False,
        "work_items_omitted": False,
        "actual_runner_promoted": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
