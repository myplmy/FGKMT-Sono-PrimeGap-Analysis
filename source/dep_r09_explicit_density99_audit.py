"""Exact diagnostics for the DEP-R09 explicit density-exponent-99 route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_explicit_density99_route_v1.json"
)

EXPLICIT_DENSITY_EXPONENT = 99
CURRENT_EFFECTIVE_EXPONENT_UPPER = 416
MCCURLEY_C = Fraction(10**9, 9_645_908_801)


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def epsilon_ceiling(
    d_upper: int = CURRENT_EFFECTIVE_EXPONENT_UPPER,
    density_exponent: int = EXPLICIT_DENSITY_EXPONENT,
) -> Fraction:
    d_value = _positive_int(d_upper, "d_upper")
    c_value = _positive_int(density_exponent, "density_exponent")
    if d_value <= c_value:
        raise ValueError("d_upper must exceed the density exponent")
    return Fraction(1, c_value) - Fraction(1, d_value)


def decay_exponent_upper(
    d_upper: int = CURRENT_EFFECTIVE_EXPONENT_UPPER,
    density_exponent: int = EXPLICIT_DENSITY_EXPONENT,
    zero_free_constant: Fraction = MCCURLEY_C,
) -> Fraction:
    c_value = zero_free_constant
    if not isinstance(c_value, Fraction) or c_value <= 0:
        raise ValueError("zero_free_constant must be a positive Fraction")
    epsilon = epsilon_ceiling(d_upper, density_exponent)
    return epsilon * epsilon * c_value * d_upper


def optimistic_sup_factor_floor(
    d_lower_strict: int = EXPLICIT_DENSITY_EXPONENT,
) -> Fraction:
    """Return the strict rational floor d*(997/1000)*(1/2)."""

    d_value = _positive_int(d_lower_strict, "d_lower_strict")
    return Fraction(d_value * 997, 2000)


def density_sigma_floor(
    density_exponent: int = EXPLICIT_DENSITY_EXPONENT,
) -> Fraction:
    c_value = _positive_int(density_exponent, "density_exponent")
    return Fraction(c_value - 1, c_value)


@dataclass(frozen=True)
class ExplicitDensity99Diagnostic:
    primary_pdf_verified: bool
    theorem_12_sigma_floor: str
    theorem_12_density_exponent: int
    theorem_12_absolute_multiplier: str
    theorem_12_base_multiplier: str
    fixed_family_is_subset_of_modulus_height_box: bool
    proof_sigma_floor_above_39_over_40: bool
    positive_range_requires_d_f_above_99: bool
    current_range_overlaps_density99: bool
    epsilon_ceiling_at_d_f_416: str
    explicit_zero_free_constant: str
    decay_exponent_upper_at_current_range: str
    decay_exponent_upper_below_3_over_1000: bool
    optimistic_sup_factor_floor: str
    optimistic_sup_factor_floor_exceeds_49: bool
    multiplier_one_direct_certificate_closes_endpoint_gate: bool
    density99_direct_black_box_route_closed: bool
    sharp_density_12_over_5_numerical: bool
    centered_endpoint_gate_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_or_zero_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> ExplicitDensity99Diagnostic:
    exponent_upper = decay_exponent_upper()
    factor_floor = optimistic_sup_factor_floor()
    return ExplicitDensity99Diagnostic(
        primary_pdf_verified=True,
        theorem_12_sigma_floor="39/40",
        theorem_12_density_exponent=99,
        theorem_12_absolute_multiplier="10^88",
        theorem_12_base_multiplier="10^421",
        fixed_family_is_subset_of_modulus_height_box=True,
        proof_sigma_floor_above_39_over_40=(
            density_sigma_floor() > Fraction(39, 40)
        ),
        positive_range_requires_d_f_above_99=True,
        current_range_overlaps_density99=True,
        epsilon_ceiling_at_d_f_416=str(epsilon_ceiling()),
        explicit_zero_free_constant=str(MCCURLEY_C),
        decay_exponent_upper_at_current_range=str(exponent_upper),
        decay_exponent_upper_below_3_over_1000=(
            exponent_upper < Fraction(3, 1000)
        ),
        optimistic_sup_factor_floor=str(factor_floor),
        optimistic_sup_factor_floor_exceeds_49=(factor_floor > 49),
        multiplier_one_direct_certificate_closes_endpoint_gate=False,
        density99_direct_black_box_route_closed=False,
        sharp_density_12_over_5_numerical=False,
        centered_endpoint_gate_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        numerical_x_cert_ready=False,
        bounded_x_cert_range_obtained=False,
        threshold_calculator_ready=False,
        actual_prime_or_zero_computation_run=False,
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
    if document.get("gate") != "DEP-R09 explicit density-exponent-99 route audit":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "EXPLICIT_DENSITY99_RANGE_OVERLAPS_BUT_DIRECT_THEOREM23_"
        "CERTIFICATE_FAILS_EVEN_AT_MULTIPLIER_ONE"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Numericalize the sharp nonexceptional exponent-12/5 density route "
        "or supply a structurally different full-interval proof; do not use "
        "the explicit exponent-99 theorem as a direct small-error certificate."
    ):
        issues.append("next_gate mismatch")
    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 5:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "THEORY58",
        "THEORY90",
        "THEORY98",
        "TZ_EXPLICIT_DENSITY",
        "TZ_PNT",
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
    "CURRENT_EFFECTIVE_EXPONENT_UPPER",
    "EXPLICIT_DENSITY_EXPONENT",
    "LEDGER_PATH",
    "MCCURLEY_C",
    "build_diagnostic",
    "decay_exponent_upper",
    "density_sigma_floor",
    "epsilon_ceiling",
    "load_ledger",
    "optimistic_sup_factor_floor",
    "validate_ledger",
]
