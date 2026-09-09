# Sono/FMT H1c-1b.4b explicit density·elementary constants

- 작성: 2026-09-09 KST
- 증거 수준: `PUBLISHED EXPLICIT INEQUALITY / PROJECT EXACT RATIONAL BRIDGE`
- 판정:
  `HALF-OPEN PRIME DENSITY AND c0,c1 UPPERS CLOSED / C_A AND ABSORPTION OPEN`
- H1c-1b.4b: `CLOSED`
- Hypothesis 1(2), Maynard Proposition 9.2: `OPEN / RATE_MISSING`
- `SIV-08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b4b_density_constants_v1.json`](data/Sono_FMT_H1c1b4b_density_constants_v1.json)
- 검산 구현:
  [`source/h1c1b4b_density_constants.py`](../../../source/h1c1b4b_density_constants.py)
- 비판적 검토:
  [`docs/review/45_20260909_H1c1b4b_density_constants_타당성검토.md`](../../review/45_20260909_H1c1b4b_density_constants_타당성검토.md)

## 1. 결론

H1c-1b.3의 exact denominator

\[
P_T=\#\{p:T\le p<2T\}
\]

에 대해 actual application에서

\[
\boxed{P_T>\frac{T}{2\log T}}
\tag{39.1}
\]

를 명시적으로 증명했다. 중심값 자체는 계속 exact \(P_T\)이며, (39.1)은 오직 상대오차
분모의 lower bound로만 쓴다.

Bordignon Theorem 1.4의 elementary constants에는 안전한 상계

\[
\boxed{c_0<49,\qquad c_1<3}
\tag{39.2}
\]

를 얻었다. 이 세 입력은 H1c-1b.4a의 미해결 \(C_A\)와 독립이다. 따라서 다음 absorption
계산에서 12개 항 중 \(C_A\) 항을 제외한 모든 항을 수치화할 수 있다.

## 2. 쉬운 설명

분포 오차가 “전체 소수 중 몇 퍼센트인가”를 말하려면, 구간에 소수가 적어도 몇 개 있는지
보장해야 한다. 오래된 명시적 정리는 \(T\)와 \(2T\) 사이에 대략
\(0.6T/\log T\)보다 많은 소수가 있다고 보장한다. 우리 구간은 양 끝을 반대로 포함하므로
소수 하나를 안전하게 빼고, 최종적으로 더 단순한 \(0.5T/\log T\)를 사용한다.

또 Bordignon 식에는 \(c_0,c_1\)이라는 두 고정 숫자가 있다. 이를 소수 목록을 대규모로
계산하지 않고 각각 49와 3보다 작다고 증명했다. 아직 가장 어려운 \(C_A\)는 남아 있다.

## 3. exact half-open prime density

### 3.1 원문 lower bound

[Rosser--Schoenfeld 1962](https://doi.org/10.1215/ijm/1255631807) Corollary 3,
식 (3.8), p. 69는 실수 \(T\ge20\frac12\)에 대해

\[
\pi(2T)-\pi(T)>\frac{3T}{5\log T}
\tag{39.3}
\]

를 준다. 여기서 인쇄된 \(20\frac12\)는 \(20.5\)이며 \(\sqrt{20}\)이 아니다.

### 3.2 endpoint convention

(39.3)은 \(T<p\le2T\)를 세지만 Maynard target은 \(T\le p<2T\)다. H1c-1b.3의 exact
endpoint identity에 따라 차이는 소수 atom 하나 이하이므로

\[
P_T\ge\pi(2T)-\pi(T)-1
>\frac{3T}{5\log T}-1.
\tag{39.4}
\]

### 3.3 project lower로 단순화

actual endpoint-safe dimension은 \(r\ge36\)이고

\[
L=\log T\ge36^5=60{,}466{,}176.
\]

모든 \(L\ge20\)에서 지수급수로 \(e^L>L^2/2\ge10L\)이므로

\[
1/T=e^{-L}<1/(10L).
\]

이를 (39.4)에 넣으면 (39.1)이 나온다. 이 proof는 actual \(T\)나 소수 목록을 생성하지 않는다.

[Dusart 2010](https://arxiv.org/abs/1002.0442) Theorem 6.9, 식 (6.6)의
\(\pi(x)\) 상·하계도 독립 교차검증 경로를 제공하지만, direct interval inequality인 (39.3)이
더 단순하므로 정본 proof에는 사용하지 않는다.

## 4. \(c_0<49\) exact rational certificate

Bordignon의 정의는

\[
c_0=\frac{2^{13/2}\{2+\log(\log2/\log(4/3))\}}
{9\pi(\log2)^2}
\left(\frac13+\frac3{2\log2}\right)
\sqrt{\frac{\psi(113)}{113}}.
\]

Rosser--Schoenfeld Theorem 12, 식 (3.35), p. 71에서

\[
\psi(113)/113<1.03883.
\]

다음 rational enclosure를 쓴다.

\[
\begin{gathered}
2^{13/2}<90.51,\quad \log2>0.693,\quad
\frac{\log2}{\log(4/3)}<2.41,\\
\log2.41<0.88,\quad \pi>3.1415,\quad
\sqrt{1.03883}<1.0193.
\end{gathered}
\]

log bound는 \(z=(x-1)/(x+1)\)의 positive atanh series와 exact rational tail,
\(\pi\) bound는 Machin identity의 alternating arctangent series로 검증한다. 그 결과

\[
c_0<\frac{1622314618240}{33191449137}
=48.8774868353\ldots<49.
\tag{39.5}
\]

부동소수점 반올림에 결론을 맡기지 않는다.

## 5. \(c_1<3\) telescope proof

\[
c_1=\prod_p\left(1+\frac1{p(p-1)}\right).
\]

\(\log(1+u)<u\)와 양의 항 확대를 사용하면

\[
\log c_1
<\sum_p\frac1{p(p-1)}
\le\sum_{n=2}^{\infty}\frac1{n(n-1)}=1.
\]

따라서 \(c_1<e<3\)이다. 마지막 부등식은
\(n!\ge2^{n-1}\)를 이용한 지수급수 비교로 충분하다.

## 6. 현재 proof 상태

이번 단계로 다음이 닫혔다.

- exact half-open \(P_T\)의 explicit density lower;
- source endpoint 차이 1;
- \(c_0<49\) exact rational certificate;
- \(c_1<3\) elementary product majorant.

다음은 닫히지 않았다.

- growing-\(A\) numerical \(C_A\);
- 12항과 count-transfer의 한 common cutoff absorption;
- H1(2), P9.2, SIV-08, \(X_{\mathrm{cert}}\).

## 7. 다음 gate

H1c-1b.4c에서는 (39.1)--(39.2)를 넣고 \(C_A\) 항을 분리하여

\[
\text{총 count error}\le\frac{P_T}{(\log T)^{100r^2}}
\]

가 되려면 \(C_A\)가 정확히 얼마 이하여야 하는지 역산한다. 이 단계는 필요 상한을 정할
뿐이며, 그 상한을 Bordignon source terms가 실제 만족한다는 증명은 후속 4d다.

```text
exact half-open P_T density = CLOSED
c0 < 49                    = CLOSED
c1 < 3                     = CLOSED
numerical growing-A C_A    = OPEN
full absorption            = OPEN
H1(2) / P9.2 / SIV-08      = OPEN
X_cert                     = OPEN
```

> 후속 endpoint 교정(2026-09-09): 위 \(P_T=\#\{p:T\le p<2T\}\)는 Maynard
> 원문 half-open bridge에 대한 역사적 표기다. FGKMT actual target은 H1c-1b.3r1에 따라
> \([T,2T]\)이다. closed population은 source \((T,2T]\)를 포함하므로
> \(P_T^{\rm cl}>T/(2\log T)\)는 같은 cutoff에서 그대로 성립한다. 이 density 결과는
> H1c-1b.4e에 합성됐다.
