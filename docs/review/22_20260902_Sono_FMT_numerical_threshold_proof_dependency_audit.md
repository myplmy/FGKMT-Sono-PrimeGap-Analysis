# Sono/FMT numerical-threshold 증명 의존성 감사

- 작성: 2026-09-02 KST
- 목적: Sono의 (k=1) 부등식에서 `sufficiently large X`를 실제 숫자 (X_0)로
  바꾸려면 무엇을 추가로 증명·수치화해야 하는지 분해한다.
- 감사 수준: 원문 정리·증명 구조의 1차 dependency audit
- 이번 문서가 하지 않는 것: numerical (X_0) 주장, 새 정리 증명, 실제 prime-gap 전수 계산

## 1. 한눈에 보는 판정

결론부터 말하면 다음과 같다.

> Sono 논문은 (2.0\times10^{-17})이라는 **계수**를 명시했지만, 그 부등식이 보장되기 시작하는
> **숫자 (X_0)**는 명시하지 않았다. Ford–Maynard–Tao(FMT)의 proof는 ineffective한
> Siegel 정리를 피했으므로 원칙적으로 계산 가능한 `effective` proof이지만, 출판된 식에 숫자 몇
> 개를 대입하는 것만으로 (X_0)가 나오지는 않는다.

현재 상태는 다음과 같이 분류해야 한다.

| 질문 | 현재 답 |
|---|---|
| 상수 (2.0\times10^{-17})이 증명된 값인가 | 예 |
| Sono/FMT proof가 원리상 effective인가 | 예; 원문이 명시하고 exceptional zero를 제거함 |
| 출판본에 바로 쓸 numerical (X_0)가 있는가 | 아니오 |
| 현재 문헌만 읽고 단순 대입으로 (X_0)를 계산할 수 있는가 | 아니오 |
| 수치화가 논리적으로 불가능하다고 판정됐는가 | 아니오 |
| 완전한 수치 proof가 작은 작업인가 | 아니오; 여러 선행정리의 정량적 재증명이 필요할 수 있음 |

따라서 연구 방향은 타당하다. 다만 첫 목표는 “(X_0) 계산”이 아니라 **누락 없는 explicit
inequality chain을 만드는 것이 가능한지** 확인하는 proof-engineering 단계여야 한다.

## 2. 서로 다른 세 threshold

### 2.1 유한 관측 threshold

고정된 검증 상한 (B) 안에서만

\[
X_{\mathrm{emp}}(B)=
\min\{x_0:H(x)\ge 2\times10^{-17}\ \text{for every integer }x_0\le x\le B\}
\]

를 정의한다. P003의 exact 결과는 분석 정의역
`[3,814,280,10^20]`에서 부등식이 계속 성립했으므로

```text
X_emp(10^20) = 3,814,280
```

이다. 이는 그 유한 표에서의 첫 점일 뿐이다.

### 2.2 증명이 보장하는 numerical threshold

\[
X_{\mathrm{cert}}:
\quad G_1(X)\ge 2\times10^{-17}F(X)
\quad\text{for every }X\ge X_{\mathrm{cert}}
\]

를 실제 숫자로 증명하는 것이 이번 이론축의 목표다. Sono는 존재를 보이지만 값을 주지 않는다.

### 2.3 실제 가장 작은 전역 threshold

\[
X_\star=
\min\{x_0:G_1(X)\ge2\times10^{-17}F(X)\ \text{for every }X\ge x_0\}
\]

는 실제 소수 전체의 성질이다. (X_{\mathrm{cert}})를 얻어도 보통 (X_\star\le X_{\mathrm{cert}})라는
상한만 얻는다. 실제 최소값을 결정하려면 그 아래의 모든 relevant maximal-gap interval도
exhaustive하게 닫아야 한다.

따라서 `3,814,280`, (X_{\mathrm{cert}}), (X_\star)를 같은 숫자로 부르면 안 된다. 현재는 첫째만
유한 범위에서 알려졌고 나머지 둘은 `OPEN`이다.

## 3. 원문 계보와 경계가 맞는가

### Sono 2025

Sono는

\[
G_k(X)=\max_{p_{n+k}\le X}\min\{p_{n+1}-p_n,\ldots,p_{n+k}-p_{n+k-1}\}
\]

를 사용한다(pp. 521–522). (k=1)이면 프로젝트 정본인 end-bounded (G_1(X))와 정확히 같다.
Theorem 3.6(p. 527)은 FMT chain theorem의 explicit version이다.

### Ford–Maynard–Tao 2018

FMT Theorem 1(p. 2)은 고정 (k\ge1)에 대해 충분히 큰 (X)에서

\[
G_k(X)\gg \frac1{k^2}F(X)
\]

를 주고 implied constant가 absolute·effective라고 명시한다. Section 2는 ineffective한
Siegel theorem을 쓰지 않고, Landau–Page theorem으로 가능한 exceptional character의 소인수
하나를 제거한다.

따라서 이번 threshold 감사의 직접 계보는

```text
FMT Chains of large gaps -> Sono explicit coefficient -> project end-bounded k=1
```

이다. FGKMT 5인 `Long gaps between primes`는 같은 scale의 중요한 별도 결과지만 Sono가 직접
수치화한 정리의 원문은 아니다.

## 4. 최종 상수는 얼마나 명시적인가

Sono Theorem 3.6(p. 527)의 계수식은 다음 곱형 분모를 갖는다.

\[
\boxed{
\widehat c=
\frac{
C_{\mathrm{PAP}}^2\theta c_{I,J}e^{4\gamma}}
{737280000\log5\;C_{\mathrm{UB}}M
\,(1+D_{\mathrm{PAP}}^{-1})^4
\,(25C_{\mathrm{UB}}+20e^\gamma M)}
}
\]

여기서 줄을 나눠 쓴 세 분모 요인은 모두 곱셈이다. 코드 형태로 쓰면 다음과 같다.

```text
numerator /
(737280000 * log(5) * C_UB * M
 * (1 + 1/D_PAP)^4
 * (25*C_UB + 20*exp(gamma)*M))
```

재현 명령은 고정 FGKMT Python의 `mpmath` 80자리에서 위 식을 그대로 평가한다. 계산 중
float64로 내리지 않는다.

여기에는 다음을 대입한다.

\[
\theta=\frac13,\quad c_{I,J}=\frac14,\quad
C_{\mathrm{PAP}}=1-e^{-2},\quad D_{\mathrm{PAP}}=160,
\]

\[
C_{\mathrm{UB}}=8e^{2\gamma},\quad M=160.
\]

80자리 `mpmath`로 원문 한 줄 곱셈식을 직접 계산하면

\[
\widehat c
=2.00386120461967036975\ldots\times10^{-17}.
\]

따라서 (2.0\times10^{-17})은 이를 아래로 둥글린 안전한 표기다. 두 값 사이의 상대 여유는

\[
1-\frac{2.0\times10^{-17}}{\widehat c}
=0.00192688226648\ldots,
\]

즉 약 `0.192688%`다.

이 마지막 반올림 여유가 모든 (o(1))의 전체 예산이라고 바로 단정할 수는 없다. Sono가 앞 단계의
분모 12800, 1800 등에서 이미 별도 안전 여유를 배정했을 수 있기 때문이다. 그러나 numerical
proof를 만들 때는 각 안전 여유의 출처와 소비량을 정확히 추적해야 한다. `o(1)`을 단순히 0으로
놓는 것은 금지한다.

## 5. 증명 dependency graph

```text
목표: G_1(X) >= 2e-17 F(X) for every X >= X_cert
|
+-- A. Sono Theorem 3.6 최종 계수와 k=1 특수화
|   +-- theta=1/3, c_IJ=1/4
|   +-- C_PAP=1-e^-2, D_PAP=160
|   +-- C_UB=8e^(2 gamma), D_UB>0, M=160
|
+-- B. PAP: 큰 modulus 산술진행의 prime lower bound
|   +-- McCurley explicit zero-free region
|   +-- Gallagher zero-density/PNT-in-AP argument
|   +-- Jutila zero-density exponent c_ZD=16
|   +-- psi -> pi 변환과 x >= q^160의 유효 범위
|
+-- C. UB: 두 선형식이 동시에 prime일 upper bound
|   +-- Halberstam-Richert Selberg upper-bound sieve
|   +-- Mertens/PNT 및 error term
|
+-- D. FMT covering과 Sono Proposition 3.1
|   +-- smooth-number remainder R=o(x/log x)
|   +-- random construction과 hypergraph covering
|   +-- 각 probability 1-o(1)의 정량적 합성
|
+-- E. multidimensional sieve weight
|   +-- FMT Theorem 6 / Maynard Dense clusters
|   +-- sufficiently small c0, sufficiently large r0
|   +-- tau >= x^-o(1), u asymp log r, finite-r integral error
|
+-- F. x-domain construction을 arbitrary X로 변환
    +-- P(x)=product_{p<=x} p의 explicit 상하한
    +-- Z=P^M, endpoint <= exp(1.5 M x)
    +-- y를 F(X)로 바꾸는 반복로그 explicit inequalities
    +-- 모든 X>=X_cert를 빈틈없이 덮는 parameter choice
```

## 6. node별 감사

| node | 원문에서 명시된 것 | numerical threshold에 빠진 것 | 판정 |
|---|---|---|---|
| A 최종 계수 | Theorem 3.6 식, 6개 parameter 값 | 각 asymptotic error가 충분히 작아지는 (x) | `NUMERIC_COEFFICIENT_ONLY` |
| B1 zero-free | McCurley (R=9.6459\ldots), exceptional zero 최대 하나 | 뒤 단계의 모든 implied constant와 결합한 유효범위 | `PARTLY_EXPLICIT` |
| B2 PAP | (C_{PAP}=1-e^{-2},D_{PAP}=160) | Gallagher/Jutila의 `\ll`, `O_\le`, (1+o(1)) 수치화; \(\psi\to\pi\) 오차 | `RATE_MISSING` |
| C UB | (C_{UB}=8e^{2\gamma}), 임의 (D_{UB}>0) | sieve error의 implied constant, Mertens/PNT threshold, `log x=o(log Z)`의 수치범위 | `RATE_MISSING` |
| D covering | 12800, 1800, 5 등 주요 계수 | smooth remainder, union bound, probability failure의 explicit rate | `RATE_MISSING` |
| E sieve weight | 일부 오류가 `1/log_2^j x` 형태 | (c_0,r_0), (x^{-o(1)}), `\asymp`, finite-r integral 수치범위 | `MAJOR_BLOCKER` |
| F x→X | (M=160), (X\le e^{1.5Mx}) 형태 | primorial·반복로그의 양방향 explicit 변환, arbitrary-X coverage | `MAJOR_BLOCKER` |

### 6.1 PAP는 상수만 explicit하고 threshold는 아니다

Sono Section 5는 McCurley의 explicit zero-free region을 사용하고 Jutila의 zero-density estimate를
통해 (c_{ZD}=16)을 택한 뒤 (D_{PAP}=160)을 얻는다. 그러나 p. 537에는 여전히

```text
principal contribution = (1+o(1)) x/phi(q)
non-principal contribution = O_<= (x e^{-aD}/phi(q))
```

가 남는다. 여기서 (O_\le)도 “모든 충분히 큰 x에서”라는 Sono의 정의를 사용한다. 숫자 160은
modulus exponent를 정한 것이지, 그 부등식이 시작되는 실제 (x)를 정한 것이 아니다.

### 6.2 UB에도 숨은 유효범위가 있다

Section 4의 (C_{UB}=8e^{2\gamma})은 명시적이지만, Halberstam–Richert sieve error,
Mertens formula, (P(x)\sim e^x), `log x=o(log Z)`가 모두 특정 오차 이하가 되는 수치범위가
필요하다. 상한은 보수적으로 잡기 쉬울 수 있지만, 하나라도 숫자가 없으면 전체 (X_0) certificate는
닫히지 않는다.

### 6.3 가장 큰 병목은 FMT/Maynard의 확률·sieve weight 층이다

FMT Theorem 6(p. 11)는

```text
sufficiently small absolute c0
sufficiently large absolute r0
tau >= x^{-o(1)}
u asymp log r
```

를 사용한다. Sono는 (r=\lfloor(\log x)^{1/5}\rfloor)를 선택하지만 (r_0)의 숫자를 주지 않는다.
단지 이 조건 하나만 보더라도, 이 proof parameterization에서

\[
r\ge r_0
\]

를 보장하려면 충분조건으로

\[
x\ge \exp((r_0+1)^5)
\]

를 요구할 수 있다. 이후 (M=160)과 (X\approx\exp(1.5Mx))가 결합되므로 규모는 대략

\[
X\approx \exp(240x)
\]

형태로 다시 커진다. 이 식은 **현재 (X_{cert})의 값이나 하한이 아니라**, 숫자 하나가 누락됐을 때
최종 threshold가 얼마나 민감해지는지 보여 주는 의존성 예시다.

### 6.4 확률 1-o(1)은 존재증명에는 충분하지만 수치 인증에는 부족하다

FMT/Sono는 여러 좋은 사건이 확률 (1-o(1))로 일어남을 보이고 union bound로 실제 residue-class
선택의 존재를 얻는다. numerical proof에서는 각 실패확률 상한을 숫자로 만들고 합이 1보다 작음을
확인해야 한다. `결국 0으로 간다`는 설명만으로 특정 (x)에서의 존재를 인증할 수 없다.

### 6.5 x에서 X로 가는 마지막 변환도 별도 proof obligation이다

Sono는 (P(x)=\prod_{p\le x}p), (Z=P^M)를 사용하고 constructed interval의 끝을

\[
2P^{M+1}\le e^{1.5Mx}
\]

로 둔다. 이를 arbitrary (X)의 정리로 바꾸려면 다음을 모두 숫자로 닫아야 한다.

- Chebyshev 함수/primorial의 explicit bound
- $x$, $\log x$, 반복로그와 $X$의 관계
- rounding과 monotonicity
- 어떤 (X\ge X_{cert})도 parameter gap 사이에서 빠지지 않는 선택 규칙

이 단계가 없으면 특정 construction sequence에서만 gap을 만든 것을 “모든 큰 X”로 잘못 확대할
수 있다.

## 7. ineffective obstruction이 있는가

이번 1차 감사에서 **본질적으로 계산 불가능한 상수가 확인되지는 않았다.** 오히려 FMT는
Section 1.2에서 모든 implied constant를 effective하게 두며, Section 2에서 ineffective한
Siegel theorem을 쓰지 않는 이유를 명시한다. Sono도 McCurley의 explicit zero-free region과
exceptional-prime deletion을 사용한다.

그러나 다음 두 문장은 다르다.

- `effective`: 원칙적으로 충분한 proof 추적을 하면 계산 가능하다.
- `numerically instantiated`: 논문에 필요한 모든 상수와 유효범위가 실제 숫자로 적혀 있다.

현재는 첫째에 해당하고 둘째에는 해당하지 않는다. 또한 이번 감사가 FMT·Maynard·Gallagher·Jutila·
Halberstam–Richert의 모든 인용 증명을 끝까지 다시 검증한 것은 아니므로, “숨은 비효율성이 절대
없다”는 최종 certificate도 아직 아니다.

## 8. 실제 numerical threshold 연구 순서

### Phase T1 — proof obligation 원장

모든 `o(1)`, `O`, `\ll`, `\asymp`, `sufficiently large/small`을 한 행씩 등록한다.

필드 예:

```text
node,source,page,equation,quantity,direction,
explicit_bound,valid_range,depends_on,status,checker
```

완료 gate: 최종 Theorem 3.6까지 가는 모든 edge가 원장에 있고 출처 없는 edge가 0개다.

### Phase T2 — 마지막 상수 여유 예산


1. \hat c에서 (2.0\times10^{-17})로 내려가는 정확한 algebraic safety margin을 추적한다.
2. Sono가 12800·1800 등에서 이미 쓴 안전 여유를 중복 계산하지 않는다.
3. 각 오차항에 허용 오차를 배분하되, 곱·합·확률 union bound 방향을 exact rational/interval
   arithmetic으로 검증한다.

목표 상수를 임의로 (10^{-17})로 낮추면 계산 여유는 커질 수 있지만 다른 부등식을 증명하는
것이다. 프로젝트의 (2\times10^{-17}) 질문을 조용히 바꾸지 않는다. 대신 upstream coefficient를
개선해 여유를 늘리는 것은 정당한 별도 연구다.

### Phase T3 — 쉬운 analytic node부터 explicit화

- explicit Mertens/primorial bound
- 반복로그 단조성과 x→X 변환
- elementary smooth-number remainder
- finite-(r) admissible tuple bound

이 단계는 exact interval arithmetic과 독립 verifier를 만들 수 있어 사용자 PC로 검증하기 좋다.

### Phase T4 — hard sieve/probability node 타당성 gate

FMT Theorem 4/6, Maynard sieve weight, Gallagher/Jutila error의 원문 증명을 추적해 실제 rate를
얻는다. 여기서 새로운 정량 lemma의 재증명이 필요하다면 그 난도와 예상 threshold를 평가한다.

다음 조건 중 하나면 일단 중단한다.

- 사용 가능한 explicit form이 없고 재증명이 현재 역량을 크게 넘음
- 얻은 threshold가 수학적으로 유효해도 저장·검산 가능한 certificate 구조가 없음
- coefficient safety budget을 만족시키지 못함

### Phase T5 — threshold calculator는 마지막에

모든 node가 explicit해진 뒤에만 (x)를 증가시키며 조건을 검증하는 코드를 만든다. 지금 코드를
먼저 만들면 알 수 없는 상수를 임의 숫자로 채우는 false precision이 된다. 그래서 이번 감사에서는
numerical (X_0) 계산기를 만들지 않았다.

## 9. ChatGPT·사용자 PC·현재 한계의 역할

| 작업 | 수행 가능성 | 설명 |
|---|---|---|
| 원문 dependency·식·방향 감사 | ChatGPT 수행 가능 | 이번 1차 감사에서 착수·구조화 |
| explicit 공개 정리 검색·비교 | ChatGPT 수행 가능 | 1차 문헌 위주로 계속 확장 가능 |
| exact constant·interval arithmetic verifier | ChatGPT 구현 + 사용자 PC 검증 가능 | 모든 입력 상수가 확보된 뒤 의미 있음 |
| parameter grid·certificate hash 검증 | 사용자 PC 적합 | CPU 수시간 규모로 제한 가능 |
| FMT/Maynard의 모든 asymptotic lemma 재증명 | 현재 한 세션에서 보장 불가 | 전문 분석수론 proof-engineering, 장기 과제 |
| (X_{cert})가 천문학적일 때 그 아래 prime 전수검증 | 현재 자원으로 불가능할 가능성 큼 | theorem threshold와 actual minimum을 분리해야 함 |

병목은 당장 CPU 12시간이나 RAM 32GB가 아니다. **필요한 부등식의 숫자와 유효범위를 수학적으로
꺼내는 일**이 먼저다. 그 뒤의 scalar inequality 검증은 상대적으로 저렴할 수 있다.

## 10. 이번 감사로 바로 확정할 수 있는 것

### 확정

- Sono의 (2.0\times10^{-17})은 FMT chain theorem의 (k=1)에 적용 가능한 증명 상수다.
- 프로젝트 end-bounded (G)와 Sono (G_1)의 경계는 일치한다.
- Sono 출판본은 numerical (X_0)를 제공하지 않는다.
- reviewed top-level proof는 exceptional zero 때문에 ineffective하지 않다.
- coefficient explicit화와 threshold explicit화는 별도 작업이다.
- `X_emp(10^20)=3,814,280`은 theorem threshold가 아니다.

### 아직 확정할 수 없음

- 실제 (X_{cert})의 존재 숫자 상한
- 그 숫자가 계산 가능한 현실적 크기인지
- 모든 cited lemma의 explicit form이 현재 문헌에 이미 있는지
- (X_\star)가 3,814,280인지 또는 다른 값인지
- full proof-engineering에 필요한 총 기간

## 11. 권장 다음 결정

가장 가치 있는 다음 작업은 새 대형 prime computation이 아니다.

1. **권장:** T1 dependency 원장을 만들고 Sono Sections 4–6의 모든 asymptotic 표기를 행 단위로
   등록한다. 예상 6–12시간의 문헌·수식 감사다.
2. T1에서 FMT Theorem 6/Maynard node가 실제 explicitization 가능한지 먼저 판정한다. 이 node가
   닫히지 않으면 쉬운 상수만 많이 계산해도 (X_{cert})는 나오지 않는다.
3. 가능 판정 뒤 T2/T3 exact verifier 계획을 별도 승인한다.
4. P018-B·P013-C와 threshold proof는 관련 없는 축이므로 recurrence 계산을 자동 재개하지 않는다.

## 12. 1차 문헌과 확인 위치

- Keiju Sono, “An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes,”
  *Le Matematiche* 80(2), 521–544 (2025),
  DOI: https://doi.org/10.4418/2025.80.2.2,
  arXiv: https://arxiv.org/abs/2404.06951
  - Theorem 3.6·PAP/UB: pp. 526–527
  - probabilistic 결합과 x→X: pp. 528–532
  - UB: pp. 532–534
  - PAP·zero density: pp. 534–537
  - FMT explicit covering/sieve 추적: pp. 538–542
- Kevin Ford, James Maynard, Terence Tao, “Chains of Large Gaps Between Primes,”
  arXiv: https://arxiv.org/abs/1511.04468
  - Theorem 1과 effectiveness: p. 2
  - asymptotic convention: p. 3
  - exceptional zero 제거·Gallagher lemma: pp. 4–5
  - Theorems 2–3: pp. 5–9
  - hypergraph Theorem 4와 random construction: pp. 9–11
  - sieve-weight Theorem 6: pp. 11–16
- Kevin S. McCurley, “Explicit Zero-Free Regions for Dirichlet L-Functions,”
  DOI: https://doi.org/10.1016/0022-314X(84)90089-1
- P. X. Gallagher, “A Large Sieve Density Estimate near \(\sigma=1\),”
  DOI: https://doi.org/10.1007/BF01403187
- Matti Jutila, “On Linnik’s Constant,”
  DOI: https://doi.org/10.7146/math.scand.a-11701
- James Maynard, “Dense Clusters of Primes in Subsets,”
  DOI: https://doi.org/10.1112/S0010437X16007296,
  arXiv: https://arxiv.org/abs/1405.2593
- H. Halberstam and H.-E. Richert, *Sieve Methods*, ISBN 0-12-318250-6.

## 13. 최종 판정

\[
\boxed{
\begin{aligned}
&c_{\mathrm{Sono}}=2\times10^{-17}:\quad \text{PROVED EXPLICIT COEFFICIENT},\\
&X_{\mathrm{cert}}:\quad \text{EFFECTIVE IN PRINCIPLE, NUMERICALLY OPEN},\\
&X_{\star}:\quad \text{OPEN},\\
&X_{\mathrm{emp}}(10^{20})=3{,}814{,}280:\quad \text{FINITE EXACT ONLY}.
\end{aligned}
}
\]

좋은 결과가 나오면 이 연구는 단순 계산 개선이 아니라, Sono/FMT 정리를 실제 숫자부터 적용할 수
있는 explicit theorem으로 강화할 수 있다. 그러나 지금은 그 숫자를 계산할 단계가 아니라, 숫자를
계산할 수 있도록 증명의 모든 숨은 유효범위를 드러내는 단계다.

## 14. 2026-09-02 T1 후속 완료

사용자 승인 후 direct proof edge를 66개 obligation으로 등록했다.

- 사람이 읽는 원장:
  `docs/method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md`
- machine-readable 원장:
  `docs/method/theory/data/Sono_FMT_T1_proof_obligations_v1.json`
- hard-node 가능성 검토:
  `docs/review/23_20260902_Sono_FMT_T1_hard_node_feasibility.md`

분류는 `EXPLICIT 5`, `PARTIAL 11`, `RATE_MISSING 30`,
`SOURCE_REVIEW_REQUIRED 4`, `HARD_BLOCKER 16`이다. dependency graph와 source key는 전부
검증됐고 cycle은 0건이다. 이로써 T1 inventory는 완료됐지만 numerical `X_cert`는 계속 OPEN이다.
다음 gate는 FMT/Maynard good-sieve-weight 층의 상수와 finite range를 실제로 복원할 수 있는지
판정하는 H1이다.

## 15. 2026-09-04 H1b-1·H1c 후속 감사

H1a 뒤 T1 분류는 `EXPLICIT 6`, `PARTIAL 10`, `RATE_MISSING 30`,
`SOURCE_REVIEW_REQUIRED 4`, `HARD_BLOCKER 16`이다. H1b-1과 H1c는 source·논리관계를 더
정확하게 만들었지만 T1 row 자체의 status 수는 바꾸지 않았다.

- H1b-1: Maynard Lemmas 8.1–8.4를 13개 node로 분해하고 Lemma 8.3의 정확한 GGPY source를
  확인했다. numerical summation multiplier와 common cutoff는 OPEN이다.
- H1c: FGKMT Hypothesis 1과 Sono PAP를 20개 node로 분리했다. Hypothesis 1(1),(3)은
  \(\mathcal A=\mathbb Z\)에서 exact sufficient reduction이 있지만, condition (2)와 PAP의
  finite rate는 OPEN이다.
- 논리 정정: `PAP-11 -> SIV-08`은 함의 관계가 아니므로 제거했다. 둘은 shared analytic source를
  가진 sibling root다.
- 서지 정정: Jutila *On Linnik's Constant*는 1970이 아니라 1977 출판이다.

따라서 최종 판정은 변하지 않는다.

```text
X_cert = OPEN
threshold calculator = NOT READY
새 prime sweep = NOT A CURRENT PROOF BOTTLENECK
```

상세 정본은
`docs/method/theory/15_Sono_FMT_H1b1_basic_summation_constant_audit.md`와
`docs/method/theory/16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md`다.

## 16. 2026-09-09 H1c-1a 후속 감사

H1c-1a는 Hypothesis 1(2)와 Maynard Proposition 9.2를 수치화할 explicit 선행정리 후보를
실제 modulus·중심항·exceptional character·log-saving·cutoff 조건별로 대조했다. 선언한
source 범위에서 drop-in 정리는 없었다. Bordignon 2021 Theorem 4가 가장 가까운 출판
합성 후보지만 affine modulus coverage, 한 공통 exceptional \(B\), \(\psi\to\pi\), exact
recentring, represented-prime lower bound와 common cutoff를 새로 연결해야 한다.

따라서 이 감사의 결론은 변하지 않는다. \(X_{\mathrm{cert}}\)는 여전히 `OPEN`이고 threshold
calculator는 `NOT READY`다. 다음 최소 gate는 H1c-1b의 Bordignon parameter·modulus-envelope
feasibility다. 상세는
[`H1c-1a 검토`](38_20260909_H1c1a_quantitative_prime_distribution_타당성검토.md)를 따른다.
