"""Exact tests for the DEP-R09 weighted survivor-moment audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_weighted_survivor_moment_audit as m


class WeightedMomentTests(unittest.TestCase):
    def test_common_shock_direct_formula_and_certificate_agree(self):
        weights = tuple(m.GaussianRational(Fraction(1)) for _ in range(4))
        model = m.common_shock_probabilities(
            4, Fraction(1, 8), Fraction(3, 8)
        )
        exhaustive = m.enumerate_common_shock_second_moment(
            weights, Fraction(1, 8), Fraction(3, 8)
        )
        direct = m.weighted_second_moment(
            weights, model["singles"], model["pairs"]
        )
        upper = m.weighted_pair_error_upper(
            weights, model["rho"], Fraction(0), model["beta"]
        )
        self.assertEqual(exhaustive, Fraction(31, 16))
        self.assertEqual(direct, exhaustive)
        self.assertEqual(upper, exhaustive)

    def test_complex_weights_are_exact(self):
        weights = (
            m.GaussianRational(Fraction(1), Fraction(1)),
            m.GaussianRational(Fraction(-1, 2), Fraction(2)),
        )
        observed = m.weighted_second_moment(
            weights,
            (Fraction(1, 2), Fraction(1, 3)),
            {(0, 1): Fraction(1, 6)},
        )
        self.assertEqual(observed, Fraction(35, 12))
        self.assertGreaterEqual(
            m.weighted_pair_error_upper(
                weights, Fraction(1, 3), Fraction(1, 2), Fraction(1, 2)
            ),
            observed,
        )

    def test_invalid_pair_data_fail_closed(self):
        weight = m.GaussianRational(Fraction(1))
        with self.assertRaises(ValueError):
            m.weighted_second_moment((weight, weight), (Fraction(1),), {})
        with self.assertRaises(ValueError):
            m.weighted_second_moment(
                (weight, weight),
                (Fraction(1), Fraction(1)),
                {},
            )
        with self.assertRaises(TypeError):
            m.GaussianRational(Fraction(1), 0)  # type: ignore[arg-type]


class PairErrorTests(unittest.TestCase):
    def test_common_shock_relative_error_is_exact(self):
        model = m.common_shock_probabilities(
            4, Fraction(1, 8), Fraction(3, 8)
        )
        self.assertEqual(model["rho"], Fraction(1, 4))
        self.assertEqual(model["pair"], Fraction(5, 64))
        self.assertEqual(model["beta"], Fraction(1, 4))
        self.assertEqual(
            m.pair_error_spectral_factor_lower(
                model["beta"], Fraction(4)
            ),
            1,
        )

    def test_invalid_common_shock_fails_closed(self):
        with self.assertRaises(ValueError):
            m.common_shock_probabilities(
                1, Fraction(1, 8), Fraction(3, 8)
            )
        with self.assertRaises(ValueError):
            m.common_shock_probabilities(
                3, Fraction(0), Fraction(0)
            )


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.arbitrary_complex_weight_second_moment_exact)
        self.assertTrue(diagnostic.entrywise_pair_error_upper_exact)
        self.assertTrue(
            diagnostic.beta_times_support_loss_is_unavoidable_from_entrywise_data
        )
        self.assertFalse(
            diagnostic.gould_kelly_handles_current_indexed_variable_edge_covering_law
        )
        self.assertFalse(diagnostic.applicable_weighted_nibble_drop_in_identified)
        self.assertFalse(diagnostic.blind_weighted_moment_closed)

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
