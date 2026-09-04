# Stadlmann, *Bounded Gaps Between Primes* 비판적 검토

- 검토일: 2026-09-04 KST
- 저자: Julia Stadlmann
- 원문: `article/unverified/BOUNDED GAPS BETWEEN PRIMES.pdf`
- 원문 식별: arXiv:2608.31126v1, 2026-08-31
- 페이지: 34
- PDF SHA-256: `4296e63a3028fcff62725c7e751811679cbfea78e4d4213486b2f9a3e81ee994`
- 심사 상태 판정: `UNVERIFIED PREPRINT / PEER REVIEW NOT CONFIRMED`
- 연구 채택 판정: `PLAUSIBLE HIGH-IMPACT CLAIM / INDEPENDENT NUMERICAL VERIFICATION BLOCKED`

## 1. 한 줄 결론

이 논문은 기존 무조건부 bounded-prime-gap 상한 \(246\)을 \(240\)으로 낮췄다고 주장하며,
논증의 큰 구조는 현대 GPY/Maynard–Tao 계열과 최근 smooth-moduli 분포 결과를 합리적으로
결합한다. 그러나 마지막 결론을 닫는 대형 수치 행렬 계산의 벡터·행렬·exact margin·실행 코드가
원고에 포함되지 않고 “추후 공개”로 남아 있어, 현재 제공 자료만으로 핵심 수치 단계를 독립
재현할 수 없다. 따라서 우리 연구에서는 검증된 정리로 채택하지 않고 아이디어·검증후보로만 둔다.

## 2. 논문이 주장하는 결과

논문의 \(H_1\)은 프로젝트의 “Sono/FMT H1 good-weight gate”와 전혀 다른 기호다. 여기서는

\[
H_1=\liminf_{n\to\infty}(p_{n+1}-p_n)
\]

을 뜻한다. 주 정리는

\[
H_1\le240
\]

이다. 즉 무한히 많은 연속 소수쌍의 간격이 240 이하라고 주장한다. 이는 우리 연구의
“아주 큰 소수 공백”과 반대로 “아주 작은 간격이 무한히 자주 존재함”을 다룬다.

논문은 직경 240의 admissible 49-tuple을 사용한다. 저자의 설명대로라면 이 tuple-count 단계에서
240은 246보다 작은 다음 가능한 직경이고, 사용한 다항식 차수는 21 이하로 이전 Polymath 계산의
27 이하보다 낮다.

## 3. 증명 구조

### 3.1 일반화된 GPY/Maynard sieve

Proposition 1은 적절한 prime minorant와 분포 정리를 가정하고, 다차원 test function의 적분에서
얻는 quotient가 1보다 크면 admissible tuple 안에 소수가 두 개 이상 생기는 경우가 무한히
많음을 준다.

### 3.2 prime minorant

Proposition 2는 Harman-type decomposition으로 소수 indicator 아래에 놓이는 minorant를 만든다.
parameter region을 Type I/II 성질과 연결해 평균 질량을 보존하려 한다.

### 3.3 smooth moduli에 대한 분포

Proposition 3은 modulus의 인수분해 구조와 partition 조건을 사용해 minorant에 필요한
equidistribution을 확보한다. 이 부분이 고전적인 Bombieri–Vinogradov 범위를 넘어서는 최신
입력이다.

### 3.4 최종 수치 최적화

Section 5는 test function을 유한 다항식 basis로 제한하고 적분을 행렬 quadratic form으로
바꾼다. 수치 eigenvector를 찾은 뒤 rational vector로 바꿔 quotient를 exact하게 확인한다는
전략이다. 마지막 페이지에서 \(k=49\),

```text
epsilon = 0.0075
A = (-epsilon, 0.253)
delta = 0.028
xi_1 = 0.38, xi_2 = xi_3 = 0.4
```

등을 선택하고 quotient가 1보다 크다고 결론 내린다.

## 4. 강점

1. 필요한 analytic input, minorant, distribution, finite-dimensional optimization의 역할이 구분돼 있다.
2. floating eigenvector를 그대로 증거로 쓰지 않고 rational vector와 exact integral로 옮기려는 방향은
   올바른 수치증명 관행이다.
3. 240이라는 개선폭이 작기 때문에 필요한 margin과 tuple diameter를 구체적으로 겨냥한다.
4. 주요 선행 결과와 무엇이 새 입력인지 비교적 명확히 설명한다.

## 5. 독립 채택을 막는 문제

### 5.1 핵심 수치 certificate가 원고에 없다

원고는 계산에 며칠과 큰 메모리가 들었다고 설명하고 full code를 추후 공개하겠다고 적는다.
그러나 현재 PDF에는 최종 rational coefficient vector, 두 행렬의 전체 entries, exact quotient 값과
1을 넘는 margin, 재현 명령, software/version/hash가 없다. 따라서 “계산 방법이 설명돼 있다”와
“계산 결과를 독립 검증할 수 있다”를 구분해야 한다.

### 5.2 analytic 압축에 대한 전문가 검토가 필요하다

minorant와 smooth-moduli 분포의 조건이 최종 parameter에 정확히 맞는지가 성패를 결정한다.
본문은 여러 긴 선행 논증을 압축해 사용하므로, proposition별 가정 누락·uniformity·경계조건을
전문가가 줄 단위로 다시 확인해야 한다.

### 5.3 편집 오류가 있다

- 첫 페이지 Theorem 1은 정의한 양이 \(H_1\)인데 결론에 \(H_m\le240\)이라고 인쇄돼 있다.
- 마지막 증명 도입부에는 “\(H_1\le246\)의 증명을 끝낸다”는 취지의 문장이 있으나 실제 목표와
  결론은 240이다.

문맥상 오탈자로 보이며 곧바로 정리의 반례는 아니다. 다만 출판 전 검토가 충분히 끝나지 않았을
가능성을 보여 주므로 미검증 표기를 강화한다.

### 5.4 심사 상태

확인된 것은 arXiv v1뿐이다. 저널 게재, 동료심사 통과, 독립 재현 성공은 확인되지 않았다.
arXiv DOI resolver `10.48550/arXiv.2608.31126`은 논문 식별자이지 동료심사를 뜻하지 않는다.

## 6. 우리 연구에서 사용할 수 있는 내용

### 직접 사용할 수 없음

- \(H_1\le240\)을 검증된 사실로 전제하는 것
- 미공개 수치 계산을 우리 certificate의 근거로 인용하는 것
- 작은 prime gap 결과를 FGKMT/Sono large-gap lower bound의 상수로 대입하는 것

### 검증후보·방법론으로 사용할 수 있음

1. high-dimensional integral을 exact rational matrix certificate로 바꾸는 설계
2. floating 탐색과 exact 최종 검증을 분리하는 방식
3. 복잡한 analytic theorem을 parameter obligation 표로 쪼개는 방식
4. 향후 코드가 공개되면 coefficient·matrix·tuple admissibility·quotient margin을 독립 재계산하는
   재현성 연구

### Sono/FMT threshold 축과의 관계

두 연구 모두 sieve weight와 prime distribution을 사용하지만 목적과 필요한 부등식이 다르다.
이 논문의 smooth-moduli 기술이 H1c의 Hypothesis 1/PAP를 자동으로 explicit하게 해 주지는 않는다.
원고 자체도 asymptotic 표기와 충분히 큰 parameter에 의존하므로, 우리 \(X_{\mathrm{cert}}\)에
필요한 numerical multiplier·cutoff 문제는 그대로 남는다.

## 7. 후속 검증 체크리스트

코드와 certificate가 공개됐을 때 다음 순서로만 판정을 올린다.

1. 공개 commit, license, dependency version과 파일 hash 고정
2. admissible 49-tuple과 diameter 240 exact 검사
3. rational vector와 행렬 entries가 논문 정의에서 생성됐는지 독립 재구성
4. 모든 적분·quadratic form을 exact rational 또는 outward interval로 재계산
5. quotient가 1을 넘는 exact lower margin 기록
6. Proposition 2–3의 parameter inequality를 별도 verifier로 확인
7. 가능하면 독립 구현과 수학 전문가 검토

## 8. 최종 판정

```text
논문 주장: H_1 <= 240
논증 구조: plausible and technically relevant
peer review: not confirmed
핵심 numerical certificate: manuscript alone is insufficient
독립 실행/검증: not performed
우리 연구의 theorem input: prohibited at present
우리 연구의 방법론 후보: retained
```

공식 원문 식별은 [arXiv:2608.31126](https://arxiv.org/abs/2608.31126)에서 확인했다.

