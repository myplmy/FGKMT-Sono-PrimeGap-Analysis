# P012-B holdout·P010B candidate-cover 구현 영향도 분석

## 판정

`P012B_IMPLEMENTATION_READY / P012A_CONTRACT_FROZEN / P010B_VERIFIER_READY / P010B_ACCELERATION_ALGORITHM_BLOCKED`

P012-A figure 사용자 QA가 PASS해 holdout 전 선결조건이 끝났다. P012-B는 개발 결과를 입력으로
쓰지 않는 별도 range sieve와 동결 contract로 구현한다. P010B는 coverage·soundness·비용을
판정하는 verifier는 구현할 수 있지만 absolute candidate generator가 없어 실제 가속
알고리즘은 아직 만들 수 없다.

## 영향도 축

| 축 | P012-B | P010B | 근거·대응 |
|---|---|---|---|
| 반복로그·end-bounded FGKMT | 영향 없음 | 영향 없음 | 둘 다 별도 recurrence/search 축 |
| start/end 의미론 | 영향 있음 | 영향 있음 | P012-B start exposure와 P010B half-open start universe를 명시 |
| dataset provenance | 영향 있음 | 향후 영향 큼 | P012-B record hash pin; P010B actual source는 아직 없음 |
| 큰 정수·정밀도 | 제한적 | 영향 큼 | P012-B int64; P010B actual은 `10^20` exact integer·PARI 필요 |
| 승인 경계 | 영향 있음 | 영향 있음 | P012-B actual 이중 gate; P010B는 toy만 실행 |
| 통계 재현성 | 영향 큼 | 영향 없음 | P012 contract hash·seed·100,000회 고정 |
| coverage·soundness | 영향 없음 | 핵심 영향 | 누락·잘못된 factor·비엄격 window를 verifier가 거부 |
| 자원 | 영향 있음 | 향후 영향 큼 | P012-B streaming 2회; P010B actual 50 GB cap |
| 정리/경험 구분 | 영향 있음 | 핵심 영향 | non-rejection과 toy coverage를 정리·가속으로 확대 금지 |
| 문서·테스트·handoff | 영향 있음 | 영향 있음 | 계획·METHODS·AGENTS·색인·새 handoff 갱신 |

## P012-B 구현 접근 비교

| 접근 | 정확성 | 재현성 | 비용 | 위험 | 판정 |
|---|---|---|---|---|---|
| `[2,10^10]` 전체 재분석 뒤 holdout filter | 가능 | 중간 | 가장 큼 | 개발 구간 혼입·경계 혼동 | 비권장 |
| `[10^9,10^10)` range-only sieve + canonical records | 높음 | 높음 | streaming 2회 | 새 range sieve 검증 필요 | **채택** |
| P006 `10^10` full을 먼저 만들고 P012-B에서 다시 sieve | 높음 | 높음 | 중간산출물·중복 pass | P006/P012 결합 복잡성 | 보류 |

채택안은 canonical record metadata로 complete plateau `31–34`만 고정하고, holdout 내부의
모든 gap start를 새로 생성한다. 왼쪽 continuation과 오른쪽 censored plateau는 사전 제외한다.
분석과 saved full recomputation이 각각 한 번씩 range를 훑는다.

## P010B 구현 접근 비교

| 접근 | 정확성 | 재현성 | 비용 | 위험 | 판정 |
|---|---|---|---|---|---|
| P010A count 상한을 곧바로 위치 후보로 해석 | 없음 | 없음 | 낮음 | 수학적으로 잘못된 가속 주장 | 폐기 |
| 즉시 `[10^20,10^21)` actual generator 작성 | 미확립 | 낮음 | 매우 큼 | false negative·순환 proof·자원 낭비 | BLOCKED |
| exact direct-universe verifier와 break-even gate부터 구현 | 높음(작은 우주) | 높음 | 낮음 | 아직 discovery 알고리즘 아님 | **채택** |

채택한 verifier는 모든 omitted start에 exact factor 또는 strict window-prime witness를 요구한다.
toy generator는 exhaustive truth를 사용하므로 가속 판정에서 자동 BLOCKED된다. actual로
확장하려면 compressed coverage 형식, PARI prime-certificate adapter, survivor adapter와
동일 baseline 비용 비교가 필요하다.

## 자원·중단 기준

- P012-B: RAM 8 GB·disk 2 GB·wall 4시간을 넘으면 중단하고 segment/log를 감사한다.
- P010B actual: RAM 32 GB·disk 50 GB·연속 168시간 한계를 넘는 설계는 채택하지 않는다.
- P010B direct verifier는 최대 1,000,000 integer starts와 작은 exact trial-prime에만 제한한다.
- 실제 `10^20` prime witness는 trial division으로 흉내 내지 않고 PARI certificate를 요구한다.

## 결론

P012-B actual runner까지 구현하는 것은 타당하다. P010B는 exact verification infrastructure를
구현하는 것이 타당하지만 실제 acceleration runner는 선결조건 미충족으로 보류해야 한다.
이 구분은 구현 부족이 아니라 false-negative 0과 총비용 개선을 증명하기 위한 필수 안전장치다.
