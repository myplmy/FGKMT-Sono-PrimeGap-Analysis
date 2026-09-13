"""Fail-closed checks for the finite Jutila Lemma 5 replacement."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl5_finite import (
    JL5_SOURCE_ERROR_COEFFICIENT,
    build_jl5_finite_evaluation,
    finite_lower_bound_gate,
    jl5_b_factor,
    jl5_main_coefficient,
    phi_over_q,
    source_error_bound,
    validate_complete_prime_divisors,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_Lemma5_finite_v1.json"
)


class DepR09JutilaLemma5FiniteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 100

    def test_peer_reviewed_source_is_present_and_exact(self):
        source = self.ledger["source_registry"][0]
        path = REPO_ROOT / source["audit_copy_locator"]
        self.assertTrue(path.is_file())
        data = path.read_bytes()
        self.assertTrue(data.startswith(b"%PDF-"))
        self.assertEqual(len(data), source["audit_copy_bytes"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), source["audit_copy_sha256"])
        self.assertEqual(source["reading_mode"], "NATIVE_TEXT_WITH_RENDERED_PAGE_COMPARISON")

    def test_all_registered_local_source_hashes(self):
        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["audit_copy_locator"]
            self.assertTrue(path.is_file(), source["key"])
            data = path.read_bytes()
            if "audit_copy_bytes" in source:
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                source["audit_copy_sha256"],
                source["key"],
            )

    def test_source_error_constant_is_exact_decimal(self):
        self.assertEqual(JL5_SOURCE_ERROR_COEFFICIENT, Fraction(1277, 500))
        self.assertEqual(
            self.ledger["source_corollary"]["absolute_error_coefficient_rational"],
            "1277/500",
        )

    def test_complete_prime_support_validation(self):
        self.assertEqual(validate_complete_prime_divisors(1, ()), ())
        self.assertEqual(validate_complete_prime_divisors(360, (2, 3, 5)), (2, 3, 5))
        for q, factors in (
            (30, (2, 3)),
            (30, (2, 3, 5, 5)),
            (30, (2, 3, 6)),
            (30, (2, 3, 7)),
            (1, (2,)),
            (2, (2.0,)),
        ):
            with self.subTest(q=q, factors=factors):
                with self.assertRaises(ValueError):
                    validate_complete_prime_divisors(q, factors)

    def test_source_products_match_direct_formulas(self):
        factors = (2, 3, 5)
        expected_c = (
            mp.mpf(6)
            / mp.pi**2
            * mp.mpf(2)
            / 3
            * mp.mpf(3)
            / 4
            * mp.mpf(5)
            / 6
        )
        expected_phi = mp.mpf(1) / 2 * mp.mpf(2) / 3 * mp.mpf(4) / 5
        expected_b = mp.mpf(1)
        for prime in factors:
            p = mp.mpf(prime)
            expected_b *= 1 + (p ** (mp.mpf(2) / 3) - 1) / (
                p ** (mp.mpf(4) / 3) + 1
            )
        self.assertTrue(mp.almosteq(jl5_main_coefficient(factors), expected_c))
        self.assertTrue(mp.almosteq(phi_over_q(factors), expected_phi))
        self.assertTrue(mp.almosteq(jl5_b_factor(factors), expected_b))

    def test_jutila_phi_bridge_is_in_safe_direction(self):
        for q, factors in ((1, ()), (2, (2,)), (30, (2, 3, 5)), (2310, (2, 3, 5, 7, 11))):
            with self.subTest(q=q):
                c_q = jl5_main_coefficient(factors)
                weaker = mp.mpf(6) / mp.pi**2 * phi_over_q(factors)
                self.assertGreaterEqual(c_q, weaker)

    def test_simple_cutoff_pays_the_published_error(self):
        for q, factors, eta in (
            (1, (), Fraction(1, 2)),
            (30, (2, 3, 5), Fraction(1, 10)),
            (2310, (2, 3, 5, 7, 11), "0.01"),
        ):
            with self.subTest(q=q, eta=str(eta)):
                evaluation = build_jl5_finite_evaluation(q, factors, eta)
                r_value = evaluation.sufficient_cutoff
                self.assertTrue(finite_lower_bound_gate(evaluation, r_value))
                self.assertGreaterEqual(r_value, mp.e)
                self.assertGreaterEqual(
                    mp.log(r_value),
                    mp.sqrt(mp.log(q)),
                )
                self.assertLessEqual(
                    source_error_bound(evaluation, r_value),
                    evaluation.eta * evaluation.c_q * mp.log(r_value),
                )
                self.assertFalse(evaluation.rigorous_interval_certificate)
                self.assertFalse(evaluation.jutila_lemma6_closed)
                self.assertFalse(evaluation.numerical_x_cert_ready)

    def test_invalid_eta_and_r_are_rejected(self):
        for eta in (0, "-0.1", "1.0001", "nan", "inf"):
            with self.subTest(eta=eta):
                with self.assertRaises(ValueError):
                    build_jl5_finite_evaluation(1, (), eta)
        evaluation = build_jl5_finite_evaluation(1, (), Fraction(1, 2))
        for r_value in (0, -1, "nan", "inf"):
            with self.subTest(r_value=r_value):
                with self.assertRaises(ValueError):
                    finite_lower_bound_gate(evaluation, r_value)

    def test_machine_status_closes_only_jl5(self):
        statuses = {row["id"]: row["status"] for row in self.ledger["jutila_nodes"]}
        self.assertEqual(
            statuses["JL5"],
            "EXPLICIT_PEER_REVIEWED_SOURCE_REPLACEMENT_WITH_Q_DEPENDENT_CUTOFF",
        )
        for node in ("JL6", "JL8"):
            self.assertEqual(statuses[node], "HARD_BLOCKER")
        self.assertFalse(self.ledger["pap_11_closed"])
        self.assertFalse(self.ledger["dep_r09_closed"])
        self.assertFalse(self.ledger["fixed_2e_minus_17_independently_certified"])
        self.assertFalse(self.ledger["threshold_calculator_ready"])
        self.assertFalse(self.ledger["numerical_x_cert_ready"])
        self.assertFalse(self.ledger["actual_prime_computation_run"])
        self.assertFalse(self.ledger["source_theorem_local_axiom_used"])
        self.assertFalse(self.ledger["proof_escape_used"])


if __name__ == "__main__":
    unittest.main()
