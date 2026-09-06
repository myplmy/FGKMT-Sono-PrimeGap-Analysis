"""Validate the H1b-1a explicit cutoff and elementary summation contract."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import mpmath as mp

from source.h1b1a_explicit_package import (
    H1B1A_ANALYTIC_PRIME_PRODUCT_START,
    H1B1A_CUTOFF_SLOPE_BOUND,
    H1B1A_EULER_PRODUCT_COEFFICIENT,
    H1B1A_FINITE_PRIME_PRODUCT_STOP,
    H1B1A_SINGULAR_SERIES_EXPONENT,
    cutoff_psi,
    cutoff_psi_derivative,
    finite_prime_product_certificate,
    log_lower_surrogate,
    smooth_step,
    smooth_step_derivative,
    tail_factor_log_loss_majorant,
    telescoping_square_tail_majorant,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1a_explicit_cutoff_summation_v1.json"
)
H1B1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1_basic_summation_constants_v1.json"
)
H1B_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1b1aExplicitPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_contract_scope_and_sources(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.0.0")
        self.assertEqual(
            self.contract["outcome"],
            "THREE_FINITE_COMPONENTS_CLOSED_"
            "PARAMETERIZED_DIVISOR_MAJORANT_DERIVED",
        )
        self.assertEqual(self.contract["finite_components_closed"], 3)
        self.assertTrue(self.contract["lemma_8_1_i_explicit"])
        self.assertFalse(self.contract["lemma_8_1_ii_common_range_closed"])
        self.assertFalse(self.contract["numerical_basic_summation_package_ready"])
        self.assertFalse(self.contract["siv_07_closed"])
        self.assertFalse(self.contract["numerical_x_cert_ready"])
        self.assertFalse(self.contract["actual_threshold_computed"])
        self.assertFalse(self.contract["new_python_dependency_required"])
        self.assertFalse(self.contract["lean_required_for_this_gate"])

        sources = {row["key"]: row for row in self.contract["source_registry"]}
        self.assertEqual(
            set(sources),
            {
                "MAYNARD2016_PUBLISHED",
                "DUSART2010",
                "ROSSER_SCHOENFELD1962",
            },
        )
        self.assertEqual(
            sources["MAYNARD2016_PUBLISHED"]["sha256"],
            "8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098",
        )
        self.assertEqual(
            sources["DUSART2010"]["sha256"],
            "3f11eca84613ad00e6a447f99b318d5c3d76e360283efcc6d3eebdda25ff3923",
        )
        self.assertEqual(
            sources["ROSSER_SCHOENFELD1962"]["sha256"],
            "8e37b06f82e09421bceb2502578c47b61469141f0287e6acedb70e01765ab556",
        )

    def test_exact_finite_prime_product_branch(self) -> None:
        certificate = finite_prime_product_certificate()
        finite = self.contract["equation_8_5_contract"]["finite_branch"]
        self.assertEqual(certificate.start, 2)
        self.assertEqual(certificate.stop, H1B1A_FINITE_PRIME_PRODUCT_STOP)
        self.assertEqual(certificate.stop, 2_973)
        self.assertEqual(certificate.count, 2_972)
        self.assertEqual(certificate.failures, ())
        self.assertEqual(certificate.maximum_surrogate_ratio_k, 2_971)
        self.assertLess(certificate.maximum_surrogate_ratio, 8)
        self.assertEqual(certificate.rows_sha256, finite["rows_sha256"])
        self.assertEqual(
            H1B1A_ANALYTIC_PRIME_PRODUCT_START,
            H1B1A_FINITE_PRIME_PRODUCT_STOP + 1,
        )
        self.assertEqual(H1B1A_EULER_PRODUCT_COEFFICIENT, 24)

    def test_log_surrogate_and_tail_rational_identities(self) -> None:
        for k in (2, 3, 10, 2_973):
            self.assertGreater(log_lower_surrogate(k), 0)

        for k, p in ((1, 3), (2, 5), (10, 23), (100, 211)):
            loss = tail_factor_log_loss_majorant(k, p)
            self.assertEqual(loss.numerator * p * p, k * k * loss.denominator)
            # The Taylor remainder is k^2/(2p(p-k)); p>2k makes it
            # strictly smaller than k^2/p^2.
            taylor = mp.mpf(k * k) / (2 * p * (p - k))
            self.assertLess(taylor, mp.mpf(loss.numerator) / loss.denominator)

        for k, stop in ((1, 10), (10, 100), (100, 1000)):
            expected = mp.mpf(1) / (2 * k) - mp.mpf(1) / stop
            actual = telescoping_square_tail_majorant(k, stop)
            self.assertEqual(
                mp.mpf(actual.numerator) / actual.denominator,
                expected,
            )
        self.assertEqual(H1B1A_SINGULAR_SERIES_EXPONENT, mp.mpf(9) / 2)

        with self.assertRaises(ValueError):
            tail_factor_log_loss_majorant(2, 4)
        with self.assertRaises(ValueError):
            telescoping_square_tail_majorant(2, 4)

    def test_cutoff_implementation_contract(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            self.assertEqual(cutoff_psi(0), 1)
            self.assertEqual(cutoff_psi(mp.mpf(9) / 10), 1)
            self.assertEqual(cutoff_psi(1), 0)
            self.assertEqual(cutoff_psi(2), 0)
            self.assertEqual(smooth_step(0), 0)
            self.assertEqual(smooth_step(1), 1)

            values = [cutoff_psi(mp.mpf(index) / 1000) for index in range(1001)]
            self.assertTrue(
                all(left >= right for left, right in zip(values, values[1:]))
            )
            self.assertTrue(all(0 <= value <= 1 for value in values))

            for u in (mp.mpf("0.1"), mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.9")):
                numerical = mp.diff(smooth_step, u)
                analytic = smooth_step_derivative(u)
                self.assertTrue(
                    mp.almosteq(
                        numerical,
                        analytic,
                        rel_eps=mp.mpf("1e-70"),
                        abs_eps=mp.mpf("1e-70"),
                    )
                )

            sampled_slopes = [
                abs(cutoff_psi_derivative(mp.mpf(index) / 10_000))
                for index in range(9_000, 10_001)
            ]
            self.assertLess(max(sampled_slopes), H1B1A_CUTOFF_SLOPE_BOUND)
            self.assertEqual(cutoff_psi_derivative(mp.mpf("0.95")), -20)

            with self.assertRaises(ValueError):
                cutoff_psi(-1)
        finally:
            mp.mp.dps = old_dps

    def test_child_updates_without_false_parent_promotion(self) -> None:
        h1b1 = json.loads(H1B1_LEDGER.read_text(encoding="utf-8"))
        by_id = {row["id"]: row for row in h1b1["obligations"]}
        for row_id in (
            "H1B1-L81-SMALL",
            "H1B1-L81-TAIL",
            "H1B1-L82-CUTOFF",
        ):
            self.assertEqual(
                by_id[row_id]["status"],
                "PROJECT_FINITE_COMPONENT_CLOSED",
            )
            self.assertEqual(by_id[row_id]["missing_numeric_inputs"], [])
            self.assertFalse(by_id[row_id]["threshold_ready"])
        self.assertEqual(
            by_id["H1B1-L81II-DIVISOR"]["status"],
            "PARTIAL_EXPLICIT",
        )
        self.assertEqual(by_id["H1B1-PACKAGE"]["status"], "HARD_BLOCKER")

        h1b = json.loads(H1B_LEDGER.read_text(encoding="utf-8"))
        parent_rows = {row["id"]: row for row in h1b["obligations"]}
        self.assertEqual(parent_rows["H1B-L81"]["status"], "RATE_MISSING")
        self.assertEqual(
            parent_rows["H1B-L82"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertFalse(h1b["numerical_x_cert_ready"])

        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        t1_rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(t1_rows["SIV-07"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
