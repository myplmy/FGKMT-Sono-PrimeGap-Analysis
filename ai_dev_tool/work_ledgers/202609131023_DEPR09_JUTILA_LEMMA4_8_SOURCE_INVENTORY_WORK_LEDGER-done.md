# DEP-R09 Jutila Lemma 4--8 source inventory 작업원장

- 시작: 2026-09-13 10:23 KST
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 직전 commit: `15aa27f2a127e65fd6f226d028a59406f8d62947`
- 목표: Jutila 1977 Lemmas 4--8과 Theorems 1, 1-prime, 2 사이의 실제 proof DAG를
  source/page/equation 단위로 고정하고, fixed `D=160` PAP에 필요한 multiplier·cutoff를
  기존 정리에서 회수할 수 있는지 fail-closed 판정한다.
- 비목적: actual prime sweep, `X_cert` 계산기 작성, 임의 hidden constant 선택,
  peer review 없이 새 analytic theorem을 사실로 승격, Huxley 비공식 mirror 사용
- 사용자 승인: source-first 정규화·증명 작업, 필요한 Lean 형식화, 문서·시험·핸드오프와
  로컬 stage/commit 승인. 장시간 계산과 새 dependency는 사용자 요청 후 중단한다.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| iterated log·end-bounded empirical 정의 | 영향 없음 | empirical code·dataset·result를 변경하지 않는다. |
| fixed `2e-17` | 핵심 영향 | source multiplier·cutoff가 모두 숫자가 되기 전에는 인증하지 않는다. |
| `X_cert` | 핵심 영향 | Jutila 한 lemma의 cutoff를 전체 threshold로 부르지 않는다. |
| provenance | 핵심 영향 | 공식 PDF와 인용 source의 version·page·equation·hash를 기록한다. |
| Lean | 조건부 영향 | 외부 analytic theorem은 axiom화하지 않고, 새 finite 대수 결론만 필요할 때 형식화한다. |
| 사용자 계산자원 | 현재 불필요 | 168시간급 연산·추가 package가 필요하면 정확한 명령과 예상량을 제시하고 중단한다. |

## 접근 비교와 선택

| 접근 | 장점 | 한계 | 이번 역할 |
|---|---|---|---|
| A. Jutila proof와 인용 source 직접 감사 | exponent 2 경로의 실제 최초 blocker를 찾음 | 1977 표기·후속 source 추적 비용 | 주 경로 |
| B. 현대 explicit density theorem으로 치환 | numerical input을 얻을 가능성 | fixed D=160 pointwise PAP의 drop-in 여부 미확정 | 각 lemma별 대체 후보 조사 |
| C. Jutila lemma를 처음부터 직접 재증명 | 모든 상수를 통제 가능 | 큰 analytic proof 비용·오류 위험 | 기존 적합 source가 없을 때만 후속 후보 |

사용자 제안대로 A와 B를 먼저 수행한다. 적합한 선행 증명이 없다고 확인한 node에 대해서만 C의
정식화 범위와 난도를 산정한다.

## 단계 현황

1. **COMPLETE — 시작 상태·승인·Huxley 유무·영향도 고정**
2. **COMPLETE — Jutila Lemmas 4--8 원문 명제와 proof call inventory**
3. **COMPLETE — 각 인용 source 공식 원문·후속 correction·현대 대체자료 조사**
4. **COMPLETE — fixed D=160 quantitative recoverability와 최초 hard blocker 판정**
5. **COMPLETE — Theory/review/machine ledger·Lean·tests 작성**
6. **COMPLETE — 정본 동기화·전체 검증·새 handoff·exact local commit 준비**

## 단계 기록

### 2026-09-13 10:23 KST — 단계 1 완료

- 시작 worktree가 clean이고 직전 Branch S commit을 확인했다.
- 지정된 `article/Huxley 1975 Large values of Dirichlet polynomials III.pdf`는 아직 없다.
  Huxley RS02-A는 대기 상태로 보존하고 비공식 사본으로 대체하지 않는다.
- Jutila 공식 Math. Scand. PDF와 300dpi OCR·원페이지 대조 자료가 남아 있어, 독립적으로
  진행 가능한 Lemma 4--8 source inventory를 다음 우선순위로 선택했다.
- 다음 재개점: OCR 전체에서 Lemma 4--8의 정확한 명제·proof·인용 번호를 추출하고 렌더링
  원페이지로 수식·부등호·quantifier를 대조한다.

### 2026-09-13 10:41 KST — 단계 2 완료

- Jutila 인쇄 pp. 49--54를 300dpi 렌더링과 대조해 Lemma 4--8의 명제·조건·인용을 고정했다.
- Lemma 4는 Graham의 Barban--Vehov 제곱합 점근식, Lemma 5는 squarefree·coprime 조화합의
  `1+o(1)`, Lemma 6은 Lemma 5와 Mellin tail, Lemma 7은 Montgomery Lemma 1.6형 정확한
  Halasz 부등식, Lemma 8은 Prachar p.331의 local zero-count `<<`를 사용한다.
- Theorem 1 proof에서 Lemma 8 -> Lemma 6 -> Lemma 7 -> 식 (3.6)의 Lemma 4 호출 순서를
  확인했다. Theorem 1-prime은 같은 골격을 단순화해 Lemmas 4--5로 explicit하게 만들 수
  있다고 쓰지만 결론은 계속 `D sufficiently large`다.

### 2026-09-13 10:41 KST — 단계 3 완료

- IMPAN 공식 HTML에서 실제 CC-BY download endpoint를 찾아 Huxley 1975 III 원문을
  확보했다. `%PDF-1.3`, 388,706 bytes, SHA-256
  `cc8b7282c1963687d357829416d5e471e130810e5324709a96319bb7a2a3428f`를 검증하고
  요청된 `article/Huxley 1975 Large values of Dirichlet polynomials III.pdf`에 보존했다.
- Huxley III와 Huxley--Jutila IV는 exponent 2의 구조를 뒷받침하지만 `D sufficiently large`,
  epsilon-의존 implied constants와 `o(1)`을 남겨 numerical drop-in은 아니다.
- Graham 1978 최종 출판정보(DOI `10.1016/0022-314X(78)90010-0`)는 확인했으나 공식
  DeepBlue 자동 다운로드는 403 challenge였다. HTML을 PDF로 오인하지 않았고 임시
  잘못된 응답은 제거했다.
- Ramaré--Zuniga Alterman arXiv `2405.12662`, Corollary 1.3이 일반 `tau>1`에서 Jutila
  식 (3.6)의 실제 one-sided weighted square-sum을 명시적으로 대체함을 확인했다.
  actual `tau=8/5` 상수는 exact rational `18884947/500000 = 37.769894`다.
- Berkane 2014는 `tau=2` 위주의 explicit route, Zuniga Alterman 2022는 one-parameter와
  `X>=U^2` route라 actual `tau=8/5`의 직접 대체가 아니다.
- 다음 재개점: Lemma 4 actual 호출의 닫힘 범위를 full asymptotic과 분리하고, Lemmas 5--8의
  최초 남은 numerical blocker를 JSON·Theory 60·review 67에 fail-closed로 기록한다.

### 2026-09-13 10:58 KST — 단계 4 완료

- Ramaré--Zuniga Alterman Corollary 1.3을 Jutila actual `tau=8/5`에 대입해 one-sided
  weighted square-sum 상수 `18884947/500000 = 37.769894`를 얻었다.
- finite `x_D=D^(11/2) log(D)^2`에는
  `exp(4 lambda loglog(D)/log(D))` 보정이 남음을 별도 식으로 보존했다. 따라서 Jutila의
  인쇄된 `10 exp(11 lambda)` 전체는 인증하지 않았다.
- 최초 남은 hard blocker는 `JL5`의 uniform finite harmonic lower bound다. 이후 `JL6`의
  Mellin/tail 절대상수와 `JL8`의 local zero-count multiplier가 순차적으로 남는다.
- Huxley source leaf 확보는 완료됐지만 원문이 parameter-dependent implied constant와
  sufficiently-large cutoff를 남기므로 `RS02-A`는 계속 HARD_BLOCKER다.

### 2026-09-13 10:58 KST — 단계 5 완료

- Theory 60, review 67, 기계 원장과 6개 fail-closed unittest를 작성했다.
- Branch S JSON·test·Theory 59·review 66의 과거 Huxley 미확보 상태를 공식 PDF
  hash·OCR 판정으로 교정했다.
- Lean 단일 파일에 actual coefficient, log-ratio, power-exponent 대수를 추가했다.
  첫 parser 실행에서 그리스 lambda가 문법 token과 충돌했으나 `lam`으로 교정했고,
  `lake env lean FGKMTSono/TheoryVerification.lean`은 exit 0이다.
- 새·Branch S 표적 unittest 13/13 PASS. 전수 원장 생성·검증은 theory 61개,
  display 1,068식, `NOT_YET_FORMALIZED` 971식, banned proof escape 0으로 PASS했다.
- 탐색 명령·patch 문맥 실패 등 비과학적 실수는 오류 원장 E107에 기록했다.
- 다음 재개점: 전체 unittest·lake build·정적 link/UTF-8/diff 검증 후 handoff와 exact commit.

### 2026-09-13 11:05 KST — 단계 6 완료

- 고정 FGKMT Python 전체 unittest 689/689 PASS(65.677초).
- Lean 4.34.0-rc2 commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`,
  `lake build` 8,765 jobs PASS, direct single-file exit 0.
- 재생성 inventory는 theory 61개, display 1,068식, declaration 122개,
  banned proof escape 0이다. status validator와 local links가 PASS했다.
- 변경 Markdown 11개 strict UTF-8·control issue 0, local link 1,274개, JSON parse,
  금지 base-log pattern, `git diff --check`가 PASS했다.
- 새 handoff `handoff/202609131105_HANDOFF.md`를 작성하고 사용자 수행절차 없음,
  후속 `JL5a` 우선순위와 한국어 commit 메시지를 기록했다.
- local commit 직전 완료 상태이므로 원장을 `-done`으로 이관한 뒤 exact staging diff를 검토한다.

## 완료 조건

- [x] Lemmas 4--8의 정확한 statement·parameter range·hidden notation 등록
- [x] Theorems 1/1-prime/2가 각 lemma를 쓰는 위치와 의존 방향 등록
- [x] 인용 source마다 공식 원문 또는 신뢰 가능한 bibliographic source 고정
- [x] `O`, `o(1)`, `sufficiently large`, lower-order·생략 세부의 numerical 상태 분류
- [x] modern explicit replacement의 drop-in 여부를 명제별로 검토
- [x] direct reproving이 필요한 최초 node와 입력·예상 난도 특정
- [x] PAP-11·DEP-R09·fixed `2e-17`·`X_cert` 상태를 fail-closed 유지
- [x] 필요한 기계검증·Lean 판단·전체 회귀검증·handoff·로컬 commit 준비 완료
