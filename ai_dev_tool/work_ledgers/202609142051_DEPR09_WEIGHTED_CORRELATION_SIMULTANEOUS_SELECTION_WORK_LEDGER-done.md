# DEP-R09 weighted correlation·simultaneous selection 작업원장

- 시작: 2026-09-14 20:51 KST
- 현재 상태: COMPLETE_READY_FOR_ATOMIC_LOCAL_COMMIT
- 사용자 승인: 기존 문헌을 먼저 감사하고, 필요한 경우 직접 정리·Lean 형식화·로컬 검증·문서 동기화·로컬 스테이징 및 커밋
- 금지·보류: actual prime sweep, threshold calculator, 장시간 계산, 외부 게시·연락, push/PR, `sorry`, `admit`, project-local `axiom`
- 선행 변경: 시작 시 `git status --short`는 빈 결과이며 branch는 `main...origin/main [ahead 31]`; 이번 작업 이전 비소유 변경 없음

## 목적과 완료조건

- 목적: Theory 77 식 (77.18)의 direct weighted-correlation 목표와 Maier Lemma 6 construction 조건을 같은 선택변수 `y`에서 동시에 만족시키기 위한 정확한 양화사·충분조건을 정식화하고, 기존 문헌이 그 조건을 실제 수치형으로 공급하는지 판정한다.
- 완료조건:
  1. Maier 원문과 후속 1차 문헌에서 선택변수·평균집합·소비식을 페이지/식 단위로 고정한다.
  2. `평균적으로 좋음`에서 `같은 y가 두 조건을 만족`으로 넘어가는 최소 유한 선택 lemma를 증명하거나, 필요한 추가 joint-moment 입력을 OPEN으로 분리한다.
  3. 기존 source theorem의 적용범위·상수·cutoff를 확인하고 drop-in 여부를 과장 없이 판정한다.
  4. 필요한 대수·유한 확률 논리를 exact Python/Lean으로 검증하되 analytic source theorem을 공리화하지 않는다.
  5. Theory·review·기계 원장·색인·METHODS/AGENTS·전수 Lean 원장·handoff를 동기화하고 검증한다.
  6. 새 bounded `X_cert` 범위가 생기면 즉시 중단·보고한다. 생기지 않으면 `X_cert OPEN`을 유지한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | `G,F,H` 정의는 바꾸지 않고 DEP-R09의 양화사만 정밀화한다 |
| 데이터·provenance | 영향 없음 | maximal-gap dataset과 actual artifact를 읽거나 생성하지 않는다 |
| 통계·정밀도 | 영향 있음 | 유한 평균·Markov/union-bound 조건을 exact rational로 검산하고 floating 결과만으로 증명하지 않는다 |
| 승인 경계 | 영향 있음 | 장시간 연산·실제 실험·threshold calculator는 수행하지 않는다 |
| 산출물·비덮어쓰기 | 영향 있음 | Theory 78·새 review·새 JSON/helper/test·새 timestamp handoff를 사용하고 기존 정본을 덮어쓰지 않는다 |
| 문헌·증거 등급 | 영향 있음 | source theorem, project lemma, conditional interface, OPEN analytic input을 분리한다 |
| Lean | 영향 있음 | 유한 선택·상수 대수 중 critical path만 형식화하고 금지 proof escape를 사용하지 않는다 |

## 접근 비교와 권장안

| 접근 | 정확성 | 비용 | 위험 | 판정 |
|---|---|---|---|---|
| 각 조건의 평균만 따로 증명하고 좋은 `y`를 동일시 | 낮음 | 낮음 | 서로 다른 `y`일 수 있는 양화사 오류 | 기각 |
| 두 bad-set 확률을 개별 상계하고 union bound로 교집합 보장 | 높음 | 낮음~중간 | 각 평균에 충분한 slack 필요 | 1차 권장 |
| 두 조건의 직접 joint weighted moment를 증명 | 잠재적으로 가장 강함 | 높음 | 새 해석정리가 필요할 수 있음 | union-bound slack이 부족할 때 후속 |

## 단계 현황

1. **DONE — authoritative source·현재 정본·Maier 선택변수 재구성**
2. **DONE — 기존 weighted correlation·short shifted character-sum·simultaneous-selection 문헌 감사**
3. **DONE — 최소 유한 선택 lemma와 numerical budget 정식화**
4. **DONE — exact helper·tests·Lean critical lemma 구현 및 검증**
5. **DONE — Theory 78·review·색인·정본 동기화**
6. **DONE — 전수 검증·새 handoff·원장 완료 이름 변경·로컬 커밋 준비**

## 단계별 기록

### 2026-09-14 20:51 KST — 작업 개시·영향도 분석

- 수행: 최신 handoff, AGENTS, 작업원장 규약, Theory 77 후속 재개점을 확인하고 세 접근을 비교했다.
- 파일: 이 작업원장.
- 명령·검증: `git status --short --branch`; 미완료 작업원장 검색.
- 결과: 선행 비소유 변경과 미완료 원장 없음. 별도 평균의 좋은 점을 동일시하는 접근은 기각하고 union-bound 충분조건을 우선 감사한다.
- 문제·결정: analytic source theorem은 아직 미확정이며 `X_cert` 범위는 전혀 좁혀지지 않았다.
- 다음 재개점: Theory 76--77과 Maier 1981 Lemma 6·formulas (I),(II)의 정확한 `y` 범위와 필요한 mass/pair 조건을 원문에서 재구성한다.

### 2026-09-14 20:55 KST — 사용자 지적에 따른 Lean 결합형 오류 재발성 감사

- 수행: 사용자가 제시한 `((18/7)*θ)*L` 대 `θ*((18/7)*L)` 첫 compile 설명을 오류 원장,
  현재 Lean 정본, git blame과 대조했다.
- 파일: `ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md`, `lean/README.md`, 이 작업원장.
- 명령·검증: 오류 원장 E117/E118/E119/E121 검색, `TheoryVerification.lean` 2508--2520행 확인,
  `git blame -L 2508,2520`.
- 결과: 인용문은 새 재발이 아니라 E117에 이미 기록된 2026-09-13 사건이며 commit
  `38f50320`에서 교정된 상태다. 다만 결합형 초안 실패 유형은 이후에도 반복됐으므로 기존
  예방책을 경계 정규화·direct compile·unused-premise 처리 규칙으로 강화했다.
- 문제·결정: `_h...`는 불필요한 가정을 숨기는 일반 해법이 아니다. source domain/interface를
  의도적으로 보존할 때만 주석과 함께 허용한다.
- 다음 재개점: 원래 단계 1로 돌아가 Theory 76--77과 Maier 1981의 `y` 양화사를 재구성한다.

### 2026-09-14 21:05 KST — LaTeX vertical-tab 커밋 재발 발견·자동 gate 구현

- 수행: Theory 77 출력의 `\varphi` 손상 징후를 계기로 AGENTS·docs·handoff·ai_dev_tool의
  UTF-8 text를 byte 단위로 검사했다.
- 파일: 현재 정본 6개 교정, 오류 원장 E126, `lean/tools/validate_text_integrity.py`,
  `tests/test_text_integrity_validator.py`, Lean ledger validator.
- 명령·검증: C0/C1 byte scan, exact line/context 추출, E108 legacy handoff 기록 대조.
- 결과: commit `2cccf31`의 현재 정본·handoff에 U+000B 9개, E108 legacy handoff에 1개를
  확인했다. handoff는 이력 보존 규칙에 따라 수정하지 않았고, 현재 정본 6개의 8개를
  `\varphi`로 교정했다. theory/review/AGENTS/METHODS/Lean 정본을 자동 검사하는 fail-closed
  validator와 in-memory negative regression을 추가했다.
- 첫 전수 validator는 과거 review 23의 U+0009 `\theta` 손상 1개를 추가 검출해 FAIL했다.
  해당 현재 참조 문서를 `(\theta,\alpha)`로 교정했으며 첫 FAIL을 검증 이력으로 보존한다.
- 재검증: negative regression 4/4 PASS, `py_compile` PASS, AGENTS·METHODS·theory·review·Lean
  정본 236파일 3,413,213 bytes의 text-integrity issue 0 PASS.

### 2026-09-14 21:10 KST — Maier 추출본 검색범위 오류

- 수행: Maier 추출 text의 기존 위치를 찾았다.
- 문제·결정: E108의 재발 방지 규칙과 달리 `tmp` 전체를 읽기 전용 검색해 access-denied
  경고를 대량 발생시켰다. 파일·프로세스 영향은 없으며 E127로 기록했다.
- 교정: 이후 모든 source 검색을 `tmp/pdfs/dep_r09_sources/`와 machine-ledger locator로 제한한다.
- 다음 재개점: page 7--12 native text와 printed 렌더를 대조해 Lemma 6의 동일 `y` 조건을 고정한다.
- 문제·결정: 링크·JSON·diff PASS는 hidden control 부재를 증명하지 않는다. 이후 별도
  text-integrity PASS를 필수 증거로 남긴다.
- 다음 재개점: 새 validator의 negative/positive 시험을 실행한 뒤 원래 단계 1 source 감사로 복귀한다.

### 2026-09-14 21:35 KST — Maier/FMT 선택변수 source-first 재구성

- 수행: Maier 1981 printed pp.263--268을 native text와 rendered page로 대조하고, Sono
  pp.527--530 및 Ford--Maynard--Tao Theorem 2·Lemma 3.1·Sections 4--6과 양화사를 비교했다.
- 결과: fixed \(P_1,P_2,P_3\)에서는 CRT \(y\bmod P(x)\)가 정확히 하나여서 고전
  \(y\)-평균은 존재하지 않는다. Sono/FMT actual proof에서는 sieve residue vector
  \(\boldsymbol a\)가 family 후보이고 vector마다 CRT \(m(\boldsymbol a)\)가 하나 정해진다.
- 판정: Theory 77의 “같은 \(y\)” 경고는 맞지만 평균 변수는 교정해야 한다. uniform
  correlation이면 선택 문제가 없고, vector-average이면 sieve-good·correlation-good의
  공통 finite failure mass가 새 analytic 의무다.
- 산출물: Theory 78, review 86, machine ledger, exact finite helper와 단위시험 초안.
- 전역 경계: published numerical joint-good mass와 direct correlation source는 확인되지
  않았고 <code>PAP-11</code>, <code>DEP-R09</code>, fixed coefficient,
  \(X_{\rm cert}\)는 OPEN이다.
- 다음 재개점: finite union-selection lemma를 단일 Lean 정본에 추가하고 즉시 direct compile한다.

### 2026-09-14 21:50 KST — finite selection Lean·exact helper 검증

- 구현: <code>source/dep_r09_maier_shift_selection.py</code>,
  <code>tests/test_dep_r09_maier_shift_selection.py</code>, machine ledger,
  TheoryVerification 단일 파일의 두 theorem.
- Lean: 세 bad finset의 cardinality 합이 전체 family보다 작으면 동시 good candidate가
  존재하는 lemma와 singleton strict budget의 zero-count 결론을 추가했다.
- direct compile: <code>lake env lean FGKMTSono/TheoryVerification.lean</code> PASS.
  새 선언을 쌓기 전에 바로 compile해 이번에는 곱 결합형 초안 재발이 없었다.
- Python: 새 selection 시험 7개와 text-integrity regression 4개, 합계 11/11 PASS.
  수정·신규 Python 5개 <code>py_compile</code> PASS.
- 전수 원장 1차: 79 theory, 1,439 formulas, 278 declarations,
  <code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=58</code>,
  <code>NOT_YET_FORMALIZED=1027</code>, banned escape 0, text-integrity issue 0 PASS.
- 경계: Lean은 finite selection logic만 인증한다. analytic bad-event bound,
  Maier/FMT source theorem과 direct correlation은 premise/open 상태다.
- 작업 중 도구 오류: raw-template와 Markdown code delimiter 충돌 및 line-array marker
  오류를 E128로 추가했다. 거부된 patch는 저장소를 바꾸지 않았다.
- 다음 재개점: AGENTS·METHODS·T1·색인·종합리뷰·Lean README를 최신 판정과 원장 수치로
  동기화한 뒤 전수 검증한다.

### 2026-09-14 21:28 KST — 정본 동기화·전체 검증

- 동기화: Theory 78·review 86의 판정을 AGENTS, METHODS, theory 색인, T1 원장,
  Theory 77 successor, 종합리뷰와 Lean 안내문에 반영했다.
- Lean: 단일 정본 direct compile와 <code>lake build</code>가 모두 PASS했다. 전수 원장은
  79 theory, 1,439 formulas, 278 declarations,
  <code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=58</code>,
  <code>NOT_YET_FORMALIZED=1027</code>, 금지 proof escape 0건이다.
- text integrity: 정본 239개 파일을 검사해 제어문자 issue 0 PASS를 확인했다.
- Python 전체 suite 첫 호출은 sandbox 임시폴더 권한 때문에 862개 중 82개가
  <code>PermissionError</code>로 실패했다. 이를 코드 실패로 채택하지 않고 오류 원장 E125에
  절차 재발로 기록했다. 동일 명령을 승인된 정상 로컬 권한에서 재실행해 862/862 PASS,
  82.525초를 확인했다.
- 판정: finite selection 논리와 기계 산출물은 검증됐지만 analytic joint-good mass가 없으므로
  <code>PAP-11</code>, <code>DEP-R09</code>, fixed <code>2e-17</code>,
  numerical <code>X_cert</code>는 계속 OPEN이다.
- 다음 재개점: 새 timestamp handoff를 작성하고 최종 diff·참조·staging 검증 뒤 로컬 commit한다.

### 2026-09-14 21:31 KST — 마감 검증·handoff

- 새 handoff: <code>handoff/202609142130_HANDOFF.md</code>.
- handoff·작업원장·오류 원장 text-integrity: 3파일, issue 0 PASS.
- 통합 Lean validator: local link 1,521개, formula 1,439개, declaration 278개,
  banned escape 0, text-integrity 239파일 issue 0 PASS.
- <code>git diff --check</code>: whitespace error 0. 표시된 LF/CRLF 문구는 Git의
  기존 line-ending 경고이며 diff 오류가 아니다.
- 완료 판단: 사용자 요청의 재발성 감사, 예방 강화, Theory 78 후속 연구,
  정본 동기화와 검증이 끝났다. 작업원장을 <code>-done</code>으로 바꾸고 이 원장을 포함한
  현재 세션 변경을 하나의 로컬 commit으로 묶는다. push/PR은 수행하지 않는다.

## 현재 재개점

다음 root 작업은 Theory 78을 기준으로 FMT Sections 4--6의 construction-law finite
positive mass를 source-first로 감사한다. fixed Maier \(y\)를 평균 변수로 되돌리지 않는다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 source theorem 상태 분리
- [x] 결과 색인·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
