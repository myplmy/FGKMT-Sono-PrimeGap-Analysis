# DEP-R09 hybrid·smoothing·cancellation 전달 타당성 검토

- 작성일: 2026-09-14 KST
- 기술 정본: [Theory 75](../method/theory/75_Sono_FMT_DEPR09_hybrid_smoothing_cancellation_transfer_feasibility.md)
- 기계 원장: [transfer feasibility v1](../method/theory/data/Sono_FMT_DEPR09_transfer_feasibility_v1.json)
- 최종 판정: **간단히 섞거나 평범하게 부드럽게 만드는 방법으로는 현재 수치 장벽을
  넘지 못하며, 큰 개선에는 부호를 버리기 전 단계의 새 정리가 필요하다**

## 1. 무엇을 알아보았나

앞 단계에서는 완전히 숫자로 적힌 두 안전견적을 얻었다. 하나는 Ramaré의 정리이고,
다른 하나는 우리가 상수를 줄인 Jutila 경로다. 이번 질문은 세 가지였다.

1. 매 지점에서 둘 중 더 좋은 견적만 쓰면 충분한가?
2. $[X,2X]$ 구간의 양 끝을 부드럽게 처리하면 위험한 영점의 영향을 크게 줄일 수 있는가?
3. 양수와 음수가 서로 지워지는 현상을 보존하면 큰 상수 손실을 없앨 수 있는가?

## 2. 결론을 숫자로 보면

필요한 전체 오차 예산은 약 $0.1353$이다. 그런데 두 견적 중 작은 쪽을 매번 골라도
첫 번째 얇은 구간의 안전견적은 최소 약 $8602.03$이었다.

| 비교 | 값 |
|---|---:|
| pointwise minimum의 첫-slice 최저 안전견적 | $8602.030894\ldots$ |
| 허용 예산 | $0.135335\ldots$ |
| 필요한 추가 감쇠율 | $0.0000157329\ldots$ |
| 표준 $[1,2]$ 비음수 smoothing의 보수적 전달 하한 | $0.967531\ldots$ |
| 실제 첫 slice에서의 전달 하한 | $0.995881\ldots$ |

즉 smoothing은 약 10만 분의 1.57 수준까지 줄여야 하지만, 영점 높이에 관한 새 정보를
쓰지 않는 표준 안전평가는 원래 값의 96.7% 이상을 남긴다.

> **일상적인 비유:** 8,602kg을 0.135kg 아래로 줄여야 하는데, 현재 완충재는 아무리
> 잘 골라도 96% 이상을 통과시킨다. 완충재의 모양을 조금 바꾸는 일보다 힘이 서로
> 상쇄되는 구조 자체를 계산하는 새 방법이 필요하다.

## 3. “둘 중 작은 값”도 왜 안 되는가

추가 정보 없이 두 upper bound를 결합할 때는 각 지점에서 작은 값을 고르는 것이 최선이다.
평균을 내거나 일정 비율로 섞으면 작은 값보다 더 커진다.

여기서 8602라는 결론은 두 적분값의 작은 쪽을 취한 것이 아니다. 같은 첫 구간의 모든
지점에서 각각 성립하는 두 transformed-integrand floor를 먼저 구한 뒤, 그 두 floor의
작은 값을 구간 전체에 적분했다. 따라서 일반적으로는 틀릴 수 있는
`두 적분의 최솟값 = 최솟값의 적분` 교환을 사용하지 않았다.

$21\le d\le186$을 전부 비교하고 수식으로 단조성도 확인한 결과, 가장 유리한 곳은
$d=186$의 source 시작점이었다. 그곳에서도 8602를 넘었다. 더 큰 $X$에서는 이 안전견적의
floor가 작아지지 않는다. 따라서 더 큰 소수를 계산하는 것으로 이 증명 상계가 저절로
좋아지지는 않는다.

이 8602는 실제 소수분포 오차를 측정한 값이 아니다. 정리가 주는 최악의 안전견적을
현재 조립법으로 계산했을 때 생기는 하한이다. 실제 오차는 훨씬 작을 수 있다.

## 4. smoothing 판정의 범위를 정확히 제한해야 한다

“smoothing은 모두 실패한다”라고 결론 내리면 과장이다. 이번에 배제한 것은 다음처럼
좁은 방법이다.

- $[X,2X]$를 보존하는 고정 비음수 weight,
- 영점의 세로 위치(height)에 관한 새 정리를 사용하지 않음,
- 모든 height를 하나의 절댓값 최악값으로 덮음.

이 경우 zero frequency에서 Mellin weight가 1에 아주 가까워서 필요한 감쇠를 만들 수 없다.
반대로 영점 높이의 분포와 진동을 함께 제어하는 새 정리가 있거나, $X$에 따라 변하는
부호 있는 weight를 정교하게 만들면 논리적으로 가능성은 남는다. 다만 후자는 소수 개수의
main term이 양수인지, 끝점과 prime power 오차가 얼마인지까지 새로 증명해야 한다.

## 5. cancellation은 왜 현재 자료에서 꺼낼 수 없나

복소수 항들은 방향이 서로 달라 합하면 작아질 수 있다. 그러나 Gallagher의 현 proof는
그 합의 각 항에 먼저 절댓값을 붙인다. 그 뒤에는 “위험한 영점이 몇 개 있는가”라는 양수
목록만 남는다. 방향과 부호를 버린 뒤에는 원래의 상쇄를 복구할 수 없다.

따라서 cancellation을 쓰려면 다음 중 하나가 새로 필요하다.

- 각 residue class에 대해 처음부터 오차를 직접 작게 잡는 fully numerical pointwise PNT,
- 절댓값 이전 character-zero 합의 제곱평균을 충분히 작게 잡는 fully explicit theorem,
- 또는 Maier의 pointwise 단계를 평균형 정보로 대체하는 완전히 새 downstream proof.

“평균적으로 대부분 잘 된다”는 정리만으로는 현재 필요한 특정 good modulus와 모든 residue
class를 자동으로 보장하지 않는다.

## 6. 연구에 미치는 실제 영향

이번 단계에서 얻은 것은 numerical $X_{\rm cert}$가 아니다. 오히려 다음 잘못된 투자를
피하게 해 주는 선별 결과다.

- 두 기존 상계를 단순 혼합하는 추가 최적화는 중단해도 된다.
- source-blind fixed nonnegative smoothing만 더 다듬는 일도 우선순위가 낮다.
- 사용자 CPU로 더 큰 소수 구간을 훑어도 theorem-level 병목은 줄지 않는다.
- 다음 문헌 조사는 “pointwise explicit PNT” 또는 “pre-absolute-value explicit moment”라는
  정확한 규격으로 좁혀야 한다.

현재 상태는 다음과 같다.

| 연구 항목 | 상태 |
|---|---|
| pointwise minimum 수치 gate | 완료, 실패 |
| fixed nonnegative source-blind smoothing gate | 완료, 실패 |
| height-sensitive/signed smoothing 전체 | 미배제, 새 증명 필요 |
| cancellation source | 미확보 |
| `PAP-11`, `DEP-R09` | OPEN |
| fixed $2\times10^{-17}$ 독립 인증 | OPEN |
| numerical $X_{\rm cert}$ 계산 가능 | 아니오 |
| 사용자 장시간 계산 | 필요 없음 |

## 7. 권장 다음 단계

1. published primary source에서 fully numerical pointwise PNT in progressions를 우선 찾는다.
2. 없으면 character sum의 절댓값 이전 단계에 적용 가능한 explicit large-sieve 또는
   second-moment theorem을 조사한다.
3. 적합한 source가 없다는 판정 뒤에만 X-dependent signed minorant를 독립 연구과제로
   설계한다. 먼저 coefficient 필요조건을 통과시킨 후 긴 증명에 들어간다.

이 순서는 이미 실패가 확인된 상수 미세조정을 반복하지 않고, 가장 큰 손실이 실제로 생긴
절댓값 edge를 직접 겨냥한다.

## 8. 형식검증 경계

Lean은 endpoint 유리수 산술, pointwise minimum의 순서 보존, 그리고 가정된 second-moment가
residue-class 오차를 원하는 크기로 옮기는 마지막 대수만 검증한다. Ramaré/Jutila 정리나
새 second-moment theorem을 local axiom으로 가정하지 않았다. `sorry`, `admit`, project-local
`axiom`도 사용하지 않았다.
