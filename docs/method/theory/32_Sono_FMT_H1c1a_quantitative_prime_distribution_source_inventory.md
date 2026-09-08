# Sono/FMT H1c-1a quantitative prime-distribution source inventory

- 작성: 2026-09-09 KST
- 증거 수준: `SOURCE INVENTORY / APPLICABILITY AUDIT`
- 판정: `NO_DROP_IN_SOURCE_BORDIGNON2021_COMPOSITION_ROUTE_FOUND`
- Hypothesis 1(2): `OPEN`
- Maynard Proposition 9.2 numerical package: `OPEN`
- `SIV-07/08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json`](data/Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json)
- 비판적 검토:
  [`../../review/38_20260909_H1c1a_quantitative_prime_distribution_타당성검토.md`](../../review/38_20260909_H1c1a_quantitative_prime_distribution_타당성검토.md)

## 1. 결론부터

이번 inventory에서 **FGKMT Hypothesis 1(2)를 수치식으로 그대로 대신할 수 있는 단일 정리**는
찾지 못했다. 이것은 전 세계 문헌에 그런 정리가 없다는 novelty 주장이 아니라, 아래에 명시한
표적 원문과 explicit 후속연구를 실제 호출 조건별로 대조한 결과다.

가장 가까운 후보는 Bordignon의 2021년 출판논문 Theorem 4다. 이 정리는 임의의 실수
\(A>3\)에 대해 예외모듈을 제외한 명시적 Bombieri--Vinogradov형 상계를 준다. 따라서
\((\log x)^{-100k^2}\) 수준을 만들 가능성이 있는 **주 합성 후보**다. 그러나 다음 연결은 그
논문이 대신 증명해 주지 않는다.

1. FGKMT의 \(q\le x^{1/3}\)을 affine modulus \(|a|q\)로 옮긴 뒤에도 정리 범위에 드는가.
2. 모든 endpoint와 모든 linear form에 한 exceptional conductor와 한 prime \(B\)를 쓸 수 있는가.
3. \(\psi\) 중심항을 Maynard의 정확한
   \(\#\mathcal P_{L,\mathcal A}(x)/\phi_L(q)\) 중심항으로 바꿀 수 있는가.
4. von Mangoldt weight, prime powers, 반열린 구간과 음의 leading coefficient를 빠짐없이 처리하는가.
5. \(k\)를 고정할 것인지, 원문 허용범위 \(k\le(\log x)^{1/5}\) 전체에 대해 \(A\)의 증가를
   제어할 것인지.
6. 모든 상수와 유효범위를 하나의 finite cutoff로 합칠 수 있는가.

따라서 H1c-1a가 닫은 것은 **어느 정리를 다음에 조립할지와 무엇을 새로 증명해야 하는지**다.
Hypothesis 1(2), Proposition 9.2, good sieve weight 또는 \(X_{\mathrm{cert}}\)를 닫지는 않았다.

## 2. 정확한 목표식

Maynard의 [*Dense Clusters of Primes in Subsets*](https://arxiv.org/abs/1405.2593)는
\(L(n)=l_1n+l_2\)에 대해

\[
\phi_L(q)=\frac{\phi(|l_1|q)}{\phi(|l_1|)}
\]

를 정의하고 Hypothesis 1(2)에서

\[
\sum_{\substack{q\le x^\theta\\(q,B)=1}}
\max_{(L(a),q)=1}
\left|
\#\mathcal P_{L,\mathcal A}(x;q,a)
-\frac{\#\mathcal P_{L,\mathcal A}(x)}{\phi_L(q)}
\right|
\ll
\frac{\#\mathcal P_{L,\mathcal A}(x)}{(\log x)^{100k^2}}
\]

를 요구한다. Proposition 9.2는 이 식을 그대로 Bdd3로 가정하며, 결론의 implied constant가
\(\theta,\alpha\)와 Bdd1--Bdd3의 implied constants에 의존한다고 명시한다.

[FGKMT](https://arxiv.org/abs/1412.5029) Lemma 7.2의 실제 검증 범위는

\[
\theta=\frac13,\qquad k\le(\log x)^{1/5},qquad
1\le |a_i|\le\log x,qquad |b_i|\le x(\log x)^2,
\]

이고 \(x\le y\le x(\log x)^2\), \(n\in[y,2y)\)의 affine forms를 다룬다. 식 (7.2)--(7.3)은
가능한 exceptional character를 한 prime \(B\)로 회피하면서 primitive-character와
Bombieri--Vinogradov형 합을 사용한다. 이 proof architecture는 목적에 맞지만 수치 multiplier와
공통 finite cutoff가 인쇄돼 있지 않다.

중요한 점은 우리가 필요한 식이 단순한
\(\psi(t;m,c)-t/\phi(m)\) 상계가 아니라는 것이다. modulus, 중심항, 구간과 분모가 모두
Maynard의 표기와 일치해야 한다.

## 3. source inventory

| source | 확인한 핵심 | 이 프로젝트 판정 |
|---|---|---|
| Maynard 2016, Hypothesis 1(2), Proposition 9.2 | 목표식과 P9.2 의존성 | `TARGET_CONTRACT` |
| FGKMT 2018, Lemmas 7.1--7.2, (7.2)--(7.3) | 원래 asymptotic character/BV 경로 | `ORIGINAL_ASYMPTOTIC_ROUTE` |
| [Akbary--Hambrook 2015](https://arxiv.org/abs/1309.2730), Thm. 1.3/Cor. 1.4 | explicit 평균상계, rough moduli | `PARTIAL_INPUT` |
| [Sedunova 2018](https://doi.org/10.5802/pmb.24), Thm. 1 | log factor 개선, 여전히 least-prime-divisor 제한 | `PARTIAL_INPUT` |
| [Sedunova 2019](https://doi.org/10.5802/jtnb.1098), effective corollary | effective asymptotic route | `PARTIAL_INPUT_WITH_CORRECTION` |
| [Yamada II](https://arxiv.org/abs/1309.5798), Thms. 1.1--1.2 | possible exceptional modulus 제외, \(2\le A\le7\) | `PARTIAL_INPUT / PREPRINT` |
| [Yamada I](https://arxiv.org/abs/1306.5322) | bounded-\(A\) explicit PNT-AP component | `PARTIAL_INPUT / PREPRINT` |
| [Bordignon 2021](https://nyjm.albany.edu/j/2021/27-54.html), Thms. 2, 4 | 임의 \(A>3\), explicit non-exceptional average | `PRIMARY_COMPOSITION_CANDIDATE` |
| [Bennett et al.](https://arxiv.org/abs/1802.00085), Thms. 1.1--1.3 | fixed-modulus \(\psi,\theta,\pi\) explicit bounds | `PARTIAL_INPUT` |
| [Kadiri](https://arxiv.org/abs/math/0510570), Thm. 1.1 | \(q\le400000\)에서 zero-free \(R=5.60\) | `PARTIAL_INPUT` |
| [Liu 2017](https://doi.org/10.1007/s10474-017-0745-z), Thm. 1 | effective all-moduli BV, 고정 log-saving | `EFFECTIVE_BUT_INSUFFICIENT_RATE` |
| [Johnston 2026](https://arxiv.org/abs/2510.10853), Thms. 1.6--1.7 | sieve 자체를 고쳐 exceptional modulus 회피 | `RECENT_PREPRINT / PROOF_REDESIGN_CANDIDATE` |

이 목록은 H1c-1a의 선언된 검색 범위다. `DROP_IN` 판정은 0개지만, 이것을 문헌 전체에 대한
비존재 주장으로 읽으면 안 된다.

## 4. 후보별 비판적 적용성

### 4.1 Akbary--Hambrook와 Sedunova 2018

두 정리는 명시적 평균상계를 주지만 합에 들어가는 modulus가

\[
\ell(q)>Q_1
\]

인 경우, 즉 모든 작은 소인자를 제거한 rough modulus에 제한된다. 반면 FGKMT 조건은

\[
(q,B)=1
\]

로, 특정 prime \(B\) 하나만 피한다. 예를 들어 \(2\nmid B\)라면 짝수 \(q\)도 FGKMT 합에
들 수 있으므로 두 조건은 같지 않다. small-prime part를 따로 합산하고 두 부분이 affine lift와
같은 \(B\)를 보존함을 증명하지 않는 한 직접 대체할 수 없다.

### 4.2 Yamada I/II

Yamada II Theorem 1.1은 possible exceptional modulus로 나누어지는 \(q\)를 제외하고
\(2\le A\le7\)에 explicit 평균상계를 준다. exceptional geometry는 rough-modulus route보다
FGKMT에 가깝다. 그러나 Hypothesis 1(2)의 지수는 \(100k^2\)이고 실제 범위는 적어도
\(k\ge36\)을 포함하므로 필요한 log-saving은 \(129600\) 이상이다. \(A\le7\)만으로는 이를
만들 수 없다. 또한 두 Yamada 문서는 후속 출판논문에서도 unpublished preprint로 취급된다.

### 4.3 Bordignon 2021: 주 합성 후보

Bordignon Theorem 4는 \(A>3\),

\[
Q=\frac{\sqrt{x}}{(\log x)^A},\qquad 1\le Q_1\le(\log x)^A
\]

에서 possible exceptional modulus \(q_0\)가 \(q\)를 나누는 경우를 제외하고 explicit 합을
준다. 우변에는 대략 \(\sqrt{x}\), \(x/(\log x)^{A-9/2}\),
\(x(\log x)^{9/2}/Q_1\), 그리고 명시된 \(C(A,A-3,X_0)\), \(E(x,A)\)가 들어간다.

이것이 가장 가까운 이유는 \(A\)를 7 같은 작은 고정 범위에 묶지 않기 때문이다. 그러나
“\(A=100k^2+\)여유를 넣으면 끝”은 아직 증명이 아니다.

- downstream이 \(k\)를 실제로 한 finite 값으로 고정하면 그 \(k\)에 대한 \(A\)를 선택할 수 있다.
- 반대로 FGKMT의 허용범위 전체에 대해 uniform statement를 원하면 \(A\)와
  \(C(A,A-3,X_0)\)의 증가를 함께 제어해야 한다.
- affine modulus가 \(|a|q\)이므로
  \(|a|x^{1/3}\le\sqrt{Y}/(\log Y)^A\) 같은 explicit coverage inequality가 필요하다.
- \(q_0\mid q\)를 제외하는 것과 \((q,B)=1\)은 한 공통 \(q_0\)의 largest prime factor를
  \(B\)로 택하면 방향상 호환될 수 있다. 하지만 endpoint마다 다른 \(q_0\)가 나오지 않는다는
  uniformization을 먼저 증명해야 한다.

따라서 채택 상태는 `PRIMARY_COMPOSITION_CANDIDATE`, `direct_substitute=false`다.

### 4.4 Bennett et al.과 Kadiri

Bennett et al.은 각 fixed modulus에 대해 explicit \(\psi,\theta,\pi\) 상계를 준다. 예를 들어
\(q\le10^5\)에서는 \(x_0(q)\le8\times10^9\), 더 큰 \(q\)에는
\(\exp(0.03\sqrt q(\log q)^3)\) 형태의 보수적 cutoff가 제시된다. 이는 작은 affine modulus의
정확한 보조검사와 represented-prime lower bound에는 유용하지만, 모든
\(q\le x^{1/3}\)을 개별 상계로 더하면 필요한 강한 평균 saving을 얻지 못한다.

Kadiri의 \(R=5.60\) zero-free region은 \(3\le q\le400000\)의 finite conductor 구간에만
적용된다. 낮은 conductor 부분을 줄이는 데는 쓸 수 있지만, 한편으로는 큰 conductor와
Landau--Page exceptional case를 별도로 닫아야 한다.

### 4.5 Liu와 Johnston

Liu의 effective BV는 all-moduli 경로라는 장점이 있지만 확인된 오차는
\(x(\log\log x)^9/(\log x)^2\) 수준이다. \((\log x)^{-100k^2}\)와는 지수부터 맞지 않으며,
computable constant가 인쇄된 숫자로 제공된 것도 아니다.

Johnston 2026은 exceptional modulus를 만났을 때 modulus 합을 억지로 같은 모양으로 만들기보다
sieve upper/lower bound 자체를 수정하는 방법을 제안한다. 이는 구조적으로 흥미롭지만 Maynard
Hypothesis 1(2)나 Proposition 9.2를 그대로 주는 정리가 아니다. multidimensional weight와
호환되는 새 proof가 필요하고, 2026년 최근 preprint이므로 이 프로젝트 theorem input으로는
아직 채택하지 않는다.

Johnston Lemma 3.4는 Sedunova 2019 Corollary 1.4의 작은 오류를 교정하면서 분모를
\((\log X)^{B-2}\)가 아니라 \((\log X)^{B-3}\)로 준다. 따라서 Sedunova의 인쇄식을 그대로
복사하는 경로는 금지한다.

## 5. affine mapping과 중심항 변환

\(L(n)=an+b\)이고 \(n\equiv r\pmod q\)라면

\[
L(n)\equiv ar+b\pmod{|a|q}.
\]

적합한 gcd 조건 아래 이 대응을 사용해 \(n\)-residue count를 한 prime residue class count로
옮길 수 있다. 하지만 analytic theorem의 중심항을 \(M/\phi(|a|q)\), 전체 count를
\(C_1=\#\mathcal P_{L,\mathcal A}(x)\), residue count를 \(C_q\)라고 쓰면 필요한 centered
quantity에는 적어도 다음 삼각부등식이 들어간다.

\[
\left|C_q-\frac{C_1}{\phi_L(q)}\right|
\le
\left|C_q-\frac{M}{\phi(|a|q)}\right|
+\frac{\phi(|a|)}{\phi(|a|q)}
\left|C_1-\frac{M}{\phi(|a|)}\right|.
\]

이 식은 **연결 경로를 보여주는 identity**일 뿐 아직 H1(2)의 합을 닫지 않는다. 두 번째 항을
\(q\) 전체에 더한 값, \(a<0\), 정확한 residue bijection, endpoint, prime powers와
represented-prime lower bound를 H1c-1b에서 증명해야 한다.

## 6. H1c-1b로 넘기는 최소 의무

### H1c-1b.1 — parameter와 modulus envelope

- actual construction이 finite \(k\)를 고정하는지 먼저 확정한다.
- 고정 \(k\)라면 필요한 \(A\)와 모든 Bordignon validity condition을 식으로 만든다.
- growing \(k\)가 필요하면 \(C(A,A-3,X_0)\)까지 uniform하게 상계한다.
- \(|a|q\)가 Theorem 4의 \(Q\) 이하임을 explicit inequality로 증명한다.

### H1c-1b.2 — 하나의 exceptional \(B\)

- FGKMT Lemma 7.1의 한 conductor 선택과 Bordignon의 \(q_0\) 정의를 같은 scale에 고정한다.
- 모든 endpoint·form에서 같은 largest prime factor \(B\)가 exclusion을 보장하는지 증명한다.

### H1c-1b.3 — exact transfer

- affine residue bijection, sign와 gcd case
- cumulative \(\psi\)에서 반열린 interval count
- \(\psi\to\theta\to\pi\), prime powers와 partial summation
- analytic main term에서 exact total-population 중심항으로 recentering

### H1c-1b.4 — density와 공통 cutoff

- \(\#\mathcal P_{L,\mathcal A}(x)\)의 explicit lower bound
- 절대오차를 \((\log x)^{-100k^2}\) relative error로 흡수
- P9.2의 다른 입력과 하나의 finite cutoff로 합성

## 7. 자원·실행 판단

지금 병목은 CPU가 아니라 증명 연결부다. source inventory 자체에는 prime sweep이나 장시간 계산이
필요하지 않았고 실제 experiment를 실행하지 않았다. H1c-1b.1에서 구체적인 scalar inequality가
생긴 뒤에는 FGKMT Python과 interval arithmetic으로 cutoff 후보를 검산할 수 있다.

현재 사용자 수행절차:

```text
별도 수행절차 필요없음
```

## 8. provenance와 보존

정확한 수식 대조를 위해 다음 working source를 `tmp/pdfs/h1c1a/`에 보존한다. 이들은 기존
`article/` 9편 corpus에 편입한 것이 아니라 H1c-1b가 이어 쓸 source evidence다.

| 파일 | SHA-256 |
|---|---|
| `Yamada2014_Explicit_PAP_II.pdf` | `0f0ae746b307aaa51115d8e77b03bf7c798acc6e85908ce1833e242d25f4132a` |
| `Sedunova2018_Explicit_BV.pdf` | `f10826c3a3375e221724332a7ee767608cd521e9bad2148b8d841052f03129d5` |
| `Sedunova2019_Log_Improvement_BV.pdf` | `ea329c2e62168e59084bcc3ba6c477b3c52bd02badb2c9996df0e40ea7be2132` |
| `Bordignon2021_Medium_PNTAP.pdf` | `63051c118ca19e9e723c5fe1769ef53f8c76ea7631ecadc87a08b1a385277805` |
| `BennettEtAl2018_Explicit_PAP.pdf` | `e51f8b8f63486c2259efe076d367504f08dda0fe9e99dc35bf36de544ffc0601` |
| `Kadiri2005_Explicit_ZFR.pdf` | `774e5aa5e5ad96ce263df8ae7b02258cf9bb7ea2e8d6d0300b83b53bde7d8166` |
| `Johnston2026_Effective_BV_Sifting.pdf` | `087000e6e0f890f61b030b3fd1bd1ab42b69dc219acc82850b8b7503e9f5f7b6` |

Yamada II p.2, Sedunova 2018 p.2, Bordignon pp.3--4는 PNG 렌더와 text extraction을 함께
대조했다. source 원본은 수정하지 않았다.

## 9. 엄밀한 종료 판정

```text
declared source inventory        = COMPLETE
drop-in theorem                  = NOT FOUND
primary composition candidate   = BORDIGNON2021
affine/recentering route         = IDENTIFIED, NOT PROVED
Hypothesis 1(2) numerical        = OPEN
Maynard Proposition 9.2 numeric = OPEN
SIV-07 / SIV-08                 = HARD_BLOCKER
threshold calculator            = NOT READY
X_cert                           = OPEN
```

다음 작업은 더 넓은 막연한 검색이 아니라 H1c-1b.1의 Bordignon parameter·modulus-envelope
feasibility다. 여기서 불가능 판정이 나오면 original FGKMT route 또는 Johnston식 proof redesign을
별도 branch로 검토한다.
