"""Exact tests for the DEP-R09 cross-scale covariance interface."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_cross_scale_covariance as m
from source.dep_r09_weighted_survivor_moment_audit import GaussianRational


class AbelTests(unittest.TestCase):
    def test_finite_abel_interval_is_exact(self):
        result = m.discrete_abel_interval(
            (Fraction(2), Fraction(-1), Fraction(3), Fraction(4)),
            (Fraction(1), Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)),
            1,
            3,
        )
        self.assertEqual(result["direct"], result["transformed"])
        self.assertEqual(result["direct"], Fraction(3, 2))

    def test_invalid_abel_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.discrete_abel_interval((Fraction(1),), (), 0, 0)
        with self.assertRaises(ValueError):
            m.discrete_abel_interval(
                (Fraction(1),), (Fraction(1),), 1, 0
            )


class CrossCovarianceTests(unittest.TestCase):
    def setUp(self):
        self.small = (Fraction(2), Fraction(-1), Fraction(1), Fraction(-2))
        self.large = (Fraction(3), Fraction(0), Fraction(-1), Fraction(-2))

    def test_character_and_residue_cross_covariance_agree(self):
        residue = m.residue_cross_covariance(self.small, self.large)
        character = m.character_cross_covariance_mod_five(
            self.small, self.large
        )
        self.assertEqual(residue, 36)
        self.assertEqual(character, GaussianRational(Fraction(36)))

    def test_polarization_is_exact(self):
        result = m.polarization_cross_covariance(self.small, self.large)
        self.assertEqual(
            result["combined_energy"]
            - result["small_energy"]
            - result["large_energy"],
            2 * result["cross"],
        )

    def test_uncentered_vectors_fail_closed(self):
        with self.assertRaises(ValueError):
            m.residue_cross_covariance(
                (Fraction(1), Fraction(0)),
                (Fraction(0), Fraction(0)),
            )


class TransferTests(unittest.TestCase):
    def test_project_abel_transfer_factor(self):
        self.assertEqual(
            m.abel_cross_transfer_factor(Fraction(1, 100)),
            Fraction(201, 100),
        )
        self.assertEqual(
            m.project_abel_transfer_upper(
                Fraction(1, 1000), Fraction(1, 100)
            ),
            Fraction(201, 100000),
        )

    def test_negative_transfer_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.abel_cross_transfer_factor(Fraction(-1, 100))


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.finite_abel_identity_exact)
        self.assertTrue(diagnostic.residue_character_cross_identity_exact)
        self.assertTrue(diagnostic.polarization_identity_exact)
        self.assertFalse(diagnostic.vaughan_source_is_mixed_fixed_modulus_theorem)
        self.assertFalse(diagnostic.harper_source_is_prescribed_fixed_modulus_theorem)
        self.assertFalse(diagnostic.cross_scale_covariance_closed)

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
