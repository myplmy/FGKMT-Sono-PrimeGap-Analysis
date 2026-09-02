# P018-A — P013 recurrence prefix 정보율 probe

최종 갱신: 2026-09-01 KST

## 1. 상태

`PRIMECOUNT_AND_P0_EXPERIMENT_PASS / GATE_CONTRACT_FROZEN / P018A_USER_RUN_AUTHORIZED / P018A_ACTUAL_NOT_RUN`

사용자는 2026-09-01 full-range 판정에는 균형형 B, prefix-only 보조 판정에는 탐색형 A를
승인했다. exact prime-count 준비와 P0 calibration은 완료·감사됐고 A의 endpoint·gate는 변경하지
않았다. P018-A actual은 사용자가 승인 플래그를 넣어 직접 실행한다.

## 2. 연구 질문과 비목적

질문은 다음 P013 full range를 수십 시간 계산하기 전에, 미리 고정한 prefix가 recurrence null의
기대 정보량·양의 분산 row·LOW_INFORMATION 비율을 얼마나 생산하는지 측정할 수 있는가이다.

비목적:

- recurrence enrichment의 통계검정
- p/q/z 계산 또는 가설의 참·거짓 판정
- prefix PASS만으로 full sweep 자동 실행
- FGKMT/Sono 정리, maximal-gap completeness 또는 탐색 가속 증명

## 3. 수학 정의와 정본 gate

본 실험은 canonical end-bounded `G(x)`와 iterated-log `F/H`를 변경하지 않는다. recurrence
정보량은 각 고정 plateau와 log-bin에서 관측 recurrence를 제외한 세 margin만 사용한다.

```text
population = bin 안의 전체 gap-start 수 - forced record
conditioned = 해당 record gap 크기의 전체 수 - forced record
exposure = 해당 plateau 안의 gap-start 수 - forced record
expected = exposure * conditioned / population
```

기대값과 분산은 exact finite-population hypergeometric margin 식을 사용한다. 다만
`P(X>=1)=1-exp(-lambda)`와 power는 exact family probability가 아니라 이름에
`poisson_proxy`를 붙인 계산가치 선별용 근사다. `exposure_equal_counts`, 관측 `C`, p/q/z는 gate
코드가 읽지 않으며 관측 통계에 의존하는 digest도 결과에 저장하지 않는다.

탐색형 A:

```text
alpha=0.05
P(null recurrence >= 1)>=0.25
positive-variance rows>=2
LOW_INFORMATION fraction<=0.75
effect=5x, Poisson planning power>=0.60
```

A PASS의 최대 의미는 `REVIEW_BALANCED_B_DESIGN`이다. full-range 승격은 균형형 B의 별도 계약과
사용자 승인 없이는 금지한다.

## 4. dataset·provenance·완전성

- validated records:
  `datas/validated/prime-gap-list-project/1a112a1387052d9ad360686313f501c01fe46b68/maximal_gap_records.csv`
- source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- records SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- verified exhaustive limit: `10^20`
- prefix gap-start count: WSL `primecount` Gourdon·Deleglise–Rivat의
  `pi(U-1)-pi(L-1)` exact 일치값

새 외부 maximal-gap dataset을 취득하지 않는다.

## 5. 입력 범위와 record 복원 규칙

정본 contract는 `test_plan/P018_prefix_information_probe_contract_v1.json`이다.

| 모드 | half-open gap-start 범위 | 완결 record | 용도 | 예상시간 |
|---|---|---|---|---:|
| P0 | `[1,346,294,310,749, 1,408,695,493,610)` | 51 | 1-row 속도·정보밀도 진단만 | 30–60분 |
| A | `[1,000,000,000,000, 1,968,188,556,462)` | 51, 52 | 탐색형 A gate 정본 | 7–10시간 |
| B reference | `[1,000,000,000,000, 2,614,941,710,600)` | 51–53 | 향후 설계 참고만 | 12–16시간 |

완결 조건은 `record_start>=L and next_record_start<U`다. 따라서 next record start를 실제 범위에
한 정수 포함시키도록 `U=next_record_start+1`로 고정했다. 이 마지막 gap-start 한 개는 전체
population/control에는 포함되지만 앞 plateau exposure에는 포함되지 않는다. 그 gap은 새로운 더 큰
record라서 선택된 이전 gap 크기의 conditioned count에도 들어가지 않는다. 오른쪽 censored plateau는
분석 row에서 제외된다.

## 6. 사전검증과 중단조건

1. contract·records·primecount CSV·metadata hash 일치
2. 두 primecount 알고리즘의 각 endpoint 결과 일치
3. exact gap count가 `pi(U-1)-pi(L-1)`와 일치
4. 예상 complete record index가 exact match
5. primary/verifier segment 수가 서로소이며 경계 집합이 다름
6. 두 full parallel pass의 모든 정수 sufficient statistics exact equality
7. 모든 adjacent boundary prime 일치, worker 8개 관측, native thread 1
8. RAM 32 GB 미만, 결과 5 GB 이하, GPU 미사용
9. P0 2시간·A 12시간 hard wall, hash/count/timeout 불일치 시 FAIL/HOLD
   - deadline 도달 시 아직 시작하지 않은 segment future를 취소한다.
   - 이미 실행 중인 최대 8개 worker는 현재 segment를 안전하게 닫은 뒤 종료하므로,
     실제 프로세스 회수 시각은 한 segment 시간만큼 늦을 수 있다. 부분 결과는 PASS로 채택하지 않는다.
10. 결과값을 보고 endpoint·gate·중단조건을 바꾸지 않음

Windows 분석은 31.5 GB Job Object process-tree ceiling을 걸어 worker도 같은 제한을 상속한다.
WSL primecount는 30,000,000 KiB `ulimit -v`와 topology에서 확인한 물리 4코어·논리 8CPU
`taskset`을 함께 적용한다. P0/A는 named mutex로 동시 실행을 거부하며, 시작 시 여유 disk가 5 GB
미만이면 계산 전에 중단한다.

## 7. 사용자 실행 절차

### 7.1 완료 — WSL exact prime-count 준비

환경: WSL Ubuntu. 시작 경로:

2026-09-01 실행·감사 완료다. `READY.txt`, CSV, metadata, metrics, 각 endpoint의
Gourdon·Deleglise–Rivat 원시 출력과 hash manifest가 보존되어 있으므로 다시 실행하지 않는다.
완료 SH는
`test_done/prepare_p018_prefix_primecounts-20260901T044708Z-done.sh`로 이관했다.

### 7.2 완료 — P0 개별 실행

환경: Windows CMD 또는 PowerShell. 시작 경로: `Z:\FGKMT-Sono-PrimeGap-Analysis`.

2026-09-01 약 32분 49초에 완료·감사됐다. P0는 A gate를 판정하지 않았으며 결과는
`CALIBRATION_ONLY_NO_GATE`다. 완료 BAT/PS1은 각각
`test_done/run_P018P0_prefix_information_calibration-20260901T044856Z-done.bat`와
`test_done/run_p018p0_prefix_information_calibration-20260901T044856Z-done.ps1`로 이관했다.

### 7.3 A 개별 실행

P0 결과를 보고 endpoint나 gate를 바꾸지 않는다. P0 감사 후 사용자가 별도로 실행한다.

```bat
run_P018A_prefix_information_probe.bat --confirm-p018a-prefix
```

예상 7–10시간, hard wall 12시간이다. P0와 A를 동시에 실행하지 않는다.

## 8. 예상 산출물

- copied frozen contract·records·primecount CSV/metadata
- copied primecount 준비 log·원시 알고리즘별 출력·evidence hash manifest
- `blinded_margin_statistics.json` (`populations/gap_counts/exposure_counts`만 저장)
- `blinded_information_components.json`
- `prefix_gate_report.json`
- `dual_partition_verification.json`
- `summary.json`, `manifest.json`, `saved_verification_report.json`
- main log와 5분 progress JSONL

saved verifier는 copied record/range와 exact count를 다시 대조하고, 저장 margin에서 components와
gate를 새로 생성해 exact equality를 확인한다. gate가 기존 components를 그대로 믿는 방식은
사용하지 않는다.

figure와 관측 recurrence/p/q/z 표는 만들지 않는다.

## 9. 판정과 해석 제한

- P0 PASS: 실행·exact cross-check·blinding이 정상이라는 뜻뿐이다.
- A HOLD: recurrence 가설 기각이 아니라 prefix 정보가 부족하다는 뜻이다.
- A PASS: 균형형 B 설계를 검토할 수 있다는 뜻뿐이며 full range 자동 승격이 아니다.
- `lambda/10^9 gap starts`와 `lambda/wall-hour`는 관측 기술량이다. 선형 외삽이나 CPU 배수로
  사용하지 않는다.
- 두 병렬 pass는 sieve/accumulator kernel을 공유하므로 독립 수학 oracle이 아니다.

## 10. 후속 작업

1. endpoint·gate 불변 상태로 A를 사용자 PC에서 개별 실행
2. A 결과를 감사한 뒤에만 B 설계 검토
3. B reference runner, P019 actual, P013-C full은 자동 생성·실행하지 않음

## 11. P0 실행 후 상태 기록 — 2026-09-01

계획·endpoint·gate는 실행 결과를 본 뒤 소급 변경하지 않았다. 아래는 별도 사후 상태 기록이다.

- exact-count log:
  `test_result/logs/run_20260901T044708Z_p018_prefix_primecount_prepare.log`
- count evidence:
  `tmp/p018-prefix-primecounts/20260901T044708Z_p018_prefix_primecount_prepare`
- P0 log:
  `test_result/logs/run_20260901T044856Z_p018p0_prefix_information_calibration.log`
- P0 result:
  `test_result/run_20260901T044856Z_p018p0_prefix_information_calibration`
- 정본 분석:
  `test_result/202609011806_P018P0_result_analysis.md`
- P0/A 네 endpoint의 Gourdon·Deleglise–Rivat primecount: exact 일치
- P0 exact gap starts: `2,232,503,547`
- A 고정 exact gap starts: `34,570,543,382`
- P0 16/17 서로소 dual partition·saved blinded recomputation: PASS
- forced record 제거 뒤 gap 582 conditioned count·expected·variance: 모두 0
- P0 판정: `EXPERIMENT_PASS / CALIBRATION_ONLY_NO_GATE`
- 관측 recurrence·p/q/z 저장과 hypothesis test: 수행하지 않음
- P0 실측 단순 외삽 A 계획값: 약 8.47시간; 보장값이 아니므로 12시간 hard wall 유지

P018-A의 기술적 선결조건은 충족됐다. WSL 준비와 P0를 반복하지 않고 7.3의 A 명령만 사용한다.

## 12. P018-A 실행 후 상태 기록 — 2026-09-02

계획·endpoint·gate·중단조건은 결과를 본 뒤 소급 변경하지 않았다. 1절의 상태는 실행 전 동결
상태를 보존하며, 현재 사후 판정은 아래와 같다.

- 실행 ID: `20260901T125849Z_p018a_prefix_information_probe`
- log:
  `test_result/logs/run_20260901T125849Z_p018a_prefix_information_probe.log`
- result:
  `test_result/run_20260901T125849Z_p018a_prefix_information_probe`
- 정본 분석:
  `test_result/202609021000_P018A_result_analysis.md`
- terminal·25 targeted tests·64/65 dual partition·saved blinded recomputation: PASS
- exact gap starts: `34,570,543,382`
- actual full-path runtime: `20,940.094`초, 약 `5.8167`시간
- primary row: 2
- forced record 제거 후 conditioned gap count: 두 행 모두 0
- primary expected recurrence: 0
- positive-variance row: 0
- LOW_INFORMATION: 2/2 = 100%
- 5x Poisson planning power: 0
- A gate: FAIL
- recommendation: `HOLD_PREFIX_INFORMATION`
- observed recurrence·p/q/z 저장과 hypothesis test: 수행하지 않음
- automatic full-range promotion: 수행하지 않음
- theorem claim: 없음
- 완료 BAT:
  `test_done/run_P018A_prefix_information_probe-20260901T125849Z-done.bat`
  - SHA-256:
    `3402f68c47e396d42c67c5a64d156f45e60c1725f1efd559fc739e1fc1dfd437`
- 완료 전용 PS1:
  `test_done/run_p018a_prefix_information_probe-20260901T125849Z-done.ps1`
  - SHA-256:
    `0a780a440c5f91c9c110ccd350bc151135fc118e849f3d7efcbd0835b38c2bf5`
- 공통 `scripts/runners/run_p018_prefix_information.ps1`와 source·evidence: 재현성과 후속 설계용
  `KEEP_ACTIVE`

판정은 `EXPERIMENT_PASS / HOLD_PREFIX_INFORMATION / NO_AUTOMATIC_PROMOTION`이다. B reference
범위가 논리적으로 불가능하다는 뜻은 아니지만, A가 사전등록 gate를 통과하지 못했으므로 B를
즉시 실행하지 않는다. 새 revision을 검토한다면 development evidence와 독립 판정 범위를
분리하고, positive-variance 정보를 얻을 사전 근거와 outcome-dependent selection 방지 규칙을
먼저 문서화한다.
