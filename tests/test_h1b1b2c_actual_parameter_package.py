"""Regression tests for the H1b-1b-2c actual-input contract."""

from __future__ import annotations

import hashlib
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    MAYNARD_ACTUAL_LOCAL_FAMILIES,
    MAYNARD_APPLICATION_EXCLUSION_IDS,
)
from source.h1b1b2c_actual_parameter_package import (
    H1B1B2C_GGPY_A1_CAP,
    H1B1B2C_LOCAL_CORRECTION_UPPER,
    H1B1B2C_LOWER_DISCREPANCY_BASE,
    H1B1B2C_MAYNARD_A1_GAP,
    H1B1B2C_UPPER_DISCREPANCY_A2,
    MAYNARD_ACTUAL_GAMMA_APPLICATION_SPECS,
    actual_local_density_certificate,
    common_actual_parameter_package,
    lower_discrepancy_l,
    nonexcluded_positive_correction_upper,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1b1b2c_actual_parameter_specialization_v1.json"
)


def primes_between(lower: int, upper: int) -> list[int]:
    """Small dependency-free prime generator used only for regression grids."""

    result: list[int] = []
    for candidate in range(max(2, lower), upper + 1):
        if all(candidate % divisor for divisor in range(2, math.isqrt(candidate) + 1)):
            result.append(candidate)
    return result


class ActualParameterPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_all_eleven_source_traced_applications_are_mapped(self) -> None:
        specs = MAYNARD_ACTUAL_GAMMA_APPLICATION_SPECS
        self.assertEqual(len(specs), 11)
        self.assertEqual({row.application_id for row in specs}, MAYNARD_APPLICATION_EXCLUSION_IDS)
        self.assertTrue({row.family for row in specs} <= MAYNARD_ACTUAL_LOCAL_FAMILIES)
        line_1135 = [row for row in specs if row.application_id.startswith("L1135")]
        self.assertEqual(len(line_1135), 2)

    def test_exact_local_grid_satisfies_uniform_density_contract(self) -> None:
        for k in range(2, 15):
            primes = primes_between(2 * k * k + 1, 2 * k * k + 80)
            self.assertTrue(primes)
            for prime in primes:
                for root_count in range(1, k + 2):
                    for previous in range(root_count):
                        for family in MAYNARD_ACTUAL_LOCAL_FAMILIES:
                            cert = actual_local_density_certificate(
                                k=k,
                                prime=prime,
                                root_count=root_count,
                                previous_available_coordinates=previous,
                                family=family,
                            )
                            self.assertGreater(cert.stage_denominator, Fraction(prime, 4))
                            self.assertLess(cert.density, Fraction(1, 2))
                            self.assertGreaterEqual(cert.density_excess_over_one_over_p, 0)
                            self.assertLessEqual(
                                cert.density_excess_over_one_over_p,
                                Fraction(12 * k, prime * prime),
                            )
                            self.assertLessEqual(cert.denominator_defect, 3 * k)

    def test_fixed_common_constants_are_fail_closed(self) -> None:
        self.assertEqual(H1B1B2C_MAYNARD_A1_GAP, Fraction(1, 2))
        self.assertEqual(H1B1B2C_GGPY_A1_CAP, 2)
        self.assertEqual(H1B1B2C_UPPER_DISCREPANCY_A2, 8)
        self.assertEqual(H1B1B2C_LOCAL_CORRECTION_UPPER, 4)
        self.assertEqual(H1B1B2C_LOWER_DISCREPANCY_BASE, 5)

    def test_nonexcluded_correction_majorant_stays_below_four(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for k in range(2, 1001):
                self.assertLess(nonexcluded_positive_correction_upper(k), 4)
            with self.assertRaises(ValueError):
                nonexcluded_positive_correction_upper(1)
        finally:
            mp.mp.dps = old_dps

    def test_common_package_uses_lambda_star_and_keeps_parent_open(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            package = common_actual_parameter_package(
                k=10,
                alpha="0.01",
                theta="0.25",
                log_r=100,
            )
            self.assertEqual(package.maynard_a1_gap, Fraction(1, 2))
            self.assertEqual(package.ggpy_a1_cap, 2)
            self.assertEqual(package.a2, 8)
            self.assertEqual(package.actual_application_count, 11)
            self.assertEqual(
                package.lower_discrepancy_l,
                5 + mp.log(package.log_excluded_integer_upper),
            )
            self.assertEqual(
                package.one_step_relative_error_coefficient,
                package.weighted_multiplier * package.lower_discrepancy_l_plus_one,
            )
            self.assertGreater(package.weighted_multiplier, mp.mpf("1e121"))
            self.assertFalse(package.r_fold_composition_closed)
            self.assertFalse(package.siv_07_closed)
            self.assertFalse(package.x_cert_ready)
        finally:
            mp.mp.dps = old_dps

    def test_invalid_scope_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            actual_local_density_certificate(
                k=2,
                prime=7,
                root_count=1,
                previous_available_coordinates=0,
                family="p_minus_a",
            )
        with self.assertRaises(ValueError):
            actual_local_density_certificate(
                k=2,
                prime=11,
                root_count=4,
                previous_available_coordinates=0,
                family="p_minus_a",
            )
        with self.assertRaises(ValueError):
            lower_discrepancy_l(1)

    def test_contract_provenance_and_nonpromotion(self) -> None:
        contract = self.contract
        self.assertEqual(contract["schema_version"], "1.0.0")
        self.assertEqual(
            contract["outcome"],
            "ACTUAL_FOUR_FAMILY_INPUTS_PARAMETERIZED_EXPLICIT",
        )
        self.assertEqual(contract["common_parameters"]["maynard_a1_gap"], "1/2")
        self.assertEqual(contract["common_parameters"]["ggpy_a1_cap"], 2)
        self.assertEqual(contract["common_parameters"]["A2"], 8)
        self.assertEqual(contract["common_parameters"]["L"], "5+log(Lambda_star)")
        self.assertEqual(len(contract["applications"]), 11)
        self.assertFalse(contract["r_fold_composition_closed"])
        self.assertFalse(contract["siv_07_closed"])
        self.assertFalse(contract["numerical_x_cert_ready"])
        self.assertFalse(contract["actual_threshold_computed"])
        self.assertFalse(contract["new_python_dependency_required"])
        self.assertFalse(contract["lean_required_for_this_gate"])

        for source in contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source["sha256"])

        parent = contract["parent_status"]
        self.assertEqual(parent["H1B-L83"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")
        self.assertEqual(parent["H1B-L84"], "RATE_MISSING")
        self.assertEqual(parent["H1B1-PACKAGE"], "HARD_BLOCKER")
        self.assertEqual(parent["SIV-07"], "HARD_BLOCKER")
        self.assertEqual(parent["X_cert"], "OPEN")


if __name__ == "__main__":
    unittest.main()
