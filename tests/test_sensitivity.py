"""Exact toy tests for P004 boundary and envelope sensitivity metrics."""

import unittest

import mpmath as mp

from source.analysis import build_end_bounded_intervals
from source.definitions import H, X_SCALE_POSITIVE_MIN
from source.models import MaximalGapRecord
from source.sensitivity import (
    build_boundary_difference_windows,
    build_boundary_pairs,
    build_shifted_log10_bin_minima,
    build_start_bounded_intervals,
    build_x_width_local_envelope,
)


def record(index: int, start: int, gap: int) -> MaximalGapRecord:
    return MaximalGapRecord(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=start + gap,
        source_id="toy",
        source_row_id=f"toy:{index}",
        source_commit="d" * 40,
        verified_exhaustive_limit=100_000_000,
    )


class SensitivityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = [
            record(1, X_SCALE_POSITIVE_MIN - 10, 10),
            record(2, 4_999_980, 20),
            record(3, 9_999_970, 30),
            record(4, 49_999_960, 40),
        ]
        self.limit = 100_000_000
        self.start = build_start_bounded_intervals(self.records, analysis_limit=self.limit)
        self.end = build_end_bounded_intervals(self.records, analysis_limit=self.limit)

    def test_start_bounded_intervals_jump_at_start_prime(self) -> None:
        self.assertEqual(
            [(item.x_left, item.x_right) for item in self.start],
            [
                (X_SCALE_POSITIVE_MIN, 4_999_979),
                (4_999_980, 9_999_969),
                (9_999_970, 49_999_959),
                (49_999_960, self.limit),
            ],
        )

    def test_functions_differ_exactly_from_new_start_to_new_end_minus_one(self) -> None:
        windows = build_boundary_difference_windows(self.records, analysis_limit=self.limit)
        self.assertEqual((windows[0].x_left, windows[0].x_right), (4_999_980, 4_999_999))
        self.assertEqual(windows[0].integer_width, 20)
        self.assertTrue(mp.almosteq(windows[0].start_over_end_ratio, mp.mpf(20) / 10))
        pairs = build_boundary_pairs(self.start, self.end)
        self.assertEqual(len(pairs), 4)
        self.assertGreaterEqual(pairs[0].h_start_interval_min, pairs[0].h_end_interval_min)

    def test_shifted_bins_match_brute_overlap_endpoints(self) -> None:
        bins = build_shifted_log10_bin_minima(self.end, shift_decades=mp.mpf("0.5"))
        self.assertTrue(bins)
        for metric in bins:
            candidates = []
            for interval in self.end:
                right = min(metric.analyzed_x_right, interval.x_right)
                left = max(metric.analyzed_x_left, interval.x_left)
                if left <= right:
                    candidates.append((H(right, interval.gap), right))
            expected_h, expected_x = min(candidates)
            self.assertEqual(metric.minimum_x, expected_x)
            self.assertTrue(mp.almosteq(metric.h_bin_min, expected_h))

    def test_x_width_minimum_uses_all_plateau_overlap_endpoints(self) -> None:
        series = build_x_width_local_envelope(self.end, width_decades=mp.mpf("0.5"))
        self.assertEqual(len(series), len(self.end))
        for metric in series:
            candidates = []
            for interval in self.end:
                left = max(metric.window_x_left, interval.x_left)
                right = min(metric.window_x_right, interval.x_right)
                if left <= right:
                    candidates.append((H(right, interval.gap), right))
            expected_h, expected_x = min(candidates)
            self.assertEqual(metric.minimum_x, expected_x)
            self.assertTrue(mp.almosteq(metric.h_x_width_min, expected_h))


if __name__ == "__main__":
    unittest.main()

