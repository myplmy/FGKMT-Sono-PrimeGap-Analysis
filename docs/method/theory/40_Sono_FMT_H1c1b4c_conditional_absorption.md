# Sono/FMT H1c-1b.4c conditional full-absorption budget

- 작성: 2026-09-09 KST
- 증거 수준: `PROJECT FINITE CONDITIONAL LEMMA / EXACT RATIONAL CORNER CHECK`
- 판정:
  `NON-C_A ABSORPTION AND CONDITIONAL C_A BUDGET CLOSED / SOURCE C_A OPEN`
- H1c-1b.4c: `CLOSED AS A CONDITIONAL LEMMA`
- Hypothesis 1(2), Maynard Proposition 9.2: `OPEN / SOURCE CONSTANT MISSING`
- `SIV-08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b4c_conditional_absorption_v1.json`](data/Sono_FMT_H1c1b4c_conditional_absorption_v1.json)
- 검산 구현:
  [`source/h1c1b4c_conditional_absorption.py`](../../../source/h1c1b4c_conditional_absorption.py)
- 비판적 검토:
  [`docs/review/46_20260909_H1c1b4c_conditional_absorption_타당성검토.md`](../../review/46_20260909_H1c1b4c_conditional_absorption_타당성검토.md)

## 1. 결론

H1c-1b.2의 Bordignon 12개 항, H1c-1b.3의 Abel·prime-power·endpoint 비용과
H1c-1b.4b의 exact prime-population lower를 한 단위로 합쳤다. 다음을 둔다.

\[
L=\log T,\qquad \ell=\log L,\qquad n=100r^2,\qquad A=n+10,
\qquad r=\lfloor L^{1/5}\rfloor.
\]

actual Maynard 목표는

\[
S_\pi\le \frac{P_T}{L^n}
\]

이고 \(P_T/T>1/(2L)\)이므로 다음이 충분하다.

\[
\boxed{\frac{S_\pi}{T}\le\frac1{2L^{n+1}}.}
\tag{40.1}
\]

모든 비용을 (40.1)로 나누면

\[
\boxed{\mathcal E(r,L;C_A)\le B_0(r,L)+\kappa(r,L)C_A,}
\tag{40.2}
\]

\[
\boxed{\kappa(r,L)=36(1+A\ell)L^{-6}.}
\tag{40.3}
\]

여기서 \(B_0\)는 미해결 Bordignon Theorem 1.2 상수 \(C_A\)를 포함하지 않는 11개
source term과 prime-power·endpoint 비용, 총 13개 양의 항이다. 따라서 정확한 조건부
허용량은

\[
\boxed{C_A<C_{\mathrm{allow}}(r,L)
=\frac{1-B_0(r,L)}{\kappa(r,L)}}
\tag{40.4}
\]

이다. 단, \(B_0<1\)이어야 한다.

다음 보수적 finite theorem을 증명했다.

\[
\boxed{
r\ge500{,}000{,}000,\quad C_A\le e^{500}
\quad\Longrightarrow\quad
\mathcal E(r,L;C_A)<\frac12<1
}
\tag{40.5}
\]

for every \(r^5\le L<(r+1)^5\). 즉 이 조건 아래에서는 H1(2)의 요구 오차보다 실제
상계가 작다. 그러나 \(C_A\le e^{500}\)가 원 논문에서 아직 나오지 않았으므로 (40.5)는
**조건부 bridge**다. H1(2), P9.2, `SIV-08`, \(X_{\mathrm{cert}}\)를 닫지 않는다.

## 2. 쉬운 설명

지금까지 모은 오차를 한 상자에 넣고, 합격선의 크기를 1이라고 다시 잰 셈이다.

- 논문 상수 \(C_A\)와 관계없는 비용은 13개다.
- \(r\ge5억\)에서는 13개가 각각 \(e^{-500}\)보다 작다.
- \(C_A\)가 곱해지는 계수는 \(e^{-536}\)보다 작다.
- 따라서 \(C_A\le e^{500}\)이면 그 항도 \(e^{-36}\)보다 작다.

전체는 합격선의 절반보다도 작다. 문제는 “원 논문의 \(C_A\)가 정말 \(e^{500}\) 이하인가”가
아직 미확인이라는 점이다. 이번 결과는 자물쇠에 맞는 열쇠의 최대 크기를 잰 것이고,
다음 단계는 논문에서 실제 열쇠를 복원해 그 구멍에 들어가는지 보는 일이다.

## 3. 선행 결과와 직접 bridge의 범위

직접 증명 전에 다음 source 경로를 이미 개별 대조했다.

- Bordignon 2021 final Theorem 1.2·1.4: 12개 positive remainder의 원천.
- Maynard 2016 Hypothesis 1(2)·Proposition 9.2: 정확한 목표 \(P_T/L^{100r^2}\).
- Akbary--Hambrook 2015: \(\psi\)에서 unweighted prime count로 가는 partial-summation
  및 prime-power 방법.
- Rosser--Schoenfeld 1962: exact half-open \(P_T\)에 전달한 explicit density.

이 source들은 각 부품을 주지만, growing \(r\), \(A=100r^2+10\), final Bordignon 12항,
exact half-open count 비용을 (40.1)에 동시에 나누어 주는 drop-in lemma는 아니다.
따라서 이번 단계는 새 analytic prime theorem을 주장하지 않고, 이미 감사한 upper들을
합성하는 project-specific elementary bridge만 직접 증명한다.

## 4. 정규화

H1c-1b.3 식 (37.10)의 Abel factor를

\[
K(L)=\frac1L+\frac2{L+\log2}+\frac1{L^2}
\]

라 하자. \(L>1\)에서

\[
K(L)\le\frac4L.
\tag{40.6}
\]

상대 Bordignon term을 \(\rho_j\)라 하면, (40.1)로 나눈 기여는

\[
2L^{n+1}K(L)\rho_j\le8L^n\rho_j.
\tag{40.7}
\]

dyadic \(u\in[T,2T]\)에서 3번 `main Q1 tail`은 증가하므로 \(\log u=L+\log2\)에서,
나머지는 감소하므로 \(\log u=L\)에서 잡는다. 감소성은 §6에서 따로 검증한다.

## 5. 14개 normalized 항

4번 \(C_A\) 항을 제외한 normalized log upper는 다음과 같다. 상수는
\(c_0<49,c_1<3,R_1=5113/2500\)를 넣었다.

| 번호 | 이름 | normalized upper의 자연로그 |
|---:|---|---|
| 1 | leading sqrt | \(\log8+n\ell-L/2\) |
| 2 | main log tail | \(\log2352-(11/2)\ell\) |
| 3 | main \(Q_1\) tail | \(\log2352+(9/2)\log(1+\log2/L)-(11/2)\ell\) |
| 5 | induced character | \(\log(4/\log2)-L/2-9\ell\) |
| 6 | exceptional zero | \(\log36+\log(1+A\ell)-\log(1-\delta)+(n+1)\ell-L/(2AR_1\ell)\) |
| 7 | density exponential | \(\log1224+\log(1+A\ell)+(n+2.52)\ell-0.81\sqrt L\) |
| 8 | density constant | \(\log(36/\log2)+\log(A\ell)+\log(1+A\ell)+(n+1)\ell-L\) |
| 9 | large sqrt | \(\log2352-L/2+(n+A+4.5)\ell\) |
| 10 | eleven twelfths | \(\log10584-L/12+(n/2-0.5)\ell\) |
| 11 | five sixths | \(\log2940-L/6+(n+4.5)\ell\) |
| 12 | five sixths log | \(\log1470-L/6+(n+5.5)\ell\) |
| 13 | prime powers | \(\log(8\sqrt2)+(n+1)\ell-L/6\) |
| 14 | half-open endpoint | \(\log2+(n+1)\ell-2L/3\) |

여기서

\[
\delta=\frac1{2AR_1\ell}.
\]

4번 term은 (40.3) 곱하기 \(C_A\)다. transport margin 10에서 지수 \(-6\)이 나오는
이유는 \(A-n=10\) 중 final source term의 \(+4\)가 네 power를 다시 소비하기 때문이다.

## 6. 전 구간 단조성

### 6.1 고정 \(r\)에서 \(L\)

각 차원 bin에서 \(r\)과 \(A\)를 고정한다. 위 log upper를 \(\ell=\log L\)로 미분한다.

- 1, 5, 8--14번은 음의 \(-cL\) 항이 polynomial log 항을 지배한다.
- 2번의 미분은 \(-11/2\)다.
- 3번의 추가항 \(\log(1+\log2/L)\)도 감소한다.
- \(\log\kappa\)의 미분은
  \(A/(1+A\ell)-6<0\)이다.
- 6번에서 \(q=L/(2AR_1\ell)\)라 두면 필요한 충분조건은
  \(q(1-1/\ell)>n+2\)다.
- 7번의 충분조건은 \(0.405\sqrt L>n+4\)다.

§7의 exact corner checks가 이 조건들을 만족한다. 왼쪽 exponential 양들은 \(L\)과 함께
증가하므로 각 bin의 가장 나쁜 점은 \(L=r^5\)다.

### 6.2 차원 \(r\)

이제 \(L=r^5,\ell=5\log r\)로 둔다. 6번의 핵심 음의 항을

\[
q(r)=\frac{r^5}{2R_1(100r^2+10)(5\log r)}
\]

라 하자. \(r\ge5\times10^8\)에서

\[
\frac{q'(r)}{q(r)}>\frac{2.9}{r}.
\]

반면 양의 부분 미분은

\[
200r\ell+\frac{5(n+1)}r+\frac3r
\]

이하이며 base point에서 exact rational 비교로 \(2.9q/r\)보다 작다. 이후 비율을 지배하는
\(r/\ell^2\)가 증가하므로 6번 전체는 계속 감소한다.

7번도 양의 미분보다 \((0.81)(5/2)r^{3/2}\)가 base point에서 크고,
\(\sqrt r/\ell\)가 증가하므로 계속 감소한다. 나머지 항은 \(-cr^5\), 음의 \(\ell\)
power 또는 같은 더 단순한 비교로 감소한다. 따라서 전 범위의 worst corner는

\[
(r,L)=(500{,}000{,}000,(500{,}000{,}000)^5)
\]

이다.

## 7. exact corner certificate

지수급수의 유리수 부분합과 tail로

\[
\frac{27}{10}<e<\frac{2719}{1000}
\]

를 얻는다. exact integer 거듭제곱 비교는

\[
(2719/1000)^{20}<500{,}000{,}000<(27/10)^{21}
\]

이므로 corner에서

\[
100<\ell<105.
\tag{40.8}
\]

또 \(1+A\ell<r^3\), \(\sqrt r>22000\), \(R_1<2.046\),
\(A<100.001r^2\)를 exact integer/rational arithmetic으로 확인한다. 이 값들을 §5의
각 행에 넣으면 13개 non-\(C_A\) log upper가 모두 \(-500\)보다 작다.

\[
B_0<13e^{-500}<\frac14.
\tag{40.9}
\]

또 \(\log(1+A\ell)<3\log r=(3/5)\ell\)이므로

\[
\log\kappa<4-\frac{27}{5}\ell<-536.
\tag{40.10}
\]

따라서 \(C_A\le e^{500}\)이면

\[
\kappa C_A<e^{-36}<\frac14.
\tag{40.11}
\]

(40.9)--(40.11)이 (40.5)를 준다. 이 증명은 floating-point root 찾기에 의존하지 않는다.

## 8. 100자리 수치 회귀값

exact proof와 별도로 corner formula를 100자리 precision으로 재계산한 값은 다음과 같다.

| 양 | 자연로그 |
|---|---:|
| \(B_0\) upper | \(-542.372094561049347936786890363\ldots\) |
| \(\kappa\) upper | \(-548.047958268349138345604330273\ldots\) |
| \(C_{\mathrm{allow}}\) | \(548.047958268349138345604330273\ldots\) |

마지막 값은 \(\log_{10}C_{\mathrm{allow}}\approx238.0142\)에 해당한다. 이는 회귀진단이며
proof cutoff의 최소성 주장이 아니다. \(5\times10^8\)은 깨끗한 exact inequality를 위한
보수적 선택이다.

## 9. 중요한 성장률 해석

(40.4)의 주된 크기는

\[
C_{\mathrm{allow}}(r,L)\asymp\frac{L^6}{A\ell}
\asymp\frac{r^{28}}{\log r}
\quad(L\asymp r^5,A\asymp r^2)
\]

이다. 즉 원 source에서 복원할 \(C_A\)가 이 polynomial envelope보다 빠르게 증가한다면,
고정 transport margin 10으로는 아무리 \(r\)을 키워도 이 proof path가 닫히지 않을 수 있다.
그 경우 선택지는 다음과 같다.

1. source 재증명에서 더 작은 \(C_A\)를 얻는다.
2. modulus capacity를 다시 확인하며 transport margin을 늘린다.
3. 더 적합한 explicit distribution theorem으로 교체한다.

어느 선택도 4d의 실제 성장률 판정 전에 채택하지 않는다.

## 10. 닫힌 것과 열린 것

| 항목 | 상태 |
|---|---|
| 13개 non-\(C_A\) 비용의 full absorption | `CLOSED FOR r>=500,000,000` |
| exact admissible \(C_A\) formula | `CLOSED` |
| \(C_A\le e^{500}\) 아래 conditional absorption | `CLOSED` |
| Bordignon source가 위 \(C_A\) 조건을 만족 | `OPEN` |
| unconditional full absorption | `OPEN` |
| H1(2), P9.2, `SIV-08` | `OPEN / HARD_BLOCKER` |
| \(X_{\mathrm{cert}}\) | `OPEN` |

## 11. 다음 gate

H1c-1b.4d에서는 Bordignon Theorem 3.4, Lemma 3.1과 zero-density 식 (28)--(32)를
최종 target에서 직접 다시 합성한다. 그 결과의 \(C_A\) 성장률을 (40.4)의
\(r^{28}/\log r\) envelope와 비교한다. 맞지 않으면 숫자를 억지로 키우지 않고 현재
margin-10 경로를 `BLOCKED_BY_CONSTANT_GROWTH`로 판정한다.

새 package, Lean, actual prime sweep 또는 사용자 장시간 계산은 이번 단계에 필요하지 않다.
사용자 수행절차는 **별도 수행절차 필요없음**이다.

> 후속 endpoint·source 판정(2026-09-09): H1c-1b.3r1은 actual target을 FGKMT closed
> \([T,2T]\)로 교정했다. lower atom의 centered 비용은 여기서 사용한 endpoint upper와
> 같은 크기이므로 이 conditional budget을 바꾸지 않는다. H1c-1b.4d는
> \(r\ge10^{10}\)에서 source \(C_A<1\)을 닫았고, 4e가 actual input에 최종 합성했다.
