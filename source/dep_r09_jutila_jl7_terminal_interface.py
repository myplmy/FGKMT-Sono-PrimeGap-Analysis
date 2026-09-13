"""Finite algebra for Jutila's Theorem 1 density terminal interface.

This module repairs a parameter-scope error in the earlier Lemma 4 inventory.
The fixed value ``tau=8/5`` belongs to Jutila's Theorem 1-prime argument on
printed page 54.  Equation (3.6), used for Theorem 1 on printed page 52, has

    z1 = D**(1/2 + 7*theta), z2 = D**(1/2 + 8*theta),

so its Barban--Vehov ratio is theta-dependent.  The functions below check the
exact rational specialization, elementary finite corrections, and the
off-diagonal exponent margin.  They do not supply the hidden constants in
Jutila's contour-integral or residue/well-spacing estimates and therefore do
not certify the terminal density theorem, PAP-11, DEP-R09, the fixed Sono
coefficient, or a numerical X_cert.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp


THETA_MAX = Fraction(1, 21)
THEOREM_ONE_PRIME_TAU = Fraction(8, 5)
THEOREM_ONE_PRIME_COEFFICIENT = Fraction(18884947, 500000)
BV_COEFFICIENT_NUMERATOR_BOUND = Fraction(13, 1)
LOG_RATIO_NUMERATOR_BOUND = Fraction(18, 7)
BV_LOG_PRODUCT_NUMERATOR_BOUND = Fraction(34, 1)
WEIGHT_QUOTIENT_BOUND = Fraction(5, 1)
OFF_DIAGONAL_BASE_MARGIN = Fraction(29, 126)
OFF_DIAGONAL_LOG_GATE = Fraction(29, 252)


def _theta_fraction(theta: Fraction) -> Fraction:
    if not isinstance(theta, Fraction):
        raise TypeError("theta must be fractions.Fraction for exact arithmetic")
    if not (0 < theta <= THETA_MAX):
        raise ValueError("require 0 < theta <= 1/21")
    return theta


def theorem_one_density_tau(theta: Fraction) -> Fraction:
    """Return tau_theta=(1+16 theta)/(1+14 theta) exactly."""

    theta = _theta_fraction(theta)
    return (1 + 16 * theta) / (1 + 14 * theta)


def bv_corollary_coefficient(tau: Fraction) -> Fraction:
    """Return the exact Ramaré--Zuniga Corollary 1.3 coefficient."""

    if not isinstance(tau, Fraction):
        raise TypeError("tau must be fractions.Fraction for exact arithmetic")
    if tau <= 1:
        raise ValueError("require tau > 1")
    return (
        Fraction(309, 100)
        * (
            Fraction(1084, 1000) * (tau + 1)
            + Fraction(1301, 1000) * (1 + tau**2)
            - Fraction(116, 1000)
        )
        / (tau - 1)
    )


def theorem_one_density_bv_coefficient(theta: Fraction) -> Fraction:
    """Return the exact coefficient for Jutila equation (3.6)."""

    return bv_corollary_coefficient(theorem_one_density_tau(theta))


def theorem_one_density_bv_coefficient_simplified(theta: Fraction) -> Fraction:
    """Return the same coefficient in its theta-polynomial form."""

    theta = _theta_fraction(theta)
    polynomial = (
        Fraction(2327, 500)
        + Fraction(34421, 250) * theta
        + Fraction(255149, 250) * theta**2
    )
    return Fraction(309, 200) * polynomial / (theta * (1 + 14 * theta))


def off_diagonal_base_exponent(theta: Fraction) -> Fraction:
    """Return the D-exponent before the finite log(D) correction."""

    theta = _theta_fraction(theta)
    return -2 * theta + Fraction(75, 2) * theta**2 - 7 * theta**3


def _positive_mpf(value: str | int | Fraction | mp.mpf, name: str) -> mp.mpf:
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


def theorem_one_density_log_ratio(
    theta: Fraction,
    log_D: str | int | Fraction | mp.mpf,
) -> mp.mpf:
    """Return log(D^(1+12 theta) log(D)^2)/log(z2/z1)."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    L = _positive_mpf(log_D, "log_D")
    return 1 / theta_mp + 12 + 2 * mp.log(L) / (theta_mp * L)


def theorem_one_density_bv_log_product(
    theta: Fraction,
    log_D: str | int | Fraction | mp.mpf,
) -> mp.mpf:
    """Return K_BV(theta) times the exact finite logarithmic ratio."""

    coefficient = theorem_one_density_bv_coefficient(theta)
    coefficient_mp = mp.mpf(coefficient.numerator) / coefficient.denominator
    return coefficient_mp * theorem_one_density_log_ratio(theta, log_D)


def theorem_one_density_safe_bv_log_bound(theta: Fraction) -> Fraction:
    """Return the proved simple upper envelope 34/theta^2."""

    theta = _theta_fraction(theta)
    return BV_LOG_PRODUCT_NUMERATOR_BOUND / theta**2


def weight_denominator_quotient(
    *,
    n: str | int | mp.mpf,
    x: str | int | mp.mpf,
    z1: str | int | mp.mpf,
    smoothing_N: str | int | mp.mpf,
    smoothing_M: str | int | mp.mpf,
) -> mp.mpf:
    """Evaluate exp(-2n/x)/(exp(-n/N)-exp(-n/M)).

    The proof interface requires ``z1 < n <= x``, ``N >= x``, ``M <= z1``,
    and ``x/z1 >= 4``.  Under these conditions the quotient is strictly less
    than 5 by splitting at sqrt(x*z1).
    """

    n_mp = _positive_mpf(n, "n")
    x_mp = _positive_mpf(x, "x")
    z1_mp = _positive_mpf(z1, "z1")
    N_mp = _positive_mpf(smoothing_N, "smoothing_N")
    M_mp = _positive_mpf(smoothing_M, "smoothing_M")
    if not (z1_mp < n_mp <= x_mp):
        raise ValueError("require z1 < n <= x")
    if N_mp < x_mp:
        raise ValueError("require smoothing_N >= x")
    if M_mp > z1_mp:
        raise ValueError("require smoothing_M <= z1")
    if x_mp < 4 * z1_mp:
        raise ValueError("require x/z1 >= 4")
    denominator = mp.exp(-n_mp / N_mp) - mp.exp(-n_mp / M_mp)
    if denominator <= 0:
        raise ArithmeticError("proof-domain denominator must be positive")
    return mp.exp(-2 * n_mp / x_mp) / denominator


def integration_area_factor(
    theta: Fraction,
    log_D: str | int | Fraction | mp.mpf,
) -> mp.mpf:
    """Return the exact normalized xi/eta integration-area factor."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    L = _positive_mpf(log_D, "log_D")
    return (
        theta_mp**2
        * (mp.mpf(1) / 2 + 7 * theta_mp)
        * (1 + 12 * theta_mp + 2 * mp.log(L) / L)
    )


def detector_lower_coefficient(theta: Fraction) -> mp.mpf:
    """Return c_g(theta)=(1-theta)*(6/pi^2)*theta."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    return (1 - theta_mp) * (6 / mp.pi**2) * theta_mp


def normalized_terminal_left_coefficient(
    theta: Fraction,
    log_D: str | int | Fraction | mp.mpf,
) -> mp.mpf:
    """Return c_g(theta)^2 times the normalized integration area."""

    return detector_lower_coefficient(theta) ** 2 * integration_area_factor(theta, log_D)


def off_diagonal_total_exponent(
    theta: Fraction,
    log_D: str | int | Fraction | mp.mpf,
) -> mp.mpf:
    """Return E(theta)+4*theta*log(log D)/log D."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    L = _positive_mpf(log_D, "log_D")
    base = off_diagonal_base_exponent(theta)
    base_mp = mp.mpf(base.numerator) / base.denominator
    return base_mp + 4 * theta_mp * mp.log(L) / L


@dataclass(frozen=True)
class JutilaTerminalDiagnostic:
    theta: str
    log_D: str
    tau_theta: str
    bv_coefficient: str
    theta_times_bv_coefficient: str
    log_ratio: str
    bv_log_product: str
    safe_bv_log_bound: str
    integration_area_factor: str
    normalized_terminal_left_coefficient: str
    off_diagonal_base_exponent: str
    off_diagonal_total_exponent: str
    log_gate_holds: bool
    theta_scope_bound_holds: bool
    off_diagonal_decay_certified_by_gate: bool
    contour_multiplier_explicit: bool
    residue_well_spacing_multiplier_explicit: bool
    terminal_density_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    threshold_calculator_ready: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic(
    *, theta: Fraction = Fraction(1, 100), log_D: str = "100000"
) -> JutilaTerminalDiagnostic:
    """Build a high-precision, non-directed diagnostic for the interface."""

    theta = _theta_fraction(theta)
    L = _positive_mpf(log_D, "log_D")
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    tau = theorem_one_density_tau(theta)
    coefficient = theorem_one_density_bv_coefficient(theta)
    log_ratio = theorem_one_density_log_ratio(theta, L)
    product = theorem_one_density_bv_log_product(theta, L)
    safe_bound = theorem_one_density_safe_bv_log_bound(theta)
    area = integration_area_factor(theta, L)
    left = normalized_terminal_left_coefficient(theta, L)
    base_exponent = off_diagonal_base_exponent(theta)
    total_exponent = off_diagonal_total_exponent(theta, L)
    log_gate_holds = bool(4 * mp.log(L) / L <= mp.mpf(29) / 252)
    decay_target = -(mp.mpf(29) / 252) * theta_mp
    return JutilaTerminalDiagnostic(
        theta=str(theta),
        log_D=mp.nstr(L, 50),
        tau_theta=str(tau),
        bv_coefficient=str(coefficient),
        theta_times_bv_coefficient=mp.nstr(theta_mp * coefficient.numerator / coefficient.denominator, 50),
        log_ratio=mp.nstr(log_ratio, 50),
        bv_log_product=mp.nstr(product, 50),
        safe_bv_log_bound=str(safe_bound),
        integration_area_factor=mp.nstr(area, 50),
        normalized_terminal_left_coefficient=mp.nstr(left, 50),
        off_diagonal_base_exponent=str(base_exponent),
        off_diagonal_total_exponent=mp.nstr(total_exponent, 50),
        log_gate_holds=log_gate_holds,
        theta_scope_bound_holds=bool(theta * coefficient < BV_COEFFICIENT_NUMERATOR_BOUND),
        off_diagonal_decay_certified_by_gate=bool(log_gate_holds and total_exponent <= decay_target),
        contour_multiplier_explicit=False,
        residue_well_spacing_multiplier_explicit=False,
        terminal_density_closed=False,
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
    "BV_COEFFICIENT_NUMERATOR_BOUND",
    "BV_LOG_PRODUCT_NUMERATOR_BOUND",
    "LOG_RATIO_NUMERATOR_BOUND",
    "OFF_DIAGONAL_BASE_MARGIN",
    "OFF_DIAGONAL_LOG_GATE",
    "THEOREM_ONE_PRIME_COEFFICIENT",
    "THEOREM_ONE_PRIME_TAU",
    "THETA_MAX",
    "WEIGHT_QUOTIENT_BOUND",
    "JutilaTerminalDiagnostic",
    "build_diagnostic",
    "bv_corollary_coefficient",
    "detector_lower_coefficient",
    "diagnostic_dict",
    "integration_area_factor",
    "normalized_terminal_left_coefficient",
    "off_diagonal_base_exponent",
    "off_diagonal_total_exponent",
    "theorem_one_density_bv_coefficient",
    "theorem_one_density_bv_coefficient_simplified",
    "theorem_one_density_bv_log_product",
    "theorem_one_density_log_ratio",
    "theorem_one_density_safe_bv_log_bound",
    "theorem_one_density_tau",
    "weight_denominator_quotient",
]


if __name__ == "__main__":
    import json

    mp.mp.dps = 100
    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
