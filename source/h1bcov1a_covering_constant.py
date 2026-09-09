"""Theory 54 bounded exact algebra checks; not an X_cert calculator.

The all-parameter quantitative proof is the document, not these finite toys.
Only rational finite probability laws are accepted. No prime data is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial, prod
from pathlib import Path

from source.h1bcor1_finite_correlation import _integer, _rational

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOV1a_covering_constant_v1.json"
SCOPE = {
    "boundary_mode": "end", "logs": "iterated_natural",
    "weight": "maynard_w_filtered", "u_quantifier": "fixed_X_and_source_B",
    "core_theorem_all_parameters_project_proved": True,
    "original_edge_independence_assumed": False,
    "same_index_uses_independent_marginal_copies": True,
    "actual_COV1_smallness_gate_closed": True,
    "fixed_subset_not_simultaneous_all_subsets": True,
    "global_union_budget_closed": False, "x_cert_ready": False,
    "threshold_calculator_ready": False, "actual_prime_experiment_performed": False,
    "independently_formally_verified": False, "C0_optimality_claimed": False,
}
CONSTANTS = {
    "C0_sufficient": 100, "t_upper": "1/100",
    "t_definition": "delta^(1/10^(m+2))", "prior_error": "t^100",
    "delta_upper_m_ge_1": "t^1000", "normalization_tolerance": "t^30",
    "normalization_square_error": "4*t^100", "normalization_bad_probability": "4*t^40",
    "conditional_first_moment_error": "4*t^99",
    "conditional_second_moment_error": "4*t^98",
    "conditional_centered_square_error": "12*t^98",
    "degree_union_bad_probability": "7*t^14",
    "good_log_error": "3*t^11", "final_relative_error": "8*t^11<=t^10",
    "actual_child_cutoff": "X>=2*exp(10^1000)",
    "actual_core_gate": "a/(20*10^(m+2))>=ln(100)+A_hg*(2+ln(1/kappa))",
    "c_sono": "2e-17",
}
CHILDREN = {key: "PROJECT_EXPLICIT" for key in (
    "C0-NORM", "C0-CONDITIONAL", "C0-TAYLOR", "C0-INDUCTION", "C0-ACTUAL-GATE"
)}


def _prob(q, label, *, positive=False):
    q = _rational(q, label)
    if not (0 < q <= 1 if positive else 0 <= q <= 1):
        raise ValueError(f"{label} is outside the probability domain")
    return q


def _subset(values, universe):
    values = tuple(values)
    if len(values) != len(set(values)) or not set(values) <= universe:
        raise ValueError("distinct vertices in the model required")
    return frozenset(values)


def _law(atoms, universe, maximum):
    atoms = tuple(atoms)
    if not 1 <= len(atoms) <= maximum:
        raise ValueError("law exceeds bounded nonempty support")
    result = {}
    for vertices, probability in atoms:
        edge = _subset(vertices, universe)
        if edge in result:
            raise ValueError("duplicate atom")
        result[edge] = _prob(probability, "atom probability", positive=True)
    if sum(result.values(), Q(0)) != 1:
        raise ValueError("law must sum exactly to one")
    return result


@dataclass
class ToyModel:
    point_probabilities: dict
    w_law: dict
    edge_laws: tuple

    def p(self, edge):
        return prod((self.point_probabilities[v] for v in edge), start=Q(1))

    def survives(self, edge):
        return sum((mass for w, mass in self.w_law.items() if edge <= w), Q(0))


def make_model(point_probabilities, w_law, edge_laws):
    """At most five vertices, four laws, and sixteen atoms per edge law."""
    if not 1 <= len(point_probabilities) <= 5:
        raise ValueError("1..5 toy vertices required")
    ps = {}
    for v, p in point_probabilities.items():
        _integer(v, "vertex", 0, 100)
        ps[v] = _prob(p, "P(v)", positive=True)
    universe = frozenset(ps)
    ws = _law(w_law, universe, 32)
    edges = tuple(edge_laws)
    if not 1 <= len(edges) <= 4:
        raise ValueError("1..4 edge laws required")
    return ToyModel(ps, ws, tuple(_law(law, universe, 16) for law in edges))


def _index(model, i):
    return _integer(i, "edge index", 0, len(model.edge_laws)-1)


def normalization(model, i):
    """Compute Xi on W; EXi^2 also from an independent product-law oracle."""
    i = _index(model, i)
    law = model.edge_laws[i]
    xs = {
        w: sum((mass/model.p(s) for s, mass in law.items() if s <= w), Q(0))
        for w in model.w_law
    }
    first = sum((model.w_law[w]*x for w, x in xs.items()), Q(0))
    second = sum((model.w_law[w]*x*x for w, x in xs.items()), Q(0))
    second_copy = sum((
        ms*mt*model.survives(s | t)/(model.p(s)*model.p(t))
        for s, ms in law.items() for t, mt in law.items()
    ), Q(0))
    return {"values": xs, "first": first, "second": second,
            "second_product_copy": second_copy,
            "centered_square": second-2*first+1}


def induction_relative_error(model):
    """Exhaust all at-most-5-vertex subsets; no independence assumed for W."""
    vertices = tuple(model.point_probabilities)
    errors = {}
    for count in range(len(vertices)+1):
        for values in combinations(vertices, count):
            e = frozenset(values)
            errors[e] = abs(model.survives(e)/model.p(e)-1)
    return max(errors.values()), errors


def conditional_degree_moments(model, e, v):
    """Direct W oracle vs marginal-product expansion, INCLUDING i=i'."""
    e = _subset(e, model.point_probabilities.keys())
    if v not in e:
        raise ValueError("v must belong to the conditioning set")
    event_probability = model.survives(e)
    if event_probability == 0:
        raise ValueError("cannot condition on a probability-zero event")
    atoms = tuple((i, s, mass) for i, law in enumerate(model.edge_laws)
                  for s, mass in law.items() if v in s)
    values = {
        w: sum((mass/model.p(s) for _, s, mass in atoms if s <= w), Q(0))
        for w in model.w_law if e <= w
    }
    first = sum((model.w_law[w]*hv for w, hv in values.items()), Q(0))/event_probability
    second = sum((model.w_law[w]*hv*hv for w, hv in values.items()), Q(0))/event_probability
    expanded_first = sum((
        mass*model.survives(e | s)/(model.p(s)*event_probability)
        for _, s, mass in atoms
    ), Q(0))
    by_index = {}
    for i in range(len(model.edge_laws)):
        for j in range(len(model.edge_laws)):
            by_index[i, j] = sum((
                ms*mt*model.survives(e | s | t) /
                (model.p(s)*model.p(t)*event_probability)
                for ii, s, ms in atoms for jj, t, mt in atoms if ii == i and jj == j
            ), Q(0))
    degree = sum((mass for _, _, mass in atoms), Q(0))
    center = degree/model.p({v})
    return {"first": first, "second": second, "expanded_first": expanded_first,
            "expanded_second": sum(by_index.values(), Q(0)), "by_index": by_index,
            "center": center, "centered_square": second-2*center*first+center*center,
            "conditioning_probability": event_probability}


def normalized_overlap_ratio(model, s, t, e, v):
    s, t, e = (_subset(x, model.point_probabilities.keys()) for x in (s, t, e))
    if v not in (s & t & e):
        raise ValueError("distinguished vertex must be in the triple intersection")
    direct = model.p({v})**2*model.p(s | t | e)/(model.p(s)*model.p(t)*model.p(e))
    factors = Q(1)
    for w in (s | t | e)-{v}:
        multiplicity = int(w in s)+int(w in t)+int(w in e)
        factors /= model.p({w})**(multiplicity-1)
    return direct, factors


def reweighted_laws(model, w, tolerance):
    w = _subset(w, model.point_probabilities.keys())
    if w not in model.w_law:
        raise ValueError("W must be a positive-mass model atom")
    tolerance = _rational(tolerance, "tolerance")
    if not 0 < tolerance <= Q(1, 2):
        raise ValueError("normalization tolerance must be in (0,1/2]")
    laws, good, xs = [], [], []
    for i, original in enumerate(model.edge_laws):
        x = normalization(model, i)["values"][w]
        xs.append(x)
        f = abs(x-1) <= tolerance
        good.append(f)
        # Deliberate branch: do not evaluate zero/X when normalization is bad.
        law = ({s: mass/(x*model.p(s)) for s, mass in original.items() if s <= w}
               if f else {frozenset(): Q(1)})
        if sum(law.values(), Q(0)) != 1 or not set(law) <= set(original) | {frozenset()}:
            raise AssertionError("reweighting normalization or support failed")
        laws.append(law)
    return {"laws": tuple(laws), "good": tuple(good), "normalizers": tuple(xs)}


def last_round_survival(model, w, e, tolerance):
    """Product oracle vs exhaustive independent conditional choices."""
    w = _subset(w, model.point_probabilities.keys())
    e = _subset(e, model.point_probabilities.keys())
    result = reweighted_laws(model, w, tolerance)
    laws = result["laws"]
    if prod(len(law) for law in laws) > 4096:
        raise ValueError("joint enumeration exceeds 4096 toy combinations")
    lambdas = tuple(sum((mass for s, mass in law.items() if s & e), Q(0)) for law in laws)
    value = prod((1-lam for lam in lambdas), start=Q(1)) if e <= w else Q(0)
    brute = Q(0)
    if e <= w:
        for choices in product(*(tuple(law.items()) for law in laws)):
            union = frozenset().union(*(s for s, _ in choices))
            if not e & union:
                brute += prod((mass for _, mass in choices), start=Q(1))
    degree_sum = sum((mass*len(s & e) for law in laws for s, mass in law.items()), Q(0))
    pair_cost = sum((mass*(len(s & e)*(len(s & e)-1)//2)
                     for law in laws for s, mass in law.items()), Q(0))
    return {**result, "product": value, "exhaustive": brute, "lambdas": lambdas,
            "degree_sum": degree_sum, "union_sum": sum(lambdas, Q(0)),
            "pair_cost": pair_cost}


def scalar_budget(t=Q(1, 100)):
    """Positive-monomial inequalities after the analytic all-t reduction."""
    t = _rational(t, "t")
    if not 0 < t <= Q(1, 100):
        raise ValueError("t must be in (0,1/100]")
    checks = {
        "conditional_ratio": t**100 <= Q(1, 3),
        "nonzero_denominator": t**30 <= Q(1, 2),
        "normalization": 2*t**898 <= 1,
        "second_moment": 6*t**897 <= 1,
        "bad_normalizer_transfer": 4*t**10 <= 1,
        "vertex_union": 12*t**23 <= 1,
        "taylor_sum": 4*t**999 <= 1,
        "good_log_sum": 3*t**986 <= 1,
        "exponential_remainder": 3*t**11 <= Q(1, 2),
        "conditional_relative": 7*t*t <= 1,
        "final_multiply": t**89+7*t**100 <= 1,
        "induction_target": 8*t <= 1,
        "direct_normalization": 3*t**100+2*t**998 <= 4*t**100,
        "direct_first": 3*t**99+2*t**997 <= 4*t**99,
        "direct_second": 3*t**98+6*t**995 <= 4*t**98,
        "direct_final": t**100+(1+t**100)*7*t**11 <= 8*t**11 <= t**10,
    }
    return checks


def actual_gate_anchors():
    """Finite integer anchors for theory53/54 monotone analytic log bounds."""
    return {
        "exp5_lower_partial_sum_gt100": sum((Q(5)**j/factorial(j) for j in range(7)), Q(0)) > 100,
        "parameter_anchor": 2**600 > 12*2000**2,
        "smallness_anchor": 2**1000 > 4000*2000**2,
        "coefficient_unchanged": CONSTANTS["c_sono"] == "2e-17",
    }


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(doc, *, check_hashes=True):
    issues = []
    for key, expected in (("schema_version", "1.0.0"), ("id", "H1b-COV1a"),
                          ("scope", SCOPE), ("constants", CONSTANTS), ("children", CHILDREN)):
        if doc.get(key) != expected:
            issues.append(f"{key} mismatch")
    if doc.get("closed_actual_work") != [f"DEP-R{i:02}" for i in range(1, 8)]:
        issues.append("actual closed scope mismatch")
    if doc.get("remaining_open_work") != [f"DEP-R{i:02}" for i in range(8, 13)]:
        issues.append("root obligations must remain open")
    if doc.get("next_gate") != "H1b-COV2 / DEP-R08":
        issues.append("next gate mismatch")
    pins = doc.get("source_pins", [])
    expected = {"FGKMT", "PROOF53", "COV1_CONTRACT", "PROOF54"}
    if len(pins) != len(expected) or {p.get("id") for p in pins if isinstance(p, dict)} != expected:
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
    if not all(scalar_budget().values()) or not all(actual_gate_anchors().values()):
        issues.append("exact scalar anchors failed")
    return issues
