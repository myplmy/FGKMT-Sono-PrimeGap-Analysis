"""Theories 51/52: bounded exact toys, not a prime sweep or formal proof.

Large-parameter statements are proved analytically in the documents. Tiny
enumerations below check identities, collisions and conditioning independently.
They do not satisfy or certify the actual enormous sieve cutoff.
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
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOR3_local_main_moments_v1.json"
CLOSED_IDS = tuple(f"DEP-R{i:02}" for i in range(1, 7))
REMAINING_IDS = tuple(f"DEP-R{i:02}" for i in range(7, 13))
SCOPE = {
    "boundary_mode": "end", "logs": "iterated_natural",
    "weight": "maynard_w_filtered", "u_quantifier": "fixed_X_and_source_B",
    "child_cutoff": "X>=2*exp(10^1000)",
    "finite_family_predeclared": True, "arbitrarily_narrow_intervals": False,
    "q_survival_preserved": True, "same_p_all_index_pairs_preserved": True,
    "conditioning_denominator_preserved": True,
    "source_sigma_b_minus_10_recovered": False,
    "full_hypergraph_certified": False, "global_union_budget_closed": False,
    "x_cert_ready": False, "threshold_calculator_ready": False,
    "actual_prime_experiment_performed": False,
    "independently_formally_verified": False,
}
CONSTANTS = {
    "c_aux": "1/(153600*ln(5))", "c_sono": "2e-17",
    "raw_count_error_upper": "10^6*b*Y/a^2",
    "minimum_interval_width": "a^(-1/4)",
    "finite_family_failure_upper": "min(1,3*J*b^6/a^17)",
    "local_count_relative_error": "1/(100*b^2)",
    "sigma_y_relative_error": "1/(200*b^2)",
    "cross_p_distinct_point_count": "2*k-1",
    "same_p_diagonal_upper": "k*X^(-73/100)*A_q",
    "main_centered_second_upper": "sigma/b^18",
    "bad_p_mass_expectation_upper": "14/a^11",
    "main_failure_upper": "min(1,800*c_aux/b^10+112*k*b^4/a^11)",
    "conditioned_main_relative_error": "3/b^3",
    "full_degree_absolute_error": "1/b^2",
    "full_degree_exception_count": "floor(X/(a*b))",
    "full_degree_failure_upper": "min(1,1600*c_aux/b^5+800*c_aux/b^10+112*k*b^4/a^11)",
    "C_bounds": "(5/4)*ln(5)<C<400",
}
PDF_READING = [
    {"source": "FMT", "pages": [10, 13, 14, 15],
     "page_type": "NATIVE_TEXT", "text_primary": True,
     "original_page_crosschecked": True, "new_ocr_performed": False},
    {"source": "FGKMT", "pages": [27, 28], "printed_pages": [91, 92],
     "page_type": "NATIVE_TEXT", "text_primary": True,
     "original_page_crosschecked": True, "new_ocr_performed": False},
    {"source": "RS1962", "pages": [6, 7], "printed_pages": [69, 70],
     "page_type": "SCAN_WITH_TEXT_LAYER",
     "original_page_crosschecked": True, "new_ocr_performed": False},
]


def sigma_correction_enclosure(r):
    """Bounds including the possible removal of one prime factor."""
    r = _rational(r, "r")
    if not 0 <= r <= Fraction(1, 10):
        raise ValueError("require 0<=r<=1/10")
    return (1-r)/(1+r), (1+r)/(1-r)**2


def finite_family_union(per_interval_failure, family_size, *, predeclared=True):
    p = _rational(per_interval_failure, "failure")
    _integer(family_size, "family size", 1, 10**6)
    if not 0 <= p <= 1 or predeclared is not True:
        raise ValueError("a predeclared family and a probability bound are required")
    return min(Fraction(1), family_size*p)


def centered_moment_envelope(t, eps, diagonal_relative):
    """Keep (t-1)^2: upper second - 2*lower first + survival mass."""
    t, eps, d = (_rational(x, name) for x, name in (
        (t, "mean ratio"), (eps, "correlation error"), (diagonal_relative, "diagonal")))
    if t < 0 or not 0 <= eps <= 1 or d < 0:
        raise ValueError("require t,d>=0 and 0<=eps<=1")
    return (t-1)**2 + eps*(t*t+2*t) + d


def finite_scalar_budget(b=2000):
    """Rational endpoint diagnostics only; analytic a=exp(b) is NOT evaluated."""
    b = _rational(b, "loglog lower bound")
    if b < 2000 or b > 10**6:
        raise ValueError("bounded diagnostic requires 2000<=b<=10^6")
    r = 1/(800*b*b)
    lo, hi = sigma_correction_enclosure(r)
    count_error = 3/b**3 + 1/(200*b*b) + 3/(200*b**5)
    coefficient_ratio = Fraction(39, 40)*153600 / (
        144*5*2*Fraction(26, 25)*80)
    return {
        "exp_quarter_endpoint_integer_guard": 2**500 > 10**6*2000,
        "exp_endpoint_integer_guard": 2**2000 > 2000**20,
        "sigma_lo": lo, "sigma_hi": hi,
        "sigma_error_upper": 4*r,
        "count_error_composition": count_error,
        "count_error_target": 1/(100*b*b),
        "coefficient_factor_times_ln5": coefficient_ratio,
        "full_degree_error_upper": Fraction(1202)/b**3,
        "full_degree_error_target": 1/b**2,
        "analytic_and_structural_inputs_assumed": True,
        "x_cert_ready": False, "actual_prime_experiment_performed": False,
    }


def disjoint_grid(values, *, y, cells, lower_cutoff=0, excluded=None):
    """Exact half-open grid; bounded fixture only, not raw dataset conversion."""
    y, lo = _rational(y, "y"), _rational(lower_cutoff, "lower cutoff")
    _integer(cells, "cells", 1, 32)
    ns = tuple(values)
    if y <= 0 or not 0 <= lo <= y or len(ns) > 32 or len(set(ns)) != len(ns):
        raise ValueError("bounded distinct values and 0<=lower<=y required")
    for n in ns:
        _integer(n, "value", 1, 10**6)
    if excluded is not None:
        _integer(excluded, "excluded value", 1, 10**6)
    eligible = tuple(n for n in ns if lo < n <= y and n != excluded)
    return tuple(tuple(n for n in eligible if j*y/cells < n <= (j+1)*y/cells)
                 for j in range(cells))


def local_count_toy(*, q_values, intervals, primes, eta=Fraction(1, 2),
                    predeclared=True):
    """Direct residue enumeration vs ordered-pair product oracle.

    Intervals are (left,right,closed_left), with exact rational endpoints.
    No actual RS cutoff is asserted; epsilon is measured on this tiny fixture.
    """
    if predeclared is not True:
        raise ValueError("family must be fixed before looking at residue outcomes")
    qs, ps, intervals = _primes(q_values), _primes(primes), tuple(intervals)
    eta = _rational(eta, "eta")
    if not 0 < eta < 1 or not 1 <= len(intervals) <= 16:
        raise ValueError("bounded nonempty family and 0<eta<1 required")
    selected = []
    for left, right, closed_left in intervals:
        left, right = _rational(left, "left"), _rational(right, "right")
        if not left < right or type(closed_left) is not bool:
            raise ValueError("valid exact endpoints and boolean closed_left required")
        selected.append(tuple(q for q in qs if (
            left <= q <= right if closed_left else left < q <= right)))
    states = prod(ps)
    if states > 5000 or states*len(intervals)*max(1, len(qs))*max(1, len(ps)) > 500_000:
        raise ValueError("bounded toy work budget exceeded")
    sigma = sigma_toy(ps)
    means = [Fraction(0) for _ in intervals]
    seconds = means.copy()
    failures = [0]*len(intervals)
    family_bad = 0
    for residues in product(*(range(p) for p in ps)):
        any_bad = False
        for j, subset in enumerate(selected):
            n = sum(all(q % s != a for s, a in zip(ps, residues)) for q in subset)
            means[j] += Fraction(n, states)
            seconds[j] += Fraction(n*n, states)
            if abs(n-sigma*len(subset)) > eta*sigma*len(subset):
                failures[j] += 1
                any_bad = True
        family_bad += any_bad
    rows = []
    for j, subset in enumerate(selected):
        expected = sigma*len(subset)
        second_product = sum((survival_probability((q, r), ps)
                              for q in subset for r in subset), Fraction(0))
        pair_eps = max((abs(survival_probability((q, r), ps)/sigma**2-1)
                        for q in subset for r in subset if q != r), default=Fraction(0))
        variance = seconds[j]-means[j]**2
        envelope = expected + pair_eps*expected**2
        chebyshev = (min(Fraction(1), envelope/(eta*expected)**2)
                     if expected else Fraction(0))
        rows.append({
            "selected": subset, "mean": means[j], "exact_mean": expected,
            "second": seconds[j], "second_product": second_product,
            "variance": variance, "variance_envelope": envelope,
            "actual_failure": Fraction(failures[j], states),
            "chebyshev_upper": chebyshev,
        })
    return {
        "states": states, "rows": rows,
        "family_actual_failure": Fraction(family_bad, states),
        "family_union_upper": min(Fraction(1), sum(
            (r["chebyshev_upper"] for r in rows), Fraction(0))),
        "analytic_cutoff_verified_by_toy": False,
        "actual_prime_experiment_performed": False,
    }


def main_pair_points(q, p1, i1, p2, i2, offsets):
    """Check the prime/short-slope geometry; return both full tuples."""
    _integer(q, "q", -10**4, 10**4)
    ps = _primes({p1, p2})
    hs = tuple(offsets)
    if not 1 <= len(hs) <= 4 or len(set(hs)) != len(hs):
        raise ValueError("one to four distinct offsets required")
    for hi in hs:
        _integer(hi, "offset", 1, 100)
    _integer(i1, "i1", 0, len(hs)-1)
    _integer(i2, "i2", 0, len(hs)-1)
    if min(ps) <= max(hs)-min(hs):
        raise ValueError("prime must exceed all nonzero offset differences")
    left = tuple(q+(hj-hs[i1])*p1 for hj in hs)
    right = tuple(q+(hj-hs[i2])*p2 for hj in hs)
    if p1 != p2 and len(set(left+right)) != 2*len(hs)-1:
        raise AssertionError("cross-p distinctness theorem failed")
    return left, right


def main_degree_toy(*, p_priors, q_values, offsets, primes,
                    eta=Fraction(1, 2), reference_c=1, independent_uniform=True):
    """Exact degree replay, product moments and all same-p index pairs.

    reference_c is an arbitrary positive toy centering constant, not actual C.
    Small prior fixtures do not certify the analytic moment assumptions.
    """
    if independent_uniform is not True:
        raise ValueError("independent uniform residues required")
    if not isinstance(p_priors, dict) or not 1 <= len(p_priors) <= 4:
        raise ValueError("one to four prior mappings required")
    pp, qs, ps = _primes(p_priors), _primes(q_values), _primes(primes)
    hs = tuple(offsets)
    main_pair_points(0, pp[0], 0, pp[0], 0, hs)
    if not qs or any(q <= max(pp) for q in qs):
        raise ValueError("toy q must be prime and greater than all p")
    priors = {}
    for p, prior in p_priors.items():
        main_pair_points(0, p, 0, p, 0, hs)
        conditional_law(prior, tuple(hi*p for hi in hs), (), ())
        priors[p] = {n: _rational(w, "prior mass") for n, w in prior.items()}
    eta, ref = _rational(eta, "eta"), _rational(reference_c, "reference C")
    if not 0 < eta < 1 or ref <= 0:
        raise ValueError("0<eta<1 and positive reference C required")
    states = prod(ps)
    work = states*(sum(map(len, priors.values()))+len(qs)*len(pp))*len(hs)*max(1, len(ps))
    if states > 5000 or work > 500_000:
        raise ValueError("bounded toy work budget exceeded")
    sigma, base = sigma_toy(ps), sigma_toy(ps)**len(hs)
    mean = {q: Fraction(0) for q in qs}
    second, centered = mean.copy(), mean.copy()
    removed_total = upper_total = Fraction(0)
    bad_p_seen, zero_d_seen = False, False
    for residues in product(*(range(p) for p in ps)):
        def alive(n):
            return all(n % s != a for s, a in zip(ps, residues))
        atoms, mass = {}, {}
        for p, prior in priors.items():
            atoms[p] = {n: w for n, w in prior.items()
                        if all(alive(n+hi*p) for hi in hs)}
            mass[p] = sum(atoms[p].values(), Fraction(0))
        good = {p for p in pp if abs(mass[p]/base-1) <= eta}
        bad_p_seen |= len(good) != len(pp)
        zero_d_seen |= any(d == 0 for d in mass.values())
        removed = Fraction(0)
        for q in qs:
            all_q = good_q = conditional = Fraction(0)
            for p in pp:
                z = sum((atoms[p].get(q-hi*p, Fraction(0)) for hi in hs), Fraction(0))
                all_q += z/base
                if p in good:
                    good_q += z/base
                    conditional += z/mass[p]
            if not alive(q) and all_q:
                raise AssertionError("dead q cannot have a main term")
            if not good_q/(1+eta) <= conditional <= good_q/(1-eta):
                raise AssertionError("conditional denominator enclosure failed")
            removed += all_q-good_q
            mean[q] += all_q/states
            second[q] += all_q**2/states
            centered[q] += int(alive(q))*(all_q/ref-1)**2/states
        upper = len(hs)*sum((mass[p]/base for p in pp if p not in good), Fraction(0))
        if not 0 <= removed <= upper:
            raise AssertionError("bad-P mass injection bound failed")
        removed_total += removed/states
        upper_total += upper/states

    rows = []
    for q in qs:
        terms = [(p, i, priors[p].get(q-hi*p, Fraction(0)))
                 for p in pp for i, hi in enumerate(hs)]
        factored_first = factored_second = diagonal = Fraction(0)
        diagonal_without_survival = Fraction(0)
        for p, i, w in terms:
            left, _ = main_pair_points(q, p, i, p, i, hs)
            factored_first += w*survival_probability(left, ps)/base
            for p2, i2, w2 in terms:
                left, right = main_pair_points(q, p, i, p2, i2, hs)
                term = w*w2*survival_probability(left+right, ps)/base**2
                factored_second += term
                if p == p2:
                    diagonal += term
                    diagonal_without_survival += w*w2/base**2
        atom_mass = sum((w for _, _, w in terms), Fraction(0))
        atom_bound = len(hs)*max(max(v.values()) for v in priors.values())*atom_mass/base**2
        rows.append({
            "q": q, "mean": mean[q], "product_mean": factored_first,
            "second": second[q], "product_second": factored_second,
            "diagonal_second": diagonal,
            "incorrect_second_without_same_p": factored_second-diagonal,
            "diagonal_trivial_upper": diagonal_without_survival,
            "diagonal_atom_upper": atom_bound,
            "centered_direct": centered[q],
            "centered_from_moments": second[q]/ref**2-2*mean[q]/ref+sigma,
        })
    return {
        "states": states, "rows": rows, "bad_p_seen": bad_p_seen,
        "zero_conditioning_mass_seen": zero_d_seen,
        "removed_mass_expectation": removed_total,
        "injection_mass_upper": upper_total,
        "analytic_cutoff_verified_by_toy": False,
        "actual_prime_experiment_performed": False,
    }


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(doc, *, check_hashes=True):
    """Fail-closed provenance and scope guard, not a mathematical prover."""
    issues = []
    if doc.get("id") != "H1b-COR3" or doc.get("schema_version") != "1.0.0":
        issues.append("contract identity mismatch")
    if doc.get("newly_closed_actual_work") != ["DEP-R03", "DEP-R06"]:
        issues.append("unsupported new closure")
    if doc.get("closed_actual_work") != list(CLOSED_IDS):
        issues.append("closed work mismatch")
    if doc.get("remaining_open_work") != list(REMAINING_IDS):
        issues.append("remaining work mismatch")
    if doc.get("scope") != SCOPE or doc.get("constants") != CONSTANTS:
        issues.append("scope or constant package mismatch")
    if doc.get("pdf_reading") != PDF_READING:
        issues.append("PDF source reading mismatch")
    if doc.get("broad_root_status") != {
        "SIV-07": "HARD_BLOCKER", "SIV-08": "HARD_BLOCKER",
        "SIV-09": "HARD_BLOCKER", "X_CERT": "OPEN",
    }:
        issues.append("unsupported broad-root promotion")
    if doc.get("next_gate") != "H1b-COV1 / DEP-R07":
        issues.append("next gate mismatch")
    if doc.get("historical_ledger_preserved") is not True:
        issues.append("history must remain immutable")
    pins = doc.get("source_pins", [])
    ids = {"FMT", "FGKMT", "RS1962", "COEFF34", "SIGMA35", "NORM47",
           "COR1_49", "COR2_50", "COR2_CONTRACT", "PROOF51", "PROOF52"}
    if len(pins) != len(ids) or {p.get("id") for p in pins} != ids:
        issues.append("source inventory mismatch")
    for pin in pins:
        path = (ROOT / pin["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            issues.append("source absent or path escapes root")
        elif check_hashes and sha256(path.read_bytes()).hexdigest() != pin["sha256"]:
            issues.append(f"hash mismatch: {pin['id']}")
    return issues
