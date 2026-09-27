# Theory 92 — DEP-R09 blind residue-discrepancy·pointwise envelope 환원

- 상태:
  <code>BLIND_INVERSE_TRANSFORM_EXACT /
  POINTWISE_BRUN_TITCHMARSH_ENVELOPE_EXPLICIT /
  NORMALIZED_PAIR_LOSS_REDUCED_TO_BETA /
  SPARSE_CENTERED_MEAN_OPEN</code>
- 선행 정본: Theory 53--55, 83, 89--91, review 100
- 기계 원장:
  [blind residue-discrepancy v1](data/Sono_FMT_DEPR09_blind_residue_discrepancy_v1.json)
- 목표: blind character weight를 residue-class prime discrepancy로 exact하게
  역변환하고, explicit pointwise upper를 Theory 91 moment와 결합해 남는 최소 analytic
  gate를 분리한다.
- 비목적: sparse centered mean을 임의로 작다고 가정하거나, actual prime 계산,
  threshold calculator, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

> **2026-09-27 successor:** [Theory 93](93_Sono_FMT_DEPR09_outer_law_sparse_centered_mean_reduction.md)은
> outer weighted fluctuation과 outcome-dependent deletion을 explicit하게 흡수해 이
> 문서의 construction-dependent \(D_V\)를 deterministic fixed-\(Q'\) mean \(D_Q\)로
> 환원했다. 최신 analytic gate는 식 (93.11)이다.

## 1. 결론

Theory 89--90처럼

\[
 \mathfrak q=fh,\qquad(f,h)=1,
 \qquad\widetilde\psi=\psi\bmod f\otimes\chi_{0,h}
 \tag{92.1}
\]

라 하자. reduced residue \(v\bmod f\)에 대해

\[
 A_h(v;U):=
 \sum_{\substack{n\le U\\n\equiv v\pmod f\\(n,h)=1}}\Lambda(n),
 \qquad
 S_h(U):=
 \sum_{\substack{n\le U\\(n,fh)=1}}\Lambda(n)
 \tag{92.2}
\]

를 정의한다. blind weight는

\[
 B_h(v):=
 \sum_{\substack{\psi\bmod f\\\psi\ne\psi_0}}
 \overline{\psi(v)}Z_{\widetilde\psi}^{(\mathfrak q)}(U).
 \tag{92.3}
\]

finite character orthogonality로 exact하게

\[
 \boxed{B_h(v)=\varphi(f)A_h(v;U)-S_h(U).}
 \tag{92.4}
\]

따라서 blind weight는 실제로 **실수**다. covering 전에 고정된 reduced-residue
vertex set \(V\), \(M:=|V|\)에는

\[
 \boxed{
 D_V:=\sum_{v\in V}B_h(v)
 =\varphi(f)\sum_{v\in V}A_h(v;U)-M S_h(U).}
 \tag{92.5}
\]

Montgomery--Vaughan 1973 Theorem 2와 elementary prime-power bound를 합치면 current
\(d_f\ge21\)에서

\[
 \boxed{|B_h(v)|<\frac{11}{5}U}
 \tag{92.6}
\]

인 fully explicit pointwise envelope를 얻는다. 그 결과 Theory 91의 inner covering
moment는, \(|D_V|\le\delta MU\)라 할 때,

\[
 \boxed{
 \frac{\mathbb E|\sum_{v\in V}B_h(v)X_v|^2}
 {(\rho MU)^2}
 \le
 \delta^2+\frac{121}{25}\Gamma_M,}
 \tag{92.7}
\]

\[
 \Gamma_M:=
 \frac{1+\alpha}{\rho M}-\frac1M
 +\beta\frac{M-1}{M}.
 \tag{92.8}
\]

특히 \(M\to\infty\)에서 \(\Gamma_M\to\beta\)다. Theory 91의
\(\beta\rho M>1\)은 pair-error operator가 diagonal covariance보다 작지 않다는
올바른 진단이지만, pointwise \(L^\infty\)와 \(M^2U^2\) success scale을 함께 쓰면
그 dimension loss가 최종 sufficient gate에서 \(\beta\)로 정규화된다.

이것은 blind branch의 실질적인 진전이다. 그러나 식 (92.5)의 construction-dependent
sparse centered mean \(D_V\)에 numerical \(\delta\ll1\) bound가 없다.
Brun--Titchmarsh는 one-sided upper이고 centered discrepancy를 작게 만들지 않는다.
따라서 blind same-law moment와 \(X_{\rm cert}\)는 아직 OPEN이다.

## 2. inverse transform 증명

식 (92.3)에 lifted character sum을 대입하고 유한합 순서를 바꾸면

\[
 \begin{aligned}
 \sum_{\psi\bmod f}\overline{\psi(v)}
 Z_{\widetilde\psi}^{(\mathfrak q)}(U)
 &=
 \sum_{\substack{n\le U\\(n,h)=1}}\Lambda(n)
 \sum_{\psi\bmod f}\overline{\psi(v)}\psi(n)\\
 &=\varphi(f)A_h(v;U).
 \end{aligned}
 \tag{92.9}
\]

여기서 \((v,f)=1\)이고 \(n\equiv v\pmod f\)이면 자동으로 \((n,f)=1\)다.
principal \(\psi_0\)의 항은 정확히 \(S_h(U)\)이므로 이를 빼면 식 (92.4)가 나온다.

우변이 실수이므로 character 표현이 complex여도 \(B_h(v)\in\mathbb R\)다. 이는
blind subfamily에는 complex positive/negative four-way split이 필요하지 않음을 뜻한다.
nonblind family에는 이 결론을 확대하지 않는다.

full reduced-residue Parseval도

\[
 \boxed{
 \sum_{\substack{v\bmod f\\(v,f)=1}}|B_h(v)|^2
 =\varphi(f)
 \sum_{\substack{\psi\bmod f\\\psi\ne\psi_0}}
 |Z_{\widetilde\psi}^{(\mathfrak q)}(U)|^2
 =\varphi(f)V_{\rm blind}^{(\mathfrak q)}(U).}
 \tag{92.10}
\]

그러나 current vertex set은 전체 reduced residues가 아니라 \(Q'\)에서 outer sieve와
예외 삭제를 거친 sparse set이다. 식 (92.10)은 식 (92.5)의 signed mean을 작게 만들지
않는다.

## 3. Montgomery--Vaughan 원문과 pointwise prime upper

새로 다시 확보한 primary source는 H. L. Montgomery and R. C. Vaughan,
*The large sieve*, Mathematika 20 (1973), 119--134다. 저자 공개 PDF는 16쪽이고
SHA-256은

~~~text
720058876b871e8d1fef22acb285550a227ae9e3b1bedaa042f6d62f3299e8b9
~~~

이다. 이는 Theory 83에서 고정한 source hash와 정확히 같다. printed p.121 Theorem 2,
식 (1.10)은 \(y>k\), \((k,l)=1\)에서

\[
 \pi(x+y;k,l)-\pi(x;k,l)
 <\frac{2y}{\varphi(k)\log(y/k)}
 \tag{92.11}
\]

를 준다. \(x=0,y=U,k=f,l=v\)로 두면

\[
 \theta(U;f,v)
 \le\log U\,\pi(U;f,v)
 <\frac{2U\log U}{\varphi(f)\log(U/f)}.
 \tag{92.12}
\]

effective exponent \(d_f=\log U/\log f\)를 쓰면

\[
 \frac{2\log U}{\log(U/f)}
 =\frac{2d_f}{d_f-1}
 \le\frac{21}{10}
 \qquad(d_f\ge21).
 \tag{92.13}
\]

Theorem 2는 cutoff나 implied multiplier가 없는 explicit upper다. 하지만 upper constant가
main term의 두 배 규모이므로 centered PNT나 lower bound로 읽지 않는다. Maynard의
Brun--Titchmarsh 연구도 bounded \(\log U/\log f\)에서 exceptional-zero 문제 없이
일반적으로 constant \(<2\)를 기대할 수 없다는 경계를 설명한다. 이 인용은 식 (92.11)의
원 source를 대체하지 않는다.

## 4. prime-power 보정과 \(11/5\) envelope

모든 prime power를 residue 조건 없이 넓히면

\[
 \begin{aligned}
 0\le\psi(U)-\theta(U)
 &=\sum_{p\le\sqrt U}
 \left(\left\lfloor\frac{\log U}{\log p}\right\rfloor-1\right)\log p\\
 &\le\pi(\sqrt U)\log U
 \le\sqrt U\log U.
 \end{aligned}
 \tag{92.14}
\]

따라서 \(A_h(v;U)\le\psi(U;f,v)\)와 식 (92.12)--(92.14)에서

\[
 \frac{\varphi(f)A_h(v;U)}U
 <\frac{2d_f}{d_f-1}
 +\frac{\varphi(f)\log U}{\sqrt U}.
 \tag{92.15}
\]

또 Theory 55에서 이미 사용한 Rosser--Schoenfeld upper
\(\theta(U)<21U/20\)로

\[
 \frac{S_h(U)}U
 \le\frac{\psi(U)}U
 <\frac{21}{20}+\frac{\log U}{\sqrt U}.
 \tag{92.16}
\]

다음 elementary correction gates를 둔다.

\[
 \frac{\varphi(f)\log U}{\sqrt U}\le\frac1{10},
 \qquad
 \frac{\log U}{\sqrt U}\le\frac1{20}.
 \tag{92.17}
\]

Theory 90의 \(f\le U^{1/21}\)을 쓰면 첫 좌변은
\((\log U)U^{-19/42}\) 이하이다. 두 함수는 \(\log U\ge20\)에서 감소하고,
endpoint에서도 각각 \(1/10,1/20\)보다 작다. existing child는 \(U>e^{20}\)을
압도적으로 만족하므로 새 장시간 계산이나 threshold search 없이 식 (92.17)이 성립한다.

식 (92.13), (92.15)--(92.17)은

\[
 0\le\varphi(f)A_h(v;U)<\frac{11}{5}U,
 \qquad
 0\le S_h(U)<\frac{11}{10}U.
 \tag{92.18}
\]

두 항이 비음수이므로 차의 절댓값은 합이 아니라 두 upper의 maximum 이하이다. 식 (92.4)로
식 (92.6)을 얻고, 임의 \(V\)에

\[
 \sum_{v\in V}|B_h(v)|^2
 <\frac{121}{25}MU^2.
 \tag{92.19}
\]

이 restricted L2 bound는 full energy \(\varphi(f)V_{\rm blind}\)를 지불하지 않는다.

## 5. Theory 91 moment의 success-scale 정규화

fixed outer fiber에서 Theory 91과 같은 inner survivor indicator \(X_v\)를 쓴다.

\[
 K_M:=(1+\alpha)\rho-\rho^2+
 \beta\rho^2(M-1).
 \tag{92.20}
\]

식 (91.5), (92.19)와 \(|D_V|\le\delta MU\)를 합치면

\[
 \mathbb E\left|\sum_{v\in V}B_h(v)X_v\right|^2
 \le
 \rho^2\delta^2M^2U^2+
 \frac{121}{25}K_MMU^2.
 \tag{92.21}
\]

\(\rho^2M^2U^2\)로 나누면 식 (92.7)--(92.8)이다. exact하게

\[
 \Gamma_M-\beta
 =\frac1M\left\{\frac{1+\alpha}{\rho}-1-\beta\right\}.
 \tag{92.22}
\]

따라서 fixed \(\rho,\alpha,\beta\)에서 finite-size correction은 \(O(1/M)\)이고
pair term은 \(\beta\)로 수렴한다. Theory 91 common-shock witness와 모순이 아니다.
그 witness도 all-one weights에서 variance excess가 \(\beta\rho^2M^2\)이므로
\((\rho M)^2\)로 나누면 정확히 \(\beta\)다.

inner success event의 conditional mass를 \(p_{\rm in}>0\)라 하고, 그 event에서

\[
 M_\omega\ge\lambda\rho M,
 \qquad0<\lambda\le1
 \tag{92.23}
\]

이라 하자. Markov를 success-event failure mass와 합치면 다음 strict gate가 충분하다.

\[
 \boxed{
 \delta^2+\frac{121}{25}\Gamma_M
 <\tau_{\rm blind}^2p_{\rm in}\lambda^2.}
 \tag{92.24}
\]

실제로 좌변은 전체 inner law의 raw moment upper이므로 correlation-bad mass는
\(p_{\rm in}\)보다 작고 success와 correlation-good의 교집합이 양의 질량을 가진다.
outer fiber마다 uniform하게 식 (92.24)을 증명해야 global law에 올릴 수 있다.

## 6. 남은 centered mean의 정확한 성격

식 (92.5)의 numerical mean gate는

\[
 \boxed{
 \left|
 \varphi(f)\sum_{v\in V}A_h(v;U)-M S_h(U)
 \right|
 \le\delta MU.}
 \tag{92.25}
\]

이다. current vertices는 \(V\subset Q'\cap\mathscr S(\mathbf A)\)에서 예외점을
지운 소수들이고 \(v<f\)다. 따라서 첫 합은

\[
 \sum_{v\in V}
 \sum_{\substack{\ell\ge0\\v+\ell f\le U\\(v+\ell f,h)=1}}
 \Lambda(v+\ell f)
\]

인 construction-dependent sparse residue prime mass다. \(v\) 자체도 prime이므로
이는 shifted prime-pair 성격을 가진다.

확인한 source들의 경계는 다음과 같다.

1. Montgomery--Vaughan Brun--Titchmarsh는 각 residue의 one-sided upper만 준다.
2. Vaughan/Friedlander--Goldston variance와 Theory 83 large sieve는 전체 reduced
   residue \(L^2\) 또는 modulus average를 다루며 식 (92.25)의 signed sparse mean을
   current budget으로 닫지 않는다.
3. outer-sieve cardinality theorem은 unweighted subset count이고 \(A_h(v;U)\)라는
   prime-error weight의 centered mean theorem이 아니다.
4. standard two-prime sieve upper만으로는 식 (92.25)의 양측 centered error를 얻지
   못한다.

따라서 식 (92.25)은 새로 정확히 분리된 root analytic gate다. 전 문헌에 그러한 정리가
없다거나 새 정리라는 novelty 주장은 하지 않는다.

## 7. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 |
|---|---|
| blind character inverse transform | <code>EXACT FINITE</code> |
| blind weight의 real-valued residue discrepancy | <code>EXACT</code> |
| MV1973 pointwise prime upper | <code>PRIMARY SOURCE EXPLICIT</code> |
| prime-power correction·\(11/5\) envelope | <code>PROJECT EXPLICIT</code> |
| normalized pair loss | <code>\(\Gamma_M\to\beta\)</code> |
| Theory 91 \(\beta\rho M\) structural obstruction | <code>REMOVED AT SUCCESS-SCALE WITH L∞</code> |
| sparse selected-residue centered mean \(\delta\) | <code>OPEN</code> |
| outer-fiber uniformity | <code>OPEN</code> |
| blind same-law moment | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 8. 검증 범위

<code>source/dep_r09_blind_residue_discrepancy.py</code>와 단위시험은
modulo 5의 네 character를 Gaussian rational로 exact 전수해 식 (92.4), (92.5),
(92.10)을 독립 검산한다. 또한 \(d_f=21\) endpoint의 \(21/10\), \(11/5\),
\(11/10\)과 식 (92.8)의 rational fixture를 검사한다. prime이나 threshold를
열거하지 않는다.

Lean은 inverse transform의 analytic source를 공리화하지 않고, pointwise bound에서
restricted L2로 가는 scalar terminal, normalized moment division, strict success gate와
rational coefficient만 검사한다. finite Dirichlet-character orthogonality,
Montgomery--Vaughan Theorem 2와 Rosser--Schoenfeld theorem은 local axiom으로 넣지 않는다.

## 9. 다음 gate와 중단 판정

다음 최소 gate는 식 (92.25)의 fully numerical centered discrepancy다. 가능한 순서는

1. outer-random law에서 \(D_V\)의 mean/variance를 actual weight와 함께 직접 계산,
2. fixed \(V\)에 대한 prime-pair/dispersion source의 current primorial 적용성 감사,
3. 어느 것도 current law에서 닫히지 않으면 construction redesign을 별도 승인받아 검토

이다.

이번 결과는 full character energy 장벽과 inner pair dimension 진단 사이에 있던
불필요한 \(\varphi(f)\)·\(\rho M\) loss를 제거하고 병목을 하나의 signed mean으로
축약한 큰 구조 진전이다. 다만 numerical range는 아직 없으므로 calculator를 만들지 않는다.

## 10. 참고문헌

- H. L. Montgomery and R. C. Vaughan, *The large sieve*, Mathematika 20
  (1973), 119--134,
  [DOI 10.1112/S0025579300004708](https://doi.org/10.1112/S0025579300004708).
- J. Maynard, *On the Brun--Titchmarsh theorem*, Acta Arith. 157 (2013),
  249--296, [arXiv:1201.1777](https://arxiv.org/abs/1201.1777).
- R. C. Vaughan, *On a variance associated with the distribution of primes in
  arithmetic progressions*, Proc. London Math. Soc. 82 (2001), 533--553,
  [DOI 10.1112/plms/82.3.533](https://doi.org/10.1112/plms/82.3.533).
