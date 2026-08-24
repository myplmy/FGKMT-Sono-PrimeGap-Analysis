# P005 CPU-only calibration 성공 결과 분석

## 최종 판정

`CALIBRATION_PASS / EXHAUSTIVE_EXTENSION_NOT_PROVED`

사용자 실행 `20260824T054203Z_p005_prime_gap_cpu_calibration`은 CPU-only 빌드, upstream Method1/Method2 비교, canonical gaps DB 변환, `gap_stats`, `gap_test_simple`, thread-scaling, 저장 hash 검사를 모두 통과했다. 이전 실행의 누락된 SQLite 장부와 `gaps.db` 문제는 재발하지 않았다.

이 PASS는 Seth Troisi `prime-gap` 도구가 현재 Ryzen 7 9700X·WSL 환경에서 작은 bounded calibration을 재현 가능하게 수행했다는 뜻이다. Rank 85와 Rank 86 사이를 빠짐없이 탐색했거나, 그 전체 소요시간을 확정했다는 뜻은 아니다.

## 실행 증거

- log: `test_result/logs/run_20260824T054203Z_p005_prime_gap_cpu_calibration.log`
- log SHA-256: `55820ffe6ba50e9cd50fe6f5b2e3cef576d65306702fe43553a9c77e6508309e`
- run root: `tmp/prime-gap-p005/20260824T054203Z_p005_prime_gap_cpu_calibration`
- manifest: `status=CALIBRATION_PASS`
- 시작/종료 UTC: `05:42:03`–`05:43:30`, 약 87초
- upstream code commit: `8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d`
- gap-data commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- GPU: 미사용
- threads: 최대 8
- memory contract: upstream 28 GiB, shell hard limit 30 GiB
- failed manifest: 없음

| 검사 | 결과 |
|---|---:|
| CPU-only build | PASS, 3.36초 |
| Method1 | PASS, 0.47초 |
| Method2 | PASS, 0.63초 |
| reference `gap_stats` | PASS, 5.41초 |
| reference `gap_test_simple` | PASS, 0.85초 |
| canonical gaps DB rows | 122,251 |
| search-ledger tables | `m_stats, range, range_stats, result` |
| thread-scaling output hash | 1·2·4·8 threads 모두 동일 |
| 최대 관측 RSS | 210,048 KiB, 약 205 MiB |

search DB와 gaps DB의 SHA-256도 manifest와 일치했고, 세 unknowns 파일의 MD5 및 thread-scaling 네 출력의 SHA-256도 모두 일치했다.

## 성능 관찰

작은 `minc=2000` 표본에서 sieve wall time은 다음과 같았다.

| threads | wall time |
|---:|---:|
| 1 | 1.23초 |
| 2 | 0.73초 |
| 4 | 0.54초 |
| 8 | 0.66초 |

이 표본에서는 4 threads가 가장 빨랐다. 그러나 실행시간이 1초 안팎이라 startup·I/O 잡음 비중이 크므로 “본 탐색도 4 threads가 최적”이라고 확정할 수 없다. `minc=10000`의 전체 작은 pipeline에서는 sieve 1.19초, stats 5.57초, candidate test 45.11초로, 이 설정에서는 마지막 검사가 대부분의 시간을 사용했다.

## warning 판정

로그의 다음 경고는 이번 PASS를 취소하지 않는다.

```text
WARNING stats aren't synchronized when running with multiple threads(8)
```

이는 upstream 프로그램이 여러 thread의 진행 통계를 동시에 갱신할 때 표시값이 완전히 동기화되지 않는다는 경고다. 최종 unknowns의 correctness는 Method1/Method2 비교와 1·2·4·8-thread 출력 hash 일치로 별도 확인됐다.

`Estimated modulo searches ... error 0.19%–0.31%`도 실제 후보 누락 판정이 아니라 내부 작업량 예측치와 관측치의 차이다. 각 단계 exit 0, 최종 checksum, terminal PASS가 모두 존재하므로 실험 실패 증거로 보지 않는다.

## 쉬운 해석

이번 실험은 새 대륙을 횡단한 것이 아니라, 탐색 차량의 엔진·계기판·기록장부가 이 PC에서 정상 작동하는지 짧은 시험주행을 한 것이다. 시험주행은 성공했다. 하지만 `prime-gap`은 임의의 연속 x 구간을 그대로 훑는 도구가 아니라 `m·P#/d` 주변 후보를 생성·선별·검사하는 pipeline이다. 따라서 Rank 85→86 사이의 모든 가능한 gap start가 이 작업단위에 포함된다는 coverage 증명이 먼저 필요하다.

공식 도구의 pipeline 역할은 [Seth Troisi prime-gap 저장소](https://github.com/sethtroisi/prime-gap)에 설명되어 있다.

## 한계와 다음 게이트

- calibration 표본으로 Rank 85→86 전체시간을 단순 외삽하지 않는다.
- 전체 연속 x 범위의 false-negative 0 coverage가 아직 증명되지 않았다.
- P008의 전역·local count 상한도 현재까지 후보 위치를 제공하지 않는다.
- 따라서 다음 단계는 장시간 본 탐색이 아니라, candidate-cover/mapping theorem과 작은 coverage verifier 설계다.

