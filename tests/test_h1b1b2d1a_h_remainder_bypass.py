"""Regression tests for the line-905 H square-sum bypass."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2d1a_h_remainder_bypass import (
    CATEGORY_A_SQUARED,
    CATEGORY_A_TIMES_B,
    CATEGORY_B_SQUARED,
    conditional_h_square_bypass_certificate,
    exact_square_bypass_certificate,
    h_square_kappa_families,
    h_square_tensor_families,
)
from source.h1b1b2d_rfold_smooth_package import (
    PROFILE_N2,
    PROFILE_NW,
    PROFILE_W2,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2d1a_H_remainder_bypass_v1.json"
)


class HSquareBypassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_pointwise_square_reduction_for_both_error_signs(self) -> None:
        for z in (Fraction(47, 10), Fraction(53, 10)):
            cert = exact_square_bypass_certificate(
                z=z,
                a=5,
                b=3,
                epsilon=Fraction(1, 10),
            )
            self.assertGreaterEqual(cert.margin, 0)
            self.assertLessEqual(cert.square_error, cert.square_error_upper_bound)

        with self.assertRaisesRegex(ValueError, "do not satisfy"):
            exact_square_bypass_certificate(z=6, a=5, b=3, epsilon="0.1")

    def test_seven_symmetry_classes_have_exact_multiplicities(self) -> None:
        k = 36
        d = k - 1
        rows = h_square_tensor_families(k)
        self.assertEqual(len(rows), 7)
        by_name = {row.name: row for row in rows}
        self.assertEqual(by_name["A2_cutoff"].multiplicity, 1)
        self.assertEqual(by_name["AB_one_NW"].multiplicity, d)
        self.assertEqual(by_name["B2_one_NW"].multiplicity, d)
        self.assertEqual(by_name["B2_one_NW"].integer_coefficient, 2)
        self.assertEqual(by_name["B2_one_W2"].multiplicity, d)
        self.assertEqual(by_name["B2_two_NW"].multiplicity, d * (d - 1) // 2)
        self.assertEqual(by_name["B2_two_NW"].integer_coefficient, 2)
        self.assertEqual(by_name["B2_one_W2"].profiles[0], PROFILE_W2)
        self.assertTrue(by_name["B2_one_W2"].wide_coordinate_first_required)
        self.assertEqual(by_name["AB_one_NW"].profiles.count(PROFILE_NW), 1)
        self.assertEqual(by_name["AB_one_NW"].profiles.count(PROFILE_N2), d - 1)

    def test_symbolic_expansion_matches_direct_A_B_algebra(self) -> None:
        # Positive toy values exercise every diagonal and off-diagonal term.
        n = (mp.mpf("0.7"), mp.mpf("0.5"), mp.mpf("0.3"))
        w = (mp.mpf("0.9"), mp.mpf("0.8"), mp.mpf("0.6"))
        p = mp.mpf("0.4")
        i_n = mp.mpf("0.2")
        i_w = mp.mpf("0.35")
        product_n = mp.fprod(n)
        a = i_n * p * product_n
        wide_sum = mp.fsum(
            w[j] * mp.fprod(n[i] for i in range(3) if i != j)
            for j in range(3)
        )
        b = i_w * product_n + i_n * wide_sum

        product_n2 = mp.fprod(value * value for value in n)
        ab_expanded = i_n * i_w * p * product_n2 + i_n**2 * p * mp.fsum(
            n[j] * w[j] * mp.fprod(n[i] ** 2 for i in range(3) if i != j)
            for j in range(3)
        )
        b2_expanded = i_w**2 * product_n2
        b2_expanded += 2 * i_n * i_w * mp.fsum(
            n[j] * w[j] * mp.fprod(n[i] ** 2 for i in range(3) if i != j)
            for j in range(3)
        )
        b2_expanded += i_n**2 * mp.fsum(
            w[j] ** 2 * mp.fprod(n[i] ** 2 for i in range(3) if i != j)
            for j in range(3)
        )
        b2_expanded += 2 * i_n**2 * mp.fsum(
            n[j] * w[j] * n[l] * w[l]
            * mp.fprod(n[i] ** 2 for i in range(3) if i not in {j, l})
            for j in range(3)
            for l in range(j + 1, 3)
        )
        self.assertAlmostEqual(float(a * b), float(ab_expanded), places=14)
        self.assertAlmostEqual(float(b * b), float(b2_expanded), places=14)

    def test_cutoff_slopes_and_distinct_kappa_families_are_finite(self) -> None:
        a2 = h_square_kappa_families(36, CATEGORY_A_SQUARED)
        ab = h_square_kappa_families(36, CATEGORY_A_TIMES_B)
        b2 = h_square_kappa_families(36, CATEGORY_B_SQUARED)
        self.assertEqual(tuple(map(len, a2)), (35,))
        self.assertEqual(tuple(map(len, ab)), (35, 35))
        self.assertEqual(tuple(map(len, b2)), (35, 35, 35, 35))
        self.assertTrue(all(mp.isfinite(value) and value > 0 for group in a2 + ab + b2 for value in group))
        with self.assertRaises(ValueError):
            h_square_kappa_families(36, "unknown")

    def test_conditional_evaluator_cannot_promote_open_source_multiplier(self) -> None:
        cert = conditional_h_square_bypass_certificate(
            k=36,
            alpha="0.01",
            theta="0.25",
            log_r="1e140",
            scalar_epsilon="0.001",
        )
        self.assertTrue(cert.pointwise_reduction_closed)
        self.assertFalse(cert.functional_h_c1_required)
        self.assertFalse(cert.source_scalar_multiplier_certified)
        self.assertFalse(cert.line_905_closed)
        self.assertFalse(cert.siv_07_closed)
        self.assertFalse(cert.x_cert_ready)
        self.assertTrue(
            mp.almosteq(cert.a_times_b_pointwise_coefficient, mp.mpf("0.002"))
        )
        self.assertTrue(
            mp.almosteq(cert.b_squared_pointwise_coefficient, mp.mpf("0.000001"))
        )
        self.assertGreaterEqual(cert.a_squared_rfold_error_upper, 0)
        self.assertGreaterEqual(cert.a_times_b_rfold_error_upper, 0)
        self.assertGreaterEqual(cert.b_squared_rfold_error_upper, 0)

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            conditional_h_square_bypass_certificate(
                k=35,
                alpha="0.01",
                theta="0.25",
                log_r="1e140",
                scalar_epsilon="0.1",
            )
        with self.assertRaisesRegex(ValueError, "too small"):
            conditional_h_square_bypass_certificate(
                k=36,
                alpha="0.01",
                theta="0.25",
                log_r="1",
                scalar_epsilon="0.1",
            )
        with self.assertRaises(ValueError):
            exact_square_bypass_certificate(z=1, a=-1, b=1, epsilon=1)

    def test_contract_source_hashes_and_parent_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "FUNCTIONAL_C1_BYPASSED_SCALAR_POINTWISE_MULTIPLIER_OPEN",
        )
        self.assertTrue(contract["project_lemma"]["pointwise_square_reduction_closed"])
        self.assertFalse(contract["project_lemma"]["functional_H_C1_required"])
        self.assertFalse(contract["source_scalar_remainder"]["numerical_multiplier_closed"])
        self.assertFalse(contract["line_905_closed"])
        self.assertFalse(contract["siv_07_closed"])
        self.assertFalse(contract["numerical_x_cert_ready"])
        self.assertFalse(contract["actual_prime_experiment_performed"])
        self.assertFalse(contract["new_python_dependency_required"])
        self.assertFalse(contract["lean_required_for_this_gate"])
        for source in contract["source_registry"]:
            if "local_path" not in source:
                continue
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source["sha256"])
        parent = contract["parent_status"]
        self.assertEqual(parent["H1B-L84"], "RATE_MISSING")
        self.assertEqual(parent["H1B1-PACKAGE"], "HARD_BLOCKER")
        self.assertEqual(parent["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(parent["X_cert"], "OPEN")


if __name__ == "__main__":
    unittest.main()
