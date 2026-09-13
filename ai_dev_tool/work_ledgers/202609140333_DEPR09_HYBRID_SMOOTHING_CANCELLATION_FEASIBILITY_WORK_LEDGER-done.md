# DEP-R09 hybrid·smoothing·cancellation PAP transfer 타당성 작업원장

- 시작: 2026-09-14 03:33 KST
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 시작 commit: `a21c48970b40c317a2bdbd4931d75da6d98d749e`
- 선행 정본:
  - `docs/method/theory/72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md`
  - `docs/method/theory/73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md`
  - `docs/method/theory/74_Sono_FMT_DEPR09_modern_explicit_density_source_screen.md`
  - `docs/review/81_20260914_DEPR09_modern_explicit_density_source_screen_타당성검토.md`
  - `handoff/202609140323_HANDOFF.md`
- 승인 경계: source-first 문헌 조사, 정적 증명·수치 필요조건, 데이터 비의존 Python 시험,
  필요한 Lean 형식화, 정본·handoff·로컬 커밋은 승인됨. 장시간 actual prime 계산은
  시작하지 않으며, 특정 numerical `X_cert` 범위가 가능해지면 즉시 중단·보고한다.

## 목표

Theory 74가 배제하지 않은 세 가지 가능성—현재 Ramaré/Jutila 상계의 pointwise minimum,
비음수 smoothing, zero/character cancellation 보존—을 실제 Gallagher--Maier PAP 계약에
맞춰 작은 coefficient 필요조건으로 판정한다. 긴 analytic proof에 들어가기 전에 각 방법이
현재 (D\le186), error budget (e^{-2})를 원리상 통과할 여지가 있는지 확인한다.

## 비목적

- 모든 smoothing 또는 cancellation proof의 불가능성 정리
- source analytic theorem을 Lean local axiom으로 가정
- threshold calculator, maximal-gap dataset 변경, prime sweep 또는 장시간 실제 계산
- finite empirical threshold를 theorem-level `X_cert`로 승격

## 영향도 사전검토

| 축 | 판정 | 통제 |
|---|---|---|
| FGKMT 함수·end-bounded 데이터 | 영향 없음 | analytic PAP branch만 다루며 (G,F,H) 계산을 변경하지 않는다. |
| PAP 수학 구조 | 영향 큼 | absolute-value/zero-count 단계 전후를 구분하고, 허용되는 결론을 좁게 기록한다. |
| source provenance | 영향 큼 | 기존 local PDF를 우선 대조하고 추가 lemma는 primary source를 먼저 조사한다. |
| 수치 정밀도 | 영향 있음 | exact rational과 고정밀 진단을 분리하고, 실패 gate는 안전한 방향으로 증명한다. |
| Lean | 조건부 영향 | dependency-critical 유한 대수만 단일 파일에 추가하며 analytic premise는 미형식화한다. |
| actual 데이터·그래프 | 영향 없음 | `datas/`, `test_result/`, figure를 생성·수정하지 않는다. |
| 사용자 자원 | 영향 없음 예상 | 짧은 CPU 정적 계산만 Codex가 수행하며 장시간 필요 시 실행 전에 중단한다. |
| 정본·재현성 | 영향 있음 | successor theory/review/machine ledger/tests/Lean inventory/handoff를 동기화한다. |

## 비교할 실제 선택지

| 방법 | 기대 장점 | 핵심 위험 | 첫 판정 기준 |
|---|---|---|---|
| Ramaré–Jutila pointwise minimum | 이미 수치화된 두 상계를 그대로 결합 | zero-free edge 첫 slice에서 둘 다 예산보다 클 수 있음 | 첫 unit slice의 `min` certificate 하한 |
| 고정 비음수 smoothing | prime main term의 양성을 보존하기 쉬움 | β→1에서 정규화 Mellin weight가 1로 수렴해 큰 감쇠 불가 | 필요한 감쇠율 대 support-based 최저 전달율 |
| cancellation-preserving transfer | 현재의 거대한 absolute-value loss를 구조적으로 제거 가능 | zero count로 바꾼 뒤에는 위상 정보가 소실; 새 source theorem 필요 | absolute value 이전의 signed/complex sum 계약 존재 여부 |

현재 권장 순서는 위 표의 순서다. pointwise minimum과 비음수 smoothing이 수치적으로
탈락하면 cancellation route를 “현 증명의 보정”이 아니라 “새 analytic input이 필요한
별도 proof architecture”로 분류한다.

## 단계 현황

1. **DONE — 선행 정본·source statement·변수계약 재고정**
2. **DONE — hybrid minimum 첫-slice exact obstruction 계산**
3. **DONE — fixed nonnegative smoothing 감쇠 필요조건·source 조사**
4. **DONE — cancellation-preserving transfer의 정보손실·필요 theorem 계약 정식화**
5. **DONE — Python fail-closed 진단·시험과 Lean 필요성 판정/형식화**
6. **DONE — successor theory/review와 METHODS/T1/색인/AGENTS 동기화**
7. **DONE — 전체 검증·handoff·완료 이름·승인된 로컬 커밋 준비**

## 단계별 기록

### 2026-09-14 03:33 KST — 착수

- 직전 단계는 commit `a21c489`와 clean worktree로 완료되어 진척으로 판정했다.
- Theory 72의 PAP near integral, Theory 73의 tightened coefficient,
  Theory 74의 Ramaré direct-insertion 식을 다음 입력으로 고정했다.
- 첫 질문은 “더 큰 (X)를 계산할 것인가”가 아니라 “두 certified upper bound의 minimum이
  첫 zero-free-edge slice를 예산 아래로 만들 수 있는가”다.
- 실제 prime 계산, dataset 접근, 새 결과 디렉터리 생성은 하지 않았다.
- 다음 재개점: Theory 71의 pointwise density 식과 Theory 73의 tightened coefficient를
  같은 slice 변수 (y=(1-\alpha)\log X)로 옮겨 hybrid lower floor를 유도한다.

### 2026-09-14 04:08 KST — source 계약과 세 갈래 feasibility 판정

- 원문 재확인: Gallagher printed p.338 식 (30)은 prime-character 오차에 절댓값을
  취한 뒤 positive triple zero sum·Stieltjes count로 옮긴다. Maier printed pp.260--261은
  Lemma 2에서 `h=x`, `Q=x^(1/D)`를 택하므로 prime interval은 `[x,2x]`다.
  Ramaré Theorem 1.1은 Theory 74에 고정한 fully numerical averaged density다.
- PDF 판독: 세 local PDF는 native text layer로 위치를 찾고 이미 렌더한 exact statement
  페이지를 대조했다. OCR은 사용하지 않았다.
- source-first 조사: smooth explicit formula는 Mellin transform으로 zero term을 가중할 수
  있으나, 표준 upper-bound 단계가 절댓값 합으로 가면 cancellation은 다시 사라진다.
  이 구조 확인에는 Helfgott Chapter 9를 background로만 사용했고 현재 PAP의 새 analytic
  premise로 승격하지 않았다. elementary Mellin continuity·positivity 필요조건은 외부
  lemma를 새로 가져오는 것보다 직접 증명이 더 짧고 정확해 직접 유도했다.
- hybrid: `y=(1-alpha)log X`의 첫 unit slice에서 Ramaré main RHS와 tightened Jutila RHS의
  pointwise minimum certificate도 `21<=d<=186` 전체에서 8602.030894...보다 작아질 수 없다.
  최저점은 `d=186`, Ramaré source 최소 `log X=186 log 10`에서 발생한다. 이는 computed
  upper certificate의 하한이며 true error의 하한이 아니다.
- smoothing: budget `exp(-2)`에 맞추려면 0.00001573294549... 이하 감쇠가 필요하지만,
  zero-height 정보 없이 gamma-uniform 절댓값 envelope를 쓰는 `[1,2]` 고정 비음수
  정규화 weight는 zero frequency에서 `delta<=1/21`이면 적어도
  `2^(-1/21)=0.967531...`를 전달한다. 실제 첫 slice의 delta에서는 0.995881... 이상이다.
  support 감쇠만으로 목표를 맞추려면 각각 `log10 U>=100.866...`, actual slice에서는
  `>=806.711...`가 필요해 `[X,2X]` pointwise PAP를 보존하지 못한다.
- signed weight: `|K_w(delta)-1|<=delta log(2)||w||_1/|int w|`이므로 fixed weight는
  `delta->0`에서 1로 돌아간다. X-dependent signed minorant는 논리적으로 배제하지 않지만,
  condition number·main term·tail을 모두 새로 수치화해야 한다.
- cancellation: `N*(alpha,T,Q)` 단계에는 character phase와 residue-class sign이 남지 않는다.
  따라서 상쇄를 쓰려면 절댓값 이전의 signed/complex sum을 uniform하게 제어하는 새
  pointwise 또는 explicit moment theorem이 필요하다. 평균적·almost-all 정리는 현재
  Maier pointwise PAP 계약의 drop-in이 아니다.
- 판정: simple pointwise minimum과 source-blind gamma-uniform fixed nonnegative
  smoothing은 현 certificate에서 탈락한다. zero-height 분포를 새 정리로 이용하는 smoothing과
  모든 cancellation의 불가능성은 주장하지 않는다. numerical `X_cert` 범위와
  사용자 장시간 계산 필요는 아직 생기지 않았다.
- 다음 재개점: fail-closed module·machine ledger·시험을 고정하고 dependency-critical
  유한 대수만 Lean 단일 파일에 형식화한다.

### 2026-09-14 04:18 KST — Python·machine ledger 1차 검증

- 추가: `source/dep_r09_transfer_feasibility.py`,
  `tests/test_dep_r09_transfer_feasibility.py`,
  `docs/method/theory/data/Sono_FMT_DEPR09_transfer_feasibility_v1.json`.
- 진단 재현값: hybrid floor 8602.030894..., required attenuation
  1.57329454987e-5, actual first-slice delta 0.00595403725...,
  fixed `[1,2]` positive-weight lower 0.9958814803..., signed-weight necessary
  condition number 242.3015...다.
- 검증: FGKMT Python `py_compile` PASS, 표적 unittest 9/9 PASS.
- fail-closed 확인: `PAP-11`, DEP-R09, fixed coefficient, numerical `X_cert`,
  threshold calculator와 actual prime computation은 모두 false/OPEN이다.
- 다음 재개점: Lean에 endpoint·budget separation·조건부 Cauchy 대수를 추가하고 direct compile한다.

### 2026-09-14 04:31 KST — Lean 핵심 대수와 successor 초안

- Lean 단일 파일에 Theory 75의 `51/20`, finite endpoint, rational budget separation,
  pointwise min monotonicity와 explicit second-moment premise 아래 Cauchy terminal transfer를
  추가했다. analytic density·smooth explicit formula·complex moment theorem은 가정하지 않았다.
- 첫 direct compile에서 같은 양의 분모를 비교하는 lemma에 두 분모용
  `div_le_div_iff₀`를 잘못 적용해 1건 실패했다. 파일 line 3319를
  `div_le_div_iff_of_pos_right`로 교정했고, 이어 unused `ring` 경고도 제거했다.
  재실행은 exit 0·경고 0이다. 이 구현 오류는 commit 전 발견됐고 수학 판정·데이터에
  영향을 주지 않았다. 최종 오류 원장에 기록한다.
- 신규 Theory 75와 쉬운 review 82를 작성했다. smoothing 판정은 처음 초안의 넓은 표현을
  자체 점검해 `zero-height 정보가 없는 source-blind gamma-uniform absolute envelope`로
  좁혔다. oscillatory height-sensitive smoothing 전체를 배제하지 않는다.
- 다음 재개점: METHODS/T1/색인/AGENTS와 Lean status·notes·README를 Theory 75 상태로 동기화한다.

### 2026-09-14 재개 세션 — 정본 동기화·전체 회귀·표기 self-audit

- 동기화 완료: `docs/METHODS.md`, T1 proof-obligation ledger, theory/review 종합 색인,
  `AGENTS.md`, Lean README·status·notes·generated inventory를 Theory 75와 review 82로 맞췄다.
- self-audit에서 원래 zero-count RHS를 뜻하던 `U_R,U_J`를 변환된 Gallagher integrand처럼
  다시 쓴 표기 위험을 발견했다. `B_S(y)=e^{-y}U_S(1-y/log X)`를 별도로 정의하고,
  식 (75.9)가 두 **구간 전체 pointwise floor**의 minimum을 적분한다는 논리를 명시했다.
  일반적으로 거짓인 `integral(min)>=min(integrals)`를 사용하지 않는다. 수치값과 결론은
  바뀌지 않았고 machine ledger·함수 docstring·review도 같은 범위로 교정했다.
- FGKMT Python 신규 모듈 py_compile과 표적시험 9/9, Theory 73--75 결합 표적시험 27/27가
  PASS했다. 전체 unittest의 sandbox 실행은 Windows temporary-directory 접근 거부만으로
  `832 tests / 82 errors`였고, 사용자가 허가한 일반 권한에서 같은 명령을 재실행해
  `Ran 832 tests in 91.003s / OK`를 확인했다. 코드 assertion failure는 없었다.
- Lean 최종 검증: generator는 76문서·1,381식, validator는 270 declarations·로컬 링크
  1,460개·금지 proof escape 0건으로 PASS했다. `lake build`는 8,765 jobs PASS,
  단일 `TheoryVerification.lean` 직접 compile도 exit 0이다.
- 정밀 경계: 8602는 pointwise-minimum **upper-certificate**의 floor이지 true error의
  하한이 아니다. source-blind fixed nonnegative smoothing만 탈락했고 height-sensitive
  smoothing 전체는 미배제다. `PAP-11`, DEP-R09, fixed `2e-17`, numerical `X_cert`는 OPEN이다.
- 시간 메모: 재개 시 시스템 시각이 일부 선행 원장 항목보다 이르게 관측되어 이 단락에는
  분 단위 시각을 소급 기입하지 않았다. 단계 순서는 본문 배치와 검증 증거를 따른다.
- 다음 재개점: 변경·신규 파일 strict UTF-8/control/JSON/local-link/delimiter와 final diff를
  검사하고 새 timestamp handoff를 만든 뒤 원장을 `-done`으로 전환해 승인된 로컬 커밋을 한다.

### 2026-09-14 재개 세션 — 최종 정적검사와 handoff

- 새 handoff `handoff/202609140410_HANDOFF.md`를 비덮어쓰기로 작성했다.
- handoff 포함 변경·신규 text 20개에서 strict UTF-8, 금지 control 문자, trailing
  whitespace, JSON 3개, Markdown 13개 display delimiter와 local link 1,730개를 검사해
  issue 0이었다. `git diff --check`도 whitespace error 0이며 출력은 repository의 기존
  LF-to-CRLF 안내뿐이다.
- 사용자 설치·다운로드·actual 계산 요청은 없다. 별도 수행절차 필요없음.
- 다음 재개점: 이 원장을 안전하게 `-done` 이름으로 바꾸고 변경 파일만 staging하여
  cached diff를 재확인한 뒤 승인된 한국어 local commit을 생성한다.

## 완료 전 점검

- [x] source/page/equation과 publication status
- [x] actual PAP family·(Q,T,d,\theta,\eta) 변수변환
- [x] hybrid certificate와 true error의 논리 구분
- [x] smoothing의 positivity·normalization·support 가정 명시
- [x] cancellation 정보가 소실되는 정확한 proof edge
- [x] exact/high-precision 계산과 negative control
- [x] Lean proof와 analytic source premise 경계
- [x] 사용자 장시간 계산·설치 필요 여부
- [x] canonical 문서·검증·handoff·commit 준비
