# H1b-1b Kuperberg 현대 sieve 재현·GGPY 오류항 타당성 검토

- 작성일: 2026-09-06
- 검토 대상:
  - Vivian Kuperberg, arXiv:2210.09775v2
  - Castillo–Hall–Lemke Oliver–Pollack–Thompson, arXiv:1403.5808
  - 대조 대상 GGPY Lemmas 3–4와 Maynard Lemmas 8.3–8.4
- 상위 연구 질문: Sono/FMT의 “sufficiently large \(X\)”를 명시적
  \(X_{\mathrm{cert}}\)로 바꾸기 위한 H1b-1b 상수 복원

## 최종 판정

~~~text
Kuperberg가 HR 5.4 구조를 접근 가능한 형태로 재현하는가?       YES
그 문헌만으로 numerical C3와 finite cutoff가 닫히는가?         NO
Lemke Oliver 등이 제기한 c_gamma 오류항 문제는 실제인가?       YES
그 문제는 kappa=1 Maynard 사용에도 관련되는가?                 YES
Lemma 8.2 multiplier 89가 무효가 되는가?                       NO
부분적분 절대오차 전달 factor 2가 무효가 되는가?                NO
GGPY/Maynard의 최종 정성적 정리가 반박되는가?                   NOT ESTABLISHED
현재 X_cert 계산이 가능해지는가?                                NO
~~~

정식 상태:

~~~text
CORRECTION_CONFIRMED
NUMERICAL_MULTIPLIER_OPEN
MAYNARD_QUALITATIVE_APPLICATION_NOT_DISPROVED
EXPLICIT_THRESHOLD_PATH_REQUIRES_NEW_OBLIGATION
~~~

## 1. 쉬운 설명

기존 공식에는 “실제 오차 = 어떤 상수 × \(c_\gamma\) × 나머지”처럼 적힌 부분이 있다.
\(c_\gamma\)가 1보다 작으면 이것은 오차를 더 작게 만들어 주는 할인과 같다. 새로 확인한
peer-reviewed 논문은 원래 가정만으로는 이 할인을 붙일 수 없고, 안전하게 증명되는 것은
“어떤 상수 × 나머지”까지라고 지적한다.

이것이 곧 기존 prime-gap 정리가 틀렸다는 뜻은 아니다. \(z\)를 \(L\)보다 충분히 크게 잡으면
더 강한 형태를 되살릴 수 있고, 정성적 “충분히 크면” 논증에서는 다른 큰 오류항이 이를
덮을 수 있다. 그러나 우리 연구는 “충분히 큰 숫자가 구체적으로 얼마인가”를 묻는다.
그러므로 얼마나 크게 잡아야 하는지, 할인율이 최소 얼마인지까지 숫자로 증명해야 한다.

## 2. provenance와 확인 범위

| source | 식별자 | 로컬 증거 | 확인 위치 |
|---|---|---|---|
| Kuperberg, *Sums of singular series with large sets and the tail of the distribution of primes* | DOI 10.1093/qmath/haad030; arXiv:2210.09775v2 | PDF SHA-256 653dcd731f11c6bab47fa61989b31f50dc3318464fc4d300276698045ba48939 | PDF 16–19쪽, 특히 Lemma 4.3 |
| Castillo et al., *Bounded gaps between primes in number fields and function fields* | DOI 10.1090/S0002-9939-2015-12554-3; arXiv:1403.5808 | PDF SHA-256 af2f402f1d0ecf67ea2b02a18f9cc2384514cb04fc3467807e20b278e3d463ca | PDF 11쪽, Lemma 2.5와 직후 Remark·proof |
| GGPY, *Small Gaps Between Products of Two Primes* | DOI 10.1112/plms/pdn046; arXiv:math/0609615 | 기존 고정 PDF SHA-256 411a638e959e6fa41d9f489477b26a8abe6550f3a61e5f2058ccdc88a6461680 | PDF 9–10쪽, Lemmas 3–4 |
| Maynard, *Dense Clusters of Primes in Subsets* | DOI 10.1112/S0010437X16007296; arXiv:1405.2593 | 기존 고정 출판 PDF SHA-256 8eb9d780353908ae22e910f4e039ebab579ae9bf2e5dd8a83b6e38cf33268098 | 출판본 18–19쪽, Lemmas 8.3–8.4 |

PDF뿐 아니라 두 새 arXiv source archive와 관련 TeX를 대조했다. 정확한 URL, 취득 UTC,
archive·TeX hash는
docs/method/theory/data/Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_v1.json에 보존한다.

## 3. Kuperberg 논문은 HR을 얼마나 대체하는가

### 3.1 실제로 제공하는 구조

Kuperberg는 HR Theorem 5.7과 Lemma 5.4를 명시적으로 따라가며
\(\nu_{\mathcal H}\)에 대해 \(\Omega_1\), \(\Omega_2(\kappa,L)\)를 확인한다.
Lemma 4.3은 충분히 큰 암시적 상수 \(B_L,B_\kappa\)와

\[
L\le\frac{\log z}{B_L},\qquad
\kappa^2\le\frac{\log z}{B_\kappa}
\]

를 가정하고

\[
\frac1{G(z)}
=W(z)e^{\gamma\kappa}\Gamma(\kappa+1)
\left(1+O\!\left(\frac{L+\kappa^4}{\log z}\right)\right)
\]

를 얻는다. proof에는 HR의 recurrence와 Euler product tail 비교가 재현되어 있다.
따라서 “HR 책을 못 읽으니 아무 구조도 확인할 수 없다”는 과거 상태는 더 이상 정확하지 않다.

### 3.2 아직 제공하지 않는 것

- \(B_L,B_\kappa\)의 수치
- proof 안 여러 \(O(k)\), \(O(k^3/\log a)\), \(O(k^4)\)의 multiplier
- 모든 작은 초기 범위를 덮는 cutoff
- 특수 \(\nu_{\mathcal H}\)에서 Maynard Lemma 8.4의 모든 \(\gamma\)로 가는 uniform 전달
- \(r\)회 반복 때의 공통 범위와 누적오차

그러므로 이 논문은 **source 구조 복원에는 매우 유용하지만 numerical certificate는 아니다.**
현재 blocker는 SOURCE_ACCESS 하나가 아니라 RATE, RANGE, SPECIALIZATION이다.

## 4. GGPY Lemma 4 오류항 지적은 맞는가

### 4.1 세 형태의 비교

| 문헌 | 주항 | 오류항 핵심 |
|---|---|---|
| GGPY Lemmas 3–4 | \(c_\gamma\) 포함 | \(c_\gamma L\) 포함 |
| Maynard Lemma 8.3 | \(c_\gamma\) 포함 | \(c_\gamma(1+L)G_{\max}\) 포함 |
| Castillo et al. Lemma 2.5 | \(c_\gamma\) 포함 | \(L G_{\max}(\log z)^{\kappa-1}\), 즉 \(c_\gamma\) 없음 |

Castillo et al.의 Remark는 GGPY와 Maynard의 proof가 더 강한 오류항을 오직 \(z\)가
\(L\)에 비해 더 크다는 추가 가정 아래에서만 지지한다고 명시한다. proof에서는 먼저

\[
G(z)=c_\gamma\frac{(\log z)^\kappa}{\Gamma(\kappa+1)}
+O\!\left(L(\log(2z))^{\kappa-1}\right)
\]

꼴의 절대오차를 만들고, \(c_\gamma\)는 주항 계수 식별에만 들어간다. 따라서 지적은
수식과 proof 양쪽에서 확인된다.

### 4.2 Maynard 출판본 주석과 다른 문제

Maynard 출판본의 주석은 일반 \(\kappa\)에서 \((L+1)^\kappa\)가 필요하다는 문제를 고친다.
이번 지적은 오류항 앞의 \(c_\gamma\) 자체가 정당한가를 묻는다. 두 문제는 별개이며,
\(\kappa=1\)이라고 후자가 사라지지 않는다.

## 5. 현재 증명에 미치는 영향

| 현재 구성요소 | 영향 | 판정 |
|---|---|---|
| H1b-1b Lemma 8.2 multiplier 89 | 독립적인 cutoff/Lipschitz 직접 증명 | 그대로 CLOSED |
| GGPY Lemma 3→4 부분적분 | 절대오차의 경계항+적분항 합 | factor 2 유지 |
| 기존 \(C_4\le2C_3\) 문구 | \(C_3\)가 \(c_\gamma\)-정규화됐다는 가정이 잘못됨 | absolute 표기로 교정 |
| Maynard Lemma 8.4 | 좌표별 \(c_{\gamma,j}\)를 공통 주항에 묶는 단계가 자동이 아님 | 새 hard obligation |
| SIV-07 | 공통 수치 bound 없음 | HARD_BLOCKER 유지 |
| \(X_{\mathrm{cert}}\) | 모든 root dependency 미폐쇄 | OPEN 유지 |
| 기존 actual empirical 결과 | 이 이론축과 독립 | 영향 없음 |

절대오차가

\[
|E_3(u)|\le C_{3,\mathrm{abs}}(L+1)
\]

이면 부분적분으로

\[
|E_4|\le2C_{3,\mathrm{abs}}(L+1)M(F)
\]

를 얻는다. 별도로 \(c_\gamma\ge c_{\min}>0\)을 증명한 경우에만

\[
|E_4|
\le\frac{2C_{3,\mathrm{abs}}}{c_{\min}}\,
c_\gamma(L+1)M(F)
\]

로 바꿀 수 있다. 이 때문에 \(c_{\min}\)은 새 원장 항목이 된다.

## 6. 가능한 repair 경로의 비판적 비교

| 경로 | 장점 | 위험·비용 | 현재 권장 |
|---|---|---|---|
| Kuperberg형 명시적 \(z/L\) gate | 인쇄된 상대오차 구조를 가장 가깝게 보존 | 모든 암시적 상수와 일반 \(\gamma\) 확장이 필요 | 1차 병행 |
| 각 \(c_{\gamma,j}\) explicit lower bound | 논리적으로 단순한 상대오차 환산 | 하한이 매우 작으면 최종 threshold가 폭발 | 우선 계산 가능성 감사 |
| 절대오차 직접 다변수 합성 | 불필요한 최악 하한 손실을 피할 가능성 | 새 증명이며 가장 난도가 높음 | 예비 아이디어 |

먼저 Maynard Lemma 8.4의 실제 \(\gamma_j\)를 정확히 펼쳐 \(c_{\gamma,j}\)의 식과 가능한
초등 하한을 구하는 것이 가장 정보가 많다. 하한이 지나치게 작으면 Kuperberg형 size gate나
직접 합성으로 빨리 방향을 바꿀 수 있다.

## 7. 연구 주장 경계

- 이 감사는 GGPY/Maynard의 최종 bounded-gap 정리를 반박하지 않는다.
- Kuperberg Lemma 4.3을 Maynard의 일반 \(\gamma\)에 그대로 적용하지 않는다.
- 암시적 \(O\)-상수를 1로 두지 않는다.
- \(c_\gamma>0\)라는 정성적 사실을 쓸 수 있는 수치 하한과 혼동하지 않는다.
- 한 root dependency가 교정됐다는 이유로 Sono/FMT 전체 threshold를 계산하지 않는다.

## 8. 다음 작업

1. Maynard Lemma 8.4의 좌표별 \(\gamma_j\), \(c_{\gamma,j}\), \(L_j\)를 식별하는
   H1b-1b-2 proof-obligation 원장을 이번 작업에서 만들었다.
2. 다음에는 \(c_{\gamma,j}\) 초등 하한 경로와 Kuperberg형 \(z/L\) gate를 같은 변수로 비교한다.
3. 가능한 경로가 정해진 뒤에만 \(r\)-fold error를 재합성한다.
4. H1c-1 quantitative character package는 병렬 이론축으로 유지한다.

현재 단계에는 새 Python 패키지나 Lean이 필요하지 않으며 사용자 CPU 실험도 유효한
proof obligation을 닫지 못한다.

## 참고문헌

- Vivian Kuperberg, “Sums of singular series with large sets and the tail of the distribution
  of primes,” *Quarterly Journal of Mathematics* 74 (2023), 1457–1479.
  DOI: 10.1093/qmath/haad030. arXiv:2210.09775.
- A. Castillo, C. Hall, R. J. Lemke Oliver, P. Pollack, L. Thompson,
  “Bounded gaps between primes in number fields and function fields,”
  *Proceedings of the American Mathematical Society* 143 (2015), 2841–2856.
  DOI: 10.1090/S0002-9939-2015-12554-3. arXiv:1403.5808.
- D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yıldırım,
  “Small Gaps Between Products of Two Primes,”
  *Proceedings of the London Mathematical Society* 98 (2009), 741–774.
  DOI: 10.1112/plms/pdn046. arXiv:math/0609615.
- James Maynard, “Dense Clusters of Primes in Subsets,”
  *Compositio Mathematica* 152 (2016), 1517–1554.
  DOI: 10.1112/S0010437X16007296. arXiv:1405.2593.
- H. Halberstam and H.-E. Richert, *Sieve Methods*,
  London Mathematical Society Monographs 4, Academic Press, 1974.
