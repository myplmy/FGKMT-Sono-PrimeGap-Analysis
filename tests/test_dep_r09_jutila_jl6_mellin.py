"""Fail-closed tests for the Jutila Lemma 6 Mellin component."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl6_mellin import (
    JL6_IMPRIMITIVE_CORRECTION_SQUARED,
    JL6_M_SUM_MULTIPLIER,
    build_jl6_mellin_evaluation,
    jl6_gamma_integral_multiplier,
    jl6_imprimitive_correction,
    jl6_l_vertical_multiplier,
    jl6_mellin_constant,
    jl6_shift_delta,
    n_over_phi_exact,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_Lemma6_Mellin_v1.json"
)


class DepR09JutilaLemma6MellinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 100

    def test_local_source_hashes_and_reading_modes(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if locator is None:
                continue
            path = REPO_ROOT / locator
            self.assertTrue(path.is_file(), source["key"])
            data = path.read_bytes()
            self.assertTrue(data.startswith(b"%PDF-"), source["key"])
            self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                source["audit_copy_sha256"],
                source["key"],
            )
        modes = {row["key"]: row["reading_mode"] for row in self.ledger["source_registry"]}
        self.assertEqual(
            modes["JUTILA_1977"],
            "OCR_ONLY_AFTER_NATIVE_TEXT_LAYER_FOUND_EMPTY_WITH_RENDERED_PAGE_COMPARISON",
        )
        self.assertEqual(
            modes["BENNETT_ET_AL_2021"],
            "NATIVE_TEXT_WITH_RENDERED_PAGE_COMPARISON",
        )
        self.assertEqual(
            modes["FIORI_2026"],
            "NATIVE_TEXT_WITH_RENDERED_PAGE_COMPARISON",
        )

    def test_shift_delta_has_required_range(self):
        for epsilon in (Fraction(1, 100), Fraction(1, 2), 1, 100):
            with self.subTest(epsilon=epsilon):
                delta = jl6_shift_delta(epsilon)
                self.assertGreater(delta, 0)
                self.assertLess(delta, mp.mpf(1) / 4)
                self.assertTrue(
                    mp.almosteq(delta, mp.mpf(str(epsilon)) / (4 * (1 + mp.mpf(str(epsilon)))))
                    if not isinstance(epsilon, Fraction)
                    else mp.almosteq(
                        delta,
                        (mp.mpf(epsilon.numerator) / epsilon.denominator)
                        / (4 * (1 + mp.mpf(epsilon.numerator) / epsilon.denominator)),
                    )
                )

    def test_exact_constant_composition(self):
        self.assertEqual(JL6_M_SUM_MULTIPLIER, Fraction(3, 1))
        self.assertEqual(JL6_IMPRIMITIVE_CORRECTION_SQUARED, Fraction(8, 3))
        self.assertTrue(mp.almosteq(jl6_imprimitive_correction() ** 2, mp.mpf(8) / 3))
        delta = mp.mpf("0.02")
        composed = (
            mp.mpf(1)
            / (2 * mp.pi)
            * jl6_l_vertical_multiplier(delta)
            * 3
            * jl6_gamma_integral_multiplier(delta)
        )
        self.assertTrue(mp.almosteq(composed, jl6_mellin_constant(delta)))

    def test_local_prime_factor_bounds(self):
        delta = Fraction(1, 5)
        for prime in (2, 3, 5, 7, 11, 97):
            with self.subTest(prime=prime):
                common = Fraction(prime * prime, prime - 1)
                self.assertLessEqual(Fraction(prime - 1, 1), common)
                self.assertLessEqual(Fraction(prime + 1, 1), common)
                self.assertLessEqual(
                    1 + mp.mpf(prime) ** (1 - mp.mpf(delta.numerator) / delta.denominator),
                    prime + 1,
                )

    def test_summatory_n_over_phi_is_below_three_R(self):
        for R in (1, 2, 10, 100, 1000):
            with self.subTest(R=R):
                exact_sum = sum((n_over_phi_exact(n) for n in range(1, R + 1)), Fraction())
                self.assertLess(exact_sum, 3 * R)

    def test_original_condition_implies_transferred_bound(self):
        evaluation = build_jl6_mellin_evaluation(
            q=3,
            T=1,
            R=2,
            z2=3,
            X=100,
            alpha=Fraction(3, 4),
            beta=Fraction(4, 5),
            epsilon=Fraction(1, 5),
        )
        self.assertTrue(evaluation.original_power_condition_holds)
        self.assertTrue(evaluation.transfer_exponent_budget_holds)
        self.assertLessEqual(
            evaluation.direct_mellin_bound,
            evaluation.transferred_mellin_bound,
        )
        self.assertFalse(evaluation.rigorous_interval_certificate)
        self.assertFalse(evaluation.source_theorem_local_axiom_used)
        self.assertFalse(evaluation.proof_escape_used)
        self.assertTrue(evaluation.jutila_lemma6_mellin_component_closed)
        self.assertFalse(evaluation.jutila_lemma6_tail_closed)
        self.assertFalse(evaluation.jutila_lemma6_closed)
        self.assertFalse(evaluation.numerical_x_cert_ready)

    def test_condition_failure_does_not_promote_component_to_full_lemma(self):
        evaluation = build_jl6_mellin_evaluation(
            q=3,
            T=1,
            R=2,
            z2=3,
            X=1,
            alpha=Fraction(3, 4),
            beta=Fraction(4, 5),
            epsilon=Fraction(1, 5),
        )
        self.assertFalse(evaluation.original_power_condition_holds)
        self.assertTrue(evaluation.transfer_exponent_budget_holds)
        self.assertFalse(evaluation.jutila_lemma6_closed)

    def test_invalid_parameters_are_rejected(self):
        base = dict(q=3, T=1, R=2, z2=3, X=100, alpha="0.75", beta="0.8", epsilon="0.2")
        invalid = (
            ("q", 2),
            ("q", 3.0),
            ("T", 0),
            ("R", 0),
            ("z2", 1),
            ("X", 0),
            ("alpha", "0.49"),
            ("alpha", 1),
            ("beta", "0.7"),
            ("beta", 1),
            ("epsilon", 0),
            ("epsilon", "nan"),
        )
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                args = dict(base)
                args[key] = value
                with self.assertRaises(ValueError):
                    build_jl6_mellin_evaluation(**args)

    def test_fiori_warning_scope_is_not_misapplied(self):
        scope = self.ledger["fiori_correction_scope"]
        self.assertEqual(scope["warning_target"], "ABSOLUTE_VALUE_OF_COMPLEX_LOG_FACTOR")
        self.assertEqual(scope["bound_used_here"], "POWER_OF_ABSOLUTE_VALUE_OF_S_PLUS_ONE")
        self.assertFalse(scope["invalidates_bennett_equation_5_3"])

    def test_machine_status_is_fail_closed(self):
        statuses = {row["id"]: row["status"] for row in self.ledger["jutila_nodes"]}
        self.assertEqual(statuses["JL6-MELLIN"], "ACTUAL_FORM_PARAMETERIZED_EXPLICIT")
        for node in ("JL6-TAIL", "JL6", "JL8"):
            self.assertEqual(statuses[node], "HARD_BLOCKER")
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
