# Theory 102 — DEP-R09 common-height centered explicit-formula replay

- 상태:
  <code>COMMON_HEIGHT_REGULARIZER_CANCEL_EXACT /
  PRINCIPAL_CHANNEL_ANNIHILATION_EXACT /
  SHARP_CENTERED_REMAINDER_COEFFICIENT_EXACT /
  T_F_THREE_HALVES_PARAMETERIZED_CORRECTION /
  SIGNED_ZERO_BOUND_AND_NUMERICAL_EF_MULTIPLIER_OPEN</code>
- 선행 정본: Theory 94--101, review 110
- 기계 원장:
  [common-height replay v1](data/Sono_FMT_DEPR09_common_height_replay_v1.json)
- 목표: 같은 modulus·height·zero convention의 두 endpoint explicit formula를
  residue-centered projection에 먼저 합성한다. Characterwise 절댓값을 취하지 않고
  signed zero packet, residue remainder, prime-power correction을 분리한다.
- 비목적: source의 effective implied constant를 수치 1로 치환하거나, 작은 height가
  signed zero gate를 닫았다고 주장하거나, actual prime/zero 계산·threshold calculator를
  실행하거나, PAP-11·DEP-R09·fixed coefficient·numerical \(X_{\rm cert}\)를 닫는 것.

## 1. 실제 적용영역과 centered mask

Theory 94--95의 actual \(f\mid P(X)/B_0\), \(f>Y>X\), \(Q'\subset(X,Y]\)를 유지한다.
\(Q'\)의 prime은 서로 다른 reduced residues이며 \(N=|Q'|<\varphi(f)=:\phi\)다.
또 \(P^+(f)\le X\)이므로 \((X,U]\)의 prime은 모두 \(f\)에 대해 unit이다.
이 절의 finite identities는 임의의 finite reduced-residue subset에도 성립한다.

\[
 H(a):=\phi\,{\bf1}_{Q'}(a)-N
 \qquad(a\in(\mathbb Z/f\mathbb Z)^\times).
 \tag{102.1}
\]

\[
 \boxed{\sum_a H(a)=0.}
 \tag{102.2}
\]

Prime-power congruence는 base prime이 아니라 integer \(n=p^k\)에 적용한다.

\[
 \psi(x;f,a):=\sum_{\substack{n\le x\\n\equiv a\pmod f}}\Lambda(n),
 \qquad
 \vartheta(x;f,a):=\sum_{\substack{p\le x\\p\equiv a\pmod f}}\log p.
 \tag{102.3}
\]

Endpoint는 closed \(n\le x\)다. Half-weight convention을 사용한다면 endpoint atom을
별도로 remainder에 넣어야 하며, 무조건 버리지 않는다.

## 2. Primary-source replay와 두 전사 문제

Thorner--Zaman, *Refinements to the Prime Number Theorem for Arithmetic Progressions*,
printed p.9, 식 (4.2) 바로 위 \(\psi\) display와 official native TeX lines 533--549를
대조했다. Official source archive와 PDF는 이전 source registry의 hash와 일치한다.

확인한 주의점:

1. \(\psi\) display의 prime-power 조건이 literal \(p\equiv a\)로 인쇄되어 있다.
   Canonical AP \(\psi\)는 식 (102.3)의 \(p^k\equiv a\)다. 예를 들어
   \(2^2\bmod5=4\), \(2\bmod5=2\)이므로 두 정의는 같지 않다.
2. 식 (4.2)는 low-zero regularizer를 outer zero sum 안에 다시 넣은 형태로 인쇄한다.
   바로 앞 \(\psi\) display는 character별 bracket 안에서 한 번 빼는 형태다.
   후자의 convention을 사용하며, literal (4.2)를 그대로 기계 전사하지 않는다.

이는 standard explicit formula의 convention/transcription 문제다. 여기서는 corrected
standard interface를 명시적 analytic premise로 유지한다. Davenport source theorem을
Lean local axiom으로 추가하지 않았고, numerical implied constant도 아직 복원하지 않았다.

같은 \(f,T\ge2\)와 같은 primitive/induction·endpoint convention에서 다음 interface를 둔다.

\[
 \psi(x;f,a)=\frac{x}{\phi}
 -\frac1\phi\sum_{\chi\bmod f}\overline{\chi(a)}
       \{F_\chi(x;T)-b_\chi(T)\}
 +r_x(a;T).
 \tag{102.4}
\]

여기 \(F_\chi\)는 \(L(s,\chi^*)\)의 nontrivial zeros를 multiplicity와 함께 세며,
possible distinguished real zero도 포함한다. Imprimitive Euler-factor의
\(\Re s=0\) zeros는 이 packet에 몰래 넣지 않고 source remainder convention에 남긴다.

\[
 F_\chi(x;T):=
 \sum_{\substack{0<\Re\rho<1\\|\Im\rho|\le T}}
       \frac{x^\rho}{\rho},
 \qquad
 \Delta F_\chi:=F_\chi(U;T)-F_\chi(X;T).
 \tag{102.5}
\]

Source의 exceptional-removed packet을 사용한다면 해당 real-zero term을 먼저 \(F_\chi\)에
돌려놓는다. Character별 \(b_\chi(T)\)는 \(x\)에 의존하지 않으므로

\[
 \boxed{(F_\chi(U;T)-b_\chi(T))
       -(F_\chi(X;T)-b_\chi(T))=\Delta F_\chi.}
 \tag{102.6}
\]

다. 서로 다른 height·zero convention을 사용하면 이 상쇄를 주장할 수 없다.

## 3. Signed zero packet과 principal channel

Character orthogonality와 식 (102.2)로 residue projection을 먼저 수행한다.
Theory 95의 \(C_\chi(Q')=\sum_{q\in Q'}\overline{\chi(q)}\)를 유지한다.
\(\Pi_a\)는 \((X,U]\)의 higher-prime-power mass다.

\[
 \boxed{
 {\cal C}_f=
 -\sum_{\chi\ne\chi_0} C_\chi(Q')\,\Delta F_\chi
 +{\cal R}_{\rm EF}-{\cal R}_{\rm pp},}
 \quad
 {\cal R}_{\rm EF}:=\sum_aH(a)\{r_U(a;T)-r_X(a;T)\},
 \quad
 {\cal R}_{\rm pp}:=\sum_aH(a)\Pi_a.
 \tag{102.7}
\]

Pole main term뿐 아니라 principal zero packet 전체가 residue-constant channel이다.

\[
 \boxed{\sum_a H(a)\,z=0\quad\text{for every }z\in\mathbb C.}
 \tag{102.8}
\]

따라서 principal zeta-zero estimate는 이 centered target의 별도 예산이 아니다.
반면 possible real zero는 nonprincipal channel일 수 있다. 이를 packet 밖으로 빼면

\[
 -C_{\chi_1}(Q')\,
       \frac{U^{\beta_1}-X^{\beta_1}}{\beta_1}
 \tag{102.9}
\]

를 반드시 유지한다. Theory 98의 actual \(B_0\) relative separation 및 structural
\(\lambda=1\) branch는 \(\beta_1\)의 부재를 증명한 것이 아니다. \(B_0\)만으로
식 (102.9)를 삭제하지 않는다.

## 4. Residue remainder의 정확한 coefficient

Source \(\psi\) display의 error shape를 다음처럼 분리한다.

\[
 {\cal E}_{\psi}(x;f,T):=
 \frac1\phi\left\{
    \frac{x\log x+T}{T}\log f+\log x
    +\frac{x(\log x)(\log T)}{T}\right\}
 +(\log x)(\log f)+\frac{x(\log x)^2}{T}.
 \tag{102.10}
\]

Uniform endpoint input \(|r_x(a;T)|\le K_{\rm EF}{\cal E}_{\psi}(x;f,T)\)를
**premise**로 둔다. Source는 effective absolute implied constant를 말하지만
\(K_{\rm EF}\)의 numerical value와 corrected closed-endpoint implementation은 인쇄하지 않는다.
이 leaf는 <code>OPEN</code>이다.

Exact centered \(L^1\) mass는

\[
 \boxed{\sum_a|H(a)|=2N(\phi-N).}
 \tag{102.11}
\]

이므로 complex residue errors의 uniform bounds \(e_U,e_X\)로부터

\[
 \boxed{
 \left|\sum_a H(a)\{r_U(a)-r_X(a)\}\right|
 \le2N(\phi-N)(e_U+e_X).}
 \tag{102.12}
\]

를 얻는다. Uniform-error premise class에서 \(r_U(a)=e_U\operatorname{sgn}H(a)\),
\(r_X(a)=-e_X\operatorname{sgn}H(a)\)로 equality가 가능하다. 이는 actual remainders가
정렬된다는 주장이 아니다. Character \(L^1\) upper로 우회할 필요가 없다.

\(X\le U\), \(f,T\ge2\)에서 식 (102.10)은 \(x\)에 대해 증가하므로

\[
 \frac{|{\cal R}_{\rm EF}|}{NU}
 \le \frac{4(\phi-N)K_{\rm EF}}{U}
          {\cal E}_{\psi}(U;f,T).
 \tag{102.13}
\]

Higher prime powers는 \(\sum_{p^k\le U,k\ge2}\log p\le\sqrt U\log U\)다:
각 \(p\le\sqrt U\)의 총 기여가 \(\log U\) 이하이고 prime 수를 integer 수로 상계한다.
\(|H(a)|\le\phi\)를 쓰면

\[
 \frac{|{\cal R}_{\rm pp}|}{NU}
 \le\frac{\phi}{N}\frac{\log U}{\sqrt U}.
 \tag{102.14}
\]

다. Source (4.2)의 implicit \(\sqrt x\) multiplier를 1로 가정하지 않고 이 elementary
global upper를 별도로 증명했다.

## 5. \(T=f^{3/2}\)의 parameterized correction budget

Actual scale \(U=f^d\), \(21\le d<416\), \(\ell=\log f\ge1\), \(T=f^s\),
\(1<s\le21\)를 쓴다. \(\phi-N\le\phi\le f\)로 식 (102.13)을 전개하면

\[
 \frac{|{\cal R}_{\rm EF}|}{NU}
 \le4K_{\rm EF}\left\{
 d(1+s)\ell^2f^{-s}+(1+d)\ell f^{-d}
 +d\ell^2f^{1-d}+d^2\ell^2f^{1-s}\right\}.
 \tag{102.15}
\]

즉 절단오차를 작게 만드는 데 \(s=5\)는 필요하지 않다. \(s=3/2\)에서

\[
 \frac{|{\cal R}_{\rm EF}|}{NU}
 \le699716K_{\rm EF}\ell^2e^{-\ell/2},
 \qquad
 \frac{|{\cal R}_{\rm pp}|}{NU}
 \le416\ell e^{-19\ell/2}.
 \tag{102.16}
\]

Coefficient는 실제 \(f,U\)를 계산한 값이 아니라 uniform rational upper다.

\[
 4\{416^2+(3+3/2)416+1\}=699716.
 \tag{102.17}
\]

\(A:=699716K_{\rm EF}+416\), \(K_{\rm EF}>0\)라 두면

\[
 \frac{|{\cal R}_{\rm EF}|+|{\cal R}_{\rm pp}|}{NU}
 \le A\ell^2e^{-\ell/2}
 \le A e^{-\ell/4}\qquad(\ell\ge64).
 \tag{102.18}
\]

마지막 부등식은 \(\ell^2\le e^{\ell/4}\)를 쓴다. \(\ell=64\)에서
\(2\log64=12\log2<12<16\)이고,
\((2\log\ell-\ell/4)'=2/\ell-1/4<0\)이므로 전 범위에 성립한다.
따라서 주어진 \(0<\varepsilon<1\)에 대한 sufficient cutoff는

\[
 \ell\ge
 \max\{64,\ 4(\log A-\log\varepsilon)\}
 \quad\Longrightarrow\quad
 |{\cal R}_{\rm EF}|+|{\cal R}_{\rm pp}|\le\varepsilon NU.
 \tag{102.19}
\]

이는 symbolic parameterized correction lemma다. \(K_{\rm EF}\)도 signed-zero input도
미수치이므로 numerical \(X_{\rm cert}\), 범위 축소 증명 또는 threshold calculator가 아니다.
직접 endpoint remainder를 모든 character별 절댓값과 곱해 과대평가하는 경로와 구별한다.

## 6. Theory 100의 height scope 교정

Theory 71의 \({\cal D}=Q^2T\), \(Q=f\),
detector \(x={\cal D}^{1+12\omega}(\log{\cal D})^2\)를 유지하면

\[
 \kappa_s(\omega)=2(2+s)(1+12\omega),
 \qquad
 \kappa_{3/2}(1/21)=11,\quad \kappa_5(1/21)=22.
 \tag{102.20}
\]

\(T=f^{3/2}\)는 inherited \(T=f^5\)보다 detector exponent를 줄이며
\(d\ge21\)에서 \(1-11/d>0\)다. 그러나 **전체 density transfer를 다시 닫지는 않았다**.
Finite detector prerequisites, actual zero-free denominator, far-alpha branch,
exceptional contribution, common remainder multiplier를 이 height에서 다시 감사해야 한다.

Theory 100의 \(>10^6\), \(>4000\) coefficient diagnostic은 \(T=f^5\)를 고정한 결과다.
다른 height까지 배제하지 않는다. Historical rational identities와 tests는 유지하고,
height 전체에 관한 universal interpretation만 철회한다.

## 7. 증거 수준과 검증 범위

- Lean: finite mask zero sum·complex constant-channel annihilation·exact \(L^1\),
  arbitrary complex interval remainder bound, common regularizer cancellation과 finite
  weighted replay를 검사한다. Endpoint analytic identities는 replay theorem의 explicit premises다.
- Python: all small abstract masks의 sharp remainder, modulo-5 complex character
  projection과 principal-packet invariance, mismatched regularizer rejection, error-shape
  monotonic fixture, rational height coefficients를 검사한다. Actual primes/zeros를 생성하지 않는다.
- Real log/exp cutoff 및 actual character/source identification은 Lean 전체 형식화가 아니다.
- Numerical \(K_{\rm EF}\), signed zero bound, PAP-11·DEP-R09·fixed \(2e-17\)·
  \(X_{\rm cert}\)는 <code>OPEN</code>. Calculator·actual 계산은
  <code>NOT READY / NOT RUN</code>.

## 8. 다음 gate

1. \(T=f^{3/2}\) 또는 symbolic \(s>1\)에서 Theory 61--71의 finite detector prerequisites와
   actual fixed-\(f\) zero-free denominator를 다시 합성한다. Theory 100 floor를 그대로 복사하지 않는다.
2. Corrected closed-endpoint \(\psi\) explicit formula의 uniform numerical \(K_{\rm EF}\)를
   원문에서 복원하거나 명시적 source로 교체한다. 수치 multiplier 1 가정은 금지한다.
3. Signed zero theorem이 필요하면 식 (102.7)의 actual coefficients와 exceptional channel을
   그대로 보존하는 lemma를 source-first로 찾거나 증명한다.
4. Numerical signed input·common cutoff·DEP-R09--R12 composition 전 calculator는 만들지 않는다.

## 9. 참고문헌

- J. Thorner and A. Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878),
  printed p.9, preceding \(\psi\) display and equation (4.2), native TeX.
- H. Davenport, *Multiplicative Number Theory*, Chapters 17--20:
  위 primary source가 인용한 standard explicit formula. Book 자체를 이번 batch에서
  직접 검증했다고 주장하지 않는다.
