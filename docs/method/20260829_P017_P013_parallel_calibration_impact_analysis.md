# P017 P013 병렬 calibration 영향도 분석

작성: 2026-08-29 KST

## 결론

P013과 같은 소수구간 sufficient-statistics 계산은 후속 holdout·민감도·독립 재검산에서 다시
필요할 가능성이 높다. 다만 현재 P013-A/B scientific question을 더 큰 범위로 자동 연장하는
것은 LOW_INFORMATION 결과와 P013-B 미완료 상태 때문에 권장하지 않는다. 이번 승격 후보는
연구 가설을 추가하는 실험이 아니라, 기존 serial 정본과 **완전히 같은 입력과 출력**을 더 짧은
wall time에 계산할 수 있는지 확인하는 engineering calibration이다.

권장 설계는 다음 두 독립 검증이다.

1. P013-A 전체 `[10^10,10^11)`를 병렬로 한 번 계산하고 완료된 serial checkpoint와 전체
   deterministic analysis를 exact 비교한다.
2. P013-B는 전체 재실행하지 않고 첫 primary half-decade
   `[10^11,316227766017)`만 serial·parallel로 각각 계산해 exact 비교한다.

한 queue의 child timeout 합은 15시간, global hard wall은 16시간으로 제한한다. 현재 실행 중인
P013-B의 process·checkpoint·result directory는 읽거나 수정하지 않는다.

## 영향 축

| 축 | 판정 | 보존·검증 조건 |
|---|---|---|
| FGKMT 반복로그·end-bounded `G(x)` | 영향 없음 | P013은 별도 gap-start recurrence 통계이며 canonical FGKMT 정의를 바꾸지 않는다. |
| P013-A scientific result | 영향 있음 | 기존 serial checkpoint와 checkpoint payload 및 100,000회 fixed-seed analysis 전체가 exact 일치해야 한다. |
| P013-B 진행 중 actual | 영향 없음이 필수 | 별도 run label·checkpoint·result directory만 사용하고 B full 산출물에는 접근하지 않는다. |
| prime/gap 완전성 | 영향 있음 | 모든 segment가 `[a,b)` gap start를 담당하고 `b` 이상 첫 소수로 crossing gap을 닫으며 인접 boundary prime을 대조한다. |
| 통계 정밀도 | 영향 없음 | bin, cohort, seed, replication 100,000회, exact hypergeometric 법칙을 변경하지 않는다. |
| 재현성 | 영향 있음 | serial/parallel exact core, plateau, component, inference 및 worker 수를 manifest에 기록한다. |
| CPU | 영향 있음 | 물리 4코어·논리 8프로세스 affinity를 사용하고 worker별 native thread는 1로 제한한다. |
| RAM | 확인 필요 | prime 배열을 IPC로 전달하지 않고 sufficient statistics만 반환한다. actual peak RAM은 사용자 실행에서 측정·보고한다. |
| 시간 | 영향 있음 | A 4시간, B-mid 11시간 child cap; queue global 16시간에서 강제 종료한다. |
| 승인·provenance | 영향 있음 | 사용자 확인 플래그, 고정 Conda Python, immutable run directory, 입력·source hash를 요구한다. |

## 선택지 비교

| 선택지 | 정확성 | 비용 | 위험 | 판정 |
|---|---|---:|---|---|
| P013-B full serial/parallel 재실행 | 높음 | 30시간 이상 가능 | 현재 B 중복·16시간 초과 | 기각 |
| A/B 모두 작은 toy만 재검증 | toy 정확성만 확인 | 매우 낮음 | actual 규모 성능·경계 검증 부족 | 이미 P016에서 완료 |
| A full + B first half-decade serial/parallel | exact oracle 유지 | 약 4–10시간 예상 | 제한된 B 범위만 검증 | 권장 |
| 기존 serial runner 즉시 교체 | 미확정 | 미확정 | shared bug·성능 역전 가능 | 금지 |

## 무손실 조건

- prime, gap, segment, bin, plateau, constraint 또는 Monte Carlo replication을 생략하지 않는다.
- P013-A는 완료된 serial checkpoint SHA-256과 canonical payload가 동일해야 한다.
- P013-A의 parallel-checkpoint 기반 analysis JSON은 완료된 serial `analysis.json`과 동일해야 한다.
- P013-B midrange는 serial과 parallel의 populations, gap counts, exposure counts,
  equal-exposure counts가 모두 동일해야 한다.
- P013-B midrange의 complete record indices는 `41–45`로 고정한다.
- worker completion order는 merge 결과에 영향을 주지 않는다.
- 8개 worker가 모두 실제 segment를 처리하지 않으면 FAIL한다.
- timeout은 PASS가 아니며 partial artifact로만 남긴다.

## 실제 runner 승격 게이트

P017이 PASS하더라도 기존 P013 runner를 자동 교체하지 않는다. 다음을 모두 확인한 뒤 사용자에게
다시 승격 여부를 묻는다.

1. A full exact equality PASS
2. B midrange serial/parallel exact equality PASS
3. 8 worker 실제 참여와 worker별 native thread=1 PASS
4. peak RAM 32 GB 미만 및 queue 16시간 미만
5. progress·terminal log·manifest·saved-artifact verification PASS
6. serial oracle보다 wall time이 실질적으로 개선됨

