"""Theory 47: exact bounded algebra and log-scale proof diagnostics.

This is NOT an X_cert calculator or a prime-data experiment. The structural
assumptions and all-parameter proofs live in the theory document. Diagnostics
do not certify primality, admissibility, source B, or a k-dimensional profile.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1bp92a_identity_prime_moment import exact_dimension_bin

MIN_K = 10**200
WEIGHT_DEFINITION = "maynard_w_filtered"


def _integer(value: int, name: str, minimum: int = 1) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an exact integer >= {minimum}")


def _fraction(value: int | str | Fraction, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError(f"{name} must be exact; floats are not accepted")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a finite rational") from exc


def exceptional_series_factor(k: int, prime: int, *, excluded_by_b: bool = False) -> Fraction:
    """Exact exceptional factor, assuming the supplied integer is prime."""
    _integer(k, "k")
    _integer(prime, "prime", 2)
    if not isinstance(excluded_by_b, bool) or prime <= 2*k*k:
        raise ValueError("require a Boolean exclusion flag and prime > 2*k^2")
    return Fraction(1) if excluded_by_b else Fraction(prime-1, prime-k)


def common_scales(*, k: int, b, series, log_r, log_x, integral_i, integral_j,
                  x, y) -> dict[str, Fraction]:
    """Bounded exact normalization fixture, not the actual huge construction."""
    _integer(k, "k")
    if k > 12:
        raise ValueError("common_scales is toy-only: k<=12")
    vals = {name: _fraction(value, name) for name, value in {
        "b": b, "series": series, "log_r": log_r, "log_x": log_x,
        "integral_i": integral_i, "integral_j": integral_j, "x": x, "y": y,
    }.items()}
    if any(v <= 0 for v in vals.values()) or not Fraction(1, 2) <= vals["b"] <= 1:
        raise ValueError("positive scales and 1/2<=b<=1 are required")
    b, s, r, a, I, J, X, Y = (vals[name] for name in (
        "b", "series", "log_r", "log_x", "integral_i", "integral_j", "x", "y"))
    M = b**(-k)*s*r**k*I
    tau = 2*M*a**k
    u = b*r/a*k*J/(2*I)
    return {"M0": M, "tau": tau, "u": u, "total_mass": tau*Y/a**k,
            "prime_moment": tau*u/k*X/(2*a**k),
            "off_tuple_reference_without_E": tau*X/a**k*Y/a}


def transfer_interval(epsilon, moment_error, *, deleted_relative=0) -> tuple[Fraction, Fraction]:
    """V/(beta*K) in [1-D,1+D] -> original/deleted prime-slice sum over K."""
    e = _fraction(epsilon, "epsilon")
    d = _fraction(moment_error, "moment_error")
    atom = _fraction(deleted_relative, "deleted_relative")
    if e < 0 or not 0 <= d < 1 or atom < 0:
        raise ValueError("require epsilon>=0, 0<=moment_error<1, deleted>=0")
    return max(Fraction(0), (1-d)/(1+e)-atom), (1+e)**2*(1+d)


def probability_relative_error(mass_error, slice_error) -> Fraction:
    d1, d2 = _fraction(mass_error, "mass_error"), _fraction(slice_error, "slice_error")
    if not 0 <= d1 < 1 or d2 < 0:
        raise ValueError("require 0<=mass_error<1 and slice_error>=0")
    return (d1+d2)/(1-d1)


def dyadic_pi_ratio_envelope(log_x, log_two) -> tuple[Fraction, Fraction]:
    """Exact algebra for RS1962; log_two is a toy rational in (0,1)."""
    a, c = _fraction(log_x, "log_x"), _fraction(log_two, "log_two")
    if a < 10 or not 0 < c < 1:
        raise ValueError("require log_x>=10 and 0<log_two<1")
    L = a-c
    return 2+1/a-a/L-3*a/(2*L**2), 2+3/a-a/L


def integer_growth_witnesses(k: int) -> dict[str, bool]:
    _integer(k, "k", MIN_K)
    return {
        "support_Y": k >= 614400**2,
        "eta_absorption": 10**536 <= k**3,
        "additive_prime_error": k**3 >= 14400,
        "M0_positive_base": k**3 > 60*243,
        "pointwise_exponent": 72+864*k*k <= k**5,
        "B0_atom": 4*(6+2*k) <= 3*k**5,
        "conditional_log_target": (3*6**10)**16 < k**3,
        "sqrt_k_at_least_ten": k >= 100,
        "off_tuple_probability": (1+Fraction(1, k))**2 < 4*(1-Fraction(4, k)),
    }


@dataclass(frozen=True)
class CommonNormalizationCertificate:
    k: int
    log_outer_half_exact: Fraction
    log_h_constant_exact: Fraction
    working_dps: int
    p91_relative_upper: mp.mpf
    p92_relative_upper: mp.mpf
    probability_relative_upper: mp.mpf
    log_probability_relative_upper: mp.mpf
    log_target_error: mp.mpf
    log_m0_lower_per_dimension: mp.mpf
    log_weight_upper: mp.mpf
    u_lower_over_log_k: mp.mpf
    u_upper_over_log_k: Fraction
    checks: tuple[tuple[str, bool], ...]
    weight_definition: str = WEIGHT_DEFINITION
    common_filtered_moments_closed: bool = True
    fixed_x_probability_inputs_closed: bool = True
    b0_single_prime_deletion_closed: bool = True
    structural_inputs_assumed_not_computed: bool = True
    u_depends_only_on_k_certified: bool = False
    literal_unfiltered_transfer_certified: bool = False
    general_proposition61_closed: bool = False
    downstream_failure_probability_closed: bool = False
    full_good_sieve_weight_closed: bool = False
    x_cert_ready: bool = False
    actual_prime_experiment_performed: bool = False
    lean_verified: bool = False


def common_normalization_certificate(
    *, k: int, log_outer_half: int | str | Fraction | None = None,
    log_h_constant: int | str | Fraction = 0, weight_definition: str = WEIGHT_DEFINITION,
) -> CommonNormalizationCertificate:
    """O(1)-dimension diagnostics; no exp(L), k**k, W, S, I, J or primes."""
    _integer(k, "k", MIN_K)
    if weight_definition != WEIGHT_DEFINITION:
        raise ValueError("explicit Maynard W-filter construction is required")
    Lq = exact_dimension_bin(k, k**5 if log_outer_half is None else log_outer_half)
    Hq = _fraction(log_h_constant, "log_h_constant")
    if not 0 <= 4*Hq <= Lq:
        raise ValueError("require 0<=log(C_h)<=log(X/2)/4 exactly")
    bits = max(v.bit_length() for v in (Lq.numerator, Lq.denominator,
                                       Hq.numerator, Hq.denominator))
    dps = max(100, bits*30103//100000+80)
    with mp.workdps(dps):
        K = mp.mpf(k)
        L = mp.mpf(Lq.numerator)/Lq.denominator
        a = L+mp.log(2)
        ell = mp.log(K)
        r = (L-mp.log(2))/9
        eta = mp.mpf(10)**134*ell**4/K**2
        t = 1/mp.sqrt(K)
        d1, d2 = 4/K, 2*t
        cond = (d1+d2)/(1-d1)
        log_target = -10*mp.log(mp.log(a))
        lower_M = -mp.mpf(9)/2+mp.log(r)-mp.log(2*K*ell)
        weight_log = 2+2*r+2*K*(mp.log(r)+mp.log(1+r)-ell)
        checks = {
            **integer_growth_witnesses(k),
            "exact_bin": k**5 <= Lq < (k+1)**5,
            "log_power_1_32": ell <= K**(mp.mpf(1)/32),
            "log_a_bound": mp.log(a) < 6*ell,
            "R_lower": r >= K**5/30 and r >= a/30,
            "R_ratio": r/a >= mp.mpf(1)/10,
            "small_exception_factor": mp.log(2)+2*ell <= L,
            "small_pi_error": 3/a <= 1/K,
            "eta_small": eta <= 1/K,
            "P91_transfer": 2*eta*(1+1/K)+1/K <= d1,
            "P92_additive": 14400*K/(L*ell) <= 1/K,
            "P92_transfer_including_atom": t+10/K <= d2,
            "M0_lower": lower_M >= 0,
            "pointwise_weight": weight_log <= L/4,
            "B0_relative_atom": mp.log(160)+2*ell <= 3*a/4,
            "probability_ratio": cond <= 3*t,
            "probability_target": mp.log(3)-ell/2 < log_target,
            "u_lower": (1-mp.log(4)/a)/144 > mp.mpf(1)/160,
        }
        if not all(checks.values()):
            raise AssertionError([name for name, ok in checks.items() if not ok])
        return CommonNormalizationCertificate(
            k=k, log_outer_half_exact=Lq, log_h_constant_exact=Hq, working_dps=dps,
            p91_relative_upper=d1, p92_relative_upper=d2,
            probability_relative_upper=cond,
            log_probability_relative_upper=mp.log(cond), log_target_error=log_target,
            log_m0_lower_per_dimension=lower_M, log_weight_upper=weight_log,
            u_lower_over_log_k=(1-mp.log(4)/a)/144,
            u_upper_over_log_k=Fraction(2, 9),
            checks=tuple((name, bool(ok)) for name, ok in checks.items()),
        )
