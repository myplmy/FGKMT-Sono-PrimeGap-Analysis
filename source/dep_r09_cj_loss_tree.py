"""Source-preserving audit of the Jutila terminal coefficient ``C_J``.

Theory 72 uses

    C_J(theta) = 884000 / (9*(1-theta)^2*theta^6).

This module exposes the exact factors that produced that coefficient and a
strictly narrower, endpoint-specific upper coefficient obtained without
changing the analytic source theorems:

* keep the exact Ramaré--Zuniga Alterman Corollary 1.3 coefficient;
* replace the denominator bound 5 by the proved uniform bound 8/5;
* preserve the exact integration-area lower at theta=1/21;
* reuse the pre-rationalized detector lower 4/147;
* retain ``40/19`` in the Gamma row and exploit q<=Q at the averaged scale;
* request an absorption remainder at most A/10^6 rather than merely A/2.

The resulting number is still only a sufficient upper coefficient for the
same primitive nonprincipal near-one branch.  It is not a lower bound for all
possible proofs and it does not certify PAP-11, the fixed Sono coefficient, or
``X_cert``.  Decimal values are high-precision diagnostics, not directed
interval certificates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp


THETA_ENDPOINT = Fraction(1, 21)
D_CAPACITY_ENDPOINT = Fraction(186, 1)
ZERO_FREE_C1 = Fraction(1, 24)
PAP_NEAR_BUDGET_EXPONENT = Fraction(2, 1)
ABSORPTION_DENOMINATOR = 1_000_000

BASELINE_RESIDUE = Fraction(52, 1)
BASELINE_DENOMINATOR = Fraction(5, 1)
BASELINE_WEIGHT_NUMERATOR = Fraction(34, 1)
BASELINE_MARGIN = Fraction(2, 1)

TIGHT_DENOMINATOR = Fraction(8, 5)
TIGHT_RESIDUE_ENDPOINT = Fraction(710, 171)
TIGHT_LOG_RATIO_ENDPOINT = Fraction(34, 1)
RATIONAL_DETECTOR_ENDPOINT = Fraction(4, 147)
EXACT_AREA_ENDPOINT = Fraction(55, 18522)


def _theta_fraction(theta: Fraction) -> Fraction:
    if not isinstance(theta, Fraction):
        raise TypeError("theta must be fractions.Fraction")
    if not (0 < theta <= THETA_ENDPOINT):
        raise ValueError("require 0 < theta <= 1/21")
    return theta


def _positive_fraction(value: Fraction, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _mpf(value: Fraction | int | str | mp.mpf) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def baseline_selected_system_coefficient(theta: Fraction) -> Fraction:
    """Return Theory 70's exact half-margin coefficient."""

    theta = _theta_fraction(theta)
    return Fraction(884000, 9) / ((1 - theta) ** 2 * theta**6)


def baseline_factor_product(theta: Fraction) -> Fraction:
    """Rebuild ``C_J`` from its six displayed loss factors."""

    theta = _theta_fraction(theta)
    detector = Fraction(3, 5) * (1 - theta) * theta
    area = theta**2 / 2
    weighted = BASELINE_WEIGHT_NUMERATOR / theta**2
    return (
        BASELINE_MARGIN
        * BASELINE_RESIDUE
        * BASELINE_DENOMINATOR
        * weighted
        / detector**2
        / area
    )


def rz_barban_vehov_coefficient(theta: Fraction) -> Fraction:
    """Exact rational specialization of Corollary 1.3 used in Theory 66."""

    theta = _theta_fraction(theta)
    polynomial = (
        Fraction(2327, 500)
        + Fraction(34421, 250) * theta
        + Fraction(255149, 250) * theta**2
    )
    return Fraction(309, 200) * polynomial / (theta * (1 + 14 * theta))


def endpoint_weighted_square_upper() -> Fraction:
    """Finite-safe weighted coefficient for theta=1/21 and log(D)>=441.

    The exact source coefficient is multiplied by the proved finite ratio
    ``log(x)/log(z2/z1) <= 34``.  This deliberately does not use its smaller
    asymptotic limit 33.
    """

    return rz_barban_vehov_coefficient(THETA_ENDPOINT) * TIGHT_LOG_RATIO_ENDPOINT


def endpoint_preterminal_upper() -> Fraction:
    """Return the tightened denominator times weighted-square coefficient."""

    return TIGHT_DENOMINATOR * endpoint_weighted_square_upper()


def endpoint_residue_row_upper() -> Fraction:
    """Retain the Gamma bound 40/19 in Theory 69's diagonal and row terms."""

    theta = THETA_ENDPOINT
    return Fraction(280, 19) * theta**2 + Fraction(2800, 57) * theta


def endpoint_residue_upper() -> Fraction:
    """Averaged-scale residue upper using q<=Q and log(D)=log(Q^2*T)."""

    return Fraction(7, 4) * endpoint_residue_row_upper()


def absorption_margin_factor(m: int = ABSORPTION_DENOMINATOR) -> Fraction:
    """Return m/(m-1) when the absorbed error is at most A/m."""

    if not isinstance(m, int):
        raise TypeError("m must be an integer")
    if m <= 1:
        raise ValueError("m must exceed 1")
    return Fraction(m, m - 1)


def tightened_selected_system_coefficient(
    m: int = ABSORPTION_DENOMINATOR,
) -> Fraction:
    """Return the finite-safe endpoint coefficient after local tightening."""

    return (
        absorption_margin_factor(m)
        * endpoint_residue_upper()
        * endpoint_preterminal_upper()
        / RATIONAL_DETECTOR_ENDPOINT**2
        / EXACT_AREA_ENDPOINT
    )


def tightened_absorption_log_cutoff(
    m: int = ABSORPTION_DENOMINATOR,
) -> mp.mpf:
    """Sufficient log(D) cutoff for ``E<=A/m`` with tightened C_pre.

    The contour-plus-Lemma-3 coefficient remains 136224.  It changes this
    cutoff but not the selected-system coefficient once the error is absorbed.
    """

    absorption_margin_factor(m)  # fail closed on nonintegral or nonpositive slack
    c_contour_lemma3 = Fraction(136224, 1)
    gamma = Fraction(29, 5292)
    ratio = (
        Fraction(36 * m, 1)
        * endpoint_preterminal_upper()
        * c_contour_lemma3
        / RATIONAL_DETECTOR_ENDPOINT**2
    )
    return mp.log(_mpf(ratio)) / _mpf(gamma)


def weight_denominator_quotient(rho: object, t: object) -> mp.mpf:
    """Evaluate the extremal quotient after setting N=x and M=z1.

    Here ``rho=x/z1>=4`` and ``t=n/x`` lies in ``[1/rho,1]``.  The proof in
    Theory 73 shows this quotient decreases in t and its supremum over rho is
    ``e/(e-1)<8/5``.
    """

    rho_mp = mp.mpf(rho)
    t_mp = mp.mpf(t)
    if not mp.isfinite(rho_mp) or rho_mp < 4:
        raise ValueError("require finite rho>=4")
    if not mp.isfinite(t_mp) or not (1 / rho_mp <= t_mp <= 1):
        raise ValueError("require 1/rho<=t<=1")
    return mp.exp(-t_mp) / (1 - mp.exp(-(rho_mp - 1) * t_mp))


def weight_denominator_rho_supremum(rho: object) -> mp.mpf:
    """Return the fixed-rho endpoint supremum at t=1/rho."""

    rho_mp = mp.mpf(rho)
    if not mp.isfinite(rho_mp) or rho_mp < 4:
        raise ValueError("require finite rho>=4")
    return weight_denominator_quotient(rho_mp, 1 / rho_mp)


def near_kernel_per_cj(
    *,
    theta: Fraction = THETA_ENDPOINT,
    d: Fraction = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> mp.mpf:
    """Return the asymptotic Theory 72 near envelope per unit C_J."""

    theta = _theta_fraction(theta)
    d = _positive_fraction(d, "d")
    c1 = _positive_fraction(c1, "c1")
    lam = 1 - Fraction(14, 1) * (1 + 12 * theta) / d
    if lam <= 0:
        raise ValueError("require positive near-kernel margin")
    lam_mp = _mpf(lam)
    d_mp = _mpf(d)
    c1_mp = _mpf(c1)
    return 2 * (
        4 * mp.exp(-lam_mp * c1_mp * d_mp / 5) / lam_mp
        + (7 / d_mp) * mp.exp(-lam_mp * d_mp / 7) / lam_mp**2
    )


def pap_cj_budget_cap(
    *,
    budget_exponent: Fraction = PAP_NEAR_BUDGET_EXPONENT,
    theta: Fraction = THETA_ENDPOINT,
    d: Fraction = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> mp.mpf:
    """Largest C_J allowed by the selected ``exp(-budget_exponent)`` gate."""

    budget_exponent = _positive_fraction(budget_exponent, "budget_exponent")
    return mp.exp(-_mpf(budget_exponent)) / near_kernel_per_cj(
        theta=theta, d=d, c1=c1
    )


def counterfactual_theta_power_coefficient(theta: Fraction) -> Fraction:
    """Return theta^-6 as a labelled scaling diagnostic, not a theorem floor."""

    theta = _theta_fraction(theta)
    return theta**-6


@dataclass(frozen=True)
class CJLossTreeDiagnostic:
    theta: str
    d_capacity_endpoint: str
    zero_free_c1: str
    baseline_selected_system_coefficient: str
    baseline_factorization_matches: bool
    rz_endpoint_coefficient: str
    weighted_square_endpoint_upper: str
    denominator_endpoint_upper: str
    residue_row_endpoint_upper: str
    residue_endpoint_upper: str
    detector_endpoint_lower: str
    area_endpoint_lower: str
    absorption_denominator: int
    absorption_margin_factor: str
    tightened_selected_system_coefficient: str
    tightened_absorption_log_cutoff: str
    coefficient_improvement_factor: str
    pap_cj_budget_cap_exp_minus_2: str
    baseline_near_limit: str
    tightened_near_limit: str
    baseline_over_budget: str
    tightened_over_budget: str
    counterfactual_theta_power_coefficient: str
    counterfactual_over_budget: str
    contour_lemma3_changes_asymptotic_cj: bool
    local_tightening_passes_pap_gate: bool
    counterfactual_scaling_is_impossibility_theorem: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> CJLossTreeDiagnostic:
    """Build the endpoint loss-tree and PAP-budget diagnostic."""

    with mp.workdps(max(mp.mp.dps, 120)):
        baseline = baseline_selected_system_coefficient(THETA_ENDPOINT)
        tightened = tightened_selected_system_coefficient()
        kernel = near_kernel_per_cj()
        budget = mp.exp(-2)
        baseline_limit = _mpf(baseline) * kernel
        tightened_limit = _mpf(tightened) * kernel
        counterfactual = counterfactual_theta_power_coefficient(THETA_ENDPOINT)
        counterfactual_limit = _mpf(counterfactual) * kernel
        cap = pap_cj_budget_cap()

    return CJLossTreeDiagnostic(
        theta=str(THETA_ENDPOINT),
        d_capacity_endpoint=str(D_CAPACITY_ENDPOINT),
        zero_free_c1=str(ZERO_FREE_C1),
        baseline_selected_system_coefficient=str(baseline),
        baseline_factorization_matches=baseline_factor_product(THETA_ENDPOINT) == baseline,
        rz_endpoint_coefficient=str(rz_barban_vehov_coefficient(THETA_ENDPOINT)),
        weighted_square_endpoint_upper=str(endpoint_weighted_square_upper()),
        denominator_endpoint_upper=str(TIGHT_DENOMINATOR),
        residue_row_endpoint_upper=str(endpoint_residue_row_upper()),
        residue_endpoint_upper=str(endpoint_residue_upper()),
        detector_endpoint_lower=str(RATIONAL_DETECTOR_ENDPOINT),
        area_endpoint_lower=str(EXACT_AREA_ENDPOINT),
        absorption_denominator=ABSORPTION_DENOMINATOR,
        absorption_margin_factor=str(absorption_margin_factor()),
        tightened_selected_system_coefficient=str(tightened),
        tightened_absorption_log_cutoff=mp.nstr(tightened_absorption_log_cutoff(), 60),
        coefficient_improvement_factor=mp.nstr(_mpf(baseline) / _mpf(tightened), 60),
        pap_cj_budget_cap_exp_minus_2=mp.nstr(cap, 60),
        baseline_near_limit=mp.nstr(baseline_limit, 60),
        tightened_near_limit=mp.nstr(tightened_limit, 60),
        baseline_over_budget=mp.nstr(baseline_limit / budget, 60),
        tightened_over_budget=mp.nstr(tightened_limit / budget, 60),
        counterfactual_theta_power_coefficient=str(counterfactual),
        counterfactual_over_budget=mp.nstr(counterfactual_limit / budget, 60),
        contour_lemma3_changes_asymptotic_cj=False,
        local_tightening_passes_pap_gate=bool(tightened <= cap),
        counterfactual_scaling_is_impossibility_theorem=False,
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
    "ABSORPTION_DENOMINATOR",
    "D_CAPACITY_ENDPOINT",
    "EXACT_AREA_ENDPOINT",
    "RATIONAL_DETECTOR_ENDPOINT",
    "THETA_ENDPOINT",
    "TIGHT_DENOMINATOR",
    "TIGHT_RESIDUE_ENDPOINT",
    "ZERO_FREE_C1",
    "CJLossTreeDiagnostic",
    "absorption_margin_factor",
    "baseline_factor_product",
    "baseline_selected_system_coefficient",
    "build_diagnostic",
    "counterfactual_theta_power_coefficient",
    "diagnostic_dict",
    "endpoint_preterminal_upper",
    "endpoint_residue_row_upper",
    "endpoint_residue_upper",
    "endpoint_weighted_square_upper",
    "near_kernel_per_cj",
    "pap_cj_budget_cap",
    "rz_barban_vehov_coefficient",
    "tightened_absorption_log_cutoff",
    "tightened_selected_system_coefficient",
    "weight_denominator_quotient",
    "weight_denominator_rho_supremum",
]


if __name__ == "__main__":
    import json

    mp.mp.dps = 120
    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
