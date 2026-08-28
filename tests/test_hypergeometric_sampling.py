from __future__ import annotations

import math
import unittest

import numpy as np

from source.hypergeometric_sampling import (
    HypergeometricSamplingError,
    NUMPY_CATEGORY_LIMIT,
    hypergeometric_sampling_plan,
    sample_hypergeometric,
)


class HypergeometricSamplingTests(unittest.TestCase):
    def test_numpy_safe_path_is_bit_for_bit_unchanged(self) -> None:
        expected_rng = np.random.default_rng(12345)
        actual_rng = np.random.default_rng(12345)
        expected = expected_rng.hypergeometric(17, 23, 11, size=10_000)
        actual, plan = sample_hypergeometric(actual_rng, 17, 23, 11, size=10_000)
        np.testing.assert_array_equal(actual, expected)
        self.assertEqual(plan.backend, "numpy_hypergeometric")

    def test_large_category_uses_exact_sequential_symmetry(self) -> None:
        values, plan = sample_hypergeometric(
            np.random.default_rng(20260828),
            10,
            NUMPY_CATEGORY_LIMIT + 10,
            500_000_000,
            size=200_000,
        )
        self.assertEqual(plan.backend, "exact_sequential_symmetry")
        self.assertEqual(plan.symmetry, "marked_items")
        self.assertEqual(plan.sequential_draws, 10)
        population = 10 + NUMPY_CATEGORY_LIMIT + 10
        expected = 500_000_000 * 10 / population
        variance = (
            500_000_000
            * (10 / population)
            * (1 - 10 / population)
            * ((population - 500_000_000) / (population - 1))
        )
        standard_error = math.sqrt(variance / values.size)
        self.assertLess(abs(float(values.mean()) - expected), 6 * standard_error)
        self.assertGreaterEqual(int(values.min()), 0)
        self.assertLessEqual(int(values.max()), 10)

    def test_all_four_symmetry_transforms_preserve_support(self) -> None:
        cases = (
            (3, 17, 8, "marked_items"),
            (17, 3, 8, "unmarked_items"),
            (8, 12, 2, "sampled_positions"),
            (8, 12, 18, "omitted_positions"),
        )
        for ngood, nbad, nsample, symmetry in cases:
            with self.subTest(symmetry=symmetry):
                values, plan = sample_hypergeometric(
                    np.random.default_rng(7),
                    ngood,
                    nbad,
                    nsample,
                    size=50_000,
                    force_sequential=True,
                )
                self.assertEqual(plan.symmetry, symmetry)
                self.assertGreaterEqual(int(values.min()), max(0, nsample - nbad))
                self.assertLessEqual(int(values.max()), min(ngood, nsample))
                self.assertAlmostEqual(
                    float(values.mean()),
                    nsample * ngood / (ngood + nbad),
                    delta=0.04,
                )

    def test_sequential_backend_agrees_with_small_exact_pmf(self) -> None:
        ngood, nbad, nsample = 4, 8, 5
        values, _ = sample_hypergeometric(
            np.random.default_rng(8675309),
            ngood,
            nbad,
            nsample,
            size=300_000,
            force_sequential=True,
        )
        denominator = math.comb(ngood + nbad, nsample)
        for outcome in range(max(0, nsample - nbad), min(ngood, nsample) + 1):
            probability = (
                math.comb(ngood, outcome)
                * math.comb(nbad, nsample - outcome)
                / denominator
            )
            observed = int(np.count_nonzero(values == outcome))
            expected = values.size * probability
            sigma = math.sqrt(values.size * probability * (1.0 - probability))
            self.assertLess(abs(observed - expected), 6.0 * sigma + 1.0)

    def test_invalid_parameters_and_excessive_sequential_plan_fail_closed(self) -> None:
        with self.assertRaises(HypergeometricSamplingError):
            sample_hypergeometric(np.random.default_rng(1), 1, 1, 3, size=1)
        with self.assertRaises(HypergeometricSamplingError):
            hypergeometric_sampling_plan(
                3_000_000,
                3_000_000,
                3_000_000,
                force_sequential=True,
            )


if __name__ == "__main__":
    unittest.main()
