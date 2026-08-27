# P012-B — Stratified conditional recurrence null 독립 holdout

## 1. 상태

`COMPLETED / EXPERIMENT_PASS / SAVED_FULL_RECOMPUTATION_PASS / INDEPENDENT_ARITHMETIC_PASS / INDEPENDENT_MC_REPLAY_PASS / USER_VISUAL_QA_PENDING`

P012-A 수치·saved 재계산·독립 감사와 사용자 figure 시각 QA가 모두 PASS했다. 통계 계약은
`test_plan/P012_statistical_contract_v1.json`에 동결했고 SHA-256은
`1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`다.

P012-B 모듈·CLI·승인형 PowerShell runner를 구현하고, holdout prime stream을 읽지 않는
preflight와 toy·approval-denial 검증을 통과했다. 사용자가 `[10^9,10^10)` actual을 실행했고,
terminal·saved full recomputation·독립 산술·독립 Monte Carlo replay가 모두 issue 0으로
PASS했다. 자동 figure QA는 PASS했으며 사용자 시각 QA만 남았다.

## 2. 연구 질문과 비목적

연구 질문:

1. P012-A에서 P011 stationary 과대예측이 사라진 현상이 독립 holdout에서도 유지되는가?
2. 고정한 local-stratified null에서 recurrence enrichment가 검출되는가?
3. LOW_INFORMATION과 zero-variance 비율이 더 큰 범위에서 개선되는가?

비목적:

- P012 null이 참이거나 prime gap이 독립이라고 주장하지 않는다.
- 유한 p/q값으로 수론 정리나 무한범위 법칙을 증명하지 않는다.
- holdout 결과를 본 뒤 bin·cohort·seed·검정 family를 바꾸지 않는다.
- P011 개발자료를 holdout 기대값 계산에 재사용하지 않는다.

FGKMT 본체의 canonical 정의

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n),\qquad
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},\qquad H(x)=G(x)/F(x)
\]

에서 `log_k`는 자연로그를 k회 반복한다. P012-B는 별도 start-exposure recurrence 통계축이며
이 정의를 변경하지 않는다.

## 3. 동결된 통계 계약

- holdout gap-start 범위: `[10^9,10^10)`
- primary bin: log10 폭 0.5, shift 0
- sensitivity: 폭 0.5/shift 0.25, 폭 1.0/shift 0.5
- primary cohort: `start_prime>=1000`
- primary statistic: two-sided family maximum absolute z
- secondary: one-sided enrichment와 Benjamini–Hochberg q
- seed: `20260827`
- Monte Carlo: row당 100,000회
- 최초 record 발생: 해당 bin의 `N,K,n,C`에서 각각 1 제거
- variance 0: row를 보존하고 z=`null`, z-family에서만 제외
- LOW_INFORMATION: conditioned gap 5 미만 또는 control exposure 1,000 미만;
  test membership은 바꾸지 않음

holdout의 모든 선택 record가 `10^9`보다 크므로 세 고정 cohort는 같은 행을 포함한다. 이
중복은 계약을 사후 변경하지 않기 위해 그대로 저장하고 해석 때 명시한다.

## 4. Dataset·provenance·완전성

- canonical record source: `prime-gap-list-project/prime-gap-list`
- commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records:
  `datas/validated/prime-gap-list-project/1a112a1387052d9ad360686313f501c01fe46b68/maximal_gap_records.csv`
- validated SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- source exhaustive coverage: `10^20`, holdout endpoint보다 큼
- pinned exact prime count:
  `pi(10^10)-pi(10^9)=455052511-50847534=404204977`
- 외부 다운로드: 필요 없음

모든 consecutive gap start는 Windows NumPy odd-only segmented sieve로 직접 생성한다.
holdout 아래의 prime은 생성하지 않으며, `10^10` 아래 마지막 start의 gap을 닫기 위해
오른쪽의 첫 소수 하나만 추가 생성한다.

## 5. Plateau 입력 필터와 경계

record `i`의 start exposure는 `[s_i,s_(i+1))`다. P012-B primary에는

```text
s_i >= 10^9 and s_(i+1) < 10^10
```

를 만족하는 complete plateau만 포함한다. pinned record indices는 `31,32,33,34`다.

- `10^9`에서 첫 holdout record 전까지의 왼쪽 continuation: left-censored이므로 제외
- record 35: 다음 record start가 `10^10` 밖이므로 right-censored로 제외
- end-bounded FGKMT plateau와 start-exposure를 같은 것으로 부르지 않음

## 6. 구현과 영향도

- frozen contract: `test_plan/P012_statistical_contract_v1.json`
- analysis: `source/recurrence_stratified_holdout.py`
- CLI: `source/recurrence_stratified_holdout_cli.py`
- tests: `tests/test_recurrence_stratified_holdout.py`
- completed runner provenance:
  `test_done/run_p012_stratified_null_holdout-20260827T121734Z-done.ps1`

P012-A source·saved 결과는 변경하지 않는다. P012-B는 validated record metadata와 새 holdout
prime stream만 사용하고 P006/P011 개발 통계 table을 입력하지 않는다.

## 7. 사전검증·성공·중단 기준

사전검증:

1. frozen contract와 validated record hash 일치
2. 선택 record indices가 정확히 `31,32,33,34`
3. actual 전 preflight는 holdout prime stream을 읽지 않음
4. range sieve가 `[lower,upper)` prime과 오른쪽 boundary prime 하나를 보존
5. gap-start count가 정확히 `404,204,977`
6. 각 bin scheme population 합이 같은 gap-start count와 일치
7. 각 plateau `N>=M>=1`, `C=M-1`; forced record 정확히 1회 제거
8. 승인 flag 없이는 입력 읽기·출력 생성 전 거부

성공:

- terminal `[PASS] P012-B independent stratified-null holdout completed.`
- analysis와 saved full deterministic recomputation 모두 PASS
- manifest artifact hash issue 0
- selected indices `31–34`, 세 scheme·세 cohort 저장
- `development_data_used_for_holdout_inference=false`
- `holdout_touched=true`, `theorem_claimed=false`, `gpu_used=false`

중단:

- contract·record hash 또는 record selection 변경
- prime/gap count·population·N/M/C 불일치
- 기존 result/log 경로 충돌
- seed·replications·bin·cohort 변경
- RAM 8 GB, disk 2 GB 또는 전체 runner 4시간 초과
- development P006/P011 table을 기대값 입력으로 사용하려는 경우

## 8. 완료 실행과 사용자 시각 QA

실행 환경은 Windows PowerShell 또는 FGKMT Conda Prompt였다. 완료 runner는 hash를 보존해
`test_done`으로 이관했으므로 다시 실행하지 않는다.

실행 이력 명령은 다음과 같다.

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p012\run_p012_stratified_null_holdout.ps1 -ConfirmP012B
```

분석 단계는 약 240.7초였고 로그·파일 시각으로 본 전체 runner는 약 7분 54초였다. 분석과
saved verification이 각각 holdout 전체를 한 번씩 streaming했다. RAM·disk 제한을 넘지 않았고
GPU를 사용하지 않았다.

사용자는 2026-08-28 아래 두 PNG의 시각검사를 완료했고 두 그림에 문제가 없음을 확인했다.

1. `test_result/run_20260827T121734Z_p012b_stratified_null_holdout/figures/p012b_holdout_expected.png`
2. `test_result/run_20260827T121734Z_p012b_stratified_null_holdout/figures/p012b_holdout_residuals.png`

축·선·막대·범례, residual 그림의 `variance=0; z undefined` x marker와 요소 잘림을
확인한 사용자 판정은 `PASS`다.

## 9. 예상 산출물

- `input_validated_records.csv`, `input_frozen_contract.json`
- `analysis.json`, `summary.json`, `manifest.json`
- `holdout_plateaus.csv`, `bin_components.csv`, `plateau_statistics.csv`
- `cohort_summary.json`
- expected/residual PNG·PDF 4개
- `saved_verification_report.json`
- `test_result/logs/run_<UTC>_p012b_stratified_null_holdout.log`

## 10. 판정 기준과 후속 작업

- family p와 BH q는 사전 고정 기준 그대로 보고하고 유의하지 않음을 null 채택으로 쓰지 않는다.
- LOW_INFORMATION·zero-variance 비율을 효과값과 같은 비중으로 보고한다.
- P012-A와 방향이 같으면 “독립 유한범위 재현”으로만 표현한다.
- 방향이 다르면 실패를 숨기지 않고 위치·표본수·검정력 차이를 분석한다.
- actual 결과 뒤 새 bin 또는 pooled model이 필요하면 P012-B를 바꾸지 않고 새 실험번호로 분리한다.

## 11. 실제 실행 결과

- run: `test_result/run_20260827T121734Z_p012b_stratified_null_holdout`
- log: `test_result/logs/run_20260827T121734Z_p012b_stratified_null_holdout.log`
- log SHA-256: `1e96ebe3f645856eb5e000382ab503e63f657526d77eb84ce604091d4436ff64`
- terminal PASS: 확인
- saved deterministic full recomputation: PASS, issues 0
- manifest SHA-256: `299e0bbd3e754c0f5f716ddfaea4b09bb4e0cd6adcb6f98e94e6f0a71abc89e5`
- selected complete plateaus: 4 (`31–34`)
- gap starts / selected plateau exposure: `404,204,977 / 138,659,994`
- recurrence: gap 336에서 1건; 나머지 288·292·320은 0건
- primary observed / expected: `1 / 0.4970217812`
- primary family p / 최소 enrichment BH q: `0.0939390606 / 0.2759572404`
- modeled / LOW_INFORMATION / zero-variance rows: `12 / 12 / 3`
- 독립 산술·100,000회 Monte Carlo replay: issues 0
- 개발자료 사용: false
- theorem claim / GPU: false / false
- 결과보고서: `test_result/202608280019_P012B_holdout_result_analysis.md`
- figure 상태: 자동 파일검사 PASS / 2026-08-28 사용자 visual QA PASS

사전 고정한 5% 기준에서 recurrence enrichment는 검출되지 않았다. 모든 행이 저정보이므로
이는 null 채택, 모형 정당성 또는 recurrence 구조 부재의 증명이 아니다. 후속 모형이나 범위는
P012-B를 소급 변경하지 않고 새 P013 개발/검증 분리로 설계한다.
