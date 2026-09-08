# H1c-1b.1a.1 `sigma*y` explicit cutoff 타당성 검토

- 검토일: 2026-09-09 KST
- 대상: FMT/FGKMT/Sono의 $\sigma y$ 정규화와 H1c-1b.1a의 $26/25$ gate
- 최종 판정:
  `VALID_PROJECT_FINITE_APPLICATION_LEMMA / SIV-03_EXPLICIT / X_CERT_OPEN`
- 정식화:
  [`docs/method/theory/35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md`](../method/theory/35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md)

## 1. 한눈에 보는 판정

| 질문 | 판정 | 이유 |
|---|---|---|
| 선행정리로 처리 가능한가 | 예 | Rosser--Schoenfeld 1962 Theorem 7이 필요한 양방향 prime-product bound를 수치 범위와 함께 준다 |
| FMT의 product endpoint와 맞는가 | 예 | $(\log x)^{20}<p\le z$가 정확히 $P(z)/P((\log x)^{20})$다 |
| 제외 prime $B_0$를 빠뜨렸는가 | 아니오 | 구간 안에서 빠진 경우 $B_0>a$를 이용해 factor 하나를 uniform하게 상계했다 |
| $26/25$ 목표를 만족하는가 | 예 | 더 강한 $1001000/998001\approx1.0030051$을 얻는다 |
| Sono 최종계수가 이 단계에서 보존되는가 | 예 | 직전 $39/40$ transfer와 결합해 원래 $16/15$ slack 안에 들어간다 |
| 전체 Sono 부등식의 시작점인가 | 아니오 | 분포정리·상위 sieve error·arbitrary-$X$ transfer가 남아 있다 |
| 새 prime 계산이 필요한가 | 아니오 | published theorem과 exact/rational scalar 검산만 쓴다 |

## 2. 무엇을 실제로 증명했는가

모든 실수

\[
x\ge2\exp(36^5)
\]

에서 FMT의 실제 정의를 그대로 쓰면

\[
\sigma y
<\frac{1001000}{998001}\,80cx\log_2x
<\frac{26}{25}\,80cx\log_2x
\]

가 성립한다. 첫 부등식은 Rosser--Schoenfeld의 명시식, FMT의 exact algebra, 그리고 몇 개의
초등 정수·유리수 부등식으로 나온다.

이 결과는 asymptotic $O(\log_2^{-10}x)$의 숨은 상수를 추측한 것이 아니다. 원문의
asymptotic 표기를 건너뛰고 더 일반적인 published explicit product theorem을 직접 적용했다.

## 3. 선행연구의 적합성 대조

### Rosser--Schoenfeld 1962 — 채택

[원 논문](https://doi.org/10.1215/ijm/1255631807)의 Theorem 7은 $P(t)$의 upper와
lower를 모두 준다. 이번 quotient에는 분자 $P(z)$ upper와 분모 $P(a)$ lower가 필요하므로
방향이 정확히 맞는다. lower의 $t\ge285$ 조건도 $a>e^{300}$으로 충족한다.

### Dusart 2010 — 보조 대조

[Theorem 6.12](https://arxiv.org/abs/1002.0442)의 더 작은 upper error도 같은 결론을 준다.
다만 이 문서는 arXiv preprint이므로, 원 출판 정리만으로 완결되는 주 증명에는 넣지 않았다.

### Axler 2018 — 재인용 확인용, Proposition 9 upper는 미채택

[출판 PDF](https://math.colgate.edu/~integers/s52/s52.pdf) p.19는 Rosser--Schoenfeld
Theorem 7을 재인용해 source identity를 확인하는 데 유용하다. 반면 그 PDF의 Proposition 9
위쪽 표시식은 적힌 그대로라면 점근 주항이 빠져 $P(t)\asymp1/\log t$와 맞지 않는다.
따라서 해당 표시식에 의존하지 않았다. 이 판단은 Axler 논문 전체를 부정하는 것이 아니라,
현재 필요한 한 줄의 안전한 채택 여부만 판단한 것이다.

## 4. 증명에서 놓치기 쉬운 부분

### 4.1 lower endpoint

FMT는 $a<p$라는 strict 조건을 쓴다. $P(a)$는 $p\le a$를 포함하므로 quotient
$P(z)/P(a)$가 strict endpoint를 정확히 구현한다. $p<a$ product로 바꾸면 $a$가 prime인
특수점에서 오류가 생긴다.

### 4.2 제외 prime

그냥 $\sigma=P(z)/P(a)$라고 쓰면 $B_0$가 구간 안에 있을 때 $\sigma$를 작게 잡는 방향의
오류가 된다. 이번 증명은 최악의 correction

\[
(1-1/a)^{-1}<1000/999
\]

를 반드시 곱했다.

### 4.3 iterated logarithm

$z=x^{\log_3x/(4\log_2x)}$의 아래첨자는 base가 아니라 자연로그 반복 횟수다. 이를 base-2,
base-3 로그로 바꾸면 $\log a/\log z$의 exact cancellation이 깨진다.

### 4.4 국소 exceptional-prime 처리와 전역 common-$B$는 다르다

이번에는 이미 주어진 하나의 $B_0$가 product에서 빠질 때의 factor만 처리했다. Bordignon
분포정리의 모든 modulus와 FGKMT construction에 걸쳐 **같은** $B$를 선택할 수 있는지는
별도 H1c-1b.2 의무다.

## 5. cutoff의 크기와 의미

$2\exp(36^5)$는 약 2,626만 자리 수다. 매우 크지만 계산 자원이 부족해서 그런 값이 나온
것은 아니다. 앞서 증명한 integral lemma의 보수적 $r\ge36$ gate를 그대로 물려받았기
때문이다.

중요한 해석은 다음과 같다.

- 이 숫자까지 소수를 전수검사한 것이 아니다.
- 2,626만 자리 수를 메모리에 정수로 만들 필요도 없다.
- `log(x)`만으로 몇 밀리초 수준의 보조검산이 가능하다.
- 이 하위 cutoff를 작게 최적화해도 다른 hard blocker가 남으므로 당장 전체 알고리즘이나
  $X_{\mathrm{cert}}$가 개선되지는 않는다.

## 6. 기존 원장에 미치는 영향

### 승격하는 항목

- `H1c-1b.1a.1`: `PROJECT_FINITE_LEMMA_CLOSED`
- `SIV-03`: `PARTIAL`에서 `EXPLICIT`
- 직전 H1c-1b.1a의 conditional finite coefficient transfer: 실제 cutoff를 얻음

### 승격하지 않는 항목

- `AN-02`: general $\varphi(P)/P$ application은 actual 방향·cutoff 감사를 따로 해야 함
- `UB-05`: reciprocal-square product와 UB 전체 합성을 따로 감사해야 함
- `SIV-07`, `SIV-08`: `HARD_BLOCKER`
- Hypothesis 1(2), Proposition 9.2, `FIN-05`, $X_{\mathrm{cert}}$: `OPEN`

같은 Rosser theorem을 재사용할 수 있다는 사실과 각 상위 application이 닫혔다는 사실을
혼동하지 않기 위해 보수적으로 분리했다.

## 7. 오류·오차 가능성에 대한 비판적 평가

| 위험 | 통제 | 남은 위험 |
|---|---|---|
| source 식 오기 | FMT·FGKMT·Sono 3개 원문을 대조 | 판본별 equation 번호 차이만 있음 |
| endpoint off-by-one | $P(z)/P(a)$를 명시 | 없음 |
| $B_0$ 누락 | 최악 correction을 포함 | global common-$B$는 별도 OPEN |
| floating-point 반올림 | 핵심 비교를 `Fraction`·정수 곱으로 검사 | 100-dps 값은 진단용일 뿐 |
| source theorem의 잘못된 재인용 | 원 Rosser--Schoenfeld PDF를 직접 채택 | theorem 자체의 독립 재증명은 하지 않음 |
| cutoff를 전체 threshold로 오독 | 모든 정본에 sublemma-only를 표시 | 상위 문서 동기화가 계속 필요 |

## 8. 계산자원·사용자 도움 필요 여부

이번 gate에는 새 package, Lean, PARI/GP, 장시간 CPU, 추가 RAM 또는 사용자 실행이 필요하지
않다. 기존 FGKMT Python의 `mpmath`, 표준 `fractions`와 unit test로 충분하다.

사용자가 지금 수행해야 할 절차는 **별도 수행절차 필요없음**이다. 실제 prime 실험을 새로
돌리는 것은 이 증명과 무관하며 권장하지 않는다.

## 9. 다음 권장 연구

다음은 `H1c-1b.2` full distribution composition이다. 순서는 다음이 안전하다.

1. Bordignon Theorem 1.4의 actual identity-form remainder를 source 변수로 다시 쓴다.
2. exceptional modulus가 FMT의 $B_0$ 선택과 하나로 통일되는지 증명한다.
3. dyadic interval의 $\psi\to\pi$, half-open endpoint, recentering을 explicit하게 합친다.
4. represented-prime density lower bound와 모든 error를 한 공통 cutoff에 묶는다.
5. 그 결과로 Hypothesis 1(2)와 Proposition 9.2를 승격할 수 있는지 판정한다.

예상 작업시간은 문헌·대수 감사 기준 4--8시간이며, source theorem에 숨은 uniformity가 더
발견되면 별도 하위 gate로 분리해야 한다. 아직 사용자 CPU actual 실험은 필요하지 않다.
