"""Exact finite checks for the DEP-R09 cross-scale covariance interface."""

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
    / "Sono_FMT_DEPR09_cross_scale_covariance_v1.json"
)


def _fraction(value: object, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    return value


def discrete_abel_interval(
    jumps: Sequence[Fraction],
    weights: Sequence[Fraction],
    start: int,
    end: int,
) -> dict[str, Fraction]:
    """Verify finite Abel summation on the inclusive index interval [start,end].

    If B_i=sum_{j<=i} jumps_j, then
      sum_{i=start}^end jumps_i weights_i
      = B_end weights_end - B_(start-1) weights_start
        + sum_{i=start}^{end-1} B_i(weights_i-weights_(i+1)).
    """

    jumps = tuple(jumps)
    weights = tuple(weights)
    if not jumps or len(jumps) != len(weights):
        raise ValueError("jumps and weights need equal nonzero length")
    if (
        isinstance(start, bool)
        or isinstance(end, bool)
        or not isinstance(start, int)
        or not isinstance(end, int)
        or not 0 <= start <= end < len(jumps)
    ):
        raise ValueError("invalid Abel interval")
    for index, value in enumerate(jumps):
        _fraction(value, f"jump[{index}]")
    for index, value in enumerate(weights):
        _fraction(value, f"weight[{index}]")

    cumulative: list[Fraction] = []
    running = Fraction(0)
    for value in jumps:
        running += value
        cumulative.append(running)
    direct = sum(
        (jumps[index] * weights[index] for index in range(start, end + 1)),
        Fraction(0),
    )
    before = cumulative[start - 1] if start > 0 else Fraction(0)
    transformed = cumulative[end] * weights[end] - before * weights[start]
    transformed += sum(
        (
            cumulative[index] * (weights[index] - weights[index + 1])
            for index in range(start, end)
        ),
        Fraction(0),
    )
    if direct != transformed:
        raise AssertionError("finite Abel identity failed")
    return {"direct": direct, "transformed": transformed}


def residue_cross_covariance(
    small_errors: Sequence[Fraction],
    large_errors: Sequence[Fraction],
) -> Fraction:
    """Return phi*sum_a E_small(a)E_large(a), with phi=len(errors)."""

    small = tuple(small_errors)
    large = tuple(large_errors)
    if not small or len(small) != len(large):
        raise ValueError("error vectors need equal nonzero length")
    for index, value in enumerate(small):
        _fraction(value, f"small[{index}]")
    for index, value in enumerate(large):
        _fraction(value, f"large[{index}]")
    if sum(small, Fraction(0)) != 0 or sum(large, Fraction(0)) != 0:
        raise ValueError("residue error vectors must be centered")
    return len(small) * sum(
        (left * right for left, right in zip(small, large)), Fraction(0)
    )


def polarization_cross_covariance(
    small_errors: Sequence[Fraction],
    large_errors: Sequence[Fraction],
) -> dict[str, Fraction]:
    small = tuple(small_errors)
    large = tuple(large_errors)
    cross = residue_cross_covariance(small, large)
    phi = len(small)
    small_energy = phi * sum((value**2 for value in small), Fraction(0))
    large_energy = phi * sum((value**2 for value in large), Fraction(0))
    combined_energy = phi * sum(
        ((left + right) ** 2 for left, right in zip(small, large)),
        Fraction(0),
    )
    if combined_energy - small_energy - large_energy != 2 * cross:
        raise AssertionError("polarization identity failed")
    return {
        "cross": cross,
        "small_energy": small_energy,
        "large_energy": large_energy,
        "combined_energy": combined_energy,
    }


def _character_mod_five(index: int, residue: int) -> GaussianRational:
    if not 0 <= index < 4:
        raise ValueError("character index must lie in 0..3")
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


def character_cross_covariance_mod_five(
    small_errors: Sequence[Fraction],
    large_errors: Sequence[Fraction],
) -> GaussianRational:
    """Return sum_(chi!=chi0) Theta_conj(chi)*Z_chi modulo five."""

    small = tuple(small_errors)
    large = tuple(large_errors)
    if len(small) != 4 or len(large) != 4:
        raise ValueError("modulo-five fixture needs four reduced residues")
    if sum(small, Fraction(0)) != 0 or sum(large, Fraction(0)) != 0:
        raise ValueError("vectors must be centered")
    residues = (1, 2, 3, 4)
    total = GaussianRational(Fraction(0))
    for index in range(1, 4):
        theta_conjugate = GaussianRational(Fraction(0))
        z_value = GaussianRational(Fraction(0))
        for residue, small_value, large_value in zip(residues, small, large):
            theta_conjugate = theta_conjugate + (
                _character_mod_five(index, residue).conjugate() * small_value
            )
            z_value = z_value + (
                _character_mod_five(index, residue) * large_value
            )
        total = total + theta_conjugate * z_value
    return total


def abel_cross_transfer_factor(loglog_ratio: Fraction) -> Fraction:
    ratio = _fraction(loglog_ratio, "loglog_ratio")
    if ratio < 0:
        raise ValueError("loglog_ratio must be nonnegative")
    return 2 + ratio


def project_abel_transfer_upper(kappa: Fraction, b_over_a: Fraction) -> Fraction:
    kappa = _fraction(kappa, "kappa")
    ratio = _fraction(b_over_a, "b_over_a")
    if kappa < 0 or ratio < 0:
        raise ValueError("inputs must be nonnegative")
    return kappa * abel_cross_transfer_factor(ratio)


@dataclass(frozen=True)
class CrossScaleCovarianceDiagnostic:
    finite_abel_identity_exact: bool
    residue_character_cross_identity_exact: bool
    polarization_identity_exact: bool
    sample_residue_cross: str
    sample_character_cross_real: str
    sample_character_cross_imag: str
    project_transfer_factor_at_b_over_a_1_over_100: str
    vaughan2001_primary_pdf_verified: bool
    harper2024_primary_pdf_verified: bool
    vaughan_source_is_mixed_fixed_modulus_theorem: bool
    harper_source_is_prescribed_fixed_modulus_theorem: bool
    thorner_zaman_fully_numerical_current_cutoff: bool
    cross_scale_covariance_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> CrossScaleCovarianceDiagnostic:
    jumps = (Fraction(2), Fraction(-1), Fraction(3), Fraction(4))
    weights = (Fraction(1), Fraction(1, 2), Fraction(1, 3), Fraction(1, 4))
    abel = discrete_abel_interval(jumps, weights, 1, 3)
    small = (Fraction(2), Fraction(-1), Fraction(1), Fraction(-2))
    large = (Fraction(3), Fraction(0), Fraction(-1), Fraction(-2))
    residue_cross = residue_cross_covariance(small, large)
    character_cross = character_cross_covariance_mod_five(small, large)
    polarization = polarization_cross_covariance(small, large)
    return CrossScaleCovarianceDiagnostic(
        finite_abel_identity_exact=(abel["direct"] == abel["transformed"]),
        residue_character_cross_identity_exact=(
            character_cross == GaussianRational(residue_cross)
        ),
        polarization_identity_exact=(
            polarization["combined_energy"]
            - polarization["small_energy"]
            - polarization["large_energy"]
            == 2 * polarization["cross"]
        ),
        sample_residue_cross=str(residue_cross),
        sample_character_cross_real=str(character_cross.real),
        sample_character_cross_imag=str(character_cross.imag),
        project_transfer_factor_at_b_over_a_1_over_100=str(
            abel_cross_transfer_factor(Fraction(1, 100))
        ),
        vaughan2001_primary_pdf_verified=True,
        harper2024_primary_pdf_verified=True,
        vaughan_source_is_mixed_fixed_modulus_theorem=False,
        harper_source_is_prescribed_fixed_modulus_theorem=False,
        thorner_zaman_fully_numerical_current_cutoff=False,
        cross_scale_covariance_closed=False,
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
    if document.get("gate") != "DEP-R09 cross-scale covariance Abel interface":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "ABEL_AND_CROSS_COVARIANCE_INTERFACES_EXACT_BUT_NO_FULLY_NUMERICAL_"
        "PRESCRIBED_MODULUS_MIXED_MOMENT_SOURCE"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove a fully numerical uniform bound for the prescribed-modulus "
        "cross-scale covariance K_f(t;X,U), or equivalently for the variance "
        "of the associated combined signed prime sequence."
    ):
        issues.append("next_gate mismatch")
    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 5:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"THEORY95", "VAUGHAN2001", "THEORY85", "HARPER2024", "THEORY59"}
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
    "abel_cross_transfer_factor",
    "build_diagnostic",
    "character_cross_covariance_mod_five",
    "discrete_abel_interval",
    "load_ledger",
    "polarization_cross_covariance",
    "project_abel_transfer_upper",
    "residue_cross_covariance",
    "validate_ledger",
]
