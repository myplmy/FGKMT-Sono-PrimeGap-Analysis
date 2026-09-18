# Theory 86 — DEP-R09 actual same-law outer-fiber minimax 감사

- 상태:
  <code>ACTUAL_LAW_OUTER_FIBER_REDUCTION_EXACT /
  OUTER_ONLY_MINIMAX_ENVELOPE_SHARP /
  ANALYTIC_FIBER_ENERGY_INPUT_OPEN</code>
- 선행 정본: Theory 79--85, review 87--94
- 기계 원장:
  [same-law outer-fiber minimax v1](data/Sono_FMT_DEPR09_same_law_outer_fiber_minimax_v1.json)
- 목표: 실제 FMT final joint law를 바꾸지 않고 Theory 82의 full residue energy보다
  약한 support-restricted outer-fiber target을 도출하고, outer law와 support만으로
  얻는 보편 상계의 정확한 한계를 고정한다.
- 비목적: actual prime-error fiber bound, final nibble concentration theorem,
  PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\)를 이번
  단계에서 인증하는 것.

## 1. 결론

FMT outer space를

\[
 {\cal A}:=\prod_{s\in{\cal S}}\mathbb Z/s\mathbb Z,
 \qquad |{\cal A}|=Q_{\cal S}:=\prod_{s\in{\cal S}}s
 \tag{86.1}
\]

로 둔다. 각 outer vector \(\boldsymbol a\)를 고정했을 때 final conditional output이
만들 수 있는 CRT shift의 support를 \({\cal M}(\boldsymbol a)\)라 하자. Theory 80--82의
weighted prime-error observable을 \(R(m)\)라 하고

\[
 {\cal H}_{\rm FMT}(R)
 :=
 \sum_{\boldsymbol a\in{\cal A}}
 \max_{m\in{\cal M}(\boldsymbol a)}|R(m)|^2
 \tag{86.2}
\]

로 정의한다. 그러면 actual sieve-good event indicator를 그대로 보존한 raw moment는

\[
 \boxed{
 \rho_S
 :=
 \mathbb E[1_{S_{\rm sieve}}|R(m_\omega)|^2]
 \le
 \frac{{\cal H}_{\rm FMT}(R)}{Q_{\cal S}}.}
 \tag{86.3}
\]

따라서 Theory 81의 \(p_*=(1-F_{\rm out})(1-F_{\rm in})>0\),
\(M_{\min}>0\), \(Y>0\), \(\tau>0\)에 대해 새로운 direct sufficient gate는

\[
 \boxed{
 {\cal H}_{\rm FMT}(R)
 <
 \tau^2p_*Q_{\cal S}M_{\min}^2Y^2.}
 \tag{86.4}
\]

이다. 이 target은 Theory 82의 full character-energy gate보다 약하다. 그러나 actual
\({\cal H}_{\rm FMT}(R)\)를 식 (86.4) 아래로 내리는 numerical analytic theorem은
현재 source에 없다.

또한 각 fiber에서 \(|R|^2\)의 maximizer를 결정론적으로 고르는 abstract conditional
law는 식 (86.3)의 equality를 만든다. 따라서 **uniform outer marginal, conditional
support, 각 fiber의 총질량 1 이하**만 사용하는 보편 논증은 식 (86.3)을 더 낮출 수
없다. 이것은 actual FMT law가 그 최악 law라는 주장이 아니다. actual conditional
weights나 prime-specific 구조를 새로 사용하면 개선 여지는 남는다.

## 2. source law와 conditional support

FMT printed p.12는 각 \(A_s\bmod s\)를 독립 균등하게 고른다. 따라서

\[
 \Pr(\mathbf A=\boldsymbol a)=\frac1{Q_{\cal S}}
 \qquad(\boldsymbol a\in{\cal A}).
 \tag{86.5}
\]

printed p.11은 각 good \(\boldsymbol a\)의 sub-event에서 covering theorem을 조건부
적용해 final \(\mathbf N'\)를 고르고, bad \(\boldsymbol a\)에서는 임의의 fallback을
둔다. 그러므로 actual joint law는

\[
 \Pr(\mathbf A=\boldsymbol a,\mathbf N'=\boldsymbol n)
 =
 \frac1{Q_{\cal S}}
 \Pr(\mathbf N'=\boldsymbol n\mid\mathbf A=\boldsymbol a).
 \tag{86.6}
\]

이다. final CRT shift를 \(m(\boldsymbol a,\boldsymbol n)\)라 쓰고

\[
 {\cal M}(\boldsymbol a)
 :=
 \left\{
 m(\boldsymbol a,\boldsymbol n)\bmod q:
 \boldsymbol n\in
 \operatorname{supp}(\mathbf N'\mid\mathbf A=\boldsymbol a)
 \right\}
 \tag{86.7}
\]

로 둔다. 이 정의는 inner residue 전체를 허용한다고 과장하지 않고 source-defined
conditional support만 사용한다.

final extension은 \(s\in{\cal S}\)에서 \(a_s=A_s\)를 보존하고

\[
 m(\boldsymbol a,\boldsymbol n)\equiv-a_s\pmod s.
 \tag{86.8}
\]

따라서 서로 다른 outer vector의 shift support는 겹치지 않는다.

\[
 \boldsymbol a\ne\boldsymbol b
 \quad\Longrightarrow\quad
 {\cal M}(\boldsymbol a)\cap{\cal M}(\boldsymbol b)=\varnothing.
 \tag{86.9}
\]

## 3. event subprobability와 exact fiber reduction

같은 actual law에서

\[
 \lambda_{\boldsymbol a}(m)
 :=
 \Pr(S_{\rm sieve},m_\omega=m\mid\mathbf A=\boldsymbol a)
 \qquad
 (m\in{\cal M}(\boldsymbol a))
 \tag{86.10}
\]

로 둔다. 이는 probability distribution일 필요가 없는 subprobability이므로

\[
 \lambda_{\boldsymbol a}(m)\ge0,
 \qquad
 \sum_{m\in{\cal M}(\boldsymbol a)}
 \lambda_{\boldsymbol a}(m)\le1.
 \tag{86.11}
\]

식 (86.5)--(86.6)의 tower identity로

\[
 \rho_S
 =
 \frac1{Q_{\cal S}}
 \sum_{\boldsymbol a\in{\cal A}}
 \sum_{m\in{\cal M}(\boldsymbol a)}
 \lambda_{\boldsymbol a}(m)|R(m)|^2.
 \tag{86.12}
\]

각 fiber에서 비음수 weighted average를 maximum으로 묶고 식 (86.11)을 쓰면

\[
 \sum_{m\in{\cal M}(\boldsymbol a)}
 \lambda_{\boldsymbol a}(m)|R(m)|^2
 \le
 \max_{m\in{\cal M}(\boldsymbol a)}|R(m)|^2.
 \tag{86.13}
\]

식 (86.13)을 outer vector 전체에 합하면 식 (86.3)이 나온다. outer와 inner의
독립성, \(S_{\rm sieve}\)와 shift의 독립성, final coordinate product law는 전혀
사용하지 않았다.

## 4. strict same-law gate

Theory 81의 pointwise floor는 정확히 \(S_{\rm sieve}\) 위에서

\[
 M_\omega\ge M_{\min}>0
 \tag{86.14}
\]

를 준다. normalized moment \(\mu_S\)는 따라서

\[
 \mu_S
 \le
 \frac{\rho_S}{M_{\min}^2Y^2}
 \le
 \frac{{\cal H}_{\rm FMT}(R)}
 {Q_{\cal S}M_{\min}^2Y^2}.
 \tag{86.15}
\]

식 (86.4)이면 strict하게

\[
 \mu_S<\tau^2p_*,
 \tag{86.16}
\]

이고 Theory 81의 positive-mass terminal gate를 사용할 수 있다. equality boundary는
양의 남은 질량을 보장하지 않으므로 식 (86.4)의 부등호는 반드시 strict다.

## 5. Theory 82 full-energy route와의 관계

식 (86.9)와 \(|R(m)|^2\ge0\)로

\[
 {\cal H}_{\rm FMT}(R)
 \le
 \sum_{\boldsymbol a\in{\cal A}}
 \sum_{m\in{\cal M}(\boldsymbol a)}|R(m)|^2
 \le
 \sum_{m\bmod q}|R(m)|^2.
 \tag{86.17}
\]

Theory 82의 finite Parseval·convolution upper는

\[
 \sum_{m\bmod q}|R(m)|^2
 \le\varphi(q)N^2V(Y,q).
 \tag{86.18}
\]

따라서 exact hierarchy는

\[
 \boxed{
 \rho_S
 \le\frac{{\cal H}_{\rm FMT}(R)}{Q_{\cal S}}
 \le\frac1{Q_{\cal S}}\sum_{m\bmod q}|R(m)|^2
 \le\frac{\varphi(q)N^2}{Q_{\cal S}}V(Y,q).}
 \tag{86.19}
\]

Theory 82 식 (82.3)이 성립하면 식 (86.4)도 성립한다. 반대 방향은 필요하지 않다.
즉 새 target은 full \(V\)를 통과하지 않고 actual support의 outer-fiber maxima만 직접
제어하는 더 약한 충분조건이다.

## 6. outer-only minimax sharpness

임의의 유한 비공집합 fiber \({\cal M}(\boldsymbol a)\)와 비음수 함수 \(E(m)\)를
고정한다. 각 fiber에서

\[
 m_{\boldsymbol a}\in
 \operatorname*{arg\,max}_{m\in{\cal M}(\boldsymbol a)}E(m)
 \tag{86.20}
\]

를 하나 골라, 조건부로 \(m_{\boldsymbol a}\)에 질량 1을 주고 event를 항상 참으로
두자. 그러면

\[
 \frac1{Q_{\cal S}}
 \sum_{\boldsymbol a}E(m_{\boldsymbol a})
 =
 \frac1{Q_{\cal S}}
 \sum_{\boldsymbol a}
 \max_{m\in{\cal M}(\boldsymbol a)}E(m).
 \tag{86.21}
\]

따라서 식 (86.3)은 outer uniformity와 support만으로는 exact sharp하다. 이 witness는
논리적 optimality test이며 published FMT conditional law의 실제 분포를 재현한다고
주장하지 않는다. actual law를 더 잘 묶으려면 다음 중 적어도 하나가 추가로 필요하다.

1. final \(\mathbf N'\)의 numerical conditional weights,
2. \(|R|\)에 맞춘 one-step increment·conditional variance,
3. FMT support 위의 prime-specific pointwise 또는 fiber-average cancellation,
4. sieve-good event와 weighted observable의 직접 joint moment.

## 7. FMT·FGKMT theorem의 적용 범위

FMT formula (6.17)의 \(n_p\)는 fixed \(\mathbf A\) 뒤의 preliminary conditional
product law다. printed p.11은 그 law에 Theorem 4를 다시 적용해 final
\(\mathbf N'\)를 만든다. 따라서 formula (6.17)의 independence를 final output 전체로
옮기지 않는다.

FMT Theorem 4와 FGKMT Corollary 4의 \(Q''\)는 covering output을 뽑기 전에 고정된다.
반면 식 (86.2)의 maximizing shift와 그 complex character phase는 final output
support에 의존한다. 기존 fixed-subset cardinality theorem은 식 (86.4)의 numerical
upper를 직접 공급하지 않는다.

이번 감사가 source에서 새로 추출한 것은 새로운 확률 독립성이 아니라, 이미 확인된
outer uniform marginal을 **support-restricted conditional subprobability**와 결합한
exact finite reduction이다.

## 8. 수학적 의미와 한계

Theory 82는 각 outer atom의 cap을 full residue energy에 곱했다. 식 (86.19)는 그 사이에
각 outer fiber당 오직 하나의 maximum만 남기는 \({\cal H}_{\rm FMT}\)를 삽입한다.
fiber 안에 여러 가능한 shifts가 있을 때 이는 full energy보다 엄밀히 작을 수 있다.

그러나 maximum은 inner direction에서 여전히 pointwise worst case다. source가 실제
conditional mass를 어디에 두는지 또는 prime-error phase가 support에서 어떻게
상쇄되는지 수치화하지 않으면 식 (86.4)을 인증할 수 없다. 따라서 이번 결과는
actual same-law target을 더 정확히 줄였지만 analytic moment 자체를 닫지 않는다.

## 9. 검증 범위와 증거수준

<code>source/dep_r09_same_law_outer_fiber_audit.py</code>와 단위시험은 exact
<code>Fraction</code>으로 다음을 검사한다.

1. 임의의 conditional event subprobability에 대한 식 (86.12)--(86.13).
2. 각 fiber의 deterministic maximizer가 abstract envelope를 exact하게 달성함.
3. modulo 30의 \(Q_{\cal S}=6\), inner modulus 5 CRT fiber partition.
4. toy에서 \({\cal H}=154<324\)이고 sharp raw moment가 \(154/6=77/3\)임.
5. 식 (86.4)의 strict boundary와 source hash·OPEN status의 fail-closed ledger.

Lean은 식 (86.15)--(86.19)의 dependency-critical scalar implication만 무공리로
검증한다. finite conditional probability와 argmax existence 전체를 이번 batch에서
형식화하지 않으며, 이를 <code>KERNEL_PASS</code>로 가장하지 않는다.

전수 refresh·validation은 theory 문서 87개, display 식 1,630개, Lean declaration
307개, 금지 proof escape 0건으로 PASS했다. 상태는
<code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=83</code>,
<code>DEFINITION_ONLY=130</code>, <code>PARTIAL_FORMALIZATION=131</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=116</code>,
<code>NOT_YET_FORMALIZED=1067</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.

## 10. 현재 판정

| 항목 | 판정 |
|---|---|
| FMT outer uniformity·final coordinate 보존 | <code>SOURCE VERIFIED</code> |
| support-restricted fiber 정의·disjointness | <code>EXACT</code> |
| same-law raw moment의 outer-fiber reduction | <code>EXACT</code> |
| outer uniformity+support만의 minimax sharpness | <code>EXACT FINITE</code> |
| Theory 82 full-energy보다 약한 direct target | <code>EXACT</code> |
| actual \({\cal H}_{\rm FMT}(R)\) numerical upper | <code>OPEN</code> |
| final nibble weighted concentration | <code>OPEN</code> |
| PAP-11·DEP-R09 | <code>OPEN</code> |
| fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\) | <code>OPEN</code> |
| 새 bounded \(X_{\rm cert}\) 범위 | <code>NONE</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 11. 다음 gate

다음 최소 gate는 식 (86.4)을 만족시키는 actual support-restricted fiber upper다.
우선순위는 다음과 같다.

1. final FMT conditional weights에서 output-dependent \(|R|^2\) moment를 직접
   상계할 수 있는지 source proof를 재감사한다.
2. 불가능하면 \({\cal M}(\boldsymbol a)\)의 arithmetic support와 \(\Lambda\)-specific
   cancellation을 함께 쓰는 prime-specific fiber theorem을 찾거나 증명한다.
3. 이 중 어느 입력도 확보되기 전에는 threshold calculator나 장시간 prime 계산을
   시작하지 않는다.

## 12. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468),
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, JAMS 31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
