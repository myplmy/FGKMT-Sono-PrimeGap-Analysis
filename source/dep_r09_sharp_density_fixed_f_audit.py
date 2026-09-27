"""Exact diagnostics for the sharp near-one density fixed-f specialization."""

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
    / "Sono_FMT_DEPR09_sharp_density_fixed_f_v1.json"
)

MCCURLEY_C = Fraction(10**9, 9_645_908_801)
TIGHT_DENSITY_COEFFICIENT = Fraction(11_503_697_604_450_072, 425_315)


def detector_kappa(window: Fraction = Fraction(1, 21)) -> Fraction:
    if not isinstance(window, Fraction) or not 0 < window <= Fraction(1, 21):
        raise ValueError("window must be a Fraction in (0,1/21]")
    return 14 * (1 + 12 * window)


def favorable_decay_exponent_upper() -> Fraction:
    """Use d_f<416 and kappa>=14 in c_M*(d_f-kappa)/5."""

    return MCCURLEY_C * Fraction(416 - 14, 5)


def tightened_coefficient_floor() -> Fraction:
    """Drop every prefactor and use exp(-x)>3^-9 when x<9."""

    return TIGHT_DENSITY_COEFFICIENT / (3**9)


def theta_power_counterfactual_floor() -> Fraction:
    """Retain only window^-6 at the most favorable window 1/21."""

    return Fraction(21**6, 3**9)


@dataclass(frozen=True)
class SharpDensityFixedFDiagnostic:
    theory71_source_hash_verified: bool
    theory73_source_hash_verified: bool
    fixed_family_parameters: str
    detector_window: str
    detector_kappa_at_one_over_21: str
    positive_decay_requires_d_f_above_22: bool
    current_d_f_upper: str
    explicit_zero_free_constant: str
    favorable_decay_exponent_upper: str
    favorable_decay_exponent_below_9: bool
    tightened_density_coefficient: str
    tightened_core_floor: str
    tightened_core_floor_exceeds_one_million: bool
    theta_power_counterfactual_floor: str
    theta_power_counterfactual_floor_exceeds_4000: bool
    pap_outer_losses_removed_in_floor: bool
    current_sharp_density_certificate_closes_endpoint_gate: bool
    actual_endpoint_error_lower_proved: bool
    structural_reproof_or_new_density_still_possible: bool
    centered_endpoint_gate_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_or_zero_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> SharpDensityFixedFDiagnostic:
    decay = favorable_decay_exponent_upper()
    tight_floor = tightened_coefficient_floor()
    theta_floor = theta_power_counterfactual_floor()
    return SharpDensityFixedFDiagnostic(
        theory71_source_hash_verified=True,
        theory73_source_hash_verified=True,
        fixed_family_parameters="Q=f,T=f^5,D=f^7",
        detector_window="1/21",
        detector_kappa_at_one_over_21=str(detector_kappa()),
        positive_decay_requires_d_f_above_22=True,
        current_d_f_upper="416",
        explicit_zero_free_constant=str(MCCURLEY_C),
        favorable_decay_exponent_upper=str(decay),
        favorable_decay_exponent_below_9=(decay < 9),
        tightened_density_coefficient=str(TIGHT_DENSITY_COEFFICIENT),
        tightened_core_floor=str(tight_floor),
        tightened_core_floor_exceeds_one_million=(tight_floor > 1_000_000),
        theta_power_counterfactual_floor=str(theta_floor),
        theta_power_counterfactual_floor_exceeds_4000=(theta_floor > 4_000),
        pap_outer_losses_removed_in_floor=True,
        current_sharp_density_certificate_closes_endpoint_gate=False,
        actual_endpoint_error_lower_proved=False,
        structural_reproof_or_new_density_still_possible=True,
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
    if document.get("gate") != "DEP-R09 sharp near-one density fixed-f audit":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "CURRENT_THETA_MINUS_SIX_DENSITY_PACKAGE_FAILS_ENDPOINT_GATE_"
        "EVEN_AFTER_PAP_OUTER_LOSSES_REMOVED"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Change the theta^-6 detector architecture, preserve pre-sup cancellation, "
        "or identify a new sharp fixed-modulus density theorem; ordinary PAP-loss "
        "removal within the current Theory-71 package is insufficient."
    ):
        issues.append("next_gate mismatch")
    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 4:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"THEORY71", "THEORY73", "THEORY99", "TZ_PNT"}
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
    "MCCURLEY_C",
    "TIGHT_DENSITY_COEFFICIENT",
    "build_diagnostic",
    "detector_kappa",
    "favorable_decay_exponent_upper",
    "load_ledger",
    "theta_power_counterfactual_floor",
    "tightened_coefficient_floor",
    "validate_ledger",
]
