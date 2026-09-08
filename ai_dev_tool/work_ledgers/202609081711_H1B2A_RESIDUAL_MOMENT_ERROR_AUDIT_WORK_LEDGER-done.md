# H1b-2a 잔여 moment/error 감사 작업원장

- 시작: 2026-09-08 17:11 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: 권장 순서에 따른 H1b-2a 문헌 추적, Lemmas 8.5--8.6 및 Proposition 9.4 잔여 오차 감사, 필요한 최소 직접 증명, 데이터 비의존 코드·시험과 정본 동기화
- 금지·보류: 실제 prime/maximal-gap sweep, P018-B 실행, threshold calculator 구현, 패키지·Lean 설치, commit/push/PR
- 선행 변경: 시작 시 `git status --short` 출력 0건; 이전 H1b-1b-2d.1b 작업은 clean 상태로 반영됨

## 목적과 완료조건

- 목적: Maynard Proposition 6.1로 이어지는 Lemmas 8.5--8.6과 Proposition 9.4의 남은 `O`, `o`, `\ll` 항을 실제 call-site와 dependency별로 분해하고, 명시적 선행정리로 닫히는 항과 정량 재증명이 필요한 항을 구분한다.
- 완료조건: 원문 식·가정·정규화·finite range를 고정하고, 적합한 선행증명을 우선 검토하며, 닫히는 최소 연결부만 증명·기계화한다. `H1B-COMP-01`, `SIV-07`, `X_cert` 상태는 증거가 충분할 때만 이동시키고 정본·검증·handoff를 동기화한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | Lemma 8.5/8.6의 hypotheses와 Proposition 9.4 실제 적용을 식 번호별로 분리한다. hidden constant를 1로 두지 않는다. |
| 데이터·provenance | NONE | actual dataset과 실험 artifact를 읽거나 생성하지 않는다. 원문 PDF/TeX 및 공식 source identity만 기록한다. |
| 통계·정밀도 | MEDIUM | 계산 보조는 exact rational 또는 충분한 고정밀 검산으로 제한하고 theorem proof와 수치 진단을 구분한다. |
| 승인 경계 | CONTROLLED | 문헌·증명·toy 검증만 수행한다. 새 설치와 heavy/actual 실행은 별도 요청 전 금지한다. |
| 산출물·비덮어쓰기 | HIGH | 새 번호 문서·v1 계약을 우선하고 기존 정본은 확인된 상태 전이만 반영한다. |

## 단계 현황

1. **COMPLETE — 원문 call-site·기존 dependency·영향도 감사**
2. **COMPLETE — 선행정리·교정본·후속 explicit 문헌 적합성 조사**
3. **COMPLETE — 잔여 오차별 finite 정량화 가능성 및 최소 직접 증명**
4. **COMPLETE — 기계 계약·코드·회귀시험과 정본 동기화**
5. **COMPLETE — 전체 검증·handoff·권장 순서·커밋 제안 및 완료 처리**

## 단계별 기록

### 2026-09-08 17:11 KST — 착수·영향도 고정

- 수행: 최신 handoff, 작업원장 규약, 관련 프로젝트 스킬을 확인하고 승인·금지 경계와 5단계 계획을 고정했다.
- 파일: 이 작업원장
- 명령·검증: `git status --short`, 활성 WORK_LEDGER 검색, 최신 handoff·스킬 전체 읽기
- 결과: worktree clean, 활성 원장 0개, 최신 handoff는 `202609081538_HANDOFF.md`.
- 문제·결정: 이번 세션의 도구 목록에 `update_plan`이 없어 별도 계획 도구 호출은 `TypeError`로 거부됐다. 5단계 계획은 이 원장에 이미 고정되어 있어 작업에는 영향이 없다. 개별 remainder를 닫더라도 공통 moment dominance가 없으면 `H1B-COMP-01`과 `SIV-07`을 승격하지 않는다.
- 다음 재개점: Maynard 최종 출판본 Lemmas 8.5--8.6, Proposition 9.4와 기존 H1b ledger의 열린 node를 식 번호·호출별로 대조한다.

### 2026-09-08 17:18--18:05 KST — 원문 전수 대조·문헌 우선 조사

- 수행: Maynard 2016 최종 출판본 pp.1536--1537의 Lemmas 8.5--8.6과
  pp.1547--1550의 Proposition 9.4, author TeX 606--668·1044--1168행을 대조했다.
  Lemma 8.6이 인용하는 Maynard 2015 Section 7도 최종 출판본 pp.405--408에서 확인했다.
- 원천: `tmp/pdfs/h1b1a/Maynard2016_Dense_Clusters_published.pdf`
  (SHA-256 `8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098`),
  `tmp/pdfs/h1b2a/Maynard2015_Small_Gaps_published.pdf`
  (SHA-256 `3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349`),
  `tmp/pdfs/h1b1b/maynard_source/Subsets.tex`
  (SHA-256 `e55592f0d674e32ad6ef7d6fe25bce2a0aa3cfc712981ccf996a5df0a4d5b18e`).
- 문헌 조사: 공식 출판본·arXiv 및 정확한 lemma/식 문구를 표적 검색했다. 같은 actual
  profile의 Lemma 8.5--8.6과 Proposition 9.4를 숫자 multiplier·finite cutoff까지 한 번에
  닫은 동형의 peer-reviewed package는 이번 표적 검색에서 확인하지 못했다. 이는 전 세계
  부재 또는 novelty 주장이 아니다.
- 확인한 분해:
  1. Lemma 8.5는 coefficient, local divisor weight, global support count의 세 의무다.
  2. Lemma 8.6은 absolute `I/J` lower와 `F1/F2` comparison으로 분리해야 한다.
  3. Proposition 9.4에는 distribution error, exact square algebra, line-1127 Euler product,
     line-1114 denominator, line-1141의 두 Euler product가 별도로 남는다.
- 발견한 교정: 상위 기계 원장의 `H1B-L86-SIZE` 설명은 출판본의
  `(2 k log k)^(-k)`를 `(-k-1)`로 잘못 옮겼다. 이번 동기화에서 수정한다.
- 환경 문제: 첫 공식 PDF 다운로드는 sandbox network 차단으로 연결 거부가 났다. 사용자가
  원문 다운로드를 승인한 범위에서 정상 네트워크 권한으로 재시도해 Maynard 2015 Annals
  최종본을 보존했다. 패키지 설치는 하지 않았다.
- 다음 재개점: actual cutoff의 plateau cube로 `I_k(F)` 절대 하한을 직접 증명하고,
  기존 `L620_dW` 유한오차 package를 이용해 Lemma 8.5의 세 항을 finite envelope로 바꾼다.

### 2026-09-08 18:05 KST — 최소 직접 증명·기계 package

- 신규 이론: `docs/method/theory/28_Sono_FMT_H1b2a_residual_moment_error_package.md`
- 신규 비판 검토: `docs/review/34_20260908_H1b2a_Lemmas85_86_Proposition94_타당성검토.md`
- 신규 계약·코드·시험:
  - `docs/method/theory/data/Sono_FMT_H1b2a_residual_moment_error_v1.json`
  - `source/h1b2a_residual_moment_package.py`
  - `tests/test_h1b2a_residual_moment_package.py`
- 닫힌 수학 연결:
  1. plateau cube로 `I_k(F)>=(2k log k)^(-k)`를 `k>=36`에서 multiplier 1로 증명했다.
  2. H1a와 합쳐 absolute `J_k` lower를 얻고, `F1/F2`에는 안전한 finite
     multiplier `2^k`, `C_J(k)`를 유도했다.
  3. 실제 `L620_dW` finite-product error로 `M_620`을 정의해 Lemma 8.5의 coefficient,
     local weight와 `R^(2+eta_85)` global finite envelope를 닫았다.
  4. Proposition 9.4의 square algebra multiplier 1, denominator `<=2/p`, 첫 Euler 곱
     `<=exp(2/k)`를 닫았다.
- 열린 수학 연결: Proposition 9.4 식 (9.52)의 distribution error와 식 (9.67)의
  pre-`O(k)` exact local factor/Euler comparison. 따라서 `H1B-P94`, `H1B-COMP-01`,
  `SIV-07/09`, `X_cert`는 승격하지 않는다.
- 진단값: `k=36`에서 cube lower/canonical lower 비는 약 `4.116989e6`,
  `I(F2)/k^2` multiplier는 `6.8719476736e10`, `J(F2)/k^2` multiplier는
  약 `2.16653866219e11`; 이는 최적값이나 threshold가 아니다.
- 1차 검증: 신규 6개와 parent 7개, 합계 `Ran 13 tests / OK`; 두 JSON strict parse PASS;
  신규 모듈·시험 `py_compile` PASS.
- 다음 재개점: H1b/H1/T1, theory 색인, METHODS와 AGENTS의 현재 상태를 같은 fail-closed
  판정으로 동기화한 뒤 전체 회귀검증을 수행한다.

### 2026-09-08 18:06 KST — 정본 동기화·검증

- 동기화: theory 색인에 28/34번 문서를 연결하고 `docs/METHODS.md`, `AGENTS.md`,
  H1b/H1/T1 정본과 H1b-1 역사 문서의 successor 상태를 갱신했다.
- 회귀계약: Proposition 9.4의 닫힌 세 local 항과 열린 식 (9.52)/(9.67)을 parent JSON과
  시험에 명시했다. `H1B-P94`, `H1B-COMP-01`, `SIV-07/09`, `X_cert`는 승격하지 않았다.
- 검증:
  - 신규·상위 표적 `Ran 25 tests / OK`
  - sandbox 밖 전체 `Ran 313 tests in 38.544s / OK`
  - 관련 Python `py_compile` PASS
  - 관련 JSON 4개 strict parse PASS
  - theory data JSON 18개 Python strict parse PASS
  - 갱신 핵심 문서 ASCII control character 0
  - 신규 문서·색인 상대 Markdown link PASS
  - `git diff --check` exit 0
- 환경 실패: sandbox 안 첫 전체 suite는 시험용 임시 폴더 생성을 거부해
  `Ran 313 tests / errors=82`였다. 동일 명령을 사용자가 미리 허가한 정상 로컬 권한으로
  재실행하자 313개가 모두 통과했으므로 코드 실패가 아니라 sandbox 권한 실패로 분류했다.
- 수정 중 실패와 조치:
  1. 첫 control-character 패치 문자열에서 diff marker를 JavaScript 단항 연산자로 잘못
     구성해 `NaN` hunk 오류가 났다. 파일은 바뀌지 않았고 올바른 `apply_patch`로 재시도했다.
  2. theory 색인 일괄 패치는 문맥의 `와/과` 불일치로 적용되지 않았다. 작은 hunk 두 개로
     나눠 정상 적용했다.
  3. AGENTS bullet 삽입의 첫 패치는 Markdown bullet의 두 번째 `-`를 patch content에
     넣지 않아 문맥 불일치가 났다. 대상 파일은 바뀌지 않았고 정확한 hunk로 재시도했다.
 4. 신규 이론 문서에 JavaScript `\v` escape에서 생긴 `U+000B` 1건을 발견해
     literal `\varepsilon`으로 교정하고 재검사 0건을 확인했다.
  5. `tests/test_h1b_maynard_constant_ledger.py`의 첫 일괄 패치는 예상 문맥이 현재 파일과
     달라 적용되지 않았다. 파일은 바뀌지 않았고 좁은 hunk로 나눠 정상 적용했다.
  6. 첫 상대-link 검사기의 표시용 pipeline이 .NET MatchCollection을 PowerShell
     pipeline object처럼 다뤄 nonterminating `Cannot index into a null array`를 냈다.
     실제 경로 판정은 실패하지 않았지만 결과를 증거로 채택하지 않고 명시적 counter를 쓰는
     검사로 재실행해 2/1/46개 상대 링크 모두 PASS를 확인했다.
  7. PowerShell `ConvertFrom-Json` 전체 검사는 기존 H1a 계약의 대소문자 구별 key `f`와
     `F`를 같은 key로 취급해 거부됐다. 관련 4개는 PowerShell로도 PASS했고, 전체 18개는
     대소문자를 구별하는 고정 FGKMT Python `json` parser로 다시 검사해 PASS했다.
  8. stale-state 최종 검색의 첫 정규식은 기본 `rg`가 지원하지 않는 negative lookahead를
     사용해 parse error가 났다. `--pcre2`로 재실행했고 검출된 1건은 `-k-1` 전사 오류를
     `-k`로 교정했다고 설명하는 의도된 역사 문장임을 확인했다.
- 실제 실행 경계: prime/maximal-gap sweep, P018-B, threshold calculator, 새 패키지·Lean
  설치는 수행하지 않았다.
- 다음 재개점: 새 timestamp handoff를 작성하고 링크·whitespace·상태 수를 최종 확인한다.

## 최종 상태

요청 산출물·정본 동기화·검증·handoff가 완료됐다. 다음 재개점은 H1b-2a.1
Proposition 9.4 식 (9.67)의 exact Euler normalization이다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] 결과 색인 N/A(actual 실험 없음), METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
