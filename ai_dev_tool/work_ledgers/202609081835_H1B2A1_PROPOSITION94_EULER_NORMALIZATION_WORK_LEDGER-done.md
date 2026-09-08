# H1b-2a.1 Proposition 9.4 Euler normalization 작업원장

- 작업 시작: 2026-09-08 18:35 KST
- 승인 범위: Maynard Proposition 9.4 식 (9.66)에 표시되고 (9.67)에서 흡수되는
  `O(k)` 이전 exact Euler 인자 복원과 유한 비교 감사
- 승인 밖: 실제 소수 탐색, P018-B 실행, numerical threshold calculator, 패키지 설치, commit/push/PR
- 정확한 재개점: 아래 첫 `IN_PROGRESS` 단계

## 영향 분석

| 영역 | 영향 | 통제 방법 |
|---|---|---|
| 수학 정의·증명 | 높음 | 원문 식과 변수 정규화를 먼저 고정하고 primewise exact identity를 별도 검증한다. |
| 데이터·실험 산출물 | 없음 | actual dataset과 `test_result/`를 읽거나 생성하지 않는다. |
| 수치 검증 | 중간 | exact integer/rational arithmetic과 고정 FGKMT Python 환경만 사용한다. |
| 승인 경계 | 높음 | 이론·문헌·toy 검증에 한정하고 threshold 계산을 시작하지 않는다. |
| 정본 문서 정합성 | 높음 | 자식 node, 부모 H1b-2a/H1b/T1 상태, theory index와 handoff를 함께 감사한다. |

## 단계

### 1. 원문 호출부·정의·영향 범위 감사 — COMPLETE

- [x] Proposition 9.4 및 식 (9.63)--(9.70)의 원문과 저자 TeX를 대조했다.
- [x] `omega`, `omega*`, singular series, `W`, `B`, `Delta_L`, `W_0` 정의를 역추적했다.
- [x] 최종 출판본 인쇄면 pp.1547--1550을 렌더링해 시각적으로 확인했다.
- 증거: 식 (9.61)의 exact denominator는
  `g_*(p,m)=(p-m)^2/(p+m-2)`이고, 식 (9.66)의 두 곱이 (9.67)에서 각각
  `O(1)`과 `O(S_{WB}(L)^(-1))`로 흡수된다. 기존 문서의 “식 (9.67)의 두 곱”은
  위치를 가리키는 축약 표현이며, 정확한 displayed 위치는 (9.66)이다.

### 2. 선행·교정·후속 증명 조사 — COMPLETE

- [x] Cambridge 최종 출판본, arXiv:1405.2593 v2/저자 TeX, 동일 weight를 사용하는
  Mastrostefano arXiv:1804.06290을 표적 검색했다.
- [x] arXiv v2는 “clarified some statements”라고만 기록하며, 해당 Euler 곱의 explicit
  replacement나 공식 erratum은 확인되지 않았다.
- [x] 후속 논문은 같은 weight를 쓰지만 Proposition 9.4의 `omega*` 곱을 재수치화하지 않는다.
- 한계: 이는 확인한 공식·관련 1차 자료 범위의 결과이며 전 세계 비존재·novelty 주장이 아니다.

### 3. exact local-factor 복원과 finite tail 증명 — COMPLETE

- [x] 식 (9.66)의 두 product를 `1+O(k)/p^2`로 축약하기 전 정확한 인자로 복원했다.
- [x] singular-series 인자와의 primewise 관계를 exact algebra로 확인했다.
- [x] `p>2k^2` tail을 초등적인 `sum p^(-2) <= 1/(2k^2)`로 닫았다.
- 결과: 마지막 두 곱은 `exp(2+2/k) S_WB(L)^(-1)` 이하이고, 식 (9.64)의
  앞쪽 곱이 제곱되는 것까지 포함한 전체 Euler multiplier는
  `exp(2+6/k) S_WB(L)^(-1)` 이하이다. `k=36`에서 설명용 근삿값은
  `8.729138363720132`이다.
- 상태: 자식 `H1B2A-P94-FINAL-EULER`만 `PROJECT_FINITE_COMPONENT_CLOSED`로
  이동한다. 식 (9.52)의 distribution error 때문에 부모 `H1B-P94=RATE_MISSING`,
  `SIV-07/09=HARD_BLOCKER`, `X_cert=OPEN`은 유지한다.

### 4. 기계검증 계약·코드·문서 정합성 — COMPLETE

- [x] 재현 가능한 JSON 계약, exact verifier와 단위시험을 작성했다.
- [x] H1b-2a, H1b, H1, T1, METHODS, 이론 색인과 AGENTS 정본을 동기화했다.
- [x] `SIV-07`, `SIV-09`, `X_cert`를 각각 `HARD_BLOCKER`, `HARD_BLOCKER`,
  `OPEN`으로 유지했다.
- [x] canonical 계약 3개의 schema version과 fail-closed 회귀시험을 갱신했다.

### 5. 전체 검증·핸드오프·완료 처리 — COMPLETE

- [x] 고정 Python으로 compile, targeted/full unittest, JSON parse를 수행했다.
- [x] 링크·제어문자·`git diff --check`를 점검했다.
- [x] `handoff/202609081917_HANDOFF.md`에 쉬운 설명, 다음 순서, 사용자 절차와
  한국어 커밋 제안을 기록했다.
- [x] 모든 산출물·정본 동기화와 최종 검증을 마쳤다. 다음 동작은 이 원장의 안전한
  `-done` 이름 변경이다.

## 실패·결정 기록

- MiKTeX `pdftotext`가 사용자 로그 경로 접근 거부로 실패했다. PDF 자체 오류가 아니며,
  Codex bundled Poppler `pdftoppm`으로 pp.1546--1550을 렌더링해 시각 확인했다.
- PowerShell에서 `rg docs/**/*.md`식 glob 전달이 Windows 경로 규칙으로 실패해 디렉터리
  인수를 직접 지정하는 방식으로 전환했다. 연구 산출물에는 영향이 없다.
- 첫 전체 unittest는 sandbox가 저장소와 Windows temp 아래 시험용 디렉터리 생성을
  거부해 82건의 `PermissionError`로 실패했다. 동일 명령을 허가된 sandbox 외부에서
  재실행해 321건 전부 PASS했다. 코드 실패로 판정하지 않는다.
- 첫 Markdown-link 점검은 Git의 quoted UTF-8 경로를 그대로 받아 한글 파일 3개를
  읽지 못했는데도 마지막 PASS를 출력하는 검사기 자체 결함이 있었다. 결과를 채택하지
  않고 `git -c core.quotepath=false`와 missing-file fail-closed 검사를 추가해 다시
  실행했고, 변경 Markdown 12개 전부 PASS했다.

## 변경 파일

- `ai_dev_tool/work_ledgers/202609081835_H1B2A1_PROPOSITION94_EULER_NORMALIZATION_WORK_LEDGER.md` (신규)
- `tmp/pdfs/h1b2a/render_h1b2a1/page-31.png`--`page-35.png` (PDF 시각감사용 임시 렌더)
- `source/h1b2a1_proposition94_euler.py` (신규 exact verifier)
- `tests/test_h1b2a1_proposition94_euler.py` (신규 exhaustive toy-grid 시험)
- `docs/method/theory/data/Sono_FMT_H1b2a1_Proposition94_Euler_normalization_v1.json` (신규 계약)
- `docs/method/theory/29_Sono_FMT_H1b2a1_Proposition94_exact_Euler_normalization.md` (신규 정본)
- `docs/review/35_20260908_H1b2a1_Proposition94_Euler_타당성검토.md` (신규 비판적 검토)
- `source/h1b2a_residual_moment_package.py`와 대응 시험·계약 (상위 child 상태 동기화)
- `handoff/202609081917_HANDOFF.md` (신규 세션 핸드오프)

## 검증 기록

- Maynard 최종 PDF pp.1547--1550과 author TeX lines 1044--1168 식·정의 일치 확인.
- 공식 arXiv version history와 관련 후속 1차 논문 표적 검색 완료.
- 고정 FGKMT Python으로 신규 시험 8건 PASS, 상위 H1b-2a 시험과 합친 14건 PASS.
- 새 verifier·직접 부모·H1b/H1/T1 정본을 합친 targeted 시험 33건 PASS.
- 관련 py_compile PASS.
- 첫 sandbox 전체 suite: 321건 중 82건 환경 `PermissionError`; 무효 판정.
- 동일 sandbox 외부 전체 suite: `Ran 321 tests in 35.471s / OK`.
- 갱신 JSON 5개 PowerShell strict parse PASS.
- 변경 Markdown 12개 상대 링크 검사 PASS.
- 금지 control character 0건, `git diff --check` whitespace error 0건.
