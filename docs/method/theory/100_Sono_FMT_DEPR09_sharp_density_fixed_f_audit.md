# Theory 100 — DEP-R09 sharp near-one density fixed-\(f\) audit

- 상태:
  <code>THEORY71_FIXED_F_SPECIALIZATION_EXACT /
  PAP_OUTER_LOSSES_REMOVED /
  TIGHTENED_DENSITY_CORE_GT_1E6 /
  THETA_MINUS_SIX_COUNTERFACTUAL_GT_4000</code>
- 선행 정본: Theory 61--73, 98--99, review 108
- 기계 원장:
  [sharp density fixed-f v1](data/Sono_FMT_DEPR09_sharp_density_fixed_f_v1.json)
- 목표: Theory 71 near-one density를 fixed \(f\), full-interval endpoint에
  재특수화하고 PAP 후단 비용을 모두 제거한 optimistic density-core certificate를
  current \(d_f<416\)에서 판정한다.
- 비목적: certificate coefficient를 actual endpoint error의 lower bound로 읽거나,
  \(\omega^{-6}\) 구조가 모든 증명에서 불가피하다고 주장하거나, construction redesign,
  actual 계산, threshold calculator, PAP-11, DEP-R09, numerical \(X_{\rm cert}\)를 닫는 것.

## 1. 결론

Theory 71의 averaged primitive family를 fixed endpoint에

\[
 Q=f,\qquad T=f^5,\qquad
 \mathcal D=Q^2T=f^7,qquad L=\log\mathcal D
 \tag{100.1}
\]

로 특수화한다. Primitive conductor \(r\mid f\)인 actual character family는
\(r\le Q\) family의 subset이므로 upper-bound 방향이 안전하다.

Near-one window \(0<1-\alpha\le\omega\le1/21\)에서 Theory 71은

\[
 \boxed{
 N^*_{\rm np}(\alpha,T,Q)
 \le2C_J(\omega)x^{2(1-\alpha)}
 \{3+r\log(2\mathcal D)\},}
 \tag{100.2}
\]

\[
 x=\mathcal D^{1+12\omega}L^2,qquad
 r=\max\{1-\alpha,L^{-1}\}.
 \tag{100.3}
\]

를 parameterized explicit하게 준다. 여기 baseline coefficient는

\[
 C_J(\omega)=\frac{884000}{9(1-\omega)^2\omega^6}.
 \tag{100.4}
\]

Theory 72의 endpoint normalization에 \(U=f^{d_f}\)를 넣으면

\[
 \kappa(\omega):=14(1+12\omega),
 \qquad
 \lambda(\omega,d_f):=1-\frac{\kappa(\omega)}{d_f}.
 \tag{100.5}
\]

가 된다. Maximal allowed window에서

\[
 \boxed{
 \omega=\frac1{21},\qquad
 \kappa=22,qquad
 \lambda=1-\frac{22}{d_f}.}
 \tag{100.6}
\]

따라서 \(21\le d_f\le22\)에서는 positive near decay가 없고, \(d_f>22\)에서만
이 certificate가 열린다.

Theory 98의 exceptional handling 뒤 available explicit standard zero-free constant를

\[
 c_M:=\frac1{9.645908801}
 =\frac{10^9}{9645908801}
 \tag{100.7}
\]

로 둔다. Theory 72 near integral의 가장 유리한 fixed-\(f\) decay shape는

\[
 \exp\left\{-\lambda\frac{c_Md_f}{5}\right\}
 =\exp\left\{-\frac{c_M(d_f-22)}5\right\}.
 \tag{100.8}
\]

Theory 73의 같은 source 안 finite-safe tightened coefficient는

\[
 \boxed{
 C_{J,{\rm tight}}
 =\frac{11503697604450072}{425315}
 =27047476821.7675\ldots .}
 \tag{100.9}
\]

Current \(d_f<416\)에서

\[
 \frac{c_M(d_f-22)}5
 <\frac{c_M\,394}{5}<9.
 \tag{100.10}
\]

\(e<3\)을 쓰고 PAP-specific positive prefactors를 **전부 1로 낮추어도** density core는

\[
 \boxed{
 C_{J,{\rm tight}}
 e^{-c_M(d_f-22)/5}
 >\frac{C_{J,{\rm tight}}}{3^9}
 =\frac{3834565868150024}{2790491715}
 >10^6.}
 \tag{100.11}
\]

따라서 principal branch, Maier selection, \(\psi\)-to-\(\pi\), centered factor 2,
Theory 72의 \(8/\lambda\), far branch와 모든 finite cutoff cost를 없애도 현재 tightened
density coefficient는 endpoint smallness를 인증하지 못한다.

더 강한 architecture diagnostic으로, current proof의 세 \(\omega^{-2}\) loss만
보존하고 모든 dimensionless factor를 1로 둔다. \(0<\omega\le1/21\)에서

\[
 \omega^{-6}\ge21^6.
 \tag{100.12}
\]

또 \(\kappa(\omega)\ge14\), \(d_f<416\)이므로 가장 유리한 decay조차

\[
 \frac{c_M(d_f-\kappa)}5
 <\frac{c_M\,402}{5}
 =\frac{80400000000}{9645908801}<9.
 \tag{100.13}
\]

따라서 \(\omega^{-6}\) architecture만 남긴 counterfactual도

\[
 \boxed{
 \omega^{-6}e^{-c_M(d_f-\kappa)/5}
 >\frac{21^6}{3^9}
 =\frac{117649}{27}>4000.}
 \tag{100.14}
\]

이다. 이 결과는 **현재 \(\omega^{-6}\) certificate architecture**에 관한 것이며,
새 detector, fixed-modulus-specific proof 또는 pre-sup cancellation의 불가능성 정리가 아니다.

## 2. 어떤 PAP 비용을 제거했는가

Theory 72--73은 pointwise PAP를 위해 다음을 추가로 지불한다.

- far-\(\alpha\) full-height branch,
- Gallagher explicit-formula와 modulus aggregation,
- principal zeta·exceptional transfer,
- Maier matrix의 positive main budget,
- \(\psi\)-to-\(\pi\)와 endpoint,
- final coefficient \(e^{-2}\) allocation.

Theory 100의 floor는 이 항들을 사용하지 않는다. Theory 71의 near-one density coefficient와
zero-free decay만 남긴다. 그러므로 Theory 72의 PAP upper를 endpoint 문제에 그대로 복사한
과대비용은 제거됐다.

그럼에도 식 (100.11), (100.14)가 크므로 ordinary PAP 후단 정리만으로는 gate가
닫히지 않는다. 최초 실패는 density detector coefficient 구조 안에 있다.

## 3. Fixed family specialization의 quantifier

Theory 71은 primitive conductors \(q_j\le Q\)를 한 번에 센다. Actual characters modulo
\(f\)는 unique primitive conductors \(r\mid f\)에서 induce된다. \(Q=f\)로 잡으면
actual family는 source family의 subset이다.

Height \(T=f^5\)는 Theory 72의 explicit-formula choice를 보존한다. 이 choice를 최적화할
가능성은 남지만, 식 (100.14)는 \(T\) 후단의 dimensionless costs를 모두 제거한 뒤에도
\(\omega^{-6}\)와 current zero-free decay만으로 4000보다 크다. 단순한 height-factor
polishing만으로 이 architecture를 small-error certificate로 만들 수 있다는 증거는 없다.

## 4. Tightened coefficient와 counterfactual의 역할

식 (100.11)은 Theory 73에서 실제로 증명한 finite-safe coefficient를 사용한다. Fixed
modulus에서는 \(\log f/L=1/7\) 같은 더 강한 비율로 residue factor를 더 줄일 수 있다.
그러나 이 개선은 dimensionless constant 수준이다.

식 (100.14)는 그 가능성을 과감하게 모두 허용해 모든 dimensionless factors를 1로 둔다.
남는 \(\omega^{-6}\) power만으로도 4000보다 크다. 따라서 다음 연구는

1. 세 \(\omega^{-2}\) loss 가운데 하나 이상을 제거하거나,
2. density upper를 pointwise sup 전에 prime-error phase와 결합하거나,
3. fixed-modulus-specific sharp source를 사용해야 한다.

이는 설계 우선순위이며 보편적 lower bound가 아니다.

## 5. 판정 범위

식 (100.11)--(100.14)가 거부하는 것은

- Theory 61--71 detector·weighted-square·area 구조를 유지하고,
- \(0<\omega\le1/21\), \(d_f<416\)을 쓰며,
- zero contributions를 nonnegative density upper로 먼저 바꾸는 certificate

다.

거부하지 않는 것은

- actual centered endpoint error의 smallness,
- density와 prime-error coefficient의 signed correlation,
- fixed-\(f\) direct zero detector,
- larger window을 허용하는 새로운 lemma,
- structurally different explicit formula or dispersion.

판정은 <code>CURRENT_CERTIFICATE_ARCHITECTURE_INSUFFICIENT</code>다.

## 6. 상태표

| 항목 | 판정 |
|---|---|
| Theory 71 fixed-family subset transfer | <code>VALID</code> |
| \(Q=f,T=f^5,\mathcal D=f^7\) specialization | <code>EXACT</code> |
| Theory 73 tightened core floor | <code>\(>10^6\)</code> |
| \(\omega^{-6}\)-only counterfactual floor | <code>\(>4000\)</code> |
| ordinary PAP outer-loss removal | <code>INSUFFICIENT</code> |
| actual endpoint error lower | <code>NOT PROVED</code> |
| structural detector/cancellation redesign | <code>OPEN</code> |
| Theory 98 endpoint gate | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime/zero 계산 | <code>NOT READY / NOT RUN</code> |

## 7. 검증 범위

<code>source/dep_r09_sharp_density_fixed_f_audit.py</code>와 tests는
\(\kappa(1/21)=22\), favorable decay exponent \(<9\), tightened coefficient floor
\(>10^6\)과 \(21^6/3^9=117649/27>4000\)을 exact rational로 검사한다.

Lean은 external density/PNT theorem을 local axiom으로 넣지 않고 parameter specialization,
coefficient·decay rational terminals만 검사한다.

## 8. 다음 gate

다음 최소 gate는 ordinary constant polishing이 아니라 다음 중 하나다.

1. \(\omega^{-6}\) detector architecture를 줄이는 fixed-modulus reproof,
2. Theorem 2.3 sup 이전의 signed character/prime-error cancellation 보존,
3. current window·coefficient를 근본적으로 개선하는 새 sharp density source.

Construction redesign이나 새 확률 law가 필요한 단계로 넘어가기 전, 우선 existing
explicit formula에서 pre-sup cancellation을 보존할 수 있는지 감사한다.

## 9. 참고문헌

- M. Jutila, [*On Linnik's Constant*](https://doi.org/10.7146/math.scand.a-11701).
- J. Thorner and A. Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878).
- O. Ramaré and S. Zuniga Alterman,
  [*An L2-bound for the Barban--Vehov weights*](https://arxiv.org/abs/2405.12662).
