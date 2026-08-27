# P015 — 48시간 independent research queue

## 1. 상태

`WAITING_FOR_USER_EXECUTION / ORCHESTRATION_ONLY / IMPLEMENTED / LOCALLY_VERIFIED / ACTUAL_NOT_RUN`

## 2. 목적과 비목적

P013-A, P013-B, P014를 한 번의 사용자 승인으로 47시간 이내에 순차 실행한다. queue는 child
결과를 합치거나 해석하지 않고 실행·timeout·disk·exit code만 기록한다.

- 시간을 채우기 위한 반복 없음
- 완료 실험 재실행 없음
- P010B blocked actual 없음
- child마다 독립 run id·log·manifest 유지

## 3. 순서·분기·자원

1. P013-A: timeout 4시간
2. P013-B: timeout 20시간; P013-A shared implementation failure면 BLOCKED
3. P014: timeout 22시간; P013 실패와 무관하게 계속

- global wall cap: 169,200초(47시간)
- aggregate output increase: 50,000,000,000 bytes 이하
- CPU only, GPU 금지
- child failure가 있어도 독립 child는 계속하고 queue는 마지막에 nonzero 반환

## 4. 사용자 실행 명령

환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P015_48h_research_queue.bat --confirm-48h
```

같은 child의 개별 BAT와 queue를 동시에 또는 연속 중복 실행하지 않는다.

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
- fixed order·46시간 child cap 합·47시간/50GB 거부 gate·approval gate unit tests: PASS
- PowerShell parser와 BAT usage gate: PASS
- actual queue: 미실행
