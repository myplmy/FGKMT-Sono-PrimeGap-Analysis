"""Exact regression checks for the Sono/FMT H1b-1a finite lemmas.

The proofs and source attributions live in
``docs/method/theory/17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md``.
This module deliberately checks only the finite/exact portions of that
argument.  It does not certify Maynard Proposition 6.1 and it never computes
the theorem threshold ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from math import isqrt

import mpmath as mp


H1B1A_FINITE_PRIME_PRODUCT_STOP = 2_973
H1B1A_ANALYTIC_PRIME_PRODUCT_START = 2_974
H1B1A_SMALL_PRIME_EXPONENT = Fraction(4, 1)
H1B1A_TAIL_EXPONENT = Fraction(1, 2)
H1B1A_SINGULAR_SERIES_EXPONENT = Fraction(9, 2)
H1B1A_CUTOFF_SLOPE_BOUND = Fraction(50, 1)
H1B1A_EULER_PRODUCT_COEFFICIENT = Fraction(24, 1)


@dataclass(frozen=True)
class FinitePrimeProductCertificate:
    """Exact certificate for the finite branch of the Mertens-product bound."""

    start: int
    stop: int
    count: int
    failures: tuple[int, ...]
    maximum_surrogate_ratio_k: int
    maximum_surrogate_ratio: Fraction
    rows_sha256: str


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % divisor for divisor in range(2, isqrt(n) + 1))


def log_lower_surrogate(k: int) -> Fraction:
    """Return the elementary lower bound ``2(k-1)/(k+1) <= log(k)``."""

    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k must be an integer at least 2")
    return Fraction(2 * (k - 1), k + 1)


def finite_prime_product_certificate(
    stop: int = H1B1A_FINITE_PRIME_PRODUCT_STOP,
) -> FinitePrimeProductCertificate:
    """Check ``prod_{p<=k} p/(p-1) < 8 log(k)`` without floats.

    The stronger rational comparison

    ``prod_{p<=k} p/(p-1) < 16(k-1)/(k+1)``

    is checked for every integer ``2 <= k <= stop``.  Its right-hand side is
    at most ``8 log(k)`` by :func:`log_lower_surrogate`.
    """

    if isinstance(stop, bool) or not isinstance(stop, int) or stop < 2:
        raise ValueError("stop must be an integer at least 2")

    product = Fraction(1, 1)
    failures: list[int] = []
    maximum_ratio = Fraction(0, 1)
    maximum_k = 2
    digest = sha256()

    for k in range(2, stop + 1):
        if _is_prime(k):
            product *= Fraction(k, k - 1)
        surrogate = log_lower_surrogate(k)
        target = 8 * surrogate
        if not product < target:
            failures.append(k)
        ratio = product / surrogate
        if ratio > maximum_ratio:
            maximum_ratio = ratio
            maximum_k = k
        digest.update(
            (
                f"{k}|{product.numerator}|{product.denominator}|"
                f"{target.numerator}|{target.denominator}\n"
            ).encode("ascii")
        )

    return FinitePrimeProductCertificate(
        start=2,
        stop=stop,
        count=stop - 1,
        failures=tuple(failures),
        maximum_surrogate_ratio_k=maximum_k,
        maximum_surrogate_ratio=maximum_ratio,
        rows_sha256=digest.hexdigest(),
    )


def tail_factor_log_loss_majorant(k: int, p: int) -> Fraction:
    """Return the exact upper bound for minus the logarithm of one tail factor.

    For integers ``p > 2k`` the proof gives

    ``-log((1-k/p) * (1-1/p)**(-k)) < k**2/p**2``.

    This function returns the rational right-hand side.  The analytic Taylor
    inequality establishing it is proved in the accompanying document.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if isinstance(p, bool) or not isinstance(p, int) or p <= 2 * k:
        raise ValueError("p must be an integer greater than 2k")
    return Fraction(k * k, p * p)


def telescoping_square_tail_majorant(k: int, stop: int) -> Fraction:
    """Majorize a finite square tail by an exact telescoping sum.

    ``sum_{n=2k+1..stop} 1/n^2`` is strictly below
    ``sum 1/(n(n-1)) = 1/(2k)-1/stop``.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if isinstance(stop, bool) or not isinstance(stop, int) or stop <= 2 * k:
        raise ValueError("stop must be an integer greater than 2k")
    return Fraction(1, 2 * k) - Fraction(1, stop)


def flat_bump(u: int | float | str | mp.mpf) -> mp.mpf:
    """The standard flat function ``exp(-1/u)`` for ``u>0``, else zero."""

    value = mp.mpf(u)
    return mp.exp(-1 / value) if value > 0 else mp.mpf(0)


def smooth_step(u: int | float | str | mp.mpf) -> mp.mpf:
    """A C-infinity nondecreasing step equal to 0/1 outside ``(0,1)``."""

    value = mp.mpf(u)
    if value <= 0:
        return mp.mpf(0)
    if value >= 1:
        return mp.mpf(1)
    left = flat_bump(value)
    right = flat_bump(1 - value)
    return left / (left + right)


def smooth_step_derivative(u: int | float | str | mp.mpf) -> mp.mpf:
    """Evaluate the exact analytic first derivative of :func:`smooth_step`."""

    value = mp.mpf(u)
    if value <= 0 or value >= 1:
        return mp.mpf(0)
    step = smooth_step(value)
    return step * (1 - step) * (1 / value**2 + 1 / (1 - value) ** 2)


def cutoff_psi(t: int | float | str | mp.mpf) -> mp.mpf:
    """Maynard-compatible cutoff on ``[0,infinity)`` with plateau ``[0,0.9]``."""

    value = mp.mpf(t)
    if value < 0:
        raise ValueError("t must be nonnegative")
    return smooth_step(10 * (1 - value))


def cutoff_psi_derivative(t: int | float | str | mp.mpf) -> mp.mpf:
    """Evaluate the first derivative of :func:`cutoff_psi`."""

    value = mp.mpf(t)
    if value < 0:
        raise ValueError("t must be nonnegative")
    return -10 * smooth_step_derivative(10 * (1 - value))


__all__ = [
    "FinitePrimeProductCertificate",
    "H1B1A_ANALYTIC_PRIME_PRODUCT_START",
    "H1B1A_CUTOFF_SLOPE_BOUND",
    "H1B1A_EULER_PRODUCT_COEFFICIENT",
    "H1B1A_FINITE_PRIME_PRODUCT_STOP",
    "H1B1A_SINGULAR_SERIES_EXPONENT",
    "H1B1A_SMALL_PRIME_EXPONENT",
    "H1B1A_TAIL_EXPONENT",
    "cutoff_psi",
    "cutoff_psi_derivative",
    "finite_prime_product_certificate",
    "flat_bump",
    "log_lower_surrogate",
    "smooth_step",
    "smooth_step_derivative",
    "tail_factor_log_loss_majorant",
    "telescoping_square_tail_majorant",
]
