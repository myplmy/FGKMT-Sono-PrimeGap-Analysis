# P012 — log-x stratified conditional recurrence null

## 1. 상태와 사전 고정

`APPROVED / IMPLEMENTED / LOCALLY_VERIFIED / USER_RUN_READY / P012-A_NOT_RUN / HOLDOUT_UNTOUCHED`

사용자는 2026-08-27 다음 Q1–Q3 권장안을 결과를 보기 전에 승인했다.

1. P012-A는 기존 `[2,10^9]` 개발 범위에서 P011과 비교하고, 방법을 고정한 뒤
   P012-B `[10^9,10^10]` holdout을 별도로 실행한다.
2. primary log10-bin 폭 0.5, shift 0을 사용한다. 민감도 분석은 폭 0.5/shift 0.25와
   폭 1.0/shift 0.5를 모두 보고하며 희소 bin을 사후 병합하지 않는다.
3. primary는 two-sided family maximum absolute standardized residual이고, secondary는
   one-sided recurrence enrichment와 Benjamini–Hochberg q-value다. seed `20260827`,
   Monte Carlo 100,000회를 사용한다.

P012-A actual은 아직 실행하지 않았다. `[10^9,10^10]` holdout은 코드·계획 조정에
사용하지 않았고 P012-A 분석과 방법 동결이 끝날 때까지 잠근다.

## 2. 연구 질문과 비목적

P011은 `[2,10^9]` 전체 gap frequency를 초기 plateau에도 동일하게 적용해 큰 음수
residual을 만들었다. P012는 위치대별 관측 gap count를 고정한 조건부 null로 바꾸면
이 과대예측이 줄어드는지 조사한다.

비목적:

- prime gap의 독립성·정상성 또는 Poisson 정리를 주장하지 않는다.
- p-value를 수론 정리나 maximal-gap 법칙의 증명으로 사용하지 않는다.
- 개발 자료 `[2,10^9]`의 적합성을 독립 재현으로 부르지 않는다.
- P012-A 결과를 본 뒤 bin 폭·shift·primary statistic을 변경하지 않는다.

## 3. 고정 조건부 null

complete plateau `i`의 start-prime exposure를 `[s_i,s_(i+1))`, record gap을 `g_i`라
한다. 고정 log bin `b`에서 다음을 센다.

- `N_b`: bin의 모든 consecutive-prime gap start 수
- `K_ib`: gap 크기가 `g_i`인 start 수
- `n_ib`: plateau `i`와 bin이 겹치는 gap start 수
- `C_ib`: 그 겹침에서 관측한 gap `g_i` 수

record 최초 발생 `s_i`는 선택으로 강제된 사건이므로 그 bin에서 `N,K,n,C` 각각 1을
뺀다. 이후 같은 기호로 보정된 값을 쓰면

\[
C_{ib}\mid N_b,K_{ib},n_{ib}
\sim \operatorname{Hypergeometric}(N_b,K_{ib},n_{ib}).
\]

plateau가 여러 bin을 지나면 독립 component 합을 진단 null로 사용한다. 기대값과 분산은

\[
E_i=\sum_b n_{ib}\frac{K_{ib}}{N_b},
\]

\[
V_i=\sum_b n_{ib}\frac{K_{ib}}{N_b}
\left(1-\frac{K_{ib}}{N_b}\right)
\frac{N_b-n_{ib}}{N_b-1}
\]

이고 `z_i=(C_i-E_i)/sqrt(V_i)`다. bin별 교환가능성과 gap category 사이의 독립
simulation은 경험적 근사이며 정리가 아니다.

## 4. cohort와 정보 부족 규칙

P011과 직접 비교하기 위해 cohort를 그대로 유지한다.

- primary: `start_prime >= 1000`
- all eligible: gap 1과 trial 0 제외
- sensitivity: `start_prime >= 100000`

결과를 보기 전에 다음 설명용 플래그를 고정한다.

- 보정 후 같은 gap occurrence가 5개 미만인 component
- 또는 plateau 바깥 control exposure가 1,000개 미만인 component

은 `LOW_INFORMATION`으로 표시한다. 이 플래그는 bin 병합이나 test family 제외에 쓰지
않는다. 분산 0인 row만 z-family 계산에서 수학적으로 제외하고 row 자체는 보존한다.

## 5. 입력·provenance

- P006 complete plateaus:
  `test_result/run_20260824T065339Z_p006_full_1000000000/tables/complete_plateaus.csv`
- SHA-256: `4675e8b6e7284b31c61ad66f3f98ffa34114553d49ab32878c609608530daca6`
- P011 stationary statistics:
  `test_result/run_20260826T100938Z_p011_recurrence_null_pilot/plateau_null_statistics.csv`
- SHA-256: `2fa3cfca10f83b91dd2f10310009370b2614549dee62d243b6f890b41ee5b302`
- analysis limit: `10^9`, pinned `pi(10^9)=50,847,534`
- generator: P006 NumPy odd-only segmented sieve, segment span 50,000,000
- Python: `W:\miniforge3\envs\FGKMT\python.exe`

전체 gap start 위치를 저장하지 않고 prime stream을 한 번 훑어 bin별 충분통계만 누적한다.

## 6. 구현과 영향도 판정

- 구현: `source/recurrence_stratified_null.py`
- CLI: `source/recurrence_stratified_null_cli.py`
- tests: `tests/test_recurrence_stratified_null.py`
- runner: `scripts/experiments/p012/run_p012_stratified_null_development.ps1`

영향도:

| 축 | 판정 | 근거 |
|---|---|---|
| FGKMT 반복로그·end-bounded H | 영향 없음 | 별도 P006 recurrence 통계축 |
| start/end plateau 의미론 | 영향 있음 | P006 start exposure `[s_i,s_(i+1))`를 그대로 검증 |
| provenance | 영향 있음 | P006/P011 입력 hash 고정 |
| 큰 정수·고정밀도 | 영향 없음 | `x<=10^9`, exact integer counts |
| 통계 재현성 | 영향 있음 | bin·seed·replications·family 사전 고정 |
| 승인 경계 | 영향 있음 | actual CLI와 runner 이중 승인 gate |
| 정리/경험 구분 | 영향 있음 | 모든 p/q를 진단값으로 제한 |

## 7. 사전검증·성공·중단 기준

사전검증:

1. P006/P011 입력 hash 일치
2. P006 모든 plateau에서 `N>=M>=1`, `C=M-1`
3. bin component 합이 각 plateau의 `N-1`, `C`와 정확히 일치
4. 생성 prime/gap 수가 pinned `pi(10^9)`와 일치
5. toy bin-crossing·forced-record 제거·고정 seed 재현성 PASS
6. 승인 플래그 없이는 입력 읽기·출력 생성 전 거부

실행 성공:

- terminal PASS
- saved artifact hash issue 0
- saved full deterministic recomputation PASS
- 세 bin scheme과 세 cohort 모두 저장
- P011/P012 같은 cohort 직접 비교표 생성
- holdout touched=false

중단:

- 입력 hash·prime count·P006 invariant 불일치
- component 합 불일치
- 기존 result directory 충돌
- 100,000 replications 또는 seed 변경
- `[10^9,10^10]` 자료 접근

## 8. 사용자 실행 절차

환경: Windows PowerShell 또는 FGKMT Conda Prompt

시작 경로: `Z:\FGKMT-Sono-PrimeGap-Analysis`

예상시간: 약 1–10분

예상 RAM: 4 GB 미만

예상 disk: 2 GB 미만

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p012\run_p012_stratified_null_development.ps1 -ConfirmP012A
```

회신할 것:

1. 마지막 `[PASS]` 또는 첫 `[FAIL]`
2. log와 result directory
3. `summary.json` 경로
4. PNG 두 장의 축·선·범례가 정상인지 시각 확인

## 9. 예상 산출물

- `analysis.json`, `summary.json`, `manifest.json`
- `bin_components.csv`, `plateau_statistics.csv`, `cohort_summary.json`
- P006/P011 입력 사본
- `p012_expected_comparison.png/.pdf`
- `p012_residual_comparison.png/.pdf`
- `saved_verification_report.json`

## 10. P012-B holdout 게이트

P012-A 결과와 saved verification을 감사한 뒤 코드·통계 계약을 동결한다. 그 후에만
`[10^9,10^10]`의 새 prime-gap sufficient statistics를 만들 수 있다. P012-B에는
P012-A에서 보고된 이상에 맞춰 bin이나 statistic을 바꾸지 않는다. P006 `10^9` 실측
2.70초와 선형 규모를 고려하면 P012-B도 3시간 이상일 가능성은 낮지만, A 실제 로그로
runner 전체시간을 다시 보정한다.
