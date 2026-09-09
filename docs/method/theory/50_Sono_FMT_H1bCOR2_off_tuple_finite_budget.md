# Sono/FMT H1b-COR2: off-tuple finite Markov budget

- 작성: 2026-09-09 KST.
- 수준: PROJECT FINITE ANALYTIC PROOF; 독립 동료심사·Lean 인증 아님.
- 범위: theories 35·47·49의 같은 실제 W-filtered construction과 고정 보조 X.
- 닫는 작업: DEP-R05. R03/R06와 전체 hypergraph·PAP·UB·최종 변수 이동은 닫지 않는다.
- child 충분조건: \(X\ge2\exp(10^{1000})\), 기존 조건 그대로.
- numerical \(X_{\rm cert}\): OPEN. 새 소수 계산·통계 실험·threshold calculator 없음.
- 계약: [data/Sono_FMT_H1bCOR2_off_tuple_budget_v1.json](data/Sono_FMT_H1bCOR2_off_tuple_budget_v1.json).
- 보조검산: [source/h1bcor2_off_tuple_budget.py](../../../source/h1bcor2_off_tuple_budget.py).
- 검토: [review 58](../../review/58_20260909_H1bCOR2_off_tuple_예산_타당성검토.md).

## 1. 선행증명과 이번에 채운 부분

[FMT, arXiv:1511.04468](https://arxiv.org/abs/1511.04468), p.14 Lemma 6.3,
(6.19)–(6.20)는 이미 다음 방법을 사용한다.

1. 좋은 p만의 합을 모든 p의 합으로 넓힌다.
2. q와 tuple의 k개 점이 함께 살아남을 확률을 계산한다.
3. off-tuple 평균 입력 (6.10)과 sigma*y (6.12)를 넣는다.
4. Markov로 큰 기여가 생기는 q의 개수를 제한한다.

따라서 새로운 확률 기법을 찾을 필요는 없다. 다만 그 원문에는 O·o(1)의 수치 계수,
실제 h의 개수와 공통 cutoff가 모두 명시되어 있지 않다. 이번에는 다음 기존 입력을
연결해 그 빈 부분만 증명한다.

| 입력 | 정확한 위치 | 현재 사용하는 결론 |
|---|---|---|
| [NORM47](47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md) | (47.1), (47.24), §§2·7 | 같은 preliminary law, 각 off-tuple h의 합 \(\le X/(ab^{10})\) |
| [COR1](49_Sono_FMT_H1bCOR1_finite_correlation_conditioning.md) | (49.5), (49.11)–(49.13), (49.21) | distinct-point correlation, 조건부 분모, bad-P 실패율 |
| [SIGMA35](35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md) | (H1c1b1a1.1), §§4–7 | \(\sigma Y<(26/25)80c_{\rm aux}Xb\), B0 한 소수 제외 포함 |
| FMT | pp.13–14, (6.15)–(6.20) | 확률 공간, 좋은 p, off-tuple Markov 구조 |

FMT p.14 proof의 일부 하첨자 k/r 혼용은 이 문서에서 같은 실제 sieve 차원 k로 통일한다.
이는 outer chain length를 growing sieve dimension과 동일시한다는 뜻이 아니다.
표적 source 조사이며 전 세계 문헌의 부재·novelty를 주장하지 않는다.

## 2. 변수와 정확한 대상

모든 로그는 자연로그다.
\[
 a=\ln X,\quad b=\ln a,\quad
 k=\lfloor(\ln(X/2))^{1/5}\rfloor\ge10^{200},
 \quad c_{\rm aux}=\frac1{153600\ln5},
 \quad Y=c_{\rm aux}Xa\frac{\ln b}{b}.
 \tag{50.1}
\]
\(c_{\rm aux}\)는 construction의 y 계수이고, 최종 Sono 계수
\(c_{\rm Sono}=2\times10^{-17}\)와 다른 수다. NORM47의 b=phi(B)/B와도
혼동하지 않는다. 여기서는 그 변수를 사용하지 않고 b를 항상 ln ln X로 쓴다.

P', Q', S, sigma, 독립 균등 residue vector \(\mathbf A\), preliminary
\(\widetilde n_p\), 좋은 소수 집합 \(P(\mathbf A)\)는 COR1 §2·(49.11)과 같다.
특히 \(P'\subset(X/2,X]\), \(Q'\subset(X,Y]\), \(|\widetilde n_p|\le Y\).
서로 다른 admissible \(h_i\)는 \(1\le h_i\le2k^2\)이고
\[
 2k^2X\le Y<Xa<X^2/4,\qquad k+1\le2k\le a.
 \tag{50.2}
\]
\(\mu_p(n)=\Pr(\widetilde n_p=n)\)는 \(\mathbf A\) 선택과 독립적으로 고정한다.
p들끼리의 독립성은 아래 선형기댓값·Markov에 필요하지 않다.

NORM47의 전체 weight mass와 이름이 겹치지 않게, FMT의 \(Z_p(\mathbf A;n)\)를
\[
 \zeta_p(\mathbf A;n)
 =\mu_p(n)\prod_{i=1}^k1_{\{n+h_ip\in\mathscr S(\mathbf A)\}}
 \tag{50.3}
\]
로 쓴다. 전체 조건부 분모는 \(D_p=\sum_n\zeta_p\)다.

다음 유한 집합은 음수·0·양수 h를 모두 포함한다.
\[
 {\cal H}_{\rm off}
 =\{h\in\mathbb Z: |h|<4Y/X,\ h\notin\{h_1,\ldots,h_k\}\}.
 \tag{50.4}
\]
q-hp가 support에 있으면 \(|h|p\le|q|+|q-hp|\le2Y\), p>X/2이므로
반드시 \(|h|<4Y/X\)다. 따라서 이 범위 밖의 항은 정확히 0이며 누락이 없다.
또
\[
 \# {\cal H}_{\rm off}\le2\lceil4Y/X\rceil-1
 <8Y/X+1\le9Y/X.
 \tag{50.5}
\]
첫 부등식에서 tuple 값을 빼는 이득은 필요 없어 버렸다. 끝점이 정수인 경우에도
strict \(|h|<4Y/X\)를 유지하며, positive h만 세는 오류를 피한다.

고정 q에 대해
\[
 V_q(\mathbf A)=\sigma^{-k}
 \sum_{p\in P(\mathbf A)}\sum_{h\in{\cal H}_{\rm off}}
       \zeta_p(\mathbf A;q-hp),\qquad
 T(\mathbf A)=\sum_{q\in Q'\cap\mathscr S(\mathbf A)}V_q(\mathbf A).
 \tag{50.6}
\]
이 T는 최종 tail threshold가 아니라 한 확률변수의 이름이다.

## 3. 모든 q를 함께 합한 기댓값

### 명제 50.1

위 실제 construction과 같은 child cutoff에서
\[
 \boxed{\mathbb E T\le\frac{800c_{\rm aux}X}{a b^9}.}
 \tag{50.7}
\]

증명. 모든 항이 비음수이므로 P(A)를 P'로 넓혀 상계한다. 각 h,p,q에서
\[
 q,\ q+(h_1-h)p,\ldots,q+(h_k-h)p
 \tag{50.8}
\]
는 서로 다른 k+1개 정수다. h가 tuple에 속하지 않고 p>0이기 때문이다.
mod s에서 residue가 겹칠 수는 있다. COR1은 정수 자체의 distinct 조건을 요구하며
그 residue 충돌 비용을 이미 포함한다.

엄밀히 \(|q+(h_i-h)p|\le Y+2k^2X+|h|X<6Y<X^2\).
마지막은 기존 \(Y<Xa\)와 \(6a<X\)로 따른다. 후자는 a>=1000에서
양의 exponential series \(e^a>a^2/2>6a\)로 충분하다.
q 역시 이 범위에 있고 k+1<=a이다.

따라서 (49.5)의 \(\epsilon=2/a^{17}\)을 적용할 수 있다.
\(\mu_p\)와 A의 독립성, 유한합의 기댓값 선형성으로
\[
\begin{split}
 \mathbb E T
 &\le \sigma^{-k}
 \sum_{h\in{\cal H}_{\rm off}}\sum_{q\in Q'}\sum_{p\in P'}
 \mu_p(q-hp)
 \Pr\{q,q+(h_i-h)p\ (\forall i)\in\mathscr S(\mathbf A)\}\\
 &\le(1+\epsilon)\sigma
 \sum_{h\in{\cal H}_{\rm off}}\sum_{q\in Q'}\sum_{p\in P'}
       \mu_p(q-hp).
\end{split}
\tag{50.9}
\]
특히 q 자체의 생존 조건을 생략하면 sigma라는 한 인수가 사라져 아래 예산이
성립하지 않는다. 서로 다른 q/p 사건을 독립이라고 곱한 식도 아니다.

NORM47 (47.24)는 C_h=4에서 각 안쪽 이중합을 \(X/(ab^{10})\)로 상계한다.
실제 요구조건 \(\ln C_h\le\ln(X/2)/4\)는 기존 cutoff에서 충분하다.
이로부터 (50.5)와 SIGMA35를 순서대로 적용하면
\[
 \mathbb E T
 \le 9(1+\epsilon)\frac{\sigma Y}{ab^{10}}
 < 9(1+\epsilon)\frac{26}{25}\,80c_{\rm aux}\frac{X}{ab^9}.
 \tag{50.10}
\]
a>=2에서 \(\epsilon\le1/100\)이다
(\(200<2^{17}\)). 정확히
\[
 9\frac{101}{100}\frac{26}{25}\,80
 =\frac{94536}{125}<800.
 \tag{50.11}
\]
따라서 (50.7). □

## 4. 큰 off-tuple 기여가 남는 q의 개수

\[
 N_{\rm bad}(\mathbf A)
 =\#\{q\in Q'\cap\mathscr S(\mathbf A):V_q(\mathbf A)>b^{-3}\},
 \qquad N_0=\frac{X}{2ab}.
\]
각 \(\mathbf A\)에서 \(N_{\rm bad}\le b^3T\)다. Markov와 (50.7)을 합치면
\[
 \boxed{\Pr\{N_{\rm bad}>N_0\}\le
 \min\left(1,\frac{1600c_{\rm aux}}{b^5}\right).}
 \tag{50.12}
\]
즉 그 실패확률을 제외하면 모든 살아남은 q 중 많아야
\(\lfloor X/(2ab)\rfloor\)개만 빼고
\[
 \boxed{V_q(\mathbf A)\le b^{-3}.}
 \tag{50.13}
\]
N0가 정수가 아니어도 위 비엄격 cardinality 상한은 floor(N0)다.
ceil(N0)-1로 무조건 바꾸지 않는다. 반면 off 기여가 정확히 b^-3인 점은
bad 집합에 넣지 않는다. 이것이 FMT (6.19)의 actual finite replacement다.

## 5. 조건부 실제 law와 실패 예산

좋은 p에서 \(D_p\ge(1-a^{-3})\sigma^k\)이므로
\[
\begin{split}
 W_q(\mathbf A)
 &:=
 \sum_{p\in P(\mathbf A)}\sum_{h\in{\cal H}_{\rm off}}
       \Pr(n_p=q-hp\mid\mathbf A)\\
 &\le\frac{V_q(\mathbf A)}{1-a^{-3}}
 \le \boxed{\frac{2}{b^3}}
\end{split}
\tag{50.14}
\]
가 같은 예외집합 밖에서 성립한다. 이는 조건부 law로 넘어갈 때의 추가 비용이다.
V와 W를 같은 값이라고 두지 않는다. bad p의 n_p=0은 prime q>p에 대해 q-hp=0을
만족할 수 없어 기여 0이다. 같은 p 안의 서로 다른 h도 서로 다른 n 값이다.

현재 cutoff에서 \(a\ge10^{1000}\)이고 ln10>2이므로 b>2000.
ln5>1을 쓰면
\[
 \frac{1600c_{\rm aux}}{b^5}
 =\frac{1}{96\ln5\,b^5}
 <\frac1{96\cdot2000^5}
 =\frac1{3{,}072{,}000{,}000{,}000{,}000{,}000}
 <10^{-18}.
 \tag{50.15}
\]
이는 현재의 매우 큰 충분조건에서만 얻은 **한 하위 사건의** 실패확률 상계다.
현재 계산 가능한 소수 범위의 관측 실패율, 전체 정리의 실패율 또는 최종
X_cert라고 해석하지 않는다. e<3에서 e^2<9<10으로 ln10>2도 초등적으로 따른다.

COR1 (49.21)의 good-P 사건까지 함께 요구하면 union bound로
\[
 \Pr(\text{off-tuple 실패 또는 good-P 실패})
 \le \frac{1600c_{\rm aux}}{b^5}+\frac7{a^8}.
 \tag{50.16}
\]
두 사건의 독립성은 필요 없다. 이는 **이 두 사건만의** 예산이며,
R03/R06 이후의 추가 사건·finite partition·hypergraph·coefficient slack까지
모두 합성한 R11의 전체 예산이 아니다.

## 6. 구현 검증이 하는 일과 하지 않는 일

작은 유한 residue 공간을 전수 열거하는 oracle와 prime별 곱으로 계산하는 별도
oracle를 exact Fraction으로 대조한다. positive/negative/zero h, strict endpoint,
q 생존, k+1 distinct, good-P를 넓히는 부등호, 조건부 분모, Markov cardinality를 검사한다.
테스트에서 q 생존을 일부러 빼거나 h를 tuple에 넣으면 동일성 또는 계약이 깨져야 한다.
모든 toy 입력에는 원소 수·연산량 제한이 있다.

큰 X나 k개의 실제 배열을 만들지 않고 (50.11),(50.15) 같은 상수 산술만 검산한다.
이 검산은 모든 실제 소수를 생성하는 실험이나 무한범위 증명의 독립 형식 인증이 아니다.
무한범위의 근거는 §§2–5의 해석적 논증과 명시된 기존 theorem/child다.
독립 검증에서 선행 child의 오류를 발견하면 이 결과도 의존 영향을 다시 감사한다.

## 7. 상태와 다음 단계

| 구분 | 상태 |
|---|---|
| DEP-R05 | ACTUAL_INPUTS_PROJECT_EXPLICIT |
| 이미 닫힌 R01/R02/R04 | 그대로 보존 |
| 현재 OPEN | R03, R06, R07, R08, R09, R10, R11, R12 (8 work packages) |
| broad SIV-07/08/09 | HARD_BLOCKER 유지 |
| X_cert / threshold calculator | OPEN / NOT READY |
| 계수 개선·새 관측범위·독립 bridge 강화 | 사용자 결정에 따라 별도 후속 연구 |

작업 ID의 수는 난이도·완료율 또는 독립 정리의 개수가 아니다.
다음은 R03 local-count/finite partition을 source-first로 확인하고,
R06 main-degree의 1·2차 moment와 같은 예외집합 예산에 연결하는 H1b-COR3다.
