# P020 recurrence 전수 종합 시각화·Sono/FMT 임계값 감사 작업원장

- 시작: 2026-09-02 11:21 KST
- 현재 상태: COMPLETE
- 사용자 승인:
  - 기존 recurrence artifact 전수 종합 시각화 수준 A의 계획·코드·figure 생성
  - Sono/FMT numerical-threshold proof-dependency 감사
  - 작업원장 규약·양식과 AGENTS 정본화
- 금지·보류:
  - 새 prime sweep, P018-B, P013-C, P019 actual
  - P018-A에서 저장하지 않은 observed recurrence, residual, p/q/z 사후 복원
  - 서로 다른 null·범위·cohort의 p-value pooling
  - 외부 게시, commit, push, PR
- 선행 변경:
  - 시작 시 `AGENTS.md`, `docs/METHODS.md`, 이론 색인·recurrence 문서,
    `test_plan/P018A_prefix_information_probe.md`가 수정 상태
  - P018 사후감사 review·기존 temp worklog·`handoff/202609021101_HANDOFF.md`가 untracked
  - 위 변경은 선행 작업이며 보존한다.

## 목적과 완료조건

- 목적 1: 저장된 P006·P011–P013·P018 artifact를 손실·임의 pooling 없이 하나의 재현 가능한
  증거 묶음과 6개 figure로 종합한다.
- 목적 2: Sono/FMT의 `sufficiently large X`를 numerical `X_0`로 바꾸려면 어떤 증명 의존성과
  explicit constant가 필요한지 문헌 근거로 감사한다.
- 목적 3: 장기 작업을 중단 후 정확히 재개할 수 있는 작업원장 규약을 정본화한다.
- 완료조건: 계획·코드·toy/자동 QA·승인 actual figure·분석보고서·threshold 감사·정본/색인 동기화·
  새 handoff가 모두 완료되고, 사용자 시각 QA만 별도 상태로 명확히 남는다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded 정의 | 영향 없음 | P020은 recurrence 저장 artifact만 읽음 |
| 데이터·provenance | 읽기 전용 영향 | run directory와 입력 hash를 계획·manifest에 고정 |
| 통계·정밀도 | 중요 | null/cohort 역할을 보존하고 p-value를 합치지 않음 |
| P018 information-only 설계 | 중요 | margin-only 정보만 사용, observed recurrence 사후 생성 금지 |
| 승인 경계 | actual figure 승인됨 | 새 prime 계산과 P018-B는 실행하지 않음 |
| 산출물 | 신규 비덮어쓰기 | 새 P020 run id, tables/figures/summary/manifest/log 생성 |
| 정리와 경험적 주장 | 중요 | finite `X_emp`, theorem `X_proof`, global minimum을 분리 |

## 단계 현황

1. **COMPLETED — 저장소 상태·최신 handoff·P018 사후감사 재확인**
2. **COMPLETED — 작업원장 규약·양식과 현재 원장 초안 작성**
3. **COMPLETED — AGENTS·ai_dev_tool README에 작업원장 정본 연결**
4. **COMPLETED — P020 입력 artifact/schema/hash inventory와 영향도 확정**
5. **COMPLETED — P020 계획·adapter·시각화·saved verifier·toy tests 구현**
6. **COMPLETED — exp-preflight와 고정 FGKMT Python 검증**
7. **COMPLETED — 승인된 P020 actual figure 생성과 자동 수치·파일 QA**
8. **COMPLETED — P020 결과 분석보고서·결과 색인·정본 동기화**
9. **COMPLETED — Sono/FMT 원문 proof-dependency 감사와 review 작성**
10. **COMPLETED — 전체 정합성 검증·새 handoff·커밋 메시지 제안**
11. **COMPLETED — 작업원장을 `-done`으로 이름 변경**

## 단계별 기록

### 2026-09-02 11:21 KST — 시작 상태 복원

- 수행: 최신 handoff, P018 사후감사, 선행 temp worklog, AGENTS, test plan 목록, recurrence run 목록 확인
- 결과: P020 번호 미사용, 수준 A 6개 figure 범위와 금지선 확인
- 문제·결정: 선행 dirty 파일을 이번 작업이 덮어쓰거나 되돌리지 않음
- 다음 재개점: `AGENTS.md`와 `ai_dev_tool/README.md`에 본 규약 경로와 재개 순서를 연결

### 2026-09-02 11:26 KST — 작업원장 규약 정본화

- 수행: `ai_dev_tool/08_작업원장_작성규약_양식.md` 신설, `work_ledgers/` 경로 신설,
  `AGENTS.md`와 `ai_dev_tool/README.md`에 재개·완료 규칙 연결
- 결과: 진행 원장과 `-done` 원장의 의미, 단계별 증거, 중단 후 재개 순서, 완료 이름 변경 안전절차 고정
- 다음 재개점: P006·P011·P012-A/B·P013-A/B·P018-P0/A의 실제 파일명·schema·hash를 inventory

### 2026-09-02 11:39 KST — P020 입력·계약·계획 동결

- 수행: 정본 run 8개의 파일 schema, manifest SHA-256, saved summary와 primary cohort 구조 확인
- 파일:
  - `test_plan/P020_recurrence_artifact_synthesis_contract_v1.json`
  - `test_plan/P020_recurrence_artifact_synthesis_visualization.md`
- 결과:
  - contract SHA-256 `5dc9c131b5f0c5eb4580af6cd0e971a40b8c079f2189846e088ea12313f6eacc`
  - 고정 figure 6종, 중복 제거 처리량 `72,178,455,399`, P018 접근 금지선 동결
  - P006/P012/P013/P018의 성공 정본만 포함; 실패 run과 P017 재계산본 제외
- 다음 재개점: 순수 table builder와 figure writer, input/saved verifier, CLI 및 toy tests 구현

### 2026-09-02 11:34 KST — P020 구현과 toy 검증

- 수행:
  - `source/recurrence_artifact_synthesis.py` table builder·6 figure writer·artifact QA·input/saved verifier 구현
  - `source/recurrence_artifact_synthesis_cli.py` preflight/run/verify-saved 구현
  - `tests/test_recurrence_artifact_synthesis.py` toy exact-accounting·P018 금지필드·figure decode·비덮어쓰기 시험 구현
- 첫 실행: `py_compile` PASS, toy 2 PASS·2 ERROR
- 첫 오류: 코드 계산이 아니라 sandbox가 `C:\Users\Uranus\AppData\Local\Temp` 쓰기를 막은 `PermissionError`
- 재실행: 동일 고정 Python toy 4/4 PASS(기존 사용자 허가 범위에 따라 sandbox 외부)
- 다음 재개점: exp-preflight 규약에 따라 정본·환경·반복로그·source 정적감사·입력 verifier·산출물 충돌을 확인

### 2026-09-02 11:37 KST — preflight 과잉재계산 발견·중단·교정

- 첫 preflight: Python 3.11.16, `pip check`, iterated-log 7/7, P020 toy 4/4 PASS 뒤 입력 verifier 진행
- 발견: P012/P013 `verify_saved_*`가 saved table만 읽는 함수가 아니라 segmented-sieve full-range
  recomputation을 호출함
- 조치: P020 result/figure 생성 전 해당 FGKMT preflight process만 Ctrl-C로 중단; PID 종료 확인,
  다른 실행 중 Python 프로세스 미조작
- 영향: P020 actual 산출물 0, 과학 결과 0; 불필요한 prime recomputation이 일부 진행된 승인경계 실수
- 교정:
  - pinned manifest SHA-256
  - manifest의 모든 artifact SHA-256
  - 원 actual의 saved-verifier clean PASS와 manifest 연결
  만 확인하는 경량 audit로 교체; `new_prime_sweep_performed=false` 기록
- 오류 원장: `ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md` E018
- 다음 재개점: 교정 코드 py_compile·toy 후 경량 preflight가 짧게 PASS하고 prime iterator를 호출하지 않는지 확인

### 2026-09-02 11:39 KST — 교정된 경량 input preflight PASS

- 검증: py_compile PASS, P020 toy 4/4 PASS
- 입력: 8/8 pinned manifest hash 일치, 각 manifest artifact hash·기존 saved-verifier 증거 clean PASS
- 계약: `new_prime_sweep_performed=false`, P018 hypothesis test false
- 실행시간: 약 8초; P012/P013 prime iterator 호출 없음
- 다음 재개점: 전체 unittest 회귀검사를 통과한 뒤 새 run id·비덮어쓰기 log로 승인 P020 actual 생성

### 2026-09-02 11:43 KST — P020 R1 actual PASS·시각 배치 R2 결정

- 전체 회귀: 201/201 PASS, 34.320초
- R1 run: `test_result/run_20260902T024226Z_p020_recurrence_artifact_synthesis`
- R1 log: `test_result/logs/run_20260902T024226Z_p020_recurrence_artifact_synthesis.log`
- 자동검증: 입력·artifact hash, 표/summary full recomputation, PNG/PDF QA 모두 PASS; 새 prime 계산 false
- 육안검사: 과학 수치 오류 없음. coverage의 좁은 라벨·주석 겹침, null figure 상자 겹침,
  constant LOW_INFORMATION 색 전달 문제 발견
- 결정: R1 불변 보존, 수치·contract 불변인 `R2_VISUAL_LAYOUT` 새 run 생성
- 다음 재개점: R2 targeted test 후 새 run ID로 생성하고 R1/R2 과학 summary exact equality를 확인

### 2026-09-02 11:47 KST — P020 R2 정본 PASS

- R2 run: `test_result/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis`
- R2 log: `test_result/logs/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis.log`
- manifest SHA-256: `4fe08a450b01d2d483018c61240c53a8e2b75a4c05864b096775280a9466a101`
- 결과: 입력·artifact hash, 6개 표·summary full recomputation, P018 margin-only contract,
  PNG/PDF 12파일 자동 QA 모두 PASS; `new_prime_computation=false`
- 육안점검: R1에서 발견한 라벨·주석·상자·constant heatmap 색 전달 문제가 R2에서 교정됨
- 남은 상태: 사용자 시각 QA는 `PENDING_USER`
- 다음 재개점: P020 결과보고서 작성 후 색인·METHODS·이론 정본에 연결

### 2026-09-02 11:51 KST — P020 결과 분석보고서 작성

- 파일: `test_result/202609021151_P020_recurrence_artifact_synthesis_result_analysis.md`
- 핵심 수치: 처리량 회계 72,178,455,399; P011→P012 기대값 92.1274% 교정;
  prospective 기대 0.4970→0.07783→0.06680; P018 conditioned count·variance 0
- 해석: 계산량과 정보량을 분리하고, enrichment 미검출과 구조 부재를 동일시하지 않음
- 다음 재개점: Sono/FMT 원문 dependency DAG와 numerical threshold blocker를 review로 작성

### 2026-09-02 11:54 KST — Sono/FMT 원문 1차 의존성 감사

- 원문 확인:
  - Sono 2025 local PDF 24쪽, Theorem 3.6·Sections 4–6
  - FMT `Chains of large gaps between primes`, arXiv:1511.04468 공개 PDF 16쪽
- FMT 임시 PDF: `tmp/FMT_Chains_of_large_gaps_between_primes.pdf`
  - source: `https://www.ford126.web.illinois.edu/wwwpapers/primegaps_chains.pdf`
  - SHA-256: `396e54a9699ad80e749b1607c0b5c26982329625615d8769de1e23328f651828`
- 예비 판정: exceptional-zero ineffectivity는 의도적으로 제거되어 proof는 effective-in-principle이나,
  PAP/UB·Mertens/PNT·smooth-number remainder·sieve weight·hypergraph probability의 수치 rate와
  `sufficiently small/large` 상수가 없어 출판본만으로 numerical `X_cert`를 대입 계산할 수 없음
- 다음 재개점: explicit/missing/blocked를 node별로 분류하고 최소 proof-engineering 순서를 작성

### 2026-09-02 12:00 KST — threshold dependency review 완료

- 파일: `docs/review/22_20260902_Sono_FMT_numerical_threshold_proof_dependency_audit.md`
- 수행:
  - finite `X_emp`, proof upper threshold `X_cert`, 실제 전역 최소 `X_star`를 분리
  - Sono Theorem 3.6의 k=1 계수식을 80-dps로 재계산
  - PAP/UB·smooth remainder·FMT/Maynard sieve weight·hypergraph probability·x→X 변환을
    node별로 분류
- 결과:
  - 명목 계수 `2.00386120461967036975...e-17`
  - `2e-17`로 내린 상대 여유 약 `0.192688%`
  - coefficient는 explicit, reviewed top-level proof는 effective-in-principle
  - numerical `X_cert`와 실제 `X_star`는 OPEN
- 결정: 알 수 없는 상수를 채운 threshold calculator를 먼저 만들지 않고, 다음 gate를 T1
  proof-obligation 행 단위 원장으로 둠
- 다음 재개점: P020/threshold 상태를 AGENTS·METHODS·이론 색인·결과 색인에 동기화

### 2026-09-02 12:04 KST — 정본 동기화와 전체 검증

- 갱신:
  - `AGENTS.md`
  - `docs/METHODS.md`
  - `docs/method/theory/00_이론_가설_방법론_색인.md`
  - `docs/method/theory/03_plateau_recurrence_방법론.md`
  - `docs/review/21_20260902_P018_recurrence_설계사후감사_전체시각화_타당성검토.md`
  - `test_plan/P018A_prefix_information_probe.md`
  - `test_plan/P020_recurrence_artifact_synthesis_visualization.md`
  - `test_result/00_실험결과_분석보고서_색인.md`
- 검증:
  - py_compile PASS
  - 전체 unittest `201/201 PASS`, 33.559초
  - P020 R2 saved verifier: artifact/table/summary/P018 contract/figure QA PASS, issue 0
  - 금지 base-2/3/4 log 정적 hit 0
  - 필수 신규 파일 존재 확인 PASS
- 명령 실수: saved verifier의 subcommand 뒤에 존재하지 않는 global option을 한 번 붙여 argparse가
  거부함. `--help`로 실제 계약을 확인하고 `verify-saved --result-directory ...`로 즉시 재실행 PASS.
  과학 계산·파일 변경은 없었음.
- 다음 재개점: 새 timestamp handoff에 사용자 시각 QA와 T1 승인 절차를 포함

### 2026-09-02 12:07 KST — handoff와 사용자 절차 작성

- 파일: `handoff/202609021207_HANDOFF.md`
- 결과:
  - P020 실행·과학·시각 QA 상태를 분리
  - E018 승인경계 실수와 최종 영향 0을 기록
  - threshold 세 수준과 T1–T4 우선순위·근거·예상시간을 쉬운 말로 기록
  - 각 권장 작업에 환경·시작 경로·명령 유무·사용자 회신 항목을 기록
  - 한국어 commit 제목·본문을 포함; commit 자체는 미수행
- 다음 재개점: 최종 `git diff --check`, 경로·상태 확인 뒤 안전하게 `-done` 이름 변경

### 2026-09-02 12:10 KST — 최종 정합성 확인과 완료 처리

- 검증:
  - `git diff --check` whitespace error 0
  - 필수 경로 11개 존재
  - 정본 figure PNG 6개·PDF 6개 존재
  - contract SHA-256 `5dc9c131b5f0c5eb4580af6cd0e971a40b8c079f2189846e088ea12313f6eacc`
  - manifest SHA-256 `4fe08a450b01d2d483018c61240c53a8e2b75a4c05864b096775280a9466a101`
- 결과: 모든 요청 산출물·검증·정본 동기화·handoff 완료
- 남은 외부 상태: 사용자 P020 figure 시각 QA만 대기하며, 이는 작업 산출물 완료와 분리함
- 다음 재개점: 없음. 사용자 회신은 최신 handoff의 시각 QA·T1 승인 절차를 따른다.

## 현재 재개점

완료. 다음 작업은 최신 handoff에서 사용자 figure QA 회신과 T1 승인 여부를 확인한 뒤 새 원장으로
시작한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 사용자 시각 QA 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
