# DEP-R09 Jutila JL7-AVERAGED source-first replay 작업원장

- 시작: 2026-09-13 23:56 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: (X_{\rm cert}) 계산기 전 정규화·증명작업을 권장 순서대로 계속하고,
  필요한 lemma는 선행 source를 먼저 개별 검토한 뒤 부족한 연결부만 직접 증명하며,
  필요하면 Lean 형식화·검증하고 단계 완료 뒤 로컬 staging·commit한다.
- 금지·보류: 실제 prime sweep, actual maximal-gap 실험, threshold calculator,
  장시간 연산, package 설치, raw PDF 수정, push/PR은 수행하지 않는다.
- 선행 변경: 시작 시 `git status --short` 출력 0건. 직전 정본 commit은
  `9fcf236d143a206467fa2e72d4458045a20ebdfc`다.

## 목적과 완료조건

- 목적: Jutila 1977 식 (3.6)의 fixed-modulus·selected-system terminal bound를
  식 (3.7)의 modulus/character 평균으로 옮기는 정확한 counting map을 복원하고,
  기존 Theory 70의 상수·strict absorption이 평균에서도 보존되는지 판정한다.
- 완료조건:
  1. printed pp.53--54와 theorem statement를 native/OCR locator 뒤 렌더 원문으로 대조한다.
  2. modulus, primitive conductor, induced character, parity, selected-zero system의
     중복계수와 endpoint를 source 식에 맞게 전사한다.
  3. 선행정리로 닫히는 부분과 source에 숨은 multiplier/cutoff를 구분한다.
  4. 닫을 수 있는 finite counting·상수 대수는 exact Python과 필요 시 Lean으로 검증한다.
  5. Theory·review·T1/METHODS/색인·Lean 원장·오류 원장·handoff를 증거 범위에 맞게 동기화한다.
  6. 전체 관련 회귀와 정적 검사를 통과하고 새 로컬 commit을 만든다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | fixed-modulus 결과를 평균 정리로 확대할 때 합의 지수·중복계수를 원문에서 재구성한다. |
| 데이터·provenance | actual dataset 영향 없음 | Jutila 고정 PDF/hash와 렌더 원문만 사용하고 raw PDF는 수정하지 않는다. |
| 통계·정밀도 | 경험통계 영향 없음 | 정수·유리수 상수는 exact arithmetic, 초월함수는 진단과 판정을 분리한다. |
| 승인 경계 | 영향 없음 | 장시간 계산·actual 실험·calculator는 계속 금지한다. |
| Lean 증거 | 확인 필요 | (X_{\rm cert}) 의존 finite counting/algebra만 source 고정 뒤 단일 Lean 파일에 추가한다. `sorry`·`admit`·local `axiom` 금지. |
| 정리 범위 | 영향 큼 | actual branch, printed general theorem, PAP bridge를 서로 자동 승격하지 않는다. |
| 산출물·비덮어쓰기 | 영향 있음 | Theory 71/review 78와 machine ledger를 신규 작성하고 기존 정본은 successor 링크만 갱신한다. |

## 단계 현황

1. **DONE — source·notation·범위 전사**
2. **DONE — averaged counting map 및 상수 손실 감사**
3. **DONE — exact checker·단위시험·Lean 필요성 판정과 형식화**
4. **DONE — Theory/review 및 정본 동기화**
5. **DONE — 전체 검증·handoff 완료, 완료 이관 뒤 로컬 commit 준비**

## 단계별 기록

### 2026-09-13 23:56 KST — 착수·영향도 고정

- 수행: 최신 handoff, AGENTS의 Lean/PDF/source-first 규약, 직전 Theory 70 상태와
  Jutila PDF/OCR/render artifact 존재를 확인했다.
- 파일: 이 작업원장을 신규 작성했다.
- 명령·검증: `git status --short` 출력 0건; Jutila PDF·18개 page render/OCR 파일 존재.
- 결과: source-first replay를 안전하게 착수할 수 있다. 새 다운로드나 장시간 연산은 현재 필요 없다.
- 문제·결정: OCR은 locator일 뿐이며 핵심 수식은 rendered printed page와 대조한다.
- 다음 재개점: Jutila pp.53--54 OCR text와 page images, Theory 60·66·70의 (3.6)/(3.7)
  전사를 나란히 대조하고 식 (3.7)의 정확한 합 범위를 기록한다.

### 2026-09-14 00:22 KST — 원문 전사·선행 source 재검색 완료

- 수행: Jutila, *On Linnik's constant* printed pp.46, 50--54를 300 dpi 렌더와
  대조했다. 식 (3.7), `|eta_j|=q_j/phi(q_j)`, modulus별 pseudocharacter,
  primitive character의 principal-pair 조건을 원문에서 재확인했다.
- 추가 source: 공식 IMPAN 원문
  `article/Jutila 1977 Zero-density estimates for L-functions.pdf`를 확보했다.
  SHA-256은
  `cbe2d1e7115717cf28f9ffaffdc1fe232958595b17c5c2ee59fc968e8ff0d5a1`,
  크기는 400,716 bytes, 5 PDF pages다. native text는 5 bytes뿐이어서 OCR은
  locator로만 쓰고 5개 landscape PDF page에 함께 수록된 printed pp.55--62를
  모두 원페이지로 대조했다.
- source 판정: 후속 논문은 primitive conductor가 `<=Q`인 variable-character
  mean-value 구조를 뒷받침하지만 상수는 `<<_{epsilon,k}`와 `(QT)^epsilon`에
  남긴다. 식 (3.7)의 생략된 수치 replay를 그대로 제공하는 drop-in 선행정리는
  표적 검색에서 식별하지 못했다. 이는 문헌 전체에 없다는 주장이 아니다.
- 정확한 counting map: detector의 `phi(q_j)/q_j`는 phase weight
  `q_j/phi(q_j)`로 각 항에서 상쇄된다. principal product는 같은 primitive
  character에서만 생기고 그때 conductor도 같으므로, residue의 두
  `phi(q)/q`와 phase weight의 제곱도 정확히 상쇄된다. off-diagonal에는
  각 phase weight를 `<=6 log(D)`로 따로 상계해야 한다.
- 새 핵심 확인: averaged family에서는 공통 scale을 `D=Q^2 T`로 잡아 product
  conductor를 덮을 수 있지만, Theory 64의 `D=qT` detector cutoff를 문구만 바꿔
  재사용하면 안 된다. 각 `q_j<=Q`에 대해 Mellin scale의 상·하 envelope를 다시
  증명하고 공통 cutoff를 갱신해야 한다.
- 다음 재개점: `D=Q^2T` 공통 매개변수에서 uniform detector의 Mellin exponent와
  식 (3.7)의 diagonal/off-diagonal coefficient를 직접 유도한 뒤, full averaged
  terminal을 닫을 수 있는지 fail-closed로 판정한다.

### 2026-09-14 01:02 KST — averaged 상수 합성과 exact/Lean 검증 완료

- 공통 detector: \(D=Q^2T\)에서
  \(D^{1/2+9\theta}\le A_j\le D^{1+9\theta}\)를 분리했다. power condition에는
  오른쪽 상계, Mellin decay에는 왼쪽 하계를 사용했다.
- phase/counting: detector와 phase의 totient factor, principal pair의
  phase·residue·pseudocharacter factor가 exact 1로 상쇄됨을 확인했다.
  off-diagonal phase pair는 \(L^{-2}\) 정규화 뒤 36 이하이며 product conductor는
  \(Q^2\) 이하라 공통 contour가 덮는다.
- terminal: Theory 70과 같은 \(A,B,E\), strict half-margin과
  \(C_J=884000/[9(1-\theta)^2\theta^6]\)가 raw \(Q\) 손실 없이 보존된다.
  actual primitive nonprincipal near-one averaged branch만 parameterized explicit으로
  판정했다. printed all-alpha·PAP·fixed coefficient·\(X_{\rm cert}\)는 OPEN이다.
- 구현: <code>source/dep_r09_jutila_jl7_averaged.py</code>, 9개 fail-closed test,
  machine ledger, Theory 71, review 78을 만들었다.
- Lean: 단일 파일에 phase/residue cancellation, phase-pair 36, Mellin envelope
  방향, common \(L^2\) cancellation, terminal reuse와 local log upper를 추가했다.
  direct compile exit 0, generator/validator PASS다. 현 inventory는 theory 72개,
  display 1,295식, declaration 240개, 금지 proof escape 0건이다.
- 새 source: Jutila 1977 *Zero-density estimates for L-functions* 공식 PDF의
  hash·크기·렌더 확인을 machine ledger에 고정했다. 사용자가 추가한
  <code>Maier 1981.pdf</code>, <code>McCurley 1984.pdf</code>,
  <code>gallagher1970.pdf</code>도 현재 hash가 기존 Theory 57 source registry와
  정확히 일치한다.
- 발견·교정: Theory 71 초안의 <code>\qquad</code> 세 곳이 문자열 transport에서
  backslash를 잃은 것을 PCRE 검사로 찾아 고쳤다. 첫 Lean 초안의 order API와
  중첩 곱 metavariable 오류도 전제를 바꾸지 않고 고쳤다. 오류 원장 E119에 기록했다.
- 검증: 신규 표적 unittest 9/9 PASS, direct Lean compile exit 0,
  Lean ledger validator PASS.
- 다음 재개점: 정본 link·상태 문구의 stale reference와 control/LaTeX transport를
  전수 검사하고 전체 unittest·Lake build·Markdown/JSON/diff 검증을 수행한다.

### 2026-09-14 00:49 KST — 전체 회귀·형식·정적 검증 완료

- Python: 신규 표적 unittest 9/9 PASS, py_compile PASS, 전체 unittest 794/794 PASS
  (110.567초, 사용자가 허가한 정상 로컬 권한).
- Lean: direct compile exit 0, full Lake build 8,765 jobs PASS.
- 검증원장: generator 72 theory·1,295 display식 생성, validator PASS;
  declaration 240개, 금지 proof escape 0건이다.
- 상태 분포: KERNEL_PASS 75, CONDITIONAL_KERNEL_PASS 47, DEFINITION_ONLY 55,
  PARTIAL_FORMALIZATION 56, SOURCE_THEOREM_UNFORMALIZED 58,
  NOT_YET_FORMALIZED 999, PARSE_REVIEW_REQUIRED 5다.
- 정적 검사: 변경 text 19개 strict UTF-8/control-character 0건, JSON 3개 strict parse,
  Markdown 12개 local link 1,616건 issue 0, 새 문서 missing-LaTeX-command issue 0.
- source: 사용자가 추가한 Maier 1981, McCurley 1984, Gallagher 1970 PDF의 SHA-256이
  기존 Theory 57 source registry와 정확히 일치함을 재확인했다.
- stale-reference 검사에서 AGENTS의 긴 현재상태 요약 한 곳이 Theory 70을 최신으로
  가리키고 averaged replay 전체를 OPEN이라 적은 것을 찾았다. narrow averaged branch와
  broad PAP 범위를 분리해 Theory 71/review 78 현재 판정으로 교정했다.
- 검증 도구 시행착오: 첫 UTF-8 검사 초안은 PowerShell nested output을 잘못 합쳤고,
  다음 초안은 `${p}`가 필요한 colon 인접 변수 문법을 썼다. 첫 JSON parse도
  case-insensitive key 충돌을 경고하면서 계속 실행됐다. 세 결과를 모두 PASS 증거에서
  제외하고, 명시적 allowlist·format operator·`-AsHashtable`·fail-fast로 다시 실행해
  위 최종 결과를 얻었다. 저장소 파일이나 과학 판정에는 영향이 없다.
- 다음 재개점: 새 timestamp handoff에 결과·열린 root·다음 source-first 순서를 적고,
  작업원장을 `-done`으로 이관한 뒤 명시적 allowlist staging과 cached diff 검증 및
  로컬 commit을 수행한다.

### 2026-09-14 00:50 KST — handoff·마감 정적검사 완료

- 새 handoff: <code>handoff/202609140050_HANDOFF.md</code>를 작성했다.
- 일반 <code>git diff --check</code>: exit 0. 신규 파일은 완료 원장 이관 뒤
  명시적 staging하여 <code>git diff --cached --check</code>로 별도 검사한다.
- handoff local link는 완료 원장 rename 전 그 미래 경로 하나만 예상대로 없었으며,
  rename 뒤 다시 검사한다.
- 모든 요청 산출물·정본 동기화·형식/회귀 검증·handoff가 끝났다. 이 원장을
  <code>-done</code>으로 이름 변경한 다음 staging transaction을 수행한다.

## 현재 재개점

전체 unittest와 Lake build를 실행하고, 생성 원장·Markdown link·JSON·control
character·LaTeX command·diff 검사를 완료한다. 그 뒤 새 handoff를 작성하고 이
원장을 <code>-done</code>으로 이관해 명시적 allowlist를 staging·commit한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 시각 QA 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check` 전 정적 검사와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경 준비 완료
