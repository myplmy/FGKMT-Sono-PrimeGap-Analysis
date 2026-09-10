"""Validate the T1 Sono/FMT numerical-threshold proof-obligation ledger."""

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
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class ThresholdProofObligationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.rows = cls.document["obligations"]
        cls.by_id = {row["id"]: row for row in cls.rows}

    def test_schema_and_required_fields(self) -> None:
        self.assertEqual(self.document["schema_version"], "1.8.0")
        self.assertEqual(len(self.rows), 66)
        self.assertEqual(len(self.by_id), len(self.rows), "obligation ids must be unique")

        required = {
            "id",
            "stage",
            "node",
            "source_key",
            "source_page",
            "equation",
            "quantity",
            "direction",
            "explicit_bound",
            "valid_range",
            "depends_on",
            "status",
            "criticality",
            "checker",
            "notes",
        }
        allowed_statuses = set(self.document["status_vocabulary"])
        source_keys = {source["key"] for source in self.document["source_registry"]}

        for row in self.rows:
            self.assertEqual(set(row), required, row["id"])
            self.assertIn(row["status"], allowed_statuses, row["id"])
            self.assertIn(row["source_key"], source_keys, row["id"])
            self.assertIsInstance(row["depends_on"], list, row["id"])

    def test_dependencies_exist_and_form_a_dag(self) -> None:
        for row in self.rows:
            for dependency in row["depends_on"]:
                self.assertIn(dependency, self.by_id, f"{row['id']} -> {dependency}")
                self.assertNotEqual(dependency, row["id"])

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(obligation_id: str) -> None:
            if obligation_id in visited:
                return
            self.assertNotIn(obligation_id, visiting, f"dependency cycle at {obligation_id}")
            visiting.add(obligation_id)
            for dependency in self.by_id[obligation_id]["depends_on"]:
                visit(dependency)
            visiting.remove(obligation_id)
            visited.add(obligation_id)

        for obligation_id in self.by_id:
            visit(obligation_id)

    def test_root_preserves_threshold_distinctions(self) -> None:
        root = self.by_id["FIN-05"]
        self.assertEqual(root["status"], "HARD_BLOCKER")
        self.assertEqual(root["criticality"], "root")
        self.assertIsNone(root["explicit_bound"])
        self.assertIn("X_emp(1e20)=3814280", root["notes"])
        self.assertIn("X_star", root["notes"])
        self.assertIn("No numerical X_cert", root["notes"])

    def test_known_local_source_hashes(self) -> None:
        sources = {
            source["key"]: source
            for source in self.document["source_registry"]
            if source["sha256"] is not None
        }
        self.assertEqual(
            set(sources),
            {
                "SONO2025",
                "FMT2018",
                "FGKMT2016",
                "ROSSER_SCHOENFELD1962",
            },
        )
        for key, source in sources.items():
            locator = source.get("audit_copy", source["locator"])
            path = ROOT / locator
            self.assertTrue(path.is_file(), path)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, source["sha256"], key)

    def test_no_open_root_is_presented_as_explicit(self) -> None:
        root_blockers = [
            row
            for row in self.rows
            if row["criticality"] in {"root", "root-blocker"}
        ]
        self.assertGreaterEqual(len(root_blockers), 6)
        for row in root_blockers:
            self.assertNotEqual(row["status"], "EXPLICIT", row["id"])

    def test_status_counts_include_h1a_sigma_y_and_covering_core(self) -> None:
        self.assertEqual(
            Counter(row["status"] for row in self.rows),
            Counter(
                {
                    "EXPLICIT": 11,
                    "PARTIAL": 10,
                    "RATE_MISSING": 28,
                    "SOURCE_REVIEW_REQUIRED": 4,
                    "HARD_BLOCKER": 13,
                }
            ),
        )

    def test_h1c_source_and_sibling_dependency_corrections(self) -> None:
        source_keys = {source["key"] for source in self.document["source_registry"]}
        self.assertIn("JUTILA1977", source_keys)
        self.assertNotIn("JUTILA1970", source_keys)
        self.assertEqual(self.by_id["PAP-04"]["source_key"], "JUTILA1977")
        self.assertEqual(self.by_id["SIV-08"]["depends_on"], [])
        self.assertEqual(self.by_id["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertEqual(self.by_id["SIV-03"]["status"], "EXPLICIT")
        self.assertEqual(self.by_id["SIV-03"]["depends_on"], [])
        self.assertIn("2*exp(36^5)", self.by_id["SIV-03"]["valid_range"])
        self.assertEqual(self.by_id["AN-02"]["status"], "RATE_MISSING")
        self.assertEqual(self.by_id["UB-05"]["status"], "RATE_MISSING")
        self.assertEqual(
            self.document["h1c1b1a1_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff_v1.json",
        )
        self.assertEqual(
            self.document["h1c1b2_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b2_common_exceptional_remainder_v1.json",
        )
        self.assertEqual(
            self.document["h1c1b3_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b3_endpoint_count_transfer_v1.json",
        )
        self.assertEqual(
            self.document["h1c1b3r1_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction_v1.json",
        )
        self.assertEqual(
            self.document["h1c1b4e_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b4e_end_to_end_composition_v1.json",
        )
        self.assertIn("H1c-1b.3", self.by_id["SIV-08"]["notes"])
        self.assertIn("H1c-1b.4e", self.by_id["SIV-08"]["notes"])
        self.assertIn("constants (1,1,2)", self.by_id["SIV-08"]["notes"])
        self.assertEqual(
            self.document["h1c_ledger"],
            "docs/method/theory/data/Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json",
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
            self.document["h1b1b2d_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json",
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
        self.assertIn(
            "all 11 application excluded-modulus bounds",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertIn(
            "closes its scalar pointwise multiplier",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertIn(
            "closes the two sharp xi*log(x) factors",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertIn(
            "H1b-2a closes finite Lemma 8.5",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertIn(
            "closes the Proposition 9.4 equation-(9.66) final Euler normalization",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertIn(
            "closes the actual A=Z equation-(9.52) distribution child",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertIn(
            "uniform multiplier below 13",
            self.by_id["SIV-07"]["notes"],
        )
        self.assertEqual(self.by_id["SIV-07"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
