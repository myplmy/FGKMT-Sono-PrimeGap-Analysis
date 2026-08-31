# P017 — P013 병렬 actual calibration

## 1. 상태

`EXPERIMENT_PASS / EXACT_EQUIVALENCE_PASS` — 2026-08-29 combined queue와 P017-A/B 두 child가
terminal·saved verification을 통과했다. 결과 정본은
`test_result/202608300229_P017_parallel_calibration_result_analysis.md`다.

P017-A는 완료된 P013-A serial checkpoint/analysis를 oracle로 읽어 새 계산은 8-worker parallel만
했다. P017-B는 해당 midrange oracle이 없으므로 single-stream serial sweep 뒤 8-worker parallel
sweep을 순서대로 수행한다. 따라서 P017-B의 `serial_sieve_progress` 동안 CPU 사용률이 P017-A보다
낮은 것은 정상이며, `serial_oracle_completed` 이후 parallel stage에서 높아져야 한다.

## 2. 연구 질문과 비목적

연구 질문:

1. P013-A 전체범위의 병렬 sufficient statistics와 downstream analysis가 완료된 serial 정본과
   exact하게 같은가?
2. P013-B 첫 primary half-decade에서 serial·parallel 계산이 prime/gap·plateau·component·
   inference를 하나도 빠뜨리지 않고 동일하게 복원하는가?
3. 물리 4코어·논리 8프로세스가 실제로 참여하고 16시간 queue 안에서 끝나는가?

비목적:

- P013-A/B의 과학적 결론을 변경하지 않는다.
- P013-B full result를 대체하거나 P013-B와 동시에 실행하지 않는다.
- P013-C나 더 큰 decade의 새로운 가설검정을 수행하지 않는다.
- 병렬 PASS만으로 기존 actual runner를 교체하지 않는다.

FGKMT canonical 정의는 end-bounded `G(x)`이고 `log_k`는 자연로그 k회 반복이다. P017은 이를
계산하지 않는 별도 engineering calibration이다.

## 3. 수학·통계 정의

- 각 segment `[a,b)`는 `a <= gap_start < b`인 모든 consecutive-prime gap을 정확히 한 번 담당한다.
- worker는 `b` 이상 첫 소수 하나까지 포함해 마지막 crossing gap을 닫는다.
- P013-A 통계 계약: 기존 P013 contract의 bin·cohort·seed `20260828`·100,000회.
- P013-B midrange calibration seed: `20260829`, 100,000회.
- serial/parallel exact equality는 integer sufficient statistics 전체와 derived plateau/component,
  fixed-seed inference 전체에 적용한다.

## 4. dataset·pin·완전성

- canonical source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated record SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- exhaustive limit: `10^20`
- P013 contract SHA-256:
  `153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf`
- P013-A serial oracle run: `20260828T071601Z_p013a_recurrence_extension_1e11_r2`
- oracle checkpoint SHA-256:
  `cd6a85ef2cb766bc04a9ddc3bf98a2fc8f12c5f19efbcaaa740318622edf4502`
- oracle analysis SHA-256:
  `70c8897af813ec072e1510bcc6e40e6535d3bce95b782801fe4f6bf9a9060b7b`
- 외부 다운로드: 없음
- P017 calibration contract SHA-256:
  `27eebe4873bf24e0b63e6e667deede9314c22207f2fd3dfc11c727218ff7932f`

## 5. 고정 범위와 복원 규칙

| step | 범위 | complete record | 비교 |
|---|---|---|---|
| P017-A | `[10^10,10^11)` | `36–39` | parallel vs 완료 serial checkpoint·analysis |
| P017-B | `[10^11,316227766017)` | `41–45` | 새 serial vs parallel exact |

P017-B upper endpoint는 primary width-0.5 log bin의 첫 경계 `10^11.5`보다 큰 최소 정수다.
따라서 정수 gap start 전체를 half-open 범위로 정확히 표현한다.

## 6. 사전검증·중단 조건

사전검증:

1. FGKMT Python `W:\miniforge3\envs\FGKMT\python.exe` 고정
2. records·P012/P013 prerequisites·P013-A oracle hash 일치
3. P017 contract와 source hash 기록
4. process affinity `0xff`, 물리 4·논리 8 확인
5. worker 8, segment A 32/B 64, worker native thread ceiling 1
6. approval flag 없이는 입력 sweep·result directory 생성 전 거부
7. P013-B original run 종료를 사용자가 확인

즉시 중단:

- P013-B original이 아직 실행 중임
- segment 경계 prime 불일치, worker 누락, gap count 또는 exact core 불일치
- plateau/component/inference 불일치
- oracle hash 또는 provenance 불일치
- A 4시간, B 11시간, queue 16시간 hard wall 초과
- aggregate 신규 artifact 5 decimal GB 초과 또는 RAM 32 GB 이상 징후
- output overwrite 시도

## 7. 완료된 사용자 실행 이력

사용자는 combined queue 방식을 실행해 완료했다. 아래 명령은 실행 provenance이며 현재 root
entrypoint는 `test_done/*-done`으로 이관됐으므로 다시 실행하지 않는다.

전체 queue:

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P017_16h_P013_parallel_calibration_queue.bat --confirm-after-p013b
```

개별 실행:

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P017A_P013A_parallel_full_calibration.bat --confirm-after-p013b
.\run_P017B_P013B_parallel_midrange_calibration.bat --confirm-after-p013b
```

개별 실행 BAT는 사용하지 않았지만 완료 P017 전용 entrypoint라 같은 run과 함께 보존 이관했다.
현재 별도 사용자 수행절차는 없다.

## 8. 산출물

- run별 `comparison.json`, `summary.json`, `manifest.json`
- P017-A parallel checkpoint·analysis 및 oracle exact 비교
- P017-B serial/parallel compact checkpoint·inference 비교
- segment별 `progress.jsonl`
- `saved_verification_report.json`
- stdout/stderr·traceback을 포함한 run log
- queue 사용 시 `queue_events.jsonl`, queue summary·manifest·verification

## 9. 판정 기준과 제한

`EXPERIMENT_PASS`는 terminal PASS, exact comparison, worker 8 참여, saved artifact verification이
모두 PASS일 때만 부여한다. 속도가 느려도 정확성 PASS와 성능 음성 결과를 구분한다. P017-B는
P013-B 전체 결과가 아니며 scientific recurrence 결론에 사용하지 않는다.

## 10. 실행 결과와 후속 작업

P017-A는 709.687초, P017-B는 15,481.750초, combined queue는 16,191.671초에 PASS했다. P017-B
내부 동일 범위 비교에서 serial은 12,598.410초, parallel은 준비시간 포함 2,866.160초로 관측
wall-time 비가 약 4.3956이었다. 다음 단계는 serial 정답표가 없는 새 범위를 위한 서로 다른
partition의 parallel dual-pass verification을 별도 revision으로 toy 검증하는 것이다.

## 구현·로컬검증 증거

- 병렬 actual-calibration: `source/recurrence_parallel_calibration.py`
- CLI: `source/recurrence_parallel_calibration_cli.py`
- bounded queue: `source/p013_parallel_calibration_queue.py`
- 공통 runner: `scripts/runners/run_p013_parallel_calibration.ps1`
- 개별/queue 진입점: `scripts/experiments/p017/`와 root BAT 3개
- targeted unit tests: 16/16 PASS, 10.166초
- 전체 regression: 170/170 PASS, 26.900초
- A/B preflight: actual prime range read false, current P013-B artifact read false
- PowerShell parser 4/4, BAT approval-denial 3/3, py_compile PASS
- Windows sandbox 내부 multiprocessing은 `PermissionError: [WinError 5]`로 차단됐고 동일 시험을
  sandbox 밖 FGKMT Python에서 재실행해 PASS했다. 이는 코드 FAIL이 아니다.
- actual queue·A·B result directory와 log: 생성 및 saved verification PASS
- 결과보고서: `test_result/202608300229_P017_parallel_calibration_result_analysis.md`
