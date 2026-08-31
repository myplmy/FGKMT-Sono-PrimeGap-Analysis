# P017 P013 병렬 actual-calibration 결과 분석

최종 갱신: 2026-08-30 02:52 KST

## 판정

`EXPERIMENT_PASS / EXACT_EQUIVALENCE_PASS / PERFORMANCE_POSITIVE`

P017 combined queue와 P017-A/B 두 child가 모두 정상 종료했다. 저장된 모든 manifest artifact의
SHA-256을 다시 계산해 일치함을 확인했고, 두 saved verification report는 issue 0이다. P017은
P013의 수론적 결론을 새로 계산한 실험이 아니라, 같은 prime-gap sufficient statistics를
8-process segment 병렬화가 빠뜨리거나 바꾸지 않는지 확인한 계산공학 calibration이다.

## 실행과 범위

| 구분 | 범위 | 비교 방법 | 결과 | child wall time |
|---|---|---|---|---:|
| P017-A | `[10^10,10^11)` | 새 8-worker·32-segment 결과 대 완료된 P013-A serial 정본 | exact equality PASS | 709.687초 |
| P017-B | `[10^11,316227766017)` | 같은 실행에서 serial oracle 생성 후 8-worker·64-segment 계산 | exact equality PASS | 15,481.750초 |
| combined queue | 위 두 child | continue-on-failure orchestration과 saved queue 검증 | 2/2 PASS | 16,191.671초 |

전체 queue는 약 4시간 29분 52초에 끝났다. 계획한 16시간 hard wall보다 충분히 짧았고,
새 artifact 증가량은 327,787 bytes로 decimal 5 GB 제한보다 매우 작았다. GPU는 사용하지 않았다.

## 정확성 감사

### P017-A

- gap start 3,663,002,302개를 32개 segment로 분할했다.
- 인접 segment 경계 31개를 검사했고 각 오른쪽 crossing gap을 boundary prime으로 닫았다.
- 실제 worker PID 8개가 참여했고 worker당 native thread ceiling은 1이었다.
- 병렬 checkpoint payload와 serial checkpoint canonical SHA-256이 정확히 같았다.
- 병렬 checkpoint로 다시 만든 analysis 파일과 P013-A serial analysis가 byte-level SHA-256까지
  같았다.
- `work_items_omitted=false`, `precision_reduced=false`, `scientific_result_changed=false`다.

### P017-B

- gap start 8,313,825,647개를 serial과 64-segment 병렬 방식으로 각각 계산했다.
- 인접 segment 경계 63개, worker PID 8개, exact integer merge를 모두 확인했다.
- serial/parallel sufficient-statistics SHA-256이
  `697845588144d01d9096210a8c745a36dfa49492fc30ba38dcd3f670ca6935f9`로 같았다.
- compact checkpoint 파일과 fixed-seed inference 파일도 각각 byte-level exact equality를
  통과했다.
- prime 배열을 process 사이에 옮겨 메모리를 불필요하게 복제하지 않았고, 빠진 작업이나
  정밀도 축소는 없었다.

### 저장 산출물 독립 확인

| 대상 | manifest SHA-256 | 저장 검증 | 독립 재해시 issue |
|---|---|---|---:|
| P017-A | `47c3e88fb7016588489fcc7dc62c4b381b3d03d91ee2ca2d5aa8f52b1f5624d5` | PASS | 0 |
| P017-B | `509929482e3f51a5314ab3799e4d0972b19e3519aa26f4432e53abf1f2963397` | PASS | 0 |
| queue | `115390933176f9d4b70d08dba1ef49a14acce4492ef3c4a32552611490142f0e` | PASS | 0 |

queue log에는 `[FAIL]`과 Python traceback이 0건이며 terminal queue PASS가 있다. 사용자가 별도로
launcher PASS도 확인했다.

## 속도 해석

P017-B는 같은 실행·같은 범위에서 serial과 parallel을 연속 측정했으므로 가장 공정한 비교다.

- serial oracle 완료: 12,598.410초, 약 3시간 29분 58초
- parallel 64-segment 단계: 준비시간 포함 2,866.160초, 약 47분 46초
- 관측 wall-time 비: `12,598.410 / 2,866.160 = 4.3956`

따라서 이 PC의 물리 4코어·논리 8프로세스 정책에서 해당 workload는 약 4.40배 빨라졌다. 8개
logical processor를 썼다고 8배가 되지 않는 것은 정상이다. segment 준비, memory bandwidth,
sieve의 비병렬 부분과 worker load imbalance가 남기 때문이다.

P017-B 초반 CPU 사용률이 P017-A보다 낮았던 원인도 확인됐다. 앞의 약 3시간 30분은 비교용
serial oracle을 단일 stream으로 만들던 단계였고, 병렬 단계는 그 뒤 약 48분만 실행됐다. 즉
8-worker 구현이 멈췄거나 일부 worker가 누락된 현상이 아니다.

P017-A는 11분 31초의 병렬 계산과 exact 비교를 통과했지만 같은 P017 실행 안에서 새 serial
계산을 하지 않았으므로, P017-B처럼 엄밀한 동일조건 speedup 수치로 사용하지 않는다.

## 무엇을 알 수 있고 무엇을 말할 수 없는가

알 수 있는 것:

- 두 실제 범위에서 segment 병렬화가 serial 정본과 exact하게 같은 결과를 만들었다.
- P013 계열의 future range 계산에 병렬 engine을 사용할 충분한 engineering calibration 근거가
  생겼다.
- 새 serial 정답표가 없는 범위에서는 서로 다른 segment partition을 이용한 병렬 이중 계산과
  독립 경계·count 검증을 결합하면 serial full pass 없이도 검증 비용을 줄일 여지가 있다.

아직 말할 수 없는 것:

- 테스트한 두 범위를 넘어 모든 범위에서 구현이 수학적으로 무조건 옳다는 증명
- 병렬 결과 한 번만으로 독립 verification까지 끝났다는 주장
- P013 recurrence 가설이나 prime-gap 정리의 지지
- 4.40배가 모든 범위·segment 수에서 그대로 유지된다는 보장

기존 serial actual runner는 이번 PASS만으로 삭제하지 않는다. 다음 revision은 primary와 verifier가
서로 다른 partition을 사용하는 parallel dual-pass를 별도 경로로 toy 검증한 뒤, 사용자가 actual
승격을 다시 승인하는 순서가 안전하다.

## provenance

- queue result: `test_result/run_20260829T124332Z_p017_16h_p013_parallel_calibration_queue`
- P017-A result: `test_result/run_20260829T124333Z_p017a_p013a_parallel_full_calibration`
- P017-B result: `test_result/run_20260829T125523Z_p017b_p013b_parallel_midrange_calibration`
- queue log SHA-256:
  `5d694cf42bf640f682d1754ae34d2e3141023b8f1fb60561ac09f7bced2c5128`
- P017-A log SHA-256:
  `6c6c2562cda33f5f1aad6c543467ea58496e05e340b8937fd994ea15bd304cbc`
- P017-B log SHA-256:
  `bdd59e7164c12b6db992353792ffe06ae9ce4886c6312e7ae45389853efe5200`

완료 entrypoint는 당시 bytes를 보존해 다음 SHA-256으로 `test_done`에 이관했다.

| 완료 파일 | SHA-256 |
|---|---|
| `run_P017_16h_P013_parallel_calibration_queue-20260829T124332Z-done.bat` | `37d20046e6141325c01f99e19090a96a5959bfb2cad415078107da08f11b29f6` |
| `run_P017A_P013A_parallel_full_calibration-20260829T124333Z-done.bat` | `58d25ebdc938e5c3c661a32e6eaad0d2f480e754a88a0245d98d0a9e5fed6b72` |
| `run_P017B_P013B_parallel_midrange_calibration-20260829T125523Z-done.bat` | `1d24ac7dfa97cc5b5263a2089d85fbbc16c9a5fff4dc05c83cad2f59a2e965c9` |
| `run_p017_16h_parallel_calibration_queue-20260829T124332Z-done.ps1` | `29d7a47864ec7bd87e4afe4dec9086049a8bccc6203f0cfae86099eb5afc3bde` |
| `run_p017a_p013a_parallel_full_calibration-20260829T124333Z-done.ps1` | `27ceca2472db5cf811925d4506b76231a5edfb59b500a5de6d7a3ea1624495d3` |
| `run_p017b_p013b_parallel_midrange_calibration-20260829T125523Z-done.ps1` | `bbee80900382c1ec72094897831540286b3695c4e787b1a4061312b0b7ac2359` |
