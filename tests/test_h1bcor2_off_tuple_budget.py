"""Finite exact oracle and adversarial scope checks for theory 50."""
from fractions import Fraction
import unittest

from source.h1bcor2_off_tuple_budget import (
    CLOSED_IDS, REMAINING_IDS, finite_scalar_budget, load_contract,
    markov_exception_budget, off_tuple_points, off_tuple_shifts, off_tuple_toy,
    validate_contract,
)


def fixture(**overrides):
    prior = {n: Fraction(1, 5) for n in (-3, 0, 1, 4, 8)}
    kwargs = dict(x=5, y=15, p_priors={3: prior, 5: prior},
                  q_values=(7, 11, 13), offsets=(1, 2), primes=(7, 11))
    kwargs.update(overrides)
    return off_tuple_toy(**kwargs)


class ShiftAndBudgetTests(unittest.TestCase):
    def test_strict_radius_integer_endpoint(self):
        hs = off_tuple_shifts(5, 15, (1, 2))
        self.assertEqual(hs, tuple(h for h in range(-11, 12) if h not in (1, 2)))
        self.assertIn(0, hs)
        self.assertIn(-11, hs)
        self.assertNotIn(12, hs)
        self.assertNotIn(-12, hs)
        self.assertLessEqual(len(hs), 9*15/5)

    def test_noninteger_radius_and_support_no_omissions(self):
        for x, y in ((5, 6), (5, 15), (5, Fraction(31, 2))):
            hs = off_tuple_shifts(x, y, (1, 2))
            self.assertLessEqual(len(hs), 9*y/x)
            for p in (3, 5):
                for q in (7, 11, 13):
                    if q > y:
                        continue
                    for h in range(-100, 101):
                        if abs(q-h*p) <= y and h not in (1, 2):
                            self.assertIn(h, hs)
        self.assertEqual(off_tuple_shifts(4, Fraction(9, 2), (1, 2)),
                         (-4, -3, -2, -1, 0, 3, 4))

    def test_extra_q_distinct_even_when_residues_collide(self):
        self.assertEqual(off_tuple_points(13, 7, 0, (1, 2)), (13, 20, 27))
        points = off_tuple_points(13, 7, -1, (1, 2))
        self.assertEqual(len(set(points)), 3)
        self.assertEqual(len({n % 7 for n in points}), 1)

    def test_refuse_tuple_h_and_bad_offsets(self):
        for h, offsets in ((1, (1, 2)), (0, (1, 1)), (0, (True, 2))):
            with self.assertRaises(ValueError):
                off_tuple_points(13, 7, h, offsets)
        for args in ((0, 15, (1, 2)), (5, 4, (1, 2)),
                     (1, 10000, (1,)), (5.0, 15, (1, 2))):
            with self.assertRaises(ValueError):
                off_tuple_shifts(*args)

    def test_markov_exact_and_cap(self):
        self.assertEqual(markov_exception_budget("1/8", "1/2", 2), Fraction(1, 8))
        self.assertEqual(markov_exception_budget(3, "1/2", 2), 1)
        self.assertEqual(markov_exception_budget(0, 1, 1), 0)
        for args in ((-1, 1, 1), (1, 0, 1), (1, 1, 0), (0.25, 1, 1)):
            with self.assertRaises(ValueError):
                markov_exception_budget(*args)

    def test_integer_cardinality_and_equal_cutoff(self):
        values = (Fraction(1, 2), Fraction(3, 4), Fraction(0))
        count = sum(v > Fraction(1, 2) for v in values)
        self.assertEqual(count, 1)  # equality is not bad
        for limit in (Fraction(1), Fraction(3, 2)):
            self.assertLessEqual(count, limit.numerator // limit.denominator)
        self.assertNotEqual(1, -(-1 // 1)-1)  # ceil(R)-1 wrong at integer R

    def test_exact_composition_and_inherited_cutoff_scalar_only(self):
        for b in (2000, 2302, 10**6):
            result = finite_scalar_budget(b)
            self.assertEqual(result["composition_multiplier"], Fraction(94536, 125))
            self.assertLess(result["failure_upper_using_ln5_gt_one"], Fraction(1, 10**18))
            self.assertTrue(result["structural_and_log_inputs_assumed"])
            self.assertFalse(result["actual_prime_experiment_performed"])
            self.assertFalse(result["x_cert_ready"])
        self.assertEqual(96*2000**5, 3_072_000_000_000_000_000)
        self.assertLess(200, 2**17)
        for b in (1999, True, 2000.0):
            with self.assertRaises(ValueError):
                finite_scalar_budget(b)


class ExactOffTupleToyTests(unittest.TestCase):
    def test_independent_oracles_good_p_and_markov(self):
        result = fixture()
        self.assertEqual(result["states"], 77)
        self.assertEqual(result["h_count"], 21)
        self.assertEqual(result["direct_all_p_expectation"],
                         result["product_oracle_expectation"])
        self.assertLessEqual(result["direct_good_p_expectation"],
                             result["direct_all_p_expectation"])
        self.assertGreater(result["direct_good_p_expectation"], 0)
        self.assertLessEqual(result["actual_exception_failure"],
                             result["markov_failure_upper"])
        self.assertGreater(result["maximum_conditioning_slack"], 0)
        self.assertFalse(result["analytic_cutoff_verified_by_toy"])

    def test_missing_q_survival_changes_expectation(self):
        result = fixture()
        self.assertGreater(result["incorrect_missing_q_expectation"],
                           result["product_oracle_expectation"])

    def test_empty_sieve_and_tighter_good_p_subset(self):
        result = fixture(primes=())
        self.assertEqual(result["states"], 1)
        self.assertEqual(result["direct_good_p_expectation"],
                         result["product_oracle_expectation"])
        strict = fixture(eta=Fraction(1, 100))
        loose = fixture(eta=Fraction(9, 10))
        self.assertLessEqual(strict["direct_good_p_expectation"],
                             loose["direct_good_p_expectation"])

    def test_actual_empirical_failure_bound_nontrivial(self):
        result = fixture(value_cutoff=Fraction(1, 5), count_cutoff=Fraction(5, 2))
        self.assertGreaterEqual(result["actual_exception_failure"], 0)
        self.assertLess(result["markov_failure_upper"], 1)

    def test_reject_missing_assumptions_or_huge_toy(self):
        changes = (
            {"independent_uniform": False}, {"primes": (97, 101)},
            {"primes": (7, 7)}, {"q_values": (5, 7)},
            {"p_priors": {2: {0: 1}}}, {"p_priors": {3: {16: 1}}},
            {"p_priors": {3: {0: Fraction(1, 2)}}}, {"eta": 0}, {"eta": 1},
            {"count_cutoff": 0}, {"value_cutoff": 0},
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                fixture(**change)


class ContractTests(unittest.TestCase):
    def test_parent_current_gate_and_root_scope(self):
        import json
        from source.h1bcor2_off_tuple_budget import ROOT
        base = ROOT / "docs/method/theory/data"
        h1b = json.loads((base / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json").read_text(encoding="utf-8"))
        h1c = json.loads((base / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json").read_text(encoding="utf-8"))
        t1 = json.loads((base / "Sono_FMT_T1_proof_obligations_v1.json").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / h1b["h1bcor2_ledger"]).is_file())
        self.assertEqual(h1b["composition"]["remaining_actual_work_packages"], 4)
        self.assertEqual(h1c["next_gate"]["id"], "DEP-R09")
        self.assertEqual(h1c["successor_finite_off_tuple_budget"]["newly_closed_actual_work"], ["DEP-R05"])
        self.assertTrue((ROOT / t1["h1bcor2_actual_off_tuple_ledger"]).is_file())
        self.assertFalse(h1b["composition"]["ready_for_threshold_calculator"])
        self.assertEqual(len(t1["obligations"]), 66)

    def test_source_pins_and_current_scope(self):
        doc = load_contract()
        self.assertEqual(validate_contract(doc), [])
        self.assertEqual(doc["closed_actual_work"], list(CLOSED_IDS))
        self.assertEqual(doc["remaining_open_work"], list(REMAINING_IDS))
        self.assertEqual(len(REMAINING_IDS), 8)

    def test_predecessor_stays_immutable_historical_snapshot(self):
        from source.h1bcor1_finite_correlation import load_contract as previous
        from source.h1bcor1_finite_correlation import validate_contract as check_previous
        doc = previous()
        self.assertEqual(check_previous(doc), [])
        self.assertEqual(len(doc["remaining_open_work"]), 9)
        self.assertIn("DEP-R05", doc["remaining_open_work"])

    def test_refuse_scope_constant_and_root_mutations(self):
        changes = (
            ("scope", "q_survival_required", False),
            ("scope", "distinct_k_plus_one_required", False),
            ("scope", "negative_zero_positive_h_included", False),
            ("scope", "conditioning_denominator_preserved", False),
            ("scope", "global_union_budget_closed", True),
            ("scope", "weight", "unfiltered"),
            ("scope", "boundary_mode", "start"),
            ("scope", "logs", "base_2"),
            ("scope", "x_cert_ready", True),
            ("constants", "failure_upper", "0"),
            ("constants", "c_aux", "2e-17"),
            ("broad_root_status", "X_CERT", "CLOSED"),
        )
        for section, key, value in changes:
            with self.subTest(key=key):
                doc = load_contract()
                doc[section][key] = value
                self.assertTrue(validate_contract(doc, check_hashes=False))

    def test_refuse_extra_closure_missing_pdf_source_or_hash_mutation(self):
        doc = load_contract()
        doc["newly_closed_actual_work"].append("DEP-R06")
        self.assertTrue(validate_contract(doc, check_hashes=False))
        doc = load_contract()
        doc["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(any("hash mismatch" in s for s in validate_contract(doc)))
        doc = load_contract()
        doc["source_pins"][0]["path"] = "../outside.pdf"
        self.assertTrue(validate_contract(doc, check_hashes=False))
        doc = load_contract()
        doc["pdf_reading"][1]["page_type"] = "NATIVE_TEXT"
        self.assertTrue(validate_contract(doc, check_hashes=False))


if __name__ == "__main__":
    unittest.main()
