"""Regression tests for the actual FGKMT endpoint correction."""

from __future__ import annotations

import hashlib
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from source.h1c1b3_endpoint_count_transfer import (
    crude_normalized_count_transfer_upper,
)
from source.h1c1b3r1_fgkmt_endpoint_correction import (
    FGKMT_HYPOTHESIS_INTERVAL,
    FGKMT_OUTER_PRIME_INTERVAL,
    SOURCE_PRIME_INTERVAL,
    centered_lower_endpoint_atom,
    closed_count_transfer_upper_from_components,
    crude_normalized_closed_count_transfer_upper,
    endpoint_correction_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction_v1.json"
)


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % divisor for divisor in range(3, math.isqrt(value) + 1, 2))


def _totient(value: int) -> int:
    return sum(math.gcd(a, value) == 1 for a in range(1, value + 1))


def _prime_count(
    lower: Fraction,
    upper: Fraction,
    *,
    lower_closed: bool,
    upper_closed: bool,
    q: int | None = None,
    a: int = 0,
) -> int:
    count = 0
    for n in range(2, upper.numerator // upper.denominator + 2):
        if not _is_prime(n):
            continue
        if lower_closed:
            lower_ok = Fraction(n) >= lower
        else:
            lower_ok = Fraction(n) > lower
        if upper_closed:
            upper_ok = Fraction(n) <= upper
        else:
            upper_ok = Fraction(n) < upper
        if lower_ok and upper_ok and (q is None or n % q == a % q):
            count += 1
    return count


class FgkmtEndpointCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exact_open_closed_to_closed_identity(self) -> None:
        for t in (Fraction(5), Fraction(11, 2), Fraction(11), Fraction(30)):
            for q in range(1, 8):
                phi_q = _totient(q)
                for a in range(q):
                    if math.gcd(a, q) != 1:
                        continue
                    source_local = _prime_count(
                        t, 2 * t, lower_closed=False, upper_closed=True, q=q, a=a
                    )
                    source_total = _prime_count(
                        t, 2 * t, lower_closed=False, upper_closed=True
                    )
                    target_local = _prime_count(
                        t, 2 * t, lower_closed=True, upper_closed=True, q=q, a=a
                    )
                    target_total = _prime_count(
                        t, 2 * t, lower_closed=True, upper_closed=True
                    )
                    delta_local = target_local - source_local
                    delta_total = target_total - source_total
                    self.assertIn(delta_total, (0, 1))
                    self.assertEqual(
                        Fraction(target_local) - Fraction(target_total, phi_q),
                        Fraction(source_local)
                        - Fraction(source_total, phi_q)
                        + Fraction(delta_local)
                        - Fraction(delta_total, phi_q),
                    )
                    self.assertLessEqual(
                        abs(Fraction(delta_local) - Fraction(delta_total, phi_q)), 1
                    )

    def test_centered_atom_exact_arithmetic(self) -> None:
        for hit in (0, 1):
            for phi_q in range(1, 20):
                self.assertLessEqual(abs(centered_lower_endpoint_atom(hit, phi_q)), 1)
        with self.assertRaises(ValueError):
            centered_lower_endpoint_atom(2, 5)
        with self.assertRaises(TypeError):
            centered_lower_endpoint_atom(True, 5)  # type: ignore[arg-type]

    def test_corrected_bound_has_same_size_but_different_semantics(self) -> None:
        old = crude_normalized_count_transfer_upper(1000, "1.25e-20")
        new = crude_normalized_closed_count_transfer_upper(1000, "1.25e-20")
        self.assertTrue(mp.almosteq(old.total, new.total))
        self.assertTrue(
            mp.almosteq(old.half_open_endpoint, new.lower_endpoint_addition)
        )
        composed = closed_count_transfer_upper_from_components(
            100,
            remainder_at_t_upper=11,
            remainder_at_2t_upper=13,
            abel_integral_upper=17,
            modulus_count=7,
            reciprocal_totient_sum="3.25",
        )
        self.assertEqual(composed.lower_endpoint_addition, 7)
        self.assertTrue(
            mp.almosteq(
                composed.partial_summation,
                13 / mp.log(200) + 11 / mp.log(100) + 17,
            )
        )

    def test_fail_closed_certificate_distinguishes_three_intervals(self) -> None:
        cert = endpoint_correction_certificate()
        self.assertEqual(cert.source_interval, SOURCE_PRIME_INTERVAL)
        self.assertEqual(cert.fgkmt_hypothesis_interval, FGKMT_HYPOTHESIS_INTERVAL)
        self.assertEqual(cert.fgkmt_outer_prime_interval, FGKMT_OUTER_PRIME_INTERVAL)
        self.assertEqual(cert.maynard_original_interval, "[T,2T)")
        self.assertTrue(cert.lower_endpoint_only)
        self.assertFalse(cert.upper_endpoint_removed)
        self.assertTrue(cert.historical_numeric_envelope_remains_safe)
        self.assertFalse(cert.historical_actual_target_label_correct)
        self.assertTrue(cert.fgkmt_hypothesis_endpoint_bridge_closed)
        self.assertFalse(cert.downstream_weighted_endpoint_closed)
        self.assertFalse(cert.siv_08_closed)
        self.assertFalse(cert.x_cert_ready)

    def test_machine_contract_and_source_hashes(self) -> None:
        self.assertEqual(
            self.contract["outcome"],
            "FGKMT_CLOSED_INTERVAL_ENDPOINT_SEMANTICS_CORRECTED_NUMERIC_ENVELOPE_PRESERVED",
        )
        self.assertFalse(self.contract["limits"]["downstream_weighted_endpoint_closed"])
        self.assertFalse(self.contract["limits"]["siv_08_closed"])
        for source in self.contract["source_registry"]:
            path = ROOT / source["local_path"]
            self.assertTrue(path.is_file(), source["local_path"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                source["sha256"],
                source["key"],
            )


if __name__ == "__main__":
    unittest.main()
