"""Exact finite algebra for the DEP-R09 same-law correlation gate.

This module checks only finite probability bookkeeping.  It does not prove a
Dirichlet-character moment estimate, FMT's analytic random construction, a
prime-distribution theorem, or a numerical ``X_cert``.  All probabilities and
moment bounds are exact :class:`fractions.Fraction` values.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_same_law_weighted_correlation_v1.json"
)


def _fraction(value: Fraction, name: str, *, positive: bool = False) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _unit_fraction(
    value: Fraction,
    name: str,
    *,
    strict_upper: bool = False,
) -> Fraction:
    value = _fraction(value, name)
    upper_ok = value < 1 if strict_upper else value <= 1
    if value < 0 or not upper_ok:
        interval = "[0,1)" if strict_upper else "[0,1]"
        raise ValueError(f"{name} must lie in {interval}")
    return value


@dataclass(frozen=True)
class InnerOutcome:
    """One conditional FMT covering outcome in a fixed outer fiber."""

    probability: Fraction
    inner_good: bool
    normalized_squared_badness: Fraction


@dataclass(frozen=True)
class OuterOutcome:
    """One first-stage residue outcome and its conditional inner law."""

    probability: Fraction
    outer_good: bool
    inner_outcomes: tuple[InnerOutcome, ...]


JointLaw = tuple[OuterOutcome, ...]


def _sum_exact(values: Iterable[Fraction]) -> Fraction:
    return sum(values, start=Fraction(0))


def validate_joint_law(law: JointLaw) -> None:
    """Fail closed unless ``law`` is an exact finite two-stage probability law."""

    if not isinstance(law, tuple) or not law:
        raise TypeError("law must be a nonempty tuple of OuterOutcome values")
    for outer_index, outer in enumerate(law):
        if not isinstance(outer, OuterOutcome):
            raise TypeError(f"law[{outer_index}] must be OuterOutcome")
        _unit_fraction(outer.probability, f"law[{outer_index}].probability")
        if not isinstance(outer.outer_good, bool):
            raise TypeError(f"law[{outer_index}].outer_good must be bool")
        if not isinstance(outer.inner_outcomes, tuple) or not outer.inner_outcomes:
            raise TypeError(
                f"law[{outer_index}].inner_outcomes must be a nonempty tuple"
            )
        for inner_index, inner in enumerate(outer.inner_outcomes):
            if not isinstance(inner, InnerOutcome):
                raise TypeError(
                    f"law[{outer_index}].inner_outcomes[{inner_index}] "
                    "must be InnerOutcome"
                )
            _unit_fraction(
                inner.probability,
                f"law[{outer_index}].inner_outcomes[{inner_index}].probability",
            )
            if not isinstance(inner.inner_good, bool):
                raise TypeError(
                    f"law[{outer_index}].inner_outcomes[{inner_index}]."
                    "inner_good must be bool"
                )
            badness = _fraction(
                inner.normalized_squared_badness,
                f"law[{outer_index}].inner_outcomes[{inner_index}]."
                "normalized_squared_badness",
            )
            if badness < 0:
                raise ValueError("normalized_squared_badness must be nonnegative")
        if _sum_exact(item.probability for item in outer.inner_outcomes) != 1:
            raise ValueError(
                f"conditional probabilities in outer fiber {outer_index} must sum to 1"
            )
    if _sum_exact(item.probability for item in law) != 1:
        raise ValueError("outer probabilities must sum to 1")


def outer_good_mass(law: JointLaw) -> Fraction:
    validate_joint_law(law)
    return _sum_exact(outer.probability for outer in law if outer.outer_good)


def exact_sieve_good_mass(law: JointLaw) -> Fraction:
    """Return ``P(outer-good and inner-good)`` under the same joint law."""

    validate_joint_law(law)
    return _sum_exact(
        outer.probability * inner.probability
        for outer in law
        if outer.outer_good
        for inner in outer.inner_outcomes
        if inner.inner_good
    )


def outer_good_moment_tower(law: JointLaw) -> Fraction:
    """Return ``E[1_outer-good W]`` by conditional expectation."""

    validate_joint_law(law)
    return _sum_exact(
        outer.probability
        * _sum_exact(
            inner.probability * inner.normalized_squared_badness
            for inner in outer.inner_outcomes
        )
        for outer in law
        if outer.outer_good
    )


def outer_good_moment_flat(law: JointLaw) -> Fraction:
    """Return the same moment by summing joint atoms directly."""

    validate_joint_law(law)
    return _sum_exact(
        outer.probability
        * inner.probability
        * inner.normalized_squared_badness
        for outer in law
        if outer.outer_good
        for inner in outer.inner_outcomes
    )


def conditional_outer_good_moment(law: JointLaw) -> Fraction:
    """Return ``E[W | outer-good]``; reject a zero-mass conditioning event."""

    mass = outer_good_mass(law)
    if mass == 0:
        raise ValueError("outer-good event must have positive mass")
    return outer_good_moment_tower(law) / mass


def exact_joint_success_mass(law: JointLaw, tau: Fraction) -> Fraction:
    """Return ``P(O and I and W <= tau^2)`` exactly.

    Here ``W`` is the normalized squared weighted-correlation badness.  The
    non-strict inequality preserves the desired boundary ``|R| <= tau*M*Y``.
    """

    tau = _fraction(tau, "tau", positive=True)
    validate_joint_law(law)
    threshold = tau**2
    return _sum_exact(
        outer.probability * inner.probability
        for outer in law
        if outer.outer_good
        for inner in outer.inner_outcomes
        if inner.inner_good
        and inner.normalized_squared_badness <= threshold
    )


def global_markov_joint_success_lower(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    outer_good_moment_upper: Fraction,
    tau: Fraction,
) -> Fraction:
    """Global same-law lower bound from ``E[1_O W] <= mu``.

    The returned quantity is
    ``max(0,(1-F_out)(1-F_in)-mu/tau^2)``.
    """

    f_out = _unit_fraction(
        outer_failure_upper, "outer_failure_upper", strict_upper=True
    )
    f_in = _unit_fraction(
        inner_failure_upper, "inner_failure_upper", strict_upper=True
    )
    mu = _fraction(outer_good_moment_upper, "outer_good_moment_upper")
    tau = _fraction(tau, "tau", positive=True)
    if mu < 0:
        raise ValueError("outer_good_moment_upper must be nonnegative")
    return max(Fraction(0), (1 - f_out) * (1 - f_in) - mu / tau**2)


def conditional_markov_joint_success_lower(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    conditional_moment_upper: Fraction,
    tau: Fraction,
) -> Fraction:
    """Conditional-on-outer-good lower bound from ``E[W|O] <= mu_O``."""

    f_out = _unit_fraction(
        outer_failure_upper, "outer_failure_upper", strict_upper=True
    )
    f_in = _unit_fraction(
        inner_failure_upper, "inner_failure_upper", strict_upper=True
    )
    mu_outer = _fraction(conditional_moment_upper, "conditional_moment_upper")
    tau = _fraction(tau, "tau", positive=True)
    if mu_outer < 0:
        raise ValueError("conditional_moment_upper must be nonnegative")
    conditional_success = max(
        Fraction(0), 1 - f_in - mu_outer / tau**2
    )
    return (1 - f_out) * conditional_success


def uniform_fiber_selection_certified(
    inner_failure_upper: Fraction,
    uniform_fiber_moment_upper: Fraction,
    tau: Fraction,
) -> bool:
    """Check ``F_in + mu_f/tau^2 < 1`` for every outer-good fiber."""

    f_in = _unit_fraction(
        inner_failure_upper, "inner_failure_upper", strict_upper=True
    )
    mu_fiber = _fraction(
        uniform_fiber_moment_upper, "uniform_fiber_moment_upper"
    )
    tau = _fraction(tau, "tau", positive=True)
    if mu_fiber < 0:
        raise ValueError("uniform_fiber_moment_upper must be nonnegative")
    return f_in + mu_fiber / tau**2 < 1


def raw_to_normalized_moment_upper(
    raw_second_moment_upper: Fraction,
    minimum_survivors: Fraction,
    prime_scale: Fraction,
) -> Fraction:
    """Normalize a raw ``E[1_O |R|^2]`` bound using ``M >= M_min``.

    This is conservative when the survivor count varies with the outcome.
    Supplying only an average survivor count is not accepted.
    """

    raw = _fraction(raw_second_moment_upper, "raw_second_moment_upper")
    minimum = _fraction(minimum_survivors, "minimum_survivors", positive=True)
    scale = _fraction(prime_scale, "prime_scale", positive=True)
    if raw < 0:
        raise ValueError("raw_second_moment_upper must be nonnegative")
    return raw / (minimum**2 * scale**2)


@dataclass(frozen=True)
class SameLawCorrelationDiagnostic:
    finite_tower_identity_exact: bool
    normalized_badness_divide_by_zero_guarded: bool
    global_markov_contract_exact: bool
    conditional_outer_good_contract_exact: bool
    uniform_fiber_contract_exact: bool
    fmt_fixed_subset_cardinality_is_drop_in_weighted_theorem: bool
    fgkmt_small_set_survival_is_drop_in_weighted_theorem: bool
    same_law_analytic_moment_bound_available: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> SameLawCorrelationDiagnostic:
    return SameLawCorrelationDiagnostic(
        finite_tower_identity_exact=True,
        normalized_badness_divide_by_zero_guarded=True,
        global_markov_contract_exact=True,
        conditional_outer_good_contract_exact=True,
        uniform_fiber_contract_exact=True,
        fmt_fixed_subset_cardinality_is_drop_in_weighted_theorem=False,
        fgkmt_small_set_survival_is_drop_in_weighted_theorem=False,
        same_law_analytic_moment_bound_available=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def load_ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def validate_ledger(
    document: dict[str, object],
    *,
    check_hashes: bool = True,
) -> list[str]:
    """Validate status fields and every local provenance pin."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != "DEP-R09 same-law weighted-correlation tower audit":
        issues.append("gate mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove an explicit global outer-good normalized second moment, or a "
        "stronger uniform outer-good-fiber moment, for the actual FMT joint "
        "law and CRT-dependent character observable."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 6:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "FMT",
        "FGKMT",
        "MAIER",
        "SONO",
        "THEORY77",
        "THEORY79",
    }
    keys = {
        item.get("key")
        for item in sources
        if isinstance(item, dict)
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
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != digest:
                issues.append(f"{key} hash mismatch")
    return issues
