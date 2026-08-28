# P014 Python-side live progress 로컬검증

## 판정

`IMPLEMENTED / LOCALLY_VERIFIED / PYTHON_FSYNC_PROGRESS_PASS / WINDOWS_CONSOLE_BYPASS_PREPARED / APPROVAL_GATE_PASS / P014_ACTUAL_NOT_RUN`

P013-A/P013-B에서 장시간 native stage의 stdout·stderr가 stage 종료 뒤 main log에 한꺼번에
복사되어, 사용자가 계산 중인지 확인하기 어려웠다. Python의 기존 `print(..., flush=True)`는
정상적으로 호출됐지만 PowerShell `Start-Process -Wait` capture 경계 밖으로 나오지 못했다.

P014부터는 Python이 별도 progress JSONL을 직접 열어 START·phase·5분 heartbeat·END를
`flush+fsync`한다. Windows console이 연결된 경우 `CONOUT$`에도 `[LIVE]` 행을 직접 써서
redirected stdout을 우회한다. 기존 main log는 stdout·stderr·exit code·traceback의 완전한 사후
기록으로 그대로 유지한다.

## 구현 범위

- 공통 Python reporter: `source/live_progress.py`
- toy tests: `tests/test_live_progress.py`
- P014 analysis/verify CLI: `source/finite_gap_mod510510_cli.py`
- P014 phase callback: `source/finite_gap_mod510510.py`
- 사용자 runner: `scripts/experiments/p014/run_p014_mod510510_staged_certificate.ps1`
- root launcher: `run_P014_mod510510_staged_certificate.bat`

analysis와 saved full exact recomputation은 서로 다른 non-overwrite progress log를 만든다.

```text
test_result/logs/<run-id>.p014-analysis.progress.jsonl
test_result/logs/<run-id>.p014-verification.progress.jsonl
```

각 JSONL 행에는 UTC, elapsed seconds, PID, experiment, stage, event와 마지막 phase가 들어간다.
Python 예외가 발생하면 END 행은 `status=FAIL`과 exception type/message를 기록한다.

## .NET 방식과의 비교·최종 선택

PowerShell parent가 비동기 process를 poll하는 .NET heartbeat도 toy로 검토했다. 그 과정에서
Windows PowerShell 5.1의 비동기 `Start-Process` exit-code 취급이 실제 실패 9를 0으로 보일 수
있는 회귀를 self-test가 잡았다. 직접 `System.Diagnostics.Process`를 쓰는 교정은 성공했지만,
native argument quoting·stream drain·메모리 경계까지 공통 helper에 추가해야 해 복잡도가 컸다.

최종 구현에서는 이 .NET 변경을 제거하고 검증된 기존 PowerShell helper를 원상 유지했다.
`scripts/common/powershell_stage_logging.ps1`과 기존 self-test의 Git blob hash는 index와 다시
같다. P014의 phase를 가장 잘 아는 Python이 liveness를 기록하는 쪽이 더 단순하고 해석도
명확하다.

## 검증 결과

### Python

- `py_compile`: `live_progress.py`, P014 analysis, P014 CLI PASS
- targeted unittest: 6/6 PASS
  - START/PROGRESS/HEARTBEAT/END가 실행 중 파일에서 보임
  - fsync-backed heartbeat와 PASS END
  - exception FAIL END와 error message
  - 기존 progress file non-overwrite
  - P014 CLI는 approval 없을 때 progress log 생성 전에 거부
  - modulus-510510 기존 exact-lift toy와 static target contract 유지

첫 sandbox 실행은 사용자 TEMP 경로 쓰기·정리를 거부해 3개 `TemporaryDirectory` test가
환경 오류로 중단됐다. 동일 명령을 승인된 sandbox 외부 FGKMT Python에서 다시 실행한 결과
6/6 PASS였다. 실제 P014 분석은 실행하지 않았다.

### PowerShell·launcher

- 변경·참조 PS1 parser: 3/3 PASS
- 기존 stage logging self-test: blank stdout/stderr와 synthetic exit 7 처리 PASS
- P014 runner approval denial: exit 1, `requires -ConfirmP014` 확인
- root BAT는 Python live progress가 5분마다 생성된다는 안내 추가
- full repository unittest: 151/151 PASS, 7.172초
- P014 read-only preflight: target constraints `8,524,288,932`, selected logical 8,
  `actual_experiment_executed=false` PASS
- root BAT usage gate: 인수 없음 exit 1·Usage 확인

## 출력의 의미와 한계

- heartbeat가 계속 추가되면 Python process와 reporter thread가 살아 있다는 뜻이다.
- exact-lift START/PASS, seed scan START/PASS, iteration, final exact START/PASS는 실제 phase event다.
- heartbeat 자체는 `8,524,288,932` constraints 중 몇 퍼센트를 끝냈다는 뜻이 아니다.
- true percent와 처리속도를 내려면 low-level exact scanner가 chunk 완료 수를 callback으로
  노출해야 한다. 이는 계산 결과에는 영향을 주지 않지만 공통 certificate scanner 계약과
  saved verifier를 함께 교정·회귀검증해야 하므로 P014 actual 전 별도 최적화 항목으로 남긴다.

현재 요구인 “장시간 아무 로그도 없는지, process가 살아 있는지, 어느 큰 phase인지 확인”은
Python progress log와 Windows console bypass로 충족한다.

## 현재 실행 안전성

이 변경은 P014 전용 analysis/CLI와 새 Python reporter에만 적용했다. 실행 중인 P013-B recurrence
source·runner·checkpoint·result는 수정하지 않았다. P013-B saved full recomputation이 끝나기
전에는 P014를 동시에 시작하지 않는다.
