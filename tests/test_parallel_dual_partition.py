from __future__ import annotations

import unittest

from source.parallel_dual_partition import (
    DualPartitionVerificationError,
    dual_partition_accumulate_bin_counts,
)
from source.parallel_segment_statistics import exact_statistics_core
from source.plateau_recurrence import RecordReference
from source.recurrence_stratified_holdout import (
    iter_prime_chunks_range,
    select_complete_holdout_plateaus,
)
from source.recurrence_stratified_null import accumulate_bin_counts


def _reference(index: int, start: int, gap: int) -> RecordReference:
    return RecordReference(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=start + gap,
        source_commit="p019-toy",
        verified_exhaustive_limit=10_000,
    )


def _toy_plateaus() -> list[dict[str, int]]:
    return select_complete_holdout_plateaus(
        [
            _reference(0, 89, 8),
            _reference(1, 101, 2),
            _reference(2, 103, 4),
            _reference(3, 109, 18),
            _reference(4, 211, 20),
        ],
        lower_inclusive=100,
        upper_exclusive=200,
    )


class ParallelDualPartitionTests(unittest.TestCase):
    def test_two_coprime_parallel_partitions_equal_toy_serial_oracle(self) -> None:
        plateaus = _toy_plateaus()
        progress: list[dict[str, object]] = []
        result = dual_partition_accumulate_bin_counts(
            100,
            200,
            plateaus,
            expected_gap_start_count=21,
            worker_count=4,
            primary_segment_count=8,
            verifier_segment_count=11,
            primary_sieve_segment_span=17,
            verifier_sieve_segment_span=19,
            progress_callback=progress.append,
        )
        serial = accumulate_bin_counts(
            iter_prime_chunks_range(100, 200, segment_span=23),
            plateaus,
        )
        self.assertEqual(result["statistics"], exact_statistics_core(serial))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["full_parallel_passes"], 2)
        self.assertFalse(result["serial_oracle_used"])
        self.assertFalse(result["work_items_omitted"])
        self.assertFalse(result["precision_reduced"])
        self.assertEqual(
            {row["dual_partition_pass"] for row in progress},
            {"primary", "verifier"},
        )
        self.assertEqual(len(progress), 19)

    def test_equal_or_non_coprime_partitions_are_rejected_before_work(self) -> None:
        for primary, verifier in ((8, 8), (8, 12)):
            with self.subTest(primary=primary, verifier=verifier):
                with self.assertRaises(ValueError):
                    dual_partition_accumulate_bin_counts(
                        100,
                        200,
                        _toy_plateaus(),
                        expected_gap_start_count=21,
                        worker_count=4,
                        primary_segment_count=primary,
                        verifier_segment_count=verifier,
                        primary_sieve_segment_span=17,
                        verifier_sieve_segment_span=19,
                    )

    def test_independent_gap_count_mismatch_blocks_acceptance(self) -> None:
        with self.assertRaisesRegex(
            DualPartitionVerificationError,
            "independently certified pi difference",
        ):
            dual_partition_accumulate_bin_counts(
                100,
                200,
                _toy_plateaus(),
                expected_gap_start_count=22,
                worker_count=2,
                primary_segment_count=3,
                verifier_segment_count=5,
                primary_sieve_segment_span=17,
                verifier_sieve_segment_span=19,
            )


if __name__ == "__main__":
    unittest.main()

