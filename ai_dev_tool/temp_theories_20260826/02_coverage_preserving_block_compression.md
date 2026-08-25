# 02 — Coverage-Preserving Block Compression for Fixed Prime-Gap Absence

## 연구 지위

**후보 B: 수학적 novelty 가능성이 두 번째로 높다.**

핵심은 G–B–D라는 이름이 아니라, **큰 block을 사용해 candidate를 압축하면서도 100% coverage를 유지하는 정리**를 만드는 것이다.

단순 block partition이나 wheel/block sieve는 새로운 것이 아니다. 새로워야 하는 내용은 다음 명제다.

> 고정 gap threshold $G$에 대해, block size $B>2$를 사용하면서도 실제 모든 $G$-gap 후보가 적어도 하나의 canonical block certificate에 포함된다는 coverage theorem.

현재 문서에서는 $B=2$에 대해서만 완전한 coverage가 쉽게 증명되며, 일반적인 큰 $B$에 대한 compression-preserving coverage theorem은 아직 없다.

---

## 1. 정확한 문제

고정 $G$에 대해

$$
\mathcal G_G([A,B])
=
\{(p_n,p_{n+1}):p_{n+1}-p_n\ge G\}.
$$

candidate family $\mathcal C(B,D,\ldots)$를 만들고 다음을 증명하려 한다.

$$
\boxed{
\forall g\in\mathcal G_G([A,B]),\quad
\exists!\ c\in\mathcal C
}
$$

또는 중복을 허용하면 적어도

$$
\boxed{
\forall g\in\mathcal G_G([A,B]),\quad
\exists c\in\mathcal C.
}
$$

---

## 2. 먼저 확정되는 정리: $B=2$의 완전 coverage

두 연속 홀수 소수 $p<q$에 대해

$$
q-p=2m.
$$

다음과 같이 정의한다.

$$
S=p-1,
\qquad
B=2,
\qquad
D=m.
$$

block

$$
I_j=[S+2(j-1),S+2j-1]
$$

을 사용하면

$$
I_2\cup\cdots\cup I_D=[p+1,q-1].
$$

연속 소수라는 정의로부터 각 $I_j$ $(j\ge2)$는 empty이다.

따라서 $B=2$는 complete coverage를 갖는다.

---

## 3. 이 정리가 중요한 이유

이 정리는 현재 framework의 가장 큰 논리적 공백을 정확히 드러낸다.

$$
\boxed{B=2\Rightarrow100\%\ coverage}
$$

하지만

$$
B>2
$$

에서는 자동으로 따라오지 않는다.

따라서 연구의 진짜 질문은

$$
\boxed{
\text{“얼마나 큰 }B\text{를 사용하면서도 coverage를 보존할 수 있는가?”}
}
$$

이다.

---

## 4. 기본 가정

### A1. parity

2보다 큰 소수는 홀수이고 prime gap은 짝수이다.

### A2. block partition

각 candidate는 정확한 endpoint convention을 갖는 finite block sequence로 표현된다.

### A3. canonical assignment

동일한 실제 gap이 여러 $(S,B,D)$ 표현을 갖더라도 canonical rule이 하나를 선택한다.

### A4. complete coverage

canonical rule이 모든 실제 $G$-gap을 포함한다.

A4는 가정이 아니라 **최종 논문의 theorem이어야 한다.**

---

## 5. G–B–D parity lower bound

$S$가 짝수이고

$$
I_j=[S+(j-1)B,S+jB-1]
$$

이라고 하자.

$N_1\ge1$ 및

$$
N_2=\cdots=N_D=0
$$

이면 마지막 소수 후보와 다음 소수 후보 사이의 parity lower bound는

$$
\boxed{
\Delta_{\min}^{(2)}(B,D)=
\begin{cases}
(D-1)B+3,&B\text{ odd},D\text{ even},\\
(D-1)B+2,&\text{otherwise.}
\end{cases}}
$$

이다.

이것은 정확하지만 새 prime-gap theorem이라고 주장할 수는 없다.

---

## 6. 진짜 novelty target

### 정리 B1 — Coverage-preserving compression theorem

찾고자 하는 형태는 다음이다.

어떤 $B>2$ 및 canonical mapping $\Phi$가 존재하여

$$
\Phi:\mathcal G_G([A,B])\to\mathcal C_{B,D}
$$

가 정의되고

$$
\boxed{\Phi\text{ is total}.}
$$

그리고 candidate 수가 직접 start enumeration보다 작아야 한다.

$$
|\mathcal C_{B,D}|
\ll
|\mathcal S_G|.
$$

더 강하게

$$
\frac{|\mathcal C_{B,D}|}{|\mathcal S_G|}	o0
$$

같은 asymptotic 또는 finite-range bound를 제시하면 매우 강한 결과가 된다.

---

## 7. 왜 이 부분이 어려운가

큰 $B$를 사용하면 하나의 block이 많은 start 위치를 묶는다.

그러나 실제 gap endpoint가 block boundary와 어떻게 정렬되는지 모르면 일부 gap이 representation에서 빠질 수 있다.

즉

$$
\text{compression}\Rightarrow\text{possible loss of coverage}.
$$

따라서 논문에서 가장 중요한 것은 candidate 감소율보다 먼저 **coverage proof**다.

---

## 8. 제안하는 접근 1 — Sliding phase classes

$S$를 block size $B$에 대한 phase

$$
r=S\bmod B
$$

로 분류한다.

그러면 start positions를

$$
S=r+tB
$$

로 정리할 수 있다.

목표는 각 phase $r$에 대해 모든 $G$-gap이 어떤 bounded family의 $(D,S)$에 대응한다는 것을 보이는 것이다.

---

## 9. 제안하는 접근 2 — Overlapping block certificates

disjoint block만 사용하지 않고

$$
I_j^{(r)}=[S+r+(j-1)B,S+r+jB-1]
$$

처럼 여러 phase를 허용한다.

coverage에는 도움이 되지만 중복이 늘어난다.

따라서 최종 연구결과는

$$
\boxed{
\text{minimum number of phases needed for complete coverage}
}
$$

를 구하는 문제로 만들 수 있다.

---

## 10. 제안하는 접근 3 — Residue-aware phase reduction

$P_z$까지 함께 사용하여

$$
(S\bmod B,\;S\bmod P_z)
$$

를 state로 둔다.

CRT에 의해 결합 residue state로 압축할 수 있다.

단, 이 구조가 실제로 기존 wheel/sieve보다 새로운지는 문헌조사를 더 해야 한다.

---

## 11. 선행연구의 경계

이미 알려진 내용:

- wheel factorization
- segmented sieve
- combined sieve / prime-gap candidate sieving
- residue classes modulo primorials
- Jacobsthal-type maximal unsieved runs

따라서 “block + wheel” 자체는 novelty가 아니다.

`primesieve`는 wheel + segmented sieve를 실제로 구현하며, combined sieve 계열의 prime-gap search도 이미 존재한다.

새로워야 하는 것은

$$
\boxed{
\text{complete coverage theorem + compression bound}
}
$$

이다.

---

## 12. 학술지 수준 조건

### 조건 B1 — 완전한 coverage theorem

모든 실제 gap에 대한 존재 정리가 있어야 한다.

### 조건 B2 — explicit compression bound

예를 들어

$$
N_{candidate}^{new}
\le C(G,z)\frac{B-A}{B}
$$

같은 명시적 bound가 필요하다.

단순 empirical reduction percentage는 충분하지 않다.

### 조건 B3 — optimality 또는 near-optimality

최소한 다음 중 하나가 필요하다.

1. 제안 방식의 asymptotic optimality
2. 특정 class에서 lower bound와 matching
3. 고정 $G$에서 finite-range 최소 phase 수에 대한 최적성

### 조건 B4 — 독립 검증

coverage theorem과 구현 결과가 서로 독립적으로 확인되어야 한다.

---

## 13. 검증 프로토콜

### 단계 1

작은 범위에서 brute-force enumerate한다.

예:

$$
10^6\le x\le10^9.
$$

모든 실제 gap을 직접 얻는다.

### 단계 2

block algorithm이 모든 실제 gap을 회수하는지 확인한다.

$$
N_{miss}=0.
$$

### 단계 3

독립 구현으로 동일 검사를 반복한다.

### 단계 4

$10^{12},10^{15},10^{18}$ 등으로 확장한다.

### 단계 5

마지막으로 $10^{20}$–$10^{21}$을 대상으로 한다.

---

## 14. 이론 철폐 기준선

### Kill criterion B1 — 단 하나의 누락

어떤 실제 gap이 candidate family에서 표현되지 않으면

$$
\boxed{\text{coverage theorem 폐기}.}
$$

이는 1회 누락이면 충분하다.

### Kill criterion B2 — compression이 사라짐

coverage를 위해 phase를 너무 많이 추가하여

$$
N_{candidate}^{new}\approx N_{raw}
$$

가 되면 연구 의미가 약해진다.

### Kill criterion B3 — exact verification cost가 증가

후보 수는 줄었으나 각 candidate당 검증비용이 커져

$$
T_{new}\ge T_{baseline}
$$

이면 알고리즘 논문으로서의 주장이 약해진다.

### Kill criterion B4 — 기존 문헌과 동형

기존 combined sieve 또는 다른 literature에서 사실상 동일한 coverage/compression theorem을 찾으면 novelty claim을 철회한다.

---

## 15. 성공 기준

가장 좋은 결과는

$$
\boxed{
\text{Total coverage}
+\text{provable compression}
+\text{lower or equal verification cost}
}
$$

이다.

특히 다음 표를 논문에서 제시할 수 있어야 한다.

| 방법 | Coverage | Candidate 수 | Exact work | 검증 비용 |
|---|---:|---:|---:|---:|
| $B=2$ baseline | 100% | 기준 | 기준 | 기준 |
| 제안 $B>2$ | 100% | 감소 | 감소 | 감소/동등 |

---

## 16. 현재 판정

이 후보는 **수학적 theorem을 만들 가능성**이 있다.

하지만 현재 알려진 결과만으로는

$$
B>2\Rightarrow100\%\ coverage
$$

가 증명되지 않았다.

따라서 연구를 시작할 때부터 다음을 명확히 해야 한다.

> $B=2$의 complete coverage는 baseline theorem으로 인정한다.
>
> 논문의 독창적 목표는 $B>2$의 coverage-preserving compression theorem이다.

이 목표를 달성하지 못하면 이 부분은 **기존 exhaustive sieve의 변형**으로 철폐한다.

---

## 주요 참고문헌

- Oliveira e Silva, Herzog, Pardi, *Mathematics of Computation* 83 (2014), 2033–2060.
- `primesieve` Algorithms documentation: segmented sieve, wheel factorization, cache-efficient implementation.
- Pritchard/Sorenson 계열의 wheel factorization 연구.
- Jacobsthal-function literature on maximal runs free of small-prime factors.
