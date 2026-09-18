# Review 95 — DEP-R09 same-law outer-fiber minimax 타당성검토

- 검토대상: Theory 86, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>ACTUAL_LAW_REDUCTION_VALID /
  MINIMAX_SCOPE_VALID /
  ANALYTIC_CLOSURE_NOT_ACHIEVED</code>

## 1. 검토 결론

Theory 86의 판정은 타당하다.

1. FMT outer vector는 정확히 균등하고 final extension에서 보존된다.
2. actual conditional inner output과 sieve-good event가 outer draw에 적응적으로
   의존해도 raw moment는 support-restricted outer-fiber maximum의 평균 이하이다.
3. 서로 다른 outer vector의 CRT shift support는 겹치지 않으므로 이 fiber energy는
   Theory 82의 full residue energy 이하이다.
4. 각 fiber maximizer에 질량 1을 주는 abstract law가 equality를 만들므로, outer
   marginal과 support만 사용하는 보편 상계로는 더 개선할 수 없다.
5. 이 sharpness는 actual FMT conditional law가 worst case라는 뜻이 아니며, actual
   fiber energy의 numerical upper도 아직 없다.

따라서 same-law target은 더 약해졌지만 PAP-11, DEP-R09, fixed coefficient와 numerical
\(X_{\rm cert}\)는 계속 열린다.

## 2. probability algebra 재검토

\({\cal A}\)의 크기는 \(Q_{\cal S}\)이고 각 \(\boldsymbol a\)의 질량은
\(Q_{\cal S}^{-1}\)이다. conditional event-and-shift mass를
\(\lambda_{\boldsymbol a}(m)\)라 하면 비음수이고 fiber별 총합이 1 이하이다. 따라서

\[
 \sum_m\lambda_{\boldsymbol a}(m)|R(m)|^2
 \le
 \left(\sum_m\lambda_{\boldsymbol a}(m)\right)
 \max_m|R(m)|^2
 \le\max_m|R(m)|^2.
\]

outer vector를 평균하면 Theory 86 식 (86.3)이 정확히 나온다. event와 shift의
독립성은 필요 없다.

## 3. support와 disjointness 재검토

Theory 86은 inner CRT residue 전체를 support라고 과장하지 않고 actual conditional
essential support의 image \({\cal M}(\boldsymbol a)\)만 사용한다. final shift는 모든
\(s\in{\cal S}\)에서 \(m\equiv-a_s\pmod s\)이므로 한 shift가 두 outer fiber에
동시에 속하면 두 outer vector가 모든 좌표에서 같아야 한다. 따라서 fiber들은
disjoint하고

\[
 {\cal H}_{\rm FMT}(R)
 \le\sum_{m\bmod q}|R(m)|^2
\]

가 성립한다. Theory 82의 full-energy route를 폐기하지 않고 그 앞에 더 작은 target을
삽입한 구조다.

## 4. strict gate 재검토

Theory 81의 \(M_{\min}\) floor와 raw moment는 모두 같은 \(S_{\rm sieve}\) event에서
사용된다. 따라서

\[
 {\cal H}_{\rm FMT}(R)
 <\tau^2p_*Q_{\cal S}M_{\min}^2Y^2
\]

이면 normalized moment가 strict하게 \(\tau^2p_*\)보다 작다. equality boundary를
통과로 처리하지 않은 점도 맞다.

## 5. minimax 문구의 범위

finite nonempty fiber마다 maximizer를 하나 선택하고 그 점에 conditional mass 1을
두면 outer 평균은 fiber-maximum 평균과 같다. 이 witness가 증명하는 것은 다음뿐이다.

> outer uniform marginal, conditional support, row mass upper 1만으로 유도하는 모든
> observable-independent 보편 상계 중 식 (86.3)은 sharp하다.

actual FMT law에는 추가 conditional probability와 hypergraph 구조가 있으므로 그 law가
실제로 equality를 만든다는 결론은 나오지 않는다. Theory 86과 machine ledger는 이
비주장을 명시해 과잉 결론을 피했다.

## 6. source 양화사 재검토

- FMT printed p.12의 outer \(A_s\)는 독립 균등이다.
- printed p.11의 final \(\mathbf N'\)는 outer value를 고정한 뒤 covering theorem으로
  얻는다.
- formula (6.17)의 conditional product law는 preliminary \(n_p\)에 관한 것이고,
  final covering output의 global product law가 아니다.
- FMT Theorem 4·FGKMT Corollary 4의 fixed \(Q''\) cardinality 결론은
  output-dependent complex CRT phase의 numerical moment가 아니다.

따라서 source보다 강한 independence를 추가하지 않았고, 반대로 source의 conditional
support를 무시해 full inner residue를 허용하지도 않았다.

## 7. 검증 경계

Python은 modulo-30 toy, arbitrary event subprobability, deterministic maximizer,
strict boundary와 source hash를 exact rational arithmetic으로 검사한다. toy의
\({\cal H}=154\), full energy \(324\), sharp raw moment \(77/3\)은 analytic prime
계산이 아니다.

Lean은 premise가 주어진 뒤의 scalar composition만 검사한다. FMT probability law,
argmax, character orthogonality 또는 prime-error estimate를 local axiom으로 넣지 않는다.

전수 verification refresh는 theory 87개, display 식 1,630개, declaration 307개,
금지 proof escape 0건으로 PASS했다. <code>CONDITIONAL_KERNEL_PASS=83</code>은 analytic
fiber premise의 참을 인증하는 표시가 아니라 그 premise 뒤 terminal 합성만 검증했다는
뜻이다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| actual same-law raw moment target이 더 약해졌는가 | <code>YES</code> |
| reduction이 final adaptive inner law를 보존하는가 | <code>YES</code> |
| outer-only envelope의 sharpness 범위가 정확한가 | <code>YES</code> |
| actual FMT law의 fiber moment가 수치화됐는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 또는 bounded range가 생겼는가 | <code>NO</code> |
| actual 계산·threshold calculator가 필요한 단계인가 | <code>NO</code> |

다음 최소 gate는 actual final-law conditional weights 또는 prime-specific support
structure를 사용해 \({\cal H}_{\rm FMT}(R)\)보다 실질적인 numerical upper를 얻는 것이다.
