"""Exact finite checks for the DEP-R09 conductor-weighted dual audit."""

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
    / "Sono_FMT_DEPR09_conductor_weighted_dual_v1.json"
)


def _validate_positive_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def divisors(value: int) -> tuple[int, ...]:
    value = _validate_positive_integer(value, "value")
    result: list[int] = []
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            result.append(divisor)
            if divisor * divisor != value:
                result.append(value // divisor)
    return tuple(sorted(result))


def euler_phi(value: int) -> int:
    value = _validate_positive_integer(value, "value")
    result = value
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result -= result // prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def mobius(value: int) -> int:
    value = _validate_positive_integer(value, "value")
    remaining = value
    count = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            count += 1
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        count += 1
    return -1 if count % 2 else 1


def residue_collision_count(residues: Sequence[int], modulus: int) -> int:
    modulus = _validate_positive_integer(modulus, "modulus")
    residues = tuple(residues)
    if not residues:
        raise ValueError("residues must be nonempty")
    counts: dict[int, int] = {}
    for residue in residues:
        if isinstance(residue, bool) or not isinstance(residue, int):
            raise TypeError("residues must be integers")
        key = residue % modulus
        counts[key] = counts.get(key, 0) + 1
    return sum(count * count for count in counts.values())


def primitive_level_coefficient_energy(
    conductor: int,
    residues: Sequence[int],
) -> int:
    """Return the primitive-character coefficient energy by Möbius inversion."""

    conductor = _validate_positive_integer(conductor, "conductor")
    residues = tuple(residues)
    if not residues:
        raise ValueError("residues must be nonempty")
    if any(math.gcd(residue, conductor) != 1 for residue in residues):
        raise ValueError("all residues must be coprime to the conductor")
    energy = 0
    for divisor in divisors(conductor):
        energy += (
            mobius(conductor // divisor)
            * euler_phi(divisor)
            * residue_collision_count(residues, divisor)
        )
    if energy < 0:
        raise AssertionError("primitive coefficient energy must be nonnegative")
    return energy


def conductor_energy_partition(
    modulus: int,
    residues: Sequence[int],
) -> dict[int, int]:
    modulus = _validate_positive_integer(modulus, "modulus")
    residues = tuple(residues)
    if not residues or len(set(residues)) != len(residues):
        raise ValueError("residues must be nonempty and distinct")
    if any(math.gcd(residue, modulus) != 1 for residue in residues):
        raise ValueError("all residues must be reduced modulo modulus")
    return {
        conductor: primitive_level_coefficient_energy(conductor, residues)
        for conductor in divisors(modulus)
    }


def expected_nonprincipal_coefficient_energy(modulus: int, count: int) -> int:
    modulus = _validate_positive_integer(modulus, "modulus")
    count = _validate_positive_integer(count, "count")
    phi = euler_phi(modulus)
    if count > phi:
        raise ValueError("count cannot exceed phi(modulus)")
    return count * (phi - count)


def separate_l2_normalized_square(
    modulus: int,
    count: int,
    prime_energy_ratio: Fraction,
) -> Fraction:
    """Return the squared Cauchy certificate divided by (N*U)^2.

    prime_energy_ratio is the source upper V_prime/U^2.
    """

    if not isinstance(prime_energy_ratio, Fraction):
        raise TypeError("prime_energy_ratio must be Fraction")
    if prime_energy_ratio < 0:
        raise ValueError("prime_energy_ratio must be nonnegative")
    energy = expected_nonprincipal_coefficient_energy(modulus, count)
    return Fraction(energy, count * count) * prime_energy_ratio


def prime_large_sieve_range_holds(
    prime_scale_exponent: Fraction,
    epsilon: Fraction,
) -> bool:
    """Check U=f^d > f^(2+epsilon) at exponent level."""

    if not isinstance(prime_scale_exponent, Fraction) or not isinstance(
        epsilon, Fraction
    ):
        raise TypeError("exponents must be Fraction")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    return prime_scale_exponent > 2 + epsilon


def small_prime_large_sieve_range_holds(
    log_small_scale_over_log_modulus: Fraction,
    epsilon: Fraction,
) -> bool:
    """Check Y>f^(2+epsilon) at logarithmic exponent level."""

    if not isinstance(log_small_scale_over_log_modulus, Fraction) or not isinstance(
        epsilon, Fraction
    ):
        raise TypeError("exponents must be Fraction")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    return log_small_scale_over_log_modulus > 2 + epsilon


@dataclass(frozen=True)
class ConductorWeightedDualDiagnostic:
    primitive_energy_partition_exact: bool
    nonprincipal_energy_identity_exact: bool
    sample_modulus: int
    sample_selected_count: int
    sample_level_energies: dict[str, int]
    sample_total_nonprincipal_energy: int
    optimistic_separate_l2_normalized_square: str
    optimistic_separate_l2_exceeds_one: bool
    schlage_puchta_primary_pdf_verified: bool
    large_prime_axis_source_range_holds: bool
    small_prime_full_modulus_source_range_holds: bool
    source_constants_fully_numerical: bool
    separate_l2_certificate_closes_gate: bool
    weighted_character_product_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> ConductorWeightedDualDiagnostic:
    modulus = 30
    residues = (7, 11, 13)
    partition = conductor_energy_partition(modulus, residues)
    nonprincipal = sum(
        energy for conductor, energy in partition.items() if conductor > 1
    )
    expected = expected_nonprincipal_coefficient_energy(modulus, len(residues))
    optimistic = separate_l2_normalized_square(
        modulus, len(residues), Fraction(1)
    )
    return ConductorWeightedDualDiagnostic(
        primitive_energy_partition_exact=(sum(partition.values()) == euler_phi(modulus) * len(residues)),
        nonprincipal_energy_identity_exact=(nonprincipal == expected),
        sample_modulus=modulus,
        sample_selected_count=len(residues),
        sample_level_energies={str(key): value for key, value in partition.items()},
        sample_total_nonprincipal_energy=nonprincipal,
        optimistic_separate_l2_normalized_square=str(optimistic),
        optimistic_separate_l2_exceeds_one=(optimistic > 1),
        schlage_puchta_primary_pdf_verified=True,
        large_prime_axis_source_range_holds=prime_large_sieve_range_holds(
            Fraction(21), Fraction(1)
        ),
        small_prime_full_modulus_source_range_holds=small_prime_large_sieve_range_holds(
            Fraction(1, 1000), Fraction(1)
        ),
        source_constants_fully_numerical=False,
        separate_l2_certificate_closes_gate=False,
        weighted_character_product_closed=False,
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
        "DEP-R09 conductor-weighted character dual audit"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "EXACT_CONDUCTOR_DUAL_BUT_SEPARATE_PRIME_SUPPORTED_L2_REINTRODUCES_"
        "PHI_OVER_N_AND_DOES_NOT_CLOSE_WEIGHTED_PRODUCT"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Control the signed weighted product sum directly, preserving the "
        "correlation between the small-prime coefficient and the large-prime "
        "character error; separate L2 estimates are quantitatively too coarse."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 4:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"SCHLAGE_PUCHTA2011", "THEORY84", "THEORY94", "FGKMT"}
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
    "conductor_energy_partition",
    "divisors",
    "euler_phi",
    "expected_nonprincipal_coefficient_energy",
    "load_ledger",
    "mobius",
    "prime_large_sieve_range_holds",
    "primitive_level_coefficient_energy",
    "residue_collision_count",
    "separate_l2_normalized_square",
    "small_prime_large_sieve_range_holds",
    "validate_ledger",
]
