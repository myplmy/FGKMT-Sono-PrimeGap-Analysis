# Sono/FMT H1b-P92a: actual identity-form weighted Proposition 9.2

- 작성: 2026-09-09 KST
- 증거 수준: PROJECT FINITE PROOF; 실제 소수 실험·Lean 인증 아님
- 범위: FGKMT Section 8의 identity-selected actual P9.2 호출
- 상태: ACTUAL INPUTS PARAMETERIZED EXPLICIT; general P9.2와 전체 good-weight는 미완료
- 검산: source/h1bp92a_identity_prime_moment.py
- 계약: data/Sono_FMT_H1bP92a_identity_prime_moment_v1.json
- 검토: ../../review/50_20260909_H1bP92a_weighted_moment_타당성검토.md

## 1. 결론과 해석 범위

외부 크기를 \(X=2T\)라 하고
\[
 L=\log T,\quad k=\lfloor L^{1/5}\rfloor,\quad
 R=(T/2)^{1/9},\quad y=\log R=(L-\log2)/9
 \tag{44.1}
\]
로 둔다. 로그는 자연로그다. 아래 \(F\)는 Maynard의 다변수 sieve profile이며,
경험적 분석의 한 변수 FGKMT scale \(F(x)\)와 다른 함수다.

actual admissible primitive linear forms, \(\alpha=2,\theta=1/3\),
\(|a_i|,|b_i|\le T^2\), identity \(L_m(n)=n\), 기존 construction의 \(B,W,\lambda,w\)를 쓴다.
음수 기울기는 form 전체의 부호를 바꾸어 divisibility·root count를 보존한다.
H1c-1b.4e의 같은 exceptional \(B\)와 closed Hypothesis input을 사용한다.

\[
\begin{split}
N&=\#(\mathbb Z\cap[T,2T]),\\
P_c&=\#(\mathbb P\cap[T,2T]),\qquad P_o=\pi(2T)-\pi(T),\\
\mathcal M(P)&=(B/\varphi(B))^{k-1}\mathfrak S_B P\,y^{k+1}J(F),\\
\mathcal A&=(B/\varphi(B))^k\mathfrak S_B N\,y^{k-1}I(F),\\
d_k&=k^{-190k^2}.
\end{split}
\tag{44.2}
\]

이번 package의 보수적 충분조건은
\[
 \boxed{k\ge10^{200},\quad\text{즉 }X\ge2\exp(10^{1000}).}
 \tag{44.3}
\]
이 조건에서 아래 finite inequalities를 얻는다.
\[
\left|\sum_{T\le n\le2T}1_{\mathbb P}(n)w(n)-\mathcal M(P_c)\right|
\le L^{-1/10}\mathcal M(P_c)+d_k\mathcal A ,
\tag{44.4}
\]
\[
\begin{split}
\left|\sum_{T<n\le2T}1_{\mathbb P}(n)w(n)-\mathcal M(P_o)\right|
&\le L^{-1/10}\mathcal M(P_o)
 +(d_k+3e^{-L/2})\mathcal A\\
&\le L^{-1/10}\mathcal M(P_o)+\mathcal A .
\end{split}
\tag{44.5}
\]
따라서 actual P9.2의 상대오차·가법오차 multiplier를 각각 1로 택할 수 있다.
최적 multiplier나 최소 시작점이라는 뜻은 아니다.

**(44.3)은 이 weighted-moment child 하나의 충분조건이지 Sono의 \(X_{\rm cert}\)가 아니다.**
여기까지 소수를 세거나 나열한 것도 아니다. 증명에 등장하는 \(\log T\)와 차원의 크기를
표현한 식이다. actual singular-series의 공통 \(\mathfrak S\) 치환, \(\tau,u\) 정규화,
P91/P95 및 hypergraph/PAP/UB 공통 budget은 남는다.

## 2. 선행연구 우선 조사

직접 원천은 Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
arXiv:1405.2593, 출판 pp.1540--1544, Proposition 9.2와 Lemma 9.3이다.
실제 선택은 FGKMT,
[*Long Gaps Between Primes*](https://doi.org/10.1090/jams/876),
arXiv:1412.5029, pp.95,98--102의 Definition 2, Theorem 6, Section 8을 따른다.

| 원문 위치 | 재사용/보완 |
|---|---|
| Maynard (9.16)--(9.19), pp.1540--1541 | CRT, \(D'_k,r_m=1\), identity prime discrepancy |
| (9.20)--(9.21) | 정확한 quadratic local matrix: 대각 \(p-2\), 비대각 \(-1\) |
| Lemma 9.3, (9.22)--(9.23) | theory 26의 \(C_Y\)와 Lemma 8.2 multiplier 89 |
| (9.24)--(9.34) | 재배치 오차, squarefree tail, Euler 정규화 |
| (9.35)--(9.38) | 전역 smooth \(H\) 대신 theory 25의 \(A^2,AB,B^2\) |
| FGKMT Definition 2·p.101 actual call | closed \([T,2T]\)와 외부 \((T,2T]\)의 lower atom |

표적 검색에서 동일 profile·growing \(k\)·끝점·수치 multiplier를 모두 제공하는
출판된 drop-in package는 확인하지 못했다. 전 세계 novelty 주장은 아니다.
공개 [PrimeGapsLib의 S2m error proof](https://github.com/AxiomMath/PrimeGapsLib/blob/main/PrimeGapsTheory/Sieve/S2m/Error/Main.lean)
도 확인했다. 그 weighted-modulus lemma는 fixed \(k\), 존재형 \(C,N_0\), 별도
level-of-distribution 가정을 사용하므로 본 수치 package의 입력으로 채택하지 않았다.
해당 repository의 전체 axiom/build audit을 했다는 뜻도 아니다.

## 3. 닫힌 입력과 새 uniformity 보정

기존 project proof로부터 다음을 사용한다.

1. theory 43: closed Hypothesis constants \(1,1,2\);
   \(\sum_{q\le T^{1/3},(q,B)=1}E_q\le P_c/L^{100k^2}\).
2. theories 22--24: corrected one-step \(C_{8.3}(1/2,8)<10^{123}\),
   support-scaled smooth product error.
3. theory 26: scalar remainder \(C_Y<10^{123}\), multiplier 89와 exact prefactor.
4. theories 17,28: \(\mathfrak S_B>e^{-9k/2}\), \(I(F)\ge(2k\log k)^{-k}\),
   \(\lambda_{\max}\le e(y/k)^k\)와 (28.13)의 pointwise weight envelope.

기존 theory 28의 \(I(F_1)/I(F)\le2^k\)는 **고정 \(k\)에서 유효**하다.
그러나 \(k=\lfloor L^{1/5}\rfloor\)를 택한 뒤 \(L\)을 키우면 이 exponential loss를
polynomial \(L\)-오차로 흡수할 수 없다. 따라서 그것을 이 경로에 그대로 대입하지 않는다.
다음 절은 H1a의 확률적 적분 논증을 재사용한 별도 growing-dimension 비교다.
기존 fixed-parameter P94 certificate는 무효화하지 않지만, 그 강한 \(2^{-k}\) gate를
maximal growing-dimension 경로에 적용하려면 별도 후속 교정이 필요하다.

## 4. 큰 차원에서의 uniform integral comparison

\[
 \ell=\log k,\quad K=k\ell,\quad U=k^{-1/2},\quad q=9/10,
 \quad n(t)=\frac{\psi(t/U)}{1+Kt},\quad h(t)=\frac{\psi(t/2)}{1+Kt}.
\]
기존 cutoff는 decreasing, \(0\le\psi\le1\), \(\psi=1\) on \([0,q]\),
\(\psi=0\) on \([1,\infty)\), \(|\psi'|<50\)다.
\[
F=\psi(\textstyle\sum t_i)\prod n(t_i),\quad F_1=\prod n(t_i),
\quad F_2=\sum_jh(t_j)\prod_{i\ne j}n(t_i).
\]
\(a=\int n^2,\ b=\int n,\ c=\int h,\ d=\int h^2\)라 쓰면 \(k\ge36\)에서
\[
a\ge\frac1{2K},\quad d\le\frac1K,\quad
b\ge\frac{\ell}{2K}=\frac1{2k},\quad c\le\frac2k,\quad c/b\le4.
\tag{44.6}
\]
예를 들어 \(b\ge K^{-1}\log(1+q\sqrt{k}\ell)\ge\ell/(2K)\)이며
\(1+2k\ell\le k^2\)에서 \(c\le2/k\)다.

독립변수 \(Y_i\)의 밀도를 \(n(t)^2/a\)로 잡는다. \(s=\sqrt{k}\ell\)라 두면
\[
\mathbb E\sum_{i=1}^kY_i
 \le(1+1/(qs))\frac{\log(1+s)}{\ell},\qquad
\operatorname{Var}\sum_{i=1}^kY_i
 \le\frac{1+1/(qs)}{\sqrt{k}\ell}.
\tag{44.7}
\]
이는 \(a\ge K^{-1}(1+1/(qs))^{-1}\),
\(\int_0^U t/(1+Kt)^2dt\le K^{-2}\log(1+s)\),
\(\int_0^U t^2/(1+Kt)^2dt\le U/K^2\)에서 따른다.

모든 \(k\ge10^{50}\)에서 \(\ell>100\), \(\log(2\ell)/\ell<0.06\)이고
\(\log(1+s)\le\ell/2+\log(2\ell)\)다. 따라서 평균은 \(3/5\) 미만,
분산은 \(1/16\) 미만이며 \(U<1/100\)이다.
\(q-U-3/5>1/4\)이므로 Cantelli 부등식은
\[
\Pr(\sum_{1}^{k}Y_i\le q)>1/2,\qquad
\Pr(\sum_{1}^{k-1}Y_i\le q-U)>1/2
\]
를 준다. 두 번째 사건에서는 inner \(t_m\in[0,U]\) 전체에서 cutoff가 1이다. 따라서
\[
\boxed{I(F_1)\le2I(F),\qquad J(F_1)\le2J(F).}
\tag{44.8}
\]
이는 수치 표본검사가 아니라 모든 해당 \(k\)에 대한 증명이다.

Cauchy와 Minkowski, (44.6)을 적용하면
\[
I(F_2)\le4k^2 I(F),\qquad J(F_2)\le8k^2J(F).
\tag{44.9}
\]
구체적으로 \(\sqrt{J(F_2)}\le[c+(k-1)b\sqrt{d/a}]a^{(k-1)/2}
\le2kb\,a^{(k-1)/2}\)이다.
\(A_0=b\prod_{i\ne m}n(t_i)\), \(A=\int Fdt_m\), \(B_*=\int F_2dt_m\),
\(U_* =F_2(t_m=0)\)라 쓰면
\[
\int A_0B_*\le4kJ(F),\quad
\int B_*^2\le8k^2J(F),\quad
\int U_*^2\le16k^4J(F).
\tag{44.10}
\]
마지막 식은 \(\int U_*^2\le2k^2a^{k-1}\),
\(J(F)\ge b^2a^{k-1}/2\), \(b\ge1/(2k)\)에서 따른다.
이는 모든 \(k\)-dimensional integral을 실제로 적분하라는 계산 지시가 아니다.

## 5. smooth/scalar 호출의 공통 작은 오차

실제 제외모듈 상계는
\[
\Lambda_*=
2k^2\log(2k^2)+k(k-1)\log2+
\{60(2k^2-k+1)+k\}y.
\tag{44.11}
\]
theories 24--26의 각 tensor coordinate는 \(n,n^2,h,h^2,nh\) 중 하나다.
integral 하한 \(\ge1/(2K)\), scaled \(C^1\) numerator \(\le5K\)에서
각 \(\Omega\le10K^2\)다. cutoff derivative는 최대 100, support는 최대 2이므로
모든 필요 family에 공통 \(\mathcal K_*=3000k^3\ell^2\)를 쓸 수 있다.
\(h^2\) support-\([0,2]\) 좌표를 먼저 합하는 기존 순서를 유지한다.
\[
\delta=\frac{10^{123}(6+\log\Lambda_*)\mathcal K_*}{y},\quad
\varepsilon=\frac{10^{123}K(\log y)^2}{y}.
\tag{44.12}
\]
모든 \(k\ge10^{50}\)에서
\[
y\ge k^5/30,\quad 5\ell-4<\log y<6\ell,\quad
6+\log\Lambda_*\le2\log y,\quad 6+\log\Lambda_*\le12\ell,
\]
따라서
\[
\delta\le10^{130}\ell^3/k^2,\qquad
\varepsilon\le10^{127}\ell^3/k^4.
\tag{44.13}
\]
증명: \(\Lambda_*\le121k^2y\), \(\log121<5\)를 적용한다.
기존 scalar theorem의 determinant gate도
\(C_\Delta=30^{1/5}(\log2+120)<363,\ \log C_\Delta<6\)와
\(\log y>496\)에서 성립한다. \(y/\sqrt{k}\ge\log2\)도 만족한다.

이제 \(k\ge10^{200}\)이면 \(\delta<1/2,\ k\varepsilon<1,\ \varepsilon<1\)이다.
모든 tensor product error는 \(e^\delta-1\le2\delta\), positive upper factor는
\(e^\delta<e<3\)로 제어된다. O(k) 길이의 이전 evaluator를 이 거대한 \(k\)로
실행하지 않고, 증명에서 얻은 공통 scalar majorant만 평가한다.

## 6. weighted prime discrepancy의 유한 전달

각 허용 \(W\)-residue에서 (9.16)의 compatible pair는
\(q=W\prod_i[d_i,e_i]\) 하나와 coprime residue 하나를 정한다.
identity-selected \(d_m=e_m=1\), \(q\) squarefree, \((q,B)=1\)이다.
\[
\log W\le2k^2\log(2k^2)\le L/9,\qquad WR^2\le T^{1/3}.
\tag{44.14}
\]
\(k\ge36\)의 \(\log k\le k/2\)로 첫 부등식을 확인할 수 있다.
고정 \(q\)에서 각 \(p\nmid W\)에는 최대 \(3(k-1)\)개의 coordinate/membership
선택이 있으므로 pair multiplicity는 정확한 계수 1로 \(\tau_{3k}(q)\) 이하이다.

\(E_q=\max_{(a,q)=1}|P_c(q,a)-P_c/\varphi(q)|\)라 하면
\(E_q\le2N/\varphi(q)\), \(\sum E_q\le N/L^{100k^2}\)다. Cauchy에 의해
아래의 모든 \(E_q\)-합은 \((q,B)=1\)에 제한한다. 이후의 비음수 harmonic divisor
majorant에서만 그 제한을 버린다.
\[
\sum_{q\le T^{1/3}}\mu^2(q)\tau_{3k}(q)E_q
\le\sqrt2N L^{-50k^2}
\left(\sum_{q\le T^{1/3}}\frac{\mu^2(q)\tau_{3k}(q)^2}{\varphi(q)}\right)^{1/2}.
\]
squarefree \(q\)에서 \(1/\varphi(q)\le2^{\omega_0(q)}/q\)이므로 summand를
\(\tau_{18k^2}(q)/q\)로 상계한다. 여기 \(\omega_0\)는 prime-factor 개수로,
linear-form root count \(\omega(p)\)와 다르다.
곱으로 푼 harmonic divisor sum은
\[
\sum_{n\le z}\tau_j(n)/n\le(1+\log z)^j
\]
이다. \(1+L/3\le L\)에서 weighted discrepancy는
\(\sqrt2 N L^{-41k^2}\) 이하다.
\(\lambda_{\max}\le e(y/k)^k\), \(W\)개의 residue upper count를 곱하면 전체 분포오차는
\[
D_{\rm dist}\le\sqrt2e^2NW(y/k)^{2k}L^{-41k^2}.
\tag{44.15}
\]
\(\mathfrak S_B\ge e^{-9k/2}\), \(I(F)\ge(2k\ell)^{-k}\)를 넣으면
\[
\log(D_{\rm dist}/\mathcal A)
\le4+2k^2+\tfrac{11}2k-(201k^2-5k-5)\ell
\le-190k^2\ell .
\tag{44.16}
\]
마지막 부등식은 \(\ell\ge1\)과 \(9k^2-\tfrac{21}2k-9\ge0\)으로 충분하다.

## 7. diagonal main term과 정확한 Euler cancellation

\(D=WB/\varphi(WB)\), \(S=\mathfrak S_{WB}\), \(K_0=D^{k-1}Sy\)라 쓴다.
Lemma 9.3의 정규화는
\[
y_{\mathbf r}^{(m)}=K_0 Z_{\mathbf r},\quad
|Z_{\mathbf r}-A(\mathbf t_{\mathbf r})|
\le\varepsilon B_*(\mathbf t_{\mathbf r}).
\tag{44.17}
\]
따라서 전역 smooth \(H\)를 가정하지 않고
\(|Z^2-A^2|\le2\varepsilon AB_*+\varepsilon^2B_*^2\)를 합한다.
theory 25의 일곱 tensor class가 모든 항을 포함한다.

identity의 각 \(p\nmid WB\)에 대해 \(D'_k,r_m=1\)에는 \(\omega(p)-1\)개의 slot이 있다.
실제 \(r\)에 등장하는 소수는 \(\omega(p)\ge2\)이고, \(\omega(p)=1\)이면 slot이 없다.
profile 밖의 \(Z\)는 0으로 연장한다. 고정 product의 모든 허용 slot 배치를 포함하면
원래 합의 zero term만 더하므로 아래 row-sum 항등식을 사용할 수 있다.
(9.21)의 row sum은 \((p-2)-(\omega(p)-2)=p-\omega(p)\)다.
따라서 \(y_{\mathbf s}^{(m)}\)를 \(y_{\mathbf r}^{(m)}\)로 바꾼 부분은 정확히
\(\sum(y_{\mathbf r}^{(m)})^2/\varphi_\omega(r)\)다.
그 smooth sum의 local Euler factor
\[
\left(1+\frac{\omega-1}{p-\omega}\right)(1-1/p)^{k-1}
\]
에 \(S\)의 local factor를 곱하면 **정확히 1**이다.
diagonal scale은 \(D^{k-1}S y^{k+1}J(F)\)가 된다.
(44.8)--(44.12)와 positive smooth upper factor \(<3\)에서 relative error는
\[
E_{\rm diag}\le4\delta+24k\varepsilon+24k^2\varepsilon^2 .
\tag{44.18}
\]
\(A^2\) error는 \(2\delta J(F_1)\), \(AB_*\) upper sum은 \(12kJ(F)\),
\(B_*^2\) upper sum은 \(24k^2J(F)\)를 사용했다.

## 8. off-diagonal 재배치 오차

\(r=\prod r_i=\prod s_i=s\)이고 \(A_r\)를 서로 다른 coordinate로 옮겨진 소수들의
곱이라 하자. Lemma 8.2의 analytic proof는 unchanged \(t_m\ge0\)에서도 성립한다.
좌표의 로그 이동량, \(|\psi'|<50\), 감소성만 사용하고 unchanged coordinate가
정수의 로그라는 성질을 사용하지 않기 때문이다. \(t_m\)에 대해 적분하면
\[
|A(\mathbf t_r)-A(\mathbf t_s)|
\le89K\frac{\log A_r}{y}(B_*(\mathbf t_r)+B_*(\mathbf t_s)).
\]
\(b,c\le2/k\)에서 \(B_*\le(2/k)U_*\),
\(\varepsilon\le1\)에서 \(|Z_r|\le4U_*(\mathbf t_r)/k\)다.
\(A_r>1,\log A_r\ge\log2>1/2,\log y\ge1\)을 쓰면
\[
|Z_r-Z_s|\le
C_D\frac{K(\log y)^2}{ky}\log A_r\,(U_*(\mathbf t_r)+U_*(\mathbf t_s)),
\quad C_D=2(89+2C_Y)<5\cdot10^{123}.
\tag{44.19}
\]

대칭 합에서 \(U_rU_s\le(U_r^2+U_s^2)/2\)를 사용한다. \(A_r\)를 제거한 vector는
여전히 \(D'_k,r_m=1\)이고, 감소성에서 \(U_{r/A_r}\ge U_r\)다.
재구성 slot 수는 \(\prod_{p\mid A_r}(\omega(p)-1)\le\prod_{p\mid A_r}\omega(p)\)이다.
(9.26)--(9.30)의 가중 tail은
\[
\sum_{\substack{A\ {\rm squarefree}\\(A,WB)=1}}
\frac{\log A\prod_{p\mid A}\omega(p)^2}{\prod_{p\mid A}(p-\omega(p))^2}
\le72\ell .
\tag{44.20}
\]
모든 소수는 \(p>2k^2\)이고
\[
\prod_{p>2k^2}(1+4k^2/p^2)\le e^2<9,\quad
4k^2\sum_{n>2k^2}\frac{\log n}{n^2}\le8\ell
\]
이므로 성립한다. 이 단계의 계수는 \(8\) (대칭/pointwise),
\(72\ell\) (tail)로 분리해 추적한다.

남은 slice sum의 denominator는 \(g(p)=(p-\omega)^2/(p-1)\)이다.
그 Euler factor와 \(S\)를 곱하면 정확히
\[
1+\frac{(\omega-1)^2}{(p-\omega)(p-1)}
\]
이며 전체 곱은 \(e^2<9\) 이하다. positive smooth upper factor \(<3\)까지 합하면
slice sum은 \(27\,y^{k-1}D^{-(k-1)}S^{-1}\int U_*^2\) 이하다.
(44.10), (44.19), (44.20)을 넣으면 \(8\cdot72\cdot27\cdot16=248832\)에서
\[
E_{\rm off}\le248832 C_D\,\frac{k^3\ell^2(\log y)^2}{y}
\le10^{133}\frac{\ell^4}{k^2}.
\tag{44.21}
\]
\(D'_k\)를 근거 없이 다른 support로 교체하지 않으며 wide coordinate first도 보존한다.

## 9. 상대오차의 합성

(44.13), \(k\varepsilon<1\), (44.18), (44.21)에서
\[
E_{\rm diag}+E_{\rm off}\le10^{135}\ell^4/k^2.
\tag{44.22}
\]
모든 \(k\ge10^{50}\)에서 \(\log k\le k^{1/8}\)이다. 첫 endpoint에서 확인하고
\(k^{1/8}/\log k\)의 도함수가 \(\log k>8\)에서 양수임을 쓴다. 따라서
\[
10^{135}\ell^4/k^2
\le10^{135}/k^{3/2}
\le1/(2\sqrt{k})
<(k+1)^{-1/2}<L^{-1/10}
\]
가 모든 \(k\ge10^{200}\), \(k^5\le L<(k+1)^5\)에서 성립한다.

마지막 \(W\)-residue prefactor는 \(\varphi_\omega(W)P_c/\varphi(W)\)다.
이를 \(D^{k-1}S\)와 곱하면 \(p\mid W\)마다
\[
\frac{p-\omega}{p-1}\left(\frac p{p-1}\right)^{k-1}
=\left(1-\frac\omega p\right)(1-1/p)^{-k}
\]
이므로 \((B/\varphi(B))^{k-1}\mathfrak S_B P_c\)가 된다.
이로써 (44.4)의 주항·오차 prefactor가 닫힌다.

## 10. closed에서 외부 prime interval로 가는 lower atom

\(T\)가 정수 소수일 때만 \(a_T=1\), 나머지는 \(a_T=0\)라 둔다.
\[
S_o=S_c-a_Tw(T),\qquad P_o=P_c-a_T .
\tag{44.23}
\]
raw count 하나를 빼는 비용과 weight 하나를 빼는 비용은 다르다.
theory 28의 pointwise envelope에서
\[
w(T)\le e^2(y/k)^{2k}e^{2y}(1+y)^{2k}.
\]
\(N\ge T/2\)와 동일한 주항 하한으로
\[
\log(w(T)/\mathcal A)
\le3+\tfrac{15}2k+(3k+1)\log L-\tfrac79L
\le-\tfrac12L .
\tag{44.24}
\]
마지막 단계는 \([3+7.5k+(3k+1)\log L]/L\)의 감소성과
\(4(15k^2+13k+3)\le k^5\ (k\ge36)\)으로 충분하다.

prime-count atom도 별도 제어한다. Cauchy에서 \(J(F)\le U I(F)\)이므로
\[
\frac{\mathcal M(1)}{\mathcal A}
\le\frac{2y^2}{T\sqrt{k}}\le e^{-L/2}.
\tag{44.25}
\]
마지막은 \(y\le L,\ 3\log L\le L/2\)에서 충분하다.
\(\delta_{\rm rel}=L^{-1/10}\le1\)에서
\[
|S_o-\mathcal M(P_o)|
\le\delta_{\rm rel}\mathcal M(P_o)
+[d_k+(1+\delta_{\rm rel})e^{-L/2}+e^{-L/2}]\mathcal A .
\]
이것이 (44.5)다. \(d_k+3e^{-L/2}<1\)은 (44.3)에서 충분한 여유로 성립한다.
소수가 아닌 실수 \(T\)에도 atom이 0인 같은 논증이 적용된다.

## 11. 검증과 명시적 한계

- evaluator는 \(k,L\)의 정확한 integer/Fraction dimension bin을 먼저 확인한다.
  \(L=k^5-1\), \(L=(k+1)^5\)를 rounded log로 통과시키지 않는다.
- \(k\)개 원소 배열, \(T=\exp L\), 실제 prime list, \(k^{190k^2}\)를 만들지 않는다.
  마지막 양은 \(\log d_k=-190k^2\log k\)로만 저장한다.
- 1차 검산은 rational local identities, 독립 slot enumeration, endpoint toy,
  universal inequality witnesses와 scalar regression이다.
- 자동 PASS는 이 문서의 증명을 Lean으로 인증하거나 독립 심사한 것이 아니다.
- general affine-selected P9.2, 임의 \(\mathcal A\), full Proposition 6.1,
  PAP/UB/hypergraph, \(X_{\rm cert}\)는 자동 승격하지 않는다.
- FGKMT의 \(S(\widetilde{\mathcal L})=(1+O(k/X))S\), weight 변환,
  \(\tau,u\) 상대오차 전달은 본 theorem에 포함하지 않는다.

다음 gate는 H1b-P91a: 같은 uniform integral comparison으로 unweighted first moment를
닫고, P94의 fixed-k gate와 maximal growing-k 경로 사이를 유한식으로 잇는 것이다.
