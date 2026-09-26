"""Exact tests for the DEP-R09 blind fixed-modulus reduction."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_blind_fixed_modulus_reduction as m


class LiftedSumTests(unittest.TestCase):
    def test_prime_power_removal_identity_is_exact(self):
        result = m.lifted_sum_decomposition(
            (
                (2, 1, Fraction(2), 1),
                (2, 2, Fraction(2), -1),
                (3, 1, Fraction(3), -1),
                (5, 1, Fraction(5), 1),
            ),
            (2, 3),
        )
        self.assertEqual(
            result,
            {
                "native": Fraction(2),
                "lifted": Fraction(5),
                "removed": Fraction(-3),
            },
        )

    def test_duplicate_or_invalid_terms_fail_closed(self):
        with self.assertRaises(ValueError):
            m.lifted_sum_decomposition(
                (
                    (2, 1, Fraction(1), 1),
                    (2, 1, Fraction(1), -1),
                ),
                (2,),
            )
        with self.assertRaises(ValueError):
            m.lifted_sum_decomposition(
                ((2, 1, Fraction(1), 2),),
                (2,),
            )


class EnergyTransferTests(unittest.TestCase):
    def test_correction_and_flexible_energy_upper(self):
        self.assertEqual(
            m.correction_pointwise_upper(2, Fraction(7)),
            14,
        )
        self.assertEqual(
            m.transferred_energy_upper(
                Fraction(9), 4, Fraction(3), Fraction(1)
            ),
            90,
        )

    def test_uniform_blind_gate_and_quarter_split(self):
        gate = m.blind_uniform_gate(
            Fraction(1, 2), Fraction(3), Fraction(5), Fraction(8)
        )
        self.assertEqual(gate, Fraction(15, 4))
        self.assertTrue(
            m.split_budget_suffices(
                Fraction(1, 2), Fraction(1, 4), gate
            )
        )
        self.assertFalse(
            m.split_budget_suffices(
                gate / 4, Fraction(0), gate
            )
        )

    def test_invalid_energy_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.transferred_energy_upper(
                Fraction(-1), 2, Fraction(1)
            )
        with self.assertRaises(ValueError):
            m.blind_uniform_gate(
                Fraction(1, 2), Fraction(4), Fraction(5), Fraction(4)
            )


class EffectiveExponentTests(unittest.TestCase):
    def test_effective_exponent_interval_is_exact(self):
        lower, upper = m.effective_fixed_modulus_exponent_interval(186)
        self.assertEqual(lower, 186)
        self.assertEqual(upper, Fraction(19530, 47))
        self.assertLess(upper, 416)

    def test_endpoint_range_is_below_bennett_coarse_cutoff(self):
        for d in (21, 160, 186):
            self.assertLess(
                m.effective_fixed_modulus_exponent_upper(d),
                900,
            )


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.lifted_native_prime_power_identity_exact)
        self.assertTrue(diagnostic.effective_exponent_upper_below_416)
        self.assertFalse(
            diagnostic.bennett_large_modulus_cutoff_overlaps_effective_range
        )
        self.assertFalse(diagnostic.native_fixed_modulus_energy_upper_identified)
        self.assertFalse(
            diagnostic.imprimitive_correction_is_the_analytic_core_blocker
        )
        self.assertFalse(diagnostic.dep_r09_closed)

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
