"""Contract, negative regressions and bounded independent geometry fixtures."""
from __future__ import annotations

import copy
import json
import unittest
from fractions import Fraction

from source.h1bdep_actual_dependency import (
    ROOT, OPEN_IDS, ancestors, load_contract, tex_prerequisite_references,
    toy_admissible_tuple, toy_is_admissible, toy_pair_divisors, toy_primes,
    toy_uniform_residue_codegree, validate_contract,
)


class ActualDependencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = load_contract()

    def mutated(self):
        return copy.deepcopy(self.document)

    def test_saved_contract_and_eleven_source_hashes(self):
        self.assertEqual(validate_contract(self.document), [])

    def test_actual_inputs_keep_p94_without_p95(self):
        deps = ancestors(self.document["nodes"], "ACTUAL_INPUTS")
        self.assertTrue({"P91", "P92", "P94", "HYP_ID", "PROFILE"} <= deps)
        self.assertNotIn("P95", deps)
        self.assertEqual(len(self.document["direct_calls"]), 5)

    def test_twelve_open_packages_are_final_ancestors(self):
        self.assertTrue(set(OPEN_IDS) <= ancestors(self.document["nodes"], "X_CERT"))
        self.assertEqual(len({r["group"] for r in self.document["remaining_work"]}), 6)

    def test_reject_p95_insertion_and_p94_deletion(self):
        for remove, add in ((None, "P95"), ("P94", None)):
            doc = self.mutated()
            norm = next(r for r in doc["nodes"] if r["id"] == "NORM")
            if remove:
                norm["depends_on"].remove(remove)
            if add:
                norm["depends_on"].append(add)
            self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_reject_cycle_and_missing_dependency(self):
        for dep in ("X_CERT", "MISSING"):
            doc = self.mutated()
            doc["nodes"][0]["depends_on"] = [dep]
            self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_reject_duplicate_node(self):
        doc = self.mutated()
        doc["nodes"].append(copy.deepcopy(doc["nodes"][0]))
        self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_reject_open_or_conditional_promotion(self):
        for node_id in (*OPEN_IDS, "X_CERT", "CODEGREE_BRIDGE", "P95"):
            with self.subTest(node=node_id):
                doc = self.mutated()
                next(r for r in doc["nodes"] if r["id"] == node_id)["status"] = "PROJECT_EXPLICIT"
                self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_reject_silent_scope_change(self):
        for key, value in (("weight", "unfiltered"), ("u_quantifier", "k_only"),
                           ("child_scale", "final_Z"), ("boundary_mode", "start"),
                           ("logs", "base_2_3_4"), ("actual_h_constant", 1)):
            doc = self.mutated()
            doc["scope"][key] = value
            self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_reject_false_global_certification(self):
        for key in ("x_cert_ready", "threshold_calculator_ready", "full_general_P61_certified",
                    "actual_prime_experiment_performed", "independently_formally_verified"):
            doc = self.mutated()
            doc["scope"][key] = True
            self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_reject_source_hash_mutation_and_escape(self):
        doc = self.mutated()
        doc["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(any("hash mismatch" in i for i in validate_contract(doc)))
        doc["source_pins"][0]["path"] = "../outside.pdf"
        self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_tex_search_is_version_limited_and_not_p95(self):
        pin = next(p for p in self.document["source_pins"] if p["id"] == "MAYNARD_TEX")
        tex = (ROOT / pin["path"]).read_text(encoding="utf-8")
        refs = tex_prerequisite_references(tex)
        self.assertNotIn("prpstn:S4", refs)
        self.assertIn(r"\label{eq:S4Bound2}", tex)
        self.assertNotIn("eq:S4Bound2", refs)  # definition, not a cited proposition
        self.assertFalse(self.document["transitive_audit"]["tex_is_final_publication_verified"])

    def test_pdf_scan_is_not_native_because_text_exists(self):
        rows = {r["source"]: r for r in self.document["pdf_reading"]}
        scan = rows["RS1962"]
        self.assertGreater(scan["text_chars"], 0)
        self.assertIn(3, scan["text_render_modes"])
        self.assertTrue(scan["image_xobjects"])
        self.assertEqual(scan["page_type"], "SCAN_WITH_TEXT_LAYER")
        doc = self.mutated()
        next(r for r in doc["pdf_reading"] if r["source"] == "RS1962")["page_type"] = "NATIVE_TEXT"
        self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_historical_t1_counts_are_preserved_with_named_successor_deltas(self):
        from collections import Counter
        path = ROOT / "docs/method/theory/data/Sono_FMT_T1_proof_obligations_v1.json"
        t1 = json.loads(path.read_text(encoding="utf-8"))
        counts = dict(Counter(r["status"] for r in t1["obligations"]))
        # DEP is immutable history.  Later packages must be represented by their
        # exact row transitions rather than silently rewriting that snapshot.
        historical = dict(self.document["historical_T1_counts"])
        self.assertEqual(historical["EXPLICIT"], 7)
        self.assertEqual(historical["HARD_BLOCKER"], 16)

        # COV1a: COV-06 HARD_BLOCKER -> EXPLICIT.
        expected = dict(historical)
        expected["EXPLICIT"] += 1
        expected["HARD_BLOCKER"] -= 1

        # COV2: COV-02/03 RATE_MISSING -> EXPLICIT;
        # COV-09 PARTIAL -> EXPLICIT; COV-08/11 HARD_BLOCKER -> PARTIAL.
        expected["EXPLICIT"] += 3
        expected["RATE_MISSING"] -= 2
        expected["PARTIAL"] += 1
        expected["HARD_BLOCKER"] -= 2
        self.assertEqual(counts, expected)
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["COV-06"]["status"], "EXPLICIT")
        self.assertIn("C0=100", rows["COV-06"]["explicit_bound"])
        for row_id in ("COV-02", "COV-03", "COV-09"):
            self.assertEqual(rows[row_id]["status"], "EXPLICIT")
        for row_id in ("COV-08", "COV-11"):
            self.assertEqual(rows[row_id]["status"], "PARTIAL")
        self.assertTrue(self.document["historical_counts_are_not_completion_percentage"])


class FiniteInterfaceToyTests(unittest.TestCase):
    def test_first_primes_give_bounded_admissible_tuple(self):
        for k in (36, 37, 64, 128):
            values = toy_admissible_tuple(k)
            self.assertEqual(len(values), k)
            self.assertGreater(min(values), k)
            self.assertLess(max(values), k*k)
            self.assertTrue(toy_is_admissible(values))

    def test_nonadmissible_and_duplicate_fixtures(self):
        self.assertFalse(toy_is_admissible((1, 2)))
        self.assertFalse(toy_is_admissible((3, 3)))

    def test_toy_cannot_allocate_actual_dimension(self):
        for value in (10**200, 129, 1.5, True):
            with self.assertRaises(ValueError):
                toy_admissible_tuple(value)
        with self.assertRaises(ValueError):
            toy_primes(10**20)

    def test_exp_five_endpoint_by_exact_positive_terms(self):
        from math import factorial
        partial = sum((Fraction(5**j, factorial(j)) for j in range(6)), Fraction(0))
        self.assertGreater(partial, 72)

    def test_codegree_geometry_exhaustive_toy_and_direct_enumeration(self):
        x, y = 20, 80
        primes = (11, 13, 17, 19)
        for q1 in range(x+1, y+1):
            for q2 in range(q1+1, y+1):
                joint, marginal = toy_uniform_residue_codegree(x, y, q1, q2)
                direct = sum((Fraction(sum(q1 % p == a and q2 % p == a
                                          for a in range(p)), p)
                              for p in primes), Fraction(0))
                self.assertEqual(joint, direct)
                self.assertLessEqual(joint, marginal)
                self.assertLessEqual(len(toy_pair_divisors(x, q1, q2)), 1)

    def test_wide_range_and_repeated_points_must_not_use_bridge(self):
        self.assertEqual(toy_pair_divisors(20, 101, 244), (11, 13))
        with self.assertRaises(ValueError):
            toy_uniform_residue_codegree(20, 245, 101, 244)
        with self.assertRaises(ValueError):
            toy_uniform_residue_codegree(20, 80, 21, 21)

    def test_boundary_product_cutoff_is_strict(self):
        with self.assertRaises(ValueError):
            toy_uniform_residue_codegree(20, 100, 21, 22)


if __name__ == "__main__":
    unittest.main()
