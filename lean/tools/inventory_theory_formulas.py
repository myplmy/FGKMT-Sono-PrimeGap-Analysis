"""Read-only inventory builder for docs/method/theory Markdown display formulae.

The script never edits the repository.  It emits deterministic JSON to stdout so
the checked-in ledger can be generated with the repository patch workflow and
then independently checked against the canonical Markdown sources.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


TAG_RE = re.compile(r"\\tag\{([^}]+)\}")
THEORY_RE = re.compile(r"^(\d{2})_")


@dataclass(frozen=True)
class Formula:
    formula_id: str
    theory: str
    source_file: str
    start_line: int
    end_line: int
    tagged: bool
    latex: str
    source_sha256: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_latex(lines: list[str]) -> str:
    text = "\n".join(lines).strip()
    text = re.sub(r"^\\\[\s*", "", text)
    text = re.sub(r"\s*\\\]$", "", text)
    text = re.sub(r"^\$\$\s*", "", text)
    text = re.sub(r"\s*\$\$$", "", text)
    return text.strip()


def extract_blocks(
    path: Path,
) -> tuple[list[tuple[int, int, str]], list[str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[tuple[int, int, str]] = []
    issues: list[str] = []
    recoveries: list[str] = []
    in_fence = False
    fence_token = ""
    mode: str | None = None
    start = 0
    collected: list[str] = []

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if mode is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            continue
        if in_fence:
            continue

        if mode == "bracket":
            # Preserve hash-pinned historical Markdown.  If a tagged display is
            # followed by a blank line without `\]`, close it at the tag and
            # record a review-required recovery instead of swallowing the next
            # formula.  This is intentionally narrower than generic recovery.
            if stripped == "" and TAG_RE.search("\n".join(collected)):
                next_nonblank = next(
                    (candidate.strip() for candidate in lines[line_no:] if candidate.strip()),
                    "",
                )
                if next_nonblank != r"\]":
                    blocks.append((start, line_no - 1, normalized_latex(collected)))
                    recoveries.append(
                        f"{path.name}:{start}-{line_no - 1}: implicit close after tagged display"
                    )
                    mode = None
                    collected = []
                    continue
            collected.append(line)
            if stripped == r"\]":
                blocks.append((start, line_no, normalized_latex(collected)))
                mode = None
                collected = []
            continue
        if mode == "dollar":
            collected.append(line)
            if stripped == "$$":
                blocks.append((start, line_no, normalized_latex(collected)))
                mode = None
                collected = []
            continue
        if mode == "environment":
            collected.append(line)
            if re.search(r"\\end\{(?:align\*?|equation\*?|gather\*?)\}", stripped):
                blocks.append((start, line_no, normalized_latex(collected)))
                mode = None
                collected = []
            continue

        if stripped == r"\[":
            mode = "bracket"
            start = line_no
            collected = [line]
            continue
        if stripped == "$$":
            mode = "dollar"
            start = line_no
            collected = [line]
            continue
        if re.search(r"\\begin\{(?:align\*?|equation\*?|gather\*?)\}", stripped):
            mode = "environment"
            start = line_no
            collected = [line]
            if re.search(r"\\end\{(?:align\*?|equation\*?|gather\*?)\}", stripped):
                blocks.append((start, line_no, normalized_latex(collected)))
                mode = None
                collected = []
            continue

        # Rare one-line bracket display.
        if r"\[" in line and r"\]" in line and line.index(r"\[") < line.index(r"\]"):
            left = line.index(r"\[")
            right = line.rindex(r"\]") + 2
            blocks.append((line_no, line_no, normalized_latex([line[left:right]])))

    if mode is not None:
        issues.append(f"{path.name}:{start}: unclosed {mode} display")
    if in_fence:
        issues.append(f"{path.name}: unclosed Markdown fence")
    return blocks, issues, recoveries


def build_inventory(repo_root: Path) -> dict[str, object]:
    theory_dir = repo_root / "docs" / "method" / "theory"
    documents = sorted(theory_dir.glob("*.md"), key=lambda p: p.name)
    theories: list[dict[str, object]] = []
    formulae: list[Formula] = []
    issues: list[str] = []
    recoveries: list[str] = []
    seen_ids: set[str] = set()

    for path in documents:
        match = THEORY_RE.match(path.name)
        theory = match.group(1) if match else path.stem
        digest = sha256(path)
        blocks, block_issues, block_recoveries = extract_blocks(path)
        issues.extend(block_issues)
        recoveries.extend(block_recoveries)
        untagged_ordinal = 0
        tagged_count = 0
        for start_line, end_line, latex in blocks:
            tags = TAG_RE.findall(latex)
            if len(tags) > 1:
                issues.append(f"{path.name}:{start_line}: multiple tags {tags}")
            if tags:
                formula_id = tags[0]
                tagged = True
                tagged_count += 1
            else:
                untagged_ordinal += 1
                formula_id = f"T{theory}-U{untagged_ordinal:03d}"
                tagged = False
            if formula_id in seen_ids:
                issues.append(f"{path.name}:{start_line}: duplicate formula id {formula_id}")
            seen_ids.add(formula_id)
            formulae.append(
                Formula(
                    formula_id=formula_id,
                    theory=theory,
                    source_file=path.relative_to(repo_root).as_posix(),
                    start_line=start_line,
                    end_line=end_line,
                    tagged=tagged,
                    latex=latex,
                    source_sha256=digest,
                )
            )
        theories.append(
            {
                "theory": theory,
                "source_file": path.relative_to(repo_root).as_posix(),
                "source_sha256": digest,
                "display_formula_count": len(blocks),
                "tagged_formula_count": tagged_count,
                "untagged_formula_count": len(blocks) - tagged_count,
            }
        )

    return {
        "schema_version": "fgkmt-lean-formula-inventory-v1",
        "scope": "Markdown display math outside fenced code blocks; inline math is contextual notation",
        "theory_count": len(theories),
        "formula_count": len(formulae),
        "tagged_formula_count": sum(1 for f in formulae if f.tagged),
        "untagged_formula_count": sum(1 for f in formulae if not f.tagged),
        "theories": theories,
        "formulae": [asdict(formula) for formula in formulae],
        "issues": issues,
        "recoveries": recoveries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument(
        "--section",
        choices=("all", "summary", "theories", "formulae"),
        default="all",
    )
    parser.add_argument("--formula-start", type=int, default=0)
    parser.add_argument("--formula-count", type=int)
    args = parser.parse_args()
    inventory = build_inventory(args.repo_root.resolve())
    if args.section == "summary":
        payload: object = {
            key: inventory[key]
            for key in (
                "schema_version",
                "scope",
                "theory_count",
                "formula_count",
                "tagged_formula_count",
                "untagged_formula_count",
                "issues",
                "recoveries",
            )
        }
    elif args.section == "theories":
        payload = inventory["theories"]
    elif args.section == "formulae":
        start = max(0, args.formula_start)
        stop = None if args.formula_count is None else start + max(0, args.formula_count)
        payload = inventory["formulae"][start:stop]
    else:
        payload = inventory
    print(
        json.dumps(
            payload,
            # ASCII JSON avoids host-console code-page corruption on Windows.
            ensure_ascii=True,
            indent=2 if args.pretty else None,
            sort_keys=True,
        )
    )
    return 1 if inventory["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
