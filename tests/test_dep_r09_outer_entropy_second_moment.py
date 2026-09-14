"""Exact tests for the DEP-R09 outer-entropy moment reduction."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_outer_entropy_second_moment as m


class OuterAtomTests(unittest.TestCase):
    def test_outer_denominator_and_cap_are_exact(self):
        self.assertEqual(m.outer_atom_denominator((2, 3, 5, 7)), 210)
        self.assertEqual(m.outer_atom_cap((2, 3, 5, 7)), Fraction(1, 210))

    def test_adaptive_inner_toy_obeys_outer_atom_cap(self):
        diagnostic = m.outer_atom_toy_diagnostic()
        self.assertEqual(diagnostic.modulus, 30)
        self.assertEqual(diagnostic.outer_vectors, 6)
        self.assertEqual(diagnostic.final_shift_atoms, 6)
        self.assertEqual(diagnostic.maximum_atom, "1/6")
        self.assertTrue(diagnostic.atom_cap_exact)

    def test_invalid_outer_moduli_fail_closed(self):
        with self.assertRaises(ValueError):
            m.outer_atom_denominator(())
        with self.assertRaises(ValueError):
            m.outer_atom_denominator((2, 2))
        with self.assertRaises(ValueError):
            m.outer_atom_denominator((2, 9))
        with self.assertRaises(TypeError):
            m.outer_atom_denominator((2, True))


class FiniteConvolutionTests(unittest.TestCase):
    def test_exact_gaussian_cauchy_bound(self):
        values = (
            m.GaussianRational(Fraction(1), Fraction(2)),
            m.GaussianRational(Fraction(-3, 5), Fraction(1, 7)),
            m.GaussianRational(Fraction(4, 9), Fraction(-2, 3)),
            m.GaussianRational(Fraction(0), Fraction(5, 11)),
        )
        for offsets in ((0,), (0, 1), (1, 3, 5), (-2, 0, 2, 4)):
            observed = m.cyclic_shift_sum_energy(values, offsets)
            upper = m.cyclic_cauchy_energy_upper(values, offsets)
            self.assertLessEqual(observed, upper)

    def test_constant_sequence_attains_the_n_squared_bound(self):
        values = tuple(
            m.GaussianRational(Fraction(2), Fraction(-1)) for _ in range(5)
        )
        offsets = (0, 2, 7)
        self.assertEqual(
            m.cyclic_shift_sum_energy(values, offsets),
            m.cyclic_cauchy_energy_upper(values, offsets),
        )

    def test_invalid_convolution_inputs_fail_closed(self):
        value = m.GaussianRational(Fraction(1))
        with self.assertRaises(ValueError):
            m.cyclic_shift_sum_energy((), (0,))
        with self.assertRaises(ValueError):
            m.cyclic_shift_sum_energy((value,), ())
        with self.assertRaises(TypeError):
            m.cyclic_shift_sum_energy((value,), (False,))
        with self.assertRaises(TypeError):
            m.GaussianRational(Fraction(1), 0)  # type: ignore[arg-type]


class MomentGateTests(unittest.TestCase):
    def test_raw_moment_and_strict_gate_are_exact(self):
        upper = m.same_law_raw_moment_upper(8, 3, Fraction(17, 5), 6)
        self.assertEqual(upper, Fraction(204, 5))
        threshold = m.character_energy_gate(
            Fraction(1, 2),
            Fraction(3, 5),
            6,
            Fraction(10),
            Fraction(7),
            8,
            3,
        )
        self.assertEqual(threshold, Fraction(245, 4))
        self.assertTrue(
            m.passes_strict_character_energy_gate(Fraction(61), threshold)
        )
        self.assertFalse(
            m.passes_strict_character_energy_gate(threshold, threshold)
        )

    def test_invalid_gate_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.same_law_raw_moment_upper(8, 0, Fraction(1), 6)
        with self.assertRaises(ValueError):
            m.same_law_raw_moment_upper(8, 3, Fraction(-1), 6)
        with self.assertRaises(TypeError):
            m.character_energy_gate(
                Fraction(1, 2), Fraction(1, 2), 6, Fraction(1), 1, 8, 3
            )


class SourceBenchmarkTests(unittest.TestCase):
    def test_davenport_erdos_prime_modulus_identity(self):
        for prime in (3, 5, 7, 11, 13):
            for interval_size in range(1, prime):
                self.assertEqual(
                    m.davenport_erdos_shift_energy(prime, interval_size),
                    prime * interval_size - interval_size**2,
                )

    def test_davenport_contract_fails_closed(self):
        with self.assertRaises(ValueError):
            m.davenport_erdos_shift_energy(9, 2)
        with self.assertRaises(ValueError):
            m.davenport_erdos_shift_energy(7, 7)


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(
            diagnostic.outer_atom_cap_exact_under_adaptive_inner_rule
        )
        self.assertTrue(diagnostic.cyclic_convolution_cauchy_exactly_verified)
        self.assertTrue(
            diagnostic.davenport_erdos_prime_modulus_identity_exactly_verified
        )
        self.assertTrue(diagnostic.same_law_raw_moment_reduction_exact)
        self.assertFalse(
            diagnostic.fully_numerical_fixed_primorial_character_energy_bound_identified
        )
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.bounded_x_cert_range_obtained)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_and_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))
        changed = deepcopy(m.load_ledger())
        changed["source_registry"][0]["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
