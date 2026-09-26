"""Exact finite checks for the DEP-R09 blind fixed-modulus reduction.

Blind characters modulo q=f*h are characters modulo f inflated by the
principal character modulo h. Their von Mangoldt sums differ from the native
modulo-f sums only at prime powers whose base prime divides h.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_blind_fixed_modulus_reduction_v1.json"
)


def _integer(value: object, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _fraction(value: object, name: str, *, positive: bool = False) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def lifted_sum_decomposition(
    terms: Iterable[tuple[int, int, Fraction, int]],
    excluded_base_primes: Iterable[int],
) -> dict[str, Fraction]:
    """Return native, lifted, and removed prime-power sums exactly."""

    excluded = frozenset(
        _integer(prime, "excluded prime", minimum=2)
        for prime in excluded_base_primes
    )
    native = Fraction(0)
    lifted = Fraction(0)
    removed = Fraction(0)
    seen: set[tuple[int, int]] = set()
    for base_prime, exponent, weight, character_value in terms:
        base_prime = _integer(base_prime, "base_prime", minimum=2)
        exponent = _integer(exponent, "exponent", minimum=1)
        weight = _fraction(weight, "weight")
        if character_value not in (-1, 0, 1):
            raise ValueError("character_value must be -1, 0, or 1")
        key = (base_prime, exponent)
        if key in seen:
            raise ValueError("prime-power terms must be distinct")
        seen.add(key)
        contribution = weight * character_value
        native += contribution
        if base_prime in excluded:
            removed += contribution
        else:
            lifted += contribution
    if lifted != native - removed:
        raise AssertionError("lifted decomposition failed")
    return {"native": native, "lifted": lifted, "removed": removed}


def correction_pointwise_upper(
    randomized_prime_count: int,
    log_prime_scale: Fraction,
) -> Fraction:
    """Return omega(h)*log(U)."""

    randomized_prime_count = _integer(
        randomized_prime_count, "randomized_prime_count"
    )
    log_prime_scale = _fraction(
        log_prime_scale, "log_prime_scale", positive=True
    )
    return randomized_prime_count * log_prime_scale


def transferred_energy_upper(
    native_energy: Fraction,
    character_count: int,
    correction_upper: Fraction,
    eta: Fraction = Fraction(1),
) -> Fraction:
    """Return a flexible native-plus-correction energy upper."""

    native_energy = _fraction(native_energy, "native_energy")
    correction_upper = _fraction(correction_upper, "correction_upper")
    eta = _fraction(eta, "eta", positive=True)
    character_count = _integer(character_count, "character_count")
    if native_energy < 0 or correction_upper < 0:
        raise ValueError("energies and correction upper must be nonnegative")
    return (
        (1 + eta) * native_energy
        + (1 + 1 / eta) * character_count * correction_upper**2
    )


def blind_uniform_gate(
    tau: Fraction,
    minimum_survivors: Fraction,
    prime_scale: Fraction,
    phi_fixed: Fraction,
) -> Fraction:
    """Return the strict uniform blind-energy target."""

    tau = _fraction(tau, "tau", positive=True)
    minimum_survivors = _fraction(
        minimum_survivors, "minimum_survivors", positive=True
    )
    prime_scale = _fraction(
        prime_scale, "prime_scale", positive=True
    )
    phi_fixed = _fraction(phi_fixed, "phi_fixed", positive=True)
    if minimum_survivors >= phi_fixed:
        raise ValueError("minimum_survivors must be below phi_fixed")
    return (
        tau**2
        * minimum_survivors
        * prime_scale**2
        / (phi_fixed - minimum_survivors)
    )


def split_budget_suffices(
    native_energy: Fraction,
    correction_energy: Fraction,
    target: Fraction,
) -> bool:
    """Use the eta=1 transfer with two strict quarter-budgets."""

    native_energy = _fraction(native_energy, "native_energy")
    correction_energy = _fraction(
        correction_energy, "correction_energy"
    )
    target = _fraction(target, "target", positive=True)
    if native_energy < 0 or correction_energy < 0:
        raise ValueError("energy inputs must be nonnegative")
    return native_energy < target / 4 and correction_energy < target / 4


def effective_fixed_modulus_exponent_upper(d: int) -> Fraction:
    """Return (105/47)*d."""

    d = _integer(d, "d", minimum=1)
    return Fraction(105 * d, 47)


def effective_fixed_modulus_exponent_interval(
    d: int,
) -> tuple[Fraction, Fraction]:
    """Return d <= d_f < 105d/47."""

    d = _integer(d, "d", minimum=1)
    return Fraction(d), effective_fixed_modulus_exponent_upper(d)


@dataclass(frozen=True)
class BlindFixedModulusDiagnostic:
    lifted_native_prime_power_identity_exact: bool
    correction_pointwise_bound_exact: bool
    flexible_energy_transfer_exact: bool
    eta_one_quarter_budget_interface_exact: bool
    toy_native_sum: str
    toy_removed_sum: str
    toy_lifted_sum: str
    toy_correction_upper: str
    toy_transferred_energy_upper: str
    d_min: int
    d_max: int
    effective_exponent_lower: str
    effective_exponent_upper_at_d_max: str
    effective_exponent_upper_below_416: bool
    bennett_large_modulus_cutoff_overlaps_effective_range: bool
    vaughan_unconditional_fixed_a_covers_growing_fixed_modulus: bool
    friedlander_goldston_unconditional_numerical_upper_identified: bool
    native_fixed_modulus_energy_upper_identified: bool
    imprimitive_correction_is_the_analytic_core_blocker: bool
    blind_prime_error_correlation_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> BlindFixedModulusDiagnostic:
    decomposition = lifted_sum_decomposition(
        (
            (2, 1, Fraction(2), 1),
            (2, 2, Fraction(2), -1),
            (3, 1, Fraction(3), -1),
            (5, 1, Fraction(5), 1),
        ),
        (2, 3),
    )
    correction_upper = correction_pointwise_upper(2, Fraction(7))
    transferred = transferred_energy_upper(
        Fraction(9), 4, Fraction(3), Fraction(1)
    )
    _, exponent_upper = effective_fixed_modulus_exponent_interval(186)
    return BlindFixedModulusDiagnostic(
        lifted_native_prime_power_identity_exact=(
            decomposition["lifted"]
            == decomposition["native"] - decomposition["removed"]
        ),
        correction_pointwise_bound_exact=True,
        flexible_energy_transfer_exact=True,
        eta_one_quarter_budget_interface_exact=True,
        toy_native_sum=str(decomposition["native"]),
        toy_removed_sum=str(decomposition["removed"]),
        toy_lifted_sum=str(decomposition["lifted"]),
        toy_correction_upper=str(correction_upper),
        toy_transferred_energy_upper=str(transferred),
        d_min=21,
        d_max=186,
        effective_exponent_lower="21",
        effective_exponent_upper_at_d_max=str(exponent_upper),
        effective_exponent_upper_below_416=(exponent_upper < 416),
        bennett_large_modulus_cutoff_overlaps_effective_range=False,
        vaughan_unconditional_fixed_a_covers_growing_fixed_modulus=False,
        friedlander_goldston_unconditional_numerical_upper_identified=False,
        native_fixed_modulus_energy_upper_identified=False,
        imprimitive_correction_is_the_analytic_core_blocker=False,
        blind_prime_error_correlation_closed=False,
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
    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != (
        "DEP-R09 blind fixed-modulus and imprimitive-correction reduction"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "BLIND_ENERGY_REDUCED_TO_NATIVE_FIXED_MODULUS_PLUS_EXPLICIT_"
        "PRIME_POWER_CORRECTION_BUT_NO_NUMERICAL_NATIVE_UPPER"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove or source a fully numerical unconditional native character-"
        "energy upper for the prescribed fixed-coordinate modulus f, or "
        "control the blind weighted correlation directly; the imprimitive "
        "prime-power correction is now an explicit secondary gate."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 7:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "VAUGHAN2001", "FRIEDLANDER_GOLDSTON1996", "THEORY76",
        "THEORY83", "THEORY85", "THEORY89", "GKM2020",
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
    "blind_uniform_gate",
    "build_diagnostic",
    "correction_pointwise_upper",
    "effective_fixed_modulus_exponent_interval",
    "effective_fixed_modulus_exponent_upper",
    "lifted_sum_decomposition",
    "load_ledger",
    "split_budget_suffices",
    "transferred_energy_upper",
    "validate_ledger",
]
