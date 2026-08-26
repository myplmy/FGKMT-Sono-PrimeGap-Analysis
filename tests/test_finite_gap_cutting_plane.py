from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from source.finite_gap_certificate import (
    RationalCertificate,
    iter_transition_edges_pairwise,
    state_count,
)
from source.finite_gap_cutting_plane import (
    _candidate_from_vector,
    _solve_working_set,
    rationalize_and_repair_candidate,
    run_cutting_plane_experiment,
)
from source.finite_gap_separation import (
    SeparationCandidate,
    scan_exact_certificate_constraints,
    scan_smallest_transition_slacks,
)
from source.provenance import ApprovalRequiredError


class FiniteGapCuttingPlaneTests(unittest.TestCase):
    def test_smallest_slack_scan_matches_brute_force(self) -> None:
        modulus = 30
        threshold = 12
        states = state_count(modulus)
        candidate = SeparationCandidate(
            lambda_value=0.02,
            mu_value=0.3,
            potentials=tuple((index - 4) / 100 for index in range(states)),
        )
        report = scan_smallest_transition_slacks(
            modulus, threshold, candidate, chunk_rows=3, top_k=11
        )
        brute: list[tuple[float, int, int, int, int]] = []
        for i, j, gap, weight in iter_transition_edges_pairwise(modulus, threshold):
            slack = (
                candidate.lambda_value * gap
                + candidate.mu_value
                + candidate.potentials[i]
                - candidate.potentials[j]
                - weight
            )
            brute.append((slack, i, j, weight, gap))
        brute.sort()
        observed = [
            (
                float(row["slack"]),
                int(row["source_index"]),
                int(row["target_index"]),
                int(row["weight"]),
                int(row["gap"]),
            )
            for row in report["smallest_constraints"]
        ]
        self.assertEqual(observed, brute[:11])

    def test_rational_repair_produces_exact_feasible_certificate(self) -> None:
        modulus = 30
        candidate = SeparationCandidate(
            lambda_value=0.0,
            mu_value=0.0,
            potentials=tuple(0.0 for _ in range(state_count(modulus))),
        )
        certificate, repair = rationalize_and_repair_candidate(
            candidate,
            modulus=modulus,
            threshold=12,
            denominator=1_000,
        )
        self.assertGreater(int(repair["mu_integer_repair"]), 0)
        exact = scan_exact_certificate_constraints(certificate)
        self.assertEqual(exact["status"], "PASS")
        self.assertEqual(exact["minimum_integer_slack"], 0)

    def test_working_set_lp_rounds_to_an_exact_certificate(self) -> None:
        modulus = 30
        threshold = 12
        edges = list(iter_transition_edges_pairwise(modulus, threshold))
        result = _solve_working_set(
            edges,
            states=state_count(modulus),
            solver_time_limit_seconds=30,
        )
        self.assertTrue(result.success, result.message)
        candidate = _candidate_from_vector(result.x, state_count(modulus))
        certificate, _ = rationalize_and_repair_candidate(
            candidate,
            modulus=modulus,
            threshold=threshold,
            denominator=1_000_000,
        )
        self.assertEqual(scan_exact_certificate_constraints(certificate)["status"], "PASS")

    def test_actual_run_refuses_before_input_read_or_output_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_cutting_plane_experiment(
                    root / "missing_manifest.json",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
