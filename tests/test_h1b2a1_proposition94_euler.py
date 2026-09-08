"""Regression checks for the H1b-2a.1 exact Euler normalization."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b2a1_proposition94_euler import (
    H1B2A1_MINIMUM_K,
    canonical_ratio_local_certificate,
    euler_tail_certificate,
    exact_star_denominator,
    pre_y_local_certificate,
    sharp_r0_local_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b2a1_Proposition94_Euler_normalization_v1.json"
)


class H1b2a1Proposition94EulerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_star_denominator(self) -> None:
        self.assertEqual(exact_star_denominator(101, 7), Fraction(94 * 94, 106))

    def test_pre_y_and_sharp_local_identities_and_bounds(self) -> None:
        for k in (36, 50, 100):
            for prime in (2 * k * k + 1, 2 * k * k + 17, 3 * k * k + 1):
                for omega in range(k + 1):
                    pre = pre_y_local_certificate(k, prime, omega)
                    sharp = sharp_r0_local_certificate(k, prime, omega)
                    self.assertTrue(pre.identity_verified)
                    self.assertTrue(pre.upper_bound_verified)
                    self.assertTrue(sharp.identity_verified)
                    self.assertTrue(sharp.upper_bound_verified)
                    self.assertGreaterEqual(pre.exact_excess, 0)
                    self.assertGreaterEqual(sharp.exact_excess, 0)

    def test_prime_dividing_b_has_unit_sharp_factor(self) -> None:
        cert = sharp_r0_local_certificate(
            36,
            2 * 36 * 36 + 1,
            0,
            prime_divides_b=True,
        )
        self.assertEqual(cert.omega_star, 1)
        self.assertEqual(cert.exact_factor, 1)
        self.assertEqual(cert.exact_excess, 0)

    def test_canonical_ratio_identities_and_bounds(self) -> None:
        for k in (36, 50, 100):
            for prime in (2 * k * k + 1, 2 * k * k + 17, 3 * k * k + 1):
                for omega in range(k + 1):
                    for collision in (False, True):
                        cert = canonical_ratio_local_certificate(
                            k,
                            prime,
                            omega,
                            collides_with_extra_form=collision,
                        )
                        self.assertTrue(cert.identity_verified)
                        self.assertTrue(cert.upper_bound_verified)
                        self.assertGreaterEqual(cert.exact_excess, 0)

    def test_natural_cutoff_product_bounds_and_fail_closed_state(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in (36, 100, 1_000):
                cert = euler_tail_certificate(k)
                self.assertEqual(cert.cutoff, 2 * k * k)
                self.assertEqual(cert.pre_y_log_tail_upper, Fraction(2, k))
                self.assertEqual(cert.sharp_r0_log_tail_upper, Fraction(2, k))
                self.assertEqual(cert.canonical_ratio_log_tail_upper, 2)
                self.assertEqual(
                    cert.final_two_products_log_tail_upper,
                    Fraction(2 * k + 2, k),
                )
                self.assertEqual(
                    cert.full_line_966_log_tail_upper,
                    Fraction(2 * k + 6, k),
                )
                self.assertTrue(cert.exact_local_factors_recovered)
                self.assertTrue(cert.final_euler_products_closed)
                self.assertFalse(cert.distribution_error_closed)
                self.assertFalse(cert.proposition_94_closed)
                self.assertFalse(cert.siv_07_closed)
                self.assertFalse(cert.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_later_cutoff_tightens_all_tail_bounds(self) -> None:
        base = euler_tail_certificate(36)
        later = euler_tail_certificate(36, 4 * 36 * 36)
        self.assertLess(later.pre_y_log_tail_upper, base.pre_y_log_tail_upper)
        self.assertLess(later.sharp_r0_log_tail_upper, base.sharp_r0_log_tail_upper)
        self.assertLess(
            later.canonical_ratio_log_tail_upper,
            base.canonical_ratio_log_tail_upper,
        )

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            euler_tail_certificate(H1B2A1_MINIMUM_K - 1)
        with self.assertRaises(ValueError):
            euler_tail_certificate(36, 2 * 36 * 36 - 1)
        with self.assertRaises(ValueError):
            pre_y_local_certificate(36, 2 * 36 * 36, 1)
        with self.assertRaises(ValueError):
            sharp_r0_local_certificate(
                36,
                2 * 36 * 36 + 1,
                1,
                prime_divides_b=True,
            )
        with self.assertRaises(ValueError):
            canonical_ratio_local_certificate(
                36,
                2 * 36 * 36 + 1,
                1,
                collides_with_extra_form=1,  # type: ignore[arg-type]
            )

    def test_contract_sources_and_parent_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "FINAL_EULER_NORMALIZATION_FINITE_COMPONENT_CLOSED_P94_PARENT_OPEN",
        )
        for source in contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )
        self.assertEqual(
            contract["status_after_this_gate"]["H1B2A-P94-FINAL-EULER"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertEqual(
            contract["status_after_this_gate"]["H1B-P94"],
            "RATE_MISSING",
        )
        self.assertEqual(
            contract["status_after_this_gate"]["SIV-07"],
            "HARD_BLOCKER",
        )
        self.assertEqual(contract["status_after_this_gate"]["X_cert"], "OPEN")
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["threshold_calculator_created"])


if __name__ == "__main__":
    unittest.main()
