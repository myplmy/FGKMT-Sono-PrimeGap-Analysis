# P018 — P013 expected-information / power 사전판정

## 1. 상태와 승인 경계

`DESIGN_APPROVED / READ_ONLY_DIAGNOSTIC_PASS / USER_GATE_SELECTION_FROZEN / PREFIX_RUNNER_LOCALLY_VERIFIED / NO_FUTURE_FULL_SWEEP`

사용자는 P013 expected-information/power preflight 설계 착수를 승인했다. 이 단계는 완료된
P012/P013 산출물을 읽어 다음 큰 범위 계산이 통계적으로 의미 있을 가능성을 먼저 가늠한다.
P013-C 이상의 새 prime sweep는 이 계획의 승인이 아니며 별도 사용자 승인이 필요하다.

2026-09-01 사용자는 full-range gate로 균형형 B를, outcome-blind prefix information probe의 보조
gate로 탐색형 A를 확정했다. 정본은
`test_plan/P018_prefix_information_probe_contract_v1.json`과
`test_plan/P018A_prefix_information_probe.md`다. A PASS는 B 설계 검토만 허용하며 full sweep를
자동 승인하지 않는다.

## 2. 문제의식

P013-A와 P013-B는 계산량이 각각 3,663,002,302와 33,489,857,205 gap starts로 크게
늘었지만 primary scheme에서 양의 분산을 가진 plateau row는 각 1개였다. 모든 primary plateau
row가 `LOW_INFORMATION`이었고 기대 recurrence도 각각 `0.0778288`, `0.0667972`였다.

즉 “더 오래 계산하면 자동으로 검정력이 커진다”는 전제가 데이터에서 확인되지 않았다. 다음
decade를 바로 실행하기 전에 필요한 정보량과 검정력 조건을 수치로 고정해야 한다.

## 3. 고정 입력

| label | 범위/역할 | manifest SHA-256 |
|---|---|---|
| P012-A | development `[2,10^9]` | `723bd82778c92b7ebe3e9f614fd7411e86f5619d3043ed292ddac93fa6966c09` |
| P012-B | holdout `[10^9,10^10)` | `299e0bbd3e754c0f5f716ddfaea4b09bb4e0cd6adcb6f98e94e6f0a71abc89e5` |
| P013-A | prospective `[10^10,10^11)` | `86da30eb0045704c7e955433906f58129d9b10a639451ba4b5827bd344a8dbdd` |
| P013-B | prospective `[10^11,10^12)` | `a4272808f4486bbfba04e6255b1693420f46392f28b2c9567fddd82076c6d760` |

각 manifest, saved verification, `summary.json`, `cohort_summary.json`,
`plateau_statistics.csv`의 hash를 읽기 전에 검증한다. stage를 결과에 맞춰 pooling하지 않는다.

## 4. primary 정보 지표

정본 scheme/cohort:

```text
scheme = primary_width_0p5_shift_0
cohort = primary_start_ge_1000
```

stage마다 독립적으로 다음을 계산한다.

- null expected total recurrences `lambda`
- observed recurrence
- primary plateau row 수
- variance가 양수인 primary row 수
- LOW_INFORMATION row 비율
- primary variance 합
- `P(X>=1)=1-exp(-lambda)`의 Poisson planning proxy
- 기대값 1, 3, 5에 필요한 단순 정보량 배수

## 5. Poisson screen의 제한

Poisson 계산은 count-only **선별 근사**다. 실제 P012/P013 검정은 bin별 조건부
hypergeometric과 family max statistic을 사용하므로 Poisson power를 실제 achieved power라고
쓰지 않는다. 정확한 prospective power를 주장하려면 미래 range 설계, effect size, component
구조와 stopping rule을 먼저 고정한 뒤 별도 conditional simulation이 필요하다.

## 6. 초안 판정 gate

다음 값은 사용자와 합의해 full-range용 균형형 B로 동결했다.

```text
two-stage alpha = 0.025
information target: null에서 recurrence >=1 확률 50%
equivalent expected recurrence target = ln(2) = 0.693147...
minimum positive-variance primary rows = 3
maximum LOW_INFORMATION primary fraction = 0.5
screening alternative = 2x enrichment
Poisson screening-power target = 0.8
```

탐색형·균형형·확인형 세 후보와 각 값을 높이거나 낮출 때의 영향, 문헌 근거는
`docs/method/20260830_P018_gate_options_literature_review.md`에 정리했다. 코드 기본값은 사용자가
탐색형 A는 prefix-only 보조 gate로만 사용한다. 어느 gate도 full future sweep을 자동 승인하지
않는다.

모든 정보 gate와 screening-power gate를 통과해야 다음 range를 자동 권고한다. 한 항목이라도
실패하면 `HOLD_NEXT_RANGE`이며, 이는 recurrence 가설이 거짓이라는 뜻이 아니라 현재 설계로는
계산 대비 판별력이 부족하다는 뜻이다.

## 7. 현재 P013-B read-only 진단

```text
primary expected recurrence = 0.06679718843665096
primary positive-variance rows = 1 / 9
LOW_INFORMATION fraction = 1.0
P(at least one | Poisson null) = 0.0646151
information multiplier to 50% event probability = 10.3769x
multiplier to expected 1 / 3 / 5 = 14.9707x / 44.9121x / 74.8534x
Poisson 2x-enrichment screening power at alpha 0.025 = 0.00817
Poisson 2x power 0.8에 필요한 null expectation = 11.269069541418046
현재 expectation 대비 power-target planning multiplier = 168.7057465x
```

판정은 `HOLD_NEXT_RANGE`다. 이 수치는 새 decade가 단순히 10.3769배 길어야 한다는 뜻이
아니다. gap frequency와 plateau/bin 구조가 decade마다 크게 달라졌기 때문에 future information은
gap-start 수만으로 선형 외삽할 수 없다.

## 8. 구현과 toy 검증

- `source/recurrence_information_preflight.py`
- `source/recurrence_information_preflight_cli.py`
- `tests/test_recurrence_information_preflight.py`

추가 구현은 discrete Poisson rejection threshold가 바뀌는 지점을 그대로 고려해 지정 power에
필요한 최소 null expectation을 계산한다. 이는 planning proxy의 수치 보완이지 formal power
인증이 아니다.

toy tests는 Poisson upper-tail critical count, LOW_INFORMATION hold, named decision stage와
비-pooling, formal-power 비주장을 확인한다.

읽기 전용 재현 명령은 다음과 같지만 새 결과 파일을 만들지 않는다.

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B `
  -m source.recurrence_information_preflight_cli `
  --stage 'P012-A=test_result\run_20260827T054007Z_p012a_stratified_null_development_r2' `
  --stage 'P012-B=test_result\run_20260827T121734Z_p012b_stratified_null_holdout' `
  --stage 'P013-A=test_result\run_20260828T071601Z_p013a_recurrence_extension_1e11_r2' `
  --stage 'P013-B=test_result\run_20260828T090006Z_p013b_recurrence_extension_1e12' `
  --decision-stage-label P013-B
```

## 9. 다음 단계와 사용자 결정

권장안은 다음과 같다.

1. 동결된 P0 runtime calibration을 먼저 사용자 실행·감사한다.
2. endpoint와 gate를 바꾸지 않은 채 A prefix를 별도 사용자 실행한다.
3. A 결과는 B 설계 검토 여부만 결정하며 P013-C 전체 sweep runner부터 만들지 않는다.
4. 미래 범위의 정보량을 outcome을 보지 않고 추정하는 원칙을 유지한다.
5. stopping이 관측 recurrence 자체에 의존하지 않고 조건부 검정의 유효성을 보존하는지 수학적
   검토를 통과한 경우에만 sequential information design을 구현한다.
6. formal conditional power simulation은 effect size(권장 2x와 3x), family statistic,
   multiplicity와 미래 component 생성 규칙을 합의한 뒤 별도 P018-B로 분리한다.

## 10. 성공·중단 기준

성공:

- 모든 입력 terminal/saved verification과 artifact hash PASS
- stage별 독립 지표 생성
- Poisson proxy와 formal power를 명시적으로 구분
- decision stage를 이름으로 고정하고 retrospective pooling 없음

중단:

- manifest/saved/artifact hash 불일치
- primary scheme/cohort가 정확히 1개가 아님
- 음수·비유한 expectation/variance
- future range 정보 없이 formal power를 확정하려는 경우

## 11. 비목적

- recurrence enrichment 정리 증명
- P013-A/B 결과의 소급 재분석으로 유의성 만들기
- 다음 범위의 정보량을 gap-start 수에 단순 선형 외삽
- 컴퓨팅 시간이 남는다는 이유만으로 P013-C 실행
