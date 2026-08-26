# P011 recurrence stationary-null pilot 결과 분석

## 판정

`EXPERIMENT_PASS / ENRICHMENT_NOT_SUPPORTED / STATIONARY_NULL_INADEQUACY_INDICATED / THEOREM_CLAIM_NONE`

실행과 saved deterministic recomputation은 PASS, issue 0이다. 그러나 통계 결과는
“record gap이 plateau 안에서 예상보다 자주 재발한다”는 가설을 지지하지 않는다.
오히려 global stationary 빈도가 여러 초기 plateau의 기대 재발을 크게 과대예측했다.

## cohort 결과

| cohort | rows | 관측 재발 합 | null 기대 합 | total upper-tail p | max `abs(z)` MC p |
|---|---:|---:|---:|---:|---:|
| primary `start>=1000` | 21 | 9 | 109.0790 | 1.0 | 0.03610 |
| all eligible | 28 | 20 | 119.4319 | 1.0 | 0.03880 |
| sensitivity `start>=100000` | 15 | 5 | 43.7337 | 1.0 | 0.12069 |

total upper-tail p가 1이라는 것은 재발 과다가 아니라 재발 부족 방향임을 뜻한다. 가장
큰 absolute residual이 family-level 진단에서 작게 나온 것은 특정 plateau가 null과
잘 맞지 않는다는 뜻이지, 어떤 수론적 repulsion 정리가 증명됐다는 뜻이 아니다.

## 눈에 띄는 plateau

- gap 72, start 31,397: 관측 0, 기대 27.3348, `z=-5.2348`
- gap 114, start 492,113: 관측 0, 기대 13.4218, `z=-3.6640`
- gap 34, start 1,327: 관측 1, 기대 13.6557, `z=-3.4492`
- gap 36, start 9,551: 관측 2, 기대 14.9070, `z=-3.3821`
- enrichment 쪽 최저 BH q는 gap 6의 약 0.1052로 0.05보다 크다.

핵심 원인은 소수 gap 분포가 `x`에 따라 변하는데, P011이 `[2,10^9]` 전체 빈도를 한
plateau에 그대로 적용했다는 점이다. 뒤쪽의 훨씬 많은 gap 자료가 큰 gap의 global
빈도를 끌어올려 초기 plateau의 기대값을 과장한다. record를 본 뒤 선택한
post-selection과 같은 자료 재사용도 남아 있다.

## figure 설명

1. `p011_observed_vs_expected`: x축은 record gap, 파란 원은 실제 재발 수, 주황 사각형은
   stationary null 기대값이다. gap 72·114 등에서 주황선이 파란선보다 크게 솟는 모습이
   model 과대예측을 보여 준다.
2. `p011_standardized_residuals`: `(관측-기대)/표준편차`다. 0 아래 막대는 기대보다 적은
   재발, 위 막대는 기대보다 많은 재발이다. gap 72의 큰 음수 막대가 주된 부적합 신호다.

Codex의 파일 검사는 축·범례·데이터가 잘리지 않은 것으로 보였으나, 프로젝트 규약상
사용자 시각 QA 확인 전에는 최종 visual PASS로 기록하지 않는다.

## 다음 단계

같은 stationary null로 범위나 Monte Carlo 횟수만 늘리는 것은 권장하지 않는다.
P012에서 log-x bin 또는 위치가 비슷한 control window로 local rate를 추정하고, bin 폭과
shift를 결과 보기 전에 고정해야 한다. 이 단계도 경험적 진단이며 무한범위 정리가 아니다.

## provenance

- log: `test_result/logs/run_20260826T100938Z_p011_recurrence_null_pilot.log`
- log SHA-256: `f2fefa7c226fb7670de6d9e90a803fd2fccf9667a2cbddbe32c545c0face1842`
- run: `test_result/run_20260826T100938Z_p011_recurrence_null_pilot`
- manifest SHA-256: `3b7b982d6fbcada92331e5dbea05f28219c25ae6de97f8808685b0da67aa78a0`
- analysis SHA-256: `8b5da09c23f662bc729b2cdbeba15ea390912039ecd84ec0334cd6b43a253746`
- cohort summary SHA-256: `e7f720603c8fc70c76e1be4723921631056d1905e7bb8bab4e2dd03bcb597b67`
