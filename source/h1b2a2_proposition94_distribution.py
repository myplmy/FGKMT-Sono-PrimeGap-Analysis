"""Finite distribution-error reduction for the actual FGKMT P9.4 call.

The proof and its scope are recorded in
``docs/method/theory/30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md``.
The important specialization is ``A = Z``.  A consecutive integer interval
has residue-class discrepancy at most one for every modulus, so the
equation-(9.52) error can be bounded without assigning a numerical value to
the general implied constants in Maynard's Hypothesis 1.

This module evaluates a deliberately coarse sufficient condition in log
space.  It does not close Proposition 9.4 as a whole, Hypothesis 1(2),
Proposition 6.1, ``SIV-07``, or ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1b1b2d_rfold_smooth_package import (
    common_smooth_gate_certificate,
)
from source.h1b1b2d1b_sharp_scale import (
    common_sharp_scale_gate_certificate,
)


H1B2A2_MINIMUM_K = 36
H1B2A2_TOTIENT_EXCEPTION_SAFE_COEFFICIENT = mp.mpf("2.50637")
H1B2A2_SINGULAR_SERIES_LOG_LOSS_PER_K = Fraction(9, 2)
H1B2A2_ASSIGNMENTS_PER_COORDINATE = 3
FMT_XI_OVER_THETA = Fraction(1, 10)
MAYNARD_LOG_R_LOWER_OVER_THETA = Fraction(1, 10)
MAYNARD_LOG_R_UPPER_OVER_THETA = Fraction(1, 3)


@dataclass(frozen=True)
class IntervalDiscrepancyCertificate:
    """Exact count and discrepancy for one integer half-open interval."""

    start: int
    stop: int
    modulus: int
    residue: int
    interval_size: int
    residue_count: int
    discrepancy: Fraction
    at_most_one: bool


@dataclass(frozen=True)
class Proposition94DistributionCertificate:
    """Evaluation of the proved finite P9.4 distribution-error gate."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    xi: mp.mpf
    log_x: mp.mpf
    decay_exponent: mp.mpf
    assignment_divisor_dimension: int
    log_v_upper: mp.mpf
    log_w0_upper: mp.mpf
    w0_over_phi_upper: mp.mpf
    log_q_upper: mp.mpf
    smooth_log_r_required: mp.mpf
    sharp_log_r_required: mp.mpf
    modulus_log_x_required: mp.mpf
    analytic_absorption_log_x_required: mp.mpf
    log_x_sufficient: mp.mpf
    log_relative_error_upper: mp.mpf
    integer_interval_discrepancy_bound: int
    modulus_gate_passed: bool
    smooth_gate_passed: bool
    sharp_gate_passed: bool
    analytic_gate_passed: bool
    direct_relative_error_gate_passed: bool
    distribution_error_closed_at_supplied_gate: bool
    hypothesis1_clause1_multiplier_required: bool
    hypothesis1_clause3_multiplier_required: bool
    proposition_94_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool
    theorem_claimed: bool


def _validate_parameters(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
) -> tuple[mp.mpf, mp.mpf]:
    if isinstance(k, bool) or not isinstance(k, int) or k < H1B2A2_MINIMUM_K:
        raise ValueError(f"k must be an integer at least {H1B2A2_MINIMUM_K}")
    if isinstance(alpha, bool) or isinstance(theta, bool):
        raise ValueError("alpha and theta must be finite positive numbers")
    alpha_value = mp.mpf(alpha)
    theta_value = mp.mpf(theta)
    if not mp.isfinite(alpha_value) or alpha_value <= 0:
        raise ValueError("alpha must be finite and positive")
    if not mp.isfinite(theta_value) or not 0 < theta_value < mp.mpf(15) / 16:
        raise ValueError("theta must lie in (0,15/16) for this coarse decay proof")
    return alpha_value, theta_value


def consecutive_interval_discrepancy(
    start: int,
    stop: int,
    modulus: int,
    residue: int,
) -> IntervalDiscrepancyCertificate:
    """Return the exact discrepancy on ``[start, stop)``.

    Every residue occurs either ``floor(N/q)`` or ``ceil(N/q)`` times in a
    consecutive interval of ``N`` integers.  The returned rational number is
    therefore strictly below one unless the discrepancy is zero.
    """

    for value, name in ((start, "start"), (stop, "stop"), (modulus, "modulus")):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
    if isinstance(residue, bool) or not isinstance(residue, int):
        raise ValueError("residue must be an integer")
    if stop <= start:
        raise ValueError("stop must be greater than start")
    if modulus <= 0:
        raise ValueError("modulus must be positive")

    normalized_residue = residue % modulus
    first = start + ((normalized_residue - start) % modulus)
    count = 0 if first >= stop else 1 + (stop - 1 - first) // modulus
    size = stop - start
    discrepancy = abs(Fraction(count, 1) - Fraction(size, modulus))
    return IntervalDiscrepancyCertificate(
        start=start,
        stop=stop,
        modulus=modulus,
        residue=normalized_residue,
        interval_size=size,
        residue_count=count,
        discrepancy=discrepancy,
        at_most_one=discrepancy <= 1,
    )


def squarefree_assignment_multiplicity_upper(
    k: int,
    free_prime_count: int,
) -> int:
    """Return ``[3(k+1)]**omega`` for the P9.4 tuple assignment.

    A prime outside the fixed modulus can be assigned to one of ``k+1``
    coordinates and, in that coordinate, to ``d`` only, ``e`` only, or both.
    Support and coprimality restrictions can only reduce this count.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if (
        isinstance(free_prime_count, bool)
        or not isinstance(free_prime_count, int)
        or free_prime_count < 0
    ):
        raise ValueError("free_prime_count must be a nonnegative integer")
    return (H1B2A2_ASSIGNMENTS_PER_COORDINATE * (k + 1)) ** free_prime_count


def divisor_summatory_log_upper(
    dimension: int,
    log_endpoint: int | float | str | mp.mpf,
) -> mp.mpf:
    """Log of ``Q(1+log Q)**dimension`` for ``sum_{q<Q} tau_d(q)``.

    The inequality follows by counting ordered positive ``dimension``-tuples
    with product below ``Q`` and using the harmonic bound
    ``sum_{n<Q} 1/n <= 1+log Q``.
    """

    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    if isinstance(log_endpoint, bool):
        raise ValueError("log_endpoint must be finite and positive")
    value = mp.mpf(log_endpoint)
    if not mp.isfinite(value) or value <= 0:
        raise ValueError("log_endpoint must be finite and positive")
    return value + dimension * mp.log(1 + value)


def _gate_components(
    *,
    k: int,
    alpha: mp.mpf,
    theta: mp.mpf,
) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    """Return prior, modulus, analytic, and full sufficient log-x gates."""

    xi = theta / 10
    beta = 1 - 16 * theta / 15
    smooth = common_smooth_gate_certificate(k=k, alpha=alpha, theta=theta)
    sharp = common_sharp_scale_gate_certificate(k=k, alpha=alpha, theta=theta)
    if not smooth.gate_verified or not sharp.sharp_calls_closed:
        raise AssertionError("an upstream finite gate failed its own verification")

    # A+B*y bounds log(W0) for D=1, V=prod_{p<=2k^2}p, and coefficients
    # |a_i|,|b_i|<=x^alpha.
    a_w0 = 4 * mp.mpf(k) ** 2 + k * mp.log(2)
    b_w0 = alpha * (2 * k + 1)
    assignment_dimension = 3 * (k + 1)
    q_affine = 1 + 4 * mp.mpf(k) ** 2 + 13 * theta / 15

    constant = (
        mp.log(8)
        + 8 * mp.mpf(k) ** 2
        + 2
        + mp.mpf(9) * k / 2
        + k * (mp.log(2) + mp.log(mp.log(k)) - mp.log(k))
        - mp.log(xi)
        + 2 * mp.log(6)
        + 2 * mp.log(1 + mp.log(a_w0 + b_w0))
        + assignment_dimension * mp.log(q_affine)
    )
    log_power = 4 * (k + 1)
    analytic_gate = max(
        mp.mpf(1),
        2 * max(mp.mpf(0), constant) / beta,
        (4 * log_power / beta) * mp.log(4 * log_power / beta),
    )
    modulus_gate = 30 * mp.mpf(k) ** 2 / theta
    full_gate = max(
        mp.log(2),
        modulus_gate,
        10 * smooth.log_r_sufficient / theta,
        10 * sharp.log_r_sufficient / theta,
        analytic_gate,
    )
    return (
        smooth.log_r_sufficient,
        sharp.log_r_sufficient,
        modulus_gate,
        analytic_gate,
        full_gate,
    )


def proposition94_distribution_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_x: int | float | str | mp.mpf | None = None,
) -> Proposition94DistributionCertificate:
    """Evaluate the actual-application finite distribution-error reduction.

    If ``log_x`` is omitted, the closed-form sufficient value is evaluated.
    The reported floating values are high-precision diagnostics for symbolic
    inequalities proved in the companion document, not directed-rounding
    interval certificates.
    """

    alpha_value, theta_value = _validate_parameters(
        k=k,
        alpha=alpha,
        theta=theta,
    )
    (
        smooth_log_r,
        sharp_log_r,
        modulus_gate,
        analytic_gate,
        full_gate,
    ) = _gate_components(k=k, alpha=alpha_value, theta=theta_value)
    if log_x is None:
        y = full_gate
    else:
        if isinstance(log_x, bool):
            raise ValueError("log_x must be finite and positive")
        y = mp.mpf(log_x)
        if not mp.isfinite(y) or y <= 0:
            raise ValueError("log_x must be finite and positive")

    xi = theta_value / 10
    beta = 1 - 16 * theta_value / 15
    log_v = 4 * mp.mpf(k) ** 2
    log_w0 = log_v + k * mp.log(2) + alpha_value * (2 * k + 1) * y
    w0_over_phi = (
        3 * mp.log(log_w0) + H1B2A2_TOTIENT_EXCEPTION_SAFE_COEFFICIENT
    )
    log_q = log_v + 13 * theta_value * y / 15
    assignment_dimension = 3 * (k + 1)
    log_r_upper = theta_value * y / 3

    # This is log(rho_94), where distribution error <= rho_94 times the
    # canonical right-hand-side scale in Maynard Proposition 9.4.
    log_relative = (
        mp.log(8)
        + 2 * log_v
        + 2 * mp.log(w0_over_phi)
        + 2  # M_620^2 <= e^2 at the smooth gate
        - beta * y
        - mp.log(xi)
        - 2 * mp.log(y)
        + mp.mpf(9) * k / 2
        + k * mp.log(2)
        + k * mp.log(mp.log(k))
        - k * mp.log(k)
        + (k + 1) * mp.log(log_r_upper)
        + assignment_dimension * mp.log(1 + log_q)
    )

    modulus_passed = y >= modulus_gate
    smooth_passed = theta_value * y / 10 >= smooth_log_r
    sharp_passed = theta_value * y / 10 >= sharp_log_r
    analytic_passed = y >= analytic_gate
    direct_passed = log_relative <= 0
    distribution_closed = (
        modulus_passed
        and smooth_passed
        and sharp_passed
        and analytic_passed
        and direct_passed
    )
    return Proposition94DistributionCertificate(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        xi=xi,
        log_x=y,
        decay_exponent=beta,
        assignment_divisor_dimension=assignment_dimension,
        log_v_upper=log_v,
        log_w0_upper=log_w0,
        w0_over_phi_upper=w0_over_phi,
        log_q_upper=log_q,
        smooth_log_r_required=smooth_log_r,
        sharp_log_r_required=sharp_log_r,
        modulus_log_x_required=modulus_gate,
        analytic_absorption_log_x_required=analytic_gate,
        log_x_sufficient=full_gate,
        log_relative_error_upper=log_relative,
        integer_interval_discrepancy_bound=1,
        modulus_gate_passed=bool(modulus_passed),
        smooth_gate_passed=bool(smooth_passed),
        sharp_gate_passed=bool(sharp_passed),
        analytic_gate_passed=bool(analytic_passed),
        direct_relative_error_gate_passed=bool(direct_passed),
        distribution_error_closed_at_supplied_gate=bool(distribution_closed),
        hypothesis1_clause1_multiplier_required=False,
        hypothesis1_clause3_multiplier_required=False,
        proposition_94_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
        theorem_claimed=False,
    )


__all__ = [
    "FMT_XI_OVER_THETA",
    "H1B2A2_ASSIGNMENTS_PER_COORDINATE",
    "H1B2A2_MINIMUM_K",
    "H1B2A2_SINGULAR_SERIES_LOG_LOSS_PER_K",
    "H1B2A2_TOTIENT_EXCEPTION_SAFE_COEFFICIENT",
    "IntervalDiscrepancyCertificate",
    "MAYNARD_LOG_R_LOWER_OVER_THETA",
    "MAYNARD_LOG_R_UPPER_OVER_THETA",
    "Proposition94DistributionCertificate",
    "consecutive_interval_discrepancy",
    "divisor_summatory_log_upper",
    "proposition94_distribution_certificate",
    "squarefree_assignment_multiplicity_upper",
]
