# Theory 99 — DEP-R09 explicit density-exponent-99 route audit

- 상태:
  <code>EXPLICIT_DENSITY99_FIXED_F_TRANSFER_VALID /
  CURRENT_RANGE_OVERLAP_CONFIRMED /
  OPTIMISTIC_THEOREM23_FACTOR_GT_49 /
  DIRECT_BLACK_BOX_ROUTE_NOT_SUFFICIENT</code>
- 선행 정본: Theory 58, 90, 98, review 107
- 기계 원장:
  [explicit density-99 route v1](data/Sono_FMT_DEPR09_explicit_density99_route_v1.json)
- 목표: fully explicit Thorner--Zaman density exponent 99를 current fixed \(f\)
  full-interval endpoint에 대입하고 direct Theorem 2.3 certificate의 실제 크기를 판정한다.
- 비목적: 큰 upper certificate를 actual error의 lower bound로 읽거나, sharp \(12/5\)
  density·stronger VK·다른 full-interval proof의 불가능성을 주장하거나, actual 계산,
  threshold calculator, PAP-11, DEP-R09, numerical \(X_{\rm cert}\)를 닫는 것.

> **2026-09-28 successor:** [Theory 100](100_Sono_FMT_DEPR09_sharp_density_fixed_f_audit.md)은
> Theory 71 sharp near-one package도 PAP outer costs 제거 뒤 density core \(>10^6\),
> \(\omega^{-6}\)-only counterfactual \(>4000\)임을 보였다. 다음 gate는 structural
> detector/cancellation proof다.

## 1. 결론

Thorner--Zaman의 fully explicit density Theorem 1.2는 \(Q\ge3\),
\(\sigma\ge39/40\)에서

\[
 \boxed{
 N(\sigma,Q)
 \le10^{88}\left(10^{421}Q^{99}\right)^{1-\sigma}.}
 \tag{99.1}
\]

Fixed modulus \(f\)와 height \(T\ge e\)에
\(Q:=\max\{f,T,3\}\)를 택한다. Characters modulo \(f\)의 primitive inducing
conductors는 \(r\mid f\le Q\)이고 \(|\gamma|\le T\le Q\)이므로 해당 zeros는 식
(99.1)의 family에 포함된다. \(Q\le fT\)에서

\[
 \boxed{
 N_f(\sigma,T)
 \le10^{88}
 \left(10^{421}(fT)^{99}\right)^{1-\sigma}.}
 \tag{99.2}
\]

따라서 modulus·height quantifier 방향은 current fixed family에 안전하다.

이 exponent를 Thorner--Zaman Remark 2.4의 direct black-box replacement로 쓰면

\[
 c_7=99,qquad \theta=1-\frac1{99}=\frac{98}{99}.
 \tag{99.3}
\]

Theorem 2.3 proof가 사용하는 lower real part는

\[
 \sigma_0=\theta+\varepsilon-\varepsilon\theta
 =\frac{98}{99}+\frac{\varepsilon}{99}
 >\frac{98}{99}>\frac{39}{40},
 \tag{99.4}
\]

이므로 Theorem 1.2의 \(\sigma\) range도 맞는다.

Full interval에서 \(U/\varphi(f)\ge U/f=U^{1-1/d_f}\)를 쓰면 source range의
충분조건은

\[
 \boxed{
 0<\varepsilon\le\frac1{99}-\frac1{d_f}.}
 \tag{99.5}
\]

Positive margin에는 \(d_f>99\)가 필요하다. Theory 90의 \(d_f<416\)을 함께 쓰면

\[
 \boxed{
 0<\varepsilon<\frac1{99}-\frac1{416}
 =\frac{317}{41184}.}
 \tag{99.6}
\]

즉 explicit exponent 99와 current range는 **겹친다**. 그러나 error certificate는
small하지 않다.

Explicit source Lemma 2.3의 McCurley zero-free constant를

\[
 c_M:=\frac1{9.645908801}
 =\frac{10^9}{9645908801}
 \tag{99.7}
\]

로 두고 \(t\ge e\)에서

\[
 \delta_M(t):=\frac{c_M}{\log(ft)}
 \tag{99.8}
\]

를 사용한다. Actual \(B_0\) branch는 Theory 98처럼 possible secondary main을
common main error로 흡수하되, 여기서는 available explicit standard zero-free width만
진단한다.

Theorem 2.3의 첫 relative factor에 나타나는 sup를

\[
 S_{99}:=
 \sup_{e\le t\le U^{(1-\theta)(1-\varepsilon)}/f}
 \frac{U^{-\varepsilon^2\delta_M(t)}}{\sqrt t}
 \tag{99.9}
\]

라 하자. 식 (99.5)는 upper endpoint exponent에

\[
 \frac{1-\varepsilon}{99}-\frac1{d_f}
 \ge\frac{98}{99}\varepsilon>0
 \tag{99.10}
\]

을 주므로 sufficiently large \(U\)에서 \(t=e\)가 interval에 들어간다. 따라서

\[
 S_{99}\ge
 \frac1{\sqrt e}
 \exp\left\{-\varepsilon^2c_Md_f
 \frac{\log f}{\log f+1}\right\}.
 \tag{99.11}
\]

Current 전체 range에서 exact rational calculation은

\[
 \boxed{
 \varepsilon^2c_Md_f
 <\left(\frac{317}{41184}\right)^2
 \frac{10^9}{9645908801}\,416
 =\frac{3140281250000}{1229014178061813}
 <\frac3{1000}.}
 \tag{99.12}
\]

을 준다. \(e^{-x}>1-x\) for \(x>0\), \(e<4\)를 쓰면

\[
 \boxed{
 S_{99}>\frac{997}{2000}.}
 \tag{99.13}
\]

Theorem 2.3의 앞 factor는 \(\log U/\log f=d_f\)이므로, multiplier를 낙관적으로
1로 두고 source의 \(10^{88},10^{421}\) 비용마저 무시해도

\[
 \boxed{
 d_fS_{99}>
 99\frac{997}{2000}
 =\frac{98703}{2000}>49.}
 \tag{99.14}
\]

따라서 explicit exponent-99 theorem을 Theorem 2.3에 black-box로 넣는 direct
certificate는 Theory 98의 small centered endpoint error를 인증하지 못한다. 이는
actual prime error의 lower bound가 아니며, sharp \(12/5\) numericalization 또는
structurally different full-interval proof는 계속 OPEN이다.

## 2. Fixed family가 explicit density box에 들어가는가

식 (99.1)의 \(N(\sigma,Q)\)는 primitive conductor \(q\le Q\), height
\(|\gamma|\le Q\)인 모든 zeros를 센다. Character modulo \(f\)는 unique primitive
character of conductor \(r\mid f\)에서 induce된다. Near-one nontrivial zeros는 primitive
\(L\)-function의 zeros이고 imprimitive Euler factors는 별도 near-one zeros를 만들지 않는다.

따라서 \(Q=\max\{f,T,3\}\) box로 넓히는 것은 upper-bound 방향이다. Modulus average를
fixed modulus theorem으로 잘못 승격한 것이 아니라, fixed family를 더 큰 nonnegative
count 안에 포함한 것이다.

Theorem 1.2의 huge constants를 식 (99.2)에 그대로 보존했다. 아래 failure floor는 이
constants를 사용하기도 전에 생기므로, constants를 1로 축소한 낙관 진단보다 actual direct
certificate가 좋아질 근거는 없다. 다만 source proof를 재배열해 전혀 다른 coefficient를
얻는 가능성은 배제하지 않는다.

## 3. Range margin과 \(t=e\) endpoint

\(U=f^{d_f}\), \(\varphi(f)\le f\)에서

\[
 \frac{U}{\varphi(f)}\ge U^{1-1/d_f}.
 \tag{99.15}
\]

이를 \(U^{\theta+\varepsilon}\) 이상으로 만들면 식 (99.5)가 나온다. \(d_f=99\)에서는
positive \(\varepsilon\)가 없고, \(d_f>99\)에서만 source range가 열린다.

Theorem 2.3의 sup upper endpoint가 lower endpoint \(e\)보다 큰지도 별도 확인해야 한다.
식 (99.10)의 positive exponent 때문에 이 조건은 finite cutoff 뒤 성립한다. 따라서 sup가
empty라는 convention으로 식 (99.14)를 우회할 수 없다.

## 4. Explicit zero-free width로 생기는 floor

At \(t=e\), \(\log(fe)=\log f+1\)이고

\[
 \varepsilon^2\delta_M(e)\log U
 =\varepsilon^2c_Md_f\frac{\log f}{\log f+1}
 <\varepsilon^2c_Md_f.
 \tag{99.16}
\]

식 (99.12)는 이 exponent가 current range 전체에서 0.003보다 작다는 뜻이다. 즉 explicit
density exponent 99가 강제하는 tiny \(\varepsilon\) 때문에, available standard
zero-free decay는 lower height \(t=e\)에서 사실상 작동하지 않는다. \(1/\sqrt t\)도
\(t=e\)에서는 fixed constant라 \(d_f\) prefactor를 상쇄하지 않는다.

Corollary 6.1의 all-\(\sigma\) exponent 127은 \(\theta=126/127\)와 더 작은
\(\varepsilon\)를 강제하므로 이 direct architecture를 개선하지 않는다.

## 5. 판정 범위

식 (99.14)가 거부하는 것은 다음 조합이다.

1. explicit density exponent 99를 Remark 2.4로 직접 사용,
2. Theorem 2.3의 sup norm을 그대로 사용,
3. Lemma 2.3의 explicit standard zero-free region을 사용,
4. current \(99<d_f<416\) range.

거부하지 않는 것은 다음이다.

- actual centered endpoint error가 작을 가능성,
- nonnumerical sharp exponent \(12/5\)의 future numericalization,
- stronger explicit VK region과 다른 optimization,
- pre-sup cancellation을 보존한 full-interval explicit-formula proof,
- prime-specific or conductor-block dispersion.

판정은 <code>DIRECT_CERTIFICATE_REJECTED</code>이지 mathematical impossibility가 아니다.

## 6. 상태표

| 항목 | 판정 |
|---|---|
| explicit Theorem 1.2 provenance | <code>VERIFIED</code> |
| fixed \(f,T\) subset transfer | <code>VALID</code> |
| \(\sigma_0>39/40\) | <code>EXACT</code> |
| current \(99<d_f<416\) overlap | <code>YES</code> |
| optimistic first-factor floor | <code>\(>49\)</code> |
| explicit-99 direct small-error certificate | <code>NO</code> |
| sharp \(12/5\) numerical multiplier·cutoff | <code>OPEN</code> |
| Theory 98 endpoint gate | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime/zero 계산 | <code>NOT READY / NOT RUN</code> |

## 7. 검증 범위

<code>source/dep_r09_explicit_density99_audit.py</code>와 tests는
\(98/99>39/40\), epsilon ceiling \(317/41184\), McCurley rational constant,
decay exponent \(<3/1000\)와 optimistic floor \(98703/2000>49\)를 exact하게 검사한다.

Lean은 external density/PNT theorem을 local axiom으로 넣지 않고 range·rational terminal과
factor floor만 검사한다.

## 8. 다음 gate

다음 1순위는 sharp nonexceptional exponent \(12/5\) route의 numericalization이다.
Existing Theory 61--71은 Jutila near-one primitive averaged components를 parameterized
explicit하게 만들었으므로, 이를 fixed \(f\) full-interval norm에 재특수화하고
Theory 72--73의 loss tree 중 PAP에만 필요한 비용을 제거할 수 있는지 감사한다.

Explicit exponent-99 theorem을 threshold calculator 입력으로 사용하지 않는다.

## 9. 참고문헌

- J. Thorner and A. Zaman,
  [*An Explicit Version of Bombieri's Log-Free Density Estimate and Sárközy's
  Theorem for Shifted Primes*](https://arxiv.org/abs/2208.11123), Theorem 1.2,
  Corollary 6.1 and Lemma 2.3.
- J. Thorner and A. Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878),
  Theorem 2.3 and Remark 2.4.
