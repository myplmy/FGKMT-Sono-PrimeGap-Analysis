"""Exact tests for the Thorner--Zaman full-interval centered transfer."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_tz_full_interval_centered as m


class ZeroFreeTransferTests(unittest.TestCase):
    def test_relative_zero_free_constant(self):
        self.assertEqual(m.relative_zero_free_constant(), Fraction(47, 2520))

    def test_invalid_zero_free_input_fails_closed(self):
        with self.assertRaises(ValueError):
            m.relative_zero_free_constant(Fraction(0))

    def test_full_interval_source_range(self):
        self.assertTrue(m.full_interval_range_holds(21, 12))
        self.assertFalse(m.full_interval_range_holds(11, 12))


class CenteringTests(unittest.TestCase):
    def test_common_main_error_centers_with_factor_two(self):
        result = m.centered_linf_envelope(
            (
                Fraction(1, 100),
                Fraction(-1, 100),
                Fraction(-1, 100),
                Fraction(-1, 100),
            )
        )
        self.assertEqual(result["raw_linf"], Fraction(1, 100))
        self.assertEqual(result["centered_linf"], Fraction(3, 200))
        self.assertEqual(result["envelope"], Fraction(1, 50))

    def test_empty_error_vector_fails_closed(self):
        with self.assertRaises(ValueError):
            m.centered_error_vector(())

    def test_exceptional_character_pattern_survives_centering(self):
        result = m.exceptional_main_centering(
            (1, -1, 1, -1), Fraction(3, 100)
        )
        self.assertEqual(
            result,
            (
                Fraction(-3, 100),
                Fraction(3, 100),
                Fraction(-3, 100),
                Fraction(3, 100),
            ),
        )

    def test_nonzero_character_mean_fails_closed(self):
        with self.assertRaises(ValueError):
            m.exceptional_main_centering((1, 1), Fraction(1, 10))


class ProjectTransferTests(unittest.TestCase):
    def test_endpoint_and_project_multipliers(self):
        source_error = Fraction(1, 1000)
        correction = Fraction(1, 100000)
        self.assertEqual(
            m.endpoint_kappa_upper(source_error, correction),
            Fraction(4221, 500000),
        )
        self.assertEqual(
            m.project_delta_upper(
                source_error, correction, Fraction(1, 100)
            ),
            Fraction(848421, 50000000),
        )

    def test_negative_project_input_fails_closed(self):
        with self.assertRaises(ValueError):
            m.project_delta_upper(
                Fraction(-1), Fraction(0), Fraction(0)
            )


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.source_tex_archive_verified)
        self.assertTrue(diagnostic.tz_remark_13_lambda_one_branch_applicable)
        self.assertFalse(diagnostic.proof_of_theorem_23_handles_h_equal_x)
        self.assertFalse(diagnostic.tz_numerical_implied_multiplier_printed)
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
