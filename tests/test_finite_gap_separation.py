from __future__ import annotations

import unittest

from source.finite_gap_certificate import iter_transition_edges_pairwise, state_count
from source.finite_gap_separation import (
    SeparationCandidate,
    SeparationResourceGuardError,
    brute_force_transition_violations,
    scan_transition_violations,
    separation_memory_estimate,
)


class FiniteGapSeparationTests(unittest.TestCase):
    def test_chunked_oracle_matches_brute_force_on_mod30(self) -> None:
        potentials = (0.0, 0.2, -0.1, 0.3, -0.4, 0.1, 0.25, -0.2)
        candidate = SeparationCandidate(0.01, -0.15, potentials)
        expected = brute_force_transition_violations(30, 12, candidate, top_k=25)
        observed = scan_transition_violations(
            30, 12, candidate, chunk_rows=3, top_k=25
        )["top_violations"]
        expected_dicts = [item.__dict__ for item in expected]
        self.assertEqual(len(observed), len(expected_dicts))
        for observed_item, expected_item in zip(observed, expected_dicts):
            self.assertEqual(
                {key: value for key, value in observed_item.items() if key != "slack"},
                {key: value for key, value in expected_item.items() if key != "slack"},
            )
            self.assertAlmostEqual(observed_item["slack"], expected_item["slack"], places=14)

    def test_scan_count_covers_every_mod30_constraint(self) -> None:
        candidate = SeparationCandidate(
            0.0, 0.0, tuple(0.0 for _ in range(state_count(30)))
        )
        report = scan_transition_violations(
            30, 12, candidate, chunk_rows=2, top_k=200
        )
        expected_constraints = len(list(iter_transition_edges_pairwise(30, 12)))
        expected_violations = brute_force_transition_violations(
            30, 12, candidate, top_k=expected_constraints
        )
        self.assertEqual(report["scanned_constraints"], expected_constraints)
        self.assertEqual(report["violation_count"], len(expected_violations))

    def test_top_k_is_deterministic_across_chunk_sizes(self) -> None:
        candidate = SeparationCandidate(
            0.0, 0.0, tuple(0.0 for _ in range(state_count(30)))
        )
        first = scan_transition_violations(
            30, 12, candidate, chunk_rows=1, top_k=10
        )["top_violations"]
        second = scan_transition_violations(
            30, 12, candidate, chunk_rows=5, top_k=10
        )["top_violations"]
        self.assertEqual(first, second)

    def test_mod30030_estimate_is_bounded_without_scanning(self) -> None:
        estimate = separation_memory_estimate(30030, chunk_rows=64, top_k=1000)
        self.assertEqual(estimate["states"], 5760)
        self.assertTrue(estimate["under_1_gib"])
        self.assertFalse(estimate["full_constraint_matrix_materialized"])

    def test_mod30030_scan_is_blocked_by_default(self) -> None:
        candidate = SeparationCandidate(
            0.0, 0.0, tuple(0.0 for _ in range(state_count(30030)))
        )
        with self.assertRaises(SeparationResourceGuardError):
            scan_transition_violations(30030, 1856, candidate, top_k=1)


if __name__ == "__main__":
    unittest.main()
