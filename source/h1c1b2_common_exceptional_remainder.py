"""Fail-closed helpers for the H1c-1b.2 distribution bridge.

The helpers in this module encode two narrow facts:

* one exceptional modulus selected at a fixed ``Q1`` can be excluded from
  both endpoints of a dyadic interval by one prime divisor ``B``; and
* the complete twelve positive terms printed in the final NYJM version of
  Bordignon's Theorem 1.4 can be evaluated and added at those endpoints.

They do *not* convert von Mangoldt weights to unweighted prime counts, change
``(T, 2T]`` into Maynard's half-open convention, absorb the remainder into
``(log T)^(-100 r^2)``, prove Hypothesis 1(2), or produce ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from fractions import Fraction
from math import gcd, isqrt

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


R1 = Fraction(5113, 2500)  # Bordignon Theorem 1.4: 2.0452 exactly.
PUBLISHED_REMAINDER_TERM_COUNT = 12


def _validated_integer(value: int, name: str, *, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _validated_mpf(
    value: object,
    name: str,
    *,
    strictly_positive: bool = True,
) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if strictly_positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    if not strictly_positive and result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def _validated_exponent(value: int | Fraction) -> mp.mpf:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("a must be an int or Fraction")
    value = Fraction(value)
    if value <= 3:
        raise ValueError("Bordignon Theorem 1.4 requires a > 3")
    return mp.mpf(value.numerator) / value.denominator


def _is_prime_trial(value: int) -> bool:
    """Exact small-integer primality check used only by toy certificates."""

    value = _validated_integer(value, "value", minimum=2)
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def exceptional_filter_implication(q0: int, b: int, q: int) -> bool:
    """Verify the finite implication ``gcd(q,B)=1 => q0 does not divide q``.

    ``B`` is required to be a prime divisor of ``q0``.  This is a toy/exact
    logical check; it does not find Bordignon's unknown exceptional modulus.
    """

    q0 = _validated_integer(q0, "q0", minimum=2)
    b = _validated_integer(b, "b", minimum=2)
    q = _validated_integer(q, "q")
    if not _is_prime_trial(b):
        raise ValueError("b must be prime")
    if q0 % b:
        raise ValueError("b must divide q0")
    return bool(gcd(q, b) != 1 or q % q0 != 0)


@dataclass(frozen=True)
class BordignonRelativeRemainderTerms:
    """The twelve final-published RHS terms, each divided by endpoint ``u``."""

    leading_sqrt: mp.mpf
    main_log_tail: mp.mpf
    main_q1_tail: mp.mpf
    theorem12_small_modulus: mp.mpf
    induced_character_small_modulus: mp.mpf
    exceptional_zero: mp.mpf
    density_exponential: mp.mpf
    density_constant: mp.mpf
    large_modulus_sqrt: mp.mpf
    large_modulus_eleven_twelfths: mp.mpf
    large_modulus_five_sixths: mp.mpf
    large_modulus_five_sixths_log: mp.mpf

    @property
    def term_count(self) -> int:
        return len(fields(self))

    @property
    def total(self) -> mp.mpf:
        return mp.fsum(getattr(self, item.name) for item in fields(self))


def bordignon_relative_remainder_terms(
    log_u: object,
    a: int | Fraction,
    log_q1: object,
    *,
    c0_upper: object,
    c1_upper: object,
    theorem12_constant_upper: object,
) -> BordignonRelativeRemainderTerms:
    """Evaluate final NYJM Theorem 1.4's full RHS divided by ``u``.

    Parameters are kept on logarithmic scale: ``log_u=log(u)`` and
    ``log_q1=log(Q1)``.  The caller must provide valid upper bounds for
    Bordignon's ``c0``, ``c1`` and ``C(A,A-3,...)``.  The function checks the
    theorem's displayed elementary domain predicates, but deliberately cannot
    resolve the publication's ``X0`` versus ``Y0=log log X0`` notation issue.
    """

    log_u_mpf = _validated_mpf(log_u, "log_u")
    a_mpf = _validated_exponent(a)
    log_q1_mpf = _validated_mpf(log_q1, "log_q1", strictly_positive=False)
    c0 = _validated_mpf(c0_upper, "c0_upper")
    c1 = _validated_mpf(c1_upper, "c1_upper")
    c12 = _validated_mpf(
        theorem12_constant_upper,
        "theorem12_constant_upper",
        strictly_positive=False,
    )

    log_log_u = mp.log(log_u_mpf)
    required_log_log = max(mp.mpf(7), 11 * mp.log(10) / (2 * a_mpf))
    if log_log_u < required_log_log:
        raise ValueError("Bordignon Theorem 1.4 log-log condition is not met")
    if log_q1_mpf > a_mpf * log_log_u:
        raise ValueError("Q1 must satisfy 1 <= Q1 <= (log u)^A")

    delta = 1 / (2 * a_mpf * (mp.mpf(R1.numerator) / R1.denominator) * log_log_u)
    if not 0 < delta < 1:
        raise ValueError("the exceptional-zero exponent delta must lie in (0,1)")

    common_small = c1**2 * (1 + a_mpf * log_log_u) * log_u_mpf / 2

    return BordignonRelativeRemainderTerms(
        leading_sqrt=mp.exp(-log_u_mpf / 2),
        main_log_tail=(
            2 * c1 * c0 * mp.exp(-(a_mpf - mp.mpf("4.5")) * log_log_u)
        ),
        main_q1_tail=(
            2
            * c1
            * c0
            * mp.exp(mp.mpf("4.5") * log_log_u - log_q1_mpf)
        ),
        theorem12_small_modulus=(
            c1**2
            * c12
            * (1 + a_mpf * log_log_u)
            * mp.exp(-(a_mpf - 4) * log_log_u)
            / 2
        ),
        induced_character_small_modulus=(
            mp.exp(-log_u_mpf / 2 - (a_mpf - 1) * log_log_u)
            / (2 * mp.log(2))
        ),
        exceptional_zero=(
            common_small * mp.exp(-delta * log_u_mpf) / (1 - delta)
        ),
        density_exponential=(
            common_small
            * 34
            * log_u_mpf ** mp.mpf("1.52")
            * mp.exp(-mp.mpf("0.81") * mp.sqrt(log_u_mpf))
        ),
        density_constant=(
            common_small
            * (a_mpf * log_log_u / mp.log(2))
            * mp.exp(-log_u_mpf)
        ),
        large_modulus_sqrt=(
            2
            * c0
            * c1
            * mp.exp(-log_u_mpf / 2 + (a_mpf + mp.mpf("4.5")) * log_log_u)
        ),
        large_modulus_eleven_twelfths=(
            9
            * c0
            * c1
            * mp.exp(
                -log_u_mpf / 12
                + (mp.mpf("4.5") - a_mpf / 2) * log_log_u
            )
        ),
        large_modulus_five_sixths=(
            mp.mpf("2.5")
            * c0
            * c1
            * mp.exp(-log_u_mpf / 6 + mp.mpf("4.5") * log_log_u)
        ),
        large_modulus_five_sixths_log=(
            mp.mpf("1.25")
            * c0
            * c1
            * mp.exp(-log_u_mpf / 6 + mp.mpf("5.5") * log_log_u)
        ),
    )


def dyadic_remainder_over_t_upper(
    log_t: object,
    a: int | Fraction,
    log_q1: object,
    *,
    c0_upper: object,
    c1_upper: object,
    theorem12_constant_upper: object,
) -> mp.mpf:
    """Return ``[R(T)+R(2T)]/T`` using one fixed ``Q1``.

    The upper endpoint's relative remainder is multiplied by two because it is
    normalized by ``2T`` inside :func:`bordignon_relative_remainder_terms`.
    """

    log_t_mpf = _validated_mpf(log_t, "log_t")
    kwargs = {
        "c0_upper": c0_upper,
        "c1_upper": c1_upper,
        "theorem12_constant_upper": theorem12_constant_upper,
    }
    lower = bordignon_relative_remainder_terms(log_t_mpf, a, log_q1, **kwargs)
    upper = bordignon_relative_remainder_terms(
        log_t_mpf + mp.log(2), a, log_q1, **kwargs
    )
    return lower.total + 2 * upper.total


@dataclass(frozen=True)
class H1c1b2StructuralCertificate:
    sieve_dimension_r: int
    bordignon_a: Fraction
    fixed_q1_for_both_endpoints: bool
    same_exceptional_modulus_for_both_endpoints: bool
    one_prime_b_filter_implication_closed: bool
    b_is_scale_dependent_not_global: bool
    b_size_condition_available: bool
    endpoint_modulus_capacity_closed: bool
    published_remainder_terms_registered: int
    final_published_formula_required: bool
    raw_von_mangoldt_open_closed_composition_closed: bool
    half_open_endpoint_transfer_closed: bool
    prime_power_removal_closed: bool
    unweighted_prime_count_transfer_closed: bool
    exact_maynard_recentering_closed: bool
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
) -> H1c1b2StructuralCertificate:
    """Build the H1c-1b.2 structural certificate without over-promotion."""

    r = _validated_integer(r, "r")
    if r < MINIMUM_SIEVE_DIMENSION:
        raise ValueError(f"r must be at least {MINIMUM_SIEVE_DIMENSION}")
    a = bordignon_exponent(r, transport_margin)
    log_t = mp.mpf(r**5)
    endpoint_capacity = bool(
        modulus_capacity_log_margin(log_t, r, transport_margin=transport_margin)
        >= 0
        and modulus_capacity_log_margin(
            log_t + mp.log(2), r, transport_margin=transport_margin
        )
        >= 0
        and q1_within_q_log_margin(log_t, r, transport_margin=transport_margin)
        >= 0
        and bordignon_capacity_is_increasing(
            log_t, r, transport_margin=transport_margin
        )
        and bordignon_basic_statement_conditions(
            log_t, r, transport_margin=transport_margin
        )
        and bordignon_basic_statement_conditions(
            log_t + mp.log(2), r, transport_margin=transport_margin
        )
    )
    toy_filter = all(
        exceptional_filter_implication(2310, 11, q)
        for q in range(1, 5001)
    )
    return H1c1b2StructuralCertificate(
        sieve_dimension_r=r,
        bordignon_a=a,
        fixed_q1_for_both_endpoints=True,
        same_exceptional_modulus_for_both_endpoints=True,
        one_prime_b_filter_implication_closed=toy_filter,
        b_is_scale_dependent_not_global=True,
        b_size_condition_available=True,
        endpoint_modulus_capacity_closed=endpoint_capacity,
        published_remainder_terms_registered=PUBLISHED_REMAINDER_TERM_COUNT,
        final_published_formula_required=True,
        raw_von_mangoldt_open_closed_composition_closed=True,
        half_open_endpoint_transfer_closed=False,
        prime_power_removal_closed=False,
        unweighted_prime_count_transfer_closed=False,
        exact_maynard_recentering_closed=False,
        full_remainder_absorption_closed=False,
        bordignon_constant_normalization_resolved=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
