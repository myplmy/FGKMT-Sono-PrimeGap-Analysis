# Review 102 — DEP-R09 outer-law sparse centered-mean 타당성검토

- 검토대상: Theory 93, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>WEIGHTED_OUTER_MOMENT_VALID /
  ADAPTIVE_DELETION_BOUND_VALID /
  FIXED_QPRIME_REDUCTION_VALID /
  ANALYTIC_MEAN_OPEN</code>

> **Successor:** review 103/Theory 94는 fixed mean을 centered binary-prime form과
> explicit corrections로 더 분리했다. 아래 outer-law 판정은 유지되며 최신 root gate는
> Theory 94 식 (94.14)다.

## 1. 검토 결론

Theory 93의 환원은 타당하다.

1. blind weights는 outer residue draw 전에 fixed된 real coefficients다.
2. Theory 49 single·pair survival probabilities는 signed weighted mean·variance에
   항별로 적용할 수 있다.
3. outer fluctuation은 \(L=11/5\), \(\epsilon=2a^{-17}\)와
   \(\sigma|Q'|\)로 fully explicit하다.
4. outcome-dependent exceptional deletion은 independence 없이 worst-case
   \(L^\infty|E|\)로 제어된다.
5. outer randomness의 expectation은 \(\sigma D_Q\)이므로 deterministic fixed-\(Q'\)
   mean은 제거되지 않는다.

따라서 construction-dependent selected mean의 확률·deletion 부분은 닫혔지만
analytic fixed mean은 계속 OPEN이다.

## 2. weighted covariance

\(W=\sum_qB_qI_q\), \(P(I_q=1)=\sigma\)에서
\(EW=\sigma\sum_qB_q\)다. pair covariance를 ordered pair로 전개하면

\[
\operatorname{Var}W
=\sigma(1-\sigma)\sum_qB_q^2
+\sum_{q\ne r}(p_{qr}-\sigma^2)B_qB_r.
\]

\(|p_{qr}-\sigma^2|\le\epsilon\sigma^2\)와 triangle inequality를 적용한 Theory 93
식 (93.6)은 맞다. signed mean의 cancellation은 보존하고 uncertainty만 absolute value로
넓혔다.

\(|B_q|\le LU\)를 넣은 normalized upper도

\[
L^2\left\{\frac{1-\sigma}{\sigma N}+epsilon\frac{N-1}{N}\right\}
\]

으로 정확하다. common-shock fixture는 pair contribution의 scaling을 독립적으로
검사한다.

## 3. adaptive deletion

count-good event에서 \(|V_0|\in[(1-\eta)\sigma N,(1+\eta)\sigma N]\), preparation
event에서 \(|E|\le r_E|V_0|\)다. 따라서

\[
|V|\ge(1-r_E)(1-\eta)\sigma N.
\]

\(E\)가 weights를 보고 최악으로 선택될 수 있어도
\(\sum_{q\in E}|B_q|\le LU|E|\)이므로 Theory 93 식 (93.10)이 성립한다.
postselection을 fixed subset으로 잘못 취급하지 않았다.

## 4. outer failure mass

weighted fluctuation, fixed whole-interval count와 preparation event를 union bound로
합친 식 (93.24)은 독립성을 요구하지 않는다. existing child에서 각 explicit cost는
작아질 수 있지만 final coefficient allocation을 아직 정하지 않았으므로 numerical
cutoff로 승격하지 않은 것도 적절하다.

## 5. fixed mean과 source screen

남은 object는

\[
D_Q=\varphi(f)\sum_{q\in Q'}A_h(q;U)-|Q'|S_h(U)
\]

다. 이는 \(q\)와 \(q+\ell f\) prime mass를 결합한다.

원문 대조 결과:

- Maynard I/III와 Stadlmann은 modulus averages 또는 absolute log-saving이다.
- 그 absolute error에 \(\varphi(f)\)를 곱하면 current relative \(|Q'|U\) budget이
  자동으로 나오지 않는다.
- Klurman--Mangerel--Teräväinen의 theorem은 1-bounded multiplicative function과
  typical modulus를 요구해 \(\Lambda\)·primorial \(f\)에 맞지 않는다.
- Leung의 moment theorem은 uniform Hardy--Littlewood conjecture를 가정하고 modulus
  range도 다르다.

따라서 non-drop-in 판정은 타당하다. 전 문헌 부재나 impossibility를 주장하지 않는다.

## 6. 검증 경계

Python은 finite probability와 rational inequalities만 검사한다. actual prime data를
만들지 않는다.

Lean은 scalar terminal만 검사하며 outer probability source·modern analytic theorem을
local axiom으로 넣지 않는다. conditional kernel PASS를 fixed mean의 형식 증명으로
해석하지 않는다.

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| outer weighted moment가 exact한가 | <code>YES</code> |
| adaptive deletion이 explicit한가 | <code>YES</code> |
| selected mean이 fixed mean으로 환원됐는가 | <code>YES</code> |
| fixed \(Q'\) mean이 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |
| calculator·actual 계산을 시작해도 되는가 | <code>NO</code> |

다음 gate는 fixed \(Q'\) shifted prime-pair discrepancy의 pre-absolute-value
dispersion theorem이다.
