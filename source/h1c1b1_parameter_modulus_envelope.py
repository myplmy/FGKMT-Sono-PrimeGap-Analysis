"""Finite parameter and modulus-envelope checks for H1c-1b.1.

This module certifies only elementary parameter identities, the dyadic
one-step dimension repair, and modulus capacity.  It does not evaluate
Bordignon's full error term and it does not prove Maynard Hypothesis 1(2),
Proposition 9.2, or a numerical FGKMT/Sono threshold.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

import mpmath as mp


MINIMUM_SIEVE_DIMENSION = 36
LOG_SAVING_COEFFICIENT = 100
DEFAULT_TRANSPORT_MARGIN = 10
ACTUAL_P92_LOG_POWER = Fraction(0, 1)
GENERAL_AFFINE_LOG_POWER = Fraction(5, 3)


def _validated_dimension(r: int) -> int:
    if isinstance(r, bool) or not isinstance(r, int):
        raise TypeError("r must be an integer")
    if r < 1:
        raise ValueError("r must be positive")
    return r


def _validated_fraction(value: int | Fraction, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an int or Fraction")
    result = Fraction(value)
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def _mp_fraction(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def maynard_log_saving_exponent(r: int) -> int:
    """Return the exponent 100*r^2 printed in Maynard Hypothesis 1."""

    r = _validated_dimension(r)
    return LOG_SAVING_COEFFICIENT * r * r


def bordignon_exponent(
    r: int,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> Fraction:
    """Return the pointwise candidate A(r)=100*r^2+transport_margin."""

    margin = _validated_fraction(transport_margin, "transport_margin")
    return Fraction(maynard_log_saving_exponent(r), 1) + margin


def r_interval_left_log_x(r: int) -> int:
    """Return r^5 for an endpoint-safe r=floor((log T)^(1/5))."""

    r = _validated_dimension(r)
    return r**5


def dyadic_safe_dimension(source_r: int) -> int:
    """Return the one-step-safe dimension for a call at T=x/2.

    If `source_r=floor((log x)^(1/5))`, then `source_r-1` is always
    admissible for the printed Maynard bound at the dyadic endpoint `x/2`
    once `source_r>=2`.  It is a repair candidate, not a claim that the
    published construction already made this replacement.
    """

    source_r = _validated_dimension(source_r)
    if source_r < 2:
        raise ValueError("source_r must be at least 2")
    return source_r - 1


def dyadic_transition_strip_log_width() -> mp.mpf:
    """Return the recurring log-scale width log(2) of the mismatch strip."""

    return mp.log(2)


def exact_dyadic_one_step_repair_certificate(source_r: int = 36) -> bool:
    """Certify the elementary r -> r-1 dyadic admissibility repair.

    Write L=log(x) and T=x/2.  On the source-r bin,
    r^5 <= L < (r+1)^5.  Since log(2)<1 and
    (r-1)^5 <= r^5-1 for r>=2, we get

        (r-1)^5 < log(T) < (r+1)^5.

    Hence floor((log(T))^(1/5)) is either r-1 or r, and r-1 is always
    admissible.  The rational checks below certify the only elementary
    inequalities used in that argument.
    """

    source_r = _validated_dimension(source_r)
    if source_r < 2:
        raise ValueError("source_r must be at least 2")
    exp_one_lower = sum(Fraction(1, factorial(n)) for n in range(3))
    return bool(
        exp_one_lower > 2
        and (source_r - 1) ** 5 <= source_r**5 - 1
        and source_r**5 - (source_r - 1) ** 5 > 1
    )


def exact_source_r_dyadic_capacity_certificate(
    *,
    minimum_source_r: int = MINIMUM_SIEVE_DIMENSION,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
    affine_log_power: int | Fraction = GENERAL_AFFINE_LOG_POWER,
) -> bool:
    """Certify capacity at T=x/2 even when A is indexed by source r.

    This deliberately does *not* certify the printed Theorem-6 dimension
    condition.  It separates two facts: Bordignon's modulus range remains
    ample at the dyadic endpoint, while Maynard's exact k-range needs the
    one-step repair on recurring transition strips.
    """

    minimum_source_r = _validated_dimension(minimum_source_r)
    if minimum_source_r < MINIMUM_SIEVE_DIMENSION:
        raise ValueError(f"minimum_source_r must be at least {MINIMUM_SIEVE_DIMENSION}")
    r = MINIMUM_SIEVE_DIMENSION
    margin = _validated_fraction(transport_margin, "transport_margin")
    beta = _validated_fraction(affine_log_power, "affine_log_power")
    extra = margin + beta

    exp_four_lower = sum(Fraction(4**n, factorial(n)) for n in range(6))
    coarse_left = Fraction((r - 1) ** 5, 1)
    coarse_right = 120 * (
        Fraction(LOG_SAVING_COEFFICIENT * r**2, 1) + extra
    )
    derivative_gate = Fraction((r - 1) ** 5, 1) > 6 * (
        Fraction(LOG_SAVING_COEFFICIENT * r**2, 1) + extra
    )
    return bool(
        exp_four_lower > r
        and coarse_left > coarse_right
        and derivative_gate
        and exact_dyadic_one_step_repair_certificate(r)
    )


def modulus_capacity_log_margin(
    log_t: object,
    r: int,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
    affine_log_power: int | Fraction = ACTUAL_P92_LOG_POWER,
) -> mp.mpf:
    """Return log(Q_B / [t^(1/3)*(log t)^beta]).

    Here Q_B=t^(1/2)/(log t)^A, A=100*r^2+transport_margin,
    beta=affine_log_power, and ``log_t`` is log(t).  A nonnegative result
    certifies the relevant modulus-capacity inequality at that endpoint.
    """

    r = _validated_dimension(r)
    margin = _validated_fraction(transport_margin, "transport_margin")
    beta = _validated_fraction(affine_log_power, "affine_log_power")
    log_t_mpf = mp.mpf(log_t)
    if not mp.isfinite(log_t_mpf) or log_t_mpf <= 1:
        raise ValueError("log_t must be finite and greater than 1")
    exponent = bordignon_exponent(r, margin)
    return (
        log_t_mpf / 6
        - (_mp_fraction(exponent) + _mp_fraction(beta)) * mp.log(log_t_mpf)
    )


def q1_within_q_log_margin(
    log_t: object,
    r: int,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> mp.mpf:
    """Return log(Q_B/Q_1) when Q_1=(log t)^A."""

    r = _validated_dimension(r)
    margin = _validated_fraction(transport_margin, "transport_margin")
    log_t_mpf = mp.mpf(log_t)
    if not mp.isfinite(log_t_mpf) or log_t_mpf <= 1:
        raise ValueError("log_t must be finite and greater than 1")
    exponent = _mp_fraction(bordignon_exponent(r, margin))
    return log_t_mpf / 2 - 2 * exponent * mp.log(log_t_mpf)


def bordignon_capacity_is_increasing(
    log_t: object,
    r: int,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> bool:
    """Check d log(Q_B)/d log(t)>0, equivalently log(t)>2A."""

    r = _validated_dimension(r)
    margin = _validated_fraction(transport_margin, "transport_margin")
    log_t_mpf = mp.mpf(log_t)
    if not mp.isfinite(log_t_mpf) or log_t_mpf <= 1:
        raise ValueError("log_t must be finite and greater than 1")
    return bool(log_t_mpf > 2 * _mp_fraction(bordignon_exponent(r, margin)))


def bordignon_basic_statement_conditions(
    log_t: object,
    r: int,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> bool:
    """Check A>3 and the displayed log-log condition in Theorem 1.4.

    This deliberately excludes the unresolved C(A,A-3,X0/Y0) normalization
    and every term-by-term error absorption.
    """

    r = _validated_dimension(r)
    margin = _validated_fraction(transport_margin, "transport_margin")
    log_t_mpf = mp.mpf(log_t)
    if not mp.isfinite(log_t_mpf) or log_t_mpf <= 1:
        raise ValueError("log_t must be finite and greater than 1")
    exponent = _mp_fraction(bordignon_exponent(r, margin))
    required = max(mp.mpf(7), 11 * mp.log(10) / (2 * exponent))
    return bool(exponent > 3 and mp.log(log_t_mpf) >= required)


def exact_uniform_r_ge_36_certificate(
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
    affine_log_power: int | Fraction = GENERAL_AFFINE_LOG_POWER,
) -> bool:
    """Exact rational certificate for the uniform r>=36 modulus gate.

    The accompanying proof uses:

    * exp(4)>36, certified by a finite positive Taylor partial sum;
    * r^3/log(r) increasing for r>=36;
    * 100+(margin+beta)/r^2 decreasing;
    * the endpoint function L/6-(A+beta)log(L) increasing once
      L>6(A+beta).

    Only the rational base inequalities are evaluated here; the calculus steps
    and their domains are recorded in the proof contract and method document.
    """

    margin = _validated_fraction(transport_margin, "transport_margin")
    beta = _validated_fraction(affine_log_power, "affine_log_power")
    extra = margin + beta
    r = MINIMUM_SIEVE_DIMENSION

    exp_four_lower = sum(Fraction(4**n, factorial(n)) for n in range(6))
    log_upper_base_ratio = Fraction(r**3, 30 * 4)
    required_base_ratio = Fraction(LOG_SAVING_COEFFICIENT, 1) + extra / r**2
    endpoint_derivative_gate = Fraction(r**5, 1) > 6 * (
        Fraction(LOG_SAVING_COEFFICIENT * r**2, 1) + extra
    )

    return bool(
        exp_four_lower > r
        and log_upper_base_ratio > required_base_ratio
        and endpoint_derivative_gate
    )


@dataclass(frozen=True)
class ParameterEnvelopeCertificate:
    outer_chain_k: int
    sieve_dimension_r: int
    maynard_linear_form_count: int
    log_t_left: int
    required_log_saving_exponent: int
    bordignon_a: Fraction
    actual_p92_capacity_margin: mp.mpf
    general_affine_capacity_margin: mp.mpf
    q1_within_q_margin: mp.mpf
    endpoint_dimension_interpretation: str
    capacity_increasing_at_left: bool
    basic_statement_conditions_at_left: bool
    actual_p92_uniform_modulus_gate_closed: bool
    general_scale_affine_modulus_gate_closed: bool
    source_r_dyadic_modulus_capacity_closed: bool
    published_source_r_dyadic_admissibility_closed: bool
    dyadic_one_step_dimension_repair_available: bool
    downstream_repaired_dimension_coefficient_transfer_closed: bool
    pointwise_diagonal_substitution_valid: bool
    full_bordignon_error_composition_closed: bool
    common_exceptional_b_closed: bool
    exact_count_transfer_closed: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_07_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def parameter_envelope_certificate(
    r: int = MINIMUM_SIEVE_DIMENSION,
    *,
    transport_margin: int | Fraction = DEFAULT_TRANSPORT_MARGIN,
) -> ParameterEnvelopeCertificate:
    """Build the fail-closed certificate for an endpoint-safe dimension r."""

    r = _validated_dimension(r)
    if r < MINIMUM_SIEVE_DIMENSION:
        raise ValueError(f"r must be at least {MINIMUM_SIEVE_DIMENSION}")
    margin = _validated_fraction(transport_margin, "transport_margin")
    log_t = r_interval_left_log_x(r)
    return ParameterEnvelopeCertificate(
        outer_chain_k=1,
        sieve_dimension_r=r,
        maynard_linear_form_count=r,
        log_t_left=log_t,
        required_log_saving_exponent=maynard_log_saving_exponent(r),
        bordignon_a=bordignon_exponent(r, margin),
        actual_p92_capacity_margin=modulus_capacity_log_margin(
            log_t,
            r,
            transport_margin=margin,
            affine_log_power=ACTUAL_P92_LOG_POWER,
        ),
        general_affine_capacity_margin=modulus_capacity_log_margin(
            log_t,
            r,
            transport_margin=margin,
            affine_log_power=GENERAL_AFFINE_LOG_POWER,
        ),
        q1_within_q_margin=q1_within_q_log_margin(
            log_t,
            r,
            transport_margin=margin,
        ),
        endpoint_dimension_interpretation=(
            "r=floor((log T)^(1/5)) at the analytic endpoint T"
        ),
        capacity_increasing_at_left=bordignon_capacity_is_increasing(
            log_t,
            r,
            transport_margin=margin,
        ),
        basic_statement_conditions_at_left=bordignon_basic_statement_conditions(
            log_t,
            r,
            transport_margin=margin,
        ),
        actual_p92_uniform_modulus_gate_closed=exact_uniform_r_ge_36_certificate(
            transport_margin=margin,
            affine_log_power=ACTUAL_P92_LOG_POWER,
        ),
        general_scale_affine_modulus_gate_closed=exact_uniform_r_ge_36_certificate(
            transport_margin=margin,
            affine_log_power=GENERAL_AFFINE_LOG_POWER,
        ),
        source_r_dyadic_modulus_capacity_closed=(
            exact_source_r_dyadic_capacity_certificate(
                minimum_source_r=r,
                transport_margin=margin,
                affine_log_power=GENERAL_AFFINE_LOG_POWER,
            )
        ),
        published_source_r_dyadic_admissibility_closed=False,
        dyadic_one_step_dimension_repair_available=(
            exact_dyadic_one_step_repair_certificate(r)
        ),
        downstream_repaired_dimension_coefficient_transfer_closed=False,
        pointwise_diagonal_substitution_valid=True,
        full_bordignon_error_composition_closed=False,
        common_exceptional_b_closed=False,
        exact_count_transfer_closed=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_07_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
