"""Independent regression checks for the H1c-1b.3 count bridge."""

from __future__ import annotations

import hashlib
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b3_endpoint_count_transfer import (
    PARTIAL_SUMMATION_INTEGRAL_SIGN,
    PRIME_POWER_CUMULATIVE_CONSTANT,
    centered_single_endpoint_atom,
    count_transfer_upper_from_components,
    crude_normalized_count_transfer_upper,
    structural_certificate,
    uniform_fixed_family_on_dyadic_interval,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b3_endpoint_count_transfer_v1.json"
)
PREDECESSOR = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b2_common_exceptional_remainder_v1.json"
)
T1_LEDGER = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_T1_proof_obligations_v1.json"
)


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % d for d in range(3, math.isqrt(value) + 1, 2))


def _totient(value: int) -> int:
    return sum(math.gcd(a, value) == 1 for a in range(1, value + 1))


def _prime_power_weight(value: int) -> Fraction:
    for prime in range(2, value + 1):
        if not _is_prime(prime):
            continue
        power = prime
        exponent = 1
        while power < value:
            power *= prime
            exponent += 1
        if power == value:
            return Fraction(1, exponent)
    return Fraction(0, 1)


def _pi1(y: Fraction, q: int | None = None, a: int = 0) -> Fraction:
    limit = y.numerator // y.denominator
    total = Fraction(0, 1)
    for n in range(2, limit + 1):
        if q is None or n % q == a % q:
            total += _prime_power_weight(n)
    return total


def _prime_count(
    lower: Fraction,
    upper: Fraction,
    *,
    lower_closed: bool,
    upper_closed: bool,
    q: int | None = None,
    a: int = 0,
) -> int:
    last = upper.numerator // upper.denominator + 1
    count = 0
    for n in range(2, last + 1):
        lower_ok = n >= lower if lower_closed else n > lower
        upper_ok = n <= upper if upper_closed else n < upper
        if lower_ok and upper_ok and _is_prime(n):
            if q is None or n % q == a % q:
                count += 1
    return count


def _von_mangoldt(value: int) -> mp.mpf:
    weight = _prime_power_weight(value)
    if not weight:
        return mp.mpf(0)
    # Lambda(p^k)=log(p), while pi_1 uses Lambda/log(p^k)=1/k.
    for prime in range(2, value + 1):
        if _is_prime(prime):
            power = prime
            while power < value:
                power *= prime
            if power == value:
                return mp.log(prime)
    raise AssertionError("prime-power decomposition not found")


def _psi(y: mp.mpf, q: int | None = None, a: int = 0) -> mp.mpf:
    limit = int(mp.floor(y))
    return mp.fsum(
        _von_mangoldt(n)
        for n in range(2, limit + 1)
        if q is None or n % q == a % q
    )


def _centered_psi(y: mp.mpf, q: int, a: int) -> mp.mpf:
    return _psi(y, q, a) - _psi(y) / _totient(q)


def _step_abel_integral(t: int, q: int, a: int) -> mp.mpf:
    total = mp.mpf(0)
    for left in range(t, 2 * t):
        right = left + 1
        coefficient = 1 / mp.log(left) - 1 / mp.log(right)
        total += _centered_psi(mp.mpf(left), q, a) * coefficient
    return total


class H1c1b3EndpointCountTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_abel_identity_has_plus_integral_and_wrong_sign_fails(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            t, q, a = 30, 5, 1
            phi = _totient(q)
            lhs = (
                mp.mpf(_pi1(Fraction(2 * t), q, a))
                - mp.mpf(_pi1(Fraction(t), q, a))
                - (
                    mp.mpf(_pi1(Fraction(2 * t)))
                    - mp.mpf(_pi1(Fraction(t)))
                )
                / phi
            )
            endpoint = _centered_psi(mp.mpf(2 * t), q, a) / mp.log(2 * t)
            endpoint -= _centered_psi(mp.mpf(t), q, a) / mp.log(t)
            integral = _step_abel_integral(t, q, a)
            self.assertTrue(mp.almosteq(lhs, endpoint + integral))
            self.assertFalse(mp.almosteq(lhs, endpoint - integral))
            self.assertEqual(PARTIAL_SUMMATION_INTEGRAL_SIGN, "+")
        finally:
            mp.mp.dps = old_dps

    def test_prime_power_bound_and_centered_increment_bound(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            for y in range(4, 401):
                total_error = _pi1(Fraction(y)) - _prime_count(
                    Fraction(0), Fraction(y), lower_closed=False, upper_closed=True
                )
                self.assertGreaterEqual(total_error, 0)
                self.assertLess(mp.mpf(total_error), 2 * mp.sqrt(y))
                for q in range(1, min(9, y) + 1):
                    for a in range(q):
                        if math.gcd(a, q) != 1:
                            continue
                        local_error = _pi1(Fraction(y), q, a) - _prime_count(
                            Fraction(0),
                            Fraction(y),
                            lower_closed=False,
                            upper_closed=True,
                            q=q,
                            a=a,
                        )
                        self.assertGreaterEqual(local_error, 0)
                        self.assertLess(mp.mpf(local_error), 2 * mp.sqrt(y))
            self.assertEqual(PRIME_POWER_CUMULATIVE_CONSTANT, 2)
        finally:
            mp.mp.dps = old_dps

    def test_half_open_endpoint_identity_and_one_atom_bound(self) -> None:
        cases = [
            Fraction(5),
            Fraction(11, 2),
            Fraction(11),
            Fraction(29),
            Fraction(30),
            Fraction(31, 2),
        ]
        for t in cases:
            for q in range(1, 8):
                phi = _totient(q)
                for a in range(q):
                    if math.gcd(a, q) != 1:
                        continue
                    half_local = _prime_count(
                        t, 2 * t, lower_closed=True, upper_closed=False, q=q, a=a
                    )
                    half_total = _prime_count(
                        t, 2 * t, lower_closed=True, upper_closed=False
                    )
                    open_local = _prime_count(
                        t, 2 * t, lower_closed=False, upper_closed=True, q=q, a=a
                    )
                    open_total = _prime_count(
                        t, 2 * t, lower_closed=False, upper_closed=True
                    )
                    delta_local = half_local - open_local
                    delta_total = half_total - open_total
                    self.assertEqual(
                        Fraction(half_local, 1) - Fraction(half_total, phi),
                        Fraction(open_local, 1)
                        - Fraction(open_total, phi)
                        + Fraction(delta_local, 1)
                        - Fraction(delta_total, phi),
                    )
                    self.assertLessEqual(
                        abs(Fraction(delta_local, 1) - Fraction(delta_total, phi)),
                        1,
                    )

        for sign in (-1, 1):
            for hit in (0, 1):
                for phi in range(1, 20):
                    self.assertLessEqual(
                        abs(centered_single_endpoint_atom(sign, hit, phi)), 1
                    )
        self.assertEqual(centered_single_endpoint_atom(0, 0, 7), 0)
        with self.assertRaises(ValueError):
            centered_single_endpoint_atom(0, 1, 7)

    def test_component_formula_matches_independent_recomputation(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 80
            result = count_transfer_upper_from_components(
                100,
                remainder_at_t_upper=11,
                remainder_at_2t_upper=13,
                abel_integral_upper=17,
                modulus_count=7,
                reciprocal_totient_sum=mp.mpf("3.25"),
            )
            expected_partial = 13 / mp.log(200) + 11 / mp.log(100) + 17
            expected_powers = 2 * mp.sqrt(200) * (7 + mp.mpf("3.25"))
            self.assertTrue(mp.almosteq(result.partial_summation, expected_partial))
            self.assertTrue(mp.almosteq(result.prime_power_removal, expected_powers))
            self.assertEqual(result.half_open_endpoint, 7)
            self.assertTrue(
                mp.almosteq(
                    result.total, expected_partial + expected_powers + 7
                )
            )
        finally:
            mp.mp.dps = old_dps

    def test_crude_normalized_envelope_matches_formula(self) -> None:
        old_dps = mp.mp.dps
        try:
            mp.mp.dps = 100
            log_t = mp.mpf(1000)
            rho = mp.mpf("1.25e-20")
            result = crude_normalized_count_transfer_upper(log_t, rho)
            expected_partial = rho * (
                1 / log_t + 2 / (log_t + mp.log(2)) + 1 / log_t**2
            )
            self.assertTrue(mp.almosteq(result.partial_summation, expected_partial))
            self.assertTrue(
                mp.almosteq(
                    result.prime_power_removal,
                    4 * mp.sqrt(2) * mp.exp(-log_t / 6),
                )
            )
            self.assertTrue(
                mp.almosteq(result.half_open_endpoint, mp.exp(-2 * log_t / 3))
            )
        finally:
            mp.mp.dps = old_dps

    def test_uniform_fixed_family_and_structural_fail_closed_flags(self) -> None:
        self.assertTrue(uniform_fixed_family_on_dyadic_interval())
        cert = structural_certificate()
        self.assertEqual(cert.sieve_dimension_r, 36)
        self.assertEqual(cert.maynard_integer_interval, "[T,2T)")
        self.assertEqual(cert.target_weight, "unweighted prime indicator 1_P(n)")
        self.assertEqual(cert.selected_linear_form, "identity L(n)=n")
        self.assertTrue(cert.same_fixed_modulus_family_through_abel_integral)
        self.assertEqual(cert.partial_summation_integral_sign, "+")
        self.assertTrue(cert.partial_summation_identity_closed)
        self.assertTrue(cert.prime_power_removal_closed)
        self.assertTrue(cert.half_open_endpoint_transfer_closed)
        self.assertTrue(cert.exact_total_prime_population_centered)
        self.assertTrue(cert.unweighted_prime_count_transfer_closed)
        for name in (
            "represented_prime_density_lower_bound_closed",
            "full_remainder_absorption_closed",
            "bordignon_constant_normalization_resolved",
            "hypothesis1_clause2_closed",
            "proposition92_closed",
            "siv_08_closed",
            "x_cert_ready",
            "actual_prime_experiment_performed",
        ):
            self.assertFalse(getattr(cert, name), name)
        with self.assertRaises(ValueError):
            uniform_fixed_family_on_dyadic_interval(35)

    def test_machine_contract_and_predecessor_history(self) -> None:
        self.assertEqual(
            self.contract["outcome"],
            "EXACT_HALF_OPEN_UNWEIGHTED_COUNT_TRANSFER_CLOSED_FULL_RATE_AND_DENSITY_OPEN",
        )
        self.assertTrue(self.contract["limits"]["exact_total_recentered"])
        self.assertFalse(self.contract["limits"]["hypothesis1_clause2_closed"])
        self.assertFalse(self.contract["limits"]["numerical_x_cert_ready"])
        predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        self.assertFalse(predecessor["limits"]["unweighted_prime_count_transfer_closed"])
        self.assertEqual(predecessor["next_gate"]["id"], "H1c-1b.3")
        t1 = json.loads(T1_LEDGER.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in t1["obligations"]}
        self.assertEqual(rows["SIV-08"]["status"], "HARD_BLOCKER")
        self.assertIn("H1c-1b.3", rows["SIV-08"]["notes"])

    def test_primary_source_hashes_are_fixed(self) -> None:
        for source in self.contract["source_registry"]:
            expected = source["sha256"]
            if expected == "SELF_HASHED_BY_REPOSITORY_TESTS":
                continue
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                expected,
                source["key"],
            )

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            count_transfer_upper_from_components(
                3,
                remainder_at_t_upper=0,
                remainder_at_2t_upper=0,
                abel_integral_upper=0,
                modulus_count=0,
                reciprocal_totient_sum=0,
            )
        count_transfer_upper_from_components(
            4,
            remainder_at_t_upper=0,
            remainder_at_2t_upper=0,
            abel_integral_upper=0,
            modulus_count=0,
            reciprocal_totient_sum=0,
        )
        with self.assertRaises(ValueError):
            count_transfer_upper_from_components(
                10,
                remainder_at_t_upper=-1,
                remainder_at_2t_upper=0,
                abel_integral_upper=0,
                modulus_count=0,
                reciprocal_totient_sum=0,
            )
        with self.assertRaises(TypeError):
            centered_single_endpoint_atom(1, 1, True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            crude_normalized_count_transfer_upper(mp.log(2), 0)


if __name__ == "__main__":
    unittest.main()
