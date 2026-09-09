"""Independent bounded algebra/regression tests for H1b-P91a."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import gcd, lcm
from pathlib import Path
import unittest

import mpmath as mp

from source.h1bp91a_unweighted_moment import (
    MIN_K, OFF_DIAGONAL_FACTOR, WEIGHT_DEFINITION, exact_shift_count,
    integer_growth_witnesses, unweighted_local_euler_ratios,
    unweighted_moment_certificate, w_filter,
)
from source.h1bp92a_identity_prime_moment import identity_prime_moment_certificate

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT/"docs/method/theory/data/Sono_FMT_H1bP91a_unweighted_moment_v1.json"


class H1bP91aTests(unittest.TestCase):
    def test_exact_contiguous_discrepancy(self):
        for start in [-17, 0, 13]:
            for n_count in range(1, 21):
                for q in range(1, 32):
                    actual = [0]*q
                    for n in range(start, start+n_count):
                        actual[n % q] += 1
                    self.assertTrue(all(
                        abs(Fraction(v)-Fraction(n_count, q)) <= 1 for v in actual
                    ))

    def test_tuple_divisor_sum_majorant(self):
        for z, j in product([8, 12], [1, 2, 3]):
            count = 0
            for values in product(range(1, z+1), repeat=j):
                n = 1
                for value in values:
                    n *= value
                count += int(n <= z)
            harmonic = sum((Fraction(1, a) for a in range(1, z+1)), Fraction())
            self.assertLessEqual(count, z*harmonic**(j-1))

    def test_p91_matrix_from_divisor_membership_not_copied_from_p92(self):
        for p, slots in [(5, 2), (7, 3), (11, 4)]:
            for i, j in product(range(slots), repeat=2):
                entry = Fraction()
                for has_d, has_e in product([False, True], repeat=2):
                    if i != j and has_d and has_e:
                        continue
                    d, e = (p if has_d else 1), (p if has_e else 1)
                    mu_product = (-1)**(has_d+has_e)
                    entry += mu_product*Fraction(d*e, lcm(d, e))
                self.assertEqual(entry, p-1 if i == j else -1)
            self.assertEqual((p-1)-(slots-1), p-slots)

    def test_multi_prime_row_sums_independent_enumeration(self):
        specs = [(5, 2), (7, 3)]
        states = list(product(*[range(w) for _, w in specs]))
        for r in states:
            row_sum = 0
            for s in states:
                cell = 1
                for i, (p, _) in enumerate(specs):
                    cell *= p-1 if r[i] == s[i] else -1
                row_sum += cell
            self.assertEqual(row_sum, (5-2)*(7-3))

    def test_euler_and_residue_cancellation_exact(self):
        for p in [5, 7, 11, 13, 17]:
            for omega in range(1, min(5, p)):
                diagonal, sliced = unweighted_local_euler_ratios(p, omega)
                self.assertEqual(diagonal, 1)
                self.assertEqual(sliced, 1+Fraction(omega*(omega-1), p*(p-omega)))
                for k in [omega, omega+2]:
                    # W-good residue density times the normalization at p.
                    lhs = Fraction(p-omega, p)*Fraction(p, p-1)**k
                    rhs = (1-Fraction(omega, p))*(1-Fraction(1, p))**(-k)
                    self.assertEqual(lhs, rhs)

    def test_missing_filter_is_not_implied_by_lambda_support(self):
        # Only d=(1,1) is used: coprime to W, yet raw weight is nonzero on bad n.
        forms = ((1, 0), (1, 2))
        raw = [9 for n in range(30)]
        filtered = [9*w_filter(n, forms, 30) for n in range(30)]
        self.assertEqual(sum(raw), 270)
        self.assertEqual(sum(filtered), 27)
        self.assertEqual(w_filter(0, forms, 30), 0)
        self.assertNotEqual(raw, filtered)

    def test_shift_bijection_and_filter_exact(self):
        forms = ((1, 22), (1, 66), (1, 132))
        for Y in [Fraction(10), Fraction(21, 2), Fraction(109, 10), Fraction(111, 10)]:
            T, N, residual = exact_shift_count(Y)
            m = T//2
            original = list(range(-m, m+1))
            shifted = list(range(T, 2*T+1))
            self.assertEqual(original, [n-3*m for n in shifted])
            self.assertEqual(len(original), N)
            self.assertLessEqual(abs(residual), 1)
            translated = tuple((a, b-3*m*a) for a, b in forms)
            for n in shifted:
                self.assertEqual(w_filter(n, translated, 30), w_filter(n-3*m, forms, 30))
            # An arbitrary nonconstant toy weight catches a missed endpoint.
            toy = lambda n: (n*n+3)*w_filter(n, translated, 30)
            self.assertEqual(
                sum(toy(n) for n in shifted),
                sum(toy(n+3*m) for n in original),
            )

    def test_prime_slice_filter_equal_for_coprime_p_and_q(self):
        h = [2, 6, 12]
        for p, q, i in product([31, 37, 41], [43, 47, 53], range(3)):
            self.assertEqual(gcd(p*q, 30), 1)
            original = tuple((1, hj*p) for hj in h)
            transformed = tuple((1, 0) if j == i else (hj-h[i], q)
                                for j, hj in enumerate(h))
            self.assertEqual(
                w_filter(q-h[i]*p, original, 30),
                w_filter(p, transformed, 30),
            )

    def test_prime_slice_requires_coprimality(self):
        # p=3 is not coprime to W: replacing q by p can change the filter.
        self.assertEqual(w_filter(11, ((1, 0), (1, 6)), 30), 1)
        self.assertEqual(w_filter(3, ((1, 0), (2, 11)), 30), 0)

    def test_bad_integer_and_weight_contract_inputs_fail_closed(self):
        for value in [True, 36.0, 35]:
            with self.assertRaises(ValueError):
                integer_growth_witnesses(value)
        for value in [False, 2.5, "nan", "0", Fraction(1, 2)]:
            with self.assertRaises(ValueError):
                exact_shift_count(value)
        for definition in [False, None, "fgkmt_literal_unfiltered"]:
            with self.assertRaises(ValueError):
                unweighted_moment_certificate(k=MIN_K, weight_definition=definition)
            with self.assertRaises(ValueError):
                identity_prime_moment_certificate(k=MIN_K, weight_definition=definition)
        for p, w in [(True, 1), (7, 0), (7, 7), (3.0, 1)]:
            with self.assertRaises(ValueError):
                unweighted_local_euler_ratios(p, w)

    def test_uniform_polynomial_witnesses(self):
        for k in [36, 37, 100, 10**4, MIN_K]:
            self.assertTrue(all(integer_growth_witnesses(k).values()))
        self.assertEqual(OFF_DIAGONAL_FACTOR, 1_384_128)

    def test_exact_bin_negative_edges(self):
        k = MIN_K
        for value in [k**5-1, (k+1)**5, Fraction(2*k**5-1, 2), "nan", 1.0, True]:
            with self.assertRaises(ValueError):
                unweighted_moment_certificate(k=k, log_outer_half=value)

    def test_actual_corner_upper_bin_and_later_k(self):
        for k in [MIN_K, 10**220]:
            for L in [k**5, (k+1)**5-1]:
                c = unweighted_moment_certificate(k=k, log_outer_half=L)
                self.assertTrue(all(v for _, v in c.checks))
                self.assertEqual(c.log_outer_half_exact, L)
                self.assertLess(c.log_relative_error_upper, c.log_relative_majorant)
                self.assertLess(c.log_symmetric_relative_majorant, c.log_relative_target_lower)
                self.assertLessEqual(c.log_distribution_ratio_upper, c.log_distribution_certificate)
                self.assertTrue(c.filtered_actual_p91_closed)
                self.assertEqual(c.weight_definition, WEIGHT_DEFINITION)

    def test_precision_restoration_and_no_root_promotion(self):
        previous = mp.mp.dps
        try:
            mp.mp.dps = 15
            c = unweighted_moment_certificate(k=MIN_K)
            self.assertGreaterEqual(c.working_dps, 1060)
            self.assertEqual(mp.mp.dps, 15)
            for flag in [
                "literal_unfiltered_transfer_certified", "general_proposition91_closed",
                "growing_k_proposition94_closed", "common_normalization_closed",
                "full_good_sieve_weight_closed", "x_cert_ready",
                "actual_prime_experiment_performed", "lean_verified",
            ]:
                self.assertFalse(getattr(c, flag), flag)
        finally:
            mp.mp.dps = previous

    def test_contract_hashes_and_scope(self):
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(data["minimum_k"], str(MIN_K))
        self.assertTrue(data["w_filter_required"])
        self.assertFalse(data["literal_unfiltered_transfer_certified"])
        self.assertFalse(data["x_cert_ready"])
        for item in data["immutable_sources"]+data["proof_dependency_snapshots"]:
            self.assertEqual(sha256((ROOT/item["path"]).read_bytes()).hexdigest(), item["sha256"])
        parent = json.loads((ROOT/data["parent_ledger"]).read_text(encoding="utf-8"))
        row = next(o for o in parent["obligations"] if o["id"] == "H1B-P91")
        self.assertEqual(row["status"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")
        self.assertIn("W-filter", " ".join(row["explicit_parts"]))
        self.assertFalse(parent["numerical_x_cert_ready"])


if __name__ == "__main__":
    unittest.main()
