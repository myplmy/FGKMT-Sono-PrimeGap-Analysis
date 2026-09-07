# H1b-1b-2c actual 공통 입력 특수화 작업원장

- 시작: 2026-09-08 06:10 KST
- 현재 상태: IN_PROGRESS
- 사용자 승인: 권장 작업 순서에 따른 H1b-1b-2c 착수, 필요한 학술자료 조사·취득, 적합한 선행증명 우선 감사 후 부족분의 최소 직접증명
- 금지·보류: actual prime sweep, threshold calculator, 장시간 수치실험, 상수의 추측 대입, Lean·추가 Python 패키지 설치, commit/push/PR
- 선행 변경: 시작 시 `git status --short` 0건(clean). 직전 H1b-1b-2b 작업은 저장소에 반영된 상태이며 이번 작업에서 임의로 되돌리지 않는다.

## 목적과 완료조건

- 목적: Maynard Section 8의 11개 analytic subapplication에 대해 교정된
  \(\kappa=1\) Wirsing multiplier 정리에 넣을 하나의 공통 실제
  \(a,A_2,L\) package를 문헌과 원문에서 복원·인증할 수 있는지 판정한다.
- 완료조건: 각 적용의 \(\gamma(p)\), 제외소수, prime-sum 가정, 변수 대응을 고정하고,
  선행 정리 적용성 표와 공통 상수 후보의 엄밀한 증거를 작성한다. 완전 인증이 불가능하면
  정확히 어느 입력·cutoff·전달 정리가 비어 있는지와 다음 최소 작업을 남긴다. 근거가 있는
  child node만 상위 정본에 승격하고 `SIV-07`, `X_cert`는 전체 의무가 닫히기 전까지 OPEN으로 둔다.

## 문헌 우선 전략의 비판적 판정

| 제안 요소 | 판정 | 이번 작업의 적용 방식 |
|---|---|---|
| 이미 증명된 lemma를 먼저 조사 | 타당 | 중복 증명을 피하고 source/page/equation까지 고정한다. |
| 이름이나 결론이 비슷한 정리를 그대로 사용 | 부적합 | 가정, 변수 정규화, uniformity, finite cutoff, 상수 의존성을 개별 대조한다. |
| 정확히 맞는 선행 정리가 없을 때 직접 증명 | 타당 | 현재 11개 적용에 필요한 최소 명제만 정식화한다. |
| 여러 논문의 부분식을 연결해 암시적 상수를 숫자로 간주 | 부적합 | 전달 단계마다 explicit bound가 없으면 OPEN으로 유지한다. |
| 실험·수치 fitting으로 proof constant를 대체 | 부적합 | 진단에는 쓸 수 있어도 theorem certificate에는 쓰지 않는다. |

따라서 `목표 가정 고정 → 선행문헌 탐색 → 적용성 감사 → 부족분만 직접증명 → exact 계약 검증`
순서를 사용한다. 이 방식은 효율과 신뢰성을 함께 높이지만, “선행논문에 있다”는 사실 자체는
적합성 증명이 아니므로 각 적용을 별도로 검사한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 반복로그·end-bounded empirical 정의 | 영향 없음 | maximal-gap 데이터와 `F/H`를 읽거나 재계산하지 않는다. |
| Sono/FMT proof chain | HIGH | application별 입력, 공통 majorant, r-fold 합성을 분리한다. |
| 문헌 provenance | HIGH | 원문 URL/DOI/arXiv, 판본, local SHA-256, page/line을 기록한다. |
| 수치 엄밀성 | HIGH | exact integer/rational 또는 증명된 directed bound만 certificate에 사용한다. |
| 승인 경계 | MEDIUM | 문헌·정리·toy/exact 검증만 수행하며 actual 실험과 설치는 하지 않는다. |
| 산출물·비덮어쓰기 | HIGH | 새 theory/review/contract/handoff를 만들고 기존 이력 문서를 덮어쓰지 않는다. |

## 단계 현황

1. **COMPLETED — 11개 actual application과 필요한 가정·변수 대응 재고정**
2. **COMPLETED — 선행연구·원문에서 공통 `a,A2,L` 제공 여부와 적용성 감사**
3. **COMPLETED — 부족분의 최소 직접 정식화 또는 정확한 blocker 분해**
4. **COMPLETED — 정본·기계 계약·필요 코드/시험 동기화**
5. **COMPLETED — 표적·전체 검증, 보고, 새 handoff와 원장 완료 처리**

## 단계별 기록

### 2026-09-08 06:10 KST — 착수·승인 경계·방법론 고정

- 수행: 최신 handoff의 첫 gate가 H1b-1b-2c임을 확인하고 clean worktree에서 새 원장을 생성했다.
- 선행 사실: H1b-1b-2b는 parameterized multiplier를 닫았지만 실제 공통
  \(a,A_2,L\), corrected r-fold composition, `SIV-07`, `X_cert`는 OPEN이다.
- 결정: 사용자의 문헌 우선 제안은 위 조건부 방식으로 채택한다. 완전 탐색의 부재를
  novelty 주장으로 바꾸지 않으며, 적합하지 않은 lemma를 강제로 연결하지 않는다.
- 다음 재개점: theory 21/22의 11개 application inventory와 Maynard `Subsets.tex`
  실제 call site를 대조해 각 \(\gamma(p)\)와 필요한 prime-sum inequality를 표로 고정한다.

### 2026-09-08 — 11개 application·네 local family 재고정

- 수행: Maynard source 531--604, 620, 737, 752, 885, 905, 995, 1015,
  1096, 1135, 1232행과 theory 20--22·두 기계 원장을 대조했다.
- 결과: 외부 call site 10곳, 1135행 이중 factor를 분리한 analytic subapplication
  11개를 재확인했다. 실제 prime denominator는
  `p-a`, `(p-a)^2/(p-1)`, `(p-a)^2/(p+a-2)`,
  `p-a-(a-1)/(p-1)` 네 family다.
- 핵심식: 비제외 소수에서
  \(\rho_p=\gamma(p)/p=1/(1+n_j(p)+g(p))\)이며,
  \(0\le n_j(p)\le a_p-1\), \(a_p\le k+1\), \(p>2k^2\)다.
  제외 소수에서는 \(\rho_p=0\)이고 effective excluded radical의
  \(\log Q\)는 theory 21의 application별 \(\Lambda_{j}\)로 덮인다.
- 불변식: 1135행의 `r_0` factor와 canonical `r`-vector factor를 합쳐 한 번의
  동일-scale 호출로 취급하지 않는다.
- 다음 재개점: Maynard·Ford·Dusart·Castillo 자료에서 이 네 family에 그대로 넣을
  수치 \(a,A_2,L\) package가 있는지 조사하고, 없으면 exact family 식에서 최소
  공통 부등식을 직접 유도한다.

### 2026-09-08 — 문헌 우선 적용성 감사 완료

- Maynard source SHA-256 `e55592f0d674e32ad6ef7d6fe25bce2a0aa3cfc712981ccf996a5df0a4d5b18e`의
  531--604행에서 목표 가정과 actual `gamma` 구조를 다시 확인했다.
- Rosser--Schoenfeld 1962 Theorem 6의 (3.21), (3.24)를 printed p.70 렌더링과
  SHA-256 `8e37b06f82e09421bceb2502578c47b61469141f0287e6acedb70e01765ab556`로 확인했다.
- Ford Theorem 4.4, Castillo et al. Lemma 2.5·Remark, Dusart explicit estimate를
  개별 대조했다. Dusart는 사용 가능하지만 모든 작은 구간을 한 식으로 덮는 이번 목적에는
  Rosser--Schoenfeld가 더 직접적이라 주 증명에 쓰지 않았다.
- 표적 검색에서 11개 실제 적용의 완성된 공통 package는 찾지 못했다. 전 세계 novelty는
  주장하지 않으며, 문헌이 직접 주지 않는 actual-family·endpoint·제외소수 연결부만 증명했다.

### 2026-09-08 — 최소 직접 lemma와 상수 package 정식화

- 네 actual family에서 exact하게
  `0 <= p-(1+n+g(p)) <= 3(root_count-1) <= 3k`를 얻었다.
- 비제외 소수에서 `rho<1/2`, `0<=rho-1/p<=12k/p^2`이고, 전 소수 correction은
  `k=2`와 `k>=3`을 나눠 모두 4 미만임을 증명했다.
- Rosser--Schoenfeld 누적합의 왼쪽 endpoint를 보정해 모든 실수 `2<=w<=z`에서
  `-7/2 < sum log(p)/p-log(z/w) < 4`를 얻었다.
- 제외소수 합은 `log Q<=Lambda_star`, `Q>=210`에서 `log Lambda_star+1` 미만이다.
- 결론: 공통 Maynard/Ford `a=1/2`, `A2=8`, `L=5+log(Lambda_star)`.
  교정 one-step multiplier는 약 `7.91726413329524e121`이고 추가
  `(6+log Lambda_star)`가 곱해진다.
- 정확한 제한: actual four-family 입력만 닫았다. corrected r-fold composition,
  smooth norm, `SIV-07`, `X_cert`는 OPEN이다.

### 2026-09-08 — 구현·정본 동기화

- 신규:
  - `source/h1b1b2c_actual_parameter_package.py`
  - `tests/test_h1b1b2c_actual_parameter_package.py`
  - `docs/method/theory/23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md`
  - `docs/review/29_20260908_H1b1b2c_actual_parameter_선행연구_적용성검토.md`
  - `docs/method/theory/data/Sono_FMT_H1b1b2c_actual_parameter_specialization_v1.json`
- 상위 `AGENTS.md`, `docs/METHODS.md`, theory 12/14/15/18--22와 관련 JSON·회귀시험을
  `H1B-L83=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 동기화했다. parent hard blocker는 유지했다.
- 표적 검증: 새 7 tests PASS. 연관 8모듈 46 tests PASS.
- 도구 실패: 미설치 `sympy`, 사용 불가 번들 `pdftotext`, 비정상 종료된 보조 합은 증거에서
  제외했다. 한 patch context 실패와 상태 기대값 회귀 실패는 수정 후 재실행했다. 상세는 오류
  원장 E027--E028이다.

### 2026-09-08 — 최종 검증·상태 정합성·핸드오프 완료

- 고정 FGKMT Python으로 신규 7 tests와 최종 관련 17 tests를 통과시켰다.
- 샌드박스 밖 전체 suite 최종 결과는 `Ran 278 tests in 32.799s` — `OK`다.
- 첫 샌드박스 전체 suite의 82 errors는 `TemporaryDirectory` 권한 오류였고 코드 실패로
  세지 않았다. 첫 샌드박스 밖 실행의 1 failure는 구형 `missing_numeric_inputs`
  불변식이었다.
- 이 실패를 조사하면서 실제 입력이 이미 닫힌 `H1B1-L83-GGPY4`,
  `H1B1-L84-GAMMA`, `H1B1-L84-L` 하위 상태가 덜 동기화된 것을 발견했다.
  세 행만 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` 의미로 교정하고 parent
  `H1B-L84`, `H1B1-PACKAGE`, `SIV-07`, `X_cert`는 OPEN/HARD_BLOCKER로 유지했다.
- 신규 module/test `py_compile` PASS, theory JSON 13/13 FGKMT Python 엄격 파싱 PASS,
  변경 텍스트 34개 UTF-8·제어문자 PASS, stale current wording 0건,
  `git diff --check` exit 0을 확인했다.
- PowerShell `ConvertFrom-Json`의 기존 대소문자 충돌(E026)을 최종 감사에서 한 번
  반복했다. 거짓 PASS나 파일 영향은 없고 Python `json`으로 재검증했으며 E026에
  재발을 기록했다. Windows `rg` wildcard 경로 오류는 E027에, 구형 시험·하위 상태
  동기화 누락은 E028에 추가했다.
- 마지막 보조 검사에서 `core.autocrlf=false`를 사용해 기존 CRLF를 후행 공백으로 오판한
  읽기 전용 오류는 E029에 기록하고 해당 결과를 폐기했다. 최종 판정에는 프로젝트 기본
  Git 설정의 `git diff --check`만 사용했다.
- 새 핸드오프: `handoff/202609080716_HANDOFF.md`.
- 실제 소수 실험, threshold calculator, commit, push, PR은 수행하지 않았다.

## 현재 재개점

이번 H1b-1b-2c 작업은 완료됐다. 다음 세션은 별도 원장을 만들고 H1b-1b-2d에서
Maynard Lemma 8.4의 actual smooth norm과 corrected r-fold error composition을
문헌 우선으로 감사한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 문헌 우선 적용가능성 매트릭스 완료
- [x] source locator·hash·변수 대응 고정
- [x] 닫힌 상수와 RATE/RANGE blocker 분리
- [x] actual 실험·threshold 미실행 경계 명시
- [x] 정본·상위 원장·AGENTS/METHODS 동기화
- [x] 고정 FGKMT Python 표적·전체 검증
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
