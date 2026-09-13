# DEP-R09 Branch S 정량 transfer 타당성검토

- 작성일: 2026-09-13 KST
- 질문: Thorner--Zaman 또는 Jutila--Huxley 경로를 따라 fixed \(D=160\) PAP와
  Sono의 \(2\times10^{-17}\)을 실제 숫자로 복원할 수 있는가?
- 상세 수식 정본: [Theory 59](../method/theory/59_Sono_FMT_DEPR09_branch_S_quantitative_transfer_audit.md)
- 기계 판정: [Branch S transfer v1](../method/theory/data/Sono_FMT_DEPR09_branch_S_transfer_v1.json)
- 결론: `경로는 타당하지만 현재 공개된 문장만으로는 수치 인증 불가`

## 1. 사용자가 먼저 알아야 할 결론

이번 단계에서 “증명의 길이”는 더 정확해졌지만 \(X_{\rm cert}\)의 숫자는 아직 나오지 않았다.
그 이유는 컴퓨터가 느려서가 아니라, 선행논문이 중간 오차를 실제 숫자로 인쇄하지 않았기 때문이다.

확인한 사실은 다음과 같다.

- Thorner--Zaman 정리는 \(q\le x^{1/160}\) 같은 범위를 다룰 수 있는 좋은 설계다.
- 그러나 핵심 상수는 “효과적으로 계산 가능”이라고만 되어 있고 실제 값이 없다.
- Jutila의 오래된 정리는 지수 면에서는 더 날카로운 단서를 주지만, 역시 여러 시작점과
  오차상수가 생략돼 있다.
- fixed \(D=160\)에서는 이 숨은 상수가 \(x\)를 크게 하는 것만으로 사라지지 않는다.

따라서 지금 수십 시간 동안 소수를 계산하는 것은 이 문제를 해결하지 못한다. 먼저 증명 안의
숨은 숫자를 복원해야 한다.

## 2. 왜 “충분히 큰 x”로 해결되지 않는가

필요한 modulus 경계는 \(q=x^{1/160}\)이다. 그러면

\[
 \frac{\log x}{\log q}=160
\]

이 정확히 고정된다. 중간 오차가 대략

\[
 K\exp\!\left(-c\frac{\log x}{\log q}\right)
\]

라면 결과는 \(K e^{-160c}\)다. \(x\)가 백 자리에서 천 자리로 커져도 이 주요 상수는
그대로 남는다.

### 쉬운 예시

오차 허용량을 0.136이라고 하자.

- 숨은 배수 \(K=1\)이면 \(c\)가 약 0.01246 이상이어야 한다.
- \(K=10\)이면 약 0.02685 이상이어야 한다.
- \(K=1000\)이면 약 0.05564 이상이어야 한다.

논문이 \(K\)와 \(c\)를 모두 숫자로 주지 않으면 통과인지 실패인지 판단할 수 없다.

## 3. Thorner--Zaman 원문에서 실제로 열린 부분

| 단계 | 원문이 주는 것 | 수치 인증에 부족한 것 |
|---|---|---|
| zero-density | exponent \(12/5\), exceptional 제거형 exponent \(37/5\) | multiplier와 최초 적용점 |
| exceptional zero | Jutila의 repulsion을 사용 | \(D_0(\varepsilon)\), 작은 \(\nu_\varepsilon\), 합성 multiplier |
| explicit formula | 표준 공식을 사용 | 원문 `O` 상수와 공통 cutoff |
| prime-power 제거 | Chebyshev bound | 실제 multiplier |
| zero 합 | dyadic 분할·partial summation | 분할 개수와 density 상수의 수치 합성 |
| 최종 decay | effectively computable \(c_1\) | 실제 \(c_1\), implied constant, 시작점 |

정리의 논리 구조가 틀렸다는 뜻은 아니다. “존재하고 계산 가능하다”와 “이미 계산된 숫자가
문서에 있다”는 서로 다른 증거 수준이라는 뜻이다.

## 4. Jutila 1977이 주는 가능성과 한계

Jutila Theorem 1은 near-one zero-density exponent를 \(2+\varepsilon\)까지 낮춘다. 이 값은
범위 설계에 매우 유리할 수 있다. Theorem 1-prime에는 \(10e^{11\lambda}\)라는 명시적 모양도
나온다.

하지만 다음이 남는다.

- `D sufficiently large`의 실제 \(D_0\)가 없다.
- proof의 Lemma 4는 당시 `to appear`인 Graham 자료를 사용한다.
- Lemma 5에는 \(1+o(1)\)이 있지만 수렴 속도가 없다.
- Theorem 2에는 epsilon-의존 \(O\)-항과 “lower order”가 남는다.
- 마지막 Linnik 분기는 “거친 추정으로 된다”고 한 뒤 세부를 생략한다.

따라서 Jutila를 버릴 이유는 없지만, 그대로 복사해 numerical certificate로 쓸 수도 없다.
올바른 역할은 `정량 재증명의 source skeleton`이다.

## 5. D를 바꾸는 선택의 장단점

\(D\)가 커지면 \(q\le x^{1/D}\)가 더 좁아져 중간 정리를 증명하기 쉬워질 수 있다. 그러나
Sono의 마지막 계수도 함께 나빠진다.

| 선택 | 장점 | 단점 |
|---|---|---|
| \(D=160\) | 기존 계수 목표와 가장 잘 맞고 총 오차 약 13.62% 허용 | 가장 넓은 modulus 범위를 증명해야 함 |
| \(D=170\) | modulus 범위가 조금 쉬워짐 | 허용 오차가 약 8.56%로 감소 |
| \(D=180\) | 더 좁은 범위 | 허용 오차 약 3.49%뿐 |
| \(D=186\) | 현재 식이 허용하는 마지막 근처 | 허용 오차 약 0.458%뿐 |
| \(D\ge187\) | proof 범위는 더 쉬울 수 있음 | \(C_{\rm PAP}=1\)이어도 fixed 계수 실패 |

권장안은 \(D=160\)을 주축으로 유지하는 것이다. \(D=170\) 이상의 보조 계산은 실제 source
상수가 나왔을 때 비교안으로만 사용한다.

## 6. 이번에 실제로 진전한 것

1. Thorner--Zaman proof의 숨은 상수 위치를 theorem 문장보다 아래 단계까지 분해했다.
2. Jutila 공식 PDF를 확보하고, text layer가 없는 것을 확인한 뒤에만 OCR을 사용했다.
3. fixed-D에서 필요한 \(c\)를 \(K\)별로 계산하는 판정식을 만들었다.
4. 그 판정식의 초등 부등식 부분은 Lean 커널 검증 대상으로 분리했다.
5. source theorem을 local axiom으로 넣지 않고 모든 root 상태를 OPEN으로 보존했다.

이번 진전은 “답을 얻음”이 아니라 “정확히 어떤 숫자가 없어서 답을 못 내는지 알게 됨”이다.
이는 불필요한 장시간 계산을 막고 다음 증명 작업을 좁힌다는 점에서 의미가 있다.

## 7. 다음에 무엇을 해야 하나

권장 순서는 다음과 같다.

1. Huxley 원문을 공식 경로로 확보해 Jutila와 결합된 density proof의 첫 source leaf를 확인한다.
2. Jutila Lemmas 4--8의 모든 \(O,\ll,o(1)\)을 목록화하고 숫자로 바꿀 수 있는 최신 explicit
   대체 정리를 찾는다.
3. 별도로 Thorner--Zaman Theorem 2.3의 explicit-formula-to-density 변환을 처음부터 수치화한다.
4. 실제 \(K,c,u_0\)가 나온 뒤에만 \(K e^{-160c}\)와 0.1361687 예산을 비교한다.
5. 통과하면 principal·exceptional·prime-power 오차를 합쳐 하나의 \(u_{\rm PAP}\)를 만든다.

Huxley 원문을 자동 다운로드하려 했지만 공식 사이트의 JavaScript proof-of-work가 차단했다.
비공식 mirror는 사용하지 않았다. 사용자가 일반 Windows 웹브라우저에서 공식 페이지의
`Pobierz zgodnie z CC-BY`를 눌러 PDF를 내려받아 `article/`에 저장해 주면 다음 source 감사를
더 안전하게 진행할 수 있다.

## 8. 계산자원과 예상시간

| 작업 | 예상시간 | 사용자 CPU/RAM 필요 |
|---|---:|---|
| Huxley 원문 theorem·proof mapping | 2–6시간 | 없음 |
| Jutila Lemmas 4–8 source inventory | 1–3일 | 없음 |
| T--Z transfer의 수치 재증명 | 수일–수주 가능 | 대부분 짧은 symbolic/high-precision 검산 |
| finite cutoff 최적화 | source package 완성 뒤 수시간–수일 | 그때 별도 runner 판단 |
| actual prime sweep | 현재 가치 없음 | 수행 금지 |

현재 필요한 것은 긴 CPU 작업보다 문헌·증명 상수 감사다. 추가 Python library나 Lean package도
현재는 필요 없다.

## 9. 엄밀한 최종 판정

```text
Branch S mathematical direction       = VALID
ready-made numerical theorem          = NOT FOUND
fixed-D transfer diagnostic           = READY
analytic K, c, common cutoff           = OPEN
PAP-11 / DEP-R09                      = HARD_BLOCKER / OPEN
fixed 2e-17                           = NOT INDEPENDENTLY CERTIFIED
X_cert                                = OPEN
long computation justified now        = NO
```

## 10. 참고문헌

- Thorner--Zaman, [arXiv:2108.10878](https://arxiv.org/abs/2108.10878),
  DOI [10.1007/s00209-023-03414-3](https://doi.org/10.1007/s00209-023-03414-3).
- Jutila, [*On Linnik's constant*](https://doi.org/10.7146/math.scand.a-11701).
- Huxley, [*Large values of Dirichlet polynomials III*](https://doi.org/10.4064/aa-26-4-435-444).
