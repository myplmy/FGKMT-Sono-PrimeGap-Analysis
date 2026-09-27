"""Exact checks for the DEP-R09 fixed-Q' bilinear reduction.

The helper verifies the centered residue kernel, the prime/prime-power split,
the reindexing of the positive prime-pair mass, and the logical boundary of a
one-sided upper-bound sieve.  It performs no actual prime search.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_fixed_qprime_bilinear_v1.json"
)


def _fraction(value: object, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    return value


def _validate_phi_and_residues(
    modulus: int,
    phi: int,
    selected_residues: Sequence[int],
) -> tuple[int, ...]:
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer at least two")
    if isinstance(phi, bool) or not isinstance(phi, int) or not 1 <= phi < modulus:
        raise ValueError("phi must be an integer in [1,modulus)")
    residues = tuple(selected_residues)
    if not residues or len(set(residues)) != len(residues):
        raise ValueError("selected residues must be nonempty and distinct")
    if any(
        isinstance(residue, bool)
        or not isinstance(residue, int)
        or not 0 <= residue < modulus
        for residue in residues
    ):
        raise ValueError("selected residue out of range")
    return residues


def centered_residue_kernel(
    phi: int,
    selected_count: int,
    selected: bool,
) -> int:
    """Return phi*1_selected-N, the kernel after summing over Q'."""

    if isinstance(phi, bool) or not isinstance(phi, int) or phi < 1:
        raise ValueError("phi must be positive")
    if (
        isinstance(selected_count, bool)
        or not isinstance(selected_count, int)
        or not 0 <= selected_count <= phi
    ):
        raise ValueError("selected_count must lie in [0,phi]")
    if not isinstance(selected, bool):
        raise TypeError("selected must be bool")
    return (phi if selected else 0) - selected_count


def centered_mean_from_terms(
    modulus: int,
    phi: int,
    selected_residues: Sequence[int],
    terms: Sequence[tuple[int, Fraction]],
) -> Fraction:
    """Return sum_n weight(n)*(phi*1_[n in Q']-N)."""

    residues = _validate_phi_and_residues(modulus, phi, selected_residues)
    selected = set(residues)
    total = Fraction(0)
    for index, item in enumerate(terms):
        if not isinstance(item, tuple) or len(item) != 2:
            raise TypeError(f"term[{index}] must be a pair")
        integer, weight = item
        if isinstance(integer, bool) or not isinstance(integer, int) or integer < 1:
            raise ValueError(f"term[{index}] integer must be positive")
        weight = _fraction(weight, f"term[{index}] weight")
        total += weight * centered_residue_kernel(
            phi, len(residues), integer % modulus in selected
        )
    return total


def original_fixed_mean(
    modulus: int,
    phi: int,
    selected_residues: Sequence[int],
    terms: Sequence[tuple[int, Fraction]],
) -> Fraction:
    """Compute phi*sum_q A(q)-N*S directly."""

    residues = _validate_phi_and_residues(modulus, phi, selected_residues)
    masses = {residue: Fraction(0) for residue in residues}
    principal = Fraction(0)
    for index, (integer, weight) in enumerate(terms):
        if isinstance(integer, bool) or not isinstance(integer, int) or integer < 1:
            raise ValueError(f"term[{index}] integer must be positive")
        weight = _fraction(weight, f"term[{index}] weight")
        principal += weight
        residue = integer % modulus
        if residue in masses:
            masses[residue] += weight
    return phi * sum(masses.values(), Fraction(0)) - len(residues) * principal


def split_centered_mean(
    modulus: int,
    phi: int,
    selected_residues: Sequence[int],
    prime_terms: Sequence[tuple[int, Fraction]],
    prime_power_terms: Sequence[tuple[int, Fraction]],
) -> dict[str, Fraction]:
    prime = centered_mean_from_terms(
        modulus, phi, selected_residues, prime_terms
    )
    prime_power = centered_mean_from_terms(
        modulus, phi, selected_residues, prime_power_terms
    )
    combined_terms = tuple(prime_terms) + tuple(prime_power_terms)
    original = original_fixed_mean(
        modulus, phi, selected_residues, combined_terms
    )
    if original != prime + prime_power:
        raise AssertionError("prime/prime-power split is not exact")
    return {
        "prime": prime,
        "prime_power": prime_power,
        "combined": original,
    }


def positive_pair_mass(
    modulus: int,
    selected_residues: Sequence[int],
    prime_terms: Sequence[tuple[int, Fraction]],
) -> Fraction:
    """Return sum of prime weights in selected residue classes."""

    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer at least two")
    selected = set(selected_residues)
    if not selected or len(selected) != len(tuple(selected_residues)):
        raise ValueError("selected residues must be nonempty and distinct")
    total = Fraction(0)
    for index, (prime, weight) in enumerate(prime_terms):
        if isinstance(prime, bool) or not isinstance(prime, int) or prime < 1:
            raise ValueError(f"prime_terms[{index}] integer must be positive")
        weight = _fraction(weight, f"prime_terms[{index}] weight")
        if prime % modulus in selected:
            total += weight
    return total


def centered_prime_bilinear(
    modulus: int,
    phi: int,
    selected_residues: Sequence[int],
    prime_terms: Sequence[tuple[int, Fraction]],
) -> Fraction:
    """Return phi*positive_pair_mass-N*principal_prime_mass."""

    residues = _validate_phi_and_residues(modulus, phi, selected_residues)
    pair_mass = positive_pair_mass(modulus, residues, prime_terms)
    principal = sum(
        (_fraction(weight, f"prime_terms[{index}] weight")
         for index, (_, weight) in enumerate(prime_terms)),
        Fraction(0),
    )
    return phi * pair_mass - len(residues) * principal


def reindex_selected_prime_terms(
    modulus: int,
    selected_residues: Sequence[int],
    prime_terms: Sequence[tuple[int, Fraction]],
) -> tuple[tuple[int, int, Fraction], ...]:
    """Return (q,ell,weight) for p=q+ell*f in selected residues.

    The caller supplies only terms in the range where q is the unique integer
    representative of its selected residue, as in Q'<f.
    """

    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer at least two")
    residues = tuple(selected_residues)
    if not residues or len(set(residues)) != len(residues):
        raise ValueError("selected residues must be nonempty and distinct")
    if any(not 0 < residue < modulus for residue in residues):
        raise ValueError("selected representatives must lie in (0,modulus)")
    selected = set(residues)
    result: list[tuple[int, int, Fraction]] = []
    for index, (prime, weight) in enumerate(prime_terms):
        if isinstance(prime, bool) or not isinstance(prime, int) or prime < 1:
            raise ValueError(f"prime_terms[{index}] integer must be positive")
        weight = _fraction(weight, f"prime_terms[{index}] weight")
        residue = prime % modulus
        if residue in selected:
            quotient, remainder = divmod(prime - residue, modulus)
            if remainder != 0 or quotient < 0:
                raise AssertionError("invalid residue reindexing")
            result.append((residue, quotient, weight))
    return tuple(result)


def prime_power_kernel_envelope(phi: int, selected_count: int) -> int:
    """Return max(|-N|,|phi-N|) for the two possible kernel values."""

    if isinstance(phi, bool) or not isinstance(phi, int) or phi < 1:
        raise ValueError("phi must be positive")
    if (
        isinstance(selected_count, bool)
        or not isinstance(selected_count, int)
        or not 0 <= selected_count <= phi
    ):
        raise ValueError("selected_count must lie in [0,phi]")
    return max(selected_count, abs(phi - selected_count))


def prime_power_correction_upper(
    phi: int,
    selected_count: int,
    prime_power_mass: Fraction,
) -> Fraction:
    mass = _fraction(prime_power_mass, "prime_power_mass")
    if mass < 0:
        raise ValueError("prime_power_mass must be nonnegative")
    return prime_power_kernel_envelope(phi, selected_count) * mass


def relative_correction_upper(
    correction: Fraction,
    selected_count: int,
    prime_scale: Fraction,
) -> Fraction:
    correction = _fraction(correction, "correction")
    scale = _fraction(prime_scale, "prime_scale")
    if correction < 0 or scale <= 0:
        raise ValueError("correction must be nonnegative and scale positive")
    if (
        isinstance(selected_count, bool)
        or not isinstance(selected_count, int)
        or selected_count < 1
    ):
        raise ValueError("selected_count must be positive")
    return correction / (selected_count * scale)


def one_sided_upper_countermodel(
    main_mass: Fraction,
    upper_multiplier: Fraction,
) -> dict[str, Fraction | bool]:
    """Exhibit pair_mass=0 under any nonnegative one-sided upper.

    For a centered expression phi*pair_mass-N*main_mass, the absolute error is
    N*main_mass.  Thus an upper bound alone cannot imply a relative error < 1.
    The normalized model sets phi=N=1.
    """

    main = _fraction(main_mass, "main_mass")
    multiplier = _fraction(upper_multiplier, "upper_multiplier")
    if main <= 0 or multiplier < 0:
        raise ValueError("main_mass must be positive and multiplier nonnegative")
    pair = Fraction(0)
    centered = pair - main
    return {
        "pair_mass": pair,
        "upper_bound": multiplier * main,
        "upper_holds": pair <= multiplier * main,
        "centered": centered,
        "relative_absolute_error": abs(centered) / main,
    }


@dataclass(frozen=True)
class FixedQPrimeBilinearDiagnostic:
    centered_kernel_identity_exact: bool
    prime_prime_power_split_exact: bool
    positive_pair_reindex_exact: bool
    prime_power_envelope_exact: bool
    signed_fixture_prime_component: str
    signed_fixture_prime_power_component: str
    signed_fixture_total: str
    upper_only_countermodel_holds: bool
    upper_only_relative_error: str
    sono_upper_bound_source_verified: bool
    sono_upper_bound_is_one_sided: bool
    r10_direct_drop_in_for_centered_mean: bool
    b0_and_prime_power_corrections_parameterized_explicit: bool
    centered_binary_prime_gate_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> FixedQPrimeBilinearDiagnostic:
    modulus = 5
    phi = 4
    selected = (1, 2)
    prime_terms = (
        (1, Fraction(2)),
        (2, Fraction(3)),
        (3, Fraction(5)),
        (6, Fraction(7)),
    )
    prime_power_terms = ((4, Fraction(11)), (8, Fraction(13)))
    split = split_centered_mean(
        modulus, phi, selected, prime_terms, prime_power_terms
    )
    reindexed = reindex_selected_prime_terms(modulus, selected, prime_terms)
    pair_mass = positive_pair_mass(modulus, selected, prime_terms)
    countermodel = one_sided_upper_countermodel(Fraction(7), Fraction(8))
    return FixedQPrimeBilinearDiagnostic(
        centered_kernel_identity_exact=(
            centered_mean_from_terms(
                modulus,
                phi,
                selected,
                prime_terms + prime_power_terms,
            )
            == original_fixed_mean(
                modulus,
                phi,
                selected,
                prime_terms + prime_power_terms,
            )
        ),
        prime_prime_power_split_exact=(
            split["combined"] == split["prime"] + split["prime_power"]
        ),
        positive_pair_reindex_exact=(
            sum((weight for _, _, weight in reindexed), Fraction(0))
            == pair_mass
        ),
        prime_power_envelope_exact=(
            prime_power_kernel_envelope(phi, len(selected)) == 2
        ),
        signed_fixture_prime_component=str(split["prime"]),
        signed_fixture_prime_power_component=str(split["prime_power"]),
        signed_fixture_total=str(split["combined"]),
        upper_only_countermodel_holds=bool(countermodel["upper_holds"]),
        upper_only_relative_error=str(countermodel["relative_absolute_error"]),
        sono_upper_bound_source_verified=True,
        sono_upper_bound_is_one_sided=True,
        r10_direct_drop_in_for_centered_mean=False,
        b0_and_prime_power_corrections_parameterized_explicit=True,
        centered_binary_prime_gate_closed=False,
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
        "DEP-R09 fixed-Q-prime pre-absolute-value bilinear reduction"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "FIXED_MEAN_EXACTLY_SPLIT_INTO_CENTERED_BINARY_PRIME_FORM_AND_"
        "EXPLICIT_CORRECTIONS_BUT_ONE_SIDED_R10_CANNOT_CLOSE_SIGNED_GATE"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove a two-sided pre-absolute-value estimate for the centered "
        "binary-prime form; the existing R10/Selberg upper controls only the "
        "positive pair mass and cannot certify cancellation against its main term."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 4:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"SONO2025", "THEORY77", "THEORY93", "FGKMT"}
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
    "centered_mean_from_terms",
    "centered_prime_bilinear",
    "centered_residue_kernel",
    "load_ledger",
    "one_sided_upper_countermodel",
    "original_fixed_mean",
    "positive_pair_mass",
    "prime_power_correction_upper",
    "prime_power_kernel_envelope",
    "reindex_selected_prime_terms",
    "relative_correction_upper",
    "split_centered_mean",
    "validate_ledger",
]
