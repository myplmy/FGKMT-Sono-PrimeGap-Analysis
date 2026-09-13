"""Finite constants for the Jutila Lemma 5 harmonic lower bound.

The analytic input is Corollary 3.4(b) of S. Zuniga Alterman,
"Explicit averages of square-free supported functions: to the edge of the
convolution method", Colloquium Mathematicum 168 (2022), 1--23.

This module evaluates the published constants and the elementary finite
transfer used by the project.  It does not prove the cited analytic theorem,
Jutila Lemma 6, the numerical PAP package, or a value of X_cert.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

import gmpy2
import mpmath as mp


JL5_SOURCE_ERROR_COEFFICIENT = Fraction(1277, 500)


@dataclass(frozen=True)
class JutilaJL5FiniteEvaluation:
    """High-precision evaluation of source constants and a sufficient cutoff."""

    q: int
    prime_divisors: tuple[int, ...]
    eta: mp.mpf
    c_q: mp.mpf
    phi_over_q: mp.mpf
    b_factor: mp.mpf
    source_error_coefficient: mp.mpf
    source_error_scale: mp.mpf
    error_budget_ratio: mp.mpf
    original_jutila_cutoff: mp.mpf
    simple_error_cutoff: mp.mpf
    sufficient_cutoff: mp.mpf
    diagnostic_ceiling: int
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    jutila_lemma6_closed: bool
    numerical_x_cert_ready: bool


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def validate_complete_prime_divisors(
    q: int, prime_divisors: Iterable[int]
) -> tuple[int, ...]:
    """Check that the supplied distinct primes give the complete support of q.

    This is a runtime consistency check for the numerical ledger.  The final
    proof certificate must still preserve the factorization provenance.
    """

    modulus = _positive_integer(q, "q")
    try:
        raw_factors = tuple(prime_divisors)
    except TypeError as exc:
        raise ValueError("prime_divisors must be an iterable of integers") from exc
    if any(isinstance(value, bool) or not isinstance(value, int) for value in raw_factors):
        raise ValueError("prime_divisors must be an iterable of integers")
    factors = raw_factors
    if factors != tuple(sorted(set(factors))):
        raise ValueError("prime_divisors must be strictly increasing and distinct")

    remainder = modulus
    for prime in factors:
        if prime < 2 or not bool(gmpy2.is_prime(prime)):
            raise ValueError(f"{prime} is not prime")
        if remainder % prime != 0:
            raise ValueError(f"{prime} does not divide q")
        while remainder % prime == 0:
            remainder //= prime
    if remainder != 1:
        raise ValueError("prime_divisors do not contain the complete prime support of q")
    return factors


def jl5_main_coefficient(prime_divisors: Iterable[int]) -> mp.mpf:
    """Return c_q = (6/pi^2) product over p|q of p/(p+1)."""

    result = mp.mpf(6) / mp.pi**2
    for prime in prime_divisors:
        result *= mp.mpf(prime) / (prime + 1)
    return result


def phi_over_q(prime_divisors: Iterable[int]) -> mp.mpf:
    """Return phi(q)/q from the distinct prime support."""

    result = mp.mpf(1)
    for prime in prime_divisors:
        result *= mp.mpf(prime - 1) / prime
    return result


def jl5_b_factor(prime_divisors: Iterable[int]) -> mp.mpf:
    """Return the published B_q product in Corollary 3.4(b)."""

    result = mp.mpf(1)
    one_third = mp.mpf(1) / 3
    for prime in prime_divisors:
        p = mp.mpf(prime)
        result *= 1 + (p ** (2 * one_third) - 1) / (p ** (4 * one_third) + 1)
    return result


def build_jl5_finite_evaluation(
    q: int,
    prime_divisors: Iterable[int],
    eta: int | str | Fraction | mp.mpf,
) -> JutilaJL5FiniteEvaluation:
    """Evaluate a sufficient finite lower-bound formula.

    The source gives

        S_q(R) = c_q (log R + b_q) + error,
        abs(error) <= 2.554 B_q R^(-1/3),

    with b_q > 0.  If A = 2.554 B_q / (eta c_q), then

        R >= max(exp(sqrt(log q)), e, A^3)

    implies S_q(R) >= (1-eta)c_q log R.  It also implies the weaker
    Jutila-Lemma-6 main coefficient with c_q replaced by
    (6/pi^2) phi(q)/q.  The two further absolute errors in Lemma 6 are not
    included here.
    """

    factors = validate_complete_prime_divisors(q, prime_divisors)
    with mp.workdps(max(mp.mp.dps, 80)):
        try:
            eta_mpf = (
                mp.mpf(eta.numerator) / mp.mpf(eta.denominator)
                if isinstance(eta, Fraction)
                else mp.mpf(eta)
            )
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise ValueError("eta must be a real number in (0, 1]") from exc
        if not mp.isfinite(eta_mpf) or not (0 < eta_mpf <= 1):
            raise ValueError("eta must be a real number in (0, 1]")

        c_q = jl5_main_coefficient(factors)
        phi_ratio = phi_over_q(factors)
        b_factor = jl5_b_factor(factors)
        source_coefficient = mp.mpf(JL5_SOURCE_ERROR_COEFFICIENT.numerator) / mp.mpf(
            JL5_SOURCE_ERROR_COEFFICIENT.denominator
        )
        error_scale = source_coefficient * b_factor
        budget_ratio = error_scale / (eta_mpf * c_q)

        log_q = mp.log(q)
        original_cutoff = mp.exp(mp.sqrt(log_q))
        simple_error_cutoff = budget_ratio**3
        sufficient_cutoff = max(original_cutoff, mp.e, simple_error_cutoff)
        diagnostic_ceiling = int(mp.ceil(sufficient_cutoff))

    return JutilaJL5FiniteEvaluation(
        q=q,
        prime_divisors=factors,
        eta=eta_mpf,
        c_q=c_q,
        phi_over_q=phi_ratio,
        b_factor=b_factor,
        source_error_coefficient=source_coefficient,
        source_error_scale=error_scale,
        error_budget_ratio=budget_ratio,
        original_jutila_cutoff=original_cutoff,
        simple_error_cutoff=simple_error_cutoff,
        sufficient_cutoff=sufficient_cutoff,
        diagnostic_ceiling=diagnostic_ceiling,
        rigorous_interval_certificate=False,
        source_theorem_local_axiom_used=False,
        jutila_lemma6_closed=False,
        numerical_x_cert_ready=False,
    )


def finite_lower_bound_gate(
    evaluation: JutilaJL5FiniteEvaluation, r_value: int | str | mp.mpf
) -> bool:
    """Return a high-precision diagnostic comparison with the stored cutoff."""

    try:
        r_mpf = mp.mpf(r_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("R must be a positive real number") from exc
    if not mp.isfinite(r_mpf) or r_mpf <= 0:
        raise ValueError("R must be a positive real number")
    return bool(r_mpf >= evaluation.sufficient_cutoff)


def source_error_bound(
    evaluation: JutilaJL5FiniteEvaluation, r_value: int | str | mp.mpf
) -> mp.mpf:
    """Evaluate the published absolute error bound at R."""

    r_mpf = mp.mpf(r_value)
    if not mp.isfinite(r_mpf) or r_mpf <= 0:
        raise ValueError("R must be a positive real number")
    return evaluation.source_error_scale / mp.root(r_mpf, 3)


__all__ = [
    "JL5_SOURCE_ERROR_COEFFICIENT",
    "JutilaJL5FiniteEvaluation",
    "build_jl5_finite_evaluation",
    "finite_lower_bound_gate",
    "jl5_b_factor",
    "jl5_main_coefficient",
    "phi_over_q",
    "source_error_bound",
    "validate_complete_prime_divisors",
]
