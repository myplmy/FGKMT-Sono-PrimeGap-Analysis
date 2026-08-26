# P009/P010 bounded queue 결과 분석

## 판정

`EXPERIMENT_PASS / P009_ONE_BLOCK_CERTIFIED_ZERO / P010_MOD30030_BASELINE_PASS / STRICT_BOUND_IMPROVEMENT_FALSE / SEARCH_ACCELERATION_NOT_PROVED`

사용자 실행 `run_20260826T144439Z_p009_p010_bounded_queue`는 세 child의 terminal PASS와
queue aggregate PASS를 모두 기록했다. Codex가 manifest hash, P010 exact arithmetic,
P009 PARI certificate 두 개와 boundary arithmetic을 다시 검사한 결과도 issue 0이다.

## queue 자원 결과

| 항목 | 값 |
|---|---:|
| queue elapsed | 25.906초 |
| P010B child wrapper | 10.265초 |
| P010A exact-lift child wrapper | 10.265초 |
| P009 child wrapper | 5.203초 |
| 저장 산출물 증가량 | 147,867 bytes |
| failure count | 0 |
| GPU 사용 | 없음 |

사용자가 관측한 “10분 미만”은 정상이다. 15시간 30분은 예상 소요시간이 아니라 runaway
방지용 hard limit였다. 이번 세 단계의 실제 핵심 계산은 각각 1초 안팎이었고 나머지는
단위시험, 새 Python/PowerShell process 시작과 logging 시간이다. 이번 결과를 전체
`[10^20,10^21)` prime search가 수십 초에 끝났다는 뜻으로 해석하면 안 된다.

## P010B modulus-30030 one-candidate scan

| 항목 | 값 |
|---|---:|
| states | 5,760 |
| 누락 없이 scan한 constraints | 35,224,647 |
| floating violation | 0 |
| floating minimum slack | `-2.220446049250313e-16` |
| 핵심 scan elapsed | 0.7741초 |
| LP solve | 미실행 |

modulus-2310 potential을 residue reduction으로 복사한 candidate는 modulus 30030의 모든
transition에서 floating tolerance 위반 0이었다. 이 결과는 memory-safe separation scan이
매우 싸다는 중요한 구현 측정이다. 그러나 새 potential을 찾은 것도, 상한을 낮춘 것도,
absolute prime-search 후보를 만든 것도 아니다.

## P010A modulus-30030 exact lift

| 항목 | 값 |
|---|---:|
| exact constraints | 35,224,647 |
| exact violation | 0 |
| minimum integer slack | 0 |
| exact streaming elapsed | 0.7684초 |
| total start-bounded upper bound | 439,161,464,927,854,179 |
| strict improvement | false |

모듈러스 배수 lift 정리를 실제 5,760-state certificate에서 exact integer arithmetic으로
확인했다. 이는 modulus 30030에서 feasible한 시작점을 제공하므로 cutting-plane 연구의
기술적 선행조건을 충족한다. 상한은 modulus 2310과 완전히 같으므로 count 개선은 아직 0이다.

## P009 single-block boundary actual

대상 block은

```text
[100000000000000000000, 100000000000000001000)
```

이다. P008의 internal start-bounded upper bound 0과 다음 exact 증거를 결합했다.

- block의 마지막 증명 소수: `100000000000000000993`
- 이 소수 다음부터 block 끝 전까지 6개 정수: 모두 exact nontrivial factor로 합성수 확인
- block 오른쪽의 증명 소수: `100000000000000001071`
- 두 증명 소수의 거리: `78 < 1856`
- PARI/GP 2.15.4 certificate 두 개 fresh-process 재검증: PASS

따라서 이 1,000 길이 block에서 시작하는 `gap >= 1856`은 정확히 0개다. 오른쪽 증명
소수가 바로 다음 소수임을 증명할 필요는 없다. block의 마지막 소수보다 78 이내에 어떤
증명 소수가 존재하므로 실제 다음 소수는 그보다 멀 수 없기 때문이다.

이 결과는 P009의 **수학적 feasibility Gate A**를 통과시킨다. 그러나 길이 1,000 block
하나를 닫은 것이 Rank 85→86 전체 범위의 exhaustive 탐색이나 알고리즘 가속을 뜻하지
않는다. 전체 폭에 적용하려면 internal-zero/candidate cover와 총비용 break-even이 여전히
필요하다.

## 사후 재검증에서 발견한 verifier 결함

P010B 결과 자체가 아니라 saved verifier의 반복 실행에 결함이 있었다. 최초 verifier가
자기 `saved_verification_report.json`을 만든 뒤 같은 verifier를 다시 실행하면 그 파일을
P010A prerequisite alias로 오인해 FAIL했다. 계산 산출물의 hash나 constraint 값은 변하지
않았으며 다음과 같이 교정했다.

1. 명시적으로 복사된 `input_p010a_saved_verification_report.json`만 prerequisite로 읽음
2. 결과 폴더 자신의 saved report 존재는 정상 상태로 허용
3. saved report가 이미 있는 상태에서 verifier를 두 번 실행하는 회귀시험 추가

교정 뒤 targeted 9/9 tests, P010B saved verification, P010A exact recomputation, P009
manifest·PARI·boundary recomputation이 모두 PASS했다. 최초 sandbox test의 TEMP ACL 오류는
정상 Windows 권한 재실행에서 사라져 코드 오류와 분리했다.

## 다음 연구에 주는 정보

1. full transition scan 자체는 병목이 아니다. G4 cutting-plane의 불확실한 비용은 반복
   sparse LP solve와 working-set 증가다.
2. modulus 30030이 가능하다는 사실만으로 개선은 보장되지 않는다. G4는 strict upper-bound
   감소를 목표로 하고, 정체하면 중단해야 한다.
3. P009 boundary proof는 싸게 생성됐지만 internal bound 0인 block을 대규모로 공급하는
   방법이 없다. boundary 비용만 더 많이 재는 것은 보조 benchmark일 뿐 가속 증명이 아니다.
4. P010A count 연구와 P010B absolute search acceleration은 계속 별도 판정을 유지한다.

## provenance

- queue log SHA-256: `23a199c936ab9bba4f6ef4b7b32fe0aba69988dcc074f251a246517201abeedf`
- queue manifest SHA-256: `d8f2a65a419b9991c289588029308bd2af2f4be42fba982cce3dfb4323ffc912`
- queue summary SHA-256: `0d66cbf6a4fe57130596902214c5771496df9ae3ab67e231aa03ea663dd2cc18`
- P010B manifest SHA-256: `ce7d087f094e833a0e195d32632fd4489bb2b762628bbe94a0e4b5a1f92ae877`
- P010A exact-lift manifest SHA-256: `d859cc6ad9f94b9b15f6db3b72f302e3704c14257d86c3be63145b74e81a8bfe`
- P009 manifest SHA-256: `4ec954d8826ba178f08292a2be4d32172811b59d992fbfd9f56cecc81f78ffbf`
