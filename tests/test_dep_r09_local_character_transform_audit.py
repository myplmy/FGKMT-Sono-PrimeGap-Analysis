"""Exact tests for the DEP-R09 local-character-transform audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_local_character_transform_audit as m


class LocalTransformTests(unittest.TestCase):
    def test_quadratic_level_set_has_small_atoms_but_transform_one(self):
        distribution = m.quadratic_level_set_distribution(
            prime=11, offset=0, target=1
        )
        self.assertEqual(len(distribution), 5)
        self.assertEqual(max(distribution.values()), Fraction(1, 5))
        self.assertEqual(
            m.quadratic_local_transform(
                distribution, prime=11, offset=0
            ),
            1,
        )

    def test_stage_transform_is_exact(self):
        self.assertEqual(
            m.stage_transform_from_atoms(
                (Fraction(1, 6), Fraction(1, 3), Fraction(1, 2)),
                (1, -1, 0),
            ),
            Fraction(-1, 6),
        )

    def test_invalid_transform_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.quadratic_level_set_distribution(
                prime=9, offset=0, target=1
            )
        with self.assertRaises(ValueError):
            m.quadratic_local_transform(
                {1: Fraction(1, 2)}, prime=11, offset=0
            )
        with self.assertRaises(ValueError):
            m.stage_transform_from_atoms(
                (Fraction(1),), (2,)
            )


class BlindEnergyTests(unittest.TestCase):
    def test_blind_energy_decomposition_is_exact(self):
        self.assertEqual(
            m.blind_character_energy(4, 3),
            {"total": 12, "principal": 9, "nonprincipal": 3},
        )
        self.assertEqual(
            m.blind_character_energy(8, 0),
            {"total": 0, "principal": 0, "nonprincipal": 0},
        )

    def test_blind_cauchy_gate_is_strictly_normalized(self):
        gate = m.blind_cauchy_gate(
            Fraction(1, 2), 3, Fraction(5), 8
        )
        self.assertEqual(gate, Fraction(15, 4))

    def test_invalid_blind_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.blind_character_energy(4, 5)
        with self.assertRaises(ValueError):
            m.blind_cauchy_gate(
                Fraction(1, 2), 4, Fraction(5), 4
            )
        with self.assertRaises(TypeError):
            m.blind_character_energy(4.0, 3)  # type: ignore[arg-type]


class ScaleTests(unittest.TestCase):
    def test_fixed_modulus_log_gap_is_exact(self):
        self.assertEqual(
            m.fixed_modulus_log_coefficient_lower(),
            Fraction(47, 100),
        )


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertFalse(diagnostic.atom_cap_implies_uniform_fourier_saving)
        self.assertEqual(diagnostic.level_set_transform, "1")
        self.assertTrue(diagnostic.blind_total_coefficient_energy_exact)
        self.assertFalse(
            diagnostic.gkm_theorem_is_actual_multidimensional_reweighted_transform
        )
        self.assertFalse(
            diagnostic.applicable_numerical_local_transform_theorem_identified
        )
        self.assertFalse(diagnostic.blind_prime_error_correlation_closed)
        self.assertFalse(diagnostic.dep_r09_closed)

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
