from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from source.p013_parallel_calibration_queue import (
    GB,
    MAX_WALL_SECONDS,
    build_steps,
    run_queue,
)
from source.provenance import APPROVAL_TOKEN, ApprovalRequiredError


class P013ParallelCalibrationQueueTests(unittest.TestCase):
    def test_steps_are_independent_and_sum_to_15_hours(self) -> None:
        steps = build_steps(Path("Z:/project"))
        self.assertEqual([step.name[:5] for step in steps], ["P017A", "P017B"])
        self.assertEqual(sum(step.timeout_seconds for step in steps), 15 * 3600)
        self.assertTrue(steps[0].script.name.startswith("run_p017a"))
        self.assertTrue(steps[1].script.name.startswith("run_p017b"))

    def test_queue_refuses_before_path_access_without_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "queue"
            with self.assertRaises(ApprovalRequiredError):
                run_queue(root / "missing", output, approval_token=None)
            self.assertFalse(output.exists())

    def test_queue_rejects_more_than_16_hours(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                run_queue(
                    root,
                    root / "queue",
                    approval_token=APPROVAL_TOKEN,
                    max_wall_seconds=MAX_WALL_SECONDS + 1,
                )

    def test_queue_rejects_more_than_5_decimal_gb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                run_queue(
                    root,
                    root / "queue",
                    approval_token=APPROVAL_TOKEN,
                    max_disk_bytes=5 * GB + 1,
                )

    def test_queue_exposes_a_known_python_flushed_live_log(self) -> None:
        source = (
            Path(__file__).resolve().parents[1]
            / "source/p013_parallel_calibration_queue.py"
        ).read_text(encoding="utf-8")
        runner = (
            Path(__file__).resolve().parents[1]
            / "scripts/experiments/p017/run_p017_16h_parallel_calibration_queue.ps1"
        ).read_text(encoding="utf-8")
        self.assertIn('live_log_path = output_directory / "live_console.log"', source)
        self.assertIn("handle.flush()", source)
        self.assertIn("queue_live_file=$QueueLivePath", runner)
        self.assertIn("while (-not (Test-Path", runner)
        self.assertIn("Get-Content -LiteralPath '$QueueLivePath' -Wait", runner)


if __name__ == "__main__":
    unittest.main()
