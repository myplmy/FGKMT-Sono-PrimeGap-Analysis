---
name: pr-workflow
description: 사용자가 명시적으로 요청한 경우 이 저장소의 브랜치, 커밋, push, pull request, merge 작업을 안전하게 준비하거나 수행한다.
---

# PR workflow

외부 상태를 바꾸는 push, PR 생성, 수정, merge는 사용자의 명시적 요청 없이는 수행하지 않는다.

## 절차

1. git status, 현재 branch, remote, base 후보를 다시 확인한다.
2. 사용자 변경과 이번 작업 변경을 분리한다.
3. git add . 또는 git add -A를 쓰지 않고 검토한 명시 경로만 stage한다.
4. raw dataset, validated dataset, 결과 산출물, 비밀정보, ../../project.json의 excludedPaths를 포함하지 않는다.
5. 관련 테스트와 문서 정합성 검사를 수행한다.
6. 한국어 commit 제목과 본문, PR Summary와 Test plan을 제안한다.
7. 사용자가 커밋만 요청했으면 push나 PR로 범위를 넓히지 않는다.
8. 충돌, 실패, 보호 규칙을 우회하지 않는다.

검증 결과에는 실제 실행과 미실행을 분리해 적고, 본 실험이 승인되지 않았다면 그 사실을 명시한다.

