"""Regression tests for the H1c-1b.4c conditional absorption budget."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import mpmath as mp

from source.h1c1b1_parameter_modulus_envelope import bordignon_exponent
from source.h1c1b2_common_exceptional_remainder import (
    bordignon_relative_remainder_terms,
)
from source.h1c1b3_endpoint_count_transfer import (
    crude_normalized_count_transfer_upper,
)
from source.h1c1b4c_conditional_absorption import (
    C_COEFFICIENT_LOG_CEILING,
    NON_C_COMPONENT_COUNT,
    NON_C_COMPONENT_LOG_CEILING,
    PROVED_DIMENSION_CUTOFF,
    SAFE_LOG_C_A_UPPER,
    conditional_absorption_budget,
    exact_corner_log_upper_witnesses,
    exact_uniformity_sufficient_checks,
    normalized_c_a_coefficient_log,
    normalized_non_c_component_logs,
    structural_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b4c_conditional_absorption_v1.json"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class H1c1b4cConditionalAbsorptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_corner_witnesses_and_uniformity_conditions(self) -> None:
        witnesses = exact_corner_log_upper_witnesses()
        self.assertEqual(len(witnesses), NON_C_COMPONENT_COUNT)
        self.assertTrue(
            all(value < NON_C_COMPONENT_LOG_CEILING for value in witnesses.values())
        )
        self.assertTrue(all(exact_uniformity_sufficient_checks().values()))

    def test_numerical_corner_budget_has_large_positive_margin(self) -> None:
        with mp.workdps(100):
            logs = normalized_non_c_component_logs(PROVED_DIMENSION_CUTOFF)
            self.assertEqual(len(logs), NON_C_COMPONENT_COUNT)
            self.assertLess(max(logs.values()), NON_C_COMPONENT_LOG_CEILING)
            self.assertLess(
                normalized_c_a_coefficient_log(PROVED_DIMENSION_CUTOFF),
                C_COEFFICIENT_LOG_CEILING,
            )
            budget = conditional_absorption_budget()
            self.assertLess(budget.normalized_non_c_log_upper, -500)
            self.assertGreater(budget.admissible_log_c_a_upper, 548)
            self.assertLess(budget.admissible_log_c_a_upper, 549)
            self.assertEqual(budget.safe_project_log_c_a_upper, SAFE_LOG_C_A_UPPER)
            self.assertTrue(budget.safe_project_condition_passes)

    def test_coarse_budget_dominates_predecessor_exact_formula(self) -> None:
        with mp.workdps(100):
            r = PROVED_DIMENSION_CUTOFF
            L = mp.mpf(r**5)
            ell = mp.log(L)
            A_fraction = bordignon_exponent(r)
            A = mp.mpf(A_fraction.numerator) / A_fraction.denominator
            kwargs = {
                "c0_upper": 49,
                "c1_upper": 3,
                "theorem12_constant_upper": 0,
            }
            lower = bordignon_relative_remainder_terms(L, A_fraction, A * ell, **kwargs)
            upper = bordignon_relative_remainder_terms(
                L + mp.log(2), A_fraction, A * ell, **kwargs
            )
            rho_upper = lower.total - lower.main_q1_tail + upper.main_q1_tail
            exact_transfer = crude_normalized_count_transfer_upper(L, rho_upper)
            target = 1 / (2 * L ** (100 * r * r + 1))
            exact_normalized_ratio = exact_transfer.total / target
            coarse_normalized_ratio = mp.exp(
                conditional_absorption_budget(r).normalized_non_c_log_upper
            )
            self.assertGreaterEqual(coarse_normalized_ratio, exact_normalized_ratio)

            c_one = bordignon_relative_remainder_terms(
                L,
                A_fraction,
                A * ell,
                c0_upper=49,
                c1_upper=3,
                theorem12_constant_upper=1,
            )
            c_coefficient_rho = c_one.theorem12_small_modulus
            exact_c_ratio = (
                crude_normalized_count_transfer_upper(L, c_coefficient_rho)
                .partial_summation
                / target
            )
            coarse_c_ratio = mp.exp(normalized_c_a_coefficient_log(r))
            self.assertGreaterEqual(coarse_c_ratio, exact_c_ratio)

    def test_invalid_or_uncertified_domains_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            normalized_non_c_component_logs(PROVED_DIMENSION_CUTOFF - 1)
        with self.assertRaises(ValueError):
            normalized_non_c_component_logs(
                PROVED_DIMENSION_CUTOFF,
                PROVED_DIMENSION_CUTOFF**5 - 1,
            )
        with self.assertRaises(ValueError):
            normalized_c_a_coefficient_log(
                PROVED_DIMENSION_CUTOFF,
                (PROVED_DIMENSION_CUTOFF + 1) ** 5,
            )
        with self.assertRaises(TypeError):
            conditional_absorption_budget(True)

    def test_structural_certificate_is_conditional_and_does_not_promote(self) -> None:
        certificate = structural_certificate()
        self.assertTrue(certificate.non_c_components_complete)
        self.assertTrue(certificate.all_non_c_components_absorbed_above_cutoff)
        self.assertTrue(certificate.admissible_c_a_formula_derived)
        self.assertTrue(certificate.conditional_full_absorption_closed)
        self.assertFalse(certificate.numerical_source_c_a_upper_closed)
        self.assertFalse(certificate.unconditional_full_absorption_closed)
        self.assertFalse(certificate.hypothesis1_clause2_closed)
        self.assertFalse(certificate.proposition92_closed)
        self.assertFalse(certificate.siv_08_closed)
        self.assertFalse(certificate.x_cert_ready)
        self.assertFalse(certificate.actual_prime_experiment_performed)

    def test_machine_contract_and_predecessor_hashes(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.0.0")
        self.assertEqual(self.contract["gate"], "H1c-1b.4c")
        self.assertEqual(
            self.contract["outcome"],
            "NON_C_ABSORPTION_AND_CONDITIONAL_C_A_BUDGET_CLOSED_SOURCE_C_A_OPEN",
        )
        self.assertEqual(
            self.contract["proof_cutoff"]["sieve_dimension_r"],
            PROVED_DIMENSION_CUTOFF,
        )
        self.assertEqual(
            self.contract["conditional_source_requirement"]["log_C_A_upper"],
            SAFE_LOG_C_A_UPPER,
        )
        for source in self.contract["predecessor_artifacts"]:
            path = ROOT / Path(source["path"])
            self.assertTrue(path.is_file(), source["path"])
            self.assertEqual(_sha256(path), source["sha256"])
        status = self.contract["status_after_this_gate"]
        self.assertTrue(status["conditional_full_absorption_closed"])
        self.assertFalse(status["numerical_source_C_A_upper_closed"])
        self.assertFalse(status["unconditional_full_absorption_closed"])
        self.assertFalse(status["hypothesis1_clause2_closed"])
        self.assertFalse(status["proposition92_closed"])
        self.assertFalse(status["siv_08_closed"])
        self.assertFalse(status["x_cert_ready"])


if __name__ == "__main__":
    unittest.main()
