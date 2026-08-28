# P014 — modulus-510510 memory-safe staged certificate experiment

## 1. 상태

`WAIT_P013B_TERMINAL / PRE-REGISTERED / IMPLEMENTED / PYTHON_LIVE_PROGRESS_LOCALLY_VERIFIED / ACTUAL_NOT_RUN`

## 2. 연구 질문과 비목적

연구 질문:

1. P010A G4 exact certificate를 modulus 510510으로 lift한 구현이 8,524,288,932개 제약을
   32 GB 미만 streaming scan으로 exact 검증할 수 있는가?
2. stage-A 실측이 자원 gate를 통과하면 bounded working-set cutting-plane이 modulus-30030
   상한 `436001550591586306`을 더 낮출 수 있는가?
3. 큰 modulus에서 실제 병목이 scan, seed selection, LP solve, exact repair 중 무엇인가?

비목적:

- full constraint matrix를 만들지 않는다.
- `[10^20,10^21)` prime을 직접 탐색하지 않는다.
- count upper bound 개선을 search acceleration으로 부르지 않는다.
- GPU를 사용하지 않는다.

## 3. 수학 계약

`30030 | 510510`이고 G4 certificate의 `lambda>=0`이므로 potential을 residue reduction으로
복제한 exact certificate는 같은 upper bound를 유지한다. stage-A는 이 정리의 구현을 모든
target constraint에서 exact integer로 검증한다.

stage-B floating LP는 candidate 발견 도구다. 저장 best certificate는 denominator `10^15`로
rationalize·common-mu repair한 뒤 모든 target constraints를 exact signed-int64로 검사한다.
비엄격 상한은 `floor/ceil` 계약을 기존 P007/P010A와 동일하게 유지한다.

## 4. 입력·provenance

- G4 run: `test_result/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h`
- G4 manifest SHA-256:
  `6f68c8f4c5356f29b23aa48025699e02887b1d396645f04e6eee96aa535080e9`
- G4 best certificate SHA-256:
  `22e345c0cae727fe60105d30a4cf99e2672c69bbf93815f02c5084c8d5805b65`
- G4 saved verification report SHA-256:
  `e10a758a93343d6af8b3c82e3b86d6aa46ba2f609cd69f36dddfb32dc7f44ca7`
- source/target modulus: `30030 / 510510`
- threshold: `gap >= 1856`, equality 포함
- baseline exact total upper bound: `436001550591586306`

## 5. 단계와 자원 계약

### Stage A — exact lift calibration

- target states: `92,160`
- exact constraints: `8,524,288,932`
- chunk rows: `64`
- full matrix materialized: false
- exact signed-int64 overflow guard 필수
- stage-A가 4시간을 초과하면 stage-B를 자동 생략하고 calibration-only 결과로 종료

### Stage B — 조건부 cutting-plane

- seed constraints: `5,000`
- add per iteration: `5,000`
- max iterations: `12`
- max working constraints: `100,000`
- per-solve limit: `1,800`초
- analysis wall cap: `54,000`초(15시간)
- runner timeout: 22시간(saved full exact verification 포함)
- output cap: decimal 10 GB; queue aggregate cap 50 GB
- process affinity: Windows topology상 첫 물리 4코어·그에 속한 논리 8프로세서(`0xff`)
- BLAS/OpenMP/HiGHS가 사용할 수 있는 thread pool ceiling: 8
- exact streaming scan은 단일 Python stream이므로 8개를 항상 동시에 사용한다고 해석하지 않음
- 장시간 analysis와 saved exact recomputation은 Python이 별도 `*.progress.jsonl`에 START,
  phase event, 300초 heartbeat, END를 직접 `flush+fsync`한다. Windows console이 있으면
  `CONOUT$`에도 같은 `[LIVE]` 행을 즉시 표시한다. PowerShell stdout capture를 우회하므로 stage
  종료 전에도 liveness를 확인할 수 있다. heartbeat는 실제 완료율을 뜻하지 않으며 exact scan의
  START/PASS와 iteration event를 phase 증거로 함께 기록한다.

## 6. 사전검증·중단 기준

사전검증:

1. G4 manifest·best certificate·saved report hash와 exact recomputation PASS
2. target state·constraint count가 고정값과 일치
3. chunk memory estimate 1 GiB 미만
4. exact overflow upper bound가 signed-int64 limit 미만
5. approval flag 없이는 input full scan·output 생성 전 거부

중단 또는 controlled stop:

- prerequisite hash·exact G4 verification 불일치
- stage-A exact violation 또는 scan count 누락
- full matrix materialization 시도
- working set·disk·wall cap 초과
- solver candidate 없음, 새 violation 없음, 또는 stage-A time gate 초과

controlled stop은 유효한 lifted baseline certificate를 저장·exact 검증한 경우 계산 PASS일 수
있지만 strict improvement 음성 또는 optimizer-not-run으로 별도 표시한다.

## 7. 사용자 실행 명령

환경: Windows PowerShell 또는 FGKMT Conda Prompt

현재 P013-B saved full recomputation이 CPU를 사용 중이므로 P014를 동시에 시작하지 않는다.
P013-B terminal PASS/FAIL과 프로세스 종료를 확인한 뒤 아래 개별 명령만 실행한다.

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P014_mod510510_staged_certificate.bat --confirm-p014
```

전체 queue 실행 방법:

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P015_48h_research_queue.bat --confirm-48h
```

개별 실행과 queue 실행을 중복하지 않는다.

## 8. 성공 기준·산출물

- stage-A lifted certificate exact violation 0
- exact constraint count `8,524,288,932`
- terminal PASS와 saved exact recomputation PASS
- stage-B를 실행했으면 iteration checkpoint·best certificate·strict improvement 기록
- `stage_a_exact_report.json`, `iteration_history.json`, `summary.json`, `manifest.json`
- `saved_verification_report.json`, stdout/stderr log

과학적 결과는 `STRICT_BOUND_IMPROVEMENT`, `NO_IMPROVEMENT`,
`CALIBRATION_ONLY_TIME_GATE`로 분리한다. 어느 경우도 search acceleration 증명이 아니다.

## 9. 후속 작업

사용자는 terminal marker·log·result directory를 회신한다. Codex는 exact scan·manifest·resource
metrics를 감사한 뒤 modulus-510510을 계속 연구할 가치가 있는지 판단한다.

## 10. 구현·로컬검증

- analysis/CLI: `source/finite_gap_mod510510.py`, `source/finite_gap_mod510510_cli.py`
- runner: `scripts/experiments/p014/run_p014_mod510510_staged_certificate.ps1`
- root BAT: `run_P014_mod510510_staged_certificate.bat`
- G4 exact prerequisite·resource·overflow preflight: PASS
- small-modulus lift/exact-scan toy, approval gate, parser와 4 physical/8 logical resource preflight: PASS
- Python `*.progress.jsonl` fsync heartbeat·phase·failure/nonoverwrite와 P014 CLI 선승인거부 포함
  targeted 6/6 tests, full 151/151 tests, py_compile, read-only preflight, PowerShell parser·기존
  stage-logging self-test·BAT usage gate: PASS
- modulus-510510 full scan/optimizer: 미실행
