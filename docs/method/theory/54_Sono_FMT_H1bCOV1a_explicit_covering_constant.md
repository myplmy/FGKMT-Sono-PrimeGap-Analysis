# Sono/FMT H1b-COV1a: covering core의 명시적 상수 C0=100

- 작성: 2026-09-09 KST.
- 증거 수준: PROJECT FINITE ANALYTIC PROOF + bounded exact algebra checks.
- 독립 심사·Lean 인증 아님. toy 검사는 아래 모든-parameter 증명의 대체물이 아니다.
- 결론: FGKMT Theorem 3의 smallness 조건에서 **C0=100은 충분하다**.
  최소 상수라는 주장이 아니며, 원문에 이 숫자가 적혀 있다는 뜻도 아니다.
- [theory 53](53_Sono_FMT_H1bCOV1_full_residue_hypergraph_interface.md)의 실제 입력과
  합성하면 DEP-R07의 core·고정 유한 subset rate가 explicit해진다.
  동시 구간 총 예산·smooth remainder·PAP/UB·최종 계수/변수는 별도다. X_cert는 OPEN.

## 1. 선행연구·원문과 이번 증명의 차이

FGKMT, *Long gaps between primes*, JAMS 31 (2018), 65–105,
[DOI 10.1090/jams/876](https://doi.org/10.1090/jams/876),
[arXiv:1412.5029](https://arxiv.org/abs/1412.5029)를 먼저 확인했다.

| 원문 위치 | 기존 내용 | 이번에 수치화한 부분 |
|---|---|---|
| 출판 pp.76–77 / PDF pp.12–13, Theorem 3 (4.1)–(4.11) | 유한 parameter 정리; C0 존재 | 같은 가정·같은 결론에서 충분한 C0=100 |
| pp.83–85 / PDF pp.19–21, (5.7)–(5.11), Lemma 5.1 | reweighting 정규화·1·2차 moment | 정규화 제곱오차 4t^100, bad 사건 4t^40 |
| pp.87–89 / PDF pp.23–25, (5.18)–(5.22) | 조건부 moment·codegree | 중심 제곱오차 12t^98; 같은 index도 product law |
| pp.85–87 / PDF pp.21–23, (5.14)–(5.17) | 조건부 곱·Taylor·분모 전달 | good-event 로그오차 3t^11, 최종 상대오차 8t^11 |

기존 로컬 PDF는 NATIVE_TEXT다. 위 9개 page를 text로 읽고 원문 전체 page에서
지수·분모·합·양화를 대조했다. OCR, 새 자료 다운로드, 패키지 설치는 하지 않았다.
저자 primary source와 arXiv를 표적 확인했지만 바로 대입할 숫자 C0는 확인하지 못했다.
이것은 전 세계 문헌에 그런 값이 없다는 주장이나 novelty 판정이 아니다.

증명 구조는 기존 §5를 재사용한다. 단 원문 (5.8)의 정규화 허용오차
t^(100/3) 대신 **t^30**을 쓴다. 따라서 인쇄 proof의 미지 O에 임의 숫자를
대입하는 작업이 아니라, 같은 정리 결론을 얻는 **정량 재증명**이다.
원래 random edge들의 독립성은 가정하지 않는다.

## 2. 정확한 정리·귀납 범위

D,r,A≥1, 0<κ≤1/2, 정수 m≥0, δ>0이고
\[
 \delta\le\left\{\frac{\kappa^A}{100e^{AD}}\right\}^{10^{m+2}}. \tag{54.1}
\]
유한 V와 서로소·비어 있지 않은 유한 I_j가 주어졌다고 하자. 원래 edge e_i의
marginal law만 사용하며 다음 가정을 요구한다.
\[
 |e_i|\le r,\quad
 \Pr(v\in e_i)\le\frac{\delta}{\sqrt{|I_j|}},\quad
 \sum_{i\in I_j}\Pr(v,w\in e_i)\le\delta\quad(v\ne w). \tag{54.2}
\]
\[
 d_j(v)=\sum_{i\in I_j}\Pr(v\in e_i),\quad P_0(v)=1,\quad
 P_j(v)=P_{j-1}(v)e^{-d_j(v)/P_{j-1}(v)},\quad
 d_j(v)\le DP_{j-1}(v),\quad P_j(v)\ge\kappa. \tag{54.3}
\]
모든 |e_i| 제약은 확률 1의 support 제약이다.
P_j(S)=∏_(v∈S)P_j(v)이며 빈 곱은 1이다.

**정리.** 각 e'_i의 support가 support(e_i)∪{∅} 안에 있고, 모든
0≤J≤m 및 |E|≤A−2rJ인 고정 E⊂V에 대해
\[
 \left|\frac{\Pr(E\text{가 }1,\ldots,J\text{라운드 뒤 남음})}{P_J(E)}-1\right|
 \le\delta^{1/10^{J+1}} \tag{54.4}
\]
인 공동확률법칙을 구성할 수 있다.
이것은 같은 하나의 법칙에 대한 모든 E의 moment 명제이지,
모든 E가 동시에 남는다는 사건 명제가 아니다.

m=0이면 정확한 등식이다. 귀납 시 (54.1)의 밑은 1보다 작으므로 같은 δ는
m−1의 smallness 조건도 만족한다. 이전 공동법칙을 보존하며 마지막 round만
그 위에 조건부로 추가한다. A≤2rm이면 마지막 결론에 비어 있지 않은 E는 없으므로
마지막 e'_i=∅로 충분하다. 이후 A>2rm, m≥1을 가정한다.
이때 r<A와 2r<A이며 모든 필요한 집합은 이전 test-set capacity 안에 있다.

다음 기호로 지수를 통일한다.
\[
 t=\delta^{1/10^{m+2}},\quad h=t^{100}=\delta^{1/10^m},\quad
 \delta\le t^{1000},\quad0<t\le1/100. \tag{54.5}
\]
(54.1)에서 κ^(−A)e^(AD)≤1/(100t)이다. 따라서
\[
 A,D,r,\kappa^{-A},e^{AD}\le t^{-1};
 \quad \kappa^{-r},\kappa^{-2r}\le t^{-1}. \tag{54.6}
\]
A≤AD≤e^(AD), D≤AD를 썼다. 개별 인자를 이렇게 느슨하게 상계하므로
뒤의 t 지수 손실은 보수적이다. κ^(−1)≤t^(−1)도 사용한다.

W를 이전 round들 뒤의 남은 집합, P=P_(m−1)로 두면
\[
 \Pr(U\subset W)=(1+\theta_U)P(U),\quad|\theta_U|\le h
 \quad(|U|\le A-2r(m-1)). \tag{54.7}
\]
κ≤P(v)≤1. 마지막 round의 N=|I_m|≥1, marginal을 μ_i(S)=Pr(e_i=S)라 쓴다.

## 3. 정규화와 작은 분모의 처리

\[
 X_i(W)=\sum_S\mu_i(S)\frac{1_{S\subset W}}{P(S)}. \tag{54.8}
\]
(54.7)로 |EX_i−1|≤h. 두 집합 S,T를 **μ_i에서 독립으로 뽑은 복사본**으로
사용하여 제곱을 전개하면
\[
 EX_i^2=\sum_{S,T}\mu_i(S)\mu_i(T)
       \frac{\Pr(S\cup T\subset W)}{P(S)P(T)}.
\]
|S∪T|≤2r<A−2r(m−1)이므로 (54.7)을 적용할 수 있다.
P(S∪T)/(P(S)P(T))=1/P(S∩T)이고,
\[
 1\le 1/P(S\cap T)\le1+\kappa^{-r}1_{\{S\cap T\ne\varnothing\}},
 \quad\Pr_{\mu_i\otimes\mu_i}(S\cap T\ne\varnothing)
 \le r\delta/\sqrt N.
\]
따라서
\[
 EX_i^2\le(1+h)(1+t^{998}),\quad
 E(X_i-1)^2\le3t^{100}+2t^{998}\le4t^{100}. \tag{54.9}
\]
우리는
\[
 F_i=\{|X_i-1|\le t^{30}\},\quad \Pr(F_i^c)\le4t^{40} \tag{54.10}
\]
를 택한다. Fi 위에서 Xi≥1−t^30≥1/2이다. Fi 밖에서는 e'_i=∅로 하고,
Fi 안에서는
\[
 \Pr(e'_i=S\mid W)=\frac{\mu_i(S)1_{S\subset W}}{X_i(W)P(S)}. \tag{54.11}
\]
합이 정확히 1이다. Xi=0인 경우에는 **나눗셈을 수행하지 않는다**.
마지막 round의 e'_i들을 W 조건부로 독립 생성한다.
유한 V·I_m이므로 이 product probability law는 존재한다.
선행 round의 공동법칙과 원래 support 조건은 보존된다.

## 4. 고정 E에 대한 조건부 degree의 두 moment

비어 있지 않은 E⊂V, s=|E|≤A−2rm, v∈E를 고정한다.
사건 \(\mathcal E=\{E\subset W\}\)는
\[
 \Pr(\mathcal E)\ge(1-h)P(E)\ge\tfrac12\kappa^s>0. \tag{54.12}
\]
정규화 이전 질량과 그 중심을
\[
 T_i(v,W)=\sum_{S\ni v}\mu_i(S)\frac{1_{S\subset W}}{P(S)},\quad
 H_v=\sum_iT_i,\quad h_v=d_m(v)/P(v)\le D \tag{54.13}
\]
로 둔다. (54.7)의 조건부 비는
\[
 \left|\frac{1+\theta_{E\cup S}}{1+\theta_E}-1\right|
 \le\frac{2h}{1-h}\le3h. \tag{54.14}
\]
E∪S∪T에 대해서도 같다. s+2r≤A−2r(m−1)이 중요하다.

### 4.1 첫 moment

중심식 P(E∪S)/(P(S)P(E))=1/P(S∩E)에서 v 하나의 기여는 1/P(v).
나머지 중복에 대한 비용은 codegree를 써서
\[
 0\le\sum_{i,S\ni v}\mu_i(S)
   \frac{1}{P(v)}
   \left\{\frac1{P((S\cap E)\setminus\{v\})}-1\right\}
 \le A\kappa^{-r}\delta/P(v)\le t^{997}.
\]
여기에 (54.14)를 곱하면
\[
 |E(H_v\mid\mathcal E)-h_v|
 \le3t^{100}D+2t^{997}\le4t^{99}. \tag{54.15}
\]

### 4.2 둘째 moment와 동일 index

H_v²의 전개는 모든 i,i'에 대해 μ_i(S)μ_i'(T)를 사용한다.
**i=i'이어도 S,T는 독립 복사본의 product law다.**
같은 실제 edge를 두 번 사용하는 joint event로 바꾸면 다른 식이 된다.
원래 서로 다른 e_i들의 독립성도 이 전개에는 필요 없다.

v∈S∩T∩E일 때
\[
 R(S,T,E;v)=
 \frac{P(v)^2P(S\cup T\cup E)}{P(S)P(T)P(E)} \tag{54.16}
\]
는, v를 제외한 pairwise intersection이 모두 비면 1이다.
일반적으로 1≤R≤κ^(−2r)이고
\[
 R-1\le\kappa^{-2r}\left\{
 \sum_{w\in E\setminus\{v\}}(1_{w\in S}+1_{w\in T})
 +\sum_{w\in S\setminus\{v\}}1_{w\in T}\right\}. \tag{54.17}
\]
증명: 각 w≠v에서 세 집합 중 출현횟수가 ℓ이면 P(w)^(−(ℓ−1))
인자가 생긴다. 총 지수는 |S|+|T|−2 이하이다.
**삼중 중복은 제곱 인자**를 만들며 한 번만 나누지 않는다.

μ_i(S)μ_i'(T)1_(v∈S∩T)로 가중하여 합하면 첫 두 indicator 합은 각각
d_m(v)Aδ 이하이고, 마지막 합은 d_m(v)rδ 이하이다.
예컨대 마지막은 각 S에 대해
Σ_(w∈S\{v})Σ_i'Pr_(μ_i')(v,w∈T)≤rδ로 얻는다.
따라서 h_v²를 뺀 비조건부 중심 합의 추가비용은
\[
 0\le B_2-h_v^2\le3AD\kappa^{-2r}\kappa^{-2}\delta
 \le3t^{995}. \tag{54.18}
\]
B2는 (54.16)의 합을 P(v)²로 나눈 양이다. (54.14)를 적용하면
\[
 |E(H_v^2\mid\mathcal E)-h_v^2|
 \le3t^{100}D^2+6t^{995}\le4t^{98}. \tag{54.19}
\]
(54.15)와 제곱을 전개하여
\[
 E((H_v-h_v)^2\mid\mathcal E)
 \le4t^{98}+2D\cdot4t^{99}\le12t^{98},\quad
 \Pr(|H_v-h_v|>t^{30}\mid\mathcal E)\le12t^{38}. \tag{54.20}
\]

## 5. 정규화된 실제 degree로의 전달

조건부 실제 degree는
\[
 L_v=\sum_i1_{F_i}\,T_i/X_i.
\]
Fi 밖의 항은 0으로 정의하며 0/0 기호를 평가하지 않는다.
Fi 안에서는 |1/X_i−1|≤2t^30이므로 점별로
\[
 |L_v-H_v|\le R_v:=
 \sum_i(1_{F_i^c}+2t^{30})T_i. \tag{54.21}
\]
각 i의 Fi를 **그 합 안에 그대로 유지**한다.
T_i≤κ^(−r)μ_i(v), d_m(v)≤D로
\[
 ER_v\le\kappa^{-r}d_m(v)(4t^{40}+2t^{30})
 \le3t^{28}.
\]
조건부 사건 확률로 나눌 때 (54.12)의 비용을 버리지 않는다.
\[
 E(R_v\mid\mathcal E)\le6t^{27},\quad
 \Pr(R_v>t^{12}\mid\mathcal E)\le6t^{15}. \tag{54.22}
\]
(54.20), (54.22)의 union bound를 쓰면 v마다 실패율≤7t^15,
s≤A≤t^(−1)개의 v에 대해 동시 실패율≤7t^14이다.
성공사건 \(\mathcal G_E\)에서는
\[
 \left|\sum_{v\in E}L_v-\mu_E\right|\le2t^{11},\qquad
 \mu_E=\sum_{v\in E}h_v\le AD. \tag{54.23}
\]
Fi들이 서로 독립이라고 가정하지 않는다.

## 6. Taylor·조건부 product와 최종 귀납 오차

W⊃E에서 λ_i(W)=Pr(E∩e'_i≠∅|W)를 둔다.
Fi 밖이면 λ_i=0이며 언제나
\[
 0\le\lambda_i\le2A\kappa^{-r}\delta/\sqrt N
 \le2t^{998}/\sqrt N<1/2,\quad
 \sum_i\lambda_i^2\le4t^{1996}. \tag{54.24}
\]
W 조건부 독립성으로 Y(W)=∏_i(1−λ_i).
원래 e_i의 독립성이 아니라 새로 구성한 e'_i들의 조건부 독립성이다.
유한 inclusion-exclusion의 첫 두 항과 (54.2)로
\[
 0\le\sum_{v\in E}L_v-\sum_i\lambda_i
 \le2A^2\kappa^{-r}\delta\le2t^{997}. \tag{54.25}
\]
0≤λ≤1/2에서 양의 급수로
0≤−ln(1−λ)−λ≤λ². 따라서
\[
 |\ln Y+\sum_vL_v|\le2t^{997}+4t^{1996}\le3t^{997}.
\]
\(\mathcal G_E\) 위에서는
\[
 |\ln Y+\mu_E|\le3t^{11},\quad
 |Y/Z-1|\le6t^{11},\qquad Z=e^{-\mu_E}\ge e^{-AD}\ge t. \tag{54.26}
\]
여기서 e^u−1≤2u (0≤u≤1/2)를 사용한다.
나쁜 사건에서는 0≤Y≤1이므로 |Y/Z−1|≤1/Z≤t^(−1).
그 확률≤7t^14를 함께 곱해야 하며 공짜로 제거하지 않는다.
\[
 \left|\frac{E(Y\mid\mathcal E)}Z-1\right|
 \le6t^{11}+7t^{13}\le7t^{11}. \tag{54.27}
\]
마지막으로 (54.7)의 E 사건 오차까지 곱하면
\[
 \left|\frac{\Pr(E\text{가 마지막 뒤에도 남음})}{P_m(E)}-1\right|
 \le t^{100}+(1+t^{100})7t^{11}
 \le8t^{11}\le t^{10}
 =\delta^{1/10^{m+1}}. \tag{54.28}
\]
empty E는 정확히 1이다. 이전 J<m의 결론은 법칙을 바꾸지 않아 그대로다.
동일 구성은 E 선택에 의존하지 않으므로 모든 허용 E의 moment 명제를 만족한다.
이로써 모든 m에 공통인 **충분한 C0=100**의 증명을 마친다.

## 7. 숨은 수치 없는 scalar audit

모든 아래 다항식은 t에 대해 증가하므로 0<t≤1/100 범위의 검사는
유리수 t=1/100에서 충분하다. 정리의 연속 parameter를 표본검사만으로
대체하는 것이 아니라, 단조성으로 전체 범위를 먼저 환원했다.

| 사용처 | 정확한 충분 부등식 |
|---|---|
| 조건부 비·분모 | t^100≤1/3, t^30≤1/2 |
| normalization / 첫 moment | 2t^898≤1 |
| 둘째 moment | 6t^897≤1 |
| bad-X 전달 | 4t^10≤1 |
| v별 union | 12t^23≤1 |
| Taylor 합 | 4t^999≤1, 3t^986≤1 |
| exponential | 3t^11≤1/2 |
| conditional relative | 7t²≤1 |
| 마지막 귀납 | t^89+7t^100≤1, 8t≤1 |

조건부 비, Markov, Taylor, product-law 합은 bounded exact toy로도
독립적인 유한 전개와 비교한다. 이 toy에 거대한 소수 입력이나 threshold 검색은 없다.

## 8. 실제 COV1 입력에 대입

theory 53의 a=ln X, b=ln a, k=floor((ln(X/2))^(1/5))와
\[
 r_{\rm hg}=2k,\ A_{\rm hg}=4km+2,\ D=2,
 \kappa=(9/10)5^{-m},\ \Delta=X^{-1/20}
\]
를 그대로 사용한다. 그 문서 (53.18)의 조건은 이제
\[
 \frac{a}{20\,10^{m+2}}\ge\ln100+A_{\rm hg}\{2+\ln(1/\kappa)\}. \tag{54.29}
\]
기존 child X≥2exp(10^1000), b>2000에서 ln100<5<√a.
ln100<5는 e^5의 0차부터 6차까지 양의 급수 부분합이 100보다 큰 것으로
유리수 검산할 수 있다. theory 53 §5는 나머지 두 조건
\[
 A_{\rm hg}\{2+\ln(1/\kappa)\}\le\sqrt a,\qquad
 a/(20\,10^{m+2})\ge2\sqrt a
\]
를 이미 증명했다. 따라서 (54.29)가 모든 허용 m에서 성립한다.
기존 child cutoff를 더 키울 필요 없이 **core smallness 입력이 닫힌다**.
큰 X를 실제로 표현하거나 그 이하 소수를 계산한 것이 아니다.

theory 53 (53.19)–(53.23)의 1·2점 moment, 고정 유한 family의 실패율,
실제 residue support equality와 예외복원 비용은 이제 미지 C0에 조건부가 아니다.
다만 거기에 남은 **명시적** 비용이 목적에 충분히 작은지는 별도 문제다.
예를 들어 8000/√b의 복원 상계는 b≈2302에서 작지 않다.
R08에서 구간폭·family 크기·허용오차에 맞는 공통 cutoff와 성공확률을 정해야 한다.

## 9. 상태·다음 단계

| 대상 | 상태 |
|---|---|
| C0-NORM / CONDITIONAL / TAYLOR / INDUCTION | PROJECT_EXPLICIT, 이 문서 §§2–7 |
| core Theorem 3 C0 | C0=100 SUFFICIENT, 최소성·독립 인증 미주장 |
| actual smallness gate | PROJECT_EXPLICIT, §8·theory53 |
| DEP-R07 actual core와 고정 유한 subset rate | ACTUAL_INPUTS_PROJECT_EXPLICIT |
| FMT 일반 wrapper 전체 / 모든 최종 구간의 동시 성공 | 여기서 승격하지 않음 |
| DEP-R08–R12, broad SIV-07/08/09, X_cert | OPEN / HARD_BLOCKER 유지 |

다음 권장은 **H1b-COV2 / DEP-R08**이다. 먼저 Sono/FMT가 실제로 필요한
구간 family와 width·floor·rounding을 원문에서 대조한 뒤, post-covering
오차·예외복원·smooth remainder를 총 예산에 넣는다.
이어서 PAP, two-prime UB, 같은 Sono 계수 보존, 최종변수 전환을 진행한다.
기존 COV1 문서·contract의 당시 OPEN 표시는 역사적 snapshot으로 보존하고,
현재 상태는 이 successor와 parent overlay를 따른다.
