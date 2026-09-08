# H1b-1b-2d Lemma 8.4 smooth norm·r-fold 합성 작업원장 — 완료

- 시작: 2026-09-08 07:52 KST
- 현재 상태: COMPLETED
- 사용자 승인: 최신 권장 1순위인 H1b-1b-2d 문헌 조사, 수학적 정식화, 보조 코드·toy/회귀검증, 정본·핸드오프 갱신
- 금지·보류: 실제 maximal-gap/prime sweep, 실제 theorem threshold 계산, 열린 상수를 임의 대입한 runner, 패키지 설치, Lean 설치·실행, commit/push/PR
- 선행 변경: 착수 시 `git status --short`는 빈 출력(clean). 진행 중인 다른 비 `-done` 작업원장은 없음.

## 목적과 완료조건

- 목적: Maynard Lemma 8.4의 실제 Section 8 사용에서 smooth test function norm과
  교정된 Lemma 8.3 one-step 오류의 (r)-회 누적을 수치적으로 명시할 수 있는지 감사한다.
- 완료조건:
  1. 원문에서 (G,G_1,G_2,\Omega_G,\varepsilon)과 반복식의 정확한 정규화를 고정한다.
  2. 같은 가정·norm·range를 제공하는 선행 lemma를 우선 조사하고 적용성을 개별 판정한다.
  3. 선행결과가 없는 연결부만 직접 증명하며, 닫히지 않는 입력은 정확한 blocker로 남긴다.
  4. 기계 판독 계약·보조 계산·회귀시험과 상위 H1b/T1 상태를 fail-closed 동기화한다.
  5. 전체 검증, 새 핸드오프, 한국어 커밋 메시지와 다음 권장 순서를 남긴다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | Lemma 8.4 한 단계 오류와 (r)-회 누적을 구분하고, 숨은 `O`·`o`를 1로 놓지 않는다. |
| 데이터·provenance | NONE | 실제 prime/maximal-gap 데이터와 `test_result/`를 읽거나 생성하지 않는다. |
| 통계·정밀도 | LOW | exact rational/symbolic 상계를 우선하고 `mpmath` 값은 진단으로만 쓴다. |
| 승인 경계 | HIGH | toy·정적 검증만 수행하며 actual threshold/prime 실험은 실행하지 않는다. |
| 문헌 적용성 | HIGH | 가정, 함수 norm, support, endpoint, 유효범위와 정정 여부를 호출별로 대조한다. |
| 상위 상태 | HIGH | (r)-fold와 공통 cutoff가 모두 닫히기 전에는 `SIV-07`, `X_cert`를 승격하지 않는다. |
| 산출물·비덮어쓰기 | MEDIUM | 새 theory/review/JSON/code/test/handoff를 만들고 기존 이력 문서를 덮어쓰지 않는다. |

## 단계 현황

1. **COMPLETED — Maynard Lemma 8.4 smooth 함수·반복식·actual call inventory 고정**
2. **COMPLETED — 선행연구의 explicit smooth norm·finite product/r-fold bound 적용성 조사**
3. **COMPLETED — 최소 직접 lemma 또는 남은 blocker 정식화**
4. **COMPLETED — 기계 계약·코드·시험과 상위 정본 동기화**
5. **COMPLETED — 표적·전체 검증, 보고, 새 handoff와 원장 완료 처리**

## 단계별 기록

### 2026-09-08 07:52 KST — 착수·승인 경계 고정

- 수행: 최신 handoff와 AGENTS의 첫 gate가 H1b-1b-2d임을 확인하고 clean worktree에서 원장을 생성했다.
- 방법 결정: lemma는 원 논문·교정본·후속 선행증명을 먼저 찾고 실제 함수·정규화에 맞는지 확인한다. 적합한 결과가 없을 때만 빠진 연결부를 직접 증명한다.
- 다음 재개점: `tmp/pdfs/h1b1b/maynard_source/Subsets.tex`의 Lemma 8.4와 실제 Section 8 호출에서 사용한 (G,\Phi,\Omega_G,r,R,k)을 행 단위로 inventory한다.

### 2026-09-08 08:20 KST — 원문 inventory·출판본 시각 대조 완료

- 원문: `Subsets.tex` 415--428행에서 \(F,F_1,F_2,T_k,U_k,\psi\)를, 531--604행에서
  Lemmas 8.3--8.4와 \(G_1,G_2,\Omega_G,\varepsilon\) 및 이항 반복식을 고정했다.
- 출판본: printed pp. 1533--1536을 렌더링·시각 확인했다. 출판 Lemma 8.3은
  `c_gamma(1+L)G_max` 보정 주석을 포함하며, Lemma 8.4는
  `(1+O(epsilon))^j-1=O(j epsilon)`만 주고 수치 smallness cutoff는 주지 않는다.
- 적용 분류:
  - `L620`: \(F=\psi(\sum t_i)\prod N(t_i)\)
  - `L752`, `L1135-canonical`: \(F^2=\psi(\sum t_i)^2\prod N(t_i)^2\)
  - `L737`, `L1232`: \(F_2^2\)의 \(k^2\)개 비음수 tensor 전개
  - `L885`: \(t_m=0\)인 \(F_2^2\)의 sliced tensor 전개
  - `L995`: 고정된 다른 좌표에서 \(F_2\)의 1변수 \(N/W\) 합
  - `L1015`: \(F\)의 1변수 weighted partial summation
  - `L1096`, `L1135-W0`: smooth 함수가 아니라 sharp one-variable cutoff이므로
    corrected summatory estimate를 직접 써야 한다.
  - `L905`: 앞선 `H=F+O(...)`의 함수형·도함수 norm이 고정되지 않은 채 제곱되므로
    현재 단계에서 유일하게 actual smooth package가 완결되지 않는 호출이다.
- 추가 원문 주의: 620행/printed p.1536의
  `k^2 T_k=o(log log R/log R)`는 Lemma 8.4 가정 및 바로 뒤 (8.20)과 reciprocal 방향이다.
  필요한 식은 `k^2 T_k log log R/log R=o(1)`, 즉
  `k^2 T_k=o(log R/log log R)`이다. 수식 (8.20)은 올바른 방향을 쓴다.

### 2026-09-08 08:35 KST — 문헌 우선 적용성 조사 완료

- 표적 검색에서 Maynard Lemma 8.4와 같은 actual Section 8 함수, corrected
  `c_gamma(L+1)` multiplier, 모든 수치 상수와 finite cutoff를 함께 주는 peer-reviewed
  후속정리는 찾지 못했다. 전 세계 부재라는 novelty 주장은 하지 않는다.
- Maynard 출판본은 구조와 정정 주석을 제공하지만 hidden `O/o`를 남긴다.
- Axiom Math의 2026 `PrimeGapsLib` blueprint/Lean source는 iterated partial summation을
  telescoping하는 독립 선례를 제공한다. 그러나 사용자 지정 미검증 source이고,
  상수 `C,C1,C2`가 존재형이며 full-profile norm과 대상 sieve datum도 달라 이번 numerical
  certificate의 theorem input으로 채택하지 않는다.
- Polymath/일반 Selberg sieve 결과는 smooth profile 또는 variational problem의 다른
  norm·가정을 사용하므로 Maynard Lemma 8.4의 actual corrected finite package로 대체하지 않는다.
- 결론: 선행 구조는 참고하되 빠진 연결부는 비음수·좌표별 support를 명시한 project lemma로
  최소 범위에서 직접 증명한다.

### 2026-09-08 08:38 KST — 보조 명령 오류 기록

- Windows PowerShell에서 `rg ... docs/method/theory/data/*.json`처럼 확장되지 않는 wildcard를
  다시 넘겨 경로 구문 오류가 났다. 이는 기존 오류 원장 E027과 같은 재발이며 연구 증거로
  사용하지 않았다. 후속 검색은 디렉터리와 `-g '*.json'` 형태만 사용한다.

## 현재 재개점

이번 원장은 완료됐다. 다음 작업은
`handoff/202609080908_HANDOFF.md`의 1순위 H1b-1b-2d.1a에서 시작한다.

### 2026-09-08 08:50 KST 기록 — project lemma·호출별 경계 정식화 완료

- 새 정본:
  - `docs/method/theory/24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md`
  - `docs/review/30_20260908_H1b1b2d_Lemma84_rfold_smooth_적용성검토.md`
  - `docs/method/theory/data/Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json`
- 직접 증명 범위:
  - support `[0,s_i]`를 `z=R^s_i`로 바꾸는 one-coordinate normalization
  - 서로 다른 비음수 profile의 exact product envelope
    `product(1+delta_i)-1`
  - actual `N,W,N2,W2,NW` integral lower/C1 upper
  - explicit smooth smallness sufficient cutoff
- 중요 교정:
  - `F2^2`의 `W2`는 `[0,2]` support라서 wide coordinate를 먼저 합해야 기존
    `Lambda_star`가 안전하다. 코드와 계약에 required ordering으로 고정했다.
  - coupled cutoff가 있는 경우 결과는 actual main integral에 대한 상대오차가 아니라
    product-profile integral 기준의 절대오차 envelope다.
  - Maynard source 620행의 reciprocal 방향 불일치를 기록하고 식 (8.20)과 Lemma 8.4
    가정에 맞는 `k^2 T_k loglogR/logR=o(1)`만 사용했다.
- 열린 범위:
  - Lemma 8.4 smooth actual call 7개는 하위 package로 닫힘
  - line 905의 opaque `H` function/C1 multiplier는 OPEN
  - sharp cutoff 2개는 공식만 parameterized; `xi log x` finite lower bound OPEN
  - parent `H1B-L84=RATE_MISSING`, `SIV-07=HARD_BLOCKER`, `X_cert=OPEN`
- 구현:
  - `source/h1b1b2d_rfold_smooth_package.py`
  - `tests/test_h1b1b2d_rfold_smooth_package.py`
- 중단 복구 중 발견한 생성 오타 `H1B1더보기B2C...`와 stray `+`를 정상 import로 교정했다.
- 표적 검증: 새 테스트 8개 PASS.
- 시각 주의: 이 항목에는 처음 `09:32 KST`라는 아직 오지 않은 시각을 잘못 적었다.
  시스템 시각과 08:56 전체시험 흔적을 대조해 `08:50 KST 사후 기록`으로 교정했다.

### 2026-09-08 09:11 KST — 정본 동기화·전체 검증·핸드오프 완료

- 상위 T1/H1b/H1b-1/H1b-1b-2c JSON·문서, METHODS, AGENTS, 이론 색인을
  `H1B-L84=RATE_MISSING`, `SIV-07=HARD_BLOCKER`, `X_cert=OPEN`으로 동기화했다.
- 문서 감사에서 상수 원장의 절 순서가 13→15→14로 뒤바뀐 것을 찾아 13→14→15로
  교정했다.
- 검증:
  - 신규 suite 8/8 PASS
  - 관련 suite 33/33 PASS
  - sandbox 밖 동일 전체 suite: `Ran 286 tests in 39.912s`, `OK`
  - theory JSON 14/14 엄격 파싱 PASS
  - 내부 참조 경로 6개 PASS
  - `git diff --check` exit 0, whitespace error 0
- sandbox 안 첫 전체 suite 82건 권한 오류, 잘못된 미래 시각, Windows 검색 명령 오류는
  오류 원장 E015/E020/E027에 기록했다. 실제 연구 결과 오염은 없었다.
- 새 핸드오프:
  `handoff/202609080908_HANDOFF.md`
- actual prime/maximal-gap 실험, threshold calculator, Lean·패키지 설치, commit/push/PR은
  수행하지 않았다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 문헌 우선 적용가능성 감사 완료
- [x] source locator·hash·변수 대응 고정
- [x] 닫힌 상수와 RATE/RANGE blocker 분리
- [x] actual 실험·threshold 미실행 경계 명시
- [x] 정본·상위 원장·AGENTS/METHODS 동기화
- [x] 고정 FGKMT Python 표적·전체 검증
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
