# DEP-R09 Branch S 정량 PNT-in-AP transfer 작업원장

- 착수: 2026-09-13 09:36 KST
- 시작 HEAD: `cc6491f60eed11bd76c365194f6b35f921cf0651`
- 사용자 승인: 활성 목표의 “권장 작업 착수 순서에 따라 작업 착수”
- 목표: fixed `2e-17` 경로와 호환 가능한 `D=160` pointwise PAP의 numerical
  multiplier, decay, exceptional branch, finite cutoff를 복원하거나 정확한 최소 blocker를 고정
- 현재 상태: `PAP-11 / DEP-R09 / fixed 2e-17 / X_cert OPEN`
- 금지: actual prime sweep, threshold calculator, 장시간 계산, source theorem의 local axiom화,
  `sorry`·`admit`, 계수의 임의 설정, 외부 저자 연락, package 설치

## 영향 분석

| 축 | 판정 | 통제 |
|---|---|---|
| iterated log·end-bounded G/F/H | 영향 없음 | empirical 코드·결과를 변경하지 않는다. |
| fixed `2e-17` | 핵심 영향 | 모든 hidden constant와 cutoff가 숫자가 될 때만 승격한다. |
| `X_cert` | 핵심 영향 | PAP 한 구성요소의 cutoff를 전체 threshold로 부르지 않는다. |
| provenance | 핵심 영향 | theorem/equation/page/version/hash와 변수 치환을 기록한다. |
| Lean | 조건부 영향 | source theorem과 downstream algebra를 분리하고 source 고정 뒤 필요한 child만 형식화한다. |
| 데이터·실험 | 영향 없음 | `datas/`, `test_result/`, figure, prime sweep을 만들지 않는다. |
| 사용자 자원 | 현재 불필요 | 168시간급 또는 별도 계산이 실제 필요해질 때 명령·시간·중단조건과 함께 요청한다. |

## 접근 비교와 권장안

| 접근 | 정확성·재현성 | 비용·위험 | 역할 |
|---|---|---|---|
| S1. Thorner--Zaman proof constant 추출 | 현대적이고 target 범위에 가장 가까움 | 의존 lemma의 `effectively computable` 상수를 끝까지 추적해야 함 | 1순위 |
| S2. Gallagher--Jutila--Huxley 고전 proof 재정량화 | Sono/FMT 경로와 직접 연결 | 숨은 Vinogradov multiplier와 오래된 source chain이 큼 | S1 blocker 확인 뒤 |
| E. fully explicit density+DH 새 transfer | 입력 숫자는 명시적 | 큰 prefactor, pointwise 변환 신규 증명, fixed 계수 손실 위험 | 독립 보조축 |

현재는 S1을 먼저 감사한다. statement 수준에서 수치 package가 회수되지 않으면 proof DAG의
첫 비명시 lemma와 필요한 대체 source를 특정한 뒤 S2 또는 E로 넘어간다.

## 단계 현황

1. **COMPLETE — 시작 상태·승인·영향도·선행 커밋 고정**
2. **COMPLETE — actual PAP target과 Thorner--Zaman proof DAG 복원**
3. **COMPLETE — 각 hidden multiplier·finite cutoff의 선행 explicit source 조사**
4. **COMPLETE — 가능한 finite transfer 정식화 또는 최소 hard blocker 확정**
5. **COMPLETE — Lean 필요성 판정·기계 원장·fail-closed 검증**
6. **COMPLETE — 정본 동기화·handoff·검증·로컬 commit 준비**

## 단계 기록

### 2026-09-13 09:36 KST — 단계 1 완료

- 직전 DEP-R09 대체자료 배치는 로컬 commit
  `cc6491f60eed11bd76c365194f6b35f921cf0651`로 고정됐고 시작 worktree는 clean이다.
- 직전 handoff의 누락된 LaTeX delimiter와 METHODS의 오래된 H1a 표기는 커밋 전에 복구했다.
  교정 및 검증 명령 오류는 오류 원장 E098--E099에 공개 기록했다.
- 다음 재개점: Theory 57·58과 Thorner--Zaman Theorems 1.1, 2.1, 2.3 및 proof Section 3을
  native text와 원 페이지로 읽어 target PAP까지의 모든 의존 lemma와 hidden constant를 표로 만든다.

### 2026-09-13 10:04 KST 확인 — 단계 2 완료

- Thorner--Zaman arXiv `2108.10878v2`, 11쪽 PDF
  `SHA-256=588ec896e0820c3620175b25da58850efbefc67b71227acac1d5c3fa4f6b3b09`를
  native text 우선으로 읽고 PDF pp. 4, 5, 8, 10, 11을 렌더링 대조했다.
- Theorem 2.1의 unconditional density (2.1)는 Huxley--Jutila 결과를 바로 인용하며
  multiplier와 시작점을 인쇄하지 않는다. exceptional-removed (2.2)는 `sufficiently small`
  `nu_epsilon`, effective beta-one lower bound, Jutila Theorem 2의 비수치 cutoff,
  implied-constant inflation과 epsilon rescaling을 추가로 사용한다.
- Theorem 2.3 proof는 standard explicit formula의 `O`, Chebyshev의 `≪`, local zero count,
  Taylor·dyadic `O(log x)`, partial summation과 density multiplier, 여러 `≪_epsilon`을 거친다.
  Theorem 1.1의 Vinogradov--Korobov decay constant도 `effectively computable`일 뿐 숫자가 없다.
- 실제 `h=x`, `q=x^(1/D)`에서 fixed `D=160`이면 leading relative error는
  `K_epsilon exp(-160 c1(epsilon)+o(1))` 꼴이다. `log x/log q=160`이 고정되므로
  `x` 증가만으로 미지 multiplier를 흡수할 수 없다는 점을 최소 구조 blocker로 확인했다.

### 2026-09-13 10:04 KST 확인 — 단계 3 완료

- Jutila 1977 공식 Math. Scand. PDF 18쪽을 확보했다.
  `SHA-256=f6e9038a7216b690763692e0a07bc8c58284c9560bf62ab987ea62a817404ad5`다.
  native `pdftotext -layout` 결과가 form-feed 18바이트뿐이라 OCR이 필요한 PDF로 판정하고,
  300dpi 렌더링 뒤 전 18쪽 OCR과 pp. 46, 47, 54, 58, 59, 61 원 페이지 대조를 수행했다.
- Theorem 1의 exponent 2 density는 구조적으로 유망하지만 `≪_epsilon` multiplier가 숨겨져 있다.
  Theorem 1-prime의 `10 exp(11 lambda)`도 `D sufficiently large`, Theorem 2도
  `D>=D0(epsilon)`이고 수치 `D0`가 없다.
- proof에는 S. Graham의 당시 `to appear` Lemma 4, `R→∞`와 `1+o(1)`인 Lemma 5,
  epsilon-의존 cutoff와 multiplier를 가진 Lemmas 6·8, `lower order`,
  `sufficiently good lower bound`, 그리고 최종 `crude estimations / do not enter into the details`
  단계가 남는다. 따라서 이 원문은 재정량화 경로이지 drop-in numerical PAP가 아니다.
- Huxley 1974/75 논문의 DOI·공식 IMPAN 페이지와 PDF endpoint를 확인했으나, 자동 다운로드가
  Anubis JavaScript proof-of-work에 막혔다. Crossref resource URL도 PDF가 아니라 HTML challenge를
  반환해 header로 탐지하고 해당 임시파일을 즉시 제거했다. 비공식 mirror는 사용하지 않았다.
  이 접근 제한은 현재 `NOT_NUMERICAL` 판정에는 영향을 주지 않지만 Huxley branch의 완전한
  직접 재정량화 전에는 공식 원문을 별도로 확보해야 한다.
- 다음 재개점: 허용 오차 `eta=1-C_min(160)`에 대해
  `c1 >= (log K-log eta)/160`인 정량 gate를 고정밀 계산하고, source theorem과 분리된
  기계 원장·Theory 59·검증시험을 작성한다.

### 2026-09-13 10:04 KST 확인 — 단계 4 완료

- [Theory 59](../../docs/method/theory/59_Sono_FMT_DEPR09_branch_S_quantitative_transfer_audit.md)와
  [review 66](../../docs/review/66_20260913_DEPR09_branch_S_정량_transfer_타당성검토.md)를 작성했다.
- actual source가 `K exp(-D c)`를 줄 때의 충분조건
  `c >= (log K-log eta)/D`를 고정했다. D=160의 총 error budget을 사용한 K별 최소 c는
  K=1/10/320/1000/1000000에서 각각 약
  0.0124616/0.0268528/0.0485136/0.0556351/0.0988086이다.
- 이 표는 actual Thorner--Zaman multiplier를 추측하지 않는 필요 진단이다. 특히 K=320은
  source 식 (2.5)에 보이는 `2D`만 떼어낸 예시이지 전체 multiplier가 아니다.
- 최소 hard blocker를 unconditional density `RS02-A`, exceptional density/DH `RS02-B`,
  density-to-prime-sum `RS03`, common cutoff `RS07`로 고정했다. `RS04--RS06`도 OPEN이다.
- D=160/170/180/186/187의 coefficient capacity를 재계산해, D가 커질수록 허용 total error가
  약 13.62%/8.56%/3.49%/0.458%/음수로 줄어드는 tradeoff를 기록했다.

### 2026-09-13 10:04 KST 확인 — 단계 5 완료

- 기계 원장
  `docs/method/theory/data/Sono_FMT_DEPR09_branch_S_transfer_v1.json`과 fail-closed test
  `tests/test_dep_r09_branch_s_transfer.py`를 작성했다. 표적 Python test 7/7, Theory 58과
  결합한 test 14/14가 PASS했다.
- source analytic theorem은 local axiom으로 만들지 않았다. 식 (59.5)의 초등 부등식만
  Lean `pap_fixed_d_transfer_gate`로 형식화했고 `lake build`가 8,765 jobs 성공했다.
- inventory generator·validator 결과: theory 60개, display 1,056식,
  `KERNEL_PASS=29`, `SOURCE_THEOREM_UNFORMALIZED=21`, `NOT_YET_FORMALIZED=970`,
  금지 proof escape 0, validator PASS다.
- `PAP-11`, DEP-R09, fixed `2e-17`, X_cert는 모두 OPEN이고 actual prime computation은
  수행하지 않았다.
- 다음 재개점: 정본 색인·METHODS·AGENTS·Lean README·오류 원장 동기화를 재검증하고,
  새 timestamp handoff를 작성한 뒤 exact allowlist만 stage·commit한다.

### 2026-09-13 session close — 단계 6 완료

- AGENTS, METHODS, theory/review 색인, Lean README·원장과 최신 handoff를 Theory 59 판정에
  맞춰 동기화했다. source theorem과 초등 transfer 대수를 계속 분리했다.
- Branch S 표적 7/7, Theory 58+59 결합 14/14가 PASS했다. 전체 unittest는 앞선 정상 로컬
  실행 683/683(66.961초)에 이어 session-close 정상 로컬 재실행도 683/683(64.077초) PASS했다.
- Lean `lake build` 8,765 jobs, inventory generator·validator, 금지 proof escape 0이 PASS했다.
- 최종 정적 감사는 Markdown 12개 strict UTF-8·제어문자 issue 0, local link 1,268개,
  신규 문서 delimiter issue 0, JSON 3개 parse와 `git diff --check` PASS다.
- 감사 명령 자체의 import/API/heuristic 오류와 false positive는 파일 영향 없이 교정하고
  오류 원장 E105에 공개 기록했다.
- 전체 suite를 sandbox에서 잘못 재실행해 발생한 82개 `PermissionError`는 환경 실패로
  분리하고, 정상 로컬 재실행 PASS와 별도 Lean 재빌드 PASS로 최종 판정을 고정했다(E106).
- actual prime sweep, threshold calculator, 외부 게시, package 설치는 수행하지 않았다.
- 이 원장은 완료 조건 충족 뒤 `-done`으로 이름을 바꾸고 exact allowlist만 로컬 commit한다.

## 완료 조건

- [x] actual PAP 변수·quantifier·one-sided error budget을 하나의 contract로 고정
- [x] proof DAG의 모든 source edge에 page/equation/version/hash 기록
- [x] 각 implied constant의 numerical/effective/ineffective 상태 구분
- [x] 기존 explicit 선행정리의 drop-in 가능성을 개별 검토
- [x] 가능한 경우 finite multiplier·cutoff 유도, 불가능하면 최초 hard blocker 특정
- [x] fixed `2e-17`·PAP-11·X_cert를 증거에 맞게 fail-closed 동기화
- [x] Lean 형식화 필요성 판정과 proof-escape 0 확인
- [x] 표적·전체 검증, 새 handoff, 사용자 수행절차 기록
