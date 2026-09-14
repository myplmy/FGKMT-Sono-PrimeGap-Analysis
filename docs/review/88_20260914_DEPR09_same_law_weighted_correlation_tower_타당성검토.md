# DEP-R09 동일법칙 weighted-correlation tower 타당성 검토

- 작성일: 2026-09-14 KST
- 대응 이론:
  [Theory 80](../method/theory/80_Sono_FMT_DEPR09_same_law_weighted_correlation_tower_audit.md)
- 기계 원장:
  [same-law weighted correlation v1](../method/theory/data/Sono_FMT_DEPR09_same_law_weighted_correlation_v1.json)
- 판정:
  <code>FINITE_BOOKKEEPING_VALID /
  SOURCE_GAP_PRECISELY_LOCALIZED /
  ANALYTIC_MOMENT_NOT_PROVED</code>

## 1. 한 문장 결론

FMT의 소수 거르기와 “소수분포 오차가 작다”는 조건을 같은 추첨 결과에서 동시에 만족시키려면,
그 추첨법 아래 weighted error의 평균제곱이 일정 문턱보다 작다는 새 정리가 필요하다.
이번 작업은 그 문턱을 정확히 계산했지만, 평균제곱 자체를 작게 만드는 수론 정리는 아직 없다.

## 2. 쉬운 예시

두 번 추첨해서 최종 후보를 만든다고 생각하면 된다.

1. 첫 번째 추첨으로 작은 소수의 금지 나머지를 정한다.
2. 둘째 추첨으로 큰 소수의 금지 나머지를 정한다.

기존 Theory 79는 “두 추첨의 거르기 조건이 모두 좋은 후보”가 양의 확률로 존재함을 유한식으로
복원했다. 그러나 같은 후보에서 소수분포 오차까지 작아야 한다.

예를 들어 sieve-good 후보가 적어도 60%이고, weighted-error가 나쁠 확률을 평균제곱으로
최대 10%라고 증명할 수 있다면 둘 다 좋은 후보가 적어도 50% 남는다. 반대로 weighted-error
실패율을 전혀 모르면 sieve-good 후보가 많다는 사실만으로 둘의 교집합을 보장할 수 없다.

## 3. 이번 진전의 학술적 의미

이전 질문은 “FMT의 무작위성을 이용하면 평균으로 해결할 수 있지 않을까?”였다. 이번에는
이를 검증 가능한 세 가지 명제로 분해했다.

- 전체 joint law에서 평균제곱을 상계하는 **global route**.
- outer-good 후보들만 조건으로 평균제곱을 상계하는 **conditional route**.
- 좋은 첫 추첨값 각각에서 상계하는 더 강한 **uniform-fiber route**.

가장 약하고 유리한 목표는 global route다. 필요한 수치는

\[
 \mathbb E[W]
 <\tau^2(1-F_{\rm out})(1-F_{\rm in})
\]

이다. 여기서 \(W\)는 weighted prime error를 실제 survivor 수와 prime scale로 나눈
제곱값이다. 이 식 덕분에 앞으로 어떤 선행정리나 새 증명이 “충분히 강한지”를 모호한 말이
아니라 수치로 판정할 수 있다.

## 4. 왜 기존 FMT 정리만으로는 부족한가

FMT/FGKMT covering 정리는 미리 정해 둔 부분집합에서 몇 개가 살아남는지를 보존한다.
이는 음수가 없는 **개수** 정보다.

이번에 필요한 것은 final covering 결과가 정한 CRT 이동량에 따라 각 항의 복소 위상이
바뀌는 **signed/complex 가중합**이다. 즉 측정하려는 저울 자체가 추첨 결과에 따라 바뀐다.
fixed-subset 정리를 그대로 적용하면 양화사 순서가 뒤집힌다.

또한 원문의 성공률은 \(1-o(1)\)이고 공통 numerical rate가 인쇄되지 않았다. 가능한 모든
가중합을 union bound하는 우회도 현재 유한 증명이 아니다.

## 5. Maier와 Sono가 해결책이 아닌 이유

Maier 1981과 Sono는 fixed CRT residue마다 pointwise prime-distribution lower bound를 쓴다.
그 뒤 별도의 matrix row 변수 \(z\)를 평균내어 좋은 행을 고른다.

이 \(z\)는 FMT가 만든 CRT 이동량 \(m(\mathbf A,\mathbf N')\)을 평균내는 변수가 아니다.
따라서 \(z\)-평균이 있다고 해서 construction-dependent character correlation이 작아지는 것은
아니다. 기존 pointwise PAP를 되살리는 경로는 앞선 상수 감사에서 너무 큰 multiplier 때문에
막혔고, 이번 average route는 별도의 새 moment 정리를 요구한다.

## 6. 반드시 보존해야 할 안전장치

1. 최종 outcome을 \(\mathbf A\) 하나가 아니라 \((\mathbf A,\mathbf N')\)로 쓴다.
2. preliminary independent edge를 final covering output과 바꾸지 않는다.
3. survivor 수 \(M_\omega\)가 0일 수 있는 곳에서 나누지 않는다.
4. raw 제곱평균을 쓸 때는 평균 survivor 수가 아니라 pointwise lower floor가 필요하다.
5. equality \(W=\tau^2\)는 목표 부등식의 good boundary에 포함한다.
6. exact finite 확률대수 PASS를 analytic character-sum theorem PASS로 승격하지 않는다.

## 7. 선행연구 판정

확인한 FMT, FGKMT, Maier, Sono 원문과 targeted hypergraph/character-moment 검색에서는
actual final FMT law와 CRT-output-dependent 복소 observable을 동시에 다루고, numerical
multiplier와 finite cutoff까지 제공하는 drop-in theorem을 식별하지 못했다.

이 결론의 범위는 중요하다. “그런 정리는 수학 문헌 어디에도 없다”는 전수 부재 증명이
아니다. 현재 확인한 source와 검색어 아래에서는 바로 대입할 결과를 찾지 못했다는 뜻이다.
일반 hypergraph nibble survey는 방법 배경으로는 유용하지만 필요한 character observable을
다루지 않는다.

## 8. 코드·Lean 검증이 보장하는 것

exact Python fixture 9개는 다음을 검증한다.

- conditional expectation으로 더한 값과 joint atom을 직접 더한 값이 정확히 같음.
- global/conditional/fiberwise 문턱과 equality boundary.
- 조건부 확률질량이 1이 아니거나 badness가 음수이면 즉시 실패.
- survivor floor가 0이면 raw moment 정규화를 거부.
- source hash와 OPEN 상태가 바뀌면 machine-ledger 검증 실패.

Lean은 같은 finite-sum 및 실수 대수만 kernel에서 검증한다. 외부 수론 정리를 공리로 넣지
않으므로, Lean PASS는 식 변형의 오류 전파를 막지만 missing analytic lemma를 대신하지 않는다.

## 9. \(X_{\rm cert}\)에 미치는 영향

이번 결과로 numerical \(X_{\rm cert}\) 상한이나 범위가 새로 생기지는 않았다.

- finite observed 범위에서 Sono 부등식이 처음 성립하는 값과,
- 모든 더 큰 \(X\)에서 정리가 성립한다고 증명하는 theorem threshold \(X_{\rm cert}\)

는 계속 다른 대상이다. 이번 작업은 두 번째 대상의 proof chain에서 필요한 missing lemma를
더 정확히 지정했다. fixed \(2\times10^{-17}\), <code>PAP-11</code>,
<code>DEP-R09</code>는 모두 OPEN이다.

## 10. 다음 권장 작업

1. **actual FMT filtration 민감도 감사 — 권장.**
   final covering output을 한 단계씩 드러낼 때 \(R(\omega)\)가 한 단계에서 얼마나 바뀌는지
   exact하게 계산한다. bounded-difference나 martingale second moment가 가능한지 판정한다.
2. **survivor denominator floor 재사용 감사.**
   Theory 55의 interval-wise lower count가 식 (80.8)에 필요한 pointwise \(M_{\min}\)으로
   그대로 쓸 수 있는지 상수·event 범위를 대조한다.
3. **불가능하면 reserve-randomization 설계 감사.**
   covering에 쓰이지 않은 residue의 일부를 독립 randomization으로 남기되 coverage와
   survivor lower bound를 잃지 않는지 먼저 증명한다. 현재는 아이디어이고 결과가 아니다.
4. **장시간 계산은 보류.**
   지금은 prime sweep이나 threshold calculator가 missing analytic lemma를 검증하지 못한다.

예상 작업시간은 1번 source/proof audit 3--6시간, 2번 1--3시간, 3번은 가능성 판정만
4--8시간이며 새 정리의 완전 증명시간은 아직 추산할 수 없다. 현재 사용자가 실행할 절차는 없다.

## 11. 참고문헌

- Ford--Maynard--Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468),
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1).
- Ford--Green--Konyagin--Maynard--Tao, *Long gaps between primes*,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
- Maier, *Chains of large gaps between primes*,
  [doi:10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- Sono, *An explicit lower bound for gaps between some consecutive primes*,
  [doi:10.1007/s40993-024-00569-8](https://doi.org/10.1007/s40993-024-00569-8).
- Kang--Kelly--Kühn--Methuku--Osthus, *Graph and hypergraph colouring via nibble
  methods: A survey*, [arXiv:2106.13733](https://arxiv.org/abs/2106.13733).
