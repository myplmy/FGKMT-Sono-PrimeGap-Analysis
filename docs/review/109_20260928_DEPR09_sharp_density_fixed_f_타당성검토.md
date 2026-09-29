# Review 109 — DEP-R09 sharp density fixed-\(f\) 타당성검토

- 검토대상: Theory 100, Theories 71--73 source chain, machine ledger v1,
  exact Python·Lean terminals
- 판정:
  <code>FIXED_F_SPECIALIZATION_VALID /
  PAP_OUTER_LOSS_REMOVAL_VALID /
  CURRENT_DENSITY_ARCHITECTURE_INSUFFICIENT</code>

> **Successor:** [Theory 101](../method/theory/101_Sono_FMT_DEPR09_presup_joint_angle_source_audit.md)과
> [review 110](110_20260929_DEPR09_presup_joint_angle_타당성검토.md)은 pre-sup signed
> target과 phase-blind source barrier를 고정했다.

## 1. 검토 결론

Theory 100의 route-specific 판정은 타당하다.

1. Actual primitive conductors \(r\mid f\)를 Theory 71의 \(q_j\le Q=f\) family에
   포함하는 방향은 안전하다.
2. \(T=f^5\), \(\mathcal D=f^7\), \(\omega=1/21\)에서
   \(\kappa=22\), \(\lambda=1-22/d_f\)다.
3. PAP의 principal·Maier·count-transfer costs를 모두 제거해도 Theory 73 tightened
   density coefficient와 가장 유리한 current decay의 core는 \(10^6\)보다 크다.
4. 모든 dimensionless factor를 1로 낮추고 \(\omega^{-6}\)만 남긴 counterfactual도
   4000보다 크다.

따라서 ordinary PAP outer-loss polishing은 endpoint gate를 닫지 않는다. Actual error가
크다는 결론이나 모든 detector proof의 불가능성은 나오지 않는다.

## 2. Parameter specialization

Theory 71 detector scale은 \(D=Q^2T\)다. \(Q=f,T=f^5\)이면 \(D=f^7\)이며
Theory 72의 exponent algebra를 그대로 사용해

\[
\kappa(\omega)=14(1+12\omega),\qquad
\lambda=1-\kappa/d_f
\]

를 얻는다. \(\omega=1/21\)에서 \(\kappa=22\)다. \(d_f\le22\)에서는 positive
decay가 없으므로 failure 판정이 즉시 맞고, \(d_f>22\)만 별도 감사하면 된다.

## 3. Tightened coefficient floor

Current \(d_f<416\)과 \(c_M=1/9.645908801\)에서

\[
c_M(d_f-22)/5<c_M(394)/5<9.
\]

따라서 \(e^{-c_M(d_f-22)/5}>e^{-9}>3^{-9}\)다. Theory 73 coefficient를
곱하면 exact하게 \(3834565868150024/2790491715>10^6\)이다.

이 계산은 \(8/\lambda\), centered factor 2와 모든 PAP 후단 cost를 버린 낙관 floor다.
따라서 기존 PAP certificate를 그대로 옮겨 생긴 과대비용 때문만은 아니다.

## 4. \(\omega^{-6}\) counterfactual

Current architecture의 세 \(\omega^{-2}\) source를 보존하면
\(\omega^{-6}\ge21^6\)다. 더 유리하게 \(\kappa\ge14\)만 쓰면

\[
c_M(d_f-\kappa)/5<c_M(402)/5<9.
\]

모든 dimensionless factor를 1로 두어도 core는
\(21^6/3^9=117649/27>4000\)다. 이는 architecture diagnostic이다. 새 proof가
\(\omega^{-6}\)을 제거하거나 cancellation과 상쇄하는 가능성은 남는다.

## 5. 해석 경계

- 큰 coefficient upper는 actual error lower가 아니다.
- Fixed modulus에서 residue factor를 추가로 개선할 수 있다.
- Height choice \(T=f^5\)를 바꿀 수 있다.
- Pre-sup signed cancellation을 보존하면 density-only certificate와 다른 결과가 가능하다.
- New detector 또는 larger-window source는 이번 판정 밖이다.

따라서 “모든 sharp density route 불가능”이 아니라 “current Theory 71 \(\omega^{-6}\)
certificate architecture에서 outer costs만 줄이는 것으로는 불충분”이 정확한 결론이다.

## 6. 검증 경계

Python과 Lean은 rational coefficient·exponent algebra만 검사한다. Jutila/Ramaré--Zuniga
analytic theorem과 PNT transfer는 local axiom으로 넣지 않았다. Actual primes·zeros도
계산하지 않았다.

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| fixed-family specialization이 맞는가 | <code>YES</code> |
| PAP outer cost를 제거했는가 | <code>YES</code> |
| current density core가 small한가 | <code>NO</code> |
| actual endpoint error lower를 증명했는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 pre-sup cancellation 또는 \(\omega^{-6}\) detector 구조를 바꾸는 proof다.
