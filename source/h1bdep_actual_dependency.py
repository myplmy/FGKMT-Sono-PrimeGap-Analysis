"""Read-only H1b-DEP contract checks and bounded exact fixtures.

Not a proof assistant, threshold calculator, PDF semantic verifier, or actual
prime-data experiment. All-parameter proofs are in theory 48. Toy generation
has hard limits so the actual k>=10**200 construction cannot be requested here.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bDEP_actual_dependency_v1.json"
OPEN_IDS = tuple(f"DEP-R{i:02d}" for i in range(1, 13))
REQUIRED_EDGES = {
    "PROFILE": (), "HYP_ID": (),
    "P91": ("PROFILE",), "P92": ("PROFILE", "HYP_ID"),
    "P94": ("PROFILE",), "POINT": ("PROFILE",),
    "NORM": ("P91", "P92", "P94", "POINT"),
    "INTERFACE": ("NORM",), "ACTUAL_INPUTS": ("NORM", "INTERFACE"),
    "CODEGREE_BRIDGE": ("INTERFACE",), "P95": ("PROFILE",),
    "GENERAL_P61": ("P95",),
    "DEP-R01": ("INTERFACE",),
    "DEP-R02": ("ACTUAL_INPUTS", "DEP-R01"),
    "DEP-R03": ("DEP-R01",),
    "DEP-R04": ("ACTUAL_INPUTS", "DEP-R01", "DEP-R02"),
    "DEP-R05": ("ACTUAL_INPUTS", "DEP-R01", "DEP-R02", "DEP-R04"),
    "DEP-R06": ("ACTUAL_INPUTS", "DEP-R01", "DEP-R02", "DEP-R04", "DEP-R05"),
    "DEP-R07": ("CODEGREE_BRIDGE", "DEP-R02", "DEP-R03", "DEP-R06"),
    "DEP-R08": ("DEP-R03", "DEP-R05", "DEP-R07"),
    "DEP-R09": (), "DEP-R10": (),
    "DEP-R11": ("NORM", "DEP-R08", "DEP-R09", "DEP-R10"),
    "DEP-R12": ("DEP-R11",), "X_CERT": ("DEP-R12",),
}


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def ancestors(nodes: list[dict], target: str) -> set[str]:
    """Dependencies of target; reject dangling edges, duplicate IDs and cycles."""
    table = {row["id"]: row for row in nodes}
    if len(table) != len(nodes) or target not in table:
        raise ValueError("duplicate node or unknown target")
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        if node not in table:
            raise ValueError(f"unknown dependency {node}")
        if node in active:
            raise ValueError(f"cycle at {node}")
        if node in done:
            return
        active.add(node)
        for child in table[node]["depends_on"]:
            visit(child)
        active.remove(node)
        done.add(node)

    visit(target)
    return done - {target}


def validate_contract(document: dict, root: Path = ROOT, *, check_hashes: bool = True) -> list[str]:
    """Fail closed against this revision's scoped graph; returns issues, not a theorem."""
    issues: list[str] = []
    try:
        if document["schema_version"] != "1.0.0":
            issues.append("unsupported schema")
        nodes = document["nodes"]
        table = {row["id"]: row for row in nodes}
        if len(table) != len(nodes) or set(table) != set(REQUIRED_EDGES):
            issues.append("node inventory mismatch")
        for row in nodes:
            node_id = row["id"]
            deps = row["depends_on"]
            if len(deps) != len(set(deps)) or set(deps) != set(REQUIRED_EDGES.get(node_id, ())):
                issues.append(f"dependency mismatch: {node_id}")
            ancestors(nodes, node_id)
            expected_status = (
                "OPEN" if node_id in (*OPEN_IDS, "X_CERT") else
                "GENERAL_OPEN" if node_id in ("P95", "GENERAL_P61") else
                "CONDITIONAL_INTERFACE_PROVED" if node_id == "CODEGREE_BRIDGE" else
                "PROJECT_EXPLICIT"
            )
            expected_scope = (
                "root" if node_id == "X_CERT" else
                "actual_remaining" if node_id in OPEN_IDS else
                "general" if node_id in ("P95", "GENERAL_P61") else
                "conditional" if node_id == "CODEGREE_BRIDGE" else "actual"
            )
            if row["status"] != expected_status or row["scope"] != expected_scope:
                issues.append(f"status/scope promotion: {node_id}")
            if not row["claim"] or not row["locator"]:
                issues.append(f"missing evidence locator: {node_id}")
        actual = ancestors(nodes, "ACTUAL_INPUTS")
        final = ancestors(nodes, "X_CERT")
        if "P95" in actual or "P95" in final or "GENERAL_P61" in final:
            issues.append("general branch leaked into actual route")
        if not set(OPEN_IDS) <= final or "P94" not in actual:
            issues.append("required actual input or remaining obligation removed")
        scope = document["scope"]
        expected = {
            "weight": "maynard_w_filtered", "u_quantifier": "fixed_X_and_source_B",
            "boundary_mode": "end", "logs": "iterated_natural",
            "child_scale": "auxiliary_sieve_X_not_final_gap_Z",
            "child_cutoff": "X>=2*exp(10^1000)", "actual_h_constant": 4,
        }
        for key, value in expected.items():
            if scope[key] != value:
                issues.append(f"scope mismatch: {key}")
        for key in ("actual_prime_experiment_performed", "threshold_calculator_ready",
                    "x_cert_ready", "full_general_P61_certified",
                    "independently_formally_verified"):
            if scope[key] is not False:
                issues.append(f"unauthorized promotion: {key}")
        work = document["remaining_work"]
        if len(work) != 12 or {r["id"] for r in work} != set(OPEN_IDS):
            issues.append("remaining work inventory mismatch")
        if {r["group"] for r in work} != {
            "probability", "cover", "PAP", "UB", "final_budget", "transfer"
        }:
            issues.append("remaining work group mismatch")
        audit = document["transitive_audit"]
        if audit["p95_required_by_actual_inputs"] is not False:
            issues.append("P95 audit mismatch")
        if audit["tex_is_final_publication_verified"] is not False:
            issues.append("unverified TeX promoted to final publication")
        if document["historical_counts_are_not_completion_percentage"] is not True:
            issues.append("historical counts misrepresented")
        if sum(document["historical_T1_counts"].values()) != 66:
            issues.append("historical T1 count mismatch")
        pins = document["source_pins"]
        if len(pins) != 11 or len({p["id"] for p in pins}) != 11:
            issues.append("source pin inventory mismatch")
        for pin in pins:
            if not re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]):
                issues.append(f"invalid source hash: {pin['id']}")
            path = (root / pin["path"]).resolve()
            if not path.is_relative_to(root.resolve()):
                issues.append(f"source outside root: {pin['id']}")
            elif check_hashes:
                if not path.is_file():
                    issues.append(f"source missing: {pin['id']}")
                elif hashlib.sha256(path.read_bytes()).hexdigest() != pin["sha256"]:
                    issues.append(f"source hash mismatch: {pin['id']}")
        reading = document["pdf_reading"]
        if {r["source"] for r in reading} != {"FGKMT", "FMT", "Maynard", "Sono", "RS1962"}:
            issues.append("PDF reading inventory mismatch")
        for row in reading:
            typ = "SCAN_WITH_TEXT_LAYER" if row["source"] == "RS1962" else "NATIVE_TEXT"
            if (row["page_type"] != typ or row["new_ocr_performed"] is not False
                    or row["classification_scope"] != "inspected_page_only"):
                issues.append(f"PDF classification mismatch: {row['source']}")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        issues.append(f"malformed contract: {type(exc).__name__}: {exc}")
    return issues


def tex_prerequisite_references(text: str) -> set[str]:
    """Search helper only: this cannot establish the published dependency graph."""
    start = text.index(r"\label{lmm:SingularSeries}")
    stop = text.index(r"\begin{prpstn}\label{prpstn:S4}", start)
    return set(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text[start:stop]))


def _bounded_int(value: int, name: str, low: int, high: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{name} must be an exact integer in [{low},{high}] (toy only)")


def toy_primes(limit: int) -> tuple[int, ...]:
    _bounded_int(limit, "limit", 2, 10000)
    return tuple(n for n in range(2, limit + 1)
                 if all(n % d for d in range(2, math.isqrt(n) + 1)))


def toy_admissible_tuple(k: int) -> tuple[int, ...]:
    _bounded_int(k, "k", 1, 128)
    primes = toy_primes(10000)
    return tuple(p for p in primes if p > k)[:k]


def toy_is_admissible(values: tuple[int, ...]) -> bool:
    if not values or len(values) > 128 or len(values) != len(set(values)):
        return False
    for value in values:
        _bounded_int(value, "tuple value", 1, 10000)
    # For primes > len(values), fewer forbidden residues than residue classes.
    return all(len({v % p for v in values}) < p
               for p in toy_primes(max(2, len(values))))


def toy_pair_divisors(x: int, q1: int, q2: int) -> tuple[int, ...]:
    _bounded_int(x, "x", 2, 10000)
    _bounded_int(q1, "q1", 1, 10000)
    _bounded_int(q2, "q2", 1, 10000)
    if q1 == q2:
        raise ValueError("distinct points required")
    return tuple(p for p in toy_primes(x) if 2*p > x and (q1-q2) % p == 0)


def toy_uniform_residue_codegree(x: int, y: int, q1: int, q2: int) -> tuple[Fraction, Fraction]:
    """Exact finite fixture: independently uniform residue per p, not actual weights."""
    _bounded_int(x, "x", 2, 100)
    _bounded_int(y, "y", x+1, 10000)
    if 4*y >= x*x or not x < q1 <= y or not x < q2 <= y:
        raise ValueError("require x<q1,q2<=y<x^2/4")
    divisors = toy_pair_divisors(x, q1, q2)
    primes = tuple(p for p in toy_primes(x) if 2*p > x)
    joint = sum((Fraction(1, p) for p in divisors), Fraction(0))
    marginal = max(Fraction(1, p) for p in primes)
    return joint, marginal
