# P010A G4 modulus-30030 cutting-plane 결과 분석

## 판정

`EXPERIMENT_PASS / EXACT_CERTIFICATE_PASS / STRICT_COUNT_BOUND_IMPROVEMENT / FULL_FLOATING_CONVERGENCE / SEARCH_ACCELERATION_NOT_PROVED`

사용자 실행 `run_20260826T155918Z_p010a_mod30030_cutting_plane_11h`은 terminal PASS와
saved exact verification PASS를 기록했다. Codex가 manifest·artifact hash·checkpoint와
best certificate의 35,224,647개 transition constraints를 다시 검사한 결과 issue 0,
minimum integer slack 0이었다.

## 핵심 결과

| 항목 | 값 |
|---|---:|
| baseline total upper bound | 439,161,464,927,854,179 |
| 새 exact total upper bound | 436,001,550,591,586,306 |
| 감소량 | 3,159,914,336,267,873 |
| 상대 감소율 | 0.7195336086% |
| 기존 비교용 `C=U/T` | 약 `1.102803437542279e15` |
| 새 비교용 `C=U/T` | 약 `1.094868396172136e15` |
| exact scanned constraints | 35,224,647 |
| exact violations | 0 |
| minimum integer slack | 0 |
| final working constraints | 20,123 (전체의 약 0.05713%) |
| LP solve 횟수 | 4 |
| core elapsed | 20.919초 |
| artifact bytes before manifest | 3,005,416 bytes |
| GPU | 미사용 |

엄밀한 결론은 start prime이 `[10^20,10^21)`에 있고 gap이 1856 이상인 consecutive-prime
gap 개수 `N`에 대해

\[
N\le 436001550591586306
\]

이라는 계산적 상한을 얻었다는 것이다. `C`는 크기 비교용 정규화값이고 정리의 핵심은
정수 상한 `U`다.

## iteration 진행

| iteration | working rows before solve | 새 위반 제약 | exact 보정 후 total bound | 당시 best |
|---:|---:|---:|---:|---:|
| 1 | 20,000 | 113 | 749,869,222,630,583,115 | baseline 유지 |
| 2 | 20,113 | 9 | 541,624,175,638,516,200 | baseline 유지 |
| 3 | 20,122 | 1 | 488,812,863,114,692,031 | baseline 유지 |
| 4 | 20,123 | 0 | 436,001,550,591,586,306 | 새 best |

네 번째 floating candidate는 전체 transition scan에서 새 위반 제약 0으로 수렴했다.
정수 denominator `10^15`로 반올림할 때 minimum slack이 `-17`이었고, 공통 `mu`를 정확히
17만큼 보정한 뒤 모든 정수 constraint의 minimum slack이 0이 됐다.

## 왜 11시간이 아니라 10분 이내에 끝났는가

11시간은 실행시간 목표가 아니라 runaway 방지용 hard cap이었다. baseline certificate에서
slack이 작은 20,000개를 잘 고른 덕분에 실제로 추가된 제약은 123개뿐이었다. HiGHS solve는
회당 약 1.26–2.55초였고 full transition streaming scan도 싸서 core가 약 21초에 종료됐다.

이 조기 종료는 계산을 덜 했다는 뜻이 아니다. 마지막 floating solution이 full scan을
통과했으므로 같은 floating LP를 더 반복할 이유가 사라진 정상 수렴이다. 다만 floating
solver의 전역 최적성을 exact하게 증명하는 별도 primal/lower certificate는 없으므로,
현재 엄밀한 주장은 저장된 **feasible exact upper-bound certificate**까지다.

## 알고리즘 개선과의 관계

이번 결과는 P010A count-upper-bound 연구에서는 실제 개선이다. 그러나 다음은 얻지 못했다.

- gap 후보의 절대 위치 목록
- 모든 실제 gap start를 포함하는 candidate-cover mapping
- block별 certified zero coverage
- baseline `prime-gap` 탐색보다 작은 total cost

따라서 P010B search acceleration은 계속 미증명이다. 상한이 약 0.72% 줄어도 여전히
`4.36×10^17` 수준이며, 전역 개수 상한만으로 어느 구간을 건너뛸지 알 수 없다.

## 독립 재검증

1. manifest의 모든 artifact SHA-256 재계산: mismatch 0
2. checkpoint 4개와 `iteration_history.json`: exact 일치
3. copied exact-lift manifest·certificate binding: 일치
4. best certificate parsing 후 35,224,647 constraints exact integer 재계산: PASS
5. summary·manifest의 strict-improvement flag와 정수 비교: 일치
6. direct search acceleration flag: false 유지

## provenance

- run: `test_result/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h`
- log: `test_result/logs/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h.log`
- log SHA-256: `3a96f2339f36069e85c6a57b242245905324edf4a018bceb6cf7c1f1cac7f6ed`
- manifest SHA-256: `6f68c8f4c5356f29b23aa48025699e02887b1d396645f04e6eee96aa535080e9`
- best certificate SHA-256: `22e345c0cae727fe60105d30a4cf99e2672c69bbf93815f02c5084c8d5805b65`
- runner SHA-256: `6dce831b8e29d72d4a0ef2ba62ff0120c679a6bb93c1789a37f8ec98affaa8c2`

## 다음 판정

1. 같은 modulus-30030 LP를 장시간 재실행하지 않는다.
2. 작은 exact rational tightening은 별도 수학·구현 검토 대상이지만 search acceleration과
   혼동하지 않는다.
3. 다음 큰 modulus 510510은 기존 full matrix가 32 GB를 크게 넘으므로 runner 작성 전
   memory-safe feasibility와 bounded calibration이 필요하다.
4. 실제 탐색 개선의 우선 blocker는 P010B absolute candidate-cover mapping이다.
