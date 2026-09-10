"""Validate the checked-in theory inventory, status ledger, and single Lean file."""

from __future__ import annotations

import json
import re
from pathlib import Path

from inventory_theory_formulas import build_inventory


VALID_STATUSES = {
    "KERNEL_PASS",
    "CONDITIONAL_KERNEL_PASS",
    "DEFINITION_ONLY",
    "PARTIAL_FORMALIZATION",
    "SOURCE_THEOREM_UNFORMALIZED",
    "NOT_YET_FORMALIZED",
    "PARSE_REVIEW_REQUIRED",
}


def strip_lean_comments_and_strings(text: str) -> str:
    output: list[str] = []
    i = 0
    block_depth = 0
    line_comment = False
    string = False
    escaped = False
    while i < len(text):
        pair = text[i : i + 2]
        char = text[i]
        if line_comment:
            if char == "\n":
                line_comment = False
                output.append(char)
            else:
                output.append(" ")
            i += 1
            continue
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                i += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                i += 2
            else:
                output.append("\n" if char == "\n" else " ")
                i += 1
            continue
        if string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                string = False
            i += 1
            continue
        if pair == "--":
            line_comment = True
            output.extend("  ")
            i += 2
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            i += 2
        elif char == '"':
            string = True
            output.append(" ")
            i += 1
        else:
            output.append(char)
            i += 1
    if block_depth or string:
        raise ValueError("unclosed Lean block comment or string")
    return "".join(output)


def declared_names(code: str) -> set[str]:
    pattern = re.compile(
        r"(?m)^\s*(?:noncomputable\s+)?(?:def|theorem|structure)\s+([A-Za-z_][A-Za-z0-9_'.]*)"
    )
    return set(pattern.findall(code))


def parse_formula_rows(ledger: str) -> list[tuple[str, str]]:
    section = ledger.split("## 8. 수식별 전수 검증 표", 1)[1]
    section = section.split("## 9. 발견된 원문·작업 오류", 1)[0]
    rows: list[tuple[str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 8 or not parts[0].isdigit():
            continue
        formula_id = parts[1].strip("`")
        status = parts[6].strip("`")
        rows.append((formula_id, status))
    return rows


def validate_local_markdown_links(paths: list[Path]) -> int:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    checked = 0
    missing: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            checked += 1
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                missing.append(f"{path.name}: {target}")
    if missing:
        raise AssertionError(f"missing local Markdown links: {missing}")
    return checked


def main() -> int:
    lean_root = Path(__file__).resolve().parents[1]
    repo_root = lean_root.parent
    inventory_path = lean_root / "verification" / "formula_inventory_v1.json"
    status_path = lean_root / "verification" / "verification_status_v1.json"
    ledger_path = lean_root / "VERIFICATION_LEDGER.md"
    lean_path = lean_root / "FGKMTSono" / "TheoryVerification.lean"

    saved_inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    rebuilt_inventory = build_inventory(repo_root)
    if saved_inventory != rebuilt_inventory:
        raise AssertionError("saved formula inventory differs from current theory sources")
    if rebuilt_inventory["issues"]:
        raise AssertionError(f"formula parse issues: {rebuilt_inventory['issues']}")

    status_document = json.loads(status_path.read_text(encoding="utf-8"))
    status_entries = status_document["formulae"]
    status_by_id = {entry["formula_id"]: entry for entry in status_entries}
    if len(status_by_id) != len(status_entries):
        raise AssertionError("duplicate formula_id in verification status")
    inventory_ids = [item["formula_id"] for item in rebuilt_inventory["formulae"]]
    unknown_status_ids = sorted(set(status_by_id) - set(inventory_ids))
    if unknown_status_ids:
        raise AssertionError(f"status refers to unknown formulae: {unknown_status_ids}")

    for entry in status_entries + status_document.get("supplemental_theorems", []):
        if entry["status"] not in VALID_STATUSES:
            raise AssertionError(f"invalid status: {entry['status']}")

    lean_text = lean_path.read_text(encoding="utf-8")
    executable_lean = strip_lean_comments_and_strings(lean_text)
    banned = re.findall(r"\b(?:axiom|sorry|admit)\b", executable_lean)
    if banned:
        raise AssertionError(f"banned Lean proof escape found: {banned}")
    declarations = declared_names(executable_lean)
    required_declarations = {
        declaration
        for entry in status_entries + status_document.get("supplemental_theorems", [])
        for declaration in entry["declarations"]
    }
    missing_declarations = sorted(required_declarations - declarations)
    if missing_declarations:
        raise AssertionError(f"ledger declarations missing from Lean: {missing_declarations}")

    ledger_rows = parse_formula_rows(ledger_path.read_text(encoding="utf-8"))
    if [row[0] for row in ledger_rows] != inventory_ids:
        raise AssertionError("ledger formula row order/coverage differs from inventory")
    for formula_id, status in ledger_rows:
        expected = status_by_id.get(formula_id, {}).get(
            "status", status_document["default_status"]
        )
        if status != expected:
            raise AssertionError(
                f"ledger status mismatch for {formula_id}: {status} != {expected}"
            )

    expected_toolchain = "leanprover/lean4:v4.34.0-rc2"
    actual_toolchain = (lean_root / "lean-toolchain").read_text(encoding="utf-8").strip()
    if actual_toolchain != expected_toolchain:
        raise AssertionError(f"unexpected Lean toolchain: {actual_toolchain}")
    mathlib_commit = "85e3a25e006c35636f0e53b0e9296caca2685bc0"
    lakefile = (lean_root / "lakefile.toml").read_text(encoding="utf-8")
    if f'rev = "{mathlib_commit}"' not in lakefile:
        raise AssertionError("lakefile does not pin the Mathlib full commit")
    manifest = json.loads((lean_root / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
    if mathlib["rev"] != mathlib_commit or mathlib["inputRev"] != mathlib_commit:
        raise AssertionError("Mathlib manifest rev/inputRev is not fully pinned")

    local_link_count = validate_local_markdown_links(
        [
            lean_root / "README.md",
            ledger_path,
            lean_root / "verification" / "README.md",
        ]
    )

    counts: dict[str, int] = {}
    for formula_id in inventory_ids:
        status = status_by_id.get(formula_id, {}).get(
            "status", status_document["default_status"]
        )
        counts[status] = counts.get(status, 0) + 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "theory_count": rebuilt_inventory["theory_count"],
                "formula_count": rebuilt_inventory["formula_count"],
                "tagged_formula_count": rebuilt_inventory["tagged_formula_count"],
                "untagged_formula_count": rebuilt_inventory["untagged_formula_count"],
                "recovery_count": len(rebuilt_inventory["recoveries"]),
                "declaration_count": len(declarations),
                "local_markdown_link_count": local_link_count,
                "status_counts": counts,
                "banned_escape_count": len(banned),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
