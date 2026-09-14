"""Fail-closed tests for the DEP-R09 Maier/FMT selection audit."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

from source.dep_r09_maier_shift_selection import (
    build_diagnostic,
    markov_bad_count_upper,
    union_bound_certifies_candidate,
    union_bound_remaining_lower_bound,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Maier_shift_selection_v1.json"
)


class DepR09MaierShiftSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_union_bound_has_exact_finite_slack(self):
        self.assertEqual(union_bound_remaining_lower_bound(10, [2, 3, 1]), 4)
        self.assertTrue(union_bound_certifies_candidate(10, [2, 3, 4]))
        self.assertFalse(union_bound_certifies_candidate(10, [2, 3, 5]))
        self.assertEqual(union_bound_remaining_lower_bound(3, [9]), 0)

    def test_singleton_family_exposes_the_quantifier_obstruction(self):
        self.assertTrue(union_bound_certifies_candidate(1, [0, 0, 0]))
        self.assertFalse(union_bound_certifies_candidate(1, [1, 0, 0]))

    def test_markov_count_is_exact_rational_arithmetic(self):
        self.assertEqual(markov_bad_count_upper(Fraction(17, 3), Fraction(2, 3)), 8)
        self.assertEqual(markov_bad_count_upper(Fraction(1, 10), Fraction(1, 3)), 0)

    def test_diagnostic_and_machine_ledger_fail_closed(self):
        diagnostic = build_diagnostic()
        saved = self.ledger["exact_finite_diagnostic"]
        for field, value in diagnostic.__dict__.items():
            self.assertEqual(saved[field], value, field)
        self.assertEqual(diagnostic.classical_fixed_partition_crt_residue_count, 1)
        self.assertFalse(diagnostic.classical_fixed_partition_has_free_y_average)
        self.assertTrue(diagnostic.sono_fmt_source_uses_randomized_sieve_vectors)
        self.assertFalse(diagnostic.numerical_mass_of_jointly_good_vectors_certified)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_source_hashes_are_pinned(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("locator")
            expected = source.get("sha256")
            if locator is None:
                continue
            path = REPO_ROOT / locator
            self.assertTrue(path.is_file(), source["key"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_machine_ledger_preserves_route_split(self):
        routes = self.ledger["route_classification"]
        self.assertEqual(routes["classical_maier_fixed_partition"], "SINGLETON_CRT_SHIFT")
        self.assertEqual(
            routes["uniform_correlation_route"],
            "LOGICALLY_SUFFICIENT_WITHOUT_SELECTION_BUT_ANALYTIC_SOURCE_OPEN",
        )
        self.assertEqual(
            routes["average_correlation_route"],
            "REQUIRES_QUANTIFIED_JOINT_GOOD_MASS_OVER_SONO_FMT_CONSTRUCTION_VECTORS",
        )

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            union_bound_remaining_lower_bound(0, [])
        with self.assertRaises(ValueError):
            union_bound_remaining_lower_bound(1, [-1])
        with self.assertRaises(TypeError):
            union_bound_remaining_lower_bound(True, [])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            markov_bad_count_upper(1, Fraction(1, 2))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            markov_bad_count_upper(Fraction(1), Fraction(0))


if __name__ == "__main__":
    unittest.main()
