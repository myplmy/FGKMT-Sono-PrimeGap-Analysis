"""Validate the H1 Sono/FMT good-sieve-weight source trace."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACE = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1_good_sieve_weight_trace_v1.json"
)


class GoodSieveWeightTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(TRACE.read_text(encoding="utf-8"))
        cls.rows = cls.document["assessments"]
        cls.by_id = {row["id"]: row for row in cls.rows}

    def test_schema_and_unique_expected_rows(self) -> None:
        self.assertEqual(self.document["schema_version"], "1.5.0")
        self.assertEqual(len(self.rows), 9)
        self.assertEqual(len(self.by_id), len(self.rows))
        self.assertEqual(
            {row["target_obligation"] for row in self.rows},
            {
                "SIV-01",
                "SIV-02",
                "SIV-05",
                "SIV-06",
                "SIV-07",
                "SIV-08",
                "SIV-09",
                "SIV-10",
                "SIV-11",
            },
        )

    def test_sources_and_recoverability_vocabulary(self) -> None:
        source_keys = {source["key"] for source in self.document["source_registry"]}
        allowed = set(self.document["recoverability_vocabulary"])
        self.assertEqual(
            source_keys,
            {"SONO2025", "FMT2018", "FGKMT2016", "MAYNARD2016"},
        )

        required = {
            "id",
            "target_obligation",
            "question",
            "source_keys",
            "source_locator",
            "printed_information",
            "missing_numeric_inputs",
            "recoverability",
            "reproof_scale",
            "next_action",
            "threshold_ready",
        }
        for row in self.rows:
            self.assertEqual(set(row), required, row["id"])
            self.assertTrue(set(row["source_keys"]).issubset(source_keys), row["id"])
            self.assertIn(row["recoverability"], allowed, row["id"])
            if row["recoverability"] == "PROJECT_FINITE_LEMMA_PROVED":
                self.assertEqual(row["missing_numeric_inputs"], [], row["id"])
            else:
                self.assertTrue(row["missing_numeric_inputs"], row["id"])
            self.assertFalse(row["threshold_ready"], row["id"])

    def test_fail_closed_threshold_status(self) -> None:
        self.assertEqual(
            self.document["overall_outcome"],
            "CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED",
        )
        self.assertFalse(self.document["numerical_x_cert_ready"])
        self.assertFalse(self.document["actual_threshold_computed"])
        package = self.by_id["H1-SIV-11"]
        self.assertEqual(package["recoverability"], "DEPENDENCY_BLOCKED")

    def test_followup_ledgers_are_linked_without_promoting_h1(self) -> None:
        self.assertEqual(
            self.document["h1b1_ledger"],
            "docs/method/theory/data/Sono_FMT_H1b1_basic_summation_constants_v1.json",
        )
        self.assertEqual(
            self.document["h1b1a_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1a_explicit_cutoff_summation_v1.json",
        )
        self.assertEqual(
            self.document["h1b1b_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_v1.json",
        )
        self.assertEqual(
            self.document["h1b1b2a_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2a_actual_local_factor_lower_bound_v1.json",
        )
        self.assertEqual(
            self.document["h1b1b2b_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier_v1.json",
        )
        self.assertEqual(
            self.document["h1b1b2d1a_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2d1a_H_remainder_bypass_v1.json",
        )
        self.assertEqual(
            self.document["h1b1b2d1a1_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2d1a1_scalar_remainder_v1.json",
        )
        self.assertEqual(
            self.document["h1b1b2d1b_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2d1b_sharp_scale_v1.json",
        )
        self.assertEqual(
            self.document["h1b2a_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a_residual_moment_error_v1.json",
        )
        self.assertEqual(
            self.document["h1b2a1_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a1_Proposition94_Euler_normalization_v1.json",
        )
        self.assertEqual(
            self.document["h1b2a2_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a2_Proposition94_distribution_error_v1.json",
        )
        self.assertEqual(
            self.document["h1b2a3_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json",
        )
        self.assertEqual(
            self.document["h1c_ledger"],
            "docs/method/theory/data/Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json",
        )
        self.assertEqual(
            self.by_id["H1-SIV-08"]["recoverability"],
            "QUANTITATIVE_REPROOF_REQUIRED",
        )
        siv_07 = next(
            row for row in self.rows if row["target_obligation"] == "SIV-07"
        )
        self.assertNotIn(
            "scalar pointwise multiplier",
            " ".join(siv_07["missing_numeric_inputs"]),
        )
        self.assertNotIn(
            "sharp xi*log(x)",
            " ".join(siv_07["missing_numeric_inputs"]),
        )
        self.assertIn(
            "All nine traced Lemma 8.4 subapplications",
            siv_07["printed_information"],
        )
        self.assertIn("H1b-2a further closes", siv_07["printed_information"])
        self.assertNotIn(
            "Euler normalizations",
            " ".join(siv_07["missing_numeric_inputs"]),
        )
        self.assertIn(
            "H1b-2a.1 closes",
            siv_07["printed_information"],
        )
        self.assertIn(
            "H1b-2a.2 closes the actual A=Z",
            siv_07["printed_information"],
        )
        self.assertIn(
            "uniform multiplier below 13",
            siv_07["printed_information"],
        )
        self.assertFalse(self.document["numerical_x_cert_ready"])

    def test_finite_integral_project_lemma_is_closed_but_not_threshold(self) -> None:
        integral = self.by_id["H1-SIV-06"]
        self.assertEqual(integral["recoverability"], "PROJECT_FINITE_LEMMA_PROVED")
        self.assertFalse(integral["threshold_ready"])
        self.assertIn("r>=36", integral["printed_information"])
        self.assertEqual(integral["missing_numeric_inputs"], [])


if __name__ == "__main__":
    unittest.main()
