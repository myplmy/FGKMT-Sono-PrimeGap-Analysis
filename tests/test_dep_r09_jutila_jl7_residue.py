"""Fail-closed tests for the Jutila JL7 principal-residue envelope."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl7_residue import (
    DIAGONAL_R_SUM_COEFFICIENT,
    RESIDUE_MULTIPLIER,
    RESIDUE_ROW_COEFFICIENT,
    SPACING_ROW_COEFFICIENT,
    THETA_MAX,
    build_diagnostic,
    cancelled_residue_pair,
    diagonal_r_sum,
    diagonal_r_sum_envelope,
    excluded_prime_ratio_product,
    interval_lengths,
    ladder_kernel,
    ladder_kernel_by_quadrature,
    ladder_mass_at_zero,
    local_excluded_prime_ratio,
    phi_over_q,
    residue_coefficient_at_theta,
    residue_intervals,
    selected_height_inverse_square_row,
    spacing_row_envelope,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_residue_v1.json"
)
PREDECESSOR_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_Lemma3_v1.json"
)


class DepR09JutilaJL7ResidueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 70
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR_PATH.read_text(encoding="utf-8"))

    def test_machine_ledger_advances_only_the_residue_gate(self):
        self.assertTrue(self.predecessor["jutila_lemma3_multiplier_explicit"])
        self.assertFalse(self.predecessor["residue_well_spacing_multiplier_explicit"])
        self.assertTrue(self.ledger["jutila_lemma3_multiplier_explicit"])
        self.assertTrue(self.ledger["residue_well_spacing_multiplier_explicit"])
        self.assertEqual(self.ledger["residue_composition"]["calculator_safe_multiplier"], 52)
        for key in (
            "terminal_density_closed",
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
        self.assertIn("JL7-ABSORB", self.ledger["next_gate"])

    def test_source_hash_and_size_when_audit_copy_present(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if not locator:
                continue
            path = REPO_ROOT / locator
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), source["audit_copy_sha256"])

    def test_exact_rational_coefficients(self):
        self.assertEqual(THETA_MAX, Fraction(1, 21))
        self.assertEqual(SPACING_ROW_COEFFICIENT, Fraction(10, 3))
        self.assertEqual(RESIDUE_ROW_COEFFICIENT, 91)
        self.assertEqual(DIAGONAL_R_SUM_COEFFICIENT, 12)
        self.assertEqual(RESIDUE_MULTIPLIER, 52)
        self.assertEqual(12 * 91, 1092)
        self.assertEqual(Fraction(1092, 1) * THETA_MAX, RESIDUE_MULTIPLIER)

    def test_actual_interval_geometry_at_hard_endpoint(self):
        theta = mp.mpf(1) / 21
        log_d = mp.mpf(441)
        a, b, c, d = residue_intervals(theta, log_d)
        length_a, length_b = interval_lengths(theta, log_d)
        self.assertLessEqual(length_a, mp.mpf(5) / 6 * theta * log_d)
        self.assertLessEqual(length_b, mp.mpf(18) / 7 * theta * log_d)
        self.assertGreater(c, b)
        self.assertLess(d - a, 3 * log_d)
        self.assertLess(ladder_mass_at_zero(theta, log_d), 7 * theta**2 * log_d**3)

    def test_closed_ladder_kernel_matches_independent_quadrature(self):
        theta = mp.mpf(1) / 21
        log_d = mp.mpf(441)
        for z in (mp.mpc("0.02", "0.3"), mp.mpc("0.07", "-0.55")):
            with self.subTest(z=z):
                closed = ladder_kernel(z, theta, log_d)
                oracle = ladder_kernel_by_quadrature(z, theta, log_d)
                self.assertLess(abs(closed - oracle), mp.mpf("1e-45") * max(1, abs(oracle)))

    def test_zero_removable_value_and_gamma_cancellation(self):
        theta = mp.mpf(1) / 21
        log_d = mp.mpf(441)
        self.assertEqual(
            ladder_kernel(0, theta, log_d),
            mp.mpc(ladder_mass_at_zero(theta, log_d)),
        )
        z = mp.mpc("0.03", "0.4")
        a, b, c, d = residue_intervals(theta, log_d)
        original = mp.gamma(-z) * mp.quad(
            lambda xi: mp.quad(
                lambda eta: mp.exp(-xi * z) - mp.exp(-eta * z), [c, d]
            ),
            [a, b],
        )
        self.assertLess(
            abs(original - cancelled_residue_pair(z, theta, log_d)),
            mp.mpf("1e-45") * max(1, abs(original)),
        )

    def test_well_spaced_height_rows_stay_below_basel_envelope(self):
        log_d = mp.mpf(441)
        delta = 1 / log_d
        heights = tuple((index - 25) * delta for index in range(51))
        for row_index in (0, 1, 25, 49, 50):
            row = selected_height_inverse_square_row(heights, row_index, log_d)
            self.assertLess(row, spacing_row_envelope(log_d))
        with self.assertRaises(ValueError):
            selected_height_inverse_square_row((0, delta / 2), 0, log_d)

    def test_rankin_excluded_prime_product_and_finite_r_sum(self):
        log_d = mp.mpf(441)
        for modulus_q in (1, 2, 6, 30, 210):
            with self.subTest(modulus_q=modulus_q):
                product = excluded_prime_ratio_product(modulus_q, log_d)
                self.assertLessEqual(product, mp.e)
                finite_sum = diagonal_r_sum(100, modulus_q)
                finite_mp = mp.mpf(finite_sum.numerator) / finite_sum.denominator
                self.assertLess(finite_mp, diagonal_r_sum_envelope(modulus_q, log_d))
        self.assertEqual(phi_over_q(1), Fraction(1, 1))
        self.assertEqual(phi_over_q(30), Fraction(4, 15))

    def test_local_excluded_prime_ratio_obeys_exponential_bound(self):
        lambda_value = mp.mpf(1) / 441
        for prime in (2, 3, 5, 11, 101):
            ratio = local_excluded_prime_ratio(prime, lambda_value)
            self.assertLessEqual(ratio, mp.exp(lambda_value * mp.log(prime) / (prime - 1)))

    def test_endpoint_residue_coefficient_is_exactly_52(self):
        self.assertEqual(residue_coefficient_at_theta(THETA_MAX), mp.mpf(52))
        self.assertLess(residue_coefficient_at_theta(Fraction(1, 22)), 52)

    def test_diagnostic_is_positive_and_fail_closed_downstream(self):
        diagnostic = build_diagnostic()
        self.assertTrue(diagnostic.interval_geometry_verified)
        self.assertTrue(diagnostic.diagonal_r_sum_verified)
        self.assertTrue(diagnostic.excluded_prime_product_verified)
        self.assertTrue(diagnostic.residue_well_spacing_multiplier_explicit)
        self.assertEqual(diagnostic.residue_multiplier, 52)
        self.assertFalse(diagnostic.terminal_density_closed)
        self.assertFalse(diagnostic.averaged_primitive_density_closed)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)

    def test_input_validation_is_fail_closed(self):
        for bad_theta in (0, -1, Fraction(1, 20), mp.inf):
            with self.subTest(theta=bad_theta):
                with self.assertRaises(ValueError):
                    residue_intervals(bad_theta, 441)
        with self.assertRaises(ValueError):
            residue_intervals(Fraction(1, 21), 440)
        with self.assertRaises(ValueError):
            phi_over_q(0)
        with self.assertRaises(ValueError):
            local_excluded_prime_ratio(1, Fraction(1, 441))


if __name__ == "__main__":
    unittest.main()
