# P012 — P011 local/log-x nonstationary recurrence null 후속안

## 상태

`USER_DECISION_REQUIRED / RECOMMENDED_DESIGN_DRAFTED / NOT_IMPLEMENTED / NOT_QUEUED`

P011은 global gap frequency를 모든 plateau에 동일하게 적용해, 초기 구간의 큰 gap
발생을 심하게 과대예측했다. P012의 목적은 이 문제를 줄이기 위해 gap-start 위치를
log-x bin으로 나누고 plateau가 차지한 노출을 뺀 local rate로 기대 재발을 계산하는
것이다.

실행 전에 다음을 사전 고정해야 한다.

1. bin 폭과 shifted-bin sensitivity
2. plateau와 control bin이 겹칠 때의 leave-out 규칙
3. 희소 count의 smoothing 여부와 계수
4. primary directional statistic과 multiple-testing family
5. 같은 `[2,10^9]` 자료 재사용 및 record post-selection 한계

이 선택들을 P011 결과를 본 뒤 임의로 바꾸면 p-value가 해석 불가능해질 수 있으므로,
이번 16시간 queue에는 넣지 않는다. 설계 합의 후 P006 segmented sieve를 재사용하면
예상 CPU 시간은 수분–1시간, RAM 4 GB 미만, disk 2 GiB 미만이다.

## 권장 통계 설계

단순히 local 빈도를 넣은 새 binomial보다 **stratified conditional null**을 권장한다.
gap-start 위치를 사전 고정한 `log10(x)` bin으로 나눈 뒤 각 bin 안에서 해당 gap 크기의
총 발생 횟수를 고정한다. record 최초 발생 1개는 강제로 선택된 사건이므로 표본과 성공
수에서 모두 제거한다. 각 bin의 plateau 내부 재발 수는 hypergeometric component로 두고,
plateau가 여러 bin에 걸치면 component 합을 사용한다.

이 방식의 장점:

- 각 위치대의 gap 빈도를 그대로 보존해 P011의 global-stationary 오류를 줄임
- 확률 추정과 임의 smoothing이 primary 결과에 들어가지 않음
- plateau exposure와 바깥 control을 같은 bin 안에서 비교

남는 한계:

- bin 내부 exchangeability는 정리가 아니라 근사 가정
- observed record를 고정한 post-selection 진단
- 서로 겹치는 plateau·gap category의 의존성
- `[2,10^9]` 재사용 시 독립 검증이 아님

## 사용자와 합의할 세 질문

### Q1. 개발 범위와 독립 검증 범위

권장안: P012-A는 기존 `[2,10^9]`에서 P011과 직접 비교하고, 방법이 고정된 뒤 별도
P012-B에서 `[10^9,10^10]`을 holdout으로 계산한다.

- 장점: null 변경 효과와 범위 확대 효과를 섞지 않고, 나중 범위를 독립 확인에 사용
- 대안: 처음부터 `[2,10^10]`을 합치면 record는 늘지만 같은 자료에서 설계를 조정할
  위험이 커짐

### Q2. log-bin 사전 고정

권장안:

- primary: 폭 0.5 decade, 경계 `10^(k/2)`
- sensitivity 1: 같은 폭을 0.25 decade shift
- sensitivity 2: 폭 1.0 decade, 0.5 decade shift
- control exposure 또는 해당 gap occurrence가 너무 적으면 bin을 사후 합치지 않고
  `LOW_INFORMATION`으로 표시

폭을 결과에 맞춰 바꾸지 않고 세 설계를 모두 보고한다.

### Q3. primary 검정 목적

권장안: primary는 “local null이 전체 record family를 설명하는가”를 보는 two-sided
maximum-absolute standardized residual Monte Carlo로 두고, one-sided recurrence enrichment와
BH q-value는 secondary로 둔다. fixed seed `20260827`, 100,000 replicates를 사용한다.

- 이유: P011은 enrichment보다 큰 음수 residual을 보였으므로 enrichment만 보면 model
  부적합을 놓침
- 대안: 원래 질문인 enrichment를 primary로 유지할 수 있으나, 이 경우 deficiency는
  별도 진단으로만 남음

## 구현·실행 게이트

위 Q1–Q3에 대한 사용자 답을 받기 전에는 P012 코드를 구현하거나 actual 계산하지 않는다.
합의 뒤 계획서에 답을 고정하고 다음을 구현한다.

1. per-bin exposure와 gap count exact invariant
2. forced first record 제거 회귀시험
3. plateau가 bin 경계를 지나는 toy hypergeometric 정답
4. 고정 seed 재현성과 saved-artifact verifier
5. P011 stationary 결과와 같은 cohort의 직접 비교표
