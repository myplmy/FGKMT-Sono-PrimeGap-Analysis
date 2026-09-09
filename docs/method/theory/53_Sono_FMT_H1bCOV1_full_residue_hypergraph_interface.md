# Sono/FMT H1b-COV1: full-residue cap와 유한 hypergraph 인터페이스

- 작성: 2026-09-09 KST.
- 수준: PROJECT FINITE ANALYTIC PROOF; 독립 심사·형식 인증 아님.
- 범위: 같은 Sono 계수, theories 47·49–52의 actual fixed-X law.
- 판정: 입력·cap·partition·재귀·복원은 explicit. core Theorem 3의 C0가
  수치화되지 않았으므로 DEP-R07 전체와 X_cert는 OPEN이다.
- 이 문서의 A_hg는 hypergraph test-set size parameter이다. residue vector
  \(\mathbf A\), FMT의 목표 density A, growing sieve dimension k와 구별한다.

## 1. 선행연구를 먼저 확인한 결과

| source | 정확한 위치 | 채택/한계 |
|---|---|---|
| [FMT, arXiv:1511.04468](https://arxiv.org/abs/1511.04468) | PDF pp.9–11, Theorems 4–5, (5.1)–(5.8) | large-degree에서 covering으로 가는 구조; o(1)와 support 연결을 숫자로 보충해야 함 |
| [FGKMT, DOI 10.1090/jams/876](https://doi.org/10.1090/jams/876), [arXiv:1412.5029](https://arxiv.org/abs/1412.5029) | 출판 pp.76–77 / PDF pp.12–13, Theorem 3 (4.1)–(4.11) | 유한 정량 core 정리. 단 C0는 존재만 명시 |
| 같은 FGKMT | pp.78–81 / PDF pp.14–17, Corollary 4 및 proof | 예외점 제거, 독립 partition, degree recursion, 1·2점 moment |
| 같은 FGKMT | p.72 / PDF p.8, Lemma 2.2 | 유계 독립 변수의 Hoeffding bound를 그대로 재사용 |
| 같은 FGKMT | pp.83–89 / PDF pp.19–25, §5 | C0 복원 대상. normalization, 조건부 1·2차 moment와 오차 흡수의 O 상수는 남음 |

FMT가 구 버전의 “Corollary 3”을 가리키지만, 현재 로컬 출판본에서 대응하는
specialized covering은 **Corollary 4**다. 예전 번호와 출판 번호를 섞지 않는다.
FGKMT PDF의 native text를 먼저 읽고 핵심 전체 페이지의 위첨자·분모·support와
quantifier를 대조했다. 새 다운로드·OCR·패키지 설치·실제 소수 계산은 없다.
이번 표적 문헌 확인에서 바로 대입할 numerical C0를 찾지 못했으며, 전 세계
문헌에 없다는 주장이나 새로운 정리의 novelty 주장은 하지 않는다.

### 1.1 앞 문서의 표시 정정

[theory 52](52_Sono_FMT_H1bCOR3_main_degree_finite_moments.md) 식 (52.17)의
마지막 항 앞에 덧셈 기호가 누락됐다. 정확한 식은
\[
 F_{\rm degree}\le\min\left(1,
 \frac{1600c}{b^5}+\frac{800c}{b^{10}}+\frac{112kb^4}{a^{11}}\right).
 \tag{53.E}
\]
이는 앞 절 (52.10), (52.13), COR2를 합한 값이며, COR3 pinned JSON과 helper는
처음부터 이 **합**으로 되어 있다. 수치 결과를 다시 만든 것이 아니다.
hash-pinned 원본을 소급 수정하지 않고 이 successor를 정정 정본으로 둔다.

## 2. 그대로 넘어가면 안 되는 세 연결

1. tuple edge \(\{n_p+h_ip\}_i\cap V_0\)의 크기는 k 이하이지만,
   실제 residue edge \(R_p(n_p)=\{q\in V_0:q\equiv n_p\bmod p\}\)는
   off-tuple 점도 지운다. tuple만의 uncovered 수를 실제 residue의
   **양측** count라고 부르면 틀릴 수 있다.
2. COR3의 예외 수 \(X/(ab)\)는 자동으로 \(\#V_0/b^2\) 이하가 아니다.
   c가 작기 때문이다. 원문의 asymptotic discard를 finite 비용으로 기록해야 한다.
3. “모든 고정 subset에 대해 균일한 실패율”은 “한 번의 결과가 모든 subset에서
   동시에 성공”이라는 뜻이 아니다. covering 결과를 보고 고른 subset에도 자동 적용되지 않는다.

아래에서는 **full residue edge 자체를 cap**하고 버린 질량을 상계한다.
그 뒤 예외점을 잠시 제거하여 Theorem 3를 직접 적용한다. Corollary 4의
예외 비율에 맞추었다고 주장하지 않으며, 복원 비용을 마지막까지 남긴다.

## 3. actual finite 입력과 full-residue cap

theories 47·49–52의
\[
 a=\ln X,\quad b=\ln a,\quad k=\lfloor(\ln(X/2))^{1/5}\rfloor,\quad
 c=(153600\ln5)^{-1},\quad Y=cXa\ln b/b
\]
를 쓴다. 기존 child \(X\ge2\exp(10^{1000})\), \(b>2000\),
\(k\ge10^{200}\)를 유지한다. 이는 최종 X_cert가 아니다.
\(V_0=Q'\cap\mathscr S(\mathbf A)\), \(N=\#V_0\).
고정 residue vector에서 좋은 p는 기존 zeta/D law, 나쁜 p는 n_p=0이다.
\[
 R_p(n)=\{q\in V_0:q\equiv n\pmod p\},\quad
 M_p(n)=\{n+h_ip:1\le i\le k\}\cap V_0,\quad O_p(n)=R_p(n)\setminus M_p(n).
 \tag{53.1}
\]
M_p는 R_p의 부분집합이고 \(\#M_p\le k\)다. 이 포함관계를 사용할 뿐,
residue class를 다른 위치로 옮겨 actual primality를 복사하지 않는다.
조건부 random edge를
\[
 e_p^0=
 \begin{cases}R_p(n_p),&\#R_p(n_p)\le2k,\\
 \varnothing,&\#R_p(n_p)>2k
 \end{cases}
 \tag{53.2}
\]
로 둔다. 큰 edge를 잘라 작은 부분집합으로 바꾸는 것이 아니라 **전체를 ∅로
보내므로**, 남긴 nonempty edge에는 원래 residue witness가 존재한다.
cap 기준은 \(\le2k\)이고 equality를 버리지 않는다.

### 3.1 cap으로 잃는 질량

\(\#R_p>2k\)이면 \(\#O_p>k\)이고 \(\#R_p\le2\#O_p\).
각 q의 잃은 degree를 L_q라 하면 Tonelli의 유한합 교환으로
\[
 \sum_{q\in V_0}L_q
 =\sum_p\mathbb E[\#R_p(n_p)1_{\{\#R_p>2k\}}\mid\mathbf A]
 \le2\sum_p\mathbb E[\#O_p(n_p)\mid\mathbf A]\le4T(\mathbf A).
 \tag{53.3}
\]
마지막 T는 theory 50 (50.6)이다. 좋은-p 분모의
\((1-a^{-3})^{-1}<2\)를 썼으며, 나쁜 p의 residue 0에는 q>p인 소수가 없다.
따라서 (50.7)로
\[
 \mathbb E_{\mathbf A}\sum_qL_q\le\frac{3200cX}{ab^9}.
 \tag{53.4}
\]
\(L_q>b^{-3}\)인 점이 \(X/(ab)\)개보다 많을 확률은
\[
 F_{\rm cap}\le\min(1,3200c/b^5).
 \tag{53.5}
\]
큰 edge를 무시한 비용을 0으로 둔 것이 아니다. 별도의 Markov budget이다.

### 3.2 예외 q를 지우고 입력을 고정

COR3 (52.15)와 COR2 (50.14)에서 예외 \(X/(ab)\)개 밖의 원래 degree는
\[
 |d_{\rm full}(q)-C|\le(3C+2)b^{-3}<1202b^{-3}.
\]
cap 예외까지 합친 집합 E는
\[
 \#E\le\left\lfloor\frac{2X}{ab}\right\rfloor,\qquad
 V=V_0\setminus E,\qquad e_p=e_p^0\cap V
 \tag{53.6}
\]
로 둘 수 있고, 모든 q∈V에서
\[
 |d(q)-C|<1203b^{-3}\le b^{-2},\qquad
 \frac54\ln5<C<400.
 \tag{53.7}
\]
E는 \(\mathbf A\)와 그 조건부 law로 결정하며, **나중 covering outcome**으로
선택하지 않는다. V로 project해도 그 안의 q의 degree는 변하지 않는다.
원래 degree와 cap 사건의 union 실패율은
\[
 F_{\rm prep}\le\min\left(1,\frac{4800c}{b^5}
       +\frac{800c}{b^{10}}+\frac{112kb^4}{a^{11}}\right).
 \tag{53.8}
\]
R03의 사전 고정 J개 구간 사건도 쓰면 \(3Jb^6/a^{17}\)을 더한다.
독립성을 가정하지 않는다.

R03 whole-interval 사건에서
\[
 N\ge79cXb/a,\qquad \frac{\#E}{N}\le\frac{8000}{b^2}<1.
 \tag{53.9}
\]
\(2/(79c)=307200\ln5/79<614400/79<8000\)을 사용했다.
따라서 V는 비어 있지 않다. 또한 \(\#P'\le X\), \(\#V\le N< X^2\).
Corollary 4의 \(\#V_0/b^2\) 예외 가정을 충족했다고 거짓 표시하지 않는다.
아래 core 정리는 V의 모든 q에 대해 (53.7)만 필요하다.

## 4. 희소성·codegree·유한 독립 partition

cap과 projection은 q의 포함 사건을 줄인다. COR1으로
\[
 \Pr(q\in e_p\mid\mathbf A)\le X^{-3/5}.
 \tag{53.10}
\]
서로 다른 q1,q2가 같은 residue edge에 들어가면 p가 q1−q2를 나눈다.
\(|q_1-q_2|<Y<X^2/4\)이고 p>X/2이므로 그런 p는 많아야 하나다. 따라서
\[
 \sum_p\Pr(q_1,q_2\in e_p\mid\mathbf A)\le X^{-3/5}\le X^{-1/20}.
 \tag{53.11}
\]
tuple edge에 한정한 논리가 아니라 full residue의 divisibility 논리다.

정수 \(1\le m\le\lfloor\ln b/\ln5\rfloor\)를 고정하고,
\[
 \lambda_j=5^{1-j}\ln5/C,\qquad 1\le j\le m.
 \tag{53.12}
\]
합은 \((5\ln5/(4C))(1-5^{-m})<1\). 각 p에 독립 label
j를 확률 \(\lambda_j\)로 부여하고 나머지 확률은 unused로 둔다.
이 label들은 edge law와 독립이다. 원래 n_p끼리 독립일 필요는 없다.
 \(I_j=\{p:\text{label }j\}\)는 서로소다.

q,j별 가중 Bernoulli의 합은 평균 \(\lambda_jd(q)\), 각 centered term의
절댓값은 \(X^{-3/5}\) 이하이다. FGKMT Lemma 2.2를 t=b^-2에 적용하면
\[
 \Pr\{|d_{I_j}(q)-\lambda_jd(q)|\ge b^{-2}\}
 \le2\exp\{-X^{1/5}/(2b^4)\}.
 \tag{53.13}
\]
모든 q,j에 동시에 적용할 실패율은
\[
 F_{\rm part}\le 2m\#V\exp\{-X^{1/5}/(2b^4)\}
 \le2bX^2\exp\{-X^{1/5}/(2b^4)\}<1/2.
 \tag{53.14}
\]
마지막은 실제 거대한 X를 계산하지 않고 증명한다.
\(e^{a/5}\ge a^3/750\), \(a=e^b\ge b^4/24\),
\(b^4\ge4500\cdot576\)이므로 \(X^{1/5}/(2b^4)\ge3a\).
그 결과 RHS≤2b e^-a<1/2이다.
따라서 **결정론적 label 선택 하나가 존재**한다. 이를 고정하면
\[
 |d_{I_j}(q)-5^{1-j}\ln5|\le2b^{-2}.
 \tag{53.15}
\]
\(\lambda_j\le4/5\)와 (53.7)을 사용했다. 좌변의 중심은
\(5^{1-j}\ln5\ge5\ln5/b>2/b^2\)이므로 모든 I_j는 비어 있지 않다.
label을 실제 거대 배열로 생성하는 실행기를 요구하는 존재증명이 아니다.

## 5. degree recursion과 core smallness gate

\(d_j=d_{I_j}(q)\), \(P_0(q)=1\),
\(P_j=P_{j-1}\exp(-d_j/P_{j-1})\)로 둔다.
\[
 d_j=5^{1-j}\ln5(1+\eta_j),\quad|\eta_j|\le1/b,\quad
 z_j=\ln(5^jP_j).
\]
그러면
\[
 z_j=z_{j-1}+\ln5-\ln5(1+\eta_j)e^{-z_{j-1}},\qquad
 |z_j|\le(3^j-1)/b<\xi:=3^m/b<1/10.
 \tag{53.16}
\]
증명: \(|z|\le1/10\)에서 미분의 절댓값은
\(1+(13/8)(2001/2000)(10/9)<3\)이다. \(\ln5<13/8\),
\(e^{1/10}<10/9\)와 평균값정리로
\(|z_j|\le3|z_{j-1}|+2/b\). 귀납한다.
\(m\le4\)이면 \(\xi\le81/2000<1/10\); m≥5이면
\(\xi\le(3/5)^m\le243/3125<1/10\).
로그 상계는 \(\ln5=2\sum_{n\ge0}(2/3)^{2n+1}/(2n+1)\)의 양의
부분합·기하 tail로 검산 가능하다. e^t≤1/(1−t)도 양의 급수로 따른다.

따라서 다음 **수치 parameter**가 맞는다.
\[
 r_{\rm hg}=2k,\quad A_{\rm hg}=2r_{\rm hg}m+2=4km+2,\quad
 D=2,\quad\kappa=(9/10)5^{-m},\quad\Delta=X^{-1/20}.
 \tag{53.17}
\]
실제로 \(d_j/P_{j-1}< (13/8)(2001/2000)(10/9)<2\),
\(P_j\ge(9/10)5^{-j}\ge\kappa\).
또 \(\#I_j\le X\)이므로
\(X^{-3/5}\le\Delta/\sqrt{\#I_j}\)이며 (53.11)도 만족한다.
\(A_{\rm hg}-2r_{\rm hg}m=2\)여서 1점과 **서로 다른 2점** 결론을 모두 쓸 수 있다.

유일하게 여기서 수치값을 아직 넣을 수 없는 core 조건은
\[
 \boxed{\frac{a}{20\,10^{m+2}}
 \ \ge\ \ln C_0+A_{\rm hg}\{2+\ln(1/\kappa)\}.}
 \tag{53.18}
\]
이는 원문 (4.1)과 동치인 log-scale 조건이다. C0≥1을 임의로 1로 놓거나,
큰 X이므로 자동 성립한다고 말하지 않는다.

참고로 기존 child에서 \(\ln C_0\le\sqrt a\)를 추가로 증명하면 (53.18)은
충분히 따른다. \(10^m\le b^{3/2}\),
\(A_{\rm hg}(2+\ln(1/\kappa))\le12a^{1/5}b^2\le\sqrt a\),
\(a/(2000b^{3/2})\ge2\sqrt a\)를 쓰면 된다.
마지막 두 식은 b=2000에서 각각
\(2^{600}>12\cdot2000^2\), \(2^{1000}>4000\cdot2000^2\)이고,
각 exponential/polynomial 비의 로그미분이 양수인 것으로 충분하다.
**이 참고는 C0의 실제 크기를 안다는 뜻이 아니다.**

## 6. C0 조건부 1·2점 moment와 subset의 실패율

(53.18)이 유효한 source C0에 대해 성립한다고 가정한다.
Theorem 3의 출력 support는 각 e_p의 support 또는 ∅이다. 쓰지 않은 p는 ∅로 둔다.
\[
 \rho=5^{-m},\quad\epsilon=\Delta^{1/10^{m+1}},\quad
 \alpha=(1+\epsilon)e^\xi-1,\quad\beta=(1+\epsilon)e^{2\xi}-1.
 \tag{53.19}
\]
Theorem3 (4.10)과 (53.16)으로 각 q의 uncovered probability는
\([(1-\epsilon)e^{-\xi},(1+\epsilon)e^\xi]\rho\), 서로 다른 pair의
joint probability는 같은 방식의 2ξ bounds 곱에 놓인다.

covering을 하기 전에 고정한 U⊂V, M=#U>0의 uncovered count Z_U에 대해
\[
 \frac{\mathbb E(Z_U-\rho M)^2}{(\rho M)^2}
 \le v(M):=\beta+2\alpha+\frac{1+\alpha}{\rho M}.
 \tag{53.20}
\]
증명: 첫 moment의 양측 오차는 αρM 이하이다.
ordered distinct pair를 세어
\(\mathbb EZ_U(Z_U-1)\le(1+\beta)\rho^2M(M-1)\)로 상계하고,
diagonal \(\mathbb EZ_U\le(1+\alpha)\rho M\)를 따로 남긴다.
이를 중앙값 ρM에 대한 제곱으로 전개하면 (53.20)이 나온다.
\[
 \Pr\{|Z_U-\rho M|>t\rho M\}\le\min(1,v(M)/t^2)\quad(t>0).
 \tag{53.21}
\]
사전 고정 J subsets에 동시에 필요하면 \(\min(1,\sum_Uv(\#U)/t_U^2)\).
independence나 subset들이 서로소라는 조건은 필요하지 않다.
U는 residue vector를 고정한 뒤 결정해도 되지만 **새 covering outcome에는
의존하면 안 된다**. 모든 subset을 동시에 보장하려면 그 family 크기까지
포함해야 한다. fixed-subset uniformity만으로 임의 postselection을 허용하지 않는다.

## 7. 실제 residue class로의 양측 복원

출력 nonempty e'_p에는 (53.2)의 cap을 통과한 원래 정수 n이 존재한다.
그중 하나를 고정 규칙으로 고르고 \(n'_p=n\)으로 둔다.
e'_p=∅이면 \(n'_p=0\)을 써도 된다. V의 모든 q는 p보다 큰 소수이므로
residue 0과 만나지 않는다. 따라서 **V 위에서**
\[
 e'_p=\{q\in V:q\equiv n'_p\bmod p\}
 \tag{53.22}
\]
이다. 단순 subset containment보다 강한 equality다.

원래 U0⊂V0, U=U0\E, \(M_0=\#U_0,\ M=\#U>0\)라 하자.
실제 full residue의 uncovered count Z0와 위 Z_U 사이에는
\[
 Z_0=Z_U+\eta_E,\quad0\le\eta_E\le\#(U_0\cap E).
\]
그러므로 (53.21)의 성공사건에서
\[
 \boxed{\left|\frac{Z_0}{\rho M_0}-1\right|
 \le t+\frac{\#(U_0\cap E)}{\rho M_0}.}
 \tag{53.23}
\]
covering 전에 뺀 예외를 마지막에 공짜로 복원하지 않는다.
\(M_0\ge N/\sqrt b\)이면 (53.9), ρ≥1/b에서 비용은 ≤8000/√b이다.
whole set에서는 ≤8000/b다. 이 느슨한 상계는 b≈2000에서 유용하지 않을 수 있다.
R08에서 원하는 구간 폭·성공확률·coefficient slack을 정하고 나서 cutoff를 선택해야 한다.
현재 child가 최종 covering에 충분하다고 선언하지 않는다.

## 8. 무엇이 닫혔고 무엇이 남았는가

| child | 판정 | 근거 |
|---|---|---|
| COV1-SOURCE | SOURCE_VERIFIED | §1 source·출판번호·원문 page |
| COV1-CAP | ACTUAL_INPUTS_PROJECT_EXPLICIT | (53.1)–(53.5), full edge를 보존하는 cap |
| COV1-EXCEPTIONS | ACTUAL_INPUTS_PROJECT_EXPLICIT | (53.6)–(53.9), 예외 수와 실패율 |
| COV1-PARTITION | ACTUAL_INPUTS_PROJECT_EXPLICIT | (53.10)–(53.15), nonempty disjoint sets 존재 |
| COV1-RECURRENCE | ACTUAL_INPUTS_PROJECT_EXPLICIT | (53.16)–(53.17), D·κ·A 숫자 |
| COV1-MOMENT-TRANSFER | CONDITIONAL_ON_SOURCE_C0_GATE | (53.18)–(53.21); C0를 검산하지 않음 |
| COV1-REALIZATION | PROJECT_EXPLICIT_SUPPORT_LEMMA | (53.22)–(53.23); source output 존재에 조건부 사용 |
| COV1-CORE-C0 | OPEN | §5 normalization·conditional moments·Taylor 상수 복원 필요 |
| DEP-R07 전체 | OPEN | 앞 child의 진척을 full theorem으로 승격하지 않음 |
| DEP-R08–R12 / X_cert | OPEN | post-covering 총 budget·smooth remainder·PAP·UB·계수·최종변수 |

다음은 **H1b-COV1a: FGKMT §5 C0와 induction multiplier 복원**이다.
먼저 Lemma 5.1 (5.10)–(5.11)의 정규화 1·2차 moment, 이어
(5.18)–(5.22)의 조건부 moment에서 같은 index의 independent copy 해석,
denominator lower bound와 Taylor budget을 정확히 수치화한다.
source의 symbolic O를 전사했다고 수치 증명이 되지는 않는다.
새 PDF·설치·긴 actual 계산은 지금 필요하지 않다.
계수 개선·새 record 탐색·독립 bridge 최적화는 사용자 결정대로 추후 별도 연구다.

## 9. bounded 검증 범위

별도 helper와 unit tests는 작은 유한 확률표의 cap 질량·support witness·
projection 복원, 독립 label의 유리수 expectation, ordered-pair 순간과 union bound를
검산한다. recurrence의 초등 exponential/log bounds는 유리수 enclosure를 쓴다.
전체 prime 목록, 실제 X 배열, threshold calculator를 만들지 않는다.
상수 산술과 toy PASS는 이 문서의 무한범위 proof나 core C0의 독립 형식 인증이 아니다.
