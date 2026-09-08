# H1c-1a quantitative prime-distribution source inventory 타당성 검토

- 작성: 2026-09-09 KST
- 검토 대상: FGKMT Hypothesis 1(2)와 Maynard Proposition 9.2를 numerical package로
  만들기 위한 선행정리 후보
- 상세 정본:
  [`../method/theory/32_Sono_FMT_H1c1a_quantitative_prime_distribution_source_inventory.md`](../method/theory/32_Sono_FMT_H1c1a_quantitative_prime_distribution_source_inventory.md)
- 기계 판독 원장:
  [`../method/theory/data/Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json`](../method/theory/data/Sono_FMT_H1c1a_quantitative_prime_distribution_inventory_v1.json)
- 최종 판정: `타당한 연구 방향 / 단일 drop-in 정리 없음 / Bordignon 2021 합성 경로 우선`

## 1. 쉬운 설명

지금 필요한 것은 “소수들이 대체로 고르게 퍼진다”는 일반 사실이 아니다. Maynard의 sieve가
사용하는 아주 구체적인 표에 대해 다음을 동시에 보증해야 한다.

- 조사해야 할 모든 modulus를 빠뜨리지 않는다.
- 한 exceptional prime \(B\)만 피한다.
- 여러 affine form과 구간 끝점을 모두 같은 규칙으로 다룬다.
- 오차가 \((\log x)^{-100k^2}\)만큼 작다.
- 오차 앞 상수와 이 식이 시작되는 최초 범위를 숫자로 안다.

비유하면, 기존 논문들은 대부분 “이 다리는 충분히 큰 차를 견딘다”거나 “특정 종류 차량에는
정확히 몇 톤까지 견딘다”를 증명한다. 우리는 **우리 차량의 축간거리·무게·진입각까지 모두
맞는 한 장의 검사증**이 필요하다. 조사한 논문 중 그 검사증을 그대로 주는 논문은 없었다.

그러나 가장 가까운 부품 묶음은 찾았다. [Bordignon 2021](https://nyjm.albany.edu/j/2021/27-54.html)은
임의 \(A>3\)에 명시적 평균상계를 주므로 필요한 강한 log-saving을 조립할 가능성이 있다.
그래서 이 논문을 H1c-1b의 첫 후보로 정했다.

## 2. 사용자 아이디어와 연구 방향은 타당한가

타당하다. 숨은 “충분히 큰 \(x\)”를 numerical threshold로 바꾸려면 먼저 이미 존재하는
explicit distribution theorem을 찾아 적용하는 것이 직접 재증명보다 효율적이다. 다만 다음
안전장치가 반드시 필요하다.

1. 비슷한 이름의 정리가 아니라 실제 Maynard 중심항과 modulus family를 대조한다.
2. 논문에서 증명하지 않은 affine transfer를 “자명”이라고 생략하지 않는다.
3. explicit라는 말이 상수·cutoff까지 모두 숫자라는 뜻인지 확인한다.
4. preprint와 교정이 필요한 식을 출판 정본과 같은 수준으로 채택하지 않는다.

이번 inventory는 이 원칙대로 수행됐다. 직접증명을 시작하기 전에 선행정리를 찾았지만, 적용에
필요한 연결부는 별도 H1c-1b proof obligation으로 남겼다.

## 3. 무엇이 그대로 쓸 수 없었는가

| 후보 | 좋은 점 | 직접 적용을 막는 핵심 |
|---|---|---|
| [Akbary--Hambrook](https://arxiv.org/abs/1309.2730), [Sedunova 2018](https://doi.org/10.5802/pmb.24) | explicit 평균상계 | 모든 작은 소인자를 피하는 rough-modulus 조건은 \((q,B)=1\)과 다름 |
| [Yamada II](https://arxiv.org/abs/1309.5798) | exceptional modulus 구조가 가까움 | \(A\le7\); 필요한 \(100k^2\) saving에 크게 부족, preprint |
| [Bennett et al.](https://arxiv.org/abs/1802.00085) | fixed modulus별 explicit \(\psi,\theta,\pi\) | \(q\le x^{1/3}\) 전체 평균상계로 바로 합치면 너무 약함 |
| [Kadiri](https://arxiv.org/abs/math/0510570) | \(q\le400000\)에서 더 좋은 zero-free constant | 낮은 conductor 일부만 담당 |
| [Liu](https://doi.org/10.1007/s10474-017-0745-z) | all-moduli effective route | log-saving이 고정 \(-2\) 수준이고 숫자 multiplier가 인쇄되지 않음 |
| [Johnston 2026](https://arxiv.org/abs/2510.10853) | exceptional modulus를 sieve 설계로 피하는 새 경로 | Maynard P9.2와 다른 정리이며 최근 preprint; 새 호환성 proof 필요 |

[Sedunova 2019](https://doi.org/10.5802/jtnb.1098)의 cited effective corollary는 Johnston 2026이
작은 오류를 지적해 log 분모 지수를 \(B-2\)에서 \(B-3\)으로 교정한다. 따라서 원문 식을 그대로
가져오는 방안은 배제했다.

## 4. Bordignon 경로의 타당성과 위험

### 타당한 부분

- peer-reviewed 출판본이다.
- Theorem 1.4가 임의의 실수 \(A>3\)를 허용한다.
- 예외모듈을 분리한 explicit 평균상계와 Theorem 2의 pointwise component가 함께 있다.
- \(q\le x^{1/3}\)은 고전적인 \(x^{1/2}\) 범위보다 작으므로, log 손실을 감안한 modulus
  coverage가 충분히 큰 \(x\)에서 가능할 개연성이 있다.

### 아직 증명이 필요한 부분

- “충분히 큰 \(x\)에서 가능”을 실제 finite inequality와 cutoff로 바꾸기
- \(A=100k^2+\)여유를 넣을 때 상수 \(C(A,A-3,X_0)\)의 증가를 통제하기
- \(|a|q\) modulus와 모든 endpoint가 같은 theorem instance에 들어가는지 확인하기
- 하나의 exceptional conductor와 \(B\)를 전 범위에 고정하기
- \(\psi\)의 main term을 Maynard의 exact total-count center로 바꾸기
- prime powers, half-open endpoint와 represented-prime lower bound를 합치기

따라서 “유망하다”는 말은 **알고리즘 실행이나 threshold 계산을 시작해도 된다**는 뜻이 아니다.
먼저 작은 수의 symbolic inequality를 닫아 이 경로가 정말 합성되는지 판정해야 한다.

## 5. 잘못 해석하면 안 되는 결론

```text
Bordignon theorem is explicit
    != FGKMT Hypothesis 1(2) is now explicit
source inventory is complete
    != numerical proof package is complete
q <= x^(1/3) is asymptotically inside sqrt(x)/log^A(x)
    != a verified finite cutoff is known
effective theorem exists
    != its multiplier and first valid x are printed
```

이번 작업으로 `SIV-07/08`, Proposition 9.2, good sieve weight와
\(X_{\mathrm{cert}}\)는 모두 계속 열린다. prime/maximal-gap 계산을 더 멀리 돌리는 것은 이
증명 병목을 해결하지 않는다.

## 6. 권장 다음 순서

| 순서 | 작업 | 권장 근거 | 예상 소요 |
|---:|---|---|---|
| 1 | H1c-1b.1 fixed-\(k\) 여부와 Bordignon parameter/modulus envelope 감사 | 가장 먼저 경로 자체가 성립 가능한지 싼 비용으로 판정 | 문헌·수식 1--3일 |
| 2 | H1c-1b.2 한 exceptional conductor/prime \(B\) uniformization | 실패하면 Bordignon 합성 전체가 막히므로 조기 확인 가치가 큼 | 2--5일 이상 |
| 3 | H1c-1b.3 affine·endpoint·\(\psi\to\pi\)·recentring lemma | 실제 Maynard 표기로 가는 필수 다리 | 3--10일 이상 |
| 4 | H1c-1b.4 prime-density와 common cutoff | 앞 세 단계가 닫힌 뒤에만 수치 calculator 입력이 됨 | 수일--수주 |
| 보조 | original FGKMT 또는 Johnston redesign branch | Bordignon 경로가 막힐 때만 비교 | 별도 수주 가능 |

예상시간은 원문 검토와 증명 정식화 시간이다. 지금은 3--12시간 CPU runner를 돌릴 단계가 아니다.
구체적인 scalar cutoff 식이 나온 뒤 사용자 PC 검증 runner를 별도 설계한다.

## 7. 사용자에게 필요한 일

현재는 없다.

```text
실행 환경: 해당 없음
시작 경로: 해당 없음
명령: 별도 수행절차 필요없음
예상 시간: 0분
로그·산출물 회신: 없음
```

다음 단계 착수 여부만 사용자가 결정하면 된다. 권장안은 H1c-1b.1부터 진행하는 것이다.

## 8. 최종 판정

```text
연구 질문의 타당성                  = YES
선행정리 우선 조사 전략             = YES, 적용성 개별 감사 조건부
바로 대입 가능한 single theorem     = NOT FOUND
가장 가까운 peer-reviewed 후보      = BORDIGNON2021
추가 직접증명 필요                  = YES, 12개 bridge/composition 의무
지금 numerical threshold 계산 가능 = NO
X_cert                              = OPEN
```

## 9. 2026-09-09 H1c-1b.1 후속 보정

후속 감사에서 Bordignon modulus 폭은 충분하다고 확인했지만, 원래 \(x\)에서 고른 sieve
dimension을 actual \(x/2\) 호출에 그대로 넣을 때 짧고 반복되는 transition strip에서 한 칸
초과할 수 있음을 발견했다. \(r-1\)로 줄이면 정확히 안전하지만 Sono의 최종 coefficient에
미치는 영향을 다시 대입해야 한다.

따라서 이 문서 6절의 과거 2순위보다 새 H1c-1b.1a를 먼저 수행한다. 상세 판정은
[`H1c-1b.1 검토`](39_20260909_H1c1b1_parameter_modulus_envelope_타당성검토.md)를 따른다.
