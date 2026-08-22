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
- 02_핸드오프_규약.md: HANDOFF.md 필수 내용과 상태 표현
- 03_실험착수_절차.md: 승인 전 준비와 승인 후 실행 순서
- verify_skill_mirror.ps1: .claude/skills와 Codex용 .agents/skills의 파일 일치 확인

## Codex 스킬

.claude/skills의 기존 스킬 폴더와 보조 자료는 보존한다. 같은 내용을 .agents/skills에 미러링하여 Codex가 저장소 스킬로 발견하도록 한다. 두 트리의 변경은 함께 반영하고 hash 검사를 통과해야 한다.

## 실행 경계

코드 작성, 문서화, 합성 데이터 단위 테스트, 읽기 전용 원격 HEAD 확인은 승인 전에 가능하다. 원본 dataset 다운로드, 실제 validation 산출물 생성, maximal-gap 계산, 결과 그래프·통계 생성은 사용자의 명시적 허가 후에만 수행한다.
