# Sono/FMT DEP-R09 hybrid·smoothing·cancellation PAP 전달 타당성

- 작성일: 2026-09-14 KST
- 단계: **DEP-R09 / ALTERNATIVE PAP TRANSFER FEASIBILITY**
- 선행 정본: [Theory 72](72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md),
  [Theory 73](73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md),
  [Theory 74](74_Sono_FMT_DEPR09_modern_explicit_density_source_screen.md)
- 기계 원장: [transfer feasibility v1](data/Sono_FMT_DEPR09_transfer_feasibility_v1.json)
- 판정: **pointwise minimum과 source-blind fixed nonnegative smoothing은 현 PAP
  certificate를 통과하지 못하며, cancellation에는 절댓값 이전의 새 수치 정리가 필요**
- 비목적: 모든 smoothing·cancellation 증명의 불가능성, 실제 소수분포 오차의 하한,
  `PAP-11`·`DEP-R09`·fixed $2\times10^{-17}$ 또는 numerical $X_{\rm cert}$ 인증

## 1. 결론

Theory 74가 남긴 세 가능성을 현재 Gallagher--Maier 계약에서 먼저 작은 수치 gate로
검사했다.

1. Ramaré와 tightened Jutila 상계 중 매 지점에서 더 작은 값을 고르는 방법,
2. $[X,2X]$ 안의 고정 비음수 smooth weight로 영점항을 감쇠하는 방법,
3. character·zero의 부호와 위상을 절댓값 이전까지 보존하는 방법이다.

첫 방법의 최선인 pointwise minimum도 coefficient capacity $21\le d\le186$ 전체에서
첫 unit slice만 최소 $8602.0308\ldots$다. 목표 budget은 $e^{-2}=0.1353\ldots$이므로
단순 hybrid는 실패한다. 두 번째 방법은 zero-height 정보를 사용하지 않는
gamma-uniform envelope라면 필요한 $1.5733\times10^{-5}$ 감쇠를 보증할 수 없다.
세 번째 방법은 논리적으로 가능하지만, Gallagher 식 (30)에서 이미 취한 절댓값 뒤에는
필요한 위상 정보가 남지 않는다. 새 pre-absolute-value uniform theorem이 필요하다.

\[
 \boxed{
 \begin{gathered}
 \text{pointwise minimum: FAILS CURRENT CERTIFICATE},\\
 \text{source-blind fixed nonnegative smoothing: FAILS CURRENT CERTIFICATE},\\
 \text{cancellation: NEW ANALYTIC INPUT REQUIRED}.
 \end{gathered}}
\tag{75.1}
\]

> **쉬운 설명:** 두 개의 큰 안전견적 중 매번 더 싼 견적만 골라도 예산보다 약
> 6만 배 이상 크다. 창을 부드럽게 만드는 표준 방법도, 영점의 높이에 관한 새 정보 없이
> 모든 경우를 안전하게 덮으려면 거의 아무것도 줄이지 못한다. 큰 손실을 없애려면
> 서로 상쇄되는 부호를 버리기 전 단계부터 다른 정리가 필요하다.

## 2. 실제 변수와 source 계약

Maier Lemma 2의 actual 선택은 $h=X$, $Q=X^{1/d}$이고 prime interval은 $[X,2X]$다.
Gallagher와 맞춘 높이 및 family scale은

\[
 Q=X^{1/d},\qquad T=Q^5,\qquad
 \mathcal D=Q^2T=Q^7,\qquad L=\log\mathcal D=\frac7d\log X.
\tag{75.2}
\]

$\delta=1-\alpha$, $y=\delta\log X$로 두면 보수적 zero-free edge
$c_1=1/24$의 첫 unit slice는

\[
 \frac{c_1d}{5}\le y\le\frac{c_1d}{5}+1.
\tag{75.3}
\]

source는 다음처럼 확인했다.

| source | 확인 위치 | 이번 역할 |
|---|---|---|
| Gallagher 1970 | printed p.338, 식 (30) | 절댓값 뒤 positive zero-count 적분으로 가는 정보손실 edge |
| Maier 1981 | printed pp.260--261, Lemmas 1--2 | pointwise good-modulus PAP와 $[X,2X]$ interval |
| Ramaré 2016 | Theorem 1.1 | fully numerical averaged density upper |
| Helfgott 2015 | Chapter 9, Lemma 9.1.1 | smooth explicit formula의 Mellin-transform 구조를 확인하는 background |
| Thorner--Zaman 2024 | uniform PNT in AP | pointwise 구조 후보지만 numerical multiplier·공통 cutoff는 OPEN |

세 local PDF는 native text로 먼저 읽고 해당 수식의 렌더 페이지와 대조했다. OCR은
사용하지 않았다. Helfgott의 smooth formula는 구조 확인에만 썼으며 현재 PAP의
unconditional numerical input으로 승격하지 않았다.

## 3. pointwise minimum은 두 상계의 최선의 단순 결합이다

공통 적용범위에서 Ramaré와 Jutila가 각각 $N^*\le U_R$, $N^*\le U_J$를 주면

\[
 N^*\le U_{\rm hyb}:=\min\{U_R,U_J\}.
\tag{75.4}
\]

어떤 convex combination도 $\lambda U_R+(1-\lambda)U_J\ge\min(U_R,U_J)$이므로,
추가 구조 없이 두 상계의 숫자만 섞는 방법 중 pointwise minimum이 가장 강하다.

$y=(1-\alpha)\log X$로 바꾼 뒤 Gallagher 적분의 비음수 integrand를
$B_S(y):=e^{-y}U_S(1-y/\log X)$, $S\in\{R,J\}$라고 쓰자. 양의 공통 kernel을 곱했으므로
$B_{\rm hyb}(y)=\min\{B_R(y),B_J(y)\}$다. 아래의 $R_d,J_d$는 각각
첫 unit slice **전체에서 성립하는 pointwise lower floor**다. 따라서 두 수를 단순히
적분 하한으로만 알고 있을 때에는 성립하지 않을 수 있는
`integral of min >= min of integrals`를 사용하지 않는다.

Theory 74의 Ramaré main term과 Theory 71·73의 tightened Jutila term에서 첫 slice의
transformed integrand에 대한 uniform computed upper-certificate floor는 각각

\[
 \begin{aligned}
 R_d(\log X)&=
 20\left(\frac{7\log X}{d}\right)^3
 \exp\!\left[-\left(1-\frac{20}{d}\right)
 \left(\frac{c_1d}{5}+1\right)\right],\\
 J_d&=6C_{J,\rm tight}
 \exp\!\left[-\left(\frac{c_1d}{5}+1\right)\right],
 \end{aligned}
\tag{75.5}
\]

이고

\[
 C_{J,\rm tight}=\frac{11503697604450072}{425315}.
\tag{75.6}
\]

Ramaré의 additive term은 양수이므로 식 (75.5)에서 버려도 이 **certificate 하한**은
유효하다. 이는 true error의 하한이 아니다.

### 3.1 finite capacity 전체의 endpoint reduction

$21\le d\le186$에서 Ramaré의 세 printed source 조건의 최대는
$\log X_{\min}=d\log10$이다. 이때

\[
 \begin{aligned}
 R_d(d\log10)
 &=20(7\log10)^3
 \exp\!\left[-\left(\frac d{120}+\frac56-\frac{20}{d}\right)\right],\\
 J_d&=6C_{J,\rm tight}\exp\!\left[-\left(\frac d{120}+1\right)\right].
 \end{aligned}
\tag{75.7}
\]

첫 exponent의 양의 부분

\[
 \frac d{120}+\frac56-\frac{20}{d}
 \quad\text{은 미분값}\quad
 \frac1{120}+\frac{20}{d^2}>0
\tag{75.8}
\]

이므로 두 하한은 모두 $d$와 함께 감소한다. 고정 $d$에서는 $R_d(\log X)$가
$\log X$와 함께 증가하고 $J_d$는 이 coarse lower에서 일정하다. 따라서 공통 source
cutoff가 Ramaré 최소점보다 더 커도 pointwise-minimum floor는 감소하지 않는다.

그 결과 finite capacity 전체의 가장 작은 floor는 $d=186$에서

\[
 \boxed{
 \int_{31/20}^{51/20}\min\{B_R(y),B_J(y)\}\,dy
 \ge \min\{R_{186}(186\log10),J_{186}\}
 \ge 8602.0308942005285029\ldots.}
\tag{75.9}
\]

여기서 $c_1d/5=31/20$이며 실제로 작은 쪽은 Ramaré main lower다. Jutila lower는
$12671472308.2271\ldots$다. 필요한 총 감쇠는

\[
 a_{\rm req}:=
 \frac{e^{-2}}{8602.0308942005285\ldots}
 =0.000015732945498702575\ldots.
\tag{75.10}
\]

식 (75.9)는 $B_R,B_J$ 각각의 구간 전체 pointwise floor를 먼저 고정한 뒤 그
minimum을 적분한 것이다. 두 source RHS의 pointwise minimum으로 만드는
**증명용 upper certificate**가
이보다 작을 수 없다는 뜻이다. 실제 소수분포 오차가 8602 이상이라는 뜻이 아니다.

## 4. 고정 비음수 smoothing의 좁은 실패 판정

$[X,2X]$를 보존하는 고정 weight를 $w\ge0$, $\operatorname{supp}w\subset[1,2]$,
$\int w>0$라 하자. smooth explicit formula에서는 zero term에 Mellin transform이
붙는다. zero height $\gamma=0$에서 main mass로 정규화한 실수 factor는

\[
 K_w(\delta,0)=
 \frac{\int_1^2w(u)u^{-\delta}\,du}{\int_1^2w(u)\,du}.
\tag{75.11}
\]

$1\le u\le2$와 $w\ge0$에서 즉시

\[
 2^{-\delta}\le K_w(\delta,0)\le1.
\tag{75.12}
\]

zero-height 분포를 쓰지 않고 모든 $|\gamma|\le T$를 하나의 absolute-value supremum으로
덮는 envelope는 $\gamma=0$ 값도 덮어야 한다. 따라서 $\delta\le1/21$이면

\[
 K_w(\delta,0)\ge2^{-1/21}=0.9675317785\ldots
 >61497\,a_{\rm req}.
\tag{75.13}
\]

Ramaré source 최소점의 실제 첫-slice 상단은
$\delta=0.00595403725\ldots$이고, 이때 lower factor는 $0.9958814803\ldots$다.
단지 support 상계 $U^{-\delta}$로 $a_{\rm req}$를 만들려면

\[
 \log_{10}U\ge100.8669\ldots\quad(\delta=1/21),
 \qquad
 \log_{10}U\ge806.7114\ldots\quad(\text{actual slice}).
\tag{75.14}
\]

이는 원래 $[X,2X]$ pointwise PAP의 support를 보존하지 않는다.

이 판정은 **고정 비음수 weight를 source-blind gamma-uniform 절댓값 envelope로 쓰는 방식**에
한정된다. actual zero height의 정량적 간격이나 oscillatory Mellin cancellation을 주는 새
정리는 배제하지 않는다.

## 5. signed 또는 X-dependent weight가 새 증명을 요구하는 이유

고정된 integrable signed weight에서 $m_w=\int_1^2w\ne0$,
$\kappa_w=\|w\|_1/|m_w|$라 두면 $1-e^{-t}\le t$로

\[
 \left|K_w(\delta,0)-1\right|
 \le\delta\log2\,\kappa_w.
\tag{75.15}
\]

따라서 $|K_w|\le a_{\rm req}$를 원하면

\[
 \kappa_w\ge
 \frac{1-a_{\rm req}}{\delta\log2}.
\tag{75.16}
\]

$\delta=1/21$에서는 $30.2961\ldots$, actual slice에서는 $242.3015\ldots$다.
더 중요한 점은 zero-free edge의 $\delta\asymp1/\log X$가 0으로 갈 때 고정 weight는
$K_w(\delta,0)\to1$이라는 사실이다. 따라서 이 경로는 $X$에 따라 condition number가
커지는 signed minorant, 양의 main mass, pointwise prime-count minorant, Mellin tail과
prime-power/endpoints를 한꺼번에 다시 제어해야 한다. 가능성을 배제하지 않지만 현재
증명의 작은 보정이 아니라 새 proof architecture다.

## 6. cancellation 정보는 어디에서 사라지는가

Gallagher printed p.338 식 (30) 전 단계는 prime-character error의 절댓값을 먼저 합한다.
그 뒤에는

\[
 \log X\int X^{\alpha-1}N^*(\alpha,T,Q)\,d\alpha
\tag{75.17}
\]

같은 positive zero-count만 남는다. $N^*$에는 character phase, residue class $a$의 부호,
서로 다른 zero term의 complex phase가 없다. 따라서 이 단계 이후에는 cancellation을
재구성할 수 없다.

절댓값 이전 zero contribution을 $Z_\chi$라 쓰면 실제 residue-class error는

\[
 E_q(a)=\frac1{\varphi(q)}
 \sum_{\chi\bmod q}\overline{\chi(a)}Z_\chi.
\tag{75.18}
\]

예를 들어 Cauchy--Schwarz 경로로

\[
 \sum_{\chi\bmod q}|Z_\chi|^2
 \le\frac{\varepsilon^2X^2}{\varphi(q)}
 \quad\Longrightarrow\quad
 |E_q(a)|\le\frac{\varepsilon X}{\varphi(q)}
\tag{75.19}
\]

를 모든 필요한 $q,a,X$에 numerical cutoff와 함께 증명할 수 있다면 구조적으로 충분하다.
하지만 현재 zero-count source들은 식 (75.19)의 좌변을 이 크기로 주지 않는다. principal,
exceptional character, prime powers, endpoint와 $\psi\to\pi$도 별도로 합쳐야 한다.
Lean은 식 (75.19)의 terminal 실수대수만 explicit premise 아래 검사하며 complex character
moment theorem 자체를 가정하지 않는다.

평균적 또는 “거의 모든 산술진행” 결과는 특정 good modulus와 모든 필요한 residue class를
쓰는 Maier의 pointwise PAP에 자동으로 대입되지 않는다. downstream proof를 평균형으로
재설계하는 별도 정리가 있어야 한다.

## 7. 정확한 판정과 다음 gate

| 항목 | 상태 | 의미 |
|---|---|---|
| Ramaré--Jutila pointwise minimum | `FAILS CURRENT CERTIFICATE` | finite $d\le186$에서 첫 slice floor가 8602 초과 |
| fixed nonnegative $[1,2]$ source-blind smoothing | `FAILS CURRENT CERTIFICATE` | zero-frequency factor가 필요한 감쇠보다 6만 배 이상 큼 |
| height-sensitive smoothing | `NOT RULED OUT / NEW THEOREM REQUIRED` | zero height 분포와 oscillation의 수치 정리가 필요 |
| fixed signed smoothing | `NECESSARY CONDITION ONLY` | $\delta\to0$에서 condition number 증가 문제 |
| cancellation after $N^*$ | `INFORMATION NOT RECOVERABLE` | 절댓값 단계에서 phase 소실 |
| pre-absolute-value moment/PNT route | `OPEN / PRIORITY` | numerical uniform source가 필요 |
| `PAP-11`, `DEP-R09` | `OPEN` | root 증명 미완료 |
| fixed $2\times10^{-17}$, numerical $X_{\rm cert}$ | `OPEN / NOT READY` | 계산기·장시간 소수 계산 착수 근거 없음 |

다음 source-first 우선순위는 다음과 같다.

1. fully numerical pointwise PNT in progressions를 계속 찾는다.
2. 없으면 Gallagher의 절댓값 이전 character sum에 적용 가능한 explicit second-moment 또는
   large-sieve theorem을 source statement부터 감사한다.
3. 그 둘도 없으면 X-dependent signed minorant를 새 증명 과제로 분리하되, main mass와
   condition number·tail의 coefficient gate를 먼저 통과시킨다.

어느 갈래도 현재 numerical $X_{\rm cert}$ 범위를 만들지 못했다. 따라서 사용자 CPU로
장시간 prime sweep을 실행할 단계가 아니다.

## 8. Lean과 계산 증거 경계

Python은 exact rational source constants와 120-dps 진단을 분리해 식 (75.5)--(75.16)을
재계산한다. Lean 단일 파일은 다음만 proof escape 없이 검사한다.

- $c_1d/5+1=51/20$과 finite $21\le186$ endpoint,
- pointwise `min`의 ordered-field monotonicity,
- coarse rational separation $1/8602<1/7$,
- 식 (75.19)의 second-moment premise 이후 terminal Cauchy 대수.

Ramaré/Jutila density theorem, smooth explicit formula의 complex analysis, 실제 second-moment
theorem은 local axiom으로 넣지 않는다. `sorry`, `admit`, project-local `axiom`은 쓰지 않는다.

## 9. 참고문헌

- P. X. Gallagher, *A Large Sieve Density Estimate near $\sigma=1$*,
  Invent. Math. 11 (1970), 329--339, DOI
  [10.1007/BF01403187](https://doi.org/10.1007/BF01403187).
- H. Maier, *Chains of Large Gaps between Consecutive Primes*,
  Adv. Math. 39 (1981), 257--269, DOI
  [10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- O. Ramaré, *An Explicit Density Estimate for Dirichlet L-series*,
  Math. Comp. 85 (2016), 325--356, DOI
  [10.1090/mcom/2991](https://doi.org/10.1090/mcom/2991).
- H. A. Helfgott, *The Ternary Goldbach Problem*, Annals of Mathematics Studies 203,
  Princeton University Press (2015 manuscript), arXiv
  [1501.05438](https://arxiv.org/abs/1501.05438).
- J. Thorner and A. Zaman, *Refinements to the Prime Number Theorem for Arithmetic Progressions*,
  Math. Z. 306 (2024), Paper 54, arXiv
  [2108.10878](https://arxiv.org/abs/2108.10878), DOI
  [10.1007/s00209-023-03414-3](https://doi.org/10.1007/s00209-023-03414-3).
