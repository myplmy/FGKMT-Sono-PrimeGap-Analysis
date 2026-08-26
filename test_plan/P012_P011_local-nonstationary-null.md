# P012 — P011 local/log-x nonstationary recurrence null 후속안

## 상태

`DESIGN_REQUIRED / NOT_IMPLEMENTED / NOT_QUEUED`

P011은 global gap frequency를 모든 plateau에 동일하게 적용해, 초기 구간의 큰 gap
발생을 심하게 과대예측했다. P012의 목적은 이 문제를 줄이기 위해 gap-start 위치를
log-x bin으로 나누고 plateau가 차지한 노출을 뺀 local rate로 기대 재발을 계산하는
것이다.

실행 전에 다음을 사전 고정해야 한다.

1. bin 폭과 shifted-bin sensitivity
2. plateau와 control bin이 겹칠 때의 leave-out 규칙
3. 희소 count의 smoothing 여부와 계수
4. primary directional statistic과 multiple-testing family
5. 같은 `[2,10^9]` 자료 재사용 및 record post-selection 한계

이 선택들을 P011 결과를 본 뒤 임의로 바꾸면 p-value가 해석 불가능해질 수 있으므로,
이번 16시간 queue에는 넣지 않는다. 설계 합의 후 P006 segmented sieve를 재사용하면
예상 CPU 시간은 수분–1시간, RAM 4 GB 미만, disk 2 GiB 미만이다.
