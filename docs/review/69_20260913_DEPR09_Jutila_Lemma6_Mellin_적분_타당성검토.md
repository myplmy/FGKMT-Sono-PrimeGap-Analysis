# DEP-R09 Jutila Lemma 6 Mellin 적분 타당성검토

- 작성일: 2026-09-13 KST
- 검토 질문: Jutila Lemma 6의 첫 번째 `<<_epsilon 1`을 실제 상수와 같은 원 조건으로 바꿀 수 있는가
- 상세 수학 정본: [Theory 62](../method/theory/62_Sono_FMT_DEPR09_Jutila_Lemma6_Mellin_integral_explicit.md)
- 판정: **타당 — Mellin 조각만 parameterized explicit; 절단 tail과 JL6 전체는 미완**

> **후속 상태(2026-09-13):** [Theory 63](../method/theory/63_Sono_FMT_DEPR09_Jutila_Lemma6_truncation_tail_actual.md)과
> [review 70](70_20260913_DEPR09_Jutila_Lemma6_actual_tail_타당성검토.md)이 actual parameter의
> tail component를 명시화했다. 이 문서의 “tail 미완”은 작성 당시 snapshot이며,
> [review 71](71_20260913_DEPR09_Jutila_Lemma6_actual_common_budget_타당성검토.md)이
> damping을 포함한 common budget을 합쳐 `JL6-ACTUAL`을 parameterized explicit로
> 닫았다. printed general JL6과 JL8 이후 의무는 여전히 미완이다.

## 1. 사용자가 알아야 할 결과

이번 단계에서 “적분 때문에 생기는 오차”는 숫자가 있는 식으로 제한했다.

\[
 |I|\le
 \frac{12\sqrt6}{\pi^{3/2}}
 \zeta(1+\delta)\left(\frac2\delta+1\right)
 \bigl((qT)^{1/2}Rz_2\bigr)^{-\varepsilon/2},
\]

\[
 \delta=\frac{\varepsilon}{4(1+\varepsilon)}.
\]

이 식은 Jutila가 이미 요구한 (2.8)을 만족할 때 성립한다. 즉 이 Mellin 조각 때문에
원래보다 강한 \(X\) 조건을 새로 부과하지 않았다.

하지만 Jutila는 그 다음 줄에서 무한합을 유한 범위로 자르며 또 하나의 숨은 오차를 쓴다.
그 tail은 이번 결과에 들어 있지 않다.

> 일상적인 비유: 배달 비용이 “기본 운송비 + 마지막 구간 비용”으로 나뉘어 있는데,
> 기본 운송비의 최대값은 계산했다. 마지막 구간 비용은 아직 영수증이 없으므로 전체 비용을
> 확정할 수 없다.

## 2. source-first 절차가 실제로 도움이 되었는가

도움이 되었다. Jutila가 인용한 Prachar 책의 해당 페이지는 공개 full text로 확보하지
못했지만, 다음 검증된 자료가 필요한 부분을 나눠 보장했다.

| 필요한 사실 | 사용한 자료 | 판정 |
|---|---|---|
| Mellin inversion·Gamma 공식 | NIST DLMF 공식 수식 | 적합 |
| strip 안의 Dirichlet \(L\)-함수 explicit upper bound | Bennett et al. 2021 Lemma 5.6 (5.3) | 적합 |
| 원 convexity source | Rademacher 1959 | metadata와 Bennett 전사로 확인; 원 full text 미열람 |
| 최근 Phragmen--Lindelof 오류 경고 | Fiori 2026 | 적용범위 확인용 |

따라서 이미 출판된 exact statement를 먼저 사용하고, source가 직접 주지 않는 actual
Barban--Vehov weight 합성과 imprimitive correction만 직접 증명했다. 이는 모든 complex
analysis를 처음부터 재작성하는 것보다 짧고, 조건 mismatch를 찾기도 쉽다.

## 3. 비판적으로 점검한 위험

### 3.1 contour 이동에서 pole을 지나치는가

선택한 선은 \(-1<-\beta+\delta<0\)에 있다. Gamma pole \(w=0\)은 지나지만 residue가
\(L(\rho,\chi)=0\)이라 사라진다. 다음 pole \(w=-1\)은 지나지 않는다. 따라서 숨은 residue
항을 누락하지 않는다.

### 3.2 primitive 지표 정리만 imprimitive 지표에 잘못 썼는가

그렇게 쓰지 않았다. conductor \(f\)로 내린 뒤 빠지는 Euler factor를 복원했고, 작은 소수
2와 3의 가장 나쁜 경우까지 포함해 \(4/\sqrt6\)의 보수 multiplier를 넣었다.

### 3.3 Jutila의 \(M\ll Rz_2\) 상수를 임의로 1이라 했는가

아니다. actual \(f=\mu\varphi\), \(|\lambda_d|\le1\), \(d\le z_2\)를 다시 넣어
\(M\)을 점별 상계했고, \(\sum n/\varphi(n)<3R\)을 통해 multiplier 3을 썼다.

### 3.4 Fiori 2026의 오류 지적이 이번 bound를 무효화하는가

확인한 범위에서는 아니다. Fiori의 특정 경고는 complex quantity
\(|\log(Q+s)|\)의 잘못된 단조성 처리다. Bennett 식 (5.3)은
\(|s+1|\)의 power를 사용한다. 두 표현은 다르다. 다만 이 판정은 Bennett 식 전체를
우리 프로젝트가 독립 재증명했다는 뜻이 아니라, Fiori가 지적한 **그 특정 오류**를 이번
대입이 사용하지 않는다는 뜻이다.

### 3.5 `parameterized explicit`이 곧 숫자 하나인가

아니다. \(q,T,R,z_2,\varepsilon\)을 넣으면 상수를 계산할 수 있다는 뜻이다. 아직 JL6
tail과 다른 downstream multiplier가 없어 최종 숫자 \(X_{\rm cert}\)는 계산할 수 없다.

## 4. 계산 검증과 증명의 경계

- Python은 source hash, 상수 합성, local prime factor, 작은 범위의
  \(\sum n/\varphi(n)<3R\), exponent transfer, fail-closed 상태를 검사한다.
- Lean은 \(\delta\) 범위와 exponent budget 같은 유한 실수대수만 커널에서 검사한다.
- Mellin inversion, contour 이동, Rademacher theorem은 project-local `axiom`으로 선언하지 않는다.
- 100-dps 수치는 directed interval certificate가 아니다.
- actual prime dataset이나 maximal-gap 계산은 실행하지 않았다.

## 5. 연구 전체에 미치는 영향

proof chain은 다음처럼 한 칸 진전했다.

```text
이전: JL5 닫힘 -> JL6 Mellin 열림 + tail 열림 -> JL6 열림 -> JL8 열림
현재: JL5 닫힘 -> JL6 Mellin 닫힘 + tail 열림 -> JL6 열림 -> JL8 열림
```

따라서 이번 결과는 중요한 blocker 하나를 없앴지만, 다음 주장을 허용하지 않는다.

- Sono fixed \(2\times10^{-17}\)의 프로젝트 독립 인증
- FGKMT/Sono 부등식이 항상 성립하기 시작하는 numerical \(X_{\rm cert}\)
- threshold calculator 제작
- 장시간 prime sweep 필요성

## 6. 다음 권장 작업

1. **JL6b tail source audit** — 예상 4--8시간의 문헌·수식 작업. 실제 장시간 CPU는 불필요하다.
2. **JL6 common error budget** — tail이 닫힌 뒤 2--4시간. JL5 loss, Mellin, tail을
   최종 \(\varepsilon\) 안에 배분한다.
3. **JL8 local zero-count multiplier** — JL6 뒤 1--2일 이상의 source audit 가능성이 있다.

현재 사용자에게 설치나 장시간 계산을 요청할 사항은 없다.

## 7. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. A. Bennett, G. Martin, K. O'Bryant, A. Rechnitzer,
  *Counting zeros of Dirichlet L-functions*, Math. Comp. 90 (2021), 1455--1482,
  DOI [10.1090/mcom/3599](https://doi.org/10.1090/mcom/3599),
  arXiv [2005.02989](https://arxiv.org/abs/2005.02989).
- H. Rademacher, *On the Phragmén--Lindelöf theorem and some applications*,
  Math. Z. 72 (1959), 192--204,
  DOI [10.1007/BF01162949](https://doi.org/10.1007/BF01162949).
- A. Fiori, *A note on the Phragmén--Lindelöf theorem*, J. Math. Anal. Appl.
  559 (2026), 130404, DOI
  [10.1016/j.jmaa.2026.130404](https://doi.org/10.1016/j.jmaa.2026.130404),
  arXiv [2502.13282](https://arxiv.org/abs/2502.13282).
- NIST DLMF §§2.5, 5.5, 5.9, 5.11.
