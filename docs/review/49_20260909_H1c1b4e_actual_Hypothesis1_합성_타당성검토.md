# H1c-1b.4e actual Hypothesis 1 합성 타당성 검토

- 작성: 2026-09-09 KST
- 판정:
  `ACTUAL IDENTITY DISTRIBUTION INPUT CLOSED AT A CONSERVATIVE CUTOFF`
- 비판적 한계:
  `WEIGHTED PROPOSITION 9.2, FGKMT ENDPOINT WEIGHT, SIV-08 ROOT, X_cert REMAIN OPEN`

## 1. 무엇이 새로 성립하는가

H1c-1b.4a--4d는 각각 source 표기, density, 허용 오차예산, source constant를 닫았지만 한
정리 호출로 합성하지 않았다. 이번에는 r1 endpoint 교정까지 포함해 같은

\[
T,\quad r=\lfloor(\log T)^{1/5}\rfloor,\quad A=100r^2+10,
\quad Q_1=(\log T)^A,\quad B
\]

를 사용한다는 것을 다시 확인했다. 그 결과 \(r\ge10^{10}\)에서 actual selected identity form에
필요한 Hypothesis 1 세 조건은 explicit constants 1, 1, 2로 성립한다.

이 cutoff는 작거나 실용적이라는 주장이 아니다. 상수 복원에서 soundness를 우선해 얻은 매우
보수적인 충분조건이다.

## 2. 선행정리와 직접 증명의 경계

- Bordignon final theorem과 그 하위 explicit-formula/zero-density 입력은 4a--4d에서
  판본·오류항을 개별 감사한 뒤 사용했다.
- Rosser--Schoenfeld의 interval prime lower bound를 density source로 사용했다.
- Maynard 원정의와 FGKMT 수정 정의를 다시 대조해 r1 endpoint를 적용했다.
- 선행정리에 따로 없는 연결부만 직접 증명했다: 연속 정수 residue 오차, (N\ge T/2),
  log-power 흡수, (B\le T^2), 그리고 닫힌 predecessor들의 quantifier composition이다.

따라서 “먼저 선행증명을 찾고 실제 적용성을 확인한 뒤 빠진 다리만 증명한다”는 작업방식은
이번 단계에서 타당했다. 다만 Bordignon의 인쇄식 오류 가능성과 FGKMT endpoint 수정처럼,
선행문헌이라는 이유만으로 식을 자동 채택하지 않았다.

## 3. 왜 P9.2 전체 PASS가 아닌가

Hypothesis 1은 Proposition 9.2에 들어가는 입력이다. Proposition 9.2는 그 입력과 sieve
coefficient를 이용해 가중합의 main term과 error를 만드는 별도 정리다. 현재 닫힌 것은 전자다.

더구나 FGKMT의 Theorem 6 합은 closed \([T,2T]\)인데 Section 8의 외부 소수 (p)는
\((T,2T]\)에 있다. \(T\)가 소수이면 closed 가중합에서 \(w(T)\) 하나를 제거해야 한다.
unweighted endpoint discrepancy가 1 이하라는 사실만으로 \(w(T)\)의 크기는 나오지 않는다.

따라서 다음 주장은 금지한다.

- “H1c-1b.4e가 Maynard Proposition 9.2를 증명했다.”
- “`SIV-08` 전체가 explicit해졌다.”
- “Sono 정리가 (X\ge2\exp(10^{50}))에서 성립한다.”

올바른 문장은 “actual identity-form P9.2에 필요한 Hypothesis input은 그 cutoff에서
explicit해졌다”이다.

## 4. 수치·논리 검증

검산 helper는 다음을 fail-closed로 확인한다.

1. \(L\)이 정확히 \(r^5\le L<(r+1)^5\) bin에 있는가.
2. 4c의 13개 non-source component와 source coefficient가 빠짐없이 들어갔는가.
3. 4d의 13개 source component upper가 그 coefficient에 합성됐는가.
4. 합친 normalized error의 log가 0보다 작은가.
5. 조건 (1), (3), (B\le T^2)에 쓰는 정수 다항식 부등식이 성립하는가.
6. endpoint r1이 weighted parent를 닫았다고 잘못 표시하지 않는가.

첫 dimension bin의 양 끝과 더 큰 (r)을 회귀점으로 사용한다. 부동소수점 값은 regression이며,
uniformity는 4c/4d의 exact rational·calculus witness와 이번 정수 witness가 담당한다.

## 5. 최종 상태

```text
actual identity Hypothesis 1 input = EXPLICIT at X >= 2*exp(10^50)
input constants                    = (1, 1, 2)
weighted Proposition 9.2           = RATE_MISSING
FGKMT weighted lower endpoint      = OPEN
broad SIV-08 root                  = HARD_BLOCKER
SIV-07 / SIV-09                    = HARD_BLOCKER
X_cert                             = OPEN
```

다음 연구는 더 큰 수까지 소수를 계산하는 작업이 아니라, Maynard Section 9의 weighted P9.2
오차를 현재 explicit input constants에 연결하는 증명 감사다.
