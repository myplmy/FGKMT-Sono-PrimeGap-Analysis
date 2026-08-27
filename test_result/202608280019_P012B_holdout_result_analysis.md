# P012-B 독립 holdout 결과 분석

## 판정

`EXPERIMENT_PASS / SAVED_FULL_RECOMPUTATION_PASS / INDEPENDENT_ARITHMETIC_PASS / INDEPENDENT_MC_REPLAY_PASS / RECURRENCE_ENRICHMENT_NOT_DETECTED / LOW_INFORMATION_LIMIT / MODEL_ACCEPTANCE_NOT_CLAIMED / FIGURE_AUTOMATIC_QA_PASS / USER_VISUAL_QA_PENDING`

사용자 실행 `run_20260827T121734Z_p012b_stratified_null_holdout`은 terminal PASS,
manifest artifact hash PASS와 saved deterministic full recomputation PASS를 모두 기록했다.
Codex가 현재 고정 코드로 holdout 전체를 다시 스트리밍하고, 저장 CSV에서 기대값·분산·z·BH
보정을 별도 산술로 계산하고, seed `20260827`의 100,000회 Monte Carlo를 독립 재생한 결과도
모두 issue 0이었다. 따라서 수치·저장·재현성 기준 P012-B는 `EXPERIMENT_PASS`다.

PNG·PDF의 hash·decode·크기·nonblank 자동검사는 PASS했다. 사람 눈으로 축·선·범례·x marker를
확인하는 시각 QA는 사용자가 수행하기 전이므로 아직 `PENDING`이다.

## 쉬운 말로 설명한 실험과 결과

P012-A에서는 `10^9` 아래 자료를 보고 “같은 크기의 gap이 record 유지 구간에서 몇 번 다시
나타나는가”를 설명하는 통계 규칙을 만들었다. P012-B에서는 그 규칙을 바꾸지 않고, 이전에
보지 않은 `[10^9,10^10)` 구간에 그대로 적용했다. 시험 문제를 본 뒤 채점 규칙을 바꾸지 않은
독립 확인이다.

이 범위에는 양쪽 경계가 완전히 닫힌 maximal-gap record 구간이 4개 있었다. gap 288, 292,
320은 최초 record 한 번만 나타났고 다시 나타나지 않았다. gap 336은 최초 record 뒤에 같은
크기의 gap이 정확히 한 번 더 나타났다.

동결된 primary 모형은 재출현을 약 `0.497`회 예상했고 실제는 1회였다. 실제가 기대보다 많기는
하지만 표본이 사실상 한 건뿐이다. family p는 `0.09394`, gap별 one-sided p를 4개 함께 보정한
최소 BH q는 `0.27596`이다. 사전 고정한 5% 기준에서는 통계적으로 뚜렷한 recurrence enrichment를
검출하지 못했다.

이 결과는 “반복 구조가 없다”거나 “P012 모형이 옳다”는 뜻이 아니다. 12개 통계 행이 전부
`LOW_INFORMATION`이고 3개는 분산이 0이다. 즉 현재 자료는 눈에 띄는 큰 효과를 찾기에는 여전히
정보가 부족하다.

## 경계와 입력 선택

P012-B는 FGKMT 본체의 end-bounded (G(x))를 바꾸지 않는다. 이 실험의 별도 recurrence
노출 구간은 gap의 start prime을 기준으로

```text
[record start, next record start)
```

를 사용한다. `[10^9,10^10)` 안에서 record start와 다음 record start가 모두 들어오는 complete
plateau만 선택했다.

| record | start prime | gap | next record start | N | M | C=M-1 |
|---:|---:|---:|---:|---:|---:|---:|
| 31 | 1,294,268,491 | 288 | 1,453,168,141 | 7,551,746 | 1 | 0 |
| 32 | 1,453,168,141 | 292 | 2,300,942,549 | 39,721,303 | 1 | 0 |
| 33 | 2,300,942,549 | 320 | 3,842,610,773 | 70,609,121 | 1 | 0 |
| 34 | 3,842,610,773 | 336 | 4,302,407,359 | 20,777,824 | 2 | 1 |

- selected plateau exposure 합: `138,659,994`
- 최초 발생을 포함한 같은-gap 출현 (M) 합: `5`
- 최초 발생을 제거한 recurrence (C) 합: `1`
- 왼쪽 continuation: 제외
- 오른쪽 censored plateau 35: 제외

전체 holdout에서는 gap start `404,204,977`개와 오른쪽 boundary prime 하나를 포함한 prime
stream `404,204,978`개를 생성했다. 이는 고정한
`pi(10^10)-pi(10^9)=404,204,977`과 정확히 일치한다.

## Primary와 sensitivity 결과

세 고정 cohort는 모든 selected start가 `10^9` 이상이므로 서로 같은 행을 포함한다. 아래 표는
`primary_start_ge_1000`을 대표로 썼으며, 이를 서로 독립인 세 번의 확인으로 세지 않는다.

| scheme | z 정의 행 | 관측 recurrence | 기대 recurrence | max `abs(z)` | family p | 최소 enrichment BH q |
|---|---:|---:|---:|---:|---:|---:|
| width 0.5, shift 0 | 3 | 1 | 0.497022 | 3.68664 | 0.093939 | 0.275957 |
| width 0.5, shift 0.25 | 3 | 1 | 0.880447 | 2.72400 | 0.127429 | 0.475755 |
| width 1.0, shift 0.5 | 3 | 1 | 0.497022 | 3.68664 | 0.092809 | 0.272317 |

세 bin scheme 모두 family p가 0.05보다 크고 최소 BH q도 0.27보다 크다. 따라서 bin 경계를
옮기거나 폭을 넓힌 sensitivity에서도 5% 기준의 enrichment 검출은 없다.

### gap 336의 해석

유일한 양의 recurrence는 다음 행이다.

```text
record start = 3,842,610,773
gap = 336
observed recurrence = 1
primary expected recurrence = 0.068534
primary z = 3.686639
primary one-sided Monte Carlo p = 0.068989
primary BH q = 0.275957
```

z가 커 보여도 Monte Carlo p가 0.05보다 작은 것은 아니다. 희귀한 count의 분포가 이산적이고,
같은 scheme에서 네 gap을 함께 살펴본 보정도 적용되기 때문이다. 이 행을 발견이나 새 수론적
구조로 해석하지 않는다.

## P012-A 개발범위와 비교

| 구분 | 범위 | z 정의 primary 행 | 관측 | 기대 | 관측/기대 | family p |
|---|---|---:|---:|---:|---:|---:|
| P012-A 개발 | `[2,10^9]` | 14 | 9 | 8.587376 | 1.048 | 0.219448 |
| P012-B holdout | `[10^9,10^10)` | 3 | 1 | 0.497022 | 2.012 | 0.093939 |

두 범위 모두 동결된 primary family 5% 기준에서 departure를 검출하지 못했다. 따라서
P012-A에서 P011의 큰 stationary 과대예측이 줄어든 뒤, 독립 holdout에서도 극단적인 모형
불일치는 확인되지 않았다는 정도로 말할 수 있다.

P012-B의 관측/기대 비율 `2.012`는 한 번의 recurrence를 0.497회와 나눈 값이라 불안정하다.
P012-A와 비율이 다르다는 사실만으로 범위에 따른 증가 추세를 주장하지 않는다. 또한 P012-B는
P011 stationary 기대값을 계산하지 않았으므로 holdout에서 P011과 직접 비교했다고 쓰지 않는다.

## 검정력과 정보 부족

| 구분 | 전체 modeled rows | variance 0 | LOW_INFORMATION |
|---|---:|---:|---:|
| P012-A | 84 | 27 | 82 |
| P012-B | 12 | 3 | 12 |

P012-B에서 variance 0 비율은 25%지만 모든 행이 LOW_INFORMATION이다. 분석 범위를 한 decade
늘렸어도 complete plateau가 4개뿐이고 record 크기 gap의 조건부 발생 횟수가 매우 작았다.
따라서 단순히 한 decade씩 계속 확장하는 방식은 계산량에 비해 검정력이 천천히 늘어날 수 있다.

후속 recurrence 연구를 한다면 P012-B를 수정하지 말고 새 실험번호에서 pooled 또는
hierarchical 모형의 검정력·식별 가능성을 먼저 평가해야 한다. holdout을 이미 열었으므로 새
모형에는 새로운 개발/검증 분리도 필요하다.

## 실행·provenance

- run id: `20260827T121734Z_p012b_stratified_null_holdout`
- range: `[10^9,10^10)` gap starts
- selected records: `31,32,33,34`
- record source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- frozen contract SHA-256:
  `1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`
- analysis source SHA-256:
  `70b8b610df0c7b7ebde987a7e66d39bb551ee0cdf95340d458ca697d79208d19`
- runner SHA-256:
  `69ab72c66ef62b7321ab59b9d08fadfea477c08950b5d1e26b6a2b09f1e92071`
- manifest SHA-256:
  `299e0bbd3e754c0f5f716ddfaea4b09bb4e0cd6adcb6f98e94e6f0a71abc89e5`
- log SHA-256:
  `1e96ebe3f645856eb5e000382ab503e63f657526d77eb84ce604091d4436ff64`
- Monte Carlo: row당 100,000회, seed `20260827`
- analysis elapsed: `240.671`초
- 전체 runner wall time: 파일 시각 기준 약 7분 54초
- GPU: 미사용
- development data used for inference: false
- theorem claimed: false

## 독립 재검증

1. log의 preflight·19 tests·analysis·saved verifier terminal marker: 모두 PASS
2. log의 FAIL·traceback·PowerShell exception: 0건
3. manifest가 결박한 12개 artifact SHA-256: mismatch 0
4. saved report와 직접 계산한 manifest SHA-256: 일치
5. current source·CLI·runner·contract·validated record hash: 실행 log와 일치
6. 현재 고정 코드로 holdout 전체 read-only 재계산: exit 0, issue 0
7. 4개 plateau의 end 산술·right boundary·`N>=M>=1`, `C=M-1`: issue 0
8. 15 components의 hypergeometric 기대값·분산·control exposure: issue 0
9. 12 rows의 기대값·분산·관측·z와 forced-record 제거: issue 0
10. seed 규칙으로 12 row p·9 family p·3 BH family의 100,000회 MC 재생: issue 0
11. gap-start count와 boundary prime count: pinned exact prime count와 일치

## Figure 자동 감사와 설명

1. `p012b_holdout_expected`: gap 288·292·320·336별 관측 recurrence와 동결된 P012 기대값을
   비교한다. gap 336에서만 관측값 1이 나타난다.
2. `p012b_holdout_residuals`: variance가 양수인 행의 standardized residual z를 표시한다.
   x marker는 z=0이 아니라 variance 0으로 z가 미정의인 gap 292 위치다.

자동 검사:

- expected PNG: 1440x990, decode·nonblank·manifest hash PASS
- residual PNG: 1440x990, decode·nonblank·manifest hash PASS
- PDF 2개: header·EOF·manifest hash PASS
- 사용자 시각 QA: `PENDING`

## 연구 질문에 대한 답

1. **독립 범위에서도 P012의 극단적 불일치가 나타났는가?** 5% family 기준에서는 아니다.
2. **record gap recurrence enrichment가 검출됐는가?** 아니다. primary family p `0.09394`,
   최소 BH q `0.27596`이다.
3. **정보 부족이 해결됐는가?** 아니다. 12/12 rows가 LOW_INFORMATION이다.
4. **P012 null이 검증됐는가?** 아니다. non-rejection과 낮은 검정력은 null의 증명이 아니다.
5. **새 수론적 패턴이 발견됐는가?** 현재 자료만으로는 아니다. gap 336의 1회 recurrence는
   후속 가설 후보도 되기 전에 더 많은 독립 정보가 필요하다.

## 권장 후속 방향

1. 사용자가 PNG 두 장의 시각 QA를 수행해 P012-B 결과를 최종 닫는다.
2. recurrence 축은 즉시 더 큰 full sieve로 확장하지 말고, 새 P013에서 pooled/hierarchical
   후보의 검정력과 새 holdout 설계를 먼저 검토한다.
3. 현재 알고리즘 연구의 우선순위는 P010B compressed coverage ledger와 exact PARI witness
   adapter다. count upper bound를 실제 위치 가속으로 연결하는 미해결 조건에 직접 대응한다.
4. P012-B의 frozen contract와 actual 산출물은 사후 수정하지 않는다.
