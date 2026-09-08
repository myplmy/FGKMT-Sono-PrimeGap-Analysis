"""Regression checks for the H1b-2a.3 P9.4 end-to-end composition."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L1135_CANONICAL_FACTOR,
)
from source.h1b1b2d_rfold_smooth_package import rfold_error_certificate
from source.h1b1b2d1b_sharp_scale import fmt_sharp_relative_error_upper
from source.h1b2a1_proposition94_euler import euler_tail_certificate
from source.h1b2a2_proposition94_distribution import (
    proposition94_distribution_certificate,
)
from source.h1b2a3_proposition94_composition import (
    FMT_THETA,
    H1B2A3_MINIMUM_K,
    fmt_actual_log_r,
    proposition94_actual_composition_certificate,
    proposition94_log_x_sufficient,
    proposition94_strong_smooth_log_r_sufficient,
    uniform_thirteen_rational_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json"
)


class H1b2a3Proposition94CompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_actual_r_formula_and_maynard_range(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            y = mp.mpf(100)
            theta = mp.mpf(FMT_THETA.numerator) / FMT_THETA.denominator
            expected = theta * (y - mp.log(4)) / 3
            log_r = fmt_actual_log_r(y)
            self.assertTrue(mp.almosteq(log_r, expected))
            self.assertGreaterEqual(log_r, theta * y / 10)
            self.assertLessEqual(log_r, theta * y / 3)
        finally:
            mp.mp.dps = old_dps

    def test_default_gate_closes_only_actual_p94_application(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            for k in (36, 100):
                cert = proposition94_actual_composition_certificate(k=k)
                self.assertEqual(cert.log_x, proposition94_log_x_sufficient(k))
                self.assertTrue(cert.maynard_dimension_gate_passed)
                self.assertTrue(cert.actual_r_lower_gate_passed)
                self.assertTrue(cert.actual_r_upper_gate_passed)
                self.assertTrue(cert.selberg_denominator_positive)
                self.assertTrue(cert.smooth_gate_passed)
                self.assertTrue(cert.sharp_gate_passed)
                self.assertTrue(cert.distribution_child_closed)
                self.assertTrue(cert.local_algebra_closed)
                self.assertEqual(cert.final_residue_factor_upper, 1)
                self.assertTrue(cert.composition_bound_verified)
                self.assertTrue(cert.uniform_integer_multiplier_verified)
                self.assertEqual(cert.uniform_integer_multiplier_upper, 13)
                self.assertLess(cert.coarse_total_multiplier_upper, 13)
                self.assertLessEqual(cert.canonical_relative_error_upper, 1)
                self.assertLessEqual(
                    cert.smooth_delta_sum_upper,
                    cert.strong_smooth_delta_target,
                )
                self.assertGreaterEqual(
                    cert.actual_log_r,
                    proposition94_strong_smooth_log_r_sufficient(k),
                )
                self.assertTrue(cert.project_actual_application_lemma_proved)
                self.assertTrue(cert.actual_application_proposition_94_closed)
                self.assertFalse(cert.source_general_proposition_94_closed)
                self.assertFalse(cert.proposition_61_closed)
                self.assertFalse(cert.siv_07_closed)
                self.assertFalse(cert.siv_09_closed)
                self.assertFalse(cert.x_cert_ready)
                self.assertFalse(cert.actual_prime_experiment_performed)
        finally:
            mp.mp.dps = old_dps

    def test_multiplier_is_independently_recomposed(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            k = 36
            cert = proposition94_actual_composition_certificate(k=k)
            smooth = rfold_error_certificate(
                application_id=APPLICATION_L1135_CANONICAL_FACTOR,
                k=k,
                alpha=2,
                theta=FMT_THETA,
                log_r=cert.actual_log_r,
            )
            sharp = fmt_sharp_relative_error_upper(
                k=k,
                alpha=2,
                theta=FMT_THETA,
                log_r=cert.actual_log_r,
            )
            euler = euler_tail_certificate(k)
            distribution = proposition94_distribution_certificate(
                k=k,
                alpha=2,
                theta=FMT_THETA,
                log_x=cert.log_x,
            )
            canonical = mp.mpf(2**k) * smooth.product_error_upper_bound
            main = (
                (1 + sharp)
                / (1 - sharp) ** 2
                * euler.full_line_966_multiplier_upper
                * (1 + canonical)
                * cert.actual_log_r
                / cert.log_x
            )
            rho = mp.exp(distribution.log_relative_error_upper)
            coarse = (
                12
                * euler.full_line_966_multiplier_upper
                * (mp.mpf(FMT_THETA.numerator) / FMT_THETA.denominator)
                / 3
                + 1
            )
            self.assertTrue(mp.almosteq(cert.canonical_relative_error_upper, canonical))
            self.assertTrue(mp.almosteq(cert.main_term_multiplier_upper, main))
            self.assertTrue(mp.almosteq(cert.distribution_relative_error_upper, rho))
            self.assertTrue(mp.almosteq(cert.total_multiplier_upper, main + rho))
            self.assertTrue(mp.almosteq(cert.coarse_total_multiplier_upper, coarse))
            self.assertLessEqual(cert.total_multiplier_upper, coarse)
        finally:
            mp.mp.dps = old_dps

    def test_uniform_thirteen_bound_has_exact_rational_certificate(self) -> None:
        self.assertTrue(uniform_thirteen_rational_certificate())
        self.assertLess(Fraction(49, 18), Fraction(11, 4))
        self.assertLess(Fraction(11, 4) ** 13, Fraction(9) ** 6)

    def test_small_log_x_fails_closed(self) -> None:
        cert = proposition94_actual_composition_certificate(k=36, log_x=10)
        self.assertFalse(cert.maynard_dimension_gate_passed)
        self.assertFalse(cert.smooth_gate_passed)
        self.assertFalse(cert.sharp_gate_passed)
        self.assertFalse(cert.distribution_child_closed)
        self.assertFalse(cert.composition_bound_verified)
        self.assertFalse(cert.uniform_integer_multiplier_verified)
        self.assertFalse(cert.actual_application_proposition_94_closed)
        self.assertIsNone(cert.coarse_total_multiplier_upper)

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            proposition94_actual_composition_certificate(
                k=H1B2A3_MINIMUM_K - 1
            )
        with self.assertRaises(ValueError):
            proposition94_actual_composition_certificate(k=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            fmt_actual_log_r(mp.log(4))
        with self.assertRaises(ValueError):
            proposition94_actual_composition_certificate(k=36, log_x=1)

    def test_contract_sources_dependencies_and_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "ACTUAL_FGKMT_FMT_PROPOSITION94_PARAMETERIZED_EXPLICIT",
        )
        for source in contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )
        for dependency in contract["dependency_contracts"]:
            self.assertTrue((ROOT / dependency).is_file(), dependency)
        states = contract["status_after_this_gate"]
        self.assertEqual(
            states["H1B-P94"],
            "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            states["H1B-P94-ACTUAL-FGKMT-FMT"],
            "ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(states["H1B-P94-GENERAL-A"], "RATE_MISSING")
        self.assertEqual(states["H1B-COMP-01"], "HARD_BLOCKER")
        self.assertEqual(states["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(states["SIV-09"], "HARD_BLOCKER")
        self.assertEqual(states["X_cert"], "OPEN")
        self.assertIn(
            "(11/4)^13<9^6",
            contract["finite_bound"]["exact_final_comparison_certificate"],
        )
        limits = contract["limits"]
        self.assertFalse(limits["general_maynard_proposition_94_proved"])
        self.assertFalse(limits["proposition_61_closed"])
        self.assertFalse(limits["full_good_sieve_weight_closed"])
        self.assertFalse(limits["threshold_calculator_created"])
        self.assertFalse(limits["actual_prime_experiment_performed"])
        self.assertFalse(limits["new_python_dependency_required"])
        self.assertFalse(limits["lean_required_for_this_gate"])
        self.assertIn(
            "NO_DROP_IN_FINITE_REPLACEMENT",
            contract["literature_search"]["result"],
        )
        self.assertIn(
            "not a global nonexistence or novelty claim",
            contract["literature_search"]["limitation"],
        )


if __name__ == "__main__":
    unittest.main()
