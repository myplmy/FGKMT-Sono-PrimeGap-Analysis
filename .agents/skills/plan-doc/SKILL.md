---
name: plan-doc
description: 이 저장소의 연구 계획, 방법론, 단계별 실행 문서를 신설·패치하고 canonical 문서와 중복 정의를 정리한다. 플랜 문서나 문서 정합성 요청에 사용한다.
---

# Plan documents

## 정본

- 운영 규칙: AGENTS.md
- 연구 목적과 지시: 루트의 연구 작업지시서
- 계산 방법: docs/METHODS.md
- 실행 계획: test_plan/
- 현재 상태: `handoff/`의 최신 `YYYYMMDDHHmm_HANDOFF.md`

## 규칙

1. 문서 목적을 먼저 판별하고 정본에 이미 있는 수식·상수·경로는 링크나 명시적 참조로 연결한다.
2. 새 계획서는 Context, Goals, Non-goals, Inputs, Steps, Verification, Risks, Approval gate, Outputs, Follow-up 순으로 작성한다.
3. 상태 변경은 근거가 있을 때만 한다. 준비 완료를 실제 실험 완료로 표시하지 않는다.
4. 수학 정의나 데이터 범위 변경은 코드·테스트·METHODS·HANDOFF에 미치는 영향을 함께 점검한다.
5. 파일 이동이나 이름 변경 시 모든 내부 참조를 검색해 갱신한다.
