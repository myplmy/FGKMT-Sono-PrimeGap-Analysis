"""Fail-closed Maynard-generic H1c-1b.3 count-transfer helpers.

This module records the narrow bridge from a cumulative von Mangoldt
discrepancy bound to Maynard's exact, half-open, unweighted prime-count
target for the identity form.  It preserves four pieces that are easy to
lose in an informal conversion:

* the plus sign in Abel/partial summation;
* prime powers in ``pi_1 - pi``;
* the endpoint atoms that change ``(T, 2T]`` into ``[T, 2T)``; and
* recentering at the exact total prime population, not at ``T/log(T)``.

This historical bridge exactly matches Maynard's original Definition (2.1),
but not FGKMT's modified closed interval.  The actual FGKMT correction is
recorded in :mod:`source.h1c1b3r1_fgkmt_endpoint_correction`.

It does not bound Bordignon's unresolved constant, prove the required
relative log-saving, produce a finite prime-density lower bound, close
Maynard Hypothesis 1(2)/Proposition 9.2, or calculate ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import (
    DEFAULT_TRANSPORT_MARGIN,
    MINIMUM_SIEVE_DIMENSION,
    bordignon_basic_statement_conditions,
    bordignon_capacity_is_increasing,
    bordignon_exponent,
    modulus_capacity_log_margin,
    q1_within_q_log_margin,
)


PRIME_POWER_CUMULATIVE_CONSTANT = 2
PARTIAL_SUMMATION_INTEGRAL_SIGN = "+"


def _validated_integer(value: int, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _validated_mpf(
    value: object,
    name: str,
    *,
    strictly_positive: bool = False,
) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if strictly_positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    if not strictly_positive and result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def centered_single_endpoint_atom(
    atom_sign: int,
    residue_hit: int,
    phi_q: int,
) -> Fraction:
    """Return the exact centered correction made by one endpoint atom.

    ``atom_sign=+1`` adds a prime at ``T`` and ``atom_sign=-1`` removes a
    prime at ``2T``.  For ``T>2`` these cannot both occur: if ``T`` is an
    integer prime, ``2T`` is composite; if ``2T`` is an odd prime, ``T`` is
    not an integer.  ``residue_hit`` records whether the one atom lies in
    the selected reduced residue class.

    The correction is ``sign*(hit - 1/phi(q))`` and always has absolute
    value at most one.  This is exact rational arithmetic and is not a
    primality test.
    """

    if isinstance(atom_sign, bool) or not isinstance(atom_sign, int):
        raise TypeError("atom_sign must be an integer")
    if atom_sign not in (-1, 0, 1):
        raise ValueError("atom_sign must be -1, 0, or 1")
    residue_hit = _validated_integer(residue_hit, "residue_hit")
    if residue_hit not in (0, 1):
        raise ValueError("residue_hit must be 0 or 1")
    phi_q = _validated_integer(phi_q, "phi_q", minimum=1)
    if atom_sign == 0 and residue_hit:
        raise ValueError("a zero endpoint atom cannot hit a residue class")
    correction = atom_sign * (Fraction(residue_hit, 1) - Fraction(1, phi_q))
    if abs(correction) > 1:
        raise AssertionError("single centered endpoint correction exceeded one")
    return correction


@dataclass(frozen=True)
class CountTransferUpperComponents:
    """Upper-bound components for the centered count on ``[T,2T)``."""

    partial_summation: mp.mpf
    prime_power_removal: mp.mpf
    half_open_endpoint: mp.mpf

    @property
    def total(self) -> mp.mpf:
        return mp.fsum(
            (
                self.partial_summation,
                self.prime_power_removal,
                self.half_open_endpoint,
            )
        )


def count_transfer_upper_from_components(
    t: object,
    *,
    remainder_at_t_upper: object,
    remainder_at_2t_upper: object,
    abel_integral_upper: object,
    modulus_count: int,
    reciprocal_totient_sum: object,
) -> CountTransferUpperComponents:
    r"""Compose the exact H1c-1b.3 parameterized upper bound.

    Let ``R(u)`` bound

    ``sum_q max_(a,q)=1 |psi(u;q,a)-psi(u)/phi(q)|``

    for the same fixed modulus family at every ``u in [T,2T]``.  If the
    supplied integral bounds

    ``integral_T^(2T) R(u)/(u*log(u)^2) du``, then this function returns

    ``R(2T)/log(2T) + R(T)/log(T) + integral``
    ``+ 2*sqrt(2T)*(M + Phi) + M``,

    where ``M`` is the number of moduli and ``Phi=sum_q 1/phi(q)``.
    The second line removes prime powers and changes ``(T,2T]`` into
    Maynard's ``[T,2T)`` convention.
    """

    t_mpf = _validated_mpf(t, "t", strictly_positive=True)
    # The cited explicit prime-power package is invoked on both endpoints and
    # is recorded with the safe source domain y >= 4.  The actual Maynard
    # application is vastly larger, but the helper still fails closed here.
    if t_mpf < 4:
        raise ValueError("t must be at least 4")
    r_t = _validated_mpf(remainder_at_t_upper, "remainder_at_t_upper")
    r_2t = _validated_mpf(remainder_at_2t_upper, "remainder_at_2t_upper")
    integral = _validated_mpf(abel_integral_upper, "abel_integral_upper")
    modulus_count = _validated_integer(modulus_count, "modulus_count")
    phi_sum = _validated_mpf(reciprocal_totient_sum, "reciprocal_totient_sum")

    partial = r_2t / mp.log(2 * t_mpf) + r_t / mp.log(t_mpf) + integral
    prime_powers = (
        PRIME_POWER_CUMULATIVE_CONSTANT
        * mp.sqrt(2 * t_mpf)
        * (modulus_count + phi_sum)
    )
    endpoint = mp.mpf(modulus_count)
    return CountTransferUpperComponents(
        partial_summation=partial,
        prime_power_removal=prime_powers,
        half_open_endpoint=endpoint,
    )


def crude_normalized_count_transfer_upper(
    log_t: object,
    relative_remainder_supremum: object,
) -> CountTransferUpperComponents:
    r"""Return a safe ``T``-normalized envelope without constructing ``T``.

    Write ``rho_* = sup_[T,2T] R(u)/u``.  The elementary bounds
    ``M <= T^(1/3)`` and ``sum 1/phi(q) <= M`` give

    ``S_pi([T,2T))/T`` no larger than

    ``rho_* * (1/log(T) + 2/log(2T) + 1/log(T)^2)``
    ``+ 4*sqrt(2)*T^(-1/6) + T^(-2/3)``.

    This is a structural envelope for the next absorption stage.  It does
    not assert that a usable numerical ``rho_*`` or prime-density lower
    bound is already available.
    """

    log_t_mpf = _validated_mpf(log_t, "log_t", strictly_positive=True)
    if log_t_mpf <= mp.log(2):
        raise ValueError("log_t must correspond to t > 2")
    rho = _validated_mpf(
        relative_remainder_supremum,
        "relative_remainder_supremum",
    )
    partial = rho * (
        1 / log_t_mpf
        + 2 / (log_t_mpf + mp.log(2))
        + 1 / log_t_mpf**2
    )
    prime_powers = 4 * mp.sqrt(2) * mp.exp(-log_t_mpf / 6)
    endpoint = mp.exp(-2 * log_t_mpf / 3)
    return CountTransferUpperComponents(
        partial_summation=partial,
        prime_power_removal=prime_powers,
        half_open_endpoint=endpoint,
    )


def uniform_fixed_family_on_dyadic_interval(
    r: int = MINIMUM_SIEVE_DIMENSION,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> bool:
    """Check that the H1c-1b.2 fixed family is valid for every ``u``.

    The lower endpoint is ``log(T)=r^5`` and
    ``Q1=(log T)^A``.  Since ``log(T)>2A``, the Bordignon capacity
    ``sqrt(u)/(log u)^A`` increases on ``[T,2T]``.  The fixed ``Q1`` also
    remains below ``(log u)^A``.  Thus the same q-family and same B can be
    used under the Abel integral, not only at its two endpoints.
    """

    r = _validated_integer(r, "r", minimum=1)
    if r < MINIMUM_SIEVE_DIMENSION:
        raise ValueError(f"r must be at least {MINIMUM_SIEVE_DIMENSION}")
    log_t = mp.mpf(r**5)
    log_2t = log_t + mp.log(2)
    a = bordignon_exponent(r, transport_margin)
    a_mpf = mp.mpf(a.numerator) / a.denominator
    fixed_log_q1 = a_mpf * mp.log(log_t)
    return bool(
        bordignon_basic_statement_conditions(
            log_t, r, transport_margin=transport_margin
        )
        and bordignon_basic_statement_conditions(
            log_2t, r, transport_margin=transport_margin
        )
        and bordignon_capacity_is_increasing(
            log_t, r, transport_margin=transport_margin
        )
        and modulus_capacity_log_margin(
            log_t, r, transport_margin=transport_margin
        )
        >= 0
        and q1_within_q_log_margin(
            log_t, r, transport_margin=transport_margin
        )
        >= 0
        and fixed_log_q1 <= a_mpf * mp.log(log_2t)
    )


@dataclass(frozen=True)
class H1c1b3StructuralCertificate:
    sieve_dimension_r: int
    maynard_integer_interval: str
    target_weight: str
    selected_linear_form: str
    same_fixed_modulus_family_through_abel_integral: bool
    partial_summation_integral_sign: str
    partial_summation_identity_closed: bool
    prime_power_cumulative_constant: int
    prime_power_removal_closed: bool
    half_open_endpoint_transfer_closed: bool
    exact_total_prime_population_centered: bool
    unweighted_prime_count_transfer_closed: bool
    represented_prime_density_lower_bound_closed: bool
    full_remainder_absorption_closed: bool
    bordignon_constant_normalization_resolved: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def structural_certificate(
    r: int = MINIMUM_SIEVE_DIMENSION,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> H1c1b3StructuralCertificate:
    """Build the narrow H1c-1b.3 certificate without over-promotion."""

    r = _validated_integer(r, "r", minimum=1)
    if r < MINIMUM_SIEVE_DIMENSION:
        raise ValueError(f"r must be at least {MINIMUM_SIEVE_DIMENSION}")
    return H1c1b3StructuralCertificate(
        sieve_dimension_r=r,
        maynard_integer_interval="[T,2T)",
        target_weight="unweighted prime indicator 1_P(n)",
        selected_linear_form="identity L(n)=n",
        same_fixed_modulus_family_through_abel_integral=(
            uniform_fixed_family_on_dyadic_interval(
                r, transport_margin=transport_margin
            )
        ),
        partial_summation_integral_sign=PARTIAL_SUMMATION_INTEGRAL_SIGN,
        partial_summation_identity_closed=True,
        prime_power_cumulative_constant=PRIME_POWER_CUMULATIVE_CONSTANT,
        prime_power_removal_closed=True,
        half_open_endpoint_transfer_closed=True,
        exact_total_prime_population_centered=True,
        unweighted_prime_count_transfer_closed=True,
        represented_prime_density_lower_bound_closed=False,
        full_remainder_absorption_closed=False,
        bordignon_constant_normalization_resolved=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
