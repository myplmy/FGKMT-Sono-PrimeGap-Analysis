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
P006/P011 개발 table은 기대값 입력으로 사용하지 않는다. range sieve·contract/hash preflight·
toy tests는 PASS했으나 actual은 미실행이다. holdout에서도 LOW_INFORMATION이 높으면 유의하지
않은 결과를 구조 부재로 해석하지 않는다.
