# P005b — Rank 85 이후 Exhaustive Prime-Gap 확장 가능성 실측 제안서 및 타당성 검토 요청서

## 1. 제안 목적

현재 확인된 maximal prime gap은 다음과 같다.

\[
g=1854
\]

시작 소수:

\[
X_0=101412319996363309069
\]

현재 공개된 다음 후보는:

\[
g=1858
\]

시작 소수:

\[
X_1=39422251630462640179641871
\]

이다.

본 제안의 목적은 처음부터 \(X_1\)까지 장기간 계산을 수행하는 것이 아니다.

먼저 \(X_0\) 직후의 **작은 calibration 구간을 CPU-only로 exhaustive하게 검사하여 실제 처리량을 측정**하고, 그 결과를 기반으로 다음 질문에 답하는 것이다.

> 현재 CPU 및 `prime-gap` 계열의 최적화만으로 Rank 85 이후의 다음 maximal gap을 exhaustive하게 검증하는 것이 실제로 어느 정도의 계산시간을 요구하는가?

특히 기존의 단순 외삽으로 제시된 "15년~40년" 등의 수치는 실행 목표로 사용하지 않고, 실제 benchmark에 의해 대체한다.

---

# 2. 현재 문제의 정확한 정의

다음 maximal gap의 시작점을

\[
x^*=
\min\left\{
p>X_0:
p_{\mathrm{next}}-p>1854
\right\}
\]

로 정의한다.

목표는 \(x^*\)를 찾는 것이다.

이를 위해서는 적어도:

\[
[X_0,x^*)
\]

구간에서

\[
p_{\mathrm{next}}-p>1854
\]

인 gap이 존재하지 않음을 exhaustive하게 검증해야 한다.

현재 알려진 1858 후보:

\[
X_1=39422251630462640179641871
\]

은 **known candidate**일 뿐이며, \(x^*=X_1\)이라는 것을 전제로 하지 않는다.

---

# 3. 중요한 원칙

## 3.1 1858 후보를 탐색 상한으로 간주하지 않는다

1858 candidate가 알려져 있다는 것은:

\[
g(X_1)=1858
\]

이라는 국소적 사실을 확인할 수 있다는 뜻이다.

그러나 다음을 별도로 증명해야 한다.

\[
\forall p,\quad X_0<p<X_1:
\qquad
g(p)\le1854
\]

따라서 X1 이전에 1856, 1858, 1860, ... gap이 하나라도 있는지 확인해야 한다.

---

## 3.2 Cramér 모델은 exhaustive coverage에 사용하지 않는다

Cramér 규모:

\[
g(x)\sim(\ln x)^2
\]

및 이에 기반한 gap-tail 모델은 다음 목적으로만 사용한다.

- 예상 workload 계산
- 탐색 순서 결정
- calibration 범위 선택
- 결과의 plausibility check

다음과 같이 사용해서는 안 된다.

> Cramér상 해당 구간에서 1856-gap이 발생할 확률이 낮으므로 해당 구간을 생략한다.

이는 exhaustive 검증이 아니다.

---

## 3.3 CPU-only

본 실험은 전 과정에서 CPU만 사용한다.

금지:

- CUDA
- GPU sieve
- GPU PRP
- OpenCL
- GPU offload
- CPU/GPU hybrid

---

# 4. 왜 calibration이 먼저 필요한가

이전 추정에서:

- brute-force 기반 계산
- `prime-gap` benchmark 외삽
- Cramér 기반 예상 위치

가 혼재되어 있었으며, 이를 그대로 전체 구간의 wall time으로 사용하는 것은 신뢰도가 낮다.

특히 다음 두 값이 실제로 측정되지 않았다.

\[
R_c=
\frac{\text{large-gap candidate coverage}}
{\text{second}}
\]

및

\[
R_s=
\frac{\text{search interval coverage}}
{\text{second}}
\]

따라서 현재로서는 "수년", "수십 년" 등의 숫자를 실행계획으로 사용할 근거가 부족하다.

본 실험에서는 작은 범위를 실제로 exhaustive하게 처리하여 이 값을 측정한다.

---

# 5. Calibration 대상 구간

다음 순서로 단계적으로 확대한다.

### Calibration A

\[
[10^{20},\,10^{20}+10^{16})
\]

### Calibration B

\[
[10^{20},\,10^{20}+10^{17})
\]

### Calibration C

\[
[10^{20},\,10^{20}+10^{18})
\]

### Calibration D

필요하면:

\[
[10^{20},\,10^{20}+10^{19})
\]

단, 각 단계는 이전 단계의 correctness와 throughput이 확인된 경우에만 확대한다.

---

# 6. Calibration의 목적

각 block에서 다음을 실제로 측정한다.

```text
range_start
range_end

wall_time
CPU_time
CPU_threads

coverage_units
candidate_count
surviving_large_gap_candidates
PRP_count
primality_proof_count

coverage_rate
candidate_rate
PRP_rate
```

특히:

\[
R_{\text{coverage}}
=
\frac{\text{covered range size}}
{\text{wall time}}
\]

과

\[
R_{\text{candidate}}
=
\frac{\text{large-gap candidates}}
{\text{wall time}}
\]

를 구한다.

---

# 7. 탐색 알고리즘 비교

최소 2개의 경로를 비교한다.

## Baseline

현재 검증된 `sethtroisi/prime-gap`의 CPU implementation을 가능한 한 그대로 사용한다.

대상:

- `combined_sieve`
- `gap_stats`
- `gap_test_simple`

단, `gap_stats`의 probability ranking만으로 검색을 제한해서는 안 된다.

---

## Experimental

현재 알고 있는:

\[
G(X_0)=1854
\]

를 이용하여 다음 조건에 특화한다.

\[
g>1854
\]

즉:

\[
p+1,\ldots,p+1855
\]

에 prime이 존재하지 않는 candidate를 우선적으로 찾도록 구성한다.

가능한 최적화:

- existing combined sieve 활용
- one-sided gap skipping
- primorial / \(D\) 최적화
- sieve depth 조정
- composite residue filtering
- candidate 후처리 최소화

단, 새로운 residue algorithm을 처음부터 재작성하는 것은 초기 calibration 단계에서는 하지 않는다.

먼저 기존 구현의 실제 성능을 측정한다.

---

# 8. Exhaustive correctness 검증

Calibration block에서는 반드시 reference 결과와 비교한다.

작은 범위에서는:

```text
Reference:
독립 segmented sieve 또는 검증된 prime-gap 구현

Experimental:
현재 사용하려는 CPU-only large-gap 탐색
```

결과가 정확히 일치해야 한다.

특히:

\[
\text{all gaps}>1854
\]

의 start와 length가 일치해야 한다.

---

# 9. False-negative 검증

새로운 candidate filter를 적용할 경우 다음 조건이 반드시 성립해야 한다.

\[
\boxed{
g(p)>1854
\Rightarrow
p\text{가 candidate set에서 제거되지 않는다}
}
\]

즉 false negative를 허용하지 않는다.

false positive는 허용할 수 있다.

---

# 10. Calibration에서 반드시 확인할 것

특히 다음을 기록한다.

### A. Sieve efficiency

\[
E_s=
1-\frac{N_{\mathrm{survivor}}}{N_{\mathrm{initial}}}
\]

### B. Candidate density

\[
D_c=
\frac{N_{\mathrm{candidate}}}
{X_{\mathrm{end}}-X_{\mathrm{start}}}
\]

### C. PRP reduction

\[
R_{PRP}
=
\frac{N_{\mathrm{baseline}}}
{N_{\mathrm{experimental}}}
\]

### D. Runtime speedup

\[
S=
\frac{T_{\mathrm{baseline}}}
{T_{\mathrm{experimental}}}
\]

---

# 11. Cramér 모델의 역할

각 calibration block에서 다음을 계산한다.

\[
L(x)=(\ln x)^2
\]

및 필요하면:

\[
P(g\ge1856\mid x)
\]

형태의 간단한 heuristic을 사용한다.

이 값을 실제 관측 candidate density와 비교한다.

목적은:

```text
Cramér가 실제 workload의 규모를 얼마나 잘 예측하는가?
```

이지:

```text
Cramér를 이용해 검색 범위를 생략할 수 있는가?
```

가 아니다.

---

# 12. 전체 범위 runtime 산정

Calibration을 통해 얻은 실제 throughput:

\[
R_{\mathrm{coverage}}
\]

를 이용하여 임의의 목표점 \(X\)까지의 단순 runtime을:

\[
T(X)
\approx
\frac{X-X_0}
{R_{\mathrm{coverage}}}
\]

로 1차 추정한다.

단, 범위가 커짐에 따라 throughput이 변하는지 확인하기 위해:

\[
R_{10^{16}},
R_{10^{17}},
R_{10^{18}},
R_{10^{19}}
\]

을 비교한다.

비선형성이 크면 단일 선형 외삽을 하지 않고 구간별 모델을 사용한다.

---

# 13. 실험 결과에 따른 의사결정 기준

### Case A

\[
T(10^{21})<1\text{ month}
\]

이면:

→ \(10^{21}\)까지 exhaustive 확장을 고려한다.

---

### Case B

\[
T(10^{21})<6\text{ months}
\]

이면:

→ 단계적으로 \(10^{22}\)까지 확대 가능성을 검토한다.

---

### Case C

\[
T(10^{21})>2\text{ years}
\]

이면:

→ 현재 알고리즘을 그대로 확대하지 않는다.

→ algorithmic optimization 또는 distributed CPU search가 필요하다.

---

### Case D

\[
T(10^{21})>10\text{ years}
\]

이면:

→ 단일 PC exhaustive expansion은 실질적으로 중단한다.

---

# 14. 왜 \(10^{21}\)을 첫 feasibility 기준으로 잡는가

현재 시작점:

\[
X_0\approx1.014\times10^{20}
\]

이다.

따라서 \(10^{21}\)까지는 약 한 자리 order만 확장한 것이다.

Cramér 규모도:

\[
(\ln10^{20})^2\approx2121
\]

에서

\[
(\ln10^{21})^2\approx2200
\]

정도로 증가한다.

따라서 1854 threshold가 여전히 의미 있는 large-gap filter로 작동하면서도, 실제 workload를 측정하기에 충분히 긴 범위다.

---

# 15. 1858 후보와의 관계

Calibration 및 초기 exhaustive search에서는 1858 후보를 특별히 우대하지 않는다.

다음과 같이 취급한다.

```text
1858 candidate
= independent known candidate
= verification target
≠ assumed next record
```

실험 중 더 작은 위치에서:

\[
g>1854
\]

가 발견되면 즉시:

\[
x^*
\]

후보가 된다.

그 뒤 해당 위치의 gap을 독립적으로 검증한다.

---

# 16. 실제 목표 구간에 대한 예상시간을 현재 시점에서 어떻게 표현할 것인가

현재 상태에서는 다음과 같이 보고하는 것이 적절하다.

### 전체 \(X_0\rightarrow X_1\)

\[
1.014\times10^{20}
\rightarrow
3.942\times10^{25}
\]

를 무조건 끝까지 돌리는 것을 목표로 하지 않는다.

이 범위는 현재 알려진 candidate 위치일 뿐이다.

### 우선 목표

\[
X_0\rightarrow10^{21}
\]

을 calibration/partial exhaustive expansion의 1차 목표로 한다.

### 이후

실측 throughput과 최초 large-gap 발생 위치에 따라:

\[
10^{21}\rightarrow10^{22}\rightarrow\cdots
\]

순차적으로 결정한다.

---

# 17. 중요한 결과 해석 원칙

다음 표현은 금지한다.

> Cramér에 따르면 다음 gap은 \(1.1\times10^{20}\)에 나온다.

대신:

> Cramér형 heuristic에서는 \(1.1\times10^{20}\) 부근이 다음 \(1856+\) gap의 전형적인 발생 규모로 예측되지만, 이는 exhaustive search 범위를 줄이는 증거가 아니다.

또한:

> 15년 또는 40년이 걸린다.

라고 calibration 전에 단정하지 않는다.

대신:

> 실제 CPU calibration 결과를 기반으로 예상 시간을 산정한다.

---

# 18. 연구의 핵심 산출물

본 실험이 성공하면 최소한 다음 값을 얻는다.

\[
R_{\mathrm{coverage}}
\]

\[
D_{\mathrm{candidate}}
\]

\[
R_{\mathrm{PRP}}
\]

\[
S_{\mathrm{baseline}}
\]

그리고 이를 통해:

\[
T(10^{21})
\]

\[
T(10^{22})
\]

\[
T(10^{23})
\]

\[
T(X_1)
\]

을 각각 추정한다.

---

# 19. Codex에 대한 검토 요청

다음 사항을 코드 및 실험 설계 관점에서 검토한다.

### 요청 1 — 기존 도구

`sethtroisi/prime-gap`의 고정 commit을 대상으로:

- build correctness
- official quick test
- CPU thread scaling
- memory usage
- `combined_sieve` throughput

을 확인한다.

### 요청 2 — Calibration

다음 범위를 순차적으로 benchmark한다.

```text
1e20 ~ 1e20+1e16
1e20 ~ 1e20+1e17
1e20 ~ 1e20+1e18
```

필요하면 \(10^{19}\) 폭까지 확장한다.

### 요청 3 — Threshold-specific mode

`gap > 1854` 탐색에 실제 도움이 되는 기존 기능을 조사한다.

특히:

- one-sided tests
- `--sieve-range`
- `--minc`
- \(P^\#/D\)
- `gap_stats`

를 실제 코드 수준에서 분석한다.

### 요청 4 — Coverage

`combined_sieve`의 후보가 일반 \(x\)-interval을 완전히 덮는지 확인한다.

덮지 못한다면:

> `prime-gap` = search tool

로만 분류하고 exhaustive engine으로 사용하지 않는다.

### 요청 5 — Runtime model

실제 calibration 데이터를 이용해:

\[
T(X)
\]

를 추정하는 모델을 작성한다.

선형 외삽과 비선형 외삽을 모두 비교하고 오차범위를 제시한다.

---

# 20. 최종 타당성 판단 기준

최종적으로 다음 중 하나로 결론을 내린다.

### Feasible

예상 시간이:

\[
<6\text{ months}
\]

이며 coverage correctness가 검증됨.

### Conditionally feasible

예상 시간이:

\[
6\text{ months}\sim2\text{ years}
\]

이며 지속적인 checkpoint/resume이 가능함.

### Not feasible for single workstation

예상 시간이:

\[
>2\text{ years}
\]

이고 알고리즘 개선으로도 의미 있는 단축 가능성이 낮음.

### Reject current method

coverage completeness 자체를 보장할 수 없거나 false negative 가능성이 존재함.

---

# 21. 최종 연구 질문

본 제안의 질문은 다음과 같이 정의한다.

> **현재 confirmed maximal gap \(1854\) 이후의 다음 maximal gap을 찾기 위해, \(101412319996363309069\) 직후에서 CPU-only exhaustive calibration을 수행했을 때 실제 large-gap coverage rate와 candidate density는 얼마이며, 그 실측값으로부터 \(10^{21},10^{22},10^{23}\) 및 알려진 1858 후보 위치까지의 exhaustive verification에 필요한 시간을 얼마나 신뢰성 있게 추정할 수 있는가?**

본 실험의 목적은 처음부터 수년짜리 계산을 시작하는 것이 아니라,

\[
\boxed{
\text{작은 실제 계산}
\rightarrow
\text{실제 throughput 측정}
\rightarrow
\text{전체 계산량 추정}
\rightarrow
\text{실행 여부 결정}
}
\]

의 순서로 **실행 가능성을 정량적으로 판단하는 것**이다.

---

## 검토 요청

Codex는 이 제안서를 기준으로 다음을 우선 평가한다.

1. `prime-gap`이 calibration용 benchmark 및 탐색용으로 적합한가?
2. `gap > 1854` threshold를 이용해 기존 구현에서 제거할 수 있는 실제 계산량은 얼마인가?
3. calibration block의 크기가 충분한가?
4. exhaustive coverage를 보장할 수 있는가?
5. 실제 측정된 throughput으로 \(10^{21}\), \(10^{22}\), \(10^{23}\), \(X_1\)까지의 시간을 얼마나 좁은 오차범위로 추정할 수 있는가?
6. 6개월 이내의 실현 가능성을 판단할 수 있는가?

**이 검토가 완료되기 전에는 전체 \(10^{20}\rightarrow3.94\times10^{25}\) 범위의 장기 실행을 시작하지 않는다.**