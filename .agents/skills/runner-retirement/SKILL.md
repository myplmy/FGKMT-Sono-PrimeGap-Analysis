---
name: runner-retirement
description: 사용자가 실제 실행한 FGKMT-Sono 전용 BAT, PS1, SH와 helper를 hash 보존해 test_done으로 이관하고 active 의존성을 점검한다. 일반 파일 정리나 미실행 runner에는 사용하지 않는다.
---

# Runner retirement

사용자가 해당 runner를 실제로 실행했다고 확인한 뒤에만 적용한다. `done`은 실행 이력이지
성공 판정이 아니며, 성공 여부는 log·manifest 감사로 정한다.

## 식별과 분류

1. 원본 log·run ID·실행 UTC·계획서에서 실제 entrypoint와 전용 helper를 식별한다.
2. log/manifest의 runner hash가 있으면 현재 파일 SHA-256과 대조한다.
3. 파일을 다음으로 분류한다.
   - `RETIRE`: 그 실행에만 쓰였고 재사용하지 않는 BAT/PS1/SH/helper
   - `KEEP_ACTIVE`: 다음 단계가 쓰는 공통 runner, source, READY, checkpoint, evidence
   - `USER_APPROVAL_REQUIRED`: 실행 여부나 downstream 의존성이 불명확

## 안전 이관

- source와 destination의 해석된 절대경로가 프로젝트 루트 안인지 확인한다.
- `test_done/<stem>-<runUTC>-done.<ext>`를 사용하고 기존 파일을 덮어쓰지 않는다.
- 이동 전후 SHA-256이 같아야 한다.
- `test_done` 파일을 수정·재실행하지 않는다.
- 실패 runner도 실행됐다면 보존하되 `USER_RUN_FAILED` 이력을 유지한다.
- 재시도는 active 위치의 새 revision과 새 승인 flag로 만든다.

## 의존성 감사

이관 전에 tests, active scripts, plan의 현재 실행 절차, README, 최신 handoff가 원본 active
경로를 계속 요구하는지 검색한다. historical handoff·실패보고서의 과거 경로는 당시 증거이므로
조용히 바꾸지 않는다. 공통 기능이 필요하면 먼저 `scripts/common` 또는 `scripts/runners`로
분리하되 실행된 원본 bytes는 그대로 보존한다.

## 완료 증거

- 원본·done 경로, run UTC, SHA-256
- active path 부재와 done path 존재
- 남긴 `KEEP_ACTIVE` 목록과 이유
- parser·syntax·relevant unit test 결과
- 결과 색인·계획의 실행 후 상태·신규 handoff 연결

삭제는 수행하지 않는다. 임시파일 정리는 별도 절차와 사용자 승인을 따른다.
