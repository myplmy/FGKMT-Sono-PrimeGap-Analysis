# Sono/FMT DEP-R09 Gallagher·Maier·McCurley 원문 복원

- 작성일: 2026-09-11 KST
- 단계: `DEP-R09 FULL-SOURCE AUDIT / REPAIR INTERFACE`
- 선행 정본: [Theory 56](56_Sono_FMT_DEPR09_numerical_PAP_source_constant_audit.md)
- 기계 원장: [source recovery v1](data/Sono_FMT_DEPR09_source_recovery_v1.json)
- 판정: `FULL_SOURCES_ACQUIRED / SONO_SECTION5_NORMALIZATION_NOT_CERTIFIED / DEP_R09_OPEN`
- 비목적: Sono 정리 전체의 반증, 대체 최종계수 확정, numerical \(X_{\rm cert}\) 계산

## 1. 결론부터

새로 확보한 Gallagher·Maier·McCurley 원문을 전수 대조한 결과, Theory 56에서 확인한
\(D_{\rm PAP}=160\), \(C_{\rm PAP}=1-e^{-2}\)의 **인쇄된 대수**는 맞지만, 이를
analytic theorem으로 만드는 앞 단계는 현재 원문만으로 인증되지 않는다.

핵심 이유는 두 가지다.

1. Sono Proposition 5.3의 분모 \(\log(Q(1+|t|))\)를 Gallagher의
   \(\log T\) 정규화로 옮길 때, 직접 따라오는 상수는 보수적으로
   \(c_{\rm ZFR}/3\)이다. Sono p.536의 \(3c_{\rm ZFR}\)는 그 반대 방향으로
   9배 큰 상수이며 Proposition 5.3에서 따라오지 않는다.
2. Gallagher Theorem 7은 숨은 양의 multiplier를 가진 \(\ll\) 정리다. Maier Lemma 2도
   “approximately”, \(\gg\), “\(D\)를 크게 선택”이라고만 한다. 그런데 Sono는
   \(D=160\)을 고정하면서 그 multiplier를 1로 둔 형태를 사용한다. 원문에는 이를
   정당화하는 수치 multiplier와 최초 적용점이 없다.

따라서 이 문서는 phase 1의 숫자를 조용히 폐기하거나 Sono 정리 전체를 거짓이라고
선언하지 않는다. 대신 **인쇄된 계산**과 **현재 원문으로 인증 가능한 계산**을 분리하고,
수정된 finite PAP가 만족해야 할 정확한 interface를 만든다.

> 쉬운 설명: 계산기에서 `1/80 × 160 = 2`라고 계산한 것은 맞다. 문제는 앞 정리에서
> `1/80`을 가져오는 다리가 성립하는가이다. 원문을 보니 그 다리의 방향과 숨은 배수에
> 빈틈이 있었다. 따라서 마지막 숫자를 다시 계산하기 전에 이 다리부터 고쳐야 한다.

## 2. 원문·판독 방식

| source | 로컬 원문 | 관련 위치 | SHA-256 | 판독 |
|---|---|---|---|---|
| Sono 2025 | `article/AN EXPLICIT LOWER BOUND FOR LARGE GAPS BETWEENSOME CONSECUTIVE PRIMES.pdf` | pp.535–537, Prop.5.3, (5.2)–(5.7) | `a45f84f5fe99e16534773005287d4ca5538f58d86793184f4d28fad1c9c67302` | native text 후 PDF 15–17쪽 화면 대조 |
| Gallagher 1970 | `article/gallagher1970.pdf` | pp.335–338, Thms.6–7, (24), (26), (29)–(30) | `ecac1c9470521e410ac8731d2f57b77eb364f1fdc0bbd1f71813205afe84adcf` | native text 후 PDF 7–10쪽 화면 대조 |
| Maier 1981 | `article/Maier 1981.pdf` | pp.260–261, Lemmas 1–2 | `ca6f2425b850dd5f9d81340d8a4a4c76faf6a947d7486ebf87ff072adbf0a3eb` | native text 후 PDF 4–5쪽 화면 대조 |
| McCurley 1984 | `article/McCurley 1984.pdf` | pp.8–9, Thms.1–2 | `6035c9e290ba4a8bb31ed4afef0e014f49324f33cd978b82450c1bdba204d8ac` | native text 후 PDF 2–3쪽 화면 대조 |

세 신규 PDF 모두 텍스트층이 있어 OCR을 사용하지 않았다. 검색은 native text로 했고,
수식의 분모·부등호·지수와 정리의 quantifier는 렌더링한 원 페이지로 재확인했다.

## 3. Sono Proposition 5.3에서 실제 따라오는 정규화

Sono Proposition 5.3은 \(Q\ge100\)인 primitive character family에 대해, 하나의 가능한
real exception을 제외하면 다음을 준다.

\[
1-\sigma\ge
\frac{c_{\rm ZFR}}{\log(Q(1+|t|))},
\qquad c_{\rm ZFR}=\frac1{24}.
\tag{57.1}
\]

modulus와 높이를 모두 \(T\) 이하로 두면 \(Q=T\), \(|t|\le T\)이고, \(T\ge2\)에서

\[
\log\!\bigl(T(1+T)\bigr)\le3\log T,
\qquad
\frac{c_{\rm ZFR}}{\log(T(1+T))}
\ge \frac{c_{\rm ZFR}}{3\log T}.
\tag{57.2}
\]

따라서 Proposition 5.3만 사용하는 직접 bridge는 \(c_1=c_{\rm ZFR}/3\)이다. 반면 Sono
p.536은 \(c_1=3c_{\rm ZFR}\)라고 적는다. 두 값은

\[
\frac{c_{\rm ZFR}}3=\frac1{72},
\qquad
3c_{\rm ZFR}=\frac18,
\qquad
\frac1{72}\ne\frac18.
\tag{57.3}
\]

이다. 이 차이는 OCR 또는 표기 취향이 아니라 분모를 상계할 때 생기는 부등식 방향의
차이다. 또한 Sono p.536 첫 (5.2) 범위의 `exp(x^(1/2) log x)`처럼 보이는 식은 같은 페이지
아래와 Gallagher 원문의 \(\exp(\sqrt{\log x})\)와 양립하지 않는다. 후자를 정본으로 쓰고
앞 표기는 typographical inconsistency로 기록한다.

## 4. McCurley 원문에서 가능한 직접 보수적 복원

McCurley Theorem 1은 \(M=\max\{k,k|t|,10\}\),
\(R=9.645908801\)에 대해 해당 modulus의 Dirichlet \(L\)-function 곱이

\[
\sigma>1-\frac1{R\log M}
\tag{57.4}
\]

에서 많아야 하나의 zero를 가지며, 가능 zero는 real nonprincipal character의 simple real
zero라고 한다. Theorem 2는 서로 다른 real primitive characters에 대해

\[
\min\{\beta_1,\beta_2\}
<1-\frac1{R_1\log M_1},
\quad
M_1=\max\{k_1k_2/17,13\},
\quad
R_1=\frac{5-\sqrt5}{15-10\sqrt2}.
\tag{57.5}
\]

을 준다. \(T\ge13\), \(k_i\le T\), \(|t|\le T\)이면
\(M,M_1\le T^2\)다. \(R<12\), \(R_1<12\)인 보수적 유리 상계를 쓰면, 같은 modulus에는
Theorem 1을, 서로 다른 moduli에는 Theorem 2를 적용해 다음 좁은 family region을 얻을 수
있다.

\[
c_{1,\mathrm{dir}}:=\frac1{24},
\qquad
\sigma>1-\frac{c_{1,\mathrm{dir}}}{\log T},
\quad |t|\le T,
\tag{57.6}
\]

with at most one simple real exception. 더 날카롭게는 Theorem 1이 병목이므로
\(c_1\le1/(2R)=0.0518354475\ldots\)까지 가능하지만, 이 문서는 exact하고 간단한
\(1/24\)만 repair baseline으로 채택한다. 식 (57.6)의 analytic source 정리 전체는 아직
Lean에 옮기지 않고, 아래 exact 상수 대수만 커널로 검사한다.

## 5. Gallagher Theorem 7의 실제 범위와 숨은 multiplier

Gallagher Theorem 7의 nonexceptional 형태는 어떤 절대상수 \(a,b>0\)에 대해

\[
\sum_{q\le Q}\sum_{\chi\ (\mathrm{mod}\ q)}^{*}
\left|\sum_{x<p\le x+h}\chi(p)\log p\right|
\ll h\exp\!\left(-a\frac{\log x}{\log Q}\right),
\tag{57.7}
\]

uniformly for \(x/Q\le h\le x\) and
\(\exp(\sqrt{\log x})\le Q\le x^b\)다. proof는 \(T=Q^5\)를 택하고, density exponent를
\(c_{\rm ZD}\)라 할 때 \(T^{c_{\rm ZD}}\le x^{1/2}\)를 요구한다. 따라서
\(b=1/(10c_{\rm ZD})\)가 충분하다. \(Q=x^{1/D}\)를 넣으면

\[
\frac{5c_{\rm ZD}}{D_{\rm PAP}}=\frac12,
\qquad c_{\rm ZD}=16,\quad D_{\rm PAP}=160.
\tag{57.8}
\]

아래쪽 범위 \(\exp(\sqrt{\log x})\le x^{1/D}\)에는 추가로

\[
D^2\le\log x,
\qquad
D=160\Longrightarrow \log x\ge25600.
\tag{57.9}
\]

가 필요하다. 이는 새로 복원한 **필요한 source-range gate 하나**일 뿐,
즉 `x>=exp(25600)`, 약 `10^11117.9387`이다. 이 값은 \(u_{\rm PAP}\)나
\(X_{\rm cert}\)가 아니다.

zero-free constant가 \(c_1\)이면 Gallagher proof의 density 절반과 \(T=Q^5\)에서
exponent shape는 \(a_0=c_1/10\)이다. 식 (57.6)을 넣은 repair baseline은

\[
a_0:=\frac{c_{1,\mathrm{dir}}}{10}=\frac1{240},
\qquad a_0D_{\rm PAP}=\frac23.
\tag{57.10}
\]

그러나 (57.7)의 \(\ll\)에는 원문에 인쇄되지 않은 \(K_G>0\)와 최초 \(x_G\)가 있다.
Maier Lemma 2의 nonprincipal contribution을 정직하게 적으면 우선

\[
|E|\le K_G e^{-a_0D}M
\quad (x\ge x_G),
\tag{57.11}
\]

처럼 multiplier를 남겨야 한다. 같은 지수로 multiplier를 지우는 것은 정확히

\[
K_Ge^{-aD}\le e^{-aD}
\quad\Longleftrightarrow\quad K_G\le1
\tag{57.12}
\]

일 때만 가능하다. 지수를 \(a_0\)에서 더 작은 \(a\)로 줄여 흡수하려면 충분조건은

\[
0<K_G,\quad 0\le a<a_0,\quad
\log K_G\le(a_0-a)D
\quad\Longrightarrow\quad
K_Ge^{-a_0D}\le e^{-aD}.
\tag{57.13}
\]

이다. Gallagher와 Maier 원문은 \(K_G\), \(x_G\), 이 흡수에 필요한 수치 \(D\)를 주지
않는다. 그래서 Sono의 exact \(O_{\le}\)와 \(D=160\) 조합은 현재 source chain에서
인증되지 않는다.

## 6. one-sided finite PAP의 교정 interface

정규화 main term을 \(M\ge0\), principal term을 \(P\), nonprincipal error를 \(E\)라 하면
finite 합성 자체는

\[
P\ge(1-\eta)M,\quad
|E|\le K_Ge^{-aD}M
\Longrightarrow
P+E\ge(1-\eta-K_Ge^{-aD})M
\tag{57.14}
\]

이다. 이 대수는 Lean 커널에서 검증한다. 하지만 실제 prime-count statement는 여전히

\[
\pi(u;q,r)\ge
\bigl(1-\eta_{\rm pr}-K_Ge^{-aD}-\eta_{\psi\to\pi}\bigr)
\frac{u}{\varphi(q)\log u}
\tag{57.15}
\]

를 공통의 explicit range, exceptional-modulus exclusion, endpoint·prime-power 보정과 함께
증명해야 한다. 이 analytic statement는 `SOURCE_THEOREM_UNFORMALIZED`이며
`PAP-11`, `R09-10`, \(X_{\rm cert}\)를 닫지 않는다.

## 7. 최종 계수에 대한 진단값

Sono Theorem 3.6의 기존 계수식을 동일하게 평가한 진단은 다음과 같다. 이는 대체 정리의
증명이 아니라, upstream PAP 보정이 fixed \(2\times10^{-17}\)에 미치는 민감도다.

| package | \(C_{\rm PAP}\) | \(D_{\rm PAP}\) | \(M\) | 명목 \(\widehat c\) | 목표 대비 |
|---|---:|---:|---:|---:|---:|
| Sono 인쇄값 | \(1-e^{-2}\) | 160 | 160 | `2.00386120461967e-17` | `100.1931%` |
| direct-McCurley baseline, 낙관적 \(K_G=1\) | \(1-e^{-2/3}\) | 160 | 160 | `6.34579170797843e-18` | `31.7290%` |
| \(a_0D=2\) 회복, 낙관적 \(K_G=1\) | \(1-e^{-2}\) | 480 | 480 | `2.42576263727930e-18` | `12.1288%` |
| sharp \(c_1=1/(2R)\), 낙관적 \(K_G=1\) | \(1-e^{-8/R}\) | 160 | 160 | `8.51587370455379e-18` | `42.5794%` |

여기서 \(M\)은 Theorem 3.6의 common power parameter이므로 \(D_{\rm PAP}\)를 480으로
올린 행에서는 함께 480으로 올렸다. 표는 finite slack, \(K_G\), cutoff를 낙관적으로
무시한 **상한적 진단**이다. 그 상태에서도 현재 같은 parameter package는
\(2\times10^{-17}\)을 보존하지 못한다.

이는 “어떤 다른 증명으로도 Sono 계수를 증명할 수 없다”는 뜻이 아니다. 정확한 판정은
다음과 같다.

```text
Sono Section 5의 인쇄된 Gallagher/Maier 연결만으로는
C_PAP=1-exp(-2), D_PAP=160 및 최종 2e-17을 현재 인증할 수 없다.
```

## 8. DEP-R09 의무 갱신

| ID | 원문감사 후 상태 | 의미·다음 증거 |
|---|---|---|
| R09-01 | `FULL_SOURCE_STATEMENT_CONFIRMED_APPLICATION_BRIDGE_PARTIAL` | McCurley Thms.1–2 확인; direct \(c_1=1/24\) bridge를 완전 형식화해야 함 |
| R09-02 | `FULL_SOURCE_AUDITED_MULTIPLIER_AND_CUTOFF_OPEN` | Gallagher 범위·shape 확인; \(K_G,x_G\) 미명시 |
| R09-03 | `SOURCE_FORM_CONFIRMED_RATE_OPEN` | Jutila \(C_\varepsilon\)와 finite range 계속 OPEN |
| R09-04 | `EXPONENT_SHAPE_EXPLICIT_MULTIPLIER_CUTOFF_OPEN` | \(c_{\rm ZD}=16\), \(D\ge160\), \(\log x\ge D^2\) shape 복원 |
| R09-05 | `FULL_SOURCE_AUDITED_NORMALIZATION_GAP` | Maier proof는 \(D\)를 크게 고르는 존재형; Sono의 exact multiplier 1을 주지 않음 |
| R09-06 | `OPEN` | principal one-sided rate 필요 |
| R09-07 | `HARD_BLOCKER` | nonprincipal \(K_G\), 최초 cutoff, exceptional branch 합성 필요 |
| R09-08 | `OPEN` | \(\psi\to\pi\), prime powers, partial summation, endpoint 필요 |
| R09-09 | `PARTIAL` | exceptional source statement는 확인; actual \(B_0\)·전 변수 uniformity 필요 |
| R09-10 | `HARD_BLOCKER` | R09-01–09 공통 \(u_{\rm PAP}\) 없음 |

`DEP-R09`, `PAP-11`, broad `SIV-07/08/09`, \(X_{\rm cert}\)는 모두 OPEN이다.

## 9. 다음 연구 gate

1. 우선 journal/arXiv의 correction·erratum 또는 저자 설명이 있는지 독립 확인한다.
   2026-09-11 공식 arXiv record와 journal article page의 공개 버전에서는 별도 correction을
   찾지 못했지만, 이는 저자 문의를 대체하지 않는다.
2. fixed \(2\times10^{-17}\) 주축을 유지하려면, Gallagher proof의 모든 \(\ll\) 상수와
   cutoff를 직접 추적하거나 더 강한 modern explicit PNT-in-AP theorem으로 교체한다.
3. 복원된 \((C_{\rm PAP},D_{\rm PAP})\)를 R11 전체 coefficient budget에 넣어 실제로
   \(2\times10^{-17}\)을 회복할 수 있는지 본다. 회복하지 못하면 사용자가
   “더 강한 source 탐색”과 “엄밀하지만 더 작은 coefficient 연구”를 별도 연구축으로
   나눌지 결정해야 한다.
4. 이 문제가 해소되기 전에는 DEP-R10으로 이동할 수는 있어도, R09가 닫힌 것처럼
   R11·threshold calculator로 넘어가지 않는다.

## 10. Lean 검증 경계

식 (57.2)–(57.3), (57.8)–(57.10), (57.12)–(57.14)의 elementary real/rational
관계만 `KERNEL_PASS` 또는 `CONDITIONAL_KERNEL_PASS`로 둔다. McCurley·Gallagher·Maier의
analytic theorem은 premise 없는 project theorem이나 local axiom으로 옮기지 않는다.
`sorry`, `admit`, project-local `axiom`은 사용하지 않는다.

## 11. 참고문헌

- Keiju Sono, [An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes](https://doi.org/10.4418/2025.80.2.2), pp.535–537.
- P. X. Gallagher, [A Large Sieve Density Estimate near sigma=1](https://doi.org/10.1007/BF01403187), pp.335–338.
- Helmut Maier, [Chains of Large Gaps Between Consecutive Primes](https://doi.org/10.1016/0001-8708(81)90003-7), pp.260–261.
- Kevin S. McCurley, [Explicit Zero-Free Regions for Dirichlet L-functions](https://doi.org/10.1016/0022-314X(84)90089-1), pp.8–9.
