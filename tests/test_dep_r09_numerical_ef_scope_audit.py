"""Provenance and no-promotion guards, not an analytic EF proof or experiment."""

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/method/theory/data/Sono_FMT_DEPR09_numerical_EF_scope_audit_v1.json"


class NumericalEFScopeAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_primary_pins_match_cached_publications(self):
        self.assertEqual(len(self.data["source_registry"]), 2)
        for item in self.data["source_registry"]:
            digest = hashlib.sha256((ROOT / item["locator"]).read_bytes()).hexdigest()
            self.assertEqual(digest, item["sha256"])

    def test_missing_primary_source_is_not_claimed_available(self):
        item = self.data["cw2_request"]
        self.assertFalse(item["primary_pdf_acquired"])
        self.assertIsNone(item["local_locator"])
        self.assertIsNone(item["sha256"])
        self.assertEqual(item["pages"], "397-408")

    def test_unclosed_gates_cannot_be_promoted(self):
        flags = self.data["project_gates"]
        self.assertTrue(flags["first_window_144_preserved"])
        self.assertTrue(flags["full_modulus_near_scalar_kernel_preserved"])
        for key in flags.keys() - {
            "first_window_144_preserved", "full_modulus_near_scalar_kernel_preserved"
        }:
            self.assertIs(flags[key], False)

    def test_each_cw2_leaf_and_source_caution_is_present(self):
        self.assertEqual(len(self.data["source_calls"]), 4)
        cautions = {item["key"] for item in self.data["audit_cautions"]}
        self.assertTrue({"signed_heights", "imprimitive_printed_step",
                         "contour_left_sign", "boundary_family"} <= cautions)

    def test_original_law_and_outer_exponent_are_retained(self):
        actual = self.data["actual_contract"]
        self.assertEqual(actual["U"], "q^160")
        self.assertFalse(actual["outer_D_changed"])
        self.assertFalse(actual["actual_X_q_U_values_generated"])


if __name__ == "__main__":
    unittest.main()
