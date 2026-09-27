"""Exact tests for the DEP-R09 outer-law sparse-mean reduction."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_outer_law_sparse_mean as m


class WeightedOuterMomentTests(unittest.TestCase):
    def test_common_shock_signed_weight_moments(self):
        weights = (Fraction(2), Fraction(-1), Fraction(3))
        table = m.common_shock_table(3, Fraction(1, 4), Fraction(3, 4))
        result = m.weighted_moments_from_table(weights, table)
        sigma = Fraction(1, 2)
        pair = Fraction(5, 16)
        epsilon = abs(pair - sigma**2) / sigma**2
        self.assertEqual(result["singles"], (sigma, sigma, sigma))
        self.assertTrue(all(value == pair for value in result["pairs"].values()))
        self.assertEqual(result["expectation"], sigma * sum(weights))
        self.assertLessEqual(
            result["variance"],
            m.weighted_outer_variance_upper(weights, sigma, epsilon),
        )

    def test_all_one_common_shock_saturates_pair_certificate(self):
        weights = (Fraction(1),) * 4
        table = m.common_shock_table(4, Fraction(1, 8), Fraction(3, 8))
        result = m.weighted_moments_from_table(weights, table)
        sigma = Fraction(1, 4)
        epsilon = Fraction(1, 4)
        self.assertEqual(
            result["variance"],
            m.weighted_outer_variance_upper(weights, sigma, epsilon),
        )

    def test_invalid_probability_table_fails_closed(self):
        with self.assertRaises(ValueError):
            m.weighted_moments_from_table(
                (Fraction(1),), {(False,): Fraction(1)}
            )
        with self.assertRaises(ValueError):
            m.common_shock_table(11, Fraction(1, 4), Fraction(3, 4))


class NormalizationTests(unittest.TestCase):
    def test_linfinity_normalized_variance_formula(self):
        observed = m.normalized_outer_variance_upper(
            Fraction(11, 5), Fraction(1, 4), Fraction(1, 100), 10
        )
        expected = Fraction(121, 25) * (
            Fraction(3, 10) + Fraction(9, 1000)
        )
        self.assertEqual(observed, expected)

    def test_markov_failure_and_strict_positive_ratio(self):
        raw = m.normalized_outer_variance_upper(
            Fraction(1), Fraction(1, 2), Fraction(1, 1000), 1000
        )
        failure = m.weighted_fluctuation_failure_upper(
            Fraction(1),
            Fraction(1, 2),
            Fraction(1, 1000),
            1000,
            Fraction(1, 10),
        )
        self.assertEqual(failure, min(Fraction(1), raw * 100))
        with self.assertRaises(ValueError):
            m.weighted_fluctuation_failure_upper(
                Fraction(1), Fraction(1, 2), Fraction(0), 10, Fraction(0)
            )


class AdaptiveDeletionTests(unittest.TestCase):
    def test_project_scale_and_selected_mean_formula(self):
        b = 2000
        eta = Fraction(1, b**3)
        deletion = Fraction(8000, b**2)
        scale = m.selected_count_scale_lower(eta, deletion)
        self.assertEqual(scale, Fraction(3991999999501, 4000000000000))
        upper = m.selected_mean_ratio_upper(
            Fraction(1, 100),
            Fraction(1, 1000),
            Fraction(11, 5),
            eta,
            deletion,
        )
        expected = (
            Fraction(1, 100)
            + Fraction(1, 1000)
            + Fraction(11, 5) * deletion * (1 + eta)
        ) / scale
        self.assertEqual(upper, expected)

    def test_adaptive_deletion_triangle_bound(self):
        result = m.deletion_triangle_bound(
            (Fraction(5), Fraction(-4), Fraction(2)), (0,)
        )
        self.assertEqual(result["before"], 3)
        self.assertEqual(result["removed"], 5)
        self.assertEqual(result["after"], -2)
        self.assertEqual(result["upper"], 8)

    def test_union_mass_is_fail_closed(self):
        self.assertEqual(
            m.outer_good_mass_lower(Fraction(1, 10), Fraction(1, 5)),
            Fraction(7, 10),
        )
        self.assertEqual(
            m.outer_good_mass_lower(Fraction(3, 4), Fraction(3, 4)),
            0,
        )
        with self.assertRaises(ValueError):
            m.selected_count_scale_lower(Fraction(0), Fraction(1))


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.weighted_expectation_exact)
        self.assertTrue(diagnostic.weighted_variance_certificate_valid)
        self.assertTrue(diagnostic.outer_fluctuation_parameterized_explicit)
        self.assertTrue(diagnostic.adaptive_deletion_parameterized_explicit)
        self.assertFalse(diagnostic.outer_randomization_removes_fixed_mean)
        self.assertFalse(diagnostic.fixed_qprime_mean_closed)
        self.assertFalse(diagnostic.prescribed_primorial_source_drop_in_identified)

    def test_ledger_and_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["dep_r09_closed"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))
        changed = deepcopy(m.load_ledger())
        changed["source_registry"][0]["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
