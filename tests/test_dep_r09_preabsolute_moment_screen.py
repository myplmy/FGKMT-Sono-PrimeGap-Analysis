"""Fail-closed tests for the DEP-R09 pre-absolute source screen."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_preabsolute_moment_screen import (
    BENNETT_UNIFORM_C_PSI,
    D_CAPACITY_ENDPOINT,
    FIRST_PRIMORIAL_ABOVE_1E5,
    FIRST_PRIMORIAL_ABOVE_1E5_PHI,
    aggregate_second_moment_budget,
    akbary_hambrook_l1_floor_relative_to_x,
    bennett_relative_pap_error_envelope,
    bennett_required_cpsi_for_pap,
    bennett_required_d_for_maier_scale,
    build_diagnostic,
    natural_variance_budget_ratio,
    pap_near_budget,
    pointwise_second_moment_budget,
    sedunova_l1_floor_relative_to_x,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_preabsolute_moment_source_screen_v1.json"
)


class DepR09PreAbsoluteMomentScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_explicit_l1_certificate_floors_exceed_pap_budget(self):
        with mp.workdps(100):
            budget = pap_near_budget()
            akbary = akbary_hambrook_l1_floor_relative_to_x(4)
            sedunova = sedunova_l1_floor_relative_to_x(4)
            self.assertGreater(akbary, 600)
            self.assertGreater(sedunova, 1800)
            self.assertGreater(akbary / budget, 4500)
            self.assertGreater(sedunova / budget, 13_000)

    def test_bennett_large_q_cutoff_has_no_d_le_186_overlap(self):
        with mp.workdps(100):
            just_above_threshold = mp.mpf("100000.0000000001")
            required_at_edge = bennett_required_d_for_maier_scale(
                just_above_threshold
            )
            required_at_primorial = bennett_required_d_for_maier_scale(
                FIRST_PRIMORIAL_ABOVE_1E5
            )
            self.assertGreater(required_at_edge, 1257)
            self.assertGreater(required_at_primorial, 3702)
            self.assertGreater(required_at_edge, D_CAPACITY_ENDPOINT)

    def test_bennett_error_normalization_also_misses_printed_budget(self):
        with mp.workdps(100):
            envelope = bennett_relative_pap_error_envelope(
                FIRST_PRIMORIAL_ABOVE_1E5,
                FIRST_PRIMORIAL_ABOVE_1E5_PHI,
                D_CAPACITY_ENDPOINT,
            )
            required = bennett_required_cpsi_for_pap(
                FIRST_PRIMORIAL_ABOVE_1E5,
                FIRST_PRIMORIAL_ABOVE_1E5_PHI,
                D_CAPACITY_ENDPOINT,
            )
            printed = mp.mpf(BENNETT_UNIFORM_C_PSI.numerator) / (
                BENNETT_UNIFORM_C_PSI.denominator
            )
            self.assertGreater(envelope, pap_near_budget())
            self.assertGreater(envelope / pap_near_budget(), mp.mpf("1.74"))
            self.assertLess(required, printed)

    def test_aggregate_budget_is_exactly_m_times_pointwise_budget(self):
        with mp.workdps(100):
            pointwise = pointwise_second_moment_budget(123, 40, mp.mpf("0.1"))
            aggregate = aggregate_second_moment_budget(
                123, 40, 17, mp.mpf("0.1")
            )
            self.assertEqual(aggregate, 17 * pointwise)

    def test_natural_variance_comparison_is_conditional_and_scale_consistent(self):
        with mp.workdps(100):
            ratio_d21 = natural_variance_budget_ratio(
                30, 8, 21, 5, mp.mpf("0.1")
            )
            ratio_d22 = natural_variance_budget_ratio(
                30, 8, 22, 5, mp.mpf("0.1")
            )
            self.assertGreater(ratio_d21, ratio_d22)
            self.assertLess(ratio_d22 / ratio_d21, mp.mpf("0.034"))

    def test_diagnostic_fails_closed_and_preserves_global_precision(self):
        before = mp.mp.dps
        diagnostic = build_diagnostic()
        self.assertEqual(mp.mp.dps, before)
        self.assertFalse(diagnostic.bennett_large_q_cutoff_overlaps_capacity)
        self.assertTrue(diagnostic.aggregate_second_moment_redesign_logically_sufficient)
        self.assertFalse(diagnostic.aggregate_second_moment_source_identified)
        self.assertFalse(diagnostic.unconditional_numerical_drop_in_found)
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
            "EXPLICIT_L1_AND_BENNETT_POINTWISE_SOURCES_FAIL_CURRENT_PAP_CONTRACT_AGGREGATE_MOMENT_REDESIGN_REMAINS_OPEN",
        )
        status = self.ledger["status_after_this_gate"]
        self.assertTrue(status["maier_quantifier_reconstruction_complete"])
        self.assertTrue(status["aggregate_moment_terminal_condition_derived"])
        self.assertFalse(status["aggregate_moment_source_identified"])
        self.assertFalse(status["pap_11_closed"])
        self.assertFalse(status["numerical_x_cert_ready"])
        self.assertFalse(status["actual_prime_computation_run"])

    def test_machine_ledger_numeric_diagnostics_match_recomputation(self):
        diagnostic = build_diagnostic()
        saved = self.ledger["explicit_source_diagnostics"]
        fields = (
            "pap_near_budget_exp_minus_2",
            "akbary_hambrook_l1_floor_at_x4_relative_to_x",
            "akbary_floor_over_budget",
            "sedunova_l1_floor_at_x4_relative_to_x",
            "sedunova_floor_over_budget",
            "bennett_required_d_just_above_1e5_lower_endpoint",
            "bennett_required_d_at_primorial_510510",
            "bennett_relative_error_envelope_q510510_d186",
            "bennett_relative_error_over_budget_q510510_d186",
            "bennett_required_cpsi_q510510_d186",
            "bennett_printed_uniform_cpsi",
        )
        for field in fields:
            self.assertEqual(saved[field], getattr(diagnostic, field), field)
        self.assertEqual(
            saved["current_d_capacity_endpoint"],
            diagnostic.current_d_capacity_endpoint,
        )
        self.assertEqual(
            saved["bennett_large_q_cutoff_overlaps_capacity"],
            diagnostic.bennett_large_q_cutoff_overlaps_capacity,
        )

    def test_committed_local_source_hashes_match(self):
        checked = 0
        for source in self.ledger["source_registry"]:
            locator = source.get("locator")
            expected = source.get("sha256")
            if not locator or not expected or source.get("retention") == "TMP_AUDIT_COPY":
                continue
            path = REPO_ROOT / locator
            self.assertTrue(path.is_file(), locator)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
            checked += 1
        self.assertGreaterEqual(checked, 2)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            akbary_hambrook_l1_floor_relative_to_x(3)
        with self.assertRaises(ValueError):
            sedunova_l1_floor_relative_to_x(0)
        with self.assertRaises(ValueError):
            bennett_required_d_for_maier_scale(100_000)
        with self.assertRaises(ValueError):
            bennett_relative_pap_error_envelope(10, 11, 2)
        with self.assertRaises(ValueError):
            aggregate_second_moment_budget(10, 4, 0, 0.1)
        with self.assertRaises(ValueError):
            natural_variance_budget_ratio(10, 4, 2, 1, 0.1, 0)


if __name__ == "__main__":
    unittest.main()
