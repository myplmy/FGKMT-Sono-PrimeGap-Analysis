# Theory 95 — DEP-R09 conductor-weighted character dual 감사

- 상태:
  <code>CHARACTER_CONDUCTOR_DUAL_EXACT /
  PRIME_SUPPORTED_LARGE_SIEVE_RANGE_PARTIAL /
  SEPARATE_L2_CERTIFICATE_TOO_COARSE /
  WEIGHTED_PRODUCT_OPEN</code>
- 선행 정본: Theory 84, 89, 94, review 103
- 기계 원장:
  [conductor weighted dual v1](data/Sono_FMT_DEPR09_conductor_weighted_dual_v1.json)
- 목표: Theory 94의 centered binary-prime form을 character·primitive conductor별로
  exact dualize하고, prime-supported large-sieve source를 별도 L2 방식으로 합성할 때
  current gate를 인증할 수 있는지 판정한다.
- 비목적: source의 implicit constant를 1로 선언하거나, separate-L2 certificate의
  실패를 actual weighted product의 하한으로 바꾸거나, actual 계산, threshold
  calculator, conditional branch, PAP-11, DEP-R09, numerical \(X_{\rm cert}\)를 닫는 것.

## 1. 결론

Theory 94의 prime core는

\[
 {\cal C}_f
 =\sum_{q\in Q'}\sum_{\substack{X<p\le U\\p\ \mathrm{prime}}}
 (\log p)K_f(p,q).
 \tag{95.1}
\]

Reduced primes \(p,q\)에 finite character orthogonality를 적용하면

\[
 K_f(p,q)
 =\sum_{\substack{\chi\bmod f\\\chi\ne\chi_0}}
 \chi(p)\overline{\chi(q)}.
 \tag{95.2}
\]

다음 두 coefficient를 둔다.

\[
 C_\chi(Q'):=\sum_{q\in Q'}\overline{\chi(q)},\qquad
 Z_\chi(X,U):=\sum_{\substack{X<p\le U\\p\ \mathrm{prime}}}(\log p)\chi(p).
 \tag{95.3}
\]

그러면 exact하게

\[
 \boxed{
 {\cal C}_f
 =\sum_{\substack{\chi\bmod f\\\chi\ne\chi_0}}
 C_\chi(Q')Z_\chi(X,U).}
 \tag{95.4}
\]

모든 character modulo \(f\)는 unique primitive core
\(\chi^*\bmod r\), \(r\mid f\)를 갖는다. 모든 summation prime은 \(>X\)이고
\(f\)의 prime factors는 \(\le X\)이므로 induction correction 없이

\[
 \boxed{
 {\cal C}_f
 =\sum_{\substack{r\mid f\\r>1}}
 \sum_{\chi^*\bmod r}^{*}
 C_{\chi^*}(Q')Z_{\chi^*}(X,U).}
 \tag{95.5}
\]

Conductor-level small-prime coefficient energy를

\[
 A_r:=\sum_{chi^*\bmod r}^{*}|C_{\chi^*}(Q')|^2
 \tag{95.6}
\]

라 하면 exact primitive orthogonality는

\[
 \boxed{
 A_r=
 \sum_{d\mid r}\mu(r/d)\varphi(d)
 \sum_{a\bmod d}N_d(a)^2,}
 \qquad
 N_d(a):=\#\{q\in Q':q\equiv a\pmod d\}.
 \tag{95.7}
\]

전체 nonprincipal energy는 여전히

\[
 \boxed{
 \sum_{\substack{r\mid f\\r>1}}A_r
 =N\{\varphi(f)-N\}.}
 \tag{95.8}
\]

다. Conductor split은 exact하지만 coefficient energy를 줄이지 않는다.

Large-prime energy를

\[
 V_{\mathbb P}:=
 \sum_{\substack{r\mid f\\r>1}}
 \sum_{\chi^*\bmod r}^{*}|Z_{\chi^*}(X,U)|^2
 \tag{95.9}
\]

라 하면 separate Cauchy certificate는

\[
 \boxed{
 |{\cal C}_f|^2
 \le N\{\varphi(f)-N\}V_{\mathbb P}.}
 \tag{95.10}
\]

Schlage--Puchta Theorem 2는 \(U>f^{2+\varepsilon}\)에서 prime-supported large
sieve를 주므로 current \(U=f^{d_f}\), \(d_f\ge21\)의 **large-prime axis** range에는
들어간다. 그러나 source constant는 implicit이고, 가장 낙관적으로
\(V_{\mathbb P}\le U^2\)를 가정해도 식 (95.10)의 normalized square는

\[
 \boxed{
 \frac{|{\cal C}_f|^2}{N^2U^2}
 \le\frac{\varphi(f)-N}{N}.}
 \tag{95.11}
\]

Project range에서 \(\varphi(f)>2N\)이므로 이 **upper certificate**는 1보다 크다.
따라서 separate L2 합성만으로 small centered gate를 인증할 수 없다.

이는 actual \({\cal C}_f\)가 크다는 하한이 아니다. 다음 input은
\(C_{\chi^*}(Q')\)와 \(Z_{\chi^*}(X,U)\)의 signed correlation을 보존하는 direct
weighted-product theorem이다.

## 2. character dualization

식 (95.2)는 all-character orthogonality에서 principal term 1을 뺀 것이다.
식 (95.1)에 넣고 finite sums를 교환하면 식 (95.4)가 나온다.

Character \(\chi\bmod f\)가 primitive \(\chi^*\bmod r\)에서 유도됐다고 하자.
\(q\in Q'\), \(X<p\le U\)는 모두 \(f\)와 coprime이다. 따라서

\[
 \chi(q)=\chi^*(q),\qquad \chi(p)=\chi^*(p).
 \tag{95.12}
\]

Theory 90에서 필요했던 removed-prime-power correction은 여기 prime-supported
\(p,q>X\)에는 생기지 않는다. Unique conductor partition으로 식 (95.5)가 나온다.

## 3. conductor-level coefficient energy

All characters modulo \(d\)의 orthogonality는

\[
 \sum_{\chi\bmod d}
 \left|\sum_{q\in Q'}\overline{\chi(q)}\right|^2
 =\varphi(d)\sum_{a\bmod d}N_d(a)^2.
 \tag{95.13}
\]

All characters를 primitive conductor별로 partition한 뒤 divisor Möbius inversion을
적용하면 식 (95.7)이 나온다.

\(Q'<f\)라 distinct \(q\)들은 modulo \(f\)에서도 distinct하다. 따라서 all-character
energy는 \(\varphi(f)N\), principal energy는 \(N^2\)이고 식 (95.8)이 나온다.

이 identity는 future source를 어디에 넣어야 하는지 정밀화한다. Small-prime AP theorem은
각 \(A_r\) 또는 weighted conductor block을 줄여야 하며, conductor level 개수만 세는
것으로는 부족하다.

## 4. Schlage--Puchta prime-supported large sieve

새로 확인한 primary source는 J.-C. Schlage-Puchta,
*Primes in short arithmetic progressions*, arXiv:1105.1623v1이다. Local PDF는
5 pages이고 SHA-256은

~~~text
51af128d287a021305412213b3828439dddd70a6bed8266134fac6d95b6705ac
~~~

이다.

Theorem 2는 \(N_0>Q^{2+\varepsilon}\)에서 prime-supported coefficients에

\[
 \sum_{r\le Q}\sum_{\chi^*\bmod r}^{*}
 \left|\sum_{p\le N_0}a_p\chi^*(p)\right|^2
 \ll_\varepsilon
 \frac{N_0}{\log N_0}
 \sum_{p\le N_0}|a_p|^2
 \tag{95.14}
\]

를 준다. \(N_0=U\), \(Q=f\),
\(a_p=(\log p)1_{\{X<p\le U\}}\)로 두면 range condition은
\(d_f>2+\varepsilon\)다. 예를 들어 \(\varepsilon=1\)에서 current \(d_f\ge21\)은
충분하다.

Theory 55의 theta upper로

\[
 \sum_{X<p\le U}(\log p)^2
 \le(\log U)\vartheta(U)
 <\frac{21}{20}U\log U.
 \tag{95.15}
\]

따라서 source는 어떤 implicit \(C_{\rm SP}(\varepsilon)>0\)에

\[
 V_{\mathbb P}
 \le\frac{21}{20}C_{\rm SP}(\varepsilon)U^2
 \tag{95.16}
\]

형태의 certificate를 준다. Divisor conductors만 합하면 full \(r\le f\) sum보다
작으므로 방향은 안전하다. 하지만 source는 multiplier와 finite cutoff를 numerical하게
고정하지 않는다.

더 중요한 점은 multiplier를 낙관적으로 1로 낮춰도 식 (95.11)의
\((\varphi(f)-N)/N\)이 남는다는 것이다.

## 5. project normalized barrier

Theory 51·53에서 \(N<X^2\)다. 한편 Theory 89--90의
\(f>e^{47X/100}\)와 Rosser--Schoenfeld/Mertens product lower를 합치면 existing child에서

\[
 \varphi(f)>2X^2>2N.
 \tag{95.17}
\]

이는 exponential versus polynomial의 explicit child inequality이며 새 threshold
search가 아니다.

식 (95.10)에 optimistic \(V_{\mathbb P}\le U^2\)를 넣으면

\[
 \frac{N\{\varphi(f)-N\}U^2}{N^2U^2}
 =\frac{\varphi(f)-N}{N}>1.
 \tag{95.18}
\]

따라서 source upper가 actual target보다 큰 certificate라는 뜻이다. Actual
\(V_{\mathbb P}\)나 \({\cal C}_f\)의 하한이 아니다.

## 6. small-prime axis의 range mismatch

Theorem 2를 \(C_\chi(Q')\) 축에 full modulus \(Q=f\), prime length \(N_0=Y\)로
적용하려면

\[
 Y>f^{2+\varepsilon}
 \tag{95.19}
\]

가 필요하다. 실제는 Theory 89의 \(Y<X^2<f\)이므로 정반대다.

Theorem 3과 Corollary 5는 single modulus/character에 Burgess형 보완을 제공한다.
Cubefree conductor \(r\)에서 Corollary 5가 nontrivial한 small-prime range는

\[
 Y>r^{3/4},\qquad r<Y^{4/3}.
 \tag{95.20}

\]

뿐이다. 이는 low-conductor slice에는 관련 있지만, high conductors 전체와 growing
number of characters를 numerical하게 합치지 않는다. Theorem 3의
\(c_{k,\varepsilon}\)도 implicit이고 growing \(k\)에 uniform한 source가 아니다.

## 7. 필요한 weighted theorem

Separate energy route는

\[
 \left(\sum A_r\right)
 \left(\sum V_r\right)
 \tag{95.21}
\]

를 지불한다. Current target은 훨씬 약한 signed sum

\[
 \boxed{
 \left|
 \sum_{\substack{r\mid f\\r>1}}
 \sum_{\chi^*\bmod r}^{*}
 C_{\chi^*}(Q')Z_{\chi^*}(X,U)
 \right|<\delta_{\mathrm{bin}}NU.}
 \tag{95.22}
\]

이다. 필요한 theorem은 다음 중 하나여야 한다.

1. conductor block별 \(\sum C_\chi Z_\chi\) direct dispersion,
2. large \(Z_\chi\)인 characters에서 \(C_\chi(Q')\)가 작은 joint large-value theorem,
3. actual primorial divisor family와 prime coefficients를 동시에 쓰는 weighted large sieve.

Checked source는 separate prime-supported L2를 주지만 이 joint statement는 주지 않는다.

## 8. 상태표

| 항목 | 판정 |
|---|---|
| character dual | <code>EXACT FINITE</code> |
| primitive conductor dual | <code>EXACT</code> |
| conductor-level coefficient energy | <code>EXACT</code> |
| large-prime Schlage--Puchta range | <code>COVERS, IMPLICIT CONSTANT</code> |
| small-prime full-modulus range | <code>DOES NOT COVER</code> |
| separate-L2 normalized certificate | <code>TOO COARSE</code> |
| direct weighted product | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 9. 검증 범위

<code>source/dep_r09_conductor_weighted_dual.py</code>와 tests는 squarefree sample
\(f=30\)에서 divisor Möbius inversion, conductor-level energy와 total
\(N(\varphi(f)-N)\), source exponent range, optimistic separate-L2 normalized square를
exact하게 검사한다. Actual prime sums를 계산하지 않는다.

Lean은 conductor/source theorem을 공리화하지 않고 energy partition 뒤 scalar Cauchy
certificate와 normalized barrier terminal만 검사한다.

## 10. 다음 gate

다음 최소 gate는 식 (95.22)의 joint weighted product다. 우선 source-first로

- Linnik dispersion with prime-supported first variable,
- Barban--Davenport--Halberstam with a prescribed smooth modulus and residue weights,
- large-values theorems coupling two prime character sums

을 감사한다. Drop-in이 없으면 필요한 joint norm statement를 project lemma로 고정한다.

## 11. 참고문헌

- J.-C. Schlage-Puchta, *Primes in short arithmetic progressions*,
  [arXiv:1105.1623](https://arxiv.org/abs/1105.1623).
- P. D. T. A. Elliott, *Subsequences of primes in residue classes to prime
  moduli*, Mathematika 30 (1983), 315--318.
- Y. Motohashi, *Large sieve extensions of the Brun--Titchmarsh theorem*,
  in *Number Theory, Noordwijkerhout 1983*, LNM 1068, 69--81.
