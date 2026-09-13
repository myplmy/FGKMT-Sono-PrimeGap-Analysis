"""Finite algebra for the Gallagher--Maier PAP density-integral split.

The module combines two already separated inputs:

* Theory 71's primitive, nonprincipal, near-one zero-density envelope; and
* Bennett--Martin--O'Bryant--Rechnitzer Theorem 1.1 for a coarse explicit
  total-zero bound away from one.

It does not certify Gallagher's explicit-formula multiplier, the principal
zeta branch, the exceptional-character transfer, the psi-to-pi step, PAP-11,
the fixed Sono coefficient, or X_cert.  Decimal evaluations are
high-precision diagnostics rather than directed interval certificates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp

from source.dep_r09_jutila_jl7_absorption import selected_system_coefficient
from source.dep_r09_jutila_jl7_averaged import (
    THETA_MAX,
    build_diagnostic as build_averaged_diagnostic,
)


BENNETT_ERROR_COEFFICIENT = Fraction(22737, 100000)
BENNETT_ELL_THRESHOLD = Fraction(1567, 1000)
CONSERVATIVE_MCCURLEY_C1 = Fraction(1, 24)
PAP_HEIGHT_POWER = Fraction(5, 1)
FAMILY_SCALE_POWER = Fraction(7, 1)


def _positive_fraction(value: Fraction, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _theta_fraction(theta: Fraction) -> Fraction:
    theta = _positive_fraction(theta, "theta")
    if theta > THETA_MAX:
        raise ValueError("require theta <= 1/21")
    return theta


def _positive_mpf(value: object, name: str) -> mp.mpf:
    try:
        converted = (
            mp.mpf(value.numerator) / value.denominator
            if isinstance(value, Fraction)
            else mp.mpf(value)
        )
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a finite positive real") from exc
    if not mp.isfinite(converted) or converted <= 0:
        raise ValueError(f"{name} must be a finite positive real")
    return converted


def _nonnegative_mpf(value: object, name: str) -> mp.mpf:
    try:
        converted = (
            mp.mpf(value.numerator) / value.denominator
            if isinstance(value, Fraction)
            else mp.mpf(value)
        )
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a finite nonnegative real") from exc
    if not mp.isfinite(converted) or converted < 0:
        raise ValueError(f"{name} must be a finite nonnegative real")
    return converted


def density_power_kappa(theta: Fraction) -> Fraction:
    """Return the X-power numerator 14*(1+12*theta)."""

    theta = _theta_fraction(theta)
    return 14 * (1 + 12 * theta)


def near_kernel_margin(theta: Fraction, d: Fraction) -> Fraction:
    """Return lambda = 1-kappa(theta)/d."""

    theta = _theta_fraction(theta)
    d = _positive_fraction(d, "d")
    margin = 1 - density_power_kappa(theta) / d
    if margin <= 0:
        raise ValueError("require d > 14*(1+12*theta)")
    return margin


def far_power_margin(theta: Fraction, d: Fraction) -> Fraction:
    """Return theta-7/d, the decay exponent of the far-alpha branch."""

    theta = _theta_fraction(theta)
    d = _positive_fraction(d, "d")
    margin = theta - FAMILY_SCALE_POWER / d
    if margin <= 0:
        raise ValueError("require theta*d > 7")
    return margin


def bennett_per_character_upper(q: object, height: object) -> mp.mpf:
    """Evaluate the direct Theorem 1.1 upper bound for one conductor.

    The returned value is zero in the theorem's zero-free small-ell case.
    Otherwise the parity term is bounded in the safe direction by 1/4.
    """

    q_mp = _positive_mpf(q, "q")
    height_mp = _positive_mpf(height, "height")
    if q_mp <= 1:
        raise ValueError("Bennett Theorem 1.1 requires conductor q > 1")
    if height_mp < mp.mpf(5) / 7:
        raise ValueError("Bennett Theorem 1.1 requires height >= 5/7")
    ell = mp.log(q_mp * (height_mp + 2) / (2 * mp.pi))
    if ell <= mp.mpf(BENNETT_ELL_THRESHOLD.numerator) / BENNETT_ELL_THRESHOLD.denominator:
        return mp.mpf(0)
    main = height_mp / mp.pi * mp.log(q_mp * height_mp / (2 * mp.pi * mp.e))
    error = (
        mp.mpf(BENNETT_ERROR_COEFFICIENT.numerator)
        / BENNETT_ERROR_COEFFICIENT.denominator
        * ell
        + 2 * mp.log(1 + ell)
        - mp.mpf("0.5")
    )
    # -chi(-1)/4 <= 1/4.
    return max(mp.mpf(0), main + error + mp.mpf("0.25"))


def bennett_uniform_character_upper(Q: object, height: object) -> mp.mpf:
    """Return a common per-character upper envelope for conductors q<=Q."""

    Q_mp = _positive_mpf(Q, "Q")
    height_mp = _positive_mpf(height, "height")
    if Q_mp < 2:
        raise ValueError("require Q >= 2")
    if height_mp < mp.mpf(5) / 7:
        raise ValueError("require height >= 5/7")
    ell = mp.log(Q_mp * (height_mp + 2) / (2 * mp.pi))
    if ell <= mp.mpf(BENNETT_ELL_THRESHOLD.numerator) / BENNETT_ELL_THRESHOLD.denominator:
        # The source theorem gives N(T, chi)=0 in this regime.  Since ell is
        # monotone in q, the same conclusion holds for every conductor q<=Q.
        return mp.mpf(0)
    main = height_mp / mp.pi * mp.log(Q_mp * height_mp)
    error = (
        mp.mpf(BENNETT_ERROR_COEFFICIENT.numerator)
        / BENNETT_ERROR_COEFFICIENT.denominator
        * ell
        + 2 * mp.log(1 + ell)
        + mp.mpf("0.25")
    )
    return main + error


def bennett_family_zero_upper(Q: object, height: object) -> mp.mpf:
    """Bound the primitive nonprincipal family count by Q^2 times one envelope."""

    Q_mp = _positive_mpf(Q, "Q")
    if Q_mp < 2:
        raise ValueError("require Q >= 2")
    return Q_mp**2 * bennett_uniform_character_upper(Q_mp, height)


def bennett_simple_family_upper(Q: object) -> mp.mpf:
    """Return 2*Q^2*T*log(Q*T) for T=Q^5.

    Theory 72 proves this is a coarse upper bound for the Bennett family
    envelope when Q>=2.
    """

    Q_mp = _positive_mpf(Q, "Q")
    if Q_mp < 2:
        raise ValueError("require Q >= 2")
    height = Q_mp**5
    return 2 * Q_mp**2 * height * mp.log(Q_mp * height)


def exact_far_density_integral(total_zeros: object, X: object, theta: Fraction) -> mp.mpf:
    """Return Z*X^(-theta), including the Stieltjes endpoint term.

    This is exactly

      log(X)*integral_[0,1-theta] X^(alpha-1) Z d alpha + X^(-1) Z.
    """

    zeros = _nonnegative_mpf(total_zeros, "total_zeros")
    X_mp = _positive_mpf(X, "X")
    theta = _theta_fraction(theta)
    if X_mp <= 1:
        raise ValueError("require X > 1")
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    return zeros * X_mp ** (-theta_mp)


def far_simple_pap_envelope(
    log_X: object,
    *,
    theta: Fraction,
    d: Fraction,
) -> mp.mpf:
    """Return (12/d)*log(X)*exp[-(theta-7/d)*log(X)]."""

    u = _positive_mpf(log_X, "log_X")
    margin = far_power_margin(theta, d)
    margin_mp = mp.mpf(margin.numerator) / margin.denominator
    d_mp = mp.mpf(d.numerator) / d.denominator
    return 12 / d_mp * u * mp.exp(-margin_mp * u)


def far_budget_log_cutoff(
    *,
    theta: Fraction,
    d: Fraction,
    budget: Fraction,
) -> mp.mpf:
    """Return an elementary sufficient log(X) cutoff for the far branch."""

    budget = _positive_fraction(budget, "budget")
    margin = far_power_margin(theta, d)
    margin_mp = mp.mpf(margin.numerator) / margin.denominator
    d_mp = mp.mpf(d.numerator) / d.denominator
    budget_mp = mp.mpf(budget.numerator) / budget.denominator
    scale = (12 / d_mp) / (margin_mp * budget_mp)
    return max(
        mp.mpf(1),
        2 / margin_mp * max(mp.mpf(0), mp.log(scale)),
    )


@dataclass(frozen=True)
class NearEnvelope:
    log_X: str
    log_family_scale: str
    zero_free_eta: str
    switch_delta: str
    terminal_theta: str
    kernel_decay_A: str
    selected_system_coefficient: str
    exact_integral_upper: str
    branch_order_holds: bool
    kernel_decay_positive: bool


def near_density_integral_envelope(
    log_X: object,
    *,
    theta: Fraction,
    d: Fraction,
    c1: Fraction,
) -> NearEnvelope:
    """Evaluate the exact piecewise integral of the Theory 71 envelope.

    The formula keeps max(delta,1/L) exactly by splitting at delta=1/L.
    It fails closed unless eta<=1/L<=theta and A>0.
    """

    u = _positive_mpf(log_X, "log_X")
    theta = _theta_fraction(theta)
    d = _positive_fraction(d, "d")
    c1 = _positive_fraction(c1, "c1")
    lam = near_kernel_margin(theta, d)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    d_mp = mp.mpf(d.numerator) / d.denominator
    c1_mp = mp.mpf(c1.numerator) / c1.denominator
    lam_mp = mp.mpf(lam.numerator) / lam.denominator

    L = 7 * u / d_mp
    if L <= 1:
        raise ValueError("require log(D)=7*log(X)/d > 1")
    eta = c1_mp * d_mp / (5 * u)
    switch = 1 / L
    branch_order = bool(eta <= switch <= theta_mp)
    if not branch_order:
        raise ValueError("require eta <= 1/log(D) <= theta")
    A = lam_mp * u - 4 * mp.log(L)
    if A <= 0:
        raise ValueError("require positive Gallagher kernel decay A")

    B = mp.log(2) + L
    coefficient = selected_system_coefficient(theta)
    coefficient_mp = mp.mpf(coefficient.numerator) / coefficient.denominator
    first = (
        (3 + B / L) * mp.exp(-A * eta) / A
        + B * mp.exp(-A * switch) / A**2
    )
    terminal = mp.exp(-A * theta_mp) * (
        (3 + B * theta_mp) / A + B / A**2
    )
    integral_upper = 2 * coefficient_mp * u * (first - terminal)
    if integral_upper <= 0:
        raise ArithmeticError("piecewise near-density integral must be positive")

    return NearEnvelope(
        log_X=mp.nstr(u, 60),
        log_family_scale=mp.nstr(L, 60),
        zero_free_eta=mp.nstr(eta, 60),
        switch_delta=mp.nstr(switch, 60),
        terminal_theta=str(theta),
        kernel_decay_A=mp.nstr(A, 60),
        selected_system_coefficient=str(coefficient),
        exact_integral_upper=mp.nstr(integral_upper, 60),
        branch_order_holds=branch_order,
        kernel_decay_positive=bool(A > 0),
    )


def near_asymptotic_certificate_limit(
    *,
    theta: Fraction,
    d: Fraction,
    c1: Fraction,
) -> mp.mpf:
    """Return the log(X)->infinity limit of the exact near envelope."""

    theta = _theta_fraction(theta)
    d = _positive_fraction(d, "d")
    c1 = _positive_fraction(c1, "c1")
    lam = near_kernel_margin(theta, d)
    coefficient = selected_system_coefficient(theta)
    lam_mp = mp.mpf(lam.numerator) / lam.denominator
    d_mp = mp.mpf(d.numerator) / d.denominator
    c1_mp = mp.mpf(c1.numerator) / c1.denominator
    coefficient_mp = mp.mpf(coefficient.numerator) / coefficient.denominator
    zero_free_scaled = c1_mp * d_mp / 5
    switch_scaled = d_mp / 7
    return 2 * coefficient_mp * (
        4 * mp.exp(-lam_mp * zero_free_scaled) / lam_mp
        + (7 / d_mp)
        * mp.exp(-lam_mp * switch_scaled)
        / lam_mp**2
    )


def first_integer_d_meeting_asymptotic_budget(
    *,
    theta: Fraction,
    c1: Fraction,
    budget: object,
    start: int = 23,
    stop: int = 10000,
) -> int:
    """Scan integer d for the first asymptotic near-envelope budget pass."""

    budget_mp = _positive_mpf(budget, "budget")
    if start < 1 or stop < start:
        raise ValueError("require 1 <= start <= stop")
    for candidate in range(start, stop + 1):
        d = Fraction(candidate, 1)
        try:
            value = near_asymptotic_certificate_limit(
                theta=theta,
                d=d,
                c1=c1,
            )
        except ValueError:
            continue
        if value <= budget_mp:
            return candidate
    raise ValueError("no integer d meeting the budget in the scan range")


@dataclass(frozen=True)
class GallagherMaierSplitDiagnostic:
    theta: str
    d: str
    c1: str
    density_power_kappa: str
    near_kernel_margin: str
    far_power_margin: str
    theory71_log_D_cutoff: str
    induced_log_X_cutoff: str
    near_envelope_at_induced_cutoff: str
    near_asymptotic_certificate_limit: str
    d160_limit_over_one: str
    d160_limit_over_exp_minus_two: str
    first_integer_d_for_limit_le_one: int
    first_integer_d_for_limit_le_exp_minus_two: int
    far_log_X_cutoff_for_one_percent: str
    bennett_global_zero_count_source_fixed: bool
    far_alpha_branch_parameterized_explicit: bool
    near_alpha_integration_parameterized_explicit: bool
    current_d160_certificate_meets_positive_pap_gate: bool
    current_d160_certificate_preserves_sono_exp_minus_two_budget: bool
    gallagher_explicit_formula_multiplier_closed: bool
    principal_zeta_branch_closed: bool
    exceptional_character_branch_closed: bool
    psi_to_pi_closed: bool
    gallagher_maier_pap_bridge_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic(
    *,
    theta: Fraction = Fraction(1, 21),
    d: Fraction = Fraction(160, 1),
    c1: Fraction = CONSERVATIVE_MCCURLEY_C1,
) -> GallagherMaierSplitDiagnostic:
    """Build the source-audit diagnostic at the current conservative endpoint."""

    theta = _theta_fraction(theta)
    d = _positive_fraction(d, "d")
    c1 = _positive_fraction(c1, "c1")
    averaged = build_averaged_diagnostic(theta)
    log_D_cutoff = mp.mpf(averaged.common_log_D_cutoff)
    d_mp = mp.mpf(d.numerator) / d.denominator
    log_X_cutoff = d_mp * log_D_cutoff / 7
    near = near_density_integral_envelope(
        log_X_cutoff,
        theta=theta,
        d=d,
        c1=c1,
    )
    limit = near_asymptotic_certificate_limit(theta=theta, d=d, c1=c1)
    exp_minus_two = mp.exp(-2)

    return GallagherMaierSplitDiagnostic(
        theta=str(theta),
        d=str(d),
        c1=str(c1),
        density_power_kappa=str(density_power_kappa(theta)),
        near_kernel_margin=str(near_kernel_margin(theta, d)),
        far_power_margin=str(far_power_margin(theta, d)),
        theory71_log_D_cutoff=mp.nstr(log_D_cutoff, 60),
        induced_log_X_cutoff=mp.nstr(log_X_cutoff, 60),
        near_envelope_at_induced_cutoff=near.exact_integral_upper,
        near_asymptotic_certificate_limit=mp.nstr(limit, 60),
        d160_limit_over_one=mp.nstr(limit, 60),
        d160_limit_over_exp_minus_two=mp.nstr(limit / exp_minus_two, 60),
        first_integer_d_for_limit_le_one=first_integer_d_meeting_asymptotic_budget(
            theta=theta, c1=c1, budget=1
        ),
        first_integer_d_for_limit_le_exp_minus_two=first_integer_d_meeting_asymptotic_budget(
            theta=theta, c1=c1, budget=exp_minus_two
        ),
        far_log_X_cutoff_for_one_percent=mp.nstr(
            far_budget_log_cutoff(
                theta=theta,
                d=d,
                budget=Fraction(1, 100),
            ),
            60,
        ),
        bennett_global_zero_count_source_fixed=True,
        far_alpha_branch_parameterized_explicit=True,
        near_alpha_integration_parameterized_explicit=True,
        current_d160_certificate_meets_positive_pap_gate=bool(limit < 1),
        current_d160_certificate_preserves_sono_exp_minus_two_budget=bool(
            limit <= exp_minus_two
        ),
        gallagher_explicit_formula_multiplier_closed=False,
        principal_zeta_branch_closed=False,
        exceptional_character_branch_closed=False,
        psi_to_pi_closed=False,
        gallagher_maier_pap_bridge_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        actual_prime_computation_run=False,
        rigorous_interval_certificate=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def diagnostic_dict(**kwargs: object) -> dict[str, object]:
    return asdict(build_diagnostic(**kwargs))


__all__ = [
    "BENNETT_ELL_THRESHOLD",
    "BENNETT_ERROR_COEFFICIENT",
    "CONSERVATIVE_MCCURLEY_C1",
    "FAMILY_SCALE_POWER",
    "GallagherMaierSplitDiagnostic",
    "NearEnvelope",
    "PAP_HEIGHT_POWER",
    "bennett_family_zero_upper",
    "bennett_per_character_upper",
    "bennett_simple_family_upper",
    "bennett_uniform_character_upper",
    "build_diagnostic",
    "density_power_kappa",
    "diagnostic_dict",
    "exact_far_density_integral",
    "far_budget_log_cutoff",
    "far_power_margin",
    "far_simple_pap_envelope",
    "first_integer_d_meeting_asymptotic_budget",
    "near_asymptotic_certificate_limit",
    "near_density_integral_envelope",
    "near_kernel_margin",
]


if __name__ == "__main__":
    import json

    mp.mp.dps = 120
    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
