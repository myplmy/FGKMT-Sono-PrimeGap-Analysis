# H1b-1b 현대 sieve source·GGPY 오류항 감사 작업원장

- 시작: 2026-09-06 16:20 KST
- 현재 상태: COMPLETE
- 사용자 승인: arXiv:2210.09775와 Lemke Oliver의 BoundedGaps 원문 감사, 관련 자료 취득, H1b-1b 상수 복원 후속 작업, 정본·검증·핸드오프 갱신
- 금지·보류: 실제 maximal-gap/prime sweep, threshold calculator, 장시간 실험, 패키지 설치, Lean 설치, commit/push/PR
- 선행 변경: 시작 시 `git status --short` 출력 0건(깨끗한 작업트리)

## 목적과 완료조건

- 목적: arXiv:2210.09775가 Halberstam–Richert Lemmas 5.3–5.4의 base multiplier와 finite range를 대체 또는 복원할 수 있는지 판정하고, GGPY Lemma 4 오류항에 대한 Lemke Oliver의 지적을 원문 수식으로 검증하여 현재 `C4 <= 2 C3` 계약과 H1b-1b 상태를 정확히 교정한다.
- 완료조건: 두 사용자 지정 원문의 provenance/hash·관련 page/equation 확보, 수학적 영향 판정, 정본 문서/기계 원장/필요 코드와 테스트 갱신, 전체 검증, 다음 작업순서·커밋안·새 handoff 작성.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | 원문의 정확한 가정, kappa 범위, L 의존성, norm과 finite cutoff를 식별하고 조건부 전달과 base constant를 구분한다. |
| 데이터·provenance | MEDIUM | PDF URL, 취득 UTC, SHA-256, page/equation을 기록하고 `tmp/pdfs` 원문을 RETAIN한다. |
| 통계·정밀도 | LOW | actual 통계/prime 계산은 하지 않으며 exact symbolic/rational 검증만 허용한다. |
| 승인 경계 | MEDIUM | 사용자가 source audit·후속 proof work를 승인했으나 package 설치와 actual experiment는 승인하지 않았다. |
| 산출물·비덮어쓰기 | MEDIUM | 새 review/이론 revision을 만들고 기존 actual artifact와 `test_result`는 수정하지 않는다. |

## 단계 현황

1. **COMPLETED — 1차 자료 취득·provenance 고정**
2. **COMPLETED — arXiv:2210.09775의 HR 대체 가능성 감사**
3. **COMPLETED — Lemke Oliver의 GGPY Lemma 4 오류항 감사**
4. **COMPLETED — H1b-1b 수식·상태·정본 교정 및 후속 합성**
5. **COMPLETED — 자동검증·정합성 감사**
6. **COMPLETED — 사용자 보고·권장순서·handoff·원장 완료 처리**

## 단계별 기록

### 2026-09-06 16:20 KST — 작업 재개·승인 경계 고정

- 수행: 최신 handoff와 작업원장 규약을 읽고 시작 작업트리를 확인했다.
- 파일: `handoff/202609060850_HANDOFF.md`, `ai_dev_tool/08_작업원장_작성규약_양식.md`
- 명령·검증: `git status --short`
- 결과: 선행 변경 0건. H1b-1b 정본은 multiplier 89, 조건부 `C4 <= 2 C3`, HR base `C3` source-blocked 상태다.
- 문제·결정: 새 원문의 공식이 같은 hypothesis와 uniformity를 제공하지 않으면 HR을 대체했다고 쓰지 않는다. 오류항 지적이 kappa=1에도 영향을 주는지 별도로 판정한다.
- 다음 재개점: 두 지정 URL의 메타데이터와 원문 PDF를 취득하고 hash를 고정한다.

### 2026-09-06 16:33 KST — 지정 원문·source provenance 고정

- 수행: Kuperberg arXiv v2와 Castillo–Hall–Lemke Oliver–Pollack–Thompson 논문 PDF 및 arXiv source를 비덮어쓰기 취득했다.
- 파일: tmp/pdfs/h1b1b_followup 아래 PDF 2개, source archive 2개와 해제한 TeX.
- 검증: PDF SHA-256은 각각 653dcd731f11c6bab47fa61989b31f50dc3318464fc4d300276698045ba48939, af2f402f1d0ecf67ea2b02a18f9cc2384514cb04fc3467807e20b278e3d463ca이다. source archive SHA-256은 각각 53bc19fdfae8c0a39530dfffdf4c36481e9060bf3c098075805a44f0ce76c620, 62131d8cd8a3c3211e8a3f9f785333408644db40d0a373d1e37f84f3f6675558이다.
- 문제·결정: 취득 과정의 첫 sandbox 네트워크 실패는 승인된 외부 네트워크 재시도로 해결했다. 연구 계산이나 패키지 설치는 수행하지 않았다.

### 2026-09-06 16:33 KST — 현대 HR 재현과 GGPY 오류항 판정

- Kuperberg Lemma 4.3(PDF 17쪽)는 HR Lemma 5.4를 따라 특수한 prime-tuple sieve function에 대해 1/G(z)의 상대오차 O((L+k^4)/log z)를 재현한다. 그러나 B_L, B_k와 O 상수가 모두 암시적이고 일반 Maynard Lemma 8.4의 gamma에 대한 수치적 uniform constant가 아니므로 C3와 finite cutoff를 닫지 못한다.
- Castillo et al. Lemma 2.5와 Remark(PDF 11쪽)는 GGPY Lemma 4 및 Maynard Lemma 8.3에 적힌 c_gamma 곱 오류항이 추가적인 z 대 L 크기조건 없이는 증명되지 않으며, 안전한 오류항에는 c_gamma가 붙지 않는다고 명시한다.
- 영향: Lemma 8.2의 89는 영향 없음. kappa=1 부분적분의 절대오차 전달계수 2도 유지된다. 다만 기존 계약의 C3*c_gamma 정규화는 교정해야 하며, Maynard의 상대오차 형태로 되돌리려면 c_gamma의 명시적 하한 또는 강한 z 대 L 조건과 r회 누적 재증명이 필요하다. 따라서 X_cert는 계속 OPEN이다.
- 다음 재개점: source/h1b1b_multiplier_recovery.py의 계약을 절대오차 기준으로 고치고 상대오차 복원 함수를 별도로 추가한 뒤 negative regression test를 작성한다.

### 2026-09-06 16:49 KST — 코드·기계 원장·정본 교정

- 수행: GGPY3→4 계약을 c_gamma 포함 상대오차에서 corrected absolute error로 바꾸고, 별도 positive c_gamma lower bound가 있을 때만 상대 multiplier 2*C3_abs/c_min을 생성하는 exact rational 함수를 추가했다.
- 문서: 신규 검토보고서 docs/review/27_20260906_H1b1b_Kuperberg_GGPY_error_term_타당성검토.md, theory 18, METHODS, AGENTS, theory index, 상위 theory/review 문서를 동기화했다.
- 기계 원장: H1b-1b schema 1.1.0과 상위 H1b-1/H1b schema 1.1.0에 Kuperberg·Castillo provenance, corrected normalization, 신규 proof obligation을 기록했다. H1B1-L83-GGPY3는 SOURCE_ACCESS_BLOCKED에서 RATE_MISSING으로 재분류했지만 parent package·SIV-07·X_cert는 승격하지 않았다.
- 오류 기록: 과거 c_gamma 계약 오류를 E022로 공개 기록했다. 문서 patch 중 JavaScript wrapper backtick parse가 두 번 재발했으나 두 번 모두 apply_patch 호출 전이어서 파일 변경 0건이며, 자리표시자 방식으로 정상 재적용했다.
- 검증: 고정 FGKMT Python py_compile PASS, targeted 17/17 tests PASS.
- 다음 재개점: stale 문구·JSON validity·참조 경로·전체 unittest·git diff를 감사한다.

### 2026-09-06 17:00 KST — H1b-1b-2 후속 원장과 전체 검증 완료

- 수행: corrected absolute error에서 Maynard식 상대오차를 복구하기 위한 독립 proof obligation 9개를 신규 이론 원장과 JSON 원장에 등록했다.
- 파일: `docs/method/theory/19_Sono_FMT_H1b1b2_cgamma_error_normalization_ledger.md`, `docs/method/theory/data/Sono_FMT_H1b1b2_cgamma_error_normalization_v1.json`, `tests/test_h1b1b2_cgamma_error_ledger.py`.
- 판정: `c_gamma`의 uniform positive lower bound 또는 명시적인 `z` 대 `L` 조건 어느 경로도 아직 닫히지 않았다. `route_selected=false`, `SIV-07=OPEN`, `X_cert=OPEN`을 유지했다.
- 검증: 신규 원장 단위시험 5/5 PASS. 고정 FGKMT Python 전체 suite는 `Ran 251 tests in 32.106s`, `OK`, failure 0, error 0, skipped 0이다.
- 정합성: JSON 6/6 parse PASS, 필수 경로 4/4 PASS, 신규 문서 local link 4건 PASS, ASCII control character 0건, `git diff --check` PASS(줄끝 변환 경고만 존재).
- 실행 경계: actual prime/maximal-gap 계산, threshold calculator, 패키지·Lean 설치는 수행하지 않았다. 이번 변경은 문헌·증명 의존성 감사와 로컬 정적·단위 검증에 한정된다.

### 2026-09-06 17:00 KST — 사용자 인계 준비 완료

- 수행: 결과 요약, 다음 권장 순서, 사용자 실행 절차, 선택적 자료 요청, 한국어 커밋 메시지안을 새 핸드오프에 기록했다.
- 파일: `handoff/202609061700_HANDOFF.md`.
- 결과 색인: actual 실행과 `test_result` 산출물이 없으므로 실험결과 색인은 변경하지 않았다.
- 시각 QA: 새 figure를 생성하지 않아 시각 QA 대상이 없다.
- 다음 재개점: H1b-1b-2의 local-factor/c_gamma 하한 경로를 먼저 감사한다.

## 현재 재개점

본 작업은 완료됐다. 다음 작업은 `handoff/202609061700_HANDOFF.md`의 1순위인 H1b-1b-2 local-factor 감사에서 시작한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
