# Review 100 — DEP-R09 weighted survivor-moment 타당성검토

- 검토대상: Theory 91, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>COMPLEX_WEIGHTED_MOMENT_VALID /
  PAIR_ERROR_SHARPNESS_VALID /
  WEIGHTED_NIBBLE_DROP_IN_REJECTION_VALID</code>

> **Successor:** review 101/Theory 92는 blind weights의 특별한 pointwise envelope를
> 사용하면 success-scale pair factor가 \(\beta\)로 정규화됨을 보였다. 아래
> arbitrary-weight operator 진단은 폐기되지 않지만 최신 root gate는 sparse centered
> mean이다.

## 1. 검토 결론

Theory 91의 판정은 타당하다.

1. complex-weighted survivor sum의 second moment는 one/two-point probabilities로
   exact하게 전개된다.
2. entrywise relative pair error \(\beta\)만 사용하면
   \(\beta\rho^2(M_V-1)\sum|b|^2\) loss가 생긴다.
3. common-shock finite law가 이 scaling을 exact하게 달성한다.
4. current parameter에서는 diagonal 대비 상대 pair loss
   \(\beta\rho M_V>1\)이라 small covariance certificate가 아니다.
5. Gould--Kelly Theorem 1.4는 genuinely weighted pseudorandom result지만 current
   variable-size indexed covering law의 numerical probability moment가 아니다.

따라서 direct weighted moment에는 covariance-operator 또는 prime-specific
event-energy theorem이 새로 필요하다.

## 2. weighted second moment

\[
S_b=\sum_vb_vX_v
\]

를 전개하면 diagonal은 \(p_v|b_v|^2\), ordered off-diagonal은
\(p_{vw}b_v\overline{b_w}\)다. ideal \(\rho^2\) pair matrix를 더하고 빼고

\[
\left(\sum|b_v|\right)^2\le M_V\sum|b_v|^2
\]

를 쓰면 Theory 91 식 (91.5)가 나온다. complex conjugation과 ordered/unordered
factor 2가 exact fixture에서 일치한다.

## 3. sharpness witness

latent probability \(1/8\) 또는 \(3/8\)을 각각 확률 \(1/2\)로 고른 뒤 conditionally
iid Bernoulli를 뽑으면 marginal은 \(1/4\), pair는 \(5/64\)다. relative pair error는
\(1/4\).

\(M_V=4\), all-one weights에서 exact moment는 \(31/16\), independent baseline은
\(28/16\), excess는 \(3/16\)이다. 이는

\[
\beta\rho^2M_V(M_V-1)
\]

와 같다. 따라서 entrywise pair constraints만으로 \(\beta M_V\) factor를 없앨 수 없다.

## 4. project scale

Theory 53에서 \(\beta\ge6/b\), \(\rho\ge1/b\),
\(M_V>78cXb/a\)다. 따라서

\[
\beta\rho M_V>\frac{468cX}{ab}>1
\]

이다. 이는 actual covariance lower가 아니라 source certificate의 row-sum/spectral
loss가 small하지 않다는 판정이다.

## 5. Gould--Kelly 적용성

Theorem 1.4는 uniform nearly-regular hypergraph에서 matching을 찾고, preselected
nonnegative vertex weights의 leftover mass를 보존한다. current object는

- variable-size indexed random edge families,
- same-stage overlap을 허용하는 covering,
- history-dependent probability law,
- complex blind prime-error weights,
- numerical failure mass

를 요구한다.

따라서 source theorem을 literal drop-in할 수 없다. complex weights를 네 nonnegative
parts로 나누는 것만으로 uniformity·matching·law·constant 문제는 해결되지 않는다.

## 6. 판정 범위

배제되는 것:

- current entrywise 1·2점 errors만으로 arbitrary complex covariance를 작게 만드는 방식,
- Gould--Kelly qualitative theorem을 current numerical same-law result로 인용하는 방식.

배제되지 않는 것:

- formula (5.9) 구조를 더 사용하는 covariance-operator theorem,
- blind \(B(v)\)에 특수한 mean/L2 cancellation,
- construction redesign을 별도 승인해 weighted matching theorem을 재적용하는 방식.

## 7. 검증 경계

Python은 rational Gaussian weights와 finite probability table을 전수한다. actual
prime data나 large hypergraph는 만들지 않는다.

Lean은 scalar inequalities와 rational witness만 검사한다. source probability law와
Gould--Kelly theorem을 local axiom으로 넣지 않는다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| weighted moment interface가 exact한가 | <code>YES</code> |
| current pair errors가 충분히 작은가 | <code>NO</code> |
| \(\beta M\) loss를 입력만으로 제거 가능한가 | <code>NO</code> |
| weighted nibble drop-in이 있는가 | <code>NO</code> |
| blind weighted correlation이 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 범위가 생겼는가 | <code>NO</code> |

다음 gate는 blind prime-error weights의 deterministic mean/L2 source theorem 또는
actual law covariance-operator theorem이다.
