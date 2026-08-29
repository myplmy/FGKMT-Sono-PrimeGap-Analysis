"""Process-parallel exact row-block scanner for the P014-R2 toy revision.

The serial :func:`source.finite_gap_separation.scan_exact_certificate_constraints`
remains the authoritative oracle.  This module partitions only source-state
rows, evaluates both constraint families with the same guarded signed-int64
formulas, and performs an order-independent exact reduction.
"""

from __future__ import annotations

import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from source.finite_gap_certificate import RationalCertificate


class ParallelExactScanError(RuntimeError):
    """Raised when exact row coverage or reduction invariants fail."""


_WORKER_CERTIFICATE: object | None = None
_WORKER_RESIDUES: object | None = None
_WORKER_POTENTIALS: object | None = None
_WORKER_TOP_K: int | None = None


def _initialize_single_thread_worker() -> None:
    """Keep eight processes from creating nested eight-thread native pools."""

    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "BLIS_NUM_THREADS",
    ):
        os.environ[name] = "1"


def _certificate_payload(certificate: RationalCertificate) -> tuple[object, ...]:
    return (
        certificate.modulus,
        certificate.threshold,
        certificate.denominator,
        certificate.lambda_num,
        certificate.mu_num,
        certificate.t_num,
        certificate.phi_num,
        certificate.internal_bound,
        certificate.total_bound,
    )


def _initialize_exact_scan_worker(
    certificate_payload: tuple[object, ...], top_k: int, startup_barrier: object | None
) -> None:
    """Initialize immutable certificate arrays once per process, not per row block."""

    _initialize_single_thread_worker()
    import numpy as np

    from source.finite_gap_certificate import RationalCertificate, unit_residues

    certificate = RationalCertificate(*certificate_payload)
    global _WORKER_CERTIFICATE, _WORKER_RESIDUES, _WORKER_POTENTIALS, _WORKER_TOP_K
    _WORKER_CERTIFICATE = certificate
    _WORKER_RESIDUES = np.asarray(unit_residues(certificate.modulus), dtype=np.int64)
    _WORKER_POTENTIALS = np.asarray(certificate.phi_num, dtype=np.int64)
    _WORKER_TOP_K = int(top_k)
    if startup_barrier is not None:
        startup_barrier.wait(timeout=120)


def _overflow_guard_upper_bound(certificate: RationalCertificate) -> int:
    max_phi = max(abs(value) for value in certificate.phi_num)
    max_representative = certificate.threshold + certificate.modulus - 1
    return (
        abs(certificate.lambda_num) * max_representative
        + abs(certificate.mu_num)
        + 2 * max_phi
        + certificate.denominator
    )


def _validate_parallel_certificate(
    certificate: RationalCertificate,
    *,
    row_block_rows: int,
    top_k: int,
    allow_large_state_scan: bool,
) -> tuple[int, int]:
    import numpy as np

    from source.finite_gap_certificate import unit_residues
    from source.finite_gap_separation import (
        DEFAULT_MAX_TOY_STATES,
        SeparationResourceGuardError,
    )

    if certificate.threshold < 2:
        raise ValueError("threshold must be at least 2")
    if certificate.denominator <= 0:
        raise ValueError("certificate denominator must be positive")
    if certificate.lambda_num < 0:
        raise ValueError("lambda must be nonnegative")
    if row_block_rows < 1 or top_k < 1:
        raise ValueError("row_block_rows and top_k must be positive")
    states = len(unit_residues(certificate.modulus))
    if len(certificate.phi_num) != states:
        raise ValueError("certificate potential count differs from residue state count")
    if states > DEFAULT_MAX_TOY_STATES and not allow_large_state_scan:
        raise SeparationResourceGuardError(
            f"state count {states} exceeds toy guard {DEFAULT_MAX_TOY_STATES}; "
            "a large parallel exact scan requires a separately authorized run"
        )
    max_phi = max(abs(value) for value in certificate.phi_num)
    if max_phi > certificate.t_num:
        raise ValueError("t_num does not bound every potential")
    overflow_upper_bound = _overflow_guard_upper_bound(certificate)
    if overflow_upper_bound > int(np.iinfo(np.int64).max):
        raise SeparationResourceGuardError(
            "parallel exact vector scan cannot prove signed-64-bit arithmetic safe"
        )
    return states, overflow_upper_bound


def _scan_source_block(payload: tuple[int, int]) -> dict[str, object]:
    import numpy as np

    from source.finite_gap_separation import (
        _least_large_representatives,
        _select_negative_flat_indices,
    )

    certificate = _WORKER_CERTIFICATE
    residues = _WORKER_RESIDUES
    potentials = _WORKER_POTENTIALS
    top_k = _WORKER_TOP_K
    if certificate is None or residues is None or potentials is None or top_k is None:
        raise ParallelExactScanError("worker immutable certificate state was not initialized")
    source_start, source_stop = payload
    states = int(residues.size)
    if not 0 <= source_start < source_stop <= states:
        raise ParallelExactScanError("worker source row block is invalid")

    source_values = residues[source_start:source_stop, None]
    d0 = (residues[None, :] - source_values) % certificate.modulus
    d0 = np.where(d0 == 0, certificate.modulus, d0).astype(
        np.int64, copy=False
    )
    potential_delta = (
        potentials[source_start:source_stop, None] - potentials[None, :]
    )
    lambda_num = np.int64(certificate.lambda_num)
    mu_num = np.int64(certificate.mu_num)
    denominator = np.int64(certificate.denominator)

    retained: list[tuple[int, int, int, int, int]] = []
    violation_count = 0
    scanned_constraints = 0
    minimum_slack: int | None = None

    def retain_negative(
        values: np.ndarray,
        mask: np.ndarray,
        gaps: np.ndarray,
        weight: int,
    ) -> None:
        nonlocal retained
        indices = _select_negative_flat_indices(values, mask, top_k)
        items = [
            (
                int(values.ravel()[flat_index]),
                source_start + int(flat_index // states),
                int(flat_index % states),
                int(gaps.ravel()[flat_index]),
                weight,
            )
            for flat_index in indices
        ]
        retained = sorted(retained + items)[:top_k]

    small_mask = d0 < certificate.threshold
    small_slack = lambda_num * d0 + mu_num + potential_delta
    small_negative = small_mask & (small_slack < 0)
    violation_count += int(np.count_nonzero(small_negative))
    retain_negative(small_slack, small_negative, d0, 0)
    if small_mask.any():
        minimum_slack = int(np.min(small_slack[small_mask]))
    scanned_constraints += int(np.count_nonzero(small_mask))

    large_gap = _least_large_representatives(
        d0, certificate.modulus, certificate.threshold
    ).astype(np.int64, copy=False)
    large_slack = (
        lambda_num * large_gap + mu_num + potential_delta - denominator
    )
    large_negative = large_slack < 0
    violation_count += int(np.count_nonzero(large_negative))
    retain_negative(large_slack, large_negative, large_gap, 1)
    large_minimum = int(np.min(large_slack))
    minimum_slack = (
        large_minimum
        if minimum_slack is None
        else min(minimum_slack, large_minimum)
    )
    scanned_constraints += int(large_slack.size)

    return {
        "source_start": source_start,
        "source_stop": source_stop,
        "scanned_constraints": scanned_constraints,
        "violation_count": violation_count,
        "minimum_integer_slack": minimum_slack,
        "retained": retained,
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
    }


def exact_scan_core(report: dict[str, object]) -> dict[str, object]:
    """Return fields that must be identical to the authoritative serial scan."""

    return {
        key: report[key]
        for key in (
            "status",
            "modulus",
            "threshold",
            "states",
            "chunk_rows",
            "scanned_constraints",
            "violation_count",
            "minimum_integer_slack",
            "top_exact_violations",
            "signed_int64_overflow_guard_upper_bound",
            "signed_int64_limit",
            "full_constraint_matrix_materialized",
            "exact_certificate_verified",
        )
    }


def parallel_scan_exact_certificate_constraints(
    certificate: RationalCertificate,
    *,
    worker_count: int,
    row_block_rows: int = 64,
    top_k: int = 100,
    allow_large_state_scan: bool = False,
    start_method: str = "spawn",
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    """Scan every exact constraint once and reduce blocks deterministically."""

    if not 1 <= worker_count <= 64:
        raise ValueError("worker_count must be in [1, 64]")
    states, overflow_upper_bound = _validate_parallel_certificate(
        certificate,
        row_block_rows=row_block_rows,
        top_k=top_k,
        allow_large_state_scan=allow_large_state_scan,
    )
    blocks = tuple(
        (start, min(states, start + row_block_rows))
        for start in range(0, states, row_block_rows)
    )
    tasks = blocks
    context = mp.get_context(start_method)
    active_worker_count = min(worker_count, len(tasks))
    startup_barrier = (
        None if active_worker_count == 1 else context.Barrier(active_worker_count)
    )
    results: list[dict[str, object]] = []
    progress_interval = max(1, len(tasks) // 100)
    with ProcessPoolExecutor(
        max_workers=active_worker_count,
        mp_context=context,
        initializer=_initialize_exact_scan_worker,
        initargs=(_certificate_payload(certificate), top_k, startup_barrier),
    ) as executor:
        for completed, result in enumerate(
            executor.map(_scan_source_block, tasks, chunksize=1), start=1
        ):
            results.append(result)
            if progress_callback is not None and (
                completed == 1
                or completed == len(tasks)
                or completed % progress_interval == 0
            ):
                progress_callback(
                    {
                        "blocks_completed": completed,
                        "blocks_total": len(tasks),
                        "source_rows_completed": sum(
                            int(item["source_stop"]) - int(item["source_start"])
                            for item in results
                        ),
                        "source_rows_total": states,
                        "scanned_constraints_so_far": sum(
                            int(item["scanned_constraints"]) for item in results
                        ),
                    }
                )
    results.sort(key=lambda item: int(item["source_start"]))

    cursor = 0
    for block, result in zip(blocks, results, strict=True):
        source_start, source_stop = block
        if (
            int(result["source_start"]) != source_start
            or int(result["source_stop"]) != source_stop
            or source_start != cursor
        ):
            raise ParallelExactScanError("source row blocks are missing or overlap")
        cursor = source_stop
    if cursor != states:
        raise ParallelExactScanError("source row coverage does not reach the final state")
    observed_worker_pids = sorted({int(item["worker_pid"]) for item in results})
    if len(observed_worker_pids) != active_worker_count:
        raise ParallelExactScanError(
            "not every requested exact-scan worker processed at least one row block"
        )

    scanned_constraints = sum(int(item["scanned_constraints"]) for item in results)
    violation_count = sum(int(item["violation_count"]) for item in results)
    minimum_slack = min(int(item["minimum_integer_slack"]) for item in results)
    retained = sorted(
        tuple(entry)
        for item in results
        for entry in item["retained"]
    )[:top_k]
    import numpy as np

    from source.finite_gap_certificate import transition_resource_estimate

    expected = int(
        transition_resource_estimate(certificate.modulus, certificate.threshold)[
            "total_transition_constraints"
        ]
    )
    if scanned_constraints != expected:
        raise ParallelExactScanError(
            "parallel exact scan constraint count disagrees with exact estimate"
        )

    return {
        "status": "PASS" if violation_count == 0 else "FAIL",
        "modulus": certificate.modulus,
        "threshold": certificate.threshold,
        "states": states,
        "chunk_rows": row_block_rows,
        "scanned_constraints": scanned_constraints,
        "violation_count": violation_count,
        "minimum_integer_slack": minimum_slack,
        "top_exact_violations": [
            {
                "slack": slack,
                "source_index": source,
                "target_index": target,
                "gap": gap,
                "weight": weight,
            }
            for slack, source, target, gap, weight in retained
        ],
        "signed_int64_overflow_guard_upper_bound": overflow_upper_bound,
        "signed_int64_limit": int(np.iinfo(np.int64).max),
        "full_constraint_matrix_materialized": False,
        "exact_certificate_verified": violation_count == 0,
        "parallel_execution": {
            "worker_count_requested": worker_count,
            "row_block_count": len(blocks),
            "worker_pids": observed_worker_pids,
            "worker_count_observed": len(observed_worker_pids),
            "source_rows_covered": cursor,
            "exact_integer_reduction": True,
            "worker_completion_order_affects_result": False,
            "worker_native_thread_ceiling": 1,
            "worker_static_arrays_initialized_once": True,
            "certificate_copied_per_row_block": False,
            "all_worker_native_thread_limits_one": all(
                all(value == "1" for value in item["native_thread_limits"].values())
                for item in results
            ),
        },
    }


__all__ = [
    "ParallelExactScanError",
    "exact_scan_core",
    "parallel_scan_exact_certificate_constraints",
]
