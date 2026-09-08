# H1b-1b-2d.1a.1 scalar remainder 수치 재증명 작업원장

- 시작: 2026-09-08 11:51 KST
- 현재 상태: COMPLETED
- 사용자 승인: 권장 1순위 H1b-1b-2d.1a.1부터 문헌 우선 source 추적·필요한 최소
  직접증명·보조 코드와 회귀검증·정본·핸드오프 갱신
- 허용: 로컬/웹 학술자료 조사·필요시 다운로드, 가정·정규화·유효범위 대조,
  고정 FGKMT Python의 데이터 비의존 exact/toy 검증
- 금지·보류: 실제 prime/maximal-gap sweep, P018-B, numerical theorem threshold 계산,
  숨은 `O`/`<<` 상수를 1로 대입, 승인 없는 package/Lean 설치, commit/push/PR
- 작업트리 경계: 직전 H1b-1b-2d.1a 변경은 미커밋 상태다. 이를 보존하고 이번 후속
  변경만 추가하며 사용자 파일을 삭제·되돌리지 않는다.

## 목적과 완료조건

목적은 Maynard source 986--999행의 `YmError` 경로를 정량 재증명해

\[
\varepsilon_Y\le C_Y\frac{T_k(\log\log R)^2}{\log R}
\]

형태의 실제 수치 (C_Y)와 유한 적용범위를 얻을 수 있는지 판정하는 것이다.

완료조건:

1. 939--1038행의 정확한 main/error 분해와 모든 정규화 인자를 식 단위로 복원한다.
2. 동일하거나 더 강한 explicit lemma를 선행연구에서 먼저 찾고 실제 가정·함수·범위에
   적용 가능한지 개별 검토한다.
3. 직접 증명할 경우 s-Euler product, t-divisor sum, determinant와 prefactor를 별도
   obligation으로 분해하고 각 부등식의 방향·상수·시작점을 고정한다.
4. 원문 불일치 또는 정보 부족으로 공통 (C_Y)를 닫을 수 없으면 닫힌 하위식과 정확한
   blocker를 분리해 fail-closed로 남긴다.
5. 하위 진전만으로 `H1B-L84`, `SIV-07`, (X_{\rm cert})를 승격하지 않는다.
6. 코드·JSON·정본·상위 DAG·오류 원장·handoff를 같은 상태로 동기화하고 전체 시험을
   고정 FGKMT Python으로 검증한다.

## 영향도 분석

| 축 | 영향 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | `O`/`<<`를 숫자 1로 두지 않고 합·곱·정규화별 상수를 추적한다. |
| actual 데이터 | NONE | `datas/`, `test_result/` 실제 산출물을 생성·분석하지 않는다. |
| source provenance | HIGH | Maynard 출판본·TeX와 채택하는 선행 lemma의 위치·hash·가정을 기록한다. |
| 수치 엄밀성 | HIGH | 정수·유리수·단조부등식을 우선하고 부동소수 계산은 진단으로만 쓴다. |
| 승인 경계 | HIGH | 이론 및 데이터 비의존 검증까지만 수행한다. |
| 상위 proof DAG | HIGH | scalar branch가 닫혀도 sharp xi, Lemmas 8.5--8.6, H1c/PAP가 남는다. |
| 재현성 | HIGH | source locator, 식별 obligation, 실패 조건과 회귀시험을 남긴다. |

## 접근 순서

1. 원문 식을 정확히 전사해 (s,t,e_m,r/\phi_L(r))의 역할과 정규화를 복원한다.
2. 각 하위합에 바로 적용되는 explicit divisor/Euler-product lemma를 문헌 우선으로 찾는다.
3. 적용 가능한 선행식은 가정 매핑을 증명하고, 없는 가장 작은 연결부만 직접 정량화한다.
4. 최종 (C_Y)를 합치기 전 각 branch의 상수·range를 독립 계약으로 검증한다.

## 단계 현황

1. **COMPLETED — 승인·영향·기존 정본 경계 고정**
2. **COMPLETED — Maynard 939--1038행 식·정규화 전수 복원**
3. **COMPLETED — 선행 explicit lemma 조사와 적용성 판정**
4. **COMPLETED — 최소 직접증명·기계 계약 구현**
5. **COMPLETED — 상위 정본 동기화·표적/전체 검증**
6. **COMPLETED — 새 handoff와 완료 원장 처리**

## 단계별 기록

### 2026-09-08 11:51 KST — 착수

- 최신 `handoff/202609081124_HANDOFF.md`와 theory 25/review 31을 확인했다.
- 직전 작업은 전역 (H)의 (C^1) 요구만 우회했으며 source scalar multiplier는 OPEN이다.
- memory registry에는 이 새 하위 gate의 추가 상세가 없어 최신 저장소 정본을 기준으로 한다.
- 다음 재개점: Maynard author TeX 935--1038행과 출판 PDF의 대응 식을 병렬 대조하고,
  정확한 (e_m), Δ, (s), (t) 합과 최종 정규화식을 별도 메모로 추출한다.

### 2026-09-08 13:10 KST — 원문 복원·문헌 우선 조사 완료

- Maynard author TeX 939--1038행과 출판본 인쇄면 1544--1546쪽의 식
  (9.39)--(9.47)을 대조했다. `s`, `t`, `e_m` 합과 main/error prefactor를 각각
  분리했다.
- 중요한 source 정정: author TeX 986행은 determinant 곱에 `i=m`을 넣지만 최종
  출판본 식 (9.43)은 정확히 `i != m`이다. 따라서 논문 출판본의 ambiguity가 아니라
  구 TeX와 출판본의 차이다. theory 25와 JSON의 기존 경고를 교정 대상으로 표시했다.
- Rosser--Schoenfeld 출판본 인쇄면 70쪽 Theorem 6의 (3.24), 인쇄면 72쪽
  (3.41)--(3.42)를 원문·렌더 양쪽으로 확인했다. 각각
  `sum_(p<=x) log(p)/p < log x (x>1)`과 예외안전 totient 상계를 제공한다.
- 표적 웹 검색에서는 source (9.42)--(9.44)의 동일한 vector multiplicity,
  determinant support, corrected Lemma 8.3 normalization을 한꺼번에 수치화한
  peer-reviewed lemma를 찾지 못했다. 전 세계 부재 주장은 하지 않는다.
- 직접 재증명 범위를 다음 네 연결부로 최소화했다.
  1. 서로소 분모를 먼저 분리한 뒤의 `s` Euler product
  2. published `Delta_m=product_(i!=m)|a_m b_i-a_i b_m|`에 대한 `t` divisor sum
  3. `phi_L`·totient·`c_gamma`의 exact prefactor cancellation
  4. direct line-1015 error와 `YmError`의 공통 scalar multiplier 결합
- 다음 재개점: 위 네 보조정리와 finite gate를 코드·JSON·방법론 문서로 구현한다.

### 2026-09-08 (시각 미기록) — scalar 상수·finite gate 구현 완료

- \(s\)-Euler product를 729, \(t\)-divisor 합을
  \(64467/3500<19\), determinant log-log 흡수를 2, prefactor residual을
  \(36/35\)로 각각 분리해 증명했다.
- YmError branch를 \(355028832/35\)에서 한 번 위로 반올림해
  \(10,143,681\)로 고정했다.
- direct (9.47) branch는 \(z=R^{U_k}\) support rescaling을 명시해
  \(4C_{8.3}(1/2,8)\)로 제한했다.
- 공통 상수는
  \(C_Y=327680(14801/69)e^{264}+10,143,697
  <3.17\times10^{122}\)이다.
- source/h1b1b2d1a1_scalar_remainder.py, 신규 JSON 계약, theory 26,
  review 32와 8개 표적 회귀시험을 작성했다.
- 첫 표적시험은 exp(log(C)) 경로와 직접식 사이 약 \(1.74\times10^{-79}\) 상대
  반올림차를 기본 exact tolerance로 비교해 1건 실패했다. symbolic coefficient는
  바꾸지 않고 수치 tolerance를 \(10^{-75}\)로 명시한 뒤 8/8 PASS했다.
- 구 author TeX와 최종 출판본을 혼동했던 과거 문구를 theory 25, review 31, JSON에서
  교정하고 오류 원장 E031에 기록했다.
- 상위 H1B-L84, SIV-07, \(X_{\rm cert}\)는 승격하지 않았다.
- 다음 재개점: theory index, METHODS, T1/H1b 원장, AGENTS와 회귀 기대값을 현재 상태로
  동기화한 뒤 표적 및 전체 suite를 실행한다.

### 2026-09-08 13:23 KST — 정본 동기화·전체 회귀검증 완료

- scalar successor 계약을 H1b-1 basic ledger, Maynard Proposition 6.1 ledger,
  H1 good-weight trace와 T1 66-node ledger에 연결했다.
- 현재 상태를 일관되게 `line-905 scalar subpackage=CLOSED`,
  `H1B-L84=RATE_MISSING`, `SIV-07=HARD_BLOCKER`, `X_cert=OPEN`으로 고정했다.
- 과거 2d/2d.1 당시의 scalar OPEN 문장은 역사적 snapshot임을 명시해 최신 판정과
  혼동되지 않게 했다.
- 관련 회귀시험 53개가 PASS했다.
- 첫 전체 suite는 sandbox의 임시 디렉터리 쓰기 거부로 301개 중 82개가
  `PermissionError`를 냈다. 이는 수학·코드 회귀 실패가 아니며, 동일 명령을 사용자
  허가 범위의 sandbox 외부에서 재실행해 `Ran 301 tests in 41.992s / OK`를 확인했다.
- 관련 Python 파일 `py_compile` PASS, theory JSON 16개 strict parse PASS,
  `git diff --check` exit 0이다. CRLF 안내만 있었고 whitespace 오류는 없었다.
- 추가 package 또는 Lean, actual prime sweep, threshold calculator는 실행하지 않았다.
- 다음 재개점: timestamp handoff를 새 파일로 작성하고 본 원장의 완료조건을 재확인한 뒤
  파일명을 `-done.md`로 변경한다.

### 2026-09-08 13:24 KST — 핸드오프·완료조건 확인

- `handoff/202609081324_HANDOFF.md`를 새 파일로 작성했다.
- 쉬운 결과 설명, 수학적 범위, source 정정, 검증 결과, 수행하지 않은 일, 다음 권장
  순서·예상시간·사용자 수행절차와 한국어 커밋 제안을 포함했다.
- 신규 6개 파일의 strict UTF-8, trailing whitespace, 핵심 내부 참조와 기존 변경의
  `git diff --check`를 다시 검증했다.
- 요청 산출물·정본·검증·handoff가 모두 완료됐으므로 본 원장을 `-done.md`로
  이름 변경할 수 있다.

## 완료 전 점검

- [x] 원문 식·변수·정규화 전수 복원
- [x] 선행연구 우선 조사와 실제 적용성 판정
- [x] 하위 상수·유효범위 또는 정확한 blocker 분리
- [x] 실제 데이터·threshold 미실행 경계 유지
- [x] 코드·JSON·정본·상위 DAG 동기화
- [x] 고정 FGKMT Python 표적·전체 검증
- [x] 오류·실패 원장 기록
- [x] 새 timestamp handoff
- [x] `git diff --check`·UTF-8·내부 참조 검사
- [x] 파일명을 `-done.md`로 변경
