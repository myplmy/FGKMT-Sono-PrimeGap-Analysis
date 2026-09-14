# Theory 80 — DEP-R09 동일법칙 weighted-correlation tower 감사

- 작성일: 2026-09-14 KST
- 선행 정본:
  [Theory 77](77_Sono_FMT_DEPR09_restricted_residue_variance_spectral_optimality_audit.md),
  [Theory 79](79_Sono_FMT_DEPR09_FMT_construction_law_finite_mass_audit.md)
- 기계 원장:
  [same-law weighted correlation v1](data/Sono_FMT_DEPR09_same_law_weighted_correlation_v1.json)
- 판정:
  <code>FINITE_TOWER_EXACT /
  GLOBAL_AND_FIBERWISE_SUFFICIENT_CONTRACTS_EXPLICIT /
  ACTUAL_ANALYTIC_MOMENT_OPEN</code>
- 계속 OPEN: <code>PAP-11</code>, <code>DEP-R09</code>, fixed
  \(2\times10^{-17}\), numerical \(X_{\rm cert}\)

## 1. 결론

Theory 79가 복원한 실제 FMT final outcome을

\[
 \omega=(\mathbf A,\mathbf N')
\tag{80.1}
\]

로 둔다. 이번 문서는 Theory 77의 direct weighted prime-error를 바로 이 joint law에서
평균내기 위한 최소 유한 계약을 정식화했다.

핵심 진전은 세 가지다.

1. final CRT 이동량과 survivor가 모두 \(\omega\)에 의존한다는 점을 보존한 normalized squared
   badness를 정의했다.
2. 그 expectation을 outer law \(p_A\)와 conditional inner law로 정확히 분해했다.
3. global moment, outer-good conditional moment, uniform fiber moment 중 어느 하나가
   어느 크기까지 내려가야 sieve-good와 correlation-good outcome이 동시에 존재하는지
   exact sufficient inequality로 고정했다.

그러나 FMT/FGKMT의 fixed-subset cardinality 정리는 final covering output에 따라 위상이
바뀌는 signed/complex character observable을 제어하지 않는다. Maier와 Sono는 이 평균을
쓰지 않고 fixed CRT residue마다 pointwise PAP를 넣는다. 확인한 source 범위에는 아래
moment contract를 바로 공급하는 drop-in theorem이 없었다. 따라서 이번 단계는 필요한
정리를 정확히 좁힌 것이며 그 analytic 입력 자체를 증명한 것은 아니다.

## 2. 실제 CRT observable

Sono의 표기처럼

\[
 P=\frac{P(x)}{B_0},\qquad
 I=[y]\setminus[x]
\tag{80.2}
\]

로 둔다. final residue system이 정해지면 CRT로 유일한 \(m_\omega\pmod P\)가 정해지고,

\[
 T_\omega=
 \{s\in I:(m_\omega+s,P)=1\},
 \qquad M_\omega=|T_\omega|
\tag{80.3}
\]

이다. Dirichlet character를 nonunit에서 0으로 연장하면 Theory 79의 survivor 합은
fixed interval 전체의 shifted character sum과 exact하게 같다.

\[
 C_\chi(\omega)
 =\sum_{s\in T_\omega}\overline{\chi(m_\omega+s)}
 =\sum_{s\in I}\overline{\chi(m_\omega+s)}.
\tag{80.4}
\]

첫 등식은 survivor 표기이고 둘째 등식은 \((m_\omega+s,P)>1\)이면 character가 0이라는
사실을 쓴다. 따라서 \(T_\omega\)와 \(m_\omega\)를 서로 독립인 자료처럼 분리하면 안 된다.

Theory 77의 prime-error vector를 \(Z_\chi(Y)\)라 쓰고 주지표를 제외한 weighted error를

\[
 R(\omega)=
 \sum_{\substack{\chi\bmod P\\\chi\ne\chi_0}}
 C_\chi(\omega)Z_\chi(Y)
\tag{80.5}
\]

로 둔다. 남은 상대오차 budget은

\[
 \tau=\varepsilon-\delta_0>0
\tag{80.6}
\]

이고 필요한 direct target은

\[
 |R(\omega)|\le \tau M_\omega Y.
\tag{80.7}
\]

## 3. divide-by-zero 없는 normalized badness

\(O\)를 Theory 55의 outer-good event라 한다. \(O\)에서 \(M_\omega\ge M_{\min}>0\)인
pointwise survivor floor를 함께 인증한다는 조건 아래

\[
 W(\omega)=
 \begin{cases}
 \displaystyle\frac{|R(\omega)|^2}{M_\omega^2Y^2},&\omega\in O,\\[6pt]
 0,&\omega\notin O
 \end{cases}
\tag{80.8}
\]

로 둔다. 이렇게 해야 bad outer outcome이나 \(M_\omega=0\)에서 정의되지 않은 나눗셈을
숨기지 않는다. \(O\) 안에서는 식 (80.7)이 정확히

\[
 W(\omega)\le\tau^2
\tag{80.9}
\]

와 동치다. equality boundary도 good event에 포함한다.

## 4. finite tower identity

outer law를 \(p_A(\boldsymbol a)\), conditional inner law를
\(p_{N\mid A}(\boldsymbol n\mid\boldsymbol a)\)라 하면

\[
 \begin{aligned}
 \mu
 :=\mathbb E[W]
 &=\sum_{\boldsymbol a\in O}p_A(\boldsymbol a)
   \sum_{\boldsymbol n}
   p_{N\mid A}(\boldsymbol n\mid\boldsymbol a)
   W(\boldsymbol a,\boldsymbol n)\\
 &=\sum_{\boldsymbol a\in O}\sum_{\boldsymbol n}
   p_A(\boldsymbol a)
   p_{N\mid A}(\boldsymbol n\mid\boldsymbol a)
   W(\boldsymbol a,\boldsymbol n).
 \end{aligned}
\tag{80.10}
\]

이는 FMT formula (1.1)의 finite version이다. 새로운 독립성 가정은 없다. 이 identity는
analytic upper bound를 만들지 않고, 그 bound가 어느 law에서 증명되어야 하는지만 고정한다.

## 5. 가장 약한 global moment 충분조건

Theory 79의 sieve-good mass는

\[
 S_{\rm sieve}=(1-F_{\rm out})(1-F_{\rm in})
\tag{80.11}
\]

이상이다. 비음수 \(W\)에 Markov를 적용하면

\[
 \Pr\bigl(O\cap\{W>\tau^2\}\bigr)
 \le\frac{\mu}{\tau^2}.
\tag{80.12}
\]

따라서 outer-good, inner-good, correlation-good을 모두 만족할 mass는

\[
 \Pr\bigl(O\cap I_{\rm good}\cap\{W\le\tau^2\}\bigr)
 \ge
 \max\!\left\{0,
 (1-F_{\rm out})(1-F_{\rm in})-\frac{\mu}{\tau^2}
 \right\}.
\tag{80.13}
\]

가장 약한 현재 sufficient gate는

\[
 \boxed{
 \mu<\tau^2(1-F_{\rm out})(1-F_{\rm in}).
 }
\tag{80.14}
\]

이 식은 correlation-bad와 inner-bad의 독립성을 요구하지 않는다.

## 6. outer-good conditional 및 uniform-fiber 경로

\(\Pr(O)>0\)이고

\[
 \mathbb E[W\mid O]\le\mu_O
\tag{80.15}
\]

이면

\[
 \Pr\bigl(O\cap I_{\rm good}\cap\{W\le\tau^2\}\bigr)
 \ge
 (1-F_{\rm out})
 \max\!\left\{0,1-F_{\rm in}-\frac{\mu_O}{\tau^2}\right\}.
\tag{80.16}
\]

따라서

\[
 F_{\rm in}+\frac{\mu_O}{\tau^2}<1
\tag{80.17}
\]

이면 충분하다.

더 강한 source가 모든 outer-good \(\boldsymbol a\)에 대해

\[
 \mathbb E[W\mid\mathbf A=\boldsymbol a]\le\mu_f
\tag{80.18}
\]

를 uniform하게 준다면

\[
 \boxed{
 F_{\rm in}+\frac{\mu_f}{\tau^2}<1
 }
\tag{80.19}
\]

로 각 good fiber 안에서 직접 하나의 inner outcome을 고를 수 있다. 식 (80.19)는 source
적용은 단순하지만 식 (80.14)보다 강한 요구다. 따라서 global route를 먼저 찾는다.

## 7. raw second moment를 쓸 때 필요한 survivor floor

어떤 source가 normalized \(W\)가 아니라

\[
 \mathbb E\!\left[1_O|R(\omega)|^2\right]\le\rho
\tag{80.20}
\]

만 준다면 \(O\)에서 pointwise \(M_\omega\ge M_{\min}>0\), \(Y>0\)를 인증해야

\[
 \mu\le\frac{\rho}{M_{\min}^2Y^2}
\tag{80.21}
\]

를 쓸 수 있다. 평균 survivor count만으로 분모를 바꾸면 Jensen 방향과 small-\(M_\omega\)
tail을 놓칠 수 있으므로 허용하지 않는다.

## 8. source 적용성 감사

| source | 실제로 주는 것 | 이번 계약에 충분한가 |
|---|---|---|
| FMT formula (1.1) | conditional expectation의 tower identity | 식 (80.10)에만 충분; moment upper 없음 |
| FMT Theorem 4 | inner draw 전에 고정된 \(Q''\subset Q'\)의 survivor cardinality | output-dependent complex weight에는 불충분 |
| FGKMT Corollary 4 | fixed \(Q''\) cardinality를 \(1-o(1)\)로 보존 | signed phase, numerical rate, growing family 없음 |
| FGKMT Theorem 3 | 작은 fixed vertex subsets의 survival probability | high-degree CRT character observable을 직접 제어하지 않음 |
| Maier 1981 Lemma 2 | fixed CRT column마다 pointwise Gallagher PNT | FMT outcome 평균이 아니라 기존 pointwise route |
| Sono Lemma 3.7 | every fixed reduced residue에 pointwise PAP | \(z\)-row 평균은 \(m_\omega\) 평균이 아님 |

특히 FMT/FGKMT의 \(Q''\)는 inner output을 뽑기 전에 고정해야 한다. 반면 식 (80.4)의
phase는 그 output이 정한 \(m_\omega\)에 의존한다. 복소 weight를 양·음 부분이나 level set으로
분해해도 각 subset 자체가 output에 따라 바뀌므로 printed theorem의 양화사에 들어가지 않는다.
모든 가능한 output을 union bound하는 방식도 printed \(o(1)\) rate와 output family size가
수치화되지 않아 현재 finite proof가 아니다.

targeted literature screen에서는 hypergraph nibble의 일반 concentration 결과와 character-sum
moment 결과도 대조했지만, actual FMT covering success와 식 (80.4)의 CRT-dependent complex
observable을 같은 law에서 numerical cutoff까지 묶는 drop-in theorem은 식별하지 못했다.
이는 관련 정리가 전 문헌에 없다는 명제가 아니라 이번에 확인한 범위의 결과다.

## 9. 최소 신규 analytic lemma

현재 가장 약한 새 lemma는 다음 **global normalized-moment** 형태다.

> 실제 final FMT joint law \((\mathbf A,\mathbf N')\)에서 식 (80.8)의 \(W\)가
> numerical multiplier와 공통 finite cutoff를 가지며 식 (80.14)를 만족한다.

이 lemma는 적어도 다음을 보존해야 한다.

1. preliminary independent edge가 아니라 actual final \(\mathbf N'\).
2. CRT shift \(m(\mathbf A,\mathbf N')\).
3. exceptional prime \(B_0\)와 \(P=P(x)/B_0\).
4. endpoint interval ([y]\setminus[x]).
5. direct normalized observable 또는 pointwise \(M_{\min}>0\).
6. FMT finite covering proof와 같은 law.
7. numerical multiplier, error allocation, common finite cutoff.

uniform-fiber lemma (80.18)는 대안이지만 더 강하다. 반대로 FMT fixed-subset count를 그대로
인용하거나, outer \(\mathbf A\)만 평균내거나, preliminary edge의 독립성을 final output에 옮기는 것은
충분하지 않다.

## 10. 검증 범위

<code>source/dep_r09_same_law_weighted_correlation.py</code>는 exact
<code>Fraction</code>으로 다음을 검사한다.

1. finite joint law와 각 conditional law의 질량 1.
2. tower 합과 flat joint-atom 합의 exact equality.
3. 식 (80.13), (80.16), (80.19)의 strict boundary.
4. 식 (80.21)의 pointwise survivor floor 요구.
5. source hash와 OPEN 상태의 fail-closed machine ledger.

Lean 단일 정본은 식 (80.10)의 finite-sum identity와 식 (80.14), (80.17), (80.21)의
terminal algebra만 검사한다. character-sum moment나 FMT analytic theorem을
project-local <code>axiom</code>으로 넣지 않는다. <code>sorry</code>, <code>admit</code>,
project-local <code>axiom</code>은 사용하지 않는다.

## 11. 현재 판정과 다음 gate

| 항목 | 판정 |
|---|---|
| actual outcome·CRT observable | <code>EXACTLY SPECIFIED</code> |
| finite tower identity | <code>EXACT</code> |
| global/conditional/fiber sufficient inequalities | <code>EXACT</code> |
| FMT fixed-subset theorem의 drop-in 적용 | <code>REJECTED AS STATED</code> |
| actual same-law analytic moment | <code>OPEN</code> |
| <code>PAP-11</code>, <code>DEP-R09</code> | <code>OPEN</code> |
| fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\) | <code>OPEN</code> |
| 새 bounded \(X_{\rm cert}\) 범위 | <code>NONE</code> |
| threshold calculator·장시간 prime 계산 | <code>NOT READY / NOT RUN</code> |

다음 source-first 우선순위는 actual FMT output law의 생성 과정을 단계별 filtration으로
분해해 식 (80.20)의 martingale 또는 bounded-difference estimate가 가능한지 검사하는 것이다.
그 과정에서도 CRT phase의 한 residue 변경 민감도와 survivor denominator floor를 먼저
수치화해야 한다. 이 입력이 없으면 장시간 소수 계산은 analytic 공백을 메우지 못한다.

## 12. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1),
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, JAMS 31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
- H. Maier, *Chains of large gaps between primes*, Advances in Mathematics 39
  (1981), 257--269,
  [doi:10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- K. Sono, *An explicit lower bound for gaps between some consecutive primes*,
  Research in Number Theory 11 (2025), Article 14,
  [doi:10.1007/s40993-024-00569-8](https://doi.org/10.1007/s40993-024-00569-8).
- D. Y. Kang, T. Kelly, D. Kühn, A. Methuku and D. Osthus,
  *Graph and hypergraph colouring via nibble methods: A survey*,
  [arXiv:2106.13733](https://arxiv.org/abs/2106.13733). 일반 배경자료이며
  식 (80.14)의 drop-in theorem으로 사용하지 않았다.
