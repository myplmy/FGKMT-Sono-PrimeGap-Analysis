"""Exact tests for the DEP-R09 fixed-Q' bilinear reduction."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_fixed_qprime_bilinear as m


class CenteredKernelTests(unittest.TestCase):
    def setUp(self):
        self.modulus = 5
        self.phi = 4
        self.selected = (1, 2)
        self.prime_terms = (
            (1, Fraction(2)),
            (2, Fraction(3)),
            (3, Fraction(5)),
            (6, Fraction(7)),
        )
        self.prime_power_terms = ((4, Fraction(11)), (8, Fraction(13)))

    def test_direct_and_kernel_fixed_means_agree(self):
        terms = self.prime_terms + self.prime_power_terms
        self.assertEqual(
            m.centered_mean_from_terms(
                self.modulus, self.phi, self.selected, terms
            ),
            m.original_fixed_mean(
                self.modulus, self.phi, self.selected, terms
            ),
        )

    def test_prime_prime_power_split_is_exact(self):
        split = m.split_centered_mean(
            self.modulus,
            self.phi,
            self.selected,
            self.prime_terms,
            self.prime_power_terms,
        )
        self.assertEqual(split["prime"], 14)
        self.assertEqual(split["prime_power"], -48)
        self.assertEqual(split["combined"], -34)

    def test_invalid_kernel_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.centered_residue_kernel(4, 5, True)
        with self.assertRaises(ValueError):
            m.centered_mean_from_terms(5, 4, (1, 1), self.prime_terms)
        with self.assertRaises(TypeError):
            m.centered_residue_kernel(4, 2, 1)  # type: ignore[arg-type]


class BilinearReindexTests(unittest.TestCase):
    def test_positive_pair_mass_reindexes_by_unique_residue(self):
        prime_terms = (
            (1, Fraction(2)),
            (2, Fraction(3)),
            (3, Fraction(5)),
            (6, Fraction(7)),
            (12, Fraction(11)),
        )
        reindexed = m.reindex_selected_prime_terms(5, (1, 2), prime_terms)
        self.assertEqual(
            reindexed,
            (
                (1, 0, Fraction(2)),
                (2, 0, Fraction(3)),
                (1, 1, Fraction(7)),
                (2, 2, Fraction(11)),
            ),
        )
        self.assertEqual(
            sum((weight for _, _, weight in reindexed), Fraction(0)),
            m.positive_pair_mass(5, (1, 2), prime_terms),
        )

    def test_centered_bilinear_matches_kernel_prime_component(self):
        prime_terms = (
            (1, Fraction(2)),
            (2, Fraction(3)),
            (3, Fraction(5)),
            (6, Fraction(7)),
        )
        self.assertEqual(
            m.centered_prime_bilinear(5, 4, (1, 2), prime_terms),
            m.centered_mean_from_terms(5, 4, (1, 2), prime_terms),
        )


class CorrectionTests(unittest.TestCase):
    def test_prime_power_envelope_and_relative_transfer(self):
        self.assertEqual(m.prime_power_kernel_envelope(10, 3), 7)
        correction = m.prime_power_correction_upper(10, 3, Fraction(5, 2))
        self.assertEqual(correction, Fraction(35, 2))
        self.assertEqual(
            m.relative_correction_upper(correction, 3, Fraction(7)),
            Fraction(5, 6),
        )

    def test_invalid_correction_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.prime_power_correction_upper(4, 2, Fraction(-1))
        with self.assertRaises(ValueError):
            m.relative_correction_upper(Fraction(1), 0, Fraction(1))


class UpperOnlyBoundaryTests(unittest.TestCase):
    def test_one_sided_upper_does_not_imply_centered_saving(self):
        witness = m.one_sided_upper_countermodel(Fraction(7), Fraction(8))
        self.assertTrue(witness["upper_holds"])
        self.assertEqual(witness["pair_mass"], 0)
        self.assertEqual(witness["centered"], -7)
        self.assertEqual(witness["relative_absolute_error"], 1)

    def test_invalid_upper_model_fails_closed(self):
        with self.assertRaises(ValueError):
            m.one_sided_upper_countermodel(Fraction(0), Fraction(1))


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.centered_kernel_identity_exact)
        self.assertTrue(diagnostic.prime_prime_power_split_exact)
        self.assertTrue(diagnostic.sono_upper_bound_is_one_sided)
        self.assertFalse(diagnostic.r10_direct_drop_in_for_centered_mean)
        self.assertFalse(diagnostic.centered_binary_prime_gate_closed)

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
