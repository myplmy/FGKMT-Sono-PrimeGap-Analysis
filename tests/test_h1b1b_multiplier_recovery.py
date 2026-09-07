"""Validate the fail-closed H1b-1b multiplier-recovery contract."""

from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b_multiplier_recovery import (
    H1B1B_GGPY4_KAPPA1_TRANSFER_FACTOR,
    H1B1B_LEMMA82_MULTIPLIER,
    H1B1B_NORMALIZED_LIPSCHITZ_UPPER_BOUND,
    H1B1B_PRINTED_C_GAMMA_ERROR_JUSTIFIED_BY_STATED_HYPOTHESES,
    ggpy4_kappa1_relative_transfer_certificate,
    ggpy4_kappa1_transfer_certificate,
    lemma82_normalized_multiplier,
    lemma82_one_coordinate_margin,
    lemma82_uniform_certificate,
    maynard_f,
    maynard_f2,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_v1.json"
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


class H1b1bMultiplierRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_contract_provenance_and_scope(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.1.0")
        self.assertEqual(
            self.contract["outcome"],
            "LEMMA82_EXPLICIT_GGPY4_ABSOLUTE_TRANSFER_APPLICATION_"
            "EXCLUSIONS_CLOSED_BASE_RATE_OPEN",
        )
        self.assertEqual(
            self.contract["h1b1b2a_ledger"],
            "docs/method/theory/data/"
            "Sono_FMT_H1b1b2a_actual_local_factor_lower_bound_v1.json",
        )
        self.assertTrue(self.contract["lemma_8_2_project_component_closed"])
        self.assertEqual(self.contract["lemma_8_2_uniform_multiplier"], 89)
        self.assertTrue(self.contract["ggpy_lemma_4_transfer_factor_closed"])
        self.assertTrue(
            self.contract["ggpy_lemma_4_absolute_transfer_factor_closed"]
        )
        self.assertFalse(
            self.contract[
                "ggpy_maynard_relative_error_valid_under_printed_hypotheses"
            ]
        )
        self.assertTrue(self.contract["castillo_absolute_error_shape_reviewed"])
        self.assertTrue(self.contract["kuperberg_structural_reproduction_reviewed"])
        self.assertFalse(self.contract["ggpy_lemma_3_numeric_multiplier_recovered"])
        self.assertFalse(
            self.contract["hr_lemmas_5_3_5_4_numeric_multiplier_recovered"]
        )
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
                "MAYNARD2016_ARXIV_SOURCE",
                "GGPY2009_ARXIV_V1",
                "GGPY2009_ARXIV_SOURCE",
                "GGPY2013_CORRIGENDUM",
                "HR1974_2011_REPRINT",
                "KUPERBERG2023",
                "KUPERBERG2023_ARXIV_SOURCE",
                "CASTILLO_ET_AL_2015",
                "CASTILLO_ET_AL_ARXIV_SOURCE",
            },
        )
        self.assertEqual(
            sources["MAYNARD2016_PUBLISHED"]["sha256"],
            "8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098",
        )
        self.assertEqual(
            sources["GGPY2009_ARXIV_V1"]["sha256"],
            "411a638e959e6fa41d9f489477b26a8abe6550f3a61e5f2058ccdc88a6461680",
        )
        self.assertEqual(
            sources["GGPY2009_ARXIV_SOURCE"]["extracted_sha256"],
            "e58cc895e8b44f6369741f184bd81b595ed177463cf09cee8d0ad74558efce45",
        )
        self.assertEqual(
            sources["HR1974_2011_REPRINT"]["status"],
            "SOURCE_ACCESS_BLOCKED",
        )
        self.assertEqual(
            sources["KUPERBERG2023"]["sha256"],
            "653dcd731f11c6bab47fa61989b31f50dc3318464fc4d300276698045ba48939",
        )
        self.assertEqual(
            sources["CASTILLO_ET_AL_2015"]["sha256"],
            "af2f402f1d0ecf67ea2b02a18f9cc2384514cb04fc3467807e20b278e3d463ca",
        )

    def test_exact_uniform_multiplier_certificate(self) -> None:
        certificate = lemma82_uniform_certificate()
        self.assertEqual(certificate.k_minimum, 2)
        self.assertEqual(certificate.cutoff_slope_bound, 50)
        self.assertEqual(certificate.ln2_lower_bound, Fraction(69, 100))
        self.assertEqual(
            certificate.inverse_sqrt2_upper_bound,
            Fraction(71, 100),
        )
        self.assertEqual(
            certificate.normalized_multiplier_upper_bound,
            H1B1B_NORMALIZED_LIPSCHITZ_UPPER_BOUND,
        )
        self.assertEqual(
            certificate.normalized_multiplier_upper_bound,
            Fraction(6119, 69),
        )
        self.assertLess(
            certificate.normalized_multiplier_upper_bound,
            H1B1B_LEMMA82_MULTIPLIER,
        )

        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in (2, 3, 4, 10, 36, 1_000, 1_000_000):
                self.assertLess(lemma82_normalized_multiplier(k), 89)
        finally:
            mp.mp.dps = old_dps

        with self.assertRaises(ValueError):
            lemma82_normalized_multiplier(1)

    def test_numeric_one_coordinate_regression_grid(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in (2, 3, 8):
                base = [mp.mpf("0.01")] * k
                for coordinate in (0, k - 1):
                    for delta in (
                        mp.mpf(0),
                        mp.mpf("1e-12"),
                        mp.mpf("0.001"),
                        mp.mpf("0.05"),
                        mp.mpf("0.5"),
                        mp.mpf("1.1"),
                    ):
                        self.assertGreaterEqual(
                            lemma82_one_coordinate_margin(
                                base,
                                coordinate,
                                delta,
                            ),
                            -mp.mpf("1e-70"),
                        )
                self.assertGreaterEqual(maynard_f2(base), maynard_f(base))

                outside = base.copy()
                outside[0] = 1 / mp.sqrt(k)
                self.assertEqual(maynard_f(outside), 0)
                self.assertGreaterEqual(
                    lemma82_one_coordinate_margin(outside, 0, mp.mpf("0.1")),
                    0,
                )
        finally:
            mp.mp.dps = old_dps

        with self.assertRaises(ValueError):
            lemma82_one_coordinate_margin([0, 0], 2, 1)
        with self.assertRaises(ValueError):
            lemma82_one_coordinate_margin([0, 0], 0, -1)

    def test_ggpy_kappa1_transfer_is_conditional(self) -> None:
        certificate = ggpy4_kappa1_transfer_certificate(Fraction(7, 3))
        self.assertEqual(certificate.lemma3_absolute_multiplier, Fraction(7, 3))
        self.assertFalse(certificate.assumed_error_contains_c_gamma)
        self.assertEqual(certificate.boundary_factor, 1)
        self.assertEqual(certificate.derivative_integral_factor, 1)
        self.assertEqual(H1B1B_GGPY4_KAPPA1_TRANSFER_FACTOR, 2)
        self.assertEqual(certificate.lemma4_absolute_multiplier, Fraction(14, 3))
        self.assertFalse(
            H1B1B_PRINTED_C_GAMMA_ERROR_JUSTIFIED_BY_STATED_HYPOTHESES
        )
        self.assertIn(
            "C3(A1,A2)",
            self.contract["ggpy_kappa_1_transfer_contract"][
                "assumed_lemma_3_error"
            ],
        )
        self.assertNotIn(
            "C3(A1,A2) c_gamma",
            self.contract["ggpy_kappa_1_transfer_contract"][
                "assumed_lemma_3_error"
            ],
        )
        self.assertEqual(
            self.contract["ggpy_kappa_1_transfer_contract"][
                "proof_status"
            ],
            "PARAMETERIZED_EXPLICIT",
        )
        self.assertIn(
            "6 C3(A1,A2)(1+log Lambda_star)",
            self.contract["ggpy_kappa_1_transfer_contract"][
                "relative_error_recovery"
            ],
        )
        with self.assertRaises(ValueError):
            ggpy4_kappa1_transfer_certificate(0)

    def test_relative_transfer_requires_separate_positive_c_gamma_bound(self) -> None:
        certificate = ggpy4_kappa1_relative_transfer_certificate(
            Fraction(7, 3), Fraction(1, 5)
        )
        self.assertEqual(certificate.lemma4_absolute_multiplier, Fraction(14, 3))
        self.assertEqual(certificate.c_gamma_lower_bound, Fraction(1, 5))
        self.assertEqual(certificate.lemma4_relative_multiplier, Fraction(70, 3))
        with self.assertRaises(ValueError):
            ggpy4_kappa1_relative_transfer_certificate(1, 0)

    def test_child_closure_does_not_promote_parent_package(self) -> None:
        h1b1 = json.loads(H1B1_LEDGER.read_text(encoding="utf-8"))
        h1b1_rows = {row["id"]: row for row in h1b1["obligations"]}
        self.assertEqual(
            h1b1_rows["H1B1-L82-LIPSCHITZ"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertEqual(
            h1b1_rows["H1B1-L82-LIPSCHITZ"]["missing_numeric_inputs"],
            [],
        )
        self.assertEqual(
            h1b1_rows["H1B1-L83-GGPY4"]["status"],
            "PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(
            h1b1_rows["H1B1-L83-GGPY3"]["status"],
            "RATE_MISSING",
        )
        self.assertEqual(h1b1_rows["H1B1-PACKAGE"]["status"], "HARD_BLOCKER")

        h1b = json.loads(H1B_LEDGER.read_text(encoding="utf-8"))
        h1b_rows = {row["id"]: row for row in h1b["obligations"]}
        self.assertEqual(
            h1b_rows["H1B-L82"]["status"],
            "PROJECT_FINITE_COMPONENT_CLOSED",
        )
        self.assertEqual(h1b_rows["H1B-L82"]["missing_numeric_inputs"], [])
        self.assertEqual(h1b_rows["H1B-L83"]["status"], "RATE_MISSING")
        self.assertEqual(h1b_rows["H1B-COMP-01"]["status"], "HARD_BLOCKER")
        self.assertFalse(h1b["numerical_x_cert_ready"])

        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        t1_rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(t1_rows["SIV-07"]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
