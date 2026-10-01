"""Finite mathematical regressions, with no actual prime/zero data."""

from fractions import Fraction as F
import unittest

from source import dep_r09_height_weighted_density_replay as m


class FixedModulusScaleTests(unittest.TestCase):
    def test_local_and_truncation_detector_exponents(self):
        self.assertEqual(m.fixed_detector_exponent(F(0)), F(22, 7))
        self.assertEqual(m.fixed_detector_exponent(F(3, 2)), F(55, 7))

    def test_low_height_cannot_reuse_half_rankin_ratio(self):
        self.assertEqual(m.validate_half_rankin_ratio(F(2, 5)), F(7, 4))
        with self.assertRaises(ValueError):
            m.validate_half_rankin_ratio(F(1))

    def test_all_height_coefficient_is_source_factor_composition(self):
        coefficient = m.all_height_selected_coefficient()
        self.assertEqual(coefficient, F(12, 7) * F(11503697604450072, 425315))
        self.assertLess(coefficient, 5 * 10**10)


class HeightLayerCakeTests(unittest.TestCase):
    def test_repeated_heights_and_terminal_atom_are_preserved(self):
        result = m.finite_height_layer_cake(
            (F(2), F(3), F(5), F(7)), (F(1), F(1), F(3), F(8)), F(8)
        )
        self.assertEqual(result["weighted_sum"], F(181, 24))
        self.assertEqual(result["weighted_sum"], result["endpoint"] + result["integral"])

    def test_single_low_height_has_full_not_terminal_suppressed_weight(self):
        result = m.finite_height_layer_cake((F(1),), (F(1),), F(100))
        self.assertEqual(result["weighted_sum"], F(1))
        self.assertEqual(result["endpoint"], F(1, 100))
        self.assertEqual(result["integral"], F(99, 100))

    def test_empty_packet_is_exact_zero(self):
        result = m.finite_height_layer_cake((), (), F(1))
        self.assertEqual(result["weighted_sum"], F(0))

    def test_negative_weight_or_outside_height_fails_closed(self):
        with self.assertRaises(ValueError):
            m.finite_height_layer_cake((F(-1),), (F(1),), F(2))
        with self.assertRaises(ValueError):
            m.finite_height_layer_cake((F(1),), (F(3),), F(2))


class DensityTransferTests(unittest.TestCase):
    def test_density_factor_at_adverse_and_favorable_supplied_ratios(self):
        for d, ratio in ((F(21), F(3, 2)), (F(333), F(0)), (F(416), F(3, 2))):
            self.assertLess(m.density_integration_factor(d, ratio), 20)
        with self.assertRaises(ValueError):
            m.density_integration_factor(F(21), F(2))

    def test_height_cost_gap_keeps_four_fifths_decay(self):
        for w in (F(0), F(3, 4), F(100)):
            self.assertGreaterEqual(m.height_cost_gap(F(441), F(416), m.C_M, w), F(4, 5)*w)
        with self.assertRaises(ValueError):
            m.height_cost_gap(F(1), F(416), m.C_M, F(2))

    def test_d333_regime_exponent_comparisons_are_rational(self):
        self.assertGreater(m.C_M, F(129, 1250))
        self.assertGreater(F(129, 1250)*(333-F(23, 7)), 34)
        self.assertGreater(m.C_B0*333, 6)
        self.assertLess(m.coarse_fixed_regime_budget(), F(1, 100))


class ProvenanceTests(unittest.TestCase):
    def test_source_pins_preserve_actual_project_gates(self):
        result = m.audit_ledger()
        self.assertEqual(result["source_count"], 6)
        self.assertEqual(result["kappa_fixed_s_3_over_2"], "55/7")
        self.assertFalse(result["uniform_native_d_ge_333_proved"])
        self.assertFalse(result["numeric_EF_multiplier_recovered"])
        self.assertFalse(result["same_law_all_character_correlation_closed"])


if __name__ == "__main__":
    unittest.main()
