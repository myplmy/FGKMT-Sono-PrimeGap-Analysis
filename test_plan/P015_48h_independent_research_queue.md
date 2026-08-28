# P015 — 48시간 independent research queue

## 1. 상태

`DO_NOT_START / PARTIALLY_SUPERSEDED_BY_INDIVIDUAL_P013_RUNS / ORCHESTRATION_ONLY / ACTUAL_NOT_RUN`

## 2. 목적과 비목적

P013-A, P013-B, P014를 한 번의 사용자 승인으로 47시간 이내에 순차 실행한다. queue는 child
결과를 합치거나 해석하지 않고 실행·timeout·disk·exit code만 기록한다.

- 시간을 채우기 위한 반복 없음
- 완료 실험 재실행 없음
- P010B blocked actual 없음
- child마다 독립 run id·log·manifest 유지

## 3. 순서·분기·자원

1. P013-A r2: timeout 4시간
2. P013-B: timeout 20시간; P013-A shared implementation failure면 BLOCKED
3. P014: timeout 22시간; P013 실패와 무관하게 계속

- global wall cap: 169,200초(47시간)
- aggregate output increase: 50,000,000,000 bytes 이하
- CPU only, GPU 금지
- P013/P014 child는 각각 topology-aware 물리 4코어·논리 8프로세서 예산을 적용
- child failure가 있어도 독립 child는 계속하고 queue는 마지막에 nonzero 반환

## 4. 사용자 실행 명령

P013-A r2는 개별 실행으로 완료됐고 P013-B도 개별 실행 중이다. 지금 queue를 실행하면 같은
child를 중복 실행하므로 **현재 P015 명령은 실행 금지**다. P013-B가 끝난 뒤 P014는 개별 BAT로
실행한다. 아래 명령은 최초 계획의 재현 기록으로만 보존한다.

환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P015_48h_research_queue.bat --confirm-48h
```

같은 child의 개별 BAT와 queue를 동시에 또는 연속 중복 실행하지 않는다.

개별 실행을 선택하는 경우의 대체 명령:

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P013A_recurrence_extension_1e11_r2.bat --confirm-p013a
# 위 명령이 terminal PASS일 때만 다음 P013-B 실행
.\run_P013B_recurrence_extension_1e12.bat --confirm-p013b
# P014는 P013과 수학적으로 독립이므로 별도 실행 가능
.\run_P014_mod510510_staged_certificate.bat --confirm-p014
```

## 5. 성공·중단 기준과 산출물

- 각 child terminal marker·result directory 기록
- queue `events.jsonl`, `summary.json`, `manifest.json`
- global wall/disk gate 위반 시 실행 중 child process tree 종료
- queue PASS는 실행 orchestration 성공이며 child의 과학 결론을 대신하지 않음
- child FAIL/BLOCKED가 하나라도 있으면 queue exit nonzero

사용자는 queue 마지막 PASS/FAIL, queue log, queue result directory, 각 child 마지막 marker와
figure 시각 QA를 회신한다.

## 6. 구현·로컬검증

- queue/CLI: `source/independent_research_queue.py`,
  `source/independent_research_queue_cli.py`
- runner: `scripts/experiments/p015/run_p015_48h_research_queue.ps1`
- root BAT: `run_P015_48h_research_queue.bat`
- fixed order(P013-A r2 경로)·46시간 child cap 합·47시간/50GB 거부 gate·approval gate unit tests: PASS
- PowerShell parser와 BAT usage gate: PASS
- actual queue: 미실행
