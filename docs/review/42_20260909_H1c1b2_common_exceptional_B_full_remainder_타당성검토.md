# H1c-1b.2 common exceptional `B`·full remainder 타당성 검토

- 검토일: 2026-09-09 KST
- 대상: Bordignon 2021 Theorem 1.4를 FGKMT actual Proposition 9.2 identity-form 호출에
  연결하는 exceptional-object·dyadic-remainder bridge
- 최종 판정:
  `VALID_NARROW_PROJECT_BRIDGE / COUNT_TRANSFER_AND_NUMERICAL_ABSORPTION_OPEN`
- 정식화:
  [`docs/method/theory/36_Sono_FMT_H1c1b2_common_exceptional_B_full_remainder.md`](../method/theory/36_Sono_FMT_H1c1b2_common_exceptional_B_full_remainder.md)

## 1. 한눈에 보는 판정

| 질문 | 판정 | 이유 |
|---|---|---|
| 두 endpoint에 같은 exceptional object를 쓸 수 있는가 | 예 | 원문 \(q_0\)는 endpoint가 아니라 fixed \(Q_1\)에 대해 정의된다 |
| \(q_0\) 자체를 Maynard의 prime \(B\)라고 해도 되는가 | 아니오 | \(q_0\)는 composite일 수 있어 prime divisor 하나를 택해야 한다 |
| prime divisor 하나로 충분한가 | 예 | \((q,B)=1\Rightarrow q_0\nmid q\) |
| 두 endpoint의 modulus range가 충분한가 | 예 | H1c-1b.1의 \(r\ge36\) capacity가 \(T\), \(2T\) 모두를 덮는다 |
| 출판 RHS를 빠짐없이 구현했는가 | 예 | 최종판의 양의 항 12개를 별도 field로 등록했다 |
| 바로 Maynard prime-count estimate가 되는가 | 아니오 | 현재 결과는 \((T,2T]\)의 von Mangoldt-weighted \(\psi\) 오차다 |
| \(X_{\mathrm{cert}}\) 계산기를 만들 수 있는가 | 아니오 | 상수 표기, count transfer, density, 전체 흡수와 상위 error budget이 남았다 |

## 2. 타당한 핵심

### 2.1 quantifier

Bordignon 최종판은 fixed \(Q_1\)까지의 exceptional modulus \(q_0\)를 먼저 정한다. 따라서
동일 \(Q_1=(\log T)^A\)를 \(u=T\), \(2T\)에 쓰는 것은 하나의 \(q_0\)를 두 번 쓰는 것이다.
endpoint마다 새 \(Q_1=(\log u)^A\)를 고르면 이 결론이 자동으로 성립하지 않으므로, 구현과
계약은 lower-endpoint \(Q_1\)을 고정한다.

### 2.2 exceptional modulus에서 prime `B`로의 변환

Maynard/FGKMT actual construction은 \(B=1\) 또는 prime을 사용한다. 따라서 \(q_0\)를 그대로
\(B\)로 놓는 것은 잘못이다. \(q_0\)의 prime divisor 하나를 택하면 다음 초등 implication이
정확하다.

\[
B\mid q_0,\ (q,B)=1\quad\Longrightarrow\quad q_0\nmid q.
\]

이 방식은 Bordignon sum보다 더 많은 modulus를 버릴 수 있지만 상계 방향에는 안전하다.
actual selected form은 \(n\)이어서 leading coefficient 1과 \(B\)의 coprimality도 자동이다.

### 2.3 dyadic subtraction

최종판의 중심은 \(\psi(u)/\varphi(q)\)다. 따라서 \(2T\) 식에서 \(T\) 식을 빼면 전체
von Mangoldt interval mass \(\psi(2T)-\psi(T)\)가 정확히 중심에 남는다. 절댓값은
삼각부등식으로 두 cumulative RHS의 합으로 제어된다. 부등호 방향과 중심항 모두 맞다.

## 3. 원문 판본 차이에 대한 비판적 판정

공식 arXiv v1 source와 최종 NYJM판 사이에 다음 차이가 실제로 있다.

- v1 중심: \(u/\varphi(q)\)
- 최종 중심: \(\psi(u)/\varphi(q)\)
- \(C\)-항과 첫 \(E\)-항의 일부 log factor도 다름

따라서 v1 수식을 코드로 옮긴 뒤 출판본을 인용하는 것은 재현성 오류다. 이번에는 final PDF의
Theorem 1.4와 proof (34)--(37)를 정본으로 고정했다. 공식 페이지에서 별도 erratum을 찾지는
못했지만, 이 표적 확인을 “오류가 절대 없다”는 주장으로 확대하지 않는다.

## 4. 아직 타당하지 않은 확대 해석

다음 주장은 현재 증거로는 성립하지 않는다.

1. **모든 \(X\)에 같은 \(B\)가 존재한다.** 필요한 것은 각 \(X\)에서 하나의 허용 \(B(X)\)다.
2. **full Bordignon remainder가 이미 충분히 작다.** 12항을 전사했을 뿐 \(C_*\)와 cutoff를
   아직 상계하지 않았다.
3. **\(\psi\) bound가 곧 prime count bound다.** prime powers와 partial summation, endpoint
   atom을 처리해야 한다.
4. **Hypothesis 1(2)가 닫혔다.** exact Maynard center와 represented-prime density까지 맞춰야 한다.
5. **\(X_{\mathrm{cert}}=2\exp(36^5)\)이다.** 그 수는 앞선 \(\sigma y\) 하위 lemma의
   cutoff일 뿐이다.

## 5. source 상수 표기 blocker

Bordignon Theorem 1.2는 \(Y_0=\log\log X_0\)와
\(C(\alpha_1,\alpha_2,Y_0)\)를 정의한다. 반면 최종 Theorem 1.4와 proof (35)는
\(C(A,A-3,X_0)\)라고 인쇄한다. type-consistent한 의도는 \(Y_0\)일 가능성이 있지만, 이를
근거 없이 자동 교정하면 최종 cutoff가 잘못될 수 있다.

따라서 코드가 \(C_*\)를 외부의 유효한 상계로 받게 한 것은 타당하다. H1c-1b.4에서는 원식
(33)의 변수를 다시 추적하거나 저자 clarification을 구하고, 어떤 해석을 썼는지 별도 표시해야 한다.

## 6. 기계검증의 의미와 한계

검증 코드는 다음 오류를 잡는다.

- \(B\)가 \(q_0\)의 prime divisor가 아닌 경우
- 12개 항 누락
- \(Q_1\) 범위와 theorem domain 위반
- \(R(T)+R(2T)\)를 \(T\)로 나눌 때 \(2R(2T)/(2T)\) factor 누락
- count transfer가 열려 있는데 상위 flag를 참으로 만드는 과승격

반대로 unit test는 Bordignon 정리 자체를 재증명하지 않으며, 미확정 \(C_*\)를 만들어내지도
않는다. 이것은 source formula transcription과 project bridge의 회귀검사다.

## 7. 계산자원과 사용자 도움

이번 gate에는 추가 논문 다운로드, 새 Python library, Lean, PARI/GP, 장시간 계산 또는 실제
소수 탐색이 필요하지 않았다. 기존 PDF, 표준 Python과 `mpmath`로 충분하다.

사용자 수행절차는 **별도 수행절차 필요없음**이다.

## 8. 권장 다음 순서

1. **H1c-1b.3 endpoint/count transfer** — 4–8시간 예상. \(\psi\)에서 unweighted prime count로
   넘어갈 때 생기는 prime-power·endpoint·partial-summation 항을 먼저 완전히 적는다.
2. **H1c-1b.4 full numerical absorption** — 1–3일 이상 예상. \(C_*\) 표기와 12개 항,
   density lower bound를 하나의 common cutoff로 묶는다. source clarification이 필요하면 중단한다.
3. **P9.2/Hypothesis 1(2) end-to-end composition** — 1–2일 이상 예상. 앞의 두 gate가 닫힌
   경우에만 상위 상태를 재판정한다.
4. **다른 P91/L93/P95와 공통 moment budget** — 수일 이상. 이것까지 닫히기 전에는
   threshold calculator를 만들지 않는다.

## 9. 최종 판정

```text
common q0 for T and 2T                   = VALID WITH FIXED Q1
prime B filter for actual identity form = VALID
final published RHS                     = 12/12 TRANSCRIBED
raw (T,2T] von Mangoldt composition     = VALID
half-open unweighted prime count        = OPEN
full numerical absorption               = OPEN
Hypothesis 1(2) / Proposition 9.2       = OPEN
SIV-07 / SIV-08                         = HARD_BLOCKER
X_cert                                  = OPEN
```
