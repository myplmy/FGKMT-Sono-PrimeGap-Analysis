"""Theory 50: bounded exact toys for the off-tuple expectation and Markov budget.

Not a prime experiment, a threshold calculator, or independent formal proof.
All-parameter justification is in theory 50; toys only audit finite algebra.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import prod
from pathlib import Path

from source.h1bcor1_finite_correlation import (
    _integer, _primes, _rational, conditional_law, sigma_toy,
    survival_probability,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOR2_off_tuple_budget_v1.json"
CLOSED_IDS = ("DEP-R01", "DEP-R02", "DEP-R04", "DEP-R05")
REMAINING_IDS = tuple(f"DEP-R{i:02}" for i in range(1, 13)
                      if f"DEP-R{i:02}" not in CLOSED_IDS)
SCOPE = {
    "boundary_mode": "end",
    "logs": "iterated_natural",
    "weight": "maynard_w_filtered",
    "u_quantifier": "fixed_X_and_source_B",
    "child_cutoff": "X>=2*exp(10^1000)",
    "q_survival_required": True,
    "distinct_k_plus_one_required": True,
    "negative_zero_positive_h_included": True,
    "conditioning_denominator_preserved": True,
    "global_union_budget_closed": False,
    "full_hypergraph_certified": False,
    "x_cert_ready": False,
    "threshold_calculator_ready": False,
    "actual_prime_experiment_performed": False,
    "independently_formally_verified": False,
}
CONSTANTS = {
    "c_aux": "1/(153600*ln(5))",
    "c_sono": "2e-17",
    "h_count_upper": "9*Y/X",
    "correlation_epsilon_upper": "1/100",
    "sigma_y_multiplier": "26/25*80",
    "expectation_upper": "800*c_aux*X/(a*b^9)",
    "exception_value": "1/b^3",
    "exception_count_upper": "floor(X/(2*a*b))",
    "failure_upper": "min(1,1600*c_aux/b^5)",
    "conditioned_value_upper": "2/b^3",
    "two_event_failure_upper": "min(1,1600*c_aux/b^5+7/a^8)",
}


def off_tuple_shifts(x, y, offsets):
    """Enumerate exactly |h|<4Y/X, with all tuple offsets excluded (toy only)."""
    x, y = _rational(x, "x"), _rational(y, "y")
    if not 0 < x <= y:
        raise ValueError("require 0<x<=y")
    hs = tuple(offsets)
    if not 1 <= len(hs) <= 4 or len(set(hs)) != len(hs):
        raise ValueError("one to four distinct toy offsets required")
    for h in hs:
        _integer(h, "tuple offset", 1, 100)
    radius = 4*y/x
    ceil_radius = -(-radius.numerator // radius.denominator)
    if 2*ceil_radius-1 > 1000:
        raise ValueError("toy h domain exceeds 1000 integers")
    return tuple(h for h in range(1-ceil_radius, ceil_radius) if h not in hs)


def off_tuple_points(q, p, h, offsets):
    """The extra q plus k distinct tuple points; collisions modulo s are OK."""
    for n, name in ((q, "q"), (p, "p"), (h, "h")):
        _integer(n, name, -10**6, 10**6)
    hs = tuple(offsets)
    if p <= 0 or not 1 <= len(hs) <= 4:
        raise ValueError("positive p and one to four offsets required")
    for hi in hs:
        _integer(hi, "offset", 1, 100)
    if len(set(hs)) != len(hs) or h in hs:
        raise ValueError("off-tuple distinctness requires distinct hi and h not in H")
    return (q, *(q+(hi-h)*p for hi in hs))


def markov_exception_budget(expectation, value_cutoff, count_cutoff):
    """For nonnegative total, bound P(# {value>cutoff}>count_cutoff)."""
    e = _rational(expectation, "expectation")
    delta = _rational(value_cutoff, "value_cutoff")
    count = _rational(count_cutoff, "count_cutoff")
    if e < 0 or delta <= 0 or count <= 0:
        raise ValueError("expectation>=0 and both cutoffs>0 required")
    return min(Fraction(1), e/(delta*count))


def finite_scalar_budget(loglog_x_lower=2000):
    """Conservative rational scalar bounds only; does not verify actual inputs.

    ln(5)>1, b>=input and a>=2 are assumed. No exponentiation of X, no k array.
    """
    b = _rational(loglog_x_lower, "loglog_x_lower")
    if b < 2000:
        raise ValueError("this scalar diagnostic inherits b>=2000")
    composition = 9*Fraction(101, 100)*Fraction(26, 25)*80
    assert composition == Fraction(94536, 125) < 800
    return {
        "composition_multiplier": composition,
        "expectation_multiplier": 800,
        "failure_multiplier": 1600,
        "failure_upper_using_ln5_gt_one": Fraction(1, 96)/b**5,
        "structural_and_log_inputs_assumed": True,
        "x_cert_ready": False,
        "actual_prime_experiment_performed": False,
        "independent_formal_verification": False,
    }


def off_tuple_toy(*, x, y, p_priors, q_values, offsets, primes,
                  eta=Fraction(1, 2), value_cutoff=Fraction(1, 4),
                  count_cutoff=Fraction(1, 2), independent_uniform=True):
    """Two independent finite expectation computations and conditioned replay.

    Main oracle enumerates all residue choices and alive prior atoms. The second
    uses the prime-wise survival product. Neither oracle uses actual prime data.
    Toy moduli/parameters need not meet the enormous analytic source cutoff.
    """
    if independent_uniform is not True:
        raise ValueError("residue independence/uniformity cannot be removed")
    x, y = _rational(x, "x"), _rational(y, "y")
    hs = tuple(offsets)
    shifts = off_tuple_shifts(x, y, hs)
    ps = _primes(primes)
    if not isinstance(p_priors, dict) or not 1 <= len(p_priors) <= 4:
        raise ValueError("one to four toy p priors required")
    pq = _primes(p_priors)
    qs = _primes(q_values)
    if not qs or len(qs) > 6:
        raise ValueError("one to six toy q values required")
    if any(not x/2 < p <= x for p in pq) or any(not x < q <= y for q in qs):
        raise ValueError("toy P/Q must use (X/2,X] and (X,Y]")
    priors = {}
    # Reuse the validated conditioning inputs, not its event summation.
    for p, prior in p_priors.items():
        conditional_law(prior, tuple(p*hi for hi in hs), (), ())
        priors[p] = {n: _rational(w, "prior mass") for n, w in prior.items()}
        if any(abs(n) > y for n in prior):
            raise ValueError("prior support escapes [-Y,Y]")
    eta = _rational(eta, "eta")
    delta = _rational(value_cutoff, "value_cutoff")
    cutoff = _rational(count_cutoff, "count_cutoff")
    if not 0 < eta < 1:
        raise ValueError("require 0<eta<1")
    markov_exception_budget(0, delta, cutoff)
    states = prod(ps)
    if states > 5000 or states*len(qs)*len(pq)*(
            len(shifts)+sum(map(len, priors.values())))*len(hs)*max(1, len(ps)) > 500_000:
        raise ValueError("bounded toy enumeration budget exceeded")
    sigma = sigma_toy(ps)
    base = sigma**len(hs)
    totals_all, totals_good, violations = [], [], 0
    max_conditioning_slack = Fraction(0)
    for residues in product(*(range(p) for p in ps)):
        # Direct all-residue oracle: build surviving atoms without product formula.
        def alive(n):
            return all(n % s != a for s, a in zip(ps, residues))
        atoms, mass = {}, {}
        for p, prior in priors.items():
            atoms[p] = {n: w for n, w in prior.items()
                        if all(alive(n+hi*p) for hi in hs)}
            mass[p] = sum(atoms[p].values(), Fraction(0))
        good = {p for p in pq if abs(mass[p]/base-1) <= eta}
        total_all = total_good = Fraction(0)
        bad_count = 0
        for q in qs:
            if not alive(q):
                continue  # q's survival is essential for the extra sigma.
            all_q = good_q = conditioned_q = Fraction(0)
            for p in pq:
                weight = sum((atoms[p].get(q-h*p, Fraction(0)) for h in shifts),
                             Fraction(0))
                all_q += weight/base
                if p in good:
                    good_q += weight/base
                    conditioned_q += weight/mass[p]
            if conditioned_q > good_q/(1-eta):
                raise AssertionError("conditional denominator inequality failed")
            max_conditioning_slack = max(max_conditioning_slack,
                                        good_q/(1-eta)-conditioned_q)
            total_all += all_q
            total_good += good_q
            bad_count += good_q > delta
        if total_good > total_all or bad_count*delta > total_good:
            raise AssertionError("positivity or exception-count inequality failed")
        totals_all.append(total_all)
        totals_good.append(total_good)
        violations += bad_count > cutoff
    direct_all = sum(totals_all, Fraction(0))/states
    direct_good = sum(totals_good, Fraction(0))/states

    # Product oracle follows the expanded (q,p,h) identity, no residue enumeration.
    factored = missing_q = Fraction(0)
    mass_by_h = {h: Fraction(0) for h in shifts}
    max_ratio = Fraction(0)
    for q in qs:
        for p in pq:
            for h in shifts:
                w = priors[p].get(q-h*p, Fraction(0))
                if not w:
                    continue
                points = off_tuple_points(q, p, h, hs)
                joint = survival_probability(points, ps)
                factored += w*joint/base
                missing_q += w*survival_probability(points[1:], ps)/base
                mass_by_h[h] += w
                max_ratio = max(max_ratio, joint/(sigma*base))
    envelope = max_ratio*sigma*sum(mass_by_h.values(), Fraction(0))
    per_h_envelope = max_ratio*sigma*len(shifts)*max(mass_by_h.values(), default=0)
    actual_failure = Fraction(violations, states)
    markov = markov_exception_budget(direct_good, delta, cutoff)
    if actual_failure > markov or factored > envelope or envelope > per_h_envelope:
        raise AssertionError("exact expectation/Markov envelope failed")
    return {
        "states": states, "h_values": shifts, "h_count": len(shifts),
        "direct_all_p_expectation": direct_all,
        "product_oracle_expectation": factored,
        "direct_good_p_expectation": direct_good,
        "incorrect_missing_q_expectation": missing_q,
        "all_p_correlation_envelope": envelope,
        "uniform_per_h_envelope": per_h_envelope,
        "actual_exception_failure": actual_failure,
        "markov_failure_upper": markov,
        "maximum_conditioning_slack": max_conditioning_slack,
        "actual_prime_experiment_performed": False,
        "analytic_cutoff_verified_by_toy": False,
    }


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(document, *, check_hashes=True):
    """Scope/provenance guard, not a proof assistant."""
    issues = []
    if document.get("id") != "H1b-COR2" or document.get("schema_version") != "1.0.0":
        issues.append("unexpected contract identity")
    if document.get("newly_closed_actual_work") != ["DEP-R05"]:
        issues.append("unsupported new closure")
    if document.get("closed_actual_work") != list(CLOSED_IDS):
        issues.append("closure inventory mismatch")
    if document.get("remaining_open_work") != list(REMAINING_IDS):
        issues.append("remaining work mismatch")
    if document.get("scope") != SCOPE or document.get("constants") != CONSTANTS:
        issues.append("scope or constant package mismatch")
    if document.get("broad_root_status") != {
        "SIV-07": "HARD_BLOCKER", "SIV-08": "HARD_BLOCKER",
        "SIV-09": "HARD_BLOCKER", "X_CERT": "OPEN",
    }:
        issues.append("unsupported root promotion")
    if document.get("next_gate") != "H1b-COR3 / DEP-R03 then DEP-R06":
        issues.append("next gate mismatch")
    if document.get("historical_ledger_preserved") is not True:
        issues.append("historical status must be preserved")
    pins = document.get("source_pins", [])
    expected_ids = {"FMT", "RS1962", "SIGMA35", "NORM47", "COR1_49", "COR1_CONTRACT"}
    if len(pins) != len(expected_ids) or {p.get("id") for p in pins} != expected_ids:
        issues.append("source inventory mismatch")
    for pin in pins:
        path = (ROOT / pin["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            issues.append("source absent or escapes root")
        elif check_hashes and sha256(path.read_bytes()).hexdigest() != pin["sha256"]:
            issues.append(f"hash mismatch: {pin['id']}")
    if document.get("pdf_reading") != [
        {"source": "FMT", "page": 14, "page_type": "NATIVE_TEXT",
         "text_primary": True, "original_page_crosschecked": True,
         "new_ocr_performed": False},
        {"source": "RS1962", "page": 6, "printed_page": 69,
         "page_type": "SCAN_WITH_TEXT_LAYER",
         "original_page_crosschecked": True, "new_ocr_performed": False},
    ]:
        issues.append("PDF reading classification mismatch")
    return issues
