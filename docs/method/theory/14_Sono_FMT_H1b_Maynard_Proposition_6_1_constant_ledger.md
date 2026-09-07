# Sono/FMT H1b Maynard Proposition 6.1 상수 원장

- 작성: 2026-09-04 KST
- 증거 수준: `SOURCE-LEVEL CONSTANT DEPENDENCY AUDIT`
- H1b 판정: `CONSTANT_DEPENDENCY_LEDGER_COMPLETE_NUMERICAL_PACKAGE_OPEN`
- `SIV-07`: `HARD_BLOCKER` 유지
- `SIV-09`: `RATE_MISSING` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json`](data/Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json)
- H1b-1 하위 감사:
  [`15_Sono_FMT_H1b1_basic_summation_constant_audit.md`](15_Sono_FMT_H1b1_basic_summation_constant_audit.md)
- H1b-1a finite package:
  [`17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md`](17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md)
- H1b-1b multiplier 복원:
  [`18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md`](18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md)
- H1b-1b-2a actual-call local-factor·제외모듈 하한:
  [`20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md`](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
  및 [`21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md`](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)

## 1. 결론부터

Maynard Proposition 6.1은 단순한 존재증명만은 아니다. 가중치가 어떻게 만들어지고, 네 종류의
moment가 어떤 주항과 오차 모양을 갖는지, 그 상수들이 \(\alpha,\theta\)와 Hypothesis 1의
상수에만 의존한다는 사실까지 서술한다. Maynard는 Hypothesis 1의 상수가 effective하면 최종
상수도 effective하게 계산할 수 있다고 명시한다.

그러나 출판된 식만을 대입해서 사용할 수 있는 **완성된 숫자표**는 아니다. 예를 들어

\[
1+O((\log x)^{-1/10})
\]

에서 지수 \(-1/10\)은 보이지만, \(O\) 앞의 multiplier와 이 식이 유효해지는 최초 \(x\)는
인쇄돼 있지 않다. Hypothesis 1도 \((\log x)^{-100k^2}\)라는 강한 감소 모양을 주지만 그 앞의
상수와 시작점은 입력으로 가정한다. 여러 식의 “충분히 큰 \(x\)”가 같은 \(x\)에서 동시에
성립하는지도 다시 합성해야 한다.

따라서 H1b가 완료했다는 말의 정확한 뜻은 다음과 같다.

> Proposition 6.1을 수치 부등식으로 다시 증명할 때 필요한 입력과 숨은 상수의 위치를 17개
> obligation으로 누락 점검 가능하게 고정했다. 아직 그 상수들의 실제 값을 계산하거나
> \(X_{\mathrm{cert}}\)를 얻은 것은 아니다.

쉬운 비유로 말하면, 설계도의 부품번호와 연결순서는 확인했지만 각 부품의 허용오차표가 빠져 있다.
허용오차표 없이 완제품이 어느 온도부터 안전하다고 계산할 수는 없다.

## 2. 감사한 원문과 범위

정본 원문은 James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
*Compositio Mathematica* 152 (2016), 1517–1554, arXiv:1405.2593이다.

감사 범위는 다음과 같다.

- Hypothesis 1의 세 분포 조건
- Theorem 3.1의 effectivity 문구
- Proposition 6.1의 parameter domain과 네 결론
- Section 7의 \(W\), \(R\), \(y_{\mathbf r}\), \(\lambda_{\mathbf d}\), \(w_n\) 구성
- Lemmas 8.1–8.6의 singular series, summation, coefficient, integral bound
- Propositions 9.1, 9.2, 9.4, 9.5와 Lemma 9.3의 moment 증명

H1b-1 후속 감사에서 Lemma 8.3의 정확한 하위 source가
Goldston–Graham–Pintz–Yıldırım의 *Small Gaps Between Products of Two Primes*, Lemma 4의
\(\kappa=1\) 특수화임을 확인했다. 후속 peer-reviewed 감사에서 Castillo et al.은 인쇄된
\(c_\gamma\)-relative 오류항이 추가 size condition 없이는 증명되지 않음을 지적했다.
Kuperberg는 HR Lemma 5.4 구조를 현대적으로 재현하지만 수치 multiplier·finite range를
주지 않는다. 따라서 source identity와 구조는 닫혔어도 행은 `RATE_MISSING`이며 closed로 승격하지 않는다.

## 3. Proposition 6.1에 실제로 인쇄된 parameter gate

Maynard의 표기를 따라 정리하면 다음 범위가 명시돼 있다.

| 항목 | 인쇄된 조건 | 숫자로 아직 필요한 것 |
|---|---|---|
| 기본 parameter | \(\alpha>0\), \(0<\theta<1\) | FGKMT/FMT에 대입할 구체값과 공통 slack |
| 선형식 계수 | \(|a_i|,|b_i|\le x^\alpha\) | 실제 form에서의 uniform constant |
| 차원 | \(k\le(\log x)^{1/5}\) | 다른 모든 조건과 동시인 최소 \(x\) |
| exceptional modulus | \(B\le x^\alpha\) | FGKMT가 제공할 실제 \(B\) package |
| sieve level | \(x^{\theta/10}\le R\le x^{\theta/3}\) | rounding과 support를 포함한 구체 \(R\) |
| roughness | \(k(\log\log x)^2/\log x\le\rho,\xi\le\theta/10\) | penalty를 목표 slack 아래로 만드는 값 |
| 최소 차원 | \(k\ge C(\alpha/\theta)\) | 숫자 \(C\) |

이 표에서 지수들이 explicit하다고 해서 Proposition 전체가 explicit한 것은 아니다. 마지막 열의
값과 아래 moment 상수들이 함께 필요하다.

## 4. 17개 obligation 요약

| 상태 | 행 수 |
|---|---:|
| `PARTIAL_EXPLICIT` | 1 |
| `PROJECT_FINITE_COMPONENT_CLOSED` | 2 |
| `RATE_MISSING` | 10 |
| `SOURCE_REVIEW_REQUIRED` | 0 |
| `INPUT_PACKAGE_MISSING` | 3 |
| `HARD_BLOCKER` | 1 |
| **합계** | **17** |

| ID | 원문 위치 | 역할 | 현재 판정 | 핵심 결손 |
|---|---|---|---|---|
| `H1B-P61-01` | Proposition 6.1 | parameter domain | `PARTIAL_EXPLICIT` | \(C(\alpha/\theta)\), 공통 최초 \(x\) |
| `H1B-HYP-01` | Hypothesis 1(1) | \(\mathcal A\) 분포 | `INPUT_PACKAGE_MISSING` | multiplier·시작점 |
| `H1B-HYP-02` | Hypothesis 1(2) | 선형식의 소수 분포 | `INPUT_PACKAGE_MISSING` | uniform multiplier·prime-density 하한 |
| `H1B-HYP-03` | Hypothesis 1(3) | progression 집중 방지 | `INPUT_PACKAGE_MISSING` | \(\ll\) 상수·시작점 |
| `H1B-L81` | Lemma 8.1 | singular series 하한 | `RATE_MISSING` | \(\exp(-Ck)\)의 \(C\) |
| `H1B-L82` | Lemma 8.2 | Lipschitz 오차 | `PROJECT_FINITE_COMPONENT_CLOSED` | H1b-1b에서 multiplier 89, \(k\ge2\) |
| `H1B-L83` | Lemma 8.3 | multiplicative sum | `RATE_MISSING` | application 제외모듈은 닫힘; \(C_{3,\mathrm{abs}}(A_1,A_2)\)·finite range 필요 |
| `H1B-L84` | Lemma 8.4 | 다차원 반복 합 | `RATE_MISSING` | 실제 \(A_1,A_2,L,\Omega_G\)·보정 반복 상수·smallness cutoff |
| `H1B-L85` | Lemma 8.5 | coefficient/weight 크기 | `RATE_MISSING` | \(R^{2+o(1)}\)의 finite 대체 |
| `H1B-L86-RATIO` | Lemma 8.6, (8.25)–(8.27) | 적분비 | `PROJECT_FINITE_COMPONENT_CLOSED` | 없음; H1a에서 \(k\ge36\) 닫음 |
| `H1B-L86-SIZE` | Lemma 8.6 | 절대 적분 크기 | `RATE_MISSING` | lower-bound multiplier |
| `H1B-P91` | Proposition 9.1 | zeroth moment | `RATE_MISSING` | 상대오차 multiplier·divisor sum |
| `H1B-P92` | Proposition 9.2 | prime moment | `RATE_MISSING` | 상대·additive error 상수 |
| `H1B-L93` | Lemma 9.3 | diagonal approximation | `RATE_MISSING` | \(F_2/F\)·오차 상수 |
| `H1B-P94` | Proposition 9.4 | extra-form/rough upper bound | `RATE_MISSING` | leading multiplier·singular factors |
| `H1B-P95` | Proposition 9.5 | 작은 소인수 penalty | `RATE_MISSING` | \(\ll\) multiplier·허용 margin |
| `H1B-COMP-01` | Sections 8–9 합성 | 하나의 finite package | `HARD_BLOCKER` | 모든 입력과 최대 cutoff |

기계 원장은 각 행의 `upstream`을 함께 저장한다. `H1B-COMP-01`은 나머지 16개 행 전부를
의존하므로, 일부 행만 닫고 Proposition 6.1 전체가 수치화됐다고 표시할 수 없다.

## 5. H1a가 해결한 것과 해결하지 않은 것

H1a는 simplex-supported test function에 대해

\[
\frac{J_k(F)}{I_k(F)}>\frac{\log k}{4k}\qquad(k\ge36)
\]

을 닫았다. 그래서 `H1B-L86-RATIO`에는 더 이상 모르는 \(O(1/\log k)\) 상수를 둘 필요가 없다.

그럼에도 Lemma 8.6에서 moment 주항의 **절대 크기**를 하한하는 상수, \(\lambda_{\max}\),
singular series, arithmetic-progression discrepancy, off-diagonal error는 별개다. 적분비가 좋다는
사실만으로 실제 finite weight moment의 주항이 모든 오차보다 크다는 결론은 나오지 않는다.

따라서 다음 추론은 금지한다.

```text
H1a PASS -> Proposition 6.1 numerical PASS -> FMT good weight PASS -> X_cert 계산 가능
```

정확한 현재 연결은 다음이다.

```text
H1a ratio component PASS
  + Lemmas 8.1-8.5 constants (OPEN)
  + Hypothesis 1 numeric package (OPEN)
  + Propositions 9.1-9.5 finite error composition (OPEN)
  = Proposition 6.1 numerical package (OPEN)
```

## 6. 왜 강한 로그 지수만으로는 부족한가

가령 어떤 오차가

\[
|E(x)|\le C(\log x)^{-1/10}M(x)
\]

이고 목표가 \(|E(x)|\le10^{-4}M(x)\)라면 필요한 조건은

\[
\log x\ge (10^4 C)^{10}
\]

이다. \(C=1\)과 \(C=10^{20}\)은 시작점을 상상하기 어려울 만큼 다르게 만든다. 여기에
\(k\), \(R\), \(B\), singular series가 얽힌 다른 오차를 더하면 가장 늦게 성립하는 조건이
전체 시작점을 결정한다. 그러므로 인쇄되지 않은 multiplier를 1로 놓는 “시험 계산”은
\(X_{\mathrm{cert}}\)의 증명이 될 수 없다.

## 7. H1b의 엄밀한 판정

### 확인된 긍정적 사실

1. weight는 finite sum의 제곱으로 주어져 symbolic하게 constructive하다.
2. Proposition 6.1이 필요로 하는 parameter와 moment의 구조를 추적할 수 있다.
3. Maynard는 Hypothesis 1 상수가 effective하면 자신의 상수도 effective하다고 명시한다.
4. H1a가 적분비 한 행을 실제 finite theorem으로 닫았다.

### 아직 닫히지 않은 핵심

1. Hypothesis 1 세 조건의 숫자 multiplier와 유효범위
2. singular series·multiplicative sums·divisor moments의 uniform 상수
3. Propositions 9.1–9.5의 모든 \(O/o/\ll\)를 finite 부등식으로 바꾸는 작업
4. 각 부등식의 error budget과 최초 \(x\)를 하나의 공통 cutoff로 합치는 작업

따라서 판정은

```text
CONSTANT_DEPENDENCY_LEDGER_COMPLETE_NUMERICAL_PACKAGE_OPEN
```

이다. 이는 Proposition 6.1이 틀렸다는 판정이 아니다. 출판된 정성적·effective-in-principle
증명을 numerical certificate로 바꾸려면 상당한 정량 재증명이 남았다는 판정이다.

## 8. 다음 proof gate

1. **H1b-1a 완료:** explicit smooth cutoff, Lemma 8.1(i)의 \(C=9/2\), 식 (8.5)의
   \(E(k)<24\log k\), parameterized divisor majorant를 고정했다.
2. **H1c-1:** FGKMT (7.2)–(7.3)의 character/Bombieri–Vinogradov package를 정량화한다.
3. **H1b-1b 진행:** Lemma 8.2는 multiplier 89로 닫혔고 교정된 GGPY Lemma 3→4
   절대오차 전달은 \(C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}\)로 정식화됐다.
   H1b-1b-2a.1은 actual-call 비제외 local factor와
   \(dW_i,W'_i,a_mWBr,rW_m,W_0\)의 호출별 overhead를 전수 인증해 공통
   \(\Lambda_*\)를 얻었다. 이제 Kuperberg/HR recurrence의
   \(C_{3,\mathrm{abs}}\)·유효범위와 실제 \(A_1,A_2,L\)을 복원한 뒤
   \(6C_{3,\mathrm{abs}}(1+\log\Lambda_*)\) 손실을 넣어 Lemma 8.4를 다시 합성한다.
4. **H1b-2:** 위 입력을 받은 뒤 Propositions 9.1–9.5를 지정 error budget으로 재증명한다.
5. **H1d:** FMT/FGKMT의 \(u\), good-event, covering 단계와 공통 \((r,x)\) slack을 합성한다.

H1b-1/H1c source trace와 H1b-1a의 세 finite component는 완료됐지만 numerical package는
계속 열려 있다. H1b-1b와 H1c-1은 논리적으로 병렬 조사할 수 있다. H1b-2는 두 입력 없이
수치화할 수 없다.
이 단계가 끝날 때까지 threshold calculator와 장시간 prime sweep을 만들지 않는다.

## 9. 검증 계약

`tests/test_h1b_maynard_constant_ledger.py`는 다음을 fail-closed로 확인한다.

- 17개 obligation ID와 dependency가 유효하고 중복이 없는가
- Hypothesis 1(1)–(3), Propositions 9.1, 9.2, 9.4, 9.5와 Lemma 9.3이 빠지지 않았는가
- missing constant가 있는 행이 closed 상태로 잘못 표시되지 않았는가
- H1a와 Lemma 8.2 component가 닫혀도 `SIV-07`, `SIV-09`, 전체 weight와
  \(X_{\mathrm{cert}}\)가 false인가
- common-cutoff 행이 나머지 16개 행 전부를 의존하고 `HARD_BLOCKER`인가

이 검증은 문서의 내부 정합성을 검사한다. Maynard의 정리를 독립 재증명하거나 수치 상수를
계산하는 실험은 아니다.

## 10. 2026-09-04 H1b-1 source 감사 반영

H1b-1은 Lemmas 8.1–8.4를 13개 하위 node로 분해했다. source chain은 추적됐지만 숫자 상수표는
얻지 못했다. 특히 다음이 남는다.

- Lemma 8.1의 \(\exp(-Ck)\)에서 실제 \(C\)
- 고정 smooth cutoff의 식과 derivative norm
- GGPY Lemmas 3–4 및 Halberstam–Richert에서 오는 multiplier
- Lemma 8.4의 \(r\)-fold error smallness와 common cutoff

따라서 parent 원장의 상태 이동은 오직 다음 하나다.

```text
H1B-L83: SOURCE_REVIEW_REQUIRED -> RATE_MISSING
```

이는 source 이름을 찾았다는 뜻이며 numerical closure가 아니다. `SIV-07`, `SIV-09`와
\(X_{\mathrm{cert}}\)는 그대로 `OPEN`이다.

## 11. 2026-09-06 H1b-1b 반영

H1b-1b는 H1b-1a에서 고정한 \(\|\psi'\|_\infty<50\)을 Maynard Lemma 8.2의
모든 인자에 직접 전파해 두 부분 모두에 uniform multiplier 89를 증명했다. 따라서
`H1B-L82`는 `PROJECT_FINITE_COMPONENT_CLOSED`로 이동한다.

GGPY Lemma 4의 \(\kappa=1\) 부분적분은 하위 Lemma 3의 **절대오차** multiplier를
\(C_{3,\mathrm{abs}}(A_1,A_2)\)라고 할 때
\(C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}\)로 명시됐다. Castillo et al.의 교정 때문에
Maynard에 인쇄된 \(c_\gamma\)-relative 형태에는 별도 \(c_\gamma\) 하한 또는 명시적
\(z\)-대-\(L\) gate가 필요하다. Kuperberg의 현대 HR 구조 재현에도 숫자 상수와 공통
finite range는 없다. 따라서 `H1B-L83`, `H1B-COMP-01`,
`SIV-07`과 \(X_{\mathrm{cert}}\)는 승격하지 않는다.

## 12. 2026-09-07 H1b-1b-2a·2a.1 반영

Maynard Section 8에서 실제 Lemma 8.4에 들어가는 prime-local denominator를 원정의까지
추적하면 네 family 모두 \(0<g(p)\le p-a(p)\)를 만족한다. 비제외 소수에서는 현재
좌표가 사용 가능하므로 \(n_j(p)\le a(p)-1\)이고, 해당 local factor는 정확히 1 이상이다.
제외 소수는 유효 \(Q_j=\widetilde W_{j+1}\prod_{i=j+2}^{r}e_i\)에 합쳐

\[
c_{\gamma,j}\ge\frac{\varphi(Q_j)}{Q_j}
>
\frac{1}{3(1+\log\Lambda_*)}
\]

로 하한화할 수 있다. H1b-1b-2a.1은 10개 source call을 11개 analytic
subapplication으로 분해하고, 모든 호출·iteration에서
\(\log Q_j\le\Lambda_*\)를 인증했다. 따라서 local normalization 경로는 추적된
actual call 전체에 대해 project-parameterized explicit 상태로 닫혔다.

또한 숫자 \(C_{3,\mathrm{abs}}\), 그 finite range, 실제 \(A_1,A_2,L\), 그리고
\(r\)-회 보정 합성은 아직 없다. 따라서 `H1B-L83`, `H1B-L84`, `H1B-COMP-01`,
`SIV-07`, \(X_{\mathrm{cert}}\)의 상태는 바뀌지 않는다.
