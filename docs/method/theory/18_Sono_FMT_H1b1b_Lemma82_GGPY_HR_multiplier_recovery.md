# Sono/FMT H1b-1b Maynard Lemma 8.2·GGPY/HR multiplier 복원

- 작성일: 2026-09-06
- 대상: Maynard, *Dense Clusters of Primes in Subsets*, Lemma 8.2와
  GGPY, *Small Gaps Between Products of Two Primes*, Lemmas 3–4
- 상위 obligation: SIV-07
- 기계 계약:
  docs/method/theory/data/Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_v1.json
- 판정:

~~~text
Maynard Lemma 8.2 multiplier       = 89 (PROJECT FINITE COMPONENT CLOSED)
GGPY Lemma 3 -> Lemma 4 transfer  = C4 <= 2 C3 (PARAMETERIZED EXPLICIT)
HR Lemmas 5.3-5.4 base C3         = SOURCE ACCESS BLOCKED / OPEN
Maynard Lemma 8.4 composition      = OPEN
SIV-07 / X_cert                    = OPEN
~~~

## 1. 쉬운 요약

이번 작업은 두 종류의 “숨은 상수”를 구분했다.

첫째, Maynard Lemma 8.2의 \(O(\cdot)\) 안에 숨어 있던 수는 선택한 cutoff를 직접 미분하고
부등식을 다시 전개해 **89**라는 안전한 숫자로 바꿨다. 이는 원문의 정성적 “어떤 상수가
존재한다”를 이 프로젝트에서 실제로 사용할 수 있는 유한 부등식으로 바꾼 것이다.

둘째, GGPY Lemma 4의 숨은 상수는 그 바로 아래 Lemma 3의 상수를 \(C_3(A_1,A_2)\)라고
부르면 **최대 \(2C_3(A_1,A_2)\)** 로 전달된다는 것을 명시했다. 그러나 \(C_3\) 자체는
Halberstam–Richert의 책에 있는 Lemmas 5.3–5.4의 증명에서 복원해야 한다. 해당 쪽의 위치는
찾았지만 현재 합법적으로 열람 가능한 미리보기에는 전체 증명이 노출되지 않았다.

비유하면, 한 기계의 두 기어 중 첫 기어의 배율 89는 확정했고, 둘째 기어는 “앞 기어의
배율에 2를 곱한다”까지 확정했다. 하지만 둘째 기어 앞에 들어오는 \(C_3\)의 숫자가 아직
없으므로 전체 기계의 최종 배율과 작동 시작점은 계산할 수 없다.

## 2. 1차 출처와 provenance

| 출처 | 확인 위치 | 이번 판정 |
|---|---|---|
| James Maynard, *Dense Clusters of Primes in Subsets*, DOI 10.1112/S0010437X16007296, arXiv 1405.2593 | Section 8의 \(F,F_2\), Lemma 8.2, 식 (8.6)–(8.8), 출판본 16–18쪽 | 출판 PDF와 arXiv TeX를 식 단위로 대조 |
| Goldston–Graham–Pintz–Yıldırım, *Small Gaps Between Products of Two Primes*, DOI 10.1112/plms/pdn046, arXiv math/0609615 | Lemmas 3–4, PDF 9–10쪽; TeX 803–882행 | 조건, norm, 부분합 공식을 직접 대조 |
| GGPY corrigendum, DOI 10.1112/plms/pds053 | 서지·수정 대상 metadata | 출판사 PDF 접근 제한으로 본문은 미검토 |
| Halberstam–Richert, *Sieve Methods* | Lemma 5.3: 인쇄 144쪽; Lemma 5.4: 인쇄 147–152쪽 | Google Books 검색으로 위치 확인, 전체 proof는 제한되어 수치 복원 불가 |

로컬 hash와 취득시각은 기계 계약의 source_registry에 고정했다. GGPY arXiv source 응답은
파일명이 .tar였지만 실제 형식은 **단일 TeX를 gzip으로 압축한 payload**였다. 처음 이를 tar로
해제하려 한 시도는 잘못된 0-byte 항목들을 만들며 실패했다. 원본 hash를 유지한 채 gzip stream으로
다시 풀었고, 이후 감사에는 SHA-256
e58cc895e8b44f6369741f184bd81b595ed177463cf09cee8d0ad74558efce45인 TeX만 사용했다.
이는 도구 처리 실패이며 논문의 오류가 아니다.

## 3. Maynard Lemma 8.2의 명시적 상수

### 3.1 고정된 함수

H1b-1a에서 다음 cutoff를 고정했다.

\[
0\le\psi\le1,\qquad
\psi(t)=1\ (0\le t\le9/10),\qquad
\operatorname{supp}\psi\subset[0,1],\qquad
\|\psi'\|_\infty<50.
\]

Maynard의 표기를 따라

\[
T_k=k\log k,\qquad U_k=k^{-1/2},
\]

\[
F(\mathbf t)=\psi\!\left(\sum_i t_i\right)
\prod_i\frac{\psi(t_i/U_k)}{1+T_kt_i},
\]

\[
F_2(\mathbf t)=\sum_j
\frac{\psi(t_j/2)}{1+T_kt_j}
\prod_{i\ne j}\frac{\psi(t_i/U_k)}{1+T_kt_i}
\]

로 둔다.

### 3.2 한 좌표를 움직일 때의 직접 부등식

\(\mathbf v=\mathbf u+\delta\mathbf e_j\), \(\delta\ge0\)라 하자. \(u_j\ge U_k\)이면
\(\psi(u_j/U_k)=0\)이고 단조성 때문에 \(F(\mathbf u)=F(\mathbf v)=0\)이다.

이제 \(u_j<U_k\), \(0\le\delta\le1\)인 경우를 본다. \(j\) 이외 좌표의 곱을

\[
P=\prod_{i\ne j}\frac{\psi(u_i/U_k)}{1+T_ku_i}
\]

로 쓰고, 전체합 cutoff·좌표 cutoff·분모의 차이를 각각 한 번씩 삼각부등식으로 분리하면

\[
|F(\mathbf v)-F(\mathbf u)|
\le
\delta\left[T_k+50\left(1+\frac1{U_k}\right)\right]
\frac{P}{1+T_ku_j}.
\]

\(u_j<U_k\le1/\sqrt2\)이므로 \(\psi(u_j/2)=1\)이고, 마지막 항은 \(F_2(\mathbf u)\)의
\(j\)번째 항 이하이다. 따라서

\[
|F(\mathbf v)-F(\mathbf u)|
\le
T_k\delta\left[1+\frac{50(1+\sqrt k)}{k\log k}\right]F_2(\mathbf u).\tag{H1b-1b.1}
\]

이 전개는 원문의 \(1+O(T_k\delta)\)를 곱해 펼치는 대신 분모 차이를 정확히 계산했기 때문에,
숨은 교차항이나 “\(\delta\)가 충분히 작다”는 추가 가정을 만들지 않는다.

### 3.3 \(k\ge2\)에서 89로 통일

양의 항만 취한 급수와 유리수 비교로

\[
\log2
=2\sum_{n\ge0}\frac{1}{(2n+1)3^{2n+1}}
>2\left(\frac13+\frac1{81}\right)
=\frac{56}{81}>\frac{69}{100},
\]

\[
\frac1{\sqrt2}<\frac{71}{100}
\]

이다. 모든 정수 \(k\ge2\)에서

\[
\frac{1/k+1/\sqrt{k}}{\log k}
<\frac{1/2+71/100}{69/100}
=\frac{121}{69}.
\]

그러므로 (H1b-1b.1)의 대괄호는

\[
1+50\frac{121}{69}=\frac{6119}{69}<89.
\]

\(\delta>1\)이면 \(F(\mathbf u)\le F_2(\mathbf u)\)이고
\(89T_k\delta>1\)이므로 같은 부등식이 더 쉽게 성립한다. 따라서 Lemma 8.2(i)를

\[
\boxed{
|y_{\mathbf s}-y_{\mathbf r}|\le
89T_kY_{\mathbf r}\frac{\log A}{\log R}\qquad(k\ge2)
}\tag{H1b-1b.2}
\]

로 명시할 수 있다.

### 3.4 Lemma 8.2(ii)

\(t_i=[r_i,s_i]\)로 두고 각 좌표에 (H1b-1b.2)를 순서대로 적용한다. \(F_2\), 따라서
\(Y\)는 각 좌표에 대해 단조 비증가하므로 중간 단계의 \(Y\)를 출발점의 \(Y\)로 상계할 수 있다.
\(\mathbf s\to\mathbf t\)와 \(\mathbf r\to\mathbf t\)의 두 부등식을 삼각부등식으로 더하면

\[
\boxed{
|y_{\mathbf s}-y_{\mathbf r}|\le
89T_k(Y_{\mathbf r}+Y_{\mathbf s})\frac{\log A}{\log R}\qquad(k\ge2)
}.\tag{H1b-1b.3}
\]

두 경로의 오차가 이미 \(Y_{\mathbf r}+Y_{\mathbf s}\) 안에 따로 들어가므로 multiplier를 178로
다시 곱하지 않는다.

## 4. GGPY Lemma 3에서 Lemma 4로의 multiplier 전달

### 4.1 원문 구조

GGPY Lemma 3은 multiplicative \(\gamma\)가 \((\Omega_1)\),
\((\Omega_2(\kappa,L))\) 조건을 만족할 때

\[
G(u)=\sum_{d<u}\mu^2(d)g(d)
=c_\gamma\frac{(\log u)^\kappa}{\Gamma(\kappa+1)}+E(u)
\]

의 오차를 준다. 이 lemma는 Halberstam–Richert Lemmas 5.3–5.4의 결합이라고 원문이
명시하며, 숨은 상수는 \(A_1,A_2,\kappa\)에는 의존할 수 있지만 \(L\)에는 의존하지 않는다고
한다.

GGPY Lemma 4는 위 누적합에 piecewise differentiable \(F\)를 넣고 Stieltjes 부분적분을
사용한다. Maynard가 쓰는 경우는 \(\kappa=1\)이다.

### 4.2 조건부이지만 정확한 factor 2

HR 증명을 복원한 뒤 어떤 명시적 \(C_3(A_1,A_2)>0\)와 공통 범위에서

\[
|E(u)|\le C_3(A_1,A_2)c_\gamma(L+1)\qquad(1\le u\le z)\tag{H1b-1b.4}
\]

를 얻었다고 가정한다. \(L+1\)은 작은 \(L\)까지 안전하게 포함하는 Maynard 출판본의
\(\kappa=1\) 사용형이다. 이를 GGPY의 부분적분식에 대입하면 lower endpoint에서는
\(E(1^-)=0\)이고,

\[
\begin{aligned}
\left|\int_{1^-}^{z}F\!\left(\frac{\log(z/u)}{\log z}\right)dE(u)\right|
&\le C_3c_\gamma(L+1)\left(\lvert F(0)\rvert+\|F'\|_\infty\right)\\
&\le 2C_3c_\gamma(L+1)M(F),
\end{aligned}
\]

\[
M(F)=\sup_{0\le x\le1}\bigl(|F(x)|+|F'(x)|\bigr).
\]

따라서 안전한 전달식은

\[
\boxed{C_4(A_1,A_2)\le2C_3(A_1,A_2)}.\tag{H1b-1b.5}
\]

이다. factor 2는 **복원 완료**, \(C_3\)은 **미복원**이다. (H1b-1b.5)에 임의로
\(C_3=1\)을 넣는 것은 금지한다. 또한 HR의 실제 부등식이 (H1b-1b.4)를 \(u\ge u_0>1\)에서만
준다면 \(1\le u<u_0\)의 유한합을 별도로 더해야 하므로, 유효범위 확인도 생략할 수 없다.

## 5. HR 원문 접근 blocker

GGPY의 인용과 Google Books 검색 결과를 함께 대조해 다음 위치를 확정했다.

- Lemma 5.3: *Sieve Methods* 인쇄 144쪽
- Lemma 5.4: 인쇄 147쪽에서 시작해 152쪽에서 끝남
- 관련 notes: 인쇄 185쪽에 Lemma 5.4를 언급하는 항목이 있음

그러나 공개 미리보기는 검색 snippet만 제공하고 144–152쪽의 전체 식과 증명을 열어 주지 않는다.
OCR snippet은 수식이 크게 손상되어 상수 복원의 증거로 사용할 수 없다. 따라서 현재 상태는
“수학적으로 불가능”이 아니라 **필요한 1차 출처 쪽을 아직 읽을 수 없음**이다.

다음 중 하나가 필요하다.

1. Dover 2011 reprint, ISBN 9780486479392, 또는 Academic Press 1974,
   ISBN 0123182506의 인쇄 144–152쪽 스캔·사진·PDF
2. 문맥과 errata를 확인하기 위해 가능하면 140–153쪽, 앞부분 errata와 185쪽 notes도 함께 제공

사용자는 합법적으로 보유한 책·전자책에서 해당 쪽만 프로젝트에 전달하면 된다. 원문을 받으면
판본·쪽·식 번호를 먼저 고정하고 \(C_3(A_1,A_2)\)의 유도 전체를 다시 계산한다.

## 6. 상태 변경과 바뀌지 않은 것

| obligation | 이전 | 현재 | 의미 |
|---|---|---|---|
| H1B1-L82-LIPSCHITZ | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | multiplier 89, \(k\ge2\) |
| H1B-L82 | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | Lemma 8.2 자체는 닫힘 |
| H1B1-L83-GGPY4 | SOURCE_CHAIN_TRACED | PARAMETERIZED_EXPLICIT | \(C_4\le2C_3\), \(C_3\)은 open |
| H1B1-L83-GGPY3 | LOWER_SOURCE_REVIEW_REQUIRED | SOURCE_ACCESS_BLOCKED | HR proof pages 필요 |
| H1B-L83 | RATE_MISSING | RATE_MISSING | 최종 숫자·range 없음 |
| H1B1-PACKAGE | HARD_BLOCKER | HARD_BLOCKER | Lemma 8.4 등 미합성 |
| SIV-07 | HARD_BLOCKER | HARD_BLOCKER | 변화 없음 |
| \(X_{\mathrm{cert}}\) | OPEN | OPEN | 계산 불가 |

Lemma 8.2에서 \(T_k\)와 \(Y\)가 기호로 남는 것은 숨은 상수가 남았다는 뜻이 아니다. 이 둘은
lemma가 원래 제어하는 명시적 변수다. 반면 \(C_3(A_1,A_2)\)는 실제 숫자가 필요한 숨은
multiplier이므로 두 상태를 구분했다.

## 7. 기계검증 계약

source/h1b1b_multiplier_recovery.py와
tests/test_h1b1b_multiplier_recovery.py는 다음을 확인한다.

- \(\log2>69/100\), \(1/\sqrt2<71/100\), \(6119/69<89\)의 exact rational chain
- 여러 \(k\), support 경계, 작은·큰 \(\delta\)에서 직접 계산한 \(F,F_2\) 회귀검사
- GGPY \(\kappa=1\) 전달식 \(C_4=2C_3\)의 exact symbolic contract
- Maynard Lemma 8.2 child만 닫고 GGPY3, Lemma 8.4, package, SIV-07,
  \(X_{\mathrm{cert}}\)를 fail-closed로 유지하는지
- 문헌 source hash와 HR source-access blocker가 기계 원장과 일치하는지

수치 grid는 구현 회귀검사이고 §3의 전 구간 증명을 대신하지 않는다. 이번 gate에는 Lean이나
새 Python 라이브러리가 필요하지 않다.

## 8. 다음 권장 순서

1. **HR 원문 확보·C3 복원:** 원문을 받은 뒤 2–6시간의 1차 식 감사가 예상된다. 증명 안의
   또 다른 비명시적 정리가 발견되면 1–3일 이상으로 늘어날 수 있다.
2. **H1b-1b 후반 Lemma 8.4 합성:** \(A_1,A_2,L,\Omega_G\), \(r\)-fold error를 한 범위에
   묶는다. \(C_3\) 확보 뒤 약 6–20시간의 문헌·수식 작업이 예상된다.
3. **H1c-1 병렬 이론축:** quantitative character/Bombieri–Vinogradov package를 복원한다.
   여러 외부 명시적 정리가 연결되어 수일–수주가 걸릴 수 있다.
4. **H1b-2:** 위 두 축이 준비된 뒤 Sections 9의 moment error를 합성한다.
5. 모든 root dependency가 숫자와 공통 범위로 닫힌 뒤에만 threshold calculator와
   \(X_{\mathrm{cert}}\) 계산을 설계한다.

현재 CPU actual 실험이나 장시간 runner를 돌릴 단계가 아니다. HR 쪽을 받기 전 사용자 수행절차는
해당 쪽을 전달하는 것 외에는 없다.

## 참고문헌

- James Maynard, “Dense Clusters of Primes in Subsets,” *Compositio Mathematica* 152 (2016),
  DOI 10.1112/S0010437X16007296, arXiv 1405.2593.
- D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yıldırım, “Small Gaps Between Products of
  Two Primes,” *Proceedings of the London Mathematical Society* 98 (2009),
  DOI 10.1112/plms/pdn046, arXiv math/0609615.
- 같은 저자, corrigendum, DOI 10.1112/plms/pds053.
- H. Halberstam and H.-E. Richert, *Sieve Methods*, London Mathematical Society Monographs 4,
  Academic Press (1974); Dover reprint (2011), ISBN 9780486479392.
