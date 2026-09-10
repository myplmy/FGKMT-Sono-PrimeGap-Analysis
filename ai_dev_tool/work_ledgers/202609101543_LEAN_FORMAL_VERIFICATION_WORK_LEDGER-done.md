# Lean 전수 수식·정리 형식검증 작업원장

- 시작: 2026-09-10 15:43 KST
- 현재 상태: COMPLETE
- 사용자 승인: 사용자가 구축한 `lean/` 프로젝트를 감사하고 설치 버전·commit을 고정한 뒤,
  필요한 디렉터리 구조, 전수 수식 원장과 단일 Lean 파일을 구축하며 Lean 커널 검증을 수행
- 금지·보류: actual prime sweep, threshold calculator, 외부 게시, push/PR, `sorry`·무표시
  project axiom으로 가짜 독립증명 생성, 선행 분석정리를 커널 검증으로 과장
- 선행 변경: 시작 HEAD `9c23d19ee3b5c231fa510e3e188c45fea2f97316`, branch `main`.
  시작 `git status --short`에는 사용자가 구축한 untracked `lean/`만 존재했다. 그 아래
  `.lake/`는 `lean/.gitignore` 대상이며 사용자 설치 cache로 보존한다.

## 목적과 완료조건

- 목적: `docs/method/theory/`의 현재 theory와 명시적 식을 전수 식별하고, 각 항목의 Lean
  전사·증명·의존 상태를 한 원장에 기록하며, 하나의 연구 Lean 파일에서 검증 가능한 핵심
  명제를 실제 커널로 검사한다.
- 완료조건:
  1. Lean·Mathlib·모든 transitive dependency가 tag가 아닌 manifest commit으로 고정·기록된다.
  2. 현재 theory 문서 목록과 모든 명시적 `\\tag{...}` 식이 source line과 함께 원장에 등록된다.
  3. `KERNEL_PASS`, `CONDITIONAL_KERNEL_PASS`, `SOURCE_THEOREM_UNFORMALIZED`,
     `DEFINITION_ONLY`, `NOT_YET_FORMALIZED`를 혼동하지 않는다.
  4. theory별 파일을 만들지 않고 단일 `FGKMTSono/TheoryVerification.lean`에 원문 theory·식번호
     주석을 붙인다.
  5. 최신 theory 55를 포함한 1차 dependency-critical 유한 명제들이 `lake build`와 직접
     `lake env lean`에서 통과하고 `sorry`가 0건이다.
  6. 전수 원장 coverage 검사, Lean 선언-원장 연결 검사, Git 정적 검사가 통과한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | 원문 식을 임의 단순화하지 않고 formalization scope와 가정을 명시한다. |
| 데이터·provenance | 직접 영향 없음 | 실제 dataset·`test_result`를 읽거나 변경하지 않는다. theory 파일 경로·line·SHA-256을 기록한다. |
| 통계·정밀도 | 직접 영향 없음 | 수치 실험이 아니라 symbolic kernel 검증이다. decimal 근사는 exact rational statement와 분리한다. |
| 승인 경계 | 영향 있음 | 사용자가 승인한 Lean 구축·bounded 검증만 수행한다. 설치 갱신·장시간 build가 새로 필요하면 중단한다. |
| 산출물·비덮어쓰기 | 영향 있음 | 사용자 `lean/` 프로젝트를 보존하고 기존 파일의 목적을 확인한 뒤 최소 패치한다. `.lake/`는 commit하지 않는다. |
| 증거 수준 | 핵심 영향 | Lean이 가정에서 결론을 유도한 것과 선행 analytic theorem 자체를 독립 증명한 것을 구분한다. |

## 단계 현황

1. **COMPLETE — 사용자 Lean 프로젝트·설치 상태 읽기 전용 감사**
2. **COMPLETE — version·commit pin과 형식검증 디렉터리 계약 구축**
3. **COMPLETE — theory·display 수식 전수 inventory 생성**
4. **COMPLETE — 단일 Lean 파일의 foundational·최신 dependency-critical 명제 형식화**
5. **COMPLETE — kernel·no-sorry·dependency·coverage·전체 회귀 검증**
6. **COMPLETE — 원장 상태·프로젝트 문서·handoff 동기화(로컬 commit은 이름 변경 뒤)**

## 단계별 기록

### 2026-09-10 15:43 KST — 사용자 Lean 프로젝트 감사

- 수행: `lean/`의 toolchain, Lake 설정, manifest, source와 ignore 규칙을 읽고 build를 실행했다.
- 파일: 사용자 선행 `lean/lean-toolchain`, `lean/lakefile.toml`, `lean/lake-manifest.json`,
  `lean/FGKMTSono.lean`, `lean/FGKMTSono/Basic.lean`.
- 명령·검증:
  - `C:\\Users\\Uranus\\.elan\\bin\\lake.exe env lean --version`
  - `C:\\Users\\Uranus\\.elan\\bin\\lake.exe build`
  - theory Markdown과 `\\tag{...}` read-only inventory
- 결과: Lean 4.34.0-rc2, kernel commit
  `6a10ac8c22beadecabdbb0919c2b50214762f91d`; Mathlib manifest commit
  `85e3a25e006c35636f0e53b0e9296caca2685bc0`; `lake build` exit 0.
  theory Markdown 56개(색인 포함), 명시적 tag 512개, unique 512개, duplicate 0개.
- 문제·결정: `lakefile.toml`은 Mathlib tag `v4.34.0-rc2`를 가리키므로 full commit pin으로
  바꿔야 한다. 기본 `hello := "world"`는 사용자 smoke scaffold이며 연구 파일로 교체한다.
- 다음 재개점: `lean/lakefile.toml`의 Mathlib rev를 manifest full commit으로 고정하고,
  provenance 문서와 단일 Lean library entry를 설계한다.

### 2026-09-10 15:50 KST — pin·초기 inventory와 발견 오류 교정

- 수행: Mathlib dependency를 full commit으로 고정하고 README·verification/tools 구조와 단일
  Lean 파일 진입점을 만들었다. Markdown fenced code 밖 display math를 전수 스캔했다.
- 파일: `lean/lakefile.toml`, `lean/lake-manifest.json`, `lean/README.md`,
  `lean/verification/README.md`, `lean/tools/inventory_theory_formulas.py`,
  `lean/FGKMTSono.lean`, `lean/FGKMTSono/TheoryVerification.lean`, theory 27.
- 명령·검증:
  - FGKMT Python `py_compile` PASS.
  - 최초 inventory: display block 1,000개, issue 2개.
  - pin 뒤 manifest Mathlib input/rev 모두
    `85e3a25e006c35636f0e53b0e9296caca2685bc0` 확인.
- 결과: theory 27에서 누락된 display 종료 delimiter 5개를 발견했다. 처음에는 식 27.9–27.13에
  각 `\\]`를 복원했으나, 후속 theory 46 계약이 theory 27 원문 SHA-256을 고정한다는 사실을
  확인해 이 소급 변경은 되돌렸다. inventory에서 tag 뒤 빈 줄만 implicit close로 복구하고
  다섯 식을 `PARSE_REVIEW_REQUIRED`로 남기는 provenance-safe 방식을 채택했다.
- 문제·결정: `FGKMTSono.lean` import 변경과 아직 생성되지 않은 target 파일의 build를 병렬로
  실행해 최초 build가 `no such file ... TheoryVerification.lean`으로 실패했다. dependency나
  기존 build 오류가 아니라 작업 순서 오류다. 빈 namespace를 가진 target을 생성했으며 다음
  단계에서 build를 반드시 재실행한다. Windows console의 비ASCII JSON 손상도 확인해 inventory
  stdout을 ASCII-escaped JSON으로 바꿨다.
- 다음 재개점: inventory를 재실행해 issue 0, 512 tagged 식과 전체 display block 수를 확정한다.

### 2026-09-10 16:20 KST — 전수 inventory·검증 원장 확정

- 수행: fenced code 밖의 bracket/dollar/environment display math를 전수 스캔하고, 원문 식번호가
  없는 항목에는 `T<theory>-U<ordinal>` ID를 부여했다. 생성기와 독립 validator를 추가했다.
- 파일: `lean/tools/inventory_theory_formulas.py`,
  `lean/tools/generate_verification_ledger.py`,
  `lean/tools/validate_verification_ledger.py`,
  `lean/verification/formula_inventory_v1.json`,
  `lean/verification/verification_status_v1.json`, `lean/VERIFICATION_LEDGER.md`.
- 결과:
  - theory Markdown 56개, display 수식 1,005개
  - tagged 512개, untagged synthetic-ID 493개, parse issue 0
  - Theory 27의 안전 복구 5개만 `PARSE_REVIEW_REQUIRED`
  - 상태 행: `KERNEL_PASS` 9, `CONDITIONAL_KERNEL_PASS` 8, `DEFINITION_ONLY` 4,
    `PARTIAL_FORMALIZATION` 6, `NOT_YET_FORMALIZED` 973, parse review 5
  - 생성기를 연속 재실행해 inventory·Markdown ledger SHA-256 불변 확인
- provenance: Theory 27은 downstream 고정 SHA-256
  `e138f7792551ce05822064e0a2c59777301f4fa5e53edd286e6abdf0c060ff12`로 복원했고
  Git content diff 0이다. Theory 01의 `qquad` 오자는 `\\qquad`로 교정했으며 전체 회귀가
  source-hash 의존성 포함 PASS했다.
- 다음 재개점: 단일 Lean 파일의 실제 kernel 검사와 전체 build를 완료한다.

### 2026-09-10 16:33 KST — 단일 Lean 파일 초기 batch kernel 검증

- 수행: `lean/FGKMTSono/TheoryVerification.lean` 한 파일에 Theory 01·07·10·11 및 최신
  Theory 55의 기초 정의, 유한 집합 논리, floor/ceil, exact rational·최종 대수 합성을
  38개 declaration으로 형식화했다. 모든 declaration 주석에 theory·formula ID를 연결했다.
- 포함 범위:
  - iterated natural log와 FGKMT scale 전개
  - canonical end-prime eligibility와 정수 plateau 오른쪽 경계
  - local `li-pi` 항등식·상계 방향·정수 floor
  - candidate/witness coverage soundness와 strict boundary arithmetic
  - modulus-lift transition monotonicity
  - Theory 55 equal-grid width, restoration/error budget, 순차 존재, exact rational slack,
    smooth 정수 상수와 최종 상계 합성
- 명령·결과:
  - `lake env lean FGKMTSono\\TheoryVerification.lean`: exit 0
  - `lake build FGKMTSono`: 8,765 jobs, exit 0, warning 0
  - executable Lean source의 `axiom|sorry|admit`: 0
- 경계: analytic source premise를 받은 8행은 `CONDITIONAL_KERNEL_PASS`다. 이 초기 batch는
  전체 Sono/FMT 정리나 `X_cert`를 증명하지 않으며 DEP-R09–R12는 OPEN이다.
- 다음 재개점: 기계 원장 validator, 전체 Python 회귀, 정적 검사를 수행한다.

### 2026-09-10 16:40 KST — validator·전체 회귀·정적 검사

- validator: formula 1,005행 exact order/coverage, 38 declaration 존재, 금지 proof escape 0,
  toolchain pin, local Markdown link 1,064개를 issue 0으로 검증했다.
- Python 전체 회귀:
  - sandbox 최초 실행: 임시 디렉터리 권한 때문에 664 tests 중 82 errors. 코드 결과로 채택하지 않음.
  - 사용자가 허가한 정상 로컬 권한 재실행: `Ran 664 tests in 89.441s`, `OK`, exit 0.
- 정적 검사: `git diff --check` PASS; generated source/ledger 등 text 22개 strict UTF-8·금지
  control character issue 0; Mathlib local HEAD와 lakefile/manifest pin
  `85e3a25e006c35636f0e53b0e9296caca2685bc0` 일치.
- 정리: 실패한 sandbox suite가 만든 정확한 임시 디렉터리 16개와 ignored Python
  `__pycache__`만 안전한 절대경로 확인 뒤 제거했다. 연구 입력·actual artifact 삭제는 없다.
- 오류 공개: build 순서, Theory 27 provenance 복원, parser 과잉복구, sandbox 82 errors,
  경로·PowerShell 보간·binary text-scan 실수는 오류 원장 E082에 기록했다.
- 다음 재개점: AGENTS/README·handoff를 동기화하고 exact allowlist를 staging해 로컬 commit한다.

### 2026-09-10 16:47 KST — 정본·handoff 동기화

- 수행: `AGENTS.md`에 Lean 증거 경계와 정본 경로를 추가하고, Lean README에 원장 재생성·검증
  명령을 기록했다. 새 `handoff/202609101647_HANDOFF.md`에 현재 상태, 비목적, 검증, 위험,
  사용자 절차, 다음 우선순위와 commit 메시지를 적었다.
- 결과: 사용자 요청 산출물·검증·문서 동기화가 완료됐다. 새 actual 결과가 없으므로
  `test_result` 색인과 `docs/METHODS.md`는 변경하지 않는 것이 맞다.
- 다음 재개점: 이 파일을 안전 절차에 따라 `-done.md`로 이름 변경하고 exact allowlist를
  staging해 로컬 commit한다.

## 현재 재개점

이 파일을 `202609101543_LEAN_FORMAL_VERIFICATION_WORK_LEDGER-done.md`로 이름 변경하고,
exact allowlist만 staging하여 로컬 commit한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 조건부/독립 kernel PASS 상태 분리
- [x] 결과 색인·METHODS/이론 정본 동기화 필요성 판정(새 actual 결과 없음; 색인/METHODS 변경 불필요)
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
