# P006 두 번째 `[2,10^8]` pilot 실행 분석 — 같은 runner 원인으로 분석 전 중단

## 판정

두 번째 사용자 실행도 P006 소수 계산 실패가 아니라 Windows PowerShell 5.1의 native stderr 처리 문제로 중단됐다. preflight까지만 PASS했고 실제 consecutive-prime 생성, plateau·recurrence 통계, 그래프, saved-artifact 검증은 전혀 실행되지 않았다.

```text
run id: 20260823T173021Z_p006_pilot1e8
overall: USER_RUN_FAILED / ANALYSIS_NOT_RUN
preflight: PASS
unit-test Python process: 시작됐으나 runner가 정상 stderr에서 중단
approved-analysis: NOT RUN
saved-artifact-verification: NOT RUN
result directory: not created
```

## 원본 로그 증거

- path: `test_result/logs/run_20260823T173021Z_p006_pilot1e8.log`
- bytes: `3150`
- SHA-256: `5B870469D3CD43EDCE6682864DEE08CBEE5996A280E4F57817016C334A3D739D`
- 마지막 stage marker: `[STAGE] unit-tests`
- 없는 marker: `[PASS] unit-tests`, `[STAGE] approved-analysis`, 전체 terminal PASS

콘솔의 `NativeCommandError`는 당시 runner가 PowerShell 오류를 log에 다시 쓰는 top-level catch를 갖지 않아 원본 log에는 남지 않았다. 사용자가 제공한 콘솔 내용과, log가 정상 unittest stderr 첫 지점에서 끊긴 모양이 첫 실행 `20260823T161227Z`과 같은 원인임을 보여 준다.

## 교정 내용

- `& python ... 2>&1 | Tee-Object` 호출을 제거했다.
- 공통 helper가 Python stdout과 stderr를 각각 임시 파일로 받고 process exit code를 별도로 판정한다.
- 정상 stderr와 빈 줄을 포함해 두 stream을 run log에 다시 기록한다.
- 비정상 exit 또는 PowerShell 예외는 stage, exit code, exception type, message, invocation, stack, 전체 ErrorRecord를 log에 기록한다.
- synthetic stderr/blank-line/exit-7 toy self-test를 추가했다.

교정판은 parser와 toy self-test까지만 통과했다. `[2,10^8]` actual pilot은 다시 실행하지 않았으므로 여전히 결과가 없다.

## 실행기 보존

당시 실행 BAT는 SHA-256 `473DDA69C89DEAEA60D30F863F0B6DAF59BCA1911ED9E39411B1B69CC6401FA0` 그대로 `test_done/run_P006_plateau_recurrence_pilot-done.bat`에 보존했다. 루트의 같은 이름 BAT는 교정된 활성판이며 아직 사용자 실행으로 확인되지 않았다.

## 쉬운 설명

두 번 모두 시험지가 틀려서 멈춘 것이 아니라, 시험 진행 안내문을 실행기가 오류로 오해해서 멈췄다. 이번에는 안내문 통로와 진짜 종료번호를 분리했다. 다만 새 실행기로 실제 소수를 계산해 본 것은 아니므로, 사용자가 새 pilot을 한 번 더 실행해야 P006 결과를 얻을 수 있다.
