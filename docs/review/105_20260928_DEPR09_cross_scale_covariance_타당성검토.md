# Review 105 — DEP-R09 cross-scale covariance·Abel 타당성검토

- 검토대상: Theory 96, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>ABEL_VALID /
  CROSS_COVARIANCE_VALID /
  TRANSFER_MULTIPLIER_VALID /
  SOURCE_DROP_IN_NOT_IDENTIFIED</code>

> **Successor:** [Theory 97](../method/theory/97_Sono_FMT_DEPR09_prescribed_modulus_endpoint_Linf_transfer.md)과
> [review 106](106_20260928_DEPR09_endpoint_Linf_transfer_타당성검토.md)은 mixed
> covariance의 sufficient input을 single endpoint centered \(L^\infty\) error로 줄였다.

## 1. 검토 결론

Theory 96의 환원은 타당하다.

1. Unweighted small-prime coefficient의 Abel identity는 half-open endpoint와 plus
   integral을 정확히 보존한다.
2. Character mixed product는 fixed-modulus residue-error cross-covariance와 exact하게
   같다.
3. Polarization은 mixed term을 combined signed sequence variance로 바꾼다.
4. Uniform cross input의 Abel transfer multiplier는 정확히
   \(2+\log(\log Y/\log X)\le2+b/a\)다.
5. 확인한 Vaughan·Harper theorem은 prescribed \(f\) mixed covariance의 fully
   numerical drop-in이 아니다.

따라서 새 lemma의 required norm과 multiplier는 닫혔지만 analytic covariance 자체는
계속 OPEN이다.

## 2. Abel endpoint와 sign

\(g(t)=1/\log t\)에 \(g'(t)=-1/[t(\log t)^2]\)다. Stieltjes integration by parts의
minus \(g'\)가 plus integral을 만든다. \((X,Y]\) convention은

\[
\Theta(Y)/\log Y-\Theta(X)/\log X
\]

와 일치한다. Active B0는 \(\le X\)라 interval에 추가 atom이 없다.

## 3. character/residue orientation

Theory 96은 small theta에 conjugate character, large error에 character를 둔다.
Reduced residues를 합하면 \(\psi=\bar\chi\)인 항만 남아

\[
{\cal K}_f=\varphi(f)\sum_aE_t(a)E_{(X,U]}(a)
\]

가 된다. Modulo 5 Gaussian-rational fixture에서 character side와 residue side가 모두
36이고 imaginary part는 0이다.

## 4. polarization 경계

\(2\langle E_t,E_L\rangle=\|E_t+E_L\|^2-\|E_t\|^2-\|E_L\|^2\)는 exact하다.
하지만 세 norms에 upper만 독립 적용하면 subtraction cancellation을 잃는다. Combined
signed sequence의 variance main term과 error를 함께 주는 theorem이 필요하다.

## 5. transfer multiplier

Uniform \(|{\cal K}_f(t)|\le\kappa NU\log t\)에서 두 endpoints가 각각
\(\kappa NU\), integral이
\(\kappa NU\log(\log Y/\log X)\)다. \(Y<Xa\), \(a=\log X\), \(b=\log a\)에서
log ratio는 \(b/a\) 이하이다. 따라서 \(2+b/a\) multiplier는 맞다.

## 6. source 적용성

- Vaughan 2001: one-scale modulus-average variance; fixed mixed covariance statement가
  아니다.
- Harper 2024: general sequence를 허용하지만 dyadic modulus average이며 prescribed
  primorial 하나를 fully numerical하게 제어하지 않는다.
- Thorner--Zaman: pointwise route로 충분할 수 있으나 project audit에서 unnamed
  multiplier·finite cutoff가 남아 있다.

전 문헌 부재나 impossibility를 주장하지 않는 범위도 적절하다.

## 7. 검증 경계

Python은 finite summation identities와 rational fixture만 검사한다. Actual primes나
continuous numerical quadrature를 수행하지 않는다.

Lean은 source theorem을 공리화하지 않고 scalar composition만 검사한다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| Abel identity가 exact한가 | <code>YES</code> |
| mixed character/residue covariance가 exact한가 | <code>YES</code> |
| project multiplier가 explicit한가 | <code>YES, \(2+b/a\)</code> |
| numerical covariance theorem이 있는가 | <code>NO DROP-IN IDENTIFIED</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 식 (96.9)의 prescribed-modulus uniform covariance bound다.
