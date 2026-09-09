"""Bounded exact checks for theory 53, NOT a covering or threshold calculator.

The analytic statements are in the document. These finite fixtures cannot
certify the source constant C0, an actual prime range, or the global theorem.
"""
from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from source.h1bcor1_finite_correlation import _integer, _primes, _rational

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOV1_hypergraph_interface_v1.json"
SCOPE = {
    "boundary_mode": "end", "logs": "iterated_natural",
    "weight": "maynard_w_filtered", "u_quantifier": "fixed_X_and_source_B",
    "full_residue_edges": True, "cap_drops_whole_edge": True,
    "exception_cost_restored": True, "fixed_subset_not_all_subsets": True,
    "source_C0_numerically_known": False, "full_hypergraph_certified": False,
    "global_union_budget_closed": False, "x_cert_ready": False,
    "threshold_calculator_ready": False, "actual_prime_experiment_performed": False,
    "independently_formally_verified": False,
}
CONSTANTS = {
    "cap": "2*k", "cap_degree_loss_expectation": "3200*c_aux*X/(a*b^9)",
    "cap_failure_upper": "min(1,3200*c_aux/b^5)",
    "preparation_failure_upper": "min(1,4800*c_aux/b^5+800*c_aux/b^10+112*k*b^4/a^11)",
    "exception_count": "floor(2*X/(a*b))", "exception_fraction_upper": "8000/b^2",
    "post_cap_degree_error": "1203/b^3<=1/b^2",
    "r_hg": "2*k", "A_hg": "4*k*m+2", "D": 2,
    "kappa": "(9/10)*5^(-m)", "Delta": "X^(-1/20)",
    "log_recursion_error": "(3^j-1)/b", "xi": "3^m/b<1/10",
    "core_log_gate": "a/(20*10^(m+2))>=ln(C0)+A_hg*(2+ln(1/kappa))",
    "single_error": "(1+epsilon)*exp(xi)-1",
    "pair_error": "(1+epsilon)*exp(2*xi)-1",
    "subset_failure_upper": "min(1,(beta+2*alpha+(1+alpha)/(rho*M))/t^2)",
    "restoration_error": "#(U0 intersect E)/(rho*#U0)",
    "source_C0_value": None, "c_sono": "2e-17",
}
CHILDREN = {
    "COV1-SOURCE": "SOURCE_VERIFIED",
    "COV1-CAP": "ACTUAL_INPUTS_PROJECT_EXPLICIT",
    "COV1-EXCEPTIONS": "ACTUAL_INPUTS_PROJECT_EXPLICIT",
    "COV1-PARTITION": "ACTUAL_INPUTS_PROJECT_EXPLICIT",
    "COV1-RECURRENCE": "ACTUAL_INPUTS_PROJECT_EXPLICIT",
    "COV1-MOMENT-TRANSFER": "CONDITIONAL_ON_SOURCE_C0_GATE",
    "COV1-REALIZATION": "PROJECT_EXPLICIT_SUPPORT_LEMMA",
    "COV1-CORE-C0": "OPEN",
}


def _probability(value, name):
    q = _rational(value, name)
    if not 0 <= q <= 1:
        raise ValueError(f"{name} must be in [0,1]")
    return q


def residue_cap_toy(*, q_values, prime, offsets, law, excluded=()):
    """Keep whole residue edges, then project; never truncate an edge in place."""
    qs = tuple(q_values)
    if not 1 <= len(qs) <= 32 or len(set(qs)) != len(qs):
        raise ValueError("require 1..32 distinct toy prime vertices")
    for q in qs:
        _primes((q,))
    ps = _primes((prime,))
    if len(ps) != 1 or not qs or any(q <= prime for q in qs):
        raise ValueError("require primes q>p and a nonempty bounded vertex set")
    hs = tuple(offsets)
    if not 1 <= len(hs) <= 8 or len(set(hs)) != len(hs):
        raise ValueError("require 1..8 distinct offsets")
    for h in hs:
        _integer(h, "offset", 1, 1024)
    removed = frozenset(excluded)
    if not removed <= set(qs):
        raise ValueError("excluded values must be vertices")
    atoms = tuple(law)
    if not 1 <= len(atoms) <= 16:
        raise ValueError("bounded nonempty probability law required")
    prior = {}
    for n, weight in atoms:
        _integer(n, "residue witness", -10**6, 10**6)
        weight = _probability(weight, "weight")
        if n in prior or weight == 0:
            raise ValueError("distinct positive-mass witnesses required")
        prior[n] = weight
    if sum(prior.values(), Q(0)) != 1:
        raise ValueError("law must sum to one")
    retained = frozenset(qs)-removed
    rows, witnesses = [], {frozenset(): 0}
    loss = off_mass = Q(0)
    full_degree = {q: Q(0) for q in qs}
    cap_degree = full_degree.copy()
    for n, weight in prior.items():
        full = frozenset(q for q in qs if (q-n) % prime == 0)
        main = frozenset(n+h*prime for h in hs) & frozenset(qs)
        off = full-main
        capped = full if len(full) <= 2*len(hs) else frozenset()
        projected = capped & retained
        if projected:
            witnesses.setdefault(projected, n)
        lost = len(full)-len(capped)
        if not main <= full or lost > 2*len(off):
            raise AssertionError("cap mass inequality failed")
        loss += weight*lost
        off_mass += weight*len(off)
        for q in full:
            full_degree[q] += weight
        for q in capped:
            cap_degree[q] += weight
        rows.append({"n": n, "weight": weight, "full": full, "main": main,
                     "off": off, "capped": capped, "projected": projected})
    for edge, n in witnesses.items():
        actual = frozenset(q for q in retained if (q-n) % prime == 0)
        if actual != edge:
            raise AssertionError("support realization must be equality on retained vertices")
    return {
        "rows": rows, "witnesses": witnesses, "retained": retained,
        "removed_degree_mass": loss, "off_degree_mass": off_mass,
        "sum_degree_difference": sum((full_degree[q]-cap_degree[q] for q in qs), Q(0)),
        "full_degree": full_degree, "cap_degree": cap_degree,
        "actual_prime_experiment_performed": False, "source_C0_verified": False,
    }


def partition_toy(weights, stage_probabilities, tolerance, *, independent=True):
    """Exhaustive small independent-label law vs separate expectation oracle."""
    if independent is not True:
        raise ValueError("the partition labels must be independent")
    rows = tuple(tuple(_probability(x, "weight") for x in row) for row in weights)
    probs = tuple(_probability(p, "stage probability") for p in stage_probabilities)
    t = _rational(tolerance, "tolerance")
    if (not 1 <= len(rows) <= 8 or not 1 <= len(probs) <= 4 or
            not rows[0] or len(rows[0]) > 8 or any(len(row) != len(rows[0]) for row in rows) or
            sum(probs, Q(0)) > 1 or t <= 0):
        raise ValueError("bounded rectangular array, valid probabilities and t>0 required")
    probabilities = probs + (1-sum(probs, Q(0)),)
    states = len(probabilities)**len(rows)
    if states > 50_000:
        raise ValueError("toy work budget exceeded")
    count = len(rows[0])
    target = [[p*sum((row[q] for row in rows), Q(0)) for q in range(count)] for p in probs]
    mean = [[Q(0) for _ in range(count)] for _ in probs]
    failures = [[Q(0) for _ in range(count)] for _ in probs]
    total = family_failure = Q(0)
    for labels in product(range(len(probabilities)), repeat=len(rows)):
        prob = Q(1)
        for label in labels:
            prob *= probabilities[label]
        total += prob
        any_bad = False
        for j in range(len(probs)):
            for q in range(count):
                val = sum((rows[p][q] for p, label in enumerate(labels) if label == j), Q(0))
                mean[j][q] += prob*val
                if abs(val-target[j][q]) >= t:
                    failures[j][q] += prob
                    any_bad = True
        if any_bad:
            family_failure += prob
    return {"states": states, "mass": total, "mean": mean, "target": target,
            "per_event_failure": failures, "family_failure": family_failure,
            "union_upper": min(Q(1), sum((sum(row, Q(0)) for row in failures), Q(0)))}


def exp_enclosure(x, *, terms=18):
    """Exact rational Taylor enclosure for |x|<=1 only."""
    x = _rational(x, "x")
    _integer(terms, "terms", 4, 32)
    if abs(x) > 1:
        raise ValueError("bounded Taylor domain is [-1,1]")
    y = abs(x)
    term = total = Q(1)
    for j in range(1, terms+1):
        term *= y/j
        total += term
    next_term = term*y/(terms+1)
    upper = total+next_term/(1-y/(terms+2))
    return (1/upper, 1/total) if x < 0 else (total, upper)


def log5_enclosure():
    r = Q(2, 3)
    terms = 20
    lower = 2*sum((r**(2*j+1)/(2*j+1) for j in range(terms)), Q(0))
    tail = 2*r**(2*terms+1)/((2*terms+1)*(1-r*r))
    return lower, lower+tail


def recurrence_step_enclosure(z, eta):
    z, eta = _rational(z, "z"), _rational(eta, "eta")
    if abs(z) > Q(1, 10) or abs(eta) > Q(1, 2000):
        raise ValueError("bounded recurrence fixture outside the proved domain")
    exp_lo, exp_hi = exp_enclosure(-z)
    llo, lhi = log5_enclosure()
    a, b = 1-(1+eta)*exp_hi, 1-(1+eta)*exp_lo
    corners = (llo*a, llo*b, lhi*a, lhi*b)
    return z+min(corners), z+max(corners)


def scalar_diagnostics():
    lo, hi = log5_enclosure()
    exp_lo, exp_hi = exp_enclosure(Q(1, 10))
    return {
        "log5_lower": lo, "log5_upper": hi,
        "exp_tenth_lower": exp_lo, "exp_tenth_upper": exp_hi,
        "derivative_upper": 1+Q(13, 8)*Q(2001, 2000)*Q(10, 9),
        "degree_ratio_upper": Q(13, 8)*Q(2001, 2000)*Q(10, 9),
        "xi_m_le_4_upper": Q(81, 2000), "xi_m_ge_5_upper": Q(243, 3125),
        "exception_coefficient_upper": Q(614400, 79),
        "partition_positive_integer_guard": 2000**4 >= 4500*576,
        "core_gate_polynomial_guards": (
            2**600 > 12*2000**2, 2**1000 > 4000*2000**2),
        "source_C0_verified": False, "x_cert_ready": False,
    }


def subset_failure_bound(*, single_error, pair_error, rho, count, tolerance):
    alpha, beta = (_rational(single_error, "single error"), _rational(pair_error, "pair error"))
    rho = _probability(rho, "rho")
    t = _rational(tolerance, "tolerance")
    _integer(count, "count", 1, 100_000)
    if min(alpha, beta) < 0 or rho == 0 or t <= 0:
        raise ValueError("nonnegative errors, rho>0 and tolerance>0 required")
    return min(Q(1), (beta+2*alpha+(1+alpha)/(rho*count))/t**2)


def restoration_error(*, original_count, removed_count, rho):
    _integer(original_count, "original count", 1, 100_000)
    _integer(removed_count, "removed count", 0, original_count-1)
    rho = _probability(rho, "rho")
    if rho == 0:
        raise ValueError("rho>0 required")
    return Q(removed_count, original_count)/rho


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(doc, *, check_hashes=True):
    """Scope and provenance guard; cannot upgrade a hypothesis to a theorem."""
    issues = []
    if doc.get("id") != "H1b-COV1" or doc.get("schema_version") != "1.0.0":
        issues.append("contract identity mismatch")
    for key, value in (("scope", SCOPE), ("constants", CONSTANTS), ("children", CHILDREN)):
        if doc.get(key) != value:
            issues.append(f"{key} mismatch")
    if doc.get("remaining_open_work") != [f"DEP-R{i:02}" for i in range(7, 13)]:
        issues.append("unsupported root closure")
    if doc.get("next_gate") != "H1b-COV1a / FGKMT Section 5 numerical C0":
        issues.append("next gate mismatch")
    if doc.get("errata") != [{
        "target": "theory52 equation52.17", "kind": "missing_plus_in_display",
        "corrected_formula": "min(1,1600*c_aux/b^5+800*c_aux/b^10+112*k*b^4/a^11)",
        "pinned_original_preserved": True, "contract_and_code_already_correct": True,
    }]:
        issues.append("erratum must preserve three additive terms")
    pins = doc.get("source_pins", [])
    expected = {"FMT", "FGKMT", "COR1_49", "COR2_50", "PROOF51", "PROOF52",
                "COR3_CONTRACT", "PROOF53"}
    if (len(pins) != len(expected) or
            {p.get("id") for p in pins if isinstance(p, dict)} != expected):
        issues.append("source inventory mismatch")
    for pin in pins:
        if not isinstance(pin, dict) or not isinstance(pin.get("path"), str):
            issues.append("malformed source pin")
            continue
        path = (ROOT / pin["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            issues.append("source absent or path escapes root")
        elif check_hashes and sha256(path.read_bytes()).hexdigest() != pin.get("sha256"):
            issues.append(f"hash mismatch: {pin.get('id')}")
    return issues
