---
name: setup-matt-pocock-skills
description: 사용자가 명시적으로 요청할 때 issue·PR 보조 스킬이 사용할 저장소별 tracker, label, domain 문서 설정을 AGENTS.md와 docs/agents에 구성한다.
---

# Setup issue workflow skills

현재 저장소에서는 로컬 연구 문서와 승인 게이트가 우선이다. 이 스킬은 사용자가 issue workflow 구성을 요청한 경우에만 사용한다.

1. AGENTS.md, ../../project.json, remote, 기존 docs/agents를 조사한다.
2. tracker 종류, label vocabulary, domain 문서 위치를 제안한다.
3. 외부 tracker를 사용할지 사용자 확인을 받는다.
4. 합의된 설정만 AGENTS.md와 docs/agents에 기록한다.
5. GitHub issue, label, PR 등 외부 객체를 자동 생성하지 않는다.
6. 연구 데이터 취득·실행 승인과 issue workflow 승인을 별개의 권한으로 다룬다.

