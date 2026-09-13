"""Fail-closed checks for the explicit Jutila JL7 shifted-contour multiplier."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_jutila_jl7_contour import (
    NONPRINCIPAL_L_COEFFICIENT_BOUND,
    PRINCIPAL_L_COEFFICIENT_BOUND,
    PRINCIPAL_RATIO_BOUND,
    THETA_MAX,
    build_diagnostic,
    contour_multiplier,
    elementary_contour_multiplier,
    gamma_integral_multiplier,
    height_envelope,
    nonprincipal_vertical_coefficient,
    power_difference_diagnostic,
    principal_rademacher_ratio,
    principal_vertical_coefficient,
    uniform_vertical_multiplier,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_contour_v1.json"
)
PREDECESSOR_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_Jutila_JL7_terminal_v1.json"
)


class DepR09JutilaJL7ContourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(PREDECESSOR_PATH.read_text(encoding="utf-8"))
        mp.mp.dps = 100

    def test_source_hashes_and_sizes_when_audit_copy_present(self):
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if locator is None:
                continue
            path = REPO_ROOT / locator
            if path.is_file():
                data = path.read_bytes()
                self.assertEqual(len(data), source["audit_copy_bytes"], source["key"])
                self.assertEqual(
                    hashlib.sha256(data).hexdigest(),
                    source["audit_copy_sha256"],
                    source["key"],
                )

    def test_peer_reviewed_source_statements_are_pinned(self):
        source_by_key = {item["key"]: item for item in self.ledger["source_registry"]}
        self.assertEqual(
            source_by_key["BENNETT_ET_AL_2021"]["statement"],
            "Lemma 5.6 equation (5.3)",
        )
        self.assertEqual(
            source_by_key["HASANALIZADE_SHEN_WONG_2022"]["statement"],
            "Proposition 3.8",
        )
        self.assertEqual(
            source_by_key["HASANALIZADE_SHEN_WONG_2022"]["doi"],
            "10.1090/mcom/3665",
        )

    def test_vertical_coefficients_fit_proved_rational_envelopes(self):
        self.assertLess(
            nonprincipal_vertical_coefficient(),
            mp.mpf(NONPRINCIPAL_L_COEFFICIENT_BOUND.numerator)
            / NONPRINCIPAL_L_COEFFICIENT_BOUND.denominator,
        )
        self.assertLess(
            principal_vertical_coefficient(),
            mp.mpf(PRINCIPAL_L_COEFFICIENT_BOUND.numerator)
            / PRINCIPAL_L_COEFFICIENT_BOUND.denominator,
        )

    def test_principal_ratio_stays_below_four_thirds(self):
        bound = mp.mpf(PRINCIPAL_RATIO_BOUND.numerator) / PRINCIPAL_RATIO_BOUND.denominator
        for sigma in (mp.mpf("1e-20"), mp.mpf(1) / 21, mp.mpf(1) / 7):
            for height in (0, mp.mpf("0.1"), 1, 100, mp.mpf("1e20")):
                self.assertLessEqual(
                    principal_rademacher_ratio(real_part=sigma, imag_part=height),
                    bound,
                )

    def test_actual_height_envelope(self):
        for theta in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 21)):
            theta_mp = mp.mpf(theta.numerator) / theta.denominator
            for T, u, v, y in (
                (1, 0, -2, 0),
                (10, 2 * theta_mp, 20, -3),
                (mp.mpf("1e9"), theta_mp, mp.mpf("-2e9"), mp.mpf("1e6")),
            ):
                actual, upper = height_envelope(
                    theta=theta,
                    T=T,
                    real_offset=u,
                    base_height=v,
                    contour_height=y,
                )
                self.assertLessEqual(actual, upper)

    def test_power_difference_triangle_bound(self):
        for theta in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 21)):
            for M, N, d, y in (
                (10, 10, 1, 0),
                (10, 1000, 2, 1),
                (mp.mpf("1e20"), mp.mpf("1e50"), mp.mpf("1e4"), -100),
            ):
                actual, upper = power_difference_diagnostic(
                    theta=theta,
                    smoothing_M=M,
                    smoothing_N=N,
                    divisor_d=d,
                    contour_height=y,
                )
                self.assertLessEqual(actual, upper * (1 + mp.mpf("1e-80")))

    def test_contour_multiplier_and_elementary_majorant(self):
        for theta in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 21)):
            theta_mp = mp.mpf(theta.numerator) / theta.denominator
            exact = contour_multiplier(theta)
            elementary = elementary_contour_multiplier(theta)
            elementary_mp = mp.mpf(elementary.numerator) / elementary.denominator
            self.assertTrue(mp.almosteq(
                uniform_vertical_multiplier(theta),
                12 * mp.zeta(1 + theta_mp),
            ))
            self.assertTrue(mp.almosteq(
                gamma_integral_multiplier(theta),
                8 * mp.sqrt(2) * (2 / theta_mp + 1),
            ))
            self.assertLess(exact, elementary_mp)
            self.assertLessEqual(mp.zeta(1 + theta_mp), 1 + 1 / theta_mp)
        self.assertEqual(elementary_contour_multiplier(Fraction(1, 21)), 45408)

    def test_invalid_scopes_fail_closed(self):
        for theta in (Fraction(0), Fraction(1, 20), Fraction(-1, 100)):
            with self.assertRaises(ValueError):
                contour_multiplier(theta)
        with self.assertRaises(ValueError):
            height_envelope(
                theta=THETA_MAX,
                T=1,
                real_offset=0,
                base_height=3,
                contour_height=0,
            )
        with self.assertRaises(ValueError):
            power_difference_diagnostic(
                theta=THETA_MAX,
                smoothing_M=10,
                smoothing_N=9,
                divisor_d=1,
                contour_height=0,
            )

    def test_successor_closes_only_contour_multiplier(self):
        diagnostic = build_diagnostic()
        self.assertFalse(self.predecessor["contour_multiplier_explicit"])
        self.assertTrue(diagnostic.contour_multiplier_explicit)
        self.assertTrue(diagnostic.nonprincipal_coefficient_below_nine_fourths)
        self.assertTrue(diagnostic.principal_coefficient_below_twelve)
        self.assertTrue(diagnostic.zeta_integral_majorant_holds_numerically)
        self.assertTrue(diagnostic.contour_below_elementary_majorant)
        for value in (
            diagnostic.jutila_lemma3_multiplier_explicit,
            diagnostic.residue_well_spacing_multiplier_explicit,
            diagnostic.terminal_density_closed,
            diagnostic.pap_11_closed,
            diagnostic.dep_r09_closed,
            diagnostic.fixed_2e_minus_17_independently_certified,
            diagnostic.threshold_calculator_ready,
            diagnostic.numerical_x_cert_ready,
            diagnostic.actual_prime_computation_run,
            diagnostic.rigorous_interval_certificate,
            diagnostic.source_theorem_local_axiom_used,
            diagnostic.proof_escape_used,
        ):
            self.assertFalse(value)
        self.assertEqual(
            self.ledger["outcome"],
            "JL7_CONTOUR_ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT_REMAINING_TERMINAL_NODES_OPEN",
        )
        self.assertTrue(self.ledger["contour_multiplier_explicit"])
        for key in (
            "jutila_lemma3_multiplier_explicit",
            "residue_well_spacing_multiplier_explicit",
            "terminal_density_closed",
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


if __name__ == "__main__":
    unittest.main()
