"""Explicit finite constants for the Mellin term in Jutila Lemma 6.

This module evaluates the elementary constant composition documented in
Theory 62.  The analytic inputs are Mellin inversion and Rademacher's
convexity bound in the exact form restated by Bennett et al. (2021).

The evaluator is deliberately fail-closed: it does not certify the separate
truncation tail in Jutila (2.11), Jutila Lemma 6 as a whole, the numerical PAP
package, the fixed Sono coefficient, or a value of X_cert.  Its mpmath values
are high-precision diagnostics rather than directed interval certificates.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp


JL6_M_SUM_MULTIPLIER = Fraction(3, 1)
JL6_IMPRIMITIVE_CORRECTION_SQUARED = Fraction(8, 3)


@dataclass(frozen=True)
class JutilaJL6MellinEvaluation:
    """High-precision evaluation of the parameterized Mellin bound."""

    q: int
    T: mp.mpf
    R: mp.mpf
    z2: mp.mpf
    X: mp.mpf
    alpha: mp.mpf
    beta: mp.mpf
    epsilon: mp.mpf
    delta: mp.mpf
    A: mp.mpf
    imprimitive_correction: mp.mpf
    l_vertical_multiplier: mp.mpf
    gamma_integral_multiplier: mp.mpf
    mellin_constant: mp.mpf
    direct_mellin_bound: mp.mpf
    transferred_power_exponent: mp.mpf
    transferred_mellin_bound: mp.mpf
    original_power_condition_ratio: mp.mpf
    original_power_condition_holds: bool
    transfer_exponent_budget_holds: bool
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool
    jutila_lemma6_mellin_component_closed: bool
    jutila_lemma6_tail_closed: bool
    jutila_lemma6_closed: bool
    numerical_x_cert_ready: bool


def _positive_mpf(value: int | str | Fraction | mp.mpf, name: str) -> mp.mpf:
    try:
        converted = (
            mp.mpf(value.numerator) / mp.mpf(value.denominator)
            if isinstance(value, Fraction)
            else mp.mpf(value)
        )
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a positive finite real number") from exc
    if not mp.isfinite(converted) or converted <= 0:
        raise ValueError(f"{name} must be a positive finite real number")
    return converted


def jl6_shift_delta(epsilon: int | str | Fraction | mp.mpf) -> mp.mpf:
    """Return delta = epsilon / (4(1+epsilon))."""

    eps = _positive_mpf(epsilon, "epsilon")
    return eps / (4 * (1 + eps))


def jl6_imprimitive_correction() -> mp.mpf:
    """Return 4/sqrt(6), the conductor-to-modulus correction."""

    return mp.mpf(4) / mp.sqrt(6)


def jl6_l_vertical_multiplier(delta: int | str | Fraction | mp.mpf) -> mp.mpf:
    """Return sqrt(3/pi)*zeta(1+delta) from the vertical-line L bound."""

    delta_mpf = _positive_mpf(delta, "delta")
    if delta_mpf > mp.mpf(1) / 4:
        raise ValueError("delta must lie in (0, 1/4]")
    return mp.sqrt(mp.mpf(3) / mp.pi) * mp.zeta(1 + delta_mpf)


def jl6_gamma_integral_multiplier(
    delta: int | str | Fraction | mp.mpf,
) -> mp.mpf:
    """Return the elementary upper bound for the weighted Gamma integral."""

    delta_mpf = _positive_mpf(delta, "delta")
    if delta_mpf > mp.mpf(1) / 4:
        raise ValueError("delta must lie in (0, 1/4]")
    return 8 * mp.sqrt(2) * (2 / delta_mpf + 1)


def jl6_mellin_constant(delta: int | str | Fraction | mp.mpf) -> mp.mpf:
    """Return K_M(delta) in |I_delta| <= K_M A X^(-beta+delta)."""

    delta_mpf = _positive_mpf(delta, "delta")
    if delta_mpf > mp.mpf(1) / 4:
        raise ValueError("delta must lie in (0, 1/4]")
    return (
        12
        * mp.sqrt(6)
        / mp.pi ** (mp.mpf(3) / 2)
        * mp.zeta(1 + delta_mpf)
        * (2 / delta_mpf + 1)
    )


def build_jl6_mellin_evaluation(
    *,
    q: int,
    T: int | str | Fraction | mp.mpf,
    R: int | str | Fraction | mp.mpf,
    z2: int | str | Fraction | mp.mpf,
    X: int | str | Fraction | mp.mpf,
    alpha: int | str | Fraction | mp.mpf,
    beta: int | str | Fraction | mp.mpf,
    epsilon: int | str | Fraction | mp.mpf,
) -> JutilaJL6MellinEvaluation:
    """Evaluate the direct and conditionally transferred Mellin bounds.

    Jutila's original power condition is

        X**alpha >= ((q*T)**(1/2) * R * z2)**(1+epsilon).

    Under it, delta=epsilon/(4(1+epsilon)) gives

        |I_delta| <= K_M(delta) * A**(-epsilon/2),

    where A=(q*T)**(1/2)*R*z2.  The returned booleans preserve that this
    high-precision comparison is not a directed interval certificate and that
    the distinct finite truncation tail remains open.
    """

    if isinstance(q, bool) or not isinstance(q, int) or q < 3:
        raise ValueError("q must be an integer at least 3 for a nonprincipal character")

    with mp.workdps(max(mp.mp.dps, 100)):
        T_mpf = _positive_mpf(T, "T")
        R_mpf = _positive_mpf(R, "R")
        z2_mpf = _positive_mpf(z2, "z2")
        X_mpf = _positive_mpf(X, "X")
        alpha_mpf = _positive_mpf(alpha, "alpha")
        beta_mpf = _positive_mpf(beta, "beta")
        eps_mpf = _positive_mpf(epsilon, "epsilon")

        if T_mpf < 1 or R_mpf < 1 or X_mpf < 1 or z2_mpf <= 1:
            raise ValueError("Jutila JL6 requires T,R,X>=1 and z2>1")
        if alpha_mpf < mp.mpf(1) / 2 or alpha_mpf >= 1:
            raise ValueError("alpha must lie in [1/2, 1)")
        if beta_mpf < alpha_mpf or beta_mpf >= 1:
            raise ValueError("beta must lie in [alpha, 1)")

        delta = jl6_shift_delta(eps_mpf)
        A = mp.sqrt(mp.mpf(q) * T_mpf) * R_mpf * z2_mpf
        if A <= 1:
            raise ValueError("A=(q*T)^(1/2)*R*z2 must exceed 1")

        imprimitive = jl6_imprimitive_correction()
        l_multiplier = jl6_l_vertical_multiplier(delta)
        gamma_multiplier = jl6_gamma_integral_multiplier(delta)
        mellin_constant = jl6_mellin_constant(delta)
        direct_bound = mellin_constant * A * X_mpf ** (-beta_mpf + delta)

        power_condition_ratio = X_mpf**alpha_mpf / A ** (1 + eps_mpf)
        power_condition_holds = bool(power_condition_ratio >= 1)
        transferred_exponent = (
            1 - (1 + eps_mpf) * (beta_mpf - delta) / alpha_mpf
        )
        exponent_budget_holds = bool(transferred_exponent <= -eps_mpf / 2)
        transferred_bound = mellin_constant * A ** (-eps_mpf / 2)

    return JutilaJL6MellinEvaluation(
        q=q,
        T=T_mpf,
        R=R_mpf,
        z2=z2_mpf,
        X=X_mpf,
        alpha=alpha_mpf,
        beta=beta_mpf,
        epsilon=eps_mpf,
        delta=delta,
        A=A,
        imprimitive_correction=imprimitive,
        l_vertical_multiplier=l_multiplier,
        gamma_integral_multiplier=gamma_multiplier,
        mellin_constant=mellin_constant,
        direct_mellin_bound=direct_bound,
        transferred_power_exponent=transferred_exponent,
        transferred_mellin_bound=transferred_bound,
        original_power_condition_ratio=power_condition_ratio,
        original_power_condition_holds=power_condition_holds,
        transfer_exponent_budget_holds=exponent_budget_holds,
        rigorous_interval_certificate=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
        jutila_lemma6_mellin_component_closed=True,
        jutila_lemma6_tail_closed=False,
        jutila_lemma6_closed=False,
        numerical_x_cert_ready=False,
    )


def n_over_phi_exact(n: int) -> Fraction:
    """Return n/phi(n) exactly; intended for small finite diagnostics."""

    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    remainder = n
    result = Fraction(1, 1)
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            result *= Fraction(prime, prime - 1)
            while remainder % prime == 0:
                remainder //= prime
        prime += 1
    if remainder > 1:
        result *= Fraction(remainder, remainder - 1)
    return result


__all__ = [
    "JL6_IMPRIMITIVE_CORRECTION_SQUARED",
    "JL6_M_SUM_MULTIPLIER",
    "JutilaJL6MellinEvaluation",
    "build_jl6_mellin_evaluation",
    "jl6_gamma_integral_multiplier",
    "jl6_imprimitive_correction",
    "jl6_l_vertical_multiplier",
    "jl6_mellin_constant",
    "jl6_shift_delta",
    "n_over_phi_exact",
]
