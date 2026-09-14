# DEP-R09 FMT construction law 유한 성공질량 타당성 검토

- 작성일: 2026-09-14 KST
- 대상:
  [Theory 79](../method/theory/79_Sono_FMT_DEPR09_FMT_construction_law_finite_mass_audit.md)
- 기계 원장:
  [FMT construction mass v1](../method/theory/data/Sono_FMT_DEPR09_FMT_construction_mass_v1.json)
- 최종 판정:
  <code>FINITE_SIEVE_MASS_RECOVERED /
  SAME_LAW_CORRELATION_STILL_OPEN /
  NO_X_CERT_RANGE_YET</code>

## 1. 쉬운 결론

FMT의 소수 거르기 과정은 한 번의 추첨이 아니라 두 번의 연속 추첨과 비슷하다.

1. 먼저 작은 소수들에 어떤 나머지를 금지할지 \(\mathbf A\)를 고른다.
2. 그 결과가 좋을 때, 큰 소수들로 남은 수들을 더 덮는 \(\mathbf N'\)를 고른다.

최종 결과는 첫 번째 종이만 보고 정해지지 않고 두 종이
\((\mathbf A,\mathbf N')\)를 함께 봐야 정해진다. Theory 78은 후보를
\(\mathbf A\) 하나처럼 적었으므로 이번 감사가 이를 교정했다.

출판된 FMT 논문은 “수가 충분히 크면 거의 확실히 성공한다”는 \(1-o(1)\) 표현을 쓴다.
그 표현만으로는 컴퓨터에 넣을 구체적인 실패확률을 알 수 없다. 하지만 우리 프로젝트의
Theory 53·55는 두 단계의 실패율을 이미 각각 \(F_{\rm out}\), \(F_{\rm in}\)이라는
유한식으로 바꿨다.

예를 들어 첫 단계 실패율이 최대 \(1/5\), 첫 단계가 성공했을 때 둘째 단계 실패율이
최대 \(1/4\)라면, 둘 다 성공할 확률은 적어도

\[
 (1-1/5)(1-1/4)=3/5
\]

이다. 두 추첨이 서로 독립이라고 가정할 필요는 없다. 둘째 실패율이 모든 좋은 첫째
결과에서 공통으로 \(1/4\) 이하라는 조건이면 충분하다.

## 2. 이번에 실제로 진전된 부분

이전에는 “sieve 조건과 weighted correlation이 동시에 좋은 후보가 있는가?”라는 질문에서
sieve-good 후보의 유한 확률질량조차 명시되지 않았다고 적었다. 이번 감사 결과:

- 출판 FMT 단독: 여전히 비수치 \(1-o(1)\).
- 프로젝트 Theory 53·55까지 결합: sieve-good 질량은
  \((1-F_{\rm out})(1-F_{\rm in})\) 이상으로 parameterized explicit.
- 따라서 sieve-good positive mass 자체는 더 이상 새 hard blocker가 아니다.

이는 기존 정리를 뒤집은 것이 아니라 기존 finite 재증명에서 이미 확보한 정보를 올바른
joint law에 다시 놓은 것이다.

## 3. 아직 해결되지 않은 핵심

우리가 최종적으로 필요한 것은 sieve만 좋은 후보가 아니라 다음 두 조건이 동시에 좋은
같은 후보다.

1. 필요한 수들이 잘 덮여 큰 소수간격이 만들어짐.
2. 그 후보에서 소수분포 오차의 weighted correlation이 충분히 작음.

둘째 조건이 실패할 확률을 \(F_{\rm corr}\)라고 하면

\[
 F_{\rm corr}<(1-F_{\rm out})(1-F_{\rm in})
\]

을 증명하는 것이 충분하다. 현재는 \(F_{\rm corr}\)의 source-level numerical 상계가 없다.
특히 \(\mathbf A\)만 평균내고 최종 \(\mathbf N'\) 의존성을 없애면 실제 outcome의
correlation을 제어한 것이 아니다.

따라서 이번 결과는 selection 논리의 한 공백을 닫았지만 다음을 뜻하지 않는다.

- Sono의 fixed \(2\times10^{-17}\) 계수가 독립 인증됨.
- <code>PAP-11</code> 또는 <code>DEP-R09</code>가 닫힘.
- numerical \(X_{\rm cert}\) 범위가 생김.
- threshold 계산이나 장시간 prime sweep을 시작할 준비가 됨.

## 4. 문헌 대조

FMT Theorem 5는 good first-stage \(\mathbf A\) 각각에 Theorem 4를 조건부로 적용한다.
Section 6 formula (6.17)은 final \(n_p\)들이 \(\mathbf A\)가 주어졌을 때 jointly
conditionally independent하다고 명시한다. Theorem 3, Theorem 4와 Lemmas 6.3--6.4의
최종 확률은 \(1-o(1)\) 또는 hidden \(O\)-constant 형태다.

이 구조는 Theory 55의 순차 존재 proof와 일치한다. 이번 product mass는 새로운 독립성
가정이 아니라 “모든 outer-good fiber에서 inner failure가 \(F_{\rm in}\) 이하”라는
기존 uniform conditional statement를 합한 결과다.

문헌에서 현재 필요한 joint weighted-correlation failure bound를 바로 주는
drop-in theorem은 이번 source screen에서 식별하지 못했다. 이는 관련 전 문헌의 부재
증명이 아니라 현재 확인한 source 범위의 판정이다.

## 5. 코드와 Lean 검증의 의미

Python helper는 exact rational arithmetic으로 product mass, failure identity,
strict boundary, fiberwise union과 Markov 상계를 검사한다. source hash와 모든
상위 OPEN 상태도 fail-closed로 고정한다.

Lean은 다음의 유한 대수·선택 논리만 커널에서 검사한다.

- \(F_{\rm out}+(1-F_{\rm out})F_{\rm in}
  =1-(1-F_{\rm out})(1-F_{\rm in})\).
- correlation failure가 product mass보다 엄격히 작으면 잔여 mass가 양수.
- outer-good 후보를 고른 뒤 한 fiber에서 두 bad set을 피하는 finite selection.

FMT의 analytic \(1-o(1)\), probability measure construction, character sum 상계를
Lean 공리로 가장하지 않는다. 이 구분 때문에 Lean PASS는 전체 소수간격 정리의
형식증명이라는 뜻이 아니다.

## 6. 사용자가 지적한 Lean 곱셈 괄호 오류 재발성

사용자가 인용한
<code>((18/7)*theta)*L</code> 대 <code>theta*((18/7)*L)</code> 사건은 새 오류가
아니라 오류 원장 E117에 기록된 2026-09-13 첫 compile 사건과 동일하다.
E118·E119·E121에서도 분수와 곱의 결합 순서가 다른 비슷한 초안 실패가 있었다.
수학 부등식이 틀린 것은 아니지만 첫 초안 실패가 반복됐다는 지적은 타당하다.

현재 재발 방지 규칙은 다음과 같다.

1. 스칼라를 곱한 부등식은 최종 경계에서만
   <code>simpa only [mul_assoc, mul_left_comm, mul_comm]</code> 또는
   <code>convert ... using 1 &lt;;&gt; ring</code>으로 정규화한다.
2. 여러 선언을 누적하기 전에 canonical 단일 Lean 파일을 직접 컴파일한다.
3. 사용하지 않는 premise는 제거하되 source domain을 보존하는 안정된 interface에서만
   이유를 주석으로 적고 <code>_h...</code> 이름을 쓴다.
4. direct compile 뒤 전체 <code>lake build</code>를 별도 gate로 실행한다.
5. <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code> 0건을
   자동 검사한다.

이번 Theory 79 Lean 정리에서는 같은 위험을 피하려고 곱셈 모양을 손으로 맞춘
<code>exact</code> 대신 <code>ring</code>, <code>nlinarith</code>와
<code>sub_pos.mpr</code>를 경계별로 사용한다.

## 7. 권장 다음 작업

1. 식 (79.8)의 weighted badness를 joint outcome 전체에 정확히 정의한다.
2. 먼저 expectation을 outer/inner conditional expectation으로 분해할 수 있는지 감사한다.
3. global bound가 너무 강하면 모든 outer-good \(\mathbf A\)에 대한 fiberwise bound를
   검토한다.
4. 둘 다 source로 공급되지 않으면 신규 weighted-correlation lemma를 최소 단위로 분해한다.

이 단계는 문헌·증명 연구가 먼저이며 장시간 CPU prime 계산으로 대신할 수 없다.
현재 사용자 수행절차는 없다.

## 8. 참고문헌

- K. Ford, J. Maynard and T. Tao, *Chains of large gaps between primes*,
  Springer proceedings (2018), pp.1--21,
  [doi:10.1007/978-3-319-92777-0_1](https://doi.org/10.1007/978-3-319-92777-0_1),
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468).
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao,
  *Long gaps between primes*, Journal of the American Mathematical Society
  31 (2018), 65--105,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
