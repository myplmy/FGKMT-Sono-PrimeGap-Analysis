"""Exact fail-closed tests for the FMT construction-law mass audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_fmt_construction_mass as m


class TwoStageMassTests(unittest.TestCase):
    def test_exact_mass_and_failure_identity(self):
        f_out = Fraction(1, 5)
        f_in = Fraction(1, 4)
        self.assertEqual(
            m.two_stage_sieve_success_lower(f_out, f_in),
            Fraction(3, 5),
        )
        self.assertEqual(
            m.two_stage_sieve_failure_upper(f_out, f_in),
            Fraction(2, 5),
        )
        self.assertEqual(
            m.two_stage_sieve_failure_upper(f_out, f_in),
            f_out + (1 - f_out) * f_in,
        )

    def test_independence_is_not_used(self):
        diagnostic = m.build_diagnostic()
        self.assertFalse(diagnostic.independence_required_for_mass_product)
        self.assertTrue(
            diagnostic.project_joint_sieve_good_mass_parameterized_explicit
        )

    def test_strict_joint_boundary(self):
        f_out = Fraction(1, 5)
        f_in = Fraction(1, 4)
        sieve_mass = Fraction(3, 5)
        self.assertTrue(
            m.joint_selection_certified(
                f_out, f_in, sieve_mass - Fraction(1, 100)
            )
        )
        self.assertFalse(
            m.joint_selection_certified(f_out, f_in, sieve_mass)
        )
        self.assertEqual(
            m.joint_good_mass_lower(f_out, f_in, Fraction(7, 10)),
            0,
        )

    def test_fiberwise_route_is_distinct(self):
        self.assertTrue(
            m.fiberwise_selection_certified(
                Fraction(99, 100),
                Fraction(2, 5),
                Fraction(1, 2),
            )
        )
        self.assertFalse(
            m.fiberwise_selection_certified(
                Fraction(1, 10),
                Fraction(2, 5),
                Fraction(3, 5),
            )
        )

    def test_markov_bound(self):
        self.assertEqual(
            m.markov_failure_upper(Fraction(3, 20), Fraction(1, 2)),
            Fraction(3, 10),
        )
        self.assertEqual(
            m.markov_failure_upper(Fraction(2), Fraction(1, 2)),
            1,
        )

    def test_invalid_inputs_fail_closed(self):
        for value in (Fraction(-1, 10), Fraction(1), Fraction(11, 10)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                m.two_stage_sieve_success_lower(value, Fraction(1, 2))
        with self.assertRaises(TypeError):
            m.two_stage_sieve_success_lower(0.1, Fraction(1, 2))
        with self.assertRaises(ValueError):
            m.markov_failure_upper(Fraction(1), Fraction(0))


class LedgerTests(unittest.TestCase):
    def test_ledger_and_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_fail_closed_status(self):
        diagnostic = m.build_diagnostic()
        self.assertFalse(
            diagnostic.printed_fmt_probability_rates_numerically_explicit
        )
        self.assertFalse(
            diagnostic.weighted_correlation_same_joint_law_failure_bound_available
        )
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))
        changed = deepcopy(m.load_ledger())
        changed["source_registry"][0]["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
