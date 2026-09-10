"""Fail-closed contract tests for the DEP-R09 full-source recovery ledger."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_source_recovery_v1.json"
)


class DepR09SourceRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_sources_are_exactly_hash_pinned_and_native_text_audited(self):
        self.assertTrue(self.ledger["full_sources_acquired"])
        self.assertTrue(self.ledger["reading_policy"]["native_text_first"])
        self.assertFalse(self.ledger["reading_policy"]["ocr_used"])
        self.assertTrue(self.ledger["reading_policy"]["visual_page_check_completed"])

        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["locator"]
            self.assertTrue(path.is_file(), source["locator"])
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, source["sha256"])

    def test_printed_and_source_compatible_bridge_constants_are_distinct(self):
        c_zfr = Fraction(1, 24)
        self.assertEqual(c_zfr / 3, Fraction(1, 72))
        self.assertEqual(3 * c_zfr, Fraction(1, 8))
        self.assertNotEqual(c_zfr / 3, 3 * c_zfr)

        mccurley_r = Fraction(9_645_908_801, 1_000_000_000)
        direct_c1 = Fraction(1, 24)
        self.assertLess(mccurley_r, 12)
        self.assertLess(2 * mccurley_r * direct_c1, 1)

    def test_repaired_exponent_and_range_gate_are_exact(self):
        direct_c1 = Fraction(1, 24)
        a0 = direct_c1 / 10
        self.assertEqual(a0, Fraction(1, 240))
        self.assertEqual(a0 * 160, Fraction(2, 3))
        self.assertEqual(Fraction(5 * 16, 160), Fraction(1, 2))
        self.assertEqual(160**2, 25_600)

    def test_coefficient_diagnostics_recompute_at_high_precision(self):
        mp.mp.dps = 80
        gamma = mp.euler
        c_ub = 8 * mp.exp(2 * gamma)

        def coefficient(c_pap, d_pap, common_power):
            return (
                c_pap**2
                * (mp.mpf(1) / 3)
                * (mp.mpf(1) / 4)
                * mp.exp(4 * gamma)
                / (
                    mp.mpf(737_280_000)
                    * mp.log(5)
                    * c_ub
                    * common_power
                    * (1 + 1 / mp.mpf(d_pap)) ** 4
                    * (25 * c_ub + 20 * mp.exp(gamma) * common_power)
                )
            )

        expected = {
            "Sono printed": coefficient(1 - mp.exp(-2), 160, 160),
            "direct McCurley conservative baseline, optimistic K_G=1": coefficient(
                1 - mp.exp(-mp.mpf(2) / 3), 160, 160
            ),
            "restore a0*D=2 with D=M=480, optimistic K_G=1": coefficient(
                1 - mp.exp(-2), 480, 480
            ),
            "sharp direct McCurley c1=1/(2R), optimistic K_G=1": coefficient(
                1 - mp.exp(-mp.mpf(8) / mp.mpf("9.645908801")), 160, 160
            ),
        }
        for row in self.ledger["coefficient_diagnostics"]:
            observed = mp.mpf(row["c_hat_80dps"])
            self.assertTrue(mp.almosteq(observed, expected[row["package"]], rel_eps=mp.mpf("1e-49")))
        target = mp.mpf(2) * mp.mpf(10) ** -17
        self.assertGreater(expected["Sono printed"], target)
        for package, value in expected.items():
            if package != "Sono printed":
                self.assertLess(value, target, package)

    def test_gate_remains_fail_closed(self):
        self.assertEqual(
            self.ledger["outcome"], "SONO_SECTION5_NORMALIZATION_NOT_CERTIFIED"
        )
        self.assertFalse(self.ledger["numerical_pap_package_ready"])
        self.assertFalse(self.ledger["pap_11_closed"])
        self.assertFalse(self.ledger["threshold_calculator_ready"])
        self.assertFalse(self.ledger["numerical_x_cert_ready"])
        statuses = {row["id"]: row["status"] for row in self.ledger["obligations"]}
        self.assertEqual(statuses["R09-07"], "HARD_BLOCKER")
        self.assertEqual(statuses["R09-10"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
