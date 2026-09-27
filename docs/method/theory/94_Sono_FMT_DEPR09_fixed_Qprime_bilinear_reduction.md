# Theory 94 — DEP-R09 fixed-\(Q'\) pre-absolute-value bilinear 환원

- 상태:
  <code>CENTERED_KERNEL_EXACT /
  PRIME_POWER_B0_CORRECTIONS_PARAMETERIZED_EXPLICIT /
  CENTERED_BINARY_PRIME_FORM_OPEN /
  R10_ONE_SIDED_NOT_DROP_IN</code>
- 선행 정본: Theory 77, 90, 92--93, review 102
- 기계 원장:
  [fixed-Q-prime bilinear v1](data/Sono_FMT_DEPR09_fixed_qprime_bilinear_v1.json)
- 목표: Theory 93의 fixed mean \(D_Q\)를 mean-zero residue kernel,
  prime-prime form과 B0·higher-prime-power correction으로 exact하게 분해하고,
  existing R10/Selberg upper가 centered gate에 주는 정확한 범위를 판정한다.
- 비목적: one-sided upper를 양측 centered asymptotic으로 승격하거나, actual prime
  계산, threshold calculator, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

> **2026-09-27 successor:** [Theory 95](95_Sono_FMT_DEPR09_conductor_weighted_character_dual.md)는
> centered binary-prime form을 primitive conductor별 weighted character product로
> exact dualize했다. Separate prime-supported L2는 quantitatively too coarse이며 최신
> gate는 식 (95.22)의 direct signed product다.

## 1. 결론

Theory 93처럼 \(Q'\)는 \((X,Y]\)의 \(N\)개 prime vertices이고
\(Q'<f\)다. Reduced \(n,q\)에 대해 centered residue kernel을

\[
 K_f(n,q):=\varphi(f)1_{\{n\equiv q\pmod f\}}-1
 \tag{94.1}
\]

로 두고

\[
 H_Q(n):=\sum_{q\in Q'}K_f(n,q)
 =\varphi(f)1_{\{[n]_f\in Q'\}}-N
 \tag{94.2}
\]

라 하자. Theory 92의 inverse transform을 합의 순서만 바꾸면

\[
 \boxed{
 D_Q=\sum_{\substack{n\le U\\(n,fh)=1}}\Lambda(n)H_Q(n).}
 \tag{94.3}
\]

이것이 필요한 pre-absolute-value form이다. Full reduced residue system에서는

\[
 \sum_{\substack{q\bmod f\\(q,f)=1}}K_f(n,q)=0,
 \tag{94.4}
\]

이므로 \(D_Q\)는 prime-selected residue mask와 centered von Mangoldt mass의
signed covariance다.

\(\Lambda_{\mathbb P}(n)=\log n\) for prime \(n\), 0 otherwise, 그리고
\(\Lambda_{\ge2}:=\Lambda-\Lambda_{\mathbb P}\)로 두면 exact하게

\[
 \boxed{D_Q=\mathcal B_Q+E_{\rm pp}.}
 \tag{94.5}
\]

여기서 prime part와 higher-prime-power part는

\[
 \mathcal B_Q:=
 \sum_{q\in Q'}
 \sum_{\substack{p\le U\\p\nmid fh\\p\ {\rm prime}}}
 (\log p)K_f(p,q),
 \tag{94.6}
\]

\[
 E_{\rm pp}:=
 \sum_{\substack{r^j\le U\\j\ge2\\r\nmid fh}}
 (\log r)H_Q(r^j)
 \tag{94.7}
\]

이다.

\(\mathfrak q=fh=P(X)/B_0\)이고 \(\iota_B=1\) if \(B_0\)가 prime,
아니면 0이라 하자. Prime divisors not in \(fh\)는 \(p>X\) 또는 active
\(B_0\)뿐이다. \(B_0\le X<q<f\)이므로 \(K_f(B_0,q)=-1\)이고

\[
 \boxed{
 \mathcal B_Q=\mathcal C_f-\iota_BN\log B_0,}
 \tag{94.8}
\]

\[
 \mathcal C_f:=
 \sum_{q\in Q'}
 \sum_{\substack{X<p\le U\\p\ {\rm prime}}}
 (\log p)K_f(p,q).
 \tag{94.9}
\]

Positive congruent pair mass를

\[
 \mathcal P_f:=
 \sum_{q\in Q'}
 \sum_{\substack{\ell\ge0\\q+\ell f\le U\\
                    q+\ell f\ {\rm prime}}}
 \log(q+\ell f)
 \tag{94.10}
\]

로 두면 \(Q'<f\)의 unique representative 때문에

\[
 \boxed{
 \mathcal C_f
 =\varphi(f)\mathcal P_f
 -N\{\vartheta(U)-\vartheta(X)\}.}
 \tag{94.11}
\]

식 (94.5), (94.8), (94.11)은 fixed mean을 하나의 **centered binary-prime form**과
두 elementary corrections로 exact하게 환원한다.

Corrections는

\[
 \boxed{
 \frac{|E_{\rm pp}|}{NU}
 \le
 \left(\frac{\varphi(f)}N+1\right)
 \frac{\log U}{\sqrt U}
 \le
 (U^{1/21}+1)\frac{\log U}{\sqrt U},}
 \tag{94.12}
\]

\[
 \boxed{
 \frac{\iota_BN\log B_0}{NU}
 \le\frac{\log X}{U}.}
 \tag{94.13}
\]

로 parameterized explicit이다. 따라서 새 core gate는

\[
 \boxed{
 \delta_{\rm bin}:=
 \frac{|\varphi(f)\mathcal P_f
 -N\{\vartheta(U)-\vartheta(X)\}|}{NU}.}
 \tag{94.14}
\]

Existing R10/Selberg source는 \(\mathcal P_f\)의 one-sided upper만 겨냥하므로
식 (94.14)의 cancellation을 인증하지 못한다.

## 2. centered kernel identity

Theory 92 식 (92.4)는 reduced \(q\)에

\[
 B_h(q)=
 \varphi(f)
 \sum_{\substack{n\le U\\n\equiv q\pmod f\\(n,h)=1}}
 \Lambda(n)
 -\sum_{\substack{n\le U\\(n,fh)=1}}\Lambda(n).
 \tag{94.15}
\]

\((q,f)=1\)이므로 첫 합의 \(n\)은 자동으로 \((n,f)=1\)이다. \(q\)를
\(Q'\)에서 합하고 finite sums를 교환하면 각 \(n\)의 coefficient가 정확히
\(H_Q(n)\)이므로 식 (94.3)이 나온다.

식 (94.4)는 fixed reduced \(n\)에 congruent한 reduced \(q\)가 정확히 하나이고,
나머지 \(\varphi(f)-1\)개 kernel이 \(-1\)인 데서 따른다. 이 cancellation을
absolute value 전에 보존하는 것이 핵심이다.

## 3. prime·prime-power exact split

\(\Lambda(n)\)의 support는 prime powers다. Exponent 1과 \(j\ge2\)를 분리하면
식 (94.5)--(94.7)이 즉시 나온다. Prime \(p\)에 \(p\nmid fh\)를 요구하면

- \(p>X\), 또는
- \(B_0\)가 prime이고 \(p=B_0\)

뿐이다. Active \(B_0\)는 \(P(X)\)의 factor라 \(B_0\le X\)이고 \(Q'\)에서
제외된다. \(B_0,q<f\)인 distinct representatives이므로 congruence가 없고 식
(94.8)이 exact하다.

\(p>X\)에서 \(p\equiv q\pmod f\) iff
\(p=q+\ell f\) for a unique integer \(\ell\ge0\). Negative kernel \(-1\)을
\(q\)마다 합하면 \(-N\{\vartheta(U)-\vartheta(X)\}\)이므로 식 (94.11)이
나온다. \(\ell=0\) diagonal을 빠뜨리지 않는다.

## 4. higher-prime-power correction

각 reduced prime power \(r^j\)에

\[
 |H_Q(r^j)|
 \le\max\{N,|\varphi(f)-N|\}
 \le\varphi(f)+N.
 \tag{94.16}
\]

또 exponent \(j\ge2\)인 모든 prime-power von Mangoldt mass를 residue 조건 없이
넓히면 Theory 92와 같이

\[
 \sum_{\substack{r^j\le U\\j\ge2}}\log r
 \le\sqrt U\log U.
 \tag{94.17}
\]

식 (94.16)--(94.17)이 식 (94.12)의 첫 부등식을 준다. \(N\ge1\),
\(\varphi(f)\le f\le U^{1/21}\)로 둘째 부등식이 나온다.

\(L=\log U\)라 하면 마지막 upper는

\[
 L\e^{-19L/42}+L\e^{-L/2},
 \tag{94.18}
\]

이고 \(L>42/19\) 이후 감소한다. 따라서 원하는 fixed positive correction budget에
대한 finite log-cutoff를 계산할 수 있다. 다만 final coefficient allocation 전이므로
이번 단계에서 이를 numerical \(X_{\rm cert}\)로 선언하거나 calculator를 만들지 않는다.

식 (94.8)의 B0 correction은 \(B_0\le X\)로 식 (94.13)이다. 따라서

\[
 \boxed{
 \delta_Q
 \le\delta_{\rm bin}
 +\frac{\log X}{U}
 +(U^{1/21}+1)\frac{\log U}{\sqrt U}.}
 \tag{94.19}
\]

Corrections는 analytic core가 아니다.

## 5. R10/Selberg upper source의 정확한 경계

Sono Assumption 3.4는 fixed offsets \(a\ne b\)에

\[
 \#\{z\le Z:Pz+a, Pz+b\ {\rm prime}\}
 \le C_{\rm UB}(1+o(1))
 \left(\frac{\log X}{\log Z}\right)^2Z
 \tag{94.20}
\]

를 요구한다. Section 4는 Halberstam--Richert Theorem 5.7을 사용해
\(C_{\rm UB}=8e^{2\gamma}\), arbitrary \(D_{\rm UB}>0\)를 얻는다.
이는 Sono의 original pair-collision 목적에 유효한 **one-sided upper**다.

Current \(\mathcal P_f\)에서 fixed \(\ell\ge1\)마다 두 forms는
\(z\)와 \(z+\ell f\)이고 determinant parameter는 \(E=\ell f\)다. Generic
Theorem 4.1을 각 shift에 적용하려면 다음 비용을 새로 처리해야 한다.

1. \(\ell\) 전체 합의 singular factor average.
2. \(\ell f\)의 prime divisors와 active B0의 균일성.
3. Weight \(\log(q+\ell f)\).
4. Source error
   \((\log Y)^{-1}\{\log_2(3Y)+\log_2(3\ell f)\}\)의 multiplier.

Current maximum \(\ell f\le U\)에서는
\(\log_2 U\asymp\log X\asymp\log Y\)이므로 fourth ratio를 \(o(1)\)로
보내는 source argument가 없다. Sono의 own specialization은 offsets
\(|a-b|\le y=o(X\log X)\)와 훨씬 긴 \(Z\)를 사용하므로 이 mismatch가 없다.

더 근본적으로, 이 네 비용을 모두 닫아 어떤 \(C\ge0\)에

\[
 0\le\mathcal P_f
 \le C\frac{N\{\vartheta(U)-\vartheta(X)\}}{\varphi(f)}
 \tag{94.21}
\]

를 얻어도 식 (94.14)은 닫히지 않는다. \(\mathcal P_f=0\)은 모든 nonnegative
upper를 만족하지만

\[
 \frac{|\varphi(f)\mathcal P_f-N\{\vartheta(U)-\vartheta(X)\}|}
 {N\{\vartheta(U)-\vartheta(X)\}}=1.
 \tag{94.22}
\]

따라서 필요한 것은 pair upper가 아니라 main term 주위의 **two-sided signed
pre-absolute-value estimate**다. 이는 parity-sensitive lower bound를 Selberg upper
sieve에서 얻으라는 요구가 아니다. Dispersion/character cancellation으로 centered form
자체를 상계해야 한다.

## 6. 상태표

| 항목 | 판정 |
|---|---|
| centered kernel identity | <code>EXACT FINITE</code> |
| prime/prime-power split | <code>EXACT</code> |
| positive pair reindexing | <code>EXACT</code> |
| B0 correction | <code>PARAMETERIZED EXPLICIT</code> |
| higher-prime-power correction | <code>PARAMETERIZED EXPLICIT</code> |
| centered binary-prime form | <code>OPEN</code> |
| Sono/R10 original upper | <code>VALID IN ORIGINAL SCOPE</code> |
| R10 direct drop-in for centered gate | <code>NO</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 7. 검증 범위

<code>source/dep_r09_fixed_qprime_bilinear.py</code>와 단위시험은 finite residue table에서
kernel/original mean, prime/prime-power split, unique \((q,\ell)\) reindexing,
correction envelope와 upper-only countermodel을 exact <code>Fraction</code>으로 검사한다.
실제 prime·large \(U\)·threshold는 계산하지 않는다.

Lean은 source theorems를 공리화하지 않고 kernel bookkeeping, correction transfer,
upper-only logical countermodel과 strict downstream transfer의 scalar terminal만 검사한다.

## 8. 다음 gate

다음 최소 gate는 식 (94.14)의 two-sided pre-absolute-value estimate다. 권장 순서는

1. \(\mathcal C_f\)를 character/dispersion bilinear form으로 dualize하고,
2. principal diagonal과 nonprincipal off-diagonal을 absolute value 전에 분리하며,
3. fixed smooth primorial에 맞는 explicit dispersion/asymptotic-sieve source를 찾고,
4. 없으면 필요한 new lemma의 정확한 norm·multiplier·cutoff statement를 고정하는 것

이다. R10 numerical UB 자체는 original proof-DAG에서 계속 OPEN이며, 이번 판정으로
폐기되지 않는다.

## 9. 참고문헌

- K. Sono, *An explicit lower bound for large gaps between some consecutive
  primes*, Section 4, Theorem 4.1 and formulas (4.1)--(4.7).
- H. Halberstam and H. E. Richert, *Sieve Methods*, London Mathematical
  Society Monographs 4, Academic Press, 1974, Theorem 5.7.
