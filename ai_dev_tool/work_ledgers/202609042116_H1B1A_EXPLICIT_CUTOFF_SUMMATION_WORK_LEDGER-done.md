# Sono/FMT H1b-1a explicit cutoff·초등 summation package 작업원장

- 시작: 2026-09-04 21:16 KST
- 현재 상태: COMPLETE
- 사용자 승인: H1b-1a의 명시적 cutoff와 초등 summation package를 문헌 근거와 함께 정식화하고, 데이터 비의존 검증 코드를 작성·실행한다. 필요한 학술자료는 직접 취득할 수 있다.
- 금지·보류: `X_cert` 계산기, 장시간 prime sweep, maximal-gap actual 실험, H1c-1 착수, package 설치, commit/push/PR은 수행하지 않는다.
- 선행 변경: 시작 시 `git status --short` 출력 0건. 미완료 작업원장 0건.

## 목적과 완료조건

- 목적: Maynard Proposition 6.1의 basic summation 단계에서 숨겨진 smooth-cutoff·초등 소수곱/합 상수를 명시적 유한 명제로 분리하고, 실제로 닫힌 항목과 여전히 열린 rate/cutoff를 구별한다.
- 완료조건:
  - H1b-1a 정본 문서와 기계 판독 가능한 obligation 자료를 작성한다.
  - 인용한 1차 문헌의 URL·페이지/정리·취득일·SHA-256을 기록한다.
  - cutoff 함수의 support/plateau/smoothness 및 채택한 유한 부등식을 exact 또는 방향 보존 방식으로 검증한다.
  - H1b-1/T1/AGENTS의 상태를 과장 없이 동기화하고 새 handoff를 작성한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 새 project finite lemma를 추가하지만 FGKMT scale·end-bounded `G(x)`는 변경하지 않음 | 문헌 정리와 프로젝트 보조정리를 별도 표기 |
| 데이터·provenance | maximal-gap 데이터는 사용하지 않고 학술 PDF/공식 웹 원문만 사용 | URL·취득시각·SHA-256·정리 위치 기록 |
| 통계·정밀도 | 통계 실험 없음; 증명용 수치는 binary float를 근거로 사용하지 않음 | 유리수, exact integer, 또는 바깥쪽 반올림 interval만 허용 |
| 승인 경계 | 문헌 취득·정식화·toy/unit 검증만 승인됨 | actual threshold/prime sweep 실행 금지 |
| 산출물·비덮어쓰기 | 새 이론 문서·data contract·test·handoff 생성 | 기존 actual artifact와 PDF 원본 불변 |

## 단계 현황

1. **COMPLETED — H1b-1/H1c 재개점과 Maynard basic summation의 정확한 target 식 확인**
2. **COMPLETED — 1차 문헌 취득·provenance 고정 및 explicit cutoff 정식화**
3. **COMPLETED — 초등 summation·소수곱/토션트 유한 package 정식화와 상태 판정**
4. **COMPLETED — machine contract·unit test 구현 및 정합성 검증**
5. **COMPLETED — 정본 동기화·최종 보고·새 handoff·원장 완료 처리**

## 단계별 기록

### 2026-09-04 21:16 KST — 착수와 승인 경계 고정

- 수행: 최신 handoff, H1b-1/H1c 상태, 적용 스킬과 작업원장 규약을 확인했다.
- 파일: 이 원장.
- 명령·검증: `git status --short`; 비 `-done` 원장 조회.
- 결과: 선행 변경과 열린 원장 모두 0건.
- 문제·결정: H1b-1a가 닫혀도 Maynard Proposition 6.1 전체나 `X_cert`가 닫힌 것으로 간주하지 않는다.
- 다음 재개점: `docs/method/theory/14_...`, `15_...`와 관련 source trace JSON에서 Lemmas 8.1–8.4의 target 식을 추출하고 1차 PDF 원문과 대조한다.

### 2026-09-04 21:35 KST — target 식과 1차 출처 고정

- 수행: Maynard 출판본 (7.10), Lemmas 8.1–8.4 및 Dusart의 명시적 Chebyshev/Mertens bound를 원문 PDF로 대조했다. Rosser–Schoenfeld Theorem 15의 totient bound도 원문과 대조했다.
- 파일: `tmp/pdfs/h1b1a/Maynard2016_Dense_Clusters_published.pdf`, `tmp/pdfs/h1b1a/Dusart2010_Explicit_estimates_over_primes.pdf`, `tmp/pdfs/h1b1a/Rosser_Schoenfeld_1962_Approximate_formulas.pdf`.
- 명령·검증: 공식/출판기관 URL에서 `Invoke-WebRequest`; `pdfinfo`; `pdftotext` 관련 페이지 추출; SHA-256 계산.
- 결과: Maynard 39쪽/`8EB9D780...68098`, Dusart 20쪽/`3F11ECA8...F3923`, Rosser–Schoenfeld 31쪽/`8E37B06F...AB556`. sandbox 안의 직접 다운로드는 연결 거부되어, 사용자 승인 범위에 따라 sandbox 밖에서 같은 명령을 재실행해 성공했다.
- 문제·결정: Lemma 8.1(i)는 `theta(2k)`와 tail을 직접 수치화할 수 있다. Lemma 8.1(ii)는 초등 majorant를 만들 수 있지만, Maynard의 입력 `|a| << 1`, `|b_i| << log x`에 숨은 상수와 공통 흡수 cutoff는 별도로 남는다.
- 다음 재개점: explicit C-infinity cutoff의 식과 첫 도함수 bound, Lemma 8.1(i)의 합성 상수, (8.5)의 Euler-product 상계를 정식 문서·코드 계약으로 작성한다.

### 2026-09-04 21:45 KST 기록 — finite lemma 정식화와 machine contract 작성

- 수행: 표준 flat bump로 cutoff를 고정해 `sup|psi'|<50`을 기호적으로 증명했다. Dusart의 `theta(x)<2x`와 직접 Taylor/telescoping bound를 합쳐 Lemma 8.1(i)를 `S_B(L)>exp(-9k/2)`로 닫았다. 식 (8.5)의 Euler product를 `24 log k`로 상계하고 Lemma 8.1(ii)의 parameterized finite majorant를 유도했다.
- 파일: `docs/method/theory/17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md`, `docs/method/theory/data/Sono_FMT_H1b1a_explicit_cutoff_summation_v1.json`, `source/h1b1a_explicit_package.py`, H1b/H1b-1 parent 문서·JSON, 관련 tests.
- 명령·검증: FGKMT Python으로 exact `Fraction` finite branch를 2..2973까지 계산. 2,972개 모두 PASS, 최대 surrogate ratio witness `k=2971`, 표시값 약 `7.148780502325333 < 8`, row digest `6dfb28c...259e5`.
- 결과: `H1B1-L81-SMALL`, `H1B1-L81-TAIL`, `H1B1-L82-CUTOFF` 세 subrow만 `PROJECT_FINITE_COMPONENT_CLOSED`; `H1B1-L81II-DIVISOR`는 `PARTIAL_EXPLICIT`; parent와 `X_cert`는 OPEN 유지.
- 문제·결정: 최초 문서 패치에서 JavaScript 문자열의 LaTeX backslash가 escape 처리되어 `\vartheta`가 control character로 손상됐다. 손상 파일을 즉시 삭제하고 `String.raw` 패치로 전면 재작성했다. 이후 문서 control-character 검사와 `git diff --check`를 필수 검증에 포함한다.
- 다음 재개점: targeted tests, JSON parse, control-character/LaTeX 정적 감사, 전체 unittest를 실행하고 실패를 수정한다.

### 2026-09-04 21:45 KST 기록 — targeted 검증과 정본 동기화

- 수행: exact finite certificate, cutoff 회귀검사, parent fail-closed 검사를 FGKMT Python으로
  실행했다. 새 상태를 `docs/METHODS.md`, H1b/H1b-1 parent 원장과 `AGENTS.md`에
  동기화하고, 도구 wrapper 실수를 오류 원장 E019에 기록했다.
- 파일: `docs/METHODS.md`, `AGENTS.md`,
  `ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md`,
  H1b-1a 문서·JSON·source·tests 및 두 parent 문서·JSON.
- 명령·검증:
  - `W:\miniforge3\envs\FGKMT\python.exe -m py_compile ...` PASS
  - targeted unittest 16/16 PASS
  - 관련 JSON 3개 parse PASS
  - 텍스트 7개 ASCII 제어문자 0건
  - source PDF 3개 SHA-256 재계산 일치
- 문제·결정: cutoff derivative 수치 회귀시험의 첫 실행은 `mp.almosteq` 기본 허용오차가
  \(u=0.9\)의 극소값에 지나치게 엄격해 1건 실패했다. analytic formula나 증명 실패가 아니라
  시험 허용오차 계약의 문제였으며, 80-dps 계산에 명시적 상대·절대오차 `1e-70`을 지정한 뒤
  16/16 PASS했다. 이 grid/수치미분 검사는 기호적 sup-bound 증명을 대신하지 않는다.
- 다음 재개점: 전체 unittest, `git diff --check`, 링크·상태 참조 감사를 수행한 뒤 새 handoff와
  최종 보고를 작성한다.

### 2026-09-04 21:48 KST — 전체 회귀·정적 감사와 인계 완료

- 수행: 고정 FGKMT Python으로 전체 suite를 실행하고, JSON·문서 경로·제어문자·stale
  next-gate·whitespace를 최종 감사했다. 새 timestamp handoff에 결과, 승인 경계, 다음 순서,
  사용자 절차와 commit 제안을 기록했다.
- 파일: `handoff/202609042146_HANDOFF.md`, 이론 색인, `docs/METHODS.md`, `AGENTS.md`,
  오류 원장과 이 작업원장.
- 명령·검증:
  - 전체 unittest 240/240 PASS, 39.141초
  - `git diff --check` PASS; CRLF 변환 안내만 있고 whitespace error 0
  - JSON 3개 parse PASS, 관련 텍스트 11개 제어문자 0
  - 필수 경로 5개 존재, 완료된 H1b-1a를 “다음 gate”로 남긴 stale 참조 0
- 결과: 사용자 요청 범위 완료. actual 실험·threshold 계산·package 설치·commit은 수행하지
  않았다. 이론 작업이라 `test_result` 색인은 갱신 대상이 아니며 figure·시각 QA도 없다.
- 다음 재개점: 사용자 승인 후 H1b-1b의 `H1B1-L82-LIPSCHITZ`,
  `H1B1-L83-GGPY3`, `H1B1-L83-GGPY4`부터 새 작업원장으로 시작한다.

## 현재 재개점

사용자 승인 전에는 추가 작업하지 않는다. 다음 재개점은 H1b-1b다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
