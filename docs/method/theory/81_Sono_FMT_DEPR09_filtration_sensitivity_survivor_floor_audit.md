# Theory 81 — DEP-R09 FMT filtration 민감도·survivor floor 감사

- 작성일: 2026-09-15 KST
- 선행 정본:
  [Theory 55](55_Sono_FMT_H1bCOV2_post_covering_interval_smooth_composition.md),
  [Theory 79](79_Sono_FMT_DEPR09_FMT_construction_law_finite_mass_audit.md),
  [Theory 80](80_Sono_FMT_DEPR09_same_law_weighted_correlation_tower_audit.md)
- 기계 원장:
  [filtration sensitivity and survivor floor v1](data/Sono_FMT_DEPR09_filtration_sensitivity_survivor_floor_v1.json)
- 판정:
  <code>SIEVE_GOOD_DENOMINATOR_FLOOR_ALIGNED_AND_PARAMETERIZED_EXPLICIT /
  NAIVE_FINAL_COORDINATE_BOUNDED_DIFFERENCE_REJECTED /
  MARTINGALE_INCREMENT_AND_VARIANCE_INPUTS_OPEN</code>
- 계속 OPEN: <code>PAP-11</code>, <code>DEP-R09</code>, fixed
  (2\times10^{-17}), numerical (X_{\rm cert})

## 1. 결론

Theory 80이 제안한 다음 두 감사를 source와 exact finite algebra로 수행했다.

1. Theory 55의 survivor lower bound는 재사용할 수 있다. 단, outer-good 사건 (O)
   전체가 아니라 conditional inner covering까지 성공한
   (S_{\rm sieve}=O\cap I_{\rm good})에서만 쓸 수 있다.
2. final FMT output을 한 residue coordinate씩 드러내는 martingale 아이디어는 현재
   그대로는 닫히지 않는다. survivor **개수** 변화는 작게 묶이지만, nonprincipal
   Dirichlet character의 **위상**은 공통 survivor에서도 바뀐다. 따라서 개수 민감도
   (2\lceil N/p\rceil)를 weighted prime error의 increment bound로 옮길 수 없다.

즉 분모 정합성 하나는 닫혔지만 분자의 same-law analytic second moment는 여전히 열린다.
새 bounded (X_{\rm cert}) 범위는 생기지 않았고 장시간 prime 계산도 시작하지 않는다.

## 2. source의 실제 확률 filtration

FMT Section 6 formula (6.17)은 first-stage residue vector
(\mathbf A=\boldsymbol a)를 고정한 뒤 preliminary (n_p)를 (p\)에 대해 jointly
conditionally independent하게 정의한다. 그러나 FMT Theorem 3의 최종 residue는 그
preliminary draw 자체가 아니다. good (\boldsymbol a)마다 Theorem 4를 다시 적용해
covering output (\mathbf N')를 고른다.

그 Theorem 4가 인용하는 FGKMT Theorem 3의 proof는 한 번에 모든 final coordinate를
독립 추첨하지 않는다. nibble 단계 (I_1,\ldots,I_m)를 순서대로 드러낸다. (m\)번째
단계 전에

\[
 W_{m-1}=V\setminus
 \bigcup_{j=1}^{m-1}\bigcup_{i\in I_j}e'_i
 \tag{81.1}
\]

를 만들고, (W_{m-1}=W)를 고정한 조건 아래 formula (5.9)의 reweighted law로
(i\in I_m)의 (e'_i)를 jointly conditionally independent하게 고른다.

따라서 정확한 구조는 다음과 같다.

- 같은 nibble 안에서는 과거 (W)를 조건으로 conditional product law가 있다.
- 앞 단계 선택은 (W)를 바꾸므로 뒤 단계의 모든 conditional distribution을 바꾼다.
- 독립 random seed들로 전체 과정을 생성할 수 있다는 사실만으로, 한 seed 변경에 대한
  작은 Lipschitz bound가 따라오지는 않는다.

즉 final residue coordinate 전체를 처음부터 독립인 product law로 취급하면 source보다
강한 가정을 추가하게 된다.

## 3. survivor floor의 정확한 사건 영역

(O)를 outer-good 사건, (I_{\rm good})을 그 outer fiber 안의 covering-good 사건이라 하고

\[
 S_{\rm sieve}=O\cap I_{\rm good}
 \tag{81.2}
\]

로 둔다. Theory 79의 exact conditional-law 합은

\[
 \Pr(S_{\rm sieve})\ge
 (1-F_{\rm out})(1-F_{\rm in})
 \tag{81.3}
\]

을 준다. Theory 55 formula (55.38)의 하한은 바로 이 final successful residue outcome에서

\[
 M_\omega=|T_\omega|
 \ge M_{\min}:=
 A(1-\eta)\frac{X}{\log X}>0
 \qquad(\omega\in S_{\rm sieve})
 \tag{81.4}
\]

이다. outer-good (O)만 알고 inner covering이 실패한 outcome까지 (81.4)를 확대할
source 근거는 없다.

따라서 divide-by-zero 없는 actual normalized badness는

\[
 W_S(\omega)=
 \begin{cases}
 \displaystyle\frac{|R(\omega)|^2}{M_\omega^2Y^2},
   &\omega\in S_{\rm sieve},\\[6pt]
 0,&\omega\notin S_{\rm sieve}
 \end{cases}
 \tag{81.5}
\]

로 둬야 한다.

\[
 \mu_S:=\mathbb E W_S
 \tag{81.6}
\]

라 하면 Markov와 (81.3)으로

\[
 \Pr\!\left(S_{\rm sieve}\cap\{W_S\le\tau^2\}\right)
 \ge
 \max\!\left\{0,
 (1-F_{\rm out})(1-F_{\rm in})-
 \frac{\mu_S}{\tau^2}\right\}.
 \tag{81.7}
\]

따라서 strict sufficient gate는

\[
 \boxed{
 \mu_S<\tau^2(1-F_{\rm out})(1-F_{\rm in}).}
 \tag{81.8}
\]

source가 raw moment

\[
 \mathbb E\!\left[1_{S_{\rm sieve}}|R(\omega)|^2\right]
 \le\rho_S
 \tag{81.9}
\]

를 준다면 같은 사건의 pointwise floor (81.4)로

\[
 \mu_S\le\frac{\rho_S}{M_{\min}^2Y^2}
 \tag{81.10}
\]

를 쓸 수 있다. 이 보정은 Theory 80의 finite 대수를 폐기하지 않고 실제 적용 domain을
정확히 줄인 것이다. 하지만 (\rho_S)를 상계하는 analytic theorem은 아직 없다.

## 4. CRT survivor 표기의 일치

Theory 78의 final residue를 (a_p\pmod p)라 쓰고 CRT shift를

\[
 m_\omega\equiv-a_p\pmod p
 \tag{81.11}
\]

로 정하면 모든 (p\mid P)에 대해

\[
 s\not\equiv a_p\pmod p
 \quad\Longleftrightarrow\quad
 p\nmid m_\omega+s.
 \tag{81.12}
\]

따라서

\[
 T_\omega
 =\{s\in I:s\not\equiv a_p\pmod p\ \text{for every }p\mid P\}
 =\{s\in I:(m_\omega+s,P)=1\}.
 \tag{81.13}
\]

Theory 55의 final sifted set과 Theory 80의 denominator가 같은 함수라는 점이 이 식으로
확인된다.

## 5. 한 residue 변경이 survivor 개수에 미치는 영향

(I\)가 (N\)개의 연속 정수, (P\)가 squarefree이고 (p\mid P)라 하자. 두 shift
(m,m')가

\[
 m\equiv m'\pmod{P/p},
 \qquad m\not\equiv m'\pmod p
 \tag{81.14}
\]

를 만족한다고 하자. (p) 이외의 모든 prime divisor에 대한 생존 여부는 같다.
따라서 survivor symmetric difference는 (m+s\equiv0\pmod p) 또는
(m'+s\equiv0\pmod p)인 두 residue class의 합집합에 포함된다.

(N\)개 연속 정수 안에서 한 residue class는 최대 (\lceil N/p\rceil)번 나타나므로

\[
 |T_m\triangle T_{m'}|
 \le2\left\lceil\frac Np\right\rceil.
 \tag{81.15}
\]

특히

\[
 \bigl||T_m|-|T_{m'}|\bigr|
 \le|T_m\triangle T_{m'}|
 \le2\left\lceil\frac Np\right\rceil.
 \tag{81.16}
\]

이 결과는 (M_\omega)라는 **분모·개수**의 민감도에는 정확하고 유용하다.

## 6. 왜 character phase에는 같은 경계가 적용되지 않는가

Dirichlet character를 nonunit에서 0으로 연장하고

\[
 C_\chi(m)=\sum_{s\in I}\overline{\chi(m+s)}
 \tag{81.17}
\]

로 둔다. (\chi)의 (p\)-local component가 principal이면 공통 survivor에서 character
값이 변하지 않아 (81.15)의 경계를 (C_\chi)에도 쓸 수 있다. 그러나 nonprincipal
(p\)-component에서는 공통 survivor의 위상도 바뀐다.

다음 exact finite example은 count 경계의 무조건적 전이가 거짓임을 보인다.

- (P=65=5\cdot13\), 변경 prime (p=5).
- (m=0\), (m'=13\): modulo 13에서는 같고 modulo 5에서만 다르다.
- (I=\{1,2,3\}).
- (\chi=\left(\frac{\cdot}{5}\right)\chi_{0,13}).

이때

\[
 C_\chi(0)=1-1-1=-1,
 \qquad
 C_\chi(13)=1+0+1=2.
 \tag{81.18}
\]

따라서

\[
 |C_\chi(13)-C_\chi(0)|=3
 >2=2\left\lceil\frac35\right\rceil,
 \tag{81.19}
\]

반면 survivor symmetric difference의 실제 크기는 1이다. 즉 membership이 그대로인 두
offset에서도 character phase가 바뀌어 추가 변화가 생겼다.

추가 구조 없이 언제나 쓸 수 있는 것은 각 합의 절댓값이 (N\) 이하라는 trivial bound

\[
 |C_\chi(m')-C_\chi(m)|\le2N
 \tag{81.20}
\]

뿐이다. Theory 80의 weighted error에는

\[
 |R(m')-R(m)|
 \le2N\sum_{\chi\ne\chi_0}|Z_\chi(Y)|
 \tag{81.21}
\]

가 되는데, 이는 (L^1) pointwise PAP 크기의 부담을 되살려 useful bounded-difference
certificate가 아니다.

## 7. generic concentration theorem을 바로 적용할 수 없는 이유

final law의 자연 filtration을 (\mathcal F_0\subset\cdots\subset\mathcal F_m)이라 하고

\[
 D_j=
 \mathbb E[R\mid\mathcal F_j]-
 \mathbb E[R\mid\mathcal F_{j-1}]
 \tag{81.22}
\]

로 두면 martingale 표현 자체는 가능하다. 하지만 concentration을 얻으려면 적어도

\[
 |D_j|\le b_j,
 \qquad
 \sum_j\mathbb E[D_j^2\mid\mathcal F_{j-1}]\le v
 \tag{81.23}
\]

같은 numerical increment·conditional-variance 입력이 필요하다.

문헌 적용성 판정은 다음과 같다.

| 방법 | 필요한 입력 | actual FMT law에서의 상태 |
|---|---|---|
| Freedman martingale tail | bounded increments와 predictable quadratic variation | 둘 다 OPEN |
| Warnke typical bounded differences | independent inputs 및 typical/worst Lipschitz constants | seed 표현은 가능하지만 Lipschitz constants 부재 |
| Kontorovich--Ramanan dependent concentration | quantitative mixing matrix/coefficient | actual numerical coefficient 부재 |
| Combes high-probability bounded differences | high-probability set에서 bounded-difference property | 그 property 자체가 부재 |

따라서 generic 정리를 이름만 바꿔 넣어서는 공백이 닫히지 않는다. 이 source screen은
모든 가능한 concentration proof의 불가능성 정리가 아니라, 현재 입력에 대한 drop-in
적용이 없다는 판정이다.

## 8. 남아 있는 더 유망한 analytic 경로

character orthogonality는 (C_\chi(m')-C_\chi(m))의 전체 character energy를 residue-count
차이의 (L^2) norm으로 바꿀 수 있다. 예를 들어

\[
 f(a)=\#\{s\in I:m'+s\equiv a\pmod P\}
      -\#\{s\in I:m+s\equiv a\pmod P\}
 \tag{81.24}
\]

를 reduced residues (a\in U(P))에서 정의하면 finite Fourier orthogonality로

\[
 \sum_{\chi\bmod P}
 |C_\chi(m')-C_\chi(m)|^2
 =\varphi(P)\sum_{a\in U(P)}|f(a)|^2.
 \tag{81.25}
\]

그 뒤 Cauchy--Schwarz는 weighted increment를

\[
 |\Delta R|^2
 \le
 \left(\sum_\chi|\Delta C_\chi|^2\right)
 \left(\sum_\chi|Z_\chi(Y)|^2\right)
 \tag{81.26}
\]

로 바꾼다. 이는 (81.21)의 (L^1) 합보다 구조적으로 낫지만,
(\sum|Z_\chi|^2)와 filtration-conditional version을 수치화하는 새 analytic input이
필요하다. FMT covering theorem이 자동으로 공급하는 결과는 아니다.

따라서 다음 우선순위는 다음 둘 중 하나다.

1. actual final law에서 (1_{S_{\rm sieve}}|R|^2)의 direct conditional second moment.
2. nibble별 (81.25)--(81.26)를 사용한 Doob increment와 conditional variance의 수치 정리.

reserve randomization은 이 두 경로가 구조적으로 실패한 뒤 검토한다.

## 9. 검증 범위

<code>source/dep_r09_filtration_sensitivity.py</code>와 11개 exact 단위시험은 다음을 검증한다.

1. (81.15)--(81.16)을 여러 small squarefree modulus·interval에서 전수 계산.
2. (81.18)--(81.19)의 (P=65) exact counterexample.
3. (81.3), (81.4), (81.7)--(81.10)의 rational algebra와 strict boundary.
4. source hash와 OPEN 상태의 fail-closed machine ledger.

이 finite 검증은 analytic moment, FMT source theorem 또는 concentration inequality의
가정을 증명하지 않는다. dependency-critical terminal algebra는 단일 Lean 정본에도
추가하되, character-sum source theorem을 project-local axiom으로 넣지 않는다.

## 10. 현재 판정

| 항목 | 판정 |
|---|---|
| final sieve-good event mass | <code>PROJECT PARAMETERIZED EXPLICIT</code> |
| survivor floor와 normalization domain | <code>ALIGNED / CORRECTED</code> |
| final law global product independence | <code>FALSE AS A SOURCE CLAIM</code> |
| within-nibble conditional independence | <code>SOURCE VERIFIED</code> |
| one-residue survivor-count sensitivity | <code>EXACT</code> |
| count bound의 nonprincipal phase 전이 | <code>REJECTED BY EXACT COUNTEREXAMPLE</code> |
| useful martingale increment·variance bound | <code>OPEN</code> |
| actual same-law analytic moment | <code>OPEN</code> |
| <code>PAP-11</code>, <code>DEP-R09</code> | <code>OPEN</code> |
| fixed (2\times10^{-17}), numerical (X_{\rm cert}) | <code>OPEN</code> |
| 새 bounded (X_{\rm cert}) 범위 | <code>NONE</code> |
| threshold calculator·장시간 prime 계산 | <code>NOT READY / NOT RUN</code> |

## 11. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468),
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
- D. A. Freedman, *On Tail Probabilities for Martingales*, Annals of Probability
  3 (1975), 100--118,
  [doi:10.1214/aop/1176996452](https://doi.org/10.1214/aop/1176996452).
- L. Warnke, *On the method of typical bounded differences*, Combinatorics,
  Probability and Computing 25 (2016), 269--299,
  [arXiv:1212.5796](https://arxiv.org/abs/1212.5796),
  [doi:10.1017/S0963548315000103](https://doi.org/10.1017/S0963548315000103).
- L. Kontorovich and K. Ramanan, *Concentration inequalities for dependent random
  variables via the martingale method*, Annals of Probability 36 (2008),
  [arXiv:math/0609835](https://arxiv.org/abs/math/0609835).
- R. Combes, *An extension of McDiarmid's inequality*,
  [arXiv:1511.05240](https://arxiv.org/abs/1511.05240).
