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

## 다음 가설·방법

`HYPOTHESIS P6-H1`: gap별 기대 occurrence를 단순 Poisson이 아닌 admissibility가 반영된
null model로 정규화하면 초기/후기 recurrence 차이의 일부가 설명된다.

다음 단계는 범위를 무작정 `10^10`으로 늘리기보다 exact 또는 Monte-Carlo null model,
사전 고정 통계량, censoring-aware comparison을 먼저 설계하는 것이다.
