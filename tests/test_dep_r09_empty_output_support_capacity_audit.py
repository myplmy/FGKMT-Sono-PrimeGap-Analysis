"""Exact tests for the DEP-R09 empty-output support-capacity audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_empty_output_support_capacity_audit as m


class SupportCapacityTests(unittest.TestCase):
    def test_randomized_coordinate_product_is_exact(self):
        self.assertEqual(
            m.randomized_residue_support_size((2, 3), (5, 7)),
            210,
        )
        self.assertEqual(
            m.randomized_residue_support_size((2, 3), ()),
            6,
        )

    def test_invalid_coordinate_sets_fail_closed(self):
        with self.assertRaises(ValueError):
            m.randomized_residue_support_size((), ())
        with self.assertRaises(ValueError):
            m.randomized_residue_support_size((2, 3), (3, 5))
        with self.assertRaises(TypeError):
            m.randomized_residue_support_size((2, True), ())


class EventPigeonholeTests(unittest.TestCase):
    def test_success_mass_is_not_dropped(self):
        mass = Fraction(3, 5)
        lower = m.event_atom_pigeonhole_lower(mass, 210)
        self.assertEqual(lower, Fraction(1, 350))
        self.assertEqual(
            m.event_entropy_factor(mass, lower, 210),
            210,
        )

    def test_looser_atom_cap_loses_entropy_factor(self):
        factor = m.event_entropy_factor(
            Fraction(3, 5), Fraction(1, 300), 210
        )
        self.assertEqual(factor, 180)
        self.assertLess(factor, 210)

    def test_impossible_atom_cap_is_rejected(self):
        with self.assertRaises(ValueError):
            m.event_entropy_factor(
                Fraction(3, 5), Fraction(1, 351), 210
            )
        with self.assertRaises(TypeError):
            m.event_atom_pigeonhole_lower(
                Fraction(1, 2), 2.0  # type: ignore[arg-type]
            )


class ScaleCoefficientTests(unittest.TestCase):
    def test_support_coefficients_are_exact(self):
        self.assertEqual(
            m.outer_support_log_coefficient_upper(),
            Fraction(21, 16000),
        )
        self.assertEqual(
            m.inner_support_log_coefficient_upper(),
            Fraction(1003, 2000),
        )
        self.assertEqual(
            m.total_support_log_coefficient_upper(),
            Fraction(1609, 3200),
        )

    def test_support_is_strictly_subprimorial(self):
        support = m.total_support_log_coefficient_upper()
        full = m.full_primorial_log_coefficient_lower()
        self.assertLess(support, Fraction(51, 100))
        self.assertEqual(full, Fraction(49, 50))
        self.assertLess(support, full)


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.finite_support_pigeonhole_exact)
        self.assertTrue(
            diagnostic.event_success_mass_retained_in_entropy_factor
        )
        self.assertTrue(
            diagnostic.randomized_support_is_strictly_subprimorial
        )
        self.assertFalse(
            diagnostic.any_empty_output_tail_can_rescue_atom_full_energy_large_sieve_route
        )
        self.assertFalse(diagnostic.local_character_phase_cancellation_ruled_out)
        self.assertFalse(diagnostic.actual_empty_output_numerical_tail_identified)
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
