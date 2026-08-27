# P010A G4·P012·장시간 실험 감사 작업일지

## 식별 정보

- 시작 시각: 2026-08-27 11:50 KST
- 시작 commit: `042aaa7005597ef481f782346639370422c88d53`
- 시작 Git 상태: clean
- 사용자 승인: P012 Q1–Q3 권장안 승인, 사용자가 완료한 P010A G4 결과 분석 승인
- 실제 새 heavy 실행: Codex는 수행하지 않음. 과학적으로 타당한 3–12시간 후보가 있을 때 사용자용 runner만 준비한다.
- 자원 경계: CPU only, RAM 32 GB 미만, 단일 실행 3–12시간, 저장량 50 GB 이하

## 단계별 상태

| 단계 | 상태 | 완료 시각 | 증거·다음 행동 |
|---:|---|---|---|
| 0. 중단 복구·live 상태·작업일지 | 완료 | 2026-08-27 11:50 KST | skill 6개 확인, HEAD·clean status·최신 handoff·G4 terminal PASS 확인 |
| 1. P010A G4 산출물 독립 감사 | 완료 | 2026-08-27 11:52 KST | 35,224,647 exact constraints 재계산·manifest/hash/checkpoint 대조 issue 0; strict 상한 개선 확인 |
| 2. P012 Q1–Q3 정본 반영 | 완료 | 2026-08-27 12:04 KST | 승인 설계를 정본화하고 P012-A 코드·CLI·tests·승인형 runner 구현; actual·holdout 미실행 |
| 3. 3–12시간 연구 후보 준비도·가치 감사 | 완료 | 2026-08-27 12:09 KST | code-ready·과학적 타당성을 함께 만족하는 후보 0개; 별도 감사 문서 작성 |
| 4. 필요한 구현·runner·로컬 검증 | 완료 | 2026-08-27 12:12 KST | P012-A 짧은 승인형 runner 준비; full unittest 115/115, PowerShell parser 7/7, gate·saved verifier PASS |
| 5. 결과보고서·색인·done 이관 | 완료 | 2026-08-27 12:15 KST | G4 결과·통합 로컬검증 보고서와 색인 반영; 사용자 실행 G4 runner를 동일 SHA-256으로 `test_done` 이관 |
| 6. 새 handoff·최종 보고·Git 감사 | 완료 | 2026-08-27 12:18 KST | `handoff/202608271216_HANDOFF.md` 작성; `git diff --check` issue 0, 상태·hash·정본 표현 최종 감사 |

## 중단 시 재개 방법

1. 이 파일과 `handoff/`의 최신 `*_HANDOFF.md`를 함께 읽는다.
2. 위 표에서 처음으로 `완료`가 아닌 단계부터 재개한다.
3. P010A G4는 사용자가 이미 실행한 결과만 감사하며 같은 actual 명령을 다시 실행하지 않는다.
4. 새 3–12시간 actual 계산은 Codex가 실행하지 않고 승인 게이트가 있는 사용자 runner로만 준비한다.
5. 각 단계 완료 즉시 이 표와 아래 기록을 갱신한다.

## 작업 중 기록

- 2026-08-27 11:50 KST: user-reported G4 terminal marker는 PASS이고 result/log 경로가 존재한다. 로그상 4회 LP solve, 20.919초 core elapsed, exact final verification PASS, strict bound improvement true로 보이나 아직 독립 artifact 감사 전이므로 최종 판정은 보류한다.
- 2026-08-27 11:50 KST: 사용자가 P012 Q1–Q3 권장안을 모두 승인했다. 이 선택을 결과를 보기 전에 정본 계획에 고정하고 구현·actual 실행 상태를 별도로 표시한다.
- 2026-08-27 11:52 KST: G4 manifest artifact hash issue 0, checkpoint 4개와 history 일치, input exact-lift binding 일치, best certificate의 35,224,647 constraints exact 재계산 PASS·minimum slack 0을 확인했다. total upper bound는 `439161464927854179`에서 `436001550591586306`으로 `3159914336267873`(0.7195336%) 감소했다. 정규화 `C`는 약 `1.094868396172136e15`이나, 위치 목록·candidate cover·search acceleration은 계속 미증명이다. core elapsed 20.919초, working constraints 20,123, artifact 약 3.0 MB로 11시간·50 GB cap에 훨씬 못 미쳐 정상 조기수렴이다.
- 2026-08-27 12:04 KST: P012 Q1–Q3를 계획서에 사전 고정했다. `[2,10^9]` prime stream의 log-bin 충분통계, forced first-record 제거, hypergeometric MC 100,000회, P011 비교, saved full recomputation을 구현했다. LOW_INFORMATION은 `K<5` 또는 control exposure `<1000`인 설명용 플래그로 고정하며 family membership을 바꾸지 않는다. py_compile·PowerShell parser·preflight·approval denial PASS, toy 4/4 PASS. 최초 sandbox toy cleanup은 기존 Windows TEMP ACL로 실패했으나 동일 FGKMT 시험을 정상 Windows 권한에서 재실행해 PASS했다. P012-A actual과 `[10^9,10^10]` holdout은 실행하지 않았다.
- 2026-08-27 12:09 KST: `docs/method/20260827_3to12h_compute_readiness_audit.md`에 전체 후보를 분류했다. 현재 code-ready이면서 연구 질문에 직접 답하는 3–12시간 후보는 0개다. P005/P010B는 coverage theorem이 없고, P009 10-block은 internal-zero 공급이 없으며, P010A 30030은 이미 21초에 수렴했다. modulus 510510은 92,160 states·8,524,288,932 constraints이고 full-matrix 추정이 최소 825.65 GiB여서 새 memory-safe 설계 전 runner 작성이 안전하지 않다. CPU 시간을 채우는 반복 실험은 만들지 않았다.
- 2026-08-27 12:12 KST: P012-A 관련 toy 4/4, 전체 unittest 115/115, active PowerShell parser 7/7, 입력 preflight, 승인 누락 거부, saved full recomputation 경로를 검증했다. 실제 P012-A는 실행하지 않았다.
- 2026-08-27 12:15 KST: G4 결과보고서와 통합 로컬검증 보고서를 결과 색인에 연결했다. 사용자 실행 G4 runner는 원 SHA-256 `6dce831b8e29d72d4a0ef2ba62ff0120c679a6bb93c1789a37f8ec98affaa8c2`를 보존한 채 `test_done/run_p010a_mod30030_cutting_plane_11h-20260826T155918Z-done.ps1`로 이관했다. P012-A active runner SHA-256은 `61ff041f32813d377d9414e700638dac359961cd29699778ae0969b40404a9f3`이다.
- 2026-08-27 12:18 KST: `handoff/202608271216_HANDOFF.md`에 쉬운 사용자 실행 절차, 장시간 runner 0개 판정, 우선순위와 커밋 제안을 기록했다. 최종 `git diff --check`는 line-ending 안내 외 whitespace issue 0이고, 완료 G4 runner hash·active P012-A runner hash·old active runner 부재를 재확인했다. commit·push는 수행하지 않았다.
