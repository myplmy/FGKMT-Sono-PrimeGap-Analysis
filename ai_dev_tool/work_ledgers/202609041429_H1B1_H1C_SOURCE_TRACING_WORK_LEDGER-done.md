# Sono/FMT H1b-1·H1c source tracing 작업원장 (완료)

- 시작: 2026-09-04 14:29 KST
- 현재 상태: COMPLETED
- 사용자 승인: H1b-1 Maynard 기본 summation 상수 감사와 H1c FGKMT Hypothesis 1/PAP source tracing
- 금지·보류: 숨은 상수 추측, numerical `X_cert` 계산, threshold calculator, 새 prime sweep·actual experiment, 외부 dependency 설치, 기존 PDF/raw/result 변경, commit/push/PR
- 선행 변경: 시작 시 `git status --short` 출력 없음(clean). 직전 H1b 원장과 미검증 논문 review는 최신 handoff 기준 완료 상태다.

## 목적과 완료조건

- 목적:
  1. Maynard Lemmas 8.1–8.4 및 인용 summation 결과를 하위 proof edge로 분해하고, 실제 finite 상수 복원 가능성과 미확인 원문 의존성을 판정한다.
  2. FGKMT Hypothesis 1 검증과 PAP가 사용하는 exceptional character, zero-free/zero-density, Bombieri–Vinogradov, partial summation 또는 `psi -> pi` 경로를 source/page/equation 단위로 고정한다.
  3. `effective-in-principle`, printed explicit, quantitative reproof required, hard blocker를 분리하고 `X_cert`를 fail-closed 상태로 유지한다.
- 완료조건:
  - H1b-1과 H1c의 사람이 읽는 정본과 machine-readable ledger를 각각 작성한다.
  - 인용 원문과 locators를 가능한 범위에서 1차 출처로 확인하고 미확인 edge를 표시한다.
  - 새 ledger의 dependency·status·threshold 상태를 검사하는 단위시험을 작성한다.
  - T1/H1/H1b/METHODS/AGENTS/이론 색인과 최신 handoff를 동기화한다.
  - 고정 FGKMT Python 표적 및 전체 시험과 문서 참조 감사를 통과한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | FGKMT/Sono scale·end-bounded 정의 영향 없음 | summation/PAP proof dependency만 추적 |
| 데이터·provenance | maximal-gap dataset 영향 없음; 논문 source provenance만 추가 | 1차 출처·페이지·정리 번호를 기록 |
| 통계·정밀도 | actual 계산 없음 | 인쇄되지 않은 multiplier·cutoff를 숫자로 만들지 않음 |
| 승인 경계 | 문헌 감사·문서·검증 코드 승인 | prime sweep·threshold 실행·설치 금지 |
| 정리·경험 주장 | proof inventory는 theorem proof가 아님 | 각 node evidence level을 fail-closed로 저장 |
| 산출물·비덮어쓰기 | 신규 H1b-1/H1c 정본과 연결 정본만 변경 | 기존 actual artifact·PDF 불변 |

## 단계 현황

1. **COMPLETED — 로컬·온라인 1차 출처와 정확한 인용 경로 고정**
2. **COMPLETED — H1b-1 Lemmas 8.1–8.4 basic summation 상수 원장 작성**
3. **COMPLETED — H1c Hypothesis 1/PAP source trace와 blocker 원장 작성**
4. **COMPLETED — fail-closed 시험·정본 동기화·전체 검증**
5. **COMPLETED — 결과 설명·권장 순서·commit 제안·handoff·완료 처리**

## 단계별 기록

### 2026-09-04 14:29 KST — 착수·영향도 고정

- 수행: 최신 handoff, H1b 정본, 작업원장·영향도·계획·검증·handoff 스킬과 clean worktree를 확인했다.
- 파일: 이 작업원장 신규 작성.
- 결과: H1b-1/H1c는 논리적으로 병렬 조사 가능하지만, 둘 모두 숫자 상수 없이 H1b-2나 threshold calculator로 승격할 수 없다.
- 문제·결정: H1b-1은 Maynard 내부 lemma와 인용 GGPY edge를 분리한다. H1c는 Hypothesis 1의 세 조건과 PAP lower bound를 같은 것으로 합치지 않고 공통 analytic input만 연결한다.
- 다음 재개점: Maynard, FGKMT, Sono/FMT 원문의 정확한 정리·식·참고문헌을 추출하고 하위 원문 링크를 고정한다.

### 2026-09-04 — source 고정과 H1b-1 원장 완료

- 수행: Maynard 출판본 Lemmas 8.1–8.4, GGPY Lemmas 3–4, FGKMT Hypothesis 1·Lemmas 7.1–7.2,
  Sono Assumption PAP·Section 5와 하위 source metadata를 대조했다.
- 교정: Maynard Lemma 8.3의 source는 *Small Gaps Between Products of Two Primes*이며
  \(\kappa=1\) 특수화다. parent `H1B-L83`은 source 미확인에서 numerical rate 누락으로만
  정정했다. Jutila source 연도는 1970이 아니라 1977이다.
- 신규 파일:
  - `docs/method/theory/15_Sono_FMT_H1b1_basic_summation_constant_audit.md`
  - `docs/method/theory/data/Sono_FMT_H1b1_basic_summation_constants_v1.json`
  - `tests/test_h1b1_basic_summation_ledger.py`
- 판정: `SOURCE_CHAIN_TRACED_NUMERICAL_SUMMATION_CONSTANTS_OPEN`; `SIV-07`과 `X_cert`는 OPEN.

### 2026-09-04 — H1c 원장과 proof-DAG 정정 완료

- 수행: Hypothesis 1의 3개 clause와 PAP를 20개 node로 분리하고, 로컬 Sono·FGKMT PDF hash를
  원장에 고정했다.
- 수학적 진전: \(\mathcal A=\mathbb Z\)에서 Hypothesis 1(1)은
  `floor(y^(1/3))*(log y)^(100 k^2) <= N`, (3)은 `N>=q`일 때 상수 2라는 exact sufficient
  reduction을 얻었다. condition (2)는 계속 hard blocker다.
- 논리 교정: PAP pointwise lower bound와 Hypothesis 1(2) average discrepancy는 sibling이므로
  T1 `SIV-08.depends_on=[PAP-11]`을 제거했다. 두 row의 hard-blocker 상태는 그대로다.
- 신규 파일:
  - `docs/method/theory/16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md`
  - `docs/method/theory/data/Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json`
  - `tests/test_h1c_hypothesis1_pap_trace.py`
- 판정: `SIBLING_SOURCE_CHAINS_TRACED_NUMERICAL_PACKAGES_OPEN`; `SIV-08`, `PAP-11`, `X_cert` OPEN.

### 2026-09-04 — 표적 fail-closed 검증

- 명령: 고정 FGKMT Python으로 신규·연결 시험 5개 모듈을 `py_compile`하고 `unittest -v` 실행.
- 결과: 29/29 PASS, 0 failure/error.
- 다음 재개점: METHODS·AGENTS·이론 색인·H1 review를 동기화하고 전체 unittest·링크·diff 검증한다.

### 2026-09-04 — 정본 동기화와 전체 검증 완료

- 동기화: `AGENTS.md`, `docs/METHODS.md`, theory index, T1/H1/H1b machine ledgers,
  T1/H1/H1b 사람이 읽는 정본과 threshold review를 H1b-1/H1c 결과에 맞췄다.
- 전체 시험 1차: sandbox 안에서 235건 중 임시폴더 ACL 때문에 82 error가 났고, 기존 완료
  작업원장의 금지 오타 문자열 1건이 vocabulary test에서 검출됐다. 새 이론 시험 실패는 없었다.
- 교정: 과거 완료 원장의 뜻은 바꾸지 않고 “금지 용어 자체를 그대로 적은 검사 결과”를
  `금지된 4글자 프로젝트명 오타`로 표현해 self-trigger를 제거했다.
- 전체 시험 2차: 기존 사용자 허용 범위에 따라 sandbox 외부의 동일 고정 FGKMT Python 명령으로
  235/235 PASS, 34.097초.
- 추가 감사: 신규·연결 문서 상대 링크 누락 0, control character 0, vocabulary test PASS,
  `git diff --check` whitespace error 0(CRLF 안내만 존재), JSON parse PASS.
- 실제 실험: 없음. dataset·result artifact·threshold calculator·prime sweep 생성 없음.
- 다음 재개점: 새 timestamp handoff를 작성하고 작업원장을 `-done`으로 닫는다.

### 2026-09-04 14:58 KST — handoff와 완료 처리

- 신규 handoff: `handoff/202609041458_HANDOFF.md`.
- 포함: H1b-1/H1c 쉬운 설명, source·DAG 교정, 실제 미수행 범위, 검증 증거, 다음 작업별
  환경·정확한 사용자 절차, 예상시간, 한국어 commit 제목·본문.
- 사용자 실행: 없음. 모든 권장 단계는 현재 `별도 수행절차 필요없음`이며 새 수학 작업은 별도
  승인 뒤 착수한다.
- 최종 상태: 요청 산출물·정본 동기화·검증·handoff 완료. 원장을 `-done`으로 변경한다.

## 현재 재개점

완료. 다음 세션은 최신 handoff의 승인 경계에서 재개한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] proof inventory와 numerical theorem 상태 분리
- [x] 문헌 provenance·locator 확인
- [x] METHODS/AGENTS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
