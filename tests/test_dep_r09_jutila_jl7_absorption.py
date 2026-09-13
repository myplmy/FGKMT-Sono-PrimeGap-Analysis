"""Fail-closed tests for the Jutila JL7 strict terminal absorption."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl7_absorption import (
    RESIDUE_MULTIPLIER,
    absorption_fraction_upper,
    absorption_log_cutoff,
    absorption_ratio,
    absorption_rational_fallback_cutoff,
    build_diagnostic,
    elementary_contour_lemma3_multiplier,
    exact_half_margin_terminal_bound,
    off_diagonal_decay_rate,
    off_diagonal_log_gate_holds,
    preterminal_multiplier,
    rational_detector_lower,
    selected_system_coefficient,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_absorption_v1.json"
)
PREDECESSOR_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_residue_v1.json"
)


class DepR09JutilaJL7AbsorptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR_PATH.read_text(encoding="utf-8"))

    def test_machine_ledger_advances_only_actual_absorption_scope(self):
        self.assertTrue(self.predecessor["residue_well_spacing_multiplier_explicit"])
        self.assertFalse(self.predecessor["terminal_density_closed"])
        self.assertTrue(self.ledger["jl7_absorb_actual_selected_system_closed"])
        self.assertTrue(self.ledger["actual_nonprincipal_near_one_density_closed"])
        self.assertTrue(self.ledger["terminal_density_closed"])
        self.assertFalse(self.ledger["printed_full_jutila_theorem_one_closed"])
        for key in (
            "averaged_primitive_density_closed",
            "pap_11_closed",
            "dep_r09_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(self.ledger[key], key)
        self.assertIn("JL7-AVERAGED", self.ledger["next_gate"])

    def test_source_hashes_and_sizes_when_local_copy_present(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if not locator:
                continue
            path = REPO_ROOT / locator
            if path.is_file():
                payload = path.read_bytes()
                self.assertEqual(len(payload), source["audit_copy_bytes"], source["key"])
                self.assertEqual(
                    hashlib.sha256(payload).hexdigest(),
                    source["audit_copy_sha256"],
                    source["key"],
                )

    def test_predecessor_artifact_hashes_and_sizes(self):
        for artifact in self.ledger["predecessor_artifacts"]:
            path = REPO_ROOT / artifact["path"]
            payload = path.read_bytes()
            self.assertEqual(len(payload), artifact["bytes"], artifact["path"])
            self.assertEqual(
                hashlib.sha256(payload).hexdigest(),
                artifact["sha256"],
                artifact["path"],
            )

    def test_exact_endpoint_coefficients(self):
        theta = Fraction(1, 21)
        self.assertEqual(preterminal_multiplier(theta), 74970)
        self.assertEqual(elementary_contour_lemma3_multiplier(theta), 136224)
        self.assertEqual(rational_detector_lower(theta), Fraction(4, 147))
        self.assertEqual(off_diagonal_decay_rate(theta), Fraction(29, 5292))
        self.assertEqual(absorption_ratio(theta), 993089345703840)
        self.assertEqual(selected_system_coefficient(theta), 9287613243090)
        self.assertEqual(RESIDUE_MULTIPLIER, 52)

    def test_preterminal_multiplier_is_product_without_duplicate_factor(self):
        for theta in (Fraction(1, 21), Fraction(1, 100), Fraction(1, 1000)):
            self.assertEqual(
                preterminal_multiplier(theta),
                Fraction(5) * Fraction(34) / theta**2,
            )

    def test_logarithmic_cutoff_is_exact_half_margin_boundary_numerically(self):
        mp.mp.dps = 100
        for theta in (Fraction(1, 21), Fraction(1, 100), Fraction(1, 1000)):
            cutoff = absorption_log_cutoff(theta)
            boundary_value = absorption_fraction_upper(theta, cutoff)
            self.assertLess(abs(boundary_value - mp.mpf("0.5")), mp.mpf("1e-90"))
            self.assertLess(absorption_fraction_upper(theta, cutoff + 1), mp.mpf("0.5"))
            self.assertGreater(absorption_fraction_upper(theta, cutoff - 1), mp.mpf("0.5"))

    def test_rational_fallback_is_stronger_than_logarithmic_cutoff(self):
        mp.mp.dps = 100
        for theta in (Fraction(1, 21), Fraction(1, 100), Fraction(1, 1000)):
            fallback = absorption_rational_fallback_cutoff(theta)
            fallback_mp = mp.mpf(fallback.numerator) / fallback.denominator
            self.assertGreater(fallback_mp, absorption_log_cutoff(theta))
            self.assertLess(absorption_fraction_upper(theta, fallback_mp), mp.mpf("0.5"))

    def test_exp_eight_log_gate_and_fail_closed_smaller_value(self):
        mp.mp.dps = 100
        self.assertTrue(off_diagonal_log_gate_holds(mp.exp(8)))
        self.assertFalse(off_diagonal_log_gate_holds(100))

    def test_generic_half_margin_terminal_oracle(self):
        bound = exact_half_margin_terminal_bound(
            A=Fraction(10), B=Fraction(3), E=Fraction(5), J=Fraction(1), Y=Fraction(2)
        )
        self.assertEqual(bound, Fraction(6, 5))
        self.assertLessEqual(Fraction(1), bound)

    def test_generic_oracle_rejects_missing_premises(self):
        with self.assertRaises(ValueError):
            exact_half_margin_terminal_bound(
                A=Fraction(10), B=Fraction(3), E=Fraction(6), J=Fraction(1), Y=Fraction(2)
            )
        with self.assertRaises(ValueError):
            exact_half_margin_terminal_bound(
                A=Fraction(10), B=Fraction(1), E=Fraction(0), J=Fraction(2), Y=Fraction(1)
            )
        with self.assertRaises(TypeError):
            exact_half_margin_terminal_bound(
                A=10, B=Fraction(3), E=Fraction(5), J=Fraction(1), Y=Fraction(2)
            )

    def test_diagnostic_preserves_scope_and_common_cutoff(self):
        diagnostic = build_diagnostic(Fraction(1, 21))
        self.assertEqual(diagnostic.common_cutoff_driver, "JL6_COMMON")
        self.assertTrue(diagnostic.jl6_budget_holds)
        self.assertTrue(diagnostic.off_diagonal_log_gate_holds)
        self.assertTrue(diagnostic.half_margin_holds_at_common)
        self.assertTrue(diagnostic.contour_area_counted_once)
        self.assertFalse(diagnostic.residue_area_recounted)
        self.assertFalse(diagnostic.parity_factor_inserted_inside_one_system_absorption)
        self.assertTrue(diagnostic.jl7_absorb_actual_selected_system_closed)
        self.assertTrue(diagnostic.actual_nonprincipal_near_one_density_closed)
        self.assertFalse(diagnostic.printed_full_jutila_theorem_one_closed)
        self.assertFalse(diagnostic.numerical_values_are_directed_interval_certificates)
        self.assertFalse(diagnostic.numerical_x_cert_ready)

    def test_input_validation_is_fail_closed(self):
        for theta in (Fraction(0), Fraction(-1, 100), Fraction(1, 20)):
            with self.subTest(theta=theta):
                with self.assertRaises(ValueError):
                    absorption_ratio(theta)
        with self.assertRaises(TypeError):
            preterminal_multiplier(0.01)  # type: ignore[arg-type]
        for bad_log in (0, -1, "nan", "inf"):
            with self.subTest(log_D=bad_log):
                with self.assertRaises(ValueError):
                    absorption_fraction_upper(Fraction(1, 21), bad_log)


if __name__ == "__main__":
    unittest.main()
