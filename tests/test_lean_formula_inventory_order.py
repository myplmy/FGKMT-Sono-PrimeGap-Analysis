"""Regression tests for numeric ordering of Lean theory inventory documents."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


TOOLS_DIR = Path(__file__).resolve().parents[1] / "lean" / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from inventory_theory_formulas import THEORY_RE, theory_document_sort_key


class TheoryDocumentOrderTests(unittest.TestCase):
    def test_three_digit_theory_number_is_parsed(self):
        match = THEORY_RE.match("100_example.md")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "100")

    def test_numeric_order_does_not_insert_100_after_10(self):
        paths = [
            Path("100_example.md"),
            Path("10_example.md"),
            Path("99_example.md"),
            Path("09_example.md"),
            Path("101_example.md"),
        ]
        ordered = sorted(paths, key=theory_document_sort_key)
        self.assertEqual(
            [path.name for path in ordered],
            [
                "09_example.md",
                "10_example.md",
                "99_example.md",
                "100_example.md",
                "101_example.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
