# Sono/FMT H1b·미검증 신규 소수간격 논문 검토 작업원장

- 시작: 2026-09-04 13:29 KST
- 현재 상태: COMPLETE
- 사용자 승인: H1b Maynard Proposition 6.1 constant ledger 작성, `article/unverified`의 신규 PDF 2편 비판적 분석, PrimeGaps186 공개 코드 참고, 연결 정본·핸드오프 갱신
- 금지·보류: 두 논문의 peer review 통과 또는 정리 진실성 확정 주장, 미검증 결과의 canonical theorem 승격, 새 prime sweep·actual experiment, 외부 저장소 clone/설치, threshold calculator, commit/push/PR
- 선행 변경: 시작 시 `git status --short` 출력 없음(clean). `article/unverified` PDF 2편은 사용자 제공 원본으로 수정하지 않는다.

## 목적과 완료조건

- 목적:
  1. Maynard Proposition 6.1과 Sections 8–9의 상수·cutoff·Hypothesis 1 의존성을 행 단위로 추적해 H1b의 실제 닫힘 가능성과 다음 blocker를 판정한다.
  2. 신규 미검증 논문 2편의 주장·증명 구조·계산/코드 의존성·우리 연구 재사용 가능성을 원문 기준으로 분석한다.
  3. 미동료심사 자료를 아이디어·검증후보로만 격리하고 기존 FGKMT/Sono 정본과 혼합하지 않는다.
- 완료조건:
  - PDF 전체 페이지·metadata·SHA-256과 온라인 provenance를 확인한다.
  - H1b machine-readable ledger와 비전문가용 해설을 작성하고 fail-closed 검증을 통과한다.
  - 논문별 review 2개 및 종합 corpus 상태를 갱신한다.
  - PrimeGaps186 공개 코드를 가능한 범위에서 source-level로 확인하고, local clone이 꼭 필요할 때만 사용자에게 요청한다.
  - METHODS/AGENTS/이론 색인·handoff를 동기화하고 실제 미실행 경계를 남긴다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | H1b는 good-weight moment의 정량 의존성만 추적; H1a·FGKMT scale 불변 | 숨은 `O/o/ll` 상수를 숫자로 추측하지 않음 |
| 데이터·provenance | 사용자 제공 미검증 PDF와 공개 저장소만 추가 | PDF hash·출처·version을 기록하고 canonical 9편 corpus와 분리 |
| 통계·정밀도 | 신규 논문 계산 주장은 재현 전 미검증 | 논문 주장, 코드 존재, 독립 검증을 서로 분리 |
| 승인 경계 | 문헌·정적 코드 검토와 toy validation 승인 | clone·dependency 설치·actual 계산은 별도 필요 시 요청 |
| 산출물·비덮어쓰기 | 신규 H1b/논문 review와 연결 정본만 변경 | 원본 PDF·기존 actual artifact 불변 |

## 단계 현황

1. **COMPLETED — 입력 PDF·Maynard/H1 기존 정본·온라인 provenance 고정**
2. **COMPLETED — H1b Proposition 6.1 lemma별 constant ledger 작성**
3. **COMPLETED — 미검증 논문 2편과 PrimeGaps186 코드 비판적 분석**
4. **COMPLETED — fail-closed 검증·정본·종합 review 동기화**
5. **COMPLETED — 권장 순서·사용자 요청·commit 제안·handoff·완료 처리**

## 단계별 기록

### 2026-09-04 13:29 KST — 착수·승인 경계 고정

- 수행: 최신 handoff, 작업원장 규약, 관련 스킬, clean worktree와 사용자 제공 PDF 2편의 존재를 확인했다.
- 파일: 이 작업원장 신규 작성.
- 결과: H1b와 미검증 논문 review는 승인됨. actual 계산·외부 clone은 승인 범위에 포함하지 않는다.
- 문제·결정: `docs/review`만 문헌 리뷰 정본으로 사용하며, 두 논문은 peer-reviewed corpus 수에 합산하지 않고 `UNVERIFIED PREPRINT`로 표시한다.
- 다음 재개점: PDF 페이지 수·metadata·full text·hash와 arXiv/저자/GitHub provenance를 고정한다.

### 2026-09-04 — provenance·원문 감사 완료

- PDF: Stadlmann 34쪽, SHA-256 `4296e63a...e81ee994`; OpenAI 39쪽,
  SHA-256 `456f05e...88b0930`.
- 원문 확인: 두 PDF 전체 text extraction과 대표 페이지 렌더링을 대조했다. bundled Poppler에서
  예상 `pdftotext.exe`가 없어 두 번 실패했으나, pypdf fallback으로 전체 추출에 성공했다.
- 온라인 provenance: Stadlmann arXiv:2608.31126v1; PrimeGaps186 HEAD
  `61340d0b74163003b32756bb16e91d9209a5e330`을 읽기 전용으로 고정했다.
- Maynard: peer-reviewed Compositio 2016 원문의 Hypothesis 1, Proposition 6.1, Sections 8–9를
  감사해 17개 constant obligation을 확정했다.

### 2026-09-04 — H1b와 논문별 검토 문서 작성 완료

- 신규 H1b 정본·contract·시험:
  - `docs/method/theory/14_Sono_FMT_H1b_Maynard_Proposition_6_1_constant_ledger.md`
  - `docs/method/theory/data/Sono_FMT_H1b_Maynard_Proposition_6_1_constants_v1.json`
  - `tests/test_h1b_maynard_constant_ledger.py`
- 신규 미검증 논문 review:
  - `docs/review/25_20260904_Stadlmann_Bounded_Gaps_240_unverified.md`
  - `docs/review/26_20260904_OpenAI_Improved_Short_Gaps_186_unverified.md`
- 판정: H1b는 dependency inventory 완료지만 `SIV-07/09`, full good weight와 `X_cert`는 OPEN.
  Stadlmann 240과 OpenAI 186은 모두 현재 프로젝트 theorem input으로 채택하지 않는다.
- PrimeGaps186: conditional Lean의 project axiom 3개와 numerical certificate 범위를 구분했다.
  1차 검토에는 local clone이 필요하지 않아 사용자 다운로드를 요청하지 않는다.

### 2026-09-04 — 정본 동기화·검증 완료

- 동기화: `AGENTS.md`, `docs/METHODS.md`, 이론 색인, T1/H1 machine ledger와 human review,
  9편 종합 문헌 review에 H1b와 별도 미검증 후보 2편의 상태를 반영했다.
- 표적 검증: H1b/H1/T1 16/16 PASS.
- 구조 검증: JSON parse PASS, control character 0, 상대 Markdown link 누락 0,
  `git diff --check` whitespace error 0(기존 CRLF 안내만 존재).
- 전체 검증 1차: 222건 중 82건이 sandbox 임시폴더 `PermissionError`; 코드 실패로 판정하지 않음.
- 동일 명령 sandbox 외부 재실행: 222/222 PASS, 32.236초.
- actual prime 실험·threshold 계산·PrimeGaps186 certificate 실행은 하지 않았다.

### 2026-09-04 13:52 KST — 핸드오프·완료 처리

- 신규 handoff: `handoff/202609041352_HANDOFF.md`.
- 권장 순서: H1b-1 기본 summation 상수 → H1c Hypothesis 1/PAP → H1b-2 moment 합성;
  PrimeGaps186 독립 재현은 별도 보조축으로 분리했다.
- 사용자 현재 실행 명령: 없음. 별도 승인 전 PrimeGaps186 clone/install/run과 actual prime 실험은 금지.
- 최종 감사: 금지된 4글자 프로젝트명 오타 0, PDF hash 2/2 일치, 상대 링크 누락 0,
  control character 0, handoff 존재 확인, `git diff --check` error 0.

## 현재 재개점

완료. 다음 작업은 최신 handoff와 이 `-done` 원장에서 재개한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 peer review/독립 검증 상태 분리
- [x] review 종합·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
