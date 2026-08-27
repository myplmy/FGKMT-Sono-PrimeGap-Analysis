# P012-A r2 결과 감사 작업일지

## 식별 정보

- 시작 시각: 2026-08-27 16:50 KST
- 시작 commit: `b1d79614755d8ddc60be5b6c04048bf6236e88a4`
- 시작 Git 상태: clean
- 사용자 실행: `run_20260827T054007Z_p012a_stratified_null_development_r2`
- 사용자 보고: terminal·saved recomputation PASS
- 실제 새 실험: Codex는 수행하지 않고 사용자 실행 결과를 읽기·독립 재검증·해석한다.

## 단계별 상태

| 단계 | 상태 | 완료 시각 | 증거·다음 행동 |
|---:|---|---|---|
| 0. live 상태·실행 증거 고정 | 완료 | 2026-08-27 16:50 KST | HEAD·clean status, log·runner hash, terminal PASS, 필수 파일 존재 확인 |
| 1. manifest·hash·saved provenance 감사 | 완료 | 2026-08-27 16:52 KST | manifest 11 artifacts, 입력·code·runner hashes, 84 rows·128 components·9 cohorts 독립 재계산 issue 0 |
| 2. primary·secondary·sensitivity 재계산·해석 | 완료 | 2026-08-27 16:53 KST | primary obs 9 vs P012 exp 8.587, family p 0.219; 모든 scheme enrichment BH q=1; 저정보 한계 고정 |
| 3. figure 자동 감사·사용자 시각 QA 항목 | 완료 | 2026-08-27 16:54 KST | PNG 2개 decode·nonblank, PDF 2개 header/EOF, manifest hash PASS; visual QA는 사용자 대기 |
| 4. r2 runner done 이관 | 완료 | 2026-08-27 16:55 KST | 원 SHA-256 보존, timestamp done 사본 생성, active 진입점 제거 |
| 5. 결과보고서·계획·색인·정본 갱신 | 완료 | 2026-08-27 16:59 KST | EXPERIMENT_PASS와 VISUAL_QA_PENDING을 분리해 정본 문서 갱신 |
| 6. 새 handoff·권장 순서·최종 Git 감사 | 완료 | 2026-08-27 17:03 KST | 새 timestamp handoff, 실행 절차, commit 제안, hash·상태·whitespace 최종 감사 완료 |

## 고정된 실행 증거

- log: `test_result/logs/run_20260827T054007Z_p012a_stratified_null_development_r2.log`
- log SHA-256: `dea10dac2982fb851c532d7b621489d85166bc3e13e9a6274167fe64c0dd76ad`
- run: `test_result/run_20260827T054007Z_p012a_stratified_null_development_r2`
- runner SHA-256: `0af40c63e02b962c2c1716d868c15a8dabc4a52302e2b87e9e9be36201ab8e28`
- terminal PASS: 있음
- saved report status: PASS, issues 0, deterministic full recomputation PASS
- manifest SHA-256: `723bd82778c92b7ebe3e9f614fd7411e86f5619d3043ed292ddac93fa6966c09`
- holdout touched: false

## 중단 시 재개 방법

1. 이 파일과 `handoff/`의 최신 `*_HANDOFF.md`를 읽는다.
2. 위 표에서 처음 `완료`가 아닌 단계부터 재개한다.
3. 사전 고정 primary와 sensitivity·secondary를 구분하고 p값만으로 수론 정리를 주장하지 않는다.
4. figure는 자동 파일 검증과 사용자 시각 QA를 분리한다.
5. 실행된 r2 runner는 hash를 확인한 뒤 `test_done/*-done.ps1`로 이관하고 재실행하지 않는다.

## 작업 중 기록

- 2026-08-27 16:50 KST: 로그는 preflight, targeted 14 tests, development analysis, saved full recomputation 순서로 모두 PASS했다. actual analysis 87.234초, modeled rows 84, component rows 128, figure 4개, GPU 미사용이다. 입력 두 hash가 계획과 일치하고 holdout·theorem flag는 false다. 아직 사후 독립 artifact·통계 감사 전이므로 최종 연구 판정은 보류한다.
- 2026-08-27 16:52 KST: manifest 11개 artifact hash와 saved manifest hash를 재계산했고 mismatch 0이다. source·CLI·runner hash는 로그와 현재 파일이 일치한다. 저장 component로 기대값·분산·z·row Monte Carlo p·BH q·9개 family max-z p를 독립 재계산해 issue 0이었다. r1과 r2의 analysis/components/statistics SHA-256도 모두 같아 교정이 통계 결과를 바꾸지 않았음을 확인했다.
- 2026-08-27 16:53 KST: 사전 primary `start>=1000`에서 observed 9, P011 expected 109.0790, P012 expected 8.58738, max abs z 2.62116, family p 0.21945다. shifted primary들도 expected 8.76695·8.32370, family p 0.71354·0.49280로 같은 결론이다. 가장 큰 enrichment는 gap 154의 observed 2 vs expected 0.66778, one-sided p 0.11157이고 모든 scheme의 최소 BH q는 1.0이다. 다만 primary scheme 28/28 rows에 적어도 한 LOW_INFORMATION component가 있어 non-rejection은 모형 정당화가 아니라 P011 과대예측의 nonstationarity 진단으로 제한한다.
- 2026-08-27 16:54 KST: expected PNG 1800x990, residual PNG 1980x990은 decode·nonblank 검사 PASS다. PDF 2개도 `%PDF` header와 EOF marker가 있고 네 figure hash 모두 manifest와 일치한다. 사람 눈의 축·범례·x marker 판정은 아직 수행되지 않아 `VISUAL_QA_PENDING`이다.
- 2026-08-27 16:55 KST: 사용자 실행 r2 runner를 `test_done/run_p012_stratified_null_development_r2-20260827T054007Z-done.ps1`로 이관했다. 실행 당시 SHA-256 `0af40c63e02b962c2c1716d868c15a8dabc4a52302e2b87e9e9be36201ab8e28`을 그대로 보존했고 active 진입점은 제거했다.
- 2026-08-27 16:59 KST: P012-A r2 결과보고서와 계획서, METHODS, 이론·종합평가 문서, 장시간 계산 준비도 감사, 결과 색인, AGENTS 현재 상태를 갱신했다. P012-B holdout은 사용자 figure QA와 통계 계약 동결 전까지 계속 잠갔다.
- 2026-08-27 17:03 KST: `handoff/202608271701_HANDOFF.md`를 새 파일로 작성했다. done runner와 manifest hash를 다시 대조했고 active r2 runner 부재, 최신 정본의 stale 상태문구 0건, 새 파일 trailing whitespace 0건, `git diff --check` exit 0을 확인했다. LF/CRLF 안내만 있었고 whitespace 오류는 없었다. commit·push는 수행하지 않았다.
