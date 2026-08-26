from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from source.recurrence_null_model import _bh_adjust, compute_null_analysis


class RecurrenceNullModelTests(unittest.TestCase):
    def test_bh_adjustment_is_monotone_in_sorted_order(self) -> None:
        p_values = [0.04, 0.001, 0.02, 0.5]
        adjusted = _bh_adjust(p_values)
        sorted_pairs = sorted(zip(p_values, adjusted))
        self.assertTrue(
            all(
                sorted_pairs[index][1] <= sorted_pairs[index + 1][1]
                for index in range(len(sorted_pairs) - 1)
            )
        )
        self.assertTrue(all(p <= q <= 1.0 for p, q in zip(p_values, adjusted)))

    def test_bh_known_values(self) -> None:
        adjusted = _bh_adjust([0.01, 0.04, 0.03, 0.002])
        for observed, expected in zip(adjusted, [0.02, 0.04, 0.04, 0.008]):
            self.assertAlmostEqual(observed, expected)

    def test_toy_analysis_is_seed_deterministic(self) -> None:
        rows = [
            {"record_index": 2, "start_prime": 1_000, "gap": 2, "N": 10, "M": 3, "C": 2},
            {"record_index": 3, "start_prime": 100_000, "gap": 4, "N": 8, "M": 1, "C": 0},
        ]
        loaded = (rows, {2: 20, 4: 10}, 100)
        with patch("source.recurrence_null_model._load_inputs", return_value=loaded):
            first = compute_null_analysis(Path("unused"), Path("unused"), replications=1_000, seed=7)
            second = compute_null_analysis(Path("unused"), Path("unused"), replications=1_000, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(first["modeled_plateau_count"], 2)
        self.assertEqual(first["cohorts"][0]["row_count"], 2)
        self.assertTrue(all("bh_q_greater_all_eligible" in row for row in first["rows"]))


if __name__ == "__main__":
    unittest.main()
