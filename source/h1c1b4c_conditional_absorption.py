"""Conditional full-error budget for Sono/FMT H1c-1b.4c.

The preceding gates provide the complete twelve-term Bordignon remainder,
the exact endpoint/count transfer, and the explicit lower bound

    P_T / T > 1 / (2 log T).

This module puts those ingredients on one normalized scale.  The unresolved
Theorem 1.2 constant is kept as the variable ``C_A``.  Consequently the
certificate proved here is conditional: it says exactly how small ``C_A``
must be, but it does not claim that Bordignon's source supplies such a bound.

No prime enumeration or threshold calculation is performed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import (
    DEFAULT_TRANSPORT_MARGIN,
    MINIMUM_SIEVE_DIMENSION,
    bordignon_exponent,
    maynard_log_saving_exponent,
)
from source.h1c1b2_common_exceptional_remainder import R1


PROVED_DIMENSION_CUTOFF = 500_000_000
SAFE_LOG_C_A_UPPER = 500
NON_C_COMPONENT_COUNT = 13
NON_C_COMPONENT_LOG_CEILING = -500
C_COEFFICIENT_LOG_CEILING = -536


def _validated_integer(value: int, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _validated_log_t_in_dimension_bin(r: int, log_t: object | None) -> mp.mpf:
    r = _validated_integer(r, "r", minimum=MINIMUM_SIEVE_DIMENSION)
    lower = r**5
    upper = (r + 1) ** 5
    if log_t is None:
        # Do not compare the 44-digit neighboring bin endpoints after a
        # default-precision mp conversion.  The exact left endpoint is known.
        with mp.workdps(80):
            return mp.mpf(lower)
    if isinstance(log_t, bool):
        raise TypeError("log_t must be a real number")
    if isinstance(log_t, int):
        if log_t < lower or log_t >= upper:
            raise ValueError("log_t must lie in [r^5,(r+1)^5)")
        with mp.workdps(80):
            return mp.mpf(log_t)
    with mp.workdps(80):
        result = mp.mpf(log_t)
        if not mp.isfinite(result):
            raise ValueError("log_t must be finite")
        if result < mp.mpf(lower) or result >= mp.mpf(upper):
            raise ValueError("log_t must lie in [r^5,(r+1)^5)")
        return result


def _logsumexp(values: tuple[mp.mpf, ...]) -> mp.mpf:
    if not values:
        raise ValueError("at least one logarithm is required")
    maximum = max(values)
    return maximum + mp.log(mp.fsum(mp.exp(value - maximum) for value in values))


def normalized_non_c_component_logs(
    r: int,
    log_t: object | None = None,
) -> dict[str, mp.mpf]:
    r"""Return safe log upper bounds after division by the target.

    Put ``L=log T``, ``ell=log L``, ``n=100r^2`` and
    ``A=n+10``.  Since

    ``1/L + 2/(L+log 2) + 1/L^2 <= 4/L``,

    a relative Bordignon remainder term ``rho_j`` contributes at most
    ``8 L^n rho_j`` after division by
    ``1/(2 L^(n+1))``.  All terms except the printed Theorem 1.2 term are
    returned here.  The latter's coefficient is returned separately by
    :func:`normalized_c_a_coefficient_log`.

    For the dyadic supremum, term 3 is evaluated at ``log(2T)=L+log 2``;
    the other eleven source terms are decreasing in that endpoint variable
    on the certified domain and are evaluated at ``L``.
    """

    r = _validated_integer(r, "r", minimum=PROVED_DIMENSION_CUTOFF)
    L = _validated_log_t_in_dimension_bin(r, log_t)
    with mp.workdps(80):
        ell = mp.log(L)
        n = mp.mpf(maynard_log_saving_exponent(r))
        A_fraction = bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN)
        A = mp.mpf(A_fraction.numerator) / A_fraction.denominator
        h = mp.log(2)
        delta = 1 / (2 * A * (mp.mpf(R1.numerator) / R1.denominator) * ell)
        if not 0 < delta < 1:
            raise AssertionError("exceptional-zero delta escaped (0,1)")

        return {
            "01_leading_sqrt": mp.log(8) + n * ell - L / 2,
            "02_main_log_tail": mp.log(2352) - mp.mpf("5.5") * ell,
            "03_main_q1_tail": (
                mp.log(2352)
                + mp.mpf("4.5") * mp.log(1 + h / L)
                - mp.mpf("5.5") * ell
            ),
            "05_induced_character_small_modulus": (
                mp.log(4 / mp.log(2)) - L / 2 - 9 * ell
            ),
            "06_exceptional_zero": (
                mp.log(36)
                + mp.log(1 + A * ell)
                - mp.log(1 - delta)
                + (n + 1) * ell
                - L / (2 * A * (mp.mpf(R1.numerator) / R1.denominator) * ell)
            ),
            "07_density_exponential": (
                mp.log(1224)
                + mp.log(1 + A * ell)
                + (n + mp.mpf("2.52")) * ell
                - mp.mpf("0.81") * mp.sqrt(L)
            ),
            "08_density_constant": (
                mp.log(36 / mp.log(2))
                + mp.log(A * ell)
                + mp.log(1 + A * ell)
                + (n + 1) * ell
                - L
            ),
            "09_large_modulus_sqrt": (
                mp.log(2352) - L / 2 + (n + A + mp.mpf("4.5")) * ell
            ),
            "10_large_modulus_eleven_twelfths": (
                mp.log(10584) - L / 12 + (n / 2 - mp.mpf("0.5")) * ell
            ),
            "11_large_modulus_five_sixths": (
                mp.log(2940) - L / 6 + (n + mp.mpf("4.5")) * ell
            ),
            "12_large_modulus_five_sixths_log": (
                mp.log(1470) - L / 6 + (n + mp.mpf("5.5")) * ell
            ),
            "13_prime_power_removal": (
                mp.log(8 * mp.sqrt(2)) + (n + 1) * ell - L / 6
            ),
            "14_half_open_endpoint": mp.log(2) + (n + 1) * ell - 2 * L / 3,
        }


def normalized_c_a_coefficient_log(
    r: int,
    log_t: object | None = None,
) -> mp.mpf:
    r"""Return log(kappa) in ``normalized_error <= B0 + kappa*C_A``.

    With the fixed transport margin ten,

    ``kappa = 36 (1 + A log log T) (log T)^(-6)``.

    The coefficient uses the same safe ``4/log T`` Abel factor as the
    non-``C_A`` components.
    """

    r = _validated_integer(r, "r", minimum=PROVED_DIMENSION_CUTOFF)
    L = _validated_log_t_in_dimension_bin(r, log_t)
    with mp.workdps(80):
        ell = mp.log(L)
        A_fraction = bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN)
        A = mp.mpf(A_fraction.numerator) / A_fraction.denominator
        return mp.log(36) + mp.log(1 + A * ell) - 6 * ell


@dataclass(frozen=True)
class ConditionalAbsorptionBudget:
    sieve_dimension_r: int
    log_t: mp.mpf
    required_log_saving_exponent: int
    bordignon_a: Fraction
    non_c_component_count: int
    normalized_non_c_log_upper: mp.mpf
    normalized_c_a_coefficient_log_upper: mp.mpf
    admissible_log_c_a_upper: mp.mpf
    safe_project_log_c_a_upper: int
    safe_project_condition_passes: bool


def conditional_absorption_budget(
    r: int = PROVED_DIMENSION_CUTOFF,
    log_t: object | None = None,
) -> ConditionalAbsorptionBudget:
    """Compute the conditional budget on the certified proof domain."""

    r = _validated_integer(r, "r", minimum=PROVED_DIMENSION_CUTOFF)
    L = _validated_log_t_in_dimension_bin(r, log_t)
    with mp.workdps(80):
        component_logs = tuple(normalized_non_c_component_logs(r, L).values())
        if len(component_logs) != NON_C_COMPONENT_COUNT:
            raise AssertionError("a non-C absorption component was omitted")
        log_b0 = _logsumexp(component_logs)
        if log_b0 >= 0:
            raise ValueError("non-C components exhaust the normalized target")
        log_kappa = normalized_c_a_coefficient_log(r, L)
        log_allowance = mp.log1p(-mp.exp(log_b0)) - log_kappa
        return ConditionalAbsorptionBudget(
            sieve_dimension_r=r,
            log_t=L,
            required_log_saving_exponent=maynard_log_saving_exponent(r),
            bordignon_a=bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN),
            non_c_component_count=len(component_logs),
            normalized_non_c_log_upper=log_b0,
            normalized_c_a_coefficient_log_upper=log_kappa,
            admissible_log_c_a_upper=log_allowance,
            safe_project_log_c_a_upper=SAFE_LOG_C_A_UPPER,
            safe_project_condition_passes=bool(
                log_b0 < 0 and SAFE_LOG_C_A_UPPER < log_allowance
            ),
        )


def _e_rational_bounds() -> tuple[Fraction, Fraction]:
    """Return elementary exact bounds ``27/10 < e < 2719/1000``."""

    lower = sum(Fraction(1, factorial(index)) for index in range(5))
    truncation = sum(Fraction(1, factorial(index)) for index in range(6))
    upper = truncation + Fraction(1, factorial(5) * 5)
    if not lower > Fraction(27, 10):
        raise AssertionError("lower exponential-series witness failed")
    if not upper < Fraction(2719, 1000):
        raise AssertionError("upper exponential-series witness failed")
    return Fraction(27, 10), Fraction(2719, 1000)


def exact_corner_log_upper_witnesses() -> dict[str, Fraction]:
    r"""Return rational strict upper witnesses at ``r=500,000,000``.

    The elementary exponential-series bounds prove
    ``100 < ell=5 log r < 105``.  The dictionary then records rational
    upper bounds for the thirteen non-``C_A`` normalized log components.
    Every entry is strictly below ``-500``.  The proof document supplies the
    monotonicity argument extending this corner check to every larger
    dimension and every ``L`` in its dimension bin.
    """

    r = PROVED_DIMENSION_CUTOFF
    L = r**5
    n = maynard_log_saving_exponent(r)
    A = int(bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN))
    e_lower, e_upper = _e_rational_bounds()
    if not e_upper**20 < r < e_lower**21:
        raise AssertionError("100 < 5 log(r) < 105 certificate failed")
    if not 1 + A * 105 < r**3:
        raise AssertionError("1+A*ell < r^3 corner certificate failed")
    if not r > 22_000**2:
        raise AssertionError("sqrt(r)>22000 certificate failed")

    q_lower = Fraction(L, 1) / (
        2
        * Fraction(2046, 1000)
        * Fraction(100001, 1000)
        * r**2
        * 105
    )
    witnesses = {
        "01_leading_sqrt": Fraction(3 + 105 * n, 1) - Fraction(L, 2),
        "02_main_log_tail": Fraction(8, 1) - Fraction(11, 2) * 100,
        "03_main_q1_tail": (
            Fraction(8, 1) + Fraction(9, 2) - Fraction(11, 2) * 100
        ),
        "05_induced_character_small_modulus": (
            Fraction(3, 1) - Fraction(L, 2) - 9 * 100
        ),
        "06_exceptional_zero": (
            Fraction(4 + 63 + 1, 1) + (n + 1) * 105 - q_lower
        ),
        "07_density_exponential": (
            Fraction(8 + 63, 1)
            + (Fraction(n, 1) + Fraction(63, 25)) * 105
            - Fraction(81, 100) * r**2 * 22_000
        ),
        "08_density_constant": (
            Fraction(5 + 126, 1) + (n + 1) * 105 - L
        ),
        "09_large_modulus_sqrt": (
            Fraction(8, 1)
            - Fraction(L, 2)
            + (n + A + Fraction(9, 2)) * 105
        ),
        "10_large_modulus_eleven_twelfths": (
            Fraction(10, 1)
            - Fraction(L, 12)
            + (Fraction(n, 2) - Fraction(1, 2)) * 105
        ),
        "11_large_modulus_five_sixths": (
            Fraction(9, 1)
            - Fraction(L, 6)
            + (n + Fraction(9, 2)) * 105
        ),
        "12_large_modulus_five_sixths_log": (
            Fraction(8, 1)
            - Fraction(L, 6)
            + (n + Fraction(11, 2)) * 105
        ),
        "13_prime_power_removal": (
            Fraction(3, 1) + (n + 1) * 105 - Fraction(L, 6)
        ),
        "14_half_open_endpoint": (
            Fraction(1, 1) + (n + 1) * 105 - Fraction(2 * L, 3)
        ),
    }
    if len(witnesses) != NON_C_COMPONENT_COUNT:
        raise AssertionError("corner witness omitted a non-C component")
    if not all(value < NON_C_COMPONENT_LOG_CEILING for value in witnesses.values()):
        raise AssertionError("a corner log witness did not fit below -500")
    return witnesses


def exact_uniformity_sufficient_checks() -> dict[str, bool]:
    """Check the rational base inequalities used by the calculus proof."""

    r = PROVED_DIMENSION_CUTOFF
    L = r**5
    n = maynard_log_saving_exponent(r)
    A = int(bordignon_exponent(r, DEFAULT_TRANSPORT_MARGIN))
    q_lower = Fraction(L, 1) / (
        2
        * Fraction(2046, 1000)
        * Fraction(100001, 1000)
        * r**2
        * 105
    )
    critical_r_positive_derivative = (
        200 * r * 105 + Fraction(5 * (n + 1), r) + Fraction(3, r)
    )
    density_r_positive_derivative = (
        200 * r * 105
        + Fraction(5, r) * (n + Fraction(63, 25))
        + Fraction(3, r)
    )
    return {
        "corner_logs_all_below_minus_500": all(
            value < NON_C_COMPONENT_LOG_CEILING
            for value in exact_corner_log_upper_witnesses().values()
        ),
        "c_coefficient_log_strictly_below_minus_536": (
            Fraction(4, 1) - Fraction(27, 5) * 100
            <= C_COEFFICIENT_LOG_CEILING
        ),
        "critical_r_derivative_is_negative": (
            Fraction(29, 10) * q_lower / r
            > critical_r_positive_derivative
        ),
        "critical_L_derivative_is_negative": (
            q_lower * Fraction(99, 100) > n + 2
        ),
        "density_r_derivative_is_negative": (
            Fraction(81, 100) * Fraction(5, 2) * r * 22_000
            > density_r_positive_derivative
        ),
        "density_L_derivative_is_negative": (
            Fraction(81, 200) * r**2 * 22_000 > n + 4
        ),
        "large_exponential_terms_decrease_in_L": L > 12 * (2 * n + A + 20),
        "one_plus_Aell_below_r_cubed_at_corner": 1 + A * 105 < r**3,
        "safe_C_condition_has_two_independent_quarter_budgets": (
            NON_C_COMPONENT_COUNT < 2**498 and 2**36 > 4
        ),
    }


@dataclass(frozen=True)
class H1c1b4cStructuralCertificate:
    proved_dimension_cutoff: int
    target_normalization: str
    non_c_components_complete: bool
    all_non_c_components_absorbed_above_cutoff: bool
    admissible_c_a_formula_derived: bool
    safe_conditional_log_c_a_upper: int
    conditional_full_absorption_closed: bool
    numerical_source_c_a_upper_closed: bool
    unconditional_full_absorption_closed: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def structural_certificate() -> H1c1b4cStructuralCertificate:
    """Build the narrow fail-closed H1c-1b.4c certificate."""

    checks = exact_uniformity_sufficient_checks()
    if not all(checks.values()):
        raise AssertionError(f"uniform conditional absorption proof failed: {checks}")
    budget = conditional_absorption_budget()
    if not budget.safe_project_condition_passes:
        raise AssertionError("C_A<=exp(500) did not fit the conditional budget")
    return H1c1b4cStructuralCertificate(
        proved_dimension_cutoff=PROVED_DIMENSION_CUTOFF,
        target_normalization="S_pi/T <= 1/(2*(log T)^(100*r^2+1))",
        non_c_components_complete=(
            budget.non_c_component_count == NON_C_COMPONENT_COUNT
        ),
        all_non_c_components_absorbed_above_cutoff=True,
        admissible_c_a_formula_derived=True,
        safe_conditional_log_c_a_upper=SAFE_LOG_C_A_UPPER,
        conditional_full_absorption_closed=True,
        numerical_source_c_a_upper_closed=False,
        unconditional_full_absorption_closed=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
