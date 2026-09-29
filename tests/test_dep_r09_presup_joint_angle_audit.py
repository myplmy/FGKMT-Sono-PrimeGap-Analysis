"""Exact tests for the DEP-R09 pre-sup joint-angle source audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_presup_joint_angle_audit as m


class PhaseBlindTests(unittest.TestCase):
    def test_alignment_attains_triangle_envelope(self):
        result = m.phase_blind_alignment_witness(
            (Fraction(2), Fraction(-3)),
            (Fraction(5), Fraction(7)),
        )
        self.assertEqual(result["packets"], ("5", "-7"))
        self.assertEqual(result["correlation"], 31)
        self.assertEqual(result["envelope"], 31)

    def test_same_magnitudes_can_cancel(self):
        self.assertEqual(
            m.weighted_correlation(
                (Fraction(1), Fraction(1)),
                (Fraction(1), Fraction(-1)),
            ),
            0,
        )
        self.assertEqual(
            m.phase_blind_triangle_envelope(
                (Fraction(1), Fraction(1)),
                (Fraction(1), Fraction(1)),
            ),
            2,
        )

    def test_invalid_magnitude_fails_closed(self):
        with self.assertRaises(ValueError):
            m.phase_blind_triangle_envelope(
                (Fraction(1),),
                (Fraction(-1),),
            )


class AngleTests(unittest.TestCase):
    def test_aligned_vectors_have_squared_angle_one(self):
        self.assertEqual(
            m.squared_angle(
                (Fraction(2), Fraction(-3)),
                (Fraction(10), Fraction(-15)),
            ),
            1,
        )

    def test_required_squared_angle_budget(self):
        self.assertEqual(
            m.required_squared_angle_budget(Fraction(1, 100), 3, 30),
            Fraction(1, 90000),
        )

    def test_zero_vector_angle_fails_closed(self):
        with self.assertRaises(ValueError):
            m.squared_angle((Fraction(0),), (Fraction(1),))


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.aligned_phase_triangle_is_exact)
        self.assertTrue(diagnostic.cancellation_fixture_same_magnitudes)
        self.assertFalse(diagnostic.support_only_source_controls_joint_angle)
        self.assertFalse(diagnostic.applicable_numerical_joint_angle_source_identified)
        self.assertFalse(diagnostic.pre_sup_joint_correlation_closed)

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
