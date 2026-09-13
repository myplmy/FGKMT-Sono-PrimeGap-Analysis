# Sono/FMT DEP-R09 Branch S 정량 transfer 감사

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 BRANCH S / FIXED-D TRANSFER AUDIT`
- 선행 정본: [Theory 58](58_Sono_FMT_DEPR09_explicit_PNT_AP_replacement_source_audit.md)
- 기계 원장: [Branch S transfer v1](data/Sono_FMT_DEPR09_branch_S_transfer_v1.json)
- 판정: `STRUCTURAL_ROUTE_CONFIRMED / NUMERICAL TRANSFER NOT RECOVERED`
- 비목적: actual prime sweep, 임의 multiplier 채택, Huxley 비공식 mirror 사용,
  numerical \(X_{\rm cert}\) 계산

## 1. 결론부터

Thorner--Zaman의 uniform PNT-in-AP는 \(q\le x^{1/160}\) 범위를 구조적으로 다룰 수 있는
가장 가까운 현대적 경로다. 그러나 원문 proof를 source leaf까지 추적한 결과, fixed
\(D=160\)의 one-sided PAP에 필요한 multiplier·decay constant·finite cutoff를 숫자로
복원하지는 못했다.

핵심 이유는 다음과 같다.

1. unconditional zero-density Theorem 2.1(2.1)은 Huxley와 Jutila를 한 문장으로 인용하며
   수치 multiplier와 시작점을 주지 않는다.
2. exceptional-removed (2.2)는 `sufficiently small` 상수, effective lower bound,
   Jutila Theorem 2의 비수치 \(D_0(\varepsilon)\), implied-constant inflation을 사용한다.
3. Theorem 2.3과 Theorem 1.1의 합성에도 explicit formula, Chebyshev, local zero count,
   partial summation, dyadic decomposition의 숨은 상수가 남는다.
4. fixed \(q=x^{1/160}\)에서는 leading exponential loss가 \(x\) 증가만으로 0이 되지 않는다.
   따라서 “충분히 큰 \(x\)”라는 말로 미지 multiplier를 흡수할 수 없다.

Jutila 1977은 exponent 2의 density estimate와 `10 exp(11 lambda)` 형태를 제공해 구조적으로
유망하지만, proof 안의 여러 \(\ll_\varepsilon\), \(O_\varepsilon\), \(1+o(1)\),
`sufficiently large`를 실제 숫자로 만들지 않았다. 즉 source chain은 존재하지만
drop-in numerical theorem은 아니다.

> 쉬운 설명: 다리의 설계도는 찾았지만, 몇 톤을 견디는지 적힌 검사표가 없다. 차가 실제로
> 지나가도 되는지 인증하려면 각 부품의 허용하중을 숫자로 다시 계산해야 한다. 길을 더 멀리
> 연장한다고 이 검사표가 저절로 생기지는 않는다.

따라서 `PAP-11`, `DEP-R09`, fixed \(2\times10^{-17}\), \(X_{\rm cert}\)는 계속 OPEN이다.

## 2. actual PAP contract

Branch S가 닫아야 하는 것은 다음 하나의 finite interface다. \(B_0\)는 가능한 exceptional
modulus에서 선택한 제외 prime을 나타낸다.

\[
 \pi(u;q,a)\ge C_{\rm PAP}\frac{u}{\varphi(q)\log u},\qquad
 u\ge u_{\rm PAP},\quad q\le u^{1/160},\quad (a,q)=1,\quad B_0\nmid q.
\tag{59.1}
\]

현재 downstream 계수에서 필요한 최소값과 총 오차 예산은

\[
 C_{\rm PAP}\ge0.863831261522671247201665369608\ldots,\qquad
 \eta_{\rm tot}:=1-C_{\rm PAP}\le
 0.136168738477328752798334630392\ldots .
\tag{59.2}
\]

이는 density estimate 하나가 아니라 principal term, nonprincipal zeros, exceptional branch,
prime powers, \(\psi\to\pi\), endpoint와 하나의 공통 cutoff를 모두 포함한 계약이다.

## 3. 원문 읽기·provenance

| source | 읽기 방식 | 대조 범위 | 판정 |
|---|---|---|---|
| Thorner--Zaman, arXiv `2108.10878v2` | native text 우선 | PDF pp. 4, 5, 8, 10, 11 | proof DAG 복원 |
| Jutila 1977, DOI `10.7146/math.scand.a-11701` | native text 18바이트로 내용 없음 → 300dpi OCR | 인쇄 pp. 46, 47, 54, 58, 59, 61 | 정량화 누락 확인 |
| Huxley 1974/75, DOI `10.4064/aa-26-4-435-444` | 공식 endpoint 접근 시도 | Anubis JS proof-of-work로 차단 | 수치 주장에 사용 안 함 |

Thorner--Zaman audit copy SHA-256은
`588ec896e0820c3620175b25da58850efbefc67b71227acac1d5c3fa4f6b3b09`, Jutila 공식
PDF SHA-256은 `f6e9038a7216b690763692e0a07bc8c58284c9560bf62ab987ea62a817404ad5`다.
Jutila의 OCR은 검색 보조일 뿐 수식 전사의 정본이 아니며, 아래 사용한 theorem·상수·부등호는
렌더링한 원 페이지와 대조했다.

## 4. Thorner--Zaman proof DAG 감사

### 4.1 density 입력

Theorem 2.1은

\[
 N_q(\sigma,T)\ll_\varepsilon
 (qT)^{(12/5+\varepsilon)(1-\sigma)},\qquad
 N_q^*(\sigma,T)\ll_\varepsilon
 \nu(qT)(qT)^{(37/5+\varepsilon)(1-\sigma)}
\tag{59.3}
\]

를 준다. 첫 식의 proof는 “Huxley와 Jutila의 work에서 잘 알려져 있다”고만 쓰므로
수치 multiplier·cutoff를 이 논문 자체에서 회수할 수 없다. 두 번째 식은 첫 식 외에도
다음 비수치 입력을 쓴다.

- effectively computable and sufficiently small \(\nu_\varepsilon\)
- \(\beta_1\)의 effective lower bound가 만드는 `sufficiently large` \(qT\)
- Jutila Theorem 2의 \(D_0(\varepsilon)\)
- implied constant inflation과 \(\varepsilon\) rescaling

따라서 `effectively computable`은 `numerically supplied`와 같지 않다.

### 4.2 density에서 prime sum으로 가는 단계

Theorem 2.3 proof의 actual edge는 다음과 같다.

```text
standard explicit formula
  -> prime powers를 Chebyshev bound로 제거
  -> local zero-count와 Taylor bound
  -> dyadic O(log x) decomposition
  -> partial summation + Theorem 2.1 density
  -> phi(q), q, lambda 비교
  -> Vinogradov--Korobov zero-free region
  -> Theorem 1.1 relative error
```

각 화살표에는 적어도 하나의 `O`, `≪` 또는 `≍`가 있다. 논문은 모두 effectively
computable이라고 선언하지만 수치 multiplier와 공통 시작점은 인쇄하지 않는다. 그러므로
Theorem 2.1의 multiplier만 복원해도 PAP package가 자동 완성되지는 않는다.

## 5. fixed-D transfer gate

어떤 정량 재증명이 nonprincipal relative error를

\[
 E_{\rm tr}(K,c;D):=K\exp(-Dc),\qquad K>0,\ c>0,
\tag{59.4}
\]

로 만들었다고 가정하자. 이 정의는 source theorem이 아니라 숨은 값을 끝까지 보존하기 위한
진단 interface다. \(D>0\), \(\eta>0\)에서

\[
 c\ge\frac{\log K-\log\eta}{D}
 \quad\Longrightarrow\quad
 K e^{-Dc}\le\eta .
\tag{59.5}
\]

식 (59.5)의 초등 실수 부등식은 Lean theorem `pap_fixed_d_transfer_gate`로 검증한다. 다만
실제 source가 그러한 \(K,c\)를 준다는 analytic 명제는 전혀 가정하거나 local axiom으로
추가하지 않는다.

식 (59.2)의 총 오차를 전부 이 한 항에 준다는 가장 낙관적인 진단에서도 \(D=160\)의 최소
decay constant는 다음과 같다.

\[
\begin{array}{c|ccccc}
K&1&10&320&10^3&10^6\\ \hline
c_{\min}&
0.0124616277388&0.0268527845700&0.0485136339625&
0.0556350982325&0.0988085687261
\end{array}
\tag{59.6}
\]

`320`은 Thorner--Zaman 식 (2.5)에 보이는 \(2\log x/\log q=2D\)만을 예시적으로 떼어낸
값이다. 전체 proof multiplier라는 뜻이 아니며, 나머지 finite error에 예산을 남기면
필요한 \(c\)는 표보다 더 커진다.

> 쉬운 설명: 숨은 배수 \(K\)가 클수록 오차를 같은 크기 아래로 누르려면 지수감쇠 \(c\)가
> 더 강해야 한다. \(K\)를 모른 채 \(c\)만 “양수”라고 아는 것으로는 통과 여부를 결정할 수 없다.

### 5.1 왜 \(x\) 증가만으로 해결되지 않는가

\(q=x^{1/D}\)이면 정확히 \(\log x/\log q=D\)다. 따라서 fixed \(D=160\)에서
\(K\exp[-c\log x/\log q]\)는 \(K e^{-160c}\)가 된다. 이는 \(x\to\infty\)에서도
상수이므로, 알려지지 않은 \(K,c\)를 finite cutoff 하나로 대체할 수 없다. 낮은 차수의
\(o(1)\) 항은 큰 \(x\)로 줄일 수 있어도 이 limiting factor는 남는다.

## 6. Jutila route의 실제 상태

Jutila Theorem 1은 \(4/5\le\alpha\le1\)에서

\[
 N(\alpha,T,q)\ll_\varepsilon(qT)^{(2+\varepsilon)(1-\alpha)},\qquad
 N^*(\alpha,T,Q)\ll_\varepsilon(Q^2T)^{(2+\varepsilon)(1-\alpha)}
\tag{59.7}
\]

를 준다. exponent 2는 구조적으로 중요하다. Thorner--Zaman Remark 2.4에 따르면 density
exponent를 \(c_7\)로 바꿀 수 있을 때 short-interval exponent는

\[
 \theta=1-\frac1{c_7}
\tag{59.8}
\]

로 개선된다. 따라서 \(c_7\approx2\)는 범위 면에서 유망하다. 그러나 이것은 numerical
multiplier나 pointwise PAP coefficient를 주는 명제가 아니다.

Jutila의 더 명시적으로 보이는 두 명제도 끝까지는 수치화되지 않았다.

\[
 N(\lambda)\le10e^{11\lambda}
 \quad\text{for all }\lambda>0\text{ and sufficiently large }D,
\tag{59.9}
\]

\[
 \delta_1\ge
 \frac{(1-6\delta)D^{-(2+\varepsilon)\delta/(1-6\delta)}}{8\log D},
 \qquad D\ge D_0(\varepsilon).
\tag{59.10}
\]

Theorem 1-prime proof는 Lemmas 4·5로 explicit하게 만들 수 있다고 말하지만 결론에는
`D sufficiently large`가 남는다. Lemma 4는 당시 `to appear`인 Graham 결과를 사용하고,
Lemma 5는 \(R\to\infty\)의 \(1+o(1)\)이다. Theorem 2 proof에는 epsilon-의존
\(O\)-항, `lower order`, `sufficiently good lower bound`가 남는다. 마지막 Linnik constant
분기는 `crude estimations`을 쓰고 세부를 생략한다.

판정은 `SHARP_STRUCTURAL_SOURCE / QUANTITATIVE_REPROOF_REQUIRED`다.

## 7. coefficient capacity와 D 선택

source theorem을 더 쉽게 만들기 위해 \(D\)를 키우면 modulus 범위는 좁아지지만 downstream
계수 여유도 줄어든다.

| \(D\) | 필요한 최소 \(C_{\rm PAP}\) | 허용 총 상대오차 | 낙관 \(C=1\) 최종계수 |
|---:|---:|---:|---:|
| 160 | 0.8638312615226712 | 0.1361687384773288 | \(2.6802306048\times10^{-17}\) |
| 170 | 0.9144441706862033 | 0.0855558293137967 | \(2.3917490170\times10^{-17}\) |
| 180 | 0.9650536817352026 | 0.0349463182647974 | \(2.1474697346\times10^{-17}\) |
| 186 | 0.9954179689225081 | 0.0045820310774919 | \(2.0184548684\times10^{-17}\) |
| 187 | 1.0004785886922302 | 음수 | \(1.9980870186\times10^{-17}\) |

이 표는 Theory 58의 같은 downstream 식을 재계산한 필요조건 진단이다. \(D=186\)에서도
PAP 오차 전체가 0.4582% 미만이어야 하므로 “\(D\)를 조금 키우면 쉬워진다”는 장점이 매우
빠르게 사라진다.

## 8. 최소 hard blockers

| ID | 최초 미수치 edge | 영향 | 닫힘 조건 |
|---|---|---|---|
| `RS02-A` | Huxley--Jutila unconditional density multiplier·cutoff | nonexceptional zero sum | 공식 source chain 전부의 수치 majorant |
| `RS02-B` | Jutila exceptional density/DH cutoff | exceptional-removed density | \(\nu_\varepsilon,D_0(\varepsilon)\)와 multiplier |
| `RS03` | Theorem 2.3 density-to-prime-sum multiplier | pointwise error | explicit formula부터 partial summation까지 합성 |
| `RS04` | \(\lambda\)와 actual \(B_0\) 제외의 one-sided 연결 | 모든 residue의 lower bound | exceptional branch uniform finite lemma |
| `RS05` | principal term·VK numerical decay | main term | 수치 \(c_8\), multiplier, cutoff |
| `RS06` | prime powers·\(\psi\to\pi\)·endpoint | PAP coefficient | 별도 오차 예산과 cutoff |
| `RS07` | 위 cutoff의 maximum | calculator input | 하나의 숫자 \(u_{\rm PAP}\) |

`RS02-A`만 닫아도 나머지가 자동으로 닫히지 않는다. 반대로 `RS03--RS06`을 숫자로 만들더라도
source density multiplier가 미지이면 최종 coefficient를 계산할 수 없다.

## 9. Lean·기계검증 경계

- 식 (59.5)의 초등 transfer 충분조건만 `KERNEL_PASS` 대상으로 삼는다.
- 식 (59.1), (59.3), (59.7), (59.9), (59.10)은 외부 analytic source theorem 또는
  목표이므로 `SOURCE_THEOREM_UNFORMALIZED`다.
- 표 (59.6)과 coefficient 표는 fixed FGKMT Python의 80-dps 재계산과 unittest로 검사한다.
- source theorem을 premise 없이 Lean에서 선언하지 않으며 `axiom`, `sorry`, `admit`을 쓰지 않는다.
- 이 batch의 Lean 통과는 Thorner--Zaman/Jutila theorem이나 fixed \(2\times10^{-17}\)을
  증명하지 않는다.

## 10. 다음 권장 경로

1. 공식 Huxley PDF를 확보해 Theorem 2.1(2.1)의 source leaf와 수치화 가능한 proof를 확인한다.
2. Jutila Lemmas 4--8의 선행 source를 정확히 고정하고, 각 `O`와 충분히 큰 조건을 목록화한다.
3. 동시에 Thorner--Zaman Theorem 2.3의 explicit-formula-to-density 합성만 독립 finite lemma로
   재작성해, density package에 요구되는 정확한 multiplier interface를 확정한다.
4. 실제 \(K,c,u_0\)가 생긴 뒤에만 (59.5), (59.2), Theory 58의 coefficient 함수 순서로 검사한다.
5. 어느 branch도 통과하지 못하면 fixed 계수를 낮추는 별도 연구안과 현 목표를 분리해 사용자와
   논의한다.

현재 단계에는 장시간 CPU 계산이나 새 Python package가 필요하지 않다. Huxley 원문 수동 확보를
제외하면 사용자 수행절차도 없다.

## 11. 엄밀한 현재 판정

```text
Thorner--Zaman structural range            = COMPATIBLE IN PRINCIPLE
Thorner--Zaman numerical transfer package  = NOT RECOVERED
Jutila exponent-2 route                    = STRUCTURALLY PROMISING, NONNUMERICAL
Huxley official full text                  = AUTOMATED ACCESS BLOCKED, NOT USED
fixed-D limiting multiplier issue          = CONFIRMED
elementary transfer sufficient condition   = LEAN TARGET
PAP-11 / DEP-R09                           = HARD_BLOCKER / OPEN
fixed 2e-17                                = NOT INDEPENDENTLY CERTIFIED
X_cert                                     = OPEN
actual prime computation                   = NOT RUN
```

## 12. 참고문헌

- Jesse Thorner and Asif Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://arxiv.org/abs/2108.10878),
  Theorems 1.1, 2.1, 2.3 and proof of Theorem 2.3; DOI `10.1007/s00209-023-03414-3`.
- Matti Jutila, [*On Linnik's constant*](https://doi.org/10.7146/math.scand.a-11701),
  *Mathematica Scandinavica* 41 (1977), 45--62.
- M. N. Huxley,
  [*Large values of Dirichlet polynomials III*](https://doi.org/10.4064/aa-26-4-435-444),
  *Acta Arithmetica* 26 (1974/75), 435--444.
