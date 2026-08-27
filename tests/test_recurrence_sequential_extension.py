from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from source.plateau_recurrence import RecordReference
from source.provenance import ApprovalRequiredError
from source.recurrence_sequential_extension import (
    P013_CONTRACT_SHA256,
    STAGES,
    StageConfig,
    run_extension,
    select_complete_plateaus,
    validate_inputs,
)


ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "datas/validated/prime-gap-list-project/1a112a1387052d9ad360686313f501c01fe46b68/maximal_gap_records.csv"
P012 = ROOT / "test_plan/P012_statistical_contract_v1.json"
P013 = ROOT / "test_plan/P013_recurrence_extension_contract_v1.json"
P012B = ROOT / "test_result/run_20260827T121734Z_p012b_stratified_null_holdout"


def _reference(index: int, start: int, gap: int) -> RecordReference:
    return RecordReference(index, start, gap, start + gap, "toy", 10_000)


class RecurrenceSequentialExtensionTests(unittest.TestCase):
    def test_contract_and_stage_a_preflight_are_pinned_without_range_sweep(self) -> None:
        report = validate_inputs(
            RECORDS,
            P012,
            P013,
            P012B / "manifest.json",
            P012B / "saved_verification_report.json",
            stage="A",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(tuple(report["selected_record_indices"]), STAGES["A"].expected_record_indices)
        self.assertEqual(report["p013_contract_sha256"], P013_CONTRACT_SHA256)
        self.assertFalse(report["extension_prime_stream_read"])
        self.assertFalse(report["actual_experiment_executed"])

    def test_complete_selection_excludes_two_censored_edges(self) -> None:
        refs = [
            _reference(0, 89, 8),
            _reference(1, 101, 2),
            _reference(2, 103, 4),
            _reference(3, 109, 18),
            _reference(4, 211, 20),
        ]
        config = StageConfig("T", 100, 200, 21, (1, 2), 7)
        rows = select_complete_plateaus(refs, config)
        self.assertEqual([row["record_index"] for row in rows], [1, 2])
        self.assertEqual([row["right_exclusive"] for row in rows], [103, 109])

    def test_actual_refuses_before_input_or_output_access(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_extension(
                    root / "missing.csv",
                    root / "missing-p012.json",
                    root / "missing-p013.json",
                    root / "missing-manifest.json",
                    root / "missing-report.json",
                    output,
                    stage="A",
                    approval_token=None,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
