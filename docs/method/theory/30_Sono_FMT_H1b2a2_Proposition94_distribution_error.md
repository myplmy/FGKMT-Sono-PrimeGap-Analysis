# Sono/FMT H1b-2a.2: Proposition 9.4 식 (9.52) distribution error

- 작성일: 2026-09-08
- 증거 수준: `ACTUAL-APPLICATION PARAMETERIZED EXPLICIT PROJECT LEMMA`
- 대상: Maynard Proposition 9.4 식 (9.52)의 \(E_q^{(1)}\) contribution
- 기계 계약:
  [`Sono_FMT_H1b2a2_Proposition94_distribution_error_v1.json`](data/Sono_FMT_H1b2a2_Proposition94_distribution_error_v1.json)
- 구현: `source/h1b2a2_proposition94_distribution.py`
- 회귀시험: `tests/test_h1b2a2_proposition94_distribution.py`
- 비판적 검토:
  [`H1b-2a.2 타당성검토`](../../review/36_20260908_H1b2a2_Proposition94_distribution_타당성검토.md)

## 1. 결론

Maynard의 일반 Proposition 9.4는 식 (9.52)의 분포 오차를 “Proposition 9.1과 동일한
논증”으로 생략한다. 일반 집합 \(\mathcal A\)에서는 이 논증에 Hypothesis 1(1)의 평균
discrepancy와 Hypothesis 1(3)의 pointwise bound가 들어간다.

그러나 FGKMT/FMT의 **실제 호출**은

\[
\mathcal A=\mathbb Z,\qquad D=1,\qquad
\xi=\frac{\theta}{10}
\tag{30.1}
\]

이다. 이때 \(\mathcal A(x)\)는 연속된 정수 interval이므로 모든 \(q,a\)에 대해

\[
\boxed{E_q^{(1)}\le1}
\tag{30.2}
\]

이 정확히 성립한다. 따라서 이 **P94 distribution child 하나**는 Hypothesis 1의 알 수 없는
Vinogradov multiplier를 쓰지 않고 직접 유한 상계할 수 있다.

이번 단계는 다음 상태 전이를 정당화한다.

~~~text
H1B2A-P94-DISTRIBUTION
  INPUT_PACKAGE_MISSING
  -> ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT
~~~

반면 다음은 승격하지 않는다.

~~~text
H1B-P94       RATE_MISSING
H1B-COMP-01   HARD_BLOCKER
SIV-07/08/09  HARD_BLOCKER
X_cert        OPEN
~~~

이유는 P94의 이미 닫힌 여러 주항 package를 아직 **하나의 end-to-end multiplier와 공통
cutoff**로 합치지 않았고, Proposition 9.2의 prime moment에는 여전히 Hypothesis 1(2)의
수치 prime-distribution package가 필요하기 때문이다.

## 2. 쉽게 설명하면

원문의 일반 논증은 “임의의 도시에서 여러 도로의 차량 수가 평균과 얼마나 다른지”를
추정해야 한다. 그래서 분포 정리의 숨은 상수가 필요하다.

하지만 실제 FGKMT 호출의 \(\mathcal A\)는 구멍 없는 연속 정수들이다. 연속된 집 번호를
\(q\)개 줄에 차례로 나누면 어느 줄도 평균보다 한 개 이상 차이 날 수 없다. 이것이
  \(E_q^{(1)}\le1\)이다. 따라서 이 한 오류항에는 어려운 소수분포 정리를 끌어올 필요가 없다.

다만 이는 **정수 \(n\)의 분포**에 관한 이야기다. \(L(n)\)이 소수인 경우의 분포는 전혀
다른 문제이므로, Hypothesis 1(2)와 H1c-1은 그대로 남는다.

## 3. 원천과 선행증명 우선 조사

### 3.1 직접 원천

1. James Maynard,
   [*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
   *Compositio Mathematica* 152 (2016), 1517--1554; arXiv:1405.2593.
   - Hypothesis 1: pp.1519--1520
   - Proposition 9.1, (9.1)--(9.3): pp.1538--1539
   - Proposition 9.4, (9.49)--(9.53): pp.1547--1548
2. Kevin Ford, Ben Green, Sergei Konyagin, James Maynard, Terence Tao,
   [*Long Gaps Between Primes*](https://doi.org/10.1090/jams/876),
   *J. Amer. Math. Soc.* 31 (2018), 65--105; arXiv:1412.5029.
   - Lemma 7.2의 \(\mathcal A=\mathbb Z,\theta=1/3\): pp.96--97
   - Theorem 6과 Proposition 9.4 호출 \(D=1,\xi=\theta/10\): pp.98--99
3. J. Barkley Rosser and Lowell Schoenfeld,
   [*Approximate Formulas for Some Functions of Prime Numbers*](https://doi.org/10.1215/ijm/1255631807),
   *Illinois J. Math.* 6 (1962), 64--94, Theorem 15.

최종 출판본과 Maynard arXiv v2 author TeX를 함께 대조했다. author TeX에서 관련 위치는
Hypothesis 1 lines 67--76, Proposition 9.1 lines 671--694, Proposition 9.4 lines
1044--1074와 1088--1099다. 파일 hash는 기계 계약에 고정했다.

여기서 source-version 차이 하나를 발견했다. author TeX line 1090은 Möbius inversion 합의
조건을 `r_0|d_0`로 적지만, 그러면 바로 뒤의 \(\widetilde\lambda_1\) 전 범위 합과 모순된다.
최종 출판본 (9.56)은 올바르게 `d_0|r_0`로 고쳤다. 이 프로젝트는 최종 출판본을 정본으로
삼고 아래 증명도 `d_0|r_0`를 사용한다.

### 3.2 표적 선행연구 검색 판정

Maynard arXiv:1405.2593, FGKMT arXiv:1412.5029, D.H.J. Polymath
arXiv:1407.4897과 출판본을 표적 조사했다. 같은 실제 호출에 대해 아래의 모든 multiplier와
finite cutoff를 인쇄한 drop-in 정리는 확인하지 못했다. 이는 전 세계 문헌에 없다는 주장이나
novelty 주장이 아니다.

따라서 원문의 구조를 바꾸지 않고, \(\mathcal A=\mathbb Z\)에서만 가능한 exact discrepancy와
앞 단계에서 이미 증명한 finite envelope를 연결한다.

## 4. 원문의 생략된 일반 논증

Proposition 9.1에서

\[
q=W\prod_{i=1}^k[d_i,e_i]
\]

를 고정하면 각 자유 소수는 좌표 \(i\)와 `d only / e only / both` 중 하나를 고른다.
원문은 이를 \(O(\tau_{3k}(q))\)로 쓰고,

\[
\sum_q\tau_{3k}(q)E_q^{(1)}
\]

에 Cauchy--Schwarz를 적용한다. 한 인자에는 Hypothesis 1(3)의
\(E_q^{(1)}\ll\#\mathcal A(x)/q\), 다른 인자에는 Hypothesis 1(1)의 평균 오차를 쓴다.

Proposition 9.4에서는 좌표가 \(0,1,\ldots,k\)로 하나 늘고

\[
q=V\prod_{i=0}^k[d_i,e_i],qquad
q<VR^2x^{2\xi}<x^\theta
\tag{30.3}
\]

가 된다. 원문은 이 부분을 “동일한 논증”이라고만 기록한다.

## 5. 실제 \(\mathcal A=\mathbb Z\) discrepancy

\(N\)개의 연속 정수로 된 interval \(I\)를 고정한다. \(N=mq+r\),
\(0\le r<q\)로 나누면 각 residue class에는 \(m\)개 또는 \(m+1\)개가 들어간다. 따라서

\[
\left|\#\{n\in I:n\equiv a\pmod q\}-\frac Nq\right|
\le\max\left\{\frac rq,1-\frac rq\right\}\le1.
\tag{30.4}
\]

Maynard의 half-open \([x,2x)\)와 FGKMT 본문의 endpoint 표기 중 어느 것을 쓰더라도
연속 정수 interval이라는 성질은 같다. \(x\ge2\)이면 보수적으로

\[
N=\#\mathcal A(x)\ge\frac x2
\tag{30.5}
\]

도 쓸 수 있다.

## 6. 숨은 상수가 없는 tuple multiplicity

### 6.1 고정 \(q\)의 경우의 수

support 때문에 모든 관련 수는 squarefree이고, 서로 다른 좌표의 \(d_ie_i\)는 서로소다.
고정된 \(q\)에서 \(V\) 밖의 각 소수는

1. \(k+1\)개 좌표 중 하나,
2. 그 좌표에서 \(d_i\)만, \(e_i\)만, 또는 양쪽

을 고른다. 자유 소수가 \(\omega\)개이면 경우의 수는 최대

\[
[3(k+1)]^\omega.
\]

squarefree \(q\)에 대해 \(\tau_a(q)=a^{\omega(q)}\)이므로, \(V\)의 고정 소수까지
과대계수하면

\[
\boxed{
\#\{(d_0,e_0,\mathbf d,\mathbf e)\mapsto q\}
\le\tau_{3(k+1)}(q).
}
\tag{30.6}
\]

여기에는 숨은 \(O(1)\) multiplier가 없다.

### 6.2 divisor-sum 상계

정수 \(a\ge1\), 실수 \(Q>1\)에 대해 \(\tau_a(q)\)는 곱이 \(q\)인 순서 있는
양의 정수 \(a\)-tuple 수다. 따라서

\[
\begin{aligned}
\sum_{q<Q}\tau_a(q)
&=\#\{(n_1,\ldots,n_a):n_1\cdots n_a<Q\}\\
&\le Q\sum_{n_1,\ldots,n_a<Q}\frac1{n_1\cdots n_a}\\
&\le Q(1+\log Q)^a.
\end{aligned}
\tag{30.7}
\]

## 7. coefficient와 modulus의 finite envelope

이 절에서는

\[
y=\log x,\qquad z=x^\xi,\qquad s=\xi\log x
\]

로 둔다.

### 7.1 \(\lambda_{\mathbf d}\)

Theory 28과 predecessor smooth gate에서

\[
|\lambda_{\mathbf d}|\le
M_{620}\left(\frac{\log R}{k}\right)^k,qquad M_{620}\le e
\tag{30.8}
\]

가 이미 증명됐다.

### 7.2 \(\widetilde\lambda_{d_0}\)

Maynard 최종 출판본 (9.56)의 Möbius inversion과
\(\widetilde y_{r_0}=W_0/\phi(W_0)\)에서

\[
\widetilde\lambda_{d_0}
=\mu(d_0)d_0\sum_{d_0\mid r_0}
\frac{\widetilde y_{r_0}}{\phi(r_0)}.
\]

\(r_0\le z\), \(1/\phi(r_0)\le1\), \(d_0\)의 배수 개수 \(\le z/d_0\)를 쓰면

\[
\boxed{
|\widetilde\lambda_{d_0}|\le C_0z,qquad
C_0=\frac{W_0}{\phi(W_0)}.
}
\tag{30.9}
\]

Theory 27의 predecessor sharp gate는 동시에

\[
\boxed{\widetilde\lambda_1\ge\frac{s}{2}>0}
\tag{30.10}
\]

를 준다.

### 7.3 \(V,W_0,q\)

\(V=\prod_{p\le2k^2}p\)이고 기존 explicit \(\vartheta\) 상계에서

\[
\log V<4k^2.
\tag{30.11}
\]

실제 \(D=1\), \(|a_i|,|b_i|\le x^\alpha\)에서

\[
\Delta_L\le2^kx^{\alpha(2k+1)},
\]

따라서

\[
\log W_0<\Lambda_0(y):=
4k^2+k\log2+\alpha(2k+1)y.
\tag{30.12}
\]

\(k\ge36\)이면 \(W_0\ge V>210\)이다. Rosser--Schoenfeld Theorem 15와
\(e^\gamma<3\), \(\log\log W_0>1\)에서

\[
\boxed{
C_0< C_\phi(y):=3\log\Lambda_0(y)+2.50637.
}
\tag{30.13}
\]

또 \(R\le x^{\theta/3}\), \(\xi=\theta/10\)이므로

\[
\log q< L_Q(y):=4k^2+\frac{13\theta}{15}y.
\tag{30.14}
\]

특히

\[
y\ge\frac{30k^2}{\theta}
\tag{30.15}
\]

이면 (30.11)의 strict inequality 덕분에 \(q<x^\theta\)가 된다.

## 8. 식 (9.52) 오류의 전체 상계

### 8.1 한 residue class

식 (9.52)의 절댓값을 취하고 (30.2), (30.6)--(30.10)을 적용한다.
\(a=3(k+1)\), \(Q=VR^2z^2\)라 두면, 한 \(v_0\pmod V\)에서 오류는

\[
\frac{4C_0^2z^2}{s^2}
M_{620}^2\left(\frac{\log R}{k}\right)^{2k}
Q(1+\log Q)^a
\tag{30.16}
\]

이하다.

### 8.2 모든 residue class

허용되는 \(v_0\)는 많아도 \(V\)개다. 따라서 전체 distribution error
\(\mathcal E_{94}\)는

\[
\boxed{
\mathcal E_{94}\le
\frac{4V^2C_0^2M_{620}^2R^2z^4}{s^2}
\left(\frac{\log R}{k}\right)^{2k}
(1+\log Q)^{3(k+1)}.
}
\tag{30.17}
\]

### 8.3 Proposition 9.4 표준 크기의 하한

Proposition 9.4 우변에서 implied multiplier를 제외한 표준 크기를

\[
T_{94}:=\xi^{-1}
\frac{\Delta_L}{\phi(\Delta_L)}
\frac D{\phi(D)}
\left(\frac B{\phi(B)}\right)^k
\mathfrak S_B(\mathcal L)\#\mathcal A(x)
(\log R)^{k-1}I_k(F)
\]

라 하자. Theory 17과 28의 finite lemma,
\(n/\phi(n)\ge1\), (30.5)에서

\[
T_{94}\ge
\frac{x}{2\xi}(\log R)^{k-1}
e^{-9k/2}(2k\log k)^{-k}.
\tag{30.18}
\]

### 8.4 명시적 상대오차

(30.17)을 (30.18)로 나누면

\[
\frac{\mathcal E_{94}}{T_{94}}\le\rho_{94},
\tag{30.19}
\]

\[
\rho_{94}:=
\frac{8V^2C_0^2M_{620}^2R^2z^4}{x\xi y^2}
e^{9k/2}2^k\left(\frac{\log k}{k}\right)^k
(\log R)^{k+1}(1+\log Q)^{3(k+1)}.
\tag{30.20}
\]

이다. 이제 \(M_{620}\le e\), (30.11)--(30.14),
\(\log R\le\theta y/3\)을 넣고

\[
\beta:=1-\frac{16\theta}{15}>0
\tag{30.21}
\]

라 두면 다음 완전히 명시적인 log 상계를 얻는다.

\[
\boxed{
\begin{aligned}
\log\rho_{94}\le{}&
\log8+8k^2+2\log C_\phi(y)+2-\beta y
-\log(\theta/10)-2\log y\\
&+\frac{9k}{2}+k\log2+k\log\log k-k\log k\\
&+(k+1)\log(\theta y/3)
+3(k+1)\log(1+L_Q(y)).
\end{aligned}
}
\tag{30.22}
\]

## 9. closed-form 충분조건

\[
A_0=4k^2+k\log2,qquad B_0=\alpha(2k+1),
\]

\[
a=3(k+1),qquad m=4(k+1)
\]

로 둔다. \(y\ge1\)이면

\[
\Lambda_0(y)\le(A_0+B_0)y,
\]

\[
C_\phi(y)\le6\log\Lambda_0(y),
\]

\[
1+L_Q(y)\le
\left(1+4k^2+\frac{13\theta}{15}\right)y.
\]

따라서 (30.22)는

\[
\boxed{
\log\rho_{94}\le C(k,\alpha,\theta)+m\log y-\beta y
}
\tag{30.23}
\]

로 약화할 수 있다. 여기서 코드와 기계 계약의 \(C\)는

\[
\begin{aligned}
C={}&\log8+8k^2+2+\frac{9k}{2}
+k(\log2+\log\log k-\log k)-\log(\theta/10)\\
&+2\log6+2\log\{1+\log(A_0+B_0)\}\\
&+3(k+1)\log\left(1+4k^2+\frac{13\theta}{15}\right).
\end{aligned}
\tag{30.24}
\]

다음은 (30.23)을 0 이하로 만드는 닫힌 충분조건이다.

\[
Y_{\rm an}:=\max\left\{
1,
\frac{2\max(0,C)}\beta,
\frac{4m}\beta\log\frac{4m}\beta
\right\}.
\tag{30.25}
\]

실제로 첫 두 항에서 \(C\le\beta y/2\)다. \(A=2m/\beta\)라 두면
\(y\ge2A\log(2A)\)에서 \(m\log y\le\beta y/2\)이고, 그 뒤에는
우변 차이가 증가한다. 따라서 \(y\ge Y_{\rm an}\)이면 \(\rho_{94}\le1\)이다.

predecessor gate를 함께 넣은 최종 충분조건은

\[
\boxed{
Y_{94}:=\max\left\{
\log2,
\frac{30k^2}{\theta},
\frac{10Y_{\rm smooth}}\theta,
\frac{10Y_{\rm sharp}}\theta,
Y_{\rm an}
\right\}.
}
\tag{30.26}
\]

\(\log x\ge Y_{94}\)이면 theorem range의
\(\log R\ge(\theta/10)\log x\)가 두 predecessor gate를 만족시키고,
modulus gate와 (30.22)의 직접검산도 모두 통과한다.

## 10. 설명용 실제 매개변수 진단

\(k=36,\alpha=2,\theta=1/3\)을 넣은 100-dps 비방향반올림 진단은

\[
Y_{94}\approx3.5227436105710286298\times10^{133},
\]

\[
\log_{10}x\approx1.5299081112309355970\times10^{133},
\]

\[
\log\rho_{94}(Y_{94})
\lesssim-2.2702125490346628947\times10^{133}
\]

를 준다. 이 값은 새 distribution 흡수식이 아니라 이미 있던 매우 보수적인
\(Y_{\rm smooth}\)가 지배한다.

이 숫자는 다음 중 어느 것도 아니다.

- Sono의 \(X_{\rm cert}\)
- 실제 maximal-gap 부등식의 최초 성립점
- Proposition 6.1 전체의 시작점
- 계산해야 할 prime-search 범위

고정된 \(k\)에서 한 하위 component의 충분조건을 확인한 설명용 진단일 뿐이다. 숫자 계산은
`mpmath`라 directed-rounding certificate도 아니다. 증명은 (30.2)--(30.26)의 symbolic
부등식이다.

## 11. 이번 정정이 H1c에 미치는 영향

기존 문서에는 P94 식 (9.52)가 Hypothesis 1(1),(3)의 numerical multiplier를 기다린다고
기록돼 있었다. 일반 Proposition에는 맞지만 실제 FGKMT 호출에는 지나치게 강한 요구였다.

정정된 의존관계는 다음과 같다.

~~~text
A=Z exact interval count
  -> P94 equation-(9.52) distribution child finite

Hypothesis 1(2) quantitative prime distribution
  -> P92 prime moment and full good-weight package (still OPEN)
~~~

Hypothesis 1(1),(3)의 정본 상태 자체는 `EXACT_SUFFICIENT_REDUCTION`으로 유지한다. 다른 일반
호출까지 무조건 닫혔다고 바꾸지 않는다.

## 12. 자동 검증 범위

새 회귀시험은 다음을 확인한다.

1. 여러 음수·양수 endpoint, modulus, residue에서 exact count와 (30.4) 전수 대조
2. toy 자유 소수 assignment 수가 정확히 \([3(k+1)]^\omega\)인지 확인
3. 작은 \(Q,a\)에서 (30.7)을 brute-force tuple count와 대조
4. \(k=36,100\), \(\alpha=2,\theta=1/3\)에서 (30.26)과 직접 (30.22) 동시 통과
5. 작은 \(\log x\), 잘못된 \(k,\theta\)에서 fail closed
6. source hash와 parent non-promotion 상태 고정

이 시험은 논문 전체나 Sono 정리를 컴퓨터가 증명한다는 뜻이 아니다.

## 13. 다음 gate

가장 가까운 후속은 `H1b-2a.3`이다. 지금까지 닫힌 P94의 smooth/sharp, Euler,
distribution package를 한 번만 세어 **단일 total multiplier와 공통 cutoff**로 합성해야 한다.
그 뒤에야 `H1B-P94` 상태 승격 여부를 판단할 수 있다.

병렬 이론축인 `H1c-1`은 여전히 중요하다. 다만 그 prime-distribution package는 이제 P94
식 (9.52) 때문이 아니라 Proposition 9.2와 전체 good-weight theorem 때문에 필요하다.

## 14. 2026-09-08 H1b-2a.3 후속 상태

13절은 이 distribution child만 닫힌 시점의 이력이다. 후속
[`H1b-2a.3`](31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md)은
\(\rho_{94}\)를 main multiplier에 곱하지 않고 additive error로 더했으며, P94 전용 강화
smooth gate와 다른 모든 child cutoff를 공통 최댓값으로 합성했다. 이에 따라 actual
FGKMT/FMT `H1B-P94`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 승격됐고,
균일한 actual-call multiplier 13을 얻었다.

일반 \(\mathcal A\) P94와 Proposition 9.2의 Hypothesis 1(2)는 이 결과로 닫히지 않는다.
따라서 `H1B-COMP-01`, `SIV-07/09`, \(X_{\rm cert}\)는 그대로 열린다.
