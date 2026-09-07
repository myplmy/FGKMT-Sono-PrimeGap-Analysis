"""Regression checks for the H1b-1b-2a.1 application inventory."""

from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L620_D_W,
    MAYNARD_APPLICATION_EXCLUSION_IDS,
    MAYNARD_APPLICATION_EXCLUSION_SPECS,
    application_exclusion_spec,
    elementary_cgamma_lower_bound,
    maynard_application_dimension,
    maynard_application_log_overhead,
    maynard_application_log_q_upper,
    maynard_base_log_excluded_integer_upper,
    maynard_uniform_application_log_q_upper,
    rosser_schoenfeld_cgamma_lower_bound,
    w0_base_domination_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2a1_application_exclusion_inventory_v1.json"
)


class H1b1b2a1ApplicationExclusionInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.rows = cls.contract["applications"]

    def test_contract_scope_and_source_hash(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.2.0")
        self.assertEqual(len(self.rows), 11)
        self.assertEqual(
            self.contract["trace_completeness"],
            {
                "external_multiple_summation_call_sites": 8,
                "external_partial_summation_call_sites": 2,
                "analytic_subapplications": 11,
                "line_1135_split_subapplications": 2,
                "internal_lemma_proof_calls_excluded": [558, 568, 581, 591],
                "all_traced_calls_closed": True,
            },
        )
        source = self.contract["source_registry"][0]
        source_path = ROOT / source["local_path"]
        self.assertEqual(
            hashlib.sha256(source_path.read_bytes()).hexdigest(),
            source["sha256"],
        )

    def test_contract_rows_match_immutable_code_inventory(self) -> None:
        self.assertEqual(
            {row["id"] for row in self.rows},
            MAYNARD_APPLICATION_EXCLUSION_IDS,
        )
        self.assertEqual(
            {spec.application_id for spec in MAYNARD_APPLICATION_EXCLUSION_SPECS},
            MAYNARD_APPLICATION_EXCLUSION_IDS,
        )
        self.assertEqual(Counter(row["delta_log_r"] for row in self.rows), {0: 8, 1: 3})
        self.assertTrue(
            all(row["status"] == "PROJECT_PARAMETERIZED_EXPLICIT" for row in self.rows)
        )
        for row in self.rows:
            spec = application_exclusion_spec(row["id"])
            self.assertEqual(row["dimension_mode"], spec.dimension_mode)
            self.assertEqual(row["delta_log_r"], spec.log_r_overhead_coefficient)

    def test_dimensions_and_w0_domination_are_exact(self) -> None:
        dimensions = {
            row["id"]: maynard_application_dimension(36, row["id"])
            for row in self.rows
        }
        for row in self.rows:
            expected = {"k": 36, "k_minus_one": 35, "one": 1}[
                row["dimension_mode"]
            ]
            self.assertEqual(dimensions[row["id"]], expected)

        for k in range(2, 257):
            certificate = w0_base_domination_certificate(k)
            self.assertEqual(certificate.log_two_margin, k * (k - 2))
            self.assertEqual(
                certificate.alpha_log_x_margin,
                2 * k * k - 3 * k - 1,
            )
            self.assertGreaterEqual(certificate.log_two_margin, 0)
            self.assertGreaterEqual(certificate.alpha_log_x_margin, 0)

    def test_every_application_iteration_is_below_uniform_bound(self) -> None:
        parameters = {
            "k": 36,
            "alpha": "0.01",
            "theta": "0.333333333333333333333333333333333333",
            "log_r": "1000",
        }
        uniform = maynard_uniform_application_log_q_upper(**parameters)
        attained = maynard_application_log_q_upper(
            application_id=APPLICATION_L620_D_W,
            iteration=0,
            **parameters,
        )
        self.assertEqual(uniform, attained)
        self.assertEqual(
            uniform,
            maynard_base_log_excluded_integer_upper(
                r=36,
                iteration=0,
                **parameters,
            )
            + mp.mpf(parameters["log_r"]),
        )

        for spec in MAYNARD_APPLICATION_EXCLUSION_SPECS:
            dimension = maynard_application_dimension(36, spec.application_id)
            self.assertEqual(
                maynard_application_log_overhead(
                    spec.application_id,
                    parameters["log_r"],
                ),
                spec.log_r_overhead_coefficient * mp.mpf(parameters["log_r"]),
            )
            for iteration in range(dimension):
                value = maynard_application_log_q_upper(
                    application_id=spec.application_id,
                    iteration=iteration,
                    **parameters,
                )
                self.assertLessEqual(value, uniform)

        self.assertGreater(
            rosser_schoenfeld_cgamma_lower_bound(uniform),
            elementary_cgamma_lower_bound(uniform),
        )

    def test_unknown_or_invalid_applications_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            application_exclusion_spec("untraced_application")
        with self.assertRaises(ValueError):
            maynard_application_dimension(1, APPLICATION_L620_D_W)
        with self.assertRaises(ValueError):
            maynard_application_log_overhead(APPLICATION_L620_D_W, 0)
        with self.assertRaises(ValueError):
            maynard_application_log_q_upper(
                application_id=APPLICATION_L620_D_W,
                k=36,
                iteration=36,
                alpha="0.01",
                theta="0.333",
                log_r="1000",
            )

    def test_closure_does_not_promote_parent_theorem(self) -> None:
        route = self.contract["route_status"]
        self.assertTrue(route["all_actual_application_overheads_certified"])
        self.assertFalse(route["explicit_lower_bound_route_selected"])
        self.assertTrue(route["corrected_kappa1_wirsing_route_selected"])
        self.assertEqual(
            self.contract["corrected_wirsing_contract"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier_v1.json",
        )
        self.assertFalse(route["C3_abs_numeric_multiplier_recovered"])
        self.assertFalse(route["actual_A1_A2_L_numeric"])
        self.assertTrue(route["actual_A1_A2_L_parameterized_explicit"])
        self.assertFalse(route["corrected_rfold_composition_closed"])
        self.assertFalse(route["numerical_route_complete"])
        self.assertEqual(self.contract["parent_status"]["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(self.contract["parent_status"]["X_cert"], "OPEN")
        self.assertFalse(self.contract["next_gate"]["ready_for_threshold_calculator"])
        self.assertFalse(self.contract["next_gate"]["ready_for_actual_prime_experiment"])


if __name__ == "__main__":
    unittest.main()
