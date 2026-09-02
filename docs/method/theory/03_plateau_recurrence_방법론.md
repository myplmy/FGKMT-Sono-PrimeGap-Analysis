# Maximal-gap plateau·recurrence 방법론

## 지위

`DEFINITION + EXACT_FINITE + EMPIRICAL`

## 연구 질문

어떤 gap 크기 `g_i`가 maximal record가 된 뒤 다음 더 큰 record가 나오기 전까지,
같은 크기의 consecutive-prime gap이 몇 번 더 나타나는지 센다. 이는 `G_end(x)`의
plateau 수명과 관련되지만 start-prime occurrence count이므로 경계를 구분한다.

## 통계량

- `N_i`: plateau 안에서 검사한 gap start 수
- `M_i`: record 첫 발생을 포함한 동일 gap 총 occurrence
- `C_i=M_i-1`: recurrence 수
- `Q_i=M_i/N_i`
- `R_i=C_i/(N_i-1)` (분모가 양수일 때)

마지막 plateau는 다음 record가 아직 없으면 right-censored로 분리한다.

## P006 finite 결과

`[2,10^9]` exact sieve에서 50,847,534 primes와 50,847,533 gaps를 처리했다.

- complete/censored plateau: 29/1
- complete 29개 중 recurrence가 관측된 record: 11개
- 최대 occurrence: gap 6의 `M=7`
- 마지막 complete gap 250: `N=2,478,966`, `M=2`, `C=1`
- gap 282는 상한에서 censored

저장 검증 issue 0이고 2026-08-26 figure 3개도 사용자 시각 QA PASS다.

## 해석 한계

- record 29개는 점근 추론에 작다.
- 큰 gap의 recurrence 0은 “영원히 재출현하지 않음”이 아니다.
- gap별 admissibility/singular-series 효과가 다르다.
- censoring과 사후 선택을 무시한 단순 추세검정은 사용하지 않는다.

## P011 stationary-null 진단

P011은 각 plateau를 제외한 `[2,10^9]` 전체 gap frequency로 binomial 기대값을 만들었다.
실행과 saved recomputation은 PASS했지만 primary 관측 재발 9에 기대 109.079로 큰
과대예측을 보였고, enrichment BH q는 모두 0.05보다 컸다. 이는 recurrence enrichment를
지지하지 않으며, global stationary rate가 위치에 따른 gap 분포 변화를 반영하지 못한다는
진단이다. 음수 residual을 새로운 repulsion theorem으로 해석하지 않는다.
P011 figure 두 개는 2026-08-27 사용자 시각 QA PASS다.

## 다음 가설·방법

`HYPOTHESIS P6-H1`: gap별 기대 occurrence를 단순 Poisson이 아닌 admissibility가 반영된
null model로 정규화하면 초기/후기 recurrence 차이의 일부가 설명된다.

P012는 범위를 무작정 `10^10`으로 늘리기보다 log-bin별 gap occurrence를 고정하는
stratified hypergeometric null을 사용한다. `[2,10^9]` 개발과 이후 holdout, primary
0.5-decade와 shifted sensitivity, two-sided family adequacy를 사용자와 사전 합의했다.
첫 actual의 zero-variance z plotting 실패는 통계 가설 문제가 아니므로 정의를 바꾸지 않고
미정의 z를 명시하는 r2로 교정했다. r2 primary는 관측 9 대 기대 8.5874, family p
0.21945이고 shifted sensitivity도 같은 방향이다. 이는 P011 stationary 과대예측을
nonstationarity가 설명한다는 진단과 일치하지만 LOW_INFORMATION 비율이 매우 높아 null의
정당성이나 recurrence 구조 부재를 증명하지 않는다.

사용자는 P012-A r2 figure의 축·범례·undefined-z marker에 문제가 없음을 확인했다. bin,
cohort, seed, 100,000회, primary·secondary와 LOW_INFORMATION 규칙은 machine-readable
contract로 동결했다.

P012-B는 `[10^9,10^10)`의 독립 gap-start stream을 사용한다. record start와 다음 record
start가 모두 holdout 안인 complete records `31–34`만 포함하고 양쪽 censored edge를 제외한다.
P006/P011 개발 table은 기대값 입력으로 사용하지 않았다. terminal·saved full recomputation·
독립 산술·독립 100,000회 Monte Carlo replay가 issue 0으로 PASS했다. 4개 plateau에서 관측
recurrence는 1, primary 기대는 0.497022, family p는 0.093939, 최소 enrichment BH q는
0.275957로 5% 기준 enrichment를 검출하지 못했다. 12/12 row가 LOW_INFORMATION이고 3개는
zero variance다. 따라서 holdout에서 극단적 모형 불일치는 검출되지 않았다고만 말하며, 유의하지
않은 결과를 모형 채택이나 구조 부재로 해석하지 않는다. 새 recurrence 모형·범위 확대는 P012-B를
소급 변경하지 않고 별도 P013 prospective 확장으로 분리했다. 사용자는 P012-B 두 figure의
시각 QA도 2026-08-28 PASS했다. P013-A/B는 `[10^10,10^11)`, `[10^11,10^12)` 범위·seed·
exact gap-start count와 stage별 alpha 0.025를 actual 전에 동결했으며, 결과를 본 뒤 pooling하지
않는다. 이는 정보량 증가와 모형의 유한범위 적합성을 보는 경험적 진단이다.

## P013 prospective 확장 결과

P013-A/B actual은 terminal·saved full recomputation·artifact hash·사용자 figure QA를 모두
PASS했다. 각각 4개와 9개의 complete plateau를 분석했지만 recurrence 관측은 모두 0이었다.
primary 기대값은 `0.0778288`, `0.0667972`이고 모든 통계행이 `LOW_INFORMATION`이었다.
P013-B에서는 primary 양의 분산 행도 1/9뿐이었다.

따라서 “더 큰 decade를 전수 계산하면 정보량이 자동 증가한다”는 전략은
`REJECTED_AS_STATED`다. 이는 recurrence 구조가 없다는 뜻이 아니라, 큰 x에서 exact
record-gap 자체의 비교 occurrence가 매우 희소하다는 유한 계산 결과다. P017은 P013의
segment-parallel 통계·checkpoint·fixed-seed inference가 serial과 exact 일치함을 확인했지만
새 과학 범위를 추가하지 않는다.

## P018 expected-information gate와 사후감사

P018은 가설검정 전에 계산가치를 판단한다. P0와 A는 관측 `exposure_equal_counts`, `C`, p/q/z를
gate에 사용하지 않고 population·target-gap total·plateau exposure margin만 사용했다.
P018-P0/A의 exact prime-count, 서로소 dual partition과 saved margin 재계산은 PASS했다.

P018-A는 `[10^12,1,968,188,556,462)`의 gap-start `34,570,543,382`개를 처리했으나 gap
582·588은 forced record 제거 후 conditioned count·expected·variance가 모두 0이었다.
primary 2/2와 sensitivity 5/5가 `LOW_INFORMATION`이므로 판정은
`EXPERIMENT_PASS / HOLD_PREFIX_INFORMATION / NO_AUTOMATIC_PROMOTION`이다.

사후감사에서 `gap_counts` margin은 target gap의 plateau/control 배치를 숨기지만, conditioned
count가 0인 경우 recurrence도 0임을 논리적으로 드러낸다는 점을 확인했다. 따라서 향후 명칭은
강한 `outcome-blind`보다 `margin-only / allocation-blinded`가 정확하다. 이 보정은 A의 HOLD를
바꾸지 않지만 A 범위를 미래 독립 holdout으로 재사용하지 못하게 한다. nested B를 연구하려면
독립 범위 또는 stopping rule을 포함한 formal conditional design이 먼저 필요하다.

현재 상태:

- stratified null이 P011 stationary 과대예측을 줄인다는 진단: `EMPIRICAL SUPPORTED`
- record-gap recurrence enrichment: `OPEN / NOT DETECTED`
- recurrence 구조 부재: 주장 불가
- P018-B·P013-C brute-force: `HOLD`
- 기존 artifact를 이용한 전체 증거 종합 시각화: P020 R2 `EXPERIMENT_PASS / SYNTHESIS_ONLY`, 2026-09-02 사용자 시각 QA PASS

상세 사후감사와 시각화 3안은
`docs/review/21_20260902_P018_recurrence_설계사후감사_전체시각화_타당성검토.md`를 따른다.

## P020 artifact 전수 종합 결과

P020은 성공 정본 8개를 새 prime 계산 없이 종합했다. 중복 제거 보고 처리량은
`72,178,455,399` gap-start이며 raw 721억 행이 저장됐다는 뜻은 아니다. P006의 complete
plateau 29개 중 11개에서 recurrence가 있고 recurrence 합은 20이었다. 같은 development
21개 row에서 P011 stationary 기대 합 109.0790은 P012-A stratified 기대 합 8.58738로
92.1274% 줄었다.

P012-B·P013-A/B의 primary 기대는 0.49702·0.07783·0.06680이고, 양의 분산 row 비율은
3/4·1/4·1/9로 줄었다. P018-P0/A는 forced record 제거 뒤 conditioned count와 분산이 0이다.
따라서 큰 처리량이 exact-record-gap recurrence의 정보량 증가를 보장하지 않는다는 판정이
전체 figure에서 일관된다. 이는 구조 부재 증명이 아니라 현재 질문의 구조적 희소성 진단이다.

정본:

- 계획: `test_plan/P020_recurrence_artifact_synthesis_visualization.md`
- 결과: `test_result/202609021151_P020_recurrence_artifact_synthesis_result_analysis.md`
- run: `test_result/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis`
- figure QA: 자동 QA와 2026-09-02 사용자 시각 QA PASS
