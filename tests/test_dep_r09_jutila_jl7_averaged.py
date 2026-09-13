"""Fail-closed checks for Jutila's variable-modulus equation (3.7)."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.dep_r09_jutila_jl7_averaged import (
    PHASE_PAIR_NORMALIZATION,
    averaged_detector_mellin_cutoff,
    averaged_mellin_decay_exponent,
    build_averaged_detector_budget,
    build_diagnostic,
    detector_phase_normalization,
    phase_pair_log_normalization,
    principal_residue_normalization,
)


ROOT = Path(__file__).resolve().parents[1]
LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_averaged_v1.json"
)


class DepR09JutilaJL7AveragedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_source_hashes_and_reading_modes(self):
        for source in self.ledger["source_registry"]:
            path = ROOT / source["audit_copy_locator"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(path.stat().st_size, source["audit_copy_bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["audit_copy_sha256"],
            )
            if source["native_text_bytes"] <= 18:
                self.assertIn("OCR_ONLY_AS_LOCATOR", source["reading_mode"])
                self.assertTrue(source["rendered_printed_pages_checked"])
            if source["key"] == "JUTILA_1977_ZERO_DENSITY":
                self.assertEqual(
                    source["rendered_printed_pages_checked"],
                    list(range(55, 63)),
                )

    def test_exact_phase_and_principal_residue_cancellation(self):
        for q, phi_q in (
            (Fraction(3), Fraction(2)),
            (Fraction(30), Fraction(8)),
            (Fraction(2310), Fraction(480)),
        ):
            self.assertEqual(detector_phase_normalization(q, phi_q), 1)
            self.assertEqual(principal_residue_normalization(q, phi_q), 1)

    def test_offdiagonal_phase_pair_normalization_boundary(self):
        normalized = phase_pair_log_normalization(
            q_j=Fraction(6),
            phi_j=Fraction(1),
            q_k=Fraction(12),
            phi_k=Fraction(2),
            log_D=Fraction(1),
        )
        self.assertEqual(normalized, PHASE_PAIR_NORMALIZATION)

    def test_normalizations_fail_closed(self):
        with self.assertRaises(ValueError):
            detector_phase_normalization(Fraction(3), Fraction(4))
        with self.assertRaises(ValueError):
            principal_residue_normalization(Fraction(0), Fraction(1))
        with self.assertRaises(ValueError):
            phase_pair_log_normalization(
                q_j=Fraction(7),
                phi_j=Fraction(1),
                q_k=Fraction(6),
                phi_k=Fraction(1),
                log_D=Fraction(1),
            )

    def test_mellin_envelope_uses_the_lower_exponent(self):
        theta = Fraction(1, 21)
        self.assertEqual(averaged_mellin_decay_exponent(theta), Fraction(13, 588))
        averaged = averaged_detector_mellin_cutoff(theta, theta / 4)
        fixed_exponent = theta * (1 + 9 * theta) / 2
        theta_mp = mp.mpf(theta.numerator) / theta.denominator
        fixed_decay_mp = mp.mpf(fixed_exponent.numerator) / fixed_exponent.denominator
        averaged_decay_mp = (
            mp.mpf(averaged_mellin_decay_exponent(theta).numerator)
            / averaged_mellin_decay_exponent(theta).denominator
        )
        self.assertLess(averaged_decay_mp, fixed_decay_mp)
        self.assertGreater(averaged, 0)

    def test_equal_budget_components_and_endpoint(self):
        for theta in (Fraction(1, 21), Fraction(1, 100), Fraction(1, 1000)):
            budget = build_averaged_detector_budget(
                theta=theta,
                eta_output=theta,
                eta_jl5=theta / 4,
                eta_damping=theta / 4,
                eta_mellin=theta / 4,
                eta_tail=theta / 4,
            )
            self.assertTrue(budget.budget_balance_holds)
            self.assertTrue(budget.power_condition_margin_holds)
            self.assertTrue(budget.component_bounds_meet_allocations)
            self.assertGreaterEqual(mp.mpf(budget.sufficient_log_D_cutoff), mp.e)

    def test_budget_rejects_invalid_allocation(self):
        theta = Fraction(1, 21)
        with self.assertRaises(ValueError):
            build_averaged_detector_budget(
                theta=theta,
                eta_output=theta,
                eta_jl5=theta,
                eta_damping=theta,
                eta_mellin=theta,
                eta_tail=theta,
            )

    def test_diagnostic_scope_is_narrow_and_fail_closed(self):
        diagnostic = build_diagnostic()
        self.assertTrue(diagnostic.averaged_uniform_detector_closed)
        self.assertTrue(diagnostic.primitive_principal_pair_diagonalized)
        self.assertTrue(diagnostic.averaged_principal_residue_normalization_closed)
        self.assertTrue(diagnostic.averaged_off_diagonal_multiplier_closed)
        self.assertTrue(diagnostic.averaged_selected_system_terminal_closed)
        self.assertTrue(diagnostic.averaged_nonprincipal_near_one_density_closed)
        self.assertFalse(diagnostic.printed_all_alpha_theorem_one_closed)
        self.assertFalse(diagnostic.gallagher_maier_pap_bridge_closed)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.fixed_2e_minus_17_independently_certified)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.rigorous_interval_certificate)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_machine_ledger_preserves_open_roots(self):
        self.assertEqual(
            self.ledger["outcome"],
            "JL7_AVERAGED_NONPRINCIPAL_NEAR_ONE_PARAMETERIZED_EXPLICIT_PRINTED_ALL_ALPHA_AND_PAP_OPEN",
        )
        status = self.ledger["status_after_this_gate"]
        self.assertTrue(status["averaged_nonprincipal_near_one_density_closed"])
        self.assertFalse(status["printed_all_alpha_theorem_one_closed"])
        self.assertFalse(status["gallagher_maier_pap_bridge_closed"])
        self.assertFalse(status["pap_11_closed"])
        self.assertFalse(status["dep_r09_closed"])
        self.assertFalse(status["fixed_2e_minus_17_independently_certified"])
        self.assertFalse(status["numerical_x_cert_ready"])
        self.assertFalse(status["threshold_calculator_ready"])
        self.assertFalse(status["actual_prime_computation_run"])
        self.assertFalse(status["source_theorem_local_axiom_used"])
        self.assertFalse(status["proof_escape_used"])


if __name__ == "__main__":
    unittest.main()
