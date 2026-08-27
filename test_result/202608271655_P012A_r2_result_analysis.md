# P012-A r2 stratified conditional null 결과 분석

## 판정

`EXPERIMENT_PASS / SAVED_FULL_RECOMPUTATION_PASS / P011_STATIONARY_OVERPREDICTION_LARGELY_REMOVED / RECURRENCE_ENRICHMENT_NOT_SUPPORTED / LOW_INFORMATION_LIMIT / MODEL_ACCEPTANCE_NOT_CLAIMED / USER_VISUAL_QA_PASS / CONTRACT_FROZEN`

사용자 실행 `run_20260827T054007Z_p012a_stratified_null_development_r2`는 terminal PASS,
manifest artifact hash PASS, saved deterministic full recomputation PASS를 모두 기록했다.
Codex가 저장 component에서 기대값·분산·z·100,000회 Monte Carlo row p·BH q·9개 family
max-abs-z p를 독립 재계산한 결과 issue 0이었다. 따라서 수치·저장 산출물 기준으로
P012-A r2는 `EXPERIMENT_PASS`다.

사용자는 2026-08-27 두 figure의 축·선·막대·범례와 undefined-z marker를 확인하고 문제가
없다고 회신했다. 따라서 자동 검사와 사용자 시각 QA가 모두 PASS다.

## 연구 질문에 대한 답

P011의 `[2,10^9]` 전역 stationary gap 빈도는 위치가 다른 plateau를 같은 비율로 비교해
초기 구간의 large-gap recurrence를 크게 과대예측했다. 사전 고정한 P012 log-x stratified
conditional null로 바꾸면 primary `start>=1000`에서 다음처럼 변한다.

| 모형 | 분석 row | 관측 recurrence | 기대 recurrence | 관측/기대 | family max-abs-z p |
|---|---:|---:|---:|---:|---:|
| P011 global stationary | 21 | 9 | 109.0790 | 0.0825 | 0.03610 |
| P012 primary width 0.5, shift 0 | 14 z-defined | 9 | 8.5874 | 1.0481 | 0.21945 |

P012 기대값은 P011보다 약 92.13% 작고 관측 9회에 매우 가깝다. P011에서 보인
family-level 부적합 신호 `p≈0.036`도 P012에서는 `p≈0.219`로 사라졌다. 이는 기존의 큰
음수 residual 상당 부분이 recurrence 자체의 특이한 회피보다 **gap 빈도의 위치
비정상성(nonstationarity)**을 무시해서 생겼다는 해석과 일치한다.

두 family의 row 수는 같지 않다. P012는 사전 규칙대로 conditional variance 0인 row를
z-family에서 제외한다. 해당 row들의 관측·기대 recurrence는 모두 0이므로 total에는 영향을
주지 않지만, p값을 P011과 완전히 동일한 검정으로 취급해서는 안 된다.

## 사전 고정 primary와 sensitivity

primary cohort `start>=1000`의 세 bin scheme 결과다.

| scheme | z-defined rows | 관측 | 기대 | max `abs(z)` | family p |
|---|---:|---:|---:|---:|---:|
| width 0.5, shift 0 | 14 | 9 | 8.5874 | 2.6212 | 0.21945 |
| width 0.5, shift 0.25 | 11 | 9 | 8.7669 | 1.5857 | 0.71354 |
| width 1.0, shift 0.5 | 15 | 9 | 8.3237 | 1.8418 | 0.49280 |

세 scheme 모두 기대 recurrence가 8.32–8.77로 관측 9에 가깝고 family p가 0.05보다 크다.
따라서 결과는 bin 경계를 약간 옮기거나 폭을 넓혀도 “P011의 전역 과대예측이
stratification 뒤 크게 줄어든다”는 방향에서 안정적이다.

다른 사전 cohort도 같은 방향이다.

| cohort·primary scheme | 관측 | P011 기대 | P012 기대 | P012 family p |
|---|---:|---:|---:|---:|
| all eligible | 20 | 119.4319 | 17.4925 | 0.22539 |
| start>=100000 sensitivity | 5 | 43.7337 | 2.8374 | 0.26671 |

이는 P012 null이 참임을 받아들였다는 뜻이 아니라, 이 유한 자료와 사전 통계로는
family-level departure를 검출하지 못했다는 뜻이다.

## secondary enrichment 결과

가장 큰 양의 P012 residual은 gap 154였다.

```text
start prime = 4,652,353
observed recurrence = 2
P012 expected recurrence = 0.667777
z = 1.99750
one-sided Monte Carlo p = 0.111569
two-sided Monte Carlo p = 0.111569
BH q = 1.0
```

모든 bin scheme에서 최소 enrichment BH q가 `1.0`이었다. 따라서 “record gap이 같은
plateau에서 조건부 기대보다 더 자주 반복된다”는 secondary 가설을 지지하는 결과는 없다.

가장 큰 절대 primary residual은 gap 34의 `z=-2.62116`이지만 row two-sided p는 약
0.1151이고 family p는 0.21945다. 개별 눈에 띄는 행을 family 보정 없이 발견으로 해석하지
않는다.

## zero variance와 LOW_INFORMATION

primary cohort에서 gap 44, 72, 112, 114, 118, 180, 220의 7개 row는 최초 record 제거 뒤
같은 gap occurrence가 해당 exposure bin에 남지 않아 expected=variance=observed=0이다.
따라서 z는 0이 아니라 `None`이다. r2는 이를 저장값과 그림 marker에서 그대로 보존했다.

정보 부족은 이 실험의 가장 큰 한계다.

| scheme | 전체 modeled rows | variance 0 rows | LOW_INFORMATION row |
|---|---:|---:|---:|
| width 0.5, shift 0 | 28 | 9 | 28 |
| width 0.5, shift 0.25 | 28 | 11 | 28 |
| width 1.0, shift 0.5 | 28 | 7 | 26 |

`LOW_INFORMATION`은 component의 보정 후 같은-gap 수가 5 미만이거나 control exposure가
1,000 미만임을 뜻하며 사전 규칙상 test membership을 바꾸지 않는다. 거의 모든 row가 이
표시를 가지므로 P012의 non-rejection을 강한 “무효과 증거” 또는 모형의 정당성으로 해석할
수 없다. local conditioning이 P011의 편향을 줄인 대신 rare-gap 검정력을 크게 낮춘 면도
있다.

## 독립 재검증

1. manifest에 기록된 11개 artifact SHA-256 전수 대조: mismatch 0
2. saved report의 manifest SHA-256 직접 대조: 일치
3. P006/P011 입력 사본 hash와 계획 pin: 일치
4. 실행 runner·analysis source·CLI source hash와 log: 일치
5. 128 components에서 84 rows의 expected·variance·observed·z 재계산: issue 0
6. 각 row의 100,000회 hypergeometric MC p를 seed 규칙으로 독립 재생: issue 0
7. scheme별 BH q 재계산: issue 0
8. 9개 cohort family max-abs-z MC p 재계산: issue 0
9. r1과 r2의 `analysis.json`, components CSV, statistics CSV hash: 모두 동일

9번은 plotting 교정이 실제 통계 결과를 변경하지 않았음을 보여 준다.

## 실행·provenance

- analysis limit: `10^9`
- prime count: `50,847,534`
- gap count: `50,847,533`
- modeled rows: 84
- component rows: 128
- Monte Carlo: 100,000회, seed `20260827`
- analysis elapsed: 87.234초
- GPU: 미사용
- holdout `[10^9,10^10]`: untouched
- theorem claimed: false
- log:
  `test_result/logs/run_20260827T054007Z_p012a_stratified_null_development_r2.log`
- log SHA-256:
  `dea10dac2982fb851c532d7b621489d85166bc3e13e9a6274167fe64c0dd76ad`
- run:
  `test_result/run_20260827T054007Z_p012a_stratified_null_development_r2`
- manifest SHA-256:
  `723bd82778c92b7ebe3e9f614fd7411e86f5619d3043ed292ddac93fa6966c09`

## figure 자동 감사와 설명

1. `p012_expected_comparison`: 관측 recurrence, P011 stationary 기대, P012 stratified 기대를
   같은 gap별로 비교한다. P012 기대가 관측에 훨씬 가까워졌는지 보여 주는 그림이다.
2. `p012_residual_comparison`: P011과 P012 standardized residual을 비교한다. 주황 x는
   P012 z=0이 아니라 conditional variance 0으로 z가 미정의인 위치다.

자동 검사:

- expected PNG: 1800x990, decode·nonblank PASS
- residual PNG: 1980x990, decode·nonblank PASS
- PDF 2개: header·EOF PASS
- figure 4개 manifest hash: 모두 일치

사용자는 2026-08-27 축·선·막대·x marker·범례에 문제가 없음을 확인했다. 주황 x가 z=0이
아닌 conditional variance 0의 미정의 z라는 표현도 승인했다.

## 결론과 다음 단계

P012-A는 “P011의 큰 음수 신호가 위치 비정상성을 무시한 null에서 주로 발생했다”는 진단을
강하게 뒷받침한다. 반면 recurrence enrichment나 새로운 수론적 구조는 검출하지 못했다.
저정보 비율이 매우 높으므로 이것은 구조 부재의 증명이 아니다.

다음 순서는 다음과 같다.

1. 완료한 figure QA와 primary·sensitivity 계약을 결과 뒤 변경하지 않고 동결한다.
2. 동결 계약 SHA-256
   `1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`를
   P012-B runner가 확인한다.
3. 같은 계약으로 `[10^9,10^10)` P012-B actual을 사용자가 별도 실행한다.
4. P012-B에서도 저정보율·zero-variance율을 반드시 함께 보고한다.
5. holdout에서도 검정력이 부족하면 P012를 억지로 확장하지 않고 새 번호의 별도 모형을
   개발·검증한다.
