# FGKMT-Sono Prime Gap Analysis 작업 규약

## 프로젝트 정체성

이 저장소는 검증된 maximal prime-gap record로 end-bounded \(G(x)\)를 복원하고 FGKMT large-gap scale 및 Sono의 explicit constant와 경험적으로 비교하는 계산수론 연구용이다. 후속 이론축으로 Sono의 “sufficiently large \(X\)”를 명시적 numerical threshold로 바꿀 수 있는지도 연구하되, finite observed threshold와 theorem threshold를 구분한다. 이전 실험의 모델 학습 및 GPU 벤치마크 규약은 이 저장소에 적용하지 않는다.

작업 루트:

```text
Z:\FGKMT-Sono-PrimeGap-Analysis
```

## 현재 상태: P002–P013-B PASS·시각 QA 완료 / P010A G4 PASS / P014-R3 actual PASS·상한 개선 없음 / P017 actual PASS / P018-P0/A PASS·A 정보량 HOLD / P019 toy PASS / P020 종합·시각 QA PASS / Sono-FMT H1b-1b Lemma 8.2=89·Lemma 8.4 관련 actual 하위호출 9/9 parameterized explicit / H1b-2a Lemma 8.5·8.6 finite component·H1b-2a.1 Euler normalization·H1b-2a.2 distribution child·H1b-2a.3 actual P94 multiplier 13 닫힘 / H1c-1b.1 actual identity modulus capacity·dyadic repair 닫힘 / H1c-1b.1a coefficient 보존 / H1c-1b.1a.1 `sigma y` cutoff \(x\ge2\exp(36^5)\)로 SIV-03 EXPLICIT / H1c-1b.2 raw \((T,2T]\) psi composition 닫힘 / H1c-1b.3r1 FGKMT actual interval \([T,2T]\)로 교정 / H1c-1b.4a–4e actual identity Hypothesis 1 input constants 1·1·2, \(X\ge2\exp(10^{50})\)에서 explicit / H1b-P92a actual identity weighted P9.2·lower atom explicit (child cutoff X>=2exp(10^1000)); H1b-P91a W-filtered unweighted·shift explicit; H1b-P94g actual T0·growing-k multiplier 1 explicit; H1b-NORM 공통 filtered moment·fixed-X 확률 입력 explicit / H1b-COR1/2/3 R01–R06 actual probability explicit·finite-family count·unit main-degree error / H1b-COV1a Theorem3 C0=100 충분·actual gate explicit / H1b-COV2 fixed-parameter 구간·예외복원·smooth remainder·순차 성공 explicit, R01–R08 child 닫힘·R09–R12 OPEN / DEP-R09 JL5·JL6-MELLIN·JL6-TAIL-ACTUAL·JL6-COMMON-BUDGET/JL6-ACTUAL parameterized explicit·PRINTED GENERAL JL6/JL8 OPEN / SIV-07·08·09 HARD_BLOCKER / X_cert OPEN

2026-09-11 DEP-R09 phase 1은 \(D_{\rm PAP}=160\),
\(C_{\rm PAP}=1-e^{-2}\)의 exact 상수 대수를 Lean으로 확인했다. 그러나 이 160은
수치 시작점이 아니며 Gallagher·Jutila·Maier 계열 multiplier와 공통 finite cutoff는
OPEN이다. 전수 inventory는 1,015식, `NOT_YET_FORMALIZED`는 960식이다. 960식 전부를
source audit보다 먼저 형식화하지는 않되, \(X_{\rm cert}\) 실제 의존 식은 source 고정 후
상위 결론에 사용하기 전에 형식화한다. 정본은 theory 56과 review 63이다.

2026-09-11 DEP-R09 full-source 후속감사에서 Sono Proposition 5.3의
`c_ZFR/log(Q(1+|t|))`는 Gallagher 정규화 `c1=3c_ZFR`를 주지 않음을 확인했다.
Proposition 경유 보수값은 `c_ZFR/3`, McCurley Theorems 1–2 직접 복원값은 `c1=1/24`다.
Gallagher `≪`의 multiplier·cutoff도 원문에 미명시다. 따라서 theory 56은 인쇄된 exact
대수 기록이고, analytic 최신 판정은 theory 57·review 64다. 현재 source chain은
`C_PAP=1-e^-2`, `D_PAP=160`과 fixed `2e-17`을 인증하지 못한다. DEP-R09·PAP-11·
`X_cert`는 OPEN이다. Theory 57 뒤 inventory는 1,030식이고 새 15식을 모두 분류해
`NOT_YET_FORMALIZED`는 960식으로 유지된다. 이 repair 전 threshold calculator나 R11
승격은 금지한다.

2026-09-13 DEP-R09 explicit 대체자료 후속감사는 최신 Sono arXiv v4와 journal판에서
Section 5의 문제 식이 그대로이고 공개 correction/erratum이 식별되지 않음을 확인했다.
Bennett·Bordignon·Yamada·Kadiri와 Thorner--Zaman의 uniform PNT·fully explicit density,
Benli--Goel--Twiss--Zaman의 explicit Deuring--Heilbronn을 비교했지만 actual
`q<=u^(1/160)` pointwise PAP를 numerical multiplier·공통 cutoff까지 바로 주는 drop-in
정리는 없었다. 현재 downstream 식에서 `D=160`의 최소 `C_PAP`은
`0.8638312615226712472...`, `exp(-2)` 이후 추가 error slack은
`0.0008334552407160609...`뿐이다. 낙관적 `C_PAP=1`, `M=D`에서도 fixed `2e-17`을
유지하는 최대 정수 D는 186이다. 이 186은 PAP 정리가 아니라 coefficient capacity
필요조건이다. 최신 analytic 정본은 theory 58·review 65이고, `PAP-11`, DEP-R09,
fixed `2e-17`, `X_cert`는 계속 OPEN이다. Theory 58 뒤 Lean inventory는 59개 문서,
1,046식이며 새 16식은 source theorem 7·definition 1·미형식화 8로 분류했다.

2026-09-13 Branch S proof-DAG 감사는 Thorner--Zaman의 Huxley--Jutila density부터
explicit formula·prime-power·dyadic partial summation·VK decay까지 numerical multiplier와
finite cutoff가 남음을 확인했다. fixed `q=x^(1/160)`의 leading error는 `K exp(-160c)`라
`x` 증가만으로 없어지지 않는다. Jutila 1977의 exponent 2와 `10 exp(11 lambda)`도
`sufficiently large`, epsilon-의존 O, `1+o(1)` rate가 미수치다. elementary gate
`c >= (log K-log eta)/D -> K exp(-Dc)<=eta`만 Lean `KERNEL_PASS`; analytic source는
미형식화다. 최신 analytic 정본은 theory 59·review 66이고 `PAP-11`, DEP-R09, fixed
`2e-17`, `X_cert`는 OPEN이다. Theory 59 뒤 inventory는 60개 문서, 1,056식,
`NOT_YET_FORMALIZED` 970식, 금지 proof escape 0건이다.

2026-09-13 Jutila Lemma 4--8 후속감사는 공식 Huxley III 원문을 확보·hash 고정했고,
Ramaré--Zuniga Alterman Corollary 1.3을 실제 `tau=8/5`에 대입해 식 (3.6)의 one-sided
weighted square-sum upper call을 exact coefficient `18884947/500000 = 37.769894`로
명시화했다. 이는 Lemma 4 full asymptotic이나 Jutila density theorem 전체의 인증이 아니다.
finite `D`의 log-squared correction과 `JL5` harmonic lower bound, `JL6` Mellin/tail,
`JL8` local zero-count multiplier가 남는다. 이 단계의 정본은 theory 60·review 67이고,
`PAP-11`, DEP-R09, fixed `2e-17`, `X_cert`는 계속 OPEN이다. Theory 60 뒤 inventory는
61개 theory 문서, 1,068식, `NOT_YET_FORMALIZED` 971식, 금지 proof escape 0건이다.

2026-09-13 JL5 후속감사는 Zuniga Alterman 2022 Corollary 3.4(b)의 exact
squarefree·coprime harmonic sum을 사용해 Jutila Lemma 5의 `1+o(1)`을 제거했다.
`0<eta<=1`에서
`R0(q,eta)=max(exp(sqrt(log q)),e,(2.554 B_q/(eta c_q))^3)`는
`S_q(R)>=(1-eta)c_q log R`의 계산 가능한 충분 cutoff다. factorwise
`c_q>=(6/pi^2)phi(q)/q`도 Lean에서 유한곱까지 검증했다. 그러나 Lemma 6의 Mellin
integral·truncation tail 두 `<<_epsilon 1`과 JL8 local zero-count multiplier는
OPEN이다. 최신 analytic 정본은 theory 61·review 68이고, `PAP-11`, DEP-R09, fixed
`2e-17`, `X_cert`는 계속 OPEN이다. Theory 61 뒤 inventory는 62개 theory 문서,
1,078식, `NOT_YET_FORMALIZED` 971식, 금지 proof escape 0건이다.

2026-09-13 JL6a 후속감사는 Jutila 식 (2.11)의 두 숨은 오차 중 Mellin 적분만 분리해
명시화했다. `Re w=-beta+delta`, `delta=epsilon/[4(1+epsilon)]`에서 actual
Barban--Vehov weight, imprimitive-character 보정, Bennett et al. 2021의 Rademacher
convexity bound와 Gamma 적분을 합성하면 원 power condition (2.8) 아래
`|I_delta|<=K_M(delta) A^(-epsilon/2)`이고
`K_M=12 sqrt(6) zeta(1+delta)(2/delta+1)/pi^(3/2)`다. 따라서
`JL6-MELLIN=ACTUAL_FORM_PARAMETERIZED_EXPLICIT`이지만, 별도 truncation tail과
JL6 전체·JL8은 `HARD_BLOCKER`다. 최신 analytic 정본은 theory 62·review 69이고,
`PAP-11`, DEP-R09, fixed `2e-17`, `X_cert`는 계속 OPEN이다. Theory 62 뒤 inventory는
63개 theory 문서, 1,104식, `NOT_YET_FORMALIZED` 984식, 금지 proof escape 0건이다.

2026-09-13 JL6b 후속감사는 Jutila 식 (2.11)을 `x=X log(qT)^2`에서 자른 actual tail을
직접 초등 상계했다. `|a(n)|<=2sqrt(n)`, `|psi_r(n)|<=r`, `beta>=1/2`와 endpoint-safe
geometric series를 합치면 `|E_tail|<=4RX exp(-log(D)^2)`이다. 실제
`R=D^epsilon`, `X=D^(1+12epsilon)`에서는
`4 exp(-L^2+(1+13epsilon)L)`이고, 원하는 absolute tail budget의 명시적 `log D`
cutoff도 얻었다. 따라서 `JL6-TAIL-ACTUAL=ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`이다.
다만 printed general Lemma 6에는 `X` upper envelope가 없으므로 일반 uniform tail은
닫지 않았다. 후속 JL6c는 source identity의 감쇠 loss까지 포함한 네 budget을 같은
`C_phi log R` 단위로 합치고 actual parameter에 대한 공통 `log D` cutoff를 만들었다.
따라서 `JL6-COMMON-BUDGET`과 `JL6-ACTUAL`은 parameterized explicit이나 printed general
JL6·JL8, `PAP-11`, DEP-R09, fixed `2e-17`, `X_cert`는 계속 OPEN이다. 최신 정본은
theory 64·review 71이다. Theory 64 뒤 inventory는 65개 theory 문서, 1,142식,
`KERNEL_PASS=42`, `CONDITIONAL_KERNEL_PASS=23`, `NOT_YET_FORMALIZED=994`,
Lean declaration 148개, 금지 proof escape 0건이다.

P002 pilot, P003 전체 `10^20` end-bounded 분석, P004 start/end 경계·local-envelope 민감도 분석이 완료됐다. P004 authoritative run `20260823T075238Z_p004_sensitivity`는 64 end/start paired intervals와 100-dps 수치·정수 3,747개를 issue 0으로 검증했고, 사용자가 y축 제한 새 그래프도 큰 문제없다고 확인했다.

P004 해석 정본은 `test_result/202608231652_P004_sensitivity_analysis.md`다. P005 bounded CPU calibration, P006 `[2,10^9]`, P007 modulus 30/210/2310 비교, P008 toy·exact prime-count·phase-A full은 모두 terminal/saved verification PASS다. P009 actual `[10^20,10^20+1000)`은 internal zero와 exact boundary witness를 결합해 certified zero 1 block을 만들었다. P010A G4는 modulus 30030의 35,224,647 constraints를 exact 검증해 count 상한을 `436,001,550,591,586,306`으로 약 0.7195% 낮췄지만 acceleration은 미증명이다. P011–P013-B recurrence 계열은 enrichment를 검출하지 못했다. P013-A/B는 각각 primary 기대 0.077829/0.066797, 관측 0, 모든 행 LOW_INFORMATION이며 사용자 figure QA까지 PASS했다. P017 combined queue와 A/B child는 terminal·saved·exact equality PASS다. P017-B 동일범위 serial 12,598.410초 대 parallel 2,866.160초로 관측 wall-time 비가 약 4.3956이었다. P014-R3는 modulus 510510의 92,160 states와 8,524,288,932 constraints를 parallel exact scan과 saved serial oracle로 issue 0 검증했지만 새 candidate를 만들지 못해 `NO_IMPROVEMENT`다. P018-P0/A는 exact 실행·저장 검증 PASS지만 conditioned information이 0이라 `HOLD_PREFIX_INFORMATION`이다. P020은 성공 정본 8개와 72,178,455,399 gap-start를 종합했고 사용자 figure QA까지 PASS했다. Sono/FMT 최신 source-first 감사는 JL5, JL6 Mellin, actual tail과 네-part common budget을 합쳐 `JL6-ACTUAL`을 parameterized explicit로 닫았다. printed general JL6, JL8과 PAP는 남아 있으므로 fixed `2e-17`은 현재 프로젝트가 독립 인증한 계수가 아니며 numerical `X_cert`와 실제 전역 최소도 OPEN이다. `X_emp(10^20)=3,814,280`만 finite exact이다. 최신 analytic 정본은 `docs/method/theory/64_Sono_FMT_DEPR09_Jutila_Lemma6_actual_common_budget.md`와 `docs/review/71_20260913_DEPR09_Jutila_Lemma6_actual_common_budget_타당성검토.md`다. P019는 future 범위의 dual-partition parallel full-pass toy를 exact count 21로 검증했지만 actual runner는 없다. 완료 runner는 `test_done`에 hash 보존하며, 추가 actual 실행·외부 게시·push/PR은 별도 사용자 승인 없이 수행하지 않는다.

Sono/FMT T1은 direct proof edge 66개를 source/page/equation/dependency 단위로 등록하고 DAG·source
hash를 검증했다. H1a 뒤 6개가 해당 행 자체에서 `EXPLICIT`이고, 30개는 rate 누락, 16개는 hard blocker다.
특히 numerical PAP·UB, asymptotic-to-finite slack, good sieve weight, hypergraph failure probability,
arbitrary-X coverage가 root critical path다. 정본은
`docs/method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md`와
`docs/review/23_20260902_Sono_FMT_T1_hard_node_feasibility.md`다. 모든 hard input이 닫히기 전에는
threshold calculator나 장시간 계산 runner를 만들지 않는다.

Sono/FMT H1 source tracing은 FMT Theorem 6→FGKMT Theorems 5–6→Maynard Proposition 6.1과
FGKMT Hypothesis 1을 추적했다. good weight는 symbolic·effective-in-principle이지만 finite
`r_0`, moment implied constants와 Hypothesis 1의 수치 package가 없어 정량 재증명이 필요하다.
H1 판정은 `CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED`이고
`X_cert`는 계속 OPEN이다. 정본은
`docs/review/24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md`와
`docs/method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json`이다. H1a는 exact envelope와
Cantelli transfer로 (J_r/I_r>\log r/(4r))를 모든 정수 (r\ge36)에서 project theorem으로 닫아
`SIV-06`을 `EXPLICIT`으로 바꿨다. 정본은
`docs/method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md`다. H1b는 Maynard Proposition
6.1·Hypothesis 1·Sections 8–9를 17개 constant obligation으로 등록했지만 전체 moment의
finite cutoff·공통 error budget을 얻지 못해 `SIV-07/09`와 `X_cert`를 닫지 않았다. 정본은
`docs/method/theory/14_Sono_FMT_H1b_Maynard_Proposition_6_1_constant_ledger.md`다. H1b-1은
Lemmas 8.1–8.4를 13개 하위 node로 감사해 Lemma 8.3의 정확한 GGPY Lemma 4 \(\kappa=1\)
source를 확인했다. H1c는 Hypothesis 1/PAP를 20개
node로 분리하고 Hypothesis 1(1),(3)의 finite sufficient reduction을 얻었지만 condition (2)와
PAP finite cutoff는 열려 있다. 두 명제는 shared analytic input을 가진 sibling이지 서로를
함의하지 않으므로 T1의 잘못된 `SIV-08 -> PAP-11` 직접 의존선을 제거했다. Jutila source는
1977로 정정했다. 정본은 `docs/method/theory/15_Sono_FMT_H1b1_basic_summation_constant_audit.md`와
`docs/method/theory/16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md`다. H1b-1a는 explicit
cutoff의 `sup|psi'|<50`, Lemma 8.1(i)의 `S_B(L)>exp(-9k/2)`, 식 (8.5)의
`E(k)<24 log k`를 project finite lemma로 닫고 divisor 평균의 parameterized majorant를
유도했다. 그러나 입력 계수·공통 cutoff는 열려 있어 `SIV-07`과
`X_cert`는 OPEN이다. 정본은
`docs/method/theory/17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md`다. H1b-1b는
Maynard Lemma 8.2의 uniform multiplier를 89로 닫았다. Castillo et al.의 교정에 따라
GGPY/Maynard의 인쇄 proof는 그대로 쓰지 않는다. H1b-1b-2b는 Ford Theorem 4.4의
누락항 \(c_\gamma(L+1)^\kappa\)를 보존한 proof를 \(\kappa=1\)에 명시화해
\(C_{8.3}(a,A_2)=2\{40960D(a,A_2)e^{256+A_2}+2\}\), \(z\ge2\)를 얻었다.
H1b-1b-2c는 실제 네 denominator family와 양 끝 포함 prime-sum을 다시 감사해
공통 \(a=1/2\), \(A_2=8\), \(L=5+\log\Lambda_*\)를 인증했다. 따라서 one-step
`H1B-L83`은 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다.
기존 절대오차 전달 \(C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}\)와 \(c_\gamma\) 하한은
optional cross-check다. H1b-1b-2a.1은 Maynard Section 8의 10개 source call을 11개 analytic
subapplication으로 분해하고, 비제외 local factor와
\(dW_i,W'_i,a_mWBr,rW_m,W_0\)를 포함한 제외모듈 상계를 전수 인증했다.
따라서 모든 추적 호출에서 공통 \(\log Q_j\le\Lambda_*\)와
\(c_{\gamma,j}>1/[3(1+\log\Lambda_*)]\)를 쓸 수 있다. 정본은
`docs/method/theory/18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md`,
`docs/method/theory/20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md`,
`docs/review/27_20260906_H1b1b_Kuperberg_GGPY_error_term_타당성검토.md`,
`docs/method/theory/22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md`와
`docs/method/theory/23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md`다. 실제 입력을
넣은 one-step multiplier는 약 \(7.9173\times10^{121}\)이다. H1b-1b-2d는
support-scaled profile norm과 \(\prod_i(1+\delta_i)-1\) 합성으로 smooth Lemma 8.4
호출 7개를 하위 package로 닫았다. \(F_2^2\)의 support-\([0,2]\) 좌표는 먼저 합해야
기존 \(\Lambda_*\)가 유지된다. H1b-1b-2d.1a는 905행에서 전역 \(H\)의 \(C^1\)
norm을 요구하지 않고 \(A^2,AB,B^2\)로 제곱합을 우회할 수 있음을 닫았다.
H1b-1b-2d.1a.1은 최종 출판본 (9.42)--(9.48)을 수치 재증명해
\(C_Y=327680(14801/69)e^{264}+10,143,697<3.17\times10^{122}\)와 finite gate를
얻었다. H1b-1b-2d.1b는 실제 \(\xi=\theta/10\), \(R\le x^{\theta/3}\)에서
\(\xi\log x\ge(3/10)\log R\)를 얻고 strict multiplier \(C_\Sigma+2\)로
두 sharp 호출을 finite하게 닫았다. 따라서 Lemma 8.4 관련 actual 하위호출 9/9와
`H1B-L84`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다. 정본은
`docs/method/theory/24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md`,
`docs/method/theory/25_Sono_FMT_H1b1b2d1a_H_remainder_bypass.md`,
`docs/method/theory/26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md`,
`docs/method/theory/27_Sono_FMT_H1b1b2d1b_sharp_xi_logx_scale.md`다.
H1b-2a는 Lemma 8.5 weight envelope와 Lemma 8.6 absolute size를 유한식으로 닫았다.
H1b-2a.1은 Proposition 9.4 식 (9.66)의 마지막 두 Euler 곱과 식 (9.64)의 제곱 보정을
\(e^{2+6/k}\mathfrak S_{WB}(\mathcal L)^{-1}\) 이하로 닫았다. H1b-2a.2는 실제
\(\mathcal A=\mathbb Z,D=1,\xi=\theta/10\) 호출에서 정확한 \(E_q^{(1)}\le1\)과
\(\tau_{3(k+1)}\) tuple multiplicity를 사용해 식 (9.52) distribution child를
`ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`으로 닫았다. 일반 \(\mathcal A\) 명제와 달리
이 actual child는 Hypothesis 1(1),(3)의 미지 multiplier를 기다리지 않는다. H1b-2a.3은
product-profile의 \(2^k\) 손실을 강화 smooth cutoff로 흡수하고 모든 child를 합성해
모든 정수 \(k\ge36\)에서 actual P94 multiplier 13 미만을 얻었다. 따라서
`H1B-P94=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다. 일반 \(\mathcal A\) P94,
P91/P92/L93/P95, `SIV-07/09`와 `X_cert`는 열려 있다. H1c-1a는 Hypothesis 1(2)와
Maynard Proposition 9.2의 source inventory를 완료했다. 선언 source 중 drop-in 정리는 없고
Bordignon 2021 Theorem 1.4가 `PRIMARY_COMPOSITION_CANDIDATE`다. H1c-1b.1은 outer
\(k_{\mathrm{chain}}=1\)과
growing sieve/form dimension \(r\)를 분리하고, actual Proposition 9.2의 identity form에서
\(A(r)=100r^2+10\)을 Bordignon 2021에 점별 대입할 수 있음과 modulus capacity를 닫았다.
source \(r_s=\lfloor(\log x)^{1/5}\rfloor\)는 \(T=x/2\)의 반복 transition strip에서
Maynard dimension 조건을 어기므로
\(r_T=\lfloor(\log(x/2))^{1/5}\rfloor\in\{r_s-1,r_s\}\)로 exact repair했다.
H1c-1b.1a는 이 dimension 손실과 실제 \(R=(x/4)^{\theta/3}\) 손실을 함께
\(39/40\)보다 크게 묶었다. 이어서
\(\sigma y\le(26/25)80cx\log_2x\)인 finite range에서는 Sono의 같은
\(2\times10^{-17}\) 계수가 유지됨을 증명했다. H1c-1b.1a.1은 Rosser--Schoenfeld
Theorem 7과 제외 prime 보정을 사용해 \(x\ge2\exp(36^5)\)에서 더 강한
\(1001000/998001<26/25\) 상계를 얻었으므로 `SIV-03`은 `EXPLICIT`이다.
H1c-1b.2는 actual fixed outer scale에서 같은 \(Q_1\)을 \(T\), \(2T\)에 써 하나의
exceptional modulus와 그 prime divisor \(B\)를 공통으로 고정했다. 최종 NYJM판
Bordignon RHS 12항을 모두 등록했고 raw \((T,2T]\) \(\psi\) discrepancy를
\(R_B(T)+R_B(2T)\)로 합성했다. H1c-1b.3은 Maynard 원문의 일반 \([T,2T)\) bridge를
정확히 처리했지만, H1c-1b.3r1은 FGKMT Definition 2의 actual interval이
\([T,2T]\)임을 확인해 표기를 교정했다. source \((T,2T]\)에서 closed target으로 더하는
lower atom의 centered count 비용은 1 이하라 기존 수치 envelope를 보존한다.
H1c-1b.4a–4d는 Bordignon source 정규화, explicit density, 12항·count 비용 흡수와
source constant 재증명을 닫았다. H1c-1b.4e는
\(T=X/2\), \(r=\lfloor(\log T)^{1/5}\rfloor\ge10^{10}\)에서 actual
\(\mathcal A=\mathbb Z\), identity subset의 Hypothesis 1 입력을 constants
\((1,1,2)\)로 explicit하게 합성했다. 이는 weighted Proposition 9.2 자체가 아니다.
H1b-P92a는 그 weighted identity P9.2와 closed-to-open lower weight/count atom을
\(k\ge10^{200}\)에서 relative/additive multiplier 1/1로 닫았다. 후속 H1b-P91a는 명시적
W-filtered unweighted moment와 closed shift를 닫았다. H1b-P94g는 actual T0에서 growing-k
P94와 각 p의 local-series off-tuple 상계를 닫았다. 공통 정규화는 theory 47에서 닫혔으나 downstream 확률·일반 정리 의무는 남아 broad SIV-07/08/09는 HARD_BLOCKER,
\(X_{\mathrm{cert}}\)는 OPEN이다. 모든 root dependency가 닫히기 전에는 새 prime
sweep·threshold calculator를 만들지 않는다.

`article/unverified/`의 2026 bounded-gap 원고 2편은 기존 9편 corpus에 합산하지 않는다.
Stadlmann의 `H_1<=240`과 OpenAI의 `H_1<=186`은 peer review·독립 검증 전 주장으로만 기록한다.
후자의 공개 Lean 결과는 핵심 project axiom 3개에 조건부이고 Python certificate는 analytic
추정 전체를 증명하지 않는다. 상세 판정은
`docs/review/25_20260904_Stadlmann_Bounded_Gaps_240_unverified.md`와
`docs/review/26_20260904_OpenAI_Improved_Short_Gaps_186_unverified.md`를 따른다.

허가 전 허용:

- 로컬 작업지시서와 논문 읽기
- 문헌 리뷰와 방법론 문서 작성
- 폴더 구조 및 import 가능 여부 확인
- 기존 파일의 정적 검토
- 데이터 취득·검증·분석·시각화 코드를 작성하되 외부 데이터 없이 toy fixture로 시험
- 데이터에 의존하지 않는 수학 정의 모듈과 사전검증 단위시험 작성·실행
- 원격 branch의 commit hash 같은 source metadata를 읽기 전용으로 확인

허가 전 금지:

- 외부 maximal-gap dataset 다운로드
- raw/validated dataset 생성 또는 변환
- 본 계산, 통계 fitting, envelope 계산, 그래프 생성
- `test_result/`에 실험 결과 작성
- 결과 해석 또는 결론 확정

사용자가 “실험 수행을 허가한다”는 취지로 명시한 뒤에만 `docs/METHODS.md`의 P1 이후를 시작한다.

## 지시 우선순위와 정본

1. 현재 사용자의 명시적 지시
2. `연구 작업지시서_ FGKMT-Sono 대형 소수간격 하한과 실제 maximal prime gap의 경험적 비교 분석.md`
3. `docs/METHODS.md` - 교정된 계산 정의와 실행 절차의 정본
4. `handoff/`의 최신 `YYYYMMDDHHmm_HANDOFF.md` - 현재 상태, 검증 결과, 승인 경계와 다음 행동
5. `test_result/00_실험결과_분석보고서_색인.md` - 실행번호, 로그, run directory, 정본 결과보고서 연결
6. `docs/review/00_문헌_종합_분석.md` - 초기 9편 비교 corpus와 DEP-R09 source 후속 종합 판정
7. `docs/review/01_...09_...md` - 논문별 상세 분석

작업지시서와 `docs/METHODS.md`가 충돌하면 수학적 오류를 조용히 덮지 말고, `docs/METHODS.md`의 교정 사유를 사용자에게 설명하고 확인받는다.

## Python 환경

반드시 아래 환경을 사용한다.

```text
Conda env name: FGKMT
Prefix: W:\miniforge3\envs\FGKMT
Python: W:\miniforge3\envs\FGKMT\python.exe
```

PowerShell에서는 환경 활성화 여부에 기대지 말고 가능하면 절대경로 Python을 호출한다.

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' --version
& 'W:\miniforge3\envs\FGKMT\python.exe' -m pip check
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest discover -s tests -v
```

시스템 Python, Codex 번들 Python, 다른 Conda 환경으로 연구 코드를 실행하지 않는다. PDF 읽기 같은 도구 내부 작업은 예외지만, 연구 산출물과 계산 결과는 반드시 FGKMT 환경에서 재현한다.

확인된 준비 상태(2026-08-22/23):

```text
Python 3.11.16
gmpy2 2.3.1
matplotlib 3.11.1
mpmath 1.4.1
numpy 2.4.6
pandas 3.0.5
pillow 12.3.0
pyarrow 25.0.1
scipy 1.17.1
statsmodels 0.14.6
```

버전 정본은 `requirements.txt`다. 패키지 설치, 제거, 업그레이드는 사용자의 별도 허가 없이 하지 않는다.

## 폴더 규약

```text
article/          초기 비교 corpus 9편과 DEP-R09 source 보존본; 검토 완료 원본 수정 금지
article/unverified/ 미심사·미독립검증 후보 원고; 정본 9편 corpus와 분리, 원본 수정 금지
datas/            source registry와 승인 후 commit별 raw/validated 데이터
source/           정의, source parser, provenance, validation, end-bounded 분석, plotting, CLI
tests/            데이터 비의존 및 toy-record 사전검증 단위시험
docs/METHODS.md   방법론 정본
docs/method/      세부 설계 문서
docs/review/      이번 연구의 문헌 리뷰 정본
test_plan/        실행 전 계획과 입력 hash, 성공/중단 기준
test_result/      승인 후 run별 tables, figures, summary
handoff/          세션별 YYYYMMDDHHmm_HANDOFF.md; 기존 메모 비덮어쓰기
.agents/skills/   Codex가 자동 탐색하는 프로젝트 스킬
ai_dev_tool/      이 프로젝트의 계산 함정·착수·핸드오프·작업원장 절차
ai_dev_tool/work_ledgers/ 장기 작업의 진행 중 원장과 `-done` 완료 원장
lean/             고정 Lean/Mathlib 프로젝트, 전수 수식 원장과 단일 theory 형식검증 파일
test_done/         완료 BAT/PS1/SH와 실험 전용 helper를 `-done` suffix·SHA-256으로 보존; 재실행 금지
scripts/common/    재사용 공통 로깅·실행 기능
scripts/runners/   특정 완료 실험과 분리된 공통 runner
scripts/experiments/ 신규 실험별 toy·준비 진입점
scripts/setup/     사용자 확인 플래그가 필요한 설치 helper; Codex 임의 실행 금지
tmp/              읽기/렌더링 임시 파일; 최종 산출물 아님
```

문헌 리뷰는 `docs/review`에만 작성한다. 유사 철자의 별도 경로를 만들지 않는다.

## 작업원장

- 세 단계 이상, actual artifact 사용, 여러 파일 변경 또는 30분 이상 걸릴 수 있는 작업은
  본작업 전에 `ai_dev_tool/work_ledgers/YYYYMMDDHHmm_<작업명>_WORK_LEDGER.md`를 새로 만든다.
- 각 큰 단계가 끝날 때 완료 증거, 변경 파일, 검증 명령·결과, 실패와 정확한 다음 재개점을 갱신한다.
- 대화 압축이나 새 세션 뒤에는 최신 비 `-done` 원장과 최신 handoff를 함께 읽고 첫 미완료 단계부터 재개한다.
- 요청 산출물·검증·정본 동기화·handoff가 모두 끝난 경우에만 파일명 끝을 `WORK_LEDGER-done.md`로 바꾼다.
- 실패·보류·사용자 결정 대기는 완료가 아니며, 완료 원장은 사용자 승인 없이 삭제하거나 덮어쓰지 않는다.
- 상세 양식과 안전한 이름 변경 절차의 정본은 `ai_dev_tool/08_작업원장_작성규약_양식.md`다.

## Agent skills

Codex의 저장소 스킬 정본 발견 경로는 `.agents/skills/`다. 현재 프로젝트에서는 `.claude` 호환 미러를 복원하거나 사용하지 않는다.

- 작업이 스킬 description과 명확히 일치하거나 사용자가 스킬을 지명하면 해당 SKILL.md 전체를 먼저 읽는다.
- 이번 연구의 핵심 스킬은 exp-plan, exp-preflight, log-to-result, runner-retirement, research-status-synthesis, run-batch, session-handoff다.
- 스킬 수정은 `.agents/skills/`에만 반영하고 해당 SKILL.md 검증을 통과시킨다.
- 스킬은 사용자 승인 경계를 확장하지 않는다. exp-preflight가 READY여도 실제 실험 허가가 없으면 실행하지 않는다.
- issue, PR, push, merge 같은 외부 변경 스킬은 사용자의 명시적 요청 범위에서만 사용한다.

## 수학적 불변식

### Lean 형식검증 증거 경계

- Lean 도구chain은 `lean/lean-toolchain`, `lean/lakefile.toml`, `lean/lake-manifest.json`으로
  고정하고, 관측 kernel·dependency commit은 `lean/README.md`에 기록한다. 임의 upgrade는 금지한다.
- theory 형식화는 요청대로 `lean/FGKMTSono/TheoryVerification.lean` 한 파일에 모으고,
  각 선언 주석에 원문 theory·식 ID를 적는다. 전수 수식 상태 정본은
  `lean/VERIFICATION_LEDGER.md`, 기계 inventory는
  `lean/verification/formula_inventory_v1.json`이다.
- `KERNEL_PASS`, `CONDITIONAL_KERNEL_PASS`, `DEFINITION_ONLY`, `PARTIAL_FORMALIZATION`,
  `SOURCE_THEOREM_UNFORMALIZED`, `NOT_YET_FORMALIZED`을 서로 바꾸어 쓰지 않는다.
  source theorem을 premise로 받은 downstream 대수 증명은 독립 source 증명이 아니다.
- 전체 미형식화 개수만으로 다음 source audit을 막지 않는다. 대신 최종 \(X_{\rm cert}\)
  의존 DAG에서 실제로 사용할 식은 source·statement 고정 후 상위 결론에 사용하기 전에
  형식화한다. dependency-critical 식이 남아 있으면 calculator와 최종 certificate는 금지한다.
- project-local `axiom`, `sorry`, `admit`으로 검증 항목을 닫지 않는다. 이들이
  불가피해 보이면 사용 전에 중단하고, 형식화가 안 되는 이유·대체 공식/방법·검증된
  외부 선행연구의 보장 여부를 보고한 뒤 사용자의 명시적 허가를 받는다. 허가 없이는
  절대 사용하지 않는다. `.lake/` build cache는 commit하지 않는다. inventory·원장 검증과
  `lake build`가 모두 PASS해야 현재 batch를 kernel 검증 완료로 기록한다.
- 2026-09-10 기준 Theory 01의 `F(x)`는 `x > exp(exp(exp(1)))`에서 양수이고
  엄격히 증가하며, 양의 end-bounded 정수 plateau의 오른쪽 끝점 minimum도
  proof escape 없이 `KERNEL_PASS`다. `G_end(x)=g_i`의 finite-record 상수성 전체는
  `T01-U004 PARTIAL_FORMALIZATION`으로 남아 있고 `X_cert`는 OPEN이다.
- 2026-09-10--11 Theory 55 식 (55.24)--(55.35)의 smooth-remainder 경로를 분해했다.
  (55.26) kernel 적분, (55.28) 두 finite-interval 비교, Ein `103/100`,
  (55.32), (55.34), 기존 (55.33)은 `KERNEL_PASS`다. (55.27)은 prime-sum
  정규화·endpoint·상수 slack·종단 합성만 통과한 `PARTIAL_FORMALIZATION`이며,
  Rosser--Schoenfeld `theta < 1.01624 t`와 Stieltjes/Abel 비교는 외부 source
  입력으로 남는다. 이를 전체 smooth-number source proof나
  `DEP-R08`, broad `SIV`, `X_cert`의 Lean 인증으로 확대하지 않는다.
- 일부 수식의 Lean 통과를 전체 Sono/FMT 증명이나 `X_cert` 확정으로 확대 해석하지 않는다.

### 반복로그 정의: 밑이 아니라 반복 횟수

모든 로그는 자연로그이며, 아래 첨자 (k)는 로그의 밑이 아니라 자연로그의 반복 횟수다.

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 적용}}.
\]

따라서 반드시 다음 정의를 사용한다.

\[
\log_1x=\ln x,\quad
\log_2x=\ln(\ln x),\quad
\log_3x=\ln(\ln(\ln x)),\quad
\log_4x=\ln(\ln(\ln(\ln x))).
\]

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},\qquad
c_{\mathrm{Sono}}=2.0\times10^{-17}.
\]

`math.log(x, 2)`, `math.log(x, 3)`, `math.log(x, 4)`, `numpy.log2(x)` 같은 base-(k) 구현을 연구 계산에 사용하지 않는다. 허용되는 예외는 iterated-log와 값이 다름을 확인하는 단위시험뿐이다.

정본 구현은 `source/definitions.py`의 `iter_log`와 `F`다. 실제 데이터 코드 실행 전 다음을 모두 만족해야 한다.

1. `iter_log(x, 2|3|4)`가 직접 중첩한 `mp.log` 값과 일치
2. 위 값이 base-(2|3|4) 로그와 서로 다름
3. `F(x)`가 직접 펼친 식과 일치
4. `source/` 정적 감사에서 금지된 base-(k) 호출이 0건

정의 오류가 발견되면 해당 코드로 계산한 `F`, `H`, Sono ratio, interval minimum, running minimum, 그래프와 통계 요약을 유효하지 않은 산출물로 표시하고 전부 재생성한다.

### canonical maximal-gap 정의

```text
G(x) = max gap with end_prime <= x
```

- 사용자가 지정한 end-bounded 정의 하나를 연구 정본으로 사용한다.
- source의 start-prime high-watermark ordering은 `end_prime=start_prime+gap`으로 변환한다.
- schema, 표, 그래프에 `boundary_mode=end`를 반드시 표시한다.
- start-bounded 보조 분석은 P004 민감도 산출물에만 격리하고 canonical end-bounded P003/Sono 계열을 교체하지 않는다.

### 분석 시작점

`x=16`은 반복로그가 형식상 정의되는 최소 정수일 뿐 양의 lower-bound scale 시작점이 아니다.

```text
X_SCALE_POSITIVE_MIN = 3_814_280
```

`16 <= x < 3_814_280`은 domain 진단으로만 다루고, theorem-scale `H`, `Q`, running minimum에는 넣지 않는다.

### envelope 성질

프로젝트의 finite table은 `x`를 정수로 제한한다. record 점프 위치를 `e_i=end_prime_i`라 할 때 정수 interval은 `[e_i, e_{i+1}-1]`이다. 실수 `X` 전체에서는 plateau가 `[e_i,e_{i+1})`이고 오른쪽 끝 minimum이 아니라 `X -> e_{i+1}-`에서의 infimum을 사용한다. 양의 scale 정수 구간에서

```text
H_interval_min = gap_i / F(e_{i+1} - 1)
```

이며 시작점은 `X_SCALE_POSITIVE_MIN`으로 clip한다. 마지막 record는 verified exhaustive limit까지만 닫는다.

global running minimum은 정의상 단조 비증가한다. 증가나 상하 요동을 보고 싶으면 log-bin minimum 또는 rolling minimum을 별도 지표로 만든다.

## 정리와 경험적 주장 구분

- Sono의 `2.0e-17`은 출판본이 제시한 보수적 계수이며 관측값의 예상 극한은 아니다. 다만 이 프로젝트의 2026-09-11 full-source 감사에서는 PAP 정규화와 숨은 multiplier 간극 때문에 아직 독립 인증하지 못했다.
- Sono 출판본은 FMT `Chains of large gaps between primes`의 explicit version이다. FGKMT 5인 논문의 상수를 그대로 계산한 것으로 서술하지 않는다.
- Sono 정리는 “sufficiently large X”에 적용되며 바로 쓸 수 있는 수치 threshold는 제시하지 않는다.
- `H=1`은 Kourbatov-Wolf 2020의 2차 empirical 진술을 근거로 한 참고선일 뿐, 증명된 정리나 \(H\)의 극한이 아니다.
- finite verification, heuristic, conditional theorem, unconditional theorem을 문장과 표에서 구분한다.
- 9편 corpus 안에서 동일한 검증 pipeline이 없다는 판정은 전 세계 문헌 novelty 판정이 아니다.
- Feliksiak 2021 preprint는 fitted \(LB/F\) 비교라는 가까운 선행 시도지만 핵심 논증을 신뢰 가능한 theorem으로 채택하지 않는다.

## 유한 certificate·탐색 가속 불변식

- `gap >= 1856`을 찾거나 배제할 때 equality 1856을 포함한다. `gap > 1856`으로 바꾸지 않는다.
- start-bounded block `[a,b)`의 internal upper bound 0만으로 전체 zero를 선언하지 않는다. 마지막 소수의 right-boundary crossing을 exact witness로 닫아야 한다.
- 전역 count upper bound가 작아져도 gap 위치 목록이나 exhaustive search acceleration이 자동으로 생기지 않는다. local zero 또는 누락 없는 candidate-cover mapping과 total-cost 개선을 별도로 증명한다.
- 같은 wheel residue state는 작은 소수 divisibility geometry만 공유한다. actual primality나 prime-witness 위치를 translation으로 복사하지 않는다.
- `D=li-pi`, `N=Delta li-Delta D`에서 `inf(Delta D)`의 하한은 `N`의 상한을 준다. 이는 empty interval 발견 방향이며, required-empty interval의 nonempty를 보여 gap 후보를 배제하는 방향과 혼동하지 않는다.
- 비엄격 `N <= R`의 exact integer 상한은 `floor(R)`다. `ceil(R)-1`은 엄격한 `N<R`을 증명한 경우에만 사용한다.

## 데이터 취급

승인 후 원본은 `datas/raw/prime-gap-list-project/<commit>/`에 저장하고 절대 덮어쓰지 않는다. 정본은 GitHub `allgaps.sql`이며, 실행 시 master를 다시 resolve한 뒤 40자 commit으로 URL을 고정한다. 웹 표는 참고용이다. 모든 source에 URL, 취득 UTC, commit, SHA-256, column semantics, boundary semantics, record count, claimed exhaustive limit를 기록한다.

정규화 최소 schema:

```text
record_index,start_prime,gap,end_prime,source_id,source_row_id,source_commit,verified_exhaustive_limit
```

검증 순서:

1. 큰 정수를 문자열/Python `int`로 읽기
2. `end_prime == start_prime + gap`
3. start prime, end prime, record gap의 엄격 증가
4. published `ismax`와 eligible first occurrences에서 독립 재구성한 high watermark 대조
5. `gmpy2.next_prime(start_prime) == end_prime` 보조검사
6. record count와 external exhaustive coverage provenance 확인
7. raw 및 schema hash와 validated output hash 기록

독립 source가 추가로 제공되면 중첩 record를 대조하되, 현재 canonical dataset 하나만으로 독립 교차검증을 했다고 주장하지 않는다.

probable-prime 검사는 record completeness의 증거가 아니다. 최신 발견 record와 exhaustive 검증범위도 같은 뜻이 아니다.

## 승인 후 구현 순서

반드시 `docs/METHODS.md`의 P1-P5 순서를 따른다.

1. 데이터 출처와 범위를 먼저 고정
2. raw와 metadata 보존
3. validation report 생성
4. toy data 단위시험 통과
5. 반복로그 preflight와 source base-(k) 정적 감사 통과
6. `F`, end-bounded `G/H/Q`, interval minimum, jump recovery, envelope 계산
7. 큰 정수를 10진 문자열로 보존한 결과 CSV 생성
8. 그래프 생성
9. 마지막에만 해석

전체 소수를 거대한 상한까지 생성하지 않는다. maximal-gap record로 해결되는 분석에 full prime list를 사용하지 않는다.

## 실행 계획과 결과 기록

각 실행 전에 `test_plan/`에 다음을 적는다.

- 목적과 연구 질문
- 입력 파일 및 SHA-256
- source/exhaustive range
- boundary mode
- 정밀도 설정
- 실행 명령
- 성공, 경고, 중단 기준
- 예상 산출물

실행 후 `test_result/`에 다음을 남긴다.

- stdout/stderr와 종료코드
- Python executable 및 패키지 버전
- 입력/코드 hash
- analyzed max x와 record count
- verified exhaustive range
- end-bounded minimum H와 위치
- Sono 대비 배수와 `H=1` 하회 여부
- running minimum 및 local envelope 요약
- 경고, 결측, 해석 한계

모든 승인 실행기는 stdout과 stderr, 빈 줄, stage exit code, Python traceback, PowerShell/shell 예외를 `test_result/logs/`에 run id별로 보존한다. 실패한 WSL 실행은 run root에 `manifest.failed.txt`도 남긴다. terminal PASS와 필수 manifest·산출물을 확인하기 전에는 실험 PASS로 기록하지 않는다.

결과를 본 뒤 계획서를 소급해 바꾸지 않는다. 변경이 필요하면 새 계획 버전과 이유를 남긴다.

## revision·runtime·결과 metadata 불변식

- 신규 actual artifact는 가능한 경우 `experiment_family`, `schema_version`, `runner_revision`을 별도 저장한다. transport-only revision도 과거 runner label을 현재 revision처럼 재사용하지 않는다.
- 예상시간은 `expected full path`, `possible early exit`, `hard wall`을 구분한다. 조기종료 시간을 full search 예상으로 재사용하지 않는다.
- `EXPERIMENT_PASS`와 `SCIENTIFIC_NO_IMPROVEMENT`, `LOW_INFORMATION`, `CALIBRATION_ONLY` 같은 과학적 판정을 동시에 허용하고 서로 대체하지 않는다.
- `tmp` 경로라도 downstream `READY`, checkpoint, raw evidence, actual provenance는 의존 실험과 감사가 끝날 때까지 `RETAIN`한다. 경로명만으로 삭제하지 않는다.
- memory는 사전 추정치와 관측 peak process-tree 값을 구분한다. 관측하지 않았으면 `not measured`라고 기록한다.
- actual result artifact는 metadata 오기가 있어도 소급 수정하지 않는다. 정정 보고서 또는 새 revision으로 교정한다.
- 한 번의 PID 조회, 낮은 CPU snapshot 또는 조용한 console만으로 장기실행 종료를 단정하지 않는다. process tree, heartbeat, file write time, terminal marker를 함께 본다.

## 사용자 실행·보고 불변식

- `IMPLEMENTED`, `LOCALLY_VERIFIED`, `USER_RUN_FAILED`, `EXPERIMENT_PASS`를 구분한다.
- 사용자가 실제 실행했다고 확인한 BAT/PS1/SH는 SHA-256을 기록하고 `test_done/<name>-done.<ext>`로 이관한다. 완료 실험 전용 helper도 함께 이관한다. done은 실행 이력이지 성공 판정이 아니다. 재시도는 `scripts/experiments/<experiment>/`의 새 revision으로 한다.
- 핸드오프의 각 권장 작업에는 실행 환경, 시작 경로, 복사 가능한 정확한 명령, 예상 시간, 로그·산출물, 사용자 회신 항목을 쓴다. 사용자 명령이 없으면 `별도 수행절차 필요없음`이라고 명시한다.
- 사용자 실행 실패는 원본 로그 hash, 마지막 PASS, 첫 FAIL, terminal marker와 결과 디렉터리 존재 여부로 감사한다. 콘솔 일부만으로 판정하지 않는다.
- heavy/actual experiment는 사용자가 실행하도록 요청하고, Codex는 별도 승인이 없으면 parser·toy·approval-denial·unit test까지만 수행한다.
- queue와 개별 runner가 모두 준비된 경우 사용자 안내에는 두 방법을 모두 제시하고, 둘 중 하나만 선택해 같은 child를 중복 실행하지 않도록 명시한다.
- 이 PC의 향후 CPU-heavy runner는 가능한 경우 물리 4코어·논리 8프로세서를 topology-aware affinity와 thread-pool ceiling으로 고정한다. 단일-stream 알고리즘을 8-thread 병렬이라고 과장하지 않고 실제 병렬성·자원 상한을 로그에 구분한다.
- 그래프는 자동 수치검증 뒤 사용자에게 시각검사를 요청한다. 사용자 확인 전에는 visual QA PASS라고 쓰지 않는다.
- 상세 절차 정본은 `ai_dev_tool/04_사용자실행_로그_완료이관_규약.md`다.

## 품질 및 안전 규칙

- 기존 사용자 파일과 untracked 파일을 임의로 삭제하거나 커밋하지 않는다.
- `git add .` 또는 `git add -A`를 사용하지 않는다.
- push, PR, issue, 외부 게시를 사용자의 별도 요청 없이 하지 않는다.
- raw PDF와 raw dataset을 수정하지 않는다.
- PDF는 native text·대응 LaTeX·scan/OCR층을 구분한다. 텍스트/TeX 우선으로 읽고 핵심 식·가정은 원본과 대조한다. 추출 가능 여부만으로 OCR 필요성을 판단하지 않는다. 절차: ai_dev_tool/09_PDF_원문_읽기_대조_규약.md.
- 결과를 사전에 정한 결론에 맞추지 않는다.
- 필요한 lemma는 먼저 원 논문·교정본·후속 선행증명에서 찾는다. 채택 전에는 가정,
  변수 정규화, 유효범위, 끝점, 오류항과 알려진 정정을 현재 적용과 개별 대조한다.
- 적합한 선행정리가 없거나 실제 호출로 이어지는 연결부가 빠진 경우에만 그 빈 부분을
  직접 증명한다. 표적 검색에서 찾지 못했다는 사실을 전 세계 novelty 주장으로 바꾸지 않는다.
- 수치와 표에는 source, 범위, boundary mode, 정밀도를 함께 쓴다.
- 논문 인용 시 페이지/정리/표 번호를 가능한 한 남긴다.
- 불명확한 source semantics는 추측으로 채우지 말고 blocker 또는 경고로 기록한다.

## 현재 준비 완료 항목

- 작업지시서 검토 완료
- `article/` 정본 PDF 9편, 총 253쪽 검토 완료
- `article/unverified/` 신규 원고 2편 검토 완료; peer review·독립 검증 전이라 theorem input 미채택
- 논문별 리뷰와 종합 비교 문서 준비
- `docs/METHODS.md`를 이번 연구 기준으로 교체
- FGKMT Conda 환경과 requirements 일치 확인
- iterated-log 정본 모듈과 사전검증 단위시험 준비
- GitHub source registry 및 commit-pinned immutable acquisition 코드 준비
- SQL 제한 parser, `ismax` 독립 대조, consecutive-prime 검증 코드 준비
- end-bounded interval, running minimum, jump recovery, Sono/Cramér 비교 및 plotting 코드 준비
- `test_plan/P001_...md`와 `scripts/runners/run_fgkmt_pipeline.ps1` 승인 gate 준비
- `.agents/skills`를 Codex 스킬 정본으로 정비
- 기존 연구 코드·결과 0건 확인; 폐기 또는 재생성 대상 없음
- P002 5-interval 제한 pilot 완료: validation PASS, 5 intervals, 4 jumps, runner 4.933초
- 실제 pin commit `1a112a1387052d9ad360686313f501c01fe46b68`; P002 그래프는 사용자가 큰 문제가 없다고 확인
- P003 authoritative run 완료: exit 0, runner 7.654초, 64 intervals와 63 jumps
- 모든 저장 `F/H`·envelope 수치 1,160개를 100-dps 직접식으로 검증, issue 0
- OEIS 84개와 Oliveira e Silva 별도 계산자료 75개 중첩 record 모두 일치
- log-bin·rolling 결과, 상세 결과보고서, 문헌 비교와 후속 가설, 신규 handoff 작성 완료

- P004 start/end paired, shifted log-bin, rolling `w=3,8,15,30`, x-width `0.5,1,2` decade 분석 완료
- P004 47 tests와 100-dps 독립 검증 3,747개 PASS, issue 0
- y축 최대 `10^4` 및 첫 interval 생략+y축 최대 `10^3` 그래프 생성; 사용자 시각 QA 완료
- P005 `20260824T054203Z` bounded CPU calibration PASS: canonical gaps DB 122,251 rows, Method1/2·stats/test·thread hashes 일치; Rank 85→86 exhaustive coverage는 미증명
- P006 `[2,10^8]` pilot PASS: 5,761,455 primes, 5,761,454 gaps, complete/censored plateau 24/1, artifact issue 0, 사용자 figure QA PASS
- P006 `[2,10^9]` full PASS: 50,847,534 primes, complete/censored plateau 29/1, artifact issue 0, figure 3개 사용자 QA PASS
- P007 supplied modulus-2310 pilot PASS: 480 states, 415,223 constraints, minimum slack 0, saved issue 0; historic ceil bound는 유효하지만 floor로 total upper bound를 1 낮출 수 있음
- P007 small-modulus full PASS: mod 30/210/2310 상한 단조감소; direct acceleration 미증명
- P010A/P010B modulus-30030 floating/exact lift PASS: 5,760 states, 35,224,647 constraints, lift 자체 strict improvement 0
- P008 phase-A PASS: five exact prime-count endpoints dual-algorithm 일치, actual four blocks certified zero 0; direct local tiling 음성 판정
- P009 boundary witness toy·adapter·actual single block PASS; Gate A만 통과, 전체 acceleration 미증명
- P010A G4 PASS: 4 solves·20.919초, exact violation 0, total upper bound `436001550591586306`, 약 0.7195% 개선; search acceleration 미증명
- P011 stationary recurrence null pilot PASS; enrichment 미지지, figure 사용자 QA PASS
- P012 stratified hypergeometric Q1–Q3 사용자 승인; r1 actual은 plotting TypeError로 USER_RUN_FAILED, partial 결과 비정본
- P012-A r2 terminal·saved·독립 재계산·사용자 figure QA PASS: primary obs 9 vs expected 8.5874, family p 0.21945, all enrichment BH q 1.0; LOW_INFORMATION 한계
- P012-A 통계 계약 hash 동결; P012-B range-only holdout terminal·saved·독립 산술·독립 MC replay PASS: 4 complete plateaus, obs 1 vs exp 0.497022, family p 0.093939, 최소 BH q 0.275957, 12/12 LOW_INFORMATION
- P012-B figure 자동 QA와 2026-08-28 사용자 시각 QA PASS
- P010B direct candidate-cover verifier toy PASS: 9,000 starts, candidate/exact 위험 start 69개 일치; exhaustive generator라 acceleration BLOCKED
- P013-A r1은 exact range-count gate 뒤 NumPy `ngood/nbad < 10^9` 제한으로 USER_RUN_FAILED; result directory·통계 산출물 없음
- P013-A r2 terminal·saved recomputation·artifact hash·사용자 figure QA PASS: 4 complete plateau, recurrence 0, primary 기대 `0.077829`, family p 1.0, 12/12 LOW_INFORMATION
- P013-B terminal·saved full recomputation·artifact 16/16 hash·사용자 figure QA PASS: 9 complete plateau, recurrence 0, primary 기대 `0.066797`, family p 1.0, 27/27 LOW_INFORMATION
- 실행 완료 P013-A r2·P013-B 전용 BAT/PS1은 SHA-256을 보존해 `test_done/*-done`으로 이관; 공통 `scripts/runners/run_p013_extension.ps1`은 유지
- P014 Python-side durable progress heartbeat·phase log와 console bypass 구현·targeted 6 tests/전체 151 tests/Python compile/preflight/PowerShell parser·logging self-test PASS; actual 미실행
- P016 P013 segment toy와 P014-R2 source-row exact-scan toy PASS: worker 1/2/4/8 serial exact equality, 통합 affinity `0xff` 8-process 관측, P013 68,906 gap starts·P014 synthetic mod30030 35,224,647 constraints 무누락, worker native thread=1, 전체 158 tests PASS
- P014-R2 user run은 PowerShell 5.1 JSON argv quote 손상으로 첫 preflight 전에 USER_RUN_FAILED; 과학 계산·result/progress 0, 실행 BAT/PS1은 hash 보존 `test_done` 이관
- P014-R3 EXPERIMENT_PASS / EXACT_FINITE / SCIENTIFIC_NO_IMPROVEMENT: modulus 510510의 92,160 states·8,524,288,932 constraints를 8-worker parallel과 saved full serial oracle로 violation 0 검증; 첫 5,000-constraint LP는 unbounded라 후보 0, 상한 `436001550591586306` 유지, search acceleration 미증명
- P017 P013 parallel calibration EXPERIMENT_PASS: A/B exact statistics·checkpoint·fixed-seed inference equality, A 32/B 64 segments와 worker 8개; B serial/parallel 관측비 약 4.3956, 기존 serial runner는 보존
- P017 완료 BAT/PS1 6개는 SHA-256을 보존해 `test_done/*-20260829T*-done`으로 이관
- P018 P013 information/power preflight PASS: P013-B expected 0.066797, positive-variance primary 1/9, LOW_INFORMATION 100%, 2x Poisson screening power 약 0.00817; balanced power 0.8에 필요한 null expectation 약 11.2691(현재의 약 168.7x), formal power 미인증
- 사용자 결정: B는 full-range 정식 gate, A는 prefix-only 보조 gate. WSL exact primecount 4 endpoints의 두 알고리즘 일치와 P018-P0 one-plateau calibration은 EXPERIMENT_PASS; P0는 16/17 dual partition exact equality와 saved blinded recomputation PASS지만 conditioned count·기대·분산 0인 `CALIBRATION_ONLY_NO_GATE`. P018-A actual은 64/65 dual partition·saved blinded recomputation PASS, 34,570,543,382 gap-start, conditioned count·expected·variance 0, LOW_INFORMATION 100%로 `HOLD_PREFIX_INFORMATION`이며 B 자동승격 없음. 사후감사상 gate는 `margin-only / allocation-blinded`이고 A 범위는 미래 독립 holdout이 아님
- P019 serial-oracle-free dual-partition toy PASS: 서로소 8/11 segments·worker 4, exact gap count 21, 두 full parallel pass·toy serial core 일치; shared sieve/accumulator common-mode risk 때문에 독립 증명 아님, actual 미승인
- P020 recurrence artifact synthesis R2 EXPERIMENT_PASS / SYNTHESIS_ONLY: 성공 정본 8개·중복 제거 72,178,455,399 gap-start 회계, 새 prime 계산 없음, 6개 표·PNG/PDF 12파일 saved QA PASS; stationary→stratified 기대 92.1274% 교정, 후기 information collapse 확인; 2026-09-02 사용자 figure QA PASS
- Sono/FMT numerical-threshold 감사: 출판본 대입식은 약 `2.0038612046196704e-17`이지만, Gallagher 정규화와 숨은 multiplier를 원문으로 복원한 결과 fixed `2e-17`은 현재 프로젝트에서 독립 인증되지 않음; PAP/UB·sieve/hypergraph·x→X 수치 rate와 `X_cert`, 실제 전역 최소는 OPEN
- Sono/FMT T1 원장: 66 obligations, dependency DAG와 로컬 PDF hash PASS; H1a는 모든 정수 `r>=36`에서 `J_r/I_r>log(r)/(4r)`를 project theorem으로 닫았다. H1b/H1b-1/H1c는 17·13·20행 원장을 등록했다. H1b-1a는 세 finite component를 닫았고 H1b-1b는 Lemma 8.2 multiplier 89와 GGPY absolute transfer factor 2를 닫았다. H1b-1b-2a.1은 11개 actual application의 local-factor·제외모듈 상계를 닫았고, H1b-1b-2c는 공통 \(a=1/2,A_2=8,L=5+\log\Lambda_*\)를 인증했다. H1b-1b-2d와 2d.1a/1a.1은 smooth 8/9와 line-905 scalar package를 닫았고, 2d.1b는 actual sharp scale까지 닫아 Lemma 8.4 관련 하위호출 9/9와 `H1B-L84`를 parameterized explicit으로 만들었다. 전체 moment budget이 남아 `SIV-07`은 HARD_BLOCKER, `X_cert`는 OPEN이다.
- Sono/FMT H1b-2a는 actual `L620_dW` 오차로 Lemma 8.5의 coefficient·local/global weight envelope를 닫고, plateau cube로 모든 정수 \(k\ge36\)에서 \(I_k(F)\ge(2k\log k)^{-k}\)와 절대 \(J_k\) 하한을 닫았다. H1b-2a.1은 Proposition 9.4 식 (9.66)의 마지막 두 Euler 곱을 \(e^{2+2/k}\mathfrak S_{WB}^{-1}\), 식 (9.64)의 제곱 보정까지 포함한 전체 normalization을 \(e^{2+6/k}\mathfrak S_{WB}^{-1}\) 이하로 닫았다. H1b-2a.2는 actual \(\mathcal A=\mathbb Z\)에서 식 (9.52)의 distribution child를 explicit \(\rho_{94}\)와 충분조건 \(Y_{94}\)로 닫았다. H1b-2a.3은 \(2^k\) comparison 손실을 강화 cutoff로 흡수하고 P94 child를 합성해 모든 정수 \(k\ge36\)에서 actual-call multiplier 13 미만을 얻었다. `H1B-P94`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이나 일반 P94, `SIV-07/09`, `X_cert`는 계속 열린다.
- Sono/FMT H1b-1b-2 원장은 Maynard Lemma 8.4의 실제 \(\gamma_j,c_{\gamma,j}\)를 작은 제외 소수·큰 제외 소수·비제외 소수로 분해하고 세 repair 경로를 등록했다. H1b-1b-2a.1은 모든 추적 호출에서 \(\log Q_j\le\Lambda_*\)를 증명했고, H1b-1b-2b/c는 교정된 상대 one-step multiplier와 actual 입력을 닫았다. H1b-1b-2d의 smooth finite-product 합성은 product-profile 절대오차 envelope이며 coupled main 자체의 상대오차로 과장하지 않는다. 2d.1a.1은 source scalar \(\varepsilon\)를 \(C_Y<3.17\times10^{122}\)로 인증했고, 2d.1b는 \(\xi\log x\ge(3/10)\log R\)와 strict \(C_\Sigma+2\)로 sharp factors를 닫았다. legacy \(C_{3,\mathrm{abs}}+c_\gamma\) 경로는 optional cross-check다.
- 새 장시간 Windows runner는 `scripts/common/live_native_tee.py`와 `Invoke-LiveLoggedNativeStage`로 .NET process capture 없이 stdout/stderr를 같은 PowerShell 화면과 main log에 즉시 기록; Windows PowerShell 5.1용 UTF-8 JSON Base64 transport 회귀시험 PASS
- P014-R3와 P018-P0/A 완료 BAT/PS1/SH는 SHA-256을 보존해 `test_done/*-20260901T*-done`으로 이관; P015 queue는 완료된 P013 child를 중복하므로 `DO_NOT_START`
- 결과·실패·교정 보고서 연결 정본: `test_result/00_실험결과_분석보고서_색인.md`

2026-09-09 사용자 결정: review 57의 기존 고정계수 X_cert 연구를 먼저 진행한다.
계수 개선·새 관측범위·독립 bridge 강화는 별도 후속 연구이며 자동 착수하지 않는다.
다음 권장 행동은 P018-B가 아니라 DEP-R09 `JL8` local zero-count의 source-first
multiplier·finite-range 감사다. `JL6-MELLIN`, actual truncation tail과 후속 네-part
common budget은 Theory 62--64에서 parameterized explicit로 진전해 `JL6-ACTUAL`을 닫았다.
printed general JL6은 별도 OPEN이다. JL5/JL6 cutoff 최적화나 actual prime sweep은 JL8과
뒤의 PAP 종단 multiplier가 numerical해진 뒤 필요성을 다시 판정한다.
H1b-COV2는 실제 fixed-parameter 구간 family·예외 복원·smooth remainder·순차 성공을 닫았고,
H1b-DEP는 완료했으며
P95는 actual 경로의 직접·간접 필수 입력이 아니다. general P95는 별도 OPEN이다.
theory48 actual 의존지도와 theory53 COV1은 당시 이력을 보존한다. 최신 정본은
docs/method/theory/55_Sono_FMT_H1bCOV2_post_covering_interval_smooth_composition.md와
docs/review/62_20260910_H1bCOV2_post_covering_구간_smooth_타당성검토.md다.
COV1의 full residue cap=2k·제거 질량·예외복원·partition에 이어
COV1a가 Theorem3의 충분한 C0=100을 모든 m에 대해 정량 재증명했다.
actual log gate와 R08 parameterized interface는 닫혔으나 최종 \(A,\varepsilon,\eta\),
같은 Sono 계수의 공통 budget과 X_cert는 아니다.
tuple-only survivor와 full-residue survivor를 혼동하지 않으며,
fixed-subset failure를 모든 subset의 동시 성공이나 postselection으로 확대하지 않는다.
theory52 (52.17)의 '+' 누락은 theory53 §1.1에 정정했고 pinned 원본·계약은 보존한다.
R01–R08 actual child는 parameterized explicit이며 R09–R12 4작업이 남는다.
남은 것은 numerical PAP, two-prime UB, 같은 계수의 총 예산, 최종변수 전달이다.
이 개수는 완료율이 아니다. broad SIV-07/08/09와 X_cert는 OPEN이다.
H1b-NORM은
공통 filtered moment와 fixed-X 확률 입력을 explicit하게 닫았다. H1b-P91a는 명시적 Maynard W-filter를
쓰는 actual unweighted moment와 T'=2floor(Y)의 closed shift·끝점 보정을 P92a와 같은
child cutoff에서 닫았다. 정본은 docs/method/theory/45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md다.
Maynard (7.5)의 W-coprimality indicator는 FGKMT (7.4) literal 표시에 없으므로
P91/P92/P94 certificate의 filtered construction 조건을 생략하지 않는다. literal unfiltered
weight와의 동일성은 미인증이다. shift·prime-slice에서 filter가 보존됨은 theory 45 §2를 따른다.
H1b-P92a는 actual identity weighted
P9.2와 lower weight/count atom을 \(k\ge10^{200}\)에서 multiplier 1/1로 닫았다.
정본은 docs/method/theory/44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md다.
이 child cutoff \(X\ge2\exp(10^{1000})\)는 \(X_{\rm cert}\)가 아니다.
기존 \(2^k\) 비교는 fixed-k에서 유효하지만 maximal growing-k 합성에는 사용하지 않는다.
새 \(I(F_1)\le2I(F),J(F_1)\le2J(F)\)를 P91 및 P94 growing-k gate에 적용했다.
P94g의 local scale은 T0=floor(Y)-floor(X)이며 endpoint·support 제거는 등호가 아닌 상계다.
정본은 docs/method/theory/46_Sono_FMT_H1bP94g_growing_dimension_rough_moment.md다.
명시적 h 범위와 k>=10^200에서 multiplier 1을 얻었지만 이전 13의 모든 범위를 대체하지 않는다.
공통 singular-series/lambda-square/tau/u_X 및 B0 한 항 삭제는 theory 47에서 닫혔다.
정본은 docs/method/theory/47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md다.
u_X는 고정 X/source B의 결정론적 값이며 only-k 의존성을 인증하지 않는다.
P91 4/k·P92 2/sqrt(k), 확률 상대오차 3/sqrt(k), point probability X^(-3/4)를
k>=10^200에서 얻었다. 일반 P6.1·뒤쪽 failure rate·root X_cert는 여전히 열린다.
FGKMT Theorem 6에서 P95는 불필요하지만 P94는 FMT sequel에 필요하다.
C_h=4·actual X^2 support는 닫혔고 codegree는 post-conditioning sparsity에 조건부다.
broad SIV-07/08/09는 계속 HARD_BLOCKER다.
H1과 병행할 수 있는 보조축은 explicit
primorial·Mertens·iterated-log transfer theorem 후보 수집이다. numerical threshold calculator는
모든 dependency가 explicit해진 뒤에만 만든다. P014 후속은 5,000-constraint
seed LP의 boundedness를 먼저 이론·toy로 확인하고 strict improvement 가능성이 보일 때만 새
revision을 만든다. P013-C full-decade 확대, P018-B, P019 actual runner는 새 설계·가치 gate가
확인되기 전에는 착수하지 않는다.
P015는 실행하지 않는다.
P010B large-range acceleration과 P005 Rank 85→86 exhaustive는 coverage 선결조건이 없어 runner를
만들지 않는다. 상세 영향도는 `docs/method/20260828_48h_runner_impact_analysis.md`다.
