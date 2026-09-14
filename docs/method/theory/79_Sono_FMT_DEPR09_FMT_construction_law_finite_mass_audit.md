# Theory 79 — DEP-R09 FMT construction law 유한 성공질량 감사

- 작성일: 2026-09-14 KST
- 선행 정본:
  [Theory 78](78_Sono_FMT_DEPR09_Maier_CRT_shift_quantifier_audit.md),
  [Theory 53](53_Sono_FMT_H1bCOV1_full_residue_hypergraph_interface.md),
  [Theory 55](55_Sono_FMT_H1bCOV2_post_covering_interval_smooth_composition.md)
- 기계 원장:
  [FMT construction mass v1](data/Sono_FMT_DEPR09_FMT_construction_mass_v1.json)
- 판정:
  <code>PRINTED_FMT_RATE_QUALITATIVE /
  PROJECT_COV2_TWO_STAGE_SIEVE_MASS_PARAMETERIZED_EXPLICIT /
  SAME_LAW_WEIGHTED_CORRELATION_FAILURE_OPEN</code>
- 계속 OPEN: <code>PAP-11</code>, <code>DEP-R09</code>, fixed \(2\times10^{-17}\),
  numerical \(X_{\rm cert}\)

## 1. 결론

Theory 78은 FMT의 무작위 후보를 \(\boldsymbol a\) 하나로 너무 짧게 썼다.
FMT Sections 5--6의 실제 최종 residue system은 두 단계 결과,
\(\mathbf A\)와 그 값에 조건부로 고른 \(\mathbf N'\)에 의존한다. 정확한 표본점은
\(\omega=(\mathbf A,\mathbf N')\)이고 그 law는

\[
 \Pr(\mathbf A=\boldsymbol a,\mathbf N'=\boldsymbol n)
 =
 \Pr(\mathbf A=\boldsymbol a)
 \Pr(\mathbf N'=\boldsymbol n\mid\mathbf A=\boldsymbol a).
\tag{79.1}
\]

Theory 55가 이미 outer failure \(F_{\rm out}\)과 모든 outer-good
\(\boldsymbol a\)에서 동일하게 쓸 수 있는 conditional inner failure
\(F_{\rm in}\)을 유한식으로 만들었다. 따라서 project finite successor에서는

\[
 \Pr(S_{\rm sieve})\ge
 (1-F_{\rm out})(1-F_{\rm in})>0
\tag{79.2}
\]

가 성립한다. 두 단계 독립성은 필요 없다. 그러므로 “sieve-good construction의
finite positive mass가 전혀 없다”는 Theory 78의 넓은 표현은 이번 문서가 교정한다.

다만 weighted prime-error correlation이 같은 \((\mathbf A,\mathbf N')\) law에서
실패할 확률은 아직 상계되지 않았다. 따라서 simultaneous good construction,
<code>PAP-11</code>, fixed coefficient와 numerical \(X_{\rm cert}\)는 여전히 열린다.

## 2. 출판된 FMT 확률구성

FMT Theorem 5의 first stage는 \(\mathbf A=(a_s\bmod s)_{s\in\mathcal S}\)다.
Section 6에서 각 \(a_s\)는 독립 균등분포이고 preliminary
\(\widetilde n_p\)와 독립이다. fixed \(\mathbf A=\boldsymbol a\) 뒤 formula (6.17)은
final \(n_p\)를 jointly conditionally independent하게 정한다.

Theorem 5의 outer-good \(\boldsymbol a\)마다 Theorem 4를 조건부 적용해
새 covering output \(n'_p\)를 고른다. bad outer \(\boldsymbol a\)에서는
\(n'_p\)를 임의로 둔다. 최종 residue class는 구조적으로

\[
 a_p^{\rm final}=
 \begin{cases}
 A_p,&p\in\mathcal S,\\
 N'_p,&p\in\mathcal P,\\
 0,&p\notin\mathcal S\cup\mathcal P
 \end{cases}
\tag{79.3}
\]

와 같은 두 단계 함수다. preliminary \(\widetilde n_p\)는 edge probability를 만드는
보조변수이지 최종 큰 소수 residue 자체가 아니다.

출판된 source는 다음 수준까지만 말한다.

- Theorem 3 formula (4.6): 각 fixed interval의 count가 probability \(1-o(1)\)로 성립.
- Theorem 4: residual count가 probability \(1-o(1)\)로 \(5^{-m}\) 비율에 접근.
- Theorem 5 formulas (5.7)--(5.8): outer count와 good-\(\mathbf A\) 사건이
  probability \(1-o(1)\)로 성립.
- Lemmas 6.3--6.4: Markov·Chebyshev를 쓰지만 앞단 \(O,o(1)\) multiplier와 공통 cutoff가
  수치로 인쇄되지 않음.

따라서 published FMT만으로 numerical mass나 numerical cutoff를 선언하지 않는다.

## 3. project COV2가 이미 주는 두 finite failure bound

Theory 55 formula (55.17)의 outer failure는

\[
 F_{\rm out}=
 \frac{4800c}{b^5}
 +\frac{800c}{b^{10}}
 +\frac{112kb^4}{a^{11}}
 +\frac{3Kb^6}{a^{17}}.
\tag{79.4}
\]

fixed outer-good \(\mathbf A\)에서 formulas (55.18)--(55.21)은

\[
 F_{\rm in}=\frac{Kv_*}{t^2},\qquad
 v_*=\beta_h+2\alpha_h+
 \frac{2(1+\alpha_h)a}{(1-r_0)AhX}
\tag{79.5}
\]

를 준다. 이 \(F_{\rm in}\)은 outer-good \(\mathbf A\)를 하나 고른 뒤 생기는
conditional hypergraph law의 failure upper bound이고, 같은 parameter gate 아래 모든
outer-good 값에 공통이다.

\(O\)를 outer-good event, \(I\)를 conditional inner-good event라 하면

\[
\begin{aligned}
\Pr(O\cap I)
&=\sum_{\boldsymbol a\in O}
  \Pr(\mathbf A=\boldsymbol a)
  \Pr(I\mid\mathbf A=\boldsymbol a)\\
&\ge(1-F_{\rm in})\Pr(O)\\
&\ge(1-F_{\rm out})(1-F_{\rm in}).
\end{aligned}
\tag{79.6}
\]

이에 대응하는 failure upper bound는 exact하게

\[
 F_{\rm sieve}
 \le F_{\rm out}+(1-F_{\rm out})F_{\rm in}
 =1-(1-F_{\rm out})(1-F_{\rm in}).
\tag{79.7}
\]

Theory 55의 순차 존재증명은 \(F_{\rm out}<1\), \(F_{\rm in}<1\)만으로 충분했다.
식 (79.6)은 그 proof에 이미 있는 uniform conditional bound를 이용해 같은 law의
성공질량까지 보존한 더 강한 bookkeeping이다.

## 4. weighted correlation과 동시에 좋은 outcome을 고르는 조건

Theory 78의 weighted coefficient도 \(\boldsymbol a\) 하나가 아니라 joint outcome에
의존하도록 고쳐 써야 한다.

\[
 C_\chi(\mathcal A_{\boldsymbol a,\boldsymbol n'})
 =
 \sum_{s\in\mathcal T(\boldsymbol a,\boldsymbol n')}
 \overline{\chi\!\left(m(\boldsymbol a,\boldsymbol n')+s\right)}.
\tag{79.8}
\]

같은 joint law에서 correlation-bad event를 \(B_{\rm corr}\)라 하고
\(\Pr(B_{\rm corr})\le F_{\rm corr}\)라 하자. union bound는

\[
 \Pr(S_{\rm sieve}\cap B_{\rm corr}^{\,c})
 \ge
 (1-F_{\rm out})(1-F_{\rm in})-F_{\rm corr}.
\tag{79.9}
\]

따라서 simultaneous good outcome의 충분조건은

\[
 \boxed{
 F_{\rm corr}<(1-F_{\rm out})(1-F_{\rm in}).
 }
\tag{79.10}
\]

더 보수적이지만 간단한

\[
 F_{\rm out}+F_{\rm in}+F_{\rm corr}<1
\tag{79.11}
\]

도 충분하다. 다만 product gate보다 slack을 더 버린다.

fiberwise theorem을 얻을 수 있다면 더 직접적이다. 모든 outer-good
\(\boldsymbol a\)에 대해

\[
 F_{\rm in}+F_{\rm corr}(\boldsymbol a)<1
\tag{79.12}
\]

이면 먼저 outer-good \(\boldsymbol a\) 하나를 고르고, 그 fiber 안에서 inner-good과
correlation-good의 교집합을 고를 수 있다.

비음수 same-law badness \(W\)와 threshold \(t>0\)에 대해

\[
 \Pr(W\ge t)\le
 \min\!\left(1,\frac{\mathbb E W}{t}\right)
\tag{79.13}
\]

이므로 \(\mathbb EW/t\)가 식 (79.10)의 우변보다 작다는 것이 한 가지 구체적인
analytic 목표다.

## 5. 무엇이 닫혔고 무엇이 남았는가

| 항목 | 판정 | 이유 |
|---|---|---|
| FMT 실제 두 단계 law | <code>SOURCE_STRUCTURE_FIXED</code> | Theorem 5와 formula (6.17)의 conditioning |
| 최종 outcome 변수 | <code>JOINT (A,N')</code> | 최종 residue와 survivor가 양쪽 결과에 의존 |
| published FMT numerical rate | <code>NOT EXPLICIT</code> | \(1-o(1)\), \(O\), \(\sim\) rate 미인쇄 |
| project \(F_{\rm out},F_{\rm in}\) | <code>PARAMETERIZED EXPLICIT</code> | Theory 53·55 |
| project sieve-good mass | <code>PARAMETERIZED EXPLICIT</code> | 식 (79.6) |
| independence 가정 | <code>NOT NEEDED</code> | conditional-law 합으로 증명 |
| same-law \(F_{\rm corr}\) | <code>OPEN</code> | 현재 source·project theorem 없음 |
| simultaneous good outcome | <code>OPEN</code> | 식 (79.10)의 왼쪽 입력 부재 |
| <code>PAP-11</code>, <code>DEP-R09</code> | <code>OPEN</code> | weighted correlation 및 앞선 PAP 장벽 |
| fixed \(2\times10^{-17}\), \(X_{\rm cert}\) | <code>OPEN</code> | root proof chain 미완료 |
| actual prime sweep·threshold calculator | <code>NOT READY / NOT RUN</code> | 새 bounded range 없음 |

## 6. Lean·Python 검증 범위

<code>source/dep_r09_fmt_construction_mass.py</code>와 표적시험은 exact
<code>Fraction</code>으로 다음을 검증한다.

1. product success와 sequential failure identity.
2. global same-law strict gate와 equality boundary의 실패.
3. fiberwise union gate.
4. Markov failure 상계와 fail-closed input domain.
5. source hash와 OPEN 상태의 machine-ledger 일치.

Lean 단일 정본은 식 (79.7)의 실수 대수, 식 (79.10)의 strict slack, 식 (79.11)이
식 (79.10)을 함의하는 충분조건, 그리고 finite outer/fiber bad-set 선택을 검증한다.
확률측도 자체, FMT analytic theorem, weighted character-sum 상계를 project-local
<code>axiom</code>으로 넣지 않는다. <code>sorry</code>, <code>admit</code>,
project-local <code>axiom</code>은 사용하지 않는다.

## 7. 다음 gate

다음 source-first 목표는 식 (79.8)의 correlation badness를 실제 joint
\((\mathbf A,\mathbf N')\) law에서 평균내는 것이다. 먼저 다음 두 경로를 구분한다.

1. **global joint route:** \(\mathbb EW\) 또는 \(F_{\rm corr}\)를 law 전체에서 상계.
2. **fiberwise route:** 모든 outer-good \(\boldsymbol a\)에서 uniform conditional 상계.

\(\mathbf A\)만 평균내고 \(\mathbf N'\) 의존성을 버리는 식은 충분하지 않다.
이 analytic input이 생기기 전에는 큰 prime 계산이 증명 공백을 메우지 못하므로
장시간 CPU 실험을 시작하지 않는다.

## 8. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  Springer proceedings (2018), pp.1--21,
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1),
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, Journal of the American Mathematical Society
  31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
