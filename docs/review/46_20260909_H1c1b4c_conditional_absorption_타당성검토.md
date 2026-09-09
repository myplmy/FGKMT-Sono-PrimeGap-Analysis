# H1c-1b.4c conditional absorption 타당성 검토

- 검토일: 2026-09-09 KST
- 대상: Bordignon 12항·count-transfer·prime density의 한 목표 단위 합성
- 최종 판정:
  `CONDITIONAL BUDGET VALID / SOURCE CONSTANT AND UNCONDITIONAL RATE OPEN`
- 정식화:
  [`docs/method/theory/40_Sono_FMT_H1c1b4c_conditional_absorption.md`](../method/theory/40_Sono_FMT_H1c1b4c_conditional_absorption.md)

## 1. 한눈에 보는 판정

| 질문 | 판정 | 이유 |
|---|---|---|
| 이전 12개 source term이 모두 들어갔는가 | 예 | \(C_A\) 항 1개와 non-\(C_A\) 11개를 분리 |
| count 변환 비용도 들어갔는가 | 예 | prime powers와 half-open endpoint 2개 포함 |
| exact prime total을 근사값으로 바꿨는가 | 아니오 | density lower는 분모 비교에만 사용 |
| dyadic 내부의 worst point를 확인했는가 | 예 | term 3만 upper endpoint, 나머지는 lower endpoint |
| 한 \(r\) 점만 검사했는가 | 아니오 | \(L\)-bin과 growing \(r\) 단조성 증명 포함 |
| \(C_A\) 값을 논문에서 얻었는가 | 아니오 | 허용 조건만 역산 |
| H1(2), P9.2가 닫혔는가 | 아니오 | source \(C_A\)가 핵심 blocker |

## 2. 왜 조건부 결과가 의미 있는가

미지 상수를 복원하기 전에 허용 크기를 계산하면 두 가지를 알 수 있다.

1. 나머지 13개 비용이 이미 실패하는지 먼저 배제할 수 있다.
2. source 재증명이 달성해야 할 정확한 목표를 알 수 있다.

이번 결과는 13개 비용 자체는 충분히 작음을 보였다. 남은 질문은 오직 source에서 복원할
\(C_A\)가

\[
C_A<C_{\mathrm{allow}}(r,L)=\frac{1-B_0(r,L)}{36(1+A\ell)L^{-6}}
\]

를 만족하는가다. 실패하더라도 무엇이 부족한지 수치적으로 진단할 수 있으므로 유용하다.

## 3. 보수적 cutoff의 해석

증명된 cutoff \(r\ge500{,}000{,}000\)은 “가장 작은 가능한 \(r\)”가 아니다. exact rational
비교를 단순하게 만들기 위한 충분조건이다. 이에 대응하는

\[
\log T\ge(500{,}000{,}000)^5
\]

도 경험적 maximal-gap 범위와 비교할 수 없을 만큼 크다. 그러나 현재 목적은 실제 소수를
그 크기까지 계산하는 것이 아니라, asymptotic proof의 `sufficiently large`를 finite
의존관계로 바꾸는 것이다.

이 cutoff만으로 theorem threshold \(X_{\mathrm{cert}}\)가 되지는 않는다. source \(C_A\),
P9.1/L9.3/P9.5와 상위 hypergraph 의무들이 모두 같은 범위에서 닫혀야 최종 threshold의
한 구성요소가 된다.

## 4. 정확도 감사

### 4.1 누락 방지

machine contract는 다음 회계를 강제한다.

```text
11 non-C_A Bordignon terms
+ 1 prime-power term
+ 1 half-open endpoint term
= 13 non-C_A terms

1 C_A Bordignon term
--------------------
14 normalized components total
```

항 수가 달라지면 helper와 회귀시험이 실패한다.

### 4.2 정밀도 오류와 교정

첫 시험에서 약 44자리인 \(r^5\)와 \((r+1)^5\)를 기본 15자리 `mpmath` 값으로 먼저
변환해 두 bin 경계가 같은 값으로 뭉개지는 오류를 발견했다. 정수 입력은 변환 전 exact
비교하고, 비정수와 로그 계산은 내부 80자리 context에서 수행하도록 즉시 교정했다.
교정 후 6/6 표적시험이 PASS했다.

이 오류는 문서의 수학 부등식을 바꾸지는 않았지만, fail-closed domain 검사를 약화시킬 수
있었으므로 작업원장과 검토 보고서에 숨기지 않고 남긴다.

## 5. 가장 중요한 한계: \(C_A\) 성장률

허용량은 대략 \(r^{28}/\log r\)이다. 이는 매우 큰 수처럼 보여도 \(r\)에 대한 polynomial이다.
반면 explicit analytic theorem의 상수는 parameter \(A\asymp r^2\)에 대해
\(\exp(cA)\) 또는 그보다 빠르게 커질 수 있다. 실제 source 재증명이 그런 성장률을 주면
고정 margin 10 경로는 실패한다.

따라서 \(C_A\le e^{500}\)를 “그럴듯한 예상”으로 취급하면 안 된다. 이는 다음 4d가 검증해야
할 합격선일 뿐이다.

## 6. 금지되는 해석

- “\(r=5억\)부터 H1(2)가 무조건 성립한다.”
- “Bordignon 상수는 \(e^{500}\) 이하이다.”
- “Sono/FGKMT theorem threshold를 얻었다.”
- “실제 maximal gap을 \(\exp((5억)^5)\)까지 계산해야 한다.”

모두 현재 증거보다 강하다.

## 7. 자원과 사용자 도움

이번 단계는 exact rational arithmetic과 짧은 100자리 회귀만 사용했다. 새 논문 다운로드,
Lean, 새 Python package, actual prime 계산이나 장시간 사용자 PC 실행은 필요하지 않았다.

사용자 수행절차는 **별도 수행절차 필요없음**이다.

## 8. 권장 다음 순서

1. **H1c-1b.4d source \(C_A\) 재증명** — 수일 이상. Theorem 3.4와 zero-density 전 항의
   growing-\(A\) 의존성을 복원한다.
2. **성장률 비교 gate** — 약 0.5--1일. 복원 상수와 \(r^{28}/\log r\) 허용량을 비교한다.
3. 성공할 때만 **H1(2)/P9.2 end-to-end 판정** — 약 1--2일.

## 9. 최종 판정

```text
non-C_A full absorption       = CLOSED FOR r >= 500,000,000
admissible C_A envelope       = CLOSED
C_A <= exp(500) implication   = CLOSED
source proof of that C_A bound = OPEN
unconditional H1(2) / P9.2    = OPEN
SIV-08 / X_cert               = HARD_BLOCKER / OPEN
```
