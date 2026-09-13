"""Finite replay of Jutila's variable-modulus equation (3.7).

This module treats the near-one, primitive, nonprincipal branch only.  It
uses a common family scale

    D = Q**2 * T,  L = log(D)

and re-runs the already audited JL5/JL6 detector components at every
conductor ``q_j <= Q``.  The important Mellin quantity

    A_j = (q_j*T)**(1/2) * R * z2

has two different uses:

    D**(1/2 + 9*theta) <= A_j <= D**(1 + 9*theta).

The upper envelope proves Jutila's power condition; the lower envelope
provides common decay.  Reversing either inequality would invalidate the
averaged detector.

For equation (3.7), phase weights of modulus ``q_j/phi(q_j)`` cancel the
detector's ``phi(q_j)/q_j``.  On a principal pair, primitivity forces the
same primitive character and hence the same conductor, so the two residue
totient factors cancel the squared phase weight exactly.  Off-diagonal
phase weights contribute at most ``36*L**2`` and that ``L**2`` cancels the
left detector normalization.  Consequently the strict terminal constants
from Theory 70 are preserved, once the common detector cutoff below holds.

The complex Halasz inequality, Dirichlet-character conductor theorem,
contour shifts, and analytic source bounds are not re-declared as axioms.
The Python calculations are exact rational checks or high-precision
diagnostics, not interval certificates.  The printed all-alpha Theorem 1,
the Gallagher--Maier PAP transfer, the fixed Sono coefficient, and X_cert
remain outside this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp

from source.dep_r09_jutila_jl5_finite import JL5_SOURCE_ERROR_COEFFICIENT
from source.dep_r09_jutila_jl6_common_budget import (
    jl6_actual_power_margin,
    jl6_b_factor_absorption_cutoff,
    jl6_b_factor_exponent_bound,
)
from source.dep_r09_jutila_jl6_mellin import (
    jl6_mellin_constant,
    jl6_shift_delta,
)
from source.dep_r09_jutila_jl7_absorption import (
    absorption_fraction_upper,
    absorption_log_cutoff,
    elementary_contour_lemma3_multiplier,
    off_diagonal_log_gate_holds,
    preterminal_multiplier,
    rational_detector_lower,
    selected_system_coefficient,
)


THETA_MAX = Fraction(1, 21)
PHASE_TOTIENT_LOG_MULTIPLIER = Fraction(6, 1)
PHASE_PAIR_NORMALIZATION = Fraction(36, 1)
RESIDUE_MULTIPLIER = Fraction(52, 1)


def _theta_fraction(theta: Fraction) -> Fraction:
    if not isinstance(theta, Fraction):
        raise TypeError("theta must be fractions.Fraction for exact arithmetic")
    if not (0 < theta <= THETA_MAX):
        raise ValueError("require 0 < theta <= 1/21")
    return theta


def _positive_fraction(value: Fraction, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


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


def detector_phase_normalization(q: Fraction, phi_q: Fraction) -> Fraction:
    """Return ``(q/phi_q)*(phi_q/q)=1`` exactly."""

    q = _positive_fraction(q, "q")
    phi_q = _positive_fraction(phi_q, "phi_q")
    if phi_q > q:
        raise ValueError("require phi_q <= q")
    return (q / phi_q) * (phi_q / q)


def principal_residue_normalization(q: Fraction, phi_q: Fraction) -> Fraction:
    """Return the exact phase/residue/pseudocharacter cancellation.

    The four factors are

        (q/phi_q)^2 * (phi_q/q) * (phi_q/q).

    The first comes from the two phase weights, the second from the
    principal Dirichlet L-function residue, and the third from the diagonal
    pseudocharacter sum.
    """

    q = _positive_fraction(q, "q")
    phi_q = _positive_fraction(phi_q, "phi_q")
    if phi_q > q:
        raise ValueError("require phi_q <= q")
    return (q / phi_q) ** 2 * (phi_q / q) ** 2


def phase_pair_log_normalization(
    *,
    q_j: Fraction,
    phi_j: Fraction,
    q_k: Fraction,
    phi_k: Fraction,
    log_D: Fraction,
) -> Fraction:
    """Return the normalized off-diagonal phase product.

    The call fails closed unless both audited bounds ``q/phi(q) <= 6L``
    hold.  The returned value is at most 36.
    """

    q_j = _positive_fraction(q_j, "q_j")
    phi_j = _positive_fraction(phi_j, "phi_j")
    q_k = _positive_fraction(q_k, "q_k")
    phi_k = _positive_fraction(phi_k, "phi_k")
    log_D = _positive_fraction(log_D, "log_D")
    if phi_j > q_j or phi_k > q_k:
        raise ValueError("require phi_j<=q_j and phi_k<=q_k")
    if q_j / phi_j > PHASE_TOTIENT_LOG_MULTIPLIER * log_D:
        raise ValueError("q_j/phi_j <= 6*log_D is required")
    if q_k / phi_k > PHASE_TOTIENT_LOG_MULTIPLIER * log_D:
        raise ValueError("q_k/phi_k <= 6*log_D is required")
    normalized = (q_j / phi_j) * (q_k / phi_k) / log_D**2
    if normalized > PHASE_PAIR_NORMALIZATION:
        raise ArithmeticError("phase-pair normalization exceeded 36")
    return normalized


def averaged_mellin_decay_exponent(theta: Fraction) -> Fraction:
    """Return ``theta*(1/2+9*theta)/2`` exactly.

    This exponent follows from the *lower* envelope for ``A_j``.  The
    distinct upper envelope is used only for the power condition.
    """

    theta = _theta_fraction(theta)
    return theta * (Fraction(1, 2) + 9 * theta) / 2


def averaged_detector_mellin_cutoff(
    theta: Fraction, eta_mellin: Fraction
) -> mp.mpf:
    """Evaluate the common averaged Mellin relative-error cutoff."""

    theta = _theta_fraction(theta)
    eta_mellin = _positive_fraction(eta_mellin, "eta_mellin")
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    eta_mp = mp.mpf(eta_mellin.numerator) / eta_mellin.denominator
    delta = jl6_shift_delta(theta_mp)
    constant = jl6_mellin_constant(delta)
    decay = averaged_mellin_decay_exponent(theta)
    decay_mp = mp.mpf(decay.numerator) / decay.denominator
    return mp.log(mp.pi**2 * constant / (theta_mp * eta_mp)) / decay_mp


@dataclass(frozen=True)
class AveragedDetectorBudget:
    theta: str
    eta_output: str
    eta_jl5: str
    eta_damping: str
    eta_mellin: str
    eta_tail: str
    base_log_cutoff: str
    original_lower_log_condition_cutoff: str
    b_factor_absorption_cutoff: str
    jl5_relative_cutoff: str
    damping_relative_cutoff: str
    mellin_relative_cutoff: str
    tail_linear_cutoff: str
    tail_relative_cutoff: str
    sufficient_log_D_cutoff: str
    cutoff_driver: str
    power_condition_exponent_margin: str
    mellin_decay_exponent: str
    jl5_relative_upper_at_cutoff: str
    damping_relative_upper_at_cutoff: str
    mellin_relative_upper_at_cutoff: str
    tail_relative_upper_at_cutoff: str
    total_relative_upper_at_cutoff: str
    budget_balance_holds: bool
    power_condition_margin_holds: bool
    component_bounds_meet_allocations: bool


def build_averaged_detector_budget(
    *,
    theta: Fraction,
    eta_output: Fraction,
    eta_jl5: Fraction,
    eta_damping: Fraction,
    eta_mellin: Fraction,
    eta_tail: Fraction,
) -> AveragedDetectorBudget:
    """Build the common detector budget for all primitive ``q_j<=Q``."""

    theta = _theta_fraction(theta)
    allocations = {
        "eta_output": _positive_fraction(eta_output, "eta_output"),
        "eta_jl5": _positive_fraction(eta_jl5, "eta_jl5"),
        "eta_damping": _positive_fraction(eta_damping, "eta_damping"),
        "eta_mellin": _positive_fraction(eta_mellin, "eta_mellin"),
        "eta_tail": _positive_fraction(eta_tail, "eta_tail"),
    }
    if allocations["eta_output"] >= 1:
        raise ValueError("eta_output must lie in (0,1)")
    if allocations["eta_output"] > theta:
        raise ValueError("eta_output must not exceed theta")
    eta_sum = sum(
        (allocations[name] for name in (
            "eta_jl5", "eta_damping", "eta_mellin", "eta_tail"
        )),
        Fraction(0, 1),
    )
    if eta_sum > allocations["eta_output"]:
        raise ValueError("the four allocated losses exceed eta_output")

    with mp.workdps(max(mp.mp.dps, 120)):
        theta_mp = mp.mpf(theta.numerator) / theta.denominator
        eta_jl5_mp = mp.mpf(allocations["eta_jl5"].numerator) / allocations["eta_jl5"].denominator
        eta_damping_mp = mp.mpf(allocations["eta_damping"].numerator) / allocations["eta_damping"].denominator
        eta_mellin_mp = mp.mpf(allocations["eta_mellin"].numerator) / allocations["eta_mellin"].denominator
        eta_tail_mp = mp.mpf(allocations["eta_tail"].numerator) / allocations["eta_tail"].denominator
        source_coefficient = (
            mp.mpf(JL5_SOURCE_ERROR_COEFFICIENT.numerator)
            / JL5_SOURCE_ERROR_COEFFICIENT.denominator
        )
        mellin_constant = jl6_mellin_constant(jl6_shift_delta(theta_mp))
        mellin_decay = averaged_mellin_decay_exponent(theta)
        mellin_decay_mp = mp.mpf(mellin_decay.numerator) / mellin_decay.denominator

        candidates = {
            "BASE_E": mp.e,
            "JL5_LOWER_LOG_R": theta_mp ** (-2),
            "B_Q_ABSORPTION": jl6_b_factor_absorption_cutoff(theta_mp),
            "JL5_RELATIVE": (6 / theta_mp) * mp.log(
                source_coefficient * mp.pi**2 / (theta_mp * eta_jl5_mp)
            ),
            "DAMPING_RELATIVE": mp.log(1 / eta_damping_mp) / (1 + 12 * theta_mp),
            "AVERAGED_MELLIN_RELATIVE": mp.log(
                mp.pi**2 * mellin_constant / (theta_mp * eta_mellin_mp)
            ) / mellin_decay_mp,
            "TAIL_LINEAR": 2 * (1 + 13 * theta_mp),
            "TAIL_RELATIVE": mp.sqrt(
                2 * mp.log(4 * mp.pi**2 / (theta_mp * eta_tail_mp))
            ),
        }
        driver, cutoff = max(candidates.items(), key=lambda item: item[1])

        b_exponent = jl6_b_factor_exponent_bound(cutoff)
        jl5_relative = (
            source_coefficient
            * mp.pi**2
            / theta_mp
            * mp.exp(b_exponent - theta_mp * cutoff / 3)
        )
        damping_relative = mp.exp(-(1 + 12 * theta_mp) * cutoff)
        mellin_relative = (
            mp.pi**2
            * mellin_constant
            / theta_mp
            * mp.exp(-mellin_decay_mp * cutoff)
        )
        tail_relative = (
            4
            * mp.pi**2
            / theta_mp
            * mp.exp(-(cutoff**2) + (1 + 13 * theta_mp) * cutoff)
        )
        total_relative = (
            jl5_relative + damping_relative + mellin_relative + tail_relative
        )
        component_holds = bool(
            jl5_relative <= eta_jl5_mp
            and damping_relative <= eta_damping_mp
            and mellin_relative <= eta_mellin_mp
            and tail_relative <= eta_tail_mp
        )
        power_margin = jl6_actual_power_margin(theta_mp)

    return AveragedDetectorBudget(
        theta=str(theta),
        eta_output=str(allocations["eta_output"]),
        eta_jl5=str(allocations["eta_jl5"]),
        eta_damping=str(allocations["eta_damping"]),
        eta_mellin=str(allocations["eta_mellin"]),
        eta_tail=str(allocations["eta_tail"]),
        base_log_cutoff=mp.nstr(candidates["BASE_E"], 60),
        original_lower_log_condition_cutoff=mp.nstr(candidates["JL5_LOWER_LOG_R"], 60),
        b_factor_absorption_cutoff=mp.nstr(candidates["B_Q_ABSORPTION"], 60),
        jl5_relative_cutoff=mp.nstr(candidates["JL5_RELATIVE"], 60),
        damping_relative_cutoff=mp.nstr(candidates["DAMPING_RELATIVE"], 60),
        mellin_relative_cutoff=mp.nstr(candidates["AVERAGED_MELLIN_RELATIVE"], 60),
        tail_linear_cutoff=mp.nstr(candidates["TAIL_LINEAR"], 60),
        tail_relative_cutoff=mp.nstr(candidates["TAIL_RELATIVE"], 60),
        sufficient_log_D_cutoff=mp.nstr(cutoff, 60),
        cutoff_driver=driver,
        power_condition_exponent_margin=mp.nstr(power_margin, 60),
        mellin_decay_exponent=str(mellin_decay),
        jl5_relative_upper_at_cutoff=mp.nstr(jl5_relative, 60),
        damping_relative_upper_at_cutoff=mp.nstr(damping_relative, 60),
        mellin_relative_upper_at_cutoff=mp.nstr(mellin_relative, 60),
        tail_relative_upper_at_cutoff=mp.nstr(tail_relative, 60),
        total_relative_upper_at_cutoff=mp.nstr(total_relative, 60),
        budget_balance_holds=eta_sum <= allocations["eta_output"],
        power_condition_margin_holds=bool(power_margin >= 0),
        component_bounds_meet_allocations=component_holds,
    )


@dataclass(frozen=True)
class JutilaJL7AveragedDiagnostic:
    theta: str
    family_scale: str
    detector_budget: dict[str, object]
    detector_phase_normalization: str
    principal_residue_normalization: str
    off_diagonal_phase_pair_normalization: str
    preterminal_multiplier: str
    residue_multiplier: str
    contour_lemma3_multiplier: str
    rational_detector_lower: str
    selected_system_coefficient: str
    absorption_log_cutoff: str
    common_log_D_cutoff: str
    common_cutoff_driver: str
    absorption_fraction_upper_at_common: str
    averaged_uniform_detector_closed: bool
    primitive_principal_pair_diagonalized: bool
    averaged_principal_residue_normalization_closed: bool
    averaged_off_diagonal_multiplier_closed: bool
    averaged_selected_system_terminal_closed: bool
    averaged_nonprincipal_near_one_density_closed: bool
    printed_all_alpha_theorem_one_closed: bool
    gallagher_maier_pap_bridge_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic(theta: Fraction = Fraction(1, 21)) -> JutilaJL7AveragedDiagnostic:
    """Build the equal-four-way-budget averaged diagnostic."""

    theta = _theta_fraction(theta)
    quarter = theta / 4
    detector = build_averaged_detector_budget(
        theta=theta,
        eta_output=theta,
        eta_jl5=quarter,
        eta_damping=quarter,
        eta_mellin=quarter,
        eta_tail=quarter,
    )
    with mp.workdps(max(mp.mp.dps, 120)):
        detector_cutoff = mp.mpf(detector.sufficient_log_D_cutoff)
        absorb_cutoff = absorption_log_cutoff(theta)
        log_gate_cutoff = mp.exp(8)
        candidates = {
            "AVERAGED_DETECTOR": detector_cutoff,
            "FINITE_LOG_GATE_EXP8": log_gate_cutoff,
            "JL7_HALF_MARGIN": absorb_cutoff,
        }
        driver, common_cutoff = max(candidates.items(), key=lambda item: item[1])
        absorb_fraction = absorption_fraction_upper(theta, common_cutoff)

    return JutilaJL7AveragedDiagnostic(
        theta=str(theta),
        family_scale="D=Q^2*T, L=log(D), primitive nonprincipal q_j<=Q",
        detector_budget=asdict(detector),
        detector_phase_normalization=str(
            detector_phase_normalization(Fraction(30), Fraction(8))
        ),
        principal_residue_normalization=str(
            principal_residue_normalization(Fraction(30), Fraction(8))
        ),
        off_diagonal_phase_pair_normalization=str(PHASE_PAIR_NORMALIZATION),
        preterminal_multiplier=str(preterminal_multiplier(theta)),
        residue_multiplier=str(RESIDUE_MULTIPLIER),
        contour_lemma3_multiplier=str(
            elementary_contour_lemma3_multiplier(theta)
        ),
        rational_detector_lower=str(rational_detector_lower(theta)),
        selected_system_coefficient=str(selected_system_coefficient(theta)),
        absorption_log_cutoff=mp.nstr(absorb_cutoff, 60),
        common_log_D_cutoff=mp.nstr(common_cutoff, 60),
        common_cutoff_driver=driver,
        absorption_fraction_upper_at_common=mp.nstr(absorb_fraction, 60),
        averaged_uniform_detector_closed=True,
        primitive_principal_pair_diagonalized=True,
        averaged_principal_residue_normalization_closed=True,
        averaged_off_diagonal_multiplier_closed=True,
        averaged_selected_system_terminal_closed=True,
        averaged_nonprincipal_near_one_density_closed=True,
        printed_all_alpha_theorem_one_closed=False,
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


__all__ = [
    "AveragedDetectorBudget",
    "JutilaJL7AveragedDiagnostic",
    "PHASE_PAIR_NORMALIZATION",
    "PHASE_TOTIENT_LOG_MULTIPLIER",
    "RESIDUE_MULTIPLIER",
    "THETA_MAX",
    "averaged_detector_mellin_cutoff",
    "averaged_mellin_decay_exponent",
    "build_averaged_detector_budget",
    "build_diagnostic",
    "detector_phase_normalization",
    "phase_pair_log_normalization",
    "principal_residue_normalization",
]
