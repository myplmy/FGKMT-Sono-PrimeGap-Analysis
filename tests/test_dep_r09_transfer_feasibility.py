"""Fail-closed tests for the DEP-R09 transfer-feasibility audit."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_transfer_feasibility import (
    D_CAPACITY_MINIMUM,
    THETA_ENDPOINT,
    build_diagnostic,
    capacity_hybrid_floor,
    first_slice_delta_upper,
    hybrid_first_slice_lower,
    jutila_first_slice_lower,
    pap_near_budget,
    positive_weight_zero_frequency_lower,
    required_attenuation,
    required_support_log10,
    signed_weight_condition_number_lower,
)
from source.dep_r09_modern_density_screen import (
    D_CAPACITY_ENDPOINT,
    ZERO_FREE_C1,
    ramare_direct_slice_lower,
    ramare_source_range_log_x,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_transfer_feasibility_v1.json"
)


class DepR09TransferFeasibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_capacity_hybrid_floor_occurs_at_d186_and_exceeds_8602(self):
        with mp.workdps(100):
            d_floor, floor = capacity_hybrid_floor()
            self.assertEqual(d_floor, D_CAPACITY_ENDPOINT)
            self.assertGreater(floor, mp.mpf("8602"))
            self.assertGreater(floor, pap_near_budget())

            rows = []
            for d in range(D_CAPACITY_MINIMUM, D_CAPACITY_ENDPOINT + 1):
                source_min = ramare_source_range_log_x(d)
                self.assertLess(
                    abs(source_min - d * mp.log(10)), mp.mpf("1e-90")
                )
                rows.append(hybrid_first_slice_lower(source_min, d))
            for before, after in zip(rows, rows[1:]):
                self.assertGreater(before, after)

    def test_hybrid_lower_is_non_decreasing_with_log_x_for_fixed_d(self):
        with mp.workdps(100):
            source_min = ramare_source_range_log_x()
            values = [
                hybrid_first_slice_lower(source_min * factor)
                for factor in (1, 2, 10, 100)
            ]
            for before, after in zip(values, values[1:]):
                self.assertLessEqual(before, after)

    def test_jutila_floor_uses_tightened_coefficient(self):
        with mp.workdps(100):
            lower = jutila_first_slice_lower()
            self.assertGreater(lower, mp.mpf("1.267e10"))
            self.assertLess(lower, mp.mpf("1.268e10"))

    def test_fixed_positive_smoothing_cannot_supply_required_attenuation(self):
        with mp.workdps(100):
            _, floor = capacity_hybrid_floor()
            target = required_attenuation(floor)
            theta = mp.mpf(THETA_ENDPOINT.numerator) / THETA_ENDPOINT.denominator
            source_min = ramare_source_range_log_x()
            delta_actual = first_slice_delta_upper(source_min)
            theta_lower = positive_weight_zero_frequency_lower(theta)
            actual_lower = positive_weight_zero_frequency_lower(delta_actual)

            self.assertLess(target, mp.mpf("1.574e-5"))
            self.assertGreater(theta_lower, mp.mpf("0.967"))
            self.assertGreater(actual_lower, mp.mpf("0.995"))
            self.assertGreater(theta_lower / target, mp.mpf("61400"))
            self.assertGreater(actual_lower / target, mp.mpf("63200"))

    def test_required_support_and_signed_condition_numbers_are_large(self):
        with mp.workdps(100):
            _, floor = capacity_hybrid_floor()
            target = required_attenuation(floor)
            theta = mp.mpf(1) / 21
            delta_actual = first_slice_delta_upper(ramare_source_range_log_x())
            self.assertGreater(required_support_log10(target, theta), 100)
            self.assertGreater(required_support_log10(target, delta_actual), 806)
            self.assertGreater(
                signed_weight_condition_number_lower(target, theta), 30
            )
            self.assertGreater(
                signed_weight_condition_number_lower(target, delta_actual), 240
            )

    def test_diagnostic_is_fail_closed_and_does_not_change_global_precision(self):
        before = mp.mp.dps
        diagnostic = build_diagnostic()
        self.assertEqual(mp.mp.dps, before)
        self.assertFalse(diagnostic.pointwise_minimum_passes_current_budget)
        self.assertFalse(
            diagnostic.fixed_nonnegative_source_blind_uniform_envelope_passes_current_budget
        )
        self.assertFalse(diagnostic.all_smoothing_or_cancellation_proofs_ruled_out)
        self.assertFalse(
            diagnostic.cancellation_recoverable_after_absolute_value_reduction
        )
        self.assertTrue(diagnostic.new_pre_absolute_value_uniform_theorem_required)
        self.assertFalse(diagnostic.public_numerical_cancellation_drop_in_found)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.fixed_2e_minus_17_independently_certified)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.threshold_calculator_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_machine_ledger_preserves_scope_and_source_boundaries(self):
        self.assertEqual(
            self.ledger["outcome"],
            "POINTWISE_MINIMUM_AND_SOURCE_BLIND_FIXED_NONNEGATIVE_SMOOTHING_FAIL_CURRENT_PAP_CERTIFICATE_NEW_PRE_ABSOLUTE_VALUE_THEOREM_REQUIRED",
        )
        statuses = self.ledger["status_after_this_gate"]
        self.assertTrue(statuses["pointwise_minimum_screen_complete"])
        self.assertTrue(statuses["fixed_nonnegative_smoothing_screen_complete"])
        self.assertFalse(statuses["all_smoothing_impossible"])
        self.assertFalse(statuses["all_cancellation_proofs_impossible"])
        self.assertFalse(statuses["public_numerical_cancellation_drop_in_found"])
        self.assertFalse(statuses["pap_11_closed"])
        self.assertFalse(statuses["numerical_x_cert_ready"])
        self.assertFalse(statuses["user_compute_required_now"])

    def test_source_hashes_match_for_local_primary_sources(self):
        checked = 0
        for source in self.ledger["source_registry"]:
            locator = source.get("locator")
            expected = source.get("sha256")
            if not locator or not expected:
                continue
            path = REPO_ROOT / locator
            self.assertTrue(path.is_file(), locator)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
            checked += 1
        self.assertGreaterEqual(checked, 3)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            hybrid_first_slice_lower(100, 20)
        with self.assertRaises(TypeError):
            hybrid_first_slice_lower(100, 21.0)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            hybrid_first_slice_lower(0)
        with self.assertRaises(TypeError):
            pap_near_budget(Fraction(2).numerator)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pap_near_budget(Fraction(0))
        for bad in (0, -1, mp.inf, mp.nan):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    positive_weight_zero_frequency_lower(bad)
        with self.assertRaises(ValueError):
            positive_weight_zero_frequency_lower(1, Fraction(1, 2))
        with self.assertRaises(ValueError):
            required_support_log10(1, Fraction(1, 21))
        with self.assertRaises(ValueError):
            signed_weight_condition_number_lower(
                Fraction(1, 2), Fraction(1, 21), 1
            )


if __name__ == "__main__":
    unittest.main()
