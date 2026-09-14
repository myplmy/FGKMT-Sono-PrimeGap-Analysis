"""Exact finite logic for the DEP-R09 Maier/FMT selection-quantifier audit.

This module does not prove an analytic prime-distribution estimate and does
not enumerate primorial residues.  It records only the finite union-bound and
Markov-count arithmetic needed *after* a genuine construction family and its
bad-event estimates have been supplied.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import floor
from typing import Iterable


def _natural(value: int, name: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    if not positive and value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def union_bound_remaining_lower_bound(
    candidate_count: int,
    bad_counts: Iterable[int],
) -> int:
    """Return ``N - sum(b_i)``, clipped at zero.

    If this value is positive, the union bound certifies at least one
    candidate outside every bad set.  The function intentionally does not
    infer independence or identify a construction family.
    """

    candidate_count = _natural(candidate_count, "candidate_count", positive=True)
    normalized: list[int] = []
    for index, value in enumerate(bad_counts):
        normalized.append(_natural(value, f"bad_counts[{index}]"))
    return max(0, candidate_count - sum(normalized))


def union_bound_certifies_candidate(
    candidate_count: int,
    bad_counts: Iterable[int],
) -> bool:
    """Return whether ``sum(b_i) < N`` certifies a simultaneous good point."""

    return union_bound_remaining_lower_bound(candidate_count, bad_counts) > 0


def markov_bad_count_upper(
    total_badness: Fraction,
    badness_threshold: Fraction,
) -> int:
    """Return the exact Markov upper bound ``floor(total/threshold)``.

    For nonnegative weights ``w_y``, this bounds the number of candidates
    with ``w_y >= threshold``.  Supplying the analytic total badness remains
    an external premise.
    """

    if not isinstance(total_badness, Fraction):
        raise TypeError("total_badness must be fractions.Fraction")
    if not isinstance(badness_threshold, Fraction):
        raise TypeError("badness_threshold must be fractions.Fraction")
    if total_badness < 0:
        raise ValueError("total_badness must be nonnegative")
    if badness_threshold <= 0:
        raise ValueError("badness_threshold must be positive")
    return floor(total_badness / badness_threshold)


@dataclass(frozen=True)
class MaierShiftSelectionDiagnostic:
    classical_fixed_partition_crt_residue_count: int
    classical_fixed_partition_has_free_y_average: bool
    singleton_zero_bad_counts_certified: bool
    singleton_one_bad_count_certified: bool
    sono_fmt_crt_m_unique_per_residue_vector: bool
    sono_fmt_source_uses_randomized_sieve_vectors: bool
    numerical_mass_of_jointly_good_vectors_certified: bool
    direct_uniform_in_vector_correlation_bypasses_selection: bool
    average_correlation_requires_joint_good_family_bound: bool
    finite_union_selection_lemma_available: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> MaierShiftSelectionDiagnostic:
    """Build the fail-closed status snapshot for this quantifier audit."""

    return MaierShiftSelectionDiagnostic(
        classical_fixed_partition_crt_residue_count=1,
        classical_fixed_partition_has_free_y_average=False,
        singleton_zero_bad_counts_certified=union_bound_certifies_candidate(
            1, [0, 0, 0]
        ),
        singleton_one_bad_count_certified=union_bound_certifies_candidate(
            1, [1, 0, 0]
        ),
        sono_fmt_crt_m_unique_per_residue_vector=True,
        sono_fmt_source_uses_randomized_sieve_vectors=True,
        numerical_mass_of_jointly_good_vectors_certified=False,
        direct_uniform_in_vector_correlation_bypasses_selection=True,
        average_correlation_requires_joint_good_family_bound=True,
        finite_union_selection_lemma_available=True,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        threshold_calculator_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def diagnostic_as_dict() -> dict[str, object]:
    """Return the status snapshot in JSON-serializable form."""

    return asdict(build_diagnostic())
