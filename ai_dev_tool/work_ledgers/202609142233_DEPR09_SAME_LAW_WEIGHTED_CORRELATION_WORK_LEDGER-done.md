# DEP-R09 same-law weighted-correlation 조건부분해 작업원장

- 시작: 2026-09-14 22:33 KST
- 현재 상태: COMPLETE
- 사용자 승인: \(X_{\rm cert}\)를 좁히는 source-first 정규화·증명 연구, 필요한
  문헌조사·Lean 형식화·exact 소규모 검증, 정본 문서·handoff 갱신, 로컬 staging·commit
- 금지·보류: actual prime sweep, threshold calculator, 장시간 계산, 외부 게시·연락,
  push/PR, <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>
- 선행 변경: 시작 시 branch <code>main...origin/main [ahead 33]</code>,
  <code>git status --short</code>는 빈 결과. 직전 정본 commit은 <code>1debb5e</code>이고
  비소유 변경·진행 중 작업원장은 없다.

## 목적과 완료조건

- 목적: Theory 79의 joint outcome \((\mathbf A,\mathbf N')\)에서 direct weighted
  prime-error badness를 정확히 정의하고, global expectation을 outer/inner conditional
  expectation으로 분해해 source theorem이 충족해야 할 최소 계약을 고정한다.
- 완료조건:
  1. Theory 77--79와 FMT 1차 source의 변수·확률법칙·CRT 이동량을 식 단위로 대조한다.
  2. nonnegative badness, threshold, global/fiberwise failure와 tower decomposition을
     유한 확률공간에서 정확히 정식화한다.
  3. 기존 선행연구가 이 same-law weighted bound를 실제로 주는지 source/page/equation과
     양화사·수치상수·cutoff를 개별 검토한다.
  4. drop-in source가 없으면 필요한 최소 신규 analytic lemma와 충분조건을 분리한다.
  5. dependency-critical 유한 합·Markov·fiber averaging 대수는 exact Python과 필요한
     경우 Lean으로 검증하되 analytic theorem을 공리로 넣지 않는다.
  6. Theory·review·기계 원장·색인·METHODS/AGENTS·Lean inventory·handoff를 동기화한다.
  7. 기존보다 새로운 bounded \(X_{\rm cert}\) 범위가 생기면 즉시 작업을 중단하고
     사용자에게 인라인 보고한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | \(G,F,H\)는 변경하지 않고 DEP-R09의 weighted badness와 joint-law 양화사만 정밀화 |
| end-bounded 의미론 | 영향 없음 | maximal-gap record·interval을 읽거나 변경하지 않음 |
| 데이터·provenance | 영향 있음 | FMT·Maier·variance source의 판본·page·equation·hash/read mode를 고정 |
| 통계·정밀도 | 영향 있음 | asymptotic average를 same-law finite failure로 자동 승격하지 않고 exact finite 대수만 인증 |
| 승인 경계 | 영향 있음 | 문헌·증명·작은 검산만 수행하고 장시간 계산은 새 bounded range 뒤 별도 요청 |
| 산출물·비덮어쓰기 | 영향 있음 | Theory 80·review·machine ledger를 새 파일로 만들고 기존 정본에는 successor만 추가 |
| Lean 증거 | 영향 있음 | tower/finite-sum terminal만 형식화하고 character-sum source theorem은 premise도 없이 OPEN 유지 |

## 접근 비교와 권장안

| 접근 | 정확성 | 비용 | 주요 위험 | 판정 |
|---|---|---|---|---|
| joint law에서 badness를 정의하고 tower expectation으로 분해 | 높음 | 중간 | conditional law와 CRT 의존성을 빠뜨릴 수 있음 | 1차 권장 |
| 모든 outcome에 pointwise correlation 상계를 요구 | 매우 높음 | 매우 높음 | 기존 PAP보다 강해져 불필요하게 난해 | 기각 또는 최후 수단 |
| outer-good 각 fiber의 uniform conditional second moment | 높음 | 높음 | uniformity가 global 평균보다 강할 수 있음 | global route 실패 시 2차 |
| 결정론적 CRT outcome을 별도 구성 | 불명 | 매우 높음 | FMT covering 성공과 correlation을 동시에 보존할 근거 없음 | 현재 보류 |

## 단계 현황

1. **DONE — 기존 식·확률법칙·source locator inventory**
2. **DONE — same-law badness와 tower/fiberwise finite contract 정식화**
3. **DONE — 선행연구 source screen과 drop-in 판정**
4. **DONE — exact helper·tests·dependency-critical Lean**
5. **DONE — Theory 80·review·기계 원장·정본 동기화**
6. **DONE — 전수 검증·handoff·완료 이름 변경 준비**

## 단계별 기록

### 2026-09-14 22:33 KST — 재개·영향도 분석

- 수행: 최신 handoff, git clean 상태, 작업원장 규약, Theory 79의 다음 gate와 승인 경계를
  확인하고 세 가지 analytic route를 비교했다.
- 파일: 이 작업원장.
- 명령·검증: <code>git status --short --branch</code>, 최신 handoff·AGENTS·관련 skill·
  작업원장 규약 읽기, theory/review locator 검색.
- 결과: 직전 턴은 authoritative progress이며 현재 첫 미완료 gate는 same-law weighted
  correlation의 정의와 conditional expectation 분해다. actual 계산은 아직 도움이 되지 않는다.
- 문제·결정: global joint route를 가장 약한 충분조건으로 먼저 감사하고, 모든 fiber uniform
  route는 source가 그 강도를 실제로 지원할 때만 사용한다.
  source locator 확인 중 좁은 경로 대신 `rg --files tmp article`을 사용해 접근권한이 없는
  다수의 `tmp/tmp*` 디렉터리에서 OS error 5가 발생했다. 읽기 전용 실패라 파일·과학 판정
  영향은 없으나 직전 E129 예방규칙의 즉시 재발이므로 오류 원장에 추가하고, 이후에는
  정본이 이미 가리키는 exact PDF·text locator만 직접 읽는다.
- 다음 재개점: Theory 77--79와 FMT/Maier source에서 weighted coefficient,
  prime-error vector, outer/inner law, final CRT shift의 정확한 식을 한 표로 고정한다.

### 2026-09-14 23:02 KST — source locator·양화사 고정

- 수행: Theory 76--79의 character coefficient와 direct weighted-correlation target,
  FMT의 조건부기댓값 식 (1.1), Theorems 4--5, FGKMT Corollary 4, Maier Lemma 2와
  matrix argument, Sono Lemma 3.7 및 식 (3.14)--(3.22)를 native text와 원문 렌더로
  대조했다.
- source hash:
  - FMT 2015 PDF SHA-256
    <code>396E54A9699AD80E749B1607C0B5C26982329625615D8769DE1E23328F651828</code>;
  - FGKMT 2018 PDF SHA-256
    <code>C31229EF40C9646DFC99BDE7C059A9A0FD35E7BE71B5836DE9DF06C01D921AC8</code>;
  - Maier 1981 PDF SHA-256
    <code>CA6F2425B850DD5F9D81340D8A4A4C76FAF6A947D7486EBF87FF072ADBF0A3EB</code>;
  - Sono journal PDF SHA-256
    <code>A45F84F5FE99E16534773005287D4CA5538F58D86793184F4D28FAD1C9C67302</code>.
- 결과: 최종 outcome은 outer residue vector 하나가 아니라
  <code>(A,N')</code>이고, FMT의 tower identity는 그 law 안에서 기대값을 분해할 수 있게
  하지만 weighted moment 자체를 주지는 않는다. FMT/FGKMT의 fixed-subset cardinality
  preservation은 output-dependent CRT phase를 가진 signed/complex character observable에
  직접 적용되지 않는다. Maier·Sono는 반대로 fixed CRT shift마다 pointwise PAP를 투입한다.
- 정확한 계수: <code>P=P(x)/B0</code>이고 최종 survivor
  <code>T_omega={s in [y]\\[x]:(m_omega+s,P)=1}</code>이므로 Dirichlet character를
  nonunit에서 0으로 연장하면
  <code>C_chi(omega)=sum_{s in [y]\\[x]} conjugate(chi(m_omega+s))</code>가 exact하다.
  이는 survivor 목록을 별도로 random weight로 보는 것보다 CRT 의존성을 더 분명히 한다.
- 문제·오류 기록:
  1. 앞 단계의 broad <code>rg --files tmp article</code>는 E129의 좁은 경로 규칙을
     바로 위반해 접근거부를 재발시켰다. 이후 exact locator만 사용했다.
  2. read-only text 정리 명령에서 <code>$raw.Replace([char]0,'')</code>를 써 .NET overload
     binding 오류가 발생했다. 파일 변경은 없고 locator 결과는 얻었지만, NUL 제거는
     PowerShell <code>-replace "`0", ''</code> 또는 string overload만 사용한다.
- 검증: PDF page count/hash, native text locator, 관련 원문 page rendering을 서로 대조했다.
- 다음 재개점: normalized squared badness, global outer-good moment, conditional-on-good 및
  uniform-fiber 충분조건을 divide-by-zero 없이 exact finite law로 정식화한다.

### 2026-09-14 KST (세부 시각 미확정) — finite contract·source screen·표적 검증

- 수행: actual outcome \(\omega=(A,N')\)에서
  \(R_\omega=\sum_{\chi\ne\chi_0}C_\chi(\omega)Z_\chi(Y)\)와 outer-good domain의
  normalized squared badness \(W_\omega\)를 정의했다. global,
  conditional-on-outer-good, uniform-fiber의 세 충분조건과 raw moment를 쓰는 경우의
  pointwise survivor floor를 분리했다.
- 핵심 gate:
  - global: \(\mu/\tau^2<(1-F_{\rm out})(1-F_{\rm in})\);
  - conditional/fiber: \(F_{\rm in}+\mu_O/\tau^2<1\);
  - raw moment: \(\mu\le\rho/(M_{\min}^2Y^2)\), \(M_{\min}>0\) pointwise.
- source screen: FMT formula (1.1)는 tower만 주고, FMT Theorem 4와 FGKMT
  Corollary 4는 inner output 전에 고정된 subset의 nonnegative cardinality를 보존한다.
  output-dependent CRT complex phase에는 바로 적용되지 않는다. Maier·Sono는 fixed residue
  pointwise PAP route다. targeted hypergraph/character-moment 검색에서도 numerical
  drop-in은 식별하지 못했으나 이는 문헌 전수 부재 증명이 아니다.
- 파일:
  - <code>source/dep_r09_same_law_weighted_correlation.py</code>
  - <code>tests/test_dep_r09_same_law_weighted_correlation.py</code>
  - <code>docs/method/theory/data/Sono_FMT_DEPR09_same_law_weighted_correlation_v1.json</code>
  - Theory 80·review 88 초안
  - 단일 Lean 정본의 Theory 80 선언 5개
- 검증:
  - <code>py_compile</code> PASS;
  - 표적 unittest 9/9 PASS;
  - formula inventory preflight: 81개 theory, 1,473식, parse issue 0;
  - Lean direct compile 재실행 exit 0. 첫 실행은 30초 경계에서 outer tool이 session ID를
    출력하지 않아 종료코드를 보존하지 못했고, 프로세스가 남지 않았음을 확인한 뒤
    session ID를 명시 출력하여 다시 검사했다.
- 문제·교정:
  1. 첫 Lean direct compile의 결과 객체에서 <code>session_id</code>를 출력하지 않은
     orchestration 오류가 있었다. 앞으로 async 가능 명령은 처음부터 반환 객체 전체 또는
     session ID를 출력하고 최종 poll의 exit code만 판정한다.
  2. conditional terminal의 <code>hTau</code>는 analytic domain 보존용이지만 대수 proof에서
     직접 쓰이지 않아 linter가 경고했다. source-domain interface를 보존한다는 주석 아래
     <code>_hTau</code>로 바꿨다.
  3. 새 Markdown을 raw string이 아닌 JavaScript patch string으로 넣어 inline
     <code>\(...\)</code>의 backslash와 한 <code>\left</code>가 소실됐다. display inventory가
     식 (80.20)의 손상을 보여 즉시 raw <code>String.raw</code> patch로 복원했다.
  4. 정본 탐색 중 존재하지 않는 root <code>METHODS.md</code>와 README 후보를 한 번에
     <code>rg</code>에 넘겨 file-not-found 진단을 만들었다. 실제 정본은
     <code>docs/METHODS.md</code>이며 이후 <code>rg --files docs</code>로 고정했다.
- 다음 재개점: Theory 80 formula-status mapping을 추가하고 direct compile, inventory,
  full Lean build, 전체 Python 회귀를 순서대로 확정한다.

### 2026-09-14 23:25 KST — 정본 동기화·전수 검증·handoff

- 수행: Theory 80, review 88, machine ledger, exact helper·tests, 단일 Lean 정본,
  formula-status inventory, T1 의무 원장, 방법론·색인·종합 review, AGENTS와 오류 원장을
  동기화하고 새 handoff를 작성했다.
- 검증:
  - 표적 exact unittest 9/9 PASS;
  - 완료 문서 변경 뒤 표적 회귀 21/21 PASS, exit code 0;
  - 전체 unittest 정상 로컬 권한 880/880 PASS, 86.995초, exit code 0;
  - 제한 샌드박스의 82개 PermissionError는 E134로 분리했고 PASS로 사용하지 않음;
  - canonical Lean direct compile exit code 0;
  - lake build 8,765 jobs, exit code 0;
  - integrated validator: 81 theory, 1,473식, Lean declaration 288,
    local link 1,557, banned proof escape 0, text issue 0, exit code 0;
  - 별도 text-integrity: 595파일, 6,392,874 bytes, issue 0, exit code 0;
  - JSON 3개 parse PASS, git diff whitespace error 0;
  - printable damage token과 미래 시각 narrow scan PASS.
- 결과: finite tower와 세 moment sufficient contract는 exact하다. actual same-law
  analytic moment source는 OPEN이고 새로운 bounded \(X_{\rm cert}\) 범위는 없다.
- 문제·교정:
  - source/path·patch transport·미래 시각·sandbox test·잘못된 NUL rg 호출을
    E129--E136에 남기고 모두 commit 전에 교정했다.
  - 원장 초안의 Theory 80 Lean 선언 수가 4개로 적혀 있었으나 실제 canonical source는
    tower, global, conditional, denominator identity, raw normalization의 5개다.
    전수 declaration 288은 generator가 계산한 값이며 원장 숫자를 5개로 교정했다.
- handoff:
  <code>handoff/202609142320_HANDOFF.md</code>.
- 다음 재개점: 한국어 로컬 commit 뒤 handoff의 우선순위에 따라 actual FMT filtration
  민감도와 Theory 55 survivor denominator floor를 source-first로 감사한다.

## 현재 재개점

handoff의 우선순위에 따라 actual FMT filtration 민감도와 Theory 55 survivor
denominator floor를 source-first로 감사한다. push·PR은 수행하지 않는다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 source theorem 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] <code>git diff --check</code>와 참조 경로 확인
- [x] 파일명을 <code>-done.md</code>로 변경
