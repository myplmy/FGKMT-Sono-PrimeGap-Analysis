# DEP-R09 Jutila Lemma 4--8 정량복원 타당성검토

- 작성일: 2026-09-13 KST
- 상세 수식 정본: [Theory 60](../method/theory/60_Sono_FMT_DEPR09_Jutila_Lemma4_8_source_inventory.md)

> **후속 상태(2026-09-13):** 아래 `JL5 HARD_BLOCKER`는 이 검토 시점의 판정이다.
> [후속 검토 68](68_20260913_DEPR09_Jutila_Lemma5_유한하한_타당성검토.md)이
> peer-reviewed explicit source로 `JL5`를 닫았다. `JL6`과 `JL8`은 계속 열려 있다.
- 기계 원장: [Jutila Lemma 4--8 v1](../method/theory/data/Sono_FMT_DEPR09_Jutila_Lemma4_8_v1.json)
- 선행 검토: [Branch S 검토](66_20260913_DEPR09_branch_S_정량_transfer_타당성검토.md)
- 결론: `한 실제 제곱합 호출은 명시화 / 전체 zero-density·PAP는 미완성`

## 1. 이번에 실제로 해결한 것

Jutila 증명의 여러 부품 가운데 Lemma 4를 쓰는 **실제 한쪽 상계**에는 이제 숨은 상수 대신
숫자를 넣을 수 있다. Ramaré--Zuniga Alterman의 Corollary 1.3을 Jutila의 실제 매개변수
\(\tau=8/5\)에 대입하면 상수는 정확히

\[
 \frac{18884947}{500000}=37.769894
\]

다. 이 대입과 로그 비율의 유리 대수는 Lean으로 검증한다. 원 논문의 전체 점근식을
재증명한 것은 아니지만, Jutila 식 (3.6)이 요구하는 위쪽 경계에는 충분하다.

> 쉬운 설명: 부품 상자 하나에 “대략 이 정도”라고만 쓰여 있던 값을, 실제 숫자
> `37.769894`가 적힌 현대 부품으로 교체했다.

## 2. 아직 전체 결과가 나오지 않는 이유

다음 세 부품은 여전히 숫자가 없다.

| 병목 | 없는 정보 | 왜 중요한가 |
|---|---|---|
| `JL5` | \(1+o(1)\)의 균일한 속도와 시작점 | zero detector의 주항이 오차보다 크다는 것을 보장해야 함 |
| `JL6` | Mellin 적분과 절단 tail의 절대상수 | detector lower bound의 실제 손실을 결정함 |
| `JL8` | local zero-count의 \(\ll\) 상수 | 한 작은 상자에 들어가는 영점 수를 숫자로 제한해야 함 |

Huxley 1975 원문도 공식 경로에서 확보했다. 이는 과거의 “source leaf 미확보” 문제는
해결하지만, 원문 자체가 `sufficiently large`와 매개변수 의존 implied constant를 쓰므로
수치 multiplier와 공통 cutoff 문제는 남는다.

> 쉬운 설명: 설계도 원본은 찾았지만 설계도 안에도 “충분히 크게”, “어떤 상수만큼”이라는
> 표현이 있다. 컴퓨터에 넣으려면 이 말들을 실제 숫자로 바꿔야 한다.

## 3. 비판적 타당성 판정

- **타당한 진전:** 최신 explicit Barban--Vehov 상계를 실제 \(\tau=8/5\) 호출에 적용하는 것.
- **금지할 확대 해석:** 이 한 호출이 닫혔다는 이유로 Jutila Theorem 1-prime, PAP 또는
  Sono의 fixed \(2\times10^{-17}\)이 인증됐다고 쓰는 것.
- **주의할 finite 보정:** \(x_D=D^{11/2}\log^2D\) 때문에 인쇄된 \(e^{11\lambda}\) 외에
  \(\exp(4\lambda\log_2D/\log D)\)가 남는다. 이를 무시하고 `10 exp(11 lambda)`를 그대로
  가져오면 엄밀하지 않다.
- **현대 global zero count의 한계:** 전체 높이까지의 명시적 \(N(T,\chi)\)를 단순 차분하면
  `JL8`의 작은 창에 비례하는 \((1-\alpha)\) 이득이 사라질 수 있어 drop-in 대체가 아니다.

따라서 연구 방향은 계속 타당하지만, 현재 결과는 `부분 명시화`이며 전체 numerical theorem은
아니다.

## 4. 다음 권장 작업과 예상시간

| 순서 | 작업 | 권장 근거 | 예상 연구시간 |
|---:|---|---|---:|
| 1 | `JL5a` finite harmonic lower bound | 직접 정량화 가능성이 가장 높고 JL6의 선행조건 | 4--12시간 |
| 2 | `JL6a` Mellin·tail 절대상수 | detector가 실제로 양수인지 결정 | 1--3일 |
| 3 | `JL8a` local zero-count 원 source·대체정리 감사 | density multiplier의 남은 핵심 | 1--3일 |
| 4 | Jutila 종단 multiplier 합성 | 앞의 숫자가 있어야 의미가 있음 | 1--3일 |
| 5 | Branch S \(K e^{-160c}\) 예산 판정 | 그때 처음 fixed 계수의 통과 여부를 판단 가능 | 수시간 |

이 시간은 CPU를 계속 돌리는 시간이 아니라 문헌 확인과 증명 정량화 시간이다. 현재 사용자 PC에서
새 소수 탐색을 하거나 장시간 계산을 할 필요가 없다.

## 5. 현재 연구 상태

```text
Huxley official source leaf             = ACQUIRED AND HASHED
Jutila Lemma 4 actual upper call         = EXPLICIT SOURCE REPLACEMENT
Jutila Lemma 4 full asymptotic           = UNFORMALIZED SOURCE THEOREM
JL5 / JL6 / JL8                          = HARD_BLOCKER
PAP-11 / DEP-R09                         = OPEN
fixed 2e-17                              = NOT INDEPENDENTLY CERTIFIED
X_cert                                   = OPEN
threshold calculator                     = NOT READY
long computation justified now           = NO
```

## 6. 사용자 수행절차

별도 수행절차 필요 없음. 새 라이브러리나 장시간 CPU 작업도 현재는 필요하지 않다.

## 7. 참고문헌

- M. Jutila, [*On Linnik's constant*](https://doi.org/10.7146/math.scand.a-11701).
- M. N. Huxley, [*Large values of Dirichlet polynomials, III*](https://doi.org/10.4064/aa-26-4-435-444).
- M. N. Huxley and M. Jutila, [*Large values of Dirichlet polynomials, IV*](https://doi.org/10.4064/aa-32-3-297-312).
- O. Ramaré and S. Zuniga Alterman, [arXiv:2405.12662](https://arxiv.org/abs/2405.12662),
  DOI [10.7169/facm/241018-19-5](https://doi.org/10.7169/facm/241018-19-5).
- D. Berkane, [*An explicit estimate for the Barban and Vehov weights*](https://nntdm.net/papers/nntdm-20/NNTDM-20-2-35-43.pdf).
- S. Zuniga Alterman, [arXiv:2005.04280](https://arxiv.org/abs/2005.04280),
  DOI [10.4064/aa200712-22-6](https://doi.org/10.4064/aa200712-22-6).
- M. A. Bennett, G. Martin, K. O'Bryant and A. Rechnitzer,
  [arXiv:2005.02989](https://arxiv.org/abs/2005.02989).
