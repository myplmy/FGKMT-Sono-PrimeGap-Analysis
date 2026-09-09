# Sono/FMT H1c-1b.4a Bordignon source normalization

- 작성: 2026-09-09 KST
- 증거 수준: `PRIMARY-SOURCE EQUATION AUDIT / PROJECT ALGEBRAIC CORRECTION`
- 판정:
  `TYPE MAPPING AND DIRECT REMAINDER ALGEBRA CLOSED / NUMERICAL C_A BLOCKED`
- H1c-1b.4a: `PARTIAL — 표기와 정확한 필요항은 복원, 수치 상계는 미복원`
- Hypothesis 1(2), Maynard Proposition 9.2: `OPEN / RATE_MISSING`
- `SIV-08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b4a_Bordignon_source_normalization_v1.json`](data/Sono_FMT_H1c1b4a_Bordignon_source_normalization_v1.json)
- 검산 구현:
  [`source/h1c1b4a_bordignon_source_normalization.py`](../../../source/h1c1b4a_bordignon_source_normalization.py)
- 비판적 검토:
  [`docs/review/44_20260909_H1c1b4a_Bordignon_source_normalization_타당성검토.md`](../../review/44_20260909_H1c1b4a_Bordignon_source_normalization_타당성검토.md)

## 1. 결론

Bordignon 최종 출판본의 Theorem 1.2 상수 \(C(\alpha_1,\alpha_2,Y_0)\)는 현재 actual
growing-dimension 적용에 그대로 수치 대입할 수 없다. 두 문제가 겹친다.

1. \(Y_0=\log\log X_0\)라 정의하고 정리는 \(x\ge X_0\)에서 성립하지만, 식 (33)의
   바깥 maximum은 \(x\ge Y_0\), Theorem 1.4와 식 (35)는
   \(C(A,A-3,X_0)\)라 인쇄한다.
2. 최종 식 (33)의 첫 항은
   \(R^*(x,T,q)\log\log x/\log^2x\)다. Theorem 3.4의 \(R^*\)는
   \(\psi\)의 **절대오차**이므로 필요한 \(x\)-정규화가 없다.

arXiv v1의 첫 항은 \(R^*T/(x\log^2x)\)로 다르다. 차원이 맞는다는 이유만으로 v1을 최종
출판식 대신 채택할 수는 없다. 이번 단계는 표시된 Theorem 3.4와 Theorem 1.2 target에서
필요한 항을 직접 다시 유도했다. 그 결과는

\[
q\frac{R^*(x,T,q)}x(\log x)^{\alpha_2}
\le
\frac{R^*(x,T,q)}x(\log x)^{\alpha_1+\alpha_2}
=\frac{R^*(x,T,q)T}{x(\log x)^3},
\tag{38.1}
\]

여기서 \(q\le(\log x)^{\alpha_1}\),
\(T=(\log x)^{\alpha_1+\alpha_2+3}\)다. (38.1)은 source의 오자를 고쳐 썼다고
가정한 식이 아니라, 정리의 target과 per-character remainder에서 직접 나온 project bridge다.

그러나 \(R^*\)의 모든 구성항에 대해 growing
\(\alpha_1=A=100r^2+10\), \(\alpha_2=A-3\)에서 한 uniform 상계를 아직 만들지 않았다.
따라서 numerical \(C_A\), full absorption, H1(2), P9.2와 \(X_{\mathrm{cert}}\)는 열려 있다.

## 2. 쉬운 설명

논문은 “각 계산에서 생기는 오차를 한 상자 \(C\) 안에 넣는다”고 말한다. 그런데 상자에
넣기 전에 나눠야 하는 전체 크기 \(x\)가 최종 인쇄식에서 빠져 있고, 상자의 시작 위치도
\(X_0\)와 \(\log\log X_0\)가 섞여 있다. 그래서 인쇄식 그대로 계산하면 유한한 상자가
아니게 된다.

이번 작업으로 “정말 상자에 들어가야 할 remainder의 크기”는 (38.1)로 복원했다. 아직
상자의 실제 최대 크기를 계산한 것은 아니다. 다음에는 Theorem 3.4의 세부 오차를 하나씩
안전하게 덮는 상계를 만들어야 한다.

## 3. 원문 버전 대조

### 3.1 최종 NYJM판

[Bordignon 2021 최종 출판본](https://nyjm.albany.edu/j/2021/27-54v.pdf)은 다음을 인쇄한다.

- Theorem 1.2, pp. 1416--1417:
  \(Y_0=\log\log X_0\), \(x\ge X_0\), 상수 \(C(\alpha_1,\alpha_2,Y_0)\).
- Lemma 3.1, p. 1420:
  \(T=(\log x)^{\alpha_1+\alpha_2+3}\)이고 explicit-formula remainder가
  \(R(C,\alpha_2,\alpha_1)x\log x\log\log x/T\) 꼴.
- Theorem 3.4, pp. 1425--1429:
  \(|\psi(x,\chi)-\delta(\chi)x|\)의 absolute remainder \(R^*(x,T,q)\).
- 식 (33), p. 1433:
  바깥 조건 \(x\ge Y_0\), 첫 항 \(R^*\log\log x/\log^2x\).
- Theorem 1.4와 식 (35), pp. 1417--1418, 1434:
  \(C(A,A-3,X_0)\)를 Theorem 1.2에서 가져온다고 씀.

### 3.2 arXiv v1 저자 source

[arXiv:2101.08610v1](https://arxiv.org/abs/2101.08610)도 \(X_0/Y_0\) 충돌을 갖지만
상수식 첫 항은

\[
\frac{R^*(x,T,q)T}{x\log^2x}
\]

다. 이것은 dimensionless이나 (38.1)보다 \(\log x\) 하나 큰 보수적 식이고, 최종
Lemma 3.1의 개선식과 그대로 동일하지 않다. 최종판이 다른 center와 다른 remainder를
사용하므로 v1 식을 선택적으로 가져오지 않는다.

NYJM 공식 페이지·PDF, arXiv record/source 및 표적 web 검색에서 별도 erratum이나 저자
계산 코드를 찾지 못했다. 이는 제한된 검색 결과이며 전 세계 비존재 주장이 아니다.

## 4. type-safe threshold 표기

변수의 물리적 의미를 분리해

\[
\widehat C(\alpha_1,\alpha_2;X_0)
=\sup_{x\ge X_0}\sup_{1\le q\le(\log x)^{\alpha_1}}
\mathcal E(x,q)
\tag{38.2}
\]

라 쓴다. \(Y_0\)를 쓰려면 오직

\[
C(\alpha_1,\alpha_2,Y_0)
=\widehat C(\alpha_1,\alpha_2;\exp(\exp Y_0))
\tag{38.3}
\]

로 정의한다. 코드도 \(X_0\) 자체를 만들지 않고
\(\log X_0=e^{Y_0}\)만 계산한다. 이것은 표기 충돌을 닫지만 \(\mathcal E\)의 상계를
자동으로 주지 않는다.

## 5. exact remainder normalization 유도

Theorem 1.2의 두 번째 target은

\[
-1+x^{-1}\sum_{\chi\bmod q}|\psi(x,\chi)|.
\]

principal character의 \(x\)를 빼고 triangle inequality를 쓰면 Theorem 3.4 remainder는
문자 수마다 하나 생긴다. \(\varphi(q)\le q\)를 쓰면 contribution은

\[
qR^*(x,T,q)/x.
\]

이를 \(C/(\log x)^{\alpha_2}\) 꼴과 비교하려면 \((\log x)^{\alpha_2}\)를 곱한다.
그 결과가 (38.1)이다. 이 대수에는 Lemma 3.1의 중간 상수나 인쇄된 식 (33)이 필요 없다.

## 6. 왜 최종 식 (33)을 그대로 쓸 수 없는가

Theorem 3.4의 \(R^*\)에는 \(x/(T-1)\)에 곱해진 zero-count 항과
\(\sqrt x\), \(x/T\) 크기의 항들이 포함된다. \(T\)는 \(x\)가 아니라 log-power다.
따라서 \(R^*\log\log x/\log^2x\)에는 절대 크기 \(x\)가 남아 unbounded \(x\) 범위의
finite constant가 될 수 없다. 단순히 “단위가 이상해 보인다”가 아니라 Theorem 3.4의
표시된 양과 상수 정의가 서로 맞지 않는다.

## 7. actual growing-A 적용의 남은 문제

actual 값은

\[
\alpha_1=A=100r^2+10,\qquad \alpha_2=A-3,\qquad
T=(\log x)^{2A}.
\]

출판 Appendix 표는 작은 고정 \(\alpha_1,\alpha_2\) 값만 제공하므로 이 범위를 덮지 않는다.
필요한 다음 증명은 다음과 같다.

1. Theorem 3.4의 \(R_2,R_3,R_5,R_7,R_8,r_4,R_{11}\)을
   \(q\le(\log x)^A\), height \((\log x)^{2A}\)에서 모두 upper-bound 한다.
2. (38.1)과 식 (28)--(32)의 zero contribution을 합쳐 하나의 \(C_A(X_0)\)를 만든다.
3. 이 상계가 H1c-1b.2의 12항과 H1c-1b.3 count transfer에 허용되는 예산보다 작은
   공통 cutoff를 증명한다.

## 8. fail-closed 구현

검산 모듈은 다음만 수행한다.

- \(Y_0\leftrightarrow\log X_0\) type-safe 변환;
- exact q-dependent contribution과 q-envelope의 log-scale 계산;
- \(T=(\log x)^{\alpha_1+\alpha_2+3}\)를 이용한 두 표현의 동일성 검사;
- 인쇄식에서 numerical \(C\)를 요구하면 예외를 발생시킴;
- 상위 theorem·threshold closure flag를 모두 false로 유지.

actual prime, maximal-gap dataset 또는 장시간 수치 sweep는 실행하지 않는다.

## 9. 다음 gate

1. **H1c-1b.4b density·\(c_0,c_1\)**: exact half-open \(P_T\) lower bound와
   Bordignon의 두 elementary constant를 독립적으로 닫는다.
2. **H1c-1b.4c conditional absorption budget**: numerical \(C_A\)가 얼마 이하여야
   full rate가 닫히는지 모든 12항·count 비용으로 역산한다.
3. **H1c-1b.4d Theorem 3.4 growing-A reproof**: 1--2가 요구하는 \(C_A\)를 실제 source
   terms로 만족시키는지 증명한다.

```text
X0/Y0 type mapping                         = CLOSED
Theorem 3.4 -> Theorem 1.2 direct algebra = CLOSED
final equation (33) numerical use          = REJECTED AS PRINTED
arXiv v1 formula adopted as final           = NO
numerical C_A upper                         = OPEN / SOURCE REPROOF REQUIRED
density / full absorption                   = OPEN
Hypothesis 1(2) / P9.2 / SIV-08 / X_cert   = OPEN
```
