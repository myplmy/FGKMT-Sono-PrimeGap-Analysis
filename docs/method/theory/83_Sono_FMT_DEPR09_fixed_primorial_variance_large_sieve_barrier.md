# Theory 83 — DEP-R09 fixed-primorial variance source·large-sieve barrier 감사

- 상태:
  <code>SOURCE_RANGE_NO_DROP_IN /
  RAW_CLASSICAL_LARGE_SIEVE_CERTIFICATE_REJECTED /
  ACTUAL_VARIANCE_AND_DIRECT_CORRELATION_OPEN</code>
- 선행 정본: Theory 76--82
- 목표: Theory 82 식 (82.3)에 넣을 fully numerical prescribed-primorial
  character-energy 상계가 기존 문헌에 있는지 확인하고, 고전 large sieve를 직접
  쓰는 경로가 수치적으로 충분한지 판정한다.
- 비목적: 실제 \(V(Y,q)\)의 하한, 모든 large-sieve refinement의 불가능성,
  PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

## 1. 결론

현재 normalization은

\[
 q=P(x)/B_0,\qquad Y=q^d,\qquad 21\le d\le186
 \tag{83.1}
\]

이고 Theory 82의 충분조건은

\[
 V(Y,q)
 <
 \tau^2p_*
 \frac{Q_{\mathcal S}M_{\min}^2Y^2}
 {\varphi(q)N^2}.
 \tag{83.2}
\]

확인한 fixed-\(q\) variance 및 modulus-average 문헌에서 다음 조건을 동시에 만족하는
drop-in theorem은 식별되지 않았다.

1. 하나의 미리 정해진 growing primorial \(q\).
2. \(q=Y^{1/d}\), \(21\le d\le186\).
3. actual nonprincipal \(Z_\chi(Y)\) normalization.
4. 모든 multiplier와 finite cutoff.

더 나아가 Montgomery--Vaughan의 고전 large sieve를 \(\Lambda\) 계수에 직접 적용한
가장 낙관적인 no-loss certificate의 RHS를

\[
 B_{\rm LS}(Y,q)
 :=
 (Y+q^2)
 \sum_{n\le Y}\Lambda(n)^2
 \tag{83.3}
\]

라 하면, 모든 \(q\ge3,d\ge21\)에서

\[
 \boxed{
 B_{\rm LS}(Y,q)
 >
 e^{-4}\frac q{\varphi(q)}Y^2.}
 \tag{83.4}
\]

오른쪽은 final shift가 \(q\)개 residue에 완전 균등하고 다른 손실이 전혀 없다고
가정했을 때조차 식 (83.2)가 가질 수 있는 최대 envelope다. 따라서

\[
 V\le B_{\rm LS}
 \quad\hbox{하나만으로는}\quad
 V< V_{\rm gate}
 \tag{83.5}
\]

를 추론할 수 없다. 이 결과는 실제 \(V\)가 크다는 하한이 아니라
**해당 직접 upper-certificate가 너무 느슨하다는 논리적 판정**이다.

## 2. source range 대조

### 2.1 프로젝트 power regime

\[
 \delta:=\frac{\log q}{\log Y}=\frac1d
 \in\left[\frac1{186},\frac1{21}\right].
 \tag{83.6}
\]

따라서

\[
 q=Y^\delta\le Y^{1/21}\ll Y^{1/2}.
 \tag{83.7}
\]

### 2.2 Friedlander--Goldston와 Vaughan

Friedlander--Goldston 1996은 fixed-modulus variance의 직접 관련 source다. 그러나
natural asymptotic의 조건부 범위는 \(q\ge Y^{1/2+\epsilon}\) 쪽이며, 현재
\(q\le Y^{1/21}\)와 겹치지 않는다. 그 원문의 fully numerical current-range
upper theorem은 이번 검색에서 확인하지 못했다.

Vaughan 2001은 \(Q/2<q\le Q\)의 modulus average를 다룬다. 공개 theorem statement의
unconditional 범위는 \(Y(\log Y)^{-A}<Q<Y\) 쪽이고, GRH 아래에서도
\(Q>Y^{3/4+\epsilon}\)인 평균 결과다. 하나의 prescribed primorial을 선택하지 않는다.

Fiorilli 2013 PDF p.2는 당시 \(Q\le Y^{1/2}\)에서 asymptotic result가 조건부로도
알려지지 않았다고 정리하고, 위 두 source의 범위를 함께 설명한다. 이는
2026년까지의 전 문헌 부재 명제가 아니라 source 범위 대조용 역사적 진술이다.

### 2.3 Fiorilli--Martin의 경고가 뜻하는 것

Fiorilli--Martin 2023 Proposition 2.2는 \(q\asymp Y^\delta\)에서 Hooley 규모의
variance bound를 uniform하게 가정하면 모든 Dirichlet \(L\)-function의 영점이

\[
 \Re s>\frac12+\frac\delta2
 \tag{83.8}
\]

에 없다는 강한 결론이 따라옴을 보인다. 현재 endpoint는

\[
 d=21:\ \frac{11}{21},
 \qquad
 d=186:\ \frac{187}{372}.
 \tag{83.9}
\]

이 논문이 반증한 logarithmic/fixed-\(q\) universal Hooley conjecture를 현재
power regime의 직접 반례로 쓰면 안 된다. 올바른 교훈은 “natural full variance
bound 자체가 매우 깊은 입력이며, 단순한 초등 보조정리로 취급할 수 없다”는 것이다.

## 3. Montgomery--Vaughan 원문 정리와 multiplicative 전달

저자 공개 원 논문 printed p.119, Theorem 1은 길이 \(N\)인
trigonometric polynomial \(S\)와 modulo 1 최소간격 \(\delta\)에 대해

\[
 \sum_r|S(x_r)|^2
 \le
 (N+\delta^{-1})
 \sum_n|a_n|^2.
 \tag{83.10}
\]

를 준다. reduced Farey fractions \(a/r\), \(r\le Q\)는 서로
\(\delta\ge Q^{-2}\)만큼 떨어져 있으므로

\[
 \sum_{r\le Q}\ \sum_{\substack{a\bmod r\\(a,r)=1}}
 \left|S\!\left(\frac ar\right)\right|^2
 \le
 (N+Q^2)\sum_n|a_n|^2.
 \tag{83.11}
\]

primitive character의 Gauss-sum identity와 reduced residue characters의
Bessel inequality를 사용하면 표준 multiplicative form

\[
 \sum_{r\le Q}\frac r{\varphi(r)}
 \sum_{\chi\bmod r}^{*}
 \left|\sum_n a_n\chi(n)\right|^2
 \le
 (N+Q^2)\sum_n|a_n|^2
 \tag{83.12}
\]

가 나온다. 별표는 primitive character 합이다.

\(Q=q,N=Y,a_n=\Lambda(n)\)로 두고 \(r/\varphi(r)\ge1\)을 버리면
conductor가 \(q\)를 나누는 primitive core를 포함하는 no-loss RHS가 식 (83.3)이다.
actual imprimitive \(Z_\chi\)로 옮길 때는 \(p\mid q/r\)인 prime-power correction을
추적해야 한다. 이번 장벽 판정은 그 correction을 0으로 놓은 **더 유리한** 상황에서
이미 RHS가 gate보다 큼을 보인다. correction을 버린 식을 actual \(V\)의 완성된
upper theorem으로 주장하지 않는다.

## 4. \(\Lambda^2\) 질량의 명시적 하한

\[
 S_2(Y):=\sum_{n\le Y}\Lambda(n)^2,
 \qquad L:=\log Y.
 \tag{83.13}
\]

Dusart 2010 Theorem 5.2의 \(k=1\) 행은 \(t\ge2\)에서

\[
 |\vartheta(t)-t|
 <
 \frac{12323}{10000}\frac t{\log t}.
 \tag{83.14}
\]

\(a=12323/10000\)라 하면

\[
 \vartheta(Y)-\vartheta(Y/2)
 >
 Y\left\{
 \frac12-\frac aL-\frac{a}{2(L-\log2)}
 \right\}.
 \tag{83.15}
\]

현재 범위에서는 \(L=d\log q\ge21\log3>8\)이다. brace를 \(c(L)\)라 하면
\(c'(L)>0\)이고, \(\log2<7/10\)을 이용한 유리 상계

\[
 c(8)>
 \frac12-\frac{12323}{80000}
 -\frac{5\cdot12323}{73\cdot10000}
 >\frac14
 \tag{83.15a}
\]

가 성립한다. 120-dps 교차검산값은
\(c(8)=0.26163754981615089376\ldots\)다. 따라서 brace는 항상
\(1/4\)보다 크고
따라서

\[
 \vartheta(Y)-\vartheta(Y/2)>\frac Y4.
 \tag{83.16}
\]

\(Y/2<p\le Y\)인 prime에서는
\((\log p)^2\ge\log(Y/2)\log p\)이므로

\[
 \begin{aligned}
 S_2(Y)
 &\ge
 \sum_{Y/2<p\le Y}(\log p)^2\\
 &\ge
 \log(Y/2)\{\vartheta(Y)-\vartheta(Y/2)\}\\
 &>
 \frac Y4(L-\log2).
 \end{aligned}
 \tag{83.17}
\]

식 (83.3)에 넣으면

\[
 \frac{B_{\rm LS}}{Y^2}
 >
 \frac{L-\log2}{4}.
 \tag{83.18}
\]

\(t:=\log q\)라 하면 \(L=dt\), \(d\ge21\), \(\log2<t\)이므로

\[
 \boxed{
 \frac{B_{\rm LS}}{Y^2}
 >
 \frac{L-\log2}{4}
 >
 5t.}
 \tag{83.19}
\]

## 5. 가장 유리한 entropy gate

final shift는 많아야 \(q\)개 residue를 갖는다. 어떤 probability distribution도
최대 atom \(\alpha\)에 대해

\[
 \alpha\ge\frac1q.
 \tag{83.20}
\]

Theory 82에서 actual atom cap은 \(1/Q_{\mathcal S}\)이고
\(Q_{\mathcal S}\le q\)다. 또한

\[
 0<\tau\le e^{-2},\qquad
 0<p_*\le1,\qquad
 0<M_{\min}\le N.
 \tag{83.21}
\]

그러므로 식 (83.2)의 RHS를 \(V_{\rm gate}\)라 할 때

\[
 \boxed{
 \frac{V_{\rm gate}}{Y^2}
 \le
 e^{-4}\frac q{\varphi(q)}.}
 \tag{83.22}
\]

이는 actual parameter 평가가 아니라 shift entropy와 나머지 factor에 모두 최선값을
준 보편적 상한이다. inner entropy를 더 개선해도 이 envelope를 넘을 수 없다.

## 6. Rosser--Schoenfeld와 strict 비교

Rosser--Schoenfeld 1962 printed p.72의 식 (3.41)은 \(q\ge3\)에서

\[
 \frac q{\varphi(q)}
 <
 e^\gamma\log\log q+
 \frac{5}{2\log\log q}
 \tag{83.23}
\]

이고 \(q=223092870\) 하나에는 \(5/2\) 대신 \(2.50637\)을 쓴 식 (3.42)가
적용된다. 큰 exceptional coefficient를 모든 \(q\ge3\)에 쓰면 안전하게

\[
 \frac q{\varphi(q)}
 <
 R(t):=
 e^\gamma\log t+\frac{2.50637}{\log t},
 \qquad t=\log q.
 \tag{83.24}
\]

를 얻는다.

\[
 f(t):=5t-e^{-4}R(t).
 \tag{83.25}
\]

이면

\[
 f'(t)
 =
 5-\frac{e^{\gamma-4}}t+
 \frac{2.50637e^{-4}}{t(\log t)^2}>0
 \qquad(t\ge\log3).
 \tag{83.26}
\]

마지막 부등식에는 \(0<\gamma<1\), \(t>1\)만으로 첫 두 항이 4보다 크다는
사실을 쓴다. endpoint는
\(e^4>50\), \(1<\log3<2\), \(\log\log3>1/20\),
\(e^\gamma<2\)를 쓰면

\[
 e^{-4}R(\log3)<\frac{53}{50}<5<5\log3,
 \tag{83.27}
\]

이므로 \(f(\log3)>0\)다. 식 (83.19), (83.22), (83.24)를 합치면 식 (83.4)가
성립한다.

Python 120-dps endpoint 진단은 더 보수적인 Rosser envelope에 대해서도

\[
 \begin{aligned}
 \frac{B_{\rm LS}}{Y^2}
 &>5.59442772036758955247\ldots,\\
 e^{-4}R(\log3)
 &=0.49117885863418770887\ldots,\\
 \text{margin}
 &>5.10324886173340184359\ldots
 \end{aligned}
 \tag{83.28}
\]

를 준다. 이 decimal은 증명을 대체하지 않고 endpoint 교차검산만 한다.

## 7. 왜 “상계가 gate보다 큼”은 경로 기각인가

strict 목표가 \(V<G\)이고 보유 정보가 \(V\le B\)뿐이라고 하자.
\(G\le B\)이면 추상값 \(V=G\)가

\[
 V\le B
 \quad\hbox{이지만}\quad
 \neg(V<G)
 \tag{83.29}
\]

를 만족한다. 따라서 그 두 부등식만으로 strict 목표를 논리적으로 도출할 수 없다.
Lean은 이 countermodel terminal을 무공리로 검사한다.

이 논리는 실제 \(V\)가 \(G\) 이상이라고 말하지 않는다. 실제 \(V\)는 훨씬 작을 수
있으며, 그것을 보여 주는 prime-specific cancellation theorem이 바로 남은 입력이다.

## 8. 배제되는 것과 남는 것

### 8.1 이번에 배제되는 경로

- raw classical large sieve의 전체 RHS를 그대로 식 (83.2)에 넣는 방식.
- modulus-average RHS가 prescribed primorial을 자동 선택한다고 보는 방식.
- final-shift entropy만 계속 키우면 raw RHS가 언젠가 gate 아래로 간다는 방식.

### 8.2 배제되지 않는 경로

- conductor가 \(q\)의 divisor인 sparse family만 쓰는 강화 large sieve.
- \(\Lambda\)와 primorial 구조를 쓰는 prime-specific variance bound.
- full \(V\) 대신 actual \(C_\chi(\omega)Z_\chi(Y)\)만 직접 제어하는
  same-law weighted correlation.
- pre-absolute-value cancellation 또는 fixed-primorial explicit formula.
- 새로운 fully numerical zero-density/PNT-in-AP transfer.

## 9. 코드·Lean 검증 범위

<code>source/dep_r09_fixed_primorial_variance_barrier.py</code>와 단위시험은
다음을 확인한다.

1. \(q=3,30,210,2310,30030,510510\)의 exact \(\varphi(q)\).
2. \(d=21,186\)에서 Dusart coefficient가 \(1/4\)보다 큼.
3. actual \(e^{-4}q/\varphi(q)\)가 Rosser envelope 아래임.
4. 각 sample의 conservative barrier margin이 양수임.
5. equality인 upper certificate는 strict gate를 통과시키지 않음.
6. source hash와 모든 OPEN status의 fail-closed 검증.

Lean은 식 (83.19)의 실수 선형대수, 식 (83.22)의 factor monotonicity,
식 (83.29)의 logical countermodel만 검사한다. Montgomery--Vaughan,
Dusart, Rosser--Schoenfeld의 analytic source theorem과 실제 character energy를
project-local axiom으로 넣지 않는다.

## 10. 현재 판정

| 항목 | 판정 |
|---|---|
| source regime normalization | <code>EXACT</code> |
| Montgomery--Vaughan 원문 constant | <code>PRIMARY SOURCE VERIFIED</code> |
| \(\Lambda^2\) RHS lower envelope | <code>PARAMETERIZED EXPLICIT</code> |
| raw large-sieve certificate의 Theory-82 gate 적합성 | <code>REJECTED</code> |
| actual \(V(Y,q)\)의 lower 또는 upper theorem | <code>OPEN</code> |
| prescribed-primorial natural variance drop-in | <code>NOT IDENTIFIED</code> |
| PAP-11·DEP-R09 | <code>OPEN</code> |
| fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\) | <code>OPEN</code> |
| 새 bounded \(X_{\rm cert}\) 범위 | <code>NONE</code> |
| threshold calculator·장시간 prime 계산 | <code>NOT READY / NOT RUN</code> |

## 11. 다음 gate

다음 최소 목표는 다음 셋 중 하나다.

1. divisor-conductor family에 특화된 fully numerical fixed-primorial energy bound.
2. full \(V\)보다 약한 actual same-law weighted-correlation theorem.
3. FMT outer law와 결합 가능한 prime-specific conditional variance theorem.

어느 하나도 source theorem·multiplier·cutoff가 고정되기 전에는
threshold calculator나 장시간 prime sweep을 시작하지 않는다.

## 12. 참고문헌

- H. L. Montgomery and R. C. Vaughan, “The large sieve,”
  Mathematika 20 (1973), 119--134,
  [DOI 10.1112/S0025579300004708](https://doi.org/10.1112/S0025579300004708).
- J. B. Friedlander and D. A. Goldston,
  “Variance of distribution of primes in residue classes,”
  [DOI 10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
- R. C. Vaughan,
  “On a variance associated with the distribution of primes in arithmetic progressions,”
  [DOI 10.1112/plms/82.3.533](https://doi.org/10.1112/plms/82.3.533).
- D. Fiorilli, “The distribution of the variance of primes in arithmetic progressions,”
  [arXiv:1301.5663](https://arxiv.org/abs/1301.5663).
- D. Fiorilli and G. Martin, “Disproving Hooley's conjecture,”
  [DOI 10.4171/JEMS/1291](https://doi.org/10.4171/JEMS/1291),
  [arXiv:2008.05837](https://arxiv.org/abs/2008.05837).
- J. B. Rosser and L. Schoenfeld,
  “Approximate formulas for some functions of prime numbers,”
  Illinois J. Math. 6 (1962), 64--94.
- P. Dusart, “Estimates of some functions over primes without R.H.,”
  [arXiv:1002.0442](https://arxiv.org/abs/1002.0442).
