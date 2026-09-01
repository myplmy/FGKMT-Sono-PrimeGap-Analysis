# P014-R3·P018-P0 사후 정본 갱신 로컬검증

최종 갱신: 2026-09-01 18:20 KST

## 1. 범위와 판정

이 검증은 사용자가 이미 완료한 P014-R3와 P018-P0의 실제 계산을 다시 실행한 것이 아니다.
결과 artifact·hash·saved verification 감사 뒤 정본 문서와 완료 실행기 이관이 코드 검증을
깨뜨리지 않았는지 확인한 로컬검증이다.

```text
P014-R3 artifact/hash/saved-serial audit = PASS
P018 primecount/P0 artifact/hash/saved-blinded audit = PASS
fixed-Python full unittest               = 197/197 PASS
Python py_compile                        = 66 files PASS
PowerShell parser                        = 12 files, 0 errors
Bash syntax                              = PASS
actual/heavy experiment in this audit    = NOT RUN
```

## 2. 전체 unittest

고정 환경:

```text
W:\miniforge3\envs\FGKMT\python.exe
```

명령:

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
```

첫 sandbox 실행은 `TemporaryDirectory` 접근·정리 권한 때문에 80개 `PermissionError`를 냈다.
이는 assertion 실패가 아니며, 같은 명령을 sandbox 외부에서 재실행해 다음을 확인했다.

```text
Ran 197 tests in 34.301s
OK
```

sandbox 실패가 남긴 접근 불가 임시 디렉터리 16개는 삭제하지 않고
`tmp/cleanup_candidates/20260901/sandbox_permission_test_artifacts_202609011817`로 격리했다.

## 3. 정적·구문 검증

- `source/`와 `scripts/common/` Python 66개: 고정 Python `py_compile` exit 0
- active PowerShell 12개: parser error 0
- 완료 P018 primecount SH:
  `bash -n test_done/prepare_p018_prefix_primecounts-20260901T044708Z-done.sh` exit 0
- compile cache는 source에 섞지 않고
  `tmp/cleanup_candidates/20260901/validation_pycache_202609011813`에 격리

## 4. 결과 정합성

- P014-R3는 실행 성공과 상한 무개선을 분리해 기록했다.
- P018-P0는 calibration 성공과 정보량 0을 분리했고 A/B gate를 통과했다고 쓰지 않았다.
- P018-A active BAT/PS1과 공통 runner/source는 유지했다.
- P014-R3·P018-P0·primecount 준비의 실제 실행 파일만 SHA-256을 보존해 `test_done`으로 이관했다.
- 문서·작업로그·handoff는 이동하지 않았다.

상세 수치 정본은 각각 `test_result/202609011805_P014R3_result_analysis.md`와
`test_result/202609011806_P018P0_result_analysis.md`다.
