---
name: session-handoff
description: 다음 Codex 작업이 즉시 이어받을 수 있도록 handoff 폴더에 timestamp 핸드오프를 새 파일로 작성한다. 핸드오프 요청이나 작업 마무리에 사용한다.
---

# Session handoff

`handoff/YYYYMMDDHHmm_HANDOFF.md`를 Asia/Seoul 기준 현재 연월일시분으로 매번 새로 만든다. 기존 핸드오프를 수정하거나 덮어쓰지 않는다. 같은 분의 파일이 이미 있으면 새 실제 분 시각을 사용해 충돌을 피한다. 최신 timestamp 파일이 진행 상태의 정본 스냅샷이며, AGENTS.md와 METHODS.md의 영구 규칙은 복제하기보다 링크하고 이번 상태와 다음 행동을 기록한다.

## 필수 섹션

1. 한 줄 상태와 승인 상태
2. ChatGPT가 이해한 연구 목적·정의·비목적
3. 완료한 파일과 구현
4. 실제로 하지 않은 일
5. 검증 명령과 결과
6. dataset 원천, 확인된 commit, coverage, 다운로드 여부
7. 위험, 미결정, 해석 주의
8. 다음 사용자에게 요청할 사항
9. 권장 작업 우선순위와 각 근거
10. 승인 후 첫 실행 명령
11. 한국어 commit 제목과 본문 제안
12. 다음 Codex가 사용할 짧은 이어받기 지시

git 상태와 산출물 존재 여부는 현재 세션에서 다시 확인한다. 과거 기록을 현재 사실처럼 복사하지 않는다.
