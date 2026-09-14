# Sono/FMT DEP-R09 사전 절댓값 moment·pointwise PNT source 감사

- 작성일: 2026-09-14 KST
- 단계: **DEP-R09 / PRE-ABSOLUTE-VALUE MOMENT AND POINTWISE PNT SOURCE AUDIT**
- 선행 정본: [Theory 72](72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md),
  [Theory 73](73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md),
  [Theory 75](75_Sono_FMT_DEPR09_hybrid_smoothing_cancellation_transfer_feasibility.md)
- 기계 원장: [pre-absolute moment source screen v1](data/Sono_FMT_DEPR09_preabsolute_moment_source_screen_v1.json)
- 판정: **감사한 fully explicit L1·pointwise PNT source는 현재 PAP 계약을 통과하지 못한다.
  다만 Maier가 마지막에 소비하는 aggregate admissible-column count를 직접 제어하는
  second-moment 재설계는 논리적으로 살아 있으며, 이를 공급할 fully numerical theorem은 아직 없다.**
- 비목적: 모든 평균·분산 방법의 불가능성, 실제 소수분포 오차의 하한,
  `PAP-11`·`DEP-R09`·fixed $2\times10^{-17}$ 또는 numerical $X_{\rm cert}$ 인증

## 1. 이번 단계의 결론

Theory 75는 Gallagher 식 (30)에서 절댓값을 취한 뒤에는 character와 zero의 위상이 사라져
필요한 cancellation을 회복할 수 없다고 판정했다. 따라서 이번에는 절댓값을 취하기 전의
두 갈래를 원문에서 다시 조사했다.

1. Maier가 실제로 요구하는 모든 허용 residue class에 fully numerical pointwise PNT를 적용한다.
2. pointwise 오차를 각각 제어하지 않고 허용 열의 합을 먼저 만든 뒤 character second moment로
   그 합만 제어한다.

첫 갈래의 공개 명시적 후보인 Akbary--Hambrook, Sedunova, Bennett--Martin--O'Bryant--
Rechnitzer를 현 변수에 정규화했다. 앞의 두 L1 상계는 direct certificate에 양의
$Y(\log Y)^c$ floor가 남고, Bennett의 large-modulus pointwise 정리는 source cutoff 자체가
$d\le186$과 겹치지 않는다. 그러므로 이번에 감사한 후보 중 drop-in은 0개다.

두 번째 갈래는 Maier 원문의 quantifier를 다시 읽은 결과 단순한 희망이 아니라 정확한
충분조건으로 쓸 수 있다. 인쇄 증명은 각 허용 열에 pointwise Lemma 2를 적용하지만, 다음 단계가
쓰는 것은 허용 열 전체의 **총 소수 개수 하한**이다. 특정 허용 residue 집합의 aggregate error를
직접 제어하면 이 부분만은 교체할 수 있다. 그러나 그 강도·범위·상수·cutoff를 모두 갖춘
unconditional individual-primorial theorem은 식별하지 못했다.

\[
 \boxed{
 \begin{gathered}
 \text{explicit L1 / Bennett pointwise drop-in: FAILS CURRENT CONTRACT},\\
 \text{aggregate second-moment redesign: LOGICALLY SUFFICIENT BUT SOURCE OPEN}.
 \end{gathered}}
\tag{76.1}
\]

따라서 $PAP$-11, DEP-R09, fixed $2\times10^{-17}$와 $X_{\rm cert}$는 계속 `OPEN`이다.
새로운 수치 범위가 생기지 않았으므로 threshold calculator나 장시간 prime 계산을 시작하지 않는다.

## 2. 현재 PAP 계약과 기호

Maier modulus를 $q$, prime-count scale을 $Y=q^d$, 허용 residue 집합을
$\mathcal A\subseteq(\mathbb Z/q\mathbb Z)^\times$, 그 크기를 $M=|\mathcal A|$라 한다.
von Mangoldt count의 residue error를

\[
 E_q(a;Y):=\psi(Y;q,a)-\frac{Y}{\varphi(q)}
\tag{76.2}
\]

로 둔다. 현재 coefficient capacity와 Theory 72의 near budget은

\[
 21\le d\le186,\qquad
 \varepsilon:=e^{-2}=0.13533528323661269189\ldots .
\tag{76.3}
\]

기존 pointwise 입력은 모든 $a\in\mathcal A$에 대해

\[
 |E_q(a;Y)|\le \varepsilon\frac{Y}{\varphi(q)}
\tag{76.4}
\]

를 요구한다. 반면 Maier의 최종 column 합에 직접 필요한 aggregate 충분조건은

\[
 \left|\sum_{a\in\mathcal A}E_q(a;Y)\right|
 \le \varepsilon M\frac{Y}{\varphi(q)}.
\tag{76.5}
\]

식 (76.5)는 식 (76.4)에서 triangle inequality로 따라오지만, 역은 성립하지 않는다.
그러므로 aggregate 정리는 pointwise Lemma 2의 문장 자체를 증명하지 않더라도 Maier의
**총 prime mass 단계**를 교체할 수 있다. 다만 이후 prime-pair upper sieve와 row deletion은
별도 의무이며 이번 결과가 그것들을 자동으로 닫지 않는다.

## 3. Maier 원문의 정확한 quantifier

Maier 1981 printed p.260 Lemma 2는 good modulus $q$에 대해 어떤 $D$를 택하면
$x>q^D$에서 $(a,q)=1$인 모든 $a$에 균일한 prime number theorem을 준다. printed
pp.266--268의 matrix conclusion에서는 다음 순서다.

\[
 \text{각 admissible column에 Lemma 2 적용}
 \Longrightarrow
 \#\mathcal P>C_3E q^{D-1}.
\tag{76.6}
\]

그 뒤 proof는 식 (76.6)의 **전체 prime count**와 prime-pair upper bound를 비교해 한 row를
선택한다. 따라서 판정은 다음처럼 좁혀야 한다.

- 임의의 Bombieri--Vinogradov 평균을 그대로 넣는 것은 불가능하다.
- 평균으로 고른 modulus가 Maier의 good primorial과 일치한다는 보장도 자동으로 없다.
- 그러나 고정된 그 primorial과 그 admissible residue subset에 대해 식 (76.5)를 직접 주는
  정리는 column 합 단계의 충분한 대체 입력이다.

Gallagher printed p.337 Theorem 7, 식 (29)는 primitive character L1 합을 제어한다.
p.338 식 (30)은 explicit formula의 character error에 절댓값을 취한 뒤 positive zero-count
integral로 넘긴다. Theory 75의 cancellation blocker가 생기는 정확한 위치가 여기다.

## 4. Akbary--Hambrook explicit L1 상계

Akbary--Hambrook Theorem 1.2는 $x\ge4$에서

\[
 \sum_{r\le Q}\frac r{\varphi(r)}
 \sum_{\chi\bmod^{*}r}\max_{y\le x}|\psi(y,\chi)|
 <c_0\left(4x+2x^{1/2}Q^2+6x^{2/3}Q^{3/2}+5x^{5/6}Q\right)
 (\log x)^{7/2},
\quad c_0=48.83236\ldots .
\tag{76.7}
\]

모든 항이 비음수이므로 이 **상계식 자체를** $x$로 나눈 direct relative certificate는

\[
 \frac{\mathrm{RHS}_{\rm AH}}x
 \ge 4c_0(\log x)^{7/2}
 \ge 612.7196429634\ldots
 >4527.4198\,e^{-2}qquad(x\ge4).
\tag{76.8}
\]

식 (76.8)은 실제 error가 612보다 크다는 하한이 아니다. 정리의 오른쪽을 추가 cancellation
없이 현재 PAP error budget으로 쓰면 certificate가 너무 크다는 뜻이다. Theorem 1.3의
least-prime-factor 제한은 작은 소인수로 구성된 primorial을 포함시키려면 $Q_1=1$로 두어야 하므로
이 floor를 제거하지 않는다.

## 5. Sedunova explicit L1 상계

Sedunova Theorem 1.2는 $x\ge4$, $1\le Q_1\le Q\le x^{1/2}$에서

\[
 \sum_{\substack{r\le Q\\\ell(r)>Q_1}}
 \max_{2\le y\le x}\max_{(a,r)=1}
 \left|\psi(y;r,a)-\frac{\psi(y)}{\varphi(r)}\right|
 <c_1F(x,Q,Q_1)(\log x)^{7/2},
\quad c_1=42.2,
\tag{76.9}
\]

\[
 F(x,Q,Q_1)=\frac{14x}{Q_1}+4x^{1/2}Q
 +15x^{2/3}Q^{1/2}+4x^{5/6}\log\frac Q{Q_1}.
\tag{76.10}
\]

primorial을 배제하지 않으려면 $Q_1=1$이 필요하다. 이때 direct certificate는

\[
 \frac{\mathrm{RHS}_{\rm Sed}}x
 \ge14c_1(\log x)^{7/2}
 \ge1853.2524593466\ldots
 >13693.7863\,e^{-2}qquad(x\ge4).
\tag{76.11}
\]

Proposition 1.6이 Vaughan mean-value 단계의 log exponent를 $5/2$로 낮추지만, 양의
$x(\log x)^{5/2}$ main floor를 현재 aggregate PAP budget 아래로 보내는 decay를 주지는 않는다.
따라서 이 역시 direct drop-in이 아니다.

## 6. Bennett et al. pointwise 정리의 유한 no-overlap

Bennett--Martin--O'Bryant--Rechnitzer Theorem 1.1은 모든 $(a,q)=1$에 대해

\[
 \left|\psi(Y;q,a)-\frac{Y}{\varphi(q)}\right|
 <c_\psi(q)\frac{Y}{\log Y}qquad(Y\ge x_\psi(q))
\tag{76.12}
\]

를 주고, $q>10^5$에서는

\[
 c_\psi(q)\le\frac1{160},qquad
 x_\psi(q)\le
 \exp\!\left(0.03\sqrt q\,(\log q)^3\right).
\tag{76.13}
\]

$Y=q^d$를 넣으면 이 source cutoff를 보장하기 위한 조건은

\[
 d\log q\ge0.03\sqrt q(\log q)^3
 \quad\Longleftrightarrow\quad
 d\ge0.03\sqrt q(\log q)^2.
\tag{76.14}
\]

$q>10^5$이면 이미 더 약한 $\sqrt q\ge300$, $\log q\ge10$으로도

\[
 0.03\sqrt q(\log q)^2\ge900>186\ge d.
\tag{76.15}
\]

따라서 large-$q$ branch는 현재 $d\le186$과 **어느 한 점에서도 겹치지 않는다**. 더 정확한
경계 진단은 $q\downarrow10^5$에서 필요한 $d$가 $1257.4555\ldots$이고, 첫 primorial
$q=510510$에서는

\[
 d_{\rm required}=3702.7410004983\ldots .
\tag{76.16}
\]

source cutoff를 무시해도 error normalization이 별도로 맞아야 한다. 식 (76.12)를
$Y/\varphi(q)$와 비교하면 published envelope가 보증하는 relative error는

\[
 \frac{c_\psi(q)Y/\log Y}{Y/\varphi(q)}
 \le\frac{\varphi(q)}{160d\log q}.
\tag{76.17}
\]

$q=510510$, $\varphi(q)=92160$, $d=186$에서는

\[
 \frac{\varphi(q)}{160d\log q}
 =0.23561859525868\ldots
 =1.7409990183\ldots e^{-2}.
\tag{76.18}
\]

이 지점에서 필요한 $c_\psi$는 $0.00358989289\ldots$ 이하인데 published uniform envelope는
$1/160=0.00625$다. 개별 $q\le10^5$ 계산표는 유용하지만 primorial이 무한히 커지는 Maier
proof를 덮지 않으므로 numerical $X_{\rm cert}$의 tail input이 아니다.

## 7. Aggregate second-moment 충분조건

character explicit-formula contribution을 $Z_\chi(Y)$라 하고

\[
 E_q(a;Y)=\frac1{\varphi(q)}
 \sum_{\chi\bmod q}\overline{\chi(a)}Z_\chi(Y)
\tag{76.19}
\]

로 쓴다. $C_\chi(\mathcal A):=\sum_{a\in\mathcal A}\overline{\chi(a)}$라 하면

\[
 \sum_{a\in\mathcal A}E_q(a;Y)
 =\frac1{\varphi(q)}\sum_{\chi\bmod q}
 C_\chi(\mathcal A)Z_\chi(Y).
\tag{76.20}
\]

$\mathcal A$가 서로 다른 reduced residues로 이루어졌을 때 character orthogonality는

\[
 \sum_{\chi\bmod q}|C_\chi(\mathcal A)|^2=\varphi(q)M
\tag{76.21}
\]

을 준다. Cauchy--Schwarz로

\[
 \left|\sum_{a\in\mathcal A}E_q(a;Y)\right|^2
 \le\frac{M}{\varphi(q)}
 \sum_{\chi\bmod q}|Z_\chi(Y)|^2.
\tag{76.22}
\]

따라서 식 (76.5)의 충분조건은 정확히

\[
 \boxed{
 \sum_{\chi\bmod q}|Z_\chi(Y)|^2
 \le\varepsilon^2M\frac{Y^2}{\varphi(q)}.}
\tag{76.23}
\]

pointwise Cauchy budget은 우변에 $M$이 없었다. aggregate를 먼저 만들면 허용 second-moment
budget이 정확히 $M$배 커진다. 이 algebraic terminal implication은 source theorem을 가정으로
받는 형태로 Lean에서 검증한다. 식 (76.19), (76.21)의 character theory와 이를 실제
explicit formula에 적용하는 analytic theorem은 local axiom으로 넣지 않는다.

## 8. 자연 크기 variance라면 왜 scale상 가능할 수 있나

만약 어떤 fully numerical unconditional theorem이 고정 primorial에 대해

\[
 \sum_{\chi\bmod q}|Z_\chi(Y)|^2
 \le C\varphi(q)Y\log q
\tag{76.24}
\]

를 준다면 식 (76.23)의 충분조건은

\[
 C\varphi(q)^2\log q\le\varepsilon^2MY.
\tag{76.25}
\]

이다. $Y=q^d$이고 $d>2$이면 단순 크기 비교로는 가능성이 있다. 이것은 **가정 아래의 scale
check**일 뿐 식 (76.24)를 증명하거나 적합한 source를 발견했다는 뜻이 아니다. 특히 다음을
모두 포함해야 실제 R09 입력이 된다.

- 한 fixed primorial 또는 Maier가 선택하는 primorial sequence에 대한 uniformity,
- 그 admissible subset $\mathcal A$와 principal/exceptional branch,
- short/endpoint interval과 prime-power correction,
- $\psi$에서 $\pi$로의 one-sided transfer,
- numerical $C$와 모든 공통 finite cutoff.

## 9. variance·few-exception 후보가 아직 drop-in이 아닌 이유

Friedlander--Goldston 1996은 residue-class variance 자체를 연구하는 직접 관련 문헌이다.
그러나 fixed-$q$ natural-order 결과는 필요한 power-scale·모든 cutoff·multiplier를 한꺼번에
주는 fully numerical Maier contract로 이번 감사에서 복원되지 않았다. 강한 개별-modulus 범위는
조건부이거나 $q$가 $Y$에 훨씬 가까운 다른 regime을 다룬다. 원문 full PDF의 안정적인 공개
mirror를 확보하지 못했으므로 exact formula를 이 프로젝트 원장에 승격하지 않았다.

Baker 2020은 $q\le x^{9/40}$인 **pairwise coprime** moduli family에서 polylog 개의 예외를
제외하는 구조를 준다. Maier primorial들은 서로 중첩되어 pairwise coprime이 아니고, 정리의
$O$-상수도 numerical certificate로 인쇄되지 않았다. good-modulus selection의 아이디어에는
가깝지만 현재 식 (76.23)의 source는 아니다.

고전 Barban--Davenport--Halberstam 평균도 modulus 평균 또는 residue 평균을 제공한다.
그 평균에서 “좋은 하나”를 고르는 것과 Maier Lemma 1이 주는 good primorial을 같은 modulus로
만드는 추가 논리가 없다. 이 quantifier mismatch를 닫지 않고 평균 정리를 drop-in으로 부르면
안 된다.

## 10. 수치 검증과 Lean 경계

고정 Python 모듈
`source/dep_r09_preabsolute_moment_screen.py`는 다음만 120-dps로 재계산한다.

- 식 (76.8), (76.11)의 direct-certificate floor,
- 식 (76.14)--(76.18)의 cutoff와 error normalization,
- aggregate budget이 pointwise budget의 정확히 $M$배라는 관계,
- hypothetical natural-order variance의 scale diagnostic.

단위시험은 local source hash와 machine ledger의 숫자까지 다시 대조한다. 이 계산은 인용한
analytic theorem 자체를 증명하지 않는다.

Lean은 단일 `TheoryVerification.lean`에서 다음 terminal algebra만 검사한다.

1. 식 (76.15): normalized cutoff premise와 elementary lower inputs가 있으면 $d\le186$과
   모순이라는 것.
2. 식 (76.22)--(76.23): Cauchy premise와 second-moment budget을 받으면 aggregate error
   target이 따라온다는 것.

둘 다 upstream source theorem을 premise로 받으므로 analytic completion은
`CONDITIONAL_KERNEL_PASS`다. `sorry`, `admit`, project-local `axiom`은 사용하지 않는다.

## 11. 판정표

| 항목 | 상태 |
|---|---|
| Maier printed quantifier와 downstream aggregate 소비 재구성 | `DONE` |
| Akbary--Hambrook·Sedunova direct L1 certificate | `FAILS CURRENT BUDGET` |
| Bennett large-$q$ source cutoff와 $d\le186$ overlap | `NO OVERLAP` |
| Bennett published uniform error envelope | 첫 primorial checkpoint에서도 `FAILS BUDGET` |
| aggregate second-moment 충분조건 | `DERIVED / CONDITIONAL TERMINAL LEAN` |
| 필요한 individual-primorial source theorem | `NOT IDENTIFIED` |
| 모든 pre-absolute-value 방법의 불가능성 | `NOT CLAIMED` |
| `PAP-11`, `DEP-R09` | `OPEN` |
| fixed $2\times10^{-17}$, numerical $X_{\rm cert}$ | `OPEN` |
| threshold calculator·actual prime 계산 | `NOT READY / NOT RUN` |

## 12. 다음 증명 gate

다음 작업은 식 (76.23)을 실제로 공급할 수 있는지 묻는 좁은 source/theorem 감사다.

1. restricted-residue variance 또는 individual-primorial variance 정리를 우선 선별한다.
2. 없다면 식 (76.23)을 정확한 신규 analytic theorem target으로 정식화하고, Maier의
   admissible set 구조가 일반 $M$보다 더 작은 character energy를 주는지 조사한다.
3. 이 gate가 통과한 뒤에만 principal/exceptional character, endpoint, prime powers,
   $\psi\to\pi$를 합성한다.

여기서 numerical theorem을 얻으면 처음으로 $d\le186$ 안에서 $X_{\rm cert}$ 후보 cutoff를
좁힐 수 있다. 현재는 그 입력이 없으므로 장시간 CPU 실험을 요청하지 않는다.

## 13. 참고문헌

- H. Maier, *Chains of Large Gaps between Consecutive Primes*, Advances in Mathematics 39
  (1981), 257--269, DOI
  [10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- P. X. Gallagher, *A Large Sieve Density Estimate near $\sigma=1$*, Inventiones
  Mathematicae 11 (1970), 329--339, DOI
  [10.1007/BF01403187](https://doi.org/10.1007/BF01403187).
- A. Akbary and K. Hambrook, *A Variant of the Bombieri--Vinogradov Theorem with Explicit
  Constants and Applications*, Math. Comp. 84 (2015), 1901--1932,
  [arXiv:1309.2730](https://arxiv.org/abs/1309.2730), DOI
  [10.1090/S0025-5718-2014-02887-4](https://doi.org/10.1090/S0025-5718-2014-02887-4).
- A. Sedunova, *A Partial Bombieri--Vinogradov Theorem with Explicit Constants*,
  Publications mathématiques de Besançon (2018), 101--110, DOI
  [10.5802/pmb.24](https://doi.org/10.5802/pmb.24).
- M. A. Bennett, G. Martin, K. O'Bryant and A. Rechnitzer,
  *Explicit Bounds for Primes in Arithmetic Progressions*, Illinois J. Math. 62 (2018),
  427--532, [arXiv:1802.00085](https://arxiv.org/abs/1802.00085), DOI
  [10.1215/00192082-7600068](https://doi.org/10.1215/00192082-7600068).
- J. B. Friedlander and D. A. Goldston, *Variance of Distribution of Primes in Residue
  Classes*, Quart. J. Math. 47 (1996), 313--336, DOI
  [10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
- R. C. Baker, *A Theorem of Bombieri--Vinogradov Type with Few Exceptional Moduli*,
  Acta Arith. 195 (2020), 217--233, [arXiv:1905.12488](https://arxiv.org/abs/1905.12488),
  DOI [10.4064/aa190527-7-1](https://doi.org/10.4064/aa190527-7-1).
