# H1b-2a.2 Proposition 9.4 distribution error 작업원장

- 시작: 2026-09-08 19:41 KST
- 현재 상태: COMPLETE
- 사용자 승인: H1b-2a.2부터 기존 권장 순서에 따른 문헌·수학 감사, 유한 reduction,
  보조 코드·toy 검증, 정본 동기화
- 금지·보류: 실제 prime/maximal-gap sweep, P018-B actual, numerical threshold calculator,
  패키지 설치, commit/push/PR, 열린 상수를 임의로 1로 두는 행위
- 선행 변경: 시작 시 `git status --short` 출력 없음. 작업트리는 clean이며 H1b-2a.1
  완료 상태를 기준선으로 사용한다.

## 목적과 완료조건

- 목적: Maynard Proposition 9.4 식 (9.52)의 `E_q^(1)` contribution을 Proposition 9.1의
  생략된 동일 논증까지 역추적해, exact tuple multiplicity와 이미 닫힌 Lemma 8.5
  coefficient/weight 상계로 유한식화한다.
- 완료조건: 분포 오차가 어떤 Hypothesis 1 조항·multiplier·cutoff를 요구하는지 exact하게
  분리하고, 닫을 수 있는 부분과 H1c-1 입력 blocker를 구분한다. 기계 계약·회귀시험,
  H1b/H1/T1/METHODS/AGENTS 동기화, 새 handoff까지 완료한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 높음 | 원문 Proposition 9.1·9.4와 Hypothesis 1을 식·변수 단위로 대조한다. |
| 데이터·provenance | 영향 없음 | actual dataset과 `test_result/`를 읽거나 생성하지 않는다. |
| 통계·정밀도 | 낮음 | exact integer/rational algebra와 보수적 양의 상계만 사용한다. |
| 승인 경계 | 높음 | 이론·toy 검증까지만 수행하고 threshold 계산은 만들지 않는다. |
| 산출물·비덮어쓰기 | 높음 | 신규 theory/review/contract를 만들고 기존 정본은 상태 근거만 패치한다. |

## 단계 현황

1. **COMPLETE — 원문 분포오차 호출부와 Hypothesis 1 의존성 역추적**
2. **COMPLETE — 선행 explicit distribution 정리·교정 조사**
3. **COMPLETE — exact tuple-count 및 finite error reduction 정식화**
4. **COMPLETE — 기계 계약·코드·toy 시험과 parent fail-closed 검증**
5. **COMPLETE — 정본 동기화·전체 검증·handoff·완료 이름 변경**

## 단계별 기록

### 2026-09-08 19:41 KST — 착수·영향 분석

- 수행: 최신 handoff, 작업원장 규약, 적용 스킬과 clean worktree를 확인했다.
- 파일: 이 작업원장 신규 작성.
- 명령·검증: 최신 handoff 조회, 비완료 원장 0건, `git status --short` 출력 없음.
- 결과: H1b-2a.1의 Euler normalization은 닫혔고 식 (9.52)만 P94의 직접 distribution
  child로 남은 기준선을 확인했다.
- 문제·결정: 상위 Proposition과 `SIV-07/09`, `X_cert`는 하위 reduction만으로 승격하지 않는다.
- 다음 재개점: Maynard author TeX에서 Proposition 9.1의 `E_q^(1)` 처리와 Proposition
  9.4 lines 1070--1074를 나란히 추출해 실제 modulus·multiplicity·합 범위를 고정한다.

### 2026-09-08 20:18 KST — 단계 1 완료: 실제 호출과 일반 명제 분리

- 수행: Maynard Proposition 9.1 source lines 671--694, Proposition 9.4 source lines
  1044--1074, Hypothesis 1 source lines 67--76, FGKMT Lemma 7.2와 Theorem 6 적용부를
  식·변수 단위로 대조했다.
- 증거: Proposition 9.1의 일반 논증은 `tau_(3k)` multiplicity, Hypothesis 1(1)의 평균
  discrepancy와 (3)의 pointwise bound를 Cauchy--Schwarz로 합성한다. Proposition 9.4는
  이를 `(k+1)`차원에서 반복한다고만 쓴다.
- 핵심 정정: FGKMT/FMT 실제 적용은 `A=Z`, `theta=1/3`, `xi=theta/10`, `D=1`이다.
  연속 정수 interval에서는 모든 `q,a`에 `E_q^(1)<=1`이 exact하므로, **이 P94 오류항만은**
  Hypothesis 1의 숨은 multiplier 없이 직접 상계할 수 있다. 이는 prime moment P92에 필요한
  Hypothesis 1(2)나 H1c 전체를 닫지 않는다.
- 변경 파일: 작업원장만 갱신.
- 검증: 최종 출판본 layout text의 (9.52), author TeX SHA-256
  `e55592f0d674e32ad6ef7d6fe25bce2a0aa3cfc712981ccf996a5df0a4d5b18e`, FGKMT
  PDF SHA-256 `c31229ef40c9646dfc99bde7c059a9a0fd35e7be71b5836de9df06c01d921ac8`를 대조했다.
- 다음 재개점: `3(k+1)` exact assignment count, squarefree divisor-sum majorant,
  `tilde_lambda`/`lambda` finite envelope와 canonical P94 scale의 흡수비를 정식화한다.

### 2026-09-08 20:31 KST — 단계 2 완료: 선행 증명 우선 조사

- 수행: Maynard arXiv:1405.2593·출판본, FGKMT arXiv:1412.5029, Polymath8b
  arXiv:1407.4897을 표적 검색하고 저장된 최종본/author TeX와 대조했다.
- 결과: 원문의 일반 `E_q^(1)` 논증은 확인했지만, 실제 `A=Z` 호출에 대해 모든 multiplier와
  finite cutoff를 인쇄한 drop-in package는 이번 표적 1차 문헌 조사에서 확인하지 못했다.
  이는 전 세계 비존재나 novelty 주장이 아니다.
- 결정: 기존 정리를 억지로 수치화하지 않고, 연속 정수의 exact discrepancy와 원문 support를
  사용한 최소 project lemma를 직접 증명한다.
- 다음 재개점: 단계 3의 유한 흡수식을 문서·기계 계약으로 고정한다.

### 2026-09-08 20:31 KST — source-version 교정 발견

- 발견: Maynard author TeX line 1090은 `r_0|d_0`로 적혀 있지만, 이는 line 1098의
  `tilde_lambda_1` 전 범위 합과 모순된다. 최종 출판본 식 (9.56)은 올바른 `d_0|r_0`다.
- 조치: 최종 출판본을 정본으로 채택하고 theory 30·contract·review에 차이를 명시했다.
- 영향: finite coefficient 상계는 올바른 `d_0|r_0`에 기초한다. 오류를 숨기거나 author
  source 표기를 그대로 재사용하지 않는다.

### 2026-09-08 20:31 KST — 단계 3 완료: actual-application finite reduction

- 증명: `A=Z`의 exact `E_q^(1)<=1`, multiplier 1의 `tau_(3(k+1))(q)`,
  `sum_(q<Q) tau_a(q)<=Q(1+log Q)^a`, finite lambda/tilde-lambda envelope를 합쳤다.
- 결과: 전체 residue class의 식 (9.52) 오류를 canonical P94 scale의 `rho_94` 배 이하로
  만들고, `rho_94<=1`을 보장하는 closed-form `Y_94`를 얻었다.
- 범위: 실제 `D=1`, `xi=theta/10`, `theta<15/16`; FGKMT/FMT의 `theta=1/3` 포함.
- 파일: theory 30, review 36, JSON contract, source module, 7개 회귀시험 신규 작성.
- 진단: `k=36, alpha=2, theta=1/3`에서 `log x` 충분조건은 약 `3.5227e133`이며
  새 distribution gate가 아니라 기존 smooth gate가 지배한다. 이는 `X_cert`가 아니다.
- 검증: `py_compile` PASS, targeted unittest 7/7 PASS.
- parent 통제: distribution child만 `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`; P94 parent,
  SIV-07/09, `X_cert`는 열림으로 고정했다.
- 다음 재개점: 기존 H1b/H1/T1/METHODS/AGENTS 문서·JSON의 오래된 “P94가 Hypothesis
  1(1),(3) multiplier를 기다린다” 문구를 actual/general 범위가 구분되도록 동기화한다.

### 2026-09-08 20:31 KST — 단계 4 완료: 기계 계약·상위 원장 회귀검증

- 수행: 새 기계 계약과 predecessor successor-link, H1b/H1/T1 master JSON을
  actual/general 범위가 분리되도록 동기화했다. H1b master schema는 1.7.0,
  H1/T1 schema는 1.4.0으로 올렸다.
- 상태 통제: `H1B2A-P94-DISTRIBUTION`만
  `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`이다. `H1B-P94=RATE_MISSING`,
  `SIV-07=HARD_BLOCKER`, `X_cert=OPEN`은 그대로다.
- 문서: AGENTS, METHODS, theory index, T1/H1b/H1 predecessor 문서와 review 24/34/35에
  후속 상태를 반영했다. 과거 시점 표는 삭제하지 않고 successor update로 보존했다.
- 교정: 새 theory/review의 “질수” 오탈자를 “소수”로, 누락된 `\\le`를 바로잡았다.
- 검증: 고정 FGKMT Python에서 `py_compile` PASS. 새 7개와 영향받은 상위 원장 시험을
  합쳐 40/40 PASS했다.
- 다음 재개점: 전체 unittest, JSON/Markdown 참조 및 diff 감사 후 handoff를 새로 쓰고
  원장을 완료 이름으로 바꾼다.

### 2026-09-08 20:34 KST — 단계 5 완료: 전체 검증·handoff

- 전체 검증: 첫 sandbox 실행은 임시폴더 권한 때문에 82개 공통 `PermissionError`로
  실패했다. 이 출력은 코드 판정에서 제외했다. 동일 FGKMT 명령을 기존 허가 범위의
  sandbox 밖에서 재실행해 `Ran 328 tests in 35.150s / OK`를 확인했다.
- 추가 검증: 새 의존성 negative assertion 뒤 표적 14/14 PASS, 신규 Markdown 상대 링크
  PASS, 갱신 JSON strict parse PASS, `git diff --check` PASS.
- 절차 오류: 이미 알려진 sandbox 우선순위와 Windows `rg` wildcard 오류가 재발해
  `ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md`의 E032에 기록했다. 연구 결과 영향은 없다.
- handoff: `handoff/202609082034_HANDOFF.md`를 새로 작성했다.
- 최종 판정: 요청한 H1b-2a.2 child를 닫았고, parent·root non-promotion 및 비실행 경계를
  보존했다. 다음 재개점은 H1b-2a.3 P94 end-to-end 합성이다.

## 현재 재개점

완료. 다음 작업은 최신 handoff에서 H1b-2a.3 첫 단계부터 시작한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] METHODS/이론 정본 동기화; actual 실행이 아닌 이론·toy 작업이라 `test_result` 색인과 실험계획 갱신은 해당 없음
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
