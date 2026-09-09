# FGKMT-Sono ChatGPT 오류·실수·환각 원장

최종 갱신: 2026-09-06 KST

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
