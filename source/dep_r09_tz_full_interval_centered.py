"""Exact checks for the DEP-R09 Thorner--Zaman full-interval centered transfer."""

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
    / "Sono_FMT_DEPR09_TZ_full_interval_centered_v1.json"
)


def _fraction(value: object, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    return value


def relative_zero_free_constant(
    c_zfr: Fraction = Fraction(1, 24),
    log_f_over_x_lower: Fraction = Fraction(47, 100),
    log_primorial_over_x_upper: Fraction = Fraction(21, 20),
) -> Fraction:
    """Transfer c_zfr/log(P(X)) to c2/log(f)."""

    c_value = _fraction(c_zfr, "c_zfr")
    lower = _fraction(log_f_over_x_lower, "log_f_over_x_lower")
    upper = _fraction(
        log_primorial_over_x_upper, "log_primorial_over_x_upper"
    )
    if c_value <= 0 or lower <= 0 or upper <= 0:
        raise ValueError("zero-free transfer inputs must be positive")
    return c_value * lower / upper


def full_interval_range_holds(d_f_min: int = 21, source_exponent: int = 12) -> bool:
    if (
        isinstance(d_f_min, bool)
        or not isinstance(d_f_min, int)
        or isinstance(source_exponent, bool)
        or not isinstance(source_exponent, int)
        or d_f_min < 1
        or source_exponent < 1
    ):
        raise ValueError("range exponents must be positive integers")
    return d_f_min >= source_exponent


def centered_error_vector(
    pointwise_errors: Sequence[Fraction],
) -> tuple[Fraction, ...]:
    values = tuple(pointwise_errors)
    if not values:
        raise ValueError("pointwise_errors must be nonempty")
    for index, value in enumerate(values):
        _fraction(value, f"pointwise_error[{index}]")
    mean = sum(values, Fraction(0)) / len(values)
    return tuple(value - mean for value in values)


def centered_linf_envelope(
    pointwise_errors: Sequence[Fraction],
) -> dict[str, Fraction]:
    """Check max|e_a-average(e)| <= 2 max|e_a| exactly."""

    values = tuple(pointwise_errors)
    centered = centered_error_vector(values)
    raw_linf = max(abs(value) for value in values)
    centered_linf = max(abs(value) for value in centered)
    envelope = 2 * raw_linf
    if centered_linf > envelope:
        raise AssertionError("centered L-infinity envelope failed")
    return {
        "raw_linf": raw_linf,
        "centered_linf": centered_linf,
        "envelope": envelope,
    }


def exceptional_main_centering(
    character_values: Sequence[int],
    amplitude: Fraction,
) -> tuple[Fraction, ...]:
    """Center the secondary main -chi(a)*amplitude for a mean-zero character."""

    values = tuple(character_values)
    size = _fraction(amplitude, "amplitude")
    if not values:
        raise ValueError("character_values must be nonempty")
    if size < 0:
        raise ValueError("amplitude must be nonnegative")
    if any(value not in (-1, 1) for value in values):
        raise ValueError("fixture expects real reduced character values +/-1")
    if sum(values) != 0:
        raise ValueError("nonprincipal character fixture must have mean zero")
    main_errors = tuple(-Fraction(value) * size for value in values)
    centered = centered_error_vector(main_errors)
    if centered != main_errors:
        raise AssertionError("exceptional character pattern should survive centering")
    return centered


def endpoint_kappa_upper(
    source_relative_error: Fraction,
    lower_endpoint_correction: Fraction,
) -> Fraction:
    source_error = _fraction(source_relative_error, "source_relative_error")
    correction = _fraction(
        lower_endpoint_correction, "lower_endpoint_correction"
    )
    if source_error < 0 or correction < 0:
        raise ValueError("endpoint inputs must be nonnegative")
    return Fraction(21, 5) * (2 * source_error + correction)


def project_delta_upper(
    source_relative_error: Fraction,
    lower_endpoint_correction: Fraction,
    b_over_a: Fraction,
) -> Fraction:
    ratio = _fraction(b_over_a, "b_over_a")
    if ratio < 0:
        raise ValueError("b_over_a must be nonnegative")
    return endpoint_kappa_upper(
        source_relative_error, lower_endpoint_correction
    ) * (2 + ratio)


@dataclass(frozen=True)
class TZFullIntervalDiagnostic:
    source_tex_archive_verified: bool
    full_interval_is_separate_printed_corollary: bool
    proof_of_theorem_23_handles_h_equal_x: bool
    full_interval_range_d_f_21_covers_exponent_12: bool
    relative_zero_free_constant: str
    actual_b0_removes_near_one_exception_structurally: bool
    tz_remark_13_lambda_one_branch_applicable: bool
    centered_linf_factor: str
    exceptional_pattern_survives_centering_without_b0: bool
    exceptional_pattern_fixture_max: str
    source_error_fixture: str
    endpoint_kappa_fixture: str
    project_delta_fixture: str
    tz_numerical_implied_multiplier_printed: bool
    tz_numerical_decay_constant_printed: bool
    tz_common_finite_cutoff_printed: bool
    centered_endpoint_gate_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> TZFullIntervalDiagnostic:
    raw_errors = (
        Fraction(1, 100),
        Fraction(-1, 100),
        Fraction(-1, 100),
        Fraction(-1, 100),
    )
    centered = centered_linf_envelope(raw_errors)
    exceptional = exceptional_main_centering(
        (1, -1, 1, -1), Fraction(3, 100)
    )
    source_error = Fraction(1, 1000)
    correction = Fraction(1, 100000)
    return TZFullIntervalDiagnostic(
        source_tex_archive_verified=True,
        full_interval_is_separate_printed_corollary=True,
        proof_of_theorem_23_handles_h_equal_x=False,
        full_interval_range_d_f_21_covers_exponent_12=(
            full_interval_range_holds()
        ),
        relative_zero_free_constant=str(relative_zero_free_constant()),
        actual_b0_removes_near_one_exception_structurally=True,
        tz_remark_13_lambda_one_branch_applicable=True,
        centered_linf_factor="2",
        exceptional_pattern_survives_centering_without_b0=True,
        exceptional_pattern_fixture_max=str(max(abs(value) for value in exceptional)),
        source_error_fixture=str(source_error),
        endpoint_kappa_fixture=str(endpoint_kappa_upper(source_error, correction)),
        project_delta_fixture=str(
            project_delta_upper(source_error, correction, Fraction(1, 100))
        ),
        tz_numerical_implied_multiplier_printed=False,
        tz_numerical_decay_constant_printed=False,
        tz_common_finite_cutoff_printed=False,
        centered_endpoint_gate_closed=False,
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
        "DEP-R09 Thorner--Zaman full-interval centered endpoint transfer"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "B0_RELATIVE_ZERO_FREE_AND_CENTERED_TRANSFER_EXACT_BUT_"
        "TZ_NUMERICAL_MULTIPLIER_DECAY_AND_CUTOFF_OPEN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Recover a fully numerical K_TZ, c_TZ, and common cutoff for the "
        "nonexceptional full-interval PNT error R_TZ(U,f), then test the "
        "Theory-97 centered endpoint budget without running actual primes."
    ):
        issues.append("next_gate mismatch")
    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 7:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "THEORY57",
        "THEORY90",
        "THEORY97",
        "TZ_PDF",
        "TZ_SOURCE",
        "SONO2025",
        "FMT2018",
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
    "centered_error_vector",
    "centered_linf_envelope",
    "endpoint_kappa_upper",
    "exceptional_main_centering",
    "full_interval_range_holds",
    "load_ledger",
    "project_delta_upper",
    "relative_zero_free_constant",
    "validate_ledger",
]
