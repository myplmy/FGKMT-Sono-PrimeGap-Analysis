"""Fail-closed feasibility arithmetic for alternative DEP-R09 PAP transfers.

This module compares three proof-design ideas after Theory 74:

* the pointwise minimum of the numerical Ramare and tightened Jutila bounds;
* a fixed normalized nonnegative smoothing weight supported on ``[1, U]``;
* a cancellation-preserving transfer before Gallagher's absolute values.

Only elementary arithmetic and necessary conditions are implemented here.  In
particular, this module does not assert a new zero-density theorem, does not
recover cancellation after an absolute-value bound, and does not certify
``PAP-11``, the fixed Sono coefficient, or a numerical ``X_cert``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp

from source.dep_r09_cj_loss_tree import tightened_selected_system_coefficient
from source.dep_r09_modern_density_screen import (
    D_CAPACITY_ENDPOINT,
    ZERO_FREE_C1,
    pap_zero_free_edge_mass,
    ramare_direct_slice_lower,
    ramare_source_range_log_x,
)


D_CAPACITY_MINIMUM = 21
THETA_ENDPOINT = Fraction(1, 21)
PAP_NEAR_BUDGET_EXPONENT = Fraction(2, 1)
DEFAULT_SUPPORT_UPPER = Fraction(2, 1)


def _capacity_d(d: int) -> int:
    if not isinstance(d, int):
        raise TypeError("d must be an integer")
    if not D_CAPACITY_MINIMUM <= d <= D_CAPACITY_ENDPOINT:
        raise ValueError(
            f"d must lie in [{D_CAPACITY_MINIMUM}, {D_CAPACITY_ENDPOINT}]"
        )
    return d


def _positive_mpf(value: object, name: str) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _fraction_mpf(value: Fraction) -> mp.mpf:
    if not isinstance(value, Fraction):
        raise TypeError("expected fractions.Fraction")
    return mp.mpf(value.numerator) / value.denominator


def jutila_first_slice_lower(
    d: int = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> mp.mpf:
    """Lower bound the tightened Jutila *upper certificate* on one y-slice.

    With ``y=(1-alpha)log(X)`` the Gallagher kernel contributes ``exp(-y)``.
    Theory 71's positive density right-hand side is at least ``6*C_J``.
    On ``c1*d/5 <= y <= c1*d/5+1`` this yields the returned quantity.

    This is not a lower bound for the true prime-distribution error.
    """

    d = _capacity_d(d)
    edge = pap_zero_free_edge_mass(d, c1)
    return (
        6
        * _fraction_mpf(tightened_selected_system_coefficient())
        * mp.exp(-(_fraction_mpf(edge) + 1))
    )


def hybrid_first_slice_lower(
    log_x: object,
    d: int = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> mp.mpf:
    """Lower bound the pointwise-minimum certificate on the first y-slice.

    After ``y=(1-alpha)log(X)``, both returned ingredients are uniform lower
    floors for their transformed nonnegative integrands throughout the same
    unit-width ``y`` slice.  Therefore the integral of the pointwise minimum
    is at least the minimum returned here.  This does *not* use the generally
    false implication ``integral(min(f,g)) >= min(integral(f),integral(g))``.
    """

    d = _capacity_d(d)
    ramare_main, _ = ramare_direct_slice_lower(log_x, d, c1)
    return min(ramare_main, jutila_first_slice_lower(d, c1))


def capacity_hybrid_floor(
    c1: Fraction = ZERO_FREE_C1,
) -> tuple[int, mp.mpf]:
    """Scan the finite coefficient-capacity range and return its lowest floor.

    The accompanying theory proves the monotonic endpoint reduction.  This
    finite scan is a reproducibility check rather than a substitute for it.
    """

    rows = []
    for d in range(D_CAPACITY_MINIMUM, D_CAPACITY_ENDPOINT + 1):
        log_x = ramare_source_range_log_x(d, c1)
        rows.append((d, hybrid_first_slice_lower(log_x, d, c1)))
    return min(rows, key=lambda row: row[1])


def pap_near_budget(
    exponent: Fraction = PAP_NEAR_BUDGET_EXPONENT,
) -> mp.mpf:
    if not isinstance(exponent, Fraction):
        raise TypeError("exponent must be an exact Fraction")
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    return mp.exp(-_fraction_mpf(exponent))


def required_attenuation(
    certificate_floor: object,
    budget: object | None = None,
) -> mp.mpf:
    """Return the multiplicative attenuation required to fit the budget."""

    floor = _positive_mpf(certificate_floor, "certificate_floor")
    target = pap_near_budget() if budget is None else _positive_mpf(budget, "budget")
    return target / floor


def first_slice_delta_upper(
    log_x: object,
    d: int = D_CAPACITY_ENDPOINT,
    c1: Fraction = ZERO_FREE_C1,
) -> mp.mpf:
    """Return ``(c1*d/5+1)/log(X)`` for the first y-slice."""

    log_x_mp = _positive_mpf(log_x, "log_x")
    edge = pap_zero_free_edge_mass(_capacity_d(d), c1)
    return (_fraction_mpf(edge) + 1) / log_x_mp


def positive_weight_zero_frequency_lower(
    delta: object,
    support_upper: object = 2,
) -> mp.mpf:
    """Necessary zero-frequency lower bound for a nonnegative Mellin weight.

    If ``w>=0`` is supported on ``[1,U]`` and has positive mass, then
    ``K_w(delta,0)=int w(u)u^-delta du / int w(u)du >= U^-delta``.
    Consequently a gamma-uniform absolute-value envelope using no zero-height
    information cannot promise a smaller factor.  This does not rule out a
    transfer that exploits a new quantitative distribution theorem in gamma.
    """

    delta_mp = _positive_mpf(delta, "delta")
    support_mp = _positive_mpf(support_upper, "support_upper")
    if support_mp < 1:
        raise ValueError("support_upper must be at least 1")
    return mp.power(support_mp, -delta_mp)


def required_support_log10(
    target_attenuation: object,
    delta: object,
) -> mp.mpf:
    """Return log10(U) required by the weak condition ``U^-delta<=target``."""

    target = _positive_mpf(target_attenuation, "target_attenuation")
    delta_mp = _positive_mpf(delta, "delta")
    if target >= 1:
        raise ValueError("target_attenuation must be less than 1")
    return -mp.log(target) / (delta_mp * mp.log(10))


def signed_weight_condition_number_lower(
    target_attenuation: object,
    delta: object,
    support_upper: object = 2,
) -> mp.mpf:
    """Necessary L1/mass ratio for a fixed signed weight on ``[1,U]``.

    For ``kappa=||w||_1/|int w|`` and normalized Mellin transform ``K_w``,
    ``|K_w(delta)-1| <= delta*log(U)*kappa``.  Thus ``|K_w|<=a<1`` requires
    ``kappa >= (1-a)/(delta*log(U))``.
    """

    target = _positive_mpf(target_attenuation, "target_attenuation")
    delta_mp = _positive_mpf(delta, "delta")
    support_mp = _positive_mpf(support_upper, "support_upper")
    if target >= 1:
        raise ValueError("target_attenuation must be less than 1")
    if support_mp <= 1:
        raise ValueError("support_upper must exceed 1")
    return (1 - target) / (delta_mp * mp.log(support_mp))


@dataclass(frozen=True)
class TransferFeasibilityDiagnostic:
    d_capacity_minimum: int
    d_capacity_endpoint: int
    zero_free_c1: str
    tightened_jutila_coefficient: str
    endpoint_source_min_log_x: str
    endpoint_zero_free_edge_mass: str
    endpoint_first_slice_delta_upper: str
    endpoint_ramare_main_slice_lower: str
    endpoint_jutila_slice_lower: str
    capacity_floor_attained_d: int
    capacity_hybrid_first_slice_floor: str
    pap_near_budget_exp_minus_2: str
    attenuation_required: str
    source_blind_nonnegative_support_1_2_lower_at_theta: str
    source_blind_nonnegative_support_1_2_lower_at_actual_slice: str
    nonnegative_theta_lower_over_required: str
    nonnegative_actual_lower_over_required: str
    support_log10_required_at_theta: str
    support_log10_required_at_actual_slice: str
    signed_weight_condition_number_lower_at_theta: str
    signed_weight_condition_number_lower_at_actual_slice: str
    pointwise_minimum_passes_current_budget: bool
    fixed_nonnegative_source_blind_uniform_envelope_passes_current_budget: bool
    all_smoothing_or_cancellation_proofs_ruled_out: bool
    cancellation_recoverable_after_absolute_value_reduction: bool
    new_pre_absolute_value_uniform_theorem_required: bool
    public_numerical_cancellation_drop_in_found: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> TransferFeasibilityDiagnostic:
    """Build the endpoint and finite-capacity feasibility diagnostic."""

    with mp.workdps(max(mp.mp.dps, 120)):
        d = D_CAPACITY_ENDPOINT
        source_min = ramare_source_range_log_x(d)
        edge = pap_zero_free_edge_mass(d)
        delta_actual = first_slice_delta_upper(source_min, d)
        ramare_main, _ = ramare_direct_slice_lower(source_min, d)
        jutila_lower = jutila_first_slice_lower(d)
        floor_d, floor = capacity_hybrid_floor()
        budget = pap_near_budget()
        attenuation = required_attenuation(floor, budget)
        theta = _fraction_mpf(THETA_ENDPOINT)
        positive_theta = positive_weight_zero_frequency_lower(theta)
        positive_actual = positive_weight_zero_frequency_lower(delta_actual)
        support_theta = required_support_log10(attenuation, theta)
        support_actual = required_support_log10(attenuation, delta_actual)
        signed_theta = signed_weight_condition_number_lower(attenuation, theta)
        signed_actual = signed_weight_condition_number_lower(
            attenuation, delta_actual
        )

    return TransferFeasibilityDiagnostic(
        d_capacity_minimum=D_CAPACITY_MINIMUM,
        d_capacity_endpoint=D_CAPACITY_ENDPOINT,
        zero_free_c1=str(ZERO_FREE_C1),
        tightened_jutila_coefficient=str(tightened_selected_system_coefficient()),
        endpoint_source_min_log_x=mp.nstr(source_min, 60),
        endpoint_zero_free_edge_mass=str(edge),
        endpoint_first_slice_delta_upper=mp.nstr(delta_actual, 60),
        endpoint_ramare_main_slice_lower=mp.nstr(ramare_main, 60),
        endpoint_jutila_slice_lower=mp.nstr(jutila_lower, 60),
        capacity_floor_attained_d=floor_d,
        capacity_hybrid_first_slice_floor=mp.nstr(floor, 60),
        pap_near_budget_exp_minus_2=mp.nstr(budget, 60),
        attenuation_required=mp.nstr(attenuation, 60),
        source_blind_nonnegative_support_1_2_lower_at_theta=mp.nstr(
            positive_theta, 60
        ),
        source_blind_nonnegative_support_1_2_lower_at_actual_slice=mp.nstr(
            positive_actual, 60
        ),
        nonnegative_theta_lower_over_required=mp.nstr(
            positive_theta / attenuation, 60
        ),
        nonnegative_actual_lower_over_required=mp.nstr(
            positive_actual / attenuation, 60
        ),
        support_log10_required_at_theta=mp.nstr(support_theta, 60),
        support_log10_required_at_actual_slice=mp.nstr(support_actual, 60),
        signed_weight_condition_number_lower_at_theta=mp.nstr(signed_theta, 60),
        signed_weight_condition_number_lower_at_actual_slice=mp.nstr(
            signed_actual, 60
        ),
        pointwise_minimum_passes_current_budget=bool(floor <= budget),
        fixed_nonnegative_source_blind_uniform_envelope_passes_current_budget=bool(
            positive_theta <= attenuation
        ),
        all_smoothing_or_cancellation_proofs_ruled_out=False,
        cancellation_recoverable_after_absolute_value_reduction=False,
        new_pre_absolute_value_uniform_theorem_required=True,
        public_numerical_cancellation_drop_in_found=False,
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
    "DEFAULT_SUPPORT_UPPER",
    "D_CAPACITY_MINIMUM",
    "PAP_NEAR_BUDGET_EXPONENT",
    "THETA_ENDPOINT",
    "TransferFeasibilityDiagnostic",
    "build_diagnostic",
    "capacity_hybrid_floor",
    "diagnostic_dict",
    "first_slice_delta_upper",
    "hybrid_first_slice_lower",
    "jutila_first_slice_lower",
    "pap_near_budget",
    "positive_weight_zero_frequency_lower",
    "required_attenuation",
    "required_support_log10",
    "signed_weight_condition_number_lower",
]


if __name__ == "__main__":
    import json

    print(json.dumps(diagnostic_dict(), ensure_ascii=True, indent=2, sort_keys=True))
