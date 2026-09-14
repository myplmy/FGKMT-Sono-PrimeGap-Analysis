"""Exact tests for the DEP-R09 filtration/survivor-floor audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_filtration_sensitivity as m


class SurvivorCountSensitivityTests(unittest.TestCase):
    def test_ceil_div_and_membership_bound(self):
        self.assertEqual(m.ceil_div(0, 5), 0)
        self.assertEqual(m.ceil_div(1, 5), 1)
        self.assertEqual(m.ceil_div(10, 5), 2)
        self.assertEqual(m.one_residue_membership_bound(11, 5), 6)

    def test_bruteforce_one_prime_changes_obey_exact_bound(self):
        for p, q in ((2, 3), (3, 5), (5, 7), (5, 13), (7, 11)):
            modulus = p * q
            for interval_start in (-7, 0, 1, 9):
                for interval_length in range(0, 3 * p + 2):
                    diagnostic = m.one_residue_count_diagnostic(
                        modulus,
                        p,
                        0,
                        q,
                        interval_start,
                        interval_length,
                    )
                    self.assertTrue(diagnostic.exact_bound_pass)
                    self.assertLessEqual(
                        diagnostic.count_difference,
                        diagnostic.symmetric_difference,
                    )
                    self.assertLessEqual(
                        diagnostic.symmetric_difference,
                        diagnostic.symmetric_difference_bound,
                    )

    def test_invalid_one_coordinate_contracts_fail_closed(self):
        with self.assertRaises(ValueError):
            m.one_residue_count_diagnostic(12, 3, 0, 4, 1, 5)
        with self.assertRaises(ValueError):
            m.one_residue_count_diagnostic(15, 4, 0, 5, 1, 5)
        with self.assertRaises(ValueError):
            m.one_residue_count_diagnostic(15, 3, 0, 1, 1, 5)
        with self.assertRaises(ValueError):
            m.one_residue_count_diagnostic(15, 3, 0, 15, 1, 5)


class CharacterPhaseTests(unittest.TestCase):
    def test_exact_nonprincipal_phase_counterexample(self):
        witness = m.character_phase_counterexample()
        self.assertEqual(witness.modulus, 65)
        self.assertEqual(witness.old_character_sum, -1)
        self.assertEqual(witness.new_character_sum, 2)
        self.assertEqual(witness.character_sum_difference, 3)
        self.assertEqual(witness.membership_symmetric_difference, 1)
        self.assertEqual(witness.membership_bound, 2)
        self.assertTrue(witness.exceeds_membership_bound)

    def test_trivial_character_and_weighted_l1_bounds(self):
        self.assertEqual(m.trivial_character_sum_change_bound(17), 34)
        self.assertEqual(
            m.weighted_l1_change_bound(17, Fraction(5, 7)),
            Fraction(170, 7),
        )
        with self.assertRaises(ValueError):
            m.weighted_l1_change_bound(1, Fraction(-1))


class SieveGoodNormalizationTests(unittest.TestCase):
    def test_mass_floor_and_raw_normalization_are_exact(self):
        self.assertEqual(
            m.sieve_good_mass_lower(Fraction(1, 5), Fraction(1, 4)),
            Fraction(3, 5),
        )
        floor = m.survivor_floor(
            Fraction(4), Fraction(1, 4), Fraction(10)
        )
        self.assertEqual(floor, Fraction(30))
        self.assertEqual(
            m.raw_to_sieve_good_normalized_moment_upper(
                Fraction(450), floor, Fraction(5)
            ),
            Fraction(1, 50),
        )

    def test_sieve_good_markov_gate_and_strict_boundary(self):
        self.assertEqual(
            m.sieve_good_markov_success_lower(
                Fraction(1, 5),
                Fraction(1, 4),
                Fraction(1, 100),
                Fraction(1, 2),
            ),
            Fraction(14, 25),
        )
        self.assertTrue(
            m.sieve_good_strict_gate(
                Fraction(1, 5),
                Fraction(1, 4),
                Fraction(149, 1000),
                Fraction(1, 2),
            )
        )
        self.assertFalse(
            m.sieve_good_strict_gate(
                Fraction(1, 5),
                Fraction(1, 4),
                Fraction(3, 20),
                Fraction(1, 2),
            )
        )

    def test_invalid_floor_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.survivor_floor(Fraction(1), Fraction(1), Fraction(3))
        with self.assertRaises(ValueError):
            m.raw_to_sieve_good_normalized_moment_upper(
                Fraction(1), Fraction(0), Fraction(3)
            )
        with self.assertRaises(TypeError):
            m.sieve_good_mass_lower(Fraction(0), 0.25)


class LedgerTests(unittest.TestCase):
    def test_ledger_and_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_fail_closed_status(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.sieve_good_denominator_floor_aligned)
        self.assertFalse(diagnostic.final_law_globally_product_independent)
        self.assertTrue(
            diagnostic.within_nibble_conditional_independence_source_verified
        )
        self.assertFalse(
            diagnostic.count_bound_transfers_to_nonprincipal_character_phase
        )
        self.assertFalse(diagnostic.martingale_increment_bound_available)
        self.assertFalse(diagnostic.martingale_conditional_variance_bound_available)
        self.assertFalse(diagnostic.same_law_analytic_moment_bound_available)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))
        changed = deepcopy(m.load_ledger())
        changed["source_registry"][0]["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
