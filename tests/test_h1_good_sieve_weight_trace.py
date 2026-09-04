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
        self.assertEqual(self.document["schema_version"], "1.0.0")
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

    def test_finite_integral_project_lemma_is_closed_but_not_threshold(self) -> None:
        integral = self.by_id["H1-SIV-06"]
        self.assertEqual(integral["recoverability"], "PROJECT_FINITE_LEMMA_PROVED")
        self.assertFalse(integral["threshold_ready"])
        self.assertIn("r>=36", integral["printed_information"])
        self.assertEqual(integral["missing_numeric_inputs"], [])


if __name__ == "__main__":
    unittest.main()
