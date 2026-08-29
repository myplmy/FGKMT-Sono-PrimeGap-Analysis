# P013 segment·P014 exact-scan 병렬화 영향도 분석

작성: 2026-08-29 KST

## 결론

병렬 계산 엔진의 **재사용 가능성은 높다**. P013과 완전히 같은 recurrence 가설검정을 더 큰
decade에 계속 반복할 과학적 가치는 현재 LOW_INFORMATION 결과 때문에 별도 재평가가 필요하지만,
동일한 segmented-prime sufficient-statistics 계산은 holdout, 민감도 분석, 독립 저장검증에서
다시 필요할 가능성이 높다. P014의 exact constraint scan은 lift, seed/separation, 최종 certificate,
saved verification에서 반복되므로 병렬화 편익이 더 직접적이다.

이번 단계에서는 기존 serial 정본을 바꾸지 않는다. 별도 toy revision이 serial 결과와 exact하게
같다는 것을 worker 수별로 확인한 뒤에만 actual 승격을 검토한다.

## 비목적

- CPU 사용률을 높이기 위해 prime, gap, constraint 또는 Monte Carlo replication을 생략하지 않는다.
- floating-point 근사로 exact integer certificate를 대체하지 않는다.
- 병렬 실행 순서에 따라 통계값·hash·top-k tie 결과가 달라지는 것을 허용하지 않는다.
- toy 속도를 actual 속도 향상으로 외삽하지 않는다.
- 병렬화만으로 P013 가설이나 P014 search acceleration이 증명됐다고 주장하지 않는다.

## 영향 축

| 축 | 판정 | 근거와 보존 조건 |
|---|---|---|
| FGKMT 반복로그·end-bounded `G(x)` | 영향 없음 | P013은 별도 start-exposure 통계이고 P014는 finite certificate다. 정본 정의는 변경하지 않는다. |
| P013 gap-start 범위 | 영향 있음 | 각 segment는 `[a,b)`의 gap start를 담당하고 `b` 이상 첫 소수를 포함해 오른쪽 crossing gap을 닫아야 한다. |
| prime/gap 완전성 | 영향 있음 | segment 사이 boundary prime 일치, 전체 gap count, bin·plateau sufficient statistics를 serial과 exact 대조한다. |
| P013 통계 정밀도 | 영향 없음이 목표 | 이번 toy는 sieve/count 병렬화만 하며 replication·seed·hypergeometric 법칙을 바꾸지 않는다. |
| P014 certificate 산술 | 영향 있음 | signed `int64` overflow guard를 동일 적용하고 각 constraint를 정확히 한 번 검사한다. |
| P014 top-k tie | 영향 있음 | `(slack, source, target, gap, weight)` 전역 정렬로 worker 완료 순서와 무관하게 결정한다. |
| provenance·승인 | 영향 있음 | toy와 actual을 분리한다. actual runner 연결은 별도 계획·사용자 승인 뒤에만 한다. |
| 재현성 | 영향 있음 | worker `1/2/4/8` 결과와 serial 결과가 동일해야 한다. |
| RAM·디스크 | 확인 필요 | actual은 동시 in-flight block 수와 worker별 working set을 측정해 RAM 32 GB 이하를 보장해야 한다. |

## P013 선택지

1. **현재 serial 유지**: 정확성 위험은 가장 낮지만 P013-B처럼 두 번의 전체 sweep 비용이 크다.
2. **prime 배열을 coordinator로 전송**: 구현은 단순하지만 IPC·메모리 비용과 순서 위험이 커서 기각한다.
3. **segment별 sufficient statistics만 반환**: 각 worker가 crossing gap까지 닫고 작은 집계표만
   반환한다. ordered exact merge가 가능하므로 권장한다.
4. **외부 native sieve로 교체**: 속도 가능성은 있지만 새 dependency·독립 검증 범위가 커 이번
   toy 범위에서 제외한다.

## P014 선택지

1. **현재 serial row scan 유지**: 정본 oracle로 보존한다.
2. **NumPy thread pool**: 배열 공유 장점이 있지만 GIL 재진입과 메모리 대역폭 효과를 별도
   측정해야 한다.
3. **process별 source-row block scan**: exact 부분합과 결정적 merge가 명확하므로 첫 toy로
   권장한다.
4. **C/OpenMP 재작성**: 검증 비용이 너무 커 현 단계에서는 제외한다.

## 승격 게이트

1. serial과 parallel의 모든 exact core field가 동일하다.
2. P013은 worker 수가 달라도 prime/gap count와 모든 nested count dictionary가 동일하다.
3. P013 인접 segment의 `boundary_prime == next.first_prime`가 전부 성립한다.
4. P014는 worker 수가 달라도 scanned constraints, violation count, minimum slack,
   top exact violations와 overflow guard가 동일하다.
5. feasible certificate와 deliberately infeasible certificate를 모두 시험한다.
6. toy 전체와 기존 전체 unittest가 PASS한다.
7. 실제 runner에는 아직 연결하지 않는다.

## actual 승격 전에 추가로 필요한 것

- P013: 1·4·8 worker 중간범위 calibration, 실제 peak RAM, worker affinity, crash/retry 시
  중복 없는 manifest, serial saved-verifier와의 독립성 설계
- P014: modulus 210/2310 중간 calibration, 4/8 worker memory-bandwidth 비교, worker당 thread=1,
  32 GB fail-fast memory gate, progress callback과 worker failure 전파
- 두 실험 공통: schema revision, 입력/code hash, worker topology, merge hash를 결과 manifest에 저장

