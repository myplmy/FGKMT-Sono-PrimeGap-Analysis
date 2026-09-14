from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "lean" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from validate_text_integrity import find_disallowed_controls  # noqa: E402


class TextIntegrityValidatorTests(unittest.TestCase):
    def test_plain_lf_and_crlf_are_allowed(self) -> None:
        self.assertEqual(find_disallowed_controls("alpha\nbeta\r\ngamma"), [])

    def test_latex_backslashes_are_preserved(self) -> None:
        self.assertEqual(
            find_disallowed_controls(r"\varphi(q), \theta, \frac{1}{2}"), []
        )

    def test_javascript_escape_damage_is_rejected(self) -> None:
        for control in ("\b", "\t", "\v", "\f", "\r"):
            with self.subTest(codepoint=ord(control)):
                issues = find_disallowed_controls(f"before{control}after")
                self.assertEqual(len(issues), 1)
                self.assertEqual(issues[0].codepoint, ord(control))

    def test_control_location_is_reported(self) -> None:
        issue = find_disallowed_controls("first\nabc\vdef", path="sample.md")[0]
        self.assertEqual(issue.path, "sample.md")
        self.assertEqual((issue.line, issue.column), (2, 4))


if __name__ == "__main__":
    unittest.main()
