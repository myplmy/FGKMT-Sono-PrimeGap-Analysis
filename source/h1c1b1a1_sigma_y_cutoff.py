"""Explicit H1c-1b.1a.1 upper cutoff for the FMT sigma*y factor.

The proof uses Rosser--Schoenfeld's explicit bounds for

    P(t) = product_{p <= t} (1 - 1/p)

and the exact FMT definitions

    a = (log x)**20,
    z = x**(log_3(x)/(4*log_2(x))),
    sigma = product_{a < p <= z, p != B0} (1 - 1/p).

Only logarithms of the astronomically large cutoff are evaluated.  This
module does not enumerate primes, run a maximal-gap experiment, prove the
remaining distribution package, or compute the final theorem threshold
``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp


MINIMUM_ENDPOINT_DIMENSION = 36
MINIMUM_LOG_X_OVER_TWO = MINIMUM_ENDPOINT_DIMENSION**5
ROSSER_LOWER_ENDPOINT = 285
COARSE_LOG_ENDPOINT = 300
COARSE_PRODUCT_ERROR = Fraction(1, 1000)
COARSE_EXCEPTIONAL_FACTOR = Fraction(1000, 999)
COARSE_SIGMA_Y_MULTIPLIER = Fraction(1_001_000, 998_001)
TARGET_SIGMA_Y_MULTIPLIER = Fraction(26, 25)


def minimum_log_x() -> mp.mpf:
    """Return log(2*exp(36**5)) without constructing the huge number."""

    return mp.mpf(MINIMUM_LOG_X_OVER_TWO) + mp.log(2)


def minimum_log10_x() -> mp.mpf:
    """Return log_10(2*exp(36**5))."""

    return minimum_log_x() / mp.log(10)


def _validated_log_x(log_x: object) -> mp.mpf:
    value = mp.mpf(log_x)
    if not mp.isfinite(value):
        raise ValueError("log_x must be finite")
    if value < minimum_log_x():
        raise ValueError("log_x must satisfy log(x/2) >= 36**5")
    return value


def exact_sigma_y_cutoff_certificate() -> bool:
    """Check the integer and rational skeleton of the finite proof.

    The proof document supplies the monotonicity and exponential-series
    arguments.  In particular, ``e < 11/4 < 3`` follows from
    ``n! >= 2*3**(n-2)`` for ``n >= 2``.
    """

    exp_one_lower = Fraction(5, 2)
    exp_one_upper = Fraction(11, 4)
    product_from_coarse_factors = (
        (1 + COARSE_PRODUCT_ERROR)
        / (1 - COARSE_PRODUCT_ERROR)
        * COARSE_EXCEPTIONAL_FACTOR
    )
    return bool(
        exp_one_lower > 2
        and exp_one_upper < 3
        and 27 < 36
        and 9 < 15
        and 15**4 > 28_800
        and 2**300 > ROSSER_LOWER_ENDPOINT
        and 2**300 > 1000
        and Fraction(1, 2 * COARSE_LOG_ENDPOINT**2)
        < COARSE_PRODUCT_ERROR
        and product_from_coarse_factors
        == COARSE_SIGMA_Y_MULTIPLIER
        and COARSE_SIGMA_Y_MULTIPLIER < TARGET_SIGMA_Y_MULTIPLIER
    )


@dataclass(frozen=True)
class SigmaYMultiplierEvaluation:
    """High-precision diagnostic at a supplied logarithmic endpoint."""

    log_x: mp.mpf
    log_2_x: mp.mpf
    log_a: mp.mpf
    log_z: mp.mpf
    upper_product_error: mp.mpf
    lower_product_error: mp.mpf
    exceptional_prime_factor: mp.mpf
    sigma_y_upper_multiplier: mp.mpf


def evaluate_sigma_y_upper_multiplier(
    log_x: object,
) -> SigmaYMultiplierEvaluation:
    """Evaluate the source-theorem multiplier using only ``log(x)``.

    Rosser--Schoenfeld Theorem 7 gives

        P(z)/P(a)
        < (log(a)/log(z))
          * (1 + 1/(2*log(z)**2))
          / (1 - 1/(2*log(a)**2)).

    If the exceptional prime ``B0`` was removed from the interval product,
    its factor is at most ``1/(1-1/a)``.  The returned multiplier is the
    factor multiplying the nominal value ``80*c*x*log_2(x)``.
    """

    log_x_mpf = _validated_log_x(log_x)
    log_2_x = mp.log(log_x_mpf)
    log_a = 20 * log_2_x
    log_z = log_x_mpf * mp.log(log_2_x) / (4 * log_2_x)
    if log_z <= log_a:
        raise ArithmeticError("the FMT interval must satisfy z > a")

    upper_error = 1 / (2 * log_z**2)
    lower_error = 1 / (2 * log_a**2)
    exceptional_factor = 1 / (1 - mp.exp(-log_a))
    multiplier = (
        (1 + upper_error) / (1 - lower_error) * exceptional_factor
    )
    return SigmaYMultiplierEvaluation(
        log_x=log_x_mpf,
        log_2_x=log_2_x,
        log_a=log_a,
        log_z=log_z,
        upper_product_error=upper_error,
        lower_product_error=lower_error,
        exceptional_prime_factor=exceptional_factor,
        sigma_y_upper_multiplier=multiplier,
    )


@dataclass(frozen=True)
class SigmaYCutoffCertificate:
    gate: str
    cutoff_symbolic: str
    minimum_endpoint_dimension: int
    rosser_lower_endpoint: int
    exact_rational_certificate: bool
    interval_endpoint_semantics_closed: bool
    exceptional_prime_local_correction_closed: bool
    sigma_y_target_multiplier: Fraction
    proved_coarse_multiplier: Fraction
    siv_03_closed: bool
    sono_coefficient_preserved_at_this_gate: bool
    full_distribution_common_exceptional_b_closed: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_07_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def sigma_y_cutoff_certificate() -> SigmaYCutoffCertificate:
    """Build the fail-closed H1c-1b.1a.1 project certificate."""

    return SigmaYCutoffCertificate(
        gate="H1c-1b.1a.1 / SIV-03",
        cutoff_symbolic="x >= 2*exp(36**5)",
        minimum_endpoint_dimension=MINIMUM_ENDPOINT_DIMENSION,
        rosser_lower_endpoint=ROSSER_LOWER_ENDPOINT,
        exact_rational_certificate=exact_sigma_y_cutoff_certificate(),
        interval_endpoint_semantics_closed=True,
        exceptional_prime_local_correction_closed=True,
        sigma_y_target_multiplier=TARGET_SIGMA_Y_MULTIPLIER,
        proved_coarse_multiplier=COARSE_SIGMA_Y_MULTIPLIER,
        siv_03_closed=True,
        sono_coefficient_preserved_at_this_gate=True,
        full_distribution_common_exceptional_b_closed=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_07_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
