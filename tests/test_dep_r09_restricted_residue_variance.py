"""Fail-closed tests for the DEP-R09 restricted-residue variance audit."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_restricted_residue_variance import (
    D_MAX,
    D_MIN,
    build_diagnostic,
    cauchy_alignment_witness,
    hooley_zero_free_boundary,
    legacy_full_moment_budget,
    nonprincipal_character_energy,
    pap_near_budget,
    principal_character_energy,
    principal_separated_nonprincipal_budget,
    separated_over_legacy_budget_ratio,
    total_character_energy,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_restricted_residue_variance_screen_v1.json"
)


class DepR09RestrictedResidueVarianceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_character_energy_decomposition_is_exact(self):
        phi_q = 92_160
        residue_count = 17
        total = total_character_energy(phi_q, residue_count)
        principal = principal_character_energy(residue_count)
        nonprincipal = nonprincipal_character_energy(phi_q, residue_count)
        self.assertEqual(total, phi_q * residue_count)
        self.assertEqual(principal, residue_count**2)
        self.assertEqual(nonprincipal, residue_count * (phi_q - residue_count))
        self.assertEqual(total, principal + nonprincipal)

    def test_principal_separated_budget_ratio_matches_closed_form(self):
        with mp.workdps(100):
            phi_q = 92_160
            residue_count = 17
            epsilon = pap_near_budget()
            y = mp.mpf("12345.5")
            legacy = legacy_full_moment_budget(
                phi_q, residue_count, y, epsilon
            )
            separated = principal_separated_nonprincipal_budget(
                phi_q, residue_count, y, epsilon, 0
            )
            ratio = separated_over_legacy_budget_ratio(
                phi_q, residue_count, epsilon, 0
            )
            self.assertEqual(separated / legacy, ratio)
            self.assertEqual(ratio, mp.mpf(phi_q) / (phi_q - residue_count))

    def test_principal_error_spends_the_square_of_remaining_budget(self):
        with mp.workdps(100):
            phi_q = 100
            residue_count = 7
            epsilon = mp.mpf("0.2")
            ratio = separated_over_legacy_budget_ratio(
                phi_q, residue_count, epsilon, epsilon / 10
            )
            expected = mp.mpf(phi_q) / (phi_q - residue_count) * mp.mpf("0.81")
            self.assertTrue(mp.almosteq(ratio, expected, rel_eps=mp.mpf("1e-95")))

    def test_cauchy_bound_has_an_exact_alignment_equality_case(self):
        lhs, rhs = cauchy_alignment_witness(1234, Fraction(7, 13))
        self.assertEqual(lhs, rhs)

    def test_power_regime_zero_free_boundaries_are_exact(self):
        self.assertEqual(hooley_zero_free_boundary(D_MIN), Fraction(11, 21))
        self.assertEqual(hooley_zero_free_boundary(D_MAX), Fraction(187, 372))

    def test_diagnostic_and_machine_ledger_fail_closed(self):
        before = mp.mp.dps
        diagnostic = build_diagnostic()
        self.assertEqual(mp.mp.dps, before)
        self.assertTrue(diagnostic.energy_decomposition_exact)
        self.assertFalse(
            diagnostic.cauchy_total_energy_constant_improvable_without_extra_structure
        )
        self.assertFalse(
            diagnostic.fully_numerical_fixed_primorial_variance_drop_in_identified
        )
        self.assertFalse(diagnostic.direct_weighted_correlation_theorem_identified)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.threshold_calculator_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

        saved = self.ledger["exact_algebra_diagnostic"]
        for field, value in diagnostic.__dict__.items():
            self.assertEqual(saved[field], value, field)

    def test_machine_ledger_preserves_quantifiers_and_next_target(self):
        self.assertEqual(
            self.ledger["outcome"],
            "NO_NUMERICAL_FIXED_PRIMORIAL_VARIANCE_DROP_IN_TOTAL_CHARACTER_ENERGY_CANNOT_BE_IMPROVED_DIRECT_WEIGHTED_CORRELATION_IS_THE_MINIMAL_OPEN_TARGET",
        )
        status = self.ledger["status_after_this_gate"]
        self.assertTrue(status["maier_formula_i_aggregate_consumer_confirmed"])
        self.assertTrue(status["unweighted_character_energy_subquestion_closed"])
        self.assertTrue(status["full_variance_is_sufficient_but_overstrong"])
        self.assertFalse(status["direct_weighted_correlation_source_identified"])
        self.assertFalse(status["pap_11_closed"])
        self.assertFalse(status["numerical_x_cert_ready"])

    def test_maier_primary_source_hash_is_pinned(self):
        source = next(
            item for item in self.ledger["source_registry"]
            if item["key"] == "MAIER1981"
        )
        path = REPO_ROOT / source["locator"]
        self.assertTrue(path.is_file())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source["sha256"])

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            total_character_energy(10, 10)
        with self.assertRaises(ValueError):
            nonprincipal_character_energy(10, 0)
        with self.assertRaises(ValueError):
            principal_separated_nonprincipal_budget(10, 2, 1, 0.1, 0.1)
        with self.assertRaises(TypeError):
            cauchy_alignment_witness(5, 0.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            hooley_zero_free_boundary(0)


if __name__ == "__main__":
    unittest.main()
