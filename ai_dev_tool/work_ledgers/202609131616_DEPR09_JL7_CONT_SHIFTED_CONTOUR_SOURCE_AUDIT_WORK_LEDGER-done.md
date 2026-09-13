# DEP-R09 JL7-CONT shifted-contour source 감사 작업원장

- 시작: 2026-09-13 16:16 KST
- 현재 상태: COMPLETE
- 사용자 승인: `X_cert` 계산기 제작 전 필요한 정규화·증명 작업을 권장 순서대로 수행하고,
  선행연구를 먼저 조사한 뒤 필요한 경우 직접 증명하며, 필요하면 Lean 형식화·검증하고
  세션 핸드오프 및 로컬 스테이징·커밋까지 수행
- 금지·보류: 실제 prime sweep, maximal-gap 재계산, threshold calculator 제작,
  fixed `2e-17` 또는 `X_cert`의 조기 인증, 장시간 연산의 Codex 임의 실행,
  package 설치, `sorry`·`admit`·project-local `axiom`, push·PR
- 선행 변경: 시작 commit `febb4d91b8c64d87098288135aa814a5edd3d5db`,
  `git status --short` 출력 없음(깨끗한 작업트리)

## 목적과 완료조건

- 목적: Jutila printed p.53의 shifted-contour estimate에 숨은
  `\ll_\theta` multiplier와 finite cutoff를 source-first 방식으로 추적하고,
  실제 식 (3.6) parameter 범위에서 수치화 가능한 부분과 남는 analytic blocker를
  서로 분리한다.
- 완료조건:
  1. `I_d(s,chi)` 정의, contour, `M,N,d,D,theta` 범위와 해당 인쇄식을 원페이지로 확정한다.
  2. Jutila가 사용한 선행 lemma·functional equation·Dirichlet-polynomial estimate를
     peer-reviewed 원문에서 먼저 찾고 실제 가정과 결론이 맞는지 대조한다.
  3. drop-in explicit source가 있으면 exact multiplier·공통 finite cutoff를 기록하고,
     없으면 필요한 직접 유한 증명을 sub-obligation으로 분해한다.
  4. 닫히는 dependency-critical 유한 대수만 Python/Lean으로 검증하고, source theorem을
     local axiom으로 대체하지 않는다.
  5. theory·review·기계 원장·상위 정본·Lean inventory를 같은 판정으로 동기화한다.
  6. 전체 검증, 새 timestamp handoff와 한국어 로컬 커밋을 완료한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | root blocker | 원문 contour 방향, pole·residue, 엄격/비엄격 범위와 `theta` 의존성을 보존 |
| 데이터·provenance | 원문 중심 | native text/OCR을 구분하고 OCR은 locator로만 사용; 모든 핵심 식은 렌더링 원페이지 대조 |
| 통계·정밀도 | 통계 실험 아님 | exact rational·고정 precision 계산은 analytic proof를 대신하지 않음 |
| 승인 경계 | actual 실행 금지 | 문헌·증명·toy 검증만 수행; 장시간 연산·새 설치가 필요하면 사용자에게 요청하고 중단 |
| Lean 증거 | fail-closed | source theorem은 premise/미형식화로 유지; `sorry`·`admit`·local `axiom` 금지 |
| 산출물 | 비덮어쓰기 | 새 theory/review/data/원장/handoff를 만들고 기존 정본에는 successor 상태만 동기화 |

## 단계 현황

1. **COMPLETE — Jutila 원문 식·기호·source citation inventory 확정**
2. **COMPLETE — 적용 가능한 peer-reviewed explicit 선행정리 조사·대조**
3. **COMPLETE — actual shifted-contour multiplier 또는 fail-closed blocker 정식화**
4. **COMPLETE — Python 및 필요 Lean 형식화·검증**
5. **COMPLETE — theory/review/상위 정본·색인 동기화**
6. **COMPLETE — 전체 검증·handoff·완료 원장 이관·로컬 커밋**

## 단계별 기록

### 2026-09-13 16:16 KST — 작업 시작과 기준선 확인

- 수행: 최신 handoff와 Theory 66의 첫 후속 의무가 `JL7-CONT`임을 확인했다.
- 파일: `handoff/202609131615_HANDOFF.md`, Theory 66, 이 원장.
- 명령·검증: `git status --short`, `git rev-parse HEAD`, 최신 원장·handoff 열람.
- 결과: 작업트리는 깨끗하고, fixed `2e-17`·`X_cert`는 OPEN이다.
- 문제·결정: Jutila PDF는 text layer가 사실상 없으므로 OCR은 위치 찾기에만 사용하고
  인쇄 페이지 이미지가 수식 판정의 정본이다.
- 다음 재개점: repo 전체에서 `I_d`, `JL7-CONT`, p.53 contour 식과 Jutila가 인용한
  lemma·참고문헌을 찾고 렌더링 페이지와 대조한다.

## 현재 재개점

Lean status mapping과 formula inventory를 재생성하고, target·전체 검증으로 문서·코드·
형식검증의 판정이 같은지 확인한다.

### 2026-09-13 16:42 KST — 원문 정의와 peer-reviewed source-first 경로 확정

- 수행: Jutila printed pp.48, 52--53을 렌더링 원페이지와 대조하고 `I_d(s,chi)`의
  integrand, line, 변수 범위를 전사했다. Bennett et al. 2021 Lemma 5.6 (5.3)과
  Hasanalizade--Shen--Wong 2022 Proposition 3.8을 native text와 렌더링 페이지에서
  다시 대조했다.
- source:
  - Jutila scan: native text 18 bytes, OCR locator 뒤 렌더링 원페이지 판정.
  - Bennett et al.: native text와 printed p.1469 Lemma 5.6 대조.
  - Hasanalizade--Shen--Wong: 저자 공개 peer-reviewed PDF를 새로 내려받아 native text와
    printed p.286 Proposition 3.8 대조; SHA-256
    `9c515d71913ba13beb2a077bc354c50d41fb79e2f4f12696a801e7704e7b39fa`.
- 결과: `s=u+iv`, `0<=u<=2theta`, `|v|<=2T`, `w=-1+theta+iy`이면
  `Re(1+s+w)=theta+u`다. 비주지표 branch에는 Bennett--Rademacher Dirichlet
  bound를 쓸 수 있다. 주지표 branch에는 `L(z,chi0)=zeta(z) product_{p|q}(1-p^-z)`와
  Hasanalizade et al.의 Dedekind-zeta bound를 쓸 수 있다.
- 핵심 판정: 주지표에서 Rademacher의 `|1+z|/|1-z|`를 따로 거칠게 잡으면 높이 손실이
  생기지만, actual `0<Re z<=3theta<=1/7`에서는 비율 자체가 `<=4/3`이다. 따라서 두
  branch 모두 `sqrt(qT)*sqrt(1+|y|)` scale을 유지한다.
- 문제·결정: 공개 secondary 요약만으로 닫지 않고 Math. Comp. 2022 peer-reviewed
  Proposition 3.8 원문을 증거 source로 고정한다. contour 이동 등식 자체는 이번
  multiplier 감사의 범위를 넘으므로 source-unformalized 상태를 유지한다.
- 다음 재개점: uniform L-bound 상수, Gamma 적분과 `N>=M` power difference를 합성해
  fully elementary `C_CONT(theta)` majorant를 산출한다.

### 2026-09-13 16:44 KST — uniform multiplier와 초등 majorant 정식화

- 수행: 비주지표 coefficient를 `C_NP<9/4`, 주지표 coefficient를 `C_P<12`로 각각
  유리 상계하고, 공통 vertical-line bound와 power difference·Gamma 적분을 합성했다.
- 결과: actual 식 (3.6) 범위에서
  `C_CONT(theta)=(96 sqrt(2)/pi) zeta(1+theta)(2/theta+1)`과
  calculator-safe majorant `48(1+1/theta)(2/theta+1)`을 얻었다.
  `theta=1/21`에서는 각각 약 `40102.3459386232`, 정확히 `45408`이다.
- 경계: contour 이동, Rademacher 두 source theorem, complex Gamma improper integral은
  Lean 독립 증명 대상에서 제외하지 않고 각각 source-unformalized/partial로 남긴다.
  따라서 `JL7-CONT`만 actual-input parameterized explicit이고, Lemma 3·residue·terminal
  absorption·averaged replay와 `X_cert`는 OPEN이다.
- 코드·문서: Theory 67, review 74, contour JSON, Python evaluator와 fail-closed test 작성.
- 검증: `py_compile` 및 target unittest 9/9 PASS; JSON strict parse와 evaluator 진단 PASS.
- 발견·수정한 실수: 초기 JSON 초안의 Jutila SHA 문자열 뒤에 임시 메모 조각이 섞였으나
  어떤 검증·판정에도 사용하기 전에 원 PDF SHA-256과 대조해 교정했다. Markdown 초안에는
  JavaScript patch 문자열의 `\t`·`\b` 해석으로 `theta` 탭과 `bar` backspace가 생겼고,
  전수 control-character 검사에서 발견해 `apply_patch`로 모두 교정했다. 한 PowerShell
  점검 명령의 빈 pipe ParserError도 `$rows` 변수 방식으로 재실행했다.
- 다음 재개점: 새 수식의 Lean 상태를 식별자별로 등록하고 generator·validator·lake build를
  통과시킨다.

### 2026-09-13 16:46 KST — Theory 67 유한 대수 Lean 직접 검증

- 수행: 단일 `TheoryVerification.lean`에 실제 contour 실수부 범위, 높이 budget,
  principal ratio의 cross-multiplied `16/9`, `C_NP<9/4`, `C_P<12`, branch 통합,
  power-difference triangle, contour coefficient identity, elementary majorant와 endpoint
  `45408`을 추가했다.
- 결과: 직접 `lake env lean FGKMTSono/TheoryVerification.lean` PASS.
- proof 경계: `sorry`, `admit`, project-local `axiom`을 사용하지 않았다. external analytic
  source와 complex identity는 status 원장에서 `SOURCE_THEOREM_UNFORMALIZED` 또는
  `PARTIAL_FORMALIZATION`으로 유지한다.
- 다음 재개점: 25개 Theory 67 display 식을 status/notes에 전수 등록한 뒤 inventory를
  생성하고 전체 검증한다.

### 2026-09-13 16:48 KST — Lean 전수 상태 분류와 1차 기계검증

- 수행: Theory 67의 tagged·untagged display 25개를 각각 증거 수준으로 분류하고,
  단일 Lean 파일의 15개 새 declaration에 연결했다.
- 결과: inventory 68개 theory 문서·1,208식, declaration 192개,
  `KERNEL_PASS=61`, `CONDITIONAL_KERNEL_PASS=31`, `DEFINITION_ONLY=30`,
  `PARTIAL_FORMALIZATION=35`, `SOURCE_THEOREM_UNFORMALIZED=51`,
  `NOT_YET_FORMALIZED=995`, `PARSE_REVIEW_REQUIRED=5`; banned escape 0건.
- 검증: strict JSON PASS, target unittest 9/9 PASS, generator PASS, validator PASS,
  Lean 4.34.0-rc2 직접 check PASS, `lake build` 8,765 jobs PASS.
- 운영상 실패와 복구: 첫 generator/validator 호출을 repository root의 잘못된 `tools/...`
  경로로 실행해 file-not-found가 났고, 첫 `lake build`도 root에서 실행해 lakefile-not-found가
  났다. 두 실패는 성공으로 기록하지 않고 `lean/tools/...` 절대 상대경로 및 `lean/`
  working directory에서 독립 재실행했다. E115에 기록했다.
- 다음 재개점: METHODS·AGENTS·theory/review 색인·T1 ledger·predecessor successor note·
  Lean README를 Theory 67 판정과 맞춘 뒤 inventory를 마지막으로 재생성한다.

### 2026-09-13 16:50 KST — 상위 정본 동기화와 handoff 작성

- 수행: AGENTS, METHODS, theory/review 색인, T1 obligation ledger, Theory 65·66 successor
  note, 문헌 종합, Lean README를 `JL7-CONT explicit / 나머지 terminal·PAP·X_cert OPEN`
  판정으로 동기화했다. 오류 원장 E115와 새 timestamp handoff도 작성했다.
- 결과: 최신 analytic 정본은 Theory 67·review 74이며, 다음 첫 gate는
  `JL7-LEMMA3`로 이동했다. 역사 문서의 과거 next action은 삭제하지 않고 successor
  완료 메모로 범위를 고정했다.
- 다음 재개점: final generator·validator, target·전체 unittest, strict text/link/formula,
  Git diff를 재검증하고 완료 원장으로 이름을 바꾼 뒤 로컬 커밋한다.

### 2026-09-13 16:54 KST — 최종 검증 완료

- target unittest 9/9 PASS, 전체 unittest 최종 정상 권한 재실행 750/750 PASS
  (61.950초).
- Lean 4.34.0-rc2 direct check PASS, `lake build` 8,765 jobs PASS.
- generator·validator PASS: theory 68개, display 1,208식, declaration 192개,
  banned proof escape 0건, `NOT_YET_FORMALIZED=995`.
- strict JSON·Python py_compile·Git diff whitespace PASS. 첫 strict 정적검사는 이력 문서가
  과거 손상 예시를 문자 그대로 담고 있고 handoff가 아직 생성 전 `-done` 경로를 가리켜
  false positive를 냈다. 신규 Theory 67·review 74와 실제 변경 대상의 control character는
  0건이며, 안전한 이름 변경 뒤 최종 경로 검사를 다시 수행한다.
- 실제 prime sweep, maximal-gap 재계산, threshold calculator, package 설치는 수행하지 않았다.
- 안전한 `-done` 이름 변경 뒤 변경·신규 text 21파일 strict UTF-8/control 0건,
  local Markdown link 1,515건, 새 문서 display delimiter 4파일과 bare `qquad` 검사를
  issue 0으로 통과했다. `git diff --check`도 whitespace error 0이다.
- 전체 파일을 staging한 뒤 실행한 첫 `git diff --cached --check`에서는 Theory 67의
  두 줄에서 후행 공백을 추가로 발견했다. 이를 제거한 뒤 문서 hash에 의존하는 Lean
  inventory를 재생성·검증하고 cached diff를 다시 검사한다. 이 문제는 수식이나 판정에는
  영향을 주지 않았으며, 발견 전 cached 상태를 최종 PASS로 간주하지 않았다.
- 다음 재개점: staged/cached diff를 마지막으로 검사하고 이 stage를 로컬 커밋한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 source theorem 경계 분리
- [x] 결과 색인·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
