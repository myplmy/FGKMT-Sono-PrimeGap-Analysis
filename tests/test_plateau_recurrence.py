"""Tests for exact P006 plateau and recurrence reconstruction."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import numpy as np

from source.plateau_recurrence import (
    RecordReference,
    analyze_prime_chunks,
    iter_prime_chunks,
    run_plateau_recurrence_analysis,
    verify_reconstruction,
    verify_saved_result,
)
from source.provenance import APPROVAL_TOKEN, ApprovalRequiredError


TOY_PRIMES = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31], dtype=np.int64)


class PlateauRecurrenceUnitTests(unittest.TestCase):
    def test_segmented_sieve_generates_exact_primes_through_100(self) -> None:
        chunks = list(iter_prime_chunks(100, segment_span=17))
        observed = np.concatenate(chunks).tolist()
        expected = [
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            53,
            59,
            61,
            67,
            71,
            73,
            79,
            83,
            89,
            97,
        ]
        self.assertEqual(observed, expected)

    def test_toy_plateau_counts_use_start_exposure_and_end_boundaries(self) -> None:
        result = analyze_prime_chunks([TOY_PRIMES], analysis_limit=31)
        self.assertEqual(
            [(row["start_prime"], row["gap"], row["end_prime"]) for row in result.records],
            [(2, 1, 3), (3, 2, 5), (7, 4, 11), (23, 6, 29)],
        )

        first, second, third = result.complete_plateaus
        self.assertEqual((first["N"], first["M"], first["C"]), (1, 1, 0))
        self.assertIsNone(first["R_C_over_N_minus_1"])
        self.assertEqual((second["N"], second["M"], second["C"]), (2, 2, 1))
        self.assertEqual(second["Q_M_over_N"], 1.0)
        self.assertEqual(second["R_C_over_N_minus_1"], 1.0)
        self.assertEqual((third["N"], third["M"], third["C"]), (5, 3, 2))
        self.assertEqual(third["end_plateau_x_left"], 11)
        self.assertEqual(third["end_plateau_x_right"], 28)
        self.assertEqual(third["start_exposure_left"], 7)
        self.assertEqual(third["start_exposure_right_exclusive"], 23)

        censored = result.right_censored_plateau
        self.assertEqual((censored["N"], censored["M"], censored["C"]), (2, 1, 0))
        self.assertTrue(censored["right_censored"])

    def test_chunk_boundary_preserves_every_gap_and_record(self) -> None:
        single = analyze_prime_chunks([TOY_PRIMES], analysis_limit=31)
        split = analyze_prime_chunks(
            [TOY_PRIMES[:4], TOY_PRIMES[4:8], TOY_PRIMES[8:]],
            analysis_limit=31,
        )
        self.assertEqual(single.records, split.records)
        self.assertEqual(single.complete_plateaus, split.complete_plateaus)
        self.assertEqual(single.right_censored_plateau, split.right_censored_plateau)
        self.assertEqual(single.gap_histogram, split.gap_histogram)

    def test_reference_and_known_prime_count_cross_validation(self) -> None:
        result = analyze_prime_chunks(
            iter_prime_chunks(100, segment_span=23), analysis_limit=100
        )
        references = [
            RecordReference(1, 2, 1, 3, "toy", 100),
            RecordReference(2, 3, 2, 5, "toy", 100),
            RecordReference(3, 7, 4, 11, "toy", 100),
            RecordReference(4, 23, 6, 29, "toy", 100),
            RecordReference(5, 89, 8, 97, "toy", 100),
        ]
        report = verify_reconstruction(result, references, analysis_limit=100)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["observed_prime_count"], 25)
        self.assertEqual(report["issues"], [])

    def test_actual_pipeline_refuses_before_read_or_write_without_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            with self.assertRaises(ApprovalRequiredError):
                run_plateau_recurrence_analysis(
                    root / "missing.csv",
                    output,
                    approval_token=None,
                    analysis_limit=100,
                    segment_span=100,
                    make_plots=False,
                )
            self.assertFalse(output.exists())

    def test_small_approved_fixture_writes_non_overwriting_verified_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records_path = root / "records.csv"
            with records_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "record_index",
                        "start_prime",
                        "gap",
                        "end_prime",
                        "source_commit",
                        "verified_exhaustive_limit",
                    ],
                )
                writer.writeheader()
                for index, start, gap, end in [
                    (1, 2, 1, 3),
                    (2, 3, 2, 5),
                    (3, 7, 4, 11),
                    (4, 23, 6, 29),
                    (5, 89, 8, 97),
                ]:
                    writer.writerow(
                        {
                            "record_index": index,
                            "start_prime": start,
                            "gap": gap,
                            "end_prime": end,
                            "source_commit": "toy",
                            "verified_exhaustive_limit": 100,
                        }
                    )
            output = root / "result"
            summary = run_plateau_recurrence_analysis(
                records_path,
                output,
                approval_token=APPROVAL_TOKEN,
                analysis_limit=100,
                segment_span=100,
                make_plots=False,
            )
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual(verify_saved_result(output)["status"], "PASS")
            with self.assertRaises(FileExistsError):
                run_plateau_recurrence_analysis(
                    records_path,
                    output,
                    approval_token=APPROVAL_TOKEN,
                    analysis_limit=100,
                    segment_span=100,
                    make_plots=False,
                )


if __name__ == "__main__":
    unittest.main()
