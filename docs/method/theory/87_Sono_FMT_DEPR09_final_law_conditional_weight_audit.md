# Theory 87 — DEP-R09 final-law conditional-weight source 감사

- 상태:
  <code>PROOF_LAW_NONEMPTY_ATOM_CAP_EXPLICIT /
  SUCCESS_FORCED_INNER_ENTROPY_EXACT /
  GUARANTEED_ENTROPY_SUBPRIMORIAL_AND_GENERIC_LARGE_SIEVE_STILL_INSUFFICIENT</code>
- 선행 정본: Theory 53--55, Theory 81--86, review 95
- 기계 원장:
  [final-law conditional-weight audit v1](data/Sono_FMT_DEPR09_final_law_conditional_weight_audit_v1.json)
- 목표: FGKMT Theorem 3의 결론만이 아니라 proof-constructed law (5.9)를 사용해
  final nonempty residue 좌표의 atom cap을 복원하고, covering 성공이 강제하는
  nonempty 좌표 수와 합성해 actual same-law shift atom cap을 정량화한다.
- 비목적: 모든 final 좌표의 global independence, empty-output tail, actual character
  phase cancellation, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

## 1. 결론

Theory 53--55의 actual child 표기를 쓴다.

\[
 a=\log X,\qquad b=\log a,\qquad
 k=\left\lfloor(\log(X/2))^{1/5}\right\rfloor,\qquad
 \kappa=\frac9{10}5^{-m}.
 \tag{87.1}
\]

FGKMT proof law와 Theory 54의 normalizer floor를 합치면 한 nonempty final
full-residue edge의 conditional atom은

\[
 \boxed{
 \omega_*:=2\kappa^{-2k}X^{-3/5}<1}
 \tag{87.2}
\]

이하이다. 이 bound는 complete past history를 조건으로 한 bound다.

retained whole-set vertex 수의 공통 floor와 covering-good survivor bound를

\[
 M_*:=\frac Xa\left(79cb-\frac2b\right),\qquad
 \gamma:=1-(1+t)\rho,\qquad
 K_*:=\left\lceil\frac{\gamma M_*}{2k}\right\rceil
 \tag{87.3}
\]

로 둔다. 여기서 \(\rho=5^{-m}\), \(t=\eta/8\). 기존 gate에서
\(m\ge1\), \(0<\eta\le1/4\)이므로 \(\gamma\ge127/160>0\)이다.
Theory 53 식 (53.9)의 같은 child bounds는 \(M_*>0\)도 보장한다.

actual sieve-good event에서는 적어도 \(K_*\)개의 output edge가 nonempty다. 따라서
모든 final CRT shift \(r\bmod\mathfrak q\)에

\[
 \boxed{
 \Pr(S_{\rm sieve},m_\omega=r)
 \le
 \frac{\omega_*^{K_*}}{Q_{\cal S}}.}
 \tag{87.4}
\]

가 성립한다. effective atom denominator를

\[
 Q_{\rm eff}:=Q_{\cal S}\omega_*^{-K_*}
 \tag{87.5}
\]

라 하면 Theory 82의 full energy와 합쳐

\[
 \rho_S
 \le
 \frac{\varphi(\mathfrak q)N^2}{Q_{\rm eff}}V(Y,\mathfrak q).
 \tag{87.6}
\]

따라서 새 sufficient character-energy gate는

\[
 \boxed{
 V(Y,\mathfrak q)
 <
 \tau^2p_*
 \frac{Q_{\rm eff}M_{\min}^2Y^2}
 {\varphi(\mathfrak q)N^2}.}
 \tag{87.7}
\]

이다. 이는 Theory 82 gate를 \(\omega_*^{-K_*}\)배 완화한 exact same-law
reduction이다.

그러나 project child 전체에서 보장되는 entropy만 쓰면

\[
 \boxed{
 \log Q_{\rm eff}<\frac X{100}
 \quad\hbox{반면}\quad
 \log\mathfrak q>\frac{49}{50}X.}
 \tag{87.8}
\]

따라서 \(Q_{\rm eff}<\mathfrak q\)이고, Theory 83의 raw classical large-sieve
certificate는 새 gate보다도 계속 크다. 즉 conditional weight에서 실제 진전은
있지만 **guaranteed minimum-count entropy만으로 actual same-law analytic moment를
닫지는 못한다**.

## 2. theorem conclusion이 아니라 proof-constructed law를 선택

FGKMT Theorem 3의 statement는 output edge들의 support와 fixed-set survival
probability만 선언한다. 이번 감사는 그 결론을 만족하는 모든 law가 식 (87.2)를
가진다고 주장하지 않는다.

대신 printed pp.83--89의 induction proof가 실제로 구성한 law를 선택한다. stage
\(I_j\) 직전의 survivor set을 \(W\), original marginal edge law를
\(\mu_i(E)=\Pr(e_i=E)\), 이전 survival product를 \(P_{j-1}(E)\)라 하면

\[
 X_i(W)
 :=
 \sum_E
 \mu_i(E)\frac{1_{\{E\subset W\}}}{P_{j-1}(E)}.
 \tag{87.9}
\]

Theory 54의 quantitative reproof는 good-normalizer event에서

\[
 X_i(W)\ge\frac12
 \tag{87.10}
\]

를 준다. 이 event에서 proof law는

\[
 \Pr(e'_i=E\mid W)
 =
 \frac{\mu_i(E)1_{\{E\subset W\}}}
 {X_i(W)P_{j-1}(E)}.
 \tag{87.11}
\]

bad-normalizer event에서는 \(e'_i=\varnothing\)이다. 한 stage 안의 \(e'_i\)들은
\(W\)를 조건으로 jointly independent하다. 앞 stage의 결과가 \(W\)를 바꾸므로
전체 final 좌표가 globally independent라고 하지 않는다.

## 3. nonempty edge atom cap

actual full-residue edge cap은

\[
 |E|\le r_{\rm hg}=2k.
 \tag{87.12}
\]

Theory 53의 recursion에서 모든 vertex survival profile은 \(\kappa\) 이상이므로

\[
 P_{j-1}(E)=\prod_{v\in E}P_{j-1}(v)
 \ge\kappa^{|E|}
 \ge\kappa^{2k}.
 \tag{87.13}
\]

nonempty \(E\)에서 \(v\in E\) 하나를 고르면

\[
 \mu_i(E)
 \le\Pr(v\in e_i)
 \le X^{-3/5}.
 \tag{87.14}
\]

첫 부등식은 \(\{e_i=E\}\subseteq\{v\in e_i\}\), 둘째는 Theory 53 식
(53.10)의 actual full-residue sparsity다. 식 (87.10)--(87.14)를 합치면

\[
 \Pr(e'_i=E\mid W)
 \le2\kappa^{-2k}X^{-3/5}
 =\omega_*
 \tag{87.15}
\]

이다. \(E\ne\varnothing\)이면 bad-normalizer branch에서는 선택확률이 0이므로
식 (87.15)는 모든 history에서 성립한다.

## 4. adaptive multistage law의 vector atom

fixed complete output edge vector \(\mathbf E=(E_i)\)를 잡고 stage \(j\) 안의
nonempty 좌표 수를 \(K_j\)라 하자. complete past를 조건으로 하면 stage 안에서
product law이므로

\[
 \Pr((e'_i)_{i\in I_j}=(E_i)_{i\in I_j}\mid\text{past})
 \le\omega_*^{K_j}.
 \tag{87.16}
\]

stage별 conditional probability를 chain rule로 곱하면

\[
 \Pr(\mathbf e'=\mathbf E\mid\mathbf A=\boldsymbol a)
 \le\omega_*^K,\qquad K:=\sum_jK_j.
 \tag{87.17}
\]

이다. 식 (87.17)은 global independence를 사용하지 않는다. empty coordinate의
conditional atom은 1로만 묶었으므로 empty-output probability에 대한 숨은 가정도 없다.

## 5. output edge에서 actual residue로의 injective lift

Theory 53은 nonempty output edge마다 fixed witness \(n'_p\)를 고르고 empty output에는
\(n'_p=0\)을 둔다. retained vertex set \(V\) 위에서

\[
 e'_p=\{q\in V:q\equiv n'_p\pmod p\}.
 \tag{87.18}
\]

nonempty edge는 포함한 아무 \(q\) 하나로 \(n'_p\bmod p=q\bmod p\)를 유일하게
결정한다. 또 \(q>p\)인 prime vertex이므로 residue 0의 edge는 empty다. 따라서
fixed \(\mathbf A=\boldsymbol a\)에서 final CRT shift가 정해지면 output edge vector도
유일하게 정해진다.

이 injectivity가 없으면 edge atom을 shift atom으로 옮길 수 없다. 이번 전달은
Theorem 3의 abstract support containment만이 아니라 Theory 53의 full-residue
equality (53.22)를 사용한다.

## 6. covering 성공이 강제하는 nonempty 좌표 수

Theory 53 식 (53.9)와 exception count로 retained whole-set 크기 \(M=|V|\)는

\[
 M\ge
 79c\frac{Xb}{a}-\frac{2X}{ab}
 =M_*.
 \tag{87.19}
\]

Theory 55의 inner-good event에는 whole-set fixed subset도 포함된다. 그 uncovered
count를 \(Z\)라 하면

\[
 Z\le(1+t)\rho M.
 \tag{87.20}
\]

따라서 output union이 덮은 vertex는 적어도 \(\gamma M\)개다. nonempty edge 하나의
크기는 \(2k\) 이하이므로, nonempty output 수 \(K\)는

\[
 2kK\ge M-Z\ge\gamma M\ge\gamma M_*.
 \tag{87.21}
\]

를 만족한다. \(K\)가 정수이므로

\[
 K\ge
 \left\lceil\frac{\gamma M_*}{2k}\right\rceil
 =K_*.
 \tag{87.22}
\]

\(m\ge1\), \(\rho\le1/5\), \(t\le1/32\)에서

\[
 \gamma
 =1-(1+t)\rho
 \ge1-\frac{33}{32}\frac15
 =\frac{127}{160}.
 \tag{87.23}
\]

식 (87.17), (87.22)와 \(0<\omega_*<1\)을 합치면 inner-good event 위의 fixed
shift conditional atom은 \(\omega_*^{K_*}\) 이하이다. outer vector의 질량
\(Q_{\cal S}^{-1}\)을 곱하면 식 (87.4)가 나온다.

## 7. same-law raw moment와 strict gate

이 절의 \(N\)은 Theory 82의 fixed offset interval 크기이며, §6의 retained
hypergraph vertex 수 \(M\)과 다른 변수다.

Theory 86과 같은 event-and-shift 합을 쓰면

\[
 \rho_S
 =
 \sum_{r\bmod\mathfrak q}
 \Pr(S_{\rm sieve},m_\omega=r)|R(r)|^2
 \le
 \frac{\omega_*^{K_*}}{Q_{\cal S}}
 \sum_{r\bmod\mathfrak q}|R(r)|^2.
 \tag{87.24}
\]

Theory 82의 full-energy upper

\[
 \sum_{r\bmod\mathfrak q}|R(r)|^2
 \le\varphi(\mathfrak q)N^2V(Y,\mathfrak q)
 \tag{87.25}
\]

와 식 (87.5)를 넣으면 식 (87.6)이 나온다. Theory 81의 same-event survivor floor로

\[
 \mu_S
 \le
 \frac{\varphi(\mathfrak q)N^2}
 {Q_{\rm eff}M_{\min}^2Y^2}V(Y,\mathfrak q).
 \tag{87.26}
\]

따라서 식 (87.7)이면 strict하게

\[
 \mu_S<\tau^2p_*.
 \tag{87.27}
\]

equality boundary는 positive remaining mass를 보장하지 않으므로 strict 부등호를
유지한다.

## 8. coordinate cap은 실제로 1보다 작다

Theory 54의

\[
 t_0:=\Delta^{1/10^{m+2}}\le\frac1{100},\qquad
 \kappa^{-2k}\le t_0^{-1},\qquad
 \Delta=X^{-1/20}
 \tag{87.28}
\]

를 쓴다. \(X^{-3/5}=\Delta^{12}=t_0^{12\cdot10^{m+2}}\)이고 \(m\ge1\)이므로

\[
 \omega_*
 \le
 2t_0^{12\cdot10^{m+2}-1}
 \le2t_0^{11999}
 <1.
 \tag{87.29}
\]

이 검사는 실제 거대 \(X\)를 평가하지 않는 all-parameter 부등식이다.

## 9. guaranteed effective entropy의 크기

\(\ell:=\log b\)라 두면 outer-prime endpoint는 \(z=X\ell/(4b)\)다.
Rosser--Schoenfeld theta upper로

\[
 \log Q_{\cal S}
 \le\vartheta(z)
 <\frac{21}{20}z
 =\frac{21X\ell}{80b}.
 \tag{87.30}
\]

\(\gamma\le1\), \(\lceil u\rceil\le u+1\), \(M_*\le79cXb/a\)로

\[
 K_*
 \le\frac{79cXb}{2ak}+1.
 \tag{87.31}
\]

식 (87.2)에서

\[
 \log(1/\omega_*)
 =
 \frac{3a}{5}-\log2-2k\log(1/\kappa)
 <\frac{3a}{5}.
 \tag{87.32}
\]

따라서

\[
 K_*\log(1/\omega_*)
 <
 \frac{237cXb}{10k}+\frac{3a}{5}.
 \tag{87.33}
\]

기존 child \(b>2000\)에서 다음 elementary bounds를 쓸 수 있다.

\[
 \frac{\ell}{b}<\frac1{200},\qquad
 c<\frac1{153600},\qquad
 \frac bk\le1,\qquad
 \frac aX<\frac1{100}.
 \tag{87.34}
\]

첫 식은 \(b/200-\log b\)의 단조성과 \(e^8>2000\), 셋째는
\(k>\tfrac14e^{b/5}>b\), 넷째는 \(e^a>100a\)에서 따른다. 모두 기존
child보다 훨씬 약한 조건이다.

식 (87.30), (87.33)--(87.34)를 합치면

\[
 \begin{aligned}
 \frac{\log Q_{\rm eff}}X
 &<
 \frac{21}{16000}
 +\frac{237}{1536000}
 +\frac3{500}\\
 &=\frac{3823}{512000}
 <\frac1{100}.
 \end{aligned}
 \tag{87.35}
\]

반면 \(\mathfrak q=P(X)/B_0\), \(\log B_0\le a\)이고 Dusart theta lower로

\[
 \log\mathfrak q
 >
 X\left(1-\frac{12323}{10000a}\right)-a.
 \tag{87.36}
\]

기존 child에서 \(12323/(10000a)<1/100\), \(a/X<1/100\)이므로

\[
 \log\mathfrak q>\frac{49}{50}X.
 \tag{87.37}
\]

식 (87.35)--(87.37)이 식 (87.8)을 준다.

## 10. generic large-sieve certificate는 여전히 gate 위

식 (87.7)의 RHS를 \(V_{\rm gate,87}\)라 하자. Theory 83과 같은 favorable
factor bounds

\[
 0<\tau\le e^{-2},\qquad
 0<p_*\le1,\qquad
 M_{\min}\le N
 \tag{87.38}
\]

로

\[
 \frac{V_{\rm gate,87}}{Y^2}
 \le
 e^{-4}\frac{Q_{\rm eff}}{\varphi(\mathfrak q)}
 <
 e^{-4}\frac{\mathfrak q}{\varphi(\mathfrak q)}.
 \tag{87.39}
\]

Theory 83의 source-derived large-sieve certificate는

\[
 \frac{B_{\rm LS}(Y,\mathfrak q)}{Y^2}
 >
 e^{-4}\frac{\mathfrak q}{\varphi(\mathfrak q)}.
 \tag{87.40}
\]

따라서

\[
 \boxed{
 B_{\rm LS}(Y,\mathfrak q)>V_{\rm gate,87}.}
 \tag{87.41}
\]

즉 \(V\le B_{\rm LS}\) 하나만으로 strict 식 (87.7)을 도출할 수 없다. 이는
actual \(V\)의 하한이 아니며, actual nonempty count가 \(K_*\)보다 훨씬 크거나
empty-output tail·local phase cancellation을 쓰는 강화의 불가능성도 아니다.

## 11. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 |
|---|---|
| FGKMT proof law (5.9) locator·quantifier | <code>SOURCE VERIFIED</code> |
| nonempty output edge conditional atom cap | <code>ACTUAL INPUTS PARAMETERIZED EXPLICIT</code> |
| multistage chain without global independence | <code>EXACT FINITE</code> |
| full-residue edge에서 final residue lift | <code>PROJECT EXPLICIT</code> |
| covering-success nonempty-coordinate floor | <code>EXACT</code> |
| same-law event-and-shift atom cap | <code>ACTUAL INPUTS PARAMETERIZED EXPLICIT</code> |
| guaranteed effective entropy \(Q_{\rm eff}\) | <code>PARAMETERIZED EXPLICIT</code> |
| minimum-count entropy + raw large sieve | <code>INSUFFICIENT CERTIFICATE</code> |
| empty-output numerical tail | <code>OPEN</code> |
| reweighted local character transform·phase moment | <code>OPEN</code> |
| prime-specific fiber upper | <code>OPEN</code> |
| actual same-law analytic moment | <code>OPEN</code> |
| PAP-11·DEP-R09, fixed coefficient, \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 12. 검증 범위

<code>source/dep_r09_final_law_conditional_weight_audit.py</code>와 단위시험은 exact
<code>Fraction</code>으로 다음을 검사한다.

1. formula (5.9)형 reweighted atom과 \(2\kappa^{-r}\mu(E)\) cap.
2. history별 conditional probability의 chain-rule 곱과 nonempty cap power.
3. covered vertex 수에서 필요한 nonempty edge 수의 ceiling.
4. nonempty full-residue edge의 residue uniqueness와 empty-to-zero rule.
5. toy의 reweighted atom \(2/9\), cap \(1/3\), \(K_*=4\), event-shift cap
   \(1/486\), effective denominator \(486\).
6. 식 (87.35)의 rational coefficient \(3823/512000<1/100\).
7. source hash와 모든 OPEN status의 fail-closed ledger.

Lean은 reweighted atom terminal, effective-atom raw-moment 합성, strict gate와
subprimorial barrier의 scalar implication만 검사한다. source probability law,
ceil count, real logarithm·theta theorem 또는 analytic character energy를
project-local axiom으로 넣지 않는다.

canonical Python 회귀시험 116개, Lean direct compile과 full build가 PASS했다.
전수 refresh·validation은 theory 문서 88개, display 식 1,675개, Lean declaration
315개, 금지 proof escape 0건이다. 상태는
<code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=89</code>,
<code>DEFINITION_ONLY=135</code>, <code>PARTIAL_FORMALIZATION=141</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=127</code>,
<code>NOT_YET_FORMALIZED=1080</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.

## 13. 다음 gate

다음 우선순위는 guaranteed minimum \(K_*\)보다 더 많은 actual law 정보를 쓰는 것이다.

1. proof law에서 empty output 수 또는 nonempty output 수의 numerical tail을 얻을 수
   있는지 감사한다.
2. 각 stage의 reweighted residue law에 local Dirichlet-character transform을 적용해
   phase moment를 직접 묶을 수 있는지 본다.
3. 둘 다 source에서 닫히지 않으면 prime-specific support-restricted fiber upper로
   이동한다.

이 중 하나가 full-primorial entropy 또는 직접 cancellation을 공급하기 전에는
threshold calculator나 장시간 prime 계산을 시작하지 않는다.

## 14. 참고문헌

- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, JAMS 31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468),
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1).
