# Theory 104 — DEP-R09 actual primorial split와 original D=160 native regime

- 상태:
  <code>ACTUAL_FIXED_RAW_PRIME_SPLIT_EXACT /
  D160_NATIVE_314_LT_DF_LT_323 /
  D333_CONDITIONAL_BRANCH_EXCLUDED_FOR_BASELINE /
  BASELINE_NONVANISHING_KERNEL_LT_1_OVER_36 /
  THREE_PERCENT_BINARY_BUDGET_PARAMETERIZED_EF</code>
- 선행 정본: Theory 47·49·88--90·98·102--103, review 112
- 기계 원장:
  [native baseline v1](data/Sono_FMT_DEPR09_native_primorial_baseline_v1.json)
- 목표: 원래 outer \(D=160\), actual raw-coordinate law를 보존하고
  prescribed-\(f\) input을 실제 primorial geometry에 연결한다.
- 비목적: \(d_f\ge333\)을 실제 law에 가정하거나 이를 맞추려고 \(D\)를 바꾸거나,
  numerical \(K_{\rm EF}\)를 지정하거나, actual 실험·calculator·\(X_{\rm cert}\) range를 만드는 것.

## 1. Primary source와 actual 좌표

FMT printed p.8 (4.1)--(4.4)는 \(S\), raw \(P\), \(Q\) 모두에서 \(B_0\)를 제외한다.
Project의 raw \(P'\)는 FMT의 이 \(P\)이고, outcome-dependent good subset \(P(\mathbf A)\)가 아니다.
Printed p.9의 final extension은 \(S\cup P'\) 밖을 residue 0으로 둔다.
Bad prime/empty output도 raw inner coordinate를 목록에서 지우지 않는다.

\(X\)는 auxiliary sieve scale이다. Final theorem threshold \(X_{\rm cert}\)와 구별한다.

\[
 \mathcal A=\{p\text{ prime}:p\le X\},\quad
 \mathcal L=\{p\text{ prime}:p\le X/2\},\quad
 P'=(\mathcal A\setminus\mathcal L)\setminus\{B_0\},
 \quad S\subset\mathcal L\setminus\{B_0\}.
 \tag{104.1}
\]

마지막 \(S\)-inclusion은 아래 power-cutoff proof로 확인한다.
\(B_0=1\)이면 prime-set erasure는 아무것도 제거하지 않는다.

\[
 \mathfrak q=\prod_{p\in\mathcal A\setminus\{B_0\}}p,\quad
 Q_S=\prod_{s\in S}s,\quad Q_I=\prod_{p\in P'}p,\quad
 h=Q_SQ_I,\quad
 f=\prod_{p\in(\mathcal L\setminus\{B_0\})\setminus S}p.
 \tag{104.2}
\]

이 \(h,f\)는 random residue values 또는 good subset의 draw에 의존하지 않는다.
Potentially randomized coordinates에 실제 empty outcomes가 포함되는 것은 허용한다.
It is not a statement that every coordinate is nonempty or genuinely random.

## 2. Exact product partition과 B0의 위치

Disjoint prime-set partition으로

\[
 \boxed{\mathfrak q=hf,\qquad f=\mathfrak q/h.}
 \tag{104.3}
\]

가 된다. Mathlib finite product partition으로 전 집합의 equality를 Lean 검증했다.
Primitive factors are distinct primes in the source application, so \(h,f\) are coprime.
Actual final shift는 fixed coordinates에서 0이므로 \(m_\omega\equiv0\pmod f\)다.

\[
 \boxed{f\mid P(X/2),\qquad
       \log f\le\vartheta(X/2).}
 \tag{104.4}
\]

\(B_{\le}:=B_0\) if \(B_0\in\mathcal L\), otherwise 1이라 하면

\[
 \boxed{fQ_SB_{\le}=P(X/2),\qquad
 \log f=\vartheta(X/2)-\log Q_S-\log B_{\le}.}
 \tag{104.5}
\]

이다. Exceptional factor를 두 번 지우지 않는다.

| case | \(B_{\le}\) | native product |
|---|---:|---|
| \(B_0=1\) | 1 | \(P(X/2)/Q_S\) |
| prime \(B_0\le X/2\), including equality | \(B_0\) | \(P(X/2)/(B_0Q_S)\) |
| prime \(X/2<B_0\le X\) | 1 | \(P(X/2)/Q_S\) |

FMT p.9 literal displayed sifted set omits the exceptional-prime exclusion, while Theorem 2
and Lemma 3.1 specify it. We use that globally consistent \(p\ne B_0\), modulus \(P(X)/B_0\)
contract, not a new sieve that also removes \(B_0\).

## 3. Correct power cutoff와 physical log bounds

Actual definition은

\[
 a=\log X,\quad b=\log a,\quad
 \rho=\frac{\log b}{4b}\le\frac14,\qquad
 z=X^\rho=e^{\rho a}.
 \tag{104.6}
\]

이다. Theory 88의 linear-looking \(z=X\log b/(4b)\) 표시는 actual definition이 아니다.
과거 pinned document를 고치지 않고 여기서 power definition으로 재증명한다.

\(a\ge16\)에서 \(e^{12}>512\), \(\rho a\le a/4\), \(3a/4\ge12\)로

\[
 \boxed{z\le X/512<X/2.}
 \tag{104.7}
\]

를 얻는다. 따라서 source \(S\)는 식 (104.1)의 lower-prime set에 들어간다.
Original child \(X\ge2\exp(10^{1000})\)를 그대로 유지하며, 이 절에서는 그 훨씬 약한
consequences \(a\ge1000\), \(X/2>563\)만 사용한다. Child cutoff를 theorem threshold로 쓰지 않는다.

Exponential series의 cubic term에서

\[
 \boxed{a\ge6\quad\Longrightarrow\quad
 a^2\le a^3/6\le e^a=X,\qquad a/X\le1/a.}
 \tag{104.8}
\]

가 된다. Rosser--Schoenfeld Corollary (3.16), printed p.70, \(\vartheta(X)>X(1-1/a)\)
for \(X\ge41\)와 \(0\le\log B_0\le a\)를 사용하면

\[
 \boxed{\log\mathfrak q
 =\vartheta(X)-\log B_0
 >X(1-2/a)\ge(499/500)X.}
 \tag{104.9}
\]

Outer product는 RS Theorem 9에서 \(\log Q_S\le\vartheta(z)<(21/20)z\)다.
Theory 47의 raw dyadic prime count
\(\#P'\le X(1+3/a)/(2a)\)를 써서

\[
 \boxed{\log h\le
 \left(\frac{21}{10240}+\frac{1003}{2000}\right)X
 =\frac{128909}{256000}X<\frac{51}{100}X.}
 \tag{104.10}
\]

가 된다. This restores the support bound without treating a power cutoff as a linear equality.

RS Theorem 4 (3.14)--(3.15)와 Theorem 9 (3.32)는
\(\log P(X)<(2001/2000)X\),
\(\vartheta(X/2)>(X/2)\{1-1/[2(a-\log2)]\}\),
\(\vartheta(X/2)<(12703/25000)X\)를 준다.
\(a-\log2\ge999\), \(\log B_{\le}\le a\le X/1000\)이므로 식 (104.5)에서

\[
 \boxed{
 \frac{993}{2000}X<\log f<
 \frac{12703}{25000}X,\qquad
 \frac12-\frac1{3996}-\frac{21}{10240}-\frac1{1000}
 =\frac{127027781}{255744000}>\frac{993}{2000}.}
 \tag{104.11}
\]

Analytic theta statements are primary-source premises; they are not Lean local axioms.
Finite partition, inequality direction and coefficient transfers are separately kernel checked.

## 4. Original D=160 actual native range

Large prime endpoint \(U=\mathfrak q^{160}\)를 바꾸지 않는다.
\(\ell=\log f>0\), \(d_f=\log U/\ell=160\log\mathfrak q/\ell\)다.
식 (104.4), (104.9), (104.11)로

\[
 \boxed{
 d_f>\frac{160(499/500)}{12703/25000}
 =\frac{3992000}{12703}>314.}
 \tag{104.12}
\]

RS upper의 \(\log\mathfrak q\le\log P(X)<(2001/2000)X\)와 strong lower for \(f\)로

\[
 \boxed{
 d_f<\frac{160(2001/2000)}{993/2000}
 =\frac{106720}{331}<323<333.}
 \tag{104.13}
\]

이다. 따라서 Theory 103의 \(d_f\ge333\) one-percent regime은 이 actual baseline에
적용되지 않는다. That conditional theorem remains true, but is not the right actual input.
Outer \(D\), fixed coefficient 또는 construction law를 변경하지 않았다.

## 5. Density source prerequisites와 native real zero

Theory 103의 fixed-modulus \(L_*\)에서 four detector budgets를 각각 \(1/84\)로 둔다.
Existing explicit Mellin constant has \(\delta=1/88\), \(\zeta(1+\delta)\le89\),
\(\sqrt6<3\), \(\pi>1\), so \(K_M<10^6\).
\(e>2\), \(e<3\), \(\log2>1/2\)의 elementary bounds를 쓰면

\[
 \boxed{L_*<30000<\log f.}
 \tag{104.14}
\]

Finite-safe component audit:

| component | upper used |
|---|---:|
| \(L_B\) | \(756\sqrt{756}<21168\) |
| JL5 log argument | \(52920<2^{16}\), cutoff \(<2016\) |
| damping | \(\log84<7\), cutoff \(<5\) |
| fixed Mellin log argument | \(17640000000<2^{35}\), cutoff \(<1029\) |
| tail linear / relative | \(<4\), \(<6\) |
| \(e^8\) | \(<6561\) |
| strong absorption argument | \(2.7\cdot10^{20}<2^{70}\), cutoff \(<70\cdot183<30000\) |

The absorption audit uses \(C_{\rm pre,tight}<15000\), \(C_{\rm CL3}<200000\),
\(\underline c_g>1/50\), \(m=10^6\).
Also \(\log f>(993/2000)e^a\ge(993/2000)a^3/6>30000\) for \(a\ge1000\).
This is a conservative density-component cutoff, not a numerical \(X_{\rm cert}\) evaluation.
Cutoff component identification/real-power composition remains source-level proof, not complete Lean formalization.

Possible native real zero의 actual \(B_0\) separation은 \(1-\beta_1\ge1/[24\log P(X)]\)다.
그 term의 exponent는 native log ratios를 곱했다가 손실시키지 않고

\[
 \boxed{
 (1-\beta_1)\log U\ge
 \frac{160\log\mathfrak q}{24\log P(X)}
 >\frac{160(499/500)}{24(2001/2000)}
 =\frac{39920}{6003}>6.}
 \tag{104.15}
\]

로 처리한다. The possible real zero is retained, not asserted absent.
Nonexceptional zeros에는 Theory 103의 \(c_M=10^9/9645908801\) width를 그대로 사용한다.

## 6. Baseline nonvanishing budget

From \(d_f>314\),

\[
 \frac{129}{1250}<c_M,\qquad
 \frac{129}{1250}\left(314-\frac{23}{7}\right)>32.
 \tag{104.16}
\]

그리고 exact rational terminal은

\[
 \boxed{
 \frac{63}{2}(5\cdot10^{10})\left(\frac{10}{27}\right)^{32}
 +\frac{21}{20}\left(\frac{10}{27}\right)^6<\frac1{36}.}
 \tag{104.17}
\]

이다. \(e>27/10\), \(C_{J,\rm all}<5\cdot10^{10}\)와 식 (104.15)를 쓰면

\[
 \boxed{
 {\cal B}_{\rm nv,160}
 :=\frac{63}{2}C_{J,\rm all}e^{-c_M(d_f-23/7)}
 +\frac{21}{20}
   e^{-160\log\mathfrak q/(24\log P(X))}
 <\frac1{36}.}
 \tag{104.18}
\]

This displayed real-exponential bound, not only its rational surrogate, is Lean verified.
No \(X,f,U\) value, exponent grid or actual zero list was evaluated.

## 7. Parameterized vanishing cutoff와 total binary core

Theory 103의 actual primitive/induced zero conventions·common-height EF interface를 유지한다.

\[
 \frac{|{\cal C}_f|}{NU}\le
 {\cal B}_{\rm nv,160}
 +\underbrace{
 \frac{147}{10}\ell e^{-(d_f-7/2)\ell}
 +5062\ell^2e^{-(d_f/21-1)\ell}
 +(699716K_{\rm EF}+416)\ell^2e^{-\ell/2}}_{{\cal V}_{160}}.
 \tag{104.19}
\]

\(d_f>314\), \(\ell\ge1\)에서

\[
 \boxed{{\cal V}_{160}\le
 B(K_{\rm EF})\,\ell^2e^{-\ell/2},\qquad
 B(K):=699716K+\frac{54927}{10}.}
 \tag{104.20}
\]

이다. \(\ell\ge64\)에서 exponential series의 fifth term과 \(\ell^3\ge64^3\)는
\(\ell^2\le e^{\ell/4}\)를 주므로

\[
 \boxed{\ell^2e^{-\ell/2}\le e^{-\ell/4}.}
 \tag{104.21}
\]

This elementary absorption is now fully Lean proved before the downstream cutoff uses it.
Unknown positive \(K_{\rm EF}\)를 보존하면

\[
 \boxed{
 \ell\ge\max\{30000,\ 64,\ 4\log(450 B(K_{\rm EF}))\}
 \quad\Longrightarrow\quad {\cal V}_{160}\le\frac1{450}.}
 \tag{104.22}
\]

이므로

\[
 \boxed{
 \frac{|{\cal C}_f|}{NU}<\frac1{36}+\frac1{450}
 =\frac3{100}.}
 \tag{104.23}
\]

이다. The CF inequality is source/premise composition; the explicit scalar cutoff and last
allocation are Lean verified. Numerical \(K_{\rm EF}\) and a corresponding numerical common
starting point are still OPEN. It is not an observed prime error or a bounded \(X_{\rm cert}\) range.

## 8. 무엇이 실제로 진전했는가

- Actual law의 raw \(P'\), \(S\), \(B_0\) 위치를 source-defined product에 맞췄다.
- Original \(D=160\)을 유지한 uniform native interval \(314<d_f<323\)을 얻었다.
- Conditional d333 theorem을 실제 baseline에 대입할 수 없음을 확인했다.
- Actual full-primorial real gap을 보존해 nonvanishing budget \(<1/36\)을 증명했다.
- Correct power-cutoff geometry, polynomial absorption과 parameterized total \(3\%\) budget을 고정했다.

This is the blind native-\(f\) component only. It is not a pointwise theorem at the full
modulus \(\mathfrak q\), nor the all-character same-law moment.
Next critical work is numerical \(K_{\rm EF}\), prime-power/lower-endpoint transfer to
Theory 94's \(D_Q\), and Theory 91--93's probability/moment composition.
Nonblind correlation·DEP-R10--R12·final-variable transfer remain OPEN.

Standard prime-product partition and published theta bounds are reused. The missing scalar
bridges are proved directly using Mathlib's finite products and exponential-series lemmas.
No novel academic theorem, actual experiment or threshold calculator is claimed.

## 9. 참고문헌

- K. Ford, J. Maynard, T. Tao,
  [*Chains of large gaps between primes*](https://arxiv.org/abs/1511.04468),
  printed pp.5--6 Corollary 1/Theorem 2/Lemma 3.1, pp.8--9 (4.1)--(4.4), final extension,
  p.13 good-prime conditional law.
- J. B. Rosser, L. Schoenfeld,
  [*Approximate formulas for some functions of prime numbers*](https://doi.org/10.1215/ijm/1255631807),
  printed p.70 Theorem 4 (3.14)--(3.16), p.71 Theorem 9 (3.32).
- Theory 64·70·73·103: source numerical detector/height-weighted replay with its explicit
  conditional/partial/unformalized boundaries.
