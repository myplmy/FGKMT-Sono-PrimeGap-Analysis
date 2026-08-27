from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from source.provenance import ApprovalRequiredError
from source.recurrence_stratified_null import (
    BIN_SCHEMES,
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
        with tempfile.TemporaryDirectory() as directory:
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


if __name__ == "__main__":
    unittest.main()
