# DEP-R09 modern explicit near-one zero-density source screening 작업원장

- 시작: 2026-09-14 02:44 KST
- 작업 루트: Z:\FGKMT-Sono-PrimeGap-Analysis
- 선행 정본:
  - docs/method/theory/73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md
  - docs/review/80_20260914_DEPR09_CJ_loss_tree_구조감사_타당성검토.md
  - handoff/202609140238_HANDOFF.md
- 시작 commit: e5059f57c03028522e1bb0ef22d00bd9a647498c
- 승인 경계: primary-source 조사·필요 자료 취득, 정적 수학감사, 고정밀 진단,
  데이터 비의존 시험과 Lean 검증은 승인됨. 장시간 actual prime 계산은 시작하지 않는다.

## 목표

Theory 73에서 확인한 \(d\le186\) PAP coefficient 병목을 줄일 수 있는 현대적
explicit near-one zero-density theorem 또는 구조적으로 다른 proof package를
primary source에서 선별한다. 이름이나 형태가 비슷하다는 이유로 drop-in으로 간주하지
않고, 실제 primitive character family·modulus/height 범위·exceptional zero 처리·
수치 multiplier·finite cutoff를 현재 PAP 변수에 대입해 판정한다.

## 완료조건

1. 기존 Theory 58--73과 source registry를 대조해 중복 조사를 제거한다.
2. peer-reviewed 또는 명확한 공식 원문 후보를 source statement/page/equation 단위로 등록한다.
3. 각 후보에 대해 \(Q=X^{1/d}\), \(T=Q^5\), \(q\le Q\),
   \(1-\alpha\asymp1/\log X\), \(d\le186\) 적합성을 판정한다.
4. multiplier가 숫자로 닫힌 후보는 Theory 72 near integral에 대입해
   \(e^{-2}\) budget 통과 가능성을 먼저 계산한다.
5. 숨은 \(O,\ll,o(1)\), 비명시적 cutoff 또는 family mismatch가 있으면 FAIL/HOLD로 기록한다.
6. dependency-critical 유한 대수가 생기면 Python fail-closed test와 Lean 단일 파일에
   형식화하되 외부 analytic theorem을 local axiom으로 넣지 않는다.
7. theory/review/machine ledger/METHODS/T1/색인/AGENTS/Lean 원장/handoff를 정합하게 갱신한다.
8. numerical \(X_{\rm cert}\)의 특정 범위를 정당하게 좁힐 수 있게 되거나 장시간 연산·
   설치·접근 불가 원문이 필요해지면 즉시 중단하고 사용자에게 보고한다.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | end-bounded empirical \(G(x)\)가 아니라 analytic PAP branch만 다룬다. |
| source provenance | 영향 큼 | primary source, version, publication status, page/equation, URL/hash를 고정한다. |
| 수치 정밀도 | 영향 있음 | exact rational 우선, 초월값은 FGKMT mpmath 고정밀 진단과 certificate를 구분한다. |
| Lean | 조건부 영향 | 유한 대수만 단일 파일에 추가하며 source theorem은 미형식화 상태로 보존한다. |
| 실제 데이터·그래프 | 영향 없음 | maximal-gap dataset, test_result와 figure를 생성하지 않는다. |
| 승인·자원 | 영향 있음 | 장시간 계산·새 package가 필요하면 실행하지 않고 사용자 요청으로 전환한다. |
| 정본·재현성 | 영향 있음 | successor 문서·machine ledger·source hash와 회귀시험을 추가한다. |

## 단계 현황

1. **DONE — 기존 후보·실패 이유와 screening 조건 inventory**
2. **DONE — primary-source 최신 후보 탐색·원문 statement 확인**
3. **DONE — PAP 변수 대입과 coefficient/exponent feasibility 계산**
4. **DONE — 구조 판정·Python/Lean 검증**
5. **DONE — successor theory/review와 정본 동기화**
6. **DONE — 전체 검증·handoff·완료 이름·로컬 커밋 준비**

## 단계별 기록

### 2026-09-14 02:44 KST — 착수

- 확인: 시작 작업트리는 clean이고 비완료 work ledger는 없다.
- 확인: 직전 Theory 73은 local coefficient polishing을 끝냈지만
  \(d=186\) budget보다 약 \(4.623\times10^{11}\)배 크다.
- 결정: 먼저 기존 Theory 58--73과 이미 확보한 Thorner--Zaman,
  Bennett et al., Benli et al., Ramaré 자료를 재분류한 뒤 새 검색을 한다.
- 비실행: actual prime sweep, threshold calculator, package 설치를 시작하지 않았다.
- 도구 오류: 첫 Add File patch는 Markdown backtick이 JavaScript template literal을
  조기에 닫아 parser 단계에서 거부됐다. 파일은 생성되지 않았고 backtick 없는 patch로
  즉시 재실행했다.
- 다음 재개점: review 65--80과 machine source registry에서 후보별 정확한 실패 원인을
  표로 추출한다.

### 2026-09-14 03:06 KST — source screen과 finite arithmetic 완료

- 기존 source baseline: 사용자가 추가한 Gallagher 1970, Maier 1981, McCurley 1984
  원문은 이미 Theory 57·65·72와 source registry에서 hash·page 단위로 감사되었음을 확인했다.
- 새 published 후보: Ramaré 2016, Thorner--Zaman 2024 두 갈래,
  Kaneko--Thorner 2025, Friedlander--Iwaniec 2023, Thorner--Zhang 2026을 비교했다.
- 미검증/비공개 후보: Chen--Gupta--Li arXiv v2는 `(qT)^o(1)` 때문에 수치 인증으로
  승격하지 않았고, Bellotti--Castillo의 Dirichlet log-free 원고는 공개 정리 부재로
  watchlist에만 두었다. 공식 연구페이지·CV에서 공동저자를 Cruz Castillo로 교정했다.
- PDF 판독: 새로 확보한 네 PDF 모두 native text를 먼저 사용했고 OCR은 쓰지 않았다.
  exact statement 페이지를 렌더해 수식과 대조했다. Poppler가 Symbol display-font 경고를
  냈지만 PNG와 수식은 온전했다.
- Ramaré direct insertion: `d=186`, `c1=1/24`, `T=Q^5`에서 exact margin은
  `83/93`, additive exponent는 `1/93`, zero-free edge mass는 `31/20`이다.
  source 최소 `log X=186 log 10`에서도 direct upper-certificate의 한 unit slice 하한이
  main 약 8602, additive 약 64912로 `exp(-2)` budget을 크게 넘는다.
- 경계: 이는 실제 오차의 하한이나 모든 hybrid/cancellation proof의 불가능성 정리가 아니다.
  현재 theorem RHS를 비음수로 그대로 적분하는 certificate가 통과하지 못한다는 뜻이다.
- 구현: `source/dep_r09_modern_density_screen.py`, machine ledger, fail-closed unittest를 추가했다.
- 도구 오류: Windows PowerShell의 `foreach` 결과를 직접 pipe한 scratch 명령은 parser에서
  실패했다. `$rows`에 먼저 저장해 재실행했고 파일 변경은 없었다. 넓은 wildcard 경로를
  `rg`에 넘긴 한 scratch 조회도 Windows 경로 문법으로 실패했으며 명시 경로로 교정했다.
- 다음 재개점: 신규 unittest를 통과시킨 뒤 Theory 74/review 81과 Lean 유한 대수를 작성한다.

### 2026-09-14 03:18 KST — successor 정본·Lean 동기화

- 신규 Theory 74와 쉬운 review 81을 작성하고, 문헌 전체 불가능성이 아니라 식별 후보
  집합의 drop-in 실패라는 scope를 명시했다.
- METHODS, T1 proof-obligation ledger, theory/review 종합 색인, AGENTS와 Lean README를
  successor 판정으로 동기화했다.
- Lean 단일 파일에 d=186 exact exponent 세 값, Thorner--Zaman/Friedlander--Iwaniec
  integer capacity, FI exponent·coefficient 산술을 추가했다. direct compile exit 0을 확인했다.
- 외부 analytic source theorem은 local axiom으로 넣지 않았다. `sorry`, `admit`,
  project-local `axiom`은 0건이다.
- 표적 Python unittest 8/8와 py_compile이 PASS했다.
- Lean inventory generator·validator 중간 실행은 75문서·1,362식·267선언,
  금지 proof escape 0건으로 PASS했다. 최종 diff 뒤 다시 실행한다.
- self-audit에서 Bellotti 공동저자, Maier·McCurley 서지 초안 오류와 도구 호출 오류를
  발견·교정해 오류 원장 E122에 기록했다. 과학 판정과 사용자 데이터에는 영향이 없다.
- 다음 재개점: 전체 unittest, full Lake build, 링크·UTF-8·수식 delimiter·source hash와
  cached diff를 검증한 뒤 handoff를 작성한다.

### 2026-09-14 03:23 KST — 최종 회귀·형식검증 완료

- 전체 unittest의 첫 sandbox 실행은 Windows 임시 디렉터리 접근 거부만으로
  `823 tests / 82 errors`였다. 코드 실패와 분리하기 위해 사용자가 허가한 일반 권한으로
  같은 명령을 재실행했고 `823/823 OK`를 확인했다.
- 신규 모듈 py_compile과 표적 unittest `8/8`가 PASS했고, 진단기는 actual 계산을 하지
  않았으며 모든 root claim을 false/OPEN으로 보존했다.
- Lean inventory generator·validator 최종 실행은 75문서·1,362식·267선언·로컬 링크
  1,440개·금지 proof escape 0건으로 PASS했다.
- `lake env lean FGKMTSono/TheoryVerification.lean` exit 0과 `lake build`
  `8765 jobs` 성공을 확인했다.
- 세 고전 PDF와 네 신규 audit PDF의 SHA-256을 재계산해 등록값과 일치시켰다.
  신규 텍스트 파일의 control character는 0건이고 Theory 74 display delimiter는
  18쌍으로 일치하며, JSON 3개 parse와 `git diff --check`가 PASS했다.
- 최종 scientific 상태: 식별한 modern 후보 중 numerical drop-in 0개,
  `PAP-11`, `DEP-R09`, fixed `2e-17`, numerical `X_cert`는 모두 OPEN이다.
- 사용자 자원·설치·장시간 계산 요청은 없다.
- 다음 재개점: 새 public numerical source가 나오면 동일 gate를 재사용하거나,
  별도 승인 아래 smoothing·hybrid minimum·cancellation-preserving transfer의 작은
  coefficient feasibility 감사를 시작한다.

## 완료 전 점검

- [x] primary source·version·page/equation provenance
- [x] actual PAP family와 변수변환
- [x] coefficient gate의 exact/high-precision 판정
- [x] 숨은 상수·finite cutoff·exceptional branch 분리
- [x] source theorem과 Lean 대수의 증거 경계
- [x] 사용자 자원·설치 필요 여부
- [x] canonical 문서·원장·handoff 동기화
- [x] 전체 회귀·Lean·링크·UTF-8·diff 검증
- [x] 완료 이름 변경과 승인된 local commit 준비
