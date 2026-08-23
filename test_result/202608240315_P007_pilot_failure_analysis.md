# P007 certificate pilot 실행 분석 — certificate audit 전 로그 복사 오류

## 판정

P007 preflight는 PASS했고 전체 unit-test Python process도 exit code 0으로 끝났다. 그러나 당시 PowerShell runner가 unittest stderr의 정상적인 빈 줄을 `Write-RunLine`에 전달하면서 빈 문자열 parameter binding 오류가 발생했다. 따라서 supplied 2310 certificate audit, 결과 저장, saved-artifact verification은 시작되지 않았다.

```text
run id: 20260823T173316Z_p007_pilot
overall: USER_RUN_FAILED / CERTIFICATE_AUDIT_NOT_RUN
preflight: PASS
unit-test Python process: exit 0
runner unit-test log copy: FAIL on empty line
approved-supplied-certificate-audit: NOT RUN
saved-artifact-verification: NOT RUN
result directory: not created
actual prime search: NOT RUN
```

## 원본 로그 증거

- path: `test_result/logs/run_20260823T173316Z_p007_pilot.log`
- bytes: `13448`
- SHA-256: `2E0E831DF50361F965EF22E95594ADB80BFF7E5173670366FCA8FD5EE76F8C1B`
- 마지막 stage marker: `[STAGE] unit-tests`
- log tail: 61-test 과정의 마지막 test까지 `... ok`
- 없는 marker: `[PASS] unit-tests`, `[STAGE] approved-supplied-certificate-audit`, 전체 terminal PASS

사용자 콘솔의 핵심 오류는 다음이었다.

```text
Copy-CapturedOutput : 'Message' 매개 변수가 빈 문자열이므로
인수를 해당 매개 변수에 바인딩할 수 없습니다.
```

이 예외 자체는 old runner에 top-level catch가 없어 log에 기록되지 않았다.

## 교정 내용

- `Write-RunLine`과 block prefix가 빈 문자열을 허용하게 했다.
- `ReadAllLines`로 stdout/stderr의 빈 줄을 보존한다.
- 공통 stage helper와 top-level catch를 P006/P007이 함께 사용한다.
- Python traceback, nonzero exit, PowerShell exception의 전체 ErrorRecord가 같은 run log에 들어간다.
- 정상 stdout/stderr 빈 줄과 synthetic exit 7을 재현하는 toy self-test를 추가했다.

교정판 actual certificate pilot은 실행하지 않았다. 따라서 제공 certificate에 관한 기존 exact 값은 코드 사전검증·제공 자료 검토에서 나온 값이지 이 failed pilot이 새로 만든 결과가 아니다.

## 실행기 보존

당시 실행 BAT는 SHA-256 `459E5363566EFC04CB82783C12607135A05BD5F05F090A62C21A4180B9A90C71` 그대로 `test_done/run_P007_finite_gap_certificate_pilot-done.bat`에 보존했다. 루트 활성 BAT는 전체 오류 로그 교정판이며 아직 사용자 실행으로 확인되지 않았다.

## 쉬운 설명

61개 검사는 실제로 모두 끝났지만, 실행기가 검사 출력 사이의 빈 줄을 파일에 옮기다가 “빈 글자는 받을 수 없다”고 스스로 오류를 냈다. 그래서 우리가 확인하려던 2310 인증서 검사는 아직 시작하지 못했다. 빈 줄도 정상 로그로 받도록 고쳤지만, 새 pilot을 다시 실행해야 정식 P007 실행 결과가 생긴다.
