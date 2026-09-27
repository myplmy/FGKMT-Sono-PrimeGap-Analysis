# Review 103 — DEP-R09 fixed-\(Q'\) bilinear 환원 타당성검토

- 검토대상: Theory 94, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>CENTERED_KERNEL_VALID /
  PRIME_SPLIT_VALID /
  CORRECTION_ENVELOPES_VALID /
  R10_NON_DROP_IN_VALID</code>

> **Successor:** review 104/Theory 95는 centered form을 primitive conductor별
> weighted product로 dualize하고 separate-L2 certificate의 \(\varphi(f)/N\) 장벽을
> 고정했다. 최신 root gate는 direct joint correlation이다.

## 1. 검토 결론

Theory 94의 판정은 타당하다.

1. Fixed mean은 mean-zero kernel
   \(H_Q(n)=\varphi(f)1_{\{[n]_f\in Q'\}}-|Q'|\)을 가진 von Mangoldt sum이다.
2. Prime과 higher prime powers를 분리하면 centered binary-prime form, B0 atom과
   explicit prime-power correction이 exact하게 나온다.
3. B0와 higher-prime-power corrections는 current \(f\le U^{1/21}\) 범위에서
   parameterized explicit하고 감쇠한다.
4. Sono/R10의 Selberg theorem은 positive pair mass의 one-sided upper이므로 centered
   main-term cancellation을 제공하지 않는다.

따라서 새 최소 gate는 correction이 아니라 binary-prime form의 two-sided signed
pre-absolute-value estimate다.

## 2. kernel identity

각 reduced \(n\)에서 selected residues를 합하면 kernel은 두 값

\[
\varphi(f)-N,\qquad -N
\]

중 하나다. Full reduced residue system을 합하면 정확히 0이다. Theory 92 inverse
transform에서 \(q\)와 \(n\)의 finite sums를 교환한 식 (94.3)은 따라서 맞다.

Python fixture는 original
\(\varphi(f)\sum_q A_h(q)-NS_h\)와 termwise kernel sum을 독립적으로 계산한다.

## 3. prime·prime-power split

\(\Lambda\) support를 exponent 1과 \(j\ge2\)로 나눈 것은 disjoint exact partition이다.
Prime \(p\nmid fh=P(X)/B_0\)는 \(p>X\) 또는 active \(B_0\)다. Active \(B_0\le X\)는
\(Q'\)의 어느 \(q>X\)와도 modulo \(f\)에서 같지 않아 contribution이
\(-N\log B_0\)다.

\(p>X\), \(q<f\)에서는 \(p\equiv q\pmod f\) iff
\(p=q+\ell f\) for unique \(\ell\ge0\). 이로써 positive pair mass와 principal
\(\vartheta(U)-\vartheta(X)\)의 centered 차가 exact하게 나온다. Diagonal
\(\ell=0\)도 보존됐다.

## 4. correction upper

Universal하게

\[
|H_Q(n)|\le\varphi(f)+N
\]

이고 higher-prime-power total은 \(\sqrt U\log U\) 이하이다. 따라서 식 (94.12)의
첫 bound가 맞다. \(N\ge1\), \(\varphi(f)\le f\le U^{1/21}\)을 쓰는 둘째 bound도
방향이 맞다.

그 upper는 \(L=\log U\)에서
\(Le^{-19L/42}+Le^{-L/2}\)이고 large \(L\)에서 감소한다. 최종 budget이 정해지면
finite cutoff를 역산할 수 있지만 지금 calculator를 시작하지 않은 것이 맞다.

## 5. R10 적용성

Sono Theorem 4.1은 general two-linear-form upper-bound sieve다. Fixed \(\ell\)의
forms \(z,z+\ell f\)에도 원리상 대응하지만, current full sum에는

- \(\ell\)-average singular factors,
- determinant \(\ell f\), B0,
- \(\log(q+\ell f)\) weight,
- source \(O\)-multiplier와 finite cutoff

가 새로 필요하다. 특히 최대 determinant scale에서 source error ratio가 자동
\(o(1)\)이 아니다.

이 applicability 문제와 별도로 one-sided upper만으로 centered absolute error를
작게 만들 수 없다는 logical 판정도 맞다. Pair mass 0은 모든 nonnegative upper를
만족하지만 relative centered error 1을 만든다.

이는 Sono Assumption UB가 원래 목적에서 잘못됐다는 뜻이 아니다. Original proof의
pair-collision upper와 current signed covariance는 서로 다른 theorem object다.

## 6. 검증 경계

Python은 finite weighted terms와 residue arithmetic을 exact <code>Fraction</code>으로 검사한다.
Prime 여부를 실제로 탐색하지 않는다.

Lean은 source theorem을 local axiom으로 넣지 않고 algebraic bookkeeping과 logical
countermodel terminal만 검사한다. Conditional kernel PASS는 binary-prime analytic
estimate의 증명이 아니다.

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| pre-absolute-value kernel이 exact한가 | <code>YES</code> |
| prime-power/B0 correction이 explicit한가 | <code>YES</code> |
| R10이 centered gate를 닫는가 | <code>NO</code> |
| centered binary-prime form이 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |
| calculator·actual 계산을 시작해도 되는가 | <code>NO</code> |

다음 gate는 character 또는 dispersion dualization을 통한 two-sided signed estimate다.
