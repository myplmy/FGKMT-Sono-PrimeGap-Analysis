# Theory 78 — DEP-R09 Maier/FMT CRT 이동량 양화사·동시 선택 감사

- 작성일: 2026-09-14 KST
- 선행 정본:
  [Theory 77](77_Sono_FMT_DEPR09_restricted_residue_variance_spectral_optimality_audit.md)
- 기계 원장:
  [Maier shift-selection v1](data/Sono_FMT_DEPR09_Maier_shift_selection_v1.json)
- 판정:
  <code>CLASSICAL_FIXED_PARTITION_SHIFT_IS_SINGLETON /
  SONO_FMT_RANDOMIZED_VECTOR_FAMILY_EXISTS_BUT_NUMERICAL_JOINT_GOOD_MASS_OPEN /
  DIRECT_UNIFORM_CORRELATION_OPEN</code>
- 계속 OPEN: <code>PAP-11</code>, <code>DEP-R09</code>, fixed \(2\times10^{-17}\),
  numerical \(X_{\rm cert}\)

> **Theory 79 successor correction:** FMT의 최종 construction outcome은
> \(\boldsymbol a\) 하나가 아니라 first-stage \(\mathbf A\)와 conditional
> hypergraph output \(\mathbf N'\)의 joint/sequential pair다. 출판 원문의
> \(1-o(1)\) rate는 비수치지만 project Theory 53·55의 finite bounds를 쓰면
> sieve-good mass 자체는
> \((1-F_{\rm out})(1-F_{\rm in})\) 이상으로 parameterized explicit이다.
> same-law weighted-correlation failure bound는 계속 OPEN이다.
> 정본은 [Theory 79](79_Sono_FMT_DEPR09_FMT_construction_law_finite_mass_audit.md)와
> [review 87](../../review/87_20260914_DEPR09_FMT_construction_law_finite_mass_타당성검토.md)이다.

## 1. 결론

Theory 77의 마지막 제안 중 “Maier Lemma 6의 성질과 weighted correlation이 동시에 좋은
\(y\)를 평균으로 고른다”는 문구는 그대로는 너무 넓었다. Maier 1981 Lemma 6의 인쇄된
구성에서 \(v,w\)를 고정하면

\[
 y\equiv0\pmod {P_1P_3},\qquad
 y\equiv1\pmod {P_2}
\tag{78.1}
\]

이고 \(P(x)=P_1P_2P_3\)의 세 인수가 서로소이므로 중국인의 나머지 정리에 따라

\[
 \boxed{\text{허용되는 }y\bmod P(x)\text{는 정확히 하나다.}}
\tag{78.2}
\]

따라서 고정된 Maier 분할 안에는 평균을 낼 자유로운 \(y\)-표본공간이 없다. 이 한 점에서
평균 상계로 좋은 점을 고르려면 모든 bad set이 비어 있음을 이미 증명해야 하므로 평균
선택의 이점이 사라진다.

그러나 Sono/Ford--Maynard--Tao의 실제 증명에는 더 큰 표본공간 후보가 있다. sieve residue
vector

\[
 \boldsymbol a=(a_p\bmod p)_{p\le x,\ p\ne B_0}
\tag{78.3}
\]

하나를 정하면 CRT가 \(m(\boldsymbol a)\bmod P\)를 정확히 하나 정한다. FMT Sections 4--6은
\(\boldsymbol a\) 자체를 무작위로 구성한다. 그러므로 평균 경로를 완전히 기각할 수는 없지만,
다음 새 정리가 필요하다.

> sieve의 global·short-interval 조건을 만족하는 vector와 direct weighted correlation을
> 만족하는 vector가 **같은 하나**임을 positive finite mass로 보장한다.

현재 문헌과 프로젝트 정본에는 이 둘의 공통 numerical failure budget이 없다. 따라서
동시 선택은 <code>OPEN</code>이고 numerical \(X_{\rm cert}\) 범위도 생기지 않았다.

## 2. Maier 1981 원문의 단일 CRT 이동량

Maier printed pp.263--264의 Lemma 6은

\[
 P(x)=P_1P_2P_3
\tag{78.4}
\]

로 소수 범위를 세 조각으로 나누고 식 (78.1)의 \(y\)를 택한다. fixed \(v,w\)에서 각
prime은 정확히 한 \(P_i\)에 들어가므로 세 인수는 pairwise coprime이다. CRT uniqueness는
식 (78.2)를 준다. 대표값 \(0<y\le P(x)\)까지 정하면 정수 \(y\)도 하나다.

같은 \(y\)는 이후 printed pp.266--268에서 동시에 다음을 결정한다.

1. admissible columns \((y+s,P(x))=1\),
2. formula (I)의 전체 prime mass,
3. formula (II)의 가까운 admissible-column pair 수,
4. 마지막에 선택되는 한 matrix row.

따라서 survivor 조건에는 \(y_1\), correlation 조건에는 \(y_2\)를 따로 골라 놓고
\(y_1=y_2\)라고 간주하면 양화사 오류다.

## 3. Sono/FMT 실제 구성에서는 무엇이 달라지는가

Sono Proposition 3.1과 FMT Theorem 2는 하나의 고정된 삼분할 대신 각 prime에 residue
\(a_p\bmod p\)를 지정해

\[
 \mathcal T(\boldsymbol a)
 =\{n\in[y]\setminus[x]:
 n\not\equiv a_p\pmod p\ \text{for all }p\le x,\ p\ne B_0\}
\tag{78.5}
\]

를 만든다. 이후

\[
 m(\boldsymbol a)\equiv-a_p\pmod p
 \quad(p\le x,\ p\ne B_0)
\tag{78.6}
\]

로 \(m(\boldsymbol a)\bmod P\)가 하나 정해진다. Sono printed pp.528--530은 이
\(\mathcal T,m\)을 고정한 뒤 \(z\in[Z]\)만 무작위로 택하며, 각
\(a\in\mathcal T\)에 pointwise PAP를 적용한다.

FMT 원문은 \(\boldsymbol a\)를 만드는 proof 내부에 무작위 vector를 사용하므로 잠재적인
construction family는 있다. 하지만 출판된 최종 Theorem 2는 “조건을 만족하는 vector가
존재한다”는 문장이고, 현재 프로젝트의 finite 재증명도 weighted prime-error correlation과
결합된 공통 확률을 제공하지 않는다. 따라서 다음 둘을 구분한다.

- **uniform route:** 모든 construction vector에 correlation 상계가 성립하면 이미 선택된
  \(\boldsymbol a\)에도 성립한다. 별도 동시 선택이 필요 없다.
- **average route:** correlation이 vector 평균에서만 좋다면 sieve-good event와 같은
  확률공간에서 failure mass를 동시에 수치화해야 한다.

## 4. 최소 finite 동시 선택 lemma

construction family를 유한집합 \(\Omega\)라 하고,

\[
\begin{aligned}
B_{\rm sieve}&=\{\omega:\text{global 또는 short-interval sieve 조건 실패}\},\\
B_{\rm corr}&=\{\omega:\text{weighted correlation 조건 실패}\},\\
B_{\rm extra}&=\{\omega:\text{추가 pair·endpoint 조건 실패}\}
\end{aligned}
\tag{78.7}
\]

로 둔다. 그러면

\[
 |B_{\rm sieve}|+|B_{\rm corr}|+|B_{\rm extra}|<|\Omega|
\tag{78.8}
\]

이면 union bound에 의해

\[
 \exists\omega\in\Omega,\quad
 \omega\notin B_{\rm sieve}\cup B_{\rm corr}\cup B_{\rm extra}.
\tag{78.9}
\]

균등분포에서는 식 (78.8)이 세 failure probability의 합이 1보다 작다는 조건과 같다.
비균등분포이면 cardinality가 아니라 probability mass로 같은 식을 써야 한다.

비음수 badness \(W(\omega)\)의 합만 아는 경우

\[
 \#\{\omega:W(\omega)\ge t\}
 \le
 \left\lfloor\frac{\sum_{\omega\in\Omega}W(\omega)}{t}\right\rfloor
\qquad(t>0)
\tag{78.10}
\]

가 Markov의 exact finite 형태다. 식 (78.8)--(78.10)은 선택 논리만 닫으며,
\(\sum W\)의 analytic 상계는 새 입력이다.

고전 Maier fixed partition에서는 \(|\Omega|=1\)이다. 이때 식 (78.8)은

\[
 |B_{\rm sieve}|=|B_{\rm corr}|=|B_{\rm extra}|=0
\tag{78.11}
\]

일 때만 성립한다. 이것이 “원래 \(y\) 하나를 평균으로 구제할 수 없다”는 정확한 뜻이다.

## 5. weighted correlation 목표의 올바른 변수

Sono/FMT vector family를 사용하는 경우 Theory 77 식 (77.18)은

\[
\left|
\sum_{\chi\ne\chi_0}
C_\chi(\mathcal A_{\boldsymbol a})Z_\chi(Y)
\right|
\le(\varepsilon-\delta_0)M_{\boldsymbol a}Y,
\tag{78.12}
\]

\[
C_\chi(\mathcal A_{\boldsymbol a})
=\sum_{s\in\mathcal T(\boldsymbol a)}
\overline{\chi(m(\boldsymbol a)+s)}
\tag{78.13}
\]

로 다시 써야 한다. 고전 Maier의 연속 block
\(\sum_{1\le s\le U}\overline{\chi(y+s)}\)는 고정 삼분할에 대응하는 특수한 경우다.
실제 Sono proof를 개선하려면 \(\mathcal T(\boldsymbol a)\)와
\(m(\boldsymbol a)\)의 **결합 의존성**을 보존해야 한다.

따라서 “일반 shifted character sum 정리”를 찾는 것만으로 충분하지 않다. 그 정리가
모든 \(\boldsymbol a\)에 uniform한지, 아니면 FMT construction law에 대한 평균인지까지
확인해야 한다.

## 6. source-first 문헌 판정

| source | 확인한 내용 | 이번 판정 |
|---|---|---|
| Maier 1981, Lemma 6·pp.266--268 | fixed \(P_1,P_2,P_3\)에서 한 CRT \(y\), 같은 \(y\)로 formulas (I),(II) | 고전 \(y\)-평균 표본공간은 없음 |
| Sono 2025, Proposition 3.1·Theorem 3.6 proof | \(\boldsymbol a\)마다 한 CRT \(m\), 이후 \(z\) 평균 | actual 변수는 \(m,\mathcal T\)의 결합 |
| Ford--Maynard--Tao 2018, Theorem 2·Sections 4--6 | random sieve vectors로 조건 좋은 \(\mathcal T\) 구성 | family 후보는 있으나 weighted correlation과의 numerical joint mass는 없음 |

이번 검색에서 식 (78.12)를 uniform하게 주거나, FMT construction law에서
\(B_{\rm sieve}\)와 \(B_{\rm corr}\)의 합동 finite failure budget을 주는 published theorem은
식별하지 못했다. 이는 그러한 정리의 전 문헌 부재를 증명한 것이 아니라 현재 source-screen의
결과다.

## 7. Lean·Python 검증 범위

<code>source/dep_r09_maier_shift_selection.py</code>와 단위시험은 다음만 exact하게 검사한다.

- \(|\Omega|-\sum_i|B_i|\)의 union-bound 잔여 하한,
- singleton family에서 bad count 하나만 있어도 선택 인증이 사라짐,
- rational Markov bad-count 상계,
- source·PAP·\(X_{\rm cert}\) 상태를 fail-closed로 저장.

Lean 단일 정본은 식 (78.8)에서 식 (78.9)로 가는 finite-set lemma와 식 (78.11)의
자연수 대수를 검사한다. analytic correlation, FMT random-construction theorem, CRT 자체를
project-local axiom으로 넣지 않는다. <code>sorry</code>, <code>admit</code>,
project-local <code>axiom</code>은 사용하지 않는다.

## 8. 판정과 다음 gate

| 항목 | 상태 |
|---|---|
| 고전 Maier fixed-partition의 \(y\) 개수 | <code>EXACTLY ONE MOD P(x)</code> |
| 고전 \(y\)-평균 simultaneous selection | <code>REJECTED AS STATED</code> |
| Sono/FMT vector당 CRT \(m\) | <code>UNIQUE</code> |
| FMT proof 내부 construction family | <code>EXISTS QUALITATIVELY</code> |
| sieve-good와 correlation-good의 공통 numerical mass | <code>NOT CERTIFIED</code> |
| finite union-selection lemma | <code>KERNEL_PASS</code> |
| uniform-in-vector direct correlation | <code>ANALYTIC SOURCE OPEN</code> |
| average-in-vector direct correlation | <code>JOINT MASS THEOREM OPEN</code> |
| formula (II) pair bound | <code>SEPARATE</code> |
| <code>PAP-11</code>, <code>DEP-R09</code> | <code>OPEN</code> |
| fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\) | <code>OPEN</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

다음 우선순위는 FMT Sections 4--6의 construction probability를 다시 열어
<code>sieve-good</code> failure mass를 finite하게 추출할 수 있는지 감사하고, 같은 확률공간에서
식 (78.12)의 평균을 표현할 수 있는지 판정하는 것이다. 이 단계가 실패하면 uniform-in-vector
correlation source가 필요하다. 어느 쪽도 큰 소수표 계산으로 대체되지 않으므로 장시간 CPU
실험은 아직 시작하지 않는다.

## 9. 참고문헌

- H. Maier, *Chains of Large Gaps between Consecutive Primes*, Advances in Mathematics
  39 (1981), 257--269,
  [doi:10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  Springer proceedings (2018), pp.1--21,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468).
- K. Sono, *An Explicit Lower Bound for Gaps between Some Consecutive Primes*,
  Tokyo Journal of Mathematics 48 (2025), 521--542,
  [doi:10.3836/tjm/1502179436](https://doi.org/10.3836/tjm/1502179436).
