# DEP-R09 Jutila JL7 주잔여항·높이 행합 타당성검토

- 작성일: 2026-09-13 KST
- 대상: [Theory 69](../method/theory/69_Sono_FMT_DEPR09_Jutila_JL7_principal_residue_height_row_sum.md)
- 판정: **JL7-RES 범위에서 타당함**
- 증거 수준: peer-reviewed exact source + 표준 Gamma identity + project direct finite proof +
  high-precision 독립 적분 대조 + Lean coefficient verification

## 1. 이번에 무엇이 진전됐는가

Jutila p.53은 주잔여항이 원하는 크기라고 쓰지만 그 앞의 상수를
\(\ll_\theta\) 안에 숨긴다. Theory 69는 원문 대각식과 영점 선택 규칙을 바꾸지 않고

\[
 |\mathcal R|<52J(\varphi(q)/q)^2x^{2-2\alpha}L^2
\]

라는 actual-range 상계를 만들었다. 따라서 `JL7-RES`를
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 올리는 것은 타당하다.

> **쉬운 설명:** 원 논문의 잔여항은 큰 계산에서 생기는 “추가 비용”이다. 지금은 그 비용이
> 얼마를 넘지 않는지 숫자로 정했다. 그러나 모든 비용을 합친 뒤 원래의 양의 주항보다
> 작은지 확인하는 다음 단계는 아직 남았다.

## 2. 비판적으로 확인한 핵심 오류 가능성

### 2.1 Lemma 3 상수 3을 residue에 이중 적용하는 오류

Theory 68의 \(3R^2\)는 절댓값 \(h\)-합을 쓰는 contour error용이다. residue에는 부호를
보존한 \(\sum_d h(d)/d\)를 써서 \(r=r'\)만 남는다. 따라서 residue에는 별도
\(S_q(R)=\sum'\varphi(r)/r^2\)를 사용해야 한다. Theory 69는 두 경로를 분리했으므로
상수 3을 이중으로 곱하지 않았다.

### 2.2 \(z=0\)에서 Gamma pole을 그대로 평가하는 오류

\(j=k\)이고 \(\Re s_j=0\)이면 \(z=0\)일 수 있다. \(\Gamma(-z)\)만 보면 pole이지만,
\(e^{-\xi z}-e^{-\eta z}\)와 곱하면 제거된다. 식 (69.9)는 먼저 두 함수를 함께
변형하고 \(z=0\)을 유한 triple integral로 정의한다. Python도 이 removable value를
별도 branch로 계산한다.

### 2.3 서로 다른 character까지 height spacing으로 합치는 오류

원문의 restriction은 \(\bar\chi_j\chi_k=\chi_0\)이므로 같은 character만 남는다.
spacing 행합도 같은 character 안에서만 적용했다. character가 다르면 높이가 같을 수
있으므로 이 제한을 버리면 식 (69.17)은 거짓일 수 있다.

### 2.4 even·odd strip을 한 well-spaced system처럼 보는 오류

인접 strip의 선택점은 arbitrarily 가까울 수 있다. Jutila가 even과 odd strip을 나누는
이유가 바로 이것이다. Theory 69의 \(J\)와 행합은 parity system 하나에만 적용된다.
두 system을 합치는 factor 2는 terminal 단계에 명시적으로 남겼다.

### 2.5 Δ 간격에서 항 개수만 세는 과도한 손실

local count만 써서 모든 pair를 같은 최악값으로 잡으면 \(J^2\) 손실이 생길 수 있다.
고정 행에서 \(m\)번째 이웃은 적어도 \(m\Delta\) 떨어진다는 순서를 보존하면
\(2\sum m^{-2}\)만 남고 \(J\) scale이 유지된다. 이는 Jutila의 최종 크기와도 일치한다.

### 2.6 \(S_q(R)\)에서 \(\varphi(q)/q\)를 잃는 오류

coprimality를 단순히 버리면 \(S_q(R)=O(L)\)만 얻어 p.53의
\((\varphi(q)/q)^2\) 구조를 잃는다. Theory 69는 excluded Euler factors를
\(\varphi(q)/q\)와 비교하여 그 구조를 보존하고, 남는 ratio만 \(e\)로 잡았다.

## 3. 상수 52의 독립 계산

세 구성요소는 다음과 같다.

1. 같은 character의 한 영점 행: \(<91\theta L^3\).
2. 대각 \(r\)-합: \(<12(\varphi(q)/q)L\).
3. 원문 바깥 factor: \(L^{-2}(\varphi(q)/q)x^{2-2\alpha}\).

따라서 \(12\cdot91\theta=1092\theta\le52\)다. endpoint에서 나눗셈이 정확히
\(1092/21=52\)이므로 decimal rounding을 쓰지 않았다.

Python 검증은 \(L=441,\theta=1/21\)의 가장 빡빡한 endpoint에서 interval 상계,
finite \(r\)-합과 excluded-prime product를 검사했고, 복소 \(z\) 두 점에서 closed kernel을
Fubini로 분리한 두 개의 독립 1차원 quadrature와 70 dps로 대조한다. 이 검사는 일반 증명의 대체가 아니라
부호·endpoint·closed-form 구현 오류를 잡는 역할이다.

## 4. source와 형식검증의 경계

Jutila 원문은 peer-reviewed exact source지만, scan에는 쓸 만한 text layer가 없어
렌더링 원페이지 대조가 필수였다. DLMF의 Gamma recurrence·Euler integral은 정확한 표준식이다.
표적 문헌 검색에서 p.53 residue용 숫자 multiplier를 바로 주는 drop-in 정리는 찾지 못했기
때문에 직접 유한 상계를 택했다. 이 검색 결과를 novelty 주장으로 확대하지 않는다.

Lean은 rational interval coefficient, \(40/19<3\), Basel coefficient,
\(91\)과 \(52\)의 합성을 검사한다. 복소 Gamma 이론, Dirichlet character와 원문 strip
selection 전체, Euler-product convergence는 아직 Lean에서 source부터 증명하지 않는다.
이를 `axiom`, `sorry`, `admit`으로 덮지 않고 상태 원장에 PARTIAL/SOURCE로 남기는 것이
적절하다.

## 5. 아직 결론내릴 수 없는 것

이번 결과는 다음을 뜻하지 않는다.

- Jutila 식 (3.6)의 terminal inequality가 이미 닫혔다는 뜻
- variable-modulus 식 (3.7)이 같은 상수로 자동 성립한다는 뜻
- Gallagher--Maier pointwise PAP가 numerical cutoff와 함께 증명됐다는 뜻
- Sono의 fixed \(2\times10^{-17}\)이 독립 인증됐다는 뜻
- numerical \(X_{\rm cert}\)를 계산할 준비가 끝났다는 뜻

올바른 다음 작업은 `JL7-ABSORB`다. 지금까지 복원한 weighted lower bound, contour,
Lemma 3 error, residue와 even/odd factor를 한 strict \(A-E>0\) inequality에 넣어 공통
finite cutoff를 얻어야 한다. 그 뒤에도 averaged replay와 PAP bridge가 남는다.

## 6. 최종 판정

| 항목 | 판정 |
|---|---|
| 원문 식·페이지 고정 | PASS |
| 대각 \(r\)-합과 \(\varphi(q)/q\) 보존 | PASS |
| removable Gamma pole 처리 | PASS |
| 같은-character·같은-parity spacing 범위 | PASS |
| calculator-safe residue multiplier 52 | PASS |
| terminal density 전체 | OPEN |
| PAP-11·DEP-R09·fixed 계수·\(X_{\rm cert}\) | OPEN |

따라서 `JL7-RES`만 닫는 제한된 승격은 타당하고, 다음 단계로 확대 해석하면 안 된다.

## 7. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- NIST DLMF, [§5.5](https://dlmf.nist.gov/5.5),
  [§5.9](https://dlmf.nist.gov/5.9).
