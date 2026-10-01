"""Exact finite checks for fixed-modulus, height-weighted density replay.

The supplied heights, log ratios and weights are abstract rational fixtures.
This module does not generate primes/zeros, evaluate X or a cutoff, optimize a
height, or promote an analytic source premise to an observed certificate.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Sequence


WINDOW = F(1, 21)
C_M = F(10**9, 9645908801)
C_B0 = F(47, 2520)
K_DENSITY = F(23, 7)
LEDGER = Path("docs/method/theory/data/Sono_FMT_DEPR09_height_weighted_density_v1.json")


def _fraction(value: F, name: str) -> F:
    if not isinstance(value, F):
        raise TypeError(f"{name} must be Fraction")
    return value


def fixed_detector_exponent(height_log_ratio: F) -> F:
    ratio = _fraction(height_log_ratio, "height_log_ratio")
    if ratio < 0:
        raise ValueError("require a nonnegative supplied height log ratio")
    return 2 * (1 + ratio) * (1 + 12 * WINDOW)


def validate_half_rankin_ratio(log_q_over_log_d: F) -> F:
    """Fail closed before reusing the old 7/4 Rankin envelope."""
    ratio = _fraction(log_q_over_log_d, "log_q_over_log_d")
    if not 0 <= ratio <= F(1, 2):
        raise ValueError("the 7/4 envelope requires log(q)/log(D)<=1/2")
    return F(7, 4)


def all_height_selected_coefficient() -> F:
    """Compose the source-tightened factors with the all-height Rankin cap 3."""
    return (
        F(10**6, 10**6 - 1)
        * (3 * F(2840, 1197))
        * F(8, 5)
        * F(15665428311, 1750000)
        / F(4, 147)**2
        / F(55, 18522)
    )


def finite_height_layer_cake(
    weights: Sequence[F], heights: Sequence[F], terminal: F
) -> dict[str, F]:
    """Integrate an abstract cumulative step function against t^-2 exactly."""
    terminal = _fraction(terminal, "terminal")
    values = tuple(_fraction(w, "weight") for w in weights)
    levels = tuple(_fraction(h, "height") for h in heights)
    if terminal < 1 or len(values) != len(levels):
        raise ValueError("require T>=1 and equal vector lengths")
    if any(w < 0 for w in values) or any(not 1 <= h <= terminal for h in levels):
        raise ValueError("require nonnegative weights and heights in [1,T]")
    endpoint = sum(values, F(0)) / terminal
    integral = sum((w * (1 / h - 1 / terminal)
                    for w, h in zip(values, levels)), F(0))
    weighted_sum = sum((w / h for w, h in zip(values, levels)), F(0))
    if weighted_sum != endpoint + integral:
        raise AssertionError("height layer-cake orientation or endpoint mismatch")
    return {"weighted_sum": weighted_sum, "endpoint": endpoint, "integral": integral}


def density_integration_factor(d: F, height_log_ratio: F, zero_free: F = C_M) -> F:
    """Return the rational scalar multiplying C*exp(-v*delta0), not the exp."""
    d = _fraction(d, "d")
    ratio = _fraction(height_log_ratio, "height_log_ratio")
    c = _fraction(zero_free, "zero_free")
    if not 21 <= d <= 416 or not 0 <= ratio <= F(3, 2) or not 0 < c <= F(1, 9):
        raise ValueError("require the audited d, height-ratio and c ranges")
    gap = d - K_DENSITY * (1 + ratio)
    if gap <= 0:
        raise ValueError("density integration requires a positive exponent gap")
    return 2 * d / gap * (5 + 2 * c + 2 * (1 + ratio) / gap)


def height_cost_gap(log_f: F, d: F, zero_free: F, log_height: F) -> F:
    """Exact rational identity for g(w)-g(0); supplied logs are not evaluated."""
    ell = _fraction(log_f, "log_f")
    d = _fraction(d, "d")
    c = _fraction(zero_free, "zero_free")
    w = _fraction(log_height, "log_height")
    if ell <= 0 or d < 0 or c < 0 or w < 0 or c * d > ell / 5:
        raise ValueError("require ell>0,w,c,d>=0 and c*d<=ell/5")
    result = w + c * d / (1 + w / ell) - c * d
    if result != w * (1 - c * d / (ell + w)):
        raise AssertionError("height cost identity failed")
    if result < F(4, 5) * w:
        raise AssertionError("height weighting lost its uniform decay")
    return result


def coarse_fixed_regime_budget() -> F:
    """A single fixed rational comparison, not a d or X search."""
    return F(63, 2) * (5 * 10**10) * F(10, 27)**34 + F(21, 20) * F(10, 27)**6


def audit_ledger(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or Path(__file__).resolve().parents[1]
    data = json.loads((root / LEDGER).read_text(encoding="utf-8"))
    for item in data["source_registry"]:
        actual = hashlib.sha256((root / item["locator"]).read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise ValueError(f"source hash mismatch: {item['key']}")
    constants = data["exact_rational_terminals"]
    expected = {
        "all_height_selected_coefficient": str(all_height_selected_coefficient()),
        "kappa_fixed_s_3_over_2": str(fixed_detector_exponent(F(3, 2))),
        "kappa_fixed_local_height_zero": str(fixed_detector_exponent(F(0))),
        "coarse_fixed_regime_budget": str(coarse_fixed_regime_budget()),
    }
    if any(constants[name] != value for name, value in expected.items()):
        raise ValueError("rational terminal mismatch")
    if not all_height_selected_coefficient() < 5 * 10**10:
        raise ValueError("all-height coefficient cap failed")
    if not coarse_fixed_regime_budget() < F(1, 100):
        raise ValueError("fixed rational budget failed")
    gates = data["actual_project_gates"]
    unresolved = (
        "uniform_native_d_ge_333_proved", "numeric_EF_multiplier_recovered",
        "same_law_all_character_correlation_closed", "pap_11_closed",
        "dep_r09_closed", "numerical_x_cert_ready", "bounded_x_cert_range_obtained",
        "threshold_calculator_ready", "actual_prime_or_zero_computation_run",
        "source_theorem_local_axiom_used", "proof_escape_used",
    )
    if any(gates[name] is not False for name in unresolved):
        raise ValueError("an unresolved project gate was promoted")
    return {
        "status": "FINITE_SOURCE_PIN_AND_RATIONAL_TERMINALS_PASS",
        "source_count": len(data["source_registry"]),
        **expected,
        **{name: gates[name] for name in unresolved},
    }


if __name__ == "__main__":
    print(json.dumps(audit_ledger(), sort_keys=True))
