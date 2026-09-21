# Review 96 — DEP-R09 final-law conditional-weight 타당성검토

- 검토대상: Theory 87, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>PROOF_LAW_ATOM_TRANSFER_VALID /
  NONEMPTY_COUNT_TRANSFER_VALID /
  SUBPRIMORIAL_ENTROPY_AND_LARGE_SIEVE_REJECTION_VALID</code>

## 1. 검토 결론

Theory 87의 판정은 타당하다.

1. FGKMT Theorem 3의 abstract conclusion이 아니라 proof가 실제 구성한 식 (5.9)의
   reweighted law를 명시적으로 선택했다.
2. complete past를 조건으로 nonempty edge atom은
   \(2\kappa^{-2k}X^{-3/5}\) 이하이다.
3. stage 내부 conditional independence와 stage 사이 chain rule만 사용했으며 final
   좌표 전체의 global independence를 가정하지 않았다.
4. Theory 53의 full-residue equality 때문에 nonempty edge는 residue를 유일하게
   결정하고 empty edge는 residue 0으로 lift된다.
5. covering-good event는 edge-size cap을 통해 최소 \(K_*\)개의 nonempty 좌표를
   강제하므로 event-and-shift atom cap이 성립한다.
6. 이 개선으로 생기는 guaranteed effective denominator는 full primorial보다
   지수적으로 작은 scale이므로 raw classical large-sieve certificate는 여전히
   strict gate를 인증하지 못한다.

따라서 conditional-weight source에서 실제 진전은 얻었지만 actual same-law analytic
moment, PAP-11, DEP-R09와 numerical \(X_{\rm cert}\)는 계속 열린다.

## 2. proof-law 선택 범위

Theorem 3 statement는 support와 fixed-subset survival moment를 만족하는 law의 존재만
말한다. 식 (5.9)는 proof 안에서 특정 witness law를 구성한다. FMT application은
어떤 valid witness를 사용할지 자유가 있으므로 이 proof law를 선택하는 것은 정당하다.

반대로 모든 possible witness law가 같은 coordinate atom cap을 갖는다고 말할 수는 없다.
Theory 87은 이 범위를 정확히 구분한다.

## 3. nonempty atom 부등식 재검토

good-normalizer history에서

\[
\Pr(e'_i=E\mid W)
=\frac{\mu_i(E)1_{\{E\subset W\}}}{X_i(W)P_{j-1}(E)}.
\]

\(X_i(W)\ge1/2\), \(|E|\le2k\), \(P_{j-1}(v)\ge\kappa\)이므로

\[
\frac1{X_i(W)P_{j-1}(E)}
\le2\kappa^{-2k}.
\]

nonempty \(E\)의 한 vertex \(v\)를 택하면
\(\mu_i(E)\le\Pr(v\in e_i)\le X^{-3/5}\)이다. 따라서 Theory 87 식
(87.15)의 \(\omega_*\)가 정확하다. bad-normalizer history에서는 output이 empty라
nonempty atom에 추가 질량이 없다.

## 4. multistage chain과 residue lift

한 stage 안에서는 \(W\)를 조건으로 product law이므로 specified nonempty 좌표
\(K_j\)개가 나올 확률은 \(\omega_*^{K_j}\) 이하이다. 앞 stage edge vector를 고정하면
다음 \(W\)가 정해지므로, stage별 조건부 확률을 chain rule로 곱해
\(\omega_*^{\sum_jK_j}\)를 얻는다.

Theory 53의 output nonempty edge는
\(\{q\in V:q\equiv n'_p\pmod p\}\) 전체다. nonempty edge 안의 q 하나가 residue를
유일하게 결정하고 empty edge에는 project rule \(n'_p=0\)을 쓴다. 따라서 fixed
outer vector와 final shift는 output edge vector를 하나로 강제한다. 이 injectivity가
edge-vector atom을 shift atom으로 옮기는 데 충분하다.

## 5. covering에서 nonempty count로의 전달

retained whole set의 크기는 \(M\ge M_*\), inner-good outcome의 survivor 수는
\(Z\le(1+t)\rho M\)이다. 그러므로 적어도
\(\gamma M=M-Z\)개의 vertex가 output union에 덮인다. edge마다 최대 \(2k\)개를
덮으므로

\[
K\ge\left\lceil\frac{\gamma M}{2k}\right\rceil
\ge\left\lceil\frac{\gamma M_*}{2k}\right\rceil=K_*.
\]

\(\rho\le1/5\), \(t\le1/32\)에서 \(\gamma\ge127/160\)인 산술도 맞다.
edge overlap은 union 크기를 줄일 뿐이므로 이 lower bound를 약화하지 않는다.

## 6. effective entropy 비교

Theory 87은 \(\log Q_{\rm eff}\)를 크게 보이려고 actual \(K\)를 사용하지 않고,
source가 무조건 보장하는 \(K_*\)만 사용한다. 따라서 다음 upper가 성립한다.

\[
\log Q_{\rm eff}
<
\left(
\frac{21}{16000}
+\frac{237}{1536000}
+\frac3{500}
\right)X
=\frac{3823}{512000}X
<\frac X{100}.
\]

반면 Dusart theta lower와 \(\log B_0\le\log X=a\)는
\(\log\mathfrak q>49X/50\)을 준다. 따라서 \(Q_{\rm eff}<\mathfrak q\)다.

이것은 actual law의 entropy가 반드시 \(Q_{\rm eff}\)와 같다는 뜻이 아니다. actual
nonempty count tail이나 empty-coordinate 분산을 새로 증명하면 더 큰 effective
denominator가 가능하다. 이번 판정은 **현재 추출한 guaranteed certificate**의 한계다.

## 7. large-sieve 비교

새 gate의 가장 유리한 envelope는

\[
\frac{V_{\rm gate,87}}{Y^2}
\le e^{-4}\frac{Q_{\rm eff}}{\varphi(\mathfrak q)}
<e^{-4}\frac{\mathfrak q}{\varphi(\mathfrak q)}.
\]

Theory 83은 raw certificate가 마지막 양보다도 큼을 source-first로 증명했다.
따라서 \(V\le B_{\rm LS}\)만으로 새 strict gate도 도출할 수 없다.

이 비교는 actual \(V\)의 하한이 아니다. 더 강한 conditional-weight moment,
prime-specific cancellation 또는 direct phase transform을 배제하지 않는다.

## 8. 검증 경계

Python exact fixture는 reweighted atom \(2/9\), cap \(1/3\), covered 7 vertex에
필요한 nonempty edge 4개, adaptive-chain vector atom \(1/675\le1/81\), outer factor를
합친 event-shift cap \(1/486\)을 검사한다. 이 toy는 actual prime 계산이 아니다.

Lean은 source premise 뒤 scalar atom·raw moment·strict gate와 entropy hierarchy만
검사한다. FGKMT probability construction, real-log bounds, theta theorem과 analytic
character energy를 local axiom으로 넣지 않는다.

canonical 회귀시험 116개, Lean direct compile·full build와 전수 verification
refresh가 모두 PASS했다. 최종 inventory는 theory 88개, display 식 1,675개,
declaration 315개, 금지 proof escape 0건이다.

## 9. 최종 상태

| 질문 | 판정 |
|---|---|
| proof law가 final coordinate weight를 제공하는가 | <code>YES, CONDITIONALLY BY STAGE</code> |
| nonempty residue atom cap을 복원했는가 | <code>YES</code> |
| success event가 nonempty count floor를 주는가 | <code>YES</code> |
| same-law shift atom cap이 개선됐는가 | <code>YES</code> |
| guaranteed entropy가 full primorial 규모인가 | <code>NO</code> |
| raw classical large sieve가 새 gate를 닫는가 | <code>NO</code> |
| stronger actual-law tail·phase argument를 배제했는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) 또는 bounded range가 생겼는가 | <code>NO</code> |

다음 최소 gate는 empty-output/nonempty-count의 numerical tail 또는 reweighted local
character transform이다. 둘 다 닫히지 않으면 prime-specific fiber upper로 이동한다.
