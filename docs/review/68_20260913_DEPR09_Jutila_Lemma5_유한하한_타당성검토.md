# DEP-R09 Jutila Lemma 5 유한 하한 타당성검토

- 작성일: 2026-09-13 KST
- 검토 대상: Jutila 1977 Lemma 5의 `1+o(1)`을 실제 숫자가 있는 유한 하한으로 교체할 수 있는가
- 상세 수학 정본:
  [Theory 61](../method/theory/61_Sono_FMT_DEPR09_Jutila_Lemma5_finite_harmonic_lower_bound.md)
- 판정: **타당 — JL5만 명시적으로 닫힘; JL6와 전체 PAP는 미완**

> **후속 상태(2026-09-13):** [Review 69](69_20260913_DEPR09_Jutila_Lemma6_Mellin_적분_타당성검토.md)에서
> JL6의 두 후속 오차 중 Mellin 항은 parameterized explicit로 진전했고,
> [review 70](70_20260913_DEPR09_Jutila_Lemma6_actual_tail_타당성검토.md)이 actual
> truncation tail도 닫았다. printed general tail, JL6 common budget·전체, JL8,
> PAP/root certificate는 계속 미완이다.

## 1. 한눈에 보는 결과

이번에는 새 증명을 처음부터 만들 필요가 없었다. 2022년 Colloquium Mathematicum에 출판된
Zuniga Alterman 논문이 Jutila가 쓴 것과 정확히 같은 합에 다음 정보를 이미 준다.

- 무엇을 더하는가: 제곱인수를 갖지 않는 수 \(r\)의 \(1/r\)
- 어떤 수를 빼는가: \(q\)와 공약수가 있는 \(r\)
- 어디까지 더하는가: \(r\le R\)
- 얼마나 틀릴 수 있는가: 최대 \(2.554\mathcal B_q/R^{1/3}\)
- 적용 범위: 모든 \(R>0\), 모든 양의 정수 \(q\)

따라서 “충분히 큰 \(R\)”을 숨은 말로 남기지 않고, 원하는 안전 여유 \(\eta\)와 \(q\)를
입력하면 충분한 시작점 \(R_0(q,\eta)\)를 계산할 수 있다.

> 일상적인 비유: 예전 설명서는 “엔진이 충분히 뜨거워지면 정상 출력이 나온다”고만 했다.
> 새 설명서는 온도계의 최대 오차까지 숫자로 알려 준다. 그래서 정상 출력이라고 말할 수 있는
> 안전 온도를 계산할 수 있다. 다만 엔진 다음에 연결된 두 부품의 오차는 아직 숫자가 없다.

## 2. 왜 이 선행정리가 정확히 맞는가

Jutila Lemma 5의 합은

\[
 \sum_{\substack{r\le R\\r\ {\rm squarefree}\\(r,q)=1}}\frac1r
\]

이다. squarefree 지시함수는 \(\mu^2(r)\)이므로 Zuniga Alterman Corollary 3.4(b)의
\(\sum\mu^2(r)/r\)와 동일하다. 서로소 조건과 오른쪽 endpoint도 같다. 주항 계수 역시

\[
 \frac6{\pi^2}\prod_{p\mid q}(1+1/p)^{-1}
\]

로 Jutila의 계수와 동일하다. 즉 비슷한 다른 평균을 억지로 바꾼 것이 아니라 직접
대입 가능한 정리다.

논문은 peer-reviewed journal에 출판되어 있고 DOI가 있다. 이 점은 출처 신뢰도를 높이지만,
우리 프로젝트에서는 문장·상수·조건을 원문 페이지와 별도로 대조했다. “동료심사됨”만으로
조건 일치를 생략하지 않았다.

## 3. 유한 하한은 어떻게 얻었는가

source theorem의 상수항 \(b_q\)는 양수다. 따라서 그 양의 이득은 사용하지 않고, 오차가
가장 나쁜 방향으로만 움직인다고 보수적으로 가정했다. 그러면

\[
 S_q(R)\ge c_q\log R-\frac{2.554\mathcal B_q}{R^{1/3}}.
\]

원하는 손실률을 \(0<\eta\le1\)로 정하면, 마지막 오차가
\(\eta c_q\log R\) 이하가 되는 충분조건을 잡을 수 있다. 프로젝트가 채택한 단순한 식은

\[
 R_0(q,\eta)=
 \max\left\{
 \exp\sqrt{\log q},\
 e,\
 \left(\frac{2.554\mathcal B_q}{\eta c_q}\right)^3
 \right\}.
\]

이다. 이 값보다 큰 모든 \(R\)에서는

\[
 S_q(R)\ge(1-\eta)c_q\log R
\]

가 보장된다. 이 cutoff는 작게 최적화한 값이 아니라, 증명과 프로그램에서 실수하기 어렵도록
고른 충분값이다.

## 4. 비판적으로 확인한 한계

### 4.1 JL6 전체를 닫지 않는다

Jutila Lemma 6은 JL5 주항 외에 두 오차를 더 쓴다.

1. Mellin 변환 적분을 제한하는 오차
2. 무한급수를 \(x=X\log^2(qT)\)에서 자르는 tail 오차

원문은 둘을 \(\ll_\varepsilon1\)로만 쓴다. 이번 \(R_0\)에는 그 상수들이 포함되지 않았다.
따라서 `JL5 EXPLICIT`을 `JL6 EXPLICIT` 또는 `PAP EXPLICIT`으로 확대하면 오류다.

### 4.2 \(\eta\)는 아직 최종 \(\varepsilon\)이 아니다

JL6의 최종 허용 손실을 세 오차가 나눠 써야 한다. 예를 들어 최종 손실이
\(\varepsilon\)이라고 해서 지금 바로 \(\eta=\varepsilon\)으로 고정할 수 없다.
두 남은 오차 상수가 나온 뒤 \(\eta\)와 나머지 예산을 함께 정해야 한다.

### 4.3 \(q\)-인수분해 provenance가 필요하다

\(c_q\)와 \(\mathcal B_q\)는 \(q\)의 서로 다른 소인수로 계산한다. evaluator는 제공된 소인수
목록이 \(q\)를 완전히 나누는지 검사하지만, 최종 certificate에서는 그 인수분해의 출처와
검증 방법도 보존해야 한다. 현재 코드는 threshold calculator가 아니라 상수 계약 검사기다.
또한 `mpmath` 80-dps 이상 평가값은 진단값이며 directed rounding을 쓰는 최종 구간산술
certificate가 아니다.

### 4.4 계산량을 늘려 해결할 종류의 문제가 아니다

이 단계는 큰 소수를 훑는 계산 문제가 아니었다. 이미 존재하는 analytic 오차항을 올바르게
찾고 조건을 대입하는 문제였다. 사용자 CPU를 수시간 더 써도 JL6의 숨은
\(\ll_\varepsilon\) 상수가 자동으로 나오지 않는다.

## 5. 대안 경로 검토

Theory 22의 corrected Wirsing theorem도 같은 곱셈함수로 특수화할 수 있다. 그러나 안전
매개변수 \(a=2/3\), \(A_2=130\)에서 multiplier가 대략 \(10^{176.819}\) 규모다.
논리적으로는 fallback이지만, 직접 source의 \(2.554\mathcal B_q R^{-1/3}\)보다 현저히
거칠다. 따라서 다음처럼 판정한다.

| 경로 | 타당성 | 채택 |
|---|---|---|
| Zuniga Alterman Cor. 3.4(b) | 정확한 합·조건, 수치오차, peer-reviewed | primary |
| corrected Wirsing 특수화 | 구조적으로 가능하지만 상수가 매우 큼 | 독립 fallback |
| Jutila 생성함수에서 직접 재증명 | 가능하지만 이미 더 좋은 source가 있음 | 불필요 |

또한 같은 논문의 Theorem 4.6은 \(R^{-1/2}\)형 더 강한 일반 경로를 제공할 수 있지만
\(q\)-곱이 더 복잡하다. 현재 충분한 Corollary 3.4(b)를 먼저 사용하고, 나중에 최종
\(X_{\rm cert}\) 예산에서 JL5 cutoff가 실제 지배항이 될 때만 최적화할 가치가 있다.

## 6. 검증 증거

- source PDF를 영구 보존하고 bytes·SHA-256을 machine ledger에 고정했다.
- native text 추출이 되는 PDF이므로 OCR을 쓰지 않았고, 수식이 있는 인쇄 pp. 10--12를
  원페이지 이미지와 대조했다.
- Jutila PDF는 native layer가 비어 있어 OCR한 뒤 인쇄 pp. 49--51과 대조했다.
- Python test는 source hash, 정확한 \(2.554=1277/500\), \(q\) 소인지지 완전성,
  \(c_q\)·\(\mathcal B_q\), cutoff error budget, root fail-closed 상태를 검사한다.
- Lean은 출판 analytic theorem을 가정으로 만들어 통과시키지 않고, 그 뒤의 유한 대수만
  커널에서 검사한다.

## 7. 연구 전체에 미치는 영향

이번 결과로 DEP-R09 Branch S의 blocker 하나가 줄었다.

```text
이전: JL4-ACTUAL 닫힘 -> JL5 열림 -> JL6 열림 -> JL8 열림
현재: JL4-ACTUAL 닫힘 -> JL5 닫힘 -> JL6 열림 -> JL8 열림
```

그러나 최종 결론은 여전히 다음과 같다.

- Sono가 인쇄한 fixed \(2\times10^{-17}\): 프로젝트 독립 인증 전
- “어느 \(X\)부터 부등식이 항상 성립하는가”라는 \(X_{\rm cert}\): OPEN
- threshold calculator: NOT READY
- actual prime sweep: 이번 작업에서 수행하지 않음

다음에는 JL6의 두 오차를 숫자로 만드는 것이 가장 가치가 높다. 그 두 값이 나와야 이번
\(R_0(q,\eta)\)와 함께 detector 전체 cutoff를 계산할 수 있다.

## 8. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- S. Zuniga Alterman, *Explicit averages of square-free supported functions:
  to the edge of the convolution method*, Colloq. Math. 168 (2022), 1--23,
  DOI [10.4064/cm8337-11-2020](https://doi.org/10.4064/cm8337-11-2020),
  arXiv [2003.05887](https://arxiv.org/abs/2003.05887).
- K. Ford, *Sieve Methods Lecture Notes* (2023), Theorem 4.4.

표적 문헌 검색에서 이 문제와 정확히 맞는 출처는 위 Zuniga Alterman 논문이었다.
이는 전 세계 문헌에 대한 완전한 novelty 조사라는 뜻은 아니다.
