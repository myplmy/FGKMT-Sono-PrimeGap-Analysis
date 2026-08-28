from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from source.independent_research_queue import GB, build_steps, run_queue
from source.provenance import APPROVAL_TOKEN, ApprovalRequiredError


class IndependentResearchQueueTests(unittest.TestCase):
    def test_steps_have_fixed_order_and_46_hour_child_cap_sum(self) -> None:
        steps = build_steps(Path("Z:/project"))
        self.assertEqual([step.name[:5] for step in steps], ["P013A", "P013B", "P014_"])
        self.assertTrue(steps[0].script.name.endswith("_r2.ps1"))
        self.assertEqual(sum(step.timeout_seconds for step in steps), 46 * 3600)

    def test_queue_refuses_before_any_path_or_output_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "queue"
            with self.assertRaises(ApprovalRequiredError):
                run_queue(root / "missing", output, approval_token=None)
            self.assertFalse(output.exists())

    def test_queue_rejects_more_than_47_hours_before_script_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                run_queue(
                    root,
                    root / "queue",
                    approval_token=APPROVAL_TOKEN,
                    max_wall_seconds=47 * 3600 + 1,
                )

    def test_queue_rejects_more_than_50_decimal_gb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                run_queue(
                    root,
                    root / "queue",
                    approval_token=APPROVAL_TOKEN,
                    max_disk_bytes=50 * GB + 1,
                )


if __name__ == "__main__":
    unittest.main()
