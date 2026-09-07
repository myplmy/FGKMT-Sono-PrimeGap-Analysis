"""Exact local-factor checks for the H1b-1b-2a Maynard repair.

The proof and source audit live in
``docs/method/theory/20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md``.
This module covers only the prime-local denominator families that occur in
the traced Section 8 applications of Maynard's Lemmas 8.3--8.4.  The bound
for the canonical ``W_i`` construction is deliberately separated from the
extra excluded factors introduced by a particular application.  Callers
must supply a certified logarithmic overhead for those factors; zero is not
assumed implicitly.  The module does not claim the same local statement for
an arbitrary function satisfying only ``g(p)=p+O(k)``, certify every actual
application overhead, recover the still-missing absolute GGPY multiplier,
certify the r-fold error accumulation, or compute ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

import mpmath as mp


LOCAL_FAMILY_LINEAR = "p_minus_a"
LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1 = "square_over_p_minus_1"
LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2 = (
    "square_over_p_plus_a_minus_2"
)
LOCAL_FAMILY_ADJUSTED_LINEAR = "adjusted_linear"

MAYNARD_ACTUAL_LOCAL_FAMILIES = frozenset(
    {
        LOCAL_FAMILY_LINEAR,
        LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1,
        LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
        LOCAL_FAMILY_ADJUSTED_LINEAR,
    }
)

MINIMUM_EXCLUDED_INTEGER_K_GE_2 = 2 * 3 * 5 * 7
ROSSER_SCHOENFELD_EXCEPTION_SAFE_COEFFICIENT = mp.mpf("2.50637")


@dataclass(frozen=True)
class LocalFactorCertificate:
    """Exact rational witness that one nonexcluded local factor is at least 1."""

    prime: int
    root_count_upper_bound: int
    previous_available_coordinates: int
    family: str
    denominator: Fraction
    denominator_upper_margin: Fraction
    local_factor: Fraction
    local_factor_margin: Fraction


@dataclass(frozen=True)
class UniformCgammaEvaluation:
    """Numerical evaluation of the proved parameterized lower-bound formulas.

    These ``mpmath`` values are diagnostics, not directed-rounding proof
    artifacts.  The rigorous inequalities are the symbolic formulas recorded
    in the accompanying method document.
    """

    log_excluded_integer_upper: mp.mpf
    rosser_schoenfeld_lower_bound: mp.mpf
    elementary_lower_bound: mp.mpf


def _validate_prime_local_inputs(prime: int, root_count: int) -> None:
    if isinstance(prime, bool) or not isinstance(prime, int):
        raise ValueError("prime must be an integer")
    if isinstance(root_count, bool) or not isinstance(root_count, int):
        raise ValueError("root_count must be an integer")
    if root_count < 1 or prime <= root_count:
        raise ValueError("require 1 <= root_count < prime")


def maynard_local_denominator(
    prime: int,
    root_count: int,
    family: str,
) -> Fraction:
    """Return one exact prime-local denominator from an actual Maynard call.

    ``root_count`` is ``omega(p)`` or ``omega*(p)`` as appropriate.  Each
    returned value is positive and at most ``prime-root_count``.
    """

    _validate_prime_local_inputs(prime, root_count)
    p = Fraction(prime)
    a = Fraction(root_count)

    if family == LOCAL_FAMILY_LINEAR:
        denominator = p - a
    elif family == LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1:
        denominator = (p - a) ** 2 / (p - 1)
    elif family == LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2:
        denominator = (p - a) ** 2 / (p + a - 2)
    elif family == LOCAL_FAMILY_ADJUSTED_LINEAR:
        denominator = p - a - (a - 1) / (p - 1)
    else:
        raise ValueError(f"unknown Maynard local family: {family}")

    if not 0 < denominator <= p - a:
        raise AssertionError("actual-call denominator escaped its proved range")
    return denominator


def nonexcluded_local_factor_certificate(
    prime: int,
    root_count_upper_bound: int,
    previous_available_coordinates: int,
    family: str,
) -> LocalFactorCertificate:
    """Certify the nonexcluded factor in one Lemma 8.4 iteration.

    For a nonexcluded prime, the current coordinate is available.  Hence the
    number ``n_j(p)`` of available coordinates among the earlier coordinates
    is at most ``a-1`` when the total availability is at most ``a``.  Together
    with ``g(p)<=p-a`` this gives ``g(p)+n_j(p)<=p-1`` and therefore

    ``(1-1/p) * (1 + 1/(g(p)+n_j(p))) >= 1``.
    """

    _validate_prime_local_inputs(prime, root_count_upper_bound)
    if (
        isinstance(previous_available_coordinates, bool)
        or not isinstance(previous_available_coordinates, int)
        or previous_available_coordinates < 0
        or previous_available_coordinates >= root_count_upper_bound
    ):
        raise ValueError(
            "previous_available_coordinates must lie in [0, root_count-1]"
        )

    denominator = maynard_local_denominator(
        prime,
        root_count_upper_bound,
        family,
    )
    denominator_upper_margin = (
        Fraction(prime - root_count_upper_bound) - denominator
    )
    stage_denominator = denominator + previous_available_coordinates
    local_factor = Fraction(prime - 1, prime) * (
        1 + Fraction(1, 1) / stage_denominator
    )
    local_factor_margin = local_factor - 1

    if denominator_upper_margin < 0 or local_factor_margin < 0:
        raise AssertionError("nonexcluded local-factor certificate failed")

    return LocalFactorCertificate(
        prime=prime,
        root_count_upper_bound=root_count_upper_bound,
        previous_available_coordinates=previous_available_coordinates,
        family=family,
        denominator=denominator,
        denominator_upper_margin=denominator_upper_margin,
        local_factor=local_factor,
        local_factor_margin=local_factor_margin,
    )


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    return all(value % divisor for divisor in range(3, isqrt(value) + 1, 2))


def excluded_totient_ratio(prime_divisors: tuple[int, ...]) -> Fraction:
    """Return ``prod_{p|Q}(1-1/p)=phi(Q)/Q`` from distinct prime divisors."""

    distinct = tuple(sorted(set(prime_divisors)))
    if len(distinct) != len(prime_divisors):
        raise ValueError("prime_divisors must not contain duplicates")
    if any(not _is_prime(prime) for prime in distinct):
        raise ValueError("every entry must be prime")

    ratio = Fraction(1, 1)
    for prime in distinct:
        ratio *= Fraction(prime - 1, prime)
    return ratio


def maynard_base_log_excluded_integer_upper(
    *,
    k: int,
    r: int,
    iteration: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
) -> mp.mpf:
    """Evaluate the canonical-``W_i`` part of ``log(Q_j)``.

    Here ``Q_j=W_{j+1}*product_{i=j+2}^r e_i`` and ``log_r=log(R)``.
    The formula replaces Maynard's printed ``R^{O(k^2)}`` using the actual
    Section 8 construction of the canonical ``W_i``.  It does *not* include
    application-specific factors such as ``d``, ``r``, ``a_m`` or ``W_0``.
    It is parameterized by the still user-selected/theorem-selected values
    ``alpha``, ``theta``, and ``R``.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k must be an integer at least 2")
    if isinstance(r, bool) or not isinstance(r, int) or not 1 <= r <= k:
        raise ValueError("r must be an integer in [1,k]")
    if (
        isinstance(iteration, bool)
        or not isinstance(iteration, int)
        or not 0 <= iteration < r
    ):
        raise ValueError("iteration must be an integer in [0,r-1]")

    alpha_value = mp.mpf(alpha)
    theta_value = mp.mpf(theta)
    log_r_value = mp.mpf(log_r)
    if alpha_value <= 0:
        raise ValueError("alpha must be positive")
    if not 0 < theta_value < 1:
        raise ValueError("theta must lie in (0,1)")
    if log_r_value <= 0:
        raise ValueError("log_r must be positive")

    coefficient_exponent = (
        10
        * alpha_value
        * (2 * k * k - k + 1)
        / theta_value
    )
    remaining_coordinates = r - iteration - 1
    return (
        2 * k * k * mp.log(2 * k * k)
        + k * (k - 1) * mp.log(2)
        + (coefficient_exponent + remaining_coordinates) * log_r_value
    )


def maynard_log_excluded_integer_upper(
    *,
    k: int,
    r: int,
    iteration: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
    application_log_overhead: int | float | str | mp.mpf,
) -> mp.mpf:
    """Add a certified application-specific overhead to the base bound.

    ``application_log_overhead`` must bound the logarithm of every extra
    factor in the effective excluded modulus beyond the canonical ``W_i``
    construction.  It is a required argument so that an unaudited actual
    application cannot silently use zero overhead.
    """

    overhead = mp.mpf(application_log_overhead)
    if overhead < 0:
        raise ValueError("application_log_overhead must be nonnegative")
    return maynard_base_log_excluded_integer_upper(
        k=k,
        r=r,
        iteration=iteration,
        alpha=alpha,
        theta=theta,
        log_r=log_r,
    ) + overhead


def rosser_schoenfeld_cgamma_lower_bound(
    log_excluded_integer_upper: int | float | str | mp.mpf,
) -> mp.mpf:
    """Evaluate the sharp symbolic lower-bound route from Theorem 15.

    If an actual excluded integer satisfies
    ``210 <= Q <= exp(Lambda)``, Rosser--Schoenfeld (3.41)--(3.42) gives

    ``c_gamma >= phi(Q)/Q > 1/(exp(EulerGamma)*log(Lambda)+2.50637)``.

    The replacement of the reciprocal term by ``2.50637`` uses
    ``log(log(Q))>1`` for ``Q>=210``.
    """

    upper = mp.mpf(log_excluded_integer_upper)
    if upper < mp.log(MINIMUM_EXCLUDED_INTEGER_K_GE_2):
        raise ValueError("log upper bound must cover an excluded integer >=210")
    return 1 / (
        mp.exp(mp.euler) * mp.log(upper)
        + ROSSER_SCHOENFELD_EXCEPTION_SAFE_COEFFICIENT
    )


def elementary_cgamma_lower_bound(
    log_excluded_integer_upper: int | float | str | mp.mpf,
) -> mp.mpf:
    """Evaluate the simpler safe bound ``1/[3(1+log(Lambda))]``.

    It follows from the same Rosser--Schoenfeld inequality together with the
    elementary relaxations ``exp(EulerGamma)<3`` and ``2.50637<3``.
    """

    upper = mp.mpf(log_excluded_integer_upper)
    if upper < mp.log(MINIMUM_EXCLUDED_INTEGER_K_GE_2):
        raise ValueError("log upper bound must cover an excluded integer >=210")
    return 1 / (3 * (1 + mp.log(upper)))


def maynard_uniform_cgamma_evaluation(
    *,
    k: int,
    r: int,
    iteration: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
    application_log_overhead: int | float | str | mp.mpf,
) -> UniformCgammaEvaluation:
    """Evaluate both conditional lower-bound formulas for one audited call."""

    upper = maynard_log_excluded_integer_upper(
        k=k,
        r=r,
        iteration=iteration,
        alpha=alpha,
        theta=theta,
        log_r=log_r,
        application_log_overhead=application_log_overhead,
    )
    rosser = rosser_schoenfeld_cgamma_lower_bound(upper)
    elementary = elementary_cgamma_lower_bound(upper)
    if not rosser > elementary > 0:
        raise AssertionError("unexpected ordering of c_gamma lower bounds")
    return UniformCgammaEvaluation(
        log_excluded_integer_upper=upper,
        rosser_schoenfeld_lower_bound=rosser,
        elementary_lower_bound=elementary,
    )


__all__ = [
    "LOCAL_FAMILY_ADJUSTED_LINEAR",
    "LOCAL_FAMILY_LINEAR",
    "LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1",
    "LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2",
    "LocalFactorCertificate",
    "MAYNARD_ACTUAL_LOCAL_FAMILIES",
    "MINIMUM_EXCLUDED_INTEGER_K_GE_2",
    "ROSSER_SCHOENFELD_EXCEPTION_SAFE_COEFFICIENT",
    "UniformCgammaEvaluation",
    "elementary_cgamma_lower_bound",
    "excluded_totient_ratio",
    "maynard_base_log_excluded_integer_upper",
    "maynard_local_denominator",
    "maynard_log_excluded_integer_upper",
    "maynard_uniform_cgamma_evaluation",
    "nonexcluded_local_factor_certificate",
    "rosser_schoenfeld_cgamma_lower_bound",
]
