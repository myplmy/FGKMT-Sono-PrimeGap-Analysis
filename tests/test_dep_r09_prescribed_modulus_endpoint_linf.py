"""Exact tests for the prescribed-modulus endpoint L-infinity transfer."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_prescribed_modulus_endpoint_linf as m


class CenteredMassTests(unittest.TestCase):
    def test_centered_l1_envelope(self):
        result = m.centered_l1_envelope(
            (Fraction(2), Fraction(0), Fraction(3), Fraction(0))
        )
        self.assertEqual(result["total"], 5)
        self.assertLessEqual(result["l1_norm"], result["envelope"])
        self.assertEqual(result["envelope"], 10)

    def test_negative_mass_fails_closed(self):
        with self.assertRaises(ValueError):
            m.centered_residue_masses((Fraction(1), Fraction(-1)))

    def test_linf_cross_envelope(self):
        result = m.linf_cross_envelope(
            (Fraction(2), Fraction(0), Fraction(3), Fraction(0)),
            (Fraction(1), Fraction(-2), Fraction(3), Fraction(-2)),
        )
        self.assertEqual(result["cross"], 44)
        self.assertEqual(result["envelope"], 120)
        self.assertLessEqual(result["absolute_cross"], result["envelope"])

    def test_uncentered_interval_error_fails_closed(self):
        with self.assertRaises(ValueError):
            m.linf_cross_envelope(
                (Fraction(1), Fraction(0)),
                (Fraction(1), Fraction(0)),
            )


class NormalizationTests(unittest.TestCase):
    def test_prime_count_half_lower(self):
        self.assertEqual(
            m.prime_count_half_lower(Fraction(16), Fraction(2)),
            14,
        )
        with self.assertRaises(ValueError):
            m.prime_count_half_lower(Fraction(16), Fraction(9))

    def test_small_scale_ratio_is_21_over_10(self):
        self.assertEqual(m.small_scale_mass_ratio_upper(), Fraction(21, 10))

    def test_source_range_exponents(self):
        result = m.source_range_exponent_diagnostic(21)
        self.assertEqual(result["current_modulus_exponent"], "1/21")
        self.assertTrue(result["below_square_root_exponent"])
        self.assertTrue(result["below_two_thirds_exponent"])


class EndpointTransferTests(unittest.TestCase):
    def test_endpoint_and_project_multipliers(self):
        endpoint = Fraction(1, 1000)
        correction = Fraction(1, 100000)
        self.assertEqual(
            m.endpoint_interval_epsilon(endpoint, correction),
            Fraction(101, 100000),
        )
        self.assertEqual(
            m.endpoint_linf_kappa(endpoint, correction),
            Fraction(2121, 500000),
        )
        self.assertEqual(
            m.project_delta_upper(
                endpoint, correction, Fraction(1, 100)
            ),
            Fraction(426321, 50000000),
        )

    def test_negative_endpoint_input_fails_closed(self):
        with self.assertRaises(ValueError):
            m.endpoint_linf_kappa(Fraction(-1), Fraction(0))


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.centered_l1_envelope_exact)
        self.assertTrue(diagnostic.linf_cross_envelope_exact)
        self.assertFalse(
            diagnostic.vaughan_i_is_prescribed_fixed_modulus_theorem
        )
        self.assertFalse(
            diagnostic.harper_dyadic_range_contains_current_modulus
        )
        self.assertFalse(diagnostic.centered_endpoint_linf_gate_closed)

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
