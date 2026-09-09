# H1c-1b.4b density·elementary constants 타당성 검토

- 검토일: 2026-09-09 KST
- 대상: Maynard half-open bridge와 FGKMT closed actual population의 명시적 density,
  Bordignon \(c_0,c_1\)
- 최종 판정:
  `VALID AND FINITE FOR ACTUAL IDENTITY APPLICATION / FULL RATE STILL OPEN`
- 정식화:
  [`docs/method/theory/39_Sono_FMT_H1c1b4b_density_constants.md`](../method/theory/39_Sono_FMT_H1c1b4b_density_constants.md)

## 1. 한눈에 보는 판정

| 질문 | 판정 | 이유 |
|---|---|---|
| density는 exact \(P_T\)와 같은 구간인가 | 예 | source 구간에서 endpoint 1을 명시적으로 보정 |
| PNT 근사로 center를 바꿨는가 | 아니오 | exact center 유지, lower bound는 분모에만 사용 |
| \(P_T>T/(2\log T)\)는 actual 범위 전체에 유효한가 | 예 | \(\log T\ge36^5\)와 elementary exponential bound |
| \(c_0<49\)는 floating-point 관측인가 | 아니오 | exact rational log/atan series enclosure |
| \(c_1<3\)는 prime product 계산인가 | 아니오 | 전체 정수합으로 확대 후 telescope |
| \(C_A\)도 해결됐는가 | 아니오 | 별도의 growing-parameter source reproof 필요 |
| H1(2), P9.2가 닫혔는가 | 아니오 | full absorption이 남음 |

## 2. density 선택의 타당성

Rosser--Schoenfeld 식 (3.8)은 \(\pi(2T)-\pi(T)\) 자체를 직접 낮춘다. Dusart의 두
pointwise bound를 빼는 방법도 가능하지만, 서로 다른 상·하계의 slack과 유효범위를 함께
관리해야 한다. 따라서 direct interval theorem을 정본으로 채택한 판단은 단순하고 안전하다.

다만 source와 Maynard의 endpoint convention은 같지 않다. 이 차이를 0으로 놓지 않고 최대
1을 뺀 뒤, actual 거대 범위에서 그 1을 \(T/(10\log T)\) 안에 흡수했다. 따라서
half-open mismatch를 숨기지 않았다.

## 3. exact center와 lower bound의 구분

H1c-1b.3은 각 residue count를 exact total \(P_T\)로 center했다. 이번 PNT lower bound는
그 center를 \(T/\log T\)로 바꾸지 않는다. 단지

\[
\frac{\text{absolute error}}{P_T}
<\frac{2\log T}{T}\,\text{absolute error}
\]

라고 비교하는 데만 쓴다. 이 구분이 없으면 추가 recentering error가 생기므로 중요한
정확성 조건이다.

## 4. \(c_0\) proof의 신뢰 범위

\(c_0\)의 \(\psi(113)\)를 직접 소수분해해 계산하는 대신, peer-reviewed global theorem
\(\psi(x)<1.03883x\)를 사용했다. 나머지 transcendental 비교는 유리수 급수의 명시적
remainder로 확인한다. 결과 upper 48.8774...와 49 사이에는 양의 exact rational margin이 있다.

이것은 Rosser--Schoenfeld Theorem 12의 진위를 재증명하는 것은 아니다. 해당 출판 정리를
source input으로 채택한 뒤, 그 정리에서 \(c_0<49\)로 가는 연결을 exact 검산한 것이다.

## 5. \(c_1\) proof의 신뢰 범위

prime만 합하던 양을 모든 정수 \(n\ge2\)로 넓히므로 상계 방향이 안전하다. 또한
\(1/[n(n-1)]=1/(n-1)-1/n\)라 정확히 telescope한다. prime 목록의 누락이나 truncation tail은
발생하지 않는다.

## 6. 아직 남은 blocker

이번 결과가 좋아도 H1c-1b.4 전체는 닫히지 않는다. 12항 중 네 번째 항에 들어가는
\(C_A\)가 미해결이고, 다른 11항과 prime-power·endpoint 비용을 목표 log saving 안에 동시에
넣는 common cutoff도 아직 증명하지 않았다.

따라서 다음 문장은 금지한다.

- “Bordignon Theorem 1.4가 actual Maynard rate를 만족한다.”
- “Hypothesis 1(2) 또는 Proposition 9.2가 증명됐다.”
- “\(X_{\mathrm{cert}}\)를 계산할 수 있다.”

## 7. 계산자원과 사용자 도움

이번 단계는 exact rational arithmetic과 기존 PDF만 사용했다. Lean, 새 Python package,
actual prime sweep, 장시간 계산 또는 사용자 PC 실행은 필요하지 않았다.

사용자 수행절차는 **별도 수행절차 필요없음**이다.

## 8. 권장 다음 순서

1. **H1c-1b.4c conditional full-absorption budget** — 약 1일. 미해결 \(C_A\)를 변수로
   남겨 허용 가능한 상한을 수치·수식으로 결정한다.
2. **H1c-1b.4d Theorem 3.4 growing-A reproof** — 수일 이상. source 세부항이 1번 budget을
   실제 만족하는지 증명한다.
3. 성공 후 **H1(2)/P9.2 end-to-end 재판정** — 약 1--2일.

## 9. 최종 판정

```text
source interval lower bound       = APPLICABLE
half-open endpoint correction     = RETAINED
P_T > T/(2 log T)                = CLOSED FOR ACTUAL RANGE
c0 < 49, c1 < 3                  = CLOSED
growing-A C_A                     = OPEN
full relative-rate absorption     = OPEN
H1(2) / P9.2 / SIV-08 / X_cert   = OPEN
```

> 후속 교정(2026-09-09): “actual exact half-open”이라는 표현은 철회한다. FGKMT의
> actual interval은 \([T,2T]\)이다. half-open 계산은 Maynard 일반형 bridge로서 정확하고,
> closed population은 더 크므로 이 문서의 density lower는 안전하게 보존된다.
