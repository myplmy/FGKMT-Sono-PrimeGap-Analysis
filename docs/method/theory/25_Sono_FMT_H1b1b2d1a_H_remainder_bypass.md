# Sono/FMT H1b-1b-2d.1a: 905행 \(H\) remainder의 square-sum 우회

- 작성일: 2026-09-08
- 상위 obligation: H1B-L84, H1B1-PACKAGE, SIV-07
- 선행 정본:
  [H1b-1b-2d smooth 반복합성](24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md)
- 기계 계약:
  [Sono_FMT_H1b1b2d1a_H_remainder_bypass_v1.json](data/Sono_FMT_H1b1b2d1a_H_remainder_bypass_v1.json)
- 구현: source/h1b1b2d1a_h_remainder_bypass.py
- 비판적 검토:
  [H remainder 우회 타당성 검토](../../review/31_20260908_H1b1b2d1a_H_remainder_타당성검토.md)

> **후속 상태 정정(2026-09-08):** 이 문서가 OPEN으로 남긴 scalar multiplier는
> [theory 26](26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md)에서 parameterized finite
> component로 닫혔다. 다만 H1B-L84, SIV-07, \(X_{\rm cert}\)는 여전히
> RATE_MISSING, HARD_BLOCKER, OPEN이다. 아래 OPEN 판정은 이 단계가 끝났을 당시의
> 역사적 판정이다.

## 1. 결론

이번 단계는 원문이 정의하지 않은 “전역 smooth \(H\)”를 만들어 내지 않는다. 대신 905행이
실제로 합하는 것은 \(H\) 자체가 아니라 \(y_{\mathbf r}^{(m)}\)의 제곱이라는 점을 이용한다.
그 결과 다음을 project lemma로 닫았다.

\[
\boxed{\text{전역 }H\text{의 }C^1\text{ norm은 필요하지 않다.}}
\]

격자점별 정규화값 \(Z_{\mathbf r}\)에 대해

\[
|Z_{\mathbf r}-A(\mathbf u_{\mathbf r})|
\le \varepsilon B(\mathbf u_{\mathbf r})
\tag{25.1}
\]

라는 수치화된 스칼라 오차만 있으면 된다. 그러면 제곱합의 오차는 \(A^2,AB,B^2\)라는
명시적 비음수 smooth tensor 합으로 바뀐다.

그러나 Maynard 원문 986--999행의 여러 \(\ll\) 상수는 아직 숫자로 복원되지 않았다.
따라서 판정은 다음과 같다.

~~~text
functional H C1 obstruction       BYPASSED
square-sum tensor expansion       PROJECT EXPLICIT
source scalar multiplier C_Y      OPEN
line 905 actual call              RATE_MISSING
H1B-L84 / SIV-07 / X_cert         RATE_MISSING / HARD_BLOCKER / OPEN
~~~

즉 불명확한 함수 문제를 더 작은 스칼라 상수 문제로 줄였지만, 905행 전체를 닫지는 않았다.

## 2. 쉽게 설명하면

원문은 “실제 값은 기준값에서 대략 작은 만큼 벗어난다”고 말하지만, 그 벗어남이 변수에 따라
얼마나 매끄럽게 움직이는지는 말하지 않는다. 이전 단계에서는 이 매끄러움을 알아야 원문의
다변수 합 공식에 넣을 수 있다고 보았다.

하지만 우리가 필요한 것은 그 값을 제곱해서 더한 결과다. 기준값을 \(A\), 오차의 크기를
최대 \(\varepsilon B\)라고 하면 실제 값 \(Z\)가 위쪽이나 아래쪽으로 움직여도

\[
|Z^2-A^2|\le 2\varepsilon AB+\varepsilon^2B^2
\]

이다. 오른쪽의 세 함수는 모두 이미 알고 있는 매끄러운 함수의 합으로 풀린다. 따라서
“오차가 어떻게 흔들리는가”는 몰라도 되고, “각 점에서 최대 얼마인가”만 알면 된다.
아직 남은 일은 원문의 “최대 얼마”에 숨어 있는 상수를 실제 숫자로 계산하는 것이다.

## 3. 원문 경로의 전수 추적

주 원천은 Maynard, Dense Clusters of Primes in Subsets,
DOI 10.1112/S0010437X16007296, arXiv:1405.2593이다.

| 원문 위치 | 역할 | 이번 판정 |
|---|---|---|
| source 411--426행 | \(F,N,W,F_2\) 정의 | 정확히 고정 |
| 488--514행 | YDifference의 한 좌표 이동 오차 | project multiplier 89가 선행 단계에서 닫힘 |
| 838--846행 | \(y_{\mathbf r}^{(m)}\)와 \(H\)를 연결하는 Lemma 9.3 | \(H\)가 pointwise \(O\)로만 표현됨 |
| 903--916행 | 905행 다중합과 \(J_k(H)\) | 실제 우회 대상 |
| 939--981행 | 정확한 합을 main/error로 분리 | 격자점별 scalar error 구조 확인 |
| 986--999행 | \(s,t,e_m\) error 상계 | 숨은 수치 multiplier의 핵심 미해결부 |
| 1002--1038행 | main Euler product와 \(e_m\) 합 | line-1015 one-step 상계는 선행 package로 explicit |

### 3.1 왜 원문의 \(H\)에서 \(C^1\)을 읽을 수 없는가

원문은 외부 격자점 \(\mathbf u_{\mathbf r}\)마다 하나의 적분값을 계산한 뒤

\[
\int H(\mathbf u_{\mathbf r},t_m)dt_m
=\int F(\mathbf u_{\mathbf r},t_m)dt_m
+O\!\left(\eta\int F_2(\mathbf u_{\mathbf r},t_m)dt_m\right)
\]

로 압축한다. 이 표기는 격자점 사이에서 같은 remainder 함수가 선택됐는지, 그 선택이
연속인지, 도함수가 얼마인지 말하지 않는다. 값의 \(O\)-상계만으로 remainder의 도함수
상계를 추론하는 것은 타당하지 않다.

### 3.2 원문 표기의 주의점

1. Lemma 9.3의 844행과 proof 1026행은
   \(T_k(\log\log R)^2/\log R\)인데 915행은 제곱 하나를 잃는다. finite package에서는
   더 약하지만 안전한 제곱형을 보존한다.
2. 구 author TeX 986행의 \(\Delta=\prod_{i=1}^k(a_mb_i-a_ib_m)\)는 \(i=m\) 항 때문에
   0이지만, 최종 출판본 식 (9.43)은 정확히 \(i\ne m\)으로 고쳐져 있다. 프로젝트는
   최종 출판본을 정본으로 사용한다.
3. 998행에서 999행으로 가는 \(\log R\) 정규화는 표시만으로 수치 multiplier를 결정할
   만큼 자세하지 않다. 임의로 누락된 인자를 추정하지 않고 해당 연결을 재증명 대상으로 둔다.

determinant 항목은 정식 erratum이 필요한 출판 오류가 아니라 오래된 author TeX와 최종
출판본의 차이다. 나머지 log-log 지수와 수치 정규화는 원문 내부 식과 변수 범위를 대조해
얻은 project source caution이다.

## 4. 적분 뒤의 두 명시적 함수

외부 변수의 수를 \(d=k-1\), \(S=\sum_{i\ne m}u_i\)라 두고

\[
I_N=\int_0^\infty N(t)dt,\qquad
I_W=\int_0^\infty W(t)dt,
\]

\[
P(S)=\frac1{I_N}\int_0^\infty\psi(S+t)N(t)dt
\tag{25.2}
\]

라 둔다. \(N\ge0\), \(0\le\psi\le1\), \(|\psi'|\le50\)이므로

\[
0\le P\le1,\qquad P(S)=0\ (S\ge1),\qquad |P'(S)|\le50.
\tag{25.3}
\]

미분은 compact support 위 적분이므로 적분 안으로 옮길 수 있다. 이제

\[
A(\mathbf u)=\int F(\mathbf u,t_m)dt_m
=I_NP(S)\prod_{i\ne m}N(u_i),
\tag{25.4}
\]

\[
B(\mathbf u)=\int F_2(\mathbf u,t_m)dt_m
=I_W\prod_{i\ne m}N(u_i)
+I_N\sum_{j\ne m}W(u_j)\prod_{\substack{i\ne m\\i\ne j}}N(u_i).
\tag{25.5}
\]

이 두 등식은 \(F,F_2\)의 정의를 \(m\) 좌표에 대해 직접 적분한 정확식이다.

## 5. Project lemma: square-sum 우회

### 명제

\(A,B\ge0\), \(\varepsilon\ge0\)이고 (25.1)이 성립하면

\[
\boxed{
|Z_{\mathbf r}^2-A(\mathbf u_{\mathbf r})^2|
\le 2\varepsilon A(\mathbf u_{\mathbf r})B(\mathbf u_{\mathbf r})
+\varepsilon^2B(\mathbf u_{\mathbf r})^2.
}
\tag{25.6}
\]

### 증명

\(D=Z-A\)라 두면 \(|D|\le\varepsilon B\)이고

\[
|Z^2-A^2|=|2AD+D^2|
\le2A|D|+|D|^2
\le2\varepsilon AB+\varepsilon^2B^2.
\]

\(Z\)의 부호는 가정하지 않아도 된다. □

이를 모든 격자점에 더하면 \(Z^2\) 합과 \(A^2\) 합의 차이는 \(AB,B^2\)의 합으로
상계된다. 따라서 smooth summation은 존재가 불명확한 \(H^2\)가 아니라
\(A^2,AB,B^2\)에만 적용한다.

## 6. 누락 없는 tensor 전개

\(N_i=N(u_i)\), \(W_i=W(u_i)\)라 쓰면 일곱 symmetry class가 전부다.

| class | multiplicity | coefficient | smooth profile | cutoff |
|---|---:|---|---|---|
| A2_cutoff | 1 | \(I_N^2\) | \((N^2)^d\) | \(P^2\) |
| AB_base | 1 | \(I_NI_W\) | \((N^2)^d\) | \(P\) |
| AB_one_NW | \(d\) | \(I_N^2\) | \(NW(N^2)^{d-1}\) | \(P\) |
| B2_base | 1 | \(I_W^2\) | \((N^2)^d\) | 없음 |
| B2_one_NW | \(d\) | \(2I_NI_W\) | \(NW(N^2)^{d-1}\) | 없음 |
| B2_one_W2 | \(d\) | \(I_N^2\) | \(W^2(N^2)^{d-1}\) | 없음 |
| B2_two_NW | \(\binom d2\) | \(2I_N^2\) | \((NW)^2(N^2)^{d-2}\) | 없음 |

\(P^2\)에는 \(|(P^2)'|\le2|P||P'|\le100\)을 사용한다. 따라서 theory 24의
support-scaled profile norm에 cutoff derivative 50 또는 100만 추가하면 모든 family의
finite-product error가 명시된다.

B2_one_W2의 \(W^2\) 좌표는 support가 \([0,2]\)이므로 반드시 먼저 합한다. 이 좌표를
현재 좌표로 제거한 뒤에는 남은 N2 좌표만 제외모듈에 들어가므로 theory 24의
\(\Lambda_*\)를 보존한다.

## 7. conditional finite evaluator의 의미

코드의 conditional_h_square_bypass_certificate는 사용자가 임의로 넣은
\(\varepsilon\)에 대해 세 category의 corrected finite-product 상계를 계산한다. 공통
one-step coefficient는

\[
\frac{C_{8.3}(1/2,8)\{6+\log\Lambda_*\}}{\log R}
\tag{25.7}
\]

이고, 각 tensor 좌표의 support-scaled norm을 정확한 유한 곱에 넣는다.

이 함수에 숫자를 넣었다고 그 숫자가 Maynard 원문에서 증명된 것은 아니다. 반환값은 항상

~~~text
source_scalar_multiplier_certified = false
line_905_closed                    = false
siv_07_closed                      = false
x_cert_ready                       = false
~~~

로 고정된다. 이는 열린 상수를 실수로 theorem input으로 승격하지 못하게 하는 안전장치다.

## 8. 아직 필요한 스칼라 재증명

목표는 유한 범위와 수치 \(C_Y\)를 가진

\[
\varepsilon_Y
\le C_Y\frac{T_k(\log\log R)^2}{\log R}
\tag{25.8}
\]

를 얻는 것이다. 다음 네 항을 각각 수치화해야 한다.

1. 986행 \(s\)-합 Euler product의 절대 multiplier와 시작 범위
2. 988--993행 \(t\mid\Delta_m\) divisor 합의 multiplier와
   \(\Delta_m=\prod_{i\ne m}|a_mb_i-a_ib_m|\)의 유한 상계
3. 995--999행 \(r/\phi_L(r)\), \(a_mWB\), \(e_m\) 합 사이의 정확한 prefactor 정규화
4. 이미 explicit인 line-1015 Lemma 8.3 branch와 위 YmError branch를 합친 공통 \(C_Y\)

Lemma 8.2의 89, Lemma 8.3의 교정 multiplier, actual
\(a=1/2,A_2=8,L=5+\log\Lambda_*\)와 이번 tensor 합성은 재사용할 수 있다. 반면 위 네
\(\ll\) multiplier를 1로 놓는 것은 금지한다.

## 9. 선행연구 우선 조사 결과

- Maynard 출판본과 author TeX가 직접 원천이다.
- Axiom Math PrimeGapsLib의 ApplyPartialSum 계열은 반복 partial summation을 별도
  증명 객체로 보존하는 구조를 보여 준다. 그러나 다른 sieve package와 존재형
  large-parameter 가정을 사용하므로 (25.8)의 수치 \(C_Y\)를 주지 않는다.
- 표적 검색에서는 실제 905행의 동일한 \(F,F_2\), norm, excluded modulus와 finite
  multiplier를 모두 제공하는 peer-reviewed lemma를 찾지 못했다.

이는 전 세계 문헌에 그런 결과가 없다는 novelty 주장이 아니다. 따라서 검증된 선행식을
우선 재사용하고, 남은 986--999행 연결부만 직접 정량 재증명하는 것이 가장 작은 다음 작업이다.

## 10. 상위 상태와 다음 단계

이번 결과로 이전 문구 “\(H\)의 수치 \(C^1\) norm이 반드시 필요하다”는 더 이상 정확하지
않다. 정확한 blocker는 “격자점별 scalar remainder의 수치 multiplier와 finite range”다.

하지만 그것도 아직 OPEN이고, sharp \(\xi\log x\), Lemmas 8.5--8.6, moment budget,
H1c/PAP가 남는다. 따라서

\[
H1B\text{-}L84=\texttt{RATE\_MISSING},\quad
SIV\text{-}07=\texttt{HARD\_BLOCKER},\quad
X_{\rm cert}=\texttt{OPEN}
\]

을 유지한다. 다음 직접 하위 gate는 H1b-1b-2d.1a.1의 scalar \(C_Y\) 재증명이고,
권장 순서의 다음 독립 공통 gate는 H1b-1b-2d.1b의 sharp \(\xi\log x\) finite scale이다.
모든 root가 닫히기 전에는 threshold calculator나 새 prime sweep을 만들지 않는다.
