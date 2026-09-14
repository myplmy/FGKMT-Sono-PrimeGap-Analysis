# Theory 82 — DEP-R09 outer entropy·convolution second-moment reduction

- 상태:
  <code>OUTER_SHIFT_MIN_ENTROPY_EXACT /
  FINITE_CONVOLUTION_REDUCTION_EXACT /
  CHARACTER_ENERGY_ANALYTIC_INPUT_OPEN</code>
- 선행 정본:
  Theory 76, Theory 79--81
- 목표: 실제 FMT final law를 바꾸지 않고
  \(\rho_S=\mathbb E[1_{S_{\rm sieve}}|R|^2]\)를 하나의 명시적
  nonprincipal character-energy 조건으로 축약한다.
- 비목적: prime-error energy 정리 자체, PAP-11, DEP-R09, fixed
  \(2\times10^{-17}\), numerical \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

## 1. 결론

FMT의 outer coordinates만으로 final CRT shift의 각 atom에 정확한 상계를 얻을 수 있다.
이 상계는 inner covering output이 outer draw에 적응적으로 의존해도 유지된다.

\[
 \boxed{\Pr(m_\omega=r)\le\frac1{Q_{\mathcal S}}}
 \qquad
 \left(
 Q_{\mathcal S}:=\prod_{s\in\mathcal S}s
 \right).
 \tag{82.1}
\]

이를 finite character Parseval과 cyclic convolution Cauchy에 합치면

\[
 \boxed{
 \rho_S
 \le
 \frac{\varphi(q)N^2}{Q_{\mathcal S}}\,
 V(Y,q),\qquad
 V(Y,q):=\sum_{\substack{\chi\bmod q\\\chi\ne\chi_0}}
 |Z_\chi(Y)|^2.}
 \tag{82.2}
\]

Theory 81의 survivor floor \(M_{\min}>0\), prime scale \(Y>0\), correlation budget
\(\tau>0\), sieve-good mass lower bound \(p_*>0\)를 쓰면 다음이 충분하다.

\[
 \boxed{
 V(Y,q)
 <
 \tau^2p_*
 \frac{Q_{\mathcal S}M_{\min}^2Y^2}
 {\varphi(q)N^2}.}
 \tag{82.3}
\]

식 (82.3)은 새롭고 정확한 **reduction**이지만 좌변을 이 크기 아래로 내리는 fully
numerical fixed-primorial 정리는 아직 확보하지 못했다. 따라서 \(X_{\rm cert}\)의
새 bounded upper range는 없다.

## 2. 실제 FMT law와 outer atom cap

FMT에서

\[
 \mathcal S
 :=
 \{s\text{ prime}:v<s\le z,\ s\ne B_0\},
 \qquad
 Q_{\mathcal S}:=\prod_{s\in\mathcal S}s
 \tag{82.4}
\]

로 둔다. FMT printed p.12는 \(A_s\bmod s\)를 \(s\)마다 서로 독립인 균등변수로
고른다. printed p.9의 final extension은 inner prime coordinates를 완성하지만
\(s\in\mathcal S\)에서는 \(a_s=A_s\)를 그대로 보존한다. CRT shift의 부호를

\[
 m_\omega\equiv-a_p\pmod p
 \tag{82.5}
\]

로 고정하자.

임의의 \(r\bmod q\)를 하나 고정하면, \(m_\omega=r\)이 되려면 모든
\(s\in\mathcal S\)에서

\[
 A_s\equiv-r\pmod s
 \tag{82.6}
\]

여야 한다. 즉 한 final residue는 outer vector 전체를 유일하게 강제한다. 이 outer
vector의 확률이 정확히 \(Q_{\mathcal S}^{-1}\)이고, 그 vector를 조건으로 한 모든
가능한 inner output의 총확률은 1 이하이므로

\[
 \Pr(m_\omega=r)
 =
 \frac1{Q_{\mathcal S}}
 \Pr(m_\omega=r\mid A_s=-r\ {\rm for\ all}\ s\in\mathcal S)
 \le\frac1{Q_{\mathcal S}}.
 \tag{82.7}
\]

더 나아가 임의의 사건 \(E\)에 대해

\[
 \Pr(E,m_\omega=r)\le\frac1{Q_{\mathcal S}}.
 \tag{82.8}
\]

특히 \(E=S_{\rm sieve}\)로 둘 수 있다. 여기서는 final shift가 균등하다고 주장하지
않으며, outer와 inner가 독립이라고도 주장하지 않는다. 필요한 것은 outer vector의
정확한 균등성과 좌표 보존뿐이다.

## 3. nonprincipal residue error와 정규화

Dirichlet character를 nonunit에서 0으로 연장하고

\[
 e(a;Y)
 :=
 \frac1{\varphi(q)}
 \sum_{\substack{\chi\bmod q\\\chi\ne\chi_0}}
 \overline{\chi(a)}Z_\chi(Y)
 \tag{82.9}
\]

로 둔다. Theory 80의

\[
 C_\chi(m)
 =
 \sum_{s\in I}\overline{\chi(m+s)},
 \qquad
 R(m)
 =
 \sum_{\chi\ne\chi_0}C_\chi(m)Z_\chi(Y)
 \tag{82.10}
\]

를 쓰면 합의 순서를 바꾸는 것만으로

\[
 \boxed{
 R(m)=\varphi(q)\sum_{s\in I}e(m+s;Y).}
 \tag{82.11}
\]

여기서 \(I\)는 fixed interval의 integer offset multiset이고 \(N:=|I|\)이다.
offset이 modulo \(q\)에서 겹쳐도 아래 Cauchy 상계는 그대로 성립한다.

## 4. finite Parseval과 cyclic convolution energy

유한군 \((\mathbb Z/q\mathbb Z)^\times\)의 character orthogonality로

\[
 \sum_{a\bmod q}|e(a;Y)|^2
 =
 \frac1{\varphi(q)}
 \sum_{\substack{\chi\bmod q\\\chi\ne\chi_0}}
 |Z_\chi(Y)|^2
 =
 \frac{V(Y,q)}{\varphi(q)}.
 \tag{82.12}
\]

각 \(m\)에서 Cauchy--Schwarz를 적용하면

\[
 \left|\sum_{s\in I}e(m+s;Y)\right|^2
 \le
 N\sum_{s\in I}|e(m+s;Y)|^2.
 \tag{82.13}
\]

\(m\mapsto m+s\)가 modulo \(q\)의 순열이므로 \(m\)과 \(s\)를 합하면

\[
 \sum_{m\bmod q}
 \left|\sum_{s\in I}e(m+s;Y)\right|^2
 \le
 N^2\sum_{a\bmod q}|e(a;Y)|^2.
 \tag{82.14}
\]

식 (82.11)--(82.12)를 대입해

\[
 \boxed{
 \sum_{m\bmod q}|R(m)|^2
 \le\varphi(q)N^2V(Y,q).}
 \tag{82.15}
\]

를 얻는다. 상수열은 식 (82.14)의 \(N^2\)에 equality case를 주므로 추가 구조 없이
이 finite convolution step의 보편상수를 낮출 수 없다.

## 5. same-law raw moment

Theory 81과 같은 final sieve-good law에서

\[
 \rho_S
 :=
 \mathbb E\!\left[
 1_{S_{\rm sieve}}|R(m_\omega)|^2
 \right]
 =
 \sum_{m\bmod q}
 \Pr(S_{\rm sieve},m_\omega=m)|R(m)|^2.
 \tag{82.16}
\]

식 (82.8)과 (82.15)를 차례로 쓰면

\[
 \rho_S
 \le
 \frac1{Q_{\mathcal S}}
 \sum_{m\bmod q}|R(m)|^2
 \le
 \frac{\varphi(q)N^2}{Q_{\mathcal S}}V(Y,q),
 \tag{82.17}
\]

즉 식 (82.2)가 나온다. \(S_{\rm sieve}\)와 \(m_\omega\)의 독립성은 어느 단계에서도
사용하지 않았다.

Theory 81의 normalized moment는

\[
 \mu_S
 \le
 \frac{\rho_S}{M_{\min}^2Y^2}.
 \tag{82.18}
\]

따라서 식 (82.3)이면

\[
 \mu_S<\tau^2p_*,
 \tag{82.19}
\]

이고 Theory 81의 strict positive-mass terminal gate를 사용할 수 있다.

## 6. \(Q_{\mathcal S}\)의 명시적 하한

\(\vartheta(t):=\sum_{p\le t}\log p\)라 하면

\[
 \log Q_{\mathcal S}
 =
 \vartheta(z)-\vartheta(v)
 -1_{\{B_0\in(v,z]\}}\log B_0.
 \tag{82.20}
\]

Dusart 2010 printed p.4, Theorem 5.2의 \(k=1\) 행은 \(t\ge2\)에서

\[
 |\vartheta(t)-t|
 <
 \frac{12323}{10000}\frac{t}{\log t}
 \tag{82.21}
\]

를 준다. 따라서 \(z>v\ge2\)에서 계산 가능한 충분 하한

\[
 \boxed{
 \log Q_{\mathcal S}
 >
 z\!\left(1-\frac{12323}{10000\log z}\right)
 -
 v\!\left(1+\frac{12323}{10000\log v}\right)
 -
 1_{\{B_0\in(v,z]\}}\log B_0}
 \tag{82.22}
\]

를 얻는다. 이것은 식 (82.3)의 outer-entropy factor를 명시화하지만 좌변 \(V(Y,q)\)를
상계하지는 않는다.

## 7. 왜 outer entropy만으로는 아직 부족한가

식 (82.3)은 \(Q_{\mathcal S}\)만큼 budget을 늘리지만, \(M_{\min}\le N\)이므로 그
우변은 많아야

\[
 \tau^2p_*\frac{Q_{\mathcal S}}{\varphi(q)}Y^2.
 \tag{82.23}
\]

반면 character별 trivial estimate를 제곱해 합친 certificate를
\(V_{\rm triv}=C_{\rm triv}\varphi(q)Y^2L^2\)로 쓰면, 식 (82.3)의 우변
\(V_{\rm gate}\)와의 정확한 비는

\[
 \frac{V_{\rm triv}}{V_{\rm gate}}
 =
 \frac{
 C_{\rm triv}\varphi(q)^2N^2L^2
 }{
 \tau^2p_*Q_{\mathcal S}M_{\min}^2
 }.
 \tag{82.24}
\]

의 손실이 남는다. FMT parameter에서 \(\log q\asymp x\)인 반면
\(\log Q_{\mathcal S}\sim z=o(x)\)이므로 이 상계 방식은 지수적으로 너무 크다.
이는 실제 \(V(Y,q)\)가 크다는 하한이 아니라 **crude upper certificate가 gate를
인증하지 못한다**는 뜻이다.

반대로 fully numerical fixed-primorial theorem이 자연스러운 variance 크기

\[
 V(Y,q)\le C\varphi(q)Y\log q
 \tag{82.25}
\]

를 적절한 cutoff와 함께 준다면 \(Y=q^d\), \(d>2\)에서 (82.3)을 통과할 가능성이
매우 높다. 현재 병목은 계산량이 아니라 그러한 정리를 actual modulus와 상수로
증명하는 것이다.

## 8. 선행연구 적용성 감사

### 8.1 Davenport--Erdos 1952

원문 printed p.253, Lemma 1은 nonprincipal character modulo prime \(p\)와
\(0<h<p\)에 대해

\[
 \sum_{x\bmod p}\left|\sum_{n=1}^{h}\chi(x+n)\right|^2
 =ph-h^2
 \tag{82.26}
\]

를 준다. 프로젝트는 Legendre character로 모든 \(p\in\{3,5,7,11,13\}\)와
\(1\le h<p\)를 exact 전수검산했다. 그러나 이는 prime modulus와 uniform shift에 대한
benchmark이며, composite primorial·prime-error weight·adaptive FMT law의 식 (82.3)을
직접 주지 않는다.

### 8.2 fixed-modulus variance

Friedlander--Goldston 1996과 Vaughan 2001은 primes in residue classes의 variance를
다루므로 주제상 가장 가깝다. 하지만 이번 source screen에서 확인한 공개 statement는
asymptotic variance framework이고, project에 필요한 다음 네 조건을 한꺼번에 주는
drop-in theorem으로 확인되지 않았다.

1. 한 개의 prescribed growing primorial \(q\).
2. nonprincipal \(V(Y,q)\)의 upper bound.
3. 모든 numerical multiplier.
4. \(Y=q^d\), \(21\le d\le186\)와 겹치는 공통 finite cutoff.

### 8.3 BDH·moving-interval 결과

Barban--Davenport--Halberstam형 결과는 보통 modulus 범위에 대한 평균을 사용한다.
Harper 2024의 general-sequence 결과도 이 계열이며 한 prescribed primorial을 자동으로
선택하지 않는다. Harper 2022의 moving-interval 결과는 fixed nonprincipal character
modulo prime과 uniform random shift를 다루므로 actual composite/adaptive law와 다르다.
이들은 아이디어 source이지 현재 식 (82.3)의 numerical input은 아니다.

## 9. 검증 범위와 증거수준

<code>source/dep_r09_outer_entropy_second_moment.py</code>와 단위시험은 다음을
exact integer/rational arithmetic으로 확인한다.

1. modulo 30 toy에서 inner residue를 outer vector에 적응적으로 정해도 atom cap
   \(1/6\)이 유지됨.
2. Gaussian rational sequence의 cyclic convolution energy와 \(N^2\) Cauchy bound.
3. Davenport--Erdos 식 (82.26)의 small-prime 전수검산.
4. 식 (82.17)--(82.19)의 strict scalar gate와 boundary rejection.
5. source hash와 OPEN status의 fail-closed ledger.

Lean은 식 (82.17)--(82.19)의 dependency-critical scalar implication을 무공리로
검증한다. finite-group character orthogonality와 복소수 convolution Cauchy 전체는 이번
Lean batch에 형식화하지 않으며, 이를 <code>KERNEL_PASS</code>로 가장하지 않는다.

## 10. 현재 판정

| 항목 | 판정 |
|---|---|
| outer coordinate law·final coordinate 보존 | <code>SOURCE VERIFIED</code> |
| final-shift atom cap | <code>EXACT</code> |
| finite convolution reduction | <code>EXACT</code> |
| same-law raw moment reduction | <code>EXACT</code> |
| \(Q_{\mathcal S}\) elementary lower envelope | <code>PARAMETERIZED EXPLICIT</code> |
| fully numerical fixed-primorial \(V(Y,q)\) upper theorem | <code>OPEN</code> |
| PAP-11·DEP-R09 | <code>OPEN</code> |
| fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\) | <code>OPEN</code> |
| 새 bounded \(X_{\rm cert}\) 범위 | <code>NONE</code> |
| threshold calculator·장시간 prime 계산 | <code>NOT READY / NOT RUN</code> |

## 11. 다음 gate

다음 우선순위는 식 (82.3)에 직접 대입 가능한 fully numerical
nonprincipal character-energy upper bound를 찾거나 증명하는 것이다. 그 과정에서는

1. fixed prescribed primorial인지,
2. \(Z_\chi(Y)\) normalization이 정확히 같은지,
3. primitive/imprimitive character 전달 손실이 모두 수치화됐는지,
4. \(Y=q^d\)와 source cutoff가 실제로 겹치는지

를 먼저 확인한다. 이 네 조건 전에는 threshold calculator나 새 prime sweep을 만들지 않는다.

## 12. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468),
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1).
- P. Dusart, *Estimates of some functions over primes without R.H.*,
  [arXiv:1002.0442](https://arxiv.org/abs/1002.0442).
- H. Davenport and P. Erdos, *The distribution of quadratic and higher residues*,
  Publicationes Mathematicae Debrecen 2 (1952), 252--265.
- J. B. Friedlander and D. A. Goldston,
  *Variance of distribution of primes in residue classes*,
  [doi:10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
- R. C. Vaughan,
  *On a variance associated with the distribution of primes in arithmetic progressions*,
  [doi:10.1112/plms/82.3.533](https://doi.org/10.1112/plms/82.3.533).
- A. J. Harper,
  *A note on character sums over short moving intervals*,
  [arXiv:2203.09448](https://arxiv.org/abs/2203.09448).
- A. J. Harper,
  *Simple Barban--Davenport--Halberstam type asymptotics for general sequences*,
  [arXiv:2412.19644](https://arxiv.org/abs/2412.19644).
