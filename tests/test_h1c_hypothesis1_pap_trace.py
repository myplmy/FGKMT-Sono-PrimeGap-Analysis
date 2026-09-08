"""Validate the H1c Hypothesis 1 and PAP sibling source trace."""

from __future__ import annotations

import hashlib
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
    / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1cHypothesis1PapTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.rows = cls.document["obligations"]
        cls.by_id = {row["id"]: row for row in cls.rows}

    def test_schema_sources_and_unique_rows(self) -> None:
        self.assertEqual(self.document["schema_version"], "1.0.0")
        self.assertEqual(len(self.rows), 20)
        self.assertEqual(len(self.by_id), len(self.rows))
        sources = {row["key"] for row in self.document["source_registry"]}
        self.assertEqual(
            sources,
            {
                "FGKMT2016",
                "SONO2025",
                "DAVENPORT2000",
                "MCCURLEY1984",
                "GALLAGHER1970",
                "JUTILA1977",
                "MAIER1981",
                "AKBARY_HAMBROOK2015",
            },
        )
        self.assertNotIn("JUTILA1970", sources)
        self.assertEqual(
            Counter(row["status"] for row in self.rows),
            Counter(
                {
                    "RATE_MISSING": 8,
                    "SOURCE_REVIEW_REQUIRED": 3,
                    "HARD_BLOCKER": 3,
                    "EXACT_SUFFICIENT_REDUCTION": 2,
                    "PARTIAL_NUMERIC": 2,
                    "ALTERNATIVE_NOT_DIRECT_SUBSTITUTE": 1,
                    "LOGICAL_RELATION_CORRECTED": 1,
                }
            ),
        )

    def test_required_fields_statuses_and_dag(self) -> None:
        required = {
            "id",
            "branch",
            "locator",
            "role",
            "printed_or_derived_information",
            "missing_numeric_inputs",
            "upstream",
            "status",
            "threshold_ready",
        }
        allowed = set(self.document["status_vocabulary"])
        for row in self.rows:
            self.assertEqual(set(row), required, row["id"])
            self.assertIn(row["status"], allowed, row["id"])
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

    def test_local_primary_source_hashes(self) -> None:
        for key in ("FGKMT2016", "SONO2025"):
            source = next(row for row in self.document["source_registry"] if row["key"] == key)
            path = ROOT / source["local_locator"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source["sha256"])

    def test_sibling_logic_and_easy_clause_reductions(self) -> None:
        self.assertFalse(self.document["hypothesis1_implies_pap"])
        self.assertFalse(self.document["pap_implies_hypothesis1"])
        self.assertTrue(self.document["shared_analytic_inputs_do_not_create_logical_dependency"])
        self.assertEqual(self.by_id["H1C-RELATION"]["status"], "LOGICAL_RELATION_CORRECTED")
        self.assertEqual(self.by_id["H1C-HYP1-1"]["status"], "EXACT_SUFFICIENT_REDUCTION")
        self.assertEqual(self.by_id["H1C-HYP1-3"]["status"], "EXACT_SUFFICIENT_REDUCTION")
        self.assertIn("constant 2", self.by_id["H1C-HYP1-3"]["printed_or_derived_information"])

    def test_packages_remain_fail_closed(self) -> None:
        self.assertEqual(self.by_id["H1C-HYP1-PACKAGE"]["status"], "HARD_BLOCKER")
        self.assertEqual(self.by_id["H1C-PAP-PACKAGE"]["status"], "HARD_BLOCKER")
        self.assertEqual(self.by_id["H1C-COMMON-CUTOFF"]["status"], "HARD_BLOCKER")
        self.assertEqual(
            self.by_id["H1C-AH-ALTERNATIVE"]["status"],
            "ALTERNATIVE_NOT_DIRECT_SUBSTITUTE",
        )
        self.assertFalse(self.document["numerical_hypothesis1_package_ready"])
        self.assertFalse(self.document["numerical_pap_package_ready"])
        self.assertFalse(self.document["numerical_x_cert_ready"])
        self.assertFalse(self.document["actual_threshold_computed"])

    def test_t1_canonical_corrections_are_applied(self) -> None:
        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        source_keys = {source["key"] for source in t1["source_registry"]}
        self.assertIn("JUTILA1977", source_keys)
        self.assertNotIn("JUTILA1970", source_keys)
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["PAP-04"]["source_key"], "JUTILA1977")
        self.assertEqual(rows["SIV-08"]["depends_on"], [])
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")

    def test_successor_parameter_envelope_remains_fail_closed(self) -> None:
        successor = self.document["successor_parameter_envelope"]
        self.assertEqual(successor["id"], "H1c-1b.1")
        self.assertTrue(successor["bordignon_modulus_capacity_closed"])
        self.assertFalse(successor["printed_source_r_dyadic_admissibility_closed"])
        self.assertTrue(successor["one_step_dimension_repair_available"])
        self.assertFalse(successor["full_distribution_package_ready"])
        self.assertEqual(
            self.document["next_gate"]["id"],
            "H1c-1b.2",
        )
        transfer = self.document["successor_dimension_coefficient_transfer"]
        self.assertTrue(transfer["asymptotic_sono_coefficient_preserved"])
        self.assertFalse(transfer["explicit_sigma_cutoff_closed"])
        self.assertTrue(
            self.document["successor_sigma_y_cutoff"][
                "explicit_sigma_cutoff_closed"
            ]
        )


if __name__ == "__main__":
    unittest.main()
