"""Exact bounded algebra and provenance; not an actual covering experiment."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
import json
from math import prod
import unittest

from source.h1bcov1a_covering_constant import (
    ROOT, actual_gate_anchors, conditional_degree_moments, induction_relative_error,
    last_round_survival, load_contract, make_model, normalization,
    normalized_overlap_ratio, reweighted_laws, scalar_budget, validate_contract,
)


def independent_w(ps):
    vertices = tuple(ps)
    return [
        (tuple(v for v, on in zip(vertices, bits) if on),
         prod((ps[v] if on else 1-ps[v] for v, on in zip(vertices, bits)), start=Q(1)))
        for bits in product((False, True), repeat=len(vertices))
    ]


def fixture():
    ps = {0: Q(1, 2), 1: Q(2, 3), 2: Q(3, 4)}
    return make_model(ps, independent_w(ps), [
        [((), Q(1, 2)), ((0,), Q(1, 4)), ((0, 1), Q(1, 4))],
        [((), Q(2, 3)), ((1, 2), Q(1, 3))],
        [((0, 2), Q(1, 2)), ((2,), Q(1, 2))],
    ])


class ExactCoveringAlgebraTests(unittest.TestCase):
    def test_normalizer_first_exact_and_second_copy_oracle(self):
        m = fixture()
        for i in range(3):
            r = normalization(m, i)
            self.assertEqual(r["first"], 1)
            self.assertEqual(r["second"], r["second_product_copy"])
            self.assertGreaterEqual(r["centered_square"], 0)

    def test_independent_w_all_subset_identity(self):
        maximum, rows = induction_relative_error(fixture())
        self.assertEqual(maximum, 0)
        self.assertEqual(len(rows), 8)

    def test_correlated_w_is_not_treated_as_product_law(self):
        ps = {0: Q(1, 2), 1: Q(1, 2)}
        m = make_model(ps, [((), Q(1, 2)), ((0, 1), Q(1, 2))],
                       [[((0, 1), Q(1))]])
        maximum, _ = induction_relative_error(m)
        self.assertEqual(maximum, 1)
        r = normalization(m, 0)
        self.assertEqual(r["first"], 2)
        self.assertEqual(r["second"], 8)
        self.assertEqual(r["second"], r["second_product_copy"])

    def test_conditional_moments_direct_vs_product_expansion(self):
        m = fixture()
        for e in ((0,), (0, 1), (1, 2), (0, 1, 2)):
            for v in e:
                r = conditional_degree_moments(m, e, v)
                self.assertEqual(r["first"], r["expanded_first"])
                self.assertEqual(r["second"], r["expanded_second"])
                self.assertGreaterEqual(r["centered_square"], 0)
                self.assertEqual(len(r["by_index"]), 9)

    def test_identical_index_requires_independent_copy(self):
        ps = {0: Q(1, 2), 1: Q(1, 2)}
        m = make_model(ps, independent_w(ps),
                       [[((0,), Q(1, 2)), ((0, 1), Q(1, 2))]])
        r = conditional_degree_moments(m, (0,), 0)
        self.assertEqual(r["by_index"][0, 0], 5)
        # The same actual edge used twice would give 6, not the square of the sum.
        wrong_same_draw = sum(
            mass*m.survives(s | {0})/(m.p(s)**2*m.survives({0}))
            for s, mass in m.edge_laws[0].items()
        )
        self.assertEqual(wrong_same_draw, 6)
        self.assertNotEqual(wrong_same_draw, r["second"])

    def test_triple_overlap_retains_squared_local_factor(self):
        m = fixture()
        ratio, expanded = normalized_overlap_ratio(m, (0, 1), (0, 1), (0, 1), 0)
        self.assertEqual(ratio, Q(9, 4))
        self.assertEqual(ratio, expanded)
        self.assertNotEqual(ratio, Q(3, 2))

    def test_disjoint_except_v_overlap_ratio_is_one(self):
        m = fixture()
        self.assertEqual(normalized_overlap_ratio(m, (0, 1), (0, 2), (0,), 0), (1, 1))

    def test_all_overlap_patterns_two_oracles(self):
        m = fixture()
        sets = [frozenset({0} | {j+1 for j, on in enumerate(bits) if on})
                for bits in product((False, True), repeat=2)]
        for s, t, e in product(sets, repeat=3):
            direct, expanded = normalized_overlap_ratio(m, s, t, e, 0)
            self.assertEqual(direct, expanded)
            self.assertGreaterEqual(direct, 1)

    def test_reweighting_sums_to_one_and_preserves_support(self):
        m = fixture()
        saw_good = saw_bad = False
        for w in m.w_law:
            r = reweighted_laws(m, w, Q(1, 2))
            for original, law, f in zip(m.edge_laws, r["laws"], r["good"]):
                self.assertEqual(sum(law.values()), 1)
                self.assertLessEqual(set(law), set(original) | {frozenset()})
                saw_good |= f
                saw_bad |= not f
        self.assertTrue(saw_good and saw_bad)

    def test_zero_normalizer_becomes_empty_without_division(self):
        ps = {0: Q(1, 2)}
        m = make_model(ps, independent_w(ps), [[((0,), Q(1))]])
        r = reweighted_laws(m, (), Q(1, 4))
        self.assertEqual(r["normalizers"], (0,))
        self.assertEqual(r["good"], (False,))
        self.assertEqual(r["laws"], ({frozenset(): Q(1)},))

    def test_good_threshold_includes_equality(self):
        ps = {0: Q(1, 2)}
        m = make_model(ps, independent_w(ps), [[((), Q(1, 2)), ((0,), Q(1, 2))]])
        at = reweighted_laws(m, (0,), Q(1, 2))
        below = reweighted_laws(m, (0,), Q(499, 1000))
        self.assertEqual(at["normalizers"], (Q(3, 2),))
        self.assertEqual(at["good"], (True,))
        self.assertEqual(below["good"], (False,))

    def test_conditional_product_matches_exhaustive_choices(self):
        m = fixture()
        for w in m.w_law:
            for e in ((), (0,), (1, 2), (0, 1, 2)):
                r = last_round_survival(m, w, e, Q(1, 2))
                self.assertEqual(r["product"], r["exhaustive"])
                self.assertGreaterEqual(r["degree_sum"]-r["union_sum"], 0)
                self.assertLessEqual(r["degree_sum"]-r["union_sum"], r["pair_cost"])

    def test_empty_set_survives_exactly(self):
        m = fixture()
        for w in m.w_law:
            self.assertEqual(last_round_survival(m, w, (), Q(1, 2))["product"], 1)

    def test_zero_conditioning_event_is_rejected(self):
        m = make_model({0: Q(1, 2)}, [((), 1)], [[((), 1)]])
        with self.assertRaisesRegex(ValueError, "probability-zero"):
            conditional_degree_moments(m, (0,), 0)

    def test_bad_distinguished_vertex_rejected(self):
        with self.assertRaises(ValueError):
            conditional_degree_moments(fixture(), (0,), 1)
        with self.assertRaises(ValueError):
            normalized_overlap_ratio(fixture(), (0,), (0,), (1,), 0)

    def test_no_float_probability_or_parameter(self):
        with self.assertRaises(ValueError):
            make_model({0: 0.5}, [((), 1)], [[((), 1)]])
        with self.assertRaises(ValueError):
            make_model({0: "1/2"}, [((), 1.0)], [[((), 1)]])
        with self.assertRaises(ValueError):
            reweighted_laws(fixture(), (), 0.5)
        with self.assertRaises(ValueError):
            scalar_budget(0.01)

    def test_invalid_law_mass_duplicate_or_vertex_rejected(self):
        for law in [[((), Q(1, 2))], [((), Q(1, 2)), ((), Q(1, 2))],
                    [((7,), 1)], [((0, 0), 1)], [((), 0), ((0,), 1)]]:
            with self.subTest(law=law), self.assertRaises(ValueError):
                make_model({0: Q(1, 2)}, [((), 1)], [law])

    def test_bounded_size_and_zero_p_rejected(self):
        for ps in ({}, {i: Q(1, 2) for i in range(6)}, {0: 0}):
            with self.subTest(ps=ps), self.assertRaises(ValueError):
                make_model(ps, [((), 1)], [[((), 1)]])
        with self.assertRaises(ValueError):
            make_model({0: Q(1, 2)}, [((), 1)], [[((), 1)]]*5)

    def test_exact_scalar_reduction_endpoint_and_smaller_t(self):
        for t in (Q(1, 100), Q(1, 1000), Q(1, 10**6)):
            self.assertTrue(all(scalar_budget(t).values()))

    def test_invalid_scalar_gate_is_not_silently_clipped(self):
        for t in (0, -1, Q(1, 99), True):
            with self.subTest(t=t), self.assertRaises(ValueError):
                scalar_budget(t)

    def test_actual_gate_integer_anchors(self):
        self.assertTrue(all(actual_gate_anchors().values()))


class CoveringConstantContractTests(unittest.TestCase):
    def test_parent_core_promoted_but_root_not_promoted(self):
        base = ROOT / "docs/method/theory/data"
        h1b = json.loads((base / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json").read_text(encoding="utf-8"))
        h1c = json.loads((base / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json").read_text(encoding="utf-8"))
        t1 = json.loads((base / "Sono_FMT_T1_proof_obligations_v1.json").read_text(encoding="utf-8"))
        rows = {r["id"]: r for r in t1["obligations"]}
        self.assertEqual(rows["COV-06"]["status"], "EXPLICIT")
        self.assertIn("C0=100", rows["COV-06"]["explicit_bound"])
        for key in ("SIV-07", "SIV-08", "SIV-09", "FIN-05"):
            self.assertEqual(rows[key]["status"], "HARD_BLOCKER")
        for key in ("COV-08", "COV-11"):
            self.assertEqual(rows[key]["status"], "PARTIAL")
        self.assertEqual(h1b["composition"]["hypergraph_core_C0_sufficient"], 100)
        self.assertEqual(h1b["composition"]["remaining_actual_work_packages"], 4)
        self.assertFalse(h1b["composition"]["ready_for_threshold_calculator"])
        self.assertEqual(h1c["next_gate"]["id"], "DEP-R09")
        self.assertEqual(h1c["successor_explicit_hypergraph_core"]["newly_closed_actual_work"], ["DEP-R07"])

    def test_live_hash_pins_and_scope(self):
        self.assertEqual(validate_contract(load_contract()), [])

    def test_c0_contract_is_sufficient_not_optimal_or_published_value(self):
        d = load_contract()
        self.assertEqual(d["constants"]["C0_sufficient"], 100)
        self.assertFalse(d["scope"]["C0_optimality_claimed"])
        self.assertIn("replaces printed", d["proof_modification"])

    def test_no_root_or_actual_promotion(self):
        d = load_contract()
        for key in ("x_cert_ready", "threshold_calculator_ready", "global_union_budget_closed",
                    "actual_prime_experiment_performed", "independently_formally_verified"):
            self.assertIs(d["scope"][key], False)
            mutated = deepcopy(d)
            mutated["scope"][key] = True
            self.assertTrue(validate_contract(mutated, check_hashes=False))

    def test_changed_constant_is_rejected_by_frozen_contract(self):
        d = load_contract()
        d["constants"]["C0_sufficient"] = 1
        self.assertTrue(validate_contract(d, check_hashes=False))

    def test_unsafe_original_independence_is_rejected(self):
        d = load_contract()
        d["scope"]["original_edge_independence_assumed"] = True
        self.assertTrue(validate_contract(d, check_hashes=False))

    def test_remaining_five_work_packages_are_not_removed(self):
        d = load_contract()
        self.assertEqual(len(d["remaining_open_work"]), 5)
        d["remaining_open_work"].pop()
        self.assertTrue(validate_contract(d, check_hashes=False))

    def test_native_text_and_original_nine_pages(self):
        d = load_contract()
        self.assertEqual(d["pdf_reading"]["pages"], [12, 13, 19, 20, 21, 22, 23, 24, 25])
        self.assertTrue(d["pdf_reading"]["text_primary"])
        self.assertTrue(d["pdf_reading"]["original_page_crosschecked"])
        self.assertFalse(d["pdf_reading"]["new_ocr_performed"])

    def test_hash_tamper_rejected(self):
        d = load_contract()
        d["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(validate_contract(d))

    def test_source_inventory_or_path_escape_rejected(self):
        d = load_contract()
        d["source_pins"].pop()
        self.assertTrue(validate_contract(d, check_hashes=False))
        d = load_contract()
        d["source_pins"][0]["path"] = "../outside.md"
        self.assertTrue(validate_contract(d, check_hashes=False))

    def test_historical_cov1_unknown_c0_remains_a_snapshot(self):
        path = ROOT / "docs/method/theory/data/Sono_FMT_H1bCOV1_hypergraph_interface_v1.json"
        d = json.loads(path.read_text(encoding="utf-8"))
        self.assertIsNone(d["constants"]["source_C0_value"])
        self.assertEqual(d["children"]["COV1-CORE-C0"], "OPEN")
        self.assertEqual(load_contract()["next_gate"], "H1b-COV2 / DEP-R08")


if __name__ == "__main__":
    unittest.main()
