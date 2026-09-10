"""Generate the checked-in formula inventory and human verification ledger.

This is a deterministic repository-maintenance tool.  It does not invoke Lean
and it never upgrades dependencies.  Kernel status is read only from the
separately reviewed verification_status_v1.json mapping.
"""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

from inventory_theory_formulas import build_inventory


STATUS_MEANING = {
    "KERNEL_PASS": (
        "표시한 명제가 project-local axiom, `sorry`, `admit` 없이 Lean 커널을 통과"
    ),
    "CONDITIONAL_KERNEL_PASS": (
        "명시한 premise에서 결론으로 가는 합성은 통과했지만 premise의 source 증명은 미인증일 수 있음"
    ),
    "DEFINITION_ONLY": "표기·함수 정의의 전사이며 참·거짓 증명 대상이 아님",
    "PARTIAL_FORMALIZATION": "display 식의 핵심 일부만 형식화; 식 전체 PASS가 아님",
    "SOURCE_THEOREM_UNFORMALIZED": "source analytic theorem을 확인했지만 Lean 독립 증명은 없음",
    "NOT_YET_FORMALIZED": "inventory만 완료; Lean 선언 없음",
    "PARSE_REVIEW_REQUIRED": (
        "hash-pinned 원문의 수식 경계가 불완전해 안전 복구했지만 원문은 소급 변경하지 않음"
    ),
}


NOTES_BY_ID = {
    "T01-U001": "정의 전개와 반복 횟수",
    "T01-U002": "finite record 표현",
    "T01-U003": "보조 start-bounded 정의",
    "T01-U004": "정수 경계만; G 상수성 premise는 후속",
    "T01-U005": "F 단조성 증명은 후속",
    "T07-U001": "D와 N의 함수 정의는 후속",
    "T07-U002": "순수 환대수 항등식",
    "T07-U003": "discrepancy lower premise 명시",
    "T07-U004": "상계 방향 커널 검증",
    "T07-U005": "Mathlib floor Galois connection",
    "T10-U001": "exact primality/next-prime는 매개변수",
    "T10-U002": "후보 superset soundness",
    "T10-U003": "witness soundness",
    "T10-U004": "total coverage",
    "T10-U005": "Nat exact arithmetic",
    "T11-U001": "source inequality와 대표 증가 premise",
    "55.4": "J,h 완료; cell I_j는 후속",
    "55.5": "Nat.ceil에서 세 bound 유도",
    "55.6": "grid-union measure premise 이후 scalar 합성",
    "55.10": "floor-log window p≤R<5p premise",
    "55.13": "pre-cover count 상계 이후 상수 합성",
    "55.14": "t=η/8을 명시적 premise로 사용",
    "55.15": "r0,e* gate를 premise로 사용",
    "55.16": "relative-error 대수 합성",
    "55.33": "exact rational arithmetic",
    "55.36": "정수 상수만; smooth count chain은 후속",
    "55.39": "analytic/count premise 이후 최종 상계 대수",
    "27.9": "원문 display 종료기호 누락; hash 보존",
    "27.10": "원문 display 종료기호 누락; hash 보존",
    "27.11": "원문 display 종료기호 누락; hash 보존",
    "27.12": "원문 display 종료기호 누락; hash 보존",
    "27.13": "원문 display 종료기호 누락; hash 보존",
}


def preview(latex: str, limit: int = 220) -> str:
    compact = " ".join(latex.split())
    if len(compact) > limit:
        compact = compact[: limit - 1] + "…"
    return html.escape(compact, quote=False).replace("|", "&#124;")


def doc_link(source_file: str) -> str:
    name = Path(source_file).name
    return f"[{name}](../{source_file})"


def build_ledger(inventory: dict[str, object], status_doc: dict[str, object]) -> str:
    status_by_id = {entry["formula_id"]: entry for entry in status_doc["formulae"]}
    default_status = status_doc["default_status"]
    formulae = inventory["formulae"]
    counts = Counter(
        status_by_id.get(item["formula_id"], {}).get("status", default_status)
        for item in formulae
    )
    reviewed_by_theory = Counter(
        item["theory"]
        for item in formulae
        if status_by_id.get(item["formula_id"], {}).get("status", default_status)
        != default_status
    )

    lines = [
        "# FGKMT-Sono Lean 전수 수식·정리 검증 원장",
        "",
        "- 생성 기준: 2026-09-10 KST",
        f"- inventory schema: `{inventory['schema_version']}`",
        f"- 원문 범위: `docs/method/theory/*.md` {inventory['theory_count']}개",
        f"- 전수 단위: Markdown fenced code 밖 display math {inventory['formula_count']:,}개",
        (
            f"- 원래 식번호: {inventory['tagged_formula_count']:,}개, 합성 ID 무번호식: "
            f"{inventory['untagged_formula_count']:,}개"
        ),
        f"- 안전 복구 표시: hash-pinned Theory 27의 누락 display 종료기호 {len(inventory['recoveries'])}개",
        "- 기계 정본: [formula_inventory_v1.json](verification/formula_inventory_v1.json)",
        "- 상태 정본: [verification_status_v1.json](verification/verification_status_v1.json)",
        "- Lean 정본: [TheoryVerification.lean](FGKMTSono/TheoryVerification.lean)",
        "- 현재 결론: 초기 dependency-critical batch만 형식화했다. 전체 Sono/FMT analytic theorem 또는",
        "  수치 `X_cert`가 Lean으로 증명됐다는 뜻이 아니다.",
        "",
        "## 1. 목적과 범위",
        "",
        "이 원장은 수식을 빠짐없이 식별하는 **전수 inventory**와 Lean이 실제 검사한 증거 수준을",
        "분리한다. inline math는 문장 안의 기호·매개변수 설명이므로 개별 proof obligation으로 세지",
        "않고, 모든 display math를 하나의 안정 항목으로 등록했다. 원래 `\\tag{...}`가 없는 display",
        "수식에는 `T<theory>-U<ordinal>` 합성 ID를 부여했다.",
        "",
        "원문 수식 자체는 각 source line과 SHA-256으로 고정한다. 표의 수식은 탐색용 preview이며,",
        "줄임 없는 LaTeX는 JSON inventory와 원문에 있다.",
        "",
        "## 2. 증거 수준",
        "",
        "| 상태 | 정확한 의미 |",
        "|---|---|",
    ]
    for status, meaning in STATUS_MEANING.items():
        lines.append(f"| `{status}` | {meaning} |")
    lines.extend(
        [
            "",
            "현재 `KERNEL_PASS`도 Lean/Mathlib의 표준 논리 기반 위의 검증이다. 외부 논문 명제를",
            "매개변수로 받은 정리는 반드시 `CONDITIONAL_KERNEL_PASS`로 낮춰 표시한다.",
            "",
            "## 3. 고정된 설치·dependency",
            "",
            "| 구성요소 | 고정값 | 검증 |",
            "|---|---|---|",
            "| Elan | 4.2.4, commit `227caca13` | 관측 |",
            "| Lean | `leanprover/lean4:v4.34.0-rc2` | `lean-toolchain` |",
            "| Lean kernel | `6a10ac8c22beadecabdbb0919c2b50214762f91d` | `lake env lean --version` |",
            "| Mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` | lakefile·manifest·local HEAD 3중 일치 |",
            "| transitive dependencies | `lake-manifest.json`의 full commit | manifest lock |",
            "",
            "## 4. 영향도와 검증 한계",
            "",
            "| 축 | 판정 |",
            "|---|---|",
            "| 반복로그·end-bounded 정의 | 정의를 Lean에 분리해 base-log 및 start/end 혼동을 방지 |",
            "| 유한 대수·floor·ceil·집합 논리 | Lean 독립 검증의 우선 대상 |",
            "| 적분·소수분포·sieve·hypergraph source theorem | Mathlib에 drop-in proof가 없으면 장기 source 형식화가 필요 |",
            "| 수치 근사 | exact rational theorem과 분리; decimal 출력만으로 PASS 금지 |",
            "| `X_cert` | DEP-R09–R12가 OPEN이므로 계속 OPEN |",
            "| actual experiment | 이번 원장은 새 prime 계산이나 `test_result`를 만들지 않음 |",
            "",
            "## 5. 현재 상태 집계",
            "",
            "| 상태 | 항목 수 |",
            "|---|---:|",
        ]
    )
    for status in STATUS_MEANING:
        lines.append(f"| `{status}` | {counts.get(status, 0):,} |")
    lines.extend(
        [
            "",
            "집계는 display 수식 행 기준이다. 하나의 Lean theorem이 여러 display 식의 합성을 검증하거나,",
            "한 display 식이 여러 Lean 선언으로 나뉠 수 있다.",
            "",
            "## 6. theory별 전수 현황",
            "",
            "| Theory | 원문 | SHA-256 | display | tagged | untagged | 현재 형식화·review 행 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    for theory in inventory["theories"]:
        lines.append(
            f"| {theory['theory']} | {doc_link(theory['source_file'])} | "
            f"`{theory['source_sha256'][:16]}…` | {theory['display_formula_count']:,} | "
            f"{theory['tagged_formula_count']:,} | {theory['untagged_formula_count']:,} | "
            f"{reviewed_by_theory[theory['theory']]:,} |"
        )
    lines.extend(
        [
            "",
            "## 7. 추가 Lean 정리(문단 논증)",
            "",
            "| 원문 | Lean 선언 | 상태 | 범위 |",
            "|---|---|---|---|",
        ]
    )
    supplemental_scope = {
        "sequential_positive_probability_choice": "독립성이나 두 실패율 합 조건이 불필요하다는 순수 논리",
    }
    for item in status_doc.get("supplemental_theorems", []):
        declarations = "; ".join(f"`{name}`" for name in item["declarations"])
        scope = "; ".join(supplemental_scope.get(name, "보조 exact 정리") for name in item["declarations"])
        lines.append(f"| {item['source']} | {declarations} | `{item['status']}` | {scope} |")
    lines.extend(
        [
            "",
            "## 8. 수식별 전수 검증 표",
            "",
            "| # | 수식 ID | Theory·원문 | line | 수식 preview | Lean 선언 | 상태 | 한계·근거 |",
            "|---:|---|---|---:|---|---|---|---|",
        ]
    )
    for ordinal, item in enumerate(formulae, start=1):
        entry = status_by_id.get(item["formula_id"], {})
        status = entry.get("status", default_status)
        declarations = entry.get("declarations", [])
        declaration_text = "; ".join(declarations) if declarations else "—"
        if declarations:
            declaration_text = f"`{declaration_text}`"
        note = NOTES_BY_ID.get(
            item["formula_id"],
            "순차 형식화 대기" if status == default_status else STATUS_MEANING[status],
        )
        line_range = (
            str(item["start_line"])
            if item["start_line"] == item["end_line"]
            else f"{item['start_line']}–{item['end_line']}"
        )
        lines.append(
            f"| {ordinal} | `{item['formula_id']}` | T{item['theory']} "
            f"{doc_link(item['source_file'])} | {line_range} | "
            f"<code>{preview(item['latex'])}</code> | {declaration_text} | `{status}` | {note} |"
        )
    lines.extend(
        [
            "",
            "## 9. 발견된 원문·작업 오류",
            "",
            "1. hash-pinned Theory 27 식 (27.9)–(27.13)에 display 종료 `\\]` 5개가 빠져 있다.",
            "   원문 SHA 계약을 보존하기 위해 소급 변경하지 않고 inventory에서만 안전 분리했으며",
            "   다섯 행을 `PARSE_REVIEW_REQUIRED`로 남겼다.",
            "2. Theory 01 plateau 식의 `qquad` 앞 backslash 누락을 확인해 `\\qquad`로 교정했다.",
            "3. 단일 Lean target을 import한 뒤 target 생성 전에 최초 build를 시작해 한 차례",
            "   `no such file ... TheoryVerification.lean`이 발생했다. 작업 순서 오류로 기록하고",
            "   target 생성 뒤 직접 kernel 검사와 전체 build를 다시 수행한다.",
            "",
            "## 10. 순차 형식화 우선순위",
            "",
            "1. 초기 batch의 declaration–원장 연결과 no-sorry 검증을 고정한다.",
            "2. Theory 01의 scale positivity·interval-minimum 단조성 가정을 정식화한다.",
            "3. Theories 10–11의 finite set/residue pullback 전체 구조를 닫는다.",
            "4. `X_cert` dependency critical path인 theories 47–55를 역의존 순서로 형식화한다.",
            "5. source analytic theorem은 먼저 Mathlib/선행 형식화를 찾고, 없으면",
            "   `SOURCE_THEOREM_UNFORMALIZED`로 차단한 뒤 별도 장기 증명 단위로 분해한다.",
            "6. 이후 theories 13–46과 초기 empirical/certificate theory를 순차 처리한다.",
            "",
            "새 theory가 추가되면 inventory와 원장을 재생성하고 기존 source SHA가 움직였는지 먼저 검사한다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    lean_root = repo_root / "lean"
    inventory = build_inventory(repo_root)
    if inventory["issues"]:
        raise ValueError(f"cannot generate from parse issues: {inventory['issues']}")
    status_path = lean_root / "verification" / "verification_status_v1.json"
    status_doc = json.loads(status_path.read_text(encoding="utf-8"))
    inventory_path = lean_root / "verification" / "formula_inventory_v1.json"
    ledger_path = lean_root / "VERIFICATION_LEDGER.md"
    inventory_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    ledger_path.write_text(
        build_ledger(inventory, status_doc),
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "GENERATED",
                "theory_count": inventory["theory_count"],
                "formula_count": inventory["formula_count"],
                "recoveries": len(inventory["recoveries"]),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
