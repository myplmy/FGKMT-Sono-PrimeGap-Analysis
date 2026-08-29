from __future__ import annotations

import unittest

from source.parallel_segment_statistics import (
    exact_statistics_core,
    parallel_accumulate_bin_counts,
    partition_integer_range,
)
from source.plateau_recurrence import RecordReference
from source.recurrence_stratified_holdout import (
    _derive_plateau_counts,
    iter_prime_chunks_range,
    select_complete_holdout_plateaus,
)
from source.recurrence_stratified_null import (
    accumulate_bin_counts,
    build_components,
)


def _reference(index: int, start: int, gap: int) -> RecordReference:
    return RecordReference(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=start + gap,
        source_commit="parallel-toy",
        verified_exhaustive_limit=10_000,
    )


def _toy_plateaus() -> list[dict[str, int]]:
    references = [
        _reference(0, 89, 8),
        _reference(1, 101, 2),
        _reference(2, 103, 4),
        _reference(3, 109, 18),
        _reference(4, 211, 20),
    ]
    return select_complete_holdout_plateaus(
        references,
        lower_inclusive=100,
        upper_exclusive=200,
    )


class ParallelSegmentStatisticsTests(unittest.TestCase):
    def test_partition_is_exact_contiguous_and_nonempty(self) -> None:
        specs = partition_integer_range(100, 211, segment_count=8)
        self.assertEqual(specs[0].lower_inclusive, 100)
        self.assertEqual(specs[-1].upper_exclusive, 211)
        self.assertTrue(
            all(
                left.upper_exclusive == right.lower_inclusive
                for left, right in zip(specs, specs[1:], strict=False)
            )
        )
        self.assertTrue(
            all(spec.lower_inclusive < spec.upper_exclusive for spec in specs)
        )

    def test_parallel_counts_equal_serial_for_worker_counts_1_2_4_8(self) -> None:
        plateaus = _toy_plateaus()
        serial = accumulate_bin_counts(
            iter_prime_chunks_range(100, 200, segment_span=23),
            plateaus,
        )
        serial_core = exact_statistics_core(serial)
        for workers in (1, 2, 4, 8):
            with self.subTest(workers=workers):
                parallel = parallel_accumulate_bin_counts(
                    100,
                    200,
                    plateaus,
                    worker_count=workers,
                    segment_count=workers,
                    sieve_segment_span=17,
                )
                self.assertEqual(exact_statistics_core(parallel), serial_core)
                metadata = parallel["parallel_execution"]
                self.assertEqual(metadata["adjacent_boundary_checks"], workers - 1)
                self.assertEqual(metadata["worker_count_observed"], workers)
                self.assertFalse(metadata["prime_arrays_transferred_between_processes"])
                self.assertTrue(metadata["exact_integer_merge"])
                self.assertEqual(metadata["worker_native_thread_ceiling"], 1)
                self.assertTrue(metadata["all_worker_native_thread_limits_one"])

    def test_parallel_counts_preserve_downstream_plateaus_and_components(self) -> None:
        provisional = _toy_plateaus()
        serial = accumulate_bin_counts(
            iter_prime_chunks_range(100, 200, segment_span=31),
            provisional,
        )
        parallel = parallel_accumulate_bin_counts(
            100,
            200,
            provisional,
            worker_count=4,
            segment_count=8,
            sieve_segment_span=19,
        )
        serial_plateaus = _derive_plateau_counts(provisional, serial)
        parallel_plateaus = _derive_plateau_counts(provisional, parallel)
        self.assertEqual(parallel_plateaus, serial_plateaus)
        self.assertEqual(
            build_components(parallel_plateaus, parallel),
            build_components(serial_plateaus, serial),
        )

    def test_nonuniform_partition_preserves_every_gap_start(self) -> None:
        plateaus = [
            {
                "record_index": 1,
                "start_prime": 1_009,
                "right_exclusive": 8_009,
                "gap": 10,
            },
            {
                "record_index": 2,
                "start_prime": 8_009,
                "right_exclusive": 19_997,
                "gap": 14,
            },
        ]
        serial = accumulate_bin_counts(
            iter_prime_chunks_range(1_000, 20_003, segment_span=997),
            plateaus,
        )
        parallel = parallel_accumulate_bin_counts(
            1_000,
            20_003,
            plateaus,
            worker_count=8,
            segment_count=13,
            sieve_segment_span=233,
        )
        self.assertEqual(exact_statistics_core(parallel), exact_statistics_core(serial))
        segments = parallel["parallel_execution"]["segments"]
        for left, right in zip(segments, segments[1:], strict=False):
            self.assertEqual(left["boundary_prime"], right["first_prime"])

    def test_progress_reports_every_segment_without_changing_exact_result(self) -> None:
        plateaus = _toy_plateaus()
        progress: list[dict[str, object]] = []
        parallel = parallel_accumulate_bin_counts(
            100,
            200,
            plateaus,
            worker_count=4,
            segment_count=8,
            sieve_segment_span=17,
            progress_callback=progress.append,
        )
        self.assertEqual(len(progress), 8)
        self.assertEqual(
            sorted(int(row["segment_index"]) for row in progress),
            list(range(8)),
        )
        self.assertEqual(
            sorted(int(row["segments_completed"]) for row in progress),
            list(range(1, 9)),
        )
        self.assertEqual(parallel["parallel_execution"]["worker_count_observed"], 4)


if __name__ == "__main__":
    unittest.main()
