# DEP-R09 FMT filtration 민감도·survivor floor 타당성검토

- 작성일: 2026-09-15 KST
- 대응 이론:
  [Theory 81](../method/theory/81_Sono_FMT_DEPR09_filtration_sensitivity_survivor_floor_audit.md)
- 기계 원장:
  [filtration sensitivity and survivor floor v1](../method/theory/data/Sono_FMT_DEPR09_filtration_sensitivity_survivor_floor_v1.json)
- 판정:
  <code>DENOMINATOR_DOMAIN_REPAIRED /
  COUNT_SENSITIVITY_VALID /
  CHARACTER_PHASE_SHORTCUT_INVALID /
  ANALYTIC_SECOND_MOMENT_OPEN</code>

## 1. 한 문장 결론

최종 후보가 충분히 많이 남는다는 **분모 하한**은 정확한 성공 사건에 맞춰 재사용할 수
있지만, residue 하나를 바꿀 때 weighted character error도 조금만 변한다는 단순 생각은
작은 exact 반례로 틀렸음이 확인됐다.

## 2. 쉬운 비유

소수 거르기를 “체에 구멍을 막아 숫자를 탈락시키는 작업”이라고 생각해 보자.

- residue 하나를 바꾸면 어느 숫자가 체를 통과하는지는 한 소수 (p)의 두 줄에서만
  달라진다. 그래서 **남은 숫자의 개수** 변화는 작다.
- 하지만 각 남은 숫자에 (+1,-1) 같은 character 부호를 붙여 더하면 이야기가 달라진다.
  통과 여부가 그대로인 숫자도 residue 변경 때문에 부호가 바뀔 수 있다.

즉 “사람 수가 거의 그대로다”라는 사실은 “사람들이 든 찬성·반대 표의 합도 거의
그대로다”를 뜻하지 않는다. 이번 weighted error가 바로 두 번째 종류다.

## 3. Theory 80에서 발견한 적용영역 보정

Theory 80은 outer-good 사건 (O)에서 survivor 수 (M_\omega)가 양수라는 floor를
전제로 normalized error를 정의했다. finite 확률대수 자체는 그 전제 아래 맞다.

그러나 Theory 55를 다시 읽으면 실제 floor는 다음 두 조건이 모두 성공한 outcome에서 나온다.

1. 첫 residue 추첨이 good이다.
2. 그 뒤 conditional covering 추첨도 good이다.

따라서 올바른 사건은 (S_{\rm sieve}=O\cap I_{\rm good})다. 이 사건의 최소 확률질량은
((1-F_{\rm out})(1-F_{\rm in}))이고, 바로 그 사건에서

\[
 M_\omega\ge A(1-\eta)X/\log X
\]

를 쓴다. Theory 81은 분자 raw moment도 같은 사건 indicator와 묶었다. 이 수정으로
0으로 나누거나 평균 survivor를 pointwise lower bound처럼 쓰는 위험을 제거했다.

## 4. 무엇이 exact하게 증명됐는가

(P)가 서로 다른 소수들의 곱이고 residue를 prime (p) 한 곳에서만 바꾼다고 하자.
(N)개의 연속 offset 중 생존 여부가 달라질 수 있는 것은 old forbidden class와 new
forbidden class 두 줄뿐이다. 한 줄에는 최대 (\lceil N/p\rceil)개가 있으므로

\[
 |T_m\triangle T_{m'}|\le2\lceil N/p\rceil.
\]

따라서 survivor **개수** 변화도 이보다 작다. 이 부분은 초등 증명과 small modulus
전수시험이 일치한다.

## 5. 어떤 지름길이 틀렸는가

(P=65=5\cdot13), offset (1,2,3), CRT shift (0\to13)을 보자. 이 변경은 modulo
13은 그대로이고 modulo 5만 바꾼다. quadratic character modulo 5와 principal character
modulo 13의 곱을 쓰면 character 합은

\[
 -1\longrightarrow2
\]

로 3만큼 변한다. 그러나 survivor symmetric difference는 1이고 일반 count 경계도 2다.
따라서 “count 변화 경계 2를 character 합에도 그대로 적용”하는 주장은 거짓이다.

이 반례는 모든 martingale 접근이 불가능하다는 뜻은 아니다. 오직 현재 제안된 단순한
coordinate-Lipschitz 근거가 충분하지 않음을 확정한다.

## 6. 왜 독립 random seed로 다시 쓰는 것만으로 해결되지 않는가

FGKMT covering proof는 여러 nibble을 순서대로 진행한다. 한 nibble 안에서는 이전 상태를
고정하면 독립이지만, 앞선 선택이 다음 상태와 다음 확률분포를 바꾼다.

컴퓨터에서는 모든 단계에 독립 난수를 미리 배정해 같은 과정을 생성할 수 있다. 하지만
초기 난수 하나를 바꾸면 이후 상태 전체가 바뀔 수 있으므로, 출력이 조금만 변한다는 보장은
별도로 증명해야 한다. “입력 seed가 독립”과 “최종 함수의 한 좌표 민감도가 작다”는 다른
명제다.

## 7. 선행 concentration 정리 적용성

- Freedman 정리는 martingale increment의 절댓값과 conditional variance가 필요하다.
- Warnke와 Combes의 변형도 typical set에서의 구체적인 Lipschitz 경계를 요구한다.
- Kontorovich--Ramanan 경로는 의존성의 mixing coefficient가 필요하다.

현재 FMT/FGKMT source는 survivor cardinality를 제어하지만 weighted character observable의
위 입력들을 numerical constant와 cutoff로 주지 않는다. 그러므로 일반 정리의 이름을
인용하는 것만으로 DEP-R09를 닫을 수 없다.

## 8. 다음에 시도할 가치가 있는 경로

권장 순서는 다음과 같다.

1. **same-law conditional second moment — 최우선.**
   final sieve-good law에서 weighted error의 평균제곱을 직접 전개한다.
2. **character (L^2) energy 경로.**
   모든 character 변화의 제곱합을 finite Fourier/Parseval로 residue-count energy에 바꾸고,
   prime-error (\sum|Z_\chi|^2)와 결합할 수 있는지 본다.
3. **nibble martingale 경로.**
   2번이 실제 conditional increment와 variance를 줄 때만 Freedman형 정리를 적용한다.
4. **reserve randomization.**
   앞 경로가 실패할 때 coverage에 쓰지 않은 독립 residue를 남기는 구조변경을 검토한다.

1--3은 큰 소수 구간을 전수 계산하는 문제가 아니라 새 analytic inequality를 증명하는
문제다. 현재 사용자가 장시간 계산을 실행할 절차는 없다.

## 9. (X_{\rm cert})에 미치는 영향

분모의 논리 공백 하나는 고쳤지만, 분자 weighted-error moment가 아직 없다. 따라서

- <code>PAP-11</code>: OPEN
- <code>DEP-R09</code>: OPEN
- fixed (2\times10^{-17}): 프로젝트 독립 인증 아님
- numerical (X_{\rm cert}): OPEN
- 새 finite upper range: 없음

이다. 이 단계에서 threshold calculator나 장시간 prime sweep을 만들면 증명 공백을
계산으로 착각하게 되므로 보류하는 것이 타당하다.

## 10. 검증 증거와 한계

- native PDF text를 먼저 읽고 FMT printed p.13의 formula (6.17), FGKMT printed
  pp.83--84의 formulas (5.1), (5.7)--(5.9)를 원본 page image로 대조했다.
- exact Python 단위시험 11개가 denominator algebra, count sensitivity, (P=65) 반례,
  source hash·OPEN gate를 검사한다.
- 이 PASS는 finite algebra와 toy counterexample에 한정된다. analytic number theory
  theorem, final moment 또는 theorem threshold의 PASS가 아니다.

## 11. 참고문헌

- Ford--Maynard--Tao, *Chains of large gaps between primes*,
  [arXiv:1511.04468](https://arxiv.org/abs/1511.04468).
- Ford--Green--Konyagin--Maynard--Tao, *Long gaps between primes*,
  [doi:10.1090/jams/876](https://doi.org/10.1090/jams/876).
- Freedman, *On Tail Probabilities for Martingales*,
  [doi:10.1214/aop/1176996452](https://doi.org/10.1214/aop/1176996452).
- Warnke, *On the method of typical bounded differences*,
  [arXiv:1212.5796](https://arxiv.org/abs/1212.5796).
- Kontorovich--Ramanan, *Concentration inequalities for dependent random variables
  via the martingale method*,
  [arXiv:math/0609835](https://arxiv.org/abs/math/0609835).
- Combes, *An extension of McDiarmid's inequality*,
  [arXiv:1511.05240](https://arxiv.org/abs/1511.05240).
