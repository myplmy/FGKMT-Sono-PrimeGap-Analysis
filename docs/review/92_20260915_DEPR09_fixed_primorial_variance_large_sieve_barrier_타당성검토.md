# DEP-R09 고정 primorial 분산·large-sieve 장벽 타당성검토

- 검토일: 2026-09-15 KST
- 대상: Theory 83
- 판정:
  <code>SOURCE RANGE MISMATCH CONFIRMED /
  DIRECT LARGE-SIEVE CERTIFICATE TOO COARSE /
  ACTUAL ENERGY AND X_CERT STILL OPEN</code>

## 1. 쉬운 설명

Theory 82에서 필요한 숫자를 하나의 “오차 에너지” \(V(Y,q)\)로 줄였다.
이번에는 이미 알려진 large sieve라는 강력한 도구가 그 에너지를 충분히 작게
보증하는지 검사했다.

비유하면 다음과 같다.

- 우리가 통과해야 하는 문 높이는 \(G\)다.
- 기존 도구가 알려 주는 것은 “실제 짐 \(V\)는 상자 \(B\) 안에 들어간다”는 사실이다.
- 그런데 그 상자 \(B\) 자체가 문 \(G\)보다 크다.

이 경우 실제 짐은 문보다 작을 수도 있다. 하지만 “상자 안에 있다”는 정보만으로는
그 사실을 증명할 수 없다. 이번 결과는 실제 짐이 크다는 결과가 아니라
**기존 포장 방식이 너무 거칠다**는 결과다.

## 2. 문헌에서 바로 가져올 정리를 찾았는가

찾지 못했다. 중요한 이유는 변수 범위와 평균 대상이 다르기 때문이다.

프로젝트는

\[
 q=Y^{1/d},\qquad21\le d\le186
\]

을 사용하므로 \(q\le Y^{1/21}\)이다. 반면 확인한 Friedlander--Goldston의
조건부 natural asymptotic과 Vaughan의 modulus-average 결과는 \(q\) 또는 평균
scale이 대체로 \(Y^{1/2}\) 이상, 많게는 \(Y\)에 가까운 범위다.

또한 여러 modulus의 평균이 좋다는 사실은 우리가 미리 정한 primorial 하나도
좋다는 뜻이 아니다. “대부분의 학생 평균이 좋다”가 “특정 학생 한 명의 점수도
좋다”를 자동으로 뜻하지 않는 것과 같다.

이 판정은 확인한 corpus와 표적 검색 범위에 한정된다. 전 세계 문헌에 해당 정리가
절대 없다는 주장으로 확대하지 않는다.

## 3. 원문 대조는 어떻게 했는가

PDF가 native text를 포함하면 먼저 text layer로 theorem과 식을 찾고, 그 뒤 해당
원문 페이지를 이미지로 렌더링해 기호와 상수를 대조했다.

Montgomery--Vaughan 1973 저자 공개본 printed p.119에서

\[
 \sum_r|S(x_r)|^2
 \le(N+\delta^{-1})\sum_n|a_n|^2
\]

를 직접 확인했다. 이전 보조 강의노트의 더 날카로운 표기와 섞지 않고,
이번 판정에는 원 논문에 인쇄된 안전한 \(N+\delta^{-1}\)을 사용했다.

Dusart의 \(\vartheta\) 상계와 Rosser--Schoenfeld의 \(q/\varphi(q)\) 상계도
native text와 원문 렌더 페이지를 대조했다. 스캔 OCR만으로 기호를 채택하지 않았다.

## 4. 수치 장벽은 무엇인가

direct classical large-sieve RHS는 가장 유리하게 단순화해도

\[
 B_{\rm LS}
 =
 (Y+q^2)\sum_{n\le Y}\Lambda(n)^2.
\]

Dusart 상계를 쓰면 현재 범위 전체에서

\[
 \frac{B_{\rm LS}}{Y^2}>5\log q.
\]

반면 Theory 82 gate에 shift 분포, 성공확률, survivor 비율을 전부 가장 유리하게
주어도

\[
 \frac{V_{\rm gate}}{Y^2}
 \le e^{-4}\frac q{\varphi(q)}.
\]

Rosser--Schoenfeld를 사용하면

\[
 5\log q>
 e^{-4}\frac q{\varphi(q)}
\qquad(q\ge3).
\]

따라서

\[
 B_{\rm LS}>V_{\rm gate}.
\]

가장 작은 검사 endpoint \(q=3,d=21\)에서도 보수적인 두 값은 각각
약 \(5.5944\)와 \(0.4912\)이고 margin은 약 \(5.1032\)다.
실제 \(q/\varphi(q)\)를 쓰면 gate 상계는 약 \(0.02747\)로 더 작다.

## 5. 무엇을 기각했고 무엇은 기각하지 않았는가

### 기각

- 고전 large sieve의 raw 전체 RHS를 그대로 넣어 Theory 82를 닫는 방법.
- modulus 평균을 prescribed primorial 하나의 결과로 바꾸는 방법.
- shift entropy만 더 확보하면 raw large-sieve RHS가 해결된다는 방법.

### 계속 가능

- \(q\)의 divisor conductor만 다루는 sparse-family 강화.
- primes와 primorial 구조를 이용하는 더 작은 variance 상계.
- full \(V\) 대신 실제 weighted correlation만 직접 제어하는 방법.
- 절댓값을 취하기 전의 cancellation을 이용하는 방법.
- 새로운 explicit fixed-primorial PNT 또는 zero-density 전달.

따라서 이번 결과를 “large sieve 계열은 전부 불가능”이라고 읽으면 잘못이다.

## 6. Fiorilli--Martin 결과의 올바른 사용

Fiorilli--Martin은 작은 \(q\)에서 보편적인 Hooley variance 추측이 거짓임을 보였다.
그러나 그 반례 범위가 지금의 \(q=Y^{1/d}\)를 직접 포함한다고 확인한 것은 아니다.

이 프로젝트에 중요한 부분은 uniform natural-variance bound가 Dirichlet
\(L\)-function의 넓은 zero-free region까지 함의한다는 것이다. 즉 full variance
정리는 편리한 보조정리가 아니라 매우 강한 해석적 수론 명제다.

그래서 앞으로는 full natural variance보다 실제 소비식에 더 가까운
weighted-correlation 정리를 먼저 찾는 편이 합리적이다.

## 7. \(X_{\rm cert}\)에 미치는 영향

| 질문 | 답 |
|---|---|
| 새 bounded \(X_{\rm cert}\) 범위를 얻었나? | 아니오 |
| fixed \(2\times10^{-17}\)을 독립 인증했나? | 아니오 |
| DEP-R09 또는 PAP-11을 닫았나? | 아니오 |
| threshold calculator를 만들 단계인가? | 아니오 |
| 장시간 CPU 계산이 필요한가? | 현재 아니오 |
| 무엇이 진전됐나? | 자연스럽지만 너무 거친 direct large-sieve 경로 하나를 전 범위에서 제거 |

이번 음성 결과는 가치가 있다. 앞으로 거대한 threshold 계산을 시작한 뒤 뒤늦게
“입력 상계가 gate보다 컸다”는 사실을 발견하는 낭비를 막기 때문이다.

## 8. Lean과 코드가 실제로 확인하는 것

Python은 exact \(\varphi(q)\), source-derived coefficient, 120-dps margin,
strict boundary와 source hash를 검사한다.

Lean은 다음 dependency-critical 부분만 검사한다.

1. \(L\ge21t\), \(\log2<t\)이면
   \(5t<(L-\log2)/4\).
2. 각 factor의 상계가 있으면 best-entropy gate envelope가 유지됨.
3. \(G\le B\)인 upper certificate만으로 \(V<G\)를 얻을 수 없다는
   \(V=G\) countermodel.

외부 analytic theorem은 local axiom으로 넣지 않으며,
<code>sorry</code>와 <code>admit</code>도 사용하지 않는다.

## 9. 권장 다음 연구

1. **sparse-divisor large-sieve 문헌 감사**
   - actual character family는 모든 \(r\le q\)가 아니라 \(r\mid q\)이므로
     구조를 이용할 여지가 있는지 본다.
2. **direct weighted-correlation theorem 설계**
   - full \(V\)보다 약하고 Maier/FMT가 실제 소비하는 양에 더 가깝다.
3. **prime-specific conditional second moment**
   - FMT outer law와 같은 probability law에서 직접 평균을 잡는다.
4. 위 셋 중 하나가 numerical multiplier와 cutoff까지 확보된 뒤에만
   \(X_{\rm cert}\) calculator와 장시간 연산을 검토한다.

현재 사용자가 실행할 명령이나 설치할 라이브러리는 없다.
