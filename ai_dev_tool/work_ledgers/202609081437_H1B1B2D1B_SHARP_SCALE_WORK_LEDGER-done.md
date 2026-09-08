# H1b-1b-2d.1b sharp xi log x scale 작업원장

- 시작: 2026-09-08 14:37 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: 권장 순서에 따른 H1b-1b-2d.1b 문헌 추적, 수학적 정식화, 데이터 비의존 코드·시험, 정본 동기화
- 금지·보류: 실제 prime/maximal-gap sweep, P018-B 실행, threshold calculator 구현, 패키지·Lean 설치, commit/push/PR
- 선행 변경: 시작 시 git status --short 출력 0건; 이번 작업 시작 전 worktree clean

## 목적과 완료조건

- 목적: Maynard Proposition 6.1 증명에서 x^xi 절단을 쓰는 source lines 1096, 1135의 두 sharp summatory 호출을 유한 수치 부등식으로 복원한다.
- 완료조건: 원문 호출·가정·변수 정규화를 확정하고, 적합한 선행정리를 우선 검토하며, 닫히는 범위와 남는 blocker를 문서·기계검증 계약·시험에 반영하고 정본과 handoff를 동기화한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | xi log x를 log R 또는 Lambda_*와 혼동하지 않고 두 실제 호출을 별도 추적한다. |
| 데이터·provenance | NONE | 실제 dataset과 actual artifact를 생성·변환하지 않는다. 원문 PDF/TeX의 source 위치와 hash를 기록한다. |
| 통계·정밀도 | MEDIUM | 부동소수 근사만으로 증명하지 않고 exact/rational 또는 방향 보존 고정밀 검산을 사용한다. |
| 승인 경계 | CONTROLLED | 문헌·증명·toy 검증만 수행하며 heavy/actual 계산과 설치는 하지 않는다. |
| 산출물·비덮어쓰기 | HIGH | 새 번호 문서와 v1 JSON을 만들고 기존 정본은 증거 수준만큼만 갱신한다. |

## 단계 현황

1. **COMPLETED — source call·정의·기존 dependency 감사**
2. **COMPLETED — 선행정리·교정본·후속 문헌 적합성 조사**
3. **COMPLETED — finite sharp-scale lemma와 기계검증 계약 정식화**
4. **COMPLETED — targeted/full 검증과 정본 동기화**
5. **COMPLETED — handoff·권장 순서·커밋 제안 및 완료 처리**

## 단계별 기록

### 2026-09-08 14:37 KST — 착수·영향도 고정

- 수행: 최신 handoff와 작업원장 규약을 확인하고 승인·금지 경계와 5단계 계획을 고정했다.
- 파일: 이 작업원장
- 명령·검증: git status --short; 활성 WORK_LEDGER 검색; 최신 handoff 이름 확인
- 결과: worktree clean, 활성 원장 0개, 최신 handoff는 202609081324_HANDOFF.md.
- 문제·결정: parent H1B-L84나 SIV-07은 두 sharp 호출만으로 자동 승격하지 않는다.
- 다음 재개점: tmp/pdfs/h1b1b/maynard_source/Subsets.tex lines 1044--1168과 xi 정의 및 기존 24/26번 이론 문서를 대조한다.

### 2026-09-08 — source·출판본·실제 FMT 호출 대조 완료

- 수행: Maynard author TeX 1044--1141행, 최종 출판본 1547--1550쪽, FGKMT/FMT 최종본 98--99쪽, 공식 arXiv v2/v3 metadata를 대조했다.
- 증거: 최종 출판본 Proposition 9.4는 `k(log log x)^2/log x << xi`로 숨은 상수를 남기지만 author TeX/arXiv HTML은 계수 1의 부등식으로 표시된다. 최종 출판본을 우선한다.
- 실제 호출: FGKMT/FMT Theorem 6의 (7.8)은 Maynard Proposition 9.4에 `xi=theta/10`, `D=1`을 넣으며, Theorem 5 적용은 `alpha=2`, `theta=1/3`, `R=(x/4)^(theta/3)`을 쓴다.
- 적합성 판정: 숨은 Vinogradov 상수를 1로 가정하지 않는다. Maynard proof에서 xi 하한을 쓰는 곳은 (9.58)과 (9.66)의 두 sharp 합뿐이므로, 교정된 project summatory theorem을 strict cutoff `d<z`에 직접 적용해 두 곳을 재증명한다.
- 교정 발견: strict cutoff 오차는 `C_Sigma`가 아니라 theory 22의 endpoint allowance를 포함한 `C_Sigma+2`다. 기존 `sharp_cutoff_relative_error` 구현과 theory 24 식 (24.16)을 함께 고쳐야 한다.
- 닫을 목표: `s=xi log x >= (3/10)log R`, `delta=(C_Sigma+2)(6+log Lambda_star)/s <= 1/2`이면 (9.58)의 양의 하한과 (9.66)의 sharp upper factor를 동시에 닫는다.
- 닫지 않는 범위: Proposition 9.4의 다른 negligible-error 상수, Lemmas 8.5--8.6, 전체 moment budget, Hypothesis 1, `SIV-07/SIV-09`, `X_cert`.
- 설치·실험: 새 PDF나 package를 받지 않았고 실제 prime 계산을 수행하지 않았다.
- 다음 재개점: strict multiplier helper와 sharp-scale certificate를 구현하고, closed-form `log R` 충분조건을 exact/algebraic test로 검증한다.

### 2026-09-08 — finite lemma·구현·기계 계약 완료

- 수행: strict cutoff endpoint allowance `C_Sigma+2`, exact FGKMT/FMT scale `xi log x >= (3/10)log R`, 두 sharp 호출의 공통 finite gate를 정식화했다.
- 신규 파일: theory 27, review 33, `source/h1b1b2d1b_sharp_scale.py`, sharp-scale JSON contract, 전용 회귀시험.
- 교정 파일: corrected-Wirsing helper에 strict multiplier를 추가하고 기존 `sharp_cutoff_relative_error`도 strict multiplier를 사용하도록 수정했다.
- 정본 반영: r-fold, H1b, H1, T1 JSON 계약에서 `H1B-L84`만 actual-input parameterized explicit으로 승격하고 `H1B-COMP-01`, `SIV-07/09`, `X_cert`는 그대로 열어 두었다.
- 검증: FGKMT Python으로 관련 6개 test module 38 tests PASS.
- 다음 재개점: 사람이 읽는 이론 색인, H1b/H1/T1 문서, METHODS, AGENTS를 같은 증거 수준으로 동기화한 뒤 전체 unittest와 diff/reference 감사를 수행한다.

### 2026-09-08 — 정본 동기화·회귀검증 완료

- 수행: 이론 색인, H1b/H1/T1 문서와 JSON, `docs/METHODS.md`, `AGENTS.md`를 새 sharp-scale 판정과 동기화했다.
- 상태 경계: 두 sharp 호출과 Lemma 8.4 관련 actual subapplication 9/9만 parameterized explicit으로 닫았다. `H1B-COMP-01`, `SIV-07`, `SIV-09`, `X_cert`는 계속 열려 있다.
- 관련 검증: 고정 FGKMT Python으로 `py_compile` PASS, 관련 7개 module 42 tests PASS, 모든 theory JSON 17개 strict parse PASS.
- 전체 검증: 최초 sandbox 실행의 82개 `PermissionError`는 임시 디렉터리 쓰기 권한 문제였다. 의도적 source 수정 때문에 드러난 source-hash 불일치 1건은 새 SHA-256으로 교정했다. 사용자가 기존에 허가한 정상 로컬 권한에서 전체 suite를 재실행해 `Ran 307 tests in 41.279s / OK`를 확인했다.
- 최종 재검: 관련 42 tests를 다시 실행해 `OK`, `git diff --check` exit 0을 확인했다. Git의 LF→CRLF 알림만 있었고 whitespace error는 없었다.
- 실제 수행 경계: prime/maximal-gap 계산, P018-B, threshold calculator, 설치, commit/push/PR은 수행하지 않았다.
- 다음 재개점: 새 timestamp handoff를 작성하고 이 원장의 완료 점검을 닫은 뒤 `-done`으로 이름을 바꾼다.

### 2026-09-08 15:38 KST — 핸드오프·마무리 완료

- 수행: `handoff/202609081538_HANDOFF.md`를 새 파일로 작성했다.
- 포함: 결론, 쉬운 설명, 문헌 우선 판정, strict `+2` 교정, 검증 증거, 비실행 경계, 다음 권장 순서·예상시간·사용자 절차, 한국어 커밋 메시지.
- 사용자 요청: 현재 설치나 사용자 계산은 필요 없다. 다음 직접 축은 H1b-2a 잔여 Lemmas 8.5--8.6과 Proposition 9.4 오차 source map이다.
- 완료 판정: 요청 산출물·검증·정본 동기화·handoff가 모두 완료됐으므로 원장을 `-done`으로 바꿀 수 있다.

## 현재 재개점

완료. 다음 세션은 `handoff/202609081538_HANDOFF.md`의 1순위부터 재개한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] git diff --check와 참조 경로 확인
- [x] 파일명을 -done.md로 변경
