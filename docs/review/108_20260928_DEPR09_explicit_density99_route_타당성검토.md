# Review 108 — DEP-R09 explicit density-99 route 타당성검토

- 검토대상: Theory 99, Thorner--Zaman explicit density Theorem 1.2,
  PNT Theorem 2.3·Remark 2.4, machine ledger v1, exact Python·Lean terminals
- 판정:
  <code>FIXED_F_SOURCE_TRANSFER_VALID /
  RANGE_OVERLAP_VALID /
  DIRECT_CERTIFICATE_REJECTION_VALID</code>

> **Successor:** [Theory 100](../method/theory/100_Sono_FMT_DEPR09_sharp_density_fixed_f_audit.md)과
> [review 109](109_20260928_DEPR09_sharp_density_fixed_f_타당성검토.md)은 sharp near-one
> package의 PAP outer losses를 제거해도 current density core가 불충분함을 확인했다.

## 1. 검토 결론

Theory 99의 route-specific 판정은 타당하다.

1. Fixed \(f\), height \(T\) zeros를 \(Q=\max(f,T,3)\) explicit density box에
   포함하는 방향은 안전하다.
2. Exponent 99는 \(\theta=98/99\)를 주며 proof의 \(\sigma\)는 \(39/40\)보다 크다.
3. Current range에는 \(99<d_f<416\) overlap이 있지만
   \(\varepsilon<317/41184\)로 매우 작다.
4. Explicit McCurley zero-free width에서 Theorem 2.3 sup의 \(t=e\) 항은 거의 감쇠하지
   않아, multiplier one 진단에서도 앞 factor가 49보다 크다.

따라서 explicit exponent-99 theorem은 current endpoint gate의 direct small-error
certificate가 아니다. Actual prime error가 크다는 결론은 나오지 않는다.

## 2. Source family 포함관계

Theorem 1.2는 primitive conductors \(q\le Q\), heights \(|\gamma|\le Q\)를 모두 센다.
Character modulo \(f\)는 conductor \(r\mid f\)의 unique primitive character에서
induce된다. \(Q=\max(f,T,3)\)이면 fixed family는 source family의 subset이다.

또 \(Q\le fT\) for \(f\ge3,T\ge e\)이므로 source \(Q^{99(1-\sigma)}\)를
\((fT)^{99(1-\sigma)}\)로 키우는 것은 upper 방향이다. Modulus average의 좋은 평균을
fixed modulus에 임의로 부여한 것이 아니다.

## 3. Sigma와 range 대수

\[
\theta=98/99,qquad
\sigma_0=98/99+\varepsilon/99>39/40.
\]

따라서 source의 near-one sigma restriction이 맞는다. Full interval main size에는
\(\varphi(f)\le f\)만 써서

\[
0<\varepsilon\le1/99-1/d_f
\]

를 충분조건으로 둔다. Positive margin은 \(d_f>99\)에서만 있고 \(d_f<416\)에서
epsilon ceiling은 정확히 \(317/41184\)보다 작다.

## 4. Certificate floor

At \(t=e\), explicit standard zero-free width는

\[
\delta_M(e)=\frac{c_M}{\log f+1},qquad
c_M=10^9/9645908801.
\]

Theory 99의 exact rational 계산으로

\[
\varepsilon^2c_Md_f<3/1000.
\]

따라서 \(U^{-\varepsilon^2\delta_M(e)}>997/1000\),
\(1/\sqrt e>1/2\)이고 sup는 \(997/2000\)보다 크다. \(d_f>99\)를 곱하면
\(98703/2000>49\)다.

식 (99.5)의 range margin은 sup upper endpoint가 eventually \(e\)보다 큼도 보장한다.
따라서 empty sup로 이 floor를 피할 수 없다.

## 5. 해석 경계

이 결과는 다음을 말하지 않는다.

- actual error가 49보다 크다.
- Theorem 1.2가 약하거나 쓸모없다.
- exact big-O multiplier가 1이다.
- sharp \(12/5\) density나 stronger VK route가 실패한다.
- pre-sup cancellation을 보존한 직접 proof가 실패한다.

오히려 source의 \(10^{88},10^{421}\) 비용을 무시하고 unresolved multiplier도 1로
낙관한 **direct black-box upper architecture**조차 smallness를 인증하지 못한다는
fail-closed 판정이다.

## 6. 검증 경계

Python과 Lean은 rational range·coefficient 대수만 검사한다. Density theorem,
zero-free theorem과 prime PNT는 local axiom으로 넣지 않았다. Actual zeros·primes도
계산하지 않았다.

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| fixed \(f\) source 포함관계가 맞는가 | <code>YES</code> |
| exponent-99 source range가 current와 겹치는가 | <code>YES, d_f>99</code> |
| direct small-error certificate인가 | <code>NO</code> |
| sharp \(12/5\) numerical route가 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 Theory 61--71의 sharp near-one components를 fixed-\(f\) full-interval
source로 재특수화하는 감사다.
