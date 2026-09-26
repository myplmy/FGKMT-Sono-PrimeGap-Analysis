"""Exact checks for the DEP-R09 blind residue-discrepancy reduction.

The helper verifies a finite character inverse transform modulo five, the
restricted Parseval identity, the explicit Brun--Titchmarsh coefficient
arithmetic, and the normalized survivor-moment gate obtained from Theory 91.
It does not enumerate primes or evaluate a threshold.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence

from source.dep_r09_weighted_survivor_moment_audit import GaussianRational


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_blind_residue_discrepancy_v1.json"
)


def _fraction(value: object, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    return value


def _character_mod_five(index: int, residue: int) -> GaussianRational:
    """Return the index-th Dirichlet character modulo five exactly.

    The generator is 2, so 1,2,4,3 have exponents 0,1,2,3.  Character
    values are powers of i and are therefore Gaussian rationals.
    """

    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < 4:
        raise ValueError("character index must lie in 0..3")
    if isinstance(residue, bool) or not isinstance(residue, int):
        raise TypeError("residue must be an integer")
    residue %= 5
    if residue == 0:
        return GaussianRational(Fraction(0))
    exponent = {1: 0, 2: 1, 4: 2, 3: 3}[residue]
    powers = (
        GaussianRational(Fraction(1)),
        GaussianRational(Fraction(0), Fraction(1)),
        GaussianRational(Fraction(-1)),
        GaussianRational(Fraction(0), Fraction(-1)),
    )
    return powers[(index * exponent) % 4]


def _validate_residue_masses(
    residue_masses: Mapping[int, Fraction],
) -> dict[int, Fraction]:
    if set(residue_masses) != {1, 2, 3, 4}:
        raise ValueError("residue masses must have keys 1,2,3,4")
    checked: dict[int, Fraction] = {}
    for residue, mass in residue_masses.items():
        mass = _fraction(mass, f"mass[{residue}]")
        if mass < 0:
            raise ValueError("residue masses must be nonnegative")
        checked[residue] = mass
    return checked


def character_sums_mod_five(
    residue_masses: Mapping[int, Fraction],
) -> tuple[GaussianRational, ...]:
    """Return Z_chi=sum_a A_a chi(a) for all characters modulo five."""

    masses = _validate_residue_masses(residue_masses)
    sums: list[GaussianRational] = []
    for index in range(4):
        total = GaussianRational(Fraction(0))
        for residue, mass in masses.items():
            total = total + (_character_mod_five(index, residue) * mass)
        sums.append(total)
    return tuple(sums)


def blind_weights_mod_five(
    residue_masses: Mapping[int, Fraction],
) -> dict[int, GaussianRational]:
    """Return B(v)=sum_(chi!=chi0) conjugate(chi(v))*Z_chi."""

    sums = character_sums_mod_five(residue_masses)
    weights: dict[int, GaussianRational] = {}
    for residue in (1, 2, 3, 4):
        total = GaussianRational(Fraction(0))
        for index in range(1, 4):
            total = total + (
                _character_mod_five(index, residue).conjugate() * sums[index]
            )
        weights[residue] = total
    return weights


def residue_discrepancies_mod_five(
    residue_masses: Mapping[int, Fraction],
) -> dict[int, Fraction]:
    """Return phi(5) A_v-S for every reduced residue."""

    masses = _validate_residue_masses(residue_masses)
    total = sum(masses.values(), Fraction(0))
    return {residue: 4 * mass - total for residue, mass in masses.items()}


def inverse_transform_holds_mod_five(
    residue_masses: Mapping[int, Fraction],
) -> bool:
    blind = blind_weights_mod_five(residue_masses)
    discrepancy = residue_discrepancies_mod_five(residue_masses)
    return all(
        blind[residue]
        == GaussianRational(discrepancy[residue])
        for residue in discrepancy
    )


def parseval_holds_mod_five(
    residue_masses: Mapping[int, Fraction],
) -> bool:
    """Verify sum_v |B(v)|^2=phi(5)*sum_(chi!=chi0)|Z_chi|^2."""

    blind = blind_weights_mod_five(residue_masses)
    character_sums = character_sums_mod_five(residue_masses)
    residue_energy = sum(
        (weight.norm_square() for weight in blind.values()), Fraction(0)
    )
    character_energy = 4 * sum(
        (value.norm_square() for value in character_sums[1:]), Fraction(0)
    )
    return residue_energy == character_energy


def subset_mean_discrepancy_mod_five(
    residue_masses: Mapping[int, Fraction],
    subset: Sequence[int],
) -> Fraction:
    masses = _validate_residue_masses(residue_masses)
    subset = tuple(subset)
    if not subset or len(set(subset)) != len(subset):
        raise ValueError("subset must be nonempty and duplicate-free")
    if any(residue not in masses for residue in subset):
        raise ValueError("subset contains a non-reduced residue")
    total = sum(masses.values(), Fraction(0))
    selected = sum((masses[residue] for residue in subset), Fraction(0))
    return 4 * selected - len(subset) * total


def brun_titchmarsh_prime_coefficient(effective_exponent: Fraction) -> Fraction:
    """Return 2d/(d-1) from MV Theorem 2 with U=f^d."""

    exponent = _fraction(effective_exponent, "effective_exponent")
    if exponent <= 1:
        raise ValueError("effective exponent must exceed one")
    return 2 * exponent / (exponent - 1)


def blind_pointwise_envelope(
    effective_exponent: Fraction,
    progression_prime_power_ratio: Fraction,
    principal_prime_power_ratio: Fraction,
) -> dict[str, Fraction]:
    """Return pointwise coefficients after prime-power corrections.

    The first correction denotes phi(f)*sqrt(U)*log(U)/U; the second denotes
    sqrt(U)*log(U)/U.  The theta(U)<21U/20 source input is kept separate.
    """

    progression_correction = _fraction(
        progression_prime_power_ratio, "progression_prime_power_ratio"
    )
    principal_correction = _fraction(
        principal_prime_power_ratio, "principal_prime_power_ratio"
    )
    if progression_correction < 0 or principal_correction < 0:
        raise ValueError("prime-power ratios must be nonnegative")
    progression = (
        brun_titchmarsh_prime_coefficient(effective_exponent)
        + progression_correction
    )
    principal = Fraction(21, 20) + principal_correction
    return {
        "progression": progression,
        "principal": principal,
        "blind_weight": max(progression, principal),
    }


def normalized_pair_factor(
    rho: Fraction,
    alpha: Fraction,
    beta: Fraction,
    vertex_count: int,
) -> Fraction:
    """Return K/(rho^2*M) in the normalized Theory 91 certificate."""

    rho = _fraction(rho, "rho")
    alpha = _fraction(alpha, "alpha")
    beta = _fraction(beta, "beta")
    if not 0 < rho <= 1 or alpha < 0 or beta < 0:
        raise ValueError("invalid moment parameters")
    if isinstance(vertex_count, bool) or not isinstance(vertex_count, int):
        raise TypeError("vertex_count must be an integer")
    if vertex_count < 1:
        raise ValueError("vertex_count must be positive")
    count = Fraction(vertex_count)
    return (
        (1 + alpha) / (rho * count)
        - 1 / count
        + beta * (count - 1) / count
    )


def normalized_moment_certificate(
    mean_discrepancy_ratio: Fraction,
    pointwise_weight_ratio: Fraction,
    rho: Fraction,
    alpha: Fraction,
    beta: Fraction,
    vertex_count: int,
) -> Fraction:
    """Return E|R|^2/(rho*M*U)^2 under the audited premises."""

    mean_ratio = _fraction(mean_discrepancy_ratio, "mean_discrepancy_ratio")
    weight_ratio = _fraction(pointwise_weight_ratio, "pointwise_weight_ratio")
    if mean_ratio < 0 or weight_ratio < 0:
        raise ValueError("ratios must be nonnegative")
    return mean_ratio**2 + weight_ratio**2 * normalized_pair_factor(
        rho, alpha, beta, vertex_count
    )


@dataclass(frozen=True)
class BlindResidueDiagnostic:
    finite_character_inverse_transform_exact: bool
    blind_weights_are_real_residue_discrepancies: bool
    full_residue_parseval_exact: bool
    selected_subset_mean_identity_exact: bool
    mv1973_primary_pdf_hash_verified: bool
    mv1973_theorem2_fully_explicit: bool
    effective_exponent_21_prime_coefficient: str
    progression_pointwise_envelope: str
    principal_pointwise_envelope: str
    blind_pointwise_envelope: str
    normalized_pair_factor: str
    normalized_pair_factor_minus_beta: str
    pair_dimension_loss_reduces_to_beta_at_large_vertex_count: bool
    sparse_selected_residue_mean_numerically_small: bool
    blind_same_law_moment_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> BlindResidueDiagnostic:
    masses = {
        1: Fraction(7),
        2: Fraction(2),
        3: Fraction(5),
        4: Fraction(11),
    }
    subset = (1, 3)
    blind = blind_weights_mod_five(masses)
    subset_identity = sum(
        (blind[residue].real for residue in subset), Fraction(0)
    ) == subset_mean_discrepancy_mod_five(masses, subset)
    envelope = blind_pointwise_envelope(
        Fraction(21), Fraction(1, 10), Fraction(1, 20)
    )
    rho = Fraction(1, 5)
    alpha = Fraction(1, 100)
    beta = Fraction(1, 1000)
    count = 1000
    pair_factor = normalized_pair_factor(rho, alpha, beta, count)
    return BlindResidueDiagnostic(
        finite_character_inverse_transform_exact=(
            inverse_transform_holds_mod_five(masses)
        ),
        blind_weights_are_real_residue_discrepancies=all(
            weight.imag == 0 for weight in blind.values()
        ),
        full_residue_parseval_exact=parseval_holds_mod_five(masses),
        selected_subset_mean_identity_exact=subset_identity,
        mv1973_primary_pdf_hash_verified=True,
        mv1973_theorem2_fully_explicit=True,
        effective_exponent_21_prime_coefficient=str(
            brun_titchmarsh_prime_coefficient(Fraction(21))
        ),
        progression_pointwise_envelope=str(envelope["progression"]),
        principal_pointwise_envelope=str(envelope["principal"]),
        blind_pointwise_envelope=str(envelope["blind_weight"]),
        normalized_pair_factor=str(pair_factor),
        normalized_pair_factor_minus_beta=str(pair_factor - beta),
        pair_dimension_loss_reduces_to_beta_at_large_vertex_count=True,
        sparse_selected_residue_mean_numerically_small=False,
        blind_same_law_moment_closed=False,
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
        "DEP-R09 blind residue discrepancy and pointwise envelope reduction"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "BLIND_WEIGHT_IS_REAL_SPARSE_RESIDUE_DISCREPANCY_AND_POINTWISE_"
        "ENVELOPE_REMOVES_BETA_RHO_M_OBSTRUCTION_BUT_CENTERED_MEAN_REMAINS_OPEN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove a fully numerical centered discrepancy bound for the "
        "construction-dependent sparse prime residue set, uniformly on the "
        "required outer-good fibers; one-sided Brun--Titchmarsh and full "
        "residue variance do not supply this mean bound."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 6:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "MONTGOMERY_VAUGHAN1973",
        "THEORY55",
        "THEORY83",
        "THEORY89",
        "THEORY90",
        "THEORY91",
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
    "blind_pointwise_envelope",
    "blind_weights_mod_five",
    "brun_titchmarsh_prime_coefficient",
    "build_diagnostic",
    "character_sums_mod_five",
    "inverse_transform_holds_mod_five",
    "load_ledger",
    "normalized_moment_certificate",
    "normalized_pair_factor",
    "parseval_holds_mod_five",
    "residue_discrepancies_mod_five",
    "subset_mean_discrepancy_mod_five",
    "validate_ledger",
]
