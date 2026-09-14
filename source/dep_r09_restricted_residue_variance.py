"""Exact algebra for the DEP-R09 restricted-residue variance audit.

This module verifies only finite character-energy identities and scalar
budget normalizations.  It does not prove a prime-distribution theorem,
does not supply the missing weighted character-error estimate, and does not
certify PAP-11, the fixed Sono coefficient, or a numerical ``X_cert``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp


D_MIN = 21
D_MAX = 186
PAP_NEAR_BUDGET_EXPONENT = Fraction(2, 1)


def _population(phi_q: int, residue_count: int) -> tuple[int, int]:
    if isinstance(phi_q, bool) or not isinstance(phi_q, int):
        raise TypeError("phi_q must be an integer")
    if isinstance(residue_count, bool) or not isinstance(residue_count, int):
        raise TypeError("residue_count must be an integer")
    if phi_q <= 0:
        raise ValueError("phi_q must be positive")
    if not 0 < residue_count < phi_q:
        raise ValueError("residue_count must satisfy 0 < M < phi_q")
    return phi_q, residue_count


def _positive_mpf(value: object, name: str) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _nonnegative_mpf(value: object, name: str) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def pap_near_budget() -> mp.mpf:
    """Return the printed relative near-branch budget ``exp(-2)``."""

    return mp.exp(-mp.mpf(PAP_NEAR_BUDGET_EXPONENT.numerator) /
                  PAP_NEAR_BUDGET_EXPONENT.denominator)


def total_character_energy(phi_q: int, residue_count: int) -> int:
    """Return ``sum_chi |C_chi(A)|^2 = phi(q) * M``.

    The identity assumes ``M`` distinct reduced residues and a complete set
    of Dirichlet characters modulo ``q``.  The finite-group orthogonality
    theorem itself is documented separately rather than asserted by this
    arithmetic helper.
    """

    phi_q, residue_count = _population(phi_q, residue_count)
    return phi_q * residue_count


def principal_character_energy(residue_count: int) -> int:
    """Return ``|C_chi0(A)|^2 = M^2`` for a reduced-residue subset."""

    if isinstance(residue_count, bool) or not isinstance(residue_count, int):
        raise TypeError("residue_count must be an integer")
    if residue_count <= 0:
        raise ValueError("residue_count must be positive")
    return residue_count**2


def nonprincipal_character_energy(phi_q: int, residue_count: int) -> int:
    """Return the exact nonprincipal energy ``M * (phi(q) - M)``."""

    phi_q, residue_count = _population(phi_q, residue_count)
    return residue_count * (phi_q - residue_count)


def legacy_full_moment_budget(
    phi_q: int,
    residue_count: int,
    y: object,
    epsilon: object,
) -> mp.mpf:
    """Return Theory 76's sufficient all-character second-moment budget."""

    phi_q, residue_count = _population(phi_q, residue_count)
    y_mp = _positive_mpf(y, "y")
    epsilon_mp = _positive_mpf(epsilon, "epsilon")
    return epsilon_mp**2 * residue_count * y_mp**2 / phi_q


def principal_separated_nonprincipal_budget(
    phi_q: int,
    residue_count: int,
    y: object,
    epsilon: object,
    principal_relative_error: object = 0,
) -> mp.mpf:
    """Return the exact Cauchy-sufficient nonprincipal moment budget.

    If ``|Z_chi0(Y)| <= delta0 * Y`` and ``delta0 < epsilon``, it is enough
    that

    ``sum_(chi != chi0) |Z_chi(Y)|^2``
    ``<= (epsilon-delta0)^2 * M * Y^2 / (phi(q)-M)``.

    This is only a terminal implication.  No analytic bound for the left
    side is supplied here.
    """

    phi_q, residue_count = _population(phi_q, residue_count)
    y_mp = _positive_mpf(y, "y")
    epsilon_mp = _positive_mpf(epsilon, "epsilon")
    delta_mp = _nonnegative_mpf(
        principal_relative_error, "principal_relative_error"
    )
    if delta_mp >= epsilon_mp:
        raise ValueError("principal_relative_error must be less than epsilon")
    return (
        (epsilon_mp - delta_mp) ** 2
        * residue_count
        * y_mp**2
        / (phi_q - residue_count)
    )


def separated_over_legacy_budget_ratio(
    phi_q: int,
    residue_count: int,
    epsilon: object,
    principal_relative_error: object = 0,
) -> mp.mpf:
    """Return the exact separated-budget / Theory-76-budget ratio."""

    phi_q, residue_count = _population(phi_q, residue_count)
    epsilon_mp = _positive_mpf(epsilon, "epsilon")
    delta_mp = _nonnegative_mpf(
        principal_relative_error, "principal_relative_error"
    )
    if delta_mp >= epsilon_mp:
        raise ValueError("principal_relative_error must be less than epsilon")
    return (
        mp.mpf(phi_q)
        / (phi_q - residue_count)
        * ((epsilon_mp - delta_mp) / epsilon_mp) ** 2
    )


def cauchy_alignment_witness(energy: int, scale: Fraction) -> tuple[Fraction, Fraction]:
    """Return both sides of the scalar equality case for Cauchy's bound.

    An error vector proportional to the conjugate coefficient vector has
    squared inner product ``(energy*scale)^2`` and Cauchy RHS
    ``energy*(energy*scale^2)``.  Equal outputs show that total energy alone
    cannot improve the universal constant.
    """

    if isinstance(energy, bool) or not isinstance(energy, int):
        raise TypeError("energy must be an integer")
    if energy <= 0:
        raise ValueError("energy must be positive")
    if not isinstance(scale, Fraction):
        raise TypeError("scale must be fractions.Fraction")
    lhs = (energy * scale) ** 2
    rhs = energy * (energy * scale**2)
    return lhs, rhs


def hooley_zero_free_boundary(d: int) -> Fraction:
    """Return ``1/2 + 1/(2d)`` for the power regime ``q=Y^(1/d)``.

    Fiorilli--Martin Proposition 2.2 shows that a uniform Hooley-sized full
    variance bound in ``q about Y^(1/d)`` would imply nonvanishing to the
    right of this line.  This function records only the exact substitution.
    """

    if isinstance(d, bool) or not isinstance(d, int):
        raise TypeError("d must be an integer")
    if d <= 0:
        raise ValueError("d must be positive")
    return Fraction(d + 1, 2 * d)


@dataclass(frozen=True)
class RestrictedVarianceDiagnostic:
    toy_phi_q: int
    toy_residue_count: int
    total_character_energy: int
    principal_character_energy: int
    nonprincipal_character_energy: int
    energy_decomposition_exact: bool
    separated_over_legacy_ratio_delta0_zero: str
    separated_over_legacy_ratio_delta0_epsilon_over_10: str
    cauchy_total_energy_constant_improvable_without_extra_structure: bool
    d_min_zero_free_boundary_fraction: str
    d_max_zero_free_boundary_fraction: str
    maier_formula_i_uses_aggregate_prime_mass: bool
    maier_formula_ii_remains_independent_pair_bound: bool
    fully_numerical_fixed_primorial_variance_drop_in_identified: bool
    direct_weighted_correlation_theorem_identified: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> RestrictedVarianceDiagnostic:
    """Build a deterministic fail-closed diagnostic for the source audit."""

    phi_q = 92_160
    residue_count = 17
    with mp.workdps(max(mp.mp.dps, 120)):
        epsilon = pap_near_budget()
        total = total_character_energy(phi_q, residue_count)
        principal = principal_character_energy(residue_count)
        nonprincipal = nonprincipal_character_energy(phi_q, residue_count)
        ratio_zero = separated_over_legacy_budget_ratio(
            phi_q, residue_count, epsilon, 0
        )
        ratio_tenth = separated_over_legacy_budget_ratio(
            phi_q, residue_count, epsilon, epsilon / 10
        )
        left, right = cauchy_alignment_witness(nonprincipal, Fraction(7, 13))

        return RestrictedVarianceDiagnostic(
            toy_phi_q=phi_q,
            toy_residue_count=residue_count,
            total_character_energy=total,
            principal_character_energy=principal,
            nonprincipal_character_energy=nonprincipal,
            energy_decomposition_exact=(total == principal + nonprincipal),
            separated_over_legacy_ratio_delta0_zero=mp.nstr(ratio_zero, 80),
            separated_over_legacy_ratio_delta0_epsilon_over_10=mp.nstr(
                ratio_tenth, 80
            ),
            cauchy_total_energy_constant_improvable_without_extra_structure=(
                left != right
            ),
            d_min_zero_free_boundary_fraction=str(hooley_zero_free_boundary(D_MIN)),
            d_max_zero_free_boundary_fraction=str(hooley_zero_free_boundary(D_MAX)),
            maier_formula_i_uses_aggregate_prime_mass=True,
            maier_formula_ii_remains_independent_pair_bound=True,
            fully_numerical_fixed_primorial_variance_drop_in_identified=False,
            direct_weighted_correlation_theorem_identified=False,
            pap_11_closed=False,
            dep_r09_closed=False,
            fixed_2e_minus_17_independently_certified=False,
            numerical_x_cert_ready=False,
            threshold_calculator_ready=False,
            actual_prime_computation_run=False,
            source_theorem_local_axiom_used=False,
            proof_escape_used=False,
        )


def diagnostic_as_dict() -> dict[str, object]:
    """Return the diagnostic in a JSON-serializable form."""

    return asdict(build_diagnostic())
