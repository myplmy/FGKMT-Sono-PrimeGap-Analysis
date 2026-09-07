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

### E020 — H1b-1a 작업원장 중간 기록에 아직 오지 않은 시각을 기입

- 분류: `METADATA_DEBT / CORRECTED_BEFORE_ACTUAL`
- 문제: 2026-09-04 작업원장 두 단계의 시각을 실제 현재시각보다 뒤인 22:05, 22:31 KST로
  잘못 적었다.
- 영향: 수학 문서·코드·검증값에는 영향이 없고, 완료 전 작업 이력의 시각 metadata만 잘못됐다.
- 교정: 시스템 `Get-Date`가 21:45 KST임을 확인한 뒤 두 항목을 “21:45 KST 기록”으로
  고치고, 이는 앞서 끝난 단계를 사후 기록한 시각임을 명시했다.
- 재발 방지: 작업원장 timestamp는 문맥에서 추정하지 않고 기록 직전 시스템 시각을 조회한다.

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
