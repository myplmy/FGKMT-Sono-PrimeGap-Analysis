# Sono/FMT H1b-1b-2d.1a.1: Maynard (9.42)--(9.48) scalar remainder 수치 재증명

- 작성일: 2026-09-08
- 상위 obligation: H1B-L84, H1B1-PACKAGE, SIV-07
- 선행 정본:
  [line-905 square-sum 우회](25_Sono_FMT_H1b1b2d1a_H_remainder_bypass.md)
- 기계 계약:
  [Sono_FMT_H1b1b2d1a1_scalar_remainder_v1.json](data/Sono_FMT_H1b1b2d1a1_scalar_remainder_v1.json)
- 구현: source/h1b1b2d1a1_scalar_remainder.py
- 비판적 검토:
  [H1b-1b-2d.1a.1 타당성 검토](../../review/32_20260908_H1b1b2d1a1_scalar_remainder_타당성검토.md)

## 1. 결론

Maynard의 최종 출판본 식 (9.42)--(9.48)에서 생략된 상수를 처음부터 다시 추적해,
line 905 square-sum 우회에 필요한 pointwise scalar bound를 다음과 같이 닫았다.

\[
\boxed{
 |Z_{\mathbf r}-A(\mathbf u_{\mathbf r})|
 \le
 C_Y\frac{T_k(\log\log R)^2}{\log R}
 B(\mathbf u_{\mathbf r})
 }
\tag{26.1}
\]

여기서

\[
\boxed{
C_Y=
327680\frac{14801}{69}e^{264}+10\,143\,697
<3.17\times10^{122}.
}
\tag{26.2}
\]

이는 작고 날카로운 상수가 아니라, 모든 숨은 \(O\)와 \(\ll\)을 실제 숫자로 덮기 위해 만든
의도적으로 보수적인 공통 상수다. 중요한 점은 유한한 숫자와 충분조건 cutoff가 존재한다는
것이지 이 값이 계산 실무에 적합하다는 뜻이 아니다.

이번 판정은 다음과 같다.

~~~text
source scalar multiplier C_Y      PROJECT FINITE COMPONENT CLOSED
line-905 scalar subpackage         PROJECT FINITE COMPONENT CLOSED
two sharp xi*log(x) calls          RATE_MISSING
H1B-L84 / SIV-07 / X_cert          RATE_MISSING / HARD_BLOCKER / OPEN
~~~

따라서 Proposition 6.1 전체나 Sono의 numerical threshold를 닫았다는 주장은 하지 않는다.

## 2. 쉽게 설명하면

이전에는 원문에 “오차가 이 정도 크기보다 작다”는 방향만 있고 그 앞의 숫자가 없었다.
이번에는 그 오차를 만드는 부품을 여섯 조각으로 나눴다.

1. 여러 좌표에 들어갈 수 있는 작은 소인수 조합의 수
2. determinant의 소인수로 이루어진 divisor 합
3. determinant가 얼마나 커질 수 있는지
4. 여러 totient 인자가 서로 정확히 지워지는지
5. 한 좌표를 합할 때 생기는 smooth summation 오차
6. 두 종류의 오차를 마지막에 합치는 과정

각 조각을 큰 쪽으로 안전하게 반올림한 뒤 곱하거나 더했다. 그 결과 상수는 매우 커졌지만,
더 이상 “어떤 상수가 있을 것”이라는 존재형 기호로 남지 않는다. 다만 다른 두 곳에는
아직 \(\xi\log x\)가 실제로 얼마나 큰지에 대한 수치 하한이 없으므로 전체 정리는 아직 열려 있다.

## 3. 원천과 출판본 정정

주 원천은 James Maynard, Dense clusters of primes in subsets, Compositio Mathematica
152 (2016), 1517--1554, DOI 10.1112/S0010437X16007296이다. 최종 출판본 1545쪽의
식 (9.43)은

\[
\Delta_m=\prod_{i\ne m}(a_mb_i-a_ib_m)
\tag{26.3}
\]

로 정확하게 인쇄돼 있다. 반면 오래된 author TeX Subsets.tex 986행에는 \(i=m\)도
포함돼 곱이 0이 되는 오자가 남아 있다. 이 프로젝트는 최종 출판본을 정본으로 사용한다.
따라서 이는 “출판 논문의 determinant ambiguity”가 아니라 “구 author TeX가 최종본보다
뒤처진 경우”다.

부호는 divisor support와 크기 상계에 영향을 주지 않도록

\[
D_m=\operatorname{rad}\!\left(\prod_{i\ne m}|a_mb_i-a_ib_m|\right)
\tag{26.4}
\]

를 사용한다. 원문의 distinct linear-form 가정 아래 각 determinant는 0이 아니다.

## 4. 선행연구 우선 조사

직접 증명 전에 다음을 조사하고 실제 가정을 대조했다.

- Maynard 최종 출판본의 (9.42)--(9.48): 정확한 합, determinant와 정규화의 정본
- Rosser--Schoenfeld (1962), Theorem 6 (3.24): 모든 \(x>1\)에서
  \(\sum_{p\le x}\log p/p<\log x\)
- Rosser--Schoenfeld (1962), (3.41)--(3.42): 모든 \(n\ge3\)에 안전한
  \(n/\varphi(n)\) explicit upper bound
- 앞서 Castillo et al.의 교정을 반영해 복원한 project Lemma 8.3 multiplier

표적 검색에서는 현재 식의 vector multiplicity, (26.3)의 support, 교정된 Lemma 8.3
정규화와 finite cutoff를 한꺼번에 제공하는 peer-reviewed numerical lemma를 찾지 못했다.
이는 전 세계 문헌에 없다는 신규성 주장이 아니다. 따라서 위 선행식을 그대로 재사용하고,
그 사이의 가장 작은 연결부만 아래에서 직접 증명한다.

## 5. \(s\)-Euler product

식 (9.42)의 조건 \((s,t)=1\)을 보존한 상태에서 먼저

\[
\varphi_\omega(st)=\varphi_\omega(s)\varphi_\omega(t)
\]

로 분모를 분리한다. 그 뒤에만 \(s\)-조건을 더 큰 집합으로 확장한다. 분리 전에 gcd
조건을 버리면 이 등식은 사용할 수 없으므로 순서가 중요하다.

\(\log(st)\le \sqrt{s}(1+\log t)\)이고, 각 \(p>2k^2\)를 \(s\) 좌표에 배치하는 방법은
최대 \(k\)개다. 따라서 local 증가분은

\[
k\frac{\sqrt p}{(p-1)(p-\omega(p))}
\le \frac{4k}{p^{3/2}}.
\]

정수 전체로 확장하면

\[
\sum_{p>2k^2}\frac{4k}{p^{3/2}}<4\sqrt2<6.
\]

그러므로 \(s\)-곱은

\[
\boxed{C_s<e^6<3^6=729.}
\tag{26.5}
\]

## 6. \(t\mid D_m\) divisor 합

eligible prime마다 \(q_p=1/(p-\omega(p))\)라 두면 square-free divisor를 전부 합한
정확식은

\[
\sum_{t\mid D_m}\frac{1+\sum_{p\mid t}\log p}{\varphi_\omega(t)}
=P_D\left(1+\sum_{p\mid D_m}
\frac{\log p}{p-\omega(p)+1}\right),
\quad
P_D=\prod_{p\mid D_m}(1+q_p).
\tag{26.6}
\]

이 식은 코드에서 로그를 formal basis로 둔 exact rational subset enumeration과 대조한다.

### 6.1 곱 부분

\[
\frac{1+1/(p-\omega(p))}{1+1/(p-1)}
=1+\frac{\omega(p)-1}{p(p-\omega(p))}.
\]

\(p>2k^2\), \(\omega(p)\le k\)를 쓰면 전체 correction은

\[
\exp(1/k)<36/35\qquad(k\ge36)
\]

이므로

\[
P_D<\frac{36}{35}\frac{D_m}{\varphi(D_m)}.
\tag{26.7}
\]

### 6.2 로그 부분

분모를 \(p\)로 바꾸며 생기는 correction은 정수합으로 확장해

\[
\sum_{p>2k^2}\frac{2k\log p}{p^2}
<\frac{\log(2k^2)+1}{k}\le\frac14
\qquad(k\ge36)
\tag{26.8}
\]

로 제한된다. Rosser--Schoenfeld (3.24)를 \(p\le\log D_m\)에 사용하고 더 큰 소인수는
그 곱의 로그로 직접 제한하면

\[
\sum_{p\mid D_m}\frac{\log p}{p}<\log\log D_m+1.
\tag{26.9}
\]

\(D_m>1\)이면 모든 소인수가 \(2k^2\)보다 커서
\(L_D=\log\log D_m>1\)이다. Rosser--Schoenfeld (3.41)--(3.42)에
\(e^\gamma<3\), \(2.50637<2.51\)을 적용하면

\[
\frac{D_m}{\varphi(D_m)}<5.51L_D.
\]

따라서 (26.6)의 계수는 정확히

\[
\frac{36}{35}\frac{551}{100}\frac{13}{4}
=\frac{64467}{3500}<19,
\]

즉

\[
\boxed{C_t=19,\qquad \text{divisor sum}<19L_D^2.}
\tag{26.10}
\]

\(D_m=1\)이면 원래 합이 1이므로 별도로 즉시 덮인다.

## 7. determinant를 \((\log\log R)^2\)에 흡수

원문의 \(|a_i|,|b_i|\le x^\alpha\)로 각 determinant는 \(2x^{2\alpha}\) 이하이다.
또한 \(k\le(\log x)^{1/5}\), \(R\ge x^{\theta/10}\), \(\log R\ge1\)이므로

\[
\log D_m\le C_\Delta(\alpha,\theta)(\log R)^{6/5},
\quad
C_\Delta=\left(\frac{10}{\theta}\right)^{1/5}
\left(\log2+\frac{20\alpha}{\theta}\right).
\tag{26.11}
\]

따라서

\[
\log\log R\ge
\max\left\{1,\frac54\max(0,\log C_\Delta)\right\}
\tag{26.12}
\]

이면 \(L_D\le2\log\log R\)이고, (26.10)은

\[
\text{\(t\)-sum}<76(\log\log R)^2
\tag{26.13}
\]

가 된다.

## 8. prefactor와 \(e_m\)-합

\(Q=\operatorname{rad}(a_mWBr)\), \((r,WB)=1\),
\(\varphi_L(r)=\varphi(a_mr)/\varphi(a_m)\)이면

\[
\frac{a_mWB}{\varphi(a_mWB)}
\frac{r}{\varphi_L(r)}
\frac{\varphi(Q)}{Q}=1.
\tag{26.14}
\]

이는 \((a_m,r)>1\)이어도 prime-by-prime 정확히 성립한다. 남는 nonexcluded local product는
(26.7)과 같은 구조여서 \(36/35\)보다 작다.

식 (9.44)의 \(e_m\)-합에는 \(F_2\)의 \(N,W\) 항을 따로 합하고, 앞서 교정한 Lemma 8.3을
한 번씩 적용한다. 기존 common smooth gate에서 각 relative error가 1 이하이므로 양의 합은
main envelope의 2배 이하이다. Lemma 8.2의 multiplier 89까지 포함한 YmError branch는

\[
C_{Ym}^{\rm exact}
=89\cdot729\cdot19\cdot4\cdot2\cdot\frac{36}{35}
=\frac{355028832}{35}
\]

이고 한 번만 위로 반올림해

\[
\boxed{C_{Ym}=10\,143\,681.}
\tag{26.15}
\]

## 9. 식 (9.47)의 direct branch

외부 좌표의 \(N\)-곱을 \(P_{\rm out}\), \(B=\int F_2dt_m\)라 쓰자. \(N\)의 support에서
\(W\ge N\)이므로

\[
\frac{B}{P_{\rm out}}\ge(k-1)I_N,
\quad
I_N\ge\frac{\log(1+0.9U_kT_k)}{T_k}\ge\frac1{2(k-1)}
\quad(k\ge36).
\tag{26.16}
\]

Lemma 8.3은 \(z=R^{U_k}\), \(v=t_m/U_k\)로 적용한다. 이 rescaling 때문에 필요한 것은
unscaled derivative가 아니라 \(|G|+U_k|G'|\)이다. 직접 미분하면

\[
\frac{G_{\max}}{P_{\rm out}}
\le51+\frac{50}{\sqrt k}+\sqrt k\log k
\le T_k
\quad(k\ge36).
\tag{26.17}
\]

(26.16)--(26.17)에서 \(G_{\max}\le2T_kB\)를 얻는다. 공통

\[
\Lambda_*=A+B_\Lambda\log R,
\]

\[
A=2k^2\log(2k^2)+k(k-1)\log2,
\quad
B_\Lambda=\frac{10\alpha(2k^2-k+1)}{\theta}+k
\]

에 대해

\[
\log\log R\ge\max\{1,6+\log(A+B_\Lambda)\}
\tag{26.18}
\]

이면 \(L+1=6+\log\Lambda_*\le2\log\log R\)이다. 따라서 direct branch coefficient는

\[
4C_{8.3}(1/2,8)
\tag{26.19}
\]

이고 \(\log\log R\ge1\)을 사용해 제곱형에 안전하게 흡수된다.

## 10. 공통 상수와 finite gate

교정된 one-step 상수는

\[
C_{8.3}(1/2,8)=2\left(40960\frac{14801}{69}e^{264}+2\right).
\]

(26.15)와 (26.19)를 더하면 (26.2)가 된다. 충분한 cutoff는 다음 네 값의 최대다.

1. theory 24의 common_smooth_gate_certificate
2. theory 25의 일곱 square-bypass tensor family에서
   \(C_{8.3}(L+1)\sum\kappa_i/\log R\le1\)을 보장하는 같은 형태의 finite-product gate
3. (26.12)를 만족시키는 \(\log R\)
4. (26.18)을 만족시키는 \(\log R\)

예를 들어 \(k=36,\alpha=0.01,\theta=0.25\)에서 기존 common smooth gate가 지배하며

\[
\log R\ge1.1742478701903428\times10^{132}
\]

가 이 하위 package의 보수적 충분조건이다. 이는 단지 parameterized diagnostic 예이며
\(x\)에 대한 Sono theorem threshold가 아니다. 특히 \(k,\alpha,\theta,R,x\)의 모든 상위
선택과 나머지 proof obligation을 아직 결합하지 않았다.

## 11. 기계 검증과 한계

코드는 다음을 검증한다.

- exact rational \(t\)-divisor identity와 독립 subset enumeration
- \((a_m,r)>1\)도 포함한 exact prefactor cancellation
- \(C_{Ym}^{\rm exact}\)와 단일 upward rounding
- direct profile의 두 analytic gate 진단
- finite cutoff에서 determinant, discrepancy와 line-995 upper gate
- parent node non-promotion

유한한 \(k\) 표본 검사는 \(k\ge36\) 전체의 해석적 증명을 대신하지 않는다. 전체 범위의
근거는 위 단조부등식이며 코드는 계수·전개·구현 회귀검사다. 추가 Python package나 Lean은
이 gate에 필요하지 않았다.

## 12. 남은 의무

이번 결과 뒤의 직접 다음 단계는 H1b-1b-2d.1b다. Maynard source의 두 sharp indicator
호출에서 분모가 되는 \(\xi\log x\)에 finite lower bound를 넣어야 한다. 그 뒤에도
Lemmas 8.5--8.6, 공통 moment error budget, H1c/PAP가 남는다. 모든 root가 닫히기 전에는
threshold calculator나 장시간 prime sweep을 만들지 않는다.
