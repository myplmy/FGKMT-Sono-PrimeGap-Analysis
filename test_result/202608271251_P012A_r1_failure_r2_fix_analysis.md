# P012-A r1 실패 원인 및 r2 교정 분석

## 판정

`USER_RUN_FAILED / ANALYSIS_STAGE_PARTIAL / PLOTTING_BUG_CONFIRMED / STATISTICAL_DEFINITION_UNCHANGED / R2_LOCALLY_VERIFIED / USER_RERUN_REQUIRED / HOLDOUT_UNTOUCHED`

사용자 실행 `run_20260827T032233Z_p012a_stratified_null_development`는 입력 preflight와
targeted 13 tests까지 PASS했지만 `p012-development-analysis`의 그림 생성 중 종료코드 1로
실패했다. terminal P012-A PASS, `summary.json`, `manifest.json`, saved verification report와
완성 figure가 없으므로 이 실행은 P012-A 결과로 채택하지 않는다.

## 실패 증거

- log: `test_result/logs/run_20260827T032233Z_p012a_stratified_null_development.log`
- log SHA-256: `d0fe9f3ff69c834bb649cfa774c726370fd7ceef9c25eed869fdb8f41a42c6f9`
- partial run: `test_result/run_20260827T032233Z_p012a_stratified_null_development`
- 마지막 PASS stage: `p012-targeted-unit-tests`
- 첫 FAIL stage: `p012-development-analysis`
- 예외: `TypeError: float() argument must be a string or a real number, not 'NoneType'`
- terminal PASS: 없음

partial run에는 입력 사본과 `analysis.json`, `bin_components.csv`, `plateau_statistics.csv`,
`cohort_summary.json`이 기록됐지만 다음 필수 산출물은 없다.

| 필수 산출물 | 존재 |
|---|---|
| `summary.json` | 아니오 |
| `manifest.json` | 아니오 |
| `saved_verification_report.json` | 아니오 |
| 두 PNG·두 PDF | 아니오 |

partial 파일은 원인 진단용 provenance로만 보존한다. manifest hash와 saved full
recomputation을 통과하지 않았으므로 그 안의 p-value나 cohort 요약을 연구 결론으로 인용하지
않는다.

## 정확한 원인

P012는 각 maximal-gap record의 강제된 최초 발생을 조건부 null에서 제거한다. gap 44, 72,
112, 114, 118, 180, 220은 primary scheme·cohort에서 이 제거 뒤 관련 log-bin의 같은 gap
occurrence가 모두 0개였다. 따라서 일곱 행은

```text
observed recurrence = 0
expected recurrence = 0
conditional variance = 0
standardized residual z = undefined (None)
```

가 된다. 이는 `z=(0-0)/sqrt(0)`이므로 `z=0`이 아니라 **수학적으로 미정의**다. 계획서는
이미 variance 0인 행을 z-family에서 제외하되 행 자체는 보존하도록 고정했다. 분석 코드가
`None`을 저장한 것은 올바르다.

결함은 `_plot_comparison`이 primary 21행 모두를 `float(...)`로 바꾸려 한 데 있다. 14개
정의된 z에는 문제가 없었지만 7개의 `None`에서 예외가 발생했다. P011 z는 21행 모두 숫자였다.

## 수정 선택과 영향도

| 방법 | 통계 정확성 | 정보 보존 | 판정 |
|---|---|---|---|
| `None`을 0으로 바꿈 | 미정의를 z=0으로 오표기 | 겉보기만 완성 | 기각 |
| 해당 gap 전체를 그림에서 삭제 | 수치 왜곡은 없음 | P011 비교도 숨김 | 기각 |
| P011 bar 유지, P012 bar 생략, x marker로 `variance=0` 명시 | 정의 보존 | gap·비교 모두 보존 | 채택 |

수정은 그림 표현만 바꾼다. 다음은 바뀌지 않았다.

- P012 bin 폭·shift·cohort
- forced first-record 제거 규칙
- hypergeometric 기대값·분산
- seed `20260827`, Monte Carlo 100,000회
- z-family에서 variance 0행 제외
- 입력 hash와 `[2,10^9]` 범위
- `[10^9,10^10]` holdout 잠금

따라서 결과를 보고 통계방법을 사후 변경한 것이 아니며 사용자의 Q1–Q3 승인은 그대로
유효하다.

## 구현 교정

- 수정: `source/recurrence_stratified_null.py`
- 회귀시험: `tests/test_recurrence_stratified_null.py`
- 새 runner: `scripts/experiments/p012/run_p012_stratified_null_development_r2.ps1`
- r2 SHA-256: `0af40c63e02b962c2c1716d868c15a8dabc4a52302e2b87e9e9be36201ab8e28`

residual figure에서 P012 z가 정의된 14행만 주황 막대로 그린다. 미정의 7행에는 숫자 막대를
그리지 않고 y=0 위치에 주황 x marker를 표시하며 범례와 제목에서 `variance=0; not z=0`임을
명시한다. x marker의 높이는 수치 z=0을 의미하지 않는다.

## 실행 원본 보존

실패 r1 runner는 원 hash를 유지한 채 다음으로 이관했다.

- `test_done/run_p012_stratified_null_development-20260827T032233Z-failed-done.ps1`
- SHA-256: `61ff041f32813d377d9414e700638dac359961cd29699778ae0969b40404a9f3`

이 파일은 실패 당시 provenance이며 다시 실행하지 않는다.

## 로컬 검증

고정 Python: `W:\miniforge3\envs\FGKMT\python.exe` 3.11.16

1. 수정 전 새 회귀시험: 사용자와 동일한 `float(None)` TypeError 재현
2. 수정 후 같은 시험: PNG/PDF 4개 생성 PASS, 입력 row의 `None` 보존
3. 관련 tests: 14/14 PASS, 0.901초
4. 전체 unittest: 116/116 PASS, 5.595초
5. Python `py_compile`: PASS
6. active PowerShell parser: 6/6 PASS, issue 0
7. r2 승인 플래그 누락: exit 1, 새 log 0개, 새 run directory 0개

Windows sandbox의 첫 임시 디렉터리 시험은 기존 ACL `PermissionError [WinError 5]`로 코드
도달 전 실패했다. 정상 Windows 권한에서 동일 시험을 실행해 수정 전 TypeError와 수정 후
PASS를 각각 확인했으므로 ACL 문제와 코드 결함을 분리했다.

## 아직 하지 않은 일

- P012-A r2 actual 실행 안 함
- partial r1을 saved PASS로 승격하지 않음
- r1 partial 수치를 결과로 해석하지 않음
- P012-B holdout 접근·실행 안 함
- 새 figure 사용자 시각 QA 안 함

## 다음 판정 기준

r2가 terminal PASS, manifest artifact hash issue 0, saved full recomputation PASS를 모두 기록한
뒤에만 P012-A `EXPERIMENT_PASS` 여부를 판단한다. 그 뒤 사용자가 두 PNG를 시각 확인해야
figure QA를 PASS로 표시할 수 있다.
