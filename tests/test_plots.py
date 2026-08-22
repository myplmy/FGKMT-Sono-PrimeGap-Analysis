"""Synthetic-data tests for the preregistered figure set."""

import tempfile
import unittest
from pathlib import Path

from source.analysis import build_end_bounded_intervals, build_jump_metrics
from source.definitions import X_SCALE_POSITIVE_MIN
from source.models import MaximalGapRecord
from source.plots import plot_all


class PlotTests(unittest.TestCase):
    def test_all_six_plots_are_written_as_png_and_pdf_without_overwrite(self) -> None:
        records = [
            MaximalGapRecord(
                record_index=1,
                start_prime=X_SCALE_POSITIVE_MIN - 10,
                gap=10,
                end_prime=X_SCALE_POSITIVE_MIN,
                source_id="toy",
                source_row_id="toy:1",
                source_commit="d" * 40,
                verified_exhaustive_limit=12_000_000,
            ),
            MaximalGapRecord(
                record_index=2,
                start_prime=4_999_980,
                gap=20,
                end_prime=5_000_000,
                source_id="toy",
                source_row_id="toy:2",
                source_commit="d" * 40,
                verified_exhaustive_limit=12_000_000,
            ),
        ]
        intervals = build_end_bounded_intervals(
            records,
            analysis_limit=12_000_000,
        )
        jumps = build_jump_metrics(records, analysis_limit=12_000_000)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            paths = plot_all(
                intervals,
                jumps,
                output,
                provenance_label="toy; boundary_mode=end",
            )
            self.assertEqual(len(paths), 12)
            self.assertTrue(all(path.is_file() and path.stat().st_size > 0 for path in paths))
            with self.assertRaises(FileExistsError):
                plot_all(
                    intervals,
                    jumps,
                    output,
                    provenance_label="toy; boundary_mode=end",
                )


if __name__ == "__main__":
    unittest.main()

