"""Exact tests for the DEP-R09 explicit density-exponent-99 audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_explicit_density99_audit as m


class RangeTests(unittest.TestCase):
    def test_epsilon_ceiling(self):
        self.assertEqual(m.epsilon_ceiling(), Fraction(317, 41184))

    def test_density_sigma_floor_exceeds_source_minimum(self):
        self.assertEqual(m.density_sigma_floor(), Fraction(98, 99))
        self.assertGreater(m.density_sigma_floor(), Fraction(39, 40))

    def test_invalid_range_fails_closed(self):
        with self.assertRaises(ValueError):
            m.epsilon_ceiling(99, 99)


class CertificateFloorTests(unittest.TestCase):
    def test_decay_exponent_is_below_three_per_thousand(self):
        result = m.decay_exponent_upper()
        self.assertEqual(
            result,
            Fraction(3140281250000, 1229014178061813),
        )
        self.assertLess(result, Fraction(3, 1000))

    def test_optimistic_floor_exceeds_49(self):
        floor = m.optimistic_sup_factor_floor()
        self.assertEqual(floor, Fraction(98703, 2000))
        self.assertGreater(floor, 49)

    def test_invalid_zero_free_constant_fails_closed(self):
        with self.assertRaises(ValueError):
            m.decay_exponent_upper(zero_free_constant=Fraction(0))


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.current_range_overlaps_density99)
        self.assertTrue(diagnostic.optimistic_sup_factor_floor_exceeds_49)
        self.assertFalse(
            diagnostic.multiplier_one_direct_certificate_closes_endpoint_gate
        )
        self.assertFalse(diagnostic.density99_direct_black_box_route_closed)
        self.assertFalse(diagnostic.centered_endpoint_gate_closed)

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
