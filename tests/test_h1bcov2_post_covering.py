"""Exact bounded tests for the H1b-COV2 successor contract."""
from copy import deepcopy
from fractions import Fraction as Q
import json
import unittest

from source import h1bcov2_post_covering as m


class EqualGridTests(unittest.TestCase):
    def test_width_enclosure_and_partition(self):
        for epsilon in (Q(1), Q(2, 3), Q(1, 2), Q(2, 7), Q(1, 101)):
            grid = m.equal_grid(epsilon)
            self.assertEqual(grid["cells"][0][0], 0)
            self.assertEqual(grid["cells"][-1][1], 1)
            self.assertEqual(sum((right-left for left, right in grid["cells"]), Q(0)), 1)
            self.assertGreaterEqual(grid["width"], epsilon/(2+epsilon))
            self.assertLessEqual(grid["width"], epsilon/2)

    def test_every_small_rational_interval_is_covered_with_endpoint_bound(self):
        points = [Q(i, 20) for i in range(21)]
        for epsilon in (Q(1), Q(1, 2), Q(1, 5)):
            for i in range(20):
                for j in range(i+1, 21):
                    result = m.cover_interval(points[i], points[j], epsilon)
                    cells = [result["cells"][index] for index in result["selected"]]
                    self.assertLessEqual(cells[0][0], points[i])
                    self.assertGreaterEqual(cells[-1][1], points[j])
                    self.assertLessEqual(result["covered_length"], result["sono_length_upper"])

    def test_crossing_interval_exposes_literal_one_cell_risk(self):
        result = m.cover_interval(Q(49, 100), Q(51, 100), Q(1, 2))
        self.assertEqual(result["count"], 4)
        self.assertEqual(len(result["selected"]), 2)
        self.assertGreater(len(result["selected"]), int(2*result["target_length"]/(Q(1, 2)))+1)
        self.assertLessEqual(result["covered_length"], result["target_length"]+2*result["width"])

    def test_invalid_or_unbounded_grid_is_rejected(self):
        for epsilon in (Q(0), Q(-1), Q(2), Q(1, 1_000_000), 0.5, True):
            with self.subTest(epsilon=epsilon), self.assertRaises(ValueError):
                m.equal_grid(epsilon)
        for endpoints in ((Q(1, 2), Q(1, 2)), (Q(3, 4), Q(1, 2)), (Q(-1), Q(1, 2))):
            with self.subTest(endpoints=endpoints), self.assertRaises(ValueError):
                m.cover_interval(*endpoints, Q(1, 2))


class FloorAndRestorationTests(unittest.TestCase):
    def test_floor_identity_at_and_between_powers(self):
        for ratio, expected_m in ((Q(5), 1), (Q(24), 1), (Q(25), 2), (Q(124), 2), (Q(125), 3)):
            # Pick A=1,c=1/80, so the supplied b is the exact ratio.
            result = m.density_floor(b=ratio, c_aux=Q(1, 80), A=Q(1))
            self.assertEqual(result["m"], expected_m)
            self.assertLessEqual(1, result["A_prime"])
            self.assertLess(result["A_prime"], 5)

    def test_floor_gate_and_float_inputs_rejected(self):
        with self.assertRaises(ValueError):
            m.density_floor(b=Q(4), c_aux=Q(1, 80), A=Q(1))
        for change in ({"b": 100}, {"c_aux": 0.01}, {"A": 1}):
            args = {"b": Q(100), "c_aux": Q(1, 80), "A": Q(1)}
            with self.assertRaises(ValueError):
                m.density_floor(**dict(args, **change))

    def test_actual_cell_restoration_beats_old_generic_shape(self):
        epsilon = Q(1, 10)
        width = m.equal_grid(epsilon)["width"]
        b, A = Q(10_000), Q(2)
        r_pre = Q(1, 100*b*b)
        value = m.restoration_upper(r_pre=r_pre, A=A, width=width, b=b)
        self.assertLess(value, Q(7, 1)/(A*epsilon*b))
        self.assertLess(value, Q(8000, 100))

    def test_composed_normalization_is_exact_product_bound(self):
        r, t, e = Q(1, 1000), Q(1, 100), Q(1, 200)
        bound = m.composed_relative_error(r_pre=r, covering_tolerance=t, restoration=e)
        for pre_sign in (-1, 1):
            for post_sign in (-1, 1):
                actual = abs((1+pre_sign*r)*(1+post_sign*(t+e))-1)
                self.assertLessEqual(actual, bound)

    def test_invalid_restoration_and_composition_rejected(self):
        with self.assertRaises(ValueError):
            m.restoration_upper(r_pre=Q(1), A=Q(1), width=Q(1, 2), b=Q(10))
        with self.assertRaises(ValueError):
            m.composed_relative_error(r_pre=Q(1, 10), covering_tolerance=Q(0), restoration=Q(0))


class ProbabilityAndSmoothTests(unittest.TestCase):
    def test_hypergraph_exponential_enclosures(self):
        result = m.hypergraph_relative_parameters(epsilon_hg=Q(1, 1000), xi=Q(1, 1000))
        self.assertLess(result["alpha_upper"], Q(3, 1000))
        self.assertLess(result["beta_upper"], Q(4, 1000))
        with self.assertRaises(ValueError):
            m.hypergraph_relative_parameters(epsilon_hg=Q(1, 10), xi=Q(1, 1000))

    def test_sequential_events_do_not_require_added_probability_or_independence(self):
        result = m.sequential_failure_bounds(
            c_aux=Q(1, 100_000), b=Q(100), a=Q(10_000), k=Q(10),
            family_size=5, precover_term=Q(1, 100), inner_v=Q(1, 100_000),
            tolerance=Q(1, 10),
        )
        self.assertTrue(result["sequential_existence"])
        self.assertLess(result["outer"], 1)
        self.assertLess(result["inner"], 1)
        self.assertNotIn("outer_plus_inner", result)

    def test_failed_stage_prevents_existence_claim(self):
        result = m.sequential_failure_bounds(
            c_aux=Q(1, 100_000), b=Q(100), a=Q(10_000), k=Q(10),
            family_size=100, precover_term=Q(2), inner_v=Q(1),
            tolerance=Q(1, 10),
        )
        self.assertFalse(result["sequential_existence"])

    def test_smooth_remainder_ratio_and_scalar_anchors(self):
        self.assertEqual(m.smooth_remainder_ratio_upper(log_b=Q(200), b=Q(10**6)), Q(1, 85_000))
        anchors = m.scalar_anchors()
        self.assertTrue(all(anchors.values()))
        self.assertTrue(anchors["ein_first_interval"])
        self.assertTrue(anchors["ein_two_piece"])
        self.assertTrue(anchors["theta_ein_coefficient"])
        with self.assertRaises(ValueError):
            m.smooth_remainder_ratio_upper(log_b=Q(2), b=Q(1))


class ContractTests(unittest.TestCase):
    def test_contract_and_source_pins(self):
        self.assertEqual(m.validate_contract(m.load_contract()), [])

    def test_exactly_r01_through_r08_closed(self):
        doc = m.load_contract()
        self.assertEqual(doc["closed_actual_work"], [f"DEP-R{i:02}" for i in range(1, 9)])
        self.assertEqual(doc["remaining_open_work"], [f"DEP-R{i:02}" for i in range(9, 13)])
        self.assertEqual(doc["children"]["DEP-R08"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")

    def test_no_threshold_or_coefficient_promotion(self):
        doc = m.load_contract()
        for key in (
            "final_A_epsilon_eta_instantiated", "same_sono_coefficient_budget_closed",
            "broad_sieve_weight_package_closed", "x_cert_ready",
            "threshold_calculator_ready", "actual_prime_experiment_performed",
            "independently_formally_verified",
        ):
            self.assertFalse(doc["scope"][key])
            changed = deepcopy(doc)
            changed["scope"][key] = True
            self.assertTrue(m.validate_contract(changed, check_hashes=False))

    def test_postselection_and_source_repair_cannot_be_reversed(self):
        doc = m.load_contract()
        changed = deepcopy(doc)
        changed["scope"]["postselection_or_uncountable_union_claimed"] = True
        self.assertTrue(m.validate_contract(changed, check_hashes=False))
        changed = deepcopy(doc)
        changed["source_repairs"][0]["source_result_preserved"] = False
        self.assertTrue(m.validate_contract(changed, check_hashes=False))

    def test_pin_tampering_and_path_escape(self):
        doc = m.load_contract()
        doc["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(m.validate_contract(doc))
        doc = m.load_contract()
        doc["source_pins"][0]["path"] = "../outside.pdf"
        self.assertTrue(m.validate_contract(doc))

    def test_parent_current_state_after_sync(self):
        base = m.ROOT / "docs/method/theory/data"
        h1b = json.loads((base / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json").read_text(encoding="utf-8"))
        h1c = json.loads((base / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json").read_text(encoding="utf-8"))
        t1 = json.loads((base / "Sono_FMT_T1_proof_obligations_v1.json").read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertTrue(h1b["composition"]["actual_post_covering_interval_remainder_closed"])
        self.assertEqual(h1b["composition"]["remaining_actual_work_packages"], 4)
        self.assertEqual(h1c["next_gate"]["id"], "DEP-R09")
        self.assertEqual(rows["COV-02"]["status"], "EXPLICIT")
        self.assertEqual(rows["COV-03"]["status"], "EXPLICIT")
        self.assertEqual(rows["COV-09"]["status"], "EXPLICIT")
        self.assertEqual(rows["COV-08"]["status"], "PARTIAL")
        self.assertEqual(rows["COV-11"]["status"], "PARTIAL")
        self.assertEqual(rows["COV-12"]["status"], "HARD_BLOCKER")
        for key in ("SIV-07", "SIV-08", "SIV-09", "FIN-05"):
            self.assertEqual(rows[key]["status"], "HARD_BLOCKER")


if __name__ == "__main__":
    unittest.main()
