# Sono/FMT H1b-2a.3: Proposition 9.4 실제 호출의 end-to-end 유한 합성

- 작성일: 2026-09-08
- 증거 수준: `ACTUAL-APPLICATION PARAMETERIZED EXPLICIT PROJECT LEMMA`
- 대상: FGKMT/FMT가 실제로 사용하는 Maynard Proposition 9.4 호출
- 기계 계약:
  [`Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json`](data/Sono_FMT_H1b2a3_Proposition94_end_to_end_v1.json)
- 구현: `source/h1b2a3_proposition94_composition.py`
- 회귀시험: `tests/test_h1b2a3_proposition94_composition.py`
- 비판적 검토:
  [`H1b-2a.3 타당성검토`](../../review/37_20260908_H1b2a3_Proposition94_end_to_end_타당성검토.md)

## 1. 결론

앞 단계에서 따로 닫은 sharp 합, smooth 합, integral 비교, exact Euler 곱, 식 (9.52)의
distribution error를 Maynard의 식 (9.49)--(9.70) 순서대로 다시 연결했다. 그 결과 실제

\[
\mathcal A=\mathbb Z,\quad D=1,\quad
\alpha=2,\quad\theta=\frac13,\quad
\xi=\frac{\theta}{10},\quad
R=(x/4)^{\theta/3}
\tag{31.1}
\]

호출에서는 숨은 상수 없는 유한 상계를 얻는다. Proposition 9.4 우변에서 multiplier를
제외한 표준 크기를 \(T_{94}\)라 하면, 아래 공통 cutoff 이상에서

\[
\boxed{
\sum_{n\in\mathcal A(x)}
\mathbf 1_{\mathcal S(\xi;1)}(L(n))w_n
\le C_{94}(k,x)T_{94},
\qquad C_{94}(k,x)<13.
}
\tag{31.2}
\]

따라서 H1b 원장의 **실제 FGKMT/FMT 호출** `H1B-P94`는
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 승격할 수 있다. 이 계약 내부의 더 좁은
실제-호출 결과 표기는 `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`이다.

그러나 이것은 임의의 집합 \(\mathcal A\)에 대한 Maynard Proposition 9.4 일반형을 새로
증명한 것이 아니다. Proposition 9.1, 9.2, Lemma 9.3, Proposition 9.5 및 공통 moment
오차예산도 남아 있다. 따라서 `H1B-COMP-01`, `SIV-07/09`는 `HARD_BLOCKER`,
\(X_{\rm cert}\)는 `OPEN`으로 유지한다.

## 2. 선행정리 우선 조사와 원천 적합성

### 2.1 채택한 1차 원천

1. James Maynard, *Dense Clusters of Primes in Subsets*,
   DOI `10.1112/S0010437X16007296`, arXiv `1405.2593`.
   Proposition 9.4, 인쇄면 pp.1547--1550, 식 (9.49)--(9.70)을 정본으로 삼았다.
2. Kevin Ford, Ben Green, Sergei Konyagin, James Maynard, Terence Tao,
   *Long Gaps Between Primes*, DOI `10.1090/jams/876`, arXiv `1412.5029`.
   Theorem 6과 식 (7.8)이 (31.1)의 실제 치환을 제공한다.
3. Kevin Ford, James Maynard, Terence Tao,
   *Chains of Large Gaps Between Primes*,
   DOI `10.1112/S0010437X17007391`, arXiv `1511.04468`.
   FGKMT good-weight theorem이 후속 large-gap proof에 들어가는 경로를 대조했다.

관련 후속 upper-moment 논문도 표적 조사했지만, 이 실제
\(\mathcal A=\mathbb Z\) 호출을 같은 정규화와 모든 finite multiplier로 바로 대체할 수 있는
drop-in 정리를 찾지 못했다. 예를 들어 Daniele Mastrostefano의
*An almost-all result for the prime k-tuples conjecture* (arXiv `1804.06290`)는 다른
prime-tuple upper moment이며 “sufficiently large” 범위를 유지하므로 이 의무를 대신하지
않는다. 이는 표적 조사 결과일 뿐 전 세계 novelty 주장이나 선행결과 부재 증명이 아니다.

따라서 새 이론을 임의로 도입하지 않고, 이미 출처별로 감사한 원문 계산을 실제 치환에 맞춰
합성하는 project finite lemma를 사용한다.

### 2.2 source-version 교정

Maynard author TeX의 식 (9.56) 대응 행은 Möbius inversion 조건을 `r_0|d_0`로 적는다.
그러나 바로 뒤의 \(\widetilde\lambda_1\) 전 범위 합과 모순된다. 최종 출판본은 표준
Möbius inversion과 일치하는 `d_0|r_0`로 교정돼 있다. 이 문서는 최종 출판본을 따르며,
두 파일의 SHA-256과 차이를 기계 계약에 남긴다.

## 3. 표준 크기와 앞 단계 입력

\[
\begin{aligned}
T_{94}:={}&\xi^{-1}
\frac{\Delta_L}{\phi(\Delta_L)}
\frac D{\phi(D)}
\left(\frac B{\phi(B)}\right)^k
\mathfrak S_B(\mathcal L)\#\mathcal A(x)\\
&\times(\log R)^{k-1}I_k(F).
\end{aligned}
\tag{31.3}
\]

이번 합성이 사용하는 앞 단계 결과는 다음과 같다.

| 입력 | 정본 | 이번에 쓰는 결과 |
|---|---|---|
| square symmetry와 local denominator | theory 28 | multiplier 1, exact \(g_*\), denominator 유효성 |
| sharp \(r_0\) 합 두 개 | theory 27 | 공통 상대오차 \(\delta_s\le1/2\) |
| canonical smooth 합 | theory 24 | product-profile 절대오차 \(\varepsilon_c\) |
| \(I(F_1)/I(F)\) | theory 28 | \(I_k(F_1)\le2^kI_k(F)\) |
| Euler normalization | theory 29 | \(e^{2+6/k}\mathfrak S_{WB}^{-1}\) |
| 식 (9.52) 오류 | theory 30 | \(\mathcal E_{94}\le\rho_{94}T_{94}\), \(\rho_{94}\le1\) |
| 식 (9.68)--(9.70) | Maynard 원문과 theory 28 | exact 항등식 뒤 남는 두 factor가 각각 1 이하 |

중요하게, theory 29의 \(e^{2+6/k}\)는 식 (9.64)의 pre-\(y\) 곱이
\(y_{\mathbf r,r_0}\)에서 제곱되는 \(e^{4/k}\)까지 이미 포함한다. 이를 별도로 한 번 더
곱하면 중복 계산이다.

## 4. 실제 \(R\) 범위와 공통 cutoff

\(y=\log x\)라 쓰면 (31.1)에서

\[
\log R=\frac{\theta}{3}(y-\log4)=\frac19(y-\log4).
\tag{31.4}
\]

Maynard의 허용범위 \(x^{\theta/10}\le R\le x^{\theta/3}\) 중 위쪽은 즉시 성립한다.
아래쪽은

\[
y\ge\frac{10}{7}\log4
\tag{31.5}
\]

이면 성립한다. 또한 원문의 \(k\le(\log x)^{1/5}\)는

\[
y\ge k^5
\tag{31.6}
\]

로 그대로 쓴다.

### 4.1 P94 전용 강화 smooth gate

Theory 24의 공통 gate는 smooth product의 좌표별 오차합 \(\Delta_c\le1\)만 요구한다.
하지만 실제 coupled integral에 대한 상대오차로 바꾸면 theory 28의 \(2^k\)가 붙는다.
약한 gate만 쓰면 유한하기는 해도 multiplier가 \(k\)에 따라 지수적으로 커진다.

이를 피하기 위해

\[
t_k:=2^{-k-1}
\tag{31.7}
\]

로 두고 theory 24의 closed-form proof에서 \(E\)를 \(E/t_k\)로 바꾼다. 즉

\[
Y_{\rm sm}^{94}:=max\left\{
1,\sqrt{k}\log2,
4(E/t_k)\log(4E/t_k),
2(E/t_k)[6+\log(A+B)]
\right\}.
\tag{31.8}
\]

그러면 같은 초등부등식으로

\[
\Delta_c\le2^{-k-1},\qquad
\varepsilon_c\le2\Delta_c\le2^{-k},\qquad
2^k\varepsilon_c\le1.
\tag{31.9}
\]

을 얻는다. 이는 정밀도를 낮추거나 항을 버린 것이 아니라 cutoff를 더 크게 잡아
\(F_1/F\) 변환 손실을 흡수한 것이다.

### 4.2 최종 actual-call cutoff

H1b-2a.2의 distribution 충분조건을 \(Y_{94}^{\rm dist}\)라 하면

\[
\boxed{
Y_{94}^{\rm comp}:=max\left\{
Y_{94}^{\rm dist},
\frac{10Y_{\rm sm}^{94}}\theta,
k^5,
\frac{10}{7}\log4
\right\}.
}
\tag{31.10}

\]

\(\log x\ge Y_{94}^{\rm comp}\)이면 (31.4)--(31.9), 두 sharp gate 및
\(\rho_{94}\le1\)이 동시에 성립한다. \(10Y_{\rm sm}^{94}/\theta\)는 actual \(R\)의
정확한 변환보다 일부러 보수적인 Maynard lower-range 변환을 사용한 값이다.

## 5. 원문 순서의 end-to-end 합성

### 5.1 식 (9.49)--(9.61): distribution과 square algebra

식 (9.52)의 정수 interval discrepancy 오류는 theory 30에 따라

\[
\mathcal E_{94}\le\rho_{94}T_{94},\qquad0\le\rho_{94}\le1.
\tag{31.11}
\]

주항에서는 \(2|ab|\le a^2+b^2\)와 \((\mathbf r,r_0)\),
\((\mathbf s,s_0)\) 대칭성을 함께 쓰면 식 (9.61)의 추가 multiplier는 정확히 1이다.

### 5.2 식 (9.58): Selberg denominator

\(s=\xi\log x\)라 하자. Sharp certificate는

\[
|\widetilde\lambda_1-s|\le\delta_s s,\qquad\delta_s\le\frac12
\tag{31.12}
\]

를 준다. 따라서

\[
\widetilde\lambda_1^{-2}
\le\frac1{(1-\delta_s)^2s^2}.
\tag{31.13}
\]

특히 denominator가 양수라는 점도 유한하게 확인된다.

### 5.3 식 (9.62)--(9.66): 두 factor

Theory 29의 exact Euler normalization을 포함한 canonical \(\mathbf r\)-factor는

\[
S_{\rm can}\le
e^{2+6/k}\mathfrak S_{WB}(\mathcal L)^{-1}
(\log R)^k I_k(F)(1+2^k\varepsilon_c)
\tag{31.14}
\]

형태로 안전하게 쓸 수 있다. 여기서 \(2^k\varepsilon_c\)는 Lemma 8.4의
product-profile **절대**오차를 coupled main integral에 대한 상대오차로 바꾼 결과다.

Sharp \(r_0\)-factor는

\[
S_0\le(1+\delta_s)S_0^{\rm main},\qquad
S_0^{\rm main}=s\times\text{exact arithmetic factor}
\tag{31.15}
\]

이다. (31.13)--(31.15)를 합치고 (31.3)의 scale로 나누면 \(s=\xi\log x\) 때문에

\[
\boxed{
C_{94}^{\rm main}=
\frac{1+\delta_s}{(1-\delta_s)^2}
e^{2+6/k}(1+2^k\varepsilon_c)
\frac{\log R}{\log x}.
}
\tag{31.16}
\]

마지막 \(\log R/\log x\)는 빼먹기 쉬운 scale 변환이다. 이를 1로 잡아도 안전하지만,
실제 (31.4)를 그대로 보존했다.

### 5.4 식 (9.68)--(9.70): residue factor

원문의 \(N\)개 residue class를 곱한 뒤 산술 factor를 exact하게 정리하면 식 (9.70)의
두 추가 local factor가 남는다. 둘 다 1 이하이므로 전체 multiplier는 1이다. 이 단계에서
\(\mathfrak S_{WB}\)가 취소되고 (31.3)의 \(\mathfrak S_B\),
\(\Delta_L/\phi(\Delta_L)\), \(D/\phi(D)\)가 정확히 남는다.

### 5.5 distribution 오류의 덧셈

식 (9.52)의 오류는 주항에 곱하는 항이 아니라 별도 additive contribution이다. 따라서

\[
\boxed{
C_{94}(k,x)=C_{94}^{\rm main}+\rho_{94}.
}
\tag{31.17}

\]

곱셈으로 합성하면 과도하게 세고, 누락하면 soundness 오류다.

## 6. 균일한 13 상계

공통 gate에서

\[
\frac{1+\delta_s}{(1-\delta_s)^2}\le6,\quad
1+2^k\varepsilon_c\le2,\quad
\frac{\log R}{\log x}\le\frac\theta3=\frac19,\quad
\rho_{94}\le1.
\]

따라서 모든 정수 \(k\ge36\)에 대해

\[
C_{94}(k,x)
\le12e^{2+6/k}\frac\theta3+1
\le\frac43e^{13/6}+1
<13.
\tag{31.18}

\]

이로써 \(k\)에 따라 증가하지 않는 단일 정수 multiplier 13을 얻는다. 여기서 13은 최적값이
아니며, 목적은 Maynard의 Vinogradov 기호를 실제 호출에서 유한하고 안전하게 대체하는 것이다.

### 6.1 마지막 지수 비교의 exact 유리수 certificate

(31.18)의 마지막 `<13`은 `mpmath` 소수값에 의존하지 않는다. 지수급수에서

\[
e<1+1+\frac12+\frac16+\frac1{24}\sum_{j\ge0}4^{-j}
=\frac{49}{18}<\frac{11}{4}
\]

이고, 정수 산술로

\[
\left(\frac{11}{4}\right)^{13}<9^6
\]

이다. 따라서 \(e^{13/6}<9\)이고
\((4/3)e^{13/6}+1<13\)이 엄밀히 따른다. 구현의
`uniform_thirteen_rational_certificate()`는 두 유리수 부등식만 exact `Fraction`으로
검사한다.

## 7. 설명용 수치

`mpmath` 100자리 보조검산에서 \(k=36\)의 기본 cutoff는 다음과 같다.

~~~text
log(x) sufficient              ~= 5.25773781601063699e144
strong smooth log(R) required  ~= 1.75257927200354566e143
actual log(R)                  ~= 5.84193090667848554e143
smooth delta sum               ~= 5.87672029631571025e-13
2^k * epsilon_can              ~= 4.03845143686761845e-2
sharp delta                    ~= 7.88248044287418694e-20
actual composed multiplier     ~= 1.00907337526621674
uniform coarse multiplier      ~= 12.6388511516268432 < 13
~~~

이 숫자는 매우 거친 **Maynard 내부변수 \(x\)의 한 component cutoff**다. 이를 지수화한 값을
Sono 부등식의 \(X_{\rm cert}\), 실제 최대소수간격을 확인할 탐색범위 또는 최소 성립점으로
부르면 안 된다. FMT의 위·아래 변수변환과 다른 모든 proof obligation이 아직 연결되지 않았다.
또한 `mpmath` 출력은 directed-rounding certificate가 아니며, 엄밀한 결론은 (31.5)--(31.18)의
symbolic 부등식이다.

## 8. 상태 전이

| obligation | 이전 | 현재 | 이유 |
|---|---|---|---|
| `H1B-P94` 실제 FGKMT/FMT 호출 | `RATE_MISSING` | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | actual-call multiplier 13과 공통 finite cutoff |
| Maynard P94 일반 \(\mathcal A\) | `RATE_MISSING` | `RATE_MISSING` | 일반 discrepancy 상수는 이번 우회 범위 밖 |
| `H1B-COMP-01` | `HARD_BLOCKER` | `HARD_BLOCKER` | P91/P92/L93/P95와 공통 budget 미완료 |
| `SIV-07/09` | `HARD_BLOCKER` | `HARD_BLOCKER` | Proposition 6.1 전체 미완료 |
| \(X_{\rm cert}\) | `OPEN` | `OPEN` | theorem root dependency 다수 미완료 |

## 9. 금지되는 결론

- 일반 집합 \(\mathcal A\)에 대해 Proposition 9.4 전체가 explicit해졌다고 하지 않는다.
- Proposition 9.4 하나가 닫혔다는 이유로 good sieve weight나 Sono 정리가 닫혔다고 하지 않는다.
- `13`을 Sono의 \(2\times10^{-17}\), empirical \(H(x)\) 또는 최종 large-gap 계수와
  혼동하지 않는다.
- 설명용 \(\log x\)를 최종 \(X_{\rm cert}\)로 보고하지 않는다.
- actual prime/maximal-gap 계산을 수행했다고 기록하지 않는다.

## 10. 검증

`tests/test_h1b2a3_proposition94_composition.py`는 다음을 검사한다.

1. 실제 \(R=(x/4)^{1/9}\) 식과 Maynard 허용범위
2. \(k=36,100\)에서 모든 child gate와 합성 gate
3. 서로 독립 호출한 five child package로 (31.16)--(31.18) 재계산
4. 작은 \(\log x\)에서 fail-closed
5. 잘못된 \(k\), endpoint 입력 거부
6. 1차 원천 SHA-256, dependency 파일, parent non-promotion

연구 Python은 `W:\miniforge3\envs\FGKMT\python.exe`만 사용한다.

## 11. 다음 의무

다음 우선순위는 `H1c-1` quantitative character/prime-distribution package다. 실제 P94의
정수-discrepancy child에서는 Hypothesis 1(1),(3)을 우회했지만, Proposition 9.2의 prime
moment에는 Hypothesis 1(2), exceptional modulus, affine-form prime density의 유한 상수와
cutoff가 여전히 필요하다. 이후 P91/P92/L93/P95를 닫고 한 공통 moment error budget으로
합쳐야 `SIV-07` 상태를 다시 판단할 수 있다.

## 12. 사용자 수행사항

별도 수행절차 필요없음. 실제 소수 실험, P018-B, 장시간 CPU, Lean, 새 Python package,
threshold calculator를 사용하지 않았다.
