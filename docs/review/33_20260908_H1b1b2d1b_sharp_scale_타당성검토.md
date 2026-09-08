# H1b-1b-2d.1b sharp \(\xi\log x\) scale 비판적 타당성 검토

- 검토일: 2026-09-08
- 대상: Maynard Proposition 9.4의 (9.58), (9.66)과 FGKMT/FMT의 실제 호출
- 판정: **하위문제는 타당하게 닫힘. 상위 numerical threshold는 계속 미완성**
- 정식화: [theory 27](../method/theory/27_Sono_FMT_H1b1b2d1b_sharp_xi_logx_scale.md)

## 1. 검토 질문과 짧은 답

### 질문 1. 최종 출판본의 숨은 \(\ll\) 상수를 1로 써도 되는가?

아니다. arXiv v2 TeX/HTML에는 계수 1의 하한이 보이지만 최종 출판본은
\(k(\log\log x)^2/\log x\ll\xi\)라고 인쇄했다. 출판본을 우선하고 숨은 상수는
미확정으로 취급해야 한다.

### 질문 2. 그러면 두 sharp 합은 계속 막혀 있는가?

아니다. FGKMT/FMT는 실제 호출에서 \(\xi=\theta/10\)을 선택한다.
Maynard의 \(R\le x^{\theta/3}\)와 합치면
\(\xi\log x\ge0.3\log R\)가 exact하게 나온다. 앞서 explicit하게 복원한
strict summatory error를 여기에 직접 적용하면 두 호출 모두 finite gate로 닫힌다.

### 질문 3. 이것으로 Sono 부등식의 최소 시작점이 나오는가?

아니다. 이는 Maynard weight 계산의 두 작은 합만 닫는다. 다른 moment 오차,
Hypothesis 1의 prime-distribution 상수, FMT 확률 단계와 arbitrary-\(X\) 연결이 남아 있다.

## 2. 타당한 점

1. **실제 호출을 사용한다.** 자유로운 \(\xi\)에 임의 하한을 만들지 않고 FGKMT가
   명시한 \(\xi=\theta/10,D=1\)을 사용했다.
2. **방향이 정확하다.** \(R\le x^{\theta/3}\)에서 얻는 것은
   \(\xi\log x\ge(3/10)\log R\)이며, 오차분모의 lower bound로 올바르게 작동한다.
3. **끝점이 보정됐다.** 원문 합은 \(d<x^\xi\)이므로 non-strict
   \(C_\Sigma\)가 아니라 \(C_\Sigma+2\)를 쓴다.
4. **두 용도를 따로 닫는다.** (9.58)은 양의 lower bound,
   (9.66)은 upper factor가 필요하다. 같은 \(\delta\le1/2\)가 각각
   \(1/2\)와 \(3/2\) factor를 준다.
5. **선행 package의 범위를 보존한다.** actual local family, 제외모듈
   \(\Lambda_*\), smooth factor는 새로 추측하지 않고 theory 21--24의 검증된
   계약을 재사용한다.

## 3. 이번 검토에서 잡힌 오류

기존 theory 24 식 (24.16)과 `sharp_cutoff_relative_error`는 strict cutoff인데도
\(C_\Sigma\)만 썼다. 정확한 값은 \(C_\Sigma+2\)다. 수치상 \(C_\Sigma\)가
약 \(10^{121}\)이라 차이는 매우 작지만, 엄밀성에는 크기와 무관하게 오류다.

또한 보통의 50--80자리 부동소수 정밀도에서는 \(10^{121}\)에 2를 더한 차이가
표시되지 않는다. 구현은 `mp.fadd(..., exact=True)`로 저장된 `mpf` 근사값에
endpoint allowance가 실제로 남도록 했고, 시험은 그 차이가 정확히 2인지 확인한다.
다만 전체 지수함수 평가는 directed interval arithmetic가 아니므로, 보고된 소수점은
증명 그 자체가 아니라 진단값이다.

## 4. 남아 있는 위험과 제한

### 4.1 source의 lower-scale 사용처

author TeX에서 해당 lower-scale 문구의 명시적 사용은 (9.58), (9.66) 두 곳이다.
그러나 Proposition 9.4 proof에는 “앞 증명과 동일하게 negligible” 같은 별도 문장이 있다.
이번 결과는 그 다른 숨은 상수를 닫았다고 주장하지 않는다. 따라서 Proposition 9.4
전체의 수치화가 아니라 **두 sharp summatory factor의 수치화**로만 기록하는 것이 맞다.

### 4.2 \(H1B-L84\)와 parent의 구분

선행 theory 24--26과 이번 결과를 합치면 추적된 Lemma 8.4 관련 actual
subapplication 9개는 모두 parameterized explicit이다. 이에 따라 `H1B-L84` 상태는
올릴 수 있다. 그러나 required main term과 error envelope의 전체 비교는
`H1B-COMP-01`과 Propositions 9.1--9.5 쪽 의무다. 이를 함께 올리면 과장이다.

### 4.3 설명용 cutoff의 크기

\(k=36,\alpha=2,\theta=1/3\)에서 충분조건은
\(\log R\approx2.99\times10^{125}\)이다. 이는 매우 보수적이고 실용적 계산범위를
뜻하지 않는다. 더구나 \(\log R\)를 곧바로 최종 \(X\)로 읽을 수 없다.

### 4.4 수치 최적화의 우선순위

현재 sharp gate는 기존 smooth/scalar gate보다 지배적이지 않다. 따라서 이 상수만
날카롭게 줄여도 최종 threshold가 바로 줄어들 가능성은 낮다. 우선은 열린 root
dependency를 찾고 닫는 편이 연구 효율이 높다.

## 5. 선행연구 조사 판정

- Maynard 최종본은 구조와 두 사용처를 주지만 numerical multiplier는 주지 않는다.
- FGKMT 최종본은 실제 \(\xi,D,\alpha,\theta,R\) 선택을 준다.
- theory 22에서 채택한 corrected \(\kappa=1\) theorem이 strict cumulative
  multiplier를 이미 제공한다.
- 이 세 입력을 현재 정규화로 한꺼번에 결합한 별도 peer-reviewed numerical lemma는
  표적 검색에서 찾지 못했다. 이는 전 세계 novelty 주장이 아니다.

따라서 사용자 제안인 “먼저 적합한 선행증명을 찾고, 없는 연결부만 직접 증명” 방식이
이번 경우에도 타당했다. 직접 증명한 부분은 (27.1)과 closed-form gate의 짧은 연결뿐이다.

## 6. 최종 판정

~~~text
두 sharp xi*log(x) factor         CLOSED (project finite component)
actual Lemma 8.4 subapplications  9/9 parameterized explicit
H1B-L84                           ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
H1B-COMP-01                       HARD_BLOCKER
SIV-07 / SIV-09                   HARD_BLOCKER
X_cert                            OPEN
~~~

다음 우선순위는 두 갈래다.

1. `H1b-2`: Lemmas 8.5--8.6 및 Proposition 9.4의 남은 error를 시작으로
   공통 moment budget을 만든다.
2. `H1c-1`: Hypothesis 1(2)에 필요한 character/Bombieri--Vinogradov 수치 package를
   독립적으로 복원한다.

두 갈래 모두 계산시간보다 문헌·증명 상수 복원이 병목이다. 실제 prime sweep이나
장시간 사용자 실험을 지금 추가하는 것은 이 blocker를 줄이지 않는다.

## 7. 사용자 수행사항

별도 수행절차 필요없음. Lean 또는 추가 Python 라이브러리 설치도 현재 단계에는 필요하지 않다.

