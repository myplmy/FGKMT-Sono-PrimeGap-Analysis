# P012-B holdout·P010B candidate-cover 로컬검증

## 판정

`P012A_CONTRACT_FROZEN / P012B_IMPLEMENTED / P012B_PREFLIGHT_PASS / P012B_ACTUAL_NOT_RUN / P010B_EXACT_COVER_TOY_PASS / P010B_ACCELERATION_BLOCKED / FULL_130_TESTS_PASS`

사용자가 P012-A r2 figure 두 장에 문제가 없음을 확인했다. P012-A 통계 계약을 hash로
동결하고 P012-B 독립 holdout 코드·CLI·runner를 준비했다. preflight와 toy 검증은 holdout
prime stream을 읽지 않았다. 실제 `[10^9,10^10)` P012-B는 실행하지 않았다.

P010B에는 finite coverage·exact rejection·break-even verifier를 구현했다. synthetic toy는
coverage와 soundness를 통과했지만 exhaustive truth를 써서 ledger를 만드는 순환 generator라
가속 판정은 의도대로 BLOCKED다.

## P012-A 계약 동결

- contract: `test_plan/P012_statistical_contract_v1.json`
- SHA-256: `1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`
- figure visual QA: 사용자 PASS
- 고정 항목: bin 3종, cohort 3종, primary·secondary, seed `20260827`,
  100,000 replications, LOW_INFORMATION, zero-variance, forced-first-record 규칙
- holdout: `[10^9,10^10)`, complete records `31–34`

## P012-B 구현·preflight

- plan: `test_plan/P012B_stratified-null-holdout.md`
- analysis: `source/recurrence_stratified_holdout.py`
- CLI: `source/recurrence_stratified_holdout_cli.py`
- tests: `tests/test_recurrence_stratified_holdout.py`
- runner: `scripts/experiments/p012/run_p012_stratified_null_holdout.ps1`

preflight 결과:

- contract·validated records hash: PASS
- selected record indices: `31,32,33,34`
- expected gap starts: `404,204,977`
- holdout prime stream read: false
- actual experiment executed: false

range sieve는 `[lower,upper)` prime에 오른쪽 boundary prime 하나를 붙여 마지막 gap을 닫는다.
왼쪽 continuation과 오른쪽 censored plateau는 사전 제외한다. P006/P011 개발 table은 holdout
기대값 입력으로 사용하지 않는다.

## P010B exact candidate-cover gate

- analysis: `source/candidate_cover.py`
- CLI: `source/candidate_cover_cli.py`
- tests: `tests/test_candidate_cover.py`
- synthetic runner: `scripts/experiments/p010b/run_p010b_candidate_cover_toy.ps1`
- local run: `tmp/p010b-candidate-cover/20260827T112421Z_p010b_candidate_cover_toy`
- local log: `tmp/p010b-candidate-cover/run_20260827T112421Z_p010b_candidate_cover_toy.log`
- saved manifest SHA-256:
  `8d9424975e6c63d642f3c107a05bbf68b7002340e9e3a77505755b0f6653135e`

toy `[1000,10000)`, threshold `H=20`:

| 항목 | 값 |
|---|---:|
| integer universe | 9,000 |
| exact dangerous starts | 69 |
| candidate survivors | 69 |
| rejected starts | 8,931 |
| composite factor witnesses | 7,939 |
| strict window-prime witnesses | 992 |
| uncovered/unsound issue | 0 |
| ledger bytes | 543,559 |

candidate set과 독립 전수계산 위험 start set은 정확히 일치했다. `q=c+H` rejection, 잘못된
factor, missing coverage, 비정수 JSON 값은 음성대조에서 모두 FAIL했다. disk cap은 이진
50 GiB가 아니라 사용자 제한과 같은 십진 `50,000,000,000` bytes로 검증한다.

break-even은 다음 이유로 BLOCKED다.

1. generator가 exhaustive truth를 사용함
2. benchmark가 1회뿐임
3. toy candidate total은 baseline보다 빠르지 않음; 최종 실측 speedup `0.311085`

따라서 verifier plumbing은 PASS지만 search acceleration은 미증명이다.

## 검증 명령과 결과

Python: `W:\miniforge3\envs\FGKMT\python.exe` 3.11.16

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m py_compile `
  source\recurrence_stratified_holdout.py `
  source\recurrence_stratified_holdout_cli.py `
  source\candidate_cover.py `
  source\candidate_cover_cli.py `
  tests\test_recurrence_stratified_holdout.py `
  tests\test_candidate_cover.py
```

결과: PASS

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest `
  tests.test_recurrence_stratified_holdout -v
```

정상 Windows 권한 결과: 5/5 PASS, 0.006초

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest `
  tests.test_candidate_cover -v
```

결과: 9/9 PASS

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
```

결과: 130/130 PASS, 최종 재검증 6.150초

추가 검증:

- active PowerShell parser 7/7 PASS
- P012-B `-ConfirmP012B` 누락: exit 1, actual 미실행
- P010B toy `-ConfirmToy` 누락: exit 1
- P012-B preflight: PASS, `holdout_prime_stream_read=false`
- P010B synthetic runner·saved verification: terminal PASS, issue 0

첫 P012-B unittest의 sandbox 실행은 계산 assertion 4개가 PASS한 뒤 Windows TEMP ACL cleanup에서
`PermissionError [WinError 5]`가 발생했다. 정상 Windows 권한의 동일 5개 시험은 모두 PASS해
환경 문제와 코드 결과를 분리했다.

P010B 최종 toy의 첫 sandbox runner도 같은 TEMP ACL로 unit-test stage에서 멈췄다. 이 실패
run은 덮어쓰지 않았고, 정상 Windows 권한의 새 run `20260827T112421Z`는 9/9 tests, toy,
saved verification과 terminal PASS를 모두 남겼다.

## 미실행·남은 gate

- P012-B actual holdout: NOT RUN
- P012-B figure: 생성 안 됨, 사용자 QA 대상 없음
- P010B `[10^20,10^21)` candidate generator/search: NOT RUN
- compressed large-range coverage ledger: 미구현
- large-prime PARI witness adapter와 survivor `prime-gap` 연결: 미구현
- acceleration proof: false

P010B actual 구현은 absolute generator와 compressed coverage format이 생긴 뒤 진행한다.
