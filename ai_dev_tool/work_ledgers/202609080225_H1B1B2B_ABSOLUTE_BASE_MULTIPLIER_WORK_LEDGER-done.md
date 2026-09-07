# H1b-1b-2b absolute base multiplier·finite range 복원 작업원장

- 시작: 2026-09-08 02:25 KST
- 현재 상태: COMPLETED
- 사용자 승인: 권장 1순위 H1b-1b-2b 착수, 필요한 학술자료 취득, 선행증명 우선 조사 후 필요 최소 범위 직접증명
- 금지·보류: actual prime sweep, threshold calculator, 장시간 수치실험, 암시적 O-상수 임의 대입, 패키지·Lean 설치, commit/push/PR
- 시작 상태: 활성 비-done 작업원장 0개, `git status --short` 0건

## 목적과 완료조건

Maynard Lemma 8.3의 교정된 절대오차

\[
|E_3(u)|\le C_{3,\mathrm{abs}}(A_1,A_2)(L+1)
\]

에 대해 기존 문헌이 실제로 수치 multiplier와 finite range를 제공하는지 먼저 조사한다.
정확히 맞는 결과가 없으면 기존 proof를 source 단위로 분해해 필요한 최소 범위만 직접
명시화하고, 닫힌 상수와 남은 blocker를 구분한다.

완료조건은 source/provenance 표, 적용가능성 매트릭스, 상수 의존성 DAG,
가능하면 explicit 상수·범위 정리와 기계 계약·회귀시험, 상위 정본 동기화,
전체 검증, 새 timestamp handoff다. 같은 가정의 수치 정리가 없으면
그 사실과 정확한 직접증명 재개점을 결과로 남기며 임의 상수를 만들지 않는다.

## 문헌 우선 전략의 비판적 판정

| 제안 요소 | 판정 | 적용 방식 |
|---|---|---|
| 이미 증명된 lemma를 먼저 찾기 | 타당 | 중복 증명을 줄이고 검증 가능한 source chain을 확보한다. |
| 제목·형태가 비슷하면 채택 | 부적합 | 가정, 정규화, uniformity, finite cutoff, 변수 대응을 모두 대조해야 한다. |
| 적합한 선행 정리가 없을 때 직접 증명 | 타당 | 전체 이론이 아니라 현재 obligation을 닫는 최소 범위만 명시화한다. |
| 비명시적 O를 경험적 fitting으로 대체 | 부적합 | theorem certificate에는 사용할 수 없으며 blocker로 유지한다. |
| 여러 source의 부분 결과를 합성 | 조건부 타당 | 각 전달 lemma와 상수·범위를 별도 증명하고 provenance를 유지한다. |

따라서 작업 순서는 `정확한 목표식 고정 → 문헌 탐색 → 적용가능성 감사 → 부족분만
직접증명 → exact 회귀검사`로 한다.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log/end-bounded empirical 정의 | 영향 없음 | maximal-gap 데이터와 F/H/envelope를 읽거나 재계산하지 않는다. |
| Sono/FMT proof chain | HIGH | `C3_abs`, finite range, 실제 입력과 r-fold를 분리하고 child만 근거가 있을 때 승격한다. |
| source provenance | HIGH | DOI/arXiv, 버전, 취득 UTC, local SHA-256, 정확한 lemma/page/line을 고정한다. |
| 수치 정확성 | HIGH | exact integer/rational 또는 directed high precision만 진단에 사용한다. |
| 승인 경계 | MEDIUM | 문헌·정리·toy/exact test만 수행하며 actual 실험은 하지 않는다. |
| 재현성 | HIGH | 기계 원장과 negative regression으로 숫자 없는 O·범위 누락을 거부한다. |
| 문서 파급 | HIGH | theory 18--21, H1b/H1/T1, METHODS, AGENTS, handoff 상태를 점검한다. |

## 단계 현황

1. COMPLETED — 목표 lemma·기존 local source와 상수 의존성 고정
2. COMPLETED — 선행연구·원문 source 탐색과 적용가능성 감사
3. COMPLETED — 부족분의 최소 직접증명과 남은 blocker 정식화
4. COMPLETED — 정본·기계 계약·코드·negative regression 갱신
5. COMPLETED — 표적·전체 검증, handoff, 원장 완료 처리

## 단계별 기록

### 2026-09-08 02:25 KST — 착수·방법론·영향도 고정

- 최신 handoff의 첫 미완료 gate가 H1b-1b-2b임을 확인했다.
- 선행 상태는 `C4_abs<=2C3_abs`, actual-call `c_gamma` lower-bound route와
  11개 application 제외모듈 상계가 닫혔지만 `C3_abs`, finite range,
  실제 `A1,A2,L`, corrected r-fold는 OPEN이다.
- Kuperberg는 HR 구조를 재현하지만 숫자·범위·일반 Maynard gamma 특수화가 없어
  그 자체로 certificate가 되지 않는다는 기존 판정을 유지한 채 재검토한다.
- 다음 재개점: Maynard Lemma 8.3, GGPY Lemma 3, Castillo Lemma 2.5,
  Kuperberg/HR 대응 proof를 식·가정·상수 의존성 단위로 나란히 추출한다.

### 2026-09-08 — 문헌 우선 조사·Ford 교정 정리 발견

- Kevin Ford, *Sieve Methods Lecture Notes, Spring 2023*, Theorem 4.4와 식
  (4.8)--(4.15)를 검토했다. 이 정리는 GGPY/Maynard 계열 proof에서 빠진
  `c_gamma*(L+1)^kappa` 항을 보존하며, HR p.146의 역수 전개 오류까지 지적한다.
- 현재 적용은 `kappa=1`이므로 교정된 두 오류항은 모두 `c_gamma*(L+1)` 크기다.
  따라서 legacy `C3_abs / c_gamma-lower-bound` 경로보다 직접적인 상대오차 경로가 있다.
- Ford 자료는 저자 강의노트이고 숨은 `O_{kappa,A1,A2}` 상수는 숫자가 아니다.
  따라서 구조만 채택하고 필요한 `kappa=1` 유한 상수는 프로젝트 정리로 다시 전개했다.
- Ford PDF: `tmp/pdfs/h1b1b2b/Ford_Sieve_Methods_Lecture_Notes_2023.pdf`,
  SHA-256 `a6e8462f1e76606614e5c2891b419515be408d5f11f0b82915f5c24e05c00e06`.
- Dusart PDF: `tmp/pdfs/h1b1a/Dusart2010_Explicit_estimates_over_primes.pdf`,
  SHA-256 `3f11eca84613ad00e6a447f99b318d5c3d76e360283efcc6d3eebdda25ff3923`.
- 표적 검토의 범위에서는 동일 가정·동일 norm·수치 multiplier를 그대로 주는 선행 정리를
  찾지 못했다. 이는 전 세계 문헌의 부재 또는 novelty 주장이 아니다.

### 2026-09-08 — 최소 직접 정식화·기계 계약

- `0<a<=1`, prime-sum upper discrepancy `A2>0`에서 다음을 정식화했다.
  - `D=4+A2+(A2/a)*(1+100*A2/69)+2*(1-a)^2/a`
  - `C_sum=40960*D*exp(256+A2)`
  - `C_L83=2*(C_sum+2)`
- 모든 실수 `x>=2`의 summatory bound와 모든 `z>=2`의 weighted Lemma 8.3 bound를
  얻었다. 전개를 다시 감사하면서 중간 tail 상계를 81/165에서 보수적인 130/256으로
  올려, 작은 `x`와 endpoint를 빠짐없이 덮었다.
- 새 정본·계약·구현·시험:
  - `docs/method/theory/22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md`
  - `docs/review/28_20260908_H1b1b2b_Ford_Wirsing_선행증명_적용성검토.md`
  - `docs/method/theory/data/Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier_v1.json`
  - `source/h1b1b2b_corrected_wirsing.py`
  - `tests/test_h1b1b2b_corrected_wirsing.py`
- 실제 공통 `a,A2,L`, corrected `r`-fold 합성, 다른 H1b/H1c root는 열어 두었다.
  `SIV-07=HARD_BLOCKER`, `X_cert=OPEN`, actual threshold 미계산 상태를 유지했다.

### 2026-09-08 — 정본 동기화·표적 회귀

- H1b-1/H1b/H1/T1/METHODS/AGENTS와 H1b-1b-2(a/a.1) 정본을 새 primary route에
  맞췄다. 기존 `C3_abs`와 `c_gamma` 하한은 삭제하지 않고 optional cross-check로 보존했다.
- 옛 문서의 당시 상태표가 최신 판정으로 오해되지 않도록 현재 열과 설명을 갱신했다.
- FGKMT Python 표적 회귀 54건이 모두 통과했다.
- 작업 중 발생한 실패와 처리:
  1. 첫 Ford PDF 다운로드에서 현재 PowerShell의 `New-Item -LiteralPath` 비지원으로 실패;
     파일 미생성 확인 후 `-Path`로 재시도해 성공했다.
  2. 최초 새 계약 시험이 잘못 옮긴 Dusart SHA를 거부했다; 원본 hash로 교정 후 통과했다.
  3. 한 `apply_patch` 호출에서 동일 파일의 중복 update section 때문에 전체가 미적용됐다;
     파일별 단일 section으로 재시도했다.
  4. 정확한 context가 달라 두 번의 patch가 미적용됐고, 작은 patch로 재시도했다.
  5. 옛 `tmp` 전체 탐색에서 보호된 임시 디렉터리 access-denied가 있었으나 표적 source
     목록은 확인됐고 파일·프로세스 변경은 없었다.
  6. Windows MiKTeX `pdftotext`는 로그 파일 쓰기 권한 진단을 내고 종료코드가 실패였지만
     요청한 47--52쪽 text는 출력했다. 기존 page render 시각검사와 원문 hash 검증을
     함께 사용했으며 이 실패를 PDF 검증 PASS로 세지 않는다.
  7. 옛 회귀시험 15건이 새 schema/status를 거부했고, 계약 자체가 아니라 시험 기대값이
     옛 상태였음을 확인해 갱신했다. 이후 한 문자열 범위 표현 차이도 fail-closed로 잡혀
     `every real z>=2`에 맞춘 뒤 최종 54건 PASS다.
  8. 여러 문서를 한 번에 갱신한 patch가 METHODS의 exact context 불일치로 전체 미적용됐다;
     작은 patch로 분리해 성공했다.

### 2026-09-08 03:45 KST — 전체 검증·핸드오프 완료

- 새 module/test `py_compile`: PASS.
- theory JSON 12개를 FGKMT Python `json.loads`로 엄격 파싱: PASS.
- H1b 표적 회귀: 54/54 PASS.
- 전체 회귀: 샌드박스 내부 첫 실행은 TemporaryDirectory 권한 거부로 82 ERROR였으며
  코드 판정에서 제외했다. 사용자가 허가한 샌드박스 외부 동일 명령은
  `Ran 271 tests in 35.612s — OK`.
- 새 H1b-1b-2b ledger link 8개 존재, UTF-8/제어문자 213파일 PASS,
  `git diff --check` exit 0.
- 현재 변경 파일 35개만 별도로 확대한 UTF-8/제어문자 검사도 PASS다. 전체 과거 handoff
  스캔에서 이번 변경과 무관한 `handoff/202609021757_HANDOFF.md` 150행의 기존 수직탭
  1개를 발견했으나, 이력 문서는 사용자 승인 없이 수정하지 않았다.
- 보조 검사 실패 추가 기록:
  - PowerShell JSON 파서는 대소문자 키 충돌을 비종료 오류로 내면서 PASS 문자열도 출력해
    해당 결과를 폐기하고 Python 엄격 파서로 대체했다.
  - 첫 제어문자 one-liner가 escape 오류로 정상 LF를 잘못 검출해 폐기하고 codepoint
    9/10/13 허용 검사로 다시 통과시켰다.
- 오류 원장 E025--E026에 수학 초안의 tail 상수 보정과 검증기 결함을 기록했다.
- 새 핸드오프: `handoff/202609080345_HANDOFF.md`.
- actual prime sweep, threshold calculator, commit/push/PR은 수행하지 않았다.

## 현재 재개점

완료. 다음 gate는 H1b-1b-2c actual-call 공통 `a,A2,L` 인증이다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 문헌 우선 전략의 적용가능성 매트릭스 완료
- [x] source locator·hash·변수 대응 고정
- [x] 닫힌 상수와 RATE/RANGE blocker 분리
- [x] actual 실험·threshold 미실행 경계 명시
- [x] 정본·상위 원장·AGENTS/METHODS 동기화
- [x] 고정 FGKMT Python 표적·전체 검증
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
