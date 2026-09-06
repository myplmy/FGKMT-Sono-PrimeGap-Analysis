# Sono/FMT H1b-1b-2 \(c_\gamma\) 오류 정규화·Lemma 8.4 보정 원장

- 작성일: 2026-09-06
- 상위 obligation: SIV-07
- 입력 정본:
  [H1b-1b multiplier 복원·오류항 교정](18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md)
- 비판적 source 감사:
  [Kuperberg·GGPY 오류항 검토](../../review/27_20260906_H1b1b_Kuperberg_GGPY_error_term_타당성검토.md)
- 기계 원장:
  data/Sono_FMT_H1b1b2_cgamma_error_normalization_v1.json

## 1. 목적

GGPY/Maynard에 인쇄된 \(c_\gamma\)-포함 오류항은 원래 가정만으로 안전하지 않다.
이 원장은 Maynard Lemma 8.4를 숫자로 다시 증명하기 위해 필요한 추가 의무를
세 경로로 나눈다.

1. 각 단계의 \(c_{\gamma,j}\)를 아래에서 명시적으로 누르는 경로
2. \(R\) 또는 \(z\)를 \(L\)과 \(k\)에 비해 충분히 크게 만들어 강한 상대오차를
   복원하는 경로
3. \(c_\gamma\)로 나누지 않고 절대오차를 다변수 합 전체에서 직접 합성하는 경로

현재는 어느 경로도 닫히지 않았다. 이 문서는 증명 완료 보고서가 아니라
중복과 가정 혼합을 막는 proof-obligation 원장이다.

## 2. Maynard Lemma 8.4의 실제 한 단계

Maynard source 568–578행에서 \(j+1\)번째 합을 수행할 때

\[
\gamma_j(p)=
\begin{cases}
0,
&
p\mid W_{j+1}\prod_{i=j+2}^{r}e_i,\\[2mm]
\dfrac{p}{1+n_j(p)+g(p)},
&
p\nmid W_{j+1}\prod_{i=j+2}^{r}e_i.
\end{cases}
\]

그리고

\[
c_{\gamma,j}
=\prod_p
\left(1-\frac{\gamma_j(p)}p\right)^{-1}
\left(1-\frac1p\right).
\]

Maynard는 \(g(p)=p+O(k)\), \(L\ll\log\log R\), “\(k\)가 충분히 크다”를 사용한다.
이 세 표기에는 \(X_{\mathrm{cert}}\)에 필요한 숫자가 없다.

## 3. \(c_{\gamma,j}\) 하한 경로의 분해

### 3.1 의무적으로 제외되는 작은 소수

모든 \(W_i\)는 \(p\le2k^2\)인 소수를 포함하므로 해당 소수에서 \(\gamma_j(p)=0\)이고
local factor는 \(1-1/p\)이다. 따라서 최소한

\[
\prod_{p\le2k^2}\left(1-\frac1p\right)
\]

의 explicit lower bound가 필요하다. 정성적 Mertens 식이 아니라 유효한 시작점과
오류상수가 있는 finite bound여야 한다.

### 3.2 큰 제외 소수

\(W_{j+1}\prod_{i>j+1}e_i\)의 큰 소인수도 local factor \(1-1/p\)를 만든다.
Maynard proof는 이 정수의 크기를 \(R^{O(k^2)}\)라고만 쓴다. 따라서 다음 숫자가 필요하다.

- \(O(k^2)\)의 실제 계수
- 주어진 정수 크기 아래에서 \(\prod_{p\mid N}(1-1/p)\)의 finite lower bound
- 모든 \(j\)와 남은 \(e_i\)에 공통인 범위

### 3.3 제외되지 않은 소수

제외되지 않은 \(p\)에서 local factor는

\[
\frac{1-1/p}
{1-1/(1+n_j(p)+g(p))}.
\]

\(g(p)=p+O(k)\)의 multiplier와 부호를 숫자로 알아야 이 무한곱의 앞부분과 tail을
아래에서 누를 수 있다. 단순히 local factor가 1에 가깝다고 말하는 것으로는 부족하다.

### 3.4 합성

위 세 부분을 합쳐 모든 단계에서

\[
c_{\gamma,j}\ge c_{\min}(k,r,R)>0
\]

를 얻으면, H1b-1b의 절대오차 transfer와 결합해 상대 multiplier

\[
\frac{2C_{3,\mathrm{abs}}(A_1,A_2)}
{c_{\min}(k,r,R)}
\]

를 얻는다. 이 식은 exact하지만 분자와 분모의 수치가 아직 없다.

## 4. Kuperberg형 size-gate 경로

Kuperberg Lemma 4.3은 특수 \(\nu_{\mathcal H}\)에 대해

\[
L\le\frac{\log z}{B_L},
\qquad
k^2\le\frac{\log z}{B_k}
\]

와 상대오차 \(O((L+k^4)/\log z)\)를 제시한다. 이 경로를 선택하려면

1. \(B_L,B_k\)와 \(O\)-multiplier를 수치화하고,
2. Maynard의 실제 \(\gamma_j\)가 같은 proof를 만족함을 보이고,
3. \(z=R\) 또는 각 단계의 실제 summation endpoint에서 조건이 동시에 성립하며,
4. \(j=0,\ldots,r-1\) 전체에 공통인 cutoff를 계산해야 한다.

이 경로는 인쇄된 Lemma 8.4 구조를 보존하기 쉽지만, 특수 함수에서 일반 함수로의
확장이 가장 큰 논리 위험이다.

## 5. 직접 절대오차 합성 경로

각 단계에서 절대오차가 생겨도 전체 합의 양성성과 exact product identity를 이용하면
매 단계마다 \(1/c_{\gamma,j}\)를 최악값으로 나누는 것보다 작은 손실을 얻을 가능성이 있다.
그러나 이는 현재 문헌의 한 줄 적용이 아니라 새로운 다변수 오차 증명이다.

따라서 지금은 아이디어로만 등록하며, 앞의 두 경로가 수치적으로 지나치게 나쁠 때
별도 정리로 설계한다.

## 6. 원장 요약

| ID | 내용 | 현재 상태 |
|---|---|---|
| H1B1B2-GAMMA-FORM | 단계별 \(\gamma_j\) 식 | PRINTED_EXACT_STRUCTURE |
| H1B1B2-CGAMMA-PRODUCT | \(c_{\gamma,j}\)와 product identity | PRINTED_EXACT_STRUCTURE |
| H1B1B2-CMIN-SMALL-EXCLUDED | 작은 제외 소수 곱 하한 | RATE_MISSING |
| H1B1B2-CMIN-LARGE-EXCLUDED | 큰 제외 소수 곱 하한 | RATE_MISSING |
| H1B1B2-CMIN-NONEXCLUDED | 나머지 무한곱 하한 | RATE_MISSING |
| H1B1B2-CMIN-COMPOSE | uniform \(c_{\min}\) 합성 | PARAMETERIZED_EXPLICIT |
| H1B1B2-SIZE-GATE | Kuperberg형 복원 | SPECIALIZATION_REQUIRED |
| H1B1B2-ROUTE-DECISION | 증명된 경로 선택 | HARD_BLOCKER |
| H1B1B2-RFOLD-COMPOSITION | \(r\)회 오류 누적 | HARD_BLOCKER |

## 7. 먼저 할 일과 중단 조건

### 권장 1단계

Maynard에서 실제로 쓰이는 \(g(p)\), \(n_j(p)\), \(W_i\), \(e_i\) 제약을 더 아래 source까지
추적해 local factor의 최악값을 식으로 만든다. 예상 4–10시간.

중단 조건:

- \(g(p)=p+O(k)\)의 multiplier가 또 다른 미접근 source에만 있으면 source gate로 돌린다.
- 얻은 \(c_{\min}\)이 너무 작아 최종 상대오차를 실용적으로 닫지 못하면 size-gate 경로와
  직접 합성 경로를 우선 비교한다.

### 권장 2단계

explicit Mertens/totient-product lower bound 후보를 1차 출처에서 수집하고
작은 범위를 exact integer arithmetic으로 메울 수 있는지 설계한다. 예상 4–12시간.

### 권장 3단계

Kuperberg recurrence의 \(B_L,B_k,O\)-상수와 일반 \(\gamma\) 확장 가능성을 감사한다.
예상 8–24시간 이상.

### 아직 하지 않을 일

- threshold calculator 작성
- 장시간 prime sweep
- P018-B 자동 실행
- \(c_{\min}\), \(C_{3,\mathrm{abs}}\), \(B_L,B_k\)에 임의 숫자 대입
- SIV-07 또는 \(X_{\mathrm{cert}}\) 상태 승격

## 8. 사용자 수행사항

현재 별도 수행절차 필요없음. 이 단계는 문헌·수식 감사이며 CPU-heavy 실험으로 proof
obligation을 대신할 수 없다. Lean이나 추가 Python 라이브러리도 현재 필요하지 않다.
