"""Regression tests for the H1c-1b.4e actual-input composition."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from source.h1c1b4e_end_to_end_composition import (
    COMPOSITION_DIMENSION_CUTOFF,
    COMPOSITION_LOG_T_CUTOFF,
    exact_easy_clause_sufficient_checks,
    prime_distribution_composition_budget,
    structural_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b4e_end_to_end_composition_v1.json"
)
T1 = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1c1b4eEndToEndCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_easy_clause_witnesses_hold_beyond_corner(self) -> None:
        for r in (
            COMPOSITION_DIMENSION_CUTOFF,
            COMPOSITION_DIMENSION_CUTOFF + 1,
            2 * COMPOSITION_DIMENSION_CUTOFF,
        ):
            self.assertTrue(all(exact_easy_clause_sufficient_checks(r).values()))
        with self.assertRaises(ValueError):
            exact_easy_clause_sufficient_checks(COMPOSITION_DIMENSION_CUTOFF - 1)

    def test_full_prime_distribution_budget_fits_at_bin_edges(self) -> None:
        r = COMPOSITION_DIMENSION_CUTOFF
        for log_t in (r**5, (r + 1) ** 5 - 1):
            budget = prime_distribution_composition_budget(r, log_t)
            self.assertTrue(budget.target_strictly_met)
            self.assertLess(budget.log_total_normalized_error_upper, 0)
            self.assertLess(budget.log_source_constant_upper, 0)
        with self.assertRaises(ValueError):
            prime_distribution_composition_budget(r, (r + 1) ** 5)

    def test_structural_certificate_closes_input_not_weighted_parent(self) -> None:
        cert = structural_certificate()
        self.assertEqual(cert.proved_log_t_cutoff, COMPOSITION_LOG_T_CUTOFF)
        self.assertEqual(cert.outer_x_cutoff, "X >= 2*exp(10^50)")
        self.assertEqual(cert.fgkmt_hypothesis_interval, "[T,2T]")
        self.assertEqual(
            (cert.clause1_constant, cert.clause2_constant, cert.clause3_constant),
            (1, 1, 2),
        )
        self.assertTrue(cert.actual_identity_hypothesis1_input_closed)
        self.assertTrue(cert.proposition92_hypothesis_input_closed)
        self.assertFalse(cert.proposition92_weighted_moment_closed)
        self.assertFalse(cert.downstream_weighted_lower_endpoint_closed)
        self.assertFalse(cert.broad_siv_08_root_closed)
        self.assertFalse(cert.x_cert_ready)
        self.assertFalse(cert.actual_prime_experiment_performed)

    def test_contract_preserves_fail_closed_root_status(self) -> None:
        self.assertEqual(
            self.contract["outcome"],
            "ACTUAL_IDENTITY_HYPOTHESIS1_INPUT_EXPLICIT_WEIGHTED_P92_AND_ROOT_SIV08_OPEN",
        )
        self.assertTrue(
            self.contract["status_after_gate"][
                "actual_identity_Hypothesis_1_at_selected_subset"
            ].startswith("EXPLICIT")
        )
        self.assertEqual(
            self.contract["status_after_gate"]["H1B-P92_weighted_moment"],
            "RATE_MISSING",
        )
        self.assertEqual(
            self.contract["status_after_gate"]["SIV-08_broad_root"],
            "HARD_BLOCKER",
        )
        t1 = json.loads(T1.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertIn("H1c-1b.4e", rows["SIV-08"]["notes"])

    def test_source_contract_hashes(self) -> None:
        for source in self.contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
                source["key"],
            )


if __name__ == "__main__":
    unittest.main()
