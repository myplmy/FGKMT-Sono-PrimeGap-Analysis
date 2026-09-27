"""Exact tests for the DEP-R09 conductor-weighted character dual audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_conductor_weighted_dual as m


class ArithmeticTests(unittest.TestCase):
    def test_divisors_phi_and_mobius(self):
        self.assertEqual(m.divisors(30), (1, 2, 3, 5, 6, 10, 15, 30))
        self.assertEqual(m.euler_phi(30), 8)
        self.assertEqual(m.mobius(30), -1)
        self.assertEqual(m.mobius(12), 0)

    def test_invalid_arithmetic_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.divisors(0)
        with self.assertRaises(ValueError):
            m.euler_phi(-1)


class ConductorEnergyTests(unittest.TestCase):
    def test_primitive_level_partition_is_exact(self):
        residues = (7, 11, 13)
        partition = m.conductor_energy_partition(30, residues)
        self.assertEqual(
            partition,
            {1: 9, 2: 0, 3: 1, 5: 3, 6: 0, 10: 0, 15: 11, 30: 0},
        )
        self.assertEqual(sum(partition.values()), 8 * 3)
        self.assertEqual(sum(v for r, v in partition.items() if r > 1), 15)
        self.assertEqual(
            15, m.expected_nonprincipal_coefficient_energy(30, 3)
        )

    def test_collision_formula_handles_repeated_classes(self):
        self.assertEqual(m.residue_collision_count((1, 4, 7), 3), 9)
        self.assertEqual(m.residue_collision_count((1, 2, 3), 3), 3)

    def test_nonreduced_residue_fails_closed(self):
        with self.assertRaises(ValueError):
            m.conductor_energy_partition(30, (2, 7))
        with self.assertRaises(ValueError):
            m.expected_nonprincipal_coefficient_energy(30, 9)


class SourceRangeAndCertificateTests(unittest.TestCase):
    def test_large_and_small_axis_source_ranges_are_distinct(self):
        self.assertTrue(
            m.prime_large_sieve_range_holds(Fraction(21), Fraction(1))
        )
        self.assertFalse(
            m.small_prime_large_sieve_range_holds(
                Fraction(1, 1000), Fraction(1)
            )
        )

    def test_optimistic_separate_l2_certificate_exceeds_one(self):
        self.assertEqual(
            m.separate_l2_normalized_square(30, 3, Fraction(1)),
            Fraction(5, 3),
        )
        self.assertGreater(
            m.separate_l2_normalized_square(30, 3, Fraction(1)), 1
        )

    def test_invalid_source_parameters_fail_closed(self):
        with self.assertRaises(ValueError):
            m.prime_large_sieve_range_holds(Fraction(21), Fraction(0))
        with self.assertRaises(TypeError):
            m.separate_l2_normalized_square(30, 3, 1)  # type: ignore[arg-type]


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.primitive_energy_partition_exact)
        self.assertTrue(diagnostic.large_prime_axis_source_range_holds)
        self.assertFalse(diagnostic.small_prime_full_modulus_source_range_holds)
        self.assertFalse(diagnostic.source_constants_fully_numerical)
        self.assertFalse(diagnostic.separate_l2_certificate_closes_gate)
        self.assertFalse(diagnostic.weighted_character_product_closed)

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
