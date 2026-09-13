"""Fail-closed checks for the Gallagher--Maier density-integral split."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.dep_r09_gallagher_maier_pap_split import (
    CONSERVATIVE_MCCURLEY_C1,
    bennett_family_zero_upper,
    bennett_per_character_upper,
    bennett_simple_family_upper,
    build_diagnostic,
    density_power_kappa,
    exact_far_density_integral,
    far_budget_log_cutoff,
    far_power_margin,
    far_simple_pap_envelope,
    first_integer_d_meeting_asymptotic_budget,
    near_asymptotic_certificate_limit,
    near_density_integral_envelope,
    near_kernel_margin,
)


ROOT = Path(__file__).resolve().parents[1]
LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Gallagher_Maier_PAP_split_v1.json"
)


class DepR09GallagherMaierPapSplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_source_hashes_and_native_text_policy(self):
        for source in self.ledger["source_registry"]:
            path = ROOT / source["locator"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(path.stat().st_size, source["bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )
            self.assertIn("NATIVE_TEXT", source["reading_mode"])
            self.assertTrue(source["rendered_pages_checked"])

    def test_exact_endpoint_exponents(self):
        theta = Fraction(1, 21)
        d = Fraction(160)
        self.assertEqual(density_power_kappa(theta), 22)
        self.assertEqual(near_kernel_margin(theta, d), Fraction(69, 80))
        self.assertEqual(far_power_margin(theta, d), Fraction(13, 3360))

    def test_bennett_individual_and_family_envelopes(self):
        with mp.workdps(80):
            for Q in (2, 3, 10, 100):
                height = mp.mpf(Q) ** 5
                family = bennett_family_zero_upper(Q, height)
                simple = bennett_simple_family_upper(Q)
                self.assertGreater(family, 0)
                self.assertLessEqual(family, simple)
                for q in range(2, Q + 1):
                    self.assertLessEqual(
                        bennett_per_character_upper(q, height) * Q**2,
                        family,
                    )

    def test_bennett_domain_fails_closed(self):
        self.assertEqual(bennett_family_zero_upper(2, Fraction(5, 7)), 0)
        with self.assertRaises(ValueError):
            bennett_per_character_upper(1, 10)
        with self.assertRaises(ValueError):
            bennett_per_character_upper(2, Fraction(1, 2))
        with self.assertRaises(ValueError):
            bennett_simple_family_upper(Fraction(3, 2))

    def test_far_stieltjes_endpoint_collapses_exactly(self):
        with mp.workdps(80):
            X = mp.mpf(17)
            theta = Fraction(1, 42)
            zeros = mp.mpf(23)
            theta_mp = mp.mpf(theta.numerator) / theta.denominator
            integral = (
                mp.log(X)
                * zeros
                * mp.quad(lambda alpha: X ** (alpha - 1), [0, 1 - theta_mp])
                + zeros / X
            )
            exact = exact_far_density_integral(zeros, X, theta)
            self.assertTrue(mp.almosteq(integral, exact))

    def test_near_piecewise_formula_matches_quadrature(self):
        with mp.workdps(90):
            theta = Fraction(1, 21)
            d = Fraction(160)
            c1 = CONSERVATIVE_MCCURLEY_C1
            u = mp.mpf(250000)
            envelope = near_density_integral_envelope(
                u, theta=theta, d=d, c1=c1
            )
            L = 7 * u / 160
            eta = (mp.mpf(1) / 24) * 160 / (5 * u)
            switch = 1 / L
            A = (mp.mpf(69) / 80) * u - 4 * mp.log(L)
            B = mp.log(2) + L
            coefficient = mp.mpf(9287613243090)
            direct = 2 * coefficient * u * (
                mp.quad(
                    lambda delta: mp.exp(-A * delta) * (3 + B / L),
                    [eta, switch],
                )
                + mp.quad(
                    lambda delta: mp.exp(-A * delta) * (3 + B * delta),
                    [switch, mp.mpf(1) / 21],
                )
            )
            saved = mp.mpf(envelope.exact_integral_upper)
            self.assertLess(abs(saved - direct) / direct, mp.mpf("1e-55"))

    def test_near_branch_order_and_decay_fail_closed(self):
        with self.assertRaises(ValueError):
            near_density_integral_envelope(
                10,
                theta=Fraction(1, 21),
                d=Fraction(160),
                c1=CONSERVATIVE_MCCURLEY_C1,
            )
        with self.assertRaises(ValueError):
            near_kernel_margin(Fraction(1, 21), Fraction(22))
        with self.assertRaises(ValueError):
            far_power_margin(Fraction(1, 21), Fraction(147))

    def test_far_cutoff_meets_one_percent_budget(self):
        theta = Fraction(1, 21)
        d = Fraction(160)
        cutoff = far_budget_log_cutoff(
            theta=theta, d=d, budget=Fraction(1, 100)
        )
        self.assertLessEqual(
            far_simple_pap_envelope(cutoff, theta=theta, d=d),
            mp.mpf("0.01"),
        )

    def test_asymptotic_gate_diagnostics(self):
        theta = Fraction(1, 21)
        c1 = CONSERVATIVE_MCCURLEY_C1
        at_160 = near_asymptotic_certificate_limit(
            theta=theta, d=Fraction(160), c1=c1
        )
        at_186 = near_asymptotic_certificate_limit(
            theta=theta, d=Fraction(186), c1=c1
        )
        self.assertGreater(at_160, mp.mpf("2.7e13"))
        self.assertGreater(at_186, mp.mpf("2.1e13"))
        self.assertEqual(
            first_integer_d_meeting_asymptotic_budget(
                theta=theta, c1=c1, budget=1
            ),
            3856,
        )
        self.assertEqual(
            first_integer_d_meeting_asymptotic_budget(
                theta=theta, c1=c1, budget=mp.exp(-2)
            ),
            4096,
        )

    def test_diagnostic_scope_is_narrow(self):
        diagnostic = build_diagnostic()
        self.assertTrue(diagnostic.bennett_global_zero_count_source_fixed)
        self.assertTrue(diagnostic.far_alpha_branch_parameterized_explicit)
        self.assertTrue(diagnostic.near_alpha_integration_parameterized_explicit)
        self.assertFalse(diagnostic.current_d160_certificate_meets_positive_pap_gate)
        self.assertFalse(
            diagnostic.current_d160_certificate_preserves_sono_exp_minus_two_budget
        )
        self.assertFalse(diagnostic.gallagher_explicit_formula_multiplier_closed)
        self.assertFalse(diagnostic.principal_zeta_branch_closed)
        self.assertFalse(diagnostic.exceptional_character_branch_closed)
        self.assertFalse(diagnostic.psi_to_pi_closed)
        self.assertFalse(diagnostic.gallagher_maier_pap_bridge_closed)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.fixed_2e_minus_17_independently_certified)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.rigorous_interval_certificate)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_machine_ledger_preserves_open_root(self):
        self.assertEqual(
            self.ledger["outcome"],
            "NEAR_FAR_DENSITY_INTEGRAL_SPLIT_PARAMETERIZED_EXPLICIT_CURRENT_D160_CERTIFICATE_INSUFFICIENT_PAP_OPEN",
        )
        status = self.ledger["status_after_this_gate"]
        self.assertTrue(status["far_alpha_branch_parameterized_explicit"])
        self.assertTrue(status["near_alpha_integration_parameterized_explicit"])
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
