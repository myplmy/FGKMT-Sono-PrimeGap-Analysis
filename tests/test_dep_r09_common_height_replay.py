"""Mathematical regression tests for the common-height explicit-formula replay."""

from fractions import Fraction as F
import unittest

from source import dep_r09_common_height_replay as m
from source.dep_r09_weighted_survivor_moment_audit import GaussianRational as G


class CenteredMaskTests(unittest.TestCase):
    def test_mass_identity_and_sharp_remainder_over_all_small_masks(self):
        # Exhaust small abstract residue masks, not primes or actual moduli.
        from itertools import combinations
        for phi in range(1, 9):
            for count in range(phi + 1):
                for selected in combinations(range(phi), count):
                    weights = m.centered_mask(phi, selected)
                    mass = m.mask_mass(phi, selected)
                    self.assertEqual(mass["zero_sum"], 0)
                    self.assertEqual(mass["l1"], mass["l1_formula"])
                    aligned = sum(abs(h) * F(3, 7) for h in weights)
                    self.assertEqual(aligned, m.remainder_budget(phi, selected, F(1, 7), F(2, 7)))

    def test_duplicate_residues_fail_closed(self):
        with self.assertRaises(ValueError):
            m.centered_mask(4, (0, 0))


class CommonHeightTests(unittest.TestCase):
    def setUp(self):
        self.upper = (G(F(99)), G(F(2), F(1)), G(F(-3)), G(F(2), F(-1)))
        self.lower = (G(F(7)), G(F(1)), G(F(2)), G(F(1)))
        self.regularizers = (G(F(200)), G(F(13), F(17)), G(F(-21)), G(F(13), F(-17)))

    def replay(self, upper=None, regularizers=None):
        return m.synthetic_replay_mod_five(
            (0, 1), upper or self.upper, self.lower,
            regularizers or self.regularizers,
            (F(1, 10), F(-1, 20), F(1, 30), F(1, 40)),
            (F(0), F(1, 20), F(0), F(-1, 40)),
        )

    def test_signed_complex_replay_agrees_with_residue_projection(self):
        result = self.replay()
        self.assertEqual(result["residue_side"], result["replay_side"])
        self.assertNotEqual(result["signed_zero"], G(F(0)))

    def test_principal_packet_and_regularizers_do_not_change_result(self):
        original = self.replay()
        changed = self.replay(
            (G(F(-10**9), F(123)), *self.upper[1:]),
            (G(F(-900)), G(F(31), F(-8)), G(F(17)), G(F(-1), F(8))),
        )
        self.assertEqual(original, changed)

    def test_different_endpoint_regularizers_are_rejected(self):
        with self.assertRaises(ValueError):
            m.common_height_packet_difference(
                self.upper, self.lower, self.regularizers, self.upper
            )


class ErrorShapeTests(unittest.TestCase):
    def test_endpoint_error_shape_is_monotone_in_supplied_scale_and_log(self):
        upper = m.ef_error_shape(F(1000), F(7), F(3), F(81), F(4), 4)
        lower = m.ef_error_shape(F(20), F(3), F(3), F(81), F(4), 4)
        self.assertGreaterEqual(upper, lower)
        self.assertEqual(m.remainder_budget(4, (0, 1), upper, lower), 8 * (upper + lower))

    def test_height_coefficient_and_density_exponents(self):
        self.assertEqual(m.truncation_coefficient(), 699716)
        self.assertEqual(m.density_height_kappa(F(5)), 22)
        self.assertEqual(m.density_height_kappa(F(3, 2)), 11)
        self.assertEqual(m.density_height_kappa(F(2)), F(88, 7))

    def test_height_without_power_saving_fails_closed(self):
        with self.assertRaises(ValueError):
            m.truncation_coefficient(height_exponent=F(1))
        with self.assertRaises(ValueError):
            m.density_height_kappa(F(1))


class ProvenanceTests(unittest.TestCase):
    def test_source_pins_and_terminals_keep_analytic_gates_open(self):
        report = m.audit_ledger()
        self.assertEqual(report["source_count"], 4)
        self.assertEqual(report["truncation_coefficient"], "699716")
        self.assertFalse(report["signed_zero_gate_closed"])
        self.assertFalse(report["lower_height_density_transfer_closed"])
        self.assertFalse(report["numeric_EF_multiplier_recovered"])


if __name__ == "__main__":
    unittest.main()
