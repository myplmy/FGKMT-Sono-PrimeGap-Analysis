# Theory 96 — DEP-R09 cross-scale covariance·Abel interface

- 상태:
  <code>ABEL_INTERFACE_EXACT /
  RESIDUE_CROSS_COVARIANCE_EXACT /
  PROJECT_TRANSFER_MULTIPLIER_EXPLICIT /
  MIXED_COVARIANCE_SOURCE_OPEN</code>
- 선행 정본: Theory 37, 59, 85, 95, review 104
- 기계 원장:
  [cross-scale covariance v1](data/Sono_FMT_DEPR09_cross_scale_covariance_v1.json)
- 목표: Theory 95의 unweighted small-prime coefficient를 endpoint-safe Abel identity로
  변환하고, weighted character product를 fixed-modulus two-scale residue covariance로
  exact 환원해 필요한 theorem의 norm과 multiplier를 고정한다.
- 비목적: separate variance upper를 mixed cancellation으로 승격하거나, modulus-average
  asymptotic을 prescribed \(f\) theorem으로 바꾸거나, actual 계산, threshold calculator,
  conditional branch, PAP-11, DEP-R09, numerical \(X_{\rm cert}\)를 닫는 것.

## 1. 결론

Prime-supported character theta sum을

\[
 \Theta_\chi(t):=
 \sum_{\substack{p\le t\\p\ \mathrm{prime}}}(\log p)\chi(p)
 \tag{96.1}
\]

로 둔다. Active \(B_0\le X\)이므로 \(Q'\)는 정확히 \((X,Y]\)의 primes이고

\[
 C_\chi(Q')=
 \sum_{X<q\le Y}\overline{\chi(q)}.
 \tag{96.2}
\]

Stieltjes/Abel summation은 endpoint와 plus sign을 보존해

\[
 \boxed{
 C_\chi(Q')
 =\frac{\Theta_{\bar\chi}(Y)}{\log Y}
 -\frac{\Theta_{\bar\chi}(X)}{\log X}
 +\int_X^Y
 \frac{\Theta_{\bar\chi}(t)}{t(\log t)^2}\,dt.}
 \tag{96.3}
\]

Theory 95의 large-prime error는

\[
 Z_\chi(X,U)=\Theta_\chi(U)-\Theta_\chi(X).
 \tag{96.4}
\]

Two-scale character covariance를

\[
 {\cal K}_f(t;X,U):=
 \sum_{\substack{\chi\bmod f\\\chi\ne\chi_0}}
 \Theta_{\bar\chi}(t)Z_\chi(X,U)
 \tag{96.5}
\]

로 두면 finite sum/integral 교환으로

\[
 \boxed{
 {\cal C}_f
 =\frac{{\cal K}_f(Y;X,U)}{\log Y}
 -\frac{{\cal K}_f(X;X,U)}{\log X}
 +\int_X^Y
 \frac{{\cal K}_f(t;X,U)}{t(\log t)^2}\,dt.}
 \tag{96.6}
\]

Reduced-residue prime error를

\[
 E_f(t;a):=
 \vartheta(t;f,a)-\frac{\vartheta_f(t)}{\varphi(f)},
 \qquad
 \vartheta_f(t):=
 \sum_{\substack{p\le t\\p\nmid f}}\log p
 \tag{96.7}
\]

로 두면 character orthogonality는 exact하게

\[
 \boxed{
 {\cal K}_f(t;X,U)
 =\varphi(f)
 \sum_{a\bmod f}^{*}
 E_f(t;a)\{E_f(U;a)-E_f(X;a)\}.}
 \tag{96.8}
\]

즉 필요한 object는 small scale \(t\in[X,Y]\)와 large interval \((X,U]\)의
fixed-modulus **cross-covariance**다.

다음 uniform input을 가정하자.

\[
 \boxed{
 |{\cal K}_f(t;X,U)|
 \le\kappa NU\log t
 \qquad(X\le t\le Y).}
 \tag{96.9}
\]

식 (96.6)에 넣으면

\[
 \boxed{
 \frac{|{\cal C}_f|}{NU}
 \le\kappa
 \left\{2+\log\frac{\log Y}{\log X}\right\}.}
 \tag{96.10}
\]

Project notation \(a=\log X\), \(b=\log a\)와 \(Y<Xa\)에서

\[
 \log Y<a+b,qquad
 \log\frac{\log Y}{\log X}
 <\log\left(1+\frac ba\right)
 \le\frac ba.
 \tag{96.11}
\]

따라서 최종 project transfer는

\[
 \boxed{
 \delta_{\rm bin}
 \le\kappa\left(2+\frac ba\right).}
 \tag{96.12}
\]

이다. 새 analytic theorem이 충족해야 할 norm과 multiplier는 이제 exact하다.
Checked source에는 식 (96.9)의 unconditional fully numerical prescribed-primorial
version이 없다.

## 2. endpoint-safe Abel identity

함수 \(g(t)=1/\log t\)는

\[
 g'(t)=-\frac1{t(\log t)^2}.
 \tag{96.13}
\]

Prime measure \(d\Theta_{\bar\chi}\)에 Stieltjes integration by parts를 적용하면

\[
 \int_{(X,Y]}g(t)\,d\Theta_{\bar\chi}(t)
 =g(Y)\Theta_{\bar\chi}(Y)-g(X)\Theta_{\bar\chi}(X)
 -\int_X^Yg'(t)\Theta_{\bar\chi}(t)\,dt.
 \tag{96.14}
\]

왼쪽 jump at prime \(q\)는
\((\log q)\overline{\chi(q)}/\log q=\overline{\chi(q)}\)다. 식 (96.13)을
대입하면 식 (96.3)이 나온다. Lower endpoint \(X\)는 제외되고 upper \(Y\)는 포함된다.
Theory 37에서 확인한 Abel plus-sign convention과 일치한다.

## 3. character에서 residue covariance로

Character inversion은

\[
 E_f(t;a)
 =\frac1{\varphi(f)}
 \sum_{\substack{\chi\bmod f\\\chi\ne\chi_0}}
 \overline{\chi(a)}\Theta_\chi(t).
 \tag{96.15}
\]

를 준다. 두 real residue-error vectors의 product를 \(a\)에서 합하면

\[
 \begin{aligned}
 \varphi(f)\sum_a^*E_f(t;a)
 \{E_f(U;a)-E_f(X;a)\}
 &={1\over\varphi(f)}
 \sum_{\chi,\psi\ne\chi_0}
 \Theta_\chi(t)Z_\psi(X,U)
 \sum_a^*\overline{\chi(a)\psi(a)}\\
 &=\sum_{\chi\ne\chi_0}
 \Theta_{\bar\chi}(t)Z_\chi(X,U).
 \end{aligned}
 \tag{96.16}
\]

따라서 식 (96.8)이 exact하다. Complex character terms를 개별 absolute value로
바꾸지 않았고 conjugate orientation도 보존했다.

## 4. polarization이 주는 것과 주지 않는 것

Residue vector norm을

\[
 \|E\|_f^2:=\varphi(f)\sum_a^*E(a)^2
 \tag{96.17}
\]

로 두면

\[
 \boxed{
 2{\cal K}_f(t;X,U)
 =\|E_t+E_{(X,U]}\|_f^2
 -\|E_t\|_f^2
 -\|E_{(X,U]}\|_f^2.}
 \tag{96.18}
\]

이는 mixed covariance를 combined signed sequence의 variance로 바꾸는 exact
interface다. 그러나 세 variance에 upper bounds만 각각 적용하면 cancellation이
사라지고 Theory 95의 separate-L2 architecture로 돌아간다. 필요한 source는 combined
sequence variance의 main term과 error를 같은 fixed \(f\)에서 함께 제어해야 한다.

## 5. Abel transfer multiplier

식 (96.9)에서 두 endpoint는 각각 \(\kappa NU\) 이하이다. Integral은

\[
 \int_X^Y\frac{\kappa NU\log t}{t(\log t)^2}\,dt
 =\kappa NU\log\frac{\log Y}{\log X}.
 \tag{96.19}
\]

따라서 식 (96.10)이 나온다. \(\log(1+u)\le u\) for \(u\ge0\)를 쓰면
식 (96.11)--(96.12)다. Existing child에서 \(b/a\)는 매우 작지만 final coefficient
allocation 전이므로 numerical cutoff를 계산하지 않는다.

## 6. source applicability

### Vaughan 2001

Vaughan의 object는 한 scale의 residue variance를 dyadic **modulus average**로 다룬다.
Theory 85의 exact energy bridge는 재사용할 수 있지만, source statement는 prescribed
\(f\)의 mixed \((t,U)\) covariance나 combined signed sequence variance를 주지 않는다.
또 current modulus power range와 source main theorem range가 맞지 않고 multiplier·finite
cutoff가 implicit하다.

### Harper 2024

새로 확인한 Adam J. Harper,
*Simple Barban--Davenport--Halberstam type asymptotics for general sequences*,
arXiv:2412.19644v1은 23 pages이고 local SHA-256은

~~~text
be7c989b3a3626ba1d956a65a8eb2235be1097ba891a88ebed0ea7dea16d1c04
~~~

다. 이 source는 general complex sequence의 variance를
\(Q/2<q\le Q\)에서 합하고, 핵심 regime도 \(Q\)가 square-root scale 이상인 modulus
average다. 식 (96.18)의 combined sequence 아이디어에는 관련 있지만 prescribed
primorial \(f=U^{1/d_f}\) 한 개의 fully numerical theorem은 아니다.

### Thorner--Zaman

Uniform pointwise PNT-in-AP가 각 \(E_f(t;a)\), \(E_f(U;a)-E_f(X;a)\)를 충분히
작게 주면 식 (96.8)을 닫을 수 있다. 그러나 Theory 59·58의 source audit에서
decay multiplier와 common finite cutoff가 unnamed로 남았다. Abel interface는 그
missing constants를 제거하지 않는다.

## 7. 상태표

| 항목 | 판정 |
|---|---|
| small-prime Abel identity | <code>EXACT</code> |
| character cross-covariance | <code>EXACT</code> |
| residue cross-covariance | <code>EXACT</code> |
| polarization interface | <code>EXACT</code> |
| project transfer multiplier | <code>\(2+b/a\) EXPLICIT</code> |
| Vaughan mixed fixed-modulus source | <code>NO</code> |
| Harper prescribed fixed-modulus source | <code>NO</code> |
| Thorner--Zaman numerical cutoff | <code>OPEN</code> |
| cross-scale covariance gate | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 8. 검증 범위

<code>source/dep_r09_cross_scale_covariance.py</code>와 tests는 finite Abel summation,
modulo-5 Gaussian-rational character/residue cross identity, real polarization과 abstract
transfer multiplier를 exact하게 검사한다. Actual prime sums나 numerical integration은
하지 않는다.

Lean은 Abel/source theorem을 local axiom으로 넣지 않고 endpoint coefficient 합성,
polarization과 project transfer scalar terminal만 검사한다.

## 9. 다음 gate

다음 최소 gate는 식 (96.9)의 fully numerical bound다. Source-first 순서는

1. Vaughan general-sequence variance I/II의 mixed polarization 적용 가능성,
2. Harper hypotheses를 current combined signed prime sequence에 대입할 수 있는지,
3. Thorner--Zaman pointwise proof에서 aggregation으로 절약 가능한 multiplier가 있는지

다. 모두 실패하면 식 (96.9)을 project lemma statement로 고정하고 direct dispersion
proof를 시작한다.

## 10. 참고문헌

- R. C. Vaughan, *On a variance associated with the distribution of primes in
  arithmetic progressions*, Proc. LMS 82 (2001), 533--553.
- A. J. Harper, *Simple Barban--Davenport--Halberstam type asymptotics for
  general sequences*, [arXiv:2412.19644](https://arxiv.org/abs/2412.19644).
- J. Thorner and A. Zaman, *Refinements to the prime number theorem for
  arithmetic progressions*, [arXiv:2108.10878](https://arxiv.org/abs/2108.10878).
