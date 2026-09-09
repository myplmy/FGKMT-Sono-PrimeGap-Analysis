# Sono/FMT H1c Hypothesis 1·PAP source tracing

## 2026-09-09 H1b-DEP 현재 상태

[theory 48](48_Sono_FMT_H1bDEP_actual_dependency_map.md)와
[진행현황 review 54](../../review/54_20260909_H1bDEP_Xcert_진행현황_의존성감사.md)가 현재 actual 경로의 정본이다.
P91/P92/P94/L85/L86 및 필요한 보조증명은 P95를 호출하지 않는다. P94는 FMT sequel에 필요하며,
P95는 일반 P6.1의 OPEN 의무로 보존하되 선택한 actual 경로의 선결조건에서 제외한다.
NORM의 filtered fixed-X 입력과 C_h=4·actual support 연결은 닫혔지만 post-conditioning,
correlation·hypergraph·PAP/UB·최종 오차·arbitrary-X는 6묶음/12작업으로 남는다.
T1 66행은 general/복합 행을 포함하므로 상태 개수를 완료율로 쓰지 않는다. broad SIV-07/08/09와
X_cert는 계속 OPEN/HARD_BLOCKER이고 다음은 H1b-COR1 / DEP-R01이다.
아래 날짜별 next-gate와 미완료 서술은 당시 이력이며 이 현재 상태가 우선한다.

- 작성: 2026-09-04 KST
- 증거 수준: `SOURCE-LEVEL PROOF-DEPENDENCY AUDIT`
- 판정: `SIBLING_SOURCE_CHAINS_TRACED_NUMERICAL_PACKAGES_OPEN`
- `SIV-03`: 후속 H1c-1b.1a.1에서 `EXPLICIT`
- `SIV-08`: `HARD_BLOCKER` 유지
- `PAP-11`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json`](data/Sono_FMT_H1c_Hypothesis1_PAP_source_trace_v1.json)

## 1. 가장 중요한 결론

FGKMT의 Hypothesis 1과 Sono의 PAP는 둘 다 “산술수열 안에 질수가 어떻게 분포하는가”를 다루지만,
같은 명제가 아니다.

```text
FGKMT Hypothesis 1(2)
  = 많은 modulus의 오차를 합한 평균 discrepancy 상한
  = q <= x^(1/3) 수준까지 필요

Sono PAP
  = 한 modulus와 residue class마다 주는 pointwise prime-count 하한
  = x >= q^160, 즉 대략 q <= x^(1/160)
```

둘은 zero-free region과 character sum 같은 도구를 일부 공유한다. 그러나 **PAP를 증명하면
Hypothesis 1이 자동으로 나오거나, Hypothesis 1을 증명하면 PAP가 자동으로 나오는 것은 아니다.**
기존 T1 DAG의 `SIV-08 -> PAP-11` 연결은 잘못된 직접 의존이므로 제거한다. 두 package는 아래에서
다시 만나는 병렬 입력이다.

이번 감사의 긍정적 결과는 Hypothesis 1의 세 조건 중 (1)과 (3)이 \(\mathcal A=\mathbb Z\)인
경우 초등적인 finite inequality로 줄어든다는 점이다. 하지만 가장 어려운 (2), 그리고 PAP의
principal/nonprincipal/\(\psi\to\pi\) 수치화는 여전히 열려 있다. 그래서 `X_cert`는 계산할 수 없다.

쉬운 비유로 말하면 다음과 같다.

- Hypothesis 1은 여러 도로의 **평균 교통오차 총합**을 제한한다.
- PAP는 특정 도로 하나에 **최소 차량 수**가 있음을 보증한다.

두 검사에 같은 교통센서를 사용할 수는 있지만, 평균오차 검사 합격증이 최소 차량 수 합격증을
대신하지는 않는다.

## 2. 정본 source와 서지 정정

### FGKMT Hypothesis 1 경로

- K. Ford, B. Green, S. Konyagin, J. Maynard, T. Tao,
  [*Long Gaps Between Primes*](https://arxiv.org/abs/1412.5029),
  Hypothesis 1, Lemmas 7.1–7.2, Corollary 6, equations (7.2)–(7.3).
- H. Davenport, *Multiplicative Number Theory*, 3rd ed. (2000), Chapters 20 and 28.

로컬 정본은
[`article/LONG GAPS BETWEEN PRIMES.pdf`](<../../../article/LONG GAPS BETWEEN PRIMES.pdf>)이며,
SHA-256은 machine ledger에 고정했다.

### Sono PAP 경로

- K. Sono,
  [*An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes*](https://doi.org/10.4418/2025.80.2.2),
  Assumption 3.2와 Section 5.
- K. S. McCurley,
  [*Explicit Zero-Free Regions for Dirichlet L-Functions*](https://doi.org/10.1016/0022-314X(84)90089-1).
- P. X. Gallagher,
  [*A Large Sieve Density Estimate near \(\sigma=1\)*](https://doi.org/10.1007/BF01403187).
- M. Jutila,
  [*On Linnik's Constant*](https://doi.org/10.7146/math.scand.a-11701),
  *Mathematica Scandinavica* 41 (1977), 45–62.
- H. Maier,
  [*Chains of Large Gaps Between Consecutive Primes*](https://doi.org/10.1016/0001-8708(81)90003-7),
  Lemma 2.

기존 T1 source key `JUTILA1970`은 잘못됐다. Sono의 참고문헌과 저널 기록 모두 **1977**을
가리키므로 `JUTILA1977`로 정정한다. 이 서지 정정은 증명 상태를 올리지는 않는다.

## 3. FGKMT Hypothesis 1의 세 조건

### 3.1 조건 (1): 정수 구간의 산술수열 균등성

\(\mathcal A(y)\)가 \(N\)개의 연속 정수로 된 interval이면, 임의의 \(q,a\)에 대해

\[
\left|\#\mathcal A(y;q,a)-\frac Nq\right|\le1.
\]

따라서 \(\theta=1/3\)일 때 Hypothesis 1(1)의 합은 최대 \(\lfloor y^{1/3}\rfloor\)이다.
그러므로 다음은 condition (1)의 exact sufficient condition이다.

\[
\boxed{
\lfloor y^{1/3}\rfloor(\log y)^{100k^2}\le N.
}
\]

이 식은 아직 전체 threshold 숫자가 아니다. 실제 FGKMT application의 interval endpoint와
\(N\), 허용 \(k\)를 넣고 다른 모든 조건과 동시에 만족하는지를 확인해야 한다. 그래도 숨은
Vinogradov 상수 없이 finite inequality로 바뀐 점은 실제 진전이다.

### 3.2 조건 (3): 한 residue class에 과도하게 몰리지 않음

같은 정수 interval에서

\[
\#\mathcal A(y;q,a)\le\frac Nq+1.
\]

\(N\ge q\)이면 우변은 \(2N/q\) 이하이므로 condition (3)의 implied constant로 2를 쓸 수 있다.
따라서 남는 일은 실제 parameter range에서 \(N\ge q\)와 endpoint를 exact하게 확인하는 것이다.

### 3.3 조건 (2): 선형식이 나타내는 질수의 평균 분포

이것이 핵심 난점이다. FGKMT Lemma 7.2의 논리는 다음과 같다.

```text
Landau-Page dichotomy
  -> exceptional conductor에서 B 선택
  -> effective primitive-character psi bound (7.2)
  -> standard Bombieri-Vinogradov proof (7.3)
  -> L(n)=an+b를 modulus |a|q의 progression으로 변환
  -> Hypothesis 1(2)
```

원문은 \(Q=\exp(c_1\sqrt{\log x})\)에서 \(c_1\)을 “충분히 작게” 고르고,

\[
x\exp(-3c\sqrt{\log x})
\]

모양의 character bound를 사용한다. 이어 Davenport Chapter 28의 standard
Bombieri–Vinogradov proof를 통해 \(q<x^{1/2-\varepsilon}\) 범위의 discrepancy를 얻는다.

숫자로 만들려면 다음이 필요하다.

1. Landau–Page와 zero-free strip의 실제 상수
2. 특정 \(c_1,c,\varepsilon\) 및 최초 \(x\)
3. large-sieve/Bombieri–Vinogradov multiplier
4. \(L(n)=an+b\)의 부호·gcd·endpoint별 exact progression mapping
5. represented-prime population \(\#\mathcal P_{L,\mathcal A}(x)\)의 explicit lower bound

조건 (1)과 (3)이 쉬워졌어도 condition (2)가 닫히지 않으므로 `SIV-08` 전체는 여전히
`HARD_BLOCKER`다.

## 4. Sono PAP 경로

Sono Assumption 3.2는 zero-free 조건 아래

\[
\pi(x;q,a)\ge
C_{\mathrm{PAP}}(1+o(1))\frac{x}{\varphi(q)\log x},
\qquad x\ge q^{D_{\mathrm{PAP}}}
\]

를 요구한다. Sono가 최종적으로 쓰는 숫자는

\[
C_{\mathrm{PAP}}=1-e^{-2},\qquad D_{\mathrm{PAP}}=160.
\]

이 두 숫자가 explicit하다는 사실과 PAP가 어떤 최초 \(x\)부터 finite inequality로 성립한다는
사실은 다르다.

### 4.1 확인된 숫자

- McCurley source에서 가져온 \(R=9.645908801\ldots\)
- Sono의 단순화 \(c_{\mathrm{ZFR}}=1/24\)
- Gallagher형 estimate에 넣는 \(a=(3/10)c_{\mathrm{ZFR}}=1/80\)
- Jutila의 고-\(\alpha\) exponent와 trivial range를 합친 \(c_{\mathrm{ZD}}=16\)
- \(D_{\mathrm{PAP}}=10c_{\mathrm{ZD}}=160\)
- \(1-e^{-aD}=1-e^{-2}\)

### 4.2 여전히 빠진 숫자

- Gallagher와 Jutila estimate의 implied multiplier·finite range
- Maier Lemma 2의 transfer 상수와 endpoint 조건
- principal term \((1+o(1))x/\varphi(q)\)의 one-sided rate
- nonprincipal term의 `O_<=`가 시작되는 최초 \(x\)
- \(\psi\)에서 실제 prime count \(\pi\)로 갈 때 prime-power·partial-summation error
- exceptional character case를 포함한 하나의 공통 cutoff

따라서 \(D=160\)을 보고 단순히 \(x=q^{160}\)부터 PAP가 증명됐다고 읽으면 안 된다. 정확한
뜻은 `x >= q^160`이라는 **형태상의 조건**과 여러 “충분히 큰 \(x\)” 조건을 모두 만족해야
한다는 것이다.

## 5. explicit Bombieri–Vinogradov 대체 source 검토

Akbary–Hambrook,
[*A Variant of the Bombieri-Vinogradov Theorem with Explicit Constants and Applications*](https://arxiv.org/abs/1309.2730)
은 실제 explicit constant를 제공하므로 중요한 후보다.

하지만 Theorem 1.3은 modulus의 최소 소인수가 지정된 \(Q_1\)보다 큰 rough-modulus family에
제한된다. FGKMT Hypothesis 1(2)는 한 exceptional prime \(B\)와 서로소인 모든 필요한 \(q\)를
합한다. 이것은 “최소 소인수가 모두 크다”와 다르다.

따라서 이 논문은 현재 proof에 바로 끼울 수 있는 대체품이 아니다.

```text
판정: ALTERNATIVE_NOT_DIRECT_SUBSTITUTE
```

사용하려면 modulus를 rough part와 small-prime part로 분리하고, 빠진 small-prime-factor moduli를
별도로 완전히 처리하며, 그 분해가 FGKMT의 affine forms와 exceptional \(B\)를 보존한다는 새
증명이 필요하다. 이는 유망한 proof redesign 후보이지만 단순 source 교체가 아니다.

## 6. 19개 source node와 1개 common-cutoff node

기계 원장은 총 20개 node를 저장한다.

| 묶음 | 행 수 | 핵심 판정 |
|---|---:|---|
| Hypothesis 1 | 9 | (1),(3) finite reduction; (2) open |
| PAP | 8 | 계수·지수 일부 explicit; rate/cutoff open |
| explicit BV 대안 | 1 | direct substitute 아님 |
| 논리관계 정정 | 1 | Hypothesis 1과 PAP는 sibling |
| 공통 cutoff | 1 | 두 package가 닫히기 전 `HARD_BLOCKER` |
| **합계** | **20** | |

모든 node의 `threshold_ready`는 `false`다.

## 7. 증명 그래프 정정의 의미

기존 T1에서 `SIV-08`은 `PAP-11`을 직접 의존했다. 이번 source comparison 뒤에는 다음처럼
정정한다.

```text
잘못된 연결:
PAP-11 -> SIV-08

정정된 연결:
PAP-11 ----+
            +--> downstream Sono/FMT composition
SIV-08 ----+
```

의존선을 제거했다고 증명이 쉬워지는 것은 아니다. 오히려 서로 다른 두 문제를 각각 증명해야
한다는 점을 명확히 한 것이다. T1의 hard-blocker 수와 `X_cert=OPEN` 판정은 바뀌지 않는다.

## 8. 실행 가능성·자원 판단

### Codex가 다음에 수행할 수 있는 일

- Hypothesis 1(1),(3)의 exact endpoint/parameter inequality 정식화
- FGKMT (7.2)–(7.3)의 proof를 Davenport 하위 lemma까지 세분화
- explicit \(\psi\to\pi\)와 prime-density lower-bound source 후보 비교
- Akbary–Hambrook rough-modulus route가 small-modulus 분할로 연결되는지 영향도 분석

### 사용자 PC 계산이 나중에 도울 수 있는 일

- 고정 parameter 후보가 생긴 뒤 finite inequality cutoff를 interval arithmetic으로 찾기
- small modulus·small \(x\) 잔여범위를 exact 계산으로 닫기
- 서로 독립인 bound 구현 두 개로 공통 cutoff certificate를 재검산

현재는 그 전에 필요한 부등식과 상수가 확정되지 않았으므로 장시간 계산 runner가 유용하지 않다.

### 현재 불가능한 것

- \(C_{\mathrm{PAP}}=1-e^{-2},D_{\mathrm{PAP}}=160\)만으로 PAP 시작점 산출
- standard Bombieri–Vinogradov라는 문구만으로 Hypothesis 1 시작점 산출
- 둘 중 하나를 다른 하나의 증명으로 대체
- `SIV-08`, `PAP-11`, good weight 또는 \(X_{\mathrm{cert}}\) closure

## 9. 다음 gate와 권장 경로

### 1순위: H1b-1a explicit cutoff·초등 summation

H1b-1의 가까운 constructive component다. 1–3일의 정식화로 실제 수치 lemma 후보를 만들 수 있다.

### 2순위: H1c-1 quantitative character package

FGKMT (7.2)–(7.3)을 다음 단위로 나눈다.

1. explicit Landau–Page/zero-free constants
2. 특정 \(c_1,c,\varepsilon\)
3. quantitative BV multiplier와 range
4. affine-form mapping
5. represented-prime lower bound

source audit·정식화에 3–10일 이상, 완전한 quantitative reproof에는 수주 이상이 걸릴 수 있다.

### 3순위: PAP 하위 source의 one-sided finite 재구성

Gallagher–Jutila–Maier–McCurley 경로의 multiplier와 \(\psi\to\pi\)를 합친다. 이 역시 수일에서
수주 이상이며, 다른 root blocker보다 먼저 threshold calculator를 만들 근거는 없다.

현재 사용자 수행절차는 없다.

```text
별도 수행절차 필요없음
```

## 10. 엄밀한 최종 판정

```text
Hypothesis 1(1) finite reduction = FOUND
Hypothesis 1(3) finite reduction = FOUND
Hypothesis 1(2) numeric package = OPEN
PAP coefficient/exponent        = PARTIAL_NUMERIC
PAP finite starting point       = OPEN
Hypothesis 1 <-> PAP implication = FALSE AS PRINTED
SIV-08 and PAP-11               = HARD_BLOCKER
X_cert                          = OPEN
```

이번 감사로 “어느 source를 읽어야 하는가”와 “어떤 두 문제를 혼동하면 안 되는가”는 닫혔다.
하지만 소수분포 정리의 숨은 multiplier와 시작점을 얻는 정량 재증명은 이제 시작 단계다.

## 11. 2026-09-09 H1c-1a source inventory 후속 판정

후속 [`H1c-1a 정본`](32_Sono_FMT_H1c1a_quantitative_prime_distribution_source_inventory.md)은
Hypothesis 1(2)와 Maynard Proposition 9.2의 exact centered target을 고정한 뒤
Akbary--Hambrook, Sedunova 2018/2019, Yamada I/II, Bordignon 2021, Bennett et al., Kadiri,
Liu와 Johnston 2026을 modulus·log-saving·exceptional character·affine transfer·finite cutoff별로
대조했다.

선언한 source 안에서 drop-in 정리는 0개다. 임의 \(A>3\)에 explicit non-exceptional average를
주는 Bordignon 2021 Theorem 1.4가 가장 가까운 `PRIMARY_COMPOSITION_CANDIDATE`다. 하지만
\(|a|q\) coverage, fixed-\(k\) 또는 growing-\(A\) branch, 하나의 공통 exceptional \(B\),
반열린 endpoint, \(\psi\to\pi\), exact total-count recentering, represented-prime lower bound와
common cutoff는 아직 증명되지 않았다.

따라서 H1c-1a source inventory는 완료됐지만 이 문서의
`numerical_hypothesis1_package_ready=false`, `SIV-08=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`은 변하지 않는다. 다음 gate는 H1c-1b이며 threshold calculator와
장시간 prime sweep은 계속 금지한다.

## 12. 2026-09-09 H1c-1b.1 후속 판정

후속 [`H1c-1b.1 정본`](33_Sono_FMT_H1c1b1_parameter_modulus_envelope.md)은
fixed-\(k\) branch를 배제하고 실제 지수를 \(100r^2\)로 고정했다. actual P9.2 호출은
identity form이므로 affine lift를 가지치기할 수 있고, Bordignon의 pointwise
\(A(r)\) 대입과 modulus capacity는 endpoint-safe \(r\ge36\)에서 닫힌다.

다만 source-selected \(r_s\)는 원래 \(x\)에서 고르고 actual call은 \(x/2\)에서 하므로
transition strip에서 Maynard의 인쇄된 dimension range를 그대로 만족하지 않는다.
\(r_s-1\) 보정은 가능하지만 coefficient transfer가 남는다. 그러므로
`numerical_hypothesis1_package_ready=false`, `SIV-08=HARD_BLOCKER`,
\(X_{\mathrm{cert}}=\)`OPEN`은 유지한다. 다음 gate는 H1c-1b.1a다.

## 13. 2026-09-09 H1c-1b.1a 후속 판정

후속
[H1c-1b.1a 정본](34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md)은
\(r_T=\lfloor(\log(x/2))^{1/5}\rfloor\)를 actual dimension으로 고정하고,
H1a의 exact \(J_r/I_r\) 하한과 FGKMT의
\(R=(x/4)^{\theta/3}\)를 합성했다. 모든 \(r_T\ge36\)에서 dimension·\(R\)
normalization은 \(39/40\)보다 크다. Sono의 \(16/15\) slack 때문에
\(\sigma y\le(26/25)80cx\log_2x\)이면 최종 \(c\)를 낮출 필요가 없다.

따라서 dyadic repair의 asymptotic coefficient transfer는 닫혔다. 후속 H1c-1b.1a.1은
Rosser--Schoenfeld Theorem 7로 (x\ge2\exp(36^5))에서 (26/25)보다 강한
Mertens upper gate를 증명해 `SIV-03`을 `EXPLICIT`으로 만들었다. common exceptional
\(B\), count transfer, density와 full error composition은 계속 열려 있다. 그러므로
`numerical_hypothesis1_package_ready=false`, `SIV-08=HARD_BLOCKER`,
\(X_{\mathrm{cert}}=\)`OPEN`은 유지한다. 다음 gate는 H1c-1b.2 full quantitative
distribution composition이다.

## 14. 2026-09-09 H1c-1b.2 후속 판정

H1c-1b.2는 Bordignon Theorem 1.4의 exceptional object가 fixed \(Q_1\)에 대해
선택된다는 quantifier를 실제 identity-form 호출에 적용했다. \(T\), \(2T\)에 같은
\(Q_1\)을 쓰고 \(q_0\)의 prime divisor \(B\)를 택하면 actual
\(q\le T^{1/3},(q,B)=1\) family를 두 endpoint에서 동시에 제어한다.

또 최종 출판본 12항을 모두 보존해 raw \((T,2T]\) \(\psi\) composition을 닫았다.
arXiv v1은 중심항과 log factor가 최종판과 달라 수치식에 채택하지 않는다.

Hypothesis 1(2)의 half-open unweighted count, exact recentering, density와 full
absorption은 계속 열려 있다. 따라서 `numerical_hypothesis1_package_ready=false`,
`SIV-08=HARD_BLOCKER`, \(X_{\mathrm{cert}}\)=`OPEN`이고 다음 gate는
H1c-1b.3이다.

## 15. 2026-09-09 H1c-1b.3 후속 판정

H1c-1b.3은 Maynard Hypothesis 1(2)의 actual identity-form 목표가
\([T,2T)\)의 unweighted prime count이며 중심은 같은 구간의 exact total이라는 점을
source에서 확정했다. fixed-\(B\) family를 Abel 적분 전체에 유지하고
\(\psi\to\pi_1\to\pi\), prime powers와 endpoint atom을 명시적으로 합성했다.

이는 Hypothesis 1(2)의 exact normalization을 닫은 것이지 required rate를 닫은 것이 아니다.
`numerical_hypothesis1_package_ready=false`, `SIV-08=HARD_BLOCKER`,
\(X_{\mathrm{cert}}\)=`OPEN`을 유지한다. 다음 gate는 H1c-1b.4 source normalization,
represented-prime density와 full absorption이다.

## 16. 2026-09-09 H1c-1b.3r1 endpoint source 교정

앞 절의 actual-target 판정은 철회한다. Maynard 원문의 일반 정의는 \([T,2T)\)이지만
FGKMT modified Definition 2는 \([T,2T]\)을 사용한다. source \((T,2T]\)에서 actual
closed target으로의 lower atom correction은 centered count에서 modulus마다 1 이하이고,
기존 수치 envelope를 보존한다.

이 교정은 unweighted input에만 해당한다. FGKMT가 Theorem 6의 closed weighted sum을
Section 8의 외부 \((T,2T]\) prime set으로 되돌릴 때 \(w(T)\)를 제거하는 의무는 열려 있다.

## 17. 2026-09-09 H1c-1b.4e actual-input 판정

H1c-1b.4a–4e를 actual identity subset에 합성하면
\(X\ge2\exp(10^{50})\)에서 Hypothesis 1(1)--(3)을 constants \(1,1,2\)로 만족한다.
따라서 machine trace의
`actual_identity_hypothesis1_input_ready=true`는 타당하다.

반면 이 문서의 `numerical_hypothesis1_package_ready=false`는 arbitrary
\(\mathcal A\)·affine form을 포함하는 일반 package에 대한 fail-closed flag이므로 유지한다.
weighted Proposition 9.2, FGKMT lower-endpoint weight, broad `SIV-08`,
PAP sibling과 \(X_{\mathrm{cert}}\)도 닫히지 않았다. 다음 gate는 H1b-P92a다.

## 18. 2026-09-09 H1b-P92a actual weighted-child 후속 상태

[theory 44](44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md)가
\(k\ge10^{200}\)에서 actual identity weighted Proposition 9.2와 closed-to-open lower
weight/count atom을 닫았다. 상대/가법 multiplier는 1/1이다. 앞 §17 및 기존 successor
snapshot의 false flag는 당시 기록으로 보존하며, 새 machine successor에 closure를 기록한다.

일반 Hypothesis package, 다른 actual moment와 singular-series/weight/tau/u 공통 합성,
PAP sibling과 \(X_{\rm cert}\)는 여전히 OPEN이다. 다음 gate는 H1b-P91a다.

## 19. 2026-09-09 H1b-NORM 후속 상태


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
