# DEP-R09 Gallagher·Maier·McCurley 원문감사 보고서

- 작성일: 2026-09-11 KST
- 검토 목적: Sono의 numerical PAP 상수
  \(C_{\rm PAP}=1-e^{-2}\), \(D_{\rm PAP}=160\)이 원문에서 실제로 따라오는지 확인
- 상세 수식 정본: [Theory 57](../method/theory/57_Sono_FMT_DEPR09_Gallagher_Maier_McCurley_source_recovery.md)
- 기계 원장: [source recovery v1](../method/theory/data/Sono_FMT_DEPR09_source_recovery_v1.json)
- 최종 판정: `중대한 정규화 간극 발견 / DEP-R09와 X_cert는 OPEN`

## 1. 아주 쉽게 말하면

지금까지 우리는 Sono 논문의 최종 숫자 \(2\times10^{-17}\)가 적용되기 시작하는
\(X_{\rm cert}\)를 찾으려 했다. 이를 집에 비유하면, 최종 숫자는 지붕이고 PAP 정리는
지붕을 받치는 기둥 하나다.

이번에 그 기둥의 원 설계도인 Gallagher, Maier, McCurley 논문을 확보해 다시 읽었다.
그 결과:

- 숫자끼리 곱한 계산은 맞다.
- 하지만 앞 정리에서 그 숫자를 가져오는 과정에 부등식 방향 문제가 있다.
- 원 논문의 `어떤 고정 배수 이하`라는 표현에서 그 고정 배수가 뒤 계산에서 1처럼
  사라졌다.

따라서 현재 결론은 “Sono의 전체 정리가 틀렸다고 확정”이 아니다. 더 정확히는
“출판된 Section 5의 적힌 과정만으로는 그 최종 숫자를 지금 엄밀하게 인증할 수 없다”이다.

## 2. 어떤 원문을 어떻게 읽었나

세 신규 PDF에는 모두 정상 텍스트층이 있었다. OCR은 사용하지 않았다. 텍스트 검색으로
정리 위치를 찾은 뒤, 관련 PDF 페이지를 이미지로 열어 분모·부등호·지수·정리 조건을 직접
대조했다.

| 논문 | 확인한 핵심 | 관련 페이지 |
|---|---|---|
| [Gallagher 1970](<../../article/gallagher1970.pdf>) | density Theorem 6, short-interval Theorem 7, 숨은 `≪` 배수와 \(Q\) 범위 | 논문 pp.335–338 |
| [Maier 1981](<../../article/Maier 1981.pdf>) | Lemma 2에서 Gallagher 정리를 PNT-in-AP로 옮기는 방식 | 논문 pp.260–261 |
| [McCurley 1984](<../../article/McCurley 1984.pdf>) | zero-free region과 family exceptional zero 통제 | 논문 pp.8–9 |

파일 hash와 실제 확인한 물리 PDF 쪽수는 Theory 57과 기계 원장에 고정했다.

## 3. 첫 번째 문제: 상수가 반대 방향으로 커졌다

Sono Proposition 5.3은 대략 다음 뜻이다.

> modulus가 \(Q\) 이하인 Dirichlet \(L\)-function들은, 하나의 가능한 예외를 빼면
> 실수부 1 근처 폭 \(c_{\rm ZFR}/\log(Q(1+|t|))\) 안에 zero가 없다.

이제 modulus와 높이를 모두 \(T\) 이하로 제한하면 분모는
\(\log(T(1+T))\)이고, 이는 \(T\ge2\)에서 \(3\log T\) 이하이다. 따라서 안전하게
가져올 수 있는 Gallagher식 상수는

\[
c_1=\frac{c_{\rm ZFR}}3=\frac1{72}
\]

이다. 그런데 Sono p.536에는

\[
c_1=3c_{\rm ZFR}=\frac18
\]

이라고 적혀 있다. 앞 값보다 9배 크며 Proposition 5.3으로부터 나오지 않는다.

> 쉬운 예: “분모가 원래 것의 최대 3배”라면 전체 분수의 보장값은 원래 상수의
> 3분의 1로 내려가는 것이 안전하다. 상수를 3배로 키우면 반대 방향이다.

## 4. McCurley 원문으로 얼마나 복구할 수 있나

다행히 Sono Proposition 5.3만 거치지 않고 McCurley Theorems 1–2를 직접 조합하면 더 나은
보수적 상수를 얻을 수 있다. \(T\ge13\)에서 modulus와 높이가 \(T\) 이하일 때

\[
c_1=\frac1{24}
\]

인 family zero-free region은 원문 상수로 뒷받침할 수 있다. 더 날카로운 한계는 대략
\(0.0518354\)이지만, 안전한 exact 값 \(1/24\approx0.0416667\)을 repair baseline으로 잡았다.

그러나 Sono가 사용한 \(1/8=0.125\)까지는 올라가지 않는다. 따라서 이 직접 복원은
오류를 완전히 원상복구하지는 못한다.

## 5. 두 번째 문제: 숨은 배수가 사라졌다

Gallagher Theorem 7의 기호 `≪`는 “오른쪽에 어떤 고정 양수 \(K_G\)를 곱하면 상계된다”는
뜻이다. 원문은 그 \(K_G\)와 정리가 시작되는 최초 \(x_G\)를 숫자로 주지 않는다.

Maier도 이 결과를 사용하면서:

- principal term은 “approximately”라고 쓰고,
- nonprincipal term은 지수적으로 작아진다고 쓰며,
- \(D\)를 충분히 크게 고른다고 한다.

이는 존재정리에는 충분하지만, 정확히 \(D=160\)부터 배수가 1 이하라는 뜻은 아니다.
정직한 finite 식은 다음 모양이다.

\[
|E|\le K_G e^{-aD}M.
\]

같은 지수 \(e^{-aD}\)를 유지한 채 \(K_G\)를 지우려면 \(K_G\le1\)을 보여야 한다.
그렇지 않으면 지수 \(a\)를 줄이거나 \(D\)를 더 키우고, 그 비용을 최종 계수식에
반영해야 한다.

## 6. 원문에서 새로 얻은 확실한 범위 정보

Gallagher Theorem 7은

\[
\exp(\sqrt{\log x})\le Q\le x^b
\]

를 요구한다. Maier처럼 \(Q=x^{1/D}\)를 대입하고 \(c_{\rm ZD}=16\)을 쓰면:

- 위쪽 범위에서 \(D\ge160\),
- 아래쪽 범위에서 \(\log x\ge D^2\)

가 필요하다. 따라서 \(D=160\)이면 최소한

\[
x\ge e^{25600}\approx10^{11117.94}
\]

라는 gate가 생긴다.

이 숫자는 매우 크지만 **아직 \(X_{\rm cert}\)가 아니다**. Gallagher 정리 하나의
범위 조건만 통과시키는 값이며, hidden multiplier, principal term, \(\psi\to\pi\), R10–R12가
추가로 남아 있다.

## 7. 최종 \(2\times10^{-17}\)에는 어떤 영향이 있나

기존 인쇄값을 Sono Theorem 3.6에 넣으면 약
`2.00386120461967e-17`이 나와 목표보다 0.193% 정도만 높다.

McCurley 원문에서 안전하게 복원한 \(c_1=1/24\)를 쓰고, 숨은 배수를 아주 낙관적으로
\(K_G=1\)이라고 가정해도:

| 시나리오 | 최종 식의 진단값 | \(2\times10^{-17}\) 대비 |
|---|---:|---:|
| \(D=160\), 실제 복원 exponent | `6.3458e-18` | 약 31.7% |
| exponent product 2를 되찾으려고 \(D=M=480\) | `2.4258e-18` | 약 12.1% |
| McCurley 상수를 더 날카롭게 사용, \(D=160\) | `8.5159e-18` | 약 42.6% |

즉 현재와 같은 나머지 parameter를 그대로 둔 채 이 단계만 보정하면 고정 목표
\(2\times10^{-17}\)이 유지되지 않는다. 숨은 배수를 넣으면 실제 값은 더 나빠질 수도 있다.

이 표가 말하지 않는 것도 중요하다.

- Sono 정리 전체의 반례를 찾은 것이 아니다.
- 실제 maximal prime gap이 기준보다 작다는 관측도 아니다.
- 더 강한 explicit PNT-in-AP 결과나 다른 parameter 최적화로 \(2\times10^{-17}\)을
  되찾을 가능성은 남아 있다.

## 8. 현재 연구 상태의 정확한 변경

| 항목 | 이전 phase-1 표현 | 원문감사 후 표현 |
|---|---|---|
| \(1/80\times160=2\) | exact 대수 PASS | 그대로 PASS, 단 analytic 입력으로는 미인증 |
| McCurley | 전문 미확보 | 전문 statement 확인, direct repair partial |
| Gallagher | multiplier·cutoff 미상 | 전문 확인, 실제로 둘 다 미명시 |
| Maier | 전문 미확보 | 전문 확인, 존재형 `D large`이며 exact 160 미보장 |
| PAP-11 | HARD_BLOCKER | 계속 HARD_BLOCKER, 이유가 더 명확해짐 |
| fixed \(2\times10^{-17}\) | 최종 rate를 찾으면 될 가능성 | PAP 상수 자체의 repair도 필요 |
| \(X_{\rm cert}\) | OPEN | 계속 OPEN |

Theory 56은 “Sono가 인쇄한 숫자를 정확히 옮겨 계산한 phase-1 기록”으로 보존한다.
그 숫자의 analytic 타당성에 관한 최신 정본은 Theory 57과 이 보고서다.

## 9. 다음 우선순위

1. **정정문·저자 설명·강한 대체 정리 확인**
   - 공식 arXiv record와 journal 페이지에서 공개 correction은 찾지 못했다.
   - 저자 문의는 외부 통신이므로 사용자 허가 없이 하지 않는다.
2. **fixed 계수 유지 가능성 감사**
   - Gallagher proof의 \(K_G,x_G\)를 직접 복원하거나 modern explicit PNT-in-AP 정리로
     교체한다.
   - 예상: 문헌·증명 작업 수일–수주; 지금은 사용자 CPU 장시간 계산이 필요하지 않다.
3. **PAP coefficient/parameter 최적화**
   - 실제로 증명된 \((C_{\rm PAP},D_{\rm PAP})\)를 전체 식에 넣고 다른 slack으로
     \(2\times10^{-17}\)을 회복할 수 있는지 본다.
4. **회복 실패 시 연구축 결정**
   - 주축: 더 강한 source를 찾아 fixed \(2\times10^{-17}\) 유지.
   - 보조축: 엄밀히 인증되는 더 작은 coefficient의 \(X_{\rm cert}\) 연구.

현재 권장은 1–3을 먼저 수행하고, 숫자를 임의로 낮추어 연구 목표를 바꾸지 않는 것이다.

## 10. 사용자가 지금 할 일

별도 수행절차 필요없음. 세 PDF는 충분히 읽혔고 추가 설치·OCR·장시간 CPU 계산은 현재
필요하지 않다. 외부 저자 문의 또는 연구 목표의 계수 변경이 필요해질 때 별도로 선택을
요청한다.
