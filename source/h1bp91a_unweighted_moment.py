"""Bounded diagnostics for theory 45; not a prime sweep or X_cert calculator.

The all-parameter proof is written separately. Exact bins are checked before
mpmath conversion; no exp(L), W, Y, k-vector, or actual primes are materialized.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

import mpmath as mp

from source.h1bp92a_identity_prime_moment import (
    exact_dimension_bin, integral_comparison_certificate,
)

MIN_K = 10**200
WEIGHT_DEFINITION = "maynard_w_filtered"
OFF_DIAGONAL_FACTOR = 178 * 72 * 27 * 4
RELATIVE_MAJORANT = 10**134


@dataclass(frozen=True)
class UnweightedMomentCertificate:
    k: int
    log_outer_half_exact: Fraction
    working_dps: int
    log_r: mp.mpf
    log_y_over_x: mp.mpf
    smooth_delta_upper: mp.mpf
    log_relative_error_upper: mp.mpf
    log_relative_majorant: mp.mpf
    log_symmetric_relative_majorant: mp.mpf
    log_relative_target_lower: mp.mpf
    log_distribution_ratio_upper: mp.mpf
    log_distribution_certificate: mp.mpf
    checks: tuple[tuple[str, bool], ...]
    weight_definition: str = WEIGHT_DEFINITION
    w_filter_required: bool = True
    filtered_actual_p91_closed: bool = True
    shift_endpoint_closed: bool = True
    conditional_on_actual_form_construction: bool = True
    literal_unfiltered_transfer_certified: bool = False
    general_proposition91_closed: bool = False
    growing_k_proposition94_closed: bool = False
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


def w_filter(n: int, forms: tuple[tuple[int, int], ...], modulus: int) -> int:
    """Exact algebraic indicator for a bounded toy; no primality assertion."""
    _integer(n, "n")
    _integer(modulus, "modulus", 1)
    if not forms:
        raise ValueError("a nonempty form tuple is required")
    for a, b in forms:
        _integer(a, "slope")
        _integer(b, "intercept")
        if a == 0:
            raise ValueError("form slope must be nonzero")
    return int(all(gcd(a*n+b, modulus) == 1 for a, b in forms))


def exact_shift_count(y: int | str | Fraction) -> tuple[int, int, Fraction]:
    """Return T'=2*floor(Y), N=T'+1 and signed N-2Y, exactly."""
    if isinstance(y, bool) or not isinstance(y, (int, str, Fraction)):
        raise ValueError("Y must be an exact positive int/string/Fraction")
    try:
        value = Fraction(y)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Y must be finite and positive") from exc
    if value < 1:
        raise ValueError("Y must be at least 1")
    m = value.numerator // value.denominator
    return 2*m, 2*m+1, 2*m+1-2*value


def unweighted_local_euler_ratios(p: int, omega: int) -> tuple[Fraction, Fraction]:
    """Diagonal cancellation and slice inflation; prime input is caller-owned."""
    _integer(p, "p", 2)
    _integer(omega, "omega", 1)
    if omega >= p:
        raise ValueError("omega must be strictly less than p")
    singular_adjustment = Fraction(p-omega, p)
    diagonal = (1+Fraction(omega, p-omega))*singular_adjustment
    slice_ratio = (
        1+Fraction(omega*(p-1), (p-omega)**2)
    )*singular_adjustment
    return diagonal, slice_ratio


def integer_growth_witnesses(k: int) -> dict[str, bool]:
    _integer(k, "k", 36)
    return {
        "W_log_small": k**3 >= 200*(k+1),
        "distribution_polynomial": 4*(13*k*k+6*k+3) <= k**5,
        "exponential_vs_power": k**5 >= 4*k,
        "row_off_factor": OFF_DIAGONAL_FACTOR == 1_384_128,
        "tail_coarse_factor": 30*OFF_DIAGONAL_FACTOR == 41_523_840,
        "real_scale_domain": k**5 >= 10,
    }


def unweighted_moment_certificate(
    *, k: int, log_outer_half: int | str | Fraction | None = None,
    weight_definition: str = WEIGHT_DEFINITION,
) -> UnweightedMomentCertificate:
    """O(1)-dimension log-scale checks for the filtered actual P91 child.

    The argument log_outer_half is log(X/2), NOT log(2*floor(Y)).
    Structural form, admissibility, B, and source hypotheses are not discovered
    numerically. The source omission is never treated as an automatic identity.
    """
    _integer(k, "k", MIN_K)
    if weight_definition != WEIGHT_DEFINITION:
        raise ValueError("the finite proof requires the explicit Maynard W filter")
    exact_l = exact_dimension_bin(k, k**5 if log_outer_half is None else log_outer_half)
    dps = max(100, len(str(exact_l.numerator))+len(str(exact_l.denominator))+60)
    with mp.workdps(dps):
        kval = mp.mpf(k)
        L = mp.mpf(exact_l.numerator)/exact_l.denominator
        ell = mp.log(kval)
        u = L+mp.log(2)
        logu = mp.log(u)
        loglogu = mp.log(logu)
        logc = -mp.log(153600)-mp.log(mp.log(5))
        log_ratio = logc+logu+mp.log(loglogu)-mp.log(logu)
        y = (L-mp.log(2))/9
        w_upper = 2*kval*kval*mp.log(2*kval*kval)
        lam = (
            w_upper+kval*(kval-1)*mp.log(2)
            +(60*(2*kval*kval-kval+1)+kval)*y
        )
        delta = mp.mpf(10)**123*(6+mp.log(lam))*3000*kval**3*ell**2/y
        off = OFF_DIAGONAL_FACTOR*kval*kval*ell*ell/y
        main = 4*delta+off
        log_dist = (
            2+2*w_upper+2*y-L+kval*mp.log(y)-kval*ell
            +kval*mp.log(2*ell)+mp.mpf(9)/2*kval
            +3*kval*mp.log(1+w_upper+2*y)
        )
        # The tiny distribution error is <= main; avoid computing exp(-L/2).
        log_error = mp.log(2*main)
        log_eta = mp.log(RELATIVE_MAJORANT)+4*mp.log(ell)-2*ell
        log_symmetric = mp.log(2)+log_eta
        target = -mp.log(2*L)/10  # valid lower bound for (log T')^-1/10
        integral = integral_comparison_certificate(k)
        checks = {
            **integer_growth_witnesses(k),
            "exact_outer_dimension_bin": k**5 <= exact_l < (k+1)**5,
            "explicit_filter": weight_definition == WEIGHT_DEFINITION,
            "c_enclosure": -mp.log(307200) < logc < -mp.log(153600),
            "Y_above_2X": log_ratio > mp.log(2),
            "Y_below_X_logX": log_ratio < logu,
            "actual_Tprime_log_upper": u+mp.log(2)+log_ratio <= 2*L,
            "actual_form_coefficients": mp.log(5)+logu <= u,
            "R_lower_at_Tprime": y >= 2*L/30,
            "R_upper_at_Tprime": y <= L/9,
            "narrow_support": y/mp.sqrt(kval) >= mp.log(2),
            "uniform_integral_comparison": integral.gate_passed,
            "lambda_star": lam <= 121*kval*kval*y,
            "smooth_small": delta < mp.mpf(1)/2,
            "smooth_polynomial": delta <= mp.mpf(10)**130*ell**3/kval**2,
            "modulus_capacity": w_upper+2*y <= L/3,
            "W_log_bound": w_upper <= L/100,
            "distribution_exponent": log_dist <= -L/2,
            "distribution_below_main": -L/2 <= mp.log(main),
            "total_relative_majorant": log_error <= log_eta,
            "endpoint_below_eta": mp.log(2)-L <= log_eta,
            "eta_below_one": log_eta < 0,
            "symmetric_relative_target": log_symmetric < target,
            "no_dimension_exponential_loss": ell <= kval**(mp.mpf(1)/8),
        }
        if not all(checks.values()):
            raise AssertionError([key for key, ok in checks.items() if not ok])
        return UnweightedMomentCertificate(
            k=k, log_outer_half_exact=exact_l, working_dps=dps, log_r=y,
            log_y_over_x=log_ratio, smooth_delta_upper=delta,
            log_relative_error_upper=log_error,
            log_relative_majorant=log_eta,
            log_symmetric_relative_majorant=log_symmetric,
            log_relative_target_lower=target,
            log_distribution_ratio_upper=log_dist,
            log_distribution_certificate=-L/2, checks=tuple(checks.items()),
        )
