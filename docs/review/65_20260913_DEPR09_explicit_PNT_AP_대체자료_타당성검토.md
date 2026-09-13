# DEP-R09 명시적 PNT-in-AP 대체자료 타당성검토

- 작성일: 2026-09-13 KST
- 검토 질문: Sono Section 5의 상수 전달 문제를 공식 정정 또는 현대 명시적 정리로
  고쳐 fixed \(2\times10^{-17}\)과 numerical \(X_{\mathrm{cert}}\)를 회복할 수 있는가?
- 상세 수식 정본: [Theory 58](../method/theory/58_Sono_FMT_DEPR09_explicit_PNT_AP_replacement_source_audit.md)
- 기계 판정: [replacement source audit v1](../method/theory/data/Sono_FMT_DEPR09_explicit_PNT_AP_replacement_v1.json)
- 결론: `즉시 끼울 수 있는 대체 정리 없음 / 고정 계수 경로는 계속 열어 둠`

## 1. 사용자가 먼저 알아야 할 결론

이번 조사는 “컴퓨터로 더 큰 소수까지 확인하면 해결되는 문제”가 아니다. 먼저 논문 증명의
중간 다리 하나를 숫자까지 포함해 고쳐야 한다.

확인 결과는 다음과 같다.

- Sono의 최신 공개 arXiv판과 journal판에도 문제의 식은 그대로 있다.
- 공개된 correction 또는 erratum은 찾지 못했다.
- 최근 연구에는 더 좋은 도구가 있지만, 우리가 필요한 최종 형태를 그대로 주지는 않는다.
- 현재 최종계수에는 여유가 매우 작아, 숨은 상수를 대충 크게 잡는 방식으로는
  \(2\times10^{-17}\)을 유지하기 어렵다.

따라서 \(X_{\mathrm{cert}}\)는 아직 계산할 수 없다. 지금 calculator를 만들면 “무엇을
계산해야 하는지 확정되지 않은 계산기”가 된다.

## 2. 무엇을 찾으려 했나

필요한 결과는 아주 쉽게 말해 다음과 같다.

> 충분히 큰 \(u\)에서, \(q\le u^{1/160}\)인 필요한 모든 산술수열마다 소수가 예상량의
> 일정 비율 이상 존재한다. 가능한 exceptional modulus 하나를 정확히 제외하고, 그 시작점도
> 숫자로 안다.

Sono가 사용한 비율은 \(1-e^{-2}\approx0.8646647\)이다. 이 한 문장 안에는 실제로 다음
네 계산이 들어 있다.

1. 주된 항이 얼마나 남는가.
2. 다른 character가 만드는 오차가 얼마나 작은가.
3. exceptional zero가 있을 때 무엇을 제외해야 하는가.
4. \(\psi\)라는 가중합을 실제 소수 개수 \(\pi\)로 바꿀 때 얼마가 손실되는가.

네 항이 같은 시작점부터 동시에 성립해야 한다.

## 3. 공식 정정 여부

arXiv `2404.06951v4`는 2024-06-05가 마지막 공개 revision이다. 이 판과 2025 journal
PDF의 Section 5를 다시 비교했지만 둘 다 다음 값을 그대로 쓴다.

\[
c_1=3c_{\rm ZFR},\qquad C_{\rm PAP}=1-e^{-2},\qquad D_{\rm PAP}=160.
\]

Theory 57에서 지적한 것처럼 첫 상수는 해당 Proposition의 분모를 직접 바꿨을 때 나오는
안전한 방향과 맞지 않는다. 공개 arXiv metadata와 journal page에서 별도 정정문도 찾지 못했다.

이 판정은 “저자가 설명할 방법이 없다”는 뜻이 아니다. 저자에게 묻는 일은 외부 연락이므로
이번에는 수행하지 않았다.

## 4. 후보들을 일상적인 말로 비교

| 후보 | 무엇을 잘하는가 | 왜 바로 못 쓰는가 | 판정 |
|---|---|---|---|
| Bennett et al. 2018 | 각 modulus에 실제 숫자 상계 제공 | 큰 \(q\)의 시작점이 너무 빨리 커져 \(q=u^{1/160}\) 전체를 못 덮음 | 부분 도구 |
| Bordignon 2021 | 중간 크기에서 매우 구체적 | \(q\)가 \((\log u)^\alpha\) 정도일 때만 적용 | 범위 부족 |
| Yamada 2014 | 많은 modulus의 평균오차를 명시 | 각 modulus마다 최소량을 보장하는 명제가 아님 | 논리형 불일치 |
| Kadiri | 작은 modulus의 zero-free region을 개선 | \(q\le400000\)에 한정 | 유한 분기 도구 |
| Thorner--Zaman PNT | 필요한 범위와 가장 가까운 현대적 구조 | 핵심 상수들이 “계산 가능”이라고만 되어 있고 숫자가 없음 | 주 대체후보, 재증명 필요 |
| Thorner--Zaman density | 큰 숫자이지만 multiplier까지 완전 명시 | zero 개수 상계일 뿐 실제 소수 최소량까지 가는 새 증명이 필요 | 명시적 부품 |
| Benli et al. DH | exceptional zero가 있을 때 다른 zero의 반발을 완전 명시 | 이것만으로 소수 개수 lower bound가 되지 않음 | 예외분기 부품 |

### 비유

우리가 필요한 것은 완성된 다리다. 최근 논문들은 더 강한 교각이나 더 정확한 볼트를 제공한다.
하지만 교각과 볼트를 모았다고 차량이 지날 수 있는 완성 다리가 자동으로 생기지는 않는다.
각 부품의 하중을 이어 붙이는 계산이 추가로 필요하다.

## 5. 왜 수치 여유가 중요한가

현재 downstream 식을 그대로 쓸 때 \(D=160\)에서 필요한 PAP 비율의 최소값은

\[
0.8638312615226712472\ldots
\]

이다. Sono가 쓴 \(1-e^{-2}\)는 약 \(0.8646647168\)이므로 두 값의 차이는 약
`0.0008334552`뿐이다.

쉽게 말하면 예상 소수량 100% 중 약 86.38% 이상을 보장해야 하는데, 원래 계산은 약
86.47%를 약속했다. 중간 보정에 쓸 수 있는 추가 여유는 전체 예상량의 약 0.0833%p뿐이다.
따라서 다음은 안전하지 않다.

- 숨은 배수가 “아마 1 정도”라고 가정
- 충분히 큰 시작점을 나중에 정하겠다고 두고 오차를 생략
- \(\psi\to\pi\) 손실을 0으로 취급

## 6. \(D\)를 키우면 해결되는가

항상 그렇지 않다. \(D\)를 키우면 \(q\le u^{1/D}\) 범위는 좁아져 중간 정리를 증명하기
쉬워질 수 있지만, Sono의 마지막 계수식 안에서도 비용이 늘어난다.

PAP 비율을 불가능할 정도로 좋게 \(C_{\rm PAP}=1\)이라고 가정해도:

- \(D=186\): 최종 진단값 약 \(2.01845\times10^{-17}\), 목표 위
- \(D=187\): 최종 진단값 약 \(1.99809\times10^{-17}\), 목표 아래

그러므로 **현재 나머지 상수를 그대로 둘 때** \(D\le186\)은 필요조건이다. 이는
\(D=186\) 정리가 이미 증명됐다는 뜻이 아니다.

## 7. 최근 fully explicit 결과의 정확한 의미

Thorner--Zaman은 zero-density exponent 127과 exceptional-zero 제거형 exponent 198을
포함한 완전 명시 결과를 제공한다. 이 숫자를 곧바로 PAP의 \(D\)라고 부르면 안 된다.
중간 transfer 방식에 따라 관계가 달라지기 때문이다.

다만 새 transfer가 \(D\ge198\)을 요구하는 형태라면, 현재 계수식의 절대 낙관 한계 186을
넘는다. 그때는 둘 중 하나가 필요하다.

1. 더 날카로운 transfer로 \(D\le186\)을 회복한다.
2. PAP 이외 downstream 손실도 함께 줄여 계수 여유를 새로 만든다.

따라서 exponent 198 결과는 무용하지 않지만 fixed 계수의 즉시 해결책도 아니다.

## 8. 권장 연구방향

### 주축: sharp \(D=160\) 복원

Thorner--Zaman PNT proof 또는 Gallagher--Jutila--Huxley 계열을 따라가며 다음을 숫자로
복원한다.

- density multiplier와 최초 범위
- prime-sum transfer multiplier
- exceptional zero가 있는 경우의 one-sided main term
- prime powers, partial summation, endpoint 손실

최종 합이 0.1361687384보다 작아야 하고, 기존 \(e^{-2}\) 형태를 그대로 살리려면 추가
손실이 0.0008334552보다 작아야 한다.

### 보조축: 완전 명시 부품 조합

Thorner--Zaman density와 Benli et al. DH를 사용해 더 보수적이지만 완전히 추적 가능한
PAP를 만든다. 이 경로가 \(D>186\) 또는 너무 작은 \(C_{\rm PAP}\)만 준다면 fixed 계수는
보존하지 못한다. 그래도 향후 “더 작은 엄밀한 계수” 연구의 기준선으로는 가치가 있다.

현재 연구목표는 사용자의 별도 결정 없이 더 작은 계수로 바꾸지 않는다.

## 9. 지금 필요한 계산자원과 사용자 작업

사용자 PC에서 장시간 소수 탐색을 할 단계가 아니다. 다음 단계는 논문 proof의 상수 추적과
짧은 exact/high-precision 대수 검증이다.

- 예상 작업시간: 문헌·증명 감사 수일 이상, 완전한 정량 재증명은 수주 이상 가능
- RAM/디스크: 현재 단계에서 32GB/50GB급 계산 불필요
- 추가 설치: 현재 필요 없음
- 사용자 수행절차: 별도 수행절차 필요없음

선택적으로 저자에게 정규화와 숨은 multiplier에 대한 설명을 문의할 수 있다. 외부 연락이므로
사용자의 별도 명시적 허가가 있어야 한다.

## 10. 최종 판정

```text
공개 correction/erratum             = 찾지 못함(2026-09-13 공개자료 범위)
즉시 사용 가능한 modern PAP         = 찾지 못함
고정 2e-17 회복 가능성               = 배제되지 않음, 정량 재증명 필요
PAP-11 / DEP-R09                     = HARD_BLOCKER / OPEN
X_cert                               = OPEN
이번 actual 소수 계산                = 수행하지 않음
```

## 11. 참고문헌

- Sono, [arXiv:2404.06951v4](https://arxiv.org/abs/2404.06951v4),
  [journal DOI](https://doi.org/10.4418/2025.80.2.2).
- Bennett et al., [arXiv:1802.00085](https://arxiv.org/abs/1802.00085).
- Bordignon, [arXiv:2101.08610](https://arxiv.org/abs/2101.08610).
- Yamada, [arXiv:1309.5798](https://arxiv.org/abs/1309.5798).
- Kadiri, [arXiv:math/0510570](https://arxiv.org/abs/math/0510570).
- Thorner--Zaman, [Refinements to the PNT in AP](https://doi.org/10.1007/s00209-023-03414-3).
- Thorner--Zaman, [Explicit Bombieri log-free density](https://doi.org/10.1515/forum-2023-0091).
- Benli--Goel--Twiss--Zaman,
  [Explicit Deuring--Heilbronn](https://doi.org/10.1090/proc/17450).
