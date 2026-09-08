"""Fail-closed square-sum bypass for Maynard's source-line-905 ``H``.

Maynard's proof records only an outer-lattice pointwise estimate

    Z_r = A(u_r) + O(epsilon * B(u_r)),

where ``A = integral F dt_m`` and ``B = integral F_2 dt_m``.  It does not
construct a single smooth remainder function in the remaining variables.
For the line-905 square sum, no such function is needed: the exact algebra

    |Z_r**2 - A(u_r)**2| <= 2*epsilon*A*B + epsilon**2*B**2

reduces the problem to finite nonnegative smooth tensor families.  This
module certifies that reduction and evaluates the already-proved r-fold
envelopes *conditional on a supplied scalar epsilon*.  It deliberately does
not assign a value to Maynard's hidden Vinogradov constants, close Lemma 8.4,
or compute ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    maynard_uniform_application_log_q_upper,
)
from source.h1b1b2b_corrected_wirsing import weighted_lemma83_multiplier
from source.h1b1b2c_actual_parameter_package import (
    H1B1B2C_MAYNARD_A1_GAP,
    H1B1B2C_UPPER_DISCREPANCY_A2,
    lower_discrepancy_l,
)
from source.h1b1b2d_rfold_smooth_package import (
    H1B1B2D_MINIMUM_TARGET_K,
    PROFILE_N2,
    PROFILE_NW,
    PROFILE_W2,
    product_relative_error_upper,
    profile_norm_certificate,
)


CATEGORY_A_SQUARED = "A_squared"
CATEGORY_A_TIMES_B = "A_times_B"
CATEGORY_B_SQUARED = "B_squared"

H1B1B2D1A_P_DERIVATIVE_BOUND = 50
H1B1B2D1A_P_SQUARED_DERIVATIVE_BOUND = 100


@dataclass(frozen=True)
class HSquareTensorFamily:
    """One symmetry class in the exact expansion of A^2, AB, or B^2."""

    name: str
    category: str
    multiplicity: int
    integer_coefficient: int
    integral_coefficient: str
    profiles: tuple[str, ...]
    coupled_cutoff: str | None
    coupled_cutoff_derivative_bound: int
    wide_coordinate_first_required: bool


@dataclass(frozen=True)
class ExactSquareBypassCertificate:
    """Exact rational verification of the pointwise square inequality."""

    z: Fraction
    a: Fraction
    b: Fraction
    epsilon: Fraction
    assumed_remainder: Fraction
    assumption_upper_bound: Fraction
    square_error: Fraction
    square_error_upper_bound: Fraction
    margin: Fraction


@dataclass(frozen=True)
class ConditionalHSquareBypassCertificate:
    """Numerical evaluation conditional on an external scalar remainder."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    log_r: mp.mpf
    scalar_epsilon_assumed: mp.mpf
    a_times_b_pointwise_coefficient: mp.mpf
    b_squared_pointwise_coefficient: mp.mpf
    log_lambda_star: mp.mpf
    l_plus_one: mp.mpf
    one_step_multiplier: mp.mpf
    a_squared_rfold_error_upper: mp.mpf
    a_times_b_rfold_error_upper: mp.mpf
    b_squared_rfold_error_upper: mp.mpf
    pointwise_reduction_closed: bool
    functional_h_c1_required: bool
    source_scalar_multiplier_certified: bool
    line_905_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


def _validate_k(k: int, *, target_range: bool = False) -> None:
    minimum = H1B1B2D_MINIMUM_TARGET_K if target_range else 2
    if isinstance(k, bool) or not isinstance(k, int) or k < minimum:
        raise ValueError(f"k must be an integer at least {minimum}")


def _nonnegative_mpf(
    value: int | float | str | mp.mpf,
    name: str,
) -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and nonnegative")
    result = mp.mpf(value)
    if not mp.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _positive_mpf(
    value: int | float | str | mp.mpf,
    name: str,
) -> mp.mpf:
    result = _nonnegative_mpf(value, name)
    if result == 0:
        raise ValueError(f"{name} must be positive")
    return result


def h_square_tensor_families(k: int) -> tuple[HSquareTensorFamily, ...]:
    """Return the complete symmetry-reduced expansion for the 905 sum.

    Put ``d=k-1``, ``I_N=integral N``, ``I_W=integral W`` and

    ``P(S)=I_N^-1 integral psi(S+t)N(t)dt``.

    Then ``A=I_N*P*product(N_i)`` and
    ``B=I_W*product(N_i)+I_N*sum_j W_j*product_{i!=j}N_i``.
    The returned seven rows are exactly the resulting A^2, AB and B^2
    symmetry classes.  Multiplicity and the explicit integer coefficient are
    kept separate so that no diagonal or cross term can be dropped.
    """

    _validate_k(k)
    d = k - 1
    n2 = (PROFILE_N2,) * d
    one_nw = (PROFILE_NW,) + (PROFILE_N2,) * (d - 1)
    one_w2 = (PROFILE_W2,) + (PROFILE_N2,) * (d - 1)
    two_nw = (PROFILE_NW, PROFILE_NW) + (PROFILE_N2,) * (d - 2)
    return (
        HSquareTensorFamily(
            "A2_cutoff",
            CATEGORY_A_SQUARED,
            1,
            1,
            "I_N^2",
            n2,
            "P(sum u)^2",
            H1B1B2D1A_P_SQUARED_DERIVATIVE_BOUND,
            False,
        ),
        HSquareTensorFamily(
            "AB_base",
            CATEGORY_A_TIMES_B,
            1,
            1,
            "I_N*I_W",
            n2,
            "P(sum u)",
            H1B1B2D1A_P_DERIVATIVE_BOUND,
            False,
        ),
        HSquareTensorFamily(
            "AB_one_NW",
            CATEGORY_A_TIMES_B,
            d,
            1,
            "I_N^2",
            one_nw,
            "P(sum u)",
            H1B1B2D1A_P_DERIVATIVE_BOUND,
            False,
        ),
        HSquareTensorFamily(
            "B2_base",
            CATEGORY_B_SQUARED,
            1,
            1,
            "I_W^2",
            n2,
            None,
            0,
            False,
        ),
        HSquareTensorFamily(
            "B2_one_NW",
            CATEGORY_B_SQUARED,
            d,
            2,
            "I_N*I_W",
            one_nw,
            None,
            0,
            False,
        ),
        HSquareTensorFamily(
            "B2_one_W2",
            CATEGORY_B_SQUARED,
            d,
            1,
            "I_N^2",
            one_w2,
            None,
            0,
            True,
        ),
        HSquareTensorFamily(
            "B2_two_NW",
            CATEGORY_B_SQUARED,
            d * (d - 1) // 2,
            2,
            "I_N^2",
            two_nw,
            None,
            0,
            False,
        ),
    )


def h_square_kappa_families(
    k: int,
    category: str,
) -> tuple[tuple[mp.mpf, ...], ...]:
    """Return every distinct support-scaled C1 family in one category."""

    rows = tuple(
        row
        for row in h_square_tensor_families(k)
        if row.category == category and row.multiplicity > 0
    )
    if not rows:
        raise ValueError(f"unknown square-bypass category: {category}")
    result = []
    for row in rows:
        kappas = []
        for profile in row.profiles:
            norm = profile_norm_certificate(k, profile)
            cutoff_factor = (
                1
                + row.coupled_cutoff_derivative_bound
                * norm.spec.support_scale
            )
            kappas.append(cutoff_factor * norm.scaled_omega_upper_bound)
        result.append(tuple(kappas))
    return tuple(result)


def exact_square_bypass_certificate(
    *,
    z: int | str | Fraction,
    a: int | str | Fraction,
    b: int | str | Fraction,
    epsilon: int | str | Fraction,
) -> ExactSquareBypassCertificate:
    """Verify ``|z-a|<=epsilon*b`` implies the exact square envelope."""

    if any(isinstance(value, bool) for value in (z, a, b, epsilon)):
        raise ValueError("boolean values are not valid rational inputs")
    z_value = Fraction(z)
    a_value = Fraction(a)
    b_value = Fraction(b)
    epsilon_value = Fraction(epsilon)
    if a_value < 0 or b_value < 0 or epsilon_value < 0:
        raise ValueError("a, b and epsilon must be nonnegative")
    remainder = abs(z_value - a_value)
    assumption_upper = epsilon_value * b_value
    if remainder > assumption_upper:
        raise ValueError("the supplied values do not satisfy |z-a|<=epsilon*b")
    square_error = abs(z_value * z_value - a_value * a_value)
    upper = (
        2 * epsilon_value * a_value * b_value
        + epsilon_value * epsilon_value * b_value * b_value
    )
    if square_error > upper:
        raise AssertionError("the exact square-bypass inequality failed")
    return ExactSquareBypassCertificate(
        z=z_value,
        a=a_value,
        b=b_value,
        epsilon=epsilon_value,
        assumed_remainder=remainder,
        assumption_upper_bound=assumption_upper,
        square_error=square_error,
        square_error_upper_bound=upper,
        margin=upper - square_error,
    )


def conditional_h_square_bypass_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
    scalar_epsilon: int | float | str | mp.mpf,
) -> ConditionalHSquareBypassCertificate:
    """Evaluate all smooth envelopes conditional on a scalar epsilon.

    ``scalar_epsilon`` is an assumption, not a recovered Maynard constant.
    Consequently this function always returns
    ``source_scalar_multiplier_certified=False`` and cannot promote the
    parent theorem nodes.
    """

    _validate_k(k, target_range=True)
    alpha_value = _positive_mpf(alpha, "alpha")
    theta_value = _positive_mpf(theta, "theta")
    if theta_value >= 1:
        raise ValueError("theta must lie in (0,1)")
    log_r_value = _positive_mpf(log_r, "log_r")
    if log_r_value < mp.sqrt(k) * mp.log(2):
        raise ValueError("log_r is too small for the narrow-profile z>=2 gate")
    epsilon_value = _nonnegative_mpf(scalar_epsilon, "scalar_epsilon")
    lambda_star = maynard_uniform_application_log_q_upper(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_value,
    )
    l_plus_one = lower_discrepancy_l(lambda_star) + 1
    multiplier = weighted_lemma83_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    coefficient = multiplier * l_plus_one / log_r_value

    def category_error(category: str) -> mp.mpf:
        return product_relative_error_upper(
            multiplier_over_log_r=coefficient,
            kappa_families=h_square_kappa_families(k, category),
        )

    return ConditionalHSquareBypassCertificate(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_value,
        scalar_epsilon_assumed=epsilon_value,
        a_times_b_pointwise_coefficient=2 * epsilon_value,
        b_squared_pointwise_coefficient=epsilon_value * epsilon_value,
        log_lambda_star=mp.log(lambda_star),
        l_plus_one=l_plus_one,
        one_step_multiplier=multiplier,
        a_squared_rfold_error_upper=category_error(CATEGORY_A_SQUARED),
        a_times_b_rfold_error_upper=category_error(CATEGORY_A_TIMES_B),
        b_squared_rfold_error_upper=category_error(CATEGORY_B_SQUARED),
        pointwise_reduction_closed=True,
        functional_h_c1_required=False,
        source_scalar_multiplier_certified=False,
        line_905_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


__all__ = [
    "CATEGORY_A_SQUARED",
    "CATEGORY_A_TIMES_B",
    "CATEGORY_B_SQUARED",
    "ConditionalHSquareBypassCertificate",
    "ExactSquareBypassCertificate",
    "H1B1B2D1A_P_DERIVATIVE_BOUND",
    "H1B1B2D1A_P_SQUARED_DERIVATIVE_BOUND",
    "HSquareTensorFamily",
    "conditional_h_square_bypass_certificate",
    "exact_square_bypass_certificate",
    "h_square_kappa_families",
    "h_square_tensor_families",
]
