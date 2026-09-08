# H1b-1b-2d.1a Maynard 905행 \(H\) remainder 타당성 검토

- 작성일: 2026-09-08
- 검토 대상: Maynard source 905행의 \(J_k(H)\) 적용과 numerical \(C^1\) 복원 가능성
- 정식화 정본:
  [25_Sono_FMT_H1b1b2d1a_H_remainder_bypass.md](../method/theory/25_Sono_FMT_H1b1b2d1a_H_remainder_bypass.md)
- 기계 계약:
  [Sono_FMT_H1b1b2d1a_H_remainder_bypass_v1.json](../method/theory/data/Sono_FMT_H1b1b2d1a_H_remainder_bypass_v1.json)

## 1. 최종 판정

\[
\boxed{\texttt{PARTIAL VALID: C1 BYPASS CLOSED, SCALAR MULTIPLIER OPEN}}
\]

원문의 \(H=F+O(\eta F_2)\)만으로 remainder의 도함수 상계를 얻을 수 있다는 생각은
타당하지 않다. \(O\)-표기는 값의 크기만 제한하고, 외부 변수에 따른 선택의 연속성이나
미분 가능성을 보장하지 않기 때문이다.

그러나 905행의 목표가 \(y_{\mathbf r}^{(m)}\)의 제곱합이라는 점을 이용하면 전역 \(H\)를
만들 필요가 없다. 격자점별 scalar bound를 제곱 부등식으로 옮기고, 오른쪽을 일곱 개의
비음수 smooth tensor symmetry class로 정확히 전개하는 우회는 타당하다.

따라서 functional obstruction은 제거됐지만 원문 986--999행의 숨은 scalar multiplier가
남는다. H1B-L84, SIV-07, \(X_{\rm cert}\)를 승격하지 않은 것이 맞다.

## 2. 어떤 부분이 개선됐는가

이전 문제는 다음과 같았다.

~~~text
원문 H가 실제 smooth 함수인지 모름
  -> C1 norm을 계산할 수 없음
  -> Lemma 8.4 입력으로 수치화할 수 없음
~~~

이번 우회 뒤에는 다음처럼 바뀐다.

~~~text
격자점별 |Z-A| <= epsilon B만 필요
  -> |Z^2-A^2| <= 2 epsilon AB + epsilon^2 B^2
  -> A^2, AB, B^2는 명시적 smooth tensor 합
  -> 남은 문제는 epsilon의 숫자와 적용 시작점
~~~

함수 전체의 모양을 복원하는 어려운 문제를 하나의 스칼라 상수 문제로 축소했으므로 실제
진전이다. 다만 스칼라 상수가 아직 없기 때문에 전체 theorem node를 닫은 진전은 아니다.

## 3. 수학적 타당성 점검

### 3.1 제곱 부등식

\(D=Z-A\), \(|D|\le\varepsilon B\), \(A,B\ge0\)이면

\[
|Z^2-A^2|=|2AD+D^2|
\le2\varepsilon AB+\varepsilon^2B^2.
\]

이는 exact algebra이고 \(Z\ge0\)조차 요구하지 않는다. 코드가 양·음 오차를 유리수로
각각 검증한다.

### 3.2 tensor 전개의 완전성

\(A=I_NP\prod N_i\),
\(B=I_W\prod N_i+I_N\sum_jW_j\prod_{i\ne j}N_i\)를 직접 제곱·곱하면
A2 1종, AB 2종, B2 4종만 생긴다. 코드가 multiplicity
\(1,d,\binom d2\)와 교차항 계수 2를 별도 필드로 보존한다. toy 양수값에서 direct
\(AB,B^2\)와 전개식의 일치를 검사했다.

### 3.3 smoothness와 support

\(P(S)=I_N^{-1}\int\psi(S+t)N(t)dt\)는 compact support 적분이므로 smooth이고
\(|P'|\le50\), \(|(P^2)'|\le100\)이다. 나머지는 theory 24에서 이미 감사한
N2, NW, W2 profile이다. 유일한 support-2 W2 좌표는 먼저 합하므로 기존
excluded-modulus upper를 손상시키지 않는다.

### 3.4 무엇을 증명하지 않았는가

- 원문의 숨은 \(C_Y\)가 1이라는 주장
- 915행의 log-log 한 제곱형이 finite 범위에서 옳다는 주장
- 986행의 인쇄 \(\Delta\)를 그대로 사용해도 된다는 주장
- conditional evaluator에 넣은 임의 \(\varepsilon\)가 source-certified라는 주장
- 실제 main \(J_k(F)\)에 대한 작은 상대오차 또는 Proposition 6.1 전체

## 4. 원문 불일치가 현재 연구에 미치는 영향

### 4.1 \((\log\log R)^2\) 대 \(\log\log R\)

statement와 proof의 두 곳이 제곱형이고 915행만 1차형이다. asymptotic 결론에서는 둘 다
작아질 수 있어 원 논문의 질적 결론에 즉시 반례가 되는 것은 아니다. 그러나 numerical
threshold에는 한 인자가 매우 중요하므로 더 약한 제곱형을 사용해야 한다.

### 4.2 determinant product의 \(i=m\)

인쇄대로면 \(\Delta=0\)이라 “\(t\mid\Delta\)”가 의도한 유한 prime support를 나타내지
못한다. 실제 construction은 \(j\ne m\)의 \(W'_j/W_j\)만 사용하므로 그 범위에 맞는
\(\Delta_m\)를 별도 정의하고 상계를 재증명해야 한다. 조용히 오자를 고쳤다고 끝내지 않고
scalar multiplier gate의 명시 의무로 남겼다.

### 4.3 998--999행 정규화

표시된 식만으로는 \(e_m\) 합의 \(\log R\)과 바깥 \(1/\log R\)이 어떻게 합쳐져 최종
H-remainder가 되는지 수치적으로 확정할 수 없다. 이 지점에서 원문의 \(\ll\)를 1로
간주하면 잘못된 threshold를 만들 수 있다.

## 5. 선행연구 적용성

Maynard 출판본은 구조의 정본이지만 수치 multiplier와 finite cutoff를 주지 않는다.
Axiom Math의 PrimeGapsLib는 반복 partial summation을 proof object로 분리하는 좋은
구조적 비교 대상이지만, 다른 sieve datum과 존재형 large-parameter 상수에 의존하므로
현재의 \(C_Y\)를 대신하지 못한다. 표적 검색에서 동형의 완성된 peer-reviewed numerical
lemma는 찾지 못했다. 이것은 문헌 전체 신규성 판정이 아니다.

따라서 선행 결과를 먼저 재사용하고, 남은 986--999행 연결부만 직접 정량 재증명하는
전략이 효율성과 정확성 모두에서 타당하다.

## 6. 코드 검증의 의미

source/h1b1b2d1a_h_remainder_bypass.py는 다음만 수행한다.

- exact rational square inequality
- 일곱 tensor symmetry class와 multiplicity 보존
- \(P,P^2\) derivative allowance를 포함한 support-scaled norm 조합
- 가정한 \(\varepsilon\)에 대한 conditional finite-product 평가
- parent node non-promotion 강제

수치 grid나 계산 결과가 연속함수 증명을 대신하지 않는다. 연속 bound의 근거는 theory 25의
해석적 proof이고 코드는 전개·계수·계약의 회귀검사다.

## 7. 후속 판정 gate

### 직접 후속: H1b-1b-2d.1a.1

986--999행을 처음부터 수치화해

\[
\varepsilon_Y\le C_YT_k(\log\log R)^2/\log R
\]

의 \(C_Y\)와 finite range를 얻는다. \(s\)-Euler product, \(t\)-divisor sum,
determinant 크기, prefactor와 line-1015 error를 분리한 뒤 마지막에만 합쳐야 한다.

### 권장 순서의 다음 공통 gate: H1b-1b-2d.1b

1096·1135행의 sharp indicator에는 \(\xi\log x\)의 유한 하한이 필요하다. 이는 이번 scalar
gate와 독립적이므로, 1a.1이 장기화될 경우 source tracing을 병행할 수 있다.

두 gate가 닫혀도 Lemmas 8.5--8.6, moment budget과 H1c/PAP가 남는다. 그러므로 현시점에
threshold calculator나 장시간 prime experiment를 만드는 것은 타당하지 않다.
