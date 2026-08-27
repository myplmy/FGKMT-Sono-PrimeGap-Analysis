from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from source.provenance import ApprovalRequiredError
from source.recurrence_stratified_null import (
    BIN_SCHEMES,
    _plot_comparison,
    accumulate_bin_counts,
    analyze_components,
    build_components,
    run_stratified_null,
)


def _toy_plateaus() -> list[dict[str, int]]:
    return [
        {
            "record_index": 1,
            "start_prime": 2,
            "gap": 1,
            "right_exclusive": 3,
            "N": 1,
            "M": 1,
            "C": 0,
        },
        {
            "record_index": 2,
            "start_prime": 3,
            "gap": 2,
            "right_exclusive": 7,
            "N": 2,
            "M": 2,
            "C": 1,
        },
        {
            "record_index": 3,
            "start_prime": 7,
            "gap": 4,
            "right_exclusive": 23,
            "N": 5,
            "M": 3,
            "C": 2,
        },
    ]


class RecurrenceStratifiedNullTests(unittest.TestCase):
    def test_components_remove_forced_record_and_preserve_p006_totals(self) -> None:
        primes = np.asarray([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=np.int64)
        plateaus = _toy_plateaus()
        accumulated = accumulate_bin_counts([primes], plateaus)
        components = build_components(plateaus, accumulated)
        for scheme in BIN_SCHEMES:
            for plateau in plateaus:
                selected = [
                    row
                    for row in components
                    if row["scheme"] == scheme.name
                    and row["record_index"] == plateau["record_index"]
                ]
                self.assertEqual(
                    sum(int(row["plateau_exposure_after_removal"]) for row in selected),
                    plateau["N"] - 1,
                )
                self.assertEqual(
                    sum(int(row["observed_recurrences"]) for row in selected),
                    plateau["C"],
                )
                self.assertEqual(
                    sum(int(row["forced_record_removed"]) for row in selected), 1
                )

    def test_fixed_seed_analysis_is_reproducible(self) -> None:
        primes = np.asarray([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=np.int64)
        plateaus = _toy_plateaus()
        components = build_components(plateaus, accumulate_bin_counts([primes], plateaus))
        first = analyze_components(plateaus, components, {}, replications=1_000, seed=123)
        second = analyze_components(plateaus, components, {}, replications=1_000, seed=123)
        self.assertEqual(first, second)

    def test_primary_and_shifted_schemes_are_all_retained(self) -> None:
        primes = np.asarray([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=np.int64)
        components = build_components(
            _toy_plateaus(), accumulate_bin_counts([primes], _toy_plateaus())
        )
        self.assertEqual(
            {str(row["scheme"]) for row in components},
            {scheme.name for scheme in BIN_SCHEMES},
        )

    def test_actual_run_refuses_before_input_read_or_output_write(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=Path.cwd() / "tmp", prefix="p012-approval-test-"
        ) as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_stratified_null(
                    root / "missing_plateaus.csv",
                    root / "missing_p011.csv",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())

    def test_plot_preserves_zero_variance_z_as_undefined(self) -> None:
        rows = [
            {
                "scheme": BIN_SCHEMES[0].name,
                "cohorts": ["all_eligible", "primary_start_ge_1000"],
                "gap": 44,
                "observed_recurrences": 0,
                "expected_recurrences": 0.0,
                "p011_expected_recurrences": 3.0,
                "standardized_residual_z": None,
                "p011_standardized_residual_z": -1.7,
            },
            {
                "scheme": BIN_SCHEMES[0].name,
                "cohorts": ["all_eligible", "primary_start_ge_1000"],
                "gap": 52,
                "observed_recurrences": 1,
                "expected_recurrences": 0.5,
                "p011_expected_recurrences": 0.8,
                "standardized_residual_z": 0.75,
                "p011_standardized_residual_z": 0.2,
            },
        ]
        self.assertIsNone(rows[0]["standardized_residual_z"])
        with tempfile.TemporaryDirectory(
            dir=Path.cwd() / "tmp", prefix="p012-plot-test-"
        ) as directory:
            paths = _plot_comparison(rows, Path(directory) / "figures")
            self.assertEqual(len(paths), 4)
            self.assertEqual(
                {path.name for path in paths},
                {
                    "p012_expected_comparison.png",
                    "p012_expected_comparison.pdf",
                    "p012_residual_comparison.png",
                    "p012_residual_comparison.pdf",
                },
            )
            for path in paths:
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)
        self.assertIsNone(rows[0]["standardized_residual_z"])


if __name__ == "__main__":
    unittest.main()
