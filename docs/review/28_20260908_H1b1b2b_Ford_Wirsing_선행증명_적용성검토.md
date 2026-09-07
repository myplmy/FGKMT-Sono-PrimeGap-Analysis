# H1b-1b-2b Ford 교정 Wirsing 정리 선행증명 적용성 검토

- 검토일: 2026-09-08
- 대상: Kevin Ford, *Sieve Methods Lecture Notes, Spring 2023*, Theorem 4.4
- 관련 출처: GGPY Lemmas 3--4, Castillo et al. Lemma 2.5, Kuperberg Lemma 4.3,
  Dusart Theorems 6.10--6.12
- 상세 정식화:
  `docs/method/theory/22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md`
- 최종 판정: `APPLICABLE_AFTER_KAPPA1_EXPLICIT_REDERIVATION`

## 1. 질문

기존 계획은 Castillo 등의 교정을 따라 \(c_\gamma\) 없는 절대오차 상수
\(C_{3,\mathrm{abs}}(A_1,A_2)\)를 먼저 복원한 뒤, 별도로 증명한
\(c_\gamma\) 하한으로 상대오차를 되찾는 것이었다. Ford의 Theorem 4.4가 이보다 직접적인
선행증명을 제공하는지 검토했다.

## 2. 핵심 판정

제공한다. 단, 원래 인쇄식 그대로가 아니라 누락된

\[
c_\gamma(L+1)^\kappa
\]

항을 포함한 교정식이다. Ford는 이 항이 빠진 원인을 HR proof의 역수 전개에서 smallness를
확인하지 않은 데까지 추적하고, 작은 \(x\)에서 이 항이 실제로 필요함을 반례형 예제로
보인다.

현재 적용은 \(\kappa=1\)이므로 Ford의 두 오류항

\[
c_\gamma\{(L+1)(\log x)^0+(L+1)^1\}
\]

이 같은 크기로 합쳐진다. 따라서 actual application의 \(c_\gamma\) 하한으로 나누지 않고도
Maynard Lemma 8.3에 필요한 상대오차를 복원할 수 있다.

## 3. 그대로 채택하지 않은 이유

Ford 자료는 저자 공개 강의노트이며 peer-reviewed 논문으로 확인되지 않는다. 또한 정리의
multiplier는 \(O_{\kappa,A_1,A_2}\)에 숨겨져 있다. 그러므로 다음 두 조치를 취했다.

1. GGPY, Castillo, Kuperberg와 식·가정·오류 정규화를 교차 대조했다.
2. Ford proof의 recurrence와 tail 분기를 \(\kappa=1\)에 한정해 explicit prime-sum
   부등식으로 다시 전개했다.

그 결과 보수적인

\[
C_\Sigma(a,A)=40960D(a,A)e^{256+A}
\]

와 모든 \(x\ge2\)의 범위를 얻었다. 이 상수는 sharp하지 않지만 proof certificate에
사용 가능한 명시식이다.

## 4. 기존 Castillo 판정과 모순되는가

모순되지 않는다. Castillo 등은 GGPY/Maynard에 인쇄된 더 강한 형태가 원래 proof에서
정당화되지 않았다고 지적했다. Ford는 그 지적의 원인인 작은 \(x\) 구간을 버리지 않고
추가 항을 넣어 정리를 고친다. 즉,

- “인쇄된 식이 그대로 증명됐다”는 주장은 계속 금지한다.
- “교정항을 넣은 \(\kappa=1\) 상대오차”는 별도 proof로 사용할 수 있다.
- 일반 \(\kappa\)에서 추가 항을 생략하는 것도 계속 금지한다.

## 5. 프로젝트 영향

- legacy 절대 \(C_{3,\mathrm{abs}}\)+\(c_\gamma\) 하한 경로는 오류가 아니라
  optional cross-check 경로로 남긴다.
- primary route는 교정된 Ford--Wirsing \(\kappa=1\) 상대오차로 바꾼다.
- Lemma 8.3의 abstract multiplier와 \(z\ge2\) 범위는 parameterized explicit로
  승격할 수 있다.
- 실제 Maynard 호출의 공통 \(a,A,L\), Lemma 8.4의 \(r\)-회 합성, 다른 H1b/H1c root가
  남아 있으므로 `SIV-07`과 \(X_{\rm cert}\)는 닫히지 않는다.

## 6. 문헌 우선 방식에 대한 비판적 결론

사용자가 제안한 “먼저 선행증명을 찾고 없을 때만 직접 증명” 방식은 타당하다. 이번에는
실제로 전체 recurrence를 처음부터 재발명하는 일을 줄였다. 다만 다음 조건이 없으면 위험하다.

- 같은 기호가 같은 parameter인지 확인할 것. 이번에는
  \(A_1^{\rm GGPY}=1/a^{\rm Maynard}\)다.
- endpoint, norm, uniformity, finite range를 대조할 것.
- peer review 여부와 proof 공개 여부를 분리할 것.
- 숨은 \(O\)-상수는 선행정리 이름만으로 숫자가 되지 않는다.
- 여러 논문을 합칠 때 전달 부등식을 따로 증명할 것.

따라서 앞으로도 `선행 source 탐색 → 적용성 표 → 부족한 최소 lemma 직접증명` 순서를
사용하되, 단순 유사성만으로 채택하지 않는다.

## 7. 출처

- Ford notes: <https://ford126.web.illinois.edu/sieve2023.pdf>, pp. 47--51.
- Dusart: <https://arxiv.org/abs/1002.0442>, pp. 10--12.
- Castillo et al.: <https://lemkeoliver.github.io/papers/11-BoundedGaps.pdf>, p. 11.
- Kuperberg: <https://arxiv.org/abs/2210.09775>, pp. 16--19.
