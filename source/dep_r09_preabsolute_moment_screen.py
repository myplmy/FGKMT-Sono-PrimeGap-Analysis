"""Source-screen arithmetic for the DEP-R09 pre-absolute-value routes.

This module performs only elementary normalization and high-precision
diagnostics for published explicit bounds.  It does not prove any cited
analytic theorem, does not assert a new prime-distribution estimate, and does
not certify PAP-11, the fixed Sono coefficient, or a numerical ``X_cert``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

import mpmath as mp


D_CAPACITY_ENDPOINT = 186
PAP_NEAR_BUDGET_EXPONENT = Fraction(2, 1)

AKBARY_HAMBROOK_C0_PRINTED_DECIMAL = "48.83236"
SEDUNOVA_C1 = Fraction(211, 5)  # 42.2

BENNETT_LARGE_Q_THRESHOLD = 100_000
BENNETT_CUTOFF_COEFFICIENT = Fraction(3, 100)  # 0.03
BENNETT_UNIFORM_C_PSI = Fraction(1, 160)

# The first primorial strictly above 10^5.  It is a concrete Maier-modulus
# checkpoint, not a claim that all later constants equal this one.
FIRST_PRIMORIAL_ABOVE_1E5 = 510_510
FIRST_PRIMORIAL_ABOVE_1E5_PHI = 92_160


def _positive_mpf(value: object, name: str) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _fraction_mpf(value: Fraction) -> mp.mpf:
    if not isinstance(value, Fraction):
        raise TypeError("expected fractions.Fraction")
    return mp.mpf(value.numerator) / value.denominator


def pap_near_budget() -> mp.mpf:
    """Return Sono's printed nonprincipal relative-error budget ``exp(-2)``."""

    return mp.exp(-_fraction_mpf(PAP_NEAR_BUDGET_EXPONENT))


def akbary_hambrook_l1_floor_relative_to_x(x: object = 4) -> mp.mpf:
    """Return the unavoidable printed ``4*c0*log(x)^(7/2)`` RHS term.

    The decimal for ``c0`` is the truncated printed value, so this is used as
    a conservative high-precision diagnostic of the theorem's certificate,
    not as a directed interval proof of the transcendental constant.
    """

    x_mp = _positive_mpf(x, "x")
    if x_mp < 4:
        raise ValueError("Akbary--Hambrook Theorem 1.2 requires x >= 4")
    c0 = mp.mpf(AKBARY_HAMBROOK_C0_PRINTED_DECIMAL)
    return 4 * c0 * mp.power(mp.log(x_mp), mp.mpf(7) / 2)


def sedunova_l1_floor_relative_to_x(x: object = 4) -> mp.mpf:
    """Return the ``Q1=1`` main RHS term in Sedunova Theorem 1.2.

    With ``Q1=1`` the theorem includes the small-prime-factor (hence
    primorial) moduli, but the displayed upper certificate already contains
    ``14*c1*x*log(x)^(7/2)``.
    """

    x_mp = _positive_mpf(x, "x")
    if x_mp < 4:
        raise ValueError("Sedunova Theorem 1.2 requires x >= 4")
    return (
        14
        * _fraction_mpf(SEDUNOVA_C1)
        * mp.power(mp.log(x_mp), mp.mpf(7) / 2)
    )


def bennett_required_d_for_maier_scale(q: object) -> mp.mpf:
    """Normalize the large-q source cutoff at the Maier scale ``Y=q^d``.

    Bennett et al. use ``Y >= exp(0.03*sqrt(q)*log(q)^3)`` for ``q>10^5``.
    Since ``log(Y)=d*log(q)``, the necessary normalized condition is
    ``d >= 0.03*sqrt(q)*log(q)^2``.
    """

    q_mp = _positive_mpf(q, "q")
    if q_mp <= BENNETT_LARGE_Q_THRESHOLD:
        raise ValueError("large-q cutoff formula requires q > 100000")
    return (
        _fraction_mpf(BENNETT_CUTOFF_COEFFICIENT)
        * mp.sqrt(q_mp)
        * mp.log(q_mp) ** 2
    )


def bennett_relative_pap_error_envelope(
    q: object,
    phi_q: object,
    d: object,
) -> mp.mpf:
    """Convert the published absolute error envelope to PAP relative scale.

    The theorem gives ``|psi(Y;q,a)-Y/phi(q)| < cpsi*Y/log(Y)``.  At
    ``Y=q^d`` and with the published ``cpsi<=1/160`` envelope, the guaranteed
    relative error versus ``Y/phi(q)`` is
    ``phi(q)/(160*d*log(q))``.
    """

    q_mp = _positive_mpf(q, "q")
    phi_mp = _positive_mpf(phi_q, "phi_q")
    d_mp = _positive_mpf(d, "d")
    if phi_mp > q_mp:
        raise ValueError("phi_q cannot exceed q")
    return (
        _fraction_mpf(BENNETT_UNIFORM_C_PSI)
        * phi_mp
        / (d_mp * mp.log(q_mp))
    )


def bennett_required_cpsi_for_pap(
    q: object,
    phi_q: object,
    d: object,
    epsilon: object | None = None,
) -> mp.mpf:
    """Return the largest ``cpsi`` that would fit a chosen PAP error budget."""

    q_mp = _positive_mpf(q, "q")
    phi_mp = _positive_mpf(phi_q, "phi_q")
    d_mp = _positive_mpf(d, "d")
    epsilon_mp = pap_near_budget() if epsilon is None else _positive_mpf(
        epsilon, "epsilon"
    )
    if phi_mp > q_mp:
        raise ValueError("phi_q cannot exceed q")
    return epsilon_mp * d_mp * mp.log(q_mp) / phi_mp


def pointwise_second_moment_budget(
    x: object,
    phi_q: object,
    epsilon: object,
) -> mp.mpf:
    """Budget from Theory 75 for every residue class separately."""

    x_mp = _positive_mpf(x, "x")
    phi_mp = _positive_mpf(phi_q, "phi_q")
    epsilon_mp = _positive_mpf(epsilon, "epsilon")
    return epsilon_mp**2 * x_mp**2 / phi_mp


def aggregate_second_moment_budget(
    x: object,
    phi_q: object,
    admissible_residue_count: object,
    epsilon: object,
) -> mp.mpf:
    """Sufficient character-moment budget for Maier's aggregate columns.

    If ``M`` distinct admissible residues are summed before Cauchy, character
    orthogonality permits ``M`` times the pointwise budget.  The analytic
    theorem needed to supply this budget remains open.
    """

    count_mp = _positive_mpf(admissible_residue_count, "admissible_residue_count")
    return count_mp * pointwise_second_moment_budget(x, phi_q, epsilon)


def natural_variance_budget_ratio(
    q: object,
    phi_q: object,
    d: object,
    admissible_residue_count: object,
    epsilon: object,
    variance_multiplier: object = 1,
) -> mp.mpf:
    """Compare a hypothetical natural-order character moment to the budget.

    The conditional input is ``V <= C*phi(q)*Y*log(q)`` with ``Y=q^d``.
    The returned ratio is that RHS divided by the aggregate sufficient
    budget.  A value below one would be enough *if* a fully numerical,
    unconditional source theorem supplied the input; none is asserted here.
    """

    q_mp = _positive_mpf(q, "q")
    phi_mp = _positive_mpf(phi_q, "phi_q")
    d_mp = _positive_mpf(d, "d")
    count_mp = _positive_mpf(admissible_residue_count, "admissible_residue_count")
    epsilon_mp = _positive_mpf(epsilon, "epsilon")
    multiplier_mp = _positive_mpf(variance_multiplier, "variance_multiplier")
    y = mp.power(q_mp, d_mp)
    natural_upper = multiplier_mp * phi_mp * y * mp.log(q_mp)
    budget = aggregate_second_moment_budget(y, phi_mp, count_mp, epsilon_mp)
    return natural_upper / budget


@dataclass(frozen=True)
class PreAbsoluteMomentDiagnostic:
    pap_near_budget_exp_minus_2: str
    akbary_hambrook_l1_floor_at_x4_relative_to_x: str
    akbary_floor_over_budget: str
    sedunova_l1_floor_at_x4_relative_to_x: str
    sedunova_floor_over_budget: str
    bennett_required_d_just_above_1e5_lower_endpoint: str
    bennett_required_d_at_primorial_510510: str
    current_d_capacity_endpoint: int
    bennett_large_q_cutoff_overlaps_capacity: bool
    bennett_relative_error_envelope_q510510_d186: str
    bennett_relative_error_over_budget_q510510_d186: str
    bennett_required_cpsi_q510510_d186: str
    bennett_printed_uniform_cpsi: str
    aggregate_budget_over_pointwise_budget_for_m17: str
    maier_pointwise_columns_required_by_printed_proof: bool
    maier_final_count_uses_only_aggregate_admissible_columns: bool
    aggregate_second_moment_redesign_logically_sufficient: bool
    aggregate_second_moment_source_identified: bool
    unconditional_numerical_drop_in_found: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> PreAbsoluteMomentDiagnostic:
    """Build the fail-closed source-screen diagnostic at 120 decimal digits."""

    with mp.workdps(max(mp.mp.dps, 120)):
        budget = pap_near_budget()
        akbary_floor = akbary_hambrook_l1_floor_relative_to_x(4)
        sedunova_floor = sedunova_l1_floor_relative_to_x(4)
        q = FIRST_PRIMORIAL_ABOVE_1E5
        phi_q = FIRST_PRIMORIAL_ABOVE_1E5_PHI
        d = D_CAPACITY_ENDPOINT
        required_d_endpoint = (
            _fraction_mpf(BENNETT_CUTOFF_COEFFICIENT)
            * mp.sqrt(BENNETT_LARGE_Q_THRESHOLD)
            * mp.log(BENNETT_LARGE_Q_THRESHOLD) ** 2
        )
        required_d_primorial = bennett_required_d_for_maier_scale(q)
        relative_envelope = bennett_relative_pap_error_envelope(q, phi_q, d)
        required_cpsi = bennett_required_cpsi_for_pap(q, phi_q, d, budget)
        pointwise = pointwise_second_moment_budget(10, 4, budget)
        aggregate = aggregate_second_moment_budget(10, 4, 17, budget)

        def s(value: mp.mpf) -> str:
            return mp.nstr(value, 80)

        return PreAbsoluteMomentDiagnostic(
            pap_near_budget_exp_minus_2=s(budget),
            akbary_hambrook_l1_floor_at_x4_relative_to_x=s(akbary_floor),
            akbary_floor_over_budget=s(akbary_floor / budget),
            sedunova_l1_floor_at_x4_relative_to_x=s(sedunova_floor),
            sedunova_floor_over_budget=s(sedunova_floor / budget),
            bennett_required_d_just_above_1e5_lower_endpoint=s(required_d_endpoint),
            bennett_required_d_at_primorial_510510=s(required_d_primorial),
            current_d_capacity_endpoint=d,
            bennett_large_q_cutoff_overlaps_capacity=required_d_endpoint <= d,
            bennett_relative_error_envelope_q510510_d186=s(relative_envelope),
            bennett_relative_error_over_budget_q510510_d186=s(
                relative_envelope / budget
            ),
            bennett_required_cpsi_q510510_d186=s(required_cpsi),
            bennett_printed_uniform_cpsi=s(
                _fraction_mpf(BENNETT_UNIFORM_C_PSI)
            ),
            aggregate_budget_over_pointwise_budget_for_m17=s(
                aggregate / pointwise
            ),
            maier_pointwise_columns_required_by_printed_proof=True,
            maier_final_count_uses_only_aggregate_admissible_columns=True,
            aggregate_second_moment_redesign_logically_sufficient=True,
            aggregate_second_moment_source_identified=False,
            unconditional_numerical_drop_in_found=False,
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
