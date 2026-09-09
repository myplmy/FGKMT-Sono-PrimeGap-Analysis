# H1b-P92a weighted identity moment·growing dimension 타당성 검토

- 검토일: 2026-09-09 KST
- 정본 증명: [theory 44](../method/theory/44_Sono_FMT_H1bP92a_actual_identity_weighted_moment.md)
- 판정: ACTUAL IDENTITY CHILD EXPLICIT / GENERAL PACKAGE AND X_cert OPEN
- 성격: 기존 원문 연결부의 project finite proof 및 단기 toy 검산; 실제 소수 실험 아님

## 1. 쉬운 설명: 이번에 무엇을 확인했나

지난 H1c-1b.4e에서는 “소수들이 나머지류에 충분히 고르게 퍼져 있다”는 입력검사를
숫자로 표현했다. 이번에는 그 입력을 실제 sieve 가중합에 넣었다.

단순히 소수를 하나씩 세는 대신, 각 소수에 서로 다른 점수를 붙여 더한다고 생각하면 된다.
소수 개수가 조금 틀렸더라도 유난히 큰 점수를 가진 소수에서 틀리면 총점 오차가 커진다.
따라서 개수 오차가 작다는 사실만으로 총점 오차까지 작다고 할 수 없다.

이번 증명은 다음을 따로 처리한 뒤 합쳤다.

1. 나머지류별 소수 개수 오차에 점수를 붙였을 때의 오차.
2. 점수의 주항을 여러 좌표로 분해하고 재배치할 때 생기는 오차.
3. 곱 형태의 보정 계수들이 실제로 서로 약분되는지.
4. 구간 맨 왼쪽 소수를 포함했다가 제외할 때 빼야 할 **그 소수의 점수**.

예를 들어 왼쪽 소수의 점수가 82라면 총점에서는 1이 아니라 82를 빼야 한다.
기존 count endpoint 교정과 이번 weight endpoint 교정이 다른 이유다.

## 2. 얻은 것과 얻지 못한 것

| 대상 | 이번 판정 |
|---|---|
| actual identity \(L(n)=n\) weighted P9.2 | 상대/가법 오차 multiplier 1/1의 finite child |
| closed \([T,2T]\)에서 \((T,2T]\)로 이동 | weight atom과 main prime-count atom 모두 별도 제어 |
| 큰 차원의 profile integral 비교 | \(I(F_1)\le2I(F),J(F_1)\le2J(F)\), \(k\ge10^{50}\) |
| child 충분조건 | \(k\ge10^{200}\), \(X=2T\ge2\exp(10^{1000})\) |
| 일반 affine form·임의 집합의 P9.2 | 이번 actual child 범위 밖 |
| actual unweighted P91 | 미완료 |
| 기존 P94를 maximal growing dimension에 적용 | 별도 호환성 보완 필요 |
| 전체 good-weight·PAP·hypergraph·Sono threshold | 계속 OPEN |

여기의 거대한 수는 **소수를 그 수까지 직접 확인한 결과가 아니다.**
오차를 넉넉하게 상계한 증명이 적용되는 시작 조건이다.
현재 유한 데이터의 \(10^{20}\), \(X_{\rm emp}(10^{20})=3,814,280\), 이 child의 충분조건,
최종 \(X_{\rm cert}\)는 서로 다른 개념이다.

\(2\exp(10^{1000})\)까지 검사해야만 실제 부등식이 참이라는 의미도 아니다.
더 낮은 sufficient cutoff가 가능할 수 있고, 이번 수는 최적화를 하지 않은 안전한 선택이다.
전체 Sono 정리가 이 수부터 성립한다고는 아직 말할 수 없다.

## 3. 선행 원문 적용성 감사

- [Maynard 2016](https://doi.org/10.1112/S0010437X16007296), arXiv:1405.2593:
  pp.1540--1544, (9.16)--(9.38), Lemma 9.3.
- [FGKMT Long Gaps](https://doi.org/10.1090/jams/876), arXiv:1412.5029:
  Definition 2 p.95, Theorem 6 pp.98--99, actual identity call pp.101--102.
- 기존 교정 summation·scalar proof: theory 22--26.
- 기존 확률적 적분 proof: theory 13 H1a.

원문의 CRT와 local quadratic identities는 그대로 사용할 수 있다. 다만 원문의
\(O(\cdot)\) 계수를 1이라고 가정하지 않고 weighted multiplicity, Cauchy sum,
Euler factor, 재배치 오차를 직접 명시화했다.

공개 [PrimeGapsLib S2m error](https://github.com/AxiomMath/PrimeGapsLib/blob/main/PrimeGapsTheory/Sieve/S2m/Error/Main.lean)는
관련 방법을 보여 주지만 fixed dimension의 존재형 상수와 별도 분포 가정이 있다.
현재 \(k\)가 \(X\)와 함께 커지는 경로에 그대로 대입할 수 없으므로 input으로 채택하지 않았다.
이 판단은 그 프로젝트가 틀렸다는 뜻이나 전체 Lean dependency 감사를 했다는 뜻이 아니다.

## 4. 중요한 보완: “고정 차원에서 충분히 큼”과 “차원도 함께 커짐”

기존 \(2^k\) 적분 비교는 잘못된 부등식이 아니다. 예를 들어 \(k=36\)을 고정하면
\(2^{36}\)은 큰 상수일 뿐이므로 \(R\)을 충분히 키워 오차를 줄일 수 있다.

그러나 실제 경로는 \(k=\lfloor(\log T)^{1/5}\rfloor\)다.
\(T\)를 키울 때 \(k\)도 커지므로, 필요한 gate가 \(2^k\)에 비례하면
polynomial인 \(\log T\)가 그 손실을 따라잡지 못한다.
따라서 “각 고정 \(k\)마다 cutoff가 있다”와 “이 growing \(k(T)\) 경로에서 공통 cutoff가 있다”는
같은 말이 아니다.

H1a의 독립 확률변수·Cantelli 논증을 재사용하면 큰 \(k\)에서 cutoff로 잃는
적분량이 전체의 절반 미만임을 보일 수 있다. 그래서 비교 계수를 \(2^k\)가 아니라 2로 바꿨다.
그 결과 본 P92 child의 오차가 \(k\) 증가에 따라 충분히 감소한다.

기존 P94 fixed-parameter certificate와 실제 결과는 그대로 보존한다.
하지만 다음 단계에서 이 새로운 비교를 P94에 적용해 maximal growing dimension의
호환성을 별도로 닫아야 한다. 자동으로 해결된 것으로 표시하지 않았다.

## 5. 오차 합성 감사표

| 의무 | 사용한 명시식/계수 | 증명 위치 |
|---|---|---|
| 고정 modulus pair multiplicity | \(\tau_{3k}(q)\), multiplier 1 | theory 44 §6 |
| weighted discrepancy | \(\sqrt2N L^{-41k^2}\), 이후 \(d_k\mathcal A\) | §6 |
| positive smooth profile | \(\mathcal K_*=3000k^3(\log k)^2\) | §5 |
| scalar remainder | \(C_Y<10^{123}\), 원래 더 작은 상수도 보존 | §5, theory 26 |
| diagonal | \(4\delta+24k\varepsilon+24k^2\varepsilon^2\) | §7 |
| off-diagonal | \(248832 C_D k^3(\log k)^2(\log y)^2/y\) | §8 |
| 전체 상대오차 | \(10^{135}(\log k)^4/k^2\le L^{-1/10}\) | §9 |
| lower weight atom | \(w(T)/\mathcal A\le e^{-L/2}\) | §10 |
| main prime-count atom | \(\mathcal M(1)/\mathcal A\le e^{-L/2}\) | §10 |

sum of errors를 확인하지 않고 개별 작은 오차만 통과로 적지 않았다.
\((q,B)=1\), identity slot 제거, zero support extension, wide coordinate first,
closed/open endpoint도 유지했다.

## 6. 단기 검증 결과

새 전용 unittest 16개가 0.021초에 통과했다.

- exact rational local Euler cancellation과 별도 slot enumeration.
- 두 소수의 tensor row sum과 divisor pair multiplicity.
- harmonic divisor sum의 작은 정수 독립 전개.
- nonconstant weight를 사용한 closed/open endpoint toy.
- signed scalar remainder의 square-sum 부등식.
- 기존 profile norm·\(C_Y\)와 새 coarse majorant 교차검사.
- exact dimension bin의 양 끝과 반정수, float·bool·NaN 거부.
- 최소 dimension와 후속 dimension의 scalar check.
- source/dependency SHA-256, root 승격 금지.

첫 corner \(k=10^{200},L=10^{1000}\)의 scalar diagnostics는 다음과 같다.

| 양 | 검산값 |
|---|---:|
| smooth \(\delta\) upper | \(1.85077924882396365\times10^{-264}\) |
| scalar \(\varepsilon\) upper | \(2.19326107473033240\times10^{-667}\) |
| 합성 상대오차 식의 upper | \(1.25665136818785723\times10^{-258}\) |
| 더 보수적인 공통 upper | \(4.49761977182310514\times10^{-255}\) |
| 허용 상대오차 | \(10^{-100}\) |

코드는 실제 \(T=\exp L\)를 만들지 않고 exact bin 검사 후 내부 1,062 decimal digits로
작은 수의 식만 계산했다. 32개 scalar/rational gate를 통과했지만,
이 수치 표본이 모든 \(k\)에 대한 증명을 대신하는 것은 아니다.
최종 표적 49개는 0.044초, 전체 434개는 62.520초에 PASS했다.
py_compile, 변경 텍스트 20개 제어문자·수식 구분자 검사, JSON 4개 parse,
local link 126개와 git diff --check도 통과했다. 초기 통합검사의 schema·모듈명 실패와
최종 교정은 오류 원장 E065--E067 및 완료 작업원장에 숨기지 않고 기록했다.
자동검사는 project proof의 독립 심사나 Lean 인증을 대체하지 않는다.

## 7. 연구 방향과 다음 권장 순서

| 순서 | 작업 | 근거 | 계획용 예상 소요 |
|---|---|---|---|
| 1 | H1b-P91a actual unweighted moment | weighted P92와 짝을 이루는 normalization 분모가 남음 | 문헌·증명·검산 1--3시간 |
| 2 | P94 growing-dimension gate 교정 | fixed-k의 exponential gate를 그대로 사용할 수 없음 | 1--3시간 |
| 3 | actual dependency 가지치기와 \(\mathfrak S,\tau,u\) 합성 | 필요하지 않은 일반 정리에 시간을 쓰지 않고 root 연결부를 닫기 위함 | 2--6시간 |
| 4 | 남은 PAP/UB·hypergraph rate | 최종 \(X_{\rm cert}\)를 결정하는 별도 핵심 의무 | 원문 감사 후 재산정 |

시간은 사람/에이전트의 조사·증명 작업에 대한 계획 추정이지 사용자 PC의 CPU runtime
보장이 아니다. 수학적 장애가 생기면 더 걸릴 수 있다. 각 단계의 예상 자동검사는 수초--수분이다.
현재는 추가 prime sweep이나 3--12시간 CPU job을 실행할 근거가 없다.

FGKMT Theorem 6의 표시된 proof는 P91/P92/P94/L85를 직접 인용한다.
P95는 general Maynard P61 목록에 있다는 이유만으로 actual 경로의 필수 gate로 취급하지 않고,
후속 FMT/Sono까지의 사용처를 조사해 필요 여부를 판정하는 것이 효율적이다.

사용자가 지금 수행할 명령은 없다. **별도 수행절차 필요없음.**
새 package, Lean, 원문 전달 요청도 현재 없다.
장시간 계산이나 필요한 원문·설치가 실제로 필요해질 때 별도로 요청한다.
