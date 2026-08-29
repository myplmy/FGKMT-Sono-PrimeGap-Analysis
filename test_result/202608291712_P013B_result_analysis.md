# P013-B prospective recurrence extension 결과 분석

## 판정

`EXPERIMENT_PASS / TERMINAL_PASS / SAVED_FULL_RECOMPUTATION_PASS / ARTIFACT_HASH_PASS / ZERO_RECURRENCES_OBSERVED / RECURRENCE_ENRICHMENT_NOT_DETECTED / LOW_INFORMATION_LIMIT / MODEL_ACCEPTANCE_NOT_CLAIMED / FIGURE_AUTOMATIC_QA_PASS / USER_VISUAL_QA_PENDING / THEOREM_NOT_CLAIMED`

사용자 실행 `run_20260828T090006Z_p013b_recurrence_extension_1e12`는 input preflight,
targeted tests, `[10^11,10^12)` 전체 분석, 두 번째 full-range recomputation과 terminal marker를
모두 PASS했다. manifest가 결박한 16개 artifact의 SHA-256도 전부 일치한다. 따라서 수치·저장·
재현성 기준으로 P013-B는 `EXPERIMENT_PASS`다. 그래프의 사용자 시각 QA만 별도로 남아 있다.

## 쉬운 말로 설명한 실험과 결과

이 실험은 maximal gap record가 생긴 뒤 다음 record가 생기기 전까지 **같은 크기의 gap이 다시
나타나는지**를 `100,000,000,000`부터 `1,000,000,000,000` 직전까지 세었다. P012에서 미리
고정한 bin·cohort·검정 규칙과 P013-B seed를 그대로 사용했고, P013-A/B 결과를 본 뒤 합쳐서 새
p-value를 만들지 않았다.

양쪽 경계가 범위 안에서 완전히 닫힌 record 구간은 9개였다. gap 468, 474, 486, 490, 500, 514,
516, 532, 534는 각각 record가 된 최초 한 번만 나타났고, 다음 record 전에 같은 gap은 한 번도
다시 나타나지 않았다. 따라서 관측 recurrence 합은 0이다.

동결된 primary 모형의 기대 recurrence 합은 약 `0.06680`회였다. 기대값 자체가 1회보다 훨씬
작기 때문에 0회를 본 것은 놀라운 결과가 아니며 family p는 `1.0`이다. recurrence enrichment는
검출되지 않았다.

그러나 이것은 “반복 구조가 없다”거나 “null 모형이 맞다”는 증거가 아니다. 27개 통계행이 모두
`LOW_INFORMATION`이고, primary에서 분산이 양수인 행도 gap 516의 한 행뿐이다. 즉 이번 범위는
앞선 범위보다 record plateau가 많아졌지만 구조를 구별할 통계 정보는 거의 늘지 않았다.

## 범위·경계·plateau 결과

P013은 FGKMT 본체의 end-bounded `G(x)`와 별도의 start-exposure recurrence 통계축이다. 여기서는
gap start를 위치로 세고, record start와 다음 record start가 모두 범위 안인 plateau만 사용한다.
왼쪽 continuation과 오른쪽 censored plateau는 제외했다.

| record | start prime | gap | next record start | gap starts `N` | 같은 gap `M` | recurrence `C=M-1` |
|---:|---:|---:|---:|---:|---:|---:|
| 41 | 127,976,334,671 | 468 | 182,226,896,239 | 2,105,850,785 | 1 | 0 |
| 42 | 182,226,896,239 | 474 | 241,160,624,143 | 2,260,175,195 | 1 | 0 |
| 43 | 241,160,624,143 | 486 | 297,501,075,799 | 2,140,802,260 | 1 | 0 |
| 44 | 297,501,075,799 | 490 | 303,371,455,241 | 222,126,859 | 1 | 0 |
| 45 | 303,371,455,241 | 500 | 304,599,508,537 | 46,446,764 | 1 | 0 |
| 46 | 304,599,508,537 | 514 | 416,608,695,821 | 4,209,805,106 | 1 | 0 |
| 47 | 416,608,695,821 | 516 | 461,690,510,011 | 1,681,688,125 | 1 | 0 |
| 48 | 461,690,510,011 | 532 | 614,487,453,523 | 5,657,528,302 | 1 | 0 |
| 49 | 614,487,453,523 | 534 | 738,832,927,927 | 4,564,989,747 | 1 | 0 |

전체 범위에서 gap start `33,489,857,205`개를 처리했다. 마지막 crossing gap을 닫는 오른쪽
boundary prime 하나를 포함한 prime stream은 `33,489,857,206`개다. 두 수는 동결된 P013
contract의 exact count와 일치한다. 9개 행의 `N >= M >= 1`, `C=M-1`도 모두 일치했다.

## Primary·sensitivity 통계

세 cohort는 이번 범위에서 같은 결과를 내므로 독립인 세 번의 확인으로 세지 않는다. 아래는
`primary_start_ge_1000` cohort의 대표 요약이다. 각 scheme에는 plateau 행 9개가 있으며,
zero-variance 행은 삭제하지 않고 `z` 미정의로 보존했다.

| scheme | 관측 recurrence | 기대 recurrence | 최대 `abs(z)` | family p | 최소 enrichment BH q | LOW_INFORMATION rows |
|---|---:|---:|---:|---:|---:|---:|
| width 0.5, shift 0 | 0 | 0.066797 | 0.267541 | 1.0 | 1.0 | 9/9 |
| width 0.5, shift 0.25 | 0 | 0.003211 | 0.056758 | 1.0 | 1.0 | 9/9 |
| width 1.0, shift 0.5 | 0 | 0.066797 | 0.267541 | 1.0 | 1.0 | 9/9 |

모든 family p는 사전 고정한 stage-B 기준 `0.025`보다 크고, 모든 one-sided enrichment BH q도
`1.0`이다. primary·width-1에서는 gap 516 한 행만 양의 분산을 가졌고, shifted scheme에서는
gap 500 한 행만 양의 분산을 가졌다. 나머지는 조건부 비교에 사용할 같은 gap 표본이 없어
분산이 0이었다.

## 앞선 recurrence 실험과의 기술적 비교

아래는 흐름을 이해하기 위한 설명이며, 결과를 본 뒤 A/B 또는 과거 범위를 pooling한 새 검정이
아니다.

| 실행 | 범위 | complete plateaus | primary 관측 | primary 기대 | family p | LOW_INFORMATION |
|---|---|---:|---:|---:|---:|---:|
| P012-A | `[2,10^9]` | 28 | 9 | 8.587376 | 0.219448 | 82/84 rows |
| P012-B | `[10^9,10^10)` | 4 | 1 | 0.497022 | 0.093939 | 12/12 rows |
| P013-A | `[10^10,10^11)` | 4 | 0 | 0.077829 | 1.0 | 12/12 rows |
| P013-B | `[10^11,10^12)` | 9 | 0 | 0.066797 | 1.0 | 27/27 rows |

P013-B는 P013-A보다 complete plateau가 4개에서 9개로 늘었지만 primary 기대값은 오히려
`0.077829`에서 `0.066797`로 낮아졌다. record plateau 수 자체보다 각 record-gap 크기가 같은
log-bin 안에서 실제로 몇 번 존재하는지가 정보량을 결정하기 때문이다. 이번 primary bin에서
강제된 첫 record를 제거한 뒤 비교 가능한 gap은 516 하나뿐이었다.

따라서 “더 큰 decade를 한 번 더 전수 계산하면 자동으로 검정력이 좋아진다”는 전략은 이번
실측으로 지지되지 않는다. 이것은 recurrence 구조의 부재가 아니라 현재 exact-gap recurrence
정의가 큰 수에서 매우 희소해진다는 계산상의 경고다.

### 후속 범위의 정보량 계획용 수치

아래는 정확한 P013 검정이 아니라 Poisson 희귀사건 근사에 의한 **계획용 직관**이다. 현재 primary
기대값 `lambda=0.066797`을 기준으로 하면 적어도 한 번을 볼 확률이 약 50%가 되려면 기대 정보가
약 `10.4배`, 95%가 되려면 약 `44.8배` 필요하다. 기대 횟수 5를 단순 목표로 잡으면 약 `74.9배`다.
실제 P013은 stratified hypergeometric family이므로 이 배수를 검정 결과로 사용하면 안 되지만,
P013-C를 만들기 전에 예상 정보량이 최소 한 자릿수 배 이상 증가하는지 사전 계산해야 한다는
의사결정 기준으로는 유용하다.

## exact sampler·실행 자원

| 항목 | 확인값 |
|---|---|
| hypergeometric distribution | exact finite-population |
| backend | exact sequential symmetry |
| component count | 31 |
| large-parameter components | 31 |
| maximum sequential draws | 1 |
| binomial approximation | 사용하지 않음 |
| process affinity | `0xff`, 물리 4코어에 대응하는 논리 8프로세서 |
| 실제 sieve parallelism | single Python stream |
| GPU | 미사용 |

31개 component가 모두 NumPy의 큰 category 제한을 넘었지만, 대칭성을 이용한 exact sampler의
최대 순차 draw는 1이었다. P013-A r1 문제를 근사분포로 우회하지 않았다는 뜻이다. 다만 소수 체
자체는 단일 Python stream이므로 affinity 8개가 곧 8-way sieve 병렬화를 뜻하지 않는다.

## 실행·provenance

- run id: `20260828T090006Z_p013b_recurrence_extension_1e12`
- 실행 시각(KST): 2026-08-28 18:00:06–2026-08-29 17:02:32
- analysis elapsed: `40,073.308`초, 약 11시간 7분 53초
- saved full recomputation: 파일 시각 기준 약 11시간 54분
- 전체 runner wall time: 파일 시각 기준 약 23시간 2분 26초
- range: `[10^11,10^12)` gap starts
- selected records: `41–49`
- Monte Carlo: scheme·cohort별 100,000회, seed `20260829`
- two-stage primary alpha: P013-B `0.025`
- record source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- P012 contract SHA-256:
  `1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`
- P013 contract SHA-256:
  `153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf`
- analysis source SHA-256:
  `cace6b6448ae72fd4816c133d3adc75c4482ba2f83250cbffda3286822ca50c2`
- checkpoint canonical SHA-256:
  `1b2bdf2a16b06f0a44b342e224a4f635600d45dff2f20e10d9b433a30cae3d64`
- manifest SHA-256:
  `a4272808f4486bbfba04e6255b1693420f46392f28b2c9567fddd82076c6d760`
- log SHA-256:
  `f43be4e87aacfead90cd90d11205fcdc4d5d7e8521bf12ab78a40986c68da84e`
- theorem claimed: false

실행 완료 진입점 보존:

- `test_done/run_P013B_recurrence_extension_1e12-20260828T090006Z-done.bat`
  SHA-256 `2af902c78549c0b5c97064246fdc15e97ff889b6cd581ddadeef6aaf935f4486`
- `test_done/run_p013b_recurrence_extension_1e12-20260828T090006Z-done.ps1`
  SHA-256 `98ceb288134440d7a4b6e9a5dc372b03ee2b0e9d107fe6291d62b42ca2b90adf`
- 공통 `scripts/runners/run_p013_extension.ps1`은 재사용 모듈이므로 이관하지 않았다.

## 사후 artifact 감사

1. preflight·targeted tests·analysis·saved full recomputation·terminal marker: 모두 PASS
2. FAIL·traceback·PowerShell exception marker: 0건
3. manifest가 기록한 artifact SHA-256: 16/16 일치
4. saved report의 manifest SHA-256과 직접 계산값: 일치
5. checkpoint canonical payload와 analysis 결속 hash: 일치
6. stage·schema·record indices·gap count·boundary prime count: 일치
7. 9개 plateau의 `N>=M>=1`, `C=M-1`: issue 0
8. 27개 통계행의 관측 recurrence 0, 27/27 LOW_INFORMATION: 저장값 정합
9. exact large-hypergeometric metadata와 no-approximation flag: 정합

saved verifier가 이미 두 번째 full prime sweep을 수행했으므로 이번 감사에서 세 번째 full sweep은
실행하지 않았다. 저장 artifact 해시, checkpoint canonical hash와 독립 산술 불변식을 읽기
전용으로 확인했다.

## Figure 자동 감사와 설명

1. `p013b_expected`: record gap별 관측 recurrence와 동결된 stratified expectation을 비교한다.
   모든 관측은 0이고, gap 516에서만 primary 기대값 약 `0.0668`이 보인다.
2. `p013b_residuals`: 분산이 양수인 gap 516의 standardized residual `-0.2675`를 막대로 표시한다.
   나머지 gap의 `x` 표시는 `z=0`이 아니라 variance 0으로 `z`가 정의되지 않음을 뜻한다.

자동 검사:

- PNG 2개: 각각 1620x990, RGBA decode·nonblank·manifest hash PASS
- PDF 2개: `%PDF-1.4` header·`%%EOF`·manifest hash PASS
- 사용자 시각 QA: `PENDING`

## 연구 질문에 대한 답

1. **새 decade에서 recurrence enrichment가 검출됐는가?** 아니다. primary 관측 0, 기대
   0.066797, family p 1.0이다.
2. **범위 확대가 정보 부족을 해결했는가?** 아니다. plateau는 9개로 늘었지만 27/27 행이
   LOW_INFORMATION이다.
3. **P012 conditional null이 검증됐는가?** 아니다. 매우 작은 기대값에서 0회를 관측한
   non-rejection은 모형의 증명이 아니다.
4. **반복 구조가 없다고 말할 수 있는가?** 아니다. exact-gap recurrence 자체가 희소해 검정력이
   너무 낮다.
5. **바로 P013-C를 실행하는 것이 타당한가?** 현재는 아니다. 먼저 다음 범위의 예상 정보량과
   최소 검출가능 효과를 계산해 유의미한 증가 가능성을 보여야 한다.

## 권장 후속 방향

1. P013-B figure 두 장의 축·범례·marker·글자 겹침을 사용자가 시각 확인한다.
2. 이미 준비된 P017을 실행해 segment 병렬화의 exact equality와 실제 wall-time 개선을
   engineering 관점에서 검증한다. 이는 P013-B 과학 결과를 바꾸지 않는다.
3. P013-C보다 먼저 `expected-information/power preflight`를 설계한다. 최소한 현재 대비 한
   자릿수 배 이상의 기대 정보 증가가 보이지 않으면 대규모 full-prime sweep을 보류한다.
4. exact gap equality 대신 gap-size neighborhood·모듈러 계층 같은 대안은 새로운 가설과
   다중검정 계약을 사전에 고정한 별도 실험으로만 검토한다.
