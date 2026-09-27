# Review 106 — DEP-R09 endpoint \(L^\infty\) transfer 타당성검토

- 검토대상: Theory 97, Vaughan 1998 I·II, Harper 2024, Thorner--Zaman,
  machine ledger v1, exact Python helper·tests, Lean terminals
- 판정:
  <code>SOURCE_RANGE_AUDIT_VALID /
  SINGLE_ENDPOINT_TRANSFER_VALID /
  NUMERICAL_ENDPOINT_PNT_NOT_ESTABLISHED</code>

> **Successor:** [Theory 98](../method/theory/98_Sono_FMT_DEPR09_TZ_full_interval_centered_transfer.md)과
> [review 107](107_20260928_DEPR09_TZ_full_interval_centered_타당성검토.md)은 actual
> \(B_0\) exceptional handling, full-interval range와 centered factor 2를 닫았다.

## 1. 검토 결론

Theory 97의 환원은 타당하다.

1. Centered nonnegative residue mass의 \(L^1\) norm은 total mass의 두 배 이하이다.
2. 이를 large-interval residue error의 \(L^\infty\)와 결합하면 mixed covariance를
   single endpoint centered error로 충분히 제어한다.
3. Project의 \(Y/X\) 조건과 Rosser--Schoenfeld prime-count bounds는
   \(\vartheta_f(t)/(N\log t)<21/10\)을 준다.
4. 따라서 endpoint error에서 cross covariance로 가는 multiplier는 \(21/5\), Abel 뒤
   whole binary core multiplier는 \((21/5)(2+b/a)\)다.
5. Vaughan I·II와 Harper는 current prescribed \(f\)의 numerical endpoint theorem이
   아니다. Thorner--Zaman은 구조상 후보지만 numerical multiplier·cutoff가 남는다.

따라서 필요한 analytic source 의무는 축소됐지만 닫히지 않았다.

## 2. Exact finite inequality

\(A_a\ge0\), \(\mu=(\sum A_a)/\varphi(f)\)이면

\[
 \sum_a|A_a-\mu|\le\sum_a(A_a+\mu)=2\sum_aA_a.
\]

Theory 96의 exact residue cross identity에 적용하면

\[
 |{\cal K}_f|
 \le\varphi(f)\max_a|E_f(U;a)-E_f(X;a)|
 \sum_a|E_f(t;a)|.
\]

Endpoint norm 정의와 lower endpoint triangle을 넣은 Theory 97 식 (97.5)는 맞다.
Character별 absolute value를 먼저 취하지 않아 Theory 95의 character-count loss도 없다.

## 3. Lower endpoint correction

Current \(f>X\)이므로 한 residue class에 \(X\) 이하 positive integer는 많아야 하나다.
따라서 \(\vartheta(X;f,a)\le\log X\)다. \(\varphi(f)\le U^{1/21}\)과
\(\vartheta_f(X)<21X/20\)을 쓰면

\[
 \epsilon_0\le U^{-20/21}\log X+\frac{21X}{20U}.
\]

이 항은 explicit correction이지만 actual numerical threshold로 평가하지 않았다.

## 4. Prime-count normalization

Theory 47의 actual child는 \(Y\ge2k^2X\), \(k\ge10^{200}\),
\(Y<X\log X<X^2/4\)를 준다. 그러므로 Theory 97의 느슨한
\(Y\ge8X\), \(\log Y<2\log X\)는 안전하다.

Rosser--Schoenfeld에서 \(\pi(Y)>Y/\log Y\), \(\pi(X)<2X/\log X\)이고

\[
 \frac{2X}{\log X}\le\frac{Y}{2\log Y}.
\]

따라서 \(N=\pi(Y)-\pi(X)>Y/(2\log Y)\)다. 같은 source upper와
\(\log X\ge30\)은 \(\vartheta_f(t)<21t/20\)을 준다. \(t/\log t\) 단조성을
합치면 \(21/10\)이 맞다.

## 5. Source 적용성

### Vaughan 1998 I

Theorem 1은 uniform Criterion-U 식 (1.6)을 선행가정하고
\(x^{2/3}\le Q\le x\)에서 \(q\le Q\) 누적 variance를 다룬다. \(Q=f\)는 current
range 밖이다. 큰 \(Q\)를 골라 \(f\)를 포함시키는 것은 aggregate scale과 strong prior
progression assumption을 지우지 않는다.

### Vaughan 1998 II

Uniform 식 (1.4), mean-square 식 (1.5), \(Q>\sqrt x\log(2x)\)를 요구한다.
이 역시 \(Q=f\)가 아니며 current theta-weighted endpoint error를 직접 주지 않는다.

### Harper 2024

General complex sequence를 허용하지만 Theorems 1--2는 \(\sqrt{2x}<Q\le x\)와
\(Q/2<q\le Q\)의 dyadic average다. \(x=U\), \(f\le U^{1/21}\)이면 existing large
\(U\)에서 어떤 allowed block도 \(f\)를 포함하지 않는다.

### Thorner--Zaman

Pointwise theorem은 endpoint route에 구조적으로 맞는다. 그러나 exceptional secondary
main term, implied \(O_\varepsilon\) multiplier, decay \(c_1(\varepsilon)\), common cutoff를
숫자로 복원해야 한다. \(21/5\) transfer는 그 unknown multiplier를 없애지 않는다.

## 6. 과장 방지

- One-sided prime lower bound는 absolute centered \(L^\infty\) bound가 아니다.
- Brun--Titchmarsh upper는 explicit이지만 small relative error가 아니다.
- Vaughan/Harper가 쓸모없다는 일반 명제가 아니다.
- Mixed covariance direct proof가 불가능하다는 명제가 아니다.
- Source를 찾지 못했다는 사실만으로 novelty를 주장하지 않는다.

## 7. 검증 경계

Python은 finite rational vectors와 scalar multipliers만 검사한다. Actual primes,
\(\pi(X)\), \(\pi(Y)\), continuous zero-density integral은 계산하지 않는다.

Lean은 analytic source theorem을 공리화하지 않고 endpoint triangle과 \(21/5\), Abel
composition의 conditional scalar terminals만 검사한다.

## 8. 최종 상태

| 질문 | 판정 |
|---|---|
| mixed covariance theorem 의무가 약화됐는가 | <code>YES, sufficient endpoint route</code> |
| endpoint-to-cross multiplier가 explicit인가 | <code>YES, 21/5</code> |
| Vaughan/Harper drop-in이 있는가 | <code>NO</code> |
| numerical centered endpoint theorem이 있는가 | <code>NO</code> |
| numerical \(X_{\rm cert}\) range가 생겼는가 | <code>NO</code> |

다음 gate는 Theory 97 식 (97.25)의 fully numerical centered fixed-modulus endpoint
bound다.
