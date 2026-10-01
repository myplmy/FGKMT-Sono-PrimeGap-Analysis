# Theory 105 — Liu--Wang first-window 독립 audit와 full-modulus hybrid

- 상태:
  <code>LW_SOURCE_SCOPE_AND_DENOMINATOR_VERIFIED /
  SAFE_LARGE_LOG_FIRST_WINDOW_COUNT_144 /
  CUMULATIVE_INTEGRAL_HYBRID_FULL_MODULUS /
  D160_NONVANISHING_ZERO_KERNEL_LT_3_PER_THOUSAND</code>
- 선행 정본: Theory 70·73·98·103--104, review 113
- 원장: [LW first-window v1](data/Sono_FMT_DEPR09_LW_first_window_v1.json)
- 목표: published fixed-modulus first-window source를 실제 large-log 영역에서
  independently conservative하게 검증하고 full \(\mathfrak q\) zero contribution에 연결한다.
- 비목적: printed 182/364 또는 EF multiplier 1.3804를 전사하거나, actual zeros를 계산하거나,
  numerical EF·PAP·\(X_{\rm cert}\)를 닫는 것.

## 1. Source의 개별 적용조건

Liu--Wang, Acta Arithmetica 102.3 (2002), printed pp.272--279를 native text와
rendered originals로 대조했다. Official PDF SHA는
50c6b5d628a07cfb216078571a846ef658aa7db29515d21bb8dbb4f20dc5055d다.
Published correction은 표적 검색에서 식별하지 못했으나 absence를 전 문헌 주장으로 쓰지 않는다.

Source Section 3에는

\[
 q\le x_{\rm src},\qquad x_{\rm src}\ge1,\qquad y\ge0,\qquad
 z\ge\max\{x_{\rm src}y,10^{11}\}.
 \tag{105.1}
\]

가 있다. Our actual application uses \(y=t\ge1\), \(x_{\rm src}=q\),
\(z=qt\). In particular \(z\ge q\). Source의 \(y=0,z<x_{\rm src}\)까지 확장하지 않는다:
the proof's local log comparison requires the max-one height to be controlled.

Count는 primitive-only 평균이 아니라 모든 characters modulo \(q\)에 대한

\[
 N(\alpha,q,t)=\sum_{\chi\bmod q}
 \#\{\rho:L(\rho,\chi)=0,\ \alpha\le\Re\rho<1,\ |\Im\rho|\le t\}.
 \tag{105.2}
\]

Multiplicity와 closed height boundary를 보존한다.
Imprimitive characters' nontrivial zeros coincide with their unique primitive inducing character.
Euler-factor zeros on \(\Re s=0\)는 이 very-near-one count에 없다.

Printed p.278의 \(4\cdot91=364\)와 p.279 Table 5의 182가 다르다.
Neither was adopted. We use source equation (3.22) and independently prove its safe terminal.

## 2. Equation (3.22)의 safe large-log envelope

고정 source parameters를

\[
 a_0=\frac{17}{50},\qquad\lambda_0=\frac9{20},\qquad
 L=\log z\ge30000,\qquad
 \kappa=\frac{5-\sqrt5}{10}
 \tag{105.3}
\]

로 둔다. \(a_0\in(0,0.4]\), \(\lambda_0\in[0.262132,0.48]\)다.
\(a_0\)는 sieve \(\log X\)와 다른 source free parameter다.

\[
 \boxed{0\le\kappa\le\frac{277}{1000}.}
 \tag{105.4}
\]

이 rational enclosure는 actual \(\sqrt5\)에서 Lean으로 증명했으며 decimal approximation을 premise로 넣지 않았다.

\[
 A=\frac{50}{17}-\frac{8973}{10000L},\quad
 B=\kappa+\frac{7647}{10000L},\quad
 C=\frac{100}{79}-\kappa-\frac{755}{10000L}.
 \tag{105.5}
\]

For the entire \(L\ge30000\) domain,

\[
 \boxed{0\le A\le3,\qquad0\le B\le\frac{139}{500},\qquad
 C\ge\frac{247}{250}.}
 \tag{105.6}
\]

Hence both source conditions (3.18), including \(C\ge0\), hold:

\[
 \boxed{
 C^2-AB\ge
 \left(\frac{247}{250}\right)^2-3\frac{139}{500}
 =\frac{2221}{15625}>\frac18,\qquad
 A^2-AB\le9.}
 \tag{105.7}
\]

Source (3.22) and the floor inequality then give

\[
 N(\alpha,q,t)\le2\left\lfloor
 \frac{A^2-AB}{C^2-AB}\right\rfloor
 \le2\cdot72=144.
 \tag{105.8}
\]

따라서

\[
 \boxed{
 N\left(1-\frac{9}{20\log(qt)},q,t\right)\le144
 \qquad(\log(qt)\ge30000,\ t\ge1).}
 \tag{105.9}
\]

이다. The analytic equation is a source premise; the complete rational/irrational
enclosure, denominator, quotient and floor terminal are kernel checked.

### 2.1 alternating selection의 local-spacing 의무

Source Lemma 3.1의 \(n\le2\) branch를 Table 2 숫자만으로 채택하지 않았다.
Eq.(3.6)에서 local \(a_{\rm loc}=78/25\), \(b_{\rm loc}=19039/10000\),
\(\lambda=\lambda_0\)를 쓰면 numerator is \(<3/5\).
The subtracted correction is nonnegative because
\(0.8973-0.3918-0.0775\kappa+\kappa\log\pi>0\).
\(\sqrt5\le9/4\)와 \(L\ge30000\)에서 denominator is \(>1/5\), so

\[
 \boxed{
 \left\lfloor\frac{\text{local numerator}}{\text{local denominator}}\right\rfloor<3,
 \quad n\le2,\quad
 \gamma_{j+2}-\gamma_j>2b_{\rm loc}/L,\quad
 N_1=\sum_\chi\left\lceil N_\chi/2\right\rceil\ge N/2.}
 \tag{105.10}
\]

Closed spacing windows and multiplicities are included.
The numerical local floor terminal is Lean proved; source log-derivative identity
and whole sequence selection are not independently formalized.
Eq.(3.22)'s primitive pair principal condition is equality of inducing characters.
Their conductor products divide fixed \(q\), not a generic modulus-square envelope.

## 3. Full modulus·original D=160 and a moving integral split

Now set \(q=\mathfrak q=P(X)/B_0\), \(U=q^{160}\),
\(\ell=\log q\), \(T=q^{3/2}\), \(u=160\ell\), \(\omega=1/21\), \(k=23/7\).
This does not change the original sieve/HG law or outer exponent.
Original child and Theory 104 give \(\ell>30000\).

For each fixed \(t\in[1,T]\),

\[
 L(t)=\ell+\log t,\quad
 \delta_0(t)=\frac{c_M}{L(t)},\quad
 \delta_s(t)=\frac{\lambda_0}{L(t)},\quad
 0<\delta_0(t)<\delta_s(t)<\omega,\quad
 c_M=\frac{10^9}{9645908801}.
 \tag{105.11}
\]

Only the possible one real exceptional zero is removed from the nonexceptional count.
This is a positive subset of source count, so both its bounds remain upper bounds.
The target family in \(\mathcal A,\mathcal S\) below is **nonprincipal characters only**,
with zeros counted as pairs \((\chi,\rho)\) and with multiplicity.
Write \(N(\delta,t)\) for this family's count with \(1-\beta\le\delta\).
LW's all-character count bounds this subset; Theory 103's Jutila tail is a
nonprincipal bound. Principal zeta zeros and the main term remain a separate channel.

\[
 \mathcal A(t)=
 \sum_{\substack{\rho\ {\rm nonexceptional}\\1-\beta\le\omega\\|\gamma|\le t}}
 U^{\beta-1}
 =e^{-u\omega}N(\omega,t)+
 u\int_{\delta_0(t)}^\omega e^{-u\delta}N(\delta,t)\,d\delta.
 \tag{105.12}
\]

Split this integral at \(\delta_s(t)\), not the zeros into fixed classes that secretly
depend on later \(t\). For \(\delta\le\delta_s(t)\), monotonicity and (105.9) give

\[
 u\int_{\delta_0(t)}^{\delta_s(t)}e^{-u\delta}N(\delta,t)\,d\delta
 \le144\{e^{-u\delta_0(t)}-e^{-u\delta_s(t)}\}
 \le144e^{-u\delta_0(t)}.
 \tag{105.13}
\]

In the tail, use Theory 103's fixed-modulus density:

\[
 N(\delta,t)\le
 2C_{J,\rm all}e^{kL(t)\delta}(5+2\delta L(t)),
 \qquad C_{J,\rm all}=\frac{19720624464771552}{425315}.
 \tag{105.14}
\]

With \(v=u-kL(t)>0\), exact integration including the upper endpoint gives the tail upper
\(2C_{J,\rm all}(u/v)(5+2\lambda_0+2L/v)e^{-v\delta_s}\).
The upper-endpoint coefficient is nonpositive.
Since \(u/v\le5/3\), \(L/v\le1/5\),

\[
 \boxed{
 2(u/v)(5+2\lambda_0+2L/v)\le24,\qquad
 \mathcal A(t)\le144e^{-c_M160\ell/L(t)}
 +24C_{J,\rm all}e^{-\lambda_0\{160\ell/L(t)-k\}}.}
 \tag{105.15}
\]

No scalar coefficient was borrowed from the smaller \(c_M\) tail allocation without rechecking it.
The \(144\) term belongs to the count-integral piece, not a global unweighted sum over all heights.

## 4. Height-weighted contribution

Finite height layer cake preserves the low-height packet:

\[
 \mathcal S=
 \sum_{\substack{\rho\ {\rm nonexceptional}\\1-\beta\le\omega\\|\gamma|\le T}}
 \frac{U^{\beta-1}}{\max(1,|\gamma|)}
 =\frac{\mathcal A(T)}T+\int_1^T\frac{\mathcal A(t)}{t^2}\,dt.
 \tag{105.16}
\]

Let \(w=\log t\). For \(c=c_M\) or \(\lambda_0\),
\(160c\le\ell/5\). Theory 103's exact field identity gives

\[
 w+c\frac{160}{1+w/\ell}-c160
 =w\left(1-\frac{160c}{\ell+w}\right)\ge\frac45w.
 \tag{105.17}
\]

Thus each weighted integral costs at most \(5/4\), and each terminal costs at most
\(e^{-6\ell/5}\le1/4\). The whole height allocation is \(3/2\).
On the near band, \(1/|\rho|\le(21/20)/\max(1,|\gamma|)\), so

\[
 \boxed{
 \mathcal S\le216e^{-160c_M}
 +36C_{J,\rm all}e^{-\lambda_0(160-k)},\qquad
 \mathcal E_{\rm near,np}\le
 \frac{1134}{5}e^{-160c_M}
 +\frac{189}{5}C_{J,\rm all}e^{-\lambda_0(160-k)}.}
 \tag{105.18}
\]

The count-integral and height-integral identification remains analytic/source-level proof.
The final scalar coefficients and the displayed numerical exponential kernel are Lean verified.

Possible real zero uses the actual full-P gap:
\(\mathcal E_{\beta_1}\le(21/20)e^{-160\log q/[24\log P(X)]}\).
Theory 104 gives its decay \(>39920/6003>6\). Since
\(160c_M>16\), \(\lambda_0(160-k)>70\) and \(e>27/10\),

\[
 \boxed{
 \frac{1134}{5}e^{-160c_M}
 +\frac{189}{5}C_{J,\rm all}e^{-\lambda_0(160-k)}
 +\frac{21}{20}e^{-160\log q/[24\log P(X)]}
 <\frac3{1000}.}
 \tag{105.19}
\]

This is a numerical nonvanishing **nonprincipal near-zero** kernel at the full modulus,
not a measured error or a bound for the principal channel.
Far zeros, endpoint/prime-power corrections and uniform numerical EF are separate.
Neither principal/main-term transfer nor pointwise full-modulus PNT is marked closed here.

## 5. 채택한 내용과 남은 입력

- The source analytic (3.6), (3.22) and their conditions are adopted within the verified
  \(q\le x_{\rm src},t\ge1,\log z\ge30000,\lambda=9/20\) contract.
- Source numerical tables 182/364 are not adopted.
- A conservative 144 terminal is independently proved over the complete large-log domain.
- Source first-window and Jutila tail are combined inside the same cumulative-count integral.
- Original full modulus and D=160 are restored; no construction/law change is needed for this zero bound.
- LW Theorem 8 remains a non-drop-in at its printed polylog-modulus/height range.
- Numerical EF·pointwise PAP·global same-law root·R10--R12·\(X_{\rm cert}\) remain OPEN.

The result changes the source-route feasibility. It is not a claim of academic novelty:
the key very-near-one theorem was already published in 2002.
Actual prime/zero/dataset computation, calculator and long computation are NOT RUN.

## 6. 다음 최소 gate

Audit the numerical truncated EF at actual \(q,T=q^{3/2},U=q^{160}\), including primitive
and imprimitive characters, principal case, closed endpoints and both positive/negative
good heights. The printed \(1.3804\) cannot be transferred without replaying those assumptions.
If a conservative uniform EF is supplied, use the full-modulus pointwise route first
before investing further in a nonblind-law covariance theorem.

## 7. 참고문헌

- M.-C. Liu, T. Wang,
  [*Distribution of zeros of Dirichlet L-functions and an explicit formula for ψ(t,χ)*](https://doi.org/10.4064/aa102-3-5),
  pp.272--279 (3.1)--(3.22), Table 2/5; pp.288--292 Theorem 8.
- J. Thorner, A. Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878),
  fixed-modulus/height-weighted explicit-formula context only.
- Theories 70·73·103--104: numerical density tail, exact height-cost and actual full-P gap,
  with their source/partial/conditional proof boundaries retained.
