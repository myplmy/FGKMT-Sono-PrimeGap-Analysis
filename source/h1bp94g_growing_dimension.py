"""Bounded log-scale diagnostics for theory 46, not a threshold calculator.

The all-k theorem lives in the proof document. Exact integer bins and bounded
toy algebra are separate from actual structural assumptions about the forms.
No X=exp(L), Delta, W, 2**k, or k-dimensional array is built by the certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import prod

import mpmath as mp

from source.h1bp92a_identity_prime_moment import (
    exact_dimension_bin, integral_comparison_certificate,
)

MIN_K = 10**200
WEIGHT_DEFINITION = "maynard_w_filtered"
SMALL_ERROR_BUDGET = Fraction(1, 100)
EULER_RATIONAL_UPPER = 8
UNIFORM_INTEGER_MULTIPLIER = 1
EXACT_COARSE_MULTIPLIER = Fraction(8*101**2, 9*99**2)+Fraction(1, 100)


@dataclass(frozen=True)
class ShiftGeometry:
    local_t: int
    extra_intercept: int
    q_to_t_offset: int
    open_integer_count: int
    closed_integer_count: int
    shifted_forms: tuple[tuple[int, int], ...]
    extra_form: tuple[int, int]
    discriminant: int


@dataclass(frozen=True)
class GrowingP94Certificate:
    k: int
    log_outer_half_exact: Fraction
    log_h_constant_exact: Fraction
    working_dps: int
    log_r: mp.mpf
    log_local_t_lower: mp.mpf
    log_local_t_upper: mp.mpf
    smooth_delta_upper: mp.mpf
    canonical_relative_error_upper: mp.mpf
    sharp_relative_error_upper: mp.mpf
    log_distribution_ratio_upper: mp.mpf
    log_distribution_certificate: mp.mpf
    main_multiplier_diagnostic_upper: mp.mpf
    total_with_distribution_budget_upper: mp.mpf
    exact_coarse_multiplier: Fraction
    delta_over_phi_logarithmic_coefficient: int
    log_off_tuple_relative_upper: mp.mpf
    log_off_tuple_target_lower: mp.mpf
    checks: tuple[tuple[str, bool], ...]
    uniform_integer_multiplier: int = UNIFORM_INTEGER_MULTIPLIER
    weight_definition: str = WEIGHT_DEFINITION
    w_filter_required: bool = True
    filtered_growing_p94_child_closed: bool = True
    exact_actual_interval_bridge_closed: bool = True
    per_p_local_series_off_tuple_bound_closed: bool = True
    conditional_on_actual_form_construction: bool = True
    literal_unfiltered_transfer_certified: bool = False
    general_proposition94_closed: bool = False
    common_normalization_closed: bool = False
    full_good_sieve_weight_closed: bool = False
    x_cert_ready: bool = False
    actual_prime_experiment_performed: bool = False
    lean_verified: bool = False


def _integer(value: int, name: str, minimum: int | None = None) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an exact integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")


def _exact(value: int | str | Fraction, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError(f"{name} must be an exact integer/string/Fraction")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be finite") from exc


def shift_geometry(
    x: int | str | Fraction, y: int | str | Fraction, *,
    p: int, h: int, shifts: tuple[int, ...],
) -> ShiftGeometry:
    """Exact bounded toy transport; does not certify p or admissibility."""
    X, Y = _exact(x, "x"), _exact(y, "y")
    _integer(p, "p", 2)
    _integer(h, "h")
    if not shifts:
        raise ValueError("nonempty shifts are required")
    for value in shifts:
        _integer(value, "shift")
    if len(set(shifts)) != len(shifts) or h in shifts:
        raise ValueError("distinct shifts and a genuinely extra h are required")
    a, b = X.numerator//X.denominator, Y.numerator//Y.denominator
    if X < 2 or Y <= X or b <= a:
        raise ValueError("require 2<=X<Y and floor(Y)>floor(X)")
    T = b-a
    intercept = -b+2*a
    return ShiftGeometry(
        local_t=T, extra_intercept=intercept, q_to_t_offset=b-2*a,
        open_integer_count=T, closed_integer_count=T+1,
        shifted_forms=tuple((1, intercept+(hi-h)*p) for hi in shifts),
        extra_form=(1, intercept),
        discriminant=prod(abs((hi-h)*p) for hi in shifts),
    )


def selberg_square_majorant(
    n: int, coefficients: tuple[tuple[int, Fraction], ...],
) -> Fraction:
    """Bounded exact square for toy tests; roughness needs a support check."""
    _integer(n, "n", 1)
    if not coefficients:
        raise ValueError("coefficients are required")
    normalized = {}
    for d, value in coefficients:
        _integer(d, "divisor", 1)
        if d in normalized:
            raise ValueError("duplicate divisor")
        normalized[d] = _exact(value, "coefficient")
    if normalized.get(1, Fraction()) == 0:
        raise ValueError("the Selberg normalization coefficient must be nonzero")
    total = sum((value for d, value in normalized.items() if n % d == 0), Fraction())
    return total**2 / normalized[1]**2


def integer_growth_witnesses(k: int) -> dict[str, bool]:
    _integer(k, "k", 200)
    euler_upper = Fraction(11, 4)**2/(1-Fraction(6, k))
    return {
        "C_distribution_polynomial": k*k-17*k-14 >= 0,
        "distribution_43k2": 24*k <= k*k,
        "distribution_half_exponent": 90*43 <= 13*k**3,
        "modulus_capacity": k**3 >= 90,
        "euler_below_eight": euler_upper < EULER_RATIONAL_UPPER,
        "coarse_fraction_identity": EXACT_COARSE_MULTIPLIER == Fraction(8249009, 8820900),
        "coarse_fraction_below_one": EXACT_COARSE_MULTIPLIER < 1,
        "off_tuple_constant": 21600*6**10 < 10**13,
    }


def _decimal_digits_upper(value: int) -> int:
    # 30103/100000 > log10(2); avoids Python's int-to-string digit ceiling.
    return max(1, (abs(value).bit_length()*30103)//100000+1)


def growing_p94_certificate(
    *, k: int, log_outer_half: int | str | Fraction | None = None,
    log_h_constant: int | str | Fraction = 0,
    weight_definition: str = WEIGHT_DEFINITION,
) -> GrowingP94Certificate:
    """All-parameter proof diagnostics on the exact actual dimension path.

    log_h_constant is log(C_h), with |h|<=C_h*Y/X assumed structurally.
    The bound log(C_h)<=L/4 is checked exactly. The local scale T0 itself is
    not constructed; L<=log(T0)<=2L is proved in theory 46 and checked via
    its sufficient envelopes, never confused with an equality.
    """
    _integer(k, "k", MIN_K)
    if weight_definition != WEIGHT_DEFINITION:
        raise ValueError("the explicit Maynard W filter is required")
    L_exact = exact_dimension_bin(k, k**5 if log_outer_half is None else log_outer_half)
    H_exact = _exact(log_h_constant, "log_h_constant")
    if not 0 <= 4*H_exact <= L_exact:
        raise ValueError("require 0<=log(C_h)<=log(X/2)/4 exactly")
    dps = max(100, *(
        _decimal_digits_upper(v.numerator)+_decimal_digits_upper(v.denominator)+60
        for v in (L_exact, H_exact)
    ))
    with mp.workdps(dps):
        kval = mp.mpf(k)
        L = mp.mpf(L_exact.numerator)/L_exact.denominator
        H = mp.mpf(H_exact.numerator)/H_exact.denominator
        ell = mp.log(kval)
        u = L+mp.log(2)
        y = (L-mp.log(2))/9
        logu = mp.log(u)
        log_ratio = (
            -mp.log(153600)-mp.log(mp.log(5))+logu
            +mp.log(mp.log(logu))-mp.log(logu)
        )
        A = 2*kval**2*mp.log(2*kval**2)+kval*(kval-1)*mp.log(2)
        B = 60*(2*kval**2-kval+1)+kval
        lam = A+B*y
        delta = mp.mpf(10)**123*(6+mp.log(lam))*3000*kval**3*ell**2/y
        canonical = 4*delta
        sharp = mp.mpf(10)/3*mp.mpf(10)**123*(6+mp.log(lam))/y
        # Evaluate the theory-30 C directly, retaining all its terms.
        A0 = 4*kval**2+kval*mp.log(2)
        B0 = 2*(2*kval+1)
        C = (
            mp.log(8)+8*kval**2+2+mp.mpf(9)/2*kval
            +kval*(mp.log(2)+mp.log(ell)-ell)-mp.log(mp.mpf(1)/30)
            +2*mp.log(6)+2*mp.log(1+mp.log(A0+B0))
            +3*(kval+1)*mp.log(1+4*kval**2+mp.mpf(13)/45)
        )
        log_dist = C+4*(kval+1)*mp.log(2*L)-mp.mpf(29)/45*L
        euler = mp.exp(2+6/kval)
        main = (1+sharp)/(1-sharp)**2*euler*(1+canonical)*y/L
        total_budget = main+mp.mpf(1)/100  # no exp(-L/2) materialization
        off_log = mp.log(720)+mp.log(ell)-mp.log(y)
        target_lower = -10*mp.log(6*ell)
        integral = integral_comparison_certificate(k)
        coarse = mp.mpf(EXACT_COARSE_MULTIPLIER.numerator)/EXACT_COARSE_MULTIPLIER.denominator
        checks = {
            **integer_growth_witnesses(k),
            "exact_dimension_bin": k**5 <= L_exact < (k+1)**5,
            "h_constant_capacity": 0 <= 4*H_exact <= L_exact,
            "Y_at_least_4X": log_ratio > mp.log(4),
            "Y_below_X_logX": log_ratio < logu,
            "local_log_upper": u+logu <= 2*L,
            "R_local_lower": 2*L/30 <= y,
            "R_local_upper": y <= L/9,
            "prime_above_local_rough_cutoff": 2*L/30 < u,
            "form_coefficient_bound": mp.log(5*u)+H <= u,
            "delta_log_upper": u+mp.log(2)+H+logu <= 2*L,
            "profile_support": y/mp.sqrt(kval) >= mp.log(2),
            "lambda_star_bound": lam <= 121*kval*kval*y,
            "uniform_integral": integral.gate_passed,
            "smooth_polynomial": delta <= mp.mpf(10)**130*ell**3/kval**2,
            "sharp_polynomial": sharp <= mp.mpf(10)**127*ell/kval**5,
            "small_canonical": canonical <= mp.mpf(1)/100,
            "small_sharp": sharp <= mp.mpf(1)/100,
            "selberg_denominator_positive": sharp < 1,
            "distribution_C_bound": C <= 18*kval*kval,
            "distribution_log_bound": log_dist <= -L/2,
            "distribution_budget": -L/2 < -mp.log(100),
            "euler_upper": euler < 8,
            "total_below_exact_coarse": total_budget <= coarse,
            "delta_phi_bound": 3*mp.log(2*kval*L)+3 < 24*ell,
            "off_tuple_log_target": off_log < target_lower,
            "log_power_comparison": ell <= kval**(mp.mpf(1)/8),
            "off_tuple_constant_absorption": k**3 > 10**13,
        }
        if not all(checks.values()):
            raise AssertionError([name for name, ok in checks.items() if not ok])
        return GrowingP94Certificate(
            k=k, log_outer_half_exact=L_exact, log_h_constant_exact=H_exact,
            working_dps=dps, log_r=y, log_local_t_lower=L, log_local_t_upper=2*L,
            smooth_delta_upper=delta, canonical_relative_error_upper=canonical,
            sharp_relative_error_upper=sharp, log_distribution_ratio_upper=log_dist,
            log_distribution_certificate=-L/2, main_multiplier_diagnostic_upper=main,
            total_with_distribution_budget_upper=total_budget,
            exact_coarse_multiplier=EXACT_COARSE_MULTIPLIER,
            delta_over_phi_logarithmic_coefficient=24,
            log_off_tuple_relative_upper=off_log,
            log_off_tuple_target_lower=target_lower, checks=tuple(checks.items()),
        )
