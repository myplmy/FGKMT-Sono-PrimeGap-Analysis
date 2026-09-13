"""Fail-closed tests for the DEP-R09 modern density-source screen."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.dep_r09_modern_density_screen import (
    D_CAPACITY_ENDPOINT,
    FI_LINNIK_EXPONENT,
    FI_POWER_EXPONENT,
    FI_SMOOTHED_COEFFICIENT,
    ZERO_FREE_C1,
    build_diagnostic,
    fi_linnik_factorization,
    pap_zero_free_edge_mass,
    ramare_additive_growth_exponent,
    ramare_direct_slice_lower,
    ramare_power_margin,
    ramare_source_range_log_x,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_modern_density_source_screen_v1.json"
)


class DepR09ModernDensityScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_d186_transformed_exponents_are_exact(self):
        self.assertEqual(D_CAPACITY_ENDPOINT, 186)
        self.assertEqual(ZERO_FREE_C1, Fraction(1, 24))
        self.assertEqual(ramare_power_margin(), Fraction(83, 93))
        self.assertEqual(ramare_additive_growth_exponent(), Fraction(1, 93))
        self.assertEqual(pap_zero_free_edge_mass(), Fraction(31, 20))

    def test_ramare_direct_slice_certificate_misses_budget_at_source_gate(self):
        with mp.workdps(100):
            minimum = ramare_source_range_log_x()
            self.assertLess(abs(minimum - 186 * mp.log(10)), mp.mpf("1e-90"))
            main_lower, additive_lower = ramare_direct_slice_lower(minimum)
            self.assertGreater(main_lower, mp.mpf("8602"))
            self.assertGreater(additive_lower, mp.mpf("64912"))
            self.assertGreater(main_lower + additive_lower, mp.exp(-2))

    def test_ramare_direct_certificate_floor_grows_with_log_x(self):
        with mp.workdps(80):
            points = [ramare_source_range_log_x(), mp.mpf(1000), mp.mpf(10000)]
            values = [ramare_direct_slice_lower(point) for point in points]
            for before, after in zip(values, values[1:]):
                self.assertGreater(after[0], before[0])
                self.assertGreater(after[1], before[1])

    def test_friedlander_iwaniec_route_is_outside_current_gate(self):
        self.assertEqual(fi_linnik_factorization(), FI_LINNIK_EXPONENT)
        self.assertEqual(FI_LINNIK_EXPONENT, 75_744_000)
        self.assertGreater(FI_POWER_EXPONENT, D_CAPACITY_ENDPOINT)
        self.assertLess(FI_SMOOTHED_COEFFICIENT, Fraction(4, 5))

    def test_diagnostic_is_fail_closed(self):
        diagnostic = build_diagnostic()
        self.assertTrue(diagnostic.thorner_zaman_near_exponent_99_within_d_gate)
        self.assertTrue(
            diagnostic.thorner_zaman_exceptional_removed_exponent_170_within_d_gate
        )
        self.assertFalse(
            diagnostic.thorner_zaman_all_sigma_exceptional_exponent_198_within_d_gate
        )
        self.assertFalse(diagnostic.bin_chen_asymptotic_factor_numerical)
        self.assertFalse(diagnostic.ramare_direct_certificate_below_exp_minus_2)
        self.assertFalse(diagnostic.public_numerical_drop_in_found)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.fixed_2e_minus_17_independently_certified)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.threshold_calculator_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_machine_ledger_preserves_publication_and_scope_boundaries(self):
        self.assertEqual(
            self.ledger["outcome"],
            "NO_IDENTIFIED_NUMERICAL_DROP_IN_AMONG_SCREENED_PUBLIC_CANDIDATES_PASSES_D_LE_186_PAP_GATE",
        )
        statuses = self.ledger["status_after_this_gate"]
        self.assertTrue(statuses["named_modern_candidate_set_screened"])
        self.assertFalse(statuses["all_possible_literature_exhaustively_ruled_out"])
        self.assertFalse(statuses["current_public_numerical_drop_in_found"])
        self.assertFalse(statuses["unverified_asymptotic_exponent_promoted"])
        self.assertFalse(statuses["in_preparation_result_promoted"])
        self.assertFalse(statuses["user_compute_required_now"])

        by_key = {row["key"]: row for row in self.ledger["source_registry"]}
        self.assertIn("UNVERIFIED_ARXIV_PREPRINT", by_key["CHEN_GUPTA_LI_2026_DENSITY"]["publication_status"])
        self.assertIn("IN_PREPARATION", by_key["BELLOTTI_CASTILLO_DIRICHLET_LOG_FREE_IN_PREPARATION"]["publication_status"])
        self.assertEqual(
            by_key["BELLOTTI_CASTILLO_DIRICHLET_LOG_FREE_IN_PREPARATION"]["author"],
            "Chiara Bellotti and Cruz Castillo",
        )

    def test_audit_copy_hashes_match_when_local_copies_exist(self):
        checked = 0
        for source in self.ledger["source_registry"]:
            locator = source.get("audit_copy_locator")
            if not locator:
                continue
            path = REPO_ROOT / locator
            if not path.is_file():
                continue
            payload = path.read_bytes()
            self.assertEqual(len(payload), source["audit_copy_bytes"], source["key"])
            self.assertEqual(
                hashlib.sha256(payload).hexdigest(),
                source["audit_copy_sha256"],
                source["key"],
            )
            checked += 1
        self.assertGreaterEqual(checked, 4)

    def test_invalid_inputs_fail_closed(self):
        for bad_d in (20, 0, -1):
            with self.subTest(d=bad_d):
                with self.assertRaises(ValueError):
                    ramare_power_margin(bad_d)
        with self.assertRaises(TypeError):
            ramare_power_margin(186.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pap_zero_free_edge_mass(c1=1 / 24)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pap_zero_free_edge_mass(c1=Fraction(0))
        with self.assertRaises(ValueError):
            ramare_direct_slice_lower(ramare_source_range_log_x() - 1)
        for bad_log_x in (0, -1, mp.inf, mp.nan):
            with self.subTest(log_x=bad_log_x):
                with self.assertRaises(ValueError):
                    ramare_direct_slice_lower(bad_log_x)


if __name__ == "__main__":
    unittest.main()
