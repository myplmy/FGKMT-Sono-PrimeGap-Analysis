# Theory 103 — DEP-R09 fixed-modulus height-weighted density replay

- 상태:
  <code>FIXED_MODULUS_D_FT_SOURCE_RECOVERED /
  ALL_HEIGHT_RANKIN_COEFFICIENT_EXPLICIT /
  HEIGHT_WEIGHTED_NEAR_FAR_REDUCTION /
  CONDITIONAL_D_GE_333_NONVANISHING_BUDGET_LT_ONE_PERCENT</code>
- 선행 정본: Theory 64--73, 90, 98, 102; review 111
- 기계 원장:
  [height-weighted density v1](data/Sono_FMT_DEPR09_height_weighted_density_v1.json)
- 목표: common-height centered target에서 fixed-\(f\) zero family와
  \(1/|\rho|\)의 height saving을 보존하고 numerical density coefficient를 재합성한다.
- 비목적: 실제 construction에 \(d_f\ge333\)을 임의 가정하거나, numerical EF multiplier를
  1로 두거나, actual prime/zero 계산·threshold calculator·range search를 실행하거나,
  PAP-11·DEP-R09·\(X_{\rm cert}\)를 닫는 것.

## 1. Source가 이미 구분한 fixed modulus와 modulus average

Jutila printed p.46은 모든 characters modulo \(q\)의 \(N(\alpha,T,q)\)와 primitive
conductors \(q\le Q\)의 \(N^*(\alpha,T,Q)\)를 별도로 정의한다.
Theorem 1 (1.7)은 전자에 \(qT\), (1.8)은 후자에 \(Q^2T\)를 사용한다.
Printed p.51의 proof도 (1.7)에서 \(D=qT\), \(\chi\ne\chi_0\)로 시작한다.
Imprimitive characters를 제외하는 asterisk는 fixed-modulus statement에 없다.

\[
 \boxed{D_f(t)=ft,\qquad
 D_{\rm avg}(t)=f^2t,\qquad
 L(t)=\log(ft).}
 \tag{103.1}
\]

따라서 Theory 70의 실제 fixed-modulus near-one package를 직접 쓸 수 있다.
Primitive conductor partition으로 확인해도 \(r,s\mid f\)이면

\[
 \boxed{\operatorname{lcm}(r,s)\mid f,\qquad
        \operatorname{lcm}(r,s)\le f.}
 \tag{103.2}
\]

이다. 모든 conductor가 임의의 \(r,s\le f\)인 경우와 구별한다.
Primitive inducing character는 modulo \(f\)에서 하나의 lift를 가지며,
nontrivial zeros \(0<\Re\rho<1\)는 같은 packet이다. Euler-factor zeros \(\Re\rho=0\)는
이 density family에 넣지 않는다. Character 수 자체를 줄였다는 주장도 아니다.

Theory 64의 fixed-\(f\) detector는

\[
 A=(ft)^{1/2}Rz_2=D_f(t)^{1+9\omega},
 \quad R=D_f(t)^\omega,\quad
 z_2=D_f(t)^{1/2+8\omega},\quad\omega=\frac1{21}.
 \tag{103.3}
\]

를 가진다. 원 power condition의 margin은

\[
 (1-\omega)(1+12\omega)-(1+\omega)(1+9\omega)
 =\omega(1-21\omega)=0.
 \tag{103.4}
\]

Zero-family/phase를 변경한 새 analytic theorem이 아니라 기존 source의 정확한 branch를
다시 사용하는 것이다. Published qualitative cross-check도 Jutila (1.7)을 fixed-modulus
all-character estimate로 인용하지만 numerical multiplier는 인쇄하지 않는다.

## 2. 모든 local height를 덮는 finite prerequisites

\(\ell=\log f\), \(1\le t\le T=f^{3/2}\)라 두고 source cutoff를

\[
 \ell\ge L_*:=
 \max\left\{
 L_0(1/21,\eta_5,\eta_X,\eta_M,\eta_T),\
 e^8,\
 \frac1\gamma\log
 \frac{36mC_{{\rm pre},{\rm tight}}\overline C_{\rm CL3}}
      {\underline c_g^2}
 \right\},\quad
 m=10^6,\quad\gamma=\frac{29}{5292}
 \tag{103.5}
\]

로 요구한다. \(L_0\)는 Theory 64 (64.20)의 네 positive budget을 합
\(\eta_{\rm out}\le1/21\)로 배분한 explicit expression이다.
그러면 \(L(t)\ge\ell\ge L_*\)여서 모든 local \(t\)의 detector·finite log ratio·
strict absorption을 함께 덮는다. Source cutoff의 decimal diagnostic은 사용하지 않는다.

Theory 73의 residue coefficient \(710/171\)는 \(\log q/L\le1/2\)를 썼다.
Local \(t<f\)에서는 이 조건이 없다. Theory 69 (69.19)--(69.20)을 보존하면

\[
 \frac{S_f(R)}{(\varphi(f)/f)L}
 \le e^{\omega+\log f/L}(1+1/L)
 \le e^{22/21}\frac{442}{441}<3
 \qquad(L\ge441).
 \tag{103.6}
\]

이다. 마지막 strict exponential inequality는 Lean으로 증명했다.
이 envelope 3과 height-row \(2840/1197\), Theory 73의 나머지 factors를 합치면

\[
 \boxed{
 C_{J,{\rm all}}=
 \frac{10^6}{999999}
 \left(3\frac{2840}{1197}\right)
 \frac85\frac{15665428311}{1750000}
 \left(\frac4{147}\right)^{-2}
 \left(\frac{55}{18522}\right)^{-1}
 =\frac{19720624464771552}{425315}<5\cdot10^{10}.}
 \tag{103.7}
\]

이는 old tightened coefficient의 \(12/7\)배다. Height를 줄인 뒤 old \(7/4\) residue
envelope를 그대로 쓰지 않는다. Source norm·complex contour의 전체 Lean proof는 아니다.

Fixed-\(f\) nonprincipal near-one count에, \(0<\delta\le\omega\)에서

\[
 N_f(\delta,t)\le
 2C_{J,{\rm all}}x(t)^{2\delta}
       \{3+\max(\delta,L(t)^{-1})\log(2ft)\},
 \qquad
 x(t)=(ft)^{1+12\omega}L(t)^2.
 \tag{103.8}
\]

를 얻는다. Theory 70의 parity/local recovery와 같은 factor 2다.
Source \(L\ge e^8\)의 \(4\log L/L\le29/252<1/7\)를 쓰면 exponent를
\(kL\delta\), \(k:=23/7\)로 올릴 수 있다. Absorption 전의 exact height exponents는

\[
 \kappa_s=2(1+s)(1+12\omega),\qquad
 \kappa_{3/2}=\frac{55}{7},\quad \kappa_0=\frac{22}{7}.
 \tag{103.9}
\]

이다. Theory 102의 averaged specialization \(\kappa_{3/2}=11\)과 다른 branch다.

## 3. Actual zero-free boundary와 한 real-zero channel

McCurley Theorem 1은 \(M=\max\{f,f|\gamma|,10\}\),
\(R=9.645908801\)에서 product over characters modulo \(f\)에 at most one simple real
zero를 허용한다. \(\ell\ge441\)이면 \(f>10\)이므로, 그 possible zero \(\beta_1\)만
분리하고 나머지 \(|\gamma|\le t\), \(t\ge1\)에는

\[
 \boxed{\delta=1-\beta\ge\delta_0(t):=\frac{c_M}{L(t)},
 \qquad c_M=\frac{10^9}{9645908801}.}
 \tag{103.10}
\]

를 쓴다. Exception을 삭제한 family는 식 (103.8)의 subset이므로 density upper가 보존된다.

Possible \(\beta_1\)는 actual \(B_0\)만으로 부재라고 할 수 없다. Theory 98의
Proposition 5.3 direct \(t=0\)와 project log ratio가

\[
 \boxed{1-\beta_1\ge\frac{c_{B_0}}{\ell},
       \qquad c_{B_0}=\frac{47}{2520}.}
 \tag{103.11}
\]

를 준다. Standard \(c_M/\ell\) width와 이 더 약한 bound를 혼용하지 않는다.
McCurley의 exceptional \(\beta_1\), Sono/FMT의 full-\(P(X)\) exception은 같은 정의가 아니다.

## 4. Near-one count를 weighted mass로 옮기기

\(u=\log U=d\ell\), \(21\le d<416\),
\(A(t)=\sum_{\rho\ne\beta_1,\,\beta\ge1-\omega,\,|\gamma|\le t}e^{-u(1-\beta)}\)라 둔다.
Finite counting-measure layer cake는

\[
 A(t)=e^{-u\omega}N_f(\omega,t)
       +u\int_{\delta_0(t)}^\omega e^{-u\delta}N_f(\delta,t)\,d\delta.
 \tag{103.12}
\]

이다. Lower zero-free interval 아래에는 해당 zeros가 없다. Boundary atoms를
임의로 삭제하지 않는다. \(N_f\)는 이 절에서는 exceptional-removed near subset count다.

\(L\ge1\), \(\log(2ft)\le2L\), \(\max(\delta,L^{-1})\le\delta+L^{-1}\)로

\[
 N_f(\delta,t)\le
 2C_{J,{\rm all}}e^{kL\delta}(5+2\delta L),
 \qquad k=\frac{23}{7}.
 \tag{103.13}
\]

라 쓸 수 있다. \(v=u-kL>0\)이면 endpoint-safe integration은

\[
 A(t)\le
 2C_{J,{\rm all}}\frac uv
 \left(5+2c_M+\frac{2L}{v}\right)e^{-v\delta_0(t)}.
 \tag{103.14}
\]

를 준다. 실제 적분의 upper-endpoint coefficient
\((1-u/v)(5+2\omega L)-2uL/v^2\)는 nonpositive이므로 버릴 수 있다.
Integral을 늘린 뒤 positive endpoint term을 중복 계상하지 않았다.

\(h=\log t/\ell\in[0,3/2]\)에서 \(L=(1+h)\ell\),
\(d-k(1+h)\ge179/14>0\)이고

\[
 \frac uv\le\frac53,\qquad
 \frac Lv\le\frac15,\qquad
 5+2c_M+\frac{2L}{v}<6
 \quad\Longrightarrow\quad
 A(t)\le20C_{J,{\rm all}}
 e^{-c_M\{d/(1+h)-k\}}.
 \tag{103.15}
\]

이다. Normalized ratios와 마지막 scalar coefficient는 Lean에서 전체 parameter
rectangle에 대해 증명했다. Analytic counting-measure integral 전체는 아직 Lean proof가 아니다.

Height weight를 마지막까지 유지하면

\[
 \boxed{
 S:=\sum_{\substack{\rho\ne\beta_1\\\beta\ge1-\omega\\|\gamma|\le T}}
 \frac{U^{\beta-1}}{\max(1,|\gamma|)}
 =\frac{A(T)}T+\int_1^T\frac{A(t)}{t^2}\,dt.}
 \tag{103.16}
\]

가 된다. Each atom of height \(H=\max(1,|\gamma|)\) contributes
\(T^{-1}+\int_H^Tt^{-2}dt=H^{-1}\).
특히 low-height mass를 \(A(T)/T\)만으로 제어하지 않는다.

\(w=\log t\)에 대해 \(g(w)=w+c_M\{d/(1+w/\ell)-k\}\)라 두면

\[
 \boxed{g(w)-g(0)
 =w\left(1-\frac{c_Md}{\ell+w}\right)
 \ge\frac45w.}
 \tag{103.17}
\]

Source \(\ell\ge441\), \(c_M<1/9\), \(d<416\)이
\(c_Md\le\ell/5\)를 보장한다. 이 비교는 derivative approximation이 아니라
전체 \(w\ge0\)의 exact field inequality이며 Lean proof다.

따라서 integral cost는 \(5/4\), terminal cost는
\(e^{-6\ell/5}\le1/4\)로 제어한다. \(\ell\ge2\)와
\(e^{12/5}>1+12/5+(12/5)^2/2>4\)면 후자가 충분하다.
\(|\rho|^{-1}\le(21/20)/\max(1,|\gamma|)\), \(|C_\chi|\le N\)를 사용하면

\[
 \boxed{
 S\le30C_{J,{\rm all}}e^{-c_M(d-k)},\qquad
 \frac1{NU}\left|
 \sum_{\chi\ne\chi_0}C_\chi
 \sum_{\substack{\rho\ne\beta_1\\\beta\ge1-\omega\\|\gamma|\le T}}
 \frac{U^\rho}{\rho}\right|
 \le\frac{63}{2}C_{J,{\rm all}}e^{-c_M(d-k)}.}
 \tag{103.18}
\]

## 5. Far zeros·lower endpoint·possible real zero

Bennett et al. Theorem 1.1은 conductor \(r>1\), \(t\ge5/7\)에 explicit total zero count를
준다. \(t\ge1\), \(r\le f\)에서는 zero-count-zero branch 또는
\(0.22737<1\), \(2\log(1+a)\le2a\)를 써서
\(N(t,\chi)\le4t\log(f(t+2))\)다. 모든 nonprincipal characters modulo \(f\)를 합해도
수는 \(\varphi(f)-1\le f\)다.

Far \(\beta\le1-\omega\), \(|\gamma|\le1\)에는 near와 달리
\(1/|\rho|\le21/20\)를 쓰지 않는다. Kernel integral로
\(|(U^\rho-X^\rho)/\rho|\le(\log U)U^\beta\)를 쓰고,
\(|\gamma|>1\)에는 \(2U^\beta/|\gamma|\)를 쓴다.
Total count의 height integration으로

\[
 \boxed{\frac{|Z_{\rm far}|}{NU}
 \le5062\,\ell^2e^{-(d/21-1)\ell}.}
 \tag{103.19}
\]

를 얻는다. Low-height cost \(4f\log(3f)\le12f\ell\)에 \(d\le416\)을 곱해 4992,
high-height weighted cost \(4f(1+\log T)\log(f(T+2))\le35f\ell^2\)에 2를 곱해 70이다.
Far decay를 얻으려면 \(d>21\)가 필요하다.

Near packet의 \(X^\rho\) part는 \(1<X<f\), \(0<\beta<1\), \(N(T)\le14fT\ell\)로

\[
 \frac{|Z_{{\rm near},X}|}{NU}
 \le\frac{147}{10}\ell e^{-(d-7/2)\ell}.
 \tag{103.20}
\]

처럼 separately vanishing하다. Upper/lower kernel에 factor 2를 고정해 near constant를
두 배로 키우지 않았다. Possible simple real zero는 \(\beta_1>1-\omega\)이고 real powers의
차가 양수이므로

\[
 \boxed{\frac{|Z_{\beta_1}|}{NU}
 \le\frac{21}{20}e^{-c_{B_0}d}.}
 \tag{103.21}
\]

이다. Real-zero absence나 small-prime coefficient cancellation을 가정하지 않는다.

## 6. 전체 centered binary-prime budget과 conditional regime

Theory 102의 EF·prime-power corrections를 포함하면

\[
 \boxed{\frac{|{\cal C}_f|}{NU}\le
 \underbrace{\frac{63}{2}C_{J,{\rm all}}e^{-c_M(d-23/7)}
 +\frac{21}{20}e^{-c_{B_0}d}}_{{\cal B}_{\rm nv}(d)}
 +\underbrace{
 \frac{147}{10}\ell e^{-(d-7/2)\ell}
 +5062\ell^2e^{-(d/21-1)\ell}
 +(699716K_{\rm EF}+416)\ell^2e^{-\ell/2}}_{{\cal B}_{\rm van}(\ell,d,K_{\rm EF})}.}
 \tag{103.22}
\]

이 bound는 mathematical source/premise composition이다. Actual error를 계산한 결과가 아니다.

하나의 fixed proof regime \(d\ge333\)에서,

\[
 c_M>\frac{129}{1250},\quad
 \frac{129}{1250}\left(333-\frac{23}{7}\right)>34,\quad
 c_{B_0}\,333>6,\quad
 \frac{63}{2}(5\cdot10^{10})\left(\frac{10}{27}\right)^{34}
 +\frac{21}{20}\left(\frac{10}{27}\right)^6<\frac1{100}.
 \tag{103.23}
\]

\(e>27/10\)와 식 (103.7)을 쓰면 real exponential kernel도

\[
 \boxed{{\cal B}_{\rm nv}(d)<\frac1{100}\qquad(d\ge333).}
 \tag{103.24}
\]

이다. Rational terminal뿐 아니라 이 displayed real exponential bound도 Lean으로 증명한다.
333은 \(X_{\rm cert}\) 수치나 최적 threshold를 검색한 값이 아니라 fixed sufficient
parameter regime이다. Actual construction의 uniform \(d_f\ge333\)은 **아직 증명하지 않았다**.

만일 actual source/scale premises와 numerical \(K_{\rm EF}\)가 공급되고
common cutoff에서 \({\cal B}_{\rm van}<1/100\)을 증명하면

\[
 \boxed{\frac{|{\cal C}_f|}{NU}<\frac1{50}.}
 \tag{103.25}
\]

를 얻는다. 이 conditional branch를 actual same-law all-character moment 또는 PAP로
바로 승격하지 않는다. Blind fixed-modulus component가 전체 correlation과 같은 것은 아니다.

## 7. 증거 수준·남은 최소 gate

- Verified primary source: Jutila p.46·51·53 rendered scans, McCurley p.8, Bennett p.2;
  native text와 scan/type를 구분하고 source SHA를 재확인했다.
- Finite tests: exact layer-cake endpoints, repeated/empty atoms, negative-premise rejection,
  detector exponents, all-height coefficient, normalized parameter ratios·fixed rational budget.
- Lean: lcm divisor bound·log specialization·Rankin exponential envelope·rational coefficient,
  finite scalar layer cake·ratio/cost algebra·fixed real-exponential budget·conditional final allocation.
- Counting-measure integrals, actual characters/zero lists·source theorems 전체는 미형식화다.
  Project-local axiom/sorry/admit은 사용하지 않는다.

다음 최소 gate는 실제 law에서의 \(d_f\) uniform lower와 downstream parameter admissibility다.
Theory 49의 \(P'\)는 \(B_0\)를 뺀 fixed raw primes \((X/2,X]\)이며 good subset
\(P(\mathbf A)\)와 다르다. Theory 89의 \(h=Q_{\cal S}\prod_{p\in P'}p\)를 이 정의에
맞춰 primorial cancellation부터 감사한다. 원래 outer \(D=160\)을 바꾸지 않고 native
regime에 필요한 실제 budget을 먼저 판정한다. 333은 필요조건이 아니며 이를 actual law에
강제하지 않는다. Numerical \(K_{\rm EF}\), vanishing cutoff, nonblind character
correlation·DEP-R09--R12 composition도 OPEN이다.

이번 개선은 classical fixed-modulus density와 height partial summation을 정확한 target에
연결한 것이며 source가 배제했던 영역의 새 학술정리라고 주장하지 않는다.
Calculator·actual prime/zero 계산·bounded \(X_{\rm cert}\) range는 NOT READY / NOT RUN이다.

## 8. 참고문헌

- M. Jutila, [*On Linnik's constant*](https://doi.org/10.7146/math.scand.a-11701),
  printed p.46 Theorem 1 (1.7), p.51 fixed-\(q\) setup, p.53 terminal inequality.
- K. S. McCurley, [*Explicit Zero-Free Regions for Dirichlet L-Functions*](https://doi.org/10.1016/0022-314X(84)90089-1),
  Theorem 1, printed p.8. Some older project registry titles confused this paper with
  the author's separate AP error-term paper; the pinned PDF/Theorem 1 used here is the zero-free paper.
- M. A. Bennett, G. Martin, K. O'Bryant, A. Rechnitzer,
  [*Counting Zeros of Dirichlet L-Functions*](https://doi.org/10.1090/mcom/3599), Theorem 1.1.
- [*Unconditional correctness of recent quantum algorithms for factoring and computing discrete logarithms*](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/unconditional-correctness-of-recent-quantum-algorithms-for-factoring-and-computing-discrete-logarithms/3077F5BD48D1F62000B1ED800EB86308),
  Proposition 3.10: qualitative fixed-modulus statement cross-check only, not numerical input.
