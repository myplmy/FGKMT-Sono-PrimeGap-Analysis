# P013 병렬 동일성 calibration runner 작업로그

- 시작: 2026-08-29 14:35 KST
- 사용자 승인: P013-A 완료 및 P013-B 진행 이후 사용할 runner 구현, 필요한 추가 P013
  동일성 검증 구현
- 허용 actual 범위: P013-A 전체범위와 P013-B 중간범위만 사용하며 한 번의 queue 실행 합계는
  16시간 이내
- 금지·주의: 현재 실행 중인 P013-B process·파일을 중단하거나 변경하지 않음. P013-B 전체범위
  병렬 재실행 금지. 정밀도·prime/gap·Monte Carlo replication·saved recomputation 생략 금지.

## 단계 현황

1. **완료 — 현재 상태·승인 경계 확인**
   - 작업 시작 시 Git tracked/untracked 상태는 clean.
   - 사용자 진술에 따라 P013-A는 완료, P013-B는 진행 중으로 취급한다.
   - `Win32_Process` command-line 조회는 권한 거부됐으며, 실행 중 process에는 추가 접근하거나
     개입하지 않는다.
2. **완료 — 영향도·실험계획 확정**
   - 영향도: `docs/method/20260829_P017_P013_parallel_calibration_impact_analysis.md`
   - 계획: `test_plan/P017_P013_parallel_actual_calibration.md`
   - 동결 계약: `test_plan/P017_p013_parallel_calibration_contract_v1.json`
   - A full 한 번 + B first half-decade serial/parallel, child cap 합 15시간·global 16시간.
3. **완료 — 병렬 actual-calibration 코드·개별 runner·bounded queue 구현**
   - P017-A: P013-A full parallel vs 완료 serial checkpoint·analysis.
   - P017-B: `[10^11,316227766017)` 새 serial vs parallel exact.
   - 개별 BAT 2개와 child cap 합 15시간·global 16시간 queue BAT 1개.
4. **완료 — toy·정적·전체 회귀검증**
   - targeted 16/16 (`10.166s`), 전체 unittest 170/170 (`26.900s`), py_compile PASS.
   - A/B preflight, PowerShell parser 4/4, BAT approval-denial 3/3 PASS.
   - sandbox IPC `WinError 5`는 동일 명령 sandbox 밖 재실행 PASS로 환경 원인 확인.
   - PowerShell array 결합 함정을 actual 전에 발견·명명 배열로 교정하고 회귀시험 추가.
   - combined queue 고정 `live_console.log` Python flush와 대기형 tail 명령 추가.
5. **완료 — 문서·색인·AGENTS·신규 handoff 정합화**
   - 로컬검증 보고서: `test_result/202608291453_P017_P013_parallel_calibration_local_validation.md`.
   - 최신 handoff: `handoff/202608291459_HANDOFF.md`.

## 재개 규칙

- 이 파일의 첫 `진행 중` 또는 `대기` 단계를 이어서 수행한다.
- P013-B가 진행 중인 동안 heavy actual 명령은 Codex가 실행하지 않는다.
- 새 runner는 기존 serial P013-A/B 실행기와 다른 run label·output directory를 사용한다.
- serial/parallel exact 동일성, 독립 saved recomputation, 16시간 queue hard limit이 정적으로
  검증되기 전에는 사용자 실행 명령으로 제시하지 않는다.
