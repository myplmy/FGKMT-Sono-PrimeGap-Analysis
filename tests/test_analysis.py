"""Toy-record tests for exact interval and jump calculations."""

import unittest

import mpmath as mp

from source.analysis import (
    analysis_limit_for_interval_count,
    build_end_bounded_intervals,
    build_jump_metrics,
    record_at_x,
    summarize_analysis,
)
from source.definitions import F, H, SONO_CONSTANT, X_SCALE_POSITIVE_MIN
from source.models import MaximalGapRecord


def toy_record(index: int, start: int, gap: int, end: int) -> MaximalGapRecord:
    return MaximalGapRecord(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=end,
        source_id="toy",
        source_row_id=f"toy:{index}",
        source_commit="c" * 40,
        verified_exhaustive_limit=12_000_000,
    )


class EndBoundedAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = [
            toy_record(1, X_SCALE_POSITIVE_MIN - 10, 10, X_SCALE_POSITIVE_MIN),
            toy_record(2, 4_999_980, 20, 5_000_000),
            toy_record(3, 9_999_970, 30, 10_000_000),
        ]

    def test_intervals_use_end_prime_jump_locations_and_integer_right_edges(self) -> None:
        intervals = build_end_bounded_intervals(
            self.records,
            analysis_limit=12_000_000,
        )
        self.assertEqual(
            [(item.x_left, item.x_right) for item in intervals],
            [
                (X_SCALE_POSITIVE_MIN, 4_999_999),
                (5_000_000, 9_999_999),
                (10_000_000, 12_000_000),
            ],
        )
        self.assertTrue(mp.almosteq(intervals[0].h_interval_min, H(4_999_999, 10)))
        self.assertLess(intervals[0].h_interval_min, intervals[0].h_left)

    def test_running_minimum_is_monotone_non_increasing(self) -> None:
        intervals = build_end_bounded_intervals(
            self.records,
            analysis_limit=12_000_000,
        )
        running = [item.running_min for item in intervals]
        self.assertTrue(all(right <= left for left, right in zip(running, running[1:])))

    def test_sono_ratio_and_cramer_ratio_are_algebraically_consistent(self) -> None:
        interval = build_end_bounded_intervals(
            self.records,
            analysis_limit=12_000_000,
        )[0]
        self.assertTrue(
            mp.almosteq(interval.sono_ratio_min, interval.h_interval_min / SONO_CONSTANT)
        )
        expected_cramer = mp.mpf(interval.gap) / mp.log(interval.x_right) ** 2
        self.assertTrue(mp.almosteq(interval.cramer_ratio_min, expected_cramer))

    def test_jump_metric_quantifies_recovery(self) -> None:
        jumps = build_jump_metrics(self.records, analysis_limit=12_000_000)
        self.assertEqual([item.jump_x for item in jumps], [5_000_000, 10_000_000])
        self.assertTrue(mp.almosteq(jumps[0].h_before_jump, 10 / F(4_999_999)))
        self.assertTrue(mp.almosteq(jumps[0].h_after_jump, 20 / F(5_000_000)))
        self.assertGreater(jumps[0].recovery_factor, 1)

    def test_analysis_refuses_to_cross_exhaustive_limit(self) -> None:
        with self.assertRaises(ValueError):
            build_end_bounded_intervals(self.records, analysis_limit=12_000_001)

    def test_limited_pilot_closes_exact_requested_interval_count(self) -> None:
        limit = analysis_limit_for_interval_count(self.records, interval_count=2)
        self.assertEqual(limit, 9_999_999)
        intervals = build_end_bounded_intervals(self.records, analysis_limit=limit)
        self.assertEqual(len(intervals), 2)

    def test_record_at_x_uses_end_bounded_jump(self) -> None:
        self.assertEqual(record_at_x(self.records, 4_999_999).gap, 10)
        self.assertEqual(record_at_x(self.records, 5_000_000).gap, 20)

    def test_limited_pilot_requires_a_closing_successor_record(self) -> None:
        with self.assertRaises(ValueError):
            analysis_limit_for_interval_count(self.records, interval_count=3)

    def test_summary_reports_descriptive_trend_and_jump_recovery(self) -> None:
        intervals = build_end_bounded_intervals(
            self.records,
            analysis_limit=12_000_000,
        )
        jumps = build_jump_metrics(self.records, analysis_limit=12_000_000)
        summary = summarize_analysis(
            intervals,
            jumps,
            source_commit="c" * 40,
            analysis_limit=12_000_000,
            verified_exhaustive_limit=12_000_000,
        )
        self.assertEqual(
            summary["interval_minimum_loglog_trend"]["status"],
            "DESCRIPTIVE_ONLY",
        )
        self.assertEqual(summary["record_jump_recovery"]["count"], 2)
        self.assertGreaterEqual(summary["running_minimum_update_count"], 1)


if __name__ == "__main__":
    unittest.main()
