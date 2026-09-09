"""Theory 49: bounded exact residue models and log-scale proof diagnostics.

No prime-data experiment, threshold calculator, formal verifier, or certification
of the inherited sieve construction. See the analytic all-parameter proof.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import isqrt, prod
from pathlib import Path

from source.h1bp92a_identity_prime_moment import exact_dimension_bin

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOR1_finite_correlation_v1.json"
CLOSED_IDS = ("DEP-R01", "DEP-R02", "DEP-R04")
REMAINING_IDS = tuple(f"DEP-R{i:02}" for i in range(1, 13)
                      if f"DEP-R{i:02}" not in CLOSED_IDS)
MIN_K = 10**200


def _integer(n, name, minimum=None, maximum=None):
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(f"{name} must be an exact integer")
    if minimum is not None and n < minimum or maximum is not None and n > maximum:
        raise ValueError(f"{name} is outside its bounded domain")
    return n


def _rational(n, name):
    if isinstance(n, bool) or not isinstance(n, (int, str, Fraction)):
        raise ValueError(f"{name} must be exact; floats are not accepted")
    try:
        return Fraction(n)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be finite rational") from exc


def _primes(primes):
    primes = tuple(primes)
    if len(primes) > 8 or len(primes) != len(set(primes)):
        raise ValueError("at most 8 distinct toy prime moduli")
    for p in primes:
        _integer(p, "toy prime", 2, 1000)
        if any(p % d == 0 for d in range(2, isqrt(p)+1)):
            raise ValueError("composite modulus is not allowed")
    return primes


def _points(points):
    points = tuple(points)
    if not 1 <= len(points) <= 16:
        raise ValueError("toy point count must be 1..16")
    for n in points:
        _integer(n, "point", -10**6, 10**6)
    return points


def sigma_toy(primes):
    """Exact finite prime product; not the huge actual S."""
    return prod((Fraction(p-1, p) for p in _primes(primes)), start=Fraction(1))


def survival_probability(points, primes, *, independent_uniform=True):
    """Exact probability in the explicitly independent uniform residue model.

    Repeated points are allowed as events; multiplicity is NOT independence.
    """
    if independent_uniform is not True:
        raise ValueError("the product identity needs independent uniform residues")
    ns, ps = _points(points), _primes(primes)
    return prod((Fraction(p-len({n % p for n in ns}), p) for p in ps),
                start=Fraction(1))


def enumerated_survival(points, primes):
    """Independent oracle: enumerate residue vectors, not the product formula."""
    ns, ps = _points(points), _primes(primes)
    count = prod(ps)
    if count > 50_000:
        raise ValueError("toy enumeration exceeds 50,000 residue vectors")
    survivors = sum(all(all(n % p != a for n in ns) for p, a in zip(ps, residues))
                    for residues in product(*(range(p) for p in ps)))
    return Fraction(survivors, count)


def correlation_log_envelope(points, primes):
    """Rational bounds A,B with -A <= log(P/sigma^t) <= B.

    If max(A,B)<=1/2, relative error is at most 2*max(A,B).
    This finite-S bound is a toy check of the proof, not a source cutoff test.
    """
    ns, ps = _points(points), _primes(primes)
    t = len(ns)
    if len(set(ns)) != t:
        raise ValueError("correlation theorem requires distinct integers")
    if any(p <= 2*t for p in ps):
        raise ValueError("require toy primes > 2*point count")
    baseline = sum((Fraction(t*t, p*p) for p in ps), Fraction(0))
    collision = sum((Fraction(t-len({n % p for n in ns}), p-t) for p in ps),
                    Fraction(0))
    return baseline, collision


def _prior(prior, shifts):
    if not isinstance(prior, dict) or not 1 <= len(prior) <= 32:
        raise ValueError("a bounded nonempty prior mapping is required")
    weights = {}
    for n, weight in prior.items():
        _integer(n, "prior support", -10000, 10000)
        w = _rational(weight, "prior mass")
        if w < 0:
            raise ValueError("prior mass must be nonnegative")
        weights[n] = w
    if sum(weights.values()) != 1:
        raise ValueError("prior mass must sum to exactly one")
    hs = _points(shifts)
    if len(hs) > 8 or len(set(hs)) != len(hs):
        raise ValueError("at most 8 distinct shifts")
    # Each concatenated pair then has at most 16 points.
    for n in weights:
        _points(n+h for h in hs)
    return weights, hs


def conditional_law(prior, shifts, primes, residues):
    """Returns survival mass D and exact conditioned law; zero D returns {}.

    Empty law is deliberately not replaced by a fake uniform/unconditioned law.
    The source's separate bad-p assignment n_p=0 is not this conditioning.
    """
    weights, hs = _prior(prior, shifts)
    ps, residues = _primes(primes), tuple(residues)
    if len(residues) != len(ps):
        raise ValueError("one residue per prime is required")
    for p, a in zip(ps, residues):
        _integer(a, "residue", 0, p-1)
    alive = {n: w for n, w in weights.items()
             if all(all((n+h) % p != a for h in hs) for p, a in zip(ps, residues))}
    mass = sum(alive.values(), Fraction(0))
    return mass, ({n: w/mass for n, w in alive.items()} if mass else {})


def conditioning_moments(prior, shifts, primes):
    """Direct vector enumeration vs independently computed two-copy moment."""
    weights, hs = _prior(prior, shifts)
    ps = _primes(primes)
    vectors = prod(ps)
    if vectors > 50_000:
        raise ValueError("toy enumeration exceeds 50,000 residue vectors")
    # Limit total work, not only number of moduli.
    if vectors*len(weights)*len(hs) > 500_000:
        raise ValueError("toy operation budget exceeded")
    mean = second = Fraction(0)
    for residues in product(*(range(p) for p in ps)):
        mass, _ = conditional_law(weights, hs, ps, residues)
        mean += mass/vectors
        second += mass*mass/vectors
    pair_second = collision_probability = Fraction(0)
    for n1, w1 in weights.items():
        left = tuple(n1+h for h in hs)
        for n2, w2 in weights.items():
            right = tuple(n2+h for h in hs)
            pair_second += w1*w2*survival_probability(left+right, ps)
            if set(left) & set(right):
                collision_probability += w1*w2
    base = sigma_toy(ps)**len(hs)
    return {
        "mean": mean, "second": second, "independent_pair_second": pair_second,
        "collision_probability": collision_probability,
        "collision_union_upper": len(hs)**2*max(weights.values()),
        "normalized_mean": mean/base, "normalized_second": second/base**2,
        "normalized_squared_deviation": second/base**2-2*mean/base+1,
    }


def finite_correlation_error(log_x):
    """Exact scalar envelope 2/a^17. This does not check a point set or prime S."""
    a = _rational(log_x, "log_x")
    if a < 2:
        raise ValueError("require log_x>=2")
    return 2/a**17


def good_p_failure_from_moments(mean_relative_error, collision_relative_error, eta):
    """Preserve mean != 1: E(U-1)^2 <= 3*eps+collision, then Markov."""
    eps = _rational(mean_relative_error, "mean_relative_error")
    collision = _rational(collision_relative_error, "collision_relative_error")
    eta = _rational(eta, "eta")
    if eps < 0 or collision < 0 or not 0 < eta < 1:
        raise ValueError("require eps,collision>=0 and 0<eta<1")
    squared = 3*eps+collision
    return squared, min(Fraction(1), squared/eta**2)


def actual_scalar_guards(*, k, log_outer_half=None):
    """O(1) exact comparisons at the inherited dimension, no exp(L) or k array.

    L lower-bounds a, so inverse-log errors at L are conservative upper bounds.
    Structural construction and the analytic real-variable arguments are assumed.
    """
    _integer(k, "k", MIN_K)
    L = exact_dimension_bin(k, k**5 if log_outer_half is None else log_outer_half)
    checks = {
        "large_log": L >= 1000,
        "distinct_double_dimension": 2*k <= L,
        "collision_k_squared": k*k <= L,
        "sigma_exponent": k**3 >= 600,
        "inherited_dimension_bin": k**5 <= L < (k+1)**5,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, ok in checks.items() if not ok])
    return {
        "checks": checks,
        "correlation_relative_upper": 2/L**17,
        "normalized_squared_error_upper": 7/L**17,
        "single_bad_p_upper": 7/L**11,
        "global_bad_p_upper": 7/L**8,
        "sigma_inverse_exponent": Fraction(1, 100),
        "conditional_atom_exponent": Fraction(37, 50),
        "residue_sparsity_exponent": Fraction(3, 5),
        "structural_inputs_assumed": True,
        "all_parameter_proof_location": "theory 49 sections 3-5",
        "x_cert_ready": False,
        "full_hypergraph_certified": False,
        "actual_prime_experiment_performed": False,
        "independent_formal_verification": False,
    }


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(document, *, check_hashes=True):
    """Guard provenance and scope; tests cannot prove an analytic theorem."""
    issues = []
    if document.get("id") != "H1b-COR1" or document.get("schema_version") != "1.0.0":
        issues.append("unexpected contract identity")
    if document.get("closed_actual_work") != list(CLOSED_IDS):
        issues.append("unsupported actual-child promotion")
    if document.get("remaining_open_work") != list(REMAINING_IDS):
        issues.append("remaining work mismatch")
    if document.get("broad_root_status") != {
        "SIV-07": "HARD_BLOCKER", "SIV-08": "HARD_BLOCKER",
        "SIV-09": "HARD_BLOCKER", "X_CERT": "OPEN",
    }:
        issues.append("unsupported broad or root promotion")
    expected_scope = {
        "boundary_mode": "end", "logs": "iterated_natural",
        "weight": "maynard_w_filtered", "u_quantifier": "fixed_X_and_source_B",
        "child_cutoff": "X>=2*exp(10^1000)",
        "distinct_correlation_only": True, "collision_cost_preserved": True,
        "sigma_lower_direction": "P(z)_lower/P(v)_upper",
        "small_codegree_actual_closed": True, "full_hypergraph_certified": False,
        "x_cert_ready": False, "threshold_calculator_ready": False,
        "actual_prime_experiment_performed": False,
        "independently_formally_verified": False,
    }
    if document.get("scope") != expected_scope:
        issues.append("scope or mathematical invariant mismatch")
    if document.get("constants") != {
        "correlation_relative": "2/a^17<=1/a^16",
        "sigma_inverse_power": "1/100", "conditional_atom": "2*X^(-37/50)",
        "residue_sparsity": "X^(-3/5)", "second_moment_error": "7/a^17",
        "single_bad_p": "7/a^11", "global_bad_p": "7/a^8",
    }:
        issues.append("constant package mismatch")
    if document.get("next_gate") != "H1b-COR2 / DEP-R05":
        issues.append("next gate mismatch")
    pins = document.get("source_pins", [])
    expected_ids = {"FGKMT", "FMT", "RS1962", "SIGMA35", "NORM47", "DEP48", "DEP_CONTRACT"}
    if len(pins) != len(expected_ids) or {p.get("id") for p in pins} != expected_ids:
        issues.append("source pin inventory mismatch")
    for pin in pins:
        path = (ROOT / pin["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            issues.append("source path absent or escapes root")
        elif check_hashes and sha256(path.read_bytes()).hexdigest() != pin["sha256"]:
            issues.append(f"hash mismatch: {pin['id']}")
    pages = document.get("pdf_reading", [])
    page_types = {p["source"]: p["page_type"] for p in pages}
    if page_types != {"FGKMT": "NATIVE_TEXT", "FMT": "NATIVE_TEXT",
                      "RS1962": "SCAN_WITH_TEXT_LAYER"}:
        issues.append("PDF page classification mismatch")
    if any(p.get("new_ocr_performed") is not False for p in pages):
        issues.append("new OCR not performed")
    return issues
