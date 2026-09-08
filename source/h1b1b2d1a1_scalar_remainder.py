"""Explicit scalar-remainder package for Maynard equations (9.42)--(9.48).

The analytic proof and its deliberately narrow scope are recorded in
``docs/method/theory/26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md``.  This
module checks the finite algebra and evaluates a conservative sufficient
cutoff.  It does not close the sharp-cutoff applications of Lemma 8.4,
certify Proposition 6.1, or compute ``X_cert``.

The published paper is authoritative here: equation (9.43) uses
``Delta_m = product_{i != m} |a_m*b_i-a_i*b_m|``.  An older author TeX file
contains ``i=1,...,k`` and would make the product zero; that stale source form
must not be used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd, isqrt
from typing import Sequence

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    maynard_uniform_application_log_q_upper,
)
from source.h1b1b2b_corrected_wirsing import weighted_lemma83_multiplier
from source.h1b1b2c_actual_parameter_package import (
    H1B1B2C_MAYNARD_A1_GAP,
    H1B1B2C_UPPER_DISCREPANCY_A2,
)
from source.h1b1b2d_rfold_smooth_package import (
    common_smooth_gate_certificate,
    f2_one_variable_kappa,
)
from source.h1b1b2d1a_h_remainder_bypass import (
    CATEGORY_A_SQUARED,
    CATEGORY_A_TIMES_B,
    CATEGORY_B_SQUARED,
    ConditionalHSquareBypassCertificate,
    conditional_h_square_bypass_certificate,
    h_square_kappa_families,
)
from source.h1b1b_multiplier_recovery import H1B1B_LEMMA82_MULTIPLIER


H1B1B2D1A1_MINIMUM_K = 36
H1B1B2D1A1_S_EULER_PRODUCT_BOUND = 729
H1B1B2D1A1_T_DIVISOR_LOGLOG_SQUARED_BOUND = 19
H1B1B2D1A1_DETERMINANT_LOGLOG_MULTIPLIER = 2
H1B1B2D1A1_PREFACTOR_RESIDUAL_BOUND = Fraction(36, 35)
H1B1B2D1A1_EM_SUM_UPPER_FACTOR = 2
H1B1B2D1A1_DIRECT_BRANCH_FACTOR = 4

# The exact product of the elementary factors in the (9.44) / YmError branch
# after replacing L_D by 2*log(log R).  We round this single rational upward
# once, rather than silently rounding each source factor.
H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT = Fraction(
    H1B1B_LEMMA82_MULTIPLIER
    * H1B1B2D1A1_S_EULER_PRODUCT_BOUND
    * H1B1B2D1A1_T_DIVISOR_LOGLOG_SQUARED_BOUND
    * H1B1B2D1A1_DETERMINANT_LOGLOG_MULTIPLIER**2
    * H1B1B2D1A1_EM_SUM_UPPER_FACTOR
    * H1B1B2D1A1_PREFACTOR_RESIDUAL_BOUND.numerator,
    H1B1B2D1A1_PREFACTOR_RESIDUAL_BOUND.denominator,
)
H1B1B2D1A1_YM_ERROR_COEFFICIENT = (
    H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT.numerator
    + H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT.denominator
    - 1
) // H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT.denominator


@dataclass(frozen=True)
class TDivisorLogLinearForm:
    """Exact coefficients of the divisor sum before evaluating logarithms."""

    constant: Fraction
    log_coefficients: tuple[tuple[int, Fraction], ...]


@dataclass(frozen=True)
class DirectProfileEnvelopeCertificate:
    """Diagnostic values for ``G_max <= 2*T_k*integral(F_2)``."""

    k: int
    t_k: mp.mpf
    u_k: mp.mpf
    i_n_lower_bound: mp.mpf
    b_over_outer_product_lower_bound: mp.mpf
    scaled_gmax_over_outer_product_upper_bound: mp.mpf
    half_integral_gate_passed: bool
    derivative_gate_passed: bool


@dataclass(frozen=True)
class ScalarRemainderConstantCertificate:
    """The two explicit contributions to the common pointwise multiplier."""

    weighted_lemma83_multiplier: mp.mpf
    direct_branch_multiplier: mp.mpf
    ym_error_exact_multiplier: Fraction
    ym_error_integer_multiplier: int
    common_c_y: mp.mpf
    common_c_y_formula: str


@dataclass(frozen=True)
class ScalarRemainderGateCertificate:
    """A sufficient finite ``log(R)`` gate for the scalar reconstruction."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    lambda_affine_constant: mp.mpf
    lambda_affine_slope: mp.mpf
    determinant_growth_coefficient: mp.mpf
    determinant_loglog_requirement: mp.mpf
    discrepancy_loglog_requirement: mp.mpf
    common_smooth_log_r_sufficient: mp.mpf
    square_bypass_kappa_sum_upper_bound: mp.mpf
    square_bypass_log_r_sufficient: mp.mpf
    log_r_sufficient: mp.mpf
    loglog_r_at_cutoff: mp.mpf
    l_plus_one_at_cutoff: mp.mpf
    l995_relative_error_at_cutoff: mp.mpf
    determinant_absorption_verified: bool
    discrepancy_absorption_verified: bool
    l995_upper_factor_verified: bool
    square_bypass_linearization_verified: bool
    gate_verified: bool
    source_scalar_multiplier_certified: bool
    line_905_subpackage_closed: bool
    h1b_l84_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


@dataclass(frozen=True)
class CertifiedLine905ScalarCertificate:
    """Composition of the recovered scalar bound with the square bypass."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    log_r: mp.mpf
    scalar_epsilon_upper_bound: mp.mpf
    square_bypass_delta_sum_upper_bound: mp.mpf
    conditional_square_certificate: ConditionalHSquareBypassCertificate
    source_scalar_multiplier_certified: bool
    line_905_scalar_subpackage_closed: bool
    h1b_l84_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


def _validate_k(k: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < H1B1B2D1A1_MINIMUM_K:
        raise ValueError(
            f"k must be an integer at least {H1B1B2D1A1_MINIMUM_K}"
        )


def _positive_mpf(value: int | float | str | mp.mpf, name: str) -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and positive")
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _prime_factors(value: int) -> tuple[int, ...]:
    """Return distinct prime divisors for small exact-test integers."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("value must be a positive integer")
    remaining = value
    factors: list[int] = []
    divisor = 2
    while divisor <= isqrt(remaining):
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def _totient(value: int) -> int:
    result = value
    for prime in _prime_factors(value):
        result = result // prime * (prime - 1)
    return result


def exact_prefactor_cancellation(a_m: int, wb: int, r: int) -> Fraction:
    """Return the exact base prefactor in equations (9.44)--(9.48).

    Under ``gcd(r, W*B)=1`` this is identically one, even if ``a_m`` and
    ``r`` share prime factors:

    ``a_m*WB/phi(a_m*WB) * r/phi_L(r) * phi(a_m*WB*r)/(a_m*WB*r)``.
    """

    if any(isinstance(value, bool) or not isinstance(value, int) or value < 1
           for value in (a_m, wb, r)):
        raise ValueError("a_m, wb and r must be positive integers")
    if gcd(wb, r) != 1:
        raise ValueError("the source application requires gcd(r,WB)=1")

    phi_l = Fraction(_totient(a_m * r), _totient(a_m))
    result = (
        Fraction(a_m * wb, _totient(a_m * wb))
        * Fraction(r, 1)
        / phi_l
        * Fraction(_totient(a_m * wb * r), a_m * wb * r)
    )
    if result != 1:
        raise AssertionError("the exact totient/phi_L cancellation failed")
    return result


def t_divisor_log_linear_form(
    prime_root_counts: Sequence[tuple[int, int]],
) -> TDivisorLogLinearForm:
    """Return the exact formal value of the divisor sum in (9.43).

    For ``q_p=1/(p-omega(p))``, the sum over square-free divisors is

    ``P * (1 + sum_p log(p)/(p-omega(p)+1))``, ``P=product_p(1+q_p)``.

    Logarithms are kept as formal basis symbols, so this identity is checked
    in exact rational arithmetic rather than floating point.
    """

    pairs = tuple(prime_root_counts)
    primes = tuple(prime for prime, _ in pairs)
    if len(set(primes)) != len(primes):
        raise ValueError("prime entries must be distinct")
    for prime, root_count in pairs:
        if (
            isinstance(prime, bool)
            or isinstance(root_count, bool)
            or not isinstance(prime, int)
            or not isinstance(root_count, int)
            or not 1 <= root_count < prime
        ):
            raise ValueError("require integer pairs with 1 <= omega(p) < p")

    product = Fraction(1)
    for prime, root_count in pairs:
        product *= 1 + Fraction(1, prime - root_count)
    coefficients = tuple(
        (prime, product / (prime - root_count + 1))
        for prime, root_count in sorted(pairs)
    )
    return TDivisorLogLinearForm(
        constant=product,
        log_coefficients=coefficients,
    )


def t_divisor_coefficient_chain() -> Fraction:
    """Return the exact coarse coefficient proved to be below 19.

    The factors are respectively ``exp(1/k)<36/35``, the
    Rosser--Schoenfeld totient coefficient ``<3+2.51``, and the weighted
    logarithm coefficient ``<=1+9/4`` after ``L_D>=1``.
    """

    coefficient = Fraction(36, 35) * Fraction(551, 100) * Fraction(13, 4)
    if not coefficient < H1B1B2D1A1_T_DIVISOR_LOGLOG_SQUARED_BOUND:
        raise AssertionError("the t-divisor coefficient no longer fits below 19")
    return coefficient


def direct_profile_envelope_certificate(k: int) -> DirectProfileEnvelopeCertificate:
    """Evaluate the two inequalities behind the direct (9.47) error bound."""

    _validate_k(k)
    k_value = mp.mpf(k)
    t_k = k_value * mp.log(k_value)
    u_k = 1 / mp.sqrt(k_value)
    i_n_lower = mp.log(1 + mp.mpf("0.9") * u_k * t_k) / t_k
    b_lower = (k_value - 1) * i_n_lower
    gmax_upper = 51 + 50 * u_k + u_k * t_k
    half_gate = b_lower >= mp.mpf("0.5")
    derivative_gate = gmax_upper <= t_k
    if not half_gate or not derivative_gate:
        raise AssertionError("the k>=36 direct-profile envelope gate failed")
    return DirectProfileEnvelopeCertificate(
        k=k,
        t_k=t_k,
        u_k=u_k,
        i_n_lower_bound=i_n_lower,
        b_over_outer_product_lower_bound=b_lower,
        scaled_gmax_over_outer_product_upper_bound=gmax_upper,
        half_integral_gate_passed=half_gate,
        derivative_gate_passed=derivative_gate,
    )


def scalar_remainder_constant_certificate() -> ScalarRemainderConstantCertificate:
    """Return the explicit common multiplier ``C_Y``.

    If the finite gate and Maynard's source assumptions hold, the result is

    ``epsilon_Y <= C_Y*T_k*(log log R)^2/log R``.
    """

    c_83 = weighted_lemma83_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    direct = H1B1B2D1A1_DIRECT_BRANCH_FACTOR * c_83
    common = direct + H1B1B2D1A1_YM_ERROR_COEFFICIENT
    return ScalarRemainderConstantCertificate(
        weighted_lemma83_multiplier=c_83,
        direct_branch_multiplier=direct,
        ym_error_exact_multiplier=H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT,
        ym_error_integer_multiplier=H1B1B2D1A1_YM_ERROR_COEFFICIENT,
        common_c_y=common,
        common_c_y_formula=(
            "4*C_8.3(1/2,8)+10143681 = "
            "327680*(14801/69)*exp(264)+10143697"
        ),
    )


def scalar_remainder_gate_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
) -> ScalarRemainderGateCertificate:
    """Construct a sufficient cutoff for the complete scalar remainder.

    The certificate remains conditional on Maynard's original source
    relations ``k <= (log x)^(1/5)`` and
    ``x^(theta/10) <= R <= x^(theta/3)``.  It makes every additional cutoff
    introduced by the project proof explicit.
    """

    _validate_k(k)
    alpha_value = _positive_mpf(alpha, "alpha")
    theta_value = _positive_mpf(theta, "theta")
    if theta_value >= 1:
        raise ValueError("theta must lie in (0,1)")

    common_gate = common_smooth_gate_certificate(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
    )
    k_value = mp.mpf(k)
    affine_constant = (
        2 * k_value**2 * mp.log(2 * k_value**2)
        + k_value * (k_value - 1) * mp.log(2)
    )
    affine_slope = (
        10 * alpha_value * (2 * k_value**2 - k_value + 1) / theta_value
        + k_value
    )

    # From Delta_m <= (2*x^(2*alpha))^(k-1), the source bounds on x,R,k
    # give log(Delta_m) <= C_delta*(log R)^(6/5).
    determinant_growth = (10 / theta_value) ** (mp.mpf(1) / 5) * (
        mp.log(2) + 20 * alpha_value / theta_value
    )
    determinant_loglog_requirement = max(
        mp.mpf(1),
        mp.mpf(5) / 4 * max(mp.mpf(0), mp.log(determinant_growth)),
    )

    # L+1 = 6+log(Lambda_star), and Lambda_star <= (A+B)*log R for
    # log R>=1.  Requiring log log R >= 6+log(A+B) gives L+1<=2loglog R.
    discrepancy_requirement = max(
        mp.mpf(1),
        6 + mp.log(affine_constant + affine_slope),
    )
    square_kappa_max = max(
        mp.fsum(family)
        for category in (
            CATEGORY_A_SQUARED,
            CATEGORY_A_TIMES_B,
            CATEGORY_B_SQUARED,
        )
        for family in h_square_kappa_families(k, category)
    )
    c_83 = scalar_remainder_constant_certificate().weighted_lemma83_multiplier
    square_e_coefficient = c_83 * square_kappa_max
    square_gate = max(
        mp.mpf(1),
        mp.sqrt(k_value) * mp.log(2),
        4 * square_e_coefficient * mp.log(4 * square_e_coefficient),
        2 * square_e_coefficient * discrepancy_requirement,
    )
    log_r_sufficient = max(
        common_gate.log_r_sufficient,
        square_gate,
        mp.exp(determinant_loglog_requirement),
        mp.exp(discrepancy_requirement),
    )
    loglog_r = mp.log(log_r_sufficient)
    lambda_star = maynard_uniform_application_log_q_upper(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_sufficient,
    )
    l_plus_one = 6 + mp.log(lambda_star)
    l995_delta = (
        c_83 * l_plus_one * f2_one_variable_kappa(k) / log_r_sufficient
    )
    square_delta_sum = (
        c_83 * l_plus_one * square_kappa_max / log_r_sufficient
    )
    determinant_absorption = (
        mp.mpf(6) / 5 * loglog_r + mp.log(determinant_growth)
        <= H1B1B2D1A1_DETERMINANT_LOGLOG_MULTIPLIER * loglog_r
    )
    discrepancy_absorption = l_plus_one <= 2 * loglog_r
    l995_upper = l995_delta <= 1
    square_linearization = square_delta_sum <= 1
    gate_verified = (
        common_gate.gate_verified
        and determinant_absorption
        and discrepancy_absorption
        and l995_upper
        and square_linearization
        and log_r_sufficient >= mp.sqrt(k_value) * mp.log(2)
    )
    if not gate_verified:
        raise AssertionError("the scalar-remainder sufficient gate failed")

    return ScalarRemainderGateCertificate(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        lambda_affine_constant=affine_constant,
        lambda_affine_slope=affine_slope,
        determinant_growth_coefficient=determinant_growth,
        determinant_loglog_requirement=determinant_loglog_requirement,
        discrepancy_loglog_requirement=discrepancy_requirement,
        common_smooth_log_r_sufficient=common_gate.log_r_sufficient,
        square_bypass_kappa_sum_upper_bound=square_kappa_max,
        square_bypass_log_r_sufficient=square_gate,
        log_r_sufficient=log_r_sufficient,
        loglog_r_at_cutoff=loglog_r,
        l_plus_one_at_cutoff=l_plus_one,
        l995_relative_error_at_cutoff=l995_delta,
        determinant_absorption_verified=determinant_absorption,
        discrepancy_absorption_verified=discrepancy_absorption,
        l995_upper_factor_verified=l995_upper,
        square_bypass_linearization_verified=square_linearization,
        gate_verified=gate_verified,
        source_scalar_multiplier_certified=True,
        line_905_subpackage_closed=True,
        h1b_l84_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


def certified_line905_scalar_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
) -> CertifiedLine905ScalarCertificate:
    """Apply the recovered source epsilon to the exact square-sum bypass.

    This closes only the line-905 scalar/smooth subpackage.  The two sharp
    applications remain outside this certificate, so the parent Lemma 8.4
    and theorem flags stay false.
    """

    log_r_value = _positive_mpf(log_r, "log_r")
    gate = scalar_remainder_gate_certificate(
        k=k,
        alpha=alpha,
        theta=theta,
    )
    if log_r_value < gate.log_r_sufficient:
        raise ValueError("log_r is below the certified scalar/square gate")
    constants = scalar_remainder_constant_certificate()
    scalar_epsilon = (
        constants.common_c_y
        * mp.mpf(k)
        * mp.log(k)
        * mp.log(log_r_value) ** 2
        / log_r_value
    )
    conditional = conditional_h_square_bypass_certificate(
        k=k,
        alpha=alpha,
        theta=theta,
        log_r=log_r_value,
        scalar_epsilon=scalar_epsilon,
    )
    square_delta_sum = (
        constants.weighted_lemma83_multiplier
        * conditional.l_plus_one
        * gate.square_bypass_kappa_sum_upper_bound
        / log_r_value
    )
    if square_delta_sum > 1:
        raise AssertionError("the certified square-bypass gate failed")
    return CertifiedLine905ScalarCertificate(
        k=k,
        alpha=gate.alpha,
        theta=gate.theta,
        log_r=log_r_value,
        scalar_epsilon_upper_bound=scalar_epsilon,
        square_bypass_delta_sum_upper_bound=square_delta_sum,
        conditional_square_certificate=conditional,
        source_scalar_multiplier_certified=True,
        line_905_scalar_subpackage_closed=True,
        h1b_l84_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


__all__ = [
    "CertifiedLine905ScalarCertificate",
    "DirectProfileEnvelopeCertificate",
    "H1B1B2D1A1_DETERMINANT_LOGLOG_MULTIPLIER",
    "H1B1B2D1A1_DIRECT_BRANCH_FACTOR",
    "H1B1B2D1A1_EM_SUM_UPPER_FACTOR",
    "H1B1B2D1A1_MINIMUM_K",
    "H1B1B2D1A1_PREFACTOR_RESIDUAL_BOUND",
    "H1B1B2D1A1_S_EULER_PRODUCT_BOUND",
    "H1B1B2D1A1_T_DIVISOR_LOGLOG_SQUARED_BOUND",
    "H1B1B2D1A1_YM_ERROR_COEFFICIENT",
    "H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT",
    "ScalarRemainderConstantCertificate",
    "ScalarRemainderGateCertificate",
    "TDivisorLogLinearForm",
    "direct_profile_envelope_certificate",
    "certified_line905_scalar_certificate",
    "exact_prefactor_cancellation",
    "scalar_remainder_constant_certificate",
    "scalar_remainder_gate_certificate",
    "t_divisor_coefficient_chain",
    "t_divisor_log_linear_form",
]
