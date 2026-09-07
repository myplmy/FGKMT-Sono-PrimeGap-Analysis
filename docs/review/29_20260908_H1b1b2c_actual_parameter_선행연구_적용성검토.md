# H1b-1b-2c actual 입력 상수의 선행연구·적용성 검토

- 작성일: 2026-09-08
- 검토 질문: Maynard Section 8의 11개 실제 적용에 공통인 \(a,A_2,L\)을
  선행 정리에서 그대로 얻을 수 있는가, 아니면 어떤 연결부를 직접 증명해야 하는가?
- 상세 정식화:
  [23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md](../method/theory/23_Sono_FMT_H1b1b2c_actual_parameter_specialization.md)

## 1. 최종 판정

~~~text
문헌에 완성된 11-application 공통 package가 있는가?       TARGETED SEARCH에서 확인 못함
Maynard의 actual gamma 식은 복원됐는가?                    YES
모든 x>1의 explicit prime weighted sum이 있는가?           YES
교정된 kappa=1 summation theorem이 있는가?                 YES
문헌 부품 사이의 특수화·endpoint 연결이 자동인가?          NO
필요한 최소 연결 lemma를 직접 증명했는가?                  YES
공통 actual a,A2,L이 닫혔는가?                             YES, PARAMETERIZED
Lemma 8.4 전체와 X_cert가 닫혔는가?                        NO
~~~

가장 중요한 결론은 “논문을 찾았으니 끝”도 아니고 “모두 새로 증명해야 한다”도 아니다.
검증된 선행 부품은 재사용하되, 실제 입력과 정확히 맞는지 하나씩 확인하고 비어 있는
연결부만 직접 증명하는 사용자의 제안이 타당하다. 이번 gate에 그대로 적용했다.

## 2. source별 적용성

| source | 확인 위치 | 제공하는 것 | 그대로 쓰지 못하는 부분 | 판정 |
|---|---|---|---|---|
| Maynard, *Dense Clusters of Primes in Subsets*, DOI 10.1112/S0010437X16007296, arXiv:1405.2593 | Lemmas 8.3--8.4; source 531--604행 | 목표 prime-sum 가정과 actual \(\gamma(p)\) 구조 | 575--579행은 “fixed constants”, `O(k/p)`, `L << log log R`만 제시 | 실제 호출 source로 채택 |
| Rosser--Schoenfeld, *Approximate Formulas for Some Functions of Prime Numbers*, DOI 10.1215/ijm/1255631807 | printed p.70, Theorem 6, (3.21), (3.24) | 모든 실수 \(x>1\)의 \(\sum_{p\le x}\log p/p\) 상·하계 | Maynard의 양 끝 포함 구간과 제외소수는 직접 변환 필요 | 핵심 explicit input으로 채택 |
| Ford, *Sieve Methods Lecture Notes* | Theorem 4.4 | 누락항을 보존하는 corrected Wirsing 구조 | 일반 정리이므로 actual four-family 상수는 제공하지 않음 | theory 22 multiplier의 주 source |
| Castillo--Hall--Lemke Oliver--Pollack--Thompson, arXiv:1403.5808; DOI 10.1090/S0002-9939-2015-12554-3 | Lemma 2.5 직후 Remark와 proof | GGPY/Maynard 인쇄 오류항의 \(c_\gamma\) 문제 확인 | actual Maynard 상수 package는 제공하지 않음 | 교정 경로 선택에 필수 |
| Dusart, arXiv:1002.0442 | explicit estimates over primes | 더 날카로운 큰-\(x\) 추정 후보 | 별도 cutoff·작은 구간 처리가 필요하고 이번 보수적 목표에는 불필요 | 검토했으나 주 증명에는 미사용 |

## 3. 문헌 우선 방식의 비판적 평가

### 채택한 부분

1. 먼저 필요한 lemma의 정확한 가정과 결론을 고정한다.
2. DOI/arXiv·판본·쪽·식 번호까지 내려가 선행 결과를 찾는다.
3. 변수 정규화, endpoint, uniformity, finite range, 상수 의존성을 개별 검사한다.
4. 완전히 맞는 부분은 인용하고, 빈 연결부만 최소 범위로 직접 증명한다.

이 방식은 중복 증명을 줄이고, 오래된 정리의 검증된 계산을 재사용하며, 직접 증명해야 할
범위를 작게 만든다.

### 채택하지 않은 부분

- 정리 이름이나 결론이 비슷하다는 이유만으로 실제 적용에 대입하는 것
- 여러 `O(...)`를 근거 없이 숫자로 바꾸는 것
- 최신 논문이라는 이유만으로 더 오래된 전 범위 explicit 부등식을 교체하는 것
- 표적 검색에서 못 찾은 것을 전 세계 최초라는 주장으로 바꾸는 것
- 수치 실험으로 proof constant나 finite cutoff를 대신하는 것

## 4. 직접 보충이 필요했던 정확한 범위

선행 문헌 사이에서 비어 있던 것은 다음 네 연결부다.

1. 네 actual denominator family에서
   \(0\le p-(1+n+g(p))\le3k\)를 증명하는 유한 대수.
2. 이 식을 \(\rho_p<1/2\)와
   \(0\le\rho_p-1/p\le12k/p^2\)로 옮기는 단계.
3. Rosser--Schoenfeld 누적합을 Maynard의 \(w\le p\le z\) 합으로 옮길 때
   왼쪽 endpoint 한 항을 보정하는 단계.
4. application별 제외소수 합을 이미 인증된
   \(\log Q\le\Lambda_*\)와 결합하는 단계.

이 네 부분은 모두 실제 Section 8 family에만 한정해 증명했다. 따라서 추상적인
`g(p)=p+O(k)` 함수 전체에 대한 새 정리를 주장하지 않는다.

## 5. 얻은 공통 package와 의미

\[
a=\frac12,\qquad A_2=8,\qquad L=5+\log\Lambda_*.
\]

이는 11개 실제 적용에서 Lemma 8.3의 입력값이 더 이상 이름 없는 `fixed constant`가
아니라는 뜻이다. 교정된 one-step multiplier는 약
\(7.9173\times10^{121}\)이고, 오차에는 추가로
\(6+\log\Lambda_*\)가 곱해진다.

이 수치가 매우 크므로, 현재 목적은 “좋은 작은 threshold를 얻었다”가 아니라
“정확히 어느 단계가 threshold를 크게 만드는지 측정할 수 있게 됐다”이다. 향후에는
교정된 r-fold 합성을 먼저 닫고, 그 결과를 보고 어느 상계를 날카롭게 할 가치가 큰지
판단해야 한다.

## 6. 연구에 미치는 영향

- `H1B-L83`의 actual 입력 gate는 `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`으로 승격 가능하다.
- theory 20--21의 \(\Lambda_*\)와 \(c_\gamma\) 하한은 입력 관리와 독립 교차검사로 유지한다.
- `H1B-L84`의 r-fold composition, smooth norm, common finite range는 여전히 열려 있다.
- `SIV-07`, Proposition 6.1 전체, H1c/PAP, arbitrary-X 전달이 남아 있으므로
  \(X_{\rm cert}\)를 계산하거나 추정값을 theorem threshold라고 부르면 안 된다.

## 7. 다음 권장 연구

1. **H1b-1b-2d:** actual \(a,A_2,L\)과 smooth norm을 넣어 Lemma 8.4의
   corrected r-fold binomial error를 정식화한다.
2. 각 iteration의 서로 다른 \(L_j\le L_*\)을 공통 최악값으로 덮는 방식과
   application별 값을 유지하는 방식의 크기를 비교한다.
3. 합성 후 가장 큰 손실 항을 찾아, 그 항에 한해서 더 날카로운 선행 explicit bound를
   조사한다. 미리 모든 상수를 날카롭게 만드는 것은 작업량 대비 효율이 낮다.

## 8. 사용자 수행사항

별도 수행절차 필요없음. 이번 단계에는 Lean, 추가 Python 라이브러리, CPU-heavy 계산,
외부 maximal-gap 데이터가 필요하지 않았다.

