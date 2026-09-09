"""Scalar diagnostics for the project H1b-P92a finite identity-form proof.

The analytic all-parameter proof is theory 44, not a finite sampling claim.
Only k and L=log(T) are represented. No prime experiment, T=exp(L), k-element
array, or enormous negative-power denominator is constructed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

import mpmath as mp

INTEGRAL_COMPARISON_MIN_K = 10**50
ACTUAL_IDENTITY_MOMENT_MIN_K = 10**200
ONE_STEP_MULTIPLIER_UPPER = 10**123
SCALAR_REMAINDER_MULTIPLIER_UPPER = 10**123
REASSIGNMENT_MULTIPLIER_UPPER = 5 * 10**123
OFF_DIAGONAL_INTEGER_FACTOR = 8 * 72 * 27 * 16
RELATIVE_MAJORANT_MULTIPLIER = 10**135


@dataclass(frozen=True)
class IntegralComparisonCertificate:
    k: int
    mean_upper: mp.mpf
    variance_upper: mp.mpf
    one_minus_cantelli_probability_lower: mp.mpf
    i_f1_over_i_f_upper: int
    j_f1_over_j_f_upper: int
    i_f2_over_i_f_upper: int
    j_f2_over_j_f_upper: int
    slice_over_j_f_upper: int
    gate_passed: bool
    based_on_analytic_all_k_proof: bool
    numerical_integration_performed: bool = False


@dataclass(frozen=True)
class IdentityPrimeMomentCertificate:
    k: int
    log_t_exact: Fraction
    working_dps: int
    log_r: mp.mpf
    smooth_delta_upper: mp.mpf
    scalar_epsilon_upper: mp.mpf
    log_main_relative_error_upper: mp.mpf
    log_main_relative_majorant: mp.mpf
    log_relative_target: mp.mpf
    log_distribution_ratio_upper: mp.mpf
    log_distribution_certificate: mp.mpf
    log_weight_atom_ratio_upper: mp.mpf
    log_prime_count_atom_ratio_upper: mp.mpf
    log_atom_certificate: mp.mpf
    checks: tuple[tuple[str, bool], ...]
    relative_multiplier: int
    additive_multiplier: int
    actual_identity_application_closed: bool
    lower_endpoint_weight_closed: bool
    conditional_on_actual_form_construction: bool = True
    general_proposition92_closed: bool = False
    proposition61_closed: bool = False
    siv_07_closed: bool = False
    siv_08_closed: bool = False
    siv_09_closed: bool = False
    x_cert_ready: bool = False
    actual_prime_experiment_performed: bool = False
    lean_verified: bool = False


def _validate_k(k: int, minimum: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < minimum:
        raise ValueError(f"k must be an integer at least {minimum}")


def _exact_fraction(value: int | str | Fraction) -> Fraction:
    # Binary floats / mpf are forbidden at exact dimension-bin boundaries.
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError("log_t must be an exact int, decimal string, or Fraction")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("log_t must be a finite positive exact value") from exc
    if result <= 0:
        raise ValueError("log_t must be positive")
    return result


def exact_dimension_bin(k: int, log_t: int | str | Fraction) -> Fraction:
    """Check k=floor(log(T)^(1/5)) with integer arithmetic, not a float root."""
    _validate_k(k, 36)
    value = _exact_fraction(log_t)
    if not k**5 <= value < (k + 1)**5:
        raise ValueError("require k**5 <= log_t < (k+1)**5 exactly")
    return value


def elementary_rational_witnesses() -> dict[str, bool]:
    """Rational series witnesses used by the monotonic analytic proof.

    For log(10), use 2*atanh(9/11), keeping a geometric upper remainder.
    For exp(6), positive Taylor terms alone certify the needed lower bound.
    """
    t = Fraction(9, 11)
    terms = 40
    lower = 2 * sum((t**(2*j + 1) / (2*j + 1) for j in range(terms)), Fraction())
    tail = 2 * t**(2*terms + 1) / ((2*terms + 1) * (1-t*t))
    exp_six_lower = sum((Fraction(6**j, factorial(j)) for j in range(21)), Fraction())
    # CY = (327680 * 14801/69) * exp(264) + 10143697.
    cy_coefficient = Fraction(327680 * 14801, 69)
    return {
        "log10_above_23_over_10": lower > Fraction(23, 10),
        "log10_below_5_over_2": lower + tail < Fraction(5, 2),
        "exp6_above_363_and_200": exp_six_lower > 363,
        "exp264_below_10pow115_from_log10": 115 * Fraction(23, 10) > 264,
        "cy_below_10pow123_using_exp264": (
            cy_coefficient * 10**115 + 10143697 < SCALAR_REMAINDER_MULTIPLIER_UPPER
        ),
        "off_diagonal_coefficient_exact": OFF_DIAGONAL_INTEGER_FACTOR == 248832,
        "off_diagonal_coarse_slack": (
            OFF_DIAGONAL_INTEGER_FACTOR * REASSIGNMENT_MULTIPLIER_UPPER * 36 * 30
            < 10**133
        ),
        "minimum_dimension_absorbs_uniform_loss": (
            ACTUAL_IDENTITY_MOMENT_MIN_K >= 2 * RELATIVE_MAJORANT_MULTIPLIER
        ),
    }


def integer_growth_witnesses(k: int) -> dict[str, bool]:
    """Polynomial sufficient conditions, valid for every integer k>=36."""
    _validate_k(k, 36)
    return {
        "modulus_capacity_polynomial": k*k >= 18*k + 18,
        "weighted_distribution_absorption": 18*k*k - 21*k - 18 >= 0,
        "weight_atom_absorption": 4*(15*k*k + 13*k + 3) <= k**5,
    }


def identity_local_euler_ratios(prime: int, root_count: int) -> tuple[Fraction, Fraction]:
    """Exact rational local cancellation and slice inflation.

    This algebra does not assert primality; the actual caller supplies prime p.
    The toy tests enumerate prime values independently.
    """
    if (isinstance(prime, bool) or isinstance(root_count, bool)
            or not isinstance(prime, int) or not isinstance(root_count, int)
            or not 1 <= root_count < prime):
        raise ValueError("require integer 1 <= root_count < prime")
    p, omega = prime, root_count
    singular_adjustment = Fraction(p - omega, p - 1)
    diagonal = (1 + Fraction(omega - 1, p - omega)) * singular_adjustment
    sliced = (
        1 + Fraction((omega - 1)*(p - 1), (p - omega)**2)
    ) * singular_adjustment
    return diagonal, sliced


def _integral_comparison(k: int) -> IntegralComparisonCertificate:
    kval = mp.mpf(k)
    ell = mp.log(kval)
    sqrtk = mp.sqrt(kval)
    s = sqrtk * ell
    inflation = 1 + 1 / (mp.mpf(9) / 10 * s)
    mean = inflation * mp.log1p(s) / ell
    variance = inflation / (sqrtk * ell)
    # The k-1-coordinate event has a smaller cutoff than the k-coordinate one.
    deviation = mp.mpf(9)/10 - 1/sqrtk - mean
    probability_lower = deviation**2 / (variance + deviation**2)
    checks = (
        mean < mp.mpf(3)/5,
        variance < mp.mpf(1)/16,
        1/sqrtk < mp.mpf(1)/100,
        deviation > mp.mpf(1)/4,
        probability_lower > mp.mpf(1)/2,
        ell <= kval**(mp.mpf(1)/8),
    )
    if not all(checks):
        raise AssertionError("uniform integral comparison diagnostic failed")
    return IntegralComparisonCertificate(
        k=k, mean_upper=mean, variance_upper=variance,
        one_minus_cantelli_probability_lower=probability_lower,
        i_f1_over_i_f_upper=2, j_f1_over_j_f_upper=2,
        i_f2_over_i_f_upper=4*k*k, j_f2_over_j_f_upper=8*k*k,
        slice_over_j_f_upper=16*k**4, gate_passed=True,
        based_on_analytic_all_k_proof=True,
    )


def integral_comparison_certificate(k: int) -> IntegralComparisonCertificate:
    _validate_k(k, INTEGRAL_COMPARISON_MIN_K)
    with mp.workdps(max(100, len(str(k)) + 60)):
        return _integral_comparison(k)


def identity_prime_moment_certificate(
    *, k: int, log_t: int | str | Fraction | None = None,
) -> IdentityPrimeMomentCertificate:
    """Check scalar envelopes for theory 44's one actual application.

    Primality distribution is supplied by the existing project theorem 43,
    not recomputed here. Structural assumptions on the actual forms, B, W
    and weights remain explicit in theory 44 and the machine contract.
    This is not a numerical Sono/FMT threshold calculator.
    """
    _validate_k(k, ACTUAL_IDENTITY_MOMENT_MIN_K)
    L_exact = exact_dimension_bin(k, k**5 if log_t is None else log_t)
    dps = max(100, len(str(L_exact.numerator)) + len(str(L_exact.denominator)) + 60)
    with mp.workdps(dps):
        kval = mp.mpf(k)
        L = mp.mpf(L_exact.numerator) / L_exact.denominator
        ell, logL = mp.log(kval), mp.log(L)
        y = (L - mp.log(2)) / 9
        v, K = mp.log(y), kval * ell
        affine_a = 2*kval**2*mp.log(2*kval**2) + kval*(kval-1)*mp.log(2)
        affine_b = 60*(2*kval**2-kval+1) + kval
        lambda_star = affine_a + affine_b*y
        lplus = 6 + mp.log(lambda_star)
        kappa = 3000*kval**3*ell**2
        delta = ONE_STEP_MULTIPLIER_UPPER*lplus*kappa/y
        epsilon = SCALAR_REMAINDER_MULTIPLIER_UPPER*K*v**2/y
        diag_error = 4*delta + 24*kval*epsilon + 24*kval**2*epsilon**2
        off_error = (
            OFF_DIAGONAL_INTEGER_FACTOR * REASSIGNMENT_MULTIPLIER_UPPER
            * kval**3 * ell**2 * v**2 / y
        )
        log_main = mp.log(diag_error + off_error)
        log_majorant = mp.log(RELATIVE_MAJORANT_MULTIPLIER) + 4*mp.log(ell) - 2*ell
        log_target = -logL / 10
        logw_upper = 2*kval**2*mp.log(2*kval**2)
        # Before the coarse polynomial absorptions (44.16), (44.24).
        log_dist = (
            mp.log(2)/2 + 2 + logw_upper + mp.mpf(9)/2*kval
            + kval*mp.log(2) - kval*ell + kval*mp.log(ell)
            + (kval+1)*v - 41*kval**2*logL
        )
        log_dist_certificate = -190*kval**2*ell
        log_atom = (
            mp.log(2) + 2 + mp.mpf(9)/2*kval + kval*mp.log(2)
            - kval*ell + kval*mp.log(ell) + (kval+1)*v
            + 2*kval*mp.log1p(y) + 2*y - L
        )
        log_count_atom = mp.log(2) + 2*v - ell/2 - L
        determinant_log = mp.log(mp.power(30, mp.mpf(1)/5)*(mp.log(2)+120))
        integral = _integral_comparison(k)
        checks: dict[str, bool] = {
            **elementary_rational_witnesses(),
            **integer_growth_witnesses(k),
            "exact_dimension_bin": k**5 <= L_exact < (k+1)**5,
            "hypothesis43_tail_domain": k >= 10**10,
            "integral_comparison": integral.gate_passed,
            "actual_R_lower": y >= L/30,
            "actual_R_upper": y <= L/9,
            "narrow_support": y/mp.sqrt(kval) >= mp.log(2),
            "lambda_star_majorant": lambda_star <= 121*kval**2*y,
            "discrepancy_loglog_gate": lplus <= 2*v,
            "discrepancy_logk_gate": lplus <= 12*ell,
            "determinant_gate": v >= max(1, mp.mpf(5)/4*determinant_log),
            "smooth_gate": delta < mp.mpf(1)/2,
            "scalar_gate": kval*epsilon < 1,
            "smooth_polynomial_envelope": delta <= mp.mpf(10)**130*ell**3/kval**2,
            "scalar_polynomial_envelope": epsilon <= mp.mpf(10)**127*ell**3/kval**4,
            "modulus_capacity": logw_upper + 2*y <= L/3,
            "main_majorant": log_main <= log_majorant,
            "main_relative_target": log_majorant <= log_target,
            "distribution_additive_bound": log_dist <= log_dist_certificate,
            "weight_atom": log_atom <= -L/2,
            "count_atom": log_count_atom <= -L/2,
            # Avoid exp(-L) and enormous negative-power denominators entirely.
            "additive_multiplier_one": (
                log_dist_certificate <= -mp.log(8) and -L/2 <= -mp.log(8)
            ),
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            raise AssertionError(f"identity prime-moment diagnostic failed: {failed}")
        return IdentityPrimeMomentCertificate(
            k=k, log_t_exact=L_exact, working_dps=dps, log_r=y,
            smooth_delta_upper=delta, scalar_epsilon_upper=epsilon,
            log_main_relative_error_upper=log_main,
            log_main_relative_majorant=log_majorant, log_relative_target=log_target,
            log_distribution_ratio_upper=log_dist,
            log_distribution_certificate=log_dist_certificate,
            log_weight_atom_ratio_upper=log_atom,
            log_prime_count_atom_ratio_upper=log_count_atom, log_atom_certificate=-L/2,
            checks=tuple(checks.items()), relative_multiplier=1, additive_multiplier=1,
            actual_identity_application_closed=True, lower_endpoint_weight_closed=True,
        )
