# Sono/FMT H1b-P91a: W-filtered unweighted moment와 실제 구간 정규화

- 작성: 2026-09-09 KST
- 증거 수준: PROJECT FINITE ANALYTIC PROOF; 독립 심사·Lean 인증 아님
- 상태: MAYNARD-W-FILTERED ACTUAL APPLICATION EXPLICIT; literal unfiltered transfer는 미인증
- 계약: data/Sono_FMT_H1bP91a_unweighted_moment_v1.json
- 검산: source/h1bp91a_unweighted_moment.py
- 검토: ../../review/51_20260909_H1bP91a_unweighted_moment_W_filter_타당성검토.md

## 1. 결론과 범위

P92a의 identity-selected prime moment 다음으로, 모든 정수에 대한 unweighted moment를 닫는다.
다만 원문 대조에서 발견한 weight 정의 차이를 숨기지 않는다. 이 문서의 weight는
Maynard 출판 (7.5)의 **명시적 W-coprimality filter가 있는** \(w^*\)다.

외부 크기를 \(X\), \(L=\log(X/2)\)라 두고
\[
 k=\lfloor L^{1/5}\rfloor\ge10^{200},\quad
 y_R=\log R=(L-\log2)/9,\quad
 c=\frac1{153600\log5},\quad
 Y=cX\frac{\log X\,\log_3X}{\log_2X}
 \tag{45.1}
\]
로 둔다. 모든 로그는 자연로그이고 아래첨자는 반복 횟수다.
\(Y\)는 긴 구간 끝점이며 \(y_R\)와 다르다. 다변수 sieve \(F\)와 empirical scale \(F(x)\)도 다르다.

\(m=\lfloor Y\rfloor,\ T'=2m,\ N=T'+1\),
\(p\in\mathbb P\cap(X/2,X]\), admissible \(h_i\in[2k^2]\)에 대해
\[
 \mathcal L^-_p=\{n+h_ip-3m:1\le i\le k\},\qquad
 \mathcal M_p=(B/\varphi(B))^k\mathfrak S_B(\mathcal L_p)\,y_R^k I(F)
\]
라 쓴다. \(B\)는 기존 construction의 같은 exceptional parameter이고 \(B\le(X/2)^2\)를 쓴다.
그러면
\[
 \boxed{\left|\sum_{T'\le n\le2T'}w^*_{\mathcal L^-_p}(n)-N\mathcal M_p\right|
 \le \eta_k N\mathcal M_p,\qquad
 \eta_k=10^{134}\frac{(\log k)^4}{k^2}<(\log T')^{-1/10}.}
 \tag{45.2}
\]
또한 original symmetric interval에 대하여
\[
 \boxed{\left|\sum_{|n|\le Y}w^*_{\mathcal L_p}(n)-2Y\mathcal M_p\right|
 \le 2\eta_k(2Y\mathcal M_p)
 <(\log T')^{-1/10}(2Y\mathcal M_p).}
 \tag{45.3}
\]
이는 actual P91의 상대 multiplier 1을 제공한다. sufficient child cutoff는 P92a와 같은
\(X\ge2\exp(10^{1000})\)다. **최소 시작점·전체 \(X_{\rm cert}\)·소수 전수검사 결과가 아니다.**
공통 singular series \(\mathfrak S\), \(\tau,u\), growing-k P94 및 상위 확률·분포 budget은 남는다.

## 2. 원문 우선 조사와 W-filter 적용 범위 교정

직접 원천:

- Maynard, [Dense Clusters of Primes in Subsets](https://doi.org/10.1112/S0010437X16007296),
  arXiv:1405.2593, 출판 p.1530 (7.5), pp.1538--1540 P9.1 (9.1)--(9.15).
- FGKMT, [Long Gaps Between Primes](https://doi.org/10.1090/jams/876),
  arXiv:1412.5029, pp.95,97--101 Definition 2, (7.4), Theorem 6, actual shift.
- 공개 [PrimeGapsLib S1_aggregate](https://github.com/AxiomMath/PrimeGapsLib/blob/main/PrimeGapsTheory/Sieve/S1/ApplyPartialSum.lean)
  선언도 조사했다. fixed k와 존재형 C,N0, 별도 W(N)·Fmax를 쓰므로 이 growing-k 수치 package의
  drop-in으로 채택하지 않는다. 저장소 전체 axiom·build 감사를 한 것은 아니다.
- FGKMT author-hosted 원고의 (7.4)도 같은 표시다. 표적 검색에서 이 차이를 해결하는 공식
  erratum을 확인하지 못했다. “공식 오류 확정”이나 세계적 novelty로 표현하지 않는다.

Maynard (7.5)는
\[
 \chi_{\mathcal L,W}(n)=1_{\gcd(W,\prod_iL_i(n))=1},\qquad
 w^*_{\mathcal L}(n)=\chi_{\mathcal L,W}(n)
 \left(\sum_{d_i\mid L_i(n)}\lambda_{\mathbf d}(\mathcal L)\right)^2
 \tag{45.4}
\]
를 명시한다. FGKMT (7.4)의 표시식에는 \(\chi\)가 없다.
\(\mathbf d\)의 support가 \(WB\)와 서로소라는 사실은 (45.4)를 자동으로 만들지 않는다.

예를 들어 toy에서 \(W=30,\mathcal L=\{n,n+2\},\lambda_{(1,1)}=3\),
나머지 coefficient가 0이면 raw weight는 항상 9지만 filtered weight는 W-bad residue에서 0이다.
이는 실제 거대 parameter 정리의 반례가 아니라 두 정의가 일반적으로 다름을 보이는 예다.
실제 nonnegative profile에서도 \(\lambda_{\mathbf1}>0\)다. 유한한 모든 \(s\le R,\ s\nmid WB\)에서
admissibility로 비근 residue를 고르고, 별도 \(p_0\mid W\)에서 root residue를 골라 CRT로 합치면,
raw divisor sum은 \(\lambda_{\mathbf1}\)이지만 filter는 0인 정수가 존재한다.
이 정수가 분석 dyadic interval 안에 있다는 주장은 필요하지 않다.

P91/P92의 출판 proof는 처음부터 W-good residue만 합한다. 따라서 이 프로젝트의 P92a도
그 **이미 사용한 가정**을 명시해야 한다. theory 44의 수치식과 검산값은 filtered weight에 대해
보존된다. literal unfiltered (7.4)에 적용됐다고 읽히는 문장은 교정한다.
원문 PDF·과거 완료 handoff·actual 실험 artifact는 변경하지 않는다.

### 2.1 보완 construction의 두 변환

정수 이동은
\[
 \chi_{\mathcal L^-_p,W}(n)=\chi_{\mathcal L_p,W}(n-3m)
\]
이고 root label과 singular series도 같은 변수 이동으로 보존된다.
따라서 weight shift는 pointwise exact다.

prime slice \(p\in\mathbb P,\ q\in\mathbb P,\ p,q>2k^2\)에서
\[
 \mathcal L_p(q-h_ip)=\{q+(h_j-h_i)p\}_j,\quad
 \widetilde{\mathcal L}_{q,i}(p)=\{p,\ q+(h_j-h_i)p\ (j\ne i)\}.
\]
교체된 두 값 \(q,p\)가 모두 W와 서로소이므로 두 filter가 정확히 같다.
따라서 이후 common coefficient ratio를 증명하면 기존 P92 prime-slice 변환에 filter 손실은 없다.
pointwise upper bound는 \(0\le w^*\le w_{\rm raw}\)여서 기존 envelope를 보존한다.

이것은 good-weight construction의 명시적 repair 경로이지, unfiltered 식과 filtered 식을
동일한 함수라고 선언하는 것이 아니다. P94·FMT 전체의 공통 합성은 후속 gate다.

## 3. 실제 규모·끝점 조건

\(u=\log X=L+\log2\)라 두자. \(1<\log5<2\)에서
\[
 1/307200<c<1/153600<1.
\]
\(L\ge10^{1000}\)이면 \(\log\log u\ge1,\ \log u\le\sqrt u\)이고
\[
 \frac{Y}{X}=cu\frac{\log\log u}{\log u}
 \ge\frac{\sqrt u}{307200}>2,\qquad Y<Xu.
\]
따라서
\[
 X\le T'=2\lfloor Y\rfloor\le2Xu,\qquad L\le\log T'\le2L.
 \tag{45.5}
\]
후자의 upper는 \(u+\log(2u)\le2L\)에서 따른다. \(L\ge10\)에서
\(\log(4(L+1))\le L\)을 미분 또는 초등 지수 하계로 확인하면 충분하다.
이제
\[
 k\le(\log T')^{1/5},\quad (T')^{1/30}\le R\le(T')^{1/9}.
 \tag{45.6}
\]
첫 R 부등식은 \(2L/30\le(L-\log2)/9\), 두 번째는 \(T'\ge X\)에서 충분하다.
\(B\le(X/2)^2\le(T')^2\)이며
\[
 |h_ip-3m|\le(2k^2+3u)X\le5uX\le X^2\le(T')^2.
\]
\(5u\le e^u\)는 \(u\ge10\)에서 충분하다. 따라서 기존 \(\alpha=2,\theta=1/3\)의
actual local-factor package를 **T' 규모에서** 적용할 수 있다. P92의 exact bin을 T'에 복사하지 않는다.

closed interval은 정확히 \([2m,4m]\)이며 \(n\mapsto n-3m\)는 \([-m,m]\)로의 전단사다.
\[
 N=2m+1,\qquad |N-2Y|\le1.
 \tag{45.7}
\]
half-open \([2m,4m)\)를 대신 쓰면 끝 정수 하나가 사라진다. 최종 통계의 end-bounded
prime-gap 정의를 바꾼 것은 아니고, 여기서는 별도 sieve interval 회계를 하는 것이다.

## 4. 재사용하는 유한 해석 입력

theory 44 §§4--5와 theories 17,23,24,28에서
\[
 \ell=\log k,\ K=k\ell,\quad I(F_1)\le2I(F),\quad I(F_2)\le4k^2I(F),
 \quad F\le F_2/k,
\]
\[
 \mathfrak S_B\ge e^{-9k/2},\quad I(F)\ge(2k\ell)^{-k},\quad
 |\lambda_{\mathbf d}|\le e(y_R/k)^k
 \tag{45.8}
\]
를 사용한다. 마지막 inequality는 다음 common smooth gate에 의해 성립한다.
\[
 \Lambda_*=2k^2\log(2k^2)+k(k-1)\log2+
 \{60(2k^2-k+1)+k\}y_R,\qquad
 \delta=\frac{10^{123}(6+\log\Lambda_*)\,3000k^3\ell^2}{y_R}.
 \tag{45.9}
\]
(45.6)에 의해 이전 제외모듈 proof의 \(\log T'\le30y_R\) 가정을 보존한다.
\[
 y_R\ge k^5/30,\quad
 \delta\le10^{130}\ell^3/k^2<1/2.
\]
positive smooth upper factor는 \(e^\delta<3\), error factor는 \(e^\delta-1\le2\delta\)다.
\(F_2^2\)에서 support-[0,2] 좌표를 먼저 합하는 순서를 바꾸지 않는다.
P91의 두 actual family는 L737_canonical, L752_canonical이다.
고정-k의 \(2^k\) comparison은 이 growing-k 경로에 사용하지 않는다.

## 5. CRT 분포오차: 실제 정수 구간의 이점

어떤 연속된 N개 정수에서든
\[
 E_q^{(1)}=\max_a|\#\{n:n\equiv a\bmod q\}-N/q|\le1
 \tag{45.10}
\]
이다. 따라서 이 actual P91에는 소수분포 Hypothesis 1(2)나 미지 implied constant가 필요 없다.

각 W-good residue에서 compatible pair는 \(q=W\prod_i[d_i,e_i]\le WR^2=:z\) 하나를 정한다.
squarefree prime마다 최대 3k개의 coordinate/membership 선택이 있어 multiplicity는
정확한 계수 1로 \(\tau_{3k}(q)\) 이하다.
\[
 \sum_{n\le z}\tau_j(n)\le z(1+\log z)^{j-1}\le z(1+\log z)^j
 \quad(j\ge1,z\ge1)
 \tag{45.11}
\]
는 j-tuple의 마지막 변수를 먼저 세어 증명한다.

\(w_W=2k^2\log(2k^2)\)를 \(\log W\)의 upper로 쓴다.
최대 W개 residue를 합친 전체 CRT 오차 \(\mathcal D\)는
\[
 \mathcal D\le W e^2(y_R/k)^{2k}z(1+\log z)^{3k}.
\]
(45.8), \(N\ge e^L\)를 넣으면
\[
\begin{split}
 \log\frac{\mathcal D}{N\mathcal M_p}
 \le\;&2+2w_W+2y_R-L
 +k\log y_R-k\ell+k\log(2\ell)+\tfrac92k\\
 &+3k\log(1+w_W+2y_R)
 \le-L/2 .
\end{split}
\tag{45.12}
\]
여기서 \(\ell\le k/2,\ k^3\ge200(k+1)\)에서 \(w_W\le L/100\)이고
\(2w_W+2y_R<L/4\), \(1+w_W+2y_R\le L\)다.
나머지는 \(\log L<6\ell,\log(2\ell)\le\ell\)로
\(26k\ell+6k+3\le13k^2+6k+3\le k^5/4\)로 흡수한다.
필요한 다항식은 \(k\ge36\) 전체에서 성립한다. 따라서
\[
 \mathcal D/(N\mathcal M_p)\le e^{-L/2}.
 \tag{45.13}
\]

## 6. 대각항의 exact Euler 정규화

\(D=WB/\varphi(WB),\ S=\mathfrak S_{WB}\)라 두고
\(y_{\mathbf r}=D^k S F(\log\mathbf r/y_R)\),
\(Y_{\mathbf r}=D^k S F_2(\log\mathbf r/y_R)\)라 쓴다.
각 \(p\nmid WB\)에는 \(\omega(p)\)개 slot이 있다.
Maynard (9.5)의 local matrix는 대각 \(p-1\), 비대각 \(-1\),
row sum은 \(p-\omega(p)\)다. \(y_{\mathbf s}\)를 \(y_{\mathbf r}\)로 바꾸면 정확히
\[
 \sum_{\mathbf r\in D_k}\frac{y_{\mathbf r}^2}{\varphi_\omega(r)}
\]
를 얻는다. 이 smooth sum의 Euler factor는
\[
 \left(1+\frac{\omega}{p-\omega}\right)(1-1/p)^k,
\]
그리고 S의 local factor와 곱하면 정확히 1이다.
그래서 diagonal main은 \(D^k S\,y_R^k I(F)\),
relative error는 \(2\delta I(F_1)/I(F)\le4\delta\)다.

P92에서는 slot 수와 대각이 각각 \(\omega-1,p-2\)였다는 차이를 보존한다.
P92의 local matrix를 P91에 복사하지 않는다.

## 7. off-diagonal 재배치 오차

\(r=\prod r_i=\prod s_i\), \(A=r/\prod_i(r_i,s_i)\)라 두면
변경된 소수의 곱이 A다. 기존 Lemma 8.2 multiplier 89에서
\[
 |y_{\mathbf s}-y_{\mathbf r}|
 \le89K\frac{\log A}{y_R}(Y_{\mathbf r}+Y_{\mathbf s}),\qquad
 0\le y_{\mathbf r}\le Y_{\mathbf r}/k .
\]
대칭 양의 합에서 \(Y_rY_s\le(Y_r^2+Y_s^2)/2\)를 쓰면 계수는 178이다.
source (9.8)--(9.9)처럼 A의 소수를 제거한 r'로 바꾸고 감소성을 사용한다.
재구성 slot 수는 \(\omega(A)\), 변경 slot 수는 \(\prod_{p\mid A}(\omega(p)-1)\).
따라서 tail을
\[
 \sum_{\substack{A\ {\rm squarefree}\\(A,WB)=1}}
 \log A\prod_{p\mid A}\frac{\omega(p)^2}{(p-\omega(p))^2}
 \le72\ell
 \tag{45.14}
\]
로 상계할 수 있다. 이는 theory 44 (44.20)의 같은 positive tail이다.
\(p>2k^2\), \(\prod(1+4k^2/p^2)<9\),
\(4k^2\sum_{n>2k^2}\log n/n^2\le8\ell\)를 사용한다.

남은 sum의 denominator는 \(g(p)=(p-\omega)^2/(p-1)\)이며 local factor에 S를 곱하면
\[
 \left(1+\frac{\omega(p-1)}{(p-\omega)^2}\right)
 \left(1-\frac\omega p\right)
 =1+\frac{\omega(\omega-1)}{p(p-\omega)}.
 \tag{45.15}
\]
전체 곱은 \(e^2<9\) 이하이다. smooth upper <3까지 적용하면
잔여 sum은 \(27D^kS y_R^k I(F_2)\) 이하이다.
따라서 relative off-diagonal error는
\[
 E_{\rm off}\le
 (178\cdot72\cdot27\cdot4)\frac{kK\ell}{y_R}
 =1{,}384{,}128\frac{k^2\ell^2}{y_R}
 \le41{,}523{,}840\frac{\ell^2}{k^3}.
 \tag{45.16}
\]
source에서 O(1)로 넘긴 tail과 Euler 곱을 위 식처럼 계수로 분리해 보존했다.

## 8. W residue 합성과 전체 finite error

good residue 수는 \(\varphi_\omega(W)=\prod_{p\mid W}(p-\omega(p))\)다.
각 residue의 prefactor \(N/W\)와 \(D^kS\)를 합치면
\[
 \frac{\varphi_\omega(W)}W D^kS
 =(B/\varphi(B))^k\mathfrak S_B .
 \tag{45.17}
\]
filter가 없으면 “good residue만” 세는 이 단계가 정당화되지 않는다.

전체 상대오차는
\[
 E_{91}\le4\delta+1{,}384{,}128\,k^2\ell^2/y_R+e^{-L/2}
 \le10^{134}\ell^4/k^2=\eta_k .
 \tag{45.18}
\]
(45.9), \(y_R\ge k^5/30,\ell\ge1\), \(e^{-k^5/2}\le k^{-2}\)로 충분하다.
\(\ell\le k^{1/8}\)와 \(k\ge10^{200}\)에서
\[
 2\eta_k\le 2\cdot10^{134}/k^{3/2}
 \le1/(2\sqrt k)<(2L)^{-1/10}\le(\log T')^{-1/10}.
 \tag{45.19}
\]
가운데 엄격 부등식은 \(L<(k+1)^5\)와
\(2(k+1)^5<2^{10}k^5\)로 충분하다.

(45.7)에서 \(a=|N/(2Y)-1|\le1/(2Y)\le e^{-L}\)이고 \(E_{91}<1\)이므로
\(2Y\mathcal M_p\)에 대한 상대오차는
\(E_{91}+(1+E_{91})a\le E_{91}+2e^{-L}\le2\eta_k\)다.
이로써 (45.2)--(45.3)을 얻는다. \(\mathcal M_p\)를 공통 \(\mathfrak S\)로 바꾸지는 않았다.

## 9. 검증과 반증 지향 toy

- exact dimension bin의 바로 아래와 위 endpoint를 거부한다.
- 정수 CRT discrepancy, divisor tuple counting, local row sums와 Euler 항등식을 별도 계산한다.
- W-filter가 λ support만으로 생기지 않음을 negative toy로 확인한다.
- shift 전단사와 prime-slice filter equality를 모든 toy residue에서 확인한다.
- \(Y\)가 정수/비정수일 때 \(|2\lfloor Y\rfloor+1-2Y|\le1\)을 확인한다.
- 거대한 \(X,Y,T',W\), k개 배열 또는 실제 prime list를 만들지 않는다.
- scalar 진단은 log-scale에서 수행하며 부동소수 PASS를 전 구간 증명의 대체로 쓰지 않는다.
- 필수 filter를 끈 certificate 요청은 거부한다. 반환 metadata도 filter 조건과 literal
  unfiltered transfer 미인증을 별도 기록한다.
- 신규 실제 실험·그래프·threshold calculator는 없다.

## 10. 다음 단계

H1b-P94g: 기존 fixed-k P94를 uniform \(I(F_1),I(F_2)\) 비교로 growing-k 경로에 연결한다.
이때도 (45.4)의 weight 정의를 명시하고 실제 shifted interval·추가 form을 점검한다.
그 다음 H1b-NORM에서 singular-series ratio, λ/weight square ratio, \(\tau,u\) 및
필요 lemma 집합을 합성한다. P95는 actual 사용처 확인 전 root 필수라고 단정하지 않는다.
full good-weight, SIV-07/08/09, \(X_{\rm cert}\)는 아직 닫히지 않았다.
