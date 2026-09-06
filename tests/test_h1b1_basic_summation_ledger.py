"""Fail-closed checks for the H1b-1 basic summation source audit."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1_basic_summation_constants_v1.json"
)
PARENT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json"
)


class H1b1BasicSummationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.rows = cls.document["obligations"]
        cls.by_id = {row["id"]: row for row in cls.rows}

    def test_schema_sources_and_unique_rows(self) -> None:
        self.assertEqual(self.document["schema_version"], "1.0.0")
        self.assertEqual(len(self.rows), 13)
        self.assertEqual(len(self.by_id), len(self.rows))
        sources = {row["key"] for row in self.document["source_registry"]}
        self.assertEqual(
            sources,
            {
                "MAYNARD2016_PUBLISHED",
                "GGPY2009",
                "GGPY2013_CORRIGENDUM",
                "HR1974",
            },
        )
        ggpy = next(row for row in self.document["source_registry"] if row["key"] == "GGPY2009")
        self.assertEqual(ggpy["doi"], "10.1112/plms/pdn046")
        self.assertEqual(ggpy["title"], "Small Gaps Between Products of Two Primes")
        self.assertEqual(
            Counter(row["status"] for row in self.rows),
            Counter(
                {
                    "RATE_MISSING": 4,
                    "PROJECT_FINITE_COMPONENT_CLOSED": 4,
                    "PARTIAL_EXPLICIT": 1,
                    "PARAMETERIZED_EXPLICIT": 1,
                    "PRINTED_STRUCTURAL_FACT": 1,
                    "SOURCE_ACCESS_BLOCKED": 1,
                    "HARD_BLOCKER": 1,
                }
            ),
        )

    def test_required_fields_statuses_and_dag(self) -> None:
        required = {
            "id",
            "locator",
            "role",
            "printed_information",
            "missing_numeric_inputs",
            "upstream",
            "status",
            "threshold_ready",
        }
        allowed = set(self.document["status_vocabulary"])
        for row in self.rows:
            self.assertEqual(set(row), required, row["id"])
            self.assertIn(row["status"], allowed, row["id"])
            if row["status"] == "PROJECT_FINITE_COMPONENT_CLOSED":
                self.assertEqual(row["missing_numeric_inputs"], [], row["id"])
            else:
                self.assertTrue(row["missing_numeric_inputs"], row["id"])
            self.assertFalse(row["threshold_ready"], row["id"])
            self.assertTrue(set(row["upstream"]).issubset(self.by_id), row["id"])

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(row_id: str) -> None:
            if row_id in visited:
                return
            self.assertNotIn(row_id, visiting, f"dependency cycle at {row_id}")
            visiting.add(row_id)
            for dependency in self.by_id[row_id]["upstream"]:
                visit(dependency)
            visiting.remove(row_id)
            visited.add(row_id)

        for row_id in self.by_id:
            visit(row_id)

    def test_imported_lemma_transfer_is_explicit_but_base_rate_is_not(self) -> None:
        self.assertTrue(self.document["lemma_8_3_citation_identified"])
        self.assertFalse(self.document["lemma_8_3_numeric_multiplier_recovered"])
        self.assertEqual(
            self.by_id["H1B1-L83-GGPY4"]["status"],
            "PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            self.by_id["H1B1-L83-GGPY3"]["status"],
            "SOURCE_ACCESS_BLOCKED",
        )
        self.assertIn(
            "kappa=1",
            self.by_id["H1B1-L83-PUBLISHED-NOTE"]["printed_information"],
        )

    def test_package_and_parent_remain_fail_closed(self) -> None:
        package = self.by_id["H1B1-PACKAGE"]
        self.assertEqual(package["status"], "HARD_BLOCKER")
        self.assertFalse(self.document["numerical_basic_summation_package_ready"])
        self.assertFalse(self.document["siv_07_closed"])
        self.assertFalse(self.document["numerical_x_cert_ready"])
        self.assertFalse(self.document["actual_threshold_computed"])

        parent = json.loads(PARENT.read_text(encoding="utf-8"))
        parent_rows = {row["id"]: row for row in parent["obligations"]}
        self.assertEqual(parent_rows["H1B-L83"]["status"], "RATE_MISSING")
        self.assertFalse(parent["siv_07_closed"])
        self.assertEqual(
            parent["h1b1_ledger"],
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


if __name__ == "__main__":
    unittest.main()
