# Sono/FMT H1b-COR3: R03 유한 local count와 사전 고정 partition

- 작성: 2026-09-09 KST
- 증거: PROJECT FINITE ANALYTIC PROOF; 독립 심사·Lean 인증 아님
- 상태: DEP-R03 actual child explicit; covering 이후의 동시성 R08은 별개
- 계약: [COR3 successor](data/Sono_FMT_H1bCOR3_local_main_moments_v1.json)
- 연결: [theory 52 R06](52_Sono_FMT_H1bCOR3_main_degree_finite_moments.md)

## 1. source-first 판정과 양화

[FMT, arXiv:1511.04468](https://arxiv.org/abs/1511.04468) p.10 (5.7),
p.13 Corollary 2 (6.14)는 고정된 alpha,beta에서 남는 소수 개수를 말한다.
그 proof는 [FGKMT, arXiv:1412.5029](https://arxiv.org/abs/1412.5029),
DOI [10.1090/jams/876](https://doi.org/10.1090/jams/876)의 구판 Corollary 4를
인용하며, 출판본 pp.91–92/PDF pp.27–28의 Corollary 5가 대응한다.
그 일·이차 moment proof를 재사용한다. 모든 실수 alpha,beta에 대한 무한 union을
인쇄 명제로부터 곧바로 얻을 수는 없다.

정확한 유한 prime count는 [Rosser–Schoenfeld 1962](https://doi.org/10.1215/ijm/1255631807),
인쇄 p.69 Theorem 1 (3.1)–(3.2), sigma는 p.70 Theorem 7 (3.25)–(3.26)을 쓴다.
새 정리를 찾아야 하는 부분보다, 알려진 정리의 끝점·오차·동시성 연결부가 필요한 경우다.
이 실제 construction에 필요한 모든 수치식을 그대로 주는 drop-in source는 확인하지 못했다.
문헌 전체의 부재나 novelty를 주장하지 않는다.

FMT/FGKMT는 native text를 먼저 읽고 해당 수식 원문 페이지를 대조했다.
RS는 scan-with-text-layer이므로 수식 원본을 직접 대조했다. 새 OCR·download는 없었다.

## 2. 공통 정의와 충분조건

[theory 49](49_Sono_FMT_H1bCOR1_finite_correlation_conditioning.md)와 같은
보조 sieve 변수·독립 균등 residue vector A를 사용한다.
\[
a=\ln X,\quad b=\ln a,\quad k=\lfloor(\ln(X/2))^{1/5}\rfloor,\quad
c=c_{\rm aux}=\frac1{153600\ln5},\quad Y=cXa\frac{\ln b}{b}.
\tag{51.1}
\]
여기 c는 최종 Sono 계수 2e-17이 아니며, b는 theory 47의 phi(B)/B가 아니다.
\[
X\ge2\exp(10^{1000}),\quad k\ge10^{200},\quad b>2000.
\tag{51.2}
\]
P', Q', sigma, S(A), B0는 theories 47/49와 같다. 특히 Q'=prime∩(X,Y]에서
B0를 뺀 집합이고, S는 a^20<s<=z인 prime 중 B0를 제외한다.
B0와 distribution source의 exceptional B를 동일시하지 않는다.
모든 로그는 자연로그; 이 구간은 보조 후보 소수의 위치 구간이지 canonical G의
end-bounded 정의를 start-bounded로 변경하는 것이 아니다.

다음 초등 여유를 사용한다.
\[
10^6b\le a^{1/4},\qquad b^{20}\le a,\qquad b\le a/100.
\tag{51.3}
\]
첫 두 식은 b=2000에서 e>2에 따른
2^500>10^6·2000, 2^2000>2000^20와
e^(b/4)/b, e^b/b^20의 양의 도함수로 모든 b>=2000에 성립한다.
마지막은 a=1000에서 ln1000<10 및 (ln a)/a의 감소성으로 충분하다.
이는 전 범위의 증명이며 몇 개 수치 표본의 외삽이 아니다.

## 3. 무작위 선택 전의 실제 local prime count

0<=alpha<beta<=1, delta=beta-alpha라 하자.
먼저 disjoint partition에 맞는 I=(alpha Y,beta Y]를 사용한다.
\[
m_I=\#(Q'\cap I).
\]
RS Theorem 1과 X<=t<=Y<Xa에서
\[
\left|\pi(t)-\frac t a\right|\le\frac{2bY}{a^2}.
\tag{51.4}
\]
실제로 ln t∈[a,a+b]이고 pi(t)>t/ln t>=t/(a+b),
pi(t)<(t/ln t)(1+3/(2ln t))<=t/a+3t/(2a²)이다.
Y 이하에서만 이 식을 쓰며, alpha Y<X이면 아래 끝을 X로 clip한다.
그 길이 변경은 X 이하이다. B0 제거와 closed lower atom까지 합쳐 비용 2로 두면
\[
\left|m_I-\frac{\delta Y}{a}\right|
\le \frac{4bY}{a^2}+\frac Xa+2
\le \frac{10^6bY}{a^2}.
\tag{51.5}
\]
beta Y<=X이면 m_I=0이고 delta Y<=X이므로 같은 식이 성립한다.
마지막 비교는 aX/(bY)=1/(c ln b)<307200과
2<=bY/a², 4+307200+1<10^6에서 따른다.
1<ln5<2, ln b>1을 썼다. 2<=bY/a²는 Y>=X=e^a,
e^a>2a²로 충분하다. closed I=[alpha Y,beta Y]에도 (51.5)가 적용된다.

이제
\[
\boxed{\delta\ge a^{-1/4}}
\tag{51.6}
\]
를 요구한다. (51.3),(51.5)에서
\[
\left|\frac{m_I}{\delta Y/a}-1\right|\le a^{-1/2}\le b^{-10},\qquad
m_I\ge\frac{\delta Y}{2a}.
\tag{51.7}
\]
고정된 양의 delta는 충분히 큰 X에서 이 조건을 만족하지만, 현재의 한 X에서
임의로 좁은 모든 구간을 포함한다고 말하지 않는다.
일반 사전 고정 family에는 a>=delta_min^(-4)를 추가한다.

## 4. 생존 count의 평균·분산과 finite union

\[
N_I(\mathbf A)=\#(Q'\cap I\cap\mathscr S(\mathbf A)),\qquad M_I=\sigma m_I.
\]
한 점의 생존확률은 **정확히 sigma**다. 서로 다른 점들의 독립성은 가정하지 않는다.
theory 49 (49.5)의 두 점 상관오차 epsilon=2a^-17로
\[
\mathbb E N_I=M_I,\qquad
\operatorname{Var}N_I\le M_I+\epsilon M_I^2.
\tag{51.8}
\]
증명은 N²의 diagonal m개에 sigma, ordered distinct pairs에
(1+epsilon)sigma²를 넣고 M²을 빼면 된다.
sigma>1/a, Y>=X와 (51.6)에서
\[
M_I\ge\frac{X}{2a^{9/4}}\ge a^{17}.
\tag{51.9}
\]
마지막에는 ln2+(77/4)b<=a만 필요하며 (51.3), a>=1000으로 충분하다.

제곱에 Markov를 적용하면
\[
\Pr\{|N_I-M_I|>b^{-3}M_I\}\le\frac{3b^6}{a^{17}}.
\tag{51.10}
\]
residue 선택 전에 결정된 J개의 유한 구간 family에서 (51.6)이 모두 성립하면
\[
\boxed{\Pr\{\text{어느 한 구간의 (51.10) 편차 발생}\}
\le \min(1,3Jb^6/a^{17}).}
\tag{51.11}
\]
구간끼리 겹쳐도 되며 독립성은 필요 없다. 사후에 결과를 보고 고른 family를
사전 고정 family처럼 취급하지 않는다.
이 사건의 여집합에서는 동시에
\[
\left|\frac{N_I}{\sigma\delta Y/a}-1\right|
\le b^{-10}+(1+b^{-10})b^{-3}\le3b^{-3}.
\tag{51.12}
\]

## 5. 80c 정규화의 양측 finite 오차

v=a^20, ln v=20b, ln z>20b는 theory 35 §7의 실제 정의에서 성립한다.
\[
r_s=\frac1{800b^2},\quad 1/v\le r_s<1/10.
\]
1/v<=r_s는 e^(20b)>=800b²에서 따르며 exponential series의 3차 항만으로도
b>=2000에서 충분하다. RS Theorem 7의 양측식과 한 B0 factor 제거를 보존하면
\[
\frac{1-r_s}{1+r_s}
\le\frac{\sigma Y}{80cXb}
\le\frac{1+r_s}{(1-r_s)^2}.
\tag{51.13}
\]
제거할 B0가 product 밖이면 그 correction은 1이다. product 안이면
(1-1/B0)^(-1)<(1-1/v)^(-1)로 상계한다. 하계에서는 삭제가 곱을 키운다.
Y(ln v/ln z)=80cXb는 정확한 항등식이다.

0<=r<=1/10에서 왼쪽은 1-2r 이상, 오른쪽은 1+4r 이하이다.
후자의 충분조건은 1-7r+4r²>=0이며 해당 구간에서 1-7r>=3/10이다. 따라서
\[
\boxed{\left|\frac{\sigma Y}{80cXb}-1\right|\le\frac1{200b^2}.}
\tag{51.14}
\]
이를 (51.12)와 곱하고
3/b+1/200+3/(200b³)<1/100 (b>=2000)을 쓰면
\[
\boxed{\left|\frac{N_I}{80c\delta Xb/a}-1\right|\le\frac1{100b^2}}
\tag{51.15}
\]
가 (51.11)의 실패확률 밖에서 family 전체에 성립한다.

이것은 FMT (5.7)/(6.14)의 **필요한 actual finite replacement**다.
인쇄된 sigma의 O(b^-10) rate를 복원한 것이 아니라, 충분한 O(b^-2) rate를 직접 썼다.
이후 다른 proof에서 더 강한 rate가 필요하면 별도로 재검토한다.

## 6. disjoint grid와 적용 범위

사전에 정한 정수 M_grid<=a^(1/4)에 대해
\[
I_j=(jY/M_{\rm grid},(j+1)Y/M_{\rm grid}],\quad 0\le j<M_{\rm grid}
\]
는 (0,Y]의 서로소 분할이다. Q'에 제한해도 중복·누락이 없다.
전체 구간 (0,Y]을 함께 요구하면 J=M_grid+1로 (51.11)을 쓰면 된다.
이미 cell에 포함되는 경우에도 이 느슨한 union 상계는 유효하다.
실제로 이만큼 큰 배열을 만들거나 소수를 나열한 것은 아니다.

이 cell count 사건이 성립할 때 임의 (alpha Y,beta Y]는
많아야 M_grid·delta+2개 cell로 덮이고 적어도
max(M_grid·delta-2,0)개의 완전한 cell을 포함한다. 따라서
E0=80cXb/a, rho=1/(100b²)에 대해
\[
(1-\rho)E_0\max(\delta-2/M_{\rm grid},0)
\le N_{(\alpha Y,\beta Y]}
\le(1+\rho)E_0(\delta+2/M_{\rm grid}).
\tag{51.16}
\]
새 확률 union을 하지 않고 동일 cell 사건의 결정론적 결과로 얻는다.
이는 **covering 전** S(A)의 count뿐이다. hypergraph 선택 뒤의 e'_p,
arbitrary subset 보존, all-final-X coverage는 R07/R08/R12에서 아직 닫아야 한다.

## 7. 검증 범위와 판정

bounded exact toy는 residue vector 전수와 별도 prime-product oracle의 평균·분산,
ordered pair/diagonal, closed/half-open atom, partition 회계를 대조한다.
finite union에는 독립성이 필요 없음을 확인하고 사후 family 플래그를 거부한다.
거대한 X나 k개 원소를 만들지 않는다. 수치 toy가 이 해석적 전 범위 증명을
독립 형식 인증한 것으로 간주하지 않는다.

DEP-R03은 위 폭·유한 family 조건을 가진 actual child로 explicit이다.
이를 임의 미세 구간이나 최종 G의 구간으로 확대하지 않는다.
전체 X_cert·threshold calculator는 OPEN/NOT READY다.
