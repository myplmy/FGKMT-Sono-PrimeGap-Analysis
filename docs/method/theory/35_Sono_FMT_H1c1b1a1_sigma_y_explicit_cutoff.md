# Sono/FMT H1c-1b.1a.1 `sigma*y` explicit cutoff

- 작성: 2026-09-09 KST
- 증거 수준: `PUBLISHED EXPLICIT THEOREM + PROJECT FINITE APPLICATION LEMMA`
- 판정:
  `EXPLICIT_SIGMA_Y_UPPER_CUTOFF_CLOSED_SONO_COEFFICIENT_PRESERVED_DISTRIBUTION_PACKAGE_OPEN`
- H1c-1b.1a.1 / `SIV-03`: `EXPLICIT`
- `SIV-07/08`: `HARD_BLOCKER` 유지
- numerical theorem threshold $X_{\mathrm{cert}}$: `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff_v1.json`](data/Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff_v1.json)
- exact 보조검산:
  [`source/h1c1b1a1_sigma_y_cutoff.py`](../../../source/h1c1b1a1_sigma_y_cutoff.py)
- 비판적 검토:
  [`docs/review/41_20260909_H1c1b1a1_sigma_y_explicit_cutoff_타당성검토.md`](../../review/41_20260909_H1c1b1a1_sigma_y_explicit_cutoff_타당성검토.md)

## 1. 결론

FMT가 사용한 prime-product asymptotic을 새로 증명할 필요는 없다. Rosser--Schoenfeld
Theorem 7의 명시적 Mertens 곱 경계를 정확한 FMT interval과 결합하면 다음을 얻는다.

\[
\boxed{
x\ge X_\sigma:=2\exp(36^5)
\quad\Longrightarrow\quad
\sigma y<\frac{1{,}001{,}000}{998{,}001}\,
80cx\log_2x
<\frac{26}{25}\,80cx\log_2x .
}
\tag{H1c1b1a1.1}
\]

이 명제는 $B_0=1$인 경우와, 하나의 prime $B_0$를 FMT의 product에서 제외하는 경우를
모두 포함한다. 따라서 직전 H1c-1b.1a가 요구한 $26/25$ gate가 같은 cutoff에서 닫히고,
endpoint-safe dimension repair 뒤에도 Sono의 $2\times10^{-17}$ 계수를 이 단계 때문에
줄일 필요가 없다.

그러나 $X_\sigma$는 다음 세 가지가 아니다.

1. 이 하위부등식이 성립하는 **가장 작은** $x$
2. Sono 정리 전체가 성립하기 시작하는 $X_{\mathrm{cert}}$
3. 실제 maximal-gap 데이터에서 관찰한 finite threshold

분포정리의 explicit error, 공통 exceptional modulus, exact recentering, prime density와 여러
상위 error budget이 남아 있으므로 threshold calculator는 아직 만들 수 없다.

## 2. 쉬운 설명

앞 단계에서는 “남은 Mertens 오차가 4% 이내이면 Sono의 최종 계수가 안전하다”는 통과선을
만들었다. 이번 단계는 실제 출판 정리를 이용해 그 오차가 약 0.3006%보다 작다는 보수적
상계를 얻었다.

```text
허용하는 최대 배수       26/25        = 1.04
이번에 증명한 상계       1001000/998001 ~= 1.003005
남은 여유                              ~= 0.036995
```

즉 이 문 하나는 넉넉하게 통과했다. 다만 집 전체의 다른 문, 특히 소수가 등차수열에 얼마나
고르게 분포하는지를 수치로 보장하는 문은 아직 열려 있다.

## 3. 선행연구 우선 조사와 채택 판정

### 3.1 주 근거

[Rosser--Schoenfeld 1962](https://doi.org/10.1215/ijm/1255631807), Theorem 7
(인쇄 p.70, PDF p.7)은

\[
P(t):=\prod_{p\le t}\left(1-\frac1p\right)
\]

에 대해 다음 명시식을 준다.

\[
P(t)<\frac{e^{-\gamma}}{\log t}
\left(1+\frac{1}{2\log^2t}\right)
\qquad(t>1),
\tag{H1c1b1a1.2}
\]

\[
P(t)>\frac{e^{-\gamma}}{\log t}
\left(1-\frac{1}{2\log^2t}\right)
\qquad(t\ge285).
\tag{H1c1b1a1.3}
\]

필요한 방향·끝점·유효범위가 모두 맞으므로 이 출판 정리를 주 근거로 채택한다.

### 3.2 독립 대조와 배제한 식

- [Dusart 2010](https://arxiv.org/abs/1002.0442), Theorem 6.12의
  $0.2/\log^2t$형 상계도 이번 목표에는 충분하다. 다만 preprint이므로 보조 대조로만 둔다.
- [Axler 2018](https://math.colgate.edu/~integers/s52/s52.pdf), p.19도
  Rosser--Schoenfeld Theorem 7을 재인용한다.
- 같은 Axler 출판 PDF의 Proposition 9 위쪽 식 (6.3)은 표시된 그대로라면 필요한 점근
  주항이 없어 $P(t)\sim e^{-\gamma}/\log t$와 양립하지 않는다. 이번 증명에는 이를 전혀
  사용하지 않고 원 Rosser--Schoenfeld 정리로 돌아간다.

이는 표적 문헌조사의 판정이며, 관련 결과의 전 세계 완전탐색이나 새 정리의 novelty 주장이
아니다.

## 4. FMT 정의와 product endpoint

[FMT](https://arxiv.org/abs/1511.04468)의 (3.1), (4.1)--(4.2)는

\[
a=(\log x)^{20},\qquad
z=x^{\log_3x/(4\log_2x)},
\tag{H1c1b1a1.4}
\]

\[
y=cx\frac{\log x\,\log_3x}{\log_2x},
\qquad
\sigma=\prod_{\substack{a<p\le z\\p\ne B_0}}
\left(1-\frac1p\right)
\tag{H1c1b1a1.5}
\]

로 정의한다. 여기서 모든 $\log_j$는 iterated natural logarithm이다.
[FGKMT](https://arxiv.org/abs/1412.5029)의 대응식과 Sono pp.541--542도 같은 정규화를
쓴다.

$P(t)$를 (H1c1b1a1.2)처럼 정의하면 strict lower endpoint와 inclusive upper endpoint는
정확히

\[
\prod_{a<p\le z}\left(1-\frac1p\right)=\frac{P(z)}{P(a)}
\tag{H1c1b1a1.6}
\]

가 된다. $a$가 우연히 prime이어도 $P(a)$에 포함되어 quotient에서는 빠지므로 endpoint
오차가 없다.

## 5. 제외 prime $B_0$의 uniform 보정

$B_0=1$이거나 $B_0\notin(a,z]$이면 (H1c1b1a1.6)이 그대로 $\sigma$다.
$B_0$가 $(a,z]$ 안의 prime이면 해당 factor 하나를 빼므로

\[
\sigma=\frac{P(z)}{P(a)}\left(1-\frac1{B_0}\right)^{-1}.
\]

이 경우 $B_0>a$가 자동으로 성립하고 $t/(t-1)$은 $t>1$에서 감소하므로

\[
\left(1-\frac1{B_0}\right)^{-1}
<\left(1-\frac1a\right)^{-1}.
\]

따라서 두 경우를 한 줄로 합치면

\[
\boxed{
\sigma\le\frac{P(z)}{P(a)}\left(1-\frac1a\right)^{-1}.
}
\tag{H1c1b1a1.7}
\]

이것은 **현재 sigma product 안의 한 prime 제거**만 닫는다. Bordignon 분포정리와 FGKMT
전체에서 하나의 공통 exceptional $B$를 선택할 수 있다는 더 큰 의무는 닫지 않는다.

## 6. Rosser--Schoenfeld 적용

$a\ge285$, $z>1$이면 (H1c1b1a1.2)--(H1c1b1a1.3)과
(H1c1b1a1.7)에서

\[
\sigma<
\frac{\log a}{\log z}
\frac{1+1/(2\log^2z)}{1-1/(2\log^2a)}
\left(1-\frac1a\right)^{-1}.
\tag{H1c1b1a1.8}
\]

한편 (H1c1b1a1.4)에서 정확히

\[
\frac{\log a}{\log z}
=\frac{80(\log_2x)^2}{\log x\,\log_3x}.
\]

이를 $y$와 곱하면

\[
y\frac{\log a}{\log z}=80cx\log_2x.
\tag{H1c1b1a1.9}
\]

즉 남은 일은 (H1c1b1a1.8)의 세 correction factor만 상계하는 것이다.

## 7. 유한 cutoff에서 모든 가정 확인

직전 단계가 이미 요구한 endpoint-safe 조건

\[
r=\left\lfloor(\log(x/2))^{1/5}\right\rfloor\ge36
\]

을 그대로 사용한다. 이는

\[
x\ge X_\sigma:=2\exp(36^5)
\tag{H1c1b1a1.10}
\]

이면 보장된다. $L=\log x$, $\ell=\log L=\log_2x$라 쓰자.

### 7.1 $a$와 Rosser lower endpoint

$L>36^5$이고 $e<3$이므로 $\log36>3$. 따라서

\[
\ell>5\log36>15,\qquad \log a=20\ell>300.
\]

또 $e>2$이므로

\[
a>e^{300}>2^{300}>285,\qquad a>1000.
\tag{H1c1b1a1.11}
\]

### 7.2 $z>a$

양의 exponential series의 한 항만 취하면 $L=e^\ell>\ell^6/720$이다.
$\ell>15>e^2$이므로 $\log\ell>2$. 따라서

\[
\log z=\frac{L\log\ell}{4\ell}
>\frac{\ell^5}{1440}.
\]

$15^4=50{,}625>28{,}800$이므로

\[
\frac{\ell^5}{1440}>20\ell=\log a.
\]

따라서 $z>a$이고, 특히 $\log z>\log a>300$이다.

### 7.3 세 correction factor

(H1c1b1a1.11)과 $\log z>\log a>300$에서

\[
\frac1{2\log^2a}<\frac1{1000},\qquad
\frac1{2\log^2z}<\frac1{1000},\qquad
\left(1-\frac1a\right)^{-1}<\frac{1000}{999}.
\]

그러므로 (H1c1b1a1.8)의 correction multiplier는

\[
<\frac{1001/1000}{999/1000}\frac{1000}{999}
=\frac{1{,}001{,}000}{998{,}001}.
\tag{H1c1b1a1.12}
\]

마지막 비교는 exact integer arithmetic이다.

\[
1{,}001{,}000\cdot25=25{,}025{,}000
<25{,}948{,}026=998{,}001\cdot26.
\]

따라서 (H1c1b1a1.1)이 증명된다.

## 8. cutoff 크기의 해석


\[
\log_{10}X_\sigma
=26{,}260{,}126.879620835647\ldots
\]

이므로 $X_\sigma$ 자체는 약 2,626만 자리 수다. 그러나 이 숫자까지 prime을 생성하거나
검사한 것이 아니다. 로그 영역의 식과 exact rational inequality만 검증했다.

이 거대한 값은 H1a의 $r\ge36$ gate를 그대로 재사용한 보수적 충분조건이다. Mertens
product만 독립적으로 최적화하면 훨씬 작은 cutoff가 나올 수 있지만, 전체 $X_{\mathrm{cert}}$
전에 그 최소화를 하는 것은 현재 critical path가 아니다.

## 9. 상위 coefficient로의 전달

직전 H1c-1b.1a는 dimension과 실제 $R=(x/4)^{\theta/3}$ 손실을 합쳐
$39/40$보다 큰 factor를 얻었다. 이번 결과와 결합하면

\[
\frac{39/40}{1{,}001{,}000/998{,}001}
>\frac{39/40}{26/25}=\frac{15}{16}.
\]

Sono의 원래 $16/15$ slack과 곱하면 hypergraph 통과선보다 엄격히 크다. 따라서
$x\ge X_\sigma$에서 `SIV-03` 때문에 최종 $2\times10^{-17}$ 계수를 낮출 필요는 없다.

## 10. 기계 검증 범위

[`h1c1b1a1_sigma_y_cutoff.py`](../../../source/h1c1b1a1_sigma_y_cutoff.py)는 다음만 한다.

- $e>2$, $e<11/4<3$에 쓰는 rational series envelope
- $15^4>28{,}800$, $2^{300}>1000>285$
- $1/(2\cdot300^2)<1/1000$
- 세 correction factor의 exact 합성과 (26/25) 비교
- $x$를 만들지 않고 $\log x$만 입력한 100-dps endpoint 보조검산
- 닫힌 gate와 열린 gate를 dataclass로 분리

이는 Rosser--Schoenfeld 정리 자체를 컴퓨터로 재증명하는 것이 아니며, prime 계산이나
maximal-gap 실험도 아니다.

## 11. 상태 전이와 남은 blocker

```text
H1c-1b.1a.1 / SIV-03                 EXPLICIT
local sigma-product B0 correction     CLOSED
AN-02 general phi(P)/P application    RATE_MISSING
UB-05 reciprocal-square application   RATE_MISSING
H1c-1b.2 full distribution package    OPEN
SIV-07 / SIV-08                       HARD_BLOCKER
X_cert                                OPEN
threshold calculator                  NOT READY
```

`AN-02`와 `UB-05`도 Mertens 곱을 사용하지만 식의 방향, 거듭제곱, 실제 cutoff 합성이 서로
다르다. 이번 한-sided interval-product 증명만으로 그 행까지 자동 승격하지 않는다.

다음 직접 gate는 `H1c-1b.2`다. Bordignon 후보정리를 actual identity form에 합성하면서
다음 항목을 함께 닫아야 한다.

1. 분포정리 전체에서 하나의 common exceptional $B$
2. full explicit remainder와 growing dimension의 공통 cutoff
3. $\psi\to\pi$ 변환과 half-open interval endpoint
4. exact recentering 및 represented-prime density lower bound
5. Hypothesis 1(2), Proposition 9.2의 완전한 finite inequality

모든 root dependency가 닫히기 전에는 `X_cert` 계산기나 장시간 prime sweep을 만들지 않는다.

## 12. 2026-09-09 H1c-1b.2 후속 결과

위 목록 중 1번과 raw cumulative-\(\psi\) 수준의 2번 일부는 H1c-1b.2에서 닫혔다.
actual fixed scale의 \(T\), \(2T\)에 하나의 \(Q_1,q_0,B\)를 쓰고, 최종 NYJM판
RHS 12항을 모두 등록해 \(R_B(T)+R_B(2T)\) composition을 얻었다.

아직 닫히지 않은 항목은 half-open·prime-power·unweighted count·exact recentering
(H1c-1b.3)과 \(C_*\)·density·12항 common cutoff(H1c-1b.4)다. 따라서
Hypothesis 1(2), Proposition 9.2, `SIV-07/08`과 \(X_{\mathrm{cert}}\)는 승격하지 않는다.
