# DEP-R09 JL7-LEMMA3 absolute-sum source 감사 작업원장

- 시작: 2026-09-13 17:01 KST
- 현재 상태: COMPLETE
- 사용자 승인: `X_cert` 계산기 전 source-first 정규화·증명, 필요한 Lean 형식화·검증,
  문서·코드·테스트·새 핸드오프 작성과 단계별 로컬 커밋
- 금지·보류: 실제 prime sweep, threshold calculator, 장시간 계산, 패키지 설치,
  외부 게시·push·PR, `sorry`·`admit`·project-local `axiom`
- 선행 변경: 시작 commit `4d4eafd430c3fc5768189917218ab26678fdcfb1`이며
  `git status --short` 출력 0행으로 clean. 이번 작업 시작 전 비소유 변경 없음.

## 목적과 완료조건

- 목적: Jutila Lemma 7에서 사용되는 “by Lemma 3” absolute sum을 원문 statement와
  proof에 맞춰 actual `(r,r',d)` 범위에 특수화하고, 숨은 multiplier와 endpoint를
  수치화할 수 있는지 fail-closed로 판정한다.
- 완료조건:
  1. Jutila Lemma 3의 정확한 원문 수식·가정·proof dependency를 페이지와 함께 고정한다.
  2. 선행 정리의 적용 가능성을 먼저 확인하고, 부족할 때만 직접 유한 대수 증명을 만든다.
  3. actual JL7 합의 인덱스 범위와 계수를 빠짐없이 복원한다.
  4. 가능한 상수는 Python exact/high-precision evaluator와 toy/unit test로 독립 검증한다.
  5. dependency-critical 유한 대수는 필요 시 단일 Lean 파일에 proof escape 없이 추가한다.
  6. theory/review/data 정본과 상위 ledger·METHODS·AGENTS·색인·handoff를 동기화한다.
  7. 전체 검증 후 원장을 `-done`으로 바꾸고 승인된 로컬 커밋을 만든다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | contour 뒤 absolute-sum 상수만 다룸 | `JL7-CONT`와 Lemma 3·residue·absorption을 혼합하지 않음 |
| 데이터·provenance | 논문 원문과 현재 정본만 사용 | PDF hash·페이지·텍스트/OCR 방식을 기록하고 원문과 대조 |
| 통계·정밀도 | 통계 실험 아님 | 정수·유리수 우선, 초월함수는 고정 precision과 보수적 상계 병기 |
| 승인 경계 | 문헌·증명·toy 검증·로컬 커밋 승인 | 장시간 연산 필요 시 실행하지 않고 사용자에게 요청 |
| Lean 증거 | 유한 대수만 kernel 검증 가능 | source analytic theorem은 별도 상태, proof escape 금지 |
| 산출물·비덮어쓰기 | 새 theory/review/data/handoff | 기존 handoff·완료 원장 덮어쓰기 금지 |

## 단계 현황

1. **COMPLETE — 원문·현재 의존식 inventory**
2. **COMPLETE — source theorem 적용성 및 actual absolute sum 복원**
3. **COMPLETE — 수치 상수 evaluator·unit test와 비판적 판정**
4. **COMPLETE — 필요한 Lean 형식화와 전수 원장 갱신**
5. **COMPLETE — 정본 동기화·전체 검증·handoff·로컬 커밋**

## 단계별 기록

### 2026-09-13 17:01 KST — 착수와 승인 경계 고정

- 수행: 최신 handoff와 `JL7-LEMMA3` 참조를 검색하고, 이전 `JL7-CONT` commit과
  clean worktree를 확인했다.
- 파일: 이 작업원장 신설.
- 명령·검증: `git status --short`; handoff·theory·review의 `JL7-LEMMA3` `rg` 검색.
- 결과: 다음 authoritative gate가 `JL7-LEMMA3`임을 재확인했다.
- 문제·결정: 아직 Lemma 3의 정확한 수식과 actual 합을 복원하지 않았으므로 어떤
  multiplier도 주장하지 않는다.
- 다음 재개점: 최신 handoff, Theory 60·65·66·67 및 Jutila printed pp.48--53에서
  Lemma 3 statement와 Lemma 7의 호출 위치를 나란히 추출한다.

### 2026-09-13 17:08 KST — 원문 statement와 선행 source 판정

- 수행: Jutila printed pp.48--49의 Lemmas 2--3과 p.53의 Lemma 7 호출을 OCR locator 뒤
  렌더링 원페이지로 직접 대조했다. Motohashi 1975 공식 J-STAGE 3쪽 발표문도 확보해
  native text와 rendered p.816을 대조했다.
- source 증거:
  - Jutila Lemma 2는 `gcd(r,r')` 안팎의 두 local Euler factor로 `h(d;r,r')`를 정의한다.
  - Lemma 3은 `f(n)=mu(n)phi(n)`에서 `sum h(d)/d=delta_(r,r') phi(r)`와
    `sum |h(d)| <= product_(p|r)(p+1) product_(p|r')(p+1)`을 명시한다.
  - p.53의 off-diagonal 호출은 정확히 `(rr')^-1 sum_d |h(d;r,r')|`이며
    `r,r'<=R`의 squarefree·coprime-to-q prime notation을 사용한다.
  - Motohashi 1975 Lemma 2에도 같은 두 product `(p+1)`가 나타나지만, `h`의 절대합이나
    현재 endpoint 합성을 더 자세히 증명하지 않는다. 따라서 provenance 보조자료이지
    drop-in numerical replacement가 아니다.
- provenance:
  - Jutila PDF SHA-256 `f6e9038a7216b690763692e0a07bc8c58284c9560bf62ab987ea62a817404ad5`.
  - Motohashi PDF 199,429 bytes, SHA-256
    `f4502e49ebbf31a6468bc0400b08ee332fc35b177926463fd3bb4e7bed92cfc9`.
- 도구상 문제: bundled Poppler 경로에는 `pdftotext.exe`가 없어 첫 native-text 명령이
  실패했다. MiKTeX `pdftotext.exe`로 재실행해 7,117 bytes를 추출했으며 Adobe-Japan1
  font-map warning은 있었지만 영문 수식 본문은 추출됐다. 판정은 렌더링 원페이지와
  대조한 내용에만 의존한다.
- 결정: 이미 peer-reviewed Jutila source statement가 있으므로 별도 analytic lemma를
  발명하지 않는다. 다만 원문이 숨긴 outer `(r,r')` 평균은 유한 divisor double-counting으로
  직접 수치화한다.
- 다음 재개점: local `h` 계수를 exact 전개하고, `K=floor(R)`에서 outer sum을
  Basel partial-sum 상계로 묶어 rational multiplier를 확정한다.

### 2026-09-13 17:36 KST — exact 합성·코드·Lean 전수 원장 완료

- exact 결과:
  - exclusive prime local coefficient `-p`, common prime coefficient `p(p-2)`.
  - `sum_d |h|`의 exact local product는 symmetric-difference에서 `p+1`, gcd에서
    `(p-1)^2`; 공통 `p=2`의 local 합은 정확히 1.
  - `K=floor(R)`에서 divisor double-counting과 finite Basel 상계로
    `H_q(R)<3R^2`.
  - Theory 67과 합친 초등 coefficient는
    `144*(1+1/theta)*(2/theta+1)`, `theta=1/21`에서 `136224`.
- 새 코드·문서: Theory 68, review 75, machine JSON, exact evaluator와 11개 단위시험.
- Python 검증: `py_compile` PASS, 표적 unittest 11/11 PASS.
- Lean:
  - 단일 정본 `lean/FGKMTSono/TheoryVerification.lean`에 local algebra, finite divisor
    double-count, Basel partial, pair/floor·coefficient 합성을 추가했다.
  - direct `lake env lean FGKMTSono/TheoryVerification.lean` exit 0.
  - generator·validator PASS: theory 69개, formula 1,226개, declaration 205개,
    `KERNEL_PASS=63`, `CONDITIONAL_KERNEL_PASS=35`, proof escape 0.
- 증거 경계: Jutila Lemma 3 전체 multiplicative-function proof와 finite-prime
  Euler-product induction은 source/partial 상태다. residue·absorption·averaged replay,
  PAP-11, fixed `2e-17`, `X_cert`는 OPEN이다.
- 교정한 작업상 문제:
  - machine JSON key의 임시 공백 오타를 strict parse 전 교정했다.
  - Lean scratch proof는 canonical 단일 파일에서 direct compile한 뒤 삭제했다.
  - Lean README 첫 patch와 이 원장의 첫 일괄 patch는 예상 문맥 불일치로 적용 전에
    거부돼 정확한 tail을 다시 읽고 작은 patch로 적용했다. 파일 손상이나 과학 결과
    영향은 없다.
- 다음 재개점: 상위 METHODS·AGENTS·T1·색인·문헌 종합·predecessor successor note를
  재생성된 inventory와 대조하고, 오류 원장·handoff를 작성한 뒤 전체 검증한다.

## 현재 재개점

다음 작업은 Theory 68 §8의 `JL7-RES`다. Jutila printed p.53의 principal residue와
Lemma 3 대각 identity, 같은 character의 repeated-height row sum을 source-first로
복원한다. drop-in peer-reviewed explicit source를 먼저 찾고, 없을 때만 actual finite
family에 직접 증명을 구성한다.

### 2026-09-13 17:43 KST — 정본 동기화·전수 검증·handoff 완료

- 정본 동기화: AGENTS, METHODS, theory/review 색인, T1 §37, Theory 66--67 successor
  note, 문헌 종합, Lean README를 Theory 68·review 75 판정과 맞췄다.
- 문서 교정: 일반 JavaScript 문자열에서 빠진 신규 inline `\(...\)` delimiter를
  commit 전에 전부 복구했다. Theory 68 display 안의 `\\(r,q)`는 line-break 뒤에
  공백을 넣어 Markdown inline delimiter와 혼동되지 않게 했다.
- 최종 검증:
  - 표적 unittest 11/11 PASS, `py_compile` PASS.
  - 전체 unittest 761/761 PASS, 62.134초, 사용자 사전 허가의 정상 로컬 권한.
  - direct Lean compile PASS; cached full `lake build` 8,765 jobs PASS.
  - generator/validator PASS: 69 theory, 1,226 formula, declaration 205,
    status 63/35/35/41/52/995/5, proof escape 0.
  - 변경·신규 텍스트 21개 strict UTF-8/control/trailing/math delimiter issue 0,
    JSON 3개 parse PASS, pre-final local link 1,529개 PASS.
  - `-done` rename 뒤 handoff 링크를 포함한 final local link 1,539개 PASS.
  - `git diff --check` exit 0; 출력은 기존 Git LF→CRLF 안내뿐.
- staged 감사: 첫 묶음 호출에서 신규 3파일의 `new blank line at EOF`를 발견했고,
  뒤 stat/status의 종료코드 0을 PASS로 오인하지 않았다. EOF 빈 줄을 제거한 뒤
  `git diff --cached --check`를 단독 재실행해 exit 0을 확인했다.
- handoff: `handoff/202609131738_HANDOFF.md`를 새 파일로 작성했다.
- 실행 경계: actual prime sweep·threshold calculator·장시간 연산·패키지 설치·외부 게시는
  수행하지 않았다.
- 다음 재개점: `JL7-RES`; 현재 사용자 수행절차는 없다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 source theorem 경계 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
