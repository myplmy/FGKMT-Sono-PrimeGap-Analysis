# H1b-2a.3 Proposition 9.4 end-to-end 합성 타당성 검토

- 작성일: 2026-09-08
- 검토 대상:
  [`31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md`](../method/theory/31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md)
- 판정: **실제 FGKMT/FMT 호출에 한해 타당 — parameterized explicit로 승격 가능**
- 일반 Maynard Proposition 9.4 판정: **여전히 open**
- `SIV-07/09`, \(X_{\rm cert}\): **변화 없음**

## 1. 쉬운 설명

Proposition 9.4는 특정 선형식에 작은 소인수가 없는 수들이 sieve weight 안에서 너무 많이
나오지 않는다는 “상한 영수증”이다. 지금까지는 영수증의 각 줄을 따로 계산했다.

- 첫 줄: Selberg 분모가 0이 되지 않는가
- 둘째 줄: 여러 약수합을 바꿀 때 생기는 오차가 얼마인가
- 셋째 줄: Euler 곱이 얼마까지 커지는가
- 넷째 줄: 정수 구간을 residue class로 나눌 때 생기는 오차가 얼마인가

이번 작업은 이 줄들을 실제 원문 순서로 더하고 곱해 **한 장의 총액 영수증**으로 만든 것이다.
검토 결과, 실제 FGKMT/FMT 설정에서는 표준 우변의 13배보다 작다는 안전한 상계를 얻었다.

하지만 이 영수증은 공장 전체, 즉 Maynard Proposition 6.1이나 Sono 정리 전체의 비용표가
아니다. 다른 moment와 확률·수변환 단계의 영수증은 아직 남아 있다.

## 2. 가장 중요한 soundness 점검

### 2.1 product-profile 절대오차를 상대오차로 잘못 부르지 않았는가

Theory 24의 \(\varepsilon_c\)는 coupled 함수 \(F\)의 main integral에 대한 상대오차가
아니다. 더 큰 product envelope \(F_1\)로 정규화한 절대오차다. 따라서 그대로
\(1+\varepsilon_c\)라고 쓰면 잘못이다.

이번 합성은 theory 28의

\[
I_k(F_1)\le2^kI_k(F)
\]

를 넣어 정확히 \(1+2^k\varepsilon_c\)로 바꿨다. 이것이 첫 번째 핵심 보정이다.

### 2.2 유한하지만 \(k\)에 따라 폭증하는 상수를 그대로 채택하지 않았는가

기존 공통 smooth gate만 사용하면 \(k=36\)에서도 \(2^k\varepsilon_c\)가 약
\(5.8\times10^9\)가 된다. 이 값도 유한하므로 계산 자체는 가능하지만, Maynard 원문의
\(k\)-uniform Vinogradov 상수를 복원하기에는 부적절하다.

이번 작업은 cutoff를 강화해

\[
\Delta_c\le2^{-k-1},\qquad2^k\varepsilon_c\le1
\]

을 먼저 보장했다. 그 결과 모든 \(k\ge36\)에서 total multiplier를 13 아래로 통일했다.
정확도를 낮춘 것이 아니라 더 큰 시작조건을 지불해 uniformity를 얻은 것이므로 타당하다.

### 2.3 sharp 오차를 분자와 분모에서 올바른 방향으로 썼는가

\[
|\widetilde\lambda_1-s|\le\delta_ss
\]

에서 분모 하한은 \((1-\delta_s)s\), 두 번째 sharp 합의 분자 상한은
\((1+\delta_s)S_0^{\rm main}\)이다. 따라서 계수는

\[
\frac{1+\delta_s}{(1-\delta_s)^2}
\]

이다. 부호나 제곱 방향을 뒤집지 않았고, \(\delta_s\le1/2\)에서 6 이하라는 계산도 맞다.

### 2.4 Euler factor를 중복 계산하지 않았는가

Theory 29의 \(e^{2+6/k}\)에는 다음 두 항이 모두 들어 있다.

1. 식 (9.64)의 pre-\(y\) factor가 제곱될 때의 \(e^{4/k}\)
2. 식 (9.66)의 마지막 두 Euler 곱 \(e^{2+2/k}\mathfrak S_{WB}^{-1}\)

이번 합성은 이를 한 번만 곱했다. pre-\(y\) factor를 별도로 다시 곱하지 않았으므로
double counting이 없다.

### 2.5 distribution error는 더해야 하는가, 곱해야 하는가

식 (9.52)에서 distribution error는 주항과 별도인 additive error다. 따라서

\[
C_{94}=C_{94}^{\rm main}+\rho_{94}
\]

가 맞다. \(C_{94}^{\rm main}(1+\rho_{94})\)로 쓰면 원문 분해와 다른 식이 된다.

### 2.6 \(\log R/\log x\)가 빠지지 않았는가

Sharp main은 \(s=\xi\log x\), canonical main은 \((\log R)^k\), Selberg denominator는
\(s^2\)이다. Proposition 표준 크기의 \(\xi^{-1}(\log R)^{k-1}\)로 나누면
\(\log R/\log x\)가 남는다. 이번 식은 이를 보존하고 실제 상계 \(1/9\)를 사용했다.

### 2.7 residue-class 합산 뒤 숨은 factor가 남지 않는가

Maynard 식 (9.68)--(9.70)은 \(N\)을 exact product로 세고 두 local factor를 1 이하로
버린다. 따라서 추가 multiplier 1이 맞다. 이 단계는 \(\mathfrak S_{WB}\)를 취소해 최종
\(\mathfrak S_B\) scale로 돌아가는 역할도 한다.

## 3. source와 적용범위 감사

### 3.1 source-version 오자

Maynard author TeX의 식 (9.56) 대응 `r_0|d_0`는 다음 식과 맞지 않는다. 최종 출판본의
`d_0|r_0`가 올바른 Möbius inversion 방향이다. 출판본을 우선하고 차이를 기록한 처리는
타당하다.

### 3.2 실제 치환

FGKMT 최종본 식 (7.8)은 Proposition 9.4를 \(\xi=\theta/10,D=1\)로 호출한다. 같은 절에서
\(\mathcal A=\mathbb Z,\alpha=2,\theta=1/3,R=(x/4)^{\theta/3}\)를 고정한다.
이번 package가 일반 파라미터가 아닌 이 조합만 닫은 것은 source 적용과 일치한다.

### 3.3 선행연구 대체 가능성

Maynard, FGKMT, FMT 원문과 관련 upper-moment 후속 연구를 우선 대조했다. 확인한 범위에서는
동일한 rough-number indicator, 동일한 \(T_{94}\) 정규화, 실제 \(\mathcal A=\mathbb Z\)
치환을 모두 finite constant로 제공하는 대체 lemma가 없었다. 따라서 직접 합성이 합리적이다.
단, 이는 문헌 전체를 완전탐색했다는 뜻이 아니다.

## 4. 수치 진단의 의미

\(k=36\)에서 강화된 공통조건은 대략

\[
\log x\ge5.26\times10^{144}
\]

이다. 이 값에서 계산된 실제 합성 multiplier는 약 1.009이고, 독립적인 coarse proof는
12.639보다 작음을 보장한다.

이 결과에서 읽어야 할 것은 다음 두 가지다.

1. **좋은 점:** 숨은 상수 때문에 P94를 무한히 기다릴 필요는 없다. 실제 호출에는 유한한
   cutoff와 multiplier가 존재하고 계산식까지 닫혔다.
2. **나쁜 점:** cutoff가 터무니없이 크다. 현재 목적은 실용적 threshold를 얻은 것이 아니라
   증명 의무 하나를 “숫자 없음”에서 “매우 크지만 계산 가능”으로 바꾼 것이다.

표시된 `12.639`는 설명용 소수지만, `<13` 판정 자체는 수치 반올림에 기대지 않는다.
\(e<49/18<11/4\)와 exact 정수 비교 \((11/4)^{13}<9^6\)로
\(e^{13/6}<9\)를 얻는 별도 유리수 certificate를 사용했다.

이 \(x\)는 FGKMT/Maynard proof 내부변수이며 Sono 정리의 최종 \(X\)가 아니다. 이를
\(X_{\rm cert}\) 또는 “부등식이 처음 성립하는 수”로 해석하면 잘못이다.

## 5. 가능한 일, 사용자 도움이 필요한 일, 현재 불가능한 일

### Codex가 현재 수행 가능한 일

- H1c-1의 character sum·explicit Bombieri--Vinogradov 선행정리 조사
- Proposition 9.1, 9.2, Lemma 9.3, Proposition 9.5의 source-level constant audit
- 닫힌 부품의 symbolic 합성과 FGKMT Python 고정밀도 보조검산
- 모든 root가 닫힌 뒤 directed-arithmetic calculator 설계

### 사용자 PC 도움이 나중에 유용할 수 있는 일

- 많은 \(k\) 후보에서 cutoff와 error-budget 최적화를 수치 탐색하는 작업
- directed interval arithmetic나 Lean formalization을 실제 설치·실행하는 작업
- 최종 threshold calculator가 완성된 뒤 장시간 재현 계산

현재는 root input이 열려 있어 이런 장시간 계산을 먼저 해도 정리 threshold가 나오지 않는다.

### 현재 자원조건 아래 바로 끝내기 어렵거나 의미 없는 일

- 아직 없는 Hypothesis 1(2) 수치상수를 CPU brute force로 대신하는 일
- \(10^{20}\) 또는 \(10^{21}\)까지의 finite prime-gap 계산으로 “모든 충분히 큰 \(X\)” 정리를
  증명하는 일
- 열린 analytic input을 168시간 계산, 32GB RAM, 100GB 디스크만으로 자동 해결한다고
  약속하는 일

병목은 현재 연산량보다 수학적 proof dependency다.

## 6. 최종 판정

다음 상태 이동은 타당하다.

~~~text
H1B-P94 actual FGKMT/FMT call
RATE_MISSING -> ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
~~~

다음 상태 이동은 타당하지 않으므로 수행하지 않는다.

~~~text
Maynard general P94     remains RATE_MISSING
H1B-COMP-01             remains HARD_BLOCKER
SIV-07 / SIV-09         remain HARD_BLOCKER
X_cert                  remains OPEN
~~~

## 7. 다음 권장 작업

1. `H1c-1`: Proposition 9.2에 필요한 quantitative character/prime-distribution package를
   원 논문과 explicit 후속정리에서 먼저 찾는다.
2. 적합한 drop-in 정리가 없으면 실제 affine forms와 exceptional modulus를 보존해 직접
   finite reduction을 작성한다.
3. 그 뒤 P91/P92/L93/P95를 각각 닫고 공통 moment budget을 만든다.
4. `SIV-07`이 닫힌 뒤에만 FMT 확률축과 최종 \(x\to X\) 변환을 합성한다.

사용자가 지금 실행하거나 설치해야 할 것은 없다.
