"""Regression checks for the H1b-1b-2a actual-call lower-bound theorem."""

from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    LOCAL_FAMILY_ADJUSTED_LINEAR,
    LOCAL_FAMILY_LINEAR,
    LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1,
    LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
    MAYNARD_ACTUAL_LOCAL_FAMILIES,
    MINIMUM_EXCLUDED_INTEGER_K_GE_2,
    elementary_cgamma_lower_bound,
    excluded_totient_ratio,
    maynard_base_log_excluded_integer_upper,
    maynard_local_denominator,
    maynard_log_excluded_integer_upper,
    maynard_uniform_cgamma_evaluation,
    nonexcluded_local_factor_certificate,
    rosser_schoenfeld_cgamma_lower_bound,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2a_actual_local_factor_lower_bound_v1.json"
)


class H1b1b2aLocalFactorLowerBoundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_contract_is_fail_closed(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.1.0")
        self.assertEqual(
            self.contract["outcome"],
            "ACTUAL_LOCAL_FACTORS_AND_ALL_TRACED_APPLICATION_EXCLUDED_MODULI_"
            "PROJECT_PARAMETERIZED_EXPLICIT_BASE_CONSTANT_AND_RFOLD_OPEN",
        )
        self.assertEqual(len(self.contract["application_map"]), 10)
        self.assertEqual(
            {row["id"] for row in self.contract["actual_local_families"]},
            MAYNARD_ACTUAL_LOCAL_FAMILIES,
        )
        route = self.contract["route_status"]
        self.assertFalse(route["explicit_lower_bound_route_primary_candidate"])
        self.assertTrue(route["explicit_lower_bound_route_selected"])
        self.assertTrue(route["all_actual_application_overheads_certified"])
        self.assertFalse(route["abstract_g_equals_p_plus_Ok_lemma_closed"])
        self.assertFalse(route["C3_abs_numeric_multiplier_recovered"])
        self.assertFalse(route["corrected_rfold_composition_closed"])
        self.assertFalse(route["numerical_route_complete"])
        self.assertEqual(self.contract["parent_status"]["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(self.contract["parent_status"]["X_cert"], "OPEN")
        self.assertFalse(
            self.contract["next_gate"]["ready_for_threshold_calculator"]
        )
        self.assertFalse(
            self.contract["next_gate"]["ready_for_actual_prime_experiment"]
        )

    def test_exact_denominator_margins_match_the_proof(self) -> None:
        samples = ((5, 1), (11, 2), (101, 7), (1009, 36))
        for prime, root_count in samples:
            linear = maynard_local_denominator(
                prime, root_count, LOCAL_FAMILY_LINEAR
            )
            square_minus = maynard_local_denominator(
                prime,
                root_count,
                LOCAL_FAMILY_SQUARE_OVER_P_MINUS_1,
            )
            square_plus = maynard_local_denominator(
                prime,
                root_count,
                LOCAL_FAMILY_SQUARE_OVER_P_PLUS_A_MINUS_2,
            )
            adjusted = maynard_local_denominator(
                prime, root_count, LOCAL_FAMILY_ADJUSTED_LINEAR
            )
            p_minus_a = Fraction(prime - root_count)

            self.assertEqual(p_minus_a - linear, 0)
            self.assertEqual(
                p_minus_a - square_minus,
                Fraction(
                    (prime - root_count) * (root_count - 1),
                    prime - 1,
                ),
            )
            self.assertEqual(
                p_minus_a - square_plus,
                Fraction(
                    2 * (prime - root_count) * (root_count - 1),
                    prime + root_count - 2,
                ),
            )
            self.assertEqual(
                p_minus_a - adjusted,
                Fraction(root_count - 1, prime - 1),
            )

    def test_nonexcluded_factor_is_at_least_one_on_exact_grid(self) -> None:
        primes = (2, 3, 5, 7, 11, 17, 31, 101)
        rows = 0
        for prime in primes:
            for root_count in range(1, prime):
                for previous in range(root_count):
                    for family in MAYNARD_ACTUAL_LOCAL_FAMILIES:
                        certificate = nonexcluded_local_factor_certificate(
                            prime,
                            root_count,
                            previous,
                            family,
                        )
                        expected_margin = Fraction(
                            prime
                            - 1
                            - (certificate.denominator + previous),
                            prime * (certificate.denominator + previous),
                        )
                        self.assertEqual(
                            certificate.local_factor_margin,
                            expected_margin,
                        )
                        self.assertGreaterEqual(certificate.local_factor_margin, 0)
                        rows += 1
        self.assertEqual(rows, 22_964)

    def test_linear_extreme_attains_one(self) -> None:
        certificate = nonexcluded_local_factor_certificate(
            101,
            36,
            35,
            LOCAL_FAMILY_LINEAR,
        )
        self.assertEqual(certificate.local_factor, 1)
        self.assertEqual(certificate.local_factor_margin, 0)

    def test_excluded_product_is_exact_totient_ratio(self) -> None:
        self.assertEqual(MINIMUM_EXCLUDED_INTEGER_K_GE_2, 210)
        self.assertEqual(
            excluded_totient_ratio((2, 3, 5, 7)),
            Fraction(8, 35),
        )
        with self.assertRaises(ValueError):
            excluded_totient_ratio((2, 2, 3))
        with self.assertRaises(ValueError):
            excluded_totient_ratio((2, 9))

    def test_base_log_q_upper_is_worst_at_first_iteration(self) -> None:
        values = [
            maynard_base_log_excluded_integer_upper(
                k=36,
                r=12,
                iteration=iteration,
                alpha="0.01",
                theta="0.333333333333333333333333333333333333",
                log_r="1000",
            )
            for iteration in range(12)
        ]
        self.assertTrue(all(left > right for left, right in zip(values, values[1:])))
        self.assertTrue(
            all(left - right == mp.mpf("1000") for left, right in zip(values, values[1:]))
        )

    def test_application_overhead_is_required_and_added_exactly(self) -> None:
        parameters = {
            "k": 36,
            "r": 12,
            "iteration": 0,
            "alpha": "0.01",
            "theta": "0.333333333333333333333333333333333333",
            "log_r": "1000",
        }
        base = maynard_base_log_excluded_integer_upper(**parameters)
        with self.assertRaises(TypeError):
            maynard_log_excluded_integer_upper(**parameters)
        self.assertEqual(
            maynard_log_excluded_integer_upper(
                **parameters,
                application_log_overhead="37.5",
            ),
            base + mp.mpf("37.5"),
        )
        with self.assertRaises(ValueError):
            maynard_log_excluded_integer_upper(
                **parameters,
                application_log_overhead="-0.1",
            )

    def test_rosser_bound_dominates_elementary_relaxation(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for log_upper in (mp.log(210), mp.mpf("100"), mp.mpf("1e9")):
                rosser = rosser_schoenfeld_cgamma_lower_bound(log_upper)
                elementary = elementary_cgamma_lower_bound(log_upper)
                self.assertGreater(rosser, elementary)
                self.assertGreater(elementary, 0)

            evaluation = maynard_uniform_cgamma_evaluation(
                k=36,
                r=12,
                iteration=0,
                alpha="0.01",
                theta="0.333333333333333333333333333333333333",
                log_r="1000",
                application_log_overhead="0",
            )
            self.assertGreater(
                evaluation.rosser_schoenfeld_lower_bound,
                evaluation.elementary_lower_bound,
            )
        finally:
            mp.mp.dps = old_dps

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            maynard_local_denominator(5, 5, LOCAL_FAMILY_LINEAR)
        with self.assertRaises(ValueError):
            maynard_local_denominator(5, 1, "p_plus_unspecified_Ok")
        with self.assertRaises(ValueError):
            nonexcluded_local_factor_certificate(
                5,
                2,
                2,
                LOCAL_FAMILY_LINEAR,
            )
        with self.assertRaises(ValueError):
            maynard_log_excluded_integer_upper(
                k=36,
                r=12,
                iteration=12,
                alpha="0.01",
                theta="0.333",
                log_r="1000",
                application_log_overhead="0",
            )
        with self.assertRaises(ValueError):
            rosser_schoenfeld_cgamma_lower_bound(mp.log(209))


if __name__ == "__main__":
    unittest.main()
