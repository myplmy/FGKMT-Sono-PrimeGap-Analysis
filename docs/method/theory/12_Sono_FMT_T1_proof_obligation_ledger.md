# Sono/FMT T1 numerical-threshold proof-obligation 원장

## 2026-09-09 H1b-COR1 현재 상태

[theory 49](49_Sono_FMT_H1bCOR1_finite_correlation_conditioning.md)와
[review 55](../../review/55_20260909_H1bCOR1_finite_correlation_타당성검토.md)가 현재 actual 확률 입력 정본이다.
H1b-DEP의 P95 비필수 판정은 유지한다. R01 correlation, R02 sigma/조건부 희소성,
R04 good-P failure와 actual small-codegree를 같은 child cutoff에서 수치로 닫았다.
theory 48/DEP JSON의 당시 12 OPEN은 소급 수정하지 않고 successor에서 3개 closure를 반영한다.
현재 9작업/6묶음이 남으며 개수는 완료율이 아니다. 다음은 H1b-COR2 / DEP-R05이다.
full hypergraph·PAP/UB·최종 공동 오차·arbitrary-X는 아직 열려 있다.
broad SIV-07/08/09는 HARD_BLOCKER, X_cert는 OPEN이다.
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
| `EXPLICIT` | 7 | 해당 행의 식·정의는 숫자 또는 exact algebra로 닫힘 |
| `PARTIAL` | 9 | 일부 상수·방향은 명시됐지만 유효범위 또는 다른 수치 입력이 빠짐 |
| `RATE_MISSING` | 30 | (o(1)), (O), (ll), `sufficiently large`의 숫자 rate가 없음 |
| `SOURCE_REVIEW_REQUIRED` | 4 | 인용된 하위 원문 정리를 더 깊게 감사해야 함 |
| `HARD_BLOCKER` | 16 | 현재 공개 서술만으로는 숫자 certificate가 닫히지 않음 |
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
| `COV-11` | 모든 random good event의 실패확률 합 (<1) | `HARD_BLOCKER` | 각 (1-o(1)) rate가 없음 |
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
| `COV-02` | epsilon finite partition | `RATE_MISSING` |
| `COV-03` | smooth-number remainder | `RATE_MISSING` |
| `COV-04` | Proposition 6.2 cardinality/probability | `RATE_MISSING` |
| `COV-05` | covering density (C) | `RATE_MISSING` |
| `COV-06` | quantitative hypergraph theorem | `HARD_BLOCKER` |
| `COV-07` | FGKMT Corollary 3→FMT Theorem 4 | `PARTIAL` |
| `COV-08` | finite success probability | `HARD_BLOCKER` |
| `COV-09` | (m,A') floor relation | `PARTIAL` |
| `COV-10` | (epsilon_0) compatibility | `RATE_MISSING` |
| `COV-11` | simultaneous good choices | `HARD_BLOCKER` |
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

따라서 `SIV-03`은 `PARTIAL`에서 `EXPLICIT`로 승격됐다. 66개 root row의 현재 상태 수는
`EXPLICIT 7`, `PARTIAL 9`, `RATE_MISSING 30`, `SOURCE_REVIEW_REQUIRED 4`,
`HARD_BLOCKER 16`이다.

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
