"""Exact process-parallel sufficient statistics for P013-style prime ranges.

This module is an isolated toy revision.  It does not replace the serial P013
pipeline.  Every worker owns the gap starts in one half-open integer segment
``[lower, upper)`` and includes exactly one prime at or above ``upper`` so the
last crossing gap is closed.  Workers return only integer sufficient
statistics; prime arrays never cross the process boundary.
"""

from __future__ import annotations

import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Iterable, Sequence

class ParallelSegmentError(RuntimeError):
    """Raised when segment coverage or deterministic merge invariants fail."""


@dataclass(frozen=True, slots=True)
class SegmentSpec:
    index: int
    lower_inclusive: int
    upper_exclusive: int


def partition_integer_range(
    lower_inclusive: int,
    upper_exclusive: int,
    *,
    segment_count: int,
) -> tuple[SegmentSpec, ...]:
    """Partition an integer range into nonempty, contiguous half-open pieces."""

    if not (2 < lower_inclusive < upper_exclusive):
        raise ValueError("range must satisfy 2 < lower < upper")
    width = upper_exclusive - lower_inclusive
    if not 1 <= segment_count <= width:
        raise ValueError("segment_count must be in [1, range width]")
    boundaries = [
        lower_inclusive + (width * index) // segment_count
        for index in range(segment_count + 1)
    ]
    specs = tuple(
        SegmentSpec(index, boundaries[index], boundaries[index + 1])
        for index in range(segment_count)
    )
    if specs[0].lower_inclusive != lower_inclusive:
        raise ParallelSegmentError("partition changed the lower endpoint")
    if specs[-1].upper_exclusive != upper_exclusive:
        raise ParallelSegmentError("partition changed the upper endpoint")
    if any(
        left.upper_exclusive != right.lower_inclusive
        for left, right in zip(specs, specs[1:], strict=False)
    ):
        raise ParallelSegmentError("partition is not contiguous")
    if any(spec.lower_inclusive >= spec.upper_exclusive for spec in specs):
        raise ParallelSegmentError("partition contains an empty segment")
    return specs


def _initialize_single_thread_worker() -> None:
    """Prevent nested native pools from oversubscribing eight worker processes."""

    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "BLIS_NUM_THREADS",
    ):
        os.environ[name] = "1"


def _segment_worker(
    payload: tuple[SegmentSpec, tuple[dict[str, int], ...], int]
) -> dict[str, object]:
    import numpy as np

    from source.recurrence_stratified_holdout import iter_prime_chunks_range
    from source.recurrence_stratified_null import accumulate_bin_counts

    spec, plateaus, sieve_segment_span = payload
    if sieve_segment_span < 10:
        raise ValueError("sieve_segment_span must be at least 10")

    first_prime: int | None = None
    boundary_prime: int | None = None
    in_range_prime_count = 0

    def monitored_chunks() -> Iterable[np.ndarray]:
        nonlocal first_prime, boundary_prime, in_range_prime_count
        for raw_chunk in iter_prime_chunks_range(
            spec.lower_inclusive,
            spec.upper_exclusive,
            segment_span=sieve_segment_span,
        ):
            chunk = np.asarray(raw_chunk, dtype=np.int64)
            if chunk.ndim != 1 or chunk.size == 0:
                raise ParallelSegmentError("worker received an invalid prime chunk")
            if first_prime is None:
                first_prime = int(chunk[0])
            boundary_prime = int(chunk[-1])
            in_range_prime_count += int(
                np.count_nonzero(chunk < spec.upper_exclusive)
            )
            yield chunk

    accumulated = accumulate_bin_counts(monitored_chunks(), plateaus)
    if first_prime is None or boundary_prime is None:
        raise ParallelSegmentError("worker did not receive a boundary-closed prime stream")
    local_prime_count = int(accumulated["prime_count"])
    local_gap_count = int(accumulated["gap_count"])
    if local_prime_count != local_gap_count + 1:
        raise ParallelSegmentError("worker prime/gap count invariant failed")
    if local_gap_count != in_range_prime_count:
        raise ParallelSegmentError("worker did not assign one gap to every in-range prime")
    if not (
        first_prime >= spec.lower_inclusive
        and boundary_prime >= spec.upper_exclusive
    ):
        raise ParallelSegmentError("worker endpoint prime invariant failed")

    return {
        "segment_index": spec.index,
        "lower_inclusive": spec.lower_inclusive,
        "upper_exclusive": spec.upper_exclusive,
        "first_prime": first_prime,
        "boundary_prime": boundary_prime,
        "in_range_prime_count": in_range_prime_count,
        "worker_pid": os.getpid(),
        "native_thread_limits": {
            name: os.environ.get(name)
            for name in (
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
                "BLIS_NUM_THREADS",
            )
        },
        "statistics": accumulated,
    }


def _merge_integer_mapping(
    target: dict[object, int], source: dict[object, int]
) -> None:
    for key, value in source.items():
        integer = int(value)
        if integer < 0:
            raise ParallelSegmentError("negative sufficient-statistic count")
        target[key] = target.get(key, 0) + integer


def _sorted_mapping(source: dict[object, int]) -> dict[object, int]:
    return {key: source[key] for key in sorted(source)}


def exact_statistics_core(payload: dict[str, object]) -> dict[str, object]:
    """Return the serial-compatible exact fields, excluding parallel metadata."""

    return {
        "prime_count": int(payload["prime_count"]),
        "gap_count": int(payload["gap_count"]),
        "populations": payload["populations"],
        "gap_counts": payload["gap_counts"],
        "exposure_counts": payload["exposure_counts"],
        "exposure_equal_counts": payload["exposure_equal_counts"],
    }


def parallel_accumulate_bin_counts(
    lower_inclusive: int,
    upper_exclusive: int,
    plateaus: Sequence[dict[str, int]],
    *,
    worker_count: int,
    segment_count: int | None = None,
    sieve_segment_span: int = 50_000,
    start_method: str = "spawn",
) -> dict[str, object]:
    """Compute exact P013 sufficient statistics with process-isolated segments."""

    if not 1 <= worker_count <= 64:
        raise ValueError("worker_count must be in [1, 64]")
    selected_segments = worker_count if segment_count is None else segment_count
    specs = partition_integer_range(
        lower_inclusive,
        upper_exclusive,
        segment_count=selected_segments,
    )
    plateau_payload = tuple(dict(row) for row in plateaus)
    tasks = tuple((spec, plateau_payload, sieve_segment_span) for spec in specs)
    context = mp.get_context(start_method)
    with ProcessPoolExecutor(
        max_workers=min(worker_count, len(tasks)),
        mp_context=context,
        initializer=_initialize_single_thread_worker,
    ) as executor:
        results = list(executor.map(_segment_worker, tasks, chunksize=1))
    results.sort(key=lambda item: int(item["segment_index"]))

    for spec, result in zip(specs, results, strict=True):
        if (
            int(result["segment_index"]) != spec.index
            or int(result["lower_inclusive"]) != spec.lower_inclusive
            or int(result["upper_exclusive"]) != spec.upper_exclusive
        ):
            raise ParallelSegmentError("worker result does not match its segment")
    for left, right in zip(results, results[1:], strict=False):
        if int(left["boundary_prime"]) != int(right["first_prime"]):
            raise ParallelSegmentError("adjacent segment boundary primes disagree")

    merged_by_field: dict[str, dict[str, dict[object, int]]] = {
        name: {} for name in (
            "populations",
            "gap_counts",
            "exposure_counts",
            "exposure_equal_counts",
        )
    }
    total_gap_count = 0
    for result in results:
        statistics = result["statistics"]
        if not isinstance(statistics, dict):
            raise ParallelSegmentError("worker statistics payload is invalid")
        total_gap_count += int(statistics["gap_count"])
        for field, merged_schemes in merged_by_field.items():
            local_schemes = statistics[field]
            if not isinstance(local_schemes, dict):
                raise ParallelSegmentError(f"worker field is invalid: {field}")
            for scheme, local_counts in local_schemes.items():
                if not isinstance(local_counts, dict):
                    raise ParallelSegmentError("worker count table is invalid")
                target = merged_schemes.setdefault(str(scheme), {})
                _merge_integer_mapping(target, local_counts)

    merged: dict[str, object] = {
        "prime_count": total_gap_count + 1,
        "gap_count": total_gap_count,
    }
    for field, schemes in merged_by_field.items():
        merged[field] = {
            scheme: _sorted_mapping(counts)
            for scheme, counts in sorted(schemes.items())
        }
    merged["parallel_execution"] = {
        "worker_count_requested": worker_count,
        "segment_count": len(specs),
        "worker_pids": sorted({int(item["worker_pid"]) for item in results}),
        "segments": [
            {
                key: int(result[key])
                for key in (
                    "segment_index",
                    "lower_inclusive",
                    "upper_exclusive",
                    "first_prime",
                    "boundary_prime",
                    "in_range_prime_count",
                )
            }
            for result in results
        ],
        "adjacent_boundary_checks": max(0, len(results) - 1),
        "prime_arrays_transferred_between_processes": False,
        "exact_integer_merge": True,
        "worker_native_thread_ceiling": 1,
        "all_worker_native_thread_limits_one": all(
            all(value == "1" for value in result["native_thread_limits"].values())
            for result in results
        ),
    }
    return merged


__all__ = [
    "ParallelSegmentError",
    "SegmentSpec",
    "exact_statistics_core",
    "parallel_accumulate_bin_counts",
    "partition_integer_range",
]
