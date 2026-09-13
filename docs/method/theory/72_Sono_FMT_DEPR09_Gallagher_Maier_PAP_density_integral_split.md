# Sono/FMT DEP-R09 Gallagher--Maier PAP density-integral split

- 작성일: 2026-09-14 KST
- 단계: **DEP-R09 / JL7-AVERAGED-TO-PAP-SPLIT**
- 선행 정본: [Theory 71](71_Sono_FMT_DEPR09_Jutila_JL7_averaged_primitive_replay.md)
- 기계 원장: [PAP split v1](data/Sono_FMT_DEPR09_Gallagher_Maier_PAP_split_v1.json)
- 판정:
  - nonprincipal far-\(\alpha\) branch = **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT**
  - Theory 71 near-\(\alpha\) 적분 = **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT**
  - 현재 \(d=160\) certificate = **SUFFICIENT PAP GATE 불통과**
- 계속 OPEN: Gallagher explicit-formula multiplier·공통 cutoff, principal zeta,
  exceptional-character/good-modulus transfer, character orthogonality의 full numerical
  replay, \(\psi\)-to-\(\pi\), <code>PAP-11</code>, <code>DEP-R09</code>,
  fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\)

## 1. 결론

Gallagher 식 (30)의 영점 적분을

\[
 0\le\alpha\le1-\theta,\qquad
 1-\theta\le\alpha\le1-\eta
\tag{72.1}
\]

로 나누면 Theory 71이 다루지 않은 모든 \(\alpha\)를 Jutila printed all-\(\alpha\)
정리로 다시 증명할 필요는 없다. 첫 구간은 Bennett--Martin--O'Bryant--Rechnitzer
Theorem 1.1의 explicit **전 높이 영점수**로 덮고, 둘째 구간은 Theory 71의
near-one density를 정확히 적분할 수 있다.

그러나 이 연결이 곧 PAP를 닫는 것은 아니다. \(\theta=1/21,d=160\)에서
away-from-one 오차는 감소하지만, near-one 인증 상계의 \(X\to\infty\) 극한은 약
\(2.7277\times10^{13}\)이다. 양의 주항을 보장하려면 이 값이 적어도 1보다 작아야
하고, Sono의 \(1-e^{-2}\) 주항을 그대로 보존하려면 오차 예산 \(e^{-2}\)보다 작아야
한다. 현재 상계는 두 기준보다 각각 약 \(2.7\times10^{13}\)배와
\(2.0\times10^{14}\)배 크다.

> **쉬운 설명:** 앞 단계에서 “위험한 영점이 1 근처에 몇 개 있는가”를 셌다. 이번에는
> 그 결과를 소수 개수 공식에 넣었다. 1에서 멀리 떨어진 영점은 이미 충분히 안전하게
> 처리할 수 있다. 문제는 1 근처 영점의 실제 개수가 많다는 것이 아니라, 우리가 만든
> 안전 상계가 너무 큰 숫자를 붙인다는 점이다. 따라서 컴퓨터로 더 큰 \(X\)까지
> 소수를 세는 것으로 해결되지 않고, 먼저 이 증명 상수를 크게 줄여야 한다.

## 2. source-first 원문 감사

| source | 원문 확인 위치 | 읽기 방식 | 이번 역할 |
|---|---|---|---|
| Gallagher 1970, *A Large Sieve Density Estimate near \(\sigma=1\)* | printed pp.335--338, Theorems 6--7, (24), (26)--(30) | native text 우선; physical PDF pp.7--10 렌더 대조 | explicit formula 구조, Stieltjes 적분, \(T=Q^5\) |
| Maier 1981, *Chains of Large Gaps between Consecutive Primes* | printed pp.260--261, Lemmas 1--2 | native text 우선; physical pp.4--5 렌더 대조 | good modulus, \(Q=x^{1/D}\), residue-class lower bound |
| McCurley 1984 | printed pp.8--9, Theorems 1--2 | native text 우선; physical pp.2--3 렌더 대조 | predecessor의 보수적 \(c_1=1/24\) zero-free 입력 |
| Bennett et al. 2021, *Counting Zeros of Dirichlet L-Functions* | Theorem 1.1, journal p.1456 | native text 우선; arXiv audit copy p.2 렌더 대조; AMS journal metadata·statement 대조 | far-\(\alpha\) 전역 zero-count |
| Theory 71 | (71.2)--(71.3) | hash 고정 정본 | near-\(\alpha\) averaged primitive nonprincipal density |

네 PDF 모두 유효한 text layer가 있어 OCR을 사용하지 않았다. Bennett audit copy는
arXiv:2005.02989v1이고, Theorem 1.1의 문구·상수는 2021년
*Mathematics of Computation* 출판 정보와 대조했다. 출판 DOI는
[10.1090/mcom/3599](https://doi.org/10.1090/mcom/3599)다.

## 3. Gallagher에서 실제로 필요한 호출

Gallagher는 \(q\le T\le X^{1/2}\)에서 explicit formula를 적용하고 prime powers와
truncation을 처리한 뒤

\[
 \sum_{q\le Q}\sum_\chi^*
 \left|\sum_{X<p\le X+h}\chi(p)\log p\right|
 \ll h\left\{
 \sum_{q\le Q}\sum_\chi^*\sum_\rho X^{\beta-1}
 +\frac{Q^4}{T}\right\}
\tag{72.2}
\]

를 얻는다. 이어서 triple zero sum을

\[
 \mathcal S(X)=
 \log X\int_0^{1-\eta}X^{\alpha-1}N^*(\alpha,T,Q)\,d\alpha
 +X^{-1}N^*(0,T,Q)
\tag{72.3}
\]

로 쓴다. 원문은 이 단계 전체에 \(\ll\)를 사용하므로 다음은 아직 숫자가 없다.

1. explicit formula와 prime-power/truncation을 식 (72.2)로 모으는 multiplier,
2. 식 (72.2)에서 primitive character 평균을 특정 residue class로 옮기는 multiplier,
3. \(q=1\) zeta 주지표와 exceptional character 처리,
4. 최종 \(\psi\) 또는 \(\theta\) 하계를 \(\pi\) 하계로 옮기는 cutoff.

이번 단계는 식 (72.3)의 **nonprincipal zero contribution**만 수치화한다.

## 4. Bennett 전역 zero-count로 far branch를 닫기

Bennett et al. Theorem 1.1은 primitive character \(\chi\)의 conductor \(q>1\),
\(T\ge5/7\)에서

\[
\left|
N(T,\chi)-
\left\{\frac{T}{\pi}\log\frac{qT}{2\pi e}
-\frac{\chi(-1)}4\right\}
\right|
\le0.22737\ell+2\log(1+\ell)-\frac12,
\quad
\ell=\log\frac{q(T+2)}{2\pi},
\tag{72.4}
\]

를 준다. \(\ell\le1.567\)이면 \(N(T,\chi)=0\)이다.

\(Q\ge2,T=Q^5\), \(2\le q\le Q\)라 하자. \(\ell_Q\)를 \(q=Q\)에서의 값이라 두면

\[
 \ell\le\ell_Q\le\log(2QT)\le\frac76\log(QT).
\tag{72.5}
\]

또한 \(0.22737<1\), \(\log(1+\ell)\le\ell\), \(T\ge32\)를 쓰면 한 character당

\[
 N(T,\chi)\le2T\log(QT).
\tag{72.6}
\]

conductor \(q\)의 primitive character 수는 \(\varphi(q)\)보다 작거나 같으므로

\[
\begin{aligned}
 Z_{\rm np}(Q,T)
 &:=
 \sum_{2\le q\le Q}\ \sum_{\chi\bmod q}^{*}N(T,\chi)\\
 &\le2Q^2T\log(QT).
\end{aligned}
\tag{72.7}
\]

이 상계는 비주지표 family만 다룬다. conductor 1인 zeta branch는 포함하지 않는다.

## 5. far 적분과 endpoint가 정확히 합쳐진다

\(0\le\alpha\le1-\theta\)에서
\(N^*_{\rm np}(\alpha,T,Q)\le Z_{\rm np}(Q,T)\)다. 식 (72.3)의 endpoint를
far branch에 함께 넣으면

\[
\begin{aligned}
\mathcal S_{\rm far}
&\le Z_{\rm np}\log X\,
\int_0^{1-\theta}X^{\alpha-1}\,d\alpha
+X^{-1}Z_{\rm np}\\
&=Z_{\rm np}X^{-\theta}.
\end{aligned}
\tag{72.8}
\]

즉 endpoint를 따로 거칠게 더할 필요가 없다. 이제

\[
 Q=X^{1/d},\qquad T=Q^5,\qquad
 \mathcal D=Q^2T=Q^7=X^{7/d}
\tag{72.9}
\]

를 대입하면

\[
 \boxed{
 \mathcal S_{\rm far}
 \le\frac{12}{d}\log X\,
 X^{-(\theta-7/d)}.}
\tag{72.10}
\]

\(\theta=1/21,d=160\)에서는

\[
 \theta-\frac7d
 =\frac1{21}-\frac7{160}
 =\frac{13}{3360}>0,\qquad
 \frac{12}{d}=\frac3{40}.
\tag{72.11}
\]

따라서 far branch는 실제로 감소한다. \(y=(\theta-7/d)\log X\)와
\(y\le e^{y/2}\)를 쓰면 budget \(\varepsilon_F\)의 계산 가능한 충분조건은

\[
 \log X\ge
 \frac{2}{\theta-7/d}
 \log\frac{12}{d(\theta-7/d)\varepsilon_F}
\tag{72.12}
\]

이다. \(d=160,\theta=1/21,\varepsilon_F=1/100\)에서는 우변이 약
\(3912.9268\)이다.

## 6. near-one density의 정확한 적분

\(\delta=1-\alpha\)라 두고 Theory 71을 대입한다. 그 detector 변수와 PAP 변수
\(X\)를 혼동하지 않도록

\[
\begin{gathered}
 L=\log\mathcal D=\frac7d\log X,\qquad
 C_J(\theta)=\frac{884000}{9(1-\theta)^2\theta^6},\\
 \kappa(\theta)=14(1+12\theta),\qquad
 \lambda=1-\frac{\kappa(\theta)}d,\\
 A=\lambda\log X-4\log L,\quad
 B=\log(2\mathcal D),\quad
 \eta=\frac{c_1d}{5\log X},\quad
 \delta_0=\frac1L.
\end{gathered}
\tag{72.13}
\]

Theory 71의 공통 cutoff 뒤에는
\(\eta\le\delta_0\le\theta\)이고 \(A>0\)이다. 따라서
\(\max\{\delta,1/L\}\)를 \(\delta_0\)에서 **정확히** 나누어 적분하면

\[
\boxed{
\begin{aligned}
\mathcal S_{\rm near}\le2C_J\log X\Bigg\{&
\frac{(3+B/L)e^{-A\eta}}{A}
+\frac{B e^{-A/L}}{A^2}\\
&-e^{-A\theta}
\left(\frac{3+B\theta}{A}+\frac{B}{A^2}\right)
\Bigg\}.
\end{aligned}}
\tag{72.14}
\]

마지막 음의 항을 버리지 않았으므로 \(\max\)를
\(\delta+1/L\)로 바꾸는 것보다 작은 상계다. endpoint 대수는

\[
 \kappa(1/21)=22,\qquad
 \lambda(1/21,160)=\frac{69}{80}.
\tag{72.15}
\]

## 7. \(X\)를 키워도 현재 near certificate가 사라지지 않는다

\(\log X\to\infty\)에서 식 (72.14)의 우변은

\[
\boxed{
\mathcal K_\infty(d,\theta,c_1)=
2C_J(\theta)\left\{
\frac{4e^{-\lambda c_1d/5}}{\lambda}
+\frac{(7/d)e^{-\lambda d/7}}{\lambda^2}
\right\}.}
\tag{72.16}
\]

현재 보수적 \(c_1=1/24,\theta=1/21\)을 넣은 120-dps 진단은 다음과 같다.

| 항목 | 값 |
|---|---:|
| \(C_J\) | \(9{,}287{,}613{,}243{,}090\) |
| Theory 71 \(\log\mathcal D\) cutoff | \(8827.2407040965\ldots\) |
| \(d=160\)에서 유도되는 \(\log X\) cutoff | \(201765.5018079213\ldots\) |
| 그 cutoff의 식 (72.14) | \(2.7289770554758\times10^{13}\) |
| \(\mathcal K_\infty(160,1/21,1/24)\) | \(2.7276984142443\times10^{13}\) |
| \(\mathcal K_\infty(186,1/21,1/24)\) | \(2.1484606972311\times10^{13}\) |
| \(\mathcal K_\infty\le1\)인 첫 정수 \(d\) | 3856 |
| \(\mathcal K_\infty\le e^{-2}\)인 첫 정수 \(d\) | 4096 |

마지막 두 행은 이 **특정 충분 상계**의 asymptotic 진단이다. \(d=3856\) 또는
4096이 실제 PAP 정리를 준다는 뜻이 아니다. 특히 선행 Theory 58에서 fixed
\(2\times10^{-17}\) 계수의 낙관적 capacity도 \(d\le186\)이 필요했다. 따라서
큰 \(d\)로 밀어 현재 상계를 흡수하는 방법은 Sono의 fixed coefficient 연구 목적과
양립하지 않는다.

## 8. 정확한 판정

| node | 이번 판정 | 뜻 |
|---|---|---|
| <code>GMP-FAR-ALPHA</code> | **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT** | Bennett 전역 count와 endpoint-safe 적분 |
| <code>GMP-NEAR-INTEGRAL</code> | **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT** | Theory 71을 \(\delta_0=1/L\)에서 정확히 적분 |
| printed Jutila all-\(\alpha\) 정리의 필요성 | **NOT REQUIRED FOR THIS SPLIT** | far branch를 별도 explicit total count가 담당 |
| current \(d=160\) certificate | **INSUFFICIENT** | 현재 상계가 PAP 양수성 budget을 인증하지 못함 |
| Gallagher full numerical replay | OPEN | 식 (72.2)의 숨은 multiplier·cutoff 등 |
| principal / exceptional / \(\psi\)-to-\(\pi\) | OPEN | 각각 독립 proof obligation |
| <code>PAP-11 / DEP-R09 / X_cert</code> | **HARD_BLOCKER / OPEN / OPEN** | root 판정 불변 |

<code>INSUFFICIENT</code>는 실제 prime-distribution error가 크다는 명제가 아니다.
현재 증명에서 사용한 explicit upper bound가 너무 커서 필요한 결론을 보증하지
못한다는 뜻이다.

## 9. 다음 우선순위

1. \(C_J\)가 \(9.29\times10^{12}\)까지 커진 정확한 loss tree를 역추적한다.
2. residue 52, preterminal \(170/\theta^2\), detector lower와 area 손실 중 어느 항이
   가장 크게 줄일 수 있는지 sensitivity lower-target을 만든다.
3. \(d\le186\)에서 near budget \(<e^{-2}\)를 만족하려면 총 multiplier를 현재보다
   최소 약 \(1.6\times10^{14}\)배 줄여야 함을 설계 gate로 사용한다.
4. 이 coefficient gate가 현실적인 대체 density theorem 또는 구조적 cancellation으로
   통과할 전망이 생긴 뒤 Gallagher explicit-formula·principal·exceptional·
   \(\psi\)-to-\(\pi\)의 나머지 상수를 복원한다.

이 순서는 열린 부품을 무시하자는 뜻이 아니다. 이미 실패하는 가장 앞선 수치 gate를
먼저 고치지 않으면, 뒤의 multiplier를 아무리 정교하게 계산해도 \(X_{\rm cert}\)가
나오지 않기 때문이다.

## 10. 재현

~~~powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m source.dep_r09_gallagher_maier_pap_split
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest tests.test_dep_r09_gallagher_maier_pap_split -v
~~~

실제 maximal-gap 데이터, prime sweep 또는 장시간 계산은 수행하지 않았다.

## 11. 참고문헌

- P. X. Gallagher, *A Large Sieve Density Estimate near \(\sigma=1\)*,
  Invent. Math. 11 (1970), 329--339,
  DOI [10.1007/BF01403187](https://doi.org/10.1007/BF01403187).
- H. Maier, *Chains of Large Gaps between Consecutive Primes*,
  Adv. Math. 39 (1981), 257--269,
  DOI [10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- K. S. McCurley, *Explicit Estimates for the Error Term in the Prime Number
  Theorem for Arithmetic Progressions*, J. Number Theory 19 (1984), 317--330,
  DOI [10.1016/0022-314X(84)90089-1](https://doi.org/10.1016/0022-314X(84)90089-1).
- M. A. Bennett, G. Martin, K. O'Bryant, A. Rechnitzer,
  *Counting Zeros of Dirichlet L-Functions*, Math. Comp. 90 (2021), 1455--1482,
  DOI [10.1090/mcom/3599](https://doi.org/10.1090/mcom/3599),
  arXiv [2005.02989](https://arxiv.org/abs/2005.02989).
