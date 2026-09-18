"""Exact diagnostics for the Vaughan 2001 variance source audit.

The paper studies moments, over a dyadic interval of moduli, of the
difference between a residue-class variance and its natural main term.  This
module records only the finite algebra needed to compare Vaughan's variance
with the Theory-82 nonprincipal character energy and the elementary power
range comparison.  It does not evaluate primes, infer hidden big-O constants,
or construct an ``X_cert`` threshold.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping

import mpmath as mp


REPO_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = REPO_ROOT / "article" / "vaughan2001.pdf"
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Vaughan2001_variance_source_audit_v1.json"
)

VAUGHAN2001_SHA256 = (
    "d5bc8d92c1204b09233c507b83ee185e35a54186122da1c906df87bbcb9d3ecc"
)
VAUGHAN2001_BYTE_SIZE = 180_481
VAUGHAN2001_PDF_PAGES = 21
D_MIN = 21
D_MAX = 186


def _integer(value: object, name: str, *, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _fraction(value: int | Fraction, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def centering_decomposition(
    residue_prime_sums: Iterable[int | Fraction],
    target_total: int | Fraction,
) -> dict[str, Fraction | int]:
    """Return the exact finite variance decomposition.

    If ``a_i`` are the reduced-residue prime sums, ``S=sum a_i``, ``n`` is
    their number, and ``Y`` is the desired total, then

      sum (a_i-Y/n)^2 = sum (a_i-S/n)^2 + (S-Y)^2/n.

    Multiplying the mean-centred term by ``n`` gives the nonprincipal Fourier
    energy by finite character Parseval.  Parseval itself remains a source
    theorem in the project documentation; this function checks the centering
    algebra exactly with rational arithmetic.
    """

    values = tuple(
        _fraction(value, f"residue_prime_sums[{index}]")
        for index, value in enumerate(residue_prime_sums)
    )
    if not values:
        raise ValueError("residue_prime_sums must be nonempty")
    target = _fraction(target_total, "target_total")
    count = len(values)
    total = sum(values, Fraction(0))
    mean = total / count
    target_mean = target / count
    vaughan_variance = sum(
        ((value - target_mean) ** 2 for value in values), Fraction(0)
    )
    mean_centered_variance = sum(
        ((value - mean) ** 2 for value in values), Fraction(0)
    )
    principal_error_term = (total - target) ** 2 / count
    character_energy = count * mean_centered_variance
    scaled_vaughan_variance = count * vaughan_variance
    return {
        "count": count,
        "total": total,
        "target_total": target,
        "vaughan_variance": vaughan_variance,
        "mean_centered_variance": mean_centered_variance,
        "principal_error_term": principal_error_term,
        "character_energy": character_energy,
        "scaled_vaughan_variance": scaled_vaughan_variance,
    }


def centering_identity_is_exact(
    residue_prime_sums: Iterable[int | Fraction],
    target_total: int | Fraction,
) -> bool:
    result = centering_decomposition(residue_prime_sums, target_total)
    return (
        result["vaughan_variance"]
        == result["mean_centered_variance"]
        + result["principal_error_term"]
        and result["character_energy"]
        + (result["total"] - result["target_total"]) ** 2
        == result["scaled_vaughan_variance"]
        and result["character_energy"] <= result["scaled_vaughan_variance"]
    )


def current_power_exponent(d: int) -> Fraction:
    """Return the exponent delta in q=Y^delta for Y=q^d."""

    d = _integer(d, "d", minimum=1)
    return Fraction(1, d)


def theorem2_exponent_gap(
    d: int,
    epsilon: int | Fraction = Fraction(0),
) -> Fraction:
    """Return ``3/4 + epsilon - 1/d`` exactly."""

    epsilon_value = _fraction(epsilon, "epsilon")
    if epsilon_value < 0:
        raise ValueError("epsilon must be nonnegative")
    return Fraction(3, 4) + epsilon_value - current_power_exponent(d)


def theorem1_required_a(q: int, d: int) -> mp.mpf:
    """Return the minimum A for the current point to meet Q>=Y/log(Y)^A.

    With ``Y=q^d`` and ``Q=q``, the source range is equivalent to
    ``A >= (d-1) log(q) / log(d log(q))``.  This diagnostic evaluates that
    expression only; it does not turn the paper's implicit constants into a
    finite cutoff.
    """

    q = _integer(q, "q", minimum=3)
    d = _integer(d, "d", minimum=2)
    with mp.workdps(max(mp.mp.dps, 80)):
        log_q = mp.log(q)
        return +((d - 1) * log_q / mp.log(d * log_q))


def theorem1_log_range_margin(q: int, d: int, a: int | Fraction) -> mp.mpf:
    """Return log(Q)-log(Y/log(Y)^A) for Q=q and Y=q^d."""

    q = _integer(q, "q", minimum=3)
    d = _integer(d, "d", minimum=2)
    a_value = _fraction(a, "a")
    if a_value < 0:
        raise ValueError("a must be nonnegative")
    with mp.workdps(max(mp.mp.dps, 80)):
        log_q = mp.log(q)
        return +(mp.mpf(a_value.numerator) / a_value.denominator * mp.log(d * log_q)
                 - (d - 1) * log_q)


@dataclass(frozen=True)
class Vaughan2001VarianceDiagnostic:
    vaughan_2001_pdf_identity_verified: bool
    vaughan_2001_pdf_page_count_verified: bool
    exact_centering_decomposition_samples_all_pass: bool
    exact_character_energy_upper_bridge_samples_all_pass: bool
    current_power_exponents_all_below_three_quarters: bool
    theorem1_is_dyadic_modulus_moment: bool
    theorem1_fixed_a_covers_growing_current_family: bool
    theorem2_requires_grh: bool
    theorem2_range_overlaps_current_power_regime: bool
    theorem3_is_fixed_primorial_character_energy_upper: bool
    fully_numerical_unconditional_current_regime_drop_in_identified: bool
    prime_specific_fixed_primorial_bound_identified: bool
    direct_same_law_correlation_theorem_identified: bool
    actual_character_energy_lower_bound_claimed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> Vaughan2001VarianceDiagnostic:
    samples = (
        ((1, 4, 7), 9),
        ((Fraction(1, 2), Fraction(5, 2)), 4),
        ((0, 0, 0, 0), 3),
    )
    centering_pass = all(
        centering_identity_is_exact(values, target)
        for values, target in samples
    )
    upper_bridge_pass = all(
        centering_decomposition(values, target)["character_energy"]
        <= centering_decomposition(values, target)["scaled_vaughan_variance"]
        for values, target in samples
    )
    exponent_pass = all(
        theorem2_exponent_gap(d) > 0 for d in (D_MIN, D_MAX)
    )
    return Vaughan2001VarianceDiagnostic(
        vaughan_2001_pdf_identity_verified=True,
        vaughan_2001_pdf_page_count_verified=True,
        exact_centering_decomposition_samples_all_pass=centering_pass,
        exact_character_energy_upper_bridge_samples_all_pass=upper_bridge_pass,
        current_power_exponents_all_below_three_quarters=exponent_pass,
        theorem1_is_dyadic_modulus_moment=True,
        theorem1_fixed_a_covers_growing_current_family=False,
        theorem2_requires_grh=True,
        theorem2_range_overlaps_current_power_regime=False,
        theorem3_is_fixed_primorial_character_energy_upper=False,
        fully_numerical_unconditional_current_regime_drop_in_identified=False,
        prime_specific_fixed_primorial_bound_identified=False,
        direct_same_law_correlation_theorem_identified=False,
        actual_character_energy_lower_bound_claimed=False,
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
    check_hash: bool = True,
) -> list[str]:
    """Validate source pinning and all fail-closed status fields."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != "DEP-R09 Vaughan 2001 variance source audit":
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "EXACT_VARIANCE_TO_CHARACTER_ENERGY_BRIDGE_"
        "BUT_SOURCE_RANGE_AND_NUMERICAL_CONSTANTS_NOT_A_CURRENT_DROP_IN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Obtain a fully numerical unconditional prime-specific upper for the "
        "prescribed growing primorial, or control the actual same-law weighted "
        "correlation directly; Vaughan 2001 supplies neither in the current "
        "q=Y^(1/d), 21<=d<=186 regime."
    ):
        issues.append("next_gate mismatch")

    source = document.get("local_primary_source")
    if not isinstance(source, dict):
        issues.append("local_primary_source mismatch")
        return issues
    if source.get("locator") != "article/vaughan2001.pdf":
        issues.append("source locator mismatch")
    if source.get("sha256") != VAUGHAN2001_SHA256:
        issues.append("source hash pin mismatch")
    if source.get("byte_size") != VAUGHAN2001_BYTE_SIZE:
        issues.append("source byte-size pin mismatch")
    if source.get("pdf_pages") != VAUGHAN2001_PDF_PAGES:
        issues.append("source page-count pin mismatch")

    if check_hash:
        if not PDF_PATH.is_file():
            issues.append("local primary source missing")
        else:
            if hashlib.sha256(PDF_PATH.read_bytes()).hexdigest() != VAUGHAN2001_SHA256:
                issues.append("local primary source hash mismatch")
            if PDF_PATH.stat().st_size != VAUGHAN2001_BYTE_SIZE:
                issues.append("local primary source byte-size mismatch")
    return issues


__all__ = [
    "D_MAX",
    "D_MIN",
    "LEDGER_PATH",
    "PDF_PATH",
    "VAUGHAN2001_BYTE_SIZE",
    "VAUGHAN2001_PDF_PAGES",
    "VAUGHAN2001_SHA256",
    "build_diagnostic",
    "centering_decomposition",
    "centering_identity_is_exact",
    "current_power_exponent",
    "load_ledger",
    "theorem1_log_range_margin",
    "theorem1_required_a",
    "theorem2_exponent_gap",
    "validate_ledger",
]
