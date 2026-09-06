# Sono/FMT H1b-1a explicit cutoff·초등 summation package

- 작성일: 2026-09-04
- 대상: Maynard Proposition 6.1의 Lemmas 8.1–8.2 입력 중 명시적 cutoff와 초등 합·소수곱
- 판정: THREE_FINITE_COMPONENTS_CLOSED_PARAMETERIZED_DIVISOR_MAJORANT_DERIVED
- SIV-07: HARD_BLOCKER 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): OPEN
- 기계 판독 정본:
  [data/Sono_FMT_H1b1a_explicit_cutoff_summation_v1.json](data/Sono_FMT_H1b1a_explicit_cutoff_summation_v1.json)
- 검증 구현: [source/h1b1a_explicit_package.py](../../../source/h1b1a_explicit_package.py)

## 1. 결론부터

이번 단계에서는 다음 세 항목을 **프로젝트 유한 보조정리**로 닫았다.

1. Maynard가 존재만 요구한 cutoff를 구체적인 \(C^\infty\) 함수로 고정하고
   \(\|\psi'\|_\infty\le 50\)을 증명했다.
2. Lemma 8.1(i)의 singular-series 하한에서 숨겨진 지수 상수를 보수적으로
   \[
   \boxed{\mathfrak S_B(\mathcal L)>e^{-9k/2}}
   \]
   로 만들었다.
3. Lemma 8.1(ii)의 식 (8.5)에 등장하는 Euler product를 모든 정수 \(k\ge2\)에서
   \[
   \boxed{E(k)<24\log k}
   \]
   로 만들었다.

또한 Lemma 8.1(ii)의 나머지 큰-divisor 항에 대해 입력이 모두 숫자로 주어지면 바로 평가할 수
있는 유한 상계식을 유도했다. 그러나 Maynard 원문의 \(|a|\ll1\),
\(|b_i|\ll\log x\)에 들어 있는 상수와 그 상계식을 목표 error budget에 흡수시키는 공통
cutoff는 아직 숫자가 아니다. 따라서 Lemma 8.1(ii), Lemma 8.2 전체, Proposition 6.1,
good sieve weight 및 \(X_{\mathrm{cert}}\)는 닫히지 않았다.

쉽게 말하면, “부품 세 개를 실제 치수로 제작했다”는 진전이지 “전체 기계를 조립해 작동시켰다”는
결과는 아니다.

## 2. 1차 출처와 provenance

### 2.1 Maynard 출판본

James Maynard, [*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
*Compositio Mathematica* 152 (2016), 1517–1554, arXiv
[1405.2593](https://arxiv.org/abs/1405.2593).

- 검토 위치: (7.10), Lemma 8.1과 (8.1)–(8.5), Lemma 8.2와 (8.6)–(8.8),
  Lemmas 8.3–8.4
- 취득 URL: https://compositio.nl/Content/prize2018_maynard.pdf
- 로컬 검토본: tmp/pdfs/h1b1a/Maynard2016_Dense_Clusters_published.pdf
- SHA-256: 8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098

출판본은 \(\psi:[0,\infty)\to[0,1]\)가 smooth, non-increasing, \([0,1]\)에
지지되고 \([0,9/10]\)에서 1이라고 요구하지만 식과 norm은 주지 않는다. Lemma 8.1(i)는
\(e^{-Ck}\)의 존재만 주고 \(C\)는 주지 않는다.

### 2.2 Dusart의 명시적 소수함수 부등식

Pierre Dusart, [*Estimates of Some Functions Over Primes without R.H.*](https://arxiv.org/abs/1002.0442),
arXiv:1002.0442 (2010); 후속 출판본은
[*The Ramanujan Journal* 45 (2018), 227–251](https://doi.org/10.1007/s11139-016-9839-4).

- 사용 위치: Theorem 5.2의 \(j=0\) 행, Theorems 6.11–6.12
- 취득 URL: https://arxiv.org/pdf/1002.0442
- 로컬 검토본: tmp/pdfs/h1b1a/Dusart2010_Explicit_estimates_over_primes.pdf
- SHA-256: 3f11eca84613ad00e6a447f99b318d5c3d76e360283efcc6d3eebdda25ff3923

Theorem 5.2의 \(j=0\) 행은 \(x\ge1\)에서
\(|\vartheta(x)-x|<x\)를 준다. 원문의 경계 표기를 보수적으로 해석해 Theorem 6.12는
\(x>2973\)에서

\[
\prod_{p\le x}\frac p{p-1}
<e^\gamma\log x\left(1+\frac{0.2}{\log^2x}\right)
\]

을 준다. Theorem 6.11은 보수적으로 \(x>2974\)에서

\[
\sum_{p\le x}\frac{\log p}{p}
\le \log x+E+\frac{0.2}{\log x}+\frac{0.2}{\log^2x},
\qquad E<0
\]

을 준다.

### 2.3 Rosser–Schoenfeld totient bound

J. Barkley Rosser and Lowell Schoenfeld,
[*Approximate Formulas for Some Functions of Prime Numbers*](https://doi.org/10.1215/ijm/1255631807),
*Illinois Journal of Mathematics* 6 (1962), 64–94.

- 사용 위치: Theorem 15, 식 (3.41)–(3.42), proof pp. 88–89
- 취득 URL: Project Euclid의 DOI 고정 PDF
- 로컬 검토본: tmp/pdfs/h1b1a/Rosser_Schoenfeld_1962_Approximate_formulas.pdf
- SHA-256: 8e37b06f82e09421bceb2502578c47b61469141f0287e6acedb70e01765ab556

모든 정수 \(n\ge3\)에 대해 예외 한 값을 포함해 하나의 보수적 식으로 쓰면

\[
\boxed{
\frac n{\varphi(n)}
<e^\gamma\log\log n+
\frac{2.50637}{\log\log n}
}
\]

을 사용할 수 있다. 일반 식의 분자는 \(5/2\)이고 한 예외에서 \(2.50637\)이므로, 후자를
전 범위에 쓰는 것은 안전한 약화다.

## 3. H1b-1a cutoff 보조정리

### 3.1 함수의 정의

\[
b(u)=
\begin{cases}
e^{-1/u},&u>0,\\
0,&u\le0,
\end{cases}
\qquad
\sigma(u)=\frac{b(u)}{b(u)+b(1-u)}.
\]

분모는 모든 실수 \(u\)에서 양수다. 표준 flat-function 성질로
\(b\in C^\infty(\mathbb R)\)이고 \(u=0\)의 모든 도함수는 0이다. 따라서
\(\sigma\in C^\infty(\mathbb R)\)이며

\[
\sigma(u)=0\ (u\le0),\qquad
\sigma(u)=1\ (u\ge1),\qquad
0\le\sigma\le1.
\]

Maynard용 함수는 \(t\ge0\)에서

\[
\boxed{\psi(t)=\sigma(10(1-t))}
\]

로 고정한다. 그러면 \(\psi\)는 non-increasing이고 \([0,1]\)에 지지되며
\([0,9/10]\)에서 정확히 1이다.

### 3.2 첫 도함수의 명시적 상계

\(0<u<1\)에서 직접 미분하면

\[
\sigma'(u)=\sigma(u)(1-\sigma(u))
\left(\frac1{u^2}+\frac1{(1-u)^2}\right).
\]

\(\sigma'(u)=\sigma'(1-u)\)이므로 \(0<u\le1/2\)만 보면 된다.

- \(1/4\le u\le1/2\)에서는
  \(\sigma(1-\sigma)\le1/4\)이고 괄호는 \(160/9\) 이하이므로
  \(\sigma'(u)\le40/9<5\)다.
- \(0<u\le1/4\)에서는
  \(\sigma(u)\le\exp(4/3-1/u)\)이고 괄호는 \(10/(9u^2)\) 이하이다.
  \(v=1/u\ge4\)에서 \(v^2e^{-v}\)는 감소하므로
  \[
  \sigma'(u)\le\frac{160}{9}e^{-8/3}
  <\frac{32}{13}<5.
  \]
  마지막 부등식에는
  \(e^{8/3}>1+8/3+(8/3)^2/2=65/9\)만 사용했다.

따라서

\[
\boxed{\|\sigma'\|_\infty<5,
\qquad \|\psi'\|_\infty<50.}
\]

Maynard (8.6)에서 실제로 쓰는 것은 함수값과 첫 도함수의 Lipschitz 제어다. \(C^\infty\)
성질은 모든 고계 도함수의 존재를 보장하지만, 이번 단계는 원문에서 아직 사용하지 않은 고계
도함수마다 숫자 norm을 임의로 만들지는 않는다.

판정:

~~~text
H1B1-L82-CUTOFF   = PROJECT_FINITE_COMPONENT_CLOSED
H1B1-L82-LIPSCHITZ = RATE_MISSING
~~~

두 번째 행이 남는 이유는 \(\|\psi'\|_\infty\) 자체가 아니라, (7.12)의 \(F_2\) 전체에서
여러 인자와 \(T_k,U_k\)가 이 norm을 어떻게 증폭하는지에 대한 하나의 숫자 multiplier가 아직
합성되지 않았기 때문이다.

## 4. Lemma 8.1(i): \(C=9/2\)의 project proof

Maynard (8.1)–(8.2)에 따라

\[
\mathfrak S_B(\mathcal L)\ge
\prod_{p\le2k}\frac1p
\prod_{p>2k}
\left(1-\frac{k}{p}\right)
\left(1-\frac1p\right)^{-k}.
\]

### 4.1 작은 소수 부분

\(\vartheta(y)=\sum_{p\le y}\log p\)라 하면

\[
\prod_{p\le2k}\frac1p=e^{-\vartheta(2k)}.
\]

Dusart Theorem 5.2의 \(j=0\) 행에서 \(y\ge1\)이면
\(\vartheta(y)<2y\)다. 따라서 모든 정수 \(k\ge1\)에서

\[
\boxed{\prod_{p\le2k}\frac1p>e^{-4k}.}
\]

### 4.2 큰 소수 tail

\(p>2k\), \(y=k/p<1/2\)라 하자. 급수의 모든 항이 양수이므로

\[
\log(1-y)
\ge-y-\frac{y^2}{2(1-y)},
\qquad
-k\log(1-1/p)\ge\frac{k}{p}=y.
\]

따라서 한 tail factor의 로그는

\[
\log\left[
\left(1-\frac{k}{p}\right)
\left(1-\frac1p\right)^{-k}
\right]
>-\frac{k^2}{p^2}.
\]

또한

\[
\sum_{p>2k}\frac1{p^2}
<\sum_{n=2k+1}^\infty\frac1{n(n-1)}
=\frac1{2k}.
\]

그러므로 tail product는 \(e^{-k/2}\)보다 크다. 두 부분을 곱하면

\[
\boxed{\mathfrak S_B(\mathcal L)>e^{-(4+1/2)k}=e^{-9k/2}.}
\]

이 부등식은 매우 보수적이지만 \(B\)와 admissible set의 구체적인 모양에 무관하고, hidden
\(O\)-상수나 “sufficiently large”를 포함하지 않는다.

판정:

~~~text
H1B1-L81-SMALL = PROJECT_FINITE_COMPONENT_CLOSED
H1B1-L81-TAIL  = PROJECT_FINITE_COMPONENT_CLOSED
H1B-L81        = RATE_MISSING
~~~

마지막 parent 행이 남는 이유는 Lemma 8.1(ii)도 같은 행에 들어 있기 때문이다.

## 5. 식 (8.5)의 Euler product

Maynard의 첫 번째 divisor-sum 항에 나타나는 곱을

\[
E(k)=
\prod_{p\le k}\left(1+\frac1{p-1}\right)
\prod_{p>k}\left(1+\frac{k}{p(p-1)}\right)
\]

라 하자.

큰 소수 부분은 \(\log(1+z)\le z\)와 망원합으로

\[
\log\prod_{p>k}\left(1+\frac{k}{p(p-1)}\right)
\le k\sum_{n=k+1}^\infty\frac1{n(n-1)}=1,
\]

따라서 이 곱은 \(e<3\)보다 작다.

작은 소수 부분은 두 범위로 나눴다.

- \(2\le k\le2973\): exact rational로 모든 정수를 검사했다. 각 \(k\)에서
  \[
  \prod_{p\le k}\frac p{p-1}
  <\frac{16(k-1)}{k+1}\le8\log k.
  \]
  두 번째 부등식은
  \(\log k\ge2(k-1)/(k+1)\)에서 온다. 이 유한 검사는 2,972개 값을 빠짐없이 다루며
  binary float를 쓰지 않는다.
- \(k\ge2974\): Dusart Theorem 6.12와
  \(\gamma<1,e<3,\log k>1\)을 쓰면
  \[
  \prod_{p\le k}\frac p{p-1}
  <e^\gamma\log k\left(1+\frac{0.2}{\log^2 k}\right)
  <4\log k<8\log k.
  \]

따라서 모든 정수 \(k\ge2\)에서

\[
\boxed{E(k)<24\log k.}
\]

## 6. Lemma 8.1(ii)의 parameterized finite majorant

이 절은 문헌의 \(\ll\)를 모두 닫았다고 주장하지 않는다. 대신 숨은 입력 상수를 숫자로 정한 뒤
무엇을 계산해야 하는지 정확한 유한식으로 바꾼다.

\[
Y=\eta\log x>1,
\qquad
\Delta_b=|a|^{k+1}\prod_{i=1}^k|b_i-b|,
\]

라 하자. 여기서 \(a\)는 0이 아닌 정수이고
\(L=an+b\notin\mathcal L\)이므로 \(\Delta_b\ge1\)이다. 모든 허용 \(b\)에 대해
\(M\ge\max(16,\Delta_b)\)인 정수 상계를 알고 있다고 하자. 다음을 둔다.

\[
A_\varphi=\frac{|a|}{\varphi(|a|)},\quad
L_M=\max(1,\log\log M),\quad
Z_M=\max(2975,\log M),
\]

\[
U(M)=3L_M+2.50637,
\qquad
V(M)=\log Z_M+2.
\]

Rosser–Schoenfeld Theorem 15와 \(\gamma<1,\ e<3\), 그리고 \(n<16\)의 exact check를 합치면
\(1\le n\le M\)에서

\[
\frac n{\varphi(n)}<U(M).
\]

여기서 \(\gamma<1\)은 \(H_m-\log m<1\)의 극한에서, \(e<3\)은
\(n!\ge2^{n-1}\)인 지수급수의 기하급수 상계에서 바로 얻으므로 새 수치 가정을 넣지 않는다.

Dusart Theorem 6.11을 \(Z_M\)까지의 소수에 적용하고 큰 소인수에는
\(1/p\le1/Z_M\)를 쓰면

\[
\sum_{p\mid n}\frac{\log p}{p}<V(M).
\]

이제 \(n/\varphi(n)=\sum_{d\mid n}\mu^2(d)/\varphi(d)\)에서 \(d\le Y\)와
\(d>Y\)를 나눈다. 첫 부분은 한 residue class 안의 정수 개수가 \(3Y/d\) 이하라는 정확한
상계와 \(E(k)<24\log k\)를 쓴다. 두 번째 부분은
\(1_{d>Y}<\log d/\log Y\)를 쓴다. 그 결과

\[
\boxed{
\sum_{\substack{|b|\le Y\\an+b\notin\mathcal L}}
\frac{\Delta_b}{\varphi(\Delta_b)}
<72A_\varphi Y\log k+
\frac{3Y\,U(M)V(M)}{\log Y}.
}
\]

예를 들어

\[
3U(M)V(M)\le\log Y\log k
\]

까지 별도로 증명하면 오른쪽은
\((72A_\varphi+1)Y\log k\) 이하가 된다. 또한 입력에

\[
|a|\le A_0,\qquad |b_i|\le B_0\log x
\]

가 숫자로 주어지면

\[
M=\left\lceil A_0^{k+1}\big((B_0+\eta)\log x\big)^k\right\rceil
\]

로 택할 수 있다.

### 왜 아직 Lemma 8.1(ii) 전체 PASS가 아닌가

Maynard가 이 위치에서 쓰는 \(|a|\ll1\), \(|b_i|\ll\log x\)는 고정된 의존관계만
말하고 \(A_0,B_0\)의 숫자를 주지 않는다. 또한 위 sufficient condition을 Proposition 6.1의
허용 \(k,\eta,x\) 전 범위와 하나의 공통 시작점으로 합쳐야 한다. 그래서 현재 판정은

~~~text
H1B1-L81II-DIVISOR = PARTIAL_EXPLICIT
~~~

이다.

## 7. 정확히 무엇이 닫혔고 무엇이 남았는가

| 항목 | 이전 | 현재 | threshold 영향 |
|---|---|---|---|
| H1B1-L81-SMALL | CONSTRUCTIVE_SUBPROBLEM | PROJECT_FINITE_COMPONENT_CLOSED | \(e^{-4k}\) 입력 확보 |
| H1B1-L81-TAIL | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | \(e^{-k/2}\) 입력 확보 |
| H1B1-L82-CUTOFF | CONSTRUCTIVE_SUBPROBLEM | PROJECT_FINITE_COMPONENT_CLOSED | \(\|\psi'\|_\infty<50\) 확보 |
| H1B1-L81II-DIVISOR | RATE_MISSING | PARTIAL_EXPLICIT | parameterized majorant만 확보 |
| H1B1-L82-LIPSCHITZ | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | H1b-1b에서 multiplier 89 |
| H1B1-L83-GGPY4 | SOURCE_CHAIN_TRACED | PARAMETERIZED_EXPLICIT | \(C_4\le2C_3\) |
| H1B1-L83-GGPY3 | LOWER_SOURCE_REVIEW_REQUIRED | SOURCE_ACCESS_BLOCKED | HR 144–152쪽 필요 |
| H1B1-L84-* | open | open | 반복오차·공통 cutoff 없음 |
| H1B1-PACKAGE | HARD_BLOCKER | HARD_BLOCKER | 변화 없음 |

따라서 다음 추론은 금지한다.

~~~text
H1b-1a 부분 closure
  -> Maynard Proposition 6.1 numerical PASS
  -> FMT/Sono numerical threshold 계산 가능
~~~

올바른 상태는 다음과 같다.

~~~text
cutoff + Lemma 8.1(i) + (8.5) Euler product = explicit
Lemma 8.1(ii) common range                  = open
Lemma 8.2 full Lipschitz multiplier         = 89 closed by H1b-1b
GGPY Lemma 4 transfer                      = C4 <= 2 C3 parameterized
HR C3 + Lemma 8.4 composition              = open
SIV-07 / X_cert                            = open
~~~

## 8. 검증 계약과 한계

tests/test_h1b1a_explicit_package.py는 다음을 fail-closed로 검사한다.

- \(2\le k\le2973\)의 exact rational prime-product 비교 2,972개가 모두 PASS인가
- finite certificate row digest와 최대 witness가 정본 JSON과 일치하는가
- tail의 rational majorant와 망원합 identity가 맞는가
- cutoff의 plateau/support/range/monotonicity와 analytic derivative formula가 구현에 반영됐는가
- H1b-1b에서 Lemma 8.2가 추가로 닫혀도 parent package, SIV-07,
  \(X_{\mathrm{cert}}\)가 계속 false인가

cutoff grid 검사는 구현 회귀검사일 뿐 \(C^\infty\) 또는 전 구간 sup bound의 증명이 아니다.
그 증명은 §3의 기호 부등식이다. exact prime-product 검사는 외부 maximal-gap 데이터나 actual
prime sweep이 아니며 2,972개의 데이터 비의존 보조정리 검증이다.

Lean과 새 Python 라이브러리는 이번 단계에 필요하지 않았다. 향후 전체 chain을 proof assistant로
옮기는 별도 단계가 승인되면, 필요한 도구·용량·설치 명령을 사용자에게 먼저 요청한다.

## 9. 다음 proof gate

1. **H1b-1b 계속 (권장):** Lemma 8.2 multiplier 89와 GGPY transfer factor 2는
   완료됐다. Halberstam–Richert Lemmas 5.3–5.4의 \(C_3(A_1,A_2)\)·유효범위를
   복원하고 Lemma 8.4에 합성한다.
2. **H1c-1 (병렬 이론축):** quantitative character/PAP package를 정식화한다.
3. 위 두 축이 닫힌 뒤에만 Lemma 8.4의 \(r\)-fold error와 공통 \((k,R,x)\) cutoff를 합친다.
4. 모든 root dependency가 닫히기 전에는 threshold calculator나 장시간 prime sweep을 만들지 않는다.

사용자에게는 합법적으로 보유한 *Sieve Methods* 인쇄 144–152쪽 제공이 필요하다.

~~~text
실행 명령어는 없다. 해당 PDF·스캔·사진을 대화에 첨부하거나 프로젝트 경로를 알려 준다.
~~~
