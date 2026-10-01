"""Exact source-expression and cumulative-split fixtures, no actual zeros."""

from fractions import Fraction as F
import unittest
from source import dep_r09_lw_first_window as m


class SourceScalarTests(unittest.TestCase):
    def test_denominator_and_floor_on_supplied_boundary_parameters(self):
        for log_z,kappa in ((F(30000),F(277,1000)),
                            (F(30000),F(0)),(F(60000),F(277,1000))):
            result=m.scalar_parts(log_z,kappa)
            self.assertGreater(result["denominator"],F(1,8))
            self.assertLessEqual(result["ratio"],72)
            self.assertLessEqual(result["twice_floor"],144)

    def test_wrong_log_or_kappa_fails_closed(self):
        with self.assertRaises(ValueError):
            m.scalar_parts(F(29999),F(277,1000))
        with self.assertRaises(ValueError):
            m.scalar_parts(F(30000),F(278,1000))

    def test_fixed_safe_envelope_is_not_the_printed_table(self):
        envelope=m.rational_envelope()
        self.assertEqual(envelope["count_upper"],144)
        self.assertGreater(envelope["denominator_lower"],F(1,8))
        self.assertNotEqual(envelope["count_upper"],182)
        self.assertNotEqual(envelope["count_upper"],364)

    def test_source_parameters_fit_published_branch(self):
        self.assertTrue(F(0)<m.LW_A<=F(2,5))
        self.assertTrue(F(262132,10**6)<=m.LW_LAMBDA<=F(12,25))
        self.assertEqual(1/(m.LW_A+m.LW_LAMBDA),F(100,79))

    def test_source_pins_and_unresolved_gates(self):
        value=m.audit_ledger()
        self.assertEqual(value["source_count"],3)
        self.assertFalse(value["numeric_EF_multiplier_recovered"])
        self.assertFalse(value["pointwise_full_modulus_PNT_closed"])
        self.assertFalse(value["numerical_x_cert_ready"])

    def test_spacing_count_is_rechecked_before_alternating_selection(self):
        value=m.local_spacing_envelope()
        self.assertLess(value["spacing_numerator_upper"],F(3,5))
        self.assertGreater(value["spacing_denominator_lower"],F(1,5))
        self.assertEqual(value["local_count_upper"],2)


class HybridScalarTests(unittest.TestCase):
    def test_tail_integral_factor_at_height_endpoints(self):
        self.assertLess(m.tail_integration_factor(F(0)),24)
        self.assertLess(m.tail_integration_factor(F(3,2)),24)
        with self.assertRaises(ValueError):
            m.tail_integration_factor(F(2))

    def test_cumulative_split_is_additive_not_a_pointwise_minimum(self):
        value=m.cumulative_split_bound(F(144),F(1,10**6),
                                       F(24),F(1,10**8))
        self.assertEqual(value,F(144,10**6)+F(24,10**8))
        self.assertGreater(value,min(F(144,10**6),F(24,10**8)))

    def test_nonnegative_split_required(self):
        with self.assertRaises(ValueError):
            m.cumulative_split_bound(F(-1),F(1),F(24),F(1))

    def test_fixed_D160_hybrid_rational_budget(self):
        self.assertLess(m.hybrid_nonvanishing_rational_budget(),F(3,1000))


if __name__ == "__main__":
    unittest.main()
