"""Regression tests for H1c-1b.4b density and elementary constants."""

from __future__ import annotations

import hashlib
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b4b_density_constants import (
    ROSSER_SCHOENFELD_INTERVAL_MINIMUM,
    SAFE_C0_UPPER,
    SAFE_C1_UPPER,
    bordignon_c0_rational_upper,
    bordignon_c1_telescope_upper,
    density_margin_over_project_lower,
    elementary_transcendental_bound_checks,
    half_open_prime_density_source_lower,
    project_half_open_density_lower,
    structural_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b4b_density_constants_v1.json"
)


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % d for d in range(3, math.isqrt(value) + 1, 2))


class H1c1b4bDensityConstantsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_rational_c0_proof_chain(self) -> None:
        checks = elementary_transcendental_bound_checks()
        self.assertTrue(all(checks.values()), checks)
        upper = bordignon_c0_rational_upper()
        self.assertIsInstance(upper, Fraction)
        self.assertLess(upper, SAFE_C0_UPPER)
        self.assertGreater(upper, 48)

    def test_c1_telescope_and_small_prime_partial_products(self) -> None:
        self.assertEqual(bordignon_c1_telescope_upper(), SAFE_C1_UPPER)
        product = Fraction(1, 1)
        for prime in range(2, 500):
            if _is_prime(prime):
                product *= 1 + Fraction(1, prime * (prime - 1))
        self.assertLess(product, SAFE_C1_UPPER)

    def test_half_open_density_source_and_project_bound(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            floor = 36**5
            source_lower = half_open_prime_density_source_lower(floor)
            project_lower = project_half_open_density_lower(floor)
            self.assertGreater(source_lower, project_lower)
            self.assertTrue(
                mp.almosteq(
                    density_margin_over_project_lower(floor),
                    source_lower - project_lower,
                )
            )
            for log_t in (floor, 40**5, mp.mpf("1e12")):
                self.assertGreater(density_margin_over_project_lower(log_t), 0)
        finally:
            mp.mp.dps = old_dps

    def test_source_endpoint_threshold_is_twenty_and_a_half(self) -> None:
        self.assertEqual(ROSSER_SCHOENFELD_INTERVAL_MINIMUM, Fraction(41, 2))
        with self.assertRaises(ValueError):
            half_open_prime_density_source_lower(mp.log(mp.mpf("20.49")))
        self.assertGreater(
            half_open_prime_density_source_lower(mp.log(mp.mpf("20.5"))),
            0,
        )

    def test_structural_certificate_does_not_overpromote(self) -> None:
        cert = structural_certificate()
        self.assertEqual(cert.sieve_dimension_r, 36)
        self.assertEqual(cert.log_t_floor, 36**5)
        self.assertTrue(cert.endpoint_loss_at_most_one)
        self.assertTrue(cert.represented_prime_density_lower_bound_closed)
        self.assertEqual(cert.bordignon_c0_upper, 49)
        self.assertTrue(cert.bordignon_c0_upper_closed)
        self.assertEqual(cert.bordignon_c1_upper, 3)
        self.assertTrue(cert.bordignon_c1_upper_closed)
        for name in (
            "numerical_theorem12_constant_upper_closed",
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
            "EXACT_HALF_OPEN_DENSITY_AND_C0_C1_UPPERS_CLOSED_C_A_AND_ABSORPTION_OPEN",
        )
        self.assertTrue(
            self.contract["status_after_this_gate"]
            ["represented_prime_density_lower_bound_closed"]
        )
        self.assertFalse(
            self.contract["status_after_this_gate"]["full_remainder_absorption_closed"]
        )
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
            project_half_open_density_lower(35**5)
        with self.assertRaises(ValueError):
            structural_certificate(35)
        with self.assertRaises(TypeError):
            structural_certificate(True)


if __name__ == "__main__":
    unittest.main()
