from __future__ import annotations

import os
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


if __name__ == "__main__":
    unittest.main()
