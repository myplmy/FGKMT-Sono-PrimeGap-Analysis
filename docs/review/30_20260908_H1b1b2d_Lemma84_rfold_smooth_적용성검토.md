# H1b-1b-2d Maynard Lemma 8.4 \(r\)-fold·smooth 적용성 비판 검토

- 작성일: 2026-09-08
- 검토 대상: Maynard Lemma 8.4의 실제 Section 8 적용을 numerical proof package로 바꾸는 단계
- 정식화 정본:
  [24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md](../method/theory/24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md)
- 기계 계약:
  [Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json](../method/theory/data/Sono_FMT_H1b1b2d_rfold_smooth_composition_v1.json)

## 1. 최종 판정

\[
\boxed{\texttt{PARTIAL\_VALID: SMOOTH SUBPACKAGE CLOSED, ACTUAL LEMMA 8.4 OPEN}}
\]

타당한 핵심은 세 가지다.

1. 교정된 one-step Lemma 8.3 오차를 좌표별로 적용하면
   \(\prod_i(1+\delta_i)-1\)이라는 exact finite-product envelope를 얻는다.
2. actual \(N,W,N^2,W^2,NW\)는 비음수 smooth profile이므로 support 길이와 도함수를
   보존해 보수적인 norm을 명시할 수 있다.
3. \(F_2^2\)의 넓은 \(W^2\) 좌표를 먼저 합하면 기존 \(\Lambda_*\) 제외모듈 상계를
   안전하게 유지할 수 있다.

그러나 source 905행의 \(H=F+O(\eta F_2)\)는 \(O\) 안의 실제 함수와 \(C^1\)
multiplier를 주지 않는다. 두 sharp cutoff 호출도 \(\xi\log x\)의 finite lower bound를
필요로 한다. 따라서 `H1B-L84=RATE_MISSING`, `SIV-07=HARD_BLOCKER`,
\(X_{\rm cert}=\texttt{OPEN}\)을 유지하는 것이 타당하다.

## 2. 선행결과 우선 전략의 타당성

사용자가 제안한 “기존 lemma를 먼저 찾고, 적합한 증명이 없을 때만 직접 증명한다”는 방식은
이 단계에 적합하다. 같은 명제를 다시 증명하는 시간을 줄이고, 오래된 인쇄 오류를 반복할
위험도 낮춘다. 단, 이름이나 결론이 비슷하다는 이유만으로 가져오지 않도록 다음을 개별
확인했다.

| 검사 항목 | Maynard 2016 | Axiom Math 2026 | 이번 project lemma |
|---|---|---|---|
| 실제 Section 8 sieve datum | 일치 | 다름 | Maynard datum만 사용 |
| actual \(F,F_2\) profile | 일치 | full-profile 직접 대체 아님 | 정확히 전개 |
| corrected \(c_\gamma(L+1)\) | 인쇄 주석은 있음 | 핵심 상수 존재형 | theory 22 수치식 사용 |
| 좌표별 support \(U_k,2\) | 숨은 \(O\)로 처리 | 같은 계약 아님 | 명시 |
| finite \(r\)-fold constant | 없음 | \(C,C_1,C_2\) 존재형 | exact product |
| peer review·독립 검증 | 출판됨 | 미검증 후보 | project lemma로 범위 제한 |

Axiom Math의 [논문 페이지](https://primegaps.axiommath.ai/paper/)와
[PrimeGapsLib 저장소](https://github.com/AxiomMath/PrimeGapsLib)는 반복 partial
summation을 telescoping하는 구조적 교차검사로는 유용하다. 그러나 사용자 지정 미검증
후보군이고, 공개 Lean 결과도 project axiom에 조건부라는 기존 리뷰 판정을 바꾸지 않는다.
이번 상수 package의 theorem input으로 채택하지 않았다.

표적 검색에서 완성된 동형 finite package를 찾지 못했지만, 이것을 문헌 전체에 대한
신규성 주장으로 확대하지 않는다.

## 3. 실제 적용에서 주의할 점

### 3.1 실제 main 대비 상대오차가 아니다

원문 error scale은

\[
\Pi_g(\log R)^{r-1}\log\log R\prod_i\int G_i
\]

형태다. \(\Phi(\sum t_i)\)가 들어간 실제 main integral은 이 product integral보다 작을 수
있다. 따라서 이번 결과도 product-profile envelope에 대한 절대오차 상계다.
“모든 actual main term의 상대오차가 1 이하”라고 읽으면 잘못이다. 이후 moment 하한과
비교할 때 별도 lower-bound multiplier가 필요하다.

### 3.2 \(F_2^2\)의 support는 모두 1이 아니다

\(W(t)=\psi(t/2)/(1+T_kt)\)는 \([0,2]\)에 지지된다. 이 좌표를 뒤에 남긴 채
“남은 변수는 각각 \(e_i\le R\)”라고 쓰면 제외 정수 상계가 작아질 수 있다. 각 tensor
term에는 넓은 \(W^2\) 좌표가 최대 하나뿐이므로 그 좌표를 먼저 합한다. 현재 좌표는 다음
제외 정수에 들어가지 않고, 이후 좌표의 support exponent는 \(U_k\le1\)이다. 이 순서
조건 아래에서만 theory 23의 \(\Lambda_*\)를 그대로 재사용한다.

### 3.3 비음수성은 증명의 가정이다

finite-product induction은 error branch의 절댓값을 nonnegative main envelope로 덮는다.
actual cutoff와 profile은 비음수이고 \(F_2^2\) 전개의 계수도 비음수라서 적용된다.
일반 signed test function까지 증명했다고 확장하지 않았다.

### 3.4 source의 reciprocal 방향 불일치

Maynard source 620행·printed p.1536의
\(k^2T_k=o(\log\log R/\log R)\)는 같은 lemma의 가정과 (8.20)에 맞지 않는다.
문맥상 필요한 조건은 \(k^2T_k\log\log R/\log R=o(1)\)이다. 계산에서는 후자를 쓴다.
정식 erratum을 찾았다고 말하지는 않는다.

## 4. 직접 증명한 범위

직접 증명한 것은 다음 연결부뿐이다.

- support \([0,s]\)를 \(z=R^s\)로 바꾸는 변수변환
- \(\omega_s(G)=\sup(|G|+s|G'|)/\int G\) 정규화
- one-step uniform error의 exact finite-product induction
- actual cutoff의 \(\|\psi'\|_\infty<50\)에서 나온 profile integral·미분 상계
- \(F_2^2\)의 finite tensor family 분류와 wide-first 순서
- 닫힌 smooth 하위문제에 대한 보수적 finite smallness cutoff

Maynard Proposition 6.1 전체, Lemma 8.4의 opaque \(H\), sharp \(\xi\), Lemmas 8.5–8.6,
Propositions 9.1–9.5는 증명하지 않았다.

## 5. 수치 예시를 threshold로 사용하면 안 되는 이유

\(k=36,\alpha=0.01,\theta=0.25\)라는 설명용 대입에서 충분조건은 대략

~~~text
log10(log R) >= 132.07
~~~

이 된다. 이는 매우 보수적인 상수의 결과이고, \(\alpha,\theta\)가 최종 Sono/FMT
application에 맞게 인증된 것도 아니다. 더구나 opaque·sharp·PAP·hypergraph·arbitrary-X
의무가 남아 있다. 따라서 이 숫자는 “FGKMT/Sono 부등식이 이 \(x\)부터 성립한다”는
threshold가 아니며, \(X_{\rm cert}\)로 보고하면 오류다.

## 6. 코드·시험의 역할과 한계

`source/h1b1b2d_rfold_smooth_package.py`는 증명된 식을 평가하고 열린 호출을 거부한다.
`tests/test_h1b1b2d_rfold_smooth_package.py`는 source hash, 호출 전수분류, tensor 전개,
profile bound, product identity와 parent non-promotion을 검사한다.

수치적분과 도함수 grid는 구현 회귀검사일 뿐 연속구간 증명이 아니다. 연속 상계의 근거는
정본 문서의 해석식이며, floating 값은 directed rounding certificate로 쓰지 않는다.

## 7. 다음 작업의 우선순위

1. **H1b-1b-2d.1 / 905행 \(H\) source tracing**  
   \(H\)를 만든 Y-difference error를 역추적해 명시적 nonnegative majorant와
   \(C^1\) multiplier를 얻을 수 있는지 확인한다.
2. **sharp \(\xi\) finite scale 복원**  
   \(\xi\)의 선택과 \(\gg\) 상수를 추적해 \(\xi\log x\)의 수치 하한을 만든다.
3. **H1c-1 quantitative character/PAP**  
   H1b와 독립인 root blocker이므로 병렬 문헌감사 대상으로 유지한다.

첫 두 항이 닫히기 전에는 `H1B-L84`를 승격하지 않고, 모든 root가 닫히기 전에는
threshold calculator나 장시간 prime 계산을 만들지 않는다.
