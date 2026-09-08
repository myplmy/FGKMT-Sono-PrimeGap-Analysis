# H1b-2a Lemmas 8.5--8.6·Proposition 9.4 타당성검토

- 검토일: 2026-09-08
- 대상: Sono/FMT numerical-threshold의 Maynard Proposition 6.1 잔여 moment/error 축
- 판정:
  `TWO_PARENT_COMPONENTS_ADVANCED_PROPOSITION94_AND_GLOBAL_THRESHOLD_OPEN`
- 이론 정본:
  [`28_Sono_FMT_H1b2a_residual_moment_error_package.md`](../method/theory/28_Sono_FMT_H1b2a_residual_moment_error_package.md)

## 1. 사용자 관점의 짧은 설명

이번 작업은 “Sono 부등식이 몇부터 성립하는가”라는 최종 숫자를 계산한 것이 아니다.
그 숫자를 계산하려면 증명 안의 모든 `충분히 크면`, `대략`, `상수배`를 실제 숫자로 바꿔야
한다. 이번에는 그 가운데 다음 두 묶음을 숫자식으로 바꿨다.

1. Maynard가 만든 sieve weight 하나가 지나치게 커지지 않는다는 Lemma 8.5
2. 좋은 주항 (I_k,J_k)가 0에 너무 가까워지지 않는다는 Lemma 8.6

세 번째 묶음인 Proposition 9.4는 일부 작은 부품만 닫혔다. 분포 오차와 마지막 Euler 곱이
남아 있으므로 전체 엔진은 아직 가동할 수 없다.

## 2. 원문을 그대로 수치화할 수 있었는가

그렇지 않다. Maynard 2016 Lemma 8.5는 `\ll`, `o(1)`을 쓰고, Lemma 8.6은
concentration argument 뒤의 multiplier를 인쇄하지 않는다. Proposition 9.4도
`negligible`, `O(1)`, `p+O(k)`를 남긴다. Maynard 2015 Section 7은 concentration 구조를
제공하지만 이번 actual cutoff에 바로 대입할 완성 숫자표는 아니다.

공식 출판본과 arXiv/author source를 대상으로 한 표적 검색에서도 같은 정규화의 완성된
explicit 대체 정리를 찾지 못했다. 따라서 “문헌에 없다”라고 단정하지 않고, 확인한 원문은
그대로 인용하되 project가 새로 채우는 연결식은 별도 lemma로 표시한 접근이 타당하다.

## 3. 새 (I_k(F)) 하한은 타당한가

타당하다. 핵심은 전체 복잡한 영역을 적분하는 대신 cutoff가 정확히 1인
([0,0.9/k]^k)만 적분하는 것이다. 비음수 함수의 전체 적분은 부분영역 적분보다 작을 수
없다. 이 영역에서는 결합 cutoff와 좌표 cutoff가 모두 1이므로 적분이 정확한 1차원 적분의
(k)제곱으로 분리된다.

이 논증은 확률적 concentration, 수치 fitting 또는 숨은 상수에 의존하지 않는다.
원문의 하한 scale

\[
(2k\log k)^{-k}
\]

를 multiplier 1로 얻는다. 상위 원장의 기존 `-k-1` 표기는 원문 전사 오류였고 이번에
`-k`로 교정해야 한다.

## 4. (F_1,F_2) 비교 상수가 너무 큰 문제

(2^k,C_J(k))는 날카롭지 않다. 그러나 다음 이유로 첫 finite certificate에는 적합하다.

- 유한하고 모든 입력이 보인다.
- 원문에 없는 `O(1)`을 1이라고 가정하지 않는다.
- 큰 상수가 최종 cutoff를 얼마나 악화시키는지 나중에 정량적으로 확인할 수 있다.
- soundness를 유지한 채 Maynard 2015 concentration을 재수치화해 교체할 수 있다.

단점은 최종 (X_{\rm cert})가 비현실적으로 커질 수 있다는 점이다. 따라서 이 상수를
“최선” 또는 “원문의 실제 implied constant”라고 부르면 안 된다. 현재 판정은
`SAFE_COARSE_FINITE_SUBSTITUTE`다.

## 5. Lemma 8.5의 finite replacement는 무엇을 보장하는가

이전 작업이 실제 `L620_dW` Lemma 8.4 호출의 product error를 명시했기 때문에
(M_{620}=1+\varepsilon_{620})을 그대로 계수 상계에 넣을 수 있다. local divisor bound는
각 squarefree prime의 포함/미포함 두 선택을 세면 되고, global bound는

\[
\#\{d_1\cdots d_k<R\}\le R(1+\log R)^k
\]

라는 elementary 상계로 닫힌다.

따라서 원문의 (R^{2+o(1)})에서 `o(1)=0`으로 놓지 않고, 실제
(eta_{85}(k,R))를 갖는 (R^{2+\eta_{85}})로 바꾼 것이 타당하다. 이 식은 매우
보수적이지만 오류항 흡수 계산에 넣을 수 있다.

## 6. Proposition 9.4에서 실제로 닫힌 것

| 부분 | 판정 | 이유 |
|---|---|---|
| (9.56)--(9.57) (ab) 제곱 대수 | 닫힘 | (2|ab|\le a^2+b^2), 대칭 후 multiplier 1 |
| (9.57) exact denominator | 닫힘 | (p>2k^2,\omega^*\le k+1)에서 (\le2/p) |
| (9.63) 첫 Euler 곱 | 닫힘 | (\sum_{p>2k^2}4k/p^2\le2/k), 따라서 (\le e^{2/k}) |
| (9.52) distribution error | 열림 | Hypothesis 1(1),(3)의 숫자 multiplier·cutoff 없음 |
| (9.67) 마지막 두 Euler 곱 | 열림 | `O(k)` 이전의 exact local factor를 복원해야 함 |
| (9.70) residue factor | 새 blocker 아님 | exact factor들이 1 이하 |

첫 Euler 곱 (e^{2/k})는 이후 (y^2)에서 (e^{4/k})로 제곱돼야 한다. 이 제곱을
빠뜨리면 과소평가다. 기계 계약이 두 값을 별도로 저장한다.

## 7. 위험한 과대해석

다음 결론은 현재 증거로 말할 수 없다.

- Proposition 9.4 전체가 explicit하게 증명됐다.
- Maynard Proposition 6.1의 네 moment가 하나의 finite cutoff에서 동시에 성립한다.
- `SIV-07` 또는 `SIV-09`가 닫혔다.
- Sono/FGKMT 부등식의 numerical (X_{\rm cert})를 계산할 준비가 끝났다.
- 현재 얻은 큰 multiplier가 최적이거나 실제 최소 threshold를 반영한다.

반대로 이번 결과가 단지 “형식적 정리”에 그치는 것도 아니다. Lemma 8.5와 8.6의 parent
행 두 개에서 숨은 상수를 제거했으므로, 이후 Proposition 9.1--9.5의 오차를 주항과 실제로
비교할 수 있는 입력이 생겼다.

## 8. 다음 작업의 타당한 분기

### 1순위: H1b-2a.1 Proposition 9.4 exact Euler normalization

식 (9.57)의 exact local denominator에서 출발해 식 (9.67)의 두 `O(k)`를 쓰기 전 인자를
복원한다. 복원된 인자를 singular series와 소수별로 나눠 비교하고 finite tail product를
만든다. 예상 6--12시간의 수학·source 감사다.

### 2순위: H1b-2a.2 Proposition 9.4 distribution error

Proposition 9.1과 “동일한 논증”이라고 생략된 식 (9.52)를 실제 tuple count와
(M_{620})로 다시 쓴다. 다만 Hypothesis 1(1),(3)의 multiplier를 입력 변수로 남길
수밖에 없으므로 H1c-1과 연결된다. 예상 6--15시간이다.

### 3순위: H1b-2b Propositions 9.1--9.5 공통 budget

위 두 항과 H1c-1이 닫힌 뒤에 수행한다. 현재 바로 착수하면 열린 상수를 기호만 바꿔
옮기게 되므로 순서를 늦추는 편이 타당하다.

## 9. 계산 자원·사용자 요청

이 단계는 대형 소수 탐색이 아니라 수학적 상수 감사다. 추가 RAM, 장시간 CPU, Lean,
새 Python 라이브러리는 필요하지 않았다. 사용자 수행절차는 별도 필요없다.
