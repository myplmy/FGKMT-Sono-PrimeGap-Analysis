# H1b-COV2 / DEP-R08 작업원장

- 작업 시작: 2026-09-10 04:14 KST
- 상태: 완료
- 목표: `X_cert` 계산기 착수 전에 필요한 covering 후단의 정규화·증명 의무(DEP-R08)를 source-first 방식으로 감사하고, 닫을 수 있는 하위 의무를 명시적 상수·cutoff와 함께 닫는다.
- 승인 경계: 문헌·기존 artifact 읽기, 수학 증명·문서·검증 코드 작성 및 로컬 검증, 로컬 스테이징·커밋 허가. actual prime 실험·threshold calculator·외부 게시·push는 수행하지 않는다.

## 단계 체크리스트

- [x] 0. 최신 handoff·AGENTS·작업원장 규약·관련 스킬 및 메모 확인
  - 최신 handoff: `handoff/202609092359_HANDOFF.md`
  - 다음 시작점: H1b-COV2 / DEP-R08, 우선 source interval·floor·rounding 감사
  - 별도 미커밋 변경 7개를 발견했으며 본 작업과 섞기 전에 provenance·정합성·검증 상태를 별도 감사한다.
- [x] 1. 영향도·범위 및 기존 변경 감사
  - COV2가 건드리는 proof-obligation 행, DAG edge, 정본 문서와 테스트를 식별한다.
  - 다른 작업 변경은 내용·검증 증거·충돌 여부를 확인해 별도 allowlist 커밋 후보로 분리한다.
- [x] 2. source-first 원문 추적
  - FMT/Sono 원문의 covering interval, partition, floor/rounding, smooth remainder, simultaneous-good-event 호출을 native text와 핵심 페이지 렌더링으로 대조한다.
  - drop-in 선행 정리 존재 여부와 적용 조건을 판정한다.
- [x] 3. H1b-COV2a 정규화·증명
  - actual interval family와 정수 경계, `m`·`|A'|`·분할 크기 관계를 명시한다.
  - rounding/endpoint 손실을 정확한 유한 부등식과 cutoff로 닫거나 OPEN 의무를 수치적으로 고립한다.
- [x] 4. H1b-COV2b 합성 감사
  - smooth-number remainder, covering 후 예외 복원, simultaneous good choices의 총 error budget을 합성한다.
  - 닫히지 않는 항은 필요한 정리·상수·수치 목표를 명시한다.
- [x] 5. 구현·검증·정본 동기화
  - 필요한 경우 pure helper/contract/test를 작성한다.
  - 고정 FGKMT Python으로 targeted test, 관련 proof-contract test, 전체 unittest를 실행한다.
  - T1/DEP/색인/리뷰 문서를 실제 판정과 동기화한다.
- [x] 6. 결과 보고·handoff·커밋
  - 새 `YYYYMMDDHHmm_HANDOFF.md`에 다음 권장 순서·근거·예상시간·사용자 절차·커밋 메시지를 기록한다.
  - 정확한 pathspec allowlist로 로컬 커밋하고 push하지 않는다.
  - 모든 산출물·검증·handoff·커밋이 끝난 뒤에만 이 원장을 `-done`으로 이름 변경한다.

## 현재 재개점

이 원장의 요청 범위는 완료됐다. 다음 작업은 새 원장을 만든 뒤 `DEP-R09 numerical PAP`
source·constant 감사에서 시작한다. COV2를 처음부터 반복하지 않는다.

## 단계별 기록

### 2026-09-10 04:14–05:00 KST — 범위·선행 변경 감사

- COV2의 직접 대상은 `DEP-R08`, T1의 `COV-01`–`COV-12`, H1b/H1c의 다음 gate와
  새 successor contract다. 과거 hash-pinned COV1/COV1a 계약은 소급 수정하지 않는다.
- 시작 시 남아 있던 review 56·두 완료 원장·두 handoff·오류 원장 E078·이론 색인 변경은
  서로 연결된 선행 문서 작업으로 확인했다. review 57은 commit `05fc40f`에 이미 추적된다.
- 선행 변경 7파일을 strict UTF-8·control character·로컬 링크 114건·정확 유리수 산술로
  재검사해 issue 0, `git diff --check` 오류 0을 확인했다. COV2와 별도 allowlist commit으로
  보존한 뒤 본체를 작성한다.

### 2026-09-10 04:20–05:00 KST — source-first 감사

- Sono PDF는 native pdfTeX 24쪽, FMT PDF는 native text 16쪽임을 확인했다. Sono printed
  pp.538–542와 FMT pp.8–11은 text를 먼저 읽고 원본 page render로 식·끝점·양화를 대조했다.
  Rosser–Schoenfeld printed pp.69–70은 scan+text layer라 원본 page를 함께 대조했다.
- Sono의 interval 분할은 고정 유한 family와 `O(1/epsilon)` union으로 충분하지만 literal
  cell-count 문구에는 작은 crossing interval에서 off-by-one 위험이 있다. 그 문구를 그대로
  숫자화하지 않고 equal-grid deterministic cover를 새로 증명한다.
- smooth remainder의 source는 FMT §4의 `o(x/log x)`와 강한 smooth-number 감쇠다.
  명시형 선행결과를 먼저 조사했으나 확인한 Waterloo bound는 이 parameter에서 필요한
  `u log u` 강도를 주지 못하고, Ford 강의노트의 sharp 형태는 여전히 implied constant다.
  따라서 기존 Rankin 방법과 Rosser–Schoenfeld의 명시적 prime sums로 special-case finite
  lemma만 직접 증명한다. 새 다운로드·OCR·라이브러리 설치는 필요하지 않았다.

### 2026-09-10 13:20–14:05 KST — COV2a/COV2b 정식화와 사후감사

- `J=ceil(2/epsilon)` equal grid로 임의 구간의 덮개 길이를
  `length+2/J<=length+epsilon`으로 증명했다. crossing interval의 off-by-one과 정수
  floor endpoint를 별도 exact test로 고정했다.
- `80*c*b/A>=5`를 명시 gate로 두어 `m>=1`, `A<=A'<5A`, 허용범위를 hidden
  Vinogradov constant 없이 닫았다.
- 실제 cell 폭을 사용해 예외복원비를 `2/((1-r_pre)*A*h*b)<7/(A*epsilon*b)`로 낮추고,
  outer residue 선택과 conditional covering 선택을 독립성 없이 순차 합성했다.
- smooth 초안의 적분 설명을 그대로 채택하지 않고 다시 감사했다. Rosser--Schoenfeld
  printed pp.65, 70--71의 (2.7), Theorems 5·9를 원본 이미지와 대조하고,
  Stieltjes 부분적분으로 first Euler increment를 `567/500*u<189/160*u`로 닫았다.
  따라서 final `#R<(log b/(17b))*X/a` 상계의 기존 여유가 유지된다.
- fixed `A,epsilon,eta`의 finite gates 아래 `DEP-R08`만
  `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 닫았다. 최종 parameter 선택, 같은 Sono 계수
  총예산, PAP/UB, final-variable transfer, broad root와 `X_cert`는 승격하지 않았다.
- targeted 및 관련 9모듈 회귀 165개를 FGKMT Python으로 실행해 165/165 PASS를 확인했다.
  첫 관련 회귀의 2 failures는 이전 `next_gate` 문구·9월 9일 header를 고정한 동기화 검사였고,
  현재 DEP-R09/COV2 상태를 직접 검사하도록 고친 뒤 전부 통과했다.

### 2026-09-10 14:05–14:20 KST — 전체·정적 검증

- 최초 sandbox 전체 회귀는 664개 중 82 errors와 1 failure였다. 82 errors는 repository
  `tmp`와 시스템 temporary directory의 읽기·쓰기·삭제를 sandbox가 거부한 동일 환경
  오류였고, 코드 판정에서 분리했다. 1 failure는 H1b-DEP의 2026-09-09 역사적 T1 합계에
  COV1a 한 행만 더한다고 가정한 stale 회귀였다.
- 합계만 새 숫자로 바꾸지 않고 COV1a의 `COV-06 HARD_BLOCKER -> EXPLICIT`과 COV2의
  `COV-02/03 RATE_MISSING -> EXPLICIT`, `COV-09 PARTIAL -> EXPLICIT`,
  `COV-08/11 HARD_BLOCKER -> PARTIAL`을 행별 successor delta로 검사하도록 교정했다.
- 관련 10모듈 **185/185 PASS**(0.769초). 사용자가 허가한 정상 로컬 권한에서 고정
  `W:\miniforge3\envs\FGKMT\python.exe`로 최종 전체 **664/664 PASS**(68.219초, exit 0).
  실제 prime 데이터·threshold 계산은 실행하지 않았다.
- 25파일 strict UTF-8·제어문자·끝 공백 issue 0, `py_compile` 3파일 PASS, JSON 4개 parse
  PASS, theory55 식번호 55.1–55.39 유일·연속, 변경 Markdown 10파일의 local link 177개
  issue 0, 세 primary PDF SHA-256 일치, `git diff --check` PASS를 확인했다.
- 사람 검토에서 새 문서에 남은 inline math delimiter와 METHODS의 display delimiter 누락을
  교정한 뒤 관련 185개 회귀를 다시 통과했다. 수학식·상수·판정은 바꾸지 않았다.

### 2026-09-10 14:20–14:30 KST — 본체 commit·handoff·종료

- 본체 24파일을 exact pathspec으로 stage하고 cached count 24, cached diff check PASS를
  확인한 뒤 local commit `5629565b8a5cafd742134eeafb72848c65314f04`
  (`H1b-COV2 후단 covering 유한 합성 명시화`)로 보존했다. push/PR은 없다.
- 새 handoff `handoff/202609101426_HANDOFF.md`에 쉬운 결론, source hash, 검증, 열린
  R09–R12, 다음 순서·예상시간·사용자 절차를 기록했다. 현재 사용자 수행절차는 없다.
- handoff 초안에서 짧은 hash를 확인 없이 40자로 확장한 provenance 환각을 발견했다.
  `git rev-parse HEAD`의 실제 hash로 commit 전에 교정하고 오류 원장 `E081`에 기록했다.
- 요청 산출물·검증·정본 동기화·handoff가 끝났으므로 이 원장을 `-done` 이름으로 이관하고,
  handoff·오류 원장·완료 원장만 별도 exact allowlist 인계 commit으로 보존한다.

## 실패·중단 기록

- 선행 변경 정적검사의 첫 PowerShell 명령은 문자열 `control:$file:$n`에서 colon이 변수명으로
  해석되어 parser 오류로 중단됐다. 파일 변경·검증 결과 생성은 없었다. `${file}`로 교정한
  동일 검사는 7파일·114 local links·issue 0으로 통과했다.
- 최초 theory 55 문자열의 LaTeX escape 제어문자, 불충분한 `Ein` 설명, 연쇄 식번호 치환과
  넓은 `tmp` 검색 재발은 commit 전에 모두 교정했다. actual/threshold 결과는 생성하지 않았고,
  오류 원장 `E079`에 영향과 재발방지를 공개했다.
- 최종 정적감사의 첫 PowerShell 보간 문자열에서도 colon 뒤 변수 구문 오류가 재발했다.
  parser 단계 실패라 파일 영향은 없었고 모든 colon 앞 변수를 `${...}`로 감싼 재실행은
  통과했다. 추가 inline-math 정규식은 정상 표시수식 괄호를 잡는 과잉탐지여서 폐기했다.
  closure 링크 검사에서도 `foreach`의 `in` 뒤 공백 누락으로 parser가 한 번 실패했다가
  교정 실행이 통과했다. 세 사실과 재발방지는 오류 원장 `E080`에 기록했다.
