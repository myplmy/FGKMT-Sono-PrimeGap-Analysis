"""Exact finite diagnostics for the DEP-R09 pre-sup joint-angle gate."""

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
    / "Sono_FMT_DEPR09_presup_joint_angle_v1.json"
)


def _fraction_vector(values: Sequence[Fraction], name: str) -> tuple[Fraction, ...]:
    result = tuple(values)
    if not result:
        raise ValueError(f"{name} must be nonempty")
    for index, value in enumerate(result):
        if not isinstance(value, Fraction):
            raise TypeError(f"{name}[{index}] must be fractions.Fraction")
    return result


def weighted_correlation(
    coefficients: Sequence[Fraction],
    packets: Sequence[Fraction],
) -> Fraction:
    left = _fraction_vector(coefficients, "coefficients")
    right = _fraction_vector(packets, "packets")
    if len(left) != len(right):
        raise ValueError("vectors must have equal length")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def phase_blind_triangle_envelope(
    coefficients: Sequence[Fraction],
    magnitudes: Sequence[Fraction],
) -> Fraction:
    left = _fraction_vector(coefficients, "coefficients")
    bounds = _fraction_vector(magnitudes, "magnitudes")
    if len(left) != len(bounds):
        raise ValueError("vectors must have equal length")
    if any(value < 0 for value in bounds):
        raise ValueError("magnitudes must be nonnegative")
    return sum((abs(a) * m for a, m in zip(left, bounds)), Fraction(0))


def aligned_packets(
    coefficients: Sequence[Fraction],
    magnitudes: Sequence[Fraction],
) -> tuple[Fraction, ...]:
    left = _fraction_vector(coefficients, "coefficients")
    bounds = _fraction_vector(magnitudes, "magnitudes")
    if len(left) != len(bounds):
        raise ValueError("vectors must have equal length")
    if any(value < 0 for value in bounds):
        raise ValueError("magnitudes must be nonnegative")
    return tuple(
        Fraction(0) if coefficient == 0 else magnitude * (1 if coefficient > 0 else -1)
        for coefficient, magnitude in zip(left, bounds)
    )


def phase_blind_alignment_witness(
    coefficients: Sequence[Fraction],
    magnitudes: Sequence[Fraction],
) -> dict[str, object]:
    packets = aligned_packets(coefficients, magnitudes)
    correlation = weighted_correlation(coefficients, packets)
    envelope = phase_blind_triangle_envelope(coefficients, magnitudes)
    if correlation != envelope:
        raise AssertionError("phase-blind alignment witness failed")
    return {
        "packets": tuple(str(value) for value in packets),
        "correlation": correlation,
        "envelope": envelope,
    }


def squared_angle(
    coefficients: Sequence[Fraction],
    packets: Sequence[Fraction],
) -> Fraction:
    left = _fraction_vector(coefficients, "coefficients")
    right = _fraction_vector(packets, "packets")
    if len(left) != len(right):
        raise ValueError("vectors must have equal length")
    left_energy = sum((value * value for value in left), Fraction(0))
    right_energy = sum((value * value for value in right), Fraction(0))
    if left_energy == 0 or right_energy == 0:
        raise ValueError("angle requires two nonzero vectors")
    correlation = weighted_correlation(left, right)
    return correlation * correlation / (left_energy * right_energy)


def required_squared_angle_budget(
    delta: Fraction,
    selected_count: int,
    phi: int,
) -> Fraction:
    if not isinstance(delta, Fraction) or delta < 0:
        raise ValueError("delta must be a nonnegative Fraction")
    if (
        isinstance(selected_count, bool)
        or not isinstance(selected_count, int)
        or isinstance(phi, bool)
        or not isinstance(phi, int)
        or not 0 < selected_count < phi
    ):
        raise ValueError("require integers 0<selected_count<phi")
    return delta * delta * selected_count / (phi - selected_count)


@dataclass(frozen=True)
class PresupJointAngleDiagnostic:
    ramare_weighted_pdf_verified: bool
    ramare_regularity_pdf_verified: bool
    motohashi_pdf_verified: bool
    zheng_pdf_verified: bool
    szabo_pdf_verified: bool
    aligned_phase_triangle_is_exact: bool
    aligned_correlation_fixture: str
    cancellation_fixture_same_magnitudes: bool
    aligned_squared_angle: str
    required_squared_angle_fixture: str
    support_only_source_controls_joint_angle: bool
    ramare_weighted_sieve_is_direct_joint_character_theorem: bool
    ramare_regularity_is_multiplicative_character_theorem: bool
    motohashi_is_prescribed_f_weighted_product_theorem: bool
    zheng_is_prescribed_primorial_theorem: bool
    szabo_covers_all_character_orders_numerically: bool
    applicable_numerical_joint_angle_source_identified: bool
    pre_sup_joint_correlation_closed: bool
    centered_endpoint_gate_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_or_zero_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> PresupJointAngleDiagnostic:
    aligned = phase_blind_alignment_witness(
        (Fraction(2), Fraction(-3)),
        (Fraction(5), Fraction(7)),
    )
    aligned_angle = squared_angle(
        (Fraction(2), Fraction(-3)),
        (Fraction(10), Fraction(-15)),
    )
    cancelling = weighted_correlation(
        (Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(-1)),
    )
    return PresupJointAngleDiagnostic(
        ramare_weighted_pdf_verified=True,
        ramare_regularity_pdf_verified=True,
        motohashi_pdf_verified=True,
        zheng_pdf_verified=True,
        szabo_pdf_verified=True,
        aligned_phase_triangle_is_exact=(
            aligned["correlation"] == aligned["envelope"]
        ),
        aligned_correlation_fixture=str(aligned["correlation"]),
        cancellation_fixture_same_magnitudes=(cancelling == 0),
        aligned_squared_angle=str(aligned_angle),
        required_squared_angle_fixture=str(
            required_squared_angle_budget(Fraction(1, 100), 3, 30)
        ),
        support_only_source_controls_joint_angle=False,
        ramare_weighted_sieve_is_direct_joint_character_theorem=False,
        ramare_regularity_is_multiplicative_character_theorem=False,
        motohashi_is_prescribed_f_weighted_product_theorem=False,
        zheng_is_prescribed_primorial_theorem=False,
        szabo_covers_all_character_orders_numerically=False,
        applicable_numerical_joint_angle_source_identified=False,
        pre_sup_joint_correlation_closed=False,
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
    if document.get("gate") != "DEP-R09 pre-sup joint-angle source audit":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "PHASE_BLIND_SOURCES_CANNOT_CONTROL_JOINT_ANGLE_AND_NO_NUMERICAL_"
        "PRESCRIBED_F_DROP_IN_IDENTIFIED"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Audit the fixed-modulus explicit formula before characterwise absolute "
        "values for a direct signed zero-packet theorem, or prove a new joint "
        "angle/covariance lemma; support-only and separate-norm inputs are insufficient."
    ):
        issues.append("next_gate mismatch")
    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 8:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "THEORY75",
        "THEORY77",
        "THEORY95",
        "RAMARE_WEIGHTED",
        "RAMARE_REGULAR",
        "MOTOHASHI",
        "ZHENG",
        "SZABO",
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
    "aligned_packets",
    "build_diagnostic",
    "load_ledger",
    "phase_blind_alignment_witness",
    "phase_blind_triangle_envelope",
    "required_squared_angle_budget",
    "squared_angle",
    "validate_ledger",
    "weighted_correlation",
]
