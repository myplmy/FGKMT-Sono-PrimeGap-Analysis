# Sono/FMT T1 hard-node 수치화 가능성 검토

- 작성: 2026-09-02 KST
- 입력: T1 66행 proof-obligation 원장
- 판정 대상: numerical (X_{\mathrm{cert}}) 연구를 계속할 실질적 가치와 난도
- 이번 문서가 하지 않는 것: 새 정리의 증명, 누락 상수의 추정, threshold 계산

## 1. 쉬운 말로 먼저 설명

현재 상황은 “공식은 아는데 계산기에 넣을 숫자가 몇 개 비어 있는 상태”보다 더 어렵다. Sono가
최종 계수 (2\times10^{-17})을 적어 두었지만, 중간 증명의 여러 문장은 다음과 같은 형태다.

- (x)가 충분히 크면 오차가 작다.
- 어떤 절대상수 (C)가 존재한다.
- 좋은 사건이 확률 (1-o(1))로 일어난다.

무한대로 보낼 때는 충분하지만 “정확히 어느 (x)부터?”라고 물으면 다음 숫자가 필요하다.

- 오차가 얼마나 빨리 작아지는가
- (O), (ll) 안의 상수가 얼마인가
- 여러 실패확률을 더했을 때 언제 1보다 작아지는가
- 한 construction 값뿐 아니라 모든 더 큰 (X)를 어떻게 빈틈없이 덮는가

좋은 소식은 현재 확인한 proof가 본질적으로 계산 불가능한 Siegel 상수에 기대지는 않는다는
점이다. 따라서 **원칙적으로 수치화할 가능성은 있다.** 나쁜 소식은 공개 논문 문장만으로 숫자를
꺼낼 수 없고, 일부 핵심 정리는 증명 안으로 들어가 상수를 다시 추적해야 한다는 점이다.

## 2. 전체 판정

\[
\boxed{
\text{연구 방향은 타당하지만, 현재 단계에서 numerical }X_{\mathrm{cert}}
\text{ 계산기를 만들면 안 된다.}
}
\]

| 질문 | 판정 |
|---|---|
| 수치화가 논리적으로 불가능하다고 밝혀졌는가 | 아니오 |
| Sono/FMT 출판본만 단순 대입하면 되는가 | 아니오 |
| 사용자 PC의 CPU·RAM이 현재 병목인가 | 아니오 |
| 전문적인 정량 재증명이 필요할 가능성이 큰가 | 예 |
| 쉬운 analytic node를 먼저 코드화하면 전체가 곧 닫히는가 | 아니오 |
| hard-node 가능성부터 확인하는 것이 타당한가 | 예 |

## 3. 난도별 분류

### A. 비교적 현실적인 node

| node | 무엇을 하면 되는가 | 난도·시간 추정 | 전체 threshold에 주는 효과 |
|---|---|---|---|
| `TRN-01`–`TRN-05` | explicit \\(\\vartheta(x)\\), primorial, 반복로그 단조성·rounding 부등식 선택 | 문헌 4–12시간, 구현·검증 4–12시간 | 필요한 층이지만 단독으로 \\(X_{cert}\\)를 주지 않음 |
| `AN-01`–`AN-02`, `UB-05` | explicit Mertens/PNT 정리를 interval inequality로 옮김 | 1–3일 | 쉬운 rate를 닫고 다른 blocker 크기를 드러냄 |
| `UB-06`–`UB-07` | (B_0), (a-b) finite product를 직접 상계 | 4–12시간 | UB의 elementary 부분 정리 |
| `SIV-06` | Maynard (8.27)의 finite-(r) remainder를 다시 추적 | 1–5일 | (c_{I,J}=1/4)의 시작 (r) 후보를 줌; sieve 전체는 안 닫힘 |

이 작업들은 ChatGPT가 정리 후보 비교·수식 전개·verifier 구현을 수행하고, 사용자 PC가 exact
interval 계산을 검산하는 방식이 적합하다. 예상 메모리와 디스크는 매우 작다. 다만 hard node가
막혀 있으면 이들만 끝내도 최종 숫자는 나오지 않는다.

### B. 중간 이상 난도의 node

| node | 핵심 문제 | 현실성 판정 |
|---|---|---|
| `UB-02`–`UB-04` | Halberstam–Richert upper-bound sieve의 (O)-상수와 모든 유효범위 | `POSSIBLE_BUT_REPROOF_LIKELY` |
| `PAP-03`–`PAP-10` | Gallagher/Jutila density estimate의 implied constant, exceptional case, (psi\to\pi) | `POSSIBLE_BUT_DEEP` |
| `AN-06`–`AN-11` | 여러 asymptotic error를 finite first/second-moment slack으로 합성 | `POSSIBLE_AFTER_INPUTS` |

UB는 PAP보다 구조가 단순할 가능성이 있지만, 책에 인쇄된 theorem의 proof constant를 처음부터
추적해야 한다면 짧은 코딩 작업이 아니다. PAP는 zero-density와 exceptional-zero case를 함께
다뤄야 하므로 더 깊다. 각각 전문 문헌 감사와 재증명에 수일에서 수주가 걸릴 수 있다.

### C. 현재 가장 큰 hard node

#### C1. FMT/Maynard good sieve weight — `SIV-01`–`SIV-11`

FMT Theorem 6에는 다음이 동시에 있다.

```text
r_0 sufficiently large
c_0 sufficiently small
tau >= x^{-o(1)}
u asymp log r
moment formulas with O-terms
good events with probability 1-o(1)
```

Maynard (8.27)은 (J_r/I_r=(\log r)/(4r)(1+O(1/\log r)))라는 유용한 rate 모양을 주지만,
그 한 식만 수치화해도 전체 weight construction의 다른 상수는 남는다. 특히 Maynard Proposition
6.1은 상수가 (	heta,alpha)와 Hypothesis 1의 implied constant에 의존한다고 명시한다. 따라서
“(c_{I,J}=1/4)만 검산하면 완료”라고 볼 수 없다.

판정은 `EFFECTIVE_IN_PRINCIPLE / NUMERICAL_REPROOF_REQUIRED`다. ChatGPT가 한 번의 세션에서
완전한 엄밀 증명을 보장할 수준은 아니다. 전문 분석수론 검토가 필요할 가능성이 가장 높다.

#### C2. quantitative hypergraph covering — `COV-06`–`COV-11`

FGKMT Theorem 3의 proof는 (delta)의 거듭제곱처럼 정량적인 모양을 많이 드러낸다. 그러나
(C_0,D,A,kappa) 등의 절대상수를 실제 숫자로 고정하지 않는다. FMT Theorem 4로 옮긴 뒤에도
(C\ll1), probability (1-o(1))이 남는다.

이는 원리상 algorithmic하게 추적할 수 있어 보이지만, 반복 nibbling의 모든 failure probability를
보수적으로 합치면 (X_{cert})가 극단적으로 커질 수 있다. 수학적 유효성과 유용한 크기는 별개다.

판정은 `POSSIBLE_IN_PRINCIPLE / LARGE_PROOF_ENGINEERING_PROJECT`다.

#### C3. arbitrary-(X) transfer — `TRN-06`

이 node 자체의 수학은 sieve weight보다 쉽다. 그러나 construction parameter가 허용되는 모든
조건을 이미 숫자로 갖고 있어야 각 (X)에 맞는 (x)를 선택할 수 있다. 따라서 순서상 마지막에
닫힌다. 특정 subsequence에서 gap을 만들었다는 것만으로 “모든 큰 (X)”를 주장하면 안 된다.

## 4. 누가 무엇을 할 수 있는가

| 작업 | ChatGPT | 사용자 PC | 현재 불가능·부적절한 부분 |
|---|---|---|---|
| 원문 식·의존성·부등식 방향 감사 | 수행 가능 | 불필요 | 없음 |
| 공개 explicit theorem 후보 검색·비교 | 수행 가능 | 불필요 | 출처 없는 상수 추정 금지 |
| rational/interval verifier 구현 | 입력이 확보되면 가능 | 빠른 독립 검산 가능 | 입력 미확보 상태의 계산기는 부적절 |
| finite-(r) integral 수치 검산 | 증명 contract 설계 가능 | 수분–수시간 계산 가능 | 계산만으로 uniform theorem을 대체할 수 없음 |
| 모든 Maynard/FMT 상수의 정량 재증명 | 부분 지원 가능 | 컴퓨터는 보조만 가능 | 한 세션·168시간 안에 완전 증명 보장 불가 |
| 천문학적 (X_{cert}) 아래 소수 전수검증 | 설계는 가능 | 현실적으로 불가능할 수 있음 | RAM 32GB·디스크 100GB·연속 168시간 한계를 넘길 가능성 큼 |

현재는 사용자에게 장시간 계산을 요청할 이유가 없다. scalar inequality 계산은 proof 상수가 모두
나온 뒤에는 싸지만, 상수를 얻는 일은 CPU 문제가 아니라 수학 문제다.

## 5. 수치 목표를 얼마나 낮춰야 도움이 되는가

이번 연구의 질문은 (2\times10^{-17})이라는 특정 계수이므로, 계수를 임의로 더 작게 바꿔서
proof를 쉽게 만들면 다른 정리를 증명하게 된다. 다만 탐색 단계에서 다음 세 목표를 구분할 수 있다.

| 목표 | 용도 | 판정 |
|---|---|---|
| 정확히 (2\times10^{-17}) | 프로젝트 본목표 | 최종 certificate에서 반드시 유지 |
| Sono nominal (widehat c)와의 전체 slack ledger | 각 오차에 허용량 배분 | T2에서 필요 |
| 더 작은 보조 계수 | proof pipeline smoke test | 명칭을 별도 정리로 분리할 때만 허용 |

nominal coefficient와 목표 사이의 상대차는 약 0.192688%다. 그러나 이 숫자만 보고 각 중간오차가
0.19%보다 작아야 한다고 단정할 수 없다. 12800·1800·25·20 같은 coarse constant가 만든 slack을
원래 식에서 다시 복원해야 한다.

## 6. 권장 연구 gate

### Gate H1 — sieve-weight recoverability

다음 네 질문에 답한다.

1. `SIV-01`: (r_0,c_0)를 proof에서 실제 숫자로 꺼낼 수 있는가?
2. `SIV-06`: Maynard (8.27)의 (O(1/\log r)) 상수를 rigorous하게 얻을 수 있는가?
3. `SIV-07`: Proposition 6.1의 implied constants를 Hypothesis 1 상수의 명시 함수로 쓸 수 있는가?
4. `SIV-08`: FGKMT application의 Hypothesis 1 상수를 PAP와 연결해 숫자로 만들 수 있는가?

판정 기준:

- 네 질문 모두 `YES_WITH_CONSTRUCTIVE_PATH`: T2/T3 계속
- 일부가 새 정량 lemma를 요구하지만 범위가 명확: 장기 proof plan 작성 후 사용자와 우선순위 협의
- source proof가 비효율적이거나 의존성이 닫히지 않음: numerical (X_{cert}) 축을 보류

예상시간은 1차 source tracing 1–3일, 실제 정량 재증명이 필요하면 수주 이상이다.

### Gate E1 — elementary transfer 후보 정리

H1과 병행하되 계산기는 만들지 않는다.

- explicit \\(\\vartheta(x)\\)/primorial theorem 후보
- explicit Mertens product 후보
- (F(X)) 단조성·rounding lemma
- construction parameter에서 arbitrary (X)를 덮는 규칙

예상시간은 문헌 선택과 lemma 초안 1–3일이다. 이 결과는 H1 실패 시에도 재사용 가능하지만,
H1보다 먼저 대규모 구현할 필요는 없다.

## 7. 최종 권고

1. 다음 실제 작업은 새 prime-gap 실험이 아니라 **Gate H1 source tracing**으로 한다.
2. H1의 첫 목표는 완전 재증명이 아니라 “어느 proof line에서 새 정량 lemma가 필요한가”를 더
   작게 자르는 것이다.
3. `TRN-01`–`TRN-05` 같은 쉬운 node는 H1과 병행 가능한 보조축으로 유지한다.
4. 모든 hard input이 닫히기 전에는 threshold calculator나 장시간 CPU runner를 만들지 않는다.
5. numerical (X_{cert})를 얻더라도 실제 최소점 (X_\star)를 결정한 것은 아니라는 구분을 유지한다.

이 방향에서 “좋은 결과”란 곧바로 작은 (X_{cert})가 나오는 것만을 뜻하지 않는다. 예를 들어
SIV-06을 수치화했지만 SIV-07이 막힌다는 정확한 결과도 매우 유용하다. 전체 연구에서 가장 비싼
막힌 지점을 조기에 찾아 불필요한 계산과 거짓 정밀도를 막기 때문이다.

## 8. 1차 문헌

- Keiju Sono, *An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes*,
  DOI: https://doi.org/10.4418/2025.80.2.2
- Kevin Ford, James Maynard, Terence Tao, *Chains of Large Gaps Between Primes*,
  arXiv: https://arxiv.org/abs/1511.04468
- Kevin Ford, Ben Green, Sergei Konyagin, James Maynard, Terence Tao,
  *Long Gaps Between Primes*, arXiv: https://arxiv.org/abs/1412.5029
- James Maynard, *Dense Clusters of Primes in Subsets*,
  arXiv: https://arxiv.org/abs/1405.2593
- Kevin S. McCurley, DOI: https://doi.org/10.1016/0022-314X(84)90089-1
- P. X. Gallagher, DOI: https://doi.org/10.1007/BF01403187
- Matti Jutila, DOI: https://doi.org/10.7146/math.scand.a-11701

## 9. 2026-09-02 H1 실행 결과

사용자 승인 뒤 source tracing을 실제 수행했다. 상세 정본은
[`24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md`](24_20260902_Sono_FMT_H1_good_sieve_weight_recoverability.md)다.

- Maynard (8.25)–(8.27)은 standalone finite-r lemma로 복원할 constructive path가 확인됐다.
- Proposition 6.1과 FGKMT Hypothesis 1은 effective-in-principle이지만 ready-made numerical
  constant가 아니며 정량 재증명이 필요하다.
- Sono의 (c_0=1/5) 선택은 인쇄돼 있으나 finite (r_0)과 모든 error의 공통 시작 (x)는 없다.
- 따라서 H1은 실패나 불가능 판정이 아니라
  `CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED`다.
- 다음 최소 gate는 H1a finite-r integral lemma이며 threshold calculator·새 prime sweep은 계속
  fail-closed다.

## 10. 2026-09-04 H1a 사후 갱신

H1a를 실제 정식화하여 `SIV-06`을 모든 정수 (r\ge36)에서 `EXPLICIT`으로 닫았다. 유한
(36\le r\le8103)은 directed interval 전수검사, (r\ge8104)는 해석적 꼬리 증명이다. 따라서
이 문서의 “SIV-06을 수치화할 수 있는가?”라는 질문에는 이제 **예**라고 답할 수 있다.

다만 `SIV-07` Proposition 6.1 moment 상수, `SIV-08` Hypothesis 1/PAP, `SIV-09/10/11` 합성
오차가 남아 있으므로 전체 H1과 (X_{\mathrm{cert}})는 열려 있다. 다음 최소 gate는 H1b이며,
threshold calculator·새 prime sweep의 fail-closed 상태도 유지한다. 상세 증명은
[`13_Sono_FMT_H1a_finite_r_integral_lemma.md`](../method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md)다.

## 11. 2026-09-08 H1b-2a.3까지의 후속 갱신

H1b를 하위 의무로 분해해 Lemmas 8.2--8.6의 actual-input package와 Proposition 9.4의
실제 FGKMT/FMT 호출을 단계적으로 수치화했다. 최신
[`H1b-2a.3 정본`](../method/theory/31_Sono_FMT_H1b2a3_Proposition94_end_to_end_composition.md)은
P94의 모든 닫힌 child를 합성해 모든 정수 \(k\ge36\)에서 actual-call multiplier가
13 미만임을 보였다. 따라서 H1b 하위행 `H1B-P94`는
`ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이다.

하지만 Gate H1의 질문 3은 Proposition 6.1 전체에 관한 것이므로 답은 아직 “부분적으로만
예”다. Proposition 9.2의 수치 소수분포 입력과 P91/P92/L93/P95 공통 budget이 남아
`SIV-07=HARD_BLOCKER`, \(X_{\mathrm{cert}}=)`OPEN`이다. 따라서 장시간 threshold 계산을
시작하지 않는 기존 권고는 유지한다.

## 12. 2026-09-09 H1c-1a source inventory 후속 갱신

H1c-1a는 Proposition 9.2의 수치 소수분포 입력에 대해 바로 대입 가능한 source가 없음을
확인하고, Bordignon 2021을 첫 합성 후보로 선정했다. 이는 `POSSIBLE_BUT_DEEP` 판정을 더
구체화한 것이며 hard node를 닫은 것은 아니다. 12개 bridge/composition 의무 중 먼저
fixed-\(k\) 여부와 affine modulus envelope를 검토하면, 큰 계산 전에 이 경로의 가능성을
낮은 비용으로 판정할 수 있다.

사용자 PC의 CPU·RAM은 여전히 현재 병목이 아니다. symbolic parameter와 common exceptional
modulus가 정해지기 전에는 장시간 runner를 만들지 않는다.
