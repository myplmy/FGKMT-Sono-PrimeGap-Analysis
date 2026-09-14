# DEP-R09 FMT construction-law finite mass 감사 작업원장

- 시작: 2026-09-14 21:37 KST
- 현재 상태: COMPLETE
- 사용자 승인: \(X_{\rm cert}\)를 좁히는 source-first 정규화·증명 연구, 필요한 Lean 형식화,
  로컬 정적·단위·전수 검증, 정본 문서·handoff 갱신, 로컬 staging·commit
- 금지·보류: actual prime sweep, threshold calculator, 장시간 계산, 외부 게시·연락,
  push/PR, <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>
- 선행 변경: 시작 시 branch <code>main...origin/main [ahead 32]</code>,
  <code>git status --short</code>는 빈 결과. 이번 작업 이전 비소유 변경 없음

## 목적과 완료조건

- 목적: Theory 78의 FMT randomized residue-vector family를 실제 source probability law로
  되돌려, sieve-good event의 finite positive mass를 수치화할 수 있는지와 direct
  weighted-correlation event를 같은 law에 결합할 수 있는지를 판정한다.
- 완료조건:
  1. Ford--Maynard--Tao의 construction probability space와 Sections 4--6의 모든
     Markov·concentration·hypergraph selection 소비를 source/page/equation 단위로 고정한다.
  2. 각 good event가 높은 확률, 양의 확률, 조건부 존재 중 무엇인지 구분하고 숨은
     \(o(1)\), implied constant, cutoff를 원장화한다.
  3. union-selection에 필요한 합계 failure mass \(<1\)을 source에서 얻을 수 있는지
     exact하게 판정한다.
  4. source가 충분하지 않으면 필요한 최소 새 quantitative lemma와 입력을 분해하고,
     analytic theorem을 Lean 공리로 넣지 않는다.
  5. dependency-critical 유한 확률 대수는 exact Python/Lean으로 검증한다.
  6. Theory·review·기계 원장·색인·METHODS/AGENTS·Lean 전수원장·handoff를 동기화한다.
  7. 새 bounded \(X_{\rm cert}\) 범위가 생기면 즉시 중단·보고한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | \(G,F,H\)는 변경하지 않고 DEP-R09의 construction-law 확률 양화사만 정밀화 |
| end-bounded 의미론 | 영향 없음 | maximal-gap dataset과 interval 정의를 읽거나 변경하지 않음 |
| 데이터·provenance | 영향 있음 | FMT 1차 source의 version·page·equation·hash/read mode를 고정 |
| 통계·정밀도 | 영향 있음 | asymptotic probability를 finite probability로 자동 승격하지 않고 exact rational budget만 인증 |
| 승인 경계 | 영향 있음 | 큰 계산·threshold calculator 없이 문헌·작은 검산만 수행 |
| 재현성 | 영향 있음 | machine ledger·tests·Lean status를 source theorem과 분리 |
| 문서 | 영향 있음 | Theory 79와 새 review를 만들고 Theory 78 successor 및 정본을 동기화 |

## 접근 비교와 권장안

| 접근 | 정확성 | 비용 | 위험 | 판정 |
|---|---|---|---|---|
| FMT의 최종 존재결론만 재사용 | 낮음 | 낮음 | failure mass와 같은-law 결합을 잃음 | 기각 |
| proof 내부 probability law와 모든 bad event를 finite하게 추적 | 높음 | 중간~높음 | 다수의 \(o(1)\), hypergraph 상수 복원이 필요 | 1차 권장 |
| 모든 vector에 uniform weighted-correlation 정리 탐색 | 높음 | 높음 | 지나치게 강하거나 source 부재 가능 | 2차 병행 screen |
| 새로운 joint-moment 정리를 직접 증명 | 잠재적으로 높음 | 매우 높음 | 수개월 이상·성공 불확실 | source 경로 실패 뒤에만 |

## 단계 현황

1. **DONE — authoritative FMT source·version·probability law inventory**
2. **DONE — Sections 4--6 event/failure-budget source audit**
3. **DONE — finite positive-mass sufficient condition과 blocker 분해**
4. **DONE — exact helper·tests·필요 Lean critical algebra**
5. **DONE — Theory 79·review·기계 원장·정본 동기화**
6. **DONE — 전수 검증·handoff·완료 이름 변경**

## 단계별 기록

### 2026-09-14 21:37 KST — 재개·영향도 분석

- 수행: 최신 handoff, Theory 78 재개점, git clean 상태, 작업원장 규약과 승인 경계를 확인했다.
- 파일: 이 작업원장.
- 명령·검증: <code>git status --short --branch</code>, 최신 handoff 읽기,
  비완료 작업원장 검색.
- 결과: 이전 턴은 Theory 78과 commit <code>aaf300c</code>로 authoritative progress.
  미완료 원장과 비소유 변경은 없다.
- 문제·결정: 작업원장 지침의 실제 정본은
  <code>ai_dev_tool/08_작업원장_작성규약_양식.md</code>인데 존재하지 않는
  <code>03_작업원장_작성지침.md</code>를 먼저 조회해 read-only path error가 한 번 발생했다.
  저장소 변경은 없었고 실제 파일을 즉시 확인했다.
- 다음 재개점: 로컬·공개 FMT 1차 source의 정확한 version과 Sections 4--6의
  probability-space 정의를 고정한다.

### 2026-09-14 22:00 KST — 재개 시 검색 오류와 source 정본 확인

- 수행: 비완료 원장과 최신 handoff를 재대조하고, FMT 로컬 PDF 두 판본 및 기존 native-text
  추출본의 존재·hash·page 수를 확인했다.
- 파일: 이 작업원장(기록만 갱신).
- 명령·검증: <code>git status --short</code>, <code>Get-FileHash -Algorithm SHA256</code>,
  <code>pdfinfo</code>, exact-path <code>Get-Content</code>.
- 결과: 기존 정본 PDF
  <code>tmp/FMT_Chains_of_large_gaps_between_primes.pdf</code>는 16쪽,
  SHA-256 <code>396e54a9699ad80e749b1607c0b5c26982329625615d8769de1e23328f651828</code>이고,
  대조용 PDF
  <code>tmp/pdfs/h1c1b1/Ford_Maynard_Tao2018_Chains_of_large_gaps.pdf</code>도
  16쪽이며 SHA-256은
  <code>4c5709180f4b427eac3525411618534a6d5ab03c1a79d3faeee3318d2ad7ecce</code>다.
  기존 <code>tmp/pdfs/t1/fmt_pages.txt</code>는 962행 native-text 추출본이다.
- 문제·결정: Windows <code>rg</code>에
  <code>docs/method/theory/53_*</code> 같은 경로 와일드카드를 직접 넘겨 OS error 123이
  발생했다. 이는 오류 원장 E095/E100/E107/E127에서 이미 금지한 탐색 패턴의 재발이며,
  읽기 전용 실패라 파일·연구 결과 영향은 없다. 실패 출력은 증거에서 제외하고
  <code>rg --files</code>로 exact path를 얻은 뒤 재조회했다. 마감 때 오류 원장에
  이 재발을 추가한다.
- 다음 재개점: 두 PDF의 native text를 구조적으로 비교하고, 최신 공개·출판 source에서
  Theorems 3--6의 random law·conditioning·failure statement를 page/equation별로 고정한다.

### 2026-09-14 KST (세부 시각 미확정) — FMT source law와 project finite mass 분리

- 수행: native-text를 원문 PDF와 대조해 Theorems 3--5, formulas (5.1)--(5.8),
  Section 6 formulas (6.11), (6.14)--(6.23)의 확률공간·조건부 선택·failure 진술을
  추출했다. Theory 53·55의 finite outer/inner bound와 결합했다.
- 파일: source 원문은 읽기 전용; 이 작업원장.
- 결과:
  1. 출판 FMT는 first-stage \(\mathbf A\)와 그 값에 조건부인 second-stage
     \(\mathbf N'\)의 순차 law를 사용한다. final residue/CRT outcome은
     \(\mathbf A\) 하나가 아니라 \((\mathbf A,\mathbf N')\)에 의존한다.
  2. 출판 원문 자체의 성공확률은 \(1-o(1)\)이며 numerical rate가 없다.
  3. project Theory 55는 \(F_{\rm out}\)과 모든 outer-good
     \(\mathbf A\)에서의 uniform conditional \(F_{\rm in}\)을 이미 유한식으로 준다.
     따라서 같은 joint law에서 sieve-good mass는
     \((1-F_{\rm out})(1-F_{\rm in})\) 이상이다. independence는 필요 없다.
  4. weighted-correlation failure를 같은 joint law에서 \(F_{\rm corr}\) 이하로
     상계하면 \(F_{\rm corr}<(1-F_{\rm out})(1-F_{\rm in})\)이 simultaneous
     selection의 충분조건이다. 이 analytic input은 아직 OPEN이다.
- 판정: sieve-good positive mass 자체는 새 hard blocker가 아니다.
  Theory 78의 \(\omega=\mathbf A\) 표기는 joint/sequential pair로 교정해야 한다.
  numerical \(X_{\rm cert}\) 범위는 생기지 않았다.
- 다음 재개점: exact helper·machine ledger·tests와 dependency-critical Lean
  probability/cardinality algebra를 추가한다.

### 2026-09-14 KST (세부 시각 미확정) — exact helper·machine ledger 표적 검증

- 수행: exact rational two-stage mass, same-law union, fiberwise gate와 Markov
  failure helper를 구현하고 provenance/status machine ledger와 fail-closed tests를 만들었다.
- 파일:
  <code>source/dep_r09_fmt_construction_mass.py</code>,
  <code>tests/test_dep_r09_fmt_construction_mass.py</code>,
  <code>docs/method/theory/data/Sono_FMT_DEPR09_FMT_construction_mass_v1.json</code>.
- 검증: 고정 FGKMT Python으로 <code>py_compile</code>과 표적 unittest 9개를 실행해
  9/9 PASS했다.
- 경계: 이는 확률 대수와 source hash를 검증한 것이며 weighted-correlation 상계,
  FMT의 모든 \(o(1)\) rate, PAP, fixed coefficient 또는 \(X_{\rm cert}\)를
  검증한 것이 아니다.
- 다음 재개점: Theory 79·review를 작성하고 새 식 중 finite logic을 Lean으로 형식화한다.

### 2026-09-14 KST (세부 시각 미확정) — Theory 79·review·Lean 초안과 오류 재발 감사

- 수행: Theory 79와 review 87을 작성하고 exact probability algebra와 finite
  outer/fiber selection을 canonical 단일 Lean 파일에 추가했다.
- 파일:
  <code>docs/method/theory/79_Sono_FMT_DEPR09_FMT_construction_law_finite_mass_audit.md</code>,
  <code>docs/review/87_20260914_DEPR09_FMT_construction_law_finite_mass_타당성검토.md</code>,
  <code>lean/FGKMTSono/TheoryVerification.lean</code>,
  <code>ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md</code>.
- 첫 direct compile:
  <code>Finset.card_union_le</code> implicit finset argument 오류 3건을 검출했다.
  새 Theory 79 한 곳과 직전 commit의 Theory 78 두 곳이다. 집합 인수를 명시한 뒤
  같은 canonical direct compile을 끝까지 poll해 exit code 0을 확인했다.
- 증거 이상: 직전 handoff의 Theory 78 direct compile PASS 기록과 현재 source의 첫
  compile 결과가 모순된다. 과거 실행의 저장 로그가 없어 원인은 확정하지 않았으며,
  session id를 최종 exit code로 오인했을 가능성을 E130에 추론으로 기록했다.
- 별도 재발:
  1. read-only 경로 추정과 Windows path wildcard 오류를 E129에 기록했다.
  2. multi-file raw patch에서 Markdown 역따옴표 충돌 E128을 다시 일으켰다.
     이 단계에서 같은 원인으로 총 2회 parser 전에 실패했으며 파일 영향은 없었다.
     placeholder 방식의 작은 hunk로 전환했다.
- 경계: Lean은 실수대수·finite selection만 검증한다. FMT analytic probability,
  weighted correlation과 numerical \(X_{\rm cert}\)는 인증하지 않는다.
- 다음 재개점: 정본 색인·상태문서와 Lean inventory를 동기화하고 전수 검증한다.

### 2026-09-14 KST (세부 시각 미확정) — 정본·전수원장 1차 동기화

- 수행: Theory 78 successor, theory/review 색인, T1 원장, METHODS, AGENTS, 종합리뷰,
  Lean 상태 안내를 Theory 79 판정으로 동기화하고 inventory를 재생성했다.
- 결과: integrated validator는 theory 80개, display 1,452식, Lean declaration 283개,
  <code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=60</code>,
  <code>NOT_YET_FORMALIZED=1027</code>, 금지 proof escape 0건, local link 1,535개,
  text-integrity 242파일 issue 0으로 PASS했다.
- 문제·교정: 별도 text-integrity helper에 존재하지 않는 <code>--repo-root</code>를
  넘겨 exit 2가 한 번 발생했다. 도움말·parser를 확인한 뒤 positional path로 재실행해
  596파일·7,621,445 bytes, issue 0, exit 0을 확인했고 오류 원장 E131에 기록했다.
- 경계: 원장 수치는 형식화 coverage이며 analytic completion percentage가 아니다.
  1,027개 미형식화 수식을 root blocker보다 먼저 전부 처리하지 않는다.
- 다음 재개점: lake build, 표적·전체 Python suite, diff/link/text gate를 최종 실행한다.

### 2026-09-14 22:25 KST — 최종 검증과 오류 증거 강화

- 수행: 오류 원장 E117의 동일 사건과 E118·E119·E121의 넓은 재발 패턴을 대조하고,
  AGENTS와 Lean README에 곱 결합형 preflight 및 비동기 종료코드 규칙을 고정했다.
  E129에는 추정 unittest 모듈명 오류를, E130에는 Theory 78 과거 PASS 기록 모순을,
  E132에는 이 원장의 미래 시각 기록 교정을 추가했다.
- 검증:
  1. inventory 재생성: theory 80개, display formula 1,452개.
  2. integrated validator: declaration 283개, local link 1,535개,
     `KERNEL_PASS=94`, `CONDITIONAL_KERNEL_PASS=60`,
     `NOT_YET_FORMALIZED=1027`, 금지 proof escape 0건, text issue 0, exit 0.
  3. 표적 unittest: 정확한 5개 모듈 46/46 PASS, exit 0.
  4. 전체 unittest discovery: 871/871 PASS, 78.965초, exit 0.
  5. 별도 text-integrity: 592파일·7,550,289 bytes, issue 0, exit 0.
  6. canonical direct Lean compile: async session을 최종 poll해 exit 0.
  7. `lake build`: 8,765 jobs, exit 0.
  8. `git diff --check`: whitespace error 0; line-ending 안내만 존재.
- 경계: 위 PASS는 finite bookkeeping·코드·원장·Lean dependency-critical logic의
  일치만 뜻한다. same-law weighted correlation, FMT analytic rate, PAP-11, DEP-R09,
  fixed coefficient와 numerical `X_cert`는 OPEN이고 실제 prime 계산은 수행하지 않았다.
- 다음 재개점: 식 (79.8)의 weighted badness를 joint `(A,N-prime)` law에 정의하고
  outer/inner conditional expectation 또는 fiberwise correlation source를 감사한다.

## 현재 재개점

현재 batch의 필수 작업은 완료됐다. 다음 batch는 Theory 79 식 (79.8)의 same-law
weighted-correlation expectation 분해와 source screen에서 시작한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 source theorem 상태 분리
- [x] 결과 색인·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] <code>git diff --check</code>와 참조 경로 확인
- [x] 파일명을 <code>-done.md</code>로 변경
