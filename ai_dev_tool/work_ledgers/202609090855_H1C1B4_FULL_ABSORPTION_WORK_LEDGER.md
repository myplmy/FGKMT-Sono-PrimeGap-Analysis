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
2. **COMPLETE — explicit prime-density·source-normalization 선행연구 조사**
3. **IN_PROGRESS — 12항·count-transfer full absorption 수학 판정 및 하위 gate 분해**
4. **IN_PROGRESS — machine contract·helper·negative-control·회귀시험 작성**
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

### 2026-09-09 10:28 KST — H1c-1b.4b density·c0·c1 증명 작성

- Rosser--Schoenfeld 1962 Corollary 3 식 (3.8), p. 69의
  `pi(2T)-pi(T)>3T/(5log T)` (`T>=20.5`)를 채택했다. source의 `(T,2T]`와 actual
  `[T,2T)` 차이로 prime atom 1을 빼고, `log T>=36^5`에서
  `1/T<1/(10log T)`를 elementary exponential series로 흡수해
  `P_T>T/(2log T)`를 얻었다.
- Rosser--Schoenfeld Theorem 12의 `psi(113)/113<1.03883`과 exact rational
  log/atan series enclosure로 Bordignon `c0<49`를 증명했다. 산출 rational upper는
  `1622314618240/33191449137 = 48.8774868353...`이다.
- `log(1+u)<u`와 `sum_(n>=2)1/[n(n-1)]=1`로 `c1<e<3`을 증명했다.
- Dusart 2010 Theorem 6.9 식 (6.6)은 independent pointwise cross-check로만 등록하고,
  더 직접적인 Rosser--Schoenfeld interval theorem을 canonical path로 선택했다.
- 첫 source-hash 회귀에서 PowerShell 표의 잘린 경로를 보고 Rosser와 Dusart PDF hash를
  서로 바꿔 적어 1건 FAIL했다. 각 contract path를 직접 hash하는 test가 이를 검출했고,
  Rosser=`8e37...ab556`, Dusart=`3f11...f3923`으로 즉시 교정했다.
- 새 helper·JSON·문서·tests를 실행했다. H1c-1b.4b 7/7, 4a+4b 통합
  13/13 unittest, `py_compile`, `git diff --check` 모두 PASS했다. 이값은 exact
  rational witness와 source hash를 재검산하고, `X_cert` 또는 H1(2)를 과승격하지 않는
  fail-closed flag를 확인한다.
- 다음 재개점: 12항·count-transfer에서 허용되는 `C_A` budget을 유도하되,
  고정 \(r\) 점검을 growing-\(r\) 전 구간 증명으로 과장하지 않도록 차원 bin의 양끝을
  모두 포함한다.

### 2026-09-09 11:42 KST — H1c-1b.4c conditional absorption budget 완료

- `L=log T`, `ell=log L`, `n=100r^2`, `A=n+10`으로 두고 exact density target을
  `S_pi/T <= 1/(2 L^(n+1))`로 정규화했다. Abel factor의 안전한 상계
  `K(L)<=4/L`를 써 12개 Bordignon term과 prime-power·endpoint를 하나의 scale로
  옮겼다.
- 미해결 4번 term을 분리해
  `normalized_error <= B0(r,L) + kappa(r,L) C_A`,
  `kappa=36(1+A log L)L^(-6)`,
  `C_allow=(1-B0)/kappa`를 유도했다. `B0`는 non-`C_A` source term 11개와
  count-transfer 2개를 합친 정확히 13개다.
- exact rational corner check와 항별 단조성으로 모든
  `r>=500,000,000`, `r^5<=L<(r+1)^5`에서 13개 normalized non-`C_A` term이
  각각 `exp(-500)`보다 작고, `log(kappa)<-536`임을 증명했다.
  따라서 `C_A<=exp(500)`이면 총 normalized error는 `1/2`보다 작다.
- corner 100-dps 회귀값은
  `log(B0)=-542.3720945610...`, `log(kappa)=-548.0479582683...`,
  `log(C_allow)=548.0479582683...`(약 `10^238.0142`)다. 이는 proof 최소 cutoff가
  아닌 회귀진단이다.
- 첫 test에서 44자리 `r^5`와 `(r+1)^5`를 default 15-digit `mpmath`로
  먼저 변환해 bin boundary가 같은 값처럼 떨어지는 구현 오류를 검출했다.
  integer는 변환 전 exact 비교, 비정수·로그 계산은 내부 80-dps로 고정했고
  4c 표적 test 6/6과 4a--4c 통합 36/36이 PASS했다.
- 판정은
  `NON_C_ABSORPTION_AND_CONDITIONAL_C_A_BUDGET_CLOSED_SOURCE_C_A_OPEN`이다.
  source가 `C_A<=exp(500)` 또는 exact `C_allow` envelope를 만족함을 증명하지
  않았으므로 H1(2), P9.2, `SIV-08`, `X_cert`는 모두 OPEN이다.
- 다음 재개점: H1c-1b.4d에서 Theorem 3.4·zero-density 식 (28)--(32)를
  final target에서 직접 재합성하고, source-derived `C_A` 성장률을
  `C_allow ~ r^28/log r`와 비교한다.

### 2026-09-09 12:24 KST — H1c-1b.4d source 재증명 범위·보수화 고정

- NYJM 최종판 Theorem 3.4의 열 개 `R*` summand, 식 (28)--(32), arXiv author
  source와 Liu--Wang 2002 원출처의 Theorems 1--2·Table 1·Tables 3--5를 다시 대조했다.
  Liu--Wang의 DOI는 `10.4064/aa102-3-5`이고, Bordignon에 전사된
  `0.26213`, `0.2067` 및 conditional pair table은 원출처와 일치한다.
- 첫 판독 때 arXiv v1 식 (31)에 `q`가 없는 것을 최종판에도 없는 것으로 잘못 판단했다.
  최종 NYJM판 인쇄 p.1431을 확대 재대조하니 식 (31)은 정확히 `2q`를 포함한다.
  따라서 project 재증명은 최종판의 `2q`를 전부 보존하고, `q`가 빠진 arXiv v1 식을
  배제한다. 이 즉시 정정으로 low-zero 계수는 초안보다 2배 커졌지만 cutoff 판정에는
  영향이 없다. 이 판독 실수와 수정은 숨기지 않고 review·오류 기록에 남긴다.
- Corollary 4.3은 알려지지 않은 “어떤 `i=1,...,6`”을 준다. 따라서 `i=6`을 임의로
  선택하지 않는다. `J=0`은 각 `min_J`의 합법적 upper 후보로 쓰고, 여섯 `i` 전체에서
  가장 작은 lambda `0.16=4/25`를 high-zero 공통 감쇠율로 쓴다. `Sigma_0`에는 모든
  `i`에서 `max(xi_(i+1),nu_1)=0.26213`이므로 `26213/100000`을 쓴다.
- actual count target의 `q=1` centered discrepancy는 정확히 0이므로 별도로 제거한다.
  source 재증명은 `q>=2`만 다뤄 `log q` 분모를 잘못 사용하지 않는다.
- `L=log x`, `ell=log L`, `A=100r^2+10`, `B=A ell`, contour height
  `H=L^(2A)`로 기호를 분리했다. `q<=L^A`, `log(qH)<=3B`를 사용한다.
  Theorem 3.4의 각 항을 직접 상계하면 corrected target 상수의 열세 component를 얻는다:
  explicit-formula remainder 9개, low-zero 1개, `Sigma_0` 1개, high-zero 두 branch다.
- `r=500,000,000`에서는 high-zero 지수상계가 허용량보다 클 수 있어 H1c-1b.4c의
  conditional cutoff를 그대로 unconditional cutoff로 승격할 수 없다. 반면
  `r>=10,000,000,000`에서는 corner에서 `115<ell<120`이고, 모든 13개 component의
  log upper를 `-100` 아래로 보낼 충분한 여유가 있다. 고정 `A`에서 `L` 증가 및 차원
  corner 증가에 대한 미분 부호를 별도로 증명해 전 범위를 덮을 예정이다.
- 다음 재개점: 위 13개 bound와 exact corner/monotonicity witnesses를 helper·tests로
  구현하고, `C_A<13e^-100<1` 및 H1c-1b.4c의 `C_A<=e^500` 조건을 실제로 닫되
  parent H1(2) 승격은 별도 H1c-1b.4e composition audit까지 보류한다.

### 2026-09-09 13:37 KST — H1c-1b.4d source constant 재증명 완료

- `source/h1c1b4d_source_constant_reproof.py`에 최종 Theorem 3.4 remainder 9개와
  식 (29)--(32) zero component 4개, 총 13개 log upper를 구현했다. 최종판 식 (31)의
  `2q`, unknown Liu--Wang `i`의 전 경우 최대화, `q=1` exact centered 분리를 보존했다.
- exact rational corner와 calculus certificate는 모든
  `r>=10,000,000,000`, `L=log x>=r^5`에서 각 component가 `exp(-100)`보다 작음을
  확인한다. 특히 첫 corner의 dimension-direction derivative dominance와 이후 증가비율
  `r/(log r)^2`, `sqrt(r)/log r`를 함께 등록했다.
- 따라서 corrected source constant는 `C_A<13 exp(-100)<1`이고, 같은 corner의
  H1c-1b.4c 허용량 `log C_allow=631.7890814632...`에 들어간다. 수치 회귀상
  `log C_A<-105.9189142777...`이며 최대 항은 `R2+R3` component다.
- `r=500,000,000`에서는 zero component 네 log upper가 모두 큰 양수이므로 4c의 더 작은
  conditional cutoff를 source closure에 재사용하지 않았다. `10^10`은 proof 편의를 위한
  보수적 cutoff이며 최소성 주장이 아니다.
- 정본 문서 41, review 47, JSON machine contract, helper와 8개 test를 작성하고 이론 색인
  71--72를 연결했다. review에는 arXiv v1을 최종판으로 잘못 읽었던 초기 실수와 최종
  `2q` 재확인·교정을 명시했다.
- H1c-1b.1--4d 회귀 65/65, 4d helper/test `py_compile`, `git diff --check`, 금지
  base-log·잘못된 약칭 정적검사가 PASS했다. 실제 소수 계산은 수행하지 않았다.
- 이 단계 판정은
  `CORRECTED_SOURCE_C_A_REPROOF_CLOSED_ABOVE_R_1E10_PARENT_COMPOSITION_PENDING`이다.
  H1(2), P9.2, `SIV-08`, `X_cert`는 H1c-1b.4e 전까지 OPEN이다.
- 다음 재개점: 이번 단계 파일만 명시 stage·local commit한 뒤 H1c-1b.4e end-to-end
  quantifier composition audit를 시작한다.

### 2026-09-09 14:28 KST — H1c-1b.3r1 actual FGKMT endpoint 교정 작성

- H1c-1b.4e 합성 전에 FGKMT 원문 Definition 2와 Section 8을 다시 대조했다. Maynard 원문
  Definition (2.1)은 \([T,2T)\)이지만 FGKMT printed p.95는
  \(\mathcal A(T)=\{T\le n\le2T\}\)로 재정의하고, printed p.101의 외부 소수집합은
  \((T,2T]\)이다. 기존 H1c-1b.3의 “actual target=[T,2T)” 판정은 잘못이었다.
- Bordignon/Abel source \((T,2T]\)에서 FGKMT closed target으로 갈 때는 (T) 소수 atom만
  더한다. centered correction은 modulus당 절댓값 1 이하라 기존 (M_B(T)) endpoint upper와
  H1c-1b.4c 수치 envelope는 보존된다. closed density는 source interval을 포함하므로
  H1c-1b.4b의 (T/(2\log T)) 하한도 보존된다.
- `source/h1c1b3r1_fgkmt_endpoint_correction.py`, 새 JSON contract, theory 42, review 48과
  독립 toy test를 작성했다. 기존 theory/review에는 actual-label 철회 notice를 붙이고 오류
  원장 E060에 원인·영향·재발방지를 기록했다.
- Section 8의 외부 \((T,2T]\) weighted sum으로 돌아갈 때 closed Theorem 6 합에서 lower
  endpoint weight를 제거하는 의무는 unweighted count correction과 다르므로 OPEN으로 유지했다.
- FGKMT Python으로 두 helper/test `py_compile`, 과거 H1c-1b.3과 새 r1 회귀 14/14,
  source PDF·predecessor hash 검증과 `git diff --check`를 모두 PASS했다.
- 다음 재개점: 이 교정 단계만 명시 stage·local commit한다. 그 뒤
  H1c-1b.4e에서 corrected closed target의 full absorption과 easy clauses를 합성한다.

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
