"""Fail-closed checks for the H1b Maynard Proposition 6.1 ledger."""

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
    / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json"
)
H1_TRACE = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1_good_sieve_weight_trace_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1bMaynardConstantLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.rows = cls.document["obligations"]
        cls.by_id = {row["id"]: row for row in cls.rows}

    def test_schema_sources_and_unique_ids(self) -> None:
        self.assertEqual(self.document["schema_version"], "1.17.0")
        self.assertEqual(len(self.rows), 17)
        self.assertEqual(len(self.by_id), len(self.rows))
        sources = {row["key"] for row in self.document["source_registry"]}
        self.assertEqual(
            sources,
            {
                "MAYNARD2016",
                "GGPY2009",
                "KUPERBERG2023",
                "CASTILLO_ET_AL_2015",
            },
        )
        maynard = next(
            row for row in self.document["source_registry"] if row["key"] == "MAYNARD2016"
        )
        self.assertEqual(maynard["doi"], "10.1112/S0010437X16007296")
        self.assertEqual(maynard["arxiv"], "1405.2593")
        ggpy = next(
            row for row in self.document["source_registry"] if row["key"] == "GGPY2009"
        )
        self.assertEqual(ggpy["doi"], "10.1112/plms/pdn046")
        self.assertEqual(ggpy["title"], "Small Gaps Between Products of Two Primes")
        self.assertEqual(
            Counter(row["status"] for row in self.rows),
            Counter(
                {
                    "RATE_MISSING": 2,
                    "INPUT_PACKAGE_MISSING": 3,
                    "PARTIAL_EXPLICIT": 1,
                    "PROJECT_FINITE_COMPONENT_CLOSED": 3,
                    "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT": 7,
                    "HARD_BLOCKER": 1,
                }
            ),
        )

    def test_required_fields_statuses_and_dependencies(self) -> None:
        required = {
            "id",
            "locator",
            "role",
            "printed_bound",
            "explicit_parts",
            "missing_numeric_inputs",
            "upstream",
            "status",
            "threshold_ready",
        }
        allowed = set(self.document["status_vocabulary"])
        for row in self.rows:
            self.assertEqual(set(row), required, row["id"])
            self.assertIn(row["status"], allowed, row["id"])
            self.assertTrue(row["explicit_parts"], row["id"])
            self.assertFalse(row["threshold_ready"], row["id"])
            self.assertTrue(set(row["upstream"]).issubset(self.by_id), row["id"])
            if row["status"] in {
                "PROJECT_FINITE_COMPONENT_CLOSED",
                "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
            }:
                self.assertEqual(row["missing_numeric_inputs"], [], row["id"])
            else:
                self.assertTrue(row["missing_numeric_inputs"], row["id"])

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

    def test_required_hypothesis_and_moment_rows_are_present(self) -> None:
        for row_id in (
            "H1B-HYP-01",
            "H1B-HYP-02",
            "H1B-HYP-03",
            "H1B-P91",
            "H1B-P92",
            "H1B-L93",
            "H1B-P94",
            "H1B-P95",
        ):
            self.assertIn(row_id, self.by_id)

        p92 = self.by_id["H1B-P92"]
        self.assertEqual(p92["status"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")
        self.assertIn("identity form", " ".join(p92["explicit_parts"]))
        self.assertIn(
            "one-step dimension repair",
            " ".join(p92["explicit_parts"]),
        )
        self.assertEqual(p92["missing_numeric_inputs"], [])
        self.assertIn(
            "general",
            " ".join(self.document["actual_application_scope_notes"][
                "H1B-P92_remaining_outside_actual_child"
            ]),
        )
        self.assertEqual(
            self.by_id["H1B-L93"]["status"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT"
        )

    def test_h1b1_trace_resolves_source_identity_not_numeric_rate(self) -> None:
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
        self.assertEqual(
            self.by_id["H1B-L82"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertEqual(
            self.by_id["H1B-L83"]["status"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(self.by_id["H1B-L83"]["missing_numeric_inputs"], [])
        self.assertIn(
            "C_L83(a,A2)",
            " ".join(self.by_id["H1B-L83"]["explicit_parts"]),
        )

    def test_project_components_are_closed_without_promoting_package(self) -> None:
        ratio = self.by_id["H1B-L86-RATIO"]
        self.assertEqual(ratio["status"], "PROJECT_FINITE_COMPONENT_CLOSED")
        self.assertIn("k >= 36", " ".join(ratio["explicit_parts"]))
        self.assertEqual(
            self.by_id["H1B-L82"]["missing_numeric_inputs"],
            [],
        )
        self.assertFalse(self.document["full_good_sieve_weight_closed"])
        self.assertFalse(self.document["siv_07_closed"])
        self.assertFalse(self.document["siv_09_closed"])
        self.assertEqual(
            self.by_id["H1B-L84"]["status"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertIn(
            "all nine source-traced Lemma 8.4 subapplications",
            " ".join(self.by_id["H1B-L84"]["explicit_parts"]),
        )
        self.assertIn(
            "square-sum bypass",
            " ".join(self.by_id["H1B-L84"]["explicit_parts"]),
        )
        self.assertIn(
            "C_Y=",
            " ".join(self.by_id["H1B-L84"]["explicit_parts"]),
        )
        self.assertEqual(
            self.by_id["H1B-L85"]["status"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            self.by_id["H1B-L86-SIZE"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertIn(
            "(2 k log k)^(-k)",
            self.by_id["H1B-L86-SIZE"]["printed_bound"],
        )
        p94 = self.by_id["H1B-P94"]
        self.assertEqual(
            p94["status"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertIn(
            "squared-y use by exp(4/k)",
            " ".join(p94["explicit_parts"]),
        )
        self.assertIn(
            "exp(2+6/k)",
            " ".join(p94["explicit_parts"]),
        )
        self.assertEqual(p94["missing_numeric_inputs"], [])
        self.assertIn("uniform multiplier 1", " ".join(p94["explicit_parts"]))
        self.assertIn("T0=floor(Y)-floor(X)", " ".join(p94["explicit_parts"]))
        self.assertTrue((ROOT / self.document["h1bp94g_ledger"]).is_file())
        self.assertIn(
            "uniform multiplier below 13",
            " ".join(p94["explicit_parts"]),
        )
        self.assertNotIn(
            "equation-(9.52) distribution error",
            " ".join(p94["missing_numeric_inputs"]),
        )
        self.assertIn(
            "H1b-2a.2 bounds the actual A=Z",
            " ".join(p94["explicit_parts"]),
        )
        self.assertNotIn("H1B-HYP-01", p94["upstream"])
        self.assertNotIn("H1B-HYP-03", p94["upstream"])
        self.assertNotIn(
            "Euler products",
            " ".join(p94["missing_numeric_inputs"]),
        )

    def test_fail_closed_common_cutoff_and_threshold(self) -> None:
        composition = self.by_id["H1B-COMP-01"]
        self.assertEqual(composition["status"], "HARD_BLOCKER")
        self.assertEqual(
            set(composition["upstream"]),
            set(self.by_id) - {"H1B-COMP-01"},
        )
        self.assertFalse(self.document["numerical_x_cert_ready"])
        self.assertFalse(self.document["actual_threshold_computed"])
        self.assertFalse(self.document["composition"]["common_cutoff_available"])
        self.assertFalse(self.document["composition"]["ready_for_threshold_calculator"])
        self.assertEqual(
            self.document["h1c1b3_endpoint_count_transfer"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b3_endpoint_count_transfer_v1.json",
        )
        self.assertEqual(
            self.document["h1c1b3r1_endpoint_correction"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction_v1.json",
        )
        self.assertEqual(
            self.document["h1c1b4e_actual_hypothesis1_composition"],
            "docs/method/theory/data/"
            "Sono_FMT_H1c1b4e_end_to_end_composition_v1.json",
        )
        self.assertIn("H1b-P92a", self.document["composition"]["next_gate"])
        self.assertIn("H1b-P91a", self.document["composition"]["next_gate"])
        self.assertTrue(self.document["composition"]["next_gate"].startswith("H1b-COR2"))
        self.assertIn("H1b-P94g", self.document["composition"]["next_gate"])
        self.assertTrue(self.document["composition"]["actual_filtered_common_cutoff_available"])
        self.assertTrue(self.document["composition"]["actual_fixed_x_probability_inputs_closed"])
        self.assertTrue((ROOT / self.document["h1bnorm_ledger"]).is_file())
        self.assertIn(
            "constants (1,1,2)",
            self.document["composition"]["project_h1a_input"],
        )

    def test_canonical_h1_and_t1_ledgers_remain_open(self) -> None:
        trace = json.loads(H1_TRACE.read_text(encoding="utf-8"))
        self.assertEqual(
            trace["h1b_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json",
        )
        h1_rows = {row["target_obligation"]: row for row in trace["assessments"]}
        self.assertEqual(h1_rows["SIV-07"]["recoverability"], "QUANTITATIVE_REPROOF_REQUIRED")
        self.assertEqual(h1_rows["SIV-09"]["recoverability"], "QUANTITATIVE_REPROOF_REQUIRED")

        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        t1_rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(t1_rows["SIV-07"]["status"], "HARD_BLOCKER")
        self.assertEqual(t1_rows["SIV-09"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
