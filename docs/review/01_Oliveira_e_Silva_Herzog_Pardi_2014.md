# Oliveira e Silva-Herzog-Pardi (2014) 분석

## 1. 서지정보

- Tomás Oliveira e Silva, Siegfried Herzog, Silvio Pardi
- “Empirical Verification of the Even Goldbach Conjecture and Computation of Prime Gaps up to \(4\cdot10^{18}\)”
- *Mathematics of Computation* 83(288), 2033-2060, 2014
- DOI: [10.1090/S0025-5718-2013-02787-1](https://doi.org/10.1090/S0025-5718-2013-02787-1)
- 검토 파일: [PDF](<../../article/EMPIRICAL VERIFICATION OF THE EVEN GOLDBACH CONJECTURE AND COMPUTATION OF PRIME GAPS UP TO 4 · 1018.pdf>)
- 분량: 28쪽
- SHA-256: `84088f8feefd04aaedec7d635b604d20e390a37aa9bec1dd1b526e5c8e9b5bf1`

## 2. 논문의 목표

주 목표는 even Goldbach conjecture를 \(4\times10^{18}\)까지 계산 검증하는 것이다. 그 과정에서 축적한 다음 통계를 이용해 prime 관련 점근식을 시험한다.

- minimal Goldbach partition의 count와 first occurrence
- 주어진 짝수 gap의 consecutive-prime occurrence count와 first occurrence
- record-breaking/maximal prime gaps
- prime-gap moments

본 프로젝트에는 Goldbach 결과보다 prime-gap 계산의 범위, 검증 절차, record table, gap moment가 중요하다.

## 3. 계산 방법과 검증 강도

### 3.1 계산 구조

논문은 cache-efficient segmented Eratosthenes sieve와 minimal Goldbach partition 계산을 결합한다. 전체 범위를 \(10^{12}\) 정수 크기의 서로 겹치지 않는 interval로 나누고 중앙 master가 worker에 분배했다(§1.1-1.3, pp. 2035-2042).

보고된 규모:

- 약 770 one-core CPU years
- interval별 두 worker ID와 소요시간
- residue class별 prime count
- minimal partition과 prime gap의 count 및 first occurrence
- 32-bit cyclic redundancy checksum
- 전체 통계 원자료 약 27 GB

### 3.2 오류 검출

각 \(10^{12}\) interval에서 다음을 검사했다.

1. minimal Goldbach partition count 합이 interval의 even integer 수와 일치
2. prime gap count 합이 interval의 prime count와 일치
3. independent combinatorial prime-count 구현과 비교
4. 불량 worker 결과를 폐기하고 재계산
5. residue-class count를 독립 프로그램으로 추가 비교

최종적으로 \(3\times10^{17}\)까지의 전 interval을 이중계산했다. 그 위 범위에서는 중요한 first occurrence를 포함한 interval과 나머지 interval의 약 4%를 이중계산했다. 고성능 계산환경에서 얻은 결과에서는 오류가 발견되지 않았다고 보고한다(pp. 2041-2042).

판정: 이 논문은 \(4\times10^{18}\) 이하 record의 강한 교차검증 근거다. 다만 모든 interval이 두 독립 구현으로 전수 재계산된 범위는 \(3\times10^{17}\)까지라는 세부를 metadata에 남겨야 한다.

## 4. prime-gap 정의와 경계

연속 소수에 대해

\[
g_k=p_{k+1}-p_k
\]

를 정의하고, \(P(g)\)를 gap \(g\)가 처음 나타나는 시작 소수로 둔다. \(N(g,x)\)는 주어진 \(g\)의 count다(§2.2, p. 2050).

논문은 count limit를 `p_k < x`로 할지 `p_{k+1} < x`로 할지 점근식에는 중요하지 않다고 말하면서, 실제 계산에서는 상한 밖 다음 소수를 구하지 않아도 되는 `p_{k+1} < x` 방식을 선택한다. 반면 Table 8 제목은 `p_k <= 4·10^18`인 record-breaking \(g_k\)를 제시한다.

이번 프로젝트에 주는 교훈:

- 논문 안에서도 count/table의 경계 표현을 세밀하게 읽어야 한다.
- source row마다 start prime과 endpoint를 모두 복원한다.
- `G_start`와 `G_end` 결과를 별도로 계산한다.

## 5. 핵심 prime-gap 결과

### 5.1 record table

- Table 8(pp. 2050): \(p_k\le4\times10^{18}\)에서 record-breaking gap \(g_k\)
- Table 9(p. 2051): \(P(g)\le4\times10^{18}\)인 first-occurrence record
- 보고 범위의 record gap은 1476까지 포함한다.

Table 8과 Table 9는 행의 의미가 다르다. Table 8은 순차 계산에서 발견한 record-breaking gap을, Table 9는 각 gap size의 first occurrence가 다시 record를 세우는 경우를 나타낸다. 데이터 정규화 시 두 표를 무비판적으로 합치지 않는다.

### 5.2 Cramér-Shanks 계열 정규화

논문은 first occurrence \(P(g)\)에 대해

\[
Q_6(g)=\frac{g}{\log^2P(g)}
\]

를 계산한다(§2.2.1, Figure 7, p. 2052). 대부분의 관측값은 1보다 작고 \(g\)와 함께 천천히 증가하는 양상을 보이지만, 저자들은 자료가 세 conjecture를 판정하기에 명백히 부족하다고 경고한다.

이 \(Q_6\)은 본 프로젝트의

\[
Q(x)=\frac{G(x)/F(x)}{2\times10^{-17}}
\]

와 완전히 다른 양이다. 이름이 같아도 혼용하지 않는다.

### 5.3 gap count와 moment

Hardy-Littlewood prime k-tuple conjecture에 근거해 gap count \(N(g,x)\)를 근사하고, 데이터가 전반적으로 예측과 잘 맞는다고 보고한다. prime-gap moment는

\[
D_k(x)=\sum_{p_{i+1}\le x}(p_{i+1}-p_i)^k
\]

로 정의하며

\[
D_k(x)\sim k!\,x\log^{k-1}x
\]

라는 일반화를 제안한다(§2.3, pp. 2056-2057). Table 12의 \(10^{10}\)에서 \(10^{18}\) 자료는 고차 보정항을 넣은 근사와 좋은 일치를 보인다.

## 6. 본 프로젝트에 사용할 부분

### 직접 사용

- \(4\times10^{18}\) 이하 maximal-gap record의 독립 교차검증
- source의 boundary semantics를 기록해야 한다는 근거
- exhaustive computation과 targeted double-check를 구분하는 provenance 양식
- gap count/moment를 Cramér형 보조 비교에 사용할 때의 기준

### 사용하지 않을 부분

- 이 논문 표만 최신 maximal-gap dataset으로 간주하지 않는다.
- Goldbach 검증범위를 prime-gap record의 최신성 또는 전 세계 exhaustive limit와 동일시하지 않는다.
- \(Q_6(g)\)를 FGMT-normalized \(H\) 또는 Sono 대비 \(Q\)로 바꾸어 읽지 않는다.

## 7. 제안 실험과의 중복 여부

| 항목 | 논문 수행 여부 |
|---|---|
| 실제 maximal-gap record | 예 |
| FGMT scale \(F(x)\) | 아니오 |
| \(H(x)=G/F\) | 아니오 |
| record interval minimum | 아니오 |
| running minimum/lower envelope of \(H\) | 아니오 |
| Sono `2e-17` 비교 | 아니오; 출판 이전 |
| Cramér \(\log^2x\) 비교 | 예 |

직접 중복은 아니다. 이 논문은 제안 연구의 data-validation anchor다.

## 8. 한계와 주의점

- 계산 논문의 upper limit와 현재 최신 record 범위는 다를 수 있다.
- 표에 실린 record는 전체 raw interval data가 아니다.
- \(3\times10^{17}\) 초과 전 범위가 모두 독립 이중계산된 것은 아니다.
- 점근식과의 좋은 일치는 증명이 아니다.
- prime-gap count, first occurrence, maximal gap의 경계 조건이 서로 어떻게 쓰였는지 결과별로 확인해야 한다.

## 9. 확인한 핵심 위치

- Abstract 및 연구범위: p. 2033
- 분산 계산과 오류 검출: pp. 2041-2042
- prime-gap record 정의와 Table 8: p. 2050
- Table 9: p. 2051
- \(Q_6(g)\) 및 Figure 7: p. 2052
- normalized gap moments, Table 12: p. 2056
- moment conjecture: pp. 2056-2057

## 10. 최종 판정

데이터 품질과 중첩 범위 검증에 가장 중요한 논문이다. 다만 본 프로젝트의 핵심 novelty 후보인 FGMT normalization, boundary별 interval minimum, Sono 대비 배수, empirical lower envelope는 수행하지 않았다.
