# Kourbatov-Wolf (2019) 분석

## 1. 서지정보

- Alexei Kourbatov, Marek Wolf
- “Predicting Maximal Gaps in Sets of Primes”
- *Mathematics* 7(5), 400, 2019
- DOI: [10.3390/math7050400](https://doi.org/10.3390/math7050400)
- 검토 파일: [PDF](<../../article/Predicting Maximal Gaps in Sets of Primes.pdf>)
- 분량: 28쪽
- SHA-256: `b3079f621e0073438ba99f6c7e2cb711df065dba13d297a6e09822de5f44eaba`

## 2. 연구 범위

다음 두 조건을 만족하는 primes의 부분수열 \(\mathcal P_c(q,r,\mathcal H)\)을 다룬다.

1. \(p\equiv r\pmod q\)
2. \(p\)가 주어진 pattern \(\mathcal H\)의 prime k-tuple 시작점

이 부분수열에서 consecutive elements 사이의 maximal gap growth, 분포, record count를 heuristic하게 예측하고 PARI/GP 계산으로 시험한다.

특수한 경우:

- \(k=1\): residue class 안의 primes
- \(k=1,q=2,r=1\): 모든 primes의 maximal gap
- \(k\ge2,q=2\): prime k-tuples 사이의 maximal gap

## 3. maximal-gap 경계 정의

모든 primes의 경우 논문은

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

로 정의한다(p. 1). 즉 gap endpoint가 \(x\) 이하인 end-bounded 정의다.

일반화된 \(G_c(p)\)도 gap이 끝나는 prime \(p\)를 기준으로 표현한다. 이번 프로젝트에서 Sono \(k=1\)과 직접 비교할 `G_end` 정의를 뒷받침하는 문헌이다.

## 4. heuristic 구성

### 4.1 부분수열의 평균 gap

Hardy-Littlewood/Bateman-Horn 계열의 equidistribution conjecture를 바탕으로 \(\pi_c(x)\)를 근사하고, 다음 두 평균 gap을 정의한다.

- \(a_c(x)=x/\pi_c(x)\)에 해당하는 below-\(x\) 평균
- \(\bar a_c(x)\)에 해당하는 local average near \(x\)

둘은 점근적으로 같지만 수렴이 매우 느리며, 이 차이가 finite-range trend에 중요하다고 본다.

### 4.2 k-tuple, \(k\ge2\)

exponential waiting time와 extreme value theory에서 lower/upper trend를 만든다.

\[
T_c(x)\approx a_c(x)\log\pi_c(x),
\qquad
\bar T_c(x)=\bar a_c(x)\log\frac{x}{\bar a_c(x)}.
\]

positive proportion의 maximal gaps가 두 trend 사이에 있고, 거의 모든 record가 generalized Cramér/Shanks 형태를 만족할 것이라고 conjecture한다.

### 4.3 primes, \(k=1\)

독립 EVT lower trend는 실제 값을 다소 과대예측한다. 저자들은 prime-gap count에 대한 exponential decay heuristic을 사용해

\[
G_{q,r}(x)\sim
\frac{\varphi(q)x}{\operatorname{li}x}
\left(
2\log\frac{\operatorname{li}x}{\varphi(q)}-\log x+b
\right)
\]

형태의 most-probable trend를 제안한다(Equation 33). \(b=O(\log q)\)이고 \(x\)가 커지면 상수로 가는 것으로 추정한다.

all-prime special case \((q,r)=(2,1)\)에서는 요약식이

\[
G(x)\sim\log^2x-2\log x\log\log x+O(\log x)
\]

가 된다(p. 22).

이것은 most-probable/heuristic trend이며 lower-bound theorem이 아니다.

## 5. record 수에 대한 conjecture

부분수열에서 \(x\) 이하 record gap 수 \(N_c(x)\)를 분석해

\[
N_c(x)\sim(k+1)\log x
\]

형태를 heuristic하게 유도한다. all-prime special case에서는 semi-empirical하게

\[
N_{2,1}(x)\sim2\log\operatorname{li}x
\]

를 제시한다. 보다 안전한 요약 conjecture는 어떤 \(C>k+1\)에 대해 \(N_c(x)<C\log x\)라는 것이다.

본 프로젝트에는 record index를 \(x\)의 균일 sample처럼 취급하면 안 된다는 근거가 된다.

## 6. 계산실험

### 6.1 범위

PARI/GP로 다음을 계산했다(§3, p. 12).

- \(q\in[4,10^5]\)의 여러 값
- 각 \(q\)의 admissible residue classes
- prime k-tuples, \(k\le6\)
- 최대 약 \(10^{14}\) 이하 primes

Figures 1-3은 \(q=313\)의 사례를 사용한다. \(k=1,2\)는 주로 \(x<10^{12}\), \(k=6\)은 \(x<10^{14}\) 범위를 보여준다.

### 6.2 growth trend

- \(k=1\): Equation 33의 red trend가 naive EVT blue trend보다 data를 더 잘 따른다.
- \(k=2\): record의 약 절반이 lower trend 아래/위에 분포한다.
- \(k\ge3\): 다수가 lower와 upper trend 사이에 있다.

### 6.3 분포

trend를 빼고 평균 gap scale로 나눈 rescaled record gap histogram이 Gumbel extreme-value distribution과 잘 맞는다고 보고한다(Figures 4-5).

- \(k=1\): fitted Gumbel scale이 관측범위에서 대략 0.7-1
- \(k\ge2\): rescaling에 따라 scale이 1 부근 또는 약간 위
- 제시된 histogram의 Kolmogorov-Smirnov statistic은 0.01 미만

저자들은 Gumbel이 실제 limiting distribution인지 명시적으로 open question으로 남긴다. 좋은 finite fit을 limit theorem으로 바꾸어 읽지 않는다.

### 6.4 재현성

Appendix A에 PARI/GP `maxgap.gp`와 보조함수, distribution fitting 절차를 싣는다. 데이터 생성의 구체성이 높은 장점이 있다. 다만 사용한 전체 output dataset과 모든 실행 metadata가 논문 PDF에 포함된 것은 아니다.

## 7. 본 프로젝트에 사용할 부분

### 직접 사용

- end-bounded `G_end` 정의
- all-prime \(\log^2x-2\log x\log\log x\) 보조 trend
- record count가 대략 logarithmic이라는 sampling 해석
- global trend를 제거한 residual distribution 분석 아이디어
- Gumbel fit을 exploratory analysis로 쓰되 limit claim과 분리하는 방식
- PARI/GP 코드가 있는 재현성 사례

### 사용하지 않을 부분

- residue-class 결과를 all-prime 결과로 자동 일반화하지 않는다.
- Gumbel fit을 FGMT/Sono lower bound의 근거로 쓰지 않는다.
- `H=1`을 이 논문의 직접 결론이라고 표현하지 않는다.
- most-probable trend를 모든 record에 대한 upper/lower theorem으로 쓰지 않는다.
- 계산범위 \(10^{14}\)를 exhaustive all-prime record coverage로 해석하지 않는다.

## 8. `H=1`과의 관계

논문이 all-prime gap에 제시한 scale은 FGMT scale이 아니라 \(\log^2x\)에 음의 보정항을 둔 식이다. 따라서 이 논문만으로

\[
H(x)=\frac{G(x)}{F(x)}\approx1
\]

을 도출할 수 없다. 본 프로젝트의 `H=1` 선은 별도 empirical reference이며, 추가 Wolf 1차 출처가 필요하다.

## 9. 제안 실험과의 중복 여부

| 항목 | 논문 수행 여부 |
|---|---|
| maximal-gap record 계산 | 예 |
| all-prime 및 residue-class trend | 예 |
| FGMT scale \(F(x)\) | 서론에서 theorem 언급만 |
| \(H=G/F\) | 아니오 |
| exact interval minimum | 아니오 |
| running minimum/lower envelope of \(H\) | 아니오 |
| Sono constant 비교 | 아니오 |
| Gumbel residual 분석 | 예 |

직접 중복은 아니다. proposed study의 Wolf/Cramér comparison layer와 boundary definition에 중요하다.

## 10. 한계와 주의점

- 주요 식은 heuristic/conjectural이다.
- 계산 중심이 residue class 및 k-tuple이라 all-prime record corpus와 다르다.
- finite-range Gumbel fit이 limiting distribution 존재를 보장하지 않는다.
- trend의 \(O(\log q)\), \(O(\log x)\) 항이 finite range에서 작지 않을 수 있다.
- record 수가 작고 residue class별 표본을 pooling하므로 독립성/동질성 가정에 주의해야 한다.
- 저자들의 `G(x)`는 endpoint 기준이므로 FGMT start 기준 결과와 직접 수치 비교 전 변환이 필요하다.

## 11. 확인한 핵심 위치

- Abstract와 all-prime `G(x)` 정의: p. 1
- FGMT 및 Wolf trend 배경: p. 2
- 평균 gap과 EVT trend: pp. 6-8
- prime case Equation 33: pp. 8-10
- record-count conjecture: pp. 10-12
- 계산범위와 growth figures: pp. 12-14
- Gumbel fits: pp. 15-16
- exceptional gaps와 record occurrence: pp. 19-21
- Summary와 all-prime trend: p. 22
- PARI/GP code: pp. 23-24

## 12. 최종 판정

본 연구의 Wolf 계열 비교와 end-bounded 정의에 가장 직접적인 논문이다. 그러나 FGMT normalization, Sono 상수, interval-wise lower envelope를 다루지 않으므로 제안 실험과 중복되지 않는다.
