# Sono/FMT H1c-1b.4e actual identity-form Hypothesis 1 합성

- 작성: 2026-09-09 KST
- 증거 수준: `PROJECT FINITE COMPOSITION / ACTUAL-APPLICATION CHILD`
- 판정:
  `ACTUAL IDENTITY HYPOTHESIS 1 INPUT EXPLICIT / WEIGHTED P9.2 AND ROOT SIV-08 OPEN`
- 충분조건:
  \(T=X/2\), \(r=\lfloor(\log T)^{1/5}\rfloor\ge10^{10}\), 즉
  \(X\ge2\exp(10^{50})\)
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b4e_end_to_end_composition_v1.json`](data/Sono_FMT_H1c1b4e_end_to_end_composition_v1.json)
- 검산 구현:
  [`source/h1c1b4e_end_to_end_composition.py`](../../../source/h1c1b4e_end_to_end_composition.py)
- 비판적 검토:
  [`docs/review/49_20260909_H1c1b4e_actual_Hypothesis1_합성_타당성검토.md`](../../review/49_20260909_H1c1b4e_actual_Hypothesis1_합성_타당성검토.md)

> 후속 상태(2026-09-09): 아래 OPEN은 H1c-1b.4e 당시 snapshot이다.
> [H1b-P92a](44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md)가 actual identity weighted
> P9.2와 lower atom을 \(k\ge10^{200}\)에서 닫았다. 본 문서의 input cutoff와 별개의
> 더 큰 child cutoff이며, general P92 및 \(X_{\rm cert}\)는 계속 OPEN이다.

## 1. 결론

FGKMT Section 8에서 Theorem 6의 두 번째 결론을 호출할 때, Hypothesis 1(2)를 확인해야 하는
선택 집합은 identity form

\[
\mathcal L'=\{\widetilde L_{q,i,i}\},\qquad
\widetilde L_{q,i,i}(n)=n
\]

하나다. H1c-1b.1--4d와 endpoint 교정 r1을 한 quantifier chain으로 합치면, 위 충분조건에서
FGKMT의 수정 closed interval

\[
\mathcal A(T)=\{n\in\mathbb Z:T\le n\le2T\}
\]

에 대해 Hypothesis 1의 세 조건을 각각 explicit constant

\[
\boxed{C_1=1,\qquad C_2=1,\qquad C_3=2}
\tag{43.1}
\]

로 만족시킨다. 이는 **actual identity-form Hypothesis input의 유한 closure**다.

그러나 Maynard Proposition 9.2의 weighted moment proof 자체와 FGKMT가 closed 합에서 외부
\((T,2T]\) prime set으로 돌아갈 때의 lower-endpoint weight는 아직 합성하지 않았다. 따라서
`H1B-P92=RATE_MISSING`, broad `SIV-08=HARD_BLOCKER`,
\(X_{\rm cert}=\texttt{OPEN}\)은 유지한다.

## 2. 쉬운 설명

Hypothesis 1은 기계가 작동하기 전에 통과해야 하는 세 가지 입력검사라고 볼 수 있다.

1. 모든 정수가 나머지류에 고르게 나뉘는가.
2. 소수도 평균적으로 나머지류에 충분히 고르게 나뉘는가.
3. 어떤 한 나머지류에 정수가 지나치게 몰리지 않는가.

첫째와 셋째는 연속 정수의 개수를 세면 정확한 오차가 1 이하라서 초등적으로 닫힌다. 둘째는
가장 어려운 검사였지만, Bordignon의 explicit 소수분포 정리와 지금까지 복원한 모든 보정항을
합쳐 매우 큰 시작점에서 통과시켰다.

이것은 “연료가 규격에 맞는다”를 확인한 것이지 “엔진 전체를 돌려 최종 주행거리를 증명했다”는
뜻은 아니다. 가중 sieve moment와 그 뒤의 FGKMT/FMT/Sono 합성이 여전히 남는다.

## 3. 공통 parameter와 cutoff

다음처럼 둔다.

\[
L=\log T,\quad \ell=\log L,\quad
r=\lfloor L^{1/5}\rfloor,\quad n=100r^2,\quad A=n+10.
\tag{43.2}
\]

\(r\ge10^{10}\)이면 \(L\ge r^5\ge10^{50}\)이고
\(L<(r+1)^5\)에서

\[
\ell<5\log(r+1)<5r.
\tag{43.3}
\]

H1c-1b.2의 fixed \(Q_1=L^A\)와 하나의 exceptional prime \(B\), r1의 closed endpoint,
4c의 full error budget과 4d의 corrected source constant를 모두 같은 \((r,L,T)\)에 넣는다.

## 4. Hypothesis 1(1): 정수의 평균분포

closed integer interval의 원소 수를

\[
N=\#\{m\in\mathbb Z:T\le m\le2T\}
\]

라 하면 \(N\ge T-1\ge T/2\)다. 연속한 \(N\)개 정수 중 한 나머지류의 개수는
\(N/q\)와 1 미만 차이 난다. 따라서

\[
\sum_{q\le T^{1/3}}\max_a
\left|\#\mathcal A(T;q,a)-\frac Nq\right|
\le T^{1/3}.
\]

목표 \(N/L^n\) 이하가 되려면

\[
\log2+n\ell\le\frac{2L}{3}
\tag{43.4}
\]

이면 충분하다. (43.3), \(L\ge r^5\), \(\log 2<1\)을 쓰면 exact integer inequality

\[
3(500r^3+1)\le2r^5
\tag{43.5}
\]

로 줄어들며 모든 \(r\ge10^{10}\)에서 성립한다. 따라서 constant 1로 조건 (1)이 닫힌다.

## 5. Hypothesis 1(2): identity primes의 평균분포

r1의 정확한 closed count를 \(P_T^{\rm cl}\)라 하자. 4b의 source density는 더 직접적으로

\[
P_T^{\rm cl}\ge\pi(2T)-\pi(T)>\frac{3T}{5L}>\frac{T}{2L}
\tag{43.6}
\]

를 준다. 4c의 normalized error를 \(B_0+\kappa C_A\)라 했고, 4d는 같은 input에서
\(C_A<13e^{-100}<1\)을 증명했다. 따라서

\[
\sum_{\substack{q\le T^{1/3}\\(q,B)=1}}
\max_{(a,q)=1}
\left|P_T^{\rm cl}(q,a)-\frac{P_T^{\rm cl}}{\varphi(q)}\right|
<\frac{T}{2L^{n+1}}
<\frac{P_T^{\rm cl}}{L^n}.
\tag{43.7}
\]

첫 corner의 100-dps 회귀값은 다음과 같다. 이는 exact/calculus certificate의 대체 증명이
아니라 구현 회귀값이다.

| 양 | 자연로그 상계 |
|---|---:|
| \(B_0\) | \(-624.7547320837841\ldots\) |
| \(\kappa\) | (-631.7890814632124\ldots) |
| \(C_A\) | (-105.9189142777261\ldots) |
| (B_0+\kappa C_A) | (-624.7547320837841\ldots) |

따라서 actual identity form의 조건 (2)는 constant 1로 닫힌다.

## 6. Hypothesis 1(3): 한 residue class의 집중 상계

연속 정수 구간에서는

\[
\#\mathcal A(T;q,a)\le\frac Nq+1.
\]

\(q<T^{1/3}\), \(N\ge T/2\), \(T^{1/3}\le T/2\)이므로 \(N\ge q\)이고

\[
\boxed{\#\mathcal A(T;q,a)\le\frac{2N}{q}}.
\tag{43.8}
\]

즉 조건 (3)은 constant 2로 닫힌다.

## 7. 하나의 exceptional \(B\)

H1c-1b.2에서 fixed \(Q_1=L^A\)에 대해 하나의 exceptional modulus를 고르고 그 소인수
하나를 \(B\)로 택했다. \(B=1\)이거나 소수이며 \(B\le Q_1\)이다. (43.3)에서

\[
\log B\le A\ell<5r(100r^2+10)\le2r^5\le2L,
\]

따라서

\[
\boxed{B\le T^2}
\tag{43.9}
\]

이다. 이것은 FGKMT actual (alpha=2)의 (B) 크기 조건에 들어간다.

## 8. 닫힌 것과 열린 것

| 항목 | 판정 |
|---|---|
| actual \(\mathcal A=\mathbb Z\), identity subset Hypothesis 1(1)--(3) | `EXPLICIT`, constants 1/1/2 |
| sufficient scale | \(X\ge2\exp(10^{50})\) |
| P9.2가 요구하는 Hypothesis input | `EXPLICIT` |
| Maynard Proposition 9.2 weighted moment proof | `RATE_MISSING` |
| FGKMT Section 8 weighted lower-endpoint | `OPEN` |
| arbitrary affine form 또는 arbitrary \(\mathcal A\) Hypothesis 1 | `OPEN / NOT REQUIRED BY THIS CHILD` |
| broad `SIV-08` root | `HARD_BLOCKER` |
| `SIV-07`, `SIV-09`, \(X_{\rm cert}\) | `HARD_BLOCKER / OPEN` |

여기의 \(2\exp(10^{50})\)는 소수분포 입력 하나의 **보수적 sufficient cutoff**다. 전체 Sono
정리가 그 수부터 성립한다는 뜻이 아니며, 최종 \(X_{\rm cert}\)는 나머지 모든 proof node의
cutoff를 합친 뒤에만 정할 수 있다.

## 9. 다음 gate

다음은 `H1b-P92a`로 분리한다.

1. Maynard Proposition 9.2 proof의 actual identity-form weighted main term과 additive error
   multiplier를 원문 Section 9에서 복원한다.
2. FGKMT closed sum에서 외부 \((T,2T]\) 합으로 돌아갈 때 \(w(T)\)를 명시적으로 상계한다.
3. 이미 닫은 Hypothesis constants 1/1/2를 해당 P9.2 error formula에 대입한다.
4. 그 뒤에만 `H1B-P92`, `SIV-08` root 분해와 상태 승격을 검토한다.

새 package, Lean, 장시간 계산 또는 actual prime sweep은 필요하지 않았다. 사용자 수행절차는
**별도 수행절차 필요없음**이다.
