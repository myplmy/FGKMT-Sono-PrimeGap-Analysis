"""Exact diagnostics for the DEP-R09 sparse divisor-conductor audit.

This module separates three facts that must not be conflated:

* characters modulo ``q`` split uniquely by primitive conductor ``r | q``;
* the set of conductor *levels* can be sparse even though the total number
  of characters is still ``phi(q)``;
* a coefficient-agnostic sparse large-sieve certificate retains an
  unavoidable length term.  In the current normalization that term alone is
  already above the most favourable Theory-82 gate.

The last item rejects one generic proof certificate.  It is not a lower
bound for the actual prime-error energy, and it does not reject a
prime-specific estimate or a direct same-law weighted-correlation theorem.
No prime experiment or threshold calculation is performed here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Mapping

import mpmath as mp

from source import dep_r09_fixed_primorial_variance_barrier as theory83


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_sparse_divisor_conductor_source_audit_v1.json"
)

SAMPLE_PRIMORIALS = (3, 30, 210, 2310, 30030, 510510)
MV2001_SHA256 = "e4d6a5fae3a41b9b50fe34355b0ea098e852bd84384bba7e1e83dbb083af0c9b"
FG1996_SHA256 = "4981fe4eb38f8788a74082d031063e4dd9e98c63411fbb31d761e346b8a01bd9"


def _integer(value: object, name: str, *, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def prime_factors(value: int) -> tuple[int, ...]:
    """Return the distinct prime factors of a positive integer."""

    value = _integer(value, "value", minimum=1)
    factors: list[int] = []
    remainder = value
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            factors.append(prime)
            while remainder % prime == 0:
                remainder //= prime
        prime = 3 if prime == 2 else prime + 2
    if remainder > 1:
        factors.append(remainder)
    return tuple(factors)


def divisors(value: int) -> tuple[int, ...]:
    """Return all positive divisors in increasing order."""

    value = _integer(value, "value", minimum=1)
    lower: list[int] = []
    upper: list[int] = []
    candidate = 1
    while candidate * candidate <= value:
        if value % candidate == 0:
            lower.append(candidate)
            partner = value // candidate
            if partner != candidate:
                upper.append(partner)
        candidate += 1
    return tuple(lower + list(reversed(upper)))


def mobius(value: int) -> int:
    """Return the exact Moebius function."""

    value = _integer(value, "value", minimum=1)
    remainder = value
    parity = 0
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            remainder //= prime
            parity += 1
            if remainder % prime == 0:
                return 0
            while remainder % prime == 0:
                remainder //= prime
        prime = 3 if prime == 2 else prime + 2
    if remainder > 1:
        parity += 1
    return -1 if parity % 2 else 1


def primitive_character_count(conductor: int) -> int:
    """Return ``phi*(conductor)`` by Moebius inversion.

    Every character modulo ``q`` has one primitive conductor ``r | q`` and
    ``phi(q) = sum_(r|q) phi*(r)``.  The inversion formula used here is
    ``phi*(r) = sum_(d|r) mu(r/d) phi(d)``.
    """

    conductor = _integer(conductor, "conductor", minimum=1)
    return sum(
        mobius(conductor // divisor) * theory83.euler_phi(divisor)
        for divisor in divisors(conductor)
    )


def conductor_partition(modulus: int) -> dict[int, int]:
    """Return the primitive-conductor partition for characters modulo q."""

    modulus = _integer(modulus, "modulus", minimum=1)
    return {
        conductor: primitive_character_count(conductor)
        for conductor in divisors(modulus)
    }


def conductor_partition_is_exact(modulus: int) -> bool:
    partition = conductor_partition(modulus)
    return sum(partition.values()) == theory83.euler_phi(modulus)


def positive_conductor_level_count(modulus: int) -> int:
    return sum(count > 0 for count in conductor_partition(modulus).values())


def squarefree_primitive_count_product(conductor: int) -> int:
    """Return ``prod_(p|r) (p-2)`` after checking squarefreeness."""

    conductor = _integer(conductor, "conductor", minimum=1)
    factors = prime_factors(conductor)
    product = 1
    radical = 1
    for prime in factors:
        product *= prime - 2
        radical *= prime
    if radical != conductor:
        raise ValueError("conductor must be squarefree")
    return product


def generic_sparse_rhs_lower_over_y2(q: int, d: int) -> mp.mpf:
    """Return a strict lower certificate for any ``(Y+D)*S2(Y)`` RHS.

    Here ``D >= 0`` is any modulus-density contribution.  Dropping it gives
    ``Y*S2(Y)``; Theory 83 already proves
    ``S2(Y)/Y > (log(Y)-log(2))/4`` in the current power regime.
    """

    return theory83.coarse_large_sieve_rhs_lower_over_y2(q, d)


def generic_sparse_barrier_margin(q: int, d: int) -> mp.mpf:
    """Return the conservative length-term margin above the Theory-82 gate."""

    with mp.workdps(max(mp.mp.dps, 100)):
        return +(
            generic_sparse_rhs_lower_over_y2(q, d)
            - theory83.rosser_entropy_gate_upper_over_y2(q)
        )


def one_frequency_extremizer(length: int) -> dict[str, int]:
    """Return the exact universal length-term extremizer.

    At one sampled frequency ``alpha_0``, choose
    ``a_n = exp(-2*pi*i*n*alpha_0)``.  Then the sampled polynomial has
    squared magnitude ``N^2`` while coefficient energy is ``N``.  Hence any
    coefficient-agnostic bound for a family containing that frequency needs
    coefficient at least ``N``.
    """

    length = _integer(length, "length", minimum=1)
    lhs_squared_magnitude = length * length
    coefficient_energy = length
    required_coefficient = Fraction(lhs_squared_magnitude, coefficient_energy)
    return {
        "length": length,
        "lhs_squared_magnitude": lhs_squared_magnitude,
        "coefficient_energy": coefficient_energy,
        "minimum_universal_coefficient": required_coefficient.numerator,
    }


def signed_cancellation_witness() -> dict[str, int]:
    """Show why a signed Moebius sum does not control its absolute-value use."""

    values = (1, -1)
    signed_sum = sum(values)
    l1_sum = sum(abs(value) for value in values)
    return {
        "signed_sum": signed_sum,
        "signed_sum_squared": signed_sum * signed_sum,
        "l1_sum": l1_sum,
        "l1_sum_squared": l1_sum * l1_sum,
    }


@dataclass(frozen=True)
class SparseDivisorConductorDiagnostic:
    sample_conductor_partitions_all_exact: bool
    sample_nonprincipal_totals_all_phi_minus_one: bool
    squarefree_product_formula_all_exact: bool
    positive_conductor_levels: dict[str, int]
    total_character_counts: dict[str, int]
    generic_sparse_length_term_margins_all_positive: bool
    one_frequency_extremizer_requires_length_term: bool
    signed_cancellation_does_not_bound_l1_witness: bool
    montgomery_vaughan_2001_pdf_is_requested_vaughan_variance_paper: bool
    friedlander_goldston_1996_pdf_identity_verified: bool
    generic_sparse_large_sieve_can_certify_theory82_gate: bool
    prime_specific_bound_identified: bool
    direct_same_law_correlation_theorem_identified: bool
    actual_character_energy_lower_bound_claimed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> SparseDivisorConductorDiagnostic:
    partitions = {
        modulus: conductor_partition(modulus) for modulus in SAMPLE_PRIMORIALS
    }
    squarefree_product_exact = all(
        primitive_character_count(conductor)
        == squarefree_primitive_count_product(conductor)
        for modulus in SAMPLE_PRIMORIALS
        for conductor in divisors(modulus)
    )
    with mp.workdps(max(mp.mp.dps, 120)):
        margins_positive = all(
            generic_sparse_barrier_margin(modulus, d) > 0
            for modulus in SAMPLE_PRIMORIALS
            for d in (theory83.D_MIN, theory83.D_MAX)
        )
    extremizer = one_frequency_extremizer(7)
    cancellation = signed_cancellation_witness()
    return SparseDivisorConductorDiagnostic(
        sample_conductor_partitions_all_exact=all(
            sum(partition.values()) == theory83.euler_phi(modulus)
            for modulus, partition in partitions.items()
        ),
        sample_nonprincipal_totals_all_phi_minus_one=all(
            sum(partition.values()) - partition[1]
            == theory83.euler_phi(modulus) - 1
            for modulus, partition in partitions.items()
        ),
        squarefree_product_formula_all_exact=squarefree_product_exact,
        positive_conductor_levels={
            str(modulus): sum(count > 0 for count in partition.values())
            for modulus, partition in partitions.items()
        },
        total_character_counts={
            str(modulus): sum(partition.values())
            for modulus, partition in partitions.items()
        },
        generic_sparse_length_term_margins_all_positive=margins_positive,
        one_frequency_extremizer_requires_length_term=(
            extremizer["minimum_universal_coefficient"]
            == extremizer["length"]
        ),
        signed_cancellation_does_not_bound_l1_witness=(
            cancellation["signed_sum_squared"] == 0
            and cancellation["l1_sum_squared"] == 4
        ),
        montgomery_vaughan_2001_pdf_is_requested_vaughan_variance_paper=False,
        friedlander_goldston_1996_pdf_identity_verified=True,
        generic_sparse_large_sieve_can_certify_theory82_gate=False,
        prime_specific_bound_identified=False,
        direct_same_law_correlation_theorem_identified=False,
        actual_character_energy_lower_bound_claimed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        bounded_x_cert_range_obtained=False,
        threshold_calculator_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def load_ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def validate_ledger(
    document: Mapping[str, object],
    *,
    check_hashes: bool = True,
) -> list[str]:
    """Validate the fail-closed status and every locally pinned source."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != "DEP-R09 sparse divisor-conductor source audit":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "GENERIC_COEFFICIENT_AGNOSTIC_SPARSE_LARGE_SIEVE_CERTIFICATE_REJECTED_"
        "PRIME_SPECIFIC_OR_WEIGHTED_CORRELATION_INPUT_OPEN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Obtain a fully numerical unconditional prime-specific fixed-primorial "
        "bound or an actual same-law weighted-correlation theorem; the number "
        "of divisor-conductor levels and a generic sparse large sieve are "
        "insufficient because the unavoidable length term already exceeds "
        "the Theory-82 gate."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list):
        issues.append("source_registry mismatch")
        return issues
    pinned = {
        item.get("key")
        for item in sources
        if isinstance(item, dict) and "locator" in item
    }
    expected_pinned = {
        "MONTGOMERY_VAUGHAN2001_LOCAL",
        "FRIEDLANDER_GOLDSTON1996_LOCAL",
        "THEORY83",
    }
    if pinned != expected_pinned:
        issues.append("pinned source keys mismatch")

    if check_hashes:
        for source in sources:
            if not isinstance(source, dict) or "locator" not in source:
                continue
            key = source.get("key", "unknown")
            locator = source.get("locator")
            digest = source.get("sha256")
            if not isinstance(locator, str) or not isinstance(digest, str):
                issues.append(f"{key} missing pin")
                continue
            path = (REPO_ROOT / locator).resolve()
            try:
                path.relative_to(REPO_ROOT.resolve())
            except ValueError:
                issues.append(f"{key} path escape")
                continue
            if not path.is_file():
                issues.append(f"{key} missing source")
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                issues.append(f"{key} hash mismatch")
            expected_size = source.get("byte_size")
            if isinstance(expected_size, int) and path.stat().st_size != expected_size:
                issues.append(f"{key} byte-size mismatch")
    return issues


__all__ = [
    "FG1996_SHA256",
    "LEDGER_PATH",
    "MV2001_SHA256",
    "SAMPLE_PRIMORIALS",
    "build_diagnostic",
    "conductor_partition",
    "conductor_partition_is_exact",
    "divisors",
    "generic_sparse_barrier_margin",
    "generic_sparse_rhs_lower_over_y2",
    "load_ledger",
    "mobius",
    "one_frequency_extremizer",
    "positive_conductor_level_count",
    "prime_factors",
    "primitive_character_count",
    "signed_cancellation_witness",
    "squarefree_primitive_count_product",
    "validate_ledger",
]
