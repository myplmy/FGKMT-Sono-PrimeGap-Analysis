# P005 WSL CPU calibration 재실행 감사 및 부분 결과 분석

## 최종 판정

`USER_RUN_FAILED / PARTIAL_CALIBRATION_EVIDENCE_VALID / CALIBRATION_PASS MANIFEST INVALID`

이번 실행은 build, SQLite search ledger, upstream Method1/Method2 output 일치, thread-scaling output 일치, 여러 `combined_sieve`와 `gap_test_simple` 단계에는 성공했다. 그러나 첫 `gap_stats`가 필수 `gaps.db` 부재로 exit 1을 반환했다.

실행기의 error handler가 `set +e`를 현재 shell에 남기는 결함 때문에 그 뒤 단계가 계속 실행됐고 마지막에 `CALIBRATION_PASS` manifest까지 생성됐다. 따라서 두 manifest 중 `manifest.failed.txt`가 최초 실패의 올바른 증거이며, 뒤의 `manifest.txt`와 terminal PASS는 전체 성공 판정에 사용할 수 없다.

## 실행 증거

- log: `test_result/logs/run_20260823T190408Z_p005_prime_gap_cpu_calibration.log`
- log SHA-256: `2a4b9ad842e520cacab72b66044cc3ab59bb5c118d2a33d854cb77c6b91b7860`
- run root: `tmp/prime-gap-p005/20260823T190408Z_p005_prime_gap_cpu_calibration`
- failure manifest SHA-256: `2689d5bc5034e9f03f35bc0bc0ebe4e4cf86c27063204507368ea32755500b52`
- misleading success manifest SHA-256: `f9e04b37303ce98869b34ea1be18ddf6b72db232cd0c1c2ceea045f7a9fc010b`
- metrics SHA-256: `b955dabbeee8ed7197cb5a32559e666015939405962ac32eff2dd5ba78202ad2`
- upstream commit: `8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d`
- WSL logical CPUs: 16, configured threads: 8
- hard virtual-memory cap: 30 GiB
- GPU: disabled
- target exhaustive search: false

## 최초 실패

```text
stage=upstream-reference-gap-stats
exit_code=1
failed_line=246
failed_command=tee "$run_root/gap_stats_minc200.txt"
'gaps.db' doesn't exist
```

`prime-gap-search.db`와 `gaps.db`는 서로 다른 데이터베이스다.

- `prime-gap-search.db`: 이번 sieve range, 통계, test 결과를 저장하는 작업 ledger
- `gaps.db`: 기존 prime-gap record와 merit를 읽는 reference database

helper는 첫 DB만 `schema.sql`로 만들었고, upstream README가 요구하는 `prime-gap-list/allgaps.sql → gaps.db` 단계를 빠뜨렸다. `gap_stats`는 `--search-db`와 별도로 기본 `gaps.db`를 열기 때문에 실패했다.

## 유효한 부분 결과

첫 실패 전에 끝난 단계와, 실패 뒤 잘못 계속되었지만 각 process exit 0·hash 대조로 독립 확인 가능한 단계만 부분 증거로 보존한다.

### build와 reference correctness

- CPU-only build exit 0
- build wall time 3.19초
- build peak RSS 210,212 KiB
- `prime-gap-search.db` table: `m_stats, range, range_stats, result`
- Method1와 Method2 minc=200 unknown output MD5 모두 upstream 고정값과 일치
- minc=200 Method1 0.43초, Method2 0.55초
- `gap_test_simple` minc=200 exit 0, 0.84초

작업 DB를 read-only로 확인한 최종 row 수는 다음과 같다.

```text
range=3
range_stats=0
m_stats=0
result=0
```

`gap_stats`가 하나도 성공하지 않아 통계 table이 비어 있는 상태와 일치한다.

### thread scaling

minc=2000의 1/2/4/8-thread unknown output SHA-256은 모두 같았다. 즉 thread 수가 결과 파일을 바꾸지는 않았다.

| threads | wall time | t1 대비 |
|---:|---:|---:|
| 1 | 1.17초 | 1.00× |
| 2 | 0.70초 | 1.67× |
| 4 | 0.53초 | 2.21× |
| 8 | 0.73초 | 1.60× |

이 매우 작은 입력에서는 4 threads가 가장 빨랐고 8 threads는 overhead 때문에 느려졌다. 실제 큰 workload의 최적 thread 수가 4라는 결론은 아직 내릴 수 없다.

### calibration search와 simple gap test

| minc | combined_sieve | gap_test_simple | gap_stats |
|---:|---:|---:|---|
| 2,000 | 0.67초 | 8.90초 | FAIL: missing gaps.db |
| 10,000 | 1.07초 | 49.99초 | FAIL: missing gaps.db |

`gap_test_simple` 시간이 minc와 함께 크게 증가했고 CPU 사용률은 약 한 core 수준이었다. 그러나 `gap_stats`가 전부 빠졌으므로 end-to-end calibration 처리량이나 Rank 85→86 예상시간을 이 실행만으로 확정하면 안 된다.

## warning 해석

### `stats aren't synchronized when running with multiple threads`

upstream의 진행 통계 counter가 multi-thread에서 정확히 동기화되지 않는다는 경고다. 최종 unknown output hash가 1/2/4/8 threads에서 일치했으므로 이번 작은 fixture에서는 correctness 불일치 증거가 아니다.

### `Estimated modulo searches ... error 0.19%/0.31%`

예상 작업량과 실제 작업량의 성능 추정 오차다. certificate 또는 prime-gap 정답 오류가 아니다. 다만 시간 예측 모델을 보정할 때 기록해야 한다.

## 왜 실패 manifest와 PASS manifest가 둘 다 생겼는가

error handler의 `write_failed_manifest`가 재귀 오류를 막으려고 `set +e`를 실행했지만 원래 shell 옵션을 복구하지 않았다. 첫 pipeline failure 뒤 `errexit`가 꺼졌고 나머지 stage가 계속 실행됐다. 마지막 코드는 failure manifest 존재를 검사하지 않고 success manifest와 PASS 문구를 썼다.

따라서 이번 실행의 올바른 시간순 해석은 다음과 같다.

1. `gap_stats`에서 최초 실패
2. failure manifest 정상 생성
3. runner bug로 후속 단계가 의도치 않게 계속됨
4. 일부 후속 명령은 독립적으로 exit 0
5. 마지막 PASS/manifest는 전체 성공을 의미하지 않음

## 로컬 교정 내용

actual 재실행은 하지 않고 helper만 다음과 같이 수정했다.

1. canonical raw `allgaps.sql` commit `1a112...b68`, SHA-256 `988c...894f`를 확인
2. 별도 `gaps.db`를 생성하고 `gaps` row가 양수인지 검사
3. `gap_stats`와 `gap_test_simple`에 `--prime-gaps-db` 명시
4. failure handler의 `set +e`를 subshell 안으로 격리해 parent `errexit` 보존
5. failure manifest가 존재하면 success manifest 작성을 거부
6. minc별 search/stats/test stage 이름을 분리
7. success/failure manifest에 gap-data provenance와 DB hash 기록

이 교정은 정적·toy shell 검증을 통과한 뒤에만 사용자에게 재실행을 요청한다.

## `tmp` 저장 위치 판정

bulky upstream clone, build binary, SQLite DB, unknown files, timing 중간산출물을 `tmp/prime-gap-p005/<run_id>`에 두는 것은 타당하다. 이들은 정본 연구결과가 아니라 재생성 가능한 calibration 작업공간이고 크기가 커질 수 있다.

반면 다음은 정본 경로에 남아야 하며 실제로 그렇게 저장됐다.

- 전체 stdout/stderr log: `test_result/logs/`
- 이 감사·분석 보고서: `test_result/`
- 향후 성공/실패 판정: run-root manifest hash와 함께 보고서에 고정

즉 `tmp` 자체가 실패 원인은 아니며 경로를 옮길 필요는 없다. `tmp` 산출물을 장기 보존 정본처럼 해석하지만 않으면 된다.

## 다음 판정

현재 P005는 `CALIBRATION_PASS`가 아니다. 교정 helper의 local validation 뒤 사용자가 새 run ID로 한 번 더 실행해야 한다. 새 실행에서는 `gap_stats` 3회가 모두 exit 0이고 failure manifest가 없으며 success manifest와 terminal PASS가 함께 있을 때만 전체 PASS로 승격한다.
