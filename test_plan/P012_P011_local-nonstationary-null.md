# P012 — log-x stratified conditional recurrence null

## 1. 상태와 사전 고정

`COMPLETED / P012-A_R2_EXPERIMENT_PASS / P012-A_USER_VISUAL_QA_PASS / CONTRACT_FROZEN / P012-B_EXPERIMENT_PASS / P012-B_SAVED_FULL_RECOMPUTATION_PASS / P012-B_USER_VISUAL_QA_PASS`

사용자는 2026-08-27 다음 Q1–Q3 권장안을 결과를 보기 전에 승인했다.

1. P012-A는 기존 `[2,10^9]` 개발 범위에서 P011과 비교하고, 방법을 고정한 뒤
   P012-B `[10^9,10^10]` holdout을 별도로 실행한다.
2. primary log10-bin 폭 0.5, shift 0을 사용한다. 민감도 분석은 폭 0.5/shift 0.25와
   폭 1.0/shift 0.5를 모두 보고하며 희소 bin을 사후 병합하지 않는다.
3. primary는 two-sided family maximum absolute standardized residual이고, secondary는
   one-sided recurrence enrichment와 Benjamini–Hochberg q-value다. seed `20260827`,
   Monte Carlo 100,000회를 사용한다.

P012-A r1 actual은 그림 생성 중 실패했지만 통계 계약을 바꾸지 않은 r2가 terminal·saved
full recomputation PASS했다. 사전 primary에서 관측 9회, P012 기대 8.5874회, family p
0.21945였고 enrichment BH q는 모든 scheme에서 1.0이었다. 결과는 P011 stationary
과대예측이 위치 비정상성에서 주로 왔다는 진단과 일치하지만 저정보 비율이 매우 높아 모형
정당성이나 구조 부재를 증명하지 않는다. `[10^9,10^10]` holdout은 사용자 figure QA와
P012-A 계약 동결 전까지 계속 잠갔다. 사용자는 2026-08-27 r2 figure 시각 QA에 문제가
없음을 확인했고, 통계 계약을 `test_plan/P012_statistical_contract_v1.json`에 동결했다.
그 뒤 사용자가 P012-B actual을 실행했다. terminal·saved full recomputation·독립 산술·독립
Monte Carlo replay가 모두 PASS했다. primary 관측 1 대 기대 0.497022, family p 0.093939,
최소 enrichment BH q 0.275957로 5% 기준 enrichment는 검출되지 않았다. 12/12 row가
LOW_INFORMATION이고 3개는 zero variance이므로 null 채택이나 구조 부재를 주장하지 않는다.

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
- completed r2 runner provenance:
  `test_done/run_p012_stratified_null_development_r2-20260827T054007Z-done.ps1`
- failed r1 provenance:
  `test_done/run_p012_stratified_null_development-20260827T032233Z-failed-done.ps1`

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

### 첫 actual 실패와 r2 교정

- failed log:
  `test_result/logs/run_20260827T032233Z_p012a_stratified_null_development.log`
- partial run:
  `test_result/run_20260827T032233Z_p012a_stratified_null_development`
- 판정: preflight·targeted tests PASS 뒤 plotting TypeError, terminal PASS 없음
- 원인: primary 21행 중 7행의 conditional variance가 0이므로 z가 올바르게 `None`인데
  plotting이 모든 z를 `float`로 강제함
- 교정: P011 bar는 유지하고 P012 undefined bar를 생략하며 x marker와 범례로 명시
- 통계 계약 변경: 없음
- r2 로컬검증: related 14/14, full 116/116, parser 6/6 PASS
- 상세 보고서: `test_result/202608271251_P012A_r1_failure_r2_fix_analysis.md`

## 8. 완료 실행과 사용자 시각 QA

실행 환경: Windows FGKMT Python 고정 PowerShell runner

실행된 명령은 다음과 같다. r2 runner는 `test_done`으로 이관했으므로 다시 실행하지 않는다.

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p012\run_p012_stratified_null_development_r2.ps1 -ConfirmP012A
```

사용자는 2026-08-27 figure 시각 QA를 완료했고 두 그림에 문제가 없음을 확인했다.
확인 대상은 다음 두 파일이었다.

1. `test_result/run_20260827T054007Z_p012a_stratified_null_development_r2/figures/p012_expected_comparison.png`
2. `test_result/run_20260827T054007Z_p012a_stratified_null_development_r2/figures/p012_residual_comparison.png`

축·선·막대·범례와 residual의 주황 x marker 의미를 포함해 `USER_VISUAL_QA_PASS`다.

## 9. 예상 산출물

- `analysis.json`, `summary.json`, `manifest.json`
- `bin_components.csv`, `plateau_statistics.csv`, `cohort_summary.json`
- P006/P011 입력 사본
- `p012_expected_comparison.png/.pdf`
- `p012_residual_comparison.png/.pdf`
- `saved_verification_report.json`

residual comparison에서 conditional variance 0인 P012 z는 막대 0으로 그리지 않는다. 해당
gap의 P011 bar는 유지하고 P012 위치에 `z undefined (variance=0; not z=0)` x marker를
표시한다.

## 10. P012-B holdout 게이트와 구현

P012-A r2 수치·saved verification·사용자 figure QA가 끝났다. primary·sensitivity 계약은
`test_plan/P012_statistical_contract_v1.json`에 동결했고 SHA-256은
`1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`다.

P012-B는 `[10^9,10^10)` gap-start range에서 record start와 다음 record start가 모두
holdout 안인 complete plateaus `31–34`만 사용한다. 왼쪽 continuation과 마지막 censored
plateau를 제외한다. 구현은 다음과 같다.

- plan: `test_plan/P012B_stratified-null-holdout.md`
- analysis: `source/recurrence_stratified_holdout.py`
- CLI: `source/recurrence_stratified_holdout_cli.py`
- tests: `tests/test_recurrence_stratified_holdout.py`
- completed runner provenance:
  `test_done/run_p012_stratified_null_holdout-20260827T121734Z-done.ps1`

preflight는 contract·record metadata만 읽고 holdout prime stream을 열지 않은 채 PASS했다.
range sieve·경계 prime·complete-plateau selection·forced record·approval denial 5/5 tests도
PASS했다. actual에서 분석과 saved full recomputation이 각각 404,204,977 gap starts를
streaming했고, 전체 runner는 약 7분 54초에 완료됐다.

## 11. P012-A r2 actual 결과

- run: `test_result/run_20260827T054007Z_p012a_stratified_null_development_r2`
- log: `test_result/logs/run_20260827T054007Z_p012a_stratified_null_development_r2.log`
- terminal PASS: 확인
- saved deterministic full recomputation: PASS, issues 0
- manifest SHA-256: `723bd82778c92b7ebe3e9f614fd7411e86f5619d3043ed292ddac93fa6966c09`
- modeled/components: 84/128
- primary observed/P012 expected/P011 expected: `9 / 8.587376 / 109.079019`
- primary max-abs-z family p: `0.2194478`
- primary shifted family p: `0.7135429`, `0.4927951`
- 모든 scheme 최소 enrichment BH q: `1.0`
- low-information rows: primary/shifted0.25/width1에서 `28/28`, `28/28`, `26/28`
- holdout touched: false
- 결과보고서: `test_result/202608271655_P012A_r2_result_analysis.md`
- figure 상태: 자동 파일검사 PASS / 사용자 visual QA 2026-08-27 PASS
- frozen contract: `test_plan/P012_statistical_contract_v1.json`
- P012-B actual: EXPERIMENT_PASS / 2026-08-28 사용자 visual QA PASS

## 12. P012-B actual 결과

- run: `test_result/run_20260827T121734Z_p012b_stratified_null_holdout`
- log: `test_result/logs/run_20260827T121734Z_p012b_stratified_null_holdout.log`
- terminal·saved deterministic full recomputation: PASS, issues 0
- 독립 산술·100,000회 Monte Carlo replay: issues 0
- complete plateaus / recurrence: `4 / 1`
- primary observed / expected: `1 / 0.4970217812`
- primary family p / 최소 enrichment BH q: `0.0939390606 / 0.2759572404`
- modeled / LOW_INFORMATION / zero-variance rows: `12 / 12 / 3`
- development data used for holdout inference: false
- 결과보고서: `test_result/202608280019_P012B_holdout_result_analysis.md`
- figure 상태: 자동 QA PASS / 2026-08-28 사용자 visual QA PASS

P012-A와 P012-B 모두 사전 고정 5% 기준에서 enrichment를 검출하지 못했다. 그러나 P012-B는
complete plateau가 4개뿐이고 모든 행이 저정보다. 따라서 “독립 holdout에서 극단적 불일치는
보이지 않았다”까지만 말하며 모형 채택·구조 부재·수론 정리를 주장하지 않는다. 다음 recurrence
연구는 이 holdout을 개발자료로 재사용하지 않고 새 P013의 검정력·식별가능성 설계부터 시작한다.
