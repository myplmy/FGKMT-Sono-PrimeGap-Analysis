# P018 expected-information gate 후보와 문헌 근거 검토

최종 갱신: 2026-08-30 KST

## 1. 먼저 알아둘 핵심

P018 gate는 “가설이 참/거짓”을 판정하는 통계검정 자체가 아니다. 수십 시간 계산을 더 하기 전에
그 계산이 구별력을 가질 가능성이 있는지 거르는 **착수 신호등**이다.

- PASS: 다음 범위 계산을 해볼 정보 근거가 생김
- HOLD: 가설이 틀렸다는 뜻이 아니라, 현재 설계로는 계산비용에 비해 정보가 너무 적음

P013-B는 33,489,857,205개 gap start를 처리했지만 primary expected recurrence가
`0.0667972`, 양의 분산 row가 `1/9`, LOW_INFORMATION이 `9/9`였다. null 아래 한 번 이상 사건이
나올 Poisson planning 확률도 약 6.46%다. 이 상태에서 0회 관측은 특별히 놀라운 결과가 아니다.

## 2. 각 gate 값의 일상어 뜻과 방향

| 값 | 뜻 | 값을 높이면 | 값을 낮추면 |
|---|---|---|---|
| `alpha` | 효과가 없는데 있다고 잘못 말할 허용확률 | 다음 단계 진입이 쉬워지지만 false positive 위험 증가 | 더 신중하지만 더 많은 정보 필요 |
| recurrence event probability target | null에서도 적어도 한 번 사건을 볼 사전 확률 | 빈 표를 받을 위험 감소, 계산 요구량 증가 | 빠른 탐색 가능, 0회 결과가 흔해짐 |
| positive-variance rows 최소수 | 실제로 비교 가능한 서로 다른 plateau row 수 | 한 row 우연에 덜 좌우됨, 진입 어려움 | 적은 구조로도 진행하지만 불안정 |
| LOW_INFORMATION 최대비율 | 정보 부족 row를 얼마나 허용할지 | 허용치를 높일수록 쉽게 통과하지만 빈약한 family가 됨 | 더 안정적이나 현재처럼 희소할 때 자주 HOLD |
| effect multiplier | 검출하려는 증가 크기, 예: `2x`는 기대의 두 배 | 큰 값은 power를 얻기 쉽지만 큰 효과만 잡음 | 작은 효과까지 보려 하지만 훨씬 많은 데이터 필요 |
| power target | 가정한 효과가 있을 때 검출할 확률 | 놓칠 위험 감소, 요구 정보 급증 | 계산 착수는 쉬우나 진짜 효과를 놓칠 가능성 증가 |

effect multiplier는 방향이 특히 헷갈린다. `5x`를 쓰면 “효과가 아주 클 것”이라고 가정하므로
검정력은 쉽게 높아진다. 대신 실제 효과가 `2x`일 때 찾을 능력을 보장하지 않는다.

## 3. 외부 문헌에서 가져올 수 있는 것과 없는 것

### 가져올 수 있는 일반 원칙

- Cohen의 power 입문 논문은 여러 표준 검정에서 `.80` power 표를 제시했다. 따라서 0.8은 널리
  쓰이는 계획 관례지만 수론에서 증명된 최적값은 아니다.
  DOI: https://doi.org/10.1037/0033-2909.112.1.155
- Holm의 multiple-testing 논문은 family-wise type-I error를 보호하는 순차 Bonferroni 절차를
  제시한다. P013의 두 planned stage에 총 0.05를 단순 분할한 `0.025`는 이 계열의 보수적 원칙과
  맞지만, prime-gap 논문에서 가져온 수치는 아니다.
  DOI: https://doi.org/10.2307/4615733
- ASA statement는 `p<0.05` 같은 한 개의 문턱만으로 과학 결론을 내리는 것을 경고한다. P018이
  alpha뿐 아니라 정보량·분산 row·LOW_INFORMATION·power를 함께 보는 이유다.
  DOI: https://doi.org/10.1080/00031305.2016.1154108

### prime-gap 문헌에서 확인되는 것

- Gallagher의 short-interval Poisson 관점과 Goldston–Ledoan의 지정된 consecutive gap count
  점근식은 count-only Poisson screen의 이론적 배경을 준다. 그러나 P018과 같은 finite
  maximal-record recurrence gate 값은 주지 않는다.
  DOI: https://doi.org/10.1112/S0025579300016442,
  arXiv: https://arxiv.org/abs/1111.3380
- Wolf/Goldston–Ledoan의 exact-gap·jumping-champion 연구는 gap frequency가 단순 동일확률이
  아니며 arithmetic structure를 반영한다는 근거다.
  arXiv: https://arxiv.org/abs/0910.2960
- Lemke Oliver–Soundararajan은 consecutive primes의 residue pattern에 예상 밖 bias가 있음을
  수치와 conjectural formula로 보였다. 독립·동일확률 가정을 그대로 쓰지 말아야 한다.
  DOI: https://doi.org/10.1073/pnas.1605366113

확인한 관련 문헌에서는 `positive-variance rows=3`, `LOW_INFORMATION<=0.5`, `2x effect`,
`event probability=0.5`를 한 묶음으로 사용한 선례를 찾지 못했다. 이 네 값은 우리 자료와 비용에
맞춰 사전 등록해야 하는 프로젝트 고유 planning gate다. 이는 전 세계 문헌 전수조사에 따른
부재 증명이 아니라 현재 corpus와 위 primary 자료에 대한 판정이다.

## 4. 세 후보

| 후보 | alpha | event 확률·목표 lambda | 양의 분산 row | LOW 최대 | 가정 효과 | power | 용도 |
|---|---:|---:|---:|---:|---:|---:|---|
| A 탐색형 | 0.05 | 25% · 0.287682 | 2 | 0.75 | 5x | 0.60 | 값싼 prefix·정보량 probe만 |
| B 균형형 **권장** | 0.025 | 50% · 0.693147 | 3 | 0.50 | 2x | 0.80 | full future range 착수 |
| C 확인형 | 0.0125 | 80% · 1.609438 | 5 | 0.25 | 1.5x | 0.90 | 후속 확인 연구 |

현재 P013-B에 적용하면 세 후보 모두 HOLD다.

| 후보 | event 정보량 배수 | power에 필요한 null 기대값 | power 정보량 배수 | 현재 proxy power |
|---|---:|---:|---:|---:|
| A | 4.3068x | 0.621076 | 9.2979x | 0.044781 |
| B | 10.3769x | 11.269070 | 168.7057x | 0.008167 |
| C | 24.0944x | 60.388860 | 904.0629x | 0.004697 |

여기서 “정보량 배수”는 expected recurrence가 선형으로 늘어난다는 가정의 계획 수치일 뿐이다.
실제 P013-A에서 B로 gap start는 약 9.14배 늘었지만 expected recurrence는
`0.0778288 -> 0.0667972`로 오히려 약 14% 줄었다. plateau·record-gap 구성과 빈도가 바뀌기
때문이다. 따라서 `168.7x`를 CPU 시간에 곧바로 곱하면 안 되며, 오히려 full sweep 전에 값싼
prefix로 미래 정보율을 추정해야 한다는 신호다.

## 5. 권장안

full scientific range를 자동 권고하는 정본 후보는 B를 유지하는 것이 좋다.

1. P013의 이미 동결된 두-stage family-wise 설계와 alpha 0.025가 맞는다.
2. 2x는 5x보다 작은, 연구적으로 의미 있는 enrichment까지 보겠다는 명확한 목표다.
3. power 0.8은 일반 planning 관례이고, 계산비가 큰 이 프로젝트에서는 낮춰서 불확실한 full
   sweep을 허용할 유인이 작다.
4. row 3개·LOW 50%는 한 row나 대부분 무정보인 family를 막는 최소한의 구조 gate다.

다만 B는 현재 자료에서 매우 높은 문턱이다. 이것은 결함이라기보다 “같은 exact-gap recurrence
설계로 decade만 계속 늘리지 말라”는 결과다. A는 정본을 대체하지 않고, 몇 분~수십 분짜리
prefix information probe의 착수 gate로만 병행할 수 있다. C는 현재 PC와 관측 희소성에서는
실용적이지 않아 보류한다.

## 6. 구현 보완

`source/recurrence_information_preflight.py`에 discrete Poisson critical count를 그대로 유지하며
지정 alpha·effect·power를 만족하는 최소 null expectation을 계산하는 함수를 추가했다. B의
재현값은 다음과 같다.

```text
minimum null expected recurrences = 11.269069541418046
critical count = 19
2x alternative power = 0.8
P013-B 대비 planning multiplier = 168.7057465x
```

이 값도 formal stratified-hypergeometric power가 아니다. formal P018-B를 하려면 future plateau
구성 규칙과 stopping rule을 결과 보기 전에 먼저 동결해야 한다.

## 7. 100,000회 simulation과 power는 다른 값

P012/P013의 100,000회 Monte Carlo 반복은 이미 가진 자료에서 family p-value의 simulation 잡음을
줄이는 설정이다. p가 0.025 부근이면 단순 이항 근사 Monte Carlo 표준오차는 약 `0.000494`, 95%
폭은 대략 `±0.00097`이다. 반복을 백만 회로 늘리면 이 잡음은 줄지만, recurrence 0.0668개라는
실제 정보량이나 positive-variance row 수는 늘지 않는다. 따라서 simulation 반복 수를 올리는
것은 P018 power gate를 통과하는 해결책이 아니다.
