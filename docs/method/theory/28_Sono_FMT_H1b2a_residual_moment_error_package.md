# Sono/FMT H1b-2a Lemma 8.5·8.6 및 Proposition 9.4 잔여 package

- 작성일: 2026-09-08
- 증거 수준: `PROJECT FINITE LEMMAS + SOURCE-LEVEL RESIDUAL AUDIT`
- 기계 계약:
  [`data/Sono_FMT_H1b2a_residual_moment_error_v1.json`](data/Sono_FMT_H1b2a_residual_moment_error_v1.json)
- 구현: `source/h1b2a_residual_moment_package.py`
- 비판적 검토:
  [`H1b-2a 타당성검토`](../../review/34_20260908_H1b2a_Lemmas85_86_Proposition94_타당성검토.md)
- 상위 상태:

~~~text
H1B-L85        ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
H1B-L86-SIZE   PROJECT_FINITE_COMPONENT_CLOSED
H1B-P94        RATE_MISSING
H1B-COMP-01    HARD_BLOCKER
SIV-07/09      HARD_BLOCKER
X_cert         OPEN
~~~

## 1. 결론과 범위

Maynard Lemma 8.5의 세 정성적 크기식은 이전 단계에서 닫은 실제 `L620_dW`
Lemma 8.4 오차를 받아 **유한식**으로 바꿀 수 있다. Lemma 8.6에서는 실제 cutoff가 1인
작은 정육면체만 적분해

\[
I_k(F)\ge (2k\log k)^{-k}\qquad(k\ge36)
\]

을 multiplier 1로 얻는다. 기존 H1a와 합치면

\[
J_k(F)>
\frac{\log k}{4k}(2k\log k)^{-k}
\]

도 유한하게 닫힌다. (F_1,F_2) 비교도 균일한 `O(1)` 대신 다소 큰
(2^k,C_J(k))를 허용하면 계산 가능한 식으로 바뀐다.

Proposition 9.4에서는 식 (9.56)--(9.63)의 대수 계수, exact denominator와 첫 Euler 곱을
명시했다. 그러나 식 (9.52)의 distribution error와 식 (9.67)의 마지막 두 Euler 곱은
아직 숫자 상수와 공통 cutoff가 없다. 따라서 Proposition 9.4와 전체 good sieve weight는
닫히지 않았다.

쉽게 말하면, 이번에는 저울에 올릴 **주항의 최소 무게**와 일부 포장재의 최대 무게를
숫자식으로 만들었다. 하지만 운송 중 생기는 분포 오차와 마지막 포장 두 겹의 무게표가
남아 있으므로 완제품 전체가 언제부터 안전한지는 아직 계산할 수 없다.

## 2. 원천과 문헌 우선 조사

직접 원천은 James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
*Compositio Mathematica* 152 (2016), Lemmas 8.5--8.6와 Proposition 9.4다.
Lemma 8.6이 인용하는 선행 논증은 Maynard,
[*Small Gaps Between Primes*](https://doi.org/10.4007/annals.2015.181.1.7),
*Annals of Mathematics* 181 (2015), Section 7이다.

최종 출판본 PDF, arXiv/author TeX와 정확한 lemma·식 문구를 표적 조사했다. 같은 시험함수,
같은 (k,R) 정규화에서 Lemmas 8.5--8.6와 Proposition 9.4를 finite multiplier까지
그대로 대체하는 peer-reviewed explicit package는 이번 조사에서 확인하지 못했다. 이는
전 세계 문헌에 그런 결과가 없다는 주장이나 novelty 주장이 아니다. 따라서 원문의 구조를
보존하고, 이미 닫힌 project lemma와 원문 사이의 최소 연결부만 아래에서 직접 증명한다.

검토본과 hash는 기계 계약에 고정했다. Maynard 2016 최종 출판본 pp.1536--1537,
pp.1547--1550 및 Maynard 2015 최종 출판본 pp.405--408을 PDF 렌더링으로도 확인했다.

## 3. 공통 정의

이 단계에서

\[
q=\frac9{10},\qquad T=T_k=k\log k,\qquad U=U_k=k^{-1/2}
\]

이고 project cutoff는

\[
0\le\psi\le1,\qquad
\psi(t)=1\ (0\le t\le q),\qquad
\psi(t)=0\ (t\ge1)
\]

을 만족한다. 실제 함수는

\[
n(t)=\frac{\psi(t/U)}{1+Tt},\qquad
h(t)=\frac{\psi(t/2)}{1+Tt},
\]

\[
F(\mathbf t)=\psi\!\left(\sum_i t_i\right)\prod_i n(t_i),
\quad F_1(\mathbf t)=\prod_i n(t_i),
\]

\[
F_2(\mathbf t)=\sum_{j=1}^k h(t_j)\prod_{i\ne j}n(t_i)
\]

다. 모든 직접 부등식은 project target 범위 (k\ge36)에서 서술한다.

## 4. Lemma 8.6: 절대 (I_k) 하한

정육면체

\[
\mathcal C=[0,q/k]^k
\]

를 잡는다. (mathbf t\in\mathcal C)이면

\[
\sum_i t_i\le q,
\qquad
\frac{t_i}{U}\le\frac{q}{\sqrt{k}}\le q.
\]

따라서 두 cutoff가 모두 정확히 1이고,

\[
I_k(F)\ge
\left\{\int_0^{q/k}\frac{dt}{(1+Tt)^2}\right\}^k
=\left\{\frac{q}{k(1+q\log k)}\right\}^k.
\tag{28.1}
\]

(q\log k\ge1)이면

\[
\frac{q}{1+q\log k}\ge\frac1{2\log k}.
\]

이 조건은 이미 (k\ge4)에서 성립하므로 target 범위 전체에서

\[
\boxed{I_k(F)\ge(2k\log k)^{-k}.}
\tag{28.2}
\]

원문의 Vinogradov 기호 앞 multiplier를 1로 가정한 것이 아니다. cutoff plateau 안의
부분영역을 직접 적분해 얻은 별도 유한 하한이다. 상위 H1b 원장에 잘못 적힌
`(2k log k)^(-k-1)`은 최종 출판본의 정확한 지수 `-k`로 교정한다.

기존 H1a 정리

\[
\frac{J_k(F)}{I_k(F)}>\frac{\log k}{4k}\quad(k\ge36)
\]

와 합치면

\[
\boxed{
J_k(F)>\frac{\log k}{4k}(2k\log k)^{-k}.
}
\tag{28.3}
\]

을 얻는다.

## 5. Lemma 8.6: (F_1,F_2) 비교의 유한 상수

(F\le F_1)은 점별로 자명하다. (n(t)\ne0)이면 (t\le U\le1)이므로
(t/2\le1/2<q), 따라서 (psi(t/2)=1\ge\psi(t/U))이고 (h(t)\ge n(t))다.
그러므로

\[
F_2\ge kF_1,
\]

따라서

\[
I(F)\le I(F_1)\le\frac{I(F_2)}{k^2},
\qquad
J(F)\le J(F_1)\le\frac{J(F_2)}{k^2}
\tag{28.4}
\]

가 정확히 성립한다.

상계는 보수적으로 얻는다. (int n^2,int h^2,int nh\le1/T)이고
Cauchy 또는 (F_2^2\le k\sum_j(cdots)^2)를 쓰면

\[
\frac{I(F_2)}{k^2}\le T^{-k}\le2^kI(F).
\tag{28.5}
\]

또한

\[
\int n\le\frac{\log(1+TU)}T,
\qquad
\int h\le\frac{\log(1+2T)}T.
\]

(F_2)를 마지막 좌표에 대해 먼저 적분하고 제곱을 정확히 전개하면

\[
\frac{J(F_2)}{k^2}
\le
\frac{[\log(1+2T)+(k-1)\log(1+TU)]^2}{k^2T^{k+1}}.
\]

(28.3)을 사용해

\[
\boxed{
\frac{J(F_2)}{k^2}\le C_J(k)J(F),
}
\]

\[
C_J(k)=
\frac{4\,2^k[\log(1+2T)+(k-1)\log(1+TU)]^2}
{k^2(\log k)^2}.
\tag{28.6}
\]

을 얻는다. (2^k,C_J(k))는 원문의 (O(1))을 날카롭게 복원한 값이 아니다. 대신
유한하고 계산 가능하며 숨은 상수가 없는 안전한 대체값이다. threshold가 지나치게 커질 경우
나중에 Maynard 2015의 concentration 계산을 더 날카롭게 수치화할 수 있지만, soundness에는
영향이 없다.

## 6. Lemma 8.5: coefficient와 두 weight bound

이전 theory 24가 실제 식 (8.19)의 `L620_dW`에 대해 product-profile envelope 오차
(\varepsilon_{620})을

\[
\varepsilon_{620}\le\prod_i(1+\delta_i)-1
\tag{28.7}
\]

로 명시했다. (M_{620}=1+\varepsilon_{620})라 둔다. 식 (8.18)--(8.21)의 exact
singular-series cancellation과 (F\le F_1)을 적용하면

\[
|\lambda_{\mathbf d}|\le
M_{620}(\log R)^k\int F_1.
\tag{28.8}
\]

한편

\[
\int_0^U n(t)dt\le\frac{\log(1+TU)}T\le\frac1k
\tag{28.9}
\]

이다. 마지막 부등식은
(log(1+\sqrt{k}\log k)\le\log k), 즉
(log k\le\sqrt{k}-1/\sqrt{k})와 동치다. 오른쪽과 왼쪽의 차는 (k=36)에서
양수이고 도함수는

\[
\frac{(\sqrt{k}-1)^2}{2k^{3/2}}\ge0
\]

이므로 모든 (k\ge36)에서 성립한다. 따라서

\[
\boxed{
|\lambda_{\mathbf d}|\le M_{620}\left(\frac{\log R}{k}\right)^k.
}
\tag{28.10}
\]

기존 common smooth gate에서 (sum_i\delta_i\le1)이면
(M_{620}\le e)다.

각 (d_i)는 squarefree이고 (B)와 서로소다. 고정된 (n)에서 가능한 divisor tuple 수를
좌표별로 독립 상계하면

\[
\#\{\mathbf d:d_i\mid L_i(n)\}
\le\prod_{i=1}^k\prod_{\substack{p\mid L_i(n)\\p\nmid B}}2.
\]

따라서 (R\le x)에서

\[
\boxed{
w_n\le M_{620}^2k^{-2k}(\log x)^{2k}
\prod_{i=1}^k\prod_{\substack{p\mid L_i(n)\\p\nmid B}}4.
}
\tag{28.11}
\]

마지막으로 (N_k(R)=\#\{(d_1,\ldots,d_k):d_1\cdots d_k<R\})라 하면

\[
N_k(R)\le
R\sum_{d_1,\ldots,d_k<R}\frac1{d_1\cdots d_k}
\le R(1+\log R)^k.
\tag{28.12}
\]

그러므로

\[
w_n\le
M_{620}^2\left(\frac{\log R}{k}\right)^{2k}
R^2(1+\log R)^{2k}.
\tag{28.13}
\]

이를 원문의 (R^{2+o(1)})과 같은 모양으로 쓰려면

\[
\boxed{
\eta_{85}(k,R)=\max\left\{0,
\frac{2\log M_{620}+2k\log[(\log R/k)(1+\log R)]}{\log R}
\right\}
}
\tag{28.14}
\]

로 두어

\[
\boxed{w_n\le R^{2+\eta_{85}(k,R)}}
\tag{28.15}
\]

을 얻는다. 이것은 `o(1)`을 0으로 놓은 것이 아니라 실제 finite exponent를 저장한 식이다.

## 7. Proposition 9.4에서 닫힌 세 local 항

### 7.1 식 (9.56)--(9.57)의 제곱 대수

(2|ab|\le a^2+b^2)를 쓰고 ((\mathbf r,r_0))와
((\mathbf s,s_0))의 대칭성을 적용하면 추가 multiplier는 정확히 1이다.

### 7.2 식 (9.57)의 denominator

(m=\omega^*(p)\le k+1), (p>2k^2)라 두면

\[
p\frac{p+m-2}{(p-m)^2}
\le\frac{1+u}{(1-u)^2},
\qquad u=\frac mp<\frac{k+1}{2k^2}<\frac15.
\]

따라서

\[
\boxed{
\frac{p+\omega^*(p)-2}{(p-\omega^*(p))^2}\le\frac2p.
}
\tag{28.16}
\]

### 7.3 식 (9.63)의 첫 Euler 곱

(p>2k^2), (omega(p)\le k)이므로

\[
\frac{\omega(p)}{(p-1)(p-\omega(p))}\le\frac{4k}{p^2}.
\]

(log(1+z)\le z)와
(sum_{n>2k^2}n^{-2}\le(2k^2)^{-1})에서

\[
\boxed{
\prod_{p\nmid WB}
\left(1+\frac{\omega(p)}{(p-1)(p-\omega(p))}\right)
\le e^{2/k}.
}
\tag{28.17}
\]

따라서 식 (9.65)의 (y_{\mathbf r,r_0}) 상계에는 (e^{2/k}), 제곱합에는
(e^{4/k})를 안전하게 쓸 수 있다.

## 8. Proposition 9.4에 남은 두 blocker

1. **식 (9.52)의 distribution error.** 원문은 Proposition 9.1과 동일한 논증으로
   negligible하다고 한다. Lemma 8.5의 finite coefficient bound는 이제 쓸 수 있지만,
   Hypothesis 1(1),(3)의 multiplier와 유효 시작점이 없으므로 최종 흡수 부등식은 열려 있다.
2. **식 (9.67)의 두 Euler 곱.** 원문은
   (prod(1+O(k)/p^2)=O(1))과 singular-series 역수 비교를 사용한다. 이 식은 exact
   pre-(O(k)) local factor를 다시 복원한 뒤에야 수치화할 수 있다. 현재 단계에서
   `O(k)`를 (k) 또는 1로 임의 치환하지 않는다.

식 (9.70)의 residue-class factor는 exact 항등식 뒤 각 extra factor가 1 이하이므로 새
blocker가 아니다. 기존 theory 27이 식 (9.58), (9.66)의 sharp cutoff도 이미 닫았다.

## 9. 상태 전이와 금지되는 결론

이번 증거로 다음 두 parent row는 승격할 수 있다.

~~~text
H1B-L85       RATE_MISSING -> ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
H1B-L86-SIZE  RATE_MISSING -> PROJECT_FINITE_COMPONENT_CLOSED
~~~

반면 다음은 바뀌지 않는다.

~~~text
H1B-P94       RATE_MISSING
H1B-COMP-01   HARD_BLOCKER
SIV-07/09     HARD_BLOCKER
X_cert        OPEN
~~~

특히 (2^k,C_J(k))가 매우 크다는 이유로 증명이 틀린 것은 아니지만, 최종 threshold를
엄청나게 악화시킬 수 있다. 또한 이번 식을 계산했다는 사실만으로 Maynard Proposition 6.1,
FGKMT/FMT good weight 또는 Sono 부등식의 numerical threshold가 증명됐다고 말하면 안 된다.

## 10. 검증과 사용자 수행사항

`tests/test_h1b2a_residual_moment_package.py`는 다음을 검사한다.

- plateau cube 적분식과 직접 고정밀 적분의 일치
- (k=36,100,1000,8104)에서 absolute lower와 comparison gate
- 기존 common smooth gate에서 (M_{620}\le e)
- Proposition 9.4 local factor와 parent non-promotion
- 세 원문 파일의 SHA-256과 계약 상태

이 시험은 문서의 대수식·기계 계약을 회귀검사한다. 열린 distribution theorem이나
Proposition 9.4 전체를 컴퓨터가 증명하는 것은 아니다.

사용자 수행절차: 별도 수행절차 필요없음. 실제 소수 데이터 실험, threshold 계산,
추가 Python 패키지 또는 Lean은 이번 gate에 필요하지 않다.
