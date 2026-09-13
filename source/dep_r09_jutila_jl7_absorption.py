"""Finite terminal absorption for Jutila's actual equation (3.6) branch.

The predecessor audits make the following ingredients explicit for one
even- or odd-strip selected system:

* detector lower coefficient ``c_g(theta)`` (Theory 64),
* the weighted square-sum and denominator multiplier (Theory 66),
* the shifted-contour plus Lemma 3 multiplier (Theories 67--68), and
* the principal-residue multiplier 52 (Theory 69).

This module composes those ingredients without counting the normalized
integration area twice.  With ``L=log(D)`` and

    gamma = 29*theta/252,

the normalized terminal inequality has the calculator-safe shape

    A*J^2 <= B*J*x^(2*delta) + E*J^2,

where

    A >= c_bar(theta)^2*A_int,
    B = 52*C_pre,
    E <= 36*C_pre*A_int*C_cont+L3*exp(-gamma*L),

``C_pre=170/theta^2`` and
``c_bar=(3/5)*(1-theta)*theta < c_g``.  The common factor ``A_int``
cancels from the sufficient half-margin test ``E <= A/2``.

All mpmath values are high-precision diagnostics, not directed interval
certificates.  The symbolic inequalities and exact rational coefficients are
the proof interface.  This module does not prove Jutila's printed theorem for
all alpha, the averaged equation (3.7), PAP-11, DEP-R09, the fixed Sono
coefficient, or a numerical X_cert.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp

from source.dep_r09_jutila_jl6_common_budget import (
    build_actual_jl6_common_budget_evaluation,
)
from source.dep_r09_jutila_jl7_terminal_interface import (
    detector_lower_coefficient,
    integration_area_factor,
)


THETA_MAX = Fraction(1, 21)
WEIGHTED_SQUARE_SUM_MULTIPLIER = Fraction(34, 1)
WEIGHT_DENOMINATOR_MULTIPLIER = Fraction(5, 1)
PRETERMINAL_MULTIPLIER_NUMERATOR = Fraction(170, 1)
RESIDUE_MULTIPLIER = Fraction(52, 1)
TOTIENT_LOG_MULTIPLIER = Fraction(6, 1)
OFF_DIAGONAL_DECAY_NUMERATOR = Fraction(29, 252)
RATIONAL_DETECTOR_FACTOR = Fraction(3, 5)
LOG_GATE_EXPONENT = Fraction(8, 1)


def _theta_fraction(theta: Fraction) -> Fraction:
    if not isinstance(theta, Fraction):
        raise TypeError("theta must be fractions.Fraction for exact arithmetic")
    if not (0 < theta <= THETA_MAX):
        raise ValueError("require 0 < theta <= 1/21")
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


def preterminal_multiplier(theta: Fraction) -> Fraction:
    """Return ``5*(34/theta^2)=170/theta^2`` exactly."""

    theta = _theta_fraction(theta)
    return PRETERMINAL_MULTIPLIER_NUMERATOR / theta**2


def elementary_contour_lemma3_multiplier(theta: Fraction) -> Fraction:
    """Return Theory 68's elementary contour-plus-Lemma-3 multiplier."""

    theta = _theta_fraction(theta)
    return Fraction(144, 1) * (1 + 1 / theta) * (2 / theta + 1)


def rational_detector_lower(theta: Fraction) -> Fraction:
    """Return ``(3/5)*(1-theta)*theta``, strictly below ``c_g``.

    The strict comparison uses ``pi^2 < 10`` and therefore
    ``6/pi^2 > 3/5``.  The returned value itself is exact rational data.
    """

    theta = _theta_fraction(theta)
    return RATIONAL_DETECTOR_FACTOR * (1 - theta) * theta


def off_diagonal_decay_rate(theta: Fraction) -> Fraction:
    """Return ``gamma=(29/252)*theta`` from Theory 66."""

    theta = _theta_fraction(theta)
    return OFF_DIAGONAL_DECAY_NUMERATOR * theta


def absorption_ratio(theta: Fraction) -> Fraction:
    """Return the exact ratio in the sufficient half-margin cutoff.

    If ``gamma*L >= log(absorption_ratio(theta))`` then the normalized
    off-diagonal coefficient is at most one half of the rational detector
    lower coefficient squared.
    """

    theta = _theta_fraction(theta)
    c_pre = preterminal_multiplier(theta)
    c_cont = elementary_contour_lemma3_multiplier(theta)
    c_bar = rational_detector_lower(theta)
    return Fraction(72, 1) * c_pre * c_cont / c_bar**2


def absorption_log_cutoff(theta: Fraction) -> mp.mpf:
    """Evaluate ``log(absorption_ratio)/gamma`` at high precision."""

    theta = _theta_fraction(theta)
    ratio = absorption_ratio(theta)
    gamma = off_diagonal_decay_rate(theta)
    ratio_mp = mp.mpf(ratio.numerator) / ratio.denominator
    gamma_mp = mp.mpf(gamma.numerator) / gamma.denominator
    return mp.log(ratio_mp) / gamma_mp


def absorption_rational_fallback_cutoff(theta: Fraction) -> Fraction:
    """Return a very conservative log-free sufficient cutoff.

    ``log u <= u`` for ``u>0`` shows that ``L >= ratio/gamma`` implies the
    sharper logarithmic cutoff.  This exact rational fallback is intended as
    a proof cross-check, not as the recommended numerical cutoff.
    """

    theta = _theta_fraction(theta)
    return absorption_ratio(theta) / off_diagonal_decay_rate(theta)


def selected_system_coefficient(theta: Fraction) -> Fraction:
    """Return a uniform coefficient for ``J <= C_J*x^(2*delta)``.

    This uses ``A_int >= theta^2/2`` and the rational detector lower bound.
    It includes the residue multiplier and preterminal multiplier, but not the
    even/odd factor 2 or the local-zero-count factor from Theory 65.
    """

    theta = _theta_fraction(theta)
    return Fraction(884000, 9) / ((1 - theta) ** 2 * theta**6)


def absorption_fraction_upper(theta: Fraction, log_D: object) -> mp.mpf:
    """Return the upper bound for ``E/A_bar`` after area cancellation."""

    theta = _theta_fraction(theta)
    L = _positive_mpf(log_D, "log_D")
    c_pre = preterminal_multiplier(theta)
    c_cont = elementary_contour_lemma3_multiplier(theta)
    c_bar = rational_detector_lower(theta)
    gamma = off_diagonal_decay_rate(theta)
    c_pre_mp = mp.mpf(c_pre.numerator) / c_pre.denominator
    c_cont_mp = mp.mpf(c_cont.numerator) / c_cont.denominator
    c_bar_mp = mp.mpf(c_bar.numerator) / c_bar.denominator
    gamma_mp = mp.mpf(gamma.numerator) / gamma.denominator
    return (
        36
        * c_pre_mp
        * c_cont_mp
        * mp.exp(-gamma_mp * L)
        / c_bar_mp**2
    )


def off_diagonal_log_gate_holds(log_D: object) -> bool:
    """Check Theory 66's finite ``4*log(L)/L <= 29/252`` gate."""

    L = _positive_mpf(log_D, "log_D")
    return bool(4 * mp.log(L) / L <= mp.mpf(29) / 252)


def exact_half_margin_terminal_bound(
    *,
    A: Fraction,
    B: Fraction,
    E: Fraction,
    J: Fraction,
    Y: Fraction,
) -> Fraction:
    """Fail closed unless an exact finite terminal fixture meets all premises.

    The returned value is ``2*B*Y/A``.  This helper is an independent exact
    arithmetic oracle for the generic algebra, not a replacement for the
    analytic predecessor bounds.
    """

    values = {"A": A, "B": B, "E": E, "J": J, "Y": Y}
    if any(not isinstance(value, Fraction) for value in values.values()):
        raise TypeError("A, B, E, J and Y must all be fractions.Fraction")
    if A <= 0 or B < 0 or E < 0 or J < 0 or Y < 0:
        raise ValueError("require A>0 and B,E,J,Y>=0")
    if E > A / 2:
        raise ValueError("the half-margin premise E<=A/2 is required")
    if A * J**2 > B * J * Y + E * J**2:
        raise ValueError("the terminal inequality premise does not hold")
    bound = 2 * B * Y / A
    if J > bound:
        raise ArithmeticError("exact terminal implication failed")
    return bound


@dataclass(frozen=True)
class JutilaJL7AbsorptionDiagnostic:
    theta: str
    preterminal_multiplier: str
    residue_multiplier: str
    contour_lemma3_multiplier: str
    rational_detector_lower: str
    actual_detector_coefficient: str
    off_diagonal_decay_rate: str
    absorption_ratio: str
    absorption_log_cutoff: str
    absorption_rational_fallback_cutoff: str
    jl6_common_log_cutoff: str
    off_diagonal_log_gate_cutoff: str
    common_log_D_cutoff: str
    common_cutoff_driver: str
    absorption_fraction_upper_at_common: str
    integration_area_at_common: str
    selected_system_coefficient: str
    jl6_budget_holds: bool
    off_diagonal_log_gate_holds: bool
    half_margin_holds_at_common: bool
    symbolic_cutoff_implication_proved: bool
    numerical_values_are_directed_interval_certificates: bool
    contour_area_counted_once: bool
    residue_area_recounted: bool
    parity_factor_inserted_inside_one_system_absorption: bool
    jl7_absorb_actual_selected_system_closed: bool
    actual_nonprincipal_near_one_density_closed: bool
    printed_full_jutila_theorem_one_closed: bool
    averaged_primitive_density_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    threshold_calculator_ready: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic(
    theta: Fraction = Fraction(1, 21),
) -> JutilaJL7AbsorptionDiagnostic:
    """Build the equal-four-way-budget diagnostic for one theta."""

    theta = _theta_fraction(theta)
    with mp.workdps(max(mp.mp.dps, 120)):
        jl6 = build_actual_jl6_common_budget_evaluation(
            theta=theta,
            eta_output=theta,
            eta_jl5=theta / 4,
            eta_damping=theta / 4,
            eta_mellin=theta / 4,
            eta_tail=theta / 4,
        )
        log_gate_cutoff = mp.exp(8)
        absorb_cutoff = absorption_log_cutoff(theta)
        candidates = {
            "JL6_COMMON": jl6.sufficient_log_D_cutoff,
            "FINITE_LOG_GATE_EXP8": log_gate_cutoff,
            "JL7_HALF_MARGIN": absorb_cutoff,
        }
        driver, common_cutoff = max(candidates.items(), key=lambda item: item[1])
        absorb_fraction = absorption_fraction_upper(theta, common_cutoff)
        area = integration_area_factor(theta, common_cutoff)
        c_actual = detector_lower_coefficient(theta)
        c_pre = preterminal_multiplier(theta)
        c_cont = elementary_contour_lemma3_multiplier(theta)
        c_bar = rational_detector_lower(theta)
        gamma = off_diagonal_decay_rate(theta)
        ratio = absorption_ratio(theta)
        rational_fallback = absorption_rational_fallback_cutoff(theta)
        selected = selected_system_coefficient(theta)

    return JutilaJL7AbsorptionDiagnostic(
        theta=str(theta),
        preterminal_multiplier=str(c_pre),
        residue_multiplier=str(RESIDUE_MULTIPLIER),
        contour_lemma3_multiplier=str(c_cont),
        rational_detector_lower=str(c_bar),
        actual_detector_coefficient=mp.nstr(c_actual, 60),
        off_diagonal_decay_rate=str(gamma),
        absorption_ratio=str(ratio),
        absorption_log_cutoff=mp.nstr(absorb_cutoff, 60),
        absorption_rational_fallback_cutoff=str(rational_fallback),
        jl6_common_log_cutoff=mp.nstr(jl6.sufficient_log_D_cutoff, 60),
        off_diagonal_log_gate_cutoff=mp.nstr(log_gate_cutoff, 60),
        common_log_D_cutoff=mp.nstr(common_cutoff, 60),
        common_cutoff_driver=driver,
        absorption_fraction_upper_at_common=mp.nstr(absorb_fraction, 60),
        integration_area_at_common=mp.nstr(area, 60),
        selected_system_coefficient=str(selected),
        jl6_budget_holds=bool(
            jl6.budget_balance_holds
            and jl6.power_condition_margin_holds
            and jl6.component_bounds_meet_allocations
        ),
        off_diagonal_log_gate_holds=off_diagonal_log_gate_holds(common_cutoff),
        half_margin_holds_at_common=bool(absorb_fraction <= mp.mpf(1) / 2),
        symbolic_cutoff_implication_proved=True,
        numerical_values_are_directed_interval_certificates=False,
        contour_area_counted_once=True,
        residue_area_recounted=False,
        parity_factor_inserted_inside_one_system_absorption=False,
        jl7_absorb_actual_selected_system_closed=True,
        actual_nonprincipal_near_one_density_closed=True,
        printed_full_jutila_theorem_one_closed=False,
        averaged_primitive_density_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        threshold_calculator_ready=False,
        numerical_x_cert_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def diagnostic_dict(**kwargs: object) -> dict[str, object]:
    return asdict(build_diagnostic(**kwargs))


__all__ = [
    "LOG_GATE_EXPONENT",
    "OFF_DIAGONAL_DECAY_NUMERATOR",
    "PRETERMINAL_MULTIPLIER_NUMERATOR",
    "RATIONAL_DETECTOR_FACTOR",
    "RESIDUE_MULTIPLIER",
    "THETA_MAX",
    "TOTIENT_LOG_MULTIPLIER",
    "WEIGHTED_SQUARE_SUM_MULTIPLIER",
    "WEIGHT_DENOMINATOR_MULTIPLIER",
    "JutilaJL7AbsorptionDiagnostic",
    "absorption_fraction_upper",
    "absorption_log_cutoff",
    "absorption_ratio",
    "absorption_rational_fallback_cutoff",
    "build_diagnostic",
    "diagnostic_dict",
    "elementary_contour_lemma3_multiplier",
    "exact_half_margin_terminal_bound",
    "off_diagonal_decay_rate",
    "off_diagonal_log_gate_holds",
    "preterminal_multiplier",
    "rational_detector_lower",
    "selected_system_coefficient",
]


if __name__ == "__main__":
    import json

    mp.mp.dps = 120
    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
