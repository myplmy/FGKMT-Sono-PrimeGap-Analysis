# DEP-R09 explicit PNT-in-AP 대체 source 감사 완료 작업원장

- 착수: 2026-09-13 08:38 KST
- 시작 HEAD: `7d9e53e4ea1737e4693bb0332bfbe5ee59387b79`
- 사용자 승인: “권장 우선순위에 따라 작업 착수”
- 현재 gate: `DEP-R09 / PAP-11 / fixed 2e-17 / X_cert OPEN`
- 선행 정본: `docs/method/theory/57_Sono_FMT_DEPR09_Gallagher_Maier_McCurley_source_recovery.md`
- 금지: actual prime sweep, threshold calculator, 외부 저자 연락, package 설치,
  `sorry`·`admit`·project-local `axiom`, source의 숨은 상수를 임의 숫자로 치환

## 영향 분석

| 축 | 판정 | 통제 |
|---|---|---|
| 반복로그·end-bounded G/F/H | 영향 없음 | empirical 정의·결과 파일을 변경하지 않는다. |
| fixed `2e-17` 증명 경로 | 핵심 영향 | 대체 source가 실제 변수범위·상수·예외 처리를 충족할 때만 후보로 승격한다. |
| `X_cert` | 핵심 영향 | 하나의 source gate나 cutoff를 최종 threshold로 부르지 않는다. |
| provenance | 핵심 영향 | DOI/arXiv/journal version, statement locator, 공개 원문 hash를 기록한다. |
| Lean | 조건부 영향 | source theorem은 무가정 재증명하지 않고, 사용할 finite algebra/interface만 형식화한다. |
| 데이터·실험 | 영향 없음 | maximal-gap data, `test_result`, figure를 생성하지 않는다. |
| 승인 | 범위 내 | 공개 학술자료의 read-only 검색·다운로드와 로컬 문서·toy 검증만 수행한다. |

## 목표와 판정 기준

목표는 다음 중 하나를 증거와 함께 판정하는 것이다.

1. Sono의 공개 correction/erratum이 Section 5 상수 전달을 실제로 교정한다.
2. 기존 또는 현대의 explicit PNT-in-AP theorem이 actual PAP 변수범위에서
   `c1=1/8` 또는 fixed `2e-17`을 회복할 충분한 정량 package를 제공한다.
3. drop-in source가 없다면, 가장 가까운 후보가 정확히 어느 조건에서 탈락하는지와
   Gallagher–Maier 재증명에 남는 최소 obligation을 확정한다.

`effective`, `computable`, `explicit constant exists`만으로는 PASS가 아니다. theorem statement에
수치 multiplier·finite cutoff·modulus/height 범위·exceptional-zero 처리·uniformity가 있어야 한다.

## 단계 현황

1. **COMPLETE — 시작 상태·승인·영향도 고정**
2. **COMPLETE — 기존 R09/H1c source inventory와 actual target 정규화**
3. **COMPLETE — Sono 공식 version·correction/erratum 공개자료 확인**
4. **COMPLETE — 현대 explicit PNT-in-AP 후보 source 수집·적용성 matrix**
5. **COMPLETE — 권장 repair route·finite interface·Lean 상태 분류**
6. **COMPLETE — 정본 동기화·검증·새 handoff**

## 단계별 기록

### 2026-09-13 08:38 KST — 단계 1 완료

- `git status --short` 출력은 0건이고 시작 HEAD는 `7d9e53e4ea1737e4693bb0332bfbe5ee59387b79`다.
- 활성 비완료 작업원장은 없었고 최신 handoff는 `handoff/202609110319_HANDOFF.md`다.
- 다음 재개점: Theory 57, H1c source inventory, T1 R09 행에서 필요한 actual PAP의
  변수·오차·예외 계약을 하나의 표로 복원한다.

### 2026-09-13 — 단계 2 완료

- actual target은 각 관련 modulus와 reduced residue에 대한 pointwise one-sided lower bound이며,
  형태상 범위는 `q <= u^(1/D_PAP)`이다. 평균 Bombieri--Vinogradov 명제와 바꾸어 쓰지 않는다.
- fixed 계수 경로는 `D_PAP=160`, `C_PAP=1-exp(-2)`뿐 아니라 principal term,
  nonprincipal error, exceptional modulus, prime-power/partial-summation/endpoint 보정을 하나의
  공통 finite cutoff에서 요구한다.
- Theory 57의 `K_G`, `x_G`, `eta_pr`, `eta_psi_to_pi`를 숨기지 않는 finite interface를
  successor에서도 유지한다.

### 2026-09-13 — 단계 3 완료

- arXiv `2404.06951v4`(2024-06-05 최종 공개 revision)와 2025 journal PDF의 Section 5를
  native text와 렌더링 페이지로 대조했다. 양쪽 모두 `c1=3c_ZFR`, `a=3c_ZFR/10`,
  `C_PAP=1-exp(-2)`, `D_PAP=160`을 그대로 인쇄한다.
- arXiv record의 version history/comments와 journal article page에서 별도 correction/erratum을
  공개적으로 식별하지 못했다. 이는 저자에게 비공개 설명이 없다는 뜻이 아니며 저자 연락은 하지 않았다.
- 최신 arXiv PDF SHA-256은
  `18a7fa5adde5a203ba93aa5a75edbf03625605f1532594ed5a4101b2c1ba6634`다.

### 2026-09-13 — 단계 4 완료

- Bennett et al. 2018, Bordignon 2021, Yamada 2014, Kadiri 2005와 현대
  Thorner--Zaman PNT-in-AP·explicit log-free density, Benli--Goel--Twiss--Zaman의
  explicit Deuring--Heilbronn source를 statement 단위로 비교했다.
- Bennett의 큰-modulus cutoff는 `exp(0.03 sqrt(q) log^3 q)`형이어서
  `q=u^(1/160)` 경계 전체를 덮지 않는다. Bordignon은 polylog modulus, Yamada는 평균합,
  Kadiri는 `q<=400000`인 유한 범위이므로 drop-in이 아니다.
- Thorner--Zaman의 uniform PNT는 구조적으로 가장 가까우나 implied constant와 decay constant가
  `effectively computable`로만 주어져 numerical PAP certificate가 아니다.
- Thorner--Zaman의 fully explicit density는 127/198 exponent와 매우 큰 prefactor를 제공하고,
  Benli et al.은 exceptional-zero repulsion을 수치화한다. 둘은 유용한 구성요소이지만
  PAP의 pointwise lower bound, transfer multiplier와 공통 cutoff를 직접 주지는 않는다.
- 고정 downstream 식에서 `D=160`일 때 필요한 최소 `C_PAP`은
  `0.8638312615226712472...`; 허용 총 상대오차는 `0.1361687384773287528...`다.
  인쇄값의 `exp(-2)`와 비교한 추가 오차 여유는 `0.0008334552407160609...`뿐이다.
- 낙관적으로 `C_PAP=1`이어도 같은 downstream 식이 fixed `2e-17`을 유지하는 최대 정수
  `D`는 186이다(`D=186` PASS, `D=187` FAIL). 따라서 exponent 198 같은 coarse 경로를
  `D>=198`로 직접 연결하는 방식은 나머지 상수를 개선하지 않고는 목표 계수를 보존할 수 없다.
- 다음 재개점: source matrix와 두 repair branch를 Theory 58/review 65/기계 JSON에 고정하고,
  수치 budget을 독립 unittest로 재계산한다. source theorem 자체를 Lean axiom으로 만들지 않는다.

### 2026-09-13 — 단계 5 완료

- Theory 58, review 65, replacement source machine JSON과 fail-closed unittest를 신설했다.
- 주축 `BRANCH_S_SHARP`는 D=160을 유지하며 모든 multiplier·cutoff를 복원한다. 보조축
  `BRANCH_E_FULLY_EXPLICIT_COARSE`는 explicit density/DH component를 새 pointwise transfer로
  합성하되 fixed 계수를 자동 보장하지 않는 cross-check다.
- 첫 표적 test가 target을 `mp.mpf(2) * 10**-17`로 만든 진단 one-liner의 binary-float 선평가를
  발견했다. exact `mp.mpf(10) ** -17`로 모든 고정밀 문자열을 교정했고 E095에 기록했다.
  `D=186` PASS, `D=187` FAIL 경계와 연구 판정은 바뀌지 않았다.
- 교정 후 표적 unittest는 7/7 PASS했다. source audit copy가 존재하면 hash를 검사하되,
  `tmp` 정리 후에도 정본 test가 깨지지 않도록 remote source hash·URL을 machine ledger에 보존했다.
- Theory 58의 16 display 식을 Lean 전수 inventory에 추가했다. source theorem 7,
  definition 1, `NOT_YET_FORMALIZED` 8이며 새 Lean declaration은 없다. generator 결과는
  theory 59, formula 1,046이고 validator는 declaration 116, banned escape 0으로 PASS했다.
- 다음 재개점: AGENTS/METHODS/index/Lean README 동기화를 재검사하고 전체 회귀시험·UTF-8·link·
  stale-state 감사를 거쳐 새 handoff를 만든다.

### 2026-09-13 09:18 KST — 단계 6 완료

- Theory 58의 두 LaTeX 표기에서 누락된 `\\qquad`·`\\quad` 백슬래시를 발견해 수식
  의미를 바꾸지 않고 교정했다. 이후 Lean formula inventory를 다시 생성했다.
- Lean generator는 theory 59개·display 식 1,046개를 생성했고 validator는 declaration
  116개, banned proof escape 0개, local Markdown link 1,108개로 PASS했다.
  상태는 `KERNEL_PASS=28`, `CONDITIONAL_KERNEL_PASS=17`, `DEFINITION_ONLY=5`,
  `PARTIAL_FORMALIZATION=8`, `SOURCE_THEOREM_UNFORMALIZED=15`,
  `NOT_YET_FORMALIZED=968`, `PARSE_REVIEW_REQUIRED=5`다.
- `lake build`는 8,765 jobs를 PASS했다. 외부 source theorem을 project-local axiom으로
  넣지 않았고 새 Lean declaration도 만들지 않았다.
- DEP-R09 선행·신규 표적 unittest 12/12가 PASS했다. sandbox 안 전체시험은 임시폴더 ACL로
  82개 `PermissionError`가 나와 무효로 분류했고, 승인된 sandbox 외부 FGKMT Python에서
  같은 전체 suite를 다시 실행해 676/676 PASS(87.676초)를 확인했다.
- handoff를 포함한 변경·신규 16파일은 strict UTF-8·ASCII control·수식 delimiter 검사를
  PASS했고 local link 1,249건, JSON 3파일 parse, Python 2파일 compile, 금지된 네 글자
  프로젝트명 오탈자 0건을 확인했다. source hash·fail-closed 상태는 표적 test와 validator로 확인했다.
  `git diff --check`는 내용 오류 없이 기존 LF→CRLF 안내만 출력했다.
- 검증 중 `lean/` 작업 디렉터리와 `lean/tools/...` 상대경로를 중복한 첫 명령 실패와
  sandbox 전체시험의 환경 실패를 E096에 기록했다. 두 실패 모두 과학 결과나 정본을
  생성하지 않았다. 최종 정적검사에서 E091의 PowerShell 콜론 보간 실수를 반복한 것도
  E097에 기록했고, `-f` 형식으로 교정한 전체 검사를 다시 PASS했다.
- actual prime sweep, maximal-gap 분석, threshold calculator, 저자 연락, package 설치는
  수행하지 않았다. 다음 분석 우선순위는 Branch S의 quantitative Gallagher--Maier 또는
  Thorner--Zaman multiplier·decay·finite cutoff 복원이다.

### 2026-09-13 — 다음 작업 착수 전 post-close 문서 감사

- 최신 handoff의 \(X_{\rm cert}\) 세 곳에서 JavaScript patch 문자열 처리로 수식
  구분자가 빠진 것을 발견했다. METHODS의 오래된 H1a 문단에서 같은 계열의 표기 6곳도
  확인해 모두 단일 LaTeX 구분자로 복구했다. 수학 판정과 수치는 바뀌지 않았다(E098).
- 기대 literal 검사에서 `rg -q`의 무출력을 실패로 잘못 해석한 false negative는
  `$LASTEXITCODE` 기준으로 교정했다. 기대 literal exit 0, 중복 백슬래시 검색 exit 1을
  확인했다(E099).
- 교정 뒤 DEP-R09 표적시험 12/12, Lean ledger validator, strict UTF-8/control,
  `git diff --check`를 다시 PASS했다.

## 완료 전 체크

- [x] 공식 Sono version/correction 상태와 확인일 기록
- [x] 후보마다 primary source statement·page/equation·hash 기록
- [x] actual q/u/D/B 범위와 coefficient budget 적합성 비교
- [x] drop-in / compositional / insufficient / unrelated를 구분
- [x] source theorem과 Lean kernel child를 분리
- [x] fixed `2e-17`, PAP-11, X_cert 상태를 fail-closed 동기화
- [x] 표적·전체 검증, 새 handoff, 사용자 수행절차 기록
