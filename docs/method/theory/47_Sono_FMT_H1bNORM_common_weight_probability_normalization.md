# Sono/FMT H1b-NORM: 공통 가중치·moment·고정-X 확률 정규화

- 작성: 2026-09-09 KST
- 수준: PROJECT FINITE ANALYTIC PROOF; 독립 심사·Lean 인증 아님
- 범위: 명시적 Maynard W-filter construction, 실제 growing dimension
- 상태: FILTERED COMMON MOMENTS AND FIXED-X PROBABILITY INPUTS EXPLICIT
- 계약: data/Sono_FMT_H1bNORM_common_normalization_v1.json
- 검산: source/h1bnorm_common_normalization.py
- 검토: ../../review/53_20260909_H1bNORM_common_normalization_타당성검토.md

## 1. 목적·전제와 source 적용성

P91은 모든 정수의 점수 합, P92는 지정한 소수 위치의 점수 합, P94는 다른 위치의
점수 합 상계다. 세 결과를 서로 다른 점수 정의로 계산해 놓고 그대로 합치면 안 된다.
이 문서는 정확한 공통 계수와 제곱비를 먼저 증명하고, 합을 확률로 나누는 오차까지 닫는다.

선행증명에서 재사용한 부분과 직접 보완한 부분은 다음과 같다.

| 원천·정확한 위치 | 재사용 | 이번 보완 |
|---|---|---|
| FGKMT, DOI [10.1090/jams/876](https://doi.org/10.1090/jams/876), arXiv:1412.5029, pp.97--102, (7.4), (8.1)--(8.4) | singular series, coefficient support, 공통 tau/u 구조 | O(k/X)를 정확한 한 소수 보정비로 대체 |
| FMT, [arXiv:1511.04468](https://arxiv.org/abs/1511.04468), pp.11--16, Theorem 6, (6.9)--(6.11), p.12 각주 2 | 확률 정규화, B0 한 소수 삭제 | 수치 오차와 삭제 비용, 고정-X 양화 |
| Rosser--Schoenfeld (1962), DOI [10.1215/ijm/1255631807](https://doi.org/10.1215/ijm/1255631807), p.69 Theorem 1, (3.1)--(3.2) | explicit pi 양측식 | dyadic count 상대오차 3/log X |
| Sono, 출판 p.542, FGKMT (8.3) 인용과 C 정의 | phi(B)/B in [1/2,1], 실제 u, C=uX/(2 sigma Y) | B와 X 의존성을 생략하지 않음 |
| [theory 44](44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md), §§4,9--10 | P92, uniform I/J, open interval atom | P92 주항을 공통 series로 변경 |
| [theory 45](45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md), §§2,8 | W-filter, P91, shift | 모든 p에 공통인 질량 기준 |
| [theory 46](46_Sono_FMT_H1bP94g_growing_dimension_rough_moment.md), §§3,7 | 실제 T0와 off-tuple 상계 | p 평균 및 확률 denominator |

표적 문헌 조사에서 이 profile·끝점·growing k·숫자 오차를 모두 제공하는 drop-in
정리를 확인하지 못했다. 세계적 부재나 novelty를 주장하지 않는다. 기존 PDF만 사용하며
새 source 다운로드, 큰 소수 계산, threshold calculator는 수행하지 않는다.

## 2. 공통 변수·construction과 최종 결과

모든 로그는 자연로그다. 다변수 sieve profile F는 empirical F(x)가 아니다.
\[
 a=\log X,\quad L=\log(X/2),\quad
 k=\lfloor L^{1/5}\rfloor\ge10^{200},\quad \ell=\log k,\quad
 y_R=\log R=(a-\log4)/9,
\]
\[
 Y=\frac{Xa\log\log a}{153600\log5\,\log a},\quad
 P=\mathbb P\cap(X/2,X],\quad Q=\mathbb P\cap(X,Y].
 \tag{47.1}
\]
같은 source-selected B는 1 또는 소수이며 \(b=\varphi(B)/B\in[1/2,1]\)로 둔다.
즉 기존 H1c identity Hypothesis와 같은 B를 사용한다. 임의 B에 대해 Hypothesis를 새로
증명했다는 뜻이 아니다. 별도의 정수 B0는 P,Q에서 각각 최대 한 소수를 제거하는 FMT
parameter이며 B와 동일하다고 가정하지 않는다. \(P'=P\setminus\{B_0\}\),
\(Q'=Q\setminus\{B_0\}\).

\(\mathcal H=(h_1,\ldots,h_k)\)는 서로 다른 admissible 정수로 \(1\le h_i\le2k^2\).
W, F, lambda, divisibility support는 theories 44--46의 같은 construction을 사용한다.
\[
 w(p,n)=1_{|n|\le Y}\,
 1_{(W,\prod_j(n+h_jp))=1}
 \left(\sum_{d_j\mid n+h_jp}\lambda_{\mathbf d}(\mathcal L_p)\right)^2,
 \quad \mathcal L_p=\{n+h_jp\}_j .
 \tag{47.2}
\]
filter는 coefficient support에서 자동 생기지 않는다. literal unfiltered FGKMT 표시식의
동일성을 주장하지 않는다. 이 보완 construction 자체로 필요한 부등식을 증명한다.

\(\nu(s)=\#\{h_j\bmod s\}\)로 두고 다음 공통 series를 정의한다.
\[
 S=\prod_{s\nmid B}(1-\nu(s)/s)(1-1/s)^{-k},\quad
 M_0=b^{-k}S y_R^k I(F),\quad
 \boxed{\tau=2M_0a^k,\qquad
 u_X=b\,\frac{y_R}{a}\frac{kJ(F)}{2I(F)}} .
 \tag{47.3}
\]
소수 곱은 s에 대한 것이다. \(a^k\)는 tau에 **곱한다**. 다음 finite bounds를 얻는다.
\[
\begin{array}{ll}
 Z_p:=\sum_nw(p,n),&
 |Z_p-2YM_0|\le(4/k)\,2YM_0,\\
 K:=M_0u_XX/k,&
 |\sum_{p\in P'}w(p,q-h_ip)-K|\le(2/\sqrt k)K
       \quad(q\in Q',1\le i\le k),\\
 E:=(\log a)^{-10},&
 \sum_{q\in Q'}\sum_{p\in P'}w(p,q-hp)
 \le 2M_0XYE/a .
\end{array}
\tag{47.4}
\]
마지막 줄은 정수 \(h\notin\mathcal H,\ |h|\le C_hY/X,\ C_h\ge1,\ \log C_h\le L/4\)인
theory 46의 명시적 off-tuple h 범위에서만 성립한다.
충분한 child cutoff는 \(X\ge2\exp(\max(10^{1000},4\log C_h))\)다.
이는 전체 \(X_{\rm cert}\), 최적 threshold 또는 실제 소수 전수검사 범위가 아니다.

## 3. 큰 차원에서 쓸 초등 여유

\(k\ge10^{200}\)에서 \(\ell\le k^{1/32}\)이다. 첫 endpoint에서
\(200\log10<500<10^6<10^{200/32}\)이고 \((\log t)/t^{1/32}\)가
\(\log t>32\)에서 감소하기 때문이다. 특히 \(\ell\le k^{1/16},\ell\le k\).
이와 \(k^5\le L<(k+1)^5\)에서
\[
 a<(k+2)^5,\quad \log a<6\ell,\quad
 y_R\ge k^5/30,\quad a/30\le y_R\le L/9,\quad y_R/a\ge1/10.
 \tag{47.5}
\]
theory 45의 \(Y/X\ge\sqrt a/307200\)를 강화하면
\[
 Y\ge2k^2X,\qquad
 0\le\epsilon:=4k/X\le1/k,\qquad 3/a\le1/k.
 \tag{47.6}
\]
첫 식에는 \(\sqrt k\ge614400\), 두 번째에는
\(\log2+2\ell\le L\)만 있으면 된다. 나머지도 \(L\ge k^5\)로 충분하다.
따라서 \(q-h_ip\in[-Y,Y]\)가 모든 \(p\in P,q\in Q\)에서 성립한다.
이 support 등호는 지정한 hi에만 쓰며 임의 h에는 쓰지 않는다.

\(\eta_k=10^{134}\ell^4/k^2\)에 대해
\[
 \eta_k\le1/k
 \tag{47.7}
\]
이다. \(\ell^4\le k^{1/4}\)와 \(10^{536}\le k^3\)로 충분하다.
뒤에서 쓰는 \(\sqrt k\ge10,\ k^3\ge14400,\ k^3\ge60\cdot243\),
\(72+864k^2\le k^5,\ 4(6+2k)\le3k^5\)도 모두 이 regime에서 성립한다.
이 다항식 비교와 단조식이 전 범위 근거이며, 몇 개 k의 수치 PASS가 그 근거가 아니다.

## 4. 정확한 series·lambda·weight 제곱비

p 이외의 s에서 \(\omega_{\mathcal L_p}(s)=\nu(s)\); s=p에서는 root가 1개다.
p>2k²이므로 \(\nu(p)=k\). 따라서 정확히
\[
 S_B(\mathcal L_p)=\alpha_pS,\quad
 S_{WB}(\mathcal L_p)=\alpha_pS_{WB},\qquad
 \alpha_p=\begin{cases}1&p\mid B,\\(p-1)/(p-k)&p\nmid B.\end{cases}
 \tag{47.8}
\]
identity slot i를 가진 \(\widetilde{\mathcal L}_{q,i}\)는
\(\widetilde L_i(n)=n,\ \widetilde L_j(n)=q+(h_j-h_i)n\ (j\ne i)\).
s!=q에서 root는 0과, 서로 다른 비영 \((h_j-h_i)\bmod s\)에 대응하는
\(-q/(h_j-h_i)\)다. 따라서 root count는 역시 \(\nu(s)\)다.
s=q에서는 q>2k²라 slope가 모두 비영이고 root가 0 하나다.
\[
 S_B(\widetilde{\mathcal L}_{q,i})=\beta_qS,\qquad
 S_{WB}(\widetilde{\mathcal L}_{q,i})=\beta_qS_{WB},\qquad
 \beta_q=\begin{cases}1&q\mid B,\\(q-1)/(q-k)&q\nmid B.\end{cases}
 \tag{47.9}
\]
이는 수렴한 무한곱에서 단 하나의 factor만 바뀌는 항등식이다.
q>2k²>=|h_j-h_i|이므로 각 tilde form은 primitive이며 위 root count로 admissible이다.
q<=Y<Xa< X²/4=T² 및 |h_j-h_i|<=2k²<T²에서 theory 44의 coefficient
조건도 만족한다. 같은 source B의 selected identity Hypothesis만 필요하고,
다른 affine-selected prime 분포 정리를 암묵적으로 추가하지 않는다.
\[
 1\le\alpha_p,\beta_q\le1+\epsilon .
 \tag{47.10}
\]
p-k>=X/4, q>=X, X>=4k와 (47.6)으로 충분하다.

p,q>R이므로 support product<=R 안에는 이 예외 소수가 없다.
W 밖의 s>2k²에서는 k개 slot 모두 허용되고 denominator s-omega=s-k다.
따라서 세 family의 truncated D_k, denominator, F 입력은 정확히 같다.
FGKMT p.98의 y_r와 lambda 정의에서
\[
 \lambda_{\mathbf d}(\mathcal L_p)=\alpha_p\lambda^0_{\mathbf d},\qquad
 \lambda_{\mathbf d}(\widetilde{\mathcal L}_{q,i})=\beta_q\lambda^0_{\mathbf d}.
 \tag{47.11}
\]
이는 모든 coefficient에 같은 scalar이므로 부호 취소가 있어도 성립한다.
prime slice에서는 d_i|q 또는 d_i|p, d_i<=R이므로 양쪽 d_i=1.
나머지 form 값과 W-filter가 정확히 같고 (47.6)으로 support도 유지된다. 그러므로
\[
 \boxed{w(p,q-h_ip)=(\alpha_p/\beta_q)^2
 w^*_{\widetilde{\mathcal L}_{q,i}}(p).}
 \tag{47.12}
\]
제곱을 빼거나 alpha_p가 p에 의존하는데 합 밖으로 꺼내지 않는다.

## 5. 명시적 dyadic prime count

Rosser--Schoenfeld Theorem 1은 t>=59에서
\(\pi(t)>t(\log t)^{-1}(1+(2\log t)^{-1})\),
t>1에서 \(\pi(t)<t(\log t)^{-1}(1+3/(2\log t))\)다.
기존 추출 텍스트의 분수·부호가 흐트러져 p.69 원문으로 확인했다.
\(a=\log X\ge10,\ L=a-\log2,\ P_o=\pi(X)-\pi(X/2),\ P_0=X/(2a)\)라 하면
\[
 2+1/a-a/L-3a/(2L^2)<P_o/P_0
 <2+3/a-a/L .
\]
왼쪽은 \(1-[1/(a-1)+3a/(2(a-1)^2)]\) 이상이며 대괄호는
\((10/9+50/27)/a=80/(27a)<3/a\) 이하다.
오른쪽은 a/L>=1에서 \(1+3/a\) 이하다. 따라서
\[
 \boxed{|P_o/P_0-1|\le3/a.}
 \tag{47.13}
\]
P_o는 정확히 열린 왼쪽 끝 (X/2,X]의 count다. 아직 B0는 빼지 않았다.

## 6. tau/u의 크기와 모든 정수의 pointwise bound

H1a의 \(J/I>\ell/(4k)\)와 (47.5), b>=1/2에서
\[
 \boxed{\frac{\ell}{144}(1-\log4/a)<u_X,\qquad
 \ell/160<u_X<\ell.}
 \tag{47.14}
\]
첫 하계가 Sono 계수 전달에 쓰는 더 정확한 식이며, 1/160만으로 대체하지 않는다.
상계 증명: theory 44의 n(t)에 대해 A=integral n²>=1/(2kell),
D=integral n<=log(1+sqrt(k)ell)/(kell)<=1/k.
1+sqrt(k)ell<=k는 (47.5)보다도 훨씬 약한 조건이다.
\(J(F)\le A^{k-1}D^2,\ I(F)\ge A^k/2\)에서 \(J/I\le4\ell/k\).
따라서 \(u_X\le2\ell/9<\ell\).

공통 S도 admissible H 자체의 series이므로 기존 \(S>e^{-9k/2}\)가 적용된다.
\(I(F)\ge(2k\ell)^{-k}\)와 \(k^3/60>243>e^{9/2}\)에서
\[
 M_0\ge[e^{-9/2}y_R/(2k\ell)]^k\ge1,\qquad\tau\ge2.
 \tag{47.15}
\]
거대한 k승을 실제 계산한 것이 아니다. 양의 밑이 1 이상임을 증명한 것이다.

기존 \(|\lambda_{\mathbf d}|\le e(y_R/k)^k\)와
\(\sum_{d\le R}\tau_k(d)\le R(1+\log R)^k\)로, form 값이 0인 경우까지 포함해
\[
 w(p,n)\le e^2(y_R/k)^{2k}R^2(1+y_R)^{2k}.
\]
\(\log y_R,\log(1+y_R)<6\ell\)에서
\[
 \log w(p,n)\le2L/9+2+24k\ell\le L/4<a/4 .
 \tag{47.16}
\]
w=0이면 로그식 대신 원래 상계를 쓴다. (47.3) 변수 하에서 결론은
\(\boxed{w(p,n)\le X^{1/4}}\)이다.

## 7. 세 moment의 공통 오차와 B0 삭제

P91의 M_p=alpha_p M0를 (45.3)에 넣으면
\[
 |Z_p/(2YM_0)-1|\le2\eta_k(1+\epsilon)+\epsilon\le4/k.
 \tag{47.17}
\]
P92의 \(\mathcal M(P_o)=\beta_q K(P_o/P_0)\), 여기
\(K=bM_0y_R(J/I)P_0=M_0u_XX/k\)다.
closed integer count \(N\le X\)와 (47.14)의 적분비 하한에서
\[
 \mathcal A/(\beta_qK)
 =\frac{N}{bP_0y_R^2(J/I)}
 \le\frac{16ak}{y_R^2\ell}
 \le\frac{14400k}{L\ell}\le1/k.
 \tag{47.18}
\]
t=k^(-1/2), v=3/a라 쓰면 (44.5), (47.13)의 합 V에 대해
\[
 |V/(\beta_qK)-1|
 \le L^{-1/10}(1+v)+v+1/k
 \le t+3/k=:D_0<1 .
 \tag{47.19}
\]
각 summand가 비음수이므로 (47.12)를 합 안에서 상·하계하면
\[
 \frac{1-D_0}{1+\epsilon}\le
 \frac{\sum_{p\in P}w(p,q-h_ip)}K
 \le(1+\epsilon)^2(1+D_0).
 \tag{47.20}
\]
즉 상대오차는 \(D_0+6/k\le t+9/k\).
B0가 P에 속하는 소수일 때만 항 하나가 사라진다.
\[
 \frac{w(B_0,q-h_iB_0)}K
 \le160kX^{-3/4}\le1/k.
 \tag{47.21}
\]
M0>=1, u_X>=ell/160>=1/160를 썼다.
마지막은 \(\log160+2\ell\le3a/4\)이며
\(4(6+2k)\le3k^5\)에서 충분하다. 따라서 삭제 후 오차는
t+10/k<=2t이다. Q에서의 삭제는 남은 q에 관한 이 결론을 바꾸지 않는다.

P94는 theory 46에서 각 p의 상계가 alpha_p M0 Y E다. 따라서 (47.13)에서
\[
 \sum_{q\in Q'}\sum_{p\in P'} w(p,q-hp)
 \le P_0(1+3/a)(1+\epsilon)M_0YE
 \le 2M_0XYE/a .
 \tag{47.22}
\]
마지막 비율은 \((1+3/a)(1+\epsilon)/4<1\).
삭제는 비음수 합을 감소시키므로 equality가 아닌 upper bound로 처리한다.

## 8. 고정-X 확률 입력과 양화의 정확한 한계

각 p에 대해 \(\Pr(\widetilde n_p=n)=w(p,n)/Z_p\).
\(Z_p\ge YM_0>0\)이고 n의 support는 유한하므로 실제 확률분포가 존재한다.
서로 다른 p의 독립성은 이 세 식에 필요하지 않으며, 필요하면 유한 product로 선택 가능하다.
\[
 \left|\frac{\sum_{p\in P'}\Pr(q=\widetilde n_p+h_ip)}
 {u_XX/(2kY)}-1\right|
 \le\frac{4/k+2/\sqrt k}{1-4/k}
 \le3/\sqrt k<E .
 \tag{47.23}
\]
첫 분모의 참조값은 P92의 K를 P91의 2YM0로 나눈 것이다.
두 번째 inequality는 t<=1/10에서 \(4t+12t^2\le1\).
마지막은 \(\log a<6\ell,\ell\le k^{1/32}\)와
\[
 (3\cdot6^{10})^{16}<k^3
\]
에서 따른다. 따라서 FMT (6.9) 오차의 multiplier 1을 쓸 수 있다.
마찬가지로 더 강한 (47.22)의 첫 상계와 Zp 하계를 사용하면
\[
 \sum_{q\in Q'}\sum_{p\in P'}\Pr(q=\widetilde n_p+hp)\le XE/a,
 \qquad \Pr(\widetilde n_p=n)\le X^{-3/4}.
 \tag{47.24}
\]
첫 inequality의 충분조건은
\((1+1/k)^2/[4(1-4/k)]<1\). 이는 k>=16에서 성립한다.
두 번째는 (47.16), Zp>=YM0>=X에서 따른다.
FMT (6.10)--(6.11)의 **입력 역할**을 명시적인 수치식으로 대체한다.

### 8.1 u=u(k)라는 문구를 그대로 인증하지 않는다

FGKMT Theorem 5와 FMT Theorem 6의 선언은 u가 차원에만 의존한다고 적지만,
FGKMT (8.3) 및 Sono p.542의 실제 정의에는 b와 y_R/a가 들어 있다.
B를 1로 바꾸거나 phi(B)/B=1이라고 놓을 근거는 없다.
이 문서가 인증한 양화는 다음과 같다.

각 허용 X와 그 source-selected B에 대해, 같은 k·profile로 하나의 결정론적
u_X를 고른다. u_X는 p,q,i,n 및 뒤의 무작위 residue 선택과 무관하고
(47.14)의 상·하한은 모든 허용 X에 균일하다.

(47.23)--(47.24)는 바로 이 양화에서 직접 증명했다. FMT §6의
(6.21)--(6.23)에서 u는 고정-X first/second moment의 기준 scalar이며
서로 다른 X의 u가 같음을 사용하지 않는다. 그러나 그 후속 moment의 수치 failure rate를
이번에 닫은 것은 아니다. 최종 C=u_X X/(2 sigma Y) 역시 같은 X의 값이다.
따라서 fixed-X 확률 입력은 사용 가능하지만, 출판된 theorem 문장의 모든 양화나
임의 k 범위를 그대로 복제했다고 하지 않는다. 공식 erratum 주장도 하지 않는다.

## 9. 검산·비목표·다음 proof gate

검산 helper는 exact k,L bin, log(C_h)와 명시 filter 조건을 검사하고 O(1)개의
로그 스칼라만 평가한다. X,Y,W,S,I,J나 k개 배열은 만들지 않는다.
bounded toy에서는 root residue 전수, 독립 coefficient 합, 제곱비·확률 ratio·B0 삭제를
exact Fraction으로 검사한다. 수치 스칼라 결과는 interval arithmetic/Lean proof가 아니다.

필수 structural 가정(admissibility, source B, 같은 F와 support)은 문서의 조건이며
숫자 k만 입력한 helper가 그것까지 검증했다고 하지 않는다.
이번 explicit 범위는 공통 filtered moment와 fixed-X 확률 입력이다.
general Maynard P6.1/P95, literal unfiltered 식, u의 only-k 의존성,
hypergraph probability, PAP/UB, arbitrary-X coverage, 전체 X_cert는 자동 승격하지 않는다.

다음 H1b-DEP에서 actual call map을 확정하여 P95의 필수 여부를 결정하고,
SIV-07/08/09의 broad node와 이번 닫힌 actual child를 분리한다.
그 뒤 FMT Lemma 6.1--6.4와 Sono hypergraph/UB/PAP의 미지 numerical rate를 감사한다.
사용자 새 설치·자료·장시간 실행은 현재 불필요하다. 별도 수행절차 필요없음.

### 이번 로컬 검증 결과

- 전용 17/17 PASS, 0.098초.
- 8개 module 표적 93/93 PASS, 0.292초. 첫 회귀의 schema 기대값 갱신 누락 1건은
  교정 후 재실행했으며 수학 gate 완화는 없다.
- 전체 483/483 PASS, 59.932초, exit 0.
- helper·전용/parent 시험 5파일 py_compile PASS, 원문/선행 proof·code 10 hash 일치.
- actual prime/data 실험, 새 PDF 다운로드, 설치, 그래프, root calculator는 미실행.
