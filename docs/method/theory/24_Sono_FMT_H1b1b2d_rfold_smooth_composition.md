# Sono/FMT H1b-1b-2d support-scaled smooth norm과 교정 \(r\)-회 합성

- 작성일: 2026-09-08
- 상위 obligation: `H1B-L83`, `H1B-L84`, `H1B1-PACKAGE`, `SIV-07`
- 선행 정본:
  - [교정된 κ=1 Wirsing multiplier](22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md)
  - [actual Section 8 입력 상수](23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md)
- 기계 계약:
  [Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json](data/Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json)
- 구현: `source/h1b1b2d_rfold_smooth_package.py`
- 비판적 검토:
  [H1b-1b-2d 적용성 검토](../../review/30_20260908_H1b1b2d_Lemma84_rfold_smooth_적용성검토.md)
- 후속 scalar 정본:
  [H1b-1b-2d.1a.1 scalar remainder](26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md)

## 1. 판정부터 요약

이번 단계는 Maynard Lemma 8.4의 숨은 \(O\)-상수를 전부 닫은 것이 아니다. 닫힌 범위와
열린 범위는 다음과 같다.

~~~text
서로 다른 nonnegative smooth profile의 finite product 합성  PROJECT PARAMETERIZED EXPLICIT
실제 N,W,N^2,W^2,NW profile norm                   PROJECT PARAMETERIZED EXPLICIT
Lemma 8.4의 smooth actual subapplication             8/9 CLOSED AS SUBPACKAGE
직접 Lemma 8.3 smooth call                            1/1 ENVELOPE EXPLICIT
sharp cutoff call                                     2 PARAMETERIZED; FINITE SCALE OPEN
line 905의 H remainder                                C1 BYPASSED / SCALAR MULTIPLIER EXPLICIT
parent H1B-L84 / SIV-07 / X_cert                      RATE_MISSING / HARD_BLOCKER / OPEN
~~~

즉 “매끄러운 함수들을 여러 번 합할 때 오차가 어떻게 쌓이는가”는 정확한 유한 곱으로
바꿨고, 실제로 나타나는 기본 함수들의 보수적인 크기도 계산식으로 만들었다. 그러나 원문
후속 H1b-1b-2d.1a는 905행의 전역 \(H\) 도함수가 없어도 되는 square-sum 우회를
정식화했고, 2d.1a.1은 \(O\) 안의 격자점별 scalar multiplier와 finite gate를
수치 재증명했다. \(r_0<x^\xi\)인 두 sharp cutoff에는 여전히 \(\xi\log x\)의 유한 하한이
없다. 이 때문에 전체
Lemma 8.4 package나 Sono 정리의 numerical threshold는 아직 닫히지 않는다.

## 2. 쉬운 설명

한 번 계산할 때 최대 1%의 오차가 난다고 하자. 이를 열 번 반복했을 때 오차를 단순히
10%라고 쓰면 작은 오차 근사일 뿐이다. 안전한 정확식은

\[
(1+0.01)^{10}-1
\]

이다. 이번 작업은 Maynard가 \((1+O(\varepsilon))^j-1=O(j\varepsilon)\)로 남긴 부분을
이와 같은 유한 곱으로 바꾼다. 좌표마다 함수 폭과 기울기가 다르므로 실제로는
\(\prod_i(1+\delta_i)-1\)을 쓴다.

또한 폭이 \(U_k=1/\sqrt{k}\)인 좁은 함수와 폭이 2인 넓은 함수를 같은 폭 1로 취급하지
않는다. 각 폭에 맞게 변수 크기를 바꾸고 그에 따른 도함수 비용을 포함한다.

## 3. 선행연구를 먼저 찾은 결과

| 출처 | 확인한 내용 | 이번 문제에 대한 적용성 |
|---|---|---|
| Maynard, *Dense Clusters of Primes in Subsets*, Lemmas 8.3–8.4 | 한 좌표 partial summation과 \(r\)-회 귀납 구조 | 직접 원천. 다만 \(O/o\) 상수와 finite cutoff는 없음 |
| Ford, *Sieve Methods* notes, Theorem 4.4 | 누락된 \(c_\gamma(L+1)^\kappa\)를 보존한 one-step proof | theory 22에서 \(\kappa=1\) 수치 multiplier로 이미 특수화 |
| Castillo et al., Lemma 2.5와 Remark | GGPY/Maynard 인쇄 오류항 경고 | 원문을 그대로 수치화하면 안 된다는 교정 근거 |
| Axiom Math `PrimeGapsLib` 2026 blueprint, Lemma 9.11 | iterated partial summation을 telescoping하는 독립 구조 | 상수 \(C,C_1,C_2\)가 존재형이고 다른 sieve datum·norm을 사용. 미검증 원고이므로 theorem input으로 쓰지 않음 |
| Polymath/일반 Selberg sieve 문헌 | smooth sieve와 variational norm | 현재 actual profile, corrected multiplier, finite cutoff의 동시 대체물이 아님 |

표적 검색에서는 같은 actual Section 8 profile, 교정된 \(c_\gamma(L+1)\), 수치 상수와 finite
cutoff를 한꺼번에 제공하는 peer-reviewed 결과를 찾지 못했다. 이는 전 세계 문헌에 그런
결과가 없다는 novelty 주장이 아니다. 따라서 원문과 교정 선행증명을 채택하고, 그 사이의
support-rescaling과 유한 곱 연결부만 아래의 project lemma로 직접 증명한다.

## 4. 원문 식과 주의할 인쇄식

Maynard 원문 Lemma 8.3은 \(G:[0,1]\to\mathbb R\)에 대해

\[
\sum_{d<z}\mu^2(d)g(d)G\!\left(\frac{\log d}{\log z}\right)
=c_\gamma\log z\int_0^1G+E_G
\]

를 주며, 교정된 theory 22의 수치형은

\[
|E_G|\le C_{8.3}(a,A_2)c_\gamma(L+1)
\sup_{[0,1]}(|G|+|G'|)
\tag{24.1}
\]

이다. 실제 공통 입력은 theory 23의

\[
a=\frac12,\qquad A_2=8,\qquad L=5+\log\Lambda_*.
\tag{24.2}
\]

원문 620행과 출판본 p.1536에는

\[
k^2T_k=o\!\left(\frac{\log\log R}{\log R}\right)
\]

가 인쇄돼 있다. 이는 Lemma 8.4의 가정과 바로 뒤 식 (8.20)의 방향과 양립하지 않는다.
그 문맥에서 필요한 식은

\[
\frac{k^2T_k\log\log R}{\log R}=o(1),\qquad
k^2T_k=o\!\left(\frac{\log R}{\log\log R}\right).
\tag{24.3}
\]

식 (8.20)은 올바른 방향을 사용한다. 이 문서는 문맥상 불일치를 기록할 뿐, 출판사의
정식 erratum이 확인됐다고 주장하지 않는다.

## 5. support-rescaled one-coordinate lemma

\(G_i\ge0\)가 \([0,s_i]\)에 지지되고 \(I_i=\int_0^{s_i}G_i(t)dt>0\)라 하자. 한 좌표에서
\(z=R^{s_i}\), \(u=\log d/\log z\), \(\widetilde G_i(u)=G_i(s_i u)\)로 둔다. 그러면

\[
\log z\int_0^1\widetilde G_i(u)du
=s_i\log R\cdot\frac{I_i}{s_i}
=\log R\,I_i.
\tag{24.4}
\]

그리고

\[
\sup_{0\le u\le1}\left(|\widetilde G_i(u)|+|\widetilde G_i'(u)|\right)
=\sup_{0\le t\le s_i}\left(|G_i(t)|+s_i|G_i'(t)|\right).
\]

따라서 support-aware norm을

\[
\boxed{
\omega_{s_i}(G_i)=
\frac{\sup(|G_i|+s_i|G_i'|)}{I_i}
}
\tag{24.5}
\]

로 정의한다. 결합 cutoff \(\Phi(\sum t_i)\)가
\(|\Phi|\le B_0\), \(|\Phi'|\le B_1\)이면 안전한 좌표 계수는

\[
\kappa_i=\max(1,B_0+s_iB_1)\omega_{s_i}(G_i)
\tag{24.6}
\]

이다. \(R^{s_i}\ge2\)가 필요하므로 모든 좁은 \(s_i=U_k\) 좌표에는

\[
\log R\ge\sqrt{k}\log2
\tag{24.7}
\]

를 함께 요구한다.

## 6. Project lemma: 서로 다른 profile의 교정 유한 합성

### 가정

1. 각 단계의 \(\gamma_i\)가 (24.1)과 공통 입력 (24.2)를 만족한다.
2. 원문의 Euler-factor recurrence가 main factor를 \(\Pi_g\)로 정확히 합성한다.
3. \(G_i\ge0\), \(I_i>0\)이고, 결합 cutoff도 비음수다.
4. 각 단계의 \(\kappa_i\)는 (24.5)–(24.6)으로 상계된다.

\[
\delta_i=\frac{C_{8.3}(1/2,8)(L_i+1)\kappa_i}{\log R}
\tag{24.8}
\]

라 두면, product-profile envelope로 정규화한 전체 절대오차는

\[
\boxed{
\frac{|E_{\rm total}|}
{\Pi_g(\log R)^r\prod_i I_i}
\le \prod_{i=1}^{r}(1+\delta_i)-1.
}
\tag{24.9}
\]

### 증명

한 좌표의 연산자를 main 연산자 \(M_i\)와 error 연산자 \(E_i\)의 합으로 쓴다.
가정 1과 (24.4)–(24.6)에 의해 nonnegative envelope 위에서
\(|E_i|\le\delta_i M_i\)다. \(r\)개 곱을 전개하면 main만 택한 한 항과, 적어도 한 번
error를 택한 나머지 항들이 생긴다. 절댓값과 비음수성을 사용해 나머지를 모두 더하면

\[
\sum_{\varnothing\ne S\subseteq\{1,\ldots,r\}}\prod_{i\in S}\delta_i
=\prod_i(1+\delta_i)-1.
\]

Euler-factor main 항은 가정 2에 따라 \(\Pi_g\)로 합쳐지므로 (24.9)가 성립한다. □

이 정리는 signed tensor sum 전체로 일반화하지 않는다. 실제 \(F,F^2,F_2^2\)는 아래처럼
비음수 tensor 항의 합으로 전개되므로, 각 항의 상대 envelope 중 최댓값을 취하면 전체 합에도
안전하다.

유용한 후속 상계는

\[
\prod_i(1+\delta_i)-1\le e^{\sum_i\delta_i}-1,
\tag{24.10}
\]

\[
\sum_i\delta_i\le1
\quad\Longrightarrow\quad
e^{\sum_i\delta_i}-1\le2\sum_i\delta_i.
\tag{24.11}
\]

(24.9)가 정확한 finite-product 상계이고, (24.11)만 smallness gate를 필요로 한다.

## 7. 실제 \(N,W\) profile의 명시적 norm

\[
T_k=k\log k,\qquad U_k=k^{-1/2},
\]

\[
P_{a,m,q}(t)=\frac{\psi(t/a)^m}{(1+T_kt)^q}.
\]

project cutoff는 \(0\le\psi\le1\), \(\psi=1\) on \([0,0.9]\),
\(\|\psi'\|_\infty<50\)를 만족한다. 따라서

\[
\int P_{a,m,1}\ge\frac{\log(1+0.9aT_k)}{T_k},\qquad
\int P_{a,m,2}\ge\frac{0.9a}{1+0.9aT_k},
\tag{24.12}
\]

\[
\sup(P_{a,m,q}+a|P'_{a,m,q}|)\le1+50m+aqT_k.
\tag{24.13}
\]

실제 profile 대응은 다음과 같다.

| profile | \(a\) | \(m\) | \(q\) | 설명 |
|---|---:|---:|---:|---|
| \(N\) | \(U_k\) | 1 | 1 | 좁은 기본 profile |
| \(N^2\) | \(U_k\) | 2 | 2 | \(F^2,F_2^2\)의 좁은 좌표 |
| \(W\) | 2 | 1 | 1 | \(F_2\)의 넓은 좌표 |
| \(W^2\) | 2 | 2 | 2 | \(F_2^2\) diagonal |
| \(NW\) | \(U_k\) | 1 | 2 | \(N\) 지지에서 \(\psi(t/2)=1\) |

\(F_2^2\)의 diagonal tensor는 \(W^2(N^2)^{k-1}\), off-diagonal tensor는
\((NW)^2(N^2)^{k-2}\)다. \(t_m=0\) slice에도 base-base, diagonal,
base-wide, wide-cross 네 family만 생긴다. 이 목록을 코드가 직접 검사한다.

## 8. 넓은 좌표의 합 순서는 필수다

\(W^2\)는 \([0,2]\)에 지지되므로 해당 정수 변수는 \(R^2\)까지 갈 수 있다. 이를 뒤에
남겨 둔 채 기존 theory 23의 “남은 좌표마다 최대 \(\log R\)” 상계를 쓰면 안전하지 않다.

각 \(F_2^2\) tensor에서 유일한 \(W^2\) 좌표를 **먼저** 합한다. Lemma 8.4의 현재 좌표는
다음 단계의 제외 정수 \(Q_j\)에 들어가지 않는다. 이후 남은 좌표는 모두 \(N^2\) 또는
\(NW\)이므로 지지 exponent가 \(U_k\le1\)이다. 따라서 기존 공통 \(\Lambda_*\)는 그대로
유효하다. 코드의 `WIDE_SUPPORT_FIRST_APPLICATIONS`가 이 조건을 고정한다.

모든 tensor의 총 support exponent도 \(k\ge36\)에서

\[
\max\left\{kU_k,\ 2+(k-1)U_k\right\}\le k
\tag{24.14}
\]

이다. 이는 전체 크기 점검이며, 좌표 순서 조건을 대신하지 않는다.

## 9. actual application별 판정

| ID | 원문 위치 | 유형 | 이번 판정 |
|---|---|---|---|
| `L620_dW` | 620–625 | Lemma 8.4, \(F\) | smooth envelope explicit |
| `L737_canonical` | 737 | Lemma 8.4, \(F_2^2\) | smooth explicit; wide-first 필수 |
| `L752_canonical` | 752 | Lemma 8.4, \(F^2\) | smooth envelope explicit |
| `L885_W_prime` | 885–892 | Lemma 8.4, sliced \(F_2^2\) | smooth explicit; wide-first 필수 |
| `L905_W_prime` | 905–916 | Lemma 8.4, \(H\) | **PARAMETERIZED EXPLICIT:** 전역 \(C^1\) 우회와 scalar multiplier finite gate |
| `L995_a_m_W_B_r` | 995–999 | 1D Lemma 8.4, \(F_2\) | nonnegative \(N/W\) 합 envelope explicit |
| `L1015_r_W_m` | 1015–1026 | direct Lemma 8.3, \(F\) | product-profile 절대 envelope explicit |
| `L1096_W0` | 1096–1098 | direct summatory, sharp cutoff | 공식 explicit; \(\xi\log x\) 하한 OPEN |
| `L1135_W0_factor` | 1135–1141 | 1D sharp factor | 공식 explicit; \(\xi\log x\) 하한 OPEN |
| `L1135_canonical_factor` | 1135–1141 | Lemma 8.4, \(F^2\) | smooth envelope explicit |
| `L1232_canonical` | 1232–1237 | Lemma 8.4, \(F_2^2\) | smooth explicit; wide-first 필수 |

여기서 “envelope explicit”는 결합 cutoff가 들어간 실제 main integral에 대한 상대오차라고
말하지 않는다. Lemma 8.4 원문과 같이 \(\prod_i\int G_i\)로 정규화한 **절대오차 상계**다.
이 구분은 main integral이 작은 slice에서 특히 중요하다.

## 10. 공통 smooth smallness cutoff

\(y=\log R\)라 두고

\[
\Lambda_*=A+By,
\]

\[
A=2k^2\log(2k^2)+k(k-1)\log2,\qquad
B=\frac{10\alpha(2k^2-k+1)}{\theta}+k.
\]

닫힌 smooth call의 tensor family 전체에서 \(\sum\kappa_i\)의 최댓값을 \(K_{\max}\),
\(E=C_{8.3}(1/2,8)K_{\max}\)라 하자. \(y\ge1\)이면

\[
\log(A+By)\le\log(A+B)+\log y.
\]

\(E>1\)인 현재 범위에서 다음은 충분조건이다.

\[
\boxed{
y\ge\max\left\{
1,\sqrt{k}\log2,
4E\log(4E),
2E[6+\log(A+B)]
\right\}.
}
\tag{24.15}
\]

실제로 \(y\ge4E\log(4E)\)이면 \(E\log y\le y/2\), 마지막 항은
\(E[6+\log(A+B)]\le y/2\)를 준다. 따라서

\[
\frac{E[6+\log\Lambda_*]}{y}\le1.
\]

이 cutoff는 최적화하지 않은 존재형 상계보다 한 단계 나은 명시식일 뿐, 실용적인
threshold라고 보지 않는다. 예를 들어 **설명용으로만** \(k=36,\alpha=0.01,\theta=0.25\)를
넣으면

~~~text
K_max ~= 1.2425700131e7
E     ~= 9.8377549979e128
log10(log R sufficient) ~= 132.06976
~~~

이다. 이 값은 directed interval certificate가 아니고 \(\alpha,\theta\)도 최종 theorem 선택으로
인증되지 않았다. 따라서 \(R\), \(x\), \(X_{\rm cert}\)의 실제 수치로 해석하면 안 된다.

## 11. sharp cutoff 두 호출

sharp indicator에는 smooth norm을 억지로 적용하지 않고 theory 22의 summatory 식을 직접 쓴다.
\(Z=x^\xi\)일 때 product main에 대한 상대오차는

\[
\frac{C_\Sigma(1/2,8)[6+\log\Lambda_*]}{\xi\log x}.
\tag{24.16}
\]

원문은 \(\xi\gg k(\log\log x)^2/\log x\)라고만 주므로, (24.16)을 특정 error budget 아래로
내리려면 그 \(\gg\)의 수치 multiplier와 유효 시작점이 필요하다. 이것은 계산량 문제가
아니라 아직 복원되지 않은 증명 상수 문제다.

## 12. 왜 parent를 닫지 않는가

남은 두 root는 다음과 같다.

1. `L905_W_prime`: theory 25/26이 전역 \(\|H\|_{C^1}\) 요구와 scalar
   remainder multiplier를 닫았다. 이 행은 더 이상 root blocker가 아니다.
2. sharp calls: \(\xi\log x\)의 유한 하한과 공통 error budget 연결이 없다.

또한 Lemma 8.4 바깥의 Lemmas 8.5–8.6과 Propositions 9.1–9.5도 남아 있다. 따라서

~~~text
H1B-L83      ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
H1B-L84      RATE_MISSING
H1B1-PACKAGE HARD_BLOCKER
SIV-07       HARD_BLOCKER
X_cert       OPEN
~~~

를 유지한다. 실제 prime sweep, threshold calculator, Lean, 새 Python package는 이 단계에
필요하지 않았고 실행·설치하지 않았다.

## 13. 검증 계약

`tests/test_h1b1b2d_rfold_smooth_package.py`는 다음을 검사한다.

1. 11개 호출이 8 direct smooth / 2 sharp / 1 H-square-bypass로 빠짐없이 분류됨
2. 5개 실제 profile의 수치적분·표본 미분값이 증명된 보수 상계를 넘지 않음
3. \(F_2^2\) tensor family와 wide-first 순서가 고정됨
4. 유리수 finite-product identity와 수치 product/exponential 상계
5. H를 직접 smooth 함수로 취급하거나 sharp call이 smooth 경로로 들어가면 즉시 거부됨
6. 공통 cutoff가 닫힌 하위문제만 통과시키고 parent 상태를 승격하지 않음
7. source hash와 기계 계약의 fail-closed 상태

수치 표본검사는 증명을 대신하지 않는다. (24.12)–(24.15)의 해석적 증명이 주 근거이고,
시험은 구현이 그 식과 달라지는 회귀를 잡는다.

## 14. 다음 gate

직접 후속은 `H1b-1b-2d.1b`이다.

1. theory 26이 source (9.42)--(9.48)의 scalar multiplier와 finite range를 닫았다.
2. \(\xi\)의 정의·선택식을 source-trace해 \(\xi\log x\)의 finite lower bound를 만든다.
3. sharp 항까지 공통 error budget에 합친 뒤에만 `H1B-L84` 전체 승격을 재검토한다.

병렬 이론축은 `H1c-1` quantitative character/Bombieri–Vinogradov package다. 두 축이
모두 상위 proof DAG의 root dependency이므로, 어느 하나만으로 \(X_{\rm cert}\)를 계산하지 않는다.
