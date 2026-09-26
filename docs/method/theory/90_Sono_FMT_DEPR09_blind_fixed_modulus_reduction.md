# Theory 90 — DEP-R09 blind fixed-modulus·imprimitive correction 환원

- 상태:
  <code>BLIND_LIFT_TO_NATIVE_FIXED_MODULUS_EXACT /
  IMPRIMITIVE_PRIME_POWER_CORRECTION_PARAMETERIZED_EXPLICIT /
  NATIVE_FIXED_MODULUS_ENERGY_UPPER_OPEN</code>
- 선행 정본: Theory 76, 83--85, 89, review 98
- 기계 원장:
  [blind fixed-modulus reduction v1](data/Sono_FMT_DEPR09_blind_fixed_modulus_reduction_v1.json)
- 목표: Theory 89의 blind lifted characters를 native modulo-\(f\) character sum과
  explicit prime-power correction으로 환원하고, 기존 variance·pointwise PNT source의
  actual range를 재판정한다.
- 비목적: GRH 채택, native \(V_f\) upper의 임의 가정, PAP-11, DEP-R09, fixed
  \(2\times10^{-17}\), numerical \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

## 1. 결론

Theory 89와 같이

\[
 \mathfrak q=fh,\qquad(f,h)=1,\qquad
 \widetilde\psi=\psi\bmod f\otimes\chi_{0,h}.
 \tag{90.1}
\]

prime scale은 혼동을 피하려고

\[
 U:=\mathfrak q^d,\qquad21\le d\le186
 \tag{90.2}
\]

로 쓴다. nonprincipal \(\psi\bmod f\)에 대해 native와 lifted von Mangoldt sum을

\[
 Z_\psi^{(f)}(U):=\sum_{n\le U}\Lambda(n)\psi(n),
 \qquad
 Z_{\widetilde\psi}^{(\mathfrak q)}(U)
 :=\sum_{n\le U}\Lambda(n)\widetilde\psi(n)
 \tag{90.3}
\]

로 둔다. 그러면 exact하게

\[
 \boxed{
 Z_{\widetilde\psi}^{(\mathfrak q)}(U)
 =
 Z_\psi^{(f)}(U)-D_{\psi,h}(U),}
 \tag{90.4}
\]

\[
 D_{\psi,h}(U)
 :=
 \sum_{p\mid h}
 \sum_{\substack{j\ge1\\p^j\le U}}
 (\log p)\psi(p)^j.
 \tag{90.5}
\]

이며

\[
 \boxed{
 |D_{\psi,h}(U)|
 \le\omega(h)\log U=:L_h.}
 \tag{90.6}
\]

blind lifted energy와 native energy를

\[
 V_{\rm blind}^{(\mathfrak q)}(U)
 :=
 \sum_{\psi\ne\psi_0}
 |Z_{\widetilde\psi}^{(\mathfrak q)}(U)|^2,
 \qquad
 V_f(U):=
 \sum_{\psi\ne\psi_0}|Z_\psi^{(f)}(U)|^2
 \tag{90.7}
\]

로 두면 모든 \(\eta>0\)에서

\[
 \boxed{
 V_{\rm blind}^{(\mathfrak q)}(U)
 \le
 (1+\eta)V_f(U)
 +(1+\eta^{-1})\{\varphi(f)-1\}L_h^2.}
 \tag{90.8}
\]

따라서 imprimitive lift는 exact하게 분리됐고 correction도 explicit하다. 실제
analytic core는 \(V_f(U)\)의 prescribed fixed-\(f\), unconditional numerical upper다.

fixed modulus의 effective power exponent를

\[
 d_f:=\frac{\log U}{\log f}
 =d\frac{\log\mathfrak q}{\log f}
 \tag{90.9}
\]

라 하면 project range 전체에서

\[
 \boxed{
 21\le d_f<\frac{105}{47}d
 \le\frac{19530}{47}<416.}
 \tag{90.10}
\]

이 범위에 native \(V_f\)를 fully numerical unconditional하게 주는 checked
source는 식별되지 않았다.

## 2. prime-power correction identity

\(\Lambda(n)\ne0\)이면 \(n=p^j\)인 prime power다. \(p\nmid h\)이면
\(\widetilde\psi(p^j)=\psi(p)^j\), \(p\mid h\)이면 principal modulo-\(h\) factor가
0이어서 \(\widetilde\psi(p^j)=0\)이다. 따라서 native sum에서 정확히 \(p\mid h\)
prime powers만 제거되며 식 (90.4)--(90.5)가 나온다.

각 \(p\mid h\)에 대해

\[
 \left|
 \sum_{\substack{j\ge1\\p^j\le U}}
 (\log p)\psi(p)^j
 \right|
 \le
 \left\lfloor\frac{\log U}{\log p}\right\rfloor\log p
 \le\log U.
 \tag{90.11}
\]

\(h\)의 distinct prime divisors를 합하면 식 (90.6)이다. prime powers를 prime
하나로 세거나 \(\log U\) factor를 빠뜨리지 않는다.

## 3. energy transfer와 correction budget

복소수 \(a,b\)와 \(\eta>0\)에

\[
 |a-b|^2
 \le(1+\eta)|a|^2+(1+\eta^{-1})|b|^2.
 \tag{90.12}
\]

식 (90.4), (90.6)에 적용하고 \(\varphi(f)-1\)개 nonprincipal characters를 합하면
식 (90.8)이 나온다.

Theory 89의 blind Cauchy gate를 sieve-good 전체에서 uniform하게 쓰기 위해
\(M_\omega\ge M_{\min}\)과 \(M_\omega<\varphi(f)\)를 사용한다.
\(M/(\varphi(f)-M)\)은 증가하므로 sufficient target을

\[
 G_{\rm blind}
 :=
 \tau_{\rm blind}^2
 \frac{M_{\min}U^2}{\varphi(f)-M_{\min}}
 \tag{90.13}
\]

로 둔다. \(\eta=1\)에서 다음 두 strict condition이면 충분하다.

\[
 \boxed{
 V_f(U)<\frac14G_{\rm blind},\qquad
 \{\varphi(f)-1\}L_h^2<\frac14G_{\rm blind}.}
 \tag{90.14}
\]

실제로 식 (90.8)의 두 항이 각각 \(G_{\rm blind}/2\) 미만이므로
\(V_{\rm blind}^{(\mathfrak q)}<G_{\rm blind}\)다.

correction condition을 denominator 없이 쓰면

\[
 \boxed{
 4\{\varphi(f)-1\}\{\varphi(f)-M_{\min}\}
 \omega(h)^2(\log U)^2
 <
 \tau_{\rm blind}^2M_{\min}U^2.}
 \tag{90.15}
\]

이는 모든 항이 elementary한 parameterized explicit gate다. 최종
\(\tau_{\rm blind}\) allocation 전에 숫자 cutoff를 \(X_{\rm cert}\)처럼 고정하지 않는다.

## 4. correction은 analytic core blocker가 아니다

\(\varphi(f)\le f\le\mathfrak q\), \(\omega(h)\le X\),
\(\log U=d\log\mathfrak q\), \(M_{\min}\ge3X/(4\log X)\)인 favorable sufficient
bounds를 쓰면 식 (90.15)의 더 강한 충분조건은

\[
 \boxed{
 \mathfrak q^{\,2d-2}
 >
 \frac{16(\log X)X}{3\tau_{\rm blind}^2}
 \{d\log\mathfrak q\}^2.}
 \tag{90.16}
\]

이다. fixed \(\tau_{\rm blind}>0\)에서 좌변은 기존 child scale에 압도적으로 크다.
중요한 점은 correction의 finite gate를 썼다는 것이며, 최종 coefficient budget을
아직 고르지 않았으므로 식 (90.16)을 numerical \(X_{\rm cert}\)로 선언하지 않는다.

따라서 blind branch의 본질적 analytic blocker는 correction이 아니라 native
\(V_f(U)\) upper다.

## 5. effective fixed-modulus exponent

Theory 88--89는

\[
 \log f>\frac{47}{100}X.
 \tag{90.17}
\]

Rosser--Schoenfeld/Dusart theta upper를 느슨하게

\[
 \log\mathfrak q\le\vartheta(X)<\frac{21}{20}X
 \tag{90.18}
\]

로 쓰면

\[
 d_f
 =d\frac{\log\mathfrak q}{\log f}
 <
 d\,\frac{21/20}{47/100}
 =\frac{105}{47}d.
 \tag{90.19}
\]

또 \(f\le\mathfrak q\)이므로 \(d_f\ge d\). 식 (90.10)이 따른다.

이 range는 original full primorial exponent보다 최대 약 2.24배 클 뿐이며, fixed
modulus가 훨씬 작다는 사실을 arbitrary large \(d_f\)로 과장하지 않는다.

## 6. Bennett pointwise source range

Theory 76에서 Bennett--Martin--O'Bryant--Rechnitzer의 large-modulus branch는
modulus \(r>10^5\), prime scale \(U=r^D\)일 때 source cutoff를 보장하려면 이미

\[
 D\ge0.03\sqrt r(\log r)^2\ge900.
 \tag{90.20}
\]

가 필요하다. 현재 \(f>\exp(47X/100)>10^5\)이지만 식 (90.10)은

\[
 d_f<416<900.
 \tag{90.21}
\]

이므로 source cutoff와 actual fixed-\(f\) range는 겹치지 않는다. 정확한 \(f\)가
full primorial보다 작다는 사실만으로 Bennett branch가 적용되는 것은 아니다.

## 7. Vaughan·Friedlander--Goldston 재대조

Vaughan 2001 Theorem 1의 unconditional lower range를 \(Q=f\), \(U=f^{d_f}\)에
대입하면 fixed \(A\)에 필요한 조건은

\[
 A\ge
 \frac{(d_f-1)\log f}{\log(d_f\log f)}.
 \tag{90.22}
\]

우변은 growing \(f\)에서 발산한다. dyadic modulus moment라는 quantifier도
prescribed \(f\)와 다르다.

Theorem 2는 GRH conditional이고

\[
 f\ge U^{3/4+\varepsilon}
 \tag{90.23}
\]

를 요구한다. actual \(f=U^{1/d_f}\le U^{1/21}\)와 겹치지 않는다.

Friedlander--Goldston에는 GRH 아래 fixed-\(f\) implicit upper가 있지만 unconditional
fully numerical multiplier·cutoff가 아니다. 따라서 현재 정본에 채택하지 않는다.

## 8. Vaughan variance bridge의 재사용

Theory 85의 finite centering identity는 modulus \(f\)에도 그대로 적용된다.
native nonprincipal energy와 Vaughan residue variance 사이에는

\[
 V_f(U)
 +|\psi(U,\chi_{0,f})-U|^2
 =
 \varphi(f)V_{\rm Vau}(U,f).
 \tag{90.24}
\]

따라서

\[
 V_{\rm Vau}(U,f)
 <
 \frac{G_{\rm blind}}{4\varphi(f)}
 \quad\Longrightarrow\quad
 V_f(U)<\frac14G_{\rm blind}.
 \tag{90.25}
\]

이 bridge는 exact하지만 왼쪽의 current-regime numerical theorem은 OPEN이다.

## 9. raw large sieve도 native gate를 닫지 않는다

기존 scale에서 \(\varphi(f)>2M_{\min}\)은 Mertens/Rosser--Schoenfeld bound와
\(f>\exp(47X/100)\), \(M_{\min}<X^2\)에서 충분히 따른다. 그러면

\[
 \frac{G_{\rm blind}/4}{U^2}
 <
 \frac{\tau_{\rm blind}^2}{2}
 \le\frac{e^{-4}}2.
 \tag{90.26}
\]

반면 Theory 83의 source-derived raw large-sieve certificate를 modulus \(f\)와
exponent \(d_f\ge21\)에 적용하면

\[
 \frac{B_{\rm LS}(U,f)}{U^2}
 >
 5\log f.
 \tag{90.27}
\]

따라서 그 certificate는 native quarter-gate보다 크다. 이는 actual \(V_f\)의
하한이 아니라 raw coefficient-agnostic upper가 너무 느슨하다는 판정이다.

## 10. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 |
|---|---|
| native/lifted prime-power identity | <code>EXACT</code> |
| imprimitive correction pointwise upper | <code>PARAMETERIZED EXPLICIT</code> |
| blind/native energy transfer | <code>EXACT FINITE</code> |
| correction absorption gate | <code>PARAMETERIZED EXPLICIT</code> |
| effective exponent \(21\le d_f<416\) | <code>EXACT SCALE</code> |
| Bennett pointwise source overlap | <code>NO</code> |
| Vaughan unconditional prescribed-\(f\) coverage | <code>NO</code> |
| Friedlander--Goldston unconditional numerical upper | <code>NOT IDENTIFIED</code> |
| raw classical large-sieve native gate | <code>INSUFFICIENT CERTIFICATE</code> |
| native \(V_f(U)\) analytic upper | <code>OPEN</code> |
| blind direct weighted correlation | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 11. 검증 범위

<code>source/dep_r09_blind_fixed_modulus_reduction.py</code>와 단위시험은 exact
<code>Fraction</code>으로 다음을 검사한다.

1. finite prime-power list의 native = lifted + removed identity.
2. flexible energy transfer와 \(\eta=1\) quarter-budget interface.
3. uniform blind target \(G_{\rm blind}\).
4. \(d_f<105d/47\), \(d=186\)에서 \(19530/47<416<900\).
5. source hashes와 모든 OPEN status의 fail-closed ledger.

Lean은 prime-power removal scalar identity, flexible energy transfer,
quarter-budget terminal, exponent range와 source-range separation만 검사한다.
analytic character sums·variance theorem을 local axiom으로 넣지 않는다.

canonical Python 회귀시험 48개, Lean direct compile과 full build가 PASS했다.
전수 refresh·validation은 theory 문서 91개, display 식 1,763개, Lean declaration
329개, 금지 proof escape 0건이다. 상태는
<code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=102</code>,
<code>DEFINITION_ONLY=150</code>, <code>PARTIAL_FORMALIZATION=151</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=151</code>,
<code>NOT_YET_FORMALIZED=1106</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.

## 12. 다음 gate

다음 우선순위는 prescribed fixed-coordinate modulus \(f\)에 대한 native
character-energy upper 또는 식 (89.23)의 direct weighted correlation이다.

기존 checked full-variance source는 적용되지 않으므로, 다음 source audit은

1. \(f\)의 disconnected primorial-factor structure를 사용하는 theorem,
2. blind coefficient를 함께 넣은 weighted variance,
3. prime-specific explicit-formula cancellation

순으로 진행한다. numerical source multiplier와 common cutoff가 생기기 전에는
threshold calculator나 장시간 prime 계산을 시작하지 않는다.

## 13. 참고문헌

- R. C. Vaughan, *On a variance associated with the distribution of primes in
  arithmetic progressions*, Proc. LMS 82 (2001), 533--553,
  [doi:10.1112/plms/82.3.533](https://doi.org/10.1112/plms/82.3.533).
- J. B. Friedlander and D. A. Goldston,
  *Variance of distribution of primes in residue classes*, Q. J. Math. 47
  (1996), 313--336,
  [doi:10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
- M. A. Bennett, G. Martin, K. O'Bryant and A. Rechnitzer,
  *Explicit bounds for primes in arithmetic progressions*,
  [arXiv:1802.00085](https://arxiv.org/abs/1802.00085).
