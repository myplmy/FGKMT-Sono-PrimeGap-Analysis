"""Fail-closed tests for the Theory-83 large-sieve barrier audit."""

from __future__ import annotations

from copy import deepcopy
import unittest

import mpmath as mp

from source import dep_r09_fixed_primorial_variance_barrier as m


class ArithmeticEnvelopeTests(unittest.TestCase):
    def test_euler_phi_is_exact_for_diagnostic_primorials(self):
        expected = {
            1: 1,
            3: 2,
            30: 8,
            210: 48,
            2310: 480,
            30030: 5760,
            510510: 92160,
        }
        for value, phi_value in expected.items():
            self.assertEqual(m.euler_phi(value), phi_value)

    def test_dusart_half_interval_is_stronger_than_one_quarter(self):
        with mp.workdps(100):
            self.assertGreater(
                m.dusart_coefficient_from_log_y(8),
                mp.mpf(1) / 4,
            )
            for q in (3, 30, 210, 2310, 30030, 510510):
                for d in (m.D_MIN, m.D_MAX):
                    coefficient = m.dusart_half_interval_coefficient(q, d)
                    self.assertGreater(coefficient, mp.mpf(1) / 4)
                    _, log_y = m.log_scales(q, d)
                    source_lower = m.lambda_square_sum_lower_over_y(q, d)
                    coarse_lower = (log_y - mp.log(2)) / 4
                    self.assertGreater(source_lower, coarse_lower)

    def test_best_atom_gate_is_below_rosser_envelope(self):
        with mp.workdps(100):
            for q in (3, 30, 210, 2310, 30030, 510510):
                self.assertLess(
                    m.best_possible_entropy_gate_upper_over_y2(q),
                    m.rosser_entropy_gate_upper_over_y2(q),
                )

    def test_direct_large_sieve_rhs_is_above_the_gate_envelope(self):
        with mp.workdps(100):
            for q in (3, 30, 210, 2310, 30030, 510510):
                for d in (m.D_MIN, m.D_MAX):
                    self.assertGreater(m.direct_large_sieve_barrier_margin(q, d), 0)


class StrictCertificateLogicTests(unittest.TestCase):
    def test_certificate_must_be_strictly_below_gate(self):
        self.assertTrue(m.upper_certificate_implies_strict_gate(9, 10))
        self.assertFalse(m.upper_certificate_implies_strict_gate(10, 10))
        self.assertFalse(m.upper_certificate_implies_strict_gate(11, 10))

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.euler_phi(0)
        with self.assertRaises(TypeError):
            m.euler_phi(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            m.log_scales(2, m.D_MIN)
        with self.assertRaises(ValueError):
            m.log_scales(3, m.D_MIN - 1)
        with self.assertRaises(ValueError):
            m.dusart_coefficient_from_log_y(mp.log(2))
        with self.assertRaises(ValueError):
            m.upper_certificate_implies_strict_gate(-1, 1)
        with self.assertRaises(ValueError):
            m.upper_certificate_implies_strict_gate(0, 0)


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        before = mp.mp.dps
        diagnostic = m.build_diagnostic()
        self.assertEqual(mp.mp.dps, before)
        self.assertTrue(diagnostic.dusart_log8_coefficient_exceeds_one_quarter)
        self.assertTrue(diagnostic.dusart_coefficient_exceeds_one_quarter)
        self.assertTrue(diagnostic.sample_primorial_margins_all_positive)
        self.assertTrue(diagnostic.montgomery_vaughan_primary_constant_crosschecked)
        self.assertFalse(diagnostic.direct_large_sieve_rhs_can_certify_theory82_gate)
        self.assertFalse(diagnostic.actual_character_energy_lower_bound_claimed)
        self.assertFalse(diagnostic.fixed_primorial_natural_variance_theorem_identified)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.bounded_x_cert_range_obtained)
        self.assertFalse(diagnostic.threshold_calculator_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_and_local_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))

        changed = deepcopy(m.load_ledger())
        pinned = next(
            source
            for source in changed["source_registry"]
            if source.get("key") == "MONTGOMERY_VAUGHAN1973"
        )
        pinned["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
