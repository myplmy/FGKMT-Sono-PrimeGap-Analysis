"""Fail closed on UTF-8 source text containing hidden control characters."""

from __future__ import annotations

import argparse
import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


TEXT_SUFFIXES = {
    ".bat",
    ".csv",
    ".json",
    ".lean",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".txt",
}


@dataclass(frozen=True)
class ControlIssue:
    path: str
    line: int
    column: int
    codepoint: int
    name: str


def find_disallowed_controls(text: str, *, path: str = "<memory>") -> list[ControlIssue]:
    """Return C0/C1 control characters other than LF and CRLF line endings."""

    issues: list[ControlIssue] = []
    line = 1
    column = 1
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\r" and index + 1 < len(text) and text[index + 1] == "\n":
            line += 1
            column = 1
            index += 2
            continue
        if char == "\n":
            line += 1
            column = 1
            index += 1
            continue
        if unicodedata.category(char) == "Cc":
            issues.append(
                ControlIssue(
                    path=path,
                    line=line,
                    column=column,
                    codepoint=ord(char),
                    name=unicodedata.name(char, "UNNAMED CONTROL"),
                )
            )
        column += 1
        index += 1
    return issues


def expand_text_paths(paths: Iterable[Path]) -> list[Path]:
    files: set[Path] = set()
    for raw_path in paths:
        path = raw_path.resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        if path.is_file():
            files.add(path)
            continue
        for candidate in path.rglob("*"):
            if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                files.add(candidate.resolve())
    return sorted(files, key=lambda item: item.as_posix())


def validate_text_integrity(paths: Iterable[Path]) -> dict[str, int]:
    files = expand_text_paths(paths)
    issues: list[ControlIssue] = []
    byte_count = 0
    for path in files:
        payload = path.read_bytes()
        byte_count += len(payload)
        text = payload.decode("utf-8")
        issues.extend(find_disallowed_controls(text, path=path.as_posix()))
    if issues:
        rendered = [
            f"{issue.path}:{issue.line}:{issue.column}: "
            f"U+{issue.codepoint:04X} {issue.name}"
            for issue in issues
        ]
        raise AssertionError("disallowed text controls: " + "; ".join(rendered))
    return {"file_count": len(files), "byte_count": byte_count, "issue_count": 0}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate UTF-8 text files and reject hidden control characters."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = validate_text_integrity(args.paths)
    except (AssertionError, FileNotFoundError, UnicodeDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **summary}, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
