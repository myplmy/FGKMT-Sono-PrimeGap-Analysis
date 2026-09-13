# DEP-R09 JL6a Mellin integral source audit 작업원장

- 시작: 2026-09-13 12:02 KST
- 현재 상태: COMPLETE
- 직전 commit: `a281ba8569ef9067ad8952310be6e039763e8ffc`
- 사용자 승인: `X_cert` 계산기 이전의 source-first 정규화·증명, 필요한 문헌 확보,
  Lean 형식화·검증, 문서·시험·handoff와 단계별 로컬 stage/commit
- 금지·보류: actual prime sweep, threshold calculator, 숨은 implied constant 임의 선택,
  장시간 연산, 새 package 설치, source theorem의 project-local axiom화
- 선행 변경: 시작 worktree clean; 이번 작업 비소유 변경 없음

## 목적과 완료조건

- 목적: Jutila 1977 Lemma 6의 zero-detector lower bound에 들어가는 Mellin 적분 항을
  원문과 인용 source까지 추적하고, actual 매개변수에서 유한 절대상수와 cutoff를 줄 수
  있는지 source-first로 판정한다.
- 완료조건:
  1. Jutila 식 (2.10)--(2.11), Lemma 6 proof와 필요한 함수·contour·매개변수를 원페이지로 고정한다.
  2. 인용되었거나 같은 적분을 다루는 검증된 선행정리를 우선 조사해 exact statement를 대조한다.
  3. drop-in explicit theorem이 없으면 원 proof를 elementary inequalities로 정량화할 수 있는지 증명한다.
  4. Mellin integral과 별도 truncation tail을 섞지 않고 상태·상수·cutoff를 machine-readable하게 남긴다.
  5. dependency-critical 유한 대수는 필요할 때만 Lean 단일 파일에 형식화하며 source theorem을 axiom화하지 않는다.
  6. JL6 전체·JL8·PAP-11·DEP-R09·fixed `2e-17`·`X_cert`는 근거 없이 승격하지 않는다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | empirical source·dataset·result를 변경하지 않는다. |
| JL5/JL6 proof DAG | 직접 영향 | JL5 완료 상태, Mellin 항, truncation tail, JL6 종단 합성을 별도 node로 둔다. |
| fixed `2e-17`·`X_cert` | 간접 핵심 영향 | 한 하위항이 닫혀도 root certificate를 닫지 않는다. |
| analytic uniformity | 핵심 위험 | 고정 epsilon/q/T 명제를 uniform theorem으로 확대하지 않는다. |
| provenance | 핵심 영향 | PDF text/OCR 분류, page/equation/version/hash를 기록하고 렌더링 원문과 대조한다. |
| Lean | 확인 필요 | 유한 대수·초등 부등식만 후보이며 외부 Mellin theorem은 source 상태로 둔다. |
| 사용자 계산자원 | 현재 불필요 | 30분 이상 연산 또는 새 dependency가 필요하면 사용자에게 요청하고 중단한다. |

## 접근 비교와 선택

| 접근 | 정확성·재현성 | 비용·위험 | 순서 |
|---|---|---|---|
| A. Jutila가 인용한 원 정리의 explicit version | 원 proof와 가장 가깝고 함수·contour mismatch가 적음 | 원 source가 비명시적일 수 있음 | 1순위 |
| B. 현대 explicit Mellin/Laplace bound | 상수와 cutoff가 인쇄돼 있으면 즉시 대입 가능 | kernel·weight·strip 조건이 다를 수 있음 | 2순위 |
| C. 식 (2.11)을 직접 적분 부등식으로 재증명 | 모든 상수를 통제 가능 | contour 이동·Gamma tail을 빠뜨릴 위험과 문서량 큼 | A/B 실패 시 |

## 단계 현황

1. **DONE — Jutila JL6 원문 statement·proof·인용 source 고정**
2. **DONE — explicit 선행연구와 actual parameter 적합성 조사**
3. **DONE — Mellin integral 유한 상수·cutoff 도출; truncation tail은 분리 유지**
4. **DONE — Theory/review/machine ledger/test 및 필요한 Lean 형식화**
5. **DONE — 정본 동기화·전체 검증·handoff·로컬 commit 준비**

## 단계별 기록

### 2026-09-13 12:02 KST — 시작

- 수행: 최신 handoff, Theory 60--61, impact-analysis·plan-doc·PDF·handoff·commit 규약과
  clean worktree를 확인했다.
- 결과: 이전 JL5 단계는 authoritative commit과 검증이 있는 progress이며, 첫 미완료 node는
  `JL6a Mellin integral`이다.
- 다음 재개점: Jutila PDF의 인쇄 pp. 49--51에서 식 (2.10)--(2.11)과 Lemma 6 proof를
  OCR/native text 및 렌더링 원페이지로 다시 고정하고 bibliography의 직접 인용을 식별한다.

### 2026-09-13 — 단계 1 완료: 원문 고정

- Jutila PDF native text layer가 18 bytes뿐임을 재확인하고, OCR은 탐색용으로만 쓴 뒤
  인쇄 pp. 48--52 렌더링 원페이지에서 식 (2.1), (2.5)--(2.11), Lemma 6과 actual
  parameter 선택을 대조했다.
- 원문 인용은 Prachar 1957 p. 380 Satz 3.2다. 공개본은 OpenLibrary/Internet Archive의
  제한 대출본만 식별되어 우회하지 않았다.
- Mellin 적분 오차와 `x=X log^2(qT)` 이후 truncation tail은 서로 다른 두
  `<<_epsilon 1`임을 고정했다.

### 2026-09-13 — 단계 2 완료: source-first 대체자료 감사

- Bennett--Martin--O'Bryant--Rechnitzer, Math. Comp. 90 (2021), Lemma 5.6 식 (5.3)의
  Rademacher convexity bound를 native text와 인쇄 p. 1469에서 대조했다.
- Rademacher 1959 원문 metadata·DOI는 식별했지만 공개 full text는 확보하지 못했다.
  따라서 peer-reviewed Bennett et al.의 exact restatement와 NIST DLMF의 Mellin/Gamma
  공식으로 필요한 범위를 교차검증한다.
- Fiori 2026의 Phragmen--Lindelof correction을 확인했다. 그 논문의 경고 대상은
  `|log(Q+s)|` 처리이며, 이번에 쓰는 Bennett 식의 `|s+1|` power는 그 특정 오류가 아니다.

### 2026-09-13 — 단계 3 완료: parameterized explicit bound

- contour를 `Re w=-beta+delta`, `0<delta<=1/4`로 옮기면 Gamma pole `w=0`의 residue는
  `L(rho,chi)=0` 때문에 사라지고 `w=-1`은 넘지 않는다.
- actual `f=mu*phi`, Barban--Vehov `lambda_d`에 대해
  `|M(delta+iv,chi,psi_r)| <= z2*r^2/phi(r)`와
  `sum_{r<=R}' r^-1 |M| < 3 R z2`를 명시화했다.
- primitive 유도 보정, Rademacher/Bennett bound와 Gamma 적분을 합성해
  `|I_delta| <= K_M(delta) A X^(-beta+delta)`를 얻었다. 여기서
  `A=(qT)^(1/2)Rz2`,
  `K_M(delta)=12 sqrt(6) zeta(1+delta)(2/delta+1)/pi^(3/2)`다.
- `delta=epsilon/[4(1+epsilon)]`와 Jutila (2.8)을 쓰면
  `|I_delta| <= K_M(delta) A^(-epsilon/2)`다.
- 판정: `JL6-MELLIN=ACTUAL_FORM_PARAMETERIZED_EXPLICIT`; 별도
  `JL6-TAIL=HARD_BLOCKER`, 따라서 `JL6`, `JL8`, `PAP-11`, DEP-R09,
  fixed `2e-17`, `X_cert`는 계속 OPEN이다.

### 2026-09-13 — 단계 4 완료: 문서·기계원장·시험·Lean

- Theory 62, review 69, machine ledger, 고정밀 evaluator와 fail-closed 회귀시험을
  작성했다. source theorem·contour 이동을 Lean axiom으로 넣지 않고, delta 범위와
  exponent transfer 등 dependency-critical 유한 실수대수만 단일 Lean 파일에 추가했다.
- 신규 표적시험 10/10, JL4--JL6 관련 시험 25/25, Python compile, JSON parse가 PASS했다.
- 전수 inventory는 theory 63개, display formula 1,104식이다. 상태는
  `KERNEL_PASS=36`, `CONDITIONAL_KERNEL_PASS=20`, `DEFINITION_ONLY=8`,
  `PARTIAL_FORMALIZATION=17`, `SOURCE_THEOREM_UNFORMALIZED=34`,
  `NOT_YET_FORMALIZED=984`, `PARSE_REVIEW_REQUIRED=5`이며 proof escape는 0건이다.
- 전체 unittest 708/708 PASS(64.135초), direct Lean compile 및 full `lake build`
  8,765 jobs PASS를 확인했다.
- 변경·신규 텍스트 21개 strict UTF-8/control issue 0, 변경 Markdown local link
  1,345개, Lean 정본 local link 1,170개, `git diff --check`가 PASS했다.
- 첫 control-character 검사 one-liner의 `"CONTROL:$rel:..."` 변수 구문은 parser가 실행
  전에 거부했다. `${rel}`로 교정해 재검사했고 오류 원장 E110에 기록했다.

### 2026-09-13 12:44 KST — 단계 5 완료: 정본·검증·handoff

- AGENTS, METHODS, theory·review 색인과 predecessor successor note, Lean README·원장,
  오류 원장을 현재 판정으로 동기화했다.
- `handoff/202609131242_HANDOFF.md`를 새로 작성해 쉬운 설명, 정확한 상태 경계,
  검증 증거, 다음 우선순위·예상시간, 사용자 수행절차와 한국어 commit 메시지를 고정했다.
- handoff를 포함한 변경·신규 텍스트 22개를 다시 검사해 strict UTF-8/control issue 0,
  변경 Markdown local link 1,345개와 `git diff --check` PASS를 확인했다.
- 다음 재개점은 `JL6b truncation tail source-first audit`이다. 실제 장시간 계산이나 새
  dependency는 현재 필요하지 않다.

## 현재 재개점

작업원장을 완료 이름으로 바꾸고 최종 diff·status를 확인한 뒤 이번 변경만 로컬 commit한다.

## 완료 전 점검

- [x] source-first 조사와 actual 조건 대조
- [x] Mellin 항과 truncation tail의 경계 분리
- [x] machine ledger·test·필요한 Lean 경계 완료
- [x] PAP-11·DEP-R09·fixed 계수·X_cert fail-closed
- [x] 정본·색인·AGENTS/METHODS 동기화
- [x] 전체 unittest·Lean·UTF-8·local links·diff 검증
- [x] 새 timestamp handoff 작성
- [x] 파일명을 `-done.md`로 변경
