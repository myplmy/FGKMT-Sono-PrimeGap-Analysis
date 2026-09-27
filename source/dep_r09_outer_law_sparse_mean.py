"""Exact finite checks for the DEP-R09 outer-law sparse-mean reduction.

The helper verifies the weighted expectation/covariance identity supplied by
the outer one/two-point survival law, its L-infinity normalization, and the
worst-case cost of an adaptive bounded deletion.  It performs no prime or
threshold computation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import itertools
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
    / "Sono_FMT_DEPR09_outer_law_sparse_mean_v1.json"
)


def _fraction(value: object, name: str, *, probability: bool = False) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if probability and not 0 <= value <= 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return value


def weighted_moments_from_table(
    weights: Sequence[Fraction],
    probability_table: Mapping[tuple[bool, ...], Fraction],
) -> dict[str, object]:
    """Return exact first/second moments and one/two-point probabilities."""

    weights = tuple(weights)
    if not weights:
        raise ValueError("weights must be nonempty")
    for index, weight in enumerate(weights):
        _fraction(weight, f"weight[{index}]")
    expected_states = set(itertools.product((False, True), repeat=len(weights)))
    if set(probability_table) != expected_states:
        raise ValueError("probability table must contain every Boolean state")
    total_mass = Fraction(0)
    expectation = Fraction(0)
    second_moment = Fraction(0)
    singles = [Fraction(0) for _ in weights]
    pairs = {
        (i, j): Fraction(0)
        for i in range(len(weights))
        for j in range(i + 1, len(weights))
    }
    for state, mass in probability_table.items():
        mass = _fraction(mass, f"mass[{state}]", probability=True)
        total_mass += mass
        value = sum(
            (weight for weight, survives in zip(weights, state) if survives),
            Fraction(0),
        )
        expectation += mass * value
        second_moment += mass * value**2
        for index, survives in enumerate(state):
            if survives:
                singles[index] += mass
        for pair in pairs:
            if state[pair[0]] and state[pair[1]]:
                pairs[pair] += mass
    if total_mass != 1:
        raise ValueError("probability masses must sum to one")
    return {
        "expectation": expectation,
        "second_moment": second_moment,
        "variance": second_moment - expectation**2,
        "singles": tuple(singles),
        "pairs": pairs,
    }


def common_shock_table(
    count: int,
    low_probability: Fraction,
    high_probability: Fraction,
) -> dict[tuple[bool, ...], Fraction]:
    """Return a fair mixture of two iid Bernoulli product laws."""

    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 10:
        raise ValueError("count must lie in 1..10")
    low = _fraction(low_probability, "low_probability", probability=True)
    high = _fraction(high_probability, "high_probability", probability=True)
    table: dict[tuple[bool, ...], Fraction] = {}
    for state in itertools.product((False, True), repeat=count):
        mass = Fraction(0)
        for theta in (low, high):
            branch = Fraction(1, 2)
            for survives in state:
                branch *= theta if survives else 1 - theta
            mass += branch
        table[state] = mass
    return table


def weighted_outer_variance_upper(
    weights: Sequence[Fraction],
    sigma: Fraction,
    relative_pair_error: Fraction,
) -> Fraction:
    """Return the exact entrywise covariance certificate.

    Premises are P(X_i=1)=sigma and
    abs(P(X_i=X_j=1)-sigma^2)<=epsilon*sigma^2.
    """

    weights = tuple(weights)
    if not weights:
        raise ValueError("weights must be nonempty")
    sigma = _fraction(sigma, "sigma", probability=True)
    epsilon = _fraction(relative_pair_error, "relative_pair_error")
    if epsilon < 0:
        raise ValueError("relative_pair_error must be nonnegative")
    l1 = Fraction(0)
    l2 = Fraction(0)
    for index, weight in enumerate(weights):
        weight = _fraction(weight, f"weight[{index}]")
        l1 += abs(weight)
        l2 += weight**2
    return sigma * (1 - sigma) * l2 + epsilon * sigma**2 * (l1**2 - l2)


def normalized_outer_variance_upper(
    pointwise_weight_ratio: Fraction,
    sigma: Fraction,
    relative_pair_error: Fraction,
    vertex_count: int,
) -> Fraction:
    """Return Var/(sigma*N*U)^2 using abs(B_q)<=L*U."""

    ratio = _fraction(pointwise_weight_ratio, "pointwise_weight_ratio")
    sigma = _fraction(sigma, "sigma", probability=True)
    epsilon = _fraction(relative_pair_error, "relative_pair_error")
    if ratio < 0 or sigma <= 0 or epsilon < 0:
        raise ValueError("invalid variance parameters")
    if isinstance(vertex_count, bool) or not isinstance(vertex_count, int):
        raise TypeError("vertex_count must be an integer")
    if vertex_count < 1:
        raise ValueError("vertex_count must be positive")
    count = Fraction(vertex_count)
    return ratio**2 * (
        (1 - sigma) / (sigma * count)
        + epsilon * (count - 1) / count
    )


def weighted_fluctuation_failure_upper(
    pointwise_weight_ratio: Fraction,
    sigma: Fraction,
    relative_pair_error: Fraction,
    vertex_count: int,
    fluctuation_ratio: Fraction,
) -> Fraction:
    fluctuation = _fraction(fluctuation_ratio, "fluctuation_ratio")
    if fluctuation <= 0:
        raise ValueError("fluctuation_ratio must be positive")
    raw = normalized_outer_variance_upper(
        pointwise_weight_ratio, sigma, relative_pair_error, vertex_count
    ) / fluctuation**2
    return min(Fraction(1), raw)


def selected_count_scale_lower(
    count_relative_error: Fraction,
    deletion_fraction: Fraction,
) -> Fraction:
    eta = _fraction(count_relative_error, "count_relative_error")
    deletion = _fraction(deletion_fraction, "deletion_fraction")
    if not 0 <= eta < 1 or not 0 <= deletion < 1:
        raise ValueError("count and deletion fractions must lie in [0,1)")
    return (1 - deletion) * (1 - eta)


def selected_mean_ratio_upper(
    fixed_mean_ratio: Fraction,
    fluctuation_ratio: Fraction,
    pointwise_weight_ratio: Fraction,
    count_relative_error: Fraction,
    deletion_fraction: Fraction,
) -> Fraction:
    """Return the bound for abs(sum_(q in V) B_q)/(abs(V)*U)."""

    fixed_mean = _fraction(fixed_mean_ratio, "fixed_mean_ratio")
    fluctuation = _fraction(fluctuation_ratio, "fluctuation_ratio")
    pointwise = _fraction(pointwise_weight_ratio, "pointwise_weight_ratio")
    eta = _fraction(count_relative_error, "count_relative_error")
    deletion = _fraction(deletion_fraction, "deletion_fraction")
    if fixed_mean < 0 or fluctuation < 0 or pointwise < 0:
        raise ValueError("mean and envelope ratios must be nonnegative")
    scale = selected_count_scale_lower(eta, deletion)
    numerator = fixed_mean + fluctuation + pointwise * deletion * (1 + eta)
    return numerator / scale


def outer_good_mass_lower(*failure_probabilities: Fraction) -> Fraction:
    total = Fraction(0)
    for index, probability in enumerate(failure_probabilities):
        probability = _fraction(
            probability, f"failure_probability[{index}]", probability=True
        )
        total += probability
    return max(Fraction(0), 1 - total)


def deletion_triangle_bound(
    surviving_weights: Sequence[Fraction],
    deleted_indices: Sequence[int],
) -> dict[str, Fraction]:
    """Check the deterministic adaptive-deletion triangle inequality."""

    weights = tuple(surviving_weights)
    if not weights:
        raise ValueError("surviving_weights must be nonempty")
    for index, weight in enumerate(weights):
        _fraction(weight, f"weight[{index}]")
    deleted = tuple(deleted_indices)
    if len(set(deleted)) != len(deleted):
        raise ValueError("deleted_indices must be duplicate-free")
    if any(index < 0 or index >= len(weights) for index in deleted):
        raise ValueError("deleted index out of range")
    deleted_set = set(deleted)
    before = sum(weights, Fraction(0))
    removed = sum((weights[index] for index in deleted), Fraction(0))
    after = sum(
        (weight for index, weight in enumerate(weights) if index not in deleted_set),
        Fraction(0),
    )
    upper = abs(before) + sum((abs(weights[index]) for index in deleted), Fraction(0))
    if after != before - removed or abs(after) > upper:
        raise AssertionError("deletion triangle inequality failed")
    return {"before": before, "removed": removed, "after": after, "upper": upper}


@dataclass(frozen=True)
class OuterLawSparseMeanDiagnostic:
    weighted_expectation_exact: bool
    weighted_variance_certificate_valid: bool
    signed_weight_fixture_checked: bool
    adaptive_deletion_triangle_exact: bool
    project_pointwise_ratio: str
    project_pair_error: str
    project_count_relative_error_at_b_2000: str
    project_deletion_fraction_at_b_2000: str
    project_selected_count_scale_at_b_2000: str
    outer_randomization_removes_fixed_mean: bool
    outer_fluctuation_parameterized_explicit: bool
    adaptive_deletion_parameterized_explicit: bool
    fixed_qprime_mean_closed: bool
    prescribed_primorial_source_drop_in_identified: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> OuterLawSparseMeanDiagnostic:
    weights = (Fraction(2), Fraction(-1), Fraction(3))
    table = common_shock_table(3, Fraction(1, 4), Fraction(3, 4))
    moments = weighted_moments_from_table(weights, table)
    sigma = Fraction(1, 2)
    pair = Fraction(5, 16)
    epsilon = abs(pair - sigma**2) / sigma**2
    certificate = weighted_outer_variance_upper(weights, sigma, epsilon)
    deletion = deletion_triangle_bound(
        (Fraction(5), Fraction(-4), Fraction(2)), (0,)
    )
    b = 2000
    eta = Fraction(1, b**3)
    deletion_fraction = Fraction(8000, b**2)
    return OuterLawSparseMeanDiagnostic(
        weighted_expectation_exact=(
            moments["expectation"] == sigma * sum(weights, Fraction(0))
        ),
        weighted_variance_certificate_valid=(moments["variance"] <= certificate),
        signed_weight_fixture_checked=True,
        adaptive_deletion_triangle_exact=(abs(deletion["after"]) <= deletion["upper"]),
        project_pointwise_ratio="11/5",
        project_pair_error="2*a^(-17)",
        project_count_relative_error_at_b_2000=str(eta),
        project_deletion_fraction_at_b_2000=str(deletion_fraction),
        project_selected_count_scale_at_b_2000=str(
            selected_count_scale_lower(eta, deletion_fraction)
        ),
        outer_randomization_removes_fixed_mean=False,
        outer_fluctuation_parameterized_explicit=True,
        adaptive_deletion_parameterized_explicit=True,
        fixed_qprime_mean_closed=False,
        prescribed_primorial_source_drop_in_identified=False,
        pap_11_closed=False,
        dep_r09_closed=False,
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
    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != (
        "DEP-R09 outer-law sparse centered-mean reduction"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "OUTER_FLUCTUATION_AND_ADAPTIVE_DELETION_PARAMETERIZED_EXPLICIT_"
        "BUT_FIXED_QPRIME_CENTERED_MEAN_REMAINS_OPEN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Obtain a fully numerical bound for the deterministic fixed-Q-prime "
        "mean D_Q; outer randomization and bounded adaptive deletion add only "
        "explicit absorbable costs and do not remove this mean."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 10:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "FGKMT",
        "THEORY49",
        "THEORY51",
        "THEORY53",
        "THEORY92",
        "MAYNARD_I",
        "MAYNARD_III",
        "STADLMANN",
        "KMT",
        "LEUNG",
    }
    keys = {item.get("key") for item in sources if isinstance(item, dict)}
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
    "common_shock_table",
    "deletion_triangle_bound",
    "load_ledger",
    "normalized_outer_variance_upper",
    "outer_good_mass_lower",
    "selected_count_scale_lower",
    "selected_mean_ratio_upper",
    "validate_ledger",
    "weighted_fluctuation_failure_upper",
    "weighted_moments_from_table",
    "weighted_outer_variance_upper",
]
