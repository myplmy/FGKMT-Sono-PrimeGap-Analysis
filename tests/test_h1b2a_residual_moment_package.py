"""Regression checks for the H1b-2a residual moment/error package."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import mpmath as mp

from source.h1b1b2d_rfold_smooth_package import common_smooth_gate_certificate
from source.h1b2a_residual_moment_package import (
    H1B2A_MINIMUM_K,
    coefficient_weight_certificate,
    integral_size_certificate,
    proposition94_local_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b2a_residual_moment_error_v1.json"
)


class H1b2aResidualMomentPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_plateau_cube_closes_absolute_integral_lower_bound(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in (36, 100, 1_000, 8_104):
                cert = integral_size_certificate(k)
                self.assertTrue(cert.plateau_gate_passed)
                self.assertTrue(cert.lower_bound_verified)
                self.assertTrue(cert.pointwise_comparisons_verified)
                self.assertGreaterEqual(
                    cert.i_lower_bound,
                    cert.canonical_i_lower_bound,
                )
                self.assertGreater(cert.j_lower_bound, 0)
                self.assertGreaterEqual(cert.i_f2_over_k2_multiplier, 1)
                self.assertGreaterEqual(cert.j_f2_over_k2_multiplier, 1)
                self.assertFalse(cert.theorem_claimed)
                self.assertFalse(cert.siv_07_closed)
                self.assertFalse(cert.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_cube_integral_formula_matches_direct_quadrature(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            cert = integral_size_certificate(36)
            direct = mp.quad(
                lambda t: 1 / (1 + cert.t_k * t) ** 2,
                [0, cert.cube_endpoint],
            )
            self.assertTrue(
                mp.almosteq(direct, cert.cube_one_dimensional_integral)
            )
        finally:
            mp.mp.dps = old_dps

    def test_finite_lemma85_envelope_at_existing_common_gate(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            gate = common_smooth_gate_certificate(
                k=36,
                alpha="0.01",
                theta="0.25",
            )
            cert = coefficient_weight_certificate(
                k=36,
                alpha="0.01",
                theta="0.25",
                log_r=gate.log_r_sufficient,
            )
            self.assertTrue(cert.support_endpoint_gate_passed)
            self.assertTrue(cert.smooth_linearization_gate_passed)
            self.assertTrue(cert.lambda_multiplier_at_most_e)
            self.assertGreaterEqual(cert.lambda_multiplier, 1)
            self.assertEqual(
                cert.local_weight_multiplier,
                cert.lambda_multiplier**2,
            )
            self.assertGreaterEqual(cert.finite_exponent_excess, 0)
            self.assertFalse(cert.theorem_claimed)
            self.assertFalse(cert.siv_07_closed)
            self.assertFalse(cert.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_proposition94_local_factors_are_closed_but_parent_is_not(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in (36, 100, 1_000):
                cert = proposition94_local_certificate(k)
                self.assertTrue(cert.denominator_two_over_p_gate_passed)
                self.assertLessEqual(cert.denominator_ratio_upper, 2)
                self.assertEqual(cert.symmetry_multiplier, 1)
                self.assertTrue(
                    mp.almosteq(
                        cert.first_euler_multiplier_upper,
                        mp.exp(mp.mpf(2) / k),
                    )
                )
                self.assertTrue(
                    mp.almosteq(
                        cert.final_two_euler_multiplier_upper,
                        mp.exp(mp.mpf(2) + mp.mpf(2) / k),
                    )
                )
                self.assertTrue(
                    mp.almosteq(
                        cert.full_line_966_normalization_multiplier_upper,
                        mp.exp(mp.mpf(2) + mp.mpf(6) / k),
                    )
                )
                self.assertFalse(cert.distribution_error_closed)
                self.assertTrue(cert.final_euler_products_closed)
                self.assertFalse(cert.proposition_94_closed)
                self.assertFalse(cert.siv_07_closed)
                self.assertFalse(cert.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            integral_size_certificate(H1B2A_MINIMUM_K - 1)
        with self.assertRaises(ValueError):
            integral_size_certificate(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            coefficient_weight_certificate(
                k=36,
                alpha="0.01",
                theta="0.25",
                log_r="0.1",
            )

    def test_contract_sources_formulas_and_parent_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "LEMMA85_LEMMA86_AND_P94_EULER_FINITE_COMPONENTS_CLOSED_P94_PARENT_OPEN",
        )
        self.assertEqual(len(contract["source_registry"]), 3)
        for source in contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )

        finite = contract["finite_lemmas"]
        self.assertEqual(len(finite), 7)
        self.assertEqual(
            finite["L86_absolute_I"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertEqual(
            finite["L85_global_weight"]["status"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        children = {row["id"]: row for row in contract["proposition_94_children"]}
        self.assertEqual(len(children), 5)
        self.assertEqual(
            children["H1B2A-P94-DISTRIBUTION"]["status"],
            "INPUT_PACKAGE_MISSING",
        )
        self.assertEqual(
            children["H1B2A-P94-FINAL-EULER"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        parent = contract["parent_status"]
        self.assertEqual(
            parent["H1B-L85"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            parent["H1B-L86-SIZE"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertEqual(parent["H1B-P94"], "RATE_MISSING")
        self.assertEqual(parent["H1B-COMP-01"], "HARD_BLOCKER")
        self.assertEqual(parent["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(parent["X_cert"], "OPEN")
        self.assertEqual(
            contract["successor_status_update"]["H1B2A-P94-DISTRIBUTION"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            contract["h1b2a2_successor_contract"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a2_Proposition94_distribution_error_v1.json",
        )
        self.assertEqual(
            contract["h1b2a3_successor_contract"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json",
        )
        self.assertEqual(
            contract["successor_status_update"]["H1B-P94"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["threshold_calculator_created"])


if __name__ == "__main__":
    unittest.main()
