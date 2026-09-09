# H1c-1b.4a Bordignon source normalization 타당성 검토

- 검토일: 2026-09-09 KST
- 대상: Bordignon 2021 Theorem 1.2 상수의 \(X_0/Y_0\)·first-term 표기와 actual
  growing-\(A\) 적용 가능성
- 최종 판정:
  `CORRECTION PATH MATHEMATICALLY VALID / PRINTED NUMERICAL CONSTANT NOT DROP-IN`
- 정식화:
  [`docs/method/theory/38_Sono_FMT_H1c1b4a_Bordignon_source_normalization.md`](../method/theory/38_Sono_FMT_H1c1b4a_Bordignon_source_normalization.md)

## 1. 한눈에 보는 판정

| 질문 | 판정 | 이유 |
|---|---|---|
| \(X_0/Y_0\) 표기는 그대로 일관적인가 | 아니오 | 정리·상수식·Theorem 1.4의 세 번째 인자가 충돌 |
| type-safe하게 고칠 수 있는가 | 예 | \(Y_0=\log\log X_0\)를 명시한 두 동치 표기로 분리 가능 |
| 최종 식 (33)의 첫 항은 유한 \(C\)를 주는가 | 아니오 | absolute \(R^*\)에 \(x\)-정규화가 없음 |
| arXiv v1 식을 대신 쓰면 되는가 | 아니오 | 최종식과 다르고 exact target이 요구하는 factor와도 같지 않음 |
| 필요한 remainder factor를 복원할 수 있는가 | 예 | Theorem 3.4와 Theorem 1.2 target에서 직접 유도 |
| actual numerical \(C_A\)가 나왔는가 | 아니오 | growing \(A\)에서 \(R^*\) 전 항의 uniform 상계가 남음 |
| 논문의 Theorem 1.4 전체를 폐기해야 하는가 | 아니오 | 12항 식은 valid upper \(C_A\)를 외부 입력하면 parameterized 사용 가능 |
| H1(2), P9.2, \(X_{\mathrm{cert}}\)가 닫혔는가 | 아니오 | density·full absorption·source reproof가 남음 |

## 2. 사용자 제안 방식의 타당성

필요한 lemma를 먼저 선행연구에서 찾고, 맞는 drop-in이 없을 때만 직접 증명하는 순서는 이번
사례에서도 타당했다. 다만 “출판 논문이니 표시식을 그대로 사용한다”는 방식은 안전하지 않았다.
최종판과 저자 초고를 함께 대조하자 같은 위치의 식이 서로 다르고, 어느 것도 현재 exact target과
그대로 일치하지 않는다는 사실이 드러났다.

따라서 이번 직접 유도는 기존 정리를 불필요하게 재증명한 것이 아니다. source formula가
현재 적용에 필요한 정규화를 제공하지 못하는 정확한 연결부만 다시 증명했다.

## 3. 출판식 문제의 강도

### 3.1 \(X_0/Y_0\) 충돌

이 부분은 표기 오자로 보고 안전하게 우회할 수 있다. \(X_0\)는 실제 \(x\)의 시작점이고
\(Y_0\)는 그 시작점의 \(\log\log\) 좌표다. 두 값을 type-safe하게 분리하면 source 정리의
유효범위를 약화하거나 넓히지 않는다.

### 3.2 식 (33)의 첫 항

이 부분은 이름만 바꾸어 해결되지 않는다. 최종식의 \(R^*\)가 Theorem 3.4와 같은 absolute
remainder라면 \(x\)로 나누지 않은 식은 finite constant의 정의가 될 수 없다. 반대로 이를
다른 정규화된 \(R\)이라 해석하면 식에 적힌 세 인자 \((x,T,q)\)와 Theorem 3.4 참조가 맞지
않는다.

따라서 “명백한 오자이므로 v1 식을 쓴다”는 결론도 과도하다. v1의 식은 최종식보다
보수적일 수 있지만, 최종 Lemma 3.1과 exact target에서 자연스럽게 나오는 식은
\(R^*T/(x\log^3x)\)이기 때문이다.

## 4. 직접 유도의 검증

Theorem 1.2 target의 오른쪽 \(C/(\log x)^{\alpha_2}\)와 비교하려면 absolute error를
먼저 \(x\)로 나누고 \((\log x)^{\alpha_2}\)를 곱해야 한다. character 수를
\(\varphi(q)\le q\)로 덮으면

\[
q(R^*/x)(\log x)^{\alpha_2}.
\]

그 뒤에만 \(q\le(\log x)^{\alpha_1}\)를 적용한다. 이 순서는 단위, q multiplicity와 target
rate를 모두 보존한다. 코드 test는 explicit q와 q-envelope, height 표현을 독립적으로
대조하고 \(x\) 또는 \(\log^3x\)가 빠지면 실패하게 한다.

## 5. 이번 결과가 해결하지 않은 것

1. Theorem 3.4의 복잡한 \(R^*\) 전 항에 대한 growing-\(A\) supremum.
2. zero-density 부분 식 (28)--(32)까지 포함한 완전한 \(C_A\).
3. \(P_T=\#\{p:T\le p<2T\}\)의 explicit lower bound.
4. H1c-1b.2 12항과 H1c-1b.3 prime-power·endpoint 비용의 full absorption.
5. Hypothesis 1(2), P9.2, SIV-08와 \(X_{\mathrm{cert}}\).

## 6. 계산자원과 사용자 도움

이번 gate에는 원문 PDF·저자 source와 표준 `mpmath`만 사용했다. Lean, 추가 Python package,
actual prime 계산, 장시간 연산 또는 사용자 PC 실행은 필요하지 않았다.

사용자 수행절차는 **별도 수행절차 필요없음**이다.

## 7. 권장 다음 순서

1. **H1c-1b.4b explicit density와 \(c_0,c_1\)** — 약 2--4시간. source \(C_A\)와
   독립이므로 먼저 완전히 닫을 수 있다.
2. **H1c-1b.4c C-budget·non-C absorption** — 약 1일. 모든 나머지항을 넣고
   numerical \(C_A\)가 만족해야 할 정확한 상한을 역산한다.
3. **H1c-1b.4d growing-A source reproof** — 수일 이상. Theorem 3.4 전 항을 다시
   상계해 2번 budget을 만족하는지 판정한다.
4. 성공한 뒤에만 H1(2)/P9.2 end-to-end 승격을 검토한다.

## 8. 최종 판정

```text
source variable types             = CORRECTABLE AND CLOSED
printed final first term          = NOT NUMERICALLY USABLE
arXiv v1 substituted              = NO
direct target algebra             = VERIFIED
actual growing-A numerical C_A    = OPEN
Theorem 1.4 12-term parameterization = RETAINED
H1(2) / P9.2 / SIV-08 / X_cert   = OPEN
```
