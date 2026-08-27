# Coverage-preserving compression의 유한범위 정식화

## 1. 지위와 범위

상태: `FORMAL FINITE FRAMEWORK / ALGORITHM SPEEDUP OPEN`

이 문서는 새로운 무한범위 소수 정리를 주장하지 않는다. 고정된 정수 범위와 gap
threshold `H`에서 “후보를 줄이거나 증거를 공유해도 실제 `gap >= H` start를 하나도
놓치지 않는다”는 데 필요한 유한 명제들을 분리해 적는다. 각 명제는 elementary
integer arithmetic과 exact prime/composite witness에만 의존한다.

`p^+`는 소수 `p` 다음의 소수다. 위험한 start의 술어를

\[
\mathcal B_H(p)\iff p\text{ is prime and }p^+-p\ge H
\]

로 둔다. 이 프로젝트에서는 equality `H=1856`도 위험에 포함한다.

## 2. 정리 A — 후보 superset 보존

유한 탐색 우주 `U`와 후보 집합 `C` (`C subseteq U`)가 다음 coverage 조건을 만족한다고 하자.

\[
\{p\in U:\mathcal B_H(p)\}\subseteq C.
\]

또한 exact verifier가 모든 `c` (`c in C`)에 대해 `not B_H(c)`를 인증하면 `U`에는
`gap >= H` start가 없다.

### 증명

반대로 `U`에 위험한 start `p`가 있다고 하자. coverage에 의해 `p`는 `C`에 속한다. 그러나
verifier는 모든 `C`의 원소에 대해 `not B_H`를 인증했으므로 모순이다. `QED`.

이 정리는 soundness만 준다. `C=U`로 두어도 맞기 때문에, 후보 수·생성비용·검증비용이
줄었다는 별도 증거 없이는 compression 또는 acceleration이라고 부르지 않는다.

## 3. 정리 B — exact rejection witness

정수 후보 `c`는 다음 두 형식 중 하나로 안전하게 제거할 수 있다.

1. `1<d<c`이고 `d`가 `c`를 나누는 exact factor가 존재한다.
2. exact certificate로 소수임이 검증된 `q`가 `c<q<c+H`를 만족한다.

첫째이면 `c`가 소수가 아니므로 위험한 prime start가 아니다. 둘째에서 `c`가 소수라면
`c^+<=q`이므로 `c^+-c<H`이고, `c`가 합성수이면 애초에 위험한 start가 아니다.

여기서 probable-prime 표시는 exact certificate가 아니다. `q=c+H`도 strict inequality를
만족하지 않으므로 제거 witness가 아니다.

## 4. 정리 C — witness family의 coverage-preserving compression

각 machine-checkable witness `w`가 유한 집합 `Cov(w)` (`Cov(w) subseteq U`)를 명시하고, exact
검증이

\[
\forall c\in Cov(w),\quad \neg\mathcal B_H(c)
\]

를 보장한다고 하자. witness family `W`가

\[
U\subseteq\bigcup_{w\in W}Cov(w)
\]

를 만족하면 `U`에는 위험한 start가 없다.

### 증명

임의의 `c` (`c in U`)는 적어도 한 `Cov(w)`에 속한다. 그 witness의 soundness로
`not B_H(c)`다. 따라서 모든 `c in U`가 안전하다. `QED`.

### 실제 compression이 되기 위한 추가 조건

위 정리는 coverage 보존만 말한다. 알고리즘 개선 후보가 되려면 다음도 모두 측정한다.

- witness family와 coverage map의 byte 수
- witness 생성 시간과 exact 검증 시간
- 남은 survivor를 기존 탐색기로 검사하는 시간
- baseline과 동일한 `U`, `H`, false-negative 0 계약
- `T_generate + T_verify + T_survivor < T_baseline`

좌표를 바꾸거나 같은 후보를 중복 표현하는 것은 이 비용을 줄이지 않으므로 compression이
아니다.

## 5. 공유 witness의 두 가지 sound한 예

### 5.1 하나의 소수로 여러 start 제거

증명된 소수 `q` 하나는 정수 집합

\[
Cov(q)=U\cap[q-H+1,q-1]
\]

의 모든 후보를 제거한다. 각 `c` (`c in Cov(q)`)에서 `c<q<c+H`이기 때문이다. 이 경우
prime certificate 하나를 여러 후보가 공유할 수 있다. 다만 이런 `q`들의 family가
`U` 전체를 덮는지 별도로 증명해야 한다.

### 5.2 합동류의 공유 factor

소수 `ell`과 residue `r=0 mod ell`에 대해 `c>ell`인 모든 `c congruent 0 mod ell`은
factor `ell`로 합성이다. wheel은 이 작은 소수 divisibility geometry를 공유하게 해준다.
그러나 wheel을 통과한 같은 residue-state의 두 수가 함께 소수이거나 같은 위치에 다음
소수를 갖는다는 결론은 나오지 않는다.

## 6. 정리 D — half-open block의 right-boundary closure

start-bounded block `[a,b)`의 내부 위험 start upper bound가 exact하게 0이라고 하자.
다음 증거가 추가로 존재한다고 하자.

1. exact certificate를 가진 소수 `p`가 `a<=p<b`다.
2. 모든 `n` (`p<n<b`)에 exact nontrivial factor가 있다.
3. exact certificate를 가진 소수 `q>=b`가 있고 `q-p<H`다.

그러면 `[a,b)`에서 시작하는 `gap >= H`는 0개다.

### 증명

2에 의해 `p`는 `b`보다 작은 마지막 소수다. `p` 다음 소수는 `p^+<=q`이므로
`p^+-p<=q-p<H`다. 따라서 block을 가로지르는 유일한 미해결 start `p`도 안전하다.
나머지 internal start는 가정한 upper bound 0이 닫는다. `QED`.

`q`가 바로 다음 소수임을 증명할 필요는 없지만, `p`와 `b` 사이의 composite coverage는
누락할 수 없다. 이것이 P009 single-block witness의 정확한 계약이다.

## 7. 따름정리 — block partition coverage

서로 겹치지 않는 half-open block `[a_i,b_i)`가 `U=[A,B)`를 정확히 분할하고, 모든
block이 정리 D의 조건을 만족하면 `U`의 위험 start는 0개다. 이는 각 block의 결론을
유한 합집합에 적용한 것이다. 마지막 block의 crossing도 반드시 닫아야 한다.

## 8. `B=2` union 교정

`S=p-1`, `q-p=2m`,

\[
I_j=[S+2(j-1),S+2j-1]
\]

이면

\[
I_2\cup\cdots\cup I_m=[p+1,q-2]
\]

이다. `q-1`은 포함되지 않는다. `p,q`가 2보다 큰 소수이면 `q-1`은 짝수라는 별도
factor-2 witness로 닫을 수 있지만, 원래의 `[p+1,q-1]` 등식은 거짓이다. 또한
`S=p-1`은 미지의 `p`를 이미 알아야 하므로 discovery compression에는 순환적이다.

## 9. 보조정리 — empty-block parity lower bound

`S`가 짝수이고 길이 `B`인 block을

\[
I_j=[S+(j-1)B,S+jB-1]
\]

로 둔다. `I_1`에 2보다 큰 소수가 있고 `p`를 그 block의 마지막 소수라 하자.
`I_2,...,I_D`에는 소수가 없고 `q`를 `I_D` 뒤의 첫 소수라 하자. 그러면

\[
q-p\ge
\begin{cases}
(D-1)B+3,&B\text{ odd and }D\text{ even},\\
(D-1)B+2,&\text{otherwise}.
\end{cases}
\]

### 증명

`p`와 `q`는 홀수다. `B`가 짝수이면 가능한 가장 큰 `p`는 `S+B-1`, 가능한 가장 작은
`q`는 `S+DB+1`이므로 차는 `(D-1)B+2` 이상이다. `B`가 홀수이면 가장 큰 홀수 `p`는
`S+B-2`다. 이때 `D`가 짝수이면 `S+DB`가 짝수라 최소 홀수 `q`는 `S+DB+1`이고
하한은 `(D-1)B+3`이다. `D`가 홀수이면 `S+DB` 자체가 홀수이므로 하한은
`(D-1)B+2`다. `QED`.

이 보조정리는 empty pattern으로 큰 gap의 **존재 하한**을 주는 방향이다. 큰 gap의
부재 필터나 candidate compression 정리는 아니다.

## 10. 같은 residue-state에서 actual primality가 전달되지 않는 이유

고정 wheel `M`의 unit residue `r`은 `gcd(r,M)=1`만 보장한다. Dirichlet 정리에 의해
`r mod M`에는 소수가 무한히 많다. 한편 `r+kM` 형태의 합성수도 만들 수 있다. 예를
들어 `r`과 서로소인 소수 `ell`을 택하고 `r+kM congruent 0 mod ell`이 되게 하는
`k`의 합동류를 택하면, 충분히 큰 항은 `ell`의 배수인 합성수다. 따라서 같은 state는
작은 소수에 대한 divisibility pattern만 공유하며 absolute primality나 다음 소수 위치를
translation할 수 없다.

## 11. P010A와 P010B의 역할

- P010A는 residue-state dual certificate로 **count upper bound**를 낮추는 연구다.
- P010B는 이 bound/certificate가 실제 search candidate를 누락 없이 줄이고 총비용도
  낮추는지 보는 **search acceleration** 연구다.

P010A의 상한이 개선되어도 정리 A의 candidate map 또는 정리 C의 total coverage가
없으면 P010B의 가속 결론은 나오지 않는다. 반대로 P010B의 candidate cover가 생겨도
exact verifier와 baseline 비교가 없으면 알고리즘 승격은 보류한다.

## 12. Direct finite verifier 구현 상태

`source/candidate_cover.py`는 정리 A–C를 최대 1,000,000 integer starts의 작은 직접 우주에서
검증한다. 각 omitted start에는 exact factor 또는 `c<q<c+H`인 exact small-prime witness를
요구하고, candidate/rejection 중복과 coverage hole을 거부한다.

`[1000,10000)`, `H=20` toy에서 69 candidates가 exact 위험 start 69개와 일치했다. 이 toy
generator는 exact truth를 먼저 계산하므로 정리의 verifier fixture일 뿐 discovery compression은
아니다. 다음 정식화 대상은 모든 start를 나열하지 않는 range/DAG coverage proof와 큰 q의
PARI certificate binding이다.
