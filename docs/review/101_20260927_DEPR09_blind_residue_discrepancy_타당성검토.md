# Review 101 — DEP-R09 blind residue-discrepancy 환원 타당성검토

- 검토대상: Theory 92, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>INVERSE_TRANSFORM_VALID /
  BRUN_TITCHMARSH_ENVELOPE_VALID /
  SUCCESS_SCALE_NORMALIZATION_VALID /
  SPARSE_MEAN_REMAINS_OPEN</code>

## 1. 검토 결론

Theory 92의 핵심 판정은 타당하다.

1. blind character weight는
   \(B_h(v)=\varphi(f)A_h(v;U)-S_h(U)\)인 실수형 residue discrepancy다.
2. Montgomery--Vaughan Theorem 2와 elementary prime-power correction으로
   current range에서 \(|B_h(v)|<11U/5\)를 얻는다.
3. 이 pointwise upper를 Theory 91 moment에 넣고 success scale
   \((\rho MU)^2\)로 나누면 pair-error factor는
   \(\Gamma_M\to\beta\)이고 \(\beta\rho M\)이 아니다.
4. sparse selected-residue mean \(D_V\)는 one-sided Brun--Titchmarsh나 full-residue
   Parseval로 작아지지 않는다.

따라서 inner pair dimension loss는 더 이상 구조 blocker가 아니지만 blind branch
전체는 닫히지 않았다. 새 최소 blocker는 construction-dependent signed mean이다.

## 2. character orthogonality

full character sum에 lifted prime sum을 넣으면

\[
\sum_{\psi\bmod f}\overline{\psi(v)}Z_{\widetilde\psi}(U)
=\varphi(f)A_h(v;U).
\]

principal term은 \(S_h(U)\)이므로 nonprincipal sum은 그 차다. reduced \(v\)와
\(n\equiv v\pmod f\)에서 \((n,f)=1\) 조건이 자동이라는 점도 맞다.

modulo 5 exact fixture는 네 character 전체를 Gaussian rational로 전수하고 inverse
transform과 Parseval을 독립적으로 확인한다. complex cancellation을 float로 근사하지
않는다.

## 3. pointwise envelope

Montgomery--Vaughan printed p.121 식 (1.10)은 \(U>f\)에서

\[
\pi(U;f,v)<\frac{2U}{\varphi(f)\log(U/f)}
\]

를 준다. \(d_f\ge21\)이면 prime contribution coefficient는 \(21/10\) 이하이다.

prime powers에는

\[
\psi(U)-\theta(U)\le\sqrt U\log U
\]

인 elementary 전체 upper를 쓴다. progression 조건을 버린 것이므로 방향이 안전하다.
Theory 90의 \(f\le U^{1/21}\)과 \(U>e^{20}\)에서 correction gates가 성립하고
progression upper는 \(11U/5\), principal upper는 \(11U/10\)이다.

두 항이 비음수라 \(|a-b|\le\max(a,b)\)를 사용한 것도 맞다. 합 \(33U/10\)을
지불할 필요가 없다.

## 4. normalized moment

Theory 91 coefficient를

\[
K_M=(1+\alpha)\rho-\rho^2+\beta\rho^2(M-1)
\]

라 하면 pointwise L2는 \((121/25)MU^2\) 이하다. mean ratio \(\delta\)를 분리해

\[
\frac{\mathbb E|R_{\rm blind}|^2}{(\rho MU)^2}
\le\delta^2+\frac{121}{25}
\left\{\frac{1+\alpha}{\rho M}-\frac1M+
\beta\frac{M-1}{M}\right\}
\]

가 exact하게 나온다. common-shock witness도 이 normalization에서는 covariance
excess가 \(\beta\)이므로 Theory 91과 모순이 없다.

success mass \(p_{\rm in}\), floor \(M_\omega\ge\lambda\rho M\)을 보존한 strict
Markov gate도 방향이 맞다. 다만 실제 적용에는 outer-good fiber 전체에서 동일한
\(\delta\), \(\lambda\), \(p_{\rm in}\) budget을 맞춰야 한다.

## 5. source 적용성

Montgomery--Vaughan 원문은 fully explicit upper지만 centered asymptotic이 아니다.
Vaughan 2001 및 Friedlander--Goldston류 full variance도 sparse construction-dependent
set의 signed mean을 그대로 주지 않는다.

식 (92.25)의 첫 항은 vertex \(v\)가 작은 prime이고 \(v+\ell f\)도 prime-power
mass를 갖는 shifted prime-pair형 합이다. standard two-prime upper만으로 main term과의
양측 오차를 작은 \(\delta\)로 만들 수 없다.

## 6. 판정 범위

닫힌 것:

- blind inverse transform과 reality,
- full Parseval과 selected mean identity,
- explicit pointwise \(11/5\) envelope,
- success-scale pair normalization.

열린 것:

- sparse selected-residue centered mean,
- outer-fiber uniformity,
- blind same-law moment,
- PAP-11, DEP-R09, fixed coefficient와 numerical \(X_{\rm cert}\).

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| blind weight가 generic complex observable인가 | <code>NO — REAL DISCREPANCY</code> |
| pointwise magnitude가 explicit한가 | <code>YES, &lt;11U/5</code> |
| pair dimension loss가 최종 blocker인가 | <code>NO AT SUCCESS SCALE</code> |
| selected sparse mean이 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 범위가 생겼는가 | <code>NO</code> |
| calculator·actual 계산을 시작해도 되는가 | <code>NO</code> |

다음 gate는 actual outer law와 fixed selected-set source를 각각 감사해 식 (92.25)의
uniform numerical \(\delta\)를 얻는 것이다.
