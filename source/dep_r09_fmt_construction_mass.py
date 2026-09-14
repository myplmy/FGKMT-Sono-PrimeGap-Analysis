"""Exact finite probability algebra for the FMT two-stage construction.

This module does not prove the analytic FMT construction theorem or a prime
distribution estimate.  It checks only the probability bookkeeping after
valid outer and uniformly conditional inner failure bounds have been supplied.
All numerical inputs must be exact fractions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_FMT_construction_mass_v1.json"
)


def _unit_fraction(
    value: Fraction,
    name: str,
    *,
    strict_upper: bool = False,
) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    upper_ok = value < 1 if strict_upper else value <= 1
    if value < 0 or not upper_ok:
        relation = "[0,1)" if strict_upper else "[0,1]"
        raise ValueError(f"{name} must lie in {relation}")
    return value


def two_stage_sieve_success_lower(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
) -> Fraction:
    """Return the exact lower bound (1-F_out)(1-F_in).

    The inner bound is interpreted uniformly conditional on every outer-good
    first-stage outcome.  Independence is neither assumed nor needed.
    """

    f_out = _unit_fraction(
        outer_failure_upper, "outer_failure_upper", strict_upper=True
    )
    f_in = _unit_fraction(
        inner_failure_upper, "inner_failure_upper", strict_upper=True
    )
    return (1 - f_out) * (1 - f_in)


def two_stage_sieve_failure_upper(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
) -> Fraction:
    """Return F_out + (1-F_out)F_in for the sequential joint law."""

    return 1 - two_stage_sieve_success_lower(
        outer_failure_upper, inner_failure_upper
    )


def joint_good_mass_lower(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    correlation_failure_upper: Fraction,
) -> Fraction:
    """Union-bound the mass good for both sieve and correlation."""

    sieve_mass = two_stage_sieve_success_lower(
        outer_failure_upper, inner_failure_upper
    )
    f_corr = _unit_fraction(
        correlation_failure_upper, "correlation_failure_upper"
    )
    return max(Fraction(0), sieve_mass - f_corr)


def joint_selection_certified(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    correlation_failure_upper: Fraction,
) -> bool:
    """Require strict positive mass under the same joint construction law."""

    return (
        joint_good_mass_lower(
            outer_failure_upper,
            inner_failure_upper,
            correlation_failure_upper,
        )
        > 0
    )


def fiberwise_selection_certified(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    conditional_correlation_failure_upper: Fraction,
) -> bool:
    """Check the stronger per-outer-good-outcome sufficient condition."""

    f_out = _unit_fraction(
        outer_failure_upper, "outer_failure_upper", strict_upper=True
    )
    f_in = _unit_fraction(
        inner_failure_upper, "inner_failure_upper", strict_upper=True
    )
    f_corr = _unit_fraction(
        conditional_correlation_failure_upper,
        "conditional_correlation_failure_upper",
    )
    return f_out < 1 and f_in + f_corr < 1


def markov_failure_upper(
    expected_badness: Fraction,
    badness_threshold: Fraction,
) -> Fraction:
    """Return min(1,E[W]/t) for nonnegative W and t>0."""

    if isinstance(expected_badness, bool) or not isinstance(
        expected_badness, Fraction
    ):
        raise TypeError("expected_badness must be fractions.Fraction")
    if isinstance(badness_threshold, bool) or not isinstance(
        badness_threshold, Fraction
    ):
        raise TypeError("badness_threshold must be fractions.Fraction")
    if expected_badness < 0:
        raise ValueError("expected_badness must be nonnegative")
    if badness_threshold <= 0:
        raise ValueError("badness_threshold must be positive")
    return min(Fraction(1), expected_badness / badness_threshold)


@dataclass(frozen=True)
class FMTConstructionMassDiagnostic:
    printed_fmt_probability_rates_numerically_explicit: bool
    project_cov2_outer_failure_parameterized_explicit: bool
    project_cov2_uniform_conditional_inner_failure_parameterized_explicit: bool
    project_joint_sieve_good_mass_parameterized_explicit: bool
    joint_outcome_includes_outer_a_and_inner_n_prime: bool
    independence_required_for_mass_product: bool
    weighted_correlation_same_joint_law_failure_bound_available: bool
    fiberwise_weighted_correlation_bound_available: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> FMTConstructionMassDiagnostic:
    """Return the fail-closed status snapshot for Theory 79."""

    return FMTConstructionMassDiagnostic(
        printed_fmt_probability_rates_numerically_explicit=False,
        project_cov2_outer_failure_parameterized_explicit=True,
        project_cov2_uniform_conditional_inner_failure_parameterized_explicit=True,
        project_joint_sieve_good_mass_parameterized_explicit=True,
        joint_outcome_includes_outer_a_and_inner_n_prime=True,
        independence_required_for_mass_product=False,
        weighted_correlation_same_joint_law_failure_bound_available=False,
        fiberwise_weighted_correlation_bound_available=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        threshold_calculator_ready=False,
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
    """Validate the machine ledger and its local provenance pins."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != "DEP-R09 FMT construction-law finite-mass audit":
        issues.append("gate mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Bound the weighted-correlation bad event under the same joint "
        "(A,N-prime) construction law, globally or uniformly in each "
        "outer-good fiber."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 4:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"FMT_AUTH", "FMT_COMPARE", "THEORY53", "THEORY55"}
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
            locator = source.get("locator")
            digest = source.get("sha256")
            if not isinstance(locator, str) or not isinstance(digest, str):
                issues.append(f"{source.get('key', 'unknown')} missing pin")
                continue
            path = (REPO_ROOT / locator).resolve()
            try:
                path.relative_to(REPO_ROOT.resolve())
            except ValueError:
                issues.append(f"{source.get('key', 'unknown')} path escape")
                continue
            if not path.is_file():
                issues.append(f"{source.get('key', 'unknown')} missing source")
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != digest:
                issues.append(f"{source.get('key', 'unknown')} hash mismatch")
    return issues
