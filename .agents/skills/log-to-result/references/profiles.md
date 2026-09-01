# Log-to-result 실험 profile

현재 실행의 연구 질문에 맞는 profile 하나를 선택한다. 여러 profile이 실제로 결합된 실행만
필요한 항목을 함께 사용한다.

## empirical-envelope

- raw/normalized source commit·hash·coverage와 boundary mode `end`
- iterated natural logarithm 직접식·금지 base-k 호출
- `start + gap = end`, exhaustive-limit closure, rejected/high-watermark mismatch 0
- interval minimum의 `next end_prime - 1`, running minimum 비증가
- 저장 `F/H/Sono ratio`의 고정밀도 독립 재계산
- log-bin·rolling·x-width local envelope와 start-bounded 보조분석의 격리
- figure numeric QA 뒤 사용자 visual QA
- finite observed threshold와 theorem-level numerical threshold의 분리

## recurrence

- prime range·gap-start range·양쪽 경계 prime·complete/censored plateau 선택
- forced record 제거, population·conditioned·exposure exact 산술
- null family, seed, Monte Carlo replay 또는 exact sampler의 재현성
- zero variance의 `None` 보존과 `LOW_INFORMATION` 비율
- multiple-testing correction, holdout/development 분리, 결과 후 pooling 금지
- worker/segment coverage와 serial 또는 dual-partition equality
- enrichment 미검출과 구조 부재를 동일시하지 않음

## finite-certificate

- threshold equality 포함 여부, source/target modulus, state·constraint count
- every-row/every-family coverage, exact integer slack, overflow·full-matrix 방지
- certificate bound와 summary·manifest exact equality
- parallel reduction과 saved serial oracle 또는 독립 verifier 범위
- restricted LP seed의 bounded/unbounded와 full LP 판정을 분리
- bound 개선 여부와 `search_acceleration_proved=false`를 별도 기록
- candidate 위치·coverage mapping·right-boundary witness가 없는 count 결과의 한계

## information-probe

- frozen contract·endpoint·gate hash, outcome-blind 필드 계약
- dual prime-count raw evidence와 `pi(U-1)-pi(L-1)` exact 일치
- 서로소 dual partition, adjacent boundary, exact sufficient-statistics equality
- saved verifier가 raw margin에서 components·gate를 다시 만드는지 확인
- observed recurrence·p/q/z·outcome digest 미열람·미저장
- `conditioned count=0` 또는 variance 0일 때 정보량 0을 보존
- P0 calibration, A prefix gate, B full-range gate의 역할과 자동승격 금지
- planning proxy와 formal hypothesis-test power를 구분
