"""Fail-closed checks for the DEP-R09 Branch S transfer audit."""

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
    / "Sono_FMT_DEPR09_branch_S_transfer_v1.json"
)


class DepR09BranchSTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 80

    @staticmethod
    def coefficient(c_pap, d_pap, common_power):
        gamma = mp.euler
        c_ub = 8 * mp.exp(2 * gamma)
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
                * (1 + mp.mpf(1) / d_pap) ** 4
                * (25 * c_ub + 20 * mp.exp(gamma) * common_power)
            )
        )

    def test_registered_local_source_copies_match_hash_and_size(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if locator is None:
                continue
            path = REPO_ROOT / locator
            # tmp copies are audit conveniences. If present, they must match the
            # registered official-source bytes exactly.
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"])
                self.assertEqual(
                    hashlib.sha256(data).hexdigest(),
                    source["audit_copy_sha256"],
                )

    def test_jutila_ocr_was_used_only_after_empty_text_layer_check(self):
        source = next(
            row for row in self.ledger["source_registry"] if row["key"] == "JUTILA_1977"
        )
        self.assertEqual(source["native_text_bytes"], 18)
        self.assertIn("OCR_ONLY_AFTER_NATIVE_TEXT_LAYER_FOUND_EMPTY", source["reading_mode"])
        native = REPO_ROOT / source["native_text_locator"]
        if native.is_file():
            self.assertEqual(native.stat().st_size, 18)
        self.assertEqual(source["rendered_printed_pages_checked"], [46, 47, 54, 58, 59, 61])

    def test_huxley_official_source_is_hash_pinned_but_not_numerical(self):
        source = next(
            row for row in self.ledger["source_registry"] if row["key"] == "HUXLEY_1974_75"
        )
        self.assertTrue(source["local_audit_copy_available"])
        self.assertEqual(source["access_status"], "OFFICIAL_SOURCE_ACQUIRED_AND_HASHED")
        self.assertEqual(
            source["classification"],
            "SOURCE_LEAF_AVAILABLE_NUMERICAL_MULTIPLIER_AND_CUTOFF_OPEN",
        )
        path = REPO_ROOT / source["audit_copy_locator"]
        data = path.read_bytes()
        self.assertEqual(len(data), source["audit_copy_bytes"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), source["audit_copy_sha256"])
        self.assertTrue(data.startswith(b"%PDF-"))

    def test_fixed_d_transfer_gate_samples_recompute(self):
        gate = self.ledger["fixed_d_transfer_gate"]
        d = mp.mpf(gate["d"])
        eta = mp.mpf(gate["eta"])
        self.assertGreater(eta, 0)
        self.assertLess(eta, 1)
        for row in gate["samples"]:
            k = mp.mpf(row["K"])
            observed = mp.mpf(row["c_min_80dps"])
            expected = (mp.log(k) - mp.log(eta)) / d
            self.assertTrue(mp.almosteq(observed, expected, rel_eps=mp.mpf("1e-48")))
            self.assertTrue(
                mp.almosteq(k * mp.exp(-d * observed), eta, rel_eps=mp.mpf("1e-48"))
            )

    def test_d_capacity_samples_recompute_from_exact_decimal_target(self):
        target = mp.mpf(2) * mp.mpf(10) ** -17
        for row in self.ledger["d_capacity_samples"]:
            d = row["D"]
            optimistic = self.coefficient(mp.mpf(1), d, d)
            c_min = mp.sqrt(target / optimistic)
            eta = 1 - c_min
            self.assertTrue(
                mp.almosteq(
                    optimistic,
                    mp.mpf(row["optimistic_c_hat_80dps"]),
                    rel_eps=mp.mpf("1e-47"),
                )
            )
            self.assertTrue(
                mp.almosteq(c_min, mp.mpf(row["c_pap_min_80dps"]), rel_eps=mp.mpf("1e-47"))
            )
            self.assertTrue(
                mp.almosteq(eta, mp.mpf(row["total_error_max_80dps"]), rel_eps=mp.mpf("1e-47"))
            )

    def test_fixed_d_observation_does_not_claim_x_decay(self):
        gate = self.ledger["fixed_d_transfer_gate"]
        self.assertIn("does not vanish merely by increasing x", gate["fixed_d_asymptotic_observation"])
        self.assertIn("conditional algebraic diagnostic", gate["scope"])

    def test_all_root_claims_remain_fail_closed(self):
        self.assertEqual(
            self.ledger["outcome"],
            "STRUCTURAL_ROUTE_CONFIRMED_NUMERICAL_TRANSFER_NOT_RECOVERED",
        )
        for key in (
            "numerical_pap_package_ready",
            "pap_11_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(self.ledger[key], key)
        statuses = {row["id"]: row["status"] for row in self.ledger["obligations"]}
        self.assertEqual(statuses["RS02-A"], "HARD_BLOCKER")
        self.assertEqual(statuses["RS03"], "HARD_BLOCKER")
        self.assertEqual(statuses["RS07"], "HARD_BLOCKER")
        self.assertNotEqual(statuses["RS08"], "PAP_THEOREM_PROVED")


if __name__ == "__main__":
    unittest.main()
