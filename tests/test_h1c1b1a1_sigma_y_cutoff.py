"""Regression checks for the H1c-1b.1a.1 sigma*y cutoff."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b1a1_sigma_y_cutoff import (
    COARSE_EXCEPTIONAL_FACTOR,
    COARSE_PRODUCT_ERROR,
    COARSE_SIGMA_Y_MULTIPLIER,
    MINIMUM_ENDPOINT_DIMENSION,
    MINIMUM_LOG_X_OVER_TWO,
    ROSSER_LOWER_ENDPOINT,
    TARGET_SIGMA_Y_MULTIPLIER,
    evaluate_sigma_y_upper_multiplier,
    exact_sigma_y_cutoff_certificate,
    minimum_log10_x,
    minimum_log_x,
    sigma_y_cutoff_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff_v1.json"
)
PREDECESSOR = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1c1b1a1SigmaYCutoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_rational_chain(self) -> None:
        self.assertTrue(exact_sigma_y_cutoff_certificate())
        self.assertEqual(COARSE_PRODUCT_ERROR, Fraction(1, 1000))
        self.assertEqual(COARSE_EXCEPTIONAL_FACTOR, Fraction(1000, 999))
        self.assertEqual(
            (1 + COARSE_PRODUCT_ERROR)
            / (1 - COARSE_PRODUCT_ERROR)
            * COARSE_EXCEPTIONAL_FACTOR,
            COARSE_SIGMA_Y_MULTIPLIER,
        )
        self.assertEqual(
            COARSE_SIGMA_Y_MULTIPLIER,
            Fraction(1_001_000, 998_001),
        )
        self.assertLess(COARSE_SIGMA_Y_MULTIPLIER, TARGET_SIGMA_Y_MULTIPLIER)

    def test_endpoint_numeric_evaluation_is_stronger_than_coarse_bound(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            endpoint = evaluate_sigma_y_upper_multiplier(minimum_log_x())
            self.assertGreater(endpoint.log_2_x, 15)
            self.assertGreater(endpoint.log_a, 300)
            self.assertGreater(endpoint.log_z, endpoint.log_a)
            self.assertLess(endpoint.upper_product_error, mp.mpf(1) / 1000)
            self.assertLess(endpoint.lower_product_error, mp.mpf(1) / 1000)
            self.assertLess(
                endpoint.exceptional_prime_factor,
                mp.mpf(1000) / 999,
            )
            self.assertLess(
                endpoint.sigma_y_upper_multiplier,
                mp.mpf(COARSE_SIGMA_Y_MULTIPLIER.numerator)
                / COARSE_SIGMA_Y_MULTIPLIER.denominator,
            )
            self.assertGreater(minimum_log10_x(), 26_000_000)
            self.assertLess(minimum_log10_x(), 27_000_000)
        finally:
            mp.mp.dps = old_dps

    def test_domain_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_sigma_y_upper_multiplier(
                mp.mpf(MINIMUM_LOG_X_OVER_TWO) + mp.log(2) - 1
            )
        with self.assertRaises(ValueError):
            evaluate_sigma_y_upper_multiplier(mp.inf)
        with self.assertRaises(ValueError):
            evaluate_sigma_y_upper_multiplier(mp.nan)

    def test_certificate_closes_only_siv03(self) -> None:
        cert = sigma_y_cutoff_certificate()
        self.assertEqual(cert.minimum_endpoint_dimension, 36)
        self.assertEqual(cert.rosser_lower_endpoint, ROSSER_LOWER_ENDPOINT)
        self.assertTrue(cert.exact_rational_certificate)
        self.assertTrue(cert.interval_endpoint_semantics_closed)
        self.assertTrue(cert.exceptional_prime_local_correction_closed)
        self.assertTrue(cert.siv_03_closed)
        self.assertTrue(cert.sono_coefficient_preserved_at_this_gate)
        for value in (
            cert.full_distribution_common_exceptional_b_closed,
            cert.hypothesis1_clause2_closed,
            cert.proposition92_closed,
            cert.siv_07_closed,
            cert.siv_08_closed,
            cert.x_cert_ready,
            cert.actual_prime_experiment_performed,
        ):
            self.assertFalse(value)

        status = self.contract["status_after_this_gate"]
        self.assertEqual(status["siv_03"], "EXPLICIT")
        self.assertEqual(status["siv_07"], "HARD_BLOCKER")
        self.assertEqual(status["siv_08"], "HARD_BLOCKER")
        self.assertEqual(status["numerical_x_cert"], "OPEN")

    def test_source_hashes_are_reproducible(self) -> None:
        for source in self.contract["source_registry"]:
            local_path = source.get("local_path")
            expected_hash = source.get("sha256")
            if local_path is None or expected_hash is None:
                continue
            path = ROOT / local_path
            self.assertTrue(path.is_file(), local_path)
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                expected_hash,
                source["key"],
            )

    def test_predecessor_and_t1_are_synchronized(self) -> None:
        predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        successor = predecessor["successor_sigma_y_cutoff"]
        self.assertEqual(successor["id"], "H1c-1b.1a.1 / SIV-03")
        self.assertTrue(successor["explicit_sigma_cutoff_closed"])
        self.assertFalse(successor["numerical_x_cert_ready"])

        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["SIV-03"]["status"], "EXPLICIT")
        self.assertEqual(rows["SIV-03"]["depends_on"], [])
        self.assertIn("2*exp(36^5)", rows["SIV-03"]["valid_range"])
        self.assertEqual(rows["AN-02"]["status"], "RATE_MISSING")
        self.assertEqual(rows["UB-05"]["status"], "RATE_MISSING")
        self.assertEqual(rows["SIV-07"]["status"], "HARD_BLOCKER")
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertEqual(rows["FIN-05"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
