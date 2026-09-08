"""Explicit finite scale for the two sharp ``r_0 < x**xi`` calls.

The proof and its source-version caveat are recorded in
``docs/method/theory/27_Sono_FMT_H1b1b2d1b_sharp_xi_logx_scale.md``.
This module evaluates conservative consequences of that proof.  It uses the
actual FGKMT/FMT specialization ``xi = theta/10`` and the Maynard admissible
range ``R <= x**(theta/3)``; hence ``xi*log(x) >= 3*log(R)/10``.

The module closes only the two sharp summatory subapplications after the
predecessor smooth/scalar contracts.  It does not certify Proposition 9.4,
Proposition 6.1, Hypothesis 1, ``SIV-07``, or ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L1096_W0,
    APPLICATION_L1135_W0_FACTOR,
    maynard_uniform_application_log_q_upper,
)
from source.h1b1b2b_corrected_wirsing import (
    strict_summatory_multiplier,
    summatory_multiplier,
)
from source.h1b1b2c_actual_parameter_package import (
    H1B1B2C_MAYNARD_A1_GAP,
    H1B1B2C_UPPER_DISCREPANCY_A2,
)


H1B1B2D1B_MINIMUM_TARGET_K = 36
FMT_XI_OVER_THETA = Fraction(1, 10)
MAYNARD_LOG_R_UPPER_EXPONENT_OVER_THETA = Fraction(1, 3)
FMT_SHARP_SCALE_OVER_LOG_R_LOWER = Fraction(3, 10)
H1B1B2D1B_RELATIVE_ERROR_TARGET = Fraction(1, 2)

SHARP_APPLICATION_IDS = frozenset(
    {
        APPLICATION_L1096_W0,
        APPLICATION_L1135_W0_FACTOR,
    }
)


@dataclass(frozen=True)
class SharpScaleGateCertificate:
    """A coarse closed-form sufficient cutoff for both sharp calls."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    xi_over_theta: Fraction
    log_r_upper_exponent_over_theta: Fraction
    sharp_scale_over_log_r_lower: Fraction
    summatory_multiplier: mp.mpf
    strict_summatory_multiplier: mp.mpf
    lambda_affine_constant: mp.mpf
    lambda_affine_slope: mp.mpf
    e_coefficient: mp.mpf
    log_r_sufficient: mp.mpf
    log_excluded_integer_upper: mp.mpf
    l_plus_one: mp.mpf
    sharp_scale_lower_bound: mp.mpf
    relative_error_upper_bound: mp.mpf
    relative_error_target: Fraction
    endpoint_scale_minimum: mp.mpf
    endpoint_gate_passed: bool
    relative_error_gate_passed: bool
    sharp_application_count: int
    sharp_calls_closed: bool
    h1b_l84_status: str
    h1b_comp_01_closed: bool
    siv_07_closed: bool
    siv_09_closed: bool
    x_cert_ready: bool
    theorem_claimed: bool


def _positive_mpf(value: int | float | str | mp.mpf, name: str) -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and positive")
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _validate_parameters(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
) -> tuple[mp.mpf, mp.mpf]:
    if (
        isinstance(k, bool)
        or not isinstance(k, int)
        or k < H1B1B2D1B_MINIMUM_TARGET_K
    ):
        raise ValueError(
            f"k must be an integer at least {H1B1B2D1B_MINIMUM_TARGET_K}"
        )
    alpha_value = _positive_mpf(alpha, "alpha")
    theta_value = _positive_mpf(theta, "theta")
    if theta_value >= 1:
        raise ValueError("theta must lie in (0,1)")
    return alpha_value, theta_value


def _fraction_mpf(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def fmt_sharp_scale_lower_bound(
    log_r: int | float | str | mp.mpf,
) -> mp.mpf:
    """Return the proved lower bound for ``xi*log(x)``.

    Under ``xi=theta/10`` and ``R<=x**(theta/3)``, taking logarithms gives
    ``xi*log(x) >= 3*log(R)/10``.  No hidden Vinogradov multiplier is used.
    """

    log_r_value = _positive_mpf(log_r, "log_r")
    return _fraction_mpf(FMT_SHARP_SCALE_OVER_LOG_R_LOWER) * log_r_value


def fmt_sharp_relative_error_upper(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
) -> mp.mpf:
    """Evaluate the strict-cutoff relative error at a supplied ``log(R)``.

    This is an upper bound for each of the two source-traced sharp factors,
    not an error bound for the whole moment calculation.
    """

    alpha_value, theta_value = _validate_parameters(
        k=k,
        alpha=alpha,
        theta=theta,
    )
    log_r_value = _positive_mpf(log_r, "log_r")
    lambda_star = maynard_uniform_application_log_q_upper(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_value,
    )
    l_plus_one = 6 + mp.log(lambda_star)
    strict = strict_summatory_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    return strict * l_plus_one / fmt_sharp_scale_lower_bound(log_r_value)


def common_sharp_scale_gate_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
) -> SharpScaleGateCertificate:
    """Construct a finite gate shared by the two actual sharp calls.

    Put ``y=log(R)``, ``Lambda_star=A+B*y`` and

    ``E=(20/3)*(C_Sigma+2)``.

    It is enough to have ``E*(6+log(Lambda_star)) <= y``.  For ``y>=1``,
    ``log(A+B*y) <= log(A+B)+log(y)``.  The two terms are each at most
    ``y/2`` when

    ``y >= 4*E*log(4*E)`` and
    ``y >= 2*E*(6+log(A+B))``.

    The additional ``(10/3)*log(2)`` gate ensures ``x**xi >= 2`` so the
    strict summatory theorem applies.  The result intentionally targets a
    relative error of ``1/2`` rather than optimizing the cutoff.
    """

    alpha_value, theta_value = _validate_parameters(
        k=k,
        alpha=alpha,
        theta=theta,
    )
    k_value = mp.mpf(k)
    affine_constant = (
        2 * k_value**2 * mp.log(2 * k_value**2)
        + k_value * (k_value - 1) * mp.log(2)
    )
    affine_slope = (
        10
        * alpha_value
        * (2 * k_value**2 - k_value + 1)
        / theta_value
        + k_value
    )

    base = summatory_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    strict = strict_summatory_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    e_coefficient = mp.mpf(20) * strict / 3
    if e_coefficient <= 1:
        raise AssertionError("the project-range sharp coefficient must exceed one")

    constant_term = 6 + mp.log(affine_constant + affine_slope)
    endpoint_gate = mp.mpf(10) * mp.log(2) / 3
    log_r_sufficient = max(
        mp.mpf(1),
        endpoint_gate,
        4 * e_coefficient * mp.log(4 * e_coefficient),
        2 * e_coefficient * constant_term,
    )
    lambda_star = maynard_uniform_application_log_q_upper(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_sufficient,
    )
    l_plus_one = 6 + mp.log(lambda_star)
    sharp_scale = fmt_sharp_scale_lower_bound(log_r_sufficient)
    relative_error = strict * l_plus_one / sharp_scale
    target = _fraction_mpf(H1B1B2D1B_RELATIVE_ERROR_TARGET)
    endpoint_passed = sharp_scale >= mp.log(2)
    relative_passed = relative_error <= target
    sharp_closed = endpoint_passed and relative_passed

    return SharpScaleGateCertificate(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        xi_over_theta=FMT_XI_OVER_THETA,
        log_r_upper_exponent_over_theta=(
            MAYNARD_LOG_R_UPPER_EXPONENT_OVER_THETA
        ),
        sharp_scale_over_log_r_lower=FMT_SHARP_SCALE_OVER_LOG_R_LOWER,
        summatory_multiplier=base,
        strict_summatory_multiplier=strict,
        lambda_affine_constant=affine_constant,
        lambda_affine_slope=affine_slope,
        e_coefficient=e_coefficient,
        log_r_sufficient=log_r_sufficient,
        log_excluded_integer_upper=lambda_star,
        l_plus_one=l_plus_one,
        sharp_scale_lower_bound=sharp_scale,
        relative_error_upper_bound=relative_error,
        relative_error_target=H1B1B2D1B_RELATIVE_ERROR_TARGET,
        endpoint_scale_minimum=mp.log(2),
        endpoint_gate_passed=endpoint_passed,
        relative_error_gate_passed=relative_passed,
        sharp_application_count=len(SHARP_APPLICATION_IDS),
        sharp_calls_closed=sharp_closed,
        h1b_l84_status=(
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT"
            if sharp_closed
            else "RATE_MISSING"
        ),
        h1b_comp_01_closed=False,
        siv_07_closed=False,
        siv_09_closed=False,
        x_cert_ready=False,
        theorem_claimed=False,
    )


__all__ = [
    "FMT_SHARP_SCALE_OVER_LOG_R_LOWER",
    "FMT_XI_OVER_THETA",
    "H1B1B2D1B_MINIMUM_TARGET_K",
    "H1B1B2D1B_RELATIVE_ERROR_TARGET",
    "MAYNARD_LOG_R_UPPER_EXPONENT_OVER_THETA",
    "SHARP_APPLICATION_IDS",
    "SharpScaleGateCertificate",
    "common_sharp_scale_gate_certificate",
    "fmt_sharp_relative_error_upper",
    "fmt_sharp_scale_lower_bound",
]
