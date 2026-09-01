"""Parallel-first exact cross-check when no full serial oracle exists.

The two passes use different coprime segment counts and independently repeat
the complete prime-range scan.  Equality catches partition, boundary, merge,
and nondeterministic execution errors.  It does not make the shared sieve and
accumulator kernels independent, so an exact externally certified prime-count
difference remains mandatory.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

from source.parallel_segment_statistics import (
    ParallelSegmentError,
    exact_statistics_core,
    parallel_accumulate_bin_counts,
    partition_integer_range,
)


class DualPartitionVerificationError(RuntimeError):
    """Raised when the two full parallel passes cannot certify one another."""


def _validate_execution(
    payload: dict[str, object],
    *,
    worker_count: int,
    segment_count: int,
) -> dict[str, object]:
    execution = payload.get("parallel_execution")
    if not isinstance(execution, dict):
        raise DualPartitionVerificationError("parallel execution metadata is missing")
    expected = {
        "worker_count_requested": worker_count,
        "worker_count_observed": worker_count,
        "segment_count": segment_count,
        "adjacent_boundary_checks": segment_count - 1,
        "prime_arrays_transferred_between_processes": False,
        "exact_integer_merge": True,
        "worker_native_thread_ceiling": 1,
        "all_worker_native_thread_limits_one": True,
    }
    for name, value in expected.items():
        if execution.get(name) != value:
            raise DualPartitionVerificationError(
                f"parallel execution contract mismatch: {name}"
            )
    segments = execution.get("segments")
    if not isinstance(segments, list) or len(segments) != segment_count:
        raise DualPartitionVerificationError("segment coverage metadata is incomplete")
    return execution


def dual_partition_accumulate_bin_counts(
    lower_inclusive: int,
    upper_exclusive: int,
    plateaus: Sequence[dict[str, int]],
    *,
    expected_gap_start_count: int,
    worker_count: int,
    primary_segment_count: int,
    verifier_segment_count: int,
    primary_sieve_segment_span: int = 50_000,
    verifier_sieve_segment_span: int = 47_003,
    start_method: str = "spawn",
    progress_callback: Callable[[dict[str, object]], None] | None = None,
    deadline_monotonic: float | None = None,
) -> dict[str, object]:
    """Repeat a complete exact scan under two different parallel partitions."""

    if expected_gap_start_count < 0:
        raise ValueError("expected_gap_start_count must be nonnegative")
    if primary_segment_count < 2 or verifier_segment_count < 2:
        raise ValueError("both segment counts must be at least two")
    if primary_segment_count == verifier_segment_count:
        raise ValueError("primary and verifier segment counts must differ")
    if math.gcd(primary_segment_count, verifier_segment_count) != 1:
        raise ValueError("primary and verifier segment counts must be coprime")

    primary_specs = partition_integer_range(
        lower_inclusive,
        upper_exclusive,
        segment_count=primary_segment_count,
    )
    verifier_specs = partition_integer_range(
        lower_inclusive,
        upper_exclusive,
        segment_count=verifier_segment_count,
    )
    primary_boundaries = {
        spec.upper_exclusive for spec in primary_specs[:-1]
    }
    verifier_boundaries = {
        spec.upper_exclusive for spec in verifier_specs[:-1]
    }
    if primary_boundaries == verifier_boundaries:
        raise DualPartitionVerificationError("partition boundary sets are identical")

    def progress(pass_name: str):
        if progress_callback is None:
            return None

        def emit(payload: dict[str, object]) -> None:
            progress_callback({"dual_partition_pass": pass_name, **payload})

        return emit

    try:
        primary = parallel_accumulate_bin_counts(
            lower_inclusive,
            upper_exclusive,
            plateaus,
            worker_count=worker_count,
            segment_count=primary_segment_count,
            sieve_segment_span=primary_sieve_segment_span,
            start_method=start_method,
            progress_callback=progress("primary"),
            deadline_monotonic=deadline_monotonic,
        )
        verifier = parallel_accumulate_bin_counts(
            lower_inclusive,
            upper_exclusive,
            plateaus,
            worker_count=worker_count,
            segment_count=verifier_segment_count,
            sieve_segment_span=verifier_sieve_segment_span,
            start_method=start_method,
            progress_callback=progress("verifier"),
            deadline_monotonic=deadline_monotonic,
        )
    except ParallelSegmentError as exc:
        raise DualPartitionVerificationError(str(exc)) from exc

    primary_execution = _validate_execution(
        primary,
        worker_count=worker_count,
        segment_count=primary_segment_count,
    )
    verifier_execution = _validate_execution(
        verifier,
        worker_count=worker_count,
        segment_count=verifier_segment_count,
    )
    primary_core = exact_statistics_core(primary)
    verifier_core = exact_statistics_core(verifier)
    if primary_core != verifier_core:
        raise DualPartitionVerificationError(
            "parallel passes disagree on exact sufficient statistics"
        )
    if int(primary_core["gap_count"]) != expected_gap_start_count:
        raise DualPartitionVerificationError(
            "parallel gap count differs from independently certified pi difference"
        )
    if int(primary_core["prime_count"]) != expected_gap_start_count + 1:
        raise DualPartitionVerificationError(
            "boundary-closed prime count differs from expected gap count plus one"
        )

    return {
        "status": "PASS",
        "serial_oracle_used": False,
        "full_parallel_passes": 2,
        "exact_statistics_equal": True,
        "expected_gap_start_count": expected_gap_start_count,
        "independent_endpoint_prime_count_required": True,
        "common_sieve_and_accumulator_kernel_risk_acknowledged": True,
        "work_items_omitted": False,
        "precision_reduced": False,
        "statistics": primary_core,
        "verification": {
            "primary_segment_count": primary_segment_count,
            "verifier_segment_count": verifier_segment_count,
            "segment_counts_coprime": True,
            "interior_boundary_overlap_count": len(
                primary_boundaries & verifier_boundaries
            ),
            "primary_adjacent_boundary_checks": primary_execution[
                "adjacent_boundary_checks"
            ],
            "verifier_adjacent_boundary_checks": verifier_execution[
                "adjacent_boundary_checks"
            ],
            "primary_worker_count_observed": primary_execution[
                "worker_count_observed"
            ],
            "verifier_worker_count_observed": verifier_execution[
                "worker_count_observed"
            ],
            "worker_native_thread_ceiling": 1,
        },
    }


__all__ = [
    "DualPartitionVerificationError",
    "dual_partition_accumulate_bin_counts",
]
