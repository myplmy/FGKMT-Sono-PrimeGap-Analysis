# 형식검증 산출물 규약

이 폴더는 theory 원문과 Lean 선언 사이의 기계 판독 가능한 inventory 및 검증 보조자료를
보존한다. 사람이 읽는 상태 정본은 상위 `VERIFICATION_LEDGER.md`, Lean 커널 입력 정본은
`../FGKMTSono/TheoryVerification.lean`이다.

상태 의미:

- `KERNEL_PASS`: project-local `axiom`, `sorry`, `admit` 없이 명제가 커널 검증됨.
- `CONDITIONAL_KERNEL_PASS`: 선행 premise를 명시적 theorem 인수로 받아 결론의 논리적 합성만 검증됨.
- `DEFINITION_ONLY`: 정의·표기이며 참/거짓 증명 대상이 아님.
- `PARTIAL_FORMALIZATION`: display 식의 핵심 일부만 형식화되었으며 식 전체 PASS가 아님.
- `SOURCE_THEOREM_UNFORMALIZED`: 채택한 선행 analytic theorem 자체는 아직 Lean 증명이 없음.
- `NOT_YET_FORMALIZED`: 원장에는 등록됐지만 아직 Lean 선언이 없음.
- `PARSE_REVIEW_REQUIRED`: Markdown 수식 경계나 식 식별자를 사람이 확인해야 함.

`CONDITIONAL_KERNEL_PASS`는 premise의 진실을 인증하지 않으며 `KERNEL_PASS`로 승격하지 않는다.

2026-09-14 Theory 74 갱신 뒤 전수 inventory는 75개 theory 문서·1,362개 display
수식·267개 Lean declaration이다. 상태는 `KERNEL_PASS=90`,
`CONDITIONAL_KERNEL_PASS=51`, `DEFINITION_ONLY=64`,
`PARTIAL_FORMALIZATION=70`, `SOURCE_THEOREM_UNFORMALIZED=67`,
`NOT_YET_FORMALIZED=1015`, `PARSE_REVIEW_REQUIRED=5`이며 금지 proof escape는 0건이다.
modern density source theorem은 local axiom으로 넣지 않았고, (d=186) exponent와
Friedlander--Iwaniec의 유한 산술만 kernel proof로 추가했다.
