from __future__ import annotations

import json
import tempfile
import time
import unittest
from pathlib import Path

from source.finite_gap_mod510510_cli import main as p014_main
from source.live_progress import LiveProgressReporter
from source.provenance import ApprovalRequiredError


class LiveProgressTests(unittest.TestCase):
    def test_p014_cli_refuses_before_progress_log_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            progress = root / "must_not_exist.jsonl"
            with self.assertRaises(ApprovalRequiredError):
                p014_main(
                    [
                        "run",
                        "--g4-result-directory",
                        str(root / "missing-g4"),
                        "--output-directory",
                        str(root / "result"),
                        "--progress-log",
                        str(progress),
                    ]
                )
            self.assertFalse(progress.exists())

    def test_events_are_fsynced_and_heartbeat_is_emitted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.jsonl"
            with LiveProgressReporter(
                path,
                experiment="P014_TEST",
                stage="analysis",
                heartbeat_seconds=0.05,
            ) as reporter:
                reporter.emit({"phase": "exact_scan", "completed": 1})
                time.sleep(0.12)
                visible = path.read_text(encoding="utf-8")
                self.assertIn('"event": "PROGRESS"', visible)
                self.assertIn('"event": "HEARTBEAT"', visible)
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[0]["event"], "START")
            self.assertEqual(rows[-1]["event"], "END")
            self.assertEqual(rows[-1]["status"], "PASS")
            self.assertTrue(any(row["event"] == "HEARTBEAT" for row in rows))

    def test_failure_and_nonoverwrite_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.jsonl"
            with self.assertRaisesRegex(RuntimeError, "synthetic"):
                with LiveProgressReporter(
                    path,
                    experiment="P014_TEST",
                    stage="verify",
                    heartbeat_seconds=1,
                ):
                    raise RuntimeError("synthetic")
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[-1]["status"], "FAIL")
            self.assertIn("RuntimeError: synthetic", rows[-1]["error"])
            with self.assertRaises(FileExistsError):
                with LiveProgressReporter(
                    path,
                    experiment="P014_TEST",
                    stage="verify",
                    heartbeat_seconds=1,
                ):
                    pass


if __name__ == "__main__":
    unittest.main()
