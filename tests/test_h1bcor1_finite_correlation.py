"""Exact finite oracles and rejection cases for the theory 49 package."""
from __future__ import annotations

import copy
from fractions import Fraction
from math import factorial
import unittest

from source.h1bcor1_finite_correlation import (
    CLOSED_IDS, REMAINING_IDS, actual_scalar_guards, conditional_law,
    conditioning_moments, correlation_log_envelope, enumerated_survival,
    finite_correlation_error, good_p_failure_from_moments, load_contract,
    sigma_toy, survival_probability, validate_contract,
)


class FiniteCorrelationTests(unittest.TestCase):
    def test_product_against_independent_residue_enumeration(self):
        for ns in ((0,), (0, 1), (-13, 0, 13), (0, 11, 22), (1, 8, 15, 22)):
            for ps in ((), (5,), (5, 7), (7, 11)):
                with self.subTest(points=ns, primes=ps):
                    self.assertEqual(survival_probability(ns, ps),
                                     enumerated_survival(ns, ps))

    def test_empty_sieve_is_exact(self):
        self.assertEqual(sigma_toy(()), 1)
        self.assertEqual(correlation_log_envelope((1, 2), ()), (0, 0))

    def test_repeated_event_not_independent_copy(self):
        self.assertEqual(survival_probability((0, 0), (5,)), Fraction(4, 5))
        self.assertNotEqual(survival_probability((0, 0), (5,)), sigma_toy((5,))**2)
        with self.assertRaises(ValueError):
            correlation_log_envelope((0, 0), (5,))

    def test_rational_log_envelopes_allow_pair_collisions(self):
        ps = (11, 13, 17)
        for ns in ((0, 1), (0, 11), (-13, 0, 143), (0, 11, 22)):
            A, B = correlation_log_envelope(ns, ps)
            d = max(A, B)
            self.assertLessEqual(d, Fraction(1, 2))
            ratio = survival_probability(ns, ps)/sigma_toy(ps)**len(ns)
            self.assertLessEqual(abs(ratio-1), 2*d)
        self.assertGreater(correlation_log_envelope((0, 11), ps)[1], 0)
        self.assertEqual(correlation_log_envelope((0, 1), ps)[1], 0)

    def test_refuse_missing_independence_and_invalid_prime_model(self):
        with self.assertRaises(ValueError):
            survival_probability((0, 1), (5,), independent_uniform=False)
        for ps in ((4,), (5, 5), (1009,), (True,), (5.0,)):
            with self.subTest(primes=ps), self.assertRaises(ValueError):
                survival_probability((0,), ps)

    def test_small_primes_cannot_use_log_expansion_bound(self):
        with self.assertRaises(ValueError):
            correlation_log_envelope((0, 1, 2), (5,))

    def test_toy_allocation_guards(self):
        with self.assertRaises(ValueError):
            enumerated_survival((0,), (97, 101, 103))
        with self.assertRaises(ValueError):
            survival_probability(range(17), (101,))
        with self.assertRaises(ValueError):
            conditioning_moments({i: Fraction(1, 32) for i in range(32)},
                                 tuple(range(8)), (97, 101))

    def test_core_error_uniform_multiplier_one(self):
        for a in (2, Fraction(5, 2), 10, 1000, 10**1000):
            bound = finite_correlation_error(a)
            self.assertGreater(bound, 0)
            self.assertLessEqual(bound, Fraction(1, a**16))
        for a in (1, True, 2.0, "nan"):
            with self.assertRaises(ValueError):
                finite_correlation_error(a)

    def test_elementary_log_endpoints_without_float(self):
        self.assertGreater(sum((Fraction(3**j, factorial(j)) for j in range(6)),
                               Fraction(0)), 18)
        self.assertGreater(2**10, 1000)  # e>2 -> ln(1000)<10


class ConditioningTests(unittest.TestCase):
    def test_conditioned_probability_keeps_denominator(self):
        prior = {0: Fraction(1, 2), 1: Fraction(1, 4), 2: Fraction(1, 4)}
        mass, law = conditional_law(prior, (0, 2), (5,), (0,))
        self.assertEqual(mass, Fraction(1, 2))
        self.assertEqual(law, {1: Fraction(1, 2), 2: Fraction(1, 2)})
        self.assertEqual(sum(law.values()), 1)
        self.assertGreater(law[1], prior[1])
        self.assertLessEqual(max(law.values()), max(prior.values())/mass)

    def test_zero_denominator_has_no_fake_law(self):
        self.assertEqual(conditional_law({0: 1}, (0,), (2,), (0,)),
                         (0, {}))

    def test_reject_malformed_prior_and_residues(self):
        for prior, shifts, residues in (
            ({0: Fraction(1, 2)}, (0,), (0,)),
            ({0: -1, 1: 2}, (0,), (0,)),
            ({0: 1.0}, (0,), (0,)),
            ({0: 1}, (0, 0), (0,)),
            ({0: 1}, (0,), (5,)),
            ({0: 1}, (0,), ()),
        ):
            with self.assertRaises(ValueError):
                conditional_law(prior, shifts, (5,), residues)

    def test_second_moment_against_independent_two_copy_enumeration(self):
        prior = {n: Fraction(1, 20) for n in range(20)}
        moments = conditioning_moments(prior, (0, 2), (11, 13))
        self.assertEqual(moments["second"], moments["independent_pair_second"])
        self.assertEqual(moments["collision_probability"], Fraction(56, 400))
        self.assertLessEqual(moments["collision_probability"],
                             moments["collision_union_upper"])
        self.assertGreater(moments["normalized_squared_deviation"], 0)
        self.assertNotEqual(moments["normalized_mean"], 1)
        # Center at one, not at the nonexact mean.
        variance = moments["normalized_second"]-moments["normalized_mean"]**2
        self.assertEqual(moments["normalized_squared_deviation"]-variance,
                         (moments["normalized_mean"]-1)**2)

    def test_three_epsilon_not_one_in_centered_error(self):
        self.assertEqual(good_p_failure_from_moments("1/100", "1/1000", "1/10"),
                         (Fraction(31, 1000), 1))
        for a in (1000, 1001):
            squared, fail = good_p_failure_from_moments(
                Fraction(2, a**17), Fraction(1, a**17), Fraction(1, a**3))
            self.assertEqual(squared, Fraction(7, a**17))
            self.assertEqual(fail, Fraction(7, a**11))
            self.assertEqual(fail* a**3, Fraction(7, a**8))
        for args in ((-1, 0, "1/10"), (0, -1, "1/10"), (0, 0, 0)):
            with self.assertRaises(ValueError):
                good_p_failure_from_moments(*args)

    def test_bad_prime_zero_assignment_cannot_hit_larger_prime(self):
        from source.h1bdep_actual_dependency import toy_primes
        for p in toy_primes(100):
            for q in toy_primes(200):
                if q > p:
                    self.assertNotEqual(q % p, 0)

    def test_actual_scalars_no_actual_array_or_threshold(self):
        for k in (10**200, 10**200+1, 10**210):
            result = actual_scalar_guards(k=k)
            self.assertTrue(all(result["checks"].values()))
            self.assertEqual(result["global_bad_p_upper"], Fraction(7, k**40))
            self.assertEqual(result["residue_sparsity_exponent"], Fraction(3, 5))
            self.assertTrue(result["structural_inputs_assumed"])
            for name in ("x_cert_ready", "full_hypergraph_certified",
                         "actual_prime_experiment_performed", "independent_formal_verification"):
                self.assertFalse(result[name])

    def test_reject_actual_dimension_or_bin_change(self):
        for k in (10**200-1, True, 1.0):
            with self.assertRaises(ValueError):
                actual_scalar_guards(k=k)
        k = 10**200
        for L in (k**5-1, (k+1)**5):
            with self.assertRaises(ValueError):
                actual_scalar_guards(k=k, log_outer_half=L)
        self.assertTrue(all(actual_scalar_guards(
            k=k, log_outer_half=Fraction((k+1)**5)-Fraction(1, 2))["checks"].values()))


class SuccessorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = load_contract()

    def test_sources_and_predecessor_hashes_unchanged(self):
        self.assertEqual(validate_contract(self.doc), [])
        self.assertEqual(len(self.doc["source_pins"]), 7)

    def test_three_closed_nine_open_not_whole_theorem(self):
        self.assertEqual(self.doc["closed_actual_work"], list(CLOSED_IDS))
        self.assertEqual(self.doc["remaining_open_work"], list(REMAINING_IDS))
        self.assertEqual(len(REMAINING_IDS), 9)
        self.assertTrue(self.doc["historical_ledger_preserved"])
        self.assertTrue(self.doc["work_counts_are_not_completion_percentages"])

    def test_no_silent_scope_or_root_promotion(self):
        for key, value in (
            ("x_cert_ready", True), ("full_hypergraph_certified", True),
            ("weight", "unfiltered"), ("u_quantifier", "k_only"),
            ("sigma_lower_direction", "upper/upper"),
            ("collision_cost_preserved", False), ("distinct_correlation_only", False),
            ("boundary_mode", "start"), ("logs", "base_2"),
        ):
            doc = copy.deepcopy(self.doc)
            doc["scope"][key] = value
            self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_no_unsupported_additional_closure(self):
        doc = copy.deepcopy(self.doc)
        doc["closed_actual_work"].append("DEP-R05")
        self.assertTrue(validate_contract(doc, check_hashes=False))
        doc = copy.deepcopy(self.doc)
        doc["broad_root_status"]["X_CERT"] = "PROJECT_EXPLICIT"
        self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_parent_ledgers_point_to_current_successor_and_keep_root_open(self):
        import json
        from source.h1bcor1_finite_correlation import ROOT
        base = ROOT / "docs/method/theory/data"
        h1b = json.loads((base / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json").read_text(encoding="utf-8"))
        h1c = json.loads((base / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json").read_text(encoding="utf-8"))
        t1 = json.loads((base / "Sono_FMT_T1_proof_obligations_v1.json").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / h1b["h1bcor1_ledger"]).is_file())
        self.assertEqual(h1c["successor_finite_correlation_conditioning"]["closed_actual_work"], list(CLOSED_IDS))
        self.assertTrue((ROOT / t1["h1bcor1_actual_probability_ledger"]).is_file())
        self.assertFalse(h1b["composition"]["ready_for_threshold_calculator"])
        self.assertEqual(len(t1["obligations"]), 66)

    def test_pdf_text_layer_does_not_turn_scan_into_native(self):
        doc = copy.deepcopy(self.doc)
        next(p for p in doc["pdf_reading"] if p["source"] == "RS1962")["page_type"] = "NATIVE_TEXT"
        self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_source_mutation_or_escape_rejected(self):
        doc = copy.deepcopy(self.doc)
        doc["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(any("hash mismatch" in s for s in validate_contract(doc)))
        doc["source_pins"][0]["path"] = "../outside.pdf"
        self.assertTrue(validate_contract(doc, check_hashes=False))


if __name__ == "__main__":
    unittest.main()
