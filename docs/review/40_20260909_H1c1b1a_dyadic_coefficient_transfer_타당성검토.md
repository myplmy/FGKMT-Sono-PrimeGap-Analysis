# H1c-1b.1a dyadic dimension·coefficient transfer 타당성 검토

- 작성: 2026-09-09 KST
- 상세 정본:
  [`34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md`](../method/theory/34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md)
- 기계 계약:
  [`Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json`](../method/theory/data/Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json)
- 판정:
  `dimension 보정 타당 / 후속 sigma-y sufficient cutoff EXPLICIT / X_cert OPEN`

## 1. 사용자가 알아야 할 핵심

직전 감사에서는 원문이 \(r\)을 \(x\)에서 고른 뒤 실제 정리를 \(x/2\)에서 호출해,
아주 짧지만 무한히 반복되는 경계구간에서 허용 후보 수를 하나 넘길 수 있음을 발견했다.

이번에는 \(r\)을 처음부터

\[
r=\left\lfloor(\log(x/2))^{1/5}\right\rfloor
\]

로 고쳤다. 이 보정 때문에 Sono의 \(2\times10^{-17}\) 계수를 더 작게 낮춰야 하는지
확인한 결과, **그럴 필요는 없다.**

Sono의 내부 hypergraph 조건에는 원래 \(16/15\), 약 6.67%의 비율 여유가 있다.
차원 보정과 FGKMT의 정확한 \(R\) 선택이 잃는 양은 합쳐서 2.5% 미만으로 묶인다.
남은 Mertens 곱의 위쪽 오차를 4% 이하로 만들면 원래 통과선을 그대로 넘는다.

후속 H1c-1b.1a.1은 Rosser--Schoenfeld Theorem 7을 적용해
\(x\ge2\exp(36^5)\)에서 오차 multiplier가 (1001000/998001<26/25)임을 증명했다.
따라서 **충분한** 수치 cutoff는 현재 있다. 다만 가장 작은 cutoff와 전체 정리의 시작점
\(X_{\mathrm{cert}}\)는 여전히 모른다.

## 2. 무엇을 실제로 증명했는가

\(T=x/2\)와 \(r=\lfloor(\log T)^{1/5}\rfloor\ge36\)에서 다음을 exact하게 보였다.

\[
\frac{5\log r}{\log_2x}>\frac{63}{64},
\qquad
1-\frac{\log4}{\log x}>\frac{104}{105}.
\]

따라서 두 factor의 곱은

\[
\frac{63}{64}\frac{104}{105}=\frac{39}{40}
\]

보다 크다. 여기에

\[
\sigma y\le\frac{26}{25}\,80cx\log_2x
\]

를 가정하면 net factor는

\[
\frac{39/40}{26/25}=\frac{15}{16}.
\]

Sono가 가지고 있던 \(16/15\) 여유와 정확히 맞물려

\[
C>\frac54\log5
\]

를 얻는다. 등호가 아니라 엄격한 부등식이므로 hypergraph gate를 만족한다.

## 3. 타당성 점검

### 강한 점

- \(r\)을 실제 theorem endpoint \(x/2\)에 맞춰 인쇄된 가정을 정확히 지킨다.
- 기존 H1a의 모든 \(r\ge36\) exact 적분비를 재사용하므로 숨은
  \(J_r/I_r\) rate를 새로 가정하지 않는다.
- FGKMT의 실제 \(R=(x/4)^{\theta/3}\)를 반영한다.
- 핵심 endpoint는 정수 거듭제곱과 유리수 항등식으로 검증한다.
- coefficient 보존과 numerical cutoff 완성을 구분한다.

### 남은 제한

- \(26/25\) Mertens gate의 sufficient cutoff는 후속 문서에서 닫혔지만, 최초 \(x\)를
  최적화하지는 않았다.
- \(C\)의 상한, weight moment 전체, common exceptional \(B\), prime-count transfer는
  이번 lemma의 범위 밖이다.
- 따라서 Proposition 9.2나 Hypothesis 1(2)를 닫지 않는다.
- 이 결과 하나로 Sono 부등식이 특정 유한 \(X\)부터 성립한다고 말할 수 없다.

## 4. 원문과의 관계

[Sono](https://doi.org/10.4418/2025.80.2.2)는 pp.541--542에서 150 대신 160을 택한다.
이 선택이 이번 transfer에 필요한 여유를 제공한다.

[FGKMT](https://arxiv.org/abs/1412.5029)는 Section 8에서
\(R=(x/4)^{\theta/3}\)를 쓰고 Proposition 9.2를 \(x/2\)에서 호출한다.
[FMT](https://arxiv.org/abs/1511.04468)는 최대 허용 dimension을 원래 scale에서
선택하지만, 더 작은 admissible dimension을 금지하지 않는다.

표적 검색에서 이 정확한 연결을 이미 정리한 erratum이나 lemma는 찾지 못했다.
이는 문헌 전체에서 없다는 주장이 아니다. 이번 project lemma는 원문 정리를 바꾸는 것이
아니라 서로 다른 scale 사이의 초등 floor/slack 연결을 명시한다.

## 5. 발견한 별도 오류

T1 machine ledger의 `SIV-03`에 \(\sigma y\) main term을

```text
80c*x*log_2(x)/log(x)
```

로 적은 오기가 있었다. 원문은

```text
80c*x*log_2(x)
```

이다. `/log(x)`는 survivor prime count에 붙는다. 이번 proof에서는 원문 식을 사용했고
기계 원장도 교정한다. 기존 empirical 계산이나 actual 실험은 이 오기를 입력으로 쓰지
않았으므로 결과 폐기는 필요 없다.

## 6. 엄밀한 판정

| 질문 | 판정 |
|---|---|
| \(x/2\) 기준 dimension 선택은 타당한가 | `YES` |
| 한 칸 감소가 asymptotic scale을 바꾸는가 | `NO` |
| 실제 \(R\) factor를 포함했는가 | `YES` |
| Sono의 \(c\)를 더 낮춰야 하는가 | `NO`, 충분히 큰 \(x\)에서 |
| \(2\times10^{-17}\) 계수는 유지되는가 | `YES`, 이 보정에 관해서는 asymptotically |
| 그 계수가 성립하는 최초 \(X\)를 얻었는가 | `NO` |
| `SIV-07/08` 또는 P9.2가 닫혔는가 | `NO` |

## 7. 후속 갱신과 다음 권장 순서

H1c-1b.1a.1은 2026-09-09에 완료됐다. 상세 증명은
[`35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md`](../method/theory/35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md)를 따른다.

| 순서 | 작업 | 근거 | 예상시간 |
|---:|---|---|---|
| 1 | H1c-1b.2 common exceptional \(B\) | endpoint마다 다른 \(B\)가 생기면 actual family를 한 번에 고정할 수 없음 | 4--8시간 1차 감사, 증명은 2--5일 이상 가능 |
| 2 | H1c-1b.3 endpoint·\(\psi\to\pi\)·recentring | Bordignon 평균상계를 Maynard의 exact prime-count 문장으로 옮기는 다리 | 3--10일 이상 |
| 3 | H1c-1b.4 density·full error·common cutoff | 앞 입력을 하나의 finite P9.2 package로 합성 | 수일--수주 |
| 4 | 남은 P91/P92/L93/P95 공통 moment budget | good sieve weight 전체를 닫아야 `SIV-07`을 승격 가능 | 수일--수주 이상 |

현재 사용자 PC에서 실행하거나 설치할 것은 없다. Lean과 추가 Python package도 필요하지 않다.

```text
별도 수행절차 필요없음
```
