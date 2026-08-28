# P013-A r1 대규모 hypergeometric 실패 분석

## 판정

`USER_RUN_FAILED / PRIME_SWEEP_COMPLETED / INFERENCE_NOT_COMPLETED / NO_SCIENTIFIC_RESULT`

P013-A r1은 input preflight와 targeted tests를 통과하고 `[10^10,10^11)`의 exact gap count와
오른쪽 boundary prime 내부 검사를 통과했다. 그러나 Monte Carlo inference 첫 large component에서 NumPy가 지원하지 않는
10억 이상 category count를 받아 종료코드 1로 실패했다. result directory·manifest·summary·CSV·
figure·saved verification report가 없으므로 `EXPERIMENT_PASS`가 아니다.

## 실행 증거

| 항목 | 값 |
|---|---|
| log | `logs/run_20260827T163052Z_p013a_recurrence_extension_1e11.log` |
| log SHA-256 | `5CCD6E2997123A99120512AF9D36A4B5AC50CFB4A3E24D6833E5B48EAEEBE79C` |
| 실행 시각(KST) | 2026-08-28 01:30:52–02:14:53 |
| runner SHA-256 | `8d073e66480b4d6eb3601f248e648c4d210ef17a3c87971a8094414306a25b5a` |
| analysis source SHA-256 | `89bf7b5011ef9503543f4c43a42138c643467d7742ebe9c84013058e56ab4b98` |
| contract SHA-256 | `153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf` |
| 마지막으로 표시된 progress | `sieve_chunks_completed=1800` |
| 마지막 prime | `99,999,999,977` |
| emitted count | `3,663,002,302` |
| 첫 FAIL | `ValueError: both ngood and nbad must be less than 1000000000` |
| 표시된 partial dir | `run_20260827T163052Z_p013a_recurrence_extension_1e11` |
| partial dir 실제 존재 | 아니오 |
| terminal PASS | 없음 |

progress는 첫 chunk와 100번째 chunk마다만 찍힌다. 1,800번째 progress 뒤의 boundary-only chunk는
표시되지 않았지만, 예외 위치가 gap/prime count 검사 뒤의 `analyze_components`이므로
`gap_count=3,663,002,302`와 `prime_count=3,663,002,303` 내부 검사는 통과했다. 그래도 inference와
saved recomputation이 없으므로 통계 결과나 full experiment PASS를 선언하지 않는다.

## 원인

`source/recurrence_stratified_null.py`의 기존 구현은 모든 component에
`rng.hypergeometric(good, population-good, sample, size=100000)`을 직접 호출했다. NumPy 2.4.6은
`good`과 `bad`를 각각 `10^9` 미만으로 제한한다. P012 `[2,10^10)`에서는 bin population이 이
제한 아래라 시험이 통과했지만, P013의 새 decade에서는 population category가 커져 같은 코드가
실패했다. preflight가 실제 sufficient statistics를 만들기 전에는 이 수를 알 수 없고, 기존 unit
fixture도 10억 초과 case를 포함하지 않아 결함을 사전에 잡지 못했다.

## 교정

1. safe-size component는 기존 NumPy 호출과 RNG stream을 bit-for-bit 유지한다.
2. large component는 exact hypergeometric symmetry와 sequential sampling without replacement를
   사용한다. binomial approximation은 금지한다.
3. small exact PMF·네 symmetry·10억 초과·support·moment·reproducibility test를 추가했다.
4. full sieve 직후 compact sufficient-statistics checkpoint를 저장한다.
5. final PASS에는 checkpoint reuse와 별개로 두 번째 full range recomputation을 유지한다.
6. P013-A 재시도는 새 `run_P013A_recurrence_extension_1e11_r2.bat`만 사용한다.
7. old BAT/PS1은 원본 SHA-256을 보존해 `test_done/`에 failed-done으로 이관했다.

## CPU 판정

호스트는 물리 8코어·논리 16프로세서다. r1 runner에는 affinity·thread cap이 없었고 P013 sieve와
Monte Carlo 코드가 single stream이므로 동시 계산 worker는 주로 1개였다. 교정 runner는 첫 물리
4코어·논리 8프로세서 topology mask `0xff`를 허용 상한으로 적용한다. P013 자체는 여전히 단일
stream이며 이를 8-thread 병렬화로 해석하지 않는다.

## 재실행 전 상태

- code/test/runner: `LOCALLY_VERIFIED`; affected 23/23, full 148/148, PowerShell parser 11/11,
  BAT gate 4/4, P013 A/B·P014 preflight PASS
- P013-A r2 actual: 미실행
- P013-B actual: 미실행
- P014 actual: 미실행
- 사용자 figure QA: r2 figure 생성 전이므로 해당 없음

교정 검증 정본은 `202608281447_P013A_r2_fix_local_validation.md`다.
