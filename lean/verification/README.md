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

2026-09-14 Theory 75 갱신 뒤 전수 inventory는 76개 theory 문서·1,381개 display
수식·270개 Lean declaration이다. 상태는 `KERNEL_PASS=91`,
`CONDITIONAL_KERNEL_PASS=53`, `DEFINITION_ONLY=67`,
`PARTIAL_FORMALIZATION=73`, `SOURCE_THEOREM_UNFORMALIZED=68`,
`NOT_YET_FORMALIZED=1024`, `PARSE_REVIEW_REQUIRED=5`이며 금지 proof escape는 0건이다.
Lean은 first-slice endpoint rational, pointwise min monotonicity와 explicit
second-moment premise 이후 Cauchy terminal 대수만 검사한다. density·smooth explicit
formula·complex moment theorem은 local axiom으로 넣지 않았다. PAP-11, DEP-R09,
fixed `2e-17`, `X_cert`는 OPEN이다.

2026-09-14 Theory 76 갱신 뒤 전수 inventory는 77개 theory 문서·1,406개 display
수식·272개 Lean declaration이다. 상태는 `KERNEL_PASS=91`,
`CONDITIONAL_KERNEL_PASS=56`, `DEFINITION_ONLY=73`,
`PARTIAL_FORMALIZATION=80`, `SOURCE_THEOREM_UNFORMALIZED=75`,
`NOT_YET_FORMALIZED=1026`, `PARSE_REVIEW_REQUIRED=5`이며 금지 proof escape는 0건이다.
Lean은 Bennett cutoff no-overlap과 aggregate second-moment의 Cauchy terminal만 검사한다.
pointwise PNT·character orthogonality·explicit formula·individual-primorial moment theorem은
local axiom으로 넣지 않았다. PAP-11, DEP-R09, fixed `2e-17`, `X_cert`는 OPEN이다.

2026-09-14 Theory 77 갱신 뒤 전수 inventory는 78개 theory 문서·1,426개 display
수식·276개 Lean declaration이다. 상태는 `KERNEL_PASS=91`,
`CONDITIONAL_KERNEL_PASS=58`, `DEFINITION_ONLY=80`,
`PARTIAL_FORMALIZATION=85`, `SOURCE_THEOREM_UNFORMALIZED=80`,
`NOT_YET_FORMALIZED=1027`, `PARSE_REVIEW_REQUIRED=5`이며 금지 proof escape는 0건이다.
Lean은 nonprincipal energy의 실수대수, principal-separated moment terminal, Cauchy scalar
equality와 power-regime endpoint만 검사한다. finite character orthogonality와 analytic
variance/correlation theorem은 local axiom으로 넣지 않았다. PAP-11, DEP-R09, fixed
`2e-17`, `X_cert`는 OPEN이다.

2026-09-14 Theory 78 갱신 뒤 전수 inventory는 79개 theory 문서·1,439개 display
수식·278개 Lean declaration이다. 상태는 `KERNEL_PASS=94`,
`CONDITIONAL_KERNEL_PASS=58`, `DEFINITION_ONLY=87`,
`PARTIAL_FORMALIZATION=86`, `SOURCE_THEOREM_UNFORMALIZED=82`,
`NOT_YET_FORMALIZED=1027`, `PARSE_REVIEW_REQUIRED=5`이며 금지 proof escape는 0건이다.
Lean은 finite bad-set union selection과 singleton bad-count 결론만 독립 검증한다.
Maier CRT source, FMT random construction 및 weighted-correlation analytic theorem은
local axiom으로 넣지 않았다. PAP-11, DEP-R09, fixed 2e-17, X_cert는 OPEN이다.

2026-09-14 Theory 79 뒤 전수 inventory는 80개 theory 문서·1,452개 display
수식·283개 Lean declaration이다. 상태는 `KERNEL_PASS=94`,
`CONDITIONAL_KERNEL_PASS=60`, `DEFINITION_ONLY=90`,
`PARTIAL_FORMALIZATION=94`, `SOURCE_THEOREM_UNFORMALIZED=82`,
`NOT_YET_FORMALIZED=1027`, `PARSE_REVIEW_REQUIRED=5`이며 금지 proof escape는 0건이다.
Lean은 two-stage failure identity와 finite outer/fiber selection의 논리만 검사한다.
FMT probability theorem, same-law weighted correlation과 numerical X_cert는 local axiom으로
넣지 않았고 계속 OPEN이다.

2026-09-14 Theory 80 뒤 전수 inventory는 81개 theory 문서·1,473개 display
수식·288개 Lean declaration이다. 상태는 <code>KERNEL_PASS=94</code>,
<code>CONDITIONAL_KERNEL_PASS=64</code>, <code>DEFINITION_ONLY=98</code>,
<code>PARTIAL_FORMALIZATION=100</code>, <code>SOURCE_THEOREM_UNFORMALIZED=85</code>,
<code>NOT_YET_FORMALIZED=1027</code>, <code>PARSE_REVIEW_REQUIRED=5</code>이며
금지 proof escape는 0건이다. Lean은 finite tower sum과 same-law
global/conditional strict-gate terminal, raw-moment normalization 대수만 검사한다.
FMT probability theorem, Markov의 actual analytic 입력, character moment source와
numerical X_cert는 local axiom으로 넣지 않았고 계속 OPEN이다.

2026-09-15 Theory 82 뒤 전수 inventory는 83개 theory 문서·1,528개 display
수식·295개 Lean declaration이다. 상태는 <code>KERNEL_PASS=94</code>,
<code>CONDITIONAL_KERNEL_PASS=69</code>, <code>DEFINITION_ONLY=113</code>,
<code>PARTIAL_FORMALIZATION=112</code>, <code>SOURCE_THEOREM_UNFORMALIZED=92</code>,
<code>NOT_YET_FORMALIZED=1043</code>, <code>PARSE_REVIEW_REQUIRED=5</code>이며
금지 proof escape는 0건이다. Lean은 outer atom·convolution analytic premises를
받은 raw-moment terminal과 strict normalized gate만 검사한다. FMT probability law,
finite character orthogonality, complex convolution proof와 numerical
fixed-primorial character-energy theorem은 local axiom으로 넣지 않았다. PAP-11,
DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-15 Theory 83 뒤 전수 inventory는 84개 theory 문서·1,561개 display
수식·300개 Lean declaration이다. 상태는 <code>KERNEL_PASS=96</code>,
<code>CONDITIONAL_KERNEL_PASS=73</code>, <code>DEFINITION_ONLY=119</code>,
<code>PARTIAL_FORMALIZATION=120</code>, <code>SOURCE_THEOREM_UNFORMALIZED=98</code>,
<code>NOT_YET_FORMALIZED=1050</code>, <code>PARSE_REVIEW_REQUIRED=5</code>이며
금지 proof escape는 0건이다. Lean은 power-regime scalar margin, best-entropy
factor monotonicity와 raw upper certificate의 strict-gate countermodel만 검사한다.
Montgomery--Vaughan·Dusart·Rosser--Schoenfeld analytic source theorem과 actual
fixed-primorial character energy는 local axiom으로 넣지 않았다. PAP-11,
DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.
