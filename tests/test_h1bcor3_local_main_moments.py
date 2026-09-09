"""Bounded exact algebra and provenance checks for theories 51/52."""
from copy import deepcopy
from fractions import Fraction as Q
import unittest

from source import h1bcor3_local_main_moments as m


class ScalarAndGeometryTests(unittest.TestCase):
    def test_scalar_endpoint_and_sono_coefficient_factor(self):
        r = m.finite_scalar_budget()
        self.assertTrue(r["exp_quarter_endpoint_integer_guard"])
        self.assertTrue(r["exp_endpoint_integer_guard"])
        self.assertEqual(r["coefficient_factor_times_ln5"], Q(5, 4))
        self.assertLess(r["count_error_composition"], r["count_error_target"])
        self.assertLess(r["full_degree_error_upper"], r["full_degree_error_target"])
        self.assertFalse(r["x_cert_ready"])

    def test_sigma_two_sides_and_one_removed_prime(self):
        for r in (Q(0), Q(1, 800*2000**2), Q(1, 100), Q(1, 10)):
            lo, hi = m.sigma_correction_enclosure(r)
            self.assertGreaterEqual(lo, 1-2*r)
            self.assertLessEqual(hi, 1+4*r)
            self.assertGreaterEqual(hi, (1+r)/(1-r))

    def test_scalar_boundaries_reject_floats_and_small_domain(self):
        for v in (1999, 2000.0, True, 10**6+1):
            with self.assertRaises(ValueError):
                m.finite_scalar_budget(v)
        with self.assertRaises(ValueError):
            m.sigma_correction_enclosure(Q(11, 100))

    def test_mean_error_remains_quadratic(self):
        for t in (Q(9, 10), Q(1), Q(11, 10), Q(2)):
            eps, d = Q(1, 1000), Q(1, 10000)
            direct = (1+eps)*t*t+d-2*(1-eps)*t+1
            self.assertEqual(m.centered_moment_envelope(t, eps, d), direct)
        self.assertEqual(m.centered_moment_envelope(Q(101, 100), 0, 0), Q(1, 10000))
        with self.assertRaises(ValueError):
            m.centered_moment_envelope(1, -1, 0)

    def test_finite_union_has_no_independence_requirement(self):
        self.assertEqual(m.finite_family_union(Q(1, 20), 3), Q(3, 20))
        self.assertEqual(m.finite_family_union(Q(1, 20), 21), 1)

    def test_postselected_or_unbounded_family_rejected(self):
        with self.assertRaises(ValueError):
            m.finite_family_union(Q(1, 20), 3, predeclared=False)
        for size in (0, True, 10**6+1):
            with self.assertRaises(ValueError):
                m.finite_family_union(Q(1, 20), size)

    def test_cross_prime_geometry_counts_shared_q_once(self):
        for i in range(2):
            for j in range(2):
                left, right = m.main_pair_points(17, 5, i, 7, j, (1, 3))
                self.assertEqual(set(left) & set(right), {17})
                self.assertEqual(len(set(left+right)), 3)

    def test_same_prime_off_diagonal_must_be_kept(self):
        left, right = m.main_pair_points(17, 5, 0, 5, 1, (1, 3))
        self.assertEqual(len(set(left+right)), 3)
        left2, right2 = m.main_pair_points(17, 5, 0, 5, 0, (1, 3))
        self.assertEqual(len(set(left2+right2)), 2)

    def test_invalid_geometry_is_not_certified(self):
        for args in ((17, 2, 0, 3, 0, (1, 3, 4)),
                     (17, 9, 0, 7, 1, (1, 3)),
                     (17, 5, 0, 7, 1, (1, 1))):
            with self.assertRaises(ValueError):
                m.main_pair_points(*args)

    def test_bad_p_mass_bound_uses_squared_deviation(self):
        eta = Q(1, 4)
        atoms = ((0, Q(1, 10)), (1, Q(4, 5)), (2, Q(1, 10)))
        deviation = sum(w*(u-1)**2 for u, w in atoms)
        probability = sum(w for u, w in atoms if abs(u-1) > eta)
        mass = sum(w*u for u, w in atoms if abs(u-1) > eta)
        self.assertLessEqual(mass, probability+deviation/eta)
        self.assertLessEqual(probability, deviation/eta**2)

    def test_conditioning_constant_algebra(self):
        b = Q(2000)
        e, d = 1/b**3, 1/(4*b**3)
        self.assertLessEqual((2*e+d)/(1-d), 3*e)
        self.assertLess((3*400+2)/b**3, 1/b**2)


class LocalCountTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = m.local_count_toy(
            q_values=(5, 7, 11, 13), primes=(5, 7),
            intervals=((5, 13, False), (5, 13, True),
                       (0, 7, False), (7, 13, False), (14, 20, False)))

    def test_exact_single_point_mean(self):
        for row in self.result["rows"]:
            self.assertEqual(row["mean"], row["exact_mean"])

    def test_second_moment_independent_oracles_match(self):
        for row in self.result["rows"]:
            self.assertEqual(row["second"], row["second_product"])

    def test_variance_and_chebyshev_envelopes(self):
        for row in self.result["rows"]:
            self.assertLessEqual(row["variance"], row["variance_envelope"])
            self.assertLessEqual(row["actual_failure"], row["chebyshev_upper"])
        self.assertLessEqual(self.result["family_actual_failure"],
                             self.result["family_union_upper"])

    def test_closed_lower_prime_adds_one_atom(self):
        opened, closed = self.result["rows"][:2]
        self.assertNotIn(5, opened["selected"])
        self.assertIn(5, closed["selected"])
        self.assertEqual(closed["mean"]-opened["mean"], Q(24, 35))

    def test_empty_interval_is_zero_without_division(self):
        row = self.result["rows"][-1]
        self.assertEqual((row["mean"], row["variance"], row["actual_failure"]), (0, 0, 0))

    def test_exact_disjoint_grid_clips_and_excludes(self):
        grid = m.disjoint_grid((2, 3, 5, 7, 11, 13, 17, 19),
                               y=20, cells=4, lower_cutoff=5, excluded=13)
        self.assertEqual(grid, ((), (7,), (11,), (17, 19)))
        self.assertEqual(sum(map(len, grid)), 4)
        boundary = m.disjoint_grid((5, 10, 15, 20), y=20, cells=4)
        self.assertEqual(boundary, ((5,), (10,), (15,), (20,)))

    def test_grid_exact_noninteger_endpoints(self):
        self.assertEqual(m.disjoint_grid((1, 2, 3, 4), y=Q(9, 2), cells=3),
                         ((1,), (2, 3), (4,)))
        with self.assertRaises(ValueError):
            m.disjoint_grid((1, 1), y=4, cells=2)

    def test_grid_interpolation_cover_and_inner_counts(self):
        values = tuple(range(1, 25))
        grid = m.disjoint_grid(values, y=24, cells=6)
        for left in range(25):
            for right in range(left+1, 25):
                n = sum(left < v <= right for v in values)
                delta = Q(right-left, 24)
                self.assertLessEqual(n, (delta+Q(2, 6))*24)
                self.assertGreaterEqual(n, max(delta-Q(2, 6), 0)*24)
        self.assertEqual(sum(map(len, grid)), 24)

    def test_local_work_limits_and_postselection(self):
        with self.assertRaises(ValueError):
            m.local_count_toy(q_values=(11,), intervals=((0, 20, False),),
                              primes=(97, 101), predeclared=True)
        with self.assertRaises(ValueError):
            m.local_count_toy(q_values=(11,), intervals=((0, 20, False),),
                              primes=(5,), predeclared=False)
        with self.assertRaises(ValueError):
            m.local_count_toy(q_values=(11,), intervals=((0.0, 20, False),), primes=(5,))


class MainMomentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prior = {n: Q(1, 12) for n in range(-3, 9)}
        cls.arguments = dict(p_priors={5: prior, 7: prior}, q_values=(11, 13, 17, 19),
                             offsets=(1, 3), primes=(11, 13), eta=Q(1, 10))
        cls.result = m.main_degree_toy(**cls.arguments)

    def test_first_and_second_independent_oracles(self):
        for row in self.result["rows"]:
            self.assertEqual(row["mean"], row["product_mean"])
            self.assertEqual(row["second"], row["product_second"])

    def test_omitting_same_p_is_detected(self):
        for row in self.result["rows"]:
            self.assertGreater(row["diagonal_second"], 0)
            self.assertGreater(row["second"], row["incorrect_second_without_same_p"])

    def test_diagonal_atom_bound(self):
        for row in self.result["rows"]:
            self.assertLessEqual(row["diagonal_second"], row["diagonal_trivial_upper"])
            self.assertLessEqual(row["diagonal_trivial_upper"], row["diagonal_atom_upper"])

    def test_centered_indicator_identity(self):
        for row in self.result["rows"]:
            self.assertEqual(row["centered_direct"], row["centered_from_moments"])

    def test_bad_p_mass_and_conditioned_enclosures(self):
        self.assertLessEqual(self.result["removed_mass_expectation"],
                             self.result["injection_mass_upper"])
        self.assertGreater(self.result["removed_mass_expectation"], 0)
        self.assertTrue(self.result["bad_p_seen"])

    def test_zero_denominator_not_used(self):
        result = m.main_degree_toy(p_priors={5: {0: 1}}, q_values=(11,),
                                   offsets=(1, 3), primes=(2,))
        self.assertTrue(result["zero_conditioning_mass_seen"])
        self.assertTrue(result["bad_p_seen"])

    def test_empty_modulus_set_deterministic(self):
        args = dict(self.arguments, primes=())
        r = m.main_degree_toy(**args)
        self.assertEqual(r["states"], 1)
        self.assertFalse(r["bad_p_seen"])
        for row in r["rows"]:
            self.assertEqual(row["second"], row["mean"]**2)

    def test_main_invalid_inputs_and_work_limit(self):
        for extra in (dict(reference_c=0), dict(eta=1.0),
                      dict(independent_uniform=False), dict(primes=(97, 101)),
                      dict(q_values=(5,)), dict(offsets=(1, 8))):
            with self.assertRaises(ValueError):
                m.main_degree_toy(**dict(self.arguments, **extra))

    def test_no_actual_or_formal_promotion(self):
        self.assertFalse(self.result["analytic_cutoff_verified_by_toy"])
        self.assertFalse(self.result["actual_prime_experiment_performed"])


class ContractTests(unittest.TestCase):
    def test_parent_overlay_is_current_but_broad_rows_stay_open(self):
        import json
        base = m.ROOT / "docs/method/theory/data"
        h1b = json.loads((base / "Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json").read_text(encoding="utf-8"))
        h1c = json.loads((base / "Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json").read_text(encoding="utf-8"))
        t1 = json.loads((base / "Sono_FMT_T1_proof_obligations_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(h1b["composition"]["remaining_actual_work_packages"], 6)
        self.assertTrue(h1b["composition"]["actual_main_degree_finite_moments_closed"])
        self.assertEqual(h1c["next_gate"]["id"], "H1b-COV1")
        self.assertEqual(h1c["successor_finite_local_main_moments"]["newly_closed_actual_work"],
                         ["DEP-R03", "DEP-R06"])
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(len(rows), 66)
        for key in ("SIV-07", "SIV-08", "SIV-09", "COV-08", "FIN-05"):
            self.assertEqual(rows[key]["status"], "HARD_BLOCKER")
        for key in ("COV-01", "COV-02"):
            self.assertEqual(rows[key]["status"], "RATE_MISSING")
            self.assertIn("PRE-covering", rows[key]["notes"])

    def test_parent_documents_current_header_not_stale(self):
        base = m.ROOT / "docs/method/theory"
        for name in ("12_Sono_FMT_T1_proof_obligation_ledger.md",
                     "14_Sono_FMT_H1b_Maynard_Proposition_6_1_constant_ledger.md",
                     "16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md"):
            header = (base / name).read_text(encoding="utf-8").split("\n\n", 2)[1]
            self.assertEqual(header, "## 2026-09-09 H1b-COR3 현재 상태")

    def test_live_contract_and_source_hashes(self):
        self.assertEqual(m.validate_contract(m.load_contract()), [])

    def test_cor3_scope_and_remaining_inventory(self):
        d = m.load_contract()
        self.assertEqual(d["newly_closed_actual_work"], ["DEP-R03", "DEP-R06"])
        self.assertEqual(d["remaining_open_work"], [f"DEP-R{i:02}" for i in range(7, 13)])
        self.assertEqual(d["next_gate"], "H1b-COV1 / DEP-R07")

    def test_false_root_or_source_rate_promotion_rejected(self):
        for key in ("x_cert_ready", "full_hypergraph_certified",
                    "source_sigma_b_minus_10_recovered", "arbitrarily_narrow_intervals"):
            d = deepcopy(m.load_contract())
            d["scope"][key] = not d["scope"][key]
            self.assertTrue(m.validate_contract(d, check_hashes=False))

    def test_missing_diagonal_or_changed_constant_rejected(self):
        d = deepcopy(m.load_contract())
        d["scope"]["same_p_all_index_pairs_preserved"] = False
        self.assertTrue(m.validate_contract(d, check_hashes=False))
        d = deepcopy(m.load_contract())
        d["constants"]["full_degree_absolute_error"] = "2/b^2"
        self.assertTrue(m.validate_contract(d, check_hashes=False))

    def test_source_pin_mismatch_detected(self):
        d = deepcopy(m.load_contract())
        d["source_pins"][0]["sha256"] = "0"*64
        self.assertTrue(any("hash mismatch" in issue for issue in m.validate_contract(d)))

    def test_predecessor_contract_not_rewritten(self):
        from source.h1bcor2_off_tuple_budget import load_contract, validate_contract
        d = load_contract()
        self.assertEqual(validate_contract(d), [])
        self.assertEqual(d["next_gate"], "H1b-COR3 / DEP-R03 then DEP-R06")
        self.assertIn("DEP-R03", d["remaining_open_work"])


if __name__ == "__main__":
    unittest.main()
