# Sono/FMT H1 good-sieve-weight recoverability source tracing 작업원장

- 시작: 2026-09-02 20:06 KST
- 현재 상태: COMPLETED
- 사용자 승인:
  - numerical threshold 질문을 비전문가가 이해하기 쉽게 설명
  - 현재 `10^20` 검증과 theorem threshold 사이의 규모·연산시간을 증거에 맞춰 평가
  - H1 good-sieve-weight recoverability source tracing 착수
- 금지·보류:
  - 알 수 없는 상수·유효범위를 임의 숫자로 채우지 않음
  - numerical `X_cert` 계산기·실제 threshold 계산 미수행
  - 새 prime sweep, P018-B, P013-C, P019 actual 미실행
  - 패키지 변경, 외부 게시, commit/push/PR 미수행

## 목적과 완료조건

1. “얼마나 더 큰 수까지 계산해야 전역 부등식을 확인하는가”에 대해 finite computation과
   theorem certificate를 분리해 답한다.
2. P013 등 실제 관측 runtime을 이용한 동일 pipeline 규모 추산은 가정과 한계를 명시한다.
3. FMT Theorem 6, FGKMT Theorem 5/6, Maynard Proposition 6.1과 (8.27)의 proof chain을 추적한다.
4. `r_0`, `c_0`, finite-r integral error, Hypothesis 1 상수를 숫자로 복원할 constructive path가
   있는지 node별로 판정한다.
5. H1 정본 review·T1 상태 갱신·검증·새 handoff를 완료한 뒤 `-done` 전환한다.

## 불변식과 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded 정의 | 변경 없음 | `G_1`과 project `G`의 동일 경계 유지 |
| threshold 세 수준 | 중요 | `X_emp`, `X_cert`, `X_star`를 분리 |
| 데이터·provenance | 변경 없음 | 기존 result/log와 원문만 읽기 |
| 실제 계산 | 미승인·불필요 | scalar 예시 외 prime 계산 금지 |
| 증명 정확성 | 중요 | source/page/equation과 숨은 의존성을 행 단위 기록 |
| 예상시간 | 추정 | 관측 runtime과 proof-size sensitivity를 구분 |
| 정본 | 영향 있음 | T1 ledger, review, METHODS/AGENTS, handoff 동기화 |

## 단계 현황

1. **COMPLETED — 최신 handoff·T1·실제 runtime 증거 복원**
2. **COMPLETED — 사용자 질문의 계산 규모·시간 시나리오 분석**
3. **COMPLETED — Maynard finite-r integral·Proposition 6.1 추적**
4. **COMPLETED — FGKMT/FMT good-weight·Hypothesis 1 상수 추적**
5. **COMPLETED — H1 constructive-path 판정과 다음 proof gate 작성**
6. **COMPLETED — 정본 동기화·검증·handoff·커밋 제안**
7. **COMPLETED — 작업원장 `-done` 전환**

## 단계별 기록

### 2026-09-02 20:06 KST — 시작

- `git status --short`: 출력 없음, clean worktree
- 비 `-done` 작업원장: 없음
- 최신 handoff: `handoff/202609021757_HANDOFF.md`
- 기준 T1: `docs/method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md`
- 다음 재개점: P013 actual runtime·범위와 T1 SIV node를 증거 파일에서 복원

## 현재 재개점

P013-A/B 실제 범위·prime/gap count·wall time을 정본 report/log에서 읽고, 순진한 범위 확장
추정과 specialized prime-gap search의 차이를 먼저 고정한다.

### 2026-09-02 20:15 KST — runtime·원문 proof chain 복원 완료

- P013-B 관측 기준:
  - 범위 `[10^11,10^12)`, gap start `33,489,857,205`
  - analysis `40,073.308`초, saved full recomputation 포함 전체 약 23시간 2분
- P017 동일범위 비교: serial `12,598.410`초, parallel `2,866.160`초, wall-time 비
  `4.3956`; 다른 범위에 그대로 외삽하지 않는다.
- 고정 FGKMT Python의 `li(10^21)-li(10^20)` 근사:
  `18,906,449,883,832,462,698.8` gap starts.
- P013-B 처리율을 선형 외삽한 설명용 수치:
  - one pass 약 `716,882`년
  - two pass 약 `1,433,765`년
  - 관측 `4.3956`배를 가정해도 one pass 약 `163,091`년
- 위 수치는 현재 Python segmented-sieve recurrence pipeline의 설명용 외삽일 뿐,
  specialized/distributed maximal-gap search의 성능 추정이나 수학적 하한이 아니다.
- FMT Theorem 6은 good weight를 직접 재증명하지 않고 FGKMT Theorem 5를 호출한다.
- FGKMT Theorem 5/6은 Maynard Proposition 6.1의 moment formula와 Hypothesis 1을 호출한다.
- Maynard는 Theorem 3.1 상수가 Hypothesis 1 상수가 effective이면 effective라고 명시하지만,
  Proposition 6.1 proof에는 `sufficiently large/small`, implied constants와 여러 absorption이 남는다.
- Maynard (8.27)의 `J_r/I_r=(log r)/(4r)(1+O(1/log r))`는 constructive extraction의
  가장 가까운 출발점이나, 인쇄된 식만으로 finite `r_0`을 계산할 수는 없다.
- FGKMT Lemma 7.2는 Hypothesis 1의 absolute implied constants와 effective character bound를
  말하지만 `c_1` sufficiently small, zero-free/Bombieri–Vinogradov 상수를 숫자로 주지 않는다.
- FMT는 FGKMT의 `r <= (log x)^(1/5)`보다 일반적으로 `r <= (log x)^c_0`를 사용하며
  `c_0` 자체가 sufficiently small로 미지다. 따라서 임의 `r_0` 예시로 실제 threshold를
  추정하지 않는다.
- 다음 재개점: H1 machine-readable trace와 비전문가용 review를 작성하고 T1 정본을 동기화한다.

### 2026-09-02 20:25 KST — H1 판정·정본 작성

- 신규 review:
  `docs/review/24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md`
- 신규 machine trace:
  `docs/method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json`
- 신규 fail-closed test:
  `tests/test_h1_good_sieve_weight_trace.py`
- H1 9개 node 판정:
  - `SIV-05/06`: `CONSTRUCTIVE_PATH_IDENTIFIED`
  - `SIV-02/07/08/09/10`: `QUANTITATIVE_REPROOF_REQUIRED`
  - `SIV-01/11`: `DEPENDENCY_BLOCKED`
- overall:
  `CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED`
- numerical `X_cert`: 계속 `OPEN`; threshold calculator gate fail-closed
- 동기화:
  - T1 proof-obligation 원장
  - T1 hard-node feasibility review
  - theory index
  - `docs/METHODS.md`
  - `AGENTS.md`
- targeted H1+T1 unittest: 9/9 PASS
- 다음 재개점: 전체 unittest·diff·문서 정합성을 검증한 뒤 새 handoff와 commit 제안을 작성한다.

### 2026-09-02 20:28 KST — timestamp audit

- 작업원장 초안의 두 단계 시각이 현재 system clock보다 뒤로 적힌 것을 발견해 실제 작업 순서 안의
  시각으로 즉시 교정했다. 파일 내용·검증 결과·수학 판정에는 영향이 없다.

### 2026-09-02 20:28 KST — 검증·handoff 완료

- `py_compile`: PASS
- H1+T1 targeted unittest: 9/9 PASS
- 전체 unittest sandbox 실행: 임시 디렉터리 권한으로 82 errors; 회귀 판정에 사용하지 않음
- 동일 전체 unittest sandbox 외부 재실행: 210/210 PASS, 31.076초
- `git diff --check`: whitespace error 0; CRLF 안내만 존재
- 신규 handoff: `handoff/202609022028_HANDOFF.md`
- 실제 prime 계산·dataset 다운로드·threshold calculator: 미수행
- 사용자 실행 명령: 없음; 다음 요청은 H1a 착수 승인 여부

## 완료 전 점검

- [x] finite 계산과 theorem certificate를 혼동하지 않음
- [x] runtime 추정의 기준·가정·불확실성 명시
- [x] H1 source/page/equation 추적
- [x] constructive path / quantitative reproof / blocked 판정
- [x] 정본 동기화와 전체 검증
- [x] 새 timestamp handoff
- [x] 작업원장 `-done` 전환
