# P005·P006·P007 실행기 교정 로컬 검증

## 판정

`LOCALLY_VERIFIED / ACTUAL_EXPERIMENT_NOT_RUN`

P006의 정상 stderr 오판, P007의 빈 줄 바인딩 오류, P005의 SQLite 미초기화와 실패 상태 미기록을 교정했다. 실제 P005 calibration, P006 `[2,10^8]` analysis, P007 certificate audit/full은 실행하지 않았다.

## 검증 환경

- 시간: 2026-08-24 03:29 KST
- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- WSL: Ubuntu
- GPU: 사용하지 않음
- network download/clone: 수행하지 않음

## PowerShell 로깅 검증

다음 네 파일의 Windows PowerShell parser가 issue 0으로 PASS했다.

- `scripts/powershell_stage_logging.ps1`
- `scripts/test_powershell_stage_logging.ps1`
- `run_plateau_recurrence.ps1`
- `run_finite_gap_certificate.ps1`

toy self-test 결과:

- 정상 stdout 앞/빈 줄/뒤 보존
- 정상 stderr 앞/빈 줄/뒤 보존
- synthetic stderr 보존
- synthetic exit code 7을 stage 실패로 변환
- exception type, message, category, invocation, stack, 전체 ErrorRecord 보존
- terminal marker: `POWERSHELL_STAGE_LOGGING_SELFTEST_PASS`

## Python 검증

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m py_compile source\finite_gap_certificate.py source\finite_gap_certificate_cli.py source\plateau_recurrence.py source\plateau_recurrence_cli.py tests\test_finite_gap_certificate.py tests\test_plateau_recurrence.py
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
```

결과:

```text
py_compile: PASS
Ran 61 tests in 4.411s
OK
```

여기에는 supplied modulus-2310 certificate exact verification, P006 toy segmented sieve/plateau, actual approval gate가 포함된다. 이는 실제 pilot 결과를 만들지 않는 로컬 시험이다.

## WSL·SQLite 검증

- `scripts/run_prime_gap_cpu_calibration.sh`: `bash -n` PASS
- `run_P005_prime_gap_cpu_calibration.sh`: `bash -n` PASS
- `scripts/test_prime_gap_sqlite_schema.sh`: `bash -n` PASS
- 기존 pinned upstream `schema.sql`을 임시 `/tmp` DB에 적용: PASS
- 확인 table: `m_stats`, `range`, `range_stats`, `result`

실제 helper는 root log가 이미 열려 있으면 그 log를 상속하고, 아니면 직접 stdout/stderr tee를 만든다. run root 생성 후 ERR/EXIT trap을 설치해 실패 stage·exit·command/line과 partial hash를 `manifest.failed.txt`에 쓰도록 했다. 이 failure manifest 경로는 정적·parser 검증됐으며 실제 실패 run에서의 생성 여부는 다음 사용자 실행 때 확인한다.

## 승인 거부 검증

승인 flag 없이 다음 세 활성 실행기를 호출했다.

- P006 pilot BAT: usage 출력, exit 1
- P007 pilot BAT: usage 출력, exit 1
- P005 WSL launcher: usage 출력, exit 1

세 경우 모두 actual 계산을 시작하지 않았다.

## BAT provenance

실행 당시 원본:

- `test_done/run_P006_plateau_recurrence_pilot-done.bat`: SHA-256 `473DDA69C89DEAEA60D30F863F0B6DAF59BCA1911ED9E39411B1B69CC6401FA0`
- `test_done/run_P007_finite_gap_certificate_pilot-done.bat`: SHA-256 `459E5363566EFC04CB82783C12607135A05BD5F05F090A62C21A4180B9A90C71`

교정된 활성판:

- `run_P006_plateau_recurrence_pilot.bat`: SHA-256 `6527806481AAB168D1143EA37FAF59815D19BECD07CB04BDD365FA3CAF0F5FDE`
- `run_P007_finite_gap_certificate_pilot.bat`: SHA-256 `7BC4524C945C4081EA93F1D50BB8E8FD3D8457F30F32703609F3504BA5A952EC`

활성판은 아직 사용자가 actual flag로 실행하지 않았다.

## 기타 정합성

- `ai_dev_tool/project_reference/project_static.json`: JSON parse와 `test_done/`·workflow 경로 PASS
- `git diff --check`: PASS
- 그래프 생성: 없음
- 사용자 시각검사: 필요 없음
- commit/push/PR: 수행하지 않음

## 다음 gate

1. P006 교정판 pilot을 사용자 실행하고 새 log·manifest·figure를 감사한다.
2. P007 교정판 pilot을 사용자 실행하고 exact certificate saved artifact를 감사한다.
3. P005 교정판 WSL calibration을 사용자 실행하고 SQLite table marker, official 두 MD5, failure/success manifest를 감사한다.

각 actual 실행은 서로 독립이며, 사용자가 해당 명령을 직접 실행하기 전에는 결과 상태를 PASS로 올리지 않는다.
