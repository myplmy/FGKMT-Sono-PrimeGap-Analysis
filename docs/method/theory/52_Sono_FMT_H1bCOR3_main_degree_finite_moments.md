# Sono/FMT H1b-COR3: R06 main-degree moment·충돌·bad-P 제거

- 작성: 2026-09-09 KST
- 증거: PROJECT FINITE ANALYTIC PROOF + bounded exact toy; 독립 심사·Lean 인증 아님
- 상태: DEP-R06 actual child explicit, R01–R06 closed overlay; R07–R12 OPEN
- 계약: [COR3 successor](data/Sono_FMT_H1bCOR3_local_main_moments_v1.json)
- 입력: [theory 51 R03](51_Sono_FMT_H1bCOR3_finite_local_count_partition.md)

## 1. 기존 증명에서 가져온 것과 보완한 것

[FMT, arXiv:1511.04468](https://arxiv.org/abs/1511.04468) pp.14–16,
Lemma 6.4 (6.21)–(6.23)은 좋은 p로 제한하는 비용과 main의 두 moment를 다룬다.
[FGKMT, DOI 10.1090/jams/876](https://doi.org/10.1090/jams/876),
출판 p.92/PDF p.28 Lemma 6.2는 대응 moment 구조를 준다.
FMT p.10 Theorem 5 (5.8)의 목표는 absolute error multiplier 1이다.
source의 proof 구조를 먼저 확인한 뒤 아래 finite 상수·실패율을 직접 연결한다.
새 source 다운로드 또는 소수 실험은 없다.

중요한 두 사항은 다음과 같다.

1. 서로 다른 p의 tuple 두 개도 공통 q를 공유하므로 독립인 2k점이 아니다.
2. 같은 p의 모든 i1,i2 항을 diagonal 비용으로 남긴다. i1=i2만 남겨서는 안 된다.

## 2. 같은 고정-X law와 기준 C

theories 47,49,50,51의 a=ln X, b=ln a, c=c_aux, k, Y, P', Q', sigma,
같은 source B와 W-filtered preliminary law mu_p를 사용한다.
충분조건은 변함없이 X>=2exp(10^1000), k>=10^200이다.
현재 X는 **보조 변수**이며 최종 X_cert가 아니다.
\[
\zeta_p(\mathbf A;n)=\mu_p(n)1_{\{n+h_jp\in\mathscr S(\mathbf A)\ \forall j\}},
\quad D_p=\sum_n\zeta_p,\quad U_p=D_p/\sigma^k.
\]
good p는 |U_p-1|<=a^-3이고 조건부 law는 zeta_p/D_p다.
\[
K_0=u_X X/(2Y),\quad A_q=\sum_{i,p\in P'}\mu_p(q-h_ip),\quad
C=K_0/\sigma,\quad t_q=A_q/K_0.
\tag{52.1}
\]
NORM47 (47.23)의 각 i 식을 합하면
\[
|t_q-1|\le r:=3/\sqrt k<b^{-10},\quad
\mu_p(n)\le X^{-3/4},\quad \sigma^{-2k}\le X^{1/50}.
\tag{52.2}
\]
이 실제 입력의 q-uniformity는 새로운 가정이 아니라 기존 child의 결론이다.

theory 47의 ell/160<u_X<ell, b<6ell, ell<=b/5와
theory 35 및 (51.14)에서
\[
\boxed{\tfrac12<C<400.}
\tag{52.3}
\]
하계는 C>1/(159744c)=(25/26)ln5>1/2,
상계는 sigma Y>(24/25)80cXb에서 C<1/(768c)=200ln5<400이다.
최종 계수 보존에는 이 느슨한 하계가 아니라 theory 34의
(5ell/b)(1-ln4/a)>39/40와 theory 47의
u_X>(ell/144)(1-ln4/a)를 함께 쓴다. 정확히
\[
\boxed{C>
\frac{39/40}{144\cdot5\cdot2\cdot(26/25)\cdot80c}
=\frac54\ln5.}
\tag{52.4}
\]
이는 기존 Sono 계수를 바꾸지 않고 같은 C를 유지함을 보여 주는 한 단계다.
최종 모든 오차의 합성 R11을 완료했다는 뜻은 아니다.

## 3. 첫 moment와 cross-p 충돌

\[
S_q=\sum_{i,p}\zeta_p(\mathbf A;q-h_ip),\qquad V_q=\sigma^{-k}S_q.
\]
각 tuple에 q가 포함되므로 q가 죽으면 V_q=0이다.
서로 다른 k점에 COR1을 적용하면 epsilon=2a^-17에 대해
\[
(1-\epsilon)A_q\le\mathbb EV_q\le(1+\epsilon)A_q.
\tag{52.5}
\]
한 q에서 두 항 (p1,i1),(p2,i2)의 tuple은
q+(h_j-h_i1)p1와 q+(h_j-h_i2)p2다.
p1!=p2이면 공통 q 이외에 교점이 없다.
있다고 하면 0이 아닌 d1,d2, |d_l|<=2k²<min(p1,p2)에 대해
d1p1=d2p2이고, 소수성 때문에 p1|d2라는 모순이 생긴다.
따라서 union에는 정확히 **2k-1점**이 있다.
점의 절댓값은 2Y<X², 2k-1<=a이므로 COR1 적용 범위 안이다.

같은 p에서는 별도 비용으로
\[
D_q^{\rm diag}:=\sigma^{-2k}\sum_p
  \left(\sum_i\mu_p(q-h_ip)\right)^2
\le kX^{-73/100}A_q
\tag{52.6}
\]
를 둔다. 이 식은 생존확률을 1로 넓히고
max_p sum_i mu<=kX^-3/4를 사용한다. 모든 같은-p 충돌을 포함한다.
그러므로
\[
\mathbb EV_q^2\le(1+\epsilon)A_q^2/\sigma+D_q^{\rm diag}.
\tag{52.7}
\]
cross-p 가중치 합을 전체 A_q²로 넓혀도 비음수이므로 유효하다.

(52.1)–(52.3)에서
\[
\frac{D_q^{\rm diag}}{\sigma C^2}
\le4kX^{-73/100}\le a^{-17}.
\tag{52.8}
\]
마지막은 k<=a와 ln4+18b<=73a/100으로 충분하다.
b<=a/100, a>=1000에서 성립한다.

## 4. 평균 오차의 제곱을 보존한 concentration

V_q=0 on q dead와 Pr(q alive)=sigma를 써서
\[
\begin{split}
\mathbb E\!\left[1_{\{q\ {\rm alive}\}}(V_q/C-1)^2\right]
&=\mathbb EV_q^2/C^2-2\mathbb EV_q/C+\sigma\\
&\le\sigma[(t_q-1)^2+\epsilon(t_q^2+2t_q)+a^{-17}]\\
&\le\sigma[r^2+17a^{-17}]
\le18\sigma b^{-20}\le\sigma b^{-18}.
\end{split}
\tag{52.9}
\]
t_q<=2를 사용했다. 마지막에는 (51.3)과 b²>=18을 쓴다.
특히 평균 오차 r를 이 단계에서 불필요하게 O(r)로 넓히지 않는다.
sigma를 빼거나 q 생존 조건을 생략해서는 안 된다.

alive인데 |V_q/C-1|>b^-3인 q 개수를 N_pre라 하자.
(52.9), m_Q<=2Y/a와 SIGMA35에서
\[
\mathbb EN_{\rm pre}\le m_Q\sigma/b^{12}
\le 200cX/(ab^{11}).
\]
Markov를 한 번 더 써서
\[
\boxed{\Pr\{N_{\rm pre}>X/(4ab)\}\le800c/b^{10}.}
\tag{52.10}
\]
q별 독립성을 사용하지 않는다. 실제 확률은 항상 위 RHS와 1 중 작은 값 이하이다.

## 5. bad-P 질량 제거

COR1 (49.18)–(49.19)는 E(U_p-1)²<=7a^-17, Pr(p bad)<=7a^-11이다.
|U_p-1|>a^-3 위에서는 |U_p-1|<a³(U_p-1)²이므로
\[
\mathbb E[U_p1_{\{p\ {\rm bad}\}}]
\le7a^{-11}+7a^{-14}\le14a^{-11}.
\tag{52.11}
\]
이는 작은 bad-P **개수**만으로 질량도 작다고 추정한 것이 아니다.
같은 분모 moment로 bad-P **질량**을 직접 상계한 것이다.
\[
B_q=\sigma^{-k}\sum_i\sum_{p\ {\rm bad}}\zeta_p(\mathbf A;q-h_ip).
\]
각 i,p에서 q->q-h_ip가 단사이므로, support 내 모든 n으로 넓혀
\[
\sum_{q\in Q'}B_q\le k\sum_{p\in P'}U_p1_{\{p\ {\rm bad}\}},\qquad
\mathbb E\sum_q B_q\le14kX/a^{12}.
\tag{52.12}
\]
NORM47의 |P'|<=X/a를 썼다.
alive이고 B_q>C/b³인 q를 N_rem으로 세면
\[
\boxed{\Pr\{N_{\rm rem}>X/(4ab)\}
\le\frac{56kb^4}{Ca^{11}}\le\frac{112kb^4}{a^{11}}.}
\tag{52.13}
\]
제거 질량은 비음수다. 두 사건의 union 밖에서 모든 alive q 중 많아야
floor(X/(2ab))개를 제외하면 good-P main V_q^g=V_q-B_q가
\[
|V_q^g/C-1|\le2b^{-3}
\tag{52.14}
\]
를 만족한다. 두 개의 floor 합은 floor 합계 이하이므로 이 개수 표기도 안전하다.

## 6. 실제 조건부 분포와 unit absolute error

좋은 p의 D_p/sigma^k∈[1-d,1+d], d=a^-3이므로
조건부 main 기여 W_q^main에 대해
\[
\frac{V_q^g}{1+d}\le W_q^{\rm main}\le\frac{V_q^g}{1-d}.
\]
d<=1/(4b³), d<=1/4를 써서
\[
|W_q^{\rm main}/C-1|
\le\frac{2b^{-3}+d}{1-d}\le3b^{-3}.
\tag{52.15}
\]
bad p는 n_p=0으로 놓지만 q>p인 소수이므로 q≡n_p(mod p)에 기여하지 않는다.
각 p 안의 h가 서로 다르면 n=q-hp도 서로 달라 확률을 합해도 중복되지 않는다.

COR2 theory 50 (50.12)–(50.14)는 다른 예외 q<=X/(2ab)를 빼고
off-tuple 기여 0<=W_q^off<=2b^-3을 준다.
같은 c, law, residue vector를 사용하므로 독립성 없이 합성할 수 있다.
(52.3)과 b>2000에서 (3C+2)/b³<1202/b³<=b^-2이다. 따라서
\[
\boxed{\left|\sum_{p\in P'}\Pr(q\equiv n_p\pmod p\mid\mathbf A)-C\right|
\le b^{-2}}
\tag{52.16}
\]
가 살아남은 q 중 많아야 floor(X/(ab))개를 제외하고 성립할 실패확률은
\[
\boxed{F_{\rm degree}\le
\min\!\left(1,\frac{1600c}{b^5}+\frac{800c}{b^{10}}
                    \frac{112kb^4}{a^{11}}\right).}
\tag{52.17}
\]
이것이 같은 actual 입력에서 FMT Theorem 5 (5.8)의 numerical replacement다.
C는 q나 A에 의존하지 않는 같은 fixed-X scalar이며 (52.4)를 유지한다.

R03의 J구간 사건도 함께 원하면 (52.17)의 min 안에 3Jb^6/a^17을 더한다.
별도 good-P 개수 사건 (49.21)까지 요구하면 추가로 7/a^8을 더한다.
이를 full hypergraph와 최종 coefficient까지의 전역 예산이라고 부르지 않는다.

## 7. 상태·검산·다음 proof

| 항목 | 이번 후속 판정 |
|---|---|
| R03 | 사전 고정 유한 family·폭 조건부 actual finite count explicit |
| R06 | collision·bad-P·분모 비용 포함 actual main degree explicit |
| R01–R06 | actual PROJECT_EXPLICIT overlay |
| R07–R12 | OPEN: full hypergraph, 동시 covering, PAP, UB, 전역 예산, 최종변수 |
| broad SIV-07/08/09 | HARD_BLOCKER 유지 |
| X_cert / calculator | OPEN / NOT READY |

새 helper는 작은 residue 공간의 직접 합과 별도 product oracle로 첫·두 번째 moment를
exact Fraction 대조한다. cross-p 2k-1, 같은-p diagonal, q 생존 indicator,
bad-P 질량, 조건부 denominator를 각각 반례 방지 시험으로 다룬다.
무한범위의 수학적 근거는 §§2–6이며 toy 검산은 독립 formal certification이 아니다.
현재 거대한 child cutoff를 최적화하거나 그 지점까지 소수를 생성하지 않는다.

다음은 **H1b-COV1 / DEP-R07**, full hypergraph source의 실제 parameter·subset·failure-rate
inventory와 finite 재증명이다. R08과 R11/R12는 그것에 자동으로 따라오지 않는다.
새 source·설치·장시간 실제 계산이 필요하면 사용자에게 보고하고 해당 지점에서 멈춘다.
