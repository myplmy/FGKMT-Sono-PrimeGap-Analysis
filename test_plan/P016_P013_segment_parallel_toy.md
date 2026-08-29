# P016 — P013 segment 병렬 sufficient-statistics toy

## 1. 상태

`COMPLETED` — 합성·소규모 prime range toy 구현과 로컬 검증을 완료했다.
P013 actual range 재실행과 기존 runner 승격은 승인되지 않았다.

## 2. 연구 질문과 비목적

P013 계열의 segmented prime stream을 독립 `[a,b)` 작업으로 나누고, 각 worker가 prime 배열이
아닌 sufficient statistics만 반환해도 기존 serial 계산과 정확히 같은 결과를 얻는지 확인한다.

비목적은 recurrence 과학결론 갱신, P013-A/B 재실행, Monte Carlo replication 축소, actual
wall-time 예측이다.

## 3. 수학·경계 정의

각 segment `[a,b)`는 그 안에 있는 prime gap start를 모두 센다. 마지막 `p<b`에서 첫
`q>=b`까지의 crossing gap도 해당 segment가 센다. 인접 segment에서 `q`는 첫 소수로 재사용되지만
그 앞 gap은 다시 세지 않는다.

canonical FGKMT 정의와 반복로그는 변경하지 않는다.

## 4. 입력·원천·완전성

- 외부 dataset 없음
- 합성 plateau metadata와 로컬 exact segmented sieve만 사용
- actual validated record 파일은 읽지 않음
- 소규모 범위의 serial 정본 `iter_prime_chunks_range + accumulate_bin_counts`가 oracle

## 5. 입력 필터와 merge 규칙

1. 전체 `[L,U)`를 겹치지 않는 연속 segment로 정수 분할한다.
2. worker는 자기 segment와 오른쪽 boundary prime을 sieve한다.
3. nested count table은 integer addition으로만 합친다.
4. 전체 `prime_count = total_gap_count + 1`로 복원한다.
5. key와 segment는 정렬해 worker 완료 순서의 영향을 제거한다.

## 6. 사전검증·중단 조건

- 범위가 비어 있거나 segment가 겹치거나 비면 중단
- 인접 `boundary_prime != next.first_prime`이면 중단
- worker local `prime_count != gap_count + 1`이면 중단
- serial과 어떤 core field라도 다르면 FAIL
- worker 1·2·4·8 결과가 다르면 FAIL

## 7. 실행 명령

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest tests.test_parallel_segment_statistics -v
```

## 8. 산출물

- 별도 source 모듈
- 단위시험 출력
- 로컬검증 보고서
- actual dataset·그래프·과학 결과는 생성하지 않음

## 9. 판정 기준과 한계

모든 exact-equivalence gate가 PASS하면 toy 엔진만 `LOCALLY_VERIFIED`다. actual 가속, 8-worker
효율, P013 연구결과는 판정하지 않는다.

## 10. 후속 작업

사용자 별도 승인 뒤 중간범위 calibration과 32 GB resource gate를 설계한다.

## 완료 증거

- targeted P013 tests: 4/4 PASS
- worker invariance: 1/2/4/8 PASS
- 통합 toy: 68,906 gap starts, 32 segments, worker process 8개 관측
- serial exact nested counts·downstream plateau/components equality PASS
- 정본: `test_result/202608290552_P013_P014_parallel_toy_local_validation.md`
- actual range·actual runner: NOT RUN / NOT PROMOTED
