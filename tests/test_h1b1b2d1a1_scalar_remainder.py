"""Regression tests for the H1b-1b-2d.1a.1 scalar remainder package."""

from __future__ import annotations

import hashlib
import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2d1a1_scalar_remainder import (
    H1B1B2D1A1_PREFACTOR_RESIDUAL_BOUND,
    H1B1B2D1A1_T_DIVISOR_LOGLOG_SQUARED_BOUND,
    H1B1B2D1A1_YM_ERROR_COEFFICIENT,
    H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT,
    certified_line905_scalar_certificate,
    direct_profile_envelope_certificate,
    exact_prefactor_cancellation,
    scalar_remainder_constant_certificate,
    scalar_remainder_gate_certificate,
    t_divisor_coefficient_chain,
    t_divisor_log_linear_form,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2d1a1_scalar_remainder_v1.json"
)


def _independent_t_divisor_form(
    pairs: tuple[tuple[int, int], ...],
) -> tuple[Fraction, dict[int, Fraction]]:
    """Enumerate every square-free divisor as an independent exact oracle."""

    constant = Fraction(0)
    coefficients = {prime: Fraction(0) for prime, _ in pairs}
    for subset_size in range(len(pairs) + 1):
        for subset in itertools.combinations(pairs, subset_size):
            weight = Fraction(1)
            for prime, root_count in subset:
                weight /= prime - root_count
            constant += weight
            for prime, _ in subset:
                coefficients[prime] += weight
    return constant, coefficients


class ScalarRemainderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_ym_coefficient_and_common_constant(self) -> None:
        self.assertEqual(H1B1B2D1A1_PREFACTOR_RESIDUAL_BOUND, Fraction(36, 35))
        self.assertEqual(
            H1B1B2D1A1_YM_ERROR_COEFFICIENT_EXACT,
            Fraction(355028832, 35),
        )
        self.assertEqual(H1B1B2D1A1_YM_ERROR_COEFFICIENT, 10143681)

        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            certificate = scalar_remainder_constant_certificate()
            expected = (
                mp.mpf(327680) * mp.mpf(14801) / 69 * mp.exp(264)
                + 10143697
            )
            # The inherited multiplier is evaluated through exp(log(C_sum));
            # allow only the resulting high-precision roundoff, not a changed
            # symbolic coefficient.
            self.assertTrue(
                mp.almosteq(
                    certificate.common_c_y,
                    expected,
                    rel_eps=mp.mpf("1e-75"),
                )
            )
            self.assertGreater(certificate.common_c_y, mp.mpf("3.16e122"))
            self.assertLess(certificate.common_c_y, mp.mpf("3.17e122"))
        finally:
            mp.mp.dps = old_dps

    def test_exact_prefactor_cancellation_including_shared_a_r_factor(self) -> None:
        self.assertEqual(exact_prefactor_cancellation(6, 35, 6), 1)
        self.assertEqual(exact_prefactor_cancellation(30, 77, 30 * 13), 1)
        with self.assertRaisesRegex(ValueError, "gcd"):
            exact_prefactor_cancellation(6, 35, 5)

    def test_t_divisor_identity_matches_independent_subset_enumeration(self) -> None:
        pairs = ((2593, 3), (2609, 5), (2621, 7))
        certificate = t_divisor_log_linear_form(pairs)
        expected_constant, expected_coefficients = _independent_t_divisor_form(pairs)
        self.assertEqual(certificate.constant, expected_constant)
        self.assertEqual(dict(certificate.log_coefficients), expected_coefficients)

        empty = t_divisor_log_linear_form(())
        self.assertEqual(empty.constant, 1)
        self.assertEqual(empty.log_coefficients, ())
        with self.assertRaises(ValueError):
            t_divisor_log_linear_form(((2593, 3), (2593, 4)))

    def test_t_divisor_coefficient_is_strictly_below_nineteen(self) -> None:
        coefficient = t_divisor_coefficient_chain()
        self.assertEqual(coefficient, Fraction(64467, 3500))
        self.assertLess(
            coefficient,
            H1B1B2D1A1_T_DIVISOR_LOGLOG_SQUARED_BOUND,
        )

    def test_direct_profile_envelope_holds_in_target_range_samples(self) -> None:
        for k in (36, 37, 100, 1000, 10000):
            certificate = direct_profile_envelope_certificate(k)
            self.assertTrue(certificate.half_integral_gate_passed)
            self.assertTrue(certificate.derivative_gate_passed)
            self.assertGreaterEqual(
                certificate.b_over_outer_product_lower_bound,
                mp.mpf("0.5"),
            )
            self.assertLessEqual(
                certificate.scaled_gmax_over_outer_product_upper_bound,
                certificate.t_k,
            )
        with self.assertRaises(ValueError):
            direct_profile_envelope_certificate(35)

    def test_parameterized_finite_gate_closes_only_scalar_subpackage(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k, alpha, theta in (
                (36, "0.01", "0.25"),
                (100, "0.02", "0.4"),
            ):
                gate = scalar_remainder_gate_certificate(
                    k=k,
                    alpha=alpha,
                    theta=theta,
                )
                self.assertTrue(gate.gate_verified)
                self.assertTrue(gate.determinant_absorption_verified)
                self.assertTrue(gate.discrepancy_absorption_verified)
                self.assertTrue(gate.l995_upper_factor_verified)
                self.assertTrue(gate.square_bypass_linearization_verified)
                self.assertTrue(gate.source_scalar_multiplier_certified)
                self.assertTrue(gate.line_905_subpackage_closed)
                self.assertFalse(gate.h1b_l84_closed)
                self.assertFalse(gate.siv_07_closed)
                self.assertFalse(gate.x_cert_ready)

                combined = certified_line905_scalar_certificate(
                    k=k,
                    alpha=alpha,
                    theta=theta,
                    log_r=gate.log_r_sufficient,
                )
                self.assertGreater(combined.scalar_epsilon_upper_bound, 0)
                self.assertLessEqual(combined.square_bypass_delta_sum_upper_bound, 1)
                self.assertTrue(combined.source_scalar_multiplier_certified)
                self.assertTrue(combined.line_905_scalar_subpackage_closed)
                self.assertFalse(combined.h1b_l84_closed)
                self.assertFalse(combined.siv_07_closed)
                self.assertFalse(combined.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_invalid_gate_inputs_fail_closed(self) -> None:
        for kwargs in (
            {"k": 35, "alpha": "0.01", "theta": "0.25"},
            {"k": 36, "alpha": 0, "theta": "0.25"},
            {"k": 36, "alpha": "0.01", "theta": 1},
        ):
            with self.assertRaises(ValueError):
                scalar_remainder_gate_certificate(**kwargs)
        gate = scalar_remainder_gate_certificate(
            k=36,
            alpha="0.01",
            theta="0.25",
        )
        with self.assertRaisesRegex(ValueError, "below"):
            certified_line905_scalar_certificate(
                k=36,
                alpha="0.01",
                theta="0.25",
                log_r=gate.log_r_sufficient / 2,
            )

    def test_contract_provenance_and_parent_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "SCALAR_REMAINDER_PARAMETERIZED_EXPLICIT_PARENT_RATE_MISSING",
        )
        self.assertTrue(contract["scalar_remainder"]["source_multiplier_closed"])
        self.assertEqual(
            contract["scalar_remainder"]["ym_error_integer_multiplier"],
            H1B1B2D1A1_YM_ERROR_COEFFICIENT,
        )
        self.assertFalse(contract["parent_status"]["H1B-L84_closed"])
        self.assertFalse(contract["parent_status"]["SIV-07_closed"])
        self.assertFalse(contract["parent_status"]["X_cert_ready"])
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["new_python_dependency_required"])
        self.assertFalse(contract["lean_required_for_this_gate"])
        for source in contract["source_registry"]:
            if "local_path" not in source:
                continue
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
