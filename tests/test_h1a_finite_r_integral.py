"""Validate the H1a finite-r integral proof contract."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from source.h1a_finite_r_integral import (
    H1A_ANALYTIC_R_START,
    H1A_FINITE_SCAN_START,
    H1A_FINITE_SCAN_STOP,
    scan_finite_r_intervals,
    verify_analytic_tail_boundary,
    verify_finite_r_interval,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1a_finite_r_integral_contract_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1aFiniteRIntegralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_contract_is_scoped_and_fail_closed(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.0.0")
        self.assertEqual(
            self.contract["outcome"],
            "FINITE_R_INTEGRAL_LEMMA_PROVED_IN_PROJECT",
        )
        self.assertEqual(self.contract["certified_uniform_r_start"], 36)
        self.assertFalse(self.contract["full_good_sieve_weight_closed"])
        self.assertFalse(self.contract["numerical_x_cert_ready"])
        self.assertFalse(self.contract["actual_threshold_computed"])

    def test_directed_interval_scan_covers_every_finite_r(self) -> None:
        summary = scan_finite_r_intervals()
        self.assertEqual(summary.start, H1A_FINITE_SCAN_START)
        self.assertEqual(summary.stop, H1A_FINITE_SCAN_STOP)
        self.assertEqual(summary.count, 8_068)
        self.assertEqual(summary.failures, ())
        self.assertEqual(summary.minimum_relative_margin_r, 36)
        self.assertGreater(summary.minimum_relative_margin_lower, 0.025)

    def test_analytic_tail_boundary_checks(self) -> None:
        checks = verify_analytic_tail_boundary()
        self.assertTrue(checks)
        self.assertTrue(all(checks.values()), checks)
        self.assertEqual(H1A_ANALYTIC_R_START, 8_104)

    def test_single_r_is_fail_closed_below_certified_start(self) -> None:
        result = verify_finite_r_interval(35)
        self.assertTrue(result.positive_margin)
        self.assertFalse(result.target_passed)

        with self.assertRaises(ValueError):
            verify_finite_r_interval(True)
        with self.assertRaises(ValueError):
            verify_finite_r_interval(1)

    def test_t1_siv_06_is_closed_without_promoting_root(self) -> None:
        ledger = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        by_id = {row["id"]: row for row in ledger["obligations"]}
        self.assertEqual(by_id["SIV-06"]["status"], "EXPLICIT")
        self.assertIn("r>=36", by_id["SIV-06"]["explicit_bound"])
        self.assertEqual(by_id["SIV-11"]["status"], "HARD_BLOCKER")
        self.assertEqual(by_id["FIN-05"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
