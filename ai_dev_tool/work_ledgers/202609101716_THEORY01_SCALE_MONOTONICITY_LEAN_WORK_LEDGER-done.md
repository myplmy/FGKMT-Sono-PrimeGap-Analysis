# Theory 01 scale·interval minimum Lean 형식검증 작업원장

- 시작: 2026-09-10 17:16 KST
- 현재 상태: COMPLETE
- 사용자 승인: 최신 handoff의 권장 1순위인 Theory 01의 양의 정의역, FGKMT scale 단조성,
  end-bounded plateau interval minimum을 기존 단일 Lean 파일에서 형식화·검증
- 금지·보류: `sorry`, `admit`, project-local `axiom`, 검증되지 않은 외부 정리의 무표시 도입,
  package upgrade, actual prime 계산, threshold calculator, push/PR
- 강제 중단 조건: 위 proof escape가 불가피해 보이거나, 새 외부 analytic theorem을 가정해야만
  진행할 수 있거나, 설치·다운로드·장시간 연산이 필요하면 이유와 대안을 사용자에게 먼저 보고
- 선행 상태: 시작 HEAD `a891db481aa92327d46f199a1728252faa830b11`, branch `main`,
  `git status --short` 출력 0건. 초기 Lean 원장은 1,005행 중 KERNEL_PASS 9,
  CONDITIONAL_KERNEL_PASS 8, DEFINITION_ONLY 4, PARTIAL 6, 미형식화 973, parse review 5다.

## 목적과 완료조건

- 목적: Theory 01의 `F(x)`가 필요한 양의 scale 구간에서 증가한다는 사실과, gap이 일정한
  end-bounded 정수 plateau에서 `gap/F(x)`의 최소가 다음 end prime 직전이라는 결론을
  Lean 커널이 검사하도록 만든다.
- 완료조건:
  1. Mathlib에 이미 증명된 log·division 단조성 정리를 먼저 조사하고 적용 범위를 확인한다.
  2. `Real.log`의 total-function 성질과 연구용 양의 domain을 명시적으로 분리한다.
  3. 기존 `lean/FGKMTSono/TheoryVerification.lean` 한 파일에 theory/formula 주석과 함께 추가한다.
  4. `sorry`, `admit`, project-local `axiom` 0건을 validator와 source scan으로 확인한다.
  5. direct Lean, Lake build, 원장 coverage, 관련·전체 Python 회귀가 통과한다.
  6. 독립 kernel proof와 premise를 받는 conditional composition을 원장에서 구분한다.
  7. 새 timestamp handoff와 오류 원장을 동기화하고 exact allowlist로 로컬 commit한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | 반복 자연로그 정의와 end-prime plateau를 바꾸지 않고 domain 가정을 별도 명제로 둔다. |
| 데이터·provenance | 영향 없음 | dataset·`test_result`를 읽거나 쓰지 않는다. theory source SHA와 원장 ID를 재검증한다. |
| 통계·정밀도 | 영향 없음 | symbolic proof만 수행하며 decimal 근사나 empirical 결과를 쓰지 않는다. |
| 승인 경계 | 영향 있음 | 사용자 승인 범위의 Lean proof만 수행하고 proof escape 필요 시 즉시 중단한다. |
| 재현성 | 영향 있음 | 고정 Lean/Mathlib에서 direct build·generator·validator를 모두 실행한다. |
| 증거 수준 | 핵심 | `F` 자체 단조성과 interval-minimum 합성을 각각 독립/조건부로 명시한다. |

## 단계 현황

1. **COMPLETE — Theory 01 원문·현재 Lean·Mathlib 선행 정리 감사**
2. **COMPLETE — domain과 monotonicity statement 설계·영향도 확정**
3. **COMPLETE — 단일 Lean 파일 구현과 전수 상태 원장 갱신**
4. **COMPLETE — kernel·coverage·회귀·정적 검증**
5. **COMPLETE — 오류 원장·handoff·로컬 commit 준비**

## 단계별 기록

### 2026-09-10 17:16 KST — 착수·승인 경계 고정

- 수행: 최신 handoff, 시작 HEAD·worktree와 적용 skill을 확인하고 본작업 전에 새 원장을 만들었다.
- 결과: clean worktree에서 시작했고, actual 계산이나 외부 다운로드는 없다.
- 다음 재개점: Theory 01 원문·inventory 행과 Mathlib의 log/iterated-log monotonicity API를 읽는다.

### 2026-09-10 17:31 KST — 선행 정리 감사·statement 설계·scratch kernel 확인

- 선행 정리: 고정 Mathlib에서 `Real.log_lt_log`, `Real.log_pos`, `Real.exp_log`,
  `Real.add_one_lt_exp`를 확인했다. 필요한 보조명제 `exp(t)/t`의 `[1,∞)` strict monotonicity는
  이 정리들과 ordered-field 대수만으로 직접 증명할 수 있어 새 외부 analytic 가정이 필요 없었다.
- domain 설계: Lean `Real.log`의 total-function junk branch를 연구 domain으로 오인하지 않도록
  실수 경계를 `scaleThreshold = exp(exp(exp(1)))`로 정의했다. 이 경계보다 큰 `x`에서는
  `x`, `log_1 x`, `log_2 x`, `log_4 x`가 양수이고 `log_3 x>1`임을 커널 명제로 둔다.
- 수치 경계 대조: 고정 FGKMT Python 100 dps에서 실수 경계는
  `3814279.104760220592209...`, ceiling은 `3814280`임을 확인했다. 이 decimal 계산은
  Lean kernel proof가 아니므로 status를 부풀리는 데 쓰지 않는다.
- scratch 결과: factorization, positivity, strict monotonicity, plateau right-end minimum proof가
  `sorry`/`admit`/`axiom` 없이 direct Lean을 통과했다. 임시 scratch는 정본 반영 뒤 제거했다.
- 정본 반영: 모든 선언을 기존 단일 파일 `lean/FGKMTSono/TheoryVerification.lean`의
  Theory 01 절에 넣었다. direct Lean 정본 실행은 오류 출력 없이 종료했다.
- 다음 재개점: Theory 01 문서에 kernel 경계와 decimal/커널 증거 경계를 명시하고,
  formula status JSON과 생성 원장을 동기화한다.

### 2026-09-10 17:39 KST — 정본·전수원장 동기화와 검증 완료

- 정본 선언: `scaleThreshold`, `exp_div_self_strictMonoOn`, `scale_domain_chain`,
  `fgkmtScale_factorization`, `iterLog_strictMono_up_to_four`, `fgkmtScale_pos`,
  `fgkmtScale_strictMonoOn`, `intervalMinimum_is_minimum`을 단일 Lean 파일에 추가했다.
- 증거 수준: `T01-U001`은 기존 `KERNEL_PASS`를 유지하되 정의뿐 아니라 domain·양수성·단조성
  선언을 연결했다. `T01-U005`만 `DEFINITION_ONLY -> KERNEL_PASS`로 올렸다.
  `T01-U004`의 실제 finite-record `G_end(x)=g_i` 상수성은 아직 전수 records 논리로 닫지 않아
  `PARTIAL_FORMALIZATION`을 유지했다.
- 문서: Theory 01에 연속 kernel 경계와 100-dps integer-ceiling 대조의 증거 차이를 명시했다.
- 기계 원장: generator 재실행 뒤 수식 1,005개, theory 56개를 유지했고 validator는
  declaration 46개, local link 1,064개, banned escape 0건으로 PASS했다. 상태 집계는
  KERNEL_PASS 10, CONDITIONAL 8, DEFINITION_ONLY 3, PARTIAL 6, NOT_YET 973,
  PARSE_REVIEW_REQUIRED 5다.
- Lean: direct `lake env lean FGKMTSono\\TheoryVerification.lean` exit 0,
  `lake build FGKMTSono` 8,765 jobs PASS다.
- Python: 표적 16 tests PASS. 사용자 기허가 범위의 sandbox 외부 전체 suite는
  664 tests, 92.365초, exit 0으로 PASS했다.
- proof escape: validator의 comment/string 제거 후 실행부 검색에서
  `sorry`/`admit`/project-local `axiom` 0건이다.
- 다음 재개점: 실제 발생한 scratch/도구 실패를 오류 원장에 기록하고 최종 링크·diff·handoff를
  검사한 뒤 정확한 allowlist만 로컬 commit한다.

### 2026-09-10 17:47 KST — 오류 공개·handoff·최종 정적검사

- 오류 원장 E083에 scratch 표현 불일치, PATH 추정, 장시간 process exit 회수,
  verbose 출력 절단과 재검증을 기록했다. 모두 정본 commit 전에 교정됐고
  actual 결과 오염은 없다.
- `AGENTS.md`와 Lean README에 `sorry`/`admit`/project-local `axiom`이 불가피해
  보이면 이유·대안·외부 보장을 감사해 사용자에게 먼저 보고하고, 명시적
  허가 전에는 절대 사용하지 않는 규칙을 고정했다.
- 새 handoff `handoff/202609101743_HANDOFF.md`를 작성했다.
- generator 재실행 전후 inventory·Markdown 원장 hash는 각각 동일했다.
- 변경 text 12개의 strict UTF-8·control character 검사 issue 0,
  handoff/Lean README local link issue 0, `git diff --check` PASS다.
- 정확한 이번 작업 경로만 stage해 로컬 commit하고 push/PR은 하지 않는다.
- 후속 재개점: Theory 55의 55.24–55.35 smooth remainder를 source/Mathlib 선행
  proof와 대조해 exact algebra와 analytic premise로 분리한다.

## 현재 재개점

완료. 후속은 `handoff/202609101743_HANDOFF.md`의 우선순위 1에서 시작한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·중단·proof-escape 금지 경계 명시
- [x] 독립/조건부 kernel PASS 상태 분리
- [x] 원장·README/AGENTS·handoff 정합성
- [x] direct Lean·Lake·validator·Python 회귀 PASS
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 local link 확인
- [x] 파일명을 `-done.md`로 변경
