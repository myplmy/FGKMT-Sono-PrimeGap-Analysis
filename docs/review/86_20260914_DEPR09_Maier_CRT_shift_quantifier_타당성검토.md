# DEP-R09 Maier/FMT CRT 이동량 양화사·동시 선택 타당성검토

- 작성일: 2026-09-14 KST
- 기술 정본:
  [Theory 78](../method/theory/78_Sono_FMT_DEPR09_Maier_CRT_shift_quantifier_audit.md)
- 판정:
  <code>중요 교정 / 고전 Maier y-평균안은 그대로는 부당 /
  FMT construction-vector 평균안은 조건부 연구가치 있음</code>

## 1. 쉬운 설명

고전 Maier 증명은 자물쇠 세 개의 조건을 동시에 만족하는 열쇠 \(y\)를 CRT로 만든다.
세 조건과 소수 구간 분할을 고정하면 열쇠는 하나뿐이다. 열쇠가 여러 개 있다고 생각하고
“평균적으로 좋은 열쇠가 있을 것”이라고 말할 수 없다.

현대 Sono/FMT 증명은 먼저 각 작은 소수마다 피할 나머지값을 여러 방식으로 고를 수 있다.
그 선택 묶음 하나마다 CRT 열쇠 \(m\)이 하나 생긴다. 따라서 **선택 묶음들의 가족**을
평균할 가능성은 있다. 하지만 다음 두 조건이 같은 묶음에서 성립해야 한다.

1. sieve 뒤에 필요한 숫자가 충분히 남고 짧은 구간에도 너무 몰리지 않는다.
2. 그 묶음의 소수분포 오차 상관이 작다.

각각 좋은 묶음이 존재한다는 말만으로는 부족하다. 두 조건을 동시에 만족하는 묶음이
적어도 하나 남는다는 수치 실패확률 합이 필요하다.

## 2. 사용자 지적과 오류 재발 감사

이번 단계 중 사용자가 지적한 Lean 곱셈 괄호 오류는 새 사건이 아니라 오류 원장 E117의
2026-09-13 사건이었다. 목표 <code>((18/7)*θ)*L</code>과 증명
<code>θ*((18/7)*L)</code>은 수학적으로 같은데 Lean에는 결합·교환 정규화가 명시되지 않아
첫 compile이 실패했다. E118, E119, E121에도 같은 넓은 유형의 초안 오류가 이어졌으므로
“이미 고친 한 줄”이 아니라 재발 유형으로 분류하는 것이 타당하다.

현재 예방책은 다음처럼 강화했다.

1. 새 정리는 작은 단위로 추가하고 바로 단일 Lean 파일을 compile한다.
2. 곱셈식 proof 경계에서
   <code>simpa only [mul_assoc, mul_left_comm, mul_comm]</code> 또는
   <code>convert ... using 1 &lt;;&gt; ring</code>으로 정규화한다.
3. 사용하지 않는 가정은 기본적으로 제거한다. source domain/interface를 의도적으로
   보존할 때만 이유를 주석으로 남기고 <code>_h...</code> 이름을 쓴다.
4. 문서의 <code>\varphi</code>, <code>\theta</code>가 JavaScript 문자열 escape로 control
   character가 되는 별도 재발도 발견해 저장소 정본 전체를 검사하는 자동 text-integrity
   gate를 추가했다.

이 조치는 수학 증명의 참·거짓을 대신하지 않지만, 같은 표면 문법 오류와 숨은 텍스트 손상이
후속 작업까지 전파되는 위험을 크게 줄인다.

## 3. Theory 77의 무엇을 고쳐야 하는가

Theory 77의 핵심인 direct weighted correlation 목표는 유지된다. 고쳐야 하는 부분은
그 목표를 만족하는 이동량을 고르는 표본공간이다.

- 고전 Maier fixed \(P_1,P_2,P_3\): \(y\bmod P(x)\)는 singleton이다.
- Sono/FMT: residue vector \(\boldsymbol a\)의 family가 있고, vector마다
  \(m(\boldsymbol a)\bmod P\)가 singleton이다.
- 따라서 평균을 쓸 경우 평균 변수는 임의의 연속 이동량 \(y\)가 아니라 FMT construction
  vector여야 한다.
- coefficient도 연속 block만이 아니라
  \(\mathcal T(\boldsymbol a)\)와 \(m(\boldsymbol a)\)의 결합형으로 다시 써야 한다.

이 교정은 Theory 77을 폐기하는 것이 아니라 열린 목표의 변수를 더 정확히 만든다.

## 4. 세 경로 비교

| 경로 | 필요한 새 입력 | 장점 | 위험·판정 |
|---|---|---|---|
| fixed Maier \(y\)에 직접 증명 | 그 한 CRT shift의 correlation 상계 | 양화사가 단순 | 현재 source 없음 |
| 모든 FMT vector에 uniform 증명 | vector-uniform correlation 상계 | 동시 선택 불필요 | 매우 강할 수 있음 |
| FMT vector 평균 + union bound | sieve-good·correlation-good 공통 수치 failure budget | uniform보다 약할 가능성 | construction proof 전체를 quantitative하게 다시 열어야 함; 1차 권장 감사 |

마지막 경로는 연구 가치가 있지만 아직 정리가 아니다. 특히 FMT proof가 사용하는
<code>1-o(1)</code>, Markov, Chebyshev, hypergraph 선택을 finite cutoff까지 복원해야 하고,
correlation 평균도 같은 probability law에 대해 증명해야 한다.

## 5. 현재 목표 도달도에 미치는 영향

이번 감사로 \(X_{\rm cert}\)의 수치 상한이나 하한은 전혀 바뀌지 않았다. 얻은 진전은
잘못된 평균 양화사로 수개월을 소비할 경로를 미리 차단하고, 실제 후보 표본공간을
FMT sieve-vector family로 교정한 것이다.

아직 남은 직접 병목은 다음과 같다.

1. construction-vector sieve-good event의 finite positive mass,
2. 같은 vector law에 대한 weighted correlation 평균,
3. 두 failure mass와 다른 endpoint/pair 실패를 합쳐 1 미만으로 만드는 slack,
4. 이후 R10--R12와 공통 cutoff.

이것들은 해석적 증명 문제다. 현재 사용자 PC에서 큰 소수 범위를 더 계산해도 이 빈칸을
닫지 못한다.

## 6. 최종 판정

“고전 Maier \(y\)들을 평균해 같은 좋은 \(y\)를 고른다”는 계획은 부당하다. fixed
partition에서 \(y\)는 하나뿐이다. 반면 Sono/FMT의 무작위 sieve vector를 표본공간으로
삼는 수정안은 논리적으로 타당하고, uniform correlation보다 약한 정리로 성공할 가능성이
있으므로 후속 source-first 감사를 수행할 가치가 있다.

다만 현재는 표본공간의 존재만 확인했을 뿐, numerical joint-good mass나 correlation
정리를 증명하지 않았다. 따라서 <code>PAP-11</code>, <code>DEP-R09</code>, fixed coefficient,
numerical \(X_{\rm cert}\)는 계속 <code>OPEN</code>이다.
