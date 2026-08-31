from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BROKER = ROOT / "scripts" / "common" / "live_native_tee.py"


class LiveNativeTeeTests(unittest.TestCase):
    def _run_broker(self, child_code: str, *, child_exit: int = 0):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        log_path = Path(directory.name) / "runner.log"
        log_path.write_text("[STAGE] toy\n", encoding="utf-8")
        child = (
            "import sys; "
            + child_code
            + f"; raise SystemExit({child_exit})"
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-u",
                "-B",
                str(BROKER),
                "--log-path",
                str(log_path),
                "--stage-name",
                "toy",
                "--executable",
                sys.executable,
                "--arguments-json",
                json.dumps(["-u", "-c", child]),
            ],
            check=False,
            capture_output=True,
        )
        return completed, log_path.read_text(encoding="utf-8")

    def test_stdout_stderr_blank_lines_and_exit_zero_are_preserved(self) -> None:
        completed, log = self._run_broker(
            "print('out-1', flush=True); print('', flush=True); "
            "print('err-1', file=sys.stderr, flush=True)"
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn(b"out-1", completed.stdout)
        self.assertIn(b"err-1", completed.stdout)
        self.assertEqual(completed.stderr, b"")
        self.assertIn("[CAPTURE] stream=stdout live", log)
        self.assertIn("[CAPTURE] stream=stderr live", log)
        self.assertIn("out-1\n\n", log)
        self.assertIn("err-1", log)
        self.assertIn("child_exit_code=0", log)

    def test_nonzero_child_exit_and_stderr_are_not_hidden(self) -> None:
        completed, log = self._run_broker(
            "print('synthetic failure', file=sys.stderr, flush=True)",
            child_exit=7,
        )
        self.assertEqual(completed.returncode, 7)
        self.assertIn(b"synthetic failure", completed.stdout)
        self.assertIn("synthetic failure", log)
        self.assertIn("child_exit_code=7", log)

    def test_invalid_argument_json_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log_path = Path(directory) / "runner.log"
            log_path.write_text("", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(BROKER),
                    "--log-path",
                    str(log_path),
                    "--stage-name",
                    "toy",
                    "--executable",
                    sys.executable,
                    "--arguments-json",
                    "{}",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("array of strings", completed.stderr)


if __name__ == "__main__":
    unittest.main()

