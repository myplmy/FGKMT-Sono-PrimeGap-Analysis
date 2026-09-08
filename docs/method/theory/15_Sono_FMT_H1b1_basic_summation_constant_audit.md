# Sono/FMT H1b-1 기본 summation 상수 감사

- 작성: 2026-09-04 KST
- 증거 수준: `SOURCE-LEVEL QUANTITATIVE DEPENDENCY AUDIT`
- 판정: `CORRECTED_KAPPA1_ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT_RFOLD_PACKAGE_OPEN`
- `SIV-07`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1b1_basic_summation_constants_v1.json`](data/Sono_FMT_H1b1_basic_summation_constants_v1.json)
- H1b-1a 후속 정식화:
  [`17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md`](17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md)
- H1b-1b multiplier 복원:
  [`18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md`](18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md)
- H1b-1b-2a actual-call local-factor·제외모듈 하한:
  [`20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md`](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
  및 [`21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md`](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)
- H1b-1b-2b 교정된 kappa=1 multiplier:
  [`22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md`](22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md)
- H1b-1b-2c actual 입력 특수화:
  [`23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md`](23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md)

## 1. 결론부터

Maynard의 Lemmas 8.1–8.4에는 Proposition 6.1의 moment 계산을 가능하게 하는 기본 합 공식이
들어 있다. 이번 감사에서는 그 식들이 어디서 오고 어떤 숨은 상수를 쓰는지 13개 하위 의무로
분해했다.

긍정적인 결과는 두 가지다.

1. Lemma 8.3의 인용 원문과 정확한 특수화가 확인됐다. 인용 논문은
   Goldston–Graham–Pintz–Yıldırım의 *Small Gaps Between Products of Two Primes*이고,
   Maynard는 그 논문의 Lemma 4를 \(\kappa=1\)로 사용한다.
2. 각 숨은 상수는 계산 불가능한 추상적 대상이라기보다, explicit cutoff 함수·소수곱·미분
   norm·한 차원 summation error를 정량적으로 다시 증명하면 얻을 수 있는 대상으로 보인다.

2026-09-04 H1b-1a 후속 정식화는 Lemma 8.1(i)의 \(C=9/2\), explicit cutoff의
\(\|\psi'\|_\infty<50\), 식 (8.5)의 \(E(k)<24\log k\)를 프로젝트 유한 보조정리로
닫았다. 2026-09-06 H1b-1b는 이어서 Lemma 8.2의 전체 Lipschitz multiplier를 89로
닫았다. Castillo et al. 교정을 반영한 Lemma 8.3/GGPY Lemma 4의 안전한 전달식은
\(C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}\)이다. 2026-09-07 H1b-1b-2a는
Maynard Section 8의 추적된 실제 호출에서 비제외 local factor를 닫고, 이어진
H1b-1b-2a.1은 11개 analytic subapplication의 확대 제외모듈을 전수 인증했다.
따라서 추적 호출 전체에서 uniform parameterized \(c_{\gamma,j}\) 하한 경로가 닫혔다.
H1b-1b-2c는 실제 네 family에 공통인
\(a=1/2,A_2=8,L=5+\log\Lambda_*\)도 인증했다. Lemma 8.1(ii)의 입력 정규화와
공통 cutoff는 열려 있다. H1b-1b-2d는 7개 smooth Lemma 8.4 call의 support norm과
보정 finite-product 반복오차를 닫았다. 후속 2d.1a는 905행 전역 \(H\)의 \(C^1\)
요구를 우회했으나, source scalar multiplier와 sharp \(\xi\) scale은 열려 있다. 절대
\(C_{3,\mathrm{abs}}(A_1,A_2)\) 경로는 보조 교차검사로 남는다.
따라서 numerical basic-summation package 전체는 아직 완료가 아니다.

쉬운 비유로 말하면, 네 개의 조립 공정과 공급업체 도면까지 찾았지만 각 부품의 실제 허용오차와
조립 온도 범위는 아직 숫자로 써 있지 않다. 공급업체 이름을 찾았다는 이유만으로 완제품 인증을
내릴 수는 없다.

## 2. 감사 범위와 정본 source

정본은 James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
*Compositio Mathematica* 152 (2016), 1517–1554이다. arXiv 식별자는
[`1405.2593`](https://arxiv.org/abs/1405.2593)이다.

Lemma 8.3의 하위 source는 다음이다.

- D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yıldırım,
  [*Small Gaps Between Products of Two Primes*](https://doi.org/10.1112/plms/pdn046),
  *Proceedings of the London Mathematical Society* 98 (2009), Lemmas 3–4.
- 같은 논문의
  [corrigendum](https://doi.org/10.1112/plms/pds053)도 존재한다. 공개된 정정 범위만으로
  Lemma 4의 숫자 multiplier가 제공된다고 볼 수 없으므로, 정량 재증명 시 본문과 정정문을 함께
  대조해야 한다.
- GGPY Lemma 3은 Halberstam–Richert, *Sieve Methods*의 Lemmas 5.3–5.4를 하위 근거로 든다.
  이 책의 상수를 프로젝트용 숫자로 재구성하는 일은 아직 하지 않았다.

기존 H1b 원장의 source 제목 `Small gaps between primes or almost primes`는 잘못된 식별이었다.
이번에 올바른 논문명과 DOI로 정정한다.

## 3. Lemma별 감사 결과

### 3.1 Lemma 8.1: singular series와 extra-form 평균

Lemma 8.1(i)의 하한은 대략 다음 두 부분을 곱한다.

```text
p <= 2k의 유한 소수곱
times
p > 2k의 tail product
```

작은 소수 부분은 유한하므로 원칙적으로 exact rational 또는 directed interval로 계산할 수 있다.
큰 소수 부분에서는 로그를 전개한 뒤 \(O(k^2/p^2)\)를 합쳐 \(\exp(-Ck)\)를 얻는다. 여기서
전개 remainder의 multiplier와 소수 제곱 역수 tail의 explicit bound가 필요하다. 논문은 최종
숫자 \(C\)를 주지 않는다.

Lemma 8.1(ii)는 인접한 추가 선형식에 대해

\[
\frac{\Delta}{\varphi(\Delta)}
\]

의 평균을 제어한다. 증명은 \(\Delta/\varphi(\Delta)\), 소인수 합, Euler product와
\(o(\eta\log x)\) 흡수를 사용한다. 각 단계는 explicit한 초등 부등식으로 바꿀 후보가 있지만,
현재 source만으로 multiplier와 흡수 시작점을 읽을 수는 없다.

판정은 `CONSTRUCTIVE_SUBPROBLEM` 또는 `RATE_MISSING`이다.

### 3.2 Lemma 8.2: cutoff 함수와 Lipschitz 상수

논문은 \([0,1]\)에 지지되고 \([0,9/10]\)에서 1인 고정 smooth 함수 \(\psi\)를 사용한다.
하지만 \(\psi\)의 실제 식이나 도함수 sup norm은 고정하지 않는다. 따라서

\[
y_{\mathbf s}=y_{\mathbf r}
 +O\!\left(T_kY_{\mathbf r}\frac{\log A}{\log R}\right)
\]

에서 \(O\) 앞 숫자를 계산할 수 없다.

이 결손은 비교적 구체적이다. 프로젝트가 explicit \(C^\infty\) cutoff를 하나 선택하고,
필요한 모든 미분 norm과 support를 interval arithmetic으로 인증하면 입력을 만들 수 있다.
다만 cutoff를 선택하는 것만으로 Lemma 8.2 전체가 자동 증명되는 것은 아니며, 증명 전체에서 그
norm이 어떻게 증폭되는지를 다시 추적해야 한다.

### 3.3 Lemma 8.3: 한 차원 multiplicative summation

출판본의 형식은 조건

\[
0\le \frac{\gamma(p)}p\le1-A_1
\]

및 소수합 discrepancy가 \(A_2,L\)로 제어될 때, 주항에 더해 대략

\[
O_{A_1,A_2}\!\left(c_\gamma(1+L)G_{\max}\right)
\]

의 error를 준다. 이 결과는 GGPY Lemma 4의 \(\kappa=1\) 특수화다.

출판본에는 중요한 version-control 주석이 있다. 일반 \(\kappa\)에는
\(c_\gamma(L+1)^\kappa\) 형태의 항이 추가로 필요하지만, Maynard가 실제로 쓰는
\(\kappa=1\)에는 문제가 없다고 설명한다. 따라서 오래된 arXiv 표현만 보고 일반화하면 안 되고,
출판본을 정본으로 삼아야 한다.

하지만 이 확인은 error multiplier의 숫자를 주지 않는다. GGPY Lemma 4의 implied constant는
\(A_1,A_2,\kappa\)에 의존하며, 그 증명은 다시 Lemma 3과 Halberstam–Richert 결과를 사용한다.
따라서 parent H1b의 `H1B-L83`은 “source 미확인”에서는 벗어나지만 “수치 rate 누락” 상태다.

```text
기존: SOURCE_REVIEW_REQUIRED
정정: RATE_MISSING
```

이는 진전이지만 closure는 아니다.

### 3.4 Lemma 8.4: r회 반복 합성

Lemma 8.4는 Lemma 8.3을 \(r\)번 적용한다. 논문에는 다음 구조가 보인다.

- \(r\le k\ll(\log R)^{1/5}\)
- \(W_i\le R^{O(k)}\)
- \(g(p)=p+O(k)\)
- total relative error의 기본 크기
  \(r\Omega_G\log\log R/\log R\)

그러나 실제 숫자를 내려면 다음을 모두 알아야 한다.

1. \(g(p)=p+O(k)\)와 \(W_i\)의 multiplier·지수
2. Lemma 8.3에 넣을 특정 \(A_1,A_2,L\)
3. 선택한 test function의 \(\Omega_G\)
4. \((1+O(\varepsilon))^r\)를 \(1+O(r\varepsilon)\)로 바꾸는 정확한 smallness 조건
5. 위 조건이 동시에 성립하는 최초 \((k,R)\)

따라서 “error가 0으로 간다”는 사실은 확인되지만, “어느 \(R\)부터 목표 error보다 작다”는
finite 명제는 아직 없다.

## 4. 13개 obligation 요약

| ID | 대상 | 상태 | 남은 핵심 |
|---|---|---|---|
| `H1B1-L81-SMALL` | 작은 소수곱 | `PROJECT_FINITE_COMPONENT_CLOSED` | \(>e^{-4k}\) |
| `H1B1-L81-TAIL` | 큰 소수 tail | `PROJECT_FINITE_COMPONENT_CLOSED` | \(>e^{-k/2}\) |
| `H1B1-L81II-DIVISOR` | extra-form 평균 | `PARTIAL_EXPLICIT` | 입력 계수·공통 흡수 cutoff |
| `H1B1-L82-CUTOFF` | smooth \(\psi\) | `PROJECT_FINITE_COMPONENT_CLOSED` | \(\|\psi'\|_\infty<50\) |
| `H1B1-L82-LIPSCHITZ` | Lipschitz bound | `PROJECT_FINITE_COMPONENT_CLOSED` | multiplier 89, \(k\ge2\) |
| `H1B1-L83-GGPY4` | 1차원 합 | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | 교정 multiplier와 공통 \(a=1/2,A_2=8,L=5+\log\Lambda_*\) |
| `H1B1-L83-PUBLISHED-NOTE` | 출판본 보정 | `PRINTED_STRUCTURAL_FACT` | 일반 \(\kappa\) 주석은 별도 \(c_\gamma\) 문제를 해결하지 않음 |
| `H1B1-L83-GGPY3` | 하위 sieve lemma | `PROJECT_PARAMETERIZED_EXPLICIT_CORRECTED_KAPPA1` | 교정된 \(\kappa=1\) 상수와 전 범위 \(z\ge2\) |
| `H1B1-L84-GAMMA` | \(\gamma\) 조건 | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | 실제 네 family에 공통인 \(a=1/2,A_2=8\), \(k\ge2\) |
| `H1B1-L84-L` | discrepancy \(L\) | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | \(L=5+\log\Lambda_*\) |
| `H1B1-L84-SMOOTH` | \(\Omega_G\) | `RATE_MISSING` | test function 수치 norm |
| `H1B1-L84-ITERATION` | \(r\)-fold 합성 | `RATE_MISSING` | 축적오차·공통 range |
| `H1B1-PACKAGE` | 기본 합 package | `HARD_BLOCKER` | 전 행과 공통 error budget |

모든 행의 `threshold_ready`는 `false`다.

## 5. 무엇이 가능하고 무엇이 아직 불가능한가

### H1b-1a에서 완료한 일

- explicit smooth cutoff와 첫 derivative norm을 고정
- Dusart 및 Rosser–Schoenfeld의 explicit prime-product/totient 부등식을 1차 출처에서 선정
- Lemma 8.1(i)의 small-prime product와 tail을 \(e^{-9k/2}\)로 정식화
- Lemma 8.1(ii)의 식 (8.5) Euler product와 parameterized finite majorant를 정식화

### 다음 단계에서 Codex와 사용자가 도울 수 있는 일

- 인증된 실제 \(a,A_2,L\)과 \(C_{8.3}(1/2,8)\)을 smooth norm에 결합
- Kuperberg/HR의 absolute \(C_{3,\mathrm{abs}}\) 경로는 필요할 때 sharpness 교차검사로 복원
- \(c_\gamma\) explicit lower bound 또는 \(z\)-대-\(L\) restoration gate를 증명
- 이미 닫힌 Lemma 8.2 multiplier 89와 absolute factor 2를 Lemma 8.4 축적오차에 재합성
- 정식 lemma가 고정된 뒤 작은 \(k,R\) 범위의 exact/interval certificate를 생성

이는 새 maximal-gap sweep이 아니라 보조 부등식 certificate 계산이다. runner는 정식 lemma와
검증 범위가 먼저 동결된 뒤에만 만드는 편이 안전하다.

### 현재 할 수 없는 주장

- Lemmas 8.1–8.4가 특정 숫자 \(x\)부터 모두 성립한다는 주장
- Proposition 6.1의 moment error multiplier가 얻어졌다는 주장
- `SIV-07`, `SIV-09`, good weight 또는 \(X_{\mathrm{cert}}\)의 closure

## 6. H1b-1a 결과와 다음 gate

H1b-1a는 세 유한 component를 닫고 divisor 평균을 parameterized 식으로 바꿨다. H1b-1b
전반은 Lemma 8.2 multiplier 89와 GGPY **절대오차** 전달 factor 2를 닫았다.
H1b-1b-2a.1은 실제 호출별 비제외 local factor와 제외 소수곱의 exact 변환에 더해
\(dW_i,W_i',a_mWBr,rW_m,W_0\)를 포함한 11개 subapplication의 상계를 전수
인증했다. 공통 상계 \(\Lambda_*\)와 uniform parameterized \(c_\gamma\) 하한을 얻었지만,
아래 합성은 계속 열려 있다.

1. 실제 test function에서 \(\Omega_G\)와 각 derivative/integral norm을 명시한다.
2. \(C_{8.3}(1/2,8)\{6+\log\Lambda_*\}\)를 사용해 Lemma 8.4의
   corrected \(r\)-fold error를 합성한다.
3. 한 공통 \((k,R)\) smallness cutoff를 도출한다.

원 HR 140–153쪽은 계보와 상수 누락을 대조하는 데 여전히 유용하지만, 현대 구조 재현이
확보됐으므로 사용자 제공이 유일한 선결조건은 아니다.

```text
실행 환경·명령어: 없음
사용자 절차: 합법적으로 보유한 해당 쪽의 PDF·스캔·사진을 대화에 첨부하거나
             프로젝트 경로를 알려 준다.
```

## 7. 엄밀한 최종 판정

```text
H1b-1 source chain          = TRACED
H1b-1a finite components    = 3 CLOSED
H1b-1b Lemma 8.2            = multiplier 89 CLOSED
GGPY Lemma 4 absolute       = C4_abs <= 2 C3_abs PARAMETERIZED
printed c_gamma-relative    = EXTRA CONDITION REQUIRED
modern HR reproduction      = STRUCTURE REVIEWED / RATE MISSING
Lemma 8.1(i) exponent       = 9/2
cutoff first-derivative norm= <50
Lemma 8.3 cited source      = IDENTIFIED_AND_CORRECTED
numerical multiplier table = PARTIAL / BASE OPEN
application exclusions      = ALL 11 TRACED SUBAPPLICATIONS CLOSED
common finite cutoff       = OPEN
SIV-07                     = HARD_BLOCKER
X_cert                     = OPEN
```

이번 감사가 보여 준 것은 “정량화할 경로가 없다”가 아니라 “어느 하위 부등식을 숫자로 다시
증명해야 하는지 알게 됐다”는 것이다. 모르는 multiplier를 1로 두지 않았기 때문에 임계값 숫자는
계산하지 않는다.

## 8. 2026-09-08 교정된 base-rate 갱신

위의 `BASE OPEN` 판정과 \(C_{3,\mathrm{abs}}\) 우선순위는 당시 사용하던
절대오차 repair 경로의 기록이다. 최신 정본 H1b-1b-2b는 Ford Theorem 4.4의
추가항을 보존한 \(\kappa=1\) 상대오차를 직접 명시화했다. 현재 상태는 다음과 같다.

```text
Lemma 8.3 corrected one-step rate = C_L83(a,A2), every z>=2
actual common a,A2,L             = 1/2, 8, 5+log(Lambda_star) CLOSED PARAMETERIZED
legacy C3_abs + c_gamma route    = OPTIONAL CROSS-CHECK
Lemma 8.4 smooth subpackage      = 7/9 PROJECT PARAMETERIZED EXPLICIT
Lemma 8.4 line-905 C1 bypass     = PROJECT EXPLICIT
Lemma 8.4 scalar/sharp remainder = OPEN
SIV-07 / X_cert                  = HARD_BLOCKER / OPEN
```

H1b-1b-2c가 실제 호출 전체에 공통인 \(a,A_2,L\)을 인증했고, H1b-1b-2d가
smooth 하위 package를 닫았다. H1b-1b-2d.1a는 905행의 전역 \(H\) \(C^1\)
majorant 요구를 square-sum으로 우회했다. 다음 직접 gate는 source 986--999행의
scalar multiplier를 복원하는 H1b-1b-2d.1a.1과 sharp \(\xi\log x\) finite scale의
H1b-1b-2d.1b다.

## 9. 2026-09-08 H1b-1b-2d 반영

교정된 Lemma 8.3 one-step bound를 서로 다른 support의 비음수 profile에 적용해
\(\prod_i(1+\delta_i)-1\)로 합성했다. actual \(N,W,N^2,W^2,NW\) norm과
smallness 충분조건도 명시했다. \(F_2^2\)에서는 support-\([0,2]\) 좌표를 먼저
합해야 theory 23의 \(\Lambda_*\)를 그대로 쓸 수 있다는 순서 조건을 추가했다.

이 결과는 product-profile integral 기준의 절대오차 envelope다. actual coupled main
integral 자체에 대한 상대오차라고 확장하지 않는다. 또한 line-905 scalar multiplier와 sharp scale이
남아 있으므로 H1b-1 basic summation package 전체 및 `SIV-07`은 닫히지 않았다.

## 10. 2026-09-08 H1b-1b-2d.1a 반영

격자점별 \(|Z-A|\le\varepsilon B\)를
\(|Z^2-A^2|\le2\varepsilon AB+\varepsilon^2B^2\)로 옮기면 \(A^2,AB,B^2\)가
일곱 비음수 smooth tensor class로 전개된다. 따라서 line 905에서 전역 \(H\)의
\(C^1\) norm은 필요하지 않다.

반면 \(\varepsilon\)의 수치값을 주는 source 986--999행의 숨은 \(\ll\) multiplier와
finite range는 OPEN이다. 조건부 evaluator가 임의의 \(\varepsilon\)을 받을 수 있다는
사실은 source certification이 아니다. 따라서 H1b-1 package, `SIV-07`과
\(X_{\mathrm{cert}}\)는 승격하지 않는다.
