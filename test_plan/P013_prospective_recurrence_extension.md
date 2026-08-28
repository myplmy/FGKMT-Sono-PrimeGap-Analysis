# P013 — Prospective stratified recurrence decade extension

## 1. 상태

`P013-A_R1_USER_RUN_FAILED / P013-A_R2_EXPERIMENT_PASS_USER_VISUAL_QA_PENDING / P013-B_SAVED_FULL_RECOMPUTATION_RUNNING / DO_NOT_DUPLICATE`

2026-08-28 감사 결과, P013-A r1은 두 input gate와 targeted tests, `[10^10,10^11)` 소수 체의
1,800번째 표시 progress와 그 뒤 exact gap-start count `3,663,002,302`·boundary-prime 내부
검사까지 완료했지만 Monte Carlo 단계에서
NumPy `Generator.hypergeometric`의 `ngood, nbad < 10^9` 구현 제한으로 중단됐다. 이는 prime
stream이나 연구 가설의 음성 결과가 아니며 통계 산출물도 생성되지 않았다. 교정 r2는 작은
parameter에서 기존 NumPy 난수열을 그대로 보존하고, 큰 parameter만 exact sequential
without-replacement symmetry sampler로 처리한다. binomial 근사는 사용하지 않는다.

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

r1 실측은 첫 full sweep이 약 44분이었다. r2는 analysis와 saved full recomputation의 두 sweep을
유지하므로 A는 약 1.5–2시간을 중심 추정으로 두되 기존 4시간 hard timeout을 유지한다. B는
gap-start count 선형 외삽으로 약 12–16시간을 예상하며 20시간 hard timeout을 유지한다.

### 2026-08-29 사후 실행 상태 메모

- P013-A r2는 전체 약 1시간 13분에 terminal·saved full recomputation PASS했다. 정본 보고서는
  `test_result/202608290456_P013A_r2_result_analysis.md`다.
- P013-B individual run은 2026-08-28 18:00:09 KST 시작했다. analysis 첫 sweep은
  `40,073.308`초(약 11시간 8분) 뒤 PASS했고, 2026-08-29 05:08부터 두 번째 saved full
  recomputation을 실행 중이다. terminal PASS 전에는 P013-B `EXPERIMENT_PASS`가 아니다.
- B 첫 sweep 실측상 전체 wall time은 기존 12–16시간 예상보다 길어 약 22–25시간이 될 수 있다.
  실행 중인 individual run에는 queue의 20시간 timeout이 적용되지 않는다.

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
7. Windows topology가 8 physical/16 logical이고 선택한 첫 4 physical core가 정확히 8 logical
   processor인지 확인; process affinity `0xff`, thread-pool ceiling 8
8. 큰 hypergeometric component는 exact sequential symmetry plan을 사용하고 각 plan의 최소
   sequential draw가 reviewed cap `2,000,000` 이하인지 확인
9. full sieve 뒤 `tmp/p013-checkpoints/p013<stage>_sufficient_statistics_v2.json`을 먼저 저장

중단:

- hash·record selection·gap-start count·population·N/M/C 불일치
- stage seed·100,000회·bin·cohort 변경
- 기존 result/log overwrite 시도
- child timeout 또는 aggregate disk 50 GB 초과
- RAM 이상 징후; streaming segment 외 full prime/gap list 저장 시도
- hypergeometric exact sequential draw cap 초과 또는 checkpoint 계약/hash 불일치

## 6. 사용자 실행 명령

아래는 재현용 원래 명령이다. P013-A r2는 이미 완료됐고 P013-B는 실행 중이므로 **현재 두
명령을 다시 실행하지 않는다.** P015 queue도 같은 child를 중복하므로 실행하지 않는다.

개별 실행 환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P013A_recurrence_extension_1e11_r2.bat --confirm-p013a
.\run_P013B_recurrence_extension_1e12.bat --confirm-p013b
```

전체 queue 실행 방법:

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
.\run_P015_48h_research_queue.bat --confirm-48h
```

queue는 P013-A r2 → P013-B → 독립 P014를 순서대로 실행한다. 개별 방식에서는 A r2가 terminal
PASS일 때만 B를 실행한다. queue 방식과 개별 방식을 동시에 또는 연속으로 중복 실행하지 않는다.

## 7. 성공 기준과 산출물

- terminal PASS
- saved deterministic full recomputation PASS, issue 0
- exact gap-start·boundary prime·selected record count 일치
- `analysis.json`, `summary.json`, `manifest.json`
- plateau·component·statistics CSV
- expected/residual PNG·PDF
- `saved_verification_report.json`
- `sufficient_statistics_checkpoint.json` 및 tmp의 resume용 원본 checkpoint
- run별 stdout/stderr log

## 8. 판정과 해석 제한

- `p<0.025`: planned two-stage primary departure candidate일 뿐 theorem이 아님
- `p>=0.025`: null 채택이 아니라 departure 미검출
- LOW_INFORMATION이 높으면 범위 확대의 효율이 낮다는 결과 자체를 보고
- A/B가 같은 방향이어도 독립 범위의 유한 재현으로만 표현
- 두 stage 완료 뒤 새 pooled/hierarchical 모형은 별도 P016 이상으로 분리

## 9. 후속 작업

사용자는 P013-A figure 두 장의 시각 QA와 P013-B 최종 terminal marker, log, result directory,
figure 시각 QA를 회신한다. Codex는
manifest·full recomputation·독립 산술을 감사한 뒤에만 `EXPERIMENT_PASS`를 부여한다.

## 10. 구현·로컬검증

- analysis/CLI: `source/recurrence_sequential_extension.py`,
  `source/recurrence_sequential_extension_cli.py`
- reusable runner: `scripts/runners/run_p013_extension.ps1`
- stage entrypoints: `scripts/experiments/p013/`
- root BAT: `run_P013A_recurrence_extension_1e11_r2.bat`,
  `run_P013B_recurrence_extension_1e12.bat`
- r1 실패 log: `test_result/logs/run_20260827T163052Z_p013a_recurrence_extension_1e11.log`
- r1 실행 BAT/PS1은 SHA-256 불변으로 `test_done/`에 failed-done 이관
- r2 exact large-parameter sampler·4 physical/8 logical affinity·checkpoint: 로컬검증 PASS
- P013-A r2 actual: terminal·saved recomputation·artifact hash `EXPERIMENT_PASS`, 사용자 figure QA 대기
- P013-B actual: analysis PASS 산출물 생성, saved full recomputation 실행 중; 최종 판정 대기
