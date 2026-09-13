"""Explicit actual-application tail bound for Jutila Lemma 6.

Jutila (1977), equation (2.11), contains an infinite n-series which is
truncated at x = X*log(qT)^2.  The paper records the discarded tail only as
``O_epsilon(1)``.  This module evaluates the elementary absolute bound proved
in Theory 63 for Jutila's *actual* parameter choice

    D=qT, R=D^epsilon, X=D^(1+12 epsilon).

The printed general Lemma 6 gives no upper envelope for X.  Consequently this
module deliberately does not claim to close that general statement, the
common detector error budget, PAP-11, the fixed Sono coefficient, or X_cert.
mpmath outputs are high-precision diagnostics, not directed intervals.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp


JL6_TAIL_COEFFICIENT_MULTIPLIER = Fraction(2, 1)
JL6_TAIL_SIMPLIFIED_MULTIPLIER = Fraction(4, 1)


@dataclass(frozen=True)
class JutilaJL6TailEvaluation:
    """High-precision diagnostics for the actual Jutila truncation tail."""

    D: mp.mpf
    epsilon: mp.mpf
    absolute_tail_budget: mp.mpf
    log_D: mp.mpf
    R: mp.mpf
    X: mp.mpf
    finite_cut_x: mp.mpf
    actual_exponent_sum: mp.mpf
    endpoint_free_tail_bound: mp.mpf
    simplified_actual_tail_bound: mp.mpf
    sufficient_log_D_cutoff: mp.mpf
    cutoff_holds: bool
    tail_budget_met: bool
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool
    jutila_lemma6_tail_actual_component_closed: bool
    jutila_lemma6_tail_general_statement_closed: bool
    jutila_lemma6_common_error_budget_closed: bool
    jutila_lemma6_closed: bool
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


def jl6_geometric_reciprocal_bound(
    X: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return X+1, an upper bound for 1/(1-exp(-1/X))."""

    X_mpf = _positive_mpf(X, "X")
    return X_mpf + 1


def jl6_endpoint_free_tail_bound(
    *,
    D: int | str | Fraction | mp.mpf,
    R: int | str | Fraction | mp.mpf,
    X: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return 2*R*(X+1)*exp(-log(D)^2).

    This is the endpoint-safe bound obtained after replacing the first omitted
    integer N=floor(x)+1 by x=X*log(D)^2 in the favorable exponential
    direction.  It is valid for D>1, R>0 and X>0.
    """

    D_mpf = _positive_mpf(D, "D")
    R_mpf = _positive_mpf(R, "R")
    X_mpf = _positive_mpf(X, "X")
    if D_mpf <= 1:
        raise ValueError("D must exceed 1")
    L = mp.log(D_mpf)
    return 2 * R_mpf * (X_mpf + 1) * mp.exp(-(L**2))


def jl6_tail_envelope(
    *,
    log_D: int | str | Fraction | mp.mpf,
    r_exponent: int | str | Fraction | mp.mpf,
    x_exponent: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return 4*exp(-L^2+(r+c)L) for R<=D^r and X<=D^c."""

    L = _positive_mpf(log_D, "log_D")
    r = _mpf(r_exponent, "r_exponent")
    c = _mpf(x_exponent, "x_exponent")
    if r < 0 or c < 0:
        raise ValueError("the upper-envelope exponents must be nonnegative")
    return 4 * mp.exp(-(L**2) + (r + c) * L)


def jl6_tail_sufficient_log_cutoff(
    *,
    r_exponent: int | str | Fraction | mp.mpf,
    x_exponent: int | str | Fraction | mp.mpf,
    absolute_tail_budget: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return a sufficient L=log(D) cutoff for the requested tail budget.

    For 0 < tau <= 4, the returned value is

        max(2(r+c), sqrt(2 log(4/tau))).

    At or beyond it, 4*exp(-L^2+(r+c)L) <= tau.
    """

    r = _mpf(r_exponent, "r_exponent")
    c = _mpf(x_exponent, "x_exponent")
    tau = _positive_mpf(absolute_tail_budget, "absolute_tail_budget")
    if r < 0 or c < 0:
        raise ValueError("the upper-envelope exponents must be nonnegative")
    if tau > 4:
        raise ValueError("absolute_tail_budget must not exceed 4")
    return max(2 * (r + c), mp.sqrt(2 * mp.log(4 / tau)))


def build_actual_jl6_tail_evaluation(
    *,
    D: int | str | Fraction | mp.mpf,
    epsilon: int | str | Fraction | mp.mpf,
    absolute_tail_budget: int | str | Fraction | mp.mpf,
) -> JutilaJL6TailEvaluation:
    """Evaluate Theory 63 at Jutila's actual parameter choice."""

    with mp.workdps(max(mp.mp.dps, 100)):
        D_mpf = _positive_mpf(D, "D")
        eps = _positive_mpf(epsilon, "epsilon")
        tau = _positive_mpf(absolute_tail_budget, "absolute_tail_budget")
        if D_mpf <= 1:
            raise ValueError("D=qT must exceed 1")
        if tau > 4:
            raise ValueError("absolute_tail_budget must lie in (0,4]")

        L = mp.log(D_mpf)
        R = D_mpf**eps
        x_exponent = 1 + 12 * eps
        X = D_mpf**x_exponent
        finite_cut_x = X * L**2
        actual_exponent_sum = 1 + 13 * eps
        endpoint_free = jl6_endpoint_free_tail_bound(D=D_mpf, R=R, X=X)
        simplified = jl6_tail_envelope(
            log_D=L,
            r_exponent=eps,
            x_exponent=x_exponent,
        )
        cutoff = jl6_tail_sufficient_log_cutoff(
            r_exponent=eps,
            x_exponent=x_exponent,
            absolute_tail_budget=tau,
        )
        cutoff_holds = bool(L >= cutoff)
        budget_met = bool(simplified <= tau)

    return JutilaJL6TailEvaluation(
        D=D_mpf,
        epsilon=eps,
        absolute_tail_budget=tau,
        log_D=L,
        R=R,
        X=X,
        finite_cut_x=finite_cut_x,
        actual_exponent_sum=actual_exponent_sum,
        endpoint_free_tail_bound=endpoint_free,
        simplified_actual_tail_bound=simplified,
        sufficient_log_D_cutoff=cutoff,
        cutoff_holds=cutoff_holds,
        tail_budget_met=budget_met,
        rigorous_interval_certificate=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
        jutila_lemma6_tail_actual_component_closed=True,
        jutila_lemma6_tail_general_statement_closed=False,
        jutila_lemma6_common_error_budget_closed=False,
        jutila_lemma6_closed=False,
        numerical_x_cert_ready=False,
    )


__all__ = [
    "JL6_TAIL_COEFFICIENT_MULTIPLIER",
    "JL6_TAIL_SIMPLIFIED_MULTIPLIER",
    "JutilaJL6TailEvaluation",
    "build_actual_jl6_tail_evaluation",
    "jl6_endpoint_free_tail_bound",
    "jl6_geometric_reciprocal_bound",
    "jl6_tail_envelope",
    "jl6_tail_sufficient_log_cutoff",
]
