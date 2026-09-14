# DEP-R09 FMT filtration 민감도·survivor floor 감사 작업원장

- 시작: 2026-09-14 23:31 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: \(X_{\rm cert}\)를 좁히는 source-first 정규화·증명 연구, 문헌 대조,
  필요한 Lean 형식화와 exact 소규모 검증, 정본·handoff 갱신 및 로컬 staging·commit
- 금지·보류: actual prime sweep, threshold calculator, 장시간 계산, 외부 게시·연락,
  push/PR, <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>
- 선행 상태: 시작 시 <code>main...origin/main [ahead 34]</code>, 작업 트리 clean,
  직전 정본 commit <code>f56a41f</code>, 진행 중 작업원장 없음

## 목적과 완료조건

- 목적: Theory 80의 same-law normalized second-moment gate에 필요한 두 선결조건을
  source-first로 감사한다.
  1. actual FMT final construction을 filtration으로 드러낼 때 한 선택이
     \(m_\omega\), \(C_\chi(\omega)\), \(R(\omega)\), \(M_\omega\)에 주는 변화량.
  2. Theory 55의 survivor lower bound가 같은 joint law·event·endpoint에서
     pointwise \(M_{\min}\)으로 재사용 가능한지 여부.
- 완료조건:
  1. Theory 55·79·80과 FMT/FGKMT 원문의 exact locator·변수·양화사를 고정한다.
  2. 한-coordinate 또는 한-edge 변경의 deterministic sensitivity를 증명 가능한
     식과 불가능하거나 과도한 식으로 분리한다.
  3. bounded-difference·martingale·variance 선행정리가 actual law에 적용되는지
     독립성, 조건부 law, reweighting, numerical rate 관점에서 판정한다.
  4. survivor floor의 pointwise/average, outer/inner event, interval endpoint를
     대조하고 raw-to-normalized moment 사용 가능 여부를 결정한다.
  5. dependency-critical finite 대수만 exact Python·Lean으로 검증하고 analytic
     source theorem을 공리로 넣지 않는다.
  6. Theory·review·machine ledger·색인·METHODS/AGENTS·Lean inventory·handoff를
     동기화하고 전체 검증 뒤 로컬 commit한다.
  7. 기존보다 새로운 bounded \(X_{\rm cert}\) 범위가 생기면 즉시 중단해 사용자에게
     인라인 보고한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | \(G,F,H\)는 변경하지 않고 DEP-R09 joint-law moment 입력만 정밀화 |
| end-bounded 의미론 | 영향 없음 | maximal-gap record와 finite empirical 결과를 읽거나 변경하지 않음 |
| source provenance | 영향 있음 | machine ledger와 theory 색인의 exact PDF·문서 경로·hash를 먼저 고정 |
| 확률·정밀도 | 영향 있음 | final reweighted law를 independent coordinates로 오인하지 않고 pointwise/average를 분리 |
| 승인 경계 | 영향 있음 | 문헌·증명·toy exact 검산만 수행하고 장시간 계산은 새 bounded range 뒤 별도 요청 |
| Lean 증거 | 영향 있음 | finite sensitivity·denominator terminal만 형식화하고 analytic concentration은 OPEN 유지 |
| 문서·재현성 | 영향 있음 | successor theory/review/machine ledger를 새 파일로 만들고 기존 정본은 링크로 동기화 |

## 접근 비교

| 접근 | 정확성 | 비용 | 핵심 위험 | 판정 |
|---|---:|---:|---|---|
| actual filtration의 martingale difference를 직접 감사 | 높음 | 중간~높음 | final hypergraph reweighting이 독립성·bounded increment를 파괴할 수 있음 | 1차 |
| raw second moment와 Theory 55 pointwise floor 결합 | 높음 | 중간 | floor event와 moment law가 다르면 사용 불가 | 1차 병행 |
| 모든 final outcome에 pointwise PAP | 매우 높음 | 매우 높음 | 기존 DEP-R09 상수 병목을 그대로 되살림 | 현재 기각 |
| reserve randomization을 새로 설계 | 불명 | 높음 | coverage와 성공질량을 다시 증명해야 함 | 앞 두 경로 실패 시 |

## 단계 현황

1. **COMPLETE — exact locator·변수·law inventory**
2. **COMPLETE — Theory 55 pointwise survivor floor 재사용 감사**
3. **COMPLETE — actual FMT filtration one-step sensitivity 감사**
4. **COMPLETE — concentration·martingale 선행정리 source screen**
5. **COMPLETE — exact helper·tests·dependency-critical Lean**
6. **COMPLETE — 정본 동기화·전수 검증·handoff·완료 이름 변경·로컬 commit 준비**

## 단계별 기록

### 2026-09-14 23:31 KST — 재개·영향도 분석

- 수행: 직전 commit·handoff·진행 중 원장 부재를 확인하고 Theory 80의 두 다음 gate를
  하나의 의존성 감사로 묶었다.
- 결정: actual filtration과 survivor floor를 병행 감사한다. 둘 중 하나만 닫혀도
  normalized moment는 완성되지 않으므로 과장하지 않는다.
- 문제: Theory 55 파일명을 기억으로
  <code>55_Sono_FMT_H1bCOV2_actual_parameter_sequential_coverage.md</code>라고 추정해
  read-only 조회가 file-not-found로 끝났다. 오류 원장 E129 규칙의 재발이며 파일·과학
  판정 영향은 없다. 이후 좁은 <code>docs/method/theory</code> 목록에서 정확한 경로를
  확정한다.
- 다음 재개점: Theory 55의 실제 파일명과 Theory 79/80 machine ledger source locator를
  고정한 뒤 survivor lower event와 final FMT law를 식 단위로 대조한다.

### 2026-09-14 23:38 KST — 사용자 지적에 따른 Lean 사건 provenance 재감사

- 수행: 인용된 곱 결합형 mismatch를 오류 원장 E117, canonical Lean source,
  <code>git blame</code>, 현재 tracked diff와 대조했다.
- 결과: 새 Lean 실패가 아니라 commit <code>38f50320</code>에서 이미 교정된
  2026-09-13 사건이다. current failure evidence가 없으므로 build를 다시 돌려 새 PASS로
  포장하지 않았다. 과거 사건을 현재처럼 설명한 보고 오류를 E137에 기록했다.
- 예방: AGENTS와 Lean README에 theorem 이름·source diff·현재 명령 종료코드·시각을
  확인한 뒤에만 현재 실패로 보고하는 fail-closed 절차를 추가했다.
- 감사 중에는 추정 경로와 Windows wildcard를 함께 쓴 read-only E129 유형도 재발해
  E138로 공개했다. 파일·Lean proof·과학 판정에는 영향이 없다.
- 다음 재개점: 원래 단계 1로 돌아가 Theory 55의 exact event와 Theory 79/80의 final
  FMT law를 식 단위로 대조한다.

### 2026-09-14 23:55 KST — 재발 방지 규칙 검증·보조 오류 공개

- 확인: canonical theorem은 commit <code>38f50320</code>에서 생성될 때부터
  <code>simpa [mul_assoc, mul_left_comm, mul_comm]</code>를 포함하며, 현재 source diff와
  새 failing compile 증거는 없다. 판정은 <code>HISTORICAL_ALREADY_FIXED</code>다.
- 조치: 오류 원장 E137, AGENTS, Lean README의 현재-사건 provenance gate를 서로
  대조했고 <code>git diff --check</code>가 통과했다. source가 바뀌지 않았으므로 과거
  사건을 새 PASS로 포장하기 위한 불필요한 Lean rebuild는 실행하지 않았다.
- 추가 공개: 후속 source 감사에서 broad <code>tmp</code> 검색(E139)과 선택적
  <code>pypdf</code>/<code>sympy</code> 의존성 가정(E140)이 발생했다. 모두 읽기 전용이며
  파일·증명·과학 판정에 영향이 없다. exact locator와 기존 native-text/표준 라이브러리
  경로로 전환했다.
- 다음 재개점: 원래 단계 1의 Theory 55 exact event 대조로 돌아간다.

### 2026-09-15 00:10 KST — Theory 81 수학 판정·exact 검증·Lean 완료

- source 대조: FMT printed p.13 formula (6.17)과 FGKMT printed pp.83--84
  formulas (5.1), (5.7)--(5.9)를 native text 우선으로 읽고 원본 page image와 대조했다.
- denominator 보정: Theory 55 formula (55.38)의 floor는 outer-good (O)가 아니라
  final (S_{\rm sieve}=O\cap I_{\rm good})에서만 성립한다. 같은 event indicator로 raw
  moment와 normalization을 다시 맞췄다.
- sensitivity 판정: one-prime residue 변경의 survivor symmetric difference·count는
  (2\lceil N/p\rceil) 이하임을 증명했다. 그러나 exact (P=65) nonprincipal-character
  fixture에서 character 합 변화 3이 membership bound 2보다 커, count-to-phase 전이를
  반례로 기각했다.
- literature 판정: Freedman, Warnke, Kontorovich--Ramanan, Combes 경로는 increment,
  conditional variance, Lipschitz 또는 mixing 입력을 별도로 요구한다. actual FMT law에
  numerical drop-in은 식별하지 못했다.
- 구현·시험: 새 exact helper·machine ledger·11개 단위시험을 작성했다. py_compile과
  11/11 tests가 PASS했다.
- Lean: dependency-critical terminal 5개를 단일 canonical 파일에 추가했다. direct compile
  exit 0, 전체 <code>lake build</code> exit 0과 8,765 jobs 성공을 확인했다. 금지 proof
  escape는 0건이다.
- inventory: 82 theory 문서, 1,499식, 293 declarations,
  <code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=66</code>,
  <code>NOT_YET_FORMALIZED=1031</code>, validator PASS다.
- 절차 오류: validator가 <code>--help</code>를 지원한다고 추정해 generator 전 stale
  inventory 실패를 한 번 만들었다. E141에 기록하고 올바른 순서로 재실행했다.
- 현재 판정: denominator domain은 닫혔지만 martingale increment·conditional variance와
  actual same-law moment는 OPEN이다. PAP-11, DEP-R09, fixed (2\times10^{-17}),
  numerical (X_{\rm cert})는 OPEN이고 새 bounded range·장시간 계산 절차는 없다.
- 다음 재개점: 정본 링크·text integrity·전체 unittest를 검증하고 새 handoff를 만든 뒤
  원장을 <code>-done</code>으로 바꾸고 로컬 commit한다.

### 2026-09-15 00:17 KST — 전수 회귀검증·오류 재발 방지 동기화 완료

- 전체 unittest는 정상 로컬 권한에서 891/891 PASS, 74.460초, exit code 0이었다.
- Lean verification ledger를 마지막 문서 상태에서 다시 생성했고 82 theory 문서,
  1,499식, 293 declarations, <code>KERNEL_PASS=94</code>,
  <code>CONDITIONAL_KERNEL_PASS=66</code>,
  <code>NOT_YET_FORMALIZED=1031</code>, 금지 proof escape 0건을 확인했다.
- integrated validator는 local Markdown link 1,584개, text-integrity issue 0,
  exit code 0으로 끝났다. 변경 JSON 4개도 모두 parse PASS다. staging 전 tracked-only
  <code>git diff --check</code>는 exit code 0이었지만 untracked 새 파일을 포함하지 않았다.
  staging 뒤 cached 검사가 Theory 81의 후행 공백 2곳을 발견해 교정했고, 이를 E142로
  기록했다. 최종 gate는 재실행한 <code>git diff --cached --check</code>다.
- 사용자가 인용한 곱 결합형 사건은 새 오류가 아니라 E117의 과거 사건임을 E137,
  AGENTS, Lean README와 canonical theorem source에서 교차 확인했다. 현재 proof는 commit
  <code>38f50320</code>부터 명시적 <code>simpa [mul_assoc, mul_left_comm, mul_comm]</code>를
  포함한다.
- E142 후 Theory 81 source byte가 바뀌었는데 generator 없이 validator를 다시 호출해
  stale inventory가 정상 거부됐다. E141의 수동 순서 규칙만으로 부족했음을 E143으로
  기록하고 generator→validator를 한 호출로 강제하는 wrapper를 추가했다. wrapper는
  py_compile과 실제 실행에서 <code>sequence=generate_then_validate</code>, 최종 exit code
  0을 확인했다.
- 최초 local commit 뒤 locator 검사에서 handoff의 닫힌 오류 범위가 E141에 머문 것을
  발견했다. E144로 기록하고 <code>E137 이후 최신 항목</code>으로 바꿔 amend 대상으로
  staging한다. 첫 동기화 multi-file patch는 원장 문맥 불일치로 원자적으로 거부돼 E145에
  기록했으며 exact locator를 확인한 작은 patch로 교정했다.
- 다음 재개점: 새 timestamp handoff를 보존하고 이 원장을 <code>-done</code>으로 이름
  변경한 뒤 명시적 변경파일만 staging·local commit하고 post-commit 정합성까지 확인한다.

## 현재 재개점

새 timestamp handoff와 완료 원장을 보존하고 post-commit 정합성·clean worktree를 확인한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 analytic source theorem 상태 분리
- [x] 정본·색인·METHODS/AGENTS·Lean inventory 동기화
- [x] 새 timestamp handoff 작성
- [x] <code>git diff --check</code>와 참조 경로 확인
- [x] 파일명을 <code>-done.md</code>로 변경
