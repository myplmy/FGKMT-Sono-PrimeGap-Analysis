# 03 — Rigorous Local Li–π Certification as a Secondary Prime-Count Layer

## 연구 지위

**후보 C: 수학적 독창성은 가장 불확실하지만, 완전히 폐기하기 전에 엄격히 시험할 가치가 있는 분석적 후보.**

핵심 아이디어는

$$
D(x)=\operatorname{li}(x)-\pi(x)
$$

를 이용해 short interval의 실제 prime count

$$
N(x,h)=\pi(x+h)-\pi(x)
$$

에 대해 endpoint-by-endpoint 전역 오차를 사용하는 대신 **local variation**을 직접 하한/상한하여 rigorous count bound를 얻는 것이다.

그러나 short intervals의 explicit prime bounds는 이미 상당한 문헌이 존재하므로, $D$ identity 자체를 novelty로 주장할 수 없다. 논문이 되려면 **새롭고 재현 가능한 local bound construction이 실제 finite-range certification cost를 유의미하게 줄여야 한다.**

---

## 1. 기본 항등식

정의:

$$
D(x)=\operatorname{li}(x)-\pi(x).
$$

그러면

$$
\begin{aligned}
D(x+h)-D(x)
&=[\operatorname{li}(x+h)-\operatorname{li}(x)]\\
&\quad-[\pi(x+h)-\pi(x)].
\end{aligned}
$$

따라서

$$
\boxed{
D(x+h)-D(x)
=\Delta_h\operatorname{li}(x)-N(x,h).
}
$$

이 식은 정의에서 즉시 나온 exact identity다.

---

## 2. Q의 정식화

유한범위에서

$$
Q_{A,B}(h)
=
\min_{A\le x\le B}
[D(x+h)-D(x)].
$$

만약 rigorous하게

$$
Q_{A,B}(h)\ge q
$$

를 증명했다면 모든 $x\in[A,B]$에 대해

$$
D(x+h)-D(x)\ge q.
$$

위 exact identity로부터

$$
\boxed{
N(x,h)
\le
\Delta_h\operatorname{li}(x)-q.
}
$$

$Q\ge-q$라고 parameterize하면

$$
\boxed{
N(x,h)
\le
\Delta_h\operatorname{li}(x)+q.
}
$$

이다.

---

## 3. 정수성에 따른 정확한 rounding

$N$은 정수다.

### non-strict bound

$$
N\le R
$$

이면

$$
\boxed{N\le\lfloor R\rfloor.}
$$

### strict bound

$$
N<R
$$

이면

$$
\boxed{N\le\lceil R\rceil-1.}
$$

이 구분은 실제 certificate 생성 시 필수다.

---

## 4. 현재 목표에서 Q가 얼마나 강해야 하는가

$h=1856$, $x=10^{20}$이면

$$
\Delta_{1856}\operatorname{li}(10^{20})
\approx40.3025279206.
$$

따라서 빈 window를 직접 인증하려면

$$
N(x,1856)<1
$$

이 필요하고, 충분조건 중 하나는

$$
40.3025-q<1
$$

즉

$$
\boxed{q>39.3025\text{ 정도}}
$$

이다.

따라서 현재 사용했던

$$
Q\ge-280.6166...
$$

수준은 empty certificate와는 약 320 정도의 차이가 있다.

---

## 5. 왜 일반적인 global Li–π bound가 충분하지 않은가

RH를 가정한 Schoenfeld형 bound는 대략

$$
|\pi(x)-\operatorname{li}(x)|
\lesssim
\frac{\sqrt{x}\log x}{8\pi}
$$

형태다.

이를 두 endpoint에 단순 적용하면 local count에 매우 큰 error가 누적된다.

따라서 이 후보의 연구 질문은

$$
\boxed{
|D(x+h)-D(x)|
\text{를 endpoint difference 수준으로 직접 제어할 수 있는가?}
}
$$

이다.

---

## 6. 중요한 선행연구

short intervals의 prime count 자체는 이미 매우 깊게 연구되어 있다.

- Dudek–Grenié–Molteni: RH 조건 아래 explicit primes-in-short-interval bounds.
- Montgomery–Soundararajan: short intervals 내 prime fluctuation 연구.
- Baker–Harman–Pintz 및 후속 연구: unconditional short-interval prime existence.
- Harman 계열의 sieve: short-interval upper/lower bounds.

따라서 단순히 “Li와 $\pi$의 차이를 short interval에 적용했다”는 것은 novelty가 아니다.

새로워야 할 것은

$$
\boxed{
\text{특정 유한 범위 }[A,B]\text{에서 certificate로 검증 가능한 local lower bound 생성법}
}
$$

이다.

---

## 7. 제안하는 연구 방향

### 방향 C1 — Monotonicity partition

$[A,B]$를 finite cells로 분할하고 각 cell에서

$$
D(x+h)-D(x)
$$

의 derivative 또는 finite-difference 구조를 이용해 최소값을 endpoint 또는 제한된 내부점으로 환원한다.

### 방향 C2 — Explicit approximation remainder

$$
\Delta_h\operatorname{li}(x)
$$

를

$$
\frac h{\log x}
$$

+ explicit remainder로 전개하고 remainder를 interval arithmetic으로 인증한다.

### 방향 C3 — Hybrid analytic-combinatorial bound

분석적 lower bound와 wheel upper bound를 동시에 사용한다.

예:

$$
N(x,h)
\le
\min\left(
U_{Q}(x,h),U_{wheel}(x,h)
\right).
$$

이 자체는 elementary하지만, 어느 영역에서 어느 bound가 더 강한지 자동으로 선택하는 certificate를 설계할 수 있다.

---

## 8. 기본 가정

### A1. 정확한 $\operatorname{li}$ 계산 또는 rigorous interval arithmetic

floating-point 근사값만으로 theorem을 만들면 안 된다.

### A2. Q lower bound가 rigorous

sampling minimum은 부족하다.

### A3. endpoint convention 고정

$\pi(x+h)-\pi(x)$가 $(x,x+h]$를 센다는 정의를 끝까지 유지한다.

### A4. 모든 numeric constants에 error enclosure 존재

예:

$$
L\le Q_{A,B}(h)\le U.
$$

그리고 증명에는 정확한 방향의 bound만 사용한다.

---

## 9. 학술지 수준으로 올리기 위한 핵심 조건

### 조건 C1 — 새로운 explicit local bound

최소한 다음 중 하나를 달성해야 한다.

1. 기존 공개 bound보다 명백히 작은 error term
2. 동일 bound를 훨씬 넓은 finite range에서 검증 가능한 형태
3. 기존 theorem보다 계산하기 쉬우면서도 rigorous한 certificate form

### 조건 C2 — 실제 prime-gap problem에서 nontrivial payoff

단순히 $N\le320$이 아니라

$$
N\le1
$$

또는

$$
N\le c
$$

with a genuinely useful small $c$가 나와야 한다.

### 조건 C3 — 독립된 exact verification과 비교

Q가 줄인 candidate 수와 Q 계산비용을 모두 측정한다.

---

## 10. 가장 중요한 실험

다음 세 방법을 비교한다.

### C0

no-Li baseline.

### C1

Li only.

### C2

Li + rigorous Q.

각각에 대해

$$
N_{undecided},
\quad
T_{analytic},
\quad
T_{exact},
\quad
T_{total}
$$

을 측정한다.

핵심 지표:

$$
\boxed{
\Delta T=T_{baseline}-T_{hybrid}
}
$$

및

$$
\boxed{
\text{analytic overhead}/\text{saved exact work}
}
$$

이다.

---

## 11. 이론 철폐 기준선

### Kill criterion C1 — bound가 유용하지 않음

$10^{20}$ 부근에서

$$
U_Q\gg1
$$

이고 실제 candidate reduction이 거의 없으면 이론의 computational role을 폐기한다.

### Kill criterion C2 — 기존 theorem이 더 강함

기존 explicit short-interval theorem이 같은 조건에서 더 강하거나 단순하면 신규 local-Q theorem을 철회한다.

### Kill criterion C3 — 계산비용 역전

$$
T_{analytic}\ge T_{saved exact}
$$

이면 algorithmic layer로서 폐기한다.

### Kill criterion C4 — finite numerical proof의 취약성

Q 계산이 높은 정밀도 floating-point에 의존하고 독립 interval verification이 불가능하면 논문용 theorem에서 제거한다.

---

## 12. 성공 기준

최소 성공 조건은

$$
\boxed{
\text{rigorous}
+\text{reproducible}
+\text{strictly tighter than baseline}
}
$$

이다.

강한 성공은

$$
\boxed{
U_Q<1
}
$$

을 finite nontrivial range에서 달성하는 것이다.

다만 이 수준이 불가능하더라도

$$
U_Q\ll U_{wheel}
$$

이면서 계산비용이 낮으면 secondary layer로는 살아남을 수 있다.

---

## 13. 현재 판정

이 후보는 수학적으로 올바른 기반을 갖지만 세 후보 중 novelty risk가 가장 크다.

이유는 short-interval prime theory 자체가 이미 깊게 연구되었기 때문이다.

따라서 다음 결과가 나오지 않으면 논문 핵심에서 철회한다.

$$
\boxed{
\text{새로운 finite-range local bound}
}
$$

또는

$$
\boxed{
\text{기존 결과보다 실질적으로 강한 certificate-compression payoff}
}
$$

둘 다 없으면 이 부분은 보조 알고리즘으로만 남긴다.

---

## 14. 최종 연구 판단

이 후보의 가치 순서는 다음과 같다.

1. **새 explicit local bound theorem** — 가장 강함
2. **같은 bound의 독립적 machine-checkable certificate** — 강함
3. **단순 Li/Q heuristic** — 논문 novelty로 부족
4. **$h/\log x$ approximation만 사용** — theorem으로 불충분

---

## 주요 참고문헌

- Dudek, Grenié, Molteni, *Primes in explicit short intervals on RH*, 2015.
- Montgomery, Soundararajan, *Primes in short intervals*, 2004.
- Baker, Harman, Pintz, 및 후속 short-interval prime-existence 연구.
- Harman 및 후속 short-interval sieve 연구.
