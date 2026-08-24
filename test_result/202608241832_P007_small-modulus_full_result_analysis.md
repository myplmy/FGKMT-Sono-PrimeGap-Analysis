# P007 small-modulus full certificate 비교 결과 분석

## 최종 판정

`EXPERIMENT_PASS / BOUND_IMPROVES_MODESTLY / DIRECT_ACCELERATION_NOT_PROVED`

사용자 실행 `20260824T090010Z_p007_full`은 modulus 30, 210, 2310에서 LP 후보를 찾고, 유리화한 certificate를 모든 허용 transition에 대해 exact integer arithmetic으로 재검증했다. 세 certificate 모두 minimum slack 0, saved-artifact verification PASS였고 상한은 modulus 증가에 따라 단조 감소했다.

그러나 30→2310의 개선은 전역 packing bound 대비 약 7.70%→9.44% 수준이다. 상한은 여전히 `4.39×10^17`이고 위치 정보를 주지 않으므로 직접 탐색 가속은 증명되지 않았다.

## 실행 증거

- log: `test_result/logs/run_20260824T090010Z_p007_full.log`
- log SHA-256: `f5a019ce0fe9a0ef1da30fe4635af44600f486ffe9a530640b72f115d357f13b`
- result: `test_result/run_20260824T090010Z_p007_full`
- exact certificates: 3
- actual prime enumeration/search: 미수행
- GPU: 미사용
- saved verification: PASS
- direct search acceleration proved: false

| modulus | states | constraints | discovery time | 저장된 total upper bound | packing 대비 개선 |
|---:|---:|---:|---:|---:|---:|
| 30 | 8 | 128 | 0.0058초 | 447,557,793,758,307,014 | 7.7036% |
| 210 | 48 | 4,608 | 0.0162초 | 442,672,596,769,194,837 | 8.7111% |
| 2310 | 480 | 415,223 | 3.9541초 | 439,161,464,927,854,179 | 9.4351% |

인접 modulus 개선은 다음과 같다.

- 30→210: 4,885,196,989,112,177 감소, 약 1.0915%
- 210→2310: 3,511,131,841,340,658 감소, 약 0.7932%

즉 상태·제약 수는 크게 늘지만 추가 개선율은 오히려 작아졌다. 세 점만으로 점근적인 수확 체감을 증명할 수는 없지만, dense modulus 확대를 곧바로 실행할 근거는 약하다.

## 정수 반올림 보정

저장된 P007 full certificate는 이전 구현과의 비교를 위해 안전한 `ceil(q)+1 crossing` 상한을 기록했다. 정수 개수에는 `floor(q)`를 적용할 수 있으므로 더 날카로운 total upper bound는 각각 저장값보다 1 작다.

| modulus | 저장된 안전 total | tight integer total |
|---:|---:|---:|
| 30 | 447,557,793,758,307,014 | 447,557,793,758,307,013 |
| 210 | 442,672,596,769,194,837 | 442,672,596,769,194,836 |
| 2310 | 439,161,464,927,854,179 | 439,161,464,927,854,178 |

기존 값도 참인 상한이므로 PASS는 유지한다. 기존 run directory는 provenance 때문에 수정하지 않고, P008이 tight `floor`와 historic `ceil`을 함께 저장한다.

## 더 큰 modulus의 자원 판정

modulus 30030은 solve하지 않고 구조만 추정했다.

- states: 5,760
- constraints: 35,224,647
- COO construction lower bound: 약 3.41 GiB
- conservative working estimate: 약 20.47 GiB
- estimate는 peak-memory 보장이 아님
- current guard: solve 금지

20.47 GiB가 32 GB보다 작다는 이유만으로 안전하다고 볼 수 없다. Python 객체·solver 내부복사·presolve peak가 포함되지 않을 수 있기 때문이다. 기존 dense formulation으로 modulus 510510까지 가면 추정 constraints가 약 85.2억, COO lower bound가 약 825.7 GiB이므로 32 GB 제한에서 불가능하다.

따라서 30030은 dense full solve가 아니라 separation oracle 또는 cutting-plane으로 현재 해를 위반하는 전이만 점진적으로 추가하는 memory-safe 설계가 먼저 필요하다.

## 쉬운 해석

modulus를 키울수록 “큰 gap 개수의 천장”은 조금씩 내려갔다. 하지만 천장 높이가 약 43.9경에서 여전히 너무 높고, 큰 gap이 어디에 있는지도 알려주지 않는다. 천장을 1% 더 낮추는 것과 탐색 후보를 1% 줄이는 것은 같은 일이 아니다.

따라서 P007은 수학 인증서 비교로는 성공했지만 검색 알고리즘 개선으로는 아직 출발점이다. 실제 가속에는 block zero 또는 누락 없는 candidate cover와 `prime-gap` 작업단위의 mapping 증명이 추가로 필요하다.

## 다음 게이트

1. modulus 30030 dense solve는 실행하지 않는다.
2. memory-safe constraint generation의 toy/작은 modulus 동등성 검증을 먼저 한다.
3. 얻은 새 상한이 block zero/candidate survivor 수를 얼마나 줄이는지 break-even으로 평가한다.
4. 위치를 주지 않는 전역 상한 개선만 반복되면 P007 계열을 탐색 가속 후보로 승격하지 않는다.

