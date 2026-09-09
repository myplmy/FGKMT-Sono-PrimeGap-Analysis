"""Regression tests for the H1c-1b.4a Bordignon source audit."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import mpmath as mp

from source.h1c1b4a_bordignon_source_normalization import (
    ARXIV_V1_EQC_FIRST_TERM,
    FINAL_EQ33_FIRST_TERM,
    PROJECT_DIRECT_FIRST_TERM,
    UnresolvedBordignonConstantError,
    direct_remainder_coefficient_log,
    log_x0_from_y0,
    numerical_theorem12_constant_from_printed_source,
    q_envelope_height_identity_log,
    structural_certificate,
    y0_from_log_x0,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b4a_Bordignon_source_normalization_v1.json"
)


class H1c1b4aSourceNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_x0_y0_round_trip_stays_on_log_scale(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            for y0 in (mp.mpf(2), mp.mpf("7.4"), mp.mpf(1000)):
                log_x0 = log_x0_from_y0(y0)
                self.assertTrue(mp.almosteq(y0_from_log_x0(log_x0), y0))
        finally:
            mp.mp.dps = old_dps

    def test_direct_remainder_algebra_and_height_identity(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            log_x = mp.mpf(100)
            alpha1 = mp.mpf(7)
            alpha2 = mp.mpf(4)
            log_ratio = mp.log(mp.mpf("1.25e-80"))
            explicit_q = direct_remainder_coefficient_log(
                log_x,
                alpha1,
                alpha2,
                log_ratio,
                q=97,
            )
            self.assertTrue(
                mp.almosteq(
                    explicit_q,
                    log_ratio + mp.log(97) + alpha2 * mp.log(log_x),
                )
            )
            direct, via_height = q_envelope_height_identity_log(
                log_x, alpha1, alpha2, log_ratio
            )
            self.assertTrue(mp.almosteq(direct, via_height))
            self.assertTrue(
                mp.almosteq(
                    direct,
                    log_ratio + (alpha1 + alpha2) * mp.log(log_x),
                )
            )
        finally:
            mp.mp.dps = old_dps

    def test_malformed_source_formula_is_fail_closed(self) -> None:
        self.assertIn("R_star", FINAL_EQ33_FIRST_TERM)
        self.assertNotIn("/x", FINAL_EQ33_FIRST_TERM)
        self.assertIn("T/(x", ARXIV_V1_EQC_FIRST_TERM)
        self.assertIn("q*R_star", PROJECT_DIRECT_FIRST_TERM)
        with self.assertRaises(UnresolvedBordignonConstantError):
            numerical_theorem12_constant_from_printed_source(36)

    def test_structural_flags_do_not_overpromote(self) -> None:
        cert = structural_certificate()
        self.assertTrue(cert.x0_y0_type_mapping_closed)
        self.assertTrue(cert.direct_theorem34_to_theorem12_remainder_algebra_closed)
        self.assertFalse(cert.final_eq33_first_term_dimensionally_valid)
        self.assertFalse(cert.arxiv_v1_first_term_adopted_as_final)
        self.assertFalse(cert.final_table_covers_actual_growing_a)
        for name in (
            "numerical_theorem12_constant_upper_closed",
            "bordignon_constant_normalization_resolved",
            "represented_prime_density_lower_bound_closed",
            "full_remainder_absorption_closed",
            "hypothesis1_clause2_closed",
            "proposition92_closed",
            "siv_08_closed",
            "x_cert_ready",
            "actual_prime_experiment_performed",
        ):
            self.assertFalse(getattr(cert, name), name)

    def test_machine_contract_and_source_hashes(self) -> None:
        self.assertEqual(
            self.contract["outcome"],
            "TYPE_MAPPING_AND_DIRECT_REMAINDER_ALGEBRA_CLOSED_NUMERICAL_C_A_BLOCKED",
        )
        self.assertFalse(
            self.contract["status_after_this_gate"]["numerical_C_A_upper_closed"]
        )
        self.assertFalse(self.contract["limits"]["numerical_x_cert_ready"])
        for source in self.contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
                source["key"],
            )

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            y0_from_log_x0(0)
        with self.assertRaises(ValueError):
            direct_remainder_coefficient_log(1, 2, 3, -10)
        with self.assertRaises(ValueError):
            direct_remainder_coefficient_log(100, 2, 3, -10, q=100_001)
        with self.assertRaises(TypeError):
            direct_remainder_coefficient_log(100, 2, 3, -10, q=True)


if __name__ == "__main__":
    unittest.main()
