# Review 104 — DEP-R09 conductor-weighted character dual 타당성검토

- 검토대상: Theory 95, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>CHARACTER_DUAL_VALID /
  CONDUCTOR_ENERGY_VALID /
  PRIME_LARGE_SIEVE_SCOPE_VALID /
  SEPARATE_L2_REJECTION_VALID</code>

## 1. 검토 결론

Theory 95의 판정은 타당하다.

1. Centered kernel은 nonprincipal character sum으로 exact하게 dualize된다.
2. Prime variables가 모두 \(>X\)라 induced character와 primitive core 사이 correction이
   없다.
3. Primitive conductor-level coefficient energy는 Möbius inversion으로 exact하다.
4. Schlage--Puchta Theorem 2는 large-prime axis range를 덮지만 multiplier·cutoff가
   fully numerical하지 않다.
5. 그 source를 낙관적으로 사용해도 separate Cauchy는
   \((\varphi(f)-N)/N>1\) factor를 남겨 current gate를 인증하지 못한다.

따라서 필요한 것은 두 L2 upper가 아니라 small/large prime character sums의 joint
signed correlation theorem이다.

## 2. exact character·conductor partition

Reduced \(p,q\)에서

\[
\varphi(f)1_{p\equiv q\pmod f}-1
=\sum_{\chi\ne\chi_0}\chi(p)\overline{\chi(q)}.
\]

Finite sums를 교환한 Theory 95 식 (95.4)은 맞다. Character induction의 unique
primitive core와 \((pq,f)=1\)을 사용한 식 (95.5)도 correction 없이 성립한다.

## 3. primitive energy formula

All-character energy modulo \(d\)는 residue occupancy squares
\(\varphi(d)\sum_aN_d(a)^2\)다. 이를 conductor divisor sum으로 보고 Möbius inversion한
식 (95.7)은 표준 finite identity다.

Sample \(f=30\), residues \(7,11,13\)에서 conductor energies의 합은 24, principal
energy는 9, nonprincipal total은 15다. 이는
\(N(\varphi(f)-N)=3(8-3)=15\)와 일치한다.

## 4. source range

Schlage--Puchta Theorem 2의 조건은 prime length \(N_0>Q^{2+\varepsilon}\)다.
Large axis에서는 \(N_0=U\), \(Q=f\), \(d_f\ge21\)이라 만족한다. Divisor conductors만
취하는 것은 full \(r\le f\) sum을 줄이므로 upper 방향이 안전하다.

Small axis에서는 \(N_0=Y<f=Q\)라 full family 적용 조건과 반대다. Corollary 5의
single-character result도 low conductors만 덮고 implicit \(o(1)\)을 갖는다.

## 5. separate-L2 barrier

Coefficient energy와 large-prime energy를 separately Cauchy하면

\[
|{\cal C}_f|^2\le N(\varphi(f)-N)V_{\mathbb P}.
\]

Source multiplier를 비현실적으로 1까지 낮춰 \(V_{\mathbb P}\le U^2\)로 두어도 normalized
square는 \((\varphi(f)-N)/N\)이다. Existing child에서 \(\varphi(f)>2N\)이므로 1보다
크다.

이는 actual weighted sum의 하한이 아니라 해당 upper-certificate architecture의
불충분성이다.

## 6. 검증 경계

Python은 divisor/phi/Möbius와 finite residue collision을 exact하게 계산한다. 실제
prime character sums는 계산하지 않는다.

Lean은 external source theorem이나 character induction을 local axiom으로 넣지 않는다.
Scalar terminal PASS를 analytic weighted-product proof로 읽지 않는다.

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| character/conductor dual이 exact한가 | <code>YES</code> |
| large-prime prime-supported L2 range가 맞는가 | <code>YES</code> |
| source가 fully numerical한가 | <code>NO</code> |
| separate L2가 current gate를 닫는가 | <code>NO</code> |
| joint weighted product가 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 small-prime coefficients와 large-prime errors를 동시에 보존하는 direct
dispersion/large-values theorem이다.
