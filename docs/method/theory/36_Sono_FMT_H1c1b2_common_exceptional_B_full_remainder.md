# Sono/FMT H1c-1b.2 common exceptional `B`·full Bordignon remainder

- 작성: 2026-09-09 KST
- 증거 수준: `SOURCE-LEVEL QUANTIFIER AUDIT / PROJECT FINITE BRIDGE`
- 판정:
  `COMMON_EXCEPTIONAL_B_AND_RAW_PSI_DYADIC_COMPOSITION_CLOSED / COUNT_TRANSFER_AND_ABSORPTION_OPEN`
- H1c-1b.2: `PARTIAL — 실제 identity-form의 common B와 raw psi 합성은 닫힘`
- Hypothesis 1(2), Maynard Proposition 9.2: `OPEN / RATE_MISSING`
- `SIV-07/08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b2_common_exceptional_remainder_v1.json`](data/Sono_FMT_H1c1b2_common_exceptional_remainder_v1.json)
- 검산 구현:
  [`source/h1c1b2_common_exceptional_remainder.py`](../../../source/h1c1b2_common_exceptional_remainder.py)
- 비판적 검토:
  [`docs/review/42_20260909_H1c1b2_common_exceptional_B_full_remainder_타당성검토.md`](../../review/42_20260909_H1c1b2_common_exceptional_B_full_remainder_타당성검토.md)

## 1. 결론

고정된 바깥 scale \(X\)에 대해 실제 Maynard Proposition 9.2 호출의 아래 endpoint를

\[
T=X/2,\qquad r=\lfloor(\log T)^{1/5}\rfloor,\qquad
A=100r^2+10,\qquad Q_1=(\log T)^A
\]

로 둔다. Bordignon Theorem 1.4를 \(u=T\)와 \(u=2T\)에 적용할 때 **같은 \(Q_1\)**을
사용하면 exceptional modulus \(q_0\)도 같은 하나다. \(q_0\)가 있으면 그 소인수 하나를
prime \(B\)로 고르고, 없으면 \(B=1\)로 둔다. 그러면

\[
(q,B)=1\quad\Longrightarrow\quad q_0\nmid q.
\]

따라서 Maynard가 합산하는 모든 \(q\le T^{1/3},(q,B)=1\)은 두 endpoint 모두에서
Bordignon의 non-exceptional 합 안에 들어간다. 이 \(B\)는 고정 \(X\)와 그 dyadic pair에
공통인 하나이며, 모든 \(X\)에 영원히 같은 전역 \(B\)를 고른다는 뜻은 아니다.

또 최종 NYJM 출판본 Theorem 1.4의 양의 RHS를 빠짐없이 12개 항으로 옮겼다. 누적 오차를

\[
D_u(q,a)=\psi(u;q,a)-\frac{\psi(u)}{\varphi(q)}
\]

라 두면

\[
\left(\psi(2T;q,a)-\psi(T;q,a)\right)
-\frac{\psi(2T)-\psi(T)}{\varphi(q)}
=D_{2T}(q,a)-D_T(q,a).
\]

삼각부등식으로 \((T,2T]\)의 von Mangoldt-weighted 합계 오차는

\[
R_B(T;A,Q_1,C_*)+R_B(2T;A,Q_1,C_*)
\]

이하가 된다. 여기서 \(C_*\)는 Bordignon Theorem 1.2에서 얻은 유효한 상수 상계다.

닫히지 않은 것은 half-open endpoint, prime powers 제거, unweighted prime count,
Maynard의 정확한 중심항, 12개 오차의 \((\log T)^{-100r^2}\) 흡수와 공통 cutoff다. 따라서
이 결과를 Hypothesis 1(2), Proposition 9.2 또는 \(X_{\mathrm{cert}}\) 완성으로 승격하지 않는다.

## 2. 쉬운 설명

Bordignon 정리는 “나쁜 예외 modulus가 있다면 하나를 빼고 나머지를 한꺼번에 제어한다”고
말한다. 우리에게는 구간의 양 끝 \(T\), \(2T\)에서 계산한 두 누적값의 차가 필요하다.

양 끝에서 서로 다른 예외를 빼면 같은 \(q\) 목록을 뺄셈할 수 없다. 해결은 예외를 endpoint가
아니라 공통 절단값 \(Q_1\)로 고르는 원문의 quantifier를 그대로 쓰는 것이다. 같은 \(Q_1\)을
두 번 쓰면 같은 예외 \(q_0\)가 나오고, 그 안의 prime 하나 \(B\)를 빼는 것만으로 두 합의
대상이 같아진다.

비유하면 두 장부의 차를 계산할 때 두 장부에서 같은 “검토 보류 계정” 하나를 제외한 셈이다.
이제 장부끼리 빼는 구조는 맞지만, 장부의 단위가 아직 “소수 개수”가 아니라 로그 가중치다.
그 단위 변환과 최종 오차 예산은 다음 단계다.

## 3. 선행연구 우선 대조

직접 bridge를 쓰기 전에 다음 원문을 대조했다.

- [Bordignon 2021 최종 NYJM판](https://nyjm.albany.edu/j/2021/27-54.html),
  Theorems 1.1·1.2·1.4와 proof (34)--(37): fixed \(Q_1\)의 exceptional modulus,
  cumulative \(\psi\) center와 full RHS.
- [Maynard 2016](https://doi.org/10.1112/S0010437X16007296), Hypothesis 1(2),
  Theorem 3.1, Proposition 9.2: \((q,B)=1\), \(B\le x^\alpha\), count target.
- [FGKMT 2018](https://doi.org/10.1090/jams/876), Theorem 6과 Section 8:
  실제 \(T=X/2\), prime-weighted identity form \(n\), \(B=1\) 또는 prime인 호출.

원문은 exceptional quantifier와 cumulative bound를 제공한다. 동일 \(Q_1\), prime divisor
\(B\), 두 endpoint 차분을 실제 호출에 연결하는 짧은 논리 bridge는 별도 표시가 없어 이번
project lemma로 적었다. 표적 검색에서 이를 그대로 적은 후속 lemma나 공식 erratum은 찾지
못했지만, 이는 전 세계 문헌 비존재나 novelty 주장이 아니다.

## 4. source 판본 통제

공식 arXiv `2101.08610` v1 author source와 최종 NYJM 출판본은 수식이 같지 않다.

| 항목 | arXiv v1 | 최종 NYJM판 | 이번 채택 |
|---|---|---|---|
| 중심항 | \(u/\varphi(q)\) | \(\psi(u)/\varphi(q)\) | 최종판 |
| \(C\)-항 log factor | v1 표시 | 최종 표시가 다름 | 최종판 |
| 첫 \(E\)-항 log factor | v1 표시 | 최종 표시가 다름 | 최종판 |

따라서 계산 구현은 최종판과 최종 proof (34)--(37)만 정본으로 삼는다. 이 선택은 중요하다.
\(\psi\) 중심을 쓰면 endpoint 차가 정확히 전체 von Mangoldt 구간합의 중심이 되지만,
\(u\) 중심을 섞으면 별도 \(\psi(u)-u\) 보정이 생긴다.

## 5. Project Lemma L1 — common exceptional `B`

Bordignon Theorem 1.4는 fixed \(Q_1\)에 대해 “\(Q_1\)까지의 exceptional modulus
\(q_0\), if it exists”를 정의한다. \(q_0\)의 선택은 theorem endpoint \(u\)가 아니라 같은
\(Q_1\)에 의해 고정된다.

1. \(u=T\), \(u=2T\)에 같은 \(Q_1=(\log T)^A\)를 쓴다.
2. \(q_0\)가 있으면 prime divisor \(B\mid q_0\) 하나를 택한다. 없으면 \(B=1\)이다.
3. \((q,B)=1\)이면 \(B\nmid q\)이므로 \(q_0\nmid q\)다.
4. H1c-1b.1의 capacity 결과로 \(q\le T^{1/3}\)은 두 endpoint의 \(Q_B(u,A)\) 안에 든다.

크기 조건도 충분하다.

\[
B\le q_0\le Q_1\le Q_B(T,A)<\sqrt T<T.
\]

따라서 FGKMT Lemma 7.2의 \(B\le T\)와 Maynard actual \(\alpha=2\) 조건을 모두
만족한다. selected form의 leading coefficient가 1이므로 \((1,B)=1\)이고,
\(B\)의 prime-factor count도 하나다.

## 6. Project Lemma L2 — full published remainder

\(L=\log u\), \(\ell=\log L\), \(\lambda=\log Q_1\)라 쓰고,

\[
\delta=\frac1{2AR_1\ell},\qquad R_1=2.0452=\frac{5113}{2500}
\]

로 둔다. Bordignon의 최종 RHS를 \(u\)로 나눈 12개 항은 다음과 같다.

| # | 이름 | \(R_j(u)/u\) |
|---:|---|---|
| 1 | leading sqrt | \(e^{-L/2}\) |
| 2 | main log tail | \(2c_1c_0e^{-(A-9/2)\ell}\) |
| 3 | main \(Q_1\) tail | \(2c_1c_0e^{(9/2)\ell-\lambda}\) |
| 4 | Theorem 1.2 small modulus | \(c_1^2C_*(1+A\ell)e^{-(A-4)\ell}/2\) |
| 5 | induced-character small modulus | \(e^{-L/2-(A-1)\ell}/(2\log2)\) |
| 6 | exceptional zero | \(c_1^2(1+A\ell)L e^{-\delta L}/[2(1-\delta)]\) |
| 7 | density exponential | \(17c_1^2(1+A\ell)L^{2.52}e^{-0.81\sqrt L}\) |
| 8 | density constant | \(c_1^2(1+A\ell)L(A\ell/\log2)e^{-L}/2\) |
| 9 | large-modulus sqrt | \(2c_0c_1e^{-L/2+(A+9/2)\ell}\) |
| 10 | \(11/12\) term | \(9c_0c_1e^{-L/12+(9/2-A/2)\ell}\) |
| 11 | \(5/6\) term | \((5/2)c_0c_1e^{-L/6+(9/2)\ell}\) |
| 12 | \(5/6\)·log term | \((5/4)c_0c_1e^{-L/6+(11/2)\ell}\) |

모든 항은 양수이므로 일부를 생략해 작은 숫자를 얻는 것은 허용하지 않는다. 구현은 상수
\(C_*\)를 명시 입력으로 요구한다. 출판본 Theorem 1.2는
\(C(\alpha_1,\alpha_2,Y_0)\), \(Y_0=\log\log X_0\)를 정의하지만 Theorem 1.4와 proof
(35)는 \(C(A,A-3,X_0)\)라고 적는다. 이 표기 불일치를 임의로 고치지 않기 위해서다.

## 7. Project Lemma L3 — dyadic subtraction

두 endpoint에 같은 modulus subset을 쓰면 각 \(q,a\)에 대해

\[
|D_{2T}(q,a)-D_T(q,a)|\le |D_{2T}(q,a)|+|D_T(q,a)|.
\]

maximum과 합을 취해도

\[
\sum_{\substack{q\le T^{1/3}\\(q,B)=1}}
\max_a |D_{2T}(q,a)-D_T(q,a)|
\le R_B(2T)+R_B(T).
\]

상대오차 함수 \(\rho(u)=R_B(u)/u\)로 쓰면 \(T\) 기준 bound는

\[
\frac{R_B(T)+R_B(2T)}T=\rho(T)+2\rho(2T).
\]

이 단계는 \((T,2T]\)의 \(\psi\) 합에 대해 정확하다. Maynard의 integer interval convention과
unweighted prime count로 옮기는 것은 다음 H1c-1b.3에서 endpoint atom까지 포함해 처리한다.

## 8. 닫힌 항목과 열린 항목

| 항목 | 상태 | 한계 |
|---|---|---|
| fixed \(Q_1\)에서 두 endpoint의 같은 \(q_0\) | `SOURCE_QUANTIFIER_VERIFIED` | 한 outer scale의 dyadic pair |
| prime divisor \(B\) filter | `PROJECT_FINITE_BRIDGE_CLOSED` | actual identity-form |
| \(B\) 크기·coefficient coprimality | `CLOSED_FOR_ACTUAL_CALL` | general affine family 아님 |
| 최종 출판본 12항 전사 | `PARAMETERIZED_EXPLICIT` | 유효한 \(C_*\) 입력 필요 |
| raw \((T,2T]\) \(\psi\) composition | `PROJECT_FINITE_BRIDGE_CLOSED` | log-weighted |
| arXiv v1 식 채택 | `REJECTED` | 최종판과 다름 |
| \(X_0/Y_0\) 상수 표기 | `OPEN` | 재유도 또는 저자 확인 필요 |
| half-open·prime powers·\(\psi\to\pi\) | `OPEN` | H1c-1b.3 |
| exact total recentering·density·12항 흡수 | `OPEN` | H1c-1b.3/1b.4 |
| H1(2), P9.2, SIV-07/08, \(X_{\mathrm{cert}}\) | `OPEN / HARD_BLOCKER` | 승격 없음 |

## 9. 검증과 자원

보조 구현은 다음을 fail-closed로 검사한다.

1. \(B\)가 실제로 \(q_0\)의 prime divisor인지.
2. \(q=1,\ldots,9999\) toy 범위에서 filter implication이 한 건도 깨지지 않는지.
3. 최종판의 12개 상대항을 모두 등록했는지.
4. dyadic 정규화가 \(\rho(T)+2\rho(2T)\)인지.
5. 닫히지 않은 count·absorption·threshold flag가 거짓인지.

새 package, Lean, PARI/GP, 장시간 CPU 또는 실제 prime 계산은 필요하지 않다.

## 10. 다음 gate

1. **H1c-1b.3 endpoint/count transfer**: \((T,2T]\) \(\psi\)에서 Maynard의 exact half-open
   unweighted identity-prime count로 옮기고, prime powers와 total recentering을 명시한다.
2. **H1c-1b.4 full absorption**: \(C_*\), \(c_0,c_1\), 12개 항, represented-prime density를
   하나의 cutoff로 합쳐 \((\log T)^{-100r^2}\) 목표를 실제로 만족하는지 판정한다.
3. 그 뒤에만 Hypothesis 1(2), Proposition 9.2와 상위 moment budget 승격을 검토한다.

```text
common exceptional B at fixed X         = CLOSED FOR ACTUAL IDENTITY CALL
final published remainder transcription = 12/12 PARAMETERIZED EXPLICIT
raw dyadic von Mangoldt composition      = CLOSED ON (T,2T]
unweighted prime-count transfer          = OPEN
full error absorption/common cutoff      = OPEN
Hypothesis 1(2) / Proposition 9.2        = OPEN / RATE_MISSING
SIV-07 / SIV-08                          = HARD_BLOCKER
threshold calculator                     = NOT READY
X_cert                                   = OPEN
```

## 11. 2026-09-09 H1c-1b.3 후속 결과

[H1c-1b.3 정본](37_Sono_FMT_H1c1b3_endpoint_count_transfer.md)은 이 문서의 fixed
q-family와 \(B\)를 Abel 적분 전체에 유지하고, plus-sign partial summation,
prime-power 제거, half-open endpoint와 exact total center를 합성했다. 따라서 successor의
unweighted prime-count transfer는 `CLOSED`다.

이 문서의 역사적 `OPEN` flag는 H1c-1b.2 당시 판정으로 보존한다. density,
\(C(A,A-3,X_0/Y_0)\) 정규화와 full absorption은 H1c-1b.4에 남아
Hypothesis 1(2), Proposition 9.2, `SIV-07/08`, \(X_{\mathrm{cert}}\)는 계속 열린다.
