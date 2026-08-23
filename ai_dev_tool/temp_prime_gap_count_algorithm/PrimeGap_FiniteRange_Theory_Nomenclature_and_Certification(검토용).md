# Finite-Range Prime-Gap Count와 C-Normalized Upper-Bound Certificate
## 명칭·기호·증명 구조·계산량 절감 메커니즘·후속 연구 계획

## 0. 문서 목적

이 문서는 특정한 `1856`에만 종속된 임시 명칭을 버리고, 현재 연구에서 사용하는 함수와 증명/계산 기법을 **일반적인 수학적 객체와 알고리즘으로 재정의**하기 위한 문서다.

최종 연구 목적은 다음과 같다.

> \(10^{20}\)부터 \(10^{26}\)까지의 유한 구간에서, 주어진 gap threshold \(H\)보다 큰 consecutive-prime gap이 존재하지 않음을 CPU 계산으로 가능한 한 빠르게 검증한다.

현재의 대표 사례는

\[
H=1856
\]

이다.

또한 문헌/기록에 아직 확정되지 않은 \(1858\) 후보가 존재하므로, 장래에는

\[
H=1856,\qquad H=1858
\]

을 동일한 framework에서 처리할 수 있어야 한다.

---

# 1. 권장되는 기본 표기

사용자가 제안한

\[
N_{\mathrm{PrimeGap\_max}}
(10^{\mathrm{Upper}};10^{\mathrm{Lower}},10^{\mathrm{Upper}})
\]

형식은 의미는 전달되지만, 함수의 인자가 무엇인지 모호하고 `PrimeGap_max`가 함수 이름인지 조건인지 구분하기 어렵다.

연구용으로는 다음과 같이 일반화하는 것을 권장한다.

## 1.1 일반적인 gap-count 함수

\[
\boxed{
N_{\ge H}(A,B)
:=
\#\left\{
p:\ A\le p<B,\ 
p\text{와 }p_{\rm next}\text{가 consecutive primes},
\ p_{\rm next}-p\ge H
\right\}.
}
\]

여기서:

- \(N_{\ge H}\): **thresholded consecutive-prime gap count**
- \(H\): **gap threshold**
- \(A\): **lower range bound**
- \(B\): **upper range bound**
- \(p_{\rm next}\): \(p\) 다음의 consecutive prime

이 notation이 가장 직접적이다.

---

## 1.2 사용자 제안 notation과의 대응

사용자가 제안한

\[
N_{\mathrm{PrimeGap\_max}}
(10^{\mathrm{Upper}};10^{\mathrm{Lower}},10^{\mathrm{Upper}})
\]

를 일반화하면 다음처럼 해석할 수 있다.

\[
\boxed{
N_{\mathrm{PrimeGap}}(H;B,A,B)
\equiv
N_{\ge H}(A,B)
}
\]

다만 실제 논문에서는 `PrimeGap_max`보다

\[
\boxed{N_{\ge H}(A,B)}
\]

를 권장한다.

이유는 함수가 실제 maximal gap을 반환하는 것이 아니라 **주어진 threshold 이상인 gap의 개수**를 반환하기 때문이다.

---

# 2. Maximal-gap 함수와의 관계

실제 최대 gap을 별도로 정의하면:

\[
\boxed{
G(A,B)
:=
\max
\left\{
p_{\rm next}-p:
A\le p<B
\right\}.
}
\]

따라서

\[
\boxed{
G(A,B)<H
\iff
N_{\ge H}(A,B)=0.
}
\]

prime gap은 \(2\)보다 큰 경우 짝수이므로, 예를 들어

\[
N_{\ge1856}(10^{20},10^{21})=0
\]

이면

\[
G(10^{20},10^{21})\le1854
\]

를 의미한다.

따라서 **gap-count function이 computational certificate의 기본 대상**이고, \(G(A,B)\)는 최종적으로 해석되는 maximal-gap quantity이다.

---

# 3. Upper / Lower의 일반화

사용자가 제안한

\[
\mathrm{Upper},\qquad \mathrm{Lower}
\]

는 다음처럼 정의할 수 있다.

\[
\boxed{
A=10^{\mathrm{Lower}},
\qquad
B=10^{\mathrm{Upper}}.
}
\]

따라서

\[
\boxed{
N_{\ge H}
(10^{\mathrm{Lower}},10^{\mathrm{Upper}})
}
\]

는

> \(10^{\mathrm{Lower}}\le p<10^{\mathrm{Upper}}\)에서 \(H\) 이상의 consecutive-prime gap이 몇 개인가

를 뜻한다.

### 권장 기호

- `Lower`: \(\mathrm{Lower}\)
- `Upper`: \(\mathrm{Upper}\)
- 실제 경계: \(A=10^{\mathrm{Lower}}, B=10^{\mathrm{Upper}}\)

---

# 4. `PrimeGap_max`라는 명칭 대신 권장하는 명칭

다음 세 가지를 구분하는 것이 좋다.

### 4.1 `Thresholded Prime-Gap Count`

\[
N_{\ge H}(A,B)
\]

가 계산하는 양의 가장 정확한 설명이다.

### 4.2 `Finite-Range Maximal-Gap Count`

구간이 finite range라는 점을 강조할 때 사용할 수 있다.

### 4.3 `Large-Gap Count`

\(H\)가 현재의 maximal-gap 규모보다 큰 임계값이라는 점을 강조할 때 사용할 수 있다.

논문/코드에서 가장 권장:

\[
\boxed{\textbf{Thresholded Consecutive-Prime Gap Count}}
\]

함수명은:

```text
count_gaps_geq(H, A, B)
```

또는 수학적 표기는:

\[
N_{\ge H}(A,B).
\]

---

# 5. C-normalized upper bound의 정의

현재 연구에서는 다음과 같은 C-normalized bound를 사용한다.

\[
N_{\ge H}(A,B)
\le
C\,
\mathcal{T}(H;A,B)
\]

여기서

\[
\boxed{
\mathcal{T}(H;A,B)
:=
\frac{B-A}{\log B}
\exp\left(
-\frac{H}{\log B}
\right).
}
\]

따라서

\[
\boxed{
C(H;A,B)
:=
\frac{
N_{\ge H}(A,B)
}{
\mathcal{T}(H;A,B)
}.
}
\]

실제 \(N_{\ge H}\)를 모르는 상태에서 우리가 증명하고 싶은 것은

\[
\boxed{
C(H;A,B)\le C_{\max}
}
\]

형태의 상계이다.

---

# 6. `C_max`의 정확한 의미

`C`와 `C_max`를 혼동하면 안 된다.

## 6.1 실제 C

이론적으로 실제 gap count를 알면

\[
C_{\rm actual}
=
\frac{
N_{\ge H}(A,B)
}{
\mathcal{T}(H;A,B)
}.
\]

하지만 \(N_{\ge H}\)를 아직 모르기 때문에 직접 계산할 수 없다.

## 6.2 증명 가능한 \(C_{\max}\)

우리가 증명하는 것은

\[
\boxed{
C_{\rm actual}\le C_{\max}.
}
\]

즉 \(C_{\max}\)는 **증명 가능한 normalized upper-bound constant**이다.

따라서 연구의 목표는:

\[
\boxed{
\text{증명 가능한 }C_{\max}\text{를 최대한 작게 만드는 것}
}
\]

이다.

---

# 7. 현재 가장 단순한 무조건적 \(C_{\max}\)

각 gap이 최소 \(H\)이므로 gap들이 서로 겹치지 않는다.

따라서

\[
N_{\ge H}(A,B)
\le
\left\lfloor
\frac{B-A}{H}
\right\rfloor.
\]

이를 \(\mathcal T(H;A,B)\)에 대입하면

\[
C_{\max}^{\rm packing}
=
\frac{
(B-A)/H
}{
\frac{B-A}{\log B}e^{-H/\log B}
}
\]

이므로

\[
\boxed{
C_{\max}^{\rm packing}
=
\frac{\log B}{H}
e^{H/\log B}.
}
\]

이것은 **완전히 무조건적인 수론적 bound**이다.

현재 대표 사례

\[
H=1856,\quad A=10^{20},\quad B=10^{21}
\]

에서는

\[
\boxed{
C_{\max}^{\rm packing}
\approx1.2177\times10^{15}.
}
\]

이 값은 이전 연구의 출발점이다.

---

# 8. 현재 사용하고 있는 개선 기법의 명칭

현재 2310 residue-state 방법은 특정 1856에만 해당하는 것이 아니므로 다음과 같이 부르는 것을 권장한다.

\[
\boxed{
\textbf{Finite-Range Residue-State Gap Certificate}
}
\]

또는 조금 더 기술적으로:

\[
\boxed{
\textbf{Residue-State Dual Certificate for Thresholded Prime Gaps}
}
\]

한국어로는:

> **유한구간 소수-gap residue-state 쌍대 인증법**

또는

> **임계 소수-gap 유한상태 잔여류 쌍대 상계법**

정도가 적절하다.

---

# 9. 이 기법의 핵심 아이디어

\(p>q_{\max}\)인 prime은 작은 primorial \(M\)과 서로소여야 한다.

현재 사용한 예:

\[
M=2\cdot3\cdot5\cdot7\cdot11
=2310.
\]

따라서 prime \(p\)는

\[
p\bmod2310
\]

중

\[
\varphi(2310)=480
\]

개의 허용 residue 중 하나에만 존재한다.

consecutive prime gap \(d\)가 주어지면

\[
s\equiv r+d\pmod M
\]

이고 \(r,s\) 모두 허용 residue여야 한다.

따라서 실제 prime sequence는 임의의 gap sequence가 아니라 **유한 상태 전이 시스템**으로 제한된다.

---

# 10. `Residue-State`를 왜 사용하는가

실제 prime 목록을 계산하는 대신 다음 세 정보만 사용한다.

1. prime residue condition
2. gap이 양의 짝수라는 조건
3. 총 gap length가 전체 구간 길이를 넘을 수 없다는 조건

이것을 finite-state flow로 표현한다.

각 transition \(e=(r,s,d)\)에 대해 변수 \(x_e\)를 두고:

\[
x_e\ge0
\]

\[
\sum_e x_e=1
\]

및 residue flow conservation:

\[
\sum_{e:\operatorname{tail}(e)=r}x_e
=
\sum_{e:\operatorname{head}(e)=r}x_e
\]

를 둔다.

추가로 평균 gap 조건:

\[
\sum_e d_e x_e
\le
\frac{B-A}{N_{\rm gaps}}
\]

을 적용할 수 있다.

목표는:

\[
\max
\sum_{e:d_e\ge H}x_e.
\]

이것이 **residue-state primal LP**다.

---

# 11. 왜 dual certificate가 중요한가

LP solver가 floating-point로 최적값을 찾는 것 자체는 증명이 아니다.

증명으로 만들려면 dual 변수

\[
\lambda,\mu,\phi(r),t
\]

를 정수/유리수 형태로 제시하고 모든 transition에 대해

\[
\boxed{
1_{\{d\ge H\}}
\le
\lambda d+\mu+\phi(r)-\phi(s)
}
\]

를 확인한다.

전체 gap sequence에 대해 합하면

\[
\phi(r_i)-\phi(r_{i+1})
\]

가 telescope하므로

\[
N_{\ge H}
\le
\lambda\sum_i d_i+\mu N_{\rm gaps}
+\text{boundary term}
\]

이 된다.

따라서 이것은 단순한 numerical optimization 결과가 아니라 **machine-checkable mathematical certificate**가 된다.

---

# 12. 현재 2310-state certificate

현재 연구에서 사용한:

\[
M=2310
\]

에는

\[
480
\]

개의 prime residue state가 있다.

transition constraint는 약

\[
415,223
\]

개이다.

부동소수점 LP를 이용해 후보 certificate를 찾은 뒤, 이를 유리수/정수 형태로 변환하여 모든 transition을 exact integer arithmetic으로 확인하는 구조다.

현재 이전 작업에서 사용한 certificate에 대해:

\[
N_{1856}
\le
4.39161464927854179\times10^{17}
\]

라는 상계가 얻어졌고, 이에 해당하는 normalized constant는

\[
\boxed{
C_{\max}
\approx
1.102803437542279\times10^{15}
}
\]

이다.

**주의:** 이 값은 향후 독립적인 verifier와 certificate 파일을 재실행하여 다시 확인하는 것을 권장한다. 특히 새로운 30030-state 구현으로 넘어가기 전에 2310-state 결과를 독립 코드로 재현하는 것이 좋다.

---

# 13. 현재 C 개선의 의미

초기 packing bound:

\[
1.2177\times10^{15}
\]

현재 2310-state certificate:

\[
1.1028\times10^{15}.
\]

따라서 약

\[
9.4\%
\]

감소했다.

이것이 중요한 이유는 단순한 숫자 개선이 아니라 **계산 후보 공간의 수학적 upper bound를 직접 낮추는 기반 이론**이기 때문이다.

---

# 14. C를 낮추는 것이 계산량을 줄이는 방법

C의 역할은 직접적인 prime-count cost를 줄이는 것이 아니라 **계산이 필요한 large-gap candidate의 개수를 상한으로 제한하는 것**이다.

예를 들어:

\[
N_{\ge H}\le C_{\max}\mathcal T(H;A,B).
\]

그리고 각 surviving candidate를 exact CPU algorithm으로 검사한다고 하자.

후보 1개 검사 비용을 \(t_{\rm cand}\)라고 하면,

\[
T_{\rm verification}
\lesssim
C_{\max}\mathcal T(H;A,B)t_{\rm cand}.
\]

따라서

\[
C_{\max}\downarrow
\]

이면 최종 exact computation의 worst-case workload가 선형적으로 감소한다.

---

# 15. 이 방식의 중요한 장점

이론상:

\[
\boxed{
C_{\max}\text{는 실제 prime list 없이 계산 가능}
}
\]

하다.

즉:

```text
수론적 certificate
        ↓
large-gap candidate count의 upper bound
        ↓
CPU exact verification 대상 감소
        ↓
9700X runtime 감소
```

라는 두 단계 구조가 가능하다.

이것이 본 연구에서 C를 낮추는 궁극적인 목적이다.

---

# 16. C_max를 낮추기 위한 현재/다음 기법

## Level 0 — Gap packing

\[
C_{\max}\approx1.2177\times10^{15}.
\]

증명 난이도: 매우 낮음.

---

## Level 1 — Residue-State Dual Certificate

현재:

\[
M=2310.
\]

기법명:

> **Finite-Range Residue-State Gap Certificate**

핵심:

\[
\text{modular prime residue constraints}
+
\text{gap-state transitions}
+
\text{LP duality}.
\]

현재 목표는:

\[
M\rightarrow30030\rightarrow510510\rightarrow9699690.
\]

---

## Level 2 — Gap-Specific Buchstab Factorization

내부

\[
p+2,\ldots,p+H-2
\]

가 전부 composite라는 구조를 사용한다.

각 내부 composite를

- small-prime factor
- medium factor
- large-prime-factor/semiprime

등으로 분해한다.

기법명:

> **Gap-Specific Buchstab–Selberg Decomposition**

또는

> **Consecutive-Prime Gap Buchstab Decomposition**

---

## Level 3 — Type-I / Type-II upper-bound sieve

gap candidate를 factor-size에 따라 분리한다.

\[
N_{\ge H}
=
N_{\rm I}+N_{\rm II}+N_{\rm exceptional}.
\]

각 항의 explicit upper bound를 합친다.

이 단계가 성공하면 residue-state certificate보다 훨씬 강한 \(C_{\max}\) 감소가 가능할 수 있다.

---

## Level 4 — Finite-Range Hybrid Certificate

최종적으로는 다음을 결합한다.

\[
\boxed{
\text{Residue-State Certificate}
+
\text{Buchstab Decomposition}
+
\text{Selberg Upper Sieve}
+
\text{Type-I/II Bounds}
}
\]

이것을

> **Finite-Range Hybrid Large-Gap Certificate**

라고 부르는 것을 권장한다.

---

# 17. 왜 전역 \(K=3,4\)를 그대로 목표로 하면 안 되는가

고정 \(H=1856\)에 대해 \(X\to\infty\)에서

\[
N_{\ge1856}(X)
\]

가 실제로

\[
X/\log^2X
\]

규모일 가능성이 높기 때문에, 무조건적으로

\[
N_{\ge1856}(X)\ll X/\log^3X
\]

또는

\[
X/\log^4X
\]

를 전역 정리로 주장하는 것은 prime-pair heuristic과 충돌할 가능성이 있다.

따라서 우리가 목표로 하는 것은:

\[
\boxed{
10^{\mathrm{Lower}}\le X\le10^{\mathrm{Upper}}
}
\]

에서만 유효한 **finite-range explicit bound**다.

---

# 18. 향후 연구 대상의 일반화

현재 \(H=1856\)이지만 함수는 다음처럼 일반화한다.

\[
\boxed{
N_{\ge H}(A,B)
}
\]

그리고:

\[
H\in\{1856,1858,\ldots\}
\]

를 바꿀 수 있다.

따라서 실제 연구 플랫폼은:

```text
Threshold H
Lower exponent L
Upper exponent U
Residue modulus M
Dual certificate
Buchstab parameters
Selberg parameters
```

를 입력으로 받아

\[
C_{\max}(H;10^L,10^U)
\]

를 계산하는 시스템으로 설계할 수 있다.

---

# 19. 10^20 ~ 10^26으로 확장할 때의 목표

장기 목표:

\[
10^{20}
\le
p
<
10^{26}.
\]

현재 알려진 기록표에는 \(1858\)이 약

\[
3.9422251630462640179641871\times10^{25}
\]

에서 `Confirmed = N`으로 기록되어 있다.

따라서 이 후보가 확정되기 전까지는:

- \(H=1856\): 확정 maximal-gap threshold
- \(H=1858\): 문헌상 미확정 후보 threshold

를 모두 parameterized하게 다루는 것이 좋다.

장기 알고리즘의 목표는:

\[
N_{\ge1856}(10^{20},10^{26})=0
\]

또는 필요하다면

\[
N_{\ge1858}(10^{20},10^{26})=0
\]

을 CPU에서 가능한 빠르게 인증하는 것이다.

---

# 20. Codex 검토 요청의 핵심

로컬 Codex에게 다음 사항을 반드시 검토하도록 한다.

### 수학적 타당성

- \(N_{\ge H}(A,B)\) 정의의 경계 처리
- \(G(A,B)<H\iff N_{\ge H}(A,B)=0\)의 정확성
- gap boundary crossing 처리
- 2310 residue-state transition 생성의 완전성
- LP dual inequality의 telescope 논리
- rational/integer certificate의 정확성
- 현재 \(C_{\max}\) 계산에서 반올림 오차가 없는지
- exact verifier와 certificate generator의 독립성

### 선행연구

다음 분야를 조사한다.

- Brun sieve
- Selberg sieve
- upper-bound sieve
- Buchstab identity
- Type-I/Type-II decomposition
- prime-pair upper bounds
- admissible tuples
- Jacobsthal function
- large prime gaps
- Banks–Ford–Tao
- finite-range explicit prime-gap results
- Montgomery–Vaughan / Halberstam–Richert 계열 sieve
- computational large-gap search
- `primesieve`, PGS, Oliveira e Silva 계열

### 알고리즘 연구

다음을 비교한다.

\[
M=2310
\]

\[
M=30030
\]

\[
M=510510
\]

\[
M=9699690
\]

에 대해:

- state 수
- transition 수
- LP solve 비용
- exact dual verification 비용
- certificate 크기
- \(C_{\max}\) 개선량
- Ryzen 7 9700X에서 계산시간

을 벤치마크한다.

### 최종 목표

\[
\boxed{
C_{\max}\le10^{14}
}
\]

를 1차 연구 목표로 한다.

그 뒤:

\[
10^{13},10^{12},\ldots
\]

로 단계적으로 낮춘다.

---

# 21. 최종 용어 추천

이 연구 전체를 다음 이름으로 부르는 것을 권장한다.

## 수학적 기법

\[
\boxed{
\textbf{Finite-Range Residue-State Gap Certificate (FR-RSGC)}
}
\]

한국어:

> **유한구간 잔여류-상태 소수-gap 인증법**

## 강화 버전

\[
\boxed{
\textbf{Finite-Range Hybrid Large-Gap Certificate (FR-HLGC)}
}
\]

한국어:

> **유한구간 하이브리드 대규모 소수-gap 상계 인증법**

여기서:

- `FR` = Finite-Range
- `RSGC` = Residue-State Gap Certificate
- `HLGC` = Hybrid Large-Gap Certificate

## 핵심 bound

\[
\boxed{
N_{\ge H}(A,B)
\le
C_{\max}(H;A,B)\,
\mathcal T(H;A,B)
}
\]

를 **C-normalized finite-range upper-bound certificate**라고 부르는 것을 권장한다.

## 연구 목표

\[
\boxed{
\min C_{\max}(H;A,B)
}
\]

즉:

> **Finite-Range C-Normalized Gap-Count Bound Minimization**

이다.

---

# 22. 가장 중요한 연구 방향

현재까지의 결과를 한 줄로 요약하면:

\[
\boxed{
\text{Gap packing}
\rightarrow
\text{Residue-State Dual Certificate}
\rightarrow
\text{Buchstab/Selberg factor decomposition}
\rightarrow
\text{Type-I/II finite-range certificate}
}
\]

순으로 \(C_{\max}\)를 낮추는 것이 가장 체계적이다.

현재 단계에서는

\[
\boxed{
C_{\max}\approx1.1028\times10^{15}
}
\]

가 2310-state dual certificate의 목표값이다.

다음 단계는

\[
\boxed{
M=30030
}
\]

에서 **새 exact dual certificate를 찾아 실제 \(C_{\max}\)가 얼마나 내려가는지 계산하는 것**이다.

그리고 그 최종적인 의미는 단순히 숫자 \(C\)를 예쁘게 만드는 것이 아니다.

\[
\boxed{
C_{\max}\downarrow
\quad\Longrightarrow\quad
\text{worst-case large-gap candidate count}\downarrow
\quad\Longrightarrow\quad
\text{9700X exact verification workload}\downarrow
}
\]

라는 연결을 만들어서, 궁극적으로

\[
10^{20}\rightarrow10^{26}
\]

구간의 maximal prime-gap 검증을 **단순 exhaustive prime enumeration보다 훨씬 적은 CPU 계산량으로 수행할 수 있는 수론적 기반**을 만드는 것이다.
