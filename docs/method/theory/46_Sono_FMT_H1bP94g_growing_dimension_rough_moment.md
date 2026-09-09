# Sono/FMT H1b-P94g: growing-k rough-prime moment와 실제 shifted interval

- 작성: 2026-09-09 KST
- 증거 수준: PROJECT FINITE ANALYTIC PROOF; 독립 심사·Lean 인증 아님
- 정본 계약: data/Sono_FMT_H1bP94g_growing_dimension_v1.json
- 검산: source/h1bp94g_growing_dimension.py
- 검토: ../../review/52_20260909_H1bP94g_growing_dimension_타당성검토.md
- 상태: FILTERED ACTUAL P94 GROWING-DIMENSION CHILD EXPLICIT; 공통 정규화·X_cert OPEN

## 1. 결론·변수·조건

[theory 45](45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md)의 외부 변수와
명시적 Maynard W-filtered weight를 유지한다.
\[
 L=\log(X/2),\quad k=\lfloor L^{1/5}\rfloor\ge10^{200},\quad
 \ell=\log k,\quad y_R=\log R=(L-\log2)/9,\quad
 Y=\frac{X\log X\log_3X}{153600\log5\,\log_2X}.
 \tag{46.1}
\]
모든 로그는 자연로그다. 다변수 profile F는 empirical F(x)가 아니다.

고정 \(C_h\ge1\)에 대해
\[
 |h|\le C_hY/X,\quad h\in\mathbb Z\setminus\{h_1,\ldots,h_k\},\quad
 \log C_h\le L/4
 \tag{46.2}
\]
를 둔다. \(p\in\mathbb P\cap(X/2,X]\), admissible distinct
\(h_i\in[1,2k^2]\), 기존 같은 \(B\le(X/2)^2\)를 사용한다.
(46.2)는 원문의 \(h=O(Y/X)\)에 숨은 범위 상수를 명시한 것이다.
C_h=1만 다루거나, 임의 h에 대해 무조건 성립한다고 범위를 바꾸지 않는다.
임의의 고정 C_h에서 충분한 child cutoff는
\[
 X\ge2\exp\{\max(10^{1000},4\log C_h)\}.
 \tag{46.3}
\]

\[
 a=\lfloor X\rfloor,\quad b=\lfloor Y\rfloor,\quad T_0=b-a,\quad
 b_0=-b+2a,\quad v=\log T_0,
\]
\[
 \mathcal L^h_p=\{n+b_0+(h_i-h)p\}_{i=1}^k,\qquad L_0(n)=n+b_0,
 \quad\Delta=p^k\prod_i|h_i-h|\ne0.
 \tag{46.4}
\]
actual local scale은 T0이며 외부 X가 아니다.

정수 \(I=[T_0,2T_0]\cap\mathbb Z\), \(N=T_0+1\),
\(\xi=1/30\), \(\mathcal S_v=\{m\ge1:s\mid m\Rightarrow s>T_0^\xi\}\)를 정의한다.
\(s\)는 소수다. 다음은 **actual filtered construction**에 대한 상계다.
\[
 \boxed{\sum_{n\in I}1_{\mathcal S_v}(L_0(n))w^*_{\mathcal L^h_p}(n)
 <T_{94},\quad
 T_{94}=30\frac{\Delta}{\varphi(\Delta)}
 (B/\varphi(B))^k\mathfrak S_B(\mathcal L_p)\,
 N y_R^{k-1}I_k(F).}
 \tag{46.5}
\]
따라서 표준 T94에 대한 정수 multiplier 1을 쓸 수 있다.
이는 theory 31의 fixed-parameter multiplier 13을 부정하거나 모든 기존 parameter에서
1로 낮춘다는 뜻이 아니다. **훨씬 강한 growing-k regime**에 대한 successor다.

원래 \(w(p,n)=1_{[-Y,Y]}(n)w^*_{\mathcal L_p}(n)\)에 대해서도
\[
 \boxed{\sum_{q\in\mathbb P\cap(X,Y]}w(p,q-hp)
 \le \frac{\mathcal M_pY}{(\log_2X)^{10}},\qquad
 \mathcal M_p=(B/\varphi(B))^k\mathfrak S_B(\mathcal L_p)y_R^kI_k(F).}
 \tag{46.6}
\]
이는 아직 공통 \(\mathfrak S,\tau,u\)나 p-average로 바꾼 전체 FGKMT (6.6)이 아니다.
**(46.3)은 child 충분조건이지 최적 임계값·전체 X_cert·prime-sweep 결과가 아니다.**

## 2. 선행증명 조사와 재사용

직접 source:

1. Maynard, [Dense Clusters of Primes in Subsets](https://doi.org/10.1112/S0010437X16007296),
   arXiv:1405.2593, 출판 pp.1547--1550, P9.4 (9.49)--(9.70).
2. FGKMT, [Long Gaps Between Primes](https://doi.org/10.1090/jams/876),
   arXiv:1412.5029, pp.99--102, 특히 p.102의 (6.6) 적용.
3. [theory 27](27_Sono_FMT_H1b1b2d1b_sharp_xi_logx_scale.md): strict 두 sharp 합.
4. [theory 29](29_Sono_FMT_H1b2a1_Proposition94_exact_Euler_normalization.md):
   exact Euler \(e^{2+6/k}\) 및 residue factor.
5. [theory 30](30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md):
   정수 discrepancy·tuple multiplicity·log error.
6. [theory 31](31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md):
   source 순서의 finite 합성. 단, 이전 \(2^{-k}\) gate는 사용하지 않는다.
7. [theory 44 §§4--5](44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md):
   uniform \(I(F_1)\le2I(F)\), common scalar delta.
8. [theory 45 §2](45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md): W-filter와 exact shift.

표적 검색에서 같은 profile, actual shifted scale, growing k, 명시 오차를 한 번에 제공하는
drop-in theorem은 확인하지 못했다. 이를 전 세계 부재·novelty로 주장하지 않는다.
관련 후속 arXiv:1804.06290의 정확한 제목은 *Weighted Average Number of Prime m-tuples
lying on an Admissible k-tuple of Linear Forms*이다. 이전 theory 31의 제목 표기는 잘못됐으며
새 수치 정리의 입력으로 채택하지 않았다. 원문·기존 정본 파일 자체의 hash는 보존한다.
이번 증명은 기존 finite child를 재사용하고 실제 변수·uniform 비교의 누락 연결만 채운다.

## 3. actual interval·support·rough cutoff 감사

원래 q를 n=q-hp로 쓰고
\[
 t=n+b-2a+hp=q+b-2a
\]
로 옮기면 정수 q의 구간은 정확히
\[
 q\in(X,Y]\cap\mathbb Z\quad\Longleftrightarrow\quad
 t\in(T_0,2T_0]\cap\mathbb Z.
 \tag{46.7}
\]
왼쪽 끝 T0를 포함하는 등호가 아니다. 닫힌 I로 늘리는 것은 모든 항이 비음수이므로
안전한 **상계**다. 추가 endpoint를 무심코 동등식에 넣지 않는다.

또 임의 \(h=O(Y/X)\)에서 \(|q-hp|\le Y\)는 자동이 아니다.
원래 support indicator를 제거하는 것도 등호가 아닌 상계다. 두 손실 모두 상계 방향이며
누락된 음수 항이나 취소를 가정하지 않는다.

form 값은
\[
 t+b_0+(h_i-h)p=q+(h_i-h)p=n+h_ip
\]
로 정확히 같으므로 filter와 divisibility, 이동된 lambda, singular series가 보존된다.
\(L_0(t)=q\)이고 추가 form의 discriminant는 (46.4)다.

u=log X=L+log2라 두면 theory 45의 하계는 실제로
\(Y/X\ge\sqrt u/307200>4\)를 준다. 또한 Y<Xu. 따라서
\[
 X\le Y/2\le T_0<Y,\quad N\le Y,\quad L\le v\le2L.
 \tag{46.8}
\]
예: T0>=Y-X-1>=Y/2, X>=2를 이용한다.
이에 따라
\[
 T_0^{1/30}\le R\le T_0^{1/9},\quad
 k^5\le v,\quad T_0^{1/30}<X.
 \tag{46.9}
\]
첫 식은 \(2L/30\le(L-\log2)/9\), 마지막은 v/30<=L/15<log X에서 따른다.
따라서 모든 q>X는 local rough cutoff \(T_0^{1/30}\)보다 크다.
외부 \(X^{1/30}\)와 local \(T_0^{1/30}\)를 동일하다고 하지 않는다.

### 3.1 coefficient·B·Delta의 조건

u>=2k^2, C_h>=1 및 Y/X<u이므로
\[
 |b_0|\le Y+2X,\quad
 |b_0+(h_i-h)p|\le(4+C_h)uX\le5C_huX.
\]
\(\log C_h\le L/4\), \(\log(5u)\le L/2\)에서
\(\log(5C_hu)\le3L/4<\log X\)다. 따라서 모든 slope/intercept는
\(T_0^2\) 이하이고 B<=(X/2)^2<=T0^2이다.
실제 alpha=2, theta=1/3의 local-factor package를 **T0에서** 적용할 수 있다.
joint tuple에 추가 L0까지 admissible일 것을 요구하지 않는다. 작은 소수에서 허용 residue가
없으면 해당 합은 0이고, 큰 소수에서는 omega*<=k+1<p이다.

## 4. growing dimension에 맞는 smooth·sharp 입력

기존 제외모듈 공통 상계
\[
 \Lambda_*=2k^2\log(2k^2)+k(k-1)\log2+
 \{60(2k^2-k+1)+k\}y_R
\]
는 local R lower bound와 coefficient bound로 여전히 유효하다. Theory 44의 실제
canonical factor에 대한 공통 delta를
\[
 \delta=\frac{10^{123}(6+\log\Lambda_*)\,3000k^3\ell^2}{y_R}
 \le10^{130}\ell^3/k^2
 \tag{46.10}
\]
로 쓴다. tensor error는 <=2delta, I(F1)<=2I(F)이므로 coupled relative error는
\[
 \varepsilon_{\rm can,rel}\le4\delta.
 \tag{46.11}
\]
2^k 또는 2^(-k)를 생성·평가·흡수할 필요가 없다. 기존 coefficient envelope
lambda_max<=e(y_R/k)^k도 같은 delta<1 gate에서 유효하다.

strict sharp constant C_strict=C_Sigma+2<10^123를 유지한다.
s=xi v=v/30>=3y_R/10에서
\[
 \delta_s\le\frac{10^{123}(6+\log\Lambda_*)}{s}
 \le\frac{10\cdot10^{123}(6+\log\Lambda_*)}{3y_R}
 \le10^{127}\ell/k^5.
 \tag{46.12}
\]
그러므로 denominator는 \(\widetilde\lambda_1\ge(1-\delta_s)s>0\)이며,
두 번째 sharp factor는 main의 1+delta_s 이하이다.

모든 k>=10^200에서 log k<=k^(1/8)이다.
k=10^200에서는 200log10<500<10^25이고 log k/k^(1/8)는 log k>8에서 감소한다.
따라서 (46.10)--(46.12)는
\[
 4\delta\le1/100,\quad \delta_s\le1/100
 \tag{46.13}
\]
을 준다. 예를 들어 400*10^130<k 및 100*10^127<k만으로 충분한 여유가 있다.
이는 유한 corner 관찰을 모든 k로 일반화한 것이 아니라 단조식·부등식으로 증명한 것이다.

## 5. distribution child의 growing-k 합성

실제 연속 정수 I에서 \(E_q\le1\), pair multiplicity \(\le\tau_{3(k+1)}(q)\)는 theory 30 그대로다.
V=prod_(p<=2k^2)p, W0=V Delta이며 log V<4k^2이다.
\[
 \log q<4k^2+13v/45<v/3
\]
는 v>=k^5>=90k^2에서 성립한다.

Theory 30 (30.23)--(30.24)를 local v에 적용하면
\[
 \log\rho_{94}\le C(k,2,1/3)+4(k+1)\log v-(29/45)v.
 \tag{46.14}
\]
기존 constant를 버리지 않고 다음처럼 약화한다.
A0+B0<=5k^2, log(1+log(A0+B0))<=ell,
log(1+4k^2+13/45)<=3ell, loglog k-log k<0,
log8+2-log(1/30)+2log6<14에서
\[
 C(k,2,1/3)\le8k^2+6k+(9k+11)\ell+14\le18k^2.
\]
마지막은 ell<=k 및 k^2-17k-14>=0에서 따른다.
또 v<=2L<4k^5, log v<6ell이므로
\[
 C+4(k+1)\log v\le42k^2+24k\le43k^2.
\]
\(90\cdot43\le13k^3\)에서
\[
 \boxed{\log\rho_{94}\le-v/2\le-L/2,\quad\rho_{94}<1/100.}
 \tag{46.15}
\]
e^(-L/2)를 실제 부동소수로 만들 필요가 없다.
이 부분은 소수 분포 가정이 아닌 **정수 discrepancy**이고, 기존 P92의 Hypothesis 1(2)를
새로 호출하지 않는다. 모든 로그 변환에서 v와 L을 구분했다.

## 6. multiplier 1의 exact 유리수 마감

source (9.49)--(9.70)의 finite 합성은 theory 31 (31.16)--(31.17)에서
2^k epsilon을 (46.11)로 바꾼 식이다.
\[
 C_{94}\le
 \frac{1+\delta_s}{(1-\delta_s)^2}
 e^{2+6/k}(1+4\delta)\frac{y_R}{v}+\rho_{94}.
 \tag{46.16}
\]
Euler prefactor e^(2+6/k)는 pre-y의 제곱 e^(4/k)까지 포함하므로 중복 곱하지 않는다.
마지막 residue factor는 1 이하이며 distribution은 곱셈이 아닌 가산항이다.

k>=200에서 e<11/4 및 exp(t)<=1/(1-t), 0<=t<1로
\[
 e^{2+6/k}<(11/4)^2/(1-6/k)\le(11/4)^2/(1-6/200)<8.
\]
따라서
\[
 \boxed{C_{94}<
 \frac{8\cdot101^2}{9\cdot99^2}+\frac1{100}
 =\frac{8249009}{8820900}<1.}
 \tag{46.17}
\]
여기에는 float comparison이나 directed-rounding 주장이 없다.
마지막은 exact integer arithmetic이다. 이전 13보다 작지만 새 regime의 강한 조건 아래의
값이므로 서로 다른 cutoff의 성과를 무조건 비교하지 않는다.

## 7. Delta/phi와 원래 off-tuple prime 합

\(h\ne h_i\)여서 Delta>=p^k>exp(kL).
또 \(|h_i-h|\le2C_hu\)이므로
\[
 kL<\log\Delta\le k(u+\log2+\log C_h+\log u)<2kL.
 \tag{46.18}
\]
Theory 30에서 사용한 Rosser--Schoenfeld Theorem 15의 explicit bound와
e^gamma<3, loglogDelta>1을 적용하면
\[
 \frac{\Delta}{\varphi(\Delta)}
 \le3\log\log\Delta+2.50637
 \le3\log(2kL)+3<24\ell.
 \tag{46.19}
\]
N<=Y, xi^-1=30 및 (46.5)--(46.9)는
\[
 \sum_{q\in\mathbb P\cap(X,Y]}w(p,q-hp)
 \le\frac{720\ell}{y_R}\mathcal M_pY.
 \tag{46.20}
\]
마지막으로 log_2 X=log u<6ell, y_R>=k^5/30에서
\[
 (720\ell/y_R)(\log_2X)^{10}
 \le21600\cdot6^{10}\ell^{11}/k^5<1.
\]
실제로 21600*6^10<10^13, ell<=k^(1/8), k^3>10^13이면 충분하다.
이는 (46.6)을 준다. 여기까지는 각 p의 실제 singular series를 그대로 보존했다.
공통 series·tau·u 치환과 p-average/PNT는 H1b-NORM에서 합성한다.

## 8. 검산 계약·비목표·다음 단계

새 helper는 k, exact L-bin, exact log(C_h)만 받고 O(1)-dimension scalar를 계산한다.
거대한 X,Y,T0,V,W,Delta나 k개 form을 생성하지 않는다. structural primes/admissibility/
weight construction 조건은 문서 가정이며 숫자 scalar만으로 탐지했다고 주장하지 않는다.

toy 시험은 서로 다른 방식으로 다음을 검산한다.

- 실제 q→t 정수 이동, lower endpoint, 원래 support 제거의 부등식 방향
- shifted form의 Delta와 W-filter 보존; h=hi의 거부
- arbitrary toy Selberg coefficients와 rough indicator의 상계
- local Euler 두 경우, signed matrix의 absolute-row/square 상계
- exact 유리수 multiplier, 전체 k를 위한 polynomial witnesses
- 작은 parameter/잘못된 L bin/float/누락 filter/과도한 log(C_h) 거부
- 최소·상단 bin 및 후속 k에서 scalar envelope, 정밀도 복원, source/proof hash
- root/common-normalization 비승격

정확도나 검사 범위를 줄이는 성능 최적화가 아니다. 너무 거친 2^k 비교를 증명된 uniform
비교로 대체했으며, 단위시험은 전 범위 문서 증명의 보조 수단이다.

다음 권장 단계는 H1b-NORM이다. 그 뒤 actual dependency를 가지치기하고 남은
PAP/UB, hypergraph probability, arbitrary-X gate를 확인한다.
X_cert calculator는 모든 필수 root 입력이 닫힌 뒤에만 작성한다.
별도 사용자 수행절차 필요없음. 실제 데이터·장시간 연산·새 설치는 수행하지 않았다.
