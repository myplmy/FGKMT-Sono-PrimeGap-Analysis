# P020 — 기존 recurrence artifact 전수 종합 시각화 수준 A

최종 갱신: 2026-09-02 KST

## 1. 상태와 승인

`EXPERIMENT_PASS / SYNTHESIS_ONLY / USER_VISUAL_QA_PENDING`

사용자는 2026-09-02 기존 recurrence artifact 전수 종합 시각화 수준 A의 계획·코드·figure 생성을
승인했다. 이 승인은 저장된 성공 artifact를 읽는 P020에 한정되며 새 prime sweep, P018-B,
P013-C, P019 actual을 허가하지 않는다.

정본 contract:

```text
test_plan/P020_recurrence_artifact_synthesis_contract_v1.json
SHA-256: `5dc9c131b5f0c5eb4580af6cd0e971a40b8c079f2189846e088ea12313f6eacc`
```

## 2. 연구 질문

1. P006에서 P018-A까지 recurrence 연구가 범위·모형·독립성·정보량 면에서 어떻게 변했는가?
2. stationary null에서 stratified conditional null로 바꿨을 때 기대 recurrence가 얼마나 교정됐는가?
3. 계산한 gap-start 수가 크게 늘어도 왜 positive-variance row와 기대 정보량이 줄었는가?
4. P018-A에서 수백억 gap-start를 처리하고도 forced record 제거 뒤 정보량이 0이 된 구조를
   한눈에 설명할 수 있는가?

## 3. 비목적

- 모든 prime gap raw point를 복원하거나 새 x-bin을 만드는 것
- 서로 다른 null·범위·cohort의 p-value를 합쳐 추세를 만드는 것
- P018-A에서 저장하지 않은 관측 recurrence, residual, p/q/z를 사후 생성하는 것
- recurrence 부재, 독립성 또는 수론 정리를 증명하는 것
- P018-B를 자동 승격하거나 실행하는 것

## 4. 입력과 provenance

입력은 contract에 고정한 성공 run 8개뿐이다. 각 입력은 `manifest.json` SHA-256, manifest가
고정한 모든 artifact hash, 원 실행에서 보존한 saved-verifier PASS 증거를 통과해야 한다.
P012/P013의 기존 `verify_saved_*` 함수는 이름과 달리 전체 prime range를 재계산하므로 P020에서
호출하지 않는다. 실패한 P012-A r1, P013-A r1, P017 재계산 child는 정본 입력이 아니다.

| 입력 | 역할 | manifest SHA-256 |
|---|---|---|
| P006 full | descriptive development | `4492d1a9...9233bde` |
| P011 | stationary-null diagnostic | `3b7b982d...67aa78a0` |
| P012-A r2 | stratified development | `723bd827...a6966c09` |
| P012-B | holdout | `299e0bbd...1abc89e5` |
| P013-A r2 | prospective | `86da30eb...4a8dbdd` |
| P013-B | prospective | `a4272808...76c6d760` |
| P018-P0 | calibration margin-only | `4c871c55...ae2d832b` |
| P018-A | prefix information margin-only | `c0a1309d...c10b75ad` |

P006·P012-B·P013-A/B·P018-A만 중복 없는 처리량 회계에 포함한다. P011·P012-A는 P006 결과를
재사용하고, P018-P0는 P018-A의 부분범위다. 동결 기대 합계는 `72,178,455,399` gap-start다.
이 값은 저장 raw 행 수가 아니라 각 정본 실행이 보고한 처리량 회계다.

## 5. 수학·통계 불변식

- canonical end-bounded `G(x)`와 iterated-log `F/H`는 변경하지 않는다.
- P006 plateau 경계와 recurrence start exposure의 차이를 보존한다.
- primary 비교는 `primary_width_0p5_shift_0`, `primary_start_ge_1000`을 사용한다.
- P011과 P012-A는 같은 development 범위의 모형 교정 비교로만 사용한다.
- P012-B, P013-A/B는 각 stage의 관측합과 primary 기대합을 나란히 표시하되 p-value를 연결하지 않는다.
- zero variance는 결측이 아니라 정확한 0 정보 상태다. `z=None`을 0으로 바꾸지 않는다.
- P018은 margin과 gate만 사용하고 `margin-only / allocation-blinded information`으로 표시한다.
- `10^9` raw-stream 경계의 `999,999,937 -> 1,000,000,007` gap 70 한 건을 coverage 그림에 주석한다.

## 6. 고정 figure 묶음

1. `01_recurrence_coverage_map`: log-x 범위, experiment role, 중복/부분범위, `10^9` 경계 주석
2. `02_p006_descriptive_recurrence`: P006 29개 complete plateau의 `M`, `C`, `R`
3. `03_null_model_correction`: 같은 development rows의 관측값, P011 기대, P012-A 기대
4. `04_prospective_stage_summary`: P012-B·P013-A/B primary 관측합과 기대합
5. `05_information_collapse`: stage별 기대합, positive-variance 비율, LOW_INFORMATION 비율
6. `06_p018_forced_record_funnel`: P018-A gap 582·588의 exposure/control, target 1→forced 1→conditioned 0

각 figure는 PNG와 PDF를 생성한다. 서로 다른 p-value를 한 figure에 pool하지 않는다.

## 7. 사전검증과 중단조건

1. 고정 Python이 `W:\miniforge3\envs\FGKMT\python.exe`이고 requirements와 일치
2. contract SHA-256과 8개 manifest SHA-256 일치
3. 8개 manifest의 모든 artifact hash와 기존 saved-verifier PASS 증거 일치
   - P020 preflight는 prime-range full recomputation을 호출하지 않음
4. contract가 허용한 P018 파일 외에는 adapter가 읽지 않음
5. source 정적감사에서 금지 base-log 구현 0건
6. toy fixture에서 표·figure 6종·saved verifier PASS, 덮어쓰기 거부 PASS
7. 입력 row key·scheme·cohort·range·처리량이 동결값과 다르면 계산 전에 FAIL
8. result directory나 log가 이미 존재하면 덮어쓰지 않고 FAIL

## 8. 실행 환경과 명령

환경: Windows PowerShell, 저장소 루트, 고정 FGKMT Python. 예상 full path는 수초~수분,
hard wall은 15분이다. CPU-heavy prime 계산은 없다.

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m source.recurrence_artifact_synthesis_cli preflight `
  --project-root 'Z:\FGKMT-Sono-PrimeGap-Analysis' `
  --contract 'test_plan\P020_recurrence_artifact_synthesis_contract_v1.json'

& 'W:\miniforge3\envs\FGKMT\python.exe' -m source.recurrence_artifact_synthesis_cli run `
  --project-root 'Z:\FGKMT-Sono-PrimeGap-Analysis' `
  --contract 'test_plan\P020_recurrence_artifact_synthesis_contract_v1.json' `
  --result-directory 'test_result\run_<UTC>_p020_recurrence_artifact_synthesis'
```

실제 run은 stdout/stderr를 `test_result/logs/run_<UTC>_p020_recurrence_artifact_synthesis.log`에
함께 보존한다.

## 9. 예상 산출물

- `input_inventory.json`: 입력 경로, manifest hash, saved verifier 결과, 접근 계약
- `tables/coverage_ranges.csv`
- `tables/p006_descriptive_recurrence.csv`
- `tables/null_model_correction.csv`
- `tables/prospective_stage_summary.csv`
- `tables/information_collapse.csv`
- `tables/p018_forced_record_funnel.csv`
- PNG/PDF figure 12개
- `summary.json`, `artifact_qa.json`, `manifest.json`, `saved_verification_report.json`
- 결과 분석보고서와 결과 색인 행

## 10. 성공·경고·판정 기준

성공:

- 모든 입력 hash/saved verifier PASS
- 표의 정수·기대값을 입력에서 독립 재계산해 exact/허용오차 일치
- figure 6종 PNG/PDF 존재, PNG decode·크기·비공백, PDF header/EOF PASS
- 저장 artifact hash와 saved recomputation PASS
- 처리량 합계 `72,178,455,399`, P018 conditioned count 0, primary stage totals 동결값 일치

과학적 판정은 `EXPERIMENT_PASS / SYNTHESIS_ONLY / NO_NEW_PRIME_COMPUTATION`이다. 그림이 구조를
명확히 보여도 recurrence 부재나 theorem을 주장하지 않는다. 자동 QA 후 사용자 시각 QA 전에는
`VISUAL_QA_PENDING_USER`로 기록한다.

## 11. 후속 결정

P020을 본 뒤 새 streaming level B가 실제로 답할 독립 질문이 생길 때만 별도 계획과 승인을
검토한다. 단지 더 촘촘한 그림을 위해 10–16시간 prime sweep를 자동 제안하지 않는다.

## 12. R1 생성 후 시각 배치 교정 — 2026-09-02

첫 P020 run은 모든 수치·hash·saved recomputation이 PASS했지만 Codex 육안검사에서 다음 전달 문제를
발견했다.

- coverage map의 좁은 P018 막대 라벨 잘림과 `10^9` seam 주석 겹침
- null 교정 합계 상자가 큰 P011 peak 일부를 가림
- LOW_INFORMATION 열이 전 행 100%일 때 degenerate column normalization이 옅은색으로 표시됨

R1 artifact는 소급 수정하지 않는다. 표·contract·입력·수치 계산은 그대로 두고 label placement,
annotation placement, constant-1 fraction color만 교정한 `R2_VISUAL_LAYOUT`을 새 run ID로 생성한다.
R2의 saved table/summary recomputation은 R1과 같은 과학 수치를 요구한다.

## 13. 실제 실행 결과 — 2026-09-02

정본은 R2다.

```text
run = test_result/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis
log = test_result/logs/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis.log
runner_revision = R2_VISUAL_LAYOUT
manifest_sha256 = 4fe08a450b01d2d483018c61240c53a8e2b75a4c05864b096775280a9466a101
new_prime_computation = false
terminal_status = PASS
saved_verification = PASS
visual_qa = PENDING_USER
```

입력 manifest·모든 등록 artifact hash·원 saved-verifier 증거, 표·summary full recomputation,
P018 margin-only output contract, PNG/PDF 12파일의 자동 QA가 모두 PASS했다. 중복 없는 처리량
회계는 `72,178,455,399` gap-start다. P011 stationary 기대 109.0790은 P012 층화 후 8.58738로
92.1274% 줄었고, P012-B·P013-A/B prospective 기대는 0.49702·0.07783·0.06680이었다.
P018 gap 582·588은 forced record 제거 후 conditioned count와 분산이 0이므로 B 자동승격은 없다.

정본 해석은
`test_result/202609021151_P020_recurrence_artifact_synthesis_result_analysis.md`에 있다. Codex의
수치·파일·배치 점검은 완료했지만, 사용자 시각 확인 전에는 figure QA를 PASS로 올리지 않는다.

## 14. 사용자 시각 QA — 2026-09-02

사용자가 R2의 여섯 figure를 확인하고 `문제 없음`으로 회신했다.

```text
visual_qa = PASS
visual_qa_source = USER_CONFIRMATION
visual_qa_date = 2026-09-02
```

이 사후 상태 기록은 동결된 P020 계산 계약·수치·manifest를 바꾸지 않는다.
