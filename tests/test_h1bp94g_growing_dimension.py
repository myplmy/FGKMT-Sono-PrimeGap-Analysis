"""Independent bounded algebra and regression for the growing P94 child."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import gcd, prod
from pathlib import Path
import unittest
from unittest.mock import patch

import mpmath as mp

from source.h1bp91a_unweighted_moment import w_filter
from source.h1b2a1_proposition94_euler import (
    canonical_ratio_local_certificate, exact_star_denominator,
)
from source.h1bp94g_growing_dimension import (
    MIN_K, EXACT_COARSE_MULTIPLIER, WEIGHT_DEFINITION,
    growing_p94_certificate, integer_growth_witnesses, selberg_square_majorant,
    shift_geometry,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT/"docs/method/theory/data/Sono_FMT_H1bP94g_growing_dimension_v1.json"


class GrowingP94Tests(unittest.TestCase):
    def test_shift_endpoints_independently_enumerated(self):
        for X, Y in [(13, 55), (Fraction(27, 2), Fraction(221, 4)),
                     (Fraction(129, 10), Fraction(301, 10))]:
            g = shift_geometry(X, Y, p=11, h=1, shifts=(2, 6))
            qs = [q for q in range(1, 100) if X < q <= Y]
            ts = [q+g.q_to_t_offset for q in qs]
            self.assertEqual(ts, list(range(g.local_t+1, 2*g.local_t+1)))
            self.assertEqual(len(ts), g.open_integer_count)
            self.assertEqual(len(ts)+1, g.closed_integer_count)
            self.assertNotIn(g.local_t, ts)
            self.assertIn(2*g.local_t, ts)

    def test_adding_lower_endpoint_is_not_an_identity(self):
        g = shift_geometry(13, 55, p=11, h=1, shifts=(2, 6))
        f = lambda t: t*t+1
        open_sum = sum(f(t) for t in range(g.local_t+1, 2*g.local_t+1))
        closed_sum = sum(f(t) for t in range(g.local_t, 2*g.local_t+1))
        self.assertEqual(closed_sum-open_sum, f(g.local_t))
        self.assertGreater(closed_sum, open_sum)

    def test_support_removal_only_upper_bound(self):
        for h in [-20, -1, 0, 1, 7, 20]:
            X, Y, p = 13, 55, 11
            g = shift_geometry(X, Y, p=p, h=h, shifts=(2, 6))
            original = lambda n: (n*n+7)*int(all(gcd(n+hi*p, 30) == 1 for hi in (2, 6)))
            truncated = sum(original(q-h*p)*int(abs(q-h*p) <= Y) for q in range(X+1, Y+1))
            raw_open = sum(original(q-h*p) for q in range(X+1, Y+1))
            shifted = sum(original(t+g.extra_intercept-h*p)
                          for t in range(g.local_t+1, 2*g.local_t+1))
            self.assertEqual(raw_open, shifted)
            self.assertLessEqual(truncated, raw_open)
            if abs(h) == 20:
                self.assertEqual(truncated, 0)
                self.assertGreater(raw_open, 0)

    def test_shift_filter_and_discriminant_from_form_coefficients(self):
        for p, h in product([11, 17], [-7, 0, 1, 9]):
            g = shift_geometry("13.2", "80.7", p=p, h=h, shifts=(2, 6, 12))
            a0, b0 = g.extra_form
            delta_direct = abs(a0)*prod(abs(a0*b-a*b0) for a, b in g.shifted_forms)
            self.assertEqual(delta_direct, g.discriminant)
            self.assertEqual(delta_direct, p**3*prod(abs(hi-h) for hi in (2, 6, 12)))
            for t in range(g.local_t+1, 2*g.local_t+1):
                q = t+g.extra_intercept
                vals = [q+(hi-h)*p for hi in (2, 6, 12)]
                self.assertEqual([a*t+b for a, b in g.shifted_forms], vals)
                self.assertEqual(w_filter(t, g.shifted_forms, 30),
                                 int(all(gcd(v, 30) == 1 for v in vals)))

    def test_shift_invalid_and_degenerate_inputs(self):
        for kwargs in [{"h": 2}, {"shifts": (2, 2)}, {"p": True}, {"h": 1.0},
                       {"shifts": ()}]:
            args = dict(p=11, h=1, shifts=(2, 6))
            args.update(kwargs)
            with self.assertRaises(ValueError):
                shift_geometry(13, 55, **args)
        for X, Y in [(2, 2), (3, 2), (1, 12), (2.1, 12), (2, "nan")]:
            with self.assertRaises(ValueError):
                shift_geometry(X, Y, p=11, h=1, shifts=(2, 6))

    def test_selberg_square_for_rough_integers(self):
        # All selected divisors are <7; every 7-rough n has only divisor 1 here.
        coefficients = ((1, Fraction(3, 2)), (2, Fraction(-7, 3)),
                        (3, Fraction(2)), (5, Fraction(-1, 2)), (6, Fraction(3)))
        for n in range(1, 150):
            rough = int(all(n % p for p in [2, 3, 5, 7]))
            majorant = selberg_square_majorant(n, coefficients)
            self.assertGreaterEqual(majorant, rough)
            if rough:
                self.assertEqual(majorant, 1)

    def test_selberg_requires_nonzero_normalization(self):
        for coefficients in [(), ((1, Fraction(0)),), ((2, Fraction(1)),),
                             ((1, Fraction(1)), (1, Fraction(2)))]:
            with self.assertRaises(ValueError):
                selberg_square_majorant(17, coefficients)

    def test_exact_integer_discrepancy_open_and_closed(self):
        for T in [3, 7, 17]:
            for lower in [T, T+1]:
                for q in range(1, 25):
                    counts = [sum(n % q == a for n in range(lower, 2*T+1))
                              for a in range(q)]
                    N = 2*T+1-lower
                    self.assertTrue(all(abs(Fraction(v)-Fraction(N, q)) <= 1 for v in counts))

    def test_signed_quadratic_square_symmetry_without_factor_two(self):
        specs = [(5, 3), (11, 4)]
        states = list(product(*[range(slots) for _, slots in specs]))
        weights = [Fraction((-1)**j*(j+1), j+2) for j in range(len(states))]
        exact = Fraction()
        for i, r in enumerate(states):
            for j, s in enumerate(states):
                local = prod(Fraction(p-1 if r[t] == s[t] else -1, (p-m)**2)
                             for t, (p, m) in enumerate(specs))
                exact += weights[i]*weights[j]*local
        diagonal_upper = sum((a*a for a in weights), Fraction())*prod(
            Fraction(p+m-2, (p-m)**2) for p, m in specs
        )
        self.assertLessEqual(exact, diagonal_upper)

    def test_exact_euler_ratios_against_unexpanded_factors(self):
        for k in [36, 100]:
            p = 2*k*k+17
            for omega in [0, 1, k//2, k]:
                for collision in [False, True]:
                    star = omega if collision else omega+1
                    lhs = (1+Fraction(omega, 1)/exact_star_denominator(p, star))/(1+Fraction(omega, p-omega))
                    rhs = canonical_ratio_local_certificate(
                        k, p, omega, collides_with_extra_form=collision
                    )
                    self.assertEqual(lhs, rhs.exact_factor)
                    self.assertTrue(rhs.upper_bound_verified)

    def test_exact_unit_multiplier_and_polynomial_witnesses(self):
        for k in [200, 201, 10**3, 10**6, MIN_K]:
            self.assertTrue(all(integer_growth_witnesses(k).values()))
        expected = ((1+Fraction(1, 100))/(1-Fraction(1, 100))**2
                    *8*(1+Fraction(1, 100))/9+Fraction(1, 100))
        self.assertEqual(EXACT_COARSE_MULTIPLIER, expected)
        self.assertLess(expected, 1)

    def test_bad_dimension_and_filter_fail_closed(self):
        for k in [True, 1.0, MIN_K-1]:
            with self.assertRaises(ValueError):
                growing_p94_certificate(k=k)
        for definition in [None, False, "fgkmt_literal_unfiltered"]:
            with self.assertRaises(ValueError):
                growing_p94_certificate(k=MIN_K, weight_definition=definition)
        for L in [MIN_K**5-1, (MIN_K+1)**5, Fraction(2*MIN_K**5-1, 2), "nan", 1.0, True]:
            with self.assertRaises(ValueError):
                growing_p94_certificate(k=MIN_K, log_outer_half=L)

    def test_h_range_bound_is_exact_and_not_implicit(self):
        L = MIN_K**5
        for H in [-1, Fraction(L, 4)+1, Fraction(L, 4)+Fraction(1, 2), "nan", True, 0.0]:
            with self.assertRaises(ValueError):
                growing_p94_certificate(k=MIN_K, log_h_constant=H)
        c = growing_p94_certificate(k=MIN_K, log_h_constant=Fraction(L, 4))
        self.assertEqual(c.log_h_constant_exact, Fraction(L, 4))
        self.assertTrue(all(v for _, v in c.checks))

    def test_actual_corner_upper_bin_and_later_k(self):
        for k in [MIN_K, 10**220]:
            for L in [k**5, (k+1)**5-1]:
                c = growing_p94_certificate(k=k, log_outer_half=L)
                self.assertTrue(all(v for _, v in c.checks))
                self.assertLess(c.total_with_distribution_budget_upper, 1)
                self.assertLessEqual(c.log_distribution_ratio_upper, c.log_distribution_certificate)
                self.assertLess(c.log_off_tuple_relative_upper, c.log_off_tuple_target_lower)
                self.assertEqual(c.uniform_integer_multiplier, 1)

    def test_never_calls_exponential_dimension_legacy_evaluator(self):
        with patch("source.h1b2a3_proposition94_composition.proposition94_actual_composition_certificate",
                   side_effect=AssertionError("legacy O(k)/2**k evaluator must not run")):
            c = growing_p94_certificate(k=MIN_K)
            self.assertTrue(c.filtered_growing_p94_child_closed)

    def test_precision_restored_and_root_flags_not_promoted(self):
        previous = mp.mp.dps
        try:
            mp.mp.dps = 15
            c = growing_p94_certificate(k=MIN_K)
            self.assertGreaterEqual(c.working_dps, 1060)
            self.assertEqual(mp.mp.dps, 15)
            self.assertEqual(c.weight_definition, WEIGHT_DEFINITION)
            for field in ["literal_unfiltered_transfer_certified", "general_proposition94_closed",
                          "common_normalization_closed", "full_good_sieve_weight_closed",
                          "x_cert_ready", "actual_prime_experiment_performed", "lean_verified"]:
                self.assertFalse(getattr(c, field), field)
        finally:
            mp.mp.dps = previous

    def test_contract_hashes_and_parent_scope(self):
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(data["minimum_k"], str(MIN_K))
        self.assertEqual(data["bounds"]["uniform_integer_multiplier"], 1)
        self.assertTrue(data["w_filter_required"])
        self.assertFalse(data["x_cert_ready"])
        for entry in data["immutable_sources"]+data["proof_dependency_snapshots"]:
            self.assertEqual(sha256((ROOT/entry["path"]).read_bytes()).hexdigest(), entry["sha256"])
        parent = json.loads((ROOT/data["parent_ledger"]).read_text(encoding="utf-8"))
        self.assertFalse(parent["numerical_x_cert_ready"])
        row = next(x for x in parent["obligations"] if x["id"] == "H1B-P94")
        self.assertEqual(row["status"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")


if __name__ == "__main__":
    unittest.main()
