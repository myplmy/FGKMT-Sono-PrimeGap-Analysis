# Sono/FMT H1b-1b-2 \(c_\gamma\) 오류 정규화·Lemma 8.4 보정 원장

- 작성일: 2026-09-06
- 갱신일: 2026-09-07
- 상위 obligation: SIV-07
- 입력 정본:
  [H1b-1b multiplier 복원·오류항 교정](18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md)
- 비판적 source 감사:
  [Kuperberg·GGPY 오류항 검토](../../review/27_20260906_H1b1b_Kuperberg_GGPY_error_term_타당성검토.md)
- 기계 원장:
  data/Sono_FMT_H1b1b2_cgamma_error_normalization_v1.json
- actual-call local-factor·제외모듈 정식화:
  [H1b-1b-2a local-factor·제외모듈 하한](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
- application 전수감사:
  [H1b-1b-2a.1 actual application-exclusion inventory](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)

## 1. 목적

GGPY/Maynard에 인쇄된 \(c_\gamma\)-포함 오류항은 원래 가정만으로 안전하지 않다.
이 원장은 Maynard Lemma 8.4를 숫자로 다시 증명하기 위해 필요한 추가 의무를
세 경로로 나눈다.

1. 각 단계의 \(c_{\gamma,j}\)를 아래에서 명시적으로 누르는 경로
2. \(R\) 또는 \(z\)를 \(L\)과 \(k\)에 비해 충분히 크게 만들어 강한 상대오차를
   복원하는 경로
3. \(c_\gamma\)로 나누지 않고 절대오차를 다변수 합 전체에서 직접 합성하는 경로

2026-09-07 H1b-1b-2a.1은 첫 번째 경로의 actual 비제외 local factor와 확대된
제외모듈 11개 subapplication의 상계를 모두 닫았다. 따라서 첫 번째 경로는
`PRIMARY_EXPLICIT_LOWER_BOUND_ROUTE_SELECTED`이고 모든 추적 호출에서
\(c_{\gamma,j}>1/[3(1+\log\Lambda_*)]\)를 쓸 수 있다. 이는 추상
`g(p)=p+O(k)` 전체나 Lemma 8.4의 수정된 (r)-회 오류 합성을 닫은 것이 아니다.
기본 절대오차 상수 (C_{3,\mathrm{abs}})도 계속 빠져 있으므로 이 문서는 여전히
전체 증명 완료 보고서가 아니라 proof-obligation 원장이다.

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

의 explicit lower bound가 필요하다. H1b-1b-2a에서는 이를 큰 제외 소수와 따로
추정하지 않고 §3.2의 한 정수 \(Q_j\)에 합쳤다.

### 3.2 큰 제외 소수

\(\widetilde W_{j+1}\prod_{i>j+1}e_i\)의 큰 소인수도 local factor \(1-1/p\)를 만든다.
H1b-1b-2a는 canonical \(W_i\) 구성의 prime support를 계수 판별식까지 추적해

\[
\log Q^{\rm base}_j\le\Lambda^{\rm base}_j
\]

의 명시식을 얻었다. H1b-1b-2a.1은 실제 호출의
\(dW_i,W_i',a_mWBr,rW_m,W_0\)를 전수 감사해 호출별
\(\eta_{\rm app,j}\in\{0,\log R\}\)를 인증했다. 모든 호출·iteration에 대해

\[
\Lambda^{\rm app}_j\le\Lambda_*=
2k^2\log(2k^2)+k(k-1)\log2+
\left\{\frac{10\alpha(2k^2-k+1)}\theta+k\right\}\log R.
\]

Rosser--Schoenfeld Theorem 15에 의해 작은·큰 제외 소수의 손실 전체는

\[
\frac{\varphi(Q_j)}{Q_j}>
\frac{1}{3(1+\log\Lambda_*)}
\]

로 내려간다. 이는 named parameter를 남긴 project-parameterized explicit 결과이며,
수치형 finite theorem은 아니다.

### 3.3 제외되지 않은 소수

제외되지 않은 \(p\)에서 local factor는

\[
\frac{1-1/p}
{1-1/(1+n_j(p)+g(p))}.
\]

추상 \(g(p)=p+O(k)\)만으로는 여전히 multiplier와 부호가 부족하다. 그러나 실제 호출은

\[
p-a,\quad
\frac{(p-a)^2}{p-1},\quad
\frac{(p-a)^2}{p+a-2},\quad
p-a-\frac{a-1}{p-1}
\]

의 네 family로 덮이며 모두 \(0<g(p)\le p-a\)다. 비제외 소수에서는
\(n_j(p)\le a-1\)이므로 local factor는 exact하게 1 이상이다. 따라서 actual-call
비제외 무한곱에는 별도 tail 손실이 없다.

### 3.4 합성

H1b-1b-2a.1이 모든 추적 단계의 유효 제외모듈을 인증했으므로

\[
c_{\gamma,j}\ge c_{\min}(k,r,R)>0
\]

를 얻는다. 보수적 공통 선택은 인증된
\(c_{\min}=1/[3(1+\log\Lambda_*)]\)이다.
H1b-1b의 절대오차 transfer와 결합한 상대 multiplier는

\[
\frac{2C_{3,\mathrm{abs}}(A_1,A_2)}
{c_{\min}(k,r,R)}
\]

이며, 초등 약화를 쓰면

\[
\frac{2C_{3,\mathrm{abs}}}{c_{\min}}
\le6C_{3,\mathrm{abs}}(1+\log\Lambda_*)
\]

이다. 현재 \(\Lambda_*\)는 닫혔지만, \(C_{3,\mathrm{abs}}\), 그 유효범위와
수정된 \(r\)-회 합성은 아직 없다.

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
| H1B1B2-CMIN-SMALL-EXCLUDED | 작은 제외 소수 곱 하한 | PRIMARY_EXPLICIT_BOUND_AVAILABLE |
| H1B1B2-CMIN-LARGE-EXCLUDED | 큰 제외 소수 곱 하한 | PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS |
| H1B1B2-CMIN-NONEXCLUDED | 나머지 무한곱 하한 | PROJECT_FINITE_COMPONENT_CLOSED_FOR_ACTUAL_CALLS |
| H1B1B2-CMIN-COMPOSE | uniform \(c_{\min}\) 합성 | PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS |
| H1B1B2-SIZE-GATE | Kuperberg형 복원 | OPTIONAL_SECONDARY_ROUTE |
| H1B1B2-ROUTE-DECISION | 증명된 경로 선택 | PRIMARY_EXPLICIT_LOWER_BOUND_ROUTE_SELECTED |
| H1B1B2-RFOLD-COMPOSITION | \(r\)회 오류 누적 | HARD_BLOCKER |

## 7. 먼저 할 일과 중단 조건

### 권장 1단계

Kuperberg/HR recurrence에서 \(C_{3,\mathrm{abs}}(A_1,A_2)\)와 그 최초 유효범위를
복원한다. 예상 8–24시간 이상. 그 뒤 Maynard actual call의 \(A_1,A_2,L\) bound와
\(6C_{3,\mathrm{abs}}(1+\log\Lambda_*)\) 손실을 넣어 Lemma 8.4의
\(r\)-회 귀납을 재합성한다. \(C_{3,\mathrm{abs}}\)가 없으면 합성에 착수하지 않는다.

### 병렬 권장

H1c-1의 quantitative character/Bombieri--Vinogradov package를 계속 source tracing한다.
예상 8–24시간 이상.

### 아직 하지 않을 일

- threshold calculator 작성
- 장시간 prime sweep
- P018-B 자동 실행
- \(C_{3,\mathrm{abs}}\), \(B_L,B_k\)에 임의 숫자 대입
- SIV-07 또는 \(X_{\mathrm{cert}}\) 상태 승격

## 8. 사용자 수행사항

현재 별도 수행절차 필요없음. 이 단계는 문헌·수식 감사이며 CPU-heavy 실험으로 proof
obligation을 대신할 수 없다. Lean이나 추가 Python 라이브러리도 현재 필요하지 않다.
