# Theory 93 — DEP-R09 outer-law sparse centered-mean 환원

- 상태:
  <code>OUTER_WEIGHTED_MOMENT_EXACT /
  ADAPTIVE_DELETION_PARAMETERIZED_EXPLICIT /
  FIXED_QPRIME_MEAN_OPEN</code>
- 선행 정본: Theory 49--53, 81, 91--92, review 101
- 기계 원장:
  [outer-law sparse mean v1](data/Sono_FMT_DEPR09_outer_law_sparse_mean_v1.json)
- 목표: Theory 92 식 (92.25)의 outcome-dependent selected mean을 actual outer residue
  law에서 deterministic fixed-\(Q'\) mean과 explicit fluctuation·deletion 비용으로
  환원하고, 남는 analytic source gate를 고정한다.
- 비목적: modulus-average theorem을 prescribed primorial theorem으로 승격하거나,
  absolute log-saving을 relative progression error로 바꾸거나, actual prime 계산,
  threshold calculator, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

## 1. 결론

고정 prime vertex set을

\[
 Q'=\{q_1,\ldots,q_N\},\qquad N:=|Q'|>0
 \tag{93.1}
\]

라 하고, Theory 49 outer residue vector \(\mathbf A\)에 대한 survival indicator를

\[
 I_q(\mathbf A):=1_{\{q\in\mathscr S(\mathbf A)\}}
 \tag{93.2}
\]

로 둔다. Theory 49는 exact하게

\[
 \Pr(I_q=1)=\sigma,qquad
 \left|\Pr(I_q=I_r=1)-\sigma^2\right|
 \le\epsilon\sigma^2,quad
 \epsilon:=2a^{-17}quad(q\ne r)
 \tag{93.3}
\]

를 준다.

Theory 92의 deterministic real weight를 \(B_q:=B_h(q)\)라 하고

\[
 D_Q:=\sum_{q\in Q'}B_q,qquad
 W(\mathbf A):=\sum_{q\in Q'}B_qI_q(\mathbf A)
 \tag{93.4}
\]

로 두면

\[
 \boxed{\mathbb EW=\sigma D_Q.}
 \tag{93.5}
\]

따라서 outer randomization은 fixed mean을 없애지 않는다. 다만 weighted fluctuation은
exact one/two-point law로

\[
 \boxed{
 \operatorname{Var}W
 \le
 \sigma(1-\sigma)\sum_qB_q^2
 +\epsilon\sigma^2
 \left\{\left(\sum_q|B_q|\right)^2-\sum_qB_q^2\right\}.}
 \tag{93.6}
\]

Theory 92의 \(|B_q|<LU\), \(L:=11/5\)를 넣으면

\[
 \boxed{
 \frac{\operatorname{Var}W}{(\sigma NU)^2}
 \le L^2\left{
 \frac{1-\sigma}{\sigma N}
 +\epsilon\frac{N-1}{N}\right\}.}
 \tag{93.7}
\]

Theory 53의 preparation event에서
\(V_0=Q'\cap\mathscr S(\mathbf A)\),
\(V=V_0\setminus E(\mathbf A)\)이고

\[
 \bigl||V_0|-\sigma N\bigr|\le\eta\sigma N,qquad
 \eta:=b^{-3},qquad
 |E|\le r_E|V_0|,quad r_E:=\frac{8000}{b^2}.
 \tag{93.8}
\]

고정 mean ratio를

\[
 \delta_Q:=\frac{|D_Q|}{NU}
 \tag{93.9}
\]

라 하자. 임의의 \(t>0\)에 대해 weighted fluctuation-good event와 식 (93.8)이
동시에 성립하면

\[
 \boxed{
 \frac{|\sum_{q\in V}B_q|}{|V|U}
 \le
 \Delta_{\rm out}(t):=
 \frac{\delta_Q+t+Lr_E(1+\eta)}
 {(1-r_E)(1-\eta)}.}
 \tag{93.10}
\]

outer fluctuation과 adaptive deletion은 모두 parameterized explicit하고 \(X\to\infty\)에서
사라진다. 새 analytic core는 deterministic

\[
 \boxed{
 D_Q
 =\varphi(f)\sum_{q\in Q'}A_h(q;U)-NS_h(U).}
 \tag{93.11}
\]

현재 확인한 unconditional source는 이 fixed primorial·growing prime-residue family에
fully numerical relative bound를 주지 않는다. 따라서 blind same-law moment와
\(X_{\rm cert}\)는 계속 OPEN이다.

## 2. weights가 outer draw 전에 고정되는가

randomized modulus \(h\)는 randomized **prime coordinates의 집합**으로 정해지는
deterministic product다. residue values \(A_s\)의 실제 draw에는 의존하지 않는다.
따라서

\[
 B_h(q)=\varphi(f)A_h(q;U)-S_h(U)
 \tag{93.12}
\]

는 \(\mathbf A\)를 고르기 전에 고정된 real weight다. Theory 49의 one/two-point
probability에 deterministic coefficients를 곱해 합하는 것이 허용된다.

반면 \(V_0\), degree/cap exceptional set \(E(\mathbf A)\), 최종 \(V\)는 outer draw에
의존한다. 이를 사전 고정 subset으로 바꾸지 않고 §5에서 worst-case deletion으로 처리한다.

또 \(q\in Q'\subset(X,Y]\)이고 \(f\)의 prime factors는 \(X\) 이하이므로
\((q,f)=1\)이다. Theory 92 inverse transform의 reduced-residue 조건도 유지된다.

## 3. weighted expectation·variance

식 (93.3)의 single probability로 유한합을 교환하면

\[
 \mathbb EW
 =\sum_qB_q\mathbb EI_q
 =\sigma\sum_qB_q,
 \tag{93.13}
\]

즉 식 (93.5)다. centered square를 전개하면 exact하게

\[
 \begin{aligned}
 \operatorname{Var}W
 ={}&\sigma(1-\sigma)\sum_qB_q^2\\
 &+\sum_{q\ne r}
 \{\Pr(I_q=I_r=1)-\sigma^2\}B_qB_r.
 \end{aligned}
 \tag{93.14}
\]

ordered off-diagonal에 triangle inequality와 식 (93.3)을 적용하면

\[
 \left|\sum_{q\ne r}
 \{\Pr(I_q=I_r=1)-\sigma^2\}B_qB_r\right|
 \le
 \epsilon\sigma^2
 \left\{\left(\sum_q|B_q|\right)^2-\sum_qB_q^2\right\}.
 \tag{93.15}
\]

식 (93.14)--(93.15)가 (93.6)을 준다. weight 부호를 버리는 것은 covariance error
항뿐이고, mean \(D_Q\)의 cancellation은 그대로 보존한다.

\(|B_q|\le LU\)에서

\[
 \sum_qB_q^2\le L^2NU^2,qquad
 \left(\sum_q|B_q|\right)^2-\sum_qB_q^2
 \le L^2N(N-1)U^2.
 \tag{93.16}
\]

이를 식 (93.6)에 넣고 \((\sigma NU)^2\)로 나누면 식 (93.7)이다.

## 4. weighted fluctuation failure mass

임의의 fixed \(t>0\)에 Chebyshev를 적용하면

\[
 \boxed{
 F_{\rm wt}(t):=
 \Pr\{|W-\sigma D_Q|>t\sigma NU\}
 \le
 \min\left(1,
 \frac{L^2}{t^2}
 \left\{\frac{1-\sigma}{\sigma N}
 +\epsilon\frac{N-1}{N}\right\}\right).}
 \tag{93.17}
\]

Theory 51의 fixed whole-interval deterministic inputs은

\[
 \sigma N
 \ge
 80c\frac{Xb}{a}
 (1-b^{-10})\left(1-\frac1{200b^2}\right)
 >79c\frac{Xb}{a}.
 \tag{93.18}
\]

여기서는 \(Q'=Q'\cap(0,Y]\), 즉 사전 고정 interval 하나를 사용했다. 따라서

\[
 \boxed{
 F_{\rm wt}(t)
 <\min\left(1,
 \frac{121}{25t^2}
 \left\{\frac{a}{79cXb}+2a^{-17}\right\}\right).}
 \tag{93.19}
\]

fixed \(t>0\)에서 이는 existing child scale에 매우 작지만, 이번 단계에서는
\(t\)를 final \(2\times10^{-17}\) budget에 수치 배정하거나 cutoff를 계산하지 않는다.

## 5. adaptive exceptional deletion

Theory 51 whole-interval count-good event은

\[
 \bigl||V_0|-\sigma N\bigr|\le\eta\sigma N,qquad
 \Pr(\text{count fail})\le\frac{3b^6}{a^{17}}.
 \tag{93.20}
\]

Theory 53 preparation event에서는 \(|E|/|V_0|\le r_E=8000/b^2<1\)이다.
따라서

\[
 |V|=|V_0|-|E|
 \ge(1-r_E)(1-\eta)\sigma N.
 \tag{93.21}
\]

삭제 집합은 \(B_q\)의 부호·크기와 상관될 수 있으므로 평균독립성을 가정하지 않는다.
결정론적 triangle inequality만으로

\[
 \begin{aligned}
 \left|\sum_{q\in V}B_q\right|
 &\le |W|+\sum_{q\in E}|B_q|\\
 &\le\sigma NU(\delta_Q+t)+LU|E|\\
 &\le\sigma NU\{\delta_Q+t+Lr_E(1+\eta)\}.
 \end{aligned}
 \tag{93.22}
\]

식 (93.21)로 나누면 (93.10)이다. 이는 adaptive deletion이 가장 큰 같은-sign
weights를 골라 지우는 worst case까지 포함한다.

preparation failure를

\[
 F_{\rm prep}:=
 \min\left(1,
 \frac{4800c}{b^5}+\frac{800c}{b^{10}}
 +\frac{112kb^4}{a^{11}}\right)
 \tag{93.23}
\]

라 하면 outer selected-mean event의 mass는 적어도

\[
 \boxed{
 p_{\rm out}(t)
 \ge
 \max\left(0,
 1-F_{\rm prep}-\frac{3b^6}{a^{17}}-F_{\rm wt}(t)
 \right).}
 \tag{93.24}
\]

독립성은 쓰지 않았다. \(p_{\rm out}(t)>0\)이고 Theory 92 inner gate를
\(\delta=\Delta_{\rm out}(t)\)로 모든 이 outer fiber에서 uniform하게 만족하면,
outer outcome 하나와 그 conditional inner outcome을 순서대로 선택할 수 있다.

## 6. 무엇이 제거됐고 무엇이 남았는가

식 (93.10)은 construction-dependent \(V\)를 다음 세 비용으로 분해한다.

1. deterministic fixed-\(Q'\) mean \(\delta_Q\),
2. outer weighted fluctuation \(t\),
3. adaptive deletion \(Lr_E(1+\eta)\).

2와 3은 explicit하고 asymptotically 0으로 보낼 수 있다. 1은 그대로 남는다.
실제로 모든 \(B_q=c_0U\)인 abstract weight family에서는
\(D_Q=c_0NU\), \(\mathbb EW=\sigma c_0NU\)다. one/two-point randomness만으로 fixed
mean이 사라진다고 주장할 수 없다.

Theory 92 inverse transform을 넣으면 fixed mean은 식 (93.11)이다. \(q<f\)이므로

\[
 \sum_{q\in Q'}A_h(q;U)
 =\sum_{q\in Q'}
 \sum_{\substack{\ell\ge0\\q+\ell f\le U\\(q+\ell f,h)=1}}
 \Lambda(q+\ell f).
 \tag{93.25}
\]

즉 small prime \(q\in(X,Y]\)와 같은 residue의 large prime-power mass를 결합한
shifted prime-pair형 sum이다. 한 residue의 upper나 전체 residue \(L^2\)와 동일한
object가 아니다.

## 7. modern source applicability

이번에 다음 primary sources를 원문으로 대조했다.

### Maynard I

Theorem 1.1은 한 fixed residue \(a\)에 대해 factored moduli \(q_1q_2\)를 **합한**
absolute error를 제어한다. prescribed \(f\) 하나의 relative error theorem이 아니다.
또 current \(Q'\)는 \(U\)와 함께 자라는 여러 prime residues다.

### Maynard III

Theorems 1.1--1.3은 residue에 대한 강한 uniformity를 주지만 modulus averages와
large-modulus factorization을 사용한다. 약한 theorem의 \(\delta\pi(U)\), 강한 theorem의
fixed log-power absolute saving은 \(\varphi(f)\)를 곱한 식 (93.11)의 relative
\(NU\) budget으로 자동 변환되지 않는다.

### Stadlmann

Theorem 1은 \(q\mid P(U^\delta)\)인 smooth moduli에 대한 absolute-error 합을 준다.
current \(f\)가 그 family에 들어가더라도 한 항을 버려 얻는
\(U(\log U)^{-A}\)형 bound는 fixed \(A\)에서 \(U/\varphi(f)\) scale의 relative
error가 아니다. \(N\)개 growing residues를 합쳐도 이 mismatch는 남는다.

### Klurman--Mangerel--Teräväinen

Theorem 1.3은 1-bounded multiplicative function과 typical smooth modulus를 다룬다.
\(\Lambda\)는 1-bounded multiplicative function이 아니고, primorial-type \(f\)는 작은
prime divisors를 거의 모두 포함해 Definition 1.1의 typical condition과 반대 방향이다.

### Leung

Theorem 1.1은 uniform Hardy--Littlewood prime-tuple conjecture를 가정하며
\(\varphi(q)\ge U^{1-o(1)}\) 쪽의 large-modulus range다. current
\(f=U^{1/d_f}\), \(d_f\ge21\)과 맞지 않고 unconditional branch도 아니다.

따라서 확인한 source 중 식 (93.11)의 fully numerical prescribed-primorial upper를
주는 drop-in은 없다. 이는 모든 future dispersion refinement의 불가능성 명제가 아니다.

## 8. 상태표

| 항목 | 판정 |
|---|---|
| outer weighted expectation | <code>EXACT FINITE</code> |
| outer weighted variance | <code>EXACT INPUTS / EXPLICIT UPPER</code> |
| fluctuation failure mass | <code>PARAMETERIZED EXPLICIT</code> |
| adaptive deletion cost | <code>PARAMETERIZED EXPLICIT</code> |
| construction-dependent \(D_V\) | <code>REDUCED TO FIXED \(D_Q\)</code> |
| fixed \(Q'\) mean \(D_Q\) | <code>OPEN</code> |
| modern source drop-in | <code>NOT IDENTIFIED</code> |
| blind same-law moment | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 9. 검증 범위

<code>source/dep_r09_outer_law_sparse_mean.py</code>와 단위시험은 finite probability
table에서 signed weighted mean·variance를 exact <code>Fraction</code>으로 전수하고,
common-shock pair error, \(L^\infty\) normalization, adaptive worst-case deletion과
union failure mass를 검산한다. actual primes, huge \(X\), threshold는 계산하지 않는다.

Lean은 weighted covariance source를 공리화하지 않고, variance certificate를 premise로
받은 normalized scalar bound, adaptive-deletion ratio와 strict event composition만
검사한다. FGKMT/FMT probability theorem과 modern analytic sources를 local axiom으로
넣지 않는다.

## 10. 다음 gate

다음 최소 gate는 식 (93.11)의 deterministic fixed-\(Q'\) mean이다. 권장 순서는

1. 식 (93.25)을 pre-absolute-value bilinear/dispersion form으로 정확히 전개하고,
2. existing R10 two-prime upper가 centered 양측식에 제공하는 것과 제공하지 않는 것을
   분리하며,
3. explicit binary-prime dispersion source가 없으면 새 lemma의 필요 statement·상수·
   cutoff를 먼저 고정하는 것

이다. construction redesign은 별도 승인 전 착수하지 않는다.

## 11. 참고문헌

- J. Maynard, *Primes in arithmetic progressions to large moduli I: Fixed
  residue classes*, [arXiv:2006.06572](https://arxiv.org/abs/2006.06572).
- J. Maynard, *Primes in arithmetic progressions to large moduli III: Uniform
  residue classes*, [arXiv:2006.08250](https://arxiv.org/abs/2006.08250).
- J. Stadlmann, *On primes in arithmetic progressions and bounded gaps between
  many primes*, [arXiv:2309.00425](https://arxiv.org/abs/2309.00425).
- O. Klurman, A. P. Mangerel and J. Teräväinen, *Multiplicative functions in
  short arithmetic progressions*, [arXiv:1909.12280](https://arxiv.org/abs/1909.12280).
- S.-K. Leung, *Moments of primes in progressions to a large modulus*,
  [arXiv:2402.07941](https://arxiv.org/abs/2402.07941).
