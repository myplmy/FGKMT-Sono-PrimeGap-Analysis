# Sono/FMT H1c-1b.4 source normalization·density·full absorption 작업원장

- 시작: 2026-09-09 08:55 KST
- 현재 상태: IN_PROGRESS
- 직전 goal turn 판정: PROGRESS — H1c-1b.3 exact count transfer를 정본·검산 코드로
  닫고 381개 전체 회귀와 local commits
  `9b00eb8de461228f1988643575c28023430b2428`,
  `73c3c196d74d111fdb0cd988ed0ec01de995fa31`을 확인했다.
- 사용자 승인: `X_cert` 계산기 전의 정규화·증명을 권장 순서대로 진행하며, 필요한 lemma는
  원 논문·교정·후속 선행증명을 먼저 조사하고 실제 적용성을 개별 대조한 뒤 빠진 연결만
  직접 증명한다. 단계 완료 후 명시 경로로 local stage·commit한다.
- 중단 조건: 필요한 학술자료를 직접 확보할 수 없거나, Lean·새 Python package 또는
  장시간 계산이 실제로 필요하면 사용자에게 요청하고 일시 중단한다.
- 금지·보류: actual prime/maximal-gap sweep, P018-B, threshold calculator, 장시간 계산,
  임의 상수 선택, package 설치, push·PR·외부 게시.
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609090849_HANDOFF.md`

## 목적과 완료조건

- 목적: H1c-1b.2의 final-published Bordignon 12항과 H1c-1b.3 count-transfer 비용을
  Maynard Hypothesis 1(2)/Proposition 9.2의 exact denominator에 대해 한 finite cutoff로
  흡수할 수 있는지 판정한다.
- 반드시 판정할 항목:
  1. Bordignon final Theorem 1.2/1.4의 `C(A,A-3,X0/Y0)` 표기가 실제로 무엇을 뜻하며
     수치 upper를 복원할 수 있는가.
  2. actual \(P_T=\#\{p:T\le p<2T\}\)에 쓸 explicit lower bound와 정확한 유효범위.
  3. 12개 remainder 및 prime-power·endpoint 비용의 \((\log T)^{-100r^2}\) 흡수.
  4. growing \(r\), \(A=100r^2+10\), dyadic \(T=x/2\) 전체에 한 monotone cutoff가
     존재하는지.
  5. source 상수의 미명시·오자·순환의존이 남으면 어떤 최소 하위 gate로 분해해야 하는지.
- 완료조건:
  1. 원 출판본·저자 버전·교정·관련 explicit PNT/BV 문헌을 page/equation/hash 단위로 대조.
  2. drop-in 가능성과 실제 변수·범위·끝점·오류항을 개별 판정.
  3. 닫을 수 있는 유한 bridge와 닫을 수 없는 source constant를 명확히 분리.
  4. theory/review/JSON, fail-closed helper·tests와 상위 정본 동기화.
  5. FGKMT Python 표적·전체 회귀와 정적검사 PASS.
  6. 새 timestamp handoff, 완료 원장과 한국어 local commit.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | dataset과 `F/G/H`를 실행·변경하지 않는다 |
| theorem source constants | 핵심 영향 | 표기 모호성을 임의 숫자로 채우지 않는다 |
| exact denominator | 핵심 영향 | \(P_T\)를 PNT 근삿값으로 대체하지 않고 lower bound만 사용한다 |
| remainder absorption | 핵심 영향 | 12항과 H1c-1b.3 비용을 하나도 누락하지 않는다 |
| growing dimension | 핵심 영향 | fixed \(r=36\) 검산을 전 범위 증명으로 과장하지 않는다 |
| theorem/empirical 구분 | 영향 있음 | proof normalization만 수행하고 `X_cert`를 승격하지 않는다 |
| 승인·자원 | 영향 있음 | source/proof/toy만 수행; 장시간 계산은 사용자 요청 전 금지 |
| 문서·회귀 | 영향 있음 | H1/H1b/H1c/T1·METHODS·AGENTS와 machine contract를 함께 점검 |
| Git | 영향 있음 | 이번 단계 파일만 명시 stage; broad add, push, PR 금지 |

## 단계 현황

1. **COMPLETE — 현재 정본·Bordignon 상수 표기와 actual target 재구성**
2. **IN_PROGRESS — explicit prime-density·source-normalization 선행연구 조사**
3. **PENDING — 12항·count-transfer full absorption 수학 판정 및 하위 gate 분해**
4. **PENDING — machine contract·helper·negative-control·회귀시험 작성**
5. **PENDING — H1/H1b/H1c/T1·METHODS·AGENTS·색인 동기화**
6. **PENDING — 전체 검증·handoff·명시 stage·local commit**

## 단계별 기록

### 2026-09-09 08:55 KST — 상태·범위 고정

- branch `main`, HEAD `73c3c196d74d111fdb0cd988ed0ec01de995fa31`, clean worktree와
  활성 작업원장 0개를 확인했다.
- 직전 H1c-1b.3은 actual \([T,2T)\) unweighted prime count와 exact center까지
  quantity normalization을 닫았지만 relative rate·density·full absorption은 열어 두었다.
- 이번 단계는 실제 실험이 아니라 source/proof normalization이다.
- 다음 재개점: Bordignon final PDF와 기존 12항 전사에서 `C`, `X0`, `Y0`, `A`의
  정의·정리 간 전달을 재구성하고, source 자체로 numerical constant를 얻을 수 있는지 판정한다.

### 2026-09-09 09:32 KST — Bordignon 상수 표기·직접 대수 재구성

- 최종 NYJM판 SHA-256
  `4bd7adf499ba667647b612a61399f0f86c272bc684718630fcde42983c014029`과
  arXiv v1 source tar SHA-256
  `0a6f83a4c4aaf0bc2178de92f6a65174de0410d48371f28783a75c70a5f386e4`를
  고정해 Theorem 1.2, Lemma 3.1, Theorem 3.4, 식 (28)--(33), Theorem 1.4와 식 (35)를
  대조했다.
- 두 버전 모두 Theorem 1.2에서 `Y0=log log X0`라 정의하지만 상수의 supremum 하한을
  `x>=Y0`로 인쇄한다. Theorem 1.4와 식 (35)는 세 번째 인자를 `X0`로 인쇄한다. 따라서
  threshold형 인자를 `X0`와 `Y0`로 분리한 project notation이 필요하다.
- 더 중대한 문제: 최종 식 (33)의 첫 항은
  `R*(x,T,q) log log x / log^2 x`다. Theorem 3.4의 `R*`는 절대오차이며 그 식에는
  `sqrt(x)`와 `x/(T-1)` 크기 항이 들어 있으므로, 이 표현은 `x` 정규화가 없어
  `x>=...` supremum의 유한 상수를 정의하지 못한다.
- arXiv v1은 `R*(x,T,q) T/(x log^2 x)`를 인쇄한다. 이것은 dimensionless이지만,
  최종 Lemma 3.1의 `x log x log log x/T` 개선식과 바로 동일한 정규화는 아니다.
  따라서 v1을 조용히 최종식으로 대신하지 않는다.
- Theorem 1.2의 exact target에서 직접 대수를 다시 하면 per-character explicit-formula
  remainder의 필요한 contribution은
  `q * R*(x,T,q) * log^(alpha2)(x) / x`다. `q<=log^alpha1(x)`를 쓰면
  `R*(x,T,q) log^(alpha1+alpha2)(x)/x`, 그리고
  `T=log^(alpha1+alpha2+3)(x)`를 쓰면 `R*T/(x log^3 x)` 이하이다.
  이것은 출판 식 (33)을 그대로 복사한 것이 아니라 표시된 Theorem 3.4와 target에서
  새로 유도해야 하는 project correction이다.
- NYJM 공식 페이지, 출판 PDF, arXiv record/source와 표적 검색에서 별도 erratum이나
  저자 계산 코드를 찾지 못했다. 이는 전 세계 비존재 주장이 아니다.
- 결론: `X0/Y0` type normalization은 안전하게 정식화할 수 있으나, growing
  `alpha1=A=100r^2+10`에 필요한 numerical `C_A`는 출판 식 (33)만으로 가져올 수 없다.
  Theorem 3.4의 모든 항을 이용한 별도 상계 재증명이 필요하다.
- 다음 재개점: source-normalization을 fail-closed 정본으로 남기고, 독립적으로 닫을 수 있는
  half-open prime-density 및 `c0,c1` 상계를 원 출처와 대조한다.
- 첫 표적 회귀에서 arXiv source tar hash와 그 안의 개별 `PNTPAP1.tex` hash를 혼동해
  1건 FAIL했다. 개별 파일의 실제 SHA-256
  `42fe4180861d13f5e02b1c43d6b85ce5956f97c7a75616757f21ff00c1f648a9`로 즉시 교정했다.
  archive hash는 별도 metadata로 유지한다.

### 2026-09-09 09:54 KST — H1c-1b.4a 정본·fail-closed 검산 완료

- `38_...source_normalization.md`, review 44, JSON contract, 검산 모듈과 6개 회귀시험을
  작성하고 theory index 65--66을 연결했다.
- 표적 unittest 6/6 PASS, 두 Python 파일 `py_compile` PASS, 새 문서의 금지 base-log·FGMT
  정적 검색 0건을 확인했다.
- 판정은 `TYPE_MAPPING_AND_DIRECT_REMAINDER_ALGEBRA_CLOSED_NUMERICAL_C_A_BLOCKED`다.
  인쇄식이나 v1 식에서 수치 `C_A`를 요청하면 helper가 의도적으로 예외를 발생시킨다.
- 다음 재개점: Rosser--Schoenfeld direct interval lower bound와 Bordignon `c0,c1`의
  elementary upper를 H1c-1b.4b로 정식화한다.

## 완료 전 점검

- [ ] 사용자 요청 범위의 산출물 완료
- [ ] 선행정리 우선 조사와 actual 적용성 대조
- [ ] source constant 표기와 provenance 고정
- [ ] exact prime-density lower bound 확보 또는 blocker 명시
- [ ] 12항·count-transfer 비용 누락 없는 absorption 판정
- [ ] growing-dimension·common-cutoff 검증
- [ ] 상위 theorem 과승격 방지
- [ ] JSON·코드·시험·정본 동기화
- [ ] 전체 회귀·정적검사 PASS
- [ ] 새 timestamp handoff 작성
- [ ] 명시 경로 stage·local commit
- [ ] 파일명을 `-done.md`로 변경
