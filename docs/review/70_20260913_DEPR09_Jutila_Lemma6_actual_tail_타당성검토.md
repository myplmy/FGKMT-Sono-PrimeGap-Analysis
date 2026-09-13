# DEP-R09 Jutila Lemma 6 actual tail 타당성검토

- 작성일: 2026-09-13 KST
- 검토 질문: Jutila가 숫자를 쓰지 않은 절단 꼬리를 실제 적용에서는 계산 가능한 값으로 바꿀 수 있는가
- 상세 수학 정본: [Theory 63](../method/theory/63_Sono_FMT_DEPR09_Jutila_Lemma6_truncation_tail_actual.md)
- 판정: **타당 — 실제 Jutila parameter에 한해 명시화; 일반 Lemma와 JL6 전체는 미완**

> **후속 상태(2026-09-13):** [review 71](71_20260913_DEPR09_Jutila_Lemma6_actual_common_budget_타당성검토.md)이
> `exp(-1/X)` 감쇠를 포함한 네 loss와 공통 cutoff를 합쳐 `JL6-ACTUAL`을
> parameterized explicit로 닫았다. 아래 common-budget 미완 설명은 작성 당시 snapshot이다.
> printed general JL6, JL8와 root certificate는 계속 OPEN이다.

## 1. 사용자가 알아야 할 결과

Jutila 증명은 무한히 이어지는 합을 어느 지점에서 자르고, 뒤에 남은 꼬리를 단순히
“충분히 작다”고 적었다. 실제 후속 증명에서 사용하는 parameter를 넣으면 그 꼬리는

\[
 |E_{\rm tail}|\le
 4\exp\{-L^2+(1+13\varepsilon)L\},\qquad L=\log(qT)
\]

이하임을 직접 증명할 수 있다. 목표 오차를 \(\eta\)라 할 때

\[
 L\ge\max\left\{2(1+13\varepsilon),\sqrt{2\log(4/\eta)}\right\}
\]

이면 꼬리가 \(\eta\) 이하라고 보장된다.

예를 들어 **이 꼬리 하나만** 보고 \(\varepsilon=0.01\), \(\eta=0.01\)을 넣으면
충분조건은 `log(qT)>=3.46164`, 즉 대략 `qT>=31.87`이다. 이는 전체 정리의 시작점이
32라는 뜻이 아니다. JL5, Mellin, JL8, PAP와 다른 훨씬 큰 cutoff를 아직 합치지 않았기
때문이다. 이 예시는 actual tail 자체가 최종 (X_{\rm cert})를 지배할 가능성이 낮다는
규모 진단일 뿐이다.

> 쉬운 비유: 긴 영수증의 뒤쪽을 잘라 버려도 되는지 확인하는 문제다. 실제 영수증 양식은
> 뒤로 갈수록 항목 금액이 아주 빠르게 줄어든다. 이번에는 “몇 줄 이후의 합계가 1원보다
> 작다” 같은 cutoff 공식을 만들었다.

## 2. 무엇이 해결됐고 무엇이 안 됐는가

| 항목 | 판정 | 쉬운 뜻 |
|---|---|---|
| 실제 Sono/Jutila 적용의 tail | 해결 | parameter를 넣으면 최대 오차와 충분 시작점을 계산 가능 |
| Jutila가 인쇄한 일반 Lemma의 모든 \(X\) | 미해결 | 원문은 \(X\)의 상한이 없어 이번 절대값 방식만으로 uniform 보장 불가 |
| JL5+Mellin+tail 전체 예산 | 미해결 | 세 비용을 한 허용 오차 안에 나누어 넣는 작업이 남음 |
| JL8 local zero count | 미해결 | 다음 큰 analytic multiplier 병목 |
| fixed \(2\times10^{-17}\), \(X_{\rm cert}\) | 미해결 | 아직 계산기를 만들 단계가 아님 |

중요한 점은 “실제 적용”과 “원 논문의 일반 명제”를 구분한 것이다. 실제 DEP-R09 경로에는
이번 결과를 사용할 수 있지만, 다른 parameter를 쓰는 응용에 그대로 복사하면 안 된다.

## 3. 계산이 빠지는 항이 없는지 확인

꼬리항에는 네 가지 요소가 있다.

1. Barban--Vehov 계수 \(a(n)\)
2. character \(\chi(n)\)
3. \(n^{-\rho}\)
4. pseudocharacter \(\psi_r(n)\)의 유한 \(r\)-합

각각을 절대값으로 제한해

\[
 |a(n)|\le2\sqrt n,\qquad |\chi(n)|\le1,
 \qquad n^{-\beta}\le n^{-1/2},\qquad
 \sum_{r\le R}'|\psi_r(n)|/r\le R
\]

을 썼다. 따라서 비지수 부분 전체가 \(2R\) 이하이다. 첫 생략 정수도
\(\lfloor x\rfloor+1\)로 처리했으므로 \(x\)가 정수가 아닐 때 생기는 경계 오류가 없다.

## 4. 비판적으로 확인한 한계

원문의 일반 Lemma는 \(X\)가 충분히 크다는 아래쪽 조건만 주고 위쪽 조건은 주지 않는다.
이번 상계는 대략 \(RXe^{-(\log(qT))^2}\)이므로 \(X\)를 무한히 키우는 일반 상황에는
uniform하지 않다. character cancellation을 이용하는 더 정교한 proof가 있을 수 있지만,
그것을 이번 결과에 몰래 포함시키지 않았다.

따라서 “Jutila Lemma 6의 오류를 발견했다”는 판정도 아니고, “일반 Lemma 6을 재증명했다”는
판정도 아니다. 정확한 판정은 **실제 parameter에 필요한 tail component를 닫았다**이다.

## 5. source-first 조사 결과

- Jutila PDF는 native text layer가 사실상 비어 OCR을 사용했고 인쇄 pp. 48, 50--52를
  원페이지와 대조했다.
- NIST DLMF의 incomplete-gamma 상계도 확인했지만, 이 discrete tail은 exact geometric
  series가 더 짧고 endpoint-safe하다.
- Graham 1981은 공식 metadata와 검색 가능한 명제상 다른 truncated-Perron detector를
  쓴다. 공식 PDF 다운로드는 JavaScript challenge로 실패했으므로 PDF를 읽었다고 하지
  않는다. 이번 직접 proof에는 필요하지 않다.
- 표적 검색에서 exact drop-in explicit multiplier를 찾지 못했지만, 이는 전 세계 문헌에
  그런 결과가 없다는 novelty 주장이 아니다.

## 6. 검증과 증명의 경계

- Python은 exact source hash, geometric endpoint, 작은 정수의 divisor bound, exponent와
  cutoff implication, fail-closed 상태를 검사한다.
- Lean은 \(X+1\le2X\), actual exponent 합, quadratic decay와 log-budget 합성만 검증한다.
- 무한급수와 character 이론을 project-local `axiom`으로 넣지 않는다.
- `sorry`, `admit`을 사용하지 않는다.
- Python의 100-dps 수치는 directed interval certificate가 아니다.
- 실제 prime 데이터·maximal-gap 계산·장시간 연산은 수행하지 않았다.

## 7. 연구 전체에 미치는 영향

proof chain은 다음처럼 진전했다.

```text
이전: JL5 닫힘 + JL6 Mellin 닫힘 + actual tail 열림 -> JL6 열림
현재: JL5 닫힘 + JL6 Mellin 닫힘 + actual tail 닫힘 -> common budget 열림 -> JL6 열림
```

즉 다음 작업이 더 선명해졌다. 새 문헌을 넓게 찾기보다 우선 세 오차를 하나의
\(D_0(\varepsilon)\)에 합치는 것이 효율적이다. 그 합성이 끝난 뒤 JL8 local zero-count
multiplier로 이동한다.

## 8. 다음 권장 작업

1. **JL6c common error budget** — 예상 2--5시간. JL5 relative loss, Mellin, tail을
   최종 detector 허용 오차에 배분하고 공통 cutoff를 만든다.
2. **JL8 source audit** — 예상 1--2일 이상. local zero-count의 \((1-\alpha)\) 구조를
   보존하는 explicit multiplier를 우선 찾는다.
3. **Branch S 종단 재합성** — JL8까지 숫자가 생긴 뒤 수행한다. 그 전에는
   threshold calculator나 장시간 prime sweep을 만들지 않는다.

현재 사용자 설치·다운로드·장시간 계산은 필요하지 않다.

## 9. 참고문헌

- M. Jutila, *On Linnik's constant*, DOI
  [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- NIST DLMF, [Incomplete Gamma Functions §8.10](https://dlmf.nist.gov/8.10).
- S. W. Graham, *On Linnik's constant*, DOI
  [10.4064/aa-39-2-163-179](https://doi.org/10.4064/aa-39-2-163-179).
