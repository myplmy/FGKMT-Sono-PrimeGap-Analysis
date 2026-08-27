from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from source.candidate_cover import (
    build_exhaustive_toy_ledger,
    dangerous_starts_exact_small,
    evaluate_break_even,
    run_toy,
    verify_candidate_cover,
    verify_saved_toy,
)


ROOT = Path(__file__).resolve().parents[1]


class CandidateCoverTests(unittest.TestCase):
    def test_toy_candidates_equal_exact_dangerous_starts(self) -> None:
        ledger = build_exhaustive_toy_ledger(1_000, 5_000, 20)
        report = verify_candidate_cover(ledger)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["coverage_complete"])
        self.assertTrue(report["sound_rejections"])
        self.assertEqual(
            [int(value) for value in ledger["candidate_starts"]],
            dangerous_starts_exact_small(1_000, 5_000, 20),
        )
        self.assertGreater(report["candidate_count"], 0)
        self.assertFalse(report["acceleration_proved"])

    def test_missing_witness_fails_coverage(self) -> None:
        ledger = build_exhaustive_toy_ledger(1_000, 1_100, 20)
        ledger["rejection_witnesses"].pop()
        report = verify_candidate_cover(ledger)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["coverage_complete"])
        self.assertTrue(any("uncovered" in issue for issue in report["issues"]))

    def test_invalid_factor_fails_soundness(self) -> None:
        ledger = build_exhaustive_toy_ledger(1_000, 1_100, 20)
        witness = next(
            row
            for row in ledger["rejection_witnesses"]
            if row["type"] == "COMPOSITE_FACTOR"
        )
        witness["factor"] = "997"
        report = verify_candidate_cover(ledger)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["sound_rejections"])

    def test_window_prime_at_threshold_is_not_a_rejection(self) -> None:
        ledger = build_exhaustive_toy_ledger(1_000, 1_100, 20)
        witness = next(
            row
            for row in ledger["rejection_witnesses"]
            if row["type"] == "WINDOW_PRIME"
        )
        witness["prime"] = str(int(witness["start"]) + 20)
        report = verify_candidate_cover(ledger)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any("outside the strict rejection window" in issue for issue in report["issues"])
        )

    def test_nonintegral_candidate_is_not_silently_truncated(self) -> None:
        ledger = build_exhaustive_toy_ledger(1_000, 1_200, 20)
        ledger["candidate_starts"][0] = "1129.5"
        report = verify_candidate_cover(ledger)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["coverage_complete"])

    def test_break_even_rejects_circular_generator_even_if_times_look_fast(self) -> None:
        verification = verify_candidate_cover(
            build_exhaustive_toy_ledger(1_000, 1_100, 20)
        )
        benchmark = {
            "run_count": 5,
            "baseline_median_seconds": 10.0,
            "candidate_generate_median_seconds": 1.0,
            "candidate_verify_median_seconds": 1.0,
            "survivor_search_median_seconds": 1.0,
            "artifact_bytes": 1_000,
            "false_negative_count": 0,
            "same_range_and_threshold": True,
            "cpu_id": "toy-cpu",
            "baseline_code_sha256": "baseline",
            "candidate_code_sha256": "candidate",
        }
        report = evaluate_break_even(verification, benchmark)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("circular" in issue for issue in report["issues"]))

    def test_break_even_can_only_promote_to_candidate_not_proof(self) -> None:
        verification = verify_candidate_cover(
            build_exhaustive_toy_ledger(1_000, 1_100, 20)
        )
        verification = copy.deepcopy(verification)
        verification["generator_uses_exhaustive_oracle"] = False
        benchmark = {
            "run_count": 7,
            "baseline_median_seconds": 10.0,
            "candidate_generate_median_seconds": 2.0,
            "candidate_verify_median_seconds": 1.0,
            "survivor_search_median_seconds": 2.0,
            "artifact_bytes": 1_000,
            "false_negative_count": 0,
            "same_range_and_threshold": True,
            "cpu_id": "toy-cpu",
            "baseline_code_sha256": "baseline",
            "candidate_code_sha256": "candidate",
        }
        report = evaluate_break_even(verification, benchmark)
        self.assertEqual(report["status"], "ACCELERATION_CANDIDATE")
        self.assertFalse(report["acceleration_proved"])
        self.assertTrue(report["independent_repeat_required"])

    def test_break_even_uses_decimal_fifty_gb_cap(self) -> None:
        verification = verify_candidate_cover(
            build_exhaustive_toy_ledger(1_000, 1_100, 20)
        )
        verification = copy.deepcopy(verification)
        verification["generator_uses_exhaustive_oracle"] = False
        benchmark = {
            "run_count": 5,
            "baseline_median_seconds": 10.0,
            "candidate_generate_median_seconds": 1.0,
            "candidate_verify_median_seconds": 1.0,
            "survivor_search_median_seconds": 1.0,
            "artifact_bytes": 50_000_000_000,
            "false_negative_count": 0,
            "same_range_and_threshold": True,
            "cpu_id": "toy-cpu",
            "baseline_code_sha256": "baseline",
            "candidate_code_sha256": "candidate",
        }
        self.assertEqual(
            evaluate_break_even(verification, benchmark)["status"],
            "ACCELERATION_CANDIDATE",
        )
        benchmark["artifact_bytes"] += 1
        report = evaluate_break_even(verification, benchmark)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("50 GB" in issue for issue in report["issues"]))

    def test_saved_toy_reverification_and_nonoverwrite(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=ROOT / "tmp", prefix="p010b-cover-test-"
        ) as directory:
            output = Path(directory) / "result"
            summary = run_toy(output, a=1_000, b=5_000, threshold=20)
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual(summary["acceleration_status"], "BLOCKED")
            self.assertEqual(verify_saved_toy(output)["status"], "PASS")
            with self.assertRaises(FileExistsError):
                run_toy(output, a=1_000, b=5_000, threshold=20)


if __name__ == "__main__":
    unittest.main()
