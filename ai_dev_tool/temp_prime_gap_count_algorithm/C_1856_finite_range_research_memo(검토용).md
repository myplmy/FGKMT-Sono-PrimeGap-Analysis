# 1856 이상 Prime Gap Count 상계 `C` 연구 메모

## 목적

이 문서는 로컬 ChatGPT/Codex가 다음 연구를 이어받아 검토·재계산·개선할 수 있도록 현재까지의 정의, 증명, 계산 결과, 오류 수정 사항, 향후 수론적/알고리즘적 목표를 하나의 명세로 정리한 것이다.

최종 계산 목적은 다음과 같다.

- 기본 검증 범위: `10^20 <= p < 10^21`
- 더 큰 연구 범위: `10^20 <= p < 10^26`
- 현재 검증 목표 gap: `1856`
- 사용자 제공 기록표의 미확인 후보: `1858` at `P26 = 39422251630462640179641871`
- 하드웨어 제약: **Ryzen 7 9700X 1대만 사용**
- 장기 목표: 수론적 pruning을 이용하여 exhaustive prime-gap computation의 CPU 시간을 최대한 줄인다.
- 이상적인 계산 목표: `N_1856 = 0` 또는 더 일반적으로 `N_1856 <= B`를 무조건적으로 인증한다.

> 중요: 이 문서는 `N_1856 = 0` 또는 1856 이상의 gap 부재를 이미 증명했다고 주장하지 않는다. 여기서 증명된 것은 `N_1856`에 대한 **상계(bound)**이며, 그 상계를 더 낮추기 위한 연구 기반이다.

---

# 1. 기본 정의

다음을 정의한다.

\[
N_h(X;A,B)
=
#\{p: A\le p<B,\ p,p+h\text{ 사이에 다른 소수가 없음}\}.
\]

우리가 연구하는 양은

\[
N_{1856}
:=
N_{1856}(10^{21};10^{20},10^{21}).
\]

`N_1856 = 0`이면 해당 범위에서 1856 이상의 consecutive-prime gap이 없다는 뜻이다.

prime gap은 `2`보다 큰 경우 짝수이므로 `gap < 1856`이면 실제 최대 gap은 `<=1854`이다.

따라서 목표 명제는

\[
\boxed{N_{1856}=0}
\]

또는 동치에 가까운 형태로

\[
\boxed{G(10^{20},10^{21})\le1854}
\]

이다.

---

# 2. 왜 `C`를 도입했는가

large-gap tail을 Cramér형 기준으로 정규화하기 위해 다음 형태를 사용한다.

\[
N_{1856}
\le
C\,
\frac{L}{\log X}
\exp\left(-\frac{1856}{\log X}\right),
\]

여기서 기본 범위에 대해

\[
X=10^{21},
\qquad
L=10^{21}-10^{20}=9\times10^{20}.
\]

따라서 기준량을

\[
Q=
\frac{9\times10^{20}}{\log(10^{21})}
\exp\left(-\frac{1856}{\log(10^{21})}\right)
\]

으로 정의한다.

수치적으로

\[
\log(10^{21})=48.35428695287496\ldots
\]

이고

\[
\boxed{Q\approx398.2227929091105}.
\]

따라서 주어진 `N_1856` 상계 `B`에서 대응하는 정규화 상계는

\[
C\le B/Q
\]

이다.

## 왜 C를 낮추는가?

`C`는 그 자체가 prime-gap 증명이 아니다. 목적은 다음과 같다.

\[
C\downarrow
\quad\Longrightarrow\quad
N_{1856}\text{의 rigorous upper bound}\downarrow.
\]

특히 `N_1856 <= 10^9`를 얻으면, 실제 1856-gap 후보를 최대 10억 개 이하로 제한한 뒤 exact verification을 수행하는 연구 설계를 생각할 수 있다.

더 강한 local/uniform theorem이면 exact computation 전에 큰 구간을 통째로 인증할 가능성도 있다.

---

# 3. 최초의 완전 무조건적 상계

서로 다른 consecutive-prime gap `>=1856`은 각각 서로 겹치지 않는 정수 구간을 차지한다.

전체 길이는

\[
L=9\times10^{20}.
\]

따라서

\[
1856N_{1856}\le9\times10^{20},
\]

즉

\[
N_{1856}
\le
\left\lfloor\frac{9\times10^{20}}{1856}\right\rfloor
=484913793103448275862.
\]

따라서

\[
\boxed{N_{1856}\le4.8491379310344828\times10^{17}}.
\]

이는 prime list, RH, Twin Prime Conjecture, Cramér conjecture 등 아무 가정도 필요 없는 완전한 무조건적 증명이다.

이를 `Q`로 나누면

\[
\boxed{C\le1.2176947219947902\times10^{15}}.
\]

따라서 현재 연구에서 사용할 첫 번째 기준값은

\[
\boxed{C_0=1.2176947219947902\times10^{15}}.
\]

---

# 4. 중요: 이전에 제시했던 `C <= 1.143e15`는 폐기

이전에 다음과 같은 논리를 사용한 적이 있다.

- 전체 prime count를 안다.
- 큰 gap이 아닌 gap들의 합이 최소 `3` times their number라고 가정한다.
- 이를 사용해 `N_1856`을 더 낮춘다.

이 논리는 **일반적인 gap sequence에서는 엄밀하지 않다.** 큰 gap이 사이에 들어가면 `2,2`가 연속해서 나타나지 않아도 되므로 전체 gap 합에 대한 단순한 `3M` lower bound를 그대로 적용할 수 없다.

따라서

\[
C\le1.143\times10^{15}
\]

라는 이전 주장은 폐기한다.

이후 문서에서는 이 값을 사용하지 않는다.

---

# 5. 정확한 prime-count 값

기본 범위에서 알려진 정확한 prime-count 값:

\[
\pi(10^{20})
=
2,220,819,602,560,918,840,
\]

\[
\pi(10^{21})
=
21,127,269,486,018,731,928.
\]

따라서 범위 내부의 prime 수는

\[
P=
18,906,449,883,457,813,088.
\]

내부 consecutive-prime gap 수는

\[
M=P-1
=18,906,449,883,457,813,087.
\]

이 정확한 `pi` 값은 OEIS A006880 같은 표에서도 확인할 수 있다.

참고: https://oeis.org/A006880

이 값은 전체 prime list를 저장해야 한다는 뜻이 아니다. `pi(x)` 자체를 정확히 계산한 결과만 사용한다.

---

# 6. 2310 residue-state 방법

## 6.1 핵심 무조건적 사실

\[
2310=2\cdot3\cdot5\cdot7\cdot11.
\]

`p > 11`인 모든 prime은

\[
\gcd(p,2310)=1
\]

이다.

따라서 모든 prime은 다음 480개 residue 중 하나다.

\[
R=\{r\pmod{2310}:\gcd(r,2310)=1\},
\]

\[
|R|=\varphi(2310)=480.
\]

consecutive primes `p_i, p_{i+1}`의 residue를 `r,s`라고 하면 gap `d`는

\[
s\equiv r+d\pmod{2310}
\]

을 만족해야 한다.

이것은 실제 소수 목록 없이 얻는 완전한 necessary condition이다.

---

# 7. Finite-state transition LP

각 residue transition `r -> s`에 대해 같은 residue class를 갖는 gap 중:

- `0 < d < 1856`인 최소 대표 gap
- `d >= 1856`인 최소 대표 gap

을 사용한다.

실제 gap은 해당 residue transition의 최소 대표값보다 작을 수 없으므로, `lambda >= 0`인 dual inequality에서는 최소 대표값만 확인하면 충분하다.

large-gap indicator를

\[
w(d)=
\begin{cases}
0,&d<1856,\\
1,&d\ge1856
\end{cases}
\]

로 둔다.

다음 certificate를 찾는다.

\[
\lambda\ge0,
\quad\mu,
\quad\phi(r),
\quad t\ge0
\]

such that 모든 허용 transition에 대해

\[
w(d)
\le
\lambda d+
\mu+
\phi(r)-\phi(s)
\]

및

\[
|\phi(r)|\le t.
\]

모든 실제 gap에 대해 이 부등식을 합하면 `phi` 항은 telescope한다.

결과적으로

\[
N_{1856}^{internal}
\le
\lambda\sum_i d_i
+
\mu M
+
2t.
\]

기본 범위에서

\[
\sum_i d_i<10^{21}-10^{20}=9\times10^{20}
\]

을 사용할 수 있다.

오른쪽 경계를 넘어가는 gap 시작점 하나가 추가될 수 있으므로 최종 target count에는 보수적으로 `+1`을 넣는다.

---

# 8. 2310-state certificate의 실제 결과

상태 수:

\[
480.
\]

transition constraint 수:

\[
415,223.
\]

부동소수점 LP 최적값은

\[
0.0232281294285584181
\]

이었다.

그러나 이것만으로는 증명이 아니다.

따라서 denominator

\[
D=10^{15}
\]

의 유리수 certificate로 변환하고, 모든 transition을 **정수 산술**로 다시 검사했다.

독립 verifier의 실제 실행 결과:

```text
PASS
states: 480
edge constraints: 415223
minimum integer slack: 0
internal large-gap bound: 439161464927854178
total large-gap bound: 439161464927854179
```

따라서 현재 certificate는

\[
\boxed{
N_{1856}\le439,161,464,927,854,179
}
\]

를 제공합니다.

이를 `Q`로 나누면

\[
\boxed{
C\le1.102803437542279\times10^{15}
}
\]

이다.

즉 초기 packing bound 대비 약 9.44% 개선이다.

---

# 9. 이 bound는 무엇을 증명한 것인가?

이 결과는

\[
N_{1856}=0
\]

을 증명한 것이 아니다.

또한 `1856-gap이 최대 10^9개`라는 것도 아니다.

현재 증명된 것은 단지

\[
\boxed{
N_{1856}\le4.39161464927854179\times10^{17}
}
\]

및 이에 대응하는

\[
\boxed{
C\le1.102803437542279\times10^{15}
}
\]

이다.

따라서 이것은 **upper-bound certificate**다.

---

# 10. 왜 이 방법이 중요한가?

기존의 trivial bound는 gap의 길이만 이용한다.

새 방법은 여기에 추가로

\[
2,3,5,7,11
\]

에 대한 **모든 residue-class restriction을 동시에 사용**한다.

즉 단순히 “gap은 1856 이상이므로 1856으로 나눈다”가 아니라

\[
\text{prime residue state}
\rightarrow
\text{next prime residue state}
\rightarrow
\text{gap size}
\]

라는 finite-state structure를 사용한다.

이것은 실제 prime list를 생성하지 않고도 계산 가능한 수론적 pruning이다.

---

# 11. C를 더 낮추기 위한 다음 단계: modulus 확대

현재 modulus:

\[
2310=2\cdot3\cdot5\cdot7\cdot11.
\]

다음은

\[
30030=2310\cdot13,
\]

그 다음

\[
510510=30030\cdot17,
\]

그 다음

\[
9699690=510510\cdot19.
\]

상태 수:

\[
\varphi(2310)=480,
\]

\[
\varphi(30030)=5760,
\]

\[
\varphi(510510)=92160,
\]

\[
\varphi(9699690)=1658880.
\]

상태 수가 빠르게 증가하므로 dense LP 대신 sparse/dynamic/dual-only formulation을 연구해야 한다.

---

# 12. 30030-state에서 검토해야 할 것

다음 실험의 목표:

\[
M=30030.
\]

수행할 것:

1. 5760 residue state 생성.
2. 각 ordered residue pair에 대한 최소 small-gap / large-gap representative 생성.
3. transition inequality를 sparse matrix로 표현.
4. floating LP 또는 다른 dual optimization으로 candidate certificate 탐색.
5. certificate를 유리수로 rationalize.
6. 모든 transition을 exact integer arithmetic으로 검증.
7. `lambda*SPAN + mu*M_GAPS + 2t`를 exact rational로 계산.
8. `C_30030`을 산출.
9. `C_2310`과 비교.

**중요:** 새로운 modulus에서 C가 반드시 더 좋아진다고 가정하지 않는다. 실제 exact certificate를 얻은 경우에만 개선으로 기록한다.

---

# 13. certificate 검증을 위한 독립성 원칙

부동소수점 LP solver는 **증명자가 아니라 certificate 탐색기**로만 사용한다.

최종 proof는 다음 형태여야 한다.

```text
rational certificate
      |
      v
integer arithmetic verifier
      |
      +-- every transition inequality PASS
      +-- |phi_r| <= t PASS
      +-- exact rational bound PASS
      |
      v
rigorous C upper bound
```

따라서 solver가 사라져도 verifier만으로 결과를 검증할 수 있어야 한다.

현재 2310 verifier:

- state count: 480
- constraints: 415,223
- integer arithmetic
- no floating-point optimization

으로 `PASS`했다.

파일:

- `C_2310_certificate.py`: certificate 탐색 + exact verification
- `verify_C2310.py`: 독립 exact verifier
- `C2310_certificate.txt`: rational certificate

---

# 14. 현재 C의 상태 요약

| 단계 | 상태 | `N_1856` upper bound | C upper bound |
|---|---|---:|---:|
| 단순 packing | 완전 무조건적 증명 | `4.8491379310344828e17` | `1.2176947219947902e15` |
| 이전 `1.143e15` 논리 | **폐기** | — | — |
| mod 2310 finite-state dual certificate | **exact integer verifier PASS** | `4.39161464927854179e17` | **`1.102803437542279e15`** |
| 목표 | 연구 목표 | `<1e9` | `<2.51e6` 수준의 C가 필요 |

---

# 15. 왜 `C <= 1e14`가 중요한가?

현재

\[
C\approx1.103\times10^{15}.
\]

목표 `1e14`까지는 약

\[
11.03\times
\]

더 줄여야 한다.

`C <= 1e14`이면

\[
N_{1856}
\lesssim
3.9822\times10^{16}
\]

정도로 정규화된 upper bound를 얻는다.

아직 `10^9`와는 큰 차이가 있지만, 계산량 감소용 수론적 certificate의 효과를 단계적으로 정량화할 수 있는 중간 목표다.

---

# 16. 왜 단순 Selberg prime-pair sieve가 해결책이 아닌가?

1856-gap이면 반드시

\[
p,p+1856
\]

가 둘 다 prime이다.

따라서

\[
N_{1856}
\le
\#\{p:p,p+1856\text{ prime}\}.
\]

Selberg/Brun upper-bound sieve는 일반적으로 fixed prime tuple에 대해

\[
\ll \frac{X}{(\log X)^2}
\]

형태를 제공한다.

표준 Selberg sieve의 dimension-`k` upper bound는 `k`개의 linear forms가 모두 prime인 문제에 대해 `X/(log X)^k` 구조를 제공한다. 참고 문헌으로 Iwaniec–Kowalski, Montgomery–Vaughan 계열의 sieve theory가 있다. ([https://mathoverflow.net/questions/222202/upper-bound-for-the-first-hardy-littlewood-conjecture](https://mathoverflow.net/questions/222202/upper-bound-for-the-first-hardy-littlewood-conjecture))

그러나 1856-gap 내부 조건은

\[
p+2,p+4,\ldots,p+1854
\]

가 **composite**라는 것이지 prime이라는 것이 아니다.

따라서 내부 composite 조건을 추가한다고 해서 자동으로

\[
X/(\log X)^3
\]

또는

\[
X/(\log X)^4
\]

가 되는 것이 아니다.

고정 `h=1856`에서 전역적으로 `K>2`를 기대하는 것은 Hardy–Littlewood의 fixed prime-pair 규모와도 맞지 않는다.

---

# 17. 그래도 Buchstab + Type-I/Type-II가 중요한 이유

내부 composite 조건은 factor-size에 따라 분해할 수 있다.

내부 값 `p+d`에 대해

\[
P^+(p+d)\le z
\]

인 경우와

\[
P^+(p+d)>z
\]

인 경우를 구분한다.

첫 번째는 small-factor sieve로 직접 처리할 수 있다.

두 번째는 composite이므로 large factors를 가진 semiprime/multifactor configuration으로 분해된다.

Buchstab identity는 이러한 least-prime-factor 분해에 사용된다. 표준 identity:

\[
S(\mathcal A,\mathcal P,w)
=
S(\mathcal A,\mathcal P,z)
+
\sum_{w\le p<z}S(\mathcal A_p,\mathcal P,p)
\]

가 있다. ([https://personal.science.psu.edu/rcv4/571s25/montgomery-vaughanII.pdf](https://personal.science.psu.edu/rcv4/571s25/montgomery-vaughanII.pdf))

따라서

\[
N_{1856}=N_{Type-I}+N_{Type-II}+\cdots
\]

분해 후 각 항의 explicit upper bound를 찾는 것이 다음 수론적 연구 방향이다.

---

# 18. 선행연구와 연결할 핵심 문헌

## Selberg sieve / upper-bound sieve

Selberg sieve의 dimension-`k` upper bound는 fixed prime tuple upper bounds의 표준 도구다. ([https://mathoverflow.net/questions/222202/upper-bound-for-the-first-hardly-littlewood-conjecture](https://mathoverflow.net/questions/222202/upper-bound-for-the-first-hardly-littlewood-conjecture))

보다 현대적인 정리/정리 형식은 Selberg upper-bound sieve의 `X/(log X)^kappa` 구조를 명시한다. ([https://androma.org/theorems/7176](https://androma.org/theorems/7176))

## Buchstab decomposition

Buchstab identity는 sieve된 집합에서 큰 prime factor를 단계적으로 분리하는 표준 identity이다. Montgomery–Vaughan의 sieve notes에서 statement와 proof를 확인할 수 있다. ([https://personal.science.psu.edu/rcv4/571s25/montgomery-vaughanII.pdf](https://personal.science.psu.edu/rcv4/571s25/montgomery-vaughanII.pdf))

## Large prime gaps

Banks–Ford–Tao의 large prime gaps 연구는 random-residue/sieve model과 실제 prime gaps의 관계를 분석하며, large-gap tail을 연구하는 현재의 중요한 이론적 출발점이다.

DOI:
https://doi.org/10.1007/s00222-023-01199-0

이 연구는 계산에 직접 적용할 unconditional `C <= 1e14` certificate를 제공한다는 뜻이 아니다. 모델/조건부 이론과 unconditional theorem을 구분해야 한다.

## Sieve theory reference

Montgomery–Vaughan, *Multiplicative Number Theory II: Analytic and Modern Techniques*의 sieve chapter가 Buchstab/Selberg sieve의 표준 참고 자료다.

---

# 19. 1854 / 1858 기록을 연구 범위에서 어떻게 취급할 것인가

현재 사용자 제공 표에는 다음이 있다.

- confirmed gap 1854
- unconfirmed gap 1858 at
  `39422251630462640179641871`

1858 위치는 약

\[
3.942225163046264\times10^{25}
\]

이다.

따라서 `10^20 -> 10^21` 문제와는 별개이다.

그러나 장기 연구 목표를

\[
10^{20}\le p<10^{26}
\]

까지 확장하면 이 1858 후보가 중요해진다.

따라서 Codex 구현에서는 두 configuration을 분리하는 것이 좋다.

### Configuration A

```text
RANGE = [10^20, 10^21)
TARGET_GAP = 1856
```

### Configuration B

```text
RANGE = [10^20, 3.9422251630462640179641871e25)
TARGET_GAP = 1856 or 1858
```

`1858` 행이 `unconfirmed`이면 이것을 확정된 prime gap으로 전제해서는 안 된다. 반드시 actual consecutive-prime verification 대상으로 취급한다.

---

# 20. 최종 연구 목적

이 프로젝트에서 `C`를 낮추는 것은 그 자체가 최종 목적이 아니다.

최종 목적은:

\[
10^{20}\sim10^{21}
\]

또는 장기적으로

\[
10^{20}\sim10^{26}
\]

범위의 maximal prime gap을 **Ryzen 7 9700X 1대의 CPU만으로 가능한 시간에 exact/exhaustive하게 검증하는 것**이다.

이를 위해 다음 pipeline을 목표로 한다.

\[
\boxed{
\text{수론적 upper-bound certificate}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{gap-candidate count 감소}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{candidate-specific CPU exhaustive search}
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{1856/1858 gap의 유무 exact verification}
}
\]

즉 C를 낮출수록 반드시 실제 계산량도 낮아지는 구조를 만드는 것이 연구 목표다.

---

# 21. Codex에 요청할 구체적 작업

## A. 현재 certificate 독립 검증

- `C2310_certificate.txt`를 읽는다.
- `verify_C2310.py`를 수정/독립 재작성한다.
- floating-point를 사용하지 않는다.
- 모든 415,223 transition을 exact integer arithmetic으로 검사한다.
- 최종 `N_1856` bound와 `C`를 exact rational로 출력한다.

## B. 2310 모델의 논리 검증

다음을 수학적으로 검토한다.

- residue transition의 최소 representative를 사용해도 되는가?
- `lambda >= 0` 조건이 충분한가?
- `phi` telescope이 정확히 성립하는가?
- boundary crossing gap을 정확히 `+1`만 추가하면 되는가?
- `M_GAPS = pi(B)-pi(A)-1`을 사용하는 과정에 빠진 gap이 없는가?
- `p<=11` 예외가 실제 범위에서 발생할 수 없는가?

## C. 30030-state 확장

\[
M=30030
\]
에 대해

- 5760 states
- sparse transitions
- LP candidate discovery
- rational certificate
- exact verifier

를 구현한다.

## D. 510510-state 확장 가능성

\[
M=510510,
\quad\varphi(M)=92160
\]
에서 dense LP를 피할 방법을 설계한다.

필요하면 dual optimization을 직접 구현하거나 sparse min-cost/shortest-path 형식으로 변환한다.

## E. C 개선 여부 기록

각 modulus에 대해 반드시 다음 표를 만든다.

| modulus | states | constraints | proven N bound | proven C | exact verification time |
|---:|---:|---:|---:|---:|---:|

`C`가 실제로 낮아지지 않으면 개선으로 인정하지 않는다.

## F. Type-I/Type-II sieve 연구

Buchstab decomposition을 적용하여

\[
N_{1856}=N_I+N_{II}+N_{III}+\cdots
\]

로 분해하고 각각에 explicit upper bound를 유도한다.

최종 목표는

\[
C<10^{14}
\]

이며, 그 다음

\[
C<10^{12},
10^{10},
10^8,
\ldots
\]

로 단계적으로 낮춘다.

---

# 22. 특히 주의할 오류

다음은 연구 문서에서 절대 섞어 쓰지 않는다.

### 증명된 정리

실제 prime sequence의 모든 경우에 대해 증명된 결과.

### 계산 certificate

정확한 정수/rational certificate를 독립 verifier가 검증한 결과.

### heuristic

Cramér, Hardy–Littlewood, random-residue model 등.

### conjecture

RH, Twin Prime Conjecture 등.

### numerical observation

실험 계산에서 관찰된 패턴.

이 다섯 가지는 최종 논문에서 명확히 분리해야 한다.

---

# 23. 현재 기준의 핵심 숫자

\[
\boxed{
Q=398.2227929091105\ldots
}
\]

최초 무조건적 bound:

\[
\boxed{
N_{1856}\le4.8491379310344828\times10^{17}
}
\]

따라서

\[
\boxed{
C\le1.2176947219947902\times10^{15}
}
\]

2310-state exact dual certificate:

\[
\boxed{
N_{1856}\le4.39161464927854179\times10^{17}
}
\]

따라서

\[
\boxed{
C\le1.102803437542279\times10^{15}
}
\]

목표:

\[
\boxed{C\le10^{14}}
\]

중장기 목표:

\[
\boxed{C\le2.5\times10^6
\Rightarrow N_{1856}<10^9}
\]

---

# 24. Codex의 최종 연구 질문

다음 질문에 답하도록 한다.

> **Q1. 2310-state dual certificate는 논리적으로 완전한가?**
>
> **Q2. 30030-state에서 exact rational certificate를 구하면 C가 얼마나 낮아지는가?**
>
> **Q3. 510510-state 또는 그 이상의 primorial을 사용하면 C가 단조적으로 개선되는가?**
>
> **Q4. Buchstab Type-I/Type-II decomposition을 1856-gap의 내부 composite 조건에 적용하여 현재 1.10e15보다 실질적으로 강한 unconditional finite-range bound를 만들 수 있는가?**
>
> **Q5. 최종적으로 C를 1e14 이하로 만들 수 있는가?**
>
> **Q6. C가 실제로 1e14, 1e12, 1e10 수준으로 떨어질 경우 Ryzen 7 9700X 1대의 exact verification 시간이 얼마나 감소하는가?**
>
> **Q7. 10^20~10^26으로 확장할 때 같은 certificate 구조를 재사용할 수 있는가?**
>
> **Q8. 사용자 제공 1858 후보가 실제 consecutive-prime gap인지 독립 검증하고, 1856/1858 각각에 대해 동일한 pipeline을 적용할 수 있는가?**

---

# 25. 핵심 결론

현재까지의 가장 중요한 결과는 다음이다.

\[
\boxed{
C\le1.2177\times10^{15}
}
\]

은 단순 packing으로 완전히 무조건적으로 증명된다.

그리고 residue-state finite-state dual certificate를 이용하여

\[
\boxed{
C\le1.102803437542279\times10^{15}
}
\]

까지 실제 exact integer verifier로 확인했다.

이것은 `C`를 낮추는 것이 단순 heuristic이 아니라 **실제 검증 가능한 수론적 certificate 설계 문제**라는 것을 보여준다.

다음 가장 중요한 단계는

\[
2310\rightarrow30030\rightarrow510510
\]

으로 residue-state 정보를 확대하고, 동시에 Buchstab/Type-I/Type-II decomposition으로 내부 composite 조건을 활용하는 것이다.

최종 목표는 `C <= 1e14`를 첫 번째 연구 milestone으로 하고, 이후 `C <= 1e12`, `1e10`, `1e9` 수준으로 단계적으로 낮추어 9700X 단일 CPU에서의 exact maximal-gap verification 시간을 줄이는 것이다.
