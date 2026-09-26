"""Exact finite checks for the DEP-R09 local-character-transform audit.

The module records three finite facts:

* the exact transform of a conditional residue distribution;
* a small-atom distribution can have multiplicative-character transform one;
* characters principal on every randomized coordinate form a blind family
  whose coefficient energy is fixed by character orthogonality.

No prime-error estimate, actual prime computation, or numerical threshold is
performed.
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
    / "Sono_FMT_DEPR09_local_character_transform_audit_v1.json"
)


def _integer(value: object, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _signed_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def _fraction(
    value: object,
    name: str,
    *,
    probability: bool = False,
) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if probability and not 0 <= value <= 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return value


def is_prime(value: int) -> bool:
    value = _integer(value, "value", minimum=2)
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def legendre_symbol(value: int, prime: int) -> int:
    """Return the exact Legendre symbol for an odd prime."""

    value = _signed_integer(value, "value")
    prime = _integer(prime, "prime", minimum=3)
    if prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime")
    residue = value % prime
    if residue == 0:
        return 0
    squares = {(item * item) % prime for item in range(1, prime)}
    return 1 if residue in squares else -1


def quadratic_local_transform(
    distribution: Mapping[int, Fraction],
    *,
    prime: int,
    offset: int,
) -> Fraction:
    """Return sum_a nu(a)*(offset-a|prime) exactly."""

    prime = _integer(prime, "prime", minimum=3)
    offset = _signed_integer(offset, "offset")
    if not isinstance(distribution, Mapping) or not distribution:
        raise ValueError("distribution must be a nonempty mapping")
    total_mass = Fraction(0)
    transform = Fraction(0)
    for residue, mass in distribution.items():
        residue = _integer(residue, "residue")
        if not 0 <= residue < prime:
            raise ValueError("residues must lie in [0,prime)")
        mass = _fraction(mass, "mass", probability=True)
        total_mass += mass
        transform += mass * legendre_symbol(offset - residue, prime)
    if total_mass != 1:
        raise ValueError("distribution must have total mass one")
    return transform


def quadratic_level_set_distribution(
    *,
    prime: int,
    offset: int,
    target: int,
) -> dict[int, Fraction]:
    """Return the uniform level-set law for a quadratic character."""

    prime = _integer(prime, "prime", minimum=3)
    offset = _signed_integer(offset, "offset")
    if target not in (-1, 1):
        raise ValueError("target must be -1 or 1")
    support = tuple(
        residue
        for residue in range(prime)
        if legendre_symbol(offset - residue, prime) == target
    )
    if not support:
        raise AssertionError("quadratic level set must be nonempty")
    mass = Fraction(1, len(support))
    return {residue: mass for residue in support}


def stage_transform_from_atoms(
    atom_probabilities: Sequence[Fraction],
    character_values: Sequence[int],
) -> Fraction:
    """Return an exact real-character stage transform."""

    probabilities = tuple(atom_probabilities)
    values = tuple(character_values)
    if not probabilities or len(probabilities) != len(values):
        raise ValueError("probabilities and values need equal nonzero length")
    total = Fraction(0)
    transform = Fraction(0)
    for index, (probability, value) in enumerate(zip(probabilities, values)):
        probability = _fraction(
            probability, f"atom_probabilities[{index}]", probability=True
        )
        if value not in (-1, 0, 1):
            raise ValueError("real Dirichlet-character values must be -1,0,1")
        total += probability
        transform += probability * value
    if total != 1:
        raise ValueError("atom probabilities must sum to one")
    return transform


def blind_character_energy(phi_fixed: int, survivor_count: int) -> dict[str, int]:
    """Return total, principal, and nonprincipal blind coefficient energies."""

    phi_fixed = _integer(phi_fixed, "phi_fixed", minimum=1)
    survivor_count = _integer(
        survivor_count, "survivor_count", minimum=0
    )
    if survivor_count > phi_fixed:
        raise ValueError("distinct reduced residues cannot exceed phi_fixed")
    total = phi_fixed * survivor_count
    principal = survivor_count**2
    return {
        "total": total,
        "principal": principal,
        "nonprincipal": total - principal,
    }


def blind_cauchy_gate(
    tau: Fraction,
    survivor_count: int,
    prime_scale: Fraction,
    phi_fixed: int,
) -> Fraction:
    """Return tau^2*M*Y^2/(phi(f)-M), rejecting the degenerate boundary."""

    tau = _fraction(tau, "tau")
    prime_scale = _fraction(prime_scale, "prime_scale")
    if tau <= 0 or prime_scale <= 0:
        raise ValueError("tau and prime_scale must be positive")
    phi_fixed = _integer(phi_fixed, "phi_fixed", minimum=1)
    survivor_count = _integer(
        survivor_count, "survivor_count", minimum=1
    )
    if survivor_count >= phi_fixed:
        raise ValueError("need survivor_count < phi_fixed")
    return (
        tau**2
        * survivor_count
        * prime_scale**2
        / (phi_fixed - survivor_count)
    )


def fixed_modulus_log_coefficient_lower() -> Fraction:
    """Return 49/50-51/100=47/100."""

    return Fraction(47, 100)


@dataclass(frozen=True)
class LocalCharacterTransformDiagnostic:
    exact_conditional_local_transform_defined: bool
    stage_product_requires_only_conditional_independence: bool
    atom_cap_implies_uniform_fourier_saving: bool
    level_set_prime: int
    level_set_support_size: int
    level_set_max_atom: str
    level_set_transform: str
    randomized_modulus_and_fixed_modulus_coprime: bool
    fixed_coordinates_force_shift_zero_mod_fixed_part: bool
    blind_family_size_is_phi_fixed: bool
    blind_total_coefficient_energy_exact: bool
    blind_nonprincipal_coefficient_energy_exact: bool
    toy_phi_fixed: int
    toy_survivor_count: int
    toy_total_energy: int
    toy_principal_energy: int
    toy_nonprincipal_energy: int
    fixed_modulus_log_coefficient_lower: str
    fixed_modulus_exponentially_larger_than_offset_interval: bool
    gkm_primary_pdf_verified: bool
    gkm_theorem_is_actual_multidimensional_reweighted_transform: bool
    gkm_constants_uniform_in_growing_dimension: bool
    applicable_numerical_local_transform_theorem_identified: bool
    blind_prime_error_correlation_closed: bool
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


def build_diagnostic() -> LocalCharacterTransformDiagnostic:
    level_set = quadratic_level_set_distribution(
        prime=11, offset=0, target=1
    )
    transform = quadratic_local_transform(
        level_set, prime=11, offset=0
    )
    energy = blind_character_energy(4, 3)
    return LocalCharacterTransformDiagnostic(
        exact_conditional_local_transform_defined=True,
        stage_product_requires_only_conditional_independence=True,
        atom_cap_implies_uniform_fourier_saving=False,
        level_set_prime=11,
        level_set_support_size=len(level_set),
        level_set_max_atom=str(max(level_set.values())),
        level_set_transform=str(transform),
        randomized_modulus_and_fixed_modulus_coprime=True,
        fixed_coordinates_force_shift_zero_mod_fixed_part=True,
        blind_family_size_is_phi_fixed=True,
        blind_total_coefficient_energy_exact=True,
        blind_nonprincipal_coefficient_energy_exact=True,
        toy_phi_fixed=4,
        toy_survivor_count=3,
        toy_total_energy=energy["total"],
        toy_principal_energy=energy["principal"],
        toy_nonprincipal_energy=energy["nonprincipal"],
        fixed_modulus_log_coefficient_lower=str(
            fixed_modulus_log_coefficient_lower()
        ),
        fixed_modulus_exponentially_larger_than_offset_interval=True,
        gkm_primary_pdf_verified=True,
        gkm_theorem_is_actual_multidimensional_reweighted_transform=False,
        gkm_constants_uniform_in_growing_dimension=False,
        applicable_numerical_local_transform_theorem_identified=False,
        blind_prime_error_correlation_closed=False,
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
        "DEP-R09 reweighted local Dirichlet-character transform audit"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "EXACT_LOCAL_TRANSFORM_BUT_ATOM_CAP_HAS_NO_FOURIER_SAVING_"
        "AND_BLIND_CHARACTER_ENERGY_REMAINS"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Control the blind-family prime-error correlation or prove a "
        "prime-specific fixed-modulus upper for the fixed-coordinate modulus; "
        "randomized-coordinate local transforms alone cannot close the full "
        "same-law moment."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 8:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "GKM2020", "FGKMT", "FMT", "THEORY47", "THEORY53",
        "THEORY77", "THEORY80", "THEORY88",
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
    "blind_character_energy",
    "blind_cauchy_gate",
    "build_diagnostic",
    "fixed_modulus_log_coefficient_lower",
    "legendre_symbol",
    "load_ledger",
    "quadratic_level_set_distribution",
    "quadratic_local_transform",
    "stage_transform_from_atoms",
    "validate_ledger",
]
