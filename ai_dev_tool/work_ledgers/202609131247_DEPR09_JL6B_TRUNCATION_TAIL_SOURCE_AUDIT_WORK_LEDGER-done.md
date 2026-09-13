# DEP-R09 JL6b truncation tail source audit 작업원장

- 시작: 2026-09-13 12:47 KST
- 현재 상태: COMPLETE
- 직전 commit: `6cab3991f3cc9500f2ebb522e409b0f4586678a2`
- 사용자 승인: `X_cert` 계산기 이전 source-first 정규화·증명, 필요한 문헌 확보,
  필요할 때 Lean 형식화·검증, 문서·시험·handoff와 단계별 로컬 stage/commit
- 금지·보류: actual prime sweep, threshold calculator, 숨은 implied constant 임의 선택,
  장시간 연산, 새 package 설치, source theorem의 project-local axiom화
- 선행 변경: 시작 worktree clean; 이번 작업 비소유 변경 없음

## 목적과 완료조건

- 목적: Jutila 1977 Lemma 6 proof가 무한급수를
  `x=X log(qT)^2`에서 자른 뒤 별도로 `<<_epsilon 1`이라 쓴 truncation tail을
  actual coefficient와 parameter에 맞춰 source-first로 명시화한다.
- 완료조건:
  1. 자르는 두 급수, 정확한 시작점·endpoint·절대값·weight를 원문 페이지에서 고정한다.
  2. Jutila/Prachar 또는 peer-reviewed explicit exponential-tail 정리가 actual 식에
     그대로 적용되는지 먼저 조사한다.
  3. drop-in source가 없으면 실제 `a(n)`, `psi_r(n)`의 점별 상계부터 직접 증명하고
     tail의 계산 가능한 multiplier와 충분조건을 도출한다.
  4. Mellin 적분, tail, JL5 loss와 JL6 종단 error budget을 섞지 않고 상태를 분리한다.
  5. dependency-critical 유한 대수만 필요시 Lean 단일 파일에 형식화하며 analytic source를
     local axiom으로 넣지 않는다.
  6. JL6 전체·JL8·PAP-11·DEP-R09·fixed `2e-17`·`X_cert`는 전체 의무가 닫히기 전
     승격하지 않는다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | dataset·empirical result·figure를 변경하지 않는다. |
| JL6 proof DAG | 직접 영향 | `JL6-MELLIN`, `JL6-TAIL`, common error budget을 별도 node로 둔다. |
| fixed `2e-17`·`X_cert` | 간접 핵심 영향 | tail 하나가 닫혀도 root certificate를 닫지 않는다. |
| analytic uniformity | 핵심 위험 | 고정 parameter tail을 uniform zero-density theorem으로 확대하지 않는다. |
| provenance | 핵심 영향 | PDF native/OCR 분류, page/equation/version/hash와 rendered 원문 대조를 기록한다. |
| Lean | 확인 필요 | exponential·log의 유한 실수대수만 후보이며 외부 analytic theorem은 premise로 남긴다. |
| 사용자 계산자원 | 현재 불필요 예상 | 30분 이상 연산 또는 새 dependency가 필요하면 실행하지 않고 요청한다. |

## 접근 비교와 선택

| 접근 | 정확성·재현성 | 비용·위험 | 순서 |
|---|---|---|---|
| A. Jutila/Prachar의 직접 tail lemma 복원 | 원 proof와 coefficient mismatch 위험이 가장 작음 | 원문 접근 제한·비명시 상수 가능 | 1순위 |
| B. 현대 explicit incomplete-Gamma/exponential tail 정리 | 상수·cutoff가 인쇄돼 있으면 짧게 대입 가능 | 함수·복소지수·coefficient 조건 mismatch 가능 | 2순위 |
| C. actual coefficient의 절대값으로 직접 초등 상계 | 모든 상수와 endpoint를 통제 가능 | 과도한 divisor bound가 Jutila (2.8) 예산을 깨뜨릴 수 있음 | A/B 부적합 시 |
| D. smoothing이나 cutoff 자체 변경 | tail을 더 작게 만들 가능성 | downstream proof 전체를 바꾸고 새 residue·main term 위험 | 현재 비권장 |

## 단계 현황

1. **COMPLETE — Jutila JL6 tail exact statement·actual coefficient 고정**
2. **COMPLETE — source-first explicit tail theorem 조사·적합성 판정**
3. **COMPLETE — 필요한 직접 finite bound와 common-condition 영향 도출**
4. **COMPLETE — Theory/review/machine ledger/test 및 필요한 Lean 형식화**
5. **COMPLETE — 정본 동기화·전체 검증·handoff·로컬 commit 준비**

## 단계별 기록

### 2026-09-13 12:47 KST — 시작

- 수행: 최신 handoff·Theory 62·commit과 관련 스킬을 확인했다. 이전 단계는 authoritative
  변경과 검증을 남겼으므로 progress이고 다음 첫 미완료 node는 `JL6-TAIL`이다.
- 문제: 필요한 파일을 찾는 첫 명령에서 `rg --files tmp`로 범위를 너무 넓게 잡아 과거
  test 임시 디렉터리의 access-denied 메시지를 다수 발생시켰다. 읽기 전용 검색 실패이며
  파일·실행 중 프로세스·수학 결과에 영향은 없다. 이후 검색 범위를
  `tmp/pdfs/dep_r09_branch_s_20260913`과 명시 파일로 제한한다.
- 다음 재개점: Jutila 인쇄 pp. 50--51에 해당하는 OCR·rendered page를 직접 읽어
  tail의 두 급수와 원문이 사용한 pointwise bound를 정확히 전사한다.

### 2026-09-13 13:05 KST — 원문·actual parameter 고정

- Jutila 인쇄 pp. 50--52의 렌더링 원페이지와 OCR을 대조했다. 식 (2.11)에서 절단되는
  유일한 무한 (n)-급수의 꼬리는
  `n > x`, `x=X log(qT)^2`이고, 첫 `r`-합은 유한합이다.
- actual Theorem 1-prime 적용은 원페이지에서
  `D=qT`, `R=D^epsilon`, `z1=D^(1/2+7epsilon)`,
  `z2=D^(1/2+8epsilon)`, `X=D^(1+12epsilon)`으로 재확인했다.
- 원문은 일반 Lemma 6에서 tail을 `<<_epsilon 1`이라고만 하고 (X)의 명시적 상한을
  주지 않는다. 따라서 절대값 proof로 actual 적용을 닫는 것과 인쇄된 일반 Lemma 전체를
  닫는 것을 분리한다.

### 2026-09-13 13:18 KST — source-first 검색·적합성 판정

- Math. Scandinavica 공식 Jutila 원문과 NIST DLMF의 incomplete-gamma/exponential-tail
  공식을 대조했다. exact discrete exponential tail에는 별도 특수함수 정리보다
  geometric series와 `exp(u)-1>=u`를 쓰는 직접 초등 proof가 더 짧고 강하다.
- S. Graham, *On Linnik's constant*, Acta Arith. 39 (1981), DOI
  `10.4064/aa-39-2-163-179`도 확인했으나, 검색 가능한 statement는 truncated Perron
  detector를 쓰는 다른 Lemma 6이므로 Jutila 식 (2.11)의 drop-in tail source가 아니다.
- Graham PDF를 공식 endpoint에서 audit copy로 받으려 한 두 명령은 Anubis JavaScript
  challenge/redirect 때문에 실패했다. 첫 시도는 실패 뒤 존재하지 않는 파일의 hash를,
  두 번째는 생성되지 않은 `.part` 파일을 후속 검사해 불필요한 오류를 연쇄 발생시켰다.
  파일은 생성·삭제되지 않았고 과학 판정 영향은 없다. 이 비필수 source를 확보하기 위해
  접근 제한을 우회하거나 사용자에게 원문을 요청하지 않는다.
- 직접 맞는 published explicit tail theorem은 표적 검색에서 식별하지 못했다. actual
  coefficient의 초등 절대값 proof로 진행한다.

### 2026-09-13 13:28 KST — 직접 finite bound

- `|lambda_d|<=1`에서 `|a(n)|<=tau(n)<=2 sqrt(n)`,
  `|psi_r(n)|<=r`, `beta>=1/2`를 사용하면 summand의 비지수 부분은 합계 `2R` 이하이다.
- `N=floor(x)+1`에 대해 geometric tail을 endpoint-safe하게 합성해
  `|E_tail| <= 2R(X+1)exp(-x/X) <= 4RX exp(-log(D)^2)`를 얻었다.
- general envelope `R<=D^r`, `X<=D^c`에서는
  `4 exp(-L^2+(r+c)L)`, `L=log D`이다. actual exponent 합은
  `r+c=1+13epsilon`이다.
- `0<tau<=4`인 목표 absolute budget에 대해
  `L>=max(2(r+c), sqrt(2 log(4/tau)))`는 tail `<=tau`의 계산 가능한 충분조건이다.
- 중요한 적용범위: 이 결과는 (R,X)의 upper envelope가 고정된 actual application을
  닫는다. (X)의 upper bound가 없는 printed general Lemma 6 전체는 닫지 않는다.

### 2026-09-13 13:12 KST — 문서·기계판정·Lean 1차 구현

- 신규: Theory 63, review 70, machine JSON, Python evaluator와 fail-closed unittest를
  작성했다. 표적 unittest 9/9, `py_compile`, strict JSON parse가 PASS했다.
- Lean 단일 파일에 `X+1<=2X`, geometric reciprocal,
  actual exponent identity, quadratic decay, exponential budget과 max/sqrt cutoff를
  추가했다. direct Lean compile이 PASS했다.
- 무한 geometric series, divisor pairing, pseudocharacter definition 전체는 이번 Lean
  batch에서 형식화하지 않았고 원장에서 `NOT_YET_FORMALIZED` 또는
  `PARTIAL_FORMALIZATION`으로 보존한다. project-local axiom·`sorry`·`admit`은 0건이다.
- 1차 inventory는 64개 theory 문서·1,119식을 식별했고 validator PASS였다. 이후 reciprocal
  theorem과 상태 연결을 추가했으므로 최종 generation/build/count를 stage 5에서 다시 한다.
- 교정: Theory 63 식 (63.9)의 `\\le`가 초안에서 `le`로 빠졌음을 inventory preview에서
  발견해 즉시 교정했다. E111에 기록했고 잘못된 식은 결과에 사용하지 않았다.

### 2026-09-13 13:22 KST — 단계 4 완료·단계 5 검증 진행

- Theory 63, review 70, machine JSON, Python evaluator·시험, Lean 단일 파일과 상태 원장을
  동기화했다. `JL6-TAIL-ACTUAL`만 parameterized explicit로 진전시키고 printed general
  tail, common budget, JL6 전체·JL8와 root certificate는 fail-closed로 유지했다.
- 신규 표적시험 9/9와 JL4--JL6 관련시험 34/34가 PASS했다. 전체 unittest의 최초 sandbox
  실행은 `TemporaryDirectory` 접근 제한 때문에 82건 `PermissionError`를 냈으며 코드 실패
  증거로 채택하지 않았다. 사용자 승인 범위의 정상 로컬 권한에서 다시 실행한 결과
  **717/717 PASS, 69.341초, exit 0**이었다.
- Python compile·strict JSON parse가 PASS했다. 최종 Lean generator/validator는 theory 64개,
  display 1,119식, declaration 143개, local link 1,186개, banned proof escape 0건으로 PASS했다.
  상태 집계는 `KERNEL_PASS=40`, `CONDITIONAL_KERNEL_PASS=20`, `DEFINITION_ONLY=13`,
  `PARTIAL_FORMALIZATION=20`, `SOURCE_THEOREM_UNFORMALIZED=34`,
  `NOT_YET_FORMALIZED=987`, `PARSE_REVIEW_REQUIRED=5`다.
- direct Lean compile과 full `lake build` **8,765 jobs PASS**를 최종 상태에서 재확인했다.

### 2026-09-13 13:22 KST — 단계 5 완료

- AGENTS, METHODS, theory·review 색인과 predecessor successor note, Lean README·원장,
  오류 원장을 동기화하고 `handoff/202609131322_HANDOFF.md`를 새로 작성했다.
- 변경·신규 텍스트 23파일 strict UTF-8/control issue 0, Markdown 16파일 local link
  1,377개 issue 0, JSON 3/3 parse, Python compile과 `git diff --check`가 PASS했다.
- 첫 복합 static-validation one-liner는 진단 없이 exit 1을 반환해 성공으로 채택하지 않았다.
  세 검사로 나누어 전부 재실행했고 오류 원장 E111에 기록했다.
- 결과·검증·정본·handoff가 모두 완료됐다. 이 원장을 `-done.md`로 이관한 뒤 이번 작업의
  변경만 로컬 stage·commit한다. push나 외부 게시를 수행하지 않는다.

## 현재 재개점

완료 원장으로 안전하게 이관한 뒤 최종 status·diff를 확인하고 이번 작업 파일만 stage하여
승인된 로컬 commit을 만든다. 다음 연구 재개점은 Theory 61--63을 한 오차예산으로 묶는
`JL6c common detector error budget`이다.

## 완료 전 점검

- [x] 원문 tail 두 급수와 endpoint·weight 고정
- [x] source-first 조사와 actual 조건 대조
- [x] tail multiplier·cutoff 또는 정직한 blocker 판정
- [x] Mellin/tail/common budget 경계 분리
- [x] machine ledger·test·필요한 Lean 경계 완료
- [x] PAP-11·DEP-R09·fixed 계수·X_cert fail-closed
- [x] 정본·색인·AGENTS/METHODS 동기화
- [x] 전체 unittest·Lean·UTF-8·local links·diff 검증
- [x] 새 timestamp handoff 작성
- [x] 파일명을 `-done.md`로 변경
