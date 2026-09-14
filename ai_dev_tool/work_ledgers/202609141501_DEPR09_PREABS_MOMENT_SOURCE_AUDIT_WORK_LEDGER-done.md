# DEP-R09 절댓값 이전 moment·pointwise PAP source 감사 작업원장

- 시작: 2026-09-14 15:01 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: `X_cert`를 좁히기 위한 권장 증명 작업, 필요한 문헌 조사·다운로드,
  필요 시 proof-escape 없는 Lean 형식화, 단계별 로컬 staging·commit
- 금지·보류: actual prime sweep, 장시간 계산, threshold calculator, 외부 연락·게시,
  `sorry`·`admit`·project-local `axiom`, fixed `2e-17` 또는 `X_cert`의 근거 없는 승격
- 선행 변경: 시작 commit `4decd50`; `git status --short` 출력 없음
- 적용 지침: `impact-analysis`, `plan-doc`, `session-handoff`, PDF native-text-first·render 대조

## 목적과 완료조건

- 목적: Theory 75가 남긴 R09 우선경로 중 (a) fully numerical pointwise PNT in AP와
  (b) Gallagher 절댓값 이전 character/zero second moment가 실제 Maier PAP 계약에
  들어갈 수 있는지를 source statement와 exact normalization으로 판정한다.
- 핵심 선행 질문: Maier downstream이 모든 modulus를 요구하는지, 평균에서 선택한 하나의
  good modulus로 충분한지 원문에서 다시 고정한다.
- 완료조건:
  1. peer-reviewed primary source와 정확한 적용범위를 page/equation 단위로 기록한다.
  2. 필요한 moment/PNT inequality를 현재 `(d<=186, Q=X^(1/d), T=Q^5)` 계약으로 정규화한다.
  3. drop-in, conditional redesign, 수치 불충분을 구분하고 과장 없는 theory/review를 작성한다.
  4. 계산 가능한 `X_cert` 범위가 새로 생기면 즉시 중단해 사용자에게 보고한다.
  5. 필요한 terminal algebra만 Lean으로 형식화하고 source theorem을 axiom으로 넣지 않는다.
  6. 이론·Lean 원장·색인·handoff를 검증하고 로컬 commit한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | end-bounded `G`와 iterated log는 불변; PAP quantifier와 modulus 선택만 원문 재감사 |
| 데이터·provenance | 영향 없음 | maximal-gap dataset 미사용; 논문 hash·page·equation만 고정 |
| 통계·정밀도 | 영향 있음 | asymptotic `O`를 숫자로 승격하지 않고 exact/rational 또는 100-dps 진단 분리 |
| 승인 경계 | 영향 있음 | 문헌·짧은 검증만 수행; 장시간 계산이 필요하면 중단·사용자 요청 |
| 산출물·비덮어쓰기 | 영향 있음 | 새 theory/review/data/handoff 사용; 기존 정본은 링크하고 덮어쓰지 않음 |
| 형식검증 | 확인 필요 | 새 terminal inequality가 상위 결론에 쓰일 때만 단일 Lean 파일에 추가 |

## 접근 비교

| 접근 | 정확성·적합성 | 비용 | 주 위험 | 현재 순위 |
|---|---|---:|---|---:|
| fully numerical pointwise PNT in AP | Maier PAP에 가장 직접적 | 문헌 선별 2--6주 규모 | power-size modulus와 작은 coefficient를 동시에 못 줄 수 있음 | 1 |
| pre-absolute-value second moment + good-modulus 선택 | phase 손실 전 구조를 보존할 가능성 | source·downstream 재설계 필요 | 평균 quantifier가 residue-class pointwise 결론에 부족할 수 있음 | 2 |
| X-dependent signed minorant | 논리적 가능성은 남음 | 새 proof architecture | main mass·condition number·tail 모두 재증명 | 3, 앞 두 경로 실패 후 |

## 단계 현황

1. **COMPLETE — 원문 quantifier·필요 inequality 재구성**
2. **COMPLETE — primary-source 후보 전수 screen 및 적용성 판정**
3. **COMPLETE — 수치 필요조건·cutoff 합성 또는 실패 certificate**
4. **COMPLETE — theory/review/data와 필요한 Lean 항목 작성**
5. **COMPLETE — 원장·색인·링크·금지 proof escape 검증**
6. **COMPLETE — 새 handoff, `-done` 이름 변경, 로컬 staging·commit**

## 단계별 기록

### 2026-09-14 15:01 KST — 재개·영향도 preflight

- 수행: 최신 handoff, Theory 75·review 82, transfer feasibility JSON, 작업원장 규약,
  적용 skills와 current goal을 확인했다.
- 파일: `handoff/202609140525_HANDOFF.md`,
  `docs/method/theory/75_Sono_FMT_DEPR09_hybrid_smoothing_cancellation_transfer_feasibility.md`
- 명령·검증: `git status --short`, `git log -3 --oneline`, fixed project files read-only 확인
- 결과: 시작 tree clean. actual 계산·설치가 필요하지 않은 source-first R09 연구가 승인 범위와 일치한다.
- 문제·결정: Theory 75의 “평균 정리는 자동 drop-in이 아니다”는 맞지만, good-modulus 선택으로
  downstream을 재설계할 여지를 배제하지 않도록 Maier 원문 quantifier를 먼저 재검사한다.
- 다음 재개점: Maier 1981 Lemmas 1--2와 Gallagher 1970 식 (24)--(30)을 native text와
  렌더 페이지에서 대조하고 필요한 modulus/residue quantifier를 표로 고정한다.

### 2026-09-14 15:51 KST — Maier--Gallagher quantifier·후보 source 원문 감사

- 수행: Maier printed pp.260, 266--268과 Gallagher printed pp.337--338을 text layer로
  추출한 뒤 렌더 이미지와 대조했다. Akbary--Hambrook 2013, Sedunova 2018,
  Bennett--Martin--O'Bryant--Rechnitzer 2018 PDF를 공개 원문에서 내려받아 SHA-256을
  고정하고 native text와 theorem 페이지 렌더를 대조했다. OCR은 사용하지 않았다.
- 원문 해시: Akbary--Hambrook
  `797bac5529cfacba249ffe367ca665304fca53f45b0ee17068b9dd13d58da32a`,
  Sedunova `556e559b70765bf8c36052c926d9c586b04b609597f539e4c4e282912accfd60`,
  Bennett et al.
  `e51f8b8f63486c2259efe076d367504f08dda0fe9e99dc35bf36de544ffc0601`.
- 결과: Maier는 각 admissible column에 pointwise Lemma 2를 적용하지만 이후에는 허용 열
  전체의 총 prime lower bound만 사용한다. 따라서 일반 평균정리는 drop-in이 아니나,
  그 특수 residue subset의 합을 직접 제어하는 second moment라면 downstream redesign은
  논리적으로 가능하다.
- 후보 screen: Akbary--Hambrook/Sedunova의 fully explicit L1 상계는 양의
  `X log(X)^c` main floor 때문에 fixed relative PAP budget을 직접 인증하지 못한다.
  Bennett et al. pointwise bound는 `q>10^5` branch에서 Maier scale `Y=q^d`와
  `d<=186`이 source cutoff와 양립하지 않으며, error normalization도
  `c_psi(q)Y/log Y`라 `Y/phi(q)` 상대오차로는 악화된다.
- 문제·결정: Friedlander--Goldston 1996 공개 PDF 미러는 Wayback 차단 페이지로 바뀌어
  로컬 다운로드가 실패했고 빈 파일은 생성되지 않았다. DOI·저자 공개 검색문에서
  fixed-modulus variance의 범위와 조건성을 확인하되 원문 식을 명시 상수로 승격하지 않는다.
- 다음 재개점: exact normalization과 수치 failure certificate를 코드·JSON·Theory 76으로
  고정하고 aggregate second-moment terminal implication만 Lean에 형식화한다.

### 2026-09-14 16:14 KST — 수치 failure certificate·Theory 76·review 84 작성

- 수행: Akbary--Hambrook·Sedunova L1 RHS floor, Bennett large-modulus cutoff와
  relative PAP normalization을 fixed FGKMT Python으로 재계산했다. Maier admissible subset의
  aggregate character-moment 충분조건을 유도하고 기술 정본 Theory 76과 비전문 검토 review 84를
  작성했다.
- 파일: `source/dep_r09_preabsolute_moment_screen.py`,
  `tests/test_dep_r09_preabsolute_moment_screen.py`,
  `docs/method/theory/data/Sono_FMT_DEPR09_preabsolute_moment_source_screen_v1.json`,
  `docs/method/theory/76_Sono_FMT_DEPR09_preabsolute_moment_pointwise_PNT_source_audit.md`,
  `docs/review/84_20260914_DEPR09_preabsolute_moment_pointwise_PNT_source_타당성검토.md`
- 명령·검증: `py_compile`; dedicated unittest 9/9 PASS; 120-dps diagnostic 출력과 machine
  ledger 수치를 대조했다. 이후 machine-ledger numeric drift를 직접 검사하는 열 번째 test를
  추가했다.
- 결과: explicit L1 두 후보는 direct certificate floor가 PAP budget을 통과하지 못한다.
  Bennett large-$q$ cutoff는 경계부터 필요한 `d>1257`, 첫 primorial에서 `d>3702`라
  current `d<=186`과 겹치지 않는다. aggregate second-moment budget은 pointwise budget의
  정확히 `M`배지만 이를 공급할 fully numerical individual-primorial source는 식별하지 못했다.
- 문제·결정: 이 결과는 actual error 하한이나 모든 moment 방법의 불가능성 명제가 아니다.
  새로운 `X_cert` 범위는 생기지 않았으므로 장시간 계산·calculator는 계속 금지한다.
- 다음 재개점: Theory 76의 두 terminal algebra를 단일 Lean 파일에 조건부 형식화하고,
  verification status·generator note·inventory를 동기화한다.

## 현재 재개점

Theory 76 식 (76.15)와 (76.22)--(76.23)의 terminal algebra를 단일 Lean 파일에
proof escape 없이 형식화하고 원장에 정확한 조건부 상태로 연결한다.

### 2026-09-14 16:27 KST — Theory 76 Lean 형식화·정본 종합보고서 동기화

- 수행: Bennett source-cutoff no-overlap과 aggregate Cauchy terminal을 단일
  `TheoryVerification.lean`에 추가하고 식 76.1--76.25의 상태·설명을 전수원장에 연결했다.
  종합 진행현황 report 83, Lean README 두 곳, AGENTS status와 오류 원장을 Theory 76의
  범위·수치·OPEN 판정에 맞게 갱신했다.
- 검증: 첫 Lean 초안의 `mul_le_mul` side-condition과 종료된 goal 뒤 `ring` 호출을 교정한
  다음 direct compile exit 0을 확인했다. generator는 theory 77개·display 1,406식,
  `KERNEL_PASS=91`, `CONDITIONAL_KERNEL_PASS=56`, declaration 272개, 금지 proof escape
  0건을 생성했고 validator가 PASS했다.
- 문제·결정: 식 (76.3)의 `\qquad` 탈자를 commit 전에 교정했다. analytic source theorem은
  local axiom으로 넣지 않았고 aggregate implication만 조건부 커널 검증으로 보존했다.
- 다음 재개점: 최종 정본 상태에서 generator·validator·`lake build`·target/full unittest·
  Markdown link·UTF-8·`git diff --check`를 다시 실행한다.

### 2026-09-14 16:35 KST — 최종 회귀·형식검증 완료

- 검증: Theory 76 targeted 10/10 PASS, 전체 정상 로컬 unittest 842/842 PASS
  (80.492초), `lake build` 8,765 jobs PASS, generator·validator PASS, JSON 3개 parse PASS,
  변경 20파일 strict UTF-8/control character PASS, 핵심 Markdown 5파일 local link PASS,
  `git diff --check` PASS.
- sandbox 분리: 첫 전체 suite는 `TemporaryDirectory` 권한 때문에 82 error였고 코드 판정으로
  쓰지 않았다. 동일 suite를 사용자가 허가한 정상 로컬 권한에서 다시 수행해 전부 통과했다.
  첫 실행이 저장소 `tmp`에 남긴 정확히 식별된 14개 임시 폴더만 안전경로 검사 후 삭제했다.
- 파일: `handoff/202609141635_HANDOFF.md`를 새로 작성했다.
- 다음 재개점: 이 원장을 `-done`으로 바꾸고 변경 범위를 diff로 감사한 뒤 로컬 staging·commit한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 actual 정리 증거 상태 분리
- [x] 결과 색인·이론 정본·Lean 원장 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
