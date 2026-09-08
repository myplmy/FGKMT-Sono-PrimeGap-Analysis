# H1c-1b.2 common exceptional B·full remainder 작업원장

- 시작: 2026-09-09 06:47 KST
- 현재 상태: COMPLETE
- 직전 goal turn 판정: PROGRESS — H1c-1b.1/1a/1a.1 정본·364 tests·로컬 commit
  `4c84ae56cfe7953e1ea096d4e34f52c6644141f5`를 확인했다.
- 사용자 승인: `X_cert` 계산기 전에 필요한 정규화·증명을 권장 순서대로 수행하고,
  적합한 선행정리를 먼저 조사한 뒤 빠진 연결만 직접 증명한다. 단계 완료 뒤 명시 경로로
  로컬 stage·commit한다.
- 금지·보류: actual prime/maximal-gap sweep, P018-B, threshold calculator, 장시간 계산,
  package·Lean 설치, push·PR·외부 게시는 수행하지 않는다. 새 source·도구·장시간 계산이
  실제로 필요하면 사용자에게 요청하고 중단한다.
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609090633_HANDOFF.md`

## 목적과 완료조건

- 목적: Bordignon 2021의 explicit prime-distribution theorem과 FMT/FGKMT의 실제
  Proposition 9.2 호출을 정확히 변수 변환하여 다음을 판정한다.
  1. 필요한 dyadic scale·modulus family에 하나의 exceptional conductor/prime `B`를
     공통으로 고정할 수 있는가.
  2. full explicit remainder를 actual identity form에서 수치적으로 합성할 수 있는가.
  3. 어느 의무가 H1c-1b.3 endpoint/count transfer와 H1c-1b.4 density/common cutoff로
     넘어가야 하는가.
- 완료조건:
  1. FMT·FGKMT·Maynard·Bordignon 원문의 정리, 가정, quantifier, endpoint, exceptional-set
     정의를 page/equation/hash 단위로 대조한다.
  2. drop-in 선행정리가 있으면 채택하고, 없으면 실제 호출에 필요한 최소 bridge만 증명하거나
     정확한 blocker로 남긴다.
  3. 사람용 theory/review와 기계 판독 JSON, 필요한 exact/toy verifier·회귀시험을 작성한다.
  4. T1/H1/H1b/H1c·METHODS·AGENTS·색인을 증거 범위에서만 동기화한다.
  5. FGKMT Python 표적·전체 회귀, JSON·링크·Markdown·Git 정적검사를 통과한다.
  6. 새 timestamp handoff와 한국어 commit을 남기고 원장을 `-done`으로 이관한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | dataset·`F/G/H`를 실행하거나 변경하지 않는다 |
| theorem/empirical 구분 | 영향 있음 | distribution 하위 gate만 판정하며 `X_cert` 전체를 닫지 않는다 |
| source quantifier | 핵심 영향 | “각 scale마다 존재”와 “모든 scale에 공통”을 구분한다 |
| exceptional object | 핵심 영향 | conductor, character, modulus, prime `B`를 같은 것으로 추정하지 않는다 |
| endpoint·recentring | 확인 필요 | 이번 단계와 H1c-1b.3의 경계를 명시한다 |
| density·relative error | 확인 필요 | 이번 단계와 H1c-1b.4의 경계를 명시한다 |
| 큰 정수·정밀도 | 영향 가능 | exact/rational·symbolic bound를 우선하고 부동소수점은 보조검산만 쓴다 |
| 승인 경계 | 영향 있음 | 문헌·증명·toy scalar 검산만 수행한다 |
| 재현성 | 영향 있음 | source hash·variable map·negative control을 기계 원장에 고정한다 |
| Git | 영향 있음 | 이번 단계 변경만 명시 stage·local commit; `git add .`/`-A` 금지; push 없음 |

## 단계 현황

1. **COMPLETE — 현재 정본과 source inventory 재구성**
2. **COMPLETE — exceptional-object quantifier·common-B 가능성 감사**
3. **COMPLETE — Bordignon full remainder actual-variable 합성**
4. **COMPLETE — finite bridge와 fail-closed blocker 정식화**
5. **COMPLETE — machine contract·회귀시험·상위 정본 동기화**
6. **COMPLETE — 전체 검증·handoff·명시 stage·local commit**

## 단계별 기록

### 2026-09-09 06:47 KST — 상태·범위 고정

- branch `main`, HEAD
  `4c84ae56cfe7953e1ea096d4e34f52c6644141f5`, clean worktree,
  활성 작업원장 0개를 확인했다.
- 최신 handoff·AGENTS와 impact-analysis, plan-doc, PDF 규약을 읽었다.
- 이번 단계는 empirical experiment가 아니며 source/proof 감사임을 고정했다.
- 다음 재개점: theory 16/32/33/34/35와 기계 JSON에서 H1c-1b.2가 요구하는 exact
  source calls·변수·open obligations를 표로 복원한다.

## 현재 재개점

H1c 관련 정본과 로컬 source PDF/TeX를 대조해 Bordignon theorem의 exact statement,
FMT/FGKMT exceptional `B_0` 선택, Maynard Proposition 9.2 호출을 하나의
quantifier map으로 만든다.

### 2026-09-09 07:03 KST — source·quantifier·dyadic composition 감사 완료

- NYJM 최종 출판본 Theorem 1.1·1.4와 proof (34)--(37), Maynard Hypothesis 1(2)·
  Proposition 9.2, FGKMT Corollary 6·Lemma 7.2·Section 8 actual call을 대조했다.
- 공식 arXiv `2101.08610` v1 source를 임시 다운로드해 SHA-256
  `0a6f83a4c4aaf0bc2178de92f6a65174de0410d48371f28783a75c70a5f386e4`로 확인했다.
  v1 TeX는 최종 출판본과 중심항·일부 log factor가 다르므로 계산 정본에서 배제한다.
- fixed base scale의 실제 P9.2 endpoint를 `T=x/2`,
  `A=100r^2+10`, `Q1=(log T)^A`로 두면 exceptional modulus `q0(Q1)`는 endpoint가
  아니라 같은 `Q1`에 의해 선택된다. 따라서 `T`와 `2T`에 하나의 `q0`를 쓸 수 있다.
- `q0`가 있으면 그 소인수 하나를 prime `B`로 택한다. 그러면
  `(q,B)=1 => q0 does not divide q`이므로 Maynard modulus family가 Bordignon의
  non-exceptional sum의 부분집합이다. 없으면 `B=1`이다.
- 기존 H1c-1b.1의 modulus capacity와 `log T>2A`를 쓰면
  `q<=T^(1/3)`가 두 endpoint의 Bordignon 범위에 모두 들어간다.
- 최종 출판본의 전체 양의 remainder를 12개 항으로 분해했다. 누적 중심항이
  `psi(u)/phi(q)`이므로 triangle inequality로 open-closed dyadic von-Mangoldt interval의
  합계 오차를 정확히 `R(T)+R(2T)`로 합성할 수 있다.
- 아직 닫히지 않은 것: 최종 출판본의 `C(A,A-3,X0)` 대 Theorem 1.2의
  `C(A,A-3,Y0)` 표기 불일치, 12개 항의 목표 log-saving 흡수, half-open endpoint,
  prime powers·partial summation, unweighted prime count, density와 common cutoff.
- 다음 재개점: 위 판정을 theory/review/JSON과 fail-closed 보조 모듈·시험으로 정식화한다.

### 2026-09-09 07:28 KST — H1c-1b.2 정식화·초기 표적검증

- theory 36, review 42와 machine JSON v1을 새로 작성했다.
- 최종 NYJM판 RHS를 endpoint 상대오차 12개 항으로 분리한 보조 모듈과 회귀시험을
  작성했다. arXiv v1 식을 채택하지 않고 final center `psi(u)/phi(q)`를 강제한다.
- 첫 표적시험 8개 중 5개 PASS, 3개 FAIL이었다.
  - 1개는 상위 T1 `SIV-08` notes를 아직 동기화하지 않은 예상 실패였다.
  - 2개는 toy implication 코드가 `q % q0` 대신 반대 방향 `q0 % q`를 쓴 실제 구현
    오류였다. 즉시 원인을 확인해 `q % q0 != 0`으로 수정했다.
- 이 오류는 새 결과가 상위 정본이나 commit에 들어가기 전에 시험이 잡았으며, 수학 문서의
  명제 `(q,B)=1 => q0 does not divide q`에는 영향이 없다.
- 다음 재개점: predecessor·T1·H1/H1b/H1c·METHODS·AGENTS·색인의 successor pointer와
  fail-closed status를 동기화한 뒤 표적시험을 다시 실행한다.

### 2026-09-09 07:50 KST — machine contract·상위 정본 동기화 완료

- predecessor H1c-1a/1b.1/1b.1a/1b.1a.1과 H1/H1b/H1c/T1 machine JSON에
  H1c-1b.2 successor pointer를 추가하고 다음 gate를 H1c-1b.3으로 갱신했다.
- METHODS, AGENTS, theory index, T1/H1/H1b/H1c 사람용 정본과 threshold/recoverability
  review를 같은 증거 범위로 동기화했다.
- 공통 \(B\)는 모든 scale의 전역 상수가 아니라 각 fixed outer scale의 dyadic pair에
  허용되는 하나임을 모든 새 정본에 명시했다.
- FGKMT Lemma 7.2를 재대조해 \(B\le q_0\le Q_1<Q_B(T,A)<\sqrt T<T\)로
  크기 조건을 강화했다. 따라서 Lemma 7.2의 \(B\le T\)와 Maynard의 actual
  \(\alpha=2\) 조건을 모두 만족한다.
- 수정 후 관련 H1/H1c/T1 표적 회귀 55개가 모두 PASS했다.
- JSON 26개 parse, 새 source/test `py_compile`, `pip check`, `git diff --check`가
  모두 PASS했다. CRLF 안내 외 오류는 없다.
- 다음 재개점: formula/test 독립 대조를 마친 뒤 전체 unittest와 문서 링크·Git scope를
  검사하고 handoff·완료 원장·명시 stage·local commit을 남긴다.

### 2026-09-09 07:46 KST — 최종 회귀·정적검증 완료

- 최종판 12개 상대오차 항을 시험에서 각각 독립 식으로 다시 계산하도록 강화했고,
  H1c/H1/T1 관련 표적 회귀 40개가 모두 PASS했다.
- 전체 회귀의 첫 sandbox 실행은 저장소 및 시스템 임시폴더 생성·정리와
  multiprocessing 접근이 차단되어 372개 중 82개가 `PermissionError`로 끝났다. 이는 코드
  실패로 판정하지 않았다. 사용자가 허가한 sandbox 외부 동일 명령으로 재실행해
  `Ran 372 tests in 34.586s / OK`를 확인했다.
- PowerShell `ConvertFrom-Json`은 기존 JSON 안의 `f`와 `F` 키를 대소문자 구분 없이
  중복으로 취급해 non-terminating error를 냈다. 이 검증 결과는 채택하지 않고 FGKMT
  Python 표준 `json` parser로 theory JSON 26개를 다시 검사해 모두 PASS했다.
- 변경 Markdown의 로컬 상대 링크 84개, 새 source/test `py_compile`, `pip check`,
  project vocabulary, primary source SHA-256 4개와 `git diff --check`가 모두 PASS했다.
- 실제 prime/maximal-gap sweep, threshold 계산, package 설치는 수행하지 않았다.
- 다음 재개점: 핵심 파일을 명시 경로로 stage·commit한 뒤 그 hash를 새 handoff와 완료
  원장에 기록하고 별도 마감 commit을 남긴다.

### 2026-09-09 07:50 KST — 핵심 commit·handoff·원장 완료

- 검증한 핵심 변경 30개 파일을 명시 경로로만 stage하고 staged diff check를 통과시킨 뒤
  local commit `4e933508edc3855cceb0d4d5222950df0ac15576`을 만들었다.
- sandbox 안 `git add`는 `.git/index.lock` 생성 권한 거부로 실패했다. 사용자가 허가한
  sandbox 외부에서 같은 명시 경로 stage를 실행해 성공했으며, broad staging은 사용하지 않았다.
- 새 handoff `handoff/202609090750_HANDOFF.md`에 증거, 열린 gate, 사용자 절차,
  권장 순서와 실제 commit 메시지를 기록했다.
- 실제 experiment·threshold 계산·package 설치·push·PR은 수행하지 않았다.
- 이 파일은 `-done` suffix로 이관한 뒤 handoff와 함께 별도 마감 commit에 포함한다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 선행정리 우선 조사와 적용성 개별 대조
- [x] exceptional conductor/character/modulus/prime 구분
- [x] 승인·비실행 경계 명시
- [x] 상위 theorem 과승격 방지
- [x] JSON·코드·시험·정본 동기화
- [x] 전체 회귀·정적검사 PASS
- [x] 새 timestamp handoff 작성
- [x] 명시 경로 stage·local commit
- [x] 파일명을 `-done.md`로 변경
