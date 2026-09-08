"""Exact slack bookkeeping for the H1c-1b.1a dyadic repair.

This module certifies the elementary part of replacing the source-scale
dimension by

    r = floor((log(x/2))**(1/5)).

It combines the finite loss from that dimension, the actual FGKMT choice
R=(x/4)**(theta/3), and a named upper gate for the Mertens product.  It does
not produce the missing cutoff for that Mertens gate and does not prove
Maynard Hypothesis 1(2), Proposition 9.2, or a numerical Sono threshold.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

import mpmath as mp


MINIMUM_ENDPOINT_DIMENSION = 36
DIMENSION_RATIO_LOWER_BOUND = Fraction(63, 64)
R_SCALE_RATIO_LOWER_BOUND = Fraction(104, 105)
COMBINED_NORMALIZATION_LOWER_BOUND = Fraction(39, 40)
SIGMA_Y_UPPER_MULTIPLIER_GATE = Fraction(26, 25)
NET_COEFFICIENT_FACTOR = Fraction(15, 16)
SONO_LIMITING_C_MULTIPLIER = Fraction(4, 3)
HYPERGRAPH_C_MULTIPLIER_REQUIRED = Fraction(5, 4)


def _validated_dimension(r: int) -> int:
    if isinstance(r, bool) or not isinstance(r, int):
        raise TypeError("r must be an integer")
    if r < MINIMUM_ENDPOINT_DIMENSION:
        raise ValueError(
            f"r must be at least {MINIMUM_ENDPOINT_DIMENSION}"
        )
    return r


def _validated_positive_fraction(
    value: int | Fraction,
    name: str,
) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an int or Fraction")
    result = Fraction(value)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def exact_transfer_slack_certificate() -> bool:
    """Return the exact integer/rational certificate for the slack chain.

    The accompanying proof document supplies the monotonicity arguments.
    The exact endpoint checks are

    * exp(1)>2, hence log(2)<1 and log(4)<2;
    * 36**64>38**63, hence log(36)/log(38)>63/64;
    * 210<36**5, hence 1-2/36**5>104/105;
    * (63/64)*(104/105)=39/40;
    * (39/40)/(26/25)=15/16;
    * (4/3)*(15/16)=5/4.
    """

    exp_one_lower = sum(Fraction(1, factorial(n)) for n in range(3))
    return bool(
        exp_one_lower > 2
        and 36**64 > 38**63
        and 210 < 36**5
        and DIMENSION_RATIO_LOWER_BOUND * R_SCALE_RATIO_LOWER_BOUND
        == COMBINED_NORMALIZATION_LOWER_BOUND
        and COMBINED_NORMALIZATION_LOWER_BOUND
        / SIGMA_Y_UPPER_MULTIPLIER_GATE
        == NET_COEFFICIENT_FACTOR
        and SONO_LIMITING_C_MULTIPLIER * NET_COEFFICIENT_FACTOR
        == HYPERGRAPH_C_MULTIPLIER_REQUIRED
    )


def endpoint_dimension_bracket_holds(log_x: object, r: int) -> bool:
    """Check r**5 <= log(x/2) < (r+1)**5 at high precision."""

    r = _validated_dimension(r)
    log_x_mpf = mp.mpf(log_x)
    if not mp.isfinite(log_x_mpf):
        raise ValueError("log_x must be finite")
    log_t = log_x_mpf - mp.log(2)
    return bool(r**5 <= log_t < (r + 1) ** 5)


def dimension_normalization_ratio(log_x: object, r: int) -> mp.mpf:
    """Return 5*log(r)/log_2(x) for an endpoint-safe dimension."""

    r = _validated_dimension(r)
    log_x_mpf = mp.mpf(log_x)
    if log_x_mpf <= 1 or not mp.isfinite(log_x_mpf):
        raise ValueError("log_x must be finite and greater than 1")
    if not endpoint_dimension_bracket_holds(log_x_mpf, r):
        raise ValueError("r is not floor((log(x/2))**(1/5))")
    return 5 * mp.log(r) / mp.log(log_x_mpf)


def actual_r_scale_ratio(log_x: object) -> mp.mpf:
    """Return the exact finite factor in log(R)/log(x).

    FGKMT Section 8 uses R=(x/4)**(theta/3), so

        log(R)/log(x) = (theta/3) * actual_r_scale_ratio(log(x)).
    """

    log_x_mpf = mp.mpf(log_x)
    if log_x_mpf <= mp.log(4) or not mp.isfinite(log_x_mpf):
        raise ValueError("log_x must be finite and greater than log(4)")
    return 1 - mp.log(4) / log_x_mpf


def combined_normalization_ratio(log_x: object, r: int) -> mp.mpf:
    """Return the dimension factor times the actual R-scale factor."""

    return dimension_normalization_ratio(log_x, r) * actual_r_scale_ratio(
        log_x
    )


def coarse_c_lower_multiplier(
    sigma_y_upper_multiplier: int | Fraction = SIGMA_Y_UPPER_MULTIPLIER_GATE,
) -> Fraction:
    """Return the rational coarse lower multiplier of log(5) for C.

    The true inequality is strict because the dimension and R-scale bounds
    are strict.  At the default sigma gate the coarse value is exactly 5/4,
    so the true C is strictly greater than (5/4)*log(5).
    """

    sigma_multiplier = _validated_positive_fraction(
        sigma_y_upper_multiplier,
        "sigma_y_upper_multiplier",
    )
    return (
        SONO_LIMITING_C_MULTIPLIER
        * COMBINED_NORMALIZATION_LOWER_BOUND
        / sigma_multiplier
    )


def coefficient_gate_passes(
    sigma_y_upper_multiplier: int | Fraction = SIGMA_Y_UPPER_MULTIPLIER_GATE,
) -> bool:
    """Check whether the coarse finite gate retains the hypergraph constant."""

    return bool(
        coarse_c_lower_multiplier(sigma_y_upper_multiplier)
        >= HYPERGRAPH_C_MULTIPLIER_REQUIRED
    )


@dataclass(frozen=True)
class DimensionCoefficientTransferCertificate:
    endpoint_dimension_rule: str
    minimum_endpoint_dimension: int
    minimum_log_x_condition: str
    h1a_integral_ratio_used: str
    actual_r_choice: str
    dimension_ratio_lower_bound: Fraction
    r_scale_ratio_lower_bound: Fraction
    combined_normalization_lower_bound: Fraction
    sigma_y_upper_multiplier_gate: Fraction
    net_coefficient_factor: Fraction
    sono_limiting_c_multiplier: Fraction
    hypergraph_c_multiplier_required: Fraction
    exact_elementary_certificate: bool
    dyadic_dimension_admissibility_closed: bool
    actual_r_scale_correction_included: bool
    asymptotic_sono_c_preserved: bool
    finite_c_preserved_under_sigma_gate: bool
    explicit_sigma_gate_cutoff_closed: bool
    full_weight_moment_package_closed: bool
    common_exceptional_b_closed: bool
    exact_count_transfer_closed: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_07_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def dimension_coefficient_transfer_certificate(
) -> DimensionCoefficientTransferCertificate:
    """Build the fail-closed H1c-1b.1a certificate."""

    return DimensionCoefficientTransferCertificate(
        endpoint_dimension_rule="r=floor((log(x/2))**(1/5))",
        minimum_endpoint_dimension=MINIMUM_ENDPOINT_DIMENSION,
        minimum_log_x_condition="log(x/2)>=36^5",
        h1a_integral_ratio_used="J_r/I_r>log(r)/(4r) for every integer r>=36",
        actual_r_choice="R=(x/4)**(theta/3)",
        dimension_ratio_lower_bound=DIMENSION_RATIO_LOWER_BOUND,
        r_scale_ratio_lower_bound=R_SCALE_RATIO_LOWER_BOUND,
        combined_normalization_lower_bound=COMBINED_NORMALIZATION_LOWER_BOUND,
        sigma_y_upper_multiplier_gate=SIGMA_Y_UPPER_MULTIPLIER_GATE,
        net_coefficient_factor=NET_COEFFICIENT_FACTOR,
        sono_limiting_c_multiplier=SONO_LIMITING_C_MULTIPLIER,
        hypergraph_c_multiplier_required=HYPERGRAPH_C_MULTIPLIER_REQUIRED,
        exact_elementary_certificate=exact_transfer_slack_certificate(),
        dyadic_dimension_admissibility_closed=True,
        actual_r_scale_correction_included=True,
        asymptotic_sono_c_preserved=True,
        finite_c_preserved_under_sigma_gate=coefficient_gate_passes(),
        explicit_sigma_gate_cutoff_closed=False,
        full_weight_moment_package_closed=False,
        common_exceptional_b_closed=False,
        exact_count_transfer_closed=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_07_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
