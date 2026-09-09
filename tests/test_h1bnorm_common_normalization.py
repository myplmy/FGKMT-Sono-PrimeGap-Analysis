"""Independent finite fixtures for theory 47; no actual prime experiment."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import gcd, prod
from pathlib import Path
import hashlib
import json
import unittest

import mpmath as mp

from source.h1bnorm_common_normalization import (
    MIN_K, common_normalization_certificate, common_scales,
    dyadic_pi_ratio_envelope, exceptional_series_factor,
    integer_growth_witnesses, probability_relative_error, transfer_interval,
)

ROOT = Path(__file__).resolve().parents[1]
SHIFTS = (2, 8, 14)
PRIMES = tuple(n for n in range(2, 224)
               if all(n % d for d in range(2, n) if d*d <= n))


def roots(forms, s):
    return {n for n in range(s) if any((a*n+b) % s == 0 for a, b in forms)}


@lru_cache(None)
def series(forms, B, exclude_w=False):
    return prod((1-F(len(roots(forms, s)), s))*(1-F(1, s))**(-3)
                for s in PRIMES if s != B and not (exclude_w and s <= 18))


@lru_cache(None)
def coefficients(forms, B):
    """Independently build source lambda from all toy product<=23 vectors."""
    W_primes = tuple(s for s in PRIMES if s <= 18 and s != B)
    D = prod(F(s, s-1) for s in set(W_primes) | ({B} if B > 1 else set()))
    support = [(1, 1, 1)]
    for s in (19, 23):
        if s != B:
            for j in range(3):
                v = [1]*3
                v[j] = s
                support.append(tuple(v))
    out = {}
    for d in support:
        total = F(0)
        for r in support:
            if all(ri % di == 0 for ri, di in zip(r, d)):
                # Rational fixture profile; same function for each form family.
                profile = F(1, 1+sum(r))
                phi_omega = prod(s-len(roots(forms, s)) for s in (19, 23)
                                 if prod(r) % s == 0)
                total += D**3*series(forms, B, True)*profile/phi_omega
        out[d] = (-1 if prod(d) > 1 else 1)*prod(d)*total
    return out


def toy_weight(forms, n, B):
    if any(any((a*n+b) % s == 0 for a, b in forms)
           for s in PRIMES if s <= 18 and s != B):
        return F(0)
    return sum((v for d, v in coefficients(forms, B).items()
                if all((a*n+b) % di == 0 for (a, b), di in zip(forms, d))), F(0))**2


class CommonNormalizationTests(unittest.TestCase):
    def test_root_counts_all_small_residues_and_both_exceptional_primes(self):
        base = tuple((1, h) for h in SHIFTS)
        p, q = 101, 211
        lp = tuple((1, h*p) for h in SHIFTS)
        for i in range(3):
            tilde = tuple((1, 0) if j == i else (h-SHIFTS[i], q)
                          for j, h in enumerate(SHIFTS))
            for s in PRIMES:
                expected = len(roots(base, s))
                self.assertLess(expected, s)  # independent admissibility
                self.assertEqual(len(roots(lp, s)), 1 if s == p else expected)
                self.assertEqual(len(roots(tilde, s)), 1 if s == q else expected)

    def test_exact_truncated_series_ratios_with_B_exclusions(self):
        base = tuple((1, h) for h in SHIFTS)
        p, q = 101, 211
        lp = tuple((1, h*p) for h in SHIFTS)
        for B, i, wb in product((1, 2, p, q), range(3), (False, True)):
            tilde = tuple((1, 0) if j == i else (h-SHIFTS[i], q)
                          for j, h in enumerate(SHIFTS))
            self.assertEqual(series(lp, B, wb)/series(base, B, wb),
                             exceptional_series_factor(3, p, excluded_by_b=B == p))
            self.assertEqual(series(tilde, B, wb)/series(base, B, wb),
                             exceptional_series_factor(3, q, excluded_by_b=B == q))

    def test_lambda_and_nonzero_weight_square_transfer(self):
        base = tuple((1, h) for h in SHIFTS)
        p, q = 101, 211
        lp = tuple((1, h*p) for h in SHIFTS)
        nonzero = 0
        for B, i in product((1, 2, p, q), range(3)):
            alpha = exceptional_series_factor(3, p, excluded_by_b=B == p)
            beta = exceptional_series_factor(3, q, excluded_by_b=B == q)
            tilde = tuple((1, 0) if j == i else (h-SHIFTS[i], q)
                          for j, h in enumerate(SHIFTS))
            for d, value in coefficients(base, B).items():
                self.assertEqual(coefficients(lp, B)[d], alpha*value)
                self.assertEqual(coefficients(tilde, B)[d], beta*value)
            w1, w2 = toy_weight(lp, q-SHIFTS[i]*p, B), toy_weight(tilde, p, B)
            self.assertEqual(w1, (alpha/beta)**2*w2)
            if w2:
                nonzero += 1
                self.assertNotEqual(w1, alpha/beta*w2)  # missing square detected
        self.assertGreater(nonzero, 0)

    def test_exception_factor_validation_and_uniform_bound(self):
        for k in range(1, 8):
            for p in PRIMES:
                if p > 2*k*k:
                    ratio = exceptional_series_factor(k, p)
                    self.assertGreaterEqual(ratio, 1)
                    self.assertLessEqual(ratio, 1+F(4*k, 2*p-1))
        for args in ((True, 11), (3, 18), (3.0, 101)):
            with self.assertRaises(ValueError):
                exceptional_series_factor(*args)
        with self.assertRaises(ValueError):
            exceptional_series_factor(3, 101, excluded_by_b=1)

    def test_common_scales_direct_identities_and_tau_multiplication(self):
        for k, b in product((2, 3, 5), (F(1, 2), F(4, 5), F(1))):
            s, r, a, I, J, X, Y = map(F, (7, 3, 10, 2, 1, 100, 1000))
            c = common_scales(k=k, b=b, series=s, log_r=r, log_x=a,
                              integral_i=I, integral_j=J, x=X, y=Y)
            self.assertEqual(c["total_mass"], 2*Y*b**(-k)*s*r**k*I)
            self.assertEqual(c["prime_moment"], b**(1-k)*s*r**(k+1)*J*X/(2*a))
            self.assertEqual(c["off_tuple_reference_without_E"], 2*c["M0"]*X*Y/a)
            self.assertEqual(c["tau"], 2*c["M0"]*a**k)
            self.assertNotEqual(c["tau"], 2*c["M0"]/a**k)

    def test_common_scale_fixture_refuses_actual_dimension_and_floats(self):
        args = dict(k=3, b=1, series=1, log_r=1, log_x=1,
                    integral_i=1, integral_j=1, x=100, y=1000)
        for update in ({"k": MIN_K}, {"b": 0.5}, {"series": 0}, {"b": 2}):
            with self.assertRaises(ValueError):
                common_scales(**(args | update))

    def test_dyadic_RS_rational_envelopes(self):
        for a, log_two in product((F(10), F(101, 10), F(100), F(10**6)),
                                  (F(1, 100), F(69, 100), F(999, 1000))):
            low, high = dyadic_pi_ratio_envelope(a, log_two)
            self.assertGreaterEqual(low, 1-3/a)
            self.assertLessEqual(high, 1+3/a)
        for a, c in ((9, F(1, 2)), (10, 0), (10, 1), (10.0, F(1, 2))):
            with self.assertRaises(ValueError):
                dyadic_pi_ratio_envelope(a, c)

    def test_transfer_brackets_weighted_sum_not_constant_alpha(self):
        beta, alphas, values = F(11, 10), (F(1), F(6, 5), F(21, 20)), (F(2), F(3), F(5))
        K = sum(values)/beta
        actual = sum((a/beta)**2*v for a, v in zip(alphas, values))/K
        lo, hi = transfer_interval(F(1, 5), 0)
        self.assertLessEqual(lo, actual)
        self.assertGreaterEqual(hi, actual)
        self.assertNotEqual(actual, sum(values)/K)  # cannot drop conversion

    def test_B0_deletion_and_probability_error_at_boundary_values(self):
        for m in (10, 100, 10**6):
            k, t = m*m, F(1, m)
            lo, hi = transfer_interval(F(1, k), t+F(3, k), deleted_relative=F(1, k))
            self.assertGreaterEqual(lo, 1-2*t)
            self.assertLessEqual(hi, 1+2*t)
            err = probability_relative_error(F(4, k), 2*t)
            self.assertLessEqual(err, 3*t)
            for d1, d2 in product((-F(4, k), F(4, k)), (-2*t, 2*t)):
                self.assertLessEqual(abs((1+d2)/(1+d1)-1), err)

    def test_nonnegative_deletion_and_invalid_error_contracts(self):
        self.assertEqual(transfer_interval(0, 0, deleted_relative=2), (F(0), F(1)))
        for e, d, atom in ((-1, 0, 0), (0, 1, 0), (0, 0, -1)):
            with self.assertRaises(ValueError):
                transfer_interval(e, d, deleted_relative=atom)
        for d1, d2 in ((1, 0), (-1, 0), (0, -1)):
            with self.assertRaises(ValueError):
                probability_relative_error(d1, d2)

    def test_pointwise_divisor_tuple_bound_including_zero_form(self):
        for k, R in product((1, 2, 3), (2, 5, 9)):
            tuples = [v for v in product(range(1, R+1), repeat=k) if prod(v) <= R]
            H = sum((F(1, n) for n in range(1, R+1)), F(0))
            self.assertLessEqual(len(tuples), R*H**(k-1))
            self.assertTrue(all(0 % d == 0 for v in tuples for d in v))

    def test_source_child_cutoff_and_integer_witnesses(self):
        for k in (MIN_K, MIN_K+1, 10**201):
            self.assertTrue(all(integer_growth_witnesses(k).values()))
        with self.assertRaises(ValueError):
            integer_growth_witnesses(MIN_K-1)

    def test_minimum_scalar_and_scope_flags(self):
        c = common_normalization_certificate(k=MIN_K)
        self.assertTrue(all(ok for _, ok in c.checks))
        self.assertTrue(c.common_filtered_moments_closed)
        self.assertTrue(c.fixed_x_probability_inputs_closed)
        self.assertTrue(c.b0_single_prime_deletion_closed)
        self.assertFalse(c.u_depends_only_on_k_certified)
        self.assertFalse(c.literal_unfiltered_transfer_certified)
        self.assertFalse(c.general_proposition61_closed)
        self.assertFalse(c.downstream_failure_probability_closed)
        self.assertFalse(c.full_good_sieve_weight_closed)
        self.assertFalse(c.x_cert_ready)
        self.assertFalse(c.actual_prime_experiment_performed)
        self.assertLess(c.log_probability_relative_upper, c.log_target_error)

    def test_exact_upper_bin_and_large_dimension_restore_precision(self):
        old = mp.mp.dps
        for k in (MIN_K, 10**201):
            c = common_normalization_certificate(k=k, log_outer_half=F(2*(k+1)**5-1, 2))
            self.assertTrue(all(ok for _, ok in c.checks))
        self.assertEqual(mp.mp.dps, old)

    def test_invalid_bin_float_filter_and_h_range_are_rejected(self):
        for kwargs in (
            {"k": MIN_K-1}, {"k": True}, {"k": MIN_K, "log_outer_half": MIN_K**5-1},
            {"k": MIN_K, "log_outer_half": (MIN_K+1)**5},
            {"k": MIN_K, "log_outer_half": 1.0},
            {"k": MIN_K, "weight_definition": "unfiltered"},
            {"k": MIN_K, "log_h_constant": F(MIN_K**5+1, 4)},
            {"k": MIN_K, "log_h_constant": -1},
        ):
            with self.assertRaises(ValueError):
                common_normalization_certificate(**kwargs)

    def test_exact_h_range_endpoint(self):
        c = common_normalization_certificate(k=MIN_K, log_h_constant=F(MIN_K**5, 4))
        self.assertTrue(all(ok for _, ok in c.checks))

    def test_frozen_sources_and_predecessors(self):
        contract = json.loads((ROOT/"docs/method/theory/data/Sono_FMT_H1bNORM_common_normalization_v1.json").read_text(encoding="utf-8"))
        for item in contract["immutable_sources"]+contract["proof_dependency_snapshots"]:
            with self.subTest(path=item["path"]):
                self.assertEqual(hashlib.sha256((ROOT/item["path"]).read_bytes()).hexdigest(), item["sha256"])
        self.assertFalse(contract["x_cert_ready"])
        self.assertFalse(contract["u_depends_only_on_k_certified"])
        for field in ("theory", "review", "helper", "test", "parent_ledger"):
            self.assertTrue((ROOT/contract[field]).is_file(), field)


if __name__ == "__main__":
    unittest.main()
