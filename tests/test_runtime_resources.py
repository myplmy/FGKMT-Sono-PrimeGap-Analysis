from __future__ import annotations

import os
import json
import subprocess
import sys
import unittest

from source.runtime_resources import plan_cpu_resources


class RuntimeResourceTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows topology contract")
    def test_four_physical_cores_map_to_eight_logical_processors(self) -> None:
        plan = plan_cpu_resources(physical_cores=4, logical_processors=8)
        self.assertGreaterEqual(plan.detected_physical_cores, 4)
        self.assertGreaterEqual(plan.detected_logical_processors, 8)
        self.assertEqual(plan.selected_logical_processors, 8)
        self.assertEqual(int(plan.affinity_mask_hex, 16).bit_count(), 8)
        self.assertEqual(plan.topology_mapping, "windows-physical-core-topology")

    @unittest.skipUnless(os.name == "nt", "Windows Job Object contract")
    def test_process_tree_memory_limit_applies_in_isolated_child(self) -> None:
        code = (
            "import json; "
            "from source.runtime_resources import configure_process_tree_memory_limit; "
            "print(json.dumps(configure_process_tree_memory_limit(limit_bytes=31500000000)))"
        )
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["applied"])
        self.assertTrue(payload["inherited_by_child_processes"])
        self.assertEqual(payload["limit_bytes"], 31_500_000_000)


if __name__ == "__main__":
    unittest.main()
