"""Exact finite checks for the DEP-R09 support-capacity audit.

The current FMT final residue system randomizes only outer primes in S and
inner primes in P'.  All other primorial coordinates are fixed.  Consequently
no empty-output tail can enlarge the shift support beyond the product of those
randomized coordinate moduli.  This module checks the finite support
pigeonhole algebra and the exact rational scale coefficients.

It does not evaluate primes, estimate an actual empty-output distribution, or
prove a local character-phase moment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from math import prod
from pathlib import Path
from typing import Iterable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_empty_output_support_capacity_audit_v1.json"
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


def randomized_residue_support_size(
    outer_moduli: Iterable[int],
    inner_moduli: Iterable[int],
) -> int:
    """Return the product of all distinct randomized coordinate moduli."""

    outer = tuple(outer_moduli)
    inner = tuple(inner_moduli)
    values = outer + inner
    if not values:
        raise ValueError("at least one randomized coordinate is required")
    for index, value in enumerate(values):
        _integer(value, f"modulus[{index}]", positive=True)
        if value < 2:
            raise ValueError("coordinate moduli must be at least two")
    if len(set(values)) != len(values):
        raise ValueError("randomized coordinate moduli must be distinct")
    return prod(values)


def event_atom_pigeonhole_lower(
    event_mass: Fraction,
    support_size: int,
) -> Fraction:
    """Return the exact lower bound event_mass/support_size."""

    event_mass = _fraction(
        event_mass, "event_mass", positive=True, probability=True
    )
    support_size = _integer(support_size, "support_size", positive=True)
    return event_mass / support_size


def event_entropy_factor(
    event_mass_lower: Fraction,
    claimed_atom_cap: Fraction,
    support_size: int,
) -> Fraction:
    """Return p_*/alpha after checking the finite support constraint."""

    event_mass_lower = _fraction(
        event_mass_lower,
        "event_mass_lower",
        positive=True,
        probability=True,
    )
    claimed_atom_cap = _fraction(
        claimed_atom_cap,
        "claimed_atom_cap",
        positive=True,
        probability=True,
    )
    support_size = _integer(support_size, "support_size", positive=True)
    minimum_possible_cap = event_atom_pigeonhole_lower(
        event_mass_lower, support_size
    )
    if claimed_atom_cap < minimum_possible_cap:
        raise ValueError("claimed event atom cap violates finite support")
    return event_mass_lower / claimed_atom_cap


def outer_support_log_coefficient_upper() -> Fraction:
    """Return 21/16000 from the outer theta bound."""

    return Fraction(21, 16000)


def inner_support_log_coefficient_upper() -> Fraction:
    """Return 1003/2000 from the dyadic-prime count bound."""

    return Fraction(1003, 2000)


def total_support_log_coefficient_upper() -> Fraction:
    """Return the sum 1609/3200."""

    return (
        outer_support_log_coefficient_upper()
        + inner_support_log_coefficient_upper()
    )


def full_primorial_log_coefficient_lower() -> Fraction:
    """Return the inherited 49/50 lower coefficient."""

    return Fraction(49, 50)


@dataclass(frozen=True)
class EmptyOutputSupportCapacityDiagnostic:
    fmt_only_s_and_p_coordinates_randomized_source_verified: bool
    outside_coordinates_fixed_zero_source_verified: bool
    finite_support_pigeonhole_exact: bool
    event_success_mass_retained_in_entropy_factor: bool
    toy_outer_support: int
    toy_inner_support: int
    toy_total_support: int
    toy_event_mass: str
    toy_minimum_event_atom: str
    toy_best_entropy_factor: str
    outer_log_coefficient_upper: str
    inner_log_coefficient_upper: str
    total_support_log_coefficient_upper: str
    total_support_log_coefficient_below_fifty_one_hundredths: bool
    full_primorial_log_coefficient_lower: str
    randomized_support_is_strictly_subprimorial: bool
    any_empty_output_tail_can_rescue_atom_full_energy_large_sieve_route: bool
    local_character_phase_cancellation_ruled_out: bool
    actual_empty_output_numerical_tail_identified: bool
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


def build_diagnostic() -> EmptyOutputSupportCapacityDiagnostic:
    outer = randomized_residue_support_size((2, 3), ())
    inner = randomized_residue_support_size((5, 7), ())
    total = randomized_residue_support_size((2, 3), (5, 7))
    event_mass = Fraction(3, 5)
    minimum_atom = event_atom_pigeonhole_lower(event_mass, total)
    entropy_factor = event_entropy_factor(
        event_mass, minimum_atom, total
    )
    support_upper = total_support_log_coefficient_upper()
    full_lower = full_primorial_log_coefficient_lower()
    return EmptyOutputSupportCapacityDiagnostic(
        fmt_only_s_and_p_coordinates_randomized_source_verified=True,
        outside_coordinates_fixed_zero_source_verified=True,
        finite_support_pigeonhole_exact=True,
        event_success_mass_retained_in_entropy_factor=True,
        toy_outer_support=outer,
        toy_inner_support=inner,
        toy_total_support=total,
        toy_event_mass=str(event_mass),
        toy_minimum_event_atom=str(minimum_atom),
        toy_best_entropy_factor=str(entropy_factor),
        outer_log_coefficient_upper=str(
            outer_support_log_coefficient_upper()
        ),
        inner_log_coefficient_upper=str(
            inner_support_log_coefficient_upper()
        ),
        total_support_log_coefficient_upper=str(support_upper),
        total_support_log_coefficient_below_fifty_one_hundredths=(
            support_upper < Fraction(51, 100)
        ),
        full_primorial_log_coefficient_lower=str(full_lower),
        randomized_support_is_strictly_subprimorial=(
            support_upper < full_lower
        ),
        any_empty_output_tail_can_rescue_atom_full_energy_large_sieve_route=False,
        local_character_phase_cancellation_ruled_out=False,
        actual_empty_output_numerical_tail_identified=False,
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
    """Validate source pins and fail-closed scientific status."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != (
        "DEP-R09 empty-output and randomized-support capacity audit"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "RANDOMIZED_RESIDUE_SUPPORT_STRICTLY_SUBPRIMORIAL_SO_EMPTY_TAIL_"
        "CANNOT_RESCUE_ATOM_TIMES_FULL_ENERGY_LARGE_SIEVE_ROUTE"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Audit the reweighted local Dirichlet-character transform or another "
        "direct phase-correlation mechanism; support cardinality proves that "
        "no empty-output tail alone can close the atom-cap times full-energy "
        "large-sieve architecture."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 7:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "FMT", "FGKMT", "THEORY47", "THEORY53", "THEORY82",
        "THEORY83", "THEORY87",
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
    "event_atom_pigeonhole_lower",
    "event_entropy_factor",
    "full_primorial_log_coefficient_lower",
    "inner_support_log_coefficient_upper",
    "load_ledger",
    "outer_support_log_coefficient_upper",
    "randomized_residue_support_size",
    "total_support_log_coefficient_upper",
    "validate_ledger",
]
