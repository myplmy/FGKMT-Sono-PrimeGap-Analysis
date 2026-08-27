# P010B — count certificate에서 실제 search acceleration으로의 연결

## 1. 상태

`ONE_CANDIDATE_SCAN_PASS / EXACT_LIFT_PASS / EXACT_COVER_VERIFIER_IMPLEMENTED / TOY_PASS / ABSOLUTE_MAPPING_BLOCKED / ACCELERATION_NOT_PROVED`

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

## 4. 완료 실행 provenance

modulus-30030 one-candidate scan은 이미 완료됐다. 당시 runner는
`test_done/run_p010b_mod30030_one_candidate_scan-20260826T144440Z-done.ps1`에 보존했으며
재실행하지 않는다. 결과 정본은
`test_result/202608270005_P009_P010_bounded_queue_result_analysis.md`다.

현재 absolute candidate generator가 없으므로 사용자가 실행할 새 actual P010B 명령은 없다.

## 5. 가속 후보 승격 기준

one-candidate scan 뒤에도 다음이 없으면 P010B는 준비 단계에 머문다.

- candidate-to-absolute-range mapping theorem
- false-negative 0의 exact verifier
- candidate 수와 certificate bytes 실측
- survivor 검증을 포함한 total cost
- 동일 CPU·범위·threshold baseline 비교

count upper bound만 줄고 이 연결이 없다면 “이론적 count 개선”으로는 의미가 있어도
prime-gap exhaustive search algorithm의 개선이라고 쓰지 않는다.

## 6. modulus-certificate 구현 범위와 보류 범위

- 구현: 5,760 states·35,224,647 constraints one-candidate full scan
- 구현: 위반 0일 때 exact modulus lift와 integer streaming 검증
- 미구현/보류: 실제 상한을 줄이는 cutting-plane solve
- 보류 이유: 먼저 full scan 시간과 exact-lift baseline을 실측해야 iteration 수와
  16시간 예산의 타당한 상한을 정할 수 있다.

## 7. 실제 G1 결과와 후속 판정

- 5,760 states·35,224,647 constraints를 0.7741초에 full scan
- floating violation 0, minimum slack `-2.220446049250313e-16`
- exact lift 35,224,647 constraints도 위반 0
- modulus-2310 상한을 그대로 복사했으므로 strict improvement 없음
- absolute candidate-to-range mapping과 break-even은 여전히 없음

full scan은 병목이 아니므로 P010A cutting-plane 연구는 진행할 가치가 있다. 그러나 이는
count upper bound 연구다. P010B 가속 승격은 coverage mapping이 생기기 전까지 BLOCKED다.

## 8. Exact candidate-cover 검증 gate

coverage-preserving 정식화를 실제 machine-checkable gate로 옮겼다.

- 구현: `source/candidate_cover.py`
- CLI: `source/candidate_cover_cli.py`
- tests: `tests/test_candidate_cover.py`
- synthetic runner: `scripts/experiments/p010b/run_p010b_candidate_cover_toy.ps1`

직접 verifier는 작은 유한 우주 `[a,b)`의 모든 정수 start를 다음 중 정확히 하나로 분류한다.

1. candidate survivor
2. exact nontrivial factor가 있는 composite rejection
3. `c<q<c+H`를 만족하는 exact-prime window rejection

누락, candidate/rejection 중복, 잘못된 factor, probable-prime 대체, `q=c+H`, 중복 witness를
모두 거부한다. equality `gap=H`는 candidate에 남는다.

break-even gate는 다음을 모두 요구한다.

- coverage·soundness PASS
- exhaustive truth를 쓰지 않은 generator
- 같은 CPU·범위·threshold·code hash
- 최소 5회 median
- false negative 0
- 생성+검증+survivor 검색 총시간이 baseline보다 최소 5% 작음
- artifact는 십진 50 GB, 즉 `50,000,000,000` bytes 이하

이 조건을 통과해도 상태는 `ACCELERATION_CANDIDATE`이며 독립 반복 전에는 가속 증명으로
표시하지 않는다.

## 9. Synthetic toy 결과

2026-08-27 Codex 로컬검증은 `[1000,10000)`, `H=20`에서 다음을 확인했다.

- exact direct universe: 9,000 starts
- survivor candidate와 전수계산 위험 start: 각각 69, exact set 일치
- factor/window-prime witness로 나머지 8,931 starts 전부 coverage
- 7/7 unit tests PASS
- saved manifest 재검증 issue 0
- 실제 prime search: 미실행
- acceleration: `BLOCKED`

`BLOCKED`인 이유는 toy generator가 정답을 전수검사해서 ledger를 만드는 순환적 oracle이기
때문이다. 이 결과는 정리 A–C의 verifier plumbing을 검증하지만 discovery algorithm을
개선하지 않는다.

## 10. 남은 선결조건과 다음 구현 gate

실제 `[10^20,10^21)` 가속 runner를 만들기 전에 다음이 필요하다.

1. exhaustive truth 없이 absolute interval을 candidate/witness로 매핑하는 generator
2. 큰 window-prime에 대한 PARI certificate와 candidate start의 정확한 연결
3. 직접 1,000,000-start verifier를 대체할 압축 coverage 증명 형식
4. survivor를 기존 `prime-gap` search에 전달하는 누락 없는 adapter
5. 동일 범위 baseline과 최소 5회 total-cost 비교

따라서 지금 장시간 actual runner를 만드는 것은 타당하지 않다. 다음 연구 대상은 compressed
coverage ledger 형식과 PARI witness adapter의 toy·중간정수 확장이며, 이 선결조건을 통과한
뒤에만 50 GB 제한 actual feasibility runner를 만든다.
