# P010B — count certificate에서 실제 search acceleration으로의 연결

## 1. 상태

`PLAN_FROZEN / P010A_REPLAY_PASS / ONE_CANDIDATE_USER_RUN_READY / ACTUAL_NOT_RUN`

P010B는 P010A의 count upper bound를 실제 탐색 후보·위치로 연결하는 축이다. 핵심 질문은
“상한이 작아졌는가?”가 아니라 “실제 `gap >= 1856` start를 하나도 빠뜨리지 않는 더
싼 candidate cover가 있는가?”다.

## 2. 필수 수학 계약

다음 네 조건을 동시에 요구한다.

1. **Coverage:** 모든 실제 위험 start가 candidate family에 포함된다.
2. **Sound rejection:** 제거된 후보마다 exact factor 또는 window-prime witness가 있다.
3. **Completeness:** block boundary crossing을 포함해 `[A,B)` 전체가 덮인다.
4. **Break-even:** 생성·ledger·검증·survivor 비용 합이 동일 범위 baseline보다 작다.

정식 명제와 증명은
`docs/method/theory/10_coverage_preserving_compression_정식화.md`를 따른다.

## 3. G1 — modulus-30030 one-candidate scan

P007 modulus-2310 potential을 residue reduction으로 modulus 30030에 lift하고 모든
transition을 chunked scan한다. 이 단계는 다음만 측정한다.

- 5,760 states와 35,224,647 constraints의 누락 없는 scan 여부
- wall time과 memory-safe 작동 여부
- lifted candidate의 floating violation 수와 minimum slack

이 실행은 LP solve도, exact modulus-30030 certificate도, search acceleration 증명도
아니다. violation이 있어도 구현 실패가 아니라 lifted candidate 음성 결과일 수 있다.

### 선행조건

- P010A modulus-2310 replay terminal PASS manifest와 hash-bound saved verification report
- pinned P007 certificate hash 일치
- chunk memory estimate 1 GiB 미만
- 별도 사용자 실행 승인

2026-08-26 P010A replay는 terminal/saved exact PASS했으므로 첫 두 선행조건은 충족됐다.
이번 사용자 지시로 50 GB·16시간 이내 bounded queue 실행기도 준비한다. 실제 실행은
사용자가 confirmation flag를 주어 시작한다.

### 성공 기준

- scanned constraints 정확히 35,224,647
- saved artifact hash issue 0
- terminal PASS
- `violation_count`를 결과로 보고하되 0을 미리 요구하지 않음

### 중단 기준

- P010A manifest 불일치
- scan count 누락
- RAM 4 GB, 이 단계 disk 1 GB 또는 queue 전체 50 GB, wall time 60분 초과
- full matrix materialization 또는 LP solve 시도

## 4. 실행 절차

P010A PASS manifest 경로를 `<P010A_MANIFEST>`에 그대로 넣는다.

환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p010b\run_p010b_mod30030_one_candidate_scan.ps1 -ConfirmP010B -P010AReplayManifest '<P010A_MANIFEST>'
```

예상시간: 1–15분. 예상 RAM: 1 GB 미만. 예상 disk: 200 MB 미만.

사용자 회신:

- 마지막 `[PASS]` 또는 첫 `[FAIL]` 줄
- 실행 로그 경로
- result directory의 `manifest.json`, `summary.json`

## 5. 가속 후보 승격 기준

one-candidate scan 뒤에도 다음이 없으면 P010B는 준비 단계에 머문다.

- candidate-to-absolute-range mapping theorem
- false-negative 0의 exact verifier
- candidate 수와 certificate bytes 실측
- survivor 검증을 포함한 total cost
- 동일 CPU·범위·threshold baseline 비교

count upper bound만 줄고 이 연결이 없다면 “이론적 count 개선”으로는 의미가 있어도
prime-gap exhaustive search algorithm의 개선이라고 쓰지 않는다.

## 6. 현재 구현 범위와 보류 범위

- 구현: 5,760 states·35,224,647 constraints one-candidate full scan
- 구현: 위반 0일 때 exact modulus lift와 integer streaming 검증
- 미구현/보류: 실제 상한을 줄이는 cutting-plane solve
- 보류 이유: 먼저 full scan 시간과 exact-lift baseline을 실측해야 iteration 수와
  16시간 예산의 타당한 상한을 정할 수 있다.
