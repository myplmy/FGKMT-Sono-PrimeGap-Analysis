"""Exact tests for the DEP-R09 same-law outer-fiber minimax audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_same_law_outer_fiber_audit as m


class OuterFiberReductionTests(unittest.TestCase):
    def test_toy_fiber_and_full_energies_are_exact(self):
        matrix = m.toy_energy_matrix()
        self.assertEqual(m.outer_fiber_maximum_energy(matrix), Fraction(154))
        self.assertEqual(m.full_support_energy(matrix), Fraction(324))
        self.assertLess(
            m.outer_fiber_maximum_energy(matrix),
            m.full_support_energy(matrix),
        )

    def test_arbitrary_event_subprobability_obeys_fiber_envelope(self):
        matrix = m.toy_energy_matrix()
        masses = tuple(
            tuple(
                Fraction((row + 2 * column) % 4, 20)
                for column in range(5)
            )
            for row in range(6)
        )
        for row in masses:
            self.assertLessEqual(sum(row, Fraction(0)), 1)
        observed = m.outer_uniform_event_raw_moment(matrix, masses)
        self.assertLessEqual(observed, m.outer_fiber_raw_moment_upper(matrix))

    def test_adaptive_maximizer_attains_abstract_envelope(self):
        matrix = m.toy_energy_matrix()
        law = m.maximizing_conditional_law(matrix)
        self.assertTrue(all(sum(row, Fraction(0)) == 1 for row in law))
        self.assertEqual(
            m.outer_uniform_event_raw_moment(matrix, law),
            Fraction(77, 3),
        )
        self.assertEqual(
            m.outer_uniform_event_raw_moment(matrix, law),
            m.outer_fiber_raw_moment_upper(matrix),
        )

    def test_zero_event_has_zero_raw_moment(self):
        matrix = m.toy_energy_matrix()
        zero = tuple(tuple(Fraction(0) for _ in row) for row in matrix)
        self.assertEqual(m.outer_uniform_event_raw_moment(matrix, zero), 0)


class CRTFiberTests(unittest.TestCase):
    def test_crt_fibers_partition_modulo_thirty(self):
        desired = m.toy_energy_matrix()
        by_residue = [Fraction(0) for _ in range(30)]
        for residue in range(30):
            by_residue[residue] = desired[residue % 6][residue % 5]
        self.assertEqual(m.crt_fiber_matrix(6, 5, by_residue), desired)

    def test_invalid_crt_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.crt_fiber_matrix(6, 4, tuple(Fraction(0) for _ in range(24)))
        with self.assertRaises(ValueError):
            m.crt_fiber_matrix(6, 5, tuple(Fraction(0) for _ in range(29)))
        with self.assertRaises(TypeError):
            m.crt_fiber_matrix(6, 5, tuple(Fraction(0) for _ in range(29)) + (0,))


class StrictGateTests(unittest.TestCase):
    def test_outer_fiber_gate_and_boundary_are_exact(self):
        threshold = m.outer_fiber_energy_gate(
            Fraction(1, 2),
            Fraction(3, 5),
            6,
            Fraction(2),
            Fraction(3),
        )
        self.assertEqual(threshold, Fraction(162, 5))
        self.assertTrue(
            m.passes_strict_outer_fiber_gate(Fraction(32), threshold)
        )
        self.assertFalse(
            m.passes_strict_outer_fiber_gate(threshold, threshold)
        )

    def test_invalid_energy_and_mass_inputs_fail_closed(self):
        matrix = m.toy_energy_matrix()
        with self.assertRaises(ValueError):
            m.outer_fiber_maximum_energy(())
        with self.assertRaises(ValueError):
            m.outer_fiber_maximum_energy(((Fraction(-1),),))
        with self.assertRaises(ValueError):
            m.outer_uniform_event_raw_moment(
                matrix,
                tuple(tuple(Fraction(1) for _ in row) for row in matrix),
            )
        with self.assertRaises(TypeError):
            m.outer_fiber_energy_gate(
                Fraction(1, 2), Fraction(1, 2), 6, Fraction(1), 1
            )


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.support_restricted_outer_fiber_envelope_exact)
        self.assertTrue(
            diagnostic.adaptive_deterministic_selector_attains_abstract_envelope
        )
        self.assertTrue(
            diagnostic.toy_fiber_bound_strictly_below_full_energy_bound
        )
        self.assertFalse(diagnostic.actual_fmt_law_attains_the_abstract_envelope_claimed)
        self.assertFalse(diagnostic.actual_fiber_energy_analytic_upper_identified)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)

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
