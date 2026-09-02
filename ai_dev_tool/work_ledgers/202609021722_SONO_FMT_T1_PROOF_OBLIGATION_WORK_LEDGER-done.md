# Sono/FMT T1 proof-obligation 원장 작업원장

- 시작: 2026-09-02 17:22 KST
- 현재 상태: COMPLETE
- 사용자 승인:
  - P020 figure 사용자 시각 QA PASS 반영
  - Sono/FMT T1 proof-obligation 원장 작성
  - 앞서 합의한 권장 순서에 따라 hard-node 타당성 판정까지 진행
- 금지·보류:
  - 알 수 없는 상수·유효범위를 임의 숫자로 채우지 않음
  - numerical `X_cert` 계산기, P018-B, P013-C, P019 actual 미실행
  - 새 prime sweep·dataset 변경·패키지 변경 미수행
  - 외부 게시, commit, push, PR 미수행
- 시작 상태:
  - `git status --short` 출력 없음; 작업 시작 시 clean worktree
  - 최신 handoff `handoff/202609021207_HANDOFF.md`
  - 선행 감사 `docs/review/22_20260902_Sono_FMT_numerical_threshold_proof_dependency_audit.md`

## 목적과 완료조건

- 목적 1: Sono의 최종 k=1 부등식까지 필요한 모든 직접 proof edge를 source/page/equation 단위로
  등록한다.
- 목적 2: 각 asymptotic·implicit 조건을 `EXPLICIT`, `PARTIAL`, `RATE_MISSING`,
  `SOURCE_REVIEW_REQUIRED`, `HARD_BLOCKER`로 분류한다.
- 목적 3: FMT/Maynard hard node가 공개 원문만으로 수치화 가능한지, 추가 정량 lemma 재증명이
  필요한지 판정한다.
- 목적 4: P020 사용자 시각 QA를 결과보고서·계획·색인·METHODS·AGENTS에 증거 그대로 반영한다.
- 완료조건:
  - 누락 점검 가능한 T1 Markdown 원장과 machine-readable 표
  - dependency graph와 critical path
  - hard-node feasibility 판정 및 다음 gate
  - 정본 동기화·검증·새 handoff
  - 작업원장 `-done` 전환

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded 정의 | 변경 없음 | threshold 세 수준과 k=1 경계만 참조 |
| dataset·provenance | 변경 없음 | local 논문·기존 결과만 읽고 새 prime 계산 금지 |
| 증명 정확성 | 중요 | 원문 페이지·정리·식과 inequality 방향을 각 행에 기록 |
| 수치 정밀도 | 이번 T1의 계산 대상 아님 | 누락 상수를 0 또는 1로 가정하지 않음 |
| 승인 경계 | 문헌·문서 감사 승인 | threshold calculator·actual computation은 별도 gate |
| 재현성 | 중요 | source file hash·schema·status vocabulary와 검증 체크 기록 |
| 경험·정리 구분 | 중요 | `X_emp`, `X_cert`, `X_star`를 섞지 않음 |

## 단계 현황

1. **COMPLETED — 상태·원문·스키마 고정과 P020 QA 반영**
2. **COMPLETED — Sono Sections 3–6 proof obligation 전수 추출**
3. **COMPLETED — FMT direct dependency와 Maynard hard node 추적**
4. **COMPLETED — T1 정본 원장·machine-readable 표·critical path 작성**
5. **COMPLETED — hard-node feasibility·다음 연구 gate 판정**
6. **COMPLETED — 정본 동기화·검증·handoff·커밋 메시지 제안**
7. **COMPLETED — 작업원장 `-done` 전환**

## 단계별 기록

### 2026-09-02 17:22 KST — 시작 상태와 승인 경계 복원

- 수행:
  - 최신 AGENTS 지시, handoff, 1차 threshold 감사 확인
  - `impact-analysis`, `plan-doc`, `check-and-verify`, `log-to-result`, `session-handoff`, PDF 절차 확인
  - memory의 threshold 세 수준 구분을 현재 문서와 재대조
- 결과:
  - P020 사용자 시각 QA PASS가 새 외부 증거
  - T1과 hard-node 판정은 승인됨
  - threshold 수치 계산·새 prime 계산은 승인 범위 밖
- 다음 재개점: P020 visual QA 상태를 최소 범위로 반영하고 T1 schema·source hash를 고정

### 2026-09-02 17:28 KST — P020 사용자 시각 QA 반영

- 증거: 사용자가 `P20 figure 문제 없음`으로 회신
- 갱신: AGENTS, METHODS, P020 계획·결과보고서·결과 색인, recurrence 방법론·이론 색인
- 통제: actual run의 immutable manifest는 소급 수정하지 않고 후속 문서 증거로만 닫음
- 결과: 자동 QA와 사용자 시각 QA 모두 PASS; `SYNTHESIS_ONLY` 과학 판정은 불변
- 다음 재개점: Sono PDF Sections 3–6과 FMT PDF의 source hash·페이지 추출을 고정하고 obligation
  schema를 작성

### 2026-09-02 17:36 KST — 원문 proof edge 추출과 시각 대조

- 출처 고정:
  - Sono PDF SHA-256 `a45f84f5fe99e16534773005287d4ca5538f58d86793184f4d28fad1c9c67302`
  - FMT Chains 감사 copy SHA-256
    `396e54a9699ad80e749b1607c0b5c26982329625615d8769de1e23328f651828`
  - FGKMT Long Gaps PDF SHA-256
    `c31229ef40c9646dfc99bde7c059a9a0fd35e7be71b5836de9df06c01d921ac8`
- 수행:
  - Sono journal pp. 527, 532, 538, 541, 542 렌더링·본문 대조
  - FMT pp. 10, 11, 13, 16 렌더링·본문 대조
  - FGKMT journal pp. 76, 89, 98, 100, 102 렌더링·본문 대조
  - Maynard arXiv:1405.2593의 Proposition 6.1, (8.27), effectivity 문구 추적
- 중요 교정:
  - Sono p. 541은 실제로 `1 << 80c/A <= 1`이며 OCR 오류가 아님
  - 첫 `<<`는 Vinogradov lower comparison으로 숨은 절대상수가 필요함
- 환경 기록:
  - MiKTeX `pdftotext`는 sandbox 밖 로그 권한 때문에 실패
  - PDF나 저장소 내용은 변경되지 않았고 bundled `pypdf`/Poppler로 읽기 전용 추출·렌더링 완료

### 2026-09-02 17:48 KST — T1 66행 원장과 hard-node 판정

- 작성:
  - `docs/method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md`
  - `docs/method/theory/data/Sono_FMT_T1_proof_obligations_v1.json`
  - `docs/review/23_20260902_Sono_FMT_T1_hard_node_feasibility.md`
  - `tests/test_threshold_proof_obligation_ledger.py`
- 분류:
  - 66 obligations
  - EXPLICIT 5 / PARTIAL 11 / RATE_MISSING 30 / SOURCE_REVIEW_REQUIRED 4 /
    HARD_BLOCKER 16
- root critical path:
  - PAP-11, UB-09, AN-11, COV-11, COV-12, SIV-11, TRN-06, FIN-05
- 과학 판정:
  - T1 direct-edge inventory 완료
  - numerical `X_cert` OPEN
  - 다음 gate H1은 FMT/Maynard good-sieve-weight recoverability
  - threshold calculator·장시간 계산 runner는 계속 fail-closed

### 2026-09-02 17:55 KST — 정본 동기화와 검증

- 동기화:
  - AGENTS, METHODS, 이론 색인, 1차 threshold 감사에 T1 결과 연결
  - P020 user figure QA PASS는 계획·결과·색인·방법론에 반영
- 검증:
  - T1 targeted unittest 5/5 PASS
  - 전체 unittest 첫 sandbox 실행은 임시 디렉터리 생성·정리가 차단돼 82개
    `PermissionError`; 코드 failure로 판정하지 않음
  - 동일 명령을 사용자 사전 허가 범위의 sandbox 외부에서 재실행: 206/206 PASS, 28.449초
  - `git diff --check`: whitespace error 0; CRLF 안내만 존재
- 다음 재개점: 새 handoff에 권장 순서·사용자 절차·커밋 제안을 기록하고 원장을 `-done` 전환

### 2026-09-02 17:57 KST — handoff와 완료 전환

- 작성: `handoff/202609021757_HANDOFF.md`
- 포함:
  - P020 최종 QA
  - T1 수치·critical path·검증
  - H1/E1/T2/calculator 권장 순서와 시간
  - 사용자 명령 필요 여부
  - 한국어 commit 제목·본문
- 완료 판정: 요청 산출물, 정본 동기화, 검증, handoff가 모두 끝나 `-done` 전환 가능

### 2026-09-02 17:59 KST — 완료 후 정적 경로 점검 보충

- 첫 PowerShell 점검 명령은 문자열 `"$p:$($_.LineNumber)"`의 `$p:` 변수 해석 때문에
  `ParserError`가 났다. 저장소 파일을 읽거나 바꾸기 전 parser 단계에서 끝났으며 산출물 영향은 없다.
- `${p}`로 범위를 명시해 즉시 재실행했다.
- 결과: 필수 새 파일 missing 0, trailing whitespace 0, targeted vocabulary/T1 tests 6/6 PASS.

## 현재 재개점

작업 완료. 다음 재개점은 handoff의 H1 승인 gate다.

## 완료 전 점검

- [x] P020 사용자 visual QA 반영
- [x] T1 direct proof edge 누락 감사
- [x] hard-node feasibility 판정
- [x] threshold 세 수준·승인 경계 유지
- [x] 정본·색인·AGENTS 동기화
- [x] 검증 명령과 결과 기록
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`·참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
