# P014-R2 — modulus 510510 병렬 exact-scan actual 승격 계획

## 1. 상태와 승인 경계

`IMPLEMENTED / USER_RUN_AUTHORIZED / ACTUAL_NOT_RUN / DO_NOT_START_WHILE_P017_ACTIVE`

사용자는 P014-R2 toy 검증에 문제가 없으면 actual 승격하는 것을 승인했다. 기존 toy는 serial
정본과 worker `1/2/4/8` exact equality 및 synthetic modulus 30030의 35,224,647 constraints
무누락을 통과했다. 이 계획은 별도 revision으로 승격하며 기존 serial P014 runner를 덮어쓰지
않는다.

Codex는 actual을 실행하지 않는다. 현재 P017이 끝나고 P017 결과 감사를 마친 뒤 사용자가 한
번만 실행한다.

## 2. 연구 질문

P010A G4 modulus-30030 certificate를 modulus 510510으로 exact lift한 뒤, 92,160 source states와
8,524,288,932 constraints 전체를 8-process source-row 분할로 검사해도 다음이 유지되는가?

1. serial과 동일한 exact integer inequality
2. source row와 두 constraint family의 무누락·무중복 coverage
3. violation count, minimum integer slack, deterministic top-k의 exact reduction
4. stage-B 조건부 count-upper-bound 탐색의 기존 의미
5. 저장 certificate를 기존 serial exact oracle이 독립적으로 재검증

## 3. 비목적

- prime-gap 위치 탐색
- Rank 85→86 exhaustive coverage
- P010B search acceleration 증명
- floating tolerance로 exact arithmetic 대체
- constraint sampling 또는 생략

count upper bound가 개선돼도 candidate-cover mapping과 total-cost 개선이 별도로 증명되지 않으면
탐색 가속이라고 주장하지 않는다.

## 4. 고정 입력과 provenance

P010A G4 정본:

```text
test_result/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h
manifest SHA-256:
6f68c8f4c5356f29b23aa48025699e02887b1d396645f04e6eee96aa535080e9
certificate SHA-256:
22e345c0cae727fe60105d30a4cf99e2672c69bbf93815f02c5084c8d5805b65
saved report SHA-256:
e10a758a93343d6af8b3c82e3b86d6aa46ba2f609cd69f36dddfb32dc7f44ca7
```

고정 수학 계약:

```text
threshold = 1856  (equality 포함)
source modulus = 30030
target modulus = 510510
target states = 92160
target constraints = 8524288932
baseline total upper bound = 436001550591586306
```

## 5. 병렬 분할과 정확성 계약

- source-state index `[0,92160)`을 64-row block으로 분할한다.
- worker 8개가 각 block의 모든 target state와 small/large 두 family를 계산한다.
- signed-int64 overflow guard가 안전하지 않으면 시작 전에 중단한다.
- scanned constraint count는 exact resource estimate와 같아야 한다.
- parent reduction은 exact integer 합·최솟값·전역 tuple 정렬만 사용한다.
- worker별 native thread ceiling은 1이며 8-process oversubscription을 막는다.
- analysis의 stage-A와 final exact scan은 병렬 revision을 사용한다.
- saved full recomputation은 기존 serial `scan_exact_certificate_constraints`를 사용한다.

마지막 항목 때문에 병렬 구현과 저장 검증이 같은 코드 오류를 공유할 위험을 줄인다.

## 6. 자원 계약

```text
CPU: 4 physical cores / 8 logical processors
GPU: forbidden
exact worker processes: 8
worker native threads: 1
analysis max wall: 54000 seconds (15 hours)
stage-A optimizer gate: 14400 seconds (4 hours)
disk child cap: decimal 10 GB
RAM cap: decimal 32 GB
full constraint matrix: forbidden
working-set constraints: at most 100000
```

64-row exact block의 보수적 단일-worker working estimate를 8배한 값은 약 4.4 GiB다. 이는
32 GB 아래지만 실제 peak RAM은 actual log에서 별도로 확인한다. solver 단계도 100,000-row
working-set cap을 넘으면 중단한다.

## 7. 실행 방법

환경: Windows CMD 또는 PowerShell, 시작 경로
`Z:\FGKMT-Sono-PrimeGap-Analysis`.

P017이 terminal PASS/FAIL로 완전히 종료되고 다른 CPU-heavy 실험이 없을 때만 실행한다.

```bat
run_P014R2_mod510510_parallel_staged_certificate.bat --confirm-p014r2
```

예상시간은 약 4–20시간이다. 분석은 최대 15시간 계약이며 이후 serial saved recomputation이
추가된다. stage-A가 4시간 gate를 넘으면 stage-B optimizer는 생략하고 calibration-only 결과로
끝난다.

## 8. 진행 관찰

runner 시작 시 다음 두 파일의 정확한 경로가 main log에 기록된다.

- `*.p014r2-analysis.progress.jsonl`
- `*.p014r2-serial-verification.progress.jsonl`

PowerShell 화면이 조용하면 별도 PowerShell에서 runner가 출력한 실제 경로를 사용한다.

```powershell
Get-Content '실제_progress.jsonl_경로' -Wait
```

## 9. PASS 기준

1. prerequisite/resource preflight PASS
2. targeted unit tests PASS
3. stage-A scanned constraints `8,524,288,932`, violation 0
4. 8 worker process 관측, source rows `92,160` coverage
5. final exact scan violation 0
6. 결과 certificate와 summary bound 일치
7. original serial scanner의 saved full recomputation PASS
8. manifest artifact/source hashes PASS
9. terminal P014-R2 PASS marker 존재
10. search acceleration claim은 false

## 10. 중단·경고 기준

- 입력 hash, state/constraint count, overflow, 32 GB estimate 중 하나라도 불일치하면 시작 전 중단
- worker row overlap/gap, worker 8개 미참여, constraint count 불일치면 FAIL
- analysis가 15시간 계약을 넘기거나 disk cap을 넘기면 FAIL
- stage-A 4시간 초과만으로는 FAIL이 아니며 optimizer 생략 경고다
- serial saved recomputation 불일치는 병렬 결과를 무효로 한다
- terminal PASS 전에는 실험 PASS로 기록하지 않는다

## 11. 예상 산출물

- run별 main log와 두 progress JSONL
- resource preflight
- lifted baseline certificate
- stage-A exact report
- 조건부 iteration history와 repair report
- final exact certificate/report
- summary, manifest, serial saved-verification report

## 12. 승격 근거와 한계

승격 근거는 P014-R2 toy의 feasible/infeasible negative control, worker-count invariance,
modulus-30030 통합 exact equality다. 아직 modulus-510510 wall-time·peak RAM·memory-bandwidth
speedup은 측정하지 않았으므로 actual 완료 전에는 성능 개선을 주장하지 않는다.

