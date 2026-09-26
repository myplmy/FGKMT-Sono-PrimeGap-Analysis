# Theory 89 — DEP-R09 reweighted local Dirichlet-character transform 감사

- 상태:
  <code>EXACT_STAGE_LOCAL_TRANSFORM /
  ATOM_CAP_FOURIER_SAVING_REJECTED /
  BLIND_CHARACTER_COEFFICIENT_ENERGY_EXACT_AND_PRIME_ERROR_CORRELATION_OPEN</code>
- 선행 정본: Theory 47, 53--54, 77, 80--88, review 97
- 기계 원장:
  [local character-transform audit v1](data/Sono_FMT_DEPR09_local_character_transform_audit_v1.json)
- 목표: FGKMT formula (5.9)의 actual witness law에 대한 local character transform을
  정확히 쓰고, 적용 가능한 선행정리와 randomized-coordinate transform이 보지 못하는
  character family를 분리한다.
- 비목적: actual local transform saving을 가정하거나, blind prime-error correlation,
  PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\)를 이번
  단계에서 인증하는 것.

## 1. 결론

fixed stage history \(W\), inner prime \(p\), offset \(u\)와 local character
\(\xi\bmod p\)를 고정한다. output edge \(E\)가 나타내는 residue를
\(a_p(E)\)라 하고 \(a_p(\varnothing)=0\)으로 둔다. exact local transform은

\[
 {\cal L}_{p,W,u}(\xi)
 :=
 \sum_E
 \Pr(e'_p=E\mid W)
 \overline{\xi(u-a_p(E))}.
 \tag{89.1}
\]

normalizer-good history에서는 FGKMT formula (5.9)로

\[
 \boxed{
 {\cal L}_{p,W,u}(\xi)
 =
 \frac1{X_p(W)}
 \sum_E
 \frac{\mu_p(E)1_{\{E\subset W\}}}{P_{j-1}(E)}
 \overline{\xi(u-a_p(E))}.}
 \tag{89.2}
\]

bad history에서는 \(e'_p=\varnothing\)이므로

\[
 {\cal L}_{p,W,u}(\xi)=\overline{\xi(u)}.
 \tag{89.3}
\]

같은 stage의 output들은 \(W\) 조건부로 independent이므로

\[
 \mathbb E\!\left[
 \prod_{p\in I_j}\overline{\xi_p(u-a_p(e'_p))}
 \,\middle|\,W
 \right]
 =
 \prod_{p\in I_j}{\cal L}_{p,W,u}(\xi_p).
 \tag{89.4}
\]

이는 exact identity다. 그러나 atom cap만으로
\(|{\cal L}_{p,W,u}(\xi)|<1\)인 uniform saving은 나오지 않는다.

더 근본적으로, randomized prime product를 \(h\), fixed-coordinate product를 \(f\)라
하면

\[
 h=Q_{\cal S}\prod_{p\in P'}p,\qquad
 f=\frac{\mathfrak q}{h},\qquad
 (f,h)=1.
 \tag{89.5}
\]

모든 outcome에서 \(m_\omega\equiv0\pmod f\)다. randomized coordinates에서
주지표인 character family

\[
 {\cal B}
 :=
 \{\widetilde\psi=\psi\bmod f\ \otimes\ \chi_{0,h}:
 \psi\bmod f\}
 \tag{89.6}
\]

는 \(\varphi(f)\)개다. final survivor set을 \(T_\omega\), 크기를 \(M_\omega\)라 하면

\[
 \boxed{
 C_{\widetilde\psi}(\omega)
 =
 \sum_{s\in T_\omega}\overline{\psi(s)}.}
 \tag{89.7}
\]

offset interval은 \(f\)보다 짧으므로 fixed-modulus character orthogonality가
outcome마다

\[
 \boxed{
 \sum_{\psi\bmod f}|C_{\widetilde\psi}(\omega)|^2
 =
 \varphi(f)M_\omega,}
 \tag{89.8}
\]

\[
 \boxed{
 \sum_{\substack{\psi\bmod f\\\psi\ne\psi_0}}
 |C_{\widetilde\psi}(\omega)|^2
 =
 M_\omega\{\varphi(f)-M_\omega\}.}
 \tag{89.9}
\]

를 준다. 따라서 randomized-coordinate local transform은 이 blind family의
**unweighted total coefficient energy**를 줄이지 않는다. 남은 입력은 blind
coefficient와 actual prime-error vector의 direct correlation이다.

## 2. proof-law local transform의 정확한 범위

original edge marginal을 \(\mu_p(E)=\Pr(e_p=E)\), prior survival product를
\(P_{j-1}(E)\), formula (5.7)의 normalizer를 \(X_p(W)\)라 한다.
Theory 53의 full-residue equality 때문에 nonempty edge \(E\)는 residue
\(a_p(E)\)를 유일하게 결정한다.

normalizer-good event에서 formula (5.9)는

\[
 \Pr(e'_p=E\mid W)
 =
 \frac{\mu_p(E)1_{\{E\subset W\}}}
 {X_p(W)P_{j-1}(E)}.
 \tag{89.10}
\]

식 (89.10)을 local phase에 대입한 것이 식 (89.2)다. bad event의 empty fallback도
식 (89.3)에 포함했으므로 0으로 나누거나 good-history formula를 bad history로
확대하지 않는다.

식 (89.4)는 한 stage 안에서만 product다. 이전 stage output이 다음 \(W\)와
\({\cal L}\) 자체를 바꾸므로

\[
 \mathbb E\prod_{p\in P'}(\cdots)
 \ne
 \prod_{p\in P'}\mathbb E(\cdots)
 \tag{89.11}
\]

를 일반적으로 가정하지 않는다.

## 3. 작은 atom은 Fourier saving을 보장하지 않는다

\(\xi=(\frac{\cdot}{11})\)을 quadratic character modulo 11로 두고 \(u=0\)으로
고정한다. level set

\[
 A:=\{a\bmod11:\xi(-a)=1\}
 =\{2,6,7,8,10\}
 \tag{89.12}
\]

에 균등한 law \(\nu(a)=1/5\)를 둔다. 그러면

\[
 \max_a\nu(a)=\frac15,
 \qquad
 \sum_{a\bmod11}\nu(a)\xi(-a)=1.
 \tag{89.13}
\]

즉 max atom이 작아도 nonprincipal multiplicative-character transform은
modulus 1일 수 있다. 큰 \(p\equiv3\pmod4\)의 같은 level-set construction에서는
max atom이 \(2/(p-1)\)로 작아져도 transform은 계속 1이다.

이 finite witness는 actual formula (5.9) law가 이런 level set이라는 주장이 아니다.
Theory 87의 atom cap과 support cardinality만으로 Fourier saving을 추론하는 논리가
성립하지 않음을 보인다.

## 4. 선행문헌 감사

표적 primary-source 검색에서 가장 가까운 자료는 Granville--Koukoulopoulos--Maynard,
*Sieve weights and their smoothings*, Theorem 1.5다. 원문 PDF 85쪽의 SHA-256은

~~~text
67feecce65ced4250aa046d6e0c36300744eb84358d21d53409a512d1649e34d
~~~

이다. printed pp.10--11와 Sections 11--12를 native text와 rendered page로 대조했다.

그 정리의 대상은 real nonprincipal character \(\chi\bmod q\)에 대한

\[
 {\cal X}_{2r}(R)
 =
 \prod_{\ell\le R}\left(1-\frac1\ell\right)
 \sum_{P^+(n)\le R}\frac1n
 \left(
 \sum_{\substack{d\mid n\\R/2<d\le R}}\chi(d)
 \right)^{2r}.
 \tag{89.14}
\]

즉 **한 개의 truncated Möbius-type divisor sum의 moment**다. 현재 대상은

1. growing \(k=\lfloor(\log(X/2))^{1/5}\rfloor\),
2. multidimensional Maynard square weight \(w(p,n)\),
3. full-residue edge projection,
4. prior survivor \(W\)에 따른 hypergraph reweighting

을 동시에 가진다.

GKM implied constants는 fixed moment order에 의존한다. exceptional-zero branch는

\[
 e^{(\log q)^C}\le R\le e^{1/(1-\beta)}
 \tag{89.15}
\]

를 요구한다. actual local modulus는 \(p\asymp X\), sieve scale은
\(R\asymp X^{1/9}\)이고 dimension은 \(X\)와 함께 증가하므로 scope가 맞지 않는다.
nonexceptional branch도 actual multidimensional/reweighted law와 numerical
growing-\(k\) constant를 제공하지 않는다.

Maynard의 large-moduli I--III는 primes in arithmetic progressions의 modulus averages를
다루며 식 (89.2)의 local hypergraph transform theorem이 아니다. 따라서 checked
primary source에서 numerical drop-in은 식별되지 않았다. 이는 전 문헌 부재나
novelty 주장이 아니다.

## 5. randomized/fixed modulus 분해

Theory 88의 \(h=H_{\rm res}\)는 \({\cal S}\)와 \(P'\) prime product다.
\(\mathfrak q=P(X)/B_0\)는 squarefree이고 \(h\mid\mathfrak q\)이므로 식 (89.5)가
성립한다. final extension은 \(p\mid f\)에서 residue 0을 택하므로

\[
 m_\omega\equiv0\pmod f.
 \tag{89.16}
\]

Theory 88의 scale separation으로

\[
 \log f
 =
 \log\mathfrak q-\log h
 >
 \left(\frac{49}{50}-\frac{51}{100}\right)X
 =
 \frac{47}{100}X.
 \tag{89.17}
\]

actual child \(X\ge10\)에서

\[
 e^{47X/100}>X^2.
 \tag{89.18}
\]

실제로 \(47X/100-2\log X\)는 \(X\ge10\)에서 증가하고 endpoint가 양수다.
한편 final offset interval의 크기 \(N\)은 기존 \(Y<X^2/4\)에서

\[
 N<X^2<f.
 \tag{89.19}
\]

따라서 interval의 서로 다른 두 offset은 modulo \(f\)에서도 서로 다르다.

## 6. blind-character coefficient identity

CRT factorization으로 모든 character modulo \(\mathfrak q=fh\)는 fixed와 randomized
local component의 곱으로 쓸 수 있다. \(\psi\bmod f\)와 principal
\(\chi_{0,h}\)의 곱을 \(\widetilde\psi\)라 하자.

Theory 80의 character를 nonunit에서 0으로 연장한다. 식 (89.16)으로

\[
 \widetilde\psi(m_\omega+s)
 =
 \psi(s)\chi_{0,h}(m_\omega+s).
 \tag{89.20}
\]

\(\psi(s)=0\) iff \((s,f)>1\), principal randomized factor는
\((m_\omega+s,h)>1\)에서 0이다. 따라서 두 factor가 동시에 nonzero인 offset이
정확히 final survivor \(T_\omega\)이고 식 (89.7)이 나온다.

finite character orthogonality는

\[
 \sum_{\psi\bmod f}\overline{\psi(s)}\psi(t)
 =
 \begin{cases}
 \varphi(f),&s\equiv t\pmod f,\ (st,f)=1,\\
 0,&\text{otherwise}.
 \end{cases}
 \tag{89.21}
\]

식 (89.19)로 \(s\equiv t\pmod f\)는 \(s=t\)와 동치다. 식 (89.7)의 square를
전개해 식 (89.8)을 얻는다. principal \(\psi_0\) coefficient는 \(M_\omega\)이므로
그 square \(M_\omega^2\)를 빼면 식 (89.9)가 나온다.

이 identity는 final law를 평균내기 전 **각 outcome마다** 성립한다.

## 7. blind prime-error target

blind nonprincipal prime-error energy를

\[
 V_{\rm blind}(Y;f,h)
 :=
 \sum_{\substack{\psi\bmod f\\\psi\ne\psi_0}}
 |Z_{\widetilde\psi}(Y)|^2
 \tag{89.22}
\]

라 하고 weighted contribution을

\[
 R_{\rm blind}(\omega)
 :=
 \sum_{\substack{\psi\bmod f\\\psi\ne\psi_0}}
 C_{\widetilde\psi}(\omega)Z_{\widetilde\psi}(Y)
 \tag{89.23}
\]

로 둔다. Cauchy--Schwarz와 식 (89.9)는

\[
 \boxed{
 |R_{\rm blind}(\omega)|^2
 \le
 M_\omega\{\varphi(f)-M_\omega\}
 V_{\rm blind}(Y;f,h).}
 \tag{89.24}
\]

총 budget 중 \(\tau_{\rm blind}>0\)을 이 family에 배정한다면 한 pointwise
sufficient condition은

\[
 \boxed{
 V_{\rm blind}(Y;f,h)
 <
 \tau_{\rm blind}^2
 \frac{M_\omega Y^2}{\varphi(f)-M_\omega}.}
 \tag{89.25}
\]

이다. 이 식은 full variance보다 좁은 fixed-coordinate subfamily target이지만
fully numerical source upper는 아직 없다.

Cauchy는 abstract error vector
\(Z_{\widetilde\psi}=c\,\overline{C_{\widetilde\psi}}\)에서 equality를 가지므로
coefficient energy와 unweighted prime-error energy만으로 보편 개선할 수 없다.
actual \(Z\)가 정렬된다고 주장하지 않으며, 바로 그 non-alignment를 증명하는 것이
남은 direct correlation 문제다.

## 8. local transform이 닫는 것과 닫지 못하는 것

nonprincipal component가 randomized modulus \(h\)에 있는 character에는 식 (89.2)가
새 analytic interface를 제공한다. 적합한 twisted Maynard-weight theorem을 얻으면
이 subfamily에는 phase saving이 가능할 수 있다.

하지만 blind family는 모든 randomized local component가 principal이다. 따라서
nonprincipal local-transform saving을 아무리 강하게 증명해도 식 (89.8)--(89.9)의
family는 남는다.

즉 “local transform route가 무의미하다”가 아니라 다음 분해가 필요하다.

1. **nonblind family:** actual reweighted multidimensional transform theorem.
2. **blind family:** \(V_{\rm blind}\) 또는 식 (89.23)의 direct prime-error correlation.

둘 중 하나만 닫아서는 full same-law moment가 닫히지 않는다.

## 9. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 |
|---|---|
| formula (5.9) local transform | <code>EXACT</code> |
| same-stage transform product | <code>EXACT CONDITIONAL</code> |
| global product independence | <code>NOT ASSUMED</code> |
| atom cap에서 Fourier saving | <code>REJECTED / EXACT COUNTEREXAMPLE</code> |
| GKM Theorem 1.5 drop-in | <code>NO: OBJECT·RANGE·GROWING-k MISMATCH</code> |
| applicable numerical multidimensional transform source | <code>NOT IDENTIFIED</code> |
| fixed/randomized modulus split | <code>EXACT</code> |
| blind family size·coefficient energy | <code>EXACT FINITE</code> |
| blind prime-error correlation | <code>OPEN</code> |
| nonblind reweighted transform upper | <code>OPEN</code> |
| actual same-law analytic moment | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 10. 검증 범위

<code>source/dep_r09_local_character_transform_audit.py</code>와 단위시험은 exact
<code>Fraction</code>으로 다음을 검사한다.

1. real-character conditional transform의 finite weighted sum.
2. quadratic level-set law의 max atom \(1/5\)와 transform 1.
3. blind energy \(\varphi(f)M\), principal \(M^2\), nonprincipal
   \(M\{\varphi(f)-M\}\).
4. blind Cauchy sufficient gate의 strict normalization.
5. fixed modulus log coefficient \(47/100\).
6. GKM PDF와 project source hash, 모든 OPEN status의 fail-closed ledger.

Lean은 transform triangle, blind energy subtraction, Cauchy·strict-gate terminal과
fixed-modulus log gap의 scalar implication만 검사한다. formula (5.9) probability law,
finite character orthogonality, GKM analytic theorem과 prime-error estimate를
project-local axiom으로 넣지 않는다.

canonical Python 회귀시험 138개, Lean direct compile과 full build가 PASS했다.
전수 refresh·validation은 theory 문서 90개, display 식 1,733개, Lean declaration
324개, 금지 proof escape 0건이다. 상태는
<code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=97</code>,
<code>DEFINITION_ONLY=143</code>, <code>PARTIAL_FORMALIZATION=149</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=144</code>,
<code>NOT_YET_FORMALIZED=1097</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.

## 11. 다음 gate

다음 우선순위는 blind family의 prime-error correlation이다.

1. \(V_{\rm blind}\)에 적용 가능한 prescribed fixed-modulus/conductor theorem을
   source-first로 감사한다.
2. full energy가 다시 너무 크면 식 (89.23)을 직접 다루는 event-energy correlation을
   조사한다.
3. 병행 가능한 nonblind branch는 actual multidimensional Maynard weight를
   character-twist한 theorem이 필요하다.

이 입력 전에는 threshold calculator나 장시간 prime 계산을 시작하지 않는다.

## 12. 참고문헌

- A. Granville, D. Koukoulopoulos and J. Maynard,
  *Sieve weights and their smoothings*,
  [arXiv:1606.06781](https://arxiv.org/abs/1606.06781).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, JAMS 31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468).
