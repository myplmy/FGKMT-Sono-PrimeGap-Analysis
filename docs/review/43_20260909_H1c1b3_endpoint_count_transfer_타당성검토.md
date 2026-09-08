# H1c-1b.3 endpoint·prime-count transfer 타당성 검토

- 검토일: 2026-09-09 KST
- 대상: H1c-1b.2의 cumulative \(\psi\) 상계를 actual Maynard Proposition 9.2
  identity-prime target으로 옮기는 bridge
- 최종 판정:
  `VALID_EXACT_QUANTITY_TRANSFER / NUMERICAL_RATE_AND_DENSITY_STILL_OPEN`
- 정식화:
  [`docs/method/theory/37_Sono_FMT_H1c1b3_endpoint_count_transfer.md`](../method/theory/37_Sono_FMT_H1c1b3_endpoint_count_transfer.md)

## 1. 한눈에 보는 판정

| 질문 | 판정 | 이유 |
|---|---|---|
| Maynard의 구간은 무엇인가 | \([T,2T)\) | Definition (2.1)의 half-open integer interval |
| target은 \(\psi\), \(\theta\), \(\pi\) 중 무엇인가 | unweighted \(\pi\) | P9.2가 prime indicator를 합함 |
| actual form에 affine 변환이 필요한가 | 아니오 | FGKMT 식 (6.5)의 selected form은 \(L(n)=n\) |
| 두 endpoint뿐 아니라 Abel 적분 안에서도 같은 \(B\)를 쓰는가 | 예 | fixed \(Q_1\), capacity 단조증가 |
| partial-summation 부호는 무엇인가 | plus | \(d(1/\log u)<0\)인 Abel summation 직접 유도 |
| prime powers를 무시했는가 | 아니오 | \(2\sqrt{2T}(M_B+\Phi_B)\)를 보존 |
| half-open endpoint를 무시했는가 | 아니오 | modulus당 최대 1, 합계 \(M_B\) 보존 |
| center가 Maynard exact total과 같은가 | 예 | \(P_T/\varphi(q)\)를 그대로 사용 |
| H1(2), P9.2가 이제 닫혔는가 | 아니오 | density lower bound와 full absorption이 남음 |
| \(X_{\mathrm{cert}}\) 계산 준비가 됐는가 | 아니오 | H1c-1b.4와 상위 moment 의무가 남음 |

## 2. 타당한 핵심

### 2.1 목표 quantity를 먼저 맞춘 순서

절대오차가 얼마나 작은지 계산하기 전에 비교 대상의 구간·가중치·중심을 맞추는 순서는
타당하다. \(\psi\) 상계를 곧바로 “소수 개수 상계”라고 부르면 prime powers와
\(\log p\) 가중치를 누락한다. 이번 bridge는 이 둘을 분리한다.

### 2.2 선행 proof를 활용하되 정리 전체를 오용하지 않음

[Akbary--Hambrook](https://doi.org/10.1090/S0025-5718-2014-02919-0)는 이미
\(\pi_1\), partial summation과 \(\pi_1-\pi<2\sqrt y\)를 사용한다. 이것은 필요한 lemma를
먼저 선행문헌에서 찾는 사용자 제안에 정확히 맞는다.

그러나 그 논문의 modulus 조건 \(\ell(q)>Q_1\)은 현재 \((q,B)=1\)과 같지 않다. 따라서
Corollary 1.4를 그대로 인용하지 않고 점별 count-transfer 부분만 가져와 fixed family에
다시 합성한 것은 필수적인 제한이다.

### 2.3 Abel 적분 구간의 quantifier

endpoint \(T\), \(2T\) 두 곳에서만 Bordignon bound를 아는 것으로는 적분항을 제어할 수
없다. 이번 증명은 모든 \(u\in[T,2T]\)에 같은 fixed \(Q_1,q_0,B\)와 q-family가 유효함을
확인했다. 이 단계가 없었다면 (37.2)는 증명되지 않았을 것이다.

### 2.4 정확한 recentering

Maynard의 중심은 예상 소수 개수나 PNT 근사가 아니라 실제
\(\#\mathcal P_{L,\mathcal A}(T)\)다. identity form에서는 이것이 정확히

\[
P_T=\#\{p:T\le p<2T\}
\]

다. project bridge도 처음부터 누적 total \(\psi(u)/\varphi(q)\), \(\pi_1\) total과
\(\pi\) total을 같이 옮겼으므로 추가 recentering error가 없다. 이것은 H1c-1b.4에서
PNT density를 **오차 중심 변경용이 아니라 denominator lower bound용**으로만 쓰게 해 준다.

## 3. partial-summation 부호 감사

Akbary--Hambrook p. 26의 보이는 display는 절댓값 안에서 적분 앞에 minus를 인쇄한다.
표준 Abel 공식

\[
\sum_{n\le y}a_nf(n)=A(y)f(y)-\int A(u)f'(u)\,du
\]

에 \(f(u)=1/\log u\)를 넣으면 \(f'(u)<0\)이므로 적분은 plus다. 작은 exact-step fixture에서
plus 식은 직접 계산한 \(\pi_1\)과 일치하고 minus 식은 일치하지 않았다.

이를 source 정리 전체의 치명적 오류라고 확대해서는 안 된다. 저자들은 바로 다음 줄에서
절댓값과 maximum을 취하므로 최종 upper bound는 어느 부호에서도 같다. 프로젝트는 정확한
항등식만 고쳐 사용하며, 공식 source의 별도 erratum을 찾지 못했다는 사실도 제한적으로만
기록한다.

## 4. endpoint 상계의 정확성

\((T,2T]\)와 \([T,2T)\)의 차는 \(T\)를 넣고 \(2T\)를 빼는 것이다. \(T>2\)에서는
두 점이 동시에 소수일 수 없으므로 centered correction은 한 atom이다. 한 reduced residue에
atom이 들어오면 \(1-1/\varphi(q)\), 들어오지 않으면 \(-1/\varphi(q)\) 형태이고 절댓값은
항상 1 이하다.

정수 \(T\)만 검사하면 \(2T\)가 홀수 소수인 경우를 놓친다. toy test에 반정수 \(T\)를 넣어
upper endpoint만 소수인 경우도 확인한 점이 적절하다.

## 5. prime-power 상계의 방향

\(E(y)=\pi_1(y)-\pi(y)\)는 prime powers \(p^k,k\ge2\)의 양의 합이므로 dyadic 증가량도
음이 아니다. 따라서 \(E(2T)-E(T)\le E(2T)<2\sqrt{2T}\)다. local count와 total center에
각각 적용해 modulus당

\[
2\sqrt{2T}\left(1+\frac1{\varphi(q)}\right)
\]

을 얻는 방향은 맞다. \(\Phi_B\le M_B\)를 쓴 \(4\sqrt2T^{5/6}\)은 느슨하지만 안전하다.

## 6. 아직 타당하지 않은 확대 해석

다음 주장은 현재 결과에서 나오지 않는다.

1. **Bordignon 12항이 목표 rate에 들어간다.** 아직 \(C_*\)와 common cutoff가 없다.
2. **PNT만 쓰면 H1(2)가 닫힌다.** explicit \(P_T\) lower bound와 절대오차의 비교가 필요하다.
3. **Akbary--Hambrook Corollary 1.4가 fixed-\(B\) 문제를 해결한다.** modulus family가 다르다.
4. **H1c-1b.3이 SIV-08 전체다.** 이것은 exact quantity normalization 한 층이다.
5. **이미 \(X_{\mathrm{cert}}\) 후보를 숫자로 계산할 수 있다.** H1c-1b.4와 P91/L93/P95,
   공통 moment budget이 남아 있다.

## 7. 기계검증의 의미와 한계

새 test는 다음 실제 실수를 막는다.

- Abel 적분 부호를 minus로 고정
- \(\psi\)에서 prime powers를 말없이 삭제
- \((T,2T]\)를 Maynard의 구간으로 오인
- 전체 중심을 \(T/\log T\)로 바꿈
- endpoint 비용을 modulus 합 밖에 한 번만 더함
- H1c-1b.3 closure를 H1(2), P9.2, SIV-08 closure로 과승격

반대로 toy enumeration은 Bordignon이나 Maynard의 정리를 재증명하지 않는다. \(R_B(u)\)의
수치 크기나 \(P_T\) density를 계산하지도 않는다.

## 8. 계산자원과 사용자 도움

이번 단계에는 기존 네 source PDF와 표준 Python·`mpmath`만 필요했다. 새 학술자료 다운로드,
Lean, 추가 package, 사용자 PC 장시간 계산 또는 actual prime sweep은 필요하지 않았다.

사용자 수행절차는 **별도 수행절차 필요없음**이다.

## 9. 권장 다음 순서

1. **H1c-1b.4 source normalization·density·full absorption** — 최소 1--3일. Bordignon의
   \(C(A,A-3,X_0/Y_0)\)를 해소하고 12항과 count-transfer 비용을 exact \(P_T\)에 대해
   한 cutoff로 흡수한다.
2. **P9.2/Hypothesis 1(2) end-to-end 재판정** — 1--2일 이상. 1번 성공 뒤에만 actual
   distribution input을 승격한다.
3. **P91/L93/P95와 common moment budget** — 수일 이상. Proposition 6.1 전체가 필요하다.
4. **모든 root gate 종료 뒤 threshold calculator 설계** — 현재 착수 금지.

## 10. 최종 판정

```text
Maynard exact interval/weight/center      = VERIFIED
uniform fixed family through Abel integral = VALID
partial summation sign                    = PLUS, VERIFIED
prime-power and endpoint costs            = RETAINED
exact half-open unweighted count transfer = CLOSED
full relative rate and density            = OPEN
Hypothesis 1(2) / Proposition 9.2         = OPEN
SIV-07 / SIV-08                           = HARD_BLOCKER
X_cert                                    = OPEN
```
