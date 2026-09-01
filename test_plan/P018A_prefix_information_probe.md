# P018-A — P013 recurrence prefix 정보율 probe

최종 갱신: 2026-09-01 KST

## 1. 상태

`PREPARATION_ONLY / GATE_CONTRACT_FROZEN / IMPLEMENTATION_APPROVED / ACTUAL_NOT_RUN`

사용자는 2026-09-01 full-range 판정에는 균형형 B, prefix-only 보조 판정에는 탐색형 A를
승인했다. 이 승인은 설계·runner 구현을 허용하며, actual 계산은 사용자가 승인 플래그를 넣어
직접 실행한다.

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

### 7.1 WSL exact prime-count 준비 — P0/A 공통 1회

환경: WSL Ubuntu. 시작 경로:

```bash
cd /mnt/z/FGKMT-Sono-PrimeGap-Analysis
bash ./scripts/experiments/p018/prepare_p018_prefix_primecounts.sh --confirm-p018-prefix-counts
```

예상시간은 수분 이내이나 WSL·primecount 버전에 따라 달라질 수 있다. `READY.txt`, CSV, metadata,
metrics, 각 endpoint의 Gourdon·Deleglise–Rivat 원시 출력과 hash manifest, log를 생성한다. Windows
BAT가 WSL을 직접 호출하지 않는다.

### 7.2 P0 개별 실행

환경: Windows CMD 또는 PowerShell. 시작 경로: `Z:\FGKMT-Sono-PrimeGap-Analysis`.

```bat
run_P018P0_prefix_information_calibration.bat --confirm-p018p0
```

P0는 A gate를 판정할 수 없으며 예상 30–60분, hard wall 2시간이다.

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

1. P0 실행·감사로 wall time과 blinding artifact를 확인
2. endpoint·gate 불변 상태로 A 실행 여부를 사용자와 재확인
3. A 결과를 감사한 뒤에만 B 설계 검토
4. B reference runner, P019 actual, P013-C full은 자동 생성·실행하지 않음
