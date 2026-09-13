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
    "T01-U001": "정의 전개·양수성·exp(exp(exp(1))) 위 strict monotonicity 커널 검증",
    "T01-U002": "finite record 표현",
    "T01-U003": "보조 start-bounded 정의",
    "T01-U004": "정수 경계만; G 상수성 premise는 후속",
    "T01-U005": "양의 end-bounded 정수 plateau의 오른쪽 끝점 minimum 커널 검증",
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
    "55.24": "Rankin counting은 source premise; rpow 지수 정규화는 커널 검증",
    "55.25": "Rosser--Schoenfeld prime harmonic 입력 이후 terminal 상계",
    "55.26": "S_delta·h(t) 정의와 t≠1의 정확한 적분 항등식 커널 검증",
    "55.27": "prime-sum 정규화·h(1)·decimal slack·종단 합성 검증; theta 1.01624 bound와 Stieltjes 비교는 미형식화",
    "T55-U002": "Ein interval-integral 정의 전사; delta L=w는 downstream premise",
    "55.28": "removable singularity, 두 finite interval 비교, improper integral·51/50 factor 커널 검증",
    "T55-U003": "Ein split과 103/100 상계 전체 커널 검증",
    "55.29": "Stieltjes premise 이후 Ein bound를 내부 호출해 actual parameter와 189/160 합성",
    "55.30": "2^(-3/4)<3/5와 terminal 대수 검증; prime/j-sum 비교는 premise",
    "55.31": "세 analytic/counting estimate 이후 product-log 합성",
    "55.32": "q>=200 actual log lower bounds 커널 검증",
    "55.33": "exact rational arithmetic",
    "55.34": "55.32 actual hypotheses에서 decay >4b 커널 검증",
    "55.35": "Rankin·Euler-product premise 이후 final exp cancellation 커널 검증",
    "55.36": "정수 상수만; smooth count chain은 후속",
    "55.39": "analytic/count premise 이후 최종 상계 대수",
    "56.1": "Sono c_ZFR=1/24에서 a=1/80 exact 대입",
    "56.2": "c_ZD=16에서 D_PAP=160 exact 대입",
    "56.3": "a*D_PAP=2와 C_PAP=1-exp(-2) exact 정의",
    "56.4": "0<C_PAP<1 exact 실수 부등식",
    "T56-U001": "Jutila Theorem 1의 source 진술; epsilon multiplier와 proof는 Lean 미형식화",
    "T56-U002": "finite error 합성의 명시적 analytic premise 쌍",
    "56.5": "principal/error premise 이후 finite slack 합성; analytic premise는 미인증",
    "56.6": "Jutila source epsilon/3 재매개화의 exact 지수 대수",
    "56.7": "alpha<=4/5의 low-alpha exponent bridge",
    "56.8": "DEP-R09 finite PAP 목표; Gallagher/Jutila/Maier rate와 cutoff 미형식화",
    "57.1": "Sono Proposition 5.3 source statement; analytic theorem은 Lean 미형식화",
    "57.2": "T>=2에서 log(T(1+T))<=3logT와 zero-free 폭 방향을 커널 검증",
    "57.3": "c_ZFR/3=1/72와 인쇄값 3c_ZFR=1/8의 불일치 exact 검증",
    "57.4": "McCurley Theorem 1 source statement; analytic theorem은 Lean 미형식화",
    "57.5": "McCurley Theorem 2 source statement; analytic theorem은 Lean 미형식화",
    "57.6": "direct c1=1/24의 R<12 수치 포함관계만 검증; family theorem 전체는 미형식화",
    "57.7": "Gallagher Theorem 7 source statement; hidden multiplier와 cutoff는 OPEN",
    "57.8": "c_ZD=16, D=160의 density-power boundary exact 검증",
    "57.9": "Q=x^(1/D)의 lower range에 필요한 D^2<=log x와 D=160 gate 검증",
    "57.10": "direct-McCurley repair exponent a0=1/240와 a0D=2/3 exact 검증",
    "57.11": "Gallagher-Maier nonprincipal error의 honest multiplier interface; rate 미형식화",
    "57.12": "같은 지수에서 multiplier 제거 iff K<=1을 커널 검증",
    "57.13": "log K budget으로 multiplier를 exponent에 흡수하는 충분조건 커널 검증",
    "57.14": "principal/error analytic premise 이후 multiplier 보존 one-sided 합성",
    "57.15": "교정 finite PAP analytic target; common cutoff와 source proof 미형식화",
    "58.1": "DEP-R09 fixed-coefficient pointwise PAP 목표; drop-in source 없음",
    "58.2": "exceptional modulus와 principal/nonprincipal/psi-to-pi를 포함한 finite target interface",
    "58.3": "D=160 coefficient-capacity 필요조건; 고정밀 Python 진단만 완료",
    "58.4": "최신 Sono arXiv v4와 journal에 그대로 인쇄된 상수 연결",
    "58.5": "Bennett et al. large-modulus cutoff source statement",
    "58.6": "Thorner-Zaman uniform PNT의 숨은 numerical multiplier interface",
    "58.7": "Thorner-Zaman fully explicit nonexceptional density source statement",
    "58.8": "Thorner-Zaman fully explicit exceptional-removed density source statement",
    "58.9": "Benli-Goel-Twiss-Zaman effective Deuring-Heilbronn source constants",
    "58.10": "Sono downstream coefficient capacity 함수 정의",
    "58.11": "D=160 최소 C_PAP 고정밀 진단; Lean 미형식화",
    "58.12": "D=160 총 상대오차 budget 고정밀 진단; Lean 미형식화",
    "58.13": "exp(-2) 이후 추가 finite-error slack 고정밀 진단; Lean 미형식화",
    "58.14": "낙관 C_PAP=1, D=186 coefficient 진단; Lean 미형식화",
    "58.15": "낙관 C_PAP=1, D=187 coefficient 진단; Lean 미형식화",
    "58.16": "현재 downstream 식의 낙관 integer-D capacity 결론; source 채택 전 Lean 미형식화",
    "59.1": "DEP-R09 Branch S의 fixed-D finite pointwise PAP 목표; analytic source package 없음",
    "59.2": "D=160 coefficient·total-error 고정밀 진단; Lean 미형식화",
    "59.3": "Thorner-Zaman Theorem 2.1 density source 진술; multiplier·cutoff 미형식화",
    "59.4": "숨은 multiplier를 보존하는 fixed-D transfer 진단 정의",
    "59.5": "positive K, eta, D의 logarithmic budget에서 exponential error 상계를 커널 검증",
    "59.6": "K별 최소 decay constant 80-dps 진단; Python 재계산",
    "59.7": "Jutila Theorem 1 density source 진술; epsilon multiplier·cutoff 미형식화",
    "59.8": "Thorner-Zaman Remark 2.4의 density exponent-to-theta source 관계",
    "59.9": "Jutila Theorem 1-prime source 진술; sufficiently large D cutoff 미수치",
    "59.10": "Jutila Theorem 2 source 진술; D0(epsilon)와 proof multiplier 미수치",
    "60.1": "Ramaré--Zuniga explicit coefficient의 actual tau=8/5 exact 대입을 커널 검증",
    "60.2": "Graham--Jutila Lemma 4 full asymptotic source theorem; hidden O multiplier는 미형식화",
    "60.3": "Ramaré--Zuniga Corollary 1.3 source theorem; actual 호출의 analytic proof는 미형식화",
    "60.4": "Jutila Theorem 1-prime actual parameter 정의 전사",
    "60.5": "finite log-ratio의 exact 유리 대수를 커널 검증",
    "60.6": "finite power correction의 exponent 대수만 커널 검증; source real-power 합성은 미형식화",
    "60.7": "finite delta cutoff sufficient condition; 후속 JL5/6/8 예산과 함께 형식화 예정",
    "60.8": "Jutila Lemma 5 source asymptotic; uniform o(1) rate와 cutoff는 OPEN",
    "60.9": "Jutila Lemma 6 detector lower bound; Mellin과 tail 상수는 OPEN",
    "60.10": "Jutila Lemma 7 modified Halasz source statement; finite proof는 후속",
    "60.11": "Jutila Lemma 8 local zero-count source statement; implied constant는 OPEN",
    "60.12": "Huxley--Jutila exponent-2 source density; epsilon multiplier와 cutoff는 OPEN",
    "62.1": "Jutila 식 (2.11)의 source Mellin identity; complex analytic theorem은 Lean 미형식화",
    "62.2": "우측 contour line 선택; residue·수평변 complex analysis는 Lean 미형식화",
    "62.3": "actual M bound의 두 local 실수부등식만 커널 검증; 전체 character polynomial은 미형식화",
    "62.4": "n/phi(n) 합과 Euler-product multiplier 3은 문서·exact Python 검산; Lean 부분형식화",
    "62.5": "4/sqrt(6) 보정의 제곱 유리값만 커널 검증; primitive 유도식은 미형식화",
    "62.6": "Bennett et al. Lemma 5.6 (5.3)의 Rademacher convexity source theorem",
    "62.7": "vertical L bound 중 real triangle budget만 커널 검증",
    "62.8": "Gamma recurrence·integral에서 얻는 pointwise source/direct-proof bound",
    "62.9": "Gamma 적분 split의 유한 계수 합성만 커널 검증",
    "62.10": "직접 Mellin 상수 합성은 문서·100-dps Python 검산; full complex integral 미형식화",
    "62.11": "delta_epsilon 정의와 0<delta<1/4를 커널 검증",
    "62.12": "alpha>=1/2, beta>=alpha에서 exponent <=-epsilon/2를 커널 검증",
    "62.13": "source power condition에서 최종 real-power transfer; exponent만 커널 검증",
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
        "- 생성 기준: 2026-09-13 KST",
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
            "2. 현재 root DEP-R09의 exact source 진술과 finite-rate 의무를 먼저 고정한다.",
            "3. DEP-R09에서 실제 사용할 상수·부등식·endpoint 합성을 사용 전에 형식화한다.",
            "4. 이후 DEP-R10, R11, R12를 같은 source-first·역의존 순서로 처리한다.",
            "5. Theory 55의 잔여 source theorem과 Theories 10–11의 별도 finite-set 구조는",
            "   해당 DAG에서 다시 필요해질 때 독립 batch로 처리한다.",
            "6. 960개라는 총개수를 선행 gate로 쓰지 않는다. empirical·역사적·대체 식은 root-critical 식 뒤로 미룬다.",
            "7. source analytic theorem은 먼저 Mathlib/선행 형식화를 찾고, 없으면",
            "   `SOURCE_THEOREM_UNFORMALIZED`로 차단한 뒤 별도 장기 증명 단위로 분해한다.",
            "8. DEP-R09–R12와 end-to-end composition이 닫힌 뒤 비임계 잔여 coverage를 순차 처리한다.",
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
