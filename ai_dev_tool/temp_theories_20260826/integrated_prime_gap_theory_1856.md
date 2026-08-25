# 1856 Prime-Gap Absence Certification 통합이론

## Li–π 국소 오차(Q) + G–B–D 블록 인증 + Residue-State + `S = 2^k + 2j`

### 후속 연구의 기준 문서

---

## 0. 문서의 목적과 적용 범위

이 문서는 지금까지 독립적으로 발전시킨 두 연구를 하나의 수학적 framework로 통합한 기준문서다.

첫 번째 연구는

\[
D(x)=\operatorname{li}(x)-\pi(x)
\]

및

\[
Q(X,h)=\inf_{x\ge X}\left[D(x+h)-D(x)\right]
\]

를 통해 **짧은 구간의 소수 개수에 대한 rigorous upper bound**를 만드는 연구다.

두 번째 연구는 고정된 gap 기준값 \(G\)에 대해 block을 나누고 parity 및 작은 소수의 residue 조건을 사용하여 **큰 gap을 만들기 위해 필요한 공백 구조**를 수학적으로 제한하는 연구다.

본 문서에서는 두 연구를 다음 목표에 맞게 통합한다.

> **목표:**
> 
> \[
> [A,B]
> \]
> 범위 안에
> \[
> p_{n+1}-p_n\ge 1856
> \]
> 인 연속 소수쌍이 존재하지 않음을, 누락 없는(complete) 방식으로 증명할 수 있는 수학적·알고리즘적 framework를 구축한다.

1차 알고리즘 개발 범위는

\[
\boxed{10^{20}\le x\le10^{21}}
\]

로 둔다.

장기적인 최종 목표 범위는 현재 연구에서 사용하는 상한 가정에 따라 대략

\[
\boxed{1.014\times10^{20}\le x\le5.85123\times10^{27}}
\]

로 둔다.

단, 마지막 상한 \(5.85123\times10^{27}\)의 출처와 “1856의 first occurrence” 상태는 별도 source verification을 수행해야 하며, 본 문서는 이를 선행사실로 가정하지 않는다.

---

# 1. 최종 연구문제를 정확하게 정의한다

## 1.1 목표 gap

본 연구의 핵심 threshold는

\[
\boxed{G=1856}
\]

이다.

최종적으로 증명하려는 명제는

\[
\boxed{
\nexists n\quad p_{n+1}-p_n\ge1856
}
\]

이며, 범위를 명시하면

\[
\boxed{
\forall p_n,p_{n+1}\in[A,B],\quad p_{n+1}-p_n<1856
}
\]

이다.

2보다 큰 모든 소수는 홀수이므로 prime gap은 짝수다. 따라서

\[
p_{n+1}-p_n<1856
\]

는 실제 가능한 gap의 최대값이

\[
\boxed{1854}
\]

이하라는 것과 동치다.

따라서 최종 부재 명제는 다음과 같이도 쓸 수 있다.

\[
\boxed{g_{\max}([A,B])\le1854.}
\]

---

# 2. 가장 중요한 논리적 구분: 발견과 부재증명

본 연구에서는 다음 두 문제를 반드시 분리한다.

### 발견 문제

어떤 위치에서

\[
p_{n+1}-p_n\ge G
\]

를 한 번 찾으면 된다.

### 부재증명 문제

범위의 **모든 가능한 위치**에 대해

\[
p_{n+1}-p_n<G
\]

임을 보여야 한다.

본 연구의 최종 목표는 두 번째 문제다.

따라서 단순히 “유망한 gap 후보를 찾는” 전략만으로는 충분하지 않다. 반드시

\[
\boxed{\text{100% coverage} + \text{rigorous rejection}}
\]

이 필요하다.

---

# 3. 소수계량함수 \(\pi(x)\)

소수계량함수는

\[
\boxed{
\pi(x)=\#\{p\le x:p\text{ is prime}\}
}
\]

이다.

길이 \(h\)의 short interval \((x,x+h]\) 안의 소수 개수를

\[
\boxed{
N(x,h)=\pi(x+h)-\pi(x)
}
\]

로 정의한다.

이 \(N(x,h)\)가 통합이론의 가장 중요한 공통 변수다.

---

# 4. 로그적분 \(\operatorname{li}(x)\)

로그적분은

\[
\boxed{
\operatorname{li}(x)=\int_2^x\frac{dt}{\log t}
}
\]

로 정의한다.

소수정리에 의해

\[
\pi(x)\sim\operatorname{li}(x)
\]

이지만

\[
\operatorname{li}(x)\neq\pi(x)
\]

이다.

따라서 \(\operatorname{li}\)는 **평균적인 기준선**이지 정확한 prime count가 아니다.

---

# 5. Li–π 차이 \(D(x)\)

다음과 같이 정의한다.

\[
\boxed{
D(x)=\operatorname{li}(x)-\pi(x)
}
\]

- \(D(x)>0\): \(\operatorname{li}(x)\)가 \(\pi(x)\)보다 큼
- \(D(x)<0\): 실제 소수 개수가 \(\operatorname{li}(x)\)보다 큼

하지만 전체적인 \(D(x)\)의 크기만으로는 짧은 구간의 prime count를 직접 정밀하게 제한할 수 없다.

---

# 6. 국소 오차의 핵심 항등식

길이 \(h\)에 대해

\[
\begin{aligned}
D(x+h)-D(x)
&=[\operatorname{li}(x+h)-\operatorname{li}(x)]\\
&\quad-[\pi(x+h)-\pi(x)].
\end{aligned}
\]

따라서

\[
\boxed{
D(x+h)-D(x)
=
\Delta_h\operatorname{li}(x)-N(x,h)
}
\]

where

\[
\boxed{
\Delta_h\operatorname{li}(x)
=
\operatorname{li}(x+h)-\operatorname{li}(x).
}
\]

즉 Li의 local increment와 실제 prime count의 차이가 바로 \(D\)의 local variation이다.

---

# 7. Q의 정의

무한범위에서는

\[
\boxed{
Q(X,h)=
\inf_{x\ge X}
[D(x+h)-D(x)]
}
\]

로 정의한다.

유한범위에서는

\[
\boxed{
Q_{A,B}(h)=
\min_{A\le x\le B}
[D(x+h)-D(x)]
}
\]

로 정의한다.

주의: 실제 값을 계산한 것이 아니라 lower bound만 확보한 경우에는 반드시

\[
Q_{A,B}(h)\ge q
\]

형태로 표현해야 한다.

---

# 8. Q → short-interval prime-count upper bound

\[
Q(X,h)\ge -q
\]

라고 하자.

그러면 모든 해당 \(x\)에 대해

\[
D(x+h)-D(x)>-q.
\]

앞의 항등식으로부터

\[
\Delta_h\operatorname{li}(x)-N(x,h)>-q
\]

이므로

\[
\boxed{
N(x,h)<\Delta_h\operatorname{li}(x)+q.
}
\]

즉

\[
\boxed{
Q\text{의 lower bound}
\Longrightarrow
\text{local prime-count upper bound}
}
\]

이다.

---

# 9. 현재 확보된 Q 기준선

현재 연구 기록에서 사용하는 finite-range 결과는

\[
\boxed{
Q_{20,21}(1856)\ge-280.6166400756
}
\]

이다.

이것은 실제 \(Q_{20,21}(1856)\)의 정확한 값이 아니다.

이는 단지 rigorous lower bound다.

따라서 해당 bound에서 얻는 count upper bound는 대략

\[
N(x,1856)
<
\Delta_{1856}\operatorname{li}(x)+280.6166400756
\]

이다.

---

# 10. 큰 전역 Li–π 오차와 local problem의 차이

RH 조건부 Schoenfeld bound는

\[
\left|\pi(x)-\operatorname{li}(x)\right|
<
\frac{\sqrt{x}\log x}{8\pi}
\]

형태를 갖는다.

하지만 이는 전역 오차다.

\[
D(x+h)-D(x)
\]

이라는 local variation에는 endpoint 오차를 합친 매우 큰 bound가 생길 수 있다.

따라서 본 연구에서는 Schoenfeld를 주된 short-window filter로 사용하지 않는다.

---

# 11. \(D(x)>0\)와 local monotonicity의 구분

\[
D(x)>0
\]

은

\[
D(x+h)-D(x)>0
\]

을 뜻하지 않는다.

따라서

\[
\operatorname{li}(x)>\pi(x)
\]

라는 사실만으로

\[
\Delta_h\operatorname{li}(x)>N(x,h)
\]

를 주장해서는 안 된다.

short interval 연구에서는 반드시 \(N(x,h)\) 자체 또는 \(D(x+h)-D(x)\)를 직접 다뤄야 한다.

---

# 12. residue / wheel 상한

작은 소수들을 \(q\le z\)까지 이용하여

\[
P_z=\prod_{q\le z}q
\]

를 정의한다.

\(p>z\)인 소수는

\[
\gcd(p,P_z)=1
\]

을 만족한다.

따라서 어떤 정수구간 \(I\)에 대해

\[
C_z(I)=
\{n\in I:\gcd(n,P_z)=1\}
\]

라고 하면

\[
\boxed{
\#\{p\in I:p\text{ prime}\}
\le
|C_z(I)|.
}
\]

이는 deterministic upper bound다.

단,

\[
\gcd(n,P_z)=1
\]

은 prime의 충분조건이 아니다.

즉 survivor는 prime candidate일 뿐이다.

---

# 13. 현재의 \(P_{23}\) 기준선

\[
P_{23}=2\cdot3\cdot5\cdot7\cdot11\cdot13\cdot17\cdot19\cdot23.
\]

현재 연구에서 사용하는 1856-window survivor 계산은

\[
\boxed{
\max_x |C_{23}((x,x+1856])|=319
}
\]

이라는 기준선을 제공한다.

따라서

\[
\boxed{
N(x,1856)\le319.
}
\]

이는 실제 prime count가 319라는 뜻이 아니라 가능한 prime 위치가 최대 319개라는 뜻이다.

---

# 14. G–B–D block 구조

고정된 \(G\), block size \(B\), 마지막 block 번호 \(D\), 시작점 \(S\)를 사용한다.

block \(j\)를

\[
\boxed{
I_j=[S+(j-1)B,\;S+jB-1]
}
\]

로 정의한다.

block의 정확한 prime count는

\[
\boxed{
N_j=
\pi(S+jB-1)-\pi(S+(j-1)B-1).
}
\]

이 정의는 이후 모든 계산에서 고정한다.

---

# 15. endpoint convention

\[
\pi(x+h)-\pi(x)
\]

는 구간 \((x,x+h]\)를 센다.

반면 \(I_j\)는 정수 폐구간

\[
[S+(j-1)B,S+jB-1]
\]

이다.

따라서 block count를 사용할 때는 반드시

\[
N_j=
\pi(S+jB-1)-\pi(S+(j-1)B-1)
\]

형식을 사용하여 1칸 off-by-one을 방지한다.

---

# 16. 첫 block과 이후 block의 의미

gap candidate를 구성하기 위한 충분조건의 하나로

\[
N_1\ge1
\]

이고

\[
N_2=\cdots=N_D=0
\]

이면 첫 block의 마지막 소수와 그 뒤의 다음 소수 사이에 긴 공백이 형성된다.

첫 block의 마지막 소수를 \(p_n\)으로 선택해야 두 소수가 실제로 연속한 소수쌍이 된다.

---

# 17. parity 정보

큰 범위에서 \(p>2\)인 소수는 홀수다.

따라서 두 연속 소수의 gap은 짝수다.

\[
\boxed{
p_{n+1}-p_n\equiv0\pmod2.
}
\]

---

# 18. 기존 \(S=2^k\)의 해석 수정

초기 연구에서는

\[
S=2^k
\]

를 시작점으로 정의했다.

하지만 parity 기반 G–B–D 공식에 필요한 핵심 정보는 실제로

\[
\boxed{S\equiv0\pmod2}
\]

이다.

따라서 parity만 사용하는 수준에서는 모든 짝수 시작점

\[
S=2m
\]

이 허용된다.

\(2^k\)는 따라서 “유일하게 허용되는 시작점”이 아니라 **canonical anchor**로 해석한다.

---

# 19. 확장된 시작점 family

전체 범위를 커버하기 위해 다음을 정의한다.

\[
\boxed{
S_{k,j}=2^k+2j,
\qquad j\in\mathbb Z.
}
\]

\(j\ge0\)만 사용하면 \(2^k\)에서 오른쪽으로 이동할 수 있고, 필요하면 음의 \(j\)도 허용할 수 있다.

모든 \(S_{k,j}\)는 짝수다.

따라서

\[
S_{k,j}\equiv0\pmod2
\]

이고 parity 기반 G–B–D 공식은 그대로 적용된다.

---

# 20. \(S=2^k+2j\)에서 유지되는 정보와 변화하는 정보

## 유지되는 것

parity:

\[
S_{k,j}\equiv0\pmod2.
\]

따라서 기존 parity certificate는 그대로 유지된다.

## 변화하는 것

홀수 소수 \(q\)에 대해

\[
S_{k,j}\bmod q
=
(2^k+2j)\bmod q.
\]

따라서 \(j\)가 변하면 higher-residue alignment도 변한다.

하지만 이 변화는 주기적이다.

---

# 21. \(S=2^k+2j\)의 residue state

홀수 소수 \(q\)에 대해

\[
S_{k,j}\equiv2^k+2j\pmod q.
\]

따라서 state는

\[
\boxed{
\operatorname{State}_q(k,j)=2^k+2j\pmod q.
}
\]

이를 \(q\le z\)에 대해 모두 모으면

\[
\boxed{
\operatorname{State}_z(k,j)
=
\left(2^k+2j\bmod q\right)_{q\le z,\ q>2}.
}
\]

이는 작은 소수에 대한 necessary residue constraints의 전체 상태다.

---

# 22. state periodicity

홀수 소수 \(q\)는 \(2\)와 서로소이므로 \(j\)에 대한 state는 주기적으로 반복된다.

특히

\[
S_{k,j+q}
=
2^k+2j+2q
\equiv
2^k+2j
\pmod q.
\]

따라서

\[
\boxed{
\operatorname{State}_q(k,j+q)
=
\operatorname{State}_q(k,j).
}
\]

여러 소수를 동시에 사용하면 CRT를 통해 전체 state는 적절한 odd wheel modulus에 대해 주기성을 가진다.

---

# 23. state와 primality pattern의 차이

다음 두 명제를 구분한다.

\[
\operatorname{State}_z(k,j_1)=\operatorname{State}_z(k,j_2)
\]

는 같은 small-prime residue restriction을 가진다는 뜻이다.

그러나

\[
\text{prime/composite pattern is identical}
\]

을 뜻하지 않는다.

즉

\[
\boxed{
\text{same residue state}\neq\text{same primality pattern}.
}
\]

따라서 state compression은 necessary-condition pattern의 재사용을 의미할 뿐, 한 위치에서 증명한 exact prime pattern을 다른 위치로 복사하는 것은 아니다.

---

# 24. \(k\bmod\operatorname{ord}_q(2)\)

anchor \(2^k\) 자체의 residue를 계산할 때

\[
2^k\bmod q
\]

는 \(2\)의 multiplicative order

\[
\operatorname{ord}_q(2)
\]

을 이용하여 주기적으로 반복된다.

따라서

\[
\boxed{
k\bmod\operatorname{ord}_q(2)
}
\]

는 anchor residue state를 압축하는 중요한 상태변수다.

그러나 \(S=2^k+2j\)에서는 이 정보만으로 충분하지 않고 \(j\)의 residue state도 함께 필요하다.

---

# 25. parity-only G–B–D gap lower bound

첫 block의 마지막 위치가

\[
S+B-1
\]

이고 \(S\)가 짝수라고 하자.

### \(B\) 홀수

\[
S+B-1
\]

은 짝수이므로 마지막 소수 후보는

\[
S+B-2.
\]

### \(B\) 짝수

\[
S+B-1
\]

은 홀수이므로 마지막 소수 후보는

\[
S+B-1.
\]

마지막 empty block의 끝은

\[
S+DB-1.
\]

따라서 다음 소수의 최소 후보는 parity에 따라

\[
S+DB
\]

또는

\[
S+DB+1
\]

이다.

결과적으로

\[
\boxed{
\Delta_{\min}^{(2)}(B,D)=
\begin{cases}
(D-1)B+3,&B\text{ odd},\ D\text{ even},\\[4pt]
(D-1)B+2,&\text{otherwise.}
\end{cases}
}
\]

---

# 26. gap 발견 certificate

다음 조건이 성립한다고 하자.

\[
N_1\ge1,
\qquad
N_2=\cdots=N_D=0.
\]

그리고

\[
\boxed{
\Delta_{\min}^{(2)}(B,D)>G
}
\]

이면 해당 configuration은

\[
\boxed{
p_{n+1}-p_n>G
}
\]

를 보장한다.

이것은 **large-gap 발견 certificate**다.

---

# 27. 최종 목표에서는 발견 certificate와 부재 certificate를 분리한다

발견 방향:

\[
\boxed{
L_{\rm gap}>G
\Rightarrow
\text{gap } >G\text{ confirmed.}
}
\]

부재 방향:

\[
\boxed{
U_{\rm gap}<G
\Rightarrow
\text{gap }\ge G\text{ impossible.}
}
\]

본 연구의 최종 목표는 두 번째 방향이다.

따라서 현재의 \(\Delta_{\min}>G\) 공식만으로는 최종 부재증명을 완성할 수 없다.

---

# 28. gap-candidate coverage

범위 \([A,B]\)에서 목표 gap \(G\) 이상의 gap이 생길 수 있는 모든 시작 위치를

\[
\boxed{
\mathcal C_G([A,B])
}
\]

라는 candidate family로 생각한다.

부재증명을 위해서는

\[
\boxed{
\text{Coverage}(\mathcal C_G,[A,B])=100\%
}
\]

가 필요하다.

즉 실제 gap이 존재한다면 반드시 어떤 candidate family member로 표현되어야 한다.

이것이 최종 증명의 **coverage theorem**이다.

---

# 29. Coverage와 reduction의 구분

### Coverage

모든 가능한 gap candidate를 빠짐없이 포함하는가?

\[
\boxed{100\%\text{ coverage required}}
\]

### Reduction

그 후보들을 얼마나 많이 제거하거나 압축하는가?

\[
\boxed{\text{reduction should be maximized subject to 100% coverage}.}
\]

높은 reduction이 있어도 coverage가 100%가 아니면 부재증명에는 사용할 수 없다.

---

# 30. Block prime count의 통합 표현

각 block에 대해

\[
N_j=
\pi(S+jB-1)-\pi(S+(j-1)B-1).
\]

각 block의 상태를 다음 세 가지로 분류한다.

### 상태 A — Certainly Empty

rigorous하게

\[
N_j=0
\]

을 증명할 수 있음.

### 상태 B — Certainly Nonempty

rigorous하게

\[
N_j\ge1
\]

을 증명할 수 있음.

### 상태 C — Undecided

현재의 cheap certificate로는 결정할 수 없음.

최종 exact verification은 상태 C에만 적용한다.

\[
\boxed{
\text{empty / nonempty / undecided}
}
\]

3-state 분류는 통합 알고리즘의 핵심이다.

---

# 31. Q를 block level에서 적용

block \(I_j	=[a_j,a_j+B-1]\)에서

\[
x=a_j-1
\]

로 놓으면

\[
N_j=\pi(x+B)-\pi(x).
\]

Q lower bound가

\[
Q\ge-q
\]

이면

\[
\boxed{
N_j
<
\Delta_B\operatorname{li}(a_j-1)+q.
}
\]

따라서 정수성을 사용한 upper bound를

\[
\boxed{
U_{Q,j}
=
\left\lceil
\Delta_B\operatorname{li}(a_j-1)+q
\right\rceil-1
}
\]

같은 형태로 정의할 수 있다.

---

# 32. residue upper bound와 결합

\[
U_{\rm res,j}=|C_z(I_j)|
\]

라 하면

\[
N_j\le U_{\rm res,j}.
\]

따라서

\[
\boxed{
U_j
=
\min(U_{Q,j},U_{\rm res,j},U_{\rm sieve,j},\ldots).
}
\]

각 upper bound가 rigorous하다면 최소값도 rigorous하다.

---

# 33. Empty-block criterion

prime count는 정수이고 항상

\[
N_j\ge0
\]

이다.

따라서

\[
\boxed{
U_j<1\Rightarrow N_j=0.
}
\]

이것은 통합이론에서 가장 강력하고 간단한 empty certificate다.

그러나 현재의 \(Q_{20,21}(1856)\) 기준선만으로는 \(1856\)-window의 \(N_j<1\)을 얻기 어렵다.

---

# 34. Q의 한계

현재

\[
Q_{20,21}(1856)\ge-280.6166
\]

이면 \(x\sim10^{20}\)에서

\[
\Delta_{1856}\operatorname{li}(x)\approx40.3
\]

이므로 약 320 수준의 upper bound만 나온다.

따라서 현재 Q는

\[
N=0
\]

을 직접 인증하는 강력한 empty-block filter가 아니다.

Q의 현재 역할은

\[
\boxed{
\text{upper-count / auxiliary analytic filter}
}
\]

이다.

---

# 35. Li의 계산 역할

\(\operatorname{li}(x)\) 자체는 exact prime count가 아니다.

또한 \(h\ll x\)인 경우

\[
\Delta_h\operatorname{li}(x)
=
\int_x^{x+h}\frac{dt}{\log t}
\]

이고

\[
\boxed{
\Delta_h\operatorname{li}(x)
\approx
\frac{h}{\log x}
}
\]

가 매우 좋은 first-order approximation이다.

따라서 알고리즘에서는 full \(\operatorname{li}(x)\)를 매번 계산하기보다 short-interval expansion을 사용할 수 있다.

단, 근사를 rigorous filter로 사용할 경우에는 오차항을 명시적으로 bound해야 한다.

---

# 36. Li와 heuristic probability의 구분

\[
\frac{h}{\log x}
\]

같은 값은 prime density의 평균적인 추정치다.

이는 candidate priority 또는 expected cost에는 유용하지만, 그 자체로

\[
N(x,h)=0
\]

을 증명하지 않는다.

Rigorous count upper bound로 사용하려면

\[
\Delta_h\operatorname{li}(x)-Q
\]

또는 그에 준하는 explicit error control이 필요하다.

---

# 37. 추가 residue-state endpoint certificate

첫 block에서 마지막 소수가 될 수 있는 가장 큰 residue-compatible 위치를

\[
\boxed{A_z(S,B)}
\]

라고 정의한다.

마지막 empty block 이후 다음 소수가 될 수 있는 가장 작은 residue-compatible 위치를

\[
\boxed{C_z(S,D,B)}
\]

라고 정의한다.

그러면 empty-block 조건이 정확히 성립할 경우

\[
\boxed{
p_n\le A_z(S,B),
\qquad
p_{n+1}\ge C_z(S,D,B).
}
\]

따라서

\[
\boxed{
p_{n+1}-p_n
\ge
C_z(S,D,B)-A_z(S,B).
}
\]

---

# 38. residue-state gap certificate

\[
\boxed{
C_z(S,D,B)-A_z(S,B)>G
}
\]

이면 해당 candidate configuration에서

\[
\boxed{
p_{n+1}-p_n>G
}
\]

가 확정된다.

parity-only formula는 사실상 \(z=2\)인 특수한 경우다.

---

# 39. `S = 2^k + 2j`와 endpoint state

이제

\[
S=S_{k,j}=2^k+2j
\]

를 넣으면

\[
A_z=A_z(k,j,B),
\qquad
C_z=C_z(k,j,D,B).
\]

따라서 gap certificate는

\[
\boxed{
C_z(k,j,D,B)-A_z(k,j,B)>G.
}
\]

state가 반복되면 동일한 necessary residue geometry를 재사용할 수 있다.

---

# 40. Coverage용 anchor–translation 구조

각 anchor

\[
S_k=2^k
\]

에 대해

\[
S_{k,j}=S_k+2j
\]

를 생성한다.

이 구조는 전체 even start lattice를 특정 anchor family를 기준으로 표현하는 방식이다.

중요한 점은 실제 proof에서 중복 coverage가 발생하지 않도록 하나의 canonical mapping을 정의해야 한다는 것이다.

예를 들어 각 짝수 \(S\)에 대해 선택되는 고유한 \((k,j)\) 규칙을 정하거나, 단순히 \(S=2m\)를 primary coordinate로 두고 \(2^k+2j\)를 state-generation representation으로만 사용하는 방법이 있다.

---

# 41. 권장 coordinate 해석

수학적으로 가장 깔끔한 방식은

\[
\boxed{S=2m}
\]

을 실제 coverage coordinate로 사용하고,

\[
S=2^k+2j
\]

는

\[
\boxed{\text{residue-state anchor/translation representation}}
\]

으로 사용하는 것이다.

이렇게 하면

- coverage가 단순하고,
- \(S\)의 parity가 항상 보장되며,
- \(2^k\) 구조를 state initialization에 활용할 수 있다.

---

# 42. 후보 state와 실제 위치의 관계

동일한 residue state를 가진 두 위치는 동일한 small-prime necessary-condition pattern을 가진다.

따라서 다음을 미리 계산할 수 있다.

\[
\boxed{
\text{state}
\rightarrow
\text{survivor pattern}
\rightarrow
\text{block candidate count}
}
\]

하지만 exact prime pattern은 동일하지 않으므로, state-level pruning만으로 모든 위치를 자동 제거할 수 있다고 가정하면 안 된다.

---

# 43. 통합 upper bound

각 block에 대해 다음을 사용한다.

\[
U_j
=
\min\left(
U_{Q,j},
U_{\rm residue,j},
U_{\rm sieve,j},
U_{\rm other,j}
\right).
\]

여기서 각 항은 서로 다른 증명 또는 계산기반 upper bound다.

이들은 경쟁 관계가 아니라 동시에 사용되는 tightening layers다.

---

# 44. 통합 lower bound

부재증명에서는 특정 block에 적어도 하나의 소수가 있다는 것도 필요할 수 있다.

따라서 독립적으로

\[
\boxed{L_j\le N_j}
\]

를 구성한다.

가능한 방법은

- exact prime count
- explicit prime-existence theorem
- verified primality of at least one candidate
- 기타 rigorous lower-bound theorem

등이다.

그리고

\[
L_j\ge1
\]

이면 해당 block은 certainly nonempty다.

---

# 45. 3-state certificate

최종적으로 각 block을

\[
\boxed{
\begin{cases}
U_j<1 &\Rightarrow \text{EMPTY},\\
L_j\ge1 &\Rightarrow \text{NONEMPTY},\\
\text{otherwise} &\Rightarrow \text{UNDECIDED}
\end{cases}}
\]

로 분류한다.

UNDECIDED만 exact prime verification 대상으로 남긴다.

이것이 계산량을 줄이는 가장 직접적인 형태다.

---

# 46. 목표 gap의 부재 certificate

어떤 가능한 gap configuration에 대해, 그 gap이 \(G\ge1856\)이 되려면 반드시 empty여야 하는 영역을

\[
E_1,E_2,\ldots,E_r
\]

라고 하자.

그 중 하나라도

\[
L(E_i)\ge1
\]

이면 해당 gap candidate는 불가능하다.

즉

\[
\boxed{
\text{required-empty region contains a rigorously nonempty block}
\Rightarrow
\text{candidate rejected.}
}
\]

이것이 최종 부재증명의 핵심 rejection rule이다.

---

# 47. Coverage theorem의 최종 형태

다음 정리를 목표로 한다.

> **Coverage Theorem:**
> 
> 임의의 두 연속 소수 \(p_n<p_{n+1}\)가 연구범위 내에서
> \(p_{n+1}-p_n\ge G\)를 만족한다면, 그 쌍은 적어도 하나의 정의된 candidate state \((S,B,D,k,j,z)\)에 대응한다.

그 다음

> **Rejection Theorem:**
> 
> 정의된 모든 candidate state에 대해 해당 gap의 필수 조건과 모순되는 rigorous certificate가 존재한다.

이 둘을 합치면

\[
\boxed{
\text{Coverage}+	ext{Rejection}
\Rightarrow
\text{no gap}\ge G.
}
\]

---

# 48. 최종 부재증명 정리의 목표

연구범위 \([A,B]\)에 대해 다음을 증명하는 것이 최종 목표다.

### 정리 목표

모든 가능한 prime pair \((p_n,p_{n+1})\)에 대해

\[
p_n,p_{n+1}\in[A,B]
\]

이면

\[
\boxed{
p_{n+1}-p_n\le1854.
}
\]

동치로

\[
\boxed{
\nexists(p_n,p_{n+1})\text{ in range with }p_{n+1}-p_n\ge1856.
}
\]

---

# 49. 범위 경계 처리

gap이 범위 경계에서 걸칠 수 있으므로 실제 candidate domain은 단순히 \([A,B]\)만 고려해서는 안 될 수 있다.

예를 들어

\[
p_n<A<p_{n+1}
\]

또는

\[
p_n<B<p_{n+1}
\]

인 경우를 어떻게 정의할지 명확히 해야 한다.

필요한 경우

\[
[A-G,B+G]
\]

같은 guard region을 내부적으로 검증한다.

최종적으로 “range 내부의 gap”의 정의를 문서와 구현에서 하나로 고정한다.

---

# 50. 계산비용 모델

우리 추가 이론의 계산비용을

\[
T_{\rm extra}
\]

라 하고, 그 결과 줄어드는 기존 exact/sieve work를

\[
T_{\rm saved}
\]

라 하자.

통합 알고리즘의 비용은

\[
\boxed{
T_{\rm hybrid}
=
T_{\rm base}
+
T_{\rm extra}
-
T_{\rm saved}.
}
\]

따라서 추가 이론이 계산적으로 유효하려면

\[
\boxed{
T_{\rm saved}>T_{\rm extra}.
}
\]

이 조건을 모든 추가 아이디어별로 독립적으로 측정한다.

---

# 51. 추가 아이디어별 marginal value

각 아이디어 \(H_i\)에 대해

\[
\boxed{
\Delta T_i
=
T_{\rm before}-T_{\rm after}
}
\]

와

\[
\boxed{
C_i=T_{\rm compute}(H_i)
}
\]

를 측정한다.

유효한 아이디어의 조건은

\[
\boxed{
\Delta T_i>C_i.
}
\]

즉 “후보를 몇 % 줄였는가”보다 “추가 계산에 비해 얼마나 많은 expensive work를 절약했는가”가 최종 기준이다.

---

# 52. Li 사용 여부에 따른 두 알고리즘 경로

## No-Li 경로

\[
\boxed{
\text{coverage}
\rightarrow
G–B–D
\rightarrow
\text{residue-state}
\rightarrow
\text{exact/verified count}
}
\]

장점:

- 추가 transcendental evaluation 비용이 없음
- purely arithmetic/residue 기반 filter
- 구현과 검증이 비교적 단순

---

## Li 경로

\[
\boxed{
\text{coverage}
\rightarrow
G–B–D
\rightarrow
\Delta_B\operatorname{li}
\rightarrow
Q\text{/count bound}
\rightarrow
\text{residue/exact}
}
\]

Li는 cheap coarse estimate 및 analytic upper bound에 사용한다.

단순 \(B/\log x\)만 사용하는 것은 새로운 rigorous information이 아니며, rigorous 역할을 하려면 explicit error bound가 필요하다.

---

# 53. 현재 Q의 실제 역할과 우선순위

현재 연구 단계에서는

\[
Q_{20,21}(1856)\ge-280.6166400756
\]

이므로 Q가 곧바로 empty-block certificate를 제공하지 않는다.

따라서 1차 알고리즘 개발에서 Q는

\[
\boxed{\text{auxiliary analytic layer}}
\]

로 둔다.

우선순위는

1. Coverage theorem
2. G-specific block geometry
3. Residue-state compression
4. Exact undecided-state verification
5. 그 다음 Q/Li 강화

순으로 둔다.

---

# 54. 계산적으로 권장하는 전체 구조

전체 알고리즘을 다음 순서로 생각한다.

\[
\boxed{
\text{Range }[A,B]
}
\]

↓

\[
\boxed{
\text{all possible }G\text{-gap candidates covered}
}
\]

↓

\[
\boxed{
S=2^k+2j\text{ representation / residue state}
}
\]

↓

\[
\boxed{
G,B,D\text{ feasibility pruning}
}
\]

↓

\[
\boxed{
\text{residue survivor restriction}
}
\]

↓

\[
\boxed{
Q/\operatorname{li}\text{ optional analytic pruning}
}
\]

↓

\[
\boxed{
\text{3-state block classification}
}
\]

↓

\[
\boxed{
\text{exact verification of UNDECIDED states only}
}
\]

↓

\[
\boxed{
\text{all candidates rejected}
}
\]

↓

\[
\boxed{
\text{No gap }\ge1856\text{ in range}
}
\]

---

# 55. 1차 연구범위: \(10^{20}\)–\(10^{21}\)

첫 번째 실험 및 알고리즘 고도화 범위를

\[
\boxed{
10^{20}\le x\le10^{21}
}
\]

로 고정한다.

이 범위는 기존에 알려진 1854 record와 바로 연결되는 중요한 검증구간이며, 네 알고리즘이 실제로 누락 없이 작동하는지를 실험할 수 있는 현실적인 첫 단계다.

이 단계의 목적은 1856 부재 자체를 최종적으로 확정하는 것이 아니라 다음을 측정하는 것이다.

\[
\boxed{
\text{coverage correctness}
}
\]

\[
\boxed{
\text{candidate reduction}
}
\]

\[
\boxed{
\text{state compression}
}
\]

\[
\boxed{
\text{exact-test reduction}
}
\]

\[
\boxed{
\text{wall-clock / CPU work}
}
\]

---

# 56. 1차 실험에서 반드시 비교할 항목

### Configuration A

우리 이론의 최소 구현:

\[
G–B–D + S=2^k+2j + residue-state.
\]

### Configuration B

A + Li.

### Configuration C

A + Q.

### Configuration D

A + Li + Q.

각 configuration에서

- candidate count
- residue survivor count
- undecided count
- exact verification count
- total arithmetic operations
- wall-clock time

을 측정한다.

---

# 57. 가장 중요한 benchmark 지표

단순 wall-clock 하나만 보면 안 된다.

다음 값을 기록한다.

\[
\boxed{
N_{\rm raw}
}
\]

전체 이론적 candidate 수.

\[
\boxed{
N_{\rm residue}
}
\]

residue filter 이후 후보 수.

\[
\boxed{
N_{\rm undecided}
}
\]

cheap certificate로 결정하지 못하고 exact verification이 필요한 후보 수.

\[
\boxed{
N_{\rm exact}
}
\]

실제로 expensive exact check를 받은 후보 수.

그리고

\[
\boxed{
T_{\rm total},
T_{\rm filter},
T_{\rm exact}
}
\]

를 분리한다.

---

# 58. 이론의 성공 기준

이론적 성공은 단순히 “후보가 줄었다”가 아니다.

### 수학적 성공

\[
\boxed{
\text{Coverage}=100\%.
}
\]

### 계산적 성공

\[
\boxed{
T_{\rm saved}>T_{\rm extra}.
}
\]

### 알고리즘적 성공

\[
\boxed{
N_{\rm exact}\ll N_{\rm raw}.
}
\]

이 세 조건을 동시에 만족해야 한다.

---

# 59. 현재 이론에서 이미 확립된 부분

다음은 통합 framework의 기준선이다.

\[
D(x)=\operatorname{li}(x)-\pi(x)
\]

\[
D(x+h)-D(x)=\Delta_h\operatorname{li}(x)-N(x,h)
\]

\[
Q(X,h)=\inf_{x\ge X}[D(x+h)-D(x)]
\]

\[
Q\ge-q\Rightarrow N(x,h)<\Delta_h\operatorname{li}(x)+q
\]

\[
N(I)\le|C_z(I)|
\]

\[
N_j=\pi(S+jB-1)-\pi(S+(j-1)B-1)
\]

\[
\Delta_{\min}^{(2)}(B,D)=
\begin{cases}
(D-1)B+3,&B\text{ odd},D\text{ even},\\
(D-1)B+2,&\text{otherwise}
\end{cases}
\]

\[
S_{k,j}=2^k+2j
\]

\[
\operatorname{State}_q(k,j)=2^k+2j\pmod q
\]

\[
U_j<1\Rightarrow N_j=0
\]

이 모든 것은 통합이론의 기준 구성요소다.

---

# 60. 현재 이론에서 아직 증명해야 하는 핵심 부분

다음은 반드시 후속 세션에서 연구해야 한다.

1. **Coverage theorem**
   
   \(S=2^k+2j\) 또는 동등한 coordinate가 전체 가능한 1856-gap candidate를 빠짐없이 표현한다는 것을 엄밀하게 증명한다.

2. **Complete rejection theorem**
   
   각 candidate가 empty/nonempty/undecided 중 하나로 빠짐없이 분류되며, undecided만 exact verification하면 전체 부재증명이 완성됨을 증명한다.

3. **Residue-state compression theorem**
   
   state periodicity를 이용하여 어떤 계산을 실제로 공유할 수 있는지 엄밀히 구분한다.

4. **Cost model**
   
   state construction, residue filtering, Li/Q evaluation, exact verification 각각의 비용을 정량화한다.

5. **Q improvement**
   
   현재 -280.6 수준의 bound를 실제 algorithmically useful 수준으로 개선할 수 있는지 검토한다.

6. **Endpoint bound**
   
   \(A_z,C_z\)를 일반적인 \(z,k,j,B,D\)에 대해 계산하는 방법을 정식화한다.

---

# 61. 가장 중요한 안전한 해석

현재 문서가 주장하는 것은 다음과 같다.

\[
\boxed{
\text{통합이론은 1856 부재증명을 위한 후보 coverage + rejection framework를 제공한다.}
}
\]

하지만 아직

\[
\boxed{
\text{이 framework만으로 }10^{20}\text{–}10^{21}\text{ 전체 부재가 증명되었다}
}
\]

고 주장하지 않는다.

또한

\[
\boxed{
Q_{20,21}(1856)=-40
}
\]

등의 값도 증명된 사실로 취급하지 않는다.

---

# 62. 후속 세션에서 바로 수행할 알고리즘 고도화 과제

## Priority 1 — Coverage formalization

\[
S=2^k+2j
\]

를 실제 범위 coverage coordinate와 어떻게 연결할지 결정한다.

## Priority 2 — 최적 \((B,D)\) 탐색

\[
\Delta_{\min}^{(2)}(B,D)>1856
\]

을 만족하는 모든 후보 중 verification cost가 최소인 조합을 찾는다.

## Priority 3 — residue-state compression

\[
\operatorname{State}_z(k,j)
\]

의 주기와 필요한 precomputation 규모를 계산한다.

## Priority 4 — endpoint certificate

\[
A_z(k,j,B),
\quad
C_z(k,j,D,B)
\]

를 계산하고 기존 parity-only bound보다 얼마나 강한지 측정한다.

## Priority 5 — 3-state classifier

각 block을 EMPTY / NONEMPTY / UNDECIDED로 분류하는 실제 rigorous rule을 구축한다.

## Priority 6 — Li/Q evaluation

No-Li 버전과 Li/Q 버전의 marginal candidate reduction 및 arithmetic overhead를 비교한다.

## Priority 7 — exact verification bridge

UNDECIDED 후보를 exact prime-count/primality verification으로 넘기는 규칙을 정식화한다.

## Priority 8 — \(10^{20}\)–\(10^{21}\) complete test

위 구조가 완성된 뒤 실제 범위에서 coverage와 누락 여부를 검증한다.

---

# 63. 최종 통합식

현재 통합이론을 가장 압축하면 다음과 같다.

\[
\boxed{
S_{k,j}=2^k+2j
}
\]

\[
\boxed{
I_j=[S_{k,j}+(j'-1)B,\;S_{k,j}+j'B-1]
}
\]

각 block의 count:

\[
\boxed{
N_{j'}=
\pi(S_{k,j}+j'B-1)
-
\pi(S_{k,j}+(j'-1)B-1)
}
\]

각 count에 대해

\[
\boxed{
L_{j'}\le N_{j'}\le U_{j'}
}
\]

을 구축하고

\[
\boxed{
U_{j'}<1\Rightarrow N_{j'}=0
}
\]

\[
\boxed{
L_{j'}\ge1\Rightarrow N_{j'}\ge1
}
\]

로 분류한다.

Residue-state는

\[
\boxed{
\operatorname{State}_z(k,j)=
(2^k+2j\bmod q)_{q\le z,\ q>2}
}
\]

이다.

Gap certificate는

\[
\boxed{
C_z(k,j,D,B)-A_z(k,j,B)>G
}
\]

이고, 최종 부재증명은 모든 covered candidate에 대해

\[
\boxed{
\text{required-empty condition is contradicted by a rigorous NONEMPTY certificate}
}
\]

또는 그와 동등한 rigorous rejection certificate를 확보하는 것이다.

---

# 64. 최종 연구 목표의 한 문장 정의

\[
\boxed{
\textbf{고정 }G=1856\textbf{에 대해 전체 범위를 100\% coverage하면서,}
}
\]

\[
\boxed{
\textbf{Li–π local bound, G–B–D block geometry, }S=2^k+2j\textbf{ residue-state 및 exact verification을 결합하여}
}
\]

\[
\boxed{
\textbf{모든 가능한 }1856\textbf{-gap candidate를 rigorous하게 제거하고,}
}
\]

\[
\boxed{
\textbf{결과적으로 해당 범위의 maximal prime gap이 }1854\textbf{ 이하임을 증명하는 것.}
}

첫 번째 실험 단계는

\[
\boxed{10^{20}\le x\le10^{21}}
\]

에서 이 framework의 **coverage, correctness, candidate reduction, state compression, exact-test reduction, 연산비용**을 검증하는 것이다.
