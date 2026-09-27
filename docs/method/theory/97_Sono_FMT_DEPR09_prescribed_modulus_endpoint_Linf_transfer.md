# Theory 97 — DEP-R09 prescribed-modulus endpoint \(L^\infty\) transfer

- 상태:
  <code>VAUGHAN_HARPER_SOURCE_DAG_AUDITED /
  SINGLE_ENDPOINT_LINF_TRANSFER_EXACT /
  SMALL_SCALE_MULTIPLIER_21_OVER_5_EXPLICIT /
  NUMERICAL_CENTERED_ENDPOINT_PNT_OPEN</code>
- 선행 정본: Theory 47, 58--59, 90, 96, review 105
- 기계 원장:
  [prescribed-modulus endpoint Linf v1](data/Sono_FMT_DEPR09_prescribed_modulus_endpoint_linf_v1.json)
- 목표: Vaughan general-sequence I/II·Harper·Thorner--Zaman을 Theory 96 식
  (96.9)에 직접 매핑하고, mixed covariance theorem보다 약한 single-endpoint centered
  \(L^\infty\) 충분조건과 exact project multiplier를 고정한다.
- 비목적: one-sided PAP를 two-sided centered error로 바꾸거나, modulus-average theorem을
  prescribed \(f\) theorem으로 승격하거나, hidden source constant를 임의로 정하거나,
  actual 계산, threshold calculator, conditional branch, PAP-11, DEP-R09, numerical
  \(X_{\rm cert}\)를 닫는 것.

> **2026-09-28 successor:** [Theory 98](98_Sono_FMT_DEPR09_TZ_full_interval_centered_transfer.md)은
> actual \(B_0\)에서 relative zero-free constant \(47/2520\)을 얻고 full-interval
> \(\lambda=1\) branch와 centered factor 2를 고정했다. Numerical source
> \(K_{\rm TZ},c_{\rm TZ},U_{\rm TZ}\)는 계속 OPEN이다.

## 1. 결론

Theory 96의 residue error를 그대로 쓰고 large endpoint의 centered norm을

\[
 \boxed{
 \epsilon_\infty(U,f):=
 \frac{\varphi(f)}U
 \max_{a\bmod f}^{*}|E_f(U;a)|}
 \tag{97.1}
\]

로 둔다. Lower endpoint의 elementary correction은

\[
 \boxed{
 \epsilon_0(X,U,f):=
 \frac{\varphi(f)\log X+\vartheta_f(X)}U.}
 \tag{97.2}
\]

Current child에서 \(f>Y>X\)이므로 한 reduced residue에는 \(X\) 이하 prime이 많아야
하나다. Triangle inequality로

\[
 \frac{\varphi(f)}U
 \max_a^*|E_f(U;a)-E_f(X;a)|
 \le \epsilon_\infty(U,f)+\epsilon_0(X,U,f).
 \tag{97.3}
\]

한편 임의 \(t\)에서 nonnegative residue masses를 center하면 exact하게

\[
 \boxed{
 \sum_a^*|E_f(t;a)|\le2\vartheta_f(t).}
 \tag{97.4}
\]

따라서 Theory 96의 cross-covariance는

\[
 \boxed{
 |{\cal K}_f(t;X,U)|
 \le2\vartheta_f(t)U
 \{\epsilon_\infty(U,f)+\epsilon_0(X,U,f)\}.}
 \tag{97.5}
\]

Project child의 이미 증명된 조건을 느슨하게

\[
 B_0\le X,\quad f>Y\ge8X,\quad
 \log Y<2\log X,\quad \log X\ge30
 \tag{97.6}
\]

로 쓴다. \(Q'\)는 정확히 \((X,Y]\)의 primes이므로

\[
 N=\pi(Y)-\pi(X).
 \tag{97.7}
\]

Rosser--Schoenfeld Theorem 1과 식 (97.6)은

\[
 \boxed{N>\frac{Y}{2\log Y}}
 \tag{97.8}
\]

를 준다. 같은 prime-count upper에서 \(X\le t\le Y\)이면

\[
 \vartheta_f(t)\le\pi(t)\log t
 <t\left(1+\frac3{2\log t}\right)
 \le\frac{21}{20}t.
 \tag{97.9}
\]

또 \(t/\log t\)는 \(t>e\)에서 증가하므로

\[
 \boxed{
 \frac{\vartheta_f(t)}{N\log t}<\frac{21}{10}
 \qquad(X\le t\le Y).}
 \tag{97.10}
\]

식 (97.5)에 넣으면

\[
 \boxed{
 |{\cal K}_f(t;X,U)|
 <\frac{21}{5}
 \{\epsilon_\infty(U,f)+\epsilon_0(X,U,f)\}
 NU\log t.}
 \tag{97.11}
\]

즉 Theory 96 식 (96.9)의 충분한 선택은

\[
 \boxed{
 \kappa=\frac{21}{5}
 \{\epsilon_\infty(U,f)+\epsilon_0(X,U,f)\}.}
 \tag{97.12}
\]

이고, Abel transfer까지 합친 project gate는

\[
 \boxed{
 \delta_{\rm bin}
 \le\frac{21}{5}
 \{\epsilon_\infty(U,f)+\epsilon_0(X,U,f)\}
 \left(2+\frac ba\right).}
 \tag{97.13}
\]

이다. 따라서 mixed covariance theorem 자체는 이 **충분경로**에서 필요하지 않다.
남은 analytic root는 single large endpoint \(U\)에서의 fully numerical centered
fixed-\(f\) \(L^\infty\) bound다. 그 bound는 아직 OPEN이다.

## 2. Lower endpoint는 elementary correction이다

\(f>X\)라서 fixed reduced residue \(a\)에 \(X\) 이하 prime은 많아야 하나다. 따라서

\[
 |E_f(X;a)|
 \le\vartheta(X;f,a)+\frac{\vartheta_f(X)}{\varphi(f)}
 \le\log X+\frac{\vartheta_f(X)}{\varphi(f)}.
 \tag{97.14}
\]

Theory 90의 \(\varphi(f)\le f\le U^{1/21}\)과 식 (97.9)의 \(t=X\) 특수화는

\[
 \boxed{
 \epsilon_0(X,U,f)
 \le U^{-20/21}\log X+\frac{21X}{20U}.}
 \tag{97.15}
\]

를 준다. 이는 parameterized explicit하고 기존 \(U=f^{d_f}\), \(d_f\ge21\)에서
사라지는 correction이다. Final coefficient allocation 전이므로 이 식을 threshold로
계산하지 않는다.

## 3. \(L^1\times L^\infty\) transfer의 직접 증명

\(A_a:=\vartheta(t;f,a)\ge0\),
\(\mu:=\vartheta_f(t)/\varphi(f)\)라 두면

\[
 \sum_a^*|A_a-\mu|
 \le\sum_a^*(A_a+\mu)
 =2\vartheta_f(t).
 \tag{97.16}
\]

Theory 96 식 (96.8)에 triangle inequality를 한 번 적용하고 식 (97.3), (97.16)을
대입하면 식 (97.5)가 나온다. Character별 absolute value나 separate character
\(L^2\)를 쓰지 않으므로 Theory 95의 \(\varphi(f)/N\) dimension loss는 생기지 않는다.
반면 large endpoint에서 residue별 maximum을 지불하므로 이 route는 pointwise PNT
상수를 그대로 보존한다.

## 4. Small-scale \(21/10\) normalization

Rosser--Schoenfeld printed p.69 Theorem 1은 이 project가 Theory 47에서 이미 채택한

\[
 \pi(s)>\frac{s}{\log s}\left(1+\frac1{2\log s}\right)
 \quad(s\ge59),\qquad
 \pi(s)<\frac{s}{\log s}\left(1+\frac3{2\log s}\right)
 \quad(s>1)
 \tag{97.17}
\]

을 준다. 따라서 \(\pi(Y)>Y/\log Y\), \(\pi(X)<2X/\log X\)다. 식 (97.6)에서

\[
 \frac{2X}{\log X}
 \le\frac{Y}{2\log Y}
 \tag{97.18}
\]

이므로 식 (97.8)이 따른다. 식 (97.9)는 \(\vartheta_f(t)\le\pi(t)\log t\)와
\(3/(2\log t)\le1/20\)의 합성이다. 외부 theta theorem을 새로 요구하지 않는다.

상수 \(21/10\)은 최적화한 값이 아니다. 목적은 pointwise endpoint error가 whole binary
core로 전달될 때 생기는 정확하고 작은 universal multiplier를 고정하는 것이다.

## 5. Vaughan general-sequence I·II 적용성

### 5.1 Vaughan 1998 I

Vaughan I의 기본 가정 식 (1.6)은 모든 real \(x\ge1\), natural \(q,a\)에 uniformly

\[
 A(x;q,a)=E(q,a)\frac{\Phi(x)}{\varphi(q)}
 +O\!\left(\frac{\Phi(x)}{\Psi(x)}\right)
 \tag{97.19}
\]

이다. Theorem 1은 이 가정과 \(\log x\le\Psi(x)\le x^{1/2}\) 아래

\[
 x^{2/3}\le Q\le x
 \tag{97.20}
\]

에서 \(\sum_{q\le Q}\sum_a|\cdots|^2\)의 asymptotic을 준다.

Current length \(x=U\), prescribed modulus \(Q=f=U^{1/d_f}\), \(d_f\ge21\)를 넣으면
식 (97.20)의 lower range와 겹치지 않는다. \(Q\ge U^{2/3}\)로 키우면 \(f\) 항을
누적합에 포함시킬 수는 있지만 aggregate main/error scale을 지불하고 fixed-\(f\)
cancellation을 보존하지 못한다. 더 근본적으로 prime-weighted current sequence에 식
(97.19)를 유용한 \(\Psi\)로 확인하는 일은 현재 필요한 pointwise progression error를
선행가정으로 다시 요구한다. 따라서 drop-in이 아니다.

### 5.2 Vaughan 1998 II

Vaughan II는 모든 \(x,q,a\)의 uniform 가정

\[
 A(x;q,a)=xf(q,(q,a))+O\!\left(\frac{x}{\Psi(x)}\right),
 \qquad \sum_{n\le x}a_n^2\ll x
 \tag{97.21}
\]

뒤 Theorems 1--2에서

\[
 Q>\sqrt{x}\log(2x)
 \tag{97.22}
\]

인 cumulative modulus variance를 다룬다. 역시 \(Q=f\)는 범위 밖이고, 식 (97.21)의
first condition은 target prime sequence에 대해 현재 endpoint PNT root를 우회하지 않는다.
Theta weight를 그대로 쓰면 mean-square normalization도 별도 검증이 필요하다.

두 PDF는 Vaughan 공식 저자 페이지에서 확보했다. 각각 12쪽·18쪽이고 SHA-256은

~~~text
250d417a0f832d551aa52ef6c8d36dd4ab9a7db42798bd83587c31af670f2050
4e6eb755dcf5a8e67f698770169a8f81c2571f54b54645ff950c1a5296f3f015
~~~

이다. 두 논문은 2001 prime-specific variance와 구분되는 1998년 I·II다.

## 6. Harper 2024 적용성

Harper는 finite complex sequence를 허용하므로 sequence class 자체는 Vaughan보다
유연하다. 그러나 Theorems 1--2의 variance는

\[
 V({\cal A},x,Q)=
 \sum_{Q/2<q\le Q}\sum_{a=1}^q
 |A(x;q,a)-\operatorname{Aver}({\cal A},x;q,(a,q))|^2,
 \qquad \sqrt{2x}<Q\le x.
 \tag{97.23}
\]

이다. \(x=U\), \(f\le U^{1/21}\), existing \(U>e^{20}\)에서는 allowed dyadic
block의 lower endpoint \(Q/2\)도 \(f\)보다 크다. 따라서 theorem의 sum에 prescribed
\(f\)가 들어가지 않는다. Progressions·Non-concentration와 추가 hereditary
sparsity/integer-resemblance hypotheses를 검증하더라도 이 quantifier mismatch는 남는다.

판정은 <code>GENERAL_SEQUENCE_RELEVANT / CURRENT_FIXED_MODULUS_NOT_INCLUDED</code>다.

## 7. Thorner--Zaman을 새 interface에 매핑

Thorner--Zaman Theorem 1.1은 pointwise prime sum을 다루므로 식 (97.1)에 구조적으로
가장 가깝다. 하지만 현재 필요한 것은 common main term에 대한 absolute centered error다.
Possible exceptional zero가 있을 때 source의 \(\lambda(x,q,a,h)\)는 residue \(a\)에
의존하는 secondary main term을 포함한다. 따라서 다음을 모두 보존해야 한다.

1. actual \(B_0\) 제외가 modulus \(f\)의 exceptional contribution을 제거하는 정확한 lemma,
2. \(O_\varepsilon\) multiplier와 \(c_1(\varepsilon)\)의 actual 숫자,
3. prime-power/endpoint와 centered total의 오차,
4. 모든 residue와 필요한 \(U\)에 공통인 finite cutoff.

Theory 59의 fixed-exponent 진단처럼 source error가 조건부로

\[
 \epsilon_\infty(U,f)
 \le K\exp(-c d_f)+R(U,f)
 \tag{97.24}
\]

꼴이라면 식 (97.13)은 \(K\)를 \(21/5\)배 선형으로 보존한다. \(d_f\)가 fixed range
\([21,416)\)이므로 unknown \(K\exp(-cd_f)\)는 \(U\)를 키우는 것만으로 사라지지 않는다.
즉 이번 aggregation은 required source를 한 endpoint로 줄였지만 hidden numerical
constant 문제를 제거하지 않는다.

또 PAP-11의 one-sided lower bound만으로 식 (97.1)의 absolute centered norm은 나오지
않는다. Montgomery--Vaughan Brun--Titchmarsh upper는 explicit envelope를 주지만 main
term의 두 배 규모라 \(\epsilon_\infty=o(1)\)를 인증하지 않는다.

## 8. source/DAG 판정표

| source 또는 edge | 정확한 판정 |
|---|---|
| Vaughan 1998 I | Criterion-U + \(q\le Q\), \(Q\ge U^{2/3}\); no fixed-\(f\) drop-in |
| Vaughan 1998 II | Criterion-U + cumulative \(Q>\sqrt U\log(2U)\); no fixed-\(f\) drop-in |
| Harper 2024 | complex sequence 허용, but dyadic block \(Q/2<q\le Q\) excludes current \(f\) |
| Thorner--Zaman | pointwise structural candidate; numerical centered endpoint package OPEN |
| centered \(L^1\) bound | <code>EXACT</code> |
| lower endpoint correction | <code>PARAMETERIZED EXPLICIT</code> |
| small-scale ratio \(21/10\) | <code>EXPLICIT SOURCE-BACKED</code> |
| cross multiplier \(21/5\) | <code>EXACT SUFFICIENT TRANSFER</code> |
| \(\epsilon_\infty(U,f)\) numerical upper | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 9. 검증 범위

<code>source/dep_r09_prescribed_modulus_endpoint_linf.py</code>와 tests는 centered finite
vector의 \(L^1\) bound, \(L^1\times L^\infty\) cross envelope, prime-count half-scale
algebra, \(21/10\), \(21/5\), project multiplier의 exact rational fixture를 검사한다.
Actual prime list나 \(\pi(X),\pi(Y)\)를 계산하지 않는다.

Lean은 Rosser--Schoenfeld나 PNT-in-AP를 local axiom으로 넣지 않고, endpoint triangle,
normalized \(21/5\) transfer와 Abel project composition의 scalar terminal만 검사한다.

## 10. 다음 gate

다음 최소 analytic lemma는

\[
 \boxed{
 \frac{\varphi(f)}U
 \max_{a\bmod f}^{*}
 \left|\vartheta(U;f,a)-\frac{\vartheta_f(U)}{\varphi(f)}\right|
 \le\epsilon_{\rm EP}(X)}
 \tag{97.25}
\]

의 fully numerical version이다. \(\epsilon_{\rm EP}\)를 식 (97.13)의 actual success
budget보다 작게 만들고, exceptional removal·prime powers·common cutoff를 함께 줘야 한다.

권장 순서는 다음이다.

1. Thorner--Zaman Theorem 2.3 proof에서 centered full-interval \(h=U\)에 불필요한
   short-interval loss를 제거할 수 있는지 감사한다.
2. Explicit formula를 character별이 아니라 residue-centered endpoint norm으로 합성해
   필요한 density multiplier interface를 고정한다.
3. 숫자 \(K,c,U_0\)가 생긴 뒤에만 식 (97.13)에 대입한다.

## 11. 참고문헌

- R. C. Vaughan, [*On a variance associated with the distribution of general
  sequences in arithmetic progressions I*](https://personal.science.psu.edu/rcv4/personal/Publications/VRSQAP.pdf),
  *Phil. Trans. Royal Soc. Lond. A* 356 (1998), 781--791.
- R. C. Vaughan, [*On a variance associated with the distribution of general
  sequences in arithmetic progressions II*](https://personal.science.psu.edu/rcv4/personal/Publications/VRSQAPT.pdf),
  *Phil. Trans. Royal Soc. Lond. A* 356 (1998), 793--809.
- A. J. Harper, [*Simple Barban--Davenport--Halberstam type asymptotics for
  general sequences*](https://arxiv.org/abs/2412.19644), arXiv:2412.19644v1.
- J. Thorner and A. Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878),
  Theorems 1.1, 2.1, 2.3.
- J. B. Rosser and L. Schoenfeld,
  [*Approximate Formulas for Some Functions of Prime Numbers*](https://doi.org/10.1215/ijm/1255631807),
  *Illinois J. Math.* 6 (1962), 64--94.
