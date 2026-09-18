# Theory 85 — DEP-R09 Vaughan 2001 variance 원문 감사

- 상태:
  <code>REQUESTED_FULL_TEXT_VERIFIED /
  VARIANCE_TO_CHARACTER_ENERGY_BRIDGE_EXACT /
  CURRENT_REGIME_NUMERICAL_DROP_IN_NOT_IDENTIFIED</code>
- 선행 정본: Theory 82--84, review 90·92·93
- 목표: R. C. Vaughan의 2001 variance 논문을 원문 page 단위로 감사하고,
  논문의 residue variance와 Theory 82의 nonprincipal character energy 사이 exact
  relation 및 source-range 경계를 고정한다.
- 비목적: GRH branch 채택, implicit (O)-상수의 임의 수치화, actual prime 계산,
  PAP-11, DEP-R09, fixed (2\times10^{-17}), numerical (X_{\rm cert})를 이번
  단계에서 인증하는 것.

## 1. 결론

새 로컬 파일은 요청한 논문 원문과 정확히 일치한다. Vaughan의 residue-class variance를
(V_{\rm Vau}(Y,q)), Theory 82의 nonprincipal character energy를
(V_{\rm proj}(Y,q))라 쓰면, endpoint와 von Mangoldt normalization을 같게 했을 때

\[
 \boxed{
 V_{\rm proj}(Y,q)
 =\varphi(q)V_{\rm Vau}(Y,q)
 -|\psi(Y,\chi_0)-Y|^2
 \le \varphi(q)V_{\rm Vau}(Y,q).}
 \tag{85.1}
\]

이것은 Vaughan variance upper를 Theory 82 input으로 옮기는 exact finite bridge다.
그러나 이 논문의 주정리는 한 prescribed (q)의 fully numerical upper가 아니라
(Q/2<q\le Q)에 대한 moment theorem이다. 무조건부 Theorem 1의 범위는 fixed
(A>0)에 대해 (Q\ge Y(\log Y)^{-A})이고, project family는
(q=Y^{1/d}\le Y^{1/21})이다. 한 fixed (A)로 growing primorial family를 덮지
못한다. GRH Theorem 2의 (Q\ge Y^{3/4+\varepsilon}) 범위는 더 멀다.

또한 정리의 (O)-상수, positive constant (c), finite cutoff는 수치화되어 있지 않다.
따라서 requested source의 identity와 exact bridge는 닫혔지만 Theory 82 식 (82.3)의
fully numerical current-regime analytic input은 계속 <code>OPEN</code>이다.

## 2. 원문 provenance

로컬 파일은 다음과 같다.

| 항목 | 확인값 |
|---|---|
| 파일 | <code>article/vaughan2001.pdf</code> |
| SHA-256 | <code>d5bc8d92c1204b09233c507b83ee185e35a54186122da1c906df87bbcb9d3ecc</code> |
| 크기 | 180,481 bytes |
| PDF | version 1.2, 21 pages, unencrypted |
| text/image | native text, raster image 0 |
| 서지 | R. C. Vaughan, “On a Variance Associated with the Distribution of Primes in Arithmetic Progressions,” *Proc. London Math. Soc.* (3) 82 (2001), 533--553 |
| DOI | 10.1112/plms/82.3.533 |

generic file parser 하나는 잘못된 10-page 값을 냈으므로 page count authority로 쓰지
않았다. MiKTeX <code>pdfinfo.exe</code>의 21 pages, native-text extraction과 rendered
printed pp.533, 535--536을 서로 대조했다. title·author·journal pagination,
equations (1.1)--(1.3), Theorems 1--3과 implied-constant convention이 모두 일치한다.

## 3. Vaughan variance와 project energy의 exact relation

printed p.533 식 (1.1)--(1.2)에 따라

\[
 \psi(Y;q,a):=
 \sum_{\substack{n\le Y\\n\equiv a\pmod q}}\Lambda(n),
 \qquad
 V_{\rm Vau}(Y,q):=
 \sum_{\substack{a\bmod q\\(a,q)=1}}
 \left|\psi(Y;q,a)-\frac{Y}{\varphi(q)}\right|^2.
 \tag{85.2}
\]

(n:=\varphi(q)), (A_a:=\psi(Y;q,a)) 및 reduced-residue total

\[
 S:=\sum_{(a,q)=1}A_a=\psi(Y,\chi_0)
 \tag{85.3}
\]

로 둔다. 유한 center-shift 항등식은

\[
 \sum_{(a,q)=1}\left|A_a-\frac Yn\right|^2
 =
 \sum_{(a,q)=1}\left|A_a-\frac Sn\right|^2
 +\frac{|S-Y|^2}{n}.
 \tag{85.4}
\]

이다. cross term은 (sum_a(A_a-S/n)=0)이므로 사라진다. nonprincipal finite
character Parseval은, Theory 76·82와 같은 endpoint convention에서,

\[
 V_{\rm proj}(Y,q):=
 \sum_{\substack{\chi\bmod q\\\chi\ne\chi_0}}|Z_\chi(Y)|^2
 =\varphi(q)
 \sum_{(a,q)=1}\left|A_a-\frac S{\varphi(q)}\right|^2.
 \tag{85.5}
\]

식 (85.4)--(85.5)를 합치면

\[
 V_{\rm proj}(Y,q)+|S-Y|^2
 =\varphi(q)V_{\rm Vau}(Y,q),
 \tag{85.6}
\]

즉 식 (85.1)이 나온다. 특히 Vaughan의 center가 (S/\varphi(q))가 아니라
(Y/\varphi(q))라는 차이는 누락할 correction이 아니라 nonnegative principal-error
subtraction이다.

Theory 82 gate를 (G_{82})라 쓰면 다음은 충분하다.

\[
 V_{\rm Vau}(Y,q)<\frac{G_{82}}{\varphi(q)}
 \quad\Longrightarrow\quad
 V_{\rm proj}(Y,q)<G_{82}.
 \tag{85.7}
\]

이 bridge는 exact하지만 좌변을 current family에서 증명하는 analytic theorem은 별도다.

## 4. Vaughan Theorem 1의 정확한 object와 범위

printed p.534 식 (1.18)--(1.19)는 natural main term (U)와 dyadic moment를

\[
 U(Y,q)
 =Y\left\{
 \log q-\gamma-\log(2\pi)-
 \sum_{p\mid q}\frac{\log p}{p-1}
 \right\},
 \tag{85.8}
\]

\[
 M_k(Y,Q):=
 \sum_{Q/2<q\le Q}
 |V_{\rm Vau}(Y,q)-U(Y,q)|^k
 \tag{85.9}
\]

로 정의한다. printed p.535 Theorem 1은 fixed (A>0), positive integer (k)와

\[
 Y(\log Y)^{-A}\le Q\le Y
 \tag{85.10}
\]

에서

\[
 M_k(Y,Q)
 =O_k\!\left(QY^kF(Y/Q)^k\right)
 +O_{k,A}\!\left(QY^k(\log Y)^{-A}\right),
 \tag{85.11}
\]

\[
 F(y)\ll y^{-1/2}
 \exp\!\left\{
 -c\frac{(\log 2y)^{3/5}}{(\log\log 3y)^{1/5}}
 \right\},\qquad y\ge1,
 \tag{85.12}
\]

를 준다. 여기서 (c>0)와 모든 (O,\ll) multiplier는 source에서 numerical 값으로
고정되지 않는다.

한 (q\in(Q/2,Q])에 대해서는 nonnegative moment의 한 항을 버리지 않음으로써

\[
 |V_{\rm Vau}(Y,q)-U(Y,q)|
 \le M_k(Y,Q)^{1/k}
 \tag{85.13}
\]

를 얻을 수 있다. 그러나 이것은 (q)가 source range 안의 dyadic block에 있을 때만
유효하고, 우변의 source (O)-constant를 명시화하지 않는다.

## 5. Theorem 1과 current growing family의 range 불일치

현재 (Y=q^d), (21\le d\le186)이고 prescribed modulus를 포함하도록 (Q=q)를
택한다. 식 (85.10)의 lower condition은

\[
 q\ge\frac{q^d}{(d\log q)^A}
 \quad\Longleftrightarrow\quad
 A\ge A_{\rm req}(q,d):=
 \frac{(d-1)\log q}{\log(d\log q)}.
 \tag{85.14}
\]

fixed (d\ge2)에서 (q\to\infty)이면 (A_{\rm req}(q,d)\to\infty)다. 동치로

\[
 \frac{q}{Y(\log Y)^{-A}}
 =q^{1-d}(d\log q)^A\longrightarrow0
 \qquad(A,d\text{ fixed},\ d\ge2).
 \tag{85.15}
\]

따라서 매 (q)마다 (A=A(q))를 새로 크게 고르는 것은 fixed-(A) theorem의 uniform
growing-family 적용이 아니다. 더구나 (O_{k,A})의 (A)-dependence와 finite cutoff가
명시되지 않아 그러한 선택을 numerical certificate로 바꿀 수도 없다.

## 6. Theorem 2와 GRH branch

printed p.535 Theorem 2는 GRH, (\varepsilon>0), integer (k\ge2)와

\[
 Y^{3/4+\varepsilon}\le Q\le Y
 \tag{85.16}
\]

에서

\[
 M_k(Y,Q)
 =O_k\!\left(QY^kF(Y/Q)^k\right)
 +O_{k,\varepsilon}\!\left(
 QY^k(Y/Q)^kY^{\varepsilon-1/2}
 \right),
 \quad F(y)\ll y^{\varepsilon-7/12}
 \tag{85.17}
\]

를 준다. current exponent는 모든 허용 (d)에서

\[
 \frac1d\le\frac1{21}<\frac34+\varepsilon.
 \tag{85.18}
\]

따라서 (Q=q=Y^{1/d})는 Theorem 2 range 아래에 있다. 이 branch는 범위도 맞지 않고
GRH conditional이며, 프로젝트는 사용자 결정 없이 GRH branch를 unconditional 정본에
혼합하지 않는다.

## 7. Theorem 3의 역할과 한계

printed p.535 식 (1.20)의 partial singular series (S_q(y))에 대해 printed p.536
Theorem 3은 explicit main terms (R_1,R_0)와 함께

\[
 S_q(y)=R_1+R_0+
 O\!\left(
 y^{1/2}\exp\!\left{-c
 \frac{(\log 2y)^{3/5}}{(\log\log 3y)^{1/5}}
 \right\}
 \prod_{p\mid q}(1-p^{-1/4})^{-1}
 \right).
 \tag{85.19}
\]

이 식은 prime-specific structure가 Vaughan moment proof에 들어가는 중요한 source다.
그러나 자체가 prescribed primorial의 (V_{\rm Vau}) 또는 (V_{\rm proj}) upper는
아니고, error의 (O)-multiplier와 (c)도 implicit이다. 따라서 Theorem 3을 식 (82.3)의
drop-in으로 승격하지 않는다.

## 8. 코드·Lean 검증 범위

<code>source/dep_r09_vaughan2001_variance_audit.py</code>와 단위시험은 다음을
검사한다.

1. rational fixture에서 식 (85.4), (85.6)과 nonnegative correction.
2. (d=21,186)에서 식 (85.18)의 exact rational exponent gap.
3. 식 (85.14)의 log-space boundary diagnostic.
4. PDF hash·byte size와 fail-closed status ledger.

Lean은 식 (85.6)에서 nonnegative principal error를 버리는 terminal과 식 (85.7),
(85.18)의 finite real algebra만 검사한다. finite character orthogonality, Vaughan의
analytic Theorems 1--3, 점근극한 식 (85.15)는 project-local axiom으로 넣지 않는다.

## 9. 현재 판정

| 항목 | 판정 |
|---|---|
| 요청 Vaughan 2001 원문 | <code>VERIFIED, 21 PAGES</code> |
| Vaughan variance와 project energy bridge | <code>EXACT</code> |
| Theorem 1 object | <code>DYADIC MODULUS MOMENT</code> |
| Theorem 1 current growing-family 적용 | <code>NO FIXED-A COVERAGE</code> |
| Theorem 2 | <code>GRH CONDITIONAL; RANGE MISMATCH</code> |
| Theorem 3 | <code>RELEVANT STRUCTURE, NOT ENERGY UPPER</code> |
| fully numerical unconditional current-regime drop-in | <code>NOT IDENTIFIED</code> |
| prime-specific fixed-primorial upper | <code>OPEN</code> |
| actual same-law weighted correlation | <code>OPEN</code> |
| PAP-11·DEP-R09 | <code>OPEN</code> |
| fixed (2\times10^{-17}), numerical (X_{\rm cert}) | <code>OPEN</code> |
| 새 bounded (X_{\rm cert}) 범위 | <code>NONE</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 10. 다음 gate와 사용자 결정 경계

unconditional 정본의 다음 최소 gate는 그대로 다음 중 하나다.

1. prescribed growing primorial에서 fully numerical prime-specific upper.
2. full variance를 우회하는 actual same-law weighted-correlation theorem.

Vaughan 2001 원문 확보 자체로 추가 사용자 계산이나 허가는 필요하지 않다. 향후 GRH
conditional branch를 별도 연구축으로 열려면 unconditional 목표와 구분하는 사용자 결정이
필요하다. 그 결정 전에는 GRH branch를 current certificate에 사용하지 않는다.

## 11. 참고문헌

- R. C. Vaughan, “On a Variance Associated with the Distribution of Primes in
  Arithmetic Progressions,” *Proc. London Math. Soc.* (3) 82 (2001), 533--553,
  [DOI 10.1112/plms/82.3.533](https://doi.org/10.1112/plms/82.3.533).
- J. B. Friedlander and D. A. Goldston, “Variance of Distribution of Primes
  in Residue Classes,” *Q. J. Math.* 47 (1996), 313--336,
  [DOI 10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
