"""End-to-end finite composition for the actual FGKMT/FMT P9.4 call.

The proof and scope are recorded in
``docs/method/theory/31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md``.
This module composes previously proved project certificates for the single
application

    A = Z, D = 1, alpha = 2, theta = 1/3,
    xi = theta/10, R = (x/4)**(theta/3).

It does not prove Maynard Proposition 9.4 for a general set ``A``, close
Maynard Proposition 6.1, or compute the Sono/FMT threshold ``X_cert``.
All large cutoffs are represented by ``log(x)`` rather than by materialising
the astronomically large integer ``x``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L1135_CANONICAL_FACTOR,
)
from source.h1b1b2d_rfold_smooth_package import (
    common_smooth_gate_certificate,
    rfold_error_certificate,
)
from source.h1b1b2d1b_sharp_scale import fmt_sharp_relative_error_upper
from source.h1b2a_residual_moment_package import (
    integral_size_certificate,
    proposition94_local_certificate,
)
from source.h1b2a1_proposition94_euler import euler_tail_certificate
from source.h1b2a2_proposition94_distribution import (
    proposition94_distribution_certificate,
)


H1B2A3_MINIMUM_K = 36
FMT_ALPHA = 2
FMT_THETA = Fraction(1, 3)
FMT_XI_OVER_THETA = Fraction(1, 10)
FMT_LOG_R_OVER_THETA = Fraction(1, 3)
SHARP_RELATIVE_ERROR_TARGET = Fraction(1, 2)


@dataclass(frozen=True)
class Proposition94CompositionCertificate:
    """Finite certificate for the one actual FGKMT/FMT P9.4 application."""

    k: int
    alpha: int
    theta: Fraction
    xi: Fraction
    log_x: mp.mpf
    actual_log_r: mp.mpf
    distribution_log_x_required: mp.mpf
    strong_smooth_log_r_required: mp.mpf
    strong_smooth_delta_target: mp.mpf
    dimension_log_x_required: int
    actual_support_log_x_required: mp.mpf
    log_x_sufficient: mp.mpf
    sharp_relative_error_upper: mp.mpf
    smooth_product_error_upper: mp.mpf
    smooth_delta_sum_upper: mp.mpf
    f1_to_f_multiplier_upper: int
    canonical_relative_error_upper: mp.mpf
    full_euler_normalization_multiplier_upper: mp.mpf
    log_r_over_log_x: mp.mpf
    main_term_multiplier_upper: mp.mpf | None
    distribution_relative_error_upper: mp.mpf
    total_multiplier_upper: mp.mpf | None
    coarse_total_multiplier_upper: mp.mpf | None
    uniform_integer_multiplier_upper: int
    maynard_dimension_gate_passed: bool
    actual_r_lower_gate_passed: bool
    actual_r_upper_gate_passed: bool
    selberg_denominator_positive: bool
    smooth_gate_passed: bool
    sharp_gate_passed: bool
    distribution_child_closed: bool
    local_algebra_closed: bool
    final_residue_factor_upper: int
    composition_bound_verified: bool
    uniform_integer_multiplier_verified: bool
    project_actual_application_lemma_proved: bool
    actual_application_proposition_94_closed: bool
    source_general_proposition_94_closed: bool
    proposition_61_closed: bool
    siv_07_closed: bool
    siv_09_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def _validate_k(k: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < H1B2A3_MINIMUM_K:
        raise ValueError(f"k must be an integer at least {H1B2A3_MINIMUM_K}")


def _fraction_mpf(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def _positive_mpf(value: int | float | str | mp.mpf, name: str) -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and positive")
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def fmt_actual_log_r(log_x: int | float | str | mp.mpf) -> mp.mpf:
    """Return ``log R`` for ``R=(x/4)**(theta/3)``, ``theta=1/3``."""

    y = _positive_mpf(log_x, "log_x")
    if y <= mp.log(4):
        raise ValueError("log_x must exceed log(4), so the actual R is greater than 1")
    theta = _fraction_mpf(FMT_THETA)
    return theta * (y - mp.log(4)) / 3


def proposition94_log_x_sufficient(k: int) -> mp.mpf:
    """Return one common sufficient ``log(x)`` cutoff for the actual call.

    Besides the H1b-2a.2 distribution gate, this includes the printed
    ``k <= (log x)**(1/5)`` condition and the elementary condition ensuring
    ``x**(theta/10) <= R=(x/4)**(theta/3)``.
    """

    _validate_k(k)
    distribution = proposition94_distribution_certificate(
        k=k,
        alpha=FMT_ALPHA,
        theta=FMT_THETA,
    )
    theta = _fraction_mpf(FMT_THETA)
    strong_smooth = proposition94_strong_smooth_log_r_sufficient(k)
    support_gate = mp.mpf(10) * mp.log(4) / 7
    return max(
        distribution.log_x_sufficient,
        10 * strong_smooth / theta,
        mp.mpf(k**5),
        support_gate,
    )


def proposition94_strong_smooth_log_r_sufficient(k: int) -> mp.mpf:
    """Force the canonical smooth error below ``2**(-k)`` relatively.

    The common H1b-1b-2d gate only asks that the sum of one-coordinate
    errors be at most one.  P9.4 compares the resulting product-profile
    error with ``I_k(F)`` through the coarse factor ``2**k``.  We therefore
    strengthen the gate to ``delta_sum <= 2**(-k-1)``.  The already proved
    linearisation ``product_error <= 2*delta_sum`` then gives
    ``2**k*product_error <= 1`` without a k-dependent loss.
    """

    _validate_k(k)
    common = common_smooth_gate_certificate(
        k=k,
        alpha=FMT_ALPHA,
        theta=FMT_THETA,
    )
    target = mp.power(2, -(k + 1))
    scaled_e = common.e_coefficient / target
    constant_term = 6 + mp.log(
        common.lambda_affine_constant + common.lambda_affine_slope
    )
    return max(
        mp.mpf(1),
        mp.sqrt(k) * mp.log(2),
        4 * scaled_e * mp.log(4 * scaled_e),
        2 * scaled_e * constant_term,
    )


def uniform_thirteen_rational_certificate() -> bool:
    """Verify an exact rational proof that the coarse multiplier is below 13.

    The elementary exponential-series estimate

    ``e < 1+1+1/2+1/6+(1/24)*sum(1/4**j) = 49/18 < 11/4``

    and the exact integer inequality ``(11/4)**13 < 9**6`` imply
    ``exp(13/6) < 9``.  Hence ``(4/3)*exp(13/6)+1 < 13``.  No floating
    evaluation or directed-rounding claim is needed for this last step.
    """

    exponential_series_upper = Fraction(49, 18)
    simple_e_upper = Fraction(11, 4)
    return bool(
        exponential_series_upper < simple_e_upper
        and simple_e_upper**13 < Fraction(9) ** 6
    )


def proposition94_actual_composition_certificate(
    *,
    k: int,
    log_x: int | float | str | mp.mpf | None = None,
) -> Proposition94CompositionCertificate:
    """Compose the finite upper bound for the actual FGKMT/FMT P9.4 call.

    Relative to the P9.4 standard scale ``T_94``, the main expression is at
    most

    ``((1+d)/(1-d)**2) * E * (1 + 2**k*eps) * log(R)/log(x)``,

    where ``d`` is the common sharp relative error, ``eps`` is the smooth
    product-envelope error, and ``E`` is the exact Euler normalization
    multiplier.  The distribution child adds ``rho_94``.  At the common
    gate, ``d<=1/2``, ``eps<=e-1``, ``rho_94<=1`` and ``log(R)/log(x)<=1``;
    hence the independently checkable coarse multiplier is

    ``12*exp(2+6/k)*(theta/3)+1 < 13``.

    The last uniform bound uses a strengthened smooth gate that makes
    ``2**k*eps<=1``.  The weaker shared smooth gate alone would leave an
    exponentially k-dependent multiplier and is therefore not used as the
    parent-closing cutoff.
    """

    _validate_k(k)
    required = proposition94_log_x_sufficient(k)
    y = required if log_x is None else _positive_mpf(log_x, "log_x")
    log_r = fmt_actual_log_r(y)

    theta = _fraction_mpf(FMT_THETA)
    xi = theta * _fraction_mpf(FMT_XI_OVER_THETA)
    support_required = mp.mpf(10) * mp.log(4) / 7
    strong_smooth_required = proposition94_strong_smooth_log_r_sufficient(k)
    strong_smooth_target = mp.power(2, -(k + 1))
    dimension_required = k**5

    distribution = proposition94_distribution_certificate(
        k=k,
        alpha=FMT_ALPHA,
        theta=FMT_THETA,
        log_x=y,
    )
    smooth = rfold_error_certificate(
        application_id=APPLICATION_L1135_CANONICAL_FACTOR,
        k=k,
        alpha=FMT_ALPHA,
        theta=FMT_THETA,
        log_r=log_r,
    )
    sharp_delta = fmt_sharp_relative_error_upper(
        k=k,
        alpha=FMT_ALPHA,
        theta=FMT_THETA,
        log_r=log_r,
    )
    integral = integral_size_certificate(k)
    local = proposition94_local_certificate(k)
    euler = euler_tail_certificate(k)

    f1_multiplier = 2**k
    canonical_relative = (
        mp.mpf(f1_multiplier) * smooth.product_error_upper_bound
    )
    scale_ratio = log_r / y
    rho = mp.exp(distribution.log_relative_error_upper)

    dimension_gate = y >= dimension_required
    lower_r_gate = y >= support_required and log_r >= theta * y / 10
    upper_r_gate = log_r <= theta * y / 3
    sharp_gate = sharp_delta <= _fraction_mpf(SHARP_RELATIVE_ERROR_TARGET)
    smooth_gate = smooth.linearization_gate_passed
    strong_smooth_gate = (
        log_r >= strong_smooth_required
        and smooth.delta_sum_upper_bound <= strong_smooth_target
        and canonical_relative <= 1
    )
    selberg_positive = sharp_delta < 1
    local_closed = (
        local.symmetry_multiplier == 1
        and local.denominator_two_over_p_gate_passed
        and local.final_euler_products_closed
        and integral.lower_bound_verified
        and integral.pointwise_comparisons_verified
    )

    main_multiplier: mp.mpf | None = None
    total_multiplier: mp.mpf | None = None
    coarse_multiplier: mp.mpf | None = None
    composition_verified = False
    if selberg_positive:
        main_multiplier = (
            (1 + sharp_delta)
            / (1 - sharp_delta) ** 2
            * euler.full_line_966_multiplier_upper
            * (1 + canonical_relative)
            * scale_ratio
        )
        total_multiplier = main_multiplier + rho

    gate_bundle = (
        y >= required
        and dimension_gate
        and lower_r_gate
        and upper_r_gate
        and sharp_gate
        and smooth_gate
        and strong_smooth_gate
        and distribution.distribution_error_closed_at_supplied_gate
        and local_closed
    )
    if gate_bundle and total_multiplier is not None:
        coarse_multiplier = (
            12
            * euler.full_line_966_multiplier_upper
            * theta
            / 3
            + 1
        )
        composition_verified = total_multiplier <= coarse_multiplier

    uniform_verified = bool(
        composition_verified
        and coarse_multiplier is not None
        and uniform_thirteen_rational_certificate()
    )
    actual_closed = gate_bundle and uniform_verified
    return Proposition94CompositionCertificate(
        k=k,
        alpha=FMT_ALPHA,
        theta=FMT_THETA,
        xi=Fraction(1, 30),
        log_x=y,
        actual_log_r=log_r,
        distribution_log_x_required=distribution.log_x_sufficient,
        strong_smooth_log_r_required=strong_smooth_required,
        strong_smooth_delta_target=strong_smooth_target,
        dimension_log_x_required=dimension_required,
        actual_support_log_x_required=support_required,
        log_x_sufficient=required,
        sharp_relative_error_upper=sharp_delta,
        smooth_product_error_upper=smooth.product_error_upper_bound,
        smooth_delta_sum_upper=smooth.delta_sum_upper_bound,
        f1_to_f_multiplier_upper=f1_multiplier,
        canonical_relative_error_upper=canonical_relative,
        full_euler_normalization_multiplier_upper=(
            euler.full_line_966_multiplier_upper
        ),
        log_r_over_log_x=scale_ratio,
        main_term_multiplier_upper=main_multiplier,
        distribution_relative_error_upper=rho,
        total_multiplier_upper=total_multiplier,
        coarse_total_multiplier_upper=coarse_multiplier,
        uniform_integer_multiplier_upper=13,
        maynard_dimension_gate_passed=bool(dimension_gate),
        actual_r_lower_gate_passed=bool(lower_r_gate),
        actual_r_upper_gate_passed=bool(upper_r_gate),
        selberg_denominator_positive=bool(selberg_positive),
        smooth_gate_passed=bool(smooth_gate and strong_smooth_gate),
        sharp_gate_passed=bool(sharp_gate),
        distribution_child_closed=bool(
            distribution.distribution_error_closed_at_supplied_gate
        ),
        local_algebra_closed=bool(local_closed),
        final_residue_factor_upper=1,
        composition_bound_verified=bool(composition_verified),
        uniform_integer_multiplier_verified=uniform_verified,
        project_actual_application_lemma_proved=bool(actual_closed),
        actual_application_proposition_94_closed=bool(actual_closed),
        source_general_proposition_94_closed=False,
        proposition_61_closed=False,
        siv_07_closed=False,
        siv_09_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )


__all__ = [
    "FMT_ALPHA",
    "FMT_LOG_R_OVER_THETA",
    "FMT_THETA",
    "FMT_XI_OVER_THETA",
    "H1B2A3_MINIMUM_K",
    "Proposition94CompositionCertificate",
    "SHARP_RELATIVE_ERROR_TARGET",
    "fmt_actual_log_r",
    "proposition94_actual_composition_certificate",
    "proposition94_log_x_sufficient",
    "proposition94_strong_smooth_log_r_sufficient",
    "uniform_thirteen_rational_certificate",
]
