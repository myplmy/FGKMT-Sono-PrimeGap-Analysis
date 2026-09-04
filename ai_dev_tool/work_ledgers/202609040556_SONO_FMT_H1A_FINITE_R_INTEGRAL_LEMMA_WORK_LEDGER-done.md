# Sono/FMT H1a finite-r integral lemma 작업원장

- 시작: 2026-09-04 05:56 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: Maynard (8.25)–(8.27)의 finite-r 적분 lemma 정식화, 필요한 문서·fail-closed 검증 구현과 로컬 검증
- 금지·보류: 새 prime sweep, maximal-gap 데이터 취득, P018-B/P013-C/P019 actual, numerical `X_cert` 계산, threshold calculator, 숨은 `O` 상수의 임의 대입, commit/push/PR
- 선행 변경: 시작 시 `git status --short` 출력 없음(clean); 이번 작업은 새 H1a 산출물과 연결 정본만 변경한다.

## 목적과 완료조건

- 목적: Maynard의 asymptotic ratio를 곧바로 수치 부등식으로 오인하지 않도록, 유한한 `r`에서 어떤 명시적 적분 구간과 오차 증명서가 주어져야 `J_r/I_r` 하한이 엄밀히 따라오는지 standalone lemma와 proof contract로 고정한다.
- 완료조건:
  - 원문의 함수·적분·지원집합·식 번호를 1차 자료와 대조한다.
  - 숨은 상수를 넣지 않은 exact/interval 형태의 finite-r lemma를 증명한다.
  - 기계 판독 contract와 fail-closed verifier·단위시험을 만든다.
  - 닫힌 부분과 여전히 열린 smoothing/tail·moment 입력을 명확히 분리한다.
  - H1/T1/METHODS/이론 색인과 새 handoff를 동기화한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | `J_r/I_r`의 유한 하한만 대상; FGKMT/Sono 최종 정리 자체를 증명하지 않음 | 원문 정의와 식 번호를 대조하고 exact inequality만 채택 |
| 데이터·provenance | maximal-gap 데이터·actual artifact 불사용 | 1차 논문과 기존 H1/T1 원장만 사용, source locator 기록 |
| 통계·정밀도 | 통계 실험 없음; 수치가 필요하면 directed interval/exact rational contract만 허용 | binary float 단독 판정을 금지하고 입력 증명서 누락 시 fail-closed |
| 승인 경계 | 이론 정식화·toy 검증만 승인됨 | actual sweep와 threshold 계산은 수행하지 않음 |
| 산출물·비덮어쓰기 | 새 H1a 정본·contract·test 및 연결 문서 갱신 | 기존 actual artifact와 PDF 원본은 수정하지 않음 |

## 단계 현황

1. **COMPLETED — 원문 식·정의·proof dependency 대조**
2. **COMPLETED — finite-r lemma와 machine-readable contract 정식화**
3. **COMPLETED — fail-closed verifier·단위시험 구현 및 검증**
4. **COMPLETED — H1/T1/METHODS/이론 색인 동기화**
5. **COMPLETED — 다음 순서·커밋 제안·새 handoff 및 완료 처리**

## 단계별 기록

### 2026-09-04 05:56 KST — 착수·영향도 고정

- 수행: 최신 handoff, 열린 원장, H1 review·JSON trace, 작업원장 규약과 clean worktree를 확인했다.
- 파일: 이 작업원장 신규 작성.
- 명령·검증: `git status --short`; latest handoff/open-ledger/H1 파일 조회.
- 결과: 열린 선행 원장 없음, 시작 worktree clean, H1a 사용자 승인 확인.
- 문제·결정: 논문의 `O(1/log r)`를 단위 상수로 해석하지 않는다. 먼저 exact interval implication을 닫고 실제 finite `r_0`는 별도 수치 적분·tail certificate가 생길 때만 판정한다.
- 다음 재개점: Maynard 원문의 Lemmas 8.1/8.5/8.6과 식 (8.25)–(8.27), 정의된 함수와 지원집합을 완독·대조한다.

### 2026-09-04 06:30 KST — 원문 대조·finite lemma 정식화

- 수행: Maynard (7.10), (7.12), Lemma 8.6, (8.22)–(8.27), Maynard 2015 Section 7의 concentration 선례, Sono (2.3), pp. 541–542를 대조했다. unrestricted `F1`과 simplex-supported `F`를 구분하고 exact one-dimensional envelope와 Cantelli transfer를 도출했다.
- 파일: `docs/method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md`, `docs/method/theory/data/Sono_FMT_H1a_finite_r_integral_contract_v1.json`, `source/h1a_finite_r_integral.py`, `tests/test_h1a_finite_r_integral.py`.
- 명령·검증: 고정 FGKMT Python으로 80-dps 사전 scalar 계산과 60-dps directed-interval prototype scan 수행.
- 결과: `36<=r<=8103` 8068개에 improved variance envelope를 적용한 interval prototype failure 0, 최저 relative margin lower 약 0.02507 at `r=36`. `log r>=9`에는 monotonic analytic tail을 정식화하여 첫 정수 `r=8104`부터 덮었다.
- 문제·결정: Maynard (8.27)은 `F1`의 식이므로 Sono simplex supremum으로의 이동을 생략하지 않는다. 새 project lemma는 `SIV-06`만 닫고 full good-weight·`X_cert`는 열어 둔다.
- 다음 재개점: 신규 모듈·JSON·시험을 py_compile/targeted unittest로 검증하고 발견되는 구현 오류를 수정한다.

### 2026-09-04 — verifier 교정·전체 회귀검증

- 수행: 해석적 꼬리의 분산 비교를 다시 감사해 문서·코드의 불필요하게 거친 보조 비교를
  (V/(2c)<649/414720<9/2500<d^2)인 직접 유리수 chain으로 교정했다. control character가
  섞인 LaTeX 두 곳도 정상 `\\frac`으로 복구했다.
- 파일: `source/h1a_finite_r_integral.py`, `tests/test_h1a_finite_r_integral.py`,
  `tests/test_h1_good_sieve_weight_trace.py`, `tests/test_threshold_proof_obligation_ledger.py`, H1a contract.
- 검증: py_compile PASS; H1a/H1/T1 targeted 14 tests PASS. 전체 215 tests의 sandbox 실행은
  임시폴더 `PermissionError` 82건으로 환경 실패했고, 같은 명령을 승인된 sandbox 외부에서
  재실행해 215/215 PASS했다. 상태-count 고정 시험을 한 개 더 추가했으므로 최종 전체 검증은
  다시 실행한다.
- 결과: finite scan 8,068개 failure 0, 최저 relative lower margin >0.025 at r=36; r=35는 이
  certificate에서 fail-closed; analytic-tail endpoint checks 전부 PASS.
- 다음 재개점: 최종 216-test 회귀검증과 diff/JSON/control-character 감사를 실행한다.

### 2026-09-04 — 정본 동기화

- 수행: `SIV-06`만 `PARTIAL`에서 `EXPLICIT`으로 승격하고 T1 수량을 6/10/30/4/16으로
  동기화했다. H1 trace·review 23/24·METHODS·이론 색인·AGENTS에 H1a 결과와 H1b 다음 gate를
  반영했다.
- 결정: H1 전체 판정, 16 hard blockers, `FIN-05`, `X_cert`, `X_star`는 변경하지 않았다.
- 다음 재개점: 최종 검증 뒤 새 timestamp handoff를 작성하고 원장을 `-done`으로 바꾼다.

### 2026-09-04 06:23 KST — 최종 검증·핸드오프

- 수행: 신규 파일·참조 경로·JSON parse·control character·whitespace를 재감사하고
  `handoff/202609040623_HANDOFF.md`를 작성했다.
- 검증: 최종 targeted 15/15 PASS; 최종 전체 unittest sandbox 외부 216/216 PASS(38.869초);
  JSON 3종 parse PASS; 필수 파일 5개 존재; `git diff --check` whitespace error 0.
- 경계: actual experiment·새 data·threshold calculator·commit/push를 실행하지 않았다.
- 다음 재개점: 사용자 승인이 있으면 H1b Maynard Proposition 6.1 constant ledger를 착수한다.

## 현재 재개점

작업 완료. 다음 세션은 새 handoff를 읽고 H1b 승인 여부부터 확인한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화 (`test_result` actual 색인은 변경 불필요)
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
