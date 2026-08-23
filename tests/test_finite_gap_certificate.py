"""Toy and exact-arithmetic tests for the P007 certificate machinery."""

from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from source.finite_gap_certificate import (
    CertificateError,
    DEFAULT_SOLVE_CONSTRAINT_CAP,
    ResourceGuardError,
    discover_certificate,
    iter_transition_edges_by_offsets,
    iter_transition_edges_pairwise,
    read_certificate,
    run_supplied_certificate_audit,
    state_count,
    transition_resource_estimate,
    verify_certificate,
)
from source.provenance import ApprovalRequiredError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUPPLIED_CERTIFICATE = (
    PROJECT_ROOT
    / "ai_dev_tool"
    / "temp_prime_gap_count_algorithm"
    / "source"
    / "C2310_certificate.txt"
)


class FiniteGapCertificateTests(unittest.TestCase):
    def test_primorial_state_counts(self) -> None:
        self.assertEqual(state_count(30), 8)
        self.assertEqual(state_count(210), 48)
        self.assertEqual(state_count(2310), 480)
        self.assertEqual(state_count(30030), 5760)

    def test_independent_edge_builders_agree_on_toy_modulus(self) -> None:
        pairwise = set(iter_transition_edges_pairwise(30, 12))
        offsets = set(iter_transition_edges_by_offsets(30, 12))
        self.assertEqual(pairwise, offsets)
        self.assertEqual(len(pairwise), 83)

    def test_resource_estimate_matches_reviewed_constraint_count(self) -> None:
        estimate = transition_resource_estimate(2310, 1856)
        self.assertEqual(estimate["states"], 480)
        self.assertEqual(estimate["total_transition_constraints"], 415_223)
        self.assertTrue(estimate["solve_allowed_by_guard"])

        large = transition_resource_estimate(30030, 1856)
        self.assertEqual(large["states"], 5760)
        self.assertGreater(large["total_transition_constraints"], 33_000_000)
        self.assertFalse(large["solve_allowed_by_guard"])

    def test_supplied_mod2310_certificate_exactly_verifies(self) -> None:
        certificate = read_certificate(SUPPLIED_CERTIFICATE)
        report = verify_certificate(certificate)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["edge_constraints"], 415_223)
        self.assertEqual(report["minimum_integer_slack"], 0)
        self.assertEqual(
            report["total_start_bounded_upper_bound"],
            "439161464927854179",
        )
        self.assertEqual(
            report["corrected_packing_total_bound"],
            "484913793103448276",
        )
        self.assertFalse(report["direct_search_acceleration_proved"])

    def test_invalid_certificate_is_rejected(self) -> None:
        certificate = read_certificate(SUPPLIED_CERTIFICATE)
        with self.assertRaises(CertificateError):
            verify_certificate(replace(certificate, lambda_num=-1))
        with self.assertRaises(CertificateError):
            verify_certificate(replace(certificate, total_bound=0))

    def test_actual_audit_refuses_before_input_read_or_output_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_supplied_certificate_audit(
                    root / "missing.txt", output, approval_token=None
                )
            self.assertFalse(output.exists())

    def test_toy_lp_candidate_is_repaired_and_exactly_verified(self) -> None:
        certificate, discovery = discover_certificate(
            30,
            threshold=12,
            a=100,
            b=10_000,
            pi_a=25,
            pi_b=1229,
            denominator=10**8,
            solve_constraint_cap=10_000,
        )
        report = verify_certificate(
            certificate,
            a=100,
            b=10_000,
            pi_a=25,
            pi_b=1229,
        )
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(discovery["floating_solver_success"])

    def test_resource_guard_prevents_large_lp_materialization(self) -> None:
        with self.assertRaises(ResourceGuardError):
            discover_certificate(
                30030,
                solve_constraint_cap=DEFAULT_SOLVE_CONSTRAINT_CAP,
            )


if __name__ == "__main__":
    unittest.main()
