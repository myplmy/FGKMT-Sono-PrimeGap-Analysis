"""Regression checks for the H1b-2a.2 P9.4 distribution reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b2a2_proposition94_distribution import (
    H1B2A2_MINIMUM_K,
    consecutive_interval_discrepancy,
    divisor_summatory_log_upper,
    proposition94_distribution_certificate,
    squarefree_assignment_multiplicity_upper,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b2a2_Proposition94_distribution_error_v1.json"
)


class H1b2a2Proposition94DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_consecutive_integer_interval_discrepancy_is_exact(self) -> None:
        for start in range(-5, 8):
            for size in range(1, 16):
                stop = start + size
                for modulus in range(1, 12):
                    for residue in range(modulus):
                        cert = consecutive_interval_discrepancy(
                            start,
                            stop,
                            modulus,
                            residue,
                        )
                        brute = sum(
                            value % modulus == residue
                            for value in range(start, stop)
                        )
                        expected = abs(
                            Fraction(brute, 1) - Fraction(size, modulus)
                        )
                        self.assertEqual(cert.residue_count, brute)
                        self.assertEqual(cert.discrepancy, expected)
                        self.assertTrue(cert.at_most_one)
                        self.assertLessEqual(cert.discrepancy, 1)

    def test_squarefree_assignment_count_has_no_hidden_constant(self) -> None:
        k = 2
        prime_count = 3
        choices = tuple(
            (coordinate, pattern)
            for coordinate in range(k + 1)
            for pattern in ("d", "e", "both")
        )
        assignments = set(itertools.product(choices, repeat=prime_count))
        self.assertEqual(
            len(assignments),
            squarefree_assignment_multiplicity_upper(k, prime_count),
        )
        self.assertEqual(len(assignments), (3 * (k + 1)) ** prime_count)

    def test_divisor_summatory_majorant_on_small_exact_ranges(self) -> None:
        for dimension in (1, 2, 3, 5):
            for endpoint in (2, 3, 5, 10, 20):
                exact = 0
                for values in itertools.product(
                    range(1, endpoint),
                    repeat=dimension,
                ):
                    if math.prod(values) < endpoint:
                        exact += 1
                log_upper = divisor_summatory_log_upper(
                    dimension,
                    mp.log(endpoint),
                )
                self.assertLessEqual(mp.mpf(exact), mp.exp(log_upper))

    def test_actual_fmt_gate_closes_only_the_distribution_child(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            for k in (36, 100):
                cert = proposition94_distribution_certificate(
                    k=k,
                    alpha=2,
                    theta=mp.mpf(1) / 3,
                )
                self.assertGreater(cert.decay_exponent, 0)
                self.assertEqual(
                    cert.assignment_divisor_dimension,
                    3 * (k + 1),
                )
                self.assertTrue(cert.modulus_gate_passed)
                self.assertTrue(cert.smooth_gate_passed)
                self.assertTrue(cert.sharp_gate_passed)
                self.assertTrue(cert.analytic_gate_passed)
                self.assertTrue(cert.direct_relative_error_gate_passed)
                self.assertTrue(
                    cert.distribution_error_closed_at_supplied_gate
                )
                self.assertLessEqual(cert.log_relative_error_upper, 0)
                self.assertFalse(cert.hypothesis1_clause1_multiplier_required)
                self.assertFalse(cert.hypothesis1_clause3_multiplier_required)
                self.assertFalse(cert.proposition_94_closed)
                self.assertFalse(cert.siv_07_closed)
                self.assertFalse(cert.x_cert_ready)
                self.assertFalse(cert.theorem_claimed)
        finally:
            mp.mp.dps = old_dps

    def test_small_log_x_fails_closed(self) -> None:
        cert = proposition94_distribution_certificate(
            k=36,
            alpha=2,
            theta=mp.mpf(1) / 3,
            log_x=10,
        )
        self.assertFalse(cert.modulus_gate_passed)
        self.assertFalse(cert.smooth_gate_passed)
        self.assertFalse(cert.sharp_gate_passed)
        self.assertFalse(cert.distribution_error_closed_at_supplied_gate)
        self.assertFalse(cert.proposition_94_closed)
        self.assertFalse(cert.x_cert_ready)

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            proposition94_distribution_certificate(
                k=H1B2A2_MINIMUM_K - 1,
                alpha=2,
                theta=Fraction(1, 3),
            )
        with self.assertRaises(ValueError):
            proposition94_distribution_certificate(
                k=36,
                alpha=2,
                theta=Fraction(15, 16),
            )
        with self.assertRaises(ValueError):
            consecutive_interval_discrepancy(1, 1, 2, 0)
        with self.assertRaises(ValueError):
            squarefree_assignment_multiplicity_upper(2, -1)
        with self.assertRaises(ValueError):
            divisor_summatory_log_upper(0, 1)

    def test_contract_sources_and_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "ACTUAL_INTEGER_INTERVAL_DISTRIBUTION_ERROR_PARAMETERIZED_EXPLICIT",
        )
        for source in contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )
        transitions = contract["status_after_this_gate"]
        self.assertEqual(
            transitions["H1B2A-P94-DISTRIBUTION"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(transitions["H1B-P94"], "RATE_MISSING")
        self.assertEqual(transitions["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(transitions["X_cert"], "OPEN")
        self.assertEqual(
            contract["h1b2a3_successor_contract"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json",
        )
        self.assertEqual(
            contract["successor_status_update"]["H1B-P94"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertFalse(contract["hypothesis1_package_closed"])
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["threshold_calculator_created"])


if __name__ == "__main__":
    unittest.main()
