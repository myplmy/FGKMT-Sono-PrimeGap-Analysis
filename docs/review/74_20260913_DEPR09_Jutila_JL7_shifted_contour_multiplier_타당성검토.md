# DEP-R09 Jutila JL7 shifted-contour multiplier 타당성검토

- 작성일: 2026-09-13 KST
- 상세 정본: [Theory 67](../method/theory/67_Sono_FMT_DEPR09_Jutila_JL7_shifted_contour_multiplier.md)
- 기계 원장: [JL7 contour v1](../method/theory/data/Sono_FMT_DEPR09_Jutila_JL7_contour_v1.json)
- 최종 판정: `contour multiplier는 actual 범위에서 명시화됨; 전체 density와 X_cert는 아직 OPEN`

## 1. 무엇이 해결됐나

Jutila 논문은 p.53에서 contour 적분 \(I_d\)가 작다고 쓰면서, 그 앞의 정확한 숫자는
\(\ll_\theta\) 안에 숨겼다. 이번 감사는 그 부분을

\[
 |I_d(s,\chi)|
 \le \frac{96\sqrt2}{\pi}\zeta(1+\theta)
       \left(\frac2\theta+1\right)
       \sqrt{qT}(M/d)^{-1+\theta}
\]

로 바꿨다. 계산기에서는 더 단순하고 조금 큰

\[
 48(1+1/\theta)(2/\theta+1)
\]

을 쓸 수 있다. \(\theta=1/21\)이면 이 안전 상계는 정확히 45,408이다.

> **일상적인 비유:** 원 논문에는 “이 짐은 충분히 가볍다”라고만 적혀 있었다. 이번에는
> “최악의 경우에도 무게가 45,408 단위 이하”처럼 실제 제한표를 붙였다. 다음 단계에서는
> 이 짐을 여러 개 합쳤을 때의 전체 무게를 따로 계산해야 한다.

## 2. 왜 이 도출이 타당한가

### 2.1 비주지표를 빠뜨리지 않았는가

비주지표에는 peer-reviewed Bennett et al. Lemma 5.6의 exact Rademacher bound를 썼다.
product character가 primitive가 아닐 수 있으므로 conductor에서 modulus \(q\)로 되돌릴 때의
Euler factor도 \(4/\sqrt6\)으로 따로 넣었다. 따라서 primitive인 경우만 계산한 것이 아니다.

### 2.2 주지표를 빠뜨리지 않았는가

\(\bar\chi_j\chi_k\)는 \((j,k)\)에 따라 주지표가 될 수 있다. 이 경우 Bennett 정리만 쓰면
안 된다. 그래서 peer-reviewed Hasanalizade--Shen--Wong Proposition 3.8을
\(K=\mathbb Q\)에 적용했다.

특히 \(|1+z|/|1-z|\)의 분자·분모를 각각 따로 크게 잡지 않았다. 실제 범위
\(0<\operatorname{Re}z\le1/7\)에서 비율 전체가 \(4/3\) 이하임을 먼저 보였다. 이 덕분에 높이에
불필요한 \(T\) 한 제곱이 더 붙지 않고, Jutila가 필요로 한 \(\sqrt{qT}\) scale을 보존한다.

### 2.3 contour 전체 높이를 다뤘는가

적분변수 \(y\)는 무한 범위를 돈다. \(|v|\le2T\)와 \(T\ge1\)을 이용해

\[
 |1+z|\le(22/7)T(1+|y|)
\]

로 잡고, \(\sqrt{1+|y|}\)를 Gamma의 수직선 감쇠와 함께 실제로 적분했다. 특정한 작은
\(y\)만 검사한 것이 아니다.

### 2.4 \(N\)항을 누락하지 않았는가

원 integrand에는 \((N/d)^w-(M/d)^w\) 두 항이 있다. \(\operatorname{Re}w<0\)이고
\(N\ge M\)이므로
두 항의 절대값을 모두 포함해 \(2(M/d)^{-1+\theta}\)로 잡았다. \(N\)항을 0으로 놓거나
상쇄를 가정하지 않았다.

## 3. 얼마나 보수적인가

비주지표의 실제 합성 coefficient는 약 2.09774이고, 주지표는 약 11.15170이다. 공통값
12는 안전한 반올림이다. \(\theta=1/21\)에서 zeta를 그대로 둔 multiplier는 약 40,102.35,
초등 상계는 45,408이다.

이 차이는 약 13%의 보수 여유다. 지금 단계의 목적은 상수를 최적화하는 것이 아니라 숨은
상수를 없애는 것이다. 후속 전체 cutoff가 지나치게 커진 뒤에만 최적화를 고려하는 편이
효율적이다.

## 4. 여전히 해결되지 않은 것

이번 결과를 전체 Jutila density theorem으로 확대하면 안 된다. 바로 다음에 다음 네 항이
남아 있다.

1. Jutila Lemma 3을 사용한 \((r,r',d)\) 절대합 multiplier
2. 주지표 residue와 같은 character의 여러 높이 합
3. 위 항들을 왼쪽으로 흡수하는 공통 finite cutoff
4. 식 (3.7)의 variable-modulus averaged replay

따라서 `PAP-11`, DEP-R09, Sono의 fixed \(2\times10^{-17}\), numerical
\(X_{\rm cert}\)는 아직 인증되지 않았다. threshold calculator도 아직 만들면 안 된다.

## 5. Lean과 수치검사의 의미

Lean에는 범위·유리부등식·coefficient 합성만 넣는다. 외부 Rademacher 정리, complex
contour 이동과 Gamma complex integral을 local `axiom`으로 만들지 않는다. Python의
100-dps 값은 수식 전사와 규모를 점검하는 진단이며 directed interval proof가 아니다.

그러므로 증거 수준은 다음처럼 읽어야 한다.

- 외부 analytic 입력: peer-reviewed source statement 확인
- actual parameter 대입과 유한 대수: Python·Lean 교차검증
- 전체 Jutila theorem: 아직 미완성

## 6. 다음 권장 작업

`JL7-LEMMA3`을 먼저 감사하는 것이 타당하다. contour multiplier를 이미 얻었으므로,
이제 \(h(d;r,r')\)의 local factor와 support를 원문 Lemma 3에서 exact하게 복원해
\(r,r'\le R\)까지 합치면 off-diagonal 전체 coefficient를 만들 수 있다. 그 후에야 residue와
최종 흡수 cutoff를 계산하는 순서가 중복을 줄인다.

현재 사용자에게 필요한 장시간 CPU 계산, 새 Python package 또는 Lean 설치는 없다.

## 7. 참고문헌

- M. Jutila, *On Linnik's constant*, DOI
  [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. A. Bennett et al., *Counting zeros of Dirichlet L-functions*, DOI
  [10.1090/mcom/3599](https://doi.org/10.1090/mcom/3599), arXiv
  [2005.02989](https://arxiv.org/abs/2005.02989).
- E. Hasanalizade, Q. Shen, P.-J. Wong,
  *Counting zeros of Dedekind zeta functions*, DOI
  [10.1090/mcom/3665](https://doi.org/10.1090/mcom/3665), arXiv
  [2102.04663](https://arxiv.org/abs/2102.04663).
- H. Rademacher, *On the Phragmén--Lindelöf theorem and some applications*, DOI
  [10.1007/BF01162949](https://doi.org/10.1007/BF01162949).
