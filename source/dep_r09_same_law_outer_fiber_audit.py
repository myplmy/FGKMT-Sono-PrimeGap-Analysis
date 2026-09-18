"""Exact finite checks for the DEP-R09 outer-fiber minimax reduction.

The actual FMT construction has a uniform outer residue vector and an
adaptive conditional inner output.  For a nonnegative observable, uniformity
of the outer vector bounds the same-law expectation by the average of the
maximum observable value in each conditional-support fiber.  This module
checks that finite statement, its sharpness among arbitrary conditional laws
on the same fibers, and the strict scalar gate used downstream.

It does not bound the actual prime-error observable on those fibers, prove a
new FMT concentration theorem, run a prime computation, or construct an
``X_cert`` threshold.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_same_law_outer_fiber_minimax_v1.json"
)


def _integer(value: object, name: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _fraction(value: object, name: str, *, positive: bool = False) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _energy_matrix(
    values: Sequence[Sequence[Fraction]],
) -> tuple[tuple[Fraction, ...], ...]:
    if not values:
        raise ValueError("energy fibers must be nonempty")
    rows = tuple(tuple(row) for row in values)
    if not rows[0]:
        raise ValueError("each energy fiber must be nonempty")
    width = len(rows[0])
    for row_index, row in enumerate(rows):
        if len(row) != width:
            raise ValueError("energy fibers must have equal width")
        for column_index, value in enumerate(row):
            if not isinstance(value, Fraction):
                raise TypeError(
                    f"energy[{row_index}][{column_index}] must be Fraction"
                )
            if value < 0:
                raise ValueError("energy must be nonnegative")
    return rows


def outer_fiber_maximum_energy(
    values: Sequence[Sequence[Fraction]],
) -> Fraction:
    """Return ``sum_a max_(m in M(a)) E(m)`` exactly."""

    rows = _energy_matrix(values)
    return sum((max(row) for row in rows), Fraction(0))


def full_support_energy(values: Sequence[Sequence[Fraction]]) -> Fraction:
    """Return the energy summed over every point of every disjoint fiber."""

    rows = _energy_matrix(values)
    return sum((sum(row, Fraction(0)) for row in rows), Fraction(0))


def outer_uniform_event_raw_moment(
    values: Sequence[Sequence[Fraction]],
    event_subprobabilities: Sequence[Sequence[Fraction]],
) -> Fraction:
    """Return the exact raw moment under a uniform outer marginal.

    For each outer fiber ``a``, the second matrix contains conditional joint
    masses ``P(S and m | A=a)``.  Each row is therefore a subprobability and
    must have total mass at most one.  No independence between the event and
    the selected inner point is assumed.
    """

    rows = _energy_matrix(values)
    masses = tuple(tuple(row) for row in event_subprobabilities)
    if len(masses) != len(rows):
        raise ValueError("subprobability matrix must have one row per fiber")
    weighted_sum = Fraction(0)
    for row_index, (energy_row, mass_row) in enumerate(zip(rows, masses)):
        if len(mass_row) != len(energy_row):
            raise ValueError("subprobability rows must match the energy width")
        conditional_total = Fraction(0)
        for column_index, (energy, mass) in enumerate(zip(energy_row, mass_row)):
            if not isinstance(mass, Fraction):
                raise TypeError(
                    "event_subprobabilities"
                    f"[{row_index}][{column_index}] must be Fraction"
                )
            if mass < 0:
                raise ValueError("event subprobabilities must be nonnegative")
            conditional_total += mass
            weighted_sum += mass * energy
        if conditional_total > 1:
            raise ValueError("each conditional event row must have mass at most one")
    return weighted_sum / len(rows)


def outer_fiber_raw_moment_upper(
    values: Sequence[Sequence[Fraction]],
) -> Fraction:
    """Return the exact outer-fiber envelope ``H/|A|``."""

    rows = _energy_matrix(values)
    return outer_fiber_maximum_energy(rows) / len(rows)


def maximizing_conditional_law(
    values: Sequence[Sequence[Fraction]],
) -> tuple[tuple[Fraction, ...], ...]:
    """Choose the first maximizer in each fiber with conditional mass one."""

    rows = _energy_matrix(values)
    result: list[tuple[Fraction, ...]] = []
    for row in rows:
        maximizing_index = row.index(max(row))
        result.append(
            tuple(
                Fraction(1) if index == maximizing_index else Fraction(0)
                for index in range(len(row))
            )
        )
    return tuple(result)


def crt_fiber_matrix(
    outer_modulus: int,
    inner_modulus: int,
    residue_energy: Sequence[Fraction],
) -> tuple[tuple[Fraction, ...], ...]:
    """Arrange energy modulo ``q`` by its coprime outer and inner residues."""

    outer_modulus = _integer(outer_modulus, "outer_modulus", positive=True)
    inner_modulus = _integer(inner_modulus, "inner_modulus", positive=True)
    if math.gcd(outer_modulus, inner_modulus) != 1:
        raise ValueError("outer and inner moduli must be coprime")
    modulus = outer_modulus * inner_modulus
    if len(residue_energy) != modulus:
        raise ValueError("residue_energy must have outer_modulus*inner_modulus entries")
    for index, value in enumerate(residue_energy):
        if not isinstance(value, Fraction):
            raise TypeError(f"residue_energy[{index}] must be Fraction")
        if value < 0:
            raise ValueError("residue energy must be nonnegative")

    rows: list[list[Fraction | None]] = [
        [None for _ in range(inner_modulus)] for _ in range(outer_modulus)
    ]
    for residue, value in enumerate(residue_energy):
        rows[residue % outer_modulus][residue % inner_modulus] = value
    if any(value is None for row in rows for value in row):
        raise AssertionError("CRT fibers must partition the residue classes")
    return tuple(tuple(value for value in row if value is not None) for row in rows)


def outer_fiber_energy_gate(
    tau: Fraction,
    sieve_good_mass_lower: Fraction,
    outer_denominator: int,
    minimum_survivors: Fraction,
    prime_scale: Fraction,
) -> Fraction:
    """Return ``tau^2 p_* Q_S M_min^2 Y^2`` exactly."""

    tau = _fraction(tau, "tau", positive=True)
    sieve_good_mass_lower = _fraction(
        sieve_good_mass_lower, "sieve_good_mass_lower", positive=True
    )
    outer_denominator = _integer(
        outer_denominator, "outer_denominator", positive=True
    )
    minimum_survivors = _fraction(
        minimum_survivors, "minimum_survivors", positive=True
    )
    prime_scale = _fraction(prime_scale, "prime_scale", positive=True)
    return (
        tau**2
        * sieve_good_mass_lower
        * outer_denominator
        * minimum_survivors**2
        * prime_scale**2
    )


def passes_strict_outer_fiber_gate(
    fiber_energy: Fraction,
    threshold: Fraction,
) -> bool:
    fiber_energy = _fraction(fiber_energy, "fiber_energy")
    threshold = _fraction(threshold, "threshold", positive=True)
    if fiber_energy < 0:
        raise ValueError("fiber_energy must be nonnegative")
    return fiber_energy < threshold


def toy_energy_matrix() -> tuple[tuple[Fraction, ...], ...]:
    """Return six outer fibers and five inner points for a modulo-30 toy."""

    return tuple(
        tuple(Fraction(value) for value in row)
        for row in (
            (1, 4, 9, 16, 25),
            (4, 1, 16, 9, 36),
            (9, 9, 1, 4, 16),
            (16, 4, 4, 1, 9),
            (25, 1, 9, 4, 1),
            (36, 25, 16, 9, 4),
        )
    )


@dataclass(frozen=True)
class SameLawOuterFiberDiagnostic:
    fmt_outer_uniformity_and_coordinate_preservation_source_verified: bool
    outer_uniform_event_subprobability_reduction_exact: bool
    support_restricted_outer_fiber_envelope_exact: bool
    adaptive_deterministic_selector_attains_abstract_envelope: bool
    outer_fiber_energy_not_above_full_support_energy: bool
    toy_outer_denominator: int
    toy_inner_denominator: int
    toy_outer_fiber_energy: str
    toy_full_support_energy: str
    toy_sharp_raw_moment: str
    toy_fiber_bound_strictly_below_full_energy_bound: bool
    actual_fmt_law_attains_the_abstract_envelope_claimed: bool
    actual_fiber_energy_analytic_upper_identified: bool
    final_nibble_weighted_concentration_theorem_identified: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> SameLawOuterFiberDiagnostic:
    matrix = toy_energy_matrix()
    fiber_energy = outer_fiber_maximum_energy(matrix)
    full_energy = full_support_energy(matrix)
    maximizing_law = maximizing_conditional_law(matrix)
    sharp_raw = outer_uniform_event_raw_moment(matrix, maximizing_law)
    return SameLawOuterFiberDiagnostic(
        fmt_outer_uniformity_and_coordinate_preservation_source_verified=True,
        outer_uniform_event_subprobability_reduction_exact=True,
        support_restricted_outer_fiber_envelope_exact=True,
        adaptive_deterministic_selector_attains_abstract_envelope=(
            sharp_raw == outer_fiber_raw_moment_upper(matrix)
        ),
        outer_fiber_energy_not_above_full_support_energy=(
            fiber_energy <= full_energy
        ),
        toy_outer_denominator=6,
        toy_inner_denominator=5,
        toy_outer_fiber_energy=str(fiber_energy),
        toy_full_support_energy=str(full_energy),
        toy_sharp_raw_moment=str(sharp_raw),
        toy_fiber_bound_strictly_below_full_energy_bound=(
            fiber_energy < full_energy
        ),
        actual_fmt_law_attains_the_abstract_envelope_claimed=False,
        actual_fiber_energy_analytic_upper_identified=False,
        final_nibble_weighted_concentration_theorem_identified=False,
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
    if document.get("gate") != "DEP-R09 same-law outer-fiber minimax audit":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "ACTUAL_FMT_RAW_MOMENT_REDUCED_TO_SUPPORT_RESTRICTED_OUTER_FIBER_"
        "MAXIMUM_BUT_THE_REQUIRED_ANALYTIC_FIBER_BOUND_REMAINS_OPEN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Bound the support-restricted outer-fiber energy for the actual prime-"
        "error observable using final-law conditional weights or prime-specific "
        "structure; outer uniformity and support alone cannot improve its "
        "universal maximum envelope."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 4:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"FMT", "THEORY79", "THEORY81", "THEORY82"}
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
    "crt_fiber_matrix",
    "full_support_energy",
    "load_ledger",
    "maximizing_conditional_law",
    "outer_fiber_energy_gate",
    "outer_fiber_maximum_energy",
    "outer_fiber_raw_moment_upper",
    "outer_uniform_event_raw_moment",
    "passes_strict_outer_fiber_gate",
    "toy_energy_matrix",
    "validate_ledger",
]
