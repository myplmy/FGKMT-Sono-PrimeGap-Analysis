# P006 maximal-gap plateau recurrence pilot 결과 분석

## 최종 판정

`EXPERIMENT_PASS — exact [2,10^8] consecutive-prime pilot`

사용자 실행 `20260823T190035Z_p006_pilot1e8`은 `[2,100,000,000]`의 모든 소수를 segmented sieve로 생성하고 모든 consecutive-prime gap을 처리했다. 알려진 `pi(10^8)` 값, validated maximal-record 목록, saved artifact hash와 재계산 검사를 모두 통과했다.

사용자가 제시한 log 경로에는 `logs`가 빠져 있었고 실제 파일은 `test_result/logs/run_20260823T190035Z_p006_pilot1e8.log`에 있었다. 결과 판정에는 실제 파일을 사용했다.

## 실행 증거

- log SHA-256: `539d9b6168ecd027497f9d33efe7ae302ef3e724610e81dc2b699dec6f099b14`
- result directory: `test_result/run_20260823T190035Z_p006_pilot1e8`
- source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated record CSV SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- segment span: 10,000,000
- GPU: 미사용
- unit tests: 61/61 PASS, 4.594초
- actual analysis elapsed: 1.151306초
- runner wall-clock: 파일 UTC 시각 기준 약 11초
- saved verification: artifact 12개, issue 0

## 정확성 교차검증

| 항목 | 관측값 | 기준 | 판정 |
|---|---:|---:|---|
| prime count | 5,761,455 | `pi(10^8)=5,761,455` | PASS |
| gap count | 5,761,454 | prime count−1 | PASS |
| reconstructed records | 25 | reference records 25 | PASS |
| complete plateaus | 24 | 다음 record가 범위 안에 존재 | PASS |
| right-censored plateau | 1 | 마지막 gap 220 plateau | PASS |
| end boundary | `[e_k,e_(k+1)-1]` | 계획 정의 | PASS |
| start exposure | `[s_k,s_(k+1))` | recurrence 표본공간 | PASS |

마지막 record gap 220은 `47,326,693→47,326,913`에서 시작한다. 다음 maximal record가 `10^8` 안에 없으므로 이 plateau는 `10^8`에서 오른쪽이 잘린 censored 자료이며 complete 24개와 같은 통계표본으로 취급하지 않았다.

## 실험이 센 것

각 maximal record gap `G_k`가 유지되는 동안 다음 세 종류를 분리했다.

- `N`: record start `s_k`부터 다음 record start 직전까지 관측한 consecutive-gap start의 수
- `M`: 그중 gap 길이가 현재 record gap `G_k`와 같은 횟수; 최초 record 발생을 포함
- `C=M-1`: 최초 발생을 제외한 재등장 횟수
- `Q=M/N`: 최초를 포함한 같은-gap 비율
- `R=C/(N-1)`: 최초를 제외한 재등장 비율

complete plateau 24개 중 `C>0`, 즉 동일 gap이 최초 이후 적어도 한 번 더 나온 plateau는 10개였다. record index는 `2,3,4,6,10,11,13,15,20,22`다.

가장 큰 `M`은 초기 gap 6 plateau에서 `N=15, M=7, C=6`이었다. 큰 x의 예로 gap 154 plateau는

```text
start exposure: [4,652,353, 17,051,707)
end plateau:    [4,652,507, 17,051,886]
N=768,569, M=3, C=2
Q=3.9033580589e-6
R=2.6022420918e-6
```

였다. 반면 마지막 complete gap 210 plateau는 `N=1,530,229, M=1, C=0`, `Q≈6.53497e-7`이었다. 이 pilot에서는 record가 커질수록 동일 gap의 재등장 비율이 매우 작아지는 모습이 보이지만, 24개의 선택된·의존적인 plateau만으로 점근 법칙을 확정할 수는 없다.

## figure별 설명

각 figure는 같은 설계를 PNG와 PDF로 저장해 총 6파일이다. PNG는 모두 1800×1080이고 PDF도 정상적인 비어 있지 않은 파일이며 manifest hash가 일치했다. 사용자는 세 그래프를 직접 보고 큰 시각적 문제가 없다고 확인했다.

### `p006_plateau_occurrences`

가로축은 maximal-gap record index, 세로축은 log scale의 횟수다.

- `M`: 현재 record gap과 같은 gap이 exposure 동안 나온 총횟수로 최초 발생 포함
- `C=M-1`: 최초를 뺀 순수 재등장 횟수

`C=0`은 log 축에 표시할 수 없어 그 점은 C 선에서 빠진다. 따라서 C 선이 없는 위치는 데이터 누락이 아니라 “재등장 0회”다. 이 그림은 초기 작은 gap은 여러 번 반복되지만 뒤의 큰 record gap은 대부분 한 번만 관측된다는 사실을 보여준다.

### `p006_plateau_rates`

가로축은 record index, 세로축은 log scale의 비율이다.

- `Q=M/N`: 최초 포함 동일-gap 비율
- `R=C/(N-1)`: 최초를 제외한 recurrence 비율

plateau마다 길이와 검사 기회 `N`이 크게 다르므로 occurrence 원수치만 비교할 때의 노출량 차이를 보정한다. `R=0`인 점은 log 축에서 빠진다. 후반부 값이 대체로 `10^-6` 안팎까지 작아지는 것은 관측 사실이지만, Poisson 독립성이나 일정한 rate를 증명한 것은 아니다.

### `p006_plateau_lifetimes`

가로축은 record index, 세로축은 linear scale의 자연로그 비율이다.

- `L_end=ln(e_(k+1)/e_k)`: canonical end-bounded plateau의 multiplicative lifetime
- `L_start=ln(s_(k+1)/s_k)`: recurrence를 센 start-exposure의 multiplicative lifetime

두 경계 정의가 대부분 가까우면서도 완전히 같지는 않음을 보여준다. 가장 긴 complete end lifetime은 gap 34 plateau의 `L_end≈1.95219`, 즉 end prime이 약 7.044배가 될 때까지였고, 가장 짧은 것은 gap 118 plateau의 `L_end≈0.005676`, 약 1.00569배였다.

## 쉬운 해석

새로운 최고 기록 gap이 나오면 그 기록은 다음 더 큰 기록이 나올 때까지 “챔피언”으로 남는다. P006은 그 챔피언 기간 동안 똑같은 길이의 gap이 또 몇 번 나왔는지를 모든 소수에서 직접 셌다.

초기의 작은 챔피언 gap은 같은 길이가 자주 다시 나오지만, 수가 커질수록 검사한 gap 수 `N`은 매우 많아지는 반면 같은 길이 재등장은 드물었다. 다만 이번 범위는 `10^8`까지이고 complete plateau가 24개뿐이므로, 이 모양을 `10^20`까지 그대로 이어진다고 말하면 안 된다.

## 한계와 다음 게이트

- `[2,10^8]` pilot 결과이며 P003의 `10^20` record-only 분석과 범위·데이터가 다르다.
- censored gap 220 plateau는 complete 통계에서 제외해야 한다.
- record-selected plateau들은 독립·동일분포 표본이 아니다.
- 작은 표본이므로 회귀·분포 fitting은 아직 수행하지 않았다.
- 확대는 먼저 `[2,10^9]` full runner를 사용자 승인 하에 실행한 뒤 처리량과 memory를 다시 판단한다.
