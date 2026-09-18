"""Fail-closed tests for the Theory-85 Vaughan 2001 source audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

import mpmath as mp

from source import dep_r09_vaughan2001_variance_audit as m


class CenteringIdentityTests(unittest.TestCase):
    def test_exact_centering_decomposition(self):
        result = m.centering_decomposition((1, 4, 7), 9)
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["vaughan_variance"], Fraction(21))
        self.assertEqual(result["mean_centered_variance"], Fraction(18))
        self.assertEqual(result["principal_error_term"], Fraction(3))
        self.assertEqual(result["character_energy"], Fraction(54))
        self.assertEqual(result["scaled_vaughan_variance"], Fraction(63))
        self.assertTrue(m.centering_identity_is_exact((1, 4, 7), 9))

    def test_exact_fractional_and_zero_samples(self):
        self.assertTrue(
            m.centering_identity_is_exact(
                (Fraction(1, 2), Fraction(5, 2)), 4
            )
        )
        self.assertTrue(m.centering_identity_is_exact((0, 0, 0, 0), 3))

    def test_invalid_centering_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.centering_decomposition((), 0)
        with self.assertRaises(TypeError):
            m.centering_decomposition((True,), 0)  # type: ignore[arg-type]


class SourceRangeTests(unittest.TestCase):
    def test_current_power_range_is_below_grh_source_range(self):
        self.assertEqual(m.current_power_exponent(21), Fraction(1, 21))
        self.assertGreater(m.theorem2_exponent_gap(21), 0)
        self.assertGreater(m.theorem2_exponent_gap(186), 0)
        self.assertGreater(
            m.theorem2_exponent_gap(21, Fraction(1, 100)),
            m.theorem2_exponent_gap(21),
        )

    def test_theorem1_required_a_is_exact_boundary_in_log_space(self):
        before = mp.mp.dps
        with mp.workdps(100):
            required = m.theorem1_required_a(510510, 21)
            margin = (
                required * mp.log(21 * mp.log(510510))
                - 20 * mp.log(510510)
            )
            self.assertLess(abs(margin), mp.mpf("1e-90"))
            self.assertLess(m.theorem1_log_range_margin(510510, 21, 1), 0)
        self.assertEqual(mp.mp.dps, before)

    def test_invalid_range_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.current_power_exponent(0)
        with self.assertRaises(ValueError):
            m.theorem2_exponent_gap(21, Fraction(-1, 100))
        with self.assertRaises(ValueError):
            m.theorem1_required_a(2, 21)
        with self.assertRaises(TypeError):
            m.theorem1_log_range_margin(3, 21, True)  # type: ignore[arg-type]


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.vaughan_2001_pdf_identity_verified)
        self.assertTrue(diagnostic.vaughan_2001_pdf_page_count_verified)
        self.assertTrue(diagnostic.exact_centering_decomposition_samples_all_pass)
        self.assertTrue(
            diagnostic.exact_character_energy_upper_bridge_samples_all_pass
        )
        self.assertTrue(diagnostic.current_power_exponents_all_below_three_quarters)
        self.assertTrue(diagnostic.theorem1_is_dyadic_modulus_moment)
        self.assertFalse(diagnostic.theorem1_fixed_a_covers_growing_current_family)
        self.assertTrue(diagnostic.theorem2_requires_grh)
        self.assertFalse(diagnostic.theorem2_range_overlaps_current_power_regime)
        self.assertFalse(diagnostic.theorem3_is_fixed_primorial_character_energy_upper)
        self.assertFalse(
            diagnostic.fully_numerical_unconditional_current_regime_drop_in_identified
        )
        self.assertFalse(diagnostic.prime_specific_fixed_primorial_bound_identified)
        self.assertFalse(diagnostic.direct_same_law_correlation_theorem_identified)
        self.assertFalse(diagnostic.actual_character_energy_lower_bound_claimed)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.bounded_x_cert_range_obtained)
        self.assertFalse(diagnostic.threshold_calculator_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_and_source_hash(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hash=False))

        changed = deepcopy(m.load_ledger())
        changed["local_primary_source"]["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
