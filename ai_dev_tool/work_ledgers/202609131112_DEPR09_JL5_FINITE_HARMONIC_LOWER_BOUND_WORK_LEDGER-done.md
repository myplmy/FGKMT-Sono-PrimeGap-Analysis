# DEP-R09 JL5 finite harmonic lower bound 작업원장

- 시작: 2026-09-13 11:12 KST
- 현재 상태: COMPLETE
- 직전 commit: `59eae05f544b8d56fab2e2f14c159c297840ca06`
- 사용자 승인: `X_cert` 계산기 이전의 source-first 정규화·증명, 필요한 Lean 형식화,
  문서·시험·handoff와 로컬 stage/commit
- 금지·보류: actual prime sweep, threshold calculator, 숨은 상수 임의 선택,
  장시간 연산, 새 package 설치, 외부 source theorem의 local axiom화
- 선행 변경: 시작 worktree clean; 이번 작업 비소유 변경 없음

## 목적과 완료조건

- 목적: Jutila 1977 Lemma 5의 squarefree·coprime harmonic sum을 actual proof call에
  사용할 수 있는 uniform finite lower bound로 바꿀 수 있는지 source-first로 판정한다.
- 완료조건:
  1. Jutila 명제·proof·quantifier와 downstream JL6 사용량을 원페이지 대조한다.
  2. 적합한 explicit 선행정리를 우선 조사하고 조건·상수·cutoff를 actual q,R 범위에 대입한다.
  3. drop-in source가 없으면 직접 초등 proof를 구성하되 모든 remainder와 q-dependence를 보존한다.
  4. theorem 전체, actual application, 조건부 algebra를 분리해 machine ledger와 test로 고정한다.
  5. dependency-critical finite algebra만 Lean으로 형식화하고 analytic source를 axiom화하지 않는다.
  6. PAP-11, DEP-R09, fixed `2e-17`, `X_cert`를 근거 없이 승격하지 않는다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | empirical code·dataset·result를 변경하지 않는다. |
| JL5/JL6 proof DAG | 직접 영향 | JL5 lower bound와 JL6 전체 detector를 별도 상태로 둔다. |
| fixed `2e-17`·`X_cert` | 간접 핵심 영향 | JL5 하나가 닫혀도 root certificate를 닫지 않는다. |
| q-uniformity | 핵심 위험 | 고정 q asymptotic을 uniform q theorem처럼 사용하지 않는다. |
| provenance | 핵심 영향 | PDF text/OCR 판정, page, equation, version, hash를 기록한다. |
| Lean | 조건부 영향 | finite sum/algebra만 우선; source analytic theorem은 미형식화 상태를 유지한다. |
| 사용자 계산자원 | 현재 불필요 | 30분 이상 연산 또는 새 dependency가 필요하면 요청하고 중단한다. |

## 접근 비교와 선택

| 접근 | 정확성·장점 | 위험·비용 | 이번 순서 |
|---|---|---|---|
| A. 기존 explicit uniform theorem | peer-reviewed statement를 그대로 쓸 가능성 | actual squarefree·coprime·harmonic 조건이 다를 수 있음 | 1순위 |
| B. Jutila 생성함수 proof 정량화 | 원래 구조와 가장 가까움 | hidden contour/remainder가 남을 수 있음 | 2순위 |
| C. 초등 convolution·partial summation 하한 | 모든 상수를 직접 통제 | 매우 거친 q-factor로 actual range를 못 통과할 수 있음 | A/B 실패 시 |

## 단계 현황

1. **COMPLETE — Jutila Lemma 5 statement·proof·JL6 actual use 원페이지 고정**
2. **COMPLETE — explicit 선행연구·보정·대체정리 source 조사**
3. **COMPLETE — actual q,R uniform finite lower bound 도출**
4. **COMPLETE — Theory/review/JSON/test·필요한 Lean 형식화**
5. **COMPLETE — 정본 동기화·전체 검증·handoff·로컬 commit 준비**

## 단계별 기록

### 2026-09-13 11:12 KST — 시작

- 수행: 최신 handoff, Theory 60, machine ledger, project·PDF·handoff·commit 지침 재확인.
- 결과: 첫 미완료 node가 `JL5`; 직전 worktree clean과 commit을 확인했다.
- 다음 재개점: Jutila OCR의 Lemma 5 proof와 Lemma 6 호출 문맥을 정확한 인쇄 페이지로
  추출하고 렌더링 이미지와 대조한다.

### 2026-09-13 11:20 KST — 단계 1 완료

- 수행: OCR이 필요한 Jutila 원문의 인쇄 pp. 49--51을 OCR text와 300 dpi 원페이지
  렌더링으로 대조했다.
- 확인: Lemma 5는
  `log R >= sqrt(log q)`에서 squarefree·`(r,q)=1` 조화합을
  `(6/pi^2) product_(p|q)(1+1/p)^(-1) log R {1+o(1)}`로 두며, proof는 생성함수
  `zeta(s)/zeta(2s) product_(p|q)(1+p^(-s))^(-1)`만 제시한다. 수치 remainder와
  cutoff, uniform quantifier는 인쇄되지 않았다.
- downstream: Lemma 6은 이 lower bound 외에도 Mellin integral과 truncation tail의
  두 `<<_epsilon 1`을 흡수한다. 따라서 JL5만 닫혀도 JL6 전체가 닫히지는 않는다.
- 검증: 원문 렌더에서 statement, 생성함수, Lemma 6의 조건과 proof 연결을 육안 대조했다.
- 작업 실수: `tmp` 전체에 광범위한 `rg`를 실행해 과거 임시 시험 디렉터리의 access-denied
  메시지가 다수 발생했다. 읽기 전용 실패라 파일·과학 결과 영향은 없으며, 이후 검색은
  해당 PDF 감사 폴더와 정본 경로로 제한한다. 최종 오류 원장에도 기록한다.
- 다음 재개점: 기존 Theory 22의 corrected Wirsing theorem이 JL5의
  `h(p)=1/p` 계열에 실제로 특수화되는지 조건을 대조하고, peer-reviewed explicit
  squarefree harmonic/coprime theorem을 표적 검색한다.

### 2026-09-13 11:44 KST — 단계 2·3 완료, 단계 4 진행

- source-first 결과: Sebastian Zuniga Alterman,
  *Explicit averages of square-free supported functions: to the edge of the
  convolution method*, Colloquium Mathematicum 168 (2022), 1--23,
  DOI 10.4064/cm8337-11-2020, arXiv 2003.05887v5의 Corollary 3.4(b)가
  Jutila JL5와 정확히 같은 합에 명시적 오차를 준다.
- source 고정: PDF 307,611 bytes,
  SHA-256 848a3a10b32f7639b584598bda98b4d9a092d4eacf87f68e9b1364e9f6880495.
  native text 98,661 bytes가 정상 추출돼 OCR은 쓰지 않았고, 인쇄 pp. 10--12와
  일반 개선경로 pp. 19--21을 렌더링 원페이지와 대조했다. 영구 보존본은
  article/Zuniga Alterman 2022 Explicit averages of square-free supported functions.pdf다.
- exact source:
  S_q(R)=c_q(log R+b_q)+E_q(R),
  |E_q(R)|<=2.554 B_q/R^(1/3),
  c_q=(6/pi^2) product_(p|q)(1+1/p)^(-1), b_q>0.
- finite transfer: 0<eta<=1,
  A=2.554 B_q/(eta c_q)와
  R0=max(exp(sqrt(log q)),e,A^3)를 두면
  S_q(R)>=(1-eta)c_q log R이다. factorwise
  p/(p+1)>=(p-1)/p이므로 JL6의
  (6/pi^2)phi(q)/q 주항에도 안전하게 전달된다.
- 판정: JL5=EXPLICIT_PEER_REVIEWED_SOURCE_REPLACEMENT_WITH_Q_DEPENDENT_CUTOFF.
  다만 JL6의 Mellin integral·truncation tail 두 숨은 상수는 별도라
  JL6/JL8/PAP-11/DEP-R09/fixed 2e-17/X_cert는 OPEN이다.
- fallback: Theory 22의 corrected Wirsing 특수화도 구조적으로 가능하지만
  안전 매개변수 a=2/3,A2=130의 log10(C_sum)=176.8190345505...라 primary로
  쓰지 않는다.
- 작성: Theory 61, review 68, machine JSON, evaluator와 8개 fail-closed test.
  표적 unittest 8/8 PASS.
- Lean: source theorem은 axiom화하지 않고 source premise 뒤의 lower transfer,
  error budget, finite Euler-product phi bridge, downstream coefficient transfer,
  2.554=1277/500만 단일 파일에서 형식화했다. direct Lean exit 0.
- inventory 중간검증: theory 62개, 1,078식, declaration 130개,
  KERNEL_PASS=34, CONDITIONAL_KERNEL_PASS=20,
  NOT_YET_FORMALIZED=971, banned proof escape 0, validator PASS.
- 교정된 탐색 오류: Theorem 4.6의 q-factor를 OCR에서 잠시 1로 읽었으나
  렌더링 원페이지에서 numerator를 확인해
  product_(p|q) sqrt(p)/(sqrt(p)-1)로 바로잡았다. 이 일반 경로는 primary 산출물에
  사용하지 않았다.
- 작업 도구 오류: 첫 review patch의 Markdown fence를 JavaScript template에서
  escaping하지 않아 parser가 실행 전에 거부했다. 파일은 생성되지 않았고 placeholder
  방식으로 재실행했다. Ford PDF hash도 실제 계산 전에 임시값을 JSON에 넣은 실수가
  있었으나 즉시 실제 SHA-256을 계산해 교정한 뒤 test를 수행했다.
- 다음 재개점: 오류 원장 E108, 정본 동기화 잔여를 완료한 뒤 full unittest·Lean build와
  strict UTF-8/local-link/diff 검증을 수행한다.

### 2026-09-13 11:52 KST — 단계 4 완료, 단계 5 검증 완료

- 정본 동기화: AGENTS, METHODS, theory index, literature synthesis, Theory 60과
  review 67의 successor note를 Theory 61·review 68 상태에 맞췄다.
- 오류 원장: 이번에 실제로 발생하고 commit 전 교정한 source 해석·hash/page count·patch
  wrapper·검색경로 문제를 E108에 기록했다.
- 표적 unittest: 9/9 PASS.
- 전체 unittest: 698/698 PASS, 61.982초. TemporaryDirectory·multiprocessing 규약에 따라
  기존 사용자 허가를 사용해 정상 로컬 권한에서 실행했다.
- Lean direct single file: exit 0.
- Lean full build: 8,765 jobs PASS.
- 전수 inventory validator: 62 theory 문서, 1,078식, declaration 130개,
  KERNEL_PASS 34, CONDITIONAL_KERNEL_PASS 20, DEFINITION_ONLY 8,
  PARTIAL_FORMALIZATION 10, SOURCE_THEOREM_UNFORMALIZED 30,
  NOT_YET_FORMALIZED 971, PARSE_REVIEW_REQUIRED 5, proof escape 0, PASS.
- strict UTF-8/control: 변경·신규 Markdown 12개 issue 0.
- local Markdown links: 변경·신규 대상 1,307개 PASS; Lean 정본 validator 1,143개 PASS.
- 저장소 전수 Markdown 추가 감사에서는 과거 이력 문서
  `handoff/202609021757_HANDOFF.md`의 byte offset 4,493에 vertical tab(ordinal 11) 1개를
  찾았다. 이번 변경이 아니며 이력 보존 원칙상 수정하지 않았다. 현재 산출물·수학 판정에는
  영향이 없고 레거시 정리 후보로만 기록한다.
- 새 JSON parse, Python compile/import, source PDF 3개 hash/bytes, 금지 base-log와 project
  vocabulary 전체 suite, git diff check: PASS. CRLF 안내는 Git 작업트리 설정 경고다.
- 수치 경계 보정: mpmath 계산은 80-dps 이상 진단으로 명시하고, symbolic cutoff 식과
  directed interval final certificate를 구분했다.
- 다음 재개점: 새 timestamp handoff 작성, ledger 완료 이름 변경, exact local stage/commit.

## 현재 재개점

모든 산출물과 검증이 완료됐다. 이 원장을 `-done`으로 바꾼 뒤 exact local
stage/commit하고 push하지 않는다.

## 완료 전 점검

- [x] source-first 조사와 actual 조건 대조
- [x] q,R uniformity와 finite cutoff 검증
- [x] 직접 증명 대신 적합한 peer-reviewed source 채택과 finite transfer 검증
- [x] machine ledger·test·Lean 경계 완료
- [x] PAP-11·DEP-R09·fixed 계수·X_cert fail-closed
- [x] 정본·색인·AGENTS/METHODS 동기화
- [x] 전체 unittest·Lean·UTF-8·local links·diff 검증
- [x] 새 timestamp handoff 작성
- [x] 파일명을 `-done.md`로 변경해 같은 local commit에 포함할 준비
