# Sono/FMT H1b-COR1: finite correlation·조건부 희소성·good-P 확률

- 작성: 2026-09-09 KST
- 증거 수준: PROJECT FINITE ANALYTIC PROOF + bounded exact toy 검산; 독립 심사·Lean 인증 아님
- 범위: theory 47–48의 실제 W-filtered, fixed-X construction
- 상태: DEP-R01·DEP-R02·DEP-R04의 actual child를 명시화; 전체 X_cert는 OPEN
- 계약: [successor JSON](data/Sono_FMT_H1bCOR1_finite_correlation_v1.json)
- helper: ../../../source/h1bcor1_finite_correlation.py
- 검토: [review 55](../../review/55_20260909_H1bCOR1_finite_correlation_타당성검토.md)

## 1. 선행증명과 정확한 재사용 범위

| 원천 | 정확한 위치 | 재사용 / 이번 추가 |
|---|---|---|
| [FGKMT, arXiv:1412.5029](https://arxiv.org/abs/1412.5029), DOI [10.1090/jams/876](https://doi.org/10.1090/jams/876) | 출판 p.91/PDF p.27 Lemma 6.1, p.93/PDF p.29 Lemma 6.3 | prime-by-prime correlation·독립 copy second moment 증명을 재사용하고 숨은 O 상수·충돌 비용을 수치화 |
| [FMT, arXiv:1511.04468](https://arxiv.org/abs/1511.04468) | pp.13–14, Lemmas 6.1–6.2, (6.13)–(6.17) | S에서 B0 제거, good P와 조건부 분포; 구판 FGKMT Lemmas 5.1/5.3 인용은 출판 6.1/6.3에 대응 |
| [Rosser–Schoenfeld 1962](https://doi.org/10.1215/ijm/1255631807) | 인쇄 p.70/PDF p.7, Theorem 7 (3.25)–(3.26) | Mertens 곱의 양측 명시식. 이번에는 sigma **하계**에 사용 |
| [theory 35](35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md) §7 | v,z의 유효범위 | v≥285, z>v, log v·log z>300 |
| [theory 47](47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md) §§2–3,5,8 | 같은 source B·고정-X 확률 입력 | support, max atom, dyadic P 개수 |
| [theory 48](48_Sono_FMT_H1bDEP_actual_dependency_map.md) §§5–6 | actual tuple·크기·잔여 12항목 | 임의 다항식 크기 대신 실제 절댓값≤X², codegree geometry |

새 증명이 필요한지 먼저 위 source를 검토했다. 필요한 proof 구조는 이미 존재한다.
다만 이 실제 입력의 숫자 상수와 cutoff를 그대로 제공하는 drop-in 결과는 확인하지 못해
그 구조 안의 초등 부등식과 확률 오차를 직접 명시화했다. 전 세계 문헌 부재·novelty 주장은 아니다.
새 source 다운로드, 설치, prime sweep은 없었다.

## 2. 변수와 실제 입력의 고정

X는 **보조 sieve 크기**다. 최종 maximal-gap 변수나 X_cert와 동일시하지 않는다.
모든 로그는 자연로그이며, 이번 문서에서는 혼동을 피하려고
\[
 a=\ln X,\quad L=\ln(X/2),\quad b=\ln a,\quad
 k=\lfloor L^{1/5}\rfloor\ge10^{200}
 \tag{49.1}
\]
로 둔다. 여기 b는 로그 보조변수이며 theory 47의 phi(B)/B가 아니다.
\[
 v=a^{20},\quad z=X^{\ln b/(4b)},\quad
 S=\{s\text{ prime}:v<s\le z,\ s\ne B_0\},\quad
 \sigma=\prod_{s\in S}(1-1/s).
 \tag{49.2}
\]
a^20은 20제곱이지 20회 반복로그가 아니다. 실제 충분조건
\[
 X\ge 2\exp(10^{1000})
 \tag{49.3}
\]
은 선행 child cutoff 그대로이며 **최종 threshold를 계산한 것이 아니다**.

P'=prime∩(X/2,X]에서 B0를 뺀 집합, Q'=prime∩(X,Y]에서 B0를 뺀 집합을 사용한다.
이미 증명한 실제 입력은
\[
 Y<Xa<X^2/4,\quad
 2k^2X\le Y,\quad
 2k\le a,\quad k^2\le a,\quad \ln a<6\ln k\le6k .
 \tag{49.4}
\]
서로 다른 h_i는 [1,2k²]에 있고 preliminary 변수 \(\widetilde n_p\)의 support는
[-Y,Y], 모든 atom의 확률은 X^{-3/4} 이하다.
각 s의 residue A_s는 서로 독립·균등하고 모든 preliminary 변수와 독립이다.
서로 다른 p의 preliminary 변수 간 독립성은 이번 선형기댓값·Markov에 필요하지 않다.
필요한 같은 p의 두 copy는 별도로 독립 생성한다.

\(\mathscr S(\mathbf A)\)는 모든 s에서 A_s를 피하는 정수 집합이다.
다음에서는 weight total mass Z_p와 혼동하지 않도록 FMT의 X_p를 D_p로 표기한다.

## 3. R01 — 독립 residue의 finite correlation

### 명제 49.1

a=ln X≥2, 1≤t≤a인 정수 t, 서로 다른 정수 n_1,…,n_t로 |n_i|≤X²라 하자.
S는 s>a^20인 소수들의 임의 유한 부분집합이어도 된다. 그러면
\[
 \boxed{\left|
 \frac{\Pr(n_1,\ldots,n_t\in\mathscr S(\mathbf A))}{\sigma^t}-1
 \right|\le2a^{-17}\le a^{-16}.}
 \tag{49.5}
\]
따라서 기존 \(O((\log X)^{-16})\)의 uniform multiplier는 **1**로 둘 수 있다.
이는 stated distinct-point 범위에 관한 project finite proof다.

### 증명

\(\nu_s=\#\{n_i\bmod s\}\), \(V=a^{20}\)라 하자.
독립·균등 선택으로 생존확률은 정확히 \(\prod_s(1-\nu_s/s)\)이다.
V≥2t이므로 모든 인수가 양수이고
\[
 \frac{\Pr(\cdots)}{\sigma^t}
 = B C,\quad
 B=\prod_s\frac{1-t/s}{(1-1/s)^t},\quad
 C=\prod_s\left(1+\frac{t-\nu_s}{s-t}\right).
 \tag{49.6}
\]
Bernoulli 부등식에서 B≤1. 로그의 급수와 t/s≤1/2를 사용하면
\[
 0\le-\ln B
 =\sum_s\sum_{m\ge2}\frac{t^m-t}{m s^m}
 \le t^2\sum_s s^{-2}
 \le\frac{t^2}{V-1}\le 2a^{-18}.
 \tag{49.7}
\]
중간 tail은 소수합을 정수합으로 넓힌 뒤
\(\sum_{j>V}j^{-2}\le1/\lfloor V\rfloor\le1/(V-1)\)로 얻는다.

같은 residue에 m개 점이 모일 때 m−1≤m(m−1)/2이므로
\[
 t-\nu_s\le \sum_{i<j}1_{s\mid n_i-n_j}.
\]
서로 다른 두 점의 차이는 0이 아니고 절댓값≤2X²다.
그 차이를 나누는 V보다 큰 **서로 다른** 소수는
\((\ln2+2a)/\ln V\)개 이하이다. 따라서
\[
 0\le\ln C
 \le\frac{\binom t2(\ln2+2a)}{(V-t)\ln V}
 \le\frac{3}{20\ln a}a^{-17}
 <a^{-17}.
 \tag{49.8}
\]
\(\ln2>1/2,\ \ln2+2a\le3a,\ V-t\ge V/2\)를 사용했다.
(49.7)의 2a^{-18}도 a^{-17} 이하다. 따라서
\[
 |\ln(BC)|\le a^{-17}=:\delta<1/2.
\]
양의 exponential series와 geometric series를 비교하면
\(e^\delta-1\le\delta/(1-\delta)\le2\delta\).
또 \(1-e^{-\delta}\le\delta\)이므로 (49.5)가 따른다. □

빈 S에서는 양변 ratio=1이며 증명이 그대로 성립한다. 같은 정수를 여러 번 적은 경우에는
이 명제를 적용하지 않는다. second moment에서 그러한 충돌은 별도 비용으로 센다.

## 4. R02 — sigma 하계와 조건부 분모

Rosser–Schoenfeld Theorem 7의 P(t)=prod_{prime≤t}(1−1/p)에 대해
\[
 \frac{e^{-\gamma}}{\ln t}\left(1-\frac1{2\ln^2t}\right)<P(t)
 \quad(t\ge285),\qquad
 P(t)<\frac{e^{-\gamma}}{\ln t}\left(1+\frac1{2\ln^2t}\right)
 \quad(t>1).
\]
B0 factor를 빼면 곱이 **커지므로**, 하계에서는 추가 손실이 없다.
theory 35 §7의 log v,log z>300을 사용하여
\[
 \sigma\ge\frac{P(z)}{P(v)}
 >\frac{\ln v}{\ln z}
    \frac{1-1/(2\ln^2z)}{1+1/(2\ln^2v)}
 >\frac12\frac{\ln v}{\ln z}
 =\frac{40b^2}{a\ln b}>\frac1a.
 \tag{49.9}
\]
마지막에는 b>15, ln b<b를 썼다. 실제의 \(\sigma\le1\)도 보존한다.
기존 theory 35의 sigma*y **상계**를 거꾸로 쓴 것이 아니다.

(49.4)와 k³≥600에서
\[
 k\ln a\le6k^2\le a/100,\qquad
 \boxed{\sigma^{-k}\le X^{1/100},\quad \sigma^{-2k}\le X^{1/50}.}
 \tag{49.10}
\]

\[
 D_p(\mathbf A)=
 \Pr(\widetilde n_p+h_i p\in\mathscr S(\mathbf A)\ (1\le i\le k)\mid\mathbf A),
 \quad
 P(\mathbf A)=\{p\in P':|D_p/\sigma^k-1|\le a^{-3}\}.
 \tag{49.11}
\]
p가 good이면 \(D_p\ge(1-a^{-3})\sigma^k\ge\sigma^k/2>0\).
FMT와 같이 good p에서 survival로 조건을 걸어 n_p를 고르고, bad p에서는 n_p=0으로 둔다.
good p에 대해
\[
 \Pr(n_p=n\mid\mathbf A)
 =\frac{1_{\{n+h_i p\in\mathscr S\ \forall i\}}\Pr(\widetilde n_p=n)}
        {D_p(\mathbf A)}
 \le2X^{-3/4+1/100}=\boxed{2X^{-37/50}}.
 \tag{49.12}
\]
원래의 max-atom X^{-3/4}를 조건부 분포에서도 그대로 쓴다고 주장하지 않는다.

q∈Q'와 good p를 고정하면 q≡n_p(mod p)는 n_p=q−hp인 정수 h의 합이다.
|n_p|≤Y, q≤Y, p>X/2에서 |h|<4Y/X.
가능한 h는 \(8Y/X+1\le9a\)개 이하이다. 따라서
\[
 \Pr(q\equiv n_p\pmod p\mid\mathbf A)
 \le18aX^{-37/50}\le\boxed{X^{-3/5}}.
 \tag{49.13}
\]
마지막 흡수는 a≥1000에서 충분하다. 실제로 ln a≤a/100이고 ln18<3이므로
\(\ln(18a)\le3+a/100\le7a/50\).
ln a≤a/100은 a=1000에서 ln1000<10 및 미분의 부호로 전 범위에 성립한다.

bad p에서는 n_p=0이다. q는 p보다 큰 소수이므로 q≡0(mod p)가 불가능해
그 확률은 0이다. 따라서 (49.13)은 **모든 residue vector**와 모든 p에서 유효하다.
조건부 분포의 결합은 필요하면 finite product로 독립 구성할 수 있다.

### 실제 small-codegree

\(e_p=\{n_p+h_ip:i\}\cap Q'\cap\mathscr S(\mathbf A)\)로 둔다.
서로 다른 q1,q2∈Q'가 같은 e_p에 들려면 p|(q1−q2)이다.
|q1−q2|<Y<X²/4인데 서로 다른 p1,p2>X/2의 곱은 X²/4보다 크다.
따라서 그런 p는 최대 하나이고
\[
 \boxed{\sum_{p\in P'}\Pr(q_1,q_2\in e_p\mid\mathbf A)
 \le X^{-3/5}\le X^{-1/20}.}
 \tag{49.14}
\]
theory 48의 conditional geometry에 이제 실제 희소성 입력을 공급했다.
단, **전체 hypergraph theorem의 모든 가정·subset 결론·failure rate를 닫은 것은 아니다**.

## 5. R04 — good P의 수치 failure rate

p∈P' 하나를 고정하고 \(U_p=D_p/\sigma^k,\ \epsilon=2a^{-17}\)라 하자.
각 n에 대한 k점은 서로 다르고 절댓값≤2Y<X²다.
(49.5)를 먼저 residue vector에 적용하고 n에 관해 평균하여
\[
 |\mathbb E U_p-1|\le\epsilon .
 \tag{49.15}
\]
이 평균을 정확히 1로 바꾸지 않는다.

독립 copy N1,N2를 같은 preliminary 분포에서 고른다.
어떤 i,j에서 N1+h_i p=N2+h_j p가 되는 사건을 C_col이라 하면,
N1을 고정한 뒤 각 가능한 N2 atom을 세어
\[
 \Pr(C_{\rm col})\le k^2 X^{-3/4}.
 \tag{49.16}
\]
충돌이 없으면 2k개의 서로 다른 점에 (49.5)를 적용하고,
충돌이 있으면 생존확률을 1로 상계한다. 그러므로
\[
 \mathbb E U_p^2
 \le1+\epsilon+k^2X^{-3/4}\sigma^{-2k}
 \le1+\epsilon+k^2X^{-73/100}
 \le1+\epsilon+a^{-17}.
 \tag{49.17}
\]
마지막에는 k²≤a와 \(18\ln a\le18a/100<73a/100\)를 사용했다.
즉 충돌을 무시하거나 distinct-point 명제를 잘못 적용한 것이 아니다.

(49.15)–(49.17)을 합치면
\[
 \boxed{\mathbb E(U_p-1)^2\le3\epsilon+a^{-17}=7a^{-17}} .
 \tag{49.18}
\]
제곱에 Markov를 적용하여
\[
 \boxed{\Pr(p\notin P(\mathbf A))\le7a^{-11}} .
 \tag{49.19}
\]
각 p 사이의 독립성은 필요하지 않다. 선형기댓값과 Markov로
\[
 \mathbb E\,\#(P'\setminus P(\mathbf A))\le7|P'|a^{-11},\quad
 \Pr\bigl(\#(P'\setminus P(\mathbf A))>|P'|a^{-3}\bigr)\le7a^{-8}.
 \tag{49.20}
\]
|P'|=0이면 bad 개수도 항상 0으로 따로 해석한다.
theory 47 (47.13)에서 |P'|≤X/a이므로
\[
 \boxed{\Pr\bigl(\#(P'\setminus P(\mathbf A))>X/a^4\bigr)\le7a^{-8}.}
 \tag{49.21}
\]
또 \(\mathbb E|P(\mathbf A)|\ge(1-7a^{-11})|P'|\).
이는 FMT Lemma 6.2/출판 FGKMT Lemma 6.3의 필요한 actual failure rate를
**uniform multiplier 7**로 공급하며 같은 child cutoff를 사용한다.

## 6. 잔여 의무·이력 보존

theory 48은 당시 12개 OPEN의 의존지도이며 소급 수정하지 않는다.
새 successor는 그중 R01/R02/R04만 PROJECT_EXPLICIT로 덮어 읽는다.
남은 수는 **9개 work package**, 여전히 6개 연구 묶음이다.

| 묶음 | 남은 의무 | 이번 결과와 차이 |
|---|---|---|
| 확률 입력 | R03 local count·finite partition, R05 off-tuple 예산, R06 main-degree moment | good-P 실패만 작아도 전체 q의 covering degree가 고르다는 결론은 안 됨 |
| covering | R07 full hypergraph, R08 simultaneous covering·smooth remainder | small-codegree 하나만 닫혔음 |
| 소수 분포 | R09 numerical PAP | selected identity Hypothesis와 다른 의무 |
| upper-bound sieve | R10 uniform two-prime UB | determinant·B0까지 균일한 수치식 필요 |
| 최종 오차 | R11 공동 확률·같은 2e-17 계수 | 개별 오차를 한 번에 합쳐야 함 |
| 변수 이동 | R12 보조 X→모든 큰 최종 Z | endpoint/primorial/log·arbitrary-Z 포함 필요 |

12→9는 **75%가 남았다거나 25%를 끝냈다는 시간·난이도 비율이 아니다**.
추후 분해·재감사에 따라 work package 수가 달라질 수 있다.
broad SIV-07/08/09는 HARD_BLOCKER, X_cert는 OPEN, calculator는 미작성이다.
기존 finite \(X_{\rm emp}(10^{20})=3,814,280\)과 이 child cutoff를 비교해
“얼마나 많은 소수를 더 계산하면 된다”는 방식의 시간을 산출할 수 없다.

## 7. 검산과 다음 순서

helper는 작은 residue 공간을 직접 전수하여 곱 공식과 독립 대조하고,
같은 toy에서 조건부 분모·두 copy의 충돌·제곱 평균을 exact Fraction으로 확인한다.
실제 k에 대해서는 O(1)개 log-scale 부등식만 확인한다.
k차원 배열, exp(10^1000), prime 데이터는 만들지 않는다.
이 검산은 전 범위 해석적 증명이나 독립 formal proof의 대체가 아니다.

다음은 **H1b-COR2: R05 off-tuple Markov/union budget**을 먼저 감사한다.
그 뒤 R03 local-count/finite partition과 R06 main-degree의 공유 입력을 연결한다.
새 자료·설치 또는 장시간 계산이 필수라면 active goal에 따라 보고 후 작업을 멈춘다.
현재 사용자 실행·추가 패키지·Lean 설치는 불필요하다. 별도 수행절차 필요없음.

### 로컬 검증 결과

- 전용 24/24 PASS (0.075초), 표적 137/137 PASS (0.583초).
- 전체 527/527 PASS (59.701초, exit 0), 승인된 정상 로컬 권한의 toy/회귀만 실행.
- 5개 Python 파일 py_compile, 19파일 UTF-8/4 JSON/157 local links/7개 source·선행 hash 검사 issue 0.
- 위 검사는 정확한 유한 fixture와 문서/코드 오류 방지다. 해석적 증명 전체의 독립 심사나 Lean 인증이 아니다.
