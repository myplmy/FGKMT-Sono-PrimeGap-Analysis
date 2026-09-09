"""Conservative source-constant reproof for Sono/FMT H1c-1b.4d.

Bordignon's final printed formula for ``C(alpha1, alpha2, ...)`` cannot be
used numerically as written.  This module instead records a deliberately
coarse, term-complete upper bound obtained directly from Theorem 3.4 and the
zero decomposition (28)--(32), after setting

    alpha1 = A, alpha2 = A - 3, H = log(x) ** (2*A).

The final-published low-height zero sum contains ``2*q``.  It is absent from
the older arXiv-v1 display, so the final factor is preserved explicitly and
the obsolete formula is not used.

No primes are enumerated and no numerical theorem threshold is computed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial, isqrt

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import (
    DEFAULT_TRANSPORT_MARGIN,
    MINIMUM_SIEVE_DIMENSION,
    bordignon_exponent,
    maynard_log_saving_exponent,
)
from source.h1c1b4c_conditional_absorption import conditional_absorption_budget


SOURCE_REPROOF_DIMENSION_CUTOFF = 10_000_000_000
SOURCE_COMPONENT_COUNT = 13
SOURCE_COMPONENT_LOG_CEILING = -100
R0 = Fraction(6397, 1000)
SIGMA0_LAMBDA = Fraction(26213, 100000)
HIGH_ZERO_LAMBDA = Fraction(4, 25)


def _validated_integer(value: int, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _validated_log_x(r: int, log_x: object | None) -> mp.mpf:
    """Validate ``L=log(x)`` for the fixed-A half-line ``L>=r^5``."""

    r = _validated_integer(
        r,
        "r",
        minimum=SOURCE_REPROOF_DIMENSION_CUTOFF,
    )
    lower = r**5
    if log_x is None:
        with mp.workdps(100):
            return mp.mpf(lower)
    if isinstance(log_x, bool):
        raise TypeError("log_x must be a real number")
    if isinstance(log_x, int):
        if log_x < lower:
            raise ValueError("log_x must be at least r^5")
        with mp.workdps(100):
            return mp.mpf(log_x)
    with mp.workdps(100):
        result = mp.mpf(log_x)
        if not mp.isfinite(result):
            raise ValueError("log_x must be finite")
        if result < mp.mpf(lower):
            raise ValueError("log_x must be at least r^5")
        return result


def _logsumexp(values: tuple[mp.mpf, ...]) -> mp.mpf:
    if not values:
        raise ValueError("at least one logarithm is required")
    maximum = max(values)
    return maximum + mp.log(mp.fsum(mp.exp(value - maximum) for value in values))


def source_constant_component_log_uppers(
    r: int,
    log_x: object | None = None,
) -> dict[str, mp.mpf]:
    r"""Return thirteen safe log uppers for the corrected source constant.

    Write ``L=log(x)``, ``ell=log(L)``, ``A=100*r^2+10`` and ``B=A*ell``.
    The contour height is ``H=L^(2*A)``.  The first nine components bound
    ``R*(x,H,q)*H/(x*L^3)`` for every ``2<=q<=L^A``.  The final four bound
    low zeros, Sigma_0, and the two branch-independent high-zero terms.

    The constants 10000, 8, 72, 32 and 2 are intentionally loose envelopes
    for the displayed elementary terms of Bordignon's Theorem 3.4.  Their
    derivation and domain checks are stated in the accompanying proof note.
    """

    r = _validated_integer(
        r,
        "r",
        minimum=SOURCE_REPROOF_DIMENSION_CUTOFF,
    )
    L = _validated_log_x(r, log_x)
    with mp.workdps(100):
        ell = mp.log(L)
        a_fraction = bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN)
        A = mp.mpf(a_fraction.numerator) / a_fraction.denominator
        B = A * ell
        r0 = mp.mpf(R0.numerator) / R0.denominator
        sigma0_lambda = mp.mpf(SIGMA0_LAMBDA.numerator) / SIGMA0_LAMBDA.denominator
        high_lambda = mp.mpf(HIGH_ZERO_LAMBDA.numerator) / HIGH_ZERO_LAMBDA.denominator

        return {
            "01_rstar_induced_character": (
                mp.log(2) + mp.log(B) + 2 * B - L - 3 * ell
            ),
            "02_rstar_R2_R3": mp.log(10_000) - ell,
            "03_rstar_log2": 2 * B - L - 3 * ell,
            "04_rstar_R5": mp.log(8) + 4 * B - L - 2 * ell,
            "05_rstar_R7": mp.log(10_000) + 2 * mp.log(B) - 3 * ell,
            "06_rstar_R8": mp.log(72) + mp.log(B) - L - 3 * ell,
            "07_rstar_logx": 2 * B - L - 2 * ell,
            "08_rstar_zero_truncation": (
                mp.log(32) + mp.log(B) - 3 * ell
            ),
            "09_rstar_R11": (
                mp.log(2)
                + 2 * mp.log(B)
                - 3 * ell
                - L / 2
                + mp.mpf("2.5") * B
            ),
            # Final equation (31) contains 2*q; all of it is preserved.
            "10_low_height_zeros_with_final_2q": (
                mp.log(8)
                + mp.log(B + 5)
                + (2 * A - 3) * ell
                - L / (r0 * B)
            ),
            "11_sigma0": (
                mp.log(4)
                + 2 * mp.log(B)
                + (2 * A - 3) * ell
                - sigma0_lambda * L / (3 * B)
            ),
            "12_high_zeros_sqrt_branch": (
                mp.log(4)
                + (3 * A - 3) * ell
                - 2 * mp.sqrt(L / r0)
            ),
            "13_high_zeros_log_branch": (
                mp.log(4)
                + (3 * A - 3) * ell
                - high_lambda * L / (3 * B)
            ),
        }


@dataclass(frozen=True)
class SourceConstantBudget:
    sieve_dimension_r: int
    log_x: mp.mpf
    bordignon_a: Fraction
    component_count: int
    source_constant_log_upper: mp.mpf
    source_constant_strictly_below_one: bool
    conditional_absorption_log_allowance: mp.mpf
    fits_h1c1b4c_allowance: bool


def source_constant_budget(
    r: int = SOURCE_REPROOF_DIMENSION_CUTOFF,
    log_x: object | None = None,
) -> SourceConstantBudget:
    """Evaluate the project source bound and the predecessor allowance."""

    r = _validated_integer(
        r,
        "r",
        minimum=SOURCE_REPROOF_DIMENSION_CUTOFF,
    )
    L = _validated_log_x(r, log_x)
    logs = tuple(source_constant_component_log_uppers(r, L).values())
    if len(logs) != SOURCE_COMPONENT_COUNT:
        raise AssertionError("a source-constant component was omitted")
    with mp.workdps(100):
        source_log_upper = _logsumexp(logs)
        # H1c-1b.4c certifies its allowance at each dimension-bin corner.
        # The source constant itself is valid on the entire fixed-A half-line.
        predecessor = conditional_absorption_budget(r, r**5)
        return SourceConstantBudget(
            sieve_dimension_r=r,
            log_x=L,
            bordignon_a=bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN),
            component_count=len(logs),
            source_constant_log_upper=source_log_upper,
            source_constant_strictly_below_one=bool(source_log_upper < 0),
            conditional_absorption_log_allowance=(
                predecessor.admissible_log_c_a_upper
            ),
            fits_h1c1b4c_allowance=bool(
                source_log_upper < predecessor.admissible_log_c_a_upper
            ),
        )


def _elementary_e_bounds() -> tuple[Fraction, Fraction]:
    """Return the exact elementary witnesses ``2.7 < e < 2.719``."""

    lower = sum(Fraction(1, factorial(index)) for index in range(5))
    truncation = sum(Fraction(1, factorial(index)) for index in range(6))
    upper = truncation + Fraction(1, factorial(5) * 5)
    if not lower > Fraction(27, 10):
        raise AssertionError("lower exponential-series witness failed")
    if not upper < Fraction(2719, 1000):
        raise AssertionError("upper exponential-series witness failed")
    return Fraction(27, 10), Fraction(2719, 1000)


def exact_corner_log_upper_witnesses() -> dict[str, Fraction]:
    r"""Give rational strict log uppers at ``r=10^10``.

    Elementary series prove ``115 < ell=5 log(r) < 120``.  At the corner,
    ``A*ell < 12001*r^2`` and ``log(A*ell)<72``.  Substitution into the
    thirteen analytic upper bounds gives exact rational witnesses below
    ``-100``; no floating-point value carries the proof.
    """

    r = SOURCE_REPROOF_DIMENSION_CUTOFF
    L = r**5
    A = int(bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN))
    e_lower, e_upper = _elementary_e_bounds()
    if not e_upper**23 < r < e_lower**24:
        raise AssertionError("115 < 5*log(r) < 120 certificate failed")

    B_upper = 12_001 * r**2
    if not A * 120 < B_upper:
        raise AssertionError("B=A*ell corner upper failed")
    if not B_upper < r**3:
        raise AssertionError("log(B)<3*log(r)<72 witness failed")

    sqrt_L = isqrt(L)
    if sqrt_L * sqrt_L != L:
        raise AssertionError("corner L must be a perfect square")

    witnesses = {
        "01_rstar_induced_character": (
            Fraction(1 + 72 - 3 * 115, 1) + 2 * B_upper - L
        ),
        "02_rstar_R2_R3": Fraction(10 - 115, 1),
        "03_rstar_log2": Fraction(-3 * 115, 1) + 2 * B_upper - L,
        "04_rstar_R5": Fraction(3 - 2 * 115, 1) + 4 * B_upper - L,
        "05_rstar_R7": Fraction(10 + 2 * 72 - 3 * 115, 1),
        "06_rstar_R8": Fraction(5 + 72 - 3 * 115, 1) - L,
        "07_rstar_logx": Fraction(-2 * 115, 1) + 2 * B_upper - L,
        "08_rstar_zero_truncation": Fraction(4 + 72 - 3 * 115, 1),
        "09_rstar_R11": (
            Fraction(1 + 2 * 72 - 3 * 115, 1)
            - Fraction(L, 2)
            + Fraction(5 * B_upper, 2)
        ),
        "10_low_height_zeros_with_final_2q": (
            Fraction(76, 1)
            + 2 * B_upper
            - Fraction(L, 7 * B_upper)
        ),
        "11_sigma0": (
            Fraction(2 + 2 * 72 - 3 * 115, 1)
            + 2 * B_upper
            - SIGMA0_LAMBDA * Fraction(L, 3 * B_upper)
        ),
        "12_high_zeros_sqrt_branch": (
            Fraction(2, 1)
            + 3 * B_upper
            - Fraction(2 * sqrt_L, 3)
        ),
        "13_high_zeros_log_branch": (
            Fraction(2, 1)
            + 3 * B_upper
            - HIGH_ZERO_LAMBDA * Fraction(L, 3 * B_upper)
        ),
    }
    if len(witnesses) != SOURCE_COMPONENT_COUNT:
        raise AssertionError("corner witness omitted a source component")
    if not all(value < SOURCE_COMPONENT_LOG_CEILING for value in witnesses.values()):
        raise AssertionError("a source component did not fit below -100")
    return witnesses


def exact_uniformity_sufficient_checks() -> dict[str, bool]:
    """Check exact corner inequalities used by the monotonicity proof."""

    r = SOURCE_REPROOF_DIMENSION_CUTOFF
    L = r**5
    A = int(bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN))
    B_upper = 12_001 * r**2
    sqrt_L = isqrt(L)
    sqrt_r = isqrt(r)

    # Fixed-A, increasing-L derivative conditions use ell>115 and R0<7.
    low_decay_derivative = (
        Fraction(L, 7 * B_upper) * Fraction(114, 115)
    )
    sigma0_decay_derivative = (
        SIGMA0_LAMBDA
        * Fraction(L, 3 * B_upper)
        * Fraction(114, 115)
    )
    high_decay_derivative = (
        HIGH_ZERO_LAMBDA
        * Fraction(L, 3 * B_upper)
        * Fraction(114, 115)
    )

    return {
        "corner_logs_all_below_minus_100": all(
            value < SOURCE_COMPONENT_LOG_CEILING
            for value in exact_corner_log_upper_witnesses().values()
        ),
        "fixed_A_elementary_exponentials_decrease": L > 5 * A + 10,
        "fixed_A_low_zero_bound_decreases": low_decay_derivative > 2 * A + 1,
        "fixed_A_sigma0_bound_decreases": sigma0_decay_derivative > 2 * A + 1,
        "fixed_A_high_log_branch_decreases": high_decay_derivative > 3 * A,
        "fixed_A_high_sqrt_branch_decreases": Fraction(sqrt_L, 3) > 3 * A,
        "dimension_ratio_r_over_log_squared_increases": r > 8,
        "dimension_ratio_sqrt_r_over_log_increases": r > 8,
        # At the first dimension corner, use 23 < log(r) < 24.  The
        # negative-decay derivatives below dominate deliberately loose
        # uppers for the positive derivatives.  Thereafter the ratios
        # r/log(r)^2 and sqrt(r)/log(r) increase.
        "dimension_low_zero_derivative_dominated": (
            Fraction(29 * r * r, 848_400) > 49_001 * r
        ),
        "dimension_sigma0_derivative_dominated": (
            Fraction(116 * r * r, 9_000_750) > 49_001 * r
        ),
        "dimension_high_log_derivative_dominated": (
            Fraction(116 * r * r, 9_000_750) > 73_501 * r
        ),
        "dimension_high_sqrt_derivative_dominated": (
            5 * sqrt_r > 3 * 73_501
        ),
        "source_sum_below_one": 13 * Fraction(10, 27) ** 3 < 1,
        # log(qH) >= 2*A*ell and 11*log(10) < 33.
        "qH_condition": 2 * A * 115 > 33,
        "contour_below_x": 2 * B_upper < L,
        "transport_exponents_consistent": (
            maynard_log_saving_exponent(r) == 100 * r * r
            and bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN)
            == 100 * r * r + 10
        ),
    }


@dataclass(frozen=True)
class H1c1b4dStructuralCertificate:
    proved_dimension_cutoff: int
    corrected_remainder_normalization: str
    printed_constant_formula_used: bool
    final_low_zero_2q_factor_preserved: bool
    unknown_i_maximized_not_selected: bool
    q_equal_one_removed_by_exact_centering: bool
    source_component_count: int
    source_constant_reproof_closed: bool
    numerical_source_c_a_upper: str
    h1c1b4c_conditional_requirement_met: bool
    unconditional_full_absorption_at_new_cutoff_closed: bool
    parent_composition_audited: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def structural_certificate() -> H1c1b4dStructuralCertificate:
    """Build the narrow H1c-1b.4d certificate without parent promotion."""

    checks = exact_uniformity_sufficient_checks()
    if not all(checks.values()):
        raise AssertionError(f"source-constant uniformity proof failed: {checks}")
    budget = source_constant_budget()
    if not budget.source_constant_strictly_below_one:
        raise AssertionError("the corrected source constant did not fit below one")
    if not budget.fits_h1c1b4c_allowance:
        raise AssertionError("the source constant exceeded the 4c allowance")
    return H1c1b4dStructuralCertificate(
        proved_dimension_cutoff=SOURCE_REPROOF_DIMENSION_CUTOFF,
        corrected_remainder_normalization="R*(x,H,q)*H/(x*(log x)^3)",
        printed_constant_formula_used=False,
        final_low_zero_2q_factor_preserved=True,
        unknown_i_maximized_not_selected=True,
        q_equal_one_removed_by_exact_centering=True,
        source_component_count=budget.component_count,
        source_constant_reproof_closed=True,
        numerical_source_c_a_upper="C_A < 13*exp(-100) < 1",
        h1c1b4c_conditional_requirement_met=True,
        unconditional_full_absorption_at_new_cutoff_closed=True,
        parent_composition_audited=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
