# Kourbatov (2018) n번째 AP record gap 분석

## 1. 서지정보

- Alexei Kourbatov
- “On the nth Record Gap Between Primes in an Arithmetic Progression”
- *International Mathematical Forum* 13(2), 65-78, 2018
- DOI: [10.12988/imf.2018.712103](https://doi.org/10.12988/imf.2018.712103)
- 검토 파일: [PDF](<../../article/On the nth Record Gap Between Primes in an Arithmetic Progression.pdf>)
- 분량: 14쪽
- SHA-256: efa5af49c85e28eb605c7d53015cc3caabff47149da33bf20d35f2679247c80d

## 2. 연구 질문

서로소인 \(q>r\ge1\)의 산술진행 \(r+kq\) 안에서 n번째 maximal record gap의 크기

\[
R(n,q,r)
\]

와 \(x\) 이하에서 관측된 record 수

\[
N_{q,r}(x)
\]

를 경험적·heuristic하게 분석한다. 관심은 \(x\)에 따른 한 계단함수의 exact envelope보다, record index \(n\)에 따른 크기와 residue class \(r\)에 걸친 분포다.

## 3. 핵심 heuristic

전체 소수의 maximal gap에 대한 Cramér-Shanks \(\log^2x\) heuristic과 record 수 가정을 결합한다. \(x\)와 \(ex\) 사이의 예상 record 수를 \(\tau(q,x)\)라 하고, 그 극한이 존재한다고 가정하면

\[
\lim_{x\to\infty}\frac{N_{q,r}(x)}{\log x}=2
\]

라고 추론한다(pp. 69-70).

그 결과 전형적인 n번째 AP record는

\[
R(n,q,r)\approx
\frac{\varphi(q)n^2}{\bar\tau^2}
\]

규모이며, \(\bar\tau\approx2\)라면 선도항은 대략 \(\varphi(q)n^2/4\)가 된다.

논문은 계산 가능한 n을 위해 보정항을 더한 a.s. heuristic upper bound

\[
R(n,q,r)<
\varphi(q)n^2+(n+2)q\log^2q
\]

를 제안한다. 이는 정리가 아니라 유한 계산으로 지지된 conjectural bound다.

## 4. 계산 설계와 범위

수정한 PARI/GP code를 사용했다(p. 71).

- 모든 \(q\le2000\)과 허용되는 모든 \(r\)에 대해 처음 14개 record 계산
- 일부 작은 \(q\)는 20개 이상 계산
- 선택한 큰 \(q\)는 \(80000\)까지 계산
- 각 \((q,n)\)에서 \(r\)별 \(R(n,q,r)\)의 최소·최대·평균·중앙값·표준편차·왜도·사분위수 계산

계산한 \(q\le2000,n<15\)에서는 제안 upper bound의 예외를 찾지 못했다. 논문 자체도 일부 \(q\)에서 유한 예외가 있을 수 있음을 열어둔다.

## 5. 성장과 분포 결과

고정 \(q\)에서 \(r\)에 대한 중앙값은

\[
\operatorname{median}_r R(n,q,r)
\approx A_qn^2+B_qn
\]

으로 잘 맞고,

\[
A_q\approx0.3\varphi(q),\qquad
B_q<\varphi(q)\log^2q
\]

라는 경험적 값을 제안한다(pp. 71-73). 평균·사분위수도 이차식으로 잘 맞고 표준편차는 대략 n에 선형으로 증가한다.

\(q=9001\), \(n=6,8,10,12\)의 \(r\)-별 histogram은 오른쪽으로 치우치며, Gumbel과 lognormal이 모두 근사한다. n이 증가할수록 왜도가 천천히 감소해, 극한분포가 존재한다면 normal일 가능성도 논의한다. 그러나 실제 계산 가능한 n에서는 normal과 상당히 멀고, limiting distribution의 존재 자체가 열린 문제다(pp. 74-76).

## 6. maximal-gap 경계 의미

논문은 \(G_{q,r}(x)\)를 progression 안에서 \(x\) 이하인 소수들 사이의 maximal gap으로 사용하고, \(N_{q,r}(x)\)도 end-of-gap prime이 \(x\) 이하인 record 수로 해석한다. 따라서 이번 프로젝트의 end-bounded convention과 가까우나 다음 차이가 있다.

- all-prime \(q=2,r=1\)이 아닌 다수 residue class가 주 대상
- x별 exact step function보다 n번째 record 통계가 주 대상
- exhaustive all-prime record coverage를 제공하지 않음

## 7. 본 프로젝트에 주는 시사점

### 활용 가능

- record count가 매우 느리게 증가한다는 empirical 배경
- \(R(n,q,r)\)의 이차 성장과 \(\log^2x\) 모델 간 연결
- Gumbel sample maxima와 nth-record limiting law를 구분해야 한다는 경고
- heuristic, finite computation, theorem을 명시적으로 분리하는 서술 방식

### 활용 불가

- AP의 \(\varphi(q)\) scaling을 all-prime FGKMT normalization으로 대체하지 않는다.
- conjectural upper bound를 데이터 validation rule로 쓰지 않는다.
- \(r\)에 걸친 distribution을 한 all-prime record trajectory의 time trend로 해석하지 않는다.
- 논문의 record table을 최신 all-prime maximal-gap 정본으로 사용하지 않는다.

## 8. 제안 실험과의 중복 여부

| 항목 | 논문 수행 여부 |
|---|---|
| 실제 record-gap 계산 | 예; AP 중심 |
| all-prime record 검증 | 제한적 배경 |
| record index별 분포 | 예; 핵심 |
| FGKMT scale \(F(x)\) | 직접 사용 안 함 |
| \(H(x)=G(x)/F(x)\) | 아니오 |
| interval-wise minimum | 아니오 |
| running/local envelope | 아니오 |
| Sono constant와 ratio | 아니오 |
| start/end 동시 계산 | 아니오 |

직접 중복되지 않는다. 이 논문은 AP record의 index-domain 통계이며, 제안 연구는 all-prime record의 x-domain FGKMT/Sono normalization과 exact interval envelope다.

## 9. 확인한 핵심 위치

- 정의·연구 질문·Resnick 배경: pp. 65-66
- all-prime \(R(n)\) heuristic과 finite check: pp. 67-68
- AP generalization과 record-count limit: pp. 68-70
- 계산 범위·upper bound·quadratic trend: pp. 71-73
- 분포와 skewness: pp. 74-76

## 10. 최종 판정

record index와 residue class를 축으로 한 유용한 empirical 연구다. \(\log^2x\) 계열 보조 비교와 record-count 해석에는 도움이 되지만, FGKMT/Sono 함수·interval minimum·global running minimum을 계산하지 않으므로 본 실험과 직접 중복되지 않는다.
