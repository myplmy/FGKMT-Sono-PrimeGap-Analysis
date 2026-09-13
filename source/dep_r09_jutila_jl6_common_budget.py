"""Common finite error budget for Jutila Lemma 6's actual application.

The source identity is Jutila (1977), equation (2.11), after truncation:

    exp(-1/X) * S_q(R) + g(rho, chi) + E_tail = I.

This module evaluates the sufficient log(D) cutoff proved in Theory 64 for
Jutila's actual choices

    D=qT, R=D^theta, z2=D^(1/2+8 theta), X=D^(1+12 theta),

with alpha >= 1-theta and 0 < theta <= 1/21.  Four losses are kept
separate: the explicit JL5 source error, exponential damping, the Mellin
integral, and the truncation tail.

The published analytic inputs are not re-declared as local axioms.  mpmath
values are high-precision diagnostics, not directed interval certificates.
The printed general Lemma 6, JL8, PAP-11, the fixed Sono coefficient, and a
numerical X_cert remain outside this evaluator.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.dep_r09_jutila_jl5_finite import JL5_SOURCE_ERROR_COEFFICIENT
from source.dep_r09_jutila_jl6_mellin import jl6_mellin_constant, jl6_shift_delta


JL6_THETA_MAX = Fraction(1, 21)
JL6_TOTIENT_LOG_MULTIPLIER = Fraction(6, 1)
JL6_B_EXPONENT_MULTIPLIER = Fraction(3, 1)
JL6_B_ABSORPTION_MULTIPLIER = Fraction(18, 1)
JL6_SMALL_Q_MAX_Q_OVER_PHI = Fraction(3, 1)


@dataclass(frozen=True)
class JutilaJL6CommonBudgetEvaluation:
    """High-precision diagnostics for the actual four-part JL6 budget."""

    theta: mp.mpf
    eta_output: mp.mpf
    eta_jl5: mp.mpf
    eta_damping: mp.mpf
    eta_mellin: mp.mpf
    eta_tail: mp.mpf
    eta_sum: mp.mpf
    delta: mp.mpf
    mellin_constant: mp.mpf
    power_condition_exponent_margin: mp.mpf
    base_log_cutoff: mp.mpf
    original_log_condition_cutoff: mp.mpf
    b_factor_absorption_cutoff: mp.mpf
    jl5_relative_cutoff: mp.mpf
    damping_relative_cutoff: mp.mpf
    mellin_relative_cutoff: mp.mpf
    tail_linear_cutoff: mp.mpf
    tail_relative_cutoff: mp.mpf
    sufficient_log_D_cutoff: mp.mpf
    b_factor_exponent_upper_at_cutoff: mp.mpf
    jl5_relative_upper_at_cutoff: mp.mpf
    damping_relative_upper_at_cutoff: mp.mpf
    mellin_relative_upper_at_cutoff: mp.mpf
    tail_relative_upper_at_cutoff: mp.mpf
    total_relative_upper_at_cutoff: mp.mpf
    budget_balance_holds: bool
    power_condition_margin_holds: bool
    component_bounds_meet_allocations: bool
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool
    jutila_lemma6_actual_application_parameterized_explicit: bool
    jutila_lemma6_printed_general_statement_closed: bool
    jutila_lemma8_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool


def _mpf(value: int | str | Fraction | mp.mpf, name: str) -> mp.mpf:
    try:
        converted = (
            mp.mpf(value.numerator) / mp.mpf(value.denominator)
            if isinstance(value, Fraction)
            else mp.mpf(value)
        )
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not mp.isfinite(converted):
        raise ValueError(f"{name} must be a finite real number")
    return converted


def _positive_mpf(value: int | str | Fraction | mp.mpf, name: str) -> mp.mpf:
    converted = _mpf(value, name)
    if converted <= 0:
        raise ValueError(f"{name} must be positive")
    return converted


def jl6_actual_power_margin(
    theta: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return theta*(1-21*theta), the actual (2.8) exponent margin."""

    theta_mpf = _positive_mpf(theta, "theta")
    if theta_mpf > mp.mpf(1) / 21:
        raise ValueError("theta must not exceed 1/21")
    return theta_mpf * (1 - 21 * theta_mpf)


def jl6_b_factor_exponent_bound(
    log_D: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return 3*(log(D)/log(2))^(1/3), an upper exponent for B_q."""

    L = _positive_mpf(log_D, "log_D")
    return 3 * mp.root(L / mp.log(2), 3)


def jl6_b_factor_absorption_cutoff(
    theta: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return a sufficient L cutoff making log(B_q) <= theta*L/6."""

    theta_mpf = _positive_mpf(theta, "theta")
    return mp.power(18 / (theta_mpf * mp.root(mp.log(2), 3)), mp.mpf(3) / 2)


def jl6_uniform_totient_inverse_coefficient_bound(
    log_D: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return pi^2*log(D), the source-backed upper bound for 1/C_phi.

    Theory 64 proves this under q>=3, T>=1, D=qT and log(D)>=e, using
    Rosser--Schoenfeld Theorem 15 for q>=16 and exact q=3,...,15 checks.
    This function evaluates only the resulting coefficient.
    """

    L = _positive_mpf(log_D, "log_D")
    if L < mp.e:
        raise ValueError("log_D must be at least e for the uniform bound")
    return mp.pi**2 * L


def _validate_budget_allocation(
    *,
    eta_output: int | str | Fraction | mp.mpf,
    eta_jl5: int | str | Fraction | mp.mpf,
    eta_damping: int | str | Fraction | mp.mpf,
    eta_mellin: int | str | Fraction | mp.mpf,
    eta_tail: int | str | Fraction | mp.mpf,
) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    output = _positive_mpf(eta_output, "eta_output")
    if output >= 1:
        raise ValueError("eta_output must lie in (0,1)")
    parts = tuple(
        _positive_mpf(value, name)
        for value, name in (
            (eta_jl5, "eta_jl5"),
            (eta_damping, "eta_damping"),
            (eta_mellin, "eta_mellin"),
            (eta_tail, "eta_tail"),
        )
    )
    total = sum(parts, mp.mpf(0))
    if total > output:
        raise ValueError("the four allocated losses must sum to eta_output or less")
    return (output, *parts, total)


def build_actual_jl6_common_budget_evaluation(
    *,
    theta: int | str | Fraction | mp.mpf,
    eta_output: int | str | Fraction | mp.mpf,
    eta_jl5: int | str | Fraction | mp.mpf,
    eta_damping: int | str | Fraction | mp.mpf,
    eta_mellin: int | str | Fraction | mp.mpf,
    eta_tail: int | str | Fraction | mp.mpf,
) -> JutilaJL6CommonBudgetEvaluation:
    """Evaluate the common sufficient L=log(D) cutoff from Theory 64."""

    with mp.workdps(max(mp.mp.dps, 120)):
        theta_mpf = _positive_mpf(theta, "theta")
        if theta_mpf > mp.mpf(1) / 21:
            raise ValueError("theta must lie in (0,1/21]")
        (
            output,
            jl5_budget,
            damping_budget,
            mellin_budget,
            tail_budget,
            total_budget,
        ) = _validate_budget_allocation(
            eta_output=eta_output,
            eta_jl5=eta_jl5,
            eta_damping=eta_damping,
            eta_mellin=eta_mellin,
            eta_tail=eta_tail,
        )
        if output > theta_mpf:
            raise ValueError(
                "eta_output must not exceed theta to recover Jutila's (1-theta) coefficient"
            )

        delta = jl6_shift_delta(theta_mpf)
        mellin_constant = jl6_mellin_constant(delta)
        source_coefficient = (
            mp.mpf(JL5_SOURCE_ERROR_COEFFICIENT.numerator)
            / JL5_SOURCE_ERROR_COEFFICIENT.denominator
        )

        base_cutoff = mp.e
        log_condition_cutoff = theta_mpf ** (-2)
        b_absorption_cutoff = jl6_b_factor_absorption_cutoff(theta_mpf)
        jl5_cutoff = (6 / theta_mpf) * mp.log(
            source_coefficient * mp.pi**2 / (theta_mpf * jl5_budget)
        )
        damping_cutoff = mp.log(1 / damping_budget) / (1 + 12 * theta_mpf)
        mellin_cutoff = (2 / (theta_mpf * (1 + 9 * theta_mpf))) * mp.log(
            mp.pi**2 * mellin_constant / (theta_mpf * mellin_budget)
        )
        tail_linear_cutoff = 2 * (1 + 13 * theta_mpf)
        tail_relative_cutoff = mp.sqrt(
            2 * mp.log(4 * mp.pi**2 / (theta_mpf * tail_budget))
        )
        cutoff = max(
            base_cutoff,
            log_condition_cutoff,
            b_absorption_cutoff,
            jl5_cutoff,
            damping_cutoff,
            mellin_cutoff,
            tail_linear_cutoff,
            tail_relative_cutoff,
        )

        b_exponent = jl6_b_factor_exponent_bound(cutoff)
        jl5_relative = (
            source_coefficient
            * mp.pi**2
            / theta_mpf
            * mp.exp(b_exponent - theta_mpf * cutoff / 3)
        )
        damping_relative = mp.exp(-(1 + 12 * theta_mpf) * cutoff)
        mellin_relative = (
            mp.pi**2
            * mellin_constant
            / theta_mpf
            * mp.exp(-theta_mpf * (1 + 9 * theta_mpf) * cutoff / 2)
        )
        tail_relative = (
            4
            * mp.pi**2
            / theta_mpf
            * mp.exp(-(cutoff**2) + (1 + 13 * theta_mpf) * cutoff)
        )
        total_relative = (
            jl5_relative + damping_relative + mellin_relative + tail_relative
        )
        component_bounds_hold = bool(
            jl5_relative <= jl5_budget
            and damping_relative <= damping_budget
            and mellin_relative <= mellin_budget
            and tail_relative <= tail_budget
        )
        power_margin = jl6_actual_power_margin(theta_mpf)

    return JutilaJL6CommonBudgetEvaluation(
        theta=theta_mpf,
        eta_output=output,
        eta_jl5=jl5_budget,
        eta_damping=damping_budget,
        eta_mellin=mellin_budget,
        eta_tail=tail_budget,
        eta_sum=total_budget,
        delta=delta,
        mellin_constant=mellin_constant,
        power_condition_exponent_margin=power_margin,
        base_log_cutoff=base_cutoff,
        original_log_condition_cutoff=log_condition_cutoff,
        b_factor_absorption_cutoff=b_absorption_cutoff,
        jl5_relative_cutoff=jl5_cutoff,
        damping_relative_cutoff=damping_cutoff,
        mellin_relative_cutoff=mellin_cutoff,
        tail_linear_cutoff=tail_linear_cutoff,
        tail_relative_cutoff=tail_relative_cutoff,
        sufficient_log_D_cutoff=cutoff,
        b_factor_exponent_upper_at_cutoff=b_exponent,
        jl5_relative_upper_at_cutoff=jl5_relative,
        damping_relative_upper_at_cutoff=damping_relative,
        mellin_relative_upper_at_cutoff=mellin_relative,
        tail_relative_upper_at_cutoff=tail_relative,
        total_relative_upper_at_cutoff=total_relative,
        budget_balance_holds=bool(total_budget <= output),
        power_condition_margin_holds=bool(power_margin >= 0),
        component_bounds_meet_allocations=component_bounds_hold,
        rigorous_interval_certificate=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
        jutila_lemma6_actual_application_parameterized_explicit=True,
        jutila_lemma6_printed_general_statement_closed=False,
        jutila_lemma8_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
    )


__all__ = [
    "JL6_B_ABSORPTION_MULTIPLIER",
    "JL6_B_EXPONENT_MULTIPLIER",
    "JL6_SMALL_Q_MAX_Q_OVER_PHI",
    "JL6_THETA_MAX",
    "JL6_TOTIENT_LOG_MULTIPLIER",
    "JutilaJL6CommonBudgetEvaluation",
    "build_actual_jl6_common_budget_evaluation",
    "jl6_actual_power_margin",
    "jl6_b_factor_absorption_cutoff",
    "jl6_b_factor_exponent_bound",
    "jl6_uniform_totient_inverse_coefficient_bound",
]
