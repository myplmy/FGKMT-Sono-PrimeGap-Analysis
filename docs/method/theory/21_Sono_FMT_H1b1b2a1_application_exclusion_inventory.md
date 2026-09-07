# Sono/FMT H1b-1b-2a.1 actual application-exclusion 전수감사

- 작성일: 2026-09-07
- 상위 정식화:
  [H1b-1b-2a local-factor·base-W 하한](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
- 상위 원장:
  [H1b-1b-2 c-gamma 오류 정규화](19_Sono_FMT_H1b1b2_cgamma_error_normalization_ledger.md)
- 기계 계약:
  [Sono_FMT_H1b1b2a1_application_exclusion_inventory_v1.json](data/Sono_FMT_H1b1b2a1_application_exclusion_inventory_v1.json)
- 검증 구현: `source/h1b1b2_local_factor_lower_bound.py`

## 1. 판정부터 요약

Maynard Section 8의 Lemma 8.4 외부 호출 8곳과 Lemma 8.3 직접 호출 2곳을
원문에서 다시 찾았다. 1135행의 한 호출은 서로 다른 cutoff를 쓰는
`r_0` 한 변수 factor와 canonical `r`-vector factor로 분리되므로,
기계 원장에는 11개 analytic subapplication을 등록했다.

각 subapplication의 effective excluded integer에서 실제로 필요한 것은 정수 자체의
중복도보다 소인수 집합이다. 따라서

\[
Q^\sharp=\operatorname{rad}(Q)
\]

를 사용한다. 모든 추적 호출에서 다음 중 하나가 성립한다.

1. `Q^\sharp`가 canonical bad-prime upper `U_W` 이하이다.
2. `Q^\sharp`가 `U_WR` 이하이다.

두 번째 경우는 620행의 `d`, 995행과 1015행의 고정된
`r`에 한정되며, 각각 support 때문에 `d<=R` 또는 `r<=R`이다.

따라서 11개 subapplication 모두의 application overhead를 닫을 수 있고,
한 번에 쓸 수 있는 공통 상계는

\[
\boxed{
\Lambda_*=
2k^2\log(2k^2)+k(k-1)\log2+
\left\{
\frac{10\alpha(2k^2-k+1)}{\theta}+k
\right\}\log R
}
\]

이다. 이는 620행, 첫 iteration에서 최악값을 갖는다.

그러므로 추적된 actual call 전체에서

\[
\boxed{
c_{\gamma,j}>
\frac{1}{3(1+\log\Lambda_*)}
}
\]

라는 **parameterized explicit lower bound**를 사용할 수 있다.

다만 이 결과는 `C3_abs(A1,A2)`의 숫자, Lemma 8.3의 finite range,
실제 `A1,A2,L`, 수정된 `r`-회 오차 합성을 제공하지 않는다.
따라서 Lemma 8.4 전체 numerical package, `SIV-07`,
`X_cert`는 계속 OPEN이다.

## 2. 1차 source와 호출 완전성

James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
arXiv:1405.2593.

- 검토 source: `tmp/pdfs/h1b1b/maynard_source/Subsets.tex`
- SHA-256:
  `e55592f0d674e32ad6ef7d6fe25bce2a0aa3cfc712981ccf996a5df0a4d5b18e`
- Lemma 8.3 정의: 531--540행
- Lemma 8.4 정의·귀납: 542--604행
- Lemma 8.4 외부 호출: 620, 737, 752, 885, 905, 995, 1135, 1232행
- Lemma 8.3 외부 직접 호출: 1015, 1096행

558, 568, 581, 591행은 Lemma 8.4 자체의 증명 내부 호출이므로
actual application 수에 다시 넣지 않는다. 1135행은 표시된 이중곱을
`r_0` factor와 `r`-vector factor로 나눠 기록한다.

## 3. 공통 canonical upper

Maynard 385행의 bad-prime integer를

\[
D_{\mathcal L}=
\prod_{i=1}^{k}|a_i|
\prod_{i\ne\ell}|a_i b_\ell-b_i a_\ell|
\]

라 하자. 396--407행의 구성에서 canonical `W_i`의 소인수는
`WBD_mathcalL`의 소인수 안에 있다. `W_i`가 square-free이므로

\[
W_i\le\operatorname{rad}(WBD_{\mathcal L})\le WBD_{\mathcal L}.
\]

계수 조건과 `R>=x^(theta/10)`을 사용하면

\[
\boxed{
U_W=
(2k^2)^{2k^2}2^{k(k-1)}
R^{10\alpha(2k^2-k+1)/\theta}
}
\]

이고 모든 canonical `W_i<=U_W`다.

`WB`는 모든 `p<=2k^2`를 포함한다. `p`가 `B`를
나누지 않으면 `W`에, 나누면 `B`에 들어가기 때문이다.

## 4. actual subapplication 표

아래 `delta`는 `Q^sharp<=U_W R^delta`에서의 지수다.

| ID | source | 차원 | effective 제외모듈 | delta | 판정 |
|---|---|---:|---|---:|---|
| L620-dW | 620 | k | rad(d W_i) | 1 | d<=R |
| L737-canonical | 737 | k | W_i | 0 | canonical |
| L752-canonical | 752 | k | W_i | 0 | canonical |
| L885-Wprime | 803--805, 885 | k-1 | W_i' | 0 | determinant가 D_mathcalL에 이미 포함 |
| L905-Wprime | 803--805, 905 | k-1 | W_i' | 0 | 동일 |
| L995-aWBr | 939--995 | 1 | rad(a_m W B r) | 1 | a_m W B support는 base, r<=R |
| L1015-rWm | 939--1020 | 1 | rad(r W_m) | 1 | r<=R |
| L1096-W0 | 1045--1098 | 1 | rad(D_aux V Delta_L) | 0 | 별도 크기식이 U_W 이하 |
| L1135-W0 | 1114--1141의 r_0 factor | 1 | rad(W_0) | 0 | L1096과 같은 W_0 |
| L1135-canonical | 1114--1141의 r-vector factor | k | W_i | 0 | canonical |
| L1232-canonical | 1228--1237 | k | W_i | 0 | canonical |

여기서 885·905행에서는 `m` 좌표가 `r_m=1`로 빠진다.
803행의 `W'_m`을 형식적으로 만들면 자기 determinant가 0이 되지만,
실제 다중합은 `i!=m`인 `k-1`개 좌표만 사용하므로
`W'_m`은 application input이 아니다.

## 5. 확대인자별 증명

### 5.1 620행: d W_i

`lambda_d`의 support에서

\[
d=\prod_i d_i\le R.
\]

따라서

\[
\operatorname{rad}(dW_i)\le dW_i\le RU_W.
\]

모든 iteration의 추가 비용은 `eta=log R` 이하이다.

### 5.2 885·905행: W_i prime

`i!=m`에서

\[
W_i'=\operatorname{rad}
\{W_i(a_i b_m-a_m b_i)\}.
\]

추가 determinant `a_i b_m-a_m b_i`는
`D_mathcalL`의 ordered factor 중 하나다. 따라서

\[
\operatorname{supp}(W_i')
\subseteq\operatorname{supp}(WBD_{\mathcal L}),
\qquad
W_i'\le U_W.
\]

별도 크기 비용은 없으며 `eta=0`이다. 이는 determinant를 무시한 것이 아니라
base upper가 이미 모든 ordered determinant를 포함한다는 뜻이다.

### 5.3 995·1015행: 고정 r

995행의 `a_m`은 `D_mathcalL`의 첫 곱에 들어가고
`WB`도 base support에 들어간다. 그러므로

\[
\operatorname{rad}(a_mWBr)\le U_W\operatorname{rad}(r).
\]

939--981행에서 `r`은 `lambda_d` 또는 `y_e` support의
약수이며 전체 support가 `d,e<=R`이므로 `r<=R`이다. 따라서

\[
\operatorname{rad}(a_mWBr)\le U_WR.
\]

1015행도 같은 고정 `r<=R`과 canonical `W_m`을 사용하므로

\[
\operatorname{rad}(rW_m)\le U_WR.
\]

두 호출의 `eta`는 모두 `log R`이다.

### 5.4 1096·1135행: W_0

이 절의 `D_aux`는 `D_mathcalL`과 다른 입력이며
Proposition S3에서 `D_aux<=x^alpha`다. 또한

\[
V=\prod_{p\le2k^2}p\le(2k^2)^{2k^2}
\]

이고

\[
\Delta_L=
|a_0|\prod_{i=1}^{k}|a_i b_0-a_0b_i|
\le2^k x^{\alpha(2k+1)}.
\]

따라서

\[
W_0=D_{\rm aux}V\Delta_L
\le(2k^2)^{2k^2}2^k x^{\alpha(2k+2)}.
\]

canonical base upper를 `x`로 쓰면 상수·지수는 각각

\[
k(k-1),\qquad 2k^2-k+1
\]

이고 `W_0` 쪽은

\[
k,\qquad 2k+2
\]

이다. `k>=2`에서

\[
k(k-1)-k=k(k-2)\ge0,
\]

\[
(2k^2-k+1)-(2k+2)=2k^2-3k-1\ge0.
\]

따라서 `W_0<=U_W`이고 `eta=0`이다.
`W_0`는 `V`를 포함하므로 작은 소수 포함 조건도 직접 만족한다.

1135행은 첫 factor에 이 `W_0`를, 두 번째 factor에 canonical
`W_i`를 사용한다. 서로 다른 cutoff의 factor를 하나의 동일-scale 다중합으로
간주하지 않고 각각 위 상계를 적용한다.

## 6. iteration별·공통 Lambda

`s`차원 application의 `j`번째 iteration에서
남은 각 변수는 support 때문에 `e_i<=R`다. 따라서

\[
\log Q^\sharp_{\mathrm{app},j}
\le
2k^2\log(2k^2)+k(k-1)\log2+
\left\{
\frac{10\alpha(2k^2-k+1)}{\theta}
+s-j-1+\delta_{\rm app}
\right\}\log R.
\]

전수표에서 `s<=k`이고 `delta<=1`이다. 두 최댓값을 동시에
갖는 620행의 첫 iteration이 있으므로 공통 최댓값은 정확히

\[
\Lambda_*=
2k^2\log(2k^2)+k(k-1)\log2+
\left\{
\frac{10\alpha(2k^2-k+1)}{\theta}+k
\right\}\log R.
\]

모든 effective modulus는 canonical `WB` 또는 `V`를 포함하므로
`k>=2`에서 `Q^sharp>=210`이다. theory 20의
Rosser--Schoenfeld 변환을 공통 `Lambda_*`에 적용할 수 있다.

## 7. 상태 변화

| obligation | 이전 | 현재 |
|---|---|---|
| H1B1B2-CMIN-LARGE-EXCLUDED | BASE_W_PARAMETERIZED_APPLICATION_OVERHEAD_OPEN | PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS |
| H1B1B2-CMIN-COMPOSE | PARAMETERIZED_EXPLICIT_APPLICATION_INPUT_OPEN | PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS |
| H1B1B2-ROUTE-DECISION | PRIMARY_CANDIDATE_APPLICATION_AUDIT_OPEN | PRIMARY_CORRECTED_KAPPA1_WIRSING_ROUTE_SELECTED |
| H1B1B2-RFOLD-COMPOSITION | HARD_BLOCKER | HARD_BLOCKER |
| SIV-07 | HARD_BLOCKER | HARD_BLOCKER |
| X_cert | OPEN | OPEN |

현재 primary는 교정된 \(\kappa=1\) Wirsing 경로다. 이 inventory가 닫은
`c_gamma` lower-bound normalization은 optional cross-check이며, Lemma 8.4 전체 오차항이
numerical하게 닫혔다는 뜻은 아니다.

## 8. 남은 proof obligation

다음 직접 gate는 H1b-1b-2b다.

1. 교정된 Lemma 8.3 절대오차의 `C3_abs(A1,A2)`를 복원한다.
2. 그 상수의 최초 유효범위와 actual `A1,A2,L`을 수치화한다.
3. 이번 `Lambda_*`를 사용해
   `C4_rel<=6 C3_abs(1+log Lambda_*)`를 만든다.
4. 이 손실을 모든 iteration에 넣어 `r`-회 binomial error를 재합성한다.

그 전에는 threshold calculator를 만들거나 `X_cert` 값을 제시하지 않는다.

## 9. 자동 검증

`tests/test_h1b1b2a1_application_exclusion_inventory.py`는 다음을 확인한다.

- source call-site 10곳과 analytic subapplication 11개의 구분
- application ID와 코드 spec의 일치
- 세 application만 `log R` overhead를 갖고 나머지 8개는 인증된 0인 점
- `W_0` 지수 지배가 모든 `k>=2`에서 성립하는 점
- 각 application·iteration의 상계가 공통 `Lambda_*` 이하인 점
- 공통 최댓값이 620행 첫 iteration과 정확히 같은 점
- application inventory closure가 `C3_abs`, r-fold, `SIV-07`,
  `X_cert`를 승격하지 않는 점

수치 검사는 대수 증명의 대체물이 아니라 구현 회귀검사다.

## 10. 사용자 수행사항

별도 수행절차 필요없음. 새 외부 자료, Lean, 추가 Python 라이브러리,
CPU-heavy 계산은 이번 단계에 필요하지 않았다.

## 11. 2026-09-08 후속 상태

§8의 `C3_abs` 우선순위는 H1b-1b-2b 이전의 역사적 경로다. Ford의 교정
\(\kappa=1\) 정리를 명시화한 뒤 주 경로는 \(C_{8.3}(a,A_2)\)를 직접 사용한다.
이 문서의 11개 application inventory와 공통 \(\Lambda_*\)는 폐기하지 않으며,
공통 actual \(a,A_2,L\)을 인증하고 독립 \(c_\gamma\) 검사를 수행할 때 재사용한다.
