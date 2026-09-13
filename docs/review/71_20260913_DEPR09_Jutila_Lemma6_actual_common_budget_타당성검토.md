# DEP-R09 Jutila Lemma 6 actual 공통 오차예산 타당성검토

- 작성일: 2026-09-13 KST
- 대상: [Theory 64](../method/theory/64_Sono_FMT_DEPR09_Jutila_Lemma6_actual_common_budget.md)
- 판정: **actual p.52 적용은 parameterized explicit로 닫힘 / 일반 JL6·JL8·\(X_{\rm cert}\)은 열림**

## 1. 쉬운 결론

이번 단계는 타당하다. 앞에서 따로 계산한 세 오차를 더하는 것만으로는 부족했고,
원 식의 앞에 붙은 \(e^{-1/X}\)도 주항을 조금 줄인다는 점을 새로 예산에 넣었다.
네 비용을 모두 더해 원 논문이 허용한 \(\theta\)보다 작게 만들었기 때문에, Jutila가
실제 density proof에서 선택한 매개변수에 대해서는 Lemma 6의 원하는 하한을 숫자가 있는
충분조건으로 복원했다.

다만 이 결과는 자동차의 한 부품 검사를 끝낸 것과 같다. 다음 부품인 JL8의 local
zero-count 상수가 아직 없고, 그 뒤 PAP 전체 조립도 남았다. 그러므로 지금 계산한
\(\log D\) cutoff를 Sono 정리 전체의 시작점 \(X_{\rm cert}\)이라고 부르면 잘못이다.

## 2. 무엇을 확인했는가

### 2.1 원 식의 부호

Jutila 식 (2.11)을 유한합과 tail로 나누면

\[
 e^{-1/X}S_q(R)+g+E_{\rm tail}=I
\]

이므로

\[
 |g|\ge e^{-1/X}S_q(R)-|I|-|E_{\rm tail}|
\]

이다. 주항에서 두 절대오차를 빼는 방향이 맞다. OCR만 믿지 않고 인쇄 pp. 50--51
원페이지에서 등호와 절단 문장을 대조했다.

### 2.2 빠졌던 감쇠 비용

기존 다음-step 메모는 JL5, Mellin, tail의 세 예산을 예상했지만,
\(e^{-1/X}<1\)이므로 실제로는 다음 네 개가 필요하다.

1. JL5 source error \(\eta_5\)
2. exponential damping \(\eta_X\)
3. Mellin integral \(\eta_M\)
4. truncation tail \(\eta_T\)

이 발견은 기존 Theory 61--63의 개별 결과를 무효화하지 않는다. 그 결과를 최종 detector에
합치는 이번 단계에서만 새 항 하나가 필요했다.

### 2.3 원 논문의 power condition

actual choice에서 \(A=D^{1+9\theta}\), \(X=D^{1+12\theta}\)다.
proof branch의 \(\alpha\ge1-\theta\)를 넣으면 남는 exponent가
\(\theta(1-21\theta)\)이므로 \(0<\theta\le1/21\)에서 음수가 아니다.
따라서 이번 explicit cutoff가 Jutila 식 (2.8)을 몰래 약화하거나 바꾸지 않는다.

### 2.4 서로 다른 단위의 오차를 같은 단위로 변환

Mellin과 tail은 절대오차이고 JL5는 주항에 대한 상대오차다. 이를 무조건 더하면 단위가
맞지 않는다. Rosser--Schoenfeld Theorem 15와 작은 \(q\)의 exact check를 합쳐

\[
 1/C_\varphi\le\pi^2\log D
\]

를 얻고, 모든 오차를 \(C_\varphi\log R\)로 나눴다. 이 정규화 뒤에만 네 예산을
합산했으므로 dimensional mismatch가 없다.

## 3. 비판적으로 본 약점

### 3.1 cutoff가 매우 크다

\(\theta=1/100\), 네 budget을 \(\theta/4\)씩 배분하면

\[
 \log D\ge91\,726.754431106\ldots
\]

라는 보수적 충분조건이 나온다. 이 숫자는 actual prime 계산 범위를 뜻하지 않고
JL6 한 단계의 proof cutoff다. 주된 원인은

\[
 \mathcal B_q\le
 \exp\!\left(3(\log D/\log2)^{1/3}\right)
\]

라는 거친 worst-case 상계다. 실제 \(q\)의 소인수 구조를 사용하거나 명시적
prime-product 상계를 쓰면 크게 줄어들 가능성이 있다.

### 3.2 최소 cutoff가 아니다

각 sufficient inequality를 max로 묶었고, 네 budget도 균등배분이 최적이라는 증거가 없다.
따라서 이 결과는 존재와 계산 가능성을 닫지만 최적화 문제는 닫지 않는다. 다만 다음 JL8이
여전히 hard blocker이므로 지금 이 숫자만 미세 최적화하는 것은 우선순위가 낮다.

### 3.3 일반 Lemma 6은 열려 있다

actual proof에서는 \(X=D^{1+12\theta}\)라는 upper envelope가 있다. 인쇄된 일반 Lemma 6은
\(X\)의 아래쪽 조건만 주므로 Theory 63의 absolute tail proof를 그대로 uniform하게
적용할 수 없다. 이번 결과를 임의 \(R,X\)에 확대하면 안 된다.

### 3.4 Lean 증거의 범위

Lean은 exponent와 네 예산 합성 같은 유한 실수대수를 확인한다. Zuniga Alterman과
Rosser--Schoenfeld의 analytic theorem, Mellin contour와 무한급수 자체를 Lean에서 새로
증명하지 않았다. source theorem을 project-local axiom으로도 넣지 않았다.
따라서 상태는 source-backed analytic proof와 kernel-checked algebra의 결합이지,
전체 source theorem의 독립 형식증명은 아니다.

## 4. 판정표

| 질문 | 판정 | 이유 |
|---|---|---|
| 원문 부호와 endpoint가 맞는가 | 예 | pp. 50--51 원페이지 대조 |
| 네 loss를 모두 포함했는가 | 예 | 새 \(\eta_X\) 포함 |
| 원 power condition이 유지되는가 | 예, actual branch | \(\theta(1-21\theta)\ge0\) |
| absolute/relative 단위가 맞는가 | 예 | \(C_\varphi\log R\)로 통일 |
| cutoff가 계산 가능한가 | 예 | Theory 64 식 (64.20) |
| cutoff가 최적인가 | 아니오 | \(\mathcal B_q\) worst-case 상계가 매우 거침 |
| printed general JL6도 닫혔는가 | 아니오 | uniform tail/cancellation 미증명 |
| JL8·PAP-11이 닫혔는가 | 아니오 | 다음 source-first 의무 |
| fixed \(2\times10^{-17}\)이 인증됐는가 | 아니오 | DEP-R09 종단 미완 |
| numerical \(X_{\rm cert}\) 계산이 가능한가 | 아직 아니오 | JL8 및 downstream 공통 cutoff 필요 |

## 5. 연구적으로 무엇을 얻었는가

첫째, JL6 actual branch에는 더 이상 이름 없는 공통 오차가 남지 않는다. 네 항과 cutoff가
모두 드러났으므로 이후 proof DAG에서 이 node를 숫자가 있는 함수로 호출할 수 있다.

둘째, cutoff 크기의 병목이 어디인지 알게 됐다. 현재 JL6 안에서는 Mellin이나 exponential
tail보다 \(\mathcal B_q\)의 uniformization이 훨씬 크다. 나중에 전체 \(X_{\rm cert}\)
식이 완성되고 JL6가 실제 최대 병목으로 판정될 때만 이 부분을 최적화하면 된다.

셋째, 다음 작업이 명확해졌다. JL8의

\[
 N_{\rm local}\ll(1-\alpha)\log(q(T+1))+1
\]

형태에서 숨은 multiplier와 finite range를 source-first로 복원해야 한다. 이 상수가 없으면
JL6의 개선값을 PAP 계수로 전달할 수 없다.

## 6. 사용자 계산자원 필요 여부

현재는 별도 계산이 필요 없다. symbolic cutoff와 짧은 고정밀 진단, unit test, Lean
유한대수 검증으로 충분하다. prime sweep이나 수시간 CPU 작업은 JL8과 downstream
multiplier가 닫혀 전체 후보 \(X_{\rm cert}\)의 크기를 먼저 본 뒤 판단하는 편이 합리적이다.

**사용자 수행절차: 별도 수행절차 필요 없음.**

## 7. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- S. Zuniga Alterman, *Explicit averages of square-free supported functions:
  to the edge of the convolution method*, Colloq. Math. 168 (2022), 1--23,
  DOI [10.4064/cm8337-11-2020](https://doi.org/10.4064/cm8337-11-2020).
- J. B. Rosser and L. Schoenfeld,
  *Approximate formulas for some functions of prime numbers*,
  Illinois J. Math. 6 (1962), 64--94,
  DOI [10.1215/ijm/1255631807](https://doi.org/10.1215/ijm/1255631807).
