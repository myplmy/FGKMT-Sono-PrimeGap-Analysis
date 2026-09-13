# FGKMT-Sono ChatGPT 오류·실수·환각 원장

최종 갱신: 2026-09-09 KST

## 1. 목적

이 문서는 ChatGPT/Codex가 이 프로젝트에서 낸 구현 오류, 성급한 상태판정, 용어·경로 실수,
과도한 추정과 검증 누락을 숨기지 않고 기록한다. 작은 오류를 즉시 인정·격리·수정하는 편이
나중에 잘못된 연구결과를 되돌리는 것보다 훨씬 싸고 안전하다.

이 원장은 성공을 자랑하는 문서가 아니다. 이미 고친 오류도 재발 방지 규칙을 남기기 위해 보존한다.
새 오류가 발견되면 과거 항목을 지우지 말고 새 ID로 추가한다.

## 2. 상태와 분류

| 표시 | 뜻 |
|---|---|
| `CORRECTED_BEFORE_ACTUAL` | 실제 결과 전에 발견·수정 |
| `USER_RUN_FAILED` | 사용자 실행을 실패시킨 구현 오류 |
| `INVALID_RESULT_NONE` | 실패했지만 채택된 과학 결과는 없음 |
| `METADATA_DEBT` | 수치는 유효하나 이름·추적 정보가 불완전 |
| `ESTIMATE_MISS` | 시간·자원 추정이 실제와 크게 다름 |
| `STATE_JUDGMENT_ERROR` | 불충분한 snapshot으로 실행 상태를 잘못 판단 |
| `USER_CORRECTED` | 사용자가 오류를 지적해 교정 |

## 3. 오류·실수 이력

### E001 — FGKMT 약칭·연구목적·경로 표기 혼선

- 분류: `USER_CORRECTED / INVALID_RESULT_NONE`
- 문제:
  - 초기 문맥에서 FGKMT를 저자 K가 빠진 네 글자 약칭으로 부를 위험이 있었다.
  - 사용자가 `docs/reveiw`가 아니라 `docs/review`임을 교정했다.
  - 연구목적을 정리의 재검증처럼 읽힐 수 있게 넓게 잡은 부분을 사용자가 finite empirical 비교로
    다시 고정했다.
- 영향: 실제 계산 전 교정되어 유효 결과 오염 없음.
- 교정: `AGENTS.md`, `docs/METHODS.md`, vocabulary test, 폴더 정본을 고정.
- 재발 방지: 프로젝트명·review 경로·비목적을 AGENTS의 짧은 불변식으로 유지한다.

### E002 — iterated log를 base-k log로 오해할 가능성

- 분류: `USER_CORRECTED / CORRECTED_BEFORE_ACTUAL`
- 문제: 작업지시서의 `log_2`, `log_3`, `log_4` 표기가 모호해 base 2/3/4 구현으로 갈 위험이 있었다.
- 영향: 기존 실제 연구코드·결과가 0건일 때 교정되어 폐기 결과 없음.
- 교정: `source/definitions.py`, 직접 중첩식, base-k negative control, source 정적감사.
- 재발 방지: 수식 표기를 기억에 의존하지 않고 METHODS와 test를 먼저 읽는다.

### E003 — P005 calibration의 DB 초기화·실패 manifest 부족

- 분류: `USER_RUN_FAILED / INVALID_RESULT_NONE`
- 문제: `gap_stats` 전에 `gaps.db`가 없었고 최초 helper는 실패 provenance를 충분히 남기지 못했다.
- 영향: partial benchmark만 생성됐고 Rank 85→86 결과는 없음.
- 교정: SQLite ledger 선초기화, 실패 manifest, 새 run에서 PASS.
- 증거: `test_result/202608240434_P005_cpu_calibration_partial_failure_analysis.md`.

### E004 — P006 정상 stderr를 PowerShell 실패로 오인

- 분류: `USER_RUN_FAILED / INVALID_RESULT_NONE`
- 문제: unittest가 정상 진행을 stderr에 쓰는데 PowerShell 5.1 pipeline이 `NativeCommandError`로 취급했다.
- 영향: 실제 analysis 전에 두 차례 중단, 과학 결과 없음.
- 교정: stdout/stderr 별도 capture, 이후 Python live tee.
- 증거: `test_result/202608240315_P006_second_pilot_failure_analysis.md`.

### E005 — P007 빈 stderr를 mandatory string으로 전달

- 분류: `USER_RUN_FAILED / INVALID_RESULT_NONE`
- 문제: 빈 stderr 내용을 허용하지 않는 PowerShell parameter에 전달해 runner 자체가 실패했다.
- 영향: certificate 결과 채택 전 중단.
- 교정: empty line 허용·stream별 안전 복사.
- 증거: `test_result/202608240315_P007_pilot_failure_analysis.md`.

### E006 — P010B 반복 verifier의 alias 오인

- 분류: `CORRECTED_AFTER_RUN`
- 문제: 같은 의미의 저장 필드를 별개 값처럼 다루는 반복 verifier 결함이 있었다.
- 영향: bounded queue 결과 감사에서 발견했으며 candidate coverage 원자료는 재검증해 유지됐다.
- 교정: canonical field binding과 negative regression test 추가.
- 증거: `test_result/202608270005_P009_P010_bounded_queue_result_analysis.md`.

### E007 — P012 zero-variance의 `z=None`을 plot에서 float로 강제

- 분류: `USER_RUN_FAILED / INVALID_RESULT_NONE`
- 문제: 통계적으로 올바른 undefined z-score를 그림 코드가 `float(None)`으로 변환했다.
- 영향: r1 결과는 비정본으로 격리. 통계식을 z=0으로 바꾸지 않았다.
- 교정: bar 생략+x marker, r2 새 run·saved recomputation·사용자 QA PASS.
- 증거: `test_result/202608271251_P012A_r1_failure_r2_fix_analysis.md`.

### E008 — P013 NumPy hypergeometric의 10^9 category 한계 누락

- 분류: `USER_RUN_FAILED / INVALID_RESULT_NONE`
- 문제: 큰 `ngood/nbad`에서 NumPy generator가 거부한다는 제한을 사전검증하지 못했다.
- 영향: exact range count 뒤 inference 전에 중단, r1 통계 산출물 없음.
- 교정: exact sequential-symmetry sampler와 작은 PMF 검증, r2 PASS.
- 증거: `test_result/202608281407_P013A_r1_large_hypergeometric_failure_analysis.md`.

### E009 — P013-B process snapshot을 종료·소실로 성급히 해석할 위험

- 분류: `STATE_JUDGMENT_ERROR / USER_CORRECTED`
- 문제: 로그가 늦게 flush되고 한 시점 process 조회가 불완전한 상황에서 “프로세스가 사라졌다”는
  과거 판단이 남을 위험이 있었다.
- 영향: 실행을 강제 종료하지 않았고 최종 P013-B는 PASS했으나 사용자 불안을 키웠다.
- 교정: 진행 JSONL, heartbeat, live console, 원본 log와 result marker가 없는 snapshot만으로 종료를
  단정하지 않는 규칙.
- 재발 방지: PID·child tree·file write time·heartbeat·terminal marker를 함께 확인한다.

### E010 — 장시간 runner의 출력 buffering과 CPU 병렬성 설명 부족

- 분류: `IMPLEMENTATION/COMMUNICATION_ERROR`
- 문제: child Python이 flush하지 않거나 바깥 PowerShell이 capture하면 사용자가 진행 여부를 볼 수
  없었다. affinity를 설정한 것과 실제 8-process 병렬 계산을 같은 것으로 설명할 위험도 있었다.
- 교정: Python `-u`, fsync JSONL, 5분 heartbeat, `live_native_tee.py`, worker PID·native thread log,
  P017 serial/parallel exact equality와 wall-time 비교.
- 증거: `test_result/202608290515_P014_python_live_progress_local_validation.md`,
  `test_result/202608300229_P017_parallel_calibration_result_analysis.md`.

### E011 — P014-R2 raw JSON argv의 PowerShell 5.1 quote 손상

- 분류: `USER_RUN_FAILED / INVALID_RESULT_NONE`
- 문제: PowerShell 7 toy만으로는 보이지 않던 PowerShell 5.1 native argv quote removal을 놓쳤다.
- 영향: 첫 resource preflight 전 실패, constraint scan/result/progress 0.
- 교정: UTF-8 JSON Base64 transport, Windows PowerShell 5.1 exact round-trip regression, broker 자체
  오류 main-log 기록. P014-R3 actual PASS.
- 증거: `test_result/202609010125_P014R2_failure_P014R3_P018_local_validation.md`.

### E012 — P018 구현 초안의 project root·saved verifier·evidence 결함

- 분류: `CORRECTED_BEFORE_ACTUAL`
- 문제:
  - 공통 PowerShell runner가 parent 수를 잘못 세어 project root를 `scripts`로 잡았다.
  - saved verifier가 raw margin에서 components를 재생성하지 않고 저장 components를 신뢰했다.
  - raw dual-primecount evidence·source hash·mutex·resource limit가 처음에는 부족했다.
- 영향: actual 전 코드감사에서 발견되어 P018-P0 결과 오염 없음.
- 교정: root 수정, margin→components→gate 전재계산, raw evidence/hash, 31.5 GB Job limit, mutex,
  deadline 추가. P018-P0 actual·saved recomputation PASS.
- 재발 방지: runner root resolution과 saved-verifier independence를 별도 static test로 유지한다.

### E013 — P014-R3 내부 experiment label에 R2가 남음

- 분류: `METADATA_DEBT`
- 문제: R3가 transport-only revision이라 과학 source/schema를 재사용했고, `summary.json`,
  `manifest.json`, analysis progress의 experiment 문자열이 P014R2로 남았다.
- 영향: run ID·runner hash·log 바깥 marker는 R3이고 수치/hash는 유효하지만 사람이 읽을 때 혼동 가능.
- 처리: actual artifact는 소급 수정하지 않고 결과보고서에 명시했다.
- 재발 방지: `experiment_family`, `schema_version`, `runner_revision`을 별도 필드로 저장한다.

### E014 — P014-R3 시간 추정이 실제보다 지나치게 큼

- 분류: `ESTIMATE_MISS`
- 문제: 4–20시간을 예상했으나 analysis+serial verification은 약 14분 5초였다.
- 원인: parallel exact scan이 예상보다 빨랐고 첫 restricted LP가 unbounded라 새 후보 없이 조기 종료.
- 영향: 자원 낭비는 없었지만 사용자가 시간을 과도하게 예약할 수 있었다.
- 재발 방지: `full-search 예상`, `early-exit 예상`, `hard wall`을 별도로 쓰고 각 gate별 시간 모델을 남긴다.

### E015 — sandbox 전체시험이 권한 오류 임시 디렉터리를 남김

- 분류: `ENVIRONMENT_EXECUTION_ERROR`
- 문제: 2026-09-01 최종 검증에서 전체 unittest를 먼저 sandbox 안에서 실행했고, sandbox가
  `TemporaryDirectory` 접근·정리를 막아 197개 중 80개가 `PermissionError`로 끝났다.
- 영향: assertion 기반 코드 실패는 아니었고, 같은 suite를 sandbox 외부에서 재실행해 197/197
  PASS했다. 다만 접근 권한이 비정상인 임시 디렉터리 16개가 남았다.
- 교정: 절대경로를 검증해 삭제 없이
  `tmp/cleanup_candidates/20260901/sandbox_permission_test_artifacts_202609011817`로 격리했다.
- 재발 방지: sandbox `PermissionError`를 코드 실패로 보고하지 않고, 허가된 동일 명령을 외부에서
  재실행해 판정을 분리한다. sandbox 실패가 남긴 임시 경로도 즉시 감사·격리한다.
- 2026-09-02 재발 기록:
  - P018-A 사후 targeted 25 tests를 sandbox 안에서 먼저 실행해 23개가
    `TemporaryDirectory`·multiprocessing pipe `PermissionError`로 종료됐다.
  - 같은 고정 Python·같은 25 tests를 정상 로컬 권한으로 재실행해 25/25 PASS했다.
  - 프로젝트 안에 남은 0-item·0-byte 디렉터리 5개는
    `tmp/cleanup_candidates/20260902/sandbox_permission_test_artifacts_202609021006`으로
    격리했다.
  - 시스템 `%TEMP%`의 6개 디렉터리는 다른 프로그램과의 소유권 혼동을 피하기 위해 건드리지
    않았다.
- 2026-09-08 재발 기록:
  - H1b-1b-2d 최종 전체 suite를 알려진 제한이 있는 sandbox 안에서 먼저 실행해
    `Ran 286 tests` 중 82개가 임시 디렉터리 `PermissionError`로 종료됐다. 이는 위의
    “첫 판정 실행부터 허가된 정상 로컬 권한을 우선한다”는 재발 방지 규칙을 지키지 않은
    작업 절차 오류다.
  - 같은 고정 FGKMT Python·같은 전체 suite를 허가된 sandbox 밖에서 다시 실행해
    `Ran 286 tests in 39.912s`와 `OK`를 확인했다. 따라서 82건을 코드 회귀로 세지 않는다.
  - 실패 시각 08:56 KST와 일치하는 프로젝트 `tmp/` 디렉터리 16개와 시스템 `%TEMP%`
    디렉터리 후보 43개를 읽기 전용으로 확인했다. 시스템 후보는 다른 프로그램 소유 가능성이
    있고, 프로젝트 후보도 현재 사용자 정리 승인이 없으므로 이번 작업에서 삭제·이동하지 않았다.
  - 다음 전체 suite부터는 기존 사용자 허가 범위 안에서 첫 실행부터 sandbox 밖의 동일 고정
    명령을 사용하고, sandbox 안 실행을 “먼저 한번 해보는” 단계로 두지 않는다.

### E016 — 공식 skill validator의 의존성·Windows 인코딩 전제

- 분류: `TOOLING_VALIDATION_ENVIRONMENT`
- 문제: `skill-creator/scripts/quick_validate.py`가 `PyYAML`을 요구하지만 FGKMT·Codex 번들 Python
  양쪽에 모듈이 없었다. 의존성 우회 뒤에는 `Path.read_text()`의 Windows 기본 CP949가 UTF-8
  한국어 `SKILL.md`를 읽지 못했다.
- 영향: 세 skill이 잘못된 것은 아니며 validator가 frontmatter 검사 전에 종료됐다. 연구 계산과
  actual artifact에는 영향이 없다.
- 교정: 패키지를 임의 설치하지 않고, 이번처럼 단순한 두 필드 frontmatter에 한정한 in-memory
  flat-YAML shim과 Python `-X utf8`로 공식 validator 본문을 실행해 세 skill 모두 `Skill is valid!`를
  확인했다.
- 재발 방지: 한국어 project skill은 validator 실행환경의 YAML 의존성과 UTF-8 mode를 먼저 확인한다.
  중첩 YAML을 쓰게 되면 shim을 확대하지 말고 사용자 허가를 받아 정식 PyYAML 환경을 준비한다.

### E017 — Markdown backtick이 apply_patch JavaScript wrapper를 먼저 종료

- 분류: `TOOL_WRAPPER_SYNTAX / CORRECTED_BEFORE_WRITE`
- 문제: 2026-09-02 P018-A 결과 색인 patch의 첫 시도에서 Markdown backtick을 JavaScript template
  literal 안에 그대로 넣어 `SyntaxError`가 발생했다.
- 영향: `apply_patch` 자체가 호출되기 전에 wrapper parsing이 실패했으므로 파일 변경·부분 patch·연구
  결과 오염은 없었다.
- 교정: patch 안의 backtick을 임시 marker로 바꾸고 tool 호출 직전에 `replaceAll`로 복원해 같은
  patch를 정상 적용했다.
- 재발 방지: `functions.exec`에서 `apply_patch` freeform을 조합할 때 JavaScript delimiter와 Markdown
  delimiter를 분리하고, 실패 뒤에는 대상 파일이 실제로 불변인지 확인한다.

### E018 — P020 사전검증에서 무거운 saved verifier를 경량 hash 검사로 오인

- 분류: `APPROVAL_SCOPE / PREFLIGHT_DESIGN_ERROR / INTERRUPTED_BEFORE_RESULT`
- 문제: 2026-09-02 P020 artifact-only 시각화 사전검증에서 P012/P013의 `verify_saved_*`를
  “저장 artifact만 다시 검사하는 함수”라고 충분히 확인하지 않고 호출했다. 실제 함수는 고정 seed
  통계뿐 아니라 해당 prime range의 segmented sieve 전수 재계산도 수행한다.
- 영향: 고정 Python P020 preflight가 P013 full recomputation에 들어간 뒤 약 수분·CPU 약 135초를
  사용했다. 결과·figure·P020 run directory는 생성되기 전이었고 다른 Python 프로세스는 건드리지
  않았다. no-new-prime-sweep 승인 경계와 충돌함을 확인한 즉시 해당 세션 PID만 중단했다.
- 교정: P020 입력 검사는 pinned manifest hash, manifest 내 모든 artifact hash, 원 actual이 저장한
  `saved_verification_report.json`의 clean PASS와 manifest 연결만 재검증한다. 새 prime sweep flag는
  명시적으로 `false`로 저장한다.
- 재발 방지: 함수명만으로 비용·부작용을 추정하지 않는다. actual artifact verifier를 새 파이프라인에
  연결하기 전에 구현 본문에서 raw input iterator, segmented sieve, network/write 동작을 확인하고
  `hash-only`, `saved-stat recomputation`, `full-range recomputation`으로 분류한다.

### E019 — H1b-1a 초안의 LaTeX backslash가 도구 wrapper에서 제어문자로 변환

- 분류: `TOOL_WRAPPER_SYNTAX / CORRECTED_BEFORE_ACTUAL`
- 문제: 2026-09-04 H1b-1a 정식 문서의 첫 patch를 일반 JavaScript 문자열로 조합하면서
  `\vartheta` 등의 backslash escape가 탭·수직탭 같은 제어문자로 바뀌었다.
- 영향: 새 이론 문서 초안 한 파일만 손상됐고, actual 실험·기존 정본·수치 결과에는 영향이 없다.
- 교정: 손상된 새 파일을 즉시 제거한 뒤 raw-string patch로 전면 재작성했다. 텍스트 확장자만
  대상으로 ASCII 제어문자 검사를 수행하고 `git diff --check`를 최종 gate에 넣었다.
- 재발 방지: 수식이 있는 patch는 항상 raw string 또는 안전한 placeholder를 사용한다. binary
  `__pycache__`를 텍스트 제어문자 검사 대상으로 넣지 않으며, 실패 직후 부분 변경 여부를 확인한다.
- 2026-09-06 재발: H1b-1b 정식 문서의 첫 patch에서도 `\\frac`의 `\\f`가 제어문자로
  변환되어 patch 검증 단계에서 거부됐다. 첫 raw 재시도도 Markdown backtick을 JavaScript
  template delimiter와 분리하지 않아 wrapper parse 단계에서 멈췄다. 두 시도 모두 파일을
  만들지 않았고, backtick-free raw patch로 정상 생성했다. 이후 수식 문서 patch는 첫 시도부터
  raw 입력을 사용하고 template 안의 Markdown backtick도 사전 제거·escape한다.
- 같은 날 후속 정본 동기화에서 이 규칙을 일관되게 적용하지 않아 AGENTS 1회와 묶음 문서 1회가
  다시 wrapper parse 단계에서 멈췄다. 두 호출 모두 apply_patch 실행 전이어서 파일 변경은 0건이며,
  이후 호출은 backtick 자리표시자 치환으로 통일했다.
- 2026-09-08 재발: H1b-1b-2d 완료 원장 patch와 뒤이은 오류 원장 patch의 raw
  template에 기존 Markdown backtick을 그대로 남기는 실수를 두 차례 했다. JavaScript
  wrapper가 각각 `SyntaxError: Unexpected number`와 `Unexpected identifier`로 중단했다.
  두 경우 모두 `apply_patch`는 호출되지 않아 파일 변경은 0건이었고, 모든 backtick을
  자리표시자로 바꾼 동일 patch를 정상 적용했다.

### E020 — H1b-1a 작업원장 중간 기록에 아직 오지 않은 시각을 기입

- 분류: `METADATA_DEBT / CORRECTED_BEFORE_ACTUAL`
- 문제: 2026-09-04 작업원장 두 단계의 시각을 실제 현재시각보다 뒤인 22:05, 22:31 KST로
  잘못 적었다.
- 영향: 수학 문서·코드·검증값에는 영향이 없고, 완료 전 작업 이력의 시각 metadata만 잘못됐다.
- 교정: 시스템 `Get-Date`가 21:45 KST임을 확인한 뒤 두 항목을 “21:45 KST 기록”으로
  고치고, 이는 앞서 끝난 단계를 사후 기록한 시각임을 명시했다.
- 재발 방지: 작업원장 timestamp는 문맥에서 추정하지 않고 기록 직전 시스템 시각을 조회한다.
- 재발 기록(2026-09-08, H1b-1b-2d): 작업원장 정식화 완료 항목에 시스템 현재시각보다 늦은
  `09:32 KST`를 기입했다. 08:56 KST 전체시험 흔적과 시스템 시각을 대조해
  `08:50 KST 사후 기록`으로 교정했다. 수학·코드·검증 결과에는 영향이 없다.

### E021 — GGPY arXiv source payload를 tar archive로 오인

- 분류: `SOURCE_CONTAINER_MISCLASSIFICATION / CORRECTED_BEFORE_ANALYSIS`
- 문제: 2026-09-06 arXiv e-print 응답을 파일명 `.tar`만 보고 tar archive로 해제했다.
  실제 payload는 단일 TeX 파일의 gzip stream이어서 Windows tar가 TeX token을 경로처럼
  해석하고 임시 폴더에 다수의 잘못된 0-byte 항목을 만들었다.
- 영향: source 원본과 정본 파일은 손상되지 않았고 수학 분석 전 단계에서 실패했다. 잘못 생긴
  항목은 `tmp/pdfs/h1b1b/ggpy_source/`에만 있으며 근거 자료로 사용하지 않았다.
- 교정: magic bytes가 gzip임을 확인하고 GZipStream으로 단일 TeX를 해제했다. 원 payload와
  extracted TeX의 SHA-256을 각각 기계 원장에 기록했다.
- 재발 방지: arXiv source는 확장자나 Content-Disposition만 믿지 않고 magic bytes와 container
  listing을 먼저 확인한다. 해제 실패 출력으로 만들어진 파일은 source 증거로 채택하지 않는다.

### E022 — GGPY Lemma 3–4 오류항에 `c_gamma`가 자동 포함된다고 계약

- 분류: `MATHEMATICAL_CONTRACT_ERROR / CORRECTED_BEFORE_PARENT_CLOSURE`
- 문제: H1b-1b 첫 정식화에서 GGPY Lemma 3의 base error를
  `|E| <= C3*c_gamma*(L+1)`로 가정하고 factor 2를 전달했다. Castillo–Hall–Lemke
  Oliver–Pollack–Thompson의 peer-reviewed Lemma 2.5와 Remark를 대조하면, 원래 가정만으로
  안전하게 증명되는 오류항에는 `c_gamma`가 없고 더 강한 형태에는 추가적인
  `z` 대 `L` 크기조건이 필요하다.
- 영향:
  - Lemma 8.2 multiplier 89와 부분적분의 절대오차 factor 2는 유효하다.
  - 그러나 factor 2는 `C4_abs <= 2*C3_abs`로 해석해야 한다.
  - Maynard Lemma 8.4의 상대오차 합성에는 별도 `c_gamma` 하한 또는 명시적 크기조건이
    추가로 필요하다.
  - parent H1b-1 package, SIV-07, `X_cert`가 모두 fail-closed OPEN이었으므로 잘못
    닫힌 theorem threshold나 actual 결과는 없다.
- 교정: 코드 계약·기계 원장·방법론 정본에서 절대오차와 상대오차를 분리하고, 양의
  `c_gamma` 하한 없이는 상대 multiplier를 만들지 못하는 negative regression을 추가했다.
- 재발 방지: 인용 lemma의 출판본 주석만 확인하지 않고, 후속 peer-reviewed 재서술·정정과 proof의
  base error normalization을 함께 대조한다. 주항에 들어간 Euler product가 오류항에도 자동
  들어간다고 추론하지 않는다.

### E023 — Maynard 기본 W 상계를 모든 actual call의 제외모듈 상계로 과잉 일반화

- 분류: `MATHEMATICAL_SCOPE_ERROR / CORRECTED_BEFORE_PARENT_CLOSURE`
- 문제: H1b-1b-2a 초안에서 Maynard의 기본 `W_j`와 남은 `e_i`로 만든 상계가
  Lemma 8.4의 모든 실제 호출에서 쓰이는 effective excluded modulus를 자동으로 덮는다고
  판단했다.
- 뒤늦게 확인한 누락:
  - `(r_j,dW_j)=1`에 들어가는 추가 `d<=R`
  - `W'_j=rad(W_j(a_j b_m-a_m b_j))`
  - `a_m W B r`, `rW_m`, `W_0=D V Delta_L` 형태의 응용별 제외 인자
- 영향:
  - 실제 네 local denominator family에서 비제외 소수 factor가 1 이상이라는 exact 대수는
    그대로 유효하다.
  - effective excluded integer `Q`에 대해 `c_gamma>=phi(Q)/Q`로 환원하는 단계도 유효하다.
  - 그러나 기본 `W_j` 상계만으로 모든 actual call의 `Q`를 명시적으로 제한했다는 결론은
    성립하지 않는다.
  - actual 실험, threshold 계산, `SIV-07`, `X_cert`의 승격은 없었으므로 오염된 계산 결과나
    잘못 닫힌 theorem threshold는 없다.
- 교정:
  - 기본 상계와 응용별 `application_log_overhead`를 분리했다.
  - 코드에서 overhead를 필수 인수로 만들어 암묵적 0을 금지했다.
  - 하위·상위 기계 원장, METHODS, AGENTS를
    `BASE_W_PARAMETERIZED_APPLICATION_OVERHEAD_OPEN`으로 fail-closed 동기화했다.
  - 누락·음수 overhead를 거부하는 회귀검사를 추가했다.
- 재발 방지: 실제 호출부가 여러 개인 lemma는 공통 정의만으로 universal closure를 선언하지
  않는다. 호출별 인수 변환표와 추가 소인수 inventory를 먼저 완성하고, 코드 API에서도
  application-specific overhead를 생략할 수 없게 한다.

### E024 — H1b-1b-2a.1 문서 patch 두 차례 사전 실패

- 분류: `TOOL_WRAPPER_SYNTAX / PATCH_CONTEXT_ERROR / CORRECTED_BEFORE_WRITE`
- 문제: 2026-09-07 첫 문서 patch에서 Markdown backtick을 JavaScript template literal에
  그대로 넣어 E017과 같은 wrapper parsing 실패를 반복했다. 이후 상위 문서 일괄 patch 한 번은
  expected context를 잘못 이어 붙여 `apply_patch verification failed`가 났다.
- 영향: 두 경우 모두 `apply_patch`가 변경을 적용하기 전에 중단되어 부분 수정이나 연구 결과
  오염은 없었다. 대상 파일을 다시 읽고 작은 patch로 분할해 정상 적용했다.
- 재발 방지: backtick 포함 patch는 일반 문자열 delimiter를 사용하고, 여러 문단을 한 호출에
  묶기 전에 현재 파일의 정확한 context를 다시 읽는다. patch 실패 직후에는 성공으로 간주하지
  않고 파일 내용과 `git diff`를 확인한다.
- 재발 기록(2026-09-08, H1b-1b-2d): 내용 변경 없이 `Move to`만 둔 완료 원장
  patch가 빈 hunk로 거부됐다. 파일은 바뀌지 않았고, 제목의 완료 표기를 함께 바꾸는 유효한
  hunk로 다시 실행해 `-done.md` 이관을 완료했다.
- 재발 기록(2026-09-08, H1b-1b-2d.1a): 긴 Markdown patch를 JavaScript 일반 문자열에
  넣으면서 TeX `\xi`가 `\x` escape로 해석돼 wrapper가 쓰기 전에
  `Invalid hexadecimal escape`로 멈췄다. 이어서 raw template에 Markdown
  backtick을 그대로 넣은 두 호출과, 서로 다른 문맥을 묶은 두 다중파일 patch가 각각
  parser 또는 context 검증에서 원자적으로 거부됐다. 실제 부분 변경은 없었다. 이후
  backtick placeholder와 작은 파일별 patch로 전환해 적용 결과를 재확인했다.

### E025 — H1b-1b-2b 초안의 tail 상수를 과소 계상

- 분류: `MATHEMATICAL_BOUND_ERROR / CORRECTED_BEFORE_PARENT_CLOSURE`
- 문제: Ford Theorem 4.4의 \(\kappa=1\) proof를 처음 명시화할 때, prime weighted-sum의
  두 endpoint 오차와 작은 \(x\) reciprocal-prime 구간을 충분히 합산하지 않아 중간 상수를
  81, 지수 상수를 165로 적었다.
- 영향: 새 이론 문서 초안·기계 계약·코드의 미검증 상태에만 잠시 존재했다. actual 실험,
  기존 결과, `SIV-07`, `X_cert` 또는 theorem threshold는 실행·승격되지 않았다.
- 교정: 원문 식 (4.8)--(4.15)와 Abel 부분합을 다시 전개해 interval bound를
  `128+A2+L <= (130+A2)(L+1)`로 고쳤다. 작은/큰 \(x\) 분기를 모두 덮도록 지수는
  보수적인 `256+A2`로 올리고 관련 문서·JSON·코드·시험을 전부 동기화했다.
- 재발 방지: asymptotic proof를 수치화할 때 endpoint, small-range split, tail integral을
  별도 행으로 원장화하고, 더 작은 상수보다 먼저 독립적인 안전 상계를 확보한다.

### E026 — JSON·제어문자 보조 검증기가 신뢰할 수 없는 PASS/FAIL을 표시

- 분류: `VALIDATION_SCRIPT_ERROR / CORRECTED_DURING_FINAL_AUDIT`
- 문제: PowerShell `ConvertFrom-Json`은 `f`와 `F`처럼 대소문자만 다른 키가 있는 기존 JSON에서
  비종료 오류를 냈지만, 명령 끝의 PASS 문자열은 그대로 출력했다. 별도 Python 제어문자
  one-liner는 escape를 잘못 써 정상 줄바꿈을 제어문자로 오판했다.
- 영향: 첫 JSON PASS와 첫 제어문자 FAIL을 모두 폐기했다. 연구 계약 파일의 오류나 수치 오염은
  없었고, 최종 판정에는 사용하지 않았다.
- 교정: 고정 FGKMT Python의 `json.loads`로 theory JSON 12개를 엄격 파싱했고, 제어문자는
  codepoint 9/10/13을 직접 허용하는 방식으로 213개 UTF-8 텍스트를 다시 검사했다.
- 재발 방지: PowerShell 검증은 `$ErrorActionPreference='Stop'` 또는 `-AsHashtable`을 쓰며,
  PASS는 오류가 없고 종료코드 0인 뒤에만 출력한다. escape-sensitive 검사는 문자 리터럴보다
  codepoint 정수 집합을 사용한다.
- 재발 기록(2026-09-08): H1b-1b-2c 최종 감사에서 `$ErrorActionPreference='Stop'`은
  설정했지만 `ConvertFrom-Json`의 대소문자 키 충돌 자체를 잊고 같은 parser를 다시 선택했다.
  이번에는 오류 즉시 명령이 중단되어 거짓 PASS는 없었고 연구 파일에도 영향이 없었다.
  향후 theory JSON 전수 파싱은 예외 없이 고정 FGKMT Python `json`을 사용한다.

### E027 — H1b-1b-2c 보조 도구 가용성을 확인하기 전에 호출

- 분류: `TOOL_AVAILABILITY_ASSUMPTION / NO_RESEARCH_IMPACT`
- 문제:
  - 초등 합 상계를 확인하는 탐색 단계에서 고정 FGKMT 환경에 설치되지 않은 `sympy`를 먼저
    호출해 `ModuleNotFoundError`가 발생했다.
  - PDF 텍스트 추출에서는 번들 dependency 안내 경로 아래에 `pdftotext.exe`가 있을 것으로
    가정했으나 해당 실행파일이 없었고, 시스템 `pdftotext`는 MiKTeX 로그 권한 오류를 냈다.
  - 큰 표준 라이브러리 합을 한 번 직접 계산하려던 보조 명령은 출력 없이 종료돼 증거로 쓸 수 없었다.
  - 최종 규칙 검색 한 번에서 Windows PowerShell이 확장하지 않은 `ai_dev_tool/*.md`를
    `rg`에 직접 넘겨 경로 구문 오류가 났다. 필요한 AGENTS/METHODS 검색 결과는 얻었지만
    이 실패 호출 자체는 검증 증거로 세지 않았다.
  - H1b-1b-2d 최종 감사에서 `Select-String` 정규식에 TeX `\mathbf`를 그대로 넣어
    PowerShell regex parser가 `\m` escape 오류로 거부했다. 고정 문자열 `rg -F`로 다시
    조회했고, 실패 호출은 source 증거로 세지 않았다.
- 영향: 새 패키지를 설치하지 않았고, 실패 출력이나 미완료 합을 수학적 증거로 사용하지 않았다.
  기존 로컬 PDF의 SHA-256, 번들 Python `pypdf` 추출과 렌더링한 원문 페이지를 사용해 다시
  확인했다. 연구 결과·actual 데이터·`SIV-07`·`X_cert`에는 영향이 없다.
- 교정: 필요한 부등식을 `fractions`, `mpmath`와 초등 적분으로 검증해 추가 dependency를 없앴다.
- 재발 방지: optional library는 먼저 import 가능 여부를 검사하고, 없어도 표준 라이브러리로
  해결 가능한지 판단한다. PDF 도구는 안내된 상위 경로만 믿지 말고 실제 실행파일 존재를
  확인하며, 추출 command의 종료코드가 0이 아닐 때 출력 텍스트도 정본 증거로 승격하지 않는다.
  Windows의 `rg`에는 디렉터리 경로를 주고 `-g '*.md'`를 쓰며 Unix식 path wildcard를
  직접 인수로 넘기지 않는다.
- 재발 기록(2026-09-08, H1b-1b-2d): JSON parent 상태를 찾는 보조 명령에서 다시
  `docs/method/theory/data/*.json`을 `rg`에 직접 넘겨 Windows 경로 구문 오류가 났다.
  실패 호출은 증거에서 제외했고 이후 디렉터리 인수와 `-g '*.json'`만 사용한다.
- 재발 기록(2026-09-08, H1b-1b-2d.1a): 존재 여부를 먼저 검색하지 않고
  `source/h1b1b_lemma82_package.py`라는 잘못 추정한 파일명을 조회했고, Windows
  `tests/test_h1b*` wildcard를 다시 직접 넘겼으며, 괄호가 닫히지 않은 복합
  `rg` 정규식도 한 번 사용했다. 모두 실패 출력은 증거에서 제외했다. 실제 파일은
  `rg --files`로 찾고, 디렉터리+glob 및 여러 `-F -e` 고정 문자열로
  재조회했다. 시스템 `pdftotext`도 MiKTeX 로그 쓰기 권한 때문에 비정상 종료해
  그 출력은 채택하지 않고, 원 TeX·로컬 PDF hash·출판사/arXiv 원문을 교차 확인했다.

### E028 — H1b-1b-2c 상위 정본 동기화 중 patch·회귀 기대값 불일치

- 분류: `PATCH_CONTEXT_ERROR / TEST_EXPECTATION_SYNC / CORRECTED_DURING_WORK`
- 문제: 여러 문서를 한 번에 갱신한 `apply_patch`에서 T1 문단 context 한 줄이 달라 전체 patch가
  사전 거부됐다. 이후 schema·상태를 갱신한 첫 표적 회귀시험은 이전 version/status 문자열을
  기대하는 시험 3건, 두 번째 실행은 boolean 기대값 1건이 실패했다. 최종 전체 suite의 첫
  실행에서도 실제 입력 하위 행의 빈 `missing_numeric_inputs`를 허용하지 않는 구형 불변식 1건이
  남아 있었고, 이를 고치며 `H1B1-L84-GAMMA/L`의 뒤늦은 상태 동기화도 발견했다.
- 영향: 거부된 patch는 원자적으로 적용되지 않았다. 시험 실패는 새 수학식의 실패가 아니라
  기계 계약의 현재 schema/status와 시험 기대값 사이의 동기화 실패였으며, 실패 상태에서 완료나
  PASS를 선언하지 않았다.
- 교정: patch를 작은 문서 단위로 나누고 현재 context를 다시 읽었다. schema, outcome,
  `H1B-L83` 상태와 fail-closed parent 기대값을 함께 갱신했다. 실제 gamma와 discrepancy 입력
  하위 행도 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 정정하고 표적·전체 suite를 다시
  통과시켰다.
- 재발 방지: 상위 JSON schema를 올릴 때 같은 patch 또는 바로 다음 patch에서 이를 검증하는
  모든 시험을 검색해 갱신한다. 대형 다중파일 patch 전에 각 대상의 정확한 주변 문맥을 다시 읽는다.

### E029 — CRLF 저장소에서 `core.autocrlf=false`로 diff 검사를 왜곡

- 분류: `VALIDATION_CONFIGURATION_ERROR / NO_RESEARCH_IMPACT`
- 문제: 2026-09-08 마지막 확인의 경고를 줄이려 `git -c core.autocrlf=false diff --check`를
  실행했다. 이 임시 설정은 작업트리의 기존 CRLF에서 `\r`을 각 줄의 후행 공백처럼 보이게 해
  대량의 거짓 `trailing whitespace`를 보고했다.
- 영향: 이 명령은 읽기 전용이었고 파일, 수학 결과, 테스트 결과에는 영향이 없다. 해당 FAIL은
  저장소 품질 판정에서 폐기했다.
- 교정: 저장소의 정상 line-ending 설정을 유지한 기본 `git diff --check`로 다시 검사한다.
- 재발 방지: 줄바꿈 경고를 감추기 위해 Git 변환 설정을 바꾸지 않는다. 필요하면 stderr만
  별도로 보존하되, 프로젝트 기본 설정에서 얻은 종료코드를 판정에 사용한다.

### E030 — H1b-1b-2d.1a mpmath 시험의 전역 정밀도 순서 의존

- 분류: `TEST_PRECISION_STATE_LEAK / NO_RESEARCH_IMPACT`
- 문제: 신규 표적 시험은 단독으로 통과했지만 전체 suite에서는 앞선 시험이 변경한
  `mp.mp.dps`의 영향으로 `epsilon**2`와 별도 10진 literal을 `assertEqual`로 비교한 한
  항목이 마지막 자리에서 달라졌다.
- 영향: 제품 코드, exact 유리수 증명과 정리 상태에는 영향이 없다. 전체 suite의 신규
  수치 시험 1건만 거짓 실패했다.
- 교정: 수치 필드는 `mp.almosteq`로 비교하고, 핵심 exact square identity는 별도의
  `Fraction` 시험으로 계속 엄밀하게 검사한다.
- 재발 방지: `mpmath` 수치 시험은 suite 순서와 외부 정밀도 상태에 독립적인 비교를 사용하고,
  완전일치가 필요한 대수 불변식은 정수 또는 `Fraction`으로 검증한다.

### E031 — 구 author TeX를 최종 출판식처럼 읽어 determinant 오류를 잘못 보고

- 분류: SOURCE_VERSION_MISREAD / CORRECTED_BEFORE_NUMERICAL_USE
- 문제: H1b-1b-2d.1a 검토에서 검색하기 쉬운 author TeX 986행의
  \(i=1,\ldots,k\) determinant를 보고 “인쇄식도 \(i=m\)을 포함해 0이 된다”는 취지로
  기록했다. 실제 최종 출판본 1545쪽 식 (9.43)은 이미 \(i\ne m\)으로 고쳐져 있었다.
  PDF 수식을 시각 대조하기 전에 구 TeX를 출판식과 동일하다고 가정한 source-version 오류다.
- 영향:
  - 잘못된 determinant를 코드나 actual 계산에 사용하지 않았고, 해당 scalar 상수는 당시
    OPEN으로 남겼으므로 수치 결과·threshold·상위 theorem 상태의 오염은 없다.
  - 다만 theory 25, review 31과 JSON의 source caution 문구가 출판 논문에 존재하지 않는
    오류를 있는 것처럼 표현했다.
- 교정:
  - 최종 출판 PDF의 식 (9.43)을 렌더링·텍스트 추출 양쪽으로 확인했다.
  - theory 25, review 31과 기계 계약을 “구 author TeX 오자, 최종 출판본 정상”으로 고쳤다.
  - H1b-1b-2d.1a.1은 출판본의 \(i\ne m\) 식만 사용해 determinant 상계를 재증명했다.
- 재발 방지: author source와 출판본이 모두 있을 때 수식 하나의 오류를 보고하기 전
  DOI 출판본의 해당 페이지를 반드시 렌더링해 대조한다. 차이가 있으면 version과 locator를
  각각 기록하고 최종 출판본을 권위 원천으로 삼는다.
- 같은 작업의 도구 오류:
  - 첫 긴 문서 patch는 JavaScript 문자열의 TeX \(\xi\)가 hexadecimal escape로 해석돼
    쓰기 전에 거부됐다.
  - 다음 raw-template 다중파일 patch는 Markdown backtick 때문에 parser가 쓰기 전에
    거부됐다.
  - 첫 상수 회귀시험은 exp(log(C)) 평가와 직접식의 약 \(1.74\times10^{-79}\) 상대
    반올림 차이를 exact-default tolerance로 비교해 거짓 실패했다.
  모두 부분 쓰기나 수학 판정 오염 없이, raw patch의 delimiter를 정리하고 symbolic
  coefficient는 exact로 유지한 채 수치 비교 tolerance만 \(10^{-75}\)로 명시해 교정했다.

### E032 — H1b-2a.2에서 이미 알려진 Windows 검증 절차 오류 재발

- 분류: `KNOWN_ENVIRONMENT_ERROR_REPEATED / COMMAND_PATTERN_RECURRENCE / NO_RESEARCH_IMPACT`
- 문제:
  1. 이 원장 5절 8항에 `TemporaryDirectory`를 쓰는 전체 suite는 허가된 정상 로컬 권한을
     우선한다고 적혀 있는데도, H1b-2a.2의 첫 전체 unittest를 sandbox 안에서 실행했다.
     82개가 공통 `PermissionError`로 실패했다.
  2. 오류 원장 검색에서 Windows `rg`에 `ai_dev_tool/*.md`와 `**/*.md`를 직접 넘겨 이미
     금지된 path-wildcard 구문 오류를 한 번 반복했다.
  3. 오래된 문서 한 곳의 실제 문맥이 예상과 달라 긴 다중파일 `apply_patch`가 원자적으로
     거부됐다.
- 영향: 첫 unittest와 `rg` 출력은 증거에서 제외했다. 거부된 patch는 아무 파일도 바꾸지
  않았다. 수학식, actual 데이터, 결과 artifact, theorem 상태에는 영향이 없다.
- 교정: 사용자 기존 허가 범위에서 동일 전체 suite를 sandbox 밖 FGKMT Python으로 다시
  실행해 `328/328 OK`를 확인했다. 검색은 디렉터리 또는 `Get-ChildItem`로 바꿨고, patch는
  현재 문맥을 다시 읽은 뒤 작은 단위로 적용했다.
- 재발 방지: 이 저장소의 전체 suite는 처음부터 승인된 unrestricted 실행을 사용한다.
  `rg` glob은 경로 인수에 넣지 않고 `-g`로만 전달한다. 5개 이상 파일을 건드리는 patch는
  대상별 현재 문맥을 먼저 고정하고 두세 묶음으로 나눈다.

### E033 — H1b-2a.3 첫 합성에서 \(2^k\) 손실을 약한 cutoff로 남김

- 분류: `PROOF_GATE_TOO_WEAK / CAUGHT_BEFORE_CANONICAL_PROMOTION / TOOL_PATCH_ERROR`
- 문제: Proposition 9.4의 product-profile 절대오차를 coupled main에 대한 상대오차로 바꿀 때
  필요한 \(I_k(F_1)\le2^kI_k(F)\)를 식에는 넣었지만, 첫 초안은 기존
  \(\Delta_c\le1\) smooth gate만 사용했다. 그러면 \(2^k\varepsilon_c\)가 유한하기는 해도
  \(k\)에 따라 커져 Maynard의 uniform implied constant를 복원하지 못한다. 또한 predecessor
  JSON 세 개를 한 번에 갱신하려던 `apply_patch` 입력의 파일 구분 형식이 잘못돼 patch가
  사전 거부됐다.
- 영향: 약한 gate 초안은 신규 정본·상위 상태 원장에 확정하기 전에 자체 검산에서 발견됐다.
  actual 데이터나 prime 계산은 수행하지 않았고, `SIV-07`, `X_cert`를 승격하지 않았다.
  거부된 patch는 파일을 바꾸지 않았다.
- 교정: P94 전용으로 \(\Delta_c\le2^{-k-1}\)을 요구해
  \(\varepsilon_c\le2\Delta_c\), \(2^k\varepsilon_c\le1\)을 보장했다. 이 강화 cutoff에서
  모든 정수 \(k\ge36\)에 대해 actual-call multiplier가 13 미만임을 다시 증명하고
  독립 재합성 회귀시험을 추가했다. predecessor patch는 파일별로 나눠 적용했다.
- 재발 방지: 절대오차를 다른 norm의 상대오차로 옮길 때 norm-comparison multiplier를
  먼저 표에 등록하고, 단순 유한성뿐 아니라 source가 요구하는 parameter-uniformity를
  별도 gate로 검사한다. 다중파일 patch는 현재 문맥을 읽은 뒤 작은 단위로 적용한다.

### E034 — H1b-2a.3 source 검색 범위를 `tmp/` 전체로 과도하게 확장

- 분류: `SEARCH_SCOPE_ERROR / READ_ONLY / NO_RESEARCH_IMPACT`
- 문제: Maynard TeX와 FGKMT 치환을 재확인하는 `rg` 명령에 필요한 하위 디렉터리 대신
  `tmp` 전체를 넣어, 이전 sandbox 시험이 남긴 접근 불가 임시 폴더에서 다수의
  `Access is denied` 진단이 발생했다.
- 영향: 명령은 읽기 전용이었고 필요한 Maynard TeX 행은 정상 출력됐다. 접근 실패 경로의
  내용을 증거로 사용하지 않았고 파일·수학 결과·실험 artifact에는 영향이 없다.
- 교정: 채택 근거는 이미 hash가 고정된 개별 TeX/PDF 파일과 해당 행·페이지로 제한했다.
- 재발 방지: source 재조회는 파일 또는 정확한 source 하위폴더만 대상으로 하고, provenance와
  무관한 `tmp` 루트 전체를 재귀 검색하지 않는다.

### E035 — H1c-1a 착수에서 E034의 `tmp/` 전역 검색을 반복

- 분류: `KNOWN_SEARCH_SCOPE_ERROR_REPEATED / READ_ONLY / NO_RESEARCH_IMPACT`
- 문제: H1c-1a source inventory 착수 시 이미 E034에 금지한 `rg --files tmp`를 다시 실행해,
  이전 sandbox 시험이 남긴 접근 불가 임시폴더에서 다수의 `Access is denied` 진단을
  재발시켰다. 동시에 H1c JSON 이름을 기억으로 추정해 첫 읽기에서 `FILE_NOT_FOUND`가 났다.
- 영향: 두 명령 모두 읽기 전용이었다. 접근 실패 경로와 잘못 추정한 파일명을 연구 증거로
  사용하지 않았고, 문서·코드·actual artifact·정리 상태에는 영향이 없다.
- 교정: `docs/method/theory/data`만 좁게 검색해 정확한 JSON 이름을 확인하고, source 검색은
  `tmp/pdfs/t1`, `tmp/pdfs/h1b1b/maynard_source`처럼 이미 알려진 개별 경로로 제한했다.
- 재발 방지: 오류 원장에 같은 검색 실수가 한 번이라도 있으면 새 작업의 첫 source 조회 전에
  대상 파일 목록을 `Get-ChildItem -LiteralPath <known-directory>`로 고정한다. 예상 파일명은
  읽기 전에 해당 정본 디렉터리에서 확인한다.

### E036 — H1c-1a PDF 도구·PowerShell wildcard 경로를 먼저 확인하지 않음

- 분류: `TOOLING_ASSUMPTION_ERROR / READ_ONLY / NO_RESEARCH_IMPACT`
- 문제:
  1. sandbox 안에서 MiKTeX `pdftotext`를 먼저 호출해 사용자 AppData의 MiKTeX log 쓰기 권한
     오류를 냈다. 같은 원문을 승인된 정상 로컬 권한으로 다시 읽으면 정상 동작하는 환경 문제였다.
  2. 번들 Poppler 경로에 `pdftotext.exe`도 있을 것이라고 추정했지만 실제 번들에는 이번 확인
     범위에서 `pdfinfo.exe`, `pdftoppm.exe`만 있었다.
  3. `Get-FileHash -LiteralPath '.../*.pdf'`에 wildcard를 넘겨 경로 구문 오류를 한 번 냈다.
  4. 첫 Markdown relative-link 검사기가 공백 경로용 `<...>` wrapper를 제거하지 않아 기존의
     유효한 PDF 링크 1개를 missing으로 잘못 보고했다.
- 영향: 모두 읽기·hash 조회 단계의 도구 오류였다. 실패 출력은 source 증거로 사용하지 않았고,
  PDF 원본·문서·수학 판정·actual artifact에는 영향이 없다.
- 교정: PDF text는 동일한 MiKTeX 명령을 정상 로컬 권한에서 실행하고, 수식 페이지는 실제 존재가
  확인된 `pdftoppm.exe`로 렌더링했다. hash는 `Get-ChildItem -Path ... -Filter '*.pdf'`로 파일을
  열거한 뒤 각 exact `-LiteralPath`에 계산했다. link 검사는 target의 양끝 angle bracket을
  제거한 뒤 다시 실행해 모든 local link가 존재함을 확인했다.
- 재발 방지: PDF 작업 전 `Get-Command`와 번들 디렉터리 목록으로 실제 executable을 고정한다.
  PowerShell `-LiteralPath`에는 wildcard를 넣지 않고, wildcard가 필요하면 `-Path` 또는 선행
  `Get-ChildItem`을 쓴다.

### E037 — H1c-1a 정본 동기화 patch의 비고유 문맥으로 절 번호가 잠시 역전

- 분류: `PATCH_CONTEXT_AMBIGUITY / CAUGHT_BEFORE_VALIDATION / NO_RESEARCH_IMPACT`
- 문제: H1b 문서 끝에 23절을 붙일 때 여러 번 나타나는 동일 종료 문장을 문맥으로 사용해,
  첫 patch가 23절을 22절 바로 앞에 삽입했다. 또한 너무 많은 파일을 한 patch로 묶은 두 시도는
  한 파일의 문맥 불일치 때문에 쓰기 전 전체 거부됐다.
- 영향: 절 순서 오류는 즉시 `Select-String '^## 2[23]'`와 문서 tail 대조에서 발견됐고 최종
  검증 전 교정했다. 거부된 patch는 원자적으로 아무 파일도 바꾸지 않았다. 수학식·판정·actual
  artifact에는 영향이 없다.
- 교정: 잘못 들어간 23절 블록을 제거하고 22절의 고유한 마지막 문단 뒤에 다시 삽입했다.
  이후 정본 동기화는 파일별 또는 고유 section header가 포함된 작은 patch로 나눴다.
- 재발 방지: append-like patch는 마지막 한 줄만 매칭하지 말고 직전 section header나 고유 문장
  2개 이상을 함께 사용한다. 적용 직후 header 순서를 기계적으로 검사한다.

### E038 — Bennett et al. 2018을 처음에 arXiv 상태로만 과소분류

- 분류: `BIBLIOGRAPHIC_STATUS_UNDERCLASSIFICATION / CAUGHT_BEFORE_HANDOFF / NO_MATH_IMPACT`
- 문제: H1c-1a source JSON 초안에서 로컬 arXiv PDF의 표지만 보고 Bennett--Martin--O'Bryant--
  Rechnitzer 논문을 `PREPRINT_REVIEW_STATUS_NOT_ADOPTED_AS_THEOREM_INPUT`으로 적었다. 실제로는
  *Illinois Journal of Mathematics* 62 (2018), 427--532에 출판된 논문이다.
- 영향: 해당 정리의 식·범위와 `PARTIAL_INPUT`, `direct_substitute=false` 판정은 바뀌지 않는다.
  출판상태와 bibliography metadata만 부정확했다.
- 교정: 저자 publication page와 출판 PDF metadata를 대조해 DOI
  `10.1215/ijm/1552442669`, 권·쪽과 `PEER_REVIEWED` 상태로 고쳤다.
- 재발 방지: arXiv PDF를 읽었더라도 source registry를 확정하기 전 DOI·저자 publication list·
  journal landing page 중 하나에서 후속 출판 여부를 별도로 확인한다.

### E039 — H1c-1b.1 조사·작성 과정의 경로 추정과 문자열 escape 오류

- 분류: `TOOLING_AND_PATCH_CONSTRUCTION_ERROR / CAUGHT_BEFORE_VALIDATION / NO_RESEARCH_IMPACT`
- 문제:
  1. source 파일을 찾는 초기에 다시 `tmp/` 전역 검색을 사용해 접근 제한 경고를 냈고,
     일부 PDF·text 파일명을 실제 목록 확인 전에 추정해 `FILE_NOT_FOUND`를 냈다.
  2. 설치 여부를 먼저 확인하지 않고 한 PDF 추출 executable 경로를 추정했으며, PowerShell
     `python -c`에 실제 newline을 부정확하게 전달해 한 차례 구문 오류를 냈다.
  3. Markdown을 JavaScript 비-raw 문자열로 만들면서 `\to`의 `\t`가 탭으로 바뀌고 일부
     수식 escape가 깨졌다. 또한 여러 파일 patch를 한 번에 만들다가 한 hunk 문법 오류로
     해당 patch 호출이 거부됐다.
  4. 최종 FGKMT 오탈자 검색에서 PowerShell `-Path`에 배열과 추가 문자열을 잘못 조합해
     non-terminating parameter conversion error가 났는데, 뒤 명령이 계속되어 처음에는
     잘못된 PASS 문구도 함께 출력됐다.
- 영향: 모두 정본 검증 전의 읽기·작성 도구 단계 오류다. 잘못 생성된 새 Markdown은 전체
  재작성했고, 거부된 patch의 대상 파일은 적용 전후를 다시 대조했다. actual 실험 artifact,
  원본 논문, 최종 수학 판정에는 영향이 없다. 오탈자 검색은 올바른 단일 경로 배열로
  재실행해 16개 파일 issue 0을 확인했다.
- 교정: 정확한 파일 목록과 executable 존재 여부를 먼저 확인했고, Markdown은 raw 문자열 또는
  명시적 line array로 다시 만들었다. 탭·깨진 수식 검색과 `git diff --check`를 최종 gate에
  추가했다.
- 재발 방지: `tmp` 전역 검색 금지를 실제 명령 선택 단계에서 지킨다. 경로를 추측하지 않고
  `Get-ChildItem -LiteralPath`로 먼저 고정하며, 수식이 있는 patch는 raw 문자열과 작은
  파일별 hunk를 사용한다.

### E040 — H1c-1a JSON의 Maynard PDF provenance가 다른 논문을 가리킴

- 분류: `PROVENANCE_MISMATCH / CORRECTED / NO_MATH_CONCLUSION_CHANGE`
- 문제: `Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json`의 Maynard
  source 경로와 SHA-256이 실제로 인용한 `Dense Clusters of Primes in Subsets`가 아니라
  다른 Maynard PDF를 가리켰다. 수식 감사 자체는 올바른 author TeX를 읽어 수행했지만,
  기계 판독 provenance가 그 증거와 일치하지 않았다.
- 영향: Hypothesis 1(2), Proposition 9.2의 식과 `RATE_MISSING` 판정은 바뀌지 않는다.
  그러나 이전 JSON의 PDF hash만으로는 그 인용을 재현할 수 없었으므로 provenance 결함이다.
- 교정: 실제 출판본 경로
  `tmp/pdfs/h1b1a/Maynard2016_Dense_Clusters_published.pdf`와 SHA-256
  `8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098`로 교체하고
  단위시험에서 경로·hash를 고정했다.
- 재발 방지: source JSON을 쓸 때 제목, 첫 페이지, 인용 식이 있는 페이지, 파일 hash를 한 묶음으로
  대조한다. TeX와 PDF를 함께 썼으면 둘의 논문 identity가 같은지도 검사한다.

### E041 — H1c-1b.1 초안이 `x`와 실제 `x/2` 사이의 반복 dimension 경계를 놓침

- 분류: `MATHEMATICAL_SCOPE_ERROR / CAUGHT_BEFORE_HANDOFF / CANONICAL_STATUS_DOWNGRADED`
- 문제: 초기 초안은 `r=floor((log T)^(1/5))`인 endpoint-safe 모형에서 modulus capacity를
  닫은 뒤 이를 source의 선택과 동일시했다. 그러나 Sono/FMT는 원래 `x`에서
  `r_s=floor((log x)^(1/5))`를 고르고, actual Proposition 9.2는 `T=x/2`에서 호출한다.
  `r_s^5 <= log x < r_s^5+log 2`인 구간에서는 `r_s>(log T)^(1/5)`라 인쇄된 Maynard
  가정이 깨진다. 이 구간은 모든 큰 정수 `r_s`에서 반복된다.
- 영향: modulus가 충분하다는 부등식 자체는 유효하지만, 이를 곧바로 actual source parameter
  전체에 적용할 수 있다는 초안의 범위가 과대했다. 이 상태로는 Hypothesis 1(2)나 최종
  Sono 계수를 닫을 수 없다.
- 교정: 판정을 `PARTIAL`로 낮추고
  `r_T=floor((log(x/2))^(1/5)) in {r_s-1,r_s}` 및 `r_s-1` admissibility를 exact
  lemma로 추가했다. final coefficient transfer를 새 gate `H1c-1b.1a`로 분리하고
  transition-strip negative regression을 추가했다.
- 재발 방지: 정리의 endpoint를 `x`, `x/2`, `y`처럼 바꿀 때 성장률만 비교하지 말고,
  floor/ceiling이 있는 integer parameter의 모든 jump strip을 따로 검사한다.

### E042 — 전체 회귀시험의 live tee 검사가 비결정적 stream 순서를 가정

- 분류: `PREEXISTING_FLAKY_TEST / FIXED_DURING_VALIDATION / NO_PRODUCTION_CHANGE`
- 문제: H1c-1b.1 전체 회귀시험에서
  `test_stdout_stderr_blank_lines_and_exit_zero_are_preserved`가 352개 중 유일하게 실패했다.
  반복 5회에서 4회 PASS·1회 FAIL이었다. production helper는 stdout과 stderr를 별도 thread로
  즉시 배수하므로, stdout의 빈 줄 전에 stderr event가 합법적으로 끼어들 수 있다. 기존 시험은
  raw combined log 안에 `out-1\n\n`이 연속할 것을 가정했다.
- 영향: 실패 로그에도 두 번째 stdout marker 다음 빈 줄이 보존돼 있었다. 실시간 로깅 구현이나
  연구 계산 결과의 손실이 아니라 시험 oracle의 stream-order 가정 오류였다.
- 교정: production 코드는 바꾸지 않고, 시험이 marker를 따라 stdout만 재구성한 뒤
  `out-1\n\n`을 확인하도록 수정했다. 해당 시험 10회 반복 PASS, 이후 전체 352개 PASS다.
- 재발 방지: 병렬 stdout/stderr capture 시험은 전역 도착 순서를 고정하지 않는다. 각 stream의
  내부 순서·내용 보존과 종료코드를 검사하고, 서로 다른 stream의 interleaving은 허용한다.

### E043 — Bordignon 출판본 정리 번호를 `Theorem 4`로 축약 표기

- 분류: `BIBLIOGRAPHIC_LOCATOR_IMPRECISION / CORRECTED / NO_MATH_IMPACT`
- 문제: H1c-1a에서 Bordignon의 정리를 여러 정본에 `Theorem 4`라고 적었다. 확인한 NYJM
  출판본의 정확한 번호는 `Theorem 1.4`이고, exceptional-term 입력은 `Theorem 1.2`다.
- 영향: 사용한 식·\(A>3\) 조건·적용성 판정은 같은 정리를 가리켜 수학 결론은 변하지 않지만,
  독자가 출판본에서 바로 찾기에는 locator가 부정확했다.
- 교정: 활성 정본·JSON·상위 threshold review를 `Theorem 1.4`와 `Theorem 1.2`로 고쳤다.
- 재발 방지: 논문 제목이나 내부 절 번호가 다른 버전 사이에서 바뀔 수 있으므로, 최종 locator는
  hash가 고정된 실제 채택 출판본의 목차와 theorem heading에서 복사한다.

### E044 — Markdown backtick이 포함된 patch 문자열 구성 실패

- 분류: `TOOLING_QUOTING_ERROR / NO_FILE_CHANGE / NO_RESEARCH_IMPACT`
- 문제: H1c-1b.1a 작성 중 JavaScript template literal 안에 Markdown backtick을 그대로
  넣어 patch 호출을 구성했고, 문자열이 조기에 닫혀 도구 실행이 실패했다. 이후 한 번은
  여러 파일을 한 patch에 묶으면서 한 파일의 context 불일치 때문에 전체 patch가 적용되지 않았다.
- 영향: 두 경우 모두 patch 검증 단계에서 멈춰 파일은 바뀌지 않았고 수학 결과·실험 산출물에는
  영향이 없다.
- 교정: backtick은 placeholder 뒤 `String.fromCharCode(96)`으로 복원하고, 서로 다른 문서는
  작은 독립 patch로 나눠 적용했다.
- 재발 방지: Markdown/TeX가 긴 patch는 제어문자를 literal template에 넣지 않고,
  적용 전후 `git diff`와 대상 문맥을 작은 단위로 확인한다.

### E045 — PDF skill 설치 경로를 복수형으로 추정

- 분류: `LOCAL_PATH_ASSUMPTION / READ_ONLY_FAILURE / NO_RESEARCH_IMPACT`
- 문제: PDF 작업 규약을 읽을 때 실제 `.../pdf/...` 대신 `.../pdfs/...` 경로를 먼저
  추정해 한 차례 `FILE_NOT_FOUND`가 발생했다.
- 영향: 읽기 전용 실패였고 source PDF나 연구 파일은 변경되지 않았다.
- 교정: 세션에 제공된 skill catalog의 exact path를 다시 사용해 `SKILL.md` 전체를 읽었다.
- 재발 방지: skill 경로는 디렉터리명을 추측하지 않고 catalog에 표시된 값을 그대로 사용한다.

### E046 — T1 기계 원장의 `sigma*y` 주항에 `/log x`를 잘못 기록

- 분류: `PROVENANCE_FORMULA_ERROR / CANONICAL_LEDGER_CORRECTED / NO_EMPIRICAL_ARTIFACT_IMPACT`
- 문제: `Sono_FMT_T1_proof_obligations_v1.json`의 `SIV-03`이
  \(\sigma y\)의 주항을 \(80cx\log_2x/\log x\)로 기록했다. FMT (6.12),
  FGKMT (6.11), Sono p.542의 식은 \(80cx\log_2x\)이며, `/log x`는
  survivor prime count \(\sigma y/\log x\)에만 붙는다.
- 영향: proof-obligation 설명의 차원과 provenance가 잘못됐다. 이 JSON 식은 기존
  maximal-gap empirical 계산이나 actual experiment의 수치 입력으로 사용되지 않았으므로
  기존 실험 산출물을 폐기할 필요는 없다.
- 교정: T1 JSON과 사람이 읽는 원장을 원문 식으로 고치고, H1c-1b.1a test가
  `SIV-03`의 정확한 주항과 `26/25` finite target을 검사하게 했다.
- 재발 방지: normalized count와 unnormalized mass를 별도 symbol·행으로 유지하고,
  원문 equation number와 단위를 함께 대조한다.

### E047 — 갱신한 회귀시험에서 successor JSON key를 추측

- 분류: `TEST_SCHEMA_ASSUMPTION / CAUGHT_BY_TARGETED_TEST / NO_RESEARCH_IMPACT`
- 문제: 과거 `next_gate` 문자열을 새 successor로 바꾸는 시험에서 실제 key
  `explicit_sigma_cutoff_closed`를 읽지 않고
  `explicit_sigma_y_cutoff_proved`라고 추측해 표적시험 2개가 `KeyError`로 실패했다.
- 영향: production JSON이나 수학 계약이 아니라 새 시험 코드만 잘못됐고, 첫 표적 검증에서
  발견되어 정본·결과에는 영향이 없다.
- 교정: 실제 JSON을 출력해 schema를 확인한 뒤 두 시험을 정확한 key로 수정했다.
- 재발 방지: 여러 원장 사이의 필드명을 연결할 때 의미상 비슷한 이름을 추측하지 않고,
  strict parse한 실제 key 또는 공통 schema contract를 먼저 확인한다.

### E048 — 금지 철자 검사 결과 문구가 금지 철자 자체를 다시 기록

- 분류: `VOCABULARY_SELF_REFERENCE / HISTORICAL_METADATA_CORRECTED / NO_MATH_IMPACT`
- 문제: 직전 완료 원장과 handoff가 금지된 네 글자 약어의 scan 결과를 설명하면서 그 철자를
  literal로 다시 적었다. 당시 제한된 핵심 파일 scan은 0건이었지만, 이후 추가된 저장소 전체
  어휘 회귀시험은 이 자기참조 2건을 정확히 실패로 잡았다.
- 영향: 연구 명칭을 실제 본문에서 잘못 사용한 것은 아니고 검증 로그 설명 2줄의 문제다.
  수학 결과·실험 산출물에는 영향이 없다.
- 교정: 기존 handoff와 완료 원장은 불변 이력이므로 직접 수정한 초안 patch를 되돌렸다.
  회귀시험은 오직 그 두 archive 유형의 정확한 역사적 `오탈자 scan` meta label만
  검사 대상에서 제거하고, 그 밖의 본문·파일명은 계속 엄격히 실패시킨다.
- 재발 방지: 새 검증 결과를 기록할 때 forbidden literal을 출력하지 않고 중립 label을
  사용한다. 기존 handoff·완료 원장의 교정이 필요해도 원본을 패치하지 않고 새 handoff와
  오류 원장에 correction을 남긴다.

### E049 — 변경 파일 정적검사의 PowerShell 배열을 중첩해 경로를 합침

- 분류: `VALIDATION_COMMAND_ERROR / INVALID_CHECK_OUTPUT_DISCARDED / NO_FILE_CHANGE`
- 문제: 변경·신규 파일 목록을 `@((git ...), (git ...))`로 만들면서 두 결과 묶음이
  각각 하나의 문자열처럼 처리됐다. 또한 루트 파일의 `Split-Path -Parent`가 빈 문자열인
  경우를 처리하지 않아 local-link 검사에서 `Join-Path` 오류가 반복됐다.
- 영향: 최초 local-link·control-character 결과는 무효다. `git diff --check` 자체는
  별도로 exit 0이었고 파일 변경은 없었다.
- 교정: 빈 배열에 각 git 결과를 `+=`로 추가하고, parent가 비면 `.`을 사용하는
  교정 명령으로 전부 다시 검사한다.
- 재발 방지: 검사 결과를 PASS로 쓰기 전에 입력 파일 수·첫 항목·마지막 항목을 출력하고,
  검사 도중 PowerShell non-terminating error가 하나라도 있으면 전체 결과를 폐기한다.

### E050 — strict JSON 재검증에 case-insensitive PowerShell parser를 사용

- 분류: `VALIDATION_TOOL_MISMATCH / INVALID_CHECK_OUTPUT_DISCARDED / NO_FILE_CHANGE`
- 문제: 최종 정적검사에서 `ConvertFrom-Json`을 사용했는데, 기존 theory JSON의
  합법적인 대소문자 구별 key `f`와 `F`를 PowerShell이 같은 key로 취급해 중단됐다.
- 영향: JSON 자체의 문법 오류가 아니며 앞선 Python `json.loads` 24/24 PASS와
  단위시험 결과에는 영향이 없다. 이 최종 복합검사 결과만 폐기했다.
- 교정: JSON strict parse는 프로젝트 Python의 `json.loads`로만 다시 실행하고,
  나머지 link·control·diff 검사를 독립적으로 재실행한다.
- 재발 방지: JSON에 대소문자 구별 key가 있을 수 있는 저장소에서는
  Windows PowerShell 5.1 `ConvertFrom-Json`을 strict schema oracle로 사용하지 않는다.

### E051 — 과거 commit 승인을 현재 turn까지 확장 해석

- 분류: `AUTHORIZATION_SCOPE_ERROR / COMMIT_REJECTED / INDEX_RESTORED / NO_COMMIT_CREATED`
- 문제: 현재 사용자는 한국어 commit 메시지의 “제안”을 요청했지만, 이전 대화의 로컬
  commit 승인이 이번 변경에도 이어진다고 넓게 해석해 29개 명시 경로를 stage하고
  `git commit`을 요청했다.
- 영향: 승인 검토가 commit을 실행 전에 거부해 새 commit은 생성되지 않았다.
  작업 파일은 바뀌지 않았고, Git index에 있던 29개 항목은 즉시 명시 경로
  `git restore --staged`로 해제해 staged count 0을 확인했다.
- 교정: handoff와 작업원장을 “commit 미수행, 메시지 제안만 제공”으로 고쳤다.
- 재발 방지: 과거 commit 승인을 standing approval로 추론하지 않는다. 현재 turn에서
  commit 실행을 명시하지 않고 메시지 제안만 요구하면 stage·commit하지 않는다.

### E052 — 학술 PDF URL의 HTML 응답을 확장자만 보고 저장

- 분류: `SOURCE_DOWNLOAD_VALIDATION_ERROR / CAUGHT_BEFORE_USE / NO_RESEARCH_IMPACT`
- 문제: Dusart 2018 출판본을 찾는 과정에서 Springer URL의 3,038-byte HTML 응답을
  `.pdf` 이름으로 저장했다. HTTP 요청 성공과 파일 확장자만으로 PDF임을 가정한 오류다.
- 영향: signature와 `pdfinfo` 검사에서 바로 발견했고, 해당 파일은 증명·hash registry·인용에
  사용하지 않았다.
- 교정: 주 증명은 공식 Project Euclid의 Rosser--Schoenfeld 1962 PDF를 직접 채택했고,
  Dusart 2010 arXiv PDF는 보조 대조로만 사용했다.
- 재발 방지: 다운로드한 학술자료는 사용 전에 `%PDF-` signature, parser 성공, 제목 첫 페이지,
  필요한 theorem 페이지를 모두 확인한다.

### E053 — PowerShell regex와 Windows `rg` glob 구문을 Unix식으로 구성

- 분류: `READ_ONLY_COMMAND_QUOTING_ERROR / CORRECTED / NO_FILE_IMPACT`
- 문제: source landing page의 href를 뽑을 때 한 차례 따옴표를 잘못 구성했고,
  `rg tmp/path/*.txt` 같은 Unix식 경로 glob을 Windows에서 세 차례 사용해 `os error 123`을 냈다.
- 영향: 모두 읽기 전용 검색 실패다. 연구 파일과 source PDF는 바뀌지 않았으며,
  `rg --glob '*.txt' <directory>` 형식으로 즉시 재실행했다.
- 재발 방지: Windows에서는 wildcard를 경로 문자열에 붙이지 않고 `rg --glob` 또는
  `Get-ChildItem -Filter`를 사용한다. regex는 실제 landing HTML의 작은 sample로 먼저 시험한다.

### E054 — Axler 출판 PDF의 표시식을 안전성 검토 없이 채택할 위험

- 분류: `SOURCE_FORMULA_HAZARD / REJECTED_BEFORE_ADOPTION / NO_RESEARCH_IMPACT`
- 문제: Axler 2018 Proposition 9의 출판 PDF 위쪽 표시식은 적힌 그대로면 필요한 점근 주항이
  없어 (P(x)\sim e^{-\gamma}/\log x)와 양립하지 않는다. 후속 논문이라는 이유만으로 이 식을
  자동 채택했다면 잘못된 상계를 쓸 수 있었다.
- 영향: 실제 증명에는 채택하지 않았다. Axler p.19의 Rosser--Schoenfeld 재인용만 대조하고,
  원 Rosser--Schoenfeld Theorem 7을 직접 사용했다.
- 재발 방지: 더 최신 source라도 부등식의 차원·극한·방향을 먼저 sanity-check하고, 이상하면
  원 인용 정리와 판본 차이를 대조한다.

### E055 — T1 source hash를 patch에서 한 글자 잘못 전사

- 분류: `PROVENANCE_TRANSCRIPTION_ERROR / IMMEDIATELY_CORRECTED / NO_RESEARCH_IMPACT`
- 문제: Rosser--Schoenfeld PDF SHA-256을 T1 JSON에 추가하는 첫 patch에서 `bceb` 중 한 글자를
  빠뜨렸다.
- 영향: 다음 확인에서 즉시 실제 `Get-FileHash` 값과 대조해 고쳤고, validation이나 commit 전이라
  잘못된 provenance가 정본으로 확정되지 않았다.
- 재발 방지: 긴 hash는 화면에서 옮겨 쓰지 않고 hash 출력과 JSON을 자동 회귀시험으로 대조한다.

### E056 — SIV-03 승격 뒤 predecessor 회귀시험의 옛 oracle을 한 곳 남김

- 분류: `STALE_TEST_EXPECTATION / CAUGHT_BY_TARGETED_TEST / NO_MATH_IMPACT`
- 문제: T1의 `SIV-03.explicit_bound`를 finite inequality로 갱신했지만 H1c-1b.1a 회귀시험 한 곳은
  과거 asymptotic 문자열을 계속 기대했다. 첫 교정 뒤에는 notes에 `26/25`가 있어야 한다는
  기존 provenance assertion을 새 문구가 만족하지 않아 표적시험이 한 번 더 실패했다.
- 영향: 새 수학식이나 production code의 실패가 아니라 test oracle 동기화 누락이다.
- 교정: 새 exact finite 식과 `EXPLICIT` 상태를 검사하도록 바꾸고, notes에도 proved multiplier와
  `26/25` 목표 관계를 명시한 뒤 표적시험을 재실행한다.
- 재발 방지: machine ledger의 status·formula를 바꿀 때 해당 row를 읽는 모든 시험을
  `rg --glob '*.py'`로 먼저 열거한다.

### E057 — 새 증명 문서의 인라인 LaTeX 구분자와 닫는 display 구분자를 손상

- 분류: `MARKDOWN_MATH_SERIALIZATION_ERROR / CAUGHT_BEFORE_FINAL_VALIDATION / NO_MATH_IMPACT`
- 문제: JavaScript 문자열을 거쳐 Markdown patch를 만들면서 일부 `\(\cdot\)` 인라인
  구분자의 backslash, 두 `\qquad`, 한 `\[` display 식의 닫는 `\]`가 빠졌다. 또한
  `\varphi`의 `\v`가 제어문자 U+000B로 바뀐 한 곳이 있었다.
- 영향: 문서 렌더링과 가독성의 결함이다. JSON 수식, Python exact arithmetic, 단위시험의
  수학 결론에는 영향이 없으며 전체 검증과 commit 전에 발견했다.
- 교정: 새 theory·review 문서의 인라인 수식은 `$...$`로 통일하고, display delimiter와
  제어문자를 전수검사해 복원했다.
- 재발 방지: Markdown 수식 patch에는 raw 문자열을 쓰더라도 작성 직후 changed Markdown 전체에
  대해 control-character scan, `\[`·`\]` 개수와 순서 검사, 의심스러운 bare TeX
  token 검사를 자동 수행한다. 오류 원장에 이미 같은 계열의 경고가 있어도 검사를 생략하지 않는다.

### E058 — 전체 unittest를 알려진 restricted sandbox에서 먼저 실행

- 분류: `VALIDATION_ENVIRONMENT_ERROR / INVALID_RUN_DISCARDED / VALID_RERUN_PASS`
- 문제: 이 저장소의 `TemporaryDirectory`·multiprocessing 시험은 restricted sandbox에서
  권한 실패가 난다는 기존 규칙을 확인하고도, 전체 364개 suite의 첫 실행을 sandbox 안에서
  시작했다. 그 결과 코드 오류가 아닌 `PermissionError` 82건이 발생했다.
- 영향: 첫 실행은 환경이 잘못된 무효 판정이며 연구 코드·산출물은 변경하지 않았다.
- 교정: 사용자가 이미 허가한 정상 로컬 권한에서 동일 suite를 다시 실행해
  `Ran 364 tests ... OK`를 확인했다.
- 재발 방지: 표적 pure unit test와 달리 전체 suite는 첫 실행부터 정상 로컬 권한을 사용하고,
  sandbox 결과와 code result를 별도 기록한다.

### E059 — 완료 원장 rename의 staged 경로 수를 2개로 잘못 예상

- 분류: `GIT_RENAME_AUDIT_ASSUMPTION / CORRECT_STATE_VERIFIED / NO_CONTENT_IMPACT`
- 문제: 완료 원장의 옛 경로 삭제와 새 `-done` 경로 추가를 stage한 뒤
  `git diff --cached --name-only`가 두 줄을 출력해야 한다고 가정했다. Git은 이를
  `R087` rename 한 항목으로 인식했으므로 사용자 정의 감사 조건만 exit 2가 됐다.
- 영향: rename과 index 내용은 정확했고, 파일 손실이나 잘못된 추가는 없었다.
- 교정: `git diff --cached --name-status`와 `--summary`에서 정확한
  old→new 경로와 `R087`, `git diff --cached --check` PASS를 확인했다.
- 재발 방지: rename 감사에서는 raw 경로 개수를 고정하지 않고 status code와 old/new pair를
  검증한다.

### E060 — Maynard 원정의만 확인하고 FGKMT의 수정 interval 정의를 놓침

- 분류: `PRIMARY_APPLICATION_SEMANTICS_ERROR / CORRECTED_BEFORE_PARENT_PROMOTION`
- 문제: H1c-1b.3에서 Maynard 2016 Definition (2.1)의 \([T,2T)\)를 확인했지만,
  FGKMT printed p.95가 \(\mathcal A(T)=\{T\le n\le2T\}\)로 재정의한다는 사실을
  actual target 판정에 반영하지 않았다. 그 결과 정확한 Maynard-generic bridge를
  “actual FGKMT target”이라고 잘못 이름 붙였다.
- 영향: 과거 half-open endpoint correction과 실제 closed correction은 모두 한 modulus당
  절댓값 1 이하라서 H1c-1b.4c의 수치 envelope는 안전하다. H1(2), `SIV-08`,
  \(X_{\rm cert}\)를 아직 승격하지 않았으므로 잘못된 theorem threshold나 actual 실험 결과는
  생성되지 않았다. 다만 FGKMT Section 8 외부 \((T,2T]\) 합과 closed Theorem 6 합 사이의
  weighted lower-endpoint 의무가 새로 명시적으로 드러났다.
- 교정: H1c-1b.3r1에서 source \((T,2T]\), FGKMT Hypothesis target \([T,2T]\),
  외부 prime set \((T,2T]\), Maynard 원정의 \([T,2T)\)를 네 칸으로 분리하고 exact toy
  회귀를 추가했다. 기존 문서는 역사적 유도로 보존하되 actual label 철회 notice를 붙였다.
- 재발 방지: 선행정리를 인용하는 논문이 “modified form”을 사용하면 원정리뿐 아니라
  인용 논문의 지역 정의, theorem 문장, 실제 호출점과 최종 외부합의 endpoint를 모두 대조한다.

### E061 — Markdown 수식의 `\\f`가 U+000C로 변환됐고 첫 검사가 untracked 파일을 누락

- 분류:
  `MARKDOWN_CONTROL_CHARACTER / INCOMPLETE_STATIC_SCAN / CAUGHT_BEFORE_COMMIT / NO_MATH_IMPACT`
- 문제: JavaScript 문자열을 거쳐 작성된 수식의 `\\frac` 두 곳에서 `\\f`가
  form-feed U+000C로 바뀌었다. 한 곳은 새 H1c-1b.4e 문서, 다른 한 곳은 기존 H1b-2a.3
  문서였다. 첫 검사는 `git diff --name-only`만 사용해 untracked인 새 4e 문서를
  검사 대상에서 누락했다.
- 영향: Markdown 렌더링·검색 결함이며 Python/JSON 수식과 증명 판정에는 영향이 없다.
  전체 검증과 commit 전에 repository-wide scan으로 발견했다.
- 교정: 두 U+000C를 literal `\\frac`로 복구하고 새 문서의 누락된 인라인 수식
  여는 구분자도 함께 고쳤다.
- 재발 방지: 변경 파일 검사는 tracked diff뿐 아니라 `git status --porcelain`의
  untracked 경로도 포함한다. 최종 단계에서는 `docs/source/tests/ai_dev_tool`의
  Markdown·Python·JSON 전체를 control-character scan한다.

### E062 — H1c-1b.4e 정본 동기화 뒤 과거 회귀 oracle 네 곳을 남김

- 분류: `STALE_TEST_AND_PROVENANCE_ORACLE / CAUGHT_BY_TARGETED_TEST / NO_MATH_IMPACT`
- 문제: H1c parent next gate와 H1b schema를 갱신한 뒤 두 테스트는 옛
  `H1c-1b.4`·`1.10.0`을 계속 기대했다. 또 T1 `SIV-08.notes`를
  간결화하면서 선행 단계 `H1c-1b.1`과 `H1c-1b.2` 이름을 빼 기존
  provenance 회귀 두 건이 실패했다.
- 영향: 108개 표적시험 중 4개가 실패했지만 새 helper의 수치·수학 시험은 모두 통과했다.
  실패 실행은 무효로 두었고 commit 전이라 정본 오염은 없다.
- 교정: T1 notes에 선행 단계 이력을 복원하고 두 oracle을 현재 next gate와 schema에 맞췄다.
- 재실행에서 source-name provenance oracle 한 곳이 `Bordignon 2021`이라는 exact
  식별자를 요구했으나 요약문이 `Bordignon source`로만 적혀 1건이 더 실패했다.
  연도 식별자를 복원하고 다시 검증한다.
- 재발 방지: parent JSON의 `schema_version`, `next_gate`, provenance
  narrative를 바꿀 때 해당 key와 선행 gate 이름을 읽는 모든 테스트를 먼저 열거한다.

### E063 — case-insensitive JSON parser와 단순 delimiter count로 유효 파일을 오탐

- 분류: `STATIC_VALIDATION_FALSE_POSITIVE / INVALID_CHECK_DISCARDED / NO_CONTENT_IMPACT`
- 문제: PowerShell `ConvertFrom-Json` 기본 모드는 기존 JSON의 서로 다른
  `f`/`F` key를 대소문자 충돌로 오인했다. 또 단순 `\\(` 개수
  검사는 display 식의 LaTeX `\\\\(q,B)`를 inline delimiter로 잘못 세었다.
- 영향: 두 1차 정적검사는 무효였고 파일 문법·수식에는 문제가 없었다.
- 교정: JSON은 `-AsHashtable`로 33/33 parse했고, delimiter는 앞에 추가
  backslash가 없는 token만 세는 escape-aware 검사로 20/20 문서를 통과시켰다.
- 재발 방지: case-sensitive JSON key를 허용하는 parser와 escape-aware Markdown
  delimiter 검사를 첫 실행부터 사용한다.

### E064 — 최종 제어문자 검사가 보존된 `tmp` 전체를 불필요하게 순회

- 분류: `STATIC_VALIDATION_SCOPE_ERROR / ACCESS_DENIED_NOISE / INVALID_CHECK_DISCARDED / NO_CONTENT_IMPACT`
- 문제: H1c-1b.4e 최종 확인에서 저장소 루트 아래 모든 텍스트 확장자를 재귀 순회했다.
  그 결과 접근이 제한된 과거 임시 시험 디렉터리에서 다수의 `Access denied`가 발생했고,
  PDF 추출 텍스트와 과거 handoff에 이미 존재하던 제어문자까지 현재 변경의 문제처럼 섞였다.
- 영향: 해당 검사는 완료 판정에 사용하지 않고 폐기했다. 새 변경 35개를 Git의
  tracked diff와 untracked 목록으로 다시 고정해 검사한 결과 제어문자 0건이었다.
- 교정: Unicode 경로가 Git의 quoted path로 바뀌지 않도록
  `git -c core.quotepath=false`를 사용했다. 커밋 대상 35개 전체와 Markdown 21개를
  다시 읽어 제어문자 0건, local link 163/163, escape-aware 수식 구분자 0건을 확인했다.
- 재발 방지: 변경 검사는 `git diff --name-only`와 `git ls-files --others
  --exclude-standard`의 합집합에 한정한다. 보존된 `tmp`·과거 artifact까지 전수 검사하려면
  별도 목적·접근권한·기존 결함 baseline을 먼저 정의한다.

### E065 — H1b-P92a 패치 문자열·PDF 도구 가용성 처리 실패

- 분류: TOOL_INPUT_ERROR / FAILED_BEFORE_WRITE / NO_RESEARCH_RESULT_IMPACT
- 증상: JavaScript raw template에 Markdown backtick을 넣어 SyntaxError가 두 번 발생했고,
  문서 add-file patch의 display 종료 두 줄에 + prefix를 빠뜨려 apply_patch 검증이 실패했다.
- 교정: 문서 본문 모든 줄에 patch prefix를 자동 부착하고, backtick이 필요한 patch는 일반
  문자열 배열로 조립했다. git apply 우회는 쓰지 않았다.
- PDF 처리에서도 fitz 및 pdftotext.exe가 없는 경로를 시도했고, 기본 출력 encoding에서
  문자 인코딩 오류가 있었다. 설치된 pypdf의 UTF-8 extraction과 Poppler rendering으로
  대체했다. 새 package를 임의로 설치하지 않았다.
- 영향: 실패한 패치는 파일을 바꾸지 않았다. raw PDF·actual dataset·실험 결과는 미변경이다.
- 재발 방지: patch와 실행 문자열을 별도 단계로 구성하고, PDF 도구 가용성과 encoding을
  먼저 확인한다. Markdown을 JS raw template에 넣을 때 backtick을 직접 섞지 않는다.

### E066 — fixed-k certificate를 growing-k 경로의 완료로 오해할 위험

- 분류: QUANTIFIER_COMPATIBILITY_GAP_FOUND / NO_INVALIDATION_OF_FIXED_PARAMETER_PROOF
- 발견: 기존 P94의 2^k 비교를 흡수하는 충분조건은 각 고정 k에서는 유효하지만,
  k=floor((log T)^(1/5))의 maximal growing 경로에 동시에 적용됨을 증명한 것이 아니다.
- 영향: “actual P94 parameterized explicit”라는 말을 growing-k 공통 cutoff까지 닫혔다고
  읽으면 과장이다. 실제 experiment 결과나 기존 fixed-parameter 부등식은 무효가 아니다.
- 조치: theory 44의 Cantelli 비교로 큰 k에서 I(F1)<=2I(F), J(F1)<=2J(F)를 증명해
  P92에는 적용했다. P94는 기존 certificate를 보존하고 growing-k 교정을 다음 gate로 남겼다.
- 재발 방지: “각 고정 parameter마다 충분조건 존재”와 “actual growing parameter 경로에서
  하나의 유한 cutoff 존재”를 별도 obligation으로 등록한다.

### E067 — H1b-P92a parent schema·시험 모듈 지정과 실행 순서 오류

- 분류: INTEGRATION_SCHEMA_MISMATCH / INVALID_TEST_COMMAND / VALIDATION_ORDER_ERROR
- 첫 통합 검사는 없는 시험 모듈 이름을 지정했고, 고정 obligation schema 안에 새 메모 field를
  넣어 43개 중 1 FAIL·1 import ERROR였다. 새 수학·수치 16개는 PASS했다.
- 메모 field를 schema 밖으로 옮긴 뒤 49개 재검사에서, actual closure 행의
  missing_numeric_inputs가 비어야 한다는 계약을 놓쳐 1 FAIL이었다.
- 이 두 번째 결과를 모델이 확인하기 전에 같은 도구 orchestration에서 전체 suite도
  시작했다. 이는 1차 실패를 고친 뒤 다음 검증으로 가야 하는 순서를 어긴 것이다.
  해당 전체 실행은 최종 성공 근거로 사용하지 않고 실패 baseline으로 보존한다.
- 교정 방향: actual child 안의 미결은 빈 목록으로 두고, 일반형·부모 합성의 미결을 별도
  actual_application_scope_notes에 보존한다. 검사 계약을 약화하지 않는다.
- 재발 방지: 시험 모듈은 rg --files로 먼저 찾는다. 의존 검증의 후속 실행은 반드시
  직전 exit_code==0일 때만 dispatch한다. JSON의 extra field/빈 목록 의미도 같이 확인한다.
- 최종 교정: schema 안의 actual-child 미결 목록은 비우고 general/parent 미결을 별도
  scope notes로 옮겼다. 검사 계약은 유지했다. 실패 baseline은 전체 434개 중 1 FAIL,
  67.993초였다. 이후 표적 49/49 PASS(0.044초)를 확인한 경우에만 전체를 dispatch했고,
  최종 전체 434/434 PASS(62.520초)였다.


### E068 — untracked 신규 Python 파일의 EOF 공백이 staged 검사에서 발견됨

- 분류: WHITESPACE_CHECK_SCOPE_GAP / CAUGHT_BEFORE_COMMIT
- 증상: stage 전 git diff --check에는 untracked 파일이 포함되지 않았다.
  stage 후 검사에서 신규 helper/test 두 파일의 마지막 빈 줄을 발견해 커밋을 중단했다.
- 교정: 마지막 빈 줄만 제거하고 코드 내용이 같음을 확인한 뒤 재검사한다.
  스테이징 경로 목록 20개는 정확했고 다른 파일이 섞인 문제는 아니었다.
- 재발 방지: 신규 파일은 stage 후 cached diff --check까지 통과해야 완료다.
  경로 allowlist 검사와 whitespace 검사 출력을 섞어 실패 유형을 혼동하지 않는다.

### E069 — 마감 검사 뒤의 git stat가 앞선 실패 종료코드를 덮음

- 분류: NATIVE_EXIT_CODE_CLOBBER / COMMITTED_DOCUMENT_WHITESPACE_ONLY
- 증상: 마감 스테이징에서 git diff --cached --check와 --stat를 같은 PowerShell 명령에
  연속 실행했다. 첫 검사는 새 handoff의 끝 빈 줄 1개를 보고했지만, 뒤의 --stat가 0으로
  끝나 전체 tool exit_code가 0이 됐다. 이를 잘못 통과로 취급해 commit 76872d2를 만들었다.
- 정확한 영향: handoff/202609091347_HANDOFF.md 마지막 빈 줄 1개가 남았다.
  proof commit 225f136의 source·수치·434개 PASS에는 영향이 없다.
  handoff 본문도 의미상 올바르며 새 과학적 오류나 actual 결과 변경은 없다.
- 처리: 기존 timestamp handoff의 불변 보존 규칙을 우선해 내용·이력을 다시 쓰지 않고
  이 경고를 명시적으로 기록한다. 공백 경고가 없는 마감이라고 주장하지 않는다.
- 재발 방지: native validation과 요약 명령을 각각 별도 tool 호출로 실행하고, 첫 결과의
  exit_code==0 및 오류 출력 확인 뒤에만 commit을 dispatch한다. 한 shell에서 여러
  native command가 꼭 필요하면 각 명령 직후 LASTEXITCODE를 별도 변수로 보존해
  실패 즉시 exit한다. ErrorActionPreference=Stop만으로 native exit를 처리했다고 믿지 않는다.
- 뒤따른 오류 기록 commit은 이 원장 한 파일만 변경한다. 과학 단계 재실행·새 actual
  실험·과거 handoff 변경은 하지 않는다.



### E070 — P92a에서 W-filter 정의의 source 간 차이를 명시하지 못함

- 분류: SOURCE_DEFINITION_SCOPE_OMISSION / FILTERED_PROOF_SCOPE_CORRECTED
- 발견: Maynard 출판 p.1530 (7.5)는 W-coprimality indicator를 명시하지만,
  FGKMT p.98 (7.4)의 literal 표시에는 없다. P91/P92 출판 proof는 W-good residue만 합한다.
- 이전 누락: P92a는 proof 안에서 W-good restriction을 사용하면서도 “actual FGKMT weight”
  표현에 이 조건을 명시하지 않았다. literal unfiltered weight로 읽으면 적용 범위가 과장된다.
- 영향: 기존 P92a 해석·수치 상계는 명시적 filtered weight에 대한 결과로 한정한다.
  실제 empirical prime-gap 산출물, recurrence 결과나 과거 데이터는 영향을 받지 않는다.
  전체 X_cert는 원래 OPEN이었고, 잘못된 최종 threshold를 배포한 것은 아니다.
- 조치: theory 45 §2에서 두 함수가 같지 않음을 toy·CRT 논증으로 설명하고, filtered
  construction의 shift·prime-slice indicator equality를 증명했다. theory 44/계약/helper/정본에
  명시적 W-filter와 literal-unfiltered-transfer 미인증 flag를 넣었다.
  unfiltered certificate 요청은 거부하는 negative regression을 추가했다.
- 한계: 공식 erratum이나 Sono theorem의 반례를 확인했다고 주장하지 않는다.
  공통 coefficient·weight·tau/u와 FMT 전체 합성은 여전히 후속 의무다.
- 재발 방지: theorem 번호뿐 아니라 호출되는 weight의 indicator, support, residue restriction을
  source 정의와 각 proof 첫 줄에서 직접 대조한다. 코드상 사용한 가정을 문서에서 생략하지 않는다.

### E071 — 이번 source inventory의 경미한 도구·경로 오류

- 폐기된 dependency alias는 “no longer available” 응답 뒤 mcp 버전으로 정상 조회했다.
- PowerShell rg에서 wildcard를 path 인자로 직접 넣어 os error 123이 반복됐다.
  사용자 지시나 파일 문제는 아니며 호출 형식 실수다. 최종 조회는 실제 경로 또는
  rg <pattern> <directory> -g <filename-pattern>으로 교정했다.
- theory 28의 경로를 추측해 FileNotFound를 냈고 rg --files로
  residual_moment_error_package 이름을 확인해 전체를 읽었다.
- PDF page index는 추측 오프셋에 기대지 않고 렌더된 printed page로 확인했다.
  P91은 PDF page 23--25, printed 1538--1540이다.
- raw GitHub web endpoint의 fetch 오류는 HTML primary source 조회로 보완했다.
- 실패한 읽기·일부가 성공한 혼합 출력은 검증 PASS로 계산하지 않았다.
  실제 연구 데이터·사용자 파일에는 영향이 없고 패키지를 설치하지 않았다.
- 이 경로 실수가 반복된 점은 효율상의 실제 실수다. 디렉터리+glob 옵션 원칙을
  실행 전에 확인하고, 발견되지 않은 파일명을 후속 보고에 쓰지 않는다.

### E072 — P94 actual local scale·끝점·support를 등호로 옮길 위험 교정

- 기존 theory 31의 고정-parameter P94 증명과 실제 FGKMT q 구간에 대한 적용을
  구분해야 했다. 실제 local scale은 외부 X가 아니라 T0=floor(Y)-floor(X)다.
  외부 R=(X/4)^(1/9)가 local T0의 허용 범위에 드는지 theory 46에서 별도로 증명했다.
- (X,Y] 정수 구간의 이동은 (T0,2T0]다. [T0,2T0]와 같은 집합으로 쓰지 않고
  비음성 상계로 연결했다. |q-hp|<=Y의 support 또한 임의 h=O(Y/X)에서 자동이 아니므로
  제거 전후 등호를 주장하지 않는다.
- 숨은 h 범위 상수 C_h와 log(C_h)<=L/4를 명시했다. C_h=1만 계산해 일반 범위를
  인증한 것으로 바꾸지 않는다.
- 원문에 대한 공식 erratum이나 전체 정리 반증을 주장하지 않는다. 원문/선행 proof hash는
  보존하며, 새 actual finite application의 누락 조건을 successor에서 닫았다.
- negative toy는 잘못된 closed equality, 원래 support의 자동 포함 및 h=h_i를 검출한다.
  실제 데이터 결과는 변경하지 않았고 X_cert로 승격하지 않았다.

### E073 — source 제목 오류·읽기 도구 호출 실패 공개

- theory 31의 arXiv:1804.06290 제목 표기가 잘못돼 있었다. 실제 제목은
  Weighted Average Number of Prime m-tuples lying on an Admissible k-tuple of Linear Forms다.
  원문 metadata로 확인해 새 theory 46/review 52에 정정했다. 이 후보를 finite proof
  입력으로 채택하지 않았고, 잘못된 제목을 근거로 lemma가 입증됐다고 주장하지 않는다.
- tmp 전체 rg는 오래된 sandbox fixture의 접근 거부를 출력했다. 범위를 tmp/pdfs의
  알려진 source로 좁혔으며 권한이나 기존 fixture를 변경하지 않았다.
- 이번에도 docs/method/theory/00*를 rg의 literal path 인자로 넣어 os error 123을
  한 번 냈다. 이미 알려진 호출 실수의 반복이다. 이후 읽기는 실제 파일명으로만 수행했다.
- 여러 큰 파일을 한 번에 ConvertTo-Json으로 읽은 출력에 Warning이 섞여 JSON parse가
  실패했다. 파일별 raw 읽기로 바꾸고 모든 파일을 정상 취득했다. 이 실패를 검증에 포함하지 않았다.
- apply_patch에서 같은 경로에 두 Update File block을 넣어 사전검증이 거부됐다.
  경로별 하나의 patch로 합쳐 정상 적용했다. git apply로 우회하지 않았다.
- 첫 문서 링크 검사에서 theory 46의 plaintext tau 표기가 Markdown 링크로 해석되어
  존재하지 않는 q 파일을 가리켰다. 수식 구분자를 명시해 교정했다. unit test 실패는
  아니지만 문서 검증의 실제 실패였으며 수정 전 결과를 PASS라고 기록하지 않는다.
- 넓은 dense-cluster 검색은 수학 외 결과가 섞였고 일부 DOI/HTML fetch는 실패했다.
  직접 출판본 PDF·지정 arXiv metadata 및 기존 local proof를 사용했다.
  조회 실패를 원문의 부재·정리 부재로 해석하지 않는다.

### E074 — 공통 정규화에서 숨기면 안 되는 양화·제곱비

- FGKMT/FMT의 u=u(r) 선언과 actual 식 (8.3)은 같은 것으로 자동 읽을 수 없다.
  actual u에는 X,B가 들어 있다. 임의로 phi(B)/B=1로 바꾸지 않고 u_X를 사용했다.
- theory 47은 fixed-X 확률 입력을 직접 증명하며 only-k 의존성은 미인증으로 남긴다.
  “원문 전체가 잘못됐다” 또는 “Sono 정리 반례”라는 주장은 하지 않는다.
- lambda의 common scalar를 weight에 옮기면 제곱해야 한다. exact nonzero toy는
  제곱을 빠뜨린 식을 반증하며 p마다 다른 alpha를 합 밖으로 꺼내지 않게 검산한다.
- B와 FMT B0는 서로 다른 parameter다. 삭제하는 소수 한 개의 weighted 비용을
  count atom 1과 동일시하지 않고 새 bound로 흡수했다. 실제 데이터는 변경하지 않았다.

### E075 — H1b-NORM 도구·문서·회귀 동기화 실수

- parent JSON과 theory 34 이름을 추측해 FileNotFound를 냈다. rg --files의 실제 이름으로
  재조회했다. 앞 inventory에서도 wildcard path 오류가 반복됐다. 사용자 파일 문제가 아니다.
- PDF 질의 확인용 -First forty는 정수가 아니라 실패했다. -First 40으로 교정했다.
  큰 출력 일부가 잘려 정확한 source 범위만 재읽었다. 실패한 읽기는 검증 PASS가 아니다.
- 최초 한국어 proof 초안에 일본어 두 문장이 섞였고, 마감 전 한국어로 교정했다.
- 표적 93개 첫 회귀는 1개 실패: parent schema 1.15.0으로 올린 뒤 시험 기대값이
  1.14.0에 남아 있었다. 실제 버전 변경을 반영하고 다시 93/93 PASS (0.292초, exit 0).
  수학 조건을 완화하거나 실패 검사를 삭제하지 않았다.
- proof PASS와 root X_cert OPEN을 분리하며, 원문·선행 proof의 10개 hash는 보존한다.

### E076 — H1b-DEP PDF 분류·도구·label 검사의 실제 오류

- 이전 PDF 질의 확인 중 존재하지 않는 Poppler 경로를 추측했다. 이번에는 실제 설치된
  pypdf/pypdfium2를 확인해 사용했다. PDF metadata가 None인 RS1962에서 producer를 바로
  읽어 AttributeError가 났고 nullable 처리 후 다섯 source 페이지를 다시 확인했다.
- RS1962는 native text PDF가 아니라 scan+숨은 텍스트층이었다. 이전 plus/minus·pi 오독은
  이 층에서 확인된 문제다. “문자 PDF도 모두 OCR이 필요하다”거나 native 추출기 탓으로
  일반화하지 않는다. 새 OCR은 수행하지 않았고 원본은 수정하지 않았다.
- 오류 원장 경로와 프로젝트 pdf skill 경로를 추측해 없는 파일을 조회했다. 실제 README와
  제공된 skill roots가 정본이다. 큰 출력이 잘리면 정확한 source 범위를 재읽었다.
- 첫 전용 20 tests 중 1개 실패: eq:S4Bound2를 ref 집합에 있을 것으로 잘못 기대했다.
  실제로는 P94 안의 label 정의이며 ref 호출이 아니다. 정의 존재와 ref 부재를 각각
  검사하도록 고쳤다. P95 미호출 판정이나 수학 가정을 완화하지 않았다.
- FMT 초고의 Corollary 3과 출판 FGKMT Corollary 4는 완전히 같은 정리가 아니다.
  codegree 외에도 부분집합 결론·finite rate가 남으므로 번호만 교체해 증명 완료로
  간주하지 않는다. p.82의 기존 codegree 논증을 새 발견으로 포장하지 않았다.
- 한 patch 호출의 JavaScript raw 문자열에 backtick 문자를 넣어 ReferenceError가 났다.
  파일 변경 전에 실패했으며 문자열 구분을 교정해 apply_patch로 재적용했다.

### E077 — H1b-COR1 원문 읽기·경로·출력 처리 실수

- 옛 dependency locator는 deprecated로 실패해 현재 mcp locator를 사용했다.
- native PDF text를 cp949 stdout으로 출력하다 UnicodeEncodeError가 났다.
  bundled Python -X utf8로 다시 추출해 성공했다. OCR 실패·원문 손상이 아니다.
- theory 47·오류 원장·H1c JSON의 경로를 추정해 없는 파일을 조회했고, Windows rg에
  literal wildcard path를 전달해 os error 123을 냈다. rg --files와 실제 handoff 경로로 재조회했다.
  반복된 실수이므로 새 파일 작업 전 검색한 정확한 경로를 변수/allowlist로 재사용한다.
- 여러 큰 문서를 한 JSON stdout에 실으려다 반환 문자열의 warning 때문에 JSON parse가 실패했다.
  내용을 읽지 않은 채 patch하지 않았고 파일별 bounded read로 전환했다.
- PDF 진행 안내 한 회를 일본어로 잘못 보냈다. 곧바로 한국어로 다시 설명했다.
- 수학 검산은 sigma 하계의 분자/분모 방향, conditioning 분모, 중복점과 mean!=1 비용을
  필수 검사로 삼았다. toy PASS를 전 범위 증명이나 root X_cert 인증으로 확대하지 않는다.
- 위 도구·언어 오류는 새 source proof 작성 전/문서 조회에서 발생했고 실제 데이터 변경은 없다.

### E078 — X_cert 투자 가치 검토의 조회 범위·locator 재사용 실수

- 분류: CORRECTED_BEFORE_ACTUAL / INVALID_RESULT_NONE.
- 기존 handoff에 정확한 오류 원장 경로가 있었는데도 07로 시작하는 없는 경로를 한 번 조회했다.
  실제 05 원장을 다시 읽었다. 앞선 E076/E077과 같은 재발이며 경로를 추측하지 않아야 한다.
- 전체 tmp를 파일 검색 범위에 포함해 예전 sandbox 임시폴더의 접근 거부 메시지가 다수 발생했고,
  여러 출력이 잘렸다. 권한이나 파일을 변경하지 않고 이미 알려진 tmp/pdfs 하위로 범위를 좁혔다.
  필요한 source·문서는 분할해서 다시 확인했다. 접근 거부는 논문·연구 코드 오류가 아니다.
- deprecated dependency locator를 다시 호출했다. 현재 mcp locator로 조회한 뒤 기존 PDF 도구를
  사용했다. Sono DOI open 실패는 공식 저널 페이지와 보존된 문헌으로 보완했다.
- PDF 판독은 RS1962 p.69의 스캔+숨은 텍스트층을 확인하고 원본 화면에서 핵심 식을 대조했다.
  새 OCR·원본 수정·actual 실험을 하지 않았고, 이 조회 오류가 과학 산출물을 바꾸지 않았다.
- 설명상 위험도 교정했다: 기존 범위에서 부등식의 실패가 관측된 것이 아니다. 미완성 X_cert와
  보조변수 cutoff를 “그 이하에서 부등식이 거짓”이라는 뜻으로 설명해서는 안 된다.

### E079 — H1b-COV2 초안의 LaTeX escape·smooth 적분·식 번호 교정

- 분류: `CORRECTED_BEFORE_COMMIT / INVALID_RESULT_NONE`.
- theory 55 최초 초안을 JavaScript 일반 문자열로 구성하면서 `\\varepsilon`, `\\vartheta`,
  `\\beta`, `\\rho` 일부가 제어문자 또는 누락된 backslash로 저장됐다. commit 전에 byte/문자
  감사를 거쳐 모두 교정했다. 최종 사람 검토에서 남아 있던 inline math delimiter 누락도
  복원했다. actual 계산·실험 산출물은 없었다.
- 최초 smooth-number 설명의 세 구간 `Ein` 상계는 필요한 중간부등식이 충분히 전개되지 않아
  그대로는 project proof로 채택하기 어려웠다. Rosser--Schoenfeld Theorem 9의 전 범위
  theta 상계와 감소함수 Stieltjes 부분적분으로 다시 증명해
  `21/20 * 27/25 = 567/500 < 189/160`을 얻었다. 원문 printed pp.65, 70--71도 새로 대조했다.
- 식 번호를 한꺼번에 미는 임시 문자열 치환이 연쇄 적용되어 여러 식이 `55.39`가 된 한 차례
  편집 오류가 있었다. 번호 55.1--55.39의 유일성·연속성을 재검사해 복구했다.
- 전체 `tmp`를 대상으로 한 `rg`가 이미 알려진 접근 제한 임시폴더를 다시 만나 출력이 잘렸다.
  필요한 근거는 `tmp/pdfs/h1bcov2`와 정확한 source 파일로 범위를 좁혀 재조회했다.
- 첫 control-character 진단용 one-liner의 escape도 잘못되어 newline을 문제문자로 세는 무효
  출력이 생겼다. 해당 판정은 폐기하고 별도 strict UTF-8/byte 검사로 다시 확인한다.

### E080 — COV2 최종 정적감사에서 PowerShell colon 변수 파싱 오류 재발

- 분류: `CORRECTED_BEFORE_COMMIT / INVALID_RESULT_NONE`.
- E079와 작업원장에 같은 유형의 예방 기록이 있었는데도, 첫 최종 정적감사 명령에서
  `"${file}:$i:$code"`를 사용했다. PowerShell은 colon 바로 앞의 `$i`를 잘못된 변수
  참조로 해석해 parser 단계에서 중단했다.
- 명령은 파일을 읽기 전에 실패해 연구 코드·문서·실험 결과를 변경하지 않았다. 모든 colon
  앞 변수를 `${file}:${i}:${code}`로 명시한 뒤 동일 감사를 다시 실행했고, 25파일의 strict
  UTF-8·제어문자 검사가 issue 0으로 통과했다.
- 재발 방지: PowerShell 보간 문자열에서 변수 바로 다음에 colon이 오면 첫 변수뿐 아니라
  **모든 해당 변수**를 `${...}`로 감싼다. 검증 명령의 성공 출력이 없으면 그 검증은
  수행되지 않은 것으로 기록한다.
- 이어 작성한 인라인-math 누락 정규식은 표시수식 내부의 정상 괄호까지 문제로 잡는
  과잉탐지였다. 그 출력은 폐기했고 수식 delimiter는 사람 검토로 교정했다. 최종 자동 증거는
  strict UTF-8·제어문자·끝 공백, JSON parse, 연속 식번호, 링크, 회귀검사처럼 판정 규칙이
  명확한 항목으로 제한한다.
- closure 링크 검사 한 줄에서는 `foreach($m in[regex]...)`처럼 `in` 뒤 공백을 빠뜨려
  PowerShell parser 오류를 한 번 더 냈다. 파일 변경 전 실패였으며
  `foreach($m in ([regex]::Matches(...)))`로 고친 동일 검사는 handoff local link 9개와
  본체 commit object를 issue 0으로 확인했다.

### E081 — H1b-COV2 handoff 초안의 전체 commit hash 환각

- 분류: `CORRECTED_BEFORE_COMMIT / PROVENANCE_CONTAMINATION_NONE`.
- 본체 commit의 짧은 해시 `5629565`만 확인한 상태에서 전체 40자 해시를 조회하지 않고
  임의의 나머지 문자를 붙여 handoff 초안에 적었다. Git object를 가리키지 않는 잘못된
  provenance였으며 수학 결과·코드·이미 완료된 본체 commit 자체에는 영향이 없다.
- handoff를 commit하기 전에 `git rev-parse HEAD`로 실제
  `5629565b8a5cafd742134eeafb72848c65314f04`를 확인해 교정했다.
- 재발 방지: 전체 hash가 필요한 문서는 짧은 console hash를 확장하지 말고 반드시
  `git rev-parse <commit>`의 출력을 그대로 사용한다. 문서에 쓴 hash는 commit 전
  `git cat-file -e <hash>^{commit}`으로 존재 여부도 검사한다.

### E082 — Lean 전수 원장 구축의 작업 순서·provenance·sandbox 오류

- 분류: `CORRECTED_BEFORE_COMMIT / INVALID_RESULT_NONE`.
- `FGKMTSono.lean`에 새 target import를 먼저 넣고 target 파일 생성과 build를 병렬화해 최초
  build가 `no such file ... TheoryVerification.lean`으로 실패했다. 기존 Lean 설치나 사용자
  scaffold 문제가 아니라 작업 순서 오류다. target 생성 뒤 직접 kernel 검사와 전체
  `lake build`를 모두 exit 0으로 다시 수행했다.
- Theory 27의 식 (27.9)–(27.13)에 누락된 display 종료기호 5개를 발견하고 처음에는 원문을
  교정했으나, downstream JSON이 이 역사 문서의 SHA-256을 고정한다는 사실을 뒤늦게 확인했다.
  소급 교정을 취소하고 byte hash `e138f779...ff12`까지 복원했다. 전수 parser만 다섯 경계를
  안전 복구하며 `PARSE_REVIEW_REQUIRED`로 표시한다. hash 계약 확인을 patch보다 먼저 했어야 한다.
- sandbox 안 `git restore`는 `.git/index.lock` 접근 거부로 실패해, 허가된 범위의 정확한 단일
  경로 restore를 외부 권한으로 재실행했다. line-ending 변환 뒤 raw SHA가 달라진 단계도 있어
  대상 하나만 LF byte로 복원하고 Git blob·downstream SHA를 모두 확인했다.
- 첫 inventory parser의 blank-line 복구 규칙은 정상적인 닫는 `\\]` 앞 공백이 있는 Theory 31
  세 식까지 과잉복구했다. 다음 nonblank가 실제 종료기호인지 보는 look-ahead를 추가해 최종
  복구는 Theory 27의 5개만 남겼다. 한 번에 전체 JSON을 stdout으로 넘긴 시도도 출력 절단으로
  무효였으며 section/chunk 출력과 결정적 생성기로 교체했다.
- 임시 PowerShell helper 이름 `H`가 내장 `Get-History` alias와 충돌해 해시 점검 출력이 오염됐다.
  이를 `Get-TaskHash`로 바꾸고 실제 SHA를 다시 확인했다. 실패 출력은 provenance 증거로 쓰지 않았다.
- 최종 version 점검 한 번을 `lean/` 작업 디렉터리에서 실행하면서 Mathlib·Theory 27 경로 앞에
  불필요한 `lean/` 또는 빠진 `../`를 사용해 두 read-only 조회가 실패했다. 저장소 루트에서
  정확한 경로로 즉시 재실행해 Mathlib HEAD와 Theory 27 SHA를 확인했다. 첫 조회를 검증으로 세지 않는다.
- 전체 664 tests를 sandbox 안에서 먼저 실행해 `TemporaryDirectory` 접근 거부로 82 errors가
  발생했다. 이는 코드 회귀가 아니며, 사용자가 이미 허가한 정상 로컬 권한에서 같은 suite를
  재실행해 664/664 PASS를 확인했다. 앞으로 이 저장소의 전체 suite는 원장의 기존 규칙대로
  처음부터 허가된 정상 로컬 권한에서 실행한다.
- strict UTF-8 감사의 첫 PowerShell 명령에서 E080에 이미 기록한 `$file:` 보간 실수를 다시
  범해 parser 단계에서 중단했다. `${file}:${n}`으로 즉시 고쳐 재실행했다. 두 번째 실행은
  binary `__pycache__/*.pyc`까지 text로 읽어 3건을 잘못 보고했으며, 생성 source만 대상으로
  범위를 고쳐 22파일 issue 0을 확인했다. 첫 두 출력은 최종 검증 증거로 쓰지 않는다.
- 위 실패들은 actual prime 계산이나 `test_result`를 만들지 않았고, Lean PASS 수나 수학적
  결론을 늘리는 데 사용하지 않았다. 특히 전체 Sono/FMT 증명과 `X_cert`는 계속 OPEN이다.

### E083 — Theory 01 Lean scratch의 표현 정규화·실행 추적 실수

- 분류: `CORRECTED_BEFORE_CANONICAL_COMMIT / INVALID_RESULT_NONE`.
- 최초 scratch에서 `iterLog 4 x`를 완전히 펼친 항과
  `Real.log (iterLog 3 x)`를 혼용해 `ring`이 정규화하지 못했고, 마지막 strict-log
  부등식에도 같은 definitional-form mismatch가 남아 direct Lean이 2건을 거부했다.
  `change`로 표현을 하나로 고정하고 이미 얻은 `iterLog 4` 부등식을 직접 사용한
  후 scratch·정본 direct Lean·Lake build를 모두 다시 PASS했다. 가정을 느슨하게
  바꾸거나 proof escape를 쓰지 않았다.
- 첫 Mathlib 경로 조회에서 `elan`이 PATH에 있을 것으로 가정해 명령이 실패했다.
  고정된 `C:\\Users\\Uranus\\.elan\\bin\\lake.exe`와 repository-local Mathlib 경로로
  전환했다. 사용자의 Lean 설치 실패가 아니다.
- direct Lean을 처음 nested command로 호출했을 때 30초 yield 뒤 process는 계속 실행되었지만
  session id를 출력하지 않아 즉시 exit code를 회수하지 못했다. 프로세스를 끊지
  않고 자연 종료를 확인한 뒤, `Start-Process -Wait -PassThru`와 session polling으로
  direct Lean exit 0과 Lake build exit 0를 독립적으로 다시 회수했다.
- 첫 전체 unittest는 `-v`로 출력이 절단되어 마지막 집계를 화면에서 즉시 보지
  못했다. 같은 suite를 비상세 모드로 다시 실행해 664 tests, 92.365초, exit 0을
  확인했다. 절단된 verbose 출력만으로 PASS를 선언하지 않았다.
- 첫 staged allowlist 비교에서 Git의 기본 `core.quotePath` 이스케이프 출력을 실제
  경로와 비교해 한국어 파일 2개를 각각 unexpected/missing으로 잘못 계수했다.
  스테이징 자체를 변경하지 않고 `git -c core.quotepath=false diff --cached --name-only`로
  다시 비교해 staged 12개, allowlist delta 0을 확인했다. 첫 비교 출력은 오염
  증거나 예상 외 파일 stage로 해석하지 않는다.
- 위 오류는 actual prime 실험·데이터·`test_result`를 변경하지 않았고,
  Theory 01 정본은 `sorry`/`admit`/project-local `axiom` 0건으로 커널 검증됐다.

### E084 — Theory 55 smooth-remainder Lean 형식화의 정리 선택·정규화 시행착오

- 분류: `CORRECTED_BEFORE_COMMIT / INVALID_RESULT_NONE`.
- 첫 증명 초안에서 나눗셈 부등식의 목표 방향에 맞지 않는 `le_div_iff` rewrite와
  strict/non-strict `mul_lt_mul` 변형을 사용해 Lean이 거부했다. 양의 분모를 먼저 증명하고
  목표와 정확히 일치하는 `div_le_iff₀`, `lt_div_iff₀`, 양의 수 곱셈 정리로 교정했다.
- `log 200 < 6`을 보일 때 \(e^6\)의 finite-series 항을 4까지만 합해 61밖에 얻지 못하는
  불충분한 시도를 했다. 그 출력은 폐기하고 8항 합으로 \(e^6>200\)을 커널에서 증명했다.
  `Real.log_div_self_antitoneOn`의 domain 인수와 strict monotonicity 호출도 처음에는 잘못
  배치했으며, 실제 Mathlib 선언을 읽고 \(e\le200\le q\)를 명시해 고쳤다.
- 존재하지 않는 이름 `Real.one_lt_exp`를 한 차례 사용했고, `Real.exp_nat_mul`에 실수 3과
  자연수 3의 cast가 맞지 않는 초안도 있었다. 각각 고정 Mathlib의
  `Real.one_lt_exp_iff`/`Real.add_one_lt_exp`와 명시적 cast equality로 교정했다.
- improper integral을 처음 전개할 때 namespace가 다른 적분 정리, Gamma 값의 정규화,
  integrand 곱셈 순서를 잘못 맞춘 시도가 있었다. Mathlib의
  `integrableOn_exp_neg_Ioi`, `Real.GammaIntegral_convergent`,
  `integral_rpow_mul_exp_neg_rpow`를 source에서 확인하고 integrand equality를 별도로 증명했다.
- (55.30)의 실제 상수 \(2^{-3/4}<3/5\)를 초안에서는 추상 premise로 남겼으나, 원문과
  대조한 뒤 네제곱 비교와 양의 역수 반전을 사용한 독립 정리로 보강했다. 이제 남은 premise는
  prime/j-sum 비교이며 수치 상수 자체가 아니다.
- 모든 시행착오는 Lean compile 단계에서 발견됐고 채택된 theorem은 없었다. 최종 상태는
  direct Lean·원장 validator에서 통과했으며 executable source의 `axiom`/`sorry`/`admit`은
  0건이다. 소수 계산, dataset, `test_result`, \(X_{\rm cert}\) 판정에는 영향이 없다.
- 최종 묶음 검증 한 번은 작업 디렉터리가 이미 `lean/`인데 Python 생성기·검증기 경로 앞에
  `lean/`을 다시 붙여 두 명령이 `can't open file ... lean/lean/tools/...`로 실패했다.
  direct Lean과 `git diff --check`는 별개로 실행됐지만 실패한 두 Python 출력을 PASS로
  세지 않았다. 저장소 루트에서 정확한 같은 명령을 다시 실행해 generator `GENERATED`,
  validator `PASS`와 banned escape 0을 확인했다.

### E085 — Theory 55 잔여 적분 형식화의 API 탐색·원장 선언 인식 오류

- 분류: `CORRECTED_BEFORE_COMMIT / INVALID_RESULT_NONE`.
- Mathlib 초기 광범위 검색 출력이 잘려 `Chebyshev.theta`가 없는 것처럼 보였지만,
  `NumberTheory/Chebyshev.lean`을 집중 검색해 theta 정의·Abel summation·`theta_le_log4_mul_x`를
  확인했다. 다만 필요한 Rosser--Schoenfeld `1.01624` drop-in theorem은 없었다.
  광범위 검색의 부정확한 초기 인상을 source 판정에 쓰지 않았다.
- 임시 `Probe.lean`에서 적분·Gamma API를 탐색할 때 namespace를 잘못 추측한 초안과
  interval change-of-variable의 정규화가 맞지 않는 초안을 Lean이 거부했다. 고정 Mathlib
  source의 실제 정리명·형을 확인해 교정했고, 최종 단일 theory 파일은 direct Lean을
  경고 없이 통과했다. 임시 probe는 정본이 아니며 commit 전 제거한다.
- 검증 상태 JSON을 처음 재생성한 뒤 validator가 `@[simp] theorem` 선언을 자신의
  단순 선언 정규식으로 인식하지 못해 1회 실패했다. 해당 simp 속성은 증명에
  필요하지 않아 제거하고 direct Lean을 다시 통과한 후 validator도 declaration 87,
  banned escape 0으로 PASS했다. 첫 validator 실패를 최종 PASS로 세지 않는다.
- 전체 unittest를 알고 있던 sandbox `TemporaryDirectory` 제약 안에서 먼저 실행해
  664건 중 82건의 `PermissionError`를 다시 발생시켰다. 이 출력은 회귀 실패로
  사용하지 않고, 기존 허가 및 저장소 규약대로 정상 로컬 권한에서 같은 664건을
  74.349초에 모두 PASS했다.
- 실패한 sandbox test가 만든 workspace `tmp` 16개를 정리하는 첫 PowerShell에서
  `Remove-Item`의 non-terminating error를 종료코드에 반영하지 않고 `removed=16`이라는
  부정확한 요약을 출력했다. 이 요약을 성공 증거로 쓰지 않았다. 각 절대경로가
  저장소 `tmp` 하위임을 다시 검증하고 `$ErrorActionPreference='Stop'`, 삭제 후 존재
  재검사를 사용한 정상 로컬 권한 명령으로 16개 전부를 제거했다.
- 이 시행착오는 actual prime 계산·dataset·`test_result`를 변경하지 않았고,
  (55.27)의 source theorem을 가정 없이 증명했다고 선언하지 않았다. `X_cert`는 OPEN이다.

### E086 — DEP-R09 상태 원장 패치의 multi-file hunk 구문 오류

- 분류: `CORRECTED_BEFORE_COMMIT / PARTIAL_WRITE_NONE`.
- Theory 56의 자동 생성 무번호식 두 개를 상태 원장과 생성기 메모에 동시에 추가하려던
  첫 `apply_patch`에서 두 번째 파일 hunk의 문맥 표기를 잘못 작성했다. 패치 도구가
  적용 전에 `invalid hunk`로 전체 요청을 거부했으므로 부분 쓰기나 정본 오염은 없었다.
- 우회 도구나 `git apply`를 사용하지 않고, 두 파일을 각각 정상 `apply_patch`로 나눠
  교정했다. 이어 generator·validator를 다시 실행해 formula 1,015, 상태 누락 0,
  `NOT_YET_FORMALIZED` 960, banned proof escape 0을 확인했다.
- 예방: 여러 파일을 한 요청에서 고칠 때 각 `*** Update File` 뒤에 독립된 정상 hunk를
  두고, 구문 실패 시 파일별 patch로 축소한다. 실패한 패치 출력을 변경 증거로 세지 않는다.
- 후속 참고문헌 patch에서 JavaScript `String.raw` template 안의 Markdown backtick을
  escape하지 않아 도구 호출 전 `SyntaxError`가 한 번 발생했다. 파일 변경은 없었고,
  일반 문자열의 정상 `apply_patch`로 즉시 재실행했다. template literal을 쓸 때는 내부
  backtick 유무를 먼저 검사한다.

### E087 — hash-pinned Theory 48에 최신 상태를 덧붙인 정본 불변성 위반

- 분류: `DETECTED_BY_FULL_REGRESSION / REVERTED_BEFORE_COMMIT / RESULT_IMPACT_NONE`.
- DEP-R09 최신 상태를 동기화하면서 역사적 predecessor인 theory 48 끝에 새 문단을
  덧붙였다. 전체 unittest의 두 contract test가 `hash mismatch: DEP48`로 이를 정확히
  거부했다. downstream 고정 hash를 새 값으로 바꾸면 과거 증거를 소급 변경하게 되므로
  그렇게 하지 않았다.
- 추가 문단만 제거해 theory 48을 시작 blob과 동일하게 복원했고, 실패했던 표적 test
  2/2가 다시 PASS했다. 최신 상태는 successor theory 56, METHODS, AGENTS, 색인에만 둔다.
- 첫 제거 patch는 새 문단의 LaTeX backslash가 앞선 JavaScript 문자열 처리에서 빠진 것을
  예상하지 못해 문맥 불일치로 거부됐다. 실제 파일을 다시 읽은 뒤 현재 byte와 일치하는
  정상 `apply_patch`로 제거했고, 나머지 새 문서의 빠진 inline-math delimiter도 교정했다.
- 예방: predecessor hash가 있는 theory는 편집 전에 `rg`로 consumer contract를 찾고,
  새 상태는 successor 문서에만 기록한다. 전체 suite의 hash failure를 문서상 사소한
  불일치로 낮춰 보지 않는다.

### E088 — DEP-R09 phase 1이 인쇄 대수와 analytic 정당화를 충분히 분리하지 못함

- 분류: `DISCOVERED_BY_NEW_PRIMARY_SOURCES / PREVIOUS_RESULT_SCOPE_NARROWED / X_CERT_REMAINS_OPEN`.
- Theory 56 phase 1은 Sono에 인쇄된 `c_ZFR=1/24`, `a=1/80`, `D_PAP=160`,
  `aD=2`의 exact 대수를 올바르게 Lean 검증했다. 당시 Gallagher·Maier·McCurley 전문이
  없다고 명시하고 analytic rate를 OPEN으로 유지했으므로 PAP나 X_cert를 PASS로 선언한
  오류는 없었다.
- 그러나 전문을 확보해 대조하자 더 강한 문제가 드러났다. Sono Proposition 5.3의
  `c_ZFR/log(Q(1+|t|))`에서 modulus와 높이를 T 이하로 두면 보수적으로
  `c1=c_ZFR/3`이 나오며, p.536의 `c1=3c_ZFR`는 반대 방향이다. McCurley 원문을 직접
  조합해도 안전하게 복원되는 baseline은 `c1=1/24`이지 `1/8`이 아니다.
- Gallagher Theorem 7은 숨은 multiplier를 가진 `≪`이고 Maier Lemma 2도 exact multiplier나
  cutoff 없이 `D`를 크게 선택한다. phase 1은 multiplier OPEN을 기록했지만, 기존 상위 문서의
  “2e-17은 증명된 계수” 표현이 이 더 구체적인 normalization gap과 충돌하는 것을 당시
  발견하지 못했다.
- 교정: Theory 56은 인쇄 대수의 역사적 predecessor로 보존하고, Theory 57·review 64에서
  source-compatible direction, hidden multiplier, finite range와 coefficient 민감도를
  successor 정본으로 분리했다. AGENTS, METHODS, theory/review 색인과 Lean 원장을 갱신해
  `PAP-11`, DEP-R09, fixed `2e-17`, X_cert를 fail-closed 상태로 유지한다.
- 예방: 외부 정리의 상수를 재사용할 때는 (a) 정리 statement, (b) 변수 재매개화,
  (c) inequality direction, (d) Vinogradov/O multiplier, (e) finite range를 각각 별도 행으로
  감사한다. exact 숫자 대입이 커널을 통과해도 upstream analytic bridge PASS로 승격하지 않는다.

### E089 — DEP-R09 source audit 중 검색 정규식·multi-file patch 문맥 실패

- 분류: `TOOLING_ERROR / PARTIAL_WRITE_NONE / CORRECTED_IMMEDIATELY`.
- Sono text excerpt를 한 번에 찾으려다 PowerShell `Select-String`의 regex pattern에 괄호가
  닫히지 않은 `exp(`를 넣어 그 검색 한 건이 실패했다. 다른 source 출력은 나왔지만 이를
  Sono 확인 증거로 세지 않았고, page별 native text와 이미 렌더링한 source page를 다시
  직접 읽었다.
- AGENTS·METHODS·Theory12·Lean README를 한 patch에서 바꾸려던 첫 시도는 Theory12의 실제
  제목이 예상 문자열과 달라 apply_patch가 전체 patch를 거부했다. 부분 쓰기는 없었으며,
  실제 첫 줄을 읽은 뒤 파일별 정상 patch로 나눴다. `git apply` 우회는 사용하지 않았다.
- 예방: regex에 literal 괄호가 들어가면 `-SimpleMatch` 또는 escape를 사용한다. 여러 파일
  patch는 각 파일의 현재 anchor를 먼저 읽고, 하나의 mismatch가 전체 작업을 막지 않도록
  독립 patch로 축소한다.

### E090 — Theory 12 successor 경고가 고정된 첫 H2 위치를 일시 변경

- 분류: `DETECTED_BY_FULL_REGRESSION / CORRECTED_BEFORE_COMMIT / RESULT_IMPACT_NONE`.
- 최신 DEP-R09 경고를 Theory 12의 문서 제목 바로 아래에 넣었더니, 기존 contract test가
  요구하는 첫 H2 `2026-09-10 H1b-COV2 현재 상태`보다 경고 blockquote가 먼저 나타났다.
  수식·상태·hash를 바꾼 오류는 아니지만, 정본 소비자가 의존하는 문서 구조를 깨뜨렸다.
- 경고 내용은 그대로 보존하면서 첫 H2 바로 아래로 이동했다. 표적 회귀시험 1/1과
  sandbox 외부 전체 회귀시험 669/669가 통과했다.
- 같은 첫 전체 시험에서 발생한 82개 `PermissionError`는 sandbox가 저장소·시스템
  임시폴더를 차단해 생긴 환경 오류였다. 코드 실패로 세지 않고, 기존 사용자 허가 범위의
  정상 로컬 권한에서 전체 suite를 다시 실행해 669/669 PASS를 확인했다.
- 예방: 정본 문서의 머리말·첫 H2도 기계 contract일 수 있으므로, successor 경고는 기존
  구조를 보존하는 위치에 넣고 전체 회귀로 확인한다.

### E091 — 최종 UTF-8 감사용 PowerShell 문자열의 변수 경계 오류

- 분류: `TOOLING_ERROR / READ_ONLY_COMMAND_FAILED / CORRECTED_IMMEDIATELY`.
- control character 진단 문자열을 `"CONTROL:$rel:$code"`로 만들면서 변수명 뒤의 콜론을
  `${}`로 구분하지 않아 PowerShell parser가 명령 전체를 실행 전에 거부했다. 읽기 전용
  검사였으므로 파일 변경이나 검증 오판은 없었다.
- 문자열 format operator를 쓰는 `('CONTROL:{0}:{1}' -f $rel,$code)`로 교정해 다시 실행했고,
  변경·신규 19파일의 strict UTF-8/control scan과 표적 local path 7건이 PASS했다.
- 예방: PowerShell 보간 문자열에서 변수 바로 뒤에 콜론이 오면 `${name}` 또는 `-f`를 쓴다.

### E092 — 작업원장 중간 갱신에 미래 시각을 잘못 기록

- 분류: `PROVENANCE_TIMESTAMP_ERROR / CORRECTED_BEFORE_COMMIT / RESULT_IMPACT_NONE`.
- 작업원장 두 단계 제목에 당시 시스템 시각보다 뒤인 `03:20`, `03:55 KST`를 정확한
  측정 없이 적었다. 수식·검증 결과와 무관하지만 재개 이력의 시간 신뢰성을 해친다.
- `Get-Date`의 실제 관측값이 2026-09-11 03:18 KST임을 확인한 뒤, 정확한 분을 재구성할
  근거가 없는 두 제목은 `2026-09-11 KST`로 낮춰 기록했다. 확인 가능한 착수 시각과 이후
  handoff 시각은 도구 출력만 사용한다.
- 예방: 원장·handoff의 시각은 작성 직전 시스템 명령으로 읽고, 사후 추정한 분 단위 시각은
  기록하지 않는다.

### E093 — sandbox 내부 첫 Git staging의 index.lock 권한 거부

- 분류: `SANDBOX_PERMISSION_ERROR / RETRIED_WITH_EXISTING_AUTHORIZATION / PARTIAL_STAGE_NONE`.
- 정상 `apply_patch` 편집은 모두 성공했지만, 첫 `git add`가 현재 sandbox의 read-only
  `.git` 정책 때문에 `Unable to create .git/index.lock: Permission denied`로 실패했다.
- 우회 patch나 `git apply`는 사용하지 않았다. 사용자가 이미 승인한 로컬 staging·commit
  범위에서, 같은 20개 exact allowlist를 sandbox 외부 Git 권한으로 다시 실행해 성공했다.
- 예방: 현재 permission profile에서 `.git`이 read-only이면 내용 편집 오류와 Git metadata
  권한 오류를 구분하고, staging은 승인된 exact allowlist로만 권한 상승한다.

### E094 — 한글 경로 quoting을 고려하지 않은 첫 staged allowlist 비교

- 분류: `VERIFICATION_COMMAND_ERROR / CORRECTED_BEFORE_COMMIT / STAGED_SCOPE_UNCHANGED`.
- 첫 allowlist 비교에서 Git 기본 `core.quotePath` 출력의 한글 경로가 octal escape와
  따옴표로 표시되는 것을 고려하지 않아, 실제 같은 4개 경로를 다르다고 판정했다.
- `git -c core.quotePath=false diff --cached --name-only`로 다시 비교해 exact allowlist
  20개가 일치하고 unstaged·untracked 경로가 0임을 확인했다. 같은 검사에서 review 64의
  EOF 빈 줄 1개도 `git diff --cached --check`가 발견해 정상 `apply_patch`로 제거했다.
- 예방: 사람이 읽는 UTF-8 경로 비교에는 `core.quotePath=false`를 명시하고,
  allowlist 일치 뒤에도 `git diff --cached --check`를 독립 gate로 실행한다.

### E095 — DEP-R09 coefficient 진단에서 float가 먼저 만들어진 고정밀 문자열 오류

- 분류: `DETECTED_BY_NEW_UNIT_TEST / CORRECTED_BEFORE_HANDOFF / GATE_UNCHANGED`.
- 첫 진단 one-liner에서 target을 `mp.mpf(2) * 10**-17`로 썼다. Python이
  `10**-17`을 먼저 binary float로 만든 뒤 `mpmath`로 올렸으므로, 최소
  `C_PAP`와 error slack의 긴 고정밀 문자열 마지막 자릿수들이 정확하지 않았다.
- 새 fail-closed test는 target을 `mp.mpf(2) * mp.mpf(10) ** -17`로 다시 계산해 이
  불일치를 2건 발견했다. 원장·Theory 58·review 65를 exact decimal target으로 교정하고
  표적 test 7/7을 다시 PASS했다.
- `D=186` PASS, `D=187` FAIL이라는 정수 경계와 연구 판정은 바뀌지 않았다.
  잘못된 문자열을 검증 통과 또는 theorem 수치로 사용하지 않았다.
- 같은 source 수집 과정에서 `tmp` 전체를 광범위하게 열거한 읽기 명령이 다른 작업의
  제한된 임시경로에서 다수 `Access denied`를 출력했다. 필요한 파일은 이미 알려진 exact
  하위경로에서 다시 확인했고, 권한 오류가 난 경로의 부재나 내용에 관한 판정은 하지 않았다.
- 예방: 모든 작은 목표값도 문자열에서 직접 `mp.mpf`로 만들고, 문서에 복사하기 전에
  독립 재계산 test를 먼저 실행한다. `tmp` 검색은 정확한 작업 하위경로로 제한한다.

### E096 — 마감 검증에서 Lean 상대경로 중복과 sandbox 전체시험 오판 위험

- 분류: `VERIFICATION_COMMAND_ERROR / SANDBOX_PERMISSION_ERROR / RESULT_IMPACT_NONE`.
- `lean/`을 작업 디렉터리로 둔 첫 검증 명령에서 다시 `lean/tools/...`를 지정해
  `lean/lean/tools/...`를 찾으려 했다. 첫 Python 호출이 즉시 실패했으므로 generator,
  test, Lean build 어느 것도 그 명령에서 실행되지 않았다. 저장소 루트의 generator·validator와
  `lean/`의 `lake build`를 분리해 다시 실행했고 각각 PASS했다.
- 이어 sandbox 안에서 전체 unittest를 실행했을 때 676건 중 82건이 `PermissionError`로
  끝났다. traceback은 저장소 `tmp/`와 시스템 임시 폴더를 만든 뒤 하위 파일 쓰기·정리를
  ACL이 거부한 동일 환경 원인이었다. 이를 코드 회귀로 판정하지 않고, 사용자가 승인한
  sandbox 외부 FGKMT Python에서 같은 suite를 재실행해 676/676 PASS(87.676초)를 확인했다.
- 예방: 루트 상대경로 도구와 하위 작업 디렉터리 도구를 한 명령에서 혼합하지 않는다.
  `TemporaryDirectory`를 광범위하게 쓰는 전체 suite는 기존 규약대로 처음부터 승인된 정상
  로컬 권한에서 실행하고, sandbox 실패 출력은 PASS/FAIL 증거로 사용하지 않는다.

### E097 — 이미 기록한 PowerShell 콜론 보간 오류를 최종 감사에서 반복

- 분류: `REPEATED_VERIFICATION_COMMAND_ERROR / PARSE_TIME_FAILURE / FILE_IMPACT_NONE`.
- 최종 UTF-8 감사 문자열에 `"UTF8:$f:$message"` 형태를 다시 사용해, 변수 `$f` 바로 뒤의
  콜론을 PowerShell이 변수명 일부로 해석했다. E091에서 이미 같은 함정을 기록했는데도
  예방 규칙을 적용하지 못했다. 명령은 parser 단계에서 전체 거부돼 파일 읽기·변경이나
  부분 검증 결과는 없었다.
- 모든 진단 문자열을 `('UTF8:{0}:{1}' -f $f,$message)` 형식으로 바꿔 재실행했다.
  변경·신규 16파일 strict UTF-8/control·수식 delimiter와 local link 1,249건,
  JSON 3파일, Python 2파일 compile, 금지된 네 글자 프로젝트명 오탈자 검사를 issue 0으로 통과했다.
- 예방: PowerShell 진단 문자열은 변수 보간을 사용하지 않고 `-f`만 사용한다. 이미 원장에
  있는 예방 규칙은 최종 명령 작성 전에 체크리스트로 먼저 확인한다.

### E098 — JavaScript patch 문자열이 핸드오프의 LaTeX 백슬래시를 소거

- 분류: `DOCUMENT_FORMATTING_ERROR / DETECTED_ON_NEXT_TURN / MATHEMATICAL_STATE_UNCHANGED`.
- `apply_patch` 입력을 일반 JavaScript 문자열로 만들면서 `\(`와 `\)`의 백슬래시가
  문자열 해석 단계에서 사라졌다. 그 결과 최신 handoff의 \(X_{\rm cert}\) 세 곳이
  `(X_{\rm cert})`로 저장됐다. 당시 delimiter 검사는 여는/닫는 표식 개수만 비교해
  둘 다 0인 상태를 잘못 PASS로 보았다.
- 다음 작업 착수 전 원문 재독에서 발견해 이중 escape를 명시한 patch로 세 곳을 교정했다.
  같은 검색에서 METHODS의 오래된 H1a 문단에 남아 있던 \(r\), \(J_r/I_r\),
  \(X_{\rm cert}\) 표기 6곳도 수학 내용 변경 없이 함께 복구했다.
- 첫 두 교정 시도는 `String.raw` template 안의 Markdown backtick 때문에 JavaScript parser가
  실행 전에 거부했다. 세 번째 시도는 백슬래시를 두 개 넣어 여전히 잘못됐고, 실제 파일을
  다시 읽은 뒤 placeholder를 단일 백슬래시로 치환하는 patch로 최종 교정했다.
- post-close 작업원장에 이 교정을 설명하는 문장을 추가할 때도 같은 이중 백슬래시가 한 번
  반복됐다. 즉시 실제 파일을 읽어 확인하고 같은 placeholder 방식으로 단일 표기로 고쳤다.
- 예방: LaTeX가 포함된 patch는 실제 도구 입력에 백슬래시가 남는지 작은 patch로 먼저
  확인한다. 단순 delimiter parity 외에 핵심 수식의 기대 literal이 실제로 존재하는지와
  `(X_{`, `(r\`, `(J_` 같은 탈락 흔적을 별도 검색한다.

### E099 — `rg -q`의 무출력을 실패로 해석한 기대 literal 검사 오류

- 분류: `VERIFICATION_LOGIC_ERROR / FALSE_NEGATIVE / FILE_IMPACT_NONE`.
- 기대 literal 검사에서 `if (-not (rg -q ...))`를 사용했다. `rg -q`는 일치해도 stdout을
  출력하지 않으므로 PowerShell 표현식 값은 비어 있었고, 실제 literal이 존재하는데도
  `MISSING_EXPECTED_XCERT_LITERAL`로 오판했다.
- `$LASTEXITCODE`를 직접 저장해 다시 검사한 결과 기대 literal은 exit 0, 금지된 중복
  백슬래시는 exit 1이었다. 표적시험 12/12와 Lean validator도 독립 PASS했다.
- 예방: `rg -q`·native validator는 출력 문자열의 truthiness가 아니라 종료코드로 판정한다.

### E100 — Branch S 탐색 명령에서 이미 알려진 두 오류 패턴 반복

- 분류: `REPEATED_EXPLORATORY_COMMAND_ERROR / CORRECTED_BEFORE_ARTIFACT / RESULT_IMPACT_NONE`.
- 첫 transfer-gate one-liner에서 E095와 같은 `mp.mpf(2) * 10**-17`을 다시 써 binary float가
  먼저 생성됐다. 출력 직후 기존 Theory 58 exact decimal과 불일치를 발견하고 target을
  `mp.mpf(2) * mp.mpf(10) ** -17`로 바꿔 재계산했다. 첫 출력은 문서·JSON에 사용하지 않았고,
  새 unittest가 모든 저장 수치를 exact-decimal target에서 다시 만든다.
- Jutila OCR 검색에서 Windows 경로에 shell wildcard를 직접 넣어 E095 당시와 같은 OS error
  123을 냈다. exact directory와 `rg -g` 방식의 성공 결과만 source 판정에 사용했다.
- 예방: 수치 one-liner도 E095 체크리스트를 그대로 적용하고, Windows `rg` file selection은
  경로 wildcard가 아니라 `-g` 또는 PowerShell이 만든 명시적 파일 목록을 쓴다.

### E101 — 상태 문서 줄 범위 출력용 PowerShell 괄호 누락

- 분류: `READ_ONLY_COMMAND_PARSE_ERROR / IMMEDIATE_CORRECTION / FILE_IMPACT_NONE`.
- 두 문서의 line-number preview를 한 명령으로 만들며 두 번째 `-f ($i,$a[$i])`의 닫는 괄호를
  빠뜨렸다. PowerShell parser가 명령 전체를 실행 전에 거부해 파일 읽기·변경은 없었다.
- 괄호를 고친 동일한 read-only 명령으로 필요한 범위를 다시 읽었다.
- 예방: 복수 loop를 한 줄에 합치지 않고, 짧은 read command도 parser 성공 여부를 먼저 확인한다.

### E102 — Theory 59 수식 patch에서 LaTeX backslash 1자 누락

- 분류: `DOCUMENT_FORMATTING_ERROR / DETECTED_BEFORE_COMMIT / MATHEMATICAL_VALUE_UNCHANGED`.
- 식 (59.2)의 `\ldots,\qquad`를 JavaScript 일반 문자열 patch에 넣을 때 `qquad` 앞
  backslash 하나를 누락했다. inventory preview가 `ldots,qquad`로 보인 것을 확인해
  source line을 읽고 정상 `apply_patch`의 raw 문자열로 교정했다.
- 수치 문자열과 부등호는 변하지 않았고 첫 상태는 commit하지 않았다. 교정 뒤 inventory를
  다시 생성·검증한다.
- 예방: 새 theory의 모든 display는 생성된 inventory preview와 source `repr`을 함께 대조하고,
  LaTeX patch는 일반 JavaScript 문자열보다 raw patch 문자열을 우선한다.

### E103 — 작업원장 단계 완료시각을 현재보다 미래로 기록

- 분류: `PROVENANCE_TIMESTAMP_ERROR / DETECTED_BEFORE_HANDOFF / RESULT_IMPACT_NONE`.
- 실제 `Get-Date`가 2026-09-13 10:04 KST인데 단계 2--5에 10:20--12:05를 임시로 적었다.
  연구 수치와 검증에는 영향이 없지만 작업 순서 provenance가 거짓이 될 수 있어 즉시
  `10:04 KST 확인 시점까지 완료`라는 관측 범위 표기로 교정했다.
- 예방: 작업원장의 각 시각은 추정해 쓰지 않고 해당 단계 마감 시 `Get-Date` 관측값 이하인지
  확인한다. 정확한 분 단위 관측이 없으면 `시각 미기록`으로 남기는 편이 낫다.

### E104 — 전체 회귀시험이 직전 완료기록의 금지 프로젝트명 오탈자를 발견

- 분류: `STALE_VOCABULARY_ERROR / DETECTED_BY_FULL_SUITE / SCIENTIFIC_RESULT_IMPACT_NONE`.
- Branch S 전체 683시험 중 vocabulary gate 하나가 오류 원장과 직전 완료 작업원장에 남은
  네 글자 프로젝트명 오탈자 두 건을 발견했다. 둘 다 “금지 표기 검사를 통과했다”는 역사적
  검증 설명 안의 문자열이었고 수학·코드에는 영향이 없었다.
- literal을 되풀이하지 않는 `금지된 네 글자 프로젝트명 오탈자` 표현으로 두 문서를 교정한다.
  이후 vocabulary 표적시험과 전체 suite를 다시 실행한다.
- 예방: 금지 문자열 검사 결과를 설명할 때도 그 금지 문자열 자체를 다시 쓰지 않는다.

### E105 — Branch S 최종 정적 감사 명령을 세 차례 잘못 설계

- 분류: `VERIFICATION_COMMAND_DESIGN_ERROR / FALSE_POSITIVE_AND_API_MISUSE / FILE_IMPACT_NONE`.
- 첫 시도는 저장소 루트에서 validator를 import하면서 sibling module 경로를 추가하지 않아
  `ModuleNotFoundError`로 중단됐다. 두 번째 시도는 허용 제어문자를 문자열
  `"\\t\\r\\n"`의 문자 집합과 비교해 정상 LF를 모두 문제로 오인했다. 세 번째 시도는
  오래된 prose와 생성 원장 전체의 LaTeX 표식을 단순 개수로 세어 문맥상 정상인 내용을
  false positive로 보고했다. 어느 시도도 파일을 변경하지 않았다.
- `lean/tools`를 import path에 명시하고, 허용 문자는 ordinal `(9, 10, 13)`으로 비교하며,
  수식 delimiter 검사는 이번에 새로 작성한 문서에만 한정하도록 교정했다. 이 과정에서
  `validate_local_markdown_links`에 존재하지 않는 두 번째 인자를 한 번 더 전달해
  `TypeError`가 났고, 함수 정의를 직접 확인한 뒤 단일 path 목록 인자로 수정했다.
- 최종 교정 명령은 변경 Markdown 12개 strict UTF-8·제어문자 issue 0, local link
  1,268개, 신규 문서 수식 delimiter issue 0, JSON 3개 parse와 `git diff --check`를
  통과했다. CRLF 변환 안내는 Git 설정 경고이며 diff 오류가 아니다.
- 예방: validator를 재사용할 때 먼저 함수 signature를 읽고, broad heuristic 검사는
  generated/prose 문서에 적용하지 않는다. 검증 명령의 실패도 연구 산출물 실패와 분리해 기록한다.

### E106 — 전체 unittest를 sandbox 안에서 재실행해 권한 오류 82건 유발

- 분류: `KNOWN_ENVIRONMENT_MISUSE / SANDBOX_PERMISSION_FAILURE / CODE_IMPACT_NONE`.
- 이 저장소의 전체 suite는 `TemporaryDirectory`와 multiprocessing 때문에 정상 로컬 권한에서
  실행해야 한다는 기존 원장 규칙이 있는데도, session-close 재검증을 sandbox 안에서 먼저
  실행했다. 683개 중 82개가 같은 계열의 `PermissionError`로 실패했고 연쇄 명령의 Lean build는
  실행 전 중단됐다. 이는 test assertion 실패나 연구 코드 회귀가 아니다.
- 사용자의 기존 허가 범위에 따라 동일 전체 suite를 정상 로컬 권한으로 재실행해
  683/683 PASS(64.077초)를 확인했다. 이어 Lean build를 별도로 실행해 8,765 jobs PASS를
  다시 확인했다. sandbox 실패 run은 성공 증거로 사용하지 않는다.
- 예방: 전체 suite 실행 전 오류 원장 E007·작업규약의 실행 권한 항목을 확인하고 첫 시도부터
  정상 로컬 권한을 사용한다. sandbox 결과와 로컬 결과를 문서에서 서로 바꾸어 쓰지 않는다.

### E107 — Jutila source 감사 중 탐색·patch·Lean 식별자 오류

- 분류: `EXPLORATORY_COMMAND_AND_DRAFT_ERROR / DETECTED_BEFORE_COMMIT / SCIENTIFIC_IMPACT_NONE`.
- Windows `rg`에 경로 wildcard를 직접 넣어 OS error 123을 한 번 반복했고, 이후 `-g` 필터로
  교정했다. PowerShell 환경에서 지원되지 않는 `Get-Content -Encoding Byte`도 사용했다가
  `Format-Hex`와 hash 검사로 대체했다.
- Graham PDF의 URL을 추측한 요청은 404였고, 공식 DeepBlue metadata를 직접 확인한 뒤 HTML
  challenge를 PDF로 취급하지 않았다. Huxley는 출판사 HTML에서 실제 CC-BY endpoint를 찾아
  `%PDF` header·byte 수·SHA-256을 모두 확인했다.
- 해시 출력용 `foreach` 결과를 괄호 없이 곧바로 pipe에 연결해 PowerShell parser가 명령을
  실행 전에 거부했다. 배열 변수에 먼저 담는 형태로 재실행했다. 여러 정본을 묶은 첫
  `apply_patch`도 AGENTS.md 긴 한 줄의 문맥 불일치로 전체 중단됐으며, 부분 적용이 없음을
  확인하고 파일별 좁은 patch로 교정했다.
- Lean 보조정리에서 그리스 문자 lambda를 변수명으로 써 parser token과 충돌했다. `lam`으로
  바꾼 뒤 단일 파일 검증이 exit 0으로 통과했다. 이 실패 상태는 inventory나 commit에
  반영하지 않았다.
- 새 review를 JavaScript 일반 문자열 patch로 만들면서 LaTeX의 backslash가 tab·form-feed
  escape로 해석돼 `tau`, `frac` 표기가 손상됐다. strict UTF-8/control-character 검사가
  form-feed를 발견했고, 문서 전체를 정상 `apply_patch` 입력으로 재작성해 control issue 0과
  local link 1,274개를 다시 확인했다. 손상본은 commit하지 않았다.
- 예방: Windows 검색은 `-g`, byte 확인은 `Format-Hex`·hash를 사용한다. 공식 download URL은
  추측하지 않고 publisher HTML에서 추출한다. PowerShell 반복 결과는 변수에 담은 뒤 pipe하며,
  긴 한 줄 정본은 동적 exact-line patch 또는 작은 patch로 나눈다. LaTeX가 있는 patch는
  raw-safe 입력 또는 backslash 이중화를 사용하고 control-character 검사를 바로 실행한다.
  Lean 식별자에는 예약 문법 기호를 쓰지 않고 단일 파일을 먼저 컴파일한 뒤 전수 원장을 생성한다.

### E108 — JL5 source 감사 중 검색 범위·PDF 해석·hash·patch 입력 오류

- 분류:
  `SOURCE_AUDIT_AND_TOOLING_DRAFT_ERRORS / ALL_CORRECTED_BEFORE_COMMIT /
  SCIENTIFIC_RESULT_IMPACT_NONE`.
- Jutila OCR 파일을 찾으면서 `tmp` 전체에 광범위한 `rg`를 실행해, 과거 임시 시험
  디렉터리에서 access-denied 메시지를 다수 발생시켰다. 읽기 전용 검색 실패였고 파일·실험
  프로세스에는 영향이 없었다. 이후 검색을 해당 PDF 감사 폴더와 정본 경로로 제한했다.
- Zuniga Alterman Theorem 4.6의 \(q\)-factor를 OCR text만 보고 잠시 1로 해석했다.
  원페이지 렌더링에서 numerator \(1-|f(p)-p^{-\alpha}|p^\alpha\)를 확인해
  실제 \(\alpha=1,f(p)=1/p\) 특수화가
  \(\prod_{p\mid q}\sqrt p/(\sqrt p-1)\)임을 바로잡았다. 이 일반 theorem은 primary
  JL5 cutoff에 사용하지 않았고 잘못 읽은 값은 문서·코드·결과에 남기지 않았다.
- Ford PDF의 SHA-256을 실제 계산하기 전에 검증되지 않은 임시 문자열로 machine JSON
  draft에 한 번 넣었다. 곧바로 `Get-FileHash`로 실제
  `a6e8462f1e76606614e5c2891b419515be408d5f11f0b82915f5c24e05c00e06`을
  확인해 교정한 뒤 표적시험을 실행했다. page count도 기억에 의존해 134로 넣었다가
  `pdfinfo`의 129 pages로 교정했다. provenance를 먼저 측정하지 않은 순서 오류다.
- review 문서를 만드는 첫 `apply_patch` wrapper에서 Markdown triple-backtick을
  JavaScript template literal 안에 그대로 넣어 parser가 도구 호출 전에 거부했다.
  파일은 생성되지 않았다. 이후 placeholder 치환 방식으로 재실행했다. METHODS patch에서도
  같은 입력 오류를 한 번 반복했으며 역시 파일 적용 전 거부됐다.
- Lean 하위경로에서 검색할 때 이미 `lean`을 workdir로 둔 상태에서 `lean/...`을 다시
  붙여 한 경로 오류를 냈다. 필요한 Mathlib example은 올바른 상대경로로 다시 읽었다.
- 변경 파일만이 아니라 저장소의 모든 Markdown을 대상으로 한 추가 제어문자 감사에서
  과거 이력 문서 `handoff/202609021757_HANDOFF.md`의 byte offset 4,493에 vertical tab
  (`U+000B`, ordinal 11) 1개가 발견됐다. 이번 작업이 만든 오류가 아니며 현재 수학 결과에도
  영향이 없다. 기존 핸드오프는 이력 보존 문서이므로 조용히 수정하지 않고 레거시 정리
  후보로만 기록했다. 이번 변경·신규 Markdown 12개는 strict UTF-8·제어문자 issue 0이다.
- 마지막 동기화에서 세 파일을 한 `apply_patch` 입력으로 묶는 과정에 hunk 종료 형식을
  잘못 써 도구가 적용 전에 거부했다. 부분 적용이 없음을 확인하고 파일별 정상 patch로
  나눠 반영했다. 기존 sandbox 오류나 `git apply` 우회는 사용하지 않았다.
- 예방:
  1. PDF 수식은 native/OCR text 해석 뒤 반드시 렌더링 원페이지를 본다.
  2. provenance hash·bytes는 JSON에 쓰기 전에 먼저 측정한다.
  3. JavaScript를 감싸는 patch의 Markdown fence와 inline backtick은 placeholder로 바꾼다.
  4. 검색 전에 현재 workdir와 target 상대경로를 함께 확인한다.

### E109 — JL6a 초안 Lean·검증 명령의 국소 오류

- 분류:
  `LEAN_DRAFT_AND_COMMAND_WORKDIR_ERROR / DETECTED_BEFORE_COMMIT /
  SCIENTIFIC_RESULT_IMPACT_NONE`.
- 첫 Lean compile에서 `hT.zero_le`라는 존재하지 않는 field projection을 사용했고,
  `field_simp`가 이미 목표를 닫은 뒤 불필요한 `ring`을 실행했으며, delta 정의를 충분히
  전개하지 않아 식 하나가 남았다. 각각 명시적 `0<=T` 증명, 중복 tactic 제거,
  `rw [jutilaJL6ShiftDelta]` 뒤 분모 제거로 교정했다. 교정 후 단일 Lean 파일은 exit 0이다.
- 이어 inventory 생성·검증과 Lean compile을 한 root 명령에 묶으며 `lake`만 저장소 루트에서
  실행해 경로 오류를 냈다. inventory 생성과 validator는 독립적으로 PASS했지만 그 출력으로
  Lean 성공을 주장하지 않고, `lean/`을 workdir로 지정해 Lean을 별도 재실행한다.
- 작업 시작 파일 탐색에서도 직전 파일명을 기억으로 추측해 존재하지 않는 JL5 경로를 한 번
  읽으려 했다. `rg --files`로 실제 canonical 파일명을 찾은 뒤 진행했으며 파일 영향은 없다.
- 예방: compile·inventory·validator는 각 도구의 canonical workdir를 명시한 별도 단계로
  실행하고, 인접 단계 파일명도 먼저 `rg --files`로 확인한다.

### E110 — JL6a 최종 control-character 검사 명령의 PowerShell 변수 구문 재발

- 분류:
  `VALIDATION_COMMAND_PARSE_ERROR / DETECTED_BEFORE_SCAN / SCIENTIFIC_RESULT_IMPACT_NONE`.
- 변경 파일의 strict UTF-8·ASCII control-character 검사를 한 번에 실행하는 PowerShell
  진단 문자열에서 `"CONTROL:$rel:..."`을 사용했다. PowerShell은 변수명 바로 뒤의
  콜론을 scope 구문처럼 해석하므로 명령 전체를 실행 전에 parser error로 거부했다.
- 이는 과거 원장에도 기록된 도구 사용 함정인데 재발한 절차상 실수다. `${rel}`로 경계를
  명시해 즉시 재실행했고, 변경·신규 텍스트 21개에서 strict UTF-8·금지 control character
  문제 0건, 변경 Markdown local link 1,345개 PASS를 확인했다. 연구 코드·문서·검증값은
  첫 실패 명령에 의해 변경되지 않았다.
- 예방: PowerShell interpolated string에서 변수 뒤에 `:`가 오면 항상 `${name}:` 형식을
  사용한다. 가능하면 이 반복 검사를 독립된 검증 스크립트로 고정해 ad-hoc 문자열 생성을
  줄인다.

### E111 — JL6b source 검색 범위·보조 PDF 다운로드 후속검사 오류

- 분류:
  `SOURCE_SEARCH_AND_DOWNLOAD_CONTROL_FLOW_ERROR / DETECTED_DURING_AUDIT /
  SCIENTIFIC_RESULT_IMPACT_NONE`.
- 작업 시작 시 이미 E108에서 경고한 `rg --files tmp`의 광범위 검색을 다시 실행해 과거
  접근 제한 임시 디렉터리의 access-denied 메시지를 다수 발생시켰다. 읽기 전용 검색
  실패였고 파일·실행 중 프로세스·연구 판정에는 영향이 없었다. 이후 Jutila audit copy의
  명시 경로로 제한했다.
- S. Graham 1981 PDF를 공식 endpoint에서 보조 source로 확보하려 한 첫 명령은 Anubis
  JavaScript challenge로 실패했는데도, 같은 명령 흐름이 존재하지 않는 출력 파일의 byte와
  hash를 계속 검사해 연쇄 오류를 만들었다. `.part`를 쓰도록 고친 두 번째 시도도 redirect
  뒤 challenge로 다운로드가 실패했지만 생성되지 않은 `.part` 검사·정리를 계속 시도했다.
  실제 PDF나 `.part` 파일은 생성되지 않았고 삭제된 파일도 없다.
- Graham의 공식 metadata와 검색 가능한 statement만으로도 이 논문이 다른 truncated-Perron
  detector를 사용해 Jutila 1977 식 (2.11) tail의 drop-in source가 아님을 판정할 수 있었다.
  PDF를 읽었다고 기록하지 않았으며, 이번 primary geometric-tail proof에 이 source를
  사용하지 않았다.
- Theory 63 초안 식 (63.9)에는 patch 문자열 작성 중 `\\le`의 backslash가 빠진 `le`가
  한 번 들어갔다. inventory preview에서 즉시 발견해 `\\le`로 교정하고 원장 전체를 다시
  생성했다. 잘못된 초안은 최종 판정에 쓰지 않았다.
- 마감 때 UTF-8·link·JSON·compile·diff 검사를 한 PowerShell one-liner에 과도하게 합친
  첫 명령이 진단 출력 없이 exit 1을 반환했다. 성공으로 취급하지 않고 검사를 UTF-8/control,
  local link, Python/JSON/diff의 세 명령으로 분리했다. 분리한 최종 검사는 변경 텍스트
  23파일, Markdown 16파일·local link 1,377개, JSON 3개에서 issue 0으로 PASS했다.
- 예방:
  1. 대용량 `tmp` 전체가 아니라 정본·audit-copy 명시 경로만 검색한다.
  2. 다운로드는 `.part`에 수행하고 `Invoke-WebRequest -ErrorAction Stop` 실패 시 같은
     command block을 즉시 끝낸다.
  3. 존재 여부와 PDF magic bytes가 확인된 뒤에만 hash·rename·cleanup을 실행한다.
  4. 공식 endpoint가 challenge를 요구하고 source가 비필수이면 반복 우회하지 않고
     `PDF_NOT_INSPECTED`로 남긴다.
  5. 새 tagged formula는 inventory preview에서 LaTeX 제어문자 보존을 확인한다.
  6. 서로 다른 validator를 긴 one-liner 하나로 합치지 말고 실패 지점을 식별할 수 있도록
     단계별 명령으로 실행한다.

### E112 — JL6c 조건·검색·patch·수치경계 초안 오류

- 분류:
  §DRAFT_CONDITION_AND_TOOLING_ERRORS / DETECTED_AND_CORRECTED_BEFORE_COMMIT /
  SCIENTIFIC_RESULT_IMPACT_NONE§.
- 직전 완료 handoff의 식에서 §D=qT§ 앞 §\qquad§ backslash가 patch 문자열 처리 중
  빠진 채 commit된 것을 이번 시작 감사에서 발견했다. Theory 63, 코드와 검증식에는 같은
  오탈자가 없었고 수학 결과에는 영향이 없다. 이력 문서의 해당 한 글자만 교정했다.
- E108·E111에서 이미 금지한 broad §tmp§ 검색을 다시 실행해 접근 제한 임시 폴더의
  access-denied 잡음을 만들었다. 검색은 읽기 전용이었고 파일·실험 프로세스에는 영향이
  없다. 이후 세 source audit copy와 정본 경로만 명시적으로 조회했다.
- 첫 JL6c evaluator 초안은 네 budget의 합을 §eta_out§ 이하로만 검사하고,
  Jutila 원 parameter와 필요한 §eta_out<=theta§를 강제하지 않았다. 첫 수치 검토에서
  이 조건 누락을 발견해 fail-closed validation을 추가했다. 잘못된 조건의 진단값은
  theory·machine ledger·결론에 쓰지 않았다.
- §B_q§ cutoff equality의 첫 unit test 두 case는 mpmath가 수학적으로 같은 양변을
  마지막 약 \(10^{-118}\) 자리에서 반대 방향으로 반올림해 실패했다. 이를 실제 부등식
  반례로 오인하지 않고, high-precision 진단의 성격에 맞게 §lhs<=rhs or almosteq§를
  요구하도록 교정했다. symbolic proof는 equality이고 재실행 10/10 PASS다.
- Lean status note를 추가한 첫 §apply_patch§는 잘못된 patch 종료 문자열 때문에 적용 전
  거부됐다. 이어 status JSON 초안에는 두 key 오탈자와 두 Lean declaration 명칭 불일치가
  들어갔으나 strict JSON parse와 실제 declaration 검색 전에 발견·교정했다. 손상 상태에서는
  generator·validator·판정·commit을 수행하지 않았다.
- §pdftotext§는 MiKTeX log 파일 접근 warning을 냈지만 stdout text와 exit 0을 반환했다.
  이를 PDF source 실패로 오분류하지 않고, 원 scan page를 별도로 렌더링해 식
  (3.41)--(3.42)를 시각 대조했다.
- 최종 §git add -A§의 첫 sandbox 실행은 §.git/index.lock: Permission denied§로
  거부됐다. 사용자가 금지한 §git apply§ 우회는 사용하지 않았고 working-tree 파일에는
  영향이 없었다. 사용자에게 즉시 알린 뒤 이미 허가된 local stage 범위에서 Git 명령만
  sandbox 외부로 재실행해 cached diff 검증을 통과했다.
- 예방:
  1. 최종 source loss와 내부 budget parameter의 순서관계를 먼저 식으로 쓰고 evaluator
     validation을 그 식에서 직접 복제한다.
  2. §tmp§는 루트 검색하지 않고 필요한 audit-copy 파일 또는 한 폴더만 지정한다.
  3. equality boundary의 부동소수 진단과 directed interval certificate를 구분한다.
  4. status JSON patch 직후 다른 생성 작업보다 먼저 strict JSON parse와 declaration
     존재 검사를 실행한다.
  5. handoff 수식도 commit 전에 inventory 대상 문서와 같은 backslash/control 검사를 한다.
  6. workspace write 권한과 §.git§ metadata write 권한은 다를 수 있으므로 staging 실패를
     파일 patch 실패로 일반화하지 말고, 정확한 §index.lock§ 오류를 보고한 뒤 승인 범위의
     Git 명령만 외부 권한으로 재실행한다.

### E113 — JL8 감사의 경로·도구 호출·Lean 분수 정규화 오류

- 분류:
  §TOOLING_AND_DRAFT_PROOF_ERRORS / DETECTED_AND_CORRECTED_BEFORE_COMMIT /
  SCIENTIFIC_RESULT_IMPACT_NONE§.
- machine-ledger 파일명을 처음에 잘못 추정했으나 `rg --files`로 실제 이름을 찾아
  교정했다. 잘못 추정한 경로에 파일을 만들거나 덮어쓰지 않았다.
- PowerShell `foreach` 출력을 바로 pipe한 첫 조회가 parser error로 끝났고, image helper의
  `forEach` index를 detail 인자로 잘못 전달한 첫 호출도 거부됐다. 둘 다 읽기 단계에서
  멈췄으며 source·산출물에는 영향이 없다.
- 두 명령에 존재하지 않는 작업경로 문자열을 넣어 command 시작 전에 거부됐고, 한
  `apply_patch` 초안은 잘못된 expected text 때문에 적용 전에 거부됐다. 이후 절대 정본
  경로와 작은 patch 단위로 교정했다.
- Lean의 shifted-kernel 상계를 처음 형식화할 때 `rw`가 분수의 실제 정규형과 맞지 않아
  두 번 compile error가 났다. 분모 양수 아래 `field_simp`로 바꿨고, `sorry`, `admit`,
  project-local `axiom` 없이 direct Lean check를 PASS했다. 실패 중인 선언을 결과로
  기록하지 않았다.
- 한 번은 `lean/`을 cwd로 둔 채 repository-root 상대 Python unittest를 호출해
  `ModuleNotFoundError`가 났다. 같은 test를 repository root에서 다시 실행해 PASS했고,
  코드 결함으로 오분류하지 않았다.
- 후속 `lake build`와 targeted test를 한 command에 묶으면서 같은 cwd 실수를 한 번
  반복했다. 마지막 command인 build가 exit 0이었다는 이유로 전체를 PASS라 하지 않고,
  targeted test를 repository root에서 별도로 재실행해 6/6 PASS를 확인했다.
- 두 차례 tool-orchestration 입력에 우발적인 문자열이 섞여 JavaScript parser가 command
  시작 전에 거부했다. shell·patch는 실행되지 않았고, 정상 입력으로 다시 호출했다.
- sandbox 안의 첫 전체 unittest는 `TemporaryDirectory` 생성·정리 권한 때문에 82개
  `PermissionError`를 냈다. 이를 82개 코드 회귀로 보고하지 않고, 사용자가 사전 허용한
  정상 로컬 권한에서 같은 733개 test를 재실행해 733/733 PASS를 확인했다.
- 작업원장 2단계 완료 시각을 파일 timestamp보다 한 시간 뒤인 `15:32`로 잘못 적었다.
  실제 순서와 file timestamp에 맞는 `14:32`로 교정했다. 과학 내용에는 영향이 없다.
- `pdftotext`가 MiKTeX log 파일 access warning을 냈지만 native text stdout과 exit 0은
  유효했다. Jutila는 실제 text layer가 비어 OCR을 locator로만 쓰고 렌더링 페이지와
  대조했으며, McCurley·Gallagher는 native text 우선 뒤 수식을 렌더링 원문과 대조했다.
- 첫 JSON 묶음 검사는 PowerShell `ConvertFrom-Json`이 유효한 대소문자 구별 key
  `Delta`/`delta`를 같은 key로 취급해 오류를 냈는데도, command가 stop-on-error가 아니어서
  뒤의 `JSON_PASS` 문자열까지 출력했다. 이를 PASS로 기록하지 않았다. ledger key를
  `strip_height`/`alpha_defect`로 바꾸고 strict parser로 다시 검사한다.
- 첫 UTF-8 검사에서 두 Git 출력 배열을 중첩 배열로 만들었고, PowerShell이 여러 경로를
  한 문자열처럼 결합해 `ReadAllText`가 실패했다. 파일 쓰기는 없었다. 배열을 명시적으로
  평탄화해 변경 text 19파일의 strict UTF-8·control-character 검사를 PASS했다.
- 예방:
  1. source·ledger 이름은 추정하지 말고 `rg --files` 결과를 먼저 고정한다.
  2. PowerShell collection과 JS callback의 암묵 인자를 피하고 명시 loop를 쓴다.
  3. Lean 분수 증명은 목표 정규형을 compile error context에서 확인한 뒤 양의 분모를
     명시해 단계별로 곱한다.
  4. repository import test는 항상 repository root에서 실행한다.
  5. 큰 다중파일 patch보다 독립적으로 검증 가능한 작은 patch를 사용한다.
  6. PowerShell JSON 검사는 `-AsHashTable`과 stop-on-error를 쓰고, 가능하면 Python strict
     parser와 교차검증한다. 오류 뒤의 자체 출력 문자열을 성공 증거로 쓰지 않는다.

### E114 — Jutila 식 (3.6)과 Theorem 1-prime의 Barban--Vehov 매개변수 혼동

- 분류:
  `MATHEMATICAL_SCOPE_ERROR / COMMITTED_PREDECESSOR_CORRECTED_BY_SUCCESSOR /
  NO_NUMERICAL_X_CERT_RESULT_EXISTED`.
- Theory 60과 그 후속 요약에서 fixed `tau=8/5`, coefficient `37.769894`를 Jutila
  식 (3.6)의 one-sided weighted square-sum 호출에 적용할 수 있다고 기록했다. 원문
  printed pp.52--54를 proof branch별로 다시 대조한 결과, 이 고정 매개변수는 p.54의
  Theorem 1-prime에만 해당한다. p.52 식 (3.6)은
  `z1=D^(1/2+7 theta)`, `z2=D^(1/2+8 theta)`이므로
  `tau_theta=(1+16 theta)/(1+14 theta)`다.
- 기존 fixed coefficient의 exact 계산 자체는 맞았지만 적용 대상이 틀렸다. 잘못된
  coefficient로 numerical PAP, fixed Sono coefficient 또는 `X_cert`를 계산한 적은 없으므로
  폐기할 numerical result는 없다. 그러나 그대로 두면 향후 threshold calculator 기반을
  훼손하는 중대한 선행 scope 오류였다.
- Theory 66에서 theta-dependent coefficient를 다시 특수화해
  `K_BV(theta)<13/theta`, weighted/log 결합 상계 `34/theta^2`를 얻었다. Theory 60,
  machine ledger, tests, METHODS, AGENTS, review와 Lean 주석을 successor correction으로
  동기화했다. fixed `37.769894`는 역사적으로 삭제하지 않고 Theorem 1-prime scope로
  재분류했다.
- 이번 작업 중 새 Theory 66·Review 73을 첫 patch에서 JavaScript 일반 문자열로 전달해
  LaTeX backslash가 tab·carriage-return 등 escape로 해석되는 E107 유형 오류를 한 번
  재발시켰다. commit 전에 제어문자와 손상된 display delimiter를 발견했고 두 초안 파일을
  삭제한 뒤 raw-safe patch로 전수 재작성했다. 수학 코드·Lean·기계 원장에는 이 손상문서를
  근거로 한 결과를 남기지 않았다.
- optional symbolic 확인에서 설치되지 않은 `sympy` import를 한 번 시도해
  `ModuleNotFoundError`가 났다. 표준 `fractions.Fraction`만으로 exact 대수가 충분하므로
  package 설치를 요청하거나 환경을 변경하지 않았다.
- Lean 초안은 coefficient 분모 정규화, log-ratio 덧셈 정규형, total-exponent 곱셈 정규형,
  양수 인자 cancellation에서 세 차례 compile 오류를 냈다. 각 실패 목표를 근거로 direct
  proof를 교정했고 proof escape 없이 최종 direct Lean check를 다시 통과시켰다. 실패 초안을
  검증 완료로 기록하지 않는다.
- 예방:
  1. 같은 논문의 서로 닮은 proof branch도 theorem 번호, printed page, 실제 parameter tuple을
     machine ledger의 `scope_id`로 분리한다.
  2. 상수를 downstream 식에 넣기 전에 source parameter map을 exact test로 고정한다.
  3. LaTeX가 포함된 대형 patch는 처음부터 raw-safe 문자열을 사용하고 patch 직후 strict
     UTF-8·제어문자·display delimiter 검사를 수행한다.
  4. optional dependency import보다 표준 exact arithmetic 가능성을 먼저 확인한다.

### E115 — JL7-CONT 초안의 source hash·LaTeX escape·검증 작업경로 실수

- 분류:
  `PRE_COMMIT_DRAFT_CORRUPTION / SOURCE_HASH_TRANSCRIPTION / CONTROL_CHARACTER /
  VALIDATION_WORKDIR_ERROR / NO_SCIENTIFIC_RESULT_AFFECTED`.
- Theory 67용 JSON 첫 초안에서 Jutila PDF SHA-256 문자열 뒤에 임시 메모 조각이 섞였다.
  source-hash test와 원 PDF 재해시 전에 발견해 정확한
  `f6e9038a7216b690763692e0a07bc8c58284c9560bf62ab987ea62a817404ad5`로 교정했다.
  잘못된 hash를 provenance PASS나 수학 판정에 사용하지 않았다.
- JavaScript 일반 문자열로 전달한 Markdown patch에서 `\theta`의 `\t`와 `\bar`의 `\b`가
  tab·backspace로 해석되는 E107/E114 계열 오류가 다시 생겼다. 두 새 문서의 전수
  control-character 검사에서 commit 전에 발견했고, `apply_patch`로 교정했다. backslash가
  조용히 빠진 `qquad` 두 곳도 formula inventory preview에서 발견해 `\qquad`로 복구했다.
- 점검용 PowerShell 명령 하나는 빈 pipe element ParserError를 냈고, 명시 `$rows` 변수로
  재실행했다. 또한 저장소 루트에서 Lean generator를 `tools/...`로, `lake build`를 root
  lakefile 대상으로 잘못 호출해 각각 path/configuration error가 났다. 올바른
  `lean/tools/...`와 `lean/` working directory에서 재실행해 generator·validator·build·
  direct Lean check를 모두 PASS했다. 실패 명령의 출력을 성공 증거로 사용하지 않았다.
- 수학·결과 영향: 없음. actual prime 계산이나 threshold calculator를 실행하지 않았고,
  초안 오류는 모두 commit·정본 동기화 전 교정됐다. `JL7-CONT` 판정은 교정된 source hash,
  9개 target test, strict JSON, Lean kernel과 전체 검증만 근거로 한다.
- 예방:
  1. 외부 PDF hash는 사람이 재입력하지 말고 `Get-FileHash` 출력과 기계 원장을 test로 연결한다.
  2. LaTeX patch는 raw-safe 입력을 사용하고 직후 tab·C0 control·backslash 소실 패턴을 함께
     검사한다. 제어문자 0건만으로 `\qquad` 같은 무효 escape 소실까지 잡힌다고 가정하지 않는다.
  3. Lean maintenance 명령은 `lean/README.md`의 고정 working directory와 절대 도구 경로를
     그대로 복사한다. generator 경로와 Lake project root를 별개로 추정하지 않는다.
  4. 같은 검증 단계의 첫 명령이 실패하면 후속 출력이 있더라도 전체 PASS로 묶지 않고,
     실패 원인을 기록한 뒤 올바른 경로에서 독립 재실행한다.

### E116 — JL7-LEMMA3 source 도구 추정·초안 key·patch 문맥 불일치

- 분류:
  `PRE_COMMIT_TOOLING_AND_DRAFT_ERRORS / DETECTED_AND_CORRECTED /
  NO_SCIENTIFIC_RESULT_AFFECTED`.
- Motohashi PDF native text를 읽을 때 workspace dependency가 반환한 bundled Poppler 경로에
  `pdftotext.exe`도 있을 것으로 먼저 가정했으나 실제로는 없었다. 이 실패 출력은 source
  증거로 사용하지 않았다. 설치된 MiKTeX `pdftotext.exe`로 다시 추출하고, Adobe-Japan1
  font-map warning 때문에 printed p.816 렌더링 원페이지와 수식을 대조했다.
- machine JSON 초안의 `rendered_printed_pages_checked` key에 임시 공백이 들어갔으나 strict
  JSON·schema 검증 전에 발견해 즉시 교정했다. 잘못된 key를 provenance 판정에 사용하지
  않았다.
- 상위 요약·handoff patch의 JavaScript 일반 문자열에서 인라인 수식 구분자 `\(`, `\)`의
  backslash가 소실돼 `(p)`, `(3R^2)`처럼 일반 괄호로 보이는 E107 계열 서식 오류가
  재발했다. display 수식과 수치에는 영향이 없었고 정적 TeX 검색에서 commit 전에 발견해
  모든 신규 단락의 인라인 delimiter를 복구했다.
- Lean finite divisor proof는 별도 scratch에서 타입·분수 정규형을 순차 교정한 뒤 direct
  compile PASS를 확인하고 단일 정본 파일로 옮겼다. scratch는 commit 전에 삭제했고,
  `sorry`, `admit`, project-local `axiom`은 사용하지 않았다.
- Lean README와 작업원장의 첫 일괄 `apply_patch`는 예상 문맥이 실제 tail과 달라 적용 전에
  거부됐다. 정확한 파일 끝을 다시 읽고 작은 patch로 적용했다. 이는 과거 sandbox patch
  장애의 재발이 아니며 대상 파일을 부분 손상시키지 않았다.
- `git status --short --ignored`를 좁은 경로 확인에 사용하면서 기존 ACL 제한
  `tmp/tmp*` 디렉터리를 대량 순회해 access-warning을 만들었다. 이 출력은 상태 판정에
  사용하지 않고 `git check-ignore`와 평범한 `git status --short`로 다시 확인했다.
- direct Lean compile과 `lake build`를 한 30초 호출에 묶어 tool wrapper가 child session
  ID를 표면에 남기지 못했다. `Get-CimInstance` 확인도 권한 거부됐지만, 비파괴적인
  `Get-Process`로 실행 중임을 확인하고 종료를 기다렸다. 완료 뒤 cached `lake build`를
  독립 재실행해 `Build completed successfully (8765 jobs)`, exit 0을 확보했다.
- 첫 staged 감사에서 `git diff --cached --check` 뒤에 stat/status 명령을 연이어 실행해
  세 신규 파일의 `new blank line at EOF` 경고가 있었는데도 shell 전체 종료코드는 0이었다.
  경고를 PASS로 취급하지 않고 세 EOF 빈 줄을 제거한 뒤 staged check를 단독 재실행해
  exit 0을 확인했다.
- 영향: actual prime 계산과 threshold calculator는 실행하지 않았고, numerical
  `X_cert`, fixed `2e-17`, PAP 또는 terminal density를 승격하지 않았다. 최종 판정은
  교정된 source hash, 렌더링 대조, exact Python test, Lean kernel 검증에만 의존한다.
- 예방:
  1. dependency runtime의 디렉터리 이름만 보고 개별 executable 존재를 가정하지 않고
     `Test-Path`/`Get-Command`로 먼저 확인한다.
  2. 새 machine-ledger key는 strict parser와 표적 test로 즉시 고정한다.
  3. 긴 문서 patch는 적용 직전에 짧은 tail을 읽고 독립 hunk로 나눈다.
  4. scratch proof는 canonical 단일 파일 direct compile 뒤 삭제 여부를 `git status`로 확인한다.
  5. ignored tree 전수 status와 Lean compile+build 묶음 호출을 피하고, 좁은 경로·단계별
     명령으로 종료코드를 각각 확보한다.
  6. `git diff --check`와 `git diff --cached --check`는 뒤 명령과 묶지 않고 단독 실행한다.

### E117 — JL7-RES 경계 반올림·LaTeX escape·scratch 계수 입력 오류

- 분류:
  `PRE_COMMIT_NUMERICAL_BOUNDARY_AND_DRAFT_ERRORS / DETECTED_AND_CORRECTED /
  NO_SCIENTIFIC_RESULT_AFFECTED`.
- 첫 Python 표적시험에서 부동소수 `theta=1/21`의 역제곱이 441보다 극미량 크게
  표현되어, 정확히 허용돼야 할 `L=441`과 `Delta=1/441` 간격을 validator가
  거부했다. 수학 cutoff를 느슨하게 바꾸지 않고 `mp.almosteq`로 표현상 같은
  endpoint만 허용했다. 수정 후 12개 표적시험이 모두 PASS했다.
- 독립 검산을 70 dps의 3중 nested quadrature로 처음 구현해 30초 호출 안에 끝나지
  않았다. 같은 triple integral에 Fubini를 적용해 두 독립 1차원 numerical quadrature로
  바꿨다. 이는 closed endpoint formula를 사용하지 않는 독립 oracle 성격을 유지하면서
  12개 suite를 약 2.5초에 끝낸다.
- scratch 진단 출력 한 줄에서 row coefficient를 `3*(7*theta+70)`로 잘못 입력해
  `211`을 출력했다. 올바른 식은 `21*theta^2+70*theta<=91*theta`다. 이 scratch
  수치는 문서·JSON·코드·Lean 결과에 사용하지 않았고, 최종 residue coefficient는
  exact `12*91/21=52`로 다시 검증했다.
- 새 Theory 69·Review 76의 첫 patch도 JavaScript 일반 문자열을 사용해 `\bar`의
  backspace, `\varphi`의 vertical-tab, `\theta`의 tab과 `\rm`의 carriage-return이
  일부 초안에 들어갔다. commit 전에 byte-level control scan과 formula inventory
  preview로 발견했고, `apply_patch`를 사용한 raw-safe 재작성 및 인라인 delimiter
  복구 뒤 두 파일의 C0 control·tab이 0건임을 확인했다.
- 첫 Lean build는 eta coefficient 결론의 곱셈 결합형이 목표와 달라 type mismatch가
  났다. 교환·결합법칙을 명시한 `simpa`로 고친 뒤 전체 8,765 jobs build와 ledger
  validator를 다시 PASS했다. `sorry`, `admit`, project-local `axiom`은 사용하지 않았다.
- 문서 동기화 중 일부 `apply_patch`가 실제 tail 문맥 차이 또는 JavaScript template의
  Markdown backtick 때문에 실행 전에 거부됐다. 작은 hunk와 placeholder 방식으로
  재적용했으며 거부된 patch가 파일을 부분 수정하지 않았음을 확인했다.
- 전체 unittest를 먼저 sandbox 안에서 실행해 `TemporaryDirectory` 쓰기·정리
  `PermissionError` 82건이 발생했다. 이를 회귀로 보고하지 않고 같은 773개 suite를
  허가된 정상 로컬 권한에서 재실행해 전부 PASS임을 확인했다. 실패 출력에는 새 residue
  표적시험도 모두 PASS였고, 오류 traceback은 임시경로 접근으로 일관됐다.
- 예방:
  1. LaTeX 포함 patch는 처음부터 raw-safe 문자열과 backtick placeholder를 함께 쓴다.
  2. exact endpoint를 arbitrary precision float로 받는 validator는 exact rational 입력과
     표현오차 동등성 검사를 분리한다.
  3. 고정밀 독립 적분 oracle은 먼저 Fubini·대수적 차원축소 가능성을 확인한다.
  4. scratch 출력도 정본 식에서 coefficient를 재사용하고, 수작업 재입력값을 판정 근거로
     사용하지 않는다.
  5. 첫 Lean 실패와 patch 거부는 최종 PASS 로그와 분리해 원장에 남긴다.

### E118 — JL7-ABSORB 수치 허용오차·Lean proof 초안·patch transport 오류

- 분류:
  <code>PRE_COMMIT_TEST_AND_PROOF_DRAFT_ERRORS / DETECTED_AND_CORRECTED /
  NO_SCIENTIFIC_RESULT_AFFECTED</code>.
- 첫 표적시험은 \(L_{\rm abs}=\log\mathcal P/\gamma\)에서 계산한 흡수비가 정확히
  \(1/2\)와 같다고 <code>mp.almosteq</code>의 기본 허용오차로 검사했다.
  \(\theta=1/100\)에서 약 \(3.3\times10^{-100}\)의 고정밀 평가 오차 때문에 한 건이
  실패했다. 기호식이나 cutoff를 바꾸지 않고 100 dps에 충분히 엄격한
  <code>abs(value-1/2)&lt;10^-90</code>로 판정을 명시했다. 수정 뒤 표적 11건이 PASS했다.
- Theory 70·review 초안의 첫 큰 patch는 JavaScript 문자열 안의 LaTeX
  backslash 또는 Markdown backtick transport 때문에 실행 전에 거부됐다.
  거부된 호출은 파일을 부분 변경하지 않았다. raw-safe 문자열, 작은 hunk와
  backtick placeholder를 사용해 정상 <code>apply_patch</code>로 다시 적용했다.
- 첫 Lean compile은 함수표현을 펼치지 않은 <code>rw</code>, 예약어
  <code>local</code>, 이미 목표를 닫은 <code>field_simp</code> 뒤의 불필요한
  <code>ring</code> 때문에 실패했다. 표현을 명시적으로 <code>change</code>하고
  변수명을 <code>radius</code>로 바꾸며 불필요한 tactic을 제거했다. 두 번째
  log-gate 초안도 분수의 결합형이 달라 rewrite가 실패해, exact ring 정규화와
  단조성의 단계별 <code>calc</code>로 교정했다. 최종 direct Lean compile은 exit 0이다.
- ledger validator PASS 뒤의 별도 요약용 scratch 명령은 JSON key를
  <code>formula_statuses</code>로 잘못 가정해 <code>KeyError</code>를 냈다.
  정본 validator가 이미 1,271식을 전부 PASS하고 상태 수를 출력했으므로 검증 결과에는
  영향이 없으며, 이후 정본 schema key를 먼저 확인하도록 한다.
- 일반 <code>git diff --check</code>를 먼저 통과시켰지만, 아직 untracked였던 Theory 70은
  그 검사 범위에 포함되지 않았다. 명시적 allowlist staging 뒤의 독립
  <code>git diff --cached --check</code>가 EOF 빈 줄 1건을 발견했다. 빈 줄을 제거하고
  staged 검사를 다시 실행했다. 이어서 Lean ledger validator가 source hash 불일치를
  fail-closed로 검출했다. EOF 보정도 source 바이트를 바꾸기 때문이었다. generator를
  다시 실행해 inventory와 human ledger를 동기화한 뒤 validator를 재통과시켰다.
  내용·수식·검증 결과에는 영향이 없다.
- 예방:
  1. 초월함수 경계의 numerical equality는 작업 dps와 독립적인 명시적 절대오차로 검사한다.
  2. Lean proof는 함수표현·분수 결합형과 예약어를 먼저 정규화한 뒤 tactic을 적용한다.
  3. 긴 LaTeX patch는 처음부터 raw-safe transport와 작은 hunk를 사용한다.
  4. 검증 정본 명령과 편의용 scratch 통계를 같은 PASS로 묶지 않는다.
  5. 신규 파일이 있는 마감에서는 일반 diff 검사만으로 끝내지 않고, 명시적 staging 뒤
     <code>git diff --cached --check</code>를 반드시 단독 gate로 실행한다.
  6. theory 문서는 공백만 바꿔도 source hash가 달라지므로 마지막 문서 보정 뒤에는
     Lean ledger generator와 validator를 순서대로 다시 실행한다.

### E119 — JL7-AVERAGED LaTeX transport와 Lean API 초안 오류

- 분류:
  <code>PRE_COMMIT_DOCUMENT_AND_FORMAL_PROOF_DRAFT_ERRORS /
  DETECTED_AND_CORRECTED / NO_SCIENTIFIC_RESULT_AFFECTED</code>.
- Theory 71 초안의 세 식에서 JavaScript 일반 문자열 transport가
  <code>\qquad</code>의 선행 backslash를 잃어
  <code>L^2,qquad</code>, <code>Rz_2,qquad</code>,
  <code>Q^2,qquad</code>로 저장됐다. 수식의 변수·부등호·계수는 바뀌지 않았고,
  정본 동기화 전에 PCRE 검색으로 발견해 세 곳 모두 교정했다.
- 첫 Lean 형식화에서 양의 \(L^2\)를 부등식 양변에서 소거할 때 현재 Mathlib의
  <code>mul_le_mul_right</code> API를 iff처럼 호출해 compile이 실패했다.
  목적에 맞는 <code>le_of_mul_le_mul_right</code>로 바꿨다.
- local-count log upper의 첫 초안도 중첩 곱셈에서 nonnegative multiplier
  metavariable가 해소되지 않았다. \(Q T\le Q^2T\)를 별도 명제로 만든 뒤
  명시적 두 배 곱셈으로 분리했고 direct Lean compile exit 0을 확인했다.
- 새 Jutila PDF는 5개 landscape PDF page가 printed pp.55--62를 두 면씩 담지만,
  첫 machine ledger는 이번에 사용한 핵심 부분만 따라 rendered check를 pp.55--59로
  불완전하게 기록했다. 최종 감사에서 5개 PDF page 전체를 직접 확인하고
  rendered 범위를 pp.55--62로 교정했다.
- 최종 UTF-8 검사 초안에서 PowerShell의 두 명령 출력을 중첩 배열로 합쳐, 실제 파일
  목록 대신 여러 경로가 이어 붙은 두 개의 가짜 경로를 검사했다. 그 결과는 유효한
  검사 결과가 아니므로 즉시 폐기했고 파일에는 아무 변경도 가하지 않았다. 최종 검사는
  명시적 경로 목록과 독립 JSON·Markdown 검사를 사용한다.
- 수정된 UTF-8 검사 첫 실행도 colon 바로 앞의 PowerShell 변수
  <code>$p:</code>를 쓴 탓에 parser 단계에서 멈췄다. format operator를 사용해
  재실행했고 19개 파일 모두 strict UTF-8·control issue 0을 확인했다.
- JSON 검사 첫 실행은 PowerShell의 case-insensitive object 변환이 inventory 안의
  <code>delta</code>/<code>Delta</code>를 같은 key로 보아 경고했는데도 nonterminating
  error 뒤 PASS 문자열까지 출력했다. 이 결과를 폐기하고
  <code>$ErrorActionPreference='Stop'</code>과 <code>-AsHashtable</code>로 다시 실행해
  JSON 3개를 정상 parse했다.
- AGENTS 상단 successor 문단은 Theory 71을 정확히 기록했지만, 아래의 긴 현재상태
  요약 한 곳이 여전히 “averaged replay OPEN·Theory 70 최신”이라고 적혀 있었다.
  최종 stale-reference 검색에서 발견해 narrow averaged branch는 닫혔고 PAP는
  열려 있다는 현재 판정과 Theory 71/review 78 링크로 교정했다.
- 이 실패들은 commit 전 형식검증 단계에서 발견됐고 analytic 판정이나 Python
  진단값을 변경하지 않았다. <code>sorry</code>, <code>admit</code>,
  project-local <code>axiom</code>은 사용하지 않았다.
- 예방:
  1. LaTeX patch는 raw-safe transport를 사용하고 모든 새 theory에
     missing-command PCRE와 control-character scan을 수행한다.
  2. Lean의 order API는 저장소 내 현재 Mathlib 사용례를 먼저 검색한 뒤 적용한다.
  3. 여러 곱의 단조성은 중간 부등식과 부호 전제를 이름 붙여 elaborator의
     암묵 metavariable에 의존하지 않는다.
  4. PowerShell에서 여러 외부 명령의 line output을 합칠 때는 중첩 배열을 만들지 말고,
     각 출력을 명시적으로 평탄화하거나 검증 대상 allowlist를 직접 고정한다.
  5. ad-hoc PowerShell 검사는 fail-fast를 기본으로 하고 JSON key case를 보존하는
     hashtable parser를 사용하며, 오류 뒤 출력된 PASS 문자열은 증거로 인정하지 않는다.
  6. successor를 덧붙인 뒤에도 기존 “최신 상태” 요약을 검색해 최신 정본 번호와
     OPEN/CLOSED 문구가 서로 충돌하지 않는지 확인한다.

### E120 — Gallagher--Maier PAP split 작성·검증 중 transport와 시험 초안 오류

- 분류:
  <code>PRE_COMMIT_DOCUMENT_TEST_AND_FORMAL_PROOF_DRAFT_ERRORS /
  DETECTED_AND_CORRECTED / NO_SCIENTIFIC_RESULT_AFFECTED</code>.
- 첫 작업원장 patch는 JavaScript template 안의 Markdown backtick 때문에
  <code>ReferenceError</code>로 실행 전에 거부됐다. Theory·review 대형 patch와
  후속 METHODS·AGENTS patch에서도 같은 계열의 parser 오류가 있었고, 다중 파일
  patch 한 번은 hunk 구분 형식 오류로 거부됐다. 거부된 호출은 파일을 부분 변경하지
  않았다. 작은 hunk와 backtick placeholder를 사용해 정상 apply_patch로 다시 적용했다.
- 첫 표적시험은 허용범위 \(\theta\le1/21\) 밖의 toy 값 \(\theta=1/5\)를 썼고,
  저장된 60자리 decimal과 90-dps quadrature를 기본 <code>mp.almosteq</code>로
  비교했다. 각각 1 error·1 failure로 검출됐다. 수학 공식을 바꾸지 않고
  \(\theta=1/42\)와 명시적 상대오차 \(10^{-55}\)로 교정했으며, 후속 11건이 PASS했다.
- 첫 Lean endpoint conjunction에서 두 분수의 타입 주석이 없어 Nat division으로
  추론되어 목표가 False가 됐다. 분자에 \((1:\mathbb R)\)을 명시했고 direct
  kernel compile exit 0을 확인했다. source theorem을 local axiom으로 넣지 않았다.
- 재컴파일 호출 한 번은 wrapper가 반환한 session id를 요약 출력에서 누락해 종료
  상태를 보존하지 못했다. 동일 커널 검사를 다시 시작해 session id를 보존하고
  exit 0을 확인했다. 중복 실행은 소스나 산출물을 바꾸지 않았다.
- 광범위한 임시경로 검색과 process command-line 조회는 접근 거부 메시지를 냈다.
  필요한 정본 경로는 명시적 allowlist로 다시 검사했고, 실행 중 사용자 프로세스를
  중단하거나 수정하지 않았다.
- 새 문서 LaTeX command 누락 검사의 첫 정규식은 prose의 영문 alpha, theta와
  quadrature 안의 quad까지 오류로 분류했다. 이 출력은 무효로 폐기하고 display
  delimiter 쌍과 실제 과거 손상형인 comma-qquad·bare-frac만 표적 검사해 issue 0을
  확인했다.
- 전체 unittest의 첫 sandbox 실행도 TemporaryDirectory 생성·정리 권한 때문에
  805건 중 82건이 PermissionError로 끝났다. 이를 코드 실패로 해석하지 않고 같은
  명령을 사용자가 이미 허가한 정상 로컬 권한에서 재실행했으며, 805건이 74.799초에
  전부 PASS했다. 첫 실패가 남긴 임시경로는 다른 tmp provenance와 섞일 수 있어
  이 작업에서 임의 삭제하지 않았다.
- 최종 보강에서 Bennett uniform helper가 작은 \(\ell\)의 source zero-free branch를
  일반 error 식으로 평가할 수 있음을 발견했다. 실제 \(T=Q^5\) 진단에는 영향이
  없었지만, source theorem대로 0을 반환하도록 고치고 경계 회귀시험을 추가했다.
- cached diff를 식 단위로 읽는 마지막 감사에서 Theory 72의 식 (72.2)와 (72.3)에
  줄바꿈 앞 덧셈기호가 각각 하나씩 빠진 것을 발견했다. Gallagher printed p.338의
  식 (30)과 바로 다음 Stieltjes identity를 native text로 다시 대조해 두 기호를
  복구했다. Python 계산과 Lean partial theorem은 처음부터 endpoint와 \(Q^4/T\)를
  별도 항으로 다뤄 수치 결과에는 영향이 없었다. 문서 hash가 바뀌었으므로
  inventory를 재생성하고 전수 검증을 다시 수행했다.
- 위 실패는 모두 commit 전에 발견됐다. analytic 식, diagnostic 수치, OPEN 판정과
  사용자 데이터에는 영향이 없다. <code>sorry</code>, <code>admit</code>,
  project-local <code>axiom</code>은 사용하지 않았다.
- 예방:
  1. LaTeX·Markdown patch는 처음부터 backtick placeholder와 작은 hunk를 사용한다.
  2. toy parameter도 production domain validator를 통과하는 값으로 고정한다.
  3. 서로 다른 정밀도의 decimal 비교는 요구 유효자리보다 엄격한 명시적 오차를 쓴다.
  4. Lean의 수치 literal·division은 목표 type이 모호하면 처음부터 Real 주석을 붙인다.
  5. 장시간 tool session은 session id와 최종 exit code를 원문 그대로 보존한다.
  6. 임시경로 전수검색보다 정본 allowlist를 우선하며, 접근 거부 뒤 PASS를 추론하지 않는다.
  7. TemporaryDirectory·multiprocessing을 쓰는 전체 suite는 처음부터 승인된 정상
     로컬 권한에서 실행하고, sandbox 결과와 정상권한 결과를 별도 증거로 기록한다.
  8. LaTeX command 누락 scan은 일반 영단어와 겹치는 command stem을 쓰지 말고
     과거 손상 형태와 delimiter 구조만 표적으로 검사한다.
  9. display 수식은 delimiter·command뿐 아니라 각 줄의 이항연산자가 줄바꿈에서
     누락되지 않았는지 cached diff와 source 원문을 함께 읽어 확인한다.

### E121 — C_J loss-tree 감사의 탐색·초안 호출·Lean proof 오류

- 분류:
  <code>PRE_COMMIT_SEARCH_TEST_DOCUMENT_AND_FORMAL_PROOF_DRAFT_ERRORS /
  DETECTED_AND_CORRECTED / NO_SCIENTIFIC_RESULT_AFFECTED</code>.
- source 탐색 초기에 `article`과 `tmp`를 너무 넓게 한 번 검색해, 이번 감사와 무관한
  임시경로에서 접근 거부 경고가 다수 출력됐다. 이후 Theory 64--72가 고정한 두 PDF와
  predecessor artifact allowlist만 검사했다. 사용자 프로세스나 파일을 변경·중단하지 않았다.
- 수치 확인용 첫 scratch 명령은 존재하지 않는 함수명
  <code>asymptotic_near_upper</code>를 import했고, 두 번째는 keyword-only 함수
  <code>near_asymptotic_certificate_limit</code>를 positional argument로 호출해 실패했다.
  두 출력은 증거에서 폐기하고 실제 module signature를 확인한 세 번째 호출과 정식
  fail-closed unit test로 재계산했다.
- Theory 73 초안의 세 LaTeX 식에서 transport 과정에 <code>\le</code>와
  <code>\qquad</code>의 선행 backslash가 빠졌다. 수식 정본·inventory 생성 전에 검색으로
  발견해 복구했다.
- 첫 Lean absorption proof는 이미 닫힌 <code>field_simp</code> 뒤 불필요한 tactic을
  실행했고, 나눗셈 정리의 곱셈 결합형을 잘못 제시해 compile이 실패했다. 곱을 명시적으로
  재결합하고 불필요 tactic을 제거했다. full denominator proof 초안에서도 unary minus의
  parser 결합형, 현재 Mathlib의 제곱 nonzero lemma 이름, 곱의 순서가 맞지 않아 compile이
  실패했다. 표준 exponential order와 명시적 ring normalization으로 교정한 뒤 direct Lean
  compile exit 0을 확인했다.
- METHODS에 successor 절을 붙이는 첫 patch는 실제 마지막 문맥과 맞지 않아 적용 전에
  거부됐고 파일은 부분 변경되지 않았다. 더 좁은 hunk로 정상 적용했다.
- 최종 정적검사에서 모든 변경 파일에 단순한 수식 delimiter 개수 검사를 적용해, 오류원장과
  자동생성 Lean 원장 안의 코드 literal·과거 예시까지 수식으로 오인한 false positive가
  발생했다. UTF-8·금지 제어문자 검사는 그대로 유효했지만 delimiter 판정은 폐기했다.
  신규 theory·review·작업원장처럼 실제 수식 문서인 세 파일에 범위를 좁혀 다시 검사해
  display·inline delimiter가 모두 짝을 이룸을 확인했다.
- 이 실패들은 모두 commit 전 검증에서 발견됐다. exact coefficient, PAP gap 판정,
  OPEN 상태에는 영향이 없고 `sorry`, `admit`, project-local `axiom`은 사용하지 않았다.
- 예방:
  1. 대형 `tmp` 전수검색보다 predecessor ledger의 고정 source allowlist를 우선한다.
  2. scratch 호출 전 실제 함수 signature를 먼저 확인하고 scratch PASS를 정식 시험과 구분한다.
  3. 새 theory는 inventory 전에 missing-command 표적검색을 실행한다.
  4. Lean 분수·지수 proof는 parser 결합형과 현재 Mathlib lemma 이름을 작은 단계에서 확인한다.
  5. 긴 정본 문서 append는 마지막 5--10줄을 다시 읽고 좁은 hunk로 적용한다.
  6. Markdown 수식 delimiter 검사는 코드 literal을 포함한 원장 전체에 기계적으로 적용하지
     말고, 새 수식 본문 allowlist에만 적용한다.

### E122 — modern density source-screen의 저자·서지 초안 및 도구 호출 오류

- 분류:
  <code>PRE_COMMIT_SOURCE_METADATA_DOCUMENT_AND_TOOLING_DRAFT_ERRORS /
  DETECTED_AND_CORRECTED / NO_SCIENTIFIC_RESULT_AFFECTED</code>.
- 첫 작업원장 Add File patch는 JavaScript string 안의 Markdown backtick 때문에 parser에서
  실행 전에 거부됐다. 파일은 생성되지 않았고 정상 `apply_patch`로 다시 만들었다.
- 초기 source 조회 한 번은 존재하지 않는 예상 test 파일명과 Windows에서 해석되지 않는
  wildcard 경로를 `rg`에 넘겼다. 조회만 실패했고 명시적 파일 경로로 다시 검사했다.
- hash 수집용 PowerShell scratch에서 `foreach` block을 직접 pipe해 빈 pipe parser 오류가
  났다. `$rows`에 결과를 먼저 저장한 뒤 같은 read-only 계산을 성공시켰다.
- Bellotti 공동연구자의 이름을 초안 machine ledger에서 근거 없이
  `Daniel R. Johnston Castillo`로 적었다. 공식 연구페이지와 CV를 다시 확인해
  `Cruz Castillo`로 교정했다. 공개 원고가 없다는 판정에는 영향이 없다.
- Theory 74 참고문헌 초안에서 Maier 1981을 다른 Maier 논문의 제목으로,
  McCurley 1984를 다른 서지·DOI로 잘못 적었다. 사용자가 제공한 두 PDF 첫 페이지와
  기존 hash-pinned source registry를 재대조해 각각 *Chains of Large Gaps between
  Consecutive Primes*, DOI `10.1016/0001-8708(81)90003-7` 및 *Explicit Zero-Free
  Regions for Dirichlet L-Functions*, DOI `10.1016/0022-314X(84)90089-1`로 교정했다.
- local MiKTeX `pdftotext`는 로그파일 접근에 관한 `log4cxx` 경고를 냈지만 native text
  출력은 정상 생성됐다. 새 네 PDF는 Poppler 렌더 중 Symbol display-font 경고가 있었으나
  페이지 PNG와 핵심 수식은 온전했다. 경고를 PASS 근거로 무시하지 않고 산출물을 직접 확인했다.
- METHODS 첫 append는 마지막 문맥을 너무 짧게 지정해 hunk가 적용 전에 거부됐다.
  실제 tail 두 줄을 다시 읽고 좁은 hunk로 적용했으며 부분 변경은 없었다.
- Lean generator 첫 호출의 선행 `Get-Content`는 작업 디렉터리가 이미 `lean/`인데 다시
  `lean/verification/...`을 붙여 조회만 실패했다. 이어진 generator·validator는 정상 경로로
  PASS했고, 최종에는 올바른 경로로 재검증한다.
- direct Lean compile의 첫 wrapper는 출력 문자열만 표시해 session id를 보존하지 못했다.
  동일 compile을 다시 실행해 두 번째 session의 exit 0을 확인했다. 중복 compile은 source나
  연구 산출물을 변경하지 않는다.
- 위 오류는 모두 commit 전 발견·교정됐고 source-screen 수치, OPEN 판정, 사용자 데이터에는
  영향이 없다. `sorry`, `admit`, project-local `axiom`은 사용하지 않았다.
- 예방:
  1. 저자·제목·journal·DOI는 검색 결과 요약이 아니라 PDF 첫 페이지와 기존 source registry를
     함께 대조한 뒤 정본에 넣는다.
  2. in-preparation 공동저자는 저자 개인의 공식 CV나 연구페이지에서 정확히 확인한다.
  3. PowerShell에서는 block pipeline과 현재 working directory를 명령 전에 확인한다.
  4. PDF 변환기의 logging warning과 실제 extraction/render 실패를 exit code·산출물로 구분한다.
  5. 장시간 session을 호출할 때는 output뿐 아니라 session id와 최종 exit code를 보존한다.

### E123 — Theory 75 Lean 공통분모 비교 lemma 선택 오류와 smoothing scope 과장 초안

- 분류:
  <code>PRE_COMMIT_FORMALIZATION_AND_SCOPE_DRAFT_ERRORS /
  DETECTED_AND_CORRECTED / NO_SCIENTIFIC_RESULT_AFFECTED</code>.
- second-moment terminal proof의 마지막 공통분모 비교에 서로 다른 두 양의 분모를 받는
  `div_le_div_iff₀`를 인수 하나로 적용해 첫 direct Lean compile이 실패했다. 같은 분모 전용
  `div_le_div_iff_of_pos_right`로 교정했고, `field_simp` 뒤 실행되지 않던 `ring` tactic도
  제거했다. 재실행은 exit 0·경고 0이다.
- smoothing 초안은 처음에 `[1,2]` 비음수 weight의 실수 Mellin factor만 보고 “fixed
  nonnegative smoothing 실패”라고 넓게 이름 붙였다. 실제 complex zero term에는
  `u^(i*gamma)` 진동이 있으므로, 증거가 지지하는 범위는 zero-height 정보를 쓰지 않는
  gamma-uniform absolute-value envelope다. 함수·machine ledger·Theory 75·review 82를
  `source-blind gamma-uniform` 판정으로 좁히고 height-sensitive smoothing 전체는
  `NOT RULED OUT`으로 보존했다.
- 위 두 오류는 모두 commit 전 발견됐다. 최종 수치 8602.030894..., 필요한 감쇠율,
  `PAP-11`·`X_cert` OPEN 상태와 사용자 데이터에는 영향이 없다. `sorry`, `admit`,
  project-local `axiom`은 사용하지 않았다.
- 예방:
  1. Lean division lemma는 공통분모인지 서로 다른 분모인지 signature를 먼저 확인한다.
  2. Mellin smoothing은 실수부 감쇠와 imaginary-height oscillation을 분리하고,
     uniform supremum·actual zero-height 정보를 명시한다.
  3. necessary condition의 실패를 전체 proof family의 불가능성으로 이름 붙이지 않는다.

## 4. 아직 남은 오류 위험

1. P014 restricted LP의 unbounded seed 원인은 아직 증명되지 않았다.
2. P018 dual partition은 공통 sieve/accumulator kernel 위험을 공유한다.
3. actual peak RAM을 모든 runner가 직접 저장하지는 않는다.
4. 오래된 문서의 “다음 우선순위”는 당시 snapshot이라 현재 정본과 다를 수 있다.
5. `tmp` 안에도 다음 실험 입력과 실제 결과 provenance가 있으므로 경로명만 보고 삭제하면 안 된다.

## 5. 오류 발견 시 행동 규칙

1. 즉시 사용자에게 증상·영향 범위·과학 결과 오염 여부를 분리해 알린다.
2. 실패 run과 원본 log hash를 보존한다.
3. 잘못된 결과가 있으면 `INVALID` 또는 비정본으로 명시하고 조용히 덮어쓰지 않는다.
4. 재시도는 새 revision·새 run ID로 한다.
5. 수정 전후에 negative regression을 추가한다.
6. 원인을 모르면 추정이라고 표시하고, 모르는 상태를 성공 설명으로 바꾸지 않는다.
7. 시간이 짧게 끝났다는 이유로 모든 계획 단계가 충분히 수행됐다고 가정하지 않는다.
8. `TemporaryDirectory` 또는 multiprocessing을 쓰는 suite는 이 저장소에서 이미 sandbox
   권한 실패가 반복됐으므로, 첫 판정 실행부터 허가된 정상 로컬 권한을 우선한다.

## 6. 현재 공개적으로 인정할 미해결 debt

- P014-R3 metadata의 내부 R2 label
- P014 bounded seed 설계의 근거 부족
- P018 actual peak RAM 미기록
- 일부 예전 `temp_work_logs`와 superseded runner의 archive 정책 미확정

이 항목들은 연구 수치의 현재 PASS를 무효화하지 않지만 다음 revision 전에 처리해야 한다.
