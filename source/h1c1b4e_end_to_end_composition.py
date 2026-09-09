"""End-to-end composition of the actual FGKMT Hypothesis 1 input.

This module combines the corrected FGKMT closed interval, the complete
H1c-1b.4c normalized error budget, and the H1c-1b.4d source-constant
reproof.  It also supplies explicit elementary constants for clauses (1)
and (3) when ``A=Z``.

The result is intentionally narrow: it closes Hypothesis 1 for the actual
identity-form subset at a conservative finite cutoff.  It does not close
the weighted Proposition 9.2 proof, the lower-endpoint weight occurring
when FGKMT returns to its external prime set, SIV-08 as a broad root node,
or the final theorem threshold ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import (
    DEFAULT_TRANSPORT_MARGIN,
    MINIMUM_SIEVE_DIMENSION,
    bordignon_exponent,
    maynard_log_saving_exponent,
)
from source.h1c1b3r1_fgkmt_endpoint_correction import (
    endpoint_correction_certificate,
)
from source.h1c1b4c_conditional_absorption import (
    PROVED_DIMENSION_CUTOFF,
    conditional_absorption_budget,
    exact_uniformity_sufficient_checks as absorption_uniformity_checks,
)
from source.h1c1b4d_source_constant_reproof import (
    SOURCE_REPROOF_DIMENSION_CUTOFF,
    exact_uniformity_sufficient_checks as source_uniformity_checks,
    source_constant_budget,
)


COMPOSITION_DIMENSION_CUTOFF = SOURCE_REPROOF_DIMENSION_CUTOFF
COMPOSITION_LOG_T_CUTOFF = COMPOSITION_DIMENSION_CUTOFF**5
HYPOTHESIS_CLAUSE_1_CONSTANT = 1
HYPOTHESIS_CLAUSE_2_CONSTANT = 1
HYPOTHESIS_CLAUSE_3_CONSTANT = 2


def _validated_integer(value: int, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _validated_dimension_bin(r: int, log_t: object | None) -> mp.mpf:
    r = _validated_integer(r, "r", minimum=COMPOSITION_DIMENSION_CUTOFF)
    lower = r**5
    upper = (r + 1) ** 5
    if log_t is None:
        with mp.workdps(100):
            return mp.mpf(lower)
    if isinstance(log_t, bool):
        raise TypeError("log_t must be a real number")
    if isinstance(log_t, int):
        if log_t < lower or log_t >= upper:
            raise ValueError("log_t must lie in [r^5,(r+1)^5)")
        with mp.workdps(100):
            return mp.mpf(log_t)
    with mp.workdps(100):
        result = mp.mpf(log_t)
        if not mp.isfinite(result):
            raise ValueError("log_t must be finite")
        if result < mp.mpf(lower) or result >= mp.mpf(upper):
            raise ValueError("log_t must lie in [r^5,(r+1)^5)")
        return result


def _logsumexp(left: mp.mpf, right: mp.mpf) -> mp.mpf:
    maximum = max(left, right)
    return maximum + mp.log(mp.exp(left - maximum) + mp.exp(right - maximum))


@dataclass(frozen=True)
class PrimeDistributionCompositionBudget:
    sieve_dimension_r: int
    log_t: mp.mpf
    log_normalized_non_source_terms: mp.mpf
    log_source_coefficient: mp.mpf
    log_source_constant_upper: mp.mpf
    log_total_normalized_error_upper: mp.mpf
    target_strictly_met: bool


def prime_distribution_composition_budget(
    r: int = COMPOSITION_DIMENSION_CUTOFF,
    log_t: object | None = None,
) -> PrimeDistributionCompositionBudget:
    """Compose all clause-(2) error components on the target scale."""

    r = _validated_integer(r, "r", minimum=COMPOSITION_DIMENSION_CUTOFF)
    L = _validated_dimension_bin(r, log_t)
    absorption = conditional_absorption_budget(r, L)
    source = source_constant_budget(r, L)
    with mp.workdps(100):
        source_contribution = (
            absorption.normalized_c_a_coefficient_log_upper
            + source.source_constant_log_upper
        )
        total = _logsumexp(
            absorption.normalized_non_c_log_upper,
            source_contribution,
        )
        return PrimeDistributionCompositionBudget(
            sieve_dimension_r=r,
            log_t=L,
            log_normalized_non_source_terms=(
                absorption.normalized_non_c_log_upper
            ),
            log_source_coefficient=(
                absorption.normalized_c_a_coefficient_log_upper
            ),
            log_source_constant_upper=source.source_constant_log_upper,
            log_total_normalized_error_upper=total,
            target_strictly_met=bool(total < 0),
        )


def exact_easy_clause_sufficient_checks(
    r: int = COMPOSITION_DIMENSION_CUTOFF,
) -> dict[str, bool]:
    r"""Return exact integer witnesses for clauses (1), (3), and ``B``.

    Let ``L=log T``, ``ell=log L``, and
    ``r=floor(L^(1/5))``.  Then ``L<(r+1)^5`` gives
    ``ell<5 log(r+1)<5r``.  For the closed integer interval its population
    ``N`` satisfies ``N>=T-1>=T/2``.

    Clause (1) follows from one unit of discrepancy per modulus once

    ``log(2)+100*r^2*ell <= 2L/3``.

    The first integer witness below proves a stronger inequality using
    ``log(2)<1``, ``ell<5r``, and ``L>=r^5``.  Clause (3) uses ``N>=q``.
    The final coefficient-style check shows the selected exceptional prime
    obeys ``B<=Q1=L^A<=T^2`` for ``A=100*r^2+10``.
    """

    r = _validated_integer(r, "r", minimum=COMPOSITION_DIMENSION_CUTOFF)
    n = maynard_log_saving_exponent(r)
    a = int(bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN))
    return {
        "composition_cutoff_dominates_conditional_cutoff": (
            r >= PROVED_DIMENSION_CUTOFF
        ),
        "dimension_bin_implies_ell_below_5r": r >= 1,
        "clause1_log_absorption": 3 * (5 * r * n + 1) <= 2 * r**5,
        "closed_interval_population_at_least_half_T": r**5 >= 1,
        "clause3_modulus_below_population": r**5 >= 3,
        "exceptional_B_below_T_squared": 5 * r * a <= 2 * r**5,
        "dimension_above_maynard_minimum": r >= MINIMUM_SIEVE_DIMENSION,
    }


@dataclass(frozen=True)
class H1c1b4eStructuralCertificate:
    proved_dimension_cutoff: int
    proved_log_t_cutoff: int
    outer_x_cutoff: str
    fgkmt_hypothesis_interval: str
    identity_subset_only: bool
    clause1_constant: int
    clause2_constant: int
    clause3_constant: int
    clause1_closed: bool
    clause2_closed: bool
    clause3_closed: bool
    common_exceptional_b_closed: bool
    exceptional_b_below_t_squared: bool
    actual_identity_hypothesis1_input_closed: bool
    proposition92_hypothesis_input_closed: bool
    proposition92_weighted_moment_closed: bool
    downstream_weighted_lower_endpoint_closed: bool
    broad_siv_08_root_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def structural_certificate() -> H1c1b4eStructuralCertificate:
    """Build the actual-input certificate while preserving parent blockers."""

    endpoint = endpoint_correction_certificate()
    easy = exact_easy_clause_sufficient_checks()
    if not all(easy.values()):
        raise AssertionError(f"an elementary Hypothesis 1 check failed: {easy}")
    if not all(absorption_uniformity_checks().values()):
        raise AssertionError("the H1c-1b.4c uniform absorption proof failed")
    if not all(source_uniformity_checks().values()):
        raise AssertionError("the H1c-1b.4d source proof failed")
    budget = prime_distribution_composition_budget()
    if not budget.target_strictly_met:
        raise AssertionError("the complete prime-distribution budget missed its target")
    if not endpoint.fgkmt_hypothesis_endpoint_bridge_closed:
        raise AssertionError("the corrected FGKMT endpoint bridge is not closed")
    return H1c1b4eStructuralCertificate(
        proved_dimension_cutoff=COMPOSITION_DIMENSION_CUTOFF,
        proved_log_t_cutoff=COMPOSITION_LOG_T_CUTOFF,
        outer_x_cutoff="X >= 2*exp(10^50)",
        fgkmt_hypothesis_interval="[T,2T]",
        identity_subset_only=True,
        clause1_constant=HYPOTHESIS_CLAUSE_1_CONSTANT,
        clause2_constant=HYPOTHESIS_CLAUSE_2_CONSTANT,
        clause3_constant=HYPOTHESIS_CLAUSE_3_CONSTANT,
        clause1_closed=True,
        clause2_closed=True,
        clause3_closed=True,
        common_exceptional_b_closed=True,
        exceptional_b_below_t_squared=True,
        actual_identity_hypothesis1_input_closed=True,
        proposition92_hypothesis_input_closed=True,
        proposition92_weighted_moment_closed=False,
        downstream_weighted_lower_endpoint_closed=False,
        broad_siv_08_root_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
