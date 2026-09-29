# Theory 101 — DEP-R09 pre-sup joint-angle source audit

- 상태:
  <code>PRE_SUP_ZERO_PACKET_INTERFACE_EXACT /
  PHASE_BLIND_CERTIFICATE_SHARPNESS_EXACT /
  JOINT_ANGLE_BUDGET_EXPLICIT /
  NUMERICAL_PRESCRIBED_F_SOURCE_NOT_IDENTIFIED</code>
- 선행 정본: Theory 75--77, 89, 95--96, 100, review 109
- 기계 원장:
  [pre-sup joint-angle v1](data/Sono_FMT_DEPR09_presup_joint_angle_v1.json)
- 목표: explicit formula에서 characterwise absolute value와 density sup를 취하기 전의
  signed target을 고정하고, recent weighted-sieve·dispersion·prime-character theorem이
  actual coefficient/error vectors의 joint angle을 제어하는지 판정한다.
- 비목적: abstract phase-alignment witness를 actual zeros의 정렬이라고 주장하거나,
  checked source 밖의 모든 correlation theorem을 배제하거나, actual 계산, threshold
  calculator, construction redesign, PAP-11, DEP-R09, numerical \(X_{\rm cert}\)를 닫는 것.

## 1. 결론

Theory 95의 small-prime coefficient와 large-prime packet을

\[
 C_\chi(Q'):=\sum_{q\in Q'}\overline{\chi(q)},
 \qquad
 Z_\chi(X,U):=sum_{X<p\le U}(\log p)\chi(p)
 \tag{101.1}
\]

로 둔다. Current centered binary-prime core는 exact하게

\[
 \boxed{
 {\cal C}_f=
 \sum_{\substack{\chi\bmod f\\\chi\ne\chi_0}}
 C_\chi(Q')Z_\chi(X,U).}
 \tag{101.2}
\]

Truncation height \(T\)에서 nonexceptional zero packet을

\[
 \mathfrak Z_\chi(X,U;T):=
 \sideset{}{'}\sum_{\substack{\rho_\chi=\beta+i\gamma\\|\gamma|\le T}}
 \frac{U^{\rho_\chi}-X^{\rho_\chi}}{\rho_\chi}
 \tag{101.3}
\]

라 한다. Prime-power, principal/exceptional normalization, low-zero convention과
truncation error를 \(\mathfrak R_\chi\)에 모으면 explicit formula의 필요한 interface는

\[
 Z_\chi(X,U)=-\mathfrak Z_\chi(X,U;T)+\mathfrak R_\chi(X,U;T).
 \tag{101.4}
\]

따라서

\[
 \boxed{
 {\cal C}_f=-{\cal Z}_{f,T}+{\cal R}_{f,T},}
 \tag{101.5}
\]

\[
 {\cal Z}_{f,T}:=
 \sum_{\chi\ne\chi_0}C_\chi(Q')\mathfrak Z_\chi(X,U;T),
 \qquad
 {\cal R}_{f,T}:=
 \sum_{\chi\ne\chi_0}C_\chi(Q')\mathfrak R_\chi(X,U;T).
 \tag{101.6}
\]

다. 필요한 pre-sup analytic theorem은 \({\cal Z}_{f,T}\)를 **signed sum 그대로**
제어하고 \({\cal R}_{f,T}\)를 separately explicit하게 흡수하는 것이다.

Checked source가 주는 support, individual magnitudes 또는 separate \(L^2\) norms만으로는
이 signed cancellation을 보증할 수 없다. Abstract finite vectors에서

\[
 |\mathfrak Z_\chi|\le M_\chi
 \quad\Longrightarrow\quad
 \left|\sum_\chi C_\chi\mathfrak Z_\chi\right|
 \le\sum_\chi|C_\chi|M_\chi
 \tag{101.7}
\]

이고, arbitrary phases를 허용하는 이 premise class에서 equality가 가능하다.

\[
 \boxed{
 \mathfrak Z_\chi=
 \begin{cases}
 M_\chi\overline{C_\chi}/|C_\chi|,&C_\chi\ne0,\\
 0,&C_\chi=0
 \end{cases}
 \quad\Longrightarrow\quad
 \sum_\chi C_\chi\mathfrak Z_\chi
 =\sum_\chi|C_\chi|M_\chi.}
 \tag{101.8}
\]

이 witness는 actual zero packets가 이렇게 정렬된다는 주장이 아니다. Magnitudes에만
의존하고 independent phase rotations에 불변인 assumptions로는 더 작은 universal
correlation constant를 논리적으로 얻을 수 없다는 뜻이다.

따라서 새로운 theorem이 제어해야 할 object는 norms가 아니라 actual joint angle이다.

## 2. Joint angle의 exact budget

Finite character vectors에

\[
 A_C:=\sum_{\chi\ne\chi_0}|C_\chi|^2,qquad
 A_Z:=\sum_{\chi\ne\chi_0}|Z_\chi|^2
 \tag{101.9}
\]

와

\[
 \Gamma_f:=
 \frac{|\sum_{\chi\ne\chi_0}C_\chi Z_\chi|}
 {\sqrt{A_C A_Z}}
 \quad(A_CA_Z>0)
 \tag{101.10}
\]

를 정의하면 Cauchy--Schwarz로

\[
 0\le\Gamma_f\le1.
 \tag{101.11}
\]

Theory 95의 exact coefficient energy는

\[
 A_C=N\{\varphi(f)-N\}.
 \tag{101.12}
\]

가장 낙관적인 separate prime-error input \(A_Z\le U^2\)를 **조건부 진단**으로만
넣으면

\[
 \boxed{
 \frac{|{\cal C}_f|}{NU}
 \le\Gamma_f\sqrt{\frac{\varphi(f)-N}{N}}.}
 \tag{101.13}
\]

따라서 target \(\delta_{\rm bin}\)을 위해 필요한 angle budget은

\[
 \boxed{
 \Gamma_f^2<
 \delta_{\rm bin}^2\frac{N}{\varphi(f)-N}.}
 \tag{101.14}
\]

이다. 예시 \(\delta_{\rm bin}=1/100,N=3,\varphi(f)=30\)에서도

\[
 \Gamma_f^2<\frac1{90000}.
 \tag{101.15}
\]

즉 “약간의 decorrelation”이 아니라 growing \(\varphi(f)/N\) loss를 상쇄하는 매우
강한 joint-angle theorem이 필요하다. 실제 project budget은 이 예시가 아니며 final
success allocation 전이므로 숫자 threshold로 사용하지 않는다.

## 3. Phase-blind premise가 target을 결정하지 못하는 finite witness

두 coefficient가 \((1,1)\)이고 packet magnitudes가 모두 1인 경우를 보자. Aligned packets와
cancelling packets는 각각

\[
 z^+=(1,1),\qquad z^-=(1,-1).
 \tag{101.16}
\]

로 같은 magnitude profile과 같은 \(L^2\) energy를 갖지만

\[
 \langle(1,1),z^+\rangle=2,
 \qquad
 \langle(1,1),z^-\rangle=0.
 \tag{101.17}
\]

이다. Support-only·magnitude-only theorem은 두 input을 구별하지 않는다. 반면 current
target은 바로 이 차이를 구별해야 한다.

Theory 77의 aligned-vector Cauchy equality는 \(L^2\) version의 같은 경계다. 이번
phase witness는 zero-packet별 \(L^\infty\)/\(L^1\) envelope에도 같은 문제가 있음을
분리한다.

## 4. Ramaré 2026 weighted large sieve 두 편

### 4.1 *The weighted large sieve through Parseval*

2026-09-23 arXiv v1의 main theorem은 local support sets와 sequence \(u_n\)의
\(L^2\) norm으로 \(|\sum u_n|\)를 제어한다. Source는 complex values도 허용할 수 있다고
말하지만, 바로 앞에서 \((|u_n|)\)에 theorem을 적용하는 방식으로 nonnegativity를
제거한다. 따라서 coefficient phases와 두 독립 character vectors의 angle을 보존하지 않는다.

Current prime sequence에 적용하면 \(u_p=(\log p)H_Q(p)\)의 support-only sieve upper가
되며 RHS는 \(\sum|u_p|^2\)에만 의존한다. 이는 Theory 95의 separate-energy architecture를
바꿀 direct \(C_\chi Z_\chi\) theorem이 아니다.

PDF는 28쪽이고 SHA-256은

~~~text
62b6972d6341b0e29d181c5c8804729c891fc88fbbf72509744c99ac8a260deb
~~~

이다. Official source archive SHA-256은

~~~text
ad31124b36165aacaa8d21dd40bfc409fbbf3ab853ef872561fe5b649b1079c2
~~~

다.

### 4.2 *The large sieve through Parseval, Large sifted sets are regular*

Companion preprint는 sieve upper에 가까운 큰 set이면 attached **additive** Fourier
polynomial \(S(\beta)=\sum u_ne(n\beta)\)가 origin 근방에서 regular하다는 conditional
result를 준다. AP corollary도 prime count가 near Brun--Titchmarsh saturation lower를
만족한다고 먼저 가정한다.

Current target은 모든 relevant multiplicative characters의 \(C_\chi Z_\chi\) joint
angle이다. Additive frequencies near \(0\)만으로 full multiplicative Gauss expansion을
제어하는 bridge는 source에 없다. Required prime-count lower도 current centered endpoint
gate에서 이미 얻어야 할 정보보다 약한 것으로 확인되지 않았다.

PDF는 24쪽이고 SHA-256은

~~~text
0a862acd884b98495aaedf0ff4c9da16e2f3c22ea5d79071cbd0b08a49664925
~~~

이다. 두 원문은 2026-09-29 현재 recent preprint이며 peer-review 완료를 가정하지 않는다.

## 5. Motohashi·Zheng·Szabó source 적용성

### Motohashi 2012

Motohashi 식 (1.2), (1.6)은 auxiliary moduli \(q\le Q\)와 primitive characters에서

\[
 \sum_{q\le Q}\sum_{\chi\bmod q}^{*}
 \left|\sum_{p\le x,\ p\equiv\ell\bmod k}\chi(p)\right|^2
 \tag{101.18}
\]

을 제어한다. 식 (2.5)는 \(|\widetilde\psi(x,\chi)|\)의 auxiliary-modulus \(L^1\)다.
둘 다 prescribed \(f\)에서 \(C_\chi(Q')\)를 weight로 가진 signed product가 아니다.
또 theorem의 \(\omega\), \(o(1)\), starting point는 numerical하게 인쇄되지 않았다.

### Zheng 2025

Zheng Theorem 1.1은 fixed residues \(a_1\ne a_2\)에 대해 \(q\sim x^\theta\)와
well-factorable \(d\)를 함께 평균하는 signed mean-value theorem이다.

\[
 \sum_{q,d}\gamma_q\lambda_d
 \left\{\pi(x;dq,a_{q,d})-\frac{\pi(x)}{\varphi(qd)}\right\}
 \ll_A\frac{x}{(\log x)^A}.
 \tag{101.19}
\]

Current \(Q'\)의 prime은 varying **residue**, prescribed \(f\)는 하나의 modulus다.
Source의 fixed two residues와 well-factorable modulus average에서 delta mass at the actual
growing primorial, variable prime-residue mask와 numerical constant를 얻는 statement는 없다.

### Szabó 2024 / Heath--Brown lemma

Szabó Proposition 6은 bounded order인 한 nonprincipal character에 smoothed prime sum의
real part upper를 준다.

\[
 \Re\sum_p\frac{\chi(p)\log p}{p}
 f\left(\frac{\log p}{\log q}\right)
 \le\left(\frac\alpha8+o(1)\right)\log q.
 \tag{101.20}
\]

Current conductor family는 unbounded character orders를 포함하고, 필요한 것은 모든
characters의 \(C_\chi\)-weighted simultaneous complex sum이다. Source의 \(o(1)\)과 cutoff도
numerical하지 않으므로 drop-in이 아니다.

## 6. 상태표

| 항목 | 판정 |
|---|---|
| pre-sup zero-packet target | <code>EXACT INTERFACE</code> |
| phase-blind triangle sharpness | <code>EXACT FINITE WITNESS</code> |
| separate-L2 angle budget | <code>EXPLICIT CONDITIONAL TERMINAL</code> |
| Ramaré support-only weighted sieve | <code>NO JOINT ANGLE</code> |
| Ramaré additive regularity | <code>OBJECT·ASSUMPTION MISMATCH</code> |
| Motohashi character moment | <code>AUXILIARY-MODULUS NORM, NOT JOINT PRODUCT</code> |
| Zheng simultaneous AP | <code>MODULUS-AVERAGE / QUANTIFIER MISMATCH</code> |
| Szabó bounded-order real part | <code>ORDER·SIMULTANEITY·NUMERICAL MISMATCH</code> |
| numerical prescribed-\(f\) joint theorem | <code>NOT IDENTIFIED</code> |
| Theory 98 endpoint gate | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| calculator·actual prime/zero 계산 | <code>NOT READY / NOT RUN</code> |

## 7. 검증 범위

<code>source/dep_r09_presup_joint_angle_audit.py</code>와 tests는 finite real subspace에서
phase-alignment equality, same-magnitude cancellation, squared angle과 exact budget
fixture를 검사한다. Real subspace witness만으로 phase-blind complex premise class의
universal improvement가 불가능함을 보이기에 충분하다.

Lean은 external source theorem이나 explicit formula를 local axiom으로 넣지 않고 finite
alignment, Cauchy angle normalization과 required budget scalar terminal만 검사한다.

## 8. 다음 gate

다음 최소 gate는 식 (101.5)--(101.6)의 direct signed zero-packet theorem이다.

1. Thorner--Zaman full-interval explicit formula에서 characterwise absolute value 이전
   finite truncation을 fixed \(f\)에 맞춰 다시 쓴다.
2. \(C_\chi(Q')\)를 zero sum 안에 보존한 weighted zero-density/dispersion lemma를 찾거나
   정확한 project lemma statement로 고정한다.
3. Support-only 또는 separate norms로 되돌아가는 proof는 식 (101.8)의 barrier를 먼저
   통과해야 한다.

New detector/weight construction 구현은 별도 승인 전 하지 않는다.

## 9. 참고문헌

- O. Ramaré,
  [*The weighted large sieve through Parseval*](https://arxiv.org/abs/2609.25885),
  arXiv:2609.25885v1.
- O. Ramaré,
  [*The large sieve through Parseval, Large sifted sets are regular*](https://arxiv.org/abs/2609.25879),
  arXiv:2609.25879v1.
- Y. Motohashi,
  [*On Some Improvements of the Brun--Titchmarsh Theorem IV*](https://arxiv.org/abs/1201.3134).
- Z. Zheng,
  [*Primes in simultaneous arithmetic progressions*](https://arxiv.org/abs/2512.22798).
- B. Szabó,
  [*On the existence of products of primes in arithmetic progressions*](https://arxiv.org/abs/2208.05762),
  DOI [10.1112/blms.12990](https://doi.org/10.1112/blms.12990).
