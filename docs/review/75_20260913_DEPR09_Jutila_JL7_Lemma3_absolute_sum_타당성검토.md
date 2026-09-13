# DEP-R09 Jutila JL7 Lemma 3 absolute-sum 타당성검토

- 작성일: 2026-09-13 KST
- 대상: [Theory 68](../method/theory/68_Sono_FMT_DEPR09_Jutila_JL7_Lemma3_absolute_sum.md)
- 판정: **수학적으로 타당하며 JL7-LEMMA3만 닫음**
- 증거 수준: peer-reviewed source statement + project direct finite proof +
  exact-arithmetic tests + Lean finite-algebra verification

## 1. 무엇을 확인했는가

Jutila는 소수 \(p\)마다 생기는 작은 계수를 \(h(d;r,r')\)라는 하나의 함수로 묶었다.
원문은 각 \((r,r')\)에 대한 상계를 정확히 주지만, 모든 \(r,r'\le R\)을 더한 뒤의
숫자 상수는 \(\ll\) 안에 숨겼다.

이번 검토는 그 마지막 유한합을 다시 계산해

\[
 \sum_{r,r'\le R}'\frac1{rr'}\sum_d|h(d;r,r')|<3R^2
\]

를 얻은 과정이 맞는지 확인한 것이다.

> **쉬운 설명:** 작은 부품 하나의 무게 제한은 원 논문에 있었지만, 부품 상자 전체의
> 최대 무게가 숫자로 적혀 있지 않았다. 이번에는 상자 전체가 \(3R^2\)보다 가볍다는
> 안전한 숫자를 붙였다.

## 2. source-first 판정

Jutila printed pp.48--49의 Lemmas 2--3은 필요한 두 식을 직접 명시한다.

1. 부호를 유지한 합은 \(r=r'\)일 때만 남는다.
2. 절댓값 합은
   \(\prod_{p\mid r}(p+1)\prod_{p\mid r'}(p+1)\) 이하이다.

Jutila가 선행 경로로 언급한 Motohashi 문헌도 조사했다. 공식 J-STAGE의 1975년
발표문 p.816에는 같은 pseudocharacter와 두 \((p+1)\) 곱이 나타난다. 그러나
\(h(d;r,r')\)의 절댓값 합과 현재 endpoint 합성을 더 자세히 주지는 않는다.

따라서 Motohashi 문헌을 없는 stronger theorem처럼 사용하지 않고, peer-reviewed
Jutila statement를 직접 입력으로 삼은 판단은 타당하다.

## 3. 가장 중요한 다섯 가지 오류 가능성

### 3.1 공통 소수 \(p=2\)

\(p\mid(r,r')\)이면 local coefficient는 \(p(p-2)\)이다. \(p=2\)에서는 0이므로
local polynomial은 1이다. 절댓값 계수합도 0이 아니라 1이다.

Theory 68은 이를 \((p-1)^2=1\)로 처리했고 exact Python 전개도 같은 값을 냈다.
따라서 이 특수 경우를 빠뜨리지 않았다.

### 3.2 \(d\)-합의 끝점

각 local polynomial은 \(p^{-s}\)의 차수 1이므로 \(h(d;r,r')\)는
\({\rm lcm}(r,r')\)의 squarefree divisor에서만 0이 아닐 수 있다. 따라서

\[
 d\le{\rm lcm}(r,r')\le rr'\le\lfloor R\rfloor^2.
\]

무한히 많은 \(d\)를 실제로 더하는 문제가 없고, 숨은 tail도 없다.

### 3.3 \(R\)이 정수가 아닐 때

원문의 합은 정수 \(r,r'\)에 대한 것이므로 정확한 endpoint는
\(K=\lfloor R\rfloor\)이다. 증명은 먼저 \(3K^2\)를 얻고 \(K\le R\)로
\(3K^2\le3R^2\)를 사용한다. \(R\)을 잘못 반올림하지 않았다.

### 3.4 항마다 최악값을 곱해 생기는 가짜 로그

\(\prod_{p\mid r}(1+1/p)\)를 각 \(r\)마다 별도로 거칠게 잡으면
\(\log R\) 같은 불필요한 손실이 생길 수 있다. Theory 68은

\[
 \sum_{n\le K}\sum_{d\mid n}\frac1d
 =\sum_{d\le K}\frac{\lfloor K/d\rfloor}{d}
\]

로 합의 순서를 바꾼다. 이는 유한합의 정확한 double-counting이다.
그 결과 원문이 필요로 한 \(R^2\) scale을 보존한다.

### 3.5 Basel 상계의 방향

\[
 \sum_{d\le K}\frac1{d^2}\le\frac{\pi^2}{6}<\frac53
\]

이므로 outer sum은 \(5K/3\)보다 작다. 이를 제곱하면 \(25K^2/9\)이고,
\(25/9<3\)이다. 상한·하한 방향이 뒤집히지 않았다. 이 부분은 Mathlib의
hasSum_zeta_two와 Real.pi_lt_d2를 사용해 Lean kernel에서도 확인한다.

## 4. exact-arithmetic 검증이 보여 준 것

새 Python 검증기는 floating point를 쓰지 않고 Fraction과 정수만 사용한다.

- \(r,r'\le50\)의 모든 squarefree pair에서 exact local coefficient를 전개했다.
- 절댓값 계수합이 local-product 식과 같은지 확인했다.
- Jutila의 printed product bound를 넘지 않는지 확인했다.
- \(\sum h(d)/d=\delta_{r,r'}\varphi(r)\)를 확인했다.
- 여러 \(K,q\)에서 actual sum, source-product square, \(3K^2\)의 순서를 확인했다.
- downstream residue·terminal·PAP·\(X_{\rm cert}\) flag는 모두 false로 고정했다.

이 toy 전수검사는 일반 증명의 대체물이 아니다. 다만 local 부호, \(p=2\), support와
코드 구현 오류를 독립적으로 잡아 준다.

## 5. 상수 3은 얼마나 보수적인가

상수 3은 최적화 목표가 아니다. 실제로는
\(\sum_{d\ge1}d^{-2}=\pi^2/6\)보다 squarefree·coprime 제한 때문에 더 작고,
공통 소수에서는 \((p-1)^2\)가 printed \((p+1)^2\)보다 작다.

그러나 현재 가장 큰 불확실성은 다음 residue multiplier와 최종 cutoff다.
이 단계에서 상수 3을 조금 줄이기 위해 복잡한 새 정리를 도입하는 것보다,
오류 가능성이 낮은 rational bound를 보존하고 다음 hard blocker를 닫는 편이
연구 효율상 타당하다. 나중에 전체 \(X_{\rm cert}\) 민감도 분석에서 이 상수가
지배적이라고 확인될 때만 exact Euler-product 평균으로 재최적화하는 것이 좋다.

## 6. \(X_{\rm cert}\)에 대한 의미

Theory 67의 contour 상계와 합치면 calculator-safe multiplier는

\[
 144\left(1+\frac1\theta\right)\left(\frac2\theta+1\right)
\]

이고 \(\theta=1/21\)에서 136,224이다. 하지만 다음 항목이 남았다.

- principal residue와 대각 조건
- 같은 character에 여러 zero height가 있을 때의 row sum
- 마지막 \(J^2\) 항을 흡수하는 strict cutoff
- variable-modulus averaged replay
- Gallagher--Maier PAP bridge

따라서 이번 결과로 numerical \(X_{\rm cert}\)를 계산하거나 fixed
\(2\times10^{-17}\)을 인증하면 안 된다. 올바른 판정은
JL7-LEMMA3만 ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT이고 나머지는 OPEN이다.

## 7. 권장 다음 작업

다음은 JL7-RES source-first 감사다. 먼저 Jutila p.53 residue 식에서
\(\delta_{r,r'}\)로 살아남는 대각항을 정확히 쓰고, 같은 character가 여러 높이에서
반복될 때 Lemma 8의 local count가 주는 row cardinality를 숫자로 합성해야 한다.
이 값이 나온 뒤에만 Theory 66의 \(A-E>0\) absorption cutoff를 계산할 수 있다.

## 8. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- Y. Motohashi, *On a Density Theorem of Linntik*, Proc. Japan Acad.
  51 Supplement (1975), 815--817,
  DOI [10.2183/pjab1945.51.Supplemnt_815](https://doi.org/10.2183/pjab1945.51.Supplemnt_815).
