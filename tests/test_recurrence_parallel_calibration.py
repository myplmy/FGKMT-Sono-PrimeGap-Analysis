from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from source.plateau_recurrence import RecordReference
from source.provenance import ApprovalRequiredError
from source.recurrence_parallel_calibration import (
    _derive_compact,
    _statistics_sha256,
    run_calibration,
    validate_calibration_inputs,
)
from source.recurrence_sequential_extension import StageConfig
from source.recurrence_stratified_holdout import iter_prime_chunks_range
from source.recurrence_stratified_null import accumulate_bin_counts


ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "datas/validated/prime-gap-list-project/1a112a1387052d9ad360686313f501c01fe46b68/maximal_gap_records.csv"
P012 = ROOT / "test_plan/P012_statistical_contract_v1.json"
P013 = ROOT / "test_plan/P013_recurrence_extension_contract_v1.json"
P017 = ROOT / "test_plan/P017_p013_parallel_calibration_contract_v1.json"
P012B = ROOT / "test_result/run_20260827T121734Z_p012b_stratified_null_holdout"
ORACLE = ROOT / "test_result/run_20260828T071601Z_p013a_recurrence_extension_1e11_r2"


def _reference(index: int, start: int, gap: int) -> RecordReference:
    return RecordReference(index, start, gap, start + gap, "toy", 10_000)


def _toy_plateaus() -> list[dict[str, int]]:
    references = [
        _reference(0, 89, 8),
        _reference(1, 101, 2),
        _reference(2, 103, 4),
        _reference(3, 109, 18),
        _reference(4, 211, 20),
    ]
    return [
        {
            "record_index": current.record_index,
            "start_prime": current.start_prime,
            "end_prime": current.end_prime,
            "gap": current.gap,
            "right_exclusive": following.start_prime,
            "next_record_start_prime": following.start_prime,
            "next_record_gap": following.gap,
            "next_record_end_prime": following.end_prime,
            "N": 0,
            "M": 0,
            "C": 0,
        }
        for current, following in zip(references[1:3], references[2:4], strict=True)
    ]


class RecurrenceParallelCalibrationTests(unittest.TestCase):
    def test_preflight_is_pinned_and_reads_no_actual_prime_range(self) -> None:
        report = validate_calibration_inputs(
            RECORDS,
            P012,
            P013,
            P012B / "manifest.json",
            P012B / "saved_verification_report.json",
            P017,
            ORACLE,
            mode="A_FULL",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["selected_record_indices"], [36, 37, 38, 39])
        self.assertFalse(report["actual_prime_range_read"])
        self.assertFalse(report["actual_experiment_executed"])
        self.assertFalse(report["current_p013b_artifacts_read"])

    def test_preflight_rejects_changed_serial_oracle_hash(self) -> None:
        def patched_hash(path: Path) -> str:
            selected = Path(path)
            if selected.name == "sufficient_statistics_checkpoint.json":
                return "changed"
            digest = hashlib.sha256()
            with selected.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(block)
            return digest.hexdigest()

        with mock.patch(
            "source.recurrence_parallel_calibration.sha256_file",
            side_effect=patched_hash,
        ):
            with self.assertRaisesRegex(Exception, "checkpoint hash changed"):
                validate_calibration_inputs(
                    RECORDS,
                    P012,
                    P013,
                    P012B / "manifest.json",
                    P012B / "saved_verification_report.json",
                    P017,
                    ORACLE,
                    mode="A_FULL",
                )

    def test_approval_denial_happens_before_path_access(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            output = Path(directory) / "result"
            missing = Path(directory) / "missing"
            with self.assertRaises(ApprovalRequiredError):
                run_calibration(
                    missing,
                    missing,
                    missing,
                    missing,
                    missing,
                    missing,
                    missing,
                    output,
                    mode="A_FULL",
                    approval_token=None,
                )
            self.assertFalse(output.exists())

    def test_toy_serial_parallel_derived_payloads_are_identical(self) -> None:
        provisional = _toy_plateaus()
        serial = accumulate_bin_counts(
            iter_prime_chunks_range(100, 200, segment_span=23), provisional
        )
        from source.parallel_segment_statistics import parallel_accumulate_bin_counts

        parallel = parallel_accumulate_bin_counts(
            100,
            200,
            provisional,
            worker_count=4,
            segment_count=8,
            sieve_segment_span=17,
        )
        config = StageConfig("TOY", 100, 200, int(serial["gap_count"]), (1, 2), 7)
        serial_checkpoint, serial_inference = _derive_compact(
            config, provisional, serial, seed=7, replications=1_000
        )
        parallel_checkpoint, parallel_inference = _derive_compact(
            config, provisional, parallel, seed=7, replications=1_000
        )
        self.assertEqual(_statistics_sha256(serial), _statistics_sha256(parallel))
        self.assertEqual(serial_checkpoint, parallel_checkpoint)
        self.assertEqual(serial_inference, parallel_inference)

    def test_contract_has_15h_child_sum_and_16h_global_cap(self) -> None:
        contract = json.loads(P017.read_text(encoding="utf-8"))
        caps = contract["resource_caps"]
        self.assertEqual(
            caps["p013a_timeout_seconds"] + caps["p013b_midrange_timeout_seconds"],
            15 * 3600,
        )
        self.assertEqual(caps["queue_wall_seconds"], 16 * 3600)
        self.assertEqual(contract["p013b_midrange"]["expected_complete_record_indices"], [41, 42, 43, 44, 45])
        self.assertFalse(contract["p013b_midrange"]["scientific_p013b_result_claimed"])

    def test_powershell_runner_builds_named_argument_arrays_before_invocation(self) -> None:
        runner = (ROOT / "scripts/runners/run_p013_parallel_calibration.ps1").read_text(
            encoding="utf-8"
        )
        self.assertIn("$PreflightArguments = @(\n", runner)
        self.assertIn("$RunArguments = @(\n", runner)
        self.assertIn("-Arguments $PreflightArguments", runner)
        self.assertIn("-Arguments $RunArguments", runner)
        self.assertNotIn("-Arguments @(\n        '-B', '-m', 'source.recurrence_parallel_calibration_cli', 'preflight'", runner)


if __name__ == "__main__":
    unittest.main()
