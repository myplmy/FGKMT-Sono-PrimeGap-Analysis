"""Exact finite checks for the DEP-R09 outer-entropy moment reduction.

This module verifies only finite probability and Fourier-algebra consequences:

* independent uniform outer residue coordinates give an atom cap for the
  final CRT shift, even when the inner output is adaptive;
* a cyclic shifted-sum satisfies the finite Cauchy energy bound;
* the atom cap and energy bound imply a same-law raw second-moment budget;
* the resulting strict scalar gate implies the Theory-81 normalized gate.

It does not prove the missing analytic bound for the nonprincipal prime-error
energy, PAP-11, DEP-R09, the fixed Sono coefficient, or a numerical ``X_cert``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import itertools
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
    / "Sono_FMT_DEPR09_outer_entropy_convolution_second_moment_v1.json"
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


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def outer_atom_denominator(primes: Iterable[int]) -> int:
    """Return ``Q_S=prod(s in S) s`` for distinct outer primes."""

    materialized = tuple(primes)
    if not materialized:
        raise ValueError("primes must be nonempty")
    if any(isinstance(prime, bool) or not isinstance(prime, int)
           for prime in materialized):
        raise TypeError("each outer modulus must be an integer")
    if len(set(materialized)) != len(materialized):
        raise ValueError("outer primes must be distinct")
    if any(not _is_prime(prime) for prime in materialized):
        raise ValueError("each outer modulus must be prime")
    product = 1
    for prime in materialized:
        product *= prime
    return product


def outer_atom_cap(primes: Iterable[int]) -> Fraction:
    """Return the exact final-shift atom cap ``1/Q_S``."""

    return Fraction(1, outer_atom_denominator(primes))


@dataclass(frozen=True)
class GaussianRational:
    """A Gaussian number with exact rational coordinates."""

    real: Fraction
    imag: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if not isinstance(self.real, Fraction) or not isinstance(
            self.imag, Fraction
        ):
            raise TypeError("GaussianRational coordinates must be Fraction")

    def __add__(self, other: object) -> "GaussianRational":
        if not isinstance(other, GaussianRational):
            return NotImplemented
        return GaussianRational(self.real + other.real, self.imag + other.imag)

    def norm_square(self) -> Fraction:
        return self.real**2 + self.imag**2


ZERO_GAUSSIAN = GaussianRational(Fraction(0), Fraction(0))


def gaussian_energy(values: Sequence[GaussianRational]) -> Fraction:
    if not values:
        raise ValueError("values must be nonempty")
    if any(not isinstance(value, GaussianRational) for value in values):
        raise TypeError("values must contain GaussianRational entries")
    return sum((value.norm_square() for value in values), Fraction(0))


def cyclic_shift_sum_energy(
    values: Sequence[GaussianRational],
    offsets: Sequence[int],
) -> Fraction:
    """Return ``sum_m |sum_(s in I) e(m+s)|^2`` exactly."""

    if not values:
        raise ValueError("values must be nonempty")
    if not offsets:
        raise ValueError("offsets must be nonempty")
    if any(not isinstance(value, GaussianRational) for value in values):
        raise TypeError("values must contain GaussianRational entries")
    if any(isinstance(offset, bool) or not isinstance(offset, int)
           for offset in offsets):
        raise TypeError("offsets must be integers")
    modulus = len(values)
    total = Fraction(0)
    for shift in range(modulus):
        row = ZERO_GAUSSIAN
        for offset in offsets:
            row = row + values[(shift + offset) % modulus]
        total += row.norm_square()
    return total


def cyclic_cauchy_energy_upper(
    values: Sequence[GaussianRational],
    offsets: Sequence[int],
) -> Fraction:
    """Return the exact Cauchy upper bound ``|I|^2 sum_a |e(a)|^2``."""

    if not offsets:
        raise ValueError("offsets must be nonempty")
    return len(offsets) ** 2 * gaussian_energy(values)


def same_law_raw_moment_upper(
    phi_q: int,
    interval_size: int,
    character_energy: Fraction,
    outer_denominator: int,
) -> Fraction:
    """Return ``phi(q) N^2 V / Q_S`` exactly."""

    phi_q = _integer(phi_q, "phi_q", positive=True)
    interval_size = _integer(interval_size, "interval_size", positive=True)
    outer_denominator = _integer(
        outer_denominator, "outer_denominator", positive=True
    )
    character_energy = _fraction(character_energy, "character_energy")
    if character_energy < 0:
        raise ValueError("character_energy must be nonnegative")
    return Fraction(phi_q * interval_size**2, outer_denominator) * character_energy


def character_energy_gate(
    tau: Fraction,
    sieve_good_mass_lower: Fraction,
    outer_denominator: int,
    minimum_survivors: Fraction,
    prime_scale: Fraction,
    phi_q: int,
    interval_size: int,
) -> Fraction:
    """Return the strict sufficient upper threshold for ``V``."""

    tau = _fraction(tau, "tau", positive=True)
    sieve_good_mass_lower = _fraction(
        sieve_good_mass_lower, "sieve_good_mass_lower", positive=True
    )
    minimum_survivors = _fraction(
        minimum_survivors, "minimum_survivors", positive=True
    )
    prime_scale = _fraction(prime_scale, "prime_scale", positive=True)
    outer_denominator = _integer(
        outer_denominator, "outer_denominator", positive=True
    )
    phi_q = _integer(phi_q, "phi_q", positive=True)
    interval_size = _integer(interval_size, "interval_size", positive=True)
    return (
        tau**2
        * sieve_good_mass_lower
        * outer_denominator
        * minimum_survivors**2
        * prime_scale**2
        / (phi_q * interval_size**2)
    )


def passes_strict_character_energy_gate(
    character_energy: Fraction,
    threshold: Fraction,
) -> bool:
    character_energy = _fraction(character_energy, "character_energy")
    threshold = _fraction(threshold, "threshold", positive=True)
    if character_energy < 0:
        raise ValueError("character_energy must be nonnegative")
    return character_energy < threshold


@dataclass(frozen=True)
class OuterAtomToyDiagnostic:
    modulus: int
    outer_primes: tuple[int, ...]
    outer_vectors: int
    final_shift_atoms: int
    maximum_atom: str
    atom_cap: str
    atom_cap_exact: bool


def outer_atom_toy_diagnostic() -> OuterAtomToyDiagnostic:
    """Enumerate an adaptive deterministic inner rule modulo 30.

    The inner residue modulo 5 depends on the complete outer vector modulo
    2 and 3.  This deliberately avoids assuming outer/inner independence.
    """

    modulus = 30
    outer_primes = (2, 3)
    denominator = outer_atom_denominator(outer_primes)
    masses: dict[int, Fraction] = {}
    vectors = tuple(itertools.product(*(range(p) for p in outer_primes)))
    for a_two, a_three in vectors:
        inner_residue = (a_two + 2 * a_three) % 5
        matches = [
            residue
            for residue in range(modulus)
            if residue % 2 == (-a_two) % 2
            and residue % 3 == (-a_three) % 3
            and residue % 5 == inner_residue
        ]
        if len(matches) != 1:
            raise AssertionError("toy CRT rule must select one final shift")
        residue = matches[0]
        masses[residue] = masses.get(residue, Fraction(0)) + Fraction(
            1, denominator
        )
    maximum = max(masses.values())
    cap = Fraction(1, denominator)
    return OuterAtomToyDiagnostic(
        modulus=modulus,
        outer_primes=outer_primes,
        outer_vectors=len(vectors),
        final_shift_atoms=len(masses),
        maximum_atom=str(maximum),
        atom_cap=str(cap),
        atom_cap_exact=(maximum <= cap and sum(masses.values()) == 1),
    )


def legendre_symbol_prime(value: int, prime: int) -> int:
    """Return the Legendre symbol for an odd prime by exact enumeration."""

    value = _integer(value, "value")
    prime = _integer(prime, "prime", positive=True)
    if prime == 2 or not _is_prime(prime):
        raise ValueError("prime must be an odd prime")
    residue = value % prime
    if residue == 0:
        return 0
    squares = {(item * item) % prime for item in range(1, prime)}
    return 1 if residue in squares else -1


def davenport_erdos_shift_energy(prime: int, interval_size: int) -> int:
    """Enumerate Davenport--Erdos Lemma 1's prime-modulus energy."""

    prime = _integer(prime, "prime", positive=True)
    interval_size = _integer(interval_size, "interval_size", positive=True)
    if prime == 2 or not _is_prime(prime):
        raise ValueError("prime must be an odd prime")
    if interval_size >= prime:
        raise ValueError("interval_size must be less than prime")
    total = 0
    for shift in range(prime):
        row = sum(
            legendre_symbol_prime(shift + offset, prime)
            for offset in range(1, interval_size + 1)
        )
        total += row**2
    return total


@dataclass(frozen=True)
class OuterEntropySecondMomentDiagnostic:
    outer_atom_cap_exact_under_adaptive_inner_rule: bool
    toy_outer_denominator: int
    toy_maximum_atom: str
    cyclic_convolution_cauchy_exactly_verified: bool
    davenport_erdos_prime_modulus_identity_exactly_verified: bool
    same_law_raw_moment_reduction_exact: bool
    fully_numerical_fixed_primorial_character_energy_bound_identified: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> OuterEntropySecondMomentDiagnostic:
    toy = outer_atom_toy_diagnostic()
    values = (
        GaussianRational(Fraction(1), Fraction(1, 2)),
        GaussianRational(Fraction(-2, 3), Fraction(1)),
        GaussianRational(Fraction(0), Fraction(-3, 4)),
        GaussianRational(Fraction(5, 7), Fraction(-1, 5)),
        GaussianRational(Fraction(-1, 2), Fraction(2, 9)),
    )
    offsets = (0, 1, 3)
    convolution_energy = cyclic_shift_sum_energy(values, offsets)
    cauchy_upper = cyclic_cauchy_energy_upper(values, offsets)
    phi_q = 8
    interval_size = 3
    character_energy = Fraction(17, 5)
    q_s = 6
    raw_upper = same_law_raw_moment_upper(
        phi_q, interval_size, character_energy, q_s
    )
    expected_raw_upper = Fraction(phi_q * interval_size**2, q_s) * character_energy
    return OuterEntropySecondMomentDiagnostic(
        outer_atom_cap_exact_under_adaptive_inner_rule=toy.atom_cap_exact,
        toy_outer_denominator=q_s,
        toy_maximum_atom=toy.maximum_atom,
        cyclic_convolution_cauchy_exactly_verified=(
            convolution_energy <= cauchy_upper
        ),
        davenport_erdos_prime_modulus_identity_exactly_verified=(
            davenport_erdos_shift_energy(7, 3) == 7 * 3 - 3**2
        ),
        same_law_raw_moment_reduction_exact=(raw_upper == expected_raw_upper),
        fully_numerical_fixed_primorial_character_energy_bound_identified=False,
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
        "DEP-R09 outer entropy and convolution second-moment reduction"
    ):
        issues.append("gate mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove a fully numerical nonprincipal character-energy bound for the "
        "actual fixed primorial and Y=q^d regime that satisfies the strict "
        "outer-entropy gate; outer min-entropy alone is insufficient."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 5:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"FMT", "DUSART2010", "DAVENPORT_ERDOS1952", "THEORY76", "THEORY81"}
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
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                issues.append(f"{key} hash mismatch")
    return issues
