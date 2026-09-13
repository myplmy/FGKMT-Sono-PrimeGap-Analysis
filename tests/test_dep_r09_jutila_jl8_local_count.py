"""Fail-closed checks for the actual Jutila Lemma 8 source replacement."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl8_local_count import (
    MAX_RADIUS,
    actual_strip_radius,
    exact_slacks,
    kappa,
    local_zero_count_envelope,
    stechkin_kernel,
    strip_to_selected_system_envelope,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_Lemma8_local_count_v1.json"
)


class DepR09JutilaLemma8LocalCountTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 100

    def test_source_hashes_are_exact_when_audit_copy_is_present(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if not locator:
                continue
            path = REPO_ROOT / locator
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
                self.assertEqual(
                    hashlib.sha256(data).hexdigest(),
                    source["audit_copy_sha256"],
                    source["key"],
                )

    def test_exact_budget_slacks_are_strictly_positive(self):
        slacks = exact_slacks()
        self.assertEqual(slacks["kernel_slack"], Fraction(23, 952))
        self.assertEqual(slacks["constant_slack"], Fraction(3722, 13125))
        self.assertEqual(slacks["log_coefficient_slack"], Fraction(1, 5))
        self.assertGreater(slacks["constant_slack"], 0)
        self.assertLess(kappa(), mp.mpf(3) / 10)

    def test_kernel_lower_bound_on_boundary_and_dense_grid(self):
        radii = [mp.mpf(1) / 21, mp.mpf("0.01"), mp.mpf("1e-6")]
        for radius in radii:
            lower = mp.mpf(3) / (8 * radius)
            for i in range(41):
                beta = 1 - radius + radius * i / 40
                for j in range(-20, 21):
                    offset = radius * j / 40
                    self.assertGreaterEqual(
                        stechkin_kernel(radius, beta, offset),
                        lower,
                    )

    def test_actual_strip_radius_stays_in_mccurley_range(self):
        for theta in (mp.mpf(1) / 21, mp.mpf("0.01"), mp.mpf("0.001")):
            log_d = theta ** -2
            for defect in (theta, theta / 2, theta**3):
                radius = actual_strip_radius(defect, log_d)
                self.assertLessEqual(radius, theta)
                self.assertLessEqual(radius, mp.mpf(MAX_RADIUS.numerator) / MAX_RADIUS.denominator)

    def test_local_and_even_odd_transfer_envelopes(self):
        radius = mp.mpf("0.01")
        envelope = local_zero_count_envelope(radius, 10**6, mp.mpf("1e9"))
        self.assertGreater(envelope, 3)
        self.assertEqual(strip_to_selected_system_envelope(envelope, 7), 14 * envelope)
        with self.assertRaises(ValueError):
            local_zero_count_envelope(mp.mpf(1) / 20, 3, 1)

    def test_scope_is_actual_near_one_only_and_roots_fail_closed(self):
        status = self.ledger["status"]
        self.assertEqual(
            status["jl8_actual_near_one"],
            "ACTUAL_APPLICATION_EXPLICIT_SOURCE_REPLACEMENT",
        )
        self.assertEqual(status["jl8_printed_general"], "OPEN")
        self.assertEqual(status["jutila_terminal_density"], "OPEN")
        for key in (
            "pap_11_closed",
            "dep_r09_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(self.ledger[key], key)


if __name__ == "__main__":
    unittest.main()
