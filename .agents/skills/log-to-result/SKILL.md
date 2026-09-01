---
name: log-to-result
description: 사용자 승인 하에 생성된 FGKMT-Sono empirical-envelope, recurrence, finite-certificate, information-probe 실행을 감사해 결과 문서·색인·계획 상태·핸드오프를 갱신한다.
---

# Log to result

실제 실행이 승인되었고 사용자가 실행했거나 승인된 산출물이 존재할 때만 적용한다. 이 skill은
actual 실행 권한을 새로 만들지 않는다.

먼저 `test_plan/`의 해당 사전계획, 최신 `handoff/*_HANDOFF.md`,
`test_result/00_실험결과_분석보고서_색인.md`를 읽는다. 실험군별 검사항목은
[profiles](references/profiles.md)에서 해당 profile 하나만 읽는다.

## 공통 감사

1. 원본 log의 byte size·SHA-256, 마지막 PASS, 첫 FAIL, terminal marker, exit code를 확인한다.
2. plan의 입력·범위·gate·자원·중단조건이 결과를 본 뒤 소급 변경되지 않았는지 확인한다.
3. result directory, manifest, 필수 artifact, source/input/code hash, 고정 FGKMT Python을 대조한다.
4. saved verifier가 무엇을 독립 재계산했는지와 공통 kernel 위험을 구분한다.
5. runtime은 expected full path, 실제 early exit, hard wall을 분리하고 조기종료를 full search로 쓰지 않는다.
6. `EXPERIMENT_PASS`와 `SCIENTIFIC_NO_IMPROVEMENT`, `LOW_INFORMATION`,
   `CALIBRATION_ONLY` 같은 과학적 결과를 동시에 기록한다.
7. partial·negative result도 숨기지 않으며 기존 결과를 덮어쓴 흔적이 없는지 확인한다.
8. figure는 수치·파일 자동검증과 사용자 visual QA를 분리한다.

## 결과 반영

1. `test_result/<timestamp>_<experiment>_result_analysis.md`에 쉬운 결론, 증거, 수치,
   과학적 의미, 말할 수 없는 것, 후속 gate를 쓴다.
2. `test_result/00_실험결과_분석보고서_색인.md`에 run/log/report와 최신 판정을 연결한다.
3. 계획서는 gate를 고치지 않고 별도 “실행 후 상태 기록”만 append한다.
4. METHODS·theory index·AGENTS의 현재 상태는 확인된 사실만 갱신한다.
5. 사용자가 실행한 전용 BAT/PS1/SH가 있으면 `runner-retirement` workflow로 hash를 보존한다.
6. 요청되었거나 세션 종료에 필요한 경우 새 timestamp handoff를 만든다.

유한 범위 관찰을 무한 범위 정리의 검증·반증·재증명으로 표현하지 않는다. count upper bound,
candidate location coverage, search acceleration도 서로 다른 결과로 유지한다.
