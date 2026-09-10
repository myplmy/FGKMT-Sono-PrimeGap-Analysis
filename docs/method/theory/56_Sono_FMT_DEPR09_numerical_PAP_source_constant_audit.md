# Sono/FMT DEP-R09 numerical PAP source·constant 감사

- 작성: 2026-09-11 KST
- 단계: `DEP-R09 PHASE 1`
- 증거 수준: `SOURCE AUDIT + FINITE ALGEBRA KERNEL CHECK`
- 판정: `CONSTANT_NORMALIZATION_EXPLICIT / ANALYTIC_RATE_AND_CUTOFF_OPEN`
- 기계 원장:
  [`data/Sono_FMT_DEPR09_numerical_PAP_v1.json`](data/Sono_FMT_DEPR09_numerical_PAP_v1.json)
- Lean 정본:
  [`lean/FGKMTSono/TheoryVerification.lean`](../../../lean/FGKMTSono/TheoryVerification.lean)
- 선행:
  [theory 16](16_Sono_FMT_H1c_Hypothesis1_PAP_source_trace.md),
  [theory 48](48_Sono_FMT_H1bDEP_actual_dependency_map.md)

## 1. 결론

Sono가 택한 상수

\[
c_{\rm ZFR}=\frac1{24},\qquad
a=\frac3{10}c_{\rm ZFR}=\frac1{80}
\tag{56.1}
\]

및

\[
c_{\rm ZD}=16,\qquad D_{\rm PAP}=10c_{\rm ZD}=160
\tag{56.2}
\]

에서

\[
aD_{\rm PAP}=2,\qquad
C_{\rm PAP}=1-e^{-2}
\tag{56.3}
\]

이고

\[
0<C_{\rm PAP}<1
\tag{56.4}
\]

이라는 exact algebra는 source와 일치하며 Lean 커널로 독립 검증할 수 있다.

하지만 이것만으로 “모든 \(u\ge q^{160}\)에서 바로 PAP가 성립한다”는 유한 정리가 되지는
않는다. Sono Section 5의 Gallagher·Jutila·Maier 경로에는 `\(\ll\)`, `\(\ll_\varepsilon\)`,
`\(O_\le\)`, `\(o(1)\)`, “sufficiently large”가 남아 있다. 이들의 multiplier와 공통
시작점을 복원해야 비로소 수치 \(u_{\rm PAP}\)를 만들 수 있다.

## 2. 쉬운 설명

`160`은 PAP가 요구하는 **성장률의 모양**이다. 예를 들어 modulus가 \(q\)이면 소수를 세는
상한 \(u\)가 적어도 \(q^{160}\)이어야 한다는 뜻이다. 그러나 논문은 동시에 “충분히 큰
\(u\)”도 요구한다. 그 “충분히 큰” 숫자가 인쇄되어 있지 않다.

따라서 `160`은 자동차의 최소 기어비와 비슷하고, 아직 빠진 \(u_{\rm PAP}\)는 실제로 시동이
걸리는 최저 온도와 비슷하다. 기어비만 알아서는 시동 온도를 계산할 수 없다.

## 3. source 대조와 PDF 판독 방식

| 원천 | 확인 위치 | 판독 | 현재 판단 |
|---|---|---|---|
| Sono 2025 | pp. 534--537, Prop. 5.1--5.3, (5.2)--(5.7) | native text 후 원 페이지 이미지 대조 | 상수와 proof chain 확인 |
| Ford--Maynard--Tao 2018 | pp. 4--5, Lemma 2.2 | native text 후 원 페이지 대조 | PAP의 비수치 선행형 확인 |
| Jutila 1977 | p. 46, Theorem 1, (1.7)--(1.8) | scan PDF라 OCR로 위치 탐색 후 원 페이지 이미지 대조 | \(\varepsilon\)-의존 `\(\ll_\varepsilon\)` 확인 |
| McCurley 1984 | Theorems 1--2 | Sono의 정확한 전사와 서지 metadata | 원문 subsidiary range 재감사 필요 |
| Gallagher 1970 | Theorems 6--7, (26), (30) | 서지·Sono 인용만 확인 | full source 미확보 |
| Maier 1981 | Lemma 2 | FMT·Sono의 인용만 확인 | full source 미확보 |

Jutila 공개 scan은 SHA-256
`f6e9038a7216b690763692e0a07bc8c58284c9560bf62ab987ea62a817404ad5`로 임시 보존했다.
해당 PDF에는 사용할 수 있는 텍스트층이 없어 OCR은 탐색용으로만 썼고, Theorem 1은 원 페이지
이미지에서 직접 대조했다. 반대로 Sono와 FMT는 native text를 먼저 사용했다.

ScienceDirect의 McCurley·Maier 직접 PDF 요청은 현재 환경에서 HTTP 403으로 실패했다.
Springer의 Gallagher 원문은 구독 콘텐츠로 표시된다. 이 세 원문을 확보하기 전에는 하위
정리의 정확한 quantifier와 상수를 추측하지 않는다.

## 4. Jutila exponent의 정확한 재매개화

Jutila Theorem 1은 \(4/5\le\alpha\le1\), \(T\ge1\)에서

\[
N^*(\alpha,T,Q)\ll_\varepsilon
  (Q^2T)^{(2+\varepsilon)(1-\alpha)}
\]

를 준다. \(Q=T\)를 넣으면 밑의 지수는 \(3(2+\varepsilon)\)이다. Sono가 쓰는
`\(6+\varepsilon\)` 표기는 source의 epsilon을 다시 이름 붙인 것이다. 정확한 대입은

\[
3\left(2+\frac{\varepsilon}{3}\right)=6+\varepsilon
\tag{56.6}
\]

이다. 이 변경은 지수에는 문제가 없지만 implied multiplier도
`\(C_{\varepsilon/3}\)`로 바뀐다. 그 값을 `1`로 둘 수 없다.

낮은 \(\alpha\) 구간의 trivial exponent는 \(\alpha\le4/5\)일 때

\[
3\le15(1-\alpha)
\tag{56.7}
\]

로 설명된다. 여기에도 \(T\log T\)와 character 수를 흡수하는 finite cutoff와 multiplier가
필요하다. `\(c_{\rm ZD}=16\)`은 이 두 구간을 asymptotic Vinogradov 표기 안에서 묶는
충분한 exponent이며, multiplier 1이나 최초 \(T\)를 뜻하지 않는다.

## 5. finite PAP가 실제로 요구하는 slack

Sono Assumption 3.2의 결론은 \(C_{\rm PAP}(1+o(1))\)이다. 부호가 정해지지 않은
`\(o(1)\)`을 유한 \(u\)에서 제거하려면 양의 slack을 따로 잡아야 한다. 가장 안전한
project contract는 \(0<\eta_{\rm PAP}<C_{\rm PAP}\)를 고정하고

\[
\pi(u;q,r)\ge
  \bigl(C_{\rm PAP}-\eta_{\rm PAP}\bigr)
  \frac{u}{\varphi(q)\log u}
\quad
\left(
  u\ge\max\{u_{\rm PAP}(\eta_{\rm PAP}),q^{160}\}
\right)
\tag{56.8}
\]

를 증명하는 것이다. residue \(r\)는 \((r,q)=1\)이고, 필요한 zero-free·exceptional
modulus 조건도 같은 quantifier 안에 둬야 한다.

예를 들어 정규화된 main term을 \(M\ge0\)라 하고 principal contribution과 error가

\[
P\ge(1-\eta)M,\qquad |E|\le e^{-2}M
\]

를 만족하면 exact하게

\[
P+E\ge(1-e^{-2}-\eta)M
\tag{56.5}
\]

이다. 이 합성은 Lean에서 닫히지만, 두 premise의 analytic 증명과 최초 \(u\)는 닫히지
않는다. 최종 Sono 계수 \(2\times10^{-17}\)를 그대로 보존하려면 이 slack을 DEP-R11의
전체 coefficient budget에 넣어야 한다. R09에서 임의로 0으로 놓지 않는다.

## 6. DEP-R09 하위 의무

| ID | 의무 | 현재 상태 | 다음 증거 |
|---|---|---|---|
| R09-01 | McCurley zero-free·예외 zero의 모든 finite range | `PARTIAL_SOURCE` | 원문 정리·case audit |
| R09-02 | Gallagher (5.2)의 multiplier, \(a,b\), 전 parameter range | `SOURCE_REQUIRED` | Gallagher 원문 정량 재증명 |
| R09-03 | Jutila Theorem 1의 \(C_\varepsilon\)와 finite proof range | `SOURCE_FORM_CONFIRMED_RATE_OPEN` | proof constant ledger |
| R09-04 | high/low \(\alpha\)를 \(c_{\rm ZD}=16\)으로 묶는 finite bridge | `PARTIAL` | R09-03 multiplier·cutoff |
| R09-05 | Maier Lemma 2의 density-to-PNT transfer | `SOURCE_REQUIRED` | 원문 lemma 전수 감사 |
| R09-06 | principal contribution의 one-sided rate | `OPEN` | explicit PNT term |
| R09-07 | nonprincipal `O_<=`의 최초 \(u\)와 예외 case | `HARD_BLOCKER` | R09-02--05 합성 |
| R09-08 | \(\psi\to\pi\), prime powers, partial summation, endpoints | `OPEN` | finite one-sided lemma |
| R09-09 | actual modulus·\(B_0\)·construction-variable uniformity | `OPEN` | Sono Lemma 3.7 mapping |
| R09-10 | 공통 \(u_{\rm PAP}(\eta)\) certificate | `HARD_BLOCKER` | R09-01--09 전체 |

## 7. Lean 검증 범위

식 (56.1)--(56.7)의 exact algebra와 finite error implication은 project-local axiom,
`sorry`, `admit` 없이 한 Lean 파일에서 검증한다. 식 (56.8)은 앞으로 증명해야 할 analytic
source contract이므로 `SOURCE_THEOREM_UNFORMALIZED`다.

Lean이 증명하는 것은 숫자 대입과 오차항의 방향이다. Lean에 Gallagher·Jutila·Maier 정리를
premise 없이 새로 만들어 넣지 않으며, 이 단계의 kernel PASS를 PAP 전체의 PASS로 확대하지
않는다.

## 8. 다음 gate

1. Gallagher 1970과 Maier 1981 원문, 가능하면 McCurley 1984 원문을 확보한다.
2. R09-02와 R09-05를 equation-by-equation constant ledger로 분해한다.
3. source proof가 실제로 effective한 각 항은 multiplier·cutoff 식으로 만들고, 단순
   존재상수만 남는 항은 `SOURCE_THEOREM_UNFORMALIZED`로 차단한다.
4. 그 뒤 R09-06--08의 one-sided finite PAP를 합성한다.
5. R09-10이 닫히기 전에는 threshold calculator, 장시간 prime 계산, `PAP-11=EXPLICIT`,
   `X_cert` 확정을 하지 않는다.

## 9. 참고문헌·원문 경로

- Keiju Sono, [An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes](https://doi.org/10.4418/2025.80.2.2).
- Kevin Ford, James Maynard, Terence Tao,
  [Chains of Large Gaps Between Primes](https://arxiv.org/abs/1511.04468).
- M. Jutila, [On Linnik's Constant](https://doi.org/10.7146/math.scand.a-11701).
- P. X. Gallagher,
  [A Large Sieve Density Estimate near sigma=1](https://doi.org/10.1007/BF01403187).
- H. Maier,
  [Chains of Large Gaps Between Consecutive Primes](https://doi.org/10.1016/0001-8708(81)90003-7).
- K. S. McCurley,
  [Explicit Zero-Free Regions for Dirichlet L-functions](https://doi.org/10.1016/0022-314X(84)90089-1).
