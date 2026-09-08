# H1b-2a.2 Proposition 9.4 distribution error 타당성검토

- 작성일: 2026-09-08
- 검토 대상:
  [`30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md`](../method/theory/30_Sono_FMT_H1b2a2_Proposition94_distribution_error.md)
- 판정: **실제 FGKMT/FMT의 \(\mathcal A=\mathbb Z\) 호출에 한해 타당한 parameterized
  finite reduction**
- 과학적 상태: `CHILD_CLOSED_AT_EXPLICIT_GATE / P94_PARENT_OPEN`

## 1. 한 문장 결론

일반 집합용 Hypothesis 1 상수를 복원하지 않고도, 실제 호출의 연속 정수 interval에서는
\(E_q^{(1)}\le1\)이 정확하므로 식 (9.52) 오류를 명시적으로 흡수할 수 있다. 다만 이 결과를
일반 Proposition 9.4나 Sono 정리 전체의 numerical threshold로 확대하는 것은 타당하지 않다.

## 2. 사용자용 쉬운 설명

이 오류는 “정수를 여러 나머지 칸에 나눴을 때 칸마다 몇 개씩 들어가는가”에서 생긴다.
연속된 정수라면 칸 사이의 차이는 최대 한 개다. 그러므로 어려운 소수분포 정리를 쓰지 않아도
된다.

예를 들어 10개의 연속 정수를 3개 나머지 칸에 나누면 \(4,3,3\)개처럼 배치된다. 평균은
\(10/3\)이고 각 칸의 오차는 1보다 작다. modulus가 아무리 커져도 이 구조는 바뀌지 않는다.

그러나 “그 정수에 선형식을 적용한 값이 소수인가”를 세는 Proposition 9.2는 이런 단순한
칸 나누기가 아니다. 그래서 H1c-1의 소수분포 연구는 계속 필요하다.

## 3. 타당한 핵심

### 3.1 실제 적용의 식별

FGKMT Lemma 7.2와 Theorem 6 적용부는 실제로

\[
\mathcal A=\mathbb Z,\quad \theta=1/3,
\]

를 선택하고 Proposition 9.4에 \(D=1,\xi=\theta/10\)을 넣는다. 따라서 일반 \(\mathcal A\)
문제를 그대로 풀 필요는 없다.

### 3.2 discrepancy의 exact bound

\(N\)개의 연속 정수를 modulus \(q\)로 나눈 residue count는
\(\lfloor N/q\rfloor\) 또는 \(\lceil N/q\rceil\)다. 따라서 기준값 \(N/q\)와의 차이가
1 이하라는 결론은 endpoint나 확률적 추정에 의존하지 않는다.

### 3.3 tuple multiplicity의 hidden constant 제거

각 자유 소수마다

- 좌표 \(k+1\)개,
- `d only / e only / both` 3개

뿐이므로 경우의 수 \([3(k+1)]^\omega\)는 정확한 과대계수다. support와 coprimality는 경우를
줄일 뿐 늘리지 않는다. 따라서 원문의 \(O(\tau_{3(k+1)}(q))\)를 multiplier 1의
\(\tau_{3(k+1)}(q)\) 상계로 바꾸는 것이 타당하다.

### 3.4 전체 residue-class factor

원문은 먼저 \(v_0\pmod V\)별로 계산한다. 이번 상계는 마지막에 허용되는 \(v_0\)가 많아도
\(V\)개라는 factor를 포함한다. 이 factor를 빠뜨리지 않았고, 결과적으로 최종식에는
\(V^2\)가 나타난다.

### 3.5 주항과의 비교 방향

오류의 상계와 Proposition 9.4 표준 우변의 **하계**를 비교해야 한다. 이번 증명은

- \(\mathfrak S_B(\mathcal L)>e^{-9k/2}\),
- \(I_k(F)\ge(2k\log k)^{-k}\),
- \(n/\phi(n)\ge1\),
- \(\#\mathcal A(x)\ge x/2\)

를 사용한다. 방향이 모두 정확하다.

### 3.6 author TeX의 Möbius inversion 순서 교정

Maynard author TeX line 1090의 `r_0|d_0`는 line 1098의
\(\widetilde\lambda_1\) 전 범위 합과 양립하지 않는다. 최종 출판본 (9.56)은
`d_0|r_0`로 되어 있고 표준 Möbius inversion과도 일치한다. 최종 출판본을 채택한 것은
타당하며, 이 차이를 숨기지 않고 contract에 correction으로 등록했다.

## 4. 일부러 보수적으로 둔 부분

### 4.1 \(\widetilde\lambda_{d_0}\)

\(1/\phi(r_0)\le1\)만 써

\[
|\widetilde\lambda_{d_0}|\le
(W_0/\phi(W_0))x^\xi
\]

로 뒀다. 실제 summatory 구조를 쓰면 훨씬 작아질 수 있지만, 현재 목적은 작은 cutoff 최적화가
아니라 hidden constant 없이 오류를 유한식으로 만드는 것이다.

### 4.2 divisor sum

squarefree·coprime 제약을 모두 버리고

\[
\sum_{q<Q}\tau_a(q)\le Q(1+\log Q)^a
\]

를 썼다. 매우 느슨하지만 안전하다.

### 4.3 \(\theta<15/16\)

crude support 상계에서는 감소 지수가

\[
\beta=1-16\theta/15
\]

다. 그래서 이 project proof는 \(\theta<15/16\)만 다룬다. 이는 일반 Maynard 명제의 허용범위를
줄이지만, 실제 FGKMT/FMT의 \(\theta=1/3\)은 충분히 안쪽에 있으므로 현재 적용에는 문제가 없다.

## 5. 반드시 유지해야 할 한계

### 한계 A: 일반 \(\mathcal A\)에는 적용 불가

구멍이 있는 임의의 집합은 residue discrepancy가 1 이하가 아니다. 따라서 이번 우회를 일반
Maynard Proposition 9.4의 증명으로 적으면 틀린다.

### 한계 B: Hypothesis 1 전체를 닫지 않음

Hypothesis 1(1),(3)은 실제 P94 오류에서 우회됐을 뿐이다. Hypothesis 1(2)의 affine prime
distribution은 Proposition 9.2에 남아 있다.

### 한계 C: P94 parent는 아직 열림

H1b-1b-2d, H1b-2a, H1b-2a.1, 이번 H1b-2a.2가 서로 다른 normalization으로 상계를
제공한다. 한 factor를 두 번 세거나 빠뜨리지 않았는지 end-to-end로 합성한 단일 certificate가
아직 없다. 따라서 `H1B-P94=RATE_MISSING` 유지가 타당하다.

### 한계 D: 설명용 수치는 theorem threshold가 아님

\(k=36,\alpha=2,\theta=1/3\) 진단에서 \(\log x\)가 약 \(3.52\times10^{133}\) 이상이라는
값이 나오지만, 기존 smooth gate가 지배한 한 component의 충분조건이다. \(X_{\rm cert}\)라고
부르면 안 된다.

### 한계 E: `mpmath`는 directed rounding 증명이 아님

코드는 log 식과 gate를 검산한다. 엄밀한 내용은 문서의 symbolic 부등식이며, 출력 소수는
진단값이다. 이번 gate에는 Lean이나 새 Python 라이브러리가 필요하지 않다.

## 6. 자동 검증 판정

회귀시험 설계는 다음 오류를 막는다.

| 위험 | 방지 시험 |
|---|---|
| interval endpoint 오산 | 음수·양수 endpoint를 포함한 brute-force count |
| \(3k\)와 \(3(k+1)\) 혼동 | toy assignment exact count |
| divisor-sum 방향 오류 | 작은 \(Q,a\)의 전수 tuple count |
| gate를 충족하지 않았는데 PASS | 작은 \(\log x\) fail-closed 시험 |
| child를 parent로 과대 승격 | `proposition_94_closed=false`, `X_cert=false` 고정 |
| source drift | 네 1차 원천의 SHA-256 확인 |

## 7. 상태 판정

| 항목 | 이전 | 현재 | 근거 |
|---|---|---|---|
| P94 interval discrepancy | general Hypothesis 1 입력 대기 | exact 1 | 실제 \(\mathcal A=\mathbb Z\) |
| P94 tuple multiplicity | hidden \(O\) | multiplier 1의 \(\tau_{3(k+1)}\) | prime assignment |
| P94 distribution child | `INPUT_PACKAGE_MISSING` | `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT` | 명시적 \(\rho_{94}\), \(Y_{94}\) |
| Hypothesis 1(2) | open | open | prime moment에 계속 필요 |
| P94 parent | `RATE_MISSING` | `RATE_MISSING` | end-to-end 합성 미완료 |
| SIV-07/09 | `HARD_BLOCKER` | `HARD_BLOCKER` | 전체 moment package 미완료 |
| \(X_{\rm cert}\) | `OPEN` | `OPEN` | root dependency 다수 미완료 |

## 8. 권장 후속

### 1순위: H1b-2a.3 P94 end-to-end composition

- 내용: 닫힌 P94 하위 package를 하나의 multiplier와 최대 cutoff로 합성한다.
- 이유: 이번 child를 실제 parent 상태 전이로 연결하는 가장 가까운 단계다.
- 예상: 6--12시간의 source 재계수·수식 감사와 2--4시간의 계약/시험.
- 사용자 수행절차: 별도 수행절차 필요없음.

### 2순위: H1c-1 quantitative prime-distribution source trace

- 내용: Proposition 9.2에 필요한 Hypothesis 1(2)의 character/Bombieri--Vinogradov 경로를
  계속 정량화한다.
- 이유: P94에서는 우회됐지만 good-weight 전체에는 여전히 핵심 hard blocker다.
- 예상: 여러 단계 합계 수일 이상. 한 번에 숫자를 약속하지 않고 lemma별로 분할한다.
- 사용자 수행절차: 별도 수행절차 필요없음.
