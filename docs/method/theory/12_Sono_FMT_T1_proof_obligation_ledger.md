# Sono/FMT T1 numerical-threshold proof-obligation 원장

## 2026-09-10 H1b-COV2 현재 상태

> **2026-09-11 successor 경고:** 아래 `PAP-11`의 Sono 인쇄 상수는
> [Theory 57](57_Sono_FMT_DEPR09_Gallagher_Maier_McCurley_source_recovery.md)의 full-source
> 감사에서 현재 source chain으로 인증되지 않는 것으로 판정됐다. Proposition 5.3에서
> Gallagher `c1=3c_ZFR`로 가는 정규화와 hidden multiplier 소거가 열린 문제다.
> 이 문서의 coefficient 산술은 역사적 인쇄값 재현이다. 최신 analytic 판정은
> [Theory 66](66_Sono_FMT_DEPR09_Jutila_JL7_terminal_parameter_repair.md)을 우선하며,
> Theory 57의 source-chain 경고도 계속 유효하다. `PAP-11`, DEP-R09,
> \(X_{\rm cert}\)는 OPEN이다.

[theory 55](55_Sono_FMT_H1bCOV2_post_covering_interval_smooth_composition.md)와
[review 62](../../review/62_20260910_H1bCOV2_post_covering_구간_smooth_타당성검토.md)가 최신 정본이다.
equal-grid endpoint, \(m,A'\) floor, actual-width 예외복원, outer→inner 순차 성공사건과
special-case Rankin–Rosser–Schoenfeld smooth remainder를 유한식으로 닫았다.
R01–R08 actual child는 parameterized explicit이고 R09–R12는 OPEN이다.
COV-02/03/09는 EXPLICIT, broad COV-08/11은 PARTIAL, COV-12와
SIV-07/08/09·X_cert는 HARD_BLOCKER/OPEN이다. 다음은 DEP-R09 numerical PAP다.
최종 \(A,\varepsilon,\eta\)와 같은 Sono 계수의 공통 budget은 아직 정하지 않았다.
fixed-subset moment를 모든 subset의 동시 성공이나 사후 선택 보장으로 확대하지 않는다.
과거 원장·hash-pinned proof는 보존하며, 남은 4작업은 완료율이 아니다.
아래 날짜별 next-gate와 미완료 서술은 당시 이력이며 이 현재 상태가 우선한다.

- 작성: 2026-09-02 KST
- 단계: `T1_DIRECT_EDGE_INVENTORY_COMPLETE`
- 수학적 판정: `X_cert NUMERICALLY OPEN`
- machine-readable 정본:
  [`data/Sono_FMT_T1_proof_obligations_v1.json`](data/Sono_FMT_T1_proof_obligations_v1.json)
- 선행 1차 감사:
  [`../../review/22_20260902_Sono_FMT_numerical_threshold_proof_dependency_audit.md`](../../review/22_20260902_Sono_FMT_numerical_threshold_proof_dependency_audit.md)
- hard-node 현실성 판정:
  [`../../review/23_20260902_Sono_FMT_T1_hard_node_feasibility.md`](../../review/23_20260902_Sono_FMT_T1_hard_node_feasibility.md)
- H1 good-weight source tracing:
  [`../../review/24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md`](../../review/24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md)
- H1 machine trace:
  [`data/Sono_FMT_H1_good_sieve_weight_trace_v1.json`](data/Sono_FMT_H1_good_sieve_weight_trace_v1.json)
- H1b Maynard constant ledger:
  [`14_Sono_FMT_H1b_Maynard_Proposition_6_1_constant_ledger.md`](14_Sono_FMT_H1b_Maynard_Proposition_6_1_constant_ledger.md)
- H1b-2a Lemma 8.5·8.6 및 Proposition 9.4 잔여 package:
  [`28_Sono_FMT_H1b2a_residual_moment_error_package.md`](28_Sono_FMT_H1b2a_residual_moment_error_package.md)
- H1b-2a.2 actual distribution child와 H1b-2a.3 end-to-end 합성:
  [`30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md`](30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md),
  [`31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md`](31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md)
- H1b-1 basic summation 감사:
  [`15_Sono_FMT_H1b1_basic_summation_constant_audit.md`](15_Sono_FMT_H1b1_basic_summation_constant_audit.md)
- H1b-1b-2a actual-call local-factor·제외모듈 하한:
  [`20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md`](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
  및 [`21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md`](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)
- H1b-1b-2b 교정된 kappa=1 Wirsing multiplier:
  [`22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md`](22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md)
- H1c Hypothesis 1·PAP source trace:
  [`16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md`](16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md)
- H1c-1b.1a.1 sigma-y explicit cutoff:
  [`35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md`](35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md)

## 1. 결론

Sono의 (k=1) 정리를 numerical threshold로 바꾸는 직접 proof edge를 7개 층, 66개 obligation으로
등록했다. 현재 분류는 다음과 같다.

| 상태 | 행 수 | 뜻 |
|---|---:|---|
| `EXPLICIT` | 8 | 해당 행의 식·정의는 숫자 또는 exact algebra로 닫힘; COV-06 포함 |
| `PARTIAL` | 9 | 일부 상수·방향은 명시됐지만 유효범위 또는 다른 수치 입력이 빠짐 |
| `RATE_MISSING` | 30 | (o(1)), (O), (ll), `sufficiently large`의 숫자 rate가 없음 |
| `SOURCE_REVIEW_REQUIRED` | 4 | 인용된 하위 원문 정리를 더 깊게 감사해야 함 |
| `HARD_BLOCKER` | 15 | 현재 공개 서술만으로는 숫자 certificate가 닫히지 않음 |
| **합계** | **66** | |

따라서 이번 T1의 성과는 임계값 숫자를 얻은 것이 아니라, 그 숫자를 주장하려면 무엇을 먼저
수치화해야 하는지를 누락 점검 가능한 형태로 고정한 것이다.


\[
\boxed{
X_{\mathrm{emp}}(10^{20})=3{,}814{,}280\quad\text{(finite exact)},
\qquad X_{\mathrm{cert}}=\mathrm{OPEN},
\qquad X_\star=\mathrm{OPEN}.
}
\]

`EXPLICIT` 행도 의존하는 upstream 행이 열려 있으면 전체 증명이 닫힌 것이 아니다. 반대로
`HARD_BLOCKER`는 해당 정리가 틀렸다는 뜻이 아니라, 정량 재증명 또는 더 강한 explicit theorem이
필요하다는 뜻이다.

## 2. 목표와 범위

목표는 실제 숫자 (X_{\mathrm{cert}})를 찾아 다음을 증명할 수 있는지 판단하는 것이다.

\[
G_1(X)\ge 2\times10^{-17}
\frac{\log X\,\log_2X\,\log_4X}{\log_3X}
\qquad (X\ge X_{\mathrm{cert}}).
\]

이번 원장은 Sono Theorem 3.6에서 직접 사용하는 FMT, FGKMT, Maynard 층까지 추적한다. Gallagher,
Jutila, McCurley, Halberstam–Richert의 인용 정리 내부를 줄 단위로 재증명하지는 않았다. 그런 지점은
숨기지 않고 `SOURCE_REVIEW_REQUIRED` 또는 `HARD_BLOCKER`로 남겼다. 따라서 66개 행은 현재
abstraction에서의 direct-edge inventory이지 완성된 numerical proof certificate가 아니다.

이번 단계에서는 다음을 하지 않았다.

- 모르는 (O)-상수나 유효범위를 1 또는 0으로 가정
- numerical (X_{\mathrm{cert}}) 계산기 구현
- 새로운 prime 계산 또는 P018-B·P013-C·P019 actual 실행
- (X_{\mathrm{emp}})를 theorem threshold 또는 실제 전역 최소점으로 승격

## 3. 출처 고정

| key | 원문 | 감사 위치 | SHA-256 또는 provenance |
|---|---|---|---|
| `SONO2025` | Keiju Sono, *An Explicit Lower Bound...* | journal pp. 521–542 | `a45f84f5...c67302` |
| `FMT2018` | Ford–Maynard–Tao, *Chains of Large Gaps...* | pp. 2–16 | 감사 copy `396e54a9...1828f651828`; 정본 URL arXiv:1511.04468 |
| `FGKMT2016` | Ford–Green–Konyagin–Maynard–Tao, *Long Gaps...* | journal pp. 76–102 | `c31229ef...1d921ac8` |
| `MAYNARD2016` | James Maynard, *Dense Clusters of Primes in Subsets* | arXiv PDF pp. 3, 5–8, 19 | arXiv:1405.2593 |
| `MCCURLEY1984` | explicit zero-free region | Sono Section 5의 인용 | DOI 10.1016/0022-314X(84)90089-1 |
| `GALLAGHER1970` | large-sieve density estimate | Sono (5.2) | DOI 10.1007/BF01403187 |
| `JUTILA1977` | *On Linnik's Constant*, Vol. 41 (1977), 45–62 | Sono Section 5 | DOI 10.7146/math.scand.a-11701 |
| `HR1974` | *Sieve Methods*, Theorem 5.7 | Sono Theorem 4.1 | 원문 theorem constant 추가 감사 필요 |
| `ROSSER_SCHOENFELD1962` | *Approximate Formulas for Some Functions of Prime Numbers* | Theorem 7, p.70 | DOI 10.1215/ijm/1255631807; `8e37b06f...ac556` |

로컬 PDF의 본문 추출과 대표 페이지 렌더링을 함께 대조했다. 특히 Sono p. 541의 조건은 OCR
오독이 아니라 실제로 (1\ll80c/A\le1)이다. 여기서 (ll)은 숨은 양의 절대상수를 갖는
Vinogradov 표기이므로 논리적 모순은 아니지만 numerical threshold에는 그 숨은 상수가 필요하다.

## 4. dependency graph

```text
FIN-05: numerical X_cert
|
+-- FIN-01..04: k=1 boundary, coefficient, parameter substitution, rounding margin
+-- PAP-11: arithmetic-progression prime lower bound with a numeric x_PAP
|   +-- McCurley zero-free region
|   +-- Gallagher/Jutila density constants
|   +-- principal/nonprincipal terms and psi->pi
+-- UB-09: two-linear-form upper sieve with a numeric x_UB
|   +-- Halberstam-Richert error constant
|   +-- Mertens and singular-factor errors
+-- COV-12: numerical Proposition 3.1
|   +-- COV-11: all good events have finite total failure probability < 1
|   +-- SIV-11: numerical good-sieve-weight package
|       +-- Maynard finite-r integral and weight constants
|       +-- FGKMT Hypothesis 1 and error absorption
+-- AN-11/12: asymptotic-to-finite slack and final construction balance
+-- TRN-06: every X >= X_cert is covered without parameter gaps
    +-- explicit primorial and iterated-log conversion
    +-- integer rounding and end-bounded boundary
```

가장 중요한 점은 “최종 계수 계산”이 그래프의 시작에 가까운 작은 부분이라는 것이다. 계수 자체는
닫혔지만, 그 계수를 실제 특정 (X)부터 사용할 수 있게 하는 아래층의 rate가 열려 있다.

## 5. 최종 계수와 slack

Sono의 parameter를 대입한 명목 계수는

\[
\widehat c=2.00386120461967036975\ldots\times10^{-17}
\]

이고 논문이 주장하는 값은 (2.0\times10^{-17})이다. 두 값의 상대차는 약 `0.192688%`다.

이 값을 모든 (o(1))에 똑같이 나눠 주면 안 된다. Sono는 (3.21)–(3.23)에서 25, 20, 12800,
1800 같은 거친 상수로 이미 일부 slack을 사용한다. 따라서 다음 T2에서는 다음을 해야 한다.

1. 각 asymptotic 식의 원래 main term과 최종 coarse constant를 같은 방향으로 복원한다.
2. 이미 소비된 slack과 마지막 반올림 slack을 분리한다.
3. 곱셈 오차, 덧셈 오차, 확률 union bound를 서로 다른 예산으로 관리한다.
4. interval/rational arithmetic으로 최종 하한이 정확히 (2\times10^{-17}) 이상인지 독립 검증한다.

## 6. root critical path

| id | 닫혀야 할 명제 | 현재 판정 | 이유 |
|---|---|---|---|
| `PAP-11` | (C_{PAP}=1-e^{-2},D_{PAP}=160)이 시작되는 숫자 (x_{PAP}) | `HARD_BLOCKER` | density estimate의 implied constant와 (psi\to\pi) 유효범위 없음 |
| `UB-09` | (C_{UB}=8e^{2\gamma})가 시작되는 숫자 (x_{UB}) | `HARD_BLOCKER` | Halberstam–Richert error의 숫자 상수 없음 |
| `AN-11` | (3.17)–(3.20)의 asymptotic에서 (3.21)–(3.22)의 finite margin으로 이동 | `RATE_MISSING` | slack 소비량이 행 단위로 제시되지 않음 |
| `COV-11` | 모든 random good event의 finite sequential choice | `PARTIAL` | actual fixed family는 닫혔으나 COV-04/10과 최종 parameter budget은 남음 |
| `COV-12` | numerical Proposition 3.1 | `HARD_BLOCKER` | covering과 sieve package가 모두 미완성 |
| `SIV-11` | FMT Theorem 6을 숫자 (x_{sieve})부터 사용 | `HARD_BLOCKER` | (r_0,c_0,x^{-o(1)},u\asymp\log r), moment (O)-상수 미명시 |
| `TRN-06` | construction subsequence가 아니라 모든 (X\ge X_{cert})를 덮음 | `HARD_BLOCKER` | numerical parameter-selection rule과 rounding proof 없음 |
| `FIN-05` | numerical (X_{cert}) certificate | `HARD_BLOCKER` | 위 모든 의존성이 열림 |

## 7. 전체 66행 색인

각 행의 source/page/equation/direction/valid-range/dependencies/checker는 machine-readable 정본에
보존한다. 아래 표는 사람이 빠르게 탐색하기 위한 색인이다.

### 7.1 최종 계수·정리

| id | obligation | status |
|---|---|---|
| `FIN-01` | (k=1) end-bounded 경계 동일성 | `EXPLICIT` |
| `FIN-02` | Theorem 3.6 계수식 | `EXPLICIT` |
| `FIN-03` | 6개 parameter 대입 | `EXPLICIT` |
| `FIN-04` | 0.192688% 반올림 margin | `EXPLICIT` |
| `FIN-05` | 모든 (X\ge X_{cert}) numerical theorem | `HARD_BLOCKER` |

### 7.2 PAP

| id | obligation | status |
|---|---|---|
| `PAP-01` | Assumption PAP의 (1+o(1)) | `RATE_MISSING` |
| `PAP-02` | McCurley zero-free region | `PARTIAL` |
| `PAP-03` | Gallagher density estimate 상수 | `SOURCE_REVIEW_REQUIRED` |
| `PAP-04` | Jutila (c_{ZD}=16)과 implied constant | `PARTIAL` |
| `PAP-05` | (a=1/80,D_{PAP}=160) 선택 | `PARTIAL` |
| `PAP-06` | exceptional zero/prime case | `PARTIAL` |
| `PAP-07` | principal-character main term | `RATE_MISSING` |
| `PAP-08` | nonprincipal contribution | `HARD_BLOCKER` |
| `PAP-09` | (psi\to\pi) 변환 | `RATE_MISSING` |
| `PAP-10` | 모든 construction modulus에 uniform range | `PARTIAL` |
| `PAP-11` | numerical PAP package | `HARD_BLOCKER` |

### 7.3 UB

| id | obligation | status |
|---|---|---|
| `UB-01` | Assumption UB의 (1+o(1)) | `RATE_MISSING` |
| `UB-02` | Halberstam–Richert theorem 상수 | `SOURCE_REVIEW_REQUIRED` |
| `UB-03` | determinant (E)의 크기 | `RATE_MISSING` |
| `UB-04` | numerical upper-sieve error | `HARD_BLOCKER` |
| `UB-05` | Mertens local product | `RATE_MISSING` |
| `UB-06` | (B_0) local factor | `RATE_MISSING` |
| `UB-07` | (a-b) singular factor | `RATE_MISSING` |
| `UB-08` | (C_{UB}=8e^{2\gamma}) 추출 | `PARTIAL` |
| `UB-09` | numerical UB package | `HARD_BLOCKER` |

### 7.4 analytic combination

| id | obligation | status |
|---|---|---|
| `AN-01` | primorial asymptotic | `RATE_MISSING` |
| `AN-02` | Mertens product | `RATE_MISSING` |
| `AN-03` | discarded/small-prime term | `RATE_MISSING` |
| `AN-04` | single-prime lower count (3.11) | `RATE_MISSING` |
| `AN-05` | pair-prime upper count (3.12) | `RATE_MISSING` |
| `AN-06` | marginal probability (3.14) | `RATE_MISSING` |
| `AN-07` | pair probability (3.15) | `RATE_MISSING` |
| `AN-08` | first moment (3.17) | `RATE_MISSING` |
| `AN-09` | second moment (3.18) | `RATE_MISSING` |
| `AN-10` | positive good-event probability | `RATE_MISSING` |
| `AN-11` | finite margin (3.21)–(3.22) | `RATE_MISSING` |
| `AN-12` | parameter balance (3.23) | `PARTIAL` |

### 7.5 covering

| id | obligation | status |
|---|---|---|
| `COV-01` | Proposition 6.1의 (A'\sim c'A)·local count | `RATE_MISSING` |
| `COV-02` | endpoint-safe epsilon finite partition (theory55) | `EXPLICIT` |
| `COV-03` | actual smooth-number remainder (theory55) | `EXPLICIT` |
| `COV-04` | Proposition 6.2 cardinality/probability | `RATE_MISSING` |
| `COV-05` | covering density (C) | `RATE_MISSING` |
| `COV-06` | quantitative hypergraph theorem, C0=100 (theory54) | `EXPLICIT` |
| `COV-07` | FGKMT Corollary 3→FMT Theorem 4 | `PARTIAL` |
| `COV-08` | actual fixed-family finite success probability | `PARTIAL` |
| `COV-09` | (m,A') floor relation과 finite gate | `EXPLICIT` |
| `COV-10` | (epsilon_0) compatibility | `RATE_MISSING` |
| `COV-11` | sequential simultaneous good choices | `PARTIAL` |
| `COV-12` | numerical Proposition 3.1 | `HARD_BLOCKER` |

### 7.6 sieve weight

| id | obligation | status |
|---|---|---|
| `SIV-01` | finite (r_0), admissible (c_0) | `HARD_BLOCKER` |
| `SIV-02` | nonnegative good weight의 존재 | `HARD_BLOCKER` |
| `SIV-03` | \(\sigma y\) Mertens upper gate | `EXPLICIT` (`x>=2*exp(36^5)`) |
| `SIV-04` | \(\tau\ge x^{-o(1)}\) | `RATE_MISSING` |
| `SIV-05` | \(u\asymp\log r\) | `RATE_MISSING` |
| `SIV-06` | Maynard (J_r/I_r) finite-r bound | `EXPLICIT` (`r>=36`, project H1a) |
| `SIV-07` | Maynard Proposition 6.1 constants | `HARD_BLOCKER` |
| `SIV-08` | FGKMT Hypothesis 1 constants | `HARD_BLOCKER` |
| `SIV-09` | FMT weight moment formulas | `HARD_BLOCKER` |
| `SIV-10` | secondary-error absorption | `RATE_MISSING` |
| `SIV-11` | numerical Theorem 6 package | `HARD_BLOCKER` |

### 7.7 (x\to X)

| id | obligation | status |
|---|---|---|
| `TRN-01` | explicit primorial bound | `SOURCE_REVIEW_REQUIRED` |
| `TRN-02` | exact endpoint (2P^{M+1}) | `EXPLICIT` |
| `TRN-03` | (2P^{M+1}\le e^{1.5Mx}) | `RATE_MISSING` |
| `TRN-04` | iterated-log scale conversion | `RATE_MISSING` |
| `TRN-05` | rounding·monotonicity·end boundary | `SOURCE_REVIEW_REQUIRED` |
| `TRN-06` | arbitrary-(X) coverage | `HARD_BLOCKER` |

## 8. T1 completion gate 판정

| gate | 결과 |
|---|---|
| direct proof edge에 source key가 있는가 | 66/66 PASS |
| dependency id가 모두 존재하는가 | PASS |
| dependency graph가 acyclic인가 | PASS |
| open root를 `EXPLICIT`으로 잘못 표시했는가 | 0건 |
| 로컬 Sono·FGKMT PDF hash가 고정값과 일치하는가 | PASS |
| numerical (X_{cert})가 도출됐는가 | 아니오; 의도된 `OPEN` 판정 |
| threshold calculator 착수 gate | FAIL-CLOSED |

이 결과는 `T1_DIRECT_EDGE_INVENTORY_COMPLETE`이면서 동시에
`NUMERICAL_THRESHOLD_NOT_READY`다. 두 판정은 모순이 아니다.

## 9. H1/H1a/H1b 후속 판정과 다음 gate

2026-09-02 H1은 Sono pp. 541–542, FMT Theorem 6, FGKMT Theorems 5–6·Lemma 7.2,
Maynard Proposition 6.1·(8.25)–(8.27)·Sections 8–9를 source level로 추적했다.

| 질문 | H1 판정 |
|---|---|
| finite (J_r/I_r) lower bound | `PROJECT_FINITE_LEMMA_PROVED`; 모든 정수 (r\ge36) |
| finite (r_0)과 공통 시작 (x) | upstream moment·Hypothesis 1에 `DEPENDENCY_BLOCKED` |
| Proposition 6.1 상수 | `QUANTITATIVE_REPROOF_REQUIRED` |
| FGKMT Hypothesis 1 상수 | `QUANTITATIVE_REPROOF_REQUIRED` |
| numerical Theorem 6 package | `DEPENDENCY_BLOCKED` |

2026-09-04 H1a는 Maynard의 unrestricted product core와 Sono가 요구하는 simplex-supported
함수를 구분하고, exact envelope와 Cantelli concentration으로

\[
\frac{J_r(F)}{I_r(F)}>\frac{\log r}{4r}\qquad(r\ge36, r\in\mathbb Z)
\]

를 증명했다. (36\le r\le8103)은 60-dps directed interval로 전수 확인했고,
(\log r\ge9), 즉 정수 (r\ge8104)는 해석적 꼬리로 닫았다. 상세 정본은
[`13_Sono_FMT_H1a_finite_r_integral_lemma.md`](13_Sono_FMT_H1a_finite_r_integral_lemma.md)다.

이는 `SIV-06` 하나만 닫는다. Sono가 (c_0=1/5)을 인쇄했지만 finite (r_0)과 그 선택이 모든
uniformity·absorption 조건과 동시에 맞는 공통 시작점은 여전히 주어지지 않는다. Maynard는
effectivity를 명시하므로 나머지 constructive path는 원칙상 존재하지만 ready-made numerical
package는 아니다. 따라서 H1 전체 판정은
`CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED`이며
(X_{\mathrm{cert}})는 계속 `OPEN`이다.

2026-09-04 H1b는 Proposition 6.1, Hypothesis 1, Lemmas 8.1–8.6과 Propositions 9.1–9.5를
17개 constant obligation으로 등록했다. 인쇄된 parameter 범위와 decay exponent는 확인했지만,
multiplier·finite cutoff·Hypothesis 1 입력과 공통 error budget은 제공되지 않는다. 따라서
`SIV-07`과 `SIV-09`의 상태와 이 문서의 66행 상태 수는 바뀌지 않는다. H1b 완료는
`CONSTANT_DEPENDENCY_LEDGER_COMPLETE_NUMERICAL_PACKAGE_OPEN`을 뜻한다.

같은 날 H1b-1은 Lemmas 8.1–8.4의 13개 하위 node를 감사했다. Lemma 8.3이 인용하는 source는
GGPY의 *Small Gaps Between Products of Two Primes*, Lemma 4의 \(\kappa=1\) 특수화다. source
identity가 닫혔으므로 당시 parent `H1B-L83`은 `SOURCE_REVIEW_REQUIRED`에서
`RATE_MISSING`으로 정정됐다. 이 2026-09-04 이력은 2026-09-08 H1b-1b-2b의
`PARAMETERIZED_EXPLICIT_INPUTS_OPEN` 판정으로 한 번 대체됐고, 다시 H1b-1b-2c의
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` 판정으로 후속 대체됐다.

H1c는 FGKMT Hypothesis 1과 Sono PAP를 별도 source chain으로 분리했다. Hypothesis 1(1),(3)은
\(\mathcal A=\mathbb Z\)일 때 exact sufficient inequality로 줄일 수 있지만, condition (2)의
character/Bombieri–Vinogradov package는 열려 있다. PAP도 \(C_{PAP}=1-e^{-2}\),
\(D_{PAP}=160\)은 explicit하지만 principal/nonprincipal rate와 \(\psi\to\pi\) cutoff가 없다.
두 명제는 analytic input을 공유하는 sibling이며 서로를 함의하지 않는다. 따라서 T1 JSON에서
`SIV-08`의 잘못된 `depends_on: [PAP-11]` edge를 제거했다. 이 graph 정정은 `SIV-08`, `PAP-11`,
hard-blocker 수 또는 \(X_{\mathrm{cert}}\)의 상태를 올리지 않는다.

아래 목록은 theory 26 직후의 역사적 권장 순서이며, 이 중 2번은 section 17에서 완료됐다.

1. **완료:** H1b-1b-2b/c가 corrected one-step multiplier와 실제
   \(a=1/2,A_2=8,L=5+\log\Lambda_*\)을 인증했다. H1b-1b-2d는
   7개 direct smooth call을, 2d.1a/1a.1은 line-905 square-sum과 scalar
   multiplier를 닫아 smooth Lemma 8.4 하위호출 8/9를 explicit으로 만들었다.
2. **완료:** `H1b-1b-2d.1b`가 두 sharp call의 \(\xi\log x\) finite lower bound를 복원했다.
3. 병렬 이론축 `H1c-1`에서 FGKMT (7.2)–(7.3)의 quantitative
   character/Bombieri–Vinogradov package를 복원한다.
4. **부분 완료:** `H1b-2a`가 Lemma 8.5 finite weight envelope와 Lemma 8.6 absolute
   size·coarse comparison을 닫았고, `H1b-2a.1`이 Proposition 9.4 식 (9.66)의 exact
   Euler normalization을 닫았다. 현재 직접 축은 식 (9.52)의 distribution error다.
5. H1b-2 뒤 `SIV-05`, `SIV-09`, `SIV-10`, `SIV-11`의 합성 slack을 닫는다.
6. H1 계열이 numeric하게 닫힌 뒤 `COV-06`–`COV-11`의 finite failure-probability ledger로 간다.
7. PAP·UB·covering·transfer hard node가 모두 닫힌 뒤에만 T2와 threshold calculator를 구현한다.

현재 사용자 PC에 계산을 요청할 단계는 아니다. 병목은 연산시간이 아니라 논문 속 숨은 상수와
유효범위를 수학적으로 복원하는 일이다.

## 10. 검증

고정 FGKMT Python으로 다음을 검증한다.

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest `
  tests.test_threshold_proof_obligation_ledger `
  tests.test_h1_good_sieve_weight_trace `
  tests.test_h1b_maynard_constant_ledger `
  tests.test_h1b1_basic_summation_ledger `
  tests.test_h1c_hypothesis1_pap_trace -v
```

검증기는 66행 T1 schema·DAG·source hash, 9행 H1 source trace, 17행 H1b, 13행 H1b-1과
20행 H1c ledger의 fail-closed 상태를 확인한다.

## 11. 2026-09-07 actual local-factor·application 제외모듈 하한 반영

H1b-1b-2a는 Maynard Section 8의 실제 호출식에서 비제외 prime-local factor가 1 이상임을
증명하고, 유효 제외 소수의 손실을 \(\varphi(Q_j)/Q_j\)로 합쳤다. 이어진
H1b-1b-2a.1은 실제 호출의 \(dW_i,W_i',a_mWBr,rW_m,W_0\)를 11개 analytic
subapplication으로 전수 고정하고 공통 \(\log Q_j\le\Lambda_*\)를 증명했다. 따라서
Rosser--Schoenfeld 변환

\[
c_{\gamma,j}>\frac{1}{3(1+\log\Lambda_*)}
\]

은 추적된 actual call 전체에 대해 project-parameterized explicit이며 lower-bound
repair 경로가 선택됐다. 다만 이 단계 당시에는
\(C_{3,\mathrm{abs}}\), 실제 \(A_1,A_2,L\), 공통 finite range와 \(r\)-회 합성이
없었으므로 T1의 66행 상태 수, `SIV-07`, \(X_{\mathrm{cert}}\)는 바뀌지 않았다.

## 12. 2026-09-08 Ford 교정 Wirsing 경로 반영

Ford Theorem 4.4는 GGPY/Maynard 계열의 기존 증명에서 빠진
\(c_\gamma(L+1)^\kappa\) 항을 보존한다. H1b-1b-2b는 이 구조를
\(\kappa=1\)에 한정해 다시 전개하여, Maynard Lemma 8.3의 한 단계 오류를

\[
C_{8.3}(a,A_2)c_\gamma(L+1)G_{\max}
\]

형태로 모든 \(z\ge2\)에서 명시했다. 이 때문에 `H1B-L83`은 당시
`PARAMETERIZED_EXPLICIT_INPUTS_OPEN`으로 세분화됐다. 그러나 당시 실제 호출 전체에 공통인
\(a,A_2,L\), smooth norm, Lemma 8.4의 \(r\)-회 합성과 다른 moment/Hypothesis 1
상수가 없으므로 T1의 66행 상태 수, `SIV-07`, `SIV-09`,
\(X_{\mathrm{cert}}\)는 그대로다. 기존 \(c_\gamma\) 하한은 버리지 않고
독립 교차검사용 보조 경로로 보존한다.

## 13. 2026-09-08 actual \(a,A_2,L\) 특수화 반영

H1b-1b-2c는 Maynard Section 8의 네 actual denominator family와 11개 application에
공통인

\[
a=\frac12,\qquad A_2=8,\qquad L=5+\log\Lambda_*
\]

을 인증했다. 따라서 child `H1B-L83`은
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 진전한다. 그러나 corrected Lemma 8.4의
smooth norm·\(r\)-회 합성, 다른 moment 상수, H1c/PAP와 arbitrary-X 전달은 남아 있다.
그러므로 T1의 66행 root 상태 수, `SIV-07`, `SIV-09`,
\(X_{\mathrm{cert}}\)는 바뀌지 않는다.

## 14. 2026-09-08 support-scaled smooth \(r\)-fold 합성 반영

H1b-1b-2d는 actual \(N,W,N^2,W^2,NW\) profile을 support 길이에 맞게 rescale하고,
교정된 one-step 오차를

\[
\prod_i(1+\delta_i)-1,\qquad
\delta_i=
\frac{C_{8.3}(1/2,8)(L_i+1)\kappa_i}{\log R}
\]

로 정확히 합성했다. 9개 Lemma 8.4 subapplication 중 7개 smooth call은
project-parameterized explicit 하위 package로 닫혔다. \(F_2^2\)의 support-\([0,2]\)
\(W^2\) 좌표를 먼저 합한다는 순서 조건도 고정해 기존 \(\Lambda_*\)를 보존했다.

후속 H1b-1b-2d.1a는 905행의 전역 \(H\) remainder 함수·도함수가 필요 없음을
square-sum 부등식과 일곱 smooth tensor class로 닫았다. 이 단락은 2d.1a 직후의 당시
상태이며, 격자점별 scalar remainder multiplier는 section 16의 2d.1a.1에서 닫혔다.
두 sharp call의 \(\xi\log x\) finite lower bound는 계속 열려 있다. 따라서 parent `H1B-L84`는
`RATE_MISSING`, `SIV-07`은 `HARD_BLOCKER`, \(X_{\mathrm{cert}}\)는 `OPEN`을 유지한다.
T1의 66행 root 상태 수도 바뀌지 않는다.

## 15. 2026-09-08 line-905 \(H\) square-sum 우회 반영

H1b-1b-2d.1a는 \(A=\int Fdt_m\), \(B=\int F_2dt_m\)와
\(|Z-A|\le\varepsilon B\)에서

\[
|Z^2-A^2|\le2\varepsilon AB+\varepsilon^2B^2
\]

를 사용한다. \(A^2,AB,B^2\)는 N2, NW, W2의 일곱 비음수 smooth tensor
symmetry class로 정확히 전개되므로, 원문이 구성하지 않은 전역 \(H\)의 \(C^1\)
norm은 더 이상 905행 제곱합의 필수 의무가 아니다.

다만 원문 986--999행의 s-Euler product, t-divisor sum과 prefactor에는 수치화되지 않은
\(\ll\) multiplier가 남는다. conditional 계산기에 임의의 \(\varepsilon\)을 넣는 것은
source certificate가 아니다. 따라서 `H1B-L84=RATE_MISSING`,
`SIV-07=HARD_BLOCKER`, \(X_{\mathrm{cert}}=\)`OPEN`과 T1의 66행 상태
수는 그대로다.

## 16. 2026-09-08 scalar remainder finite component 반영

H1b-1b-2d.1a.1은 Maynard 최종 출판본 (9.42)--(9.48)을 기준으로 source scalar
remainder를 수치 재증명했다. \(s\)-Euler product, \(t\)-divisor 합, determinant,
\(\varphi_L\) prefactor와 direct branch를 분리해

\[
C_Y=327680\frac{14801}{69}e^{264}+10,143,697
<3.17\times10^{122}
\]

와 parameterized finite gate를 얻었다. theory 25의 square-sum 우회와 결합하면
line-905 scalar/smooth 하위 package는 닫히며 smooth Lemma 8.4 하위호출은 8/9 explicit이다.
구 author TeX와 달리 최종 출판본 식 (9.43)이 \(i\ne m\)을 사용한다는 source 정정도
반영했다.

남은 Lemma 8.4 blocker는 두 sharp call의 \(\xi\log x\) finite lower bound다.
따라서 parent `H1B-L84=RATE_MISSING`, `SIV-07=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`과 T1의 66행 root 상태 수는 유지한다.

## 17. 2026-09-08 sharp scale 후속 반영

위 마지막 문장은 theory 26 직후의 당시 상태다. theory 27은 FGKMT/FMT 실제
\(\xi=\theta/10\), \(R\le x^{\theta/3}\)을 이용해
\(\xi\log x\ge(3/10)\log R\)를 얻고, strict endpoint를 포함한
\(C_\Sigma+2\) multiplier로 두 sharp factor를 finite하게 닫았다.

따라서 `H1B-L84`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 이동한다.
그러나 T1의 `SIV-07` 행은 Maynard Proposition 6.1 **전체**를 가리키므로
`HARD_BLOCKER` 그대로다. 66행의 top-level 상태 수도 바뀌지 않으며
\(X_{\mathrm{cert}}\)도 계속 `OPEN`이다. 다음 직접 축은 H1b-2의 잔여
moment/error 감사와 H1c-1의 quantitative character/Bombieri--Vinogradov package다.

## 18. 2026-09-08 H1b-2a 잔여 moment/error 반영

theory 28은 actual cutoff의 plateau cube를 사용해 모든 정수 (k\ge36)에서

\[
I_k(F)\ge(2k\log k)^{-k},\qquad
J_k(F)>\frac{\log k}{4k}(2k\log k)^{-k}
\]

를 finite하게 닫고, (F_1/F_2)에는 (2^k,C_J(k))라는 안전한 explicit
comparison multiplier를 주었다. actual `L620_dW` 오차와 elementary support count를
결합해 Lemma 8.5의 coefficient, local weight, (R^{2+\eta_{85}(k,R)}) 상계도 닫았다.

따라서 H1b 하위행 `H1B-L85`와 `H1B-L86-SIZE`는 각각
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`, `PROJECT_FINITE_COMPONENT_CLOSED`로 이동한다.
Proposition 9.4에서는 square algebra, denominator (\le2/p), 식 (9.64)의 앞쪽 Euler 곱
(\le e^{2/k})을 닫았다. 이 단락 작성 당시 식 (9.52)의 distribution error와 식 (9.66)의
마지막 두 Euler normalization이 열려 있었으나, 아래 Section 19에서 Euler 항은 닫힌다.

T1의 `SIV-07`은 Proposition 6.1 전체 행이므로 계속 `HARD_BLOCKER`이고, 66행 상태 수와
(X_{\mathrm{cert}})=`OPEN`도 변하지 않는다. 다음 직접 축은 H1b-2a.2 distribution
error와 H1c-1의 quantitative character package다.

## 19. 2026-09-08 H1b-2a.1 exact Euler normalization 반영

H1b-2a.1은 Maynard Proposition 9.4 식 (9.61)의 exact denominator에서 식 (9.66)의
두 Euler 곱을 복원했다. \(p>2k^2\)에서 local excess를 각각
\(4k/p^2\), \(4k^2/p^2\)로 지배해 마지막 두 곱을
\(e^{2+2/k}\mathfrak S_{WB}(\mathcal L)^{-1}\) 이하로 닫았다. 식 (9.64)의
앞쪽 multiplier가 제곱합에 두 번 들어가는 것까지 포함하면 전체는
\(e^{2+6/k}\mathfrak S_{WB}(\mathcal L)^{-1}\) 이하이다.

이로써 `H1B2A-P94-FINAL-EULER`만 `PROJECT_FINITE_COMPONENT_CLOSED`로 이동한다.
식 (9.52)의 distribution error, 다른 moment와의 공통 cutoff·error budget은 남아
`SIV-07=HARD_BLOCKER`, T1의 66행 상태 수와 \(X_{\mathrm{cert}}=\)`OPEN`은
변하지 않는다. 다음 직접 gate는 H1b-2a.2이며 H1c-1이 병렬 선결축이다.

## 20. 2026-09-08 H1b-2a.2 actual distribution child 반영

앞 절 마지막 두 문장은 H1b-2a.1 직후의 역사적 상태다. 후속
[`H1b-2a.2 정본`](30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md)은 일반
집합 \(\mathcal A\)와 실제 FGKMT/FMT 호출을 분리했다. 실제
\(\mathcal A=\mathbb Z,D=1\)에서는 연속 정수 interval의 residue discrepancy가 모든
modulus에 대해 정확히 1 이하이다. 이를 multiplier 1의
\(\tau_{3(k+1)}(q)\) tuple 상계 및 기존 finite weight envelope와 결합해 식 (9.52)의
distribution child를 `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`으로 닫았다.

이 진전은 T1의 66개 상위 행을 분할하거나 상태 수를 바꾸지 않는다. `SIV-07`은 Proposition
6.1 전체를 나타내므로 계속 `HARD_BLOCKER`이고, `SIV-08/09`와
\(X_{\mathrm{cert}}\)도 변하지 않는다. 다음 직접 gate는 H1b-2a.3의 P94 단일
multiplier·공통 cutoff 합성이다. H1c-1은 actual 식 (9.52)의 선결조건이 아니라
Proposition 9.2와 전체 good-weight theorem에 필요한 병렬 축이다.

## 21. 2026-09-08 H1b-2a.3 actual P94 부모 반영

20절은 H1b-2a.2 직후의 역사적 상태다. 후속
[`H1b-2a.3 정본`](31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md)은 actual
FGKMT/FMT Proposition 9.4의 닫힌 하위 package를 하나의 finite cutoff와 multiplier로
합성했다. \(2^k\) product-envelope 손실을 강화 smooth gate로 흡수한 뒤 모든 정수
\(k\ge36\)에서 multiplier 13 미만을 얻었으므로 H1b 하위행 `H1B-P94`는
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다.

T1의 `SIV-07`은 Proposition 6.1 전체를 나타내므로 상태는 `HARD_BLOCKER` 그대로다.
따라서 66개 root 행의 상태 수, `SIV-08/09`, \(X_{\mathrm{cert}}\)=`OPEN`도 변하지
않는다. 다음 root-critical 작업은 Proposition 9.2에 필요한 H1c-1 quantitative
character/prime-distribution package이며, 이후 P91/P92/L93/P95와 공통 moment budget을
합성해야 한다.

## 22. 2026-09-09 H1c-1a source inventory 반영

H1c-1a는 `SIV-08`의 실제 Maynard/FGKMT 호출 계약과 12개 bridge/composition 의무를 고정했다.
explicit 선행연구 중 즉시 대입 가능한 정리는 없고 Bordignon 2021을 주 합성 후보로 선택했다.
이는 source 선택 진전이지 theorem closure가 아니다. 기계 원장의 `SIV-08` notes와 H1/H1b
successor pointer를 동기화했으며 66개 root row의 상태 수는 바꾸지 않았다.

따라서 `SIV-08=HARD_BLOCKER`, `SIV-07/09=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`이다. 다음 root-critical gate는 H1c-1b의 parameter/modulus
envelope와 한 exceptional \(B\), exact transfer와 common cutoff 합성이다.

## 23. 2026-09-09 H1c-1b.1 parameter·modulus 감사 반영

H1c-1b.1은 outer chain parameter \(k_{\mathrm{chain}}=1\), Sono/FMT의 growing sieve
dimension \(r_s\), Maynard linear-form count \(k=r\)을 분리했다. 따라서 Hypothesis 1(2)의
필요 지수는 고정 100이 아니라 \(100r^2\)이다. Bordignon Theorem 1.4에
\(A(r)=100r^2+10\)을 점별 대입할 수 있고, endpoint-safe \(r\ge36\)에서 actual
Proposition 9.2 identity-form modulus capacity는 project finite lemma로 닫혔다.

동시에 FGKMT 식 (6.5)가 Theorem 6을 \(x/2\)에서 호출한다는 사실 때문에,
\(r_s=\lfloor(\log x)^{1/5}\rfloor\)를 그대로 쓰면 반복되는 transition strip에서
인쇄된 \(k\le(\log(x/2))^{1/5}\) 조건을 만족하지 않는다는 경계 문제를 발견했다.
\(r_s-1\) 또는 \(r_T=\lfloor(\log(x/2))^{1/5}\rfloor\)가 항상 안전하다는 초등 보정은
닫혔지만, 이 보정이 actual weight normalization과 Sono의 최종 coefficient를 보존하는지는
열려 있다.

따라서 66개 root row의 상태 수는 바뀌지 않는다.
`SIV-07/08/09=HARD_BLOCKER`, \(X_{\mathrm{cert}}\)=`OPEN`이며 다음 gate는
H1c-1b.1a의 dyadic dimension-to-coefficient transfer다.

## 24. 2026-09-09 H1c-1b.1a dyadic coefficient transfer 반영

23절은 H1c-1b.1 직후의 역사적 상태다. 후속
[H1c-1b.1a 정본](34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md)은
actual endpoint에 맞춰

\[
r_T=\left\lfloor(\log(x/2))^{1/5}\right\rfloor
\]

를 사용한다. 기존 H1a의 \(J_r/I_r>\log r/(4r)\), FGKMT의 정확한
\(R=(x/4)^{\theta/3}\), Sono의 \(160\) 대 \(150\) slack을 합성해 모든
\(r_T\ge36\)에서 dimension·\(R\) normalization factor가 \(39/40\)보다 큼을
exact하게 증명했다. 따라서

\[
\sigma y\le\frac{26}{25}\,80cx\log_2x
\]

이면 \(C>(5/4)\log5\)이고, dimension repair는 Sono의 asymptotic
\(2\times10^{-17}\) 계수를 낮추지 않는다.

기계 원장의 `SIV-03`에는 \(\sigma y\) main term 뒤에 잘못 붙어 있던
`/log x`도 제거했다. 그 factor는 \(\sigma y\)가 아니라 survivor count
\(\sigma y/\log x\)에 속한다.

다만 \(26/25\) upper gate의 explicit cutoff는 아직 없으므로 `SIV-03` 상태는
`PARTIAL`, `SIV-05`의 전체 two-sided 상태는 `RATE_MISSING`으로 유지한다.
66개 root row의 상태 수, `SIV-07/08/09=HARD_BLOCKER`과
\(X_{\mathrm{cert}}\)=`OPEN`도 변하지 않는다. 다음 직접 gate는
H1c-1b.1a.1의 explicit Mertens \(\sigma y\) cutoff이고, 이후 H1c-1b.2의
한 common exceptional \(B\)로 진행한다.

## 25. 2026-09-09 H1c-1b.1a.1 sigma-y cutoff 반영

24절은 H1c-1b.1a 직후의 역사적 상태다. 후속
[H1c-1b.1a.1 정본](35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md)은 FMT의 exact
prime interval을 \(P(z)/P((\log x)^{20})\)로 다시 쓰고, 구간 안에서 제외되는 prime
\(B_0\)의 최악 factor도 포함했다. Rosser--Schoenfeld 1962 Theorem 7을 적용하면

\[
x\ge2\exp(36^5)
\quad\Longrightarrow\quad
\sigma y<\frac{1001000}{998001}\,80cx\log_2x
<\frac{26}{25}\,80cx\log_2x.
\]

따라서 `SIV-03`은 `PARTIAL`에서 `EXPLICIT`로 승격됐다. 66개 root row의 당시 상태 수는
`EXPLICIT 7`, `PARTIAL 9`, `RATE_MISSING 30`, `SOURCE_REVIEW_REQUIRED 4`,
`HARD_BLOCKER 16`이었다. 이후 COV1a의 COV-06 승격은 맨 위 현재 상태와 §1 집계를 따른다.

이 승격은 one-sided sigma-y application만 닫는다. general \(\varphi(P)/P\)의 `AN-02`와
reciprocal-square product의 `UB-05`는 실제 방향·합성 감사를 기다리므로 각각
`RATE_MISSING`으로 유지한다. 분포정리 전체의 common exceptional \(B\), Bordignon remainder,
count transfer와 density도 열려 있어 `SIV-07/08=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`은 변하지 않는다. 다음 gate는 H1c-1b.2다.

## 26. 2026-09-09 H1c-1b.2 common exceptional B·raw psi 합성 반영

H1c-1b.2는 actual Proposition 9.2 identity-form 호출의 fixed outer scale에서
\(Q_1=(\log T)^A\)를 \(T\), \(2T\) 양쪽에 공통으로 썼다. 이때 Bordignon의
exceptional modulus \(q_0\)도 하나이고, 그 prime divisor \(B\)를 택하면
\((q,B)=1\Rightarrow q_0\nmid q\)다. H1c-1b.1의 capacity와 합쳐 actual modulus
family가 두 endpoint의 non-exceptional sum에 포함됨을 닫았다.

최종 NYJM판 Theorem 1.4의 양의 RHS 12항도 전수 등록했다. 중심이
\(\psi(u)/\varphi(q)\)이므로 raw \((T,2T]\) von Mangoldt discrepancy는
\(D_{2T}-D_T\), 합계 상계는 \(R_B(2T)+R_B(T)\)다.

그러나 half-open endpoint, prime powers, unweighted prime count, exact recentering,
represented-prime density와 12항의 common cutoff는 열려 있다. 따라서 66개 root row의
상태 수는 바뀌지 않고 `SIV-07/08=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`이다. 다음 gate는 H1c-1b.3 count transfer다.

## 27. 2026-09-09 H1c-1b.3 endpoint·count transfer 반영

H1c-1b.3은 actual identity form의 목표를 Maynard 정의 그대로
\([T,2T)\)의 unweighted prime count와 exact total center로 고정했다. H1c-1b.2의
fixed family가 두 endpoint뿐 아니라 Abel 적분의 모든 \(u\in[T,2T]\)에서도 유효함을
확인하고, plus-sign partial summation, prime-power 비용
\(2\sqrt{2T}(M_B+\Phi_B)\)와 half-open endpoint 비용 \(M_B\)를 보존했다.

따라서 exact target-quantity transfer는 닫혔다. 그러나 Bordignon의 source constant
정규화, represented-prime density와 모든 remainder/count 비용의 common-cutoff 흡수는
H1c-1b.4에 남는다. 66개 root row 상태 수와 `SIV-07/08/09=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`은 바뀌지 않는다.

## 28. 2026-09-09 H1c-1b.3r1 FGKMT endpoint 교정

앞 절의 “actual \([T,2T)\)” 표기는 철회한다. Maynard 원문 Definition (2.1)은
\([T,2T)\)이지만, FGKMT Definition 2는
\(\mathcal A(T)=\{n:T\le n\le2T\}\)로 수정했다. FGKMT Section 8의 외부 prime set은
\((T,2T]\)이다.

H1c-1b.3r1은 source \((T,2T]\)에서 actual closed target으로 옮길 때 lower atom
\(1_{\mathbb P}(T)\) 하나만 더하면 되며, centered residue discrepancy의 추가 절댓값이
modulus마다 1 이하임을 확인했다. 따라서 기존 endpoint 수치 envelope와 density lower는
보존된다. 다만 Theorem 6의 weighted closed sum을 외부 \((T,2T]\) sum으로 되돌릴 때의
\(w(T)\)는 별도 의무다.

## 29. 2026-09-09 H1c-1b.4a–4e actual input 합성

4a–4d는 Bordignon source normalization, exact density, 모든 remainder/count-transfer
비용의 absorption과 corrected source constant를 닫았다. 4e는 이를 actual closed
identity-form input에 합성해

\[
T=X/2,\qquad r=\lfloor(\log T)^{1/5}\rfloor\ge10^{10}
\]

즉 \(X\ge2\exp(10^{50})\)에서 Hypothesis 1(1)--(3)의 valid constants
\((1,1,2)\)를 얻었다.

이는 `SIV-08` 안의 **actual P9.2 Hypothesis-input child**만 닫는다. weighted
Proposition 9.2의 main/error 합성, lower-endpoint weight, Theorem 6 전체 상수는
열려 있다. 따라서 66개 root row의 상태 수와
`SIV-07/08/09=HARD_BLOCKER`, \(X_{\mathrm{cert}}=\)`OPEN`은 유지한다.
다음 gate는 H1b-P92a다.

## 30. 2026-09-09 H1b-P92a actual weighted child

앞 §29의 OPEN은 당시 snapshot이다.
[theory 44](44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md)는 actual identity
weighted P9.2의 모든 prefactor·error와 lower weight/count atom을
\(k\ge10^{200}\), \(X=2T\ge2\exp(10^{1000})\)에서 multiplier 1/1로 닫는다.
이 수는 child 하나의 sufficient cutoff다. 소수를 그 수까지 센 결과도, Sono의
\(X_{\rm cert}\)도 아니다.

root 66행의 상태는 바꾸지 않는다. SIV-07/08/09는 general형/실제 다른 moment/공통
정규화를 포함하기 때문이다. 다음은 H1b-P91a, growing-k P94 호환성과 실제 dependency
가지치기다. FGKMT Theorem 6 proof에 P95 직접 인용이 없다는 source 사실은 확인했지만,
그것만으로 모든 후속 FMT/Sono 사용처에서 P95가 불필요하다고 단정하지 않는다.


## 31. 2026-09-09 H1b-P91a unweighted·W-filter scope correction

[theory 45](45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md)는 actual
\(\mathcal A=\mathbb Z,\ T'=2\lfloor Y\rfloor,\mathcal L'=\varnothing\)에서
unweighted moment와 exact closed shift를 \(k\ge10^{200}\)에서 닫았다.
따라서 H1B-P91은 ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT이다.
exact \(E_q^{(1)}\le1\)을 직접 사용하므로 actual child는 미지 Hypothesis multiplier를 기다리지 않는다.

중요한 적용 범위: P91/P92/P94의 Maynard proof는 명시적 W-coprimality filter를 쓴다.
FGKMT (7.4)의 literal 표시에는 이 indicator가 없어 두 함수를 동일시하지 않는다.
theory 45 §2가 filtered construction의 shift·prime-slice 호환성을 증명한다.
P92a의 이전 수치식은 filtered weight에서 보존되며 unfiltered transfer는 미인증이다.

다음은 H1b-P94g의 growing-k 호환성과 H1b-NORM의 공통 정규화다.
root 66행의 상태, SIV-07/08/09 HARD_BLOCKER와 X_cert OPEN은 바꾸지 않는다.

## 32. 2026-09-09 H1b-P94g growing-k·actual local interval

[theory 46](46_Sono_FMT_H1bP94g_growing_dimension_rough_moment.md)는
명시적 W-filtered actual P94의 growing-k 호환성을 닫았다.
실제 local scale \(T_0=\lfloor Y\rfloor-\lfloor X\rfloor\)를 사용하며, q 구간의 이동은
\((T_0,2T_0]\)다. closed interval 확대와 원래 support 제거는 비음성 상계로 처리했다.

기존 uniform \(I(F_1)\le2I(F)\)에서 상대오차 \(4\delta\)를 얻어 fixed-k의 \(2^{-k}\)
gate를 사용하지 않는다. sharp·Euler·distribution을 합성한 exact
\(8249009/8820900<1\)로 multiplier 1을 얻었다.
\(k\ge10^{200}\), \(\log C_h\le\log(X/2)/4\)라는 강한 새 regime의 결과이며,
기존 multiplier 13의 모든 parameter 범위를 교체하지 않는다.
각 p의 local singular series를 보존한 off-tuple 상계도 explicit하다.

다음은 H1b-NORM: 세 moment의 공통 series/lambda/filtered-weight/tau/u 및 실제 dependency
가지치기다. broad SIV-07/08/09 HARD_BLOCKER, root 66행 상태와 X_cert OPEN은 유지한다.
기존 §31의 다음 단계는 당시 snapshot이며 이 절이 현재 상태다.

## 33. 2026-09-09 H1b-NORM 후속 상태


공통 정규화 successor [theory 47](47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md)는
같은 W-filter construction의 P91/P92/P94를 exact series/lambda-square/tau/u_X로 연결했다.
k>=10^200에서 P91 상대오차 4/k, P92 상대오차 2/sqrt(k), fixed-X 확률 입력
상대오차 3/sqrt(k)와 point probability X^(-3/4)를 얻었다.
FMT B0 삭제도 한 weighted atom 비용으로 닫았다.

u_X는 X와 source B에 의존할 수 있다. 고정-X에서 p,q,i 및 무작위 선택에 무관한
scalar라는 양화로 직접 확률식을 증명했으며 literal only-k 의존성은 인증하지 않았다.
actual filtered common child가 explicit하다는 사실과 broad 일반 P6.1/Hypothesis,
뒤쪽 FMT correlation/failure 및 전체 X_cert가 열려 있다는 사실을 함께 기록한다.
다음 H1b-DEP는 actual call graph에서 P95 필수 여부와 root node 분리를 감사한다.
앞 절들의 다음 단계는 당시 snapshot이며 이 절이 현재 상태다.

## 34. 2026-09-13 DEP-R09 JL8 actual local-count 후속 상태

[theory 65](65_Sono_FMT_DEPR09_Jutila_Lemma8_actual_local_zero_count.md)는 McCurley 1984의
식 (5), (13), Lemmas 1--4를 actual near-one square에 다시 합성해

```text
N_square < 3 + r*log(q*(1+abs(t0))),  0<r<=1/21
```

을 얻었다. Jutila의 strip-to-selected-system 전달은
`N_nonprin<=2J{3+r log(2qT)}`다. 따라서 Jutila density 재증명의 하위 node
`JL8-ACTUAL-NEAR-ONE`은 explicit source replacement로 진전했다.

그러나 T1의 root `PAP-08/PAP-11`은 JL7·식 (3.6) terminal multiplier, finite
log correction, exceptional branch와 Gallagher/Maier 종단 합성을 함께 포함한다. 따라서
66개 root row의 상태 수는 바꾸지 않고 `PAP-11=HARD_BLOCKER`, DEP-R09·fixed coefficient·
`X_cert=OPEN`을 유지한다. 이 절의 다음 gate 표기는 당시 snapshot이며 아래 절이 우선한다.

## 35. 2026-09-13 DEP-R09 JL7·식 (3.6) 종단 매개변수 교정

[theory 66](66_Sono_FMT_DEPR09_Jutila_JL7_terminal_parameter_repair.md)은 Theory 60의
branch scope를 교정했다. 고정 \(\tau=8/5\), `37.769894`는 Jutila printed p.54
Theorem \(1'\)에만 해당하고, p.52 식 (3.6)은

```text
tau_theta = (1+16*theta)/(1+14*theta)
```

를 쓴다. 올바른 대입으로 \(0<\theta\le1/21\)에서 Barban--Vehov coefficient는
\(13/\theta\) 미만, finite log ratio까지 곱한 weighted call은
\(34/\theta^2\) 미만이다. weight quotient 5, normalized area \(\theta^2/2\),
off-diagonal exponent margin과 strict \(A-E>0\) absorption interface도 explicit하다.

하지만 `JL7-CONT` shifted contour, `JL7-LEMMA3` absolute sum, `JL7-RES`
principal residue·well-spacing multiplier는 숫자가 아니다. 따라서 66개 root row의
상태를 바꾸지 않고 `PAP-11=HARD_BLOCKER`, DEP-R09·fixed coefficient·
`X_cert=OPEN`을 유지한다. 다음 gate는 `JL7-CONT`의 numerical multiplier를
선행 source에서 복원하거나 actual 범위에 직접 증명하는 일이다.

## 36. 2026-09-13 DEP-R09 JL7-CONT shifted-contour 후속 상태

[theory 67](67_Sono_FMT_DEPR09_Jutila_JL7_shifted_contour_multiplier.md)은 위 절의
첫 gate를 닫았다. 비주지표와 주지표를 서로 다른 peer-reviewed exact source에서 가져오고,
actual `0<Re z<=1/7`에서 principal ratio를 `4/3` 이하로 보존했다. 따라서

```text
|L(theta+u+i(v+y),chi)|
  <= 12*zeta(1+theta)*sqrt(q*T)*sqrt(1+|y|)
C_CONT(theta)
  = (96*sqrt(2)/pi)*zeta(1+theta)*(2/theta+1)
Cbar_CONT(theta)
  = 48*(1+1/theta)*(2/theta+1)
```

를 actual 식 (3.6) 범위에서 쓸 수 있다. `theta=1/21`에서 마지막 초등 상계는 정확히
`45408`이다. 이로써 `JL7-CONT=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다.

그러나 `JL7-LEMMA3`, `JL7-RES`, `JL7-ABSORB`, `JL7-AVERAGED`는 계속 OPEN이다.
따라서 66개 root row의 상태와 `PAP-11=HARD_BLOCKER`, DEP-R09·fixed coefficient·
`X_cert=OPEN`은 바꾸지 않는다. 다음 gate는 `JL7-LEMMA3`의 actual absolute-sum
multiplier와 support endpoint를 source-first로 복원하는 일이다.

## 37. 2026-09-13 DEP-R09 JL7-LEMMA3 absolute-sum 후속 상태

[theory 68](68_Sono_FMT_DEPR09_Jutila_JL7_Lemma3_absolute_sum.md)은 위 절의
두 번째 gate를 닫았다. Jutila Lemma 2의 actual
`f(p)=mu(p)phi(p)=-(p-1)`를 대입하면, \(p\)가 한 outer 변수에만 있을 때 local
절댓값 계수합은 \(p+1\), 두 변수에 모두 있을 때는 \((p-1)^2\)다. 특히 \(p=2\)의
nonconstant coefficient는 0이고 local 합은 1이다. Jutila Lemma 3의 인쇄 상계와
유한 divisor double-counting을 결합해

```text
H_q(R) < 3*R^2
Cbar_CONT+L3(theta) = 144*(1+1/theta)*(2/theta+1)
Cbar_CONT+L3(1/21) = 136224
```

를 얻었다. 이로써 `JL7-LEMMA3=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다. 상수 3은
최적화값이 아니라 hidden asymptotic 없이 쓸 수 있는 rational safety bound다.

그러나 `JL7-RES`, `JL7-ABSORB`, `JL7-AVERAGED`는 계속 OPEN이다. 따라서 66개 root
row의 상태와 `PAP-11=HARD_BLOCKER`, DEP-R09·fixed `2e-17`·`X_cert=OPEN`은
바꾸지 않는다. 다음 gate는 `JL7-RES`의 principal residue, 대각 조건과 같은
character의 repeated-height row-sum multiplier를 source-first로 복원하는 일이다.

## 38. 2026-09-13 DEP-R09 JL7-RES principal residue 후속 상태

[theory 69](69_Sono_FMT_DEPR09_Jutila_JL7_principal_residue_height_row_sum.md)은
Jutila printed p.53 residue와 p.51의 parity별 \(\Delta\)-well-spacing을 합성했다.
Lemma 3의 reciprocal identity로 \(r=r'\)만 남기고, pole-cancelled Gamma ladder
kernel과 same-character height inverse-square row를 수치화하면 한 selected system에서

~~~text
zero-pair row < 91*theta*L^3
sum'_(r<=R) phi(r)/r^2 < 12*(phi(q)/q)*L
principal residue < 52*J*(phi(q)/q)^2*x^(2-2alpha)*L^2
~~~

를 얻는다. 마지막 52는 \(12\cdot91\theta\le1092/21=52\)의 calculator-safe
endpoint다. 따라서 `JL7-RES=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 진전한다.

그러나 이 결과는 66개 root row 중 `PAP-08/PAP-11` 자체를 닫지 않는다.
`JL7-ABSORB`의 even/odd factor·모든 오차의 strict common cutoff,
`JL7-AVERAGED`의 variable-modulus replay와 Gallagher--Maier pointwise PAP bridge가
남아 있다. 따라서 root 상태 수는 바꾸지 않고 `PAP-11=HARD_BLOCKER`,
DEP-R09·fixed `2e-17`·`X_cert=OPEN`을 유지한다. 다음 gate는 `JL7-ABSORB`다.

## 39. 2026-09-13 DEP-R09 JL7-ABSORB strict terminal 후속 상태

[theory 70](70_Sono_FMT_DEPR09_Jutila_JL7_strict_terminal_absorption.md)은
Theory 64--69의 detector, weighted upper, contour·Lemma 3와 residue 상수를 한
selected-system 부등식에 넣었다. exact composition은

~~~text
C_pre = 170/theta^2
C_CL3 = 144*(1+1/theta)*(2/theta+1)
A = c_bar^2*A_int
B = 52*C_pre
E <= 36*C_pre*A_int*C_CL3*exp(-29*theta*L/252)
~~~

이다. \(L\ge L_{\rm common}\)에서 \(E\le A/2<A\)이므로
<code>J <= 884000*x^(2(1-alpha)) / [9(1-theta)^2*theta^6]</code>이다.

Theory 65의 parity·local-count factor는 이 one-system 흡수 뒤에만 넣는다.
따라서 <code>JL7-ABSORB</code>와 actual fixed-\(q\) nonprincipal near-one terminal
density는 parameterized explicit으로 진전한다.

이 승격은 66개 root row의 <code>PAP-08/PAP-11</code>을 닫지 않는다. printed
Jutila Theorem 1 전체, 식 (3.7)의 가변 modulus·primitive-character averaged replay와
Gallagher--Maier pointwise PAP bridge가 남아 있다. 그러므로 root 상태 수,
<code>PAP-11=HARD_BLOCKER</code>, DEP-R09·fixed \(2\times10^{-17}\)·
\(X_{\rm cert}=\mathrm{OPEN}\)은 유지한다. 다음 gate는 <code>JL7-AVERAGED</code>다.

## 40. 2026-09-14 DEP-R09 JL7-AVERAGED primitive near-one 후속 상태

[theory 71](71_Sono_FMT_DEPR09_Jutila_JL7_averaged_primitive_replay.md)은 Jutila
printed pp.53--54 식 (3.7)을 공통 \(D=Q^2T\)에서 재생했다. 각
primitive nonprincipal conductor \(q_j\le Q\)에서 detector의
\(\varphi(q_j)/q_j\)는 phase \(q_j/\varphi(q_j)\)와 상쇄된다. principal
product pair는 같은 primitive character에서만 생기므로 conductor가 같고,
residue·pseudocharacter totient factor까지 합친 exact product는 1이다.
off-diagonal phase pair는 \(L^{-2}\)로 정규화하면 36 이하이며, product
conductor는 \(\operatorname{lcm}(q_j,q_k)\le Q^2\)라 공통 contour scale에 든다.

따라서 Theory 70의 strict half-margin과

<code>C_J = 884000 / [9(1-theta)^2 theta^6]</code>

를 raw \(Q\) multiplier 없이 재사용할 수 있고,
<code>JL7-AVERAGED-NP-NEAR-ONE=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT</code>으로
진전한다.

하지만 이 좁은 density result는 66개 root row의 pointwise
<code>PAP-08/PAP-11</code>을 직접 닫지 않는다. Gallagher--Maier proof 안에서
near-one family, principal zeta, exceptional character, prime powers,
\(\psi\to\pi\), endpoint와 common cutoff를 합성하는
<code>JL7-AVERAGED-TO-PAP</code>가 새 hard blocker다. 그러므로 root 상태 수,
<code>PAP-11=HARD_BLOCKER</code>, DEP-R09·fixed \(2\times10^{-17}\)·
\(X_{\rm cert}=\mathrm{OPEN}\)은 변경하지 않는다.

## 41. 2026-09-14 DEP-R09 Gallagher--Maier PAP split 후속 상태

[theory 72](72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md)는
앞 절의 <code>JL7-AVERAGED-TO-PAP</code>를 다음 두 primitive nonprincipal
component로 분리했다.

~~~text
GMP-FAR-ALPHA:
  Bennett total zero-count + Stieltjes endpoint
  -> ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT

GMP-NEAR-INTEGRAL:
  Theory 71 near-one density split at delta=1/log(D)
  -> ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
~~~

\(Q=X^{1/d},T=Q^5,\mathcal D=Q^7\)와
\(\theta=1/21,d=160,c_1=1/24\)에서 far exponent는 \(13/3360>0\)이지만,
near certificate의 asymptotic upper envelope는 약
\(2.7277\times10^{13}\)이다. 따라서 현재 sufficient certificate는 양의 PAP
main-term gate도 통과하지 못한다. 이 판정은 actual prime-distribution error의
크기에 관한 하한이 아니며, 현 proof upper bound의 불충분성만 뜻한다.

printed Jutila all-alpha theorem은 이 분할의 필수 의무에서 제외할 수 있지만,
Gallagher explicit-formula multiplier·공통 cutoff, principal zeta,
exceptional/good-modulus transfer, full orthogonality replay,
\(\psi\)-to-\(\pi\)는 여전히 OPEN이다. 더구나 가장 앞선 coefficient gate가
이미 실패하므로 66개 root 상태 수와 <code>PAP-11=HARD_BLOCKER</code>,
DEP-R09·fixed \(2\times10^{-17}\)·\(X_{\rm cert}=\mathrm{OPEN}\)은 유지한다.
다음 gate는 \(C_J\) loss tree의 구조적 축소 가능성 감사다.

## 42. 2026-09-14 DEP-R09 \(C_J\) loss tree 후속 상태

[theory 73](73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md)은 앞 절에서 처음 실패한
near coefficient를 exact factor tree로 분해했다.

~~~text
C_J baseline = 2 * 52 * 5 * (34/theta^2) * cbar^(-2) * (theta^2/2)^(-1)
C_J(1/21) = 9,287,613,243,090
C_J finite-safe tightened = 11503697604450072/425315
local improvement = 343.3818727...
d=186 exp(-2) cap = 0.05850429428...
tightened/cap = 4.62316094119e11
~~~

denominator, averaged residue, weighted source specialization, exact area와 absorption slack의
국소 개선은 유효하다. 그러나 현 \(\theta^{-6}\) architecture의 scale만 남긴
counterfactual도 budget보다 약 \(1.466\times10^9\)배 크다. 이는 모든 재배열에 대한
불가능성 정리는 아니지만, `JL7-CONT`나 Lemma 3 cutoff 상수를 더 줄이는 작업이 현재
root gate를 닫지 못한다는 판정이다.

따라서 66개 root row의 상태와 <code>PAP-11=HARD_BLOCKER</code>,
DEP-R09·fixed \(2\times10^{-17}\)·\(X_{\rm cert}=\mathrm{OPEN}\)은 변경하지 않는다.
다음 gate는 \(d\le186\) actual family에 적용되는 modern explicit near-one density source
또는 detector·weight·integration 구조를 바꾸는 증명의 정량 비교다. 새 source가 cap을
통과할 전망을 보이기 전에는 threshold calculator와 장시간 prime 계산을 만들지 않는다.

## 43. 2026-09-14 DEP-R09 modern explicit density source-screen 상태

[theory 74](74_Sono_FMT_DEPR09_modern_explicit_density_source_screen.md)는
Theory 73 이후 식별한 modern 후보를 다음 fail-closed 계약으로 선별했다.

~~~text
actual primitive family + numerical multiplier + numerical finite cutoff
+ exceptional handling + pointwise PAP transfer + D<=186 coefficient capacity
~~~

Ramaré 2016은 이 중 source density 상수와 범위는 모두 수치지만, 현재 Gallagher
kernel에 theorem RHS를 direct nonnegative insertion하면 (d=186,c_1=1/24)의
source 최소범위에서 한 unit slice만으로 main certificate가 8602, additive certificate가
64912보다 크다. 이 certificate floor는 (X)와 함께 증가한다. 이는 실제 error의
하한이나 Ramaré source의 무용성 명제가 아니라 이 direct proof composition의 실패다.

Thorner--Zaman explicit density의 near exponent 99·170은 capacity 안이지만 fixed
prefactor·exceptional·PAP transfer budget이 닫히지 않았다. uniform PNT 계열은 구조상
유망하지만 relevant numerical constants와 cutoff가 없다. Friedlander--Iwaniec sieve
route는 (52600>186), (1/210000<4/5)이고, 미검증 arXiv의 (o(1))과
in-preparation statement는 승격하지 않았다.

따라서 66개 root row의 상태와 <code>PAP-11=HARD_BLOCKER</code>,
DEP-R09·fixed (2\times10^{-17})·(X_{\rm cert}=mathrm{OPEN})은 변경하지 않는다.
이번 판정은 식별한 후보 집합에 한정하며 모든 문헌·hybrid proof를 배제하지 않는다.
다음 gate는 numerical source watch 또는 smoothing·hybrid minimum·cancellation을
보존하는 PAP transfer의 coefficient-feasibility 설계다. 이 gate 전에는 threshold
calculator나 장시간 prime sweep을 실행하지 않는다.

## 44. 2026-09-14 DEP-R09 alternative PAP transfer feasibility 상태

[theory 75](75_Sono_FMT_DEPR09_hybrid_smoothing_cancellation_transfer_feasibility.md)는
Theory 74가 남긴 hybrid·smoothing·cancellation 세 경로를 coefficient gate에서 먼저
검사했다. Ramaré와 tightened Jutila RHS의 pointwise minimum도
$21\le d\le186$ 전체에서 첫 unit slice certificate floor가 8602.030894...를 넘는다.
이는 실제 error 하한이 아니라 현 sufficient upper certificates의 결합 한계다.

fixed nonnegative $[1,2]$ smoothing은 zero-height 분포를 사용하지 않는 gamma-uniform
absolute envelope에서 필요한 $1.5733\times10^{-5}$ 감쇠를 보증하지 못한다.
height-sensitive smoothing 전체는 배제하지 않는다. Gallagher 식 (30)의 절댓값 뒤
$N^*$에는 phase 정보가 없으므로 cancellation은 pre-absolute-value pointwise PNT 또는
explicit second-moment theorem이라는 새 input을 요구한다.

따라서 66개 root row의 상태와 <code>PAP-11=HARD_BLOCKER</code>,
DEP-R09·fixed $2\times10^{-17}$·$X_{\rm cert}=\mathrm{OPEN}$은 변경하지 않는다.
threshold calculator와 장시간 prime sweep도 NOT READY다. 다음 gate는 fully numerical
pointwise PNT 또는 pre-absolute-value uniform moment source audit다.

## 45. 2026-09-14 DEP-R09 pre-absolute moment·pointwise PNT source 상태

[theory 76](76_Sono_FMT_DEPR09_preabsolute_moment_pointwise_PNT_source_audit.md)은
Maier printed proof가 각 admissible column에 pointwise PNT를 적용하지만 최종 row 선택은
그 columns의 aggregate prime mass만 소비함을 재확인했다. 따라서 일반 modulus 평균은
drop-in이 아니나, Maier가 정한 fixed primorial과 residue subset에 대한 aggregate
second-moment theorem은 R09의 column-mass 단계를 교체할 수 있다.

감사한 fully explicit 후보 중 Akbary--Hambrook와 Sedunova L1 RHS는 direct certificate
floor가 $e^{-2}$ budget보다 각각 4,527배·13,693배 이상 크다. Bennett et al. pointwise
theorem의 $q>10^5$ source cutoff는 $Y=q^d$에서
$d\ge0.03\sqrt q(\log q)^2$를 요구해 경계부터 $d>1257$이고, current
$d\le186$과 겹치지 않는다. 이는 actual prime error의 하한이나 모든 평균 방법의
불가능성 명제가 아니다.

$M$개 admissible residues에 필요한 정확한 missing input은

~~~text
sum_chi |Z_chi(Y)|^2 <= epsilon^2 * M * Y^2 / phi(q)
~~~

이며 pointwise second-moment budget보다 $M$배 약하다. 그러나 numerical multiplier,
finite cutoff, exceptional/principal·endpoint·prime-power·psi-to-pi 처리를 포함한
unconditional individual-primorial source는 식별하지 못했다.

따라서 66개 root row의 상태와 <code>PAP-11=HARD_BLOCKER</code>, DEP-R09,
fixed $2\times10^{-17}$, $X_{\rm cert}=\mathrm{OPEN}$은 변경하지 않는다. 다음 R09 gate는
restricted-residue/individual-primorial variance source 또는 이 missing theorem의 직접
proof decomposition이다. 이 gate 전 threshold calculator와 장시간 prime sweep은 NOT READY다.

## 46. 2026-09-14 DEP-R09 restricted-residue spectral 후속 상태

[theory 77](77_Sono_FMT_DEPR09_restricted_residue_variance_spectral_optimality_audit.md)은
Theory 76이 제안한 character-energy 하위질문을 exact하게 닫았다. (M)개 reduced residues의
total energy는 항상 (\varphi(q)M), 비주지표 energy는 (M(\varphi(q)-M))이므로 Maier
admissible set이라는 구조만으로 unweighted (L^2) total을 줄일 수 없다. aligned-vector
equality가 있어 total-energy Cauchy 상수도 보편적으로 sharp하다.

따라서 R09의 최소 열린 입력은 full variance보다 약한 direct weighted correlation

~~~text
abs(sum_(chi != chi0) C_chi(A_y) Z_chi(Y))
  <= (epsilon-delta0) * M * Y
~~~

이다. 같은 (y)가 Maier Lemma 6의 survivor 조건도 만족해야 하므로 modulus/y 평균 결과를
자동 승격하지 않는다. current power regime에서 unconditional fully numerical fixed-primorial
source는 식별되지 않았다. 66개 root row 수와 <code>PAP-11=HARD_BLOCKER</code>, DEP-R09,
fixed (2\times10^{-17}), (X_{\rm cert}=\mathrm{OPEN})은 변경하지 않는다.

## 47. 2026-09-14 DEP-R09 Maier/FMT CRT 이동량 양화사 후속 상태

[theory 78](78_Sono_FMT_DEPR09_Maier_CRT_shift_quantifier_audit.md)은 Theory 77의
simultaneous-selection 문구를 실제 source quantifier로 고쳤다. Maier 1981 Lemma 6의
fixed prime partition에서는

~~~text
y = 0 mod P1*P3
y = 1 mod P2
~~~

가 \(y\bmod P(x)\)를 하나로 정하므로 고전 \(y\)-평균 표본공간은 없다. Sono/FMT actual
proof에서는 sieve residue vector \(\boldsymbol a\)마다 CRT \(m(\boldsymbol a)\)가 하나
정해지고, FMT proof 내부의 randomized vector family가 평균 후보가 된다.

그러나 현재 정본은 sieve-good event와 direct weighted-correlation-good event가 같은
vector에서 성립한다는 numerical positive mass를 주지 않는다. finite family
\(\Omega\)에서 세 bad-set cardinality 합이 \(|\Omega|\)보다 작으면 simultaneous good
candidate가 남는다는 논리만 Lean <code>KERNEL_PASS</code>로 닫았다. analytic bad-set
상계는 새 R09 의무다.

따라서 66개 root row와 <code>PAP-11=HARD_BLOCKER</code>, DEP-R09,
fixed \(2\times10^{-17}\), \(X_{\rm cert}=\mathrm{OPEN}\)은 변경하지 않는다.
uniform-in-vector correlation source 또는 FMT construction law 위의 공통 numerical
failure budget 전에는 threshold calculator와 장시간 prime sweep을 시작하지 않는다.

## 48. 2026-09-14 DEP-R09 FMT construction law 유한 성공질량 후속 상태

[theory 79](79_Sono_FMT_DEPR09_FMT_construction_law_finite_mass_audit.md)은
Theory 78의 FMT 후보 변수를 source law에 맞게 교정했다. final residue outcome은
first-stage \(\mathbf A\) 하나가 아니라 conditional hypergraph output
\(\mathbf N'\)까지 포함한 joint/sequential pair다.

출판된 FMT의 성공률은 여전히 \(1-o(1)\)이고 numerical rate가 없다. 그러나 project
Theory 53·55는 outer failure \(F_{\rm out}\)과 모든 outer-good \(\mathbf A\)에 대한
uniform conditional inner failure \(F_{\rm in}\)을 이미 유한식으로 준다. 따라서 같은
joint law에서

~~~text
P(sieve-good) >= (1-F_out)(1-F_in)
~~~

이 parameterized explicit이다. independence는 필요 없다. 이로써 sieve-good positive
mass 자체는 새 hard blocker가 아니게 됐다.

남은 R09 입력은 같은 \((\mathbf A,\mathbf N')\) law에서 weighted-correlation bad
event의 failure upper bound다. \(F_{\rm corr}<(1-F_{\rm out})(1-F_{\rm in})\)이면
simultaneous selection이 가능하지만 현재 \(F_{\rm corr}\)는 OPEN이다. 따라서 66개 root
row와 <code>PAP-11=HARD_BLOCKER</code>, DEP-R09, fixed \(2\times10^{-17}\),
\(X_{\rm cert}=\mathrm{OPEN}\)은 변경하지 않는다. threshold calculator와 장시간
prime sweep도 NOT READY다.

## 49. 2026-09-14 DEP-R09 same-law weighted-correlation tower 후속 상태

[theory 80](80_Sono_FMT_DEPR09_same_law_weighted_correlation_tower_audit.md)은
Theory 79의 열린 \(F_{\rm corr}\)를 actual joint law의 normalized second moment로
분해했다. final CRT-dependent error를 \(R(\omega)\), survivor count를 \(M_\omega\),
\(\tau=\varepsilon-\delta_0>0\)라 하면 outer-good domain의

~~~text
W(omega)=abs(R(omega))^2/(M_omega^2*Y^2)
~~~

에 대한 가장 약한 현재 sufficient input은

~~~text
E[W] < tau^2*(1-F_out)*(1-F_in)
~~~

이다. outer-good conditional 또는 uniform-fiber route는
<code>F_in+mu_f/tau^2&lt;1</code>을 요구한다. raw moment만 쓰면 pointwise
\(M_\omega\ge M_{\min}>0\)가 별도로 필요하다.

FMT formula (1.1)는 finite tower identity만 주며, FMT Theorem 4·FGKMT Corollary 4의
fixed-subset cardinality preservation은 final output이 정한 signed/complex CRT weight에
대한 theorem이 아니다. actual same-law analytic moment source는 식별되지 않았다.
따라서 66개 root row와 <code>PAP-11=HARD_BLOCKER</code>, DEP-R09, fixed
\(2\times10^{-17}\), \(X_{\rm cert}=\mathrm{OPEN}\)은 변경하지 않는다. 다음 gate는
final FMT covering filtration에서 이 moment의 one-step 민감도와 numerical concentration
가능성을 감사하는 것이다. threshold calculator와 장시간 prime sweep은 NOT READY다.

## 50. 2026-09-15 DEP-R09 filtration 민감도·survivor floor 후속 상태

[theory 81](81_Sono_FMT_DEPR09_filtration_sensitivity_survivor_floor_audit.md)은
Theory 80의 denominator premise를 actual Theory 55 event에 맞췄다. pointwise floor는
outer-good (O) 전체가 아니라 (S_{\rm sieve}=O\cap I_{\rm good})에서 성립한다.
따라서 raw moment와 normalized badness도 같은 event indicator로 제한한다.

FGKMT Theorem 3의 final covering은 nibble별 conditional product law이며 final residue
전체의 global product law가 아니다. 한 prime residue 변경에 대한 survivor count 경계
(2\lceil N/p\rceil)는 exact하지만, (P=65) nonprincipal-character fixture는 character
합 변화 3이 membership bound 2보다 큼을 보인다. 따라서 이 count 경계를 weighted
phase의 bounded increment로 옮기는 경로는 기각한다.

현재 새 R09 의무는 actual final sieve-good law의 conditional second moment 또는 nibble별
Doob increment와 conditional variance의 numerical theorem이다. generic Freedman·typical
bounded-difference 정리는 이 입력을 대신 공급하지 않는다. 따라서 66개 root row와
<code>PAP-11=HARD_BLOCKER</code>, DEP-R09, fixed (2\times10^{-17}),
(X_{\rm cert}=\mathrm{OPEN})은 변경하지 않는다. threshold calculator와 장시간 prime
sweep은 NOT READY다.

## 51. 2026-09-15 DEP-R09 outer entropy·convolution moment 후속 상태

[theory 82](82_Sono_FMT_DEPR09_outer_entropy_convolution_second_moment.md)는 Theory 81의
direct same-law moment 목표를 actual FMT outer law와 finite Fourier algebra로 축약했다.
outer coordinates \(A_s\bmod s\)가 독립 균등이고 final system에 보존되므로
\(Q_{\mathcal S}=\prod_{s\in\mathcal S}s\)에 대해

\[
\Pr(S_{\rm sieve},m_\omega=r)\le Q_{\mathcal S}^{-1}.
\]

finite Parseval과 cyclic convolution Cauchy를 합치면

\[
\rho_S\le\varphi(q)N^2V(Y,q)/Q_{\mathcal S},
\]

따라서 strict sufficient gate는

\[
V(Y,q)<
\tau^2p_*Q_{\mathcal S}M_{\min}^2Y^2/
\{\varphi(q)N^2\}.
\]

이 reduction은 exact하지만 좌변에 대한 fully numerical fixed-primorial upper theorem은
OPEN이다. Dusart theta bound는 \(Q_{\mathcal S}\)만 명시화하고, 확인한
Davenport--Erdos, Friedlander--Goldston, Vaughan, BDH와 moving-interval source는
actual modulus·law·cutoff를 동시에 충족하지 않는다. 따라서 66개 root row와
<code>PAP-11=HARD_BLOCKER</code>, DEP-R09, fixed \(2\times10^{-17}\),
\(X_{\rm cert}=\mathrm{OPEN}\)은 변경하지 않는다. threshold calculator와 장시간
prime sweep도 NOT READY다.
