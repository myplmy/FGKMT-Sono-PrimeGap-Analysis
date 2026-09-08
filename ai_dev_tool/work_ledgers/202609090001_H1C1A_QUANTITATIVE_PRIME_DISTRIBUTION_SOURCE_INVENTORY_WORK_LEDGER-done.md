# H1c-1a quantitative prime-distribution source inventory 작업원장

- 시작: 2026-09-09 00:01 KST
- 상태: COMPLETE_PENDING_RENAME
- 승인: 사용자가 `H1c-1a source inventory 착수`를 명시 승인
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609082158_HANDOFF.md`

## 목표

Maynard Proposition 9.2와 FGKMT Hypothesis 1(2)의 실제 호출에 필요한 정량적
character-sum, Bombieri--Vinogradov형 분포, exceptional modulus, affine-linear-form 및
prime-density 입력을 원 논문·교정본·후속 explicit 연구에서 추적한다. 각 후보 정리가 실제
FGKMT 파라미터에 그대로 적용되는지 가정, 변수 정규화, modulus 범위, exceptional character,
끝점, 상수와 finite cutoff 단위로 판정하고 H1c-1b에 넘길 최소 증명 의무를 확정한다.

## 비목표·승인 경계

- 실제 prime/maximal-gap sweep, P018-B 또는 다른 actual 실험을 실행하지 않는다.
- 아직 추적하지 않은 `O`, `o`, Vinogradov 상수를 임의 숫자로 대체하지 않는다.
- source inventory만으로 Hypothesis 1(2), Proposition 9.2, Proposition 6.1, `SIV-07/09`
  또는 `X_cert`를 닫지 않는다.
- threshold calculator나 장시간 계산 runner를 만들지 않는다.
- 패키지·Lean 설치, commit, push, PR, 외부 게시는 별도 사용자 승인 없이는 하지 않는다.
- 표적 조사에서 drop-in 정리를 찾지 못해도 전 세계 novelty 또는 비존재를 주장하지 않는다.

## 변경 전 영향 분석

| 축 | 판정 | 근거·통제 |
|---|---|---|
| 반복로그·end-bounded `G/H` | 영향 없음 | empirical pipeline·정의·결과를 수정하거나 실행하지 않음 |
| dataset provenance·coverage | 영향 없음 | maximal-gap dataset을 취득·변환하지 않음 |
| 정리/경험적 주장 구분 | 영향 있음 | source inventory와 theorem closure를 분리하고 모든 root를 fail-closed 유지 |
| proof dependency | 영향 있음 | H1c 20행, H1b/H1/T1 DAG와 실제 FGKMT 호출의 관계를 감사 |
| 원천 provenance | 영향 있음 | 1차 원문·출판본·교정본·explicit 후속연구의 판본과 위치를 기록 |
| 수치·큰 정수 | 확인 필요 | explicit 후보가 있으면 상수·cutoff 산술만 FGKMT Python으로 보조검산 |
| 승인 경계 | 영향 있음 | 문헌·정적 증명 감사만 수행하고 actual 계산은 금지 |
| 재현성 | 영향 있음 | source inventory를 JSON 계약과 단위시험으로 고정할지 단계 3에서 판정 |
| 정본 동기화 | 영향 있음 | theory 16, H1/H1b/T1, METHODS, 이론 색인, AGENTS, handoff를 근거에 맞춰 갱신 |

## 단계별 계획과 진행 기록

### 단계 0 — 범위·상태 고정

- [x] 최신 handoff, AGENTS, 승인 경계 확인
- [x] 미완료 작업원장 0개와 깨끗한 시작 worktree 확인
- [x] 영향 분석과 fail-closed 비목표 기록
- 시작 상태: H1b-2a.3 actual P94만 닫힘. Hypothesis 1(2), Proposition 9.2,
  `H1B-COMP-01`, `SIV-07/09`, `X_cert`는 열려 있음.
- 다음 재개점: 단계 1에서 로컬 정본과 실제 source call을 식 단위로 복원한다.

### 단계 1 — 현재 의무와 실제 호출 복원

- [x] theory 16의 H1c 20개 node와 JSON 계약 상태 감사
- [x] Maynard Proposition 9.2의 정확한 가정·결론·오차항·의존 정리 추적
- [x] FGKMT Hypothesis 1(2), 식 (7.2)--(7.3), 실제 \(\mathcal A,\mathcal P,\mathcal L,B,D\)
  치환과 exceptional modulus 처리 복원
- [x] FMT/Sono로 이어지는 적용 경로와 필요한 정량 출력 확정
- 착수 오류: `tmp` 전역 read-only 검색으로 접근 제한 경고를 재발시켰고 H1c JSON 이름을
  한 번 잘못 추정했다. 연구 증거·파일에는 영향이 없으며 오류 원장 E035에 기록했다.
- 교정된 다음 재개점: 정확한
  `docs/method/theory/data/Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json`과 이미 알려진
  개별 PDF/TeX 경로만 읽는다.
- 완료 증거:
  - Maynard author TeX의 Hypothesis 1(2)와 Proposition 9.2를 직접 대조했다. P9.2는 바로 그
    평균 discrepancy를 가정하며 implied constant가 \(\theta,\alpha\)와 Bdd1--Bdd3 상수에
    의존한다.
  - FGKMT 최종 PDF의 Hypothesis 1, Lemma 7.1--7.2, 식 (7.2)--(7.3)을 확인했다. 원래 경로는
    \(\theta=1/3\), \(k\le\log^{1/5}x\), affine forms와 한 exceptional prime \(B\)를
    함께 다뤄야 한다.
  - 정량 출력은 exact centered count, \(q\le x^{1/3}\), \((q,B)=1\),
    \((\log x)^{-100k^2}\), prime-density lower bound와 하나의 공통 finite cutoff로 확정했다.

### 단계 2 — 선행연구 source inventory와 적용성 판정

- [x] 원 논문·교정본·후속 explicit 연구를 우선 조사
- [x] 각 후보를 가정, 범위, 상수, cutoff, exceptional character, affine 변환별로 판정
- [x] `DROP_IN`, `PARTIAL_INPUT`, `CONCEPTUAL_ONLY`, `NOT_APPLICABLE`로 분류
- [x] 누락된 연결부와 H1c-1b의 최소 직접증명 범위 확정
- 완료 증거:
  - Akbary--Hambrook, Sedunova 2018/2019, Yamada I/II, Bordignon, Bennett et al., Kadiri,
    Liu와 Johnston의 1차 원문·출판 metadata를 조사했다.
  - exact theorem 페이지는 Yamada II p.2, Sedunova 2018 p.2, Bordignon pp.3--4를
    PNG로 렌더링해 OCR뿐 아니라 시각 대조했다.
  - `DROP_IN` 후보는 0개다. Bordignon 2021 Theorem 4가 가장 가까운
    `PRIMARY_COMPOSITION_CANDIDATE`지만 growing \(A\), 하나의 공통 exceptional \(B\), affine
    lift, 중심항 변환, \(\psi\to\pi\), endpoint와 공통 cutoff 연결 증명이 남는다.
  - Sedunova 2019 Corollary 1.4는 Johnston 2026이 작은 오류와 log 분모 손실을 교정했으므로
    인쇄식 그대로 채택하지 않는다. Johnston 원고 자체는 최근 preprint라 redesign 후보로만 둔다.
- 보존 증거: `tmp/pdfs/h1c1a/`의 PDF·추출 text·렌더 page는 H1c-1b source provenance로
  `RETAIN`한다. 이 경로가 `tmp`라는 이유만으로 삭제하지 않는다.

### 단계 3 — 정본·기계 계약 작성

- [x] H1c-1a source inventory 이론 문서와 비판적 검토 작성
- [x] source/equation/dependency/status를 JSON 계약으로 기록
- [x] 계약 consistency·negative assertion 단위시험 작성
- [x] predecessor H1c/H1b/H1/T1 상태를 successor 방식으로 동기화
- 산출물:
  - `docs/method/theory/32_Sono_FMT_H1c1a_quantitative_prime_distribution_source_inventory.md`
  - `docs/review/38_20260909_H1c1a_quantitative_prime_distribution_타당성검토.md`
  - `docs/method/theory/data/Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json`
  - `tests/test_h1c1a_prime_distribution_inventory.py`
- 동기화: theory 12/14/16, H1/H1b/T1 JSON pointer와 T1 `SIV-08` notes,
  METHODS, theory index, reviews 22--24, AGENTS를 fail-closed 상태로 갱신했다.
- 표적 검증: 새 test 7/7 PASS. 모든 local PDF hash, source/candidate/requirement 참조,
  `drop_in=false`, Bordignon 단일 primary candidate와 parent closure=false를 확인했다.
- 작업 중 patch 문맥 오류와 교정은 오류 원장 E037에 기록했다.

### 단계 4 — 전체 검증·handoff

- [x] FGKMT Python `py_compile`, 표적·전체 unittest
- [x] JSON strict parse, Markdown 참조, `git diff --check`
- [x] 오류·실패가 있으면 오류 원장에 기록
- [x] 새 timestamp handoff와 다음 권장 순서·예상시간·한국어 commit 메시지 작성
- [x] 모든 산출물 완료 뒤 작업원장을 `-done.md`로 변경
- 검증 증거:
  - 새 test: 7/7 PASS
  - H1c/H1b/H1/T1 직접 영향 test: 32/32 PASS
  - 전체 suite: `Ran 342 tests in 39.627s / OK`
  - 변경 JSON 5개 strict parse: PASS
  - 핵심 Markdown local link: PASS
  - section header 순서: PASS
  - `git diff --check`: whitespace error 0; LF/CRLF 안내만 존재
- 오류 기록: E035--E038. 모두 도구·검색·서지·patch 단계에서 정본 완료 전에 교정됐고
  actual 실험이나 수학 판정 오염은 없다.
- 새 handoff: `handoff/202609090052_HANDOFF.md`

## 현재 재개점

단계 4의 모든 산출물과 검증을 완료했다. 안전 절차에 따라 이 파일을
`202609090001_H1C1A_QUANTITATIVE_PRIME_DISTRIBUTION_SOURCE_INVENTORY_WORK_LEDGER-done.md`로
이름 변경하는 것만 남았다.
