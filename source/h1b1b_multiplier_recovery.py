"""Exact contracts for the Sono/FMT H1b-1b multiplier recovery.

The accompanying proof is recorded in
``docs/method/theory/18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md``.
This module checks the finite rational inequalities used to make Maynard's
Lemma 8.2 explicit and the *conditional* partial-summation transfer from
GGPY Lemma 3 to Lemma 4 when ``kappa=1``.  It deliberately does not invent
the still-missing Halberstam--Richert base multiplier, certify Maynard
Lemma 8.4, or compute ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

import mpmath as mp

from source.h1b1a_explicit_package import (
    H1B1A_CUTOFF_SLOPE_BOUND,
    cutoff_psi,
)


H1B1B_LN2_LOWER_BOUND = Fraction(69, 100)
H1B1B_INV_SQRT2_UPPER_BOUND = Fraction(71, 100)
H1B1B_NORMALIZED_LIPSCHITZ_UPPER_BOUND = Fraction(6119, 69)
H1B1B_LEMMA82_MULTIPLIER = 89
H1B1B_GGPY4_KAPPA1_TRANSFER_FACTOR = 2


@dataclass(frozen=True)
class Lemma82UniformCertificate:
    """Exact rational certificate for the uniform Lemma 8.2 multiplier."""

    k_minimum: int
    cutoff_slope_bound: Fraction
    ln2_lower_bound: Fraction
    inverse_sqrt2_upper_bound: Fraction
    normalized_multiplier_upper_bound: Fraction
    certified_integer_multiplier: int


@dataclass(frozen=True)
class GGPY4Kappa1TransferCertificate:
    """Conditional transfer of a Lemma 3 error constant into Lemma 4.

    ``lemma3_multiplier`` denotes a certified number ``C3`` such that

    ``|E(u)| <= C3 * c_gamma * (L + 1)``

    uniformly on the required interval.  The returned Lemma 4 multiplier is
    valid for GGPY's norm ``M(F)=sup(|F|+|F'|)``.  This function does not
    establish that such a ``C3`` is available.
    """

    lemma3_multiplier: Fraction
    boundary_factor: int
    derivative_integral_factor: int
    lemma4_multiplier: Fraction


def lemma82_uniform_certificate() -> Lemma82UniformCertificate:
    """Return the exact rational proof data for multiplier 89.

    The proof uses

    ``log(2) > 2*(1/3 + 1/81) = 56/81 > 69/100``

    and ``1/sqrt(2) < 71/100``.  Hence for every integer ``k>=2``

    ``1 + 50*(1+sqrt(k))/(k*log(k)) < 6119/69 < 89``.
    """

    series_lower_bound = 2 * (Fraction(1, 3) + Fraction(1, 81))
    if not series_lower_bound > H1B1B_LN2_LOWER_BOUND:
        raise AssertionError("the rational lower bound for log(2) failed")
    if not H1B1B_INV_SQRT2_UPPER_BOUND**2 > Fraction(1, 2):
        raise AssertionError("the rational upper bound for 1/sqrt(2) failed")

    numerator_bound = Fraction(1, 2) + H1B1B_INV_SQRT2_UPPER_BOUND
    ratio_bound = numerator_bound / H1B1B_LN2_LOWER_BOUND
    normalized_bound = 1 + H1B1A_CUTOFF_SLOPE_BOUND * ratio_bound
    if normalized_bound != H1B1B_NORMALIZED_LIPSCHITZ_UPPER_BOUND:
        raise AssertionError("unexpected normalized multiplier bound")
    if not normalized_bound < H1B1B_LEMMA82_MULTIPLIER:
        raise AssertionError("integer multiplier does not dominate the bound")

    return Lemma82UniformCertificate(
        k_minimum=2,
        cutoff_slope_bound=H1B1A_CUTOFF_SLOPE_BOUND,
        ln2_lower_bound=H1B1B_LN2_LOWER_BOUND,
        inverse_sqrt2_upper_bound=H1B1B_INV_SQRT2_UPPER_BOUND,
        normalized_multiplier_upper_bound=normalized_bound,
        certified_integer_multiplier=H1B1B_LEMMA82_MULTIPLIER,
    )


def lemma82_normalized_multiplier(k: int) -> mp.mpf:
    """Evaluate the unrounded multiplier ``1+50(1+sqrt(k))/(k log k)``."""

    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k must be an integer at least 2")
    value = mp.mpf(k)
    slope = mp.mpf(H1B1A_CUTOFF_SLOPE_BOUND.numerator) / mp.mpf(
        H1B1A_CUTOFF_SLOPE_BOUND.denominator
    )
    return 1 + slope * (1 + mp.sqrt(value)) / (value * mp.log(value))


def maynard_f(arguments: Sequence[int | float | str | mp.mpf]) -> mp.mpf:
    """Evaluate Maynard's Section 8 test function ``F`` for regression tests."""

    values = tuple(mp.mpf(value) for value in arguments)
    if len(values) < 2 or any(value < 0 for value in values):
        raise ValueError("arguments must contain at least two nonnegative values")
    k = len(values)
    t_k = mp.mpf(k) * mp.log(k)
    u_k = 1 / mp.sqrt(k)
    result = cutoff_psi(sum(values))
    for value in values:
        result *= cutoff_psi(value / u_k) / (1 + t_k * value)
    return result


def maynard_f2(arguments: Sequence[int | float | str | mp.mpf]) -> mp.mpf:
    """Evaluate Maynard's nonnegative error majorant ``F_2``."""

    values = tuple(mp.mpf(value) for value in arguments)
    if len(values) < 2 or any(value < 0 for value in values):
        raise ValueError("arguments must contain at least two nonnegative values")
    k = len(values)
    t_k = mp.mpf(k) * mp.log(k)
    u_k = 1 / mp.sqrt(k)
    total = mp.mpf(0)
    for j, value_j in enumerate(values):
        term = cutoff_psi(value_j / 2) / (1 + t_k * value_j)
        for i, value_i in enumerate(values):
            if i != j:
                term *= cutoff_psi(value_i / u_k) / (1 + t_k * value_i)
        total += term
    return total


def lemma82_one_coordinate_margin(
    arguments: Sequence[int | float | str | mp.mpf],
    coordinate: int,
    delta: int | float | str | mp.mpf,
) -> mp.mpf:
    """Return ``89*T_k*delta*F2(u) - |F(u+delta e_j)-F(u)|``.

    Nonnegativity is a numerical regression check of the proved inequality;
    it is not itself the proof.
    """

    values = tuple(mp.mpf(value) for value in arguments)
    if len(values) < 2 or any(value < 0 for value in values):
        raise ValueError("arguments must contain at least two nonnegative values")
    if isinstance(coordinate, bool) or not isinstance(coordinate, int):
        raise ValueError("coordinate must be an integer")
    if coordinate < 0 or coordinate >= len(values):
        raise ValueError("coordinate is out of range")
    displacement = mp.mpf(delta)
    if displacement < 0:
        raise ValueError("delta must be nonnegative")

    shifted = list(values)
    shifted[coordinate] += displacement
    k = len(values)
    t_k = mp.mpf(k) * mp.log(k)
    left = abs(maynard_f(shifted) - maynard_f(values))
    right = (
        H1B1B_LEMMA82_MULTIPLIER
        * t_k
        * displacement
        * maynard_f2(values)
    )
    return right - left


def ggpy4_kappa1_transfer_certificate(
    lemma3_multiplier: int | Fraction,
) -> GGPY4Kappa1TransferCertificate:
    """Transfer an assumed explicit GGPY Lemma 3 constant to Lemma 4.

    One copy of ``C3`` bounds the upper boundary term and one copy bounds the
    derivative integral.  With GGPY's pointwise-sum norm this gives the safe
    multiplier ``C4=2*C3``.  The missing HR reconstruction is precisely the
    missing certified input ``C3(A1,A2)`` and its common finite range.
    """

    multiplier = Fraction(lemma3_multiplier)
    if multiplier <= 0:
        raise ValueError("lemma3_multiplier must be positive")
    return GGPY4Kappa1TransferCertificate(
        lemma3_multiplier=multiplier,
        boundary_factor=1,
        derivative_integral_factor=1,
        lemma4_multiplier=H1B1B_GGPY4_KAPPA1_TRANSFER_FACTOR * multiplier,
    )


__all__ = [
    "GGPY4Kappa1TransferCertificate",
    "H1B1B_GGPY4_KAPPA1_TRANSFER_FACTOR",
    "H1B1B_INV_SQRT2_UPPER_BOUND",
    "H1B1B_LEMMA82_MULTIPLIER",
    "H1B1B_LN2_LOWER_BOUND",
    "H1B1B_NORMALIZED_LIPSCHITZ_UPPER_BOUND",
    "Lemma82UniformCertificate",
    "ggpy4_kappa1_transfer_certificate",
    "lemma82_normalized_multiplier",
    "lemma82_one_coordinate_margin",
    "lemma82_uniform_certificate",
    "maynard_f",
    "maynard_f2",
]
