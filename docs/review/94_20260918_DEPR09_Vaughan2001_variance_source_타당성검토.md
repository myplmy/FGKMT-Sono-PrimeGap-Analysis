# Review 94 — DEP-R09 Vaughan 2001 variance 원문 감사 타당성검토

- 검토대상: Theory 85, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>SOURCE_IDENTITY_VALID /
  EXACT_VARIANCE_BRIDGE_VALID /
  CURRENT_REGIME_DROP_IN_REJECTION_VALID</code>

## 1. 검토 결론

Theory 85의 판정은 타당하다.

1. 새 PDF는 요청한 R. C. Vaughan 2001 PLMS 논문 원문이다.
2. Vaughan variance와 Theory 82 nonprincipal character energy 사이에는 nonnegative
   principal correction을 포함한 exact identity가 있다.
3. Theorem 1은 dyadic modulus moment이고 fixed-(A) large-(Q) 범위이므로 current
   growing (q=Y^{1/d}) family를 덮지 않는다.
4. Theorem 2는 GRH conditional이고 (Q\ge Y^{3/4+\varepsilon})라 current range와
   겹치지 않는다.
5. source constants와 cutoff도 implicit이므로 numerical (X_{\rm cert}) input은
   생기지 않았다.

## 2. PDF identity·locator 재검토

- 180,481 bytes, SHA-256
  <code>d5bc8d92c1204b09233c507b83ee185e35a54186122da1c906df87bbcb9d3ecc</code>.
- PDF 1.2, 21쪽, native text, raster image 없음.
- printed pp.533--553, title·author·journal metadata 일치.
- rendered printed p.533에서 식 (1.1)--(1.3), p.535에서 Theorems 1--2,
  p.536에서 Theorem 3과 implied-constant convention을 대조했다.

한 generic parser의 10-page 표시는 실제 PDF page tree와 rendering에 어긋나므로
기각했다. 21쪽 판정은 <code>pdfinfo.exe</code>와 page rendering 양쪽이 지지한다.

## 3. exact bridge 독립 검토

(n=\varphi(q)), (A_a=\psi(Y;q,a)), (S=\sum_aA_a)라 하자. 그러면

\[
 \sum_a|A_a-Y/n|^2
 =\sum_a|A_a-S/n|^2+|S-Y|^2/n.
\]

finite character Parseval로 nonprincipal energy는 첫 mean-centred sum의 (n)배다.
따라서

\[
 V_{\rm proj}+|S-Y|^2=nV_{\rm Vau},
 \qquad V_{\rm proj}\le nV_{\rm Vau}.
\]

Theory 85는 principal correction의 부호를 정확히 보존한다. Python rational fixture
((1,4,7)), target total 9에서는 (V_{\rm Vau}=21), mean-centred variance 18,
principal correction 3, (V_{\rm proj}=54), (3V_{\rm Vau}=63)으로 exact identity가
확인된다. 이 finite fixture는 analytic prime theorem의 대체물이 아니다.

## 4. Theorem 1 range 판정 검토

source lower range에 (Q=q), (Y=q^d)를 대입하면

\[
 A\ge\frac{(d-1)\log q}{\log(d\log q)}.
\]

우변은 fixed (d\ge2)에서 발산한다. 따라서 Theorem 1의 한 fixed (A)는 growing
primorial family 전체를 덮지 못한다. 각 modulus마다 (A)를 바꾸면
(O_{k,A})와 source cutoff도 함께 바뀌며, source는 그 dependence를 numerical하게
주지 않는다.

또한 (M_k)는 (Q/2<q\le Q) 전체의 moment다. 한 항이 moment 이하라는 finite
추출은 맞지만 source range와 implicit constant를 제거하지 않는다. Theory 85의
<code>NO FIXED-A COVERAGE</code> 판정은 필요한 범위만 기각하며, Vaughan theorem
자체나 다른 refinement를 기각하지 않는다.

## 5. Theorem 2·3 검토

Theorem 2의 lower exponent는 (3/4+\varepsilon)이고 current exponent는
(1/d\le1/21)이다. exact rational gap은 양수다. GRH도 별도 가정이므로 current
unconditional input으로 사용할 수 없다.

Theorem 3은 partial singular series에 prime-specific structure를 제공하지만
(V_{\rm Vau}) 또는 (V_{\rm proj})의 prescribed-(q) upper가 아니다. error의
(O)-multiplier와 positive (c)도 implicit하다. 관련 source와 drop-in theorem을
구분한 Theory 85의 분류는 타당하다.

## 6. 형식검증 경계

Lean은 source-derived identity를 premise로 받은 뒤 nonnegative correction을 버리는
대수, Theory 82 strict gate transfer, exponent comparison만 검사한다. finite character
orthogonality와 Vaughan analytic theorem을 local axiom으로 선언하지 않는다.

Python은 rational centering identity, range arithmetic, source hash와 OPEN flags를
검증한다. actual prime energy, dataset 또는 threshold를 계산하지 않는다.

## 7. 최종 상태

| 질문 | 판정 |
|---|---|
| 요청 Vaughan 2001 원문이 확보됐는가 | <code>YES</code> |
| project character energy로 exact 전달 가능한가 | <code>YES, WITH PRINCIPAL CORRECTION</code> |
| Vaughan Theorem 1이 current growing family를 덮는가 | <code>NO</code> |
| Theorem 2가 current unconditional branch를 덮는가 | <code>NO</code> |
| fully numerical prescribed-primorial upper가 생겼는가 | <code>NO</code> |
| numerical (X_{\rm cert}) 또는 bounded range가 생겼는가 | <code>NO</code> |
| 사용자 추가 실행이 지금 필요한가 | <code>NO</code> |

다음 최소 gate는 prime-specific fixed-primorial upper 또는 actual same-law weighted
correlation이다. GRH conditional branch를 새로 열려면 별도 사용자 결정이 필요하다.
