"""Fail-closed tests for the DEP-R09 C_J loss-tree audit."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_cj_loss_tree import (
    ABSORPTION_DENOMINATOR,
    EXACT_AREA_ENDPOINT,
    RATIONAL_DETECTOR_ENDPOINT,
    THETA_ENDPOINT,
    TIGHT_DENOMINATOR,
    TIGHT_RESIDUE_ENDPOINT,
    absorption_margin_factor,
    baseline_factor_product,
    baseline_selected_system_coefficient,
    build_diagnostic,
    counterfactual_theta_power_coefficient,
    endpoint_preterminal_upper,
    endpoint_residue_row_upper,
    endpoint_residue_upper,
    endpoint_weighted_square_upper,
    near_kernel_per_cj,
    pap_cj_budget_cap,
    rz_barban_vehov_coefficient,
    tightened_absorption_log_cutoff,
    tightened_selected_system_coefficient,
    weight_denominator_quotient,
    weight_denominator_rho_supremum,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_CJ_loss_tree_v1.json"
)


class DepR09CJLossTreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_baseline_factorization_is_exact(self):
        baseline = baseline_selected_system_coefficient(THETA_ENDPOINT)
        self.assertEqual(baseline, 9_287_613_243_090)
        self.assertEqual(baseline_factor_product(THETA_ENDPOINT), baseline)
        self.assertEqual(baseline // counterfactual_theta_power_coefficient(THETA_ENDPOINT), 108_290)

    def test_exact_endpoint_source_coefficients(self):
        self.assertEqual(
            rz_barban_vehov_coefficient(THETA_ENDPOINT),
            Fraction(921495783, 3500000),
        )
        self.assertEqual(
            endpoint_weighted_square_upper(),
            Fraction(15665428311, 1750000),
        )
        self.assertEqual(
            endpoint_preterminal_upper(),
            Fraction(15665428311, 1093750),
        )
        self.assertEqual(TIGHT_DENOMINATOR, Fraction(8, 5))
        self.assertEqual(endpoint_residue_row_upper(), Fraction(2840, 1197))
        self.assertEqual(endpoint_residue_upper(), TIGHT_RESIDUE_ENDPOINT)
        self.assertEqual(TIGHT_RESIDUE_ENDPOINT, Fraction(710, 171))
        self.assertEqual(RATIONAL_DETECTOR_ENDPOINT, Fraction(4, 147))
        self.assertEqual(EXACT_AREA_ENDPOINT, Fraction(55, 18522))

    def test_weight_denominator_bound_on_dense_grid(self):
        mp.mp.dps = 80
        for rho in (mp.mpf(4), mp.mpf(10), mp.mpf(1000), mp.mpf("1e20")):
            lower = 1 / rho
            previous = None
            for index in range(101):
                t = lower + (1 - lower) * index / 100
                value = weight_denominator_quotient(rho, t)
                self.assertLess(value, mp.mpf(8) / 5)
                if previous is not None:
                    self.assertLessEqual(value, previous)
                previous = value
            self.assertEqual(weight_denominator_rho_supremum(rho), weight_denominator_quotient(rho, lower))
        self.assertLess(mp.e / (mp.e - 1), mp.mpf(8) / 5)

    def test_tightened_coefficient_is_exact_and_still_huge(self):
        tightened = tightened_selected_system_coefficient()
        self.assertEqual(absorption_margin_factor(), Fraction(1_000_000, 999_999))
        self.assertEqual(tightened, Fraction(11503697604450072, 425315))
        baseline = baseline_selected_system_coefficient(THETA_ENDPOINT)
        gain = mp.mpf(baseline.numerator) / baseline.denominator / (
            mp.mpf(tightened.numerator) / tightened.denominator
        )
        self.assertGreater(gain, 343)
        self.assertLess(gain, 344)
        self.assertGreater(tightened, 27_000_000_000)

    def test_absorption_cutoff_matches_one_over_million_boundary(self):
        mp.mp.dps = 100
        cutoff = tightened_absorption_log_cutoff()
        cpre = mp.mpf(endpoint_preterminal_upper().numerator) / endpoint_preterminal_upper().denominator
        cbar = mp.mpf(RATIONAL_DETECTOR_ENDPOINT.numerator) / RATIONAL_DETECTOR_ENDPOINT.denominator
        gamma = mp.mpf(29) / 5292
        fraction = 36 * cpre * 136224 * mp.exp(-gamma * cutoff) / cbar**2
        self.assertLess(abs(fraction - mp.mpf(1) / ABSORPTION_DENOMINATOR), mp.mpf("1e-90"))

    def test_pap_budget_gap_remains_after_all_local_tightening(self):
        mp.mp.dps = 100
        cap = pap_cj_budget_cap()
        tightened = tightened_selected_system_coefficient()
        tightened_mp = mp.mpf(tightened.numerator) / tightened.denominator
        self.assertLess(cap, mp.mpf("0.059"))
        self.assertGreater(cap, mp.mpf("0.058"))
        self.assertGreater(tightened_mp / cap, mp.mpf("4.62e11"))
        self.assertLess(tightened_mp / cap, mp.mpf("4.63e11"))
        self.assertGreater(
            mp.mpf(counterfactual_theta_power_coefficient(THETA_ENDPOINT)) / cap,
            mp.mpf("1.46e9"),
        )

    def test_near_kernel_is_positive_and_scales_linearly_in_cj(self):
        mp.mp.dps = 80
        kernel = near_kernel_per_cj()
        self.assertGreater(kernel, 0)
        diagnostic = build_diagnostic()
        baseline = mp.mpf(diagnostic.baseline_selected_system_coefficient)
        tightened = mp.mpf(Fraction(diagnostic.tightened_selected_system_coefficient).numerator) / Fraction(
            diagnostic.tightened_selected_system_coefficient
        ).denominator
        self.assertLess(abs(mp.mpf(diagnostic.baseline_near_limit) - baseline * kernel), mp.mpf("1e-45"))
        self.assertLess(abs(mp.mpf(diagnostic.tightened_near_limit) - tightened * kernel), mp.mpf("1e-45"))

    def test_machine_ledger_preserves_scope_and_source_hashes(self):
        status = self.ledger["status_after_this_gate"]
        self.assertTrue(status["cj_loss_tree_factorized"])
        self.assertTrue(status["finite_safe_local_tightening_derived"])
        self.assertTrue(status["structural_proof_change_required_for_credible_progress"])
        self.assertFalse(status["local_tightening_passes_pap_gate"])
        self.assertFalse(status["source_replacement_logically_proved_necessary"])
        for key in (
            "pap_11_closed",
            "dep_r09_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(status[key], key)
        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["audit_copy_locator"]
            payload = path.read_bytes()
            self.assertEqual(len(payload), source["audit_copy_bytes"], source["key"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), source["audit_copy_sha256"], source["key"])

    def test_diagnostic_matches_machine_values(self):
        diagnostic = build_diagnostic()
        machine = self.ledger["endpoint_diagnostic_theta_1_over_21"]
        self.assertEqual(diagnostic.baseline_selected_system_coefficient, machine["baseline_CJ"])
        self.assertEqual(diagnostic.tightened_selected_system_coefficient, machine["finite_safe_tightened_CJ"])
        self.assertEqual(diagnostic.pap_cj_budget_cap_exp_minus_2, machine["CJ_cap_for_exp_minus_2"])
        self.assertFalse(diagnostic.local_tightening_passes_pap_gate)
        self.assertFalse(diagnostic.contour_lemma3_changes_asymptotic_cj)
        self.assertFalse(diagnostic.counterfactual_scaling_is_impossibility_theorem)
        self.assertFalse(diagnostic.numerical_x_cert_ready)

    def test_input_validation_fails_closed(self):
        for bad_theta in (Fraction(0), Fraction(-1, 2), Fraction(1, 20)):
            with self.subTest(theta=bad_theta):
                with self.assertRaises(ValueError):
                    baseline_selected_system_coefficient(bad_theta)
        with self.assertRaises(TypeError):
            baseline_selected_system_coefficient(0.1)  # type: ignore[arg-type]
        for bad_m in (1, 0, -2):
            with self.assertRaises(ValueError):
                absorption_margin_factor(bad_m)
        with self.assertRaises(TypeError):
            absorption_margin_factor(2.5)  # type: ignore[arg-type]
        for rho, t in ((3, 1 / 3), (4, 0.1), (4, 2)):
            with self.assertRaises(ValueError):
                weight_denominator_quotient(rho, t)


if __name__ == "__main__":
    unittest.main()
