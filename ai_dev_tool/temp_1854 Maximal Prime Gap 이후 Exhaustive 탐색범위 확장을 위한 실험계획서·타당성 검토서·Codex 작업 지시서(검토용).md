# 1854 Maximal Prime Gap 이후 Exhaustive 탐색범위 확장을 위한 실험계획서·타당성 검토서·Codex 작업 지시서

## 0. 연구 목표

현재 확인된 maximal prime gap:

- Gap = **1854**
- Gap start = `101412319996363309069`
- Rank = 85
- Status = Confirmed

다음 후보:

- Gap = **1858**
- Gap start = `39422251630462640179641871`
- Rank = 86
- Status = Unconfirmed

목표는 다음 구간을 exhaustive하게 탐색하여:

```text
101412319996363309069
<
p
<
39422251630462640179641871
```

에서

```text
next_prime(p) - p > 1854
```

인 모든 후보를 놓치지 않고 찾는 것이다.

최종적으로 다음을 판정할 수 있는 것이 목표다.

1. 1854보다 큰 prime gap이 해당 구간에 존재하는가?
2. 존재한다면 가장 작은 gap-start는 어디인가?
3. 그 gap의 실제 길이는 얼마인가?
4. 따라서 1854가 다음 maximal gap으로 유지되는 범위는 어디까지인가?
5. 현재 1858 후보가 실제 next maximal gap인지 검증할 수 있는가?

---

# 1. 가장 중요한 수학적 정의

다음을 사용한다.

\[
G(x)=\max_{p_n\le x}(p_{n+1}-p_n)
\]

현재:

\[
G(101412319996363309069)=1854
\]

이다.

우리가 찾는 것은:

\[
x^*=
\min\{p>101412319996363309069:
p_{next}-p>1854\}
\]

이다.

따라서 exhaustive 검증의 핵심 조건은:

```text
모든 p in [X0, X1) 에 대해
p가 gap-start가 되어
p_next - p > 1854
인지 검사하고,
그러한 p를 하나도 놓치지 않아야 한다.
```

중요:

- `1854 이하 gap`의 정확한 크기는 관심 대상이 아니다.
- `1856, 1858, 1860, ...` 중 어떤 값인지 미리 정할 필요가 없다.
- `1856만 찾는 검색`으로 대체하면 안 된다.
- `1858만 찾는 검색`도 exhaustive proof가 아니다.
- 후보의 실제 다음 소수까지 확인하여 실제 gap을 결정해야 한다.

---

# 2. 현재 사용 가능한 공개 후보 정보

다음 데이터는 이미 알려져 있다고 가정한다.

| Rank | Confirmed | Gap | Gap start |
|---:|:---:|---:|---:|
| 85 | Y | 1854 | 101412319996363309069 |
| 86 | N | 1858 | 39422251630462640179641871 |

따라서 1858 후보가 실제 gap이라는 사실과 별개로, 현재 우리의 실험 목표는 반드시 다음과 같이 정의한다.

```text
[X0, X1)
=
[101412319996363309069,
 39422251630462640179641871)
```

에서

```text
gap > 1854
```

인 모든 후보를 exhaustively 탐색한다.

1858 후보는 "탐색 종료 상한 후보"로 사용할 수 있지만,
그 후보 자체를 선험적으로 신뢰하여 중간 구간을 생략해서는 안 된다.

---

# 3. 기존 코드의 기준 구현

반드시 먼저 다음 저장소를 직접 분석한다.

```text
https://github.com/sethtroisi/prime-gap
```

특히:

```text
README / EXTENDED.md
BENCHMARKS.md
THEORY.md
combined_sieve
gap_stats
gap_test_simple
```

을 확인한다.

중요한 관찰:

- `combined_sieve`는 여러 구간을 동시에 sieve한다.
- `combined_sieve`의 주요 병목은 `modulo_search_*` 계열이다.
- `Method2`가 일반적으로 `Method1`보다 빠르다.
- `--sieve-range`는 PRP 테스트를 줄이는 역할을 하며, 너무 크게 하면 sieve 비용이 커진다.
- `gap_stats`는 실제 gap test에 들어갈 대상을 확률적으로 우선순위화할 수 있다.
- `THEORY.md`에는 `D`, primorial, coprime interval, skipped PRP, one-sided tests 등의 최적화가 설명되어 있다.
- 단, `gap_stats`의 확률 모델은 **탐색 순서 최적화용**이지 exhaustive proof 자체가 아니다.

Codex는 반드시 현재 저장소의 실제 구현을 읽고, 위의 개념을 코드 수준에서 확인해야 한다.

---

# 4. 기존 maximal-gap 검색법과 이번 실험의 차이

이번 작업은 완전히 새로운 prime-gap 알고리즘을 발명하려는 것이 아니다.

기존 maximal-gap 검색은 대략:

```text
large interval
→ sieve
→ surviving candidates
→ prime/gap analysis
→ record gap detection
```

구조를 사용한다.

이번 실험에서는 이미:

```text
G(X0) = 1854
```

라는 선행 정보가 있기 때문에 목적을:

```text
전체 maximal gap 분포 계산
```

이 아니라

```text
gap > 1854 인 후보만 exhaustive하게 검출
```

로 특화한다.

따라서 다음 두 가지를 비교한다.

### Baseline A

기존 `prime-gap` 프로그램을 최대한 그대로 사용하여 해당 범위를 탐색.

### Experimental B

`combined_sieve`를 다음 조건에 맞춰 특화:

```text
threshold = 1854
target = existence of a prime gap > 1854
```

가능한 경우:

- one-sided test 적극 활용
- previous prime에서 이미 gap <=1854가 확정되면 불필요한 next-side 작업 생략
- 1854-length composite run 후보만 후속 검사
- 필요한 경우 sieve pattern을 gap threshold에 맞게 최적화
- 그러나 exhaustive coverage를 절대 희생하지 않음

두 방법의 처리량을 실제 benchmark로 비교한다.

---

# 5. Cramér 모델의 사용 범위

Cramér 규모:

\[
g(x)\sim(\log x)^2
\]

또는 refined large-gap heuristic을 사용할 수 있다.

그러나 반드시 다음 원칙을 지킨다.

### 허용

- 탐색 순서 결정
- 어느 구간을 먼저 실험할지 결정
- 예상 후보 밀도 추정
- benchmark 범위 선정
- `gap_stats`의 probability ranking 보조

### 금지

다음과 같은 이유로 구간을 생략하지 않는다.

```text
Cramér상 여기서는 gap >1854가 희박하므로 생략
```

그렇게 하면 exhaustive가 아니다.

즉:

```text
Cramér = heuristic / prioritization
```

이고

```text
sieve = exact elimination
```

이다.

---

# 6. residue / wheel / combined sieve 전략

목표 gap은:

\[
g>1854
\]

이다.

소수 \(p>2\)에서 다음 소수까지의 gap은 짝수이므로 첫 가능한 값은:

\[
1856
\]

이다.

따라서 후보 \(p\)가 large-gap start가 되려면:

\[
p+1,\ldots,p+1855
\]

가 모두 composite이어야 한다.

즉 다음 조건을 사용한다.

```text
Candidate p
↓
p+1 ... p+1855 안에 prime이 존재하는가?
↓
존재하면 즉시 reject
없으면 large-gap candidate
↓
p+1856 이후 최초의 prime 탐색
```

중요:

`p+1856이 prime인지`만 검사하면 안 된다.

반드시:

```text
p+1 ... p+1855가 모두 composite
```

임을 확인해야 한다.

---

# 7. residue pattern 사전 계산 실험

다음 두 방식을 분리해 benchmark한다.

## A. 작은 소수별 mask precomputation

각 작은 소수 \(q\)와 각 residue \(r\)에 대해:

\[
p\equiv r\pmod q
\]

일 때

\[
p+i\equiv0\pmod q
\]

가 되는 offset \(i\)를 bitmask로 저장한다.

예:

```text
mask[q][r]
```

단, 내부 gap 길이는 1855이므로 약 1855-bit mask면 충분하다.

2는 별도 처리한다.

실제 관심 offset은 홀수 소수 p에 대해 사실상 짝수 offset 위주로 제한할 수 있다.

이 precomputation 자체가 얼마나 걸리는지 측정한다.

## B. 전체 CRT residue space precomputation은 하지 않는다.

예를 들어 큰 primorial 전체의 residue class를 전부 열거하는 방법은 금지한다.

이는 residue 공간이 폭발하기 때문이다.

대신:

```text
per-prime masks
+
runtime combination
```

을 기본 방식으로 한다.

---

# 8. 사전 계산 benchmark

다음 small-prime limit을 각각 시험한다.

```text
B = 43
B = 59
B = 97
B = 127
B = 251
B = 509
B = 1000
```

각 경우 측정:

1. precomputation time
2. memory
3. candidate filtering rate
4. runtime overhead
5. 실제 expensive primality test 감소량

최적화 목적은 단순 filtering percentage가 아니다.

다음 metric을 사용한다.

\[
\text{total time}
=
\text{sieve time}
+
\text{candidate processing time}
+
\text{PRP time}
+
\text{proof time}
\]

---

# 9. Primorial / D 선택 실험

`THEORY.md`의 내용에 따라 여러 \(P\), \(D\) 조합을 benchmark한다.

최소 후보:

```text
P = 43, 59, 71
D = 210
```

추가:

```text
D = 30
D = 210
D = 2310
D = 30030
```

단, 가능한 모든 조합을 무작정 시도하지 말고:

1. m-count
2. coprime count
3. estimated unknown count
4. benchmark runtime

을 이용해 후보를 줄인다.

`THEORY.md`에서 small primorial D를 사용하는 것이 일반적인 최적화라고 설명되어 있으므로 반드시 기존 알고리즘의 구조와 비교한다.

---

# 10. 첫 번째 실험: 작은 구간에서 correctness 검증

곧바로 \(10^{25}\)로 가지 않는다.

다음과 같이 작게 검증한다.

```text
10^12
10^14
10^16
10^18
10^20
```

각 구간에서:

### Reference

기존 일반 prime sieve로 정확한 \(G(x)\)를 계산한다.

### Experimental

새 threshold-specific 알고리즘으로:

```text
gap > known_G_threshold
```

후보만 탐색한다.

두 결과가 동일해야 한다.

특히 확인:

- candidate 누락 여부
- gap length
- gap start
- first occurrence
- record gap
- 마지막 상태

---

# 11. Exhaustive correctness invariant

새 구현은 다음 invariant를 만족해야 한다.

모든 후보 start \(p\)에 대해:

```text
p is prime
AND
p+1 ... p+1855 are all composite
```

일 때만 `large_gap_candidate`가 된다.

반대로 실제 gap이:

```text
>1854
```

이면 반드시 candidate set에 포함되어야 한다.

즉:

\[
\text{True large gap}
\Rightarrow
\text{candidate survives sieve}
\]

가 반드시 성립해야 한다.

sieve는 false positive를 남길 수 있어도 되지만, false negative는 허용되지 않는다.

---

# 12. 두 번째 실험: threshold-specific 최적화

baseline:

```text
기존 combined_sieve
```

experimental:

```text
combined_sieve
+
1854 threshold
+
one-sided gap skipping
+
large-gap-only candidate handling
+
residue masks
```

다음 metric을 비교한다.

```text
wall time
CPU time
memory
m/s
candidate/s
PRP/s
number of PRP tests
number of skipped PRP
number of final candidates
```

속도 향상률:

\[
S=
\frac{T_{baseline}}
{T_{experimental}}
\]

을 계산한다.

---

# 13. 세 번째 실험: 실제 목표 구간을 여러 블록으로 분할

전체 구간:

```text
X0 = 101412319996363309069
X1 = 39422251630462640179641871
```

를 한 번에 돌리지 않는다.

로그 스케일로 다음과 같이 나눈다.

```text
[1.0e20, 2.0e20]
[2.0e20, 5.0e20]
[5.0e20, 1.0e21]
[1.0e21, 2.0e21]
[2.0e21, 5.0e21]
...
```

단, 실제 block 경계는 구현 구조에 맞춰 결정한다.

각 블록마다 기록:

```text
block_start
block_end
elapsed_time
m_count
candidate_count
survivor_count
PRP_count
large_gap_count
best_gap
best_gap_start
```

이렇게 하면 전체 runtime을 단순 외삽하지 않고 실제 측정값으로 예측할 수 있다.

---

# 14. Cramér 예측 실험

각 block에 대해:

\[
C(x)=\frac{(\log x)^2}{1854}
\]

를 계산한다.

추가적으로 가능하면 refined gap model도 계산한다.

다음과 비교한다.

```text
predicted gap scale
actual maximal gap found
candidate density
sieve survivor density
```

목적은:

```text
Cramér를 proof에 사용
```

하는 것이 아니라,

```text
benchmark / workload prediction
```

에 얼마나 유용한지 평가하는 것이다.

---

# 15. 1858 후보를 통한 중간 종료 조건

오른쪽 경계:

```text
39422251630462640179641871
```

에서 실제로 1858 gap이 성립하는지를 먼저 독립 검증할 수 있다.

그것이 맞다면:

```text
X1 = next known large-gap candidate
```

로 사용할 수 있다.

그러나 X0와 X1 사이에 다른:

```text
1856+
```

gap이 있는지 exhaustive하게 탐색해야 한다.

가장 작은 candidate start:

\[
x^*=
\min\{p:
p> X_0,\,
gap(p)>1854\}
\]

를 찾아야 한다.

---

# 16. 예상 computational scale 계산

Codex는 benchmark 결과를 이용해서 다음 값을 실제 측정해야 한다.

### 기본량

\[
N_p\approx \pi(X_1)-\pi(X_0)
\]

를 계산한다.

그러나 prime-by-prime enumeration 비용만 계산하지 않는다.

실제 `combined_sieve` 방식에 맞춰:

```text
P#
D
K = P#/D
m_start
m_end
coprime m count
interval count
sieve_length
```

을 계산한다.

### 출력

```text
Estimated total m
Estimated sieve operations
Estimated candidate count
Estimated PRP count
Estimated wall time
```

---

# 17. 반드시 benchmark 기반으로 runtime을 추정

저장소의 benchmark를 단순 선형 외삽하지 말 것.

특히 다음 현상을 고려해야 한다.

- `--minc` scaling 비선형
- cache pressure
- large integer modulo cost
- sieve range가 너무 커질 때의 diminishing return
- PRP cost 증가
- CPU architecture 차이

따라서 최소 3개 이상의 실제 benchmark point를 얻은 후 회귀한다.

예:

\[
T(M)=aM+bM^\alpha
\]

같은 모델을 시도하고,

\[
0<\alpha<1
\]

이 실제 측정과 맞는지 검증한다.

모델이 잘 맞지 않으면 구간별 piecewise model을 사용한다.

---

# 18. 개인 PC 기준 calibration

최종 대규모 실행 전 반드시 현재 PC에서 다음 benchmark를 수행한다.

가능하면:

```text
1 million m
10 million m
50 million m
100 million m
```

규모를 각각 측정한다.

각각에 대해:

```text
wall time
CPU utilization
RAM
L3/cache
candidate rate
```

를 기록한다.

그 결과를 이용하여 전체 범위 runtime을 추정한다.

---

# 19. GPU 사용 가능성

저장소의 GPU gap test가 제공하는 부분과 CPU `combined_sieve`를 구분한다.

실험:

```text
CPU-only
CPU sieve + GPU gap test
GPU-enabled variant
```

를 별도로 비교한다.

다만 GPU를 사용한다고 해서 전체 exhaustive sieve가 자동으로 빨라진다고 가정하지 않는다.

병목이:

```text
sieve
```

인지

```text
PRP
```

인지 먼저 profiling한다.

---

# 20. 최종 실험 성공 기준

다음 4가지가 모두 충족되어야 실험 성공으로 판단한다.

### A. Correctness

작은 범위에서 reference와 결과가 100% 일치.

### B. No candidate loss

synthetic known gaps를 삽입한 테스트에서 threshold-specific sieve가 모든 gap을 검출.

### C. Exhaustive coverage

실제 목표 범위 전체가 gap candidate 조건으로 coverage됨.

### D. Performance

baseline보다 실질적인 wall-time 감소.

단순히 candidate 수가 감소하는 것만으로 성공으로 판단하지 않는다.

---

# 21. 최종 탐색 절차

검증된 implementation으로 최종적으로 다음을 실행한다.

```text
Phase 1
X0 ~ X1 coverage preparation

Phase 2
1854-threshold combined sieve

Phase 3
all surviving large-gap candidates extraction

Phase 4
exact next-prime determination

Phase 5
candidate sorting by gap-start

Phase 6
smallest gap-start verification

Phase 7
independent re-verification of the winning gap

Phase 8
coverage certificate / log generation
```

최종 결과는 반드시 다음 형식으로 저장한다.

```text
range_start
range_end

known_previous_record = 1854

candidate_count

for each candidate:
    gap_start
    next_prime
    gap

minimum_gap_start
minimum_gap
```

그리고 coverage checksum 또는 block hash를 저장한다.

---

# 22. 절대로 하면 안 되는 것

다음 방식은 exhaustive라고 부르지 않는다.

```text
Cramér에서 gap 가능성이 낮으므로 구간 생략
```

```text
1858 후보가 있으므로 그 앞 일부만 검색
```

```text
1856 gap만 검색
```

```text
1936 gap만 검색
```

```text
Mills / Mersenne 등 특정 생성식에서만 gap 검색
```

```text
PRP 결과만 있고 compositeness coverage가 없는 상태
```

```text
residue sieve에서 살아남지 않았다는 것만으로 composite라고 추정
```

---

# 23. Codex가 먼저 해야 할 작업

1. `sethtroisi/prime-gap` 저장소의 실제 코드를 분석한다.
2. `combined_sieve`, `gap_stats`, `gap_test_simple`의 데이터 흐름을 파악한다.
3. `BENCHMARKS.md`, `EXTENDED.md`, `THEORY.md`의 benchmark 및 최적화 내용을 코드와 대조한다.
4. 현재 구현이 `1854-threshold-only exhaustive search`로 어떻게 변형될 수 있는지 분석한다.
5. 기존 구현을 수정하기 전 작은 범위에서 reference와 동일한 결과를 내는지 확인한다.
6. 현재 CPU/GPU 환경에서 calibration benchmark를 수행한다.
7. 실제 목표 구간의 runtime을 benchmark 기반으로 추정한다.
8. 그 다음에야 전체 구간 탐색 여부를 판단한다.

---

# 24. 실험 결과 보고서에 반드시 포함할 것

```text
1. Baseline implementation
2. Experimental implementation
3. Correctness comparison
4. Candidate reduction ratio
5. PRP reduction ratio
6. Sieve overhead
7. Runtime speedup
8. Memory usage
9. Scaling model
10. Estimated full-range runtime
11. Exhaustive coverage proof method
12. Any assumptions / heuristic components
13. Whether Cramér is used only for prioritization
14. Whether residue sieve introduces any possibility of false negative
15. Final recommendation
```

---

# 25. 최종 연구 질문

이 실험의 핵심 질문은 다음 하나로 요약한다.

> 현재 confirmed maximal gap이 1854임을 알고 있을 때,  
> `101412319996363309069`부터 `39422251630462640179641871`까지의 구간에서  
> `gap > 1854`인 최초의 prime gap을 exhaustive하게 탐색하는 데  
> 기존 `prime-gap`의 combined-sieve를 threshold-specific 방식으로 최적화하면  
> 기존 maximal-gap 탐색 대비 실제 계산량과 wall time을 얼마나 줄일 수 있는가?

그리고 최종적으로:

\[
\boxed{
x^*=
\min\{p>101412319996363309069:
p_{next}-p>1854\}
}
\]

를 결정하는 것을 목표로 한다.

이 값이 존재하고 그 뒤의 모든 계산이 독립적으로 검증되면:

\[
G(x)=1854
\]

가 유지되는 최대 exhaustive-verified 범위를 확장할 수 있다.

# 26. Codex 작업 방식

작업 중에는 다음 원칙을 지킨다.

- 기존 구현을 임의로 크게 변경하지 않는다.
- 모든 최적화는 baseline과 benchmark 비교를 남긴다.
- heuristic과 proof logic을 코드 레벨에서 분리한다.
- candidate filtering은 false negative가 없어야 한다.
- 각 최적화 단계마다 작은 reference range에서 exact comparison을 수행한다.
- 대규모 실행 전 예상 runtime과 실제 calibration 결과를 비교한다.
- 결과 로그는 재현 가능하도록 명령행 옵션과 git commit hash를 함께 저장한다.
- "검색했다"와 "exhaustively verified했다"를 구분하여 보고한다.

최종 산출물은 단순히 "gap을 찾았다"가 아니라:

```text
verified search range
+
algorithm
+
candidate elimination logic
+
coverage evidence
+
runtime benchmark
+
result
```

형태로 남긴다.