# DEP-R09 Jutila JL7·식 (3.6) 종단 교정 타당성검토

- 작성일: 2026-09-13 KST
- 상세 수식 정본: [Theory 66](../method/theory/66_Sono_FMT_DEPR09_Jutila_JL7_terminal_parameter_repair.md)
- 기계 원장: [JL7 terminal v1](../method/theory/data/Sono_FMT_DEPR09_Jutila_JL7_terminal_v1.json)
- 최종 판정: `중대한 scope 오류 교정 / actual weighted call 복구 / terminal density 미완`

## 1. 무엇이 잘못돼 있었나

앞선 Theory 60은 explicit Barban--Vehov 상계의
\(\tau=8/5\), \(K=37.769894\)를 Jutila 식 (3.6)에 적용할 수 있다고 적었다. 원문을
proof branch별로 다시 대조하면 이 값은 p.54의 Theorem \(1'\) 선택에만 맞는다. 식 (3.6)이
있는 p.52의 Theorem 1은

\[
 z_1=D^{1/2+7\theta},\qquad z_2=D^{1/2+8\theta}
\]

를 사용하므로

\[
 \tau_\theta=\frac{1+16\theta}{1+14\theta}
\]

이다. 따라서 고정 `37.769894`를 식 (3.6)에 넣은 것은 타당하지 않았다.

> 쉬운 설명: 한 논문 안의 “계산 A”와 “계산 B”가 비슷하게 생겼지만 숫자 설정은 달랐다.
> 과거 문서가 B의 숫자를 A에도 썼다. 아직 이 숫자로 최종 결과를 계산한 적은 없어서 실제
> \(X_{\rm cert}\) 결과를 폐기할 일은 없지만, 지금 고치지 않으면 나중 계산 전체가 잘못될 수
> 있는 중요한 오류였다.

## 2. 교정 결과는 타당한가

Ramaré--Zuniga Corollary 1.3은 \(\tau>1\) 전 범위에 적용되므로 올바른
\(\tau_\theta\)를 다시 대입할 수 있다. exact rational 전개와 Lean 대수를 통해

\[
 K_{\rm BV}(\theta)<\frac{13}{\theta},\qquad
 K_{\rm BV}(\theta)\frac{\log x}{\log(z_2/z_1)}<\frac{34}{\theta^2}
\]

를 \(0<\theta\le1/21\), \(L=\log D\ge4\)에서 얻었다. 따라서 식 (3.6)의 one-sided
weighted square-sum 호출은 고정상수가 아니라 **\(\theta\)-의존 explicit bound**로 복구된다.

이 결과가 보수적이어도 방향은 안전하다. upper bound를 더 크게 잡았으므로 필요한 제곱합을
과소평가하지 않는다. \(\theta\to0\)에서 상수가 커지는 현상도
\(\tau_\theta\to1\)인 source 구조와 일치한다.

## 3. 추가로 닫힌 부분

- Lemma 7의 \(b_n^{-1}\) quotient는 actual 범위에서 5 미만이다.
- integration 면적은 생략하지 않고
  \(A_{\rm int}\ge\theta^2/2\)로 보존했다.
- off-diagonal의 \(D\)-지수는 finite log gate 아래
  \(-29\theta/252\) 이하로 감소한다.
- 최종 흡수는 \(AJ^2\le BJY+EJ^2\), \(E<A\)라는 fail-closed interface로 바꿨다.

이 네 항은 원문 \(\ll_\theta\)를 모두 숫자로 만들지는 않지만, 다음 감사에서 “이미 닫힌
부분”과 “아직 모르는 multiplier”를 혼합하지 않게 해 준다.

## 4. 아직 증명되지 않은 것

Jutila p.53의 다음 표현에는 여전히 numerical multiplier가 없다.

1. shifted contour integral \(I_d(s,\chi)\ll_\theta\cdots\)
2. Lemma 3을 사용한 \(r,r',d\) 절대합
3. principal residue와 같은 character의 height well-spacing 합
4. 마지막 \(J^2\) 항을 왼쪽으로 흡수하는 공통 finite cutoff
5. 식 (3.7)의 variable-modulus averaged replay

그러므로 `Jutila terminal density`, `PAP-11`, `DEP-R09`, fixed
\(2\times10^{-17}\), numerical \(X_{\rm cert}\)는 모두 OPEN이다.

## 5. 다른 explicit density 정리로 바로 바꿀 수 있나

Ramaré 2016 Theorem 1.1은 명시적 상수를 주므로 좋은 비교 대상이다. 하지만 우변의
\(32Q^2\log^2(Q^2T)\) additive 항은 현재의
\(1-\sigma=\lambda/\log D\) near-one regime에서 bounded log-free multiplier로 일률 흡수되지
않는다. 따라서 drop-in replacement가 아니다. 이 정리를 쓰려면 PAP transfer를 별도 방식으로
다시 설계해야 한다.

## 6. 연구 진행에 미치는 영향

- 나쁜 영향: 기존 `37.769894`를 식 (3.6)에 쓰는 간단한 경로는 폐기해야 한다.
- 좋은 영향: 올바른 coefficient를 explicit하게 복구했고, 다음 blocker를 contour와 residue
  multiplier로 정확히 좁혔다.
- 결과 영향: numerical \(X_{\rm cert}\)나 fixed coefficient를 인증한 적이 없으므로, 기존 실제
  prime-gap 실험 결과를 다시 계산할 필요는 없다.
- 작업 우선순위: `JL7-CONT` source-first 감사가 가장 먼저다. 그 다음 Lemma 3 합,
  residue/well-spacing, 최종 흡수, averaged replay 순서가 타당하다.

현재 필요한 작업은 문헌·수식 감사와 짧은 검증뿐이다. 사용자의 장시간 CPU 실행이나 새
라이브러리 설치는 필요 없다.

## 7. 참고문헌

- M. Jutila, *On Linnik's constant*, DOI
  [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- O. Ramaré and S. Zuniga Alterman, *An \(L^2\)-bound for the Barban--Vehov weights*,
  DOI [10.7169/facm/241018-19-5](https://doi.org/10.7169/facm/241018-19-5),
  arXiv [2405.12662](https://arxiv.org/abs/2405.12662).
- O. Ramaré, *An explicit density estimate for Dirichlet \(L\)-series*,
  [author PDF](https://ramare-olivier.github.io/Maths/DensityEstimate-34.pdf).
