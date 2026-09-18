# Review 93 — DEP-R09 sparse divisor-conductor source 감사 타당성검토

- 검토대상: Theory 84, machine ledger v1, exact Python helper·tests, Lean terminal
- 판정:
  <code>ARITHMETIC_REDUCTION_VALID /
  GENERIC_SPARSE_CERTIFICATE_REJECTION_VALID /
  ANALYTIC_TARGET_REMAINS_OPEN</code>

## 1. 검토 결론

Theory 84의 핵심 판정은 타당하다.

1. character modulo \(q\)의 primitive conductor partition은 exact하다.
2. conductor level 수가 적어도 character 총수는 \(\varphi(q)\)로 보존된다.
3. generic sampled-frequency sparse large sieve가 보존하는 길이 \(Y\) 항만으로도
   Theory 82의 가장 유리한 gate보다 RHS가 크다.
4. 그러므로 **generic coefficient-agnostic sparse certificate**는 기각되지만,
   actual \(\Lambda\)-specific cancellation이나 same-law weighted correlation은
   기각되지 않는다.
5. 새 bounded \(X_{\rm cert}\) 범위는 생기지 않았다.

## 2. conductor 수식 독립 대조

Möbius inversion

\[
 \varphi^*(r)=\sum_{e\mid r}\mu(r/e)\varphi(e)
\]

을 divisor 전수열거로 계산하면 sample \(q=3,30,210,2310,30030,510510\) 모두에서

\[
 \sum_{r\mid q}\varphi^*(r)=\varphi(q)
\]

가 exact하게 복원된다. squarefree \(r\)의 local factor \(p-2\)도 각 divisor에서
일치한다. \(2\mid r\)인 level의 count가 0인 것과 전체 character가 사라지는 것은
다르다. Theory 84는 이 두 층을 올바르게 분리한다.

## 3. sparse large-sieve 판정 검토

Baier Theorem 2의 source 구조에는 \(N Z\)가 남는다. Theory 84는 Baier theorem을
현재 divisor set에 무리하게 적용하지 않고, 오히려 더 유리한 가상 certificate에서
modulus-density 항을 0까지 낮춘다.

한 retained frequency \(\alpha_0\)에 \(a_n=e(-n\alpha_0)\)를 고르면
sampled square는 \(N^2\), coefficient energy는 \(N\)이다. 따라서 모든 coefficient를
대상으로 하는 sampled-frequency inequality의 전체 coefficient는 \(N\)보다 작을 수 없다.

Theory 83의 독립 source lower와 gate upper는

\[
 YS_2(Y)>V_{\rm gate}
\]

를 준다. 따라서 “sparse cardinality만 개선한 upper certificate가 strict target을
증명하지 못한다”는 결론은 맞다. 여기서 실제 \(V\)의 하한을 주장하지 않은 것도 맞다.

## 4. 추가 PDF 대조

### 4.1 Montgomery--Vaughan 파일

- 320,668 bytes, SHA-256
  <code>e4d6a5fae3a41b9b50fe34355b0ea098e852bd84384bba7e1e83dbb083af0c9b</code>.
- PDF 16쪽, journal printed pp.199--214.
- 실제 제목은 “Mean Values of Multiplicative Functions.”
- printed p.202 Theorem 5와 pp.212--214 proof를 원문 이미지와 text에서 대조했다.
- Vaughan 2001 variance 논문은 아니다.

Theorem 5의 truncated signed Möbius sum은 implicit constant를 사용하며, absolute-square
character energy로의 전달 정리가 없다. Theory 84의 <code>NOT A DROP-IN</code> 판정은
보수적이고 타당하다.

### 4.2 Friedlander--Goldston 파일

- 679,866 bytes, SHA-256
  <code>4981fe4eb38f8788a74082d031063e4dd9e98c63411fbb31d761e346b8a01bd9</code>.
- PDF 24쪽, scan+OCR, printed pp.313--336.
- title·저자·journal이 요청 source와 일치한다.
- printed pp.314--317과 333--335를 원문 이미지로 대조했다.

GRH 아래 fixed-\(q\) upper \(G(x,q)\ll x(\log x)^4\)가 있다는 점을 Theory 84가
명시해 기존 source-range 설명을 정밀화했다. 그러나 상수·cutoff가 implicit이고
unconditional 목표가 아니므로 current numerical gate를 닫지 못한다. Theorem 1의
large-\(Q\) average와 Theorem 2의 lower bound도 방향·범위가 맞지 않는다.

## 5. 형식검증 경계

Lean terminal은 \(D,S_2\ge0\)에서

\[
 YS_2\le(Y+D)S_2
\]

와 strict inequality 합성만 검사한다. source analytic theorem, character induction,
GRH 또는 prime cancellation을 Lean premise 없이 발명하지 않는다. 따라서 Lean PASS는
Theory 84의 전 수론을 독립 증명했다는 뜻이 아니다.

Python은 finite arithmetic·source hash·OPEN flags를 검증한다. 실제 prime energy,
dataset, threshold는 계산하지 않는다.

## 6. 최종 상태

| 질문 | 판정 |
|---|---|
| sparse conductor decomposition은 정확한가 | <code>YES</code> |
| level 희소성이 character 총수를 줄이는가 | <code>NO</code> |
| generic sparse large-sieve RHS가 gate를 닫는가 | <code>NO</code> |
| actual \(V\)의 크기가 판정됐는가 | <code>NO</code> |
| prime-specific·weighted-correlation 경로가 남는가 | <code>YES</code> |
| 요청 Vaughan 2001 전문이 확보됐는가 | <code>NO</code> |
| Friedlander--Goldston 1996이 확인됐는가 | <code>YES</code> |
| numerical \(X_{\rm cert}\) 또는 bounded range가 생겼는가 | <code>NO</code> |

다음 최소 gate는 unconditional prime-specific fixed-primorial upper 또는 actual same-law
weighted-correlation theorem이다. 요청 Vaughan 2001 전문은 source completeness를 위해
추가 확보할 가치가 있으나, generic length-term 장벽 자체의 판정에는 필요하지 않다.
