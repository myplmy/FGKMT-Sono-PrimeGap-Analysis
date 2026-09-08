# Sono/FMT H1b-2a.1 Proposition 9.4 exact Euler normalization

- 작성일: 2026-09-08
- 상위 obligation: H1B-P94, H1B-COMP-01, SIV-07
- 선행 정본: [H1b-2a 잔여 moment/error package](28_Sono_FMT_H1b2a_residual_moment_error_package.md)
- 기계 계약: [Sono_FMT_H1b2a1_Proposition94_Euler_normalization_v1.json](data/Sono_FMT_H1b2a1_Proposition94_Euler_normalization_v1.json)
- 구현: source/h1b2a1_proposition94_euler.py
- 비판적 검토: [H1b-2a.1 타당성 검토](../../review/35_20260908_H1b2a1_Proposition94_Euler_타당성검토.md)

## 1. 결론

Maynard Proposition 9.4의 최종 출판본 식 (9.61)에 남아 있는 정확한 denominator

\[
g_*(p,m)=\frac{(p-m)^2}{p+m-2},
\qquad m=\omega^*(p)
\tag{29.1}
\]

에서 출발해, 식 (9.66)의 두 Euler 곱을 O-표기 이전의 유리함수로 복원했다.
모든 정수 \(k\ge36\)에서

\[
\boxed{
P_0\le e^{2/k},
\qquad
P_{\rm can}\le e^2\mathfrak S_{WB}(\mathcal L)^{-1}.
}
\tag{29.2}
\]

따라서 식 (9.66)에 표시된 마지막 두 곱은

\[
\boxed{
P_0P_{\rm can}
\le e^{2+2/k}\mathfrak S_{WB}(\mathcal L)^{-1}.
}
\tag{29.3}
\]

식 (9.64)에서 식 (9.65)로 갈 때 숨겨진 앞쪽 곱이 제곱되는 것까지 포함하면 전체
Euler-normalization multiplier는

\[
\boxed{
M_{\rm Euler}(k)
\le e^{2+6/k}\mathfrak S_{WB}(\mathcal L)^{-1}.
}
\tag{29.4}
\]

이다. \(k=36\)에서는 \(e^{13/6}\approx8.72914\)다. 이 수치는 설명용 근삿값이며
directed-rounding certificate가 아니다.

이에 따라 H1B2A-P94-FINAL-EULER는 PROJECT_FINITE_COMPONENT_CLOSED로
이동한다. 그러나 식 (9.52)의 distribution error가 열려 있으므로 H1B-P94는
RATE_MISSING, SIV-07은 HARD_BLOCKER, \(X_{\rm cert}\)는 OPEN으로 유지한다.

## 2. 쉽게 설명하면

원문은 복잡한 소수별 곱을 마지막에 “어떤 고정 상수 이하”라고 줄여 쓴다. 무한히 큰
범위의 정리를 증명할 때는 충분하지만, “정확히 얼마부터 성립하는가”를 계산하려면 그
고정 상수의 숫자가 필요하다.

이번 작업은 원문이 줄이기 직전의 분수를 다시 꺼내 소수 하나마다 비교한 것이다.
각 소수에서 생기는 작은 초과량을 모두 더해도 수렴하며, 가장 보수적으로 세어도
전체 multiplier가 식 (29.4)를 넘지 않음을 증명했다.

다만 엔진 전체가 완성된 것은 아니다. 비유하면, 배관 끝의 두 연결부에서 새는 양을
숫자로 막았지만, 앞쪽의 “소수가 등차수열에 얼마나 고르게 놓이는가”라는 큰 밸브의
수치 보증이 아직 없다.

## 3. 원천과 위치 정정

주 원천은 James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
Compositio Mathematica 152 (2016), 1517--1554; [arXiv:1405.2593](https://arxiv.org/abs/1405.2593)다.

- 최종 출판본 pp.1547--1550: Proposition 9.4, 식 (9.49)--(9.70)
- author TeX lines 1076--1149: \(\omega^*\), exact denominator, 두 Euler 곱
- 정의부 lines 376--407: \(\omega,\phi_\omega,\mathfrak S_D,W,W_i\)
- Lemma 8.4 lines 542--604: Euler main product \(\Pi_g\)

기존 프로젝트 문서는 편의상 “식 (9.63)의 첫 곱”, “식 (9.67)의 마지막 두 곱”이라고
불렀다. 출판본을 시각 재확인하면 정확한 displayed 위치는 다음과 같다.

| 대상 | 정확한 위치 | 다음 식의 역할 |
|---|---|---|
| \(C_{\rm pre}\) | 식 (9.64) | 식 (9.65)에서 O(1)로 흡수 |
| \(P_0,P_{\rm can}\) | 식 (9.66) | 식 (9.67)에서 O(1), \(O(\mathfrak S^{-1})\)로 흡수 |

수식 자체에 대한 이전 판단은 유지되고, 식 번호만 바로잡는다.

공식 출판본·arXiv v2와 같은 Maynard weight를 사용하는
[Mastrostefano, arXiv:1804.06290](https://arxiv.org/abs/1804.06290)을 표적 검색했으나,
이 두 곱을 수치 상수로 대신 닫아 주는 정식 결과는 확인하지 못했다. 이는 확인한
1차 자료 범위의 판정이지 전 세계 문헌에 없다는 주장이나 novelty 주장이 아니다.

## 4. 정확한 입력

원문의 정의에서

\[
\omega(p)=
\begin{cases}
\#\{n\bmod p:\prod_{i=1}^kL_i(n)\equiv0\pmod p\},&p\nmid B,\\
0,&p\mid B,
\end{cases}
\tag{29.5}
\]

이고

\[
\mathfrak S_{WB}(\mathcal L)
=\prod_{p\nmid WB}
\left(1-\frac{\omega(p)}p\right)
\left(1-\frac1p\right)^{-k}.
\tag{29.6}
\]

추가 선형식 \(L\)을 넣은 root count는

\[
\omega^*(p)=
\begin{cases}
\omega(p),&p\mid\Delta_L,\ p\nmid B,\\
\omega(p)+1,&p\nmid\Delta_L,\ p\nmid B,\\
1,&p\mid B.
\end{cases}
\tag{29.7}
\]

이다. \(V=\prod_{p\le2k^2}p\), \(W_0=DV\Delta_L\)이고
\(W=\prod_{p\le2k^2,p\nmid B}p\)이므로

- \(p\nmid W_0\)이면 \(p>2k^2\),
- \(p\nmid WB\)이면 \(p>2k^2\),
- \(0\le\omega(p)\le k\), \(0\le\omega^*(p)\le k+1\)

이다.

## 5. 식 (9.64)의 앞쪽 곱

식 (9.63)의 crude bound 안의 double sum을 소수별로 세면 식 (9.64)의 첫 곱은 정확히

\[
C_{\rm pre}
=\prod_{p\nmid WB}
\left(1+\frac{\omega(p)}{(p-1)(p-\omega(p))}\right).
\tag{29.8}
\]

이다. 이 곱을 그대로 보존하면 식 (9.65)의 Vinogradov 기호 대신

\[
|y_{\mathbf r,r_0}|
\le C_{\rm pre}y_{\mathbf r}\widetilde y_{r_0}L(\mathbf r,r_0)
\tag{29.9}
\]

를 쓸 수 있다. 여기서 원문 (9.65)의 두 local product를 합친
\(L(\mathbf r,r_0)\)는 각 인자가 1 이하이므로

\[
|y_{\mathbf r,r_0}|\le C_{\rm pre}y_{\mathbf r}\widetilde y_{r_0}.
\tag{29.10}
\]

또 \(p>2k^2\), \(0\le\omega\le k\)에서

\[
0\le
\frac{\omega}{(p-1)(p-\omega)}
\le\frac{4k}{p^2}.
\tag{29.11}
\]

\(\log(1+t)\le t\)와
\(\sum_{n>2k^2}n^{-2}\le(2k^2)^{-1}\)를 적용하면

\[
\boxed{C_{\rm pre}\le e^{2/k}.}
\tag{29.12}
\]

식 (9.61)의 제곱합에서는 반드시 \(C_{\rm pre}^2\le e^{4/k}\)를 쓴다.

## 6. 양의 합의 분리

식 (9.61)의 exact reciprocal denominator는

\[
h_*(p,m)=\frac1{g_*(p,m)}
=\frac{p+m-2}{(p-m)^2}.
\tag{29.13}
\]

(29.10)을 제곱하고 양의 합에서 \((r_0,r)=1\) 조건을 버리면

\[
\sum_{\mathbf r,r_0}y_{\mathbf r,r_0}^2
\prod_{p\mid rr_0}h_*(p,\omega^*(p))
\le C_{\rm pre}^2 S_0S_{\rm can}.
\tag{29.14}
\]

여기서

\[
S_0=\sum_{\substack{r_0<x^\xi\\(r_0,W_0)=1}}
\widetilde y_{r_0}^2\prod_{p\mid r_0}h_*(p,\omega^*(p)),
\tag{29.15}
\]

\[
S_{\rm can}=\sum_{\mathbf r\in\mathcal D_k}
y_{\mathbf r}^2\prod_{p\mid r}h_*(p,\omega^*(p)).
\tag{29.16}
\]

이다. 조건을 버리는 것은 양의 항을 더 추가하는 상계이므로 multiplier가 새로 생기지 않는다.
sharp \(S_0\)와 smooth \(S_{\rm can}\)의 summation error는 각각 선행 theory 27과
theory 24에서 parameterized explicit하게 처리돼 있다. 이 문서는 그 main Euler factor만
복원한다.

## 7. 첫 번째 최종 곱 \(P_0\)

Lemma 8.4의 one-variable Euler factor와
\(\widetilde y_{r_0}=W_0/\phi(W_0)\)를 결합하면

\[
\Pi_0=\frac{\phi(W_0)}{W_0}P_0,
\qquad
P_0=\prod_{p\nmid W_0}
\left(1+\frac1{g_*(p,\omega^*(p))}\right)
\left(1-\frac1p\right).
\tag{29.17}
\]

\(p\mid B\)이면 \(\omega=0,\omega^*=1\)이라 local factor는 정확히 1이다.
\(p\nmid B\)이면 \(p\nmid W_0\)에서 \(p\nmid\Delta_L\)이므로
\(m=\omega+1\)이다. 직접 통분하면

\[
\boxed{
\left(1+\frac1{g_*(p,\omega+1)}\right)
\left(1-\frac1p\right)
=1+\frac{\omega(3p-\omega-3)}
{p(p-\omega-1)^2}.
}
\tag{29.18}
\]

\(k\ge36\), \(p>2k^2\)이면

\[
\frac{k+1}{p}<\frac{k+1}{2k^2}\le\frac1{10},
\qquad
p-\omega-1>\frac9{10}p.
\tag{29.19}
\]

따라서 (29.18)의 초과량은

\[
0\le\delta_0(p)
\le\frac{3kp}{p(9p/10)^2}
=\frac{100}{27}\frac{k}{p^2}
<\frac{4k}{p^2}.
\tag{29.20}
\]

그러므로 \(P_0\le e^{2/k}\)다.

## 8. 두 번째 최종 곱과 singular series

Lemma 8.4에서 각 \(p\nmid WB\)에 허용되는 좌표 수는 \(\omega(p)\)다. 따라서

\[
P_{\rm can}
=\prod_{p\nmid WB}
\left(1+\frac{\omega(p)}
{g_*(p,\omega^*(p))}\right)
\left(1-\frac1p\right)^k.
\tag{29.21}
\]

한편 (29.6)의 역수 local factor는

\[
\left(1+\frac{\omega}{p-\omega}\right)
\left(1-\frac1p\right)^k.
\tag{29.22}
\]

공통 마지막 인자를 없애고 비율을 계산한다.

### 8.1 \(p\mid\Delta_L\): 기존 root와 충돌

이때 \(\omega^*=\omega\)이고

\[
\boxed{
\frac{1+\omega/g_*(p,\omega)}
{1+\omega/(p-\omega)}
=1+\frac{2\omega(\omega-1)}{p(p-\omega)}.
}
\tag{29.23}
\]

### 8.2 \(p\nmid\Delta_L\): 새 root 하나

이때 \(\omega^*=\omega+1\)이고

\[
\boxed{
\frac{1+\omega/g_*(p,\omega+1)}
{1+\omega/(p-\omega)}
=1+\frac{\omega\{(2\omega+1)(p-\omega)-1\}}
{p(p-\omega-1)^2}.
}
\tag{29.24}
\]

두 경우 모두 비율은 1 이상이다. 충돌 경우에는
\(p-\omega>9p/10\)을 쓰고, 새 root 경우에는 \(\omega=0\)을 따로 처리한 뒤
\(2\omega+1\le3k\)와 (29.19)를 쓰면

\[
0\le\delta_{\rm can}(p)\le\frac{4k^2}{p^2}.
\tag{29.25}
\]

따라서

\[
\boxed{
P_{\rm can}
\le
\exp\left(4k^2\sum_{p>2k^2}\frac1{p^2}\right)
\mathfrak S_{WB}(\mathcal L)^{-1}
\le e^2\mathfrak S_{WB}(\mathcal L)^{-1}.
}
\tag{29.26}
\]

## 9. 임의 cutoff 뒤의 finite tail

정수 \(Y\ge2k^2\)에 대해

\[
\sum_{p>Y}\frac1{p^2}
\le\sum_{n>Y}\frac1{n^2}
\le\int_Y^\infty\frac{dt}{t^2}
=\frac1Y.
\tag{29.27}
\]

그러므로 실제 linear forms의 \(\omega(p)\)를 유한한 \(p\le Y\)에서 exact rational로
곱하고 나머지를 다음 식으로 닫을 수 있다.

| 곱 | \(p>Y\) tail multiplier |
|---|---:|
| \(C_{\rm pre}\) | \(\exp(4k/Y)\) |
| \(P_0\) | \(\exp(4k/Y)\) |
| \(P_{\rm can}/\mathfrak S^{-1}\) | \(\exp(4k^2/Y)\) |

이번 gate는 실제 linear-form data를 만들지 않고 자연 cutoff \(Y=2k^2\)의 universal
상계를 채택했다. 더 큰 \(Y\)를 쓰면 head를 exact 계산하는 대신 tail은 더 작아진다.

## 10. 상태 전이

| obligation | 이전 | 현재 | 이유 |
|---|---|---|---|
| H1B2A-P94-FINAL-EULER | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | exact 두 곱과 finite singular-series comparison |
| H1B2A-P94-DISTRIBUTION | INPUT_PACKAGE_MISSING | 변화 없음 | Hypothesis 1(1),(3) multiplier·cutoff 필요 |
| H1B-P94 | RATE_MISSING | 변화 없음 | 위 distribution child가 열림 |
| H1B-COMP-01 | HARD_BLOCKER | 변화 없음 | 다른 moment와 공통 budget 미완료 |
| SIV-07/09 | HARD_BLOCKER | 변화 없음 | Proposition 6.1 전체 미완료 |
| \(X_{\rm cert}\) | OPEN | 변화 없음 | threshold calculator 선결조건 미충족 |

특히 \(8.73\)이라는 설명용 multiplier는 Sono 부등식의 threshold가 작다는 뜻이 아니다.
다른 단계의 explicit 상수는 훨씬 크고, 아직 숫자가 없는 분포 정리도 남아 있다.

> **2026-09-08 후속 갱신:** 위 표는 H1b-2a.1 종료 당시 상태다. 후속
> [`H1b-2a.2`](30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md)가 actual
> \(\mathcal A=\mathbb Z\)의 식 (9.52) child를
> `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`으로 닫았다. 따라서 “Hypothesis
> 1(1),(3) multiplier 필요”는 일반 \(\mathcal A\)에 대해서만 유지된다. P94 부모와
> `SIV-07/09`, \(X_{\rm cert}\)의 열린 상태는 변하지 않는다.

## 11. 기계검증

source/h1b2a1_proposition94_euler.py는 다음을 exact Fraction으로 계산한다.

1. \(g_*(p,m)\)
2. (29.8), (29.18), (29.23), (29.24)의 양변
3. local \(4k/p^2\), \(4k^2/p^2\) 상계
4. 임의 \(Y\ge2k^2\)의 tail exponent
5. parent non-promotion 상태

tests/test_h1b2a1_proposition94_euler.py는 \(k=36,50,100\)의 여러 정수
\(p>2k^2\)와 모든 \(0\le\omega\le k\)를 검사한다. 실제 적용은 소수에만 이루어지지만
대수 부등식이 모든 해당 정수에서 성립하므로 이 시험은 더 강한 toy grid다.

이 시험은 식 (9.52)의 분포 추정이나 Proposition 9.4 전체를 컴퓨터가 증명한다는 뜻이 아니다.

## 12. 사용자 수행사항

별도 수행절차 필요없음. 실제 소수 탐색, maximal-gap 데이터, 장시간 CPU, Lean,
추가 Python package 또는 threshold calculator를 사용하지 않았다.
