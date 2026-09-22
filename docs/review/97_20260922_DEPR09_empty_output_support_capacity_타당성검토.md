# Review 97 — DEP-R09 empty-output·support-capacity 타당성검토

- 검토대상: Theory 88, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>FINAL_SUPPORT_CAPACITY_VALID /
  SUCCESS_MASS_PIGEONHOLE_VALID /
  EMPTY_TAIL_ARCHITECTURE_REJECTION_VALID</code>

## 1. 검토 결론

Theory 88의 판정은 타당하다.

1. current final residue construction에서 변할 수 있는 coordinate는
   \({\cal S}\)와 \(P'\subset(X/2,X]\)뿐이다.
2. 따라서 final shift support는 \(H_{\rm res}=Q_{\cal S}\prod_{p\in P'}p\)
   이하이다.
3. sieve-good mass \(p_*\)를 at most \(H_{\rm res}\)개 shift atom에 나누므로
   최대 joint atom은 \(p_*/H_{\rm res}\) 이상이다.
4. 어떤 improved empty-output tail도 atom-gate entropy factor
   \(p_*/\alpha\)를 \(H_{\rm res}\)보다 크게 만들 수 없다.
5. explicit scale에서 \(\log H_{\rm res}<51X/100\)이고 full primorial은
   \(\log\mathfrak q>49X/50\)이므로 support는 strict하게 subprimorial이다.
6. 따라서 empty-tail + maximum atom + full residue energy + raw classical
   large sieve의 조합은 새 strict gate도 인증하지 못한다.

이 결과는 local character-phase cancellation 또는 direct correlation을 배제하지 않는다.

## 2. final support audit

FMT final extension은

\[
a_p=A_p\ (p\in{\cal S}),\qquad
a_p=N'_p\ (p\in P'),\qquad
a_p=0\ (p\notin{\cal S}\cup P')
\]

로 되어 있다. 각 randomized coordinate의 가능한 값 수를 해당 prime으로 상계하면

\[
\#\operatorname{supp}(m_\omega)
\le
\prod_{s\in{\cal S}}s\prod_{p\in P'}p
=H_{\rm res}.
\]

독립성이나 full coordinate support는 필요 없다. 실제 support가 더 작으면 이후
capacity bound는 더 강해진다.

## 3. event pigeonhole 재검토

\(\lambda_r=\Pr(S_{\rm sieve},m_\omega=r)\)라 하자. event mass lower를 버리지 않으면

\[
p_*\le\sum_r\lambda_r
\le H_{\rm res}\max_r\lambda_r.
\]

따라서 \(\max_r\lambda_r\ge p_*/H_{\rm res}\)다. 모든 atom의 upper가
\(\alpha\)라면

\[
\frac{p_*}{\alpha}\le H_{\rm res}.
\]

이 bound는 event mass가 support 전체에 균등하게 놓일 때 equality를 허용하므로
support cardinality만 사용하는 논증으로 개선할 수 없다.

## 4. empty-output source 판정

normalizer-good history의 empty atom은 original empty mass
\(\mu_i(\varnothing)\)와 \(X_i(W)\)에 의존한다. normalizer-bad history에서는
output을 empty로 둔다. checked source에는 모든 coordinate와 history에 공통인
strict upper \(<1\)이 없다.

그러므로 numerical empty-count tail 자체는 이번 단계에서 얻지 못했다. 그러나
Theory 88은 더 강하게, 모든 \(P'\) coordinate가 nonempty이고 최적으로 분산된다고
가정해도 support ceiling을 넘을 수 없음을 사용한다. tail 부재를 성급한 blocker로
삼은 것이 아니다.

## 5. support scale 산술

outer support는

\[
\log Q_{\cal S}<\frac{21}{16000}X.
\]

Theory 47의 dyadic prime count에서

\[
\#P'\le\frac{1003X}{2000a},
\qquad
\log\prod_{p\in P'}p
\le a\,\#P'
\le\frac{1003}{2000}X.
\]

따라서

\[
\frac{\log H_{\rm res}}X
<
\frac{21}{16000}+\frac{1003}{2000}
=\frac{1609}{3200}
<\frac{51}{100}.
\]

Theory 87의 \(\log\mathfrak q>49X/50\)와 비교하면 \(H_{\rm res}<\mathfrak q\)다.
각 coefficient의 부등호 방향과 success mass factor가 보존됐다.

## 6. large-sieve architecture 판정

event atom cap \(\alpha\)와 full energy를 합친 gate는

\[
V_{\rm gate}(\alpha)
=
\tau^2\frac{p_*}{\alpha}
\frac{M_{\min}^2Y^2}{\varphi(\mathfrak q)N^2}.
\]

\(p_*/\alpha\le H_{\rm res}\), \(\tau\le e^{-2}\), \(M_{\min}\le N\)에서

\[
\frac{V_{\rm gate}(\alpha)}{Y^2}
\le e^{-4}\frac{H_{\rm res}}{\varphi(\mathfrak q)}
<e^{-4}\frac{\mathfrak q}{\varphi(\mathfrak q)}.
\]

Theory 83의 raw RHS는 마지막 양보다 크다. 따라서 그 upper certificate만으로
strict gate를 도출하지 못한다.

이는 actual \(V\)의 하한이 아니며 atom별 energy correlation을 버리는 단계가
병목이라는 뜻이다.

## 7. 판정이 배제하지 않는 경로

- event atom이 큰 residue에서 \(|R(r)|^2\)가 작은 직접 correlation
- formula (5.9)의 local character Fourier transform
- support-restricted prime-specific variance
- current proof와 다른 residue randomization construction
- pointwise PAP 또는 별도 analytic architecture

따라서 “empty tail로는 안 된다”를 “same-law route 전체가 불가능하다”로 확대하면 안 된다.

## 8. 검증 경계

Python exact fixture는 outer support 6, inner support 35, total support 210과
event mass \(3/5\)에서 minimum max atom \(1/350\), best entropy factor 210을
확인한다. coefficient

\[
\frac{21}{16000}+\frac{1003}{2000}
=\frac{1609}{3200}
<\frac{51}{100}
<\frac{49}{50}
\]

도 exact rational arithmetic으로 검사한다. actual prime list를 만들지 않는다.

Lean은 source premise 뒤 finite scalar implication만 검사한다. final support의 CRT
enumeration, prime-count theorem과 character energy를 local axiom으로 넣지 않는다.

canonical 회귀시험 143개, Lean direct compile·full build와 전수 verification
refresh가 모두 PASS했다. 최종 inventory는 theory 89개, display 식 1,705개,
declaration 320개, 금지 proof escape 0건이다.

## 9. 최종 상태

| 질문 | 판정 |
|---|---|
| numerical empty-output tail을 얻었는가 | <code>NO</code> |
| tail이 없어 판정 불가인가 | <code>NO, SUPPORT CEILING IS STRONGER</code> |
| any empty tail이 atom/full-energy/raw-LS route를 구제하는가 | <code>NO</code> |
| local phase/direct correlation도 배제되는가 | <code>NO</code> |
| actual same-law moment가 닫혔는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 또는 bounded range가 생겼는가 | <code>NO</code> |

다음 최소 gate는 reweighted local Dirichlet-character transform 또는 동등한
direct phase-correlation theorem이다.
