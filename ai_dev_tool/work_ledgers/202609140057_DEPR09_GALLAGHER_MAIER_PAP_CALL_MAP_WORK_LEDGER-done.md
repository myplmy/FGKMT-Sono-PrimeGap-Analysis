# DEP-R09 Gallagher--Maier PAP source-call map 작업원장

- 시작: 2026-09-14 00:57 KST
- 상태: IN PROGRESS
- 선행 정본: Theory 57·71, review 64·78, handoff 202609140050
- 목표:
  Jutila의 actual primitive nonprincipal near-one averaged density를
  Gallagher--Maier의 pointwise prime-in-AP lower bound에 넣는 정확한 source-call
  경로를 페이지·식·변수·상수 단위로 복원한다.
- 완료조건:
  1. Gallagher 1970, Maier 1981, McCurley 1984 PDF의 text/OCR 필요성을 분류하고
     핵심 페이지를 렌더 원문과 대조한다.
  2. density theorem, explicit formula, exceptional character, prime powers,
     dyadic/endpoint 및 psi-to-pi 호출의 방향과 범위를 전사한다.
  3. Theory 71의 near-one 범위만으로 충분한지, away-from-one 또는 principal branch가
     별도로 필요한지 fail-closed로 판정한다.
  4. source에 없는 multiplier·cutoff를 추정으로 채우지 않고 새 proof obligation을
     machine-readable하게 기록한다.
  5. 닫히는 유한 대수는 Python과 필요 시 단일 Lean 파일에서 검증한다.
  6. Theory·review·METHODS·T1·색인·Lean 원장·오류 원장·handoff를 동기화하고
     전체 회귀 뒤 명시적 로컬 commit을 만든다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | averaged density와 pointwise PAP를 같은 명제로 취급하지 않는다. |
| dataset | 영향 없음 | maximal-gap 데이터나 실제 소수 범위를 읽거나 계산하지 않는다. |
| provenance | 영향 있음 | 사용자 제공 3개 PDF와 Jutila source의 hash·printed page를 고정한다. |
| 정밀도 | 확인 필요 | source의 big-O 또는 sufficiently-large를 숫자 1로 바꾸지 않는다. |
| 승인 | 영향 없음 | 장시간 계산·threshold calculator·actual prime sweep은 계속 금지한다. |
| Lean | 확인 필요 | source theorem 전체가 아니라 새 결론에 실제 필요한 유한 대수만 형식화한다. |
| 정본 | 영향 있음 | 새 Theory 72/review 79와 dependency machine ledger를 successor로 만든다. |

## 단계 현황

1. **DONE — source modality·페이지·식 inventory**
2. **DONE — exact proof-call DAG와 변수 정규화**
3. **DONE — near-one sufficiency 및 잔여 blocker 판정**
4. **DONE — exact checker·Lean 형식화**
5. **DONE — 정본 동기화·전체 검증·handoff·완료 이관·commit 준비**

## 단계별 기록

### 2026-09-14 00:57 KST — 착수

- 직전 작업은 commit <code>0b0dc9d</code>에서 Theory 71의 좁은
  <code>JL7-AVERAGED-NP-NEAR-ONE</code>을 닫았다.
- 현재 worktree는 clean이다.
- 사용자 제공 Gallagher 1970, Maier 1981, McCurley 1984 PDF가 모두 존재한다.
- 이번 작업은 proof source tracing이며 actual 실험·소수 sweep·threshold 계산을 하지 않는다.
- 다음 재개점: 각 PDF의 metadata·native text 양을 확인하고 Theory 57/review 64가
  이미 전사한 page/equation locator를 원문과 대조한다.

### 2026-09-14 01:26 KST — source와 near/far 수식 고정

- Gallagher·Maier·McCurley 세 PDF는 각각 native text
  24,750·30,516·51,518 bytes로 OCR이 필요하지 않았다. Gallagher printed
  pp.335--338, Maier pp.260--261, McCurley pp.8--9를 렌더 원문과 대조했다.
- Bennett--Martin--O'Bryant--Rechnitzer 2021의 peer-reviewed publication과
  DOI <code>10.1090/mcom/3599</code>를 AMS에서 확인하고 arXiv v1 audit copy를
  <code>article/</code>에 hash 고정했다. 이 파일도 native text 115,483 bytes이며
  Theorem 1.1 페이지를 렌더 대조했다.
- Gallagher 식 (30)의 Stieltjes 적분을
  <code>[0,1-theta]</code>와 <code>[1-theta,1-eta]</code>로 나누었다.
  far branch는 endpoint까지 합쳐 정확히 <code>Z*X^(-theta)</code>가 된다.
- <code>Q=X^(1/d)</code>, <code>T=Q^5</code>,
  <code>D=Q^7</code>에서 Bennett Theorem 1.1과 primitive-character 수
  <code>&lt;=Q^2</code>를 합쳐
  <code>Z_np&lt;=2Q^2T log(QT)</code>인 보수적 전역 영점수 상계를 얻었다.
- Theory 71의 near-one envelope는
  <code>delta=1/log D</code>에서 정확히 두 구간으로 나누어 적분했다.
  endpoint <code>theta=1/21,d=160</code>에서는
  <code>kappa=22</code>, <code>lambda=69/80</code>,
  far exponent <code>13/3360</code>이다.
- 새 Python exact/high-precision checker와 11개 표적시험은 최종 PASS했다.
  첫 표적시험에서는 허용되지 않는 toy theta와 저장 60자리 대 90-dps
  <code>almosteq</code> 기준 때문에 1 error·1 failure가 발생했고, 수식 변경 없이
  유효 theta와 명시적 상대오차 <code>1e-55</code>로 교정했다.
- 현재 certificate의 near asymptotic envelope는 d=160에서 약
  <code>2.7277e13</code>이다. 이는 실제 오차의 하한이 아니라 현 상계의
  불충분성을 뜻한다. asymptotic envelope가 1 이하가 되는 첫 정수 d는 3856,
  <code>exp(-2)</code> 이하가 되는 첫 정수 d는 4096이지만, 두 값은 선행
  fixed-coefficient capacity <code>d&lt;=186</code>을 크게 넘으므로 채택 가능한
  PAP parameter가 아니다.
- 다음 재개점: Theory 72/review 79를 작성하고 닫힌 near/far 유한식과 여전히 열린
  explicit-formula·principal·exceptional·orthogonality·psi-to-pi node를 분리한다.

### 2026-09-14 01:35 KST — Theory 72·review 79·Lean batch 완성

- Theory 72와 review 79에 source call DAG, exact near/far 식, 수치 gate와
  잔여 OPEN node를 분리했다. Bennett arXiv audit copy는 peer-reviewed AMS
  publication의 Theorem 1.1 진술을 대조하는 source로 hash 고정했다.
- Bennett helper의 작은 ell zero-free branch를 source theorem대로 0으로 반환하도록
  보강하고 경계 회귀시험을 추가했다. 실제 T=Q^5 진단값은 변하지 않는다.
- 표적 unittest 11/11 PASS, py_compile PASS, JSON parse PASS.
- Lean 단일 파일에 endpoint 유리수 대수, family count 조건부 합성,
  far endpoint 소거, near piecewise 원시함수 소거를 추가했다. 첫 compile의
  Real type 주석 누락을 교정한 뒤 direct kernel compile exit 0이다.
- theory 72 추가 뒤 inventory는 73개 문서·1,311식, Lean declaration 245개다.
  상태는 KERNEL_PASS 77, CONDITIONAL_KERNEL_PASS 49,
  DEFINITION_ONLY 58, PARTIAL_FORMALIZATION 58,
  SOURCE_THEOREM_UNFORMALIZED 62, NOT_YET_FORMALIZED 1002,
  PARSE_REVIEW_REQUIRED 5이고 금지 proof escape는 0이다.
- 정본 METHODS, theory/review 종합 색인, T1 원장, Lean README, AGENTS와
  오류 원장을 successor 판정으로 동기화했다.
- 다음 재개점: generator 재실행 뒤 validator·전체 unittest·Lean build와
  UTF-8/JSON/link/diff 검사를 수행하고 새 handoff를 작성한다.

### 2026-09-14 01:39 KST — 전체 회귀·정적검사·handoff 완료

- 전체 unittest의 첫 sandbox 실행은 TemporaryDirectory 권한 때문에 805건 중
  82건이 PermissionError로 끝났고 결과로 채택하지 않았다. 사용자가 허가한 정상
  로컬 권한에서 동일 명령을 재실행해 805/805 PASS, 74.799초를 확인했다.
- direct Lean compile exit 0, full Lake build 8,765 jobs PASS.
- Lean generator/validator PASS: 73 theory·1,311 display식·245 declarations,
  금지 proof escape 0건.
- 변경·신규 text 19개 strict UTF-8/control issue 0, Markdown 12개 local link
  1,643건 issue 0, JSON strict parse, 새 문서 수식 delimiter와 과거 transport
  손상형 표적 scan PASS.
- 새 handoff <code>handoff/202609140139_HANDOFF.md</code>에 쉬운 설명,
  source/수식/수치 판정, 열린 root, 다음 우선순위·예상시간, 사용자 절차와
  한국어 commit 문구를 기록했다.
- 이번 단계에서 actual maximal-gap 계산·prime sweep·장시간 CPU 실험은
  실행하지 않았다. sandbox 실패가 남겼을 수 있는 tmp 경로도 임의 삭제하지 않았다.
- cached diff의 수식 감사에서 Theory 72 식 (72.2), (72.3)의 줄바꿈 앞 덧셈기호
  누락을 발견했다. Gallagher printed p.338 원문으로 재확인해 두 기호를 복구했고,
  코드·Lean·수치에는 영향이 없음을 확인했다. 교정 뒤 전체 unittest 805/805
  PASS, 74.556초를 재확인했다. 오류 원장 E120에 기록했다.
- 이 원장은 <code>-done</code>으로 이관됐다. 다음 재개점은 명시적 allowlist
  staging을 갱신하고 cached diff·JSON·validator를 재검사한 뒤 로컬 commit하는 것이다.

## 완료 전 점검

- [x] source PDF modality와 hash 고정
- [x] proof-call DAG와 OPEN node 기록
- [x] 과장 없는 쉬운 설명
- [x] 필요 finite algebra Python/Lean 검증
- [x] 정본 문서와 원장 동기화
- [x] 전체 unittest·Lean·정적 검사
- [x] 새 timestamp handoff
- [x] 파일명 <code>-done.md</code> 이관 준비
- [x] 명시적 staging·cached diff·로컬 commit 준비
