from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from source.plateau_recurrence import RecordReference, load_record_references
from source.provenance import ApprovalRequiredError
from source.recurrence_sequential_extension import (
    P013_CONTRACT_SHA256,
    STAGES,
    StageConfig,
    _payload_sha256,
    _sufficient_statistics_payload,
    _validate_sufficient_statistics,
    compute_extension_analysis,
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
    def test_sufficient_statistics_checkpoint_is_canonical_and_validated(self) -> None:
        config = StageConfig("T", 100, 200, 4, (1,), 7)
        provisional = [
            {
                "record_index": 1,
                "start_prime": 101,
                "end_prime": 103,
                "gap": 2,
                "right_exclusive": 109,
                "next_record_start_prime": 109,
                "next_record_gap": 4,
                "next_record_end_prime": 113,
                "N": 0,
                "M": 0,
                "C": 0,
            }
        ]
        plateaus = [{**provisional[0], "N": 4, "M": 2, "C": 1}]
        components = []
        for scheme in (
            "primary_width_0p5_shift_0",
            "sensitivity_width_0p5_shift_0p25",
            "sensitivity_width_1_shift_0p5",
        ):
            components.append(
                {
                    "scheme": scheme,
                    "record_index": 1,
                    "plateau_exposure_after_removal": 3,
                    "observed_recurrences": 1,
                }
            )
        payload = _sufficient_statistics_payload(
            config,
            prime_count=5,
            gap_count=4,
            plateaus=plateaus,
            components=components,
        )
        restored_plateaus, restored_components = _validate_sufficient_statistics(
            payload, config, provisional
        )
        self.assertEqual(restored_plateaus, plateaus)
        self.assertEqual(restored_components, components)
        self.assertEqual(_payload_sha256(payload), _payload_sha256(dict(payload)))

    def test_valid_checkpoint_reuse_skips_range_sweep_and_returns_boundary_count(self) -> None:
        config = STAGES["A"]
        provisional = select_complete_plateaus(load_record_references(RECORDS), config)
        plateaus = [{**row, "N": 2, "M": 1, "C": 0} for row in provisional]
        components = []
        for scheme in (
            "primary_width_0p5_shift_0",
            "sensitivity_width_0p5_shift_0p25",
            "sensitivity_width_1_shift_0p5",
        ):
            for plateau in plateaus:
                components.append(
                    {
                        "scheme": scheme,
                        "record_index": plateau["record_index"],
                        "start_prime": plateau["start_prime"],
                        "gap": plateau["gap"],
                        "bin_index": 0,
                        "bin_left": 1.0,
                        "bin_right_exclusive": 10.0,
                        "forced_record_removed": 1,
                        "population_after_removal": 10,
                        "conditioned_gap_count_after_removal": 0,
                        "plateau_exposure_after_removal": 1,
                        "observed_recurrences": 0,
                        "control_exposure": 9,
                        "expected_component": 0.0,
                        "variance_component": 0.0,
                        "information_flag": "LOW_INFORMATION",
                    }
                )
        payload = _sufficient_statistics_payload(
            config,
            prime_count=config.expected_gap_start_count + 1,
            gap_count=config.expected_gap_start_count,
            plateaus=plateaus,
            components=components,
        )
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            checkpoint = Path(directory) / "checkpoint.json"
            checkpoint.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            progress = []
            analysis = compute_extension_analysis(
                RECORDS,
                P012,
                P013,
                P012B / "manifest.json",
                P012B / "saved_verification_report.json",
                stage="A",
                checkpoint_path=checkpoint,
                progress_callback=progress.append,
            )
        self.assertEqual(
            analysis["prime_stream_count_including_boundary_prime"],
            config.expected_gap_start_count + 1,
        )
        self.assertEqual(progress[0]["sufficient_statistics_checkpoint"], "REUSED")

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
