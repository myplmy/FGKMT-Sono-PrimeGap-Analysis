# DEP-R09 Gallagher--Maier PAP density-integral split 타당성 검토

- 검토일: 2026-09-14 KST
- 대상: Theory 71의 near-one density를 Gallagher--Maier PAP에 연결하는 경로
- 정본: [Theory 72](../method/theory/72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md)
- 판정: **분할 자체는 타당, 현 \(d=160\) 수치 certificate는 불충분**

## 1. 사용자용 요약

이번 결과에는 좋은 소식과 나쁜 소식이 하나씩 있다.

- 좋은 소식: Theory 71이 “1 가까이”만 다룬다고 해서 Jutila의 훨씬 넓은 정리를
  전부 다시 증명할 필요는 없다. 1에서 먼 부분은 2021년 peer-reviewed explicit
  zero-count로 안전하게 덮을 수 있다.
- 나쁜 소식: 1 가까운 부분의 현재 안전계수가 너무 크다. \(X\)를 크게 하면 사라져야
  하는 오차 상계가 약 \(2.73\times10^{13}\)에 머물러, 주항보다 작다는 보증조차 못 한다.

이는 “FGKMT/Sono 부등식이 틀렸다”거나 “소수 분포의 실제 오차가 크다”는 결과가 아니다.
현재 만든 증명용 자가 너무 두꺼워 실제 물체보다 \(10^{14}\)배쯤 넓게 재고 있다는
뜻이다.

## 2. 핵심 논리의 타당성

### 2.1 near/far 분할

Gallagher의 Stieltjes identity에는 \(N(\alpha)\), 즉 실수부가 \(\alpha\) 이상인
영점 수가 들어간다. \([0,1-\theta]\)에서는 이를 전체 영점수 \(N(0)\)로 올려도
부등호 방향이 맞다. endpoint \(X^{-1}N(0)\)까지 함께 계산하면
\(N(0)X^{-\theta}\)로 정확히 정리된다.

**판정:** 타당. endpoint 중복이나 누락이 없다.

### 2.2 Bennett et al.의 적용

Theorem 1.1은 primitive conductor \(q>1\), \(T\ge5/7\)의 양쪽 높이
\(|\gamma|\le T\)를 multiplicity 포함해 센다. Theory 71과 Gallagher가 필요한
primitive nonprincipal family의 전 높이 상계로 방향이 맞다. conductor 1은 이 정리의
범위가 아니므로 zeta branch를 별도로 OPEN으로 남긴 것도 맞다.

**판정:** far branch의 입력으로 타당. local near-one density의 대체품은 아니지만,
이번에는 far branch에만 사용하므로 scope가 맞다.

### 2.3 Theory 71의 near 적분

Theory 71의 local factor는
\(\max\{\delta,1/L\}\)다. 이를 단순히 \(\theta\)로 올리면 불필요한
\(\log X\) 손실이 생긴다. 새 식은 \(\delta=1/L\)에서 두 구간으로 나누어
지수함수를 정확히 적분했고, 독립 numerical quadrature와 일치했다.

**판정:** 타당. 이 분할은 정밀도를 낮추지 않으며 오히려 거친 상계를 피한다.

## 3. 수치 판정의 의미

\(\theta=1/21,d=160,c_1=1/24\)에서

- far exponent는 \(13/3360>0\)라 감소한다.
- near kernel exponent는 \(\lambda=69/80>0\)다.
- 그런데 Theory 71의 \(C_J=9{,}287{,}613{,}243{,}090\)가 앞에 남는다.
- 결과적으로 현재 near upper certificate의 asymptotic 값은
  \(2.7276984\times10^{13}\)이다.

따라서 다음 두 문장을 구분해야 한다.

1. **말할 수 있음:** 현 certificate는 \(d=160\) PAP를 증명하기에 너무 약하다.
2. **말할 수 없음:** 실제 PAP 오차가 \(2.7\times10^{13}\)이다.

두 번째는 잘못이다. 계산한 값은 실제 오차가 아니라 실제 오차를 덮는 매우 보수적인
상계다.

## 4. \(d=3856,4096\)을 채택하면 안 되는 이유

현 asymptotic 상계만 놓고 보면 첫 정수 통과점은 다음과 같다.

| 목표 | 첫 정수 \(d\) |
|---|---:|
| near certificate \(<1\) | 3856 |
| near certificate \(\le e^{-2}\) | 4096 |

하지만 Theory 58의 downstream coefficient capacity는 낙관적으로 잡아도
fixed \(2\times10^{-17}\)를 유지하려면 \(d\le186\)이었다. 즉 \(d\)를 수천으로
늘리는 방법은 한 문제를 해결하면서 연구 대상 계수를 잃는다. 또한 위 값은
asymptotic 진단일 뿐 finite common cutoff와 나머지 OPEN multiplier를 포함한 완성
정리가 아니다.

**판정:** 유용한 불가능성 진단이지만 새 PAP parameter로 채택 금지.

## 5. 아직 반드시 필요한 증명

| 남은 항목 | 필요한 이유 | 현재 상태 |
|---|---|---|
| near-one coefficient 대폭 축소 | 가장 먼저 실패하는 gate | HARD BLOCKER |
| Gallagher explicit-formula multiplier·cutoff | 식 (30) 앞의 \(\ll\) 제거 | OPEN |
| principal zeta branch | q=1 항은 Theory 71/Bennett family 밖 | OPEN |
| exceptional/good-modulus transfer | Maier Lemma 1과 Gallagher exceptional branch가 정성적 | OPEN |
| orthogonality·induction numerical replay | family 평균을 각 residue-class 하계로 옮김 | OPEN |
| \(\psi\)-to-\(\pi\) | 최종 prime count에는 partial summation 비용 필요 | OPEN |
| 모든 cutoff의 maximum | 한 \(X_{\rm cert}\)로 합침 | OPEN |

## 6. 권장 연구 방향

현재는 뒤쪽 OPEN 항목을 차례로 숫자화하기보다 \(C_J\) loss tree를 먼저 감사하는 편이
합리적이다. 현재 상계는 \(d=186\)에서도 약 \(2.15\times10^{13}\)이므로, principal
또는 partial-summation 상수를 조금 개선해서는 gate가 바뀌지 않는다.

우선 후보는 다음 세 가지다.

1. Jutila selected-system coefficient에서 residue 52와 preterminal
   \(170/\theta^2\)를 곱하기 전에 평균 수준 cancellation을 보존할 수 있는지 확인.
2. local square count를 모든 cell에 동일 최악값으로 곱한 factor 2와
   \(3+r\log(2\mathcal D)\)를 Gallagher 적분 안에서 직접 평균할 수 있는지 확인.
3. current detector를 거치지 않는 modern explicit near-one density theorem이
   \(d\le186\)에서 충분한 coefficient를 주는지 source-first 비교.

필요한 개선폭이 약 \(10^{14}\)이므로 몇 퍼센트 수준의 상수 다듬기는 충분하지 않다.
구조적 중복 제거 또는 더 강한 source theorem이 필요하다.

## 7. 검증 범위

- Python 표적시험 11개 PASS:
  source hash·판독정책, Bennett family envelope, far endpoint identity,
  near piecewise formula 대 quadrature, endpoint exact exponent, fail-closed domain,
  root OPEN 상태.
- Lean 대상:
  endpoint 유리수 대수, family-count 조건부 합성, far endpoint 소거,
  near piecewise 대수 소거.
- 실제 maximal-gap data·prime sweep·장시간 연산: 수행하지 않음.
- decimal: 120-dps diagnostic이며 directed interval certificate 아님.
- <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>:
  사용하지 않음.

## 8. 최종 판정

**Theory 71의 near-one 범위는 Gallagher 적분을 완성하는 데 원리상 충분하다.**
far branch를 Bennett total-zero bound가 맡기 때문이다. 그러나 **현재 Theory 71
상수로는 \(d=160\), 나아가 fixed coefficient capacity 안의 \(d\le186\)에서 PAP를
인증할 수 없다.** 그러므로 <code>PAP-11</code>, <code>DEP-R09</code>,
fixed \(2\times10^{-17}\), \(X_{\rm cert}\)는 계속 OPEN이다.
