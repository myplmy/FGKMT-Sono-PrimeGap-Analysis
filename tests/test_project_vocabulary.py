"""Guard the five-author theorem acronym across project text and filenames."""

import unittest
from pathlib import Path


class ProjectVocabularyTests(unittest.TestCase):
    def test_deprecated_four_letter_typo_is_absent(self) -> None:
        root = Path(__file__).resolve().parents[1]
        forbidden = "FG" + "MT"
        extensions = {".md", ".py", ".json", ".yml", ".yaml", ".ps1", ".txt"}
        violations: list[str] = []

        for path in root.rglob("*"):
            relative = path.relative_to(root)
            if any(part in {".git", "__pycache__", "article", "tmp"} for part in relative.parts):
                continue
            if forbidden.casefold() in path.name.casefold():
                violations.append(f"filename: {relative}")
            if path.is_file() and path.suffix.casefold() in extensions:
                text = path.read_text(encoding="utf-8", errors="strict")
                if (
                    relative.parts[0] == "handoff"
                    or path.name.endswith("WORK_LEDGER-done.md")
                ):
                    historical_scan_label = (
                        f"`{forbidden}` 오탈자 scan"
                    )
                    text = text.replace(historical_scan_label, "")
                if forbidden.casefold() in text.casefold():
                    violations.append(f"content: {relative}")

        self.assertEqual(violations, [], msg="\n".join(violations))


if __name__ == "__main__":
    unittest.main()
