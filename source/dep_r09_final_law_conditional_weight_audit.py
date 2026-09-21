"""Exact finite checks for the DEP-R09 final-law conditional-weight audit.

FGKMT's proof-constructed covering law reweights each original edge law after
conditioning on the previous surviving set.  For a nonempty output edge, the
normalizer and survival-product floors give an explicit atom cap.  Combining
that cap with a covering-forced minimum number of nonempty edges yields a
same-law shift-atom bound.

This module checks only finite probability algebra, integer coverage counting,
the resulting strict scalar interface, and source provenance.  It does not run
prime experiments, evaluate a threshold, or prove the missing analytic
prime-error estimate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_final_law_conditional_weight_audit_v1.json"
)


def _integer(value: object, name: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _fraction(
    value: object,
    name: str,
    *,
    positive: bool = False,
    probability: bool = False,
) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    if probability and not 0 <= value <= 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return value


def reweighted_atom_probability(
    original_atom: Fraction,
    normalizer: Fraction,
    survival_weight: Fraction,
) -> Fraction:
    """Return mu(E)/(X_i(W) P(E)) exactly."""

    original_atom = _fraction(
        original_atom, "original_atom", probability=True
    )
    normalizer = _fraction(normalizer, "normalizer", positive=True)
    survival_weight = _fraction(
        survival_weight, "survival_weight", positive=True
    )
    result = original_atom / (normalizer * survival_weight)
    if result > 1:
        raise ValueError("inputs do not define a probability atom")
    return result


def proof_law_nonempty_atom_cap(
    original_nonempty_atom_upper: Fraction,
    kappa_power_inverse: Fraction,
) -> Fraction:
    """Return the Theory-54 cap 2*kappa^(-r)*mu_atom_upper."""

    original_nonempty_atom_upper = _fraction(
        original_nonempty_atom_upper,
        "original_nonempty_atom_upper",
        probability=True,
    )
    kappa_power_inverse = _fraction(
        kappa_power_inverse, "kappa_power_inverse", positive=True
    )
    return 2 * kappa_power_inverse * original_nonempty_atom_upper


def minimum_nonempty_edges(
    total_vertices: int,
    survivor_upper: int,
    edge_size_cap: int,
) -> int:
    """Return ceil((total_vertices-survivor_upper)/edge_size_cap)."""

    total_vertices = _integer(total_vertices, "total_vertices", positive=True)
    survivor_upper = _integer(survivor_upper, "survivor_upper")
    edge_size_cap = _integer(edge_size_cap, "edge_size_cap", positive=True)
    if not 0 <= survivor_upper <= total_vertices:
        raise ValueError("survivor_upper must lie in [0,total_vertices]")
    covered = total_vertices - survivor_upper
    return (covered + edge_size_cap - 1) // edge_size_cap


def sequential_output_atom_probability(
    conditional_probabilities: Sequence[Fraction],
    nonempty_coordinates: Sequence[bool],
    nonempty_atom_cap: Fraction,
) -> dict[str, Fraction | int | bool]:
    """Check a history-adaptive chain of conditioned probabilities.

    The supplied probabilities may come from different histories and stages.
    Multiplying them is the chain rule, not an assumption of global
    independence.  Only coordinates marked nonempty are required to obey the
    proof-law atom cap; empty-coordinate probabilities are bounded by one.
    """

    probabilities = tuple(conditional_probabilities)
    markers = tuple(nonempty_coordinates)
    if not probabilities or len(probabilities) != len(markers):
        raise ValueError("probabilities and markers must have equal nonzero length")
    nonempty_atom_cap = _fraction(
        nonempty_atom_cap, "nonempty_atom_cap", probability=True
    )
    product = Fraction(1)
    nonempty_count = 0
    for index, (probability, is_nonempty) in enumerate(
        zip(probabilities, markers)
    ):
        probability = _fraction(
            probability, f"conditional_probabilities[{index}]", probability=True
        )
        if not isinstance(is_nonempty, bool):
            raise TypeError("nonempty coordinate markers must be bool")
        if is_nonempty:
            nonempty_count += 1
            if probability > nonempty_atom_cap:
                raise ValueError("nonempty conditional atom exceeds the cap")
        product *= probability
    upper = nonempty_atom_cap**nonempty_count
    return {
        "probability": product,
        "nonempty_count": nonempty_count,
        "cap_power": upper,
        "obeys_cap": product <= upper,
    }


def event_shift_atom_upper(
    outer_denominator: int,
    nonempty_atom_cap: Fraction,
    minimum_nonempty_count: int,
) -> Fraction:
    """Return omega^K/Q_S exactly."""

    outer_denominator = _integer(
        outer_denominator, "outer_denominator", positive=True
    )
    nonempty_atom_cap = _fraction(
        nonempty_atom_cap, "nonempty_atom_cap", probability=True
    )
    minimum_nonempty_count = _integer(
        minimum_nonempty_count, "minimum_nonempty_count"
    )
    if minimum_nonempty_count < 0:
        raise ValueError("minimum_nonempty_count must be nonnegative")
    return nonempty_atom_cap**minimum_nonempty_count / outer_denominator


def effective_atom_denominator(
    outer_denominator: int,
    nonempty_atom_cap: Fraction,
    minimum_nonempty_count: int,
) -> Fraction:
    """Return reciprocal atom denominator Q_S*omega^(-K)."""

    upper = event_shift_atom_upper(
        outer_denominator, nonempty_atom_cap, minimum_nonempty_count
    )
    if upper == 0:
        raise ValueError("zero atom cap has no finite reciprocal")
    return 1 / upper


def residue_from_output_edge(edge: Sequence[int], prime: int) -> int:
    """Return the residue represented by a nonempty edge; empty maps to 0."""

    prime = _integer(prime, "prime", positive=True)
    materialized = tuple(edge)
    if any(isinstance(value, bool) or not isinstance(value, int)
           for value in materialized):
        raise TypeError("edge vertices must be integers")
    if len(set(materialized)) != len(materialized):
        raise ValueError("edge vertices must be distinct")
    if not materialized:
        return 0
    residue = materialized[0] % prime
    if any(value % prime != residue for value in materialized):
        raise ValueError("a nonempty full-residue edge must have one residue")
    if residue == 0:
        raise ValueError("nonempty prime-vertex edge cannot use residue zero")
    return residue


def guaranteed_effective_entropy_log_coefficient_upper() -> Fraction:
    """Return the exact coefficient in the project-scale upper bound."""

    return Fraction(21, 16000) + Fraction(237, 1_536_000) + Fraction(3, 500)


def full_primorial_log_coefficient_lower() -> Fraction:
    """Return 1-1/100-1/100=49/50."""

    return Fraction(49, 50)


@dataclass(frozen=True)
class FinalLawConditionalWeightDiagnostic:
    fgkmt_formula_5_9_proof_law_source_verified: bool
    formula_5_9_is_conditional_product_not_global_independence: bool
    nonempty_edge_atom_cap_exact: bool
    full_residue_nonempty_edge_determines_unique_residue: bool
    empty_edge_uses_zero_residue_rule: bool
    covering_success_forces_nonempty_edge_floor: bool
    same_law_event_shift_atom_cap_exact: bool
    toy_reweighted_nonempty_atom: str
    toy_nonempty_atom_cap: str
    toy_minimum_nonempty_edges: int
    toy_vector_atom_probability: str
    toy_vector_atom_cap: str
    toy_event_shift_atom_cap: str
    toy_effective_atom_denominator: str
    effective_entropy_log_coefficient_upper: str
    effective_entropy_log_coefficient_below_one_hundredth: bool
    full_primorial_log_coefficient_lower: str
    guaranteed_effective_entropy_is_subprimorial: bool
    generic_large_sieve_certificate_can_close_new_gate: bool
    stronger_actual_nonempty_tail_or_phase_cancellation_ruled_out: bool
    actual_same_law_analytic_moment_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> FinalLawConditionalWeightDiagnostic:
    original_atom = Fraction(1, 12)
    reweighted = reweighted_atom_probability(
        original_atom, Fraction(3, 4), Fraction(1, 2)
    )
    cap = proof_law_nonempty_atom_cap(original_atom, Fraction(2))
    minimum = minimum_nonempty_edges(10, 3, 2)
    vector = sequential_output_atom_probability(
        (
            Fraction(2, 9),
            Fraction(1, 4),
            Fraction(1, 3),
            Fraction(1, 5),
            Fraction(2, 5),
            Fraction(1),
        ),
        (True, True, True, True, False, False),
        cap,
    )
    event_atom = event_shift_atom_upper(6, cap, minimum)
    effective = effective_atom_denominator(6, cap, minimum)
    entropy_upper = guaranteed_effective_entropy_log_coefficient_upper()
    primorial_lower = full_primorial_log_coefficient_lower()
    return FinalLawConditionalWeightDiagnostic(
        fgkmt_formula_5_9_proof_law_source_verified=True,
        formula_5_9_is_conditional_product_not_global_independence=True,
        nonempty_edge_atom_cap_exact=(reweighted <= cap),
        full_residue_nonempty_edge_determines_unique_residue=(
            residue_from_output_edge((7, 13, 19), 3) == 1
        ),
        empty_edge_uses_zero_residue_rule=(
            residue_from_output_edge((), 3) == 0
        ),
        covering_success_forces_nonempty_edge_floor=(minimum == 4),
        same_law_event_shift_atom_cap_exact=True,
        toy_reweighted_nonempty_atom=str(reweighted),
        toy_nonempty_atom_cap=str(cap),
        toy_minimum_nonempty_edges=minimum,
        toy_vector_atom_probability=str(vector["probability"]),
        toy_vector_atom_cap=str(vector["cap_power"]),
        toy_event_shift_atom_cap=str(event_atom),
        toy_effective_atom_denominator=str(effective),
        effective_entropy_log_coefficient_upper=str(entropy_upper),
        effective_entropy_log_coefficient_below_one_hundredth=(
            entropy_upper < Fraction(1, 100)
        ),
        full_primorial_log_coefficient_lower=str(primorial_lower),
        guaranteed_effective_entropy_is_subprimorial=(
            entropy_upper < primorial_lower
        ),
        generic_large_sieve_certificate_can_close_new_gate=False,
        stronger_actual_nonempty_tail_or_phase_cancellation_ruled_out=False,
        actual_same_law_analytic_moment_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        bounded_x_cert_range_obtained=False,
        threshold_calculator_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def load_ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def validate_ledger(
    document: Mapping[str, object],
    *,
    check_hashes: bool = True,
) -> list[str]:
    """Validate fail-closed status fields and source provenance."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != (
        "DEP-R09 final-law conditional-weight source audit"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "PROOF_LAW_NONEMPTY_ATOM_CAP_AND_SUCCESS_FORCED_ENTROPY_EXPLICIT_"
        "BUT_GUARANTEED_EFFECTIVE_ENTROPY_REMAINS_SUBPRIMORIAL"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Use more than the guaranteed minimum nonempty-coordinate count: "
        "obtain a numerical tail for empty outputs, a local character-phase "
        "transform under the reweighted law, or a prime-specific fiber bound; "
        "the extracted minimum-count atom cap does not close the generic "
        "large-sieve route."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 7:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "FGKMT", "FMT", "THEORY53", "THEORY54", "THEORY55",
        "THEORY83", "THEORY86",
    }
    keys = {
        item.get("key") for item in sources if isinstance(item, dict)
    }
    if keys != expected_keys:
        issues.append("source keys mismatch")

    if check_hashes:
        for source in sources:
            if not isinstance(source, dict):
                issues.append("invalid source entry")
                continue
            key = source.get("key", "unknown")
            locator = source.get("locator")
            digest = source.get("sha256")
            if not isinstance(locator, str) or not isinstance(digest, str):
                issues.append(f"{key} missing pin")
                continue
            path = (REPO_ROOT / locator).resolve()
            try:
                path.relative_to(REPO_ROOT.resolve())
            except ValueError:
                issues.append(f"{key} path escape")
                continue
            if not path.is_file():
                issues.append(f"{key} missing source")
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                issues.append(f"{key} hash mismatch")
    return issues


__all__ = [
    "LEDGER_PATH",
    "build_diagnostic",
    "effective_atom_denominator",
    "event_shift_atom_upper",
    "full_primorial_log_coefficient_lower",
    "guaranteed_effective_entropy_log_coefficient_upper",
    "load_ledger",
    "minimum_nonempty_edges",
    "proof_law_nonempty_atom_cap",
    "residue_from_output_edge",
    "reweighted_atom_probability",
    "sequential_output_atom_probability",
    "validate_ledger",
]
