"""Regression tests for the fail-closed H1b-1b-2b contract."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2b_corrected_wirsing import (
    H1B1B2B_FINITE_X_MINIMUM,
    H1B1B2B_INTERVAL_LOG_WEIGHTED_DEVIATION_BASE,
    H1B1B2B_INV_LN2_UPPER_BOUND,
    H1B1B2B_LN2_LOWER_BOUND,
    H1B1B2B_MERTENS_PRODUCT_MULTIPLIER,
    H1B1B2B_PRIME_RECIPROCAL_DEVIATION_BOUND,
    H1B1B2B_PRIME_WEIGHTED_DEVIATION_BOUND,
    H1B1B2B_SUMMATORY_PREFACTOR,
    H1B1B2B_TAIL_EXPONENT_BASE,
    corrected_kappa1_wirsing_certificate,
    summatory_log_multiplier,
    summatory_multiplier,
    weighted_lemma83_multiplier,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier_v1.json"
)


class CorrectedKappa1WirsingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_parameter_mapping_and_formula_parts(self) -> None:
        certificate = corrected_kappa1_wirsing_certificate(
            Fraction(1, 2), Fraction(2)
        )
        self.assertEqual(certificate.maynard_a1_gap, Fraction(1, 2))
        self.assertEqual(certificate.ggpy_a1_cap, 2)
        self.assertEqual(certificate.a2, 2)
        expected_tail = Fraction(2, 1) / Fraction(1, 2) * (
            1 + Fraction(100, 69) * 2
        ) + 2 * Fraction(1, 2) ** 2 / Fraction(1, 2)
        self.assertEqual(certificate.local_recurrence_tail_bound, expected_tail)
        self.assertEqual(certificate.delta_multiplier, 6 + expected_tail)
        self.assertEqual(certificate.tail_exponent, 258)
        self.assertEqual(certificate.summatory_prefactor, 40960)
        self.assertEqual(certificate.finite_x_minimum, 2)
        self.assertEqual(certificate.error_scale, "c_gamma * (L+1)")
        self.assertTrue(certificate.error_contains_c_gamma)
        self.assertTrue(certificate.corrected_extra_term_included)
        self.assertFalse(certificate.c_gamma_lower_bound_required)

    def test_fixed_global_majorants_are_fail_closed(self) -> None:
        self.assertEqual(H1B1B2B_LN2_LOWER_BOUND, Fraction(69, 100))
        self.assertEqual(H1B1B2B_INV_LN2_UPPER_BOUND, Fraction(100, 69))
        self.assertEqual(H1B1B2B_PRIME_WEIGHTED_DEVIATION_BOUND, 64)
        self.assertEqual(H1B1B2B_PRIME_RECIPROCAL_DEVIATION_BOUND, 16)
        self.assertEqual(H1B1B2B_MERTENS_PRODUCT_MULTIPLIER, 8192)
        self.assertEqual(H1B1B2B_INTERVAL_LOG_WEIGHTED_DEVIATION_BASE, 130)
        self.assertEqual(H1B1B2B_TAIL_EXPONENT_BASE, 256)
        self.assertEqual(H1B1B2B_SUMMATORY_PREFACTOR, 40960)
        self.assertEqual(H1B1B2B_FINITE_X_MINIMUM, 2)

    def test_multiplier_evaluation_and_monotonic_safety(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            baseline_log = summatory_log_multiplier(Fraction(1, 2), 2)
            baseline = summatory_multiplier(Fraction(1, 2), 2)
            weighted = weighted_lemma83_multiplier(Fraction(1, 2), 2)
            self.assertTrue(mp.isfinite(baseline_log))
            self.assertTrue(mp.isfinite(baseline))
            self.assertGreater(baseline, 0)
            self.assertEqual(weighted, 2 * (baseline + 2))
            self.assertGreater(
                summatory_log_multiplier(Fraction(1, 4), 2), baseline_log
            )
            self.assertGreater(summatory_log_multiplier(Fraction(1, 2), 3), baseline_log)
        finally:
            mp.mp.dps = old_dps

    def test_invalid_or_ambiguous_parameters_are_rejected(self) -> None:
        for value in (0, -1, True):
            with self.assertRaises(ValueError):
                corrected_kappa1_wirsing_certificate(value, 1)
        with self.assertRaises(ValueError):
            corrected_kappa1_wirsing_certificate(Fraction(3, 2), 1)
        for value in (0, -1, False):
            with self.assertRaises(ValueError):
                corrected_kappa1_wirsing_certificate(Fraction(1, 2), value)

    def test_contract_provenance_and_parent_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "CORRECTED_KAPPA1_RELATIVE_BASE_RATE_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(contract["finite_x_minimum"], 2)
        self.assertTrue(contract["corrected_extra_term_included"])
        self.assertFalse(contract["legacy_absolute_c3_required_on_primary_route"])
        self.assertFalse(contract["actual_a1_a2_l_instantiated"])
        self.assertFalse(contract["r_fold_composition_closed"])
        self.assertFalse(contract["siv_07_closed"])
        self.assertFalse(contract["numerical_x_cert_ready"])
        self.assertFalse(contract["actual_threshold_computed"])
        self.assertFalse(contract["new_python_dependency_required"])
        self.assertFalse(contract["lean_required_for_this_gate"])

        sources = {row["key"]: row for row in contract["source_registry"]}
        self.assertEqual(set(sources), {"FORD2023_NOTES", "DUSART2010"})
        for source in sources.values():
            path = ROOT / source["local_path"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, source["sha256"])

        parent = contract["parent_status"]
        self.assertEqual(parent["H1B-L83"], "PARAMETERIZED_EXPLICIT_INPUTS_OPEN")
        self.assertEqual(parent["H1B-L84"], "RATE_MISSING")
        self.assertEqual(parent["H1B1-PACKAGE"], "HARD_BLOCKER")
        self.assertEqual(parent["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(parent["X_cert"], "OPEN")


if __name__ == "__main__":
    unittest.main()
