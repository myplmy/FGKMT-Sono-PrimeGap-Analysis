# Feliksiak (2021 preprint) 비판적 분석

## 1. 서지정보와 심사 상태

- Jan Feliksiak
- PDF 본문 제목: “Maximal Prime Gaps Bounds”
- ScienceOpen Preprints DOI: [10.14293/S2199-1006.1.SOR-.PPWVKRR.v1](https://doi.org/10.14293/S2199-1006.1.SOR-.PPWVKRR.v1)
- first posted online: 2021-02-09
- PDF 첫 페이지 명시: preprint, not peer-reviewed
- 본문 copyright 표기: 2018
- 검토 파일: [PDF](<../../article/Maximal Gaps Lower bound Revised.pdf>)
- 분량: 27쪽
- SHA-256: d5e843fdcea5cfd041fa3c22c973c4d1a9cf6a52cb1724837ad954fb438f8ce8

출판연도 표기가 PDF 내부에서 2018과 2021로 나뉘므로, 본 프로젝트에서는 공개 preprint version의 first-posted year인 2021로 식별한다.

## 2. 논문의 주장

논문은 maximal prime gap에 대해 네 종류의 식을 제안한다.

1. 단순 upper bound
2. Riemann sum 기반 “infimum”
3. Riemann sum 기반 “supremum”
4. 별도의 lower-bound 함수 \(LB(p_n)\)

그 뒤 FGKMT scale

\[
PB(x)=
\frac{\log x\,\log_2x\,\log_4x}{\log_3x}
\]

와 자신이 제안한 \(LB\)의 ratio를 계산해, \(LB/PB\)가 32보다 크고 무한히 발산하므로 FGKMT의 implicit constant도 그렇게 추정할 수 있다고 주장한다(pp. 13-15).

표는 start prime \(p_n\), actual record gap, 제안 bound를 78개 record와 약 \(1.836\times10^{19}\)까지 제시한다.

## 3. 제안한 함수

### 3.1 upper bound

\[
g\le5(\log_{10}p_n)^2
\]

를 모든 \(p_n\ge11\)에 대한 theorem으로 인용하지만, 증명은 저자의 별도 문헌으로 넘긴다. 이 정도의 all-prime gap upper bound는 Cramér형 문제와 직접 관련된 매우 강한 주장이다.

### 3.2 infimum과 supremum

maximal record interval마다 250,000 subdivisions per integer를 둔 Riemann sum과 자료에 맞춘 decimal parameter를 사용한다. 알려진 78개 record에서 actual gap 바로 아래·위에 매우 근접하도록 parameter가 설정되어 있다.

### 3.3 lower bound

Theorem 3.4는

\[
LB(p_n)=
\mathcal M\left(
5(\log_{10}p_n)^\alpha
-7(\log_{10}p_n)^{2\gamma}
\right)+\beta
\]

형태를 모든 \(p_n\ge23\)의 maximal gap lower bound라고 주장한다. 여기서 \(\alpha,\beta,\mathcal M\)은 고정된 경험식이다.

## 4. FGKMT scale 비교

이 논문은 현재 corpus에서 제안 실험과 가장 가까운 비교를 시도한다. Figure 7과 Tables 4-5에서

- 제안 \(LB\)
- FGKMT 함수형 scale \(PB\)
- \(LB-PB\)
- \(LB/PB\)

를 record 위치에서 비교한다. 약 \(1.958\times10^{13}\)의 end prime에서 \(LB/PB\approx32.34035\)라는 global minimum을 보고하고, 이후 증가한다고 주장한다.

그러나 이것은 실제

\[
H(x)=\frac{G(x)}{F(x)}
\]

의 exact record-interval minimum이 아니다. 분자는 관측 \(G\)가 아니라 저자가 별도로 fitting한 \(LB\)이며, record 사이의 right endpoint도 평가하지 않는다. Sono \(2.0\times10^{-17}\)과도 비교하지 않는다.

## 5. 증명의 핵심 문제

이 문서의 theorem과 corollary를 본 프로젝트의 수학적 근거로 채택할 수 없다. 구체적인 이유는 다음과 같다.

### 5.1 finite record 관찰을 무한 범위로 확장

알려진 record에서 어떤 ratio가 증가했다는 계산은 미래의 모든 record에서도 단조증가한다는 증명이 아니다. 논문은 “strictly increases at every step”과 “diverges”를 유한 표·그래프에서 무한 범위로 확장한다.

### 5.2 Cauchy root test의 적용 대상 문제

root test는 일반적으로 급수 \(\sum a_j\)의 절대수렴·발산을 판정한다. 유한한 j에서 \(\sqrt[j]{|a_j|}>1\)인 관찰이나 어떤 sequence의 root 값이 1에 접근한다는 사실만으로, 제안한 gap inequality의 부호·모든 미래 record·lower-bound 성립을 결론낼 수 없다.

### 5.3 Westzynthius 결과로부터 fitted formula가 나오지 않음

\[
\limsup\frac{G(x)}{\log x}=\infty
\]

라는 고전 결과는 maximal gaps가 평균 gap보다 임의로 크게 될 수 있음을 말한다. 이 사실만으로 특정 decimal parameter를 가진 Riemann-sum 함수가 모든 maximal record의 infimum 또는 supremum이라는 결론은 나오지 않는다.

### 5.4 강한 upper bound에 대한 독립적 근거 부족

\(5(\log_{10}p)^2\) all-prime upper bound는 이 PDF 안에서 증명하지 않고 저자의 다른 비심사 preprint에 의존한다. 하위 theorem들이 이를 전제로 사용하므로 독립적인 논증이 아니다.

### 5.5 observed ratio와 theorem constant의 혼동

FGKMT의 \(\gg\) constant는 충분히 큰 모든 \(X\)에 대해 uniform하게 성립해야 하는 증명 상수다. 알려진 record에 fitting한 \(LB/F\) ratio가 크다고 해서 그 값을 FGKMT 증명의 implicit constant로 식별할 수 없다. 특히 unknown threshold와 start/end 경계도 처리되지 않는다.

## 6. 데이터와 재현성

장점은 78개 maximal record의 start prime, gap, end prime 및 여러 함수값을 표로 제공한다는 점이다. 하지만 데이터 provenance·취득일·checksum·exhaustive coverage·parser가 제안 연구의 기준만큼 기록되어 있지 않다.

또한 parameter가 알려진 record에 맞춰져 있어, 같은 record 표에서 작은 estimation error를 보이는 것은 독립적인 out-of-sample 검증이 아니다. 300,000 decimal precision과 Mathematica를 언급하지만 실행 코드와 원시 계산 artefact를 제공하지 않는다.

따라서 이 표는 authoritative dataset 대신 사용할 수 없고, 승인 후 검증 데이터와의 spot-check 대상으로만 취급한다.

## 7. novelty와 중복성에 미치는 영향

이 preprint의 존재 때문에 “기존 문헌에는 FGKMT 함수와 실제 maximal-gap record를 비교한 시도가 전혀 없다”라고 단정하면 안 된다. 더 정확한 판정은 다음과 같다.

- FGKMT scale과 record-derived 함수를 수치 비교한 선행 시도는 있다.
- 그러나 분자가 실제 step function \(G(x)\)가 아닌 fitted \(LB\)다.
- exact interval minimum, start/end audit, running/local envelope, Sono ratio가 없다.
- proof와 extrapolation에 중대한 논리적 문제가 있다.
- 데이터·코드 재현성이 부족하다.

따라서 제안 연구의 차별점은 단순히 “최초 비교”가 아니라, 검증된 원자료와 명시적 경계 정의를 사용해 실제 \(G/F\)의 exact finite envelope를 재현 가능하게 계산하고 Sono 상수와 분리해 해석하는 데 있다.

## 8. 본 프로젝트의 처리 규칙

### 참고 가능

- prior-overlap report의 가장 가까운 선행 시도
- 알려진 record table의 비정본 spot-check
- observed empirical ratio와 theorem constant를 혼동하면 안 된다는 반례적 사례
- interval-wise minimum이 왜 필요한지 설명하는 비교대상

### 채택 금지

- 논문의 upper/lower/infimum/supremum을 theorem으로 인용하지 않는다.
- \(C\ge32\) 또는 divergence 주장을 FGKMT/Sono 결과로 사용하지 않는다.
- table을 최신·완전·exhaustive dataset으로 사용하지 않는다.
- 이 preprint의 finite figures로 본 프로젝트의 예상 결론을 정하지 않는다.

## 9. 제안 실험과의 비교

| 항목 | preprint | 제안 실험 |
|---|---|---|
| 분자 | fitted \(LB\) | 실제 validated \(G_b(x)\) |
| 경계 | start/end 혼재 가능 | start와 end 분리 |
| interval worst case | 없음 | 정확히 \(a_{i+1}-1\) 평가 |
| running/local envelope | 없음 | 둘 다 분리 산출 |
| Sono explicit constant | 없음 | \(Q=H/(2.0\times10^{-17})\) |
| 데이터 provenance | 제한적 | URL, hash, coverage, schema |
| 재현 코드 | 없음 | versioned source와 tests |
| 수학적 지위 | 비심사·논증 문제 | empirical 계산으로 한정 |

## 10. 확인한 핵심 위치

- preprint 상태와 metadata: p. 1
- 주장의 요약: p. 2
- upper bound와 Riemann-sum 방법: pp. 3-11
- 제안 lower bound: pp. 11-13
- FGKMT scale 비교와 \(C\ge32\) 주장: pp. 13-15
- record 및 함수값 표: pp. 18-27

## 11. 최종 판정

FGKMT scale과 maximal-record 자료의 수치 비교를 시도했다는 점에서 중복성 검토에 반드시 포함해야 한다. 그러나 비심사 preprint이고, finite fitting을 무한 theorem으로 확장하며 root test를 gap inequality 증명에 사용하는 등 핵심 논증이 충분하지 않다. 본 프로젝트의 이론 근거나 데이터 정본으로 사용하지 않고, 가장 가까운 선행 시도이자 방법론적 경고 사례로만 기록한다.
