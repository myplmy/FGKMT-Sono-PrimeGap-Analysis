# Sono/FMT H1c-1b.3 endpoint·unweighted prime-count transfer

> **2026-09-09 적용구간 교정:** 아래 half-open 계산은 Maynard 원논문의 Definition
> (2.1)에 대해서는 정확하지만, FGKMT가 실제로 사용하는 수정 Definition 2는
> \([T,2T]\)이다. 따라서 아래 문서의 “actual FGKMT target” 표기는 철회한다. 실제
> 적용용 교정과 보존되는 수치상계는
> [H1c-1b.3r1](42_Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction.md)을 따른다.
> 과거 유도 자체를 숨기지 않기 위해 본문은 역사적 기록으로 보존한다.

- 작성: 2026-09-09 KST
- 증거 수준: `SOURCE-LEVEL TARGET AUDIT / PROJECT FINITE BRIDGE`
- 판정:
  `EXACT_HALF_OPEN_UNWEIGHTED_COUNT_TRANSFER_CLOSED / FULL RATE AND DENSITY OPEN`
- H1c-1b.3: `CLOSED — actual identity form의 target quantity까지 정확히 전달`
- Hypothesis 1(2), Maynard Proposition 9.2: `OPEN / RATE_MISSING`
- `SIV-07/08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b3_endpoint_count_transfer_v1.json`](data/Sono_FMT_H1c1b3_endpoint_count_transfer_v1.json)
- 검산 구현:
  [`source/h1c1b3_endpoint_count_transfer.py`](../../../source/h1c1b3_endpoint_count_transfer.py)
- 비판적 검토:
  [`docs/review/43_20260909_H1c1b3_endpoint_count_transfer_타당성검토.md`](../../review/43_20260909_H1c1b3_endpoint_count_transfer_타당성검토.md)

## 1. 결론

H1c-1b.2가 얻은 fixed-family cumulative von Mangoldt discrepancy를 Maynard가 실제로
요구하는 양으로 정확히 옮길 수 있다. 실제 FGKMT Section 8 호출에서

\[
T=x/2,\qquad \mathcal A=\mathbb Z,\qquad \mathcal P=\mathbb P,
\qquad L(n)=n
\]

이며 Maynard의 정의는

\[
\mathcal A(T)=\{n\in\mathbb Z:T\le n<2T\}.
\]

따라서 목표는 log-weighted \(\psi\)가 아니라

\[
P_T(q,a)=\#\{p:T\le p<2T,\ p\equiv a\pmod q\},\qquad
P_T=\#\{p:T\le p<2T\}
\]

의 exact centered discrepancy

\[
P_T(q,a)-\frac{P_T}{\varphi(q)}
\]

다. 이번 단계는 partial summation, prime powers와 endpoint atom을 모두 보존해 이 target에
도달한다. 중심값을 \(T/\log T\)로 근사하지 않으므로 recentering residual은 생기지 않는다.

다만 이 절대오차 상계가 Maynard의 요구량

\[
\frac{P_T}{(\log T)^{100r^2}}
\]

보다 작다는 수치 증명은 아직 없다. Bordignon의 상수 표기, 12개 remainder의 공통 흡수와
\(P_T\)의 explicit lower bound는 H1c-1b.4로 남는다. 그러므로 H1(2), P9.2 또는
\(X_{\mathrm{cert}}\)를 완성했다고 해석하면 안 된다.

## 2. 쉬운 설명

직전 결과는 물건 개수가 아니라 각 물건에 `log(소수)`라는 무게를 붙인 장부였다. 이번에는
그 장부를 실제 소수 개수 장부로 바꾼다. 변환할 때 세 가지 차이가 생긴다.

1. 소수의 제곱·세제곱도 \(\psi\) 장부에 들어 있으므로 빼야 한다.
2. 직전 장부 구간은 \((T,2T]\), Maynard 구간은 \([T,2T)\)이므로 양 끝 한 칸을 바꿔야 한다.
3. 각 나머지류의 개수를 전체 구간의 실제 소수 개수와 비교해야 한다.

이 세 차이에 안전한 비용을 붙여 같은 장부 단위로 만드는 데 성공했다. 아직 남은 일은
그 비용이 목표보다 충분히 작은지 증명하는 것이다. 즉 “단위와 구간이 맞아졌다”가 이번
결과이고, “오차가 최종 합격선 안에 들어갔다”는 다음 결과다.

## 3. 원문 target 감사

### 3.1 Maynard 2016

[Maynard 2016](https://doi.org/10.1112/S0010437X16007296)의 Definition (2.1)은

\[
\mathcal A(T)=\{n\in\mathcal A:T\le n<2T\}
\]

를 사용한다. Hypothesis 1(2)와 Proposition 9.2의 오차는

\[
\#\mathcal P_{L,\mathcal A}(T;q,a)
-\frac{\#\mathcal P_{L,\mathcal A}(T)}{\varphi_L(q)}
\]

이며 prime indicator \(1_{\mathcal P}(L(n))\)를 합한다. 이는 unweighted prime count다.

### 3.2 FGKMT actual application

[FGKMT 2018](https://doi.org/10.1090/jams/876) Section 8의 식 (6.5) 증명은
\(T=x/2\)에서

\[
\widetilde L_{q,i,i}(n)=n
\]

인 identity form에 Theorem 6의 두 번째 결론, 즉 Maynard Proposition 9.2를 적용한다.
\(\mathcal P\)는 모든 소수이고 \(\varphi_L(q)=\varphi(q)\)다. 따라서 general affine
residue 변환, 음의 leading coefficient와 별도 gcd case는 이번 actual child에서 필요 없다.

## 4. 선행연구 우선 조사와 채택 범위

[Akbary--Hambrook 2015](https://arxiv.org/abs/1309.2730)의 Corollary 1.4 proof는

\[
\pi_1(y;q,a)=\sum_{\substack{2\le n\le y\\n\equiv a\pmod q}}
\frac{\Lambda(n)}{\log n}
=\sum_{\substack{p^k\le y\\p^k\equiv a\pmod q}}\frac1k
\]

를 도입해 partial summation과 prime-power removal을 수행한다. 따라서 이 방법을 먼저
채택하고, 현재 fixed-\(B\) modulus family에 맞는 dyadic 형식만 project bridge로 다시 쓴다.

그 논문의 Corollary 1.4 전체는 \(\ell(q)>Q_1\)인 rough-modulus family를 다루므로
\((q,B)=1\) family에 drop-in할 수 없다. 반대로 그 proof의 \(\pi_1\) 항등식과
\(\pi_1-\pi\) bound는 각 \(q,a\)에 대한 점별 사실이므로 사용할 수 있다.

원문 p. 26의 cumulative partial-summation display에는 적분 앞에 minus가 보인다. 그러나
Stieltjes/Abel summation을 직접 적용하면 적분 부호는 plus다. 그 원문도 다음 줄에서
triangle inequality만 사용하므로 최종 크기 상계는 부호에 무관하다. 프로젝트는 표시를
복사하지 않고 아래의 직접 유도된 plus identity를 사용한다. 공식 arXiv·AMS를 표적으로
검색했지만 별도 erratum은 찾지 못했다. 이는 전 세계 비존재 주장이 아니다.

## 5. Project Lemma L1 — Abel 구간 항등식

누적 discrepancy를

\[
D_\psi(u;q,a)=\psi(u;q,a)-\frac{\psi(u)}{\varphi(q)}
\]

라 하자. 함수 \(f(u)=1/\log u\)는

\[
f'(u)=-\frac1{u(\log u)^2}
\]

이므로 Abel summation은

\[
D_{\pi_1}(y;q,a)
=\frac{D_\psi(y;q,a)}{\log y}
+\int_2^y\frac{D_\psi(u;q,a)}{u(\log u)^2}\,du
\]

를 준다. \(y=2T\) 식에서 \(y=T\) 식을 빼면 정확히

\[
\boxed{
D_{\pi_1}^{(T,2T]}(q,a)
=\frac{D_\psi(2T;q,a)}{\log(2T)}
-\frac{D_\psi(T;q,a)}{\log T}
+\int_T^{2T}\frac{D_\psi(u;q,a)}{u(\log u)^2}\,du
}
\tag{37.1}
\]

이다.

### 적분 전체에서 같은 modulus family를 쓸 수 있는가

H1c-1b.2의

\[
A=100r^2+10,\qquad Q_1=(\log T)^A
\]

와 같은 \(B\)를 고정한다. H1c-1b.1은 \(r\ge36\)에서

\[
T^{1/3}\le\frac{\sqrt T}{(\log T)^A},\qquad \log T>2A
\]

를 닫았다. 후자는

\[
u\longmapsto \frac{\sqrt u}{(\log u)^A}
\]

가 \([T,2T]\)에서 증가함을 뜻한다. 또한
\(Q_1=(\log T)^A\le(\log u)^A\)다. 따라서 모든 \(u\in[T,2T]\)에서 같은

\[
\mathcal Q_T(B)=\{q:q\le T^{1/3},\ (q,B)=1\}
\]

가 Bordignon의 허용 family 안에 있고, fixed \(Q_1\)이 고른 같은 exceptional \(q_0\)와
같은 \(B\)가 유지된다.

각 \(u\)에서

\[
\sum_{q\in\mathcal Q_T(B)}\max_{(a,q)=1}|D_\psi(u;q,a)|\le R_B(u)
\]

라 하자. 유한합·maximum·적분에 triangle inequality를 적용하면 (37.1)에서

\[
S_{\pi_1}^{(T,2T]}
\le
\frac{R_B(2T)}{\log(2T)}
+\frac{R_B(T)}{\log T}
+\int_T^{2T}\frac{R_B(u)}{u(\log u)^2}\,du.
\tag{37.2}
\]

## 6. Project Lemma L2 — prime powers 제거

\[
E(y;q,a)=\pi_1(y;q,a)-\pi(y;q,a),\qquad
E(y)=\pi_1(y)-\pi(y)
\]

라 하자. 이는 지수 \(k\ge2\)인 prime powers의 양의 합이다. Akbary--Hambrook의 explicit
estimate는 \(y\ge4\)에서

\[
0\le E(y;q,a)<2\sqrt y,\qquad 0\le E(y)<2\sqrt y
\tag{37.3}
\]

를 준다. 구간 증가량도 음이 아니며 각각 \(E(2T;q,a)\), \(E(2T)\) 이하이므로

\[
\left|D_\pi^{(T,2T]}-D_{\pi_1}^{(T,2T]}\right|
\le2\sqrt{2T}\left(1+\frac1{\varphi(q)}\right).
\]

다음 두 양을 정의한다.

\[
M_B(T)=\#\mathcal Q_T(B),\qquad
\Phi_B(T)=\sum_{q\in\mathcal Q_T(B)}\frac1{\varphi(q)}.
\]

그러면 전체 prime-power 비용은

\[
2\sqrt{2T}\{M_B(T)+\Phi_B(T)\}
\tag{37.4}
\]

이하다. 조악하지만 완전 명시적인 \(\Phi_B\le M_B\le T^{1/3}\)을 쓰면

\[
(37.4)\le4\sqrt2\,T^{5/6}.
\tag{37.5}
\]

이 상계는 sharp할 필요가 없다. 다음 H1c-1b.4에서 목표 rate에 흡수되는지만 판단한다.

## 7. Project Lemma L3 — \((T,2T]\)에서 \([T,2T)\)로

실수 \(v\)에 대해 \(1_{\mathbb P}(v)\)는 \(v\)가 정수 소수일 때만 1이라고 하자. 전체와
각 나머지류에서

\[
P^{[T,2T)}=P^{(T,2T]}+1_{\mathbb P}(T)-1_{\mathbb P}(2T).
\tag{37.6}
\]

\(T>2\)이면 두 endpoint가 동시에 소수일 수 없다. \(T\)가 정수 소수이면 \(2T\)는
합성수이고, \(2T\)가 홀수 소수이면 \(T\)는 정수가 아니다. 따라서 한 \(q\)의 centered
endpoint correction은 한 atom뿐이며

\[
\left|\delta_{q,a}-\frac{\delta}{\varphi(q)}\right|\le1.
\tag{37.7}
\]

모든 modulus를 합치면 endpoint 비용은

\[
M_B(T)\le T^{1/3}.
\tag{37.8}
\]

코드의 `centered_single_endpoint_atom`은 (37.7)을 `Fraction`으로 exact 검산한다. 별도의
primality 판정이나 actual prime sweep을 하지 않는다.

## 8. 최종 parameterized count-transfer theorem

위 세 lemma를 합치면 (T\ge4)인 actual identity form에 대해

\[
\boxed{
\begin{aligned}
S_\pi^{[T,2T)}\le{}&
\frac{R_B(2T)}{\log(2T)}
+\frac{R_B(T)}{\log T}
+\int_T^{2T}\frac{R_B(u)}{u(\log u)^2}\,du\\
&+2\sqrt{2T}\{M_B(T)+\Phi_B(T)\}+M_B(T).
\end{aligned}}
\tag{37.9}
\]

여기서

\[
S_\pi^{[T,2T)}=
\sum_{q\in\mathcal Q_T(B)}
\max_{(a,q)=1}
\left|P_T(q,a)-\frac{P_T}{\varphi(q)}\right|.
\]

따라서 중심항은 Maynard의 exact total \(P_T\)와 **완전히 같다**. \(T/\log T\) 또는
\(\operatorname{li}(2T)-\operatorname{li}(T)\)로 바꾸지 않았다.

### 다음 단계용 상대 envelope

\[
\rho_*=\sup_{T\le u\le2T}\frac{R_B(u)}u
\]

라 하면 적분항은

\[
\int_T^{2T}\frac{R_B(u)}{u(\log u)^2}\,du
\le\frac{\rho_*T}{{(\log T)^2}}
\]

이고 (37.5), (37.8)을 써서

\[
\boxed{
\frac{S_\pi^{[T,2T)}}T
\le\rho_*\left{
\frac1{\log T}+\frac2{\log(2T)}+\frac1{(\log T)^2}
\right}
+4\sqrt2\,T^{-1/6}+T^{-2/3}.}
\tag{37.10}
\]

(37.10)은 absorption에 쓸 수 있는 안전한 envelope이지, 현재 \(\rho_*\)의 모든 상수와
cutoff가 이미 준비됐다는 뜻은 아니다.

## 9. 독립 toy 검산

검산은 다음을 서로 다른 방식으로 확인한다.

1. 작은 \(T,q,a\)에서 \(\Lambda\), \(\pi_1\), \(D_\psi\)를 직접 열거한다.
2. 계단함수 \(D_\psi(u)\)의 적분을 각 정수 구간에서
   \(1/\log n-1/\log(n+1)\)로 독립 계산한다.
3. plus identity는 일치하고 minus identity는 일치하지 않는 fixture를 고정한다.
4. \(4\le y\le400\)의 prime powers를 직접 열거해 (37.3)을 검사한다.
5. 정수·반정수 \(T\) fixture에서 (37.6), exact centered correction과 (37.7)을 검사한다.
6. 구현 formula를 독립 재계산하고 상위 open flag가 거짓인지 확인한다.

이 검산은 원 정리를 재증명하지 않는다. source 증명과 project bridge의 전사·부호·끝점
회귀검사다.

## 10. 닫힌 항목과 열린 항목

| 항목 | 상태 | 한계 |
|---|---|---|
| Maynard target interval·weight·center | `SOURCE_VERIFIED` | actual identity form |
| Abel 적분 전체의 same fixed family | `PROJECT_FINITE_BRIDGE_CLOSED` | \(r\ge36\), fixed outer scale |
| partial summation | `CLOSED_WITH_PLUS_SIGN` | (37.1) |
| prime powers 제거 | `EXPLICIT`, constant 2 | Akbary--Hambrook bound |
| half-open endpoint | `EXACT`, cost \(M_B\) | \(T>2\) |
| unweighted exact-center transfer | `CLOSED` | formula (37.9) |
| Bordignon \(C(A,A-3,X_0/Y_0)\) | `OPEN` | H1c-1b.4 |
| \(P_T\) explicit lower bound | `OPEN` | H1c-1b.4 |
| 12항·count 비용 full absorption | `OPEN` | H1c-1b.4 |
| H1(2), P9.2, SIV-07/08 | `OPEN / HARD_BLOCKER` | 승격 없음 |
| \(X_{\mathrm{cert}}\) | `OPEN` | calculator 작성 금지 유지 |

## 11. 자원과 다음 gate

이번 증명·toy 검산에는 새 논문 다운로드, 새 Python package, Lean, PARI/GP, 장시간 CPU 또는
actual prime 계산이 필요하지 않았다. 사용자 수행절차는 **별도 수행절차 필요없음**이다.

다음 gate H1c-1b.4는 다음을 한 번에 해결해야 한다.

1. Bordignon의 \(C(A,A-3,X_0/Y_0)\) 표기를 source 원식에서 type-safe하게 해소한다.
2. \(c_0,c_1,C_*\), 12개 \(R_B\) 항과 (37.9)의 추가 비용을 한 cutoff에 합친다.
3. exact \(P_T\)에 대한 explicit lower bound를 증명한다.
4. (37.9)가 \(P_T/(\log T)^{100r^2}\) 이하임을 보인다.
5. 이 결과 뒤에만 Hypothesis 1(2), P9.2 상태를 재판정한다.

```text
actual Maynard quantity                 = SOURCE VERIFIED
Abel / prime powers / half-open endpoint = CLOSED
exact total-population recentering       = CLOSED
full relative-rate absorption            = OPEN
Hypothesis 1(2) / Proposition 9.2        = OPEN / RATE_MISSING
SIV-07 / SIV-08                          = HARD_BLOCKER
threshold calculator                     = NOT READY
X_cert                                   = OPEN
```
