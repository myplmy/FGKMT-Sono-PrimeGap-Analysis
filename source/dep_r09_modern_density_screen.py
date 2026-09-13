"""Fail-closed arithmetic for the DEP-R09 modern density-source screen.

The module does not assert any analytic zero-density theorem.  It only
specializes source statements that were checked separately in Theory 74 and
tests whether their *direct nonnegative insertion* into the Gallagher density
integral can meet the current ``d <= 186`` PAP gate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp


D_CAPACITY_ENDPOINT = 186
ZERO_FREE_C1 = Fraction(1, 24)
RAMARE_Q_POWER_AFTER_T_Q5 = 20
RAMARE_ADDITIVE_Q_POWER = 2
RAMARE_MIN_Q = 10
RAMARE_MIN_T = 2000
RAMARE_MIN_SIGMA = Fraction(13, 25)  # 0.52
FI_POWER_EXPONENT = 52_600
FI_SMOOTHED_COEFFICIENT = Fraction(1, 210_000)
FI_LINNIK_EXPONENT = 75_744_000


def _positive_mpf(value: object, name: str) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _valid_d(d: int) -> int:
    if not isinstance(d, int):
        raise TypeError("d must be an integer")
    if d <= RAMARE_Q_POWER_AFTER_T_Q5:
        raise ValueError("d must exceed the transformed Ramare Q exponent 20")
    return d


def ramare_power_margin(d: int = D_CAPACITY_ENDPOINT) -> Fraction:
    """Return ``1 - 20/d`` after setting ``T=Q^5``."""

    d = _valid_d(d)
    return Fraction(d - RAMARE_Q_POWER_AFTER_T_Q5, d)


def ramare_additive_growth_exponent(d: int = D_CAPACITY_ENDPOINT) -> Fraction:
    """Return the residual ``X^(2/d)`` exponent in the additive source term."""

    d = _valid_d(d)
    return Fraction(RAMARE_ADDITIVE_Q_POWER, d)


def pap_zero_free_edge_mass(
    d: int = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> Fraction:
    """Return ``delta * log(X) = c1*d/5`` at ``T=Q^5``."""

    d = _valid_d(d)
    if not isinstance(c1, Fraction):
        raise TypeError("c1 must be an exact Fraction")
    if c1 <= 0:
        raise ValueError("c1 must be positive")
    return c1 * d / 5


def ramare_source_range_log_x(
    d: int = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> mp.mpf:
    """Smallest log(X) forced by the printed Ramare source conditions.

    Conditions checked here are ``Q>=10``, ``T=Q^5>=2000``, and the
    one-unit slice endpoint ``delta=(c1*d/5+1)/log(X) <= 1-0.52``.
    """

    d = _valid_d(d)
    edge_mass = pap_zero_free_edge_mass(d, c1)
    sigma_room = 1 - Fraction(RAMARE_MIN_SIGMA)
    return max(
        mp.mpf(d) * mp.log(RAMARE_MIN_Q),
        mp.mpf(d) * mp.log(RAMARE_MIN_T) / 5,
        (mp.mpf(edge_mass.numerator) / edge_mass.denominator + 1)
        / (mp.mpf(sigma_room.numerator) / sigma_room.denominator),
    )


def ramare_direct_slice_lower(
    log_x: object,
    d: int = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> tuple[mp.mpf, mp.mpf]:
    """Lower bounds for the *computed upper certificate* on one delta slice.

    The slice is ``[eta, eta + 1/log(X)]`` with
    ``eta*log(X)=c1*d/5``.  We integrate the positive right-hand side of
    Ramare's Theorem 1.1 after multiplying by Gallagher's ``X^-delta`` and
    the outer ``log(X)``.  The returned pair is for the main and additive
    source terms.  It is not a lower bound for the true prime-distribution
    error; it only proves that this direct theorem-only certificate is too
    coarse.
    """

    d = _valid_d(d)
    log_x_mp = _positive_mpf(log_x, "log_x")
    minimum = ramare_source_range_log_x(d, c1)
    if log_x_mp < minimum:
        raise ValueError("log_x is outside the checked Ramare source range")

    edge_mass = pap_zero_free_edge_mass(d, c1)
    edge_mp = mp.mpf(edge_mass.numerator) / edge_mass.denominator
    margin = ramare_power_margin(d)
    margin_mp = mp.mpf(margin.numerator) / margin.denominator
    common_log = mp.mpf(7) * log_x_mp / d

    # On the unit-width-in-delta*log(X) slice, 56^delta >= 1 and
    # L^(3+2delta) >= L^3.  The smallest exponential weight is at the
    # right endpoint, delta*log(X)=edge_mass+1.
    main_lower = (
        20
        * common_log**3
        * mp.exp(-margin_mp * (edge_mp + 1))
    )

    # The additive 32*Q^2*L^2 term retains X^(2/d).  The same right-endpoint
    # bound supplies the displayed lower certificate.
    additive_lower = (
        32
        * common_log**2
        * mp.exp(mp.mpf(2) * log_x_mp / d - (edge_mp + 1))
    )
    return main_lower, additive_lower


def fi_linnik_factorization() -> int:
    """Reproduce the exponent multiplication printed after FI Theorem 7.2."""

    return 80 * 18 * FI_POWER_EXPONENT


@dataclass(frozen=True)
class ModernDensityScreenDiagnostic:
    d_capacity_endpoint: int
    zero_free_c1: str
    zero_free_edge_mass: str
    ramare_power_margin: str
    ramare_additive_growth_exponent: str
    ramare_source_min_log_x: str
    ramare_source_min_main_slice_lower: str
    ramare_source_min_additive_slice_lower: str
    ramare_direct_certificate_below_exp_minus_2: bool
    thorner_zaman_near_exponent_99_within_d_gate: bool
    thorner_zaman_exceptional_removed_exponent_170_within_d_gate: bool
    thorner_zaman_all_sigma_exceptional_exponent_198_within_d_gate: bool
    bin_chen_asymptotic_factor_numerical: bool
    friedlander_iwaniec_power_exponent: int
    friedlander_iwaniec_power_within_d_gate: bool
    friedlander_iwaniec_smoothed_coefficient: str
    friedlander_iwaniec_coefficient_above_four_fifths: bool
    friedlander_iwaniec_linnik_exponent: int
    public_numerical_drop_in_found: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> ModernDensityScreenDiagnostic:
    """Build the finite arithmetic screening result at ``d=186``."""

    with mp.workdps(max(mp.mp.dps, 100)):
        minimum = ramare_source_range_log_x()
        main_lower, additive_lower = ramare_direct_slice_lower(minimum)
        edge = pap_zero_free_edge_mass()

    return ModernDensityScreenDiagnostic(
        d_capacity_endpoint=D_CAPACITY_ENDPOINT,
        zero_free_c1=str(ZERO_FREE_C1),
        zero_free_edge_mass=str(edge),
        ramare_power_margin=str(ramare_power_margin()),
        ramare_additive_growth_exponent=str(ramare_additive_growth_exponent()),
        ramare_source_min_log_x=mp.nstr(minimum, 60),
        ramare_source_min_main_slice_lower=mp.nstr(main_lower, 60),
        ramare_source_min_additive_slice_lower=mp.nstr(additive_lower, 60),
        ramare_direct_certificate_below_exp_minus_2=bool(
            main_lower + additive_lower < mp.exp(-2)
        ),
        thorner_zaman_near_exponent_99_within_d_gate=99 <= D_CAPACITY_ENDPOINT,
        thorner_zaman_exceptional_removed_exponent_170_within_d_gate=(
            170 <= D_CAPACITY_ENDPOINT
        ),
        thorner_zaman_all_sigma_exceptional_exponent_198_within_d_gate=(
            198 <= D_CAPACITY_ENDPOINT
        ),
        bin_chen_asymptotic_factor_numerical=False,
        friedlander_iwaniec_power_exponent=FI_POWER_EXPONENT,
        friedlander_iwaniec_power_within_d_gate=(
            FI_POWER_EXPONENT <= D_CAPACITY_ENDPOINT
        ),
        friedlander_iwaniec_smoothed_coefficient=str(FI_SMOOTHED_COEFFICIENT),
        friedlander_iwaniec_coefficient_above_four_fifths=(
            FI_SMOOTHED_COEFFICIENT >= Fraction(4, 5)
        ),
        friedlander_iwaniec_linnik_exponent=fi_linnik_factorization(),
        public_numerical_drop_in_found=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        threshold_calculator_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def diagnostic_dict() -> dict[str, object]:
    return asdict(build_diagnostic())


__all__ = [
    "D_CAPACITY_ENDPOINT",
    "FI_LINNIK_EXPONENT",
    "FI_POWER_EXPONENT",
    "FI_SMOOTHED_COEFFICIENT",
    "RAMARE_ADDITIVE_Q_POWER",
    "RAMARE_Q_POWER_AFTER_T_Q5",
    "ZERO_FREE_C1",
    "ModernDensityScreenDiagnostic",
    "build_diagnostic",
    "diagnostic_dict",
    "fi_linnik_factorization",
    "pap_zero_free_edge_mass",
    "ramare_additive_growth_exponent",
    "ramare_direct_slice_lower",
    "ramare_power_margin",
    "ramare_source_range_log_x",
]


if __name__ == "__main__":
    import json

    mp.mp.dps = 100
    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
