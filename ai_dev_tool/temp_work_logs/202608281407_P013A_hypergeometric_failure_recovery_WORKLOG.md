# P013-A 대규모 hypergeometric 실패 복구 작업 로그

- 작업 시작: 2026-08-28 14:07 KST
- 대상 실패 run: `20260827T163052Z_p013a_recurrence_extension_1e11`
- 원본 로그 SHA-256: `5CCD6E2997123A99120512AF9D36A4B5AC50CFB4A3E24D6833E5B48EAEEBE79C`
- 승인 경계: 실패 감사·코드/runner 수정·로컬 toy/회귀검증만 수행. P013/P014 actual 재실행은 하지 않음.

## 단계별 상태

1. **실패 원본 존재 및 저장소 상태 확인 — 완료**
   - Git work tree 확인: `true`, HEAD `a02a4db`.
   - 원본 로그 존재 확인.
   - 로그가 가리키는 partial result directory는 생성되지 않았음을 확인.
   - 실행된 P013-A BAT와 실험 전용 PS1은 아직 active 경로에 존재.
2. **로그·산출물·해시 상세 감사 — 완료**
   - run 44분, two preflight gate·targeted tests PASS, exact gap/boundary 내부검사 뒤 inference에서 첫 FAIL.
   - result directory·terminal PASS·manifest·summary·saved report 없음.
   - old BAT/PS1 원본 SHA-256을 보존해 `test_done/`으로 이관.
3. **대규모 hypergeometric sampler 교정 설계·영향 분석 — 완료**
   - NumPy safe path bit-for-bit 보존.
   - large path는 네 분포 대칭 중 최소 draw를 고르는 exact sequential without-replacement sampler.
   - binomial approximation 금지, component당 2,000,000 draw fail-closed cap.
   - exact PMF·support·moment·10억 초과·네 symmetry unit test PASS.
4. **P013-A r2·P015 queue·CPU 자원 정책 구현 — 완료**
   - P013-A r2 entrypoint와 checkpoint, P015 child 경로 교정.
   - Windows topology 실측 8 physical/16 logical; 첫 4 physical/8 logical mask `0xff` 적용 smoke PASS.
   - P013/P014 thread-pool ceiling 8; single-stream 구간은 병렬이라고 주장하지 않음.
5. **FGKMT 환경 정적/toy/전체 검증 — 완료**
   - affected py_compile PASS.
   - active PowerShell parser 11 files issue 0, BAT approval-denial 4/4 PASS.
   - P013 A/B와 P014 resource preflight PASS, actual=false.
   - sandbox 밖 affected unittest 23/23, 전체 unittest 148/148 PASS.
   - final `git diff --check` PASS.
6. **실패 보고서·색인·handoff·사용자 실행 안내 — 완료**
   - 실패 분석, 교정 영향도, 로컬검증, 결과 색인과 P013/P014/P015 계획 갱신.
   - 신규 handoff: `handoff/202608281450_HANDOFF.md`.
   - queue 방식과 개별 방식의 정확한 Windows 명령·예상시간·회신 항목을 모두 기록.

## 최종 상태

`P013-A_R1_USER_RUN_FAILED / P013-A_R2_LOCALLY_VERIFIED / P013-B_P014_P015_ACTUAL_NOT_RUN`

실제 heavy 재실행은 하지 않았다. 다음 사용자 행동은 교정된 P015 queue 전체 또는 P013-A r2
개별 실행 중 하나를 선택하는 것이다.

## 현재 확인된 핵심 사실

- 마지막 표시 progress는 chunk 1,800·`99,999,999,977`이고, 코드 위치상 그 뒤 exact gap count와 오른쪽 boundary prime 검사를 통과한 다음 통계 분석에서 실패했다.
- 예외는 NumPy `Generator.hypergeometric`의 개별 `ngood`/`nbad < 1,000,000,000` 구현 제한이다.
- 이 시점에는 정본 결과 디렉터리가 생성되지 않았으므로 실패 run을 실험 PASS 또는 통계 결과로 해석하지 않는다.
