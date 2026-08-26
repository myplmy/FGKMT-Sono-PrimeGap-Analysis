from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from source.bounded_research_queue import GB, _extract_result_directory, run_bounded_queue
from source.provenance import APPROVAL_TOKEN, ApprovalRequiredError


class BoundedResearchQueueTests(unittest.TestCase):
    def test_result_directory_parser_uses_last_marker(self) -> None:
        value = _extract_result_directory(
            [
                "[RUN] result_directory=C:\\old\n",
                "noise\n",
                "[RUN] result_directory=Z:\\new\n",
            ]
        )
        self.assertEqual(value, Path(r"Z:\new"))

    def test_queue_refuses_before_any_path_or_output_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "queue"
            with self.assertRaises(ApprovalRequiredError):
                run_bounded_queue(
                    root / "missing-project",
                    root / "missing-manifest.json",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())

    def test_queue_rejects_more_than_sixteen_hours_before_manifest_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "queue"
            with self.assertRaises(ValueError):
                run_bounded_queue(
                    root,
                    root / "missing-manifest.json",
                    output,
                    approval_token=APPROVAL_TOKEN,
                    max_wall_seconds=16 * 3600 + 1,
                )
            self.assertFalse(output.exists())

    def test_queue_rejects_more_than_decimal_fifty_gb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "queue"
            with self.assertRaises(ValueError):
                run_bounded_queue(
                    root,
                    root / "missing-manifest.json",
                    output,
                    approval_token=APPROVAL_TOKEN,
                    max_disk_bytes=50 * GB + 1,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
