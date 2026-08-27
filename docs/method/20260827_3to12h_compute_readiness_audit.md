# 2026-08-27 3–12시간 CPU 실험 준비도 감사

## Context

사용자는 Ryzen 7 9700X CPU의 유휴 시간을 낭비하지 않도록, 현재 코드가 준비된 연구 중
3시간 이상 12시간 미만의 의미 있는 실행이 있는지 확인해 달라고 요청했다. 목적은 시간을
채우는 것이 아니라, 장시간 계산이 필요한 연구를 짧은 pilot만 반복하며 미루고 있는지와
그 이유를 구분하는 것이다.

이 문서는 실행 결과가 아니라 현재 계획·코드·실측을 대조한 준비도 감사다. 수학·승인
정본은 `AGENTS.md`, `docs/METHODS.md`, 각 `test_plan/`을 따른다.

## Goals

1. 3–12시간 안에 끝날 가능성이 있고 과학 질문에 직접 답하는 code-ready 실행을 찾는다.
2. 단순 benchmark, 중복 계산, coverage가 없는 탐색을 장시간 실험으로 잘못 승격하지 않는다.
3. 장시간 실행이 없다면 계산이 아니라 무엇이 병목인지 명확히 기록한다.

## Non-goals

- CPU 시간을 채우기 위한 임의 반복·seed sweep·범위 확장을 만들지 않는다.
- hard wall limit을 예상 실행시간으로 해석하지 않는다.
- count upper bound를 candidate 위치나 search acceleration으로 바꾸어 표현하지 않는다.
- `[10^9,10^10]` P012 holdout을 방법 조정 전에 열지 않는다.

## Inputs

- P005 calibration: 87초, full Rank 85→86 coverage 미증명
- P006 `[2,10^9]`: 핵심 sieve·분석 2.699초
- P009 one-block actual: 핵심 0.734초, Gate A만 PASS
- P010 modulus-30030 scan: 35,224,647 constraints 약 0.77초
- P010A G4: 4 LP solves, 핵심 20.919초, full floating convergence
- P011 actual: 짧은 stationary-null pilot
- P012-A: 구현·toy 검증 완료, 예상 1–10분, actual 미실행

## 후보별 판정

| 후보 | 현재 코드 준비도 | 예상시간 | 과학적 게이트 | 3–12시간 runner 판정 |
|---|---|---:|---|---|
| P005 Rank 85→86 exhaustive | calibration만 준비 | 현실적으로 범위 밖 | every-prime-start coverage와 ledger 없음 | 작성 금지 |
| P006/P012-A `[2,10^9]` | 준비 | 1–10분 | 개발범위 actual 필요 | 짧은 runner만 준비 |
| P012-B `[10^9,10^10]` | A 이후 설계 | A 실측상 3시간 미만 가능성 큼 | A 결과 감사·방법 동결 전 holdout 금지 | 아직 작성하지 않음 |
| P009 10-block boundary sample | actual adapter는 준비, 새 block list 미정 | 10–120분 | internal-zero block 공급·대표성 없음 | 장시간 후보 아님 |
| P010A modulus-30030 재실행 | 완료 | 약 21초 | 같은 full floating LP에 이미 수렴 | 중복이므로 작성 금지 |
| P010A modulus-510510 | 미구현 | 미측정 | 92,160 states·8,524,288,932 constraints, 새 exact lift·streaming·LP 설계 필요 | 현재 작성 불가 |
| P010B 실제 search acceleration | 차단 | 산정 불가 | absolute candidate-cover mapping과 false-negative 0 증명 없음 | 계산 전 수학 blocker |

### modulus 510510 자원 경고

기존 full-matrix 자원식은 modulus 510510에서 다음을 준다.

- states: 92,160
- LP variables: 92,163
- transitions: 8,524,288,932
- COO 배열만의 하한 추정: 약 825.65 GiB
- 보수적 solver working 추정: 약 4,953.90 GiB

따라서 32 GB PC에서 기존 full LP는 불가능하다. modulus-30030 cutting-plane을 단순히
숫자만 바꾸는 runner도 안전하지 않다. 새 memory-safe oracle의 scan 속도·potential 저장,
초기 working-set LP의 92k-variable 동작, exact int overflow를 먼저 작은 bounded calibration로
검증해야 한다. 이 단계가 통과하면 향후 3–12시간 후보가 될 수 있지만 현재는 code-ready가
아니다.

## 접근법 비교

| 접근 | 정확성 | 비용 | 위험 | 판정 |
|---|---|---|---|---|
| 준비된 짧은 코드를 반복해 3시간을 채움 | 새 질문에 답하지 않음 | 높음 | 중복 결과를 진전으로 오인 | 기각 |
| 임의의 큰 parameter benchmark 작성 | 성능정보만 얻음 | 중간–높음 | coverage·가설과 연결되지 않음 | blocker가 풀릴 때만 조건부 |
| 이론·coverage gate 뒤 필요한 계산만 실행 | 가장 높음 | 필요한 만큼 | CPU 유휴시간이 생길 수 있음 | 권장 |

## Verification

1. 각 계획의 상태·성공·중단 기준을 live 파일에서 재확인했다.
2. 실제 로그의 핵심 elapsed를 사용했고 hard wall limit은 제외했다.
3. modulus 510510 states·constraint·memory estimate를 현재 코드로 정적으로 계산했다.
4. code-ready, implemented-but-blocked, conceptual-only를 구분했다.

## Risks

- P006의 매우 빠른 `10^9` 실측을 더 큰 범위에 완전 선형 외삽하면 I/O·cache 변화를 놓칠 수 있다.
- HiGHS floating convergence는 exact LP 최적성 증명이 아니다. G4의 exact certificate는 상한의
  유효성만 엄밀히 보장한다.
- 새로운 modulus가 상한을 더 낮춰도 absolute search 위치와 비용 감소는 자동으로 생기지 않는다.
- P012 holdout을 미리 실행하면 독립 확인 자료로서의 가치가 줄어든다.

## Approval gate

현재 과학적으로 타당하고 code-ready인 3–12시간 actual runner는 **0개**다. 따라서 새
장시간 runner를 만들지 않는다. 준비된 P012-A 짧은 runner만 사용자가 실행한다. 다음 중
하나가 충족되면 이 감사를 갱신한다.

1. P012-A 결과 감사와 방법 동결 완료
2. modulus-510510 memory-safe bounded calibration 설계 완료
3. P010B absolute candidate-cover theorem/verifier 준비
4. P005 every-prime-start coverage mapping 준비

## Outputs

- P012-A 사용자 runner:
  `scripts/experiments/p012/run_p012_stratified_null_development.ps1`
- 3–12시간 runner: 없음
- 실제 heavy 실행: 없음

## Follow-up

1. P012-A를 먼저 실행·감사한다.
2. P012-A 계약을 동결한 뒤 P012-B runner와 실제 예상시간을 작성한다.
3. 계산수론 축에서는 G4 exact certificate를 문서화하고, 다음 계산보다 먼저 P010B mapping
   또는 modulus-510510 memory-safe feasibility를 이론·toy 단계에서 검토한다.
