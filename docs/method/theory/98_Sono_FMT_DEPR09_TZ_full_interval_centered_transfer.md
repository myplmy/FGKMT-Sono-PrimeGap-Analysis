# Theory 98 — DEP-R09 Thorner--Zaman full-interval centered transfer

- 상태:
  <code>ACTUAL_B0_RELATIVE_ZFR_EXPLICIT /
  TZ_LAMBDA_ONE_BRANCH_STRUCTURAL /
  FULL_INTERVAL_CENTERING_FACTOR_2_EXACT /
  NUMERICAL_K_C_CUTOFF_OPEN</code>
- 선행 정본: Theory 57, 59, 88--90, 97, review 106
- 기계 원장:
  [TZ full-interval centered v1](data/Sono_FMT_DEPR09_TZ_full_interval_centered_v1.json)
- 목표: actual \(B_0\) zero-free exclusion을 Thorner--Zaman full-interval PNT와
  결합해 exceptional secondary main을 common main으로 structural하게 흡수하고,
  Theory 97 centered endpoint gate까지의 exact remaining numerical interface를 고정한다.
- 비목적: `effectively computable`을 numerical constant로 읽거나, Sono의
  미인증 \(3c_{\rm ZFR}\) normalization을 재사용하거나, actual 계산, threshold
  calculator, conditional branch, PAP-11, DEP-R09, numerical \(X_{\rm cert}\)를 닫는 것.

## 1. 결론

Full primorial을 \(P(X)=\prod_{p\le X}p\), actual exceptional-prime deletion을
\(B_0=B_{P(X)}\), 그리고

\[
 \mathfrak q=\frac{P(X)}{B_0},\qquad
 f\mid\mathfrak q,\qquad U=f^{d_f},\qquad d_f\ge21
 \tag{98.1}
\]

로 둔다. Character modulo \(f\)의 primitive inducing conductor \(r\)는
\(r\mid f\)이므로 \((r,B_0)=1\)이다.

Sono Proposition 5.3의 **직접 \(t=0\) 특수화**는 이 primitive source에

\[
 1-\beta\ge\frac{1}{24\log P(X)}.
 \tag{98.2}
\]

를 준다. Theory 90의 project scale은

\[
 \log f>\frac{47}{100}X,qquad
 \log P(X)=\vartheta(X)<\frac{21}{20}X,
 \tag{98.3}
\]

이므로

\[
 \boxed{
 \frac{\log f}{\log P(X)}>\frac{47}{105}.}
 \tag{98.4}
\]

식 (98.2)--(98.4)을 합치면

\[
 \boxed{
 \beta<1-\frac{c_2}{\log f},
 \qquad c_2:=\frac1{24}\frac{47}{105}
 =\frac{47}{2520}.}
 \tag{98.5}
\]

이다. 따라서 Thorner--Zaman Remark 1.3의 fixed relative zero-free branch를
\(q=f\), \(c_2=47/2520\)으로 적용할 수 있고, source statement에서

\[
 \boxed{\lambda=1,\qquad\theta=\frac7{12}}
 \tag{98.6}
\]

로 둘 수 있다. 이는 real zero의 존재 자체를 부정하는 것이 아니라, 그 zero가
\(1\)에서 uniform하게 떨어져 있으므로 secondary main을 source error에 흡수할 수
있다는 뜻이다.

Thorner--Zaman Corollary 1.4의 full-interval range는 \(U\ge f^{12}\)다. Current

\[
 \boxed{d_f\ge21>12\quad\Longrightarrow\quad U=f^{d_f}\ge f^{12}}
 \tag{98.7}
\]

이므로 range는 닫힌다.

Source에 인쇄되지 않은 positive constants와 common cutoff를
\(K_{\rm TZ},c_{\rm TZ},U_{\rm TZ}\)로 보존하고

\[
 L_{\rm VK}(U):=
 \frac{(\log U)^{3/5}}{(\log\log U)^{1/5}},
 \tag{98.8}
\]

\[
 \boxed{
 R_{\rm TZ}(U,f):=
 K_{\rm TZ}\left{
 e^{-c_{\rm TZ}d_f}+e^{-c_{\rm TZ}L_{\rm VK}(U)}
 \right}.}
 \tag{98.9}
\]

이라 하자. Full-interval source가 numerical하게 복원되면

\[
 \max_{a\bmod f}^{*}
 \left|\vartheta(U;f,a)-\frac{U}{\varphi(f)}\right|
 \le R_{\rm TZ}(U,f)\frac{U}{\varphi(f)}
 \qquad(U\ge U_{\rm TZ})
 \tag{98.10}
\]

이 된다. Reduced residues에서 합하면

\[
 \left|\vartheta_f(U)-U\right|
 \le R_{\rm TZ}(U,f)U.
 \tag{98.11}
\]

따라서 Theory 97의 centered norm은 exact하게

\[
 \boxed{
 \epsilon_\infty(U,f)\le2R_{\rm TZ}(U,f).}
 \tag{98.12}
\]

이고 whole binary-prime gate는

\[
 \boxed{
 \delta_{\rm bin}
 \le\frac{21}{5}
 \{2R_{\rm TZ}(U,f)+\epsilon_0(X,U,f)\}
 \left(2+\frac ba\right).}
 \tag{98.13}
\]

즉 exceptional branch·source range·centering normalization은 structural하게
닫혔다. 남은 analytic root는 \(K_{\rm TZ},c_{\rm TZ},U_{\rm TZ}\)의 실제 숫자다.

## 2. Actual \(B_0\)가 주는 conductor-level zero-free input

FMT Corollary 1은 \(Q=P(X)\) 이하 primitive characters에서 possible exceptional
character의 conductor에 든 prime 하나를 \(B_{P(X)}\)로 택한다. Sono Lemma 3.7의
actual application도

\[
 B_0=B_{P(X)},\qquad P=P(X)/B_0
 \tag{98.14}
\]

를 사용한다. Current \(f\mid\mathfrak q=P(X)/B_0\)이므로 primitive conductor
\(r\mid f\)는 exceptional conductor일 수 없고 Proposition 5.3의 nonexceptional
zero-free bound를 받는다.

여기서는 Theory 57이 안전하다고 판정한 Proposition 5.3 원식

\[
 1-\beta\ge
 \frac{c_{\rm ZFR}}{\log(P(X)(1+|\gamma|))},
 \qquad c_{\rm ZFR}=\frac1{24}
 \tag{98.15}
\]

만 사용했다. \(\gamma=0\)에서 분모는 정확히 \(\log P(X)\)다. Sono Section 5의
\(3c_{\rm ZFR}/\log T\) 변환이나 Gallagher multiplier는 식 (98.2)--(98.5)에
사용하지 않았다.

Near-one zero of an imprimitive character modulo \(f\)도 그 primitive inducing
character와 같은 nontrivial zero를 가진다. 따라서 conductor-level exclusion이면
Thorner--Zaman product over characters modulo \(f\)에 필요한 relative separation으로
전달된다. Imprimitive Euler factors의 zeros는 이 near-one real branch가 아니다.

## 3. 왜 centering만으로 exceptional main이 사라지지 않는가

Actual \(B_0\) input 없이 Thorner--Zaman의 full-interval exceptional main을 그대로
쓰면

\[
 \lambda_a
 =1-\chi_1(a)S_\beta(U),qquad
 S_\beta(U):=\frac{U^{\beta_1-1}}{\beta_1}.
 \tag{98.16}
\]

Nonprincipal real character는 \(\sum_a^*\chi_1(a)=0\)이므로
\(\varphi(f)^{-1}\sum_a^*\lambda_a=1\)이다. 그러나 residue별 secondary main에서
그 평균을 빼면

\[
 \boxed{
 \frac{\lambda_aU}{\varphi(f)}-
 \frac1{\varphi(f)}\sum_b^*\frac{\lambda_bU}{\varphi(f)}
 =-\chi_1(a)S_\beta(U)\frac{U}{\varphi(f)}.}
 \tag{98.17}
\]

즉 exceptional character pattern은 centered norm에서도 크기 \(S_\beta(U)\)로 남는다.
Theory 97의 centering alone이 exceptional term을 취소한다는 주장은 틀리다. 식 (98.5)와
Remark 1.3의 \(\lambda=1\) branch가 필요한 이유다.

## 4. Full interval은 Theorem 2.3 short-interval proof와 별도다

Official arXiv v2 source TeX의 proof of Theorem 2.3은 첫 문장에서 “it suffices to
consider \(h\le x-1\)”라고 제한한다. 이후 두 endpoint explicit formula, kernel
\((x^\rho-(x-h)^\rho)/\rho\), local zero count, dyadic decomposition을 사용한다.

반면 \(h=x\)는 source의 Corollary 1.4로 별도 인쇄돼 있다. 그 statement는

\[
 \vartheta(x;q,a)
 =\frac{\lambda_ax}{\varphi(q)}
 \left[1+O\left{
 e^{-c_4\log x/\log q}
 +e^{-c_4L_{\rm VK}(x)}
 \right}\right],qquad x\ge q^{12},
 \tag{98.18}
\]

이고 implied multiplier와 \(c_4\)는 absolute and effectively computable이라고만
말한다. 식 (98.6)을 적용한 뒤 \(q=f,x=U\)로 놓으면 식 (98.9)--(98.10)의 shape가
나온다.

따라서 centered endpoint route에는 short-interval factor \(\sqrt{x/h}\), 두 endpoint
subtraction, lower endpoint dyadic split을 별도로 지불할 필요가 없다. 그러나 Corollary
1.4도 Theorem 2.1 density와 Vinogradov--Korobov optimization의 숨은 constants를
상속하므로 numerical certificate는 아니다.

Official source archive SHA-256은

~~~text
bd8d3cdfe1ec1880bfed2b8275e51f8920b6e0e0d8eba609482e8b5430794610
~~~

이고 archive 안 TeX SHA-256은

~~~text
23348e767689fd971c5b696d35bd05fe948ffd4b6f24d7ed093bae3ffddab6ba
~~~

다.

## 5. Common-main error에서 centered error로

\[
 e_a:=\vartheta(U;f,a)-\frac{U}{\varphi(f)},qquad
 \bar e:=\frac1{\varphi(f)}\sum_b^*e_b
 \tag{98.19}
\]

로 두면 \(E_f(U;a)=e_a-\bar e\)다. 식 (98.10)에서

\[
 |e_a|\le R_{\rm TZ}\frac{U}{\varphi(f)},qquad
 |\bar e|\le R_{\rm TZ}\frac{U}{\varphi(f)}.
 \tag{98.20}
\]

따라서

\[
 \frac{\varphi(f)}U|E_f(U;a)|
 \le\frac{\varphi(f)}U(|e_a|+|\bar e|)
 \le2R_{\rm TZ},
 \tag{98.21}
\]

즉 식 (98.12)가 exact하다. 이 factor 2는 finite centering의 universal envelope이며
source error를 1로 축소하지 않는다.

## 6. 남은 numerical proof-DAG

| ID | 최초 미수치 edge | 이번 판정 | 닫힘 조건 |
|---|---|---|---|
| `TZ-FI-N01` | Huxley--Jutila exponent \(12/5\) density multiplier·start | <code>OPEN</code> | 공식 finite upper |
| `TZ-FI-N02` | explicit formula·prime-power·local zero-count constants | <code>OPEN</code> | full-interval absolute error budget |
| `TZ-FI-N03` | numerical VK \(c_8\)와 \(c_{\rm TZ}\) optimization | <code>OPEN</code> | explicit zero-free source·calculus |
| `TZ-FI-N04` | range·absorption·centering의 common \(U_{\rm TZ}\) | <code>OPEN</code> | N01--N03 cutoff maximum |

Theorem 2.1은 \(N_q(\sigma,T)\ll_\varepsilon
(qT)^{(12/5+\varepsilon)(1-\sigma)}\)를 Huxley와 Jutila의 work에서
“well-known”이라고만 인용한다. Source TeX에도 multiplier와 최초 적용점은 없다.
따라서 식 (98.5)의 exceptional repair가 N01을 자동으로 닫지는 않는다.

## 7. 상태표

| 항목 | 판정 |
|---|---|
| actual \(B_0\) conductor exclusion | <code>EXACT SOURCE MAPPING</code> |
| relative zero-free \(c_2=47/2520\) | <code>EXPLICIT</code> |
| TZ \(\lambda=1,\theta=7/12\) branch | <code>STRUCTURALLY APPLICABLE</code> |
| full-interval \(U\ge f^{12}\) range | <code>CLOSED BY \(d_f\ge21\)</code> |
| pointwise-to-centered factor 2 | <code>EXACT</code> |
| \(K_{\rm TZ},c_{\rm TZ},U_{\rm TZ}\) | <code>OPEN</code> |
| Theory 97 endpoint gate | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 8. 검증 범위

<code>source/dep_r09_tz_full_interval_centered.py</code>와 tests는 \(47/2520\) rational
transfer, \(21\ge12\) range, common-main error centering factor 2, exceptional character
pattern counterfixture와 Theory 97 multiplier composition을 exact하게 검사한다. Actual
prime sums, zeros 또는 long computation은 수행하지 않는다.

Lean은 external zero-free/PNT theorem을 local axiom으로 넣지 않고 \(47/2520\), range,
centering triangle과 project scalar composition만 검사한다.

## 9. 다음 gate

다음 최소 gate는 식 (98.9)의 \(K_{\rm TZ},c_{\rm TZ},U_{\rm TZ}\)를 numerical하게
복원하는 것이다. Source-first 순서는

1. nonexceptional Huxley--Jutila density multiplier·cutoff의 explicit replacement,
2. full-interval explicit-formula constants와 numerical VK source,
3. 식 (98.13)의 actual success budget 대입

이다. 숫자가 생기기 전에는 threshold calculator를 만들지 않는다.

## 10. 참고문헌

- J. Thorner and A. Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878),
  Remark 1.3, Corollary 1.4, Theorems 2.1 and 2.3.
- K. Sono,
  [*An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes*](https://doi.org/10.4418/2025.80.2.2),
  equations (3.5)--(3.8), Proposition 5.3.
- K. Ford, J. Maynard and T. Tao,
  [*Chains of Large Gaps Between Primes*](https://arxiv.org/abs/1511.04468),
  Section 2, Corollary 1 and Lemma 3.1.
