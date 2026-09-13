"""Fail-closed checks for the corrected Jutila (3.6) terminal interface."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl7_terminal_interface import (
    BV_COEFFICIENT_NUMERATOR_BOUND,
    BV_LOG_PRODUCT_NUMERATOR_BOUND,
    OFF_DIAGONAL_BASE_MARGIN,
    OFF_DIAGONAL_LOG_GATE,
    THEOREM_ONE_PRIME_COEFFICIENT,
    THEOREM_ONE_PRIME_TAU,
    THETA_MAX,
    WEIGHT_QUOTIENT_BOUND,
    build_diagnostic,
    bv_corollary_coefficient,
    integration_area_factor,
    off_diagonal_base_exponent,
    off_diagonal_total_exponent,
    theorem_one_density_bv_coefficient,
    theorem_one_density_bv_coefficient_simplified,
    theorem_one_density_bv_log_product,
    theorem_one_density_log_ratio,
    theorem_one_density_safe_bv_log_bound,
    theorem_one_density_tau,
    weight_denominator_quotient,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_terminal_v1.json"
)
PREDECESSOR_LEDGER = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_Lemma4_8_v1.json"
)


class DepR09JutilaJL7TerminalInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR_LEDGER.read_text(encoding="utf-8"))
        mp.mp.dps = 100

    def test_source_hashes_and_sizes_when_audit_copy_present(self):
        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["audit_copy_locator"]
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
                self.assertEqual(
                    hashlib.sha256(data).hexdigest(),
                    source["audit_copy_sha256"],
                    source["key"],
                )

    def test_fixed_tau_scope_is_theorem_one_prime_only(self):
        self.assertEqual(THEOREM_ONE_PRIME_TAU, Fraction(8, 5))
        self.assertEqual(
            bv_corollary_coefficient(THEOREM_ONE_PRIME_TAU),
            THEOREM_ONE_PRIME_COEFFICIENT,
        )
        specialization = self.predecessor["actual_bv_specialization"]
        self.assertEqual(specialization["scope_id"], "JL4-T1PRIME-ACTUAL")
        self.assertFalse(specialization["applies_to_equation_3_6"])
        self.assertEqual(specialization["tau"], "8/5")

    def test_theta_specialization_exact_identities(self):
        expected = {
            Fraction(1, 1000): Fraction(123412143347, 16900000),
            Fraction(1, 100): Fraction(1579221647, 1900000),
            Fraction(1, 21): Fraction(921495783, 3500000),
        }
        for theta, coefficient in expected.items():
            self.assertEqual(
                theorem_one_density_tau(theta),
                (1 + 16 * theta) / (1 + 14 * theta),
            )
            self.assertEqual(theorem_one_density_bv_coefficient(theta), coefficient)
            self.assertEqual(
                theorem_one_density_bv_coefficient_simplified(theta),
                coefficient,
            )

    def test_exact_global_theta_bounds(self):
        for denominator in range(22, 5000, 17):
            theta = Fraction(1, denominator)
            coefficient = theorem_one_density_bv_coefficient(theta)
            self.assertLess(theta * coefficient, BV_COEFFICIENT_NUMERATOR_BOUND)
            self.assertLessEqual(
                off_diagonal_base_exponent(theta),
                -OFF_DIAGONAL_BASE_MARGIN * theta,
            )
        self.assertEqual(THETA_MAX, Fraction(1, 21))

    def test_log_ratio_and_weighted_sum_safe_envelope(self):
        for theta in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 21)):
            for L in (mp.mpf("200"), mp.mpf("100000"), mp.mpf("1e20")):
                exact_ratio = theorem_one_density_log_ratio(theta, L)
                direct_ratio = (
                    (1 + 12 * mp.mpf(theta.numerator) / theta.denominator) * L
                    + 2 * mp.log(L)
                ) / (mp.mpf(theta.numerator) / theta.denominator * L)
                self.assertTrue(mp.almosteq(exact_ratio, direct_ratio))
                product = theorem_one_density_bv_log_product(theta, L)
                safe = theorem_one_density_safe_bv_log_bound(theta)
                safe_mp = mp.mpf(safe.numerator) / safe.denominator
                self.assertLess(product, safe_mp)
                self.assertEqual(safe, BV_LOG_PRODUCT_NUMERATOR_BOUND / theta**2)

    def test_weight_denominator_quotient_stays_below_five(self):
        for scale in (mp.mpf("4"), mp.mpf("10"), mp.mpf("1e6")):
            z1 = mp.mpf("100")
            x = scale * z1
            split = mp.sqrt(x * z1)
            for n in (z1 * (1 + mp.mpf("1e-20")), split, x):
                quotient = weight_denominator_quotient(
                    n=n,
                    x=x,
                    z1=z1,
                    smoothing_N=x,
                    smoothing_M=z1,
                )
                self.assertLess(quotient, WEIGHT_QUOTIENT_BOUND)
        with self.assertRaises(ValueError):
            weight_denominator_quotient(
                n=101,
                x=300,
                z1=100,
                smoothing_N=300,
                smoothing_M=100,
            )

    def test_area_and_off_diagonal_gate(self):
        for theta in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 21)):
            L = mp.mpf("100000")
            theta_mp = mp.mpf(theta.numerator) / theta.denominator
            self.assertGreaterEqual(integration_area_factor(theta, L), theta_mp**2 / 2)
            self.assertLessEqual(4 * mp.log(L) / L, mp.mpf(OFF_DIAGONAL_LOG_GATE.numerator) / OFF_DIAGONAL_LOG_GATE.denominator)
            self.assertLessEqual(
                off_diagonal_total_exponent(theta, L),
                -mp.mpf(OFF_DIAGONAL_LOG_GATE.numerator)
                / OFF_DIAGONAL_LOG_GATE.denominator
                * theta_mp,
            )

    def test_diagnostic_and_machine_ledger_fail_closed(self):
        diagnostic = build_diagnostic(theta=Fraction(1, 100), log_D="100000")
        self.assertTrue(diagnostic.theta_scope_bound_holds)
        self.assertTrue(diagnostic.log_gate_holds)
        self.assertTrue(diagnostic.off_diagonal_decay_certified_by_gate)
        for value in (
            diagnostic.contour_multiplier_explicit,
            diagnostic.residue_well_spacing_multiplier_explicit,
            diagnostic.terminal_density_closed,
            diagnostic.pap_11_closed,
            diagnostic.dep_r09_closed,
            diagnostic.fixed_2e_minus_17_independently_certified,
            diagnostic.threshold_calculator_ready,
            diagnostic.numerical_x_cert_ready,
            diagnostic.actual_prime_computation_run,
            diagnostic.source_theorem_local_axiom_used,
            diagnostic.proof_escape_used,
        ):
            self.assertFalse(value)

        self.assertEqual(
            self.ledger["outcome"],
            "EQUATION_3_6_PARAMETER_REPAIRED_WEIGHTED_CALL_EXPLICIT_TERMINAL_MULTIPLIERS_OPEN",
        )
        self.assertEqual(
            self.ledger["status"]["jl4_theorem_one_density_actual"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT_SOURCE_REPLACEMENT",
        )
        for key in (
            "contour_multiplier_explicit",
            "residue_well_spacing_multiplier_explicit",
            "terminal_density_closed",
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


if __name__ == "__main__":
    unittest.main()
