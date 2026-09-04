# Sono/FMT H1a finite-\(r\) 적분 lemma

- 작성: 2026-09-04 KST
- 증거 수준: `PROJECT THEOREM / DIRECTED-INTERVAL + ANALYTIC PROOF`
- 결과: `SIV-06 CLOSED FOR INTEGER r >= 36`
- 전체 good-sieve-weight package: `OPEN`
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 contract:
  [`data/Sono_FMT_H1a_finite_r_integral_contract_v1.json`](data/Sono_FMT_H1a_finite_r_integral_contract_v1.json)

## 1. 결론부터

Maynard의 test-function 정의만 사용해 다음 유한 명제를 얻는다.

> **H1a 정리.** 모든 정수 \(r\ge36\)에 대해 Sono가 정의한 simplex 함수족
> \(\mathcal F_r\) 안에 함수 \(F\)가 존재하여
> \[
> \frac{J_r(F)}{I_r(F)}>\frac{\log r}{4r}
> \]
> 이 성립한다.

따라서 Sono가 (2.3)에서 사용하는 \(c_{I,J}=1/4\)의 **적분비 부분만큼은** 더 이상
“숨은 \(O(1/\log r)\) 상수를 모르는 상태”로 둘 필요가 없다. T1의 `SIV-06`을
\(r\ge36\)에서 explicit하게 닫을 수 있다.

그러나 이것은 다음을 뜻하지 않는다.

- FMT Theorem 6의 weight moment가 모두 수치화됐다는 뜻이 아니다.
- Sono의 \(u\) 상·하한에 남은 \(o(1)\)을 제거한 것이 아니다.
- FGKMT Hypothesis 1, PAP, UB, hypergraph covering, \(x\to X\) 변환을 닫은 것이 아니다.
- \(X_{\mathrm{cert}}\) 또는 실제 전역 최소 \(X_\star\)를 계산한 것이 아니다.

쉽게 말하면, 긴 증명 사슬에 있던 “적분비 톱니바퀴” 하나를 실제 숫자로 만든 것이다. 그
톱니바퀴가 맞물리는 나머지 축과 기어에는 아직 숫자가 빠져 있다.

## 2. 원문에서 바로 같다고 쓰면 안 되는 두 함수

[Maynard, *Dense Clusters of Primes in Subsets*](https://arxiv.org/abs/1405.2593)의
(7.10), (7.12)는 다음을 둔다. \(q=9/10\),

\[
T=r\log r,\qquad U=r^{-1/2},\qquad
f(t)=\frac{\psi(t/U)}{1+Tt},
\]

\[
F_1(t_1,\ldots,t_r)=\prod_{i=1}^r f(t_i),
\qquad
F(t_1,\ldots,t_r)=\psi\!\left(\sum_i t_i\right)F_1(t_1,\ldots,t_r).
\]

여기서 \(\psi:[0,\infty)\to[0,1]\)는 smooth·non-increasing이고, \([0,q]\)에서 1,
\([0,1]\) 밖에서 0이다.

- \(F_1\)은 좌표별 곱이라 적분을 정확히 1차원으로 분해할 수 있지만 simplex 밖에도 값이 있다.
- \(F\)는 \(\sum t_i\le1\)에 지지되므로 Sono의 \(\mathcal F_r\)에 들어가지만 좌표들이 결합된다.

Maynard (8.27)의 식은 정확히 \(J_r(F_1)/I_r(F_1)\)에 대한 asymptotic이다. Sono (2.3)는
simplex 함수족의 supremum을 요구한다. 따라서 “(8.27)이므로 곧바로 \(F\)에도 계수 \(1/4\)”라고
쓰면 중간의 concentration 이동이 빠진다. 아래 lemma는 그 이동을 유한 부등식으로 채운다.

Maynard의 앞선 논문 [*Small Gaps Between Primes*](https://arxiv.org/abs/1311.4600),
Section 7, (7.5)–(7.14)도 unrestricted product integral을 simplex로 옮길 때 같은 종류의
second-moment concentration을 사용한다.

## 3. exact product-core 식

다음을 둔다.

\[
A=\int_0^\infty f(t)^2\,dt,\qquad
B=\int_0^\infty f(t)\,dt.
\]

Fubini 정리와 곱구조만으로

\[
I_r(F_1)=A^r,\qquad J_r(F_1)=B^2A^{r-1},
\]

따라서

\[
\frac{J_r(F_1)}{I_r(F_1)}=\frac{B^2}{A}
\]

가 **오차항 없이 정확히** 성립한다. Maynard (8.24)–(8.27)은 이 \(A,B\)를 asymptotic하게
평가한다. H1a에서는 그 \(O\)-상수를 추측하는 대신 \(0\le\psi\le1\),
\(\psi|_{[0,q]}=1\), support \([0,1]\)만으로 양쪽을 직접 감싼다.

## 4. H1a finite-\(r\) certificate lemma

아래 원시함수를 사용한다.

\[
\begin{aligned}
A_-&=\frac{qU}{1+qTU}, & A_+&=\frac{U}{1+TU},\\
B_-&=\frac{\log(1+qTU)}{T},\\
C(z)&=\frac{\log(1+Tz)+(1+Tz)^{-1}-1}{T^2},\\
D_+&=\frac{1+TU-2\log(1+TU)-(1+TU)^{-1}}{T^3}.
\end{aligned}
\]

그러면 직접 적분으로

\[
A_-\le A\le A_+,\quad B\ge B_-,\quad
C(qU)\le \int tf(t)^2dt\le C(U),\quad
\int t^2f(t)^2dt\le D_+
\]

이다.

확률밀도 \(f(t)^2/A\)를 따르는 독립 확률변수 \(Y_1,\ldots,Y_{r-1}\)를 두고

\[
\mu_- = \frac{C(qU)}{A_+},\qquad
\mu_+ = \frac{C(U)}{A_-},\qquad
v_+ = \frac{D_+}{A_-}-\mu_-^2
\]

로 두면 \(\mu_-\le E[Y_i]\le\mu_+\), \(\operatorname{Var}(Y_i)\le v_+\)다.
또

\[
d=q-U-(r-1)\mu_+
\]

라 하자. \(d>0\)이면 Cantelli 부등식으로

\[
P\!\left(\sum_{i=1}^{r-1}Y_i\le q-U\right)
\ge \frac{d^2}{d^2+(r-1)v_+}.
\]

왼쪽 사건에서는 \(0\le t_r\le U\)인 동안 \(\sum_i t_i\le q\)이므로 바깥 cutoff
\(\psi(\sum t_i)=1\)이다. 따라서

\[
J_r(F)\ge B^2A^{r-1}
P\!\left(\sum_{i=1}^{r-1}Y_i\le q-U\right),
\qquad I_r(F)\le A^r,
\]

이고 다음 완전히 명시적인 하한을 얻는다.

\[
\boxed{
\frac{J_r(F)}{I_r(F)}\ge
\frac{B_-^2}{A_+}
\frac{d^2}{d^2+(r-1)v_+}
}
\tag{H1a.1}
\]

식 (H1a.1)에는 \(O\), \(o(1)\), \(\ll\), “sufficiently large”가 없다. 지정한 정수
\(r\)에서 모든 양의 분모와 부등식 방향을 interval arithmetic으로 검사할 수 있다.

## 5. 왜 \(r\ge36\)이면 충분한가

### 5.1 유한 구간 \(36\le r\le8103\)

`source/h1a_finite_r_integral.py`는 식 (H1a.1)을 60-decimal-place outward-rounded
`mpmath.iv`로 **8068개 정수 모두** 검사한다. 누락 없이

```text
36, 37, ..., 8103
```

을 확인한 결과 failure는 0이다. 가장 작은 directed relative margin lower endpoint는
\(r=36\)에서 0.025보다 크다. \(r=35\)에서는 이 특정 보수적 certificate가 target을 넘지
못한다. 이는 \(r=35\)에서 더 좋은 함수가 없다는 뜻이 아니다.

### 5.2 무한 꼬리 \(\log r\ge9\)

\(\ell=\log r\), \(s=TU=\sqrt r\,\ell\),

\[
c=\frac{2\log(q\ell)}{\ell}>0
\]

라 하자. 먼저

\[
\frac{B^2}{A}
\ge \frac{\log^2(1+qs)}{T}
>\frac{\ell}{4r}(1+c)^2.
\tag{H1a.2}
\]

\(\ell\ge9\)에서는 다음 단조 endpoint bound가 성립한다.

\[
(r-1)E[Y_i]<\frac{37}{45}\frac{501}{500},\qquad
q-U>\frac{71}{80},
\]

따라서 평균과 cutoff 사이 거리는 \(d>3/50\)이다. 또한

\[
(r-1)\operatorname{Var}(Y_i)
\le \frac{e^{-\ell}}{q\ell^2}+\frac{e^{-\ell/2}}{\ell}=:V.
\]

\(e^{9/2}>80\), \(\log18<2.9\), \(\log8.1>2\)와 각 항의 단조성을 쓴다.
구체적으로

\[
\frac{V}{2c}
=\frac{e^{-\ell}}{4q\ell\log(q\ell)}
+\frac{e^{-\ell/2}}{4\log(q\ell)}
\]

의 두 항은 \(\ell\ge9\)에서 각각 감소하고, \(\ell=9\)의 위 endpoint bound로

\[
\frac{V}{2c}
<\frac{1}{414720}+\frac{1}{640}
=\frac{649}{414720}
<\frac{9}{2500}
=\left(\frac{3}{50}\right)^2<d^2.
\]

따라서

\[
\frac{V}{d^2}<2c.
\]

따라서 Cantelli factor는

\[
P\ge\frac{1}{1+V/d^2}>\frac{1}{1+2c}>\frac{1}{(1+c)^2}.
\tag{H1a.3}
\]

(H1a.2)와 (H1a.3)을 곱하면 \(J_r(F)/I_r(F)>\ell/(4r)\)이다.
directed interval로 \(8103<e^9<8104\)도 확인하므로 이 해석적 꼬리는 모든 정수
\(r\ge8104\)를 덮는다. 유한 scan과 합쳐 모든 정수 \(r\ge36\)이 닫힌다.

## 6. 검증의 성격

자동 검증은 다음을 확인한다.

1. JSON contract가 \(X_{\mathrm{cert}}\)를 열지 않은 fail-closed 상태인지
2. \(36\le r\le8103\)의 8068개 정수를 하나도 건너뛰지 않았는지
3. 모든 directed interval lower bound가 target보다 엄격히 큰지
4. \(\log r=9\) 경계에서 해석적 tail에 사용한 수치 부등식이 모두 분리되는지
5. T1 `SIV-06`만 `EXPLICIT`으로 바뀌고 `SIV-11`, `FIN-05`는 계속
   `HARD_BLOCKER`인지

이 검증은 proof assistant나 독립 동료심사를 대신하지 않는다. 특히 project theorem을 외부
논문 결과로 인용하거나 “Sono 논문이 \(r_0=36\)을 제시했다”고 쓰면 안 된다. \(36\)은 이
프로젝트가 원문 정의에서 새로 도출한 **충분조건**이다.

## 7. Sono/FMT threshold에 미치는 실제 영향

Sono는

\[
r=\left\lfloor(\log x)^{1/5}\right\rfloor
\]

를 쓴다. H1a의 \(r\ge36\)만 놓고 보면

\[
x\ge \exp(36^5)=\exp(60{,}466{,}176)
\]

이면 이 적분비 gate는 통과한다. 이 \(x\)는 약 26,260,127자리다. 이 값이 큰 이유는
H1a bound가 보수적인 데 더해 \(r=(\log x)^{1/5}\) 변환이 작은 \(r\)도 폭발시키기 때문이다.

하지만 이 숫자를 \(X_{\mathrm{cert}}\)로 부르면 안 된다.

- 이는 Sono proof parameter \(x\)에 대한 **한 개 하위조건**일 뿐 최종 theorem variable
  \(X\)가 아니다.
- 다른 node가 더 큰 \(x\)를 요구할 수 있다.
- 모든 node를 닫은 뒤 arbitrary-\(X\) transfer와 유한 bridge를 따로 확인해야 한다.

즉 이번 결과는 “얼마나 더 소수를 계산해야 하는가”의 답이 아니라, 그 질문에 답하기 위해
필요한 증명 사슬 한 부분의 숫자를 처음으로 복원한 것이다.

## 8. 남은 H1 proof obligations

| 순서 | 남은 항목 | H1a 뒤에도 열린 이유 |
|---:|---|---|
| 1 | H1b: Proposition 6.1 constant ledger | 적분비와 별개로 weight moment의 \(O\)-상수·공통 cutoff가 없음 |
| 2 | H1c: Hypothesis 1/PAP | distribution theorem의 수치 상수·유효범위가 없음 |
| 3 | `SIV-05` | Sono의 \(u\) 식에는 \(J/I\) 외 moment 및 Mertens 오차도 들어감 |
| 4 | `SIV-09/10/11` | good event, secondary absorption, 전체 weight package가 미완성 |
| 5 | covering·transfer | sieve weight와 독립적인 root blocker |

다음 권장 gate는 H1b다. threshold calculator나 장시간 prime sweep은 여전히 선결조건을
충족하지 않는다.

## 9. 1차 자료

- James Maynard, *Dense Clusters of Primes in Subsets*, Compositio Mathematica 152 (2016),
  1517–1554, DOI
  [10.1112/S0010437X16007296](https://doi.org/10.1112/S0010437X16007296),
  arXiv:[1405.2593](https://arxiv.org/abs/1405.2593).
- James Maynard, *Small Gaps Between Primes*, Annals of Mathematics 181 (2015), 383–413,
  DOI [10.4007/annals.2015.181.1.7](https://doi.org/10.4007/annals.2015.181.1.7),
  arXiv:[1311.4600](https://arxiv.org/abs/1311.4600).
- Keiju Sono, *An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes*,
  Le Matematiche 80 (2025), 521–544, DOI
  [10.4418/2025.80.2.2](https://doi.org/10.4418/2025.80.2.2), 특히 (2.3), pp. 541–542.
