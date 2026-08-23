# P005b Rank 85 이후 exhaustive 확장 calibration 제안 타당성 검토

## 1. 판정

**`REJECT_CURRENT_METHOD / ABSORB_VALID_METRICS_INTO_P005`**

“작은 실행으로 처리량을 측정한 뒤 장기 계산 여부를 결정한다”는 의사결정 원칙은 타당하다. 그러나 제안된 `sethtroisi/prime-gap` 실행으로 임의의

\[
[10^{20},10^{20}+10^{16})
\]

를 exhaustive하게 덮을 수 있다는 전제가 성립하지 않는다. 따라서 현재 제안 그대로는 P005b 실행계획을 신설하지 않는다. 공식 correctness, CPU thread scaling, wall/CPU time, RSS, output hash 기록만 기존 P005에 흡수한다.

## 2. 타당한 부분

1. gap 1858 위치를 다음 record라고 가정하지 않고, 그보다 앞선 모든 `gap > 1854`의 부재가 별도 증명 대상이라고 구분한 점
2. Cramér형 모델을 coverage 생략 근거가 아니라 workload heuristic으로만 제한한 점
3. false positive는 후처리할 수 있지만 false negative는 허용할 수 없다고 한 점
4. CPU-only, 단계별 중단, checkpoint, 처리시간·메모리·candidate 수 기록을 요구한 점
5. 독립 reference와 결과가 정확히 일치해야 한다고 한 점

이 원칙들은 P005의 coverage 계약과 향후 일반 구간 엔진의 승인 게이트에 유지한다.

## 3. 핵심 결함: 좌표계가 다르다

고정 commit의 upstream 설명과 코드 계약에서 `combined_sieve` 입력은 `m_start`, `m_inc`, `P#`, `d`이고, 대상은 여러 `m * P#/d` 주변 interval이다. `--minc`는 일반 정수축의 길이가 아니라 처리할 `m` 개수다. 따라서 다음 두 처리량은 동일하지 않다.

```text
valid:   primorial-centered m values / second
invalid: arbitrary x-range integers / second
```

P005b의 Calibration A–D는 임의의 `[start,end)` API, block ledger, 경계 overlap, 누락 검증을 요구한다. 현재 `prime-gap` suite에는 이 계약이 없다. `gap_stats`의 확률 순위도 후보 우선순위이지 coverage certificate가 아니다.

근거: [고정 commit의 prime-gap 저장소](https://github.com/sethtroisi/prime-gap/tree/8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d), [README](https://github.com/sethtroisi/prime-gap/blob/8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d/README.md), [combined_sieve.cpp](https://github.com/sethtroisi/prime-gap/blob/8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d/combined_sieve.cpp)

## 4. “작은 calibration 구간”도 작지 않다

`x≈10^20`에서 평균 소수 밀도를 `1/ln(x)`로만 거칠게 잡아도 폭 `10^16`에는 약

\[
10^{16}/\ln(10^{20})\approx2.17\times10^{14}
\]

개의 prime-start 관측기회가 있다. 폭 `10^17`, `10^18`은 각각 이 값의 10배, 100배다. 이것은 coverage 엔진의 짧은 smoke test가 아니다. 초기 correctness block은 구현된 엔진의 처리량을 본 뒤 수분~수십 분 안에 끝나는 크기로 정해야 한다.

또한 표준 `primesieve`는 `[START,STOP] < 2^64` 계약이다. Rank 85 시작점 `101412319996363309069`은 `2^64-1`보다 크므로 설치된 `primesieve-bin`을 이 구간의 직접 reference로 사용할 수 없다. [primesieve 공식 README](https://github.com/kimwalisch/primesieve)

## 5. threshold 특화가 coverage를 대신하지 못한다

`gap > 1854`에 특화한 residue filter는 survivor와 PRP 수를 크게 줄일 가능성이 있다. 그러나 후보가 제거되기 전에

\[
g(p)>1854\Rightarrow p\text{가 candidate set에 남는다}
\]

를 모든 block에서 증명하거나 기계 검증해야 한다. survivor 처리량만 측정해 전체 x-구간 처리량으로 환산하면 sieve coverage 비용과 false-negative 위험이 빠진다.

## 6. P005에 흡수하는 항목

- pinned commit official Method1/Method2 quick-test와 기대 MD5
- CPU-only build와 GPU target 미빌드
- 1, 2, 4, 8 threads의 같은 `m` 범위 output hash 일치
- 각 단계 wall time, CPU time, maximum RSS, exit code, output hash
- `gap_stats`와 `gap_test_simple`의 candidate/PRP 관측값
- 보고 단위를 `m-values/s`, `unknown candidates/s`, `PRP/s`로 명시
- 이 값을 `integers/s`, `x-range/s`, Rank 85→86 ETA로 변환하지 않는 해석 게이트

## 7. P005b 재개 조건

다음 조건이 모두 준비되면 별도 P005b 계획을 신설할 수 있다.

1. `X0 > 2^64`를 지원하는 arbitrary `[start,end)` CPU engine
2. 모든 prime start 또는 동치인 완전 residue coverage에 대한 증명 가능한 분할 규칙
3. block별 시작·끝·overlap·완료 hash를 보존하는 coverage ledger
4. `gap > 1854` survivor의 양 끝 소수성과 내부 합성수를 검증하는 certificate
5. 작고 독립적인 reference block 100% 일치
6. 재시작 가능한 checkpoint와 32 GiB 미만 강제 자원 제한
7. 최소 3개 block 반복 측정과 위치·폭에 따른 throughput uncertainty

이 조건 전에는 `REJECT_CURRENT_METHOD`이며, P005 calibration 성공도 일반 구간 exhaustive 가능성을 의미하지 않는다.

## 8. 결론

P005b의 좋은 점은 계산 전 실측과 중단 기준을 요구한 것이다. 하지만 측정 대상 도구가 요청한 x-구간을 덮지 못하므로 현재 형태의 runtime model은 식별 불가능하다. 독립 P005b 실험은 만들지 않고, 먼저 P005의 bounded functional calibration으로 upstream 도구가 이 PC에서 정확히 작동하는지만 측정한다. 일반 구간 엔진이 따로 생겼을 때 P005b를 새 승인 단계로 재설계한다.
