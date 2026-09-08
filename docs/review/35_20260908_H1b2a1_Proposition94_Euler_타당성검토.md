# H1b-2a.1 Proposition 9.4 exact Euler normalization 타당성검토

- 검토일: 2026-09-08
- 대상: Maynard Proposition 9.4 식 (9.61)--(9.67)의 숨은 Euler normalization
- 판정: EXACT_EULER_COMPONENT_VALID_AND_FINITE_PARENT_PROPOSITION_OPEN
- 이론 정본: [29_Sono_FMT_H1b2a1_Proposition94_exact_Euler_normalization.md](../method/theory/29_Sono_FMT_H1b2a1_Proposition94_exact_Euler_normalization.md)

## 1. 사용자 관점의 결론

이번 단계는 타당하며, 원문에서 “고정 상수 정도”로 생략한 마지막 소수별 곱을 실제
상수식으로 바꿨다. 가장 보수적인 전체 Euler multiplier는

\[
e^{2+6/k},
\]

이고 현재 최소 \(k=36\)에서 약 8.73이다.

그러나 “Sono/FGKMT 부등식이 특정 \(X\)부터 성립한다”는 최종 결론은 아직 아니다.
Proposition 9.4의 분포 오차와 다른 moment들의 공통 예산이 남아 있기 때문이다.

## 2. 원문을 잘못 읽을 위험은 없었는가

두 가지 식 번호를 정정해야 했다.

- 앞쪽 \(O(1)\) 곱은 식 (9.63)이 아니라 (9.64)에 표시된다.
- 마지막 두 곱은 식 (9.67)이 아니라 (9.66)에 표시되고, (9.67)은 그 곱을 흡수한 결론이다.

출판 PDF pp.1549--1550을 시각 확인하고 author TeX lines 1120--1153과 대조했다.
수학적 대상은 이전 계획과 같으므로 연구 방향이 바뀐 것은 아니며 locator만 정밀해졌다.

## 3. exact factor 복원은 타당한가

타당하다. \(p+O(k)\)를 거꾸로 추측하지 않았다. 바로 앞 식 (9.61)의

\[
\frac{(p-\omega^*(p))^2}{p+\omega^*(p)-2}
\]

를 Lemma 8.4의 \(g(p)\)로 그대로 사용했다. \(\omega^*=\omega\)인 충돌 소수와
\(\omega^*=\omega+1\)인 새-root 소수를 분리해 통분했으며, 양변은 Python Fraction
회귀검사로 독립 비교했다.

## 4. 무한 곱을 유한 상수로 바꾸는 논리는 타당한가

타당하다. 세 local excess는 각각

\[
\frac{4k}{p^2},\qquad \frac{4k}{p^2},\qquad \frac{4k^2}{p^2}
\]

이하이다. 모든 관련 소수는 \(p>2k^2\)이고,

\[
\sum_{p>2k^2}\frac1{p^2}
\le\sum_{n>2k^2}\frac1{n^2}
\le\frac1{2k^2}
\]

이므로 로그를 합해 각각 \(2/k,2/k,2\)를 얻는다. 소수 정리나 수치 fitting에
의존하지 않는 보수적인 elementary 상계다.

임의 cutoff \(Y\ge2k^2\)에서도 tail을 \(1/Y\)로 닫았기 때문에, 나중에 실제
\(\omega(p)\) head를 계산하더라도 누락 없는 certificate로 확장할 수 있다.

## 5. singular series 방향은 맞는가

맞다. 두 번째 곱을 나누는 기준은

\[
\mathfrak S_{WB}(\mathcal L)^{-1}
=\prod_{p\nmid WB}
\left(1+\frac{\omega(p)}{p-\omega(p)}\right)
\left(1-\frac1p\right)^k.
\]

두 local 비율은 모두 1 이상의 exact 유리수이고 위에서 \(1+4k^2/p^2\)로 상계했다.
따라서 방향은

\[
P_{\rm can}\le e^2\mathfrak S_{WB}^{-1}
\]

이며 역수 방향을 뒤집지 않았다. 이 역수가 식 (9.66)의 기존
\(\mathfrak S_{WB}^2\) 중 하나를 상쇄해 원문 식 (9.67)의
\(\mathfrak S_{WB}\) 하나가 남는 구조와도 일치한다.

## 6. 누락 또는 과소계상 위험

가장 위험한 항은 식 (9.64)의 \(C_{\rm pre}\)가 식 (9.65)의
\(y_{\mathbf r,r_0}\)에 한 번 들어간 뒤 제곱합에서 두 번 들어간다는 점이다.
이를 빠뜨리지 않고 \(C_{\rm pre}^2\le e^{4/k}\)로 계산했다.

또 \((r,r_0)=1\)을 버리고 합을 분리하는 단계는 모든 항이 비음수인 upper-bound
방향에서만 사용했다. 따라서 누락이나 상계 방향 역전은 없다.

## 7. 선행연구 우선 조사 결과

확인한 1차 자료는 다음과 같다.

1. Maynard 최종 출판본과 arXiv:1405.2593 v2 author source
2. 같은 Maynard weight를 다른 upper moment에 쓰는 Mastrostefano,
   [arXiv:1804.06290](https://arxiv.org/abs/1804.06290)

표적 검색에서 이번 두 곱을 그대로 수치화한 정식 replacement나 공식 erratum은
확인하지 못했다. 따라서 기존 정리를 잘못 재증명했다고 주장하지 않고, 원문에서
생략된 이 연결부만 project finite lemma로 표시했다. 검색 결과는 전 세계 문헌의
비존재 또는 novelty 판정이 아니다.

## 8. 이번에 닫힌 것과 열려 있는 것

| 항목 | 판정 |
|---|---|
| exact \(g_*(p,\omega^*)\) 복원 | 닫힘 |
| 식 (9.64) \(C_{\rm pre}\) 및 제곱 보정 | 닫힘 |
| 식 (9.66) sharp \(r_0\) Euler product | 닫힘 |
| 식 (9.66) canonical product / singular-series 비교 | 닫힘 |
| 식 (9.52) distribution error | 후속 H1b-2a.2에서 actual child 닫힘; 일반 \(\mathcal A\)는 별도 |
| Proposition 9.4 전체 | 열림 |
| Proposition 6.1 전체와 SIV-07 | 열림 |
| numerical \(X_{\rm cert}\) | 열림 |

## 9. 다음 순서

### 1순위: H1b-2a.2 식 (9.52) distribution error

Proposition 9.1의 생략된 동일 논증을 actual tuple count와 finite Lemma 8.5
coefficient bound로 복원한다. 다만 Hypothesis 1(1),(3)의 숫자 multiplier는
H1c-1 입력으로 남겨야 한다. 예상 6--15시간의 Codex 수학·source 감사다.

> **후속 결과:** actual \(\mathcal A=\mathbb Z\)에서는 exact
> \(E_q^{(1)}\le1\)을 쓸 수 있어 Hypothesis 1(1),(3) multiplier 없이 이 child를
> 닫았다. 상세는 [theory 30](../method/theory/30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md)과
> [review 36](36_20260908_H1b2a2_Proposition94_distribution_타당성검토.md)이다.

### 2순위: H1c-1 quantitative character/Bombieri--Vinogradov package

FGKMT Lemma 7.2가 호출하는 character-sum과 prime-distribution 상수의 원천·유효범위를
수치화한다. 이는 Proposition 9.2와 전체 good-weight theorem에 필요하지만 actual 식
(9.52)의 선결조건은 아니다. 예상 1--3일 이상의 문헌·증명 감사이며, 실제 난도에 따라 더
길 수 있다.

### 3순위: H1b-2b 공통 moment budget

H1b-2a.3에서 먼저 P94 내부의 닫힌 package를 한 multiplier·cutoff로 합성한다. 이후
H1c-1과 다른 moment 입력이 마련되면 Propositions 9.1--9.5 전체를 한 cutoff에서
동시에 지배하도록 합성한다.

## 10. 사용자 요청사항

별도 수행절차 필요없음. 다음 단계도 우선은 문헌·수학 감사이므로 추가 CPU, RAM,
Lean 또는 Python package 설치를 요청하지 않는다.

## 11. H1b-2a.3 완료 뒤의 후속 판정

9절의 P94 내부 합성은 후속
[theory 31](../method/theory/31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md)에서
완료됐다. 이 문서의 Euler normalization은 정확히 한 번만 사용됐고, actual FGKMT/FMT
`H1B-P94`는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 승격됐다. 일반 P94와
`H1B-COMP-01`, `SIV-07/09`, \(X_{\rm cert}\)의 판정은 변하지 않는다.
