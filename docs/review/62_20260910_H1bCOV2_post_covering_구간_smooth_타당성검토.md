# H1b-COV2 post-covering 구간·smooth remainder 타당성 검토

- 작성: 2026-09-10 KST.
- 검토 대상: [theory 55](../method/theory/55_Sono_FMT_H1bCOV2_post_covering_interval_smooth_composition.md)와
  [machine contract](../method/theory/data/Sono_FMT_H1bCOV2_post_covering_v1.json).
- 판정: `DEP-R08 ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`.
- 비판정: Sono 전체 정리, broad `SIV-07/08/09`, 최종 coefficient budget,
  \(X_{\rm cert}\), 독립 형식 인증.

## 1. 쉬운 결론

이번 단계는 “한 구간에서는 대략 맞는다”라는 논문 속 점근 문장을, 우리가 실제로 필요한
유한 개 구간에서 **한 번에 성공하는 수치 조건**으로 바꿨다.

비유하면 다음과 같다.

1. 길 전체를 무한히 많은 위치에서 따로 검사하지 않고, 미리 고정한 같은 길이의 칸으로 나눈다.
2. 각 칸에서 남는 소수 후보 수가 예상값에 가깝다는 사건을 한꺼번에 잡는다.
3. 검사 전에 잠시 제외했던 예외점도 실제 칸의 크기에 맞는 비용을 내고 되돌린다.
4. sieve로 설명되지 않는 smooth 수들도 “무시할 만큼 작다”가 아니라 숫자로 상계한다.

그 결과 covering 부분의 마지막 actual 연결 `R08`은 닫혔다. 그러나 아직 소수분포 PAP,
두 소수가 동시에 소수일 때의 upper-bound sieve, 전체 오차를 Sono의 같은 계수 안에 넣는 일,
보조변수에서 최종 \(X\)로 옮기는 일이 남았다. 즉 주소를 계산할 준비가 한 단계 진전했지만
아직 \(X_{\rm cert}\) 주소를 출력할 수는 없다.

## 2. 원문을 그대로 숫자로 바꾸면 생기는 두 문제

### 2.1 interval cell 개수의 작은 끝점 위험

Sono의 proof는 폭이 \(\varepsilon/2\)와 \(\varepsilon\) 사이인 cell을 사용한다. printed 문장을
그대로 cell 개수 공식으로 읽으면, 아주 짧은 구간이 cell 경계를 걸칠 때 “한 칸”이라고
계산하지만 실제로는 두 칸과 만나는 경우가 생길 수 있다.

theory 55는 이를 오류라고 단정해 원문 결론을 버리지 않는다. 대신
\(J=\lceil2/\varepsilon\rceil\)개의 동일 길이 cell을 사용하고, 양 끝에서 각각 한 칸씩 늘어나는
최악의 경우를 직접 더했다. 그러면 덮은 총 길이는 항상
\[
 (\beta-\alpha)+2/J\le(\beta-\alpha)+\varepsilon
\]
이다. 원래 목표 \(2(\beta-\alpha)+\varepsilon\)보다 강하므로 결론과 계수 방향을 보존한다.

### 2.2 `1 << 80c/A`는 숫자 1보다 크다는 뜻이 아님

수론 논문에서 `1 << t`는 보통 “\(t\)가 어떤 양의 상수보다 크다”는 Vinogradov 표기다.
이를 \(t>1\)로 읽거나 숨은 상수를 임의로 1로 놓으면 안 된다. 실제로 필요한 것은
\(m=\lfloor\log_5(80cb/A)\rfloor\)가 양수이고 허용범위 안이라는 사실이다.

이번에는 정확한 충분조건
\[
 80cb/A\ge5
\]
를 사용했다. 그러면 \(m\ge1\), \(A\le A'<5A\),
\(m<\log_3X/\log5\)가 floor 정의만으로 나온다. 숨은 상수를 추측하지 않는다.

## 3. 가장 큰 실제 개선: 예외 복원비

이전 [theory 53 §7](../method/theory/53_Sono_FMT_H1bCOV1_full_residue_hypergraph_interface.md)은
모든 큰 subset에 공통으로 쓸 수 있는 느슨한 복원비 \(8000/\sqrt b\)를 남겼다.
현재 child의 \(b\) 부근에서는 이것이 작지 않아 최종 구간 분석에 바로 쓸 수 없었다.

이번에는 각 cell 폭 \(h\)를 실제로 넣어
\[
 e_{\rm cell}\le\frac2{(1-r_0)Ahb}<\frac7{A\varepsilon b}
\]
를 얻었다. \(A,\varepsilon\)는 고정 상수이므로 \(b=\log_2X\)가 커질수록 \(1/b\)로 감소한다.
예외점 수를 줄인 것이 아니라, 그 예외점이 실제 cell 주항에서 차지하는 비율을 정확히
계산한 것이다.

## 4. 확률을 잘못 합치지 않았는가

독립이라고 가정하지 않았다. 순서는 다음과 같다.

1. residue vector의 outer 실패율 \(F_{\rm out}<1\)이면 good vector 하나가 존재한다.
2. 그 vector를 고정한 뒤 생긴 유한 subset family에 대해 conditional inner 실패율
   \(F_{\rm in}<1\)이면 good covering 하나가 존재한다.
3. smooth remainder는 확률사건이 아니라 결정론적 개수 상계다.

따라서 outer와 inner가 독립이라거나 \(F_{\rm out}+F_{\rm in}<1\)이라고 주장하지 않는다.
결과를 본 뒤 가장 유리한 subset을 새로 골라 fixed-subset 정리를 재사용하지도 않는다.

## 5. smooth remainder 직접 증명의 타당성

선행 자료를 먼저 찾았지만, 확인한 명시 bound는 이 변수에서 필요한 감쇠보다 약했고 sharp
\(u\log u\) 형태에는 여전히 implied constant가 남았다. 그래서 일반 smooth-number 정리를
새로 증명하려 하지 않고 actual FMT parameter에 한정해 Rankin 부등식을 사용했다.

핵심은
\[
 \Psi(Y,z)\le Y e^{-uw}\prod_{p\le z}(1-p^{-(1-\delta)})^{-1}
\]
에서 Euler product 증가분을 정확히 세는 것이다. 사후감사에서 초안의 적분 구간 설명이
충분히 엄밀하지 않음을 발견해 교정했다. Rosser–Schoenfeld Theorem 9의 전 범위
\(\vartheta(t)<1.01624t\)와 감소함수 Stieltjes 부분적분을 직접 결합하면
\[
 \sum_{p\le z}\frac{p^\delta-1}{p}
 \le\frac{21}{20}\{\delta+\operatorname{Ein}(w)\}
 <\frac{189}{160}u
\]
가 된다. \(\operatorname{Ein}(w)\)는 두 구간으로 나눠
\(103e^w/(100w)\) 이하임을 증명했다. 이 보정 뒤에도 기존 최종 상수 여유는 유지된다.
매우 보수적인 gate \(b\ge e^{200}\) 아래
\[
 \#R<\frac{\log b}{17b}\frac X{\log X}
\]
를 얻었다. \(B_0\)의 모든 거듭제곱 수도 포함했다.

장점은 hidden \(O\)가 사라진다는 점이다. 단점은 cutoff가 매우 크고 최적화되지 않았다는 점이다.
현재 목적은 “가장 작은 숫자”가 아니라 먼저 오류 없이 유효한 finite path를 만드는 것이므로
타당한 선택이다. 나중에 \(X_{\rm cert}\)의 지배항으로 드러날 때만 더 강한 published explicit
smooth-number theorem이나 정밀한 직접 bound로 교체하는 편이 효율적이다.

## 6. 무엇을 증명했고 무엇을 증명하지 않았는가

| 주장 | 현재 판정 |
|---|---|
| 고정 \(\varepsilon\)의 endpoint-safe finite grid | 증명 |
| \(m,A'\)의 floor·범위 | 명시 gate 아래 증명 |
| 실제 cell의 예외복원 비용 | 증명 |
| 한 residue·covering 선택의 순차 존재 | 두 explicit 실패율이 각각 1 미만일 때 증명 |
| smooth remainder의 actual one-sided bound | 명시 gate 아래 project proof |
| `DEP-R08` | parameterized explicit |
| 실제 최종 \(A,\varepsilon,\eta\) | 아직 선택하지 않음 |
| 같은 Sono 계수의 전체 오차 budget | OPEN (`DEP-R11`) |
| PAP·two-prime UB | OPEN (`DEP-R09`, `DEP-R10`) |
| 모든 최종 \(X\)로의 transfer | OPEN (`DEP-R12`) |
| numerical \(X_{\rm cert}\) | OPEN |

`parameterized explicit`은 “식에 숨은 상수가 없고 정해진 parameter를 넣으면 검사할 수 있다”는
뜻이다. “현재 모든 parameter를 넣어 최종 숫자까지 계산했다”는 뜻이 아니다.

### 6.1 Lean 형식검증으로 다시 나눈 증거 경계

2026-09-10 후속 감사에서는 [단일 Lean 파일](../../lean/FGKMTSono/TheoryVerification.lean)과
[전수 검증 원장](../../lean/VERIFICATION_LEDGER.md)을 사용해 식 (55.24)--(55.35)를 다시
나눴다.

| 범위 | Lean 판정 | 뜻 |
|---|---|---|
| (55.32), (55.34), 기존 (55.33) | `KERNEL_PASS` | 실제 \(q,b,u,w\) 조건에서 로그 하계·유리수 여유·감쇠 결론을 proof escape 없이 검사 |
| (55.24), (55.25), (55.29)--(55.31), (55.35) | `CONDITIONAL_KERNEL_PASS` | 적어 둔 source premise가 참이면 뒤의 지수·로그·상수 합성이 맞음을 검사 |
| (55.26) | `KERNEL_PASS` | \(S_\delta\), \(h(t)\)를 정의하고 \(t>0,t\ne1\)에서 const-rpow 미분과 FTC로 \(h(t)=\int_0^\delta t^{v-1}dv\)를 검증 |
| (55.27) | `PARTIAL_FORMALIZATION` | finite prime-sum 정규화, \(h(1)=\delta\), \(1.01624<21/20\), 종단 Ein 치환은 검증; Rosser--Schoenfeld theta bound와 Stieltjes/Abel 비교는 외부 premise |
| (55.28) | `KERNEL_PASS` | 0의 removable singularity를 continuous extension·AE equality로 처리하고 두 finite interval 비교와 improper integral 상계를 전체 검증 |
| untagged Ein \(103/100\) bound | `KERNEL_PASS` | 정확한 interval split과 (55.28)을 합성해 \(w\ge100\)에서 최종 상계를 검증 |

특히 \(2^{-3/4}<3/5\), \(w\ge100\)에서의 half-tail, improper integral
\(\int_0^\infty e^{-t}(1+2t/w)\,dt=1+2/w\)뿐 아니라, 날것의
\((e^v-1)/v\)가 \(v=0\)에서 정의되지 않는 문제도 연속 확장과 거의 모든 곳
동치로 처리했다. 이제 (55.29)는 Ein 상계를 외부 premise로 받지 않고 이 커널
정리를 내부에서 쓴다.

반면 고정 Mathlib에는 `Chebyshev.theta`와 Abel summation 기반은 있지만,
필요한 Rosser--Schoenfeld \(\vartheta(t)<1.01624t\) 전 범위 정리는 없다. 현재
제공되는 즉시 사용 가능한 상계는 \(\vartheta(t)\le(\log4)t\)로 상수가 더 크다.
따라서 (55.27)을 완전 `KERNEL_PASS`로 올리려면 Rosser--Schoenfeld 정리의
finite verification을 포함한 별도 형식화와 그 상계를 감소 kernel에 적용하는
Stieltjes/Abel lemma가 필요하다. 이를 `axiom`, `sorry`, `admit`으로 우회하지 않았다.
그러므로 이번 보강은 project proof의 적분·endpoint·상수 전사 오류 위험을
크게 줄였지만, 제6절의 `DEP-R08` 판정이나 \(X_{\rm cert}\) 상태를 더 강하게
만들지는 않는다.

## 7. 검증 코드의 역할과 한계

[helper](../../source/h1bcov2_post_covering.py)는 `Fraction`으로 equal-grid, floor, 복원식과
순차 union bound를 검산한다. [tests](../../tests/test_h1bcov2_post_covering.py)는 특히 아주 짧은
crossing interval이 실제로 두 cell과 만나는 사례를 포함한다.

이 검사는 식의 전사 오류·부등호·반올림 실수를 찾는 장치다. 거대한 소수를 생성하지 않으며,
analytic proof 전체를 자동 증명하지 않는다. actual experiment나 연구 result를 생성한 것도 아니다.

## 8. 다음 권장 작업

다음은 `DEP-R09 numerical PAP`다. Sono가 쓰는
\(C_{\rm PAP}=1-e^{-2}\), \(D_{\rm PAP}=160\)이 실제 interval·exceptional modulus에서
어느 숫자부터 유효한지 source별로 연결해야 한다. 그 뒤 `DEP-R10` two-prime UB,
`DEP-R11` 같은 coefficient의 총 오차, `DEP-R12` final-variable transfer 순서가 맞다.

현재 사용자 PC에서 돌릴 actual 계산은 없다. PAP 원문 추적 중 새 논문 원문이나 라이브러리가
꼭 필요해지면 먼저 필요성과 사용법을 설명하고 사용자에게 요청해야 한다.
