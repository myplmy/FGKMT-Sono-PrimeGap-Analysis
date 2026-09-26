"""Exact tests for the DEP-R09 blind residue-discrepancy reduction."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_blind_residue_discrepancy as m


class CharacterTransformTests(unittest.TestCase):
    def setUp(self):
        self.masses = {
            1: Fraction(7),
            2: Fraction(2),
            3: Fraction(5),
            4: Fraction(11),
        }

    def test_inverse_transform_and_reality_are_exact(self):
        self.assertTrue(m.inverse_transform_holds_mod_five(self.masses))
        blind = m.blind_weights_mod_five(self.masses)
        discrepancy = m.residue_discrepancies_mod_five(self.masses)
        for residue, weight in blind.items():
            self.assertEqual(weight.imag, 0)
            self.assertEqual(weight.real, discrepancy[residue])

    def test_parseval_and_selected_mean_are_exact(self):
        self.assertTrue(m.parseval_holds_mod_five(self.masses))
        blind = m.blind_weights_mod_five(self.masses)
        observed = blind[1].real + blind[3].real
        expected = m.subset_mean_discrepancy_mod_five(
            self.masses, (1, 3)
        )
        self.assertEqual(observed, expected)

    def test_invalid_residue_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.character_sums_mod_five({1: Fraction(1)})
        with self.assertRaises(ValueError):
            m.subset_mean_discrepancy_mod_five(self.masses, (1, 1))
        bad = dict(self.masses)
        bad[2] = Fraction(-1)
        with self.assertRaises(ValueError):
            m.blind_weights_mod_five(bad)


class PointwiseEnvelopeTests(unittest.TestCase):
    def test_endpoint_coefficients_are_exact(self):
        self.assertEqual(
            m.brun_titchmarsh_prime_coefficient(Fraction(21)),
            Fraction(21, 10),
        )
        envelope = m.blind_pointwise_envelope(
            Fraction(21), Fraction(1, 10), Fraction(1, 20)
        )
        self.assertEqual(envelope["progression"], Fraction(11, 5))
        self.assertEqual(envelope["principal"], Fraction(11, 10))
        self.assertEqual(envelope["blind_weight"], Fraction(11, 5))

    def test_invalid_envelope_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.brun_titchmarsh_prime_coefficient(Fraction(1))
        with self.assertRaises(ValueError):
            m.blind_pointwise_envelope(
                Fraction(21), Fraction(-1, 10), Fraction(1, 20)
            )


class NormalizedMomentTests(unittest.TestCase):
    def test_normalized_pair_factor_and_certificate(self):
        factor = m.normalized_pair_factor(
            Fraction(1, 5), Fraction(1, 100), Fraction(1, 1000), 1000
        )
        self.assertEqual(factor, Fraction(5049, 1000000))
        certificate = m.normalized_moment_certificate(
            Fraction(1, 10000),
            Fraction(11, 5),
            Fraction(1, 5),
            Fraction(1, 100),
            Fraction(1, 1000),
            1000,
        )
        self.assertEqual(
            certificate,
            Fraction(1, 100000000) + Fraction(121, 25) * factor,
        )

    def test_pair_factor_tends_to_beta_not_beta_rho_m(self):
        rho = Fraction(1, 5)
        alpha = Fraction(1, 100)
        beta = Fraction(1, 1000)
        small = m.normalized_pair_factor(rho, alpha, beta, 1000)
        large = m.normalized_pair_factor(rho, alpha, beta, 1_000_000)
        self.assertLess(abs(large - beta), abs(small - beta))
        self.assertGreater(large, beta)

    def test_invalid_moment_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.normalized_pair_factor(
                Fraction(0), Fraction(0), Fraction(0), 10
            )
        with self.assertRaises(TypeError):
            m.normalized_pair_factor(
                Fraction(1, 2), Fraction(0), Fraction(0), True
            )


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.finite_character_inverse_transform_exact)
        self.assertTrue(diagnostic.blind_weights_are_real_residue_discrepancies)
        self.assertTrue(
            diagnostic.pair_dimension_loss_reduces_to_beta_at_large_vertex_count
        )
        self.assertFalse(diagnostic.sparse_selected_residue_mean_numerically_small)
        self.assertFalse(diagnostic.blind_same_law_moment_closed)

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
