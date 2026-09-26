# Review 99 — DEP-R09 blind fixed-modulus reduction 타당성검토

- 검토대상: Theory 90, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>IMPRIMITIVE_REDUCTION_VALID /
  CORRECTION_GATE_VALID /
  NATIVE_SOURCE_RANGE_REJECTION_VALID</code>

## 1. 검토 결론

Theory 90의 판정은 타당하다.

1. blind lifted character sum은 native modulo-\(f\) sum에서 \(p\mid h\) prime powers만
   제거한 exact identity다.
2. correction은 character별 \(\omega(h)\log U\) 이하이고 flexible energy transfer가
   성립한다.
3. \(\eta=1\) quarter-budget은 native energy와 correction을 strict target 안에
   합성하는 충분조건이다.
4. actual fixed-modulus exponent는 \(21\le d_f<416\)이다.
5. Bennett cutoff는 최소 coarse exponent 900을 요구하므로 겹치지 않는다.
6. Vaughan unconditional range와 GRH theorem, Friedlander--Goldston conditional
   upper도 current unconditional numerical input이 아니다.

따라서 imprimitive correction은 parameterized finite gate로 분리됐고, 실제 blocker는
native prescribed-\(f\) energy 또는 direct blind correlation이다.

## 2. prime-power identity

\(\widetilde\psi=\psi\otimes\chi_{0,h}\)에서 \(p\nmid h\) prime powers는 native와
lifted sum에 똑같이 들어간다. \(p\mid h\)에서는 lifted principal factor가 0이다.
따라서

\[
Z_{\widetilde\psi}^{(\mathfrak q)}
=Z_\psi^{(f)}-D_{\psi,h}
\]

가 exact하다. \(\Lambda\) support가 prime powers라는 사실 때문에 composite
cross terms는 없다.

각 \(p\mid h\)는 최대 \(\lfloor\log U/\log p\rfloor\)개 power를 내고 각 weight는
\(\log p\)이므로 prime당 절댓값 합은 \(\log U\) 이하이다.

## 3. energy와 quarter budget

\[
|a-b|^2\le(1+\eta)|a|^2+(1+\eta^{-1})|b|^2
\]

를 character마다 합하면 Theory 90 식 (90.8)이 나온다. \(\eta=1\)에서 native와
correction energy를 각각 \(G_{\rm blind}/4\) 미만으로 두면 transfer 뒤 각각
\(G_{\rm blind}/2\) 미만이므로 합이 strict하게 \(G_{\rm blind}\)보다 작다.

correction absorption 식 (90.15)은 분모를 양수로 곱한 exact equivalent sufficient
condition이다. 최종 \(\tau_{\rm blind}\) allocation 전에는 숫자 cutoff가 아니다.

## 4. effective exponent

\[
d_f=d\frac{\log\mathfrak q}{\log f}.
\]

\(\log\mathfrak q<21X/20\), \(\log f>47X/100\)에서

\[
d_f<\frac{105}{47}d.
\]

\(d\le186\)이면 upper는 \(19530/47<416\)이다. \(f\le\mathfrak q\)에서
\(d_f\ge d\ge21\)도 맞다.

## 5. source applicability

- Bennett pointwise theorem은 \(f>10^5\)에서 source cutoff를 보장하려면
  \(d_f\ge900\)이라는 더 약한 필요조건부터 요구한다. actual upper 416과 불일치한다.
- Vaughan Theorem 1은 fixed-\(A\) near-\(U\) dyadic modulus moment이며
  \(f=U^{1/d_f}\) prescribed family를 덮지 않는다.
- Vaughan Theorem 2는 GRH와 exponent \(3/4+\varepsilon\)를 요구한다.
- Friedlander--Goldston fixed-\(f\) upper는 GRH·implicit이며 unconditional numerical
  정본에 넣을 수 없다.

modulus가 full primorial보다 작아졌다는 사실만으로 기존 theorem의 cutoff가 자동
충족된다고 하지 않은 판정이 타당하다.

## 6. raw large-sieve 경계

native quarter-gate는 favorable factor에서도 \(O(U^2)\)보다 작다. 반면 Theory 83의
raw certificate는 \(d_f\ge21\)에서 \(5(\log f)U^2\)보다 크다. 따라서 그 upper 하나로
strict native gate를 증명할 수 없다.

이는 actual native energy의 하한이 아니며 fixed-\(f\) prime-specific cancellation을
배제하지 않는다.

## 7. 검증 경계

Python은 symbolic prime-power fixture, energy transfer, strict quarter budgets와 rational
exponent range를 exact하게 검사한다. actual prime list나 threshold를 만들지 않는다.

Lean은 source premise 뒤 scalar implication만 검사한다. Vaughan·Bennett·
Friedlander--Goldston theorem과 actual character energy를 local axiom으로 넣지 않는다.

canonical 회귀시험 48개, Lean direct compile·full build와 전수 verification
refresh가 모두 PASS했다. 최종 inventory는 theory 91개, display 식 1,763개,
declaration 329개, 금지 proof escape 0건이다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| imprimitive lift가 exact하게 환원됐는가 | <code>YES</code> |
| correction이 explicit한가 | <code>YES, PARAMETERIZED</code> |
| correction이 현재 analytic core blocker인가 | <code>NO</code> |
| native fixed-\(f\) upper source가 있는가 | <code>NOT IDENTIFIED</code> |
| Bennett/Vaughan unconditional range가 겹치는가 | <code>NO</code> |
| blind weighted correlation이 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 범위가 생겼는가 | <code>NO</code> |

다음 최소 gate는 fixed-coordinate modulus structure를 쓰는 prime-specific energy
또는 blind direct weighted correlation이다.
