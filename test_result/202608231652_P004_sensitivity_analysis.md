# P004 Start/End 경계·Local Envelope 민감도 분석 결과

## 1. 한 줄 결과

P003의 end-prime 기준 결과는 정수 `x`에 대해 정확했고 재계산할 필요가 없다. FGKMT 원문형 start-prime 경계를 나란히 계산해 보니 경계 선택의 영향은 63개의 짧은 gap 내부 window, 총 50,016개 정수에만 생겼다. global minimum을 만든 record와 shifted log-bin 결론은 변하지 않았고, 모든 3,747개 저장 수치·정수를 100자리 정밀도로 독립 재계산하여 오류 0건으로 PASS했다.

authoritative run은 `20260823T075238Z_p004_sensitivity`다. 그래프 파일 생성·해시·개수는 자동검증됐고 사용자가 시각적으로도 큰 문제없다고 확인했다.

## 2. 무엇을 알아보려 했는가

P003은 gap이 **끝나는 소수**가 x 이하일 때 그 gap을 `G(x)`에 넣었다. 이것은 Sono의 finite 함수와 사용자가 확정한 canonical 정의다. 반면 FGKMT 원문의 finite 표기는 gap이 **시작하는 소수**가 x 이하일 때 넣는 방식이다.

두 정의는 한 record gap의 시작 소수와 끝 소수 사이에서만 다르다. 이번 실험은 그 짧은 차이가 P003의 최솟값·추세 해석을 바꾸는지, 그리고 local envelope 결과가 임의로 고른 bin 시작점이나 rolling window 크기에 민감한지를 확인했다.

추가로 첫 interval의 큰 값 때문에 후반부가 눌려 보이는 문제를 줄이기 위해 다음 두 그래프를 만들었다.

1. 전체 점을 유지하고 y축 최대를 `10^4`로 제한
2. 첫 interval minimum을 생략하고 y축 최대를 `10^3`으로 제한

## 3. 사용한 두 경계와 엄밀한 의미

record `i`의 gap start, gap, end를 `(s_i,g_i,e_i=s_i+g_i)`라 한다.

Sono-compatible canonical 함수:

\[
G_{end}(x)=\max_{e_i\le x}g_i,
\qquad e_i\le x\le e_{i+1}-1.
\]

FGKMT finite 보조 함수:

\[
G_{start}(x)=\max_{s_i\le x}g_i,
\qquad s_i\le x\le s_{i+1}-1.
\]

모든 계산은 정수 `x`를 대상으로 한다. 따라서 interval minimum은 각각 다음 record 직전의 정수에서 정확히 얻는다.

\[
H_{i,min}^{end}=g_i/F(e_{i+1}-1),
\qquad
H_{i,min}^{start}=g_i/F(s_{i+1}-1).
\]

실수 `X` 전체로 바꾸면 half-open interval의 오른쪽 끝이 포함되지 않으므로 “minimum”이 아니라 다음 jump에서의 좌극한 **infimum**을 써야 한다. 이 이론적 구분은 문서에 명시했으며, 정수 domain인 P003/P004 코드에는 보정할 오류가 없다.

## 4. 데이터·환경·검증

- 분석 범위: `[3,814,280, 10^20]`
- canonical record 수: 84
- 완성된 end/start interval: 각각 64
- paired record: 64
- source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- Python: `W:\miniforge3\envs\FGKMT\python.exe` 3.11.16
- 계산 정밀도: 50 dps, 독립 검증: 100 dps
- 실행시간/exit: 9.466초 / 0
- 전체 단위시험: 47건 PASS
- 독립 검증: 3,747개, issue 0
- 최대 상대오차: `4.79166666666666666666666666667e-40`
- 그래프: PNG/PDF 12개, 모두 존재·비어 있지 않음·SHA-256 기록

## 5. 수행방법을 일상용어로 설명하면

1. 같은 maximal-gap record로 end-prime 기준 계단과 start-prime 기준 계단을 각각 만들었다.
2. 각 계단이 다음 record 직전까지 정확히 이어지는지 확인했다.
3. 두 계단이 다른 위치를 정확히 `[새 gap start, 새 gap end-1]`로 뽑았다.
4. 같은 record의 두 interval minimum을 한 행에 붙여 절대차와 상대차를 계산했다.
5. 기존 10진 decade의 시작점을 0.25, 0.50, 0.75 decade씩 옮겨 minimum이 바뀌는지 확인했다.
6. 최근 record를 보는 rolling window를 3, 8, 15, 30개로 추가했다.
7. record 개수가 아니라 최근 0.5, 1, 2 decade의 x-폭을 보는 envelope를 계산했다.
8. 저장 수치를 사용하지 않고 자연로그를 직접 네 번 중첩한 별도 경로로 모두 재계산했다.
9. 마지막에만 표와 그래프를 생성하고 해석했다.

## 6. Start/End 경계 비교 결과

end-bounded global minimum:

\[
37.81686039672168054712906420750827080243
\]

start-bounded global minimum:

\[
37.81686039812796235781969318162473189002
\]

둘 다 record 50, gap 540에서 발생했다. 상세 범위와 gap start는 다음과 같다.

| 모드 | analysis 범위 | gap start | gap end | gap | interval minimum 위치 | minimum H |
|---|---:|---:|---:|---:|---:|---:|
| end canonical | `[738,832,928,467, 1,346,294,311,330]` | 738,832,927,927 | 738,832,928,467 | 540 | 1,346,294,311,330 | 37.81686039672168 |
| start auxiliary | `[738,832,927,927, 1,346,294,310,748]` | 738,832,927,927 | 738,832,928,467 | 540 | 1,346,294,310,748 | 37.81686039812796 |

두 finite 함수가 다른 window는 63개이며 총 정수 폭은 50,016이다. 가장 큰 pointwise 비는 record 64에서 `1.225108225108...`였고, window는 `[1,693,182,318,746,371, 1,693,182,318,747,502]`다. 이는 같은 x에서 end 함수는 이전 gap 924를, start 함수는 새 gap 1132를 쓰는 경계효과다.

같은 record의 interval minimum 상대차가 가장 컸던 것은 record 21의 약 `0.0001669452`, 즉 약 `0.0167%`였다. 따라서 유한 경계차는 실제로 존재하지만 P003의 global minimum record나 큰 규모의 추세 해석을 바꾸지 않았다.

중요한 라벨 규칙은 다음과 같다.

- end-bounded `H/(2e-17)`만 Sono finite 함수와 직접 같은 ratio다.
- start-bounded 값은 FGKMT finite convention 민감도이며 “Sono ratio”라고 부르지 않는다.
- P003의 end-bounded 결과를 start-bounded 결과로 교체하지 않는다.

## 7. Shifted log-bin 결과

shift `0.25`, `0.50`, `0.75`에서 각각 14, 14, 15개 bin이 만들어졌다. 세 경우 모두 전체 minimum은 동일한 record 50, x `1,346,294,311,330`, gap 540, H `37.81686039672168...`였다.

즉 기존 decade 경계가 우연히 global minimum을 만들어 낸 것은 아니다. 다만 bin별 세부 궤적은 shift에 따라 달라지며, 이 일치는 점근 안정성의 증명이 아니다.

## 8. 추가 rolling window 결과

| 최근 record 수 | 마지막 local minimum H | 전체 window 최저 H |
|---:|---:|---:|
| 3 | 43.13553843132987 | 37.81686039672168 |
| 8 | 41.90652751786737 | 37.81686039672168 |
| 15 | 41.45859052273451 | 37.81686039672168 |
| 30 | 38.89898508738846 | 37.81686039672168 |

짧은 window일수록 최근 변화에 빠르게 반응하고, 긴 window는 과거의 낮은 값을 오래 기억한다. 네 마지막 값이 모두 global minimum보다 높다는 점은 P003의 “최근 local floor 회복” 관찰과 일치한다.

## 9. 고정 x-폭 local envelope 결과

| trailing 폭 | 마지막 local minimum H | 완전한 window의 최저 H |
|---:|---:|---:|
| 0.5 decade | 43.92385901100359 | 37.81686039672168 |
| 1 decade | 41.90652751786737 | 37.81686039672168 |
| 2 decades | 41.90652751786737 | 37.81686039672168 |

record 수가 아니라 실제 x-scale 폭을 고정해도 마지막 local floor는 global minimum보다 높았다. 따라서 P003의 회복 관찰은 record-count window 하나에만 의존하지 않는다. 그래도 window들이 서로 겹치므로 독립 표본으로 취급하거나 p-value를 붙이지 않았다.

## 10. 엄밀한 보정에 대한 최종 판정

### 코드 수정이 필요했던 부분

start/end paired difference가 매우 작을 때 이미 반올림된 두 H를 빼면 cancellation이 생길 수 있었다. 최종 코드는 endpoint F를 100자리 guard precision으로 다시 계산하고 상대차에 `expm1(log(F_end)-log(F_start))`를 사용하도록 보정했다. 이 수정 후 독립 검증 최대 상대오차는 약 `4.79e-40`이고 문제는 0건이다.

### 추가 코드 수정이 필요하지 않은 부분

- P003 integer end-bounded interval minimum `g/F(e_next-1)`
- end-prime jump와 다음 end-prime 자체를 이전 interval에서 제외하는 규칙
- 반복 자연로그 `log_k`와 F/H 계산
- Sono ratio의 canonical end-bounded 적용
- P003 결과·그래프의 재생성

### 향후 이론 부록으로 추가할 수 있는 부분

실수 `X`의 left-limit infimum `g/F(e_next)` 표는 엄밀한 논문 대조에 도움이 될 수 있다. 그러나 이는 현재 정수 실험의 오류 수정이 아니라 domain을 하나 더 정의하는 별도 산출물이다. 추가하더라도 integer minimum과 섞지 않고 별도 열·라벨로 유지해야 한다.

## 11. 실행 감사 추적

1. `20260823T074718Z_p004_sensitivity`: 내부 승인 token 문자열 불일치로 분석 전 중단. 결과 해석 없음.
2. `20260823T074823Z_p004_sensitivity`: 분석은 완료됐으나 극소 paired delta의 cancellation 때문에 독립 검증 FAIL. 결과 해석에서 제외.
3. `20260823T075238Z_p004_sensitivity`: 안정화 후 전체 47 tests, 분석, 100-dps 검증 모두 PASS. 유일한 authoritative run.

실패 로그와 결과 디렉터리는 원인·수정 이력을 남기기 위해 삭제하지 않았다.

## 12. 산출물과 사용자 시각검사 결과

핵심 파일:

- `test_result/run_20260823T075238Z_p004_sensitivity/summary.json`
- `test_result/run_20260823T075238Z_p004_sensitivity/verification_report.json`
- `test_result/run_20260823T075238Z_p004_sensitivity/tables/`
- `test_result/logs/run_20260823T075238Z_p004_sensitivity.log`

요청한 새 PNG:

- `figures/h_interval_trajectory_ymax_1e4.png`
- `figures/h_interval_trajectory_skip_first_ymax_1e3.png`

사용자는 두 그림에서 다음을 확인해 주면 된다.

1. y축 상한이 각각 `10^4`, `10^3`으로 보이는지
2. 두 번째 그림에서 첫 interval minimum이 빠져 후반부 점들이 더 잘 구분되는지
3. 범례·축 글자·점·선이 겹치거나 잘리지 않는지

사용자는 기본 그래프와 추가 y축 제한 그래프가 큰 문제없이 그려졌다고 확인했다. 이는 표현 품질 확인이며 수치 정확성은 별도 자동검증 결과를 따른다.
