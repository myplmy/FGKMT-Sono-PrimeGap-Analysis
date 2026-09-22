# Theory 88 — DEP-R09 empty-output·randomized-support capacity 감사

- 상태:
  <code>EMPTY_TAIL_SOURCE_INPUT_NOT_IDENTIFIED /
  RANDOMIZED_SUPPORT_CAPACITY_EXACT /
  NO_EMPTY_TAIL_CAN_RESCUE_ATOM_TIMES_FULL_ENERGY_LARGE_SIEVE_ROUTE</code>
- 선행 정본: Theory 47, 53--55, 82--87, review 96
- 기계 원장:
  [empty-output support-capacity audit v1](data/Sono_FMT_DEPR09_empty_output_support_capacity_audit_v1.json)
- 목표: final-law empty-output/nonempty-count tail이 Theory 87의 atom-cap route를
  충분히 강화할 수 있는지 감사하고, 현재 final residue construction의 전체
  randomized support capacity로 그 가능 범위를 exact하게 고정한다.
- 비목적: local character-phase cancellation, direct correlation, 새로운 residue
  construction, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 배제하거나 인증하는 것.

## 1. 결론

현재 FMT final residue vector에서 무작위로 변할 수 있는 prime coordinate는

1. outer set \({\cal S}\),
2. inner dyadic set \(P'\subset(X/2,X]\)

뿐이다. 나머지 \(p\le X\) 좌표는 residue 0으로 고정된다. 따라서

\[
 Q_P:=\prod_{p\in P'}p,\qquad
 H_{\rm res}:=Q_{\cal S}Q_P
 \tag{88.1}
\]

라 하면 final shift support는

\[
 \boxed{
 \#\operatorname{supp}(m_\omega)\le H_{\rm res}.}
 \tag{88.2}
\]

actual sieve-good event의 질량은 \(p_*>0\) 이상이다. event-and-shift atom을

\[
 \lambda_r:=\Pr(S_{\rm sieve},m_\omega=r)
 \tag{88.3}
\]

라 하면 at most \(H_{\rm res}\)개 atom에

\[
 \sum_r\lambda_r=\Pr(S_{\rm sieve})\ge p_*.
 \tag{88.4}
\]

따라서 finite pigeonhole로

\[
 \boxed{
 \max_r\lambda_r\ge\frac{p_*}{H_{\rm res}}.}
 \tag{88.5}
\]

모든 event atom을 \(\alpha\) 이하로 묶는 어떤 empty-tail theorem도 반드시

\[
 \boxed{
 \frac{p_*}{\alpha}\le H_{\rm res}.}
 \tag{88.6}
\]

를 만족한다. 즉 success mass를 포함한 atom-gate entropy factor는 final shift
support cardinality를 넘을 수 없다.

현재 child에서

\[
 \boxed{
 \log H_{\rm res}<\frac{51}{100}X
 \quad\hbox{반면}\quad
 \log\mathfrak q>\frac{49}{50}X.}
 \tag{88.7}
\]

그러므로 \(H_{\rm res}<\mathfrak q\)다. **모든 inner coordinate가 nonempty이고
그 허용 residue에 가장 유리하게 분산된다는 가정까지 주어도**, empty-output tail만으로
full primorial entropy를 만들 수 없다.

Theory 83의 raw classical large-sieve RHS는 따라서 atom-cap × full-energy
architecture의 best support gate보다도 계속 크다. 이 판정은 local character transform,
weighted phase cancellation 또는 prime-specific direct correlation을 배제하지 않는다.

## 2. source의 final coordinate support

FMT printed p.9의 final extension과 Theory 53의 actual successor는

\[
 a_p^{\rm final}
 =
 \begin{cases}
 A_p,&p\in{\cal S},\\
 N'_p,&p\in P',\\
 0,&p\le X,\ p\notin{\cal S}\cup P'
 \end{cases}
 \tag{88.8}
\]

로 residue vector를 완성한다. exceptional \(B_0\)는 modulus에서 빠지므로 support
factor를 늘리지 않는다.

각 \(s\in{\cal S}\) coordinate는 많아야 \(s\)개, 각 \(p\in P'\) coordinate는
많아야 \(p\)개 값을 가진다. 좌표들이 independent이거나 모든 값이 실제 support에
들어간다고 가정하지 않고 단순 cardinality upper만 취하면 식 (88.2)가 나온다.

empty output을 residue 0으로 lift하는 현재 project rule도 이 support 안에 있다.
empty-output tail은 \(N'_p=0\)의 빈도를 바꿀 수 있지만 새로운 prime coordinate를
추가하지는 못한다.

## 3. checked source에는 uniform empty atom upper가 없다

FGKMT proof law에서 normalizer-good history라면

\[
 \Pr(e'_i=\varnothing\mid W)
 =
 \frac{\mu_i(\varnothing)}{X_i(W)}
 \tag{88.9}
\]

이다. \(P_{j-1}(\varnothing)=1\), \(\varnothing\subset W\)를 썼다. original
empty edge가 support에 없으면 \(\mu_i(\varnothing)=0\)으로 읽는다.

normalizer-bad history에서는 construction이 \(e'_i=\varnothing\)으로 둔다.
Theory 54는 bad history의 unconditional probability를 상계하지만, checked input은
모든 coordinate와 history에 공통인

\[
 \Pr(e'_i=\varnothing\mid\text{past})\le1-\delta_0
 \qquad(\delta_0>0)
 \tag{88.10}
\]

형태를 주지 않는다. actual original empty mass \(\mu_i(\varnothing)\)의 uniform
upper도 없다.

따라서 source에서 numerical empty-count tail을 새로 인증하지 않는다. 그러나
식 (88.7)은 그 tail을 가장 낙관적으로 가정해도 atom/full-energy route에 충분하지
않음을 별도로 보인다.

## 4. event success mass를 보존한 pigeonhole

event atom cap을 사용할 때 \(\Pr(S_{\rm sieve})\)를 1로 바꾸거나 없애면 안 된다.
\({\cal R}\)를 actual shift support라 하면

\[
 p_*
 \le\Pr(S_{\rm sieve})
 =\sum_{r\in{\cal R}}\lambda_r
 \le\#{\cal R}\max_r\lambda_r
 \le H_{\rm res}\max_r\lambda_r.
 \tag{88.11}
\]

따라서 식 (88.5)가 정확하다. equality는 event mass가 \(H_{\rm res}\)개 support
atom에 균등하게 놓일 때 달성 가능하므로, support cardinality만으로는 이 bound를
낮출 수 없다.

\(\lambda_r\le\alpha\)를 증명했다면 식 (88.11)로

\[
 p_*\le H_{\rm res}\alpha
 \quad\Longleftrightarrow\quad
 \frac{p_*}{\alpha}\le H_{\rm res}.
 \tag{88.12}
\]

Theory 87의 specific \(\alpha=\omega_*^{K_*}/Q_{\cal S}\)뿐 아니라 어떤 더 강한
empty-count tail이 주는 atom cap에도 같은 capacity ceiling이 적용된다.

## 5. outer randomized support

\(\ell=\log b\), \(z=X\ell/(4b)\)라 하자. outer product는

\[
 \log Q_{\cal S}\le\vartheta(z)
 <\frac{21}{20}z
 =\frac{21X\ell}{80b}.
 \tag{88.13}
\]

기존 \(b>2000\)에서 \(\ell/b<1/200\)이므로

\[
 \boxed{
 \log Q_{\cal S}<\frac{21}{16000}X.}
 \tag{88.14}
\]

이 upper는 outer coordinate가 모두 uniform하고 full support를 가진다고 허용한
가장 유리한 cardinality bound다.

## 6. inner randomized support

Theory 47 식 (47.13)은

\[
 P_o:=\pi(X)-\pi(X/2),\qquad
 P_0:=\frac{X}{2a},\qquad
 \left|\frac{P_o}{P_0}-1\right|\le\frac3a.
 \tag{88.15}
\]

를 준다. \(P'\)는 이 interval에서 \(B_0\)를 뺀 subset이므로

\[
 \#P'
 \le P_o
 \le\left(1+\frac3a\right)\frac{X}{2a}.
 \tag{88.16}
\]

기존 \(a\ge1000\)에서

\[
 \#P'\le\frac{1003X}{2000a}.
 \tag{88.17}
\]

모든 \(p\in P'\)에서 \(\log p\le a\)이므로

\[
 \boxed{
 \log Q_P
 =\sum_{p\in P'}\log p
 \le a\,\#P'
 \le\frac{1003}{2000}X.}
 \tag{88.18}
\]

이는 every inner coordinate가 \(p\)개 residue를 모두 사용할 수 있다고 허용한
support upper다. empty-output probability나 nonempty-count tail은 이보다 support를
늘릴 수 없다.

## 7. support capacity와 full primorial 비교

식 (88.14), (88.18)을 합치면

\[
 \begin{aligned}
 \frac{\log H_{\rm res}}X
 &<
 \frac{21}{16000}+\frac{1003}{2000}\\
 &=\frac{1609}{3200}
 <\frac{51}{100}.
 \end{aligned}
 \tag{88.19}
\]

Theory 87의 Dusart lower를 재사용하면

\[
 \log\mathfrak q>\frac{49}{50}X.
 \tag{88.20}
\]

따라서

\[
 \boxed{
 H_{\rm res}<\mathfrak q.}
 \tag{88.21}
\]

차이는 단순 constant polishing 문제가 아니다. current construction은
중간 prime range의 대부분을 residue 0으로 고정하므로 randomized-coordinate
support 자체가 full primorial dimension보다 작다.

## 8. atom-cap × full-energy architecture의 최선 gate

어떤 event atom cap \(\alpha\)를 사용해

\[
 \rho_S
 \le
 \alpha\sum_{r\bmod\mathfrak q}|R(r)|^2
 \le
 \alpha\varphi(\mathfrak q)N^2V(Y,\mathfrak q)
 \tag{88.22}
\]

를 얻었다고 하자. Theory 81의 positive-mass gate에 충분한 \(V\) upper는

\[
 V_{\rm gate}(\alpha)
 :=
 \tau^2\frac{p_*}{\alpha}
 \frac{M_{\min}^2Y^2}{\varphi(\mathfrak q)N^2}.
 \tag{88.23}
\]

식 (88.6), \(0<\tau\le e^{-2}\), \(M_{\min}\le N\)으로

\[
 \frac{V_{\rm gate}(\alpha)}{Y^2}
 \le
 e^{-4}\frac{H_{\rm res}}{\varphi(\mathfrak q)}
 <
 e^{-4}\frac{\mathfrak q}{\varphi(\mathfrak q)}.
 \tag{88.24}
\]

Theory 83의 source-derived certificate는

\[
 \frac{B_{\rm LS}(Y,\mathfrak q)}{Y^2}
 >
 e^{-4}\frac{\mathfrak q}{\varphi(\mathfrak q)}.
 \tag{88.25}
\]

따라서

\[
 \boxed{
 B_{\rm LS}(Y,\mathfrak q)>V_{\rm gate}(\alpha)}
 \tag{88.26}
\]

이다. 즉 **어떤 empty-output/nonempty-count tail도**, atom cap을 full residue
energy 앞에 곱하는 이 architecture 안에서는 raw classical large-sieve RHS를 strict
gate 아래로 내릴 수 없다.

## 9. 판정의 정확한 범위

식 (88.26)이 배제하는 것은 다음 조합이다.

1. current final residue support,
2. event 최대 atom 하나,
3. full residue \(L^2\) energy,
4. raw classical large-sieve RHS.

배제하지 않는 것은 다음과 같다.

1. \(\lambda_r\)와 \(|R(r)|^2\)의 직접 negative correlation,
2. formula (5.9)의 local Dirichlet-character transform,
3. support-restricted prime-specific energy,
4. fixed coordinates를 새로 randomize하는 별도 construction 변경,
5. pointwise PAP 또는 다른 analytic proof architecture.

특히 support가 작다는 사실만으로 weighted observable이 나쁘다고 결론내리지 않는다.
다음 proof package는 support cardinality가 아니라 phase를 직접 사용해야 한다.

## 10. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 |
|---|---|
| final randomized coordinate set | <code>SOURCE VERIFIED</code> |
| full shift support cardinality upper | <code>EXACT</code> |
| success-event pigeonhole atom lower | <code>EXACT FINITE</code> |
| best atom-gate entropy factor | <code>EXACT FINITE</code> |
| randomized support log upper | <code>PARAMETERIZED EXPLICIT</code> |
| full primorial과 strict separation | <code>PARAMETERIZED EXPLICIT</code> |
| numerical empty-output tail | <code>NOT IDENTIFIED</code> |
| any empty tail + atom/full-energy/raw-LS route | <code>INSUFFICIENT ARCHITECTURE</code> |
| local character phase·direct correlation | <code>OPEN</code> |
| actual same-law analytic moment | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 11. 검증 범위

<code>source/dep_r09_empty_output_support_capacity_audit.py</code>와 단위시험은 exact
<code>Fraction</code>으로 다음을 검사한다.

1. disjoint randomized coordinate moduli의 support product.
2. event mass \(3/5\), support 210에서 max joint atom \(1/350\)의 pigeonhole.
3. equality atom cap에서 \(p_*/\alpha=210\)인 support ceiling.
4. looser atom cap이 entropy factor를 180으로 낮추는 strict 방향.
5. outer \(21/16000\), inner \(1003/2000\), total
   \(1609/3200<51/100<49/50\)의 exact rational arithmetic.
6. source hash와 모든 OPEN status의 fail-closed ledger.

Lean은 success-mass pigeonhole premise에서 entropy factor로 가는 scalar division,
rational support coefficient, support/full-primorial hierarchy와 large-sieve barrier
terminal만 검사한다. finite support enumeration, prime-count source theorem,
theta theorem과 analytic character energy를 local axiom으로 넣지 않는다.

canonical Python 회귀시험 143개, Lean direct compile과 full build가 PASS했다.
전수 refresh·validation은 theory 문서 89개, display 식 1,705개, Lean declaration
320개, 금지 proof escape 0건이다. 상태는
<code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=94</code>,
<code>DEFINITION_ONLY=138</code>, <code>PARTIAL_FORMALIZATION=146</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=135</code>,
<code>NOT_YET_FORMALIZED=1089</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.

## 12. 다음 gate

empty-output tail은 이 architecture의 다음 gate에서 제거된다. 다음 우선순위는
formula (5.9)의 reweighted local Dirichlet-character transform 또는 동등한
direct phase-correlation mechanism이다.

그 경로가 source에서 닫히지 않으면 prime-specific support-restricted fiber upper로
이동한다. fixed coordinates를 새로 randomize하는 것은 current proof의 단순 보조정리가
아니라 construction 변경이므로 별도 영향도·사용자 승인 없이 자동 착수하지 않는다.

## 13. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468),
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, JAMS 31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
