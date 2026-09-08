# H1b-1b-2d.1a.1 scalar remainder 수치 재증명 타당성 검토

- 작성일: 2026-09-08
- 검토 대상: Maynard 최종 출판본 (9.42)--(9.48)의 숨은 scalar multiplier와 finite range
- 정식화:
  [26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md](../method/theory/26_Sono_FMT_H1b1b2d1a1_scalar_remainder.md)
- 기계 계약:
  [Sono_FMT_H1b1b2d1a1_scalar_remainder_v1.json](../method/theory/data/Sono_FMT_H1b1b2d1a1_scalar_remainder_v1.json)

## 1. 최종 판정

\[
\boxed{\texttt{VALID AS A PARAMETERIZED FINITE SUBPACKAGE}}
\]

다만 이 판정의 범위는 line 905 square-sum 우회에 들어가는 scalar remainder 하나다.

\[
C_Y=
327680\frac{14801}{69}e^{264}+10\,143\,697
<3.17\times10^{122}
\]

와 충분조건 finite gate를 얻었으므로, 이전의 “source scalar multiplier OPEN”은 이
하위 package 안에서는 닫을 수 있다. 반면 두 sharp \(\xi\log x\) 호출은 아직
수치화되지 않았으므로 다음 상태를 유지해야 한다.

~~~text
H1B-L84      RATE_MISSING
H1B1-PACKAGE HARD_BLOCKER
SIV-07       HARD_BLOCKER
X_cert       OPEN
~~~

## 2. 무엇이 타당한가

### 2.1 문헌을 먼저 쓰고 직접 증명을 최소화했다

prime log sum과 totient 상계는 Rosser--Schoenfeld의 명시식을 그대로 썼다. Maynard
식의 정확한 구조는 최종 출판본을 따랐고, one-step partial summation은 앞서
peer-reviewed 교정을 반영해 복원한 multiplier를 재사용했다. 직접 증명한 것은 이 세
결과 사이에 남아 있던 \(s\)-배치, \(t\)-divisor, determinant, prefactor와 profile
연결부뿐이다.

표적 검색으로 동형의 완성된 수치 lemma를 찾지 못했다는 것은 “그런 논문이 전혀 없다”는
주장이 아니다. 현재 package에 필요한 가정과 정규화를 실제로 충족하는 source를 찾지 못했다는
좁은 기록이다.

### 2.2 gcd를 버리는 순서가 교정됐다

원문은 \((s,t)=1\)을 버린다고 짧게 서술한다. 수치 재증명은 먼저 이 조건 아래
\(\varphi_\omega(st)\)를 분리하고 나서 \(s\)-합만 확장한다. 분모가 아직 결합된 상태에서
gcd 조건부터 버리는 잘못된 상계는 사용하지 않았다.

### 2.3 \(t\)-합이 exact identity로 환원된다

divisor 전수합은

\[
P_D\left(1+\sum_{p\mid D}\frac{\log p}{p-\omega(p)+1}\right)
\]

로 정확히 환원된다. 코드는 세 소수 toy에서 모든 부분집합을 독립 열거해 상수항과 각
\(\log p\) 계수를 유리수로 대조한다. 따라서 수치 sampling으로 조합 누락을 가리는 방식이 아니다.

### 2.4 prefactor cancellation은 공유 소인수에도 안전하다

\((a_m,r)>1\)일 수 있다는 점을 별도로 검사했다. 필요한 조건은 원문의
\((r,WB)=1\)이고, 이 조건 아래 totient와 \(\varphi_L\) 인자는 prime-by-prime 정확히 1로
지워진다. 남는 local product만 \(36/35\)로 상계했다.

### 2.5 direct derivative는 support rescaling을 명시했다

Lemma 8.3을 \(z=R^{U_k}\)에 적용하면 test function은 \(G(U_kv)\)가 된다. 따라서
\(|G|+U_k|G'|\)가 정확한 norm이다. 이 rescaling 없이 원래 변수의 derivative를
그대로 \(T_k\) 이하라고 두면 틀릴 수 있다. 정식화는 이 지점을 식 (26.17)에 명시했다.

## 3. source 정정 감사

구 author TeX 986행에는

\[
\prod_{i=1}^{k}(a_mb_i-a_ib_m)
\]

가 있어 \(i=m\) 항 때문에 0이 된다. 그러나 최종 출판본 1545쪽 식 (9.43)은 이미
\(i\ne m\)으로 고쳐져 있다. 따라서 이전 theory 25/review 31에서 이를 “인쇄식의
ambiguity”로 표현한 것은 부정확했다.

이번 감사에서는 다음 원칙으로 교정한다.

- 최종 출판본을 권위 원천으로 사용
- author TeX는 검색 보조자료로만 사용
- 서로 다르면 출판본 수식을 렌더링해 직접 대조
- 과거 정본·JSON·오류 원장에 정정 사실을 함께 기록

이 정정은 계산 결과를 바꾸지 않는다. 직전 단계는 scalar 상수를 OPEN으로 남겼고
잘못된 determinant를 실제 수치 계산에 사용하지 않았기 때문이다.

## 4. 상수의 보수성과 실제 의미

\(C_Y\)의 거의 전부는 교정된 Lemma 8.3의 매우 큰 보수적 multiplier다. YmError의
\(10\,143\,681\)은 \(10^{122}\) 규모의 direct branch와 비교하면 사실상 보이지 않는다.
이는 증명이 유효하지 않다는 뜻은 아니지만 다음 두 사실을 뜻한다.

1. 이 상수로 얻는 threshold는 현실적인 prime 계산 범위와 비교할 수 없을 만큼 커질 수 있다.
2. 나중에 \(X_{\rm cert}\)를 낮추려면 algebraic 소수항보다 Lemma 8.3 multiplier를
   날카롭게 하는 연구가 훨씬 영향이 크다.

예시 \(k=36,\alpha=0.01,\theta=0.25\)에서 \(\log R\) 충분조건도 약
\(1.17\times10^{132}\)이다. 이는 \(X_{\rm cert}\)가 아니라 이 하위 부등식만 안전하게
만드는 parameterized 예시다.

## 5. 남아 있는 위험과 통제

### 5.1 \(k\ge36\) 전체성

코드는 몇 개 \(k\)를 sample하지만 전체 범위 증거는 아니다. 전체성은 다음 단조 비교로
닫는다.

- \((\log(2k^2)+1)/k\)는 \(k\ge36\)에서 감소한다.
- \(51+50/\sqrt{k}+\sqrt{k}\log k\le k\log k\)는 \(k=36\)에서 성립하고
  오른쪽 여유가 이후 증가한다.
- \(I_N\) 하한은 \(0.9\log k>2\)와
  \(k^{1/(2(k-1))}<2\)를 써 \(1/[2(k-1)]\)보다 크게 만든다.

이 단조 논증과 코드 회귀검사를 서로 대체하지 않는다.

### 5.2 determinant가 1인 경우

\(\log\log D\)는 \(D=1\)에서 정의되지 않는다. 정식화는 이를 억지로 로그식에 넣지 않고
원 divisor 합이 정확히 1임을 별도 case로 처리한다.

### 5.3 상위 변수 선택

finite gate는 \(k,\alpha,\theta\)가 주어진 뒤 \(\log R\)에 대한 충분조건을 반환한다.
Sono/FMT 전체에서 이 매개변수를 어떻게 선택하고 \(R,x,X\)를 연결하는지는 별도
proof obligation이다. 대표값을 theorem threshold로 승격하면 안 된다.

### 5.4 출판 논문의 질적 \(O\)-결론

이번 상수는 원 논문의 질적 asymptotic 결론이 틀렸다는 판정이 아니다. 오히려 그
생략된 상수가 finite 계산에 쓸 수 있게 존재함을 한 보수적 경로로 보인 것이다.

## 6. 기계 검증이 보장하는 것과 보장하지 않는 것

보장:

- exact coefficient와 upward rounding
- exact prefactor identity
- exact divisor 조합 항등식
- 대표 finite gate의 모든 내부 조건
- parent non-promotion 및 source hash

보장하지 않음:

- Rosser--Schoenfeld 정리 자체의 새로운 형식증명
- \(k\ge36\) 해석 부등식을 brute-force로 대체
- Maynard Proposition 6.1 전체
- Sono/FMT의 numerical \(X_{\rm cert}\)
- 실제 prime 또는 maximal-gap 데이터에 대한 새 결과

따라서 Lean이나 추가 라이브러리는 이 하위 gate에 필요하지 않았다. 향후 전체 증명
artifact를 독립 proof assistant로 옮기려는 별도 목표가 생기면 그때 설치 여부를 판단한다.

## 7. 권장 후속

1. H1b-1b-2d.1b에서 두 sharp \(\xi\log x\) scale을 문헌 우선으로 수치화한다.
2. 그 결과와 이번 scalar package를 합쳐 H1B-L84 전체 상태를 다시 감사한다.
3. 병렬 독립 경로로 H1c-1 quantitative character/PAP package를 복원한다.
4. 모든 root dependency가 닫힌 뒤에만 threshold calculator를 설계한다.

현재 새 prime sweep이나 장시간 계산은 열린 해석 상수를 닫아 주지 못하므로 권장하지 않는다.
