# P014-R2 실패 분석·P014-R3 및 P018 prefix 로컬검증 보고서

최종 갱신: 2026-09-01 01:34 KST

## 1. 판정 요약

| 대상 | 판정 | 핵심 의미 |
|---|---|---|
| P014-R2 사용자 실행 | `USER_RUN_FAILED_BEFORE_PREFLIGHT` | PowerShell 5.1 인수 전달 오류이며 수학 계산 실패가 아님 |
| P014-R3 | `IMPLEMENTED / LOCALLY_VERIFIED / ACTUAL_NOT_RUN` | R2 과학·자원 계약을 유지하고 transport만 교정 |
| P018 결정 | `FROZEN` | B=full-range 정식 gate, A=prefix-only 보조 gate |
| P018 P0/A | `IMPLEMENTED / LOCALLY_VERIFIED / ACTUAL_NOT_RUN` | outcome-blind margin probe와 exact dual verification 준비 |

Codex는 P014-R3 actual, P018 primecount actual, P018 P0/A actual을 실행하지 않았다.

## 2. P014-R2 실패 증거

- log: `test_result/logs/run_20260831T150343Z_p014r2_mod510510_parallel_staged_certificate.log`
- log SHA-256:
  `beb57218a5d8403686c31f925d809b2bc37a5a20daf052486b659acc3eb77f3b`
- first/last stage: `p014r2-prerequisite-resource-preflight`
- child preflight PASS: 0
- analysis constraint scan: 0
- result directory: 없음
- analysis/serial-verification progress JSONL: 없음

사용자 콘솔에는 `live_native_tee=JSONDecodeError: Expecting value: line 1 column 2`가 있었지만 기존
broker는 자기 argument decode 실패를 main log에 append하지 못했다. 따라서 원본 log에는 바깥
PowerShell의 exit-code 2만 남아 있다. 이 누락도 R3에서 교정했다.

실제 원인은 BAT가 호출한 Windows PowerShell 5.1의 native argument binder다. PowerShell helper가
문자열 배열을 JSON `[-B,-m,...]`으로 만든 뒤 raw 명령행 인수로 전달할 때 JSON 내부 큰따옴표가
제거됐다. Python broker가 받은 값은 유효한 JSON 문자열 배열이 아니므로 두 번째 문자에서
`JSONDecodeError`가 발생했다. PowerShell 7에서는 같은 인수가 보존되어 기존 toy가 이 결함을
발견하지 못했다.

실행된 R2 파일은 active 경로에서 제거하고 다음 hash로 보존했다.

| done 파일 | SHA-256 |
|---|---|
| `test_done/run_P014R2_mod510510_parallel_staged_certificate-20260831T150343Z-done.bat` | `3bb3131699c2468cd69aebdad2079eca8bf892befc0c898510283cc89f8c2c8a` |
| `test_done/run_p014r2_mod510510_parallel_staged_certificate-20260831T150343Z-done.ps1` | `ee1e91bad9626f159f4ae6c384eb810045cc659eed4622f0b9cf643e12af5b0b` |

PS1 hash는 R2 원본 log의 `runner_sha256`과 일치한다. done 파일은 실패 provenance이며 재실행하지
않는다.

## 3. P014-R3 교정과 불변성

R3는 PowerShell에서 argument array를 compressed UTF-8 JSON으로 만든 뒤 Base64 한 문자열로
전달하고, Python broker가 Base64 validation→UTF-8 decode→JSON string-array validation 순서로
복원한다. 이는 .NET process capture를 되살린 것이 아니다. 자식 프로세스 실행과 stdout/stderr
동시 drain은 계속 Python `subprocess`가 담당한다.

추가 보완:

- invalid Base64/UTF-8/JSON과 broker argument 자체 오류를 초기화된 main log에 즉시 flush
- stdout/stderr·빈 줄·traceback·정확한 child exit code를 화면과 main log에 보존
- 승인된 runner에서 Python/G4 입력 누락 검사를 logging 초기화 뒤 `try/catch`에서 수행
- helper·broker hash를 run log에 기록

R2→R3 diff에서 다음 과학·자원 인수는 모두 동일했다.

```text
modulus=510510
states=92160
constraints=8524288932
threshold=1856
row block=64
workers=8, physical/logical=4/8
analysis/stage-A/per-solve=54000/14400/1800 seconds
iterations=12, seed/add=5000, working set<=100000
disk cap=10 GB
analysis=parallel exact, saved recomputation=serial exact oracle
```

직접 read-only preflight는 target state/constraint·signed-int64 guard·4/8 topology·보수적 all-worker
scan memory 4,339.53125 MiB를 확인하고 `actual_experiment_executed=false`로 PASS했다.

## 4. P018 결정과 구현

사용자 결정은 다음과 같이 결과를 보기 전에 동결했다.

- 균형형 B: future full-range를 검토할 정식 gate
- 탐색형 A: outcome-blind prefix information probe 전용 보조 gate
- A PASS의 최대 의미: `REVIEW_BALANCED_B_DESIGN`
- P0: 한 plateau runtime·정보밀도 calibration만 수행하며 gate 판정 불가

범위는 gap-start half-open 구간이다.

| 모드 | 범위 | 완결 record | dual segments | 예상시간·limit |
|---|---|---|---|---|
| P0 | `[1346294310749,1408695493610)` | 51 | 16/17 | 30–60분, 2시간 |
| A | `[10^12,1968188556462)` | 51,52 | 64/65 | 7–10시간, 12시간 |

strict `next_start<U`를 위해 마지막 next-record start 한 개가 population/control에 포함된다. 이는
선택 plateau exposure에 포함되지 않고, 더 큰 새 record gap이므로 선택된 이전 gap의 conditioned
count에도 들어가지 않는다.

구현 안전장치:

- WSL primecount Gourdon·Deleglise–Rivat의 각 endpoint raw output·값·hash를 모두 보존
- `pi(U-1)-pi(L-1)`와 두 알고리즘 일치값을 exact gap-start count로 사용
- 서로소 두 partition이 전체 range를 각각 완전 계산하고 모든 integer statistics exact equality
- gate는 population/gap-count/exposure만 읽음
- 관측 recurrence, p/q/z, 관측 통계 digest를 저장하지 않음
- raw blinded margin을 저장하고 saved verifier가 margin→components→gate를 새로 생성
- 실행 중 input/evidence/scientific-source hash 변화 시 결과 저장 전 FAIL
- Windows process tree 31.5 GB Job Object limit, free disk 5 GB gate, P0/A named mutex
- WSL 30,000,000 KiB virtual-memory limit과 확인된 4 physical/8 logical `taskset`
- deadline 도달 시 queued future 취소; 실행 중 최대 8 segment 안전 회수 뒤 partial 폐기

Poisson event probability와 power는 필드명에 `poisson_proxy`를 명시했으며 formal
stratified-hypergeometric power나 hypothesis test로 쓰지 않는다.

## 5. 검증 결과

고정 환경: `W:\miniforge3\envs\FGKMT\python.exe`.

- P014/P018 targeted 최종: 25/25 PASS, 13.134초
- 전체 unittest 최종 재실행: 197/197 PASS, 28.263초
- Windows PowerShell 5.1 quote/space/backslash/한글 argv exact round-trip: PASS
- Windows Job Object 31.5 GB isolated-child 적용: PASS
- P018 blinded margin 변조 검출 negative control: PASS
- A gate PASS/HOLD 경계·positive-variance informative expectation 분리: PASS
- expired deadline fail-fast: PASS
- active PowerShell parser: 14/14 PASS
- changed Python files `py_compile`: PASS
- P018 WSL helper `bash -n`: PASS
- WSL topology: 8 physical cores/16 logical processors가 2-thread/core로 노출됨; 선택 0–7은
  physical core 0–3의 logical 8개
- P014-R3/P018 BAT 승인 flag 누락: 각 exit 1, log count 변화 0
- `git diff --check`: whitespace error 0; line-ending 안내만 존재
- P018 frozen contract SHA-256:
  `7171efef2659340e240993a384f5dfdfb1b5d60c1b1ab20880aa2129317b0f92`

최초 targeted/full 시도의 sandbox `PermissionError`는 Windows Temp와 multiprocessing Pipe 접근이
코드 진입 전에 거부된 환경 문제였다. 사용자가 기존에 허가한 sandbox 외부의 동일 FGKMT 명령은
각각 PASS했으므로 코드 회귀로 분류하지 않는다. WSL 첫 `lscpu` 시도의 실패는 PowerShell에서
쉼표 인수를 인용하지 않은 parser 오류였고, 인용 후 read-only 재실행은 PASS했다.
최종 `bash -n` 재확인의 첫 시도도 sandbox가 WSL service를 `E_ACCESSDENIED`로 차단했으나,
동일한 읽기 전용 명령을 sandbox 외부에서 재실행해 exit 0으로 PASS했다.

## 6. 해석과 남은 한계

- P014-R2 실패는 modulus-510510 이론·certificate·병렬 scanner의 반례가 아니다.
- P014-R3는 transport와 로컬 검증이 끝났을 뿐 count bound actual 결과가 없다.
- P018 dual partition은 partition/boundary/merge 오류를 강하게 검출하지만 sieve/accumulator kernel을
  공유한다. 독립 수학 증명은 아니며 exact endpoint primecount가 필수다.
- A gate는 정보가 충분한지 묻는 계산가치 gate다. recurrence 가설을 검정하지 않는다.
- P018 saved verifier는 full prime range를 세 번째로 계산하지 않는다. 두 full pass가 actual 단계의
  exact cross-check이고 saved 단계는 copied provenance와 blinded margin을 재계산한다.
- 실제 wall time·peak job memory·P014 bound·P018 정보량은 사용자 actual 뒤에만 보고할 수 있다.
