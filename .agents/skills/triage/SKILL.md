---
name: triage
description: 사용자가 요청한 issue나 연구 작업 항목을 정보 부족, 준비 완료, 사용자 결정 필요, 보류 상태로 분류하고 다음 행동을 제안한다.
---

# Triage

## 상태

- needs-info: 필수 입력이나 재현 증거가 부족함
- waiting-for-user-approval: 실제 데이터 취득 또는 실험 허가 대기
- ready-for-codex: 승인 범위 안에서 구현·문서·합성 테스트 가능
- ready-for-user: 사용자가 실행하거나 도메인 결정을 내려야 함
- blocked: 반복 확인 후에도 외부 조건 때문에 진행 불가
- wontfix: 근거와 사용자 결정으로 수행하지 않음

항목마다 category, state, 근거, 다음 담당자, 검증 기준을 제시한다. 외부 issue의 label, comment, 상태를 바꾸기 전에는 사용자의 명시적 요청을 확인한다. AI가 작성한 외부 comment에는 그 사실을 명시한다.

