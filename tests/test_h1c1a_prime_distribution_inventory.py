"""Validate the H1c-1a quantitative prime-distribution source inventory."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json"
)
PREDECESSOR = (
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


class H1c1aPrimeDistributionInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(INVENTORY.read_text(encoding="utf-8"))
        cls.requirements = cls.document["requirements"]
        cls.requirement_ids = {row["id"] for row in cls.requirements}
        cls.sources = cls.document["source_registry"]
        cls.source_keys = {row["key"] for row in cls.sources}
        cls.candidates = cls.document["candidate_evaluations"]

    def test_schema_scope_and_negative_claims(self) -> None:
        self.assertEqual(self.document["schema_version"], "1.0.0")
        self.assertTrue(self.document["inventory_complete_for_declared_sources"])
        self.assertFalse(self.document["worldwide_exhaustiveness_claimed"])
        self.assertFalse(self.document["drop_in_source_found"])
        self.assertEqual(
            self.document["outcome"],
            "NO_DROP_IN_SOURCE_BORDIGNON2021_COMPOSITION_ROUTE_FOUND",
        )

    def test_requirements_are_unique_and_open(self) -> None:
        self.assertEqual(len(self.requirements), 12)
        self.assertEqual(len(self.requirement_ids), len(self.requirements))
        for row in self.requirements:
            self.assertEqual(set(row), {"id", "name", "requirement", "status"})
            self.assertTrue(row["status"].startswith("OPEN_"), row["id"])

    def test_sources_and_local_hashes(self) -> None:
        self.assertEqual(len(self.source_keys), len(self.sources))
        self.assertTrue(
            {
                "MAYNARD2016",
                "FGKMT2018",
                "AKBARY_HAMBROOK2015",
                "SEDUNOVA2018",
                "SEDUNOVA2019",
                "YAMADA2014_II",
                "YAMADA2015_I",
                "BORDIGNON2021",
                "BENNETT_ET_AL2018",
                "KADIRI2018",
                "LIU2017",
                "JOHNSTON2026",
            }.issubset(self.source_keys)
        )
        for source in self.sources:
            locator = source["local_locator"]
            digest = source["sha256"]
            self.assertEqual(locator is None, digest is None, source["key"])
            if locator is None:
                continue
            path = ROOT / locator
            self.assertTrue(path.is_file(), path)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_candidate_references_and_classifications(self) -> None:
        allowed = set(self.document["classification_vocabulary"])
        candidate_ids = {row["id"] for row in self.candidates}
        self.assertEqual(len(candidate_ids), len(self.candidates))
        for row in self.candidates:
            self.assertIn(row["classification"], allowed, row["id"])
            self.assertFalse(row["direct_substitute"], row["id"])
            self.assertTrue(set(row["source_keys"]).issubset(self.source_keys), row["id"])
            self.assertTrue(row["blocking_requirements"], row["id"])
            self.assertTrue(
                set(row["blocking_requirements"]).issubset(self.requirement_ids),
                row["id"],
            )
        primary = [
            row
            for row in self.candidates
            if row["classification"] == "PRIMARY_COMPOSITION_CANDIDATE"
        ]
        self.assertEqual(len(primary), 1)
        self.assertEqual(primary[0]["source_keys"], ["BORDIGNON2021"])
        self.assertEqual(self.document["primary_composition_candidate"], "BORDIGNON2021")

    def test_sedunova_correction_and_rough_modulus_caution(self) -> None:
        cautions = {row["id"]: row for row in self.document["corrections_and_cautions"]}
        self.assertIn("B-3", cautions["H1C1A-X01"]["rule"])
        self.assertIn("least_prime_factor", cautions["H1C1A-X02"]["rule"])
        sedunova = next(row for row in self.sources if row["key"] == "SEDUNOVA2019")
        self.assertIn("CORRECTION_REQUIRED", sedunova["publication_status"])

    def test_all_parent_gates_remain_fail_closed(self) -> None:
        for key in (
            "numerical_hypothesis1_clause2_ready",
            "maynard_proposition_9_2_numerical_ready",
            "siv_08_closed",
            "siv_07_closed",
            "numerical_x_cert_ready",
            "actual_threshold_computed",
        ):
            self.assertFalse(self.document[key], key)
        self.assertFalse(self.document["target_contract"]["threshold_ready"])
        self.assertFalse(self.document["next_gate"]["ready_for_threshold_calculator"])
        self.assertFalse(self.document["next_gate"]["requires_user_computation_now"])

    def test_predecessor_and_t1_are_synchronized_fail_closed(self) -> None:
        predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        self.assertEqual(predecessor["next_gate"]["id"], "H1c-1b")
        self.assertEqual(
            predecessor["successor_inventory"]["outcome"],
            self.document["outcome"],
        )
        self.assertFalse(predecessor["numerical_hypothesis1_package_ready"])
        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertIn("Bordignon 2021", rows["SIV-08"]["notes"])


if __name__ == "__main__":
    unittest.main()
