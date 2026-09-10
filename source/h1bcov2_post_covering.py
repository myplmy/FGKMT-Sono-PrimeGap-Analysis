"""Bounded exact checks for theory 55; never a prime or X_cert calculator.

The analytic proof lives in the theory document.  This module checks the
finite grid, floor, restoration and union-bound algebra with exact rationals,
and freezes the successor contract/provenance.  It deliberately does not try
to instantiate the final Sono A/epsilon budget.
"""
from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOV2_post_covering_v1.json"

SCOPE = {
    "boundary_mode": "end",
    "logs": "iterated_natural",
    "auxiliary_X_not_final_gap_X": True,
    "fixed_A_epsilon_eta_before_random_choices": True,
    "equal_grid_endpoint_safe": True,
    "postselection_or_uncountable_union_claimed": False,
    "outer_and_inner_events_composed_sequentially_without_independence": True,
    "smooth_remainder_deterministic": True,
    "final_A_epsilon_eta_instantiated": False,
    "same_sono_coefficient_budget_closed": False,
    "broad_sieve_weight_package_closed": False,
    "x_cert_ready": False,
    "threshold_calculator_ready": False,
    "actual_prime_experiment_performed": False,
    "independently_formally_verified": False,
}

CONSTANTS = {
    "c_aux": "1/(153600*ln(5))",
    "A_domain": "A>=1 fixed",
    "epsilon_domain": "0<epsilon<=1 fixed",
    "eta_domain": "0<eta<=1/4 fixed",
    "grid_cells": "J=ceil(2/epsilon)",
    "grid_width": "d=1/J; epsilon/(2+epsilon)<=d<=epsilon/2",
    "precover_relative_error": "r_pre=1/(100*b^2)",
    "density_choice": "m=floor(log_5(80*c_aux*b/A)); A_prime=5^(-m)*80*c_aux*b",
    "density_floor_gate": "80*c_aux*b/A>=5",
    "density_range": "A<=A_prime<5*A and 1<=m<=log_5(b)",
    "exception_count": "E<=floor(2*X/(a*b))",
    "cell_restoration": "e_cell<=2/((1-r_pre)*A*d*b)<7/(A*epsilon*b)",
    "composed_cell_relative_error": "r_pre+(1+r_pre)*(t_cov+e_cell)",
    "family_size": "K=J+1 (J cells and the whole interval)",
    "outer_failure": "4800*c_aux/b^5+800*c_aux/b^10+112*k*b^4/a^11+3*K*b^6/a^17",
    "inner_failure": "K*(beta_hg+2*alpha_hg+2*(1+alpha_hg)*a/((1-r_pre)*A*d*X))/t_cov^2",
    "smooth_remainder": "#R<(log(b)/(17*b))*X/a for b>=exp(200) and the stated Rankin gates",
    "finite_output": "A*(1-eta)*X/a<=#T<=5*A*(1+2*eta)*X/a; local upper<=5*A*(1+2*eta)*(2*length+epsilon)*X/a",
    "actual_child_cutoff": "maximum of inherited X>=2*exp(10^1000) and the explicit COV2 gates",
    "c_sono": "2e-17",
}

CHILDREN = {
    "COV2-GRID": "PROJECT_EXPLICIT",
    "COV2-FLOOR": "PROJECT_EXPLICIT",
    "COV2-RESTORATION": "PROJECT_EXPLICIT",
    "COV2-SMOOTH": "PROJECT_EXPLICIT",
    "COV2-SEQUENTIAL": "PROJECT_EXPLICIT",
    "DEP-R08": "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
}

SOURCE_REPAIRS = [
    {
        "target": "Sono Proposition 6.1 to Proposition 3.1 cell-cover sentence",
        "risk": "literal printed cell count can be off by one for a short interval crossing a grid boundary",
        "repair": "J=ceil(2/epsilon) equal cells and total covered length<=length+2/J<=length+epsilon",
        "source_result_preserved": True,
    },
    {
        "target": "Sono printed 1 << 80*c/A <= 1",
        "risk": "Vinogradov lower relation has no numerical constant",
        "repair": "replace the needed positive-m fact by the explicit gate 80*c*b/A>=5; retain 80*c/A<1",
        "source_result_preserved": True,
    },
]


def _rational(value, label):
    if isinstance(value, bool) or not isinstance(value, Q):
        raise ValueError(f"{label} must be an exact Fraction")
    return value


def _unit(value, label, *, positive=False):
    value = _rational(value, label)
    if not (0 < value <= 1 if positive else 0 <= value <= 1):
        raise ValueError(f"{label} is outside its unit interval")
    return value


def equal_grid(epsilon, *, maximum_cells=100_000):
    """Return an exact half-open partition ((j-1)/J,j/J] of (0,1]."""
    epsilon = _unit(epsilon, "epsilon", positive=True)
    j = (2 * epsilon.denominator + epsilon.numerator - 1) // epsilon.numerator
    if j < 2 or j > maximum_cells:
        raise ValueError("grid exceeds the bounded exact-check budget")
    width = Q(1, j)
    cells = tuple((Q(i, j), Q(i + 1, j)) for i in range(j))
    if not (epsilon / (2 + epsilon) <= width <= epsilon / 2):
        raise AssertionError("ceil-derived grid-width enclosure failed")
    return {"count": j, "width": width, "cells": cells}


def cover_interval(alpha, beta, epsilon, *, maximum_cells=100_000):
    """Cover (alpha,beta] by whole equal-grid cells, with exact endpoints."""
    alpha = _unit(alpha, "alpha")
    beta = _unit(beta, "beta", positive=True)
    if alpha >= beta:
        raise ValueError("require 0<=alpha<beta<=1")
    grid = equal_grid(epsilon, maximum_cells=maximum_cells)
    selected = tuple(
        i for i, (left, right) in enumerate(grid["cells"])
        if right > alpha and left < beta
    )
    covered_length = len(selected) * grid["width"]
    target_length = beta - alpha
    if not selected or covered_length > target_length + 2 * grid["width"]:
        raise AssertionError("deterministic interval-cover bound failed")
    return {
        **grid,
        "selected": selected,
        "target_length": target_length,
        "covered_length": covered_length,
        "sono_length_upper": 2 * target_length + epsilon,
    }


def density_floor(*, b, c_aux, A, maximum_m=100_000):
    """Exact floor(log_5(80*c*b/A)) without floating logarithms."""
    b = _rational(b, "b")
    c_aux = _rational(c_aux, "c_aux")
    A = _rational(A, "A")
    if b <= 0 or c_aux <= 0 or A < 1:
        raise ValueError("require b,c_aux>0 and A>=1")
    ratio = 80 * c_aux * b / A
    if ratio < 5:
        raise ValueError("the explicit positive-m density gate is not met")
    m = 1
    power = Q(5)
    while power * 5 <= ratio:
        m += 1
        power *= 5
        if m > maximum_m:
            raise ValueError("floor loop exceeds the bounded exact-check budget")
    a_prime = 80 * c_aux * b / power
    if not (power <= ratio < 5 * power and A <= a_prime < 5 * A):
        raise AssertionError("density floor enclosure failed")
    return {"m": m, "five_to_m": power, "ratio": ratio, "A_prime": a_prime}


def restoration_upper(*, r_pre, A, width, b):
    """E/(rho*M0) for a cell, using E<=2X/(ab) and A' >= A."""
    r_pre = _unit(r_pre, "r_pre")
    A = _rational(A, "A")
    width = _unit(width, "width", positive=True)
    b = _rational(b, "b")
    if r_pre >= 1 or A < 1 or b <= 0:
        raise ValueError("invalid restoration parameters")
    return Q(2) / ((1 - r_pre) * A * width * b)


def composed_relative_error(*, r_pre, covering_tolerance, restoration):
    """Convert the rho*M0 error to the ideal rho*mu normalization."""
    r_pre = _unit(r_pre, "r_pre")
    covering_tolerance = _rational(covering_tolerance, "covering_tolerance")
    restoration = _rational(restoration, "restoration")
    if r_pre >= 1 or covering_tolerance <= 0 or restoration < 0:
        raise ValueError("invalid composed-error parameters")
    return r_pre + (1 + r_pre) * (covering_tolerance + restoration)


def hypergraph_relative_parameters(*, epsilon_hg, xi):
    """Accept rational enclosures E>=epsilon_hg and Z>=xi and return safe bounds.

    If E,Z<=1/100, exp(Z)<=1/(1-Z) and exp(2Z)<=1/(1-2Z).
    """
    epsilon_hg = _unit(epsilon_hg, "epsilon_hg")
    xi = _unit(xi, "xi")
    if epsilon_hg > Q(1, 100) or xi > Q(1, 100):
        raise ValueError("rational enclosures must be at most 1/100")
    alpha = (1 + epsilon_hg) / (1 - xi) - 1
    beta = (1 + epsilon_hg) / (1 - 2 * xi) - 1
    return {"alpha_upper": alpha, "beta_upper": beta}


def sequential_failure_bounds(
    *, c_aux, b, a, k, family_size, precover_term, inner_v, tolerance
):
    """Exact outer/inner union bounds; they are sequential, not independent."""
    values = {
        "c_aux": _rational(c_aux, "c_aux"),
        "b": _rational(b, "b"),
        "a": _rational(a, "a"),
        "k": _rational(k, "k"),
        "precover_term": _rational(precover_term, "precover_term"),
        "inner_v": _rational(inner_v, "inner_v"),
        "tolerance": _rational(tolerance, "tolerance"),
    }
    if any(values[name] <= 0 for name in ("c_aux", "b", "a", "k", "tolerance")):
        raise ValueError("positive parameters required")
    if values["precover_term"] < 0 or values["inner_v"] < 0:
        raise ValueError("failure terms cannot be negative")
    if isinstance(family_size, bool) or not isinstance(family_size, int) or not 1 <= family_size <= 100_001:
        raise ValueError("bounded positive integer family_size required")
    outer = (
        4800 * values["c_aux"] / values["b"] ** 5
        + 800 * values["c_aux"] / values["b"] ** 10
        + 112 * values["k"] * values["b"] ** 4 / values["a"] ** 11
        + values["precover_term"]
    )
    inner = family_size * values["inner_v"] / values["tolerance"] ** 2
    return {"outer": outer, "inner": inner, "sequential_existence": outer < 1 and inner < 1}


def smooth_remainder_ratio_upper(*, log_b, b):
    """Return the theory-55 coefficient multiplying X/a after its gates hold."""
    log_b = _rational(log_b, "log_b")
    b = _rational(b, "b")
    if log_b <= 0 or b <= 0 or log_b >= b:
        raise ValueError("require 0<log(b)<b")
    return log_b / (17 * b)


def scalar_anchors():
    """Exact elementary inequalities used by the smooth-number proof."""
    return {
        "ein_first_interval": 10_000 < 2**50,
        "ein_two_piece": Q(1, 100) + Q(51, 50) == Q(103, 100),
        "theta_ein_coefficient": (
            Q(21, 20) * Q(27, 25) == Q(567, 500)
            and Q(567, 500) < Q(189, 160)
        ),
        "ln4_margin_after_ein": Q(4, 3) - Q(1, 19) - Q(189, 160) == Q(907, 9120),
        "e7_c_aux_coarse": 4 * 3**7 * 17 < 153_600,
        "two_to_three_quarters": 8 * 81 > 625,
        "higher_euler_tail": Q(5, 4) * 2 < 3,
        "m_power_exponents": 3**4 < 5**3 and 10**2 < 5**3,
        "restoration_seven_factor": Q(6, 1) / Q(99, 100) < 7,
        "eta_output_composition": Q(1, 4) + Q(1, 4) <= Q(1, 2),
        "coefficient_unchanged": CONSTANTS["c_sono"] == "2e-17",
    }


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(doc, *, check_hashes=True):
    issues = []
    for key, expected in (
        ("schema_version", "1.0.0"),
        ("id", "H1b-COV2"),
        ("scope", SCOPE),
        ("constants", CONSTANTS),
        ("children", CHILDREN),
        ("source_repairs", SOURCE_REPAIRS),
    ):
        if doc.get(key) != expected:
            issues.append(f"{key} mismatch")
    if doc.get("closed_actual_work") != [f"DEP-R{i:02}" for i in range(1, 9)]:
        issues.append("actual closed scope mismatch")
    if doc.get("remaining_open_work") != [f"DEP-R{i:02}" for i in range(9, 13)]:
        issues.append("root obligations must remain open")
    if doc.get("next_gate") != "DEP-R09 / numerical PAP source-and-constant audit":
        issues.append("next gate mismatch")
    if doc.get("closed_claim") != (
        "DEP-R08 actual post-covering interface is parameterized explicit for each fixed "
        "A, epsilon and eta after its displayed finite gates."
    ):
        issues.append("closed claim mismatch")
    pins = doc.get("source_pins", [])
    expected_ids = {"SONO", "FMT", "ROSSER_SCHOENFELD", "PROOF51", "PROOF53", "PROOF54"}
    if len(pins) != len(expected_ids) or {p.get("id") for p in pins if isinstance(p, dict)} != expected_ids:
        issues.append("source inventory mismatch")
    for pin in pins:
        if not isinstance(pin, dict) or not isinstance(pin.get("path"), str):
            issues.append("malformed source pin")
            continue
        path = (ROOT / pin["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            issues.append("source missing or escaping root")
        elif check_hashes and sha256(path.read_bytes()).hexdigest() != pin.get("sha256"):
            issues.append(f"source hash mismatch: {pin.get('id')}")
    if not all(scalar_anchors().values()):
        issues.append("exact scalar anchor failed")
    return issues
