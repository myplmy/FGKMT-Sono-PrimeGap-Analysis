# H1b-2a.3 Proposition 9.4 end-to-end 합성 작업원장

- 시작: 2026-09-08 20:51 KST
- 상태: 완료
- 승인: 사용자가 권장 순서에 따른 H1b-2a.3 착수를 명시 승인
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609082034_HANDOFF.md`

## 목표

Maynard Proposition 9.4의 실제 FGKMT/FMT 호출에서 이미 개별적으로 유한화한 smooth/sharp
summation, Lemma 8.5--8.6 weight envelope, Euler normalization, 식 (9.52) distribution
error를 원문의 한 계산 흐름으로 다시 연결한다. 모든 가정·곱셈계수·오차합·공통 cutoff를
추적하여 `H1B-P94` 부모를 닫을 수 있는지 엄격하게 판정한다.

## 비목표·승인 경계

- 실제 소수 또는 maximal-gap sweep을 실행하지 않는다.
- P018-B나 다른 actual 실험을 실행하지 않는다.
- Sono 최종 `X_cert` 또는 threshold calculator를 만들지 않는다.
- 열린 `O`, `o`, Vinogradov 상수를 임의로 1로 두지 않는다.
- 선행 정리의 가정·변수 정규화·유효범위가 실제 호출과 일치하기 전에는 채택하지 않는다.
- 패키지·Lean 설치, commit, push, PR, 외부 게시는 별도 사용자 승인 없이는 하지 않는다.

## 변경 전 영향 분석

| 축 | 판정 | 근거·통제 |
|---|---|---|
| 반복로그·end-bounded `G/H` | 영향 없음 | empirical pipeline을 실행하거나 수정하지 않음 |
| dataset provenance·coverage | 영향 없음 | 외부 maximal-gap dataset을 취득하지 않음 |
| 큰 정수·고정밀도 | 영향 있음 | explicit 상수 합성은 exact integer 및 `mpmath` 보조검산으로 교차 확인 |
| 정리/경험적 주장 구분 | 영향 있음 | project finite lemma와 원 논문 theorem을 분리하고 `X_cert` 비승격 |
| 승인 경계 | 영향 있음 | 이론·toy 검산만 수행; actual 계산 금지 |
| 재현성 | 영향 있음 | 기계 판독 계약, 독립식 시험, source/page/equation provenance 저장 |
| 문서·상위 원장 | 영향 있음 | H1b/H1/T1/METHODS/AGENTS와 predecessor/successor 상태를 함께 감사 |

## 단계별 계획과 진행 기록

### 단계 0 — 범위·상태 고정

- [x] 최신 handoff와 AGENTS 승인 경계 확인
- [x] 미완료 작업원장 0개와 깨끗한 시작 worktree 확인
- [x] 영향 분석 및 fail-closed 상태 작성
- 현재 상태: `H1B2A-P94-DISTRIBUTION=ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`,
  `H1B-P94=RATE_MISSING`, `SIV-07/08/09=HARD_BLOCKER`, `X_cert=OPEN`.
- 다음 재개점: 단계 1 원문·선행연구 대조.

### 단계 1 — 원문·선행 정리 대조

- [x] Maynard Proposition 9.4 식 (9.49)--(9.70)의 주항·분포오차·Selberg denominator·Euler 곱·residue-class factor와 가정을 등록
- [x] Lemmas 8.2--8.6 및 Proposition 9.1과의 실제 의존선 확인
- [x] FGKMT/FMT 실제 파라미터 \(\mathcal A=\mathbb Z,D=1,\alpha=2,\theta=1/3,\xi=\theta/10,R=(x/4)^{\theta/3}\)와 support·제외모듈·끝점 조건 확인
- [x] 후속 교정 또는 더 직접적인 explicit 선행증명이 있는지 표적 조사
- 출처 증거: Maynard 최종 출판본 Proposition 9.4, pp. 1547--1550, 식
  (9.49)--(9.70); 저자 TeX `Subsets.tex` 1044--1169행; FGKMT JAMS 최종본
  Theorem 6과 식 (7.8); FMT Theorem 6 실제 호출.
- 교정 확인: 저자 TeX의 식 (9.56)은 `r_0|d_0`로 잘못 적혔지만 최종 출판본은
  올바른 `d_0|r_0`로 교정돼 있다. 합성은 최종 출판본을 따른다.
- 선행연구 우선 조사: Maynard 원문, FGKMT, FMT 및 관련 후속 upper-moment 문헌을
  표적 대조했으나 이 실제 \(\mathcal A=\mathbb Z\) P9.4 호출을 숨은 상수 없이 그대로
  제공하는 drop-in 정리는 확인하지 못했다. 이는 표적 조사 결과이지 전 세계 novelty
  주장이 아니다. 따라서 이미 감사한 원문 계산을 보존하는 project finite lemma로 진행한다.
- 추가 다운로드·설치: 로컬 원문과 기존 계약으로 충분하여 불필요. Lean 및 추가 Python
  라이브러리도 현재 단계에는 필요하지 않다.
- 다음 재개점: 단계 2에서 (9.58), (9.65)--(9.70)과 distribution child를 한
  multiplier·공통 cutoff로 합성한다.

### 단계 2 — end-to-end 유한 합성

- [x] 닫힌 하위 package를 원문 식 (9.49)--(9.70)에 일대일 대응
- [x] 합성 과정의 덧셈·곱셈계수와 공통 cutoff를 중복 없이 계산
- [x] 전체 오류/주항 비와 충분조건을 유한식으로 정식화
- [x] 부모 `H1B-P94` 승격 가능 여부 및 남은 blocker 판정
- 합성 결과: \(T_{94}\)에 대한 actual-call multiplier를
  \[
  C_{94}=\frac{1+\delta_s}{(1-\delta_s)^2}
  e^{2+6/k}(1+2^k\varepsilon_c)\frac{\log R}{\log x}+\rho_{94}
  \]
  로 얻었다. P94 전용 강화 smooth gate
  \(\delta_{\rm sum}\le2^{-k-1}\)를 두면
  \(2^k\varepsilon_c\le1\)이고, 실제
  \(\log R/\log x\le\theta/3=1/9\)이므로
  \(C_{94}\le12e^{2+6/k}(\theta/3)+1<13\) (\(k\ge36\))이다.
- 공통 cutoff는 H1b-2a.2의 \(Y_{94}\), 강화 smooth cutoff의 actual-x 변환,
  원문 차원조건 \(k^5\), 실제
  \(R\ge x^{\theta/10}\) 조건 \((10/7)\log4\)의 최댓값이다.
- 판정: 실제 FGKMT/FMT 호출의 `H1B-P94`만
  `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`으로 승격 가능. 일반
  \(\mathcal A\), Proposition 6.1, `H1B-COMP-01`, `SIV-07/09`,
  `X_cert`는 계속 열려 있다.

### 단계 3 — 코드·기계 계약·시험

- [x] exact/고정밀도 보조 모듈 작성
- [x] 정상·경계·오류 입력과 독립식 단위시험 작성
- [x] source/version/equation/state를 JSON 계약에 기록
- [x] `py_compile` 및 신규 표적 회귀시험 통과
- 구현: `source/h1b2a3_proposition94_composition.py`.
- 계약: `docs/method/theory/data/Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json`.
- 시험: `tests/test_h1b2a3_proposition94_composition.py`, 7/7 PASS. 균일 상수 13의 마지막
  비교는 `Fraction`으로 \(e<49/18<11/4\), \((11/4)^{13}<9^6\)을 검사해
  `mpmath` 반올림과 분리했다.
- 설명용 진단: \(k=36\)에서 강화 gate의
  `log_x ~= 5.2577378160106370e144`, actual main/total multiplier
  `~=1.0090733752662167`, uniform coarse multiplier `~=12.638851151626843`;
  \(k=100\)에서도 모든
  actual-call gate PASS. directed rounding 또는 final threshold 주장이 아니다.
- 다음 재개점: 단계 4 이론·검토 문서와 상위 H1b/H1/T1 정본 동기화.

### 단계 4 — 정본 동기화

- [x] 신규 이론 정본과 비판적 타당성 검토 작성
- [x] H1b/H1/T1 및 predecessor 문서·JSON 상태 동기화
- [x] METHODS, 이론 색인, AGENTS 현재 상태 갱신
- [x] 과거 사실은 successor update로 보존하고 소급 변경 금지
- 정본: `docs/method/theory/31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md`,
  `docs/review/37_20260908_H1b2a3_Proposition94_end_to_end_타당성검토.md`.
- predecessor의 당시 `RATE_MISSING` 행은 그대로 두고
  `h1b2a3_successor_contract`와 `successor_status_update`로 현재 상태를 연결했다.
- H1b master schema는 1.8.0, H1/T1 schema는 각각 1.5.0으로 올렸으며,
  `H1B-P94=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`과 root non-promotion을 함께 고정했다.
- 자체감사 교정: 첫 합성 초안의 공통 smooth gate만으로는
  \(2^k\varepsilon_c\)가 uniform하지 않았다. 정본 반영 전에
  \(\Delta_c\le2^{-k-1}\)인 강화 gate로 바꿨고, 오류 원장 E033에 기록했다.
- 다음 재개점: 단계 5 전체 검증과 handoff.

### 단계 5 — 전체 검증·handoff

- [x] 전체 unittest, JSON strict parse, Markdown 참조, `git diff --check`
- [x] 실패·환경 문제를 오류 원장에 기록
- [x] 새 timestamp handoff 작성
- [x] 사용자 보고·다음 권장 순서·한국어 commit 메시지 작성
- [x] 모든 산출물 완료 후 원장 파일명을 `-done.md`로 변경

최종 검증 증거:

- 연구 Python `py_compile`: PASS.
- 신규 H1b-2a.3 시험: 7/7 PASS.
- sandbox 밖 전체 회귀시험: `Ran 335 tests in 41.166s / OK`.
- 갱신·신규 JSON 7개 `python -m json.tool`: PASS.
- 변경 Markdown 18개 상대 참조 검사: PASS.
- `git diff --check`: whitespace error 0. 표시된 LF/CRLF 메시지는 Git의 줄바꿈
  안내이며 검증 실패가 아니다.
- actual prime/maximal-gap 실험, P018-B, threshold calculator, 패키지·Lean 설치는
  수행하지 않았다.
- 새 핸드오프: `handoff/202609082158_HANDOFF.md`.

## 현재 재개점

작업 완료. 다음 착수 후보는 H1c-1a quantitative character/prime-distribution source
inventory와 실제 FGKMT affine-form 적용성 감사다.
