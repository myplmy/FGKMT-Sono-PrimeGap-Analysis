# Sono/FMT H1c-1b.4d corrected source-constant reproof

- 작성: 2026-09-09 KST
- 증거 수준: `PROJECT FINITE LEMMA / EXACT RATIONAL CORNER AND CALCULUS CHECK`
- 판정: `CORRECTED SOURCE C_A REPROOF CLOSED FOR r>=10^10 / PARENT COMPOSITION PENDING`
- H1c-1b.4d: `CLOSED`
- Hypothesis 1(2), Maynard Proposition 9.2, `SIV-08`: `OPEN` — 다음 composition 감사 전에는 승격하지 않음
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b4d_source_constant_reproof_v1.json`](data/Sono_FMT_H1c1b4d_source_constant_reproof_v1.json)
- 검산 구현:
  [`source/h1c1b4d_source_constant_reproof.py`](../../../source/h1c1b4d_source_constant_reproof.py)
- 비판적 검토:
  [`docs/review/47_20260909_H1c1b4d_source_constant_reproof_타당성검토.md`](../../review/47_20260909_H1c1b4d_source_constant_reproof_타당성검토.md)

## 1. 결론

Bordignon 2021 Theorem 1.2의 출판 상수식 (33)은 그 상태로 numerical input으로 쓸 수
없다. H1c-1b.4a에서 확인했듯 첫 항에 absolute remainder \(R^*\)의 \(x\)-정규화가 빠져
있기 때문이다. 이번 단계는 그 식을 고쳐 썼다고 가정하지 않고, 최종판 Theorem 3.4와
식 (28)--(32)의 모든 항을 actual target에서 직접 다시 합성했다.

다음을 둔다.

\[
L=\log x,\qquad \ell=\log L,\qquad
A=100r^2+10,\qquad B=A\ell,\qquad H=L^{2A}.
\tag{41.1}
\]

여기서 \(H\)는 소수간격 함수가 아니라 explicit formula의 contour height다. 모든
\(2\le q\le L^A\)에 대해 corrected target에 들어가는 열세 component를 얻고,

\[
\boxed{
r\ge10^{10},\quad L\ge r^5
\quad\Longrightarrow\quad
C_A<13e^{-100}<1
}
\tag{41.2}
\]

을 증명했다. H1c-1b.4c의 같은 지점 허용량은 \(e^{631.789\ldots}\)보다 크므로 이
source bound는 충분히 들어간다. 따라서 **새 cutoff에서 full numerical absorption의
마지막 미지 상수는 닫혔다.** 다만 공통 exceptional \(B\), dyadic endpoint, exact
recentring, modulus와 quantifier가 한 정리 호출로 정확히 연결되는지는 H1c-1b.4e에서
별도로 감사한다. 이번 단계만으로 H1(2)나 P9.2를 닫았다고 쓰지 않는다.

## 2. 쉬운 설명

앞 단계에서는 “논문 속 미지 상자 \(C_A\)가 어느 정도 작으면 전체 오차가 합격하는가”를
계산했다. 이번에는 그 상자를 논문의 더 아래쪽 식까지 뜯어 열세 조각으로 나눈 뒤, 조각을
하나도 빼지 않고 각각의 최대 크기를 잰 것이다.

- \(r=5\times10^8\)에서는 zero 항 네 개의 보수적 상계가 아직 너무 커서 증명이 안 된다.
- \(r=10^{10}\)에서는 열세 조각이 각각 \(e^{-100}\)보다 작다.
- 열세 조각의 합도 1보다 작고, 앞 단계가 허용한 크기보다 훨씬 작다.

이는 실제 소수를 \(e^{10^{50}}\)까지 계산했다는 뜻이 아니다. 식의 양변을 exact inequality로
비교한 **증명 cutoff**다. 또한 \(e^{10^{50}}\)은 최종 Sono/FMT threshold가 아니라 이
하위 부품 하나의 매우 보수적인 시작점이다.

## 3. 원 출처 우선 조사와 판본 차이

### 3.1 채택한 원 출처

1. Matteo Bordignon, *Medium-sized values for the prime number theorem for primes in
   arithmetic progressions*, New York J. Math. 27 (2021), 1415--1438,
   [journal page](https://nyjm.albany.edu/j/2021/27-54.html).
   사용 위치: Theorems 1.2, 3.4, 식 (28)--(33), Corollary 4.3.
2. M.-C. Liu and T. Wang, *Distribution of zeros of Dirichlet L-functions and an
   explicit formula for psi(t,chi)*, Acta Arith. 102 (2002), 261--293,
   DOI [10.4064/aa102-3-5](https://doi.org/10.4064/aa102-3-5).
   사용 위치: Theorems 1--2, Tables 1, 3--5에서 Bordignon이 옮긴 zero-density 수치의
   원천 대조.

현재 target에 그대로 대입할 수 있는 별도 후속 정리나 공식 erratum은 표적 검색에서 찾지
못했다. 이는 전 세계 문헌에 없다는 novelty 주장이 아니다. 따라서 직접 증명한 부분은 새
zero-density theorem이 아니라, 위 source upper들을 actual parameter에 보수적으로 합성한
project bridge다.

### 3.2 최종판의 `2q`를 보존

최종 NYJM판 식 (31)의 low-height zero upper에는 \(2q\)가 있다. arXiv v1 display에는
그 \(q\)가 없다. 최종 출판식을 우선하여 \(2q\) 전체를 보존한다. 이 판본 차이 때문에
low-zero component의 계수와 \(L\)-지수도 final 식에서 다시 유도했다.

### 3.3 알려지지 않은 Liu--Wang 대안을 임의 선택하지 않음

Corollary 4.3은 특정 \(i\)를 주는 것이 아니라 “어떤 \(i=1,\ldots,6\)”이 존재한다고 한다.
따라서 가장 좋아 보이는 \(i=6\)을 임의로 쓰지 않는다. 각 \(i\)에서 합법적인 \(J=0\)을
고른 뒤 여섯 경우 모두의 최대를 잡는다.

- \(\Sigma_0\)에는 모든 경우
  \(\max(\xi_{i+1},\nu_1)=0.26213\)을 쓸 수 있다.
- high-zero branch에는 모든 \(\eta_i,\xi_{i+1}\) 중 최소인
  \(0.16=4/25\)만 공통 감쇠율로 쓴다.

이 선택은 더 날카로운 `min_J` 값을 버리는 대신 unknown-\(i\) 논리 오류를 피한다.

## 4. corrected remainder normalization

Theorem 1.2의 character sum target과 Theorem 3.4를 직접 합치면 explicit-formula
remainder의 필요한 기여는

\[
q\frac{R^*(x,H,q)}x L^{A-3}
\le \frac{R^*(x,H,q)H}{xL^3},
\tag{41.3}
\]

이다. 여기서 \(q\le L^A\), \(H=L^{2A}\)를 썼다. 이것이 H1c-1b.4a에서 얻은
정규화이고, 최종판 식 (33)의 무차원화되지 않은 첫 항이나 arXiv v1의 다른 식을 그대로
가져오지 않는다.

또

\[
q\le e^B,\qquad H=e^{2B},\qquad \log(qH)\le3B
\tag{41.4}
\]

이다. actual centered identity-form에서 \(q=1\) 항은 정확히 0이므로, \(\log q\)가
들어가는 source bound는 \(q\ge2\)에만 적용한다.

## 5. Theorem 3.4 remainder 아홉 항

최종판의 표시식과 \(x\ge e^{r^5}\), \(H=L^{2A}\), \(q\le L^A\)에서 다음 보수적
중간 upper를 쓴다.

\[
r_1(q,t)\le\log(qt)+5,quad r_4(H,q)\le16B,quad
\max r_5\le14B,quad\max r_6\le4B,
\tag{41.5}
\]

\[
R_2+R_3\le10000\frac{xL^2}{H},\quad R_5\le8LH,quad
R_7\le10000\frac{xB^2}{H},
\tag{41.6}
\]

\[
R_8\le72\frac B H,qquad
R_{11}\le2\sqrt{x}\,B^2e^{B/2}.
\tag{41.7}
\]

상수는 최소화하지 않았다. (41.3)으로 나눈 각 component의 자연로그 upper는 다음과 같다.

| 번호 | 원천 | log upper |
|---:|---|---|
| 1 | induced-character \(\log q/\log2\) | \(\log2+\log B+2B-L-3\ell\) |
| 2 | \(R_2+R_3\) | \(\log10000-\ell\) |
| 3 | \(\log2\) | \(2B-L-3\ell\) |
| 4 | \(R_5\) | \(\log8+4B-L-2\ell\) |
| 5 | \(R_7\) | \(\log10000+2\log B-3\ell\) |
| 6 | \(R_8\) | \(\log72+\log B-L-3\ell\) |
| 7 | \(\log x\) | \(2B-L-2\ell\) |
| 8 | \(x r_4/(H-1)\) | \(\log32+\log B-3\ell\) |
| 9 | \(R_{11}\) | \(\log2+2\log B-3\ell-L/2+(5/2)B\) |

Theorem 3.4의 항을 합치기 전에 버리지 않았으며, JSON과 unit test가 component 수 9를
고정한다.

## 6. zero decomposition 네 항

식 (29)의 최종판

\[
S(H,q)=\frac2\pi\log\frac q{2\pi e}+2r_1(q,1)
+\frac{\log H}{2\pi}
\left(\log H+2\left(\log\frac q{2\pi e}+1\right)\right)+0.298
\]

에는 이 범위에서 안전한 \(S(H,q)<8B^2\)를 쓴다. 오래된 arXiv v1의 더 큰 모양을
최종판 정의와 혼합하지 않는다. 최종 식 (31)의 \(2q\)와 식 (32)의 unknown-\(i\) 처리를
포함하면 나머지 네 component는 다음과 같다.

| 번호 | 이름 | log upper |
|---:|---|---|
| 10 | low-height zeros, final \(2q\) | \(\log8+\log(B+5)+(2A-3)\ell-L/(R_0B)\) |
| 11 | \(\Sigma_0\) | \(\log4+2\log B+(2A-3)\ell-0.26213L/(3B)\) |
| 12 | high zeros, square-root branch | \(\log4+(3A-3)\ell-2\sqrt{L/R_0}\) |
| 13 | high zeros, logarithmic branch | \(\log4+(3A-3)\ell-(0.16)L/(3B)\) |

여기서 \(R_0=6.397\)이다. 식 (32)의 두 주항을 최대값의 두 배로 잡았으므로 계수 4가
남는다. source의 더 좋은 table 조합은 사용하지 않아도 증명에 충분하다.

## 7. exact cutoff와 전 구간 uniformity

### 7.1 첫 corner

\(r_0=10^{10}\), \(L_0=r_0^5=10^{50}\)로 둔다. 지수급수의 유리수 부분합·tail로

\[
2.7<e<2.719,qquad e^{23}<10^{10}<e^{24}
\]

을 exact integer arithmetic으로 확인한다. 따라서

\[
115<\ell_0=5\log r_0<120,quad
B<12001r_0^2,quad \log B<72.
\tag{41.8}
\]

이를 §5--6의 열세 식에 대입한 rational upper가 모두 \(-100\)보다 작다. floating-point
계산은 이 부등식의 증거가 아니다.

### 7.2 고정 \(A\)에서 \(L\) 증가

각 dimension bin 안에서는 \(A\)를 고정한다. §5의 항은 직접 미분하면 감소한다.
10, 11, 13번의 핵심 음의 항 \(L/(cA\ell)\)은

\[
\frac{d}{d\ell}\frac{L}{A\ell}
=\frac{L(\ell-1)}{A\ell^2}
\]

로 증가하고, 12번의 \(\sqrt L\)도 양의 log-polynomial보다 빠르게 증가한다. 첫 corner의
exact derivative inequalities가 네 critical 항의 감소를 확인한다.

### 7.3 dimension corner 사이

corner에서 \(L=r^5\), \(\ell=5\log r\)다. critical negative-to-positive derivative
비율은 각각 \(r/(\log r)^2\) 또는 \(\sqrt r/\log r\)에 의해 아래에서 제어된다. 두 함수는
\(r\ge10^{10}\)에서 증가한다. helper는 첫 corner에서 다음 보수적 exact 비교를 확인한다.

\[
\frac{29r^2}{848400}>49001r,qquad
\frac{116r^2}{9000750}>73501r,qquad
5\sqrt r>3\cdot73501.
\tag{41.9}
\]

나머지 항은 \(-r^5\), 감소하는 \(\ell\)-power 또는 더 단순한 같은 비교를 가진다.
따라서 이후 half-line과 모든 차원 corner에서 upper가 다시 커지지 않는다.

## 8. 합성과 predecessor allowance

열세 항을 \(u_j\)라 하면

\[
C_A\le\sum_{j=1}^{13}u_j<13e^{-100}<1.
\tag{41.10}
\]

H1c-1b.4c는 같은 dimension corner에서

\[
\log C_{\mathrm{allow}}=631.7890814632124882\ldots
\]

를 허용한다. 반면 이번 source 합의 100자리 회귀값은

\[
\log C_A<-105.9189142777261014\ldots.
\]

가장 큰 component는 \(R_2+R_3\)에서 온 `02_rstar_R2_R3`이다. 이 숫자들은 구현 회귀용이며,
증명은 (41.8)--(41.10)의 rational·calculus certificate가 담당한다.

## 9. 왜 이전 \(r=5\times10^8\) cutoff를 쓰지 않는가

H1c-1b.4c의 conditional gate는 \(r=5\times10^8\)부터 열렸다. 그러나 source zero bound를
그 지점에 넣으면 네 log upper가 각각 대략

\[
3.0564\times10^{21},\quad3.9169\times10^{21},\quad
3.0908\times10^{21},\quad6.8456\times10^{21}
\]

으로 양수다. 이는 실제 error가 그만큼 크다는 측정이 아니라, 현재 보수적 상계로는 그
cutoff에서 흡수를 증명하지 못한다는 뜻이다. 따라서 source closure의 더 큰 cutoff
\(r=10^{10}\)을 채택한다. 최소 cutoff라고 주장하지 않는다.

## 10. 닫힌 것과 열린 것

| 항목 | 상태 |
|---|---|
| final Theorem 3.4 remainder 9개 전수 합성 | `CLOSED` |
| final 식 (31)의 \(2q\) 보존 | `CLOSED` |
| unknown Liu--Wang \(i\)의 안전한 최대화 | `CLOSED` |
| zero component 4개 | `CLOSED` |
| \(C_A<1\), H1c-1b.4c allowance 흡수 | `CLOSED FOR r>=10^10` |
| H1c-1b.1--4의 한 호출 composition | `PENDING H1c-1b.4e` |
| H1(2), P9.2, `SIV-08` | `OPEN` |
| 전체 Sono/FMT \(X_{\mathrm{cert}}\) | `OPEN` |

## 11. 다음 gate

H1c-1b.4e는 다음을 한 줄의 quantifier chain으로 다시 검사한다.

1. actual identity form과 \([T,2T)\) endpoint,
2. \(r=\lfloor(\log T)^{1/5}\rfloor\), \(A=100r^2+10\),
3. 한 공통 exceptional prime \(B\),
4. 모든 필요한 modulus와 두 dyadic endpoint,
5. \(\psi\to\pi\) 및 exact centered total,
6. 이번 \(C_A\)와 4c absorption.

하나라도 범위가 맞지 않으면 상위 node는 열린 채로 둔다. 새 package, Lean, actual prime
sweep 또는 사용자 장시간 계산은 이번 단계에 필요하지 않다. 사용자 수행절차는
**별도 수행절차 필요없음**이다.
