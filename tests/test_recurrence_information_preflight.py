from __future__ import annotations

import math
import unittest

from source.recurrence_information_preflight import (
    build_preflight_report,
    evaluate_stage,
    poisson_screening_metrics,
)


def _stage(*, label: str, expected: float, positive_rows: int, low_fraction: float):
    return {
        "label": label,
        "primary_expected_recurrences": expected,
        "primary_positive_variance_rows": positive_rows,
        "primary_low_information_fraction": low_fraction,
    }


class RecurrenceInformationPreflightTests(unittest.TestCase):
    def test_poisson_screen_uses_upper_tail_critical_count(self) -> None:
        report = poisson_screening_metrics(0.1, alpha=0.025)
        self.assertEqual(report["critical_count"], 2)
        self.assertAlmostEqual(
            report["null_probability_at_least_one"], 1.0 - math.exp(-0.1)
        )
        self.assertFalse(report["is_actual_stratified_hypergeometric_family_power"])

    def test_low_information_stage_is_held(self) -> None:
        evaluated = evaluate_stage(
            _stage(label="P013-B", expected=0.0668, positive_rows=1, low_fraction=1.0)
        )
        self.assertFalse(evaluated["information_gate_pass"])
        self.assertFalse(evaluated["automatic_next_range_promotion"])
        self.assertFalse(evaluated["formal_power_certified"])

    def test_information_rich_stage_still_requires_proxy_power_gate(self) -> None:
        evaluated = evaluate_stage(
            _stage(label="future", expected=3.0, positive_rows=5, low_fraction=0.2)
        )
        self.assertTrue(evaluated["information_gate_pass"])
        self.assertIn("poisson_screening_power_gate_pass", evaluated)

    def test_report_uses_named_decision_stage_without_pooling(self) -> None:
        report = build_preflight_report(
            [
                _stage(label="history", expected=3.0, positive_rows=5, low_fraction=0.2),
                _stage(label="P013-B", expected=0.0668, positive_rows=1, low_fraction=1.0),
            ],
            decision_stage_label="P013-B",
        )
        self.assertEqual(report["recommendation"], "HOLD_NEXT_RANGE")
        self.assertTrue(report["poisson_screen_is_planning_proxy_only"])
        self.assertFalse(report["formal_power_certified"])


if __name__ == "__main__":
    unittest.main()
