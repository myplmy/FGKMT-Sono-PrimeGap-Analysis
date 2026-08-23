# P006 — Maximal-gap Plateau·Recurrence 통계의 비판적 타당성 검토

## 결론

“한 maximal-gap record가 유지되는 동안 같은 크기의 gap이 몇 번 다시 나타나는가”는 계산 가능하고 탐색적 가치가 있는 질문이다. 다만 현재 보유한 `allgaps.sql`은 알려진 first-occurrence/large-gap 목록이지 모든 consecutive prime pair의 stream이 아니다. 따라서 이 파일만으로 exact recurrence count를 계산할 수 없다.

실험은 다음 조건에서만 타당하다.

1. 분석 범위의 모든 consecutive prime gap을 빠짐없이 생성하거나 검증된 raw stream을 확보한다.
2. canonical end-bounded plateau와 recurrence를 세는 start-prime exposure를 구별한다.
3. 최초 발생을 제외한 recurrence count의 분모를 같은 표본공간에 맞춘다.
4. 마지막 plateau의 right-censoring과 record selection bias를 명시한다.
5. raw count 외에 gap별 singular-series/위치 효과를 고려한 기대값 또는 대조군을 둔다.

이 조건을 적용한 작은 범위 pilot은 권장하지만, `10^20` 전체를 다시 소수 열거하는 본실험은 현재 데이터와 단일 PC 자원으로 준비되지 않았다.

## 검토용 문서에서 타당한 부분

- plateau longevity와 exact gap recurrence는 서로 다른 통계라는 구분
- maximal-gap record 목록만으로 recurrence를 복원할 수 없다는 지적
- 모든 consecutive prime pair 또는 동등한 exhaustive raw 결과가 필요하다는 데이터 게이트
- 마지막 미완료 plateau를 right-censored로 처리하는 규칙
- 작은 reference 범위에서 직접 열거 결과와 100% 일치시킨 뒤 확장하는 순서
- raw count, exposure-normalized rate, plateau length를 함께 보는 설계
- Pearson correlation 하나로 결론내리지 않고 selection effect와 비독립성을 경고하는 태도

## 반드시 수정할 부분

### 1. start/end 경계 혼합

본 프로젝트의 Sono-compatible canonical 함수는

\[
G_{\mathrm{end}}(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

이다. record `k`의 start/end를 `s_k,e_k`라 하면 canonical plateau는

\[
[e_k,e_{k+1})
\]

이다. 반면 gap occurrence를 세는 관측 단위는 gap start prime `p_n`이므로 start exposure set은

\[
A_k=\{p_n:s_k\le p_n<s_{k+1}\}
\]

이다. 두 구간은 목적이 다르며 하나를 다른 하나의 정의로 바꾸면 안 된다. 보고서에는 end-bounded plateau length와 start-event exposure length를 모두 저장하되 이름으로 구분한다.

### 2. recurrence rate의 분자·분모 불일치

검토용 문서는 최초 record occurrence를 제외한

\[
C_k=\#\{p_n:s_k<p_n<s_{k+1},\ g_n=G_k\}
\]

를 정의하면서 분모는 최초 occurrence를 포함하는

\[
N_k=\pi(s_{k+1})-\pi(s_k)
\]

로 두었다. 이는 서로 다른 표본공간이다.

정합적인 두 rate를 별도로 정의한다.

\[
M_k=\#\{p_n\in A_k:g_n=G_k\},\qquad Q_k=M_k/N_k
\]

\[
C_k=M_k-1,\qquad R_k=C_k/(N_k-1)\quad(N_k>1).
\]

`Q_k`는 최초 발생을 포함한 plateau multiplicity rate, `R_k`는 최초 발생 이후의 conditional recurrence rate이다. `C_k/N_k`를 주 rate로 사용하지 않는다.

### 3. raw rate만으로 확률 구조를 해석할 수 없음

고정된 even gap `d`의 빈도는 크기만이 아니라 작은 소수에 대한 residue 구조, 즉 Hardy–Littlewood singular series의 영향을 받는다. 위치 `x`가 커질수록 평균 간격도 변한다. 따라서 서로 다른 record gap들의 `R_k`를 그대로 비교해 “재출현 성향”이라고 해석하면 gap-specific arithmetic effect와 exposure effect가 섞인다.

최소한 다음을 함께 보고한다.

- exact `M,C,N,Q,R`
- plateau 중간 규모에서의 `log x`
- 동일 범위의 주변 even-gap 빈도 대조군
- Goldston–Ledoan 또는 Wolf 계열 heuristic expected count와 `observed/expected`
- 표본 수가 충분할 때 exposure offset을 둔 Poisson/negative-binomial exploratory model

expected model이 엄밀한 정리가 아니라 Hardy–Littlewood 계열 조건부/경험적 기준임을 표시한다.

### 4. 데이터 원천의 한계

현재 pin한 `allgaps.sql`에는 약 12만 개의 알려진 large/first-known gaps가 있지만 모든 consecutive gaps가 들어 있지 않다. 여기서 같은 gap-size row를 세는 것은 “목록에 제출된 known first occurrence/large gap”의 횟수일 뿐 실제 recurrence가 아니다.

정확한 P006 main 분석은 다음 중 하나가 필요하다.

- 독립 exhaustive 프로젝트가 보존한 모든 consecutive gap stream과 coverage certificate
- 분석 범위에서 segmented sieve로 모든 consecutive primes를 다시 생성한 stream

후자는 작은 pilot 범위에서만 현재 PC로 현실적이다.

## 연구 가치와 한계

가치가 있는 부분은 record의 수명, 동일 gap의 multiplicity, exposure-normalized recurrence를 한 데이터 모델에서 분리해 보는 것이다. 특히 `M_k=1`인 일회성 record와 여러 번 반복된 record를 구분하고, raw count 증가가 단지 더 많은 소수쌍 관측 때문인지 확인할 수 있다.

그러나 maximal records는 이미 극단값으로 선택된 작은 표본이고 plateau가 서로 독립이지 않다. 같은 gap의 빈도도 singular series에 의해 달라진다. 따라서 상관관계는 탐색적 결과이며 인과·새 법칙·점근 정리로 표현할 수 없다. “새로운 연구 질문” 가능성은 있으나 선행연구 전수조사 없이 독창성을 주장하지 않는다.

## 권장 pilot

1. `[2,10^8]`에서 모든 consecutive primes/gaps를 생성한다.
2. 독립 구현 또는 `primesieve`와 Python reference를 교차검증한다.
3. end-bounded record plateau와 start-event exposure를 동시에 복원한다.
4. `M,C,N,Q,R`, 두 종류 plateau length, censoring flag를 산출한다.
5. 작은 손계산 fixture와 전체 gap histogram으로 exact count를 재검산한다.
6. PASS 후 `[2,10^9]`, 필요 시 `[2,10^10]`으로만 단계 확장한다.

`10^20` main 분석은 raw exhaustive stream의 외부 확보 또는 분산 재계산 계획이 생길 때까지 보류한다.

## 선행연구와 연결

- G. H. Hardy, J. E. Littlewood, “Some Problems of Partitio Numerorum III,” DOI: https://doi.org/10.1007/BF02403921 — 고정 prime-pair/gap 빈도의 singular-series 기준.
- P. X. Gallagher, “On the distribution of primes in short intervals,” DOI: https://doi.org/10.1112/S0025579300016442 — Hardy–Littlewood 가정 아래 평균 간격 규모의 Poisson 관점.
- D. A. Goldston, A. H. Ledoan, “On the differences between consecutive prime numbers, I,” arXiv: https://arxiv.org/abs/1111.3380 — 지정된 거리의 consecutive prime pair 개수에 대한 조건부 점근식.
- M. Wolf, “Some heuristics on the gaps between consecutive primes,” arXiv: https://arxiv.org/abs/1102.0481 — exact gap 빈도와 first occurrence에 대한 경험적 공식.
- A. Kourbatov, M. Wolf, “Predicting maximal gaps in sets of primes,” arXiv: https://arxiv.org/abs/1901.03785 — maximal-gap trend와 extreme-value 해석.
- R. J. Lemke Oliver, K. Soundararajan, “Unexpected biases in the distribution of consecutive primes,” DOI: https://doi.org/10.1073/pnas.1605366113 — consecutive prime 관측의 단순 독립성 가정에 대한 경고.
- Prime Gap List Project: https://primegap-list-project.github.io/ — first occurrence, maximal, certification 분류 및 공개 데이터 범위.

