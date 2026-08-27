# 2026-08-28 48시간 사용자 실행용 실험 영향도 분석

## Context

사용자는 향후 3일 동안 Codex에 추가 작업을 요청하기 어렵고, 합계 약 48시간의 CPU 시간을
미리 준비된 실험에 사용할 수 있다. 목적은 시간을 채우는 것이 아니라 현재 선결조건이 충족된
질문을 재현 가능한 runner로 독립 실행하는 것이다.

## 후보 비교

| 후보 | 정확성·과학 질문 | 예상시간 | 현재 blocker | 판정 |
|---|---|---:|---|---|
| P013-A `[10^10,10^11)` recurrence extension | P012 규칙을 그대로 적용한 새 범위 진단 | 1.5–3시간 | 없음 | 채택 |
| P013-B `[10^11,10^12)` recurrence extension | 더 많은 complete plateau에서 저정보 한계가 줄어드는지 확인 | 10–18시간 | 없음; 동일 구현 gate 필요 | 채택 |
| P014 modulus-510510 staged certificate | exact lift의 memory-safe 검증과 조건부 count-bound 개선 가능성 | 3–16시간 | 없음; stage-A가 느리면 optimizer 자동 생략 | 채택 |
| P010B large-range acceleration | absolute candidate cover와 total-cost 개선 | 산정 불가 | non-circular mapping·PARI survivor adapter 없음 | 제외 |
| P005 Rank 85→86 exhaustive | 실제 exhaustive coverage | 현실적으로 불명 | every-prime-start coverage·ledger 없음 | 제외 |
| P010A modulus-30030 반복 | 이미 full floating convergence | 수분 | 새 질문 없음 | 중복으로 제외 |

## 변경 영향 축

| 축 | P013 | P014 | 판정 근거 |
|---|---|---|---|
| 반복로그·end-bounded `G/H` | 영향 없음 | 영향 없음 | 두 실험 모두 별도 recurrence/count-certificate 축 |
| recurrence 경계 | 영향 있음 | 영향 없음 | P013은 start exposure `[s_i,s_(i+1))`만 사용 |
| 통계 재현성 | 영향 있음 | 영향 없음 | P013 범위·bin·seed·100,000회·두-stage alpha를 실행 전에 고정 |
| certificate 수학 | 영향 없음 | 영향 있음 | P014는 `30030 | 510510`, `lambda>=0` exact lift 정리를 사용 |
| provenance | 영향 있음 | 영향 있음 | validated record와 P012/P010A saved manifest hash를 고정 |
| 큰 정수 | 영향 있음 | 영향 있음 | P013 count는 Python int, P014는 signed-int64 overflow guard 후 exact scan |
| RAM·disk | 영향 있음 | 영향 있음 | P013 streaming; P014 chunk 64 추정 550 MiB, full matrix 금지 |
| theorem/empirical 구분 | 영향 있음 | 영향 있음 | P013은 경험적 진단, P014는 finite exact certificate만 주장 |
| search acceleration | 영향 없음 | 영향 없음 | P014 count 상한 개선이 생겨도 P010B 가속은 미증명 |

## P013 선택 근거

P012-B는 4개 complete plateau와 12/12 LOW_INFORMATION으로 끝났다. 더 큰 범위를 보는 것은
그 한계가 실제로 줄어드는지 직접 측정한다는 의미가 있다. 다만 P012-B 결과를 본 뒤 새 범위를
선택했으므로 P012-B 자체를 소급 변경하지 않는다. P013-A/B의 방법·범위·seed와 두-stage
primary 기준 `0.025`를 이번 실행 전에 새 계약으로 고정한다. A와 B는 각각 별도 결과로
보고하며, 결과를 본 뒤 bin을 합치거나 pooled discovery를 만들지 않는다.

P012-B 실측의 두 full sweeps 약 7분 54초를 gap-start 수에 선형 외삽하면 P013-A는 약
72분, P013-B는 약 10.9시간이다. 큰 범위의 cache·OS 변동을 반영해 각각 1.5–3시간,
10–18시간으로 보수적으로 잡는다.

## P014 선택 근거

P010A G4의 modulus-30030 certificate는 exact PASS이고 `lambda_num>=0`이다. 따라서 potential을
residue reduction으로 modulus 510510에 복제하면 같은 상한의 exact feasible certificate가
된다. P014 stage-A는 이 수학적 lift를 8,524,288,932 constraints 전체에서 구현상 재검증한다.

현재 정적 자원값:

- states: `92,160`
- constraints: `8,524,288,932`
- full matrix 하한: 약 `825.65 GiB`이므로 금지
- chunk rows 64, top-k 20,000 보수적 scan workspace: 약 `549.8 MiB`
- lifted exact int64 guard upper bound: `279,298,307,186,501,460`
- signed int64 limit: `9,223,372,036,854,775,807`

stage-A가 PASS하고 사전 시간 gate 안이면 stage-B working-set cutting-plane을 실행한다.
stage-A가 너무 느리면 optimizer를 자동 생략하고 calibration-only PASS로 종료한다. 이는 실패를
숨기는 것이 아니라 48시간 자원계약을 지키는 사전 고정 분기다.

## 48시간 queue 설계

권장 순서는 P013-A → P013-B → P014다. P013-A가 shared implementation 문제로 실패하면
같은 코드의 P013-B는 자동 `BLOCKED` 처리하고, 독립인 P014는 계속한다. 각 child는 자체 log,
run id, manifest를 가진다. queue는 orchestration-only이며 child 결과를 대신 판정하지 않는다.

- P013-A timeout: 4시간
- P013-B timeout: 20시간
- P014 timeout: 22시간
- global wall cap: 47시간
- aggregate artifact cap: decimal 50 GB
- CPU only, GPU 금지

## 결론

P013-A, P013-B, P014는 현재 선결조건이 충족됐고 서로 다른 질문에 답한다. P010B actual과
Rank 85→86 exhaustive runner는 핵심 coverage 증명이 없으므로 만들지 않는다. 준비된 세
실험의 합은 보수적 상한 46시간이며 48시간 창 안에 들어온다.

## 구현 후 확인

P013-A/B, P014와 P015 queue는 구현됐고 actual은 실행하지 않았다. P013 두 stage preflight,
P014 G4 provenance·resource·overflow preflight, approval/BAT gate 8개, active PS1 parser 11개,
고정 FGKMT Python 전체 unittest 140개가 PASS했다. 실행 정본은 P015 한 번이며 개별 BAT와
중복 실행하지 않는다. 로컬검증 증거는
`test_result/202608280109_P013_P014_P015_local_validation.md`에 기록했다.
