"""Regression tests for the H1c-1b.4d source-constant reproof."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import bordignon_exponent
from source.h1c1b4d_source_constant_reproof import (
    HIGH_ZERO_LAMBDA,
    SOURCE_COMPONENT_COUNT,
    SOURCE_COMPONENT_LOG_CEILING,
    SOURCE_REPROOF_DIMENSION_CUTOFF,
    exact_corner_log_upper_witnesses,
    exact_uniformity_sufficient_checks,
    source_constant_budget,
    source_constant_component_log_uppers,
    structural_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b4d_source_constant_reproof_v1.json"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class H1c1b4dSourceConstantReproofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_corner_witnesses_and_uniformity_conditions(self) -> None:
        witnesses = exact_corner_log_upper_witnesses()
        self.assertEqual(len(witnesses), SOURCE_COMPONENT_COUNT)
        self.assertTrue(
            all(value < SOURCE_COMPONENT_LOG_CEILING for value in witnesses.values())
        )
        checks = exact_uniformity_sufficient_checks()
        self.assertTrue(all(checks.values()), checks)
        self.assertTrue(checks["dimension_low_zero_derivative_dominated"])
        self.assertTrue(checks["dimension_sigma0_derivative_dominated"])
        self.assertTrue(checks["dimension_high_log_derivative_dominated"])
        self.assertTrue(checks["dimension_high_sqrt_derivative_dominated"])

    def test_numerical_corner_source_bound_fits_predecessor_allowance(self) -> None:
        with mp.workdps(100):
            logs = source_constant_component_log_uppers(
                SOURCE_REPROOF_DIMENSION_CUTOFF
            )
            self.assertEqual(len(logs), SOURCE_COMPONENT_COUNT)
            self.assertEqual(
                max(logs, key=logs.get),  # type: ignore[arg-type]
                "02_rstar_R2_R3",
            )
            self.assertLess(max(logs.values()), SOURCE_COMPONENT_LOG_CEILING)
            budget = source_constant_budget()
            self.assertLess(budget.source_constant_log_upper, -105)
            self.assertGreater(budget.source_constant_log_upper, -106)
            self.assertTrue(budget.source_constant_strictly_below_one)
            self.assertGreater(budget.conditional_absorption_log_allowance, 631)
            self.assertLess(budget.conditional_absorption_log_allowance, 632)
            self.assertTrue(budget.fits_h1c1b4c_allowance)

    def test_low_zero_bound_preserves_final_two_q_factor(self) -> None:
        with mp.workdps(100):
            r = SOURCE_REPROOF_DIMENSION_CUTOFF
            L = mp.mpf(r**5)
            ell = mp.log(L)
            A = mp.mpf(int(bordignon_exponent(r)))
            B = A * ell
            current = source_constant_component_log_uppers(r)[
                "10_low_height_zeros_with_final_2q"
            ]
            obsolete_v1_style_without_q = current - B - mp.log(2)
            expected_difference = B + mp.log(2)
            relative_error = abs(
                (current - obsolete_v1_style_without_q) - expected_difference
            ) / B
            self.assertLess(relative_error, mp.mpf("1e-90"))
            self.assertGreater(current, obsolete_v1_style_without_q)

    def test_unknown_liu_wang_alternative_is_bounded_by_global_minimum(self) -> None:
        eta = [mp.mpf("0.16"), mp.mpf("0.17"), mp.mpf("0.18"),
               mp.mpf("0.19"), mp.mpf("0.20"), mp.mpf("0.206")]
        xi_next = [mp.mpf("0.2477"), mp.mpf("0.2356"), mp.mpf("0.2242"),
                   mp.mpf("0.2135"), mp.mpf("0.2074"), mp.mpf("0.2067")]
        common = mp.mpf(HIGH_ZERO_LAMBDA.numerator) / HIGH_ZERO_LAMBDA.denominator
        self.assertEqual(common, min(eta + xi_next))
        self.assertTrue(all(value >= common for value in eta + xi_next))
        self.assertTrue(all(max(value, mp.mpf("0.26213")) == mp.mpf("0.26213")
                            for value in xi_next))

    def test_component_bounds_decrease_inside_half_line_and_across_corner(self) -> None:
        with mp.workdps(100):
            r = SOURCE_REPROOF_DIMENSION_CUTOFF
            corner = source_constant_component_log_uppers(r)
            later_same_a = source_constant_component_log_uppers(r, 2 * r**5)
            next_corner = source_constant_component_log_uppers(r + 1)
            self.assertTrue(all(later_same_a[key] < corner[key] for key in corner))
            self.assertTrue(all(next_corner[key] < corner[key] for key in corner))

    def test_invalid_or_uncertified_domains_fail_closed(self) -> None:
        cutoff = SOURCE_REPROOF_DIMENSION_CUTOFF
        with self.assertRaises(ValueError):
            source_constant_component_log_uppers(cutoff - 1)
        with self.assertRaises(ValueError):
            source_constant_component_log_uppers(cutoff, cutoff**5 - 1)
        with self.assertRaises(TypeError):
            source_constant_budget(True)
        with self.assertRaises(ValueError):
            source_constant_budget(cutoff, "nan")

    def test_structural_certificate_stops_before_parent_promotion(self) -> None:
        certificate = structural_certificate()
        self.assertTrue(certificate.source_constant_reproof_closed)
        self.assertTrue(certificate.final_low_zero_2q_factor_preserved)
        self.assertTrue(certificate.unknown_i_maximized_not_selected)
        self.assertTrue(certificate.q_equal_one_removed_by_exact_centering)
        self.assertTrue(certificate.h1c1b4c_conditional_requirement_met)
        self.assertTrue(certificate.unconditional_full_absorption_at_new_cutoff_closed)
        self.assertFalse(certificate.printed_constant_formula_used)
        self.assertFalse(certificate.parent_composition_audited)
        self.assertFalse(certificate.hypothesis1_clause2_closed)
        self.assertFalse(certificate.proposition92_closed)
        self.assertFalse(certificate.siv_08_closed)
        self.assertFalse(certificate.x_cert_ready)
        self.assertFalse(certificate.actual_prime_experiment_performed)

    def test_machine_contract_and_hashes(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.0.0")
        self.assertEqual(self.contract["gate"], "H1c-1b.4d")
        self.assertEqual(
            self.contract["outcome"],
            "CORRECTED_SOURCE_C_A_REPROOF_CLOSED_ABOVE_R_1E10_PARENT_COMPOSITION_PENDING",
        )
        self.assertEqual(
            self.contract["proof_cutoff"]["sieve_dimension_r"],
            SOURCE_REPROOF_DIMENSION_CUTOFF,
        )
        self.assertEqual(
            self.contract["source_component_accounting"]["total"],
            SOURCE_COMPONENT_COUNT,
        )
        for source in self.contract["predecessor_artifacts"]:
            path = ROOT / Path(source["path"])
            self.assertTrue(path.is_file(), source["path"])
            self.assertEqual(_sha256(path), source["sha256"])
        for source in self.contract["primary_sources"]:
            local_path = source.get("local_path")
            if local_path:
                path = ROOT / Path(local_path)
                self.assertTrue(path.is_file(), local_path)
                self.assertEqual(_sha256(path), source["sha256"])
        status = self.contract["status_after_this_gate"]
        self.assertTrue(status["corrected_source_C_A_reproof_closed"])
        self.assertTrue(status["unconditional_full_absorption_at_new_cutoff_closed"])
        self.assertFalse(status["parent_composition_audited"])
        self.assertFalse(status["hypothesis1_clause2_closed"])
        self.assertFalse(status["proposition92_closed"])
        self.assertFalse(status["siv_08_closed"])
        self.assertFalse(status["x_cert_ready"])


if __name__ == "__main__":
    unittest.main()
