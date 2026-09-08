# Sono/FMT H1c-1b.1 growing-dimension·Bordignon modulus envelope

- 작성: 2026-09-09 KST
- 증거 수준: `SOURCE-LEVEL PARAMETER AUDIT / PROJECT FINITE LEMMA`
- 판정:
  `GROWING_R_CONFIRMED_POINTWISE_DIAGONAL_AND_MODULUS_CAPACITY_CLOSED_DYADIC_ONE_STEP_REPAIR_COEFFICIENT_TRANSFER_OPEN`
- H1c-1b.1: `PARTIAL — endpoint-safe modulus capacity는 닫힘 / published r의 dyadic coefficient transfer는 열림`
- Hypothesis 1(2), Maynard Proposition 9.2: `OPEN / RATE_MISSING`
- `SIV-07/08`: `HARD_BLOCKER` 유지
- numerical theorem threshold $X_{\mathrm{cert}}$: `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json`](data/Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json)
- 검산 구현:
  [`source/h1c1b1_parameter_modulus_envelope.py`](../../../source/h1c1b1_parameter_modulus_envelope.py)
- 비판적 검토:
  [`docs/review/39_20260909_H1c1b1_parameter_modulus_envelope_타당성검토.md`](../../review/39_20260909_H1c1b1_parameter_modulus_envelope_타당성검토.md)

## 1. 결론

서로 다른 세 매개변수를 분리해야 한다.

| 매개변수 | 뜻 | 실제 선택 |
|---|---|---|
| $k_{\mathrm{chain}}$ | 연속한 큰 gap의 개수 | 이번 목표에서는 1 |
| $r_s$ | Sono/FMT가 원래 척도 $x$에서 고른 sieve dimension | $\lfloor(\log x)^{1/5}\rfloor$ |
| $k_{\mathrm{Maynard}}$ | Maynard linear forms의 개수 | FGKMT Section 8에서 sieve dimension과 같음 |

따라서 Maynard Hypothesis 1(2)의 요구 지수는 100이 아니라

$$
100k_{\mathrm{Maynard}}^2
$$

이며 $x$와 함께 증가한다. 최종 large-gap 문제의 $k_{\mathrm{chain}}=1$을 여기에 넣을 수 없다.

다음 두 사실은 닫혔다.

1. Bordignon Theorem 1.4는 각 실수 $A>3$에 대해 성립하므로, 모든 표시 조건을 같은
   endpoint에서 따로 확인한다는 조건 아래 $A=A(r)$의 점별 대입은 논리적으로 가능하다.
2. $A(r)=100r^2+10$으로 두면 endpoint-safe dimension $r\ge36$에서 실제 Proposition 9.2가
   요구하는 modulus 범위를 Bordignon의 $Q$가 덮는다. 더 보수적인 base-scale affine
   capacity inequality도 성립한다.

그러나 원문을 다시 대조하면서 중요한 경계 문제가 발견됐다. Sono/FMT는
$r_s=\lfloor(\log x)^{1/5}\rfloor$를 고르지만, 실제 Proposition 9.2 호출은 $T=x/2$에서
이루어진다. 일부 반복되는 transition strip에서는 $r_s>(\log T)^{1/5}$이므로 Maynard의
인쇄된 dimension 범위를 그대로 만족하지 않는다. $r_s-1$ 또는
$r_T=\lfloor(\log(x/2))^{1/5}\rfloor$를 쓰면 정확히 고칠 수 있지만, 그 교체가 Sono의
weight normalization과 최종 계수를 보존한다는 수치 전달은 아직 증명하지 않았다.

따라서 이번 결과는 **경로가 가능하고 modulus 폭은 충분하다는 부분 성공**이지,
Hypothesis 1(2), Proposition 9.2 또는 $X_{\mathrm{cert}}$의 완성이 아니다.

## 2. 선행연구 우선 조사

직접 lemma를 만들기 전에 다음 원문을 적용 지점별로 대조했다.

- [FMT, *Chains of Large Gaps Between Primes*](https://arxiv.org/abs/1511.04468),
  Theorem 6과 (6.1), (6.8): 허용되는 최대 $r$을 원래 척도 $x$에서 선택한다.
- [Sono](https://doi.org/10.4418/2025.80.2.2), Proposition 6.2 proof:
  $c_0=1/5$와 $r_s=\lfloor(\log x)^{1/5}\rfloor$를 명시한다.
- [FGKMT, *Long Gaps Between Primes*](https://arxiv.org/abs/1412.5029),
  Theorem 6, Lemma 7.2와 Section 8: 실제 weight에서 $k:=r$이고, 식 (6.5)의
  prime-weighted 호출은 $x$를 $x/2$로 바꾼다.
- [Maynard, *Dense Clusters of Primes in Subsets*](https://arxiv.org/abs/1405.2593),
  Hypothesis 1(2)와 Proposition 9.2: 요구 saving은
  $(\log T)^{-100k^2}$이다.
- [Bordignon 2021](https://nyjm.albany.edu/j/2021/27-54.html), Theorem 1.4:
  임의의 실수 $A>3$와 $Q=T^{1/2}/(\log T)^A$를 허용한다.
- [Akbary--Hambrook](https://arxiv.org/abs/1309.2730), Theorems 1.2--1.3:
  Bordignon proof의 large-modulus explicit mean-value 입력이다.

표적 검색에서는 growing dimension, FGKMT의 실제 $x/2$ 호출, Bordignon의 점별 $A(r)$,
modulus capacity와 최종 coefficient transfer를 한꺼번에 처리한 선행정리를 찾지 못했다.
이는 전 세계 비존재나 novelty 주장이 아니다. 원문이 주는 analytic theorem과 parameter
identity는 채택하고, 원문 사이의 초등 연결부만 project lemma로 정식화한다.

## 3. 실제 Proposition 9.2 호출의 가지치기

FGKMT Section 8의 세 호출을 분리하면 다음과 같다.

1. 식 (6.4): Theorem 6을 $\mathcal L'=\varnothing$로 호출하므로 Hypothesis 1(2)와
   Proposition 9.2를 사용하지 않는다.
2. 식 (6.5): $T=x/2$에서
   $\mathcal L'=\{\widetilde L_{q,i,i}(n)=n\}$로 호출한다. 이것이 실제 Proposition 9.2
   prime-moment 호출이다.
3. 식 (6.6): Proposition 9.4를 사용한다. 프로젝트 H1b-2a.2/2a.3은 actual
   $\mathcal A=\mathbb Z,D=1$ distribution child를 Hypothesis 1(2)의 미지 multiplier 없이
   별도로 닫았다.

따라서 실제 P9.2 form의 leading coefficient는 1이고 analytic modulus도 $q$다. 일반
FGKMT Lemma 7.2의 affine map 전체는 여전히 열려 있지만, actual P9.2를 닫는 데에는 필요 없다.

## 4. Project Lemma L1 — pointwise diagonal 대입

Bordignon Theorem 1.4의 논리형은 다음과 같다.

$$
\forall A>3\ \forall T\,[P(A,T)\Rightarrow B(A,T)].
$$

그러므로 임의의 함수 $A(T)>3$에 대해 각 $T$에서

$$
P(A(T),T)\Rightarrow B(A(T),T)
$$

를 얻는다. 이것은 전칭명제의 점별 대입이므로 $A$가 $T$와 함께 증가한다는 사실 자체는
장애가 아니다.

다만 이 대입은 하나의 공통 cutoff를 자동으로 만들지 않는다. Bordignon의
$C(A,A-3,\cdot)$, $E(T,A)$, exceptional modulus와 downstream count-transfer 오차를
$A(T)$에 대해 실제로 상계해야 한다.

## 5. Project Lemma L2 — dyadic dimension mismatch와 한 단계 보정

원래 척도의 로그를 $L_x=\log x$, 실제 P9.2 endpoint를 $T=x/2$,
$L_T=\log T=L_x-\log2$라 하자. Sono가 고른 값은

$$
r_s=\left\lfloor L_x^{1/5}\right\rfloor.
$$

$r_s$-bin에서는

$$
r_s^5\le L_x<(r_s+1)^5.
$$

그중

$$
r_s^5\le L_x<r_s^5+\log2
$$

인 transition strip에서는 $L_T<r_s^5$이므로

$$
r_s>L_T^{1/5}.
$$

따라서 Theorem 6의 인쇄된 $k\le(\log T)^{1/5}$ 조건에 $k=r_s$를 그대로 넣을 수 없다.
이 strip은 모든 큰 $r_s$에서 다시 나타나므로 하나의 더 큰 $X$를 택하는 것만으로 사라지지 않는다.

반면 $\log2<1$이고 $r_s\ge2$이면

$$
(r_s-1)^5\le r_s^5-1<L_T<(r_s+1)^5.
$$

따라서

$$
r_T:=\left\lfloor L_T^{1/5}\right\rfloor\in\{r_s-1,r_s\},
$$

이고 $r_s-1$은 항상 endpoint-safe하다. 이 한 단계 보정은 exact integer/rational
certificate로 닫혔다.

그러나 “$r_s$ 대신 $r_T$를 쓰면 최종 asymptotic coefficient가 같아 보인다”는 직관만으로
Sono의 explicit coefficient를 보존했다고 말할 수 없다. weight의 $u$, $I_r$, $J_r$,
normalization과 최종 slack에 이 교체를 대입하는 H1c-1b.1a가 필요하다.

## 6. Project Lemma L3 — modulus capacity

잠정 parameter 여유를 $\Delta=10$으로 두고

$$
A(r)=100r^2+10
$$

으로 정한다. 10은 displayed log-power 손실보다 큰 단순 여유일 뿐, 전체 error budget으로
인증된 숫자가 아니다.

### 6.1 Endpoint-safe actual P9.2

실제 identity-form 호출에서 필요한 범위는 $q\le T^{1/3}$이다. Bordignon의 capacity

$$
Q_B(T,A)=\frac{T^{1/2}}{(\log T)^A}
$$

가 이를 덮는 충분조건은, $L=\log T$일 때,

$$
\frac L6\ge A(r)\log L.
$$

$r=\lfloor L^{1/5}\rfloor$이면 $L\ge r^5$이다. 더 강한 affine base-scale 식

$$
\frac L6\ge\left(A(r)+\frac53\right)\log L
$$

을 보면 $L=r^5$에서 충분조건은

$$
\frac{r^3}{30\log r}\ge100+\frac{35}{3r^2}.
$$

$e^4>36$이므로 $\log36<4$이다. $r=36$에서 왼쪽은 $388.8$보다 크고 오른쪽은
$100.01$보다 작다. $r^3/\log r$은 증가하고 오른쪽은 감소한다. 또 고정된 $r$에서

$$
f_r(L)=\frac L6-\left(A(r)+\frac53\right)\log L
$$

은 $L>6(A(r)+5/3)$에서 증가하며 $L=r^5$가 이 조건을 만족한다. 따라서 모든 정수
$r\ge36$과 해당 $r$-bin 전체에서 성립한다.

### 6.2 Published $r_s$를 $T=x/2$에 그대로 둔 capacity

dimension 조건은 transition strip에서 실패하지만 modulus 폭 자체는 실패하지 않는다.
$L_T>(r_s-1)^5$이고 $r_s\ge36$이다. $r_s=36$에서

$$
(r_s-1)^5>120\left(100r_s^2+10+\frac53\right).
$$

왼쪽과 오른쪽의 비는 $r_s$에 따라 증가한다. 또한
$(r_s-1)^5>6(A(r_s)+5/3)$이므로 같은 단조성 논증을 적용할 수 있다. 따라서 source
$r_s$로 더 큰 $A$를 사용해도 Bordignon capacity는 모든 dyadic endpoint에서 충분하다.

즉 이번에 발견한 문제는 **modulus 부족이 아니라 Maynard dimension admissibility**다.

### 6.3 $r_s=36$ transition-left 수치 검산

$L_T=36^5-\log2$, $A=129{,}610$에서 80-dps 보조검산 결과는 다음과 같다.

| 검사 | log margin |
|---|---:|
| actual $Q_B/T^{1/3}$ | $7{,}755{,}396.437894\ldots$ |
| base-scale affine $Q_B/[T^{1/3}L_T^{5/3}]$ | $7{,}755{,}366.575236\ldots$ |
| $Q_B/Q_1$ | $25{,}588{,}488.760264\ldots$ |

모두 크게 양수다. 이 값은 exact 증명의 회귀검사일 뿐 증명 자체를 대신하지 않는다.

## 7. Bordignon source 표기의 열린 문제

출판본 Theorem 1.2는 $Y_0=\log\log X_0$와
$C(\alpha_1,\alpha_2,Y_0)$를 정의하고 식 (33)도 $Y_0$를 쓴다. 그런데 Theorem 1.4와
proof 식 (35)는 $C(A,A-3,X_0)$라고 인쇄한다. type-consistent 해석은
$C(A,A-3,Y_0)$로 보이지만, 이를 조용히 고치지 않는다. H1c-1b.4에서 원식 재유도,
후속 source 또는 저자 clarification이 필요하다.

## 8. 닫힌 항목과 열린 항목

| 항목 | 상태 | 범위·주의 |
|---|---|---|
| 세 parameter의 구분 | `SOURCE_VERIFIED` | $k_{\mathrm{chain}}$와 Maynard $k$를 혼동하지 않음 |
| growing exponent $100r^2$ | `SOURCE_VERIFIED` | fixed exponent 100이 아님 |
| $A(r)$의 점별 대입 | `LOGICALLY_VALID` | 각 predicate를 같은 endpoint에서 확인해야 함 |
| actual P9.2 identity-form 가지치기 | `SOURCE_VERIFIED` | 일반 affine theorem closure가 아님 |
| endpoint-safe $r\ge36$ modulus capacity | `PROJECT_FINITE_LEMMA_CLOSED` | full discrepancy 제외 |
| source $r_s$의 dyadic modulus capacity | `PROJECT_FINITE_LEMMA_CLOSED` | dimension 조건과 별개 |
| printed $r_s$의 모든 $x/2$ 호출 admissibility | `NOT_CLOSED` | recurring transition strip |
| $r_s-1$ 보정의 elementary admissibility | `PROJECT_FINITE_LEMMA_CLOSED` | coefficient transfer 제외 |
| 보정 후 Sono coefficient 보존 | `OPEN` | 다음 H1c-1b.1a |
| 한 common exceptional $B$ | `OPEN` | H1c-1b.2 |
| $\psi\to\pi$, endpoint, recentering | `OPEN` | H1c-1b.3 |
| Bordignon $C,E$, density, common cutoff | `OPEN` | H1c-1b.4 |
| H1(2), P9.2, `SIV-07/08`, $X_{\mathrm{cert}}$ | `OPEN / HARD_BLOCKER` | 승격 없음 |

## 9. Provenance 교정

H1c-1a JSON의 `MAYNARD2016` 행이 제목과 달리 2015 *Small Gaps Between Primes* PDF를
가리키고 있었다. 당시 핵심 식은 올바른 *Dense Clusters* author TeX에서 확인했으므로 기존
수학 판정은 바뀌지 않지만 파일 provenance는 잘못됐다. 이번에 2016 출판 PDF와 SHA-256으로
교정하고 회귀시험을 추가했다.

| 원문 | SHA-256 |
|---|---|
| FMT 2018 arXiv PDF | `4c5709180f4b427eac3525411618534a6d5ab03c1a79d3faeee3318d2ad7ecce` |
| Maynard 2016 출판 PDF | `8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098` |
| Bordignon 2021 NYJM 최종본 | `4bd7adf499ba667647b612a61399f0f86c272bc684718630fcde42983c014029` |
| Akbary--Hambrook arXiv v2 | `797bac5529cfacba249ffe367ca665304fca53f45b0ee17068b9dd13d58da32a` |

관련 FMT pp.11--12, Sono pp.541--542, FGKMT pp.96·99--102, Maynard
pp.1518·1539--1540, Bordignon pp.1417--1418·1433--1435와 Akbary--Hambrook p.3을
추출 텍스트와 렌더 페이지로 대조했다.

## 10. 다음 gate

다음은 `H1c-1b.1a`다. endpoint-safe

$$
r_T=\left\lfloor(\log(x/2))^{1/5}\right\rfloor
$$

또는 보수적인 $r_s-1$을 actual FMT/Sono weight 정의, $u$, $I_r$, $J_r$와 최종 coefficient
slack에 넣어 동일한 explicit lower coefficient를 보존하는지 증명하거나 필요한 손실을
수치화해야 한다. 이 gate가 통과한 뒤에 `H1c-1b.2`의 한 common exceptional $B$로 간다.

actual prime/maximal-gap 실험, threshold calculator, 새 package 또는 Lean은 이번 단계에
필요하지 않았다.

```text
growing dimension identity              = SOURCE_VERIFIED
pointwise Bordignon A(r) substitution   = VALID WITH ALL PREDICATES CHECKED
actual identity-form modulus capacity   = CLOSED FOR ENDPOINT-SAFE r >= 36
dyadic one-step admissibility repair    = AVAILABLE
repair-to-final-coefficient transfer    = OPEN
full Bordignon discrepancy              = OPEN
Hypothesis 1(2) / Proposition 9.2       = OPEN / RATE_MISSING
SIV-07 / SIV-08                         = HARD_BLOCKER
threshold calculator                    = NOT READY
X_cert                                  = OPEN
```

## 11. 2026-09-09 H1c-1b.1a 후속 결과

위의 `repair-to-final-coefficient transfer = OPEN`은 이 문서 작성 시점의
역사적 판정이다. 후속
[H1c-1b.1a 정본](34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md)은
actual endpoint-safe
\(r_T=\lfloor(\log(x/2))^{1/5}\rfloor\), 기존 H1a 적분비와
FGKMT의 정확한 \(R=(x/4)^{\theta/3}\)를 합성했다.

모든 \(r_T\ge36\)에서 dimension·\(R\) factor는 \(39/40\)보다 크다. Sono의
\(16/15\) slack과 결합하면

\[
\sigma y\le(26/25)\,80cx\log_2x
\]

하에서 같은 \(c=\theta c_{I,J}/(12800\log5)\)로
\(C>(5/4)\log5\)를 얻는다. 따라서 dimension repair가 Sono의 asymptotic
\(2\times10^{-17}\) 계수를 낮추지는 않는다.

후속 H1c-1b.1a.1은 Rosser--Schoenfeld Theorem 7로 위 \(\sigma y\) gate를
\(x\ge2\exp(36^5)\)에서 닫았다. full Bordignon error, common exceptional \(B\), count
transfer와 density는 계속 열려 있다. 따라서 Hypothesis 1(2), Proposition 9.2, `SIV-07/08`,
\(X_{\mathrm{cert}}\)는 승격하지 않는다.

## 12. 2026-09-09 H1c-1b.2 후속 결과

H1c-1b.2는 이 문서에서 열어 둔 common exceptional \(B\)를 actual fixed-scale
identity-form에 한해 닫았다. 같은 \(Q_1=(\log T)^A\)를 \(T\), \(2T\)에 쓰고
\(q_0\)의 prime divisor를 \(B\)로 고른다. 최종 Bordignon 12항의 raw
\((T,2T]\) \(\psi\) composition도 닫혔다.

따라서 이 문서의 역사적 `common_exceptional_b_closed=false` 자체는 당시 판정으로
보존하되 successor JSON을 따른다. count transfer와 full absorption은 계속 열려 있고,
다음 gate는 H1c-1b.3이다.

## 13. 2026-09-09 H1c-1b.3 후속 결과

H1c-1b.3은 본 문서의 \(\log T>2A\) capacity 단조성을 사용해 fixed q-family가
Abel 적분의 모든 \(u\in[T,2T]\)에서 허용됨을 닫았다. half-open unweighted count와
exact total-center transfer도 닫혔다. 역사적 certificate는 당시 판정으로 보존하고
successor JSON을 따른다. full density·absorption이 남아 다음 gate는 H1c-1b.4다.
