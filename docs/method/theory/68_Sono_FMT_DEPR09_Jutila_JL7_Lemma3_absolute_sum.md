# Sono/FMT DEP-R09 Jutila JL7 Lemma 3 absolute-sum 명시화

- 작성일: 2026-09-13 KST
- 단계: DEP-R09 / JL7-LEMMA3
- 선행 정본: [Theory 67](67_Sono_FMT_DEPR09_Jutila_JL7_shifted_contour_multiplier.md)
- 기계 원장: [JL7 Lemma 3 v1](data/Sono_FMT_DEPR09_Jutila_JL7_Lemma3_v1.json)
- 판정: JL7-LEMMA3 = ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT
- 비목적: residue·terminal density·PAP 닫기, fixed \(2\times10^{-17}\) 인증,
  \(X_{\rm cert}\) 계산기 제작, actual prime 계산

## 1. 결론

Jutila printed p.53에서 contour 항 뒤에 남는 합을

\[
 {\cal H}_q(R)=
 \sum_{\substack{r,r'\le R\\r,r'\ {\rm squarefree}\\
                  (rr',q)=1}}
 \frac1{rr'}\sum_{d\ge1}|h(d;r,r')|
\tag{68.1}
\]

로 쓰자. Jutila의 원문 Lemma 3과 유한 divisor double-counting을 합치면,
모든 \(R>1\)에

\[
 \boxed{{\cal H}_q(R)<3R^2}
\tag{68.2}
\]

를 쓸 수 있다. 상수 3은 최적값이 아니라, 최종 계산기에 바로 넣을 수 있는 완전한
유리수 안전 상계다. 이 component에는 \(R>1\) 외의 새 cutoff가 없다. actual
\(R=D^\theta\), \(D=qT\ge3\), \(\theta>0\)이므로 이 조건은 자동이다.

> **쉬운 설명:** 원문은 “이 많은 항을 모두 더해도 대략 \(R^2\) 정도”라고만 썼다.
> 이번 단계에서는 그 “대략”을 “3보다 작은 배수”로 바꿨다. 그러나 바로 다음 residue
> 계산의 “대략”은 아직 남아 있으므로 전체 \(X_{\rm cert}\) 계산은 아직 시작할 수 없다.

## 2. source-first 확인

| source | 확인 위치 | 이번 역할 | 판정 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | printed pp.48--49 Lemmas 2--3, p.53 호출 | \(h(d;r,r')\)의 exact Euler product, 두 Lemma 3 식, actual outer sum | 원출처 |
| Motohashi, *On a Density Theorem of Linntik* | printed p.816 Lemmas 1--2 | 같은 pseudocharacter와 \(\prod(p+1)\prod(p+1)\) loss의 선행 경로 | 보조 provenance, 더 강한 drop-in 아님 |

Jutila scan은 native text가 18 bytes뿐이므로 OCR은 위치 찾기에만 사용하고 printed
pp.48--49, 53의 렌더링 원페이지를 대조했다. Motohashi 공식 J-STAGE PDF는 native text를
먼저 추출했으며 Adobe-Japan1 font-map warning이 있었으므로 printed p.816의 렌더링
원페이지로 수식을 다시 대조했다.

Jutila는 Lemmas 1--3이 Motohashi의 당시 원고를 부분적으로 일반화했다고 썼다. 현재
공개된 1975년 Motohashi 발표문은 같은 \((p+1)\) local loss를 보여 주지만 \(h\)-절대합의
endpoint 상수를 제공하지 않는다. 따라서 별도 선행 정리를 잘못 가져오지 않고, Jutila의
peer-reviewed exact statement에서 아래 유한 합성을 직접 수행한다.

## 3. \(h(d;r,r')\)의 exact local factor

Jutila Lemma 2는 \(r,r'\)가 squarefree일 때

\[
 \prod_{\substack{p\mid rr'\\p\nmid(r,r')}}
   \{1+(f(p)-1)p^{-s}\}
 \prod_{p\mid(r,r')}
   \{1+(f(p)^2-1)p^{-s}\}
 =\sum_{d\ge1}h(d;r,r')d^{-s}
\tag{68.3}
\]

로 \(h\)를 정의한다. actual 함수는

\[
 f(p)=\mu(p)\varphi(p)=-(p-1).
\]

따라서 local nonconstant coefficient는 다음과 같다.

- \(p\)가 \(r,r'\) 중 정확히 하나만 나눌 때: \(f(p)-1=-p\).
- \(p\mid(r,r')\)일 때:
  \(f(p)^2-1=(p-1)^2-1=p(p-2)\).

각 local polynomial은 차수 1이므로 \(h\)의 support는
\({\rm lcm}(r,r')\)의 squarefree divisor에만 있다. 특히

\[
 d\le {\rm lcm}(r,r')\le rr'\le \lfloor R\rfloor^2.
\]

절댓값 계수합은 exact하게

\[
 \sum_d|h(d;r,r')|
 =
 \prod_{p\mid r\triangle r'}(p+1)
 \prod_{p\mid(r,r')}(p-1)^2.
\tag{68.4}
\]

공통 소수 \(p=2\)에서는 \(p(p-2)=0\)이므로 local factor가 1이고,
식 (68.4)의 \((p-1)^2=1\)과 정확히 일치한다. 이것은 구현에서 빠뜨리기 쉬운
endpoint다.

\((p-1)^2\le(p+1)^2\)이므로 Jutila Lemma 3의 인쇄된 상계

\[
 \sum_d|h(d;r,r')|
 \le
 \prod_{p\mid r}(p+1)\prod_{p\mid r'}(p+1)
\tag{68.5}
\]

가 나온다. 같은 local factor를 \(s=1\)에서 부호와 함께 곱하면

\[
 \sum_d\frac{h(d;r,r')}{d}
 =\delta_{r,r'}\varphi(r).
\tag{68.6}
\]

서로 다른 \(r,r'\)에는 한쪽에만 있는 소수가 있어 local factor가 0이고,
\(r=r'\)이면 각 소수가 \(p-1\)을 준다. 식 (68.6)은 다음 JL7-RES에서 residue
대각선만 남기는 정확한 source identity로 보존한다.

## 4. 두 outer sum의 factorization

\(K=\lfloor R\rfloor\)라 두고

\[
 a(r)=\frac1r\prod_{p\mid r}(p+1)
     =\prod_{p\mid r}\left(1+\frac1p\right),
\qquad
 A_q(K)=\sum_{\substack{r\le K\\r\ {\rm squarefree}\\ (r,q)=1}}a(r).
\tag{68.7}
\]

식 (68.5)를 식 (68.1)에 넣으면 두 outer family가 같은 Cartesian product이므로

\[
 {\cal H}_q(R)\le A_q(K)^2.
\tag{68.8}
\]

여기에는 항 개수를 \(K^2\)라고 거칠게 세는 추가 손실이나 \(\log K\)가 없다.

## 5. 유한 divisor double-counting

squarefree \(r\)에는

\[
 a(r)=\sum_{d\mid r}\frac1d.
\]

coprime와 squarefree 제한을 버려 upper bound를 취하고, 유한합 순서를 바꾸면

\[
\begin{aligned}
 A_q(K)
 &\le \sum_{n\le K}\sum_{d\mid n}\frac1d\\
 &=\sum_{d\le K}\frac{\lfloor K/d\rfloor}{d}\\
 &\le K\sum_{d\le K}\frac1{d^2}.
\end{aligned}
\tag{68.9}
\]

Basel 합과 \(\pi<3.15\)를 사용하면

\[
 \sum_{d\le K}\frac1{d^2}
 \le\frac{\pi^2}{6}
 <\frac53.
\tag{68.10}
\]

따라서

\[
 A_q(K)<\frac53K,\qquad
 {\cal H}_q(R)<\frac{25}{9}K^2<3K^2\le3R^2,
\]

이고 식 (68.2)가 증명된다. 이 증명은 asymptotic이나 hidden \(O\)-constant를
사용하지 않는다.

> **쉬운 설명:** 각 \(r\)의 무게를 따로 최악으로 잡으면 불필요한 로그가 붙는다.
> 대신 “\(d\)의 배수는 \(K/d\)개 이하”라는 단순한 사실로 합의 순서를 바꾸면,
> 잘 알려진 \(1+1/4+1/9+\cdots\) 합 하나만 남는다. 그래서 \(R^2\)의 원래 크기를
> 그대로 보존할 수 있다.

## 6. Theory 67 contour 상수와의 합성

Theory 67의

\[
 |I_d(s,\chi)|
 \le C_{\rm CONT}(\theta)\sqrt{qT}(M/d)^{-1+\theta}
\]

에 식 (68.2)를 넣으면 이 두 component가 만드는 multiplier는

\[
 C_{\rm CONT+L3}(\theta)=3C_{\rm CONT}(\theta).
\tag{68.11}
\]

계산기용 완전 초등 상계는

\[
 \boxed{
 \overline C_{\rm CONT+L3}(\theta)
 =144\left(1+\frac1\theta\right)
      \left(\frac2\theta+1\right)}
\tag{68.12}
\]

이다. \(\theta=1/21\)에서는

\[
 \overline C_{\rm CONT+L3}(1/21)=136224.
\tag{68.13}
\]

이 수치는 contour와 Lemma 3 outer sum만 합친 값이다. weight denominator,
integration normalization, residue, 마지막 \(J^2\) absorption을 모두 포함한 terminal
density coefficient가 아니다.

## 7. 코드·Lean 증거 경계

- [exact evaluator](../../../source/dep_r09_jutila_jl7_lemma3.py)는 local \(h\) 계수,
  식 (68.4)--(68.6), actual primed family와 세 단계 upper bound를 Fraction으로 계산한다.
- [fail-closed tests](../../../tests/test_dep_r09_jutila_jl7_lemma3.py)는
  \(r,r'\le50\)의 모든 squarefree pair, 공통 \(p=2\), divisor double-counting과
  downstream false flag를 검사한다.
- Lean 단일 파일에는 local real algebra, finite divisor double-count identity,
  finite Basel upper bound, \(5/3\to3\) coefficient 합성과 식 (68.12)--(68.13)을 넣는다.
- Jutila Lemma 3 전체의 multiplicative-function source proof와 finite prime-factor
  induction은 local project axiom으로 대체하지 않는다. 전자는
  SOURCE_THEOREM_UNFORMALIZED, Euler-product 전체 연결은 PARTIAL_FORMALIZATION으로
  구분한다.
- sorry, admit, project-local axiom을 사용하지 않는다.

따라서 Lean PASS는 Jutila의 analytic source 전체를 새로 형식화했다는 뜻이 아니다.
다만 이번 direct finite double-counting과 계산기 계수에 잘못된 부등식 방향이 들어가는
것을 kernel에서 막는다.

## 8. 상태와 다음 gate

| ID | 이번 판정 | 남은 일 |
|---|---|---|
| JL7-CONT | ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT | Theory 67 상수 보존 |
| JL7-LEMMA3 | ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT | 상수 3과 대각 identity를 downstream에 보존 |
| JL7-RES | HARD_BLOCKER | residue 적분, \(\delta_{r,r'}\), 같은 character의 height row sum 수치화 |
| JL7-ABSORB | HARD_BLOCKER | 모든 multiplier를 \(A-E>0\)에 넣은 공통 cutoff |
| JL7-AVERAGED | HARD_BLOCKER | 식 (3.7)의 variable-modulus replay |

따라서 terminal density, PAP-11, DEP-R09, fixed \(2\times10^{-17}\),
numerical \(X_{\rm cert}\)와 threshold calculator는 계속 OPEN/NOT READY다.
다음 우선순위는 JL7-RES의 source-first 복원이다.

## 9. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- Y. Motohashi, *On a Density Theorem of Linntik*, Proc. Japan Acad.
  51 Supplement (1975), 815--817,
  DOI [10.2183/pjab1945.51.Supplemnt_815](https://doi.org/10.2183/pjab1945.51.Supplemnt_815).
