"""Regression tests for end-prime intervals and exact local envelopes."""

import unittest

import mpmath as mp

from source.analysis import build_end_bounded_intervals
from source.definitions import F, H, X_SCALE_POSITIVE_MIN
from source.local_envelopes import (
    build_log10_bin_minima,
    build_rolling_local_envelope,
)
from source.models import MaximalGapRecord


def record(index: int, start: int, gap: int) -> MaximalGapRecord:
    return MaximalGapRecord(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=start + gap,
        source_id="boundary-regression",
        source_row_id=f"boundary:{index}",
        source_commit="a" * 40,
        verified_exhaustive_limit=200_000_000,
    )


class LocalEnvelopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = [
            record(21, 2_010_733, 148),
            record(22, 4_652_353, 154),
            record(23, 17_051_707, 180),
            record(24, 20_831_323, 210),
            record(25, 47_326_693, 220),
            record(26, 122_164_747, 222),
        ]
        self.intervals = build_end_bounded_intervals(
            self.records,
            analysis_limit=200_000_000,
        )

    def test_actual_gap_154_uses_end_prime_interval_and_next_end_minus_one(self) -> None:
        metric = next(item for item in self.intervals if item.gap == 154)
        self.assertEqual(metric.start_prime, 4_652_353)
        self.assertEqual(metric.end_prime, 4_652_507)
        self.assertEqual((metric.x_left, metric.x_right), (4_652_507, 17_051_886))
        self.assertTrue(mp.almosteq(metric.f_left, F(4_652_507)))
        self.assertTrue(mp.almosteq(metric.f_right, F(17_051_886)))
        self.assertTrue(mp.almosteq(metric.h_interval_min, 154 / F(17_051_886)))

    def test_log_bins_are_closed_right_and_exact_over_all_overlap_candidates(self) -> None:
        bins = build_log10_bin_minima(self.intervals)
        self.assertEqual([item.decade_exponent for item in bins], [6, 7, 8])
        self.assertEqual((bins[0].analyzed_x_left, bins[0].analyzed_x_right), (X_SCALE_POSITIVE_MIN, 10_000_000))
        self.assertEqual((bins[1].analyzed_x_left, bins[1].analyzed_x_right), (10_000_001, 100_000_000))
        self.assertEqual((bins[2].analyzed_x_left, bins[2].analyzed_x_right), (100_000_001, 200_000_000))

        for bin_metric in bins:
            candidates = []
            for interval in self.intervals:
                overlap_left = max(bin_metric.analyzed_x_left, interval.x_left)
                overlap_right = min(bin_metric.analyzed_x_right, interval.x_right)
                if overlap_left <= overlap_right:
                    candidates.append((H(overlap_right, interval.gap), overlap_right))
            expected_h, expected_x = min(candidates)
            self.assertEqual(bin_metric.minimum_x, expected_x)
            self.assertTrue(mp.almosteq(bin_metric.h_bin_min, expected_h))

    def test_rolling_minimum_uses_only_full_trailing_record_windows(self) -> None:
        rolling = build_rolling_local_envelope(self.intervals, window_size=5)
        self.assertEqual(len(rolling), 2)
        for position, metric in enumerate(rolling, start=4):
            window = self.intervals[position - 4 : position + 1]
            expected = min(window, key=lambda item: item.h_interval_min)
            self.assertEqual(metric.window_x_left, window[0].x_left)
            self.assertEqual(metric.window_x_right, window[-1].x_right)
            self.assertEqual(metric.minimizing_record_index, expected.record_index)
            self.assertTrue(mp.almosteq(metric.h_rolling_min, expected.h_interval_min))


if __name__ == "__main__":
    unittest.main()
