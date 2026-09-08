"""Regression checks for the H1c-1b.2 exceptional-B/remainder bridge."""

from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b2_common_exceptional_remainder import (
    PUBLISHED_REMAINDER_TERM_COUNT,
    R1,
    bordignon_relative_remainder_terms,
    dyadic_remainder_over_t_upper,
    exceptional_filter_implication,
    structural_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b2_common_exceptional_remainder_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


class H1c1b2CommonExceptionalRemainderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_prime_factor_filter_implication_and_negative_inputs(self) -> None:
        for q in range(1, 10000):
            self.assertTrue(exceptional_filter_implication(2310, 11, q))
        with self.assertRaises(ValueError):
            exceptional_filter_implication(2310, 13, 17)
        with self.assertRaises(ValueError):
            exceptional_filter_implication(2310, 21, 17)
        with self.assertRaises(TypeError):
            exceptional_filter_implication(True, 11, 17)  # type: ignore[arg-type]

    def test_final_published_twelve_terms_match_direct_formulas(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            log_u = mp.e**8
            a = Fraction(10, 1)
            ell = mp.log(log_u)
            log_q1 = mp.mpf(7) * ell
            c0 = mp.mpf("2.3")
            c1 = mp.mpf("1.8")
            c12 = mp.mpf("4.7")
            terms = bordignon_relative_remainder_terms(
                log_u,
                a,
                log_q1,
                c0_upper=c0,
                c1_upper=c1,
                theorem12_constant_upper=c12,
            )
            self.assertEqual(terms.term_count, PUBLISHED_REMAINDER_TERM_COUNT)
            self.assertEqual(terms.term_count, 12)
            self.assertTrue(all(value > 0 for value in terms.__dict__.values()))

            delta = 1 / (2 * mp.mpf(10) * (mp.mpf(5113) / 2500) * ell)
            common_small = c1**2 * (1 + 10 * ell) * log_u / 2
            expected = {
                "leading_sqrt": mp.exp(-log_u / 2),
                "main_log_tail": (
                    2 * c1 * c0 * mp.exp(-mp.mpf("5.5") * ell)
                ),
                "main_q1_tail": (
                    2 * c1 * c0 * mp.exp(mp.mpf("4.5") * ell - log_q1)
                ),
                "theorem12_small_modulus": (
                    c1**2 * c12 * (1 + 10 * ell) * mp.exp(-6 * ell) / 2
                ),
                "induced_character_small_modulus": (
                    mp.exp(-log_u / 2 - 9 * ell) / (2 * mp.log(2))
                ),
                "exceptional_zero": (
                    common_small * mp.exp(-delta * log_u) / (1 - delta)
                ),
                "density_exponential": (
                    common_small
                    * 34
                    * log_u ** mp.mpf("1.52")
                    * mp.exp(-mp.mpf("0.81") * mp.sqrt(log_u))
                ),
                "density_constant": (
                    common_small
                    * (10 * ell / mp.log(2))
                    * mp.exp(-log_u)
                ),
                "large_modulus_sqrt": (
                    2
                    * c0
                    * c1
                    * mp.exp(-log_u / 2 + mp.mpf("14.5") * ell)
                ),
                "large_modulus_eleven_twelfths": (
                    9
                    * c0
                    * c1
                    * mp.exp(-log_u / 12 - mp.mpf("0.5") * ell)
                ),
                "large_modulus_five_sixths": (
                    mp.mpf("2.5")
                    * c0
                    * c1
                    * mp.exp(-log_u / 6 + mp.mpf("4.5") * ell)
                ),
                "large_modulus_five_sixths_log": (
                    mp.mpf("1.25")
                    * c0
                    * c1
                    * mp.exp(-log_u / 6 + mp.mpf("5.5") * ell)
                ),
            }
            self.assertEqual(set(expected), set(terms.__dict__))
            for name, expected_value in expected.items():
                self.assertTrue(
                    mp.almosteq(getattr(terms, name), expected_value),
                    name,
                )
            self.assertTrue(mp.almosteq(terms.total, mp.fsum(terms.__dict__.values())))
        finally:
            mp.mp.dps = old_dps

    def test_dyadic_normalization_is_r_t_plus_two_r_2t(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            log_t = mp.e**8
            a = 10
            log_q1 = 7 * mp.log(log_t)
            kwargs = {
                "c0_upper": 2,
                "c1_upper": 2,
                "theorem12_constant_upper": 3,
            }
            lower = bordignon_relative_remainder_terms(
                log_t, a, log_q1, **kwargs
            )
            upper = bordignon_relative_remainder_terms(
                log_t + mp.log(2), a, log_q1, **kwargs
            )
            combined = dyadic_remainder_over_t_upper(
                log_t, a, log_q1, **kwargs
            )
            self.assertTrue(mp.almosteq(combined, lower.total + 2 * upper.total))
        finally:
            mp.mp.dps = old_dps

    def test_structural_certificate_closes_only_the_narrow_bridge(self) -> None:
        cert = structural_certificate()
        self.assertEqual(cert.sieve_dimension_r, 36)
        self.assertEqual(cert.bordignon_a, Fraction(129610, 1))
        self.assertTrue(cert.fixed_q1_for_both_endpoints)
        self.assertTrue(cert.same_exceptional_modulus_for_both_endpoints)
        self.assertTrue(cert.one_prime_b_filter_implication_closed)
        self.assertTrue(cert.b_is_scale_dependent_not_global)
        self.assertTrue(cert.b_size_condition_available)
        self.assertTrue(cert.endpoint_modulus_capacity_closed)
        self.assertEqual(cert.published_remainder_terms_registered, 12)
        self.assertTrue(cert.final_published_formula_required)
        self.assertTrue(cert.raw_von_mangoldt_open_closed_composition_closed)
        for name in (
            "half_open_endpoint_transfer_closed",
            "prime_power_removal_closed",
            "unweighted_prime_count_transfer_closed",
            "exact_maynard_recentering_closed",
            "full_remainder_absorption_closed",
            "bordignon_constant_normalization_resolved",
            "hypothesis1_clause2_closed",
            "proposition92_closed",
            "siv_08_closed",
            "x_cert_ready",
            "actual_prime_experiment_performed",
        ):
            self.assertFalse(getattr(cert, name), name)

    def test_machine_contract_and_t1_remain_fail_closed(self) -> None:
        self.assertEqual(
            self.contract["outcome"],
            "COMMON_EXCEPTIONAL_B_AND_RAW_PSI_DYADIC_COMPOSITION_CLOSED_COUNT_TRANSFER_AND_ABSORPTION_OPEN",
        )
        self.assertEqual(
            len(self.contract["published_final_remainder"]["terms"]), 12
        )
        self.assertTrue(
            self.contract["common_exceptional_object"][
                "one_prime_B_filter_implication_closed"
            ]
        )
        self.assertFalse(self.contract["limits"]["hypothesis1_clause2_closed"])
        self.assertFalse(self.contract["limits"]["numerical_x_cert_ready"])
        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertIn("H1c-1b.2", rows["SIV-08"]["notes"])

    def test_primary_source_hashes_are_fixed(self) -> None:
        for source in self.contract["source_registry"]:
            expected = source["sha256"]
            if expected == "SELF_HASHED_BY_REPOSITORY_TESTS":
                continue
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                expected,
                source["key"],
            )

    def test_final_published_version_is_authoritative(self) -> None:
        version = self.contract["source_version_control"]
        self.assertEqual(version["authoritative_formula"], "NYJM_FINAL_2021")
        self.assertEqual(version["center"], "psi(u)/phi(q)")
        self.assertFalse(version["arxiv_v1_formula_adopted"])
        self.assertEqual(R1, Fraction(5113, 2500))

    def test_invalid_remainder_inputs_fail_closed(self) -> None:
        kwargs = {
            "c0_upper": 1,
            "c1_upper": 1,
            "theorem12_constant_upper": 1,
        }
        with self.assertRaises(ValueError):
            bordignon_relative_remainder_terms(mp.e**6, 10, 0, **kwargs)
        with self.assertRaises(ValueError):
            bordignon_relative_remainder_terms(mp.e**8, 3, 0, **kwargs)
        with self.assertRaises(ValueError):
            bordignon_relative_remainder_terms(
                mp.e**8, 10, 11 * 8, **kwargs
            )
        with self.assertRaises(ValueError):
            bordignon_relative_remainder_terms(
                mp.e**8,
                10,
                0,
                c0_upper=-1,
                c1_upper=1,
                theorem12_constant_upper=1,
            )


if __name__ == "__main__":
    unittest.main()
