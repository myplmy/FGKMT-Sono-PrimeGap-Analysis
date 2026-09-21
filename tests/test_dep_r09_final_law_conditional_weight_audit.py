"""Exact tests for the DEP-R09 final-law conditional-weight audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_final_law_conditional_weight_audit as m


class ReweightedAtomTests(unittest.TestCase):
    def test_reweighted_atom_and_source_cap_are_exact(self):
        observed = m.reweighted_atom_probability(
            Fraction(1, 12), Fraction(3, 4), Fraction(1, 2)
        )
        upper = m.proof_law_nonempty_atom_cap(
            Fraction(1, 12), Fraction(2)
        )
        self.assertEqual(observed, Fraction(2, 9))
        self.assertEqual(upper, Fraction(1, 3))
        self.assertLessEqual(observed, upper)

    def test_bad_reweighted_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.reweighted_atom_probability(
                Fraction(1, 2), Fraction(0), Fraction(1, 2)
            )
        with self.assertRaises(ValueError):
            m.reweighted_atom_probability(
                Fraction(1), Fraction(1, 2), Fraction(1, 2)
            )
        with self.assertRaises(TypeError):
            m.proof_law_nonempty_atom_cap(
                Fraction(1, 12), 2  # type: ignore[arg-type]
            )


class CoverageAndChainTests(unittest.TestCase):
    def test_coverage_forces_nonempty_edges_with_ceil(self):
        self.assertEqual(m.minimum_nonempty_edges(10, 3, 2), 4)
        self.assertEqual(m.minimum_nonempty_edges(10, 10, 2), 0)
        self.assertEqual(m.minimum_nonempty_edges(9, 4, 5), 1)

    def test_adaptive_conditional_chain_needs_no_global_independence(self):
        result = m.sequential_output_atom_probability(
            (
                Fraction(2, 9),
                Fraction(1, 4),
                Fraction(1, 3),
                Fraction(1, 5),
                Fraction(2, 5),
                Fraction(1),
            ),
            (True, True, True, True, False, False),
            Fraction(1, 3),
        )
        self.assertEqual(result["probability"], Fraction(1, 675))
        self.assertEqual(result["nonempty_count"], 4)
        self.assertEqual(result["cap_power"], Fraction(1, 81))
        self.assertTrue(result["obeys_cap"])

    def test_chain_rejects_nonempty_atom_above_cap(self):
        with self.assertRaises(ValueError):
            m.sequential_output_atom_probability(
                (Fraction(1, 2),), (True,), Fraction(1, 3)
            )
        with self.assertRaises(TypeError):
            m.sequential_output_atom_probability(
                (Fraction(1, 3),), (1,), Fraction(1, 3)  # type: ignore[arg-type]
            )


class ResidueLiftTests(unittest.TestCase):
    def test_nonempty_edge_determines_residue_and_empty_maps_zero(self):
        self.assertEqual(m.residue_from_output_edge((7, 13, 19), 3), 1)
        self.assertEqual(m.residue_from_output_edge((), 3), 0)

    def test_invalid_full_residue_edge_fails_closed(self):
        with self.assertRaises(ValueError):
            m.residue_from_output_edge((7, 11), 3)
        with self.assertRaises(ValueError):
            m.residue_from_output_edge((3, 6), 3)
        with self.assertRaises(ValueError):
            m.residue_from_output_edge((7, 7), 3)


class ShiftAtomAndEntropyTests(unittest.TestCase):
    def test_event_shift_cap_and_effective_denominator(self):
        atom = m.event_shift_atom_upper(6, Fraction(1, 3), 4)
        effective = m.effective_atom_denominator(6, Fraction(1, 3), 4)
        self.assertEqual(atom, Fraction(1, 486))
        self.assertEqual(effective, 486)
        self.assertEqual(atom * effective, 1)

    def test_project_scale_entropy_coefficients_are_exact(self):
        upper = m.guaranteed_effective_entropy_log_coefficient_upper()
        lower = m.full_primorial_log_coefficient_lower()
        self.assertEqual(upper, Fraction(3823, 512000))
        self.assertEqual(lower, Fraction(49, 50))
        self.assertLess(upper, Fraction(1, 100))
        self.assertLess(upper, lower)

    def test_invalid_shift_cap_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.event_shift_atom_upper(0, Fraction(1, 3), 4)
        with self.assertRaises(ValueError):
            m.event_shift_atom_upper(6, Fraction(1, 3), -1)
        with self.assertRaises(ValueError):
            m.effective_atom_denominator(6, Fraction(0), 1)


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.nonempty_edge_atom_cap_exact)
        self.assertTrue(diagnostic.covering_success_forces_nonempty_edge_floor)
        self.assertTrue(diagnostic.same_law_event_shift_atom_cap_exact)
        self.assertTrue(diagnostic.guaranteed_effective_entropy_is_subprimorial)
        self.assertFalse(
            diagnostic.generic_large_sieve_certificate_can_close_new_gate
        )
        self.assertFalse(diagnostic.actual_same_law_analytic_moment_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)

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
