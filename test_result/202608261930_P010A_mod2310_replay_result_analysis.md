# P010A modulus-2310 replay 결과 분석

## 판정

`EXPERIMENT_PASS / EXACT_REPLAY_PASS / UPPER_BOUND_UNCHANGED / SEARCH_ACCELERATION_NOT_PROVED`

사용자 실행 `run_20260826T100715Z_p010a_mod2310_replay`는 terminal PASS와 saved exact
verification PASS를 모두 만족했다. Codex가 결과 폴더를 다시 검증한 결과도 issue 0,
`exact_recomputed=true`였다.

## 핵심 결과

| 항목 | 값 |
|---|---:|
| modulus / states | 2310 / 480 |
| threshold | `gap >= 1856` |
| pairwise exact constraints | 415,223 |
| offset exact constraints | 415,223 |
| minimum integer slack | 0 |
| floating violation count | 0 |
| floating minimum slack | `-2.220446049250313e-16` |
| total start-bounded upper bound | 439,161,464,927,854,179 |
| corrected packing bound 대비 개선 | 9.4351468% |
| actual replay elapsed | 0.2652032초 |

floating 최소 slack의 작은 음수는 배정밀도 반올림 수준이며 tolerance를 넘는 위반은
0개다. certificate의 유효성 판정은 floating 값이 아니라 minimum integer slack 0과
두 독립 exact edge builder의 일치에 근거한다.

## 무엇이 확인됐는가

1. P007 certificate hash와 480개 potential이 고정 입력과 일치한다.
2. pairwise와 offset 방식이 같은 415,223개 계약과 같은 상한을 재현한다.
3. chunked oracle이 빠뜨린 제약 없이 같은 candidate를 검사한다.
4. 저장 artifact hash와 manifest binding을 다시 계산해도 문제가 없다.

## 무엇이 확인되지 않았는가

- 상한은 P007보다 1도 낮아지지 않았다.
- `gap>=1856`의 실제 위치 목록은 생성되지 않았다.
- Rank 85→86 exhaustive search가 빨라진다는 증명은 없다.
- modulus-30030 candidate, exact certificate, LP optimum은 아직 실행 결과가 없다.

따라서 이번 성공은 “다음 대규모 단계를 믿고 시험할 수 있는 검증 기반”의 성공이다.
알고리즘 개선 자체의 성공으로 해석하면 안 된다.

수치적 격차도 매우 크다. 위치가 이미 주어진다는 비현실적으로 유리한 가정에서도
50 GB에 후보당 1 byte를 쓴다면 500억 개만 저장할 수 있으므로 현재 상한은 약
878만 배 더 작아져야 한다. 후보당 16 byte면 필요한 축소율은 약 1억 4천만 배다.
실제로는 이 certificate가 위치를 주지 않으므로 이 계산은 단지 격차의 크기를 보이는
낙관적 하한이다. modulus 30→210→2310의 상한 개선도 각각 약 1.09%, 0.79% 수준으로
작아졌기 때문에 modulus 30030 하나만으로 수백만 배 개선될 근거는 현재 없다.

## provenance

- log: `test_result/logs/run_20260826T100715Z_p010a_mod2310_replay.log`
- log SHA-256: `1ac1a0e2f02c715120b60f98a525134b7c28d59d1269b0ad6037f4c8e51315d8`
- run: `test_result/run_20260826T100715Z_p010a_mod2310_replay`
- manifest SHA-256: `19c0f244afab7dce5b0274032c96370d50d00486b5dfdfa2f53f19e0bcfb8b6c`
- input certificate SHA-256: `725a2dcd4fd04b870a7f42edb85e6d9c029290fba861c592348a54d370c88ae5`
- summary SHA-256: `12cdf7ed6d022847b85f71f60df5f15406d836cf004dde356acba3e8297c0b45`
