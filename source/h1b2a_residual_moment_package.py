"""Finite envelopes for the Sono/FMT H1b-2a residual moment audit.

The mathematical proofs live in
``docs/method/theory/28_Sono_FMT_H1b2a_residual_moment_error_package.md``.
This module evaluates those proved formulae and fails closed on the parent
Maynard package: it neither proves Hypothesis 1 nor computes ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from source.h1a_finite_r_integral import H1A_Q_DENOMINATOR, H1A_Q_NUMERATOR
from source.h1b1b2_local_factor_lower_bound import APPLICATION_L620_D_W
from source.h1b1b2d_rfold_smooth_package import rfold_error_certificate


H1B2A_MINIMUM_K = 36


@dataclass(frozen=True)
class IntegralSizeCertificate:
    """Explicit Lemma 8.6 bounds for the actual Maynard test function."""

    k: int
    q: mp.mpf
    t_k: mp.mpf
    u_k: mp.mpf
    cube_endpoint: mp.mpf
    cube_one_dimensional_integral: mp.mpf
    i_lower_bound: mp.mpf
    canonical_i_lower_bound: mp.mpf
    j_lower_bound: mp.mpf
    i_f2_over_k2_multiplier: mp.mpf
    j_f2_over_k2_multiplier: mp.mpf
    plateau_gate_passed: bool
    lower_bound_verified: bool
    pointwise_comparisons_verified: bool
    theorem_claimed: bool
    siv_07_closed: bool
    x_cert_ready: bool


@dataclass(frozen=True)
class CoefficientWeightCertificate:
    """Finite replacements for the three claims of Maynard Lemma 8.5."""

    k: int
    log_r: mp.mpf
    lambda_multiplier: mp.mpf
    lambda_multiplier_at_most_e: bool
    local_weight_multiplier: mp.mpf
    log_global_weight_coefficient: mp.mpf
    finite_exponent_excess: mp.mpf
    support_endpoint_gate_passed: bool
    smooth_linearization_gate_passed: bool
    theorem_claimed: bool
    siv_07_closed: bool
    x_cert_ready: bool


@dataclass(frozen=True)
class Proposition94LocalCertificate:
    """Closed local algebra/Euler factors and open P9.4 root dependencies."""

    k: int
    maximum_u: mp.mpf
    denominator_ratio_upper: mp.mpf
    denominator_two_over_p_gate_passed: bool
    first_euler_log_upper: mp.mpf
    first_euler_multiplier_upper: mp.mpf
    squared_y_multiplier_upper: mp.mpf
    symmetry_multiplier: int
    distribution_error_closed: bool
    final_euler_products_closed: bool
    proposition_94_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


def _validate_k(k: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < H1B2A_MINIMUM_K:
        raise ValueError(f"k must be an integer at least {H1B2A_MINIMUM_K}")


def _positive_mpf(value: int | float | str | mp.mpf, name: str) -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and positive")
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def integral_size_certificate(k: int) -> IntegralSizeCertificate:
    """Evaluate the exact plateau-cube and coarse F1/F2 comparisons.

    On the cube ``0 <= t_i <= q/k`` both cutoffs in the actual test function
    are one.  This gives ``I_k(F) >= [q/(k(1+q log k))]^k``.  For
    ``q log k >= 1`` it dominates ``(2 k log k)^(-k)``.
    """

    _validate_k(k)
    k_mpf = mp.mpf(k)
    q = mp.mpf(H1A_Q_NUMERATOR) / H1A_Q_DENOMINATOR
    log_k = mp.log(k_mpf)
    t_k = k_mpf * log_k
    u_k = 1 / mp.sqrt(k_mpf)
    cube_endpoint = q / k_mpf
    cube_integral = q / (k_mpf * (1 + q * log_k))
    i_lower = cube_integral**k
    canonical_i_lower = (2 * t_k) ** (-k)
    plateau_gate = q * log_k >= 1

    # H1a proves J/I > log(k)/(4k) for every integer k>=36.
    j_lower = log_k / (4 * k_mpf) * canonical_i_lower

    # Put n(t)=psi(t/U)/(1+Tt), h(t)=psi(t/2)/(1+Tt).
    # I(F2) is expanded exactly and bounded with all L2 products <=1/T.
    i_multiplier = mp.power(2, k)

    narrow_l1_log = mp.log(1 + t_k * u_k)
    wide_l1_log = mp.log(1 + 2 * t_k)
    combined_l1_log = wide_l1_log + (k_mpf - 1) * narrow_l1_log
    j_multiplier = (
        4
        * mp.power(2, k)
        * combined_l1_log**2
        / (k_mpf**2 * log_k**2)
    )

    # F<=F1 and F2>=kF1 follow pointwise from 0<=psi<=1 and
    # psi(t/2)=1 on the support of psi(t/U), since U<=1.
    pointwise_gate = u_k <= 1 and q <= 1
    return IntegralSizeCertificate(
        k=k,
        q=q,
        t_k=t_k,
        u_k=u_k,
        cube_endpoint=cube_endpoint,
        cube_one_dimensional_integral=cube_integral,
        i_lower_bound=i_lower,
        canonical_i_lower_bound=canonical_i_lower,
        j_lower_bound=j_lower,
        i_f2_over_k2_multiplier=i_multiplier,
        j_f2_over_k2_multiplier=j_multiplier,
        plateau_gate_passed=bool(plateau_gate),
        lower_bound_verified=bool(i_lower >= canonical_i_lower),
        pointwise_comparisons_verified=bool(pointwise_gate),
        theorem_claimed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


def coefficient_weight_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
) -> CoefficientWeightCertificate:
    """Evaluate explicit finite Lemma 8.5 coefficient and support bounds.

    If ``M=1+epsilon_620``, the proved inequalities are

    ``|lambda_d| <= M (log R/k)^k``;

    ``w_n <= M^2 (log x/k)^(2k) product 4``;

    ``w_n <= R^(2+eta)``, where ``eta`` is the nonnegative exponent returned
    below.  The last bound uses
    ``# {d_1...d_k<R} <= R(1+log R)^k``.
    """

    _validate_k(k)
    log_r_value = _positive_mpf(log_r, "log_r")
    support_gate = log_r_value >= mp.sqrt(k) * mp.log(2)
    if not support_gate:
        raise ValueError("log_r must satisfy the narrow-profile support gate")

    l620 = rfold_error_certificate(
        application_id=APPLICATION_L620_D_W,
        k=k,
        alpha=alpha,
        theta=theta,
        log_r=log_r_value,
    )
    lambda_multiplier = 1 + l620.product_error_upper_bound
    local_weight_multiplier = lambda_multiplier**2

    # The factor beyond R^2 in the global support-count bound is
    # M^2 * [(log R/k)(1+log R)]^(2k).  Its log avoids constructing R.
    log_global_coefficient = (
        2 * mp.log(lambda_multiplier)
        + 2
        * k
        * (mp.log(log_r_value) - mp.log(k) + mp.log(1 + log_r_value))
    )
    finite_excess = max(mp.mpf(0), log_global_coefficient / log_r_value)
    multiplier_at_most_e = (
        l620.delta_sum_upper_bound <= 1
        and lambda_multiplier <= mp.e
    )
    return CoefficientWeightCertificate(
        k=k,
        log_r=log_r_value,
        lambda_multiplier=lambda_multiplier,
        lambda_multiplier_at_most_e=bool(multiplier_at_most_e),
        local_weight_multiplier=local_weight_multiplier,
        log_global_weight_coefficient=log_global_coefficient,
        finite_exponent_excess=finite_excess,
        support_endpoint_gate_passed=bool(support_gate),
        smooth_linearization_gate_passed=l620.linearization_gate_passed,
        theorem_claimed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


def proposition94_local_certificate(k: int) -> Proposition94LocalCertificate:
    """Return explicit local bounds from Maynard Proposition 9.4.

    For ``p>2k^2`` and ``m=omega*(p)<=k+1``, the line-(9.57) factor
    ``(p+m-2)/(p-m)^2`` is at most ``2/p``.  The first Euler product in
    (9.63) is at most ``exp(2/k)``.  These facts do not close the
    distribution error in (9.52) or the two products in (9.67).
    """

    _validate_k(k)
    k_mpf = mp.mpf(k)
    maximum_u = (k_mpf + 1) / (2 * k_mpf**2)
    denominator_ratio = (1 + maximum_u) / (1 - maximum_u) ** 2
    first_log = 2 / k_mpf
    first_multiplier = mp.exp(first_log)
    return Proposition94LocalCertificate(
        k=k,
        maximum_u=maximum_u,
        denominator_ratio_upper=denominator_ratio,
        denominator_two_over_p_gate_passed=bool(denominator_ratio <= 2),
        first_euler_log_upper=first_log,
        first_euler_multiplier_upper=first_multiplier,
        squared_y_multiplier_upper=first_multiplier**2,
        symmetry_multiplier=1,
        distribution_error_closed=False,
        final_euler_products_closed=False,
        proposition_94_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


__all__ = [
    "CoefficientWeightCertificate",
    "H1B2A_MINIMUM_K",
    "IntegralSizeCertificate",
    "Proposition94LocalCertificate",
    "coefficient_weight_certificate",
    "integral_size_certificate",
    "proposition94_local_certificate",
]
