# Banks-Ford-Tao (2023) 분석

## 1. 서지정보

- William Banks, Kevin Ford, Terence Tao
- “Large Prime Gaps and Probabilistic Models”
- *Inventiones Mathematicae* 233, 1471-1518, 2023
- DOI: [10.1007/s00222-023-01199-0](https://doi.org/10.1007/s00222-023-01199-0)
- 검토 파일: [PDF](<../../article/Large prime gaps and probabilistic models.pdf>)
- 분량: 48쪽
- SHA-256: `c0d261432e263d07431c4b129616868c65e3e406fff043ea47135402321b8498`

## 2. 연구 목적

Cramér model은 각 정수를 독립 확률로 선택해 prime number theorem의 평균밀도는 흉내 내지만, modular obstruction과 Hardy-Littlewood singular series를 재현하지 못한다. Granville model은 작은 소수의 residue-class bias를 부분 반영하지만 분석에 한계가 있다.

이 논문은 작은 소수별 random residue class를 제거한 뒤 살아남는 정수로 새 random set \(\mathcal R\)을 구성한다. 목표는 다음과 같다.

1. sieve가 만드는 local correlation을 포함하는 prime model 제시
2. model의 largest gap을 interval sieve extremal problem과 연결
3. model에 대해 uniform Hardy-Littlewood analogue와 prime-counting 오차를 엄밀히 증명
4. Hardy-Littlewood형 가정에서 large gap을 도출하는 일반 정리 제시

## 3. maximal-gap 정의

임의의 집합 \(\mathcal A\subset\mathbb N\)에 대해

\[
G_{\mathcal A}(x)
=\max\{b-a:[a,b]\subset[1,x],\ [a,b]\cap\mathcal A=\varnothing\}
\]

를 사용한다. 이는 record start/end table의 계단함수라기보다 \([1,x]\) 안의 largest empty interval 정의다.

본 프로젝트의 `G_start`, `G_end`와 점근적으로 같은 scale을 논할 수 있지만, 유한 record interval을 exact하게 복원할 때는 정의를 직접 치환하지 않는다.

## 4. 기존 model 평가

### 4.1 Cramér model

각 \(n\ge3\)을 확률 \(1/\log n\)로 독립 선택한다. 거의 확실하게 largest gap이

\[
G_{\mathcal C}(x)\sim\log^2x
\]

가 되지만 prime k-tuple의 singular-series bias를 놓친다.

### 4.2 Granville model

작은 소수로 먼저 체질한 뒤 남은 정수를 보정확률로 선택해 local density를 반영한다. 논문은

\[
G_{\mathcal G}(x)\ge(\xi-o(1))\log^2x,
\qquad \xi=2e^{-\gamma}=1.1229\ldots
\]

형태의 차이를 설명한다.

이 비교는 “독립 exponential spacing만으로 maximal gap tail을 해석하면 산술적 구조를 놓친다”는 경고다.

## 5. 새 random model

각 정수 \(n\)마다 cutoff \(z(n)\)까지의 소수 \(p\)에 대해 무작위 residue class \(a_p\pmod p\)를 제거하고 살아남은 정수를 \(\mathcal R\)에 포함한다. cutoff가 \(n\)에 따라 증가하므로 event 사이에 복잡한 coupling이 생기지만, 바로 그 구조가 primes의 local correlation을 모사한다(§1.3).

## 6. 핵심 정리와 conjecture

### 6.1 interval sieve 함수

\(W_y\)를 작은 소수 residue class로 interval \([0,y]\)를 얼마나 남길 수 있는지 나타내는 extremal quantity로 두고,

\[
g(u)=\max\{y:W_y\log y\le u\}
\]

를 정의한다. 알려진 sieve bounds로 대략

\[
(1+o(1))u\le g(u)
\le(1+o(1))\frac{u\log u}{4\log_2u}
\]

범위를 얻는다.

### 6.2 random model의 largest gap(Theorem 1.1)

모든 \(\varepsilon>0\)에 대해 거의 확실하게 충분히 큰 \(x\)에서

\[
g((\xi-\varepsilon)\log^2x)
\le G_{\mathcal R}(x)
\le g((\xi+\varepsilon)\log^2x)
\]

를 증명한다. 모델 분석 자체는 엄밀하지만 실제 primes에 바로 적용되는 정리는 아니다.

### 6.3 primes에 대한 conjecture(Conjecture 1.2)

\[
G_{\mathcal P}(x)\sim g(\xi\log^2x)
\]

를 제안한다. folklore conjecture \(g(u)\sim u\)까지 가정하면

\[
G_{\mathcal P}(x)\sim\xi\log^2x
\]

가 된다. 이는 경험적/확률모형 예측이며 FGMT lower bound와 논리적 지위가 다르다.

### 6.4 uniform Hardy-Littlewood(Theorems 1.3-1.4)

model \(\mathcal R\)이 넓은 범위의 admissible tuple에 대해 uniform Hardy-Littlewood analogue를 만족함을 보이고, 단일 tuple에서는 Riemann-hypothesis형 counting error도 얻는다. 이는 새 model이 Cramér보다 산술적 구조를 더 잘 담는다는 핵심 근거다.

### 6.5 Hardy-Littlewood에서 large gaps(Theorems 1.5-1.6)

일반 집합 \(\mathcal A\)가 충분히 uniform한 Hardy-Littlewood-type conjecture를 만족하면 large gap lower bound를 얻는 deterministic converse를 제시한다. 더 강한 averaged uniformity에서는 interval-sieve 함수 \(g\)가 직접 나타난다.

본 프로젝트에는 “관측된 large gap과 probabilistic model의 일치”를 정리의 무조건부 보장과 혼동하지 않게 해주는 이론적 틀이다.

## 7. 논문에 포함된 실제 prime-gap 수치

Figure 1(p. 1473)은 실제 prime maximal gap 계단함수를 다음과 비교한다.

- \(\log^2x\)
- \((\log x)(\log x-\log_2x)\)
- \(2e^{-\gamma}\log^2x\)

공개 prime-gap table을 이용해

\[
\sup_{x\le10^{18}}\frac{G_{\mathcal P}(x)}{\log^2x}\approx0.9206
\]

이라고 보고하며, gap 1132가 시작 소수 1693182318746371 뒤에 나타나는 사례를 언급한다.

이 수치 도표는 논문의 새 exhaustive computation이 아니다. 공개 table을 probabilistic model의 배경 evidence로 재사용한 것이다.

## 8. 본 프로젝트에 사용할 부분

### 채택

- \(\xi\log^2x\) 및 interval-sieve-aware probabilistic benchmark
- Cramér model의 singular-series 결손에 대한 해석
- empirical, model-a.s., conditional theorem, prime conjecture의 네 층 분리
- actual record plot에 여러 theoretical curve를 parameter fitting 없이 겹치는 방식
- \(H(x)\)의 장기 trend가 단순 상수 수렴일 필요가 없다는 이론적 배경

### 채택하지 않음

- \(\mathcal R\)의 gap law를 actual prime gap에 대한 증명으로 쓰지 않는다.
- \(g(u)\sim u\)를 확정 사실로 쓰지 않는다.
- Figure 1의 source table을 최신 데이터 정본으로 사용하지 않는다.
- \(\xi\log^2x\)를 FGMT/Sono lower bound와 같은 종류의 식으로 설명하지 않는다.

## 9. 제안 실험과의 중복 여부

| 항목 | 논문 수행 여부 |
|---|---|
| 실제 maximal-gap curve | 배경 도표로 부분 수행 |
| FGMT scale \(F(x)\) | 서론에서 known lower bound로만 제시 |
| \(H=G/F\) | 아니오 |
| record interval minimum | 아니오 |
| running minimum/lower envelope of \(H\) | 아니오 |
| Sono constant 비교 | 아니오 |
| Cramér/Granville 보정 | 핵심 수행 |

직접 중복은 아니다. 제안 실험 결과의 heuristic interpretation layer와 가장 관련이 깊다.

## 10. 한계와 주의점

- primes에 대한 핵심 asymptotic은 Conjecture 1.2다.
- \(g(u)\)의 정확한 asymptotic 자체가 미해결이다.
- 모델의 almost-sure theorem은 actual primes의 theorem이 아니다.
- Figure 1은 제한된 공개 record 자료의 시각 비교다.
- 논문의 `largest empty interval`과 데이터셋의 start/end-bounded record 함수는 유한 \(x\)에서 경계가 다를 수 있다.

## 11. 확인한 핵심 위치

- Abstract 및 모델 정의: pp. 1471-1472
- 실제 gap Figure 1과 Cramér model 비판: p. 1473
- Granville model: p. 1474
- 새 model: p. 1475
- Theorem 1.1, Conjecture 1.2: p. 1476
- Theorems 1.3-1.4: p. 1477
- Theorems 1.5-1.6: p. 1478
- 비교표와 open problems: p. 1479

## 12. 최종 판정

이 논문은 FGMT-normalized empirical envelope가 아니라 sieve-aware probabilistic model의 엄밀한 분석이다. 제안 연구와 직접 중복되지 않으며, observed \(H\)가 왜 Cramér형 scale과 복잡한 관계를 가질 수 있는지를 설명하는 핵심 이론 문헌이다.
