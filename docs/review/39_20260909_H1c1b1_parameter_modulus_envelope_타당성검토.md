# H1c-1b.1 growing-dimension·Bordignon envelope 타당성 검토

- 작성: 2026-09-09 KST
- 상세 정본:
  [`33_Sono_FMT_H1c1b1_parameter_modulus_envelope.md`](../method/theory/33_Sono_FMT_H1c1b1_parameter_modulus_envelope.md)
- 기계 계약:
  [`Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json`](../method/theory/data/Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json)
- 최종 판정: `부분 성공 — modulus 폭은 충분 / dyadic dimension 보정의 최종 계수 전달은 OPEN`

## 1. 쉬운 설명

이번에는 Bordignon 정리가 우리 계산에 필요한 “통로 폭”을 제공하는지 확인했다. 처음에는
최종적으로 큰 gap 하나만 찾으므로 parameter를 1로 고정할 가능성도 검토했다. 원문을 따라가면
그 생각은 틀리다. 내부 sieve가 동시에 다루는 후보 수는

$$
r=\left\lfloor(\log x)^{1/5}\right\rfloor
$$

처럼 $x$와 함께 커지고, Maynard가 요구하는 오차도 $100r^2$만큼 강해진다.

Bordignon 정리는 임의의 $A>3$를 허용하므로 각 $x$에서
$A=100r^2+10$을 넣을 수 있다. 필요한 modulus 범위도 충분히 넓다. 이 부분은 긍정적이다.

그런데 원문에는 수치 정리로 바꿀 때 무시하면 안 되는 작은 이음새가 있다. $r$은 $x$에서
고르지만 실제 Maynard 호출은 $x/2$에서 한다. 대부분의 $x$에서는 같은 정수가 나오지만,
$r$이 막 하나 증가한 짧은 구간에서는 $x/2$ 쪽 허용값이 아직 $r-1$이다.

비유하면, 새 신분증의 유효일은 시작됐지만 검사 시스템의 날짜는 반나절 전이라 아주 짧은
구간에 한 칸 차이가 생기는 셈이다. $r-1$을 쓰면 정확히 해결된다. 다만 이 한 칸 감소가
Sono가 계산한 최종 계수에 아무 손실도 주지 않는지까지 다시 대입해야 한다.

따라서 “Bordignon 경로가 불가능하다”는 결과는 아니지만, 이번 단계 전체를 완전 종료했다고
말할 수도 없다.

## 2. 선행연구를 먼저 찾는 전략의 평가

이 전략은 타당했다. [FMT](https://arxiv.org/abs/1511.04468),
[FGKMT](https://arxiv.org/abs/1412.5029),
[Maynard](https://arxiv.org/abs/1405.2593),
[Sono](https://doi.org/10.4418/2025.80.2.2) 원문이 parameter의 뜻과 실제 $x/2$ 호출을
결정한다. [Bordignon 2021](https://nyjm.albany.edu/j/2021/27-54.html)은 모든
$A>3$에 대한 explicit 평균상계를 제공한다.

표적 검색에서는 이 원문들을 growing-$r$, dyadic endpoint와 최종 coefficient까지 정확히
연결한 후속 정리를 찾지 못했다. 그래서 새로 증명한 것은 다음 초등 연결부뿐이다.

- 점별 $A(r)$ 대입의 논리
- actual Proposition 9.2가 identity form 하나만 요구한다는 dependency 가지치기
- $r\ge36$ modulus-capacity 부등식
- dyadic endpoint에서 $r-1$이 항상 안전하다는 one-step lemma

이 검색은 전 세계 문헌의 완전탐색이나 novelty 주장이 아니다.

## 3. 세 parameter를 혼동하면 생기는 오류

| 기호 | 뜻 |
|---|---|
| $k_{\mathrm{chain}}=1$ | 목표로 하는 연속 large-gap 개수 |
| $r_s$ | Sono/FMT의 원래 $x$ 기준 sieve dimension |
| $k_{\mathrm{Maynard}}$ | Maynard linear-form 수; actual application에서 sieve dimension |

$k_{\mathrm{chain}}=1$을 Maynard 식에 넣어 log-saving exponent를 100으로 만드는 것은
잘못이다. actual exponent는 growing $100r^2$이다.

## 4. Actual call 가지치기의 타당성

FGKMT 식 (6.5)의 actual Proposition 9.2 대상은
$\widetilde L_{q,i,i}(n)=n$이다. 따라서 leading coefficient는 1이며 affine modulus
$|a|q$ 확대가 없다. 식 (6.4)는 prime-distribution clause를 사용하지 않고, 식 (6.6)의
actual Proposition 9.4 distribution child는 별도 project proof로 닫혀 있다.

이는 actual P9.2에 대한 정확한 가지치기다. 일반 Lemma 7.2의 모든 affine form을 닫은 것으로
확대 해석하면 안 된다.

## 5. 새로 발견한 dyadic 경계 문제

원래 선택을 $r_s=\lfloor(\log x)^{1/5}\rfloor$, actual endpoint를 $T=x/2$라 하자.

$$
r_s^5\le\log x<r_s^5+\log2
$$

이면

$$
\log T=\log x-\log2<r_s^5.
$$

따라서 printed Maynard 조건 $k\le(\log T)^{1/5}$에 $k=r_s$는 들어가지 않는다. 이
transition strip은 arbitrarily large $r_s$에서 반복되므로 “충분히 큰 $x$”라는 말만으로
없앨 수 없다.

다만

$$
r_T=\left\lfloor(\log(x/2))^{1/5}\right\rfloor\in\{r_s-1,r_s\}
$$

이고 $r_s-1$은 항상 안전하다. 수학적으로 보정 방법은 단순하다. 열린 문제는 보정된
dimension을 실제 weight와 최종 coefficient에 전부 다시 넣는 일이다.

초기 초안은 $r$을 처음부터 endpoint-safe dimension으로 읽어 이 경계를 놓쳤다. 최종
정본 승격 전 원문 식 (6.5)의 `x replaced by x/2`를 다시 대조해 발견했고, 판정을
fail-closed로 낮췄다.

## 6. Modulus gate는 왜 여전히 통과하는가

Bordignon capacity는

$$
Q_B(T,A)=\frac{T^{1/2}}{(\log T)^A}
$$

이고 actual 요구는 $q\le T^{1/3}$이다. $L=\log T$이면 충분조건은

$$
\frac L6\ge A\log L.
$$

endpoint-safe $r\ge36$, $A=100r^2+10$에서 이 식은 큰 여유로 성립한다. source
$r_s$를 그대로 $A$에 넣고 transition strip의 가장 작은 $T$를 보수적으로 잡아도
$r_s=36$부터 같은 부등식이 성립한다.

즉 “Bordignon의 통로가 좁다”가 문제가 아니다. “Maynard가 허용한 dimension을 어느 endpoint
기준으로 골랐는가”가 문제다.

## 7. $\Delta=10$의 의미

$A=100r^2+10$의 10은 parameter와 modulus 비교용 잠정 여유다.

- 장점: displayed log-power와 modulus capacity를 단순한 식으로 비교할 수 있다.
- 한계: Bordignon의 $C$, $E$, exceptional-zero term, $\psi\to\pi$, endpoint,
  recentering, density를 모두 흡수했다는 뜻이 아니다.

후속 합성에서 부족하면 $\Delta$를 키우거나 별도 slack 함수를 써야 한다.

## 8. Source와 provenance 위험

### Bordignon 상수 표기

Theorem 1.2와 식 (33)은 $C(\alpha_1,\alpha_2,Y_0)$,
$Y_0=\log\log X_0$를 사용하지만 Theorem 1.4와 식 (35)는
$C(A,A-3,X_0)$라고 인쇄한다. type상 $Y_0$가 의도됐을 가능성이 있어도 임의로 고치지
않는다. 전체 상수 합성 전에 원식 재유도 또는 추가 source 확인이 필요하다.

### H1c-1a Maynard PDF pointer

기존 `MAYNARD2016` 행이 다른 Maynard 논문 PDF를 가리킨 provenance 오류가 있었다.
핵심 식은 올바른 author TeX에서 확인돼 수학 판정은 바뀌지 않지만, 이번에 올바른
*Dense Clusters of Primes in Subsets* 출판 PDF와 hash로 교정했다.

## 9. 현재 닫힌 것과 열린 것

```text
parameter 종류와 growing exponent       = 확인
actual P9.2 identity-form                = 확인
Bordignon pointwise A(r) 대입            = 조건부로 가능
endpoint-safe modulus capacity           = 증명
dyadic r -> r-1 admissibility repair     = 증명
repair의 final coefficient 보존          = 미증명
common exceptional B                     = 미증명
full error/count/density/common cutoff   = 미증명
Hypothesis 1(2), P9.2                    = OPEN / RATE_MISSING
Sono numerical X_cert                    = OPEN
```

## 10. 다음 순서

1. `H1c-1b.1a`: $r_T$ 또는 $r_s-1$을 FMT/Sono weight와 최종 coefficient 식에 전부
   대입해 손실을 증명·수치화한다.
2. 통과하면 `H1c-1b.2`: 모든 endpoint에 하나의 exceptional conductor/prime $B$가
   작동하는지 확인한다.
3. 이어 `H1c-1b.3`: $\psi\to\pi$, half-open endpoint와 exact recentering을 닫는다.
4. 마지막 `H1c-1b.4`: $C,E$, represented-prime density와 common cutoff를 합성한다.

현재 병목은 CPU가 아니라 증명 의존성이다. actual prime sweep, threshold calculator,
Lean 또는 새 Python package는 아직 필요하지 않다.

## 11. 2026-09-09 H1c-1b.1a 후속 판정

이 문서에서 열어 둔 coefficient transfer는 후속
[H1c-1b.1a 검토](40_20260909_H1c1b1a_dyadic_coefficient_transfer_타당성검토.md)에서
해결됐다. endpoint-safe \(r_T\)와 실제 \(R=(x/4)^{\theta/3}\)를 함께 넣어도
normalization factor가 \(39/40\)보다 크며, \(\sigma y\) upper multiplier가
\(26/25\) 이하이면 Sono의 원래 hypergraph gate를 통과한다.

따라서 “한 칸 보정 때문에 최종 계수를 낮춰야 한다”는 우려는 asymptotic 정리 수준에서
해소됐다. 후속 H1c-1b.1a.1은 Rosser--Schoenfeld Theorem 7로
\(x\ge2\exp(36^5)\)에서 \(26/25\)보다 강한 explicit Mertens cutoff를 증명했다.
그래도 full distribution package가 열려 있으므로 \(X_{\mathrm{cert}}\)가 계산 가능해진 것은
아니다. 다음 gate는 H1c-1b.2다.
