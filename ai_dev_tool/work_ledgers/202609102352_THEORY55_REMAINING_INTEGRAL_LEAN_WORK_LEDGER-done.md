# Theory 55 잔여 적분·Stieltjes Lean 검증 작업원장

- 시작: 2026-09-10 23:52 KST
- 현재 상태: COMPLETE
- 사용자 승인: 직전 Theory 55 batch에서 남은 식 (55.26), (55.27), (55.28)의
  Lean 검증을 우선 마무리
- 금지·보류: `sorry`, `admit`, project-local `axiom`, 외부 analytic premise를 독립
  `KERNEL_PASS`로 위장, actual prime 계산, dataset·`test_result` 변경, dependency upgrade,
  threshold calculator, push/PR
- 강제 중단 조건: proof escape가 필요하거나 새 dependency 설치·폐쇄 원문·장시간 계산이
  필수인 경우 근거와 대안을 먼저 보고하고 사용자 허가 전 중단
- 선행 상태: branch `main`, clean worktree, 시작 HEAD
  `313a2bfaa13efb1432476d3c3d0c6ae6b3349415`

## 목적과 완료조건

- 목적: Theory 55 smooth remainder의 남은 integral/Stieltjes 경계를 source-first로 조사하고,
  고정 Mathlib에서 가정 없이 증명 가능한 부분을 단일 Lean 파일에 추가한다.
- 완료조건:
  1. 원문 (55.26)--(55.28), Rosser--Schoenfeld source, Mathlib 관련 정리를 대조한다.
  2. (55.26)의 scalar 적분 항등식과 (55.28)의 두 finite-interval comparison을 가능한 한
     전체 커널 검증한다.
  3. (55.27)은 drop-in source formalization 여부를 먼저 조사하고, 없으면 exact finite/measure
     child와 남은 source blocker를 분리한다.
  4. 모든 선언은 `lean/FGKMTSono/TheoryVerification.lean` 하나에만 둔다.
  5. 상태 JSON·전수 원장·README/review를 실제 증거 수준과 동기화한다.
  6. direct Lean, full Lake, validator, 표적·전체 회귀, proof escape 0건을 확인한다.
  7. 오류 원장·새 handoff를 작성하고 exact allowlist만 로컬 commit한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | 원문 변수·적분 구간·strict/non-strict 방향을 그대로 보존한다. |
| 반복로그·end-bounded 의미 | 영향 없음 | Theory 01과 empirical 정의를 수정하지 않는다. |
| 데이터·provenance | 영향 없음 | symbolic proof만 수행하고 dataset·actual artifact를 사용하지 않는다. |
| 수치·통계·그래프 | 영향 없음 | exact real inequalities만 다루고 경험적 결과를 재계산하지 않는다. |
| 승인 경계 | 영향 있음 | 형식증명·문서·로컬 검증/commit만 수행한다. |
| 증거 수준 | 핵심 | source theorem premise와 독립 kernel proof를 상태상 분리한다. |
| 재현성 | 영향 있음 | 고정 Lean/Mathlib, 단일 target, inventory/status/ledger를 함께 검증한다. |

## 단계 현황

1. **COMPLETE — 원문·선행 source·Mathlib theorem inventory**
2. **COMPLETE — (55.26) 적분 항등식 형식화**
3. **COMPLETE — (55.28) finite-interval comparison 형식화**
4. **COMPLETE_WITH_SOURCE_BOUNDARY — (55.27) Stieltjes exact child·source blocker 분리**
5. **COMPLETE — 상태·문서 동기화와 전체 검증**
6. **COMPLETE — 오류 원장·handoff·로컬 commit**

## 단계별 기록

### 2026-09-10 23:52 KST — 착수

- 수행: 최신 handoff와 완료 Theory 55 원장을 읽고 clean HEAD와 사용자 승인 범위를 확인했다.
- 결과: 현재 상태는 55.26/55.28 `PARTIAL_FORMALIZATION`, 55.27
  `SOURCE_THEOREM_UNFORMALIZED`이다. `X_cert`와 R09--R12는 OPEN으로 고정한다.
- 다음 재개점: 원문 55.26--55.28과 고정 Mathlib의 const-rpow derivative,
  interval-integral comparison, finite sum/measure partial summation 정리를 조사한다.

## 현재 재개점

요청 산출물·형식검증·회귀·문서·handoff·완료 이름 변경이 모두 끝났다.
다음 작업은 최신 handoff의 DEP-R09 우선순위를 따라 새 작업원장에서 시작한다.

### 2026-09-11 00:32 KST — source·Mathlib inventory 완료

- 수행: theory 55 (55.26)--(55.28)과 고정 Mathlib의
  `NumberTheory/Chebyshev.lean`, Abel summation 정리를 대조했다.
- 결과: Mathlib에 `Chebyshev.theta`와 Abel summation 기반은 있지만 즉시 사용할 수
  있는 theta 상계는 `theta_le_log4_mul_x`이며, 필요한 Rosser--Schoenfeld
  `theta(t) < 1.01624 t` drop-in theorem은 없다.
- 결정: 55.27의 source theta 상계와 감소 kernel Stieltjes/Abel 비교는
  외부 premise로 남겨 `PARTIAL_FORMALIZATION`으로 표시한다.

### 2026-09-11 00:36 KST — (55.26), (55.28) 커널 검증 완료

- 파일: `lean/FGKMTSono/TheoryVerification.lean`.
- (55.26): `smoothStieltjesKernel_integral`이 `t>0`, `t!=1`에서 const-rpow
  미분과 interval FTC로 exact identity를 증명한다.
- (55.28): `expm1DivContinuous`로 0의 removable singularity를 처리하고 AE equality,
  두 finite interval comparison, improper exponential moment, `51/50`, `103/100`을 증명했다.
- 추가 강화: (55.29)는 Ein bound를 외부 premise로 받지 않고
  `smoothEin_upper_bound`를 내부 호출하도록 수정했다.
- 검증: `lake env lean FGKMTSono\\TheoryVerification.lean` exit 0, 경고 0.

### 2026-09-11 00:39 KST — (55.27) 정확한 완료 경계

- 검증: endpoint extension `h(1)=delta`, prime term·finite prime sum 정규화,
  exact decimal inequality `1.01624 < 21/20`, Ein 종단 치환.
- 미완료: Rosser--Schoenfeld theta 상계 자체와 그를 쓰는 Stieltjes/Abel
  비교. 이는 theorem premise로 눈에 보이게 보존했다.
- proof escape: `sorry`, `admit`, project-local `axiom` 0건.

### 2026-09-11 00:47 KST — 상태 동기화·형식 검증

- 생성기: theory 56, formula 1,005, recovery 5, `GENERATED`.
- validator 최종: declaration 87, local link 1,064, banned escape 0,
  `KERNEL_PASS=15`, `CONDITIONAL_KERNEL_PASS=14`, `PARTIAL_FORMALIZATION=7`, PASS.
- 첫 validator는 `@[simp] theorem smoothStieltjesKernelExtended_one`을 선언 정규식으로
  인식하지 못해 실패했다. 증명에 불필요한 attribute를 제거한 뒤 direct Lean과
  validator를 다시 PASS했다.
- direct Lean: exit 0, 경고 0.
- Lake: `Build completed successfully (8765 jobs)`.
- `py_compile`: 생성기·validator PASS.
- COV2 표적 unittest: 19/19 PASS.
- 전체 unittest: sandbox 실행은 임시폴더 권한으로 82 errors이며 무효.
  정상 로컬 권한 재실행은 664/664 PASS, 74.349초.
- sandbox test가 workspace `tmp` 하위에 남긴 임시폴더 16개는 절대경로
  검증 후 정상 로컬 권한으로 제거했다. 첫 sandbox 제거 시도의 실패 요약은
  성공 증거로 세지 않았다.
- strict UTF-8/control character: 12파일 issue 0; JSON parse status 45/inventory 1,005.

### 2026-09-11 00:51 KST — 문서·오류 원장·handoff 동기화

- 갱신: `lean/README.md`, `AGENTS.md`, `docs/METHODS.md`, theory 55, review 62,
  오류 원장 E085.
- 새 handoff: `handoff/202609110051_HANDOFF.md`; 기존 handoff를 덮어쓰지 않았다.
- 경계: (55.27) source theorem, R09--R12, broad SIV, `X_cert` OPEN을 모든
  정본에서 유지했다.
- 다음: 완료 이름 변경, final allowlist stage, local commit.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행·proof-escape 경계 명시
- [x] exact/conditional/open 증거 수준 분리
- [x] 원장·README/AGENTS·review·handoff 정합성
- [x] direct Lean·Lake·validator·Python 회귀 PASS
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`·링크·strict UTF-8 확인
- [x] 파일명을 `-done.md`로 변경
