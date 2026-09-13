# Sono/FMT DEP-R09 Jutila Lemma 6 actual truncation tail 명시화

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 / JL6b ACTUAL TRUNCATION TAIL`
- 선행 정본: [Theory 62](62_Sono_FMT_DEPR09_Jutila_Lemma6_Mellin_integral_explicit.md)
- 기계 원장: [Jutila Lemma 6 actual tail v1](data/Sono_FMT_DEPR09_Jutila_Lemma6_tail_actual_v1.json)
- 판정: `JL6-TAIL-ACTUAL ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT / JL6-TAIL-GENERAL AND JL6-COMMON-BUDGET OPEN`
- 비목적: 인쇄된 일반 Lemma 6의 uniform tail을 증명했다고 주장하기, JL6 종단 error budget 생략,
  actual prime sweep, threshold calculator, fixed (2\times10^{-17}) 또는 (X_{\rm cert}) 승격

## 1. 결론

Jutila 1977 Lemma 6은 식 (2.11)의 무한급수를

\[
 x=X\{\log(qT)\}^2
\]

에서 자른 나머지를 별도 \(\ll_\varepsilon1\)로만 기록한다. actual Theorem 1-prime
적용의

\[
 D=qT,\qquad R=D^\varepsilon,\qquad X=D^{1+12\varepsilon}
\]

을 사용하면 이 꼬리는 모든 \(\varepsilon>0\), \(D>1\)에서

\[
 \boxed{
 |E_{\rm tail}|
 \le4\exp\!\left(-L^2+(1+13\varepsilon)L\right),
 \qquad L=\log D
 }
\tag{63.10}
\]

로 명시화된다. 원하는 absolute budget을 \(0<\eta_{\rm tail}\le4\)라 하면

\[
 \boxed{
 L\ge
 \max\!\left\{2(1+13\varepsilon),
 \sqrt{2\log\frac4{\eta_{\rm tail}}}\right\}
 }
\tag{63.11}
\]

은 \(|E_{\rm tail}|\le\eta_{\rm tail}\)의 계산 가능한 충분조건이다.

따라서 `JL6-TAIL-ACTUAL`은 `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`으로
진전한다. 그러나 인쇄된 일반 Lemma 6은 \(X\)의 explicit upper envelope를 주지 않는다.
이번 절대값 proof는 \(X\)에 비례하므로 일반 명제의 uniform
\(\ll_\varepsilon1\)을 증명하지 않는다. 또한 JL5 relative loss, Theory 62의 Mellin
오차와 이번 tail을 하나의 detector budget에 아직 합치지 않았다. 그러므로
`JL6-TAIL-GENERAL`, `JL6-COMMON-BUDGET`, JL6 전체와 JL8은 열려 있고,
`PAP-11`, DEP-R09, fixed Sono 계수와 \(X_{\rm cert}\)도 OPEN이다.

> 쉬운 설명: 실제 후속 증명에서 쓰는 부품 크기에 한정하면, 잘라 버린 꼬리의 최대값을
> 숫자가 있는 공식으로 바꿨다. 하지만 원 논문의 모든 가능한 부품 크기까지 같은 방식으로
> 보장한 것은 아니다. 또 이 꼬리 비용을 다른 두 비용과 합쳐 최종 예산 안에 넣는 작업이
> 한 단계 남아 있다.

## 2. 원문·읽기 방식과 source-first 판정

| source | 확인 위치 | 읽기 방식 | 판정 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | 인쇄 pp. 48, 50--52; (2.11), 절단 문장, actual parameter | native text 18 bytes로 사실상 비어 300dpi OCR 후 원페이지 대조 | 원래 tail·endpoint·actual \(R,X\)의 정본 |
| NIST DLMF §8.10 | official web equations | 웹 수식 | incomplete-gamma 경로의 교차검토; 주 proof에는 불필요 |
| Graham, *On Linnik's constant* (1981) | 공식 metadata와 검색 가능한 statement | PDF는 공식 endpoint의 JavaScript challenge로 미확보 | truncated Perron을 쓰는 다른 detector라 drop-in source가 아님 |

표적 source 검색에서는 Jutila 식 (2.11)의 actual discrete tail에 그대로 넣을 수 있는
published explicit multiplier를 식별하지 못했다. 이 결과는 전 세계 문헌 부재 주장이 아니다.
이번 실제 계수에는 geometric series의 exact 합이 더 짧고 endpoint-safe하므로 직접 초등
proof를 주 경로로 채택한다. Graham PDF는 이 proof의 필수 입력이 아니며, 읽지 못한 PDF를
읽었다고 기록하지 않는다.

## 3. 정확히 잘리는 항

\(\rho=\beta+it\), \(\beta\ge\alpha\ge1/2\)이고
\(\psi_r(n)=\mu((r,n))\varphi((r,n))\)라 하자. 식 (2.11)의 유일한 무한
\(n\)-급수에서 버리는 꼬리는

\[
 E_{\rm tail}=
 \sum_{n>x}a(n)\chi(n)e^{-n/X}n^{-\rho}
 \sum_{r\le R}'\frac{\psi_r(n)}r,
 \qquad x=X(\log D)^2,\quad D=qT.
\tag{63.1}
\]

prime은 Jutila의 squarefree·\((r,q)=1\) 제한을 뜻한다. 바깥 \(r\)-합과
\(M\)-polynomial은 유한하므로 별도의 무한 tail이 아니다.

## 4. actual coefficient의 점별 상계

Jutila (2.5)--(2.6)의 \(|\lambda_d|\le1\)과 support를 쓰면

\[
 |a(n)|
 =\left|\sum_{d\mid n}\lambda_d\right|
 \le\tau(n)\le2\sqrt n,
 \qquad
 |\psi_r(n)|\le(r,n)\le r.
\tag{63.2}
\]

마지막 divisor bound는 약수 \(d<\sqrt n\)와 \(n/d>\sqrt n\)를 짝짓고, 제곱수의
중앙 약수는 한 번만 세면 얻는다. 또한 \(|\chi(n)|\le1\), \(\beta\ge1/2\)이므로

\[
 |a(n)|n^{-\beta}\le2,
 \qquad
 \sum_{r\le R}'\frac{|\psi_r(n)|}{r}\le R.
\tag{63.3}
\]

여기서는 prime 조건을 버려 합을 더 크게 만들었다. \(R\ge1\)일 때 정수 \(r\le R\)의
개수는 \(\lfloor R\rfloor\le R\)이다.

## 5. endpoint-safe geometric tail

첫 생략 정수를 \(N=\lfloor x\rfloor+1\)이라 하면 \(N>x\)이고

\[
 \sum_{n>x}e^{-n/X}
 =\frac{e^{-N/X}}{1-e^{-1/X}}
 \le\frac{e^{-x/X}}{1-e^{-1/X}}.
\tag{63.4}
\]

\(u=1/X>0\)와 \(e^u-1\ge u\)에서

\[
 \frac1{1-e^{-1/X}}
 =1+\frac1{e^{1/X}-1}
 \le X+1.
\tag{63.5}
\]

식 (63.3)--(63.5)을 합치고 \(X\ge1\)에서 \(X+1\le2X\)를 쓰면

\[
 |E_{\rm tail}|
 \le2R(X+1)e^{-x/X}
 \le4RXe^{-(\log D)^2}.
\tag{63.6}
\]

이 proof는 \(x\)가 정수가 아닐 수 있는 경우도 \(N=\lfloor x\rfloor+1\)로 정확히 처리한다.

## 6. general upper envelope와 finite cutoff

어떤 actual 적용에서

\[
 R\le D^r,\qquad X\le D^c,\qquad r,c\ge0
\tag{63.7}
\]

라는 upper envelope가 있으면, \(L=\log D>0\)에서

\[
 |E_{\rm tail}|
 \le4\exp\{-L^2+(r+c)L\}.
\tag{63.8}
\]

\(L\ge2(r+c)\)이면
\(-L^2+(r+c)L\le-L^2/2\)이다. 또한
\(L^2\ge2\log(4/\eta_{\rm tail})\)이면

\[
 4e^{-L^2+(r+c)L}\le\eta_{\rm tail}.
\tag{63.9}
\]

\(0<\eta_{\rm tail}\le4\)일 때 식 (63.11)은 이 두 조건을 동시에 보장한다.

## 7. actual Jutila parameter 특수화

Jutila 인쇄 p. 52의 선택은

\[
 R=D^\varepsilon,\quad
 z_1=D^{1/2+7\varepsilon},\quad
 z_2=D^{1/2+8\varepsilon},\quad
 X=D^{1+12\varepsilon}.
\tag{63.12}
\]

따라서 식 (63.7)의 \(r+c\)는 정확히

\[
 \varepsilon+(1+12\varepsilon)=1+13\varepsilon.
\tag{63.13}
\]

식 (63.10)--(63.11)은 여기서 바로 나온다. 이 꼬리 cutoff는 아직
Theory 61의 JL5 cutoff나 Theory 62의 Mellin cutoff와 합친 공통 \(D_0(\varepsilon)\)이 아니다.

## 8. 왜 printed general Lemma 6은 열어 두는가

인쇄된 일반 Lemma 6은 식 (2.8)로 \(X\)의 **아래쪽** 크기를 제한하지만 위쪽 크기는
제한하지 않는다. 식 (63.6)의 절대값 상계는 \(RXe^{-(\log D)^2}\)이므로, 고정 \(D,R\)에서
\(X\)를 임의로 크게 하면 이 상계도 커진다. 이는 Jutila 일반 명제가 틀렸다는 뜻이 아니다.
nonprincipal character의 상쇄나 더 정교한 Dirichlet-series 추정으로 uniform bound를 얻을
가능성이 남아 있다. 다만 이번 elementary proof가 그것을 증명하지 않았다는 뜻이다.

DEP-R09의 현재 branch가 사용하는 것은 식 (63.12)의 actual parameter이므로 다음 단계의
common budget에는 actual bound를 쓸 수 있다. 일반 Lemma 전체가 필요해지는 다른 응용에는
이번 상태를 재사용하면 안 된다.

## 9. Python·Lean 검증 경계

`source/dep_r09_jutila_jl6_tail.py`는 100-dps로 식 (63.6), (63.8), (63.10)--(63.11)을
평가하고 다음 fail-closed flag를 보존한다.

- actual tail component: closed
- printed general tail: open
- JL6 common budget·JL6 전체: open
- fixed Sono coefficient·\(X_{\rm cert}\): not ready

Python 수치는 directed interval certificate가 아니다. 단위시험은 source hash, 약수함수의
작은 exact 진단, geometric endpoint, actual exponent와 cutoff implication을 검사한다.

Lean 단일 파일에는 다음 유한 실수대수만 형식화한다.

1. \(X+1\le2X\)
2. actual exponent 합 \(1+13\varepsilon\)
3. \(L\ge2a\)에서 quadratic decay
4. \(L^2\ge2\log(4/\eta)\)와 합친 tail budget
5. max/square-root cutoff가 위 quadratic 조건을 준다는 transfer

무한 geometric series, divisor bound, character·pseudocharacter의 analytic 정의는 이번
Lean batch에서 전부 형식화하지 않는다. source theorem이나 직접 analytic proof를
project-local `axiom`으로 선언하지 않으며 `sorry`, `admit`도 사용하지 않는다.

## 10. 상태표와 다음 gate

| ID | 현재 판정 | 의미·남은 의무 |
|---|---|---|
| `JL5` | `EXPLICIT_PEER_REVIEWED_SOURCE_REPLACEMENT_WITH_Q_DEPENDENT_CUTOFF` | Theory 61 유지 |
| `JL6-MELLIN` | `ACTUAL_FORM_PARAMETERIZED_EXPLICIT` | Theory 62 유지 |
| `JL6-TAIL-ACTUAL` | `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT` | 식 (63.10)--(63.11) |
| `JL6-TAIL-GENERAL` | `OPEN_PRINTED_STATEMENT_REQUIRES_X_UPPER_ENVELOPE_OR_CANCELLATION` | 일반 uniform proof 미완 |
| `JL6-COMMON-BUDGET` | `HARD_BLOCKER` | JL5 loss+Mellin+tail의 한 \(D_0(\varepsilon)\) 필요 |
| `JL6` / `JL8` | `HARD_BLOCKER` | detector 종단·local zero count 미완 |
| `PAP-11` / DEP-R09 | `OPEN` | density와 principal/error 합성 미완 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | `OPEN` | calculator 제작 금지 유지 |

다음 우선순위는 `JL6c common error budget`이다. Theory 61의 relative JL5 loss와
Theory 62의 Mellin absolute error, 이번 actual tail absolute error를 최종
\((1-\varepsilon)\) detector coefficient 안에 배분하고 하나의 finite cutoff로 합친다.

## 11. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- NIST Digital Library of Mathematical Functions,
  [Incomplete Gamma Functions §8.10](https://dlmf.nist.gov/8.10).
- S. W. Graham, *On Linnik's constant*, Acta Arith. 39 (1981), 163--179,
  DOI [10.4064/aa-39-2-163-179](https://doi.org/10.4064/aa-39-2-163-179).
