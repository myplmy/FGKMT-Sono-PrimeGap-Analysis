# 01 — Certified Finite-Range Prime-Gap Certificate Compression

## 연구 지위

**후보 A: 가장 강한 후보.**

현재 문헌 조사만으로 이 아이디어가 독창적이라고 확정할 수는 없다. 다만 단순한 wheel sieve나 segmented sieve가 아니라, **이미 수행된 대규모 탐색 전체를 더 작은 독립 검증용 certificate로 압축하고, 그 certificate만으로 finite-range prime-gap absence를 검증**하는 문제로 정식화하면 연구 기여 가능성이 가장 높다.

중요한 선행연구가 이미 존재한다. Oliveira e Silva–Herzog–Pardi는 `Mathematics of Computation`에서 $4\times10^{18}$까지 Goldbach와 prime gaps를 계산했고, `primesieve` 등은 segmented sieve + wheel factorization을 실제 계산의 표준으로 사용한다. 따라서 **"더 빠른 sieve" 자체는 이 후보의 novelty가 아니다.**

---

## 1. 목표 명제

고정된 $G$와 유한 범위 $[A,B]$에 대해

$$
\forall p_n<p_{n+1}\in[A,B],\qquad p_{n+1}-p_n<G.
$$

특히 $G=1856$이면

$$
\boxed{\max g([A,B])\le1854}
$$

를 증명한다.

직접 모든 소수를 생성하는 대신, 다음 형태의 finite certificate $\mathcal C$를 목표로 한다.

$$
\boxed{\operatorname{Verify}(\mathcal C,A,B,G)=\text{TRUE}}
$$

이면 위 명제가 논리적으로 따라오도록 한다.

---

## 2. 핵심 수학적 환원

소수 $p$에 대해

$$
p\text{가 }G\text{-gap의 왼쪽 endpoint}
$$
이면

$$
\pi(p+G-1)-\pi(p)=0.
$$

따라서 다음 명제가 정확히 동치이다.

> $G$ 이상의 prime gap이 존재하지 않는다.
>
> $\Longleftrightarrow$
>
> 모든 $p\in[A,B-G]$에 대해
> $$
> p\text{ composite}
> \quad\text{or}\quad
> \exists q\in(p,p+G-1]\text{ prime}.
> $$

따라서 certificate는 각 candidate start $p$를 두 가지 방식 중 하나로 제거하면 된다.

### Type-I rejection

$$
\boxed{p\text{ composite}.}
$$

### Type-II rejection

$$
\boxed{\exists q\in(p,p+G-1]\text{ with }q\text{ prime}.}
$$

이것이 certificate의 논리적 원자 단위다.

---

## 3. 제안하는 certificate 구조

다음 4층 구조를 연구한다.

$$
\boxed{\text{State partition}\to\text{rejection witness}\to\text{coverage proof}\to\text{hash/check certificate}}
$$

### Layer 1 — State partition

작은 primorial

$$
P_z=\prod_{q\le z}q
$$

를 정하고 candidate start를

$$
\sigma_z(p)=p\bmod P_z
$$

에 따라 묶는다.

동일 state에서는 wheel survivor pattern이 translation-equivalent이다.

### Layer 2 — Rejection witness

각 state class에서 다음 중 하나를 저장한다.

- composite witness rule
- 적어도 하나의 prime witness를 찾는 위치 rule
- 또는 더 강한 exact rejection certificate

### Layer 3 — Coverage proof

모든 candidate start가 정확히 하나 이상의 certificate class에 배정됨을 증명한다.

$$
\boxed{\text{Coverage}=100\%}
$$

### Layer 4 — Independent verification

원래 탐색 결과 전체를 재실행하지 않고도 certificate만 읽어 다음을 검증할 수 있게 한다.

$$
\boxed{
\text{certificate validity}\Rightarrow\text{no gap}\ge G
}
$$

---

## 4. 가장 중요한 가정

### A1. 유한범위

$[A,B]$는 유한하다.

### A2. deterministic primality/compositeness

최종 증명의 primitive operation은 probabilistic-only test가 아니라 deterministic proof이어야 한다.

$10^{20}$ 부근에서는 이미 작은 base의 deterministic Miller–Rabin이 실용적일 수 있지만, 논문에서는 사용한 범위와 theorem을 정확히 고정해야 한다. 더 일반적으로는 ECPP 계열 certificate도 사용할 수 있다.

### A3. state equivalence

$$
 p_1\equiv p_2\pmod{P_z}
$$
이면 wheel survivor geometry를 재사용할 수 있다.

이것은 새로운 가정이 아니라 기본적인 합동성 정리다.

### A4. complete coverage

실제 $G$-gap이 존재한다면 그 왼쪽 endpoint가 certificate가 검사하는 candidate universe에 반드시 들어간다.

이 가정은 **가장 중요한 증명 대상**이며 가정으로 남겨서는 안 된다.

---

## 5. 이미 증명 가능한 기본 정리

### 정리 A — Wheel translation

$$
S_1\equiv S_2\pmod{P_z}
$$
이면 모든 $t$에 대해

$$
\gcd(S_1+t,P_z)=1
\iff
\gcd(S_2+t,P_z)=1.
$$

따라서 상대적인 survivor pattern은 동일하다.

#### 증명

$S_2=S_1+kP_z$라 하면

$$
S_2+t=S_1+t+kP_z,
$$

따라서 gcd가 $P_z$와 취하는 값은 동일하다.

QED.

---

## 6. 이미 존재하는 선행연구와의 경계

다음은 novelty로 주장하면 안 된다.

1. wheel factorization 자체
2. segmented sieve 자체
3. 작은 소수 residue state 자체
4. Jacobsthal-type maximal wheel gap 자체
5. prime-gap exhaustive computation 자체

`primesieve`는 segmented sieve와 wheel factorization을 명시적으로 사용한다. Oliveira e Silva–Herzog–Pardi는 $4\times10^{18}$까지의 prime-gap computation을 포함한 대규모 검증을 수행했다.

따라서 A의 novelty는 반드시 **certificate compression과 독립적 검증 복잡도**에서 발생해야 한다.

---

## 7. 학술지 수준으로 올리기 위한 핵심 조건

### 조건 A — Certificate-size theorem

단순 구현 성능이 아니라 다음 형태의 정리가 필요하다.

$$
|\mathcal C|\le F(A,B,G,z)
$$

그리고 baseline exhaustive enumeration이 갖는 정보량보다 asymptotically 또는 practically 의미 있게 작아야 한다.

가장 강한 목표는

$$
|\mathcal C|=o(N_{\rm candidates}).
$$

이다.

### 조건 B — Verification theorem

certificate 검증 비용이

$$
T_{verify}(\mathcal C)
$$
로 주어지고,

$$
T_{verify}\ll T_{enumerate}
$$

임을 이론 또는 실험으로 입증해야 한다.

### 조건 C — Independent reproducibility

제3자가 원래 생성 프로그램을 신뢰하지 않고도 certificate를 검증할 수 있어야 한다.

권장 방식:

- canonical binary/JSON certificate schema
- versioned generator
- SHA-256 artifact hash
- deterministic verifier
- independent implementation

### 조건 D — Completeness

누락이 한 개라도 있으면 결과는 폐기된다.

---

## 8. 검증 실험

$10^{20}\le x\le10^{21}$에서 최소한 다음 baseline을 둔다.

### Baseline

segmented sieve / primesieve 계열 exact scan.

### Experimental

certificate-compressed algorithm.

측정값:

$$
N_{raw},\quad N_{state},\quad N_{witness},\quad |\mathcal C|,
$$

그리고

$$
T_{generation},\quad T_{verification},\quad T_{baseline}.
$$

핵심은 wall-clock 하나가 아니라

$$
\boxed{\text{certificate bytes per verified integer}}
$$

또는

$$
\boxed{\text{verification operations per candidate}}
$$

를 제시하는 것이다.

---

## 9. 이론 철폐 기준선 — 언제 실패로 판정할 것인가

다음 중 하나라도 발생하면 A의 “학술적 독창성” 주장은 폐기하거나 연구목표를 수정한다.

### Kill criterion A1

최종 certificate가 baseline exact scan보다 본질적으로 작지 않다.

예:

$$
|\mathcal C|\ge0.5N_{raw}
$$

수준이면 압축이라는 논거가 약하다.

### Kill criterion A2

certificate 검증 자체가 baseline보다 비싸다.

$$
T_{verify}\ge T_{baseline}.
$$

### Kill criterion A3

coverage proof를 위해 결국 모든 candidate를 exact test해야 한다.

그러면 compression이 논리적으로 존재해도 실제 증명 비용은 줄지 않는다.

### Kill criterion A4

문헌 조사에서 동일한 certificate abstraction과 동일한 complexity result가 발견된다.

이 경우 novelty claim은 즉시 철회한다.

---

## 10. 성공 기준

가장 강한 성공 결과는 다음이다.

$$
\boxed{
\text{100\% coverage}
+\text{100\% deterministic rejection}
+|\mathcal C|\ll N_{raw}
+T_{verify}\ll T_{baseline}
}
$$

그리고 이 결과를 최소 2개의 독립 구현으로 재현한다.

---

## 11. 실제 논문으로 만들기 위한 최소 추가 결과

1. certificate의 formal definition
2. completeness theorem
3. certificate-size bound
4. verifier-correctness theorem
5. baseline과 독립적인 benchmark
6. independent implementation
7. machine-checkable artifact
8. 기존 prime-gap certification 방법과의 정량적 비교

---

## 12. 현재 결론

이 후보는 세 후보 중 가장 강하다.

그러나 현재는

$$
\boxed{\text{“유망한 novelty candidate”}
\neq
\text{“이미 새로운 정리”}}
$$

이다.

**논문의 중심 정리는 wheel이나 G–B–D가 아니라, finite prime-gap absence를 어떤 최소 정보량의 deterministic certificate로 압축할 수 있는가가 되어야 한다.**

### 주요 참고문헌

- Oliveira e Silva, Herzog, Pardi, *Empirical verification of the even Goldbach conjecture and computation of prime gaps up to $4\cdot10^{18}$*, Mathematics of Computation 83 (2014), 2033–2060. DOI: 10.1090/S0025-5718-2013-02787-1.
- `primesieve` algorithm documentation: segmented sieve + wheel factorization.
- Prime-gap verification community documentation on certified endpoints and reproducible computation.
