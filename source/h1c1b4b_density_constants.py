"""Exact elementary certificate for H1c-1b.4b density and constants.

This module closes two inputs that are independent of Bordignon's unresolved
Theorem 1.2 constant:

* an explicit lower bound for the exact half-open prime population
  ``P_T = #{p : T <= p < 2T}``; and
* safe upper bounds ``c0 < 49`` and ``c1 < 3`` for the constants printed in
  Bordignon's final Theorem 1.4.

The rational checks below are proof witnesses, not floating-point estimates.
They do not close the remaining twelve-term absorption or ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import MINIMUM_SIEVE_DIMENSION


ROSSER_SCHOENFELD_INTERVAL_NUMERATOR = 3
ROSSER_SCHOENFELD_INTERVAL_DENOMINATOR = 5
ROSSER_SCHOENFELD_INTERVAL_MINIMUM = Fraction(41, 2)
ROSSER_SCHOENFELD_PSI_RATIO_UPPER = Fraction(103883, 100000)
SAFE_C0_UPPER = 49
SAFE_C1_UPPER = 3
PROJECT_DENSITY_DENOMINATOR = 2


def _validated_integer(value: int, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _validated_mpf(value: object, name: str, *, positive: bool = False) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _log_rational_bounds(value: Fraction, terms: int = 24) -> tuple[Fraction, Fraction]:
    r"""Return exact rational lower/upper bounds for log(value), value>1.

    With ``z=(value-1)/(value+1)`` we use

    ``log(value)=2*sum_(k>=0) z^(2k+1)/(2k+1)``.

    The omitted positive tail is at most
    ``2*z^(2n+1)/((2n+1)*(1-z^2))``.
    """

    if not isinstance(value, Fraction):
        raise TypeError("value must be a Fraction")
    if value <= 1:
        raise ValueError("value must exceed one")
    terms = _validated_integer(terms, "terms", minimum=1)
    z = (value - 1) / (value + 1)
    partial = Fraction(0, 1)
    for k in range(terms):
        partial += 2 * z ** (2 * k + 1) / (2 * k + 1)
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z**2))
    return partial, partial + tail


def _atan_unit_fraction_bounds(denominator: int, pairs: int = 8) -> tuple[Fraction, Fraction]:
    """Return exact alternating-series bounds for atan(1/denominator)."""

    denominator = _validated_integer(denominator, "denominator", minimum=2)
    pairs = _validated_integer(pairs, "pairs", minimum=1)
    z = Fraction(1, denominator)
    lower = Fraction(0, 1)
    for k in range(2 * pairs):
        lower += (-1) ** k * z ** (2 * k + 1) / (2 * k + 1)
    upper = lower + z ** (4 * pairs + 1) / (4 * pairs + 1)
    return lower, upper


def elementary_transcendental_bound_checks() -> dict[str, bool]:
    """Verify the rational inequalities used in the c0 proof."""

    log2_lower, log2_upper = _log_rational_bounds(Fraction(2, 1))
    log43_lower, _ = _log_rational_bounds(Fraction(4, 3))
    log241_lower, log241_upper = _log_rational_bounds(Fraction(241, 100))
    atan5_lower, _ = _atan_unit_fraction_bounds(5)
    _, atan239_upper = _atan_unit_fraction_bounds(239)
    pi_lower = 16 * atan5_lower - 4 * atan239_upper

    return {
        "two_power_13_over_2_lt_90_51": Fraction(2**13, 1)
        < Fraction(9051, 100) ** 2,
        "log2_gt_0_693": log2_lower > Fraction(693, 1000),
        "log2_over_log4_3_lt_2_41": log2_upper
        < Fraction(241, 100) * log43_lower,
        "log_2_41_lt_0_88": log241_upper < Fraction(22, 25),
        "pi_gt_3_1415": pi_lower > Fraction(6283, 2000),
        "sqrt_1_03883_lt_1_0193": ROSSER_SCHOENFELD_PSI_RATIO_UPPER
        < Fraction(10193, 10000) ** 2,
        "log_2_41_lower_is_positive": log241_lower > 0,
    }


def bordignon_c0_rational_upper() -> Fraction:
    r"""Return a rigorous rational majorant for Bordignon's printed c0.

    Rosser--Schoenfeld Theorem 12 gives ``psi(113)/113 < 1.03883``.
    The remaining transcendental factors are replaced by the exact rational
    inequalities checked by :func:`elementary_transcendental_bound_checks`.
    """

    checks = elementary_transcendental_bound_checks()
    if not all(checks.values()):
        raise AssertionError(f"elementary c0 bound failed: {checks}")

    two_power = Fraction(9051, 100)
    two_plus_log_ratio = Fraction(72, 25)
    pi_lower = Fraction(6283, 2000)
    log2_lower = Fraction(693, 1000)
    bracket_upper = Fraction(1, 3) + Fraction(3, 2) / log2_lower
    square_root_upper = Fraction(10193, 10000)
    result = (
        two_power
        * two_plus_log_ratio
        * bracket_upper
        * square_root_upper
        / (9 * pi_lower * log2_lower**2)
    )
    if result >= SAFE_C0_UPPER:
        raise AssertionError("rational c0 upper failed to fit below 49")
    return result


def bordignon_c1_telescope_upper() -> int:
    r"""Return the safe integer upper ``c1<3``.

    ``log(1+u)<u`` and enlargement from primes to all integers give

    ``log c1 < sum_(n>=2) 1/(n(n-1)) = 1``.

    Hence ``c1<e<3``.  The last inequality follows from
    ``e=2+sum_(n>=2)1/n! < 2+sum_(n>=2)1/2^(n-1)=3``.
    """

    return SAFE_C1_UPPER


def half_open_prime_density_source_lower(log_t: object) -> mp.mpf:
    r"""Return ``3/(5 log T)-1/T`` for the half-open prime interval.

    Rosser--Schoenfeld (3.8) gives
    ``pi(2T)-pi(T)>3T/(5log T)`` for ``T>=20.5``.  Replacing the source's
    endpoint convention by ``[T,2T)`` loses at most one prime, so
    ``P_T/T > 3/(5log T)-1/T``.
    """

    log_t_mpf = _validated_mpf(log_t, "log_t", positive=True)
    if log_t_mpf < mp.log(mp.mpf(41) / 2):
        raise ValueError("Rosser-Schoenfeld interval bound requires T>=20.5")
    return mp.mpf(3) / (5 * log_t_mpf) - mp.exp(-log_t_mpf)


def project_half_open_density_lower(log_t: object) -> mp.mpf:
    r"""Return the project bound ``P_T/T > 1/(2 log T)``.

    The actual application has ``log T>=36^5``.  For every ``L>=20``, the
    exponential series gives ``exp(L)>L^2/2>=10L`` and hence
    ``exp(-L)<1/(10L)``.  Combining this with the source bound yields
    ``P_T/T>3/(5L)-1/(10L)=1/(2L)``.
    """

    log_t_mpf = _validated_mpf(log_t, "log_t", positive=True)
    minimum_log_t = mp.mpf(MINIMUM_SIEVE_DIMENSION**5)
    if log_t_mpf < minimum_log_t:
        raise ValueError(
            f"actual density certificate requires log_t>={MINIMUM_SIEVE_DIMENSION}^5"
        )
    if minimum_log_t < 20:
        raise AssertionError("stored actual log-scale floor must exceed 20")
    return 1 / (PROJECT_DENSITY_DENOMINATOR * log_t_mpf)


def density_margin_over_project_lower(log_t: object) -> mp.mpf:
    """Return the source half-open lower minus the simpler project lower."""

    log_t_mpf = _validated_mpf(log_t, "log_t", positive=True)
    return half_open_prime_density_source_lower(log_t_mpf) - (
        1 / (PROJECT_DENSITY_DENOMINATOR * log_t_mpf)
    )


@dataclass(frozen=True)
class H1c1b4bDensityConstantsCertificate:
    sieve_dimension_r: int
    log_t_floor: int
    exact_half_open_prime_population: str
    endpoint_loss_at_most_one: bool
    source_interval_density_applies: bool
    project_density_lower: str
    represented_prime_density_lower_bound_closed: bool
    bordignon_c0_upper: int
    bordignon_c0_upper_closed: bool
    bordignon_c1_upper: int
    bordignon_c1_upper_closed: bool
    numerical_theorem12_constant_upper_closed: bool
    full_remainder_absorption_closed: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def structural_certificate(
    r: int = MINIMUM_SIEVE_DIMENSION,
) -> H1c1b4bDensityConstantsCertificate:
    """Build the narrow H1c-1b.4b certificate."""

    r = _validated_integer(r, "r", minimum=MINIMUM_SIEVE_DIMENSION)
    log_t_floor = r**5
    if density_margin_over_project_lower(log_t_floor) <= 0:
        raise AssertionError("source density did not dominate project density")
    if bordignon_c0_rational_upper() >= SAFE_C0_UPPER:
        raise AssertionError("c0 certificate failed")
    return H1c1b4bDensityConstantsCertificate(
        sieve_dimension_r=r,
        log_t_floor=log_t_floor,
        exact_half_open_prime_population="P_T=#{p:T<=p<2T}",
        endpoint_loss_at_most_one=True,
        source_interval_density_applies=True,
        project_density_lower="P_T>T/(2*log(T))",
        represented_prime_density_lower_bound_closed=True,
        bordignon_c0_upper=SAFE_C0_UPPER,
        bordignon_c0_upper_closed=True,
        bordignon_c1_upper=bordignon_c1_telescope_upper(),
        bordignon_c1_upper_closed=True,
        numerical_theorem12_constant_upper_closed=False,
        full_remainder_absorption_closed=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
