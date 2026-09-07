"""Actual Maynard Section 8 input package for the corrected kappa=1 lemma.

The analytic proof is recorded in
``docs/method/theory/23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md``.
This module preserves the exact algebraic contract and evaluates the resulting
parameterized bounds.  It does not replace that proof, perform an actual prime
experiment, compose all Lemma 8.4 iterations, or compute ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L1015_R_W_M,
    APPLICATION_L1096_W0,
    APPLICATION_L1135_CANONICAL_FACTOR,
    APPLICATION_L1135_W0_FACTOR,
    APPLICATION_L1232_CANONICAL,
    APPLICATION_L620_D_W,
    APPLICATION_L737_CANONICAL,
    APPLICATION_L752_CANONICAL,
    APPLICATION_L885_W_PRIME,
    APPLICATION_L905_W_PRIME,
    APPLICATION_L995_A_M_W_B_R,
    LOCAL_FAMILY_ADJUSTED_LINEAR,
    LOCAL_FAMILY_LINEAR,
    LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1,
    LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
    maynard_local_denominator,
    maynard_uniform_application_log_q_upper,
)
from source.h1b1b2b_corrected_wirsing import (
    weighted_lemma83_multiplier,
)


H1B1B2C_MAYNARD_A1_GAP = Fraction(1, 2)
H1B1B2C_GGPY_A1_CAP = Fraction(2, 1)
H1B1B2C_UPPER_DISCREPANCY_A2 = 8
H1B1B2C_MERTENS_INTERVAL_LOWER_MAGNITUDE = Fraction(7, 2)
H1B1B2C_MERTENS_INTERVAL_UPPER = 4
H1B1B2C_LOCAL_CORRECTION_UPPER = 4
H1B1B2C_EXCLUDED_TAIL_ALLOWANCE = 1
H1B1B2C_LOWER_DISCREPANCY_BASE = 5


@dataclass(frozen=True)
class ActualGammaApplicationSpec:
    """One of the eleven source-traced analytic subapplications."""

    application_id: str
    source_locator: str
    family: str
    root_count: str


@dataclass(frozen=True)
class ActualLocalDensityCertificate:
    """Exact rational certificate for one nonexcluded local density."""

    k: int
    prime: int
    root_count: int
    previous_available_coordinates: int
    family: str
    g_denominator: Fraction
    stage_denominator: Fraction
    denominator_defect: Fraction
    density: Fraction
    density_excess_over_one_over_p: Fraction
    defect_upper: int
    density_gap_bound: Fraction


@dataclass(frozen=True)
class ActualCommonParameterPackage:
    """Common actual-family inputs, still parameterized by global k and R."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    log_r: mp.mpf
    maynard_a1_gap: Fraction
    ggpy_a1_cap: Fraction
    a2: int
    log_excluded_integer_upper: mp.mpf
    lower_discrepancy_l: mp.mpf
    lower_discrepancy_l_plus_one: mp.mpf
    weighted_multiplier: mp.mpf
    weighted_log_multiplier: mp.mpf
    one_step_relative_error_coefficient: mp.mpf
    actual_application_count: int
    r_fold_composition_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


MAYNARD_ACTUAL_GAMMA_APPLICATION_SPECS = (
    ActualGammaApplicationSpec(
        APPLICATION_L620_D_W,
        "Maynard source lines 620-622",
        LOCAL_FAMILY_LINEAR,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L737_CANONICAL,
        "Maynard source lines 723-739",
        LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L752_CANONICAL,
        "Maynard source lines 750-760",
        LOCAL_FAMILY_LINEAR,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L885_W_PRIME,
        "Maynard source lines 883-888",
        LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L905_W_PRIME,
        "Maynard source lines 903-910",
        LOCAL_FAMILY_LINEAR,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L995_A_M_W_B_R,
        "Maynard source lines 995-999",
        LOCAL_FAMILY_LINEAR,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L1015_R_W_M,
        "Maynard source lines 1015-1019",
        LOCAL_FAMILY_ADJUSTED_LINEAR,
        "omega(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L1096_W0,
        "Maynard source lines 1096-1098",
        LOCAL_FAMILY_LINEAR,
        "1",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L1135_W0_FACTOR,
        "Maynard source lines 1112-1141, r_0 factor",
        LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
        "omega*(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L1135_CANONICAL_FACTOR,
        "Maynard source lines 1112-1141, r-vector factor",
        LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
        "omega*(p)",
    ),
    ActualGammaApplicationSpec(
        APPLICATION_L1232_CANONICAL,
        "Maynard source lines 1228-1237",
        LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
        "omega(p)",
    ),
)


def actual_local_density_certificate(
    *,
    k: int,
    prime: int,
    root_count: int,
    previous_available_coordinates: int,
    family: str,
) -> ActualLocalDensityCertificate:
    """Certify the common local-density inequalities using exact rationals.

    In an actual nonexcluded Maynard call, ``prime > 2*k^2``, the relevant
    root count is at most ``k+1``, and the number of previously available
    coordinates is at most ``root_count-1``.  For all four audited families,

    ``0 <= p-(1+n+g(p)) <= 3*(root_count-1) <= 3*k``.

    Consequently ``1+n+g(p) > p/4 > 2`` and the density
    ``rho=1/(1+n+g(p))`` is below ``1/2``.  Its nonnegative excess above
    ``1/p`` is at most ``12*k/p^2``.

    The algebra holds for integer ``prime`` under these inequalities; actual
    use supplies a prime.  Avoiding an internal primality test keeps this a
    constant-time exact contract even for very large source primes.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k must be an integer at least 2")
    if isinstance(prime, bool) or not isinstance(prime, int):
        raise ValueError("prime must be an integer")
    if prime <= 2 * k * k:
        raise ValueError("a nonexcluded actual-call prime must exceed 2*k^2")
    if (
        isinstance(root_count, bool)
        or not isinstance(root_count, int)
        or not 1 <= root_count <= k + 1
    ):
        raise ValueError("root_count must be an integer in [1,k+1]")
    if (
        isinstance(previous_available_coordinates, bool)
        or not isinstance(previous_available_coordinates, int)
        or not 0 <= previous_available_coordinates <= root_count - 1
    ):
        raise ValueError(
            "previous_available_coordinates must lie in [0,root_count-1]"
        )

    g_value = maynard_local_denominator(prime, root_count, family)
    stage = 1 + previous_available_coordinates + g_value
    defect = Fraction(prime) - stage
    defect_upper = 3 * (root_count - 1)
    if not 0 <= defect <= defect_upper <= 3 * k:
        raise AssertionError("actual local denominator defect bound failed")
    if not stage > Fraction(prime, 4) > 2:
        raise AssertionError("actual local denominator lower bound failed")

    density = 1 / stage
    density_excess = density - Fraction(1, prime)
    excess_upper = Fraction(12 * k, prime * prime)
    if not 0 <= density_excess <= excess_upper:
        raise AssertionError("actual local density excess bound failed")
    if not density < Fraction(1, 2):
        raise AssertionError("Maynard A1 gap certificate failed")

    return ActualLocalDensityCertificate(
        k=k,
        prime=prime,
        root_count=root_count,
        previous_available_coordinates=previous_available_coordinates,
        family=family,
        g_denominator=g_value,
        stage_denominator=stage,
        denominator_defect=defect,
        density=density,
        density_excess_over_one_over_p=density_excess,
        defect_upper=defect_upper,
        density_gap_bound=H1B1B2C_MAYNARD_A1_GAP,
    )


def lower_discrepancy_l(
    log_excluded_integer_upper: int | float | str | mp.mpf,
) -> mp.mpf:
    """Return the common ``L = 5 + log(Lambda)`` bound.

    ``Lambda`` bounds ``log(rad(Q))`` and is at least ``log(210)`` for every
    traced application.  Rosser--Schoenfeld (3.24), a split at ``Lambda``,
    and the exact excluded-support inventory give

    ``sum_{p|Q} log(p)/p < log(Lambda)+1``.

    Combining this with the lower interval Mertens error ``>-7/2`` and
    rounding upward gives ``L=5+log(Lambda)``.
    """

    upper = mp.mpf(log_excluded_integer_upper)
    if upper < mp.log(210):
        raise ValueError("log excluded-integer upper must cover Q>=210")
    return H1B1B2C_LOWER_DISCREPANCY_BASE + mp.log(upper)


def nonexcluded_positive_correction_upper(k: int) -> mp.mpf:
    """Evaluate the proved all-prime correction majorant for diagnostics.

    For ``k=2`` the proof isolates ``p=11`` and integrates the tail from 12.
    For ``k>=3`` it integrates the decreasing function ``log(t)/t^2`` from
    ``2*k^2``.  The accompanying theory document proves each expression is
    strictly below 4; this floating evaluation is only a regression aid.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k must be an integer at least 2")
    if k == 2:
        return mp.mpf(24) * mp.log(11) / 121 + mp.log(12) + 1
    return 3 * (mp.log(2 * k * k) + 1) / k


def common_actual_parameter_package(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
) -> ActualCommonParameterPackage:
    """Evaluate the common actual-family input package.

    The resulting one-step coefficient is explicit, but it is *not* a full
    Lemma 8.4 or Proposition 6.1 error bound.  Smooth-function norms and the
    corrected accumulation through all iterations remain separate blockers.
    """

    alpha_value = mp.mpf(alpha)
    theta_value = mp.mpf(theta)
    log_r_value = mp.mpf(log_r)
    lambda_star = maynard_uniform_application_log_q_upper(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_value,
    )
    l_value = lower_discrepancy_l(lambda_star)
    multiplier = weighted_lemma83_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    log_multiplier = mp.log(multiplier)
    return ActualCommonParameterPackage(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_value,
        maynard_a1_gap=H1B1B2C_MAYNARD_A1_GAP,
        ggpy_a1_cap=H1B1B2C_GGPY_A1_CAP,
        a2=H1B1B2C_UPPER_DISCREPANCY_A2,
        log_excluded_integer_upper=lambda_star,
        lower_discrepancy_l=l_value,
        lower_discrepancy_l_plus_one=l_value + 1,
        weighted_multiplier=multiplier,
        weighted_log_multiplier=log_multiplier,
        one_step_relative_error_coefficient=multiplier * (l_value + 1),
        actual_application_count=len(MAYNARD_ACTUAL_GAMMA_APPLICATION_SPECS),
        r_fold_composition_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


__all__ = [
    "ActualCommonParameterPackage",
    "ActualGammaApplicationSpec",
    "ActualLocalDensityCertificate",
    "H1B1B2C_EXCLUDED_TAIL_ALLOWANCE",
    "H1B1B2C_GGPY_A1_CAP",
    "H1B1B2C_LOCAL_CORRECTION_UPPER",
    "H1B1B2C_LOWER_DISCREPANCY_BASE",
    "H1B1B2C_MAYNARD_A1_GAP",
    "H1B1B2C_MERTENS_INTERVAL_LOWER_MAGNITUDE",
    "H1B1B2C_MERTENS_INTERVAL_UPPER",
    "H1B1B2C_UPPER_DISCREPANCY_A2",
    "MAYNARD_ACTUAL_GAMMA_APPLICATION_SPECS",
    "actual_local_density_certificate",
    "common_actual_parameter_package",
    "lower_discrepancy_l",
    "nonexcluded_positive_correction_upper",
]
