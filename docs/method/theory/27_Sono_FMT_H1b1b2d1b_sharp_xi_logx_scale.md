# Sono/FMT H1b-1b-2d.1b: sharp \(\xi\log x\) finite scale

- 작성일: 2026-09-08
- 상위 obligation: `H1B-L84`, `H1B-COMP-01`, `SIV-07`
- 선행 정본: [corrected \(\kappa=1\) summation](22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md), [actual parameter specialization](23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md), [smooth composition](24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md), [line-905 scalar remainder](26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md)
- 기계 계약: [Sono_FMT_H1b1b2d1b_sharp_scale_v1.json](data/Sono_FMT_H1b1b2d1b_sharp_scale_v1.json)
- 구현: `source/h1b1b2d1b_sharp_scale.py`
- 비판적 검토: [H1b-1b-2d.1b 타당성 검토](../../review/33_20260908_H1b1b2d1b_sharp_scale_타당성검토.md)

## 1. 결론

Maynard Proposition 9.4 증명의 두 sharp cutoff 합, 즉 최종 출판본 (9.58)과
(9.66)에 필요한 finite scale을 다음처럼 명시화했다.

FGKMT/FMT는 실제로

\[
\xi=\frac{\theta}{10}
\]

을 선택하고, Maynard weight의 범위는

\[
R\le x^{\theta/3}
\]

이다. 따라서 숨은 Vinogradov 상수를 전혀 쓰지 않고

\[
\boxed{\xi\log x\ge\frac3{10}\log R}
\tag{27.1}
\]

를 얻는다. Theory 22의 strict cumulative estimate를 두 합에 직접 적용하면,

\[
\boxed{
\delta_{\rm sharp}
\le
\frac{(C_\Sigma+2)[6+\log\Lambda_*]}{\xi\log x}
\le
\frac{10(C_\Sigma+2)[6+\log\Lambda_*]}{3\log R}.
}
\tag{27.2}
\]

아래 §7의 finite gate에서 \(\delta_{\rm sharp}\le1/2\)가 된다. 그 결과

- (9.58)의 \(\widetilde\lambda_1\)은 \(\xi\log x/2\) 이상이라 양수이고,
- (9.66)의 sharp \(r_0\) factor는 주항의 \(3/2\) 이하이다.

따라서 선행 24--26번 package와 결합했을 때 source-traced Lemma 8.4 관련
actual subapplication은 **9/9가 parameterized explicit**이 되고,
`H1B-L84`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 이동할 수 있다.

그러나 이는 Proposition 9.4 전체, Proposition 6.1 전체, `SIV-07` 또는
Sono의 \(X_{\rm cert}\)를 닫지 않는다.

## 2. 쉽게 설명하면

원문에는 “작은 소인수를 거르는 자의 길이가 충분히 길다”는 말이 있지만,
그 “충분히” 앞의 숫자가 최종 출판본에서는 숨겨져 있다. 그 숫자를 1이라고
가정하면 안 된다.

다행히 FGKMT는 그 자의 길이를 자유롭게 두지 않고 \(\xi=\theta/10\)으로
정확히 선택했다. 또 \(R\)과 \(x\) 사이의 범위도 이미 정해져 있다. 이 둘을
합치면 “자의 로그 길이” \(\xi\log x\)가 적어도 \(0.3\log R\)이라는
숫자 부등식이 나온다. 여기에 앞 단계에서 복원한 오차상수를 직접 넣었다.

즉, 숨은 상수를 찾아 맞히는 대신 실제 FGKMT 설정에서 필요한 두 계산을
더 강한 명시적 조건으로 다시 증명했다. 이는 배관의 한 구간을 닫은 것이며,
건물 전체인 Sono 정리의 시작점은 아직 계산할 수 없다.

## 3. 원천과 선행연구 우선 조사

### 3.1 Maynard 최종 출판본

James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
*Compositio Mathematica* 152 (2016), 1517--1554; arXiv:1405.2593.

- Proposition 9.4: 인쇄면 p.1547
- sharp cutoff와 첫 합: (9.49)--(9.58), pp.1547--1548
- 두 번째 sharp factor: (9.65)--(9.70), p.1550
- arXiv에는 v1과 v2가 있고 v2 설명은 “clarified some statements”이다.

### 3.2 FGKMT 최종 출판본

Kevin Ford, Ben Green, Sergei Konyagin, James Maynard, Terence Tao,
[*Long Gaps Between Primes*](https://doi.org/10.1090/jams/876),
*J. Amer. Math. Soc.* 31 (2018), 65--105; arXiv:1412.5029.

- Theorem 6과 \(R\) 범위: 인쇄면 p.98
- (7.8)에 Maynard Proposition 9.4를 적용하는 선택
  \(\xi=\theta/10,D=1\): p.99
- 실제 Theorem 5 설정 \(\alpha=2,\theta=1/3,
  R=(x/4)^{\theta/3}\): p.99

표적 공식 출처 검색에서 Proposition 9.4의 이 표기 차이를 다루는 정식 erratum은
찾지 못했다. 이는 전 세계에 erratum이 없다는 주장이 아니다. 이번 증명은 erratum의
존재 여부에 의존하지 않는다.

## 4. source-version 차이

Maynard arXiv v2 author TeX 1045행과 현재 arXiv HTML은

\[
\frac{k(\log\log x)^2}{\log x}\le\xi\le\frac\theta{10}
\tag{27.3a}
\]

처럼 계수 1을 표시한다. 그러나 최종 출판본은

\[
\frac{k(\log\log x)^2}{\log x}\ll\xi\le\frac\theta{10}
\tag{27.3b}
\]

이다. 이 프로젝트의 정본 우선순위에 따라 최종 출판본 (27.3b)을 채택한다.
따라서 (27.3a)의 계수 1을 numerical certificate에 사용하지 않는다.

proof text에서 이 lower-scale 조건이 실제로 호출되는 곳은 두 군데다.

1. (9.58)의 \(\widetilde\lambda_1\) 평가
2. (9.66)의 \(r_0<x^\xi\) factor 평가

\(\xi\le\theta/10\)이라는 반대 방향 조건은 합동 modulus를
\(x^\theta\) 아래로 두는 별도 역할을 하며 그대로 보존한다.

## 5. strict endpoint 보정

두 합의 범위는 \(d<z\), \(z=x^\xi\)이다. Theory 22의 non-strict
summatory multiplier는

\[
C_\Sigma(a,A_2)=40960D(a,A_2)e^{256+A_2}.
\]

그러나 모든 실수 \(z>1\)에 대한 strict cumulative bound는 끝점과
\(1<z\le2\) 구간을 함께 덮기 위해

\[
\boxed{C_{\rm strict}=C_\Sigma+2}
\tag{27.4}
\]

를 써야 한다. 실제 입력 \(a=1/2,A_2=8\)에서는

\[
C_\Sigma=40960\frac{14801}{69}e^{264}.
\tag{27.5}
\]

기존 `sharp_cutoff_relative_error`는 \(+2\)를 빠뜨리고 있었으므로 코드와
theory 24의 식을 함께 교정했다. smooth Stieltjes 부분적분에서 드는 추가 factor 2는
sharp indicator의 **누적합 자체**에는 필요하지 않는다. 따라서 (27.4)가 맞고
\(2(C_\Sigma+2)\)를 쓰는 것도 아니다.

## 6. 실제 sharp scale

FGKMT의 선택과 Maynard 허용범위에서

\[
\log R\le\frac\theta3\log x,
\qquad
\xi\log x=\frac\theta{10}\log x.
\]

첫 식에 \(3/10\)을 곱하면 (27.1)이 즉시 따른다. 실제 Section 8의
\(R=(x/4)^{\theta/3}\)를 쓰면 약간 더 강한 식도 얻지만, 불필요한 변수변환
위험을 피하기 위해 Theorem 6 전체 범위에서 유효한 (27.1)만 사용한다.

## 7. 공통 finite gate

\(y=\log R\)라 놓고, 선행 application inventory의 공통 제외모듈 상계를

\[
\Lambda_*=A+By,
\tag{27.6}
\]

\[
A=2k^2\log(2k^2)+k(k-1)\log2,
\quad
B=\frac{10\alpha(2k^2-k+1)}\theta+k
\tag{27.7}
\]

로 쓴다. 실제 두 호출에서 \(L+1\le6+\log\Lambda_*\)다.

\[
E=\frac{20}{3}C_{\rm strict}
\tag{27.8}
\]

라 정의한다. 다음 명시식은 두 호출에 공통인 충분조건이다.

\[
\boxed{
y\ge Y_{\rm sharp}:=
\max\left\{
1,\frac{10}{3}\log2,
4E\log(4E),
2E[6+\log(A+B)]
\right\}.
}
\tag{27.9}

### 증명

\(y\ge1\)에서

\[
\log(A+By)\le\log(A+B)+\log y.
\tag{27.10}

현재 \(E>1\)이다. \(y\ge4E\log(4E)\)이면
\(E\log y\le y/2\)이고, 마지막 gate는

\[
E[6+\log(A+B)]\le y/2
\]

를 준다. 따라서

\[
E[6+\log\Lambda_*]\le y.
\tag{27.11}

(27.2), (27.8), (27.11)을 합치면
\(\delta_{\rm sharp}\le1/2\)다. 또한
\(y\ge(10/3)\log2\)와 (27.1)에서
\(\xi\log x\ge\log2\), 즉 \(z=x^\xi\ge2\)이므로
strict summatory theorem의 유효범위도 만족한다. □

## 8. 두 원문 호출에 주는 결과

### 8.1 식 (9.58)

\(\widetilde y_{r_0}=W_0/\varphi(W_0)\)이고
\((r_0,W_0)=1\)인 합에서는 Euler-product main constant와 이 prefactor가
서로 상쇄된다. \(s=\xi\log x\)라 쓰면

\[
|\widetilde\lambda_1-s|\le\delta_{\rm sharp}s.
\]

그러므로 (27.9) 아래에서

\[
\boxed{\widetilde\lambda_1\ge s/2>0.}
\tag{27.12}

이는 Selberg upper-bound 분모가 0이 아님을 finite inequality로 보장한다.

### 8.2 식 (9.66)

선행 theory 23은 \(r_0\) factor의 실제 local denominator family를
\((p-a)^2/(p+a-2)\), root count \(\omega^*(p)\)로 고정했고,
theory 21은 제외모듈 \(W_0\)가 공통 \(\Lambda_*\)에 포함됨을 증명했다.
따라서 같은 strict estimate가 적용되어

\[
\boxed{S_{r_0}\le(1+\delta_{\rm sharp})S_{r_0}^{\rm main}
\le\frac32S_{r_0}^{\rm main}.}
\tag{27.13}

두 번째 \(\mathbf r\)-factor의 smooth composition은 theory 24에서 이미 닫혔다.

## 9. 설명용 수치와 그 한계

FMT의 실제 \(\alpha=2,\theta=1/3\)와 현재 최소 \(k=36\)을 넣으면

~~~text
log R sufficient       ~= 2.9903201460632474e125
log10(log R sufficient) ~= 125.4757176867
delta_sharp at gate     ~= 0.1354085332
~~~

이 값은 일부러 매우 거친 충분조건이고 directed-rounding certificate가 아니다.
또한 \(\log R\)의 크기이지 \(R\), Maynard의 \(x\), FGKMT의 최종 \(X\)가 아니다.
상위 변수변환과 다른 모든 proof gate를 결합하지 않았으므로
이를 Sono 부등식의 시작점으로 지수화하거나 보고하면 안 된다.

기존 smooth gate의 설명용 크기는 이 sharp gate보다도 더 컸다. 따라서 이번 결과의
의미는 실용적 threshold 축소가 아니라 “숫자 없는 sharp-scale blocker 하나를 제거했다”는 데 있다.

## 10. 상태 이동과 남은 blocker

| obligation | 이전 | 현재 | 의미 |
|---|---|---|---|
| two sharp calls | scale hidden | `PROJECT_FINITE_COMPONENT_CLOSED` | 실제 \(\xi\) 선택으로 직접 재증명 |
| actual Lemma 8.4 subapplications | 8/9 explicit | 9/9 parameterized explicit | 선행 scalar/smooth package 포함 |
| `H1B-L84` | `RATE_MISSING` | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | 이 lemma-level actual 호출만 |
| `H1B-COMP-01` | `HARD_BLOCKER` | 변화 없음 | 전체 moment 예산 미완료 |
| `SIV-07`, `SIV-09` | `HARD_BLOCKER` | 변화 없음 | Proposition 6.1 전체 미완료 |
| \(X_{\rm cert}\) | `OPEN` | 변화 없음 | numerical theorem threshold 계산 불가 |

남은 직접 의무는 다음과 같다.

1. Lemmas 8.5--8.6의 size 상수와 finite range
2. Propositions 9.1, 9.2, 9.4, 9.5에서 두 sharp factor 바깥의 오차상수
3. 필요한 main term을 모든 product-profile envelope가 누르도록 하는 공통 moment budget
4. H1c-1의 quantitative character/Bombieri--Vinogradov package
5. 후속 FMT probability와 arbitrary-\(X\) 합성

## 11. 기계검증과 비목표

`tests/test_h1b1b2d1b_sharp_scale.py`는 다음을 검사한다.

1. \(1/10,1/3,3/10,1/2\) 관계를 exact `Fraction`으로 고정
2. \(R=x^{\theta/3}\) 끝점에서 (27.1)이 정확히 equality인지 확인
3. strict multiplier가 non-strict multiplier보다 정확히 2 큰지 확인
4. (27.9)가 (27.11), \(z\ge2\), \(\delta\le1/2\)를 실제로 함의하는지 확인
5. 두 application ID만 닫히고 상위 package는 fail-closed인지 확인
6. 세 원천 파일의 SHA-256과 기계 계약 일치

수치시험은 §5--§8의 증명을 대신하지 않는다. 실제 maximal-gap dataset, prime sweep,
그래프, threshold calculator는 실행하지 않았다. Lean이나 새 Python package도 필요하지 않았다.

## 12. 사용자 수행사항

별도 수행절차 필요없음. 이번 결과는 로컬 문헌·대수 감사와 데이터 비의존 단위시험이다.

