# DEP-R09 JL6c common detector error budget 작업원장

- 시작: 2026-09-13 13:29 KST
- 현재 상태: COMPLETE — rename·stage·local commit 직전
- 직전 commit: `15b875707bc8beadd4e4b7cc9d1e7bbafc770339`
- 사용자 승인: `X_cert` 계산기 전 source-first 정규화·증명, 필요한 문헌 확보,
  필요시 Lean 형식화·검증, 정본·handoff와 단계별 로컬 stage/commit
- 금지·보류: actual prime sweep, threshold calculator, 숨은 implied constant 임의 선택,
  30분 이상 계산, 새 package 설치, source theorem의 project-local axiom화
- 시작 상태: worktree clean, 진행 중 비 `-done` 원장 없음

## 목적과 완료조건

- 목적: Theory 61의 JL5 relative loss, Theory 62의 Mellin absolute error, Theory 63의
  actual truncation-tail absolute error와 원문 감쇠 loss가 Jutila Lemma 6의 실제 detector
  lower bound에 어떤 부호·정규화로 들어가는지 원문에서 고정하고, 하나의 계산 가능한
  오차예산과 공통 finite cutoff로 합성한다.
- 완료조건:
  1. Jutila 식 (2.8)--(2.12)와 Lemma 6의 main term, 두 error, JL5 사용 위치를
     원문 페이지·식 번호·endpoint까지 재고정한다.
  2. absolute error를 relative main-term loss로 바꿀 때 필요한 하한과 coefficient를
     누락 없이 명시한다.
  3. actual `R,z1,z2,X`에서 JL5·감쇠·Mellin·tail의 충분조건을 하나의
     `D_0(epsilon, budget)`으로 합치거나, 불가능하면 정확한 남은 blocker를 증거와 함께
     남긴다.
  4. 인쇄된 일반 Lemma와 actual application을 분리하고 JL8·PAP-11·fixed `2e-17`·
     `X_cert`를 자동 승격하지 않는다.
  5. dependency-critical 유한 대수는 필요한 범위만 Lean 단일 파일에 형식화하고,
     `sorry`, `admit`, project-local `axiom`을 사용하지 않는다.
  6. Python fail-closed evaluator·회귀시험, machine ledger, theory/review·정본·handoff를
     동기화하고 전체 검증 뒤 로컬 commit한다.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | dataset, P002--P020 결과와 figure를 변경하지 않는다. |
| JL6 actual proof DAG | 직접 핵심 영향 | JL5/Mellin/tail의 단위와 부호를 식별한 뒤에만 합산한다. |
| printed general JL6 | 확인 필요 | actual upper envelope 결과를 general uniform statement로 확대하지 않는다. |
| fixed `2e-17`·`X_cert` | 간접 핵심 영향 | JL6만 닫혀도 JL8·PAP가 남으므로 OPEN을 유지한다. |
| provenance | 직접 영향 | OCR 전사와 렌더링 원페이지를 대조하고 source hash를 보존한다. |
| Lean | 확인 필요 | analytic theorem이 아니라 budget·cutoff 유한 대수만 후보로 삼는다. |
| 사용자 계산자원 | 현재 영향 없음 예상 | 30분 이상 연산·새 dependency가 필요하면 실행하지 않고 요청한다. |

## 접근 비교

| 접근 | 정확성·재현성 | 비용·위험 | 판정 |
|---|---|---|---|
| A. Jutila 원래 proof의 actual parameter와 error 흡수를 그대로 명시화 | 원 의존성과 가장 잘 맞음 | 인쇄된 `O`·`<<`가 추가로 나타날 수 있음 | 1순위 |
| B. JL5/Mellin/tail 각각에 독립 임의 예산을 배정 | 구현은 간단 | main term 정규화가 다르면 잘못된 합성 가능 | 원문 확인 전 금지 |
| C. detector lemma를 새 smoothing으로 재설계 | 더 나은 상수 가능 | branch 전체 proof 변경과 새 source 의무 발생 | 현재 비권장 |

## 단계 현황

1. **COMPLETE — 원문 식·main/error 정규화와 actual parameter 재고정**
2. **COMPLETE — source-first 흡수 정리 조사 및 공통 budget 도출**
3. **COMPLETE — Python/machine ledger/test와 필요한 Lean 형식화**
4. **COMPLETE — theory/review·정본·색인 동기화**
5. **COMPLETE — 전체 검증·새 handoff·완료 원장·로컬 commit 준비**

## 단계별 기록

### 2026-09-13 13:29 KST — 시작

- 직전 goal turn은 Theory 63, Lean/Python 검증과 commit을 남겼으므로 `progress`다.
- 최신 handoff를 현재 파일에서 다시 확인했고 worktree가 clean임을 확인했다.
- 직전 handoff 식의 `D=qT` 뒤 `\\qquad`가 `qquad`로 손상된 것을 발견했다. 이는 설명
  문서의 LaTeX 오탈자이며 Theory 63·코드·검증식에는 영향이 없다. 이번 단계에서 교정하고
  오류 원장에 숨김없이 기록한다.
- 다음 재개점: Jutila audit PDF의 인쇄 pp. 50--52를 원페이지/OCR로 다시 대조해 식
  (2.8)--(2.12), Lemma 6의 최종 lower bound와 실제 parameter 흡수 순서를 전사한다.

### 2026-09-13 — 단계 1 완료: 원문 정규화 재고정

- Jutila 원본 인쇄 pp. 50--52를 OCR locator와 렌더링 원페이지로 다시 대조했다.
  식 (2.11)은 절단 전 정확히
  `M + g + E_tail = I`, `M=exp(-1/X) S_q(R)`이므로
  `|g| >= M-|I|-|E_tail|` 방향이다.
- 원문 식 (2.10)의 최종 계수는
  `C_phi=(6/pi^2) phi(q)/q`이고, actual p.52 선택은
  `D=qT`, `R=D^theta`, `z1=D^(1/2+7theta)`,
  `z2=D^(1/2+8theta)`, `X=D^(1+12theta)`다.
- 인쇄 p.51은 해당 proof branch에서 `alpha>=1-theta`를 먼저 고정한다. 따라서
  식 (2.8)의 actual exponent margin은
  `(1-theta)(1+12theta)-(1+theta)(1+9theta)=theta(1-21theta)`이고
  `0<theta<=1/21`이면 비음수가 아니다.
- 기존 예상의 세 budget 외에 `exp(-1/X)`가 만드는 별도 relative loss를 발견했다.
  공통 budget은 JL5 source error, exponential damping, Mellin integral, truncation tail의
  네 항이어야 한다. 이 항을 빼면 식 (2.10)의 `1-theta`를 엄밀히 보존할 수 없다.
- Zuniga Alterman Corollary 3.4(b) 원문 text layer와 Rosser--Schoenfeld 인쇄 p.72
  Theorem 15 식 (3.41)--(3.42) 원페이지를 확인했다. 후자는 유일한 예외에도
  coefficient `2.50637`을 주므로 exact small-q check와 합쳐 uniform
  `q/phi(q)<=6 log D` 충분상계를 만들 수 있다.
- 다음 재개점: 네 positive budget의 합이 최종 loss 이하가 되도록 하고, JL5의
  `B_q`, `C_phi`, Mellin·tail absolute error를 같은 `C_phi log R` 단위로 바꾸는
  공통 `L_0(theta,budgets)`를 도출한다.

### 2026-09-13 — 단계 2 완료: 네 loss와 공통 cutoff 도출

- 최종 source coefficient를 되찾으려면
  `eta_5+eta_X+eta_M+eta_T<=eta_out<=theta`가 필요함을 고정했다. 초기에 만든
  evaluator는 `eta_out`과 `theta`의 관계를 강제하지 않았으나 첫 수치 검토에서 이를
  발견해 `eta_out<=theta` fail-closed validation으로 즉시 교정했다. 잘못된 조건의 값은
  정본·보고서·결론에 사용하지 않았다.
- Rosser--Schoenfeld와 `q=3,...,15` exact check로 `L=log D>=e`에서
  `q/phi(q)<=6L`, 따라서 `1/C_phi<=pi^2 L`을 얻었다.
- Zuniga Alterman의 `B_q`에는 local factor `<=exp(p^(-2/3))`, distinct-prime count
  `omega<=L/log 2`를 적용해
  `B_q<=exp(3(L/log 2)^(1/3))`을 얻었다.
- `L>=(18/(theta*(log 2)^(1/3)))^(3/2)`이면 위 exponent가 `theta L/6`
  이하가 된다. 이를 JL5, damping, Mellin, tail의 각각 계산 가능한 cutoff와 합쳐
  여덟 항 max인 공통 `L_0`을 도출했다.
- `theta=1/100`, 각 loss `theta/4`의 120-dps 진단은
  `L_0=91726.7544311060566...`이며 `B_q` uniformization 항이 지배적이다.
  이는 JL6 한 단계의 보수적 충분조건이지 numerical `X_cert`가 아니다.
- 다음 재개점: evaluator·machine ledger·fail-closed test와 dependency-critical Lean
  대수를 완성하고 status inventory를 생성·검증한다.

### 2026-09-13 — 단계 3 완료: evaluator·machine ledger·Lean

- `source/dep_r09_jutila_jl6_common_budget.py`에 네 loss, 여덟 cutoff와 fail-closed
  상태 evaluator를 구현했다. mpmath 출력은 directed interval certificate가 아니라는
  경계를 보존했다.
- machine ledger `Sono_FMT_DEPR09_Jutila_Lemma6_common_budget_v1.json`에 세 source의
  경로·SHA-256·bytes·읽기 방식, identity, budget, cutoff와 OPEN 상태를 고정했다.
- 신규 10시험과 JL5--JL6 관련 총 38시험이 PASS했다. 첫 boundary 시험은 mpmath가 같은
  대수값을 마지막 자리에서 서로 다른 방향으로 반올림해 2 case가 실패했다. 이는 proof
  실패가 아니므로 directed 부등호로 강제하지 않고 `mp.almosteq`를 함께 요구하도록
  교정했으며 재실행 10/10 및 관련 38/38 PASS를 확인했다.
- Lean 단일 파일에 actual power margin, damping product, four-part conditional transfer,
  source coefficient 회복, terminal `B_q` exponent 흡수를 추가했다. direct compile exit 0,
  inventory generator와 validator가 PASS했다.
- Theory 64 추가 뒤 현재 inventory는 theory 65개, display 1,142식, declaration 148개다.
  상태는 `KERNEL_PASS=42`, `CONDITIONAL_KERNEL_PASS=23`, `DEFINITION_ONLY=20`,
  `PARTIAL_FORMALIZATION=22`, `SOURCE_THEOREM_UNFORMALIZED=36`,
  `NOT_YET_FORMALIZED=994`, `PARSE_REVIEW_REQUIRED=5`, 금지 proof escape 0건이다.
- status JSON을 수동 patch한 첫 초안에 두 JSON key 오탈자와 두 declaration 명칭 불일치가
  들어갔으나 strict JSON parse 전에 즉시 발견·교정했다. 손상 상태는 원장 생성·판정·commit에
  사용하지 않았다.
- 다음 재개점: Theory 64/review 71을 predecessor와 AGENTS, METHODS, theory·문헌 색인,
  Lean README에 동기화하고 handoff LaTeX 오탈자 및 오류 원장을 교정한다.

### 2026-09-13 — 단계 4 완료: 정본·색인 동기화

- Theory 64와 쉬운 review 71을 신설하고 source identity, 네 budget, 여덟 cutoff,
  수치 진단과 정확한 OPEN 경계를 기록했다.
- Theory 60--63과 review 67--70에 후속 snapshot note를 추가해 과거 component 단계의
  OPEN 문구가 현재 상태로 오해되지 않게 했다. 과거 machine ledger의 당시 상태는
  provenance이므로 소급 덮어쓰지 않았다.
- AGENTS, METHODS, theory index, 문헌 종합, Lean README를 최신 정본 theory 64·review 71과
  inventory 65문서/1,142식/148 declaration에 맞췄다.
- 직전 handoff의 `D=qT` 앞 LaTeX backslash 한 글자를 교정했다. 이번 조건 누락,
  broad tmp 검색, floating equality, patch/status JSON 초안 오류를 오류 원장 E112에
  영향 범위와 예방책까지 기록했다.
- 다음 재개점: inventory 재생성, targeted/full Python, direct/full Lean, UTF-8·control·
  local-link·JSON·diff 감사를 실행하고 결과로 handoff와 완료 원장을 작성한다.

### 2026-09-13 — 단계 5 완료: 전수 검증·handoff·commit 준비

- 고정 FGKMT Python에서 신규 10/10, JL5--JL6 관련 38/38, 전체 727/727 unittest가
  PASS했다. 전체 quiet 재검증은 64.733초였고 exit 0이다.
- 신규 Python source/test의 `py_compile`, machine/status/inventory JSON 3개 strict parse,
  Lean ledger generator·validator가 PASS했다. validator는 theory 65개, display 1,142식,
  declaration 148개와 금지 proof escape 0건을 확인했다.
- `lake env lean FGKMTSono/TheoryVerification.lean` direct compile과 전체 `lake build`
  8,765 jobs가 PASS했다. `sorry`, `admit`, project-local `axiom`은 사용하지 않았다.
- 변경 파일 26개의 strict UTF-8·금지 control 문자와 변경 Markdown local link 1,424개를
  검사해 issue 0이었다. `git diff --check`도 whitespace error 0이며 Git line-ending
  warning만 관측했다.
- 새 handoff `handoff/202609131404_HANDOFF.md`에 쉬운 설명, 정확한 상태 경계,
  검증 증거, 사용자 절차, 다음 우선순위와 한국어 commit 메시지를 기록했다.
- 첫 sandbox staging은 `.git/index.lock: Permission denied`로 거부됐다. 파일 영향은 없었고
  사용자에게 보고한 뒤 허가된 Git stage만 외부 권한으로 재실행해 cached diff 검사를
  통과했다.
- 실제 prime sweep·threshold calculator·장시간 계산·dependency 설치는 수행하지 않았다.
- 최종 local commit은 한국어 제목 `DEP-R09 Jutila Lemma 6 actual 공통 오차예산 명시화`로
  성공했다. 이 원장은 같은 commit 안의 자기 상태를 기록하므로 hash 문자열은 넣지 않고
  Git history를 정본으로 삼는다. push는 수행하지 않았다.
- 다음 재개점: Jutila Lemma 8의 local zero-count source, 정확한 square/rectangle,
  numerical multiplier와 finite range를 원문부터 고정한다.

## 완료 전 점검

- [x] 원문 main/error/JL5 사용 위치 고정
- [x] actual/general 적용범위 분리
- [x] 공통 budget·finite cutoff 또는 정직한 blocker 판정
- [x] machine ledger·test·필요한 Lean 완료
- [x] PAP-11·DEP-R09·fixed coefficient·X_cert fail-closed
- [x] 정본·색인·오류 원장 동기화
- [x] 전체 unittest·Lean·UTF-8·local links·diff 검증
- [x] 새 timestamp handoff 작성
- [x] 파일명을 `-done.md`로 변경
- [x] 이번 작업만 명시 stage·local commit, push 없음
