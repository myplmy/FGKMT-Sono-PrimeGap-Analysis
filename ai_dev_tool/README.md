# FGKMT-Sono 연구용 AI 개발 보조 규약

이 폴더는 이번 maximal prime-gap 연구에서 Codex가 반복적으로 확인해야 할 계산 함정, 핸드오프 형식, 실험 착수 절차를 모은다. 이전 모델 학습 실험의 GPU·배치 규칙은 제거했다.

## 정본 우선순위

1. 사용자 최신 지시
2. AGENTS.md
3. 루트 연구 작업지시서
4. docs/METHODS.md
5. test_plan의 개별 실행 계획
6. 이 폴더의 보조 체크리스트

충돌하면 상위 정본을 따르고 하위 문서를 정정한다.

## 파일

- 01_계측함정_원장.md: 수학·데이터·수치·해석 오류 방지
- 02_핸드오프_규약.md: `handoff/YYYYMMDDHHmm_HANDOFF.md` 필수 내용과 상태 표현
- 03_실험착수_절차.md: 승인 전 준비와 승인 후 실행 순서
- 04_사용자실행_로그_완료이관_규약.md: 사용자 명령 형식, 전체 오류 로그, 실패 감사, `test_done` 보존, 시각검사
- 05_ChatGPT_오류_실수_환각_원장.md: 구현·판정·표기·추정 오류와 재발방지, 미해결 debt
- 06_스킬_AGENTS_작업규약_개선제안_20260901.md: 사용자 작업성향을 반영한 skill·AGENTS·보조규약 개선안
- 07_임시파일_격리_정리_절차.md: tmp 의존성 감사, 복구 가능한 quarantine, 사용자 승인 뒤 정확한 경로 삭제 절차
- 08_작업원장_작성규약_양식.md: 장기 작업의 단계별 기록, 중단 후 재개, `-done` 완료 표시 규약과 양식
- work_ledgers/: 진행 중 작업원장과 완료된 `WORK_LEDGER-done.md` 보존 경로

재사용 가능한 실행 기능은 `scripts/common`, `scripts/runners`, `scripts/tests`,
`scripts/setup`에 둔다. 특정 완료 실험의 BAT/PS1/SH와 전용 helper는 `test_done`에
hash를 남기고 다시 실행하지 않는다.

## Codex 스킬

현재 프로젝트는 `.agents/skills`만 Codex 스킬 정본으로 사용한다. `.claude` 호환 미러는 복원하거나 사용하지 않는다. 결과 감사는 profile 기반 `log-to-result`, 완료 실행기 이관은 `runner-retirement`, 전체 연구현황 정리는 `research-status-synthesis`를 사용한다.

## 실행 경계

코드 작성, 문서화, 합성 데이터 단위 테스트, 읽기 전용 원격 HEAD 확인은 승인 전에 가능하다. 원본 dataset 다운로드, 실제 validation 산출물 생성, maximal-gap 계산, 결과 그래프·통계 생성은 사용자의 명시적 허가 후에만 수행한다.
