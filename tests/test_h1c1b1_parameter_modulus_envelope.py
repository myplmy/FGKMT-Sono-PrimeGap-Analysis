"""Regression checks for H1c-1b.1 parameter and modulus envelopes."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import (
    ACTUAL_P92_LOG_POWER,
    DEFAULT_TRANSPORT_MARGIN,
    GENERAL_AFFINE_LOG_POWER,
    MINIMUM_SIEVE_DIMENSION,
    bordignon_basic_statement_conditions,
    bordignon_capacity_is_increasing,
    bordignon_exponent,
    dyadic_safe_dimension,
    dyadic_transition_strip_log_width,
    exact_dyadic_one_step_repair_certificate,
    exact_source_r_dyadic_capacity_certificate,
    exact_uniform_r_ge_36_certificate,
    maynard_log_saving_exponent,
    modulus_capacity_log_margin,
    parameter_envelope_certificate,
    q1_within_q_log_margin,
    r_interval_left_log_x,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json"
)
PREDECESSOR = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1c1b1ParameterModulusEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_parameter_identity_keeps_three_kinds_separate(self) -> None:
        for r in (36, 100, 1000):
            cert = parameter_envelope_certificate(r)
            self.assertEqual(cert.outer_chain_k, 1)
            self.assertEqual(cert.sieve_dimension_r, r)
            self.assertEqual(cert.maynard_linear_form_count, r)
            self.assertEqual(cert.required_log_saving_exponent, 100 * r * r)
            self.assertEqual(cert.bordignon_a, Fraction(100 * r * r + 10, 1))
        identity = self.contract["parameter_identity"]
        self.assertFalse(identity["fixed_k_reduction_valid"])
        self.assertTrue(identity["growing_r_required"])
        self.assertFalse(identity["outer_k_equals_maynard_k"])

    def test_uniform_exact_certificate_and_boundary_samples(self) -> None:
        self.assertTrue(
            exact_uniform_r_ge_36_certificate(
                affine_log_power=ACTUAL_P92_LOG_POWER
            )
        )
        self.assertTrue(
            exact_uniform_r_ge_36_certificate(
                affine_log_power=GENERAL_AFFINE_LOG_POWER
            )
        )
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            for r in (36, 37, 100, 1000):
                left = mp.mpf(r_interval_left_log_x(r))
                right = mp.mpf((r + 1) ** 5) - mp.mpf("1e-40")
                for log_t in (left, right):
                    self.assertGreater(
                        modulus_capacity_log_margin(
                            log_t,
                            r,
                            affine_log_power=ACTUAL_P92_LOG_POWER,
                        ),
                        0,
                    )
                    self.assertGreater(
                        modulus_capacity_log_margin(
                            log_t,
                            r,
                            affine_log_power=GENERAL_AFFINE_LOG_POWER,
                        ),
                        0,
                    )
                    self.assertGreater(q1_within_q_log_margin(log_t, r), 0)
                    self.assertTrue(bordignon_capacity_is_increasing(log_t, r))
                    self.assertTrue(bordignon_basic_statement_conditions(log_t, r))
        finally:
            mp.mp.dps = old_dps

    def test_small_scale_does_not_pass_by_construction(self) -> None:
        log_t = mp.mpf(1000)
        self.assertLess(
            modulus_capacity_log_margin(
                log_t,
                MINIMUM_SIEVE_DIMENSION,
                affine_log_power=GENERAL_AFFINE_LOG_POWER,
            ),
            0,
        )
        self.assertFalse(
            bordignon_capacity_is_increasing(log_t, MINIMUM_SIEVE_DIMENSION)
        )

    def test_actual_p92_dependency_is_pruned_but_general_affine_is_not(self) -> None:
        pruning = self.contract["actual_call_pruning"]
        self.assertEqual(pruning["actual_p92_affine_leading_coefficient"], 1)
        self.assertFalse(pruning["general_affine_lift_required_for_actual_p92"])
        self.assertTrue(pruning["general_lemma_7_2_affine_bridge_still_open"])
        updates = {
            row["id"]: row for row in self.contract["requirement_updates"]
        }
        self.assertEqual(
            updates["H1C1A-R02-ACTUAL-P92"]["status"],
            "PROJECT_FINITE_MODULUS_ENVELOPE_CLOSED",
        )
        self.assertEqual(
            updates["H1C1A-R06-ACTUAL-P92"]["status"],
            "NOT_REQUIRED_FOR_ACTUAL_P92_IDENTITY_CALL",
        )

    def test_dyadic_scale_mismatch_and_one_step_repair(self) -> None:
        r = MINIMUM_SIEVE_DIMENSION
        log_x = mp.mpf(r**5)
        log_t = log_x - dyadic_transition_strip_log_width()
        self.assertLess(log_t, r**5)
        self.assertGreater(log_t, (r - 1) ** 5)
        self.assertEqual(dyadic_safe_dimension(r), r - 1)
        self.assertTrue(exact_dyadic_one_step_repair_certificate(r))
        self.assertTrue(exact_source_r_dyadic_capacity_certificate())
        self.assertTrue(
            exact_source_r_dyadic_capacity_certificate(minimum_source_r=1000)
        )
        dyadic = self.contract["dyadic_scale_alignment"]
        self.assertFalse(dyadic["printed_source_r_uniformly_admissible_at_x_over_2"])
        self.assertTrue(dyadic["one_step_safe_repair_certified"])
        self.assertFalse(dyadic["downstream_coefficient_transfer_closed"])

    def test_pointwise_specialization_does_not_promote_full_error(self) -> None:
        cert = parameter_envelope_certificate()
        self.assertTrue(cert.pointwise_diagonal_substitution_valid)
        self.assertTrue(cert.actual_p92_uniform_modulus_gate_closed)
        self.assertTrue(cert.general_scale_affine_modulus_gate_closed)
        self.assertTrue(cert.source_r_dyadic_modulus_capacity_closed)
        self.assertFalse(cert.published_source_r_dyadic_admissibility_closed)
        self.assertTrue(cert.dyadic_one_step_dimension_repair_available)
        self.assertFalse(cert.downstream_repaired_dimension_coefficient_transfer_closed)
        self.assertFalse(cert.full_bordignon_error_composition_closed)
        self.assertFalse(cert.common_exceptional_b_closed)
        self.assertFalse(cert.exact_count_transfer_closed)
        self.assertFalse(cert.hypothesis1_clause2_closed)
        self.assertFalse(cert.proposition92_closed)
        self.assertFalse(cert.siv_07_closed)
        self.assertFalse(cert.siv_08_closed)
        self.assertFalse(cert.x_cert_ready)
        self.assertFalse(cert.actual_prime_experiment_performed)
        limits = self.contract["limits"]
        for key in (
            "bordignon_full_error_term_bounded",
            "bordignon_constant_normalization_resolved",
            "printed_source_r_dyadic_admissibility_proved",
            "repaired_dimension_coefficient_transfer_proved",
            "one_common_exceptional_modulus_proved",
            "psi_to_pi_and_half_open_transfer_proved",
            "exact_total_recentered",
            "represented_prime_density_lower_bound_proved",
            "proposition92_closed",
            "hypothesis1_clause2_closed",
            "threshold_calculator_created",
            "actual_prime_experiment_performed",
        ):
            self.assertFalse(limits[key], key)

    def test_source_hashes_and_bordignon_notation_caution(self) -> None:
        for source in self.contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
                source["key"],
            )
        caution = self.contract["source_normalization_caution"]
        self.assertIn("Y0=log log X0", caution["observation"])
        self.assertIn("X0", caution["observation"])
        self.assertTrue(caution["status"].endswith("OPEN_FOR_CONSTANT_REDERIVATION_OR_CLARIFICATION"))

    def test_predecessor_and_t1_stay_fail_closed(self) -> None:
        predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        self.assertEqual(
            predecessor["successor_parameter_envelope"]["outcome"],
            self.contract["outcome"],
        )
        maynard = next(
            row
            for row in predecessor["source_registry"]
            if row["key"] == "MAYNARD2016"
        )
        self.assertEqual(
            maynard["local_locator"],
            "tmp/pdfs/h1b1a/Maynard2016_Dense_Clusters_published.pdf",
        )
        self.assertEqual(
            maynard["sha256"],
            "8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098",
        )
        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertIn("H1c-1b.1", rows["SIV-08"]["notes"])

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            parameter_envelope_certificate(35)
        with self.assertRaises(TypeError):
            maynard_log_saving_exponent(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            bordignon_exponent(36, -1)
        with self.assertRaises(ValueError):
            modulus_capacity_log_margin(1, 36)
        with self.assertRaises(TypeError):
            exact_uniform_r_ge_36_certificate(transport_margin=1.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            dyadic_safe_dimension(1)
        with self.assertRaises(ValueError):
            exact_source_r_dyadic_capacity_certificate(minimum_source_r=35)
        self.assertEqual(DEFAULT_TRANSPORT_MARGIN, 10)


if __name__ == "__main__":
    unittest.main()
