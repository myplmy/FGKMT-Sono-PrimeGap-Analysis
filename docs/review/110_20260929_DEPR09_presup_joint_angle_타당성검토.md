# Review 110 — DEP-R09 pre-sup joint-angle 타당성검토

- 검토대상: Theory 101, Ramaré 2026 두 preprint, Motohashi 2012,
  Zheng 2025, Szabó 2024, machine ledger v1, exact Python·Lean terminals
- 판정:
  <code>PRE_SUP_INTERFACE_VALID /
  PHASE_BLIND_SHARPNESS_VALID /
  CHECKED_SOURCE_DROP_IN_NOT_IDENTIFIED</code>

## 1. 검토 결론

Theory 101의 논리 경계는 타당하다.

1. Theory 95 weighted product에 characterwise explicit formula를 대입하면 signed
   zero-packet sum과 explicit corrections로 분해된다.
2. Packet magnitudes나 separate norms만 쓰는 premise는 independent phase rotations에
   불변이며 triangle/Cauchy equality witness가 있다.
3. 따라서 current target에는 actual coefficient/error vectors의 joint angle을
   제어하는 추가 theorem이 필요하다.
4. 확인한 Ramaré·Motohashi·Zheng·Szabó source는 support-only norm, additive Fourier,
   auxiliary-modulus moment, well-factorable average 또는 bounded-order single-character
   theorem이라 prescribed \(f\) joint angle을 numerical하게 주지 않는다.

이는 actual packets가 aligned라는 주장이 아니며 checked premise class의 정보 한계다.

## 2. Explicit-formula orientation

Theory 95는

\[
C_\chi(Q')=\sum_{q\in Q'}\overline{\chi(q)},\qquad
Z_\chi=\sum_{X<p\le U}(\log p)\chi(p)
\]

를 사용한다. Character explicit formula에서 \(Z_\chi=-\mathfrak Z_\chi+\mathfrak R_\chi\)를
대입하면 \({\cal C}_f=-\sum C_\chi\mathfrak Z_\chi+sum C_\chi\mathfrak R_\chi\)다.
Conjugation orientation과 minus sign이 보존됐다.

Prime powers·principal/exceptional normalization과 truncation은 correction packet에 남겨
두므로 analytic completion으로 과장하지 않았다.

## 3. Phase-blind sharpness

For nonzero complex \(C_i\), \(z_i=M_i\overline C_i/|C_i|\)를 택하면
\(C_iz_i=|C_i|M_i\)다. 따라서 individual magnitude bounds만으로 triangle upper보다
작은 universal constant는 나오지 않는다.

Real two-point subspace에서도 coefficients \((1,1)\)와 packets \((1,1)\), \((1,-1)\)는
같은 magnitudes와 energy를 가지면서 correlations 2와 0을 만든다. Python fixture가 이를
exact rational로 검사한다.

이 witness는 actual L-function zeros의 admissibility를 주장하지 않는다. Source assumptions가
phase를 전혀 제약하지 않으면 conclusion도 phase cancellation을 요구할 수 없다는
logical certificate boundary다.

## 4. Angle budget

Theory 95 coefficient energy와 conditional \(A_Z\le U^2\)에서

\[
|{\cal C}_f|/(NU)le\Gamma_f\sqrt{(\varphi(f)-N)/N}.
\]

따라서 squared angle budget은
\(\Gamma_f^2<\delta_{\rm bin}^2N/(\varphi(f)-N)\)다. Conditional optimistic energy를
actual theorem으로 승격하지 않았고, fixture \(1/90000\)도 project threshold가 아니다.

## 5. Source 판정

### Ramaré weighted sieve

Support와 \(\ell^2\) norm을 사용하며 complex extension 설명은 absolute-value sequence를
통한다. 두 character vectors의 angle을 statement로 제어하지 않는다.

### Ramaré regularity companion

Near-saturation count를 가정해 additive Fourier polynomial near zero를 제어한다.
Current multiplicative-character family와 required input lower가 다르다.

### Motohashi

Auxiliary moduli에 대한 character-square/L1 mean이다. Prescribed \(f\)의
\(C_\chi Z_\chi\) signed product가 아니고 constants/cutoff도 numerical하지 않다.

### Zheng

Fixed residues에 대해 two moduli와 well-factorable weights를 평균한다. Current prime
residue mask와 one prescribed growing primorial을 isolate하는 theorem이 아니다.

### Szabó / Heath--Brown

한 bounded-order character의 smoothed real part를 asymptotically 제어한다. Current all-order
simultaneous complex weighted sum과 numerical cutoff를 제공하지 않는다.

## 6. 과장 방지

- 전 문헌 부재를 주장하지 않는다.
- Recent Ramaré preprints의 peer review를 가정하지 않는다.
- Actual joint angle이 크다고 주장하지 않는다.
- Support-only theorem이 다른 sieve 문제에 유용하지 않다고 말하지 않는다.
- New joint theorem이나 direct fixed-modulus proof 가능성을 보존한다.

## 7. 검증 경계

Python과 Lean은 finite vector algebra만 검사한다. External explicit formula, zero-density,
dispersion theorem은 local axiom으로 넣지 않았다. Actual primes·zeros는 계산하지 않았다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| pre-sup target이 exact한가 | <code>YES</code> |
| magnitudes/norms만으로 joint saving이 나오는가 | <code>NO, sharp witnesses</code> |
| checked numerical prescribed-\(f\) source가 있는가 | <code>NO</code> |
| actual joint cancellation이 부정됐는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 fixed-\(f\) explicit formula를 characterwise absolute value 전에 직접
재작성하고 weighted zero-packet lemma의 정확한 statement를 확정하는 것이다.
