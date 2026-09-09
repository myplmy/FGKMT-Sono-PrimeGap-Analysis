"""Finite interface checks; these do not prove the source C0 or a prime theorem."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
import json
import unittest

from source import h1bcov1_hypergraph_interface as m


class ResidueCapTests(unittest.TestCase):
    arguments = {
        "q_values": (7, 17, 19, 29, 37, 47, 59, 67, 79, 97),
        "prime": 5, "offsets": (1, 3),
        "law": ((2, Q(1, 4)), (4, Q(1, 2)), (0, Q(1, 4))),
        "excluded": (19, 37),
    }

    @classmethod
    def setUpClass(cls):
        cls.result = m.residue_cap_toy(**cls.arguments)

    def test_cap_removes_positive_mass_and_never_truncates_in_place(self):
        r = self.result
        self.assertEqual(r["removed_degree_mass"], Q(3, 2))
        for row in r["rows"]:
            self.assertIn(row["capped"], (row["full"], frozenset()))
        self.assertLessEqual(r["removed_degree_mass"], 2*r["off_degree_mass"])

    def test_cap_boundary_equality_is_kept(self):
        row = next(row for row in self.result["rows"] if row["n"] == 4)
        self.assertEqual(len(row["full"]), 4)
        self.assertEqual(row["capped"], row["full"])

    def test_q_degree_loss_equals_edge_mass_loss(self):
        self.assertEqual(self.result["sum_degree_difference"], self.result["removed_degree_mass"])
        for q in self.arguments["q_values"]:
            self.assertLessEqual(self.result["cap_degree"][q], self.result["full_degree"][q])

    def test_projected_support_has_actual_residue_equality(self):
        for edge, n in self.result["witnesses"].items():
            self.assertEqual(edge, frozenset(q for q in self.result["retained"] if (q-n) % 5 == 0))

    def test_empty_projection_uses_zero_residue(self):
        result = m.residue_cap_toy(**dict(self.arguments, excluded=(19, 29, 59, 79)))
        self.assertEqual(result["witnesses"], {frozenset(): 0})
        self.assertTrue(all(q % 5 for q in result["retained"]))

    def test_tuple_only_does_not_preserve_actual_survivor_lower_bound(self):
        result = m.residue_cap_toy(q_values=(7, 17, 37), prime=5,
                                   offsets=(1, 3), law=((2, 1),))
        row = result["rows"][0]
        self.assertEqual(len(set((7, 17, 37))-row["main"]), 1)
        self.assertEqual(len(set((7, 17, 37))-row["full"]), 0)

    def test_bad_mass_tally_needs_off_tuple_points(self):
        row = self.result["rows"][0]
        self.assertEqual((len(row["full"]), len(row["main"]), len(row["off"])), (6, 2, 4))
        self.assertGreater(len(row["full"]), 2*len(row["main"]))

    def test_invalid_prime_or_zero_witness_conditions_rejected(self):
        for replacement in (dict(q_values=(5, 7)), dict(prime=4),
                            dict(offsets=(1, 1)), dict(excluded=(11,)),
                            dict(law=((2, Q(1, 2)),)), dict(law=((2, 1.0),)),
                            dict(law=((2, 1), (2, Q(0))))):
            with self.assertRaises(ValueError):
                m.residue_cap_toy(**dict(self.arguments, **replacement))

    def test_cap_is_not_an_actual_or_core_verification(self):
        self.assertFalse(self.result["actual_prime_experiment_performed"])
        self.assertFalse(self.result["source_C0_verified"])


class PartitionTests(unittest.TestCase):
    def test_independent_labels_match_separate_exact_expectation(self):
        result = m.partition_toy(((Q(1, 3), Q(1, 2)), (Q(1, 4), Q(1, 5)),
                                   (Q(2, 3), Q(1, 7))),
                                  (Q(1, 2), Q(1, 4)), Q(1, 10))
        self.assertEqual(result["states"], 27)
        self.assertEqual(result["mass"], 1)
        self.assertEqual(result["mean"], result["target"])
        self.assertLessEqual(result["family_failure"], result["union_upper"])

    def test_unused_probability_zero_is_allowed(self):
        result = m.partition_toy(((1,), (Q(1, 3),)), (Q(1, 2), Q(1, 2)), Q(1, 10))
        self.assertEqual(result["mass"], 1)
        self.assertEqual(result["mean"], result["target"])

    def test_partition_assumptions_and_size_guard(self):
        for args in (
            (((1,),), (Q(3, 4), Q(3, 4)), Q(1, 10)),
            (((1,), (1, 1)), (Q(1, 2),), Q(1, 10)),
            (((1,),), (Q(1, 2),), 0),
            (((1,),)*8, (Q(1, 5),)*4, Q(1, 10)),
        ):
            with self.assertRaises(ValueError):
                m.partition_toy(*args)
        with self.assertRaises(ValueError):
            m.partition_toy(((1,),), (Q(1, 2),), 1, independent=False)

    def test_C_lower_bound_gives_disjoint_probability_budget(self):
        # C/(ln5)>=5/4; use exact lower endpoint to upper-bound the sum.
        for stages in (1, 2, 4, 10, 20):
            probabilities = tuple(Q(4, 5**j) for j in range(1, stages+1))
            self.assertEqual(sum(probabilities), 1-Q(1, 5**stages))
            self.assertLess(sum(probabilities), 1)


class RecurrenceTests(unittest.TestCase):
    def test_rational_log_exp_and_derivative_bounds(self):
        d = m.scalar_diagnostics()
        self.assertGreater(d["log5_lower"], Q(8, 5))
        self.assertLess(d["log5_upper"], Q(13, 8))
        self.assertLess(d["exp_tenth_upper"], Q(10, 9))
        self.assertLess(d["derivative_upper"], 3)
        self.assertLess(d["degree_ratio_upper"], 2)
        self.assertLess(d["xi_m_le_4_upper"], Q(1, 10))
        self.assertLess(d["xi_m_ge_5_upper"], Q(1, 10))
        self.assertLess(d["exception_coefficient_upper"], 8000)
        self.assertTrue(d["partition_positive_integer_guard"])
        self.assertTrue(all(d["core_gate_polynomial_guards"]))
        self.assertFalse(d["source_C0_verified"])
        self.assertFalse(d["x_cert_ready"])

    def test_taylor_exact_sign_reciprocal_and_zero(self):
        self.assertEqual(m.exp_enclosure(0), (1, 1))
        lo, hi = m.exp_enclosure(Q(1, 3))
        self.assertEqual(m.exp_enclosure(Q(-1, 3)), (1/hi, 1/lo))
        self.assertLess(lo, hi)
        with self.assertRaises(ValueError):
            m.exp_enclosure(2)
        with self.assertRaises(ValueError):
            m.exp_enclosure(0.1)

    def test_recurrence_point_enclosures_respect_analytic_step_bound(self):
        for z in (Q(-1, 10), Q(-1, 100), Q(0), Q(1, 100), Q(1, 10)):
            for eta in (Q(-1, 2000), Q(0), Q(1, 2000)):
                lo, hi = m.recurrence_step_enclosure(z, eta)
                target = 3*abs(z)+Q(2, 2000)
                self.assertGreaterEqual(lo, -target)
                self.assertLessEqual(hi, target)

    def test_exact_recurrence_error_majorant(self):
        for b, stages in ((2000, 4), (3125, 5), (10**6, 8)):
            error = Q(0)
            for j in range(1, stages+1):
                error = 3*error+Q(2, b)
                self.assertEqual(error, Q(3**j-1, b))
            self.assertLess(error, Q(1, 10))
        with self.assertRaises(ValueError):
            m.recurrence_step_enclosure(Q(11, 100), 0)

    def test_post_cap_and_exception_arithmetic(self):
        b = 2000
        self.assertLess(Q(1203, b**3), Q(1, b*b))
        self.assertLess(Q(8000, b*b), 1)
        # The inherited exceptional bound is not silently <= N/b^2.
        self.assertGreater(Q(8000, b*b), Q(1, b*b))
        for k, stages in ((1, 1), (3, 5), (100, 20)):
            r, size = 2*k, 4*k*stages+2
            self.assertEqual(size-2*r*stages, 2)


class SubsetAndRestorationTests(unittest.TestCase):
    def test_ordered_pair_moment_and_diagonal(self):
        outcomes = list(product((0, 1), repeat=8))
        mass = Q(1, len(outcomes))
        mean = sum((mass*sum(row) for row in outcomes), Q(0))
        second = sum((mass*sum(row)**2 for row in outcomes), Q(0))
        pair = sum((mass*sum(row)*(sum(row)-1) for row in outcomes), Q(0))
        self.assertEqual(second, pair+mean)
        self.assertGreater(second, pair)
        failure = sum((mass for row in outcomes if abs(Q(sum(row), 4)-1) > Q(3, 4)), Q(0))
        upper = m.subset_failure_bound(single_error=0, pair_error=0,
                                      rho=Q(1, 2), count=8, tolerance=Q(3, 4))
        self.assertLessEqual(failure, upper)
        self.assertLess(upper, 1)

    def test_single_point_uniformity_does_not_replace_pair_control(self):
        # All 16 survive or none survive: each point marginal=1/2, pair relative error=1.
        bad_upper = m.subset_failure_bound(single_error=0, pair_error=0,
                                          rho=Q(1, 2), count=16, tolerance=Q(9, 10))
        good_upper = m.subset_failure_bound(single_error=0, pair_error=1,
                                           rho=Q(1, 2), count=16, tolerance=Q(9, 10))
        self.assertLess(bad_upper, 1)
        self.assertEqual(good_upper, 1)

    def test_fixed_subset_not_simultaneous_postselected_subset(self):
        v = frozenset(range(10))
        surviving_laws = (frozenset(range(5)), frozenset(range(5, 10)))
        for point in v:
            self.assertEqual(sum(Q(int(point in w), 2) for w in surviving_laws), Q(1, 2))
        for w in surviving_laws:
            selected_after_outcome = w
            self.assertEqual(len(selected_after_outcome & w), 5)
            self.assertNotEqual(Q(1, 2)*len(selected_after_outcome), 5)

    def test_restoration_bound_exhaustive_small_counts(self):
        for original in range(1, 13):
            for removed in range(original):
                retained = original-removed
                for rho in (Q(1, 2), Q(1, 5), Q(1)):
                    extra = m.restoration_error(original_count=original,
                                                removed_count=removed, rho=rho)
                    for z in range(retained+1):
                        tolerance = abs(Q(z, 1)/(rho*retained)-1)
                        for outside in range(removed+1):
                            error = abs(Q(z+outside, 1)/(rho*original)-1)
                            self.assertLessEqual(error, tolerance+extra)

    def test_forgetting_deleted_vertices_can_hide_all_error(self):
        rho, retained, deleted = Q(1, 2), 8, 2
        z, outside = 4, 2
        self.assertEqual(Q(z)/(rho*retained), 1)
        self.assertNotEqual(Q(z+outside)/(rho*(retained+deleted)), 1)

    def test_invalid_and_empty_subset_not_divided_by_zero(self):
        for change in (dict(count=0), dict(rho=0), dict(single_error=-1),
                       dict(tolerance=0), dict(rho=0.5)):
            args = dict(single_error=0, pair_error=0, rho=Q(1, 2), count=5, tolerance=Q(1, 2))
            with self.assertRaises(ValueError):
                m.subset_failure_bound(**dict(args, **change))
        with self.assertRaises(ValueError):
            m.restoration_error(original_count=5, removed_count=5, rho=Q(1, 2))


class ContractTests(unittest.TestCase):
    def test_live_contract_and_source_pins(self):
        self.assertEqual(m.validate_contract(m.load_contract()), [])

    def test_core_is_open_and_conditional_claim_is_labeled(self):
        doc = m.load_contract()
        self.assertEqual(doc["children"]["COV1-CORE-C0"], "OPEN")
        self.assertEqual(doc["children"]["COV1-MOMENT-TRANSFER"], "CONDITIONAL_ON_SOURCE_C0_GATE")
        self.assertEqual(len(doc["remaining_open_work"]), 6)
        self.assertIsNone(doc["constants"]["source_C0_value"])

    def test_false_core_or_threshold_promotion_rejected(self):
        for key in ("source_C0_numerically_known", "x_cert_ready", "full_hypergraph_certified"):
            d = deepcopy(m.load_contract())
            d["scope"][key] = True
            self.assertTrue(m.validate_contract(d, check_hashes=False))
        d = deepcopy(m.load_contract())
        d["remaining_open_work"].remove("DEP-R07")
        self.assertTrue(m.validate_contract(d, check_hashes=False))

    def test_missing_support_or_exception_conditions_rejected(self):
        for key in ("full_residue_edges", "cap_drops_whole_edge", "exception_cost_restored",
                    "fixed_subset_not_all_subsets"):
            d = deepcopy(m.load_contract())
            d["scope"][key] = False
            self.assertTrue(m.validate_contract(d, check_hashes=False))

    def test_error_addends_and_C0_cannot_be_silently_changed(self):
        d = deepcopy(m.load_contract())
        d["constants"]["source_C0_value"] = 1
        self.assertTrue(m.validate_contract(d, check_hashes=False))
        d = deepcopy(m.load_contract())
        d["errata"][0]["corrected_formula"] = "product_without_plus"
        self.assertTrue(m.validate_contract(d, check_hashes=False))

    def test_pin_tampering_and_path_escape(self):
        d = deepcopy(m.load_contract())
        d["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(any("hash mismatch" in s for s in m.validate_contract(d)))
        d["source_pins"][0]["path"] = "../outside.pdf"
        self.assertTrue(any("escapes root" in s for s in m.validate_contract(d)))

    def test_predecessor_keeps_original_hash_and_correct_sum(self):
        from source import h1bcor3_local_main_moments as predecessor
        d = predecessor.load_contract()
        self.assertEqual(predecessor.validate_contract(d), [])
        self.assertEqual(d["next_gate"], "H1b-COV1 / DEP-R07")
        self.assertEqual(d["constants"]["full_degree_failure_upper"],
                         m.load_contract()["errata"][0]["corrected_formula"])

    def test_parent_current_status_not_broad_promotion(self):
        base = m.ROOT / "docs/method/theory/data"
        h1c = json.loads((base / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json").read_text(encoding="utf-8"))
        t1 = json.loads((base / "Sono_FMT_T1_proof_obligations_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(h1c["next_gate"]["id"], "H1b-COV2")
        rows = {r["id"]: r for r in t1["obligations"]}
        self.assertEqual(len(rows), 66)
        for key in ("COV-08", "COV-11", "SIV-07", "SIV-08", "SIV-09"):
            self.assertEqual(rows[key]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
