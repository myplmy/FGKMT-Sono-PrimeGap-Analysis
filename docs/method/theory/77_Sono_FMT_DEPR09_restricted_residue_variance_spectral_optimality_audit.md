# Theory 77 — DEP-R09 제한 잔여류 분산·spectral optimality 감사

- 작성일: 2026-09-14
- 선행 정본: [Theory 76](76_Sono_FMT_DEPR09_preabsolute_moment_pointwise_PNT_source_audit.md)
- 기계 원장:
  [restricted-residue variance screen v1](data/Sono_FMT_DEPR09_restricted_residue_variance_screen_v1.json)
- 결론 상태:
  `NO_NUMERICAL_FIXED_PRIMORIAL_VARIANCE_DROP_IN / UNWEIGHTED_CHARACTER_ENERGY_ROUTE_CLOSED / DIRECT_WEIGHTED_CORRELATION_OPEN`
- 전역 상태: `PAP-11 OPEN`, `DEP-R09 OPEN`, fixed (2\times10^{-17}) 미인증,
  numerical (X_{\rm cert}) `OPEN`

## 1. 질문과 결론

Theory 76은 Maier가 각 admissible column에 pointwise PNT를 쓰지만 마지막 행 선택은
그 열들의 **총 prime mass**만 소비한다는 점을 이용해 더 약한 aggregate second-moment
충분조건을 만들었다. 이번 감사는 두 질문을 검토한다.

1. 그 충분조건을 그대로 공급하는 기존 fixed-primorial variance 정리가 있는가?
2. Maier가 고른 특별한 admissible set의 character energy가 일반적인 (M)개 집합보다
   작아서 조건을 더 완화할 수 있는가?

판정은 다음과 같다.

\[
 \boxed{\text{현재 계약에 바로 들어가는 fully numerical source는 식별되지 않았다.}}
 \tag{77.1}
\]

더 중요한 교정은 두 번째 질문이다. 서로 다른 (M)개 reduced residues로 이루어진
어떤 집합에도 전체 character energy는 정확히 (arphi(q)M)이다. 따라서 Maier 집합의
**unweighted total (L^2) energy 자체를 줄이는 경로는 불가능**하다. 남은 최소 목표는
전체 variance가 아니라, Maier의 짧은 shifted character sum과 실제 prime-error vector의
직접 상관을 제어하는 정리다.

이것은 모든 cancellation·weighted-moment 접근의 불가능성 명제가 아니다. 단지 집합의
크기 (M)과 unweighted (L^2) norm만 쓰는 Cauchy 경로가 이미 sharp하다는 뜻이다.

## 2. Maier 원문에서 실제로 필요한 소비식

(q=P(x)=\prod_{p<x}p)라 하고 Maier의 행렬을

\[
 a_{r,s}=y+s+rq,
 \qquad 1\le r\le q^{D-1},\quad 1\le s\le U
 \tag{77.2}
\]

로 쓴다. (U<q)인 충분히 큰 범위에서 admissible columns의 서로 다른 reduced residue
집합은

\[
 \mathcal A_y=
 \{,y+s\pmod q:1\le s\le U,\ (y+s,q)=1,\},
 \qquad M=|\mathcal A_y|
 \tag{77.3}
\]

이다. Maier printed p.266은 각 admissible column에 Gallagher Lemma 2를 적용하고,
그 결과를 합해 p.267의 formula (I)를 얻는다.

\[
 |\mathcal P|\ge C_3E q^{D-1}.
 \tag{77.4}
\]

이후 dense row 제거는 개별 열의 하한을 다시 보지 않고 식 (77.4)의 총량을 쓴다. 따라서
같은 (mathcal A_y)에 대해 총 prime mass 하한을 직접 주는 정리는 formula (I)의 pointwise
호출을 논리적으로 대체할 수 있다.

그러나 가까운 두 열에 prime이 함께 생기는 수를 제어하는 formula (II)는 별도다.

\[
 \#\{\text{small prime pairs}\}
 < C_4E^2q^{D-1}/A.
 \tag{77.5}
\]

aggregate variance redesign은 식 (77.4)만 대체한다. 식 (77.5)와 뒤의 row-deletion 상수는
R10에서 따로 명시화해야 한다. 또한 모든 (y)에 대한 평균에서 좋은 하나를 고르는 것으로는
충분하지 않다. 같은 (y)가 Maier Lemma 6의 sparse-survivor 성질도 만족한다는 동시 선택
논리가 필요하다.

## 3. Character energy는 집합 구조와 무관하게 고정된다

모든 Dirichlet characters modulo (q)에 대해

\[
 C_\chi(\mathcal A)
 :=\sum_{a\in\mathcal A}\overline{\chi(a)}
 \tag{77.6}
\]

라고 둔다. (mathcal A)가 서로 다른 reduced residues (M)개로 이루어졌으면 finite
character orthogonality로

\[
 \sum_{\chi\bmod q}|C_\chi(\mathcal A)|^2
 =\varphi(q)M.
 \tag{77.7}
\]

주지표 (chi_0)에서는 (C_{\chi_0}=M)이므로

\[
 |C_{\chi_0}(\mathcal A)|^2=M^2,
 \tag{77.8}
\]

\[
 \boxed{
 \sum_{\substack{\chi\bmod q\\\chi\ne\chi_0}}
 |C_\chi(\mathcal A)|^2
 =\varphi(q)M-M^2=M\{\varphi(q)-M\}.}
 \tag{77.9}
\]

따라서 (mathcal A_y)가 Maier sieve로 특별하게 선택됐다는 사실은 total unweighted
character energy를 줄이지 않는다. 구조는 에너지가 **어떤 characters에 분포하는지**와
prime errors (Z_\chi(Y))와의 상관에는 영향을 줄 수 있지만, 합 자체에는 영향을 주지 않는다.

## 4. 주지표를 분리한 정확한 충분 budget

Theory 76의 character expansion을

\[
 E_q(a;Y)=\frac1{\varphi(q)}
 \sum_{\chi\bmod q}\overline{\chi(a)}Z_\chi(Y)
 \tag{77.10}
\]

로 쓴다. 주지표가 어떤 (0\le\delta_0<\varepsilon)에 대해

\[
 |Z_{\chi_0}(Y)|\le\delta_0Y
 \tag{77.11}
\]

를 만족한다고 가정한다. 비주지표 부분에 Cauchy--Schwarz와 식 (77.9)를 쓰면

\[
 \left|
 \sum_{\chi\ne\chi_0}C_\chi(\mathcal A)Z_\chi(Y)
 \right|^2
 \le M\{\varphi(q)-M\}
 \sum_{\chi\ne\chi_0}|Z_\chi(Y)|^2.
 \tag{77.12}
\]

그러므로 aggregate target을 보장하는 한 가지 충분조건은

\[
 \boxed{
 \sum_{\chi\ne\chi_0}|Z_\chi(Y)|^2
 \le
 (\varepsilon-\delta_0)^2
 \frac{M Y^2}{\varphi(q)-M}.}
 \tag{77.13}
\]

이다. (delta_0=0)에서 Theory 76 식 (76.23)에 대한 budget 비는

\[
 \frac{\varphi(q)}{\varphi(q)-M}.
 \tag{77.14}
\]

Maier 범위에서는 (M)이 (q)보다 subexponential인 반면 (arphi(q))는 (q) 규모이므로
이 비는 1에 가깝다. 즉 주지표 분리는 논리적으로 정확하지만 missing nonprincipal variance
theorem을 크게 쉽게 만들지는 않는다. (delta_0>0)이면 남은 budget은
((1-\delta_0/\varepsilon)^2)만큼 더 줄어든다.

## 5. Unweighted (L^2)만으로는 더 좋아질 수 없다

식 (77.12)의 Cauchy 상수는 임의의 error vector에 대해 sharp하다. 실제로 어떤 실수 (t)에
대해

\[
 Z_\chi=t\,\overline{C_\chi(\mathcal A)}
 \quad(\chi\ne\chi_0)
 \tag{77.15}
\]

로 두면 양변이 모두

\[
 t^2\left(
 \sum_{\chi\ne\chi_0}|C_\chi(\mathcal A)|^2
 \right)^2
 \tag{77.16}
\]

이 된다. 이것은 실제 (Z_\chi(Y))가 이렇게 정렬된다고 주장하는 것이 아니다. 다음의 좁은
결론만 준다.

> 집합의 크기와 두 unweighted total (L^2) norm만 아는 상태에서는 식 (77.12)의
> 보편 상수를 개선할 수 없다.

따라서 다음 단계에서 필요한 추가 정보는 weighted spectral distribution, character별
conductor·zero 위치, 부호/위상, 또는 Maier-selected (y)와의 decorrelation이다.

## 6. 문헌 source-screen

| 문헌 | 제공하는 정보 | 현재 계약 판정 |
|---|---|---|
| Friedlander--Goldston 1996 | fixed-(q) residue variance를 직접 연구 | 관련성 높음. 그러나 (q=Y^{1/d}), (21\le d\le186)의 한 primorial에 unconditional fully numerical upper를 주는 drop-in은 확인되지 않음 |
| Fiorilli 2013/2015 | moderate (q) variance 분포와 natural scale을 GRH·LI 아래 분석 | conditional/heuristic; numerical certificate 아님 |
| Fiorilli--Martin 2023 | Hooley의 (G(Y;q)\ll Y\log q)가 모든 작은 (q)에서 성립하지 않음을 증명; power regime의 uniform bound가 zero-free strip을 함의함 | full natural variance를 손쉬운 입력으로 가정하면 안 된다는 경고. 다만 Maier weighted target의 반례는 아님 |
| Vaughan 2001 및 BDH 계열 | (q)에 대한 평균 variance/moment | Maier가 선택한 특정 nested primorial과 양화사 불일치 |
| Maynard large-moduli III | convenient divisors를 가진 (q>Y^{1/2}) 평균에서 residue-class uniformity | 현재 (q=Y^{1/d}\le Y^{1/21})와 regime가 반대이고 fixed-(q) 정리가 아님 |
| Montgomery--Vaughan 1986 | reduced residues 자체의 분포 | (mathcal A_y)의 combinatorics에는 관련되지만 prime-error vector와의 상관은 제어하지 않음 |

특히 Fiorilli--Martin Proposition 2.2에 (delta=1/d)를 넣으면, power regime
(q\asymp Y^{1/d})에서 Hooley 크기의 full variance upper를 uniform하게 보이는 일은 모든
관련 Dirichlet (L)-functions에 대해

\[
 \Re(s)>\frac12+\frac1{2d}
 \tag{77.17}
\]

인 zero-free half-plane을 함의한다. 현재 (21\le d\le186)에서는 경계가 각각
(11/21)과 (187/372)다. 이는 full variance 목표가 상당히 강하다는 진단이다. 해당 논문의
반례는 주로 (q\asymp\log\log Y)인 다른 regime이므로 식 (77.13)이나 아래의 더 약한
weighted target을 반증하지 않는다.

## 7. 현재의 최소 analytic target

full variance 식 (77.13)은 충분하지만 필요조건은 아니다. 실제로 필요한 최소 입력은

\[
 \boxed{
 \left|
 \sum_{\chi\ne\chi_0}
 C_\chi(\mathcal A_y)Z_\chi(Y)
 \right|
 \le(\varepsilon-\delta_0)MY.}
 \tag{77.18}
\]

이다. Dirichlet character는 nonunit에서 0이므로 Maier set의 coefficient는

\[
 C_\chi(\mathcal A_y)
 =\sum_{1\le s\le U}\overline{\chi(y+s)}.
 \tag{77.19}
\]

즉 길이

\[
 U=E x\frac{\log x\,\log_3x}{(\log_2x)^2}
 =q^{o(1)}
 \tag{77.20}
\]

인 ultra-short shifted character sum이다. 일반 Pólya--Vinogradov나 Burgess 상계는 이
짧은 길이에서 자동으로 유용한 saving을 주지 않는다. 반대로 식 (77.18)은 full variance보다
훨씬 선택적이므로, 다음 세 형태를 source-first로 조사할 가치가 있다.

1. (C_\chi(\mathcal A_y))를 weight로 직접 포함한 explicit character-error correlation.
2. conductor/height별 weight (w_\chi)를 둔 dual weighted moment.
3. Maier Lemma 6의 survivor 조건을 보존하는 construction-choice 평균과 동시 good-(y) 선택.

세 경로 모두 principal/exceptional character, endpoint, prime powers, (psi\to\pi), formula
(II)와 공통 finite cutoff를 마지막에 합성해야 한다. 단순히 평균 (y) 하나가 좋다는 사실을
Maier가 고른 (y)로 바꿔 쓰면 안 된다.

## 8. 계산·Lean 검증의 경계

`source/dep_r09_restricted_residue_variance.py`와 단위시험은 다음만 재계산한다.

- 식 (77.7)--(77.9)의 exact energy 분해,
- 식 (77.13)--(77.14)의 scalar budget,
- 식 (77.15)--(77.16)의 Cauchy equality witness,
- 식 (77.17)의 (d=21,186) exact rational endpoints.

Lean 단일 정본은 energy 분해와 식 (77.13)의 terminal implication을 premise-explicit 형태로
검사한다. finite character orthogonality와 문헌의 analytic theorem을 project-local axiom으로
넣지 않는다. 따라서 energy 항등식은 `KERNEL_PASS`, moment-to-target 합성은
`CONDITIONAL_KERNEL_PASS`, 문헌 source theorem은 `SOURCE_THEOREM_UNFORMALIZED`다.
`sorry`, `admit`, project-local `axiom`은 사용하지 않는다.

## 9. 판정표

| 항목 | 상태 |
|---|---|
| Maier formula (I)의 aggregate consumer 확인 | `DONE` |
| formula (II)가 별도 R10 입력임을 확인 | `DONE` |
| total·nonprincipal character energy | `EXACT / KERNEL_PASS` |
| Maier 구조로 unweighted total energy 감소 | `REJECTED_AS_STATED` |
| principal-separated sufficient budget | `DERIVED / CONDITIONAL_KERNEL_PASS` |
| Cauchy의 energy-only 보편 개선 | `IMPOSSIBLE / EXACT EQUALITY WITNESS` |
| numerical fixed-primorial full variance source | `NOT IDENTIFIED` |
| direct weighted correlation source | `NOT IDENTIFIED` |
| 모든 weighted/correlation proof의 불가능성 | `NOT CLAIMED` |
| `PAP-11`, `DEP-R09` | `OPEN` |
| fixed (2\times10^{-17}), numerical (X_{\rm cert}) | `OPEN` |
| threshold calculator·actual prime 계산 | `NOT READY / NOT RUN` |

## 10. 다음 gate와 예상 연구량

다음 우선순위는 식 (77.18)의 direct weighted correlation을 source-first로 분해하는 것이다.

1. Maier-selected (y)의 construction family와 simultaneous-selection quantifier 고정:
   약 1--2주.
2. (C_\chi(\mathcal A_y))의 conductor/height별 spectral profile 및 기존 shifted character-sum
   정리 적용성 감사: 약 2--6주.
3. 기존 정리가 맞으면 numerical specialization과 common cutoff: 약 1--3개월.
4. 새 analytic theorem이 필요하면: 6--24개월 이상, 성공 불확실.

현재 장시간 prime 계산은 이 증명 입력을 만들지 못한다. 새 numerical theorem과 finite cutoff가
생기기 전에는 threshold calculator도 만들지 않는다.

## 11. 참고문헌

- H. Maier, *Chains of Large Gaps between Consecutive Primes*, Advances in Mathematics 39
  (1981), 257--269, DOI
  [10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- J. B. Friedlander and D. A. Goldston, *Variance of Distribution of Primes in Residue
  Classes*, Quart. J. Math. 47 (1996), 313--336, DOI
  [10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
- D. Fiorilli, *The Distribution of the Variance of Primes in Arithmetic Progressions*,
  Int. Math. Res. Not. 2015, [arXiv:1301.5663](https://arxiv.org/abs/1301.5663).
- D. Fiorilli and G. Martin, *Disproving Hooley's Conjecture*, J. Eur. Math. Soc. 25
  (2023), 4791--4812, DOI
  [10.4171/JEMS/1291](https://doi.org/10.4171/JEMS/1291),
  [arXiv:2008.05837](https://arxiv.org/abs/2008.05837).
- R. C. Vaughan, *On a Variance Associated with the Distribution of General Sequences in
  Arithmetic Progressions*, Proc. Lond. Math. Soc. 82 (2001), 533--553, DOI
  [10.1112/S0024611501000081](https://doi.org/10.1112/S0024611501000081).
- J. Maynard, *Primes in Arithmetic Progressions to Large Moduli III: Uniform Residue
  Classes*, Memoirs AMS 308 (2025), no. 1544,
  [arXiv:2006.08250](https://arxiv.org/abs/2006.08250), DOI
  [10.1090/memo/1544](https://doi.org/10.1090/memo/1544).
- H. L. Montgomery and R. C. Vaughan, *On the Distribution of Reduced Residues*, Annals
  of Mathematics 123 (1986), 311--333, DOI
  [10.2307/1971274](https://doi.org/10.2307/1971274).
