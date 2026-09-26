# Theory 91 — DEP-R09 complex-weighted survivor moment·weighted nibble 감사

- 상태:
  <code>EXACT_COMPLEX_WEIGHTED_SECOND_MOMENT /
  ENTRYWISE_PAIR_ERROR_HAS_SHARP_BETA_M_LOSS /
  WEIGHTED_NIBBLE_SOURCE_NOT_DROP_IN</code>
- 선행 정본: Theory 53--54, 89--90, review 99
- 기계 원장:
  [weighted survivor-moment audit v1](data/Sono_FMT_DEPR09_weighted_survivor_moment_audit_v1.json)
- 목표: FGKMT one/two-point survival bounds가 fixed complex weights에 주는 exact
  second-moment certificate를 도출하고, weighted Rödl-nibble 선행정리의 actual-law
  적용 가능성을 판정한다.
- 비목적: actual covariance operator를 크다고 주장하거나, construction redesign,
  PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\)를 이번
  단계에서 수행·인증하는 것.

> **2026-09-27 successor:** [Theory 92](92_Sono_FMT_DEPR09_blind_residue_discrepancy_reduction.md)는
> blind weight가 real residue discrepancy이고 \(|B(v)|<11U/5\)임을 복원했다.
> 따라서 이 문서의 \(\beta\rho M>1\) operator/diagonal 진단은 유효하지만,
> \((\rho MU)^2\) success scale의 final sufficient gate에서는 pair factor가
> \(\beta\)로 정규화된다. 최신 최소 gate는 sparse selected-residue centered mean이다.

## 1. 결론

covering 전에 고정한 finite vertex set \(V\), \(M_V:=|V|\), complex weights
\((b_v)_{v\in V}\)와 final survival indicator \(X_v\in\{0,1\}\)를 둔다.

\[
 S_b:=\sum_{v\in V}b_vX_v.
 \tag{91.1}
\]

single·pair survival probability를

\[
 p_v:=\Pr(X_v=1),\qquad
 p_{vw}:=\Pr(X_v=X_w=1)\quad(v\ne w)
 \tag{91.2}
\]

라 하면 exact하게

\[
 \boxed{
 \mathbb E|S_b|^2
 =
 \sum_vp_v|b_v|^2
 +
 \sum_{v\ne w}p_{vw}b_v\overline{b_w}.}
 \tag{91.3}
\]

어떤 \(\rho\in(0,1]\), \(\alpha,\beta\ge0\)에 대해

\[
 p_v\le(1+\alpha)\rho,\qquad
 |p_{vw}-\rho^2|\le\beta\rho^2
 \tag{91.4}
\]

라 하자. 그러면

\[
 \boxed{
 \begin{aligned}
 \mathbb E|S_b|^2
 \le{}&
 \rho^2\left|\sum_vb_v\right|^2\\
 &+\left\{
 (1+\alpha)\rho-\rho^2
 +\beta\rho^2(M_V-1)
 \right\}
 \sum_v|b_v|^2.
 \end{aligned}}
 \tag{91.5}
\]

식 (91.5)는 arbitrary complex fixed weights에 대해 FGKMT 1·2점 정보만으로 얻는
직접적인 certificate다. pair-error contribution의 relative diagonal scale은
\(\beta\rho(M_V-1)\)이다.

current Theory 53 parameter에서

\[
 \boxed{
 \beta\rho M_V
 >
 \frac{468cX}{ab}
 >1.}
 \tag{91.6}
\]

따라서 available entrywise pair-error bound는 small covariance-operator
certificate가 아니다.

finite common-shock law는 식 (91.5)의 \(\beta M_V\) scaling을 exact하게 달성한다.
그러므로 one/two-point entrywise error만으로 이 factor를 보편 제거할 수 없다.

2025년 Gould--Kelly weighted pseudorandom matching theorem도 감사했지만 current
indexed variable-size covering law와 같은 확률 moment를 공급하는 drop-in은 아니다.
이 단계만 보면 다음 입력은 numerical covariance-operator 또는 blind event-energy
direct correlation이다. Theory 92 successor는 pointwise envelope로 pair dimension
loss를 정규화하고, 더 좁은 sparse centered-mean gate를 분리한다.

## 2. exact complex second moment

식 (91.1)의 square를 전개하면

\[
 |S_b|^2
 =
 \sum_v|b_v|^2X_v
 +
 \sum_{v\ne w}b_v\overline{b_w}X_vX_w.
 \tag{91.7}
\]

finite expectation을 항별로 취하면 식 (91.3)이 나온다. \(v,w\) ordered pair를
사용하므로 complex conjugate pair가 함께 들어가 최종값은 실수다.

ideal pair term을 더하고 빼면

\[
 \begin{aligned}
 \mathbb E|S_b|^2
 ={}&
 \rho^2\left|\sum_vb_v\right|^2\\
 &+\sum_v(p_v-\rho^2)|b_v|^2\\
 &+\sum_{v\ne w}(p_{vw}-\rho^2)b_v\overline{b_w}.
 \end{aligned}
 \tag{91.8}
\]

식 (91.4)와 triangle inequality로

\[
 \sum_v(p_v-\rho^2)|b_v|^2
 \le\{(1+\alpha)\rho-\rho^2\}\sum_v|b_v|^2,
 \tag{91.9}
\]

\[
 \left|
 \sum_{v\ne w}(p_{vw}-\rho^2)b_v\overline{b_w}
 \right|
 \le
 \beta\rho^2
 \left\{
 \left(\sum_v|b_v|\right)^2-\sum_v|b_v|^2
 \right\}.
 \tag{91.10}
\]

Cauchy로

\[
 \left(\sum_v|b_v|\right)^2
 \le M_V\sum_v|b_v|^2.
 \tag{91.11}
\]

식 (91.8)--(91.11)이 식 (91.5)를 준다.

## 3. \(\beta M_V\) factor의 finite sharpness

fair latent coin을 먼저 고른 뒤, 한 branch에서는 \(M_V=4\)개의 indicator를
iid Bernoulli \(1/8\), 다른 branch에서는 iid Bernoulli \(3/8\)로 뽑는다.
그러면

\[
 \rho=\frac14,\qquad
 p_{vw}
 =\frac12\left\{\left(\frac18\right)^2+
 \left(\frac38\right)^2\right\}
 =\frac5{64}
 =\left(1+\frac14\right)\rho^2.
 \tag{91.12}
\]

즉 \(\alpha=0,\beta=1/4\)다. 모든 \(b_v=1\)이면 exact enumeration은

\[
 \mathbb E|S_b|^2=\frac{31}{16}.
 \tag{91.13}
\]

independent Bernoulli-\(\rho\) baseline은 \(7/4=28/16\)이고 excess는

\[
 \frac3{16}
 =
 \beta\rho^2M_V(M_V-1).
 \tag{91.14}
\]

식 (91.5)도 정확히 \(31/16\)을 준다. 따라서 entrywise pair error만 아는
abstract class에서는 \(\beta M_V\) scaling이 sharp하다.

actual FGKMT law가 이 common-shock law라는 주장이 아니다. 더 작은 spectral norm을
얻으려면 formula (5.9)의 추가 구조를 쓰는 새 theorem이 필요하다는 뜻이다.

## 4. current FGKMT parameter에서 pair loss

Theory 53의

\[
 \rho=5^{-m},\qquad
 \beta=(1+\epsilon_h)e^{2\xi}-1,\qquad
 \xi=\frac{3^m}{b}
 \tag{91.15}
\]

를 쓴다. \(\epsilon_h\ge0\), \(e^{2\xi}\ge1+2\xi\), \(m\ge1\)에서

\[
 \beta\ge2\xi\ge\frac6b.
 \tag{91.16}
\]

\(m\le\log_5b\)이므로

\[
 \rho=5^{-m}\ge\frac1b.
 \tag{91.17}
\]

retained vertex floor는

\[
 M_V
 \ge\frac Xa\left(79cb-\frac2b\right)
 >78c\frac{Xb}{a}.
 \tag{91.18}
\]

마지막에는 \(cb^2>2\), \(b>2000\)을 썼다. 따라서

\[
 \beta\rho M_V
 >
 \frac6b\frac1b
 78c\frac{Xb}{a}
 =
 \frac{468cX}{ab}.
 \tag{91.19}
\]

existing child \(X\ge2\exp(10^{1000})\)에서는 오른쪽이 1보다 크다.
식 (91.5)의 pair-error coefficient는 diagonal \(\rho\sum|b|^2\)에 비해
작은 perturbation으로 인증되지 않는다.

이는 actual covariance가 크다는 하한이 아니다. available **certificate**가 arbitrary
weights에 충분히 작지 않다는 판정이다.

## 5. blind prime-error weights에 필요한 입력

Theory 89의 blind contribution은 fixed survivor weights로

\[
 R_{\rm blind}(\omega)
 =
 \sum_{v\in V}B(v)X_v,
 \qquad
 B(v):=
 \sum_{\psi\ne\psi_0}\overline{\psi(v)}
 Z_{\widetilde\psi}(U).
 \tag{91.20}
\]

식 (91.5)에 \(b_v=B(v)\)를 넣으면 deterministic analytic inputs는

\[
 \left|\sum_{v\in V}B(v)\right|^2,
 \qquad
 \sum_{v\in V}|B(v)|^2
 \tag{91.21}
\]

다. full residue Parseval은 두 번째 합을 상계할 수 있지만 식 (91.19)의
pair-error multiplier를 제거하지 않는다. 첫 번째 mean term도 fixed-\(f\)
aggregate prime-error theorem을 요구한다.

따라서 current one/two-point theorem은 필요한 object를 정확히 식 (91.21)로
줄이지만 그것을 numerical budget 아래로 보내지 못한다.

## 6. Gould--Kelly 2025 weighted nibble source

새로 확인한 primary source는 Gould--Kelly,
*Advancing the Rödl Nibble: New bounds on matchings and the list chromatic index of
hypergraphs*, arXiv:2511.11375v1이다. 로컬 PDF SHA-256은

~~~text
cad7ce8d7b2e7fc5562431d4178c5dcdf50be13d5b5b048ff5013e4970db653c
~~~

이다.

Theorem 1.4의 weighted conclusion은 nearly \(D\)-regular
\((k+1)\)-uniform hypergraph matching과 preselected family
\({\cal T}\) of **nonnegative** vertex weights를 다룬다. 각 weight는

\[
 \tau(V)\ge B\max_v\tau(v),
 \tag{91.22}
\]

support-size와 per-vertex family-incidence 조건도 만족해야 한다. 결론은 matching
leftover의 weighted mass에 대한 existence statement다.

current FGKMT/FMT object와의 차이는 다음과 같다.

1. edge sizes가 \(0\)부터 \(2k\)까지 변하고 index별 marginal law가 다르다.
2. output은 formula (5.9)의 conditional **covering law**이며 같은-stage overlap도
   허용한다. uniform hypergraph matching이 아니다.
3. 필요한 것은 한 matching의 existence가 아니라 actual final law에서의 numerical
   second moment다.
4. \(B(v)\)는 complex이고 real/imaginary positive/negative split을 해도
   regularity·law·quantitative mismatch는 남는다.
5. source는 asymptotic hierarchy \(1/D\ll1/A\ll\gamma\ll1/k\)를 사용하며
   current \(X_{\rm cert}\)에 넣을 numerical multiplier·finite cutoff·failure rate를
   제공하지 않는다.

따라서 Theorem 1.4는 관련 선행연구지만 drop-in으로 채택하지 않는다. current
construction을 그 theorem에 맞게 바꾸는 일은 별도 proof architecture redesign이고
사용자 승인 없이 자동 착수하지 않는다.

## 7. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 |
|---|---|
| arbitrary complex weighted second moment | <code>EXACT</code> |
| FGKMT 1·2점 기반 upper | <code>EXACT FINITE</code> |
| entrywise pair-error \(\beta M_V\) 제거 | <code>IMPOSSIBLE FROM THESE INPUTS ALONE</code> |
| project \(\beta\rho M_V\) smallness | <code>FAILS CERTIFICATE</code> |
| Gould--Kelly weighted theorem source | <code>VERIFIED</code> |
| Gould--Kelly current law drop-in | <code>NO</code> |
| numerical covariance-operator bound | <code>OPEN</code> |
| blind mean/L2 analytic bounds | <code>OPEN</code> |
| blind same-law weighted moment | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 8. 검증 범위

<code>source/dep_r09_weighted_survivor_moment_audit.py</code>와 단위시험은 exact
<code>Fraction</code> Gaussian arithmetic으로 다음을 검사한다.

1. arbitrary complex weights의 one/two-point expansion.
2. 식 (91.5)의 certificate.
3. common-shock mixture의 exact \(31/16\) moment와 \(3/16\) covariance excess.
4. \(\beta M_V\) scaling의 equality witness.
5. source hashes와 OPEN status의 fail-closed ledger.

Lean은 weighted-moment scalar upper, \(\ell_1\)-to-\(\ell_2\) factor,
common-shock rational witness와 project \(\beta\rho M_V\) terminal만 검사한다.
probability space, complex finite sums와 Gould--Kelly theorem을 local axiom으로
넣지 않는다.

## 9. 다음 gate와 작업 규모

다음 최소 gate는 actual formula (5.9) law의 covariance operator 또는
\(B(v)\)-specific event-energy correlation이다. 이는 current fixed 1·2-point
entrywise theorem보다 강한 lemma다.

checked weighted nibble source를 current law에 옮기려면 variable-size indexed
covering을 uniform matching으로 바꾸고 numerical constants를 재증명해야 하므로
단순 normalization 작업이 아니다. construction redesign 없이 계속할 수 있는
다음 source-first 경로는 식 (91.21)의 prime-specific mean/L2 theorem이다.

## 10. 참고문헌

- S. Gould and T. Kelly, *Advancing the Rödl Nibble: New bounds on matchings
  and the list chromatic index of hypergraphs*,
  [arXiv:2511.11375](https://arxiv.org/abs/2511.11375).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, JAMS 31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
