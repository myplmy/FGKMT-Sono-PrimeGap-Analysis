# 형식검증 산출물 규약

이 폴더는 theory 원문과 Lean 선언 사이의 기계 판독 가능한 inventory 및 검증 보조자료를
보존한다. 사람이 읽는 상태 정본은 상위 `VERIFICATION_LEDGER.md`, Lean 커널 입력 정본은
`../FGKMTSono/TheoryVerification.lean`이다.

상태 의미:

- `KERNEL_PASS`: project-local `axiom`, `sorry`, `admit` 없이 명제가 커널 검증됨.
- `CONDITIONAL_KERNEL_PASS`: 선행 premise를 명시적 theorem 인수로 받아 결론의 논리적 합성만 검증됨.
- `DEFINITION_ONLY`: 정의·표기이며 참/거짓 증명 대상이 아님.
- `SOURCE_THEOREM_UNFORMALIZED`: 채택한 선행 analytic theorem 자체는 아직 Lean 증명이 없음.
- `NOT_YET_FORMALIZED`: 원장에는 등록됐지만 아직 Lean 선언이 없음.
- `PARSE_REVIEW_REQUIRED`: Markdown 수식 경계나 식 식별자를 사람이 확인해야 함.

`CONDITIONAL_KERNEL_PASS`는 premise의 진실을 인증하지 않으며 `KERNEL_PASS`로 승격하지 않는다.
