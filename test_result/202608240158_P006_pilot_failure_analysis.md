# P006 `[2,10^8]` pilot 실행 분석 — 분석 시작 전 중단

## 한눈에 보는 결과

P006 수학 계산이나 segmented sieve가 실패한 것이 아니다. preflight는 PASS했지만, Windows PowerShell 5.1 실행기가 정상적인 Python 단위시험 진행 메시지를 오류로 잘못 취급해 멈췄다. 따라서 `[2,10^8]` prime/gap 분석은 시작되지 않았다.

```text
run id: 20260823T161227Z_p006_pilot1e8
overall verdict: FAIL / ANALYSIS NOT RUN
preflight: PASS
unit tests: runner stopped before completion
approved analysis stage: NOT RUN
saved-artifact verification: NOT RUN
result directory: not created
GPU: not used
```

검토 로그:

```text
test_result/logs/run_20260823T161227Z_p006_pilot1e8.log
```

## preflight에서 확인된 것

- 고정 Python `W:\miniforge3\envs\FGKMT\python.exe` 일치
- validated record CSV 존재와 SHA-256 일치
- analysis limit `100000000`과 exact `pi(10^8)` support 확인
- NumPy·Matplotlib import 확인
- segment span `10000000` 허용 범위
- GPU 비사용, network 불필요

이것은 “실행 준비가 맞다”는 뜻이지 실제 prime stream이 계산됐다는 뜻은 아니다.

## 정확한 실패 원인

공통 runner `run_plateau_recurrence.ps1`은 다음 조건을 함께 사용한다.

```powershell
$ErrorActionPreference = 'Stop'
& $Python @Arguments 2>&1 | Tee-Object ...
```

Python `unittest -v`는 통과 중인 test 이름도 stderr에 출력한다. Windows PowerShell 5.1은 native program의 stderr를 `NativeCommandError`로 감싸고, `ErrorActionPreference=Stop` 때문에 Python exit code를 확인하기 전에 pipeline을 종료할 수 있다. 같은 호출 형태를 작은 통과 test로 재현했을 때도 첫 stderr 출력에서 exit 1로 중단됐다.

로그가 정확히

```text
[STAGE] unit-tests
```

에서 끝나고 `[PASS] unit-tests` 또는 `[STAGE] approved-analysis`가 없는 것이 이 원인과 일치한다.

## 이번 실행으로 말할 수 없는 것

- P006 단위시험이 실패했다고 말할 수 없음
- `[2,10^8]` prime count나 maximal records가 틀렸다고 말할 수 없음
- recurrence/plateau 표나 그래프 결과가 있다고 말할 수 없음
- `[2,10^9]` 또는 `[2,10^10]` 예상시간을 보정할 수 없음

## 수정 가능성

Python stderr를 PowerShell error stream에 직접 합치지 않고, `Start-Process`의 `RedirectStandardOutput`과 `RedirectStandardError`로 별도 파일에 받은 뒤 process exit code를 검사하면 해결할 수 있다. 이 방식은 정상 stderr를 로그에 보존하면서도 `NativeCommandError` 오판을 피한다.

이번 요청에서는 실패 원인과 수정 방향만 확정했으며 P006 runner를 수정하거나 실제 pilot을 재실행하지 않았다. runner patch 검증과 재실행에는 새 사용자 승인이 필요하다.

## 쉬운 설명

시험 프로그램은 “지금 몇 번째 검사를 하는 중인지”를 별도 통로로 알려 줬다. PowerShell이 그 안내문을 진짜 오류로 착각해 정지 버튼을 눌렀다. 실제 소수 계산 단계에는 아직 들어가지 않았으므로, 이번 로그만으로 P006 알고리즘의 성공이나 실패를 판단하면 안 된다.

## 2026-08-24 후속 교정

같은 BAT의 두 번째 사용자 실행 `20260823T173021Z_p006_pilot1e8`도 같은 원인으로 actual analysis 전에 중단됐다. 상세 문서는 `test_result/202608240315_P006_second_pilot_failure_analysis.md`다.

이후 P006/P007 공통 PowerShell helper로 stdout/stderr 분리 수집, 빈 줄 보존, process exit 판정, 전체 ErrorRecord 기록을 구현했다. parser, blank-line stdout/stderr, synthetic exit 7 toy self-test와 BAT approval-denial은 PASS했다. 교정판 actual P006 pilot은 아직 실행하지 않았다.
