# Review 107 — DEP-R09 Thorner--Zaman full-interval centered 타당성검토

- 검토대상: Theory 98, Thorner--Zaman official PDF·source TeX, Sono Proposition 5.3,
  FMT exceptional-prime deletion, machine ledger v1, exact Python helper·tests, Lean terminals
- 판정:
  <code>B0_ZERO_FREE_TRANSFER_VALID /
  FULL_INTERVAL_CENTERING_VALID /
  NUMERICAL_SOURCE_CONSTANTS_NOT_RECOVERED</code>

## 1. 검토 결론

Theory 98의 structural 합성은 타당하다.

1. Actual \(B_0=B_{P(X)}\)를 제거한 \(f\mid P(X)/B_0\)의 primitive conductors는
   Sono/FMT nonexceptional zero-free bound를 받는다.
2. Direct \(t=0\) constant \(1/24\)와 project log ratio는
   \(c_2=47/2520\)을 준다.
3. 이 \(c_2\)는 Thorner--Zaman Remark 1.3의 \(\lambda=1,\theta=7/12\) branch에
   충분하다.
4. Current \(d_f\ge21\)은 full-interval \(U\ge f^{12}\) range를 덮는다.
5. Common-main pointwise relative error \(R_{\rm TZ}\)는 centered norm으로 정확히
   factor 2 이하로 전달된다.

따라서 exceptional secondary main, source range와 centering은 더 이상 독립 blocker가
아니다. 그러나 source multiplier·decay·cutoff가 미수치이므로 endpoint gate는 OPEN이다.

## 2. \(B_0\)와 primitive conductor

FMT Corollary 1은 scale \(Q=P(X)\)의 possible exceptional primitive conductor에서
prime factor 하나 \(B_{P(X)}\)를 고른다. Sono Lemma 3.7도 이 선택을 actual \(B_0\)로
사용한다.

\(f\mid P(X)/B_0\)이면 character modulo \(f\)를 induce하는 primitive conductor
\(r\mid f\)는 \(B_0\)와 coprime이다. 따라서 exceptional conductor와 같을 수 없고
Proposition 5.3의 nonexceptional bound를 받는다. Imprimitive Euler-factor zeros는
near-one real zero가 아니므로 이 전달을 훼손하지 않는다.

## 3. Zero-free constant 방향

Theory 98은

\[
1-\beta\ge\frac1{24\log P(X)}
\]

를 \(t=0\)에서 직접 사용한다. Theory 57이 거부한 것은 이를 height \(T\) family에서
\(3c_{\rm ZFR}/\log T\)로 키우는 방향이다. 이번 proof는 그 변환을 쓰지 않는다.

\(\log f>47X/100\), \(\log P(X)<21X/20\)에서

\[
\frac1{24\log P(X)}>
\frac{47}{2520\log f}.
\]

따라서 rational constant와 부등식 방향이 맞다.

## 4. Centering 경계

Exceptional source main을 그대로 두면
\(\lambda_a=1-\chi_1(a)S_\beta\)이고 character mean은 0이다. Total average에서
principal part만 사라지며 residue별 \(-\chi_1(a)S_\beta\)는 남는다. Python finite
fixture도 이 패턴을 exact하게 확인한다.

Remark 1.3의 \(\lambda=1\) branch를 적용한 뒤에는

\[
e_a=\vartheta(U;f,a)-U/\varphi(f),\qquad
E_f(U;a)=e_a-\frac1{\varphi(f)}\sum_b e_b.
\]

\(|e_a|\le R U/\varphi(f)\)를 합하면 평균 error도 같은 upper이므로
\(\epsilon_\infty\le2R\)다.

## 5. Full-interval source 경계

Official source TeX는 proof of Theorem 2.3에서 \(h\le x-1\)만 처리한다. \(h=x\)는
Corollary 1.4에 별도 인쇄돼 있다. 따라서 short-interval kernel·dyadic lower endpoint를
다시 지불하지 않는 Theory 98의 선택이 맞다.

다만 Corollary 1.4의 “effectively computable”은 다음 숫자를 주지 않는다.

- relative error implied multiplier \(K_{\rm TZ}\),
- decay \(c_{\rm TZ}\),
- density·explicit formula·VK optimization의 common \(U_{\rm TZ}\).

Full-interval source를 선택했다고 이 값들이 자동으로 생기지는 않는다.

## 6. 과장 방지

- \(B_0\)는 모든 real zero의 부재를 증명하지 않는다.
- \(c_2=47/2520\)은 TZ decay constant \(c_{\rm TZ}\)와 같지 않다.
- Effective computability는 numerical certificate가 아니다.
- Centering factor 2는 source pointwise error를 줄이는 cancellation theorem이 아니다.
- 이번 합성은 기존 정리의 project-specific 적용이며 학술적 신규성을 주장하지 않는다.

## 7. 검증 경계

Python은 rational zero-free transfer, finite centered vectors, exceptional character
counterfixture와 scalar multiplier만 검사한다. Actual zeros·primes는 계산하지 않는다.

Lean은 external analytic theorem을 공리화하지 않고 rational constant, exponent range,
centering triangle과 project composition만 검사한다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| actual \(B_0\) exceptional handling이 structural하게 닫혔는가 | <code>YES</code> |
| full-interval source range가 맞는가 | <code>YES</code> |
| centered transfer가 exact한가 | <code>YES, factor 2</code> |
| numerical \(K,c,U_0\)가 있는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 nonexceptional full-interval PNT의 fully numerical multiplier·decay·common
cutoff 복원이다.
