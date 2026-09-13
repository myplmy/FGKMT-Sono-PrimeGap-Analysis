"""Fail-closed checks for the DEP-R09 explicit PNT-in-AP source audit."""

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
    / "Sono_FMT_DEPR09_explicit_PNT_AP_replacement_v1.json"
)


class DepR09ExplicitPntApReplacementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

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

    def test_public_version_audit_is_narrow_and_fail_closed(self):
        version = self.ledger["official_version_audit"]
        self.assertEqual(version["arxiv_id"], "2404.06951v4")
        self.assertTrue(version["relevant_printed_constants_unchanged"])
        self.assertFalse(version["public_correction_or_erratum_identified"])
        self.assertFalse(self.ledger["author_contact_performed"])
        self.assertIn("public", version["scope_note"].lower())

        journal = REPO_ROOT / version["journal_locator"]
        self.assertTrue(journal.is_file())
        self.assertEqual(
            hashlib.sha256(journal.read_bytes()).hexdigest(),
            version["journal_sha256"],
        )

    def test_available_audit_copies_match_registered_hashes(self):
        paths_and_hashes = [
            (
                self.ledger["official_version_audit"]["arxiv_audit_copy_locator"],
                self.ledger["official_version_audit"]["arxiv_audit_copy_sha256"],
            )
        ]
        paths_and_hashes.extend(
            (row["audit_copy_locator"], row["audit_copy_sha256"])
            for row in self.ledger["source_registry"]
        )
        for locator, expected in paths_and_hashes:
            path = REPO_ROOT / locator
            # tmp copies are audit conveniences rather than durable repository inputs.
            # When present, they must be byte-identical to the recorded source.
            if path.is_file():
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_no_candidate_is_misclassified_as_drop_in_pap(self):
        classes = {row["key"]: row["classification"] for row in self.ledger["source_registry"]}
        self.assertEqual(len(classes), 7)
        self.assertFalse(any(value == "DROP_IN_NUMERICAL_PAP" for value in classes.values()))
        self.assertIn("NUMERICAL_CONSTANTS_NOT_PRINTED", classes["THORNER_ZAMAN_REFINEMENTS_PNT_AP"])
        self.assertIn("NEW_TRANSFER_REQUIRED", classes["THORNER_ZAMAN_EXPLICIT_BOMBIERI_DENSITY"])
        self.assertIn("NOT_PAP", classes["BENLI_GOEL_TWISS_ZAMAN_EXPLICIT_DH"])

    def test_d160_coefficient_and_error_budget_recompute(self):
        mp.mp.dps = 80
        target = mp.mpf(2) * mp.mpf(10) ** -17
        capacity = self.ledger["coefficient_capacity"]
        c_min = mp.sqrt(target / self.coefficient(mp.mpf(1), 160, 160))
        total_error = 1 - c_min
        printed_error = mp.exp(-2)
        extra_error = total_error - printed_error
        relative_headroom = (1 - printed_error) / c_min - 1

        expected = {
            "d_160_c_pap_min_80dps": c_min,
            "d_160_total_relative_error_max_80dps": total_error,
            "printed_exp_minus_2_error_80dps": printed_error,
            "additional_error_slack_after_exp_minus_2_80dps": extra_error,
            "relative_c_pap_headroom_80dps": relative_headroom,
        }
        for key, value in expected.items():
            self.assertTrue(
                mp.almosteq(mp.mpf(capacity[key]), value, rel_eps=mp.mpf("1e-49")),
                key,
            )
        self.assertGreater(extra_error, 0)
        self.assertLess(extra_error, mp.mpf("0.001"))

    def test_optimistic_integer_d_capacity_is_exactly_186(self):
        mp.mp.dps = 80
        target = mp.mpf(2) * mp.mpf(10) ** -17
        passing = [
            d
            for d in range(1, 1_000)
            if self.coefficient(mp.mpf(1), d, d) >= target
        ]
        self.assertEqual(max(passing), 186)
        self.assertGreaterEqual(self.coefficient(mp.mpf(1), 186, 186), target)
        self.assertLess(self.coefficient(mp.mpf(1), 187, 187), target)

        capacity = self.ledger["coefficient_capacity"]
        self.assertEqual(capacity["optimistic_c_pap_one_max_integer_d"], 186)
        for row in capacity["samples"]:
            observed = mp.mpf(row["c_hat_80dps"])
            expected = self.coefficient(mp.mpf(row["C_PAP"]), row["D"], row["M"])
            self.assertTrue(mp.almosteq(observed, expected, rel_eps=mp.mpf("1e-48")))
            self.assertEqual(row["passes_target"], expected >= target)

    def test_density_exponents_are_not_silently_promoted_to_pap_d(self):
        density = next(
            row
            for row in self.ledger["source_registry"]
            if row["key"] == "THORNER_ZAMAN_EXPLICIT_BOMBIERI_DENSITY"
        )
        self.assertEqual(density["constants"]["all_sigma_nonexceptional_exponent"], 127)
        self.assertEqual(density["constants"]["all_sigma_exceptional_removed_exponent"], 198)
        self.assertIn("not automatically identical", self.ledger["coefficient_capacity"]["interpretation"])

    def test_final_gate_remains_open(self):
        self.assertEqual(
            self.ledger["outcome"], "NO_DROP_IN_NUMERICAL_PAP_REPLACEMENT_FOUND"
        )
        self.assertFalse(self.ledger["numerical_pap_package_ready"])
        self.assertFalse(self.ledger["pap_11_closed"])
        self.assertFalse(self.ledger["threshold_calculator_ready"])
        self.assertFalse(self.ledger["numerical_x_cert_ready"])
        self.assertFalse(self.ledger["actual_prime_computation_run"])
        statuses = {row["id"]: row["status"] for row in self.ledger["obligations"]}
        self.assertEqual(statuses["R09-RS03"], "HARD_BLOCKER")
        self.assertEqual(statuses["R09-RS07"], "HARD_BLOCKER")
        self.assertEqual(statuses["R09-RS08"], "EXPLICIT_DIAGNOSTIC")


if __name__ == "__main__":
    unittest.main()
