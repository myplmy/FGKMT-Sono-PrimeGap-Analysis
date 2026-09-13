"""Explicit multiplier for Jutila's shifted-contour term on printed p. 53.

The analytic source statements are Bennett et al. (2021), Lemma 5.6 (5.3),
for primitive nonprincipal Dirichlet L-functions and Hasanalizade--Shen--
Wong (2022), Proposition 3.8, for the principal (Dedekind-zeta) branch.

Only the actual Jutila equation (3.6) range is covered:

    0 < theta <= 1/21, q >= 3, T >= 1,
    0 <= Re(s) <= 2 theta, |Im(s)| <= 2 T,
    Re(w) = -1 + theta, and 0 < M <= N.

The module evaluates the finite constant composition.  It does not certify
Jutila's separate Lemma 3 sum, residue/well-spacing term, terminal density
theorem, PAP-11, DEP-R09, the fixed Sono coefficient, or a numerical X_cert.
Numerical values are high-precision diagnostics, not directed intervals.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp


THETA_MAX = Fraction(1, 21)
NONPRINCIPAL_L_COEFFICIENT_BOUND = Fraction(9, 4)
PRINCIPAL_L_COEFFICIENT_BOUND = Fraction(12, 1)
UNIFORM_L_COEFFICIENT_BOUND = PRINCIPAL_L_COEFFICIENT_BOUND
HEIGHT_COEFFICIENT = Fraction(22, 7)
PRINCIPAL_RATIO_BOUND = Fraction(4, 3)
ELEMENTARY_CONTOUR_FRONT = Fraction(48, 1)


def _theta_fraction(theta: Fraction) -> Fraction:
    if not isinstance(theta, Fraction):
        raise TypeError("theta must be fractions.Fraction for exact scope checks")
    if not (0 < theta <= THETA_MAX):
        raise ValueError("require 0 < theta <= 1/21")
    return theta


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


def _finite_mpf(value: str | int | Fraction | mp.mpf, name: str) -> mp.mpf:
    try:
        converted = (
            mp.mpf(value.numerator) / value.denominator
            if isinstance(value, Fraction)
            else mp.mpf(value)
        )
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a finite real") from exc
    if not mp.isfinite(converted):
        raise ValueError(f"{name} must be a finite real")
    return converted


def imprimitive_euler_correction() -> mp.mpf:
    """Return 4/sqrt(6), the conductor-to-modulus Euler-factor loss."""

    return mp.mpf(4) / mp.sqrt(6)


def nonprincipal_vertical_coefficient() -> mp.mpf:
    """Coefficient before zeta(1+theta)*sqrt(qT)*sqrt(1+|y|).

    The two terms respectively cover a possible base below one in
    Rademacher's power and the actual height envelope.
    """

    return (
        mp.mpf(4) / mp.sqrt(18)
        + mp.mpf(4) / mp.sqrt(6) * mp.sqrt(mp.mpf(11) / (7 * mp.pi))
    )


def principal_vertical_coefficient() -> mp.mpf:
    """Coefficient for the principal-character branch before zeta(1+theta)."""

    return (
        mp.mpf(16)
        / mp.sqrt(6)
        * (1 + mp.sqrt(mp.mpf(11) / (7 * mp.pi)))
    )


def uniform_vertical_multiplier(theta: Fraction) -> mp.mpf:
    """Return 12*zeta(1+theta), valid for both character branches."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    coefficient = (
        mp.mpf(UNIFORM_L_COEFFICIENT_BOUND.numerator)
        / UNIFORM_L_COEFFICIENT_BOUND.denominator
    )
    return coefficient * mp.zeta(1 + theta_mp)


def gamma_integral_multiplier(theta: Fraction) -> mp.mpf:
    """Return 8*sqrt(2)*(2/theta+1) for Re(w)=-1+theta."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    return 8 * mp.sqrt(2) * (2 / theta_mp + 1)


def contour_multiplier(theta: Fraction) -> mp.mpf:
    """Return C_CONT(theta) in the explicit shifted-contour bound."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    return (
        96
        * mp.sqrt(2)
        / mp.pi
        * mp.zeta(1 + theta_mp)
        * (2 / theta_mp + 1)
    )


def elementary_contour_multiplier(theta: Fraction) -> Fraction:
    """Return the rational majorant 48*(1+1/theta)*(2/theta+1)."""

    theta = _theta_fraction(theta)
    return ELEMENTARY_CONTOUR_FRONT * (1 + 1 / theta) * (2 / theta + 1)


def principal_rademacher_ratio(
    *, real_part: str | int | Fraction | mp.mpf, imag_part: str | int | Fraction | mp.mpf
) -> mp.mpf:
    """Evaluate |1+z|/|1-z| on the actual principal branch."""

    sigma = _finite_mpf(real_part, "real_part")
    height = _finite_mpf(imag_part, "imag_part")
    if not (0 < sigma <= mp.mpf(1) / 7):
        raise ValueError("require 0 < real_part <= 1/7")
    return mp.sqrt(((1 + sigma) ** 2 + height**2) / ((1 - sigma) ** 2 + height**2))


def height_envelope(
    *,
    theta: Fraction,
    T: str | int | Fraction | mp.mpf,
    real_offset: str | int | Fraction | mp.mpf,
    base_height: str | int | Fraction | mp.mpf,
    contour_height: str | int | Fraction | mp.mpf,
) -> tuple[mp.mpf, mp.mpf]:
    """Return |1+z| and its 22/7*T*(1+|y|) upper envelope."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    T_mp = _positive_mpf(T, "T")
    u = _finite_mpf(real_offset, "real_offset")
    v = _finite_mpf(base_height, "base_height")
    y = _finite_mpf(contour_height, "contour_height")
    if T_mp < 1:
        raise ValueError("require T >= 1")
    if not (0 <= u <= 2 * theta_mp):
        raise ValueError("require 0 <= real_offset <= 2*theta")
    if abs(v) > 2 * T_mp:
        raise ValueError("require |base_height| <= 2*T")
    sigma = theta_mp + u
    actual = mp.sqrt((1 + sigma) ** 2 + (v + y) ** 2)
    height_coefficient = mp.mpf(HEIGHT_COEFFICIENT.numerator) / HEIGHT_COEFFICIENT.denominator
    upper = height_coefficient * T_mp * (1 + abs(y))
    return actual, upper


def power_difference_diagnostic(
    *,
    theta: Fraction,
    smoothing_M: str | int | Fraction | mp.mpf,
    smoothing_N: str | int | Fraction | mp.mpf,
    divisor_d: str | int | Fraction | mp.mpf,
    contour_height: str | int | Fraction | mp.mpf,
) -> tuple[mp.mpf, mp.mpf]:
    """Evaluate the power difference and its triangle-inequality majorant."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    M = _positive_mpf(smoothing_M, "smoothing_M")
    N = _positive_mpf(smoothing_N, "smoothing_N")
    d = _positive_mpf(divisor_d, "divisor_d")
    y = _finite_mpf(contour_height, "contour_height")
    if N < M:
        raise ValueError("require smoothing_N >= smoothing_M")
    exponent = mp.mpc(-1 + theta_mp, y)
    difference = abs(mp.power(N / d, exponent) - mp.power(M / d, exponent))
    upper = 2 * mp.power(M / d, -1 + theta_mp)
    return difference, upper


@dataclass(frozen=True)
class JutilaJL7ContourDiagnostic:
    theta: str
    nonprincipal_vertical_coefficient: str
    principal_vertical_coefficient: str
    uniform_vertical_multiplier: str
    gamma_integral_multiplier: str
    contour_multiplier: str
    elementary_contour_multiplier: str
    nonprincipal_coefficient_below_nine_fourths: bool
    principal_coefficient_below_twelve: bool
    zeta_integral_majorant_holds_numerically: bool
    contour_below_elementary_majorant: bool
    contour_multiplier_explicit: bool
    jutila_lemma3_multiplier_explicit: bool
    residue_well_spacing_multiplier_explicit: bool
    terminal_density_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    threshold_calculator_ready: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    rigorous_interval_certificate: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic(theta: Fraction = Fraction(1, 21)) -> JutilaJL7ContourDiagnostic:
    """Build a high-precision diagnostic without widening the proof scope."""

    theta = _theta_fraction(theta)
    theta_mp = mp.mpf(theta.numerator) / theta.denominator
    nonprincipal = nonprincipal_vertical_coefficient()
    principal = principal_vertical_coefficient()
    vertical = uniform_vertical_multiplier(theta)
    gamma = gamma_integral_multiplier(theta)
    contour = contour_multiplier(theta)
    elementary = elementary_contour_multiplier(theta)
    elementary_mp = mp.mpf(elementary.numerator) / elementary.denominator
    return JutilaJL7ContourDiagnostic(
        theta=str(theta),
        nonprincipal_vertical_coefficient=mp.nstr(nonprincipal, 50),
        principal_vertical_coefficient=mp.nstr(principal, 50),
        uniform_vertical_multiplier=mp.nstr(vertical, 50),
        gamma_integral_multiplier=mp.nstr(gamma, 50),
        contour_multiplier=mp.nstr(contour, 50),
        elementary_contour_multiplier=str(elementary),
        nonprincipal_coefficient_below_nine_fourths=bool(nonprincipal < mp.mpf(9) / 4),
        principal_coefficient_below_twelve=bool(principal < 12),
        zeta_integral_majorant_holds_numerically=bool(
            mp.zeta(1 + theta_mp) <= 1 + 1 / theta_mp
        ),
        contour_below_elementary_majorant=bool(contour < elementary_mp),
        contour_multiplier_explicit=True,
        jutila_lemma3_multiplier_explicit=False,
        residue_well_spacing_multiplier_explicit=False,
        terminal_density_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        threshold_calculator_ready=False,
        numerical_x_cert_ready=False,
        actual_prime_computation_run=False,
        rigorous_interval_certificate=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def diagnostic_dict(**kwargs: object) -> dict[str, object]:
    return asdict(build_diagnostic(**kwargs))


__all__ = [
    "ELEMENTARY_CONTOUR_FRONT",
    "HEIGHT_COEFFICIENT",
    "JutilaJL7ContourDiagnostic",
    "NONPRINCIPAL_L_COEFFICIENT_BOUND",
    "PRINCIPAL_L_COEFFICIENT_BOUND",
    "PRINCIPAL_RATIO_BOUND",
    "THETA_MAX",
    "UNIFORM_L_COEFFICIENT_BOUND",
    "build_diagnostic",
    "contour_multiplier",
    "diagnostic_dict",
    "elementary_contour_multiplier",
    "gamma_integral_multiplier",
    "height_envelope",
    "imprimitive_euler_correction",
    "nonprincipal_vertical_coefficient",
    "power_difference_diagnostic",
    "principal_rademacher_ratio",
    "principal_vertical_coefficient",
    "uniform_vertical_multiplier",
]


if __name__ == "__main__":
    import json

    mp.mp.dps = 100
    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
