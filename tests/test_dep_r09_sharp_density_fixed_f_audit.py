"""Exact tests for the sharp near-one density fixed-f audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_sharp_density_fixed_f_audit as m


class ParameterTests(unittest.TestCase):
    def test_detector_kappa_endpoint(self):
        self.assertEqual(m.detector_kappa(), 22)

    def test_invalid_detector_window_fails_closed(self):
        with self.assertRaises(ValueError):
            m.detector_kappa(Fraction(1, 20))

    def test_favorable_decay_exponent_is_below_nine(self):
        result = m.favorable_decay_exponent_upper()
        self.assertEqual(result, Fraction(80400000000, 9645908801))
        self.assertLess(result, 9)


class CoefficientFloorTests(unittest.TestCase):
    def test_tightened_coefficient_floor_exceeds_one_million(self):
        result = m.tightened_coefficient_floor()
        self.assertEqual(result, Fraction(3834565868150024, 2790491715))
        self.assertGreater(result, 1_000_000)

    def test_theta_power_counterfactual_floor_exceeds_4000(self):
        result = m.theta_power_counterfactual_floor()
        self.assertEqual(result, Fraction(117649, 27))
        self.assertGreater(result, 4_000)


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.pap_outer_losses_removed_in_floor)
        self.assertTrue(diagnostic.tightened_core_floor_exceeds_one_million)
        self.assertTrue(diagnostic.theta_power_counterfactual_floor_exceeds_4000)
        self.assertFalse(
            diagnostic.current_sharp_density_certificate_closes_endpoint_gate
        )
        self.assertFalse(diagnostic.actual_endpoint_error_lower_proved)

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
