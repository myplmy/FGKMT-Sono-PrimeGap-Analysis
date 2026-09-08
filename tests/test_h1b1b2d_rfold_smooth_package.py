"""Regression tests for the H1b-1b-2d smooth r-fold package."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1a_explicit_package import cutoff_psi, cutoff_psi_derivative
from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L737_CANONICAL,
    APPLICATION_L905_W_PRIME,
    APPLICATION_L1096_W0,
    MAYNARD_APPLICATION_EXCLUSION_IDS,
)
from source.h1b1b2d_rfold_smooth_package import (
    APPLICATION_MODE_H_SQUARE_BYPASS_SCALAR_OPEN,
    APPLICATION_MODE_SHARP_SUMMATORY,
    APPLICATION_MODE_SMOOTH_COMPOSED,
    MAYNARD_APPLICATION_SMOOTH_SPECS,
    PROFILE_N,
    PROFILE_N2,
    PROFILE_NW,
    PROFILE_W,
    PROFILE_W2,
    WIDE_SUPPORT_FIRST_APPLICATIONS,
    application_kappa_sum,
    application_kappa_term_families,
    common_smooth_gate_certificate,
    exact_product_relative_error,
    maximum_tensor_support_exponent,
    product_relative_error_upper,
    profile_norm_certificate,
    rfold_error_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json"
)


def _profile_value_and_derivative(k: int, profile: str, t: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    cert = profile_norm_certificate(k, profile)
    spec = cert.spec
    psi = cutoff_psi(t / spec.support_scale)
    psi_derivative = cutoff_psi_derivative(t / spec.support_scale) / spec.support_scale
    denominator = 1 + cert.t_k * t
    value = psi**spec.psi_power / denominator**spec.denominator_power
    derivative = (
        spec.psi_power
        * psi ** (spec.psi_power - 1)
        * psi_derivative
        / denominator**spec.denominator_power
        - spec.denominator_power
        * cert.t_k
        * psi**spec.psi_power
        / denominator ** (spec.denominator_power + 1)
    )
    return value, derivative


class RfoldSmoothPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_all_source_traced_applications_are_fail_closed_classified(self) -> None:
        rows = MAYNARD_APPLICATION_SMOOTH_SPECS
        self.assertEqual(len(rows), 11)
        self.assertEqual({row.application_id for row in rows}, MAYNARD_APPLICATION_EXCLUSION_IDS)
        counts = {
            mode: sum(row.mode == mode for row in rows)
            for mode in {
                APPLICATION_MODE_SMOOTH_COMPOSED,
                APPLICATION_MODE_SHARP_SUMMATORY,
                APPLICATION_MODE_H_SQUARE_BYPASS_SCALAR_OPEN,
            }
        }
        self.assertEqual(counts[APPLICATION_MODE_SMOOTH_COMPOSED], 8)
        self.assertEqual(counts[APPLICATION_MODE_SHARP_SUMMATORY], 2)
        self.assertEqual(counts[APPLICATION_MODE_H_SQUARE_BYPASS_SCALAR_OPEN], 1)

    def test_actual_profile_integral_and_scaled_c1_bounds(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 60
            for profile in (PROFILE_N, PROFILE_N2, PROFILE_W, PROFILE_W2, PROFILE_NW):
                cert = profile_norm_certificate(36, profile)
                support = cert.spec.support_scale
                integral = mp.quad(
                    lambda t: _profile_value_and_derivative(36, profile, t)[0],
                    [0, mp.mpf("0.9") * support, support],
                )
                self.assertGreaterEqual(integral, cert.integral_lower_bound)
                sampled_scaled_c1 = max(
                    abs(value) + support * abs(derivative)
                    for value, derivative in (
                        _profile_value_and_derivative(
                            36,
                            profile,
                            support * sample / 400,
                        )
                        for sample in range(401)
                    )
                )
                self.assertLessEqual(
                    sampled_scaled_c1,
                    cert.scaled_c1_numerator_upper_bound,
                )
        finally:
            mp.mp.dps = old_dps

    def test_tensor_families_preserve_wide_first_order_and_support_gate(self) -> None:
        families = application_kappa_term_families(36, APPLICATION_L737_CANONICAL)
        self.assertEqual(len(families), 2)
        self.assertEqual(len(families[0]), 36)
        self.assertEqual(len(families[1]), 36)
        self.assertIn(APPLICATION_L737_CANONICAL, WIDE_SUPPORT_FIRST_APPLICATIONS)
        for k in (36, 50, 100, 1000):
            self.assertLessEqual(maximum_tensor_support_exponent(k), k)

    def test_exact_and_numeric_product_envelopes(self) -> None:
        deltas = (Fraction(1, 10), Fraction(1, 20), Fraction(1, 30))
        expected = (Fraction(11, 10) * Fraction(21, 20) * Fraction(31, 30)) - 1
        self.assertEqual(exact_product_relative_error(deltas), expected)
        with self.assertRaises(ValueError):
            exact_product_relative_error((Fraction(1, 2), -1))  # type: ignore[arg-type]

        families = ((mp.mpf(2), mp.mpf(3)), (mp.mpf(5),))
        value = product_relative_error_upper(
            multiplier_over_log_r=mp.mpf("0.1"),
            kappa_families=families,
        )
        self.assertEqual(value, mp.mpf("0.56"))

    def test_open_and_sharp_calls_cannot_use_smooth_path(self) -> None:
        with self.assertRaisesRegex(ValueError, "direct H smooth path"):
            application_kappa_sum(36, APPLICATION_L905_W_PRIME)
        with self.assertRaisesRegex(ValueError, "sharp-cutoff"):
            application_kappa_sum(36, APPLICATION_L1096_W0)

    def test_common_gate_closes_only_the_registered_smooth_subproblem(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in (36, 100):
                gate = common_smooth_gate_certificate(
                    k=k,
                    alpha="0.01",
                    theta="0.25",
                )
                self.assertTrue(gate.gate_verified)
                self.assertGreaterEqual(gate.log_r_sufficient, mp.sqrt(k) * mp.log(2))
                self.assertFalse(gate.all_actual_calls_closed)
                self.assertFalse(gate.siv_07_closed)
                self.assertFalse(gate.x_cert_ready)

            cert = rfold_error_certificate(
                application_id=APPLICATION_L737_CANONICAL,
                k=36,
                alpha="0.01",
                theta="0.25",
                log_r=common_smooth_gate_certificate(
                    k=36,
                    alpha="0.01",
                    theta="0.25",
                ).log_r_sufficient,
            )
            self.assertTrue(cert.linearization_gate_passed)
            self.assertLessEqual(cert.product_error_upper_bound, cert.exponential_error_upper_bound)
            self.assertLessEqual(cert.exponential_error_upper_bound, cert.linearized_error_upper_bound)
            self.assertFalse(cert.theorem_claimed)
            self.assertFalse(cert.siv_07_closed)
            self.assertFalse(cert.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_invalid_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            common_smooth_gate_certificate(k=35, alpha="0.01", theta="0.25")
        with self.assertRaises(ValueError):
            common_smooth_gate_certificate(k=36, alpha="0.01", theta=1)
        with self.assertRaises(ValueError):
            product_relative_error_upper(multiplier_over_log_r=True, kappa_families=((mp.mpf(1),),))

    def test_contract_provenance_and_parent_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "SMOOTH_RFOLD_SUBPACKAGE_PARAMETERIZED_EXPLICIT_ACTUAL_PACKAGE_OPEN",
        )
        self.assertEqual(contract["application_counts"]["source_traced_total"], 11)
        self.assertEqual(contract["application_counts"]["smooth_profile_closed"], 8)
        self.assertEqual(contract["application_counts"]["lemma84_smooth_closed"], 7)
        self.assertEqual(contract["application_counts"]["sharp_parameterized"], 2)
        self.assertEqual(contract["application_counts"]["h_square_bypass_scalar_open"], 1)
        self.assertTrue(contract["generic_distinct_profile_composition_closed"])
        self.assertFalse(contract["all_actual_lemma84_calls_closed"])
        self.assertFalse(contract["siv_07_closed"])
        self.assertFalse(contract["numerical_x_cert_ready"])
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["new_python_dependency_required"])
        self.assertFalse(contract["lean_required_for_this_gate"])

        for source in contract["source_registry"]:
            if "local_path" not in source:
                continue
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source["sha256"])

        parent = contract["parent_status"]
        self.assertEqual(parent["H1B-L83"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")
        self.assertEqual(parent["H1B-L84"], "RATE_MISSING")
        self.assertEqual(parent["H1B1-PACKAGE"], "HARD_BLOCKER")
        self.assertEqual(parent["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(parent["X_cert"], "OPEN")


if __name__ == "__main__":
    unittest.main()
