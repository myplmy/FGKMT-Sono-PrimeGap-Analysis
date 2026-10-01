"""Finite factor partitions and rational terminals for the D=160 native regime.

No primes, zeros, X values or numerical cutoffs are generated. The supplied
factor labels and fractions are abstract proof fixtures, not source PNT data.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from math import prod
from pathlib import Path
from typing import Sequence


OUTER_D = F(160)
Q_LOWER = F(499, 500)
F_UPPER = F(12703, 25000)
F_LOWER = F(47, 100)
Q_UPPER = F(21, 20)
Q_UPPER_NATIVE = F(2001, 2000)
F_LOWER_NATIVE = F(993, 2000)
LEDGER = Path("docs/method/theory/data/Sono_FMT_DEPR09_native_primorial_baseline_v1.json")


def _labels(values: Sequence[int], name: str) -> frozenset[int]:
    labels = tuple(values)
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 2 for x in labels):
        raise ValueError(f"{name} requires distinct positive factor labels >=2")
    if len(set(labels)) != len(labels):
        raise ValueError(f"duplicate factor label in {name}")
    return frozenset(labels)


def factor_partition(
    all_labels: Sequence[int], lower_labels: Sequence[int],
    outer_labels: Sequence[int], exceptional: int,
) -> dict[str, object]:
    """Replay P(X)/B0=h*f using supplied labels, without testing primality."""
    all_set = _labels(all_labels, "all_labels")
    lower = _labels(lower_labels, "lower_labels")
    outer = _labels(outer_labels, "outer_labels")
    if (isinstance(exceptional, bool) or not isinstance(exceptional, int)
            or (exceptional != 1 and exceptional not in all_set)):
        raise ValueError("B0 must be 1 or a supplied factor of the full product")
    if not lower <= all_set or not outer <= lower - {exceptional}:
        raise ValueError("require lower<=all and S<=lower minus B0")
    inner = (all_set - lower) - {exceptional}
    fixed = (lower - {exceptional}) - outer
    q = prod(all_set - {exceptional})
    h = prod(outer) * prod(inner)
    f = prod(fixed)
    low_exception = exceptional if exceptional in lower else 1
    lower_product = prod(lower)
    if q != h*f or f*prod(outer)*low_exception != lower_product:
        raise AssertionError("raw-coordinate product partition failed")
    if lower_product % f:
        raise AssertionError("native product does not divide the lower product")
    return {
        "q": q, "h": h, "f": f, "lower_product": lower_product,
        "low_exception": low_exception,
        "inner_labels": tuple(sorted(inner)), "fixed_labels": tuple(sorted(fixed)),
    }


def require_raw_inner(
    supplied: Sequence[int], all_labels: Sequence[int],
    lower_labels: Sequence[int], exceptional: int,
) -> None:
    """Do not replace the fixed raw inner set with an outcome-good subset."""
    expected = factor_partition(all_labels, lower_labels, (), exceptional)["inner_labels"]
    if _labels(supplied, "supplied_inner") != frozenset(expected):
        raise ValueError("inner support must be the complete raw set minus B0")


def native_log_ratio_terminals() -> tuple[F, F]:
    return OUTER_D * Q_LOWER / F_UPPER, OUTER_D * Q_UPPER_NATIVE / F_LOWER_NATIVE


def baseline_nonvanishing_rational_budget() -> F:
    """One fixed analytic comparison; not an exponent or X search."""
    return F(63, 2) * (5 * 10**10) * F(10, 27)**32 + F(21, 20)*F(10, 27)**6


def full_primorial_real_decay_lower() -> F:
    """D*log(q)/(24*log(P(X))); this avoids a second lossy f-log ratio."""
    return OUTER_D * Q_LOWER / (24 * Q_UPPER_NATIVE)


def source_support_log_cap() -> F:
    # a>=1000: raw inner sum<=1003 X/2000; z<=X/512; theta(z)<21z/20.
    return F(1003, 2000) + F(21, 10240)


def vanishing_coefficient(supplied_k_ef: F) -> F:
    if not isinstance(supplied_k_ef, F) or supplied_k_ef < 0:
        raise ValueError("supplied K_EF must be a nonnegative Fraction fixture")
    return 699716 * supplied_k_ef + F(54927, 10)


def audit_ledger(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or Path(__file__).resolve().parents[1]
    data = json.loads((root / LEDGER).read_text(encoding="utf-8"))
    for item in data["source_registry"]:
        observed = hashlib.sha256((root / item["locator"]).read_bytes()).hexdigest()
        if observed != item["sha256"]:
            raise ValueError(f"source hash mismatch: {item['key']}")
    low, high = native_log_ratio_terminals()
    expected = {
        "native_lower": str(low), "native_upper": str(high),
        "nonvanishing_rational_budget": str(baseline_nonvanishing_rational_budget()),
        "support_log_cap": str(source_support_log_cap()),
        "vanishing_additive_coefficient": str(F(54927, 10)),
        "full_primorial_real_decay_lower": str(full_primorial_real_decay_lower()),
    }
    if any(data["rational_terminals"][key] != value for key, value in expected.items()):
        raise ValueError("rational terminal mismatch")
    if not low > 314 or not high < 323 or not baseline_nonvanishing_rational_budget() < F(1, 36):
        raise ValueError("baseline regime or budget comparison failed")
    gates = data["actual_project_gates"]
    open_names = (
        "numeric_EF_multiplier_recovered", "same_law_all_character_correlation_closed",
        "pap_11_closed", "dep_r09_closed", "numerical_x_cert_ready",
        "bounded_x_cert_range_obtained", "threshold_calculator_ready",
        "actual_prime_or_zero_computation_run", "source_theorem_local_axiom_used",
        "proof_escape_used", "outer_D_changed",
    )
    if any(gates[name] is not False for name in open_names):
        raise ValueError("an unresolved/unauthorized gate was promoted")
    if data["parameterized_vanishing"]["numeric_K_EF"] is not None:
        raise ValueError("the numerical EF constant must remain unresolved")
    return {
        "status": "FINITE_SOURCE_PIN_AND_BASELINE_TERMINALS_PASS",
        "source_count": len(data["source_registry"]),
        **expected,
        **{name: gates[name] for name in open_names},
    }


if __name__ == "__main__":
    print(json.dumps(audit_ledger(), sort_keys=True))
