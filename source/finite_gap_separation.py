"""Memory-bounded transition separation for a future modulus-30030 LP.

The existing P007 solver materializes all transition inequalities.  Modulus
30030 has 5,760 residue states and more than 35 million inequalities, so dense
or monolithic sparse construction is unsafe under the 32 GiB project limit.

This module is a *separation-oracle prototype*: it scans source-state chunks,
computes slacks for one candidate dual solution, and retains only the most
violated inequalities.  It does not solve or certify the modulus-30030 LP.
Floating-point slacks are discovery aids; a promoted rational certificate must
still pass a streaming exact-integer verifier.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from source.finite_gap_certificate import state_count, unit_residues


DEFAULT_CHUNK_ROWS = 64
DEFAULT_MAX_TOY_STATES = 1_000


class SeparationResourceGuardError(RuntimeError):
    """Raised before an unauthorized large-state transition scan."""


@dataclass(frozen=True)
class SeparationCandidate:
    lambda_value: float
    mu_value: float
    potentials: tuple[float, ...]


@dataclass(frozen=True)
class TransitionViolation:
    slack: float
    source_index: int
    target_index: int
    gap: int
    weight: int


def separation_memory_estimate(
    modulus: int,
    *,
    chunk_rows: int = DEFAULT_CHUNK_ROWS,
    top_k: int = 1_000,
) -> dict[str, object]:
    """Conservative working-memory estimate for one vectorized scan chunk."""

    if chunk_rows < 1 or top_k < 1:
        raise ValueError("chunk_rows and top_k must be positive")
    states = state_count(modulus)
    cells = min(chunk_rows, states) * states
    # d0, large-gap, two float slack workspaces, two index workspaces and masks.
    # The factor 96 intentionally exceeds the raw NumPy storage estimate and
    # leaves room for temporary expressions and retained Python objects.
    array_bytes_conservative = cells * 96
    retained_bytes_conservative = top_k * 512
    total = array_bytes_conservative + retained_bytes_conservative
    return {
        "modulus": modulus,
        "states": states,
        "chunk_rows": chunk_rows,
        "cells_per_chunk": cells,
        "top_k": top_k,
        "conservative_working_bytes": total,
        "conservative_working_mib": total / (1024**2),
        "under_1_gib": total < 1024**3,
        "full_constraint_matrix_materialized": False,
        "estimate_is_not_a_solver_memory_guarantee": True,
    }


def _least_large_representatives(
    d0: np.ndarray, modulus: int, threshold: int
) -> np.ndarray:
    steps = np.maximum(0, (threshold - d0 + modulus - 1) // modulus)
    return d0 + steps * modulus


def _violation_sort_key(item: TransitionViolation) -> tuple[float, int, int, int, int]:
    return (
        item.slack,
        item.source_index,
        item.target_index,
        item.weight,
        item.gap,
    )


def _retain_smallest(
    retained: list[TransitionViolation],
    candidates: Iterable[TransitionViolation],
    top_k: int,
) -> list[TransitionViolation]:
    merged = retained + list(candidates)
    merged.sort(key=_violation_sort_key)
    return merged[:top_k]


def _select_negative_flat_indices(
    values: np.ndarray,
    mask: np.ndarray,
    top_k: int,
) -> np.ndarray:
    """Select at most K smallest masked entries without Python objects per hit.

    Ties at the cutoff are resolved by the row-major flat index, which makes
    the selected constraints independent of NumPy's partition tie ordering.
    """

    flat_mask = mask.ravel()
    indices = np.flatnonzero(flat_mask)
    if indices.size <= top_k:
        return indices
    flat_values = values.ravel()
    selected_values = flat_values[indices]
    cutoff = np.partition(selected_values, top_k - 1)[top_k - 1]
    strict = indices[selected_values < cutoff]
    need = top_k - strict.size
    equal = indices[selected_values == cutoff]
    selected = np.concatenate((strict, equal[:need]))
    order = np.lexsort((selected, flat_values[selected]))
    return selected[order]


def scan_transition_violations(
    modulus: int,
    threshold: int,
    candidate: SeparationCandidate,
    *,
    chunk_rows: int = DEFAULT_CHUNK_ROWS,
    top_k: int = 100,
    violation_tolerance: float = 1e-10,
    allow_large_state_scan: bool = False,
) -> dict[str, object]:
    """Return the most negative transition slacks without materializing the LP.

    The default state guard deliberately blocks modulus 30030.  Removing it is
    an explicit future experiment action, not part of the current toy tests.
    """

    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    if chunk_rows < 1 or top_k < 1:
        raise ValueError("chunk_rows and top_k must be positive")
    residues = np.asarray(unit_residues(modulus), dtype=np.int64)
    states = len(residues)
    if len(candidate.potentials) != states:
        raise ValueError("candidate potential count differs from residue state count")
    if states > DEFAULT_MAX_TOY_STATES and not allow_large_state_scan:
        raise SeparationResourceGuardError(
            f"state count {states} exceeds toy guard {DEFAULT_MAX_TOY_STATES}; "
            "a modulus-30030 scan requires a separately authorized run"
        )
    potentials = np.asarray(candidate.potentials, dtype=np.float64)
    retained: list[TransitionViolation] = []
    scanned_constraints = 0
    violation_count = 0
    minimum_slack = math.inf

    for source_start in range(0, states, chunk_rows):
        source_stop = min(states, source_start + chunk_rows)
        source_values = residues[source_start:source_stop, None]
        d0 = (residues[None, :] - source_values) % modulus
        d0 = np.where(d0 == 0, modulus, d0)
        potential_delta = (
            potentials[source_start:source_stop, None] - potentials[None, :]
        )

        small_mask = d0 < threshold
        small_slack = (
            candidate.lambda_value * d0
            + candidate.mu_value
            + potential_delta
        )
        small_violation_mask = small_mask & (small_slack < -violation_tolerance)
        small_violation_count = int(np.count_nonzero(small_violation_mask))
        small_indices = _select_negative_flat_indices(
            small_slack, small_violation_mask, top_k
        )
        small_items = [
            TransitionViolation(
                slack=float(small_slack.ravel()[flat_index]),
                source_index=source_start + int(flat_index // states),
                target_index=int(flat_index % states),
                gap=int(d0.ravel()[flat_index]),
                weight=0,
            )
            for flat_index in small_indices
        ]
        violation_count += small_violation_count
        if small_mask.any():
            minimum_slack = min(minimum_slack, float(np.min(small_slack[small_mask])))
        retained = _retain_smallest(retained, small_items, top_k)
        scanned_constraints += int(np.count_nonzero(small_mask))

        large_gap = _least_large_representatives(d0, modulus, threshold)
        large_slack = (
            candidate.lambda_value * large_gap
            + candidate.mu_value
            + potential_delta
            - 1.0
        )
        large_violation_mask = large_slack < -violation_tolerance
        large_violation_count = int(np.count_nonzero(large_violation_mask))
        large_indices = _select_negative_flat_indices(
            large_slack, large_violation_mask, top_k
        )
        large_items = [
            TransitionViolation(
                slack=float(large_slack.ravel()[flat_index]),
                source_index=source_start + int(flat_index // states),
                target_index=int(flat_index % states),
                gap=int(large_gap.ravel()[flat_index]),
                weight=1,
            )
            for flat_index in large_indices
        ]
        violation_count += large_violation_count
        minimum_slack = min(minimum_slack, float(np.min(large_slack)))
        retained = _retain_smallest(retained, large_items, top_k)
        scanned_constraints += large_slack.size

    return {
        "status": "PASS",
        "modulus": modulus,
        "threshold": threshold,
        "states": states,
        "chunk_rows": chunk_rows,
        "scanned_constraints": scanned_constraints,
        "violation_count": violation_count,
        "minimum_slack": minimum_slack,
        "top_violations": [item.__dict__ for item in retained],
        "full_constraint_matrix_materialized": False,
        "floating_discovery_only": True,
        "exact_certificate_verified": False,
    }


def brute_force_transition_violations(
    modulus: int,
    threshold: int,
    candidate: SeparationCandidate,
    *,
    top_k: int = 100,
    violation_tolerance: float = 1e-10,
) -> list[TransitionViolation]:
    """Small-modulus reference implementation for oracle cross-checks."""

    residues = unit_residues(modulus)
    if len(candidate.potentials) != len(residues):
        raise ValueError("candidate potential count differs from residue state count")
    violations: list[TransitionViolation] = []
    for i, source in enumerate(residues):
        for j, target in enumerate(residues):
            d0 = (target - source) % modulus or modulus
            if d0 < threshold:
                slack = (
                    candidate.lambda_value * d0
                    + candidate.mu_value
                    + candidate.potentials[i]
                    - candidate.potentials[j]
                )
                if slack < -violation_tolerance:
                    violations.append(TransitionViolation(slack, i, j, d0, 0))
            large_gap = d0
            if large_gap < threshold:
                large_gap += ((threshold - large_gap + modulus - 1) // modulus) * modulus
            slack = (
                candidate.lambda_value * large_gap
                + candidate.mu_value
                + candidate.potentials[i]
                - candidate.potentials[j]
                - 1.0
            )
            if slack < -violation_tolerance:
                violations.append(TransitionViolation(slack, i, j, large_gap, 1))
    violations.sort(key=_violation_sort_key)
    return violations[:top_k]


__all__ = [
    "DEFAULT_CHUNK_ROWS",
    "DEFAULT_MAX_TOY_STATES",
    "SeparationCandidate",
    "SeparationResourceGuardError",
    "TransitionViolation",
    "brute_force_transition_violations",
    "scan_transition_violations",
    "separation_memory_estimate",
]
