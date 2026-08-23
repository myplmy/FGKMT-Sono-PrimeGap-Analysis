# Maximal Prime Gap Plateau·Recurrence 통계 분석
## 실험 타당성 검증 및 실행 준비 문서

---

# 0. 문서 목적

본 문서는 기존에 exhaustive하게 검증된 prime-gap 탐색 범위에서 **maximal prime gap이 갱신되지 않고 유지되는 구간(plateau)​**과 그 구간에서 **현재 maximal gap과 동일한 gap이 몇 차례 재출현하는지**를 정량적으로 분석하기 위한 실험의 타당성을 검토하고, 타당성이 확인될 경우 실제 실험을 수행할 수 있도록 계산 정의와 실행 절차를 명확히 규정하는 것을 목적으로 한다.

본 문서는 실험 자체의 결과를 주장하는 문서가 아니다.

먼저 다음 질문을 검증해야 한다.

> 기존 exhaustive prime-gap 검증 데이터 또는 이를 재생성할 수 있는 계산 절차를 이용하여, maximal-gap plateau length와 record-gap recurrence를 신뢰성 있게 계산할 수 있는가?

그 결과가 타당하다고 판단될 경우에만 실제 데이터 수집 및 분석을 수행한다.

---

# 1. 실험의 배경

소수열을

\[
p_1,p_2,p_3,\ldots
\]

라고 하고, 연속 소수 사이의 간격을

\[
g_n=p_{n+1}-p_n
\]

으로 정의한다.

최대 소수 간격 함수를

\[
G(x)=\max_{p_n\le x} g_n
\]

로 정의한다.

어떤 지점에서 새로운 maximal gap이 발견되면 \(G(x)\)가 증가한다.

예를 들어 다음과 같은 가상의 상황을 생각한다.

\[
G(x)=100
\]

이던 구간에서 어느 소수 \(x_k\)에서 gap 110이 처음 발견되었다면:

\[
G(x)=110
\]

이후 다음 maximal gap 120이 등장하는 \(x_{k+1}\) 직전까지 유지된다.

따라서

\[
x_k\le x<x_{k+1}
\]

에서는

\[
G(x)=G_k
\]

이다.

본 실험은 이 plateau 구간 안에서 단순히 \(G(x)\)의 값만 보는 것이 아니라, 그 기록이 유지되는 동안 발생하는 **동일 크기 maximal gap의 재출현 빈도**를 추가적으로 측정한다.

---

# 2. 실험의 핵심 의도

본 실험의 핵심 의도는 다음 질문을 정량적으로 검토하는 것이다.

> 하나의 maximal prime gap \(G_k\)가 새로운 기록을 세운 뒤 다음 maximal gap이 출현할 때까지, 해당 gap은 얼마나 오랫동안 maximal record의 지위를 유지하며, 그 동안 동일한 크기의 gap은 몇 번 재출현하는가?

이를 세 가지 통계량으로 분리한다.

### ① Record plateau length

현재 maximal gap이 maximal record로 유지되는 \(x\)-범위의 로그 길이.

### ② Exact recurrence count

해당 plateau 동안 동일한 gap \(G_k\)가 다시 발생한 횟수.

### ③ Relative recurrence rate

해당 plateau에서 발생한 전체 prime gap 중 동일 gap \(G_k\)가 차지하는 비율.

---

# 3. 실험의 구체적 목적

본 실험에서는 다음 값을 도출한다.

각 maximal-gap record \(k\)에 대해:

\[
L_k
\]

\[
C_k
\]

\[
R_k
\]

을 계산한다.

그리고 필요하다면 추가적으로:

\[
M_k=1+C_k
\]

를 계산한다.

여기서 \(M_k\)는 **record gap이 처음 record를 만든 사건까지 포함한 총 발생 횟수**다.

이를 이용하여 다음 관계를 탐색한다.

1. 오래 유지된 maximal gap일수록 동일 gap의 recurrence가 더 많은가?
2. plateau length와 recurrence count 사이에 상관관계가 있는가?
3. 단순 recurrence count가 아니라 recurrence rate로 정규화했을 때도 관계가 유지되는가?
4. maximal gap이 증가할수록 recurrence 특성이 변화하는가?
5. 관찰된 recurrence가 단순히 더 많은 소수를 관측했기 때문에 발생한 것인지, 아니면 상대적인 빈도에서도 차이가 존재하는가?

---

# 4. 가장 중요한 사전 타당성 검증 항목

실험 전에 반드시 다음을 확인한다.

## 4.1 기존 exhaustive 결과가 무엇을 저장하는가

기존 공개 자료가 다음을 모두 제공하는지 확인한다.

```text
p_n
p_{n+1}
g_n = p_{n+1}-p_n
```

만약 모든 연속 소수쌍의 데이터가 존재한다면 추가 계산 없이 바로 recurrence 통계를 계산할 수 있다.

반대로 공개 데이터가:

```text
maximal gap
first occurrence
record start
```

만 제공한다면 \(C_k\)는 직접 계산할 수 없다.

이 경우 두 가지 대안이 있다.

### 방법 A

기존 exhaustive 계산의 원시 결과/로그/데이터베이스를 확보한다.

### 방법 B

동일한 exhaustive 알고리즘을 동일 범위에서 다시 실행하되 recurrence counter를 추가한다.

---

# 5. 기존 maximal-gap record와 recurrence 데이터의 차이

maximal-gap record 데이터는 일반적으로:

\[
(x_k,G_k)
\]

를 기록하는 것에 초점이 있다.

즉:

> 이 gap이 언제 처음 maximal record가 되었는가?

를 나타낸다.

하지만 본 실험의 핵심 질문인

\[
C_k
\]

는:

> 그 이후 다음 record가 나타날 때까지 동일 gap이 몇 번 더 등장했는가?

를 묻는다.

따라서 maximal-gap record 표만으로는 일반적으로 \(C_k\)를 복원할 수 없다.

이는 실험 타당성 검토에서 반드시 명시해야 한다.

---

# 6. 기호 및 숫자 정의

## 6.1 소수

\[
p_n
\]

: \(n\)번째 소수.

---

## 6.2 연속 소수 간격

\[
g_n=p_{n+1}-p_n
\]

: \(n\)번째 소수와 다음 소수 사이의 gap.

---

## 6.3 Maximal gap function

\[
G(x)=\max_{p_n\le x}g_n
\]

: \(x\) 이하에서 발견된 최대 prime gap.

---

## 6.4 \(k\)번째 maximal-gap record

\[
G_k
\]

: \(k\)번째 maximal-gap 기록의 gap 크기.

---

## 6.5 Record start

\[
x_k
\]

: \(G_k\)가 최초로 등장하여 기존 maximal gap을 갱신한 **gap의 시작 소수**.

즉:

\[
g_n=G_k,\qquad p_n=x_k
\]

이다.

---

## 6.6 다음 record start

\[
x_{k+1}
\]

: 다음 maximal gap \(G_{k+1}>G_k\)가 최초로 등장하는 gap의 시작 소수.

---

# 7. Record Plateau 정의

\(k\)번째 maximal gap이 처음 등장한 위치가 \(x_k\), 다음 maximal gap이 처음 등장한 위치가 \(x_{k+1}\)라면:

\[
x_k\le x<x_{k+1}
\]

에서:

\[
G(x)=G_k
\]

이다.

이 구간을 **\(k\)번째 record plateau​**라고 정의한다.

중요:

plateau는

> \(G_k\)라는 gap이 실제로 계속 반복되는 구간

이 아니라,

> \(G(x)\)의 maximal value가 \(G_k\)에서 변화하지 않는 구간

이다.

따라서 plateau 안에는:

- \(G_k\)와 같은 gap
- \(G_k\)보다 작은 gap

이 모두 존재할 수 있다.

---

# 8. ① Plateau Length

정의:

\[
L_k=
\log\left(\frac{x_{k+1}}{x_k}\right)
\]

기본 로그는 자연로그 \(\ln\)으로 한다.

필요한 경우 보조적으로:

\[
L_k^{(10)}
=
\log_{10}
\left(
\frac{x_{k+1}}{x_k}
\right)
\]

도 기록한다.

---

## 8.1 의미

\(L_k\)는:

> \(G_k\)가 maximal record로 유지된 \(x\)-범위의 상대적인 규모

를 나타낸다.

단순한:

\[
x_{k+1}-x_k
\]

대신 비율:

\[
\frac{x_{k+1}}{x_k}
\]

을 사용한다.

이는 prime-gap의 규모가 매우 빠르게 증가하기 때문에 절대적인 차이보다 로그 비율이 비교에 유리하기 때문이다.

---

## 8.2 예시

\[
x_k=10^{20},\qquad
x_{k+1}=10^{25}
\]

이면:

\[
L_k
=
\ln(10^5)
=
5\ln10
\approx11.513
\]

이고:

\[
L_k^{(10)}=5
\]

이다.

즉 약 5 decimal orders 동안 동일 maximal-gap record가 유지되었다고 해석한다.

---

# 9. ② Exact Recurrence Count

정의:

\[
C_k=
\#\left\{
n:
x_k<p_n<x_{k+1},
\quad
g_n=G_k
\right\}
\]

즉:

> record를 처음 만든 \(G_k\) gap 이후, 다음 maximal record가 나타나기 전까지 같은 크기의 gap \(G_k\)가 몇 번 더 등장했는가?

를 센다.

---

## 9.1 최초 record occurrence는 제외

정의에서:

\[
x_k<p_n
\]

로 설정했기 때문에 \(x_k\)에서 최초로 record를 만든 gap은 \(C_k\)에 포함되지 않는다.

따라서:

\[
M_k=1+C_k
\]

를 정의하면 \(G_k\) gap의 plateau 전체 발생 횟수를 얻을 수 있다.

---

## 9.2 예시

다음과 같은 gap sequence가 있다고 하자.

```text
100, 50, 100, 70, 100, 80, 110
```

첫 번째 100이 \(G_k=100\)을 만드는 record이고 마지막 110에서 record가 갱신된다.

그러면:

\[
C_k=2
\]

이고:

\[
M_k=3
\]

이다.

즉 100-gap은 plateau 동안 총 3번 발생했다.

---

# 10. ③ Relative Recurrence Rate

정의:

\[
R_k=
\frac{C_k}
{\pi(x_{k+1})-\pi(x_k)}
\]

여기서:

\[
\pi(x)
\]

는 \(x\) 이하의 소수 개수이다.

따라서 분모:

\[
\pi(x_{k+1})-\pi(x_k)
\]

는 해당 plateau 구간에 속하는 소수의 개수를 의미한다.

---

## 10.1 의미

\(R_k\)는:

> 해당 plateau에서 관찰된 gap들 중 기존 maximal gap과 정확히 같은 gap이 얼마나 자주 나타났는가?

를 나타내는 상대 빈도이다.

---

## 10.2 예시

어떤 plateau 동안:

\[
C_k=20
\]

이고:

\[
\pi(x_{k+1})-\pi(x_k)=1,000,000
\]

이면:

\[
R_k
=
\frac{20}{1,000,000}
=
2\times10^{-5}
\]

즉:

\[
0.002\%
\]

이다.

---

# 11. Plateau Length와 Gap Multiplicity의 차이

두 개념은 반드시 구별한다.

## Record Plateau Length

\[
L_k
\]

는:

> **record가 얼마나 오랫동안 유지되었는가?**

를 측정한다.

---

## Record Gap Multiplicity

\[
M_k=1+C_k
\]

는:

> **그 record gap이 그 기간 동안 몇 번 발생했는가?**

를 측정한다.

---

## 11.1 예시 A

\[
x_k=10^{20}
\]

에서 \(G_k=1854\)가 기록되었고:

\[
x_{k+1}=10^{25}
\]

에서 새로운 기록이 나왔다고 하자.

그러면:

\[
L_k^{(10)}=5
\]

이다.

그 기간에 1854-gap이 총 3번 발생했다면:

\[
M_k=3
\]

이다.

---

## 11.2 예시 B

똑같이:

\[
x_k=10^{20}
\]

\[
x_{k+1}=10^{25}
\]

이지만 1854-gap이 총 100번 발생했다면:

\[
L_k^{(10)}=5
\]

는 동일하지만:

\[
M_k=100
\]

이다.

따라서:

\[
L_k
\]

와

\[
M_k
\]

는 완전히 다른 정보를 제공한다.

---

# 12. 왜 단순 Recurrence Count만으로는 충분하지 않은가

\(C_k\)는 plateau가 길어질수록 자연스럽게 증가할 가능성이 있다.

예:

```text
Plateau A
소수 10만 개 관측
1854-gap = 5회

Plateau B
소수 10억 개 관측
1854-gap = 500회
```

단순히:

\[
500>5
\]

라는 사실만으로 B에서 1854-gap이 더 자주 나타난다고 결론내릴 수 없다.

관측 opportunity 자체가 훨씬 많기 때문이다.

따라서:

\[
R_k
\]

를 함께 계산해야 한다.

---

# 13. 반드시 수집해야 하는 핵심 데이터

각 maximal-gap plateau마다 최소 다음 값을 저장한다.

```text
k
G_k
x_k
x_{k+1}
L_k
C_k
M_k
pi(x_{k+1}) - pi(x_k)
R_k
```

권장 추가 데이터:

```text
plateau_decimal_orders
total_gap_count
mean_gap
median_gap
next_record_gap = G_{k+1}
record_gap_merit
```

---

# 14. 마지막 plateau의 특별한 처리

가장 중요한 주의사항이다.

현재 exhaustive 검증 범위의 마지막 maximal-gap record에 대해서는:

\[
x_{k+1}
\]

이 검증 범위 밖에 있을 수 있다.

그 경우 해당 plateau의 전체 길이와 recurrence count는 완전히 관측되지 않는다.

예:

검증 범위가:

\[
[x_k,X_{\max}]
\]

이고 다음 record가 아직 발견되지 않았다면:

\[
x_{k+1}>X_{\max}
\]

이다.

이 경우:

\[
L_k
\]

와

\[
C_k
\]

는 완전한 값이 아니다.

이러한 record는:

\[
\boxed{\text{right-censored}}
\]

로 표시하고 일반 plateau와 별도로 처리한다.

절대로 관측된 구간만으로 완전한 \(L_k,C_k\)라고 주장하지 않는다.

---

# 15. 분석 대상 선정

실험은 두 단계로 수행한다.

## 단계 A — 완료된 plateau만 분석

조건:

\[
x_{k+1}
\]

이 실제 exhaustive 검증 범위 내에 존재하는 maximal-gap record만 포함한다.

이렇게 하면 \(L_k,C_k,R_k\)가 모두 완전하게 정의된다.

## 단계 B — 마지막 미완료 plateau 별도 보고

다음 record가 검증 범위 밖인 경우:

```text
status = right-censored
```

로만 기록한다.

---

# 16. 첫 번째 실험 대상

가장 먼저 모든 maximal-gap record에 대해 전체 분석을 시도하되, 타당성 검증을 위해 다음 우선순위를 둔다.

### Pilot

작은 exhaustive 범위에서:

\[
10^n
\]

단위의 기존 검증 데이터가 확보된 구간을 사용한다.

### Main

모든 완전한 maximal-gap plateau를 대상으로 한다.

### Special case

현재 관심이 집중된 1854 plateau는 별도로 분석한다.

단, 1854 plateau의 오른쪽 끝이 아직 확정된 next maximal gap이 아니라면 right-censored 여부를 먼저 확인한다.

---

# 17. 실제 실행 방법

## 방법 1 — 기존 전체 gap 데이터가 존재하는 경우

가능하면 이 방법을 우선한다.

기존 데이터에서 각 row:

```text
p_n
p_{n+1}
gap
```

을 순차적으로 읽는다.

현재 record를 추적한다.

의사코드:

```text
current_record = initial record
current_record_start = initial start
recurrence_count = 0

for each consecutive prime pair (p, q):
    gap = q - p

    if gap > current_record:
        finalize previous plateau
        current_record = gap
        current_record_start = p
        recurrence_count = 0

    else if gap == current_record:
        recurrence_count += 1
```

실제 구현에서는 record transition 시점과 포함/제외 규칙을 엄밀하게 확인한다.

---

# 18. 방법 2 — 전체 gap 데이터가 없는 경우

기존 exhaustive 알고리즘을 동일한 범위에서 재실행한다.

단순히 maximal gap만 저장하지 말고 다음 counter를 추가한다.

```text
current_record_gap
current_record_start
recurrence_count
total_gap_count
```

gap이 계산될 때마다:

\[
g_n=p_{n+1}-p_n
\]

를 검사한다.

---

# 19. 실험 결과의 독립 검증

각 plateau에 대해:

\[
C_k
\]

를 계산한 후 독립적인 두 방식 중 하나로 검산한다.

### 검산 A

gap histogram 전체를 생성하고:

\[
\text{histogram}[G_k]
\]

와 비교.

### 검산 B

해당 plateau만 다시 읽어서:

\[
g_n=G_k
\]

조건을 재검사.

두 결과가 일치해야 한다.

---

# 20. 정확성 검증

작은 reference 범위에서 모든:

\[
p_n,p_{n+1},g_n
\]

을 직접 생성하여:

\[
G(x)
\]

를 계산한다.

그 결과로부터 독립적으로:

\[
L_k,C_k,R_k
\]

를 계산한다.

실험 프로그램의 결과와 100% 일치해야 한다.

---

# 21. 도출하려는 1차 결과

각 plateau:

\[
k
\]

에 대해:

\[
(G_k,x_k,x_{k+1},L_k,C_k,R_k)
\]

를 확보한다.

이것이 기본 결과 데이터셋이다.

---

# 22. 도출하려는 2차 결과

다음 상관관계를 분석한다.

## 22.1 Plateau length vs recurrence count

\[
L_k
\quad\text{vs}\quad
C_k
\]

질문:

> 오래 유지된 record일수록 같은 gap이 더 많이 반복되는가?

---

## 22.2 Plateau length vs recurrence rate

\[
L_k
\quad\text{vs}\quad
R_k
\]

질문:

> 긴 plateau에서 단순 관측 기회 증가를 정규화한 후에도 recurrence rate가 증가하는가?

---

## 22.3 Gap size vs recurrence

\[
G_k
\quad\text{vs}\quad
C_k
\]

\[
G_k
\quad\text{vs}\quad
R_k
\]

질문:

> maximal gap의 크기가 커질수록 recurrence 특성이 변하는가?

---

## 22.4 Plateau length vs next-record increase

\[
L_k
\quad\text{vs}\quad
G_{k+1}-G_k
\]

질문:

> record가 오래 유지된 경우 다음 기록의 증가폭이 큰가?

단, 이 항목은 탐색적 분석이며 인과관계를 주장하지 않는다.

---

# 23. 추가로 계산할 수 있는 값

## Record multiplicity

\[
M_k=1+C_k
\]

## Decimal plateau length

\[
L_k^{(10)}
=
\log_{10}
\left(
\frac{x_{k+1}}{x_k}
\right)
\]

## Plateau 소수 개수

\[
N_k=
\pi(x_{k+1})-\pi(x_k)
\]

## Recurrence rate

\[
R_k=\frac{C_k}{N_k}
\]

---

# 24. 해석에서 금지되는 주장

다음과 같은 결론은 단순한 관측만으로 주장하지 않는다.

```text
"오래 살아남은 maximal gap은 원래 재출현 확률이 높다."
```

```text
"Recurrence가 maximal-gap 생성 원인이다."
```

```text
"C_k와 L_k의 상관관계가 prime-gap의 새로운 법칙을 증명한다."
```

관측된 상관관계가 발견되더라도:

- 소수 개수 증가
- \(x\) 규모 증가
- gap distribution 변화
- selection effect
- record가 되는 조건 자체

등을 고려해야 한다.

---

# 25. 비교 기준

가능하면 단순한 raw recurrence count보다 다음을 비교한다.

\[
C_k
\]

\[
R_k
\]

그리고:

\[
L_k^{(10)}
\]

를 함께 본다.

특히:

\[
C_k
\]

가 증가하더라도:

\[
R_k
\]

가 감소한다면:

> 같은 gap이 더 많이 등장한 것은 단순히 관측된 소수의 수가 증가했기 때문일 수 있다.

반대로:

\[
R_k
\]

도 일정하게 유지되거나 증가한다면 더 흥미로운 통계적 특성이 있을 수 있다.

---

# 26. 통계 분석에서의 주의사항

maximal-gap record는 정의상 극단값을 선택한 결과다.

따라서:

\[
G_k
\]

자체가 selection bias를 포함한다.

또한 plateau와 recurrence count는 서로 독립적인 관측이 아니다.

따라서 단순 Pearson correlation 하나만 계산하지 않는다.

가능하면:

- Spearman correlation
- 로그 스케일 scatter plot
- \(L_k\) 대비 \(C_k\) 회귀
- \(L_k\) 대비 \(R_k\) 회귀
- record index별 변화

등을 함께 검토한다.

표본 수가 적으면 통계적 유의성을 과도하게 주장하지 않는다.

---

# 27. 실험의 가장 중요한 sanity check

가상의 극단 사례를 테스트한다.

### Case A

동일 record가 한 번만 등장:

\[
C_k=0
\]

\[
M_k=1
\]

### Case B

동일 record가 두 번 재출현:

\[
C_k=2
\]

\[
M_k=3
\]

### Case C

plateau 길이는 동일하지만 recurrence가 다른 경우:

\[
L_1=L_2
\]

\[
C_1\ne C_2
\]

프로그램이 이를 올바르게 구별해야 한다.

---

# 28. 1854 record에 대한 특별 분석

1854가 포함되는 plateau의 경우 다음을 계산한다.

\[
G_k=1854
\]

\[
x_k=101412319996363309069
\]

그 오른쪽 경계가 확정된 next record:

\[
x_{k+1}
\]

인지 확인한다.

만약 다음 1858 후보:

\[
39422251630462640179641871
\]

가 아직 unconfirmed라면:

```text
1854 plateau = right-censored / provisionally bounded
```

로 처리한다.

즉:

\[
L_k
\]

와

\[
C_k
\]

를 확정값으로 보고하지 않는다.

---

# 29. 실험 타당성 판정 기준

실험은 다음 조건을 모두 만족할 경우 "타당"으로 판정한다.

### 조건 1 — 데이터 접근성

각 완전한 plateau에 대해 연속 prime-gap 데이터를 확보할 수 있다.

### 조건 2 — 정의 가능성

\(x_k,x_{k+1},G_k\)가 명확하게 정의된다.

### 조건 3 — 계산 가능성

\(C_k\)를 누락 없이 계산할 수 있다.

### 조건 4 — 정규화 가능성

\[
\pi(x_{k+1})-\pi(x_k)
\]

를 정확하게 구할 수 있다.

### 조건 5 — 재현성

동일 입력에서 동일한:

\[
L_k,C_k,R_k
\]

를 재현할 수 있다.

### 조건 6 — right-censoring 처리

마지막 불완전 plateau를 완전한 관측값으로 잘못 취급하지 않는다.

---

# 30. 실험 실패 또는 보류 조건

다음 중 하나라도 발생하면 실험을 보류한다.

- exhaustive raw gap 데이터가 존재하지 않음
- 기존 exhaustive 범위의 정확한 경계를 확인할 수 없음
- plateau의 시작점/끝점을 정확히 정의할 수 없음
- \(C_k\)를 계산할 때 일부 gap이 누락될 가능성이 있음
- 기존 데이터와 재생성 결과가 일치하지 않음
- 마지막 right-censored plateau를 완전한 plateau로 처리해야만 분석이 가능함

---

# 31. 최종 산출물

최종적으로 다음 데이터셋을 생성한다.

| k | \(G_k\) | \(x_k\) | \(x_{k+1}\) | \(L_k\) | \(C_k\) | \(M_k\) | \(N_k\) | \(R_k\) | Status |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| … | … | … | … | … | … | … | … | … | complete/censored |

여기서:

- `complete`: 다음 maximal record까지 전체 관측
- `right-censored`: 검증 범위가 다음 record 이전에 끝남

으로 정의한다.

---

# 32. 최종적으로 검증하고자 하는 연구 가설

본 실험 자체는 다음 가설을 증명하기 위한 것이 아니다.

대신 다음 탐색적 질문을 검토한다.

### H1

\[
L_k\uparrow
\Rightarrow
C_k\uparrow
\]

즉 record plateau가 길수록 동일 maximal gap의 재출현 횟수가 증가하는가?

### H2

\[
L_k\uparrow
\Rightarrow
R_k\uparrow
\]

관측 기회 증가를 정규화해도 recurrence rate가 증가하는가?

### H3

\[
G_k\uparrow
\Rightarrow
R_k\downarrow
\]

maximal gap의 크기가 증가할수록 동일 gap의 상대적 재출현 빈도가 감소하는가?

H1~H3는 **검증 대상 가설**이지 전제되는 사실이 아니다.

---

# 33. 실험 실행 순서

## Phase 1 — 타당성 검증

- 기존 exhaustive 범위 확인
- 기존 데이터 형식 확인
- 모든 gap 데이터 존재 여부 확인
- maximal record 정의 확인
- plateau 경계 확인
- right-censoring 여부 확인

## Phase 2 — 작은 범위 검증

- 독립적인 prime enumeration
- \(G_k\) 재계산
- \(L_k\) 재계산
- \(C_k\) 재계산
- \(R_k\) 재계산
- reference와 비교

## Phase 3 — 전체 데이터 추출

완전한 plateau만 분석.

## Phase 4 — 통계 계산

\[
L_k,\ C_k,\ M_k,\ R_k
\]

계산.

## Phase 5 — exploratory analysis

- \(L\) vs \(C\)
- \(L\) vs \(R\)
- \(G\) vs \(C\)
- \(G\) vs \(R\)

분석.

## Phase 6 — 결과 검증

독립 실행으로 주요 통계 재현.

---

# 34. 최종적으로 얻고자 하는 핵심 값

각 maximal-gap record마다:

\[
\boxed{
L_k=
\ln(x_{k+1}/x_k)
}
\]

\[
\boxed{
C_k=
\#\{n:x_k<p_n<x_{k+1},g_n=G_k\}
}
\]

\[
\boxed{
M_k=1+C_k
}
\]

\[
\boxed{
R_k=
\frac{C_k}
{\pi(x_{k+1})-\pi(x_k)}
}
\]

를 얻는다.

그리고 이를 통해:

\[
\boxed{
\text{record longevity}
}
\]

\[
\boxed{
\text{record recurrence}
}
\]

\[
\boxed{
\text{normalized recurrence}
}
\]

를 각각 정량화한다.

---

# 35. ChatGPT 타당성 검증 후 다음 단계

타당성 검증 시 반드시 다음 질문에 답한다.

1. 기존 exhaustive prime-gap 검증 범위가 정확히 어디까지인가?
2. 해당 범위에서 모든 consecutive prime gap을 재구성할 수 있는가?
3. 공개된 데이터만으로 \(C_k\)를 계산할 수 있는가?
4. 계산할 수 없다면 기존 exhaustive 알고리즘을 어느 정도 재실행해야 하는가?
5. 모든 완전한 plateau의 \(L_k,C_k,R_k\)를 계산하는 것이 가능한가?
6. 마지막 plateau의 censoring 문제를 어떻게 처리해야 하는가?
7. \(R_k\)의 분모를 정확히 어떤 소수 집합으로 정의해야 하는가?
8. 기존 prime-gap 통계 연구와 중복되는 부분은 무엇인가?
9. 이 분석에서 독창적인 연구 질문으로 볼 만한 부분은 무엇인가?
10. 추가 계산량 대비 연구 가치가 충분한가?

**위 질문에 대한 타당성 검증이 끝난 뒤에만 실제 데이터 추출 및 계산을 시작한다.**

---

# 36. 최종 판단의 기준

본 실험의 목적은 단순히 새로운 숫자 몇 개를 만드는 것이 아니다.

최종 판단은 다음 두 축으로 한다.

### 계산적 가치

- 기존 exhaustive 계산에서 거의 추가 비용 없이 얻을 수 있는가?
- 또는 재계산 비용이 감당 가능한가?
- 결과가 재현 가능한가?

### 연구적 가치

- 단순 count를 넘어 normalized recurrence라는 의미가 있는가?
- maximal-gap record의 plateau 특성에 대한 새로운 통계적 정보를 제공하는가?
- 기존 prime-gap distribution 연구와 차별성이 있는가?

두 조건 모두 긍정적일 경우:

\[
\boxed{
\text{Maximal-gap Plateau / Recurrence Analysis}
}
\]

를 독립적인 부가 실험으로 진행한다.

단순 recurrence count만으로 독창성을 주장하지 않고, **plateau length + exact recurrence + normalized recurrence를 함께 분석하는 통계적 프레임워크**를 기본 분석 단위로 한다.