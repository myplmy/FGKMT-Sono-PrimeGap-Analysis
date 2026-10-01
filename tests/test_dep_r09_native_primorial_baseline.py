"""Source-independent finite fixtures for the native primorial split."""

from fractions import Fraction as F
import unittest

from source import dep_r09_native_primorial_baseline as m


class FactorPartitionTests(unittest.TestCase):
    ALL = (2, 3, 5, 7, 11, 13)
    LOWER = (2, 3, 5)

    def test_no_exception_and_inner_exception_have_same_native_product(self):
        no_exception = m.factor_partition(self.ALL, self.LOWER, (3,), 1)
        inner_exception = m.factor_partition(self.ALL, self.LOWER, (3,), 11)
        self.assertEqual(no_exception["f"], 10)
        self.assertEqual(inner_exception["f"], 10)
        self.assertEqual(inner_exception["inner_labels"], (7, 13))
        self.assertEqual(inner_exception["q"], inner_exception["h"]*inner_exception["f"])

    def test_lower_exception_is_removed_exactly_once(self):
        result = m.factor_partition(self.ALL, self.LOWER, (3,), 2)
        self.assertEqual(result["f"], 5)
        self.assertEqual(result["low_exception"], 2)
        self.assertEqual(result["f"]*3*2, result["lower_product"])

    def test_exceptional_factor_cannot_remain_in_outer_coordinates(self):
        with self.assertRaises(ValueError):
            m.factor_partition(self.ALL, self.LOWER, (3,), 3)
        result = m.factor_partition(self.ALL, self.LOWER, (5,), 3)
        self.assertEqual(result["f"], 2)

    def test_wrong_raw_inner_subset_fails_closed(self):
        with self.assertRaises(ValueError):
            m.require_raw_inner((7, 13), self.ALL, self.LOWER, 1)
        m.require_raw_inner((7, 11, 13), self.ALL, self.LOWER, 1)

    def test_wrong_lower_membership_fails_closed(self):
        with self.assertRaises(ValueError):
            m.factor_partition(self.ALL, (2, 17), (), 1)

    def test_duplicate_factor_labels_fails_closed(self):
        with self.assertRaises(ValueError):
            m.factor_partition((2, 2, 3), (2,), (), 1)


class BaselineBudgetTests(unittest.TestCase):
    def test_D160_native_regime_is_above_314_below_323(self):
        low, high = m.native_log_ratio_terminals()
        self.assertEqual(low, F(3992000, 12703))
        self.assertEqual(high, F(106720, 331))
        self.assertGreater(low, 314)
        self.assertLess(high, 323)
        self.assertLess(high, 333)

    def test_native_314_exponent_enclosures(self):
        self.assertGreater(F(129, 1250)*(314-F(23, 7)), 32)
        self.assertEqual(m.full_primorial_real_decay_lower(), F(39920, 6003))
        self.assertGreater(m.full_primorial_real_decay_lower(), 6)
        self.assertLess(m.baseline_nonvanishing_rational_budget(), F(1, 36))

    def test_power_support_cap_preserves_original_definition(self):
        self.assertEqual(m.source_support_log_cap(), F(128909, 256000))
        self.assertLess(m.source_support_log_cap(), F(51, 100))

    def test_vanishing_coefficient_is_parametric_not_K_equals_one(self):
        self.assertEqual(m.vanishing_coefficient(F(0)), F(54927, 10))
        self.assertEqual(m.vanishing_coefficient(F(7, 3)),
                         699716*F(7, 3)+F(54927, 10))
        with self.assertRaises(ValueError):
            m.vanishing_coefficient(F(-1))


class ProvenanceTests(unittest.TestCase):
    def test_source_pins_and_unresolved_global_gates(self):
        result = m.audit_ledger()
        self.assertEqual(result["source_count"], 6)
        self.assertEqual(result["native_upper"], "106720/331")
        self.assertEqual(result["full_primorial_real_decay_lower"], "39920/6003")
        self.assertFalse(result["numeric_EF_multiplier_recovered"])
        self.assertFalse(result["same_law_all_character_correlation_closed"])
        self.assertFalse(result["outer_D_changed"])


if __name__ == "__main__":
    unittest.main()
