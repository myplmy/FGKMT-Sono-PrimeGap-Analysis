# serial full oracle 없는 병렬 계산 검증 영향도 분석

최종 갱신: 2026-08-30 KST

## 결론

새 범위도 병렬로 계산할 수 있다. 권장 구조는 **병렬 한 번**이 아니라 서로 다른 분할로 전체를
병렬 두 번 계산하고 exact endpoint prime count와 함께 확인하는 P019 dual-partition 방식이다.
P017-B 실측을 대입하면 같은 범위에서 약 1시간 36분으로 추정되어 serial+parallel 약 4시간
18분보다 약 2.70배 짧다.

## 대안 비교

| 방법 | 전체 scan | 장점 | 주요 약점 | 판정 |
|---|---:|---|---|---|
| serial + parallel | 2 | 서로 다른 execution shape, P017에서 검증됨 | serial이 느려 CPU 사용률·wall time 불리 | calibration 정본 |
| parallel 1회 | 1 | 가장 빠름 | partition/worker 오류의 full cross-check 없음 | production 비권장 |
| parallel dual-partition | 2, 모두 병렬 | exact 전수검사 유지, partition 오류 검출, wall time 단축 | sieve·accumulator 공통 오류 가능 | future production 권장 후보 |
| 완전 독립 구현 2개 | 2 | common-mode risk 최소 | 두 번째 고성능 sieve·통계 구현과 검증 비용 큼 | 장기 연구 |

## 과학 결과에 미치는 영향

P019는 prime/gap을 샘플링하거나 통계 정밀도를 낮추지 않는다. exact core가 같아야 하므로 P013의
plateau, component와 fixed-seed inference 입력은 기존 serial 방식과 같은 정수표를 받는다. 따라서
올바르게 통과하면 연구 질문이나 유의수준을 바꾸지 않는다.

다만 source가 같은 두 실행은 논리적으로 독립인 증명이 아니다. 보고서에는 반드시
`parallel dual-partition cross-check`라고 쓰고 `independent serial oracle`이라고 쓰지 않는다.

## 운영 영향

- 8 worker를 두 pass에서 순차 사용하므로 peak CPU/RAM은 한 parallel pass와 비슷하고 총 CPU
  사용량은 약 2배다.
- wall time은 느린 serial pass가 없어져 줄어든다.
- 두 pass의 full sufficient statistics를 동시에 저장할 필요는 없다. verifier equality와 manifest
  증거만 저장하면 disk 증가는 작다.
- source hash가 바뀌면 P017 calibration 근거가 끊기므로 새 serial calibration이 필요하다.

## 승격 판단

toy PASS 뒤에도 P018 정보 gate가 HOLD인 동안 새 P013 range를 계산할 이유는 없다. 먼저 P018
gate를 사용자와 동결하고, 다음 범위가 정보량 기준을 통과할 사전 근거가 생겼을 때 P019 actual
runner를 만든다. 계산 시간이 남는다는 이유만으로 production sweep을 만들지 않는다.

