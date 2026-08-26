# P006 plateau·recurrence `[2,10^9]` 확대 결과 분석

## 최종 판정

`EXPERIMENT_PASS / NUMERIC_QA_PASS / USER_VISUAL_QA_PASS`

사용자 실행 `20260824T065339Z_p006_full_1000000000`은 `[2,10^9]`의 모든 consecutive prime gap 50,847,533개를 처리했고, exact `pi(10^9)`, 30개 maximal-gap records, 저장 CSV·그림 hash를 issue 0으로 검증했다. 수치·구조 검증은 PASS다.

새로 생성된 3개 PNG/PDF figure는 크기와 hash가 검증됐고, 사용자가
2026-08-26 각 그림에 문제가 없음을 확인했다. 따라서 visual QA도 `PASS`다.

사용자 확인 범위는 `p006_plateau_occurrences`, `p006_plateau_rates`,
`p006_plateau_lifetimes` 세 figure의 전체 시각 배치다. 이 확인은 수치 검증을
대체하지 않으며 기존 saved-artifact issue 0과 함께 최종 QA를 구성한다.

## 실행 증거

- log: `test_result/logs/run_20260824T065339Z_p006_full_1000000000.log`
- log SHA-256: `bdaacbea9cea0df331300c52ea4cc8ded5f336f312a923979f1f7d13e2350206`
- result: `test_result/run_20260824T065339Z_p006_full_1000000000`
- input record SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- prime count: 50,847,534, known exact value와 일치
- gap count: 50,847,533
- record count: 30
- complete plateaus: 29
- right-censored plateaus: 1
- core analysis: 약 2.70초
- saved-artifact verifier: PASS, issue 0
- GPU: 미사용

P006 pilot `[2,10^8]`과 겹치는 앞 24개 complete row도 값 불일치 0건으로 대조됐다.

## 주요 결과

`M`은 plateau의 start exposure에서 같은 크기의 gap이 나타난 총횟수, `C=M-1`은 최초 record를 뺀 재출현 횟수다.

- complete 29개 중 `C>0`인 record: 11개
- 지금까지 가장 많은 recurrence를 가진 record: gap 6, `M=7`
- 가장 긴 complete end-bounded plateau: gap 34, `ln(e_next/e_current)≈1.9522`
- 가장 짧은 complete plateau: gap 118, 약 `0.0056757`
- `[10^8,10^9]` 확대로 새로 닫힌 마지막 complete record:
  - gap 250
  - start prime 387,096,133
  - next record start 436,273,009
  - `N=2,478,966`, `M=2`, `C=1`
  - `Q=M/N≈8.06788×10^-7`
  - `R=C/(N-1)≈4.03394×10^-7`
- 마지막 gap 282 plateau는 상한 `10^9`에서 아직 끝나지 않아 right-censored:
  - `N=27,684,236`, `M=1`, `C=0`
  - `Q≈3.61216×10^-8`, `R=0`

right-censored gap 282는 관측 종료 뒤에 recurrence가 더 생길 수 있으므로 complete sample과 합치지 않는다.

## 각 figure가 설명하는 것

### `p006_plateau_occurrences`

각 maximal-gap plateau에서 동일 gap 크기가 총 몇 번 나왔는지 `M`, 최초를 제외하고 다시 나온 횟수 `C`를 비교한다. 값이 큰 초기 record 때문에 후기의 작은 차이가 눌릴 수 있으므로 점 하나의 높이를 곧바로 장기 법칙으로 해석하면 안 된다.

### `p006_plateau_rates`

단순 횟수 대신 관측기회로 나눈 `Q=M/N`과 `R=C/(N-1)`을 표시한다. plateau마다 소수 start를 관찰한 횟수가 다르다는 점을 보정한 경험적 빈도다. `R=0`은 관측 범위에서 재출현이 없었다는 뜻이지, 미래에도 절대 없다는 뜻은 아니다.

### `p006_plateau_lifetimes`

canonical end-bounded plateau 수명과 start-prime recurrence exposure 수명을 로그 비율로 나란히 보여 준다. 이는 gap이 `G_end(x)`로 유지되는 범위와 동일 gap occurrence를 세는 start 범위가 서로 다른 경계를 쓴다는 사실을 시각적으로 확인하기 위한 그림이다.

## 쉬운 해석

어떤 최대 gap이 기록을 세운 뒤 다음 더 큰 기록이 나오기까지 같은 크기의 gap이 몇 번 다시 나오는지 센 실험이다. 초기 작은 gap은 반복이 여러 번 있었지만 큰 gap으로 갈수록 관측된 재출현은 드물다. 다만 뒤쪽 plateau는 관측기회 자체와 표본 수가 작고 마지막 plateau는 끝나지 않았으므로, “큰 gap은 절대 재출현하지 않는다”는 결론은 낼 수 없다.

## 한계와 후속 분석

- record 29개는 점근 추론에 매우 작은 표본이다.
- 각 gap의 singular-series와 위치 효과를 아직 완전히 보정하지 않았다.
- 여러 통계량을 사후 탐색하므로 다중비교 위험이 있다.
- `10^20`까지 모든 소수를 재열거하는 방식은 자원상 부적절하다.
- 다음 통계 단계는 더 큰 무작정 열거보다 gap-specific 기대빈도와 exact/Monte-Carlo null model을 먼저 설계하는 편이 타당하다.
