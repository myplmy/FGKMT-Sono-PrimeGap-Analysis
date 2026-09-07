# H1b-1b-2 local-factor 하한 감사 작업원장

- 시작: 2026-09-07 13:41 KST
- 현재 상태: COMPLETE
- 사용자 승인: 최신 핸드오프의 권장 순서에 따른 H1b-1b-2 local-factor 감사, 필요한 학술자료 취득, 정본·검증·핸드오프 갱신
- 금지·보류: actual prime sweep, threshold calculator, 장시간 실험, 임의 상수 대입, 패키지·Lean 설치, commit/push/PR
- 선행 상태: 시작 시 활성 작업원장 0개, git status clean

## 목적과 완료조건

Maynard Lemma 8.4의 실제 gamma_j를 원정의까지 추적하고, c_gamma_j Euler product의 작은 제외 소수·큰 제외 소수·비제외 소수 factor를 정확한 식으로 분해한다. 명시적 uniform lower bound 가능성을 판정하고, 가능한 경우 parameterized finite bound를 증명한다. 불가능하면 정확한 blocker와 다음 자료를 등록한다.

완료조건은 1차 자료 provenance와 locator 확보, local-factor 수식 감사, lower-bound 경로 판정, 문서·기계 원장·필요 코드/테스트 갱신, 전체 검증, 새 handoff 작성이다.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | Maynard의 g, n_j, W_i, e_i 정의와 각 local factor를 원문 식에서 유도한다. |
| 데이터 provenance | MEDIUM | 새 논문은 URL·버전·취득시각·SHA-256·page/equation을 기록한다. |
| empirical 데이터 | NONE | maximal-gap dataset과 기존 actual 결과는 읽거나 재계산하지 않는다. |
| 승인 경계 | MEDIUM | 문헌·수식·toy/exact symbolic 검증만 수행하고 actual 계산은 하지 않는다. |
| 재현성 | HIGH | 수식 원장과 fail-closed test로 숫자 없는 bound가 threshold-ready가 되지 않게 한다. |
| 문서 파급 | HIGH | theory 19, 상위 H1b 원장, METHODS, AGENTS, handoff 상태를 근거에 맞게 동기화한다. |

## 단계 현황

1. COMPLETED — Maynard 원정의와 source graph 추적
2. COMPLETED — 네 종류 local factor의 exact algebra와 최악값 감사
3. COMPLETED — explicit Mertens/totient-product 1차 자료 감사
4. COMPLETED — parameterized lower bound와 route 가치 판정
5. COMPLETED — 정본·기계 원장·테스트 갱신
6. COMPLETED — 전체 검증·handoff·원장 완료 처리

## 단계별 기록

### 2026-09-07 13:41 KST — 작업 시작

- 최신 handoff와 H1b-1b-2 9-node 원장을 확인했다.
- 시작 상태: 활성 비-done 원장 0개, git status clean.
- 기존 경계: absolute transfer factor 2와 Lemma 8.2 multiplier 89는 유지되며 relative normalization, SIV-07, X_cert는 OPEN이다.
- 다음 재개점: Maynard source의 Lemma 8.4에서 g(p), W_i, e_i가 유입되는 상위 정의와 실제 응용을 추적한다.

### 2026-09-07 13:48 KST — 1차 자료 취득·시각 확인

- sandbox 내부 네트워크 호출은 연결 실패했고, 사용자 승인에 따른 동일 URL 외부 호출로
  Dusart arXiv:1002.0442와 Rosser--Schoenfeld DOI PDF를 취득했다.
- 취득 UTC: `2026-09-07T04:48:29Z`.
- SHA-256:
  - Dusart: `3f11eca84613ad00e6a447f99b318d5c3d76e360283efcc6d3eebdda25ff3923`
  - Rosser--Schoenfeld: `8e37b06f82e09421bceb2502578c47b61469141f0287e6acedb70e01765ab556`
- PDF page 11의 Dusart Theorem 6.12와 PDF page 9(인쇄면 72)의
  Rosser--Schoenfeld Theorem 15, (3.41)--(3.42)를 텍스트 추출과 page render 양쪽으로 확인했다.
- MiKTeX `pdftotext`는 사용자 로그 디렉터리 접근 거부 경고를 냈으나 텍스트 파일은 생성됐다.
  식 확인은 bundled `pypdf` 추출과 Poppler render로 독립 재확인했으므로 수식 판독에는 영향이 없다.

### 2026-09-07 13:54 KST — Maynard actual-call 전수 추적과 핵심 대수

- Maynard TeX 542--604행의 Lemma 8.4와 실제 호출부 620, 737, 752, 885,
  905, 995, 1015, 1096, 1135, 1232행을 대조했다.
- 실제 분모의 prime-local 형태는 다음 네 family로 덮인다. 여기서 `a`는 해당
  root-count upper bound이고 현재 단계 이전의 허용 좌표 수는 `n_j<=a-1`이다.
  - `p-a`
  - `(p-a)^2/(p-1)`
  - `(p-a)^2/(p+a-2)`
  - `p-a-(a-1)/(p-1)`
- 네 family 모두 `0<g(p)<=p-a`다. 따라서 비제외 소수에서는
  `g(p)+n_j(p)<=p-1`이고 local factor가 exact하게 1 이상이다.
- 제외 소수 집합을 `Q_j=W_{j+1} product_{i=j+2}^r e_i`의 소인수로 묶으면
  `c_gamma_j >= phi(Q_j)/Q_j`다. 따라서 작은/큰 제외 소수를 별개 Mertens tail로
  처리할 필요가 없다.
- 이 결론은 추상 가정 `g(p)=p+O(k)` 전체에는 적용하지 않고, Maynard Section 8의
  추적된 actual call에만 적용한다.

### 2026-09-07 13:56 KST — 숨은 `R^{O(k^2)}`의 명시적 상계

- TeX 385, 389, 396--407의 `W_j` 구성과 계수 제한 366행을 이용했다.
- 모든 `W_j`의 prime support는 `WB`와
  `D=product_i |a_i| product_{i!=l}|a_i b_l-b_i a_l|`의 소인수 안에 있다.
- `|a_i|,|b_i|<=x^alpha`, `B<=x^alpha`, `R>=x^(theta/10)`에서
  다음 parameterized upper bound를 얻었다.

  `W_j <= (2k^2)^(2k^2) 2^(k(k-1)) R^[10 alpha (2k^2-k+1)/theta]`.

- 각 남은 `e_i<=R`이므로 `Q_j`의 로그 상계 `Lambda_j`도 숨은 O 없이 쓸 수 있다.
- Rosser--Schoenfeld의 모든 `n>=3` totient bound와 `Q_j>=210`을 결합하면
  `c_gamma_j > 1/[3(1+log Lambda_j)]`라는 느슨하지만 완전 명시적인 uniform
  lower bound를 얻는다. Dusart Theorem 6.12는 더 약한 primorial fallback으로 보존한다.
- 다음 재개점: 이 증명을 정식 문서·기계 계약·회귀검사에 옮기고, relative error에는
  `1/c_min=O(log log R)` 손실이 추가됨을 반영해 route 상태를 fail-closed로 갱신한다.

### 2026-09-07 14:20 KST — 하위 정리와 상위 원장 동기화

- 신규 정식화 `docs/method/theory/20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md`,
  기계 계약, 데이터 비의존 exact-rational 검사 모듈과 단위시험을 작성했다.
- H1b-1b-2, H1b-1, H1b, H1, T1, METHODS, 이론 색인과 AGENTS의 상태를 동기화했다.
- actual-call 하한 route만 `PROJECT_PARAMETERIZED_EXPLICIT`으로 올리고,
  추상 `g(p)=p+O(k)`, `C3_abs`, corrected r-fold, `SIV-07`, `X_cert`는
  fail-closed로 유지했다.
- 원문 정의를 재대조했다. 작은 소수 `p<=2k^2`는 `p`가 `B`를 나누지 않으면
  `W`에, 나누면 `B`에 들어가므로 `WB|W_i`; 따라서 `k>=2`에서 `Q_j>=210`이다.

### 2026-09-07 14:24 KST — 1차 표적검증과 교정

- `py_compile`과 theory data JSON 10개 parse는 PASS했다.
- 첫 표적 unittest는 42건 중 41건 PASS, 1건 FAIL이었다.
- 실패 원인: 수학·코드 오류가 아니라 테스트가 문자열 `6C3_abs`를 찾았지만
  정본은 명확한 곱셈 표기 `6*C3_abs`를 사용한 기대값 불일치였다.
- 조치: 정본을 유지하고 테스트 기대 문자열을 `6*C3_abs`로 수정했다.
- 다음 재개점: 동일 표적 suite를 재실행한 뒤 전체 unittest와 정적 감사를 수행한다.

### 2026-09-07 14:45 KST — actual-call 범위 과잉 일반화 발견과 fail-closed 교정

- 최종 원문 호출부 전수 재검토에서 기본 `W_j` 외에 실제 Lemma 8.4 호출에
  `dW_j`, `W'_j=rad(W_j(a_jb_m-a_mb_j))`, `a_mWBr`, `rW_m`,
  `W_0=DVDelta_L` 같은 추가 제외 인자가 있음을 확인했다.
- 기존 초안의 `Lambda_j`는 canonical/base `W_j` 부분만 명시적으로 덮으며, 이 추가 인자를
  모두 덮는다는 주장은 과잉 일반화였다.
- 교정 범위:
  - 네 actual local denominator family와 비제외 factor 1 이상 정리는 유지
  - effective `Q`에 대한 `phi(Q)/Q` 환원은 유지
  - base `Lambda`와 application overhead를 분리
  - 코드의 `application_log_overhead`를 필수 인수로 지정하여 암묵적 0 금지
  - H1b-1b-2a와 모든 상위 문서·JSON·테스트를 application overhead OPEN으로 동기화
  - `SIV-07`, `X_cert`는 계속 OPEN
- actual 계산·기존 empirical 결과에는 영향이 없다. 오류 원장 E023에 공개적으로 기록했다.

### 2026-09-07 14:48 KST — 교정 후 표적 회귀검사

- 교정 뒤 표적 suite 첫 실행은 새 상태 문자열
  `PARAMETERIZED_EXPLICIT_APPLICATION_INPUT_OPEN`이 status vocabulary에 없어서 43건 중
  1건 FAIL했다.
- 해당 상태의 뜻을 vocabulary에 명시한 뒤 같은 표적 suite를 재실행했고
  `Ran 43 tests ... OK`를 확인했다.

### 2026-09-07 14:52 KST — 최종 전체·정적 검증

- 고정 FGKMT Python으로 전체 unittest를 정상 로컬 권한에서 실행:
  `Ran 260 tests in 34.353s — OK`.
- 신규 source와 test의 `py_compile` PASS.
- 상위·하위 theory JSON 7개를 PowerShell JSON parser로 재검증해 모두 PASS.
- universal closure, `SIV-07 EXPLICIT`, `X_cert CLOSED` 과장 패턴 검색 0건.
- `git diff --check` exit 0. LF→CRLF 경고는 작업트리 line-ending 안내이며 whitespace 오류가 아니다.
- Rosser--Schoenfeld와 Dusart PDF의 SHA-256을 원장 값과 재대조했다.

### 2026-09-07 14:54 KST — handoff와 완료 상태 고정

- 신규 handoff:
  `handoff/202609071454_HANDOFF.md`
- handoff에 닫힌 local-factor 정리, application-overhead OPEN 교정,
  source provenance, 260/260 검증, 다음 연구 순서·예상시간·사용자 절차,
  한국어 커밋 메시지를 모두 기록했다.
- actual prime sweep, threshold calculator, commit/push/PR은 수행하지 않았다.
- 현재 사용자에게 필요한 설치·실행 절차는 없다.

## 현재 재개점

작업 완료. 다음 세션은 handoff의 1순위인 actual application-exclusion inventory에서 시작한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] source provenance와 exact locator 기록
- [x] 수식 유도와 상태 승격을 분리
- [x] 자동 검증과 실제 실험 상태 분리
- [x] 정본·상위 원장·AGENTS/METHODS 동기화
- [x] 새 timestamp handoff 작성
- [x] git diff --check와 참조 경로 확인
- [x] 파일명을 -done.md로 변경
