"""Pre-execution checks for the canonical iterated-log definition."""

import ast
import math
import unittest
from pathlib import Path

import mpmath as mp

from source.definitions import (
    F,
    H,
    SONO_CONSTANT,
    WORKING_DPS,
    X_SCALE_POSITIVE_MIN,
    iter_log,
    sono_bound,
    sono_ratio,
)


class IteratedLogDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        mp.mp.dps = WORKING_DPS

    def assert_mp_equal(self, actual: mp.mpf, expected: mp.mpf) -> None:
        tolerance = mp.mpf("1e-45")
        self.assertTrue(
            mp.almosteq(actual, expected, rel_eps=tolerance, abs_eps=tolerance),
            msg=f"{actual!r} != {expected!r}",
        )

    def test_iter_log_matches_directly_nested_natural_logs(self) -> None:
        x = mp.mpf("1e100")
        direct_1 = mp.log(x)
        direct_2 = mp.log(direct_1)
        direct_3 = mp.log(direct_2)
        direct_4 = mp.log(direct_3)

        self.assert_mp_equal(iter_log(x, 1), direct_1)
        self.assert_mp_equal(iter_log(x, 2), direct_2)
        self.assert_mp_equal(iter_log(x, 3), direct_3)
        self.assert_mp_equal(iter_log(x, 4), direct_4)

    def test_base_k_logs_are_not_iterated_logs(self) -> None:
        # These base-k calls exist only as negative controls required by the
        # protocol.  They must never be used in production calculations.
        x_float = 1.0e12
        base_values = (
            math.log(x_float, 2),
            math.log(x_float, 3),
            math.log(x_float, 4),
        )
        iterated_values = (
            iter_log(x_float, 2),
            iter_log(x_float, 3),
            iter_log(x_float, 4),
        )

        for base_value, iterated_value in zip(base_values, iterated_values, strict=True):
            self.assertGreater(abs(mp.mpf(base_value) - iterated_value), mp.mpf("1e-6"))

    def test_F_matches_fully_expanded_formula(self) -> None:
        x = mp.mpf("1e100")
        log_1 = mp.log(x)
        log_2 = mp.log(log_1)
        log_3 = mp.log(log_2)
        log_4 = mp.log(log_3)
        expanded = log_1 * log_2 * log_4 / log_3

        self.assert_mp_equal(F(x), expanded)

    def test_normalizations_are_algebraically_consistent(self) -> None:
        x = mp.mpf("1e100")
        gap = mp.mpf("123456")

        self.assert_mp_equal(H(x, gap), gap / F(x))
        self.assert_mp_equal(sono_bound(x), SONO_CONSTANT * F(x))
        self.assert_mp_equal(sono_ratio(x, gap), H(x, gap) / SONO_CONSTANT)

    def test_domain_and_positive_scale_boundary(self) -> None:
        with self.assertRaises(ValueError):
            iter_log(15, 4)

        self.assertLess(F(16), 0)
        self.assertLess(F(X_SCALE_POSITIVE_MIN - 1), 0)
        self.assertGreater(F(X_SCALE_POSITIVE_MIN), 0)

    def test_iteration_count_must_be_positive_integer(self) -> None:
        for invalid_n in (0, -1, 2.0, True):
            with self.subTest(invalid_n=invalid_n):
                with self.assertRaises(ValueError):
                    iter_log(100, invalid_n)  # type: ignore[arg-type]

    def test_production_source_contains_no_base_k_log_calls(self) -> None:
        source_root = Path(__file__).resolve().parents[1] / "source"
        violations: list[str] = []

        for source_path in sorted(source_root.rglob("*.py")):
            tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue

                if isinstance(node.func, ast.Attribute):
                    function_name = node.func.attr
                    if function_name in {"log2", "log3", "log4"}:
                        violations.append(f"{source_path}:{node.lineno} uses .{function_name}()")
                    if function_name == "log" and (
                        len(node.args) >= 2 or any(keyword.arg == "base" for keyword in node.keywords)
                    ):
                        violations.append(f"{source_path}:{node.lineno} uses a base argument")

                if isinstance(node.func, ast.Name) and node.func.id == "log" and (
                    len(node.args) >= 2 or any(keyword.arg == "base" for keyword in node.keywords)
                ):
                    violations.append(f"{source_path}:{node.lineno} uses an imported base argument")

        self.assertEqual(violations, [], msg="\n".join(violations))


if __name__ == "__main__":
    unittest.main()
