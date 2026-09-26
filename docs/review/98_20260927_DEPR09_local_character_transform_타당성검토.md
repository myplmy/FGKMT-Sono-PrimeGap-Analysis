# Review 98 — DEP-R09 reweighted local character-transform 타당성검토

- 검토대상: Theory 89, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>LOCAL_TRANSFORM_IDENTITY_VALID /
  ATOM_TO_FOURIER_REJECTION_VALID /
  BLIND_CHARACTER_OBSTRUCTION_VALID</code>

## 1. 검토 결론

Theory 89의 판정은 타당하다.

1. formula (5.9)를 local character phase에 대입한 transform 식은 exact하다.
2. same-stage product는 history 조건부 independence만 사용하고 global independence를
   가정하지 않는다.
3. 작은 atom cap이 nonprincipal Fourier saving을 함의하지 않는 finite witness가 있다.
4. randomized/fixed modulus CRT split에서 randomized component가 principal인
   blind family가 정확히 \(\varphi(f)\)개 남는다.
5. 각 outcome의 blind nonprincipal coefficient energy는
   \(M_\omega\{\varphi(f)-M_\omega\}\)로 고정된다.
6. 관련 GKM theorem은 object·range·growing-dimension이 달라 drop-in이 아니다.

따라서 local transform은 nonblind family의 유효한 interface지만 full same-law
moment를 혼자 닫지 못한다. blind prime-error correlation이 별도 필요하다.

## 2. local transform 양화사

normalizer-good history \(W\)에서 formula (5.9)는

\[
\Pr(e'_p=E\mid W)
=
\frac{\mu_p(E)1_{\{E\subset W\}}}{X_p(W)P_{j-1}(E)}.
\]

이를 \(\overline{\xi(u-a_p(E))}\)에 대해 합한 식이 Theory 89 식 (89.2)다.
bad history의 deterministic empty output은 별도로 \(\overline{\xi(u)}\)를 준다.

같은 stage에서는 \(W\) 조건부 product가 맞다. 그러나 다음 stage의 transform은
앞 output이 만든 \(W\)에 의존한다. Theory 89가 stage product만 선언하고 global
factorization을 거부한 것은 정확하다.

## 3. atom-cap counterexample

quadratic character modulo 11에서

\[
A=\{a:\xi(-a)=1\}
=\{2,6,7,8,10\}
\]

에 uniform law를 두면 atom은 \(1/5\)이지만 transform은 정확히 1이다.
따라서 atom cap이나 Shannon/min-entropy 정보만으로 multiplicative Fourier
coefficient를 strict하게 줄일 수 없다.

이 witness는 actual law의 transform이 1이라는 말이 아니다. current source inputs에서
빠진 analytic cancellation이 무엇인지 보여 주는 logical countermodel이다.

## 4. GKM 선행정리 적용성

GKM Theorem 1.5는 real character로 twisted한 단일 truncated divisor sum의
\(2r\)-moment다. current weight는 growing-dimensional Maynard square weight이고
그 위에 full-residue projection과 formula (5.9) reweighting이 있다.

또 GKM implied constants는 fixed moment order에 의존하고 exceptional branch는
\(e^{(\log q)^C}\le R\)를 요구한다. project의 local modulus는 \(p\asymp X\),
sieve scale은 \(R\asymp X^{1/9}\), dimension은 growing이다. 따라서 theorem 이름의
“sieve weights”와 “Dirichlet character”가 같다는 이유만으로 적용할 수 없다.

이번 source screen은 checked primary corpus의 판정이며 전 문헌 부재를 주장하지 않는다.

## 5. blind family factorization

\(\mathfrak q=fh\), \((f,h)=1\), \(m_\omega=0\bmod f\)다. \(\psi\bmod f\)에
principal randomized component를 붙인 \(\widetilde\psi\)는

\[
C_{\widetilde\psi}(\omega)
=\sum_{s\in T_\omega}\overline{\psi(s)}
\]

를 만족한다. Theory 88의 log separation은 \(f>X^2>N\)을 주므로 distinct offsets는
modulo \(f\)에서도 distinct하다. character orthogonality를 적용할 수 있다.

따라서

\[
\sum_{\psi\bmod f}|C_{\widetilde\psi}|^2
=\varphi(f)M_\omega,
\]

principal square를 빼면

\[
\sum_{\psi\ne\psi_0}|C_{\widetilde\psi}|^2
=M_\omega\{\varphi(f)-M_\omega\}.
\]

이는 law-average가 아니라 outcome별 identity다.

## 6. 남은 analytic target

blind prime-error energy \(V_{\rm blind}\)에 Cauchy를 쓰면

\[
|R_{\rm blind}|^2
\le
M_\omega\{\varphi(f)-M_\omega\}V_{\rm blind}.
\]

따라서 Theory 89의 식 (89.25)은 충분하다. 하지만 coefficient and error total
energies만 쓰는 Cauchy는 abstract aligned vector에서 sharp하다. actual prime-error
vector가 align되지 않는다는 theorem이 바로 남은 direct-correlation 입력이다.

## 7. 판정 범위

배제되는 것:

- atom cap만으로 local Fourier saving을 선언하는 방식,
- randomized-coordinate transform 하나로 모든 characters를 처리하는 방식,
- GKM Theorem 1.5의 이름 유사성만으로 drop-in하는 방식.

배제되지 않는 것:

- nonblind family의 actual Maynard-weight character transform,
- blind family의 prime-specific \(V_{\rm blind}\) upper,
- \(C_{\widetilde\psi}Z_{\widetilde\psi}\) direct decorrelation,
- 다른 construction 또는 pointwise PAP.

## 8. 검증 경계

Python exact fixture는 quadratic transform, blind energy decomposition,
strict Cauchy gate와 source hashes를 검사한다. actual prime data는 사용하지 않는다.

Lean은 source premise 뒤 scalar composition만 검사한다. formula (5.9), finite
character orthogonality와 analytic literature theorem을 local axiom으로 넣지 않는다.

canonical 회귀시험 138개, Lean direct compile·full build와 전수 verification
refresh가 모두 PASS했다. 최종 inventory는 theory 90개, display 식 1,733개,
declaration 324개, 금지 proof escape 0건이다.

## 9. 최종 상태

| 질문 | 판정 |
|---|---|
| exact local transform을 고정했는가 | <code>YES</code> |
| atom cap이 Fourier saving을 주는가 | <code>NO</code> |
| applicable numerical source theorem이 있는가 | <code>NOT IDENTIFIED</code> |
| blind family가 남는가 | <code>YES, EXACT</code> |
| blind coefficient energy가 law로 감소하는가 | <code>NO, TOTAL IS EXACT</code> |
| blind weighted prime error가 닫혔는가 | <code>NO</code> |
| actual same-law moment가 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 범위가 생겼는가 | <code>NO</code> |

다음 최소 gate는 blind-family prime-error correlation 또는 fixed-coordinate modulus의
prime-specific numerical upper다.
