# Kourbatov-Wolf (2020) First Occurrences 분석

## 1. 서지정보

- Alexei Kourbatov, Marek Wolf
- “On the First Occurrences of Gaps Between Primes in a Residue Class”
- *Journal of Integer Sequences* 23, Article 20.9.3, 2020
- 검토 파일: [PDF](<../../article/On the First Occurrences of Gaps Between Primes in a Residue Class.pdf>)
- 분량: 24쪽
- SHA-256: 559caae5a1a9a72672f0eb3154af091e2b72ea0024bd215367049d7c700fdf2b

## 2. 연구 대상

서로소인 \(q>r\ge1\)에 대해 산술진행

\[
(P)_{q,r}: r,r+q,r+2q,\ldots
\]

안의 연속한 두 소수 사이 gap을 다룬다. 주 대상은 특정 크기 \(d\)가 처음 나타나는 first-occurrence gap이며, maximal record gap은 그 부분수열이다.

이번 프로젝트의 all-prime maximal-gap record와 동일한 데이터는 아니지만, \(q=2,r=1\)이 전체 소수의 특수 경우이고, end-bounded maximal-gap 정의·\(\log^2x\) trend·Gumbel 모델을 명시적으로 제공한다.

## 3. maximal-gap 정의와 로그

논문은

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

로 정의한다(p. 2). 따라서 끝 소수가 \(x\) 이하인 end-bounded 정의이며 이번 프로젝트의 \(G_{\mathrm{end}}\)와 맞는다.

p. 3의 notation은 \(\log x\)가 자연로그임을 명시한다. 논문은 FGKMT lower-bound scale을 서론에 쓰면서 “computations suggest” 계수 \(A=1\)이 정의 가능한 계산 범위에서 성립한다고 서술한다(p. 2). 이는 \(H=1\)을 Wolf-related empirical reference로 둘 수 있는 현재 corpus의 직접적인 2차 진술이지만 다음 한계가 있다.

- 증명된 constant가 아니다.
- 해당 문장이 이 논문의 새 계산 산출물은 아니며 참고문헌 [10]을 가리킨다.
- exact record-interval minimum이나 데이터 provenance가 그 문장과 함께 제시되지 않는다.
- Sono의 explicit constant와 같은 논리적 지위를 갖지 않는다.

따라서 \(H=1\)은 “Kourbatov-Wolf 2020이 보고한 계산적 참고선”으로는 인용할 수 있지만 theorem 또는 \(H\)의 극한으로 부르면 안 된다.

## 4. 세 trend 함수

평균 gap 추정량은

\[
a(q,x)=\frac{x\varphi(q)}{\operatorname{li}x}
\]

이다. 이를 바탕으로 다음 함수를 구분한다.

### 4.1 baseline \(T_0\)

\[
T_0(q,x)=a(q,x)\log\frac{\operatorname{li}x}{a(q,x)}
\]

로 정의하며 점근적으로 \(\varphi(q)\log^2x\)보다 약간 작다. 수치 자료에서는 maximal gap의 다수가 이 선 위에 있고, non-maximal first occurrence의 상당 부분은 아래에 있다.

### 4.2 maximal-gap trend \(T_m\)

\[
T_m(q,x)=T_0(q,x)+E_m(q,x)
\]

이며 \(E_m\)은 양의 경험적 보정이다. parameter는 자료에 맞춰 추정하므로 엄밀한 예측식이 아니다.

### 4.3 first-occurrence trend \(T_f\)

\[
T_f(q,x)=T_0(q,x)+E_f(q,x)
\]

이며 충분히 큰 \(x\)에서 \(E_f\)는 음의 경험적 보정이다. \(q\)가 prime 또는 특정 semiprime인 경우의 parameter식을 수치적으로 제안한다(pp. 5-7).

## 5. 계산 범위와 분포 결과

PARI/GP로 \(2\le q\le10^5\)의 여러 progression을 계산했다. 대표 결과는 다음과 같다.

- \(q=211\), \(r=1,\ldots,210\), end prime \(10^7\)에서 \(10^{12}\): trend와 rescaled histogram
- \(q=17011\), \(x=e^j\), \(j\le27\): first occurrence 및 record count
- 많은 trend 검사는 \(x\le10^{14}\) 범위

rescaling

\[
u=\frac{d_{q,r}(x)-T_f(q,x)}{a(q,x)}
\]

후 first-occurrence gap의 histogram은 오른쪽 꼬리가 긴 Gumbel extreme-value 분포에 잘 맞는다. best-fit GEV의 shape는 대체로 \([-0.04,0]\)이고, Gumbel limit의 실제 존재 여부는 열린 문제로 남긴다(pp. 8-10).

## 6. first occurrence 위치와 개수

gap \(d\)의 첫 시작 소수를 \(P_f(d;q,r)\)라 할 때

\[
P_f(d;q,r)\asymp
\sqrt d\,\exp\left(\sqrt{\frac d{\varphi(q)}}\right)
\]

형태가 무한히 자주 나타날 것으로 추측한다. generalized Brun constant의 heuristic으로도 같은 규모를 유도한다(pp. 11-15).

개수에 대해서는

\[
N'_{q,r}(x)=O(\log^2x)
\]

인 first occurrence가 maximal record보다 훨씬 많고,

\[
N_{q,r}(x)\sim2\log x
\]

를 conjecture한다. \(e\)-배 구간당 평균 maximal record 수가 2로 접근한다는 수치 fitting이 근거다(pp. 15-17).

## 7. record index 관점

n번째 first occurrence 크기는 대략 선형,

\[
S(n;q,r)\approx n\,\operatorname{lcm}(2,q),
\]

n번째 maximal record는 대략 이차,

\[
R(n;q,r)\approx\frac{\varphi(q)n^2}{4},
\]

로 추측한다. 이는 record 수가 \(O(\log x)\)라는 관점과 일관된다(p. 17).

## 8. 본 프로젝트와의 관계

### 직접 활용

- end-bounded \(G(x)\) 정의
- \(H=1\)의 Wolf-related empirical 참고 문구
- \(\log^2x\) trend와 local extreme-value 비교축
- maximal record와 first occurrence를 혼동하지 않아야 한다는 경고
- record count와 end-point convention

### 직접 사용할 수 없음

- 산술진행 여러 residue class의 합산 결과를 all-prime record에 그대로 대입하지 않는다.
- Gumbel fit을 FGKMT/Sono lower-bound 정리로 해석하지 않는다.
- \(A=1\) 진술을 증명된 lower-bound constant로 쓰지 않는다.
- paper의 summary 값만으로 raw record provenance나 exhaustive coverage를 대체하지 않는다.

## 9. 제안 실험과의 중복 여부

| 항목 | 논문 수행 여부 |
|---|---|
| 실제 gap 계산 | 예; 주로 residue classes |
| all-prime maximal record | 배경 및 특수 경우 |
| FGKMT scale 언급 | 예; 서론 |
| empirical \(A=1\) 언급 | 예; 2차 진술 |
| \(H=G/F\) 전체 trajectory | 아니오 |
| exact interval minimum | 아니오 |
| global running minimum | 아니오 |
| Sono \(2.0\times10^{-17}\) ratio | 아니오 |
| start/end 동시 audit | 아니오 |

직접 중복은 아니다. 다만 \(H=1\) 참고선의 문헌 근거를 제공하므로 종합 판정과 방법론 문서도 이 논문을 반영해 수정했다.

## 10. 확인한 핵심 위치

- 초록과 연구 범위: p. 1
- end-bounded \(G(x)\), FGKMT \(A=1\) 계산 진술: p. 2
- 자연로그와 notation: p. 3
- trend functions: pp. 5-7
- 계산 figure와 Gumbel fit: pp. 8-10
- first occurrence 위치 heuristic: pp. 11-15
- record/first-occurrence 개수: pp. 15-17
- n번째 gap conjecture: p. 17

## 11. 최종 판정

Sono 상수나 FGKMT-normalized envelope를 계산한 연구는 아니지만, end-bounded 정의와 Wolf-related \(H=1\) empirical reference를 직접 뒷받침하는 중요한 보조 문헌이다. 결과의 대부분은 residue-class 계산과 heuristic이므로, 정리·all-prime 데이터·exhaustive verification과 명확히 구분해야 한다.
