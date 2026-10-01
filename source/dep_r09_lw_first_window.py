"""Exact scalar checks for Liu--Wang's first zero-window source.

Only supplied rational log parameters and abstract cumulative counts are
used. This is neither an actual zero computation nor an X/threshold search.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


LW_A = F(17, 50)
LW_LAMBDA = F(9, 20)
KAPPA_UPPER = F(277, 1000)
COUNT_CAP = 144
LEDGER = Path("docs/method/theory/data/Sono_FMT_DEPR09_LW_first_window_v1.json")


def scalar_parts(log_z: F, supplied_kappa: F) -> dict[str, F]:
    if not isinstance(log_z, F) or not isinstance(supplied_kappa, F):
        raise TypeError("log_z and kappa must be supplied Fraction fixtures")
    if log_z < 30000 or not 0 <= supplied_kappa <= KAPPA_UPPER:
        raise ValueError("require log_z>=30000 and 0<=kappa<=277/1000")
    aa = 1/LW_A-F(8973, 10000)/log_z
    bb = supplied_kappa+F(7647, 10000)/log_z
    cc = 1/(LW_A+LW_LAMBDA)-supplied_kappa-F(755, 10000)/log_z
    numerator = aa**2-aa*bb
    denominator = cc**2-aa*bb
    if not denominator > F(1, 8) or cc < F(247, 250):
        raise AssertionError("source denominator conditions (3.18) failed")
    ratio = numerator/denominator
    if numerator > 9 or ratio > 72:
        raise AssertionError("safe ratio envelope failed")
    floor_ratio = ratio.numerator//ratio.denominator
    return {
        "A": aa, "B": bb, "C": cc, "numerator": numerator,
        "denominator": denominator, "ratio": ratio,
        "twice_floor": F(2*floor_ratio),
    }


def rational_envelope() -> dict[str, F]:
    denominator = F(247, 250)**2-3*F(139, 500)
    return {
        "denominator_lower": denominator,
        "ratio_upper": F(72),
        "count_upper": F(COUNT_CAP),
        "tail_factor_upper": F(24),
    }


def local_spacing_envelope() -> dict[str, F]:
    """Safe arithmetic for source (3.6), lambda=9/20, local a=78/25."""
    aa, bb = F(78,25), F(19039,10000)
    main_denominator = (aa+LW_LAMBDA)/((aa+LW_LAMBDA)**2+bb**2)
    numerator_upper = KAPPA_UPPER+1/aa
    # sqrt(5)<=9/4 implies (5+sqrt(5))/(10*L)<=1/1000 at L>=30000.
    if not main_denominator-F(1,1000) > F(1,5):
        raise AssertionError("spacing denominator bound failed")
    if not numerator_upper < F(3,5):
        raise AssertionError("spacing numerator bound failed")
    return {"spacing_denominator_lower":main_denominator-F(1,1000),
            "spacing_numerator_upper":numerator_upper,
            "local_count_upper":F(2)}


def tail_integration_factor(height_log_ratio: F) -> F:
    if not isinstance(height_log_ratio, F) or not 0 <= height_log_ratio <= F(3, 2):
        raise ValueError("require a supplied height log ratio in [0,3/2]")
    gap = 160-F(23, 7)*(1+height_log_ratio)
    return 2*F(160)/gap*(5+2*LW_LAMBDA+2*(1+height_log_ratio)/gap)


def cumulative_split_bound(
    small_coefficient: F, small_decay_weight: F,
    tail_coefficient: F, tail_decay_weight: F,
) -> F:
    """A scalar envelope for the two count-INTEGRAL pieces, not zero classes."""
    values = (small_coefficient,small_decay_weight,tail_coefficient,tail_decay_weight)
    if any(not isinstance(v, F) or v < 0 for v in values):
        raise ValueError("nonnegative rational coefficients/weights required")
    return small_coefficient*small_decay_weight+tail_coefficient*tail_decay_weight


def hybrid_nonvanishing_rational_budget() -> F:
    # fixed D=160, e>27/10, c_M*160>16, lambda*(160-23/7)>70.
    return (
        F(1134, 5)*F(10, 27)**16
        +F(189, 5)*(5*10**10)*F(10, 27)**70
        +F(21, 20)*F(10, 27)**6
    )


def audit_ledger(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or Path(__file__).resolve().parents[1]
    data = json.loads((root/LEDGER).read_text(encoding="utf-8"))
    for item in data["source_registry"]:
        observed = hashlib.sha256((root/item["locator"]).read_bytes()).hexdigest()
        if observed != item["sha256"]:
            raise ValueError(f"source hash mismatch: {item['key']}")
    expected = {
        **{k:str(v) for k,v in rational_envelope().items()},
        **{k:str(v) for k,v in local_spacing_envelope().items()},
        "hybrid_nonvanishing_rational_budget": str(hybrid_nonvanishing_rational_budget()),
    }
    if any(data["rational_terminals"][k] != v for k,v in expected.items()):
        raise ValueError("rational terminal mismatch")
    if not expected["count_upper"] == "144":
        raise ValueError("source count cap mismatch")
    gates = data["project_gates"]
    names = (
        "printed_table_182_adopted", "printed_prose_364_adopted",
        "LW_Theorem8_multiplier_13804_adopted", "numeric_EF_multiplier_recovered",
        "pointwise_full_modulus_PNT_closed", "pap_11_closed", "dep_r09_closed",
        "numerical_x_cert_ready", "bounded_x_cert_range_obtained",
        "threshold_calculator_ready", "actual_prime_or_zero_computation_run",
        "source_theorem_local_axiom_used", "proof_escape_used",
    )
    if any(gates[k] is not False for k in names):
        raise ValueError("a printed/unresolved analytic gate was promoted")
    return {"status":"SOURCE_PIN_AND_RATIONAL_TERMINALS_PASS",
            "source_count":len(data["source_registry"]),**expected,
            **{k:gates[k] for k in names}}


if __name__ == "__main__":
    print(json.dumps(audit_ledger(),sort_keys=True))
