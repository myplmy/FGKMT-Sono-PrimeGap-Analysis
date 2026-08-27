# P013 — Prospective stratified recurrence decade extension

## 1. 상태

`WAITING_FOR_USER_EXECUTION / PRE-REGISTERED / IMPLEMENTED / LOCALLY_VERIFIED / ACTUAL_NOT_RUN`

## 2. 연구 질문과 비목적

연구 질문:

1. P012에서 고정한 stratified conditional null이 새 decade에서도 극단적으로 어긋나지 않는가?
2. 범위 확대가 LOW_INFORMATION·zero-variance 비율을 실제로 줄이는가?
3. recurrence 관측·기대의 위치별 변화가 후속 모형을 정당화할 만큼 커지는가?

비목적:

- P012-B를 소급 수정하거나 새 개발자료로 재채점하지 않는다.
- 유의하지 않은 결과를 null 채택 또는 구조 부재로 해석하지 않는다.
- 유의한 결과 하나를 수론 정리나 prime-gap 독립성 반증으로 표현하지 않는다.
- 두 stage 결과를 본 뒤 bin·cohort·seed·검정 family를 변경하거나 사후 pooling하지 않는다.

FGKMT 본체의 canonical `G(x)`는 end-prime 기준이고 `log_k`는 자연로그 k회 반복이다. P013은
별도 start-exposure recurrence 통계축이며 이를 변경하지 않는다.

## 3. 사전 고정 통계 계약

- contract: `test_plan/P013_recurrence_extension_contract_v1.json`
- contract SHA-256:
  `153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf`
- parent P012 contract SHA-256:
  `1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`
- bin schemes·cohorts·forced-first-record·zero-variance·LOW_INFORMATION 규칙: P012와 동일
- Monte Carlo: stage별 100,000회
- P013-A seed: `20260828`
- P013-B seed: `20260829`
- stage별 primary: two-sided family maximum absolute z
- 두 planned stages의 primary family-wise 기준: Bonferroni `alpha=0.025`씩
- secondary BH q: 설명적 지표이며 두 stage를 사후 합치지 않음

## 4. dataset·provenance·범위

- canonical record source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256:
  `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- source exhaustive limit: `10^20`, 두 endpoint보다 큼
- P012-B prerequisite manifest SHA-256:
  `299e0bbd3e754c0f5f716ddfaea4b09bb4e0cd6adcb6f98e94e6f0a71abc89e5`
- 외부 다운로드: 없음

| stage | gap-start range | exact gap-start count | complete records | 예상시간 | hard timeout |
|---|---|---:|---|---:|---:|
| A | `[10^10,10^11)` | `3,663,002,302` | `36–39` | 1.5–3시간 | 4시간 |
| B | `[10^11,10^12)` | `33,489,857,205` | `41–49` | 10–18시간 | 20시간 |

각 range의 오른쪽 첫 소수 하나를 추가해 마지막 gap start를 닫는다. record start와 다음 record
start가 모두 range 안인 plateau만 포함하고 양쪽 censored edge는 제외한다.

## 5. 사전검증과 중단 기준

사전검증:

1. 고정 Python·record·P012/P013 contract·P012-B manifest/report hash 일치
2. stage와 exact prime-count difference 일치
3. complete record indices 정확히 일치
4. source exhaustive limit이 endpoint 이상
5. holdout/extension prime stream을 읽지 않는 preflight
6. approval flag 없이는 입력 sweep·output 생성 전 거부

중단:

- hash·record selection·gap-start count·population·N/M/C 불일치
- stage seed·100,000회·bin·cohort 변경
- 기존 result/log overwrite 시도
- child timeout 또는 aggregate disk 50 GB 초과
- RAM 이상 징후; streaming segment 외 full prime/gap list 저장 시도

## 6. 사용자 실행 명령

개별 실행 환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P013A_recurrence_extension_1e11.bat --confirm-p013a
.\run_P013B_recurrence_extension_1e12.bat --confirm-p013b
```

두 파일을 직접 연속 실행하는 대신 P015 48시간 queue 사용을 권장한다. 같은 실험을 queue와
개별 runner로 중복 실행하지 않는다.

## 7. 성공 기준과 산출물

- terminal PASS
- saved deterministic full recomputation PASS, issue 0
- exact gap-start·boundary prime·selected record count 일치
- `analysis.json`, `summary.json`, `manifest.json`
- plateau·component·statistics CSV
- expected/residual PNG·PDF
- `saved_verification_report.json`
- run별 stdout/stderr log

## 8. 판정과 해석 제한

- `p<0.025`: planned two-stage primary departure candidate일 뿐 theorem이 아님
- `p>=0.025`: null 채택이 아니라 departure 미검출
- LOW_INFORMATION이 높으면 범위 확대의 효율이 낮다는 결과 자체를 보고
- A/B가 같은 방향이어도 독립 범위의 유한 재현으로만 표현
- 두 stage 완료 뒤 새 pooled/hierarchical 모형은 별도 P016 이상으로 분리

## 9. 후속 작업

사용자는 terminal marker, log, result directory와 figure 시각 QA를 회신한다. Codex는
manifest·full recomputation·독립 산술을 감사한 뒤에만 `EXPERIMENT_PASS`를 부여한다.

## 10. 구현·로컬검증

- analysis/CLI: `source/recurrence_sequential_extension.py`,
  `source/recurrence_sequential_extension_cli.py`
- reusable runner: `scripts/runners/run_p013_extension.ps1`
- stage entrypoints: `scripts/experiments/p013/`
- root BAT: `run_P013A_recurrence_extension_1e11.bat`,
  `run_P013B_recurrence_extension_1e12.bat`
- preflight A/B, approval gate, parser, full 140 unittest: PASS
- actual range sweep: 미실행
