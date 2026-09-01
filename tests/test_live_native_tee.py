from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BROKER = ROOT / "scripts" / "common" / "live_native_tee.py"


class LiveNativeTeeTests(unittest.TestCase):
    @staticmethod
    def _encoded_arguments(arguments: object) -> str:
        return base64.b64encode(
            json.dumps(arguments, ensure_ascii=False).encode("utf-8")
        ).decode("ascii")

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
                "--arguments-base64",
                self._encoded_arguments(["-u", "-c", child]),
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

    def test_base64_round_trip_preserves_quote_sensitive_arguments(self) -> None:
        expected = ['space value', r'C:\\한글 경로\\file.txt', 'a"b']
        child = "import json,sys; print(json.dumps(sys.argv[1:], ensure_ascii=False), flush=True)"
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        log_path = Path(directory.name) / "runner.log"
        log_path.write_text("[STAGE] argv\n", encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                "-u",
                "-B",
                str(BROKER),
                "--log-path",
                str(log_path),
                "--stage-name",
                "argv",
                "--executable",
                sys.executable,
                "--arguments-base64",
                self._encoded_arguments(["-u", "-c", child, *expected]),
            ],
            check=False,
            capture_output=True,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(completed.returncode, 0)
        decoded = completed.stdout.decode("utf-8")
        self.assertIn(json.dumps(expected, ensure_ascii=False), decoded)
        self.assertIn(
            json.dumps(expected, ensure_ascii=False),
            log_path.read_text(encoding="utf-8"),
        )

    def test_invalid_argument_base64_is_rejected_and_logged(self) -> None:
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
                    "--arguments-base64",
                    "not-valid-***",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("live_native_tee=Error", completed.stderr)
            self.assertIn(
                "[FAIL] live_native_tee=Error",
                log_path.read_text(encoding="utf-8"),
            )

    def test_non_array_json_is_rejected_and_logged(self) -> None:
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
                    "--arguments-base64",
                    self._encoded_arguments({}),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("array of strings", completed.stderr)
            self.assertIn("array of strings", log_path.read_text(encoding="utf-8"))

    def test_broker_argument_parse_failure_is_logged_when_log_path_is_present(self) -> None:
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
                    "malformed",
                    "--executable",
                    sys.executable,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("broker argument error", completed.stderr)
            self.assertIn(
                "broker argument error", log_path.read_text(encoding="utf-8")
            )

    @unittest.skipUnless(sys.platform == "win32", "Windows PowerShell 5.1 regression")
    def test_windows_powershell_51_preserves_quote_sensitive_argv(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            temp_root = Path(directory)
            log_path = temp_root / "runner.log"
            script_path = temp_root / "invoke-live-stage.ps1"
            expected = ["space value", r"C:\한글 경로\file.txt", 'a"b']
            child = (
                "import json,sys; "
                "print(json.dumps(sys.argv[1:], ensure_ascii=False), flush=True)"
            )
            quote = lambda value: str(value).replace("'", "''")
            rendered_arguments = ",".join(
                f"'{quote(value)}'" for value in ["-u", "-c", child, *expected]
            )
            script_path.write_text(
                "$ErrorActionPreference='Stop'\n"
                "$env:PYTHONUTF8='1'\n"
                "$env:PYTHONIOENCODING='utf-8'\n"
                f". '{quote(ROOT / 'scripts' / 'common' / 'powershell_stage_logging.ps1')}'\n"
                f"Initialize-RunnerLogging -LogPath '{quote(log_path)}' "
                f"-CaptureDirectory '{quote(temp_root)}' -CapturePrefix 'ps51'\n"
                f"$arguments=@({rendered_arguments})\n"
                f"Invoke-LiveLoggedNativeStage -Name 'ps51-argv' "
                f"-FilePath '{quote(sys.executable)}' -BrokerPythonPath "
                f"'{quote(sys.executable)}' -Arguments $arguments\n",
                encoding="utf-8-sig",
            )
            completed = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script_path),
                ],
                check=False,
                capture_output=True,
            )
            console = completed.stdout.decode("utf-8", errors="replace")
            log = log_path.read_text(encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr.decode(errors="replace"))
            self.assertIn('"space value"', console)
            self.assertIn('"a\\"b"', console)
            self.assertIn(json.dumps(expected, ensure_ascii=False), log)
            self.assertIn("[PASS] ps51-argv", log)


if __name__ == "__main__":
    unittest.main()
