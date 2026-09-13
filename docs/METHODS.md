# FGKMT-Sono maximal prime gap 비교 방법론

## 0. 문서 상태와 실행 경계

이 문서는 `Z:\FGKMT-Sono-PrimeGap-Analysis`에서 수행할 대형 소수간격 비교 실험의 방법론 정본이다.

- 현재 단계: P003/P004 본체, P005–P014-R3 실제 실행, P017 병렬 보정, P018 exact prime-count·P0·A와 설계 사후감사, P020 recurrence artifact 종합 완료; A는 정보량 HOLD
- 완료 승인 범위: P003/P004 분석, P005 calibration, P006–P014-R3 실제 실행·사후 검증, P017 exact-equivalence calibration, P018-P0/A margin-only information pipeline·사후감사, P020 저장 artifact 전수 종합 시각화
- 현재 미실행 범위: P018-B, P019 actual, P013-C, P010B large-range acceleration, 외부 게시, commit/push/PR
- 2026-09-09 최신 승인: 완료 proof 단계의 로컬 staging/commit은 허가됐다. push/PR·actual 확대는 여전히 별도 승인 대상이다.
- 최신 proof 상태: COR1–COR3/COV1–COV2가 R01–R08 actual child를 닫았다. COV1a는 Theorem3의 충분한 C0=100을 정량 재증명했고, COV2는 endpoint-safe equal grid, actual-width 예외복원, outer→inner 순차 성공과 special-case smooth remainder를 fixed \(A,\varepsilon,\eta\)에서 parameterized explicit으로 합성했다. R09 full-source 감사에서는 Sono Proposition 5.3→Gallagher zero-free constant 정규화와 숨은 multiplier 소거가 현재 원문으로 인증되지 않음을 확인했다. numerical PAP/UB·같은 Sono 계수 총예산·최종변수(R09–R12)는 OPEN이다. 같은 Sono 계수를 목표로 유지하되, PAP repair 전에는 X_cert·계산기·R11·독립 형식인증으로 승격하지 않는다.
- 다음 단계: P018-B를 자동 실행하지 않는다. Sono/FMT H1a와 H1b-1 계열은 finite-r 적분비, Lemma 8.2 multiplier 89, 교정된 \(\kappa=1\) one-step multiplier, 실제 제외모듈과 Lemma 8.4 관련 하위호출 9/9를 parameterized explicit 수준으로 닫았다.
  2026-09-08 H1b-2a는 Lemma 8.5의 coefficient·weight envelope와 Lemma 8.6의 절대 \(I_k,J_k\) 크기 및 보수적 \(F_1/F_2\) 비교를 유한식으로 닫았다. H1b-2a.1은 Proposition 9.4 식 (9.66)의 마지막 두 Euler 곱도 exact local factor와 finite singular-series 비교로 닫았다.
  H1b-2a.2는 실제 \(\mathcal A=\mathbb Z,D=1\) 호출의 정확한 \(E_q^{(1)}\le1\)을 이용해 식 (9.52) distribution child를 parameterized explicit으로 닫았다. H1b-2a.3은 actual FGKMT/FMT P94의 모든 닫힌 child를 공통 cutoff로 합성해 모든 정수 \(k\ge36\)에서 multiplier 13 미만을 얻었고, `H1B-P94=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 승격했다. 2026-09-09 H1c-1a는 quantitative character/Bombieri–Vinogradov source inventory를 완료했고, H1c-1b.1은 actual Proposition 9.2의 identity form에 대해 Bordignon 2021의 pointwise growing-\(A\) 대입과 modulus capacity를 닫았다. H1c-1b.1a는 endpoint-safe \(r_T=\lfloor(\log(x/2))^{1/5}\rfloor\)와 실제 \(R=(x/4)^{\theta/3}\)를 사용해 두 finite normalization factor의 곱이 \(39/40\)보다 큼을 exact하게 증명했다. H1c-1b.1a.1은 Rosser--Schoenfeld Theorem 7과 제외 prime 보정을 합성해 \(x\ge2\exp(36^5)\)에서 \(\sigma y<(1001000/998001)80cx\log_2x<(26/25)80cx\log_2x\)를 증명했다. 따라서 `SIV-03=EXPLICIT`이고 Sono의 같은 \(2\times10^{-17}\) 계수가 이 단계에서 유지된다. H1c-1b.2는 fixed \(Q_1\)에서 두 endpoint에 한 exceptional modulus와 그 prime divisor \(B\)를 공통으로 쓰고, 최종 NYJM판 12항을 이용한 raw \((T,2T]\) \(\psi\) composition을 닫았다. H1c-1b.3r1은 Maynard 원문의 일반 \([T,2T)\)와 FGKMT actual \([T,2T]\)를 구분하고 closed target의 한 lower atom을 안전하게 보정했다. H1c-1b.4a–4e는 source 정규화·density·full absorption을 합성해 \(X\ge2\exp(10^{50})\)에서 actual identity-form Hypothesis 1 input을 constants \((1,1,2)\)로 explicit하게 닫았다. 후속 H1b-P92a는 \(k\ge10^{200}\)에서 actual identity weighted P9.2와 lower weight/count atom을 multiplier 1/1로 닫았다. child cutoff \(X\ge2\exp(10^{1000})\)는 전체 threshold가 아니다. H1b-P91a는 filtered unweighted moment·shift를, H1b-P94g는 actual shifted T0의 growing-dimension P94 multiplier 1을 닫았다. 이 1은 더 강한 새 regime의 값이고 기존 13을 보편적으로 대체하지 않는다. 후속 H1b-NORM은 공통 singular-series/lambda-square/tau/u_X와 B0 삭제·확률 입력까지 닫았다. H1b-DEP가 actual dependency를 분리했고 다음은 뒤쪽 finite correlation/failure rate다. `SIV-07/08=HARD_BLOCKER`, `X_cert=OPEN`은 유지하고 P020 figure는 2026-09-02 사용자 시각 QA까지 PASS했다.

모든 실패·성공 로그는 독립 run id로 보존하며 기존 산출물을 덮어쓰지 않는다.

## 1. 연구 목적

2026-09-09 사용자 결정은
[review 57](review/57_20260909_연구방향_세가지제안_비교검토.md)의 기존 고정계수
X_cert 방향 우선이다. 다른 계수·새 관측범위·독립 bridge 강화는 별도 후속 연구다.
review 56의 유한 bridge는 같은 방향의 보조 근거로만 유지하며 무한 tail 완료로 해석하지 않는다.

검증된 maximal prime-gap records를 이용해 end-bounded 실제 maximal gap

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

을 복원하고 FGKMT large-gap asymptotic scale에 대한 \(H(x)=G(x)/F(x)\)의 변화와 lower envelope를 분석한다. record 사이의 감소, 새 record에서의 회복, interval minima, global running minimum과 local empirical envelope, Wolf 계열 경험적 관찰, Sono explicit constant와의 정량적 격차를 조사한다.

유한 계산으로 FGKMT 또는 Sono의 무한 범위 정리를 재증명·검증하지 않으며, 계산 범위의 부등식을 모든 더 큰 \(x\)로 일반화하지 않는다. 관찰 패턴은 empirical statement로 분리한다. 동시에 Sono의 “sufficiently large \(X\)”를 실제 숫자로 바꾸는 explicit-threshold 연구를 별도 이론축으로 둔다. 첫 목표는 증명 가능한 유한 상한 \(X_0^{\mathrm{cert}}\)의 도출 가능성을 판정하는 것이며, 이를 유한 자료의 첫 관측점이나 실제 전역 최소 threshold와 혼동하지 않는다.

자연로그와 반복로그를 다음과 같이 정의한다.

\[
\log_1 x=\log x,\quad
\log_2 x=\log\log x,\quad
\log_3 x=\log\log\log x,\quad
\log_4 x=\log\log\log\log x.
\]

여기서 아래 첨자 \(k\)는 로그의 밑이 아니라 자연로그를 적용한 횟수다. 즉,

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 반복}}
\]

이며, 특히

\[
\log_2(x)=\ln(\ln x),\quad
\log_3(x)=\ln(\ln(\ln x)),\quad
\log_4(x)=\ln(\ln(\ln(\ln x))).
\]

FGKMT scale은

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x}
\]

로 둔다. 주 분석량은

\[
H(x)=\frac{G(x)}{F(x)},\qquad
Q(x)=\frac{H(x)}{c_{\mathrm{Sono}}},\qquad
c_{\mathrm{Sono}}=2.0\times10^{-17}
\]

이다.

### 1.1 반복로그 구현 계약과 사전검증

정본 구현은 `source/definitions.py`의 `iter_log`와 `F`다. 최소 작업 정밀도는 `mpmath` 50 decimal digits로 고정한다.

```python
import mpmath as mp

mp.mp.dps = 50

def iter_log(x, n):
    value = mp.mpf(x)
    for _ in range(n):
        value = mp.log(value)
    return value

def F(x):
    log1 = iter_log(x, 1)
    log2 = iter_log(x, 2)
    log3 = iter_log(x, 3)
    log4 = iter_log(x, 4)
    return log1 * log2 * log4 / log3
```

다음은 base-\(k\) 로그이므로 연구 계산 코드에서 금지한다.

```python
math.log(x, 2)
math.log(x, 3)
math.log(x, 4)
numpy.log2(x)
```

단위시험에서 위 base-\(k\) 값을 negative control로 계산해 iterated natural logarithm과 서로 다름을 검증하는 경우만 예외다. 실제 데이터 단계로 가기 전에 반드시 아래 명령을 통과시킨다.

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest discover -s tests -v
```

필수 preflight 판정은 다음과 같다.

1. `iter_log(x, 2|3|4)`가 직접 중첩한 `mp.log`와 고정밀도로 일치한다.
2. 위 값이 밑이 2, 3, 4인 로그와 각각 다르다.
3. `F(x)`가 풀어 쓴 식과 일치한다.
4. `source/`에서 base-\(k\) 로그 호출이 발견되지 않는다.
5. `x=16`의 음의 \(F\)와 `X_SCALE_POSITIVE_MIN=3_814_280`의 양의 \(F\)를 재확인한다.

정의 오류가 발견된 코드로 계산한 결과는 부분 수정하지 않는다. 해당 실행의 `F`, `H`, Sono ratio \(Q\), interval-wise minimum, running minimum, 그래프와 통계 요약을 모두 무효 처리한 뒤 교정된 코드와 동일 입력으로 전부 재생성한다.

## 2. 정리 계보와 상수의 의미

### 2.1 FGKMT와 FMT를 구분한다

- Ford-Green-Konyagin-Maynard-Tao(2018)는 `LONG GAPS BETWEEN PRIMES`에서 start-bounded \(G(X)\)에 대해 \(G(X)\gg F(X)\)를 증명했다.
- Sono가 수치화한 \(c_{\mathrm{LG}}\)는 Ford-Maynard-Tao의 `Chains of large gaps between primes`에 제시된 \(G_k(X)\) 정리의 explicit constant이다.
- \(k=1\)이면 동일한 함수형 scale을 갖지만, “Sono가 FGKMT 5인 논문의 숨은 상수를 그대로 계산했다”고 쓰지 않는다.

Sono의 2025년 출판본은 [An explicit lower bound for large gaps between some consecutive primes](https://doi.org/10.4418/2025.80.2.2)이며, 현재 `article/`의 6번째 PDF와 `docs/review/06_Sono_2025.md`에서 직접 검토했다.

### 2.2 상수와 threshold

Sono 결과는 고정된 \(k\)와 충분히 큰 \(X\)에 대해

\[
G_k(X)\ge \frac{c_{\mathrm{LG}}}{k^2}F(X),
\qquad c_{\mathrm{LG}}\ge2.0\times10^{-17}
\]

형태이다.

- `2.0e-17`은 경험적 예상값이나 극한값이 아니라 Sono 출판본이 제시한 보수적 계수이다. 다만 이 프로젝트의 2026-09-11 full-source 감사에서는 PAP zero-free 정규화와 숨은 multiplier를 독립 복원하지 못했으므로, 현재 상태는 `PUBLICATION_CLAIM_NOT_PROJECT_CERTIFIED`다.
- 정리의 문구는 “for any sufficiently large X”이며, 출판본에 바로 사용할 수 있는 수치 \(X_0\)가 제시되어 있지 않다.
- 유한 데이터에서 \(H(x)<c_{\mathrm{Sono}}\)가 나와도 정의와 계산이 맞다면 정리 반례가 아니라 그 \(x\)가 보장 구간 밖이라는 정보이다.
- 유한 데이터에서 항상 \(H(x)\ge c_{\mathrm{Sono}}\)여도 정리를 계산으로 입증한 것이 아니다.

### 2.2.1 threshold 연구의 세 수준

Sono의 \(k=1\) explicit inequality에 대해 다음 세 양을 분리한다.

1. 검증 상한 \(B\)까지의 유한 관측 threshold

   \[
   X_{\mathrm{emp}}(B)=\min\{x_0\ge X_{\mathrm{scale+}}:
   H(x)\ge c_{\mathrm{Sono}}\text{ for all integers }x_0\le x\le B\}.
   \]

   P003의 정본 범위에서는 \(X_{\mathrm{scale+}}=3{,}814{,}280\), \(B=10^{20}\)이고 전체
   interval의 최소 \(H\approx37.8168604>2\times10^{-17}\)이므로
   \(X_{\mathrm{emp}}(10^{20})=3{,}814{,}280\)이다. 이는 분석 정의역 안의 exact finite 사실이다.

2. 증명이 보장하는 명시적 threshold

   \[
   X_{\mathrm{proof}}=\min\{X_0:\text{현재 증명이 모든 }X\ge X_0\text{에서 부등식을 보장}\}.
   \]

   Sono 출판본은 numerical \(X_0\)를 제공하지 않는다. 이를 만들려면 증명의 \(o(1)\), analytic
   estimates, sieve·covering parameter를 모두 effective inequality로 추적해야 한다. 먼저 어떤
   값이라도 증명 가능한 \(X_0^{\mathrm{cert}}\)를 만들고, 이후 상한을 낮춘다.

3. 실제 부등식의 가장 작은 전역 threshold

   후보 이후의 무한 tail 전체 성립과 더 작은 후보의 배제를 함께 증명해야 한다. 유한 record
   계산만으로는 정할 수 없다. 특히 `3,814,280`은 \(F>0\)인 분석 시작점이지 Sono 정리가 보장한
   threshold가 아니다.

Sono가 직접 explicit화한 것은 FMT chain theorem이며, FGKMT는 같은 large-gap scale의 중요한
결과다. 따라서 문서에는 “FGKMT/FMT 계열 scale과 Sono \(k=1\) explicit inequality의 threshold
연구”라고 쓰고 Sono 상수를 FGKMT 5인 논문의 명시 상수로 돌리지 않는다.

### 2.3 Wolf 기준선의 지위

\(H=1\)은 작업지시서에 따른 경험적 참고선으로만 표시한다. Kourbatov-Wolf 2020(p. 2)은 FGKMT 함수형 lower bound가 계산상 \(A=1\)로 성립한다는 2차 진술을 제공하지만 exact \(H\) envelope나 극한을 입증하지 않는다. 따라서 그래프 범례는 `Kourbatov-Wolf 2020 empirical reference H=1 (not a theorem)`처럼 쓰고, “Wolf가 \(c=1\)을 증명했다”거나 “\(H\to1\)을 예측했다”고 단정하지 않는다.

## 3. maximal gap 경계 정의

record gap을 시작 소수 \(s_i\), gap \(g_i\), 끝 소수 \(e_i=s_i+g_i\)로 기록한다.

### 3.1 canonical end-bounded 정의

사용자가 지정한 연구 정본이며 Sono의 \(G_1(X)\), Kourbatov-Wolf 2019의 정의와 맞춘다.

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n).
\]

record \(i\)의 점프 위치는 \(e_i\)이다.

### 3.2 source와 분석 경계의 변환

- Prime Gap List Project의 high-watermark 표는 작은 start prime이 있는지로 record를 배열한다.
- 원본의 `startprime`과 `gapsize`로 \(e_i=s_i+g_i\)를 계산한 뒤 분석 jump를 end prime으로 변환한다.
- 모든 표·그래프·요약에 `boundary_mode=end`와 `G definition: end_prime <= x`를 기록한다.
- start-bounded 보조 계열은 P004 전용 파일과 변수명으로 격리하고 canonical end-bounded 계열을 교체하지 않는다.

## 4. 반복로그 도메인과 분석 시작점

\(F(x)\)는 실수식으로는 정수 \(x=16\)부터 계산할 수 있지만, 이때 \(\log_4x<0\)이므로 양의 lower-bound scale 비교에는 부적합하다. \(F(x)>0\)이 되는 조건은

\[
\log_4x>0
\iff x>e^{e^e}=3814279.1047602205\ldots
\]

이다. 따라서

```text
X_SCALE_POSITIVE_MIN = 3_814_280
```

을 theorem-scale 분석의 최소 정수로 고정한다.

- `16 <= x < 3_814_280`은 반복로그 도메인 진단표에만 포함할 수 있다.
- 이 초기 구간을 \(H\), \(Q\), global running minimum에 포함하지 않는다.
- \(\log_4x=0\) 부근의 부호 변화와 작은 분모가 전체 결과를 지배하지 않도록 한다.
- 양의 scale 구간에서 \(F(x)\)의 단조증가를 수식 검토와 수치 단위시험으로 모두 확인한다.

## 5. interval-wise minimum과 envelope

점프 위치 \(e_i\)에 대해

\[
e_i\le x<e_{i+1}\quad\Longrightarrow\quad G(x)=g_i.
\]

정수 구간을 양의 scale 시작점으로 자른다.

\[
\ell_i=\max(e_i, X_{\mathrm{scale+}}),\qquad
r_i=e_{i+1}-1.
\]

\(\ell_i\le r_i\)이고 \(F\)가 증가하는 구간에서 정확한 interval minimum은

\[
H_i^{\min}=\frac{g_i}{F(r_i)}
\]

여기서 “정확한 minimum”은 프로젝트가 고정한 정수 격자 `x in Z`에 대한 말이다. 논문의 변수를 실수 `X` 전체로 연장하면 plateau는 `[e_i,e_(i+1))`이고 오른쪽 끝이 포함되지 않으므로 minimum은 일반적으로 달성되지 않는다. 그 경우 대응하는 양은
`inf H(X) = g_i/F(e_(i+1))`, 즉 `X -> e_(i+1)-`의 극한이다. 현재 코드·CSV·log-bin은 일관되게 정수 domain을 사용한다.

마지막 record는 다음 record가 없으므로 `verified_exhaustive_limit` 또는 사용자가 승인한 분석 상한까지만 닫는다. 검증범위를 넘어 무한히 연장하지 않는다.

running minimum은

\[
M(X)=\min_{X_{\mathrm{scale+}}\le x\le X}H(x)
\]

로 정의한다. 정의상 \(M(X)\)는 단조 비증가한다. 따라서 “증가”나 “상하 요동”은 global running minimum의 가능한 패턴이 아니다. 1차 분석에서는 interval minima 궤적과 ln H 대 ln x의 descriptive slope·correlation을 함께 산출한다.

P003에서는 다음 두 local envelope를 실행 전에 고정한다.

1. 정수 decade log-bin

\[
(10^k,10^{k+1}]\cap[3{,}814{,}280,10^{20}]
\]

즉 정수 범위 `[10^k+1,10^(k+1)]`을 사용하고 첫·마지막 bin은 분석 범위로 clip한다. 각 bin과 겹치는 모든 end-bounded interval에서 겹침의 오른쪽 끝을 평가한 뒤 가장 작은 `H`를 정확한 bin minimum으로 선택한다.

2. 고정 record-window rolling minimum

interval-minimum sequence에서 직전 `w`개 record interval의 최소를 계산하며 `w=5,10,20`을 주 window로 고정한다. window가 완전히 찬 지점부터만 산출한다. 오래된 최저값이 window 밖으로 빠지면 이 local 지표는 상승할 수 있다.

고정 log-width robust quantile은 P003 정본 산출물에 포함하지 않고 후속 민감도 분석 후보로 남긴다. global running minimum에서는 새 최저치와 plateau만 해석한다.

### 5.1 결과 표의 경계 필드

각 interval 행에는 gap의 `start_prime`, `end_prime`, canonical `[x_left,x_right]`, `F(x_left)`, `F(x_right)`, `H(x_left)`, `H_interval_min`을 함께 저장한다. `start_prime`은 provenance와 사람이 읽는 식별자일 뿐 interval 시작점으로 사용하지 않는다.

Sono 원문의 `G_1(X)`는 `end_prime <= X`여서 현재 함수와 정확히 일치한다. FGKMT 2018 원문의 `G(X)`는 `start_prime <= X`이므로 유한 계단함수는 다르다. 현재 연구는 end-bounded `G`와 Sono를 직접 비교하고, FGKMT는 동일한 large-gap scale의 이론적 출처로 구분해 비교한다.

## 6. 데이터 정책

### 6.1 우선순위

1. 정본 입력: [Prime Gap List Project GitHub 저장소](https://github.com/primegap-list-project/prime-gap-list)의 commit-pinned `allgaps.sql`
2. 참고 표: `prime-gaps-high-watermarks` 웹페이지(입력으로 사용하지 않음)
3. exhaustive limit: `fully-analyzed` 페이지와 연결된 원 발표
4. Oliveira e Silva-Herzog-Pardi 자료의 중첩 범위 교차검증

준비 시점(2026-08-22 UTC)에 `master`는 `1a112a1387052d9ad360686313f501c01fe46b68`로 확인했다. 실제 취득 시 다시 resolve하고 그 시점의 40자 commit으로 raw URL을 고정한다. 현재 웹페이지가 명시한 exhaustive upper bound는 2026-05-08의 \(10^{20}\)이다.

전체 소수를 상한까지 다시 생성하지 않는다. 이 연구의 1차 데이터 단위는 record gap이다.

### 6.2 원본 보존

승인 후 사용할 구조는 다음과 같다.

```text
datas/
  raw/prime-gap-list-project/<commit>/
    allgaps.sql     # 다운로드 원본, 수정·덮어쓰기 금지
    schema.sql      # 같은 commit의 upstream schema
    metadata.json   # 두 파일의 commit, URL, 취득 UTC, byte 수, SHA-256
  validated/prime-gap-list-project/<commit>/
    maximal_gap_records.csv
    validation_report.json
```

각 원본에 다음 메타데이터를 남긴다.

```text
source_url
retrieved_at_utc
publisher_or_maintainer
source_version_or_date
sha256
license_or_usage_note
column_semantics
boundary_semantics
record_count
claimed_exhaustive_limit
parser_version
```

원본과 사람이 수정한 CSV를 같은 경로에 두지 않는다.

### 6.3 필수 열

정규화 데이터의 최소 schema:

```text
record_index
start_prime
gap
end_prime
source_id
source_row_id
source_commit
verified_exhaustive_limit
```

큰 정수는 float로 변환하지 않는다. CSV에서는 10진 문자열로 직렬화하고 Python `int`로 복원한다. Parquet을 추가할 경우 `int64`가 \(10^{20}\)을 담지 못하므로 decimal 또는 string schema를 명시하기 전에는 사용하지 않는다.

### 6.4 검증 항목

- `end_prime == start_prime + gap`
- `start_prime` 엄격 증가
- `end_prime` 엄격 증가
- record `gap` 엄격 증가
- published `ismax=1`과 eligible first-occurrence rows에서 독립 재구성한 high watermark의 완전 일치
- `gmpy2.next_prime(start_prime) == end_prime` 보조검사
- 중첩 출처 간 `(start_prime, gap, end_prime)` 일치
- source가 주장한 record 수와 exhaustive limit 일치
- 시작점/끝점 경계 의미를 metadata와 결과에 보존
- 미검증 확장 record와 exhaustive verified 범위를 별도 표시

probable-prime 검사만으로 exhaustive completeness를 주장하지 않는다.

## 7. 계산 정밀도

- 모든 로그의 밑은 \(e\)이다.
- record 소수는 Python `int`로 유지한다.
- 반복로그와 비율은 `mpmath`로 계산하고 작업 정밀도(`mp.dps`)를 결과 metadata에 기록한다.
- 정본 50-dps 계산은 `source.definitions.F/H`를 호출하지 않는 별도 100-dps 직접 중첩식으로 전수 교차검증한다. float64를 사용할 경우 진단값일 뿐 정본으로 삼지 않는다.
- CSV에는 표시용 반올림 값과 재계산 가능한 고정밀 문자열을 구분한다.
- Sono 대비 배수 \(Q\)는 매우 크므로 선형축과 로그축을 혼동하지 않는다.

## 8. 재현 가능한 단계

각 단계는 독립적으로 재실행 가능해야 하며, 이전 단계의 hash를 입력 metadata에 기록한다.

### P0 - 준비(완료)

- 작업지시서 검토
- PDF 9편 분석
- 정의 충돌과 도메인 교정
- Conda 환경 검증
- iterated-log 정본 모듈과 negative-control 단위시험 검증
- 기존 코드와 결과의 base-\(k\) 오염 여부 정적 감사
- GitHub allgaps.sql 제한 parser, schema.sql 검증, immutable acquisition, end-bounded interval/jump 분석 코드 작성
- toy record 기반 parser·high-watermark·interval·승인 gate 단위시험
- P003 실행 승인, 계획 고정과 preflight 완료

### P1 - 데이터 취득(완료)

- `master`를 40자 commit으로 resolve
- commit-pinned raw URL에서 allgaps.sql과 schema.sql 다운로드
- 두 raw source와 같은 commit 디렉터리에 hash/retrieval metadata 기록

### P2 - 데이터 검증(완료)

- schema 열 순서 검증과 row 정규화
- record 및 endpoint 산술 검증
- `ismax`와 독립 high-watermark 재구성 대조
- external exhaustive coverage provenance와 record count 확인
- OEIS 84개 공개표현과 Oliveira 별도 계산자료 75개 중첩 record 교차검증

### P3 - 수학 계산(완료)

- `log1`-`log4`, `F`, end-bounded `G`, `H`, `Q`
- end-prime jump interval minimum과 record recovery factor
- global running minimum, interval-minimum trajectory와 descriptive log-log trend
- `(10^k,10^(k+1)]` exact log-bin minimum
- full trailing record-window `w=5,10,20` rolling local envelope와 100-dps 전수검증

### P4 - 산출물(완료; 사용자 시각 QA 완료)

- 큰 정수를 10진 문자열로 보존한 핵심 통계 CSV
- end-bounded trajectory, interval minimum, running minimum, jump recovery 그래프
- Sono 및 `H=1` 참고선
- Cramér/Wolf 계열 \(\log^2x\) trend와 보조 비교
- 8종 PNG/PDF 16개 생성 및 파일 존재 자동검증; 사용자 시각 판정 완료

### P5 - 해석과 중복성 검토(완료)

- observed, heuristic, conditional, proved를 분리
- 9편 corpus 안의 중복 여부와 추가 문헌검색 결과를 분리
- 새 패턴은 재현 결과와 독립 가설로 구분
- P003 상세 결과와 문헌 비교·후속 가설 보고서 분리 작성

## 9. 예상 산출물 위치

```text
source/                 # 정의, source parser, provenance, validation, analysis, plotting, CLI
tests/                  # 데이터 비의존 및 toy-record preflight 단위시험
test_plan/P003_*.md     # 전체 실행 전 목적, source, gate, 성공/중단 기준
datas/raw/prime-gap-list-project/<commit>/ # 승인 후 immutable raw + schema + metadata
datas/validated/prime-gap-list-project/<commit>/
test_result/run_<run-id>/
  tables/
  figures/
  summary.json
  verification_report.json
  cross_validation/
  tables/log10_bin_minima.csv
  tables/rolling_local_envelope_w5.csv
  tables/rolling_local_envelope_w10.csv
  tables/rolling_local_envelope_w20.csv
docs/review/            # 이번 연구의 문헌 리뷰 정본
docs/method/             # 세부 방법 문서
```

문헌 리뷰는 `docs/review/`에만 작성하며 유사 철자의 별도 경로를 만들지 않는다.

## 10. 필수 단위시험과 불변식

실제 데이터 계산 전에 최소한 다음을 통과해야 한다.

1. `log_2`, `log_3`, `log_4`가 직접 중첩한 자연로그와 일치
2. iterated natural logarithm이 base-\(2\), base-\(3\), base-\(4\) 로그와 다름
3. `source/`의 금지된 base-\(k\) 구현 0건
4. 반복로그 domain 및 `X_SCALE_POSITIVE_MIN == 3_814_280`
5. 양의 분석 구간에서 \(F(x)>0\)
6. 대표 구간에서 \(F(x)\) 단조증가
7. end-prime 점프 위치 toy record 정답
8. interval minimum이 brute-force 정수 열거와 일치하는 소형 사례
9. running minimum 단조 비증가
10. 마지막 record가 verified limit에서 정확히 잘림
11. 임의정밀도와 float64 교차검증 허용오차
12. 정규화 row마다 원본 line 기반 source_row_id가 보존됨
13. 모든 결과 schema와 그래프에 `boundary_mode=end`가 표시됨
14. 승인 marker 없이는 fetch/validate/analyze가 network·파일 write 전에 중단됨
15. 프로젝트 텍스트와 파일명에 잘못된 4글자 약어가 0건임
16. 실제 gap 154가 `[4,652,507,17,051,886]`을 사용하고 minimum이 `154/F(17,051,886)`임
17. 모든 저장 `F/H`와 envelope 값을 별도 100-dps 직접 중첩 자연로그 식으로 상대오차 `1e-38` 이내 대조
18. log-bin이 `(10^k,10^(k+1)]`, rolling이 full-window `w=5,10,20` 계약을 지킴

## 11. 해석 금지사항

- Sono 상수를 실제 극한 또는 예상 계수로 부르지 않는다.
- `H=1`을 증명된 Wolf bound로 부르지 않는다.
- 유한 계산을 무한 범위의 증명으로 표현하지 않는다.
- unknown \(X_0\) 아래 관측을 정리 위반으로 표현하지 않는다.
- source의 start-prime ordering을 canonical end-bounded \(G(x)\)와 혼동하지 않는다.
- `x=16`부터 계산 가능하다는 사실을 양의 lower-bound 비교 가능성과 혼동하지 않는다.
- global running minimum이 증가하거나 상하 요동한다고 해석하지 않는다.
- 최신 record와 exhaustive verified coverage를 같은 뜻으로 쓰지 않는다.
- 9편에서 동일한 검증 pipeline이 없다는 사실을 전 세계 문헌 novelty 확정으로 확대하지 않는다.
- Feliksiak preprint의 fitted \(LB/F\) 비교를 무시하고 “FGKMT scale과 record의 최초 비교”라고 주장하지 않는다.

## 12. 실행 승인 체크포인트

실험 허가 요청 시 사용자는 다음 인식이 일치하는지 확인한다.

1. canonical \(G(x)\)는 사용자가 지정한 `end_prime <= x` 정의 하나다.
2. theorem-scale envelope는 `3_814_280`부터이며, `16`부터의 앞 구간은 domain 진단뿐이다.
3. GitHub `allgaps.sql`을 commit으로 고정하고, 실제 \(G(x)\) 주장은 문서화된 exhaustive limit 안에서만 한다.
4. Sono 비교는 같은 \(F(x)\) scale의 \(k=1\) explicit 기준선이지만, FGKMT 5인 논문의 상수를 그대로 추출한 것으로 표현하지 않는다.
5. 유한 관측은 empirical result이며 asymptotic theorem의 검증이 아니다.

사용자는 2026-08-23에 위 경계와 P003 범위를 승인했다. 실제 실행 직전에는 승인 사실과 별개로 `exp-preflight`의 환경·수학·provenance·비덮어쓰기 gate를 모두 통과해야 한다.

## 13. P003 실제 실행 기록

authoritative run:

```text
run_id = 20260822T195906Z_full1e20
analysis_limit = 100000000000000000000
python = W:\miniforge3\envs\FGKMT\python.exe
working_dps = 50
verification_dps = 100
stored_relative_tolerance = 1e-38
exit_code = 0
elapsed_seconds = 7.654
```

검증 결과:

- canonical pin: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- 64 end-bounded intervals, 63 jumps, 14 log bins
- rolling rows `w=5/10/20`: 60/55/45
- 독립 100-dps 수치 필드 1,160개 PASS, issue 0
- gap 154 interval `[4,652,507,17,051,886]` 회귀시험 PASS
- OEIS record 84/84 PASS; 독립 공개 표현으로 분류
- Oliveira e Silva 별도 계산 record 75/75 PASS; source limit `4e18`
- figure 16 files 존재, 누락 0; 사용자 시각 QA 완료

해석 정본은 `test_result/202608230503_P003_full_analysis.md`, 문헌 비교와 가설은 `docs/review/10_P003_문헌비교와_후속가설.md`다. machine summary의 `COMPUTED_NOT_INTERPRETED` 상태는 실행 시점의 사전 분리 원칙을 보존하기 위해 사후 변경하지 않는다.

## 14. P004–P008 실제 실행 기록

P004 authoritative run `20260823T075238Z_p004_sensitivity`는 전체 47 tests와 100-dps 독립 검증 3,747개를 issue 0으로 PASS했다. end/start global minimum은 같은 record 50, gap 540에서 각각 `37.81686039672168...`, `37.81686039812796...`였고 shifted log-bin 3종도 같은 global minimum을 보존했다. 상세 해석은 `test_result/202608231652_P004_sensitivity_analysis.md`다.

P004 실행기는 기존 `source.cli preflight` → 전체 unit tests → 분석 → 독립 verifier를 직렬로 실행하고 첫 실패에서 중단한다. 자동 스크립트가 정의·환경·hash·toy 회귀·수치를 1차로 검증하고, Codex는 source semantics·문헌 적용 범위·해석 라벨·graph visual QA처럼 자동화하기 어려운 부분만 2차 점검한다.

P005에서는 `sethtroisi/prime-gap`이 `m * P#/d` 주변 탐색 도구임을 확인했다. Rank 85→86 일반 x-범위 exhaustive 인증과 동일하지 않으므로 WSL-native CPU-only shell은 official correctness, 1/2/4/8-thread hash 일치와 작은 calibration만 수행했다. `20260824T054203Z` bounded calibration은 PASS했지만 full exhaustive 실행은 coverage certificate와 현실적 계산계획이 생길 때까지 금지한다.

P006에서는 canonical plateau `[e_k,e_(k+1))`와 recurrence exposure `{p_n:s_k<=p_n<s_(k+1)}`를 분리한다. Windows NumPy segmented sieve가 모든 consecutive gap을 직접 생성하고, 최초 발생 포함 rate `M/N`과 최초 이후 rate `C/(N-1)`를 계산한다. `[2,10^8]` pilot과 `[2,10^9]` full은 모두 PASS했고 full의 complete/censored plateau는 29/1이다. figure 3개는 2026-08-26 사용자 시각 QA도 PASS했다.

P007은 start-bounded `gap>=1856` count의 residue-state dual certificate를 floating LP로 발견하고 exact integer/Fraction arithmetic으로 모든 constraint를 재검증한다. modulus 30/210/2310 비교는 PASS했다. modulus-2310 저장 total upper bound는 `439161464927854179`이지만 위치 정보와 exhaustive search acceleration은 증명하지 않는다.

P008은 P007 certificate를 block-local하게 적용하고 exact prime-count 입력을 두 알고리즘으로 교차검증했다. actual four blocks는 saved verification PASS였으나 certified zero 0개다. nonempty block의 right-boundary crossing을 해결하지 않고 zero라고 판정하지 않는다.

## 15. P009/P010/P011 준비와 이론 문서 체계

P009 boundary witness는 `[a,b)`의 마지막 증명 소수 `p`, `p<n<b` 전체 합성수 coverage,
증명 소수 `q>=b`, `q-p<1856`을 검사한다. PARI/GP 2.15.4 설치와 small integer·중간
ECPP adapter의 fresh-process verification은 PASS했다. 실제 `[10^20,10^20+1000)` block은
P008 internal upper bound 0, last prime `10^20+993`, proven right prime `10^20+1071`,
거리 78을 결합해 exact certified zero PASS했다. 이는 한 block의 feasibility이며 전체
범위 가속이 아니다.

P010은 두 연구축으로 분리한다. P010A는 modulus-2310 replay와 modulus-30030
cutting-plane으로 count upper bound를 연구한다. P010B는 누락 없는 absolute candidate
mapping, boundary closure, total-cost break-even으로 실제 search acceleration을 연구한다.
count upper bound만 낮아져서는 P010B 가속이 증명되지 않는다. modulus-2310 replay는 두
exact builder와 chunk oracle, saved recheck가 PASS했지만 상한은
`439161464927854179`로 동일하다. 35,224,647 constraints의 modulus-30030 one-candidate
floating scan과 exact integer lift도 실제 PASS했고 핵심 scan은 각각 약 0.77초였다.
`M|M'`, `lambda>=0`에서 potential을 residue reduction으로 lift하면 기존 certificate가
target modulus에서도 성립한다. exact lift 자체는 같은 상한의 feasibility baseline이다.
P010A G4 actual은 seed 20,000에서 위반 제약 123개를 추가하고 4회 solve 뒤 full floating
scan 위반 0으로 수렴했다. 최종 certificate는 35,224,647 exact constraints 위반 0,
minimum slack 0이며 total upper bound를 `436001550591586306`으로 낮췄다. 이 약 0.7195%
count 개선은 absolute candidate mapping이나 search acceleration을 증명하지 않는다.

P010B direct candidate-cover verifier는 작은 half-open integer universe에서 각 start를 candidate,
exact composite factor rejection, strict window-prime rejection 중 하나로 누락 없이 분류한다.
`q=c+H`는 제거 witness가 아니며 equality `gap=H`는 candidate에 남긴다. `[1000,10000)`,
`H=20` toy에서는 candidate 69개가 exact 위험 start 69개와 일치했고 나머지 8,931개 witness
coverage도 PASS했다. 그러나 generator가 exhaustive truth를 사용하므로 acceleration은
BLOCKED다. 실제 승격에는 non-circular absolute generator, compressed coverage, PARI
certificate adapter, survivor search와 동일 baseline의 5회 이상 total-cost 비교가 필요하다.

P011은 P006 recurrence count를 leave-plateau-out binomial reference와 비교하는 경험적
진단이다. exact binomial, 고정 seed Monte Carlo, BH 보정을 사용하지만 record 선택편향,
비독립성, nonstationarity 때문에 theorem evidence로 해석하지 않는다. 실제 pilot은
terminal/saved PASS했지만 primary 관측 9 대 기대 109.079로 enrichment를 지지하지 않고
global stationary null의 부적합을 드러냈다. 두 figure는 사용자 시각 QA PASS다. P012는
log-bin별 gap 발생 수를 고정하고 forced first record를 제거한 stratified hypergeometric
null이다. 사용자는 `[2,10^9]` 개발/`[10^9,10^10]` holdout 분리, 0.5-decade primary와
두 shifted sensitivity, two-sided family max-abs-z primary, seed `20260827`, 100,000회를
사전 승인했다. 첫 P012-A actual은 조건부 분산 0인 7개 primary row의 올바른
`standardized_residual_z=None`을 plotting이 `float`로 강제해 실패했다. 이 값은 z=0이
아니므로 통계 계산은 바꾸지 않는다. r2 residual figure는 P011 bar를 유지하면서 해당 P012
bar를 생략하고 `variance=0; z undefined` x marker를 표시한다. r2 actual과 saved full
recomputation은 PASS했다. primary 관측 9 대 stratified 기대 8.5874, family p 0.21945이고
shifted family p도 0.71354·0.49280으로 P011 stationary 과대예측이 크게 줄었다. 모든 scheme의
enrichment BH q는 1.0이다. 거의 모든 row가 LOW_INFORMATION이므로 이는 recurrence 구조
부재나 null 정당성 증명이 아니다. 사용자는 r2 figure 시각 QA도 PASS했다. P012 계약은
`test_plan/P012_statistical_contract_v1.json`의 SHA-256
`1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`로 동결했다.

P012-B는 P006/P011 개발 table을 재사용하지 않고 `[10^9,10^10)`의 모든 consecutive gap
start를 range-only segmented sieve로 생성한다. canonical record metadata에서 record start와
다음 record start가 모두 holdout 안인 complete records `31–34`만 선택하고 왼쪽 continuation과
오른쪽 censored plateau를 제외한다. pinned gap-start 수는
`pi(10^10)-pi(10^9)=404204977`이며 오른쪽 boundary prime 하나로 마지막 gap을 닫는다.
사용자 실행 `20260827T121734Z_p012b_stratified_null_holdout`은 분석과 saved full recomputation,
사후 독립 산술과 100,000회 Monte Carlo replay를 issue 0으로 통과했다. 4개 complete plateau에서
recurrence는 1건이고 primary 기대 0.497022, family p 0.093939, 최소 enrichment BH q
0.275957로 5% 기준 enrichment를 검출하지 못했다. 12/12 row가 LOW_INFORMATION이고 3개는
zero variance이므로 null 채택이나 recurrence 구조 부재로 해석하지 않는다. 자동 figure QA와
2026-08-28 사용자 시각 QA가 모두 PASS했다. 정본 결과보고서는
`test_result/202608280019_P012B_holdout_result_analysis.md`다.

P013은 P012-B를 소급 수정하지 않고 `[10^10,10^11)`, `[10^11,10^12)` 두 새 gap-start
범위에 동일한 bin·cohort·forced-record·zero-variance·LOW_INFORMATION 규칙을 적용한다.
범위·exact prime-count difference·seed `20260828/20260829`·stage별 100,000회와 two-stage
Bonferroni alpha `0.025`는 contract SHA-256
`153cc1f3cd158a31e984f7d0f32502411102ab8ae6d5b9623cd0e81dcc5795bf`로 actual 전에 동결했다.
각 stage는 range를 한 번 분석하고 saved verifier가 전체 range를 다시 streaming한다. 이는
경험적 prospective 진단이며 결과를 본 뒤 pooling하지 않는다.

P014는 exact P010A G4 certificate를 `30030 | 510510` 배수-modulus 정리로 lift한다. R2 사용자
실행은 Windows PowerShell 5.1의 raw-JSON argv 손상으로 첫 preflight 전에 실패했고 과학 계산은
시작되지 않았다. transport만 Base64로 교정한 R3 actual은 92,160 states와 8,524,288,932
constraints를 full matrix 없이 8-worker exact signed-int64 streaming과 saved full serial oracle로
모두 검증했다. violation 0, minimum slack 0, artifact issue 0으로 실행은 `EXPERIMENT_PASS /
EXACT_FINITE`다. 그러나 첫 5,000-constraint LP가 unbounded라 새 candidate를 만들지 못했고 상한은
G4와 같은 `436001550591586306`으로 유지됐다. 따라서 과학적 판정은 `NO_IMPROVEMENT`이며 search
acceleration이 아니다. 후속 actual 전에 bounded seed sufficient condition과 toy 재현이 필요하다.
P015는 완료된 P013 child를 중복하므로 실행하지 않는다.

P017은 P013-A/B의 serial·parallel exact statistics/checkpoint/inference equality를 검증했고,
P017-B 동일범위 wall-time은 serial 12,598.410초 대 parallel 2,866.160초였다. 이는 계산 engineering
실측이며 모든 범위의 고정 speedup 보장이 아니다.

P018은 완료 P013-B의 낮은 정보량을 근거로 full-range gate를 균형형 B, margin-only prefix
보조 gate를 탐색형 A로 동결한다. WSL primecount Gourdon·Deleglise–Rivat는 P0/A 네 endpoint에서
일치했고 P0/A exact gap-start count를 고정했다. P018-P0 actual은 16/17 서로소 partition의 모든
정수 sufficient statistics와 saved blinded recomputation이 exact 일치해 `EXPERIMENT_PASS`다.
다만 forced record를 제거한 gap 582 conditioned count가 0이므로 expected·variance도 0이고 P0
판정은 `CALIBRATION_ONLY_NO_GATE`다. P0/A는 관측 recurrence·p/q/z를 읽거나 저장하지 않고
population·gap count·exposure margin만 사용한다. P018-A는 동결된 endpoint/gate로 실행 준비됐고,
2026-09-01 actual에서 64/65 dual partition과 saved blinded recomputation이 PASS했다. 그러나
gap-start 34,570,543,382개 안에서 primary gap 582·588은 forced record 제거 후 conditioned
count가 모두 0이었고 expected·variance도 0, LOW_INFORMATION은 100%였다. 따라서 A는
`EXPERIMENT_PASS / HOLD_PREFIX_INFORMATION / NO_AUTOMATIC_PROMOTION`이다. P018-B,
P019 actual, P013-C는 새 설계·가치 gate 없이 만들거나 실행하지 않는다.

P018의 기존 artifact명 `blinded`는 `exposure_equal_counts`와 plateau/control 배치를 gate에서
제외했다는 뜻으로 한정한다. bin 전체 `gap_counts`는 margin으로 저장되므로 conditioned count가
0이면 recurrence 0도 논리적으로 드러난다. 따라서 이후 방법론 명칭은
`margin-only / allocation-blinded`를 사용하고, P018-A 범위를 독립 holdout으로 재사용하지 않는다.
상세 사후감사는
`docs/review/21_20260902_P018_recurrence_설계사후감사_전체시각화_타당성검토.md`다.

P020은 P006·P011·P012-A/B·P013-A/B·P018-P0/A의 성공 정본 8개를 읽기 전용으로
종합했다. 새 prime sweep 없이 중복 제거 처리량 `72,178,455,399` gap-start를 회계하고,
coverage·P006 기술통계·null 교정·prospective 단계·정보량 붕괴·P018 forced-record funnel의
6개 표와 PNG/PDF figure를 생성했다. 정본 R2는 입력 manifest와 모든 등록 artifact hash,
원 saved-verifier 증거, 새 표·summary full recomputation, P018 margin-only contract와 figure
자동 QA를 모두 PASS했다. P011 stationary 기대 109.0790은 P012 층화 후 8.58738로
92.1274% 줄었고, 후기 범위에서 처리량 증가가 positive-variance row나 기대 recurrence 증가로
이어지지 않았다. 과학적 판정은 `SYNTHESIS_ONLY`이며, 자동 QA와 2026-09-02 사용자 figure QA가 모두 PASS했다.
정본 해석은 `test_result/202609021151_P020_recurrence_artifact_synthesis_result_analysis.md`다.

Sono/FMT numerical-threshold 1차 감사는 coefficient explicit화와 threshold explicit화를 분리한다.
Sono Theorem 3.6의 parameter를 대입한 계수는 약
`2.0038612046196704e-17`이지만, 출판본은 `sufficiently large X`의 숫자를 주지 않는다.
FMT는 exceptional zero를 제거해 proof를 effective하게 만들었으나 PAP/UB, Mertens/PNT,
smooth-number remainder, sieve weight, hypergraph probability와 x→X 변환에 수치 rate·유효범위가
남아 있다. 따라서 `X_emp(10^20)=3,814,280`은 finite exact이고 theorem-level `X_cert`와 실제
전역 최소 `X_star`는 계속 OPEN이다. 의존성 정본은
`docs/review/22_20260902_Sono_FMT_numerical_threshold_proof_dependency_audit.md`다. 모든 proof
node가 explicit해지기 전에 numerical threshold calculator를 만들지 않는다.

2026-09-02 T1 후속 원장은 Sono/FMT/FGKMT/Maynard의 직접 proof edge를 66개 obligation으로
등록했다. machine-readable 정본은
`docs/method/theory/data/Sono_FMT_T1_proof_obligations_v1.json`, 사람이 읽는 정본은
`docs/method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md`다. dependency id·DAG·source key·로컬
PDF hash 검증을 통과했지만 numerical PAP·UB, good sieve weight, finite covering probability와
arbitrary-X transfer가 열려 있어 `X_cert`는 계속 `OPEN`이다. 다음 proof gate는
`docs/review/23_20260902_Sono_FMT_T1_hard_node_feasibility.md`의 H1이며, 이 gate가 닫히기 전에는
threshold calculator 또는 실제 threshold 계산 runner를 작성하지 않는다.

2026-09-02 H1 source tracing은 FMT Theorem 6→FGKMT Theorem 5/6→Maynard Proposition 6.1과
FGKMT Lemma 7.2의 chain을 추적했다. 2026-09-04 H1a는 unrestricted product core와
simplex-supported 함수 사이의 concentration 이동을 exact하게 채워 모든 정수 \(r\ge36\)에서
\(J_r/I_r>\log r/(4r)\)를 증명했다. \(36\le r\le8103\)의 8,068개 정수는 60-dps directed interval,
\(r\ge8104\)는 해석적 꼬리로 닫았다. 그러나 finite
\(r_0\)의 나머지 조건, moment formula implied constants, Hypothesis 1 상수와 공통 시작 \(x\)는
인쇄돼 있지 않다.
판정은 `CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED`이며
\(X_{\rm cert}\)는 계속 `OPEN`이다. 정본은
`docs/review/24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md`와
`docs/method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json`,
`docs/method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md`다. 2026-09-04 H1b는 Hypothesis 1,
Proposition 6.1, Lemmas 8.1–8.6, Propositions 9.1–9.5와 common-cutoff를 17개 obligation으로
등록했다. 인쇄된 exponent와 parameter 범위는 확인했지만 multiplier·finite cutoff·공통 error
budget은 열려 있으므로 `SIV-07/09`와 `X_cert`는 변하지 않는다. 정본은
`docs/method/theory/14_Sono_FMT_H1b_Maynard_Proposition_6_1_constant_ledger.md`다. 다음 gate는
H1b-1과 H1c다. 2026-09-04 H1b-1 source 감사는 Lemmas 8.1–8.4를 13개 하위 node로 분해하고
Lemma 8.3의 정확한 GGPY Lemma 4 \(\kappa=1\) source를 확인했다. 이로써 source identity는
닫혔다. 후속 H1b-1a는 explicit \(C^\infty\) cutoff와 \(\|\psi'\|_\infty<50\),
Lemma 8.1(i)의 \(\mathfrak S_B(\mathcal L)>e^{-9k/2}\), 식 (8.5)의
\(E(k)<24\log k\)를 프로젝트 유한 보조정리로 닫았다. Lemma 8.1(ii)는 숫자
\(A_0,B_0\)와 공통 흡수 cutoff가 주어졌을 때 평가 가능한 parameterized majorant까지만
얻었으므로 `PARTIAL_EXPLICIT`이다. 2026-09-06 H1b-1b는 Lemma 8.2의 multiplier를
모든 정수 \(k\ge2\)에 대해 89로 닫았다. 또한 교정된 GGPY Lemma 3의 절대오차 multiplier를
\(C_{3,\mathrm{abs}}(A_1,A_2)\)라고 둘 때의 \(\kappa=1\) factor-2 전달을 보조 경로로
명시했다. Castillo et al.의 Lemma 2.5와 Remark는 GGPY/Maynard에 인쇄된 proof가
\(c_\gamma\)-relative 오류를 원 가정만으로 정당화하지 못함을 확인한다.
2026-09-07 H1b-1b-2a는 Maynard Section 8의
actual-call 분모를 네 exact family로 환원해 비제외 local factor가 1 이상임을 증명했다.
H1b-1b-2a.1은 이어서 10개 source call을 11개 analytic subapplication으로 분해하고,
canonical \(W_i\)와 \(dW_i,W'_i,a_mWBr,rW_m,W_0\)를 모두 포함해
\(\log Q_j\le\Lambda_*\)를 인증했다. 따라서 Rosser--Schoenfeld로 추적 호출 전체에서
\(c_{\gamma,j}>1/[3(1+\log\Lambda_*)]\)를 쓸 수 있음을 별도로 인증했다.
2026-09-08 H1b-1b-2b는 Ford Theorem 4.4의 누락항
\(c_\gamma(L+1)^\kappa\)를 보존한 교정 proof를 \(\kappa=1\)에 명시화했다.
이에 따라
\(C_{8.3}(a,A_2)=2\{40960D(a,A_2)e^{256+A_2}+2\}\)와 \(z\ge2\)가
 project-parameterized explicit가 되었다. 이어진 H1b-1b-2c는 실제 네 local family와
 Rosser--Schoenfeld의 양 끝 포함 구간 보정을 결합해 공통
 \(a=1/2,A_2=8,L=5+\log\Lambda_*\)를 인증했다. 따라서 `H1B-L83`은
 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다. 기존 절대 \(C_3\)+\(c_\gamma\) 하한 및
 Kuperberg size gate는 독립·sharpness 비교용 보조 경로로 보존한다. H1b-1b-2d는
 support-scaled \(N,W,N^2,W^2,NW\) norm과 exact finite-product 합성을 사용해 smooth
 Lemma 8.4 호출 7개를 project-parameterized explicit 하위 package로 닫았다.
 H1b-1b-2d.1a는 905행의 전역 \(H\) 함수·도함수를 만들지 않고
 \(|Z^2-A^2|\le2\varepsilon AB+\varepsilon^2B^2\)로 우회해 \(A^2,AB,B^2\)를
 일곱 비음수 smooth tensor class로 전개했다. 이어진 H1b-1b-2d.1a.1은
 최종 출판본 (9.42)--(9.48)의 \(s\)-Euler product, \(t\)-divisor 합,
 determinant, prefactor와 direct branch를 수치 재증명해
 \[
 C_Y=327680(14801/69)e^{264}+10,143,697<3.17\times10^{122}
 \]
 및 parameterized finite gate를 얻었다. H1b-1b-2d.1b는 실제
 \(\xi=\theta/10\), \(R\le x^{\theta/3}\)을 이용해
 \(\xi\log x\ge(3/10)\log R\)를 얻고 strict endpoint를 포함한
 \(C_\Sigma+2\) multiplier로 두 sharp factor도 finite하게 닫았다.
 따라서 Lemma 8.4 관련 actual 하위호출 9/9와 `H1B-L84`는
 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다. 전체 moment budget이 남아
 `SIV-07`은 계속 `HARD_BLOCKER`다.
정본은 `docs/method/theory/15_Sono_FMT_H1b1_basic_summation_constant_audit.md`와
`docs/method/theory/17_Sono_FMT_H1b1a_explicit_cutoff_summation_package.md`,
`docs/method/theory/18_Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_recovery.md`다.
추가 proof obligation과 세 repair 경로는
`docs/method/theory/19_Sono_FMT_H1b1b2_cgamma_error_normalization_ledger.md`에
fail-closed로 등록했고, actual local-factor와 application 제외모듈 하한 증명은
`docs/method/theory/20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md`와
`docs/method/theory/21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md`가 정본이다.
 교정된 one-step multiplier 정본은
 `docs/method/theory/22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md`다.
 actual 입력 특수화 정본은
 `docs/method/theory/23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md`다.
 actual one-step 입력, smooth \(r\)-회 하위 package, line-905 scalar/square package와
 sharp scale이 명시됐어도 전체 Proposition 6.1 numerical threshold package는 아직 아니다.
 H1b-1b-2d 정본은
 `docs/method/theory/24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md`,
 `docs/method/theory/25_Sono_FMT_H1b1b2d1a_H_remainder_bypass.md`와
 `docs/method/theory/26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md`,
 `docs/method/theory/27_Sono_FMT_H1b1b2d1b_sharp_xi_logx_scale.md`다.

H1b-2a는 실제 cutoff의 plateau cube를 직접 적분해 모든 정수 \(k\ge36\)에서
\(I_k(F)\ge(2k\log k)^{-k}\)와 이에 대응하는 절대 \(J_k(F)\) 하한을 닫고,
actual `L620_dW` 오차를 이용해 Lemma 8.5의 coefficient·local/global weight를
\(M_{620}\)과 \(\eta_{85}(k,R)\)의 유한식으로 바꿨다. 따라서 `H1B-L85`와
`H1B-L86-SIZE`는 각각 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`,
`PROJECT_FINITE_COMPONENT_CLOSED`다. 후속 H1b-2a.1은 Proposition 9.4 식 (9.61)의
exact denominator에서 식 (9.66)의 마지막 두 Euler local factor를 복원해, 앞쪽 식
(9.64)의 제곱 보정까지 포함한 normalization을
\(e^{2+6/k}\mathfrak S_{WB}(\mathcal L)^{-1}\) 이하로 닫았다. 후속 H1b-2a.2는 실제
\(\mathcal A=\mathbb Z,D=1,\xi=\theta/10\)에서 연속 정수 interval의 exact
\(E_q^{(1)}\le1\), multiplier 1의 \(\tau_{3(k+1)}\) tuple bound와 explicit 흡수비
\(\rho_{94}\)를 결합해 식 (9.52) distribution child를 닫았다. 후속 H1b-2a.3은
product-profile 절대오차에 붙는 \(2^k\) 손실을 강화 smooth cutoff로 흡수하고,
sharp·Euler·distribution 항을 원문 순서로 합성했다. 그 결과 actual FGKMT/FMT P94는
모든 정수 \(k\ge36\)에서 표준 우변의 13배 미만이며
`H1B-P94=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다. 일반 \(\mathcal A\) P94와
P91/P92/L93/P95의 공통 moment budget은 열려 있으므로 `SIV-07/09`, `X_cert`는
승격하지 않는다. 정본은
`docs/method/theory/28_Sono_FMT_H1b2a_residual_moment_error_package.md`와
`docs/method/theory/29_Sono_FMT_H1b2a1_Proposition94_exact_Euler_normalization.md`,
`docs/method/theory/30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md`,
`docs/method/theory/31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md`다.

같은 날 H1c는 FGKMT Hypothesis 1과 Sono PAP를 20개 node로 분리했다. \(\mathcal A=\mathbb Z\)인
Hypothesis 1(1)은 `floor(y^(1/3))*(log y)^(100 k^2) <= N`, (3)은 `N>=q`일 때 implied
constant 2라는 exact sufficient reduction이 있다. 그러나 condition (2)의 character/Bombieri–
Vinogradov·affine-form·prime-density package와 PAP의 principal/nonprincipal·`psi->pi` finite
rate는 열려 있다. PAP와 Hypothesis 1은 shared source를 가진 sibling obligation이지 서로를
함의하지 않으므로 T1의 잘못된 `SIV-08 -> PAP-11` 직접 의존선을 제거했다. Jutila source 연도는
1977로 정정했다. 정본은
`docs/method/theory/16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md`다. 이 graph·서지 교정은
`SIV-07/08/09`, `PAP-11` 또는 `X_cert`를 닫지 않는다. H1b-2a.3 뒤 다음 gate는
H1c-1 quantitative character package다. H1c-1은 actual 식 (9.52)가 아니라
Proposition 9.2와 전체 good-weight theorem 때문에 남는다.

2026-09-09 H1c-1a source inventory는 Maynard의 exact centered discrepancy와 FGKMT actual
parameter를 계약으로 고정하고 explicit 후보들을 적용 조건별로 대조했다. 선언한 source 안에서
drop-in 정리는 0개다. Bordignon 2021 Theorem 1.4가 임의 \(A>3\)와 explicit
non-exceptional-modulus average를 제공해 `PRIMARY_COMPOSITION_CANDIDATE`로 선정됐다. 그러나
fixed-\(k\) 또는 growing-\(A\) 선택, \(|a|q\) coverage, 한 공통 exceptional \(B\), 반열린
endpoint, \(\psi\to\pi\), exact total-count recentering, represented-prime density와 common
cutoff가 열려 있다. Sedunova 2019 Corollary 1.4는 Johnston 2026의 \(B-3\) 교정을 적용하지
않고 사용하지 않는다. 정본은
`docs/method/theory/32_Sono_FMT_H1c1a_quantitative_prime_distribution_source_inventory.md`와
`docs/review/38_20260909_H1c1a_quantitative_prime_distribution_타당성검토.md`다.

H1c-1b.1은 먼저 서로 다른 세 매개변수를 분리했다. outer chain parameter는
\(k_{\mathrm{chain}}=1\)로 고정되지만, FGKMT Section 8의 sieve dimension과 Maynard의 form
count는 둘 다 \(r\)이며 \(x\)와 함께 증가한다. 따라서 Hypothesis 1(2)의 saving exponent는
\(100\)이 아니라 \(100r^2\)이다. Bordignon 2021 Theorem 1.4는 모든 실수 \(A>3\)에 대한
명제이므로 같은 \(x\)에서 \(A(r)=100r^2+10\)을 점별로 대입할 수 있다. actual Proposition
9.2 호출은 \(\mathcal L'=\{n\}\)인 identity form이고, 그 modulus 조건
\[
\frac{\log T}{6}\ge A(r)\log\log T
\]
은 \(r\ge36\)에서 exact rational/calculus certificate로 닫힌다. 일반 affine family를 위한
\(\log T/6\ge(A(r)+5/3)\log\log T\)도 capacity envelope로만 닫혔으며 endpoint/count transfer는
아직 포함하지 않는다.

그러나 source가 택한 \(r_s=\lfloor(\log x)^{1/5}\rfloor\)를 actual scale \(T=x/2\)에 그대로
넣으면
\[
r_s^5\le\log x<r_s^5+\log2
\]
인 반복 transition strip에서 \(r_s>(\log T)^{1/5}\)가 되어 Maynard의 인쇄된 dimension
가정을 만족하지 않는다. 이는 큰 \(x\) 하나를 택해 없앨 수 없는 반복 경계다. exact repair는
\[
r_T=\lfloor(\log(x/2))^{1/5}\rfloor\in\{r_s-1,r_s\}
\]
이며 \(r_s-1\)은 항상 admissible하다. 하지만 이 한 단계 감소가 FMT/Sono의 최종
\(\log_4x/\log_3x\) 정규화와 명시 계수 \(2\times10^{-17}\)을 보존하는지는 후속
H1c-1b.1a에서 다시 검증한다. 정본은
`docs/method/theory/33_Sono_FMT_H1c1b1_parameter_modulus_envelope.md`와
`docs/review/39_20260909_H1c1b1_parameter_modulus_envelope_타당성검토.md`다.

H1c-1b.1a는 actual endpoint-safe
\[
r_T=\left\lfloor(\log(x/2))^{1/5}\right\rfloor\ge36
\]
을 쓰고, H1a의 \(J_r/I_r>\log r/(4r)\)와 FGKMT의 실제
\(R=(x/4)^{\theta/3}\)를 합성했다. dimension과 \(R\)의 finite normalization
factor는 \(39/40\)보다 크다. Sono가 150 대신 160을 택해 확보한 \(16/15\) slack 때문에
\[
\sigma y\le\frac{26}{25}\,80cx\log_2x
\]
이면 같은 \(c=\theta c_{I,J}/(12800\log5)\)로
\(C>(5/4)\log5\)를 얻는다. 따라서 dyadic repair는 asymptotic
\(2\times10^{-17}\) 계수를 낮추지 않는다. 후속 H1c-1b.1a.1은
Rosser--Schoenfeld Theorem 7로 위 upper gate를 (x\ge2\exp(36^5))에서 명시화했다. 정본은
`docs/method/theory/34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md`와
`docs/method/theory/35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md`다.

H1c-1b.2는 actual \(T=x/2\)와 \(2T=x\)에 같은 \(Q_1=(\log T)^A\)를 사용한다.
그러면 Bordignon의 exceptional modulus \(q_0\)도 하나로 고정된다. \(q_0\)가 있으면 그
prime divisor \(B\) 하나를 고르고, 없으면 \(B=1\)로 둔다. 이때
\((q,B)=1\Rightarrow q_0\nmid q\)이므로 실제 identity-form의 modulus family를 두
endpoint 모두에서 같은 non-exceptional subset으로 제어한다.

또 Bordignon 최종 NYJM판 Theorem 1.4의 양의 RHS 12항을 모두 등록했다. 누적 중심이
\(\psi(u)/\varphi(q)\)이므로 \((T,2T]\) von Mangoldt interval의 centered discrepancy는
\(D_{2T}-D_T\)이고, 그 합계 상계는 \(R_B(2T)+R_B(T)\)다. arXiv v1은 중심항과 일부 log
factor가 최종판과 달라 수치 정본으로 사용하지 않는다.

H1c-1b.3은 모든 \(u\in[T,2T]\)에서 같은 q-family와 \(B\)를 유지한 채

\[
\frac{R_B(2T)}{\log(2T)}+\frac{R_B(T)}{\log T}
+\int_T^{2T}\frac{R_B(u)}{u(\log u)^2}\,du
+2\sqrt{2T}(M_B+\Phi_B)+M_B
\]

로 Maynard 원문 Definition (2.1)의 exact half-open unweighted count discrepancy를
상계했다. 그러나 FGKMT는 Definition 2에서 actual set을
\(\mathcal A(T)=\{n:T\le n\le2T\}\)로 수정한다. H1c-1b.3r1은 source
\((T,2T]\) count에 lower atom \(1_{\mathbb P}(T)\)만 더하면 되고 centered correction은
modulus마다 1 이하임을 증명해 기존 endpoint envelope와 density를 보존했다.

H1c-1b.4a는 Bordignon의 \(C(A,A-3,X_0/Y_0)\) 표기와 최종 remainder 정규화를
fail-closed로 교정했다. 4b–4d는 represented-prime density, 12항·count 비용의 공통
log-saving 흡수와 corrected source constant \(C_A<1\)을
\(r\ge10^{10}\)에서 닫았다. 4e는 같은 \(T,r,A,Q_1,B\)를 한 quantifier chain으로
합성해

\[
X\ge2\exp(10^{50})
\]

에서 actual \(\mathcal A=\mathbb Z\), identity subset의 Hypothesis 1(1)--(3)을
constants \(1,1,2\)로 explicit하게 닫는다. 그 뒤 H1b-P92a는 actual identity의
weighted P9.2를 \(k\ge10^{200}\), \(X\ge2\exp(10^{1000})\)에서 상대/가법 multiplier
1/1로 닫고 closed-to-\((T,2T]\) lower weight/count atom도 별도로 흡수했다.
공통 moment 합성은 남으며 이 child cutoff는 전체 \(X_{\rm cert}\)가 아니다. 따라서 `SIV-07/08` 또는 `X_cert`를 승격하지 않는다. 정본은
`docs/method/theory/36_Sono_FMT_H1c1b2_common_exceptional_B_full_remainder.md`와
`docs/method/theory/37_Sono_FMT_H1c1b3_endpoint_count_transfer.md`,
`docs/method/theory/42_Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction.md`,
`docs/method/theory/43_Sono_FMT_H1c1b4e_actual_Hypothesis1_composition.md`와
`docs/method/theory/44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md`다.
고정 차원의 P94 sufficient gate와 maximal growing dimension의 호환성을 혼동하지 않는다.
H1b-P91a는 H1b-P92a의 uniform integral comparison과 exact integer discrepancy를 사용해
unweighted actual P91을 닫았다. T'=2floor(Y), N=T'+1과 2Y의 차이 <=1도 보존한다.
정본은 docs/method/theory/45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md다.
중요한 scope correction: 이 P91/P92 및 source P94 proof는 Maynard (7.5)의 명시적
W-coprimality indicator가 있는 construction을 사용한다. FGKMT (7.4) literal 표시와
자동으로 동일시하지 않는다. theory 45는 shift·prime-slice filter 보존을 증명했고,
helper는 unfiltered certificate 요청을 거부한다. actual empirical 결과는 바꾸지 않았다.
H1b-P94g는 같은 uniform comparison으로 growing-k 호환성을 닫았다.
정본은 docs/method/theory/46_Sono_FMT_H1bP94g_growing_dimension_rough_moment.md다.
실제 local scale T0=floor(Y)-floor(X)를 사용하고 원래 (X,Y]의 이동은 (T0,2T0]로 보존한다.
closed interval 확대와 원래 support 제거는 비음성 상계이지 등호가 아니다.
고정 C_h>=1, |h|<=C_h Y/X 및 log(C_h)<=log(X/2)/4 아래에서 multiplier 1과
각 p의 local-series off-tuple 상계를 얻었다. root threshold가 아닌 child 충분조건이다.
다음 H1b-NORM에서 공통 series/lambda/weight/tau/u를 맞추고, P95의 actual
필수성은 FGKMT Theorem 6의 직접 인용 경로부터 별도로 점검한다.
모든 root dependency가 닫히기
전에는 장시간 prime sweep이나 threshold calculator를 만들지 않는다.

`article/unverified/`의 2026 bounded-gap 원고 2편은 기존 9편 corpus와 분리한다. 두 원고가
주장하는 `H_1<=240`과 `H_1<=186`의 `H_1`은 bounded-gap liminf 기호이며 본 프로젝트의 H1
good-weight gate와 다르다. peer review·독립 검증 전에는 theorem input으로 사용하지 않고,
exact/interval certificate 및 proof-obligation 설계만 방법론 후보로 참고한다. 검토 정본은
`docs/review/25_20260904_Stadlmann_Bounded_Gaps_240_unverified.md`와
`docs/review/26_20260904_OpenAI_Improved_Short_Gaps_186_unverified.md`다.

coverage-preserving compression의 finite soundness 정본은
`docs/method/theory/10_coverage_preserving_compression_정식화.md`다.
modulus 배수 exact-lift 정본은
`docs/method/theory/11_residue_certificate_modulus_lift.md`다.

이론·가설·폐기된 연결의 정본 지도는 `docs/method/theory/00_이론_가설_방법론_색인.md`다. 신규 네 이론 초안의 오류와 채택 범위는 `docs/review/17_20260826_prime-gap_통합이론_비판적_타당성검토.md`에 기록한다.

완료된 특정 실험 runner는 `test_done/`에 SHA-256과 함께 보존하고 재실행하지 않는다. 재사용 공통 runner·logging·test는 각각 `scripts/runners/`, `scripts/common/`, `scripts/tests/`에 둔다.


## 2026-09-09 H1b-NORM 공통 filtered construction

[theory 47](method/theory/47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md)의
같은 W-filtered weight로 P91/P92/P94를 합성했다. 정확한 한 소수 series factor,
lambda 선형비와 weight 제곱비를 유지하고, Rosser--Schoenfeld Theorem 1에서
dyadic prime-count 상대오차 3/log X를 얻었다. B0 삭제는 별도 가중치 한 항 비용이다.

공통 tau=2M0(log X)^k, u_X=(phi(B)/B)(log R/log X)kJ/(2I)이며,
k>=10^200에서 P91/P92 상대오차 4/k와 2/sqrt(k), fixed-X 확률 상대오차
3/sqrt(k), point probability X^(-3/4)를 얻었다. u_X의 X/B 의존성을 지우지 않으며
literal only-k 선언이나 unfiltered 식을 인증한 것으로 표현하지 않는다.
같은 강한 child cutoff는 전체 X_cert가 아니다. 다음 H1b-DEP에서 actual proof graph와
general P6.1/P95를 분리한 뒤 FMT correlation/failure rate와 PAP/UB/arbitrary-X를 닫아야 한다.
기존 section별 OPEN·next gate는 당시 snapshot이며 이 절과 최신 handoff가 우선한다.



## 2026-09-09 H1b-DEP actual proof 경로

[theory 48](method/theory/48_Sono_FMT_H1bDEP_actual_dependency_map.md)는 P95의 직접·간접
불필요성을 확인하고 일반 P6.1의 미완료 의무와 actual W-filtered fixed-X 입력을 분리한다.
P94는 FMT sequel에 필요하다. C_h=4·admissible tuple·실제 point의 X^2 범위는 닫았지만
conditioned sparsity와 hypergraph 전체 결론은 닫지 않았다. 남은 6묶음/12작업은
독립 정리 개수나 완료율이 아니며, child sieve X>=2exp(10^1000)는 최종 gap 변수의
X_cert가 아니다. 다음은 H1b-COR1 / DEP-R01이다. 과거 날짜별 next-gate는 당시 기록이다.
PDF 판독은 [규약 09](../ai_dev_tool/09_PDF_원문_읽기_대조_규약.md)를 따른다.

## 2026-09-09 H1b-COR1 finite 확률 입력

[theory 49](method/theory/49_Sono_FMT_H1bCOR1_finite_correlation_conditioning.md)는
distinct-point correlation 상대오차 2/(ln X)^17, sigma>1/ln X,
조건부 residue 희소성 X^(-3/5), good-P failure 7/(ln X)^8을 actual construction에서 닫았다.
두 copy의 충돌과 조건부 분모, 평균!=1의 오차를 보존한다. small-codegree도 실제 입력으로
연결했지만 full hypergraph 전체는 OPEN이다. 기존 child cutoff를 늘리지 않았고 최종
X_cert로 해석하지 않는다. DEP의 12 OPEN은 당시 이력, successor의 현재 미완료는 9개다.
당시 다음은 H1b-COR2 / R05였다. 후속 결과는 아래 절을 따른다. 새 actual 계산은 하지 않는다.

## 2026-09-09 H1b-COR2 off-tuple finite 예산

[theory 50](method/theory/50_Sono_FMT_H1bCOR2_off_tuple_finite_budget.md)는
NORM47·COR1·SIGMA35의 같은 W-filtered law에서 R05를 닫았다.
a=ln X, b=ln a, c_aux=1/(153600 ln5)이며 c_aux는 최종 Sono 계수가 아니다.
총 off-tuple 기댓값은 800 c_aux X/(a b^9) 이하, b^-3 초과 q가
X/(2ab)개보다 많을 확률은 1600 c_aux/b^5 이하다. 조건부 law에서는 2/b^3 상계를 쓴다.
양·음·0 h와 q 자체의 생존, k+1 distinct 및 조건부 분모를 보존한다.
기존 child cutoff에서 한 사건의 실패율이 10^-18 미만이지만 전체 정리의 실패율은 아니다.
R01/R02/R04/R05 외 R03/R06/R07/R08/R09/R10/R11/R12의 8 work package와
broad SIV-07/08/09·X_cert는 열린 채다. 다음은 H1b-COR3의 R03→R06이며,
기존 COR1의 9 OPEN과 DEP의 12 OPEN은 당시의 변경하지 않은 이력이다.

## 2026-09-09 H1b-COR3 유한 local count·main degree

[theory 51](method/theory/51_Sono_FMT_H1bCOR3_finite_local_count_partition.md)은
사전 고정 J개 구간, delta>=a^(-1/4)에서 local count의 relative error 1/(100b²)와
failure 3Jb^6/a^17을 준다. disjoint grid와 covering 전 interpolation도 명시했다.
[theory 52](method/theory/52_Sono_FMT_H1bCOR3_main_degree_finite_moments.md)는
같은-p 모든 index pair의 충돌과 bad-P 질량을 상계하고, 조건부 denominator를 보존했다.
그 결과 살아남은 q 중 floor(X/(ab))개를 제외한 FMT (5.8)의 absolute error는
1/b² 이하, degree failure는 1600c_aux/b^5+800c_aux/b^10+112kb^4/a^11 이하이다.
같은 C>(5/4)ln5를 유지하며 a=ln X, b=ln a, c_aux=1/(153600ln5)다.

기존 X>=2exp(10^1000)는 **actual child sufficient cutoff**이지 최종 X_cert가 아니다.
R03의 보조 local 구간과 canonical maximal-gap end-bounded 구간도 혼동하지 않는다.
sigma의 O(b^-10)를 복원했다고 쓰지 않으며 이번에 충분한 O(b^-2)를 직접 썼다.
R01–R06 actual child는 explicit, R07–R12는 OPEN이다. 후속 COV1에서 cardinality·subset·
failure 전체를 확인해야 하며 SIV-07/08/09와 calculator는 여전히 fail-closed다.

## 2026-09-09 H1b-COV1 full-residue hypergraph 연결 (당시 이력; 아래 COV1a가 후속)

[theory 53](method/theory/53_Sono_FMT_H1bCOV1_full_residue_hypergraph_interface.md)은
전체 residue edge를 2k로 cap하고 제거 degree mass의 기대를 3200cX/(ab^9)로 상계한다.
예외 총 2X/(ab)를 별도 관리하여 남은 모든 q의 degree error 1/b²와 같은 C를 보존한다.
서로소 nonempty partition, D=2, r_hg=2k, A_hg=4km+2, kappa=(9/10)5^-m을 얻었다.
Theorem3의 core C0가 미수치화이므로 1·2점 moment transfer는 조건부이며
R07 전체와 X_cert는 OPEN이다. 다음 H1b-COV1a에서 source §5 상수를 복원한다.

실제 residue realization은 retained vertices 위에서 equality를 증명한다.
tuple만 덮은 것을 full residue survivor의 하한으로 대체하지 않는다.
복원한 예외 q의 비용과 고정 finite family의 union bound를 유지하고,
현재 child에서 그 비용이 최종 목적에 충분히 작다는 판정은 R08로 남긴다.
theory52 (52.17)의 마지막 '+' 누락은 theory53 §1.1이 정정 정본이며,
기존 JSON/helper의 세 항의 합과 일치한다. pinned 원본을 소급 수정하지 않는다.

## 2026-09-09 H1b-COV1a numerical C0=100

[theory54](method/theory/54_Sono_FMT_H1bCOV1a_explicit_covering_constant.md)의
project quantitative proof는 FGKMT Theorem3를 같은 가정·결론으로 복원한다.
정규화 good-event 허용오차를 t^30으로 바꾸고 모든 숨은 상수를 상계하여
충분한 C0=100을 얻었다. 원문에 인쇄된 값이나 최적 상수라는 뜻이 아니다.
이는 theory53의 C0-조건부 입력을 해소한다. COV-06은 EXPLICIT이고,
T1 현재 합계는 EXPLICIT8/PARTIAL9/RATE_MISSING30/SOURCE_REVIEW_REQUIRED4/HARD_BLOCKER15다.
theory53의 예외복원비와 유한 family 실패율을 실제 Sono 구간에 합성하는 R08,
PAP/UB·계수·최종변수 R09–R12는 남아 있다. 실제 prime 실험·calculator는 만들지 않는다.

## 2026-09-10 H1b-COV2 post-covering 유한 합성

[theory55](method/theory/55_Sono_FMT_H1bCOV2_post_covering_interval_smooth_composition.md)는
\(J=\lceil2/\varepsilon\rceil\) equal grid로 임의 half-open interval의 endpoint와 정수 floor를
정확히 처리한다. \(m=\lfloor\log_5(80cb/A)\rfloor\)에는 \(80cb/A\ge5\)라는 finite gate를
사용해 숫자 없는 Vinogradov lower constant를 추측하지 않는다.

theory53의 총 예외를 실제 cell 폭 \(h=1/J\)의 주항으로 나누어
\[
 e_{\rm cell}\le\frac2{(1-r_0)Ahb}<\frac7{A\varepsilon b}
\]
를 얻는다. outer residue 사건을 먼저 고르고, 그 고정값에서 \(J+1\) subsets의 inner
covering 사건을 고르는 순차 존재증명이므로 독립성이나 두 실패율의 합이 1 미만임을 요구하지
않는다. 결과를 본 뒤 subset을 고르는 postselection은 여전히 금지한다.

FMT §4의 smooth remainder는 actual parameter에 한정한 Rankin–Rosser–Schoenfeld proof로
\(b\ge e^{200}\) 및 표시된 finite gates 아래
\[
 \#R<\frac{\log b}{17b}\frac X{\log X}
\]
로 명시화했다. 최종 \(A,\varepsilon,\eta\)는 R11에서 PAP/UB 오차와 함께 정해야 하므로
numerical covering cutoff나 \(X_{\rm cert}\)를 아직 계산하지 않는다. R01–R08 actual child가
parameterized explicit이고 다음은 R09 numerical PAP다.

2026-09-11 Lean 보강에서 (55.26)의 kernel 적분 항등식, (55.28)의 두
finite-interval 비교와 Ein `103/100` 상계는 `KERNEL_PASS`로 올랐다.
(55.27)은 prime-sum 정규화·endpoint·decimal slack·종단 합성까지 검증한
`PARTIAL_FORMALIZATION`이다. 고정 Mathlib의 Chebyshev/Abel 기반은 있지만
Rosser--Schoenfeld `theta < 1.01624 t`와 해당 Stieltjes 비교의 독립 형식증명은
남았다. 이 증거 경계는 R08 판정을 바꾸지 않고 R09--R12·\(X_{\rm cert}\)를
계속 OPEN으로 유지한다.

## 2026-09-11 Lean 미형식화 의존성 gate·DEP-R09 phase 1

Lean 전수 inventory의 초기 1,005식 중 960식이 `NOT_YET_FORMALIZED`였다는 사실은
형식검증 coverage가 낮다는 경고이지만, 960식 전부를 source audit보다 먼저 형식화하는
gate로 사용하지 않는다. 경험적·역사적·대체 식도 섞여 있기 때문이다. 대신 다음 규칙을
적용한다.

1. source tracing과 exact obligation 정규화는 먼저 진행할 수 있다.
2. 최종 \(X_{\rm cert}\) 경로에 실제로 쓰일 식은 statement·source를 고정한 뒤,
   상위 결론에 사용하기 전에 dependency 순서로 형식화한다.
3. 외부 analytic source theorem을 premise로 받은 대수 합성은
   `CONDITIONAL_KERNEL_PASS`이며 source theorem의 독립 검증이 아니다.
4. R09--R12와 end-to-end critical path가 닫히기 전에는 threshold calculator나
   \(X_{\rm cert}\) 증명 완료를 선언하지 않는다.

[theory 56](method/theory/56_Sono_FMT_DEPR09_numerical_PAP_source_constant_audit.md)은
Sono의 \(c_{\rm ZFR}=1/24\), \(a=1/80\), \(c_{\rm ZD}=16\),
\(D_{\rm PAP}=160\), \(C_{\rm PAP}=1-e^{-2}\)를 source와 대조하고 exact 대수를
Lean으로 검증했다. 하지만 Gallagher·Jutila·Maier 계열의 implied multiplier와 공통
finite cutoff는 OPEN이다. 유한 one-sided PAP는 양의 \(\eta_{\rm PAP}\)를 두어
\(C_{\rm PAP}-\eta_{\rm PAP}\) 형태로 R11 예산에 연결한다. Theory 56 추가 후 inventory는
1,015식이고, 새 10식을 모두 분류해 미형식화 수는 여전히 960식이다.

## 2026-09-11 DEP-R09 Gallagher·Maier·McCurley full-source 보정

[theory 57](method/theory/57_Sono_FMT_DEPR09_Gallagher_Maier_McCurley_source_recovery.md)과
[review 64](review/64_20260911_DEPR09_Gallagher_Maier_McCurley_원문감사.md)는 사용자가
추가한 세 원문을 native text로 읽고 관련 PDF 페이지를 시각 대조했다. OCR은 사용하지 않았다.

Sono Proposition 5.3은 하나의 possible real exception을 제외하고
`1-sigma >= c_ZFR/log(Q(1+|t|))`를 준다. modulus와 높이를 모두 T 이하로 놓으면
`log(T(1+T))<=3log T`이므로 Proposition만 경유한 Gallagher constant는 보수적으로
`c1=c_ZFR/3=1/72`다. 출판본 p.536의 `c1=3c_ZFR=1/8`은 이 방향으로부터 나오지 않는다.
McCurley Theorems 1–2를 직접 쓰면 T>=13에서 `c1=1/24`인 더 나은 보수적 family region을
복원할 수 있지만 `1/8`은 복원하지 못한다.

Gallagher Theorem 7의 실제 lower range는 `exp(sqrt(log x))<=Q`다. `Q=x^(1/D)`와
`c_ZD=16`을 넣으면 `D>=160` 외에도 `log x>=D^2`가 필요해 D=160에서
`x>=exp(25600)`이 하나의 source-range gate가 된다. 이것은 PAP 공통 cutoff나 X_cert가 아니다.

더 중요하게 Gallagher의 결론은 hidden `K_G`와 cutoff를 가진 `≪`이고 Maier Lemma 2도
이를 숫자로 만들지 않는다. 따라서 finite nonprincipal error는 우선
`abs(E)<=K_G exp(-aD)M`으로 보존한다. 같은 exponent에서 multiplier를 지우는 것은
`K_G<=1`일 때뿐이며, 그렇지 않으면 `log K_G <= (a0-a)D` 같은 명시 budget으로 exponent나
D를 소비해야 한다.

direct McCurley 보수값은 `a0=1/240`, D=160에서 `a0D=2/3`이다. hidden multiplier와 finite
slack을 낙관적으로 1/0으로 놓아도 기존 최종식의 진단값은 약 `6.3458e-18`로
`2e-17`의 31.7%다. D=M=480으로 exponent product 2를 회복하면 M 비용 때문에 약
`2.4258e-18`이다. 이 값들은 대체 theorem이 아니라 민감도 진단이다.

따라서 phase-1의 `1/80*160=2`는 **인쇄 숫자의 exact 대수**로만 보존한다. 현재 source chain은
`C_PAP=1-exp(-2), D_PAP=160`과 final `2e-17`을 독립 인증하지 못한다. DEP-R09, PAP-11,
SIV-07/08/09, R09–R12, X_cert는 OPEN이다. 다음은 correction·강한 대체 explicit PNT-in-AP
source 조사 또는 Gallagher–Maier multiplier·cutoff의 정량 재증명이다. 이 repair 전에
threshold calculator나 R11 coefficient budget으로 넘어가지 않는다.

## 2026-09-13 DEP-R09 explicit PNT-in-AP 대체자료·coefficient capacity 감사

[theory 58](method/theory/58_Sono_FMT_DEPR09_explicit_PNT_AP_replacement_source_audit.md)과
[review 65](review/65_20260913_DEPR09_explicit_PNT_AP_대체자료_타당성검토.md)는 최신
Sono arXiv v4·journal판과 현대 explicit PNT-in-AP 후보를 감사했다. 공개 arXiv record와
journal article page에서 별도 correction/erratum은 식별하지 못했고, 저자 연락은 하지 않았다.

Bennett et al.의 large-modulus cutoff는 `q=u^(1/160)` 경계를 asymptotically 덮지 못한다.
Bordignon은 polylog modulus, Yamada는 average-over-moduli, Kadiri는 `q<=400000`이므로
actual pointwise PAP의 drop-in theorem이 아니다. Thorner--Zaman의 uniform PNT-in-AP는
구조적으로 가장 가까우나 decay constant와 implied multiplier가 numerical하지 않다.
fully explicit density의 127/198 exponent와 Benli et al.의 explicit Deuring--Heilbronn은
유용한 component지만 새 density-to-prime-sum transfer, exceptional `B0`,
principal term, `psi->pi`, 하나의 common cutoff가 필요하다. density exponent를 PAP의
`D`와 자동으로 동일시하지 않는다.

고정 Sono downstream 식을 80 dps로 독립 재계산하면 `D=160`, `M=160`에서 fixed
`2e-17`에 필요한 최소 `C_PAP`은 `0.8638312615226712472...`다. 총 허용 상대오차는
`0.1361687384773287528...`이고, 인쇄된 `exp(-2)`를 제외한 추가 finite-error slack은
`0.0008334552407160609...`뿐이다. `C_PAP=1`, `M=D`인 낙관 상한에서도 최대 정수
`D`는 186이며 187에서 목표 아래로 내려간다. 이는 source theorem이나 실제 PAP가 아니라
현재 downstream coefficient의 필요조건 진단이다.

따라서 주 repair branch는 `D=160`을 유지하며 Gallagher--Jutila--Huxley 또는
Thorner--Zaman proof의 모든 multiplier·finite cutoff를 복원하는 것이다. fully explicit
coarse branch는 독립 cross-check와 작은 인증계수 후보로 보존하되, 사용자의 결정 없이
연구목표 계수를 낮추지 않는다. `PAP-11`, DEP-R09, fixed `2e-17`, `X_cert`는 계속 OPEN이고,
actual prime sweep과 threshold calculator는 금지한다.

새 theory의 16식은 Lean 전수 inventory에 추가했지만 analytic source를 local axiom으로
만들지 않았다. 분류는 `SOURCE_THEOREM_UNFORMALIZED` 7식, `DEFINITION_ONLY` 1식,
`NOT_YET_FORMALIZED` 8식이다. 전체는 theory 문서 59개, display 1,046식이고
`NOT_YET_FORMALIZED`는 968식이다. coefficient 진단은 fixed FGKMT Python의 독립
high-precision unittest를 통과했으며 Lean theorem으로 승격하지 않는다.

## 2026-09-13 DEP-R09 Branch S fixed-D 정량 transfer 감사

[theory 59](method/theory/59_Sono_FMT_DEPR09_branch_S_quantitative_transfer_audit.md)와
[review 66](review/66_20260913_DEPR09_branch_S_정량_transfer_타당성검토.md)은
Thorner--Zaman의 uniform PNT-in-AP proof를 Theorem 2.1의 Huxley--Jutila density부터
Theorem 2.3의 explicit formula·prime-power 제거·local zero count·dyadic partial summation과
Theorem 1.1의 zero-free decay까지 분해했다. 각 단계에는 numerical하지 않은 multiplier 또는
finite cutoff가 남는다. Jutila 1977 공식 PDF는 native text layer가 사실상 비어 있어 그 경우에만
OCR을 사용했고, 사용한 theorem·상수·부등호는 렌더링 페이지와 대조했다.

actual boundary `q=x^(1/D)`에서는 `log(x)/log(q)=D`이므로 transfer leading error
`K exp(-c log(x)/log(q))`는 fixed D에서 `K exp(-Dc)`다. 따라서 x 증가만으로 숨은 K와 c를
없애지 않는다. D=160, 총 error budget eta에 대해
`c >= (log K-log eta)/160`이면 `K exp(-160c)<=eta`라는 초등 충분조건은
Lean `pap_fixed_d_transfer_gate`로 proof escape 없이 검증했다. K=1, 10, 320, 1000,
1,000,000의 80-dps gate와 D=160/170/180/186/187 capacity 표는 fixed FGKMT Python
unittest로 독립 재계산한다.

이 Lean 결과는 analytic source가 actual K, c, common cutoff를 준다는 증명이 아니다.
후속 조사에서 Huxley 공식 source leaf는 확보했지만, 원문 자체의 implied constant와 finite
cutoff가 numerical하지 않아 수치 주장에는 아직 사용하지 않는다.
`RS02-A/B`, `RS03`, `RS07`은 HARD_BLOCKER이고 `PAP-11`, DEP-R09, fixed `2e-17`,
`X_cert`는 OPEN이다. Theory 59의 10식을 추가한 inventory는 theory 문서 60개,
display 1,056식, `NOT_YET_FORMALIZED` 970식이며 금지 proof escape는 0건이다.

## 2026-09-13 DEP-R09 Jutila Lemma 4--8 정량 source inventory

[theory 60](method/theory/60_Sono_FMT_DEPR09_Jutila_Lemma4_8_source_inventory.md)과
[review 67](review/67_20260913_DEPR09_Jutila_Lemma4_8_정량복원_타당성검토.md)은 Jutila
Lemmas 4--8의 actual proof call을 분해했다. 공식 Huxley III 원문을 hash 고정했고,
Ramaré--Zuniga Alterman Corollary 1.3을 actual \(\tau=8/5\)에 대입해 Jutila 식 (3.6)의
one-sided weighted square-sum upper call을 exact coefficient
`18884947/500000 = 37.769894`로 명시화했다.

이는 Graham/Jutila Lemma 4의 전체 점근식 복원이 아니다. finite
`x_D=D^(11/2) log(D)^2`에는 `exp(4 lambda loglog(D)/log(D))` 보정이 남으므로 Jutila의
인쇄된 `10 exp(11 lambda)`를 그대로 인증하지 않는다. `JL5` harmonic lower bound,
`JL6` Mellin·tail, `JL8` local zero-count는 HARD_BLOCKER다. 따라서 `PAP-11`, DEP-R09,
fixed `2e-17`, `X_cert`와 threshold calculator는 계속 OPEN/NOT READY다. Theory 60의
12식을 추가한 inventory는 theory 문서 61개, display 1,068식이며 상태는
`KERNEL_PASS` 2식, `PARTIAL_FORMALIZATION` 1식, `SOURCE_THEOREM_UNFORMALIZED` 7식,
`DEFINITION_ONLY` 1식, `NOT_YET_FORMALIZED` 1식이다. 전체
`NOT_YET_FORMALIZED`는 971식이고 금지 proof escape는 0건이다.
