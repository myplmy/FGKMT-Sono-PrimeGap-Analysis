# P019 — serial 정답표 없는 범위의 parallel dual-partition exact cross-check

## 1. 상태와 승인 경계

`DESIGN_APPROVED / IMPLEMENTED_TOY / ACTUAL_NOT_AUTHORIZED`

사용자는 P017-B처럼 새 중간범위의 serial 정답표가 없을 때도 병렬 계산할 수 있는 방법을 검토하고,
가능하면 구현·toy 검증하도록 승인했다. P019는 검증 구조의 toy revision이다. 새 실제 prime range
sweep, P013-C 또는 production runner 실행은 별도 사용자 승인이 필요하다.

## 2. 목적

P017-B는 먼저 serial full pass를 만들고 그 뒤 parallel full pass를 수행했기 때문에 정확성 비교는
강하지만 wall time 대부분을 serial 계산이 차지했다. P019의 질문은 다음과 같다.

> P017에서 serial과 exact equality를 통과한 병렬 engine을 새 범위에서 두 개의 서로 다른
> segment partition으로 전수 실행하고, 두 결과와 독립 endpoint prime count를 함께 비교하면
> serial full pass 없이도 현재 saved recomputation에 준하는 계산 검증을 할 수 있는가?

## 3. 고정 검증 구조

1. primary: 8 worker, `N`개 segment로 전체 `[L,U)` gap start를 계산
2. verifier: 8 worker, `M`개 segment로 같은 전체 범위를 다시 계산
3. `N != M`, `gcd(N,M)=1`로 내부 경계를 다르게 함
4. 각 pass가 모든 인접 boundary prime, worker 참여, exact integer merge를 자체 검증
5. populations, gap counts, exposure, equal exposure, prime/gap count 전체 exact equality
6. 별도 exact prime-count 절차에서 얻은
   `pi(U-1)-pi(L-1)`와 gap-start count 일치
7. 두 pass가 모두 끝난 뒤에만 downstream checkpoint·inference 생성

production 후보는 primary 64 segments, verifier 73 segments다. 이는 64와 73이 서로소라 내부
분할 경계가 거의 겹치지 않으면서 worker 8개에 충분한 task를 준다. 범위가 작으면 segment 수를
줄이되 위 조건을 유지한다.

## 4. 정확성의 의미와 남는 한계

이 방식은 샘플링하지 않는다. 두 pass 모두 전체 prime/gap을 다시 읽고 정수 통계를 계산하므로
`work_items_omitted=false`, `precision_reduced=false`다. partition 경계, crossing gap, merge,
worker 누락, 비결정적 실행 오류에는 강한 교차검사다.

그러나 두 pass가 `iter_prime_chunks_range`와 `accumulate_bin_counts`를 공유하므로 같은 코드의
공통 오류는 둘 다 똑같이 재현할 수 있다. 따라서 이를 “완전히 독립적인 수학적 oracle”이나
증명이라고 부르지 않는다. 다음 세 조건이 production 전 필수다.

- P017 실제 serial/parallel calibration과 source hash provenance 유지
- endpoint prime count를 enumeration과 다른 exact 알고리즘으로 확인
- source가 바뀌면 P017 calibration 또는 동등한 serial 비교를 다시 수행

## 5. 시간 영향

P017-B 같은 범위에서 serial은 12,598.410초, parallel은 준비 포함 2,866.160초였다. 같은 속도가
두 번째 partition에서도 유지된다는 가정 아래 dual-parallel은 약 5,732초(1시간 35분 32초)다.
P017-B의 serial+parallel 15,464.8초보다 약 2.70배 짧다. 이는 실측에서 계산한 계획 추정이며
새 범위의 보장값은 아니다.

한 번의 parallel 결과만 저장하는 안은 더 빠르지만 verification이 약해져 채택하지 않는다.

## 6. toy 구현

- `source/parallel_dual_partition.py`
- `tests/test_parallel_dual_partition.py`

toy 범위 `[100,200)`에서 다음을 검사한다.

- primary 8 segments와 verifier 11 segments, worker 4
- 두 parallel exact core와 별도 toy serial core의 일치
- 정확한 gap-start count 21 일치
- 두 pass progress 총 19개·pass label 보존
- 동일/non-coprime partition 사전 거부
- 잘못된 독립 count가 주어지면 결과 수용 거부

## 7. actual 전 추가 gate

- 새 범위와 plateau selection을 결과 보기 전에 contract로 동결
- endpoint exact prime count 2개 구현 또는 한 구현+certificate의 일치
- primary/verifier segment 수와 sieve span 동결
- 4 physical/8 logical, worker native thread 1
- RAM 32 GB, disk cap과 hard wall 설정
- 두 pass artifact와 source/input SHA-256 manifest 결박
- terminal/saved verification 전 결과 사용 금지

P018가 다음 recurrence range를 `HOLD_NEXT_RANGE`로 판정한 상태이므로 P019 actual P013-C runner는
지금 만들지 않는다. P019는 future range가 통계적 gate를 통과했을 때 쓰는 계산공학 준비다.

