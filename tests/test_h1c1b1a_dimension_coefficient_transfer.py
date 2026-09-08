"""Regression checks for H1c-1b.1a dimension/coefficient transfer."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b1a_dimension_coefficient_transfer import (
    COMBINED_NORMALIZATION_LOWER_BOUND,
    DIMENSION_RATIO_LOWER_BOUND,
    HYPERGRAPH_C_MULTIPLIER_REQUIRED,
    MINIMUM_ENDPOINT_DIMENSION,
    NET_COEFFICIENT_FACTOR,
    R_SCALE_RATIO_LOWER_BOUND,
    SIGMA_Y_UPPER_MULTIPLIER_GATE,
    actual_r_scale_ratio,
    coarse_c_lower_multiplier,
    coefficient_gate_passes,
    combined_normalization_ratio,
    dimension_coefficient_transfer_certificate,
    dimension_normalization_ratio,
    endpoint_dimension_bracket_holds,
    exact_transfer_slack_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json"
)
PREDECESSOR = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1c1b1aDimensionCoefficientTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_integer_and_rational_slack_chain(self) -> None:
        self.assertTrue(exact_transfer_slack_certificate())
        self.assertEqual(DIMENSION_RATIO_LOWER_BOUND, Fraction(63, 64))
        self.assertEqual(R_SCALE_RATIO_LOWER_BOUND, Fraction(104, 105))
        self.assertEqual(
            DIMENSION_RATIO_LOWER_BOUND * R_SCALE_RATIO_LOWER_BOUND,
            COMBINED_NORMALIZATION_LOWER_BOUND,
        )
        self.assertEqual(
            COMBINED_NORMALIZATION_LOWER_BOUND
            / SIGMA_Y_UPPER_MULTIPLIER_GATE,
            NET_COEFFICIENT_FACTOR,
        )
        self.assertEqual(
            coarse_c_lower_multiplier(),
            HYPERGRAPH_C_MULTIPLIER_REQUIRED,
        )
        self.assertTrue(coefficient_gate_passes())
        self.assertFalse(coefficient_gate_passes(Fraction(27, 25)))

    def test_endpoint_safe_dimension_and_numeric_samples(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            for r in (36, 37, 100, 1000):
                left_log_x = mp.mpf(r**5) + mp.log(2)
                right_log_x = mp.mpf((r + 1) ** 5) + mp.log(2) - mp.mpf(
                    "1e-60"
                )
                for log_x in (left_log_x, right_log_x):
                    self.assertTrue(endpoint_dimension_bracket_holds(log_x, r))
                    self.assertGreater(
                        dimension_normalization_ratio(log_x, r),
                        mp.mpf(63) / 64,
                    )
                    self.assertGreater(
                        actual_r_scale_ratio(log_x),
                        mp.mpf(104) / 105,
                    )
                    self.assertGreater(
                        combined_normalization_ratio(log_x, r),
                        mp.mpf(39) / 40,
                    )
        finally:
            mp.mp.dps = old_dps

    def test_wrong_dimension_or_small_domain_fails_closed(self) -> None:
        log_x = mp.mpf(36**5) + mp.log(2)
        with self.assertRaises(ValueError):
            endpoint_dimension_bracket_holds(log_x, 35)
        with self.assertRaises(ValueError):
            dimension_normalization_ratio(log_x, 37)
        with self.assertRaises(ValueError):
            actual_r_scale_ratio(1)
        with self.assertRaises(TypeError):
            coarse_c_lower_multiplier(1.04)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            coarse_c_lower_multiplier(0)

    def test_certificate_closes_only_the_transfer(self) -> None:
        cert = dimension_coefficient_transfer_certificate()
        self.assertEqual(cert.minimum_endpoint_dimension, 36)
        self.assertTrue(cert.exact_elementary_certificate)
        self.assertTrue(cert.dyadic_dimension_admissibility_closed)
        self.assertTrue(cert.actual_r_scale_correction_included)
        self.assertTrue(cert.asymptotic_sono_c_preserved)
        self.assertTrue(cert.finite_c_preserved_under_sigma_gate)
        for value in (
            cert.explicit_sigma_gate_cutoff_closed,
            cert.full_weight_moment_package_closed,
            cert.common_exceptional_b_closed,
            cert.exact_count_transfer_closed,
            cert.hypothesis1_clause2_closed,
            cert.proposition92_closed,
            cert.siv_07_closed,
            cert.siv_08_closed,
            cert.x_cert_ready,
            cert.actual_prime_experiment_performed,
        ):
            self.assertFalse(value)

        status = self.contract["status_after_this_gate"]
        self.assertEqual(
            status["h1c_1b_1a"],
            "CLOSED_FOR_ASYMPTOTIC_COEFFICIENT_AND_PARAMETERIZED_FINITE_SIGMA_GATE",
        )
        self.assertEqual(
            status["siv_03_sigma_y_cutoff"],
            "RATE_MISSING_TARGET_26_OVER_25_FIXED",
        )
        self.assertEqual(status["siv_07"], "HARD_BLOCKER")
        self.assertEqual(status["siv_08"], "HARD_BLOCKER")
        self.assertEqual(status["numerical_x_cert"], "OPEN")
        self.assertTrue(
            self.contract["slack_accounting"][
                "sono_final_2e_minus_17_coefficient_preserved_asymptotically"
            ]
        )
        self.assertFalse(
            self.contract["slack_accounting"][
                "explicit_sigma_y_cutoff_available"
            ]
        )

    def test_source_hashes_are_reproducible(self) -> None:
        for source in self.contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
                source["key"],
            )

    def test_predecessor_and_t1_are_synchronized_fail_closed(self) -> None:
        predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        successor = predecessor["successor_dimension_coefficient_transfer"]
        self.assertEqual(successor["id"], "H1c-1b.1a")
        self.assertEqual(successor["outcome"], self.contract["outcome"])
        self.assertTrue(successor["asymptotic_sono_coefficient_preserved"])
        self.assertFalse(successor["explicit_sigma_cutoff_closed"])
        self.assertFalse(successor["numerical_x_cert_ready"])
        self.assertTrue(
            predecessor["successor_sigma_y_cutoff"][
                "explicit_sigma_cutoff_closed"
            ]
        )
        self.assertEqual(predecessor["next_gate"]["id"], "H1c-1b.2")

        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(
            rows["SIV-03"]["explicit_bound"],
            "sigma*y<(1001000/998001)*80c*x*log_2 x"
            "<(26/25)*80c*x*log_2 x",
        )
        self.assertEqual(rows["SIV-03"]["status"], "EXPLICIT")
        self.assertIn("26/25", rows["SIV-03"]["notes"])
        self.assertIn("r_T", rows["SIV-05"]["notes"])
        self.assertEqual(rows["SIV-07"]["status"], "HARD_BLOCKER")
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertEqual(rows["FIN-05"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
