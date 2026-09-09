"""Independent rational/toy and scalar regression tests for H1b-P92a."""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import unittest

import mpmath as mp

from source.h1bp92a_identity_prime_moment import (
    ACTUAL_IDENTITY_MOMENT_MIN_K,
    INTEGRAL_COMPARISON_MIN_K,
    ONE_STEP_MULTIPLIER_UPPER,
    SCALAR_REMAINDER_MULTIPLIER_UPPER,
    elementary_rational_witnesses,
    exact_dimension_bin,
    identity_local_euler_ratios,
    identity_prime_moment_certificate,
    integer_growth_witnesses,
    integral_comparison_certificate,
)
from source.h1b1b2d_rfold_smooth_package import (
    PROFILE_N, PROFILE_N2, PROFILE_W, PROFILE_W2, PROFILE_NW,
    profile_norm_certificate,
)
from source.h1b1b2d1a1_scalar_remainder import scalar_remainder_constant_certificate

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/method/theory/data/Sono_FMT_H1bP92a_identity_prime_moment_v1.json"


def is_prime_toy(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


class IdentityPrimeMomentTests(unittest.TestCase):
    def test_rational_elementary_and_polynomial_witnesses(self):
        self.assertTrue(all(elementary_rational_witnesses().values()))
        for k in [36, 37, 100, 10**50, 10**200, 10**220]:
            self.assertTrue(all(integer_growth_witnesses(k).values()))

    def test_exact_dimension_endpoints_not_rounded(self):
        k = ACTUAL_IDENTITY_MOMENT_MIN_K
        self.assertEqual(exact_dimension_bin(k, k**5), k**5)
        self.assertEqual(exact_dimension_bin(k, (k+1)**5-1), (k+1)**5-1)
        self.assertEqual(exact_dimension_bin(k, str(k**5)), k**5)
        for bad in [k**5-1, Fraction(2*k**5-1, 2), (k+1)**5]:
            with self.assertRaises(ValueError):
                exact_dimension_bin(k, bad)

    def test_float_bool_and_invalid_inputs_fail_closed(self):
        for k in [True, 35, 36.0, 10**200-1]:
            with self.assertRaises(ValueError):
                identity_prime_moment_certificate(k=k)
        for L in [True, 1.0, mp.mpf(10)**1000, "nan", "inf", "0", "-1"]:
            with self.assertRaises(ValueError):
                exact_dimension_bin(36, L)
        with self.assertRaises(ValueError):
            integral_comparison_certificate(INTEGRAL_COMPARISON_MIN_K-1)

    def test_integral_comparison_tail_and_ratio_constants(self):
        for k in [10**50, 10**80, 10**200]:
            c = integral_comparison_certificate(k)
            self.assertTrue(c.gate_passed)
            self.assertGreater(c.one_minus_cantelli_probability_lower, Fraction(1, 2))
            self.assertEqual(c.i_f1_over_i_f_upper, 2)
            self.assertEqual(c.j_f1_over_j_f_upper, 2)
            self.assertEqual(c.i_f2_over_i_f_upper, 4*k*k)
            self.assertEqual(c.j_f2_over_j_f_upper, 8*k*k)
            self.assertEqual(c.slice_over_j_f_upper, 16*k**4)
            self.assertFalse(c.numerical_integration_performed)

    def test_coarse_profile_norm_covers_existing_exact_profiles(self):
        with mp.workdps(100):
            for k in [36, 100, 10**50, 10**200]:
                bound = 10*(mp.mpf(k)*mp.log(k))**2
                for profile in [PROFILE_N, PROFILE_N2, PROFILE_W, PROFILE_W2, PROFILE_NW]:
                    self.assertLessEqual(
                        profile_norm_certificate(k, profile).scaled_omega_upper_bound, bound
                    )

    def test_existing_scalar_constants_fit_coarse_bounds(self):
        with mp.workdps(100):
            c = scalar_remainder_constant_certificate()
            self.assertLess(c.weighted_lemma83_multiplier, ONE_STEP_MULTIPLIER_UPPER)
            self.assertLess(c.common_c_y, SCALAR_REMAINDER_MULTIPLIER_UPPER)

    def test_local_euler_cancellation_independent_products(self):
        for p in [q for q in range(3, 80) if is_prime_toy(q)]:
            for omega in range(1, min(8, p-1)+1):
                diagonal, sliced = identity_local_euler_ratios(p, omega)
                self.assertEqual(diagonal, 1)
                self.assertEqual(
                    sliced, 1 + Fraction((omega-1)**2, (p-omega)*(p-1))
                )
                # Evaluate the unsimplified k-dimensional local factors.
                k = max(omega, 3)
                singular = Fraction(p-omega, p) * Fraction(p, p-1)**k
                smooth = (1+Fraction(omega-1, p-omega))*Fraction(p-1, p)**(k-1)
                self.assertEqual(singular*smooth, diagonal)
                w_residue = Fraction(p-omega, p-1)*Fraction(p, p-1)**(k-1)
                self.assertEqual(w_residue, singular)

    def test_quadratic_row_sum_by_independent_slot_enumeration(self):
        # A prime with omega roots has omega-1 slots after removing identity.
        for p, omega in [(11, 3), (17, 5), (29, 7)]:
            slots = list(range(omega-1))
            for chosen in slots:
                row = [p-2 if s == chosen else -1 for s in slots]
                self.assertEqual(sum(row), p-omega)
        # Tensor product over two distinct primes: sum over all actual s.
        entries = [(11, 3), (17, 4)]
        states = list(product(*(range(omega-1) for _, omega in entries)))
        for r in states:
            row_sum = 0
            for s in states:
                term = 1
                for j, (p, _) in enumerate(entries):
                    term *= p-2 if r[j] == s[j] else -1
                row_sum += term
            self.assertEqual(row_sum, (11-3)*(17-4))

    def test_fixed_modulus_pair_multiplicity_exact(self):
        # For one prime, d/e are absent or assigned to one allowed slot.
        # Their lcm must contain p, and nonempty assignments must be compatible.
        for slots in [1, 2, 3, 5]:
            assignments = [None] + list(range(slots))
            legal = [
                (d, e) for d, e in product(assignments, repeat=2)
                if (d is not None or e is not None)
                and (d is None or e is None or d == e)
            ]
            self.assertEqual(len(legal), 3*slots)
        # Independent local choices multiply, with coefficient one.
        self.assertEqual(3*2 * 3*4, 72)

    def test_harmonic_divisor_majorant_toy(self):
        # Sum over n of tau_j(n)/n == sum_{prod tuple <= z} 1/prod tuple.
        z = 12
        for j in [1, 2, 3]:
            exact_sum = Fraction()
            for values in product(range(1, z+1), repeat=j):
                n = 1
                for value in values:
                    n *= value
                if n <= z:
                    exact_sum += Fraction(1, n)
            harmonic = sum((Fraction(1, n) for n in range(1, z+1)), Fraction())
            self.assertLessEqual(exact_sum, harmonic**j)
            with mp.workdps(60):
                self.assertLess(
                    mp.mpf(exact_sum.numerator)/exact_sum.denominator,
                    (1+mp.log(z))**j,
                )

    def test_endpoint_weight_atom_independent_toy(self):
        # A deliberately nonconstant weight makes count-atom substitution fail.
        for T in [Fraction(5), Fraction(6), Fraction(11, 2), Fraction(13)]:
            closed = [n for n in range(2, 40) if T <= n <= 2*T and is_prime_toy(n)]
            opened = [n for n in range(2, 40) if T < n <= 2*T and is_prime_toy(n)]
            atom = int(T.denominator == 1 and is_prime_toy(T.numerator))
            weight = lambda n: 3*n*n+7
            self.assertEqual(len(closed)-len(opened), atom)
            weighted_atom = atom*weight(T.numerator) if atom else 0
            self.assertEqual(
                sum(weight(n) for n in closed)-sum(weight(n) for n in opened),
                weighted_atom,
            )
            if atom:
                self.assertNotEqual(weighted_atom, atom)

    def test_square_bypass_with_signed_residual(self):
        for A, B, eps in product(
            [Fraction(0), Fraction(1, 3), Fraction(5)],
            [Fraction(0), Fraction(1, 5), Fraction(7)],
            [Fraction(0), Fraction(1, 9), Fraction(2)],
        ):
            for direction in [Fraction(-1), Fraction(-1, 3), Fraction(1, 2), Fraction(1)]:
                Z = A + direction*eps*B
                self.assertLessEqual(abs(Z*Z-A*A), 2*eps*A*B + eps*eps*B*B)

    def test_uniform_actual_corner_and_later_dimension(self):
        for k in [10**200, 10**220]:
            c = identity_prime_moment_certificate(k=k)
            self.assertTrue(all(value for _, value in c.checks))
            self.assertLessEqual(c.log_main_relative_error_upper, c.log_relative_target)
            self.assertLessEqual(c.log_distribution_ratio_upper, c.log_distribution_certificate)
            self.assertLessEqual(c.log_weight_atom_ratio_upper, c.log_atom_certificate)
            self.assertLessEqual(c.log_prime_count_atom_ratio_upper, c.log_atom_certificate)
            self.assertEqual((c.relative_multiplier, c.additive_multiplier), (1, 1))
            self.assertTrue(c.actual_identity_application_closed)
            self.assertTrue(c.lower_endpoint_weight_closed)
            self.assertTrue(c.conditional_on_actual_form_construction)

    def test_dimension_bin_top_and_half_integer_are_safe(self):
        k = 10**200
        for L in [(k+1)**5-1, Fraction(2*k**5+1, 2)]:
            c = identity_prime_moment_certificate(k=k, log_t=L)
            self.assertEqual(c.log_t_exact, L)
            self.assertTrue(all(value for _, value in c.checks))

    def test_increased_internal_precision_does_not_promote_roots(self):
        old = mp.mp.dps
        try:
            mp.mp.dps = 15
            c = identity_prime_moment_certificate(k=10**200)
            self.assertGreaterEqual(c.working_dps, 1060)
            for name in [
                "general_proposition92_closed", "proposition61_closed",
                "siv_07_closed", "siv_08_closed", "siv_09_closed",
                "x_cert_ready", "actual_prime_experiment_performed", "lean_verified",
            ]:
                self.assertFalse(getattr(c, name), name)
            self.assertEqual(mp.mp.dps, 15)
        finally:
            mp.mp.dps = old

    def test_contract_hashes_scope_and_current_parent(self):
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(data["minimum_k"], str(ACTUAL_IDENTITY_MOMENT_MIN_K))
        for item in data["immutable_sources"] + data["proof_dependency_snapshots"]:
            self.assertEqual(sha256((ROOT/item["path"]).read_bytes()).hexdigest(), item["sha256"])
        for flag in ["x_cert_ready", "actual_prime_experiment_performed", "lean_verified"]:
            self.assertFalse(data[flag])
        parent = json.loads((ROOT/data["parent_ledger"]).read_text(encoding="utf-8"))
        row = next(o for o in parent["obligations"] if o["id"] == "H1B-P92")
        self.assertEqual(row["status"], "ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT")
        self.assertFalse(parent["numerical_x_cert_ready"])


if __name__ == "__main__":
    unittest.main()
