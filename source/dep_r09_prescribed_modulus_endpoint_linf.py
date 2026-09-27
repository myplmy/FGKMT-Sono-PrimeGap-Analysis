"""Exact checks for the DEP-R09 prescribed-modulus endpoint L-infinity transfer."""

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
    / "Sono_FMT_DEPR09_prescribed_modulus_endpoint_linf_v1.json"
)


def _fraction(value: object, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    return value


def centered_residue_masses(
    masses: Sequence[Fraction],
) -> tuple[Fraction, ...]:
    """Center a nonnegative finite residue-mass vector by its exact mean."""

    values = tuple(masses)
    if not values:
        raise ValueError("masses must be nonempty")
    for index, value in enumerate(values):
        _fraction(value, f"mass[{index}]")
        if value < 0:
            raise ValueError("masses must be nonnegative")
    mean = sum(values, Fraction(0)) / len(values)
    return tuple(value - mean for value in values)


def centered_l1_envelope(masses: Sequence[Fraction]) -> dict[str, Fraction]:
    """Return the exact L1 norm and the universal twice-total envelope."""

    values = tuple(masses)
    centered = centered_residue_masses(values)
    total = sum(values, Fraction(0))
    l1_norm = sum((abs(value) for value in centered), Fraction(0))
    envelope = 2 * total
    if l1_norm > envelope:
        raise AssertionError("centered L1 envelope failed")
    return {"total": total, "l1_norm": l1_norm, "envelope": envelope}


def linf_cross_envelope(
    small_masses: Sequence[Fraction],
    interval_errors: Sequence[Fraction],
) -> dict[str, Fraction]:
    """Check phi*<centered small mass, interval error> by L1 times L-infinity."""

    masses = tuple(small_masses)
    errors = tuple(interval_errors)
    if not masses or len(masses) != len(errors):
        raise ValueError("mass and error vectors need equal nonzero length")
    for index, value in enumerate(errors):
        _fraction(value, f"interval_error[{index}]")
    if sum(errors, Fraction(0)) != 0:
        raise ValueError("interval error vector must be centered")
    centered = centered_residue_masses(masses)
    phi = len(masses)
    theta_mass = sum(masses, Fraction(0))
    cross = phi * sum(
        (left * right for left, right in zip(centered, errors)),
        Fraction(0),
    )
    max_error = max(abs(value) for value in errors)
    envelope = 2 * phi * theta_mass * max_error
    if abs(cross) > envelope:
        raise AssertionError("L1-Linfinity cross envelope failed")
    return {
        "cross": cross,
        "absolute_cross": abs(cross),
        "theta_mass": theta_mass,
        "max_interval_error": max_error,
        "envelope": envelope,
    }


def endpoint_interval_epsilon(
    endpoint_epsilon: Fraction,
    lower_endpoint_correction: Fraction,
) -> Fraction:
    endpoint = _fraction(endpoint_epsilon, "endpoint_epsilon")
    correction = _fraction(
        lower_endpoint_correction, "lower_endpoint_correction"
    )
    if endpoint < 0 or correction < 0:
        raise ValueError("endpoint inputs must be nonnegative")
    return endpoint + correction


def prime_count_half_lower(
    y_over_log_y: Fraction,
    pi_x_upper: Fraction,
) -> Fraction:
    """Deduce N>=Y/(2 log Y) after source bounds are supplied."""

    y_scale = _fraction(y_over_log_y, "y_over_log_y")
    x_upper = _fraction(pi_x_upper, "pi_x_upper")
    if y_scale <= 0 or x_upper < 0:
        raise ValueError("prime-count inputs have the wrong sign")
    if x_upper > y_scale / 2:
        raise ValueError("pi(X) upper does not fit the half-scale budget")
    lower = y_scale - x_upper
    if lower < y_scale / 2:
        raise AssertionError("half-scale count lower failed")
    return lower


def small_scale_mass_ratio_upper(
    theta_coefficient: Fraction = Fraction(21, 20),
    count_fraction: Fraction = Fraction(1, 2),
) -> Fraction:
    """Return C_theta/c_N in theta(t)<=C_theta*t and N>=c_N*Y/logY."""

    theta = _fraction(theta_coefficient, "theta_coefficient")
    count = _fraction(count_fraction, "count_fraction")
    if theta < 0 or count <= 0:
        raise ValueError("normalization coefficients have the wrong sign")
    return theta / count


def endpoint_linf_kappa(
    endpoint_epsilon: Fraction,
    lower_endpoint_correction: Fraction,
) -> Fraction:
    """Return 2*(21/10)*(epsilon_U+epsilon_0)."""

    epsilon = endpoint_interval_epsilon(
        endpoint_epsilon, lower_endpoint_correction
    )
    return 2 * small_scale_mass_ratio_upper() * epsilon


def project_delta_upper(
    endpoint_epsilon: Fraction,
    lower_endpoint_correction: Fraction,
    b_over_a: Fraction,
) -> Fraction:
    ratio = _fraction(b_over_a, "b_over_a")
    if ratio < 0:
        raise ValueError("b_over_a must be nonnegative")
    return endpoint_linf_kappa(
        endpoint_epsilon, lower_endpoint_correction
    ) * (2 + ratio)


def source_range_exponent_diagnostic(d_min: int = 21) -> dict[str, object]:
    if isinstance(d_min, bool) or not isinstance(d_min, int) or d_min < 1:
        raise ValueError("d_min must be a positive integer")
    current = Fraction(1, d_min)
    return {
        "d_min": d_min,
        "current_modulus_exponent": str(current),
        "below_square_root_exponent": current < Fraction(1, 2),
        "below_two_thirds_exponent": current < Fraction(2, 3),
    }


@dataclass(frozen=True)
class EndpointLinfDiagnostic:
    centered_l1_envelope_exact: bool
    linf_cross_envelope_exact: bool
    sample_cross: str
    sample_cross_envelope: str
    prime_count_half_lower_fixture: str
    small_scale_mass_ratio_upper: str
    endpoint_interval_epsilon_fixture: str
    endpoint_linf_kappa_fixture: str
    project_delta_fixture: str
    current_modulus_exponent: str
    vaughan_i_primary_pdf_verified: bool
    vaughan_ii_primary_pdf_verified: bool
    vaughan_i_is_prescribed_fixed_modulus_theorem: bool
    vaughan_ii_is_prescribed_fixed_modulus_theorem: bool
    harper_dyadic_range_contains_current_modulus: bool
    thorner_zaman_fully_numerical_centered_endpoint_bound: bool
    centered_endpoint_linf_gate_closed: bool
    cross_scale_covariance_gate_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> EndpointLinfDiagnostic:
    masses = (Fraction(2), Fraction(0), Fraction(3), Fraction(0))
    errors = (Fraction(1), Fraction(-2), Fraction(3), Fraction(-2))
    l1 = centered_l1_envelope(masses)
    cross = linf_cross_envelope(masses, errors)
    endpoint = Fraction(1, 1000)
    correction = Fraction(1, 100000)
    range_diagnostic = source_range_exponent_diagnostic()
    return EndpointLinfDiagnostic(
        centered_l1_envelope_exact=(l1["l1_norm"] <= l1["envelope"]),
        linf_cross_envelope_exact=(
            cross["absolute_cross"] <= cross["envelope"]
        ),
        sample_cross=str(cross["cross"]),
        sample_cross_envelope=str(cross["envelope"]),
        prime_count_half_lower_fixture=str(
            prime_count_half_lower(Fraction(16), Fraction(2))
        ),
        small_scale_mass_ratio_upper=str(small_scale_mass_ratio_upper()),
        endpoint_interval_epsilon_fixture=str(
            endpoint_interval_epsilon(endpoint, correction)
        ),
        endpoint_linf_kappa_fixture=str(
            endpoint_linf_kappa(endpoint, correction)
        ),
        project_delta_fixture=str(
            project_delta_upper(endpoint, correction, Fraction(1, 100))
        ),
        current_modulus_exponent=str(
            range_diagnostic["current_modulus_exponent"]
        ),
        vaughan_i_primary_pdf_verified=True,
        vaughan_ii_primary_pdf_verified=True,
        vaughan_i_is_prescribed_fixed_modulus_theorem=False,
        vaughan_ii_is_prescribed_fixed_modulus_theorem=False,
        harper_dyadic_range_contains_current_modulus=False,
        thorner_zaman_fully_numerical_centered_endpoint_bound=False,
        centered_endpoint_linf_gate_closed=False,
        cross_scale_covariance_gate_closed=False,
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
        "DEP-R09 prescribed-modulus centered endpoint L-infinity transfer"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "SINGLE_ENDPOINT_LINFINITY_SUFFICIENT_TRANSFER_EXACT_BUT_"
        "NUMERICAL_CENTERED_PNT_INPUT_OPEN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Prove a fully numerical centered fixed-modulus endpoint bound "
        "epsilon_infinity(U,f) small enough for the 21/5 endpoint transfer, "
        "including exceptional-modulus removal and one common cutoff."
    ):
        issues.append("next_gate mismatch")
    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 7:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "THEORY47",
        "THEORY96",
        "VAUGHAN1998I",
        "VAUGHAN1998II",
        "HARPER2024",
        "THORNER_ZAMAN",
        "ROSSER_SCHOENFELD",
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
    "build_diagnostic",
    "centered_l1_envelope",
    "centered_residue_masses",
    "endpoint_interval_epsilon",
    "endpoint_linf_kappa",
    "linf_cross_envelope",
    "load_ledger",
    "prime_count_half_lower",
    "project_delta_upper",
    "small_scale_mass_ratio_upper",
    "source_range_exponent_diagnostic",
    "validate_ledger",
]
