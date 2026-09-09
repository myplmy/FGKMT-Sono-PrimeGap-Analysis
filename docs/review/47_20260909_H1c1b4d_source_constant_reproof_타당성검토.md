# H1c-1b.4d Bordignon source constant 재증명 타당성 검토

- 작성: 2026-09-09 KST
- 검토 대상: H1c-1b.4d corrected source-constant reproof
- 판정: `NARROW PROJECT LEMMA ACCEPT / PARENT PROMOTION DEFER`
- 실제 소수 실험: 수행하지 않음

## 1. 요약 판정

이번 결과는 받아들일 수 있다. 최종 Bordignon Theorem 3.4와 식 (28)--(32)에서 actual
target에 필요한 상수를 다시 만들고, 모든 source component를 보수적으로 포함했다.
\(r\ge10^{10}\)에서 exact corner·미분 비교로 \(C_A<1\)을 얻으므로 H1c-1b.4c의 조건부
빈칸은 이 더 큰 cutoff에서 채워진다.

그러나 다음 이유로 H1(2), Maynard Proposition 9.2, `SIV-08`을 아직 `EXPLICIT`으로
올리면 안 된다.

- 여러 선행 bridge의 quantifier와 공통 exceptional \(B\)가 실제 한 호출에서 일치하는지
  아직 end-to-end 감사하지 않았다.
- cutoff \(10^{10}\)은 충분조건이지 최소값이 아니다.
- Bordignon 출판 상수식에는 실제 표기·정규화 문제가 있어, 이번 결과는 저자 erratum이
  아니라 project reproof다.
- 이 하위 cutoff를 전체 Sono/FMT theorem threshold와 동일시할 수 없다.

## 2. 잘된 부분

### 2.1 선행연구를 먼저 확인함

Bordignon 최종 journal 판을 주 source로 삼고, zero-density 수치는 Liu--Wang 2002의
Theorems 1--2와 표까지 대조했다. 별도 drop-in 정리를 찾지 못한 뒤에만 실제로 빠진
normalization·composition bridge를 직접 증명했다. 이는 “기존 증명을 우선 재사용하되
현재 변수·범위에 맞는지 개별 확인한다”는 작업 규칙에 맞는다.

### 2.2 판본 차이를 fail-closed로 처리함

arXiv v1 식 (31)은 \(q\)가 없지만 최종판은 \(2q\)다. 더 작은 v1 식을 편의상 쓰지 않고
최종판의 큰 계수를 보존했다. Corollary 4.3의 존재형 unknown-\(i\)도 임의의 유리한 값을
선택하지 않고 여섯 경우의 공통 최악값으로 바꿨다.

### 2.3 항 누락 방지 장치가 있음

Theorem 3.4 remainder 9개와 zero 4개를 이름 붙인 13개 component로 고정했다. machine
contract와 unit test는 component 수, 최종 `2q`, source hash, 상위 node의 false flag를
확인한다. 모든 항을 먼저 양수 upper로 분리했으므로 상쇄에 의존하지 않는다.

### 2.4 floating-point를 증명으로 쓰지 않음

100자리 계산은 회귀진단에만 쓴다. 실제 cutoff는 exponential series의 rational enclosure,
exact integer power, rational derivative-dominance와 symbolic monotonicity로 운반한다.

## 3. 작업 중 발견하고 교정한 오류

초기 판독에서는 arXiv v1 식 (31)에 \(q\)가 없는 것을 보고 최종판도 같다고 잘못 판단했다.
최종 NYJM PDF p.1431을 다시 확대 대조해 `2q`를 확인했고, 다음을 즉시 고쳤다.

- low-zero upper의 계수와 \(L\)-지수,
- helper key와 구조 certificate,
- JSON source-correction 설명,
- unit test의 final-vs-v1 negative control.

수정 후 8개 표적 회귀시험이 모두 통과했다. 이 실수는 결론을 유리하게 만들기 위해 숨기지
않으며, 최종판 우선 규칙을 더 강하게 만든 사례로 원장에 보존한다.

## 4. 남은 위험과 한계

### 4.1 출판식 문제에 대한 외부 승인 없음

H1c-1b.4a에서 final 식 (33)의 첫 항은 absolute \(R^*\)에 \(x\)-정규화가 없어 unbounded
supremum을 주지 못한다고 판정했다. 이번 (41.3)은 표시된 target과 Theorem 3.4에서 직접
유도한 교정이다. 논리적으로 검산할 수 있지만 저자가 공인한 erratum은 아니다. 향후 외부
공개 전에는 독립 수학 검토를 받는 것이 바람직하다.

### 4.2 보수적 cutoff

\(r=10^{10}\), 즉 source endpoint에서 \(\log x\ge10^{50}\)는 엄청나게 크다. 이것은
계산으로 순회할 범위가 아니며 최소성도 없다. 더 날카로운 `min_J`, source 항별 상수 또는
최적 contour height를 쓰면 낮아질 수 있으나, 전체 proof threshold의 다른 항이 더 클 수
있으므로 지금 최적화하는 우선순위는 낮다.

### 4.3 calculus 문서와 구현의 역할

helper는 exact base-corner 부등식과 대표 monotonicity 조건을 검사한다. 무한구간 증명 자체는
문서의 미분 부호와 증가비율 논증이다. 소프트웨어 test만으로 theorem을 증명했다고 표현하면
안 된다. 반대로 문서 식을 바꾸면 helper와 JSON도 함께 갱신해야 한다.

### 4.4 아직 닫히지 않은 composition

이번 단계는 source constant만 닫았다. 다음에는 H1c-1b.1--1b.4d의 모든 가정이 동일한
\(T,r,A,Q_1,B\)에 동시에 성립하는지 검사해야 한다. 특히 half-open endpoint, q=1 exact
centering, common exceptional object, 두 dyadic endpoint와 strict/non-strict inequality가
중요하다.

## 5. 수치 해석에서 금지할 표현

- “실제로 \(e^{10^{50}}\)까지 소수를 검증했다.” — 거짓이다.
- “Sono/FMT 부등식의 최종 threshold가 \(e^{10^{50}}\)다.” — 아직 거짓이다.
- “Bordignon 논문이 \(C_A<1\)을 직접 명시했다.” — 거짓이다.
- “H1(2)가 닫혔다.” — composition 전에는 과장이다.

허용되는 표현은 “Bordignon의 표시된 하위 upper들을 보수적으로 재합성하면,
\(r\ge10^{10}\)에서 actual target에 필요한 source constant를 1보다 작게 만들 수 있다”다.

## 6. 검증 결과

- `tests.test_h1c1b4d_source_constant_reproof`: 8/8 PASS
- helper/test `py_compile`: PASS
- 최종판 `2q` negative control: PASS
- unknown-\(i\) global-minimum check: PASS
- source/predecessor SHA-256 checks: PASS
- 상위 node false flags: PASS
- 금지된 base-log 또는 잘못된 프로젝트 약칭: 0건

## 7. 다음 권장 단계

H1c-1b.4e end-to-end composition audit를 먼저 수행한다. 예상 소요는 3--6시간이다.
수식·문서·toy verification만 필요하므로 사용자 PC의 장시간 계산, Lean 또는 새 Python
package는 필요하지 않다. composition이 통과할 때만 actual identity-form H1(2)/P9.2와
`SIV-08`의 상태 승격을 검토한다.
