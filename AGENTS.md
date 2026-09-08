# FGKMT-Sono Prime Gap Analysis 작업 규약

## 프로젝트 정체성

이 저장소는 검증된 maximal prime-gap record로 end-bounded \(G(x)\)를 복원하고 FGKMT large-gap scale 및 Sono의 explicit constant와 경험적으로 비교하는 계산수론 연구용이다. 후속 이론축으로 Sono의 “sufficiently large \(X\)”를 명시적 numerical threshold로 바꿀 수 있는지도 연구하되, finite observed threshold와 theorem threshold를 구분한다. 이전 실험의 모델 학습 및 GPU 벤치마크 규약은 이 저장소에 적용하지 않는다.

작업 루트:

```text
Z:\FGKMT-Sono-PrimeGap-Analysis
```

## 현재 상태: P002–P013-B PASS·시각 QA 완료 / P010A G4 PASS / P014-R3 actual PASS·상한 개선 없음 / P017 actual PASS / P018-P0/A PASS·A 정보량 HOLD / P019 toy PASS / P020 종합·시각 QA PASS / Sono-FMT H1b-1b Lemma 8.2=89·Lemma 8.4 관련 actual 하위호출 9/9 parameterized explicit / H1b-2a Lemma 8.5·8.6 finite component·H1b-2a.1 Euler normalization·H1b-2a.2 distribution child·H1b-2a.3 actual P94 multiplier 13 닫힘 / H1c-1b.1 actual identity modulus capacity·dyadic repair 닫힘 / H1c-1b.1a coefficient 보존 / H1c-1b.1a.1 `sigma y` cutoff \(x\ge2\exp(36^5)\)로 SIV-03 EXPLICIT / H1c-1b.2 fixed-scale common exceptional B·최종 12항 raw psi dyadic composition 닫힘 / H1c-1b.3 Abel·prime-power·half-open·exact-center count transfer 닫힘 / SIV-07·08 HARD_BLOCKER / X_cert OPEN

P002 pilot, P003 전체 `10^20` end-bounded 분석, P004 start/end 경계·local-envelope 민감도 분석이 완료됐다. P004 authoritative run `20260823T075238Z_p004_sensitivity`는 64 end/start paired intervals와 100-dps 수치·정수 3,747개를 issue 0으로 검증했고, 사용자가 y축 제한 새 그래프도 큰 문제없다고 확인했다.

P004 해석 정본은 `test_result/202608231652_P004_sensitivity_analysis.md`다. P005 bounded CPU calibration, P006 `[2,10^9]`, P007 modulus 30/210/2310 비교, P008 toy·exact prime-count·phase-A full은 모두 terminal/saved verification PASS다. P009 actual `[10^20,10^20+1000)`은 internal zero와 exact boundary witness를 결합해 certified zero 1 block을 만들었다. P010A G4는 modulus 30030의 35,224,647 constraints를 exact 검증해 count 상한을 `436,001,550,591,586,306`으로 약 0.7195% 낮췄지만 acceleration은 미증명이다. P011–P013-B recurrence 계열은 enrichment를 검출하지 못했다. P013-A/B는 각각 primary 기대 0.077829/0.066797, 관측 0, 모든 행 LOW_INFORMATION이며 사용자 figure QA까지 PASS했다. P017 combined queue와 A/B child는 terminal·saved·exact equality PASS다. P017-B 동일범위 serial 12,598.410초 대 parallel 2,866.160초로 관측 wall-time 비가 약 4.3956이었다. P014-R3는 modulus 510510의 92,160 states와 8,524,288,932 constraints를 parallel exact scan과 saved serial oracle로 issue 0 검증했지만, 첫 5,000-constraint LP가 unbounded라 새 후보를 만들지 못했고 상한은 G4와 같은 `436,001,550,591,586,306`이다. 따라서 실행은 PASS지만 과학적 결과는 `NO_IMPROVEMENT`이고 search acceleration은 미증명이다. P018 read-only 사전판정 뒤 사용자는 full-range 정식 gate로 균형형 B, prefix 보조 gate로 탐색형 A를 동결했다. exact prime-count 준비와 P018-P0 one-plateau calibration은 terminal·saved·dual-partition 검증 PASS다. P0는 gap 582의 forced record 제거 뒤 conditioned count·기대값·분산이 모두 0인 calibration-only 결과였고 A/B gate를 판정하지 않았다. P018-A actual은 34,570,543,382 gap-start를 64/65 dual partition과 saved blinded recomputation으로 issue 0 검증했지만 primary gap 582·588 모두 forced record 제거 뒤 conditioned count·expected·variance가 0이고 LOW_INFORMATION이 100%였다. 따라서 실행은 `EXPERIMENT_PASS`, 과학적 판정은 `HOLD_PREFIX_INFORMATION`이며 B 자동승격은 없다. 2026-09-02 사후감사는 이 gate가 강한 outcome-blind가 아니라 `margin-only / allocation-blinded`임을 확인했다. zero conditioned margin은 recurrence 0을 드러내므로 A 범위는 미래 독립 holdout이 아니다. P020은 성공 정본 8개를 새 prime 계산 없이 종합해 72,178,455,399 gap-start 회계와 6개 figure family를 saved 검증했다. stationary→stratified 기대는 92.1274% 교정됐고, 후기 범위에서 계산량이 정보량을 보장하지 않음을 확인했다. 2026-09-02 사용자 figure QA도 PASS했다. Sono/FMT 1차 threshold 감사는 coefficient가 explicit·proof가 effective-in-principle이지만 numerical `X_cert`를 내려면 PAP/UB·sieve weight·hypergraph probability·x→X의 수치 rate가 더 필요함을 확인했다. `X_emp(10^20)=3,814,280`은 finite exact이고 `X_cert`와 실제 전역 최소는 OPEN이다. 정본은 `docs/review/21_20260902_P018_recurrence_설계사후감사_전체시각화_타당성검토.md`, `test_result/202609021151_P020_recurrence_artifact_synthesis_result_analysis.md`, `docs/review/22_20260902_Sono_FMT_numerical_threshold_proof_dependency_audit.md`다. P019는 serial 정답표 없는 future 범위의 서로소 dual-partition parallel full-pass toy를 exact count 21로 검증했지만 actual runner는 없다. P014-R2 transport 실패와 P014-R3/P018-P0/A 완료 실행기는 hash 보존해 `test_done` 이관했다. P015 queue는 완료 P013 child를 중복하므로 실행하지 않는다. 결과 연결 정본은 `test_result/00_실험결과_분석보고서_색인.md`다. 추가 actual 실행, 외부 게시, commit/push/PR은 별도 사용자 행동·승인 없이 수행하지 않는다.

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
Bordignon 2021 Theorem 1.4가 `PRIMARY_COMPOSITION_CANDIDATE`다. affine modulus, 한 공통
exceptional \(B\), \(\psi\to\pi\), recentering, density와 common cutoff가 남아
`SIV-08`도 계속 `HARD_BLOCKER`다. H1c-1b.1은 outer \(k_{\mathrm{chain}}=1\)과
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
\(R_B(T)+R_B(2T)\)로 합성했다. H1c-1b.3은 같은 family가 Abel 적분 전체에서 유효함을
확인하고 올바른 plus 부호의 partial summation, prime-power 비용
\(2\sqrt{2T}(M_B+\Phi_B)\), half-open endpoint 비용 \(M_B\)와 exact total prime
population 중심을 보존해 actual unweighted \([T,2T)\) count transfer를 닫았다. density,
Bordignon source 상수 정규화와 12항·count 비용의 공통 cutoff는 열려 있다. 다음 gate는
H1c-1b.4 full absorption이다. 모든 root
dependency가 닫히기 전에는 새 prime sweep·threshold calculator를 만들지 않는다.

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
6. `docs/review/00_문헌_종합_분석.md` - 현재 9편 corpus의 종합 판정
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
article/          검토 완료 정본 선행논문 PDF 9편; 원본 수정 금지
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

- Sono의 `2.0e-17`은 증명된 보수적 상수이지 관측값의 예상 극한이 아니다.
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
- Sono/FMT numerical-threshold 1차 audit: 대입 계수 약 `2.0038612046196704e-17`, `2e-17`은 proved coefficient이나 출판본의 numerical `X_cert`는 없음; top-level proof는 effective-in-principle, PAP/UB·sieve/hypergraph·x→X 수치 rate가 blocker; 실제 전역 최소도 OPEN
- Sono/FMT T1 원장: 66 obligations, dependency DAG와 로컬 PDF hash PASS; H1a는 모든 정수 `r>=36`에서 `J_r/I_r>log(r)/(4r)`를 project theorem으로 닫았다. H1b/H1b-1/H1c는 17·13·20행 원장을 등록했다. H1b-1a는 세 finite component를 닫았고 H1b-1b는 Lemma 8.2 multiplier 89와 GGPY absolute transfer factor 2를 닫았다. H1b-1b-2a.1은 11개 actual application의 local-factor·제외모듈 상계를 닫았고, H1b-1b-2c는 공통 \(a=1/2,A_2=8,L=5+\log\Lambda_*\)를 인증했다. H1b-1b-2d와 2d.1a/1a.1은 smooth 8/9와 line-905 scalar package를 닫았고, 2d.1b는 actual sharp scale까지 닫아 Lemma 8.4 관련 하위호출 9/9와 `H1B-L84`를 parameterized explicit으로 만들었다. 전체 moment budget이 남아 `SIV-07`은 HARD_BLOCKER, `X_cert`는 OPEN이다.
- Sono/FMT H1b-2a는 actual `L620_dW` 오차로 Lemma 8.5의 coefficient·local/global weight envelope를 닫고, plateau cube로 모든 정수 \(k\ge36\)에서 \(I_k(F)\ge(2k\log k)^{-k}\)와 절대 \(J_k\) 하한을 닫았다. H1b-2a.1은 Proposition 9.4 식 (9.66)의 마지막 두 Euler 곱을 \(e^{2+2/k}\mathfrak S_{WB}^{-1}\), 식 (9.64)의 제곱 보정까지 포함한 전체 normalization을 \(e^{2+6/k}\mathfrak S_{WB}^{-1}\) 이하로 닫았다. H1b-2a.2는 actual \(\mathcal A=\mathbb Z\)에서 식 (9.52)의 distribution child를 explicit \(\rho_{94}\)와 충분조건 \(Y_{94}\)로 닫았다. H1b-2a.3은 \(2^k\) comparison 손실을 강화 cutoff로 흡수하고 P94 child를 합성해 모든 정수 \(k\ge36\)에서 actual-call multiplier 13 미만을 얻었다. `H1B-P94`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이나 일반 P94, `SIV-07/09`, `X_cert`는 계속 열린다.
- Sono/FMT H1b-1b-2 원장은 Maynard Lemma 8.4의 실제 \(\gamma_j,c_{\gamma,j}\)를 작은 제외 소수·큰 제외 소수·비제외 소수로 분해하고 세 repair 경로를 등록했다. H1b-1b-2a.1은 모든 추적 호출에서 \(\log Q_j\le\Lambda_*\)를 증명했고, H1b-1b-2b/c는 교정된 상대 one-step multiplier와 actual 입력을 닫았다. H1b-1b-2d의 smooth finite-product 합성은 product-profile 절대오차 envelope이며 coupled main 자체의 상대오차로 과장하지 않는다. 2d.1a.1은 source scalar \(\varepsilon\)를 \(C_Y<3.17\times10^{122}\)로 인증했고, 2d.1b는 \(\xi\log x\ge(3/10)\log R\)와 strict \(C_\Sigma+2\)로 sharp factors를 닫았다. legacy \(C_{3,\mathrm{abs}}+c_\gamma\) 경로는 optional cross-check다.
- 새 장시간 Windows runner는 `scripts/common/live_native_tee.py`와 `Invoke-LiveLoggedNativeStage`로 .NET process capture 없이 stdout/stderr를 같은 PowerShell 화면과 main log에 즉시 기록; Windows PowerShell 5.1용 UTF-8 JSON Base64 transport 회귀시험 PASS
- P014-R3와 P018-P0/A 완료 BAT/PS1/SH는 SHA-256을 보존해 `test_done/*-20260901T*-done`으로 이관; P015 queue는 완료된 P013 child를 중복하므로 `DO_NOT_START`
- 결과·실패·교정 보고서 연결 정본: `test_result/00_실험결과_분석보고서_색인.md`

다음 권장 행동은 P018-B를 자동 실행하지 않고 H1c-1b.4로 진행하는 것이다.
H1c-1b.3이 endpoint·prime-power·\(\psi\to\pi\)·exact recentering을 닫았으므로,
H1c-1b.4에서 Bordignon source 상수 정규화, exact represented-prime density와
full-remainder/count-transfer absorption·common cutoff를 합성한다. actual P94 식 (9.52)의
직접 선결조건으로 다시 연결하지 않는다.
그 뒤 P91/P92/L93/P95와 공통 moment error budget을 합성한다.
H1과 병행할 수 있는 보조축은 explicit
primorial·Mertens·iterated-log transfer theorem 후보 수집이다. numerical threshold calculator는
모든 dependency가 explicit해진 뒤에만 만든다. P014 후속은 5,000-constraint
seed LP의 boundedness를 먼저 이론·toy로 확인하고 strict improvement 가능성이 보일 때만 새
revision을 만든다. P013-C full-decade 확대, P018-B, P019 actual runner는 새 설계·가치 gate가
확인되기 전에는 착수하지 않는다.
P015는 실행하지 않는다.
P010B large-range acceleration과 P005 Rank 85→86 exhaustive는 coverage 선결조건이 없어 runner를
만들지 않는다. 상세 영향도는 `docs/method/20260828_48h_runner_impact_analysis.md`다.
