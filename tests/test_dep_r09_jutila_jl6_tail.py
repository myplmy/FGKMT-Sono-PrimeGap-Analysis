"""Fail-closed tests for the actual Jutila Lemma 6 truncation tail."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl6_tail import (
    JL6_TAIL_COEFFICIENT_MULTIPLIER,
    JL6_TAIL_SIMPLIFIED_MULTIPLIER,
    build_actual_jl6_tail_evaluation,
    jl6_endpoint_free_tail_bound,
    jl6_geometric_reciprocal_bound,
    jl6_tail_envelope,
    jl6_tail_sufficient_log_cutoff,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_Lemma6_tail_actual_v1.json"
)


def _divisor_count(n: int) -> int:
    return sum(1 for d in range(1, n + 1) if n % d == 0)


class DepR09JutilaLemma6TailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 100

    def test_source_hash_and_original_scope(self):
        source = self.ledger["source_registry"][0]
        path = REPO_ROOT / source["audit_copy_locator"]
        data = path.read_bytes()
        self.assertTrue(data.startswith(b"%PDF-"))
        self.assertEqual(len(data), source["audit_copy_bytes"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), source["audit_copy_sha256"])
        self.assertEqual(source["native_text_bytes"], 18)
        self.assertIn(51, source["rendered_printed_pages_checked"])
        self.assertIn(52, source["rendered_printed_pages_checked"])

    def test_elementary_coefficient_multipliers(self):
        self.assertEqual(JL6_TAIL_COEFFICIENT_MULTIPLIER, Fraction(2, 1))
        self.assertEqual(JL6_TAIL_SIMPLIFIED_MULTIPLIER, Fraction(4, 1))
        for n in range(1, 1001):
            with self.subTest(n=n):
                self.assertLessEqual(_divisor_count(n), 2 * math.sqrt(n))

    def test_geometric_reciprocal_bound(self):
        for X in (Fraction(1, 10), 1, 2, 10, 100):
            with self.subTest(X=X):
                x = mp.mpf(X.numerator) / X.denominator if isinstance(X, Fraction) else mp.mpf(X)
                exact = 1 / (1 - mp.exp(-1 / x))
                self.assertLessEqual(exact, jl6_geometric_reciprocal_bound(X))

    def test_endpoint_free_bound_dominates_exact_geometric_tail(self):
        for D, R, X in ((3, 1, 1), (10, 2, 3), (100, 7, 11)):
            with self.subTest(D=D, R=R, X=X):
                cut = mp.mpf(X) * mp.log(D) ** 2
                first = int(mp.floor(cut)) + 1
                exact_geometric_majorant = (
                    2 * R * mp.exp(-mp.mpf(first) / X) / (1 - mp.exp(-mp.mpf(1) / X))
                )
                self.assertLessEqual(
                    exact_geometric_majorant,
                    jl6_endpoint_free_tail_bound(D=D, R=R, X=X),
                )

    def test_actual_parameter_exponent_and_simplification(self):
        evaluation = build_actual_jl6_tail_evaluation(
            D=1000,
            epsilon=Fraction(1, 100),
            absolute_tail_budget=1,
        )
        self.assertTrue(mp.almosteq(evaluation.actual_exponent_sum, mp.mpf("1.13")))
        self.assertLessEqual(
            evaluation.endpoint_free_tail_bound,
            evaluation.simplified_actual_tail_bound,
        )
        expected = jl6_tail_envelope(
            log_D=mp.log(1000),
            r_exponent=Fraction(1, 100),
            x_exponent=Fraction(28, 25),
        )
        self.assertTrue(mp.almosteq(evaluation.simplified_actual_tail_bound, expected))

    def test_sufficient_cutoff_pays_tail_budget(self):
        for epsilon, tau in (
            (Fraction(1, 100), Fraction(1, 10)),
            (Fraction(1, 10), Fraction(1, 1000)),
            (1, Fraction(1, 10**12)),
        ):
            with self.subTest(epsilon=epsilon, tau=tau):
                x_exponent = 1 + 12 * (mp.mpf(epsilon.numerator) / epsilon.denominator)
                cutoff = jl6_tail_sufficient_log_cutoff(
                    r_exponent=epsilon,
                    x_exponent=x_exponent,
                    absolute_tail_budget=tau,
                )
                bound = jl6_tail_envelope(
                    log_D=cutoff,
                    r_exponent=epsilon,
                    x_exponent=x_exponent,
                )
                tau_mpf = mp.mpf(tau.numerator) / tau.denominator
                self.assertLessEqual(bound, tau_mpf)

    def test_actual_builder_preserves_fail_closed_boundaries(self):
        evaluation = build_actual_jl6_tail_evaluation(
            D=mp.exp(10),
            epsilon=Fraction(1, 100),
            absolute_tail_budget=Fraction(1, 100),
        )
        self.assertTrue(evaluation.cutoff_holds)
        self.assertTrue(evaluation.tail_budget_met)
        self.assertTrue(evaluation.jutila_lemma6_tail_actual_component_closed)
        self.assertFalse(evaluation.jutila_lemma6_tail_general_statement_closed)
        self.assertFalse(evaluation.jutila_lemma6_common_error_budget_closed)
        self.assertFalse(evaluation.jutila_lemma6_closed)
        self.assertFalse(evaluation.numerical_x_cert_ready)
        self.assertFalse(evaluation.rigorous_interval_certificate)
        self.assertFalse(evaluation.source_theorem_local_axiom_used)
        self.assertFalse(evaluation.proof_escape_used)

    def test_invalid_inputs_fail_closed(self):
        for kwargs in (
            {"D": 1, "epsilon": 1, "absolute_tail_budget": 1},
            {"D": 10, "epsilon": 0, "absolute_tail_budget": 1},
            {"D": 10, "epsilon": 1, "absolute_tail_budget": 0},
            {"D": 10, "epsilon": 1, "absolute_tail_budget": 5},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    build_actual_jl6_tail_evaluation(**kwargs)

    def test_machine_ledger_statuses_are_fail_closed(self):
        statuses = {row["id"]: row["status"] for row in self.ledger["jutila_nodes"]}
        self.assertEqual(
            statuses["JL6-TAIL-ACTUAL"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            statuses["JL6-TAIL-GENERAL"],
            "OPEN_PRINTED_STATEMENT_REQUIRES_X_UPPER_ENVELOPE_OR_CANCELLATION",
        )
        self.assertEqual(statuses["JL6-COMMON-BUDGET"], "HARD_BLOCKER")
        self.assertEqual(statuses["JL6"], "HARD_BLOCKER")
        for flag in (
            "pap_11_closed",
            "dep_r09_closed",
            "fixed_2e_minus_17_independently_certified",
            "threshold_calculator_ready",
            "numerical_x_cert_ready",
            "actual_prime_computation_run",
            "source_theorem_local_axiom_used",
            "proof_escape_used",
        ):
            self.assertFalse(self.ledger[flag], flag)


if __name__ == "__main__":
    unittest.main()
