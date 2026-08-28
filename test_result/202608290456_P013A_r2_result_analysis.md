# P013-A r2 prospective recurrence extension 결과 분석

## 판정

`EXPERIMENT_PASS / TERMINAL_PASS / SAVED_FULL_RECOMPUTATION_PASS / ARTIFACT_HASH_PASS / ZERO_RECURRENCES_OBSERVED / RECURRENCE_ENRICHMENT_NOT_DETECTED / LOW_INFORMATION_LIMIT / MODEL_ACCEPTANCE_NOT_CLAIMED / FIGURE_AUTOMATIC_QA_PASS / USER_VISUAL_QA_PENDING / THEOREM_NOT_CLAIMED`

사용자 실행 `run_20260828T071601Z_p013a_recurrence_extension_1e11_r2`는 input preflight,
targeted tests, `[10^10,10^11)` 전체 분석, saved full recomputation과 terminal marker를 모두
PASS했다. manifest가 결박한 16개 artifact의 SHA-256도 전부 일치한다. 따라서 P013-A r2는
수치·저장·재현성 기준의 `EXPERIMENT_PASS`다.

P013-A r1에서 실패했던 10억 이상 hypergeometric category는 r2의 exact sequential symmetry
sampler로 처리됐다. 6개 large-parameter component가 이 경로를 사용했고, 필요한 최대 순차 draw는
3이었다. binomial approximation은 사용하지 않았다.

## 쉬운 말로 설명한 실험과 결과

이 실험은 maximal gap record가 생긴 뒤, 다음 record가 생기기 전까지 **같은 크기의 gap이 다시
몇 번 나타나는지**를 `[10^10,10^11)`라는 새로운 범위에서 세었다. P012에서 정한 bin·cohort·검정
규칙은 결과를 보기 전에 고정했고, P012-B 결과를 P013-A 추론에 섞지 않았다.

양쪽 경계가 범위 안에서 완전히 닫힌 record 구간은 4개였다. gap 382, 384, 394, 456은 각각
record가 된 최초 한 번만 나타났고, 같은 크기의 gap은 다음 record 전까지 한 번도 다시 나타나지
않았다. 따라서 관측 recurrence 합은 0이다.

동결된 primary 모형은 recurrence를 약 `0.07783`회 예상했다. 관측 0회는 이 작은 기대값과 매우
가깝고 family p는 `1.0`이다. recurrence가 특별히 많이 나타난다는 enrichment는 검출되지 않았다.

그러나 이것은 “반복 구조가 없다”는 증거가 아니다. 기대값 자체가 0.1회보다도 작고 12개 통계
행이 전부 `LOW_INFORMATION`이다. 즉 이번 decade에서는 record 크기의 gap이 너무 희귀해서,
재출현이 0회여도 모형이나 수론적 구조를 강하게 구별할 정보가 거의 없다.

## 범위·경계·plateau 결과

P013은 FGKMT 본체의 end-bounded `G(x)` 분석과 별도의 recurrence 통계축이다. 여기서는 gap의
start prime을 노출 위치로 세고, record start와 다음 record start가 모두 범위 안인 complete
plateau만 사용한다. 왼쪽 continuation과 오른쪽 censored plateau는 제외했다.

| record | start prime | gap | next record start | gap starts `N` | 같은 gap `M` | recurrence `C=M-1` |
|---:|---:|---:|---:|---:|---:|---:|
| 36 | 10,726,904,659 | 382 | 20,678,048,297 | 424,203,917 | 1 | 0 |
| 37 | 20,678,048,297 | 384 | 22,367,084,959 | 70,991,343 | 1 | 0 |
| 38 | 22,367,084,959 | 394 | 25,056,082,087 | 112,564,912 | 1 | 0 |
| 39 | 25,056,082,087 | 456 | 42,652,618,343 | 726,141,109 | 1 | 0 |

전체 range에서 gap start `3,663,002,302`개를 처리했고, 마지막 gap을 닫는 오른쪽 boundary prime
하나를 더 포함한 prime stream은 `3,663,002,303`개였다. 이 값들은 P013 contract의 exact prime-count
difference와 일치한다.

## Primary·sensitivity 통계

세 cohort는 이번 범위에서 같은 eligible row를 포함하므로 서로 독립인 세 번의 확인으로 세지
않는다. 아래 표는 `primary_start_ge_1000` cohort를 대표로 표시한다.

| scheme | 관측 recurrence | 기대 recurrence | 최대 `abs(z)` | family p | 최소 enrichment BH q | LOW_INFORMATION rows |
|---|---:|---:|---:|---:|---:|---:|
| width 0.5, shift 0 | 0 | 0.077829 | 0.290512 | 1.0 | 1.0 | 4/4 |
| width 0.5, shift 0.25 | 0 | 0.211698 | 0.375232 | 1.0 | 1.0 | 4/4 |
| width 1.0, shift 0.5 | 0 | 0.077829 | 0.290512 | 1.0 | 1.0 | 4/4 |

모든 scheme에서 사전 고정한 P013-A primary 기준 `0.025`보다 family p가 크고, 모든 one-sided
enrichment BH q도 1.0이다. variance가 0인 행의 z는 올바르게 미정의로 보존됐다.

## 앞선 recurrence 실험과의 기술적 비교

아래 비교는 흐름을 이해하기 위한 설명일 뿐, 결과를 본 뒤 세 범위를 pooling한 새 검정이 아니다.

| 실행 | 범위 | complete plateaus | primary 관측 | primary 기대 | family p | LOW_INFORMATION |
|---|---|---:|---:|---:|---:|---:|
| P012-A | `[2,10^9]` | 28 | 9 | 8.587376 | 0.219448 | 82/84 rows |
| P012-B | `[10^9,10^10)` | 4 | 1 | 0.497022 | 0.093939 | 12/12 rows |
| P013-A | `[10^10,10^11)` | 4 | 0 | 0.077829 | 1.0 | 12/12 rows |

P013-A에서는 range를 한 decade 늘렸는데도 complete plateau 수가 4개로 유지됐고, 새 record 크기
gap의 조건부 발생 자체가 더 희귀해졌다. 따라서 단순히 더 큰 decade로 이동하는 것이 recurrence
검정력을 자동으로 높이지 않는다는 실측 경고를 얻었다. P013-B가 더 많은 complete plateau를
제공하더라도 같은 정보 부족이 얼마나 줄어드는지는 별도 결과를 보기 전에는 알 수 없다.

## r1 오류 교정 검증

| 항목 | r2 확인값 |
|---|---|
| hypergeometric distribution | exact finite-population |
| backend | NumPy native + exact sequential symmetry |
| large-parameter components | 6 |
| maximum sequential draws | 3 |
| binomial approximation | 사용하지 않음 |
| sufficient-statistics checkpoint | 생성·hash 검증 PASS |
| saved verifier | 두 번째 full range recomputation PASS |

r1의 NumPy category-size 제한을 피하려고 근사분포로 바꾼 것이 아니다. 분포 대칭을 이용해 더
작은 쪽을 exact without-replacement 방식으로 뽑았으며, 저장 verifier가 전체 범위를 두 번째로
다시 계산했다.

## 실행·provenance

- run id: `20260828T071601Z_p013a_recurrence_extension_1e11_r2`
- 실행 시각(KST): 2026-08-28 16:16:01–17:29:17
- analysis elapsed: `2,226.930`초, 약 37분 7초
- 전체 runner wall time: 파일 시각 기준 약 1시간 13분 16초
- range: `[10^10,10^11)` gap starts
- selected records: `36,37,38,39`
- Monte Carlo: scheme·cohort별 100,000회, seed `20260828`
- two-stage primary alpha: P013-A `0.025`
- record source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- P012 contract SHA-256:
  `1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`
- P013 contract SHA-256:
  `153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf`
- analysis source SHA-256:
  `cace6b6448ae72fd4816c133d3adc75c4482ba2f83250cbffda3286822ca50c2`
- manifest SHA-256:
  `86da30eb0045704c7e955433906f58129d9b10a639451ba4b5827bd344a8dbdd`
- log SHA-256:
  `90d593369696d606c9e265a654c061233e20069f25f896ff2ccc00e99a4e56c5`
- CPU policy: 물리 4코어에 해당하는 논리 8프로세서 affinity `0xff`
- 실제 분석 parallelism: single Python stream
- GPU: 미사용
- theorem claimed: false

## 사후 artifact 감사

1. input preflight·15 targeted tests·analysis·saved full recomputation·terminal marker: 모두 PASS
2. FAIL·traceback·PowerShell exception: 0건
3. manifest에 기록된 artifact SHA-256: 16/16 일치
4. saved report의 manifest SHA-256과 직접 계산값: 일치
5. stage·schema·record indices·gap count·boundary prime count: 일치
6. 4개 plateau의 `N>=M>=1`, `C=M-1`: issue 0
7. 12개 row의 관측 recurrence: 모두 0
8. 12/12 row LOW_INFORMATION, primary·sensitivity family p와 BH q: 저장값 정합
9. exact large-hypergeometric metadata와 no-approximation flag: 정합

saved verifier 자체가 이미 두 번째 full prime sweep을 수행했으므로, P013-B가 실행 중인 이번
감사에서는 세 번째 full sweep을 추가로 돌리지 않았다. 대신 저장 artifact hash와 독립 산술
불변식을 읽기 전용으로 확인했다.

## Figure 자동 감사와 설명

1. `p013a_expected`: record gap 382·384·394·456별 관측 recurrence와 stratified conditional
   null의 기대값을 비교한다. 모든 관측은 0이며 기대값도 매우 작다.
2. `p013a_residuals`: variance가 양수인 행의 standardized residual을 표시한다. variance 0이라
   z가 정의되지 않는 점은 별도 marker로 구분해야 한다.

자동 검사:

- PNG 2개: 각각 1620x990, RGBA decode·nonblank·manifest hash PASS
- PDF 2개: header·EOF·manifest hash PASS
- 사용자 시각 QA: `PENDING`

## 연구 질문에 대한 답

1. **새 decade에서 recurrence enrichment가 검출됐는가?** 아니다. primary 관측 0,
   기대 0.077829, family p 1.0이다.
2. **r1 계산 오류는 정확한 방법으로 해결됐는가?** 그렇다. 근사 없이 exact sampler를 쓰고
   두 번째 full recomputation까지 PASS했다.
3. **범위 확대가 정보 부족을 해결했는가?** 아니다. 12/12 row가 LOW_INFORMATION이다.
4. **P012 conditional null이 검증됐는가?** 아니다. 작은 기대값에서 0회를 관측한 non-rejection은
   모형의 증명이 아니다.
5. **반복 구조가 없다고 말할 수 있는가?** 아니다. 검정력이 너무 낮다.

## 권장 후속 방향

1. 현재 실행 중인 P013-B를 중단하지 않고 terminal marker까지 기다린다.
2. P013-B 완료 후 A와 B를 사후 pooling하지 말고, 사전 고정한 stage-B alpha `0.025`로 독립
   판정한다.
3. P013-B에서도 LOW_INFORMATION이 거의 줄지 않으면, 더 큰 decade의 brute-force recurrence
   count보다 검정력·식별 가능성을 먼저 계산하는 새 방법론 설계를 우선한다.
4. P013-A figure 두 장은 사용자가 축·범례·marker·글자 겹침을 시각 확인한 뒤 QA를 닫는다.
