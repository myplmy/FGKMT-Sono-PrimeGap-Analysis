"""Fail-closed checks for the DEP-R09 Jutila Lemma 4--8 inventory."""

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
    / "Sono_FMT_DEPR09_Jutila_Lemma4_8_v1.json"
)


class DepR09JutilaLemma48Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 80

    def test_registered_source_hashes_and_sizes(self):
        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["audit_copy_locator"]
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
                self.assertEqual(
                    hashlib.sha256(data).hexdigest(),
                    source["audit_copy_sha256"],
                    source["key"],
                )

    def test_permanent_huxley_source_is_present_and_exact(self):
        source = next(
            row for row in self.ledger["source_registry"] if row["key"] == "HUXLEY_1975_III"
        )
        path = REPO_ROOT / source["audit_copy_locator"]
        self.assertTrue(path.is_file())
        data = path.read_bytes()
        self.assertEqual(len(data), 388706)
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "cc8b7282c1963687d357829416d5e471e130810e5324709a96319bb7a2a3428f",
        )
        self.assertTrue(data.startswith(b"%PDF-"))
        self.assertIn("OCR_ONLY_AFTER_NATIVE_TEXT_LAYER_FOUND_EMPTY", source["reading_mode"])

    def test_theorem_one_prime_tau_and_coefficient_are_exact(self):
        tau = Fraction(8, 5)
        coefficient = (
            Fraction(309, 100)
            * (
                Fraction(1084, 1000) * (tau + 1)
                + Fraction(1301, 1000) * (1 + tau**2)
                - Fraction(116, 1000)
            )
            / (tau - 1)
        )
        self.assertEqual(coefficient, Fraction(18884947, 500000))
        actual = self.ledger["actual_bv_specialization"]
        self.assertEqual(actual["scope_id"], "JL4-T1PRIME-ACTUAL")
        self.assertEqual(actual["tau"], "8/5")
        self.assertEqual(actual["coefficient_rational"], "18884947/500000")
        self.assertFalse(actual["applies_to_equation_3_6"])
        self.assertEqual(mp.mpf(coefficient.numerator) / coefficient.denominator, mp.mpf("37.769894"))

    def test_finite_parameter_identities(self):
        for d in (mp.mpf("1e10"), mp.mpf("1e100"), mp.e ** mp.mpf(1000)):
            log_d = mp.log(d)
            log2_d = mp.log(log_d)
            x_d = d ** (mp.mpf(11) / 2) * log_d**2
            z1 = d ** (mp.mpf(5) / 2)
            z2 = d**4
            ratio = mp.log(x_d) / mp.log(z2 / z1)
            expected_ratio = mp.mpf(11) / 3 + mp.mpf(4) / 3 * log2_d / log_d
            self.assertTrue(mp.almosteq(ratio, expected_ratio, rel_eps=mp.mpf("1e-65")))

            lam = mp.mpf("0.125")
            alpha = 1 - lam / log_d
            lhs = mp.power(x_d, 2 - 2 * alpha)
            rhs = mp.exp(11 * lam + 4 * lam * log2_d / log_d)
            self.assertTrue(mp.almosteq(lhs, rhs, rel_eps=mp.mpf("1e-65")))

    def test_scope_separates_theorem_one_prime_from_equation_3_6(self):
        statuses = {row["id"]: row["status"] for row in self.ledger["jutila_nodes"]}
        self.assertEqual(
            statuses["JL4-T1PRIME-ACTUAL"],
            "ACTUAL_APPLICATION_EXPLICIT_SOURCE_REPLACEMENT",
        )
        self.assertEqual(
            statuses["JL4-T1-DENSITY-ACTUAL"],
            "CORRECTED_BY_SUCCESSOR_THEORY66",
        )
        self.assertEqual(statuses["JL4-FULL"], "SOURCE_THEOREM_UNFORMALIZED")
        for node in ("JL5", "JL6", "JL8"):
            self.assertEqual(statuses[node], "HARD_BLOCKER")
        self.assertFalse(
            self.ledger["actual_bv_specialization"]["jutila_printed_10_exp_11lambda_certified"]
        )

    def test_all_root_claims_remain_fail_closed(self):
        self.assertEqual(
            self.ledger["outcome"],
            "THEOREM1PRIME_LEMMA4_ACTUAL_EXPLICIT_EQUATION3_6_SCOPE_CORRECTED_IN_THEORY66",
        )
        for key in (
            "numerical_pap_package_ready",
            "pap_11_closed",
            "dep_r09_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(self.ledger[key], key)
        self.assertFalse(self.ledger["user_compute_required_now"])
        self.assertFalse(self.ledger["new_dependency_required_now"])


if __name__ == "__main__":
    unittest.main()
