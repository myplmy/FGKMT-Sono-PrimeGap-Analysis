# DEP-R09 \(C_J\) loss tree 구조감사 타당성 검토

- 작성일: 2026-09-14 KST
- 기술 정본: [Theory 73](../method/theory/73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md)
- 기계 원장: [C_J loss tree v1](../method/theory/data/Sono_FMT_DEPR09_CJ_loss_tree_v1.json)
- 최종 판정: **상수 정리는 유효하지만 현재 증명 구조로 PAP gate를 닫기에는 불충분**

## 1. 이번에 무엇을 물었는가

앞 단계에서 위험한 영점들의 기여를 현재 공식에 넣으니, 필요한 상한이 1보다 작아야 하는데
약 21조가 나왔다. 이번에는 그 큰 숫자가 단순히 여러 안전 여유를 너무 많이 곱해서 생긴
것인지 확인했다.

쉽게 말하면 영수증의 각 항목을 펼쳐서 다음을 물었다.

- 같은 물건을 두 번 계산했는가?
- 5라고 잡은 비용을 실제로는 2 이하로 줄일 수 있는가?
- 아주 큰 52나 14994가 어디서 나왔는가?
- 이런 항목을 전부 고치면 합격선까지 갈 수 있는가?

## 2. 답: 중복 계산은 없었지만 보수적인 숫자는 있었다

기존 \(C_J\)는 다음 여섯 비용의 곱이었다.

| 쉬운 이름 | 기존 비용 | 이번에 가능한 개선 |
|---|---:|---:|
| 오차를 절반만 흡수한 여유 | 2 | 거의 1 |
| 같은 문자의 여러 영점을 합친 비용 | 52 | 약 4.15 |
| 분모가 작아질 때의 안전비용 | 5 | 1.6 |
| weighted 평균 비용 | 14994 | 약 8951.67 |
| detector가 작을 때의 비용 | 약 1350.56 | 이번에는 유지 |
| 적분구간이 좁을 때의 비용 | 882 | 약 336.76 |

Theory 70이 residue에 Lemma 3이나 적분면적을 다시 곱하지 않은 것은 맞았다. 즉 큰 숫자의
원인이 단순한 중복 계산 오류는 아니었다. 다만 각 부품을 필요 이상으로 둥글게 올린 부분은
있었고, 그것을 모두 고치면 약 343배 개선된다.

## 3. 개선 뒤의 숫자

한 selected system의 계수는

\[
 9{,}287{,}613{,}243{,}090
 \quad\longrightarrow\quad
 27{,}047{,}476{,}821.77\ldots
\]

로 줄었다. 상당한 개선처럼 보이지만, \(d=186\)에서 Sono 쪽 near-error 예산이 허용하는
계수는 약

\[
 0.0585043
\]

이하다. 따라서 개선한 뒤에도 약 4,620억 배 크다.

비유하면 21조 원짜리 견적을 625억 원까지 줄였지만, 실제 예산은 14센트 정도인 상황이다.
견적 정리는 성공했지만 이 공법으로 목표 예산을 맞출 수 있다고 말할 수 없다.

## 4. 어떤 개선은 효과가 있고, 어떤 개선은 지금 중요하지 않은가

### 지금 실제로 줄인 항목

- 분모의 5는 초등 미분으로 \(8/5\)까지 줄였다.
- residue 52는 averaged scale의 \(q\le Q\) 정보를 보존해 \(710/171\)까지 줄였다.
- weighted source의 정확한 식과 실제 적분 길이를 사용했다.
- 오차가 주항의 절반이 아니라 백만분의 1 이하가 되도록 시작점을 더 크게 잡았다.

### 지금 줄여도 최종 계수는 변하지 않는 항목

contour, Lemma 3, phase 36은 오차가 충분히 작아지기 시작하는 지점을 결정한다. 이 숫자를
줄이면 finite cutoff는 줄지만 \(X\to\infty\)에서 남는 주 coefficient는 줄지 않는다.
따라서 지금 이 항목을 몇 퍼센트 최적화하는 것은 우선순위가 낮다.

### 구조적으로 바꿔야 하는 항목

현재 방식은 \(\theta^{-2}\) 비용을 세 번 지불해 전체가 \(\theta^{-6}\)로 커진다.
허용범위 \(\theta\le1/21\)에서는 이 power만으로도 매우 크다. 이 구조를 바꾸려면 다음 중
하나가 필요하다.

- 훨씬 강한 explicit zero-density theorem,
- 다른 detector 또는 weight,
- 적분에서 좁은 구간 비용을 되돌려 받는 새로운 합성,
- Sono가 인용한 PAP coefficient의 다른 정당화 경로.

## 5. “현재 방법으로 불가능하다”는 증명인가

아니다. 이번 결과는 다음 두 말을 구분한다.

1. **증명된 말:** 우리가 확인한 local 상수 개선만으로는 여전히 약
   \(4.62\times10^{11}\)배 부족하다.
2. **증명하지 않은 말:** Jutila 계열의 어떤 재배열이나 미래의 새 정리도 절대로 성공할 수 없다.

두 번째는 훨씬 강한 불가능성 정리이며 이번 연구가 증명하지 않았다. 따라서 연구 방향은
폐기보다 “숫자 polishing을 중단하고 구조적 대체 정리를 찾는다”가 맞다.

## 6. \(X_{\rm cert}\)에는 어떤 변화가 있는가

아직 numerical \(X_{\rm cert}\)의 상한이나 구간을 얻지 못했다. 이번 결과는 오히려
현재 수식에 매우 큰 \(X\)를 넣는 것만으로는 해결되지 않는다는 판정이다.

- 실제 maximal-gap 데이터가 보장하는 finite empirical threshold와는 다른 문제다.
- prime sweep을 더 오래 실행해도 이 analytic coefficient는 줄지 않는다.
- 그러므로 사용자 CPU를 장시간 쓰는 실험은 현재 가치가 없다.
- 새 density source가 이 coefficient gate를 통과할 전망을 보인 뒤에만 threshold calculator를
  만드는 것이 타당하다.

## 7. 신뢰할 수 있는 범위

이번 계산에서 신뢰할 수 있는 부분:

- baseline factorization의 exact rational identity,
- denominator \(8/5\)의 초등 상계,
- Ramaré--Zuniga exact source coefficient 대입,
- averaged residue \(710/171\)의 유한 상계,
- absorption fraction을 임의 \(1/m\)으로 만드는 cutoff 식,
- \(d=186\) budget과의 고정밀 비교.

여전히 열린 부분:

- source analytic theorem 전체의 Lean 형식증명,
- 새로운 explicit density theorem의 실제 적합성,
- principal·exceptional character와 \(\psi\)-to-\(\pi\) 전달,
- `PAP-11`, `DEP-R09`, fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\).

decimal 값은 120자리 정밀도의 진단값이며 directed interval certificate는 아니다. 결론의 핵심
부등식은 exact fractions와 기호적 cutoff로 별도 보존했다.

## 8. 다음 권장 작업

다음에는 “52를 4로 더 줄이는 작업”을 반복하지 말고, modern explicit zero-density 정리들을
동일한 PAP 변수에 직접 대입해 비교해야 한다. 후보마다 다음 질문에 답해야 한다.

1. \(q\le X^{1/d}\), \(T=q^5\) 규모를 실제로 덮는가?
2. 1에 아주 가까운 영점까지 multiplier가 숫자로 주어지는가?
3. \(d\le186\)에서 적분한 전체 기여가 \(e^{-2}\)보다 작아지는가?
4. “충분히 큰”이나 숨은 \(O\)-상수를 다시 남기지 않는가?

이 조건을 만족하는 후보가 없다면, Sono의 fixed coefficient를 현재 공개 source만으로 독립
인증할 수 있는지 자체를 다시 평가해야 한다.

## 9. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- O. Ramaré and S. Zuniga-Alterman,
  *An \(L^2\)-bound for the Barban--Vehov weights*,
  DOI [10.7169/facm/241018-19-5](https://doi.org/10.7169/facm/241018-19-5),
  arXiv [2405.12662](https://arxiv.org/abs/2405.12662).
