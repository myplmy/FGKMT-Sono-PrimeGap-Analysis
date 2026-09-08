"""Fail-closed checks for the H1b-1b-2d.1b sharp-scale package."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L1096_W0,
    APPLICATION_L1135_W0_FACTOR,
)
from source.h1b1b2b_corrected_wirsing import (
    strict_summatory_multiplier,
    summatory_multiplier,
)
from source.h1b1b2c_actual_parameter_package import (
    H1B1B2C_MAYNARD_A1_GAP,
    H1B1B2C_UPPER_DISCREPANCY_A2,
)
from source.h1b1b2d_rfold_smooth_package import sharp_cutoff_relative_error
from source.h1b1b2d1b_sharp_scale import (
    FMT_SHARP_SCALE_OVER_LOG_R_LOWER,
    FMT_XI_OVER_THETA,
    H1B1B2D1B_RELATIVE_ERROR_TARGET,
    MAYNARD_LOG_R_UPPER_EXPONENT_OVER_THETA,
    SHARP_APPLICATION_IDS,
    common_sharp_scale_gate_certificate,
    fmt_sharp_relative_error_upper,
    fmt_sharp_scale_lower_bound,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2d1b_sharp_scale_v1.json"
)


class H1b1b2d1bSharpScaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_rational_scale_constants_and_application_inventory(self) -> None:
        self.assertEqual(FMT_XI_OVER_THETA, Fraction(1, 10))
        self.assertEqual(
            MAYNARD_LOG_R_UPPER_EXPONENT_OVER_THETA,
            Fraction(1, 3),
        )
        self.assertEqual(FMT_SHARP_SCALE_OVER_LOG_R_LOWER, Fraction(3, 10))
        self.assertEqual(H1B1B2D1B_RELATIVE_ERROR_TARGET, Fraction(1, 2))
        self.assertEqual(
            SHARP_APPLICATION_IDS,
            {APPLICATION_L1096_W0, APPLICATION_L1135_W0_FACTOR},
        )

    def test_sharp_scale_bound_is_tight_at_the_upper_R_endpoint(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            theta = mp.mpf(1) / 3
            log_x = mp.mpf(120)
            xi_log_x = theta * log_x / 10
            log_r = theta * log_x / 3
            self.assertEqual(fmt_sharp_scale_lower_bound(log_r), xi_log_x)
        finally:
            mp.mp.dps = old_dps

    def test_strict_endpoint_allowance_is_used_by_old_and_new_diagnostics(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 160
            base = summatory_multiplier(
                H1B1B2C_MAYNARD_A1_GAP,
                H1B1B2C_UPPER_DISCREPANCY_A2,
            )
            strict = strict_summatory_multiplier(
                H1B1B2C_MAYNARD_A1_GAP,
                H1B1B2C_UPPER_DISCREPANCY_A2,
            )
            self.assertEqual(mp.fsub(strict, base, exact=True), 2)
            scale = mp.mpf(1000)
            log_lambda = mp.mpf(7)
            self.assertEqual(
                sharp_cutoff_relative_error(
                    scale_log=scale,
                    log_lambda_star=log_lambda,
                ),
                strict * (6 + log_lambda) / scale,
            )
        finally:
            mp.mp.dps = old_dps

    def test_closed_form_gate_proves_both_required_inequalities(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 180
            for k in (36, 100):
                certificate = common_sharp_scale_gate_certificate(
                    k=k,
                    alpha=2,
                    theta=mp.mpf(1) / 3,
                )
                y = certificate.log_r_sufficient
                e_value = certificate.e_coefficient
                self.assertLessEqual(e_value * mp.log(y), y / 2)
                self.assertLessEqual(
                    e_value
                    * (
                        6
                        + mp.log(
                            certificate.lambda_affine_constant
                            + certificate.lambda_affine_slope
                        )
                    ),
                    y / 2,
                )
                self.assertLessEqual(
                    e_value * (6 + mp.log(certificate.log_excluded_integer_upper)),
                    y,
                )
                self.assertTrue(certificate.endpoint_gate_passed)
                self.assertTrue(certificate.relative_error_gate_passed)
                self.assertTrue(certificate.sharp_calls_closed)
                self.assertEqual(certificate.sharp_application_count, 2)
                self.assertEqual(
                    certificate.h1b_l84_status,
                    "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
                )
                self.assertFalse(certificate.h1b_comp_01_closed)
                self.assertFalse(certificate.siv_07_closed)
                self.assertFalse(certificate.siv_09_closed)
                self.assertFalse(certificate.x_cert_ready)
                self.assertFalse(certificate.theorem_claimed)
                self.assertEqual(
                    fmt_sharp_relative_error_upper(
                        k=k,
                        alpha=2,
                        theta=mp.mpf(1) / 3,
                        log_r=y,
                    ),
                    certificate.relative_error_upper_bound,
                )
        finally:
            mp.mp.dps = old_dps

    def test_invalid_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            common_sharp_scale_gate_certificate(k=35, alpha=2, theta="0.3")
        with self.assertRaises(ValueError):
            common_sharp_scale_gate_certificate(k=36, alpha=0, theta="0.3")
        with self.assertRaises(ValueError):
            common_sharp_scale_gate_certificate(k=36, alpha=2, theta=1)
        with self.assertRaises(ValueError):
            fmt_sharp_scale_lower_bound(True)

    def test_contract_sources_scope_and_fail_closed_parent(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "TWO_SHARP_CALLS_PARAMETERIZED_EXPLICIT_"
            "H1B_L84_COMPONENT_CLOSED_PARENT_PACKAGE_OPEN",
        )
        self.assertEqual(
            {row["id"] for row in contract["applications"]},
            SHARP_APPLICATION_IDS,
        )
        self.assertIn("<< xi", contract["source_version_caution"]["published_statement"])
        self.assertFalse(
            contract["source_version_caution"]["formal_erratum_found_in_targeted_official_search"]
        )
        for source in contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )

        status = contract["status_after_predecessor_composition"]
        self.assertTrue(status["sharp_calls_closed"])
        self.assertEqual(
            status["actual_lemma84_subapplications_parameterized_explicit"],
            "9/9",
        )
        self.assertEqual(status["H1B-L84"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")
        self.assertEqual(status["H1B-COMP-01"], "HARD_BLOCKER")
        self.assertEqual(status["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(status["SIV-09"], "HARD_BLOCKER")
        self.assertEqual(status["X_cert"], "OPEN")
        self.assertFalse(contract["numerical_x_cert_ready"])
        self.assertFalse(contract["actual_threshold_computed"])
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["new_python_dependency_required"])
        self.assertFalse(contract["lean_required_for_this_gate"])


if __name__ == "__main__":
    unittest.main()
