# P014-R3 — PowerShell 5.1 transport 교정 후 modulus 510510 actual 재시도 계획

최종 갱신: 2026-09-01 KST

## 1. 상태와 승인 경계

`EXPERIMENT_PASS / EXACT_FINITE / SCIENTIFIC_NO_IMPROVEMENT / SEARCH_ACCELERATION_NOT_PROVED`

P014-R2 actual은 수학 계산 전에 Windows PowerShell 5.1이 raw JSON 인수의 큰따옴표를 제거해
Python live broker가 `JSONDecodeError`로 종료됐다. R3는 UTF-8 JSON을 Base64 한 문자열로
운반하도록 로깅 경계만 교정한다. 사용자가 승인한 P014 actual 재시도 범위 안에서 준비했으며
Codex는 actual을 실행하지 않는다.

## 2. R2 실패 증거와 R3 변경 범위

- R2 log: `test_result/logs/run_20260831T150343Z_p014r2_mod510510_parallel_staged_certificate.log`
- log SHA-256: `beb57218a5d8403686c31f925d809b2bc37a5a20daf052486b659acc3eb77f3b`
- 마지막 stage: `p014r2-prerequisite-resource-preflight`
- preflight/certificate constraint scan/result directory/progress log: 모두 시작 또는 생성 0
- R2 BAT/PS1: 원본 hash를 유지해 `test_done/*-20260831T150343Z-done`으로 이관

R3 변경은 다음 셋뿐이다.

1. PowerShell: argument array → compressed UTF-8 JSON → Base64 한 argv
2. Python broker: validated Base64 → UTF-8 → JSON string array 복원
3. broker 자체 decode/validation 실패도 이미 초기화된 main log에 즉시 append·flush

modulus·state·constraint·threshold·parallel exact scan·serial saved oracle·시간·RAM·disk 계약은
R2와 같다.

## 3. 연구 질문과 비목적

P010A G4 modulus-30030 certificate를 modulus 510510으로 exact lift하여 92,160 source states와
8,524,288,932 constraints 전부를 8-process로 검사할 때 exact count upper bound를 유지하거나
개선할 수 있는지 측정한다.

다음은 이 실험이 증명하지 않는다.

- prime-gap 위치 또는 Rank 85→86 exhaustive coverage
- P010B search acceleration
- constraint sampling으로 얻은 근사 certificate
- FGKMT/Sono 정리

## 4. 고정 입력·수학 계약

```text
G4 input: test_result/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h
threshold: 1856 (equality 포함)
source modulus: 30030
target modulus: 510510
target states: 92160
target constraints: 8524288932
baseline total upper bound: 436001550591586306
source-row block: 64
```

모든 source row와 small/large 두 constraint family를 생략 없이 exact integer arithmetic으로
계산한다. parent는 정수 합·minimum slack·deterministic top-k만 병합한다. 저장 결과는 기존 serial
scanner가 전 범위를 다시 계산해 검증한다.

## 5. 자원·진행 계약

```text
CPU: 4 physical cores / 8 logical processors
exact worker processes: 8
worker native threads: 1
GPU: forbidden
analysis max wall: 54000 seconds
stage-A optimizer gate: 14400 seconds
per solve: 1800 seconds
max iterations: 12
working-set constraints: <=100000
RAM: <32 GB
disk child cap: decimal 10 GB
full constraint matrix materialization: forbidden
```

stdout/stderr는 Python broker가 현재 PowerShell 화면과 main log에 즉시 기록한다. analysis와
serial verification은 각자 5분 heartbeat progress JSONL을 쓴다. 승인 후 필수 입력 누락도 logging
초기화 뒤 `try/catch`에서 main log에 남긴다.

## 6. 사전검증·PASS·중단 기준

사전검증:

1. Windows PowerShell 5.1 quote/space/backslash/한글 argv exact round-trip
2. invalid Base64/JSON은 exit 2이며 main log에 원인 보존
3. R2→R3 과학·자원 인수 동일성
4. 고정 FGKMT Python, G4 manifest/certificate/saved report, resource preflight
5. 승인 플래그 누락 시 exit 1이고 log/result 생성 0

actual PASS는 다음을 모두 요구한다.

1. terminal P014-R3 PASS
2. stage-A/final scanned constraints `8,524,288,932`, violation 0
3. source rows `92,160`, worker 8, 무누락·무중복 coverage
4. certificate/summary bound exact equality
5. serial saved full recomputation·manifest/artifact/source hash PASS
6. `search_acceleration_proved=false`

입력 hash·overflow·coverage·constraint count·RAM/disk·serial oracle 중 하나라도 어긋나면 FAIL이다.
stage-A 4시간 초과만은 optimizer 생략 경고이며 exact calibration 결과를 별도 표시한다. terminal
PASS 전에는 실험 PASS로 기록하지 않는다.

## 7. 사용자 실행 방법

환경: Windows CMD 또는 PowerShell. 시작 경로:
`Z:\FGKMT-Sono-PrimeGap-Analysis`.

다른 CPU-heavy 실험과 동시에 실행하지 않는다.

```bat
run_P014R3_mod510510_parallel_staged_certificate.bat --confirm-p014r3
```

- 예상시간: 약 4–20시간
- 정상 marker: `[PASS] P014-R3 launcher completed.`
- 회신: terminal PASS/FAIL, `[RUN] result_directory=...`, `[RUN] log=...`, 대략 실행시간과 관찰 peak RAM

## 8. 예상 산출물과 해석 제한

- run별 main log, analysis/serial-verification progress JSONL
- resource preflight, lifted baseline, stage-A/final exact report와 certificate
- 조건부 iteration/repair report, summary, manifest, saved verification

R3 결과가 count upper bound를 낮춰도 candidate 위치를 빠짐없이 덮는 mapping과 총 계산비용 감소가
별도로 증명되지 않으면 search acceleration이라고 부르지 않는다.

## 9. 실행 후 상태 기록 — 2026-09-01

계획·gate는 실행 결과를 본 뒤 소급 변경하지 않았다. 아래는 별도 사후 상태 기록이다.

- actual log:
  `test_result/logs/run_20260901T042740Z_p014r3_mod510510_parallel_staged_certificate.log`
- result:
  `test_result/run_20260901T042740Z_p014r3_mod510510_parallel_staged_certificate`
- 정본 분석:
  `test_result/202609011805_P014R3_result_analysis.md`
- terminal·targeted tests·parallel scan·saved full serial recomputation: PASS
- states/constraints/violations: `92,160 / 8,524,288,932 / 0`
- final upper bound: `436001550591586306`, G4 baseline과 동일
- optimizer: 첫 5,000-constraint LP가 `Unbounded`, candidate 생성 0
- 판정: 실행·유한검증 PASS, strict improvement 없음, search acceleration 미증명
- analysis부터 saved serial 종료까지 약 845.4초; 짧은 시간은 첫 solve 조기종료를 포함하므로
  12회 bounded optimization을 완료했다는 뜻이 아님
- 완료 실행기:
  `test_done/run_P014R3_mod510510_parallel_staged_certificate-20260901T042740Z-done.bat`,
  `test_done/run_p014r3_mod510510_parallel_staged_certificate-20260901T042740Z-done.ps1`

다음 revision은 5,000개 seed set의 boundedness를 보장하는 조건을 이론·toy에서 먼저 검증한 뒤에만
설계한다. R3 actual을 같은 입력으로 다시 실행할 필요는 없다.
