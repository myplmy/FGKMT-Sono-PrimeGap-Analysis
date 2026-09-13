"""Fail-closed tests for the actual Jutila Lemma 6 common budget."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl5_finite import jl5_b_factor
from source.dep_r09_jutila_jl6_common_budget import (
    JL6_B_ABSORPTION_MULTIPLIER,
    JL6_B_EXPONENT_MULTIPLIER,
    JL6_SMALL_Q_MAX_Q_OVER_PHI,
    JL6_THETA_MAX,
    JL6_TOTIENT_LOG_MULTIPLIER,
    build_actual_jl6_common_budget_evaluation,
    jl6_actual_power_margin,
    jl6_b_factor_absorption_cutoff,
    jl6_b_factor_exponent_bound,
    jl6_uniform_totient_inverse_coefficient_bound,
)
from source.dep_r09_jutila_jl6_mellin import n_over_phi_exact


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_Lemma6_common_budget_v1.json"
)


class DepR09JutilaLemma6CommonBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 120

    def test_source_hashes_and_reading_modes(self):
        for source in self.ledger["source_registry"]:
            path = REPO_ROOT / source["audit_copy_locator"]
            data = path.read_bytes()
            self.assertTrue(data.startswith(b"%PDF-"), source["key"])
            self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                source["audit_copy_sha256"],
                source["key"],
            )
        self.assertIn(
            "OCR_ONLY_AFTER_NATIVE_TEXT_LAYER_FOUND_EMPTY",
            self.ledger["source_registry"][0]["reading_mode"],
        )

    def test_exact_constants_and_small_q_totient_cases(self):
        self.assertEqual(JL6_THETA_MAX, Fraction(1, 21))
        self.assertEqual(JL6_TOTIENT_LOG_MULTIPLIER, Fraction(6, 1))
        self.assertEqual(JL6_B_EXPONENT_MULTIPLIER, Fraction(3, 1))
        self.assertEqual(JL6_B_ABSORPTION_MULTIPLIER, Fraction(18, 1))
        self.assertEqual(JL6_SMALL_Q_MAX_Q_OVER_PHI, Fraction(3, 1))
        ratios = [n_over_phi_exact(q) for q in range(3, 16)]
        self.assertEqual(max(ratios), Fraction(3, 1))
        for ratio in ratios:
            self.assertLessEqual(float(ratio), 6 * math.e)

    def test_actual_power_margin_and_source_power_condition(self):
        for theta in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 21)):
            with self.subTest(theta=theta):
                margin = jl6_actual_power_margin(theta)
                self.assertGreaterEqual(margin, 0)
                theta_mpf = mp.mpf(theta.numerator) / theta.denominator
                lhs_exponent = (1 - theta_mpf) * (1 + 12 * theta_mpf)
                rhs_exponent = (1 + theta_mpf) * (1 + 9 * theta_mpf)
                self.assertTrue(mp.almosteq(lhs_exponent - rhs_exponent, margin))

    def test_b_factor_elementary_upper_envelope(self):
        cases = (
            (3, (3,)),
            (30, (2, 3, 5)),
            (2310, (2, 3, 5, 7, 11)),
            (30030, (2, 3, 5, 7, 11, 13)),
        )
        for q, primes in cases:
            with self.subTest(q=q):
                L = mp.log(q)
                upper = mp.exp(jl6_b_factor_exponent_bound(L))
                self.assertLessEqual(jl5_b_factor(primes), upper)

    def test_b_factor_absorption_cutoff(self):
        for theta in (Fraction(1, 100), Fraction(1, 42), Fraction(1, 21)):
            with self.subTest(theta=theta):
                theta_mpf = mp.mpf(theta.numerator) / theta.denominator
                cutoff = jl6_b_factor_absorption_cutoff(theta)
                lhs = jl6_b_factor_exponent_bound(cutoff)
                rhs = theta_mpf * cutoff / 6
                self.assertTrue(lhs <= rhs or mp.almosteq(lhs, rhs))

    def test_uniform_inverse_coefficient_formula_is_guarded(self):
        with self.assertRaises(ValueError):
            jl6_uniform_totient_inverse_coefficient_bound(2)
        L = mp.e
        self.assertTrue(
            mp.almosteq(
                jl6_uniform_totient_inverse_coefficient_bound(L),
                mp.pi**2 * L,
            )
        )

    def test_equal_split_cutoff_pays_all_four_budgets(self):
        cases = (
            (Fraction(1, 100), Fraction(1, 400)),
            (Fraction(1, 42), Fraction(1, 168)),
            (Fraction(1, 21), Fraction(1, 84)),
        )
        for theta, part in cases:
            with self.subTest(theta=theta):
                evaluation = build_actual_jl6_common_budget_evaluation(
                    theta=theta,
                    eta_output=theta,
                    eta_jl5=part,
                    eta_damping=part,
                    eta_mellin=part,
                    eta_tail=part,
                )
                self.assertTrue(evaluation.budget_balance_holds)
                self.assertTrue(evaluation.power_condition_margin_holds)
                self.assertTrue(evaluation.component_bounds_meet_allocations)
                self.assertLessEqual(
                    evaluation.total_relative_upper_at_cutoff,
                    evaluation.eta_output,
                )
                self.assertGreaterEqual(
                    evaluation.sufficient_log_D_cutoff,
                    evaluation.original_log_condition_cutoff,
                )

    def test_builder_preserves_fail_closed_boundaries(self):
        evaluation = build_actual_jl6_common_budget_evaluation(
            theta=Fraction(1, 100),
            eta_output=Fraction(1, 100),
            eta_jl5=Fraction(1, 400),
            eta_damping=Fraction(1, 400),
            eta_mellin=Fraction(1, 400),
            eta_tail=Fraction(1, 400),
        )
        self.assertTrue(
            evaluation.jutila_lemma6_actual_application_parameterized_explicit
        )
        self.assertFalse(evaluation.jutila_lemma6_printed_general_statement_closed)
        self.assertFalse(evaluation.jutila_lemma8_closed)
        self.assertFalse(evaluation.pap_11_closed)
        self.assertFalse(evaluation.dep_r09_closed)
        self.assertFalse(evaluation.fixed_2e_minus_17_independently_certified)
        self.assertFalse(evaluation.numerical_x_cert_ready)
        self.assertFalse(evaluation.rigorous_interval_certificate)
        self.assertFalse(evaluation.source_theorem_local_axiom_used)
        self.assertFalse(evaluation.proof_escape_used)

    def test_invalid_parameters_fail_closed(self):
        valid = {
            "theta": Fraction(1, 100),
            "eta_output": Fraction(1, 100),
            "eta_jl5": Fraction(1, 400),
            "eta_damping": Fraction(1, 400),
            "eta_mellin": Fraction(1, 400),
            "eta_tail": Fraction(1, 400),
        }
        bad_cases = (
            {"theta": 0},
            {"theta": Fraction(1, 20)},
            {"eta_output": Fraction(1, 5)},
            {"eta_output": 1},
            {"eta_jl5": 0},
            {"eta_tail": Fraction(1, 100)},
        )
        for replacement in bad_cases:
            with self.subTest(replacement=replacement):
                kwargs = valid | replacement
                with self.assertRaises(ValueError):
                    build_actual_jl6_common_budget_evaluation(**kwargs)

    def test_machine_ledger_statuses_are_fail_closed(self):
        statuses = {row["id"]: row["status"] for row in self.ledger["jutila_nodes"]}
        self.assertEqual(
            statuses["JL6-COMMON-BUDGET"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            statuses["JL6-ACTUAL"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT",
        )
        self.assertIn("OPEN", statuses["JL6-PRINTED-GENERAL"])
        self.assertEqual(statuses["JL8"], "HARD_BLOCKER")
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
