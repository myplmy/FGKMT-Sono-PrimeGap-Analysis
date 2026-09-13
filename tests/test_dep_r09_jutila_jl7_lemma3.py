"""Fail-closed checks for the Jutila JL7 Lemma 3 finite composition."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

from source.dep_r09_jutila_jl7_lemma3 import (
    LEMMA3_OUTER_COEFFICIENT,
    LEMMA3_PAIR_COEFFICIENT,
    absolute_h_sum,
    absolute_h_sum_local_product,
    actual_absolute_composition,
    all_integer_divisor_envelope,
    build_diagnostic,
    eligible_r_values,
    expected_reciprocal_h_identity,
    h_coefficients,
    is_squarefree,
    lemma3_source_product_bound,
    outer_rational_bound,
    outer_lemma3_weight,
    outer_weight_sum,
    pair_rational_bound,
    positive_divisors,
    reciprocal_divisor_weight,
    reciprocal_h_identity,
    reciprocal_square_partial_sum,
    source_product_composition_bound,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_Lemma3_v1.json"
)
PREDECESSOR_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_contour_v1.json"
)


class DepR09JutilaJL7Lemma3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR_PATH.read_text(encoding="utf-8"))

    def test_machine_ledger_is_fail_closed_and_advances_only_one_gate(self):
        self.assertTrue(self.predecessor["contour_multiplier_explicit"])
        self.assertFalse(self.predecessor["jutila_lemma3_multiplier_explicit"])
        self.assertTrue(self.ledger["contour_multiplier_explicit"])
        self.assertTrue(self.ledger["jutila_lemma3_multiplier_explicit"])
        for key in (
            "residue_well_spacing_multiplier_explicit",
            "terminal_density_closed",
            "averaged_primitive_density_closed",
            "pap_11_closed",
            "dep_r09_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(self.ledger[key], key)
        self.assertIn("JL7-RES", self.ledger["next_gate"])
        self.assertEqual(
            self.ledger["outer_sum_composition"]["calculator_safe_multiplier"], 3
        )

    def test_source_hashes_and_sizes_when_audit_copy_present(self):
        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["audit_copy_locator"]
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
                self.assertEqual(
                    hashlib.sha256(data).hexdigest(),
                    source["audit_copy_sha256"],
                    source["key"],
                )

    def test_exact_local_coefficients_cover_common_two(self):
        self.assertEqual(h_coefficients(2, 2), {1: 1})
        self.assertEqual(h_coefficients(2, 3), {1: 1, 2: -2, 3: -3, 6: 6})
        self.assertEqual(h_coefficients(6, 10), {1: 1, 3: -3, 5: -5, 15: 15})
        self.assertEqual(absolute_h_sum(2, 2), 1)
        self.assertEqual(absolute_h_sum(2, 3), 12)
        self.assertEqual(absolute_h_sum(6, 10), 24)

    def test_local_product_and_printed_bound_for_all_small_squarefree_pairs(self):
        squarefree = [n for n in range(1, 51) if is_squarefree(n)]
        for r in squarefree:
            for r_prime in squarefree:
                with self.subTest(r=r, r_prime=r_prime):
                    exact = absolute_h_sum(r, r_prime)
                    self.assertEqual(exact, absolute_h_sum_local_product(r, r_prime))
                    self.assertLessEqual(exact, lemma3_source_product_bound(r, r_prime))

    def test_reciprocal_identity_for_all_small_squarefree_pairs(self):
        squarefree = [n for n in range(1, 51) if is_squarefree(n)]
        for r in squarefree:
            for r_prime in squarefree:
                with self.subTest(r=r, r_prime=r_prime):
                    self.assertEqual(
                        reciprocal_h_identity(r, r_prime),
                        expected_reciprocal_h_identity(r, r_prime),
                    )

    def test_squarefree_outer_weight_is_reciprocal_divisor_sum(self):
        for r in range(1, 101):
            if is_squarefree(r):
                self.assertEqual(outer_lemma3_weight(r), reciprocal_divisor_weight(r))
        self.assertEqual(positive_divisors(60), (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60))

    def test_finite_divisor_double_counting_identity(self):
        for endpoint_k in (1, 2, 10, 50):
            direct = sum(
                (reciprocal_divisor_weight(n) for n in range(1, endpoint_k + 1)),
                Fraction(0, 1),
            )
            self.assertEqual(direct, all_integer_divisor_envelope(endpoint_k))
            self.assertLessEqual(
                all_integer_divisor_envelope(endpoint_k),
                endpoint_k * reciprocal_square_partial_sum(endpoint_k),
            )

    def test_basel_and_rational_outer_envelopes(self):
        self.assertEqual(LEMMA3_OUTER_COEFFICIENT, Fraction(5, 3))
        self.assertEqual(LEMMA3_PAIR_COEFFICIENT, Fraction(3, 1))
        for endpoint_k in (1, 2, 10, 100, 1000):
            partial = reciprocal_square_partial_sum(endpoint_k)
            self.assertLess(partial, Fraction(5, 3))
            self.assertEqual(outer_rational_bound(endpoint_k), Fraction(5 * endpoint_k, 3))
            self.assertEqual(pair_rational_bound(endpoint_k), 3 * endpoint_k * endpoint_k)

    def test_actual_composition_is_below_all_three_envelopes(self):
        for endpoint_k, modulus_q in ((1, 1), (10, 1), (20, 6), (30, 30)):
            with self.subTest(endpoint_k=endpoint_k, modulus_q=modulus_q):
                outer = outer_weight_sum(endpoint_k, modulus_q)
                divisor_envelope = all_integer_divisor_envelope(endpoint_k)
                actual = actual_absolute_composition(endpoint_k, modulus_q)
                source_bound = source_product_composition_bound(endpoint_k, modulus_q)
                self.assertLessEqual(outer, divisor_envelope)
                self.assertLess(outer, outer_rational_bound(endpoint_k))
                self.assertLessEqual(actual, source_bound)
                self.assertLess(source_bound, pair_rational_bound(endpoint_k))

    def test_diagnostic_reports_exact_checks_and_open_downstream(self):
        diagnostic = build_diagnostic(30, 30)
        self.assertEqual(diagnostic.eligible_r_count, len(eligible_r_values(30, 30)))
        self.assertTrue(diagnostic.reciprocal_identity_verified)
        self.assertTrue(diagnostic.local_absolute_product_verified)
        self.assertTrue(diagnostic.printed_source_product_bound_verified)
        self.assertTrue(diagnostic.outer_double_count_verified)
        self.assertTrue(diagnostic.reciprocal_square_bound_verified_numerically)
        self.assertTrue(diagnostic.pair_composition_verified)
        self.assertTrue(diagnostic.lemma3_actual_inputs_parameterized_explicit)
        self.assertFalse(diagnostic.residue_multiplier_explicit)
        self.assertFalse(diagnostic.terminal_density_closed)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)

    def test_input_validation_is_fail_closed(self):
        for bad in (0, -1, True, 1.5):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    eligible_r_values(bad, 3)
        with self.assertRaises(ValueError):
            h_coefficients(4, 1)
        with self.assertRaises(ValueError):
            outer_lemma3_weight(12)


if __name__ == "__main__":
    unittest.main()
